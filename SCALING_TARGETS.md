# Scaling Targets

This file defines the scaling targets the project should optimize for before
opening new broad experiment bursts.

## Gravity target

The retained unitary core should produce a dimensionless response law that does
not collapse into a sign-threshold as graph size grows.

Desired properties:

- Keep the corrected `1/L^p` propagator, Born safety, interference, and `k=0 -> 0`.
- Measure a response that depends in a controlled way on:
  - impact parameter
  - source mass / persistent support size
  - graph scale or layer depth
- Avoid a regime where the observable only says:
  - `toward mass`
  - `away from mass`

Current best candidate reduced variable:

- `k * ΣΔS_local`

Current best bounded benchmark observable:

- packet-local near-mass action `Q`

What counts as success:

- The response law stays meaningfully graded as graph size grows.
- The same reduced variable remains predictive across at least one minimal
  family with a single scaling parameter varied at a time.
- The asymptotic story is not just “many paths average everything to a plateau”
  unless that plateau is itself derived and controlled.

## Decoherence target

The non-unitary lane needs a scaling law in which detector-state mixedness does
not wash out as path multiplicity rises.

Desired properties:

- At fixed local environment density, detector-state mixedness should stay
  bounded away from `1` or strengthen with size.
- Decoherence should not disappear merely because many paths reuse the same
  environment labels.
- The target should survive on growing graphs, not only small tuned graphs.

Current anti-target:

- finite/discrete environment tags whose detector-conditioned purity rises back
  toward `1` as graph size grows

What counts as success:

- mixedness remains stable or deepens as path count grows
- the environment law scales with branch diversity, not with one global finite
  label budget

## Shared scaling discipline

For both gravity and decoherence:

- Hold all but one scaling variable fixed at a time.
- Prefer minimal graph families over the full random-DAG suite first.
- Treat reduced variables as first-class outputs, not just side diagnostics.
- Separate retained core laws from provisional closures.
