## Email Client CSS Feature Support

### Results

The supported features of the email clients can be found in `css-detection.csv`.
`gen_supported_features.py` generates the table in `table.md` which showcases
the relevant features for CSS-based fingerprinting.

The tested clients are listed in `tested_clients.md`.

### Proxy Usage

`log.txt` shows the user agents which requested external resources on our
server. It highlights which email services use a proxy to fetch such resources.

### Data Collection

Replace `example.com` in this whole directory with your own domain.

On a publically reachable server run `server.py` behind an HTTPS reverse proxy.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 server.py
```

Update the list at the top of `server.py` to reflect which clients you want to
test. Send emails to the respective clients using the `sender*.py` scripts which
uses the `config.yml` which should contain the config for your SMTP server.

Open the emails in the respective clients and the server will log to the CSV
file which requests have reached the server.
