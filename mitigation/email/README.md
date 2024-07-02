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

Export a few emails of your inbox and run the scripts on single files, or a whole directory.

```bash
python3 code/main.py $input_eml $output_path
python3 code/all.py $input_directory $output_directory

# compare sizes of the folders
du -sh $input_directory 
du -sh $output_directory
```