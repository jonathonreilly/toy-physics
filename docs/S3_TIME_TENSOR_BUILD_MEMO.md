# Route 2 Tensor Build Memo

**Status:** unknown (pending author classification)
**Date:** 2026-04-19  
**Scope:** current Route-2 tensor/readout/time stack after the exact bilinear
carrier and the readout/time-coupling theorem block

## Round verdict

The Route-2 tensor carrier is no longer missing.

The current exact stack already contains:

- exact background `PL S^3 x R`
- exact slice generator `Lambda_R`
- exact transfer backbone `T_R = exp(-Lambda_R)`
- exact bilinear carrier `K_R`

The new readout/time block then pins down the remaining gap:

- the readout problem reduces exactly to the channelwise map `P_R`
- the exact endpoint ratio chain still does not derive
- the smallest missing readout entry is the `E`-channel ratio
  `beta_E / alpha_E`
- and without that map entry the branch has only an exact conditional
  readout-to-slice family, not a unique exact time-coupling theorem

## 1. Exact objects already available

### Carrier side

- exact microscopic support carrier
  `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

### Slice side

- exact Schur boundary generator `Lambda_R`
- exact self-adjoint contractive transfer backbone `T_R = exp(-Lambda_R)`

### Kinematics

- exact `PL S^3 x R`

## 2. Exact sub-primitives still missing

### Missing primitive P1: exact readout map

- map `P_R : vec(K_R) -> Theta_R`
- restricted bright form
  `gamma_E = alpha_E u_E + beta_E delta_A1 u_E`
  `gamma_T = alpha_T u_T + beta_T delta_A1 u_T`
- current theorem endpoint:
  exact carrier reduction is closed, exact coefficient theorem is not

### Missing primitive P2: exact readout-to-slice coupling law

- desired unique theorem
  `Xi_R(t ; c) = (P_R c) ⊗ exp(-t Lambda_R) u_*`
- current status:
  exact conditional family exists for any admissible `P_R`, but uniqueness is
  blocked by the unresolved readout map

### Missing primitive P3: final dynamics identification

- identify the exact carrier/readout/coupling package with Einstein/Regge
  tensor dynamics on the current restricted class

## 3. What the new theorem block actually closed

The new block did close several things cleanly:

1. exact reduction of the restricted readout problem to one `E` map and one
   `T` map
2. exact algebraic equivalence between the endpoint ratio chain and the
   dimensionless readout triple
3. exact slice-side semigroup backbone for time coupling
4. exact proof that unresolved readout exactness induces the current
   time-coupling obstruction

That is a real theorem-grade narrowing of the Route-2 target.

## 4. Immediate next theorem

The next theorem should not be “find another tensor primitive.”

It should be:

> derive the `E`-channel readout map entry on the current exact carrier/slice
> stack, or prove a stronger admissibility theorem showing why the current
> stack cannot force it uniquely.

That is now the correct constructive target.
