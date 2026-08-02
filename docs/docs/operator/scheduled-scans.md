# Scheduled scans

Scheduled scans are executed by CronJobs running inside your cluster.

By default, the Kubescape posture CronJob runs daily. With an empty `scanV1` (`{}`):

- If [`defaultFrameworks`](../install-operator.md#default-posture-frameworks) is set, those frameworks are scanned.
- If `defaultFrameworks` is empty / omitted, the operator falls back to scanning **all** frameworks (`targetNames: ["all"]`).

!!! note
    Startup scans and exception-triggered rescans use a different empty-list fallback: `allcontrols`, `nsa`, and `mitre` (not `"all"`).

## Override frameworks for the CronJob only

If you need the scheduled job to scan a different set of frameworks than `defaultFrameworks`, set `kubescapeScheduler.requestBody`:

```yaml
kubescapeScheduler:
  requestBody:
    commands:
      - CommandName: kubescapeScan
        args:
          scanV1:
            targetType: Framework
            targetNames:
              - nsa
```

Use `targetType: Framework` (capital **F**) so the operator can also append the `security` framework when `kubescape.triggerSecurityFramework` is enabled (the chart default).

Leave `scanV1` empty (`{}`) to use the install-time `defaultFrameworks` list (or the `"all"` legacy fallback when that list is empty).
