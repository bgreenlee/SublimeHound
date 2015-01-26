import sublime
import sublime_plugin
import logging
import webbrowser
import subprocess
import re
from collections import OrderedDict
from .lib import requests

logging.basicConfig(format='[Hound] %(levelname)s: %(message)s')
logger = logging.getLogger()

SETTINGS = "Hound.sublime-settings"

class HoundBaseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.settings = sublime.load_settings(SETTINGS)
        self.hound_url = self.settings.get("hound_url")
        self.github_base_url = self.settings.get("github_base_url")
        self.exclude_repos = set(self.settings.get("exclude_repos", []))
        self.custom_headers = self.settings.get("custom_headers", {})
        self.debug = self.settings.get("debug", False)
        if self.debug:
            logger.setLevel(logging.DEBUG)
            # uncomment the following section to enable http request logging
            # try:
            #     import http.client as httplib
            # except ImportError:
            #     import httplib
            # httplib.HTTPConnection.debuglevel = 1
            # requests_log = logging.getLogger("requests.packages.urllib3")
            # requests_log.setLevel(logging.DEBUG)
            # requests_log.propagate = True

        if self.hound_url == "" or self.github_base_url == "":
            self.settings.set("hound_url", self.hound_url)
            self.settings.set("github_base_url", self.github_base_url)
            sublime.save_settings(self.SETTINGS)  # save them so we have something to edit
            sublime.error_message("Please set your hound_url and github_base_url.")
            self.open_settings()
            return

    def open_settings(self):
        sublime.active_window().open_file(sublime.packages_path() + "/User/" + self.SETTINGS)


class HoundCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # get current selection, if any
        if all([region.empty() for region in self.view.sel()]):
            search_text = ""
        else:
            search_text = "\n".join([self.view.substr(region) for region in self.view.sel()])

        self.view.window().show_input_panel("Search:", search_text, self.on_done_input, None, None)

    def on_done_input(self, value):
        self.view.run_command("hound_search", {"query": value})


