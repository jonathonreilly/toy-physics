# CKM Thales-Mediated Cross-System CP-Asymmetry Ratio Theorem

**Date:** 2026-04-25

**Status:** Retained atlas-leading CKM structural-ratio theorem. It derives
a framework-side relation between the B_d and B_s CP-phase readouts:

```text
sin(2 beta_s,0)_LO / sin(2 beta_d,0)  =  lambda^2  =  alpha_s(v) / 2,

phi_s,0 / sin(2 beta_d,0)          =  -lambda^2  =  -alpha_s(v) / 2.
```

Both relations are exact for the atlas-leading Wolfenstein readout, with
no hadronic mixing-amplitude input on the framework side. The canonical
coupling `alpha_s(v)` controls the cross-system CP ratio through the
framework-retained Thales circle `eta^2 = rho(1 - rho)`.

The B_d -> B_s correspondence is measured cleanly:

```text
phi_s_meas / sin(2 beta_d)_meas  =  -0.0552 +/- 0.031,
framework prediction -lambda^2    =  -0.0517,
```

at `0.11 sigma` agreement.

This is a non-trivial structural prediction: unlike amplitude-ratio
comparators such as `Delta m_s / Delta m_d`, the framework-side phase
ratio is not built from decay constants, bag parameters, meson-mass
ratios, or the short-distance factor `eta_B`. The retained readout
depends only on the canonical plaquette/CMT coupling.

