#! /usr/bin/env python3

from email.mime.text import MIMEText
import sys

def html_to_eml(html: str, subject: str) -> str:
    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    return msg.as_string()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print(f"Usage: ./generator.py <.eml path> <email_subject>")
        sys.exit(-1)

    with open(args[0], "r") as f:
        html = f.read()
    print(html_to_eml(html, args[1]))