# Claim Audit Note

**Date:** 2026-04-01  
**Purpose:** compact claim ledger for syncing future README / docs updates after the topology, decoherence, and gravity fixes.

## Safe current claims

1. The corrected propagator still supports positive gravity-like deflection on the retained modular graph family.
2. The IF / CL reduced-description route still supports decoherence on the retained modular family.
3. The modular family is the current joint gravity + decoherence lane.
4. The emergence story is still open: local feedback and soft-pruning rules do not generate a stable hard-gap topology asymptotically.

## Metric caveats to keep explicit

### `gap=0` baseline

- In the modular generator, `gap=0` now behaves as the true uniform-style baseline.
- Do not describe `gap=0` as a channelized modular special case.
- Broad-window claims should be phrased as properties of the modular sweep itself, not as a continuous “uniform to modular” dial.

### `pur_cl` vs `pur_min`

- `pur_cl` is the actual traced CL-bath detector purity.
- `pur_min` is the fully decohered lower-bound / floor metric.
- Phase-diagram pass/fail should be read using the metric the script actually tests.
- Do not swap `pur_min` and `pur_cl` in prose.

### Paired gravity SE

- Gravity significance should be reported from paired per-seed deltas, not from pooled `(seed, k)` samples.
- The old error bars were too optimistic when `k` samples were treated as independent.
- Use the paired-SE wording unless the script explicitly changes again.

### Large-N visibility

- The current large-`N` script now does compute a true single-vs-double-slit visibility gain.
- The old both-slits-open detector-profile contrast still stays high.
- The true visibility gain is only `+0.023` at `N=12`, drops to `+0.002` at `N=18`, and is near zero or negative by `N>=25`.
- So do not describe the asymptotic modular bath lane as preserving strong interference gain.

### Node-removal asymptotics

- Node removal helps at intermediate `N`.
- By `N = 80..100`, the ceiling returns.
- Adaptive/aggressive pruning pushes the graph toward disconnection.
- Treat node removal as a nonlocal pruning surrogate, not a solved local emergence law.

## Recommended wording discipline

- Use “retained modular family” for the joint gravity + decoherence result.
- Use “actual traced purity `pur_cl`” only where the script measures it.
- Use “decoherence floor `pur_min`” only where the lower-bound metric is intended.
- Distinguish clearly between the old detector-profile contrast proxy and the new true visibility gain.
- Use “intermediate-`N` pruning surrogate” for node removal.

## One-line summary

The code now supports a modular-family joint gravity/decoherence result, but the repo should keep its metric language precise: `gap=0` is the true baseline, `pur_cl` and `pur_min` are distinct, gravity SE is paired, true large-`N` visibility gain is weak/gone on the retained modular bath lane, and node removal is asymptotically insufficient.
