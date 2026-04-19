# Quark Route-2 Exact Readout Map

**Date:** 2026-04-19  
**Status:** exact carrier/readout reduction plus exact missing-map obstruction  
**Primary runner:** `scripts/frontier_quark_route2_exact_readout_map.py`

## Safe statement

The current branch now separates the Route-2 readout problem cleanly.

The exact bilinear carrier `K_R` and exact endpoint columns already force the
restricted bright readout class into the channelwise form

```text
gamma_E = alpha_E u_E + beta_E delta_A1 u_E
gamma_T = alpha_T u_T + beta_T delta_A1 u_T.
```

That exact reduction is real progress. But the current exact stack still does
**not** derive the endpoint ratio chain

```text
{5/6, -2, -8/9} -> 15/8 -> r_E = 21/4 -> D_E = 21/8.
```

Equivalently, it still does not derive the exact dimensionless readout triple

```text
(beta_T / alpha_T, alpha_T / alpha_E, beta_E / alpha_E)
= (-1, -2, 21/4).
```

So the honest endpoint is:

- exact carrier/readout reduction on the restricted class,
- exact endpoint algebra for the ratio chain,
- and an exact missing-map obstruction rather than an exact readout theorem.

## 1. Exact carrier/readout setup

On the live support surface:

```text
delta_A1(e0)        = 1/6
delta_A1(s/sqrt(6)) = 0
```

and the exact carrier columns are

```text
E-shell  = (1, 0, 0,   0)
E-center = (1, 0, 1/6, 0)
T-shell  = (0, 1, 0,   0)
T-center = (0, 1, 0, 1/6).
```

Those four columns span a direct sum of disjoint `E` and `T` endpoint
subspaces. So any admissible bright-preserving linear readout on this
restricted class must reduce to one `E` map and one `T` map:

```text
P_R = [[alpha_E, 0, beta_E, 0],
       [0, alpha_T, 0, beta_T]].
```

The runner then recomputes the live bounded endpoint values directly from the
current modules and confirms that the endpoint-fixed map reproduces them
exactly on this class.

## 2. Exact endpoint algebra

Once the readout is reduced to `P_R`, the endpoint ratios are algebraic:

```text
q_T   := gamma_T(center) / gamma_T(shell) = 1 + (beta_T / alpha_T) / 6
q_E   := gamma_E(center) / gamma_E(shell) = 1 + (beta_E / alpha_E) / 6
s_TE  := gamma_T(shell) / gamma_E(shell)  = alpha_T / alpha_E
c_TE  := gamma_T(center) / gamma_E(center) = s_TE * q_T / q_E.
```

So the target ratio chain

```text
q_T = 5/6,  s_TE = -2,  c_TE = -8/9
```

is exactly equivalent to

```text
beta_T / alpha_T = -1
alpha_T / alpha_E = -2
beta_E / alpha_E = 21/4.
```

This is the key compression of the theorem target.

## 3. Theorem attempt on the live surface

The live endpoint-fixed readout is

```text
beta_T / alpha_T = -1.000030814262
alpha_T / alpha_E = -2.005382749600
beta_E / alpha_E =  5.257476782081
```

and therefore

```text
q_T  = 0.833328197623
s_TE = -2.005382749600
c_TE = -0.890683778231.
```

So the exact readout theorem does **not** land on the current surface.

The important point is that this is no longer a vague “bad fit.” The branch
now knows precisely what theorem would be needed, and exactly which readout
ratios would have to be proved.

## 4. Smallest exact obstruction

The new runner then proves the smallest exact obstruction.

If the two `T`-side candidates are granted exactly,

```text
beta_T / alpha_T = -1
alpha_T / alpha_E = -2,
```

then the entire remaining readout theorem collapses to one exact map entry:

```text
beta_E / alpha_E = 21/4.
```

This is seen directly on the reduced exact family

```text
P(rho_E) = [[1, 0, rho_E, 0],
            [0, -2, 0, 2]].
```

All such maps agree on the shell `E` normalization, but the center `E` lift is

```text
1 + rho_E / 6.
```

So `rho_E = 0` and `rho_E = 21/4` are both exact admissible maps on the
restricted carrier class, but they produce different center `E` readouts.

That is the theorem-grade obstruction:

> the exact carrier and exact endpoint algebra do not yet fix the readout map
> uniquely; the irreducible missing map entry is the `E`-channel ratio
> `beta_E / alpha_E`.

## Honest endpoint

The current Route-2 readout status is now:

- exact bilinear carrier `K_R`: already present,
- exact restricted readout reduction: closed,
- exact endpoint ratio theorem: not derived,
- smallest exact missing map entry: `beta_E / alpha_E = 21/4` after the
  `T`-side candidates are granted.

That is the right theorem endpoint for this block.

## Validation

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_readout_map.py
```

Current expected result on this branch:

- `frontier_quark_route2_exact_readout_map.py`: `PASS=11 FAIL=0`
