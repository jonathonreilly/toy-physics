# Assumptions And Imports

## Frozen Inputs

- Compact exact lattice family: `h=0.25`, `W=3`, `L=6`.
- Boundary-clipped source cluster: four in-bounds nodes.
- Source strengths: `0.001`, `0.002`, `0.004`, `0.008`.
- Green kernel: `exp(-mu r)/(r+eps)` with `mu=0.08`, `eps=0.5`.
- Calibrated gain input: `1.7578903308081324`.
- One self-consistency update from propagated source-cluster amplitudes.

## New Assumptions

None.  The block makes the existing frozen setup machine-checkable.

## Boundary

The calibrated gain is admitted as a setup input.  The block does not derive
an uncalibrated amplitude, a converged field equation, or a general
self-consistent field theory.
