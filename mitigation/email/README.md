## Privacy Proxy

### Usage

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 code/main.py $input_eml $output_path
```

### Testing

Many email clients can directly export `.eml` files. An example is Thunderbird,
where you can export single emails or whole inboxes.

Export a few emails of your inbox and run the scripts on single files, or a
whole directory.

```bash
python3 code/main.py $input_eml $output_path
python3 code/all.py $input_directory $output_directory

# compare sizes of the folders
du -sh $input_directory
du -sh $output_directory
```

### Testing using a Spam Dataset

In the following, we provide instructions on how to test the email privacy proxy
using a part of the [SPAM Archive by Bruce Guenter from untroubled.org](https://untroubled.org/spam/).

**Warning:**
This reveals your IP address to the servers of remote content included in the emails.
If you are concerned about your privacy, you should use a VPN or Tor and consider
running the experiment in a virtual machine.

```bash
wget https://untroubled.org/spam/2024-08.7z
7z x 2024-08.7z
# adding the .eml extension to all files
cd 2024/08/
for file in *; do [ -f "$file" ] && mv "$file" "$file.eml"; done
cd ../..

python3 code/all.py 2024/08/ output/
```

The size of the original emails is 13MB. After running the script, the size of
the `output/` directory is 112MB.

**Note:** Keep in mind that is is merely a proof of concept. The dataset
contains a variety of files with complex MIME structures and encodings. The
script is not optimized for such cases. Further, a set of URLs in the dataset
are not accessible anymore, which may lead to discrepancies for later testing.
