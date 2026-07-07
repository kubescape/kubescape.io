# Profile size and performance

Wildcards and compaction aren't cosmetic. A profile is evaluated **on every exec and every
file open in the workload**, and the matcher is a linear scan — so the *size* of the profile is a
direct, per-event CPU cost. Abstracting a verbose profile into an abstracted SBOB isn't just
tidier; it is measurably cheaper, often by two to three orders of magnitude.

This page shows the cost with numbers you can reproduce.

## Where profiles get big - they burden human and machine

A *learned* or *imported* profile records one observed instance, very often it is the install phase, in which some tools are extremely verbose.

- **Exec arguments.** A process launched many times with different command-lines becomes one entry
  *per command-line*. A real learned profile for a security agent held **1445 exec entries — from
  just 72 binaries** (`bash` alone appeared 329 times, `ps` 305×), because an init system and a rule
  engine spawn the same tools with thousands of unique argument lists.
- **Per-request file opens.** A workload that writes a file per session/request learns one `opens`
  entry per path — tens of thousands of near-identical paths. A real learned Enterprise software profile resulted in 120000 `opens`.


Wildcards and globs collapse the cardinality: `{bash, ["bash", "⋯⋯"]}` or `/srv/svc/cache/*` can make a huge difference. This is
of course only admissible if those files are security irrelevant:

`` A wildcard is justified, if an average analyst needs more time to verify each False Positive than implementing an independent filter ``

## Why size is a per-event cost: the matcher is O(N)

- **Execs** — `MatchExecArgs` is called per entry until one matches (or all are exhausted).
- **Opens** — `CompareDynamic` is called per entry, the same way.

Execs have a memory cost as well, whereas Opens (with exception of pathological cases) do not scale in memory.


## Measured — execs

The real learned agent profile above (**1445** exec entries) vs. its wildcard form (**72** entries,
one `⋯⋯` per binary):

| profile | entries | CPU / event | memory / event | on-disk (etcd) |
|---|---|---|---|---|
| **verbose** (learned) | 1445 | 900 µs | 3.6 MB allocated | ~250 KB |
| **wildcard** (`⋯⋯`) | 72 | 25 µs | 50 KB allocated | ~11 KB |


## Measured — opens

Opens dominate *count* in most profiles, so they matter even more. **50 000 literal opens** (100
directories × 500 per-request files) vs. the **100-entry wildcard** equivalent that covers exactly
the same files (`/srv/svcN/cache/*`):

| profile | entries | CPU / event | on-disk / resident |
|---|---|---|---|
| **verbose** (50 000 literal paths) | 50 000 | **1.38 ms** | 1.38 MB |
| **wildcard** (100 `*` entries) | 100 | **2.65 µs** | 1.79 KB |




## Next

- **[Signing &amp; tamper detection](signing-and-tamper.md)** — sign the compact profile you ship.
