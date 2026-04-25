# Koide Q Information-Measure Midpoint No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects the claim that the
canonical logdet/Fisher information measure on the normalized second-order
carrier derives the charged-lepton traceless source law.
**Primary runner:** `scripts/frontier_koide_q_information_measure_midpoint_no_go.py`

---

## 1. Theorem Attempt

The strongest information-geometric route is:

> the retained normalized two-block carrier has a canonical logdet/Fisher
> measure, and that measure might select the block-democratic midpoint
> `Y = I_2`, forcing `K_TL = 0` and hence `Q = 2/3`.

The executable result is negative. The midpoint is symmetric and stationary,
but selection depends on an extra measure-power convention.

---

## 2. Exact Carrier Calculation

On the trace-normalized carrier

```text
Y = diag(y, 2-y), 0 < y < 2,
```

the induced logdet/Fisher metric is:

```text
g(y) = 1/y^2 + 1/(2-y)^2.
```

The midpoint is stationary:

```text
g'(1) = 0,
```

but it is an interior minimum:

```text
g''(1) = 12 > 0.
```

The density diverges at both carrier boundaries. Thus the direct
Fisher/Jeffreys density does not select the source-free midpoint as a maximum
or unique physical state.

---

## 3. Measure-Power Freedom

A symmetric measure-power family has the form:

```text
mu_p(y) = (y(2-y))^p.
```

For every real `p`,

```text
d log(mu_p)/dy |_{y=1} = 0,
```

so block exchange alone gives only stationarity. The local selection is set by:

```text
d^2 log(mu_p)/dy^2 |_{y=1} = -2p.
```

Therefore:

```text
p > 0  -> midpoint maximum
p = 0  -> flat
p < 0  -> midpoint minimum / boundary preference
```

Choosing the power that favors the midpoint is an additional prior. It is not
derived by the retained charged-lepton `Cl(3)/Z^3` structure.

---

## 4. Source-Law Consequence

For the normalized two-block carrier, the traceless source is:

```text
K_TL(y) = (1-y)/(y(2-y)).
```

It vanishes exactly at:

```text
y = 1.
```

But the same information geometry allows nearby normalized points. The runner
checks:

```text
y = 4/5 -> K_TL = 5/24 != 0.
```

Thus information geometry by itself does not derive the no-traceless-source
law. It supplies a symmetric landscape whose physical selector remains
undetermined.

---

## 5. Hostile Review

This route does not import mass-table data, observational pins, `Q = 2/3`,
`P_Q = 1/2`, `delta = 2/9`, or an endpoint equality. Its failure is internal:
to get the Koide leaf one must choose a measure convention that favors
`Y = I_2`.

That convention would be a renamed selector primitive unless it is separately
derived from retained charged-lepton structure.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_information_measure_midpoint_no_go.py
```

Result:

```text
PASS=12 FAIL=0
INFORMATION_MEASURE_FORCES_K_TL=FALSE
KOIDE_Q_INFORMATION_MEASURE_MIDPOINT_CLOSES_Q=FALSE
RESIDUAL_SCALAR=measure_power_p_selecting_midpoint
```

---

## 7. Boundary

This note does not reject information geometry as support. It rejects only the
stronger claim that the canonical information measure already derives:

```text
K_TL = 0.
```

The residual primitive remains:

```text
derive the physical measure-power/selector law, or derive K_TL = 0 directly.
```
