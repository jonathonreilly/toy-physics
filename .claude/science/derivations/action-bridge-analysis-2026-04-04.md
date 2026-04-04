# Analysis: Spent-delay vs Valley-linear Bridge

## Date
2026-04-04

## Target
Explain why spent-delay gives more TOWARD on random graphs while
valley-linear gives Newtonian scaling on regular lattices. Is this
a renormalization (same theory at different scales) or genuinely
different physics?

## Finding: Signal-to-noise, not renormalization

The bridge is a SIGNAL-TO-NOISE effect, not an action transformation.

At typical field f = s/r = 1.67e-5 (r=3, s=5e-5):
  Spent-delay |delta_S/L| = sqrt(2f) = 5.77e-3
  Valley-linear |delta_S/L| = f = 1.67e-5
  Ratio: spent-delay is 346x larger

On RANDOM graphs:
  Paths to the same detector node are incoherent (varied lengths).
  The gravity signal is the average of ~N_paths random contributions.
  Signal ~ perturbation_size × sqrt(N_paths) (random walk in phase).
  Spent-delay has 346x more perturbation → much stronger signal.

On REGULAR lattices:
  Paths to the same detector node are coherent (same topological route
  → same phase). The gravity signal is N_paths × perturbation (not sqrt).
  The perturbation size cancels in the centroid ratio.
  What matters: the f-dependence of delta_S.
  Linear f → deflection 1/b (Newtonian).
  sqrt(f) → deflection 1/sqrt(b) (non-Newtonian).

## Implication

The two actions are GENUINELY DIFFERENT, not the same theory at
different effective scales. The crossover in the regularity sweep
is a signal-to-noise transition, not a renormalization.

- Valley-linear is the correct action for Newtonian gravity (linear f)
- Spent-delay is a stronger probe for gravity detection on noisy graphs
  (larger perturbation → better signal-to-noise)
- On random graphs, the f-dependence doesn't matter because the path
  sum is too noisy to resolve it

## What this means for the model

The model has a CHOICE of action, not a derived one:
- If the goal is Newtonian gravity: use valley-linear S = L(1-f)
- If the goal is robust gravity detection: use spent-delay

The earlier "crossover" result was real but misinterpreted:
  - NOT: "spent-delay renormalizes to valley-linear"
  - YES: "spent-delay has more signal on noisy graphs"

## Testable prediction

If we increase the field strength by 346x (making valley-linear
perturbation the same size as spent-delay at standard strength),
the crossover should vanish: valley-linear should perform as well
as spent-delay on random graphs.

## Status
CONFIRMED (analytically) — the signal-to-noise explanation is
quantitative and matches the observed crossover.
