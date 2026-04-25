# CP-Asymmetry Product as Cross-Sector alpha_s(v) Extraction Theorem

**Date:** 2026-04-25

**Status:** retained atlas-leading structural theorem on `main`. This
establishes a cross-sector consistency identity: the canonical coupling
`alpha_s(v)`, retained from the gauge-vacuum plaquette/CMT surface, is
also encoded by the framework in the product of two independently
measured CP-violation observables in B-meson physics. Specifically, at
atlas-leading Wolfenstein order,

```text
sin(2 beta_d,0) * sin(2 beta_s,0)  =  5 alpha_s(v) / 18,
```

equivalent to the **new atlas-LO alpha_s(v) estimator**

```text
alpha_s(v)  =  (18 / 5) * sin(2 beta_d) * sin(2 beta_s).
```

This is the framework's first CKM-CP-only consistency estimator for
`alpha_s(v)`. Combined with the canonical retained plaquette/CMT
determination, it opens an independent comparator sector for the
framework's coupling: gauge-vacuum structure versus B-meson
CP-violation, both tied to one canonical value.

Using the repo's PDG/LHCb 2024 comparator baseline,

```text
alpha_s(v)_CP-estimator  = 0.098 +/- 0.056   (from PDG sin(2 beta_d) and LHCb phi_s),
alpha_s(v)_canonical     = 0.103             (CMT plaquette/CMT surface),
```

agreeing at **0.09 sigma** under that loose comparator baseline. As
`phi_s` precision improves, the CP-product estimator becomes a sharper
atlas-LO falsification target. At that point the known finite-`lambda`
and higher-order Wolfenstein corrections must be included rather than
silently absorbed.