class HoundSearchCommand(HoundBaseCommand):
    RESULT_VIEW_NAME = "Hound Search Results"

    def run(self, edit, query):
        super(HoundSearchCommand, self).run(edit)
        self.edit = edit
        self.result_view = self.create_result_view()

        result_view_start_point = self.result_view.size()
        self.print_result("Searching for \"%s\"\n" % query)

        repos = self.fetch_repos(self.exclude_repos)

        self.result_view.insert(edit, result_view_start_point + 9, " %d repositories" % len(repos))

        num_matching_files = 0
        search_results = self.fetch_search_results(query, repos)
        for repo, repo_data in search_results.items():
            for file_match in repo_data['Matches']:
                num_matching_files += 1
                self.print_result("\n[%s] %s:\n" % (repos[repo]['name'], file_match['Filename']))
                lines = OrderedDict()
                for line_match in file_match['Matches']:
                    lineno = line_match['LineNumber']
                    num_before = len(line_match['Before'])
                    for i in range(num_before):
                        adjusted_lineno = lineno - num_before + i
                        if not adjusted_lineno in lines:
                            lines[adjusted_lineno] = "% 5d  %s\n" % (adjusted_lineno, line_match['Before'][i])
                    lines[lineno] = "% 5d: %s\n" % (lineno, line_match['Line'])
                    num_after = len(line_match['After'])
                    for i in range(num_after):
                        adjusted_lineno = lineno + i + 1
                        if not adjusted_lineno in lines:
                            lines[adjusted_lineno] =  "% 5d  %s\n" % (adjusted_lineno, line_match['After'][i])

                last_lineno = list(lines)[0]
                for lineno, line in lines.items():
                    if lineno - last_lineno > 1:
                        self.print_result("  ...\n")
                    self.print_result(line)
                    last_lineno = lineno

        # highlight matches
        matching_regions = self.result_view.find_all(query, sublime.IGNORECASE)
        total_matches = len(matching_regions)
        self.result_view.add_regions('a', matching_regions, 'string', '', sublime.DRAW_NO_FILL)
        self.print_result("\n%d matches across %d files" % (total_matches, num_matching_files))
        # scroll back to beginning of matches
        # TODO: figure out how to get this to scroll to the top of the page
        self.result_view.show(result_view_start_point)

    def print_result(self, string):
        # add the given string to the end of the results document
        self.result_view.insert(self.edit, self.result_view.size(), string)

    def create_result_view(self):
        # find an existing results view, or create one
        try:
            result_view = next(view for view in self.view.window().views() if view.name() == self.RESULT_VIEW_NAME)
        except StopIteration:
            result_view = self.view.window().new_file()
            result_view.set_name(self.RESULT_VIEW_NAME)
            result_view.set_scratch(True)
        result_view.set_syntax_file('Packages/Default/Find Results.hidden-tmLanguage')
        result_view.settings().set('line_numbers', False)
        self.view.window().focus_view(result_view)
        if result_view.size() > 0:
            result_view.insert(self.edit, result_view.size(), "\n\n")  # add some spacing
        return result_view

    def api_request(self, uri, params=None):
        url = "%s/api/v1/%s" % (self.hound_url, uri)
        r = requests.get(url, params=params, headers=self.custom_headers)
        response = r.json()
        if self.debug:
            logger.debug("API response: %s" % response)

        return response

    # get the list of searchable repos from Hound
    def fetch_repos(self, exclude_repos=set()):
        repos = self.api_request('repos')
        for repo in exclude_repos:
            del repos[repo]
        for k, v in repos.items():
            repos[k]['base_url'] = v['url'][:-4]
            repos[k]['name'] = repos[k]['base_url'].replace(self.github_base_url, '')
        return repos

    # query Hound
    def fetch_search_results(self, query, repos={}):
        repos_str = ",".join(repos.keys()) if repos else "*"
        search_results = self.api_request("search", params={
            "repos": repos_str,
            "rng": "0:100", # first 100 results
            "i": "fosho",  # ignore case
            "q": query
        })
        return search_results['Results']


class HoundDoubleClickCommand(sublime_plugin.TextCommand):
    def run_(self, counter, args):
        # do default action
        system_command = args["command"] if "command" in args else None
        if system_command:
            system_args = dict({"event": args["event"]}.items())
            system_args.update(dict(args["args"].items()))
            self.view.run_command(system_command, system_args)

        if self.view.name() == "Hound Search Results":
            self.settings = sublime.load_settings(SETTINGS)
            self.github_base_url = self.settings.get("github_base_url")

            # it would be nice if this worked, but for some reason, layout_to_text is inaccurate:
            #   click_layout_location = (args['event']['x'], args['event']['y'])
            #   click_point_location = self.view.layout_to_text(click_layout_location)
            # so, instead, we rely on the above drag_select command and just get the selection
            word_region = self.view.sel()[0]
            # self.view.sel().subtract(word_region) # immediately deselect
            line_region = self.view.line(word_region)
            # look to see if it matches the pattern of a search result, and pull out the line number
            line = self.view.substr(line_region)
            line_match = re.match(r"^\s*(\d+)", line)
            if line_match:
                lineno = line_match.group(1)
                # search upwards until we find the filepath
                (row, col) = self.view.rowcol(word_region.begin())
                while row > 0:
                    row -= 1
                    line_region = self.view.line(self.view.text_point(row, col))
                    line = self.view.substr(line_region)
                    line_match = re.match(r"^\[(.*?)\]\s+(.*?):", line)
                    if line_match:
                        repo = line_match.group(1)
                        filepath = line_match.group(2)
                        url = "%s/%s/blob/master/%s#L%s" % (self.github_base_url, repo, filepath, lineno)
                        url = url.replace("//", "/")
                        webbrowser.open(url)
                        break
