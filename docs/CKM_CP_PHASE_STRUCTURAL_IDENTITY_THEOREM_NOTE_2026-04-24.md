# CKM CP-Phase Structural Identity Theorem

**Date:** 2026-04-24
**Status:** proposed_retained standalone structural-identity theorem on `main`.
This note extracts, names, and regression-tests the CKM CP-phase identities
already present inside
`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`. It does
not change the status of the parent CKM atlas package.

**Primary runner:** `scripts/frontier_ckm_cp_phase_structural_identity.py`

---

## 1. Statement

On the retained CKM atlas/axiom surface, the six-state quark block has the
projector split

```text
6 = 1 + 5
```

with one `A1` center-excess channel and a five-dimensional orthogonal channel.
The resulting angular weights are

```text
w_A1   = 1/6
w_perp = 5/6.
```

The retained CKM atlas separately fixes the bright/tensor CP radius

```text
r^2 = rho^2 + eta^2 = 1/6.
```

Therefore the Wolfenstein CP-plane coordinates are

```text
rho = r sqrt(w_A1)   = 1/6
eta = r sqrt(w_perp) = sqrt(5)/6.
```

The CKM phase then satisfies the exact identities

```text
cos^2(delta_CKM) = 1/6
sin^2(delta_CKM) = 5/6
tan(delta_CKM)   = sqrt(5)
delta_CKM        = arccos(1/sqrt(6)) = arctan(sqrt(5))
                 = 65.905157447889... degrees.
```

The atlas/Wolfenstein Jarlskog-area factor factorises as

```text
J_0 = lambda^6 A^2 eta
    = (alpha_s(v)/2)^3 * (2/3) * (sqrt(5)/6)
    = alpha_s(v)^3 sqrt(5) / 72.
```

The `lambda^2 = alpha_s(v)/2` and `A^2 = 2/3` factors used in this
factorisation are named separately in
[`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md).

The phase identities are pure structural numbers. The numerical value of
`J_0` still inherits the separately retained `alpha_s(v)` input from the
canonical plaquette/CMT surface. The parent CKM atlas note separately carries
the finite-`lambda` exact standard-matrix `J` readout.

## 2. Retained Inputs

| Ingredient | Authority |
| --- | --- |
| Parent CKM atlas/axiom package | `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` |
| Quark-block dimension `dim(Q_L) = 2 x 3 = 6` | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), parent CKM atlas |
| Exact `1 + 5` center-excess projector weights | parent CKM atlas; tensor support notes used there |
| Bright/tensor CP radius `r^2 = 1/6` | parent CKM atlas |
| Canonical `alpha_s(v)` for the J factorisation | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |

No quark mass, fitted CKM observable, or observation-side phase is used as a
derivation input.

## 3. Derivation

The important bookkeeping point is that two different `1/6` statements occur:

1. `w_A1 = 1/6` is the angular weight of the `A1` channel in the `1 + 5`
   projector split.
2. `r^2 = rho^2 + eta^2 = 1/6` is the retained CKM CP radius squared on the
   bright/tensor atlas surface.

Combining them gives

```text
rho^2 = r^2 w_A1   = (1/6)(1/6) = 1/36
eta^2 = r^2 w_perp = (1/6)(5/6) = 5/36.
```

Taking the positive CKM branch,

```text
rho = 1/6,
eta = sqrt(5)/6,
rho^2 + eta^2 = 1/36 + 5/36 = 1/6.
```

The standard CKM phase angle obeys

```text
cos(delta_CKM) = rho / sqrt(rho^2 + eta^2)
sin(delta_CKM) = eta / sqrt(rho^2 + eta^2).
```

Substitution gives

```text
cos^2(delta_CKM) = (1/36)/(1/6) = 1/6
sin^2(delta_CKM) = (5/36)/(1/6) = 5/6
tan(delta_CKM)   = sqrt(5).
```

Thus

```text
delta_CKM = arccos(1/sqrt(6)) = arctan(sqrt(5)).
```

For `J_0`, use the parent atlas inputs `lambda^2 = alpha_s(v)/2` and
`A^2 = 2/3`:

```text
J_0 = lambda^6 A^2 eta
    = (alpha_s(v)/2)^3 * (2/3) * (sqrt(5)/6)
    = alpha_s(v)^3 sqrt(5) / 72.
```

## 4. What This Claims

- `cos^2(delta_CKM) = 1/6` exactly on the retained CKM atlas surface.
- Equivalently, `tan(delta_CKM) = sqrt(5)` exactly.
- `rho = 1/6`, `eta = sqrt(5)/6`, and `rho^2 + eta^2 = 1/6` exactly on the
  same atlas surface.
- `J_0 = alpha_s(v)^3 sqrt(5) / 72` as a retained atlas-area factorisation
  once the parent atlas `alpha_s(v)` input is supplied.
- The structural origin is the retained `1 + 5` center-excess projector split
  plus the retained bright/tensor CP radius.

## 5. What This Does Not Claim

- It does not derive `alpha_s(v)`; that remains the separate plaquette/CMT
  input already used by the CKM atlas.
- It does not derive CKM magnitudes beyond the parent atlas package.
- First- and third-row magnitude identities are named separately in
  `CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`
  and
  `CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`,
  which preserves the finite-`lambda` standard-matrix guardrail.
- It does not promote the older bounded Cabibbo, mass-basis NNI, or partial
  Jarlskog route-history notes as controlling authority.
- It does not claim BSM CP phases, PMNS phases, or Majorana phases.
- It does not claim a new experimental projection or date-specific future
  sensitivity window; future global fits simply test the sharp identity
  `delta_CKM = 65.905157447889... degrees`.

## 6. Post-Derivation Comparators

The parent atlas already records the observation-side comparator split. This
standalone note keeps the same posture: comparison is downstream of the
theorem, not an input.

| Quantity | Structural value | Comparator role |
| --- | ---: | --- |
| `delta_CKM` | `65.905157... deg` | angle-facing global-fit comparator |
| `cos^2(delta_CKM)` | `1/6` | exact falsification surface |
| atlas `J_0` | `alpha_s(v)^3 sqrt(5)/72` | depends on separately retained `alpha_s(v)` |

The current canonical plaquette value used by the executable gives
`J_0 = 3.4237e-5`, which remains within the parent atlas' observation-comparator
band. The exact theorem content is the atlas factorisation, not a new
independent `alpha_s(v)` determination.

## 7. Reproduction

```bash
python3 scripts/frontier_ckm_cp_phase_structural_identity.py
```

Expected result:

```text
TOTAL: PASS=27, FAIL=0
```

The runner uses only the Python standard library plus the already-mainline
`scripts/canonical_plaquette_surface.py` constants. It intentionally does not
depend on `sympy`.

## 8. Relationship To Adjacent Rows

| Row | Status after this note |
| --- | --- |
| Full CKM atlas/axiom package | unchanged parent authority |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | standalone retained Wolfenstein structural identities in the companion note |
| `cos^2(delta_CKM) = 1/6` | standalone retained structural identity |
| `rho = 1/6`, `eta = sqrt(5)/6` | standalone retained coordinate identities |
| `J_0 = alpha_s(v)^3 sqrt(5)/72` | standalone retained atlas factorisation conditioned on parent `alpha_s(v)` |
| CKM-only neutron EDM | unchanged downstream corollary on the retained `theta_eff = 0` surface |
| Third-row CKM magnitudes | standalone atlas-leading identities with finite-`lambda` guardrail in the third-row companion note |

This is the same extraction pattern as
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`:
an implicit retained result is named, bounded, and regression-tested without
expanding the parent theorem's scope.
