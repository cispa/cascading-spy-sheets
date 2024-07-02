## Browser Evaluation

### Experiments

- `static/calc.html`: This file contains a simple fuzzer that generates CSS `calc` expressions.
  
  Output = `generate_results/results/calc*`

- `static/env.html`: This file aggregates information from the CSS `env()` function.
  
  Output = `generate_results/results/env`
  
- `static/props.html`: This file collects information about the computed CSS properties of common HTML5 elements.
  
  Output = `generate_results/results/props`
  
- `static/container.html`: This file collects the sizes of elements that are assigned sizes defined by different CSS units and system fonts.
  
  Output = `generate_results/results/*container`

### Running the Server

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 server.py
```

You can now navigate to the calc experiment on the server using http://localhost:3000/calc.
Other experiments can be addressed by their filename.

### Using Different Versions

To use different versions of Firefox and Chromium on a Linux-based system we provide Playwright scripts in `playwright_versions/`.