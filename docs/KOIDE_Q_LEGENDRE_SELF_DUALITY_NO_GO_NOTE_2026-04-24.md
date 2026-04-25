# Koide Q Legendre/Self-Duality No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects normalized
Legendre/self-duality as a retained derivation of the charged-lepton
traceless source law.
**Primary runner:** `scripts/frontier_koide_q_legendre_self_duality_no_go.py`

---

## 1. Theorem Attempt

The strongest duality route is:

> the exact logdet Legendre geometry on the normalized second-order carrier
> might require the physical charged-lepton response to be self-dual under
> normalized inversion. Since the unique fixed point is `Y = I_2`, this would
> derive `K_TL = 0` and hence `Q = 2/3`.

The executable result is negative. Normalized inversion does have the Koide
fixed point, but retained Legendre geometry supplies a source-response
correspondence, not a fixed-point axiom.

---

## 2. Exact Dual Involution

On the trace-normalized carrier:

```text
Y = diag(y, 2-y), 0 < y < 2,
```

normalized inversion is:

```text
D(Y) = 2 Y^{-1} / Tr(Y^{-1}) = diag(2-y, y).
```

It is an involution:

```text
D(D(Y)) = Y.
```

The unique fixed point is:

```text
y = 1,
```

which is exactly:

```text
Y = I_2
<=> K_TL = 0
<=> Q = 2/3.
```

---

## 3. Why This Does Not Close Q

The same exact duality flips the residual:

```text
K_TL(D(y)) = -K_TL(y).
```

It does not force the residual to vanish. The runner checks the exact
off-center pair:

```text
y = 4/5  <->  D(y) = 6/5
K_TL = 5/24  <->  -5/24
Q = 5/6      <->  5/9
```

Both points are valid normalized carrier points with exact Legendre sources.
They are paired by the involution, not rejected by it.

---

## 4. Hostile Review

This route does not import mass-table data, observational pins, `Q = 2/3`,
`P_Q = 1/2`, `delta = 2/9`, or `K_TL = 0` as an assumption. The failed step is:

```text
Legendre correspondence -> physical fixed point.
```

That step is not retained. Requiring:

```text
Y = D(Y)
```

is the quotient block-exchange fixed-point law:

```text
y = 2-y.
```

This is exactly the missing equal-block/source-neutrality primitive in duality
language.

---

## 5. Brainstorm and Ranking Snapshot

Routes considered at this cycle:

```text
1. Legendre self-duality fixed point: high novelty, strong exact algebra, but likely block-exchange in disguise.
2. Categorical trace naturality: already packeted; leaves trace-state ratio.
3. Information-measure midpoint: already packeted; leaves measure-power prior.
4. RG/Ward fixed point: already packeted; leaves fixed-point coefficient.
5. Delta endpoint replay: lower Q relevance; defer unless Q routes saturate.
```

The selected route was `1` because it tests the exact duality structure most
closely tied to the retained second-order effective-action theorem.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_legendre_self_duality_no_go.py
```

Result:

```text
PASSED: 13/13
KOIDE_Q_LEGENDRE_SELF_DUALITY_NO_GO=TRUE
Q_LEGENDRE_SELF_DUALITY_CLOSES_Q=FALSE
RESIDUAL_SCALAR=legendre_self_duality_fixed_point_equiv_K_TL
```

---

## 7. Boundary

This note does not weaken the exact normalized effective-action support
theorem. It rejects only the stronger claim that retained Legendre duality
requires the physical charged-lepton response to be self-dual.

The remaining primitive is:

```text
derive the fixed-point law Y = D(Y),
```

equivalently:

```text
derive K_TL = 0.
```
