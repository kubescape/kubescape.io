# kubescape.io website

This repository contains the source files for the kubescape.io website.

## Building the site

### Local testing

We use [mkdocs](https://www.mkdocs.org/) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme. 

To build and test locally: 

* [install mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/) with `pip` or Docker 
* run `mkdocs serve`

## Local build

Run `mkdocs build`, and the site will be built in the `site/` directory.

### Production

The site is hosted with thanks to Netlify.  On each successful push to the repository, the site will be published by their bot.