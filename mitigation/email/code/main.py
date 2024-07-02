#!/usr/bin/env python3

from argparse import ArgumentParser
from email import message_from_file, message_from_binary_file

from modify import modify_email

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="PrivacyProxy", description="Parse an email and inline css and images"
    )
    parser.add_argument("infile", help="The email file to parse")
    parser.add_argument("outfile", help="The output file")
    args = parser.parse_args()
    with open(args.infile, "r") as f:
        # email = message_from_binary_file(f)
        email = message_from_file(f)
    email = modify_email(email)
    with open(args.outfile, "w") as f:
        f.write(email.as_string())
