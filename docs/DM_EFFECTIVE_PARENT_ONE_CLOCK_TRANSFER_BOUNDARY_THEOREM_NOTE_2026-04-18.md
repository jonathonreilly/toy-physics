# DM Effective Parent One-Clock Transfer Boundary Theorem Note

**Date:** 2026-04-18  
**Status:** exact retained one-clock transfer law on the enlarged slice space;
exact positive-ready boundary for a genuine gauge-only effective parent; the
script includes a toy witness showing why determinant positivity and temporal
nearest-neighbor locality do not by themselves force scalar edge factorization  
**Script:** `scripts/DM_EFFECTIVE_PARENT_one_clock_transfer_boundary_2026_04_18.py`

## Question

On the retained Wilson-plus-staggered surface, can the determinant-dressed
effective action

`S_eff[U] = S_Wilson[U] - log det(D[U] + m)`

already be treated as carrying the same kind of exact one-clock parent as the
pure-gauge plaquette lane?

## Bottom line

Not yet at the gauge-only parent level.

What *is* derivable exactly on the current stack is stronger than the old
audit boundary in one direction and still limited in another:

1. the full retained Wilson-plus-staggered partition has an exact one-clock
   transfer law on an **enlarged graded slice space** because both the Wilson
   gauge action and the staggered fermion action are nearest-neighbor in
   derived time;
2. but a genuine **gauge-only** effective parent for `S_eff` would require one
   further theorem not currently present on `main`:

   > an exact edge-local factorization / bosonic compression law for the
   > determinant dressing, equivalently a theorem that the fermion contribution
   > collapses from the enlarged slice-space transfer object to a positive
   > scalar one-step kernel on the gauge slice space alone.

So the strongest honest conclusion is a **positive-ready boundary theorem**:

- exact retained one-clock parent exists on the enlarged graded space,
- exact gauge-only effective parent is still open,
- the missing theorem is now isolated sharply.

## Local input stack used here

From [STRONG_CP_THETA_ZERO_NOTE.md](./STRONG_CP_THETA_ZERO_NOTE.md):

- the retained partition is
  `Z = integral DU det(D[U] + m) e^(-S_Wilson[U])`;
- on the retained action surface `det(D[U] + m) > 0` for real `m > 0`;
- therefore `S_eff[U] = S_Wilson[U] - log det(D[U] + m)` is real.

From [GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md):

- the pure-gauge Wilson partition already has one exact one-clock transfer
  law
  `Z_(L_s,L_t)(beta) = Tr[T_(L_s,beta)^(L_t)]`
  on the gauge-invariant spatial Hilbert space.

From [DM_WILSON_PARENT_CORRECTNESS_AUDIT_NOTE_2026-04-18.md](./DM_WILSON_PARENT_CORRECTNESS_AUDIT_NOTE_2026-04-18.md):

- the repo did **not** yet have a theorem identifying the determinant-dressed
  retained partition with an exact one-clock effective parent;
- the positive route left open there was precisely this effective-parent lane.

## Setup

Write the finite retained action on an `L_s^3 x L_t` lattice as a sum over
derived-time slices:

`S_ret = sum_t [ S_g^sp(U_t) + S_g^mix(U_(t+1), U_t) + S_f(U_(t+1), U_t; chi_(t+1), chi_t, bar chi_(t+1), bar chi_t) ]`

where:

- `U_t` denotes the spatial gauge links on slice `t`;
- `S_g^sp` is the purely spatial Wilson half-slice contribution;
- `S_g^mix` is the mixed plaquette contribution between slices `t` and `t+1`;
- `S_f` is the staggered fermion mass-plus-hopping bilinear, which is local in
  the spatial slice and nearest-neighbor in derived time.

Because the staggered action is bilinear, each slice carries a finite
fermionic mode space `V_slice`, hence a finite fermionic Fock / exterior space
`F_slice = Lambda(V_slice)`.

## Theorem 1: exact retained one-clock transfer law on the enlarged graded slice space

On every finite retained Wilson-plus-staggered `L_s^3 x L_t` surface with
periodic gauge boundary conditions and temporal APBC on the fermions, there is
one exact one-step operator

`T_ret`

acting on

`H_slice^gauge tensor F_slice`

such that the full retained partition satisfies

`Z_ret = STr[(T_ret)^(L_t)]`.

Here:

- the gauge factor of `T_ret` is the exact Wilson one-clock kernel coming from
  `S_g^sp + S_g^mix`;
- the fermion factor of `T_ret` is the exact finite-dimensional Gaussian
  bilinear evolution operator induced by `S_f`;
- the APBC are carried by the graded trace / supertrace.

### Reason

This is a direct locality statement.

The gauge action already factorizes one step at a time on the accepted `3+1`
surface. The staggered fermion action also couples only neighboring time
slices, so after slicing in derived time the full Boltzmann factor is a cyclic
product of one-step local kernels. Finite-dimensional Berezin / Fock
identification turns each bilinear one-step fermion factor into a linear map
on `F_slice`. Therefore the entire retained partition is exactly one graded
one-clock transfer trace.

So the repo is now past the weaker audit slogan "no one-clock parent at all."
The honest stronger statement is:

