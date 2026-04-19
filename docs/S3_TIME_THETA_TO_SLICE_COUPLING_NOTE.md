# Route 2 Readout to Slice Coupling

**Date:** 2026-04-19  
**Purpose:** state the current exact status of the Route-2
`Theta_R -> Lambda_R` coupling problem after the exact bilinear carrier and
the new readout/time-coupling theorem block

## Verdict

The current answer is no longer “bounded staging object only.”

The branch now has:

- exact slice backbone `Lambda_R`, `T_R = exp(-Lambda_R)`
- exact bilinear carrier `K_R`
- exact restricted readout reduction to one admissible map `P_R`
- exact conditional coupling family
  `Xi_P(t ; c) = (P_R c) ⊗ exp(-t Lambda_R) u_*`

What it still does **not** have is one unique exact readout-to-slice theorem,
because the readout map itself is not yet derived exactly.

So the honest endpoint is:

> exact conditional coupling family, exact induced obstruction to uniqueness.

## Exact ingredients already available

### Carrier

- `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

### Readout class

- restricted bright form
  `gamma_E = alpha_E u_E + beta_E delta_A1 u_E`
  `gamma_T = alpha_T u_T + beta_T delta_A1 u_T`

### Slice backbone

- exact `Lambda_R`
- exact `T_R = exp(-Lambda_R)`
- exact seed law `V_R(t) = exp(-t Lambda_R) u_*`

## Exact conditional coupling family

Once an admissible readout map `P_R` is chosen, the current branch supports
the exact family

```text
Xi_P(t ; c) = (P_R c) ⊗ V_R(t)
```

for every restricted carrier column `c`.

This is exact because:

1. `c` is exact,
2. `P_R` is algebraic once specified,
3. `V_R(t)` is exact.

So the route does not lack a carrier-to-slice construction anymore.

## Why the unique theorem is still blocked

The readout theorem does not yet derive the endpoint triple

```text
beta_T / alpha_T = -1
alpha_T / alpha_E = -2
beta_E / alpha_E = 21/4.
```

Therefore the readout map remains non-unique even on the restricted class.

The new runner shows this directly:

- distinct exact admissible maps agree at shell normalization,
- but produce different center `E` source factors,
- so they produce different exact spacetime tensors on the same slice
  backbone.

That means the ambiguity is not in `Lambda_R`. It is in the unresolved source
readout map.

## Current blocker

The blocker is now very precise:

> unresolved readout exactness blocks a unique exact `Theta_R -> Lambda_R`
> coupling law on the current carrier.

This is sharper than the older “missing tensor observable” statement, because
the carrier and the slice semigroup are already exact.

## Bottom line

Route 2 now has:

- exact carrier,
- exact slice backbone,
- exact conditional readout-to-slice family,
- no unique exact coupling theorem yet.

The next theorem target is the missing readout map entry, not a new slice law.
