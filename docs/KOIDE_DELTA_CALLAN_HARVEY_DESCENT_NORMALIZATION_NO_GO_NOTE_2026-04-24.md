# Koide Delta Callan-Harvey Descent-Normalization No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the Brannen
`delta = 2/9` bridge but does not close it.
**Primary runner:** `scripts/frontier_koide_delta_callan_harvey_descent_normalization_no_go.py`

---

## 1. Theorem Attempt

The strongest current delta route is the Callan-Harvey / APS descent candidate:

```text
ambient APS / anomaly value = 2/9
```

and the intended bridge is:

```text
physical selected-line Brannen phase delta = ambient APS / anomaly value.
```

The precise theorem attempted here is:

> The retained `Cl(3)/Z^3` and `Z_3` anomaly/APS package forces the
> selected-line Berry phase to equal the descended ambient anomaly with unit
> normalization.

The executable result is negative.

---

## 2. What Is Retained Support

The runner verifies two exact support scalars:

```text
eta_APS(Z_3; weights 1,2) = 2/9
```

and

```text
A_CH = (2d) * (1/d)^3 = 2/9   at d = 3.
```

These agree exactly:

```text
eta_APS = A_CH = 2/9.
```

This remains strong support for the delta lane.

---

## 3. Residual Scalar

The physical bridge still has the form

```text
delta_physical = N_desc * eta_APS,
```

where `N_desc` packages the two missing physical statements named in the
Callan-Harvey candidate note:

1. the selected-line Berry phase is the descended inflow/anomaly object;
2. the descent length or normalization is exactly one.

The exact residual is therefore:

```text
delta_physical / eta_APS - 1 = N_desc - 1.
```

The current retained APS/anomaly equations contain no equation for `N_desc`.
The runner checks this as a zero-rank Jacobian with respect to `N_desc`.

---

## 4. Counterfamily

The family

```text
N_desc in {1/2, 1, 3/2}
```

keeps every retained support statement true:

```text
eta_APS = 2/9,
A_CH = 2/9,
eta_APS = A_CH.
```

but gives different selected-line phases:

```text
N_desc = 1/2 -> delta = 1/9
N_desc = 1   -> delta = 2/9
N_desc = 3/2 -> delta = 1/3
```

Thus the retained support arithmetic fixes the ambient scalar, but not the
physical selected-line normalization.

---

## 5. Review Consequence

Promoting this route to closure requires adding:

```text
N_desc = 1.
```

That is exactly the missing Berry/inflow identification plus unit
descent-normalization theorem. It is not derived by the current APS/anomaly
package.

The delta lane therefore remains open:

```text
derive N_desc = 1
```

without assuming `delta = 2/9`, `delta = eta_APS`, PDG mass matching, or an
unexplained physical selected-line primitive.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_delta_callan_harvey_descent_normalization_no_go.py
```

Result:

```text
PASSED: 8/8
KOIDE_DELTA_CALLAN_HARVEY_DESCENT_NORMALIZATION_NO_GO=TRUE
DELTA_CALLAN_HARVEY_ROUTE_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=N_desc - 1
```

---

## 7. Boundary

This note does not demote the ambient APS/anomaly result. It demotes only the
stronger claim that the present Callan-Harvey descent candidate already proves
the physical selected-line Brannen phase.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0`;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
