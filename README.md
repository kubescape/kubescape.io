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

## Documentation checks

CI uses Python 3.10 and the existing `Pipfile.lock`, without updating the lock or
documentation dependencies. To reproduce that environment locally, keep Pipenv's
export tooling separate from the site's virtual environment:

```bash
mkdir -p tmp/validation
python3.10 -m venv tmp/docs-lock-tools
tmp/docs-lock-tools/bin/python -m pip install pipenv==2026.10.2
tmp/docs-lock-tools/bin/pipenv requirements --hash > tmp/validation/locked-requirements.txt
python3.10 -m venv tmp/docs-venv
tmp/docs-venv/bin/python -m pip install --require-hashes -r tmp/validation/locked-requirements.txt
tmp/docs-venv/bin/python -m pip check
tmp/docs-venv/bin/python -B -m unittest discover -s tests -p 'test_*.py' -v
tmp/docs-venv/bin/python -m mkdocs build --strict --clean
tmp/docs-venv/bin/python scripts/check_links.py internal --site-dir site --report tmp/validation/internal-links.json
```

The build needs network access for the Mermaid plugin's CDN availability check.
The internal link checker runs offline after the build. Strict MkDocs builds alone
do not catch every published path or anchor problem with the pinned MkDocs version.

The checker inspects generated HTML (including blog archives), resource attributes,
`srcset`, and static CSS `url(...)`/`@import` references. It resolves same-site URLs
against the generated files and checks HTML fragment IDs. It does not execute
JavaScript, documentation commands, or third-party applications. Computed resources
and application fragments require separate review. Static example URLs, including
the historical BoB manifests, are declared in `scripts/linkcheck-inventory.json`;
exceptions must match a specific referring page and URL and explain why they exist.

External availability can be checked separately:

```bash
tmp/docs-venv/bin/python scripts/check_links.py external --site-dir site --report tmp/validation/external-links.json
```

| Mode | Exit status |
| --- | --- |
| Internal | `0`: complete, no defects; `1`: missing files/resources/anchors; `2`: incomplete scan or configuration/tool error |
| External | `0`: complete advisory report, even with availability findings; `2`: incomplete scan or configuration/tool error |

Reports include counts, referring pages, original and resolved URLs, exceptions and
unverified destinations. Authentication failures, rate limits and network errors do
not prove a page was deleted. Review redirect destinations and page content before
replacing a link: an unrelated landing page can also return HTTP 200. An external
report is a point-in-time observation, not a guarantee of third-party availability.

The `Documentation integrity` workflow runs the locked build, checker tests and
internal validation on all PRs to `main` and pushes to `main`. Weekly and manual runs
also produce an external report. Diagnostic artifacts are uploaded even when checks
fail. A maintainer must make the **Documentation integrity** status required in the
applicable branch rule and verify it runs for documentation-bot PRs without a bypass;
adding the workflow alone does not block merges. Netlify preview validation remains
separate because hosted build settings are not fully defined in this repository.

## Production

The site is hosted with thanks to Netlify. On each successful push to the repository, the site will be published by their bot. [Read about the GitHub/Netlify integration](https://www.netlify.com/integrations/github/).
