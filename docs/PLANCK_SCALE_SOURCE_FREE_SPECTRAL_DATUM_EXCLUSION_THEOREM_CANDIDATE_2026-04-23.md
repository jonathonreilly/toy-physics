# Planck-Scale Source-Free Spectral-Datum Exclusion Theorem Candidate

**Date:** 2026-04-23  
**Status:** science-only new-theory candidate on the last Planck blocker  
**Audit runner:** `scripts/frontier_planck_source_free_spectral_datum_exclusion_theorem_candidate.py`

## Question

Can the last Planck blocker be attacked in the most direct possible way on the
primitive one-cell algebra, without introducing thermodynamic language,
boundary language, or even an explicit symmetry principle?

The only remaining blocker is:

`rho_cell = I_16 / 16`.

The direct counting law is already closed:

`c_cell(rho) = Tr(rho P_A)`.

So the question is:

> what does it really mean for a local state on the primitive cell to be
> source-free?

## Bottom line

The cleanest direct candidate is:

> **Source-Free Spectral-Datum Exclusion Theorem.**
> On the primitive one-cell algebra `M_16(C)`, a source-free local state cannot
> itself inject a canonically retrievable proper local projector. But every
> nontracial state does exactly that through its spectral decomposition.
> Therefore the unique source-free local state is the tracial state
>
> `rho_cell = I_16 / 16`.

Then the direct counting theorem gives

`c_cell = Tr((I_16 / 16) P_A) = 1/4`,

so the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

This route is sharper than the older flip witness and even sharper than the
automorphism/max-entropy packaging, because it says exactly what is wrong with
every nontracial candidate:

> it already contains extra one-cell datum in the form of a preferred spectral
> sector.

## Why this route is distinct

Earlier direct candidates said:

- no preferred primitive projector;
- unitary naturality;
- center-only local datum;
- max entropy.

All of those point to the trace state. The present route isolates the common
core:

> a nontracial state is not source-free because the state itself canonically
> singles out proper local spectral projectors.

So the remaining question is no longer about how to choose the uniform state.
It is:

> can a source-free local state be allowed to carry its own proper spectral
> datum?

If not, traciality follows immediately.

## Inputs

This note uses only already-opened branch-local surfaces:

- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CENTRAL_CELL_STATE_THEOREM_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CENTRAL_CELL_STATE_THEOREM_CANDIDATE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_LOCAL_NATURALITY_TRACIALITY_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_LOCAL_NATURALITY_TRACIALITY_CANDIDATE_2026-04-23.md)

What those already fix:

1. the Planck route is reduced to a local state theorem on `M_16(C)`;
2. current retained structure still leaves a nontrivial family of source-free
   candidates;
3. the only real issue is what "source-free local state" is allowed to mean.

## Setup

Work on the primitive one-cell algebra

`A_cell = M_16(C)`.

Let `rho` be a normalized positive operator on `H_cell = C^16`.

Call a proper projector `Q` **canonically retrievable from `rho`** if `Q` is
determined by `rho` alone through exact spectral functional calculus, with no
additional local datum.

For example, if `rho` has a maximal eigenvalue `lambda_max`, then the spectral
projector

`Q_max = 1_{ {lambda_max} } (rho)`

is canonically retrievable from `rho`.

## Theorem 1: every nontracial state carries proper spectral datum

Let `rho` be a normalized positive operator on `C^d`.

If `rho != I_d / d`, then there exists a canonically retrievable proper
projector `Q` with

`0 < rank(Q) < d`.

### Proof

If `rho != I_d / d`, then not all eigenvalues of `rho` are equal.

So the spectrum contains at least two distinct values. Let `lambda_max` be the
largest eigenvalue.

Define

`Q_max = 1_{ {lambda_max} } (rho)`.

This is determined by `rho` alone through functional calculus, so it is
canonically retrievable from `rho`.

Because `lambda_max` is an eigenvalue, `Q_max != 0`.

Because not all eigenvalues are equal, the full space is not the
`lambda_max`-eigenspace, so `Q_max != I_d`.

Therefore

`0 < rank(Q_max) < d`,

so `Q_max` is a proper canonically retrievable projector.

## Corollary 1: source-free local state must be tracial

Assume:

> a source-free local state on the primitive cell may not itself inject any
> canonically retrievable proper local projector.

Then by Theorem 1 every nontracial state is excluded.

Therefore the only normalized positive source-free local state is

`rho_cell = I_16 / 16`.

## Corollary 2: quarter follows immediately

The direct counting theorem already gives

`c_cell(rho) = Tr(rho P_A)`.

So with `rho_cell = I_16 / 16` and `rank(P_A)=4`,

`c_cell = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4`.

Then the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

## Why this is strong

This candidate says the missing content is not really "choose the uniform
state" at all.

It says:

- the local primitive cell is physical;
- source-free means no extra local datum;
- but a nontracial state already contains extra exact local datum, namely its
  own proper spectral projector structure;
- therefore only the trace state survives.

That is a cleaner direct argument than:

- maximizing entropy,
- choosing infinite temperature,
- or inserting a special symmetry group by hand.

Those can all be read as consequences or witnesses of the same deeper fact.

## Honest status

This is **not** yet retained.

It is a new theorem candidate.

The honest claim is only:

- the direct counting law is already closed;
- the current retained stack still underdetermines the source-free state;
- the cleanest remaining direct argument may be that every nontracial state
  already carries forbidden one-cell spectral datum.

So the Planck lane is now reduced to one sharp question:

> can a source-free local state on a physical primitive finite cell be allowed
> to carry a canonically retrievable proper spectral projector?

If the answer is no, Planck closes immediately.
