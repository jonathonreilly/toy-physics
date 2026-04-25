# Koide Q Positive-Parent Spectral-Value No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the positive-parent /
`sqrt(m)` route but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_positive_parent_spectral_value_no_go.py`

---

## 1. Theorem Attempt

The positive-parent route has a strong exact statement:

```text
M positive Hermitian
Y = M^(1/2)
eig(Y) = sqrt(eig(M)).
```

The tempting closure upgrade is:

> a positive `C_3`-covariant parent makes the charged-lepton `sqrt(m)` readout
> physical and thereby closes Koide.

The executable result is negative.

---

## 2. What Survives

For every positive spectral triple

```text
lambda = (lambda_0, lambda_1, lambda_2),
```

functional calculus constructs:

```text
Y = F^dag diag(lambda_0, lambda_1, lambda_2) F,
M = Y^2 = F^dag diag(lambda_0^2, lambda_1^2, lambda_2^2) F.
```

The runner verifies exactly:

- `M` is Hermitian;
- `M` commutes with the retained `C_3` shift;
- `Y^2 = M`;
- the principal square root carries the spectral amplitudes.

This is valid support for the square-root dictionary.

---

## 3. What Is Not Derived

The construction does not select the spectral ratios. After removing common
scale, a positive spectral parent still has two projective ratios:

```text
u = lambda_1/lambda_0,
v = lambda_2/lambda_0.
```

The Koide value computed from the spectral amplitudes is:

```text
Q(u,v) = (1 + u^2 + v^2)/(1 + u + v)^2.
```

This is not constant. The runner checks exact samples:

```text
lambda = (1,1,1)      -> Q = 1/3
lambda = (1,2,3)      -> Q = 7/18
lambda = Koide sample -> Q = 2/3
```

So Koide is an extra equation on the chosen spectrum, not a consequence of
positive-parent existence.

---

## 4. Readout Obstruction

The axis-basis diagonal entries of a `C_3`-covariant parent are all equal:

```text
diag_axis(M) = ((m_0+m_1+m_2)/3,
                (m_0+m_1+m_2)/3,
                (m_0+m_1+m_2)/3).
```

Thus a nondegenerate positive parent places the hierarchy in the eigenvalue
channel, not in the current strict axis-diagonal charged-lepton readout.

For example:

```text
eig(M) = (1,4,9)
diag_axis(M) = (14/3,14/3,14/3),
```

with nonzero off-diagonal axis-basis entries.

Therefore a positive-parent closure needs one extra physical statement:

- a value law selecting the spectral ratios;
- a retained selected-line law selecting the spectrum;
- or an independently justified eigenvalue-channel readout primitive.

---

## 5. Review Consequence

The positive-parent route proves:

```text
chosen positive spectrum -> square-root amplitude operator.
```

It does not prove:

```text
retained charged-lepton physics -> chosen Koide spectrum.
```

Nor does it prove that the eigenvalue channel is the physical charged-lepton
mass readout on the current retained surface.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_positive_parent_spectral_value_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_POSITIVE_PARENT_SPECTRAL_VALUE_NO_GO=TRUE
Q_POSITIVE_PARENT_CONSTRUCTION_CLOSES_Q=FALSE
RESIDUAL_DATA=spectral_ratios_or_eigenvalue_readout
```

---

## 7. Boundary

This note does not demote the square-root/positive-parent dictionary. It
demotes only the stronger claim that positive-parent existence by itself
selects the charged-lepton Koide spectrum or readout channel.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0`;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
