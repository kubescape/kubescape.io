# kubescape.io Website

This repository contains the source files for the [kubescape.io](https://kubescape.io) website. The website is built using [mkdocs](https://www.mkdocs.org/) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme.

## Table of Contents

- [Getting Started](#getting-started)
- [Local Testing](#local-testing)
- [Production](#production)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python installed on your local machine
- pip 

### Setting Up

1. Clone the repository to your local machine.
```bash
git clone https://github.com/kubescape/website.git
```
2. Navigate to the project directory.
```bash
cd website
```
3. Install the required dependencies using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

## Local Testing

To build and test the website locally, follow these steps:

1. Naviagte to project directory and run the command `mkdocs build`. The site will be built in the `site/` directory.
2. After building the website locally, you can run the website locally using the command `mkdocs serve`.

## Production

The site is currently hosted with thanks to Netlify. On each successful push to the repository, the site will be published by their bot.

## Contributing

We welcome contributions from the community. Please read our [contributing guide](https://github.com/kubescape/kubescape.io/blob/main/docs/project/contributing.md) for more information.

## License

This project is licensed under the Creative Commons Attribution 4.0 International License - see the [LICENSE.md](https://github.com/kubescape/kubescape.io/blob/main/LICENSE) file for details.