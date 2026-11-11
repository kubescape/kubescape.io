# Scanning a fleet of clusters

Kubescape can scan several clusters in one run and combine what it finds into a single fleet report: one compliance score for the whole fleet, the controls the clusters disagree on, and which clusters it could not scan and why.

This page covers the basics. The full reference, including retries, the summary and the report format, is in [Scanning a fleet of clusters](https://github.com/kubescape/kubescape/blob/master/docs/fleet-scanning.md) in the Kubescape repository.

## Scanning several clusters

Pass the kubeconfig contexts to scan with `--kube-contexts`:

```sh
kubescape scan framework nsa \
  --kube-contexts prod,staging,dr \
  --output report.json --format json \
  --fleet-report fleet.json
```

Kubescape scans the contexts one after another. One cluster failing does not stop the others. When it is done, it:

* writes one report per cluster, named after `--output`: `report.prod.json`, `report.staging.json` and `report.dr.json`
* writes `fleet.json`, the combined report for the whole fleet
* prints a fleet summary with each cluster's status, score and coverage, and the controls the clusters disagree on

`--kube-contexts` works with `kubescape scan`, `scan framework`, `scan control` and `scan workload`. Add `--reference-cluster prod` to compare the other clusters against `prod`.

Every cluster you ask for appears in the fleet report, with one of these statuses:

| Status | Meaning |
|--------|---------|
| `scanned` | The scan completed and the cluster has a report. |
| `unreachable` | The cluster's API server never answered. These clusters are retried, twice by default. Use `--retries 0` to fail fast. |
| `error` | Something answered but the scan failed, for example a request was forbidden. |
| `cancelled` | The run was stopped, by Ctrl-C or `--scan-timeout`, before the cluster finished. |

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Every cluster was scanned and passed. |
| `1` | Every cluster was scanned, but at least one failed a threshold such as `--compliance-threshold`. |
| `2` | At least one cluster could not be scanned, or a report could not be written. |

If one cluster fails a threshold and another could not be scanned, the run exits with `2`. The reports and the summary are still written for the clusters that were scanned.

## Running a fleet scan in CI

This GitHub Actions workflow scans three clusters every morning, fails when any of them could not be scanned or scores below 80%, and keeps the reports as an artifact either way:

```yaml
name: Fleet scan

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  fleet-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Install Kubescape
        run: |
          curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash -s -- -v v4.0.20
          echo "$HOME/.kubescape/bin" >> "$GITHUB_PATH"

      - name: Write the kubeconfig
        env:
          FLEET_KUBECONFIG: ${{ secrets.FLEET_KUBECONFIG }}
        run: |
          mkdir -p ~/.kube
          umask 077
          printf '%s\n' "$FLEET_KUBECONFIG" > ~/.kube/config

      - name: Scan the fleet
        run: |
          kubescape scan framework nsa \
            --kube-contexts prod,staging,dr \
            --output report.json --format json \
            --fleet-report fleet.json \
            --compliance-threshold 80

      - name: Keep the reports
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: fleet-reports
          path: |
            fleet.json
            report.*.json
```

The `FLEET_KUBECONFIG` secret holds a kubeconfig with a context for each cluster. Use credentials that can only read, and make sure the runner can reach every API server. A GitHub-hosted runner can only reach clusters with a public endpoint, so use a [self-hosted runner](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners) for private clusters.

Each cluster's report includes the cluster's resources, and anyone who can read the repository can download the artifact, so run this workflow from a private repository.

The workflow pins the Kubescape version, so a new release cannot change how the job behaves until you update it.

## Keeping the settings in a file

Instead of repeating the fleet flags, you can keep them in a file and pass it with `--fleet-config`:

```yaml
apiVersion: config.kubescape.io/v1alpha1
kind: FleetConfig
metadata:
  name: production
spec:
  contexts: [prod, staging, dr]
  output: report.json
  fleetReport: fleet.json
  referenceCluster: prod
  retries: 2
```

```sh
kubescape scan framework nsa --format json --fleet-config fleet.yaml
```

A flag on the command line overrides the same setting in the file.

## The fleet report

`fleet.json` lists every cluster with its status, score and coverage, the fleet score and which clusters it is based on, every control against the clusters that were scanned, and the controls they disagree on. For example, to list each cluster's status:

```sh
jq '.clusters[] | {clusterID, status, attempts}' fleet.json
```

Its format is described by a [JSON schema](https://github.com/kubescape/kubescape/blob/master/docs/fleet-report.schema.json). Fleet scanning is still in alpha, so the format may change. Ignore fields you do not recognise.
