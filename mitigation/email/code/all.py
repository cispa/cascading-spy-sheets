#!/usr/bin/env python3

from argparse import ArgumentParser
from email import message_from_file, message_from_binary_file
import os

from modify import modify_email

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="PrivacyProxy", description="Parse an email and inline css and images"
    )
    parser.add_argument("indir", help="The directory of email files to parse")
    parser.add_argument("outdir", help="The output file")
    args = parser.parse_args()
    assert os.path.isdir(args.indir) and os.path.isdir(args.outdir)
    for filename in os.listdir(args.indir):
        if filename.endswith(".eml"):
            inpath = os.path.join(args.indir, filename)
            outpath = os.path.join(args.outdir, filename)
            print(f"[+] Working on {inpath}.")
            try:
                with open(inpath, "r") as f:
                    # email = message_from_binary_file(f)
                    email = message_from_file(f)
                email = modify_email(email)
                with open(outpath, "w") as f:
                    f.write(email.as_string())
            except:
                print(f"[!] Error processing {inpath}.")
