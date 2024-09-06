# Artifact - Cascading Spy Sheets: Exploiting the Complexity of Modern CSS for Email and Browser Fingerprinting

This repository contains the artifact for our paper "Cascading Spy Sheets:
Exploiting the Complexity of Modern CSS for Email and Browser Fingerprinting"
published at NDSS 2025.

The artifact is citable via the following DOI: [10.5281/zenodo.13712489](https://doi.org/10.5281/zenodo.13712489).

We systematically investigate the modern dynamic features of CSS and their
applicability for script-less fingerprinting, bypassing many state-of-the-art
mitigations. This allows us to infer detailed application, OS, and hardware
configurations at high accuracy. Since our techniques have fewer requirements
than other state-of-the-art fingerprinting techniques, they are applicable to
the restricted setting of email clients.

## Structure

This repository is structured as follows:

- `pocs/`: Contains snippets that are able to differentiate different client
  configurations.
- `evaluation/`: Contains the data and scripts for reproducing our evaluation.
- `mitigation/`: Contains our two proof-of-concept mitigations.
- `LICENSE`: The license file for the repository.

### Proof-of-concepts

- `pocs/browser`: Contains proof-of-concepts that can distinguish different
  browser/OS environments.
- `pocs/email`: Contains proof-of-concepts that can distinguish different email
  client/OS environments.
- `pocs/extensions`: Contains proof-of-concepts that can identify the presence
  of popular Chrome extensions.
- `pocs/examples`: Contains additional examples of CSS fingerprinting
  techniques.

### Evaluation

- `evaluation/browser`: Contains the setup and data used for our data collection
  on popular browsers.
- `evaluation/email`: Contains the setup and data used for our data collection
  on popular email clients.
- `evaluation/translate`: Contains a small evaluation that the translation
  functionality of Google Chrome can be fingerprinted.

### Mitigation

- `mitigation/browser`: Contains our proof-of-concept Firefox extension that
  unconditionally prefetches URLs contained in stylesheets.
- `mitigation/email`: Contains our proof-of-concept email proxy that
  unconditionally prefetches URLs contained in emails and inlines them as data
  URLS. Further, stylesheets are converted to style attributes.

## Reproduction Instructions

### Proof-of-Concepts

For reproduction of the proof-of-concepts we expect access to a Windows 11 and
an Ubuntu 22.04 LTS environment. This can be native or virtual machines. Each
environment should have an installation of Google Chrome, Mozilla Firefox, the Tor Browser and Mozilla Thunderbird.

These environments are required for the PoCs in `pocs/browser/`, `pocs/email/`
and `pocs/extensions/`.

The relevant HTML files:
- `pocs/browser/poc_chrome.html`: Google Chrome on Windows 11 and Ubuntu 22.04 LTS
- `pocs/browser/chrome_translate.html`: Google Chrome on Windows 11
- `pocs/browser/poc_firefox.html`: Mozilla Firefox on Windows 11 and Ubuntu 22.04 LTS
- `pocs/browser/poc_tor.html`: Tor Browser on Windows 11 and Ubuntu 22.04 LTS
- `pocs/browser/extensions/*.html`: Google Chrome on Windows 11

The relevant EML files:
- `pocs/email/osdetect/osdetect.eml`: Mozilla Thunderbird on Windows 11 and Ubuntu 22.04 LTS
- `pocs/email/printdetect/printdetect.eml` (optional): Apple iCloud Mail
- `pocs/email/styledetect/styledetect.eml` (optional): Mozilla Thunderbird and Apple iCloud Mail on Windows 11
- `pocs/email/officedetect/officedetect.eml` (optional): Apple iCloud Mail on Windows 11 with and without MS Office

Some experiments are marked as optional, since they require a license for MS Office or an Apple ID.

### Evaluation

In `evaluation/`, you may run the Python scripts that generate the statistics of the paper.
It also contains the setup used to collect the data.

The relevant scripts:
- `evaluation/browser/generate_results/Results.ipynb`
- `evaluation/email/gen_supported_features.py`

### Mitigation

In `mitigation/browser/eval/`, you may run the crawl on a set of domains from the Tranco list and then calculate the statistics.
Otherwise, you may simply recalculate the statistics of our crawl using the provided script.

In `mitigation/email/` you can run our email privacy scripts on a set of your own emails.
We expect emails to be available as `.eml` files which is a popular export format (e.g., Thunderbird).
The scripts will fetch all remote resources in the emails and inline them as data URLs.