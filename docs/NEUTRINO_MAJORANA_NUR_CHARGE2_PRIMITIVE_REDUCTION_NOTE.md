# Neutrino Majorana `nu_R` Charge-2 Primitive Reduction

**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem
**Date:** 2026-04-16  
**Script:** [`scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py`](../scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py)
**Runner sha256:** `93f3a18f3a93043b04b3f2f80660fd3a28fcfb197e0ac3f4e3d4338c1de3a457`

## Prior feedback perimeter (2026-05-05)

Prior independent feedback identified the scalar-bank span premise as
the load-bearing boundary for this row: the local `2 x 2` algebra
closes, but the current-bank reading imports the premise that the scalar
transfer / response bank spans only diagonal Nambu lifts. The requested
repair was either a theorem-grade derivation or certificate for that
bank-span premise, or a scope narrowing to only the local `2 x 2`
primitive reduction.

The feedback explicitly offers a scope-narrowing route: make the claim
only the local `2 x 2` primitive reduction. This rigorization edit
sharpens the boundary without changing source authority. The runner's
`PASS=11 FAIL=0` covers the local `2 x 2` algebra exhaustively (parts 1,
2, 3); the part-4 "current bank misses that slot" reading imports the
bank-span premise flagged by prior feedback.

## Question
On the local one-line `nu_R` model, if a Majorana reopening ever exists,
what is the exact missing object? Is it still a matrix family, or has the
problem already reduced to one canonical source slot?

## Answer
It has already reduced all the way down.

On the doubled `nu_R` line, the charge-`(+2)` adjoint eigenspace is exactly the
one-dimensional slot `E12`. After the local antisymmetry / Nambu completion,
that slot becomes the one-complex-parameter block

`A_M(m) = m J_2`,  with  `J_2 = [[0,1],[-1,0]]`.

The existing local `nu_R` rephasing removes the phase of `m`, so every
future one-generation Majorana reopening on this local line is equivalent
to the unique normal form

`mu J_2`,  with  `mu >= 0`.

So the current Majorana blocker is not a hidden matrix family. It is one new
off-diagonal charge-`2` source amplitude on the doubled `nu_R` line.

## Exact Content

The bounded calculation proves:

1. the charge-`(+2)` eigenspace of the doubled-line adjoint action is exactly
   one-dimensional
2. that eigenspace is the upper-right slot `E12`
3. the paired antisymmetric / Nambu completion is exactly the single-complex
   family `m J_2`
4. local `nu_R` rephasing removes the phase of `m`, leaving the unique real
   normal form `mu J_2`
5. conditional on the scalar-bank span premise, the current scalar
   transfer / response bank still misses precisely that off-diagonal slot

## Consequence

This sharpens the Majorana side of the full-closure frontier.

The sibling boundary analysis shows, conditional on the modeled rank-`1`
support:

- the `nu_R` support is rank `1`
- every framework projected observable on that support is scalar
- the induced Nambu lifts are diagonal and have zero anomalous block

This new theorem closes the remaining geometric ambiguity:

> if Majorana is ever reopened on the local `nu_R` line, the missing object
> is exactly one rephasing-reduced off-diagonal charge-`2` amplitude `mu`.

So the conditional scalar-bank reading does not fail because it leaves a
large unexplored matrix family. It fails because it does not yet generate
the one exact source slot that Majorana would need.

## Dependency perimeter register

The table below separates load-bearing source references from sibling
context. Markdown links are reserved for intended graph dependencies;
plain code-formatted filenames are contextual and should not seed a
dependency edge.

| Source surface | Note | Role |
|---|---|---|
| Anomaly-fixed unique `nu_R` Majorana channel (one-generation) | [`NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`](NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md) | candidate source for uniqueness of `S_unique = nu_R^T C P_R nu_R` |
| Local one-complex-coefficient reduction (canonical block) | [`NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md`](NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md) | candidate source for local Nambu pairing-plane structure |
| Phase removal by `nu_R` rephasing | [`NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md`](NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md) | candidate source for reducing `m J_2` to `mu J_2` with `mu >= 0` |
| Unique source slot | [`NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md`](NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md) | candidate source for uniqueness of the off-diagonal source slot under the local-bilinear assumption |
| `nu_R` transfer-character boundary sibling | `NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY_NOTE.md` | contextual sibling; scalar-character family on the rank-`1` model line |
| Lower-level pairing no-go sibling | `NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md` | contextual sibling; charge-preserving normal-kernel class |
| Charge-`2` primitive reduction parent / cluster anchor | [`NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md`](NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md) | candidate source for charge-zero containment |
| Majorana lane packet | `NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md` | aggregate context, not a theorem authority |
| Scalar-only Nambu-lift bank-span premise | not yet packaged as a theorem-grade note | open missing dependency edge / scope-narrowing target |

The open perimeter is therefore precisely the last table row.
The runner closes parts 1-3 (the local `2 x 2` algebra: charge-`(+2)`
eigenspace dimension, antisymmetric / Nambu completion, rephasing-reduction)
fully and unconditionally. The conditional content lives in the part-4
assertion that the current scalar transfer / response bank lifts only to the
diagonal subspace on the `nu_R` line; the runner illustrates the
one-half of this implication that goes via `J_2`-vs-diagonal-span distance,
but does not derive the *bank span* itself.

## What the runner demonstrates exactly

The companion script
[`scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py`](../scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py)
runs four parts:

- **Part 1 (charge-`2` operator slot, bounded):** the adjoint action
  `ad_Q` on the doubled `nu_R` line has a one-dimensional charge-`(+2)`
  eigenspace, equal exactly to `span(E12)`; `E21` carries charge `-2`.
- **Part 2 (Nambu / antisymmetry completion, bounded):** the
  canonical antisymmetric completion of the charge-`2` slot is exactly
  `m J_2`; every local antisymmetric completion has zero diagonal.
- **Part 3 (local rephasing, bounded):** the local `nu_R` rephasing
  `U = exp(-i alpha) I` acts as `U A U^T` on the pairing block; choosing
  `alpha = arg(m) / 2` sends `m J_2` to `|m| J_2`; the missing source reduces
  to one real amplitude `mu >= 0`.
- **Part 4 (current-bank gap, conditional):** the linear distance
  between `J_2` and the diagonal-block span is positive (about `1.41`); the
  runner reports this as evidence the current scalar bank misses that slot.
  The premise that the scalar transfer / response bank spans only
  the diagonal subspace is imported, not derived — this is the flagged
  perimeter.

The `PASS=11 FAIL=0` includes both the unconditional parts 1-3 and the
conditional part-4 distance check; only the part-4 *interpretation* (current
bank ⟶ diagonal-only) imports the missing dependency edge.

## Repair path

Two repair routes remain:

1. **Cited authority route.** Provide a theorem-grade note or certificate
   deriving that the current scalar transfer / response Nambu lifts span only
   the diagonal subspace on the `nu_R` line; add it as an explicit
   `deps` entry under this row. The runner content stays unchanged.
2. **Scope-narrowing route.** Restate the claim as "the local `2 x 2`
   primitive reduction" only — i.e. the parts 1-3 content (charge-`(+2)`
   slot, Nambu completion, rephasing-reduction) — and demote the
   current-bank-gap reading of part 4 to a heuristic illustration.

Both routes preserve the runner sha256
`93f3a18f3a93043b04b3f2f80660fd3a28fcfb197e0ac3f4e3d4338c1de3a457` and
leave any current verdict or effective status to independent audit.

## Verification

```bash
python3 scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py
```

Expected: `PASS=11 FAIL=0`. Runner sha256 `93f3a18f...3a457`.
