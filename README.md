# Hound - Hound Search Sublime Text Plugin

Search [Hound](https://github.com/etsy/hound) from within Sublime Text.

## Installation

Install via [Package Control](https://packagecontrol.io/). Open your Command Palette (⇧⌘P), run "Package Control: Install Package", and look for "Hound Search".

## Configuration

There are two required parameters:

- `hound_url` - the location of your hound instance
- `github_base_url` - the base url of where your repositories live

If you want to be able to double-click on search results to open them in Sublime, you'll also need to set:

- `local_root_dir` - the local root directory of your repositories

See below for all settings.

```javascript
/* default settings */
{
    // location of your hound instance
    // e.g. http://hound.example.com
    "hound_url": "",

    // the base url of where your repositories live
    // e.g. https://github.com/youror
    "github_base_url": "",

    // local root directory of your repositories, used for opening files within Sublime
    // e.g. /Users/bob/repositories
    "local_root_dir": "",

    // don't display results from these repos
    // e.g. ["somerepo", "someotherrepo"]
    "exclude_repos": [],

    // custom headers to send with the API request to Hound
    // e.g. {"X-Auth":"s3kret"}
    "custom_headers": {},

    // open double-clicked search results in the browser by default
    // set to false to open in Sublime Text (must have local_root_dir set)
    // shift-double-click will always do the opposite
    "default_open_in_browser": true,

    // set to true to enable debug logging
    "debug": false
}
```

## Notes

Hound sets up double-click handler for search results. The event is forwarded, so it doesn't interfere with the system double-click handler. However, since Sublime Text currently has only a global context for mouse events, if will conflict with any other plugins that also define a double-click handler.

