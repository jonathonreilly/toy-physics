# DM Neutrino `v_even` Bosonic Normalization Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
transfer coefficients  
**Script:** `scripts/frontier_dm_neutrino_veven_bosonic_normalization_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

After the weak even swap-reduction theorem, the exact current even leg is

`[E1, E2]^T = v_even tau_+`

with

- `tau_+ = tau_E + tau_T`
- `v_even = (v_1, v_2)^T`.

Can the coefficient vector `v_even` itself be fixed from the single axiom plus
the current atlas?

## Bottom line

Yes, canonically.

The two exact even channels

- `E1 = delta + rho`
- `E2 = A + b - c - d`

have canonical Frobenius-dual target generators

- `F1 = (1/2) T_delta + (1/4) T_rho`
- `F2 = A_op + (1/4) b_op - (1/2) c_op - (1/2) d_op`.

These are isospectral to scaled copies of the unique traceless row generator
on the exact 2-row weak source factor:

- `F1 <-> sqrt(3/8) Z_row`
- `F2 <-> (3/sqrt(8)) Z_row`

with

`Z_row = diag(1,-1)`.

Under the unique additive CPT-even bosonic source-response generator, this
fixes the even coefficient vector to

`v_even = (sqrt(8/3), sqrt(8)/3)`

on the source-oriented branch convention.

Equivalently:

`E1 = sqrt(8/3) tau_+`

`E2 = (sqrt(8)/3) tau_+`.

## Exact even channel representatives

The active Hermitian basis entering these channels is Frobenius-orthogonal:

- `A_op`
- `b_op`
- `c_op`
- `d_op`
- `T_delta`
- `T_rho`.

So the exact Riesz/Frobenius dual representatives of the two scalar channels
are:

`F1 = (1/2) T_delta + (1/4) T_rho`

because

`<H, F1>_F = delta + rho = E1`,

and

`F2 = A_op + (1/4) b_op - (1/2) c_op - (1/2) d_op`

because

`<H, F2>_F = A + b - c - d = E2`.

So the even channels are not just coordinate names. They are exact scalar
observables with canonical target generators.

## Exact source-side row factor

The weak even swap-reduction theorem already proved that the exact current
source carrier factors through the symmetric source combination

`tau_+ = tau_E + tau_T`

and that the live source geometry is the exact 2-row factor of

`K_R(q) = [1, delta_A1(q)]^T [u_E(q), u_T(q)]`.

On that exact row factor, the unique traceless Hermitian generator is

`Z_row = diag(1,-1)`.

So the single-axiom source side now offers one exact canonical even generator.

## Spectral match

The target generators have exact spectra:

- `spec(F1) = {-sqrt(3/8), 0, +sqrt(3/8)}`
- `spec(F2) = {-3/sqrt(8), 0, +3/sqrt(8)}`.

The source row generator has

- `spec(Z_row) = {-1, +1}`.

Therefore:

- `F1` is isospectral to `sqrt(3/8) Z_row`
- `F2` is isospectral to `(3/sqrt(8)) Z_row`

up to the same null-multiplicity issue already handled in the `c_odd`
theorem.

## Bosonic normalization law

Let

`W[J] = log|det(D+J)| - log|det D|`

be the unique additive CPT-even scalar generator.

Then on scalar baselines:

- `F1` and `sqrt(3/8) Z_row` have the same exact bosonic source-response
- `F2` and `(3/sqrt(8)) Z_row` have the same exact bosonic source-response.

So the scalar source amplitude `tau_+` is related to the channel amplitudes by

`sqrt(3/8) E1 = tau_+`

`(3/sqrt(8)) E2 = tau_+`.

Hence

`E1 = sqrt(8/3) tau_+`

`E2 = (sqrt(8)/3) tau_+`.

This is exactly

`v_even = (sqrt(8/3), sqrt(8)/3)`.

## What this closes

This closes the even transfer coefficients.

The branch can no longer honestly say:

- “the odd coefficient is closed, but the even coefficient vector is still open”

The sharper statement is:

- the odd coefficient is closed: `c_odd = +1`
- the even coefficient vector is closed:
  `v_even = (sqrt(8/3), sqrt(8)/3)`

So the transfer coefficients are now fully fixed on the current exact
single-axiom transfer bundle.

## What this does not close

This note does **not** derive:

- the selector amplitude `a_sel`
- the symmetric weak source amplitude `tau_+`
- the full leptogenesis benchmark after rewriting the kernel in terms of the
  exact transfer law

So this is a coefficient-normalization theorem, not yet a full benchmark
rebuild theorem.

## Benchmark consequence

The benchmark remains

- `eta = 1.81e-10`
- `eta / eta_obs ~= 0.30`

for a precise reason: the current benchmark runner still uses the older reduced
kernel. This theorem closes the transfer coefficients, not yet the source
amplitude law or the full rewritten kernel.

## Command

```bash
python3 scripts/frontier_dm_neutrino_veven_bosonic_normalization_theorem.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit upstream authority
citations named by the 2026-05-05 audit verdict's
`missing_dependency_edge` repair target (audit row:
`dm_neutrino_veven_bosonic_normalization_theorem_note_2026-04-15`,
`audited_conditional`, leaf criticality). It does not promote this note
or change the audited claim scope, which remains the conditional
isospectrality identification of the active even target generators
`F1`, `F2` with scaled copies of the source row generator `Z_row` plus
the imported bosonic source-response premise.

