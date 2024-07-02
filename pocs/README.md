## Proof-of-concepts

### OS and Browser Language Fingerprinting

- `poc_chrome.html`: A PoC for Google Chrome. This file distinguishes Windows
  11 and Ubuntu 22.04 LTS using a calc expression. In addition, it
  differentiates the language setting of the browser (en-US vs german).
- `poc_firefox.html`: A PoC for Firefox. This file distinguishes Windows 11 and
  Ubuntu 22.04 LTS using a calc expression.
- `poc_tor.html`: A PoC for the Tor browser. This file distinguishes Windows 11
  and Ubuntu 22.04 LTS using a calc expression and the width of the email
  element. In addition, it differentiates the language setting of the browser
  (en-US vs Malaysian).

### Translation Detection

`poc_chrome_translate.html` is a PoC that showcases how we can fingerprint the
translation feature into Google Chrome. It was tested using Google Chrome 126 on
macOS Sonoma 14.5 and targets the languages English, German and Catalan.

### Extension Detection

`extensiondetect/` contains a set of HTML files designed to detect popular
Chrome Extensions. The extensions are linked in the README of the respective
folder.

The tests with the extensions were conducted on Feb 06, 2024.

### Email Fingerprinting

`mailfingerprint/` contains a set of email-related PoCs that demonstrate how the capabilities of CSS-based fingerprinting translate to email clients.

### Examples

Further examples that showcase our techniques can be found in `examples/`.