# CKM B_s Mixing Phase Derivation Theorem

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure prediction with a standard B_s-mixing
phase-convention bridge. This note derives a new leading CKM prediction by
combining three retained inputs --
`alpha_s(v)` (canonical plaquette/CMT surface),
`lambda^2 = alpha_s(v)/2` (Wolfenstein structural identity), and
`eta = sqrt(5)/6` (CP-phase structural identity) -- with the standard
Wolfenstein expansion of the CKM matrix to the leading non-trivial order in
`lambda`. The output is the atlas-leading B_s-meson mixing phase

```text
beta_s,0   = alpha_s(v) sqrt(5) / 12,
phi_s,0    = -2 beta_s,0 = -alpha_s(v) sqrt(5) / 6,
```

which has not previously been carried as a named retained framework
prediction. As a corollary the note also packages the trigonometric catalog
of doubled atlas-triangle angles `(sin/cos)(2 alpha_0, 2 beta_0, 2 gamma_0)`
and the missing right-leg side-length identity `R_t^2 = 5/6` Pythagorean
companion to the retained `R_b^2 = 1/6`.

The leading numerical prediction `phi_s,0 = -3.850e-2 rad = -2.206 deg` lies
inside the LHCb single-measurement 1-sigma band
`phi_s = -0.039 +/- 0.022(stat) +/- 0.006(syst) rad` at the `0.02 sigma`
level if the statistical uncertainty is used as the comparator. The exact
finite-`lambda` standard-matrix readout from the parent CKM atlas is
`phi_s = -3.922e-2 rad`; it is retained here as a guardrail, not as a
replacement for the compact leading identity.

**Primary runner:** `scripts/frontier_ckm_bs_mixing_phase_derivation.py`

## Statement

Combining the retained inputs

```text
alpha_s(v)        canonical [ALPHA_S_DERIVED_NOTE.md]
lambda^2 = alpha_s(v)/2     [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM]
A^2      = 2/3              [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM]
rho      = 1/6              [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM]
eta      = sqrt(5)/6        [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM]
alpha_0  = pi/2             [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM]
```

with the Wolfenstein expansion of the CKM matrix at order `lambda^2`,

```text
V_us  =  lambda + O(lambda^7),
V_cs  =  1 - lambda^2/2 + O(lambda^4),
V_cb  =  A lambda^2 + O(lambda^8),
V_ts  = -A lambda^2 [1 - lambda^2 (1/2 - rho - i eta)] + O(lambda^6),
V_tb  =  1 + O(lambda^4),
```

the B_s unitarity triangle phase

```text
beta_s = arg[ -V_ts V_tb^* / (V_cs V_cb^*) ]
```

evaluates at leading non-trivial order to

```text
(B1)  beta_s,0 = lambda^2 eta + O(lambda^4)
              = (alpha_s(v)/2)(sqrt(5)/6)
              = alpha_s(v) sqrt(5) / 12.

(B2)  phi_s,0  = -2 beta_s,0 = -alpha_s(v) sqrt(5) / 6.

(B3)  sin(2 beta_s,0) = 2 lambda^2 eta + O(lambda^4)
                      = alpha_s(v) sqrt(5) / 6.
```

In addition, the atlas-leading triangle trigonometric catalog evaluates to

```text
(T1)  sin(2 alpha_0) =  0,           cos(2 alpha_0) = -1,
(T2)  sin(2 beta_0)  =  sqrt(5)/3,   cos(2 beta_0)  =  2/3,
(T3)  sin(2 gamma_0) =  sqrt(5)/3,   cos(2 gamma_0) = -2/3,
(T4)  sin(2 beta_0)  =  sin(2 gamma_0)
                          (forced by alpha_0 = pi/2),
```

and the side-length catalog evaluates to

```text
(S1)  |R_b|^2 = rho^2 + eta^2     = 1/6,
(S2)  |R_t|^2 = (1-rho)^2 + eta^2 = 5/6,
(S3)  |R_b|^2 + |R_t|^2 = 1     (Pythagoras forced by alpha_0 = pi/2),
(S4)  |R_t| / |R_b| = sqrt(5).
```

Identity `(S2)` and the catalog `(T1)-(T3)` are new named structural rows; the
identities `(B1)-(B3)` are the new leading CKM-derived numerical prediction.

## Retained Inputs

