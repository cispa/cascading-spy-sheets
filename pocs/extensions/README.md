## Extension Detection

Each HTML file in this directory is a PoC for detecting a specific extension.
All PoCs are blank if an extension is detected and show a message if the extension is not detected, apart from the Mozbar and NoScript PoCs. In the case of Mozbar, the background turns red if the extension is detected and in the case of NoScript a request is issued to `/noscript-detected`. This is visible in the console or network tab. Note that in the case of the Tripadvisor extension the page is not fully blank when the extension is detected. In that case the site still shows a logo, but no text.

List of extensions taken from the [https://github.com/plaperdr/fingerprinting-in-style](artifact) of the paper ["Fingerprinting in Style: Detecting Browser Extensions via Injected Style Sheets"](https://www.usenix.org/system/files/sec21-laperdrix.pdf) by Pierre Laperdrix, Oleksii Starov, Quan Chen, Alexandros Kapravelos and Nick Nikiforakis.

| Extension                                 | Extension ID                                                                                                                             |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| TTSReaderX In-Page Text to Speech         | [pakknklefcjdhejnffafpeelofiekebg](https://chrome.google.com/webstore/detail/ttsreaderx-in-page-text-t/pakknklefcjdhejnffafpeelofiekebg) |
| Touch VPN                                 | [bihmplhobchoageeokmgbdihknkjbknd](https://chrome.google.com/webstore/detail/touch-vpn-secure-and-unli/bihmplhobchoageeokmgbdihknkjbknd) |
| AdBlocker by Trustnav                     | [dgbldpiollgaehnlegmfhioconikkjjh](https://chrome.google.com/webstore/detail/adblocker-by-trustnav/dgbldpiollgaehnlegmfhioconikkjjh)     |
| MozBar                                    | [eakacpaijcpapndcfffdgphdiccmpknp](https://chrome.google.com/webstore/detail/mozbar/eakacpaijcpapndcfffdgphdiccmpknp)                    |
| Disconnect                                | [jeoacafpbcihiomhlakheieifhpjdfeo](https://chrome.google.com/webstore/detail/disconnect/jeoacafpbcihiomhlakheieifhpjdfeo)                |
| TripAdvisor Browser Button                | [oiekdmlabennjdpgimlcpmphdjphlcha](https://chrome.google.com/webstore/detail/tripadvisor-browser-butto/oiekdmlabennjdpgimlcpmphdjphlcha) |
| Awesome Screenshot: Screen Video Recorder | [nlipoenfbbikpbjkfpfillcgkoblgpmj](https://chrome.google.com/webstore/detail/awesome-screenshot-screen/nlipoenfbbikpbjkfpfillcgkoblgpmj) |
| Hunter: Find email addresses in seconds   | [hgmhmanijnjhaffoampdlllchpolkdnj](https://chrome.google.com/webstore/detail/hunter-find-email-address/hgmhmanijnjhaffoampdlllchpolkdnj) |
| NoScript                                  | [doojmbjmlfjjnbmnoijecmcbfeoakpjm](https://chromewebstore.google.com/detail/noscript/doojmbjmlfjjnbmnoijecmcbfeoakpjm)                   |

These extension have fundamentally changed since 2021:
- Cently (Coupons at Checkout)
- Data Scraper - Easy Web Scraping

**Note:**
The extension "Screenshot reader" with id [enfolipbjmnmleonhhebhalojdpcpdoo](https://chrome.google.com/webstore/detail/screenshot-reader/enfolipbjmnmleonhhebhalojdpcpdoo) has changed since submission and no longer injects stylesheets.
