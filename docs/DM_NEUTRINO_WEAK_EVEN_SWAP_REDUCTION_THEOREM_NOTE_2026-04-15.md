# DM Neutrino Weak Even Swap-Reduction Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
transfer leg  
**Script:** `scripts/frontier_dm_neutrino_weak_even_swap_reduction_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

Once the odd leg is closed as

- `gamma = c_odd a_sel`
- `c_odd = +1`,

does the exact current weak source carrier already reduce the remaining even
law beyond a generic `2 x 2` matrix

- `[E1, E2]^T = M_even [tau_E, tau_T]^T`?

## Bottom line

Yes.

The exact weak tensor carrier

`K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]]`

is closed under source-column swap and carries no exact `E/T`-distinguishing
datum on the current single-axiom stack.

Therefore any exact linear even-response readout defined only on this current
source carrier must descend to the swap quotient. That forces

`M_even = [[v_1, v_1], [v_2, v_2]] = v_even [1, 1]`

for one real target vector

`v_even = (v_1, v_2)^T`.

Equivalently:

`[E1, E2]^T = v_even (tau_E + tau_T)`.

So the live even-response blocker is no longer a generic `2 x 2` matrix. It is
only the two-real target vector `v_even`.

## Exact source-side reason

The exact weak carrier is the bilinear support object

`K_R(q) = [1, delta_A1(q)]^T [u_E(q), u_T(q)]`.

Its column swap is internal:

`K_R(q) P_ET = K_R(delta_A1(q), u_T(q), u_E(q))`

with

`P_ET = [[0,1],[1,0]]`.

So the exact current source family is closed under `E/T` exchange.

If the even-response readout is exact and built only from this current source
carrier, then it cannot depend on a column label that the current exact source
family itself does not distinguish. Therefore it must satisfy

`M_even = M_even P_ET`.

Solving this fixed-point condition gives exactly

`M_even = [[v_1, v_1], [v_2, v_2]]`.

## Equivalent factorization

The antisymmetric source mode

`tau_- = tau_E - tau_T`

lies in the exact kernel:

`M_even [1,-1]^T = 0`.

So only the symmetric source combination survives:

`tau_+ = tau_E + tau_T`.

Then the exact current even law is simply

`[E1, E2]^T = v_even tau_+`.

This reduces the remaining coefficient problem from four even coefficients to
two.

## Why this does not contradict the old Route-2 staging tools

The old two-channel source-side objects

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`
- `Xi_R^(0) = d Theta_R^(0) / d delta_A1`

do distinguish `E` and `T`.

But both are already recorded as **bounded**, not exact.

So they do not yet supply an exact single-axiom `E/T`-distinguishing readout.
They remain staging tools, not theorem-grade coefficient laws.

## What this closes

This closes the strongest remaining overstatement about the even leg.

The branch can no longer honestly say only:

- “the odd leg is closed but the even leg is still a generic `2 x 2` matrix”

The sharper statement is:

- the current exact source carrier already forces the even map to factor
  through the symmetric source combination
- so the live even-response blocker is only the target vector `v_even`

## What this does not close

This note does **not** derive:

- the value of `v_1`
- the value of `v_2`
- a new exact two-channel readout that would break the swap quotient

So the even leg is still open, but it is now a two-real problem, not a
four-real one.

## Benchmark consequence

This sharpening does **not** change the current benchmark:

- `eta = 1.81e-10`
- `eta / eta_obs ~= 0.30`

The benchmark remains bounded because `v_even` is still not fixed, even though
the odd normalization is now closed and the even transfer shape is reduced.

## Command

```bash
python3 scripts/frontier_dm_neutrino_weak_even_swap_reduction_theorem.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [s3_time_bilinear_tensor_primitive_note](S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md)
- [s3_time_tensor_primitive_prototype_note](S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md)
- [s3_time_constructed_support_tensor_primitive_note](S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md)
