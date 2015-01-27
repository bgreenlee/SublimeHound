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

    // set to true to enable debug logging
    "debug": false
}
```

## Notes

Hound sets up double-click handler for search results. The event is forwarded, so it doesn't interfere with the system double-click handler. However, since Sublime Text currently has only a global context for mouse events, if will conflict with any other plugins that also define a double-click handler.

