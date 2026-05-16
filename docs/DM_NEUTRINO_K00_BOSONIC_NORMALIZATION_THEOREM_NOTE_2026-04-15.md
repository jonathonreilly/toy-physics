# DM Neutrino `K00` Bosonic Normalization Theorem (Conditional)

**Date:** 2026-04-15  
  - status line narrowed 2026-05-16 per 2026-05-05 audit-lane verdict
    (`audited_renaming`, class F, leaf criticality, audit row:
    `dm_neutrino_k00_bosonic_normalization_theorem_note_2026-04-15`)
**Claim type:** bounded_theorem
**Status:** bounded conditional diagonal-normalization selector on the
upstream DM-neutrino source packet — IF the unique additive CPT-even
bosonic-observable principle is taken as the physical local scalar
observable selector (observable-principle premise), AND IF the source
amplitudes `tau_E = tau_T = 1/2` are taken from the upstream
source-oriented branch (source-amplitude premise), THEN the algebraic
checks close and the heavy-basis diagonal normalization is `K00 = 2`.
The observable-principle premise is currently registered as
`audited_conditional` on the audit lane (upstream:
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md));
the source-amplitude premise enters via two `unaudited` upstream
authorities (see the audit dependency repair links section below). Not
yet a retained-grade baseline-framework diagonal-normalization theorem; the
runner verifies the algebraic identifications, not the load-bearing
coefficient law or the source-amplitude branch values.
**Script:** `scripts/frontier_dm_neutrino_k00_bosonic_normalization_theorem.py`

## Framework sentence

In this note, the baseline physical framework is `Cl(3)` local algebra on the
`Z^3` spatial substrate. Everything else is a derived atlas row or an admitted
lane premise.

## Question

Once the exact source package is closed, can the remaining heavy-neutrino-basis
diagonal normalization

`K00 = (K_mass)00`

be fixed canonically from the same single-axiom source-response machinery?

## Bottom line

Conditionally yes — `K00 = 2` follows from the algebra below once the
upstream observable-principle premise and the upstream source-amplitude
premise are accepted as inputs. The runner-checked content (Parts 1-4
below) is exact finite-dimensional matrix algebra. The two physical
inputs that promote the algebra to the numerical value `K00 = 2` are
imported from upstream authorities, not derived inside the restricted
runner packet of this note. The audit lane records this as
`audited_renaming` rather than `audited_clean` for that reason.

The target functional `K00` has exact Frobenius-dual generator

`F00 = J3/3`

with `J3` the `3 x 3` all-ones matrix. On the source side, the exact swap-even
weak mode `tau_+ = tau_E + tau_T` lives on the row-sum generator

`J2 = [[1,1],[1,1]]`.

Since `F00` is isospectral to `(1/2) J2`, **and assuming the unique
additive CPT-even bosonic-observable principle as the local scalar
observable selector**, the coefficient law is

`K00 = 2 tau_+`.

**Assuming the upstream source-oriented branch** then sets

- `tau_E = 1/2`
- `tau_T = 1/2`
- `tau_+ = 1`

so the heavy-basis diagonal normalization is

`K00 = 2`.

Both italicised premises are explicitly admitted inputs of this
conditional packet; neither is derived inside this note or its runner.

## Honest conditional scope

The two load-bearing imports of this conditional packet, each named by
the 2026-05-05 audit verdict, are:

1. **Observable-principle premise** (audit class F load-bearing): the
   identification of physical local scalar observables with exact
   source-response coefficients of the unique additive CPT-even scalar
   generator `W[J] = log|det(D+J)| - log|det D|`. This is the premise
   that turns isospectrality of `F00` with `(1/2) J2` into the
   coefficient identity `K00 = 2 tau_+`. Upstream authority:
   [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
   (currently `audited_conditional`).

2. **Source-amplitude premise** (audit class F load-bearing): the
   values `tau_E = tau_T = 1/2` of the source amplitudes. The runner
   hard-codes these and does not derive them from `Cl(3)` on `Z^3`.
   Upstream authority candidates are
   [`DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md)
   (currently `unaudited`; supplies `tau_+ = tau_E + tau_T` on the
   row-sum generator `J2` but not the individual magnitudes) and
   [`DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md)
   (currently `unaudited`; that note itself explicitly disclaims
   deriving the magnitude of `gamma`, `delta`, `rho`, and by extension
   `tau_E`, `tau_T`).

Because neither of the two premises is currently retained, the
endpoint `K00 = 2` is not a retained number. It is a conditional value
that the algebra below carries forward exactly once those two
upstream gaps close. The conditional structure here matches the live
pattern of the sister theorem
[`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md)
(headline "Bosonic Normalization Theorem (Conditional)"), which makes
the same observable-principle premise explicit. The path from
`audited_renaming` to `audited_conditional` for this row is upstream
closure of the source-amplitude premise; the path from
`audited_conditional` to `audited_clean`/retained additionally requires
the observable-principle premise to lift past its own conditional
verdict.

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

## Consequence (conditional on the two upstream premises)

Conditional on the observable-principle premise and the
source-amplitude premise (see "Honest conditional scope" above), the
diagonal-normalization slot the exact-source diagnostic left open is
filled by `K00 = 2`. Within this conditional packet the source-side
package is

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`
- `K00 = 2`

which is the conditional kernel input that the downstream coherent
leptogenesis sum currently consumes. The downstream sum inherits the
conditional status of both upstream premises through the cite-chain
rule and is not itself retained at the value `K00 = 2` until the two
upstream gaps named above close.

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

## Scope of this 2026-05-16 honest demotion

The 2026-05-16 follow-up edit (this revision) does not add or change
any algebraic content, runner code, or load-bearing step classification
either. It narrows the headline status line, the Question/Bottom-line
framing, and the Consequence section to make the two load-bearing
upstream premises (observable-principle premise; source-amplitude
premise) explicit at the top of the note rather than only at the
graph-bookkeeping addendum, and to make the conditional nature of the
endpoint `K00 = 2` explicit in the headline. It matches the conditional
headline pattern of the sister theorem
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`
(headline "(Conditional)"). It does not edit the runner, the runner
cache, the audit ledger JSONs, the publication matrix, or any
verdict-bearing audit artefact. The note's `audit_status` is unchanged
and must be re-set by the audit lane, not by this edit.
