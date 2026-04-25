# Koide Q Least-Source-Norm No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects least-traceless-source
norm as a retained derivation of the charged-lepton Koide source law.
**Primary runner:** `scripts/frontier_koide_q_least_source_norm_no_go.py`

---

## 1. Theorem Attempt

The simplified scalar route is:

> the physical charged-lepton selector might be the point on the normalized
> second-order carrier minimizing the exact traceless-source norm.

The executable calculation is exact: the unique least-source point is the
Koide leaf. The hostile-review result is still negative because no retained
law says the physical charged-lepton selector minimizes that norm.

---

## 2. Exact Scalar Calculation

On the trace-normalized carrier:

```text
Y = diag(y, 2-y), 0 < y < 2,
```

the exact traceless source scalar is:

```text
K_TL(y) = (1-y)/(y(2-y)).
```

The source norm is:

```text
|K_TL|^2 = (y-1)^2 / (y^2 (y-2)^2).
```

It has a unique interior zero and minimum:

```text
y = 1.
```

Thus:

```text
least |K_TL|
-> K_TL = 0
-> Y = I_2
-> Q = 2/3.
```

---

## 3. Why This Is Not Closure

The retained source-coupled effective-action grammar admits every interior
point with a matching source. The runner checks:

```text
y = 4/5
K_TL = 5/24
Q = 5/6.
```

This is a valid source-coupled point. It is excluded only after adopting the
extra physical rule:

```text
choose the least-source point.
```

That rule is source neutrality in variational language. It is not derived by
the retained `Cl(3)/Z^3` charged-lepton package.

---

## 4. Musk Simplification Pass

After the Legendre/self-duality, dihedral-normalizer, `Cl(3)` grade-involution,
delta spectral-flow, and least-source audits, the proof target has simplified
again:

```text
All successful-looking routes select Q only by imposing a fixed-point,
equal-block, endpoint, or zero-source choice.
```

Deleted as insufficient:

```text
self-dual fixed point,
D3/S3 normalizer reflection,
Cl(3) grade/chiral parity,
integer spectral-flow endpoint quantization,
least-source minimization without a retained physical law.
```

The smallest unresolved Q statement remains:

```text
derive K_TL = 0 from retained charged-lepton dynamics.
```

---

## 5. Hostile Review

This route does not import mass-table data, observational pins, `Q = 2/3`,
`P_Q = 1/2`, `delta = 2/9`, or `K_TL = 0` as an assumption. It uses the target
leaf only as the zero of the exact residual scalar.

The failure is:

```text
exact source norm has minimum at K_TL = 0
```

but not:

```text
retained physics requires minimizing |K_TL|.
```

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_least_source_norm_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_LEAST_SOURCE_NORM_NO_GO=TRUE
Q_LEAST_SOURCE_NORM_CLOSES_Q=FALSE
RESIDUAL_SCALAR=least_source_norm_selection_equiv_K_TL
```

---

## 7. Boundary

This note keeps the least-source calculation as support. It rejects only the
claim that least-source selection is already retained. Positive closure still
needs an independent physical theorem that makes the charged-lepton selector
source-neutral.
