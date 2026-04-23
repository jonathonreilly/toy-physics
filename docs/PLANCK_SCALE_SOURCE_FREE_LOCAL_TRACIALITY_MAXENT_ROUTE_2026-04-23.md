# Planck-Scale Source-Free Local Traciality Max-Entropy Route

**Date:** 2026-04-23  
**Status:** science-only max-entropy theorem candidate plus sharp retained no-go  
**Audit runner:** `scripts/frontier_planck_source_free_local_traciality_maxent_route.py`

## Question

After the direct counting law is closed,

`c_cell(rho) = Tr(rho P_A)`,

can the last blocker

`rho_cell = I_16 / 16`

be derived from a sharp source-free / no-local-datum maximum-entropy theorem on
the primitive time-locked cell algebra `M_16(C)`?

## Bottom line

Yes, conditionally; no, not yet as a retained theorem.

The clean max-entropy route is:

1. work on the full primitive one-cell algebra `A_cell = M_16(C)`;
2. interpret "source-free / no local datum" as:
   no local expectation constraints are imposed on the one-cell state;
3. choose the source-free local state by maximum von Neumann entropy on the full
   primitive cell;
4. then the unique maximizer is the tracial state

   `rho_cell = I_16 / 16`;

5. with the already-closed counting law,

   `c_cell = Tr(rho_cell P_A) = 4/16 = 1/4`,

   so the direct Planck route closes:

   `a^2 = l_P^2`,
   hence
   `a = l_P`.

But the current retained stack does **not** yet contain the missing step

`source-free => maximize entropy on the full primitive cell`.

So the strongest honest result is:

- **new theorem candidate:** source-free full-cell maximum entropy implies
  traciality and closes the route;
- **exact retained no-go:** without promoting that theorem, the current retained
  stack still leaves a nontrivial family of admissible source-free cell states.

## Why this is the right max-entropy formulation

The source-free problem is no longer a packet-combinatorics problem.

The direct worldtube route already fixes:

- the primitive carrier `H_cell = C^16`,
- the one-step packet `P_A`,
- the direct counting law `c_cell(rho) = Tr(rho P_A)`.

So the only remaining open content is local state selection on the primitive
cell.

If "source-free / no local datum" is to have a clean information-theoretic
meaning, the sharpest version is:

> among all density matrices on the full primitive cell algebra compatible with
> no additional one-cell expectation constraint, pick the entropy maximizer.

That is the smallest exact max-entropy statement that can possibly close the
route.

## Inputs

This route uses the already-open branch-local surfaces:

- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)

The current retained-direct note already proves the important negative result:
the accepted stack alone does **not** select `rho_cell = I_16 / 16`.

## Setup

Work on the primitive time-locked one-cell algebra

`A_cell = M_16(C)`.

Let the source-free local state be a density matrix `rho` on `A_cell`.

Let the section-canonical one-step worldtube packet be

`P_A = sum_(|eta|=1) P_eta`,

with rank `4`.

The already-closed direct counting theorem gives

`c_cell(rho) = Tr(rho P_A)`.

Define the tracial state

`tau_16 := I_16 / 16`.

Define the von Neumann entropy

`S(rho) := - Tr(rho log rho)`.

## Candidate principle: source-free full-cell maximum entropy

Call a state selection law **source-free full-cell max-entropy** if it says:

> In the absence of any additional one-cell datum or expectation constraint,
> the physical source-free local state is the entropy maximizer on the full
> primitive one-cell algebra `M_16(C)`.

This is stronger than the current retained stack, but it is cleaner than the
older scalar-Schur route because it attacks the last blocker directly.

## Theorem 1: full-cell max-entropy forces the tracial state

Among all density matrices on `M_16(C)`, the unique maximizer of von Neumann
entropy is

`tau_16 = I_16 / 16`.

### Proof

Use relative entropy against the tracial state:

`D(rho || tau_16) = Tr(rho (log rho - log tau_16)) >= 0`.

Since `log tau_16 = - log 16 * I_16`,

`D(rho || tau_16) = Tr(rho log rho) + log 16`

because `Tr(rho) = 1`.

So

`D(rho || tau_16) = log 16 - S(rho) >= 0`,

hence

`S(rho) <= log 16`.

Equality holds iff `D(rho || tau_16) = 0`, i.e. iff `rho = tau_16`.

Therefore the unique maximum-entropy source-free state is

`rho_cell = I_16 / 16`.

## Corollary 1: quarter follows immediately

With the direct counting law already closed,

`c_cell(rho) = Tr(rho P_A)`,

Theorem 1 gives

`c_cell = Tr((I_16 / 16) P_A) = rank(P_A) / 16 = 4/16 = 1/4`.

So if source-free full-cell maximum entropy is accepted, the direct Planck
route closes:

`a^2 = l_P^2`,
therefore
`a = l_P`.

## Theorem 2: strongest exact retained no-go on the max-entropy route

The current retained stack does **not** yet imply the source-free full-cell
maximum-entropy principle.

Therefore the current retained stack does **not** yet derive

`rho_cell = I_16 / 16`

by the max-entropy route.

### Reason

The retained-direct source-free derivation note already proves that the current
accepted direct stack leaves an exact nontrivial family of admissible
source-free candidate states on the full `C^16` cell.

In particular, it contains both:

- the tracial witness

  `rho_tr = I_16 / 16`,

  with
  `Tr(rho_tr P_A) = 1/4`;

- the packet-light witness

  `rho_lt = (1/32) P_A + (7/96) (I_16 - P_A)`,

  with
  `Tr(rho_lt P_A) = 1/8`.

The entropy theorem strictly prefers `rho_tr` over `rho_lt`, but that
preference appears only **after** one adds the new source-free max-entropy
selection law.

So the sharp retained verdict is:

> the max-entropy route is exact and mathematically clean, but it is still a
> new theorem candidate rather than an already-retained consequence.

## Why this is sharper than a vague "maximum ignorance" slogan

The real content is not the phrase "maximum ignorance." The sharp version is:

- maximize entropy on the **full primitive cell algebra**;
- do **not** pre-restrict the state to packet-weight families beyond positivity
  and normalization;
- do **not** insert extra local expectation constraints by hand.

If any extra one-cell datum is introduced, the maximizer can move away from the
tracial state. So the theorem candidate is exact about what "no local datum"
must mean.

## Honest verdict

This route now has a clean exact split:

- **Conditional close:** if the source-free local state is defined by full-cell
  maximum entropy with no extra one-cell datum, then
  `rho_cell = I_16 / 16`, quarter follows, and the direct Planck route closes.
- **Retained status today:** not closed. The current accepted stack still lacks
  the theorem equating source-free local physics with that maximum-entropy
  principle.

So the max-entropy route is now either:

- the cleanest new theorem candidate for the last blocker, or
- the strongest exact statement of what is still missing if review refuses that
  candidate.
