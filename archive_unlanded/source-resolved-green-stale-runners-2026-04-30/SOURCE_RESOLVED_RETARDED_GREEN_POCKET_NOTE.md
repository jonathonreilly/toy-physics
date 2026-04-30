# Source-Resolved Retarded Green Pocket

**Date:** 2026-04-05  
**Status:** exact-lattice finite-lag pocket, frozen on the proposed_retained compact family

## Artifact chain

- [`scripts/source_resolved_retarded_green_pocket.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_retarded_green_pocket.py)
- [`logs/2026-04-05-source-resolved-retarded-green-pocket.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-retarded-green-pocket.txt)

## Question

Does a minimal finite-lag update on the exact-lattice Green pocket do anything
qualitatively beyond the same-site-memory control?

This probe stays narrow:

- one compact exact lattice family at `h = 0.25`
- one source-resolved Green control
- one same-site-memory baseline
- one finite-lag retarded-like candidate
- one reduction check: zero source must recover free propagation exactly
- one observable: detector spread/support relative to the same-site control

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- interior source placement `source_z = 2.0`
- fixed cross5 source cluster with `5` in-bounds nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- same-site memory `mix = 0.9`
- retarded-like finite lag `lag = 2`, `mix = 0.7`

Reduction check:

- zero-source same-site shift: `+0.000000e+00`
- zero-source retarded shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | same-site deflection | retarded deflection | ret/same | ret - same |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.0010` | `+2.050891e-03` | `+2.412419e-03` | `+2.475657e-03` | `1.207` | `+6.32e-05` |
| `0.0020` | `+4.105409e-03` | `+4.824993e-03` | `+4.951595e-03` | `1.206` | `+1.27e-04` |
| `0.0040` | `+8.225500e-03` | `+9.650581e-03` | `+9.904265e-03` | `1.204` | `+2.54e-04` |
| `0.0080` | `+1.651142e-02` | `+1.930336e-02` | `+1.981254e-02` | `1.200` | `+5.09e-04` |

Support / spread comparison:

- mean `(ret support - same support) = 0.000e+00`
- mean `(ret N_eff - same N_eff) = +4.493e-02`

Fitted exponents:

- instantaneous `F~M`: `1.00`
- same-site memory `F~M`: `1.00`
- retarded-like `F~M`: `1.00`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the retarded-like update keeps the weak-field `TOWARD` sign on the compact
  exact lattice
- the mass-scaling class stays essentially linear
- the retarded-like update broadens detector support only slightly relative to
  the same-site baseline

## Honest limitation

This is still a minimal pocket, not a full retarded field equation.

- the update is a finite-lag memory rule, not a dynamical wave equation
- the support change is detectable but small
- the result is therefore best read as a controlled perturbation on top of the
  same-site-memory control, not a qualitative architectural jump

## Branch verdict

Treat this as a real bounded positive:

- exact zero-source reduction survives
- weak-field sign survives
- `F~M` stays at `1.00`
- the finite-lag update is real, but only a small correction relative to the
  same-site-memory pocket
- the generated-family bottleneck is therefore not fixed by this minimal step
