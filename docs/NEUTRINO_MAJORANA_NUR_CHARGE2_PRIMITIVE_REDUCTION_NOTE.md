# Neutrino Majorana `nu_R` Charge-2 Primitive Reduction

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Script:** [`scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py`](../scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py)
**Runner sha256:** `48f7644cc9ba2482c58b88cd29feb43a8bfb99ff263f21effb1f8117e6685247`

## Audit-conditional perimeter (2026-05-05)

The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and load-bearing step
class `A`. The audit chain-closure explanation is exact:

> "The local `2 x 2` algebra closes, but the claim that the current scalar
> transfer / response bank still misses exactly that slot imports the premise
> that the bank spans only diagonal Nambu lifts. No cited authority or runner
> data derives the actual bank span from the restricted packet."

The audit-stated repair target is verbatim:

> "missing_dependency_edge: provide the retained-grade note or certificate
> deriving that the current scalar transfer / response Nambu lifts span only
> the diagonal subspace on the retained `nu_R` line, or make the audited
> scope only the local `2 x 2` primitive reduction."

The audit verdict explicitly offers a scope-narrowing route ("or make the
audited scope only the local `2 x 2` primitive reduction"). This
rigorization edit only sharpens the boundary of the conditional perimeter;
nothing here promotes audit status. The runner's `PASS=11 FAIL=0` already
covers the local `2 x 2` algebra exhaustively (parts 1, 2, 3); the part-4
"current bank misses that slot" claim is the part of the runner that imports
the bank-span premise the audit verdict flags.

## Question
On the retained one-line `nu_R` lane, if a sole-axiom Majorana reopening ever
exists, what is the exact missing object? Is it still a matrix family, or has
the problem already reduced to one canonical source slot?

## Answer
It has already reduced all the way down.

On the doubled `nu_R` line, the charge-`(+2)` adjoint eigenspace is exactly the
one-dimensional slot `E12`. After the local antisymmetry / Nambu completion,
that slot becomes the one-complex-parameter block

`A_M(m) = m J_2`,  with  `J_2 = [[0,1],[-1,0]]`.

The existing local `nu_R` rephasing removes the phase of `m`, so every future
retained one-generation Majorana reopening is equivalent to the unique normal
form

`mu J_2`,  with  `mu >= 0`.

So the current Majorana blocker is not a hidden matrix family. It is one new
off-diagonal charge-`2` source amplitude on the doubled `nu_R` line.

## Exact Content

The theorem proves:

1. the charge-`(+2)` eigenspace of the doubled-line adjoint action is exactly
   one-dimensional
2. that eigenspace is the upper-right slot `E12`
3. the paired antisymmetric / Nambu completion is exactly the single-complex
   family `m J_2`
4. local `nu_R` rephasing removes the phase of `m`, leaving the unique real
   normal form `mu J_2`
5. the current scalar transfer / response bank still misses precisely that
   off-diagonal slot

## Consequence

This sharpens the Majorana side of the full-closure frontier.

The branch already showed:

- the retained `nu_R` support is rank `1`
- every sole-axiom projected observable on that support is scalar
- the induced Nambu lifts are diagonal and have zero anomalous block

This new theorem closes the remaining geometric ambiguity:

> if Majorana is ever reopened on the retained `nu_R` line, the missing object
> is exactly one rephasing-reduced off-diagonal charge-`2` amplitude `mu`.

So the current exact bank does not fail because it leaves a large unexplored
matrix family. It fails because it does not yet generate the one exact source
slot that Majorana would need.

## Cited authority chain (audit-conditional perimeter register)

The audit ledger entry for this row records `deps = []`, so the conditional
perimeter is the *unstated* citation surface. The table below registers the
neighbouring cluster authorities the note implicitly leans on, together with
their current ledger statuses, to make the conditional perimeter explicit.

| Cited authority | Note | Effective status (2026-05-10) | Conditional on |
|---|---|---|---|
| Anomaly-fixed unique `nu_R` Majorana channel (one-generation) | [`NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`](NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md) | unaudited | uniqueness of `S_unique = nu_R^T C P_R nu_R` |
| Local one-complex-coefficient reduction (canonical block) | [`NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md`](NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md) | unaudited | local Nambu pairing-plane structure |
| Phase removal by `nu_R` rephasing | [`NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md`](NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md) | unaudited | rephasing reduces `m J_2` to `mu J_2` with `mu >= 0` |
| Unique source slot | [`NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md`](NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md) | unaudited | uniqueness of the off-diagonal source slot under the local-bilinear assumption |
| `nu_R` transfer-character boundary (sibling row) | [`NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY_NOTE.md`](NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY_NOTE.md) | `audited_conditional` | scalar-character family on the rank-`1` `nu_R` line |
| Lower-level pairing no-go (sibling row) | [`NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md`](NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md) | `audited_conditional` | charge-preserving normal-kernel class on the retained lane |
| Charge-`2` primitive reduction (parent / cluster anchor) | [`NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md`](NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md) | unaudited | retained-grammar charge-zero containment |
| Retained Majorana lane packet | [`NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md`](NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md) | unaudited | aggregate listing of the cluster |
| Retained scalar-only Nambu-lift bank-span (the audit-flagged premise) | not yet packaged as a retained-grade note | not retained | the missing dependency edge / scope-narrowing target |

The audit-conditional perimeter is therefore precisely the last table row.
The runner closes parts 1-3 (the local `2 x 2` algebra: charge-`(+2)`
eigenspace dimension, antisymmetric / Nambu completion, rephasing-reduction)
fully and unconditionally. The conditional content lives in the part-4
assertion that the current scalar transfer / response bank lifts only to the
diagonal subspace on the retained `nu_R` line; the runner illustrates the
one-half of this implication that goes via `J_2`-vs-diagonal-span distance,
but does not derive the *bank span* itself.

## What the runner demonstrates exactly

The companion script
[`scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py`](../scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py)
runs four parts:

- **Part 1 (charge-`2` operator slot, retained-grade):** the adjoint action
  `ad_Q` on the doubled `nu_R` line has a one-dimensional charge-`(+2)`
  eigenspace, equal exactly to `span(E12)`; `E21` carries charge `-2`.
- **Part 2 (Nambu / antisymmetry completion, retained-grade):** the
  canonical antisymmetric completion of the charge-`2` slot is exactly
  `m J_2`; every local antisymmetric completion has zero diagonal.
- **Part 3 (local rephasing, retained-grade):** the local `nu_R` rephasing
  `U = exp(-i alpha) I` acts as `U A U^T` on the pairing block; choosing
  `alpha = arg(m) / 2` sends `m J_2` to `|m| J_2`; the missing source reduces
  to one real amplitude `mu >= 0`.
- **Part 4 (current-bank gap, audit-conditional):** the linear distance
  between `J_2` and the diagonal-block span is positive (about `1.41`); the
  runner reports this as evidence the current scalar bank misses that slot.
  The premise that the *retained* scalar transfer / response bank spans only
  the diagonal subspace is imported, not derived — this is the audit-flagged
  perimeter.

The `PASS=11 FAIL=0` includes both the unconditional parts 1-3 and the
conditional part-4 distance check; only the part-4 *interpretation* (current
bank ⟶ diagonal-only) imports the missing dependency edge.

## Audit-stated repair path

The audit verdict explicitly offers two repair routes:

1. **Cited authority route.** Provide a retained-grade note or certificate
   deriving that the current scalar transfer / response Nambu lifts span only
   the diagonal subspace on the retained `nu_R` line; add it as an explicit
   `deps` entry under this row. The runner content stays unchanged.
2. **Scope-narrowing route.** Restate the audited claim as "the local `2 x 2`
   primitive reduction" only — i.e. the parts 1-3 content (charge-`(+2)`
   slot, Nambu completion, rephasing-reduction) — and demote the
   current-bank-gap reading of part 4 to a heuristic illustration. The audit
   verdict explicitly admits this scope-narrowing route in
   `notes_for_re_audit_if_any`.

Both routes preserve the runner sha256
`48f7644cc9ba2482c58b88cd29feb43a8bfb99ff263f21effb1f8117e6685247` and
respect the ledger's `audit_status = audited_conditional`.

## Verification

```bash
python3 scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py
```

Expected: `PASS=11 FAIL=0`. Runner sha256 `48f7644c...85247`.
