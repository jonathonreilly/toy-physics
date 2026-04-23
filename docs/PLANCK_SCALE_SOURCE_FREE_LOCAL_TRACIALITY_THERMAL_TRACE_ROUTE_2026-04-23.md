# Planck-Scale Source-Free Local Traciality Thermal-Trace Route

**Date:** 2026-04-23  
**Status:** science-only exact reduction / sharp no-go on the thermal-trace KMS route  
**Audit runner:** `scripts/frontier_planck_source_free_local_traciality_thermal_trace_route.py`

## Question

Can the last Planck blocker

`rho_cell = I_16 / 16`

be derived on the primitive time-locked `C^16` cell by a same-surface
thermal-trace / KMS argument?

The intended attraction of this route is clear:

- it lives directly on the primitive cell rather than on the older boundary
  scalar packaging;
- it suggests a source-free state as a canonical thermal state;
- on a finite cell, the infinite-temperature state is exactly tracial.

So the real question is:

> does a primitive-cell thermal/KMS grammar actually force the source-free state
> to be tracial, or does it only repackage the missing premise as a choice of
> generator or temperature?

## Bottom line

It does **not** close the route by itself.

The thermal/KMS route gives an exact criterion:

> on the primitive one-cell algebra `M_16(C)`, a thermal/KMS state is tracial
> if and only if either
> `beta = 0`
> or the primitive generator `H_cell` is scalar:
> `H_cell = lambda I_16`.

So this route sharpens the last blocker, but it does not remove it.

The exact same-surface conclusion is:

- if source-free means **infinite-temperature primitive KMS state**, then
  `rho_cell = I_16 / 16`;
- if source-free means **primitive generator has no nontrivial local splitting**,
  then also `rho_cell = I_16 / 16`;
- without one of those two premises, the thermal route leaves a nontrivial
  family of source-free candidate states and does not close Planck.

So the thermal route is honest but conditional. It does not beat the existing
automorphism/traciality candidate. It translates the last blocker into one of
two sharper forms:

1. **Source-Free Infinite-Temperature Theorem** on the primitive cell, or
2. **Source-Free Scalar-Generator Theorem** on the primitive cell.

## Inputs

This route uses only the direct Planck stack plus thermal-trace inspiration:

- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [PLANCK_SCALE_AXIOM_NATIVE_ROUTE_CHECK_2026-04-23.md](./PLANCK_SCALE_AXIOM_NATIVE_ROUTE_CHECK_2026-04-23.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md)

The gauge-vacuum note is used only as inspiration for the style of reduction:
there the thermal trace works because an exact transfer operator is already
fixed. Here no exact primitive one-cell generator is yet fixed, and that is
exactly why the route does not close automatically.

## Setup

Work on the primitive time-locked one-cell Hilbert carrier

`H_cell = span{|eta> : eta in {0,1}^4} ~= C^16`.

Let

- `A_cell = M_16(C)`,
- `P_eta = |eta><eta|`,
- `P_A = sum_(|eta|=1) P_eta`

be the exact one-step worldtube packet.

The direct counting law is already closed:

`c_cell(rho) = Tr(rho P_A)`.

So this route attacks only `rho`.

## Definition: primitive thermal/KMS family

Let `H_cell` be a self-adjoint primitive one-cell generator and `beta >= 0`.

Define the finite-cell thermal state

`rho_(beta,H) = exp(-beta H_cell) / Tr(exp(-beta H_cell))`.

On a finite-dimensional matrix algebra this is the exact `beta`-KMS state for
the one-parameter dynamics

`alpha_t(A) = exp(i t H_cell) A exp(-i t H_cell)`.

The thermal question is therefore:

> when does `rho_(beta,H)` equal the tracial state `I_16 / 16`?

## Theorem 1: finite-cell KMS states are Gibbs states

On `A_cell = M_16(C)`, every `beta`-KMS state for the inner dynamics generated
by `H_cell` is exactly the Gibbs state

`rho_(beta,H) = exp(-beta H_cell) / Z_(beta,H)`,

with

`Z_(beta,H) = Tr(exp(-beta H_cell))`.

So the thermal route is completely explicit.

## Theorem 2: exact traciality criterion for primitive thermal states

The finite-cell thermal state is tracial,

`rho_(beta,H) = I_16 / 16`,

if and only if

`beta (H_cell - lambda I_16) = 0`

for some scalar `lambda`.

Equivalently:

- either `beta = 0`, or
- `H_cell` is scalar.

### Proof

If `beta = 0`, then

`exp(-beta H_cell) = I_16`,

so immediately

`rho_(0,H) = I_16 / 16`.

If `H_cell = lambda I_16`, then

`exp(-beta H_cell) = exp(-beta lambda) I_16`,

and normalization again gives `I_16 / 16`.

