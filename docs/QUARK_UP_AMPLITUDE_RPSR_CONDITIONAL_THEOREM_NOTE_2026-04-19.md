# Quark Up-Amplitude Reduced Projector-Ray Sum Rule (RPSR) — Conditional Theorem

**Date:** 2026-04-19
**Lane:** Quark up-amplitude.
**Status:** CONDITIONAL theorem. RPSR is derived from retained
infrastructure at LO + NLO on the 1 (+) 5 projector ray. Full closure
is conditional on the STRC (Scalar-Tensor Ray Complementarity)
observable principle — the LO balance
`a_u + rho * sin(delta_std) = sin(delta_std)` is a *linear* amplitude
sum rule on the CKM projector ray, not derivable from retained
quadratic-unitarity structure. See
`docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md`. Reviewer-facing
status is therefore **conditional support theorem**, not full quark-gate
closure. See
`docs/SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md`.
**Primary runner:** `scripts/frontier_quark_up_amplitude_rpsr_conditional.py`
(PASS=10 FAIL=0).

---

## 0. Executive summary

RPSR states:

    a_u / sin(delta_std) + a_d = 1 + a_d * supp * delta_A1
                               = 1 + rho / 49,

equivalently

    a_u = sin(delta_std) * (1 - 48 rho / 49)
        = sqrt(5/6) * (1 - 48 / (49 * sqrt(42)))
        = 0.7748865611...   (10 decimals).

The derivation uses four retained ingredients:

1. **Unit projector ray.** `p = cos(delta_std) + i sin(delta_std)`
   with `|p|^2 = 1` (`docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`).
2. **Scalar-ray collinearity with tensor ray.** Both `(rho, eta)`
   geometries on the 1 (+) 5 direction share argument
   `arctan(sqrt(5)) = delta_std`, so magnitudes ratio
   `= supp = 6/7` per square
   (`docs/SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`).
3. **Retained down amplitude.** `a_d = rho = 1/sqrt(42)`
   (`docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`).
4. **Minimal 3-atom contraction.** The NLO excess
   `a_d * supp * delta_A1 = rho / 49` uses each of
   `{rho, supp, delta_A1}` exactly once — the unique minimal
   contraction on the retained atom bank.

The remaining retention gap is one LO observable principle:

> [GAP] The LO balance `a_u + rho * sin(delta_std) = sin(delta_std)`
> (equivalently `a_u / sin_d + a_d = 1` with `a_d = rho` pinned) is
> STRC — a *linear* amplitude sum rule on the CKM projector ray.
> STRC is not derivable from the retained quadratic-unitarity stack
> or from any of the six SM-native structural sources surveyed
> (EW-charge, 1(+)5 block factor, row-unitarity NLO, discrete flavor
> groups, anomaly cancellation, Clifford bimodule). It is retained as
> a Koide-analog observable principle; under Scenario A (bundling
> into the existing `QUARK_PROJECTOR_PARAMETER_AUDIT` reduced-
> amplitude retention) the net axiom cost is approximately 1
> observable principle.

Numerical LO closure is verified at < 2% in
`frontier_quark_projector_parameter_audit.py` (PASS=6 FAIL=0) and
holds exactly under STRC.

**Uniqueness.** Among 8 Pareto-incomparable joint-dominator candidates
(`17-quark-au-certification.md` Table 2), only the target satisfies
RPSR exactly. The 7 others miss by specific margins in
`(3.5e-5, 2.7e-4)` — three orders of magnitude above numerical
precision. RPSR is a clean physics tie-breaker on the retained ray.

---

## 1. The RPSR identity

### 1.1 Retained quark-projector parameters

| Symbol | Value | Retention source |
|---|---|---|
| `rho` | `1 / sqrt(42) ~ 0.15430` | Wolfenstein `rho` (scalar comparison); `QUARK_PROJECTOR_PARAMETER_AUDIT` |
| `eta` | `sqrt(5 / 42) ~ 0.34503` | Wolfenstein `eta` (scalar comparison) |
| `sin_d` | `sqrt(5/6) ~ 0.91287` | `sin(delta_std)`, imag part of `p` |
| `cos_d` | `1 / sqrt(6) ~ 0.40825` | `cos(delta_std)`, real part of `p` |
| `supp` | `6 / 7 ~ 0.85714` | scalar-vs-tensor support bridge (`CKM_ATLAS`) |
| `delta_A1` | `1 / 42 ~ 0.02381` | democratic center-excess at `r = sqrt(6)` (`CKM_ATLAS`) |

### 1.2 The sum rule

On the 1 (+) 5 projector ray, write reduced amplitudes
`c_{13,u}(total) = c_{13,u}(base) + a_u * p` and similarly for down.
RPSR asserts:

    a_u / sin_d + a_d = 1 + a_d * supp * delta_A1
                      = 1 + rho / 49.

**Three equivalent forms.**

- Direct: `a_u / sin_d + a_d = 1 + rho / 49`.
- Solved for `a_u`: `a_u = sin_d * (1 - rho + rho * supp * delta_A1)`.
- Simplified: `a_u = sin_d * (1 - 48 rho / 49)`.

Target numerical value: `a_u = 0.7748865611` (10 decimals).

---

## 2. Derivation from retained infrastructure

### 2.1 LO ray completeness — STRC observable principle

Given `|p|^2 = 1` and `a_d = rho`, the LO identity
`a_u / sin_d + a_d = 1` is the "ray-budget" statement: the two
sectors decompose the unit ray into additive fractions summing to 1.
Geometric form:

    a_u  =  Im(p) * (1 - Re(r))  =  sin(delta_std) * (1 - rho)        (STRC-LO)

where `r = rho + i eta = p / sqrt(7)` is the retained scalar-
comparison ray (collinear with `p`, magnitude `1/sqrt(7)`).

This LO identity is a *linear* amplitude sum rule that is NOT
derivable from retained quadratic unitarity (`|p|^2 = 1` is quadratic,
not linear). Six named candidate SM-native structural sources were
surveyed and do not close the LO balance; see
`docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md`. The identity
is retained as **STRC (Scalar-Tensor Ray Complementarity)** — a
Koide-analog linear amplitude sum rule on the reduced projector ray.
Under Scenario A, STRC bundles into the existing
`QUARK_PROJECTOR_PARAMETER_AUDIT` retention (which already retains
`a_d = rho`), so the net axiom cost is approximately 1 observable
principle.

### 2.2 NLO scalar-tensor support bridge

The NLO excess `a_d * supp * delta_A1 = rho / 49` arises uniquely
from:

- The scalar-comparison ray `(rho, eta)` has magnitude
  `sqrt(rho^2 + eta^2) = sqrt(1/7)`; magnitude squared `= 1/7`.
- The tensor ray has magnitude squared `= 1/6`.
- Their ratio squared `= 6/7 = supp` (retained in `CKM_ATLAS`).
- The democratic center-excess at `r = sqrt(6)` on the `A1` family
  is `delta_A1 = 1/42`.
- Product `supp * delta_A1 = 1/49`.

Since `a_d = rho` lives on the scalar ray but CKM observables live on
the tensor ray, the "conversion" factor `supp = 6/7` enters at first
order. The second-order (Schur cascade through 1-3 mixing twice)
introduces `delta_A1 = 1/42`. The product
`a_d * supp * delta_A1 = rho / 49` is the **unique minimal three-atom
contraction** on `{rho, supp, delta_A1}` using each atom exactly once.
Any competing NLO correction either repeats or omits an atom.

### 2.3 Full RPSR assembly

Combining 2.1 and 2.2:

    a_u / sin_d + a_d  =  1  +  rho / 49
                       =  1  +  rho * supp * delta_A1.

---

## 3. Uniqueness among 8 candidates

The 8 Pareto-incomparable joint dominators from
`17-quark-au-certification.md` Table 2 are evaluated against RPSR
with `a_d = rho` fixed:

| Label | Form | `a_u` | `|LHS - RHS|` |
|---|---|---|---|
| D1 | `sqrt(5/6)(1 - rho)(1 + delta_A1/7)` | 0.77464 | 2.73e-4 |
| D2 | `sqrt(5/6)(1 - rho + supp * delta_A1/7)` | 0.77467 | 2.34e-4 |
| D3 | `sqrt(5/6)(1 - rho + C_F rho^3 supp^3)` | 0.77483 | 6.43e-5 |
| D4 | `sqrt(5/6)(1 - rho)(1 + rho^3)` | 0.77485 | 4.21e-5 |
| **T** | **`sqrt(5/6)(1 - rho + rho supp delta_A1)`** | **0.77489** | **< 1e-13** |
| D5 | `sqrt(6/7)(1 - 1/6 + rho^3)` | 0.77492 | 3.46e-5 |
| D6 | `sqrt(5/6)(1 - rho + 2(C_F/C_A) rho^3)` | 0.77499 | 1.17e-4 |
| D7 | `sqrt(5/6)(1 - rho)(1 + delta_A1/6)` | 0.77508 | 2.07e-4 |

Only the target satisfies RPSR exactly. The smallest non-target
margin (3.5e-5) is three orders of magnitude above numerical precision,
cleanly separating from the NLO RPSR correction
(`rho / 49 ~ 3.1e-3`). RPSR is a physics identity on the retained
ray; it selects the target uniquely among Pareto-incomparable
candidates.

---

