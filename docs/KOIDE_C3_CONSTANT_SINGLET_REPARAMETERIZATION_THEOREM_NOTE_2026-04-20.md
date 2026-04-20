# Koide `C_3` Constant-Singlet Reparameterization Theorem

**Date:** 2026-04-20  
**Status:** exact sharpening of the fixed-coupling singlet-Schur route on the
selected scalar slice
**Runner:** `scripts/frontier_koide_c3_constant_singlet_reparametrization_theorem.py`

## Question

The companion singlet-extension reduction theorem reduced the open `4 x 4`
route to one scalar Schur law

```text
K_eff(m) = K_sel(m) - lambda(m) J,
```

and, in the fixed-coupling subclass, to one constant `lambda`.

That still leaves an honest scientific question:

> if `lambda` is constant, does that actually select the physical Koide point
> `m_*`, or does it merely rename the same scalar gap?

## Bottom line

It renames the gap.

On the physical first branch, the stationarity equation of the fixed-coupling
potential can be solved exactly for `lambda` as a function of the selected-line
coordinate `m`:

```text
lambda_±(m)
  = m/3 + 1/3
    ± sqrt(-144 m - 48 sqrt(6) - 69 + 96 sqrt(2)) / 18.
```

So the fixed-coupling singlet route does **not** isolate one point. Instead:

1. real constant-coupling stationary points exist for the whole interval
   ```text
   m in [m_pos, m_disc],
   m_disc = (96 sqrt(2) - 48 sqrt(6) - 69)/144 ~= -0.352854206012;
   ```
2. on the lower subinterval `(m_pos, m_V)` there is exactly one positive root
   `lambda_+(m)`;
3. at
   ```text
   m_V = -3 + sqrt(-48 sqrt(6) + 96 sqrt(2) + 219)/6 ~= -0.433176442380,
   ```
   the lower branch hits `lambda_-(m_V) = 0`, which is exactly the old
   zero-coupling selected-slice minimum;
4. on the upper subinterval `(m_V, m_disc]` there are **two** positive
   constant-coupling roots.

So fixed-coupling singlet dressing does not close Koide `Q = 2/3`. It gives an
exact reparameterization of a continuum of first-branch stationary points.

## Input stack

This note sharpens:

1. [KOIDE_Z3_SCALAR_POTENTIAL_SUPPORT_NOTE_2026-04-19.md](./KOIDE_Z3_SCALAR_POTENTIAL_SUPPORT_NOTE_2026-04-19.md)
2. [KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md](./KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md)
3. [KOIDE_C3_SINGLET_EXTENSION_REDUCTION_THEOREM_NOTE_2026-04-20.md](./KOIDE_C3_SINGLET_EXTENSION_REDUCTION_THEOREM_NOTE_2026-04-20.md)

## 1. Exact stationary roots

For constant `lambda`, the selected-slice potential from the companion theorem
obeys

```text
dV_lambda/dm
  = 9 lambda^2 / 2
  - 3 (m+1) lambda
  + m^2 / 2
  + 3m
  - 4 sqrt(2)/3
  + 35/24
  + 2 sqrt(6)/3.
```

Solving `dV_lambda/dm = 0` for `lambda` gives the exact pair

```text
lambda_±(m)
  = m/3 + 1/3
    ± sqrt(Delta(m)) / 18,
Delta(m) = -144 m - 48 sqrt(6) - 69 + 96 sqrt(2).
```

The fixed-coupling route therefore remains one-scalar. But now that scalar is
explicitly soluble on the selected line.

## 2. Accessible branch interval

Real roots require `Delta(m) >= 0`, so the constant-coupling route reaches the
first branch only on

```text
m <= m_disc,
m_disc = (96 sqrt(2) - 48 sqrt(6) - 69)/144 ~= -0.352854206012.
```

Since the unphased first-branch endpoint is

```text
m_0 ~= -0.265815998702,
```

the constant-coupling family does **not** even cover the whole first branch.
It covers only the lower subinterval `[m_pos, m_disc]`, which still contains
the physical point `m_*`.

## 3. The old zero-coupling minimum sits inside the same family

The lower branch satisfies

```text
lambda_-(m_V) = 0
```

at

```text
m_V = -3 + sqrt(-48 sqrt(6) + 96 sqrt(2) + 219)/6 ~= -0.433176442380.
```

That is exactly the original `lambda = 0` selected-slice minimum from the
Z^3 scalar-potential theorem. So the fixed-coupling singlet family does not
replace the old route; it deforms it continuously away from `m_V`.

## 4. One-positive-root and two-positive-root regimes

The runner verifies the following exact branch split:

### 4.1 Lower interval `(m_pos, m_V)`

```text
lambda_-(m) < 0 < lambda_+(m).
```

So here there is exactly one positive constant-coupling singlet value for each
physical first-branch point.

### 4.2 Upper interval `(m_V, m_disc]`

```text
0 < lambda_-(m) < lambda_+(m).
```

So above the old zero-coupling minimum there are **two** positive constant
singlet values producing the same branch point.

This is a stronger underdetermination statement than the companion theorem:
the fixed-coupling route is not just missing a distinguished value. Over part
of the branch it is genuinely two-to-one.

## 5. Reparameterization, not selection

The positive branch `lambda_+(m)` is strictly decreasing across the whole
admissible interval `[m_pos, m_disc]`, while `lambda_-(m)` is strictly
increasing on `[m_V, m_disc]`.

For every such root, the companion stationary point of `V_lambda` lies below
the positivity threshold `m_pos`. Therefore each positive `lambda` root gives
exactly one stationary point on the physical first branch.

That means:

```text
constant-coupling singlet dressing
```

is not a selector theorem. It is an exact reparameterization of a continuum of
branch points.

## 6. Position of the physical point

At the physical Koide point from the actual-route bridge,

```text
delta = 2/9  ->  m_* = -1.160443440065,
```

the positive branch gives

```text
lambda_* = lambda_+(m_*) ~= 0.545625311688,
```

which is exactly the value found in the companion reduction theorem.

But `lambda_*` is an interior value of the decreasing `lambda_+(m)` family:
it sits strictly between the threshold-end value `lambda_+(m_pos)` and the
zero-coupling turning value `lambda_+(m_V)`. So branch geometry and constant
coupling alone do **not** distinguish it.

## 7. Scientific consequence

This is the honest update to the selected-slice singlet route:

- the route is still one-scalar;
- in the fixed-coupling subclass it is now completely explicit;
- but that explicit family does **not** close Koide `Q = 2/3`;
- it shows that the real remaining object is still a microscopic law fixing
  `lambda` itself, equivalently fixing the selected-line scalar `m`.

So the fixed-coupling singlet route is not a hidden closure. It is a sharpened
restatement of the same one-scalar gap.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_c3_constant_singlet_reparametrization_theorem.py
```
