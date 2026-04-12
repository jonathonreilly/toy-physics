# EM + Gravity Coexistence Control Note

**Date:** 2026-04-12  
**Status:** blocker control design, not a retained positive

## Baseline

The overnight electromagnetism audit does **not** support the stronger claim
that gravity and electromagnetism already coexist in one Hamiltonian on the
same packet experiment. What is supported so far is narrower:

- a scalar gravity-like weak-field lane
- a scalar electrostatics-like sign-law lane
- a common propagator skeleton across those scalar couplings

## Minimal Clean Control

Use one fixed family, one packet, one detector, and one time schedule. Run a
2x2 factorial:

1. `H0`: free propagation
2. `Hg`: gravity-only sector on
3. `Hem`: EM-only sector on
4. `Hg + Hem`: both sectors on together

Measure both sector-specific readouts on the same evolved packet:

- gravity channel: the strongest retained gravity readout on that family
- EM channel: the strongest retained electrostatics or magnetic readout on
  that family

Compute the mixed residual:

```text
R_GE = Δ(Hg + Hem) - Δ(Hg) - Δ(Hem) + Δ(H0)
```

## Promotion Rule

Do **not** promote any current bounded claim to “gravity and EM coexist in one
Hamiltonian” without this control.

The strongest supportable claim today is narrower:

- the same propagator family supports separate scalar gravity-like and
  electrostatics-like couplings
- the joint-Hamiltonian coexistence claim remains blocked until the factorial
  residual is measured on the same packet experiment