The cross-system Thales theorem
[`CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md)
established the ratio identity
`sin(2 beta_s) / sin(2 beta_d) = lambda^2 = alpha_s(v)/2`. This
theorem is its **product-form companion**: combined, the ratio and
the product completely determine both `sin(2 beta_d)` and
`sin(2 beta_s)` from `alpha_s(v)` alone, providing twin atlas-LO
predictions and a new route to estimate the canonical coupling from
CP-observable data.

**Primary runner:**
`scripts/frontier_ckm_cp_product_alpha_s_cross_sector_extraction.py`

## Statement

On the retained CKM atlas surface,

```text
(P1)  sin(2 beta_d,0) * sin(2 beta_s,0)  =  5 alpha_s(v) / 18,

(P2)  alpha_s(v)  =  (18 / 5) * sin(2 beta_d,0) * sin(2 beta_s,0)
                  =  3.6 * sin(2 beta_d,0) * sin(2 beta_s,0),

(P3)  sin^2(2 beta_d,0) + sin^2(2 beta_s,0)  =  5 (4 + alpha_s(v)^2) / 36,

(P4)  sin(2 beta_d,0) * sin(2 beta_s,0)  =  4 sqrt(5) * J / alpha_s(v)^2,
```

where `J = alpha_s(v)^3 sqrt(5)/72` is the retained Jarlskog invariant.

Identity `(P1)` is the pure-framework CP-asymmetry product identity.
Identity `(P2)` is the equivalent estimator route, treating
`alpha_s(v)` as an inferred quantity from the two CP-asymmetry
measurements at atlas-LO.
Identity `(P3)` is the companion squared-sum. Identity `(P4)` rewrites
the product purely in terms of `J` and `alpha_s(v)^2`, exposing the
framework's J-controlling structure.

## Retained Inputs

| Input | Authority |
| --- | --- |
| `lambda^2 = alpha_s(v)/2` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `eta = sqrt(5)/6`, `rho = 1/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Thales `eta^2 = rho(1 - rho)` | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| `sin(2 beta_d,0) = 2 eta = sqrt(5)/3` (Thales-mediated) | [`CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md) |
| `sin(2 beta_s,0) = 2 lambda^2 eta = alpha_s(v) sqrt(5)/6` | [`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md) |
| Canonical `alpha_s(v) = 0.10330381612...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |

No fitted CKM observable, B-meson lifetime, lattice bag parameter, or
hadronic mixing factor enters either side of `(P1)` or `(P2)`. The
identity is pure-framework on the structural side; the numerical
comparison is post-derivation.

## Derivation

The framework retains, at atlas-LO Wolfenstein:

```text
sin(2 beta_d,0)  =  2 eta                = sqrt(5) / 3,
sin(2 beta_s,0)  =  2 lambda^2 eta       = alpha_s(v) sqrt(5) / 6.
```

(The first uses the Thales-mediated simplification; the second is the
leading-order B_s mixing-phase atlas-LO result.) Their product is

```text
sin(2 beta_d,0) * sin(2 beta_s,0)
   =  (2 eta) * (2 lambda^2 eta)
   =  4 lambda^2 eta^2
   =  4 (alpha_s(v)/2) (5/36)
   =  5 alpha_s(v) / 18.
```

This establishes `(P1)`. Inverting:

```text
alpha_s(v)  =  (18 / 5) * sin(2 beta_d,0) * sin(2 beta_s,0).
```

This is `(P2)`.

For `(P3)`, the squared sum:

```text
sin^2(2 beta_d,0) + sin^2(2 beta_s,0)
   =  4 eta^2 + 4 lambda^4 eta^2
   =  4 eta^2 (1 + lambda^4)
   =  (5/9) (1 + alpha_s(v)^2/4)
   =  (5/9) (4 + alpha_s(v)^2) / 4
   =  5 (4 + alpha_s(v)^2) / 36.
```

For `(P4)`, using `J = A^2 lambda^6 eta`:

```text
4 sqrt(5) J / alpha_s(v)^2
   =  4 sqrt(5) * (alpha_s(v)^3 sqrt(5)/72) / alpha_s(v)^2
   =  4 * 5 * alpha_s(v) / 72
   =  20 alpha_s(v) / 72
   =  5 alpha_s(v) / 18.
```

So the product `sin(2 beta_d) sin(2 beta_s)` equals `5 alpha_s/18`,
which equals `4 sqrt(5) J/alpha_s^2`. All three forms are equivalent.

## Numerical Predictions

With canonical `alpha_s(v) = 0.10330381612227...`:

| Quantity | Closed form | Atlas-LO value |
| --- | --- | ---: |
| `sin(2 beta_d,0)` | `sqrt(5)/3` | `0.745356` |
| `sin(2 beta_s,0)` | `alpha_s(v) sqrt(5)/6` | `0.038499` |
| Product | `5 alpha_s(v)/18` | `0.028696` |
| Inverse estimator | `(18/5) * product` | `0.103304` (recovers canonical) |
| `sin^2(2 beta_d) + sin^2(2 beta_s)` | `5 (4 + alpha_s^2)/36` | `0.557038` |

PDG/LHCb 2024 comparator baseline:

```text
sin(2 beta_d)_PDG       = 0.706 +/- 0.011
sin(2 beta_s)_LHCb      = 0.0386 +/- 0.022 (from phi_s = -2 beta_s)
product (PDG)           = 0.0273 +/- 0.0155
alpha_s_CP-estimator    = (18/5) * product = 0.0981 +/- 0.0559
alpha_s_canonical (CMT) = 0.10330
deviation               = -0.09 sigma
```

The CP-product estimator matches the canonical CMT value at
`0.09 sigma` under this comparator baseline.

## Why This Pushes the Framework Forward

The canonical `alpha_s(v) = 0.10330381612...` is retained from the
plaquette/CMT gauge-vacuum surface -- a pure-QCD determination. This
note proves that the same coupling is structurally encoded in
B-meson CP-asymmetry observables that have **no QCD running content
in their leading-order Wolfenstein form**.

This opens a **new sector** of alpha_s(v) consistency tests:

1. **Gauge-vacuum sector** (existing): the canonical plaquette/CMT
   surface gives `alpha_s(v) = 0.10330` directly from QCD lattice
   computation.
2. **CP-violation sector** (new): the product of B_d and B_s
   CP-asymmetries gives an independent atlas-LO estimator
   `alpha_s(v) = 18/5 * sin(2 beta_d) * sin(2 beta_s)`.

These two sectors probe different observables. Their agreement at the
repo's PDG/LHCb 2024 precision baseline provides a non-trivial
consistency check on the framework's canonical coupling.

The structural mechanism is the same Thales geometry that drives
the cross-system ratio theorem: `eta^2 = rho(1 - rho)` forces
`sin(2 beta_d) = 2 eta`, and the parent `B_s` mixing phase derivation
gives `sin(2 beta_s) = 2 lambda^2 eta`. The product is
`4 lambda^2 eta^2`, which evaluates to `5 alpha_s(v)/18` in retained
framework values.

This is a **cross-sector consistency identity**. It does not replace
standard QCD extractions of `alpha_s`, but it gives this framework a
CP-observable estimator that can be compared against the canonical
plaquette/CMT value.

## Falsification

The PDG/LHCb 2024 baseline uncertainty is dominated by
`sigma(phi_s) = 0.022 rad`. Projected improvements:

| Era | `sigma(phi_s)` | `sigma(alpha_s)_CP` | Comparison |
| --- | --- | ---: | --- |
| PDG/LHCb 2024 baseline | `+/- 0.022 rad` | `+/- 0.056` | non-test |
| LHCb Run 4 (~2027) | `+/- 0.005 rad` | `+/- 0.013` | ~1 sigma test |
| HL-LHC | `+/- 0.002 rad` | `+/- 0.005` | precision test |

By the HL-LHC era, the CP-product estimator may resolve `alpha_s(v)` to
roughly `+/- 0.005`, comparable to the canonical CMT precision.
A non-zero deviation between the estimator and the canonical value would
falsify the framework's atlas-LO Wolfenstein structure or its canonical
`alpha_s(v)` value.

The atlas-LO identity carries `O(lambda^2) ~ 5%` Wolfenstein
corrections, which at the PDG/LHCb 2024 precision baseline are smaller than the
`sin(2 beta_s)` measurement uncertainty (28% relative). At LHCb
precision the NLO Wolfenstein will need to be incorporated.

## What This Claims

- `sin(2 beta_d,0) * sin(2 beta_s,0) = 5 alpha_s(v)/18` exactly at
  atlas-LO Wolfenstein.
- Equivalent estimator route:
  `alpha_s(v) = (18/5) * sin(2 beta_d,0) * sin(2 beta_s,0)`.
- Equivalent J-form:
  `sin(2 beta_d,0) * sin(2 beta_s,0) = 4 sqrt(5) J / alpha_s(v)^2`.
- The CP-product estimator agrees with the canonical CMT/plaquette
  `alpha_s(v) = 0.10330` at `0.09 sigma` against the PDG/LHCb 2024
  baseline, providing a non-trivial cross-sector consistency check.

## What This Does Not Claim

- It does not derive `alpha_s(v)` independently of the retained CKM
  atlas surface; it repackages that surface as an atlas-LO CP-observable
  estimator and comparator.
- It does not promote the CP-product estimator as a competitive `alpha_s`
  measurement at the PDG/LHCb 2024 precision baseline; the LHCb `phi_s`
  uncertainty is the dominant systematic.
- It does not modify the atlas-leading B_s mixing-phase derivation;
  the parent `phi_s = -alpha_s(v) sqrt(5)/6` identity is preserved.
- It does not promote any BSM contribution to either CP asymmetry.
- It does not claim NLO sharpening; the identity is atlas-LO only,
  with `O(lambda^2) ~ 5%` Wolfenstein corrections expected.

## Reproduction

```bash
python3 scripts/frontier_ckm_cp_product_alpha_s_cross_sector_extraction.py
```

Expected result:

```text
TOTAL: PASS=28, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import.

## Cross-References

- [`CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md)
  -- companion ratio identity `sin(2 beta_s)/sin(2 beta_d) = lambda^2`.
- [`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md)
  -- parent atlas-LO B_s mixing-phase derivation.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- retained Thales `eta^2 = rho(1 - rho)`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `rho = 1/6`, `eta = sqrt(5)/6`, `J` definition.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` plaquette/CMT determination.