> there is an exact one-clock retained parent, but it still lives on the
> enlarged gauge-plus-fermion slice space.

## Theorem 2: exact boundary for a genuine gauge-only effective parent

Assume we want more than the enlarged graded parent.

Assume there exists an **action-derived gauge-only one-clock effective parent**
`T_eff` on the gauge slice Hilbert space alone, with scalar kernel

`K_eff(U_(t+1), U_t)`,

whose trace expansion reproduces the determinant-dressed retained partition
using the same exact slice grammar:

`Z_ret = Tr[(T_eff)^(L_t)]`

with no hidden auxiliary memory beyond the gauge slice itself.

Then the fermion determinant must admit an exact edge-local factorization:

`det(D[U] + m) = C_(L_t) prod_t Q(U_(t+1), U_t)`

for some positive scalar one-step dressing `Q`, equivalently

`-log det(D[U] + m) = c_(L_t) + sum_t phi(U_(t+1), U_t)`.

### Reason

Expanding the gauge-only trace of `T_eff^(L_t)` over slice histories produces a
cyclic path weight that is, by construction, a product of scalar one-step
kernels.

But the pure-gauge Wilson part already factorizes exactly into the product of
its one-step gauge kernels. So if the *same action-derived* history weight is
to be reproduced without extra auxiliary memory, the residual determinant
dressing must also factor edge-by-edge into a scalar one-step product.

That factorization is therefore **necessary** for a genuine gauge-only
effective parent on the present slice space.

## Corollary 1: the missing theorem is now sharp

The current missing theorem is not "some parent-like object somewhere."

It is exactly one of the following equivalent collapse statements:

1. **Edge-local logarithmic factorization**

   `-log det(D[U] + m) = c_(L_t) + sum_t phi(U_(t+1), U_t)`;

2. **Scalar determinant dressing**

   `det(D[U] + m) = C_(L_t) prod_t Q(U_(t+1), U_t)`;

3. **Bosonic compression of the graded parent**

   the exact enlarged one-clock operator `T_ret` compresses to a positive
   scalar kernel on the gauge slice Hilbert space with no retained auxiliary
   memory.

Any one of these would close the effective-parent route in the sense needed
for the DM Wilson-parent program.

## Corollary 2: what the strong-CP closure does and does not give

The strong-CP note gives exact reality and positivity of the determinant on
the retained surface. That is enough to prove:

- no strong CP phase survives,
- the determinant-dressed action is real,
- the retained measure is positive.

It is **not** enough by itself to prove:

- edge-local factorization of `log det(D[U] + m)`,
- scalar one-step determinant dressing,
- or bosonic compression from the enlarged graded parent to a gauge-only
  transfer kernel.

So positivity should not be confused with one-step scalarizability.

## Witness-only packet in the script

The companion script includes one exact toy witness with three derived-time
slices and one fermionic mode per slice:

`M_cyc = [[m, r_0, s_2], [s_0, m, r_1], [r_2, s_1, m]]`.

For that toy cyclic nearest-neighbor fermion system:

1. the determinant is exactly

   `det(M_cyc) = m^3 - m sum_t r_t s_t + r_0 r_1 r_2 + s_0 s_1 s_2`;

2. the same determinant has an exact one-clock transfer representation

   `det(M_cyc) = Tr[T_2 T_1 T_0]`

   on a four-state auxiliary space with

   `T_t = diag([[m, -r_t s_t], [1, 0]], [r_t], [s_t])`;

3. but the mixed third edge-difference of `log det(M_cyc)` is nonzero on a
   positive sample cube, so `log det(M_cyc)` is **not** edge-additive there.

That witness is not a proof that the retained staggered determinant behaves
identically. It is included for one narrower reason:

> it shows why temporal nearest-neighbor locality plus global positivity do
> not, by themselves, force scalar edge factorization of the determinant
> dressing.

So the missing collapse theorem above is real, not just semantic.

## Exact derived content vs witness-only content

### Exact derived content

1. the retained Wilson-plus-staggered partition has an exact one-clock
   transfer law on the enlarged gauge-plus-fermion slice space;
2. any action-derived gauge-only one-clock effective parent on the present
   slice space requires exact scalar edge factorization of the determinant
   dressing;
3. the current stack has not yet proved that factorization, so the effective
   parent route remains open precisely at that bosonic-compression step.

### Witness-only content

1. the script's `3`-slice toy cyclic fermion model;
2. the explicit `4 x 4` auxiliary transfer matrices used there;
3. the nonzero mixed third edge-difference and least-squares non-factorization
   audit on that toy family.

Those witness items justify the sharpness of the boundary, but they are not
the theorem-grade proof for the retained lattice itself.

## What this closes

- one exact upgrade of the old audit: the retained stack does admit an exact
  one-clock parent, but on the enlarged graded slice space
- one exact identification of the missing theorem for a genuine gauge-only
  effective parent
- one positive-ready reformulation of the effective-parent route as a concrete
  bosonic-compression / determinant-factorization theorem

## What this does not close

- an exact gauge-only one-clock effective parent for `S_eff`
- an exact edge-local factorization theorem for `log det(D[U] + m)`
- a Wilson-native charged descendant `I_e / P_e / dW_e^H`
- the DM selector gate
