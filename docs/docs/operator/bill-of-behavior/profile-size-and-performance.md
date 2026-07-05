# Profile size and performance

Wildcards and compaction aren't cosmetic. A Bill of Behavior is evaluated **on every exec and every
file open in the workload**, and the matcher is a linear scan — so the *size* of the profile is a
direct, per-event CPU and memory cost. Abstracting a verbose profile into a few wildcards isn't just
tidier; it is measurably cheaper, often by two to three orders of magnitude.

This page shows the cost with numbers you can reproduce.

## Where profiles get big

A *learned* or *imported* profile records one observed instance, so its size grows with the work the
container did, not the size of its image:

- **Exec arguments.** A process launched many times with different command-lines becomes one entry
  *per command-line*. A real learned profile for a security agent held **1445 exec entries — from
  just 72 binaries** (`bash` alone appeared 329 times, `ps` 305×), because an init system and a rule
  engine spawn the same tools with thousands of unique argument lists.
- **Per-request file opens.** A workload that writes a file per session/request learns one `opens`
  entry per path — tens of thousands of near-identical paths.
- Third-party profile exporters make this worse: a Dynatrace OneAgent profile of ~120 000 entries
  compacts to ~1 500 with wildcards — an ~80× reduction of the same behavior.

Wildcards collapse the cardinality: `{bash, ["bash", "⋯⋯"]}` replaces all 329 `bash` command-lines;
`/srv/svc/cache/*` replaces every file under that directory.

## Why size is a per-event cost: the matcher is O(N)

Detection compares each live event against the profile by scanning its entries:

- **Execs** — `MatchExecArgs` is called per entry until one matches (or all are exhausted → alert).
- **Opens** — `CompareDynamic` is called per entry, the same way.

Both are **O(N)** in the number of entries, run **on every event**. Fewer, wider entries mean a
shorter scan. Two things follow, and the measurements below quantify them.

## Measured — execs

The real learned agent profile above (**1445** exec entries) vs. its wildcard form (**72** entries,
one `⋯⋯` per binary), matching one exec event:

| profile | entries | CPU / event | memory / event | on-disk (etcd) |
|---|---|---|---|---|
| **verbose** (learned) | 1445 | 900 µs | 3.6 MB allocated | ~250 KB |
| **wildcard** (`⋯⋯`) | 72 | 25 µs | 50 KB allocated | ~11 KB |
| **factor** | 20× | **≈ 36×** | **≈ 72×** | **≈ 23×** |

Execs allocate while matching (each comparison builds slices for the argument lists), so the verbose
profile churns **3.6 MB of garbage per exec event** → real GC pressure that scales with N. The
wildcard short-circuits at `⋯⋯`.

## Measured — opens

Opens dominate *count* in most profiles, so they matter even more. **50 000 literal opens** (100
directories × 500 per-request files) vs. the **100-entry wildcard** equivalent that covers exactly
the same files (`/srv/svcN/cache/*`), matching one open event:

| profile | entries | CPU / event | on-disk / resident |
|---|---|---|---|
| **verbose** (50 000 literal paths) | 50 000 | **1.38 ms** | 1.38 MB |
| **wildcard** (100 `*` entries) | 100 | **2.65 µs** | 1.79 KB |
| **factor** | 500× | **≈ 520×** | **≈ 773×** |

That 1.38 ms is **per `open()`**. A workload opening files at even ~700/s would need a **full CPU
core** just to evaluate this one profile; the wildcard form costs ~2 ms/s — effectively free. The
1.38 MB of path strings is held per container in node-agent *and* shipped to etcd and every
node-agent watch.

!!! info "Does memory scale with N too, or just CPU?"
    - **CPU**: always O(N).
    - **Resident / etcd memory**: always O(N) — you store every entry.
    - **Per-event heap allocation**: **zero** for ordinary path shapes (literal or a single trailing
      `*`/`⋯` use a zero-allocation walk), so it does *not* scale with N. It only becomes O(N)
      allocation for the pathological open shape below.

## Getting the abstraction right

Wildcards are a large win, but two shapes need care:

!!! warning "Don't over-compact opens to a bare `/*`"
    Collapsing opens all the way to `/*` matches **every** path — matching becomes trivial, but the
    open signal is **gone**: `R0002` (unexpected file open) can never fire, because every open is now
    "in profile". Compaction shrinks the profile *and can silently disable detection*. Tune
    `CollapseConfiguration` to keep meaningful prefixes (`/srv/svc/cache/*`, not `/*`).

!!! warning "Avoid 2+ non-adjacent `*` in a single open path"
    A path with one `*` (or a trailing `*`) uses a zero-allocation segment walk (~17–120 ns, 0 B). A
    path with **two or more non-adjacent** wildcards — `/var/*/app/*/data` — drops into a
    dynamic-programming matcher that allocates a memo (~1.8 µs and ~3.5 KB **per match**). That is
    ~100× the CPU *and* it allocates. Prefer a single trailing wildcard, or an anchored prefix, over
    scattering `*` through a path.

## How this was measured

The numbers are Go microbenchmarks on the storage matcher
(`pkg/registry/file/dynamicpathdetector`: `MatchExecArgs`, `CompareDynamic`) — the same code node-agent
runs per event — replaying one event against each profile with `-benchmem`. Absolute times are
machine-specific; the **factors and the O(N) scaling are not**. The exec figures use a real recorded
`ApplicationProfile`; the open figures use a modeled 50 000-path high-cardinality set (the regime a
per-request-file workload or an imported OneAgent profile produces).

## Next

- **[End-to-end example](tutorial.md#authoring-a-production-profile-with-wildcards)** — authoring a
  wildcard profile by hand.
- **[Signing &amp; tamper detection](signing-and-tamper.md)** — sign the compact profile you ship.
