# Convention C-iso Temporal-Step Boundary

**Date:** 2026-05-07
**Claim type:** open_gate
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Primary runner:** [`scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py`](../scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py)

## Claim

The current `Cl(3)` / `Z^3` framework does not derive the isotropic
time-step convention

```text
a_tau = a_s.
```

The runner checks the two local routes that would make this convention
structural:

1. A Lieb-Robinson velocity route would need a canonical dimensionless
   `v_LR = 1`. The runner computes the standard bound proxy
   `v_LR = 2 e r J` and shows that it depends on `g^2`; at the canonical
   `g^2 = 1` point it gives `v_LR ~= 5.44`, hence
   `a_tau,LR ~= 0.18 a_s`, not `a_s`.
2. The single-clock route fixes the form of one-parameter evolution, not
   the lattice step. For any `a_tau > 0`, the transfer step can be written
   as `T(a_tau) = exp(-a_tau H)`.

This note therefore keeps C-iso as an admitted discretization convention:
standard isotropic Wilson at `beta = 6` is available only after admitting
`a_tau = a_s` and the usual finite-lattice representative choice. The note
does not claim that the Wilson or heat-kernel temporal form is uniquely
selected by the framework primitives.

## Dependencies

- `MINIMAL_AXIOMS_2026-05-03.md` for the
  `Cl(3)` / `Z^3` primitive surface.
- [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
  for the Lieb-Robinson velocity form.
- [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
  for the single-clock transfer-matrix surface.

These dependencies are allowed imports for an `open_gate` boundary. They are
not used here to lift C-iso to a retained or bounded closure.

## Boundaries

This note does not claim:

- that `a_tau = a_s` is uniquely forced by `Cl(3)` and `Z^3`;
- that standard isotropic Wilson at `beta = 6` is a zero-input derivation;
- that a future categorical or renormalization condition cannot select a
  preferred time step.

It only records that the two checked framework-local routes do not close the
time-step convention.

## Verification

Run:

```bash
python3 scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py
```

Expected:

```text
PASS=4 FAIL=0
```
