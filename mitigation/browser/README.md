## Browser Extension Mitigation

### Source

The source code of the Firefox extension is available in `extension/`.
It can be installed using the instruction found [here](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Your_first_WebExtension#installing).

### Testing

A small site can be found in `testcases/` which can be visited with the extension.
You may run the site locally using `python3 -m http.server 3000`.
The site is now reachable via http://localhost:3000.
All external resources should be loaded unconditionally.

### Evaluation

The scripts in `eval/` were used to perform a crawl of the [Tranco Top 200 Sites](https://tranco-list.eu/list/LJ494/200).
The folder contains network traffic statistics with and without the extension.