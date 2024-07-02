## Email Client Fingerprinting PoCs

You can send the corresponding email for an experiment using the sender script.
First, adapt the `sender-config.yml` to an SMTP server you can send emails from.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

./sender.py "your_email" $path_to_eml
```

The .eml files were generated from the .html files using `generator.py`.

### OS Fingerprinting

The email in `osdetect/` distinguishes Windows 11 and Ubuntu 22.04 LTS from
[Mozilla Thunderbird](https://www.thunderbird.net/).

It was tested using Thunderbird 115.12.2.

### Thunderbird vs Apple iCloud Mail

The email in `styledetect/` distinguishes Thunderbird and Apple iCloud Mail on
Windows 11.

It was tested using Thunderbird 115.12.2 and Google Chrome 126.

### Print Detection

The email in `printdetect/` looks different upon being printed. To reproduce
open the printing dialog of the browser (Ctrl + p). The preview should look
different.

It is designed for [Apple iCloud Mail](https://www.icloud.com/mail/) opened with
a Chromium browser. It was tested using Google Chrome 126.

### MS Office Detection

The email in `officedetect/` distinguishes Windows 11 without MS Office
installation from a Windows 11 instance with such an installation. It leverages
font fingerprinting for the font
[Leelawadee](https://learn.microsoft.com/en-us/typography/font-list/leelawadee).

It is designed for [Apple iCloud Mail](https://www.icloud.com/mail/) opened with
a Chromium browser. It was tested using Google Chrome 126.
