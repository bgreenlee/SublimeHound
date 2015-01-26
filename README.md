# Hound - Hound Search Sublime Text Plugin

Search [Hound](https://github.com/etsy/hound) from within Sublime Text.

## Installation

Install via [Package Control](https://packagecontrol.io/)

## Configuration

There are two required parameters:

- `hound_url` - the location of your hound instance
- `github_base_url` - the base url of where your repositories live

Here are the default settings:

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