| Input | Authority |
| --- | --- |
| Canonical `alpha_s(v) = 0.10330381612...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta = sqrt(5)/6`, `rho^2 + eta^2 = 1/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `alpha_0 = pi/2` (atlas-leading right angle) | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| Standard Wolfenstein expansion of the CKM matrix | textbook CKM phenomenology |
| Standard relation `phi_s = -2 beta_s` for the SM B_s mixing phase | textbook B_s-mixing convention |

No fitted CKM observable, B-meson lifetime, or lattice-QCD parameter is used
as a derivation input. The B_s phase convention is a standard observation
bridge, not a new framework-native hadronic mixing theorem.

## Derivation

### 1. Atlas-triangle doubled-angle catalog

On the atlas surface,

```text
tan(beta_0)  = eta / (1-rho)  = (sqrt(5)/6) / (5/6) = sqrt(5)/5 = 1/sqrt(5),
tan(gamma_0) = eta / rho      = (sqrt(5)/6) / (1/6) =  sqrt(5),
alpha_0      = pi - beta_0 - gamma_0 = pi/2
            (using arctan(x) + arctan(1/x) = pi/2 for x>0).
```

Doubling via the standard tan-half formulas with `t = tan(theta)`:

```text
sin(2 theta) = 2t / (1 + t^2),
cos(2 theta) = (1 - t^2) / (1 + t^2).
```

Plug `t_beta = 1/sqrt(5)` (so `t_beta^2 = 1/5`):

```text
sin(2 beta_0) = (2/sqrt(5)) / (6/5) = 10/(6 sqrt(5)) = sqrt(5)/3,
cos(2 beta_0) = (4/5) / (6/5)       = 2/3.
```

Plug `t_gamma = sqrt(5)` (so `t_gamma^2 = 5`):

```text
sin(2 gamma_0) = (2 sqrt(5)) / 6    = sqrt(5)/3,
cos(2 gamma_0) = (1 - 5) / 6        = -2/3.
```

Identity `sin(2 beta_0) = sin(2 gamma_0)` is forced by
`2 beta_0 + 2 gamma_0 = pi`, equivalently `alpha_0 = pi/2`.

### 2. Side-length Pythagorean catalog

The atlas triangle has vertices `B = (0,0)`, `C = (1,0)`, `A = (rho, eta)`.
Side lengths squared:

```text
|BA|^2 = rho^2 + eta^2 = 1/36 + 5/36 = 6/36 = 1/6   [R_b^2],
|CA|^2 = (1-rho)^2 + eta^2
       = (5/6)^2 + 5/36 = 25/36 + 5/36 = 30/36 = 5/6  [R_t^2].
```

Adding,

```text
R_b^2 + R_t^2 = 1/6 + 5/6 = 1 = |BC|^2,
```

which is the Pythagorean relation forced by the right angle at `A`.
Equivalently `R_t / R_b = sqrt(5)`.

### 3. B_s unitarity-triangle phase

The B_s unitarity triangle is

```text
V_us V_ub^* + V_cs V_cb^* + V_ts V_tb^* = 0.
```

Its CP-violating angle is

```text
beta_s = arg[ -V_ts V_tb^* / (V_cs V_cb^*) ].
```

Inserting the Wolfenstein expansion truncated at `lambda^2`,

```text
V_ts V_tb^*    = -A lambda^2 [1 - lambda^2 (1/2 - rho - i eta)] + O(lambda^6),
V_cs V_cb^*    = (1 - lambda^2/2) (A lambda^2)
              = A lambda^2 (1 - lambda^2/2) + O(lambda^6),

-V_ts V_tb^* / (V_cs V_cb^*)
              = [1 - lambda^2 (1/2 - rho - i eta)] / (1 - lambda^2/2)
              = 1 + lambda^2 (rho + i eta) + O(lambda^4).
```

The argument of `1 + lambda^2 (rho + i eta) + O(lambda^4)` at leading
non-trivial order is

```text
beta_s = arctan( lambda^2 eta / (1 + lambda^2 rho) )
       = lambda^2 eta + O(lambda^4).
```

Inserting the retained identities `lambda^2 = alpha_s(v)/2` and
`eta = sqrt(5)/6`,

```text
beta_s = (alpha_s(v)/2) (sqrt(5)/6)
       = alpha_s(v) sqrt(5) / 12.
