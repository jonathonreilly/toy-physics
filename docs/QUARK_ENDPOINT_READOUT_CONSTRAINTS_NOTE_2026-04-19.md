# Quark Endpoint Readout Constraints

**Date:** 2026-04-19  
**Status:** exact endpoint-fixation theorem plus bounded ratio/no-go audit on
the live forward quark worktree  
**Primary runner:** `scripts/frontier_quark_endpoint_readout_constraints.py`

## Safe statement

The current Route-2 support notes already fix the affine readout coefficients
`(a_E, b_E, a_T, b_T)` exactly once the two live endpoint values

- `gamma(center)`
- `gamma(shell)`

are supplied.

But the same notes still do **not** derive an exact coefficient theorem.

The honest endpoint on the live forward branch is therefore:

- **exact endpoint fixation** of the current affine readout,
- **exact reduction** of the remaining structural question to the channel ratios
  `r_E = b_E / a_E` and `r_T = b_T / a_T`,
- **bounded live relations** such as
  - `b_T / a_T ~ -1`,
  - `a_T / a_E ~ -2.005`,
  - `|b_E / b_T| ~ 2.6216`,
- and an **exact note-level no-go** against promoting the current `E/T`
  readout to a theorem-grade coefficient law.

This is narrower and safer than the nearby quark endpoint-bridge lane. It does
not try to derive a quark amplitude law. It only formalizes what the current
Route-2 endpoint readout already fixes, and where the current notes still stop.

## Exact endpoint fixation

The runner recomputes the live support-tensor readout directly from the current
modules, not copied constants.

The exact support endpoints remain:

```text
delta_A1(e0)        = 1/6
delta_A1(s/sqrt(6)) = 0
endpoint gap        = 1/6
```

So for the bounded affine readout

```text
gamma_E(delta_A1) = a_E + b_E delta_A1
gamma_T(delta_A1) = a_T + b_T delta_A1
```

the coefficients are fixed exactly by the endpoint values:

```text
a_E = gamma_E(shell)
a_T = gamma_T(shell)
b_E = [gamma_E(center) - gamma_E(shell)] / (1/6)
b_T = [gamma_T(center) - gamma_T(shell)] / (1/6)
```

On the live forward branch this gives

```text
gamma_E(delta_A1) = -2.010572657265e-04 + (-1.057053906426e-03) delta_A1
gamma_T(delta_A1) = +4.031967723697e-04 + (-4.032091965809e-04) delta_A1
```

That is the exact positive part of this lane: once the current endpoint data
are admitted, the affine coefficients are no longer free.

## Exact reduction to channel ratios

The live forward stack already contains two exact ingredients that sharpen the
remaining coefficient question further:

1. [ONE_PARAMETER_REDUCED_SHELL_LAW_NOTE.md](./ONE_PARAMETER_REDUCED_SHELL_LAW_NOTE.md)
   records the exact common denominator law

   ```text
   A_aniso = c_aniso * Q
   ```

2. [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
   records that on the aligned bright directions the carrier columns are
   channel-blind:

   ```text
   E_x  -> (1, delta_A1)
   T1x  -> (1, delta_A1)
   ```

So the structural readout question is no longer an arbitrary four-coefficient
problem. It reduces exactly to the two channel ratios

```text
r_E = b_E / a_E
r_T = b_T / a_T
```

with the shell amplitudes `a_E`, `a_T` already fixed by the endpoint values.

## Bounded live relations

The runner then records the bounded live coefficient pattern on the same
surface:

```text
r_E         = +5.257476782081
r_T         = -1.000030814263
a_T / a_E   = -2.005382749600
|b_E / b_T| =  2.621601678210
gamma_T(center)/gamma_T(shell) = 0.833328197623
```

These are useful live constraints, but they remain bounded observations rather
than theorem-grade identities.

The strongest one is:

```text
r_T = b_T / a_T ~ -1
```

So the `T` channel is already effectively

```text
gamma_T(delta_A1) ~ a_T * (1 - delta_A1)
```

and therefore at the center endpoint

```text
gamma_T(e0) / gamma_T(s/sqrt(6)) ~ 1 - 1/6 = 5/6.
```

while the shell/intercept and slope ratios remain visibly nontrivial:

- `r_E = b_E / a_E ~ 5.25748`
- `a_T / a_E ~ -2.005`
- `|b_E / b_T| ~ 2.6216`

So the coefficient lane is already sharply structured, and the remaining
unresolved primitive is now most naturally the `E`-channel readout ratio
`r_E`, not the common denominator and not the `T`-channel shape.

## Exact no-go from the current notes

The runner then checks the current Route-2 note stack directly.

Three facts matter:

1. [DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md)
   explicitly says the old two-channel objects
   `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))` and
   `Xi_R^(0) = d Theta_R^(0) / d delta_A1`
   still **distinguish `E` and `T`**, but are **bounded, not exact**.
2. [S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md](./S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md)
   still lists **“an exact endpoint coefficient theorem”** under what the note
   does not close.
3. [S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md](./S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md)
   keeps the same endpoint theorem open for the constructed `Xi_R^(0)` object.

So the safe no-go statement is exact:

> the current notes do not support an exact coefficient theorem for
> `(a_E, b_E, a_T, b_T)`.

They support only:

- exact endpoint fixation of the current bounded affine readout,
- exact reduction to the channel ratios `r_E`, `r_T`,
- bounded `E/T`-distinguishing staging objects,
- and an open endpoint-coefficient theorem.

## What this closes

This note closes the ambiguity in the readout-coefficient lane itself.

The branch can now say precisely:

- the affine readout coefficients are fixed exactly by the two live endpoint
  values,
- the exact support stack reduces the structural question to the channel ratios
  `r_E`, `r_T`,
- the live coefficient ratios show a stable bounded pattern,
- the `T` channel is already effectively `1 - delta_A1` on the live surface,
- but the current notes still do not promote that pattern to an exact theorem,
  and the unresolved primitive is still the `E`-channel ratio.

That is the right disciplined endpoint for this coefficient lane.

## What this does not close

This note does **not** prove:

1. an exact `E/T`-symmetric coefficient reduction such as
   `a_E = a_T`, `b_E = b_T`;
2. an exact tensor dynamics identification of the readout;
3. a quark amplitude law downstream of these coefficients;
4. a promoted retained quark closure theorem.

## Validation

Run:

```bash
python3 scripts/frontier_quark_endpoint_readout_constraints.py
```

Current expected result on this branch:

- `frontier_quark_endpoint_readout_constraints.py`: `PASS=14 FAIL=0`
