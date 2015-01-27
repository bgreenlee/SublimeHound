# Hound - Hound Search Sublime Text Plugin

Search [Hound](https://github.com/etsy/hound) from within Sublime Text.

## Installation

Install via [Package Control](https://packagecontrol.io/). Open your Command Palette (⇧⌘P), run "Package Control: Install Package", and look for "Hound Search".

## Configuration

There are two required parameters:

- `hound_url` - the location of your hound instance
- `github_base_url` - the base url of where your repositories live

See below for other settings.

```javascript
/* default settings */
{
    // location of your hound instance
    "hound_url": "http://hound.example.com",

    // the base url of where your repositories live
    "github_base_url": "https://github.com/yourorg",

    // don't display results from these repos
    // e.g. ["somerepo", "someotherrepo"]
    "exclude_repos": [],

    // custom headers to send with the API request to Hound
    // e.g. {"X-Auth":"s3kret"}
    "custom_headers": {},

    // Set to true to enable double-click handling in search results. You will
    // need to restart Sublime Text for this to take effect.
    // This defaults to false because Sublime Text currently has only a global
    // context for mouse events, so enabling this will conflict with any other
    // plugins that also define a double-click handler
    "search_results_double_click": false,

    // set to true to enable debug logging
    "debug": false
}
```