One-hop authorities cited:

- [`DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md)
  — currently `unaudited` (audit row:
  `dm_neutrino_weak_even_swap_reduction_theorem_note_2026-04-15`).
  Upstream authority candidate for the exact 2-row factor of `K_R(q)`
  and the symmetric source carrier `tau_+ = tau_E + tau_T` used in this
  note's "Exact source-side row factor" section.
- [`DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md)
  — currently `unaudited` (audit row:
  `dm_neutrino_triplet_character_source_theorem_note_2026-04-15`).
  Upstream authority candidate for the active Hermitian basis
  (`A_op, b_op, c_op, d_op, T_delta, T_rho`) entering the even channels
  `E1 = delta + rho` and `E2 = A + b - c - d`.
- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — currently `audited_conditional` (audit row:
  `observable_principle_from_axiom_note`). Upstream conditional
  authority for the load-bearing premise that physical local scalar
  observables are exact source derivatives of the unique additive
  CPT-even scalar generator `W[J] = log|det(D+J)| - log|det D|`, given
  premises P1 (scalar additivity), P2 (CPT-even phase blindness),
  P3 (continuity / minimal regularity), and P4 (normalization choice).

Because two of the three cited upstream authorities are `unaudited` and
the third is `audited_conditional`, the even coefficient vector
selection `v_even = (sqrt(8/3), sqrt(8)/3)` cannot lift past
`audited_conditional` under the standard cite-chain rule. This matches
the live audit row's current `audited_conditional` verdict and does not
require any audit JSON edit.

The runner-checked content of this note (Part 1: spectra of `F1, F2`
and `Z_row`; Part 2: isospectrality `F1 <-> sqrt(3/8) Z_row`,
`F2 <-> (3/sqrt(8)) Z_row`; Part 3: identical exact bosonic response on
scalar baselines forcing
`v_even = (sqrt(8/3), sqrt(8)/3)`; Part 4: closure point of the even
transfer coefficients) is exact finite-dimensional matrix algebra on
the active 2- and 3-dimensional source/target blocks and is independent
of the cited upstream authorities. The cite chain is what supplies the
physical selection rule that turns isospectrality into a coefficient
identity rather than only a comparator.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
the observation that A=9 algebraic checks close after hard-coding the
matrices and source-row generator that carry the contested structure,
but the runner-only restricted packet does not derive the active
Hermitian basis, the exact 2-row source carrier, or the bosonic
source-response normalization bridge from `Cl(3)` on `Z^3`. The
cite-chain repair above wires `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE`
(`audited_conditional`) as the bosonic source-response authority and
`DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15` and
`DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15` (both
`unaudited`) as the source-row-factor and active-basis upstream
authorities. The fact that two upstream authorities are still
`unaudited` is registered explicitly here as an open class D upstream
gap (no retained one-hop authority on the source side); closing those
two upstream rows is the path to lifting the current
`audited_conditional` verdict on this row, not local rewriting of this
note. Effective status remains `audited_conditional` under the
cite-chain rule. The note's `audit_status` is unchanged by this
addendum.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) with an
explicit class D upstream gap registration. It does not change any
algebraic content, runner output, or load-bearing step classification.
It records the upstream authorities the audit verdict expected and
matches the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` rigorize
(commit `8e84f0c23`) and the `DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`
cluster rigorize (commit `02ad4fadd`).
