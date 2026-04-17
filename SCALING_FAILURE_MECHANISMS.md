# Scaling Failure Mechanisms

This file records the current best reduced explanation of the two main scaling
failures. They should be treated as separate architectural problems.

## Gravity scaling failure

Current read:

- local field/action asymmetry is real
- packet-local near-mass action observables improve the bounded law
- but the large-scale response still tends toward a plateau-like kick instead of
  a clean impact-parameter law

Reduced mechanism:

- many near-equivalent routes through the same local phase valley contribute
  coherently
- the path sum averages microscopic action contrast into a coarser packet-level
  bias
- as path multiplicity grows, added micro-routes do not keep changing the
  signed response proportionally

Current reduced variable:

- `k * ΣΔS_local`

Current best bounded refinement:

- packet-local near-mass action spread in the denominator

Working toy law:

- `Δk_y ≈ Δk_sat * tanh(C * Q_local)`

where:

- `Q_local = local_action_gap / local_action_spread`

Main gap:

- we do not yet have a derived asymptotic law showing when microscopic path
  multiplicity should renormalize the response into a plateau and when it
  should preserve graded scaling

## Decoherence scaling failure

Current read:

- small finite-environment mechanisms can yield some detector-side decoherence
- but tested finite/discrete environment architectures wrong-scale on growing
  DAGs

Reduced mechanism:

- path diversity grows with graph size
- both slit branches increasingly overlap the same environment labels
- the environment no longer separates branch histories well enough to maintain
  detector mixedness

Likely reduced competition:

- path diversity helps interference / gravity survive
- path overlap through the same env labels kills slit selectivity
- finite label budgets saturate before branch diversity does

Main gap:

- no retained law yet for how:
  - path count growth
  - path overlap growth
  - env-label diversity growth
  scale against one another

## Stop-rule implications

Bad next move for gravity:

- more raw `k` sweeps without a reduced asymptotic variable

Bad next move for decoherence:

- another clever small finite register

Good next move:

- derive the reduced competition first
- then test one architecture-level change that directly targets the reduced
  failure mechanism
