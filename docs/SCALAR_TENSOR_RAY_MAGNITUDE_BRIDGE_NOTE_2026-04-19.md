# Scalar-Tensor Ray-Magnitude Bridge

**Date:** 2026-04-19
**Lane:** Quark CKM atlas / 1 (+) 5 projector-ray geometry.
**Status:** support - structural or confirmatory support note
theorem. Retained inside `CKM_ATLAS_AXIOM_CLOSURE_NOTE`.

---

## 0. Summary

On the 1 (+) 5 CKM projector-ray direction, two coexisting ray
geometries share a common argument and differ only in magnitude:

- **Tensor ray:** `(rho_T, eta_T) = (1/6, sqrt(5)/6)`, magnitude
  squared `|tensor-ray|^2 = 1/6`.
- **Scalar-comparison ray:** `(rho, eta) = (1/sqrt(42), sqrt(5/42))`,
  magnitude squared `|scalar-ray|^2 = 1/7`.

Both vectors have argument `arctan(sqrt(5)) = delta_std`, i.e. they
are **collinear**. The magnitude ratio gives the retained
support-bridge factor

    supp  =  |scalar-ray|^2  /  |tensor-ray|^2  *  (7/6)
          =  6 / 7.

This is the scalar-to-tensor support-bridge identity retained in
`docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`.

The clean reading: **`supp = 6/7` is the squared-ray-magnitude ratio
on the common 1 (+) 5 CKM direction**.

---

## 1. Context

This identity feeds the RPSR derivation (see
`docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`)
as the structural origin of the NLO excess
`a_d * supp * delta_A1 = rho / 49`:

- `a_d = rho` lives on the scalar-comparison ray.
- CKM observables (`|V_us|`, `|V_cb|`, `|V_ub|` magnitudes etc.) live
  on the tensor ray.
- The conversion scalar -> tensor carries the factor `supp = 6/7` at
  first order.
- The second-order Schur-cascade factor `delta_A1 = 1/42` combines
  with `supp` to give `supp * delta_A1 = 1/49` exactly, which
  multiplied by `a_d = rho` gives the `rho / 49` NLO RPSR excess.

Without the scalar-tensor bridge, the NLO RPSR correction would be
unanchored. With it, the correction is the **unique minimal 3-atom
contraction** on the retained atom bank `{rho, supp, delta_A1}` using
each atom exactly once.

---

## 2. Verification

Verified algebraically by direct computation:

| Quantity | Value | Check |
|---|---|---|
| `rho^2 + eta^2` (scalar-ray mag sq) | `1/42 + 5/42 = 6/42 = 1/7` | exact |
| `1/6` (tensor-ray mag sq) | `1/6` | exact |
| ratio `(scalar/tensor)^2` | `(1/7) / (1/6) = 6/7` | exact |
| `supp` (retained) | `6/7` | exact |

Also verified in the RPSR runner: checks T8 and T9 of
`scripts/frontier_quark_up_amplitude_rpsr_conditional.py`.

---

## 3. Cross-references

- `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` (`supp` retention, source)
- `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
  (RPSR theorem, primary application)
- `docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` (retained
  `(rho, eta)` scalar-comparison values)

---

## 4. Status

This is a retained structural identity. It is NOT an independent axiom
or theorem — it is a direct algebraic consequence of the retained
`(rho, eta)` scalar-comparison values combined with the retained
tensor-ray structure. The content is: the two ray geometries on the
1 (+) 5 direction are collinear and differ only in magnitude by
`supp = 6/7`.

**Significance.** The bridge `supp = 6/7` is structurally forced by
the retained CKM atlas, not a free parameter. It is the squared-
magnitude ratio of the two coexisting rays on the common 1 (+) 5
direction.

No dedicated runner (the identity is verified inside
`frontier_quark_up_amplitude_rpsr_conditional.py`).
