# DM Neutrino `K00` Bosonic Normalization Theorem

**Date:** 2026-04-15  
**Status:** exact diagonal-normalization theorem on the refreshed `main`-derived DM lane  
**Script:** `scripts/frontier_dm_neutrino_k00_bosonic_normalization_theorem.py`

## Framework sentence

In this note, "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

Once the exact source package is closed, can the remaining heavy-neutrino-basis
diagonal normalization

`K00 = (K_mass)00`

be fixed canonically from the same single-axiom source-response machinery?

## Bottom line

Yes.

The target functional `K00` has exact Frobenius-dual generator

`F00 = J3/3`

with `J3` the `3 x 3` all-ones matrix. On the source side, the exact swap-even
weak mode `tau_+ = tau_E + tau_T` lives on the row-sum generator

`J2 = [[1,1],[1,1]]`.

Since `F00` is isospectral to `(1/2) J2`, the unique additive CPT-even bosonic
observable fixes the coefficient law

`K00 = 2 tau_+`.

On the exact source-oriented branch,

- `tau_E = 1/2`
- `tau_T = 1/2`
- `tau_+ = 1`

so the exact heavy-basis diagonal normalization is

`K00 = 2`.

## Exact target formula

On the exact breaking-triplet decomposition

`H = H_core + B(delta,rho,gamma)`

with

`H_core = [[A,b,b],[b,c,d],[b,d,c]]`

and

`B = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`,

the transformed heavy-basis diagonal is

`K00 = (K_mass)00 = (A + 4b + 2c + 2d)/3`.

Equivalently,

`K00 = Tr(H F00),  F00 = J3/3`.

So `K00` is independent of the odd/even breaking triplet
`(delta,rho,gamma)` and depends only on the aligned core.

## Bosonic normalization argument

The exact source-side even mode is not the projector `(1/2) J2`; it is the
full row-sum generator `J2` with amplitude `tau_+`.

The bosonic observable principle compares exact source-deformed responses

`W[J] = log|det(D+J)| - log|det D|`.

Since `F00` and `(1/2) J2` have the same nonzero spectrum `{+1}`, they have
identical exact bosonic response on scalar baselines. Therefore the target
coefficient must compensate the factor of `2` between `J2` and `(1/2) J2`,
forcing

`K00 = 2 tau_+`.

## Consequence

This closes the diagonal normalization that the exact-source diagnostic left
open.

The refreshed branch no longer has:

- open odd transfer coefficient
- open even transfer vector
- open source amplitudes
- open heavy-basis diagonal normalization

At this point the exact source-side package is

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`
- `K00 = 2`

which is the full exact kernel input for the standard coherent leptogenesis
sum on the retained benchmark.

## Command

```bash
python3 scripts/frontier_dm_neutrino_k00_bosonic_normalization_theorem.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit upstream authority
citations named by the 2026-05-05 audit verdict. The verdict
(`audited_renaming`, leaf criticality, audit row:
`dm_neutrino_k00_bosonic_normalization_theorem_note_2026-04-15`) records
that the algebraic isospectrality check closes (A=7), but the bridge
from isospectral bosonic response to the physical coefficient identity
`K00 = 2 tau_+` is asserted rather than derived from the single axiom
in the runner packet, and `tau_E = tau_T = 1/2` is hard-coded rather
than computed from `Cl(3)` on `Z^3`. This addendum does not promote
this note or change the audited claim scope, which remains the
conditional isospectrality identification of the target diagonal
generator `F00 = J3/3` with the scaled source row-sum mode `(1/2) J2`
plus the imported bosonic source-response premise.

One-hop authorities cited:

- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — currently `audited_conditional` (audit row:
  `observable_principle_from_axiom_note`). Upstream conditional
  authority for the load-bearing premise that physical local scalar
  observables are exact source derivatives of the unique additive
  CPT-even scalar generator `W[J] = log|det(D+J)| - log|det D|`, given
  premises P1 (scalar additivity), P2 (CPT-even phase blindness),
  P3 (continuity / minimal regularity), and P4 (normalization choice).
  This is the upstream authority the audit verdict identifies as
  required for the bosonic coefficient law `K00 = 2 tau_+` to follow
  from isospectrality rather than be asserted.
