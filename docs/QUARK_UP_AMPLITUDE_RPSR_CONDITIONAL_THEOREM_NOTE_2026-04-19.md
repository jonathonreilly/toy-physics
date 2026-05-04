# Quark Up-Amplitude Reduced Projector-Ray Sum Rule (RPSR)

**Date:** 2026-04-19
**Lane:** Quark up-amplitude.
**Status:** Derived theorem. The old LO condition is now discharged by
`docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`, which proves
the physical law
`a_u + rho * sin(delta_std) = sin(delta_std)` as exact `1(+)5` channel
completeness on the physical reduced carrier. This note now records the
downstream LO+NLO RPSR assembly. The historical filename is preserved from the
earlier conditional stage.
**Primary runner:** `scripts/frontier_quark_up_amplitude_rpsr_conditional.py`
(PASS=9 FAIL=0). T10 (det-phase neutrality compatibility) is checked in the
companion runner `scripts/frontier_quark_projector_parameter_audit.py`
(PASS=6 FAIL=0); see Section 5 for the split.

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

The old LO gap is now closed:

> [DISCHARGED] The LO balance `a_u + rho * sin(delta_std) = sin(delta_std)`
> is no longer carried as a separate observable principle here. It is derived
> in `docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md` from the exact
> `1(+)5` carrier, the canonical `5`-projector, and the canonical
> `A1 -> 5` transfer operator induced by the physical projector ray.

The companion note
`docs/QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md`
provides an independent support-side derivation of the same LO balance from
the exact shell-normalized Route-2 carrier.

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

### 2.1 LO ray completeness — STRC theorem

Given `|p|^2 = 1` and `a_d = rho`, the LO identity
`a_u / sin_d + a_d = 1` is the "ray-budget" statement: the two
sectors decompose the unit ray into additive fractions summing to 1.
Geometric form:

    a_u  =  Im(p) * (1 - Re(r))  =  sin(delta_std) * (1 - rho)        (STRC-LO)

where `r = rho + i eta = p / sqrt(7)` is the retained scalar-
comparison ray (collinear with `p`, magnitude `1/sqrt(7)`).

This LO identity is now derived in
`docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md` as exact
`1(+)5` channel completeness:

- `Pi_5 p = sin_d e_5` is the total physical `5` budget,
- `T_p = Pi_5 |p><e_1| = sin_d |e_5><e_1|` is the canonical `A1 -> 5`
  transfer operator induced by the physical ray,
- applying `T_p` to the retained down occupancy `a_d e_1` gives the mixed
  channel budget `a_d sin_d e_5`,
- the up-sector amplitude is the unique residual on the one-dimensional
  `5` channel.

So the LO balance is no longer an added postulate in this lane.

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

## 4. Derivation status

| Step | Content | Retained? |
|---|---|---|
| (1) Unit projector ray `|p|^2 = 1` | `CKM_ATLAS` | YES |
| (2) Scalar-ray collinearity with tensor | Algebraic from `(rho, eta)` | YES |
| (3) Scalar -> tensor support bridge `supp = 6/7` | `CKM_ATLAS` | YES |
| (4) `a_d = rho` retained | `QUARK_PROJECTOR_PARAMETER_AUDIT` | YES |
| (5) LO ray completeness `a_u/sin_d + a_d = 1` | `STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md` | YES |
| (6) NLO excess `rho/49` from (3) + `delta_A1` | Minimal 3-atom contraction | YES |
| (7) Full RPSR identity | From (1)-(6) | YES |
| (8) Det-phase neutrality compatibility | `QUARK_PROJECTOR_PARAMETER_AUDIT` (verified by its own runner) | YES |

### 4.1 Exact LO discharge

> The LO balance
>
> ```
> a_u + rho * sin(delta_std) = sin(delta_std)
> ```
>
> is now discharged by exact operator algebra on the physical `1(+)5`
> carrier, not by a separate observable-principle postulate. The named
> future-target note remains useful as route history, but this lane no longer
> depends on it for LO closure.

---

## 5. Runner verification

`scripts/frontier_quark_up_amplitude_rpsr_conditional.py` verifies
(9 checks):

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

Expected: PASS=9 FAIL=0.

T10 (det-phase neutrality compatibility) is intentionally not re-checked
in this runner to avoid a hardcoded annotation PASS. It is verified in
the companion runner `scripts/frontier_quark_projector_parameter_audit.py`
(PASS=6 FAIL=0), which holds the retained anchor for the projector
parameter audit.

---

## 6. Cross-sector meta-principle

RPSR is quark-specific and is NOT universal. Sector-by-sector:

- **Quarks:** RPSR — `a_u / sin_d + a_d = 1 + rho / 49` (exact).
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

RPSR is now derivable at LO + NLO from retained infrastructure.

The former LO gap

```text
a_u + rho * sin_d = sin_d
```

is discharged in
`docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
as exact `1(+)5` channel completeness on the physical reduced carrier.

Target `a_u = 0.7748865611` reproduced to 10 decimals. Uniqueness
against the 8 Pareto candidates is quantified and clean (smallest
non-target margin 3.5e-5, well above numerical precision). All 7
retained no-gos pass. All 4 retained quark runners pass.

**Status:** derived theorem. The quark `a_u` gate no longer depends on a
separate STRC observable-principle postulate in this lane.

Runner status: PASS=9 FAIL=0 (this runner) plus PASS=6 FAIL=0 in the
companion `frontier_quark_projector_parameter_audit.py`.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [ckm_atlas_axiom_closure_note](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [quark_projector_parameter_audit_note_2026-04-19](QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
- [scalar_tensor_ray_magnitude_bridge_note_2026-04-19](SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md)
- [strc_lo_collinearity_theorem_note_2026-04-19](STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md)
