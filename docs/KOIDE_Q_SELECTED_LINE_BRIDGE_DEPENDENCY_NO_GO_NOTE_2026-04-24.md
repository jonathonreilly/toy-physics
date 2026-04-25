# Koide Q Selected-Line Bridge Dependency No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the selected-line
axis/Fourier support route but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_selected_line_bridge_dependency_no_go.py`

---

## 1. Theorem Attempt

The selected-line axis/Fourier bridge is strong support:

```text
axis slots on the retained selected line
  = v0 * Brannen Fourier envelopes.
```

The tempting closure upgrade is:

> the selected-line bridge itself forces `Q = 2/3`.

The executable result is negative.

The bridge closes `Q` only after the Brannen radius has already been fixed to

```text
c = sqrt(2).
```

That radius law is exactly the missing `Q` value law in another coordinate.

---

## 2. Free-Radius Envelope

The runner frees the Brannen radius:

```text
lambda_k = 1 + c cos(theta + 2*pi*k/3),    k = 0,1,2.
```

Then exact trigonometric sums give:

```text
sum_k lambda_k = 3,
sum_k lambda_k^2 = 3 + (3/2)c^2.
```

Therefore

```text
Q(c) = (sum lambda_k^2)/(sum lambda_k)^2
     = 1/3 + c^2/6.
```

No phase value appears in `Q(c)`.

---

## 3. Phase Is Orthogonal To Q

The runner verifies:

```text
dQ/dtheta = 0.
```

So a theorem deriving the physical selected-line phase, even a valid derivation
of `delta = 2/9`, would not by itself close `Q`.

The phase controls the position around the Brannen circle. The `Q` value is
controlled by the circle radius.

---

## 4. What Must Be Derived

The exact condition for the Koide value is:

```text
Q(c) = 2/3
<=> c^2 = 2
<=> c = sqrt(2)       (positive radius).
```

In circulant block language, with

```text
c = 2|b|/a,
kappa = a^2/|b|^2,
```

this is:

```text
kappa = 4/c^2 = 2.
```

This is the same `A1` / block-democracy / normalized-source condition already
isolated elsewhere:

```text
kappa = 2
<=> Q = 2/3
<=> K_TL = 0
```

on the normalized second-order carrier.

---

## 5. Exact Counterexamples

The same envelope form allows different exact `Q` values:

```text
c = 0       -> Q = 1/3
c = 1       -> Q = 1/2
c = sqrt(2) -> Q = 2/3
c = 2       -> Q = 1
```

Thus the selected-line envelope form is not enough. The radius law is the
load-bearing input.

---

## 6. Relation To The Existing Selected-Line Bridge

The existing bridge runner uses:

```text
fourier_envelopes(delta)
  = 1 + sqrt(2) cos(delta + 2*pi*k/3).
```

That `sqrt(2)` is not a harmless normalization. It is exactly the radius law
`c^2 = 2`.

The bridge remains valuable after that law is retained, because it connects:

```text
selected-line axis slots
<-> Brannen Fourier amplitudes
<-> positive-parent / sqrt(m) support.
```

But it does not derive the radius law from earlier retained assumptions.

---

## 7. Review Consequence

The selected-line axis/Fourier bridge proves:

```text
if the retained selected line and Brannen radius c = sqrt(2) are accepted,
then the axis/Fourier comparison is rigid and reusable.
```

It does not prove:

```text
retained charged-lepton physics -> c = sqrt(2).
```

Nor does a phase theorem prove this, since the phase variable drops out of
`Q(c)` exactly.

So the residual is:

```text
c^2 = 2
equiv kappa = 2
equiv K_TL = 0
```

not the selected-line phase.

---

## 8. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_selected_line_bridge_dependency_no_go.py
```

Result:

```text
PASSED: 12/12
KOIDE_Q_SELECTED_LINE_BRIDGE_DEPENDENCY_NO_GO=TRUE
Q_SELECTED_LINE_AXIS_FOURIER_BRIDGE_CLOSES_Q=FALSE
RESIDUAL_RADIUS_LAW=c^2=2_equiv_kappa=2_equiv_K_TL=0
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used.

---

## 9. Boundary

This note does not demote:

- the selected-line axis/Fourier bridge as support;
- the positive-parent / square-root dictionary;
- the Brannen phase bridge work for `delta`.

It rejects only the stronger claim that the selected-line bridge by itself
derives the charged-lepton `Q` value.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0` or an
  equivalent retained radius/source theorem;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
