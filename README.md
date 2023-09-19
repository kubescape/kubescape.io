# kubescape.io website

This repository contains the source files for the kubescape.io website.

## Building the site

### Local testing

We use [mkdocs](https://www.mkdocs.org/) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme to built the website. 

To build and test locally: 

* Ensure you have python and pip installed.
* you can install all the required dependencies such as rrs plugin, mkdocs and more using the following command:
```bash 
pip install -r requirements.txt
```
* [install mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/) with `pip` or Docker.
* Once you have all the dependencies installed, run `mkdocs build` and the site will be built in the `site/` directory.
* After building the website locally, you can run the wesbite locally using the command `mkdocs serve`.

### Production

The site is hosted with thanks to Netlify. On each successful push to the repository, the site will be published by their bot.