### Evaluation

#### Crawl

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
playwright install

python3 measure_overhead.py
# manually install extension
```

Firefox will wait 20 seconds for you to install the custom extension.
Press the button "Load temporary add-on" and navigate to the `manifest.json` of the extension in the parent directory.

**Note:** The extension will often lead to some site-specific events not being triggered (e.g., `domcontentloaded`). If this happens too often, stop the crawl and try again.

#### Statistics

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 stats.py
```