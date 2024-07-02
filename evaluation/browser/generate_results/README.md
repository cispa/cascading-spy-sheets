## Results Generation

Running the Jupyter Notebooks:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

jupyter notebook
```

### Results

In `results/` you can find the results for the experiments of the parent folder.
They were collected on the browser/OS combinations listed in the Appendix of the
paper.

- `results/calc`: Contains the results of our calc expression fuzzer on the
  generic tested systems. Corresponds to the `calc.html` experiment.
- `results/calc_arch`: Contains the results of our calc expression fuzzer on
  systems running on ARM or x86. Corresponds to the `calc.html` experiment.
- `results/calc_bit`: Contains the results of our calc expression fuzzer on
  32-bit vs 64-bit browsers. Corresponds to the `calc.html` experiment.
- `results/env`: Contains the values of CSS env variables on mobile Apple
  devices (i.e., iPhones). Corresponds to the `env.html` experiment.
- `results/fontcontainer`: Contains the results of our font fingeprinting using
  CSS units on the tested systems. Corresponds to the `container.html`
  experiment.
- `results/props`: Contains the results of our computed styles difference
  aggregator on the tested systems. Corresponds to the `props.html` experiment.
- `results/valuecontainer`: Contains the default values of CSS units on the
  tested systems. Corresponds to the `container.html` experiment.

### Analysis

`Results.ipynb` produces a matrix of which browser/OS combinations can be
differentiated using the techniques that correspond to the following
experiments:

- `calc.html`
- `container.html`
- `props.html`

Individual results can also be inspected using the generator scripts
`gen_*_results.py`.

### @supports Analysis

`SupportsAnalysis.ipynb` produces a matrix of which browser/OS combinations can
be differentiated using `@supports` queries.

`browser-compat-data.json` built from
[mdn/browser-compat-data](https://github.com/mdn/browser-compat-data) on
[Jan 03, 2024](https://github.com/mdn/browser-compat-data/commit/f809a774bc7d85c27747cd873ab652414b1d07d5).

### Version Analysis

In `version_results/` you find the data that was collected using different
versions of the browsers provided by Playwright. `VersionResults.ipynb` presents
the corresponding matrix of which versions can be differentiated using the
results of our experiments.