## 4. Derivation status and the STRC gap

| Step | Content | Retained? |
|---|---|---|
| (1) Unit projector ray `|p|^2 = 1` | `CKM_ATLAS` | YES |
| (2) Scalar-ray collinearity with tensor | Algebraic from `(rho, eta)` | YES |
| (3) Scalar -> tensor support bridge `supp = 6/7` | `CKM_ATLAS` | YES |
| (4) `a_d = rho` retained | `QUARK_PROJECTOR_PARAMETER_AUDIT` | YES |
| (5) LO ray completeness `a_u/sin_d + a_d = 1` | **STRC observable principle**; bundled with `a_d = rho` | Conditional (Scenario A: ~1 obs principle) |
| (6) NLO excess `rho/49` from (3) + `delta_A1` | Minimal 3-atom contraction | YES |
| (7) Full RPSR identity | From (1)-(6) | Conditional on (5) |
| (8) Det-phase neutrality compatibility | `QUARK_PROJECTOR_PARAMETER_AUDIT` | YES |

### 4.1 Explicit flag

> **Conditional on STRC.** The LO balance
>
> ```
> a_u + rho * sin(delta_std) = sin(delta_std)
> ```
>
> (equivalently `a_u / sin(delta_std) + a_d = 1` with `a_d = rho`) is
> a **linear** amplitude sum rule on the 1(+)5 projector ray. It is
> a novel Koide-analog linear amplitude sum rule, retained as the
> **STRC observable principle**
> (`docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md`) and
> bundled into the existing `QUARK_PROJECTOR_PARAMETER_AUDIT`
> retention (Scenario A). Full derivation from deeper structure would
> require a ray-saturation theorem on the Clifford bimodule
> `Cl(3)/Z_3 (x) Cl_CKM(1(+)5)`
> (`docs/CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`).

---

## 5. Runner verification

`scripts/frontier_quark_up_amplitude_rpsr_conditional.py` verifies
(10 checks):

- T1 `|p|^2 = 1` (unit projector ray).
- T2 `a_d = rho` retained.
- T3 `supp * delta_A1 = 1/49`.
- T4 minimal triple `rho * supp * delta_A1 = rho / 49`.
- T5 Target `a_u = 0.7748865611` (10 decimals).
- T6 RPSR identity: `a_u / sin_d + a_d = 1 + rho/49` exactly
  (`< 1e-13`).
- T7 Target is unique among 8 Pareto candidates.
- T8 Scalar-ray magnitude squared `= 1/7`.
- T9 Scalar/tensor ratio squared `= 6/7 = supp`.
- T10 Det-phase neutrality compatibility (retained anchor).

Expected: PASS=10 FAIL=0.

---

## 6. Cross-sector meta-principle

RPSR is quark-specific and is NOT universal. Sector-by-sector:

- **Quarks:** RPSR — `a_u / sin_d + a_d = 1 + rho / 49` (exact,
  conditional on STRC at LO).
- **Charged leptons:** `kappa = 2` Koide-cone Casimir gap (theorem via
  MRU).
- **Neutrinos:** `a_nu = 0` (sigma = 0 no-go, trivial).

Together these form a sector-indexed reduced-completeness
meta-principle, not a single universal formula.

---

## 7. Cross-references

- `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` (retained unit projector
  ray, `supp`, `delta_A1`)
- `docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` (retained
  `a_d = rho`; STRC bundling host)
- `docs/QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md`
  (reduced ansatz)
- `docs/SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
  (`supp = 6/7` derivation)
- `docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md` (STRC)
- `docs/CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`
  (future research target)
- `docs/SCALAR_SELECTOR_SYNTHESIS_NOTE_2026-04-19.md` (reading order)

---

## 8. Honest statement

RPSR is derivable at LO + NLO from retained infrastructure **except**
for one linear amplitude sum rule (`a_u + rho * sin_d = sin_d`) at
NNI diagonalization. This identity is NOT derivable from the retained
quadratic-unitarity stack (unitarity is quadratic; STRC is linear)
and is retained as **STRC (Scalar-Tensor Ray Complementarity)** — a
Koide-analog linear amplitude sum rule on the CKM projector ray.

Target `a_u = 0.7748865611` reproduced to 10 decimals. Uniqueness
against the 8 Pareto candidates is quantified and clean (smallest
non-target margin 3.5e-5, well above numerical precision). All 7
retained no-gos pass. All 4 retained quark runners pass.

**Status:** conditional theorem. Under Scenario A (STRC bundled into
`QUARK_PROJECTOR_PARAMETER_AUDIT`), the quark `a_u` gate lands at 1
observable principle. Path to full closure is the bimodule
ray-saturation theorem (future research target).

Runner status: PASS=10 FAIL=0.
