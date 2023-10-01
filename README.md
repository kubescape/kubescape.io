# kubescape.io website

This repository contains the source files for the [kubescape.io](https://kubescape.io) website. 

## Dependencies

The site is built using [mkdocs](https://www.mkdocs.org/) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme.

With Python and `pip` installed, you can install both of these, and all the required dependencies, using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```
## Local development

To make changes to the site: 

1. Clone the repo, create a branch and make your changes
2. Run `mkdocs serve` and connect to the local server on the URL shown (default http://127.0.0.1:8000/)
3. Verify your changes look good, and then submit them via a Pull Request. Please read our [contributing guide](https://github.com/kubescape/kubescape/blob/master/CONTRIBUTING.md) for more information.

If needed, `mkdocs build` will build an entire static copy in the `site/` directory.

## Production

The site is hosted with thanks to Netlify. On each successful push to the repository, the site will be published by their bot. [Read about the GitHub/Netlify integration](https://www.netlify.com/integrations/github/).
