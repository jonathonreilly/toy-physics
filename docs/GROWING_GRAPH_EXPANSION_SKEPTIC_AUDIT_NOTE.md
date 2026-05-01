# Growing Graph Expansion Skeptic Audit Note

**Date:** 2026-04-06  
**Status:** bounded - bounded or caveated result note

## Audited target

Primary target:

- [`docs/GROWING_GRAPH_EXPANSION_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GROWING_GRAPH_EXPANSION_CARD_NOTE.md)

Supporting diagnostic:

- [`docs/GROWING_GRAPH_DYNAMIC_LIMIT_DIAGNOSTIC_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GROWING_GRAPH_DYNAMIC_LIMIT_DIAGNOSTIC_NOTE.md)
- [`logs/2026-04-06-growing-graph-dynamic-limit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-growing-graph-dynamic-limit.txt)

## What survives

The audit confirms a real retained expansion proxy:

- frontier delay grows from `3.000` to `22.000`
- frontier-delay slope is `+0.9325` hops/step
- RMS delay slope is `+0.5981` hops/step
- width slope is `+0.2129` hops/step
- the static control stays flat at frontier delay `3.000`

The same replay also shows the graph-growth signal itself is strong:

- node count grows from `35` to `1395`
- mean delay grows from `2.000` to `13.022`
- mean radius-like spread increases steadily with step

That is enough to retain the graph-growth proxy as a bounded result.

## What does not survive promotion

The audit does not support promoting this lane into a cosmology-style headline:

- the dynamic-propagation visibility drop weakens with size:
  - `0.0492` at `n_layers = 10`
  - `0.0366` at `n_layers = 15`
  - `0.0224` at `n_layers = 20`
- the positive-seed count also falls:
  - `4/10`
  - `4/10`
  - `2/10`
- the signal is therefore noisy, seed-dependent, and not monotone

So the expansion story should stay framed as a graph-expansion proxy, not as
de Sitter-like transport or a cosmology derivation.

## Review-safe conclusion

The honest retained claim surface is:

- frontier expansion on the growing graph is retained
- static control remains flat
- dynamic propagation remains a replacement candidate, not a promoted law
- the cosmology-flavored language is too strong for the present evidence

The narrowest safe summary is:

- keep the graph-distance proxy
- reject dynamic-propagation repair as a promoted mechanism
- keep all transport-like wording out of the claim surface

## Final verdict

**retain graph-distance proxy; demote de Sitter-like wording**