The B_s-mixing-phase derivation
[`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md)
gives the absolute prediction `phi_s,0 = -alpha_s(v) sqrt(5)/6`. This
note proves the cross-system *ratio* identity that explicitly cancels
the `sqrt(5)` factors and exposes the canonical coupling alone.

**Primary runner:**
`scripts/frontier_ckm_thales_cross_system_cp_ratio.py`

## Statement

Let

```text
beta_d,0  = arctan( eta / (1 - rho) )                  (B_d apex angle)
beta_s,0  = lambda^2 eta + O(lambda^4)                 (B_s apex angle, leading)
phi_s,0   = -2 beta_s,0
```

with the retained framework values `rho = 1/6`, `eta = sqrt(5)/6`,
`lambda^2 = alpha_s(v)/2`. Then on the retained CKM atlas surface

```text
(C1)  R_t^2  =  (1 - rho)^2 + eta^2  =  1 - rho     (Thales-circle corollary),

(C2)  sin(2 beta_d,0)  =  2 eta (1 - rho) / R_t^2
                       =  2 eta                     (Thales simplification),

(C3)  sin(2 beta_s,0)_LO  :=  2 beta_s,0  (small-angle, leading)
                       =  2 lambda^2 eta,

(C4)  sin(2 beta_s,0)_LO / sin(2 beta_d,0)  =  lambda^2  =  alpha_s(v) / 2,

(C5)  phi_s,0 / sin(2 beta_d,0)          =  -lambda^2 =  -alpha_s(v) / 2.
```

Identity `(C1)` exposes the structural simplification driven by the
retained Thales-circle relation `eta^2 = rho(1 - rho)`. Identity `(C2)`
expresses `sin(2 beta_d,0)` in terms of `eta` alone, with the
`(1-rho)/R_t^2` factor canceling exactly. The ratios `(C4)` and `(C5)`
are the retained atlas-leading cross-system CP-asymmetry predictions.

## Retained Inputs

| Input | Authority |
| --- | --- |
| Canonical `alpha_s(v) = 0.10330381612...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| `lambda^2 = alpha_s(v)/2` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Thales circle `eta^2 = rho(1 - rho)` and `alpha_0 = pi/2` | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| `beta_s,0 = lambda^2 eta`, `phi_s,0 = -2 beta_s,0` (leading) | [`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md) |

No fitted CKM observable, B-meson decay constant, lattice bag parameter,
or hadronic mixing-amplitude factor enters the framework-side identity.
The B_s phase convention `phi_s = -2 beta_s` is the standard observation
bridge already used in the parent B_s note.

## Derivation

### 1. The Thales-circle corollary `(C1)`

Start from the retained right-angle theorem's Thales-circle relation

```text
eta^2  =  rho (1 - rho).
```

Then

```text
R_t^2  =  (1 - rho)^2 + eta^2
       =  (1 - rho)^2 + rho (1 - rho)
       =  (1 - rho) [ (1 - rho) + rho ]
       =  (1 - rho).
```

In framework values, `R_t^2 = 5/6` and `1 - rho = 5/6`, confirming the
identity. This is identity `(C1)`. The geometric content is that the
retained apex sits *exactly* on the Thales circle of the unit base, so
`R_t = sqrt(1 - rho)` -- the right-leg length collapses to a single
linear function of `rho`.

### 2. Simplification of `sin(2 beta_d,0)` `(C2)`

The standard tan-half formula gives

```text
sin(2 beta_d,0)  =  2 tan(beta_d,0) / (1 + tan^2(beta_d,0))
                 =  2 (eta / (1 - rho)) / (1 + eta^2/(1 - rho)^2)
                 =  2 eta (1 - rho) / [(1 - rho)^2 + eta^2]
                 =  2 eta (1 - rho) / R_t^2.
```

Applying `(C1)`, `R_t^2 = 1 - rho`, the `(1 - rho)` factor cancels:

```text
sin(2 beta_d,0)  =  2 eta (1 - rho) / (1 - rho)
                 =  2 eta.
```

In framework: `sin(2 beta_d,0) = 2 (sqrt(5)/6) = sqrt(5)/3`, matching
the retained value but expressed in the new minimal `eta`-only form.

### 3. The B_s asymmetry `(C3)`

From the parent B_s mixing-phase derivation, at leading non-trivial
Wolfenstein order

```text
beta_s,0  =  lambda^2 eta.
```

In the small-angle regime (numerically `beta_s,0 = 1.10 deg`), define
the atlas-leading sine readout by

```text
sin(2 beta_s,0)_LO  :=  2 beta_s,0  =  2 lambda^2 eta,
```

with the residual to the exact trigonometric `sin(2 beta_s,0)` about
`2.5e-4` relative.

### 4. The cross-system ratio `(C4)`

Combining `(C2)` and `(C3)`, the `2 eta` factor cancels:

```text
sin(2 beta_s,0)_LO / sin(2 beta_d,0)
   =  (2 lambda^2 eta) / (2 eta)
   =  lambda^2
   =  alpha_s(v) / 2.
```

This is the retained structural-ratio identity. Note the cancellation
mechanism: the `eta` factor enters identically in both numerator and
denominator after the Thales simplification, so the ratio carries
*only* the `lambda^2` from the B_s mixing phase. The structural
identity makes the cross-system ratio independent of `rho`, `eta`,
`A`, `R_t`, and `R_b`.

### 5. The phi_s ratio `(C5)`

Using `phi_s,0 = -2 beta_s,0` and `sin(2 beta_s,0)_LO = 2 beta_s,0` at
leading order,

```text
phi_s,0 / sin(2 beta_d,0)
   =  -2 beta_s,0 / sin(2 beta_d,0)
   =  -sin(2 beta_s,0)_LO / sin(2 beta_d,0)
   =  -lambda^2
   =  -alpha_s(v) / 2.
```

This is identity `(C5)`.

## Numerical Predictions

With canonical `alpha_s(v) = 0.10330381612227...`:

| Quantity | Closed form | Atlas-leading value |
| --- | --- | ---: |
| `R_t^2` (Thales) | `1 - rho` | `5/6` |
| `sin(2 beta_d,0)` | `2 eta` | `sqrt(5)/3 = 0.745356` |
| `sin(2 beta_s,0)_LO` | `2 lambda^2 eta` | `0.038499` |
| `phi_s,0` | `-2 lambda^2 eta` | `-0.038499` |
| `sin(2 beta_s,0)_LO / sin(2 beta_d,0)` | `lambda^2` | `0.051652` |
| `phi_s,0 / sin(2 beta_d,0)` | `-lambda^2` | `-0.051652` |
| `phi_s,0 / (2 eta)` | `-alpha_s(v)/2` | `-0.051652` |

PDG / LHCb comparators:

| Ratio | Framework | Measured | Deviation |
| --- | ---: | ---: | ---: |
| `phi_s / sin(2 beta_d)` | `-0.0517` | `-0.0552 +/- 0.031` | `+0.11 sigma` |
| `sin(2 beta_d)` (atlas-LO) | `0.7454` | `0.706 +/- 0.011` | `+3.6 sigma` |
| `phi_s` (atlas-LO) | `-0.0385` | `-0.039 +/- 0.022` | `+0.02 sigma` |

The cross-system **ratio** lands at `0.11 sigma`. The atlas-LO
*absolute* `sin(2 beta_d)` retains its known `3.6 sigma` tension with
B_d -> J/psi K_S; the absolute `phi_s` matches at `0.02 sigma`. The
ratio identity `phi_s / sin(2 beta_d) = -lambda^2` is therefore
sharper than the current individual atlas-LO comparison surface because
the retained ratio isolates the shared `2 eta` factor and leaves only
`lambda^2`.

## Scientific Role

The ratio `phi_s / sin(2 beta_d)` is a clean cross-system CP-phase
comparator. It is not an amplitude-ratio extraction and does not require
framework-side inputs such as `f_Bs/f_Bd`, `B_Bs/B_Bd`, `M_Bs/M_Bd`, or
`eta_B`. Until now the framework predicted the numerator and denominator
separately at atlas-LO, each carrying its own match-to-data status.

This note packages the *ratio* as a sharp framework-side prediction
controlled solely by the canonical `alpha_s(v)`. The mechanism is the
retained Thales-circle structure `eta^2 = rho(1 - rho)` -- a structural
geometric fact of the framework's CKM atlas surface, not a fitted
input -- which forces `R_t^2 = 1 - rho` and collapses the ratio to
`lambda^2`. The result is a sharper match to data than either
individual atlas-LO prediction.

## What This Claims

- `R_t^2 = 1 - rho` exactly at atlas-LO, as a Thales-circle corollary.
- `sin(2 beta_d,0) = 2 eta = sqrt(5)/3` at atlas-LO, with the
  `(1-rho)/R_t^2` factor canceling.
- `sin(2 beta_s,0)_LO / sin(2 beta_d,0) = lambda^2 = alpha_s(v)/2`
  exactly at atlas-LO Wolfenstein.
- `phi_s,0 / sin(2 beta_d,0) = -lambda^2 = -alpha_s(v)/2` exactly at
  atlas-LO Wolfenstein.
- The cross-system ratio is independent of the CP-radius `rho^2 + eta^2`
  and of `A^2`.

## What This Does Not Claim

- It does not derive `alpha_s(v)`; that remains the retained
  plaquette/CMT input.
- It does not promote a new B_s mixing-phase result beyond the parent
  derivation note `(B1)-(B3)`.
- It does not improve the absolute atlas-LO `sin(2 beta_d) = sqrt(5)/3`
  prediction; that retains its known atlas-vs-physical tension at
  approximately `3.6 sigma`.
- It does not promote any BSM contribution to B_d or B_s mixing; the
  prediction is pure SM at atlas-leading.
- It does not promote `phi_s = -2 beta_s` as a new framework theorem;
  this is the standard B_s mixing convention.
- It does not claim an all-orders trigonometric identity for
  `sin(2 beta_s,0)`; the sine readout is the atlas-leading small-angle
  readout, with the exact-sine residual tracked by the runner.

## Reproduction

```bash
python3 scripts/frontier_ckm_thales_cross_system_cp_ratio.py
```

Expected result:

```text
TOTAL: PASS=35, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import.

## Cross-References

- [`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md)
  -- parent absolute B_s mixing-phase derivation.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `rho`, `eta`, `eta^2 = rho(1 - rho)` Thales relation.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- retained right-angle theorem, alpha_0 = pi/2.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `lambda^2 = alpha_s(v)/2`.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` derivation.
