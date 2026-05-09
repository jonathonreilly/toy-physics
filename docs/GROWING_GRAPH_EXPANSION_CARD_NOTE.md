# Growing Graph Expansion Card

**Date:** 2026-04-05  
**Status:** bounded analog expansion proxy on a frontier-growing graph

**Audit-lane runner update (2026-05-09):** The primary runner `scripts/growing_graph_expansion_card.py` now carries explicit assertion checks (`assert math.isclose(...)`, `assert abs(...) < EPS`, etc.) mirroring its existing PASS-condition booleans. This makes the runner's class-A invariants visible to `docs/audit/scripts/classify_runner_passes.py`. The runner output and pass/fail semantics are unchanged.

## Artifact chain

- [`scripts/growing_graph_expansion_card.py`](/Users/jonreilly/Projects/Physics/scripts/growing_graph_expansion_card.py)
- [`logs/2026-04-05-growing-graph-expansion-card.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-growing-graph-expansion-card.txt)

## Question

Can a simple frontier-growing graph produce a de Sitter-like spreading proxy,
or does it remain an ordinary local growth rule with a static control?

This card stays deliberately narrow:

- one seed strip
- one frontier-growth rule
- one static control
- one node-count growth proxy
- one radius growth proxy

It does **not** claim a cosmology derivation or a literal de Sitter solution.

## Frozen Result

On the growing-graph toy rule:

- seed size: `35`
- growth steps: `16`
- node count grows from `35` to `1369`
- frontier size grows from `20` to `144`
- mean radius grows from `2.2837` to `14.1520`
- max radius grows from `3.6056` to `25.4558`
- log-slope fit for node count: `1.041` with `R^2 = 0.970`
- log-slope fit for mean radius: `0.519` with `R^2 = 0.970`

Static control:

- node count stays `35`
- mean radius stays `2.2837`
- max radius stays `3.6056`

## Safe Read

The narrow, review-safe statement is:

- the frontier-growing graph expands strongly relative to the static control
- the count growth is close to exponential over the tested window
- the radius growth also accelerates cleanly over the same window
- this is a de Sitter-like spreading proxy on the toy rule, not a cosmology
  derivation

## What This Is Not

- It is not a proof of de Sitter spacetime.
- It is not an inflation model.
- It is not a claim about real cosmological data.

## Final Verdict

**retained analog expansion proxy**
