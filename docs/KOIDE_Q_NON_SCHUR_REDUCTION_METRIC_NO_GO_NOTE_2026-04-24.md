# Koide Q Non-Schur Reduction-Metric No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the non-Schur
full-lattice reduction escape hatch but does not close charged-lepton
`Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_non_schur_reduction_metric_no_go.py`

---

## 1. Theorem Attempt

The full-lattice Schur-inheritance theorem leaves a genuine escape hatch:

```text
a non-Schur or non-C_3-equivariant reduction map from the full lattice to the
charged sector.
```

The controlled-breaking audit handles the non-`C_3` direction. This note tests
the strongest remaining scale-free non-Schur route that still preserves the
retained `C_3` isotype split:

> change the positive reduction metric on the singlet/doublet carrier and ask
> whether the metric-weighted source-free point forces the Koide radius.

The executable result is negative.

The most general positive `C_3`-equivariant metric has one free ratio. The
Koide radius follows only after choosing the equal singlet/doublet metric,
which is the canonical Schur/Frobenius metric choice in another form.

---

## 2. C3-Equivariant Metric Freedom

Let `P_+` be the real singlet projector and `P_perp` the real doublet
projector for the retained `C_3` action on the three-slot carrier. A general
positive `C_3`-equivariant metric is:

```text
G = g_+ P_+ + g_perp P_perp,
g_+ > 0, g_perp > 0.
```

The runner verifies exactly:

```text
C G C^T = G
```

for arbitrary positive `g_+` and `g_perp`.

Thus retained `C_3` covariance does not force:

```text
g_+ = g_perp.
```

The ratio `g_+/g_perp` is a symmetry-allowed scalar.

---

## 3. Metric-Weighted Normalized Carrier

On the unweighted charged-lepton second-order carrier, write the block powers
as:

```text
E_+, E_perp.
```

A metric-weighted non-Schur normalized carrier is:

```text
Y_G = diag(
  2 g_+ E_+ / (g_+ E_+ + g_perp E_perp),
  2 g_perp E_perp / (g_+ E_+ + g_perp E_perp)
).
```

It still has:

```text
Tr(Y_G) = 2,
```

and common scale cancels exactly.

But source-freeness on this metric-weighted carrier gives:

```text
Y_G = I_2
<=> g_+ E_+ = g_perp E_perp
<=> E_perp/E_+ = g_+/g_perp.
```

So the non-Schur metric moves the source-free point according to a free metric
ratio.

---

## 4. Consequence For Q

The physical charged-lepton Koide quotient uses the unweighted block ratio:

```text
Q = (1 + E_perp/E_+)/3.
```

At the metric-weighted source-free point:

```text
Q = (1 + g_+/g_perp)/3,
c^2 = 2 g_+/g_perp,
kappa = 2 g_perp/g_+.
```

Therefore:

```text
Q = 2/3
<=> g_+ = g_perp.
```

That equality is not supplied by non-Schur reduction itself.

---

## 5. Exact Countermetrics

The runner checks exact positive `C_3`-equivariant metrics:

```text
g_+/g_perp = 1/2 -> E_perp/E_+ = 1/2, c^2 = 1, Q = 1/2
g_+/g_perp = 1   -> E_perp/E_+ = 1,   c^2 = 2, Q = 2/3
g_+/g_perp = 2   -> E_perp/E_+ = 2,   c^2 = 4, Q = 1
```

All three commute with the retained `C_3` action. Only the equal metric gives
the Koide leaf.

---

## 6. Source-Law Reading

The unweighted normalized source difference is:

```text
K_+ - K_perp.
```

After imposing source-freeness on `Y_G`, the runner verifies:

```text
K_+ - K_perp = (g_+ - g_perp)(g_+ + g_perp)/(2 g_+ g_perp).
```

So the physical unweighted traceless source still vanishes only for:

```text
g_+ = g_perp.
```

The non-Schur route has not derived `K_TL = 0`; it has changed the source
convention and exposed a metric-ratio law that must itself be derived.

---

## 7. Review Consequence

The non-Schur metric route proves:

```text
a C_3-equivariant non-Schur reduction can move the normalized source-free
point along the one-parameter charged-lepton Q family.
```

It does not prove:

```text
retained Cl(3)/Z^3 charged-lepton structure -> g_+/g_perp = 1.
```

The residual scalar is:

```text
g_+/g_perp = 1
equiv c^2 = 2
equiv K_TL = 0.
```

So this route cannot be promoted as a Koide closeout unless a retained theorem
selects the canonical equal singlet/doublet reduction metric.

---

## 8. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_non_schur_reduction_metric_no_go.py
```

Result:

```text
PASSED: 13/13
KOIDE_Q_NON_SCHUR_REDUCTION_METRIC_NO_GO=TRUE
Q_NON_SCHUR_REDUCTION_METRIC_CLOSES_Q=FALSE
RESIDUAL_METRIC_LAW=g_plus/g_perp=1_equiv_c^2=2_equiv_K_TL=0
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used as an input.

---

## 9. Boundary

This note does not demote:

- the full-lattice Schur-inheritance theorem;
- the exact first-live second-order carrier;
- the source-free effective-action support theorem on the admitted canonical
  normalized carrier.

It rejects only the stronger claim that moving to a non-Schur positive
reduction metric by itself derives the Koide radius.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0` or an
  equivalent retained radius/source/metric theorem;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