- [`DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md)
  — currently `unaudited` (audit row:
  `dm_neutrino_weak_even_swap_reduction_theorem_note_2026-04-15`).
  Upstream authority candidate for the exact swap-even weak mode
  `tau_+ = tau_E + tau_T` on the row-sum generator `J2`. This is the
  upstream that would supply the source-side `tau_+` carrier without
  hard-coding.
- [`DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md)
  — currently `unaudited` (audit row:
  `dm_neutrino_triplet_character_source_theorem_note_2026-04-15`).
  Upstream authority candidate for the source-oriented branch values
  `tau_E = tau_T = 1/2` flowing into `tau_+ = 1` and therefore
  `K00 = 2`. The audit verdict records these source amplitudes as
  hard-coded in the current runner; the path to deriving them is
  upstream closure of this triplet-character source authority, not
  local rewriting of this note.

Because all three cited upstream authorities are either `unaudited` or
`audited_conditional`, the heavy-basis diagonal normalization
identification `K00 = 2` cannot lift past `audited_conditional` under
the standard cite-chain rule. The current `audited_renaming` status
records that the source-amplitude branch is hard-coded; the path to
moving from `audited_renaming` to `audited_conditional` is the
weak-even-swap and triplet-character source upstream closures cited
above. The path to moving from `audited_conditional` to
`audited_clean`/retained additionally requires
`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE` to lift past its own
conditional verdict (i.e., P1-P4 to be ratified). No audit JSON edit
is required by this addendum.

The runner-checked content of this note (Part 1: target formula
`K00 = (A + 4b + 2c + 2d)/3 = Tr(H F00)` with `F00 = J3/3` independent
of `(delta, rho, gamma)`; Part 2: isospectrality of `F00` with
`(1/2) J2` (both rank-one projectors, spectrum `{+1}` plus zeros);
Part 3: identical exact bosonic response forcing
`K00 = 2 tau_+`; Part 4: source package `tau_E = tau_T = 1/2` giving
`tau_+ = 1` and `K00 = 2`) is exact finite-dimensional matrix algebra
on the 3 x 3 heavy basis and the 2 x 2 source row-sum block and is
independent of the cited upstream authorities. The cite chain is what
supplies the physical selection rule that turns isospectrality into a
coefficient identity, and the source-side authority that would supply
`tau_E = tau_T = 1/2` from `Cl(3)` on `Z^3` rather than as an imported
branch convention.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_renaming` (a
narrowing verdict, not a failure) with the observation that A=7
algebraic checks close, but the load-bearing identification of the
target `K00` normalization with twice the source amplitude is imposed
as a coefficient law rather than independently computed, and the final
value `K00 = 2` depends on hard-coded `tau_E = tau_T = 1/2` with no
retained upstream authority cited in the restricted packet. The
cite-chain repair above wires `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE`
(`audited_conditional`) as the bosonic-coefficient-law authority and
the weak-even-swap and triplet-character source theorems (both
`unaudited`) as the source-amplitude upstream authorities. The fact
that two of the three upstream authorities are still `unaudited` is
registered explicitly here as an open class D upstream gap; closing
those two upstream rows is the path to lifting the current
`audited_renaming` verdict toward `audited_conditional`, not local
rewriting of this note. Effective status remains `audited_renaming`
under the cite-chain rule because the strongest upstream is still
itself only `audited_conditional`. The note's `audit_status` is
unchanged by this addendum.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) with an
explicit class D upstream gap registration. It does not change any
algebraic content, runner output, or load-bearing step classification.
It records the upstream authorities the audit verdict expected and
matches the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` rigorize
(commit `8e84f0c23`) and the `DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`
cluster rigorize (commit `02ad4fadd`).
