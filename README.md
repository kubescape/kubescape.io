# kubescape.io Website

This repository contains the source files for the [kubescape.io](https://kubescape.io) website. The website is built using [mkdocs](https://www.mkdocs.org/) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme.

## Prerequisites

- Python
- pip 
- Install the required dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Local Testing

To build and test the site locally:

1. Run the command `mkdocs build`. The site will be built in the `site/` directory.
2. you can run the site locally using the command `mkdocs serve`.

## Production

The site is currently hosted with thanks to Netlify. On each successful push to the repository, the site will be published by their bot.

## Contributing

We welcome contributions from the community. Please read our [contributing guide](https://github.com/kubescape/kubescape.io/blob/main/docs/project/contributing.md) for more information.