#!/usr/bin/env python

import yaml
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import time
from pathlib import Path
import sys

CLIENT_PLACEHOLDER = "XPLACEHOLDERX"

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

    def sendMail(self, receivers, message):
        assert isinstance(receivers, list)
        message["From"] = self.config["sender_email"]
        message["To"] = ", ".join(receivers)
        context = ssl.create_default_context()
        with smtplib.SMTP(
            self.config["smtp_server"], self.config["smtp_port"]
        ) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.config["username"], self.config["password"])
            server.sendmail(self.config["sender_email"], receivers, message.as_string())


clients = {
    # "web-gmail": "",
    # "web-aol": "",
    # "web-outlook": "",
    # "web-icloud": "",
    # "web-yahoo": "",
    # "web-proton": "",
    # "web-roundcube": "",
    # "desktop-thunderbird": "",
    # "desktop-outlook": "",
    # "desktop-apple": "",
    # "desktop-winmail": "",
    # "android-gmail": "",
    # "android-outlook": "",
    # "android-samsung": "",
    # "ios-mail": "",
    # "ios-outlook": "",
    # "ios-gmail": ""
}

if __name__ == "__main__":
    notifier = MailNotifier("config.yml")

    for client in clients:
      msg = MIMEMultipart("mixed")
      msg["Subject"] = "Open in " + client

      html = """\
  <!DOCTYPE html>
  <html>

  <head>
    <style>
      @media (min-width: 8000px) {
        td {
          background-image: url(https://example.com/XPLACEHOLDERX/sanity-no);
        }
      }
      @media (max-width: 8000px) {
        td {
          background-image: url(https://example.com/XPLACEHOLDERX/sanity-yes);
        }
      }
    </style>
  </head>

  <body>
    <table>
      <tr>
        <td>A</td>
        <td>B</td>
        <td>C</td>
      </tr>
    </table>
  </body>

  </html>
      """
      html = html.replace(CLIENT_PLACEHOLDER, client)
      msg.attach(MIMEText(html, "html"))

      print(f"[+] Sending mail to {client} on {clients[client]}")
      notifier.sendMail(
          [
            clients[client]
          ],
          msg,
      )
      time.sleep(1)
