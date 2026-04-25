# Koide Q Effective-Action Tilt No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the normalized
effective-action route but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_effective_action_tilt_no_go.py`

---

## 1. Theorem Attempt

The strongest remaining second-order `Q` route is:

> the exact normalized effective action on the first-live carrier is convex and
> has a unique minimum at the identity, so perhaps the effective-action
> principle itself forces the Koide point.

The executable result is negative.

---

## 2. Source-Free Support

On the normalized carrier

```text
Y = diag(y, 2-y),
```

the exact source-free effective action is

```text
S_0(y) = -log(y(2-y)).
```

It has a unique interior stationary point:

```text
y = 1,
```

and is strictly convex:

```text
d^2 S_0 / dy^2 = 1/y^2 + 1/(2-y)^2 > 0.
```

Thus the source-free route correctly lands at:

```text
Y = I_2
<=> E_+ = E_perp
<=> K_TL = 0
<=> Q = 2/3.
```

This remains valid support.

---

## 3. Tilt Family

The retained source-coupled effective-action grammar also allows a traceless
linear source:

```text
K = tau * diag(+1, -1).
```

On the trace-2 slice this gives the tilted family

```text
S_tau(y) = S_0(y) + 2 tau (y-1).
```

The linear tilt preserves strict convexity. Its stationarity equation is:

```text
tau = (1-y)/(y(2-y)) = K_TL(y).
```

Therefore every interior point `y0 in (0,2)` is the unique minimum of the
same exact effective action with a matching admissible traceless source:

```text
tau(y0) = (1-y0)/(y0(2-y0)).
```

---

## 4. Counterexample

The runner checks the exact off-center point:

```text
y = 4/5.
```

Then:

```text
tau = K_TL = 5/24,
Q = 5/6 != 2/3.
```

The tilted action is still strictly convex and has that point as its unique
minimum. So convexity and effective-action naturality do not select the
Koide leaf by themselves.

---

## 5. Review Consequence

The normalized effective-action route closes `Q` only after imposing:

```text
tau = K_TL = 0.
```

But that is exactly the already named missing primitive. The route proves:

```text
source-free effective action -> Koide.
```

It does not prove:

```text
retained charged-lepton physics -> source-free effective action.
```

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_effective_action_tilt_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_EFFECTIVE_ACTION_TILT_NO_GO=TRUE
Q_EFFECTIVE_ACTION_CONVEXITY_CLOSES_Q=FALSE
RESIDUAL_SCALAR=tau=K_TL
```

---

## 7. Boundary

This note does not demote the exact normalized effective action. It demotes
only the stronger claim that effective-action convexity alone derives the
physical no-traceless-source law.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0`;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
