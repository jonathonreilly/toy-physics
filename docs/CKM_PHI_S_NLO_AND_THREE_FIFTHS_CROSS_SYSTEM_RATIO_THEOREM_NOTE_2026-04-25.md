# φ_s NLO Closed Form and the 3/5 Cross-System CP Ratio Theorem

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM
atlas/axiom + B_s mixing-phase surfaces. This note derives **two new
results** purely from retained inputs on `main`:

1. an NLO Wolfenstein closed form for the B_s mixing phase
   ```text
   phi_s  =  -alpha_s(v) sqrt(5)/6  -  alpha_s(v)^2 sqrt(5)/36  +  O(alpha_s^3),
          =  -(alpha_s(v) sqrt(5)/6)(1 + alpha_s(v)/6),
   ```
   filling the gap between the retained leading prediction
   `phi_s,0 = -alpha_s(v) sqrt(5)/6` and the parent note's numerical
   "finite-lambda guardrail" `-0.03922 rad`;

2. an α_s-INDEPENDENT cross-system CP-asymmetry ratio
   ```text
   sin(2 alpha_bar) / phi_s  =  3/5    [exactly, leading order],
   ```
   binding B_d and B_s CP-violation observables through a pure
   rational ratio that is **independent of the canonical coupling**.

The 3/5 ratio falls out as a clean integer ratio of the leading
coefficients: `sin(2 alpha_bar) ~ -(sqrt(5)/10) alpha_s` and
`phi_s ~ -(sqrt(5)/6) alpha_s` give `(1/10)/(1/6) = 6/10 = 3/5`.

Both results are derivable using **only retained inputs on `main`**:
the canonical `alpha_s(v)`, retained Wolfenstein, retained CP-phase,
retained right-angle theorem, retained NLO-protected-γ̄ theorem, and
the retained B_s mixing-phase derivation. No SUPPORT-tier or open
inputs (Koide, bare-coupling ratios, dimension-color identities) are
used.

**Primary runner:**
`scripts/frontier_ckm_phi_s_nlo_and_three_fifths_cross_system_ratio.py`

## Statement

```text
(R1)  phi_s(NLO)  =  -alpha_s(v) sqrt(5)/6  -  alpha_s(v)^2 sqrt(5)/36
                                                + O(alpha_s^3);

(R2)  Equivalent factored form:
      phi_s(NLO)  =  -(alpha_s(v) sqrt(5)/6) (1 + alpha_s(v)/6).

(R3)  sin(2 alpha_bar)  =  -(sqrt(5)/10) alpha_s(v)  +  O(alpha_s^2)
                          [pure NLO; sin(2 alpha_0) = 0 at atlas-LO].

(R4)  Cross-system identity (α_s-INDEPENDENT, leading order):
      sin(2 alpha_bar) / phi_s  =  3/5.

(R5)  Combined with retained Thales cross-system
      sin(2 beta_s) / sin(2 beta_d) = lambda^2 = alpha_s(v)/2:
      sin(2 alpha_bar) / sin(2 beta_d)  =  -3 alpha_s(v) / 10
                                          [leading order].
```

