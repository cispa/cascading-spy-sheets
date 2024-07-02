#! /usr/bin/env python3

import yaml
import smtplib, ssl
from pathlib import Path
import sys
import re

class MailNotifier:
    def __init__(self, config) -> None:
        if isinstance(config, str) or isinstance(config, Path):
            with open(config, "r") as stream:
                try:
                    config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        if not isinstance(config, dict):
            print(
                f"ERROR - config must be instance of `str`, `pathlib.Path` or `dict`!"
            )
            sys.exit(-1)

        assert "username" in config and isinstance(config["username"], str)
        assert "smtp_port" in config and isinstance(config["smtp_port"], int)
        assert "smtp_server" in config and isinstance(config["smtp_server"], str)
        assert "sender_email" in config and isinstance(config["sender_email"], str)
        assert "password" in config and isinstance(config["password"], str)

        self.config = config

    def sendMail(self, receivers : list, message : str):
        assert isinstance(receivers, list)
        print("[+] Sending mail to " + ", ".join(receivers))
        context = ssl.create_default_context()
        with smtplib.SMTP(
            self.config["smtp_server"], self.config["smtp_port"]
        ) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.config["username"], self.config["password"])
            server.sendmail(self.config["sender_email"], receivers, message)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print(f"Usage: ./sender.py <recipient_email> <.eml files> ...")
        sys.exit(-1)
    
    recipient = args[0]
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", recipient):
        print(f"Usage: ./sender.py <recipient_email> <.eml files> ...")
        print("\t- Recipient email address is invalid!")
        sys.exit(-1)

    email_paths = args[1:]
    if not all(map(lambda x: x.endswith(".eml"), email_paths)):
        print(f"Usage: ./sender.py <recipient_email> <.eml files> ...")
        print("\t- At least one file does not end in `.eml`.")
        sys.exit(-1)

    notifier = MailNotifier("sender-config.yml")
    for path in email_paths:
        with open(path, "r") as f:
            print(f"[+] Sending {path}")
            notifier.sendMail(receivers=[recipient], message=f.read())
            print("[+] Success!\n")
