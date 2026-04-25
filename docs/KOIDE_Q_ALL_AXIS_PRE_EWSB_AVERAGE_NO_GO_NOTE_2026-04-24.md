# Koide Q All-Axis / Pre-EWSB Averaging No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the all-axis
pre-EWSB symmetry escape hatch but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_all_axis_pre_ewsb_average_no_go.py`

---

## 1. Theorem Attempt

The full-cube `Gamma_i` orbit law proves that one local three-slot template
generates the exact axis family:

```text
D_1 = diag(u,v,w),
D_2 = diag(w,u,v),
D_3 = diag(v,w,u).
```

The attempted closure upgrade is:

> all-axis / pre-EWSB covariance forces the physical charged-lepton selector by
> averaging or symmetrizing the three axis returns before weak-axis selection.

The executable result is negative.

All-axis averaging erases the doublet and gives the degenerate point. If weak
axis selection is applied first, the template `(u,v,w)` remains free and Koide
requires the same selector cone as an extra law.

---

## 2. Brainstorm And Ranking

This route was chosen after the full-taste source-neutral no-go because it
attacks the next strongest assumption inversion:

```text
What if we selected the weak axis too early?
```

Five variants remain live at this point:

```text
1. all-axis / pre-EWSB averaging;
2. higher-order O_3 return source balancing;
3. Q-delta residual bootstrap;
4. nonlocal spectral readout beyond the eigenvalue-channel no-go;
5. positive one-clock semigroup value law without selector import.
```

All-axis averaging ranked first because it is exact, local, and directly
tests whether pre-EWSB symmetry can supply the missing source law.

---

## 3. Exact Check

The axis-covariant orbit gives:

```text
D_1 = (u,v,w),
D_2 = (w,u,v),
D_3 = (v,w,u).
```

The Koide quotient is invariant under these cyclic permutations:

```text
Q(D_1) = Q(D_2) = Q(D_3).
```

But literal all-axis averaging gives:

```text
(D_1 + D_2 + D_3)/3 = ((u+v+w)/3, (u+v+w)/3, (u+v+w)/3),
```

therefore:

```text
Q(<D_i>) = 1/3.
```

Similarly, averaging source-free axis identities gives only the identity
point. It does not produce a nondegenerate Koide hierarchy.

---

## 4. What Remains After Axis Selection

If weak-axis selection happens before charged-lepton readout, the family is:

```text
Q(u,v,w) = (u^2+v^2+w^2)/(u+v+w)^2.
```

The Koide leaf is exactly:

```text
Q = 2/3
<=> u^2 + v^2 + w^2 = 4(uv + uw + vw).
```

That selector cone is not derived by all-axis covariance. It is precisely the
missing source/radius law in the three-slot template coordinates.

Exact samples:

```text
(1,1,1)                 -> Q = 1/3
(1,2,3)                 -> Q = 7/18
(1,4+3 sqrt(2),1)       -> Q = 2/3
(4,1,1)                 -> Q = 1/2
```

---

## 5. Assumption Inversion Result

The route splits cleanly:

```text
keep pre-EWSB all-axis symmetry -> hierarchy is erased, Q = 1/3;
select a weak axis first        -> hierarchy is possible, but values are free.
```

So pre-EWSB/all-axis covariance does not derive `K_TL = 0`. It either deletes
the hierarchy or leaves the selector law untouched.

---

## 6. Review Consequence

The all-axis route proves:

```text
the exact Gamma_i orbit is consistent and cyclic across the three weak axes.
```

It does not prove:

```text
retained Cl(3)/Z^3 charged-lepton structure
-> u^2+v^2+w^2 = 4(uv+uw+vw).
```

The residual scalar is:

```text
u^2+v^2+w^2 = 4(uv+uw+vw)
equiv K_TL = 0.
```

So this route cannot be promoted as a Koide closeout unless a retained theorem
selects the three-slot template cone without importing the target.

---

## 7. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_all_axis_pre_ewsb_average_no_go.py
```

Result:

```text
PASSED: 11/11
KOIDE_Q_ALL_AXIS_PRE_EWSB_AVERAGE_NO_GO=TRUE
Q_ALL_AXIS_PRE_EWSB_AVERAGE_CLOSES_Q=FALSE
RESIDUAL_TEMPLATE_SELECTOR=u^2+v^2+w^2=4(uv+uw+vw)_equiv_K_TL=0
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used as an input.

---

## 8. Boundary

This note does not demote:

- the exact full-cube `Gamma_i` orbit law;
- the first-live second-order carrier;
- the possibility of a future retained value law on the three-slot template.

It rejects only the stronger claim that pre-EWSB all-axis averaging itself
derives the Koide source law.