Conversely, if

`exp(-beta H_cell) / Tr(exp(-beta H_cell)) = I_16 / 16`,

then

`exp(-beta H_cell)` must be proportional to the identity. Taking logarithms on
the positive spectrum gives `beta H_cell = beta lambda I_16`. Hence either
`beta = 0` or `H_cell` is scalar.

That is the exact criterion.

## Corollary 1: exact Planck closure under a primitive thermal source-free theorem

If one proves either of the following same-surface statements:

1. **source-free primitive state is the `beta = 0` KMS state**, or
2. **source-free primitive generator is scalar**,

then

`rho_cell = I_16 / 16`.

Since the counting law is already closed,

`c_cell = Tr(rho_cell P_A) = Tr((I_16 / 16) P_A) = 4/16 = 1/4`,

and the direct Planck chain closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

So the thermal route does isolate a clean one-shot closure condition.

## Theorem 3: the thermal route inherits the primitive-generator freedom

Without a theorem fixing `beta = 0` or forcing `H_cell` to be scalar, the
thermal route does not select the tracial state.

More concretely, for any diagonal residual-`S_3` orbit Hamiltonian

`H_cell = sum_(t=0)^1 sum_(w=0)^3 h_(t,w) Pi_(t,w)`,

the thermal state is

`rho_(beta,H)
 = (1 / Z) sum_(t,w) exp(-beta h_(t,w)) Pi_(t,w)`,

with

`Z = sum_(t,w) binom(3,w) exp(-beta h_(t,w))`.

So the thermal route stays inside the same eight-orbit grammar isolated by the
source-free underdetermination note. It does not collapse that family unless
the primitive generator theorem does extra work.

## Two explicit thermal witnesses

The failure is not abstract.

### Witness A: zero generator

Take

`H_0 = 0`.

Then for any `beta`,

`rho_(beta,H_0) = I_16 / 16`,

so

`Tr(rho_(beta,H_0) P_A) = 1/4`.

### Witness B: packet-energy tilt

Take

`H_A = P_A`

and `beta = log 2`.

Then

`exp(-beta H_A) = (1/2) P_A + (I_16 - P_A)`,

and the normalized thermal state gives

`Tr(rho_(log 2,H_A) P_A)
 = (4 * 1/2) / (12 + 4 * 1/2)
 = 2 / 14
 = 1/7`.

So even within the same-surface primitive thermal family, the packet
coefficient can be `1/4` or `1/7` depending on the unfixed primitive
generator.

That is an exact obstruction to claiming closure from thermal/KMS grammar
alone.

## Why this route is still useful

This route does sharpen the science in an honest way.

It proves that the last blocker is **not** “find a clever new packet
normalization.” It is one of these precise primitive statements:

- source-free means infinite-temperature on the primitive cell;
- or source-free means no nontrivial primitive energetic splitting.

That is a real improvement in conceptual precision.

## Why this route does not beat the direct traciality candidate

The direct automorphism/traciality candidate says:

`source-free local state has no preferred primitive projector`
`-> rho_cell = I_16 / 16`.

The thermal route says:

`source-free local KMS state is tracial iff beta = 0 or H_cell is scalar`.

So the thermal route does not truly replace the direct candidate. It just
re-expresses it in thermal language.

If `beta = 0` is adopted as the source-free law, that is basically the
infinite-temperature / max-entropy version of local traciality.

If `H_cell` is forced to be scalar, that is basically the no-preferred-splitting
version of local traciality.

So the direct source-free traciality theorem remains the cleaner formulation.

## Honest status

This route is **not retained closure**.

What is closed:

- exact finite-cell KMS/Gibbs form;
- exact criterion for when the KMS state is tracial;
- exact reason the route does not close automatically.

What is still open:

- a retained theorem that source-free primitive local state is the
  infinite-temperature KMS state, or
- a retained theorem that source-free primitive generator is scalar.

Without one of those, the Planck route stays conditional.

## Safe wording

**Can claim**

- the primitive thermal/KMS route reduces the last Planck blocker to one exact
  criterion;
- on the primitive cell, thermal traciality is equivalent to `beta = 0` or
  scalar `H_cell`;
- the current package does not yet supply that premise;
- the route therefore sharpens but does not close retained Planck.

**Cannot claim**

- that a primitive thermal/KMS grammar by itself derives `rho_cell = I_16/16`;
- that the branch now has an axiom-native retained Planck derivation;
- that `beta = 0` is already earned rather than chosen.

## Changed files

- `docs/PLANCK_SCALE_SOURCE_FREE_LOCAL_TRACIALITY_THERMAL_TRACE_ROUTE_2026-04-23.md`
- `scripts/frontier_planck_source_free_local_traciality_thermal_trace_route.py`