```

The B_s mixing CP-violating phase is the standard

```text
phi_s,0 = -2 beta_s,0 = -alpha_s(v) sqrt(5) / 6.
```

The small-angle expansion of `sin(2 beta_s)` matches `2 beta_s` to better
than one part in `1e4`.

### 4. Finite-lambda standard-matrix guardrail

The compact identities above are the atlas-leading CKM surface. If the same
retained inputs are inserted into the exact standard CKM parameterization,
with

```text
s12 = lambda,
s23 = A lambda^2,
s13 = A lambda^3 sqrt(rho^2 + eta^2),
delta = arctan(sqrt(5)),
```

then the direct standard-matrix ratio

```text
beta_s = arg[-V_ts V_tb^* / (V_cs V_cb^*)]
```

gives

```text
beta_s = 1.9609e-2 rad,
phi_s  = -3.9218e-2 rad.
```

This differs from the compact leading identity by `1.9%`, an `O(lambda^2)`
finite-CKM correction. The exact readout is a guardrail against promoting the
leading identity as an all-orders B_s-mixing theorem.

## Numerical Predictions

With the canonical `alpha_s(v) = 0.10330381612227...`,

| Quantity | Structural form | Atlas value | PDG/LHCb | Deviation |
| --- | --- | ---: | ---: | ---: |
| `sin(2 beta_0)` | `sqrt(5)/3` | `0.745356` | `0.706 +/- 0.011` | `+3.6 sigma` |
| `cos(2 beta_0)` | `2/3` | `0.666667` | `0.708 +/- 0.011` | -- |
| `sin(2 gamma_0)` | `sqrt(5)/3` | `0.745356` | -- | -- |
| `cos(2 gamma_0)` | `-2/3` | `-0.666667` | -- | -- |
| `R_b` | `1/sqrt(6)` | `0.408248` | `0.435 +/- 0.014` | `-1.9 sigma` |
| `R_t` | `sqrt(5/6)` | `0.912871` | `0.92 +/- 0.02` | `-0.4 sigma` |
| `R_t / R_b` | `sqrt(5)` | `2.236068` | `~2.27 +/- 0.07` | `-0.5 sigma` |
| `beta_s,0` | `alpha_s(v) sqrt(5)/12` | `0.019250 rad` | `0.0188 +/- 0.0030 rad` | `+0.15 sigma` |
| `phi_s,0` | `-alpha_s(v) sqrt(5)/6` | `-0.038499 rad` | `-0.039 +/- 0.022(stat) +/- 0.006(syst) rad` | `+0.02 sigma` |
| exact standard `phi_s` guardrail | standard CKM matrix | `-0.039218 rad` | `-0.039 +/- 0.022(stat) +/- 0.006(syst) rad` | `-0.01 sigma` |
| `sin(2 beta_s)` | `~ alpha_s(v) sqrt(5)/6` | `0.038490` | `~0.038 +/- 0.022` | `+0.02 sigma` |

The B_s phase prediction lies within the quoted LHCb 1-sigma band. The
atlas-leading `sin(2 beta_0)` retains a `3.6 sigma` tension relative to the
B_d -> J/psi K_S measurement, which is precisely the residual that the
finite-lambda barred-unitarity-triangle correction in
[`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
keeps outside the exact atlas-leading claim. This note keeps the
atlas-leading and finite-lambda predictions clearly separated.

## What This Claims

- `phi_s,0 = -alpha_s(v) sqrt(5)/6` as an atlas-leading retained CKM
  prediction for B_s mixing, with no fitted CKM or B-mixing input and a quoted
  LHCb comparator offset of `0.02 sigma`.
- `beta_s,0 = alpha_s(v) sqrt(5)/12` as the corresponding leading-order
  B_s unitarity triangle angle.
- The exact finite-`lambda` standard-matrix readout is carried only as a
  guardrail on the compact leading identity.
- `sin(2 beta_0) = sin(2 gamma_0) = sqrt(5)/3`, `cos(2 beta_0) = 2/3`,
  `cos(2 gamma_0) = -2/3` as exact atlas-triangle trigonometric identities.
- `R_t^2 = 5/6` as the Pythagorean companion to the retained `R_b^2 = 1/6`,
  equivalently `R_t / R_b = sqrt(5)` exactly.

## What This Does Not Claim

- It does not derive `alpha_s(v)`; that remains the retained plaquette/CMT
  input.
- It does not claim higher-order Wolfenstein corrections; the prediction is
  the leading non-trivial term, as is standard.
- It does not derive the hadronic B_s mixing amplitude, bag parameters,
  decay constants, lifetimes, penguin corrections, or a new lattice-QCD
  extraction of `phi_s`.
- It does not promote any BSM contribution to B_s mixing.
- It does not modify the parent CKM atlas/axiom or right-angle theorems; the
  atlas-leading `sin(2 beta_0) = sqrt(5)/3` retains its known tension with
  the precise B_d -> J/psi K_S measurement, just as the right-angle theorem
  records.

## Reproduction

```bash
python3 scripts/frontier_ckm_bs_mixing_phase_derivation.py
```

Expected result:

```text
TOTAL: PASS=53, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import.

## Cross-References

- `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
  -- parent CKM atlas/axiom package.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `rho`, `eta`, `delta_CKM` identities.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `lambda^2`, `A^2` identities.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- retained `alpha_0 = pi/2` and finite-lambda barred-triangle treatment.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` derivation.
- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
  -- companion atlas-leading `|V_td|`, `|V_ts|` magnitudes.