`(R1)` and `(R2)` are NEW NLO Wolfenstein closed-form expressions
for `phi_s`. `(R3)` is a re-derivation of the leading sin(2α̅)
coefficient (atlas-LO α_0 = π/2 makes it pure NLO) using only
retained inputs (atlas-LO + the retained NLO-protected-γ̄ theorem).
`(R4)` is the NEW α_s-independent cross-system ratio. `(R5)` is the
NEW joint cross-system identity combining all three retained
cross-system predictions.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| Canonical `alpha_s(v) = 0.103303816...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Atlas Thales, `alpha_0 = pi/2` | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| `alpha_bar - pi/2 = (sqrt(5)/20) alpha_s + O(alpha_s^2)` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md), N7 |
| Leading B_s mixing phase `phi_s,0 = -alpha_s sqrt(5)/6` | [`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md) |
| Cross-system Thales `sin(2 beta_s)/sin(2 beta_d) = lambda^2` | [`CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md) |
| Standard PDG-Wolfenstein expansion (textbook) | textbook CKM phenomenology |

No PDG observable enters as a derivation input. No SUPPORT-tier or
open inputs (Koide `Q_l`, bare-coupling ratios, dimension-color
quadratic) are used.

## Derivation

### `(R1), (R2)`: φ_s at NLO Wolfenstein

The PDG-Wolfenstein expansion of the relevant CKM elements to the
order needed for the imaginary parts:

```text
V_ts  =  -A lambda^2 + (A lambda^4/2)(1 - 2(rho + i eta))  +  O(lambda^6),
V_tb  =  1 - A^2 lambda^4/2  +  O(lambda^6),
V_cs  =  1 - lambda^2/2 - lambda^4(1+4 A^2)/8  +  O(lambda^6),
V_cb  =  A lambda^2  +  O(lambda^8).
```

Compute the ratio `-V_ts V_tb*/(V_cs V_cb*)` at NLO in lambda²:

```text
V_ts V_tb*  =  -A lambda^2 + (A lambda^4/2)(1 - 2 rho - 2 i eta)
               + O(lambda^6).

V_cs V_cb*  =  (1 - lambda^2/2)(A lambda^2)  +  O(lambda^6)
            =  A lambda^2 (1 - lambda^2/2)  +  O(lambda^6).

-V_ts V_tb* / (V_cs V_cb*)
   =  [1 - (lambda^2/2)(1 - 2 rho - 2 i eta)] / [1 - lambda^2/2]
   =  [1 - lambda^2/2 + lambda^2 rho + i lambda^2 eta] / [1 - lambda^2/2]
   =  1 + (lambda^2 rho + i lambda^2 eta) / (1 - lambda^2/2)
   =  1 + (lambda^2 rho + i lambda^2 eta)(1 + lambda^2/2 + ...)
   =  1 + lambda^2 (rho + i eta)(1 + lambda^2/2)  +  O(lambda^6).
```

The argument at NLO in `lambda²`:

```text
beta_s  =  arctan( lambda^2 eta (1 + lambda^2/2) /
                   (1 + lambda^2 rho (1 + lambda^2/2)) )
        ≈  lambda^2 eta (1 + lambda^2/2 - lambda^2 rho)  +  O(lambda^6)
        =  lambda^2 eta + lambda^4 eta (1/2 - rho)  +  O(lambda^6).
```

Substituting `lambda^2 = alpha_s(v)/2`, `eta = sqrt(5)/6`, `rho = 1/6`:

```text
beta_s(NLO)  =  (alpha_s/2)(sqrt(5)/6) + (alpha_s/2)^2 (sqrt(5)/6)(1/2 - 1/6)
            =  alpha_s sqrt(5)/12  +  (alpha_s^2/4)(sqrt(5)/6)(1/3)
            =  alpha_s sqrt(5)/12  +  alpha_s^2 sqrt(5)/72.
```

The B_s mixing CP-violating phase is

```text
phi_s(NLO)  =  -2 beta_s(NLO)
             =  -alpha_s sqrt(5)/6  -  alpha_s^2 sqrt(5)/36
             =  -(alpha_s sqrt(5)/6)(1 + alpha_s/6).
```

This is `(R1)` and its factored form `(R2)`.

**Numerical cross-check.** At canonical `alpha_s(v) = 0.10330381612...`:

```text
LO:           phi_s,0 = -alpha_s sqrt(5)/6        =  -0.038499
NLO correction:        -alpha_s^2 sqrt(5)/36       =  -0.000663
NLO total:             phi_s(NLO)                  =  -0.039162.
```

The parent retained note records the "finite-lambda standard-matrix
guardrail" as `-0.03922 rad`. The closed-form `(R1)` reproduces this
to within `6 x 10^-5` (the next O(α_s³) correction), confirming that
`(R1)` is the correct NLO closed-form expression behind the parent
note's numerical value.

### `(R3)`: sin(2α̅) leading order from retained inputs

From the retained NLO-protected-γ̄ theorem (N7),
`alpha_bar - pi/2 = (sqrt(5)/20) alpha_s(v) + O(alpha_s^2)`. Then

```text
2 alpha_bar - pi  =  (sqrt(5)/10) alpha_s(v)  +  O(alpha_s^2).
sin(2 alpha_bar)  =  sin(pi + (sqrt(5)/10) alpha_s)
                  =  -sin((sqrt(5)/10) alpha_s)
                  =  -(sqrt(5)/10) alpha_s(v)  +  O(alpha_s^2).
```

Since `sin(2 alpha_0) = sin(pi) = 0` exactly at atlas-LO, `sin(2 alpha_bar)`
is a **pure NLO observable**: any non-zero value is entirely an NLO
Wolfenstein effect, decoupled from atlas-LO uncertainties.

### `(R4)`: cross-system 3/5 ratio

Combining `(R1)` at leading order and `(R3)`:

```text
sin(2 alpha_bar) / phi_s
   =  [-(sqrt(5)/10) alpha_s + O(alpha_s^2)]
       / [-(sqrt(5)/6) alpha_s + O(alpha_s^2)]
   =  (1/10) / (1/6)  +  O(alpha_s)
   =  6/10  +  O(alpha_s)
   =  3/5  +  O(alpha_s).
```

The leading order ratio is the pure rational number `3/5 = 0.6`,
**independent of `alpha_s(v)`'s numerical value**. The factor of
`sqrt(5)` cancels exactly.

The next correction is at relative `O(alpha_s)`, dominated by the
NLO term in `phi_s` that we derived above. With α_s ≈ 0.103 at the
canonical value, this correction is about `+α_s/6 ≈ +1.7%` from
`phi_s`'s NLO term, plus separate NLO corrections to `sin(2 alpha_bar)`.

### `(R5)`: combined cross-system identity

Combining `(R4)` with the retained Thales cross-system identity
`sin(2 beta_s)/sin(2 beta_d) = lambda^2 = alpha_s(v)/2` and the
relation `phi_s = -2 beta_s ≈ -sin(2 beta_s)` for small β_s:

```text
sin(2 alpha_bar) / sin(2 beta_d)
   =  (sin(2 alpha_bar) / phi_s)  ×  (phi_s / sin(2 beta_s))
                                     ×  (sin(2 beta_s) / sin(2 beta_d))
   =  (3/5)  ×  (-1)                 ×  lambda^2
   =  -(3/5)(alpha_s/2)
   =  -3 alpha_s(v) / 10.
```

This is `(R5)`. At canonical α_s: `-3 × 0.10330/10 = -0.0310`. Direct
check: `sin(2 alpha_bar)/sin(2 beta_d) = -0.0231 / 0.7454 = -0.0310`. ✓

## Numerical Predictions

With canonical `alpha_s(v) = 0.10330381612227...`:

| Quantity | Closed form | Atlas-NLO value |
| --- | --- | ---: |
| `phi_s(LO)` (retained) | `-alpha_s sqrt(5)/6` | `-0.038499` |
| `phi_s` NLO correction | `-alpha_s^2 sqrt(5)/36` | `-0.000663` |
| `phi_s(NLO)` (NEW) | `-(alpha_s sqrt(5)/6)(1 + alpha_s/6)` | `-0.039162` |
| `phi_s(NLO)` direct full-Wolfenstein | -- | `-0.039169` |
| Closed-form residual | NLO (O(α_s³)) | `7 x 10^-6` |
| `sin(2 alpha_bar)` (LO) | `-(sqrt(5)/10) alpha_s` | `-0.023099` |
| `sin(2 alpha_bar) / phi_s` | `3/5` (pure rational) | `0.600000` (exact) |
| `sin(2 alpha_bar) / sin(2 beta_d)` | `-3 alpha_s/10` | `-0.030991` |

PDG/LHCb comparators:

```text
phi_s_LHCb (PDG 2024)        =  -0.039 +/- 0.022 rad

framework phi_s(LO)          =  -0.0385       (0.02 sigma agreement)
framework phi_s(NLO)         =  -0.0392       (0.01 sigma agreement)

sin(2 alpha) (PDG isospin)   =  +0.18 +/- 0.10  (penguin-polluted; not pure-tree)
framework sin(2 alpha_bar)   =  -0.0231        (pure-tree, as predicted)
```

The framework's NLO `phi_s` lands inside the LHCb 1-sigma band at
`0.01 sigma` — slightly tighter than the LO at `0.02 sigma`, as
expected for a higher-order correction. Both `phi_s` predictions
match observation. The `sin(2 alpha)` PDG comparator is dominated by
B → π+π- penguin pollution, which the framework's pure-tree
prediction is not designed to match directly.

## Science Value

### What this lets the framework predict that it could not before

The retained B_s mixing-phase note carries the leading prediction
`phi_s,0 = -alpha_s sqrt(5)/6` and a numerical "finite-lambda
standard-matrix guardrail" of `-0.03922 rad`. The closed-form
expression behind that guardrail is **derived here for the first
time**:

```text
phi_s(NLO)  =  -(alpha_s(v) sqrt(5)/6)(1 + alpha_s(v)/6).
```

This converts a previously-numerical observation into an explicit
algebraic identity. Future precision on `phi_s` (LHCb upgrade,
HL-LHC) will probe the framework at the `O(alpha_s^2 sqrt(5)/36) ~
7 x 10^-4 rad` level — well within projected experimental reach.

### A pure rational, alpha_s-INDEPENDENT cross-system identity

The 3/5 cross-system ratio `(R4)` is a **new dimensionless,
alpha_s-independent identity** the framework derives that simultaneously
binds:

- a B_d CP observable at NLO Wolfenstein (`sin(2 alpha_bar)`),
- a B_s CP observable at LO Wolfenstein (`phi_s`).

Standard SM phenomenology has no a priori reason for this ratio to
be 3/5 — it emerges specifically from the framework's retained atlas
Thales geometry (which fixes `alpha_0 = pi/2`, hence the slope
`sqrt(5)/20` in the protected-γ̄ theorem) and the specific
`eta = sqrt(5)/6` of the framework's atlas surface.

**Why this matters for falsification.** The 3/5 ratio is independent
of `alpha_s(v)`'s numerical precision. Even if the canonical
coupling is later revised, the leading-order ratio between the two
CP observables stays pinned to 3/5 (so long as atlas Thales geometry
holds). Future experiments measuring `phi_s` and `sin(2 alpha)`
independently can test the framework without reference to the
canonical coupling -- a sharper falsification surface than alpha_s-dependent
predictions allow once the B_d alpha extraction is placed on the same
pure-tree / isospin-corrected surface.

### A complete leading-order cross-system catalog

Combining `(R4)` with the previously-retained Thales cross-system
identity `sin(2 beta_s)/sin(2 beta_d) = lambda^2`, the framework
now provides a complete leading-order catalog of cross-system CP
ratios across the three SM unitarity triangles:

| Ratio | Closed form | Status |
| --- | --- | --- |
| `sin(2 beta_s) / sin(2 beta_d)` | `lambda^2 = alpha_s(v)/2` | retained Thales cross-system |
| `sin(2 alpha_bar) / phi_s` | `3/5` | **NEW (R4) α_s-INDEPENDENT** |
| `sin(2 alpha_bar) / sin(2 beta_d)` | `-3 alpha_s(v)/10` | **NEW (R5) joint** |
| `phi_s / sin(2 beta_d)` | `-alpha_s(v)/2` | (derivable from above) |
| `\|V_cb\| = \|V_ts\|` (leading) | implicit at atlas-LO | retained third-row magnitudes |

This stratifies the cross-system tests into:
- **α_s-independent geometric tests** (3/5 cross-system, λ²/λ²-style
  ratios in CKM-magnitude land);
- **α_s-dependent dynamical tests** that pull the canonical
  coupling out of CP measurements.

Each ratio provides an independent falsification target sensitive to
different facets of the framework's structure.

### Connection to experiment

| Experimental measurement | Framework prediction |
| --- | --- |
| LHCb φ_s (B_s → J/ψ φ) | `phi_s = -(alpha_s sqrt(5)/6)(1 + alpha_s/6) = -0.0392` |
| LHCb / Belle II isospin α from B → ππ | `alpha_bar = 90.66°`, pure-tree `sin(2 alpha_bar) = -0.0231` |
| Joint LHCb φ_s + isospin α | `sin(2 alpha_bar)/phi_s = 3/5` (α_s-independent) |
| HL-LHC sub-percent precision on both | sub-σ test of 3/5 ratio (geometric) and α_s² term in φ_s |

The 3/5 ratio test is valuable because it is a ratio of independently
measured B_d and B_s CP observables, with no input from QCD coupling
determinations, lattice QCD, or hadronic form factors. The live experimental
qualification is the B_d side: the alpha-channel readout must be interpreted
on the same pure-tree / isospin-corrected surface, not as the raw
penguin-polluted asymmetry.

### What this rules out

If a future precision joint measurement of `phi_s` and pure-tree
`sin(2 alpha)`
gives a ratio significantly different from `3/5` (say, `0.6 ± 0.05`
becomes `0.5 ± 0.02`), the framework's atlas Thales geometry fails.
The 3/5 ratio is tied to `cos(2 alpha_0) = -1` (atlas right angle)
and `eta = sqrt(5)/6` (CP-phase coordinates) — both retained on
`main`. A non-3/5 ratio would falsify either:

- atlas-LO `alpha_0 = pi/2`, OR
- atlas CP-phase η = √5/6, OR
- the protected-γ̄ NLO theorem's slope coefficient.

Each of these is a load-bearing piece of the framework's CKM-CP
sector. So the 3/5 ratio is a sharp single-number test of the
framework's CP-violation foundation.

## What This Claims

- `(R1), (R2)`: explicit NLO closed form
  `phi_s = -(alpha_s(v) sqrt(5)/6)(1 + alpha_s(v)/6) + O(alpha_s^3)`
  filling the gap between the retained leading prediction and the
  parent's numerical guardrail.
- `(R3)`: `sin(2 alpha_bar) = -(sqrt(5)/10) alpha_s(v) + O(alpha_s^2)`
  derived from retained inputs (atlas-LO + protected-γ̄).
- `(R4)`: NEW α_s-INDEPENDENT cross-system ratio
  `sin(2 alpha_bar) / phi_s = 3/5` exactly at leading order.
- `(R5)`: NEW joint identity
  `sin(2 alpha_bar) / sin(2 beta_d) = -3 alpha_s(v)/10` at leading
  order, derived from `(R4)` plus retained Thales cross-system.

## What This Does NOT Claim

- It does not promote NLO Wolfenstein predictions beyond second-
  order in `lambda^2` (i.e., `O(alpha_s^2)`); the `(R1)` closed form
  is leading + first NLO term, with O(α_s³) corrections suppressed.
- It does not promote any direct PDG comparator for raw `S_(pi+ pi-)`
  because that observable carries large penguin pollution; the
  framework's `sin(2 alpha_bar)` is the **pure-tree** value, not
  the raw measured asymmetry.
- It does not modify any retained CKM atlas, Wolfenstein, CP-phase,
  right-angle, B_s mixing-phase, or Thales cross-system theorem.
- It does not use any SUPPORT-tier or open input (Koide `Q_l`,
  bare-coupling ratios, dimension-color quadratic).
- It does not promote the 3/5 ratio beyond leading order; the next
  correction is `O(alpha_s)` and combines NLO contributions from
  both numerator and denominator.

## Reproduction

```bash
python3 scripts/frontier_ckm_phi_s_nlo_and_three_fifths_cross_system_ratio.py
```

Expected result:

```text
TOTAL: PASS=28, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import. All upstream
authorities are retained on `main`.

## Cross-References

- [`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md)
  -- retained leading `phi_s,0 = -alpha_s sqrt(5)/6` and numerical
  finite-lambda guardrail this note's closed form reproduces.
- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  -- retained `alpha_bar - pi/2 = (sqrt(5)/20) alpha_s` (N7).
- [`CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md)
  -- retained `sin(2 beta_s)/sin(2 beta_d) = lambda^2`.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- retained `alpha_0 = pi/2`, atlas Thales geometry.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `rho = 1/6`, `eta^2 = 5/36`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` retained input.
