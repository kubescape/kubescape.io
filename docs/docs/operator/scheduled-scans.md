# Scheduled scans

Scheduled scans are executed by CronJobs running inside your cluster.

By default, the Kubescape posture CronJob runs daily and scans using the frameworks configured at install time via [`defaultFrameworks`](../install-operator.md#default-posture-frameworks).

## Override frameworks for the CronJob only

If you need the scheduled job to scan a different set of frameworks than `defaultFrameworks`, set `kubescapeScheduler.requestBody`:

```yaml
kubescapeScheduler:
  requestBody:
    commands:
      - CommandName: kubescapeScan
        args:
          scanV1:
            targetType: framework
            targetNames:
              - nsa
```

Leave `scanV1` empty (`{}`) to use the install-time `defaultFrameworks` list.
