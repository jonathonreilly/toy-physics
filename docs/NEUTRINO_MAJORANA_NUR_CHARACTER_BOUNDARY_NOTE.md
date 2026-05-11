# Neutrino Majorana `nu_R` Transfer-Character Boundary

**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem
**Date:** 2026-04-16  
**Script:** [`scripts/frontier_neutrino_majorana_nur_character_boundary.py`](../scripts/frontier_neutrino_majorana_nur_character_boundary.py)
**Runner sha256:** `5dbe03a3ec64f1befbb3c01f0b8ab5968d9e6135d2cb159207229851c077ff38`

## Prior feedback perimeter (2026-05-05)

Prior independent feedback identified the rank-`1` `nu_R` support as
the load-bearing boundary for this row: the algebraic closure works once
the `nu_R` line projector is granted, but the restricted packet does not
derive the anomaly-fixed `nu_R` support or its rank-`1` projector from
the framework. The requested repair was a theorem-grade derivation or
cited authority establishing that rank-`1` support.

This rigorization edit only sharpens the boundary. The runner's `PASS=6 FAIL=0`
demonstrates the bounded *algebraic implication* (rank-`1` line → scalar
projection → diagonal Nambu lift), not the *premise* (anomaly-fixed
`nu_R` line is rank `1`).

## Question
On the physical `Cl(3)` on `Z^3` Majorana lane, can the lower-level
transport / transfer / response data on the unique anomaly-fixed `nu_R`
line generate or force a nonzero charge-`2` Majorana pairing law by
themselves?

## Answer
No.

In the runner model, the `nu_R` support is represented by a
one-dimensional line. Given that line, every projected linear observable
on that support is scalar. The transfer/holonomy family on the modeled
`nu_R` line is therefore at most a `U(1)` character family, and its
lower-level response data remain scalar resolvents.

After Nambu doubling, those scalar responses lift only to diagonal `2 x 2`
blocks. Their anomalous off-diagonal block vanishes identically.

Therefore this bounded model does not produce a nonzero Majorana pairing
law on the `nu_R` lane without an additional rank-`1` support derivation.

## Exact Content

The bounded calculation proves:

1. given the modeled rank-`1` `nu_R` projector, the support is rank `1`
2. every projected microscopic operator on that support is exactly of the form
   `lambda P_{nu_R}`
3. the canonical transfer/holonomy data therefore form only a scalar `U(1)`
   character family
4. the induced lower-level responses are scalar resolvents
5. the associated Nambu lifts are diagonal and have zero anomalous block
6. the canonical charge-`2` Majorana primitive is not contained in that scalar
   Nambu-lift span

So the strongest next honest statement is not just "charge-preserving normal
response does not reopen Majorana." It is:

> if the transfer/response family on the `nu_R` line is restricted to the
> modeled scalar rank-`1` line, then it cannot generate the required
> off-diagonal charge-`2` Nambu primitive.

## Consequence

This sharpens the blocker for full framework neutrino closure:

- the missing Dirac/PMNS object is still a nontrivial response law
- the missing Majorana object is now identified more precisely as a genuinely
  new off-diagonal charge-`2` primitive on the Nambu-doubled `nu_R` line

So this bounded model does not merely fail to pick a Majorana amplitude.
It does not generate the correct kind of object on the modeled `nu_R`
line at all.

## Dependency perimeter register

The table below separates load-bearing source references from sibling
context. Markdown links are reserved for intended graph dependencies;
plain code-formatted filenames are contextual and should not seed a
dependency edge.

| Source surface | Note | Role |
|---|---|---|
| Anomaly-fixed unique `nu_R` Majorana channel (one-generation) | [`NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`](NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md) | candidate source for uniqueness of `S_unique = nu_R^T C P_R nu_R` |
| Local one-complex-coefficient reduction (`mu J_2`) | [`NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md`](NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md) | candidate source for the local Nambu pairing-plane structure |
| Charge-`2` primitive sibling | `NEUTRINO_MAJORANA_NUR_CHARGE2_PRIMITIVE_REDUCTION_NOTE.md` | contextual sibling; local `2 x 2` doubled-line algebra |
| Lower-level pairing no-go sibling | `NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md` | contextual sibling; charge-preserving normal-kernel class |
| Majorana lane packet | `NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md` | aggregate context, not a theorem authority |
| Rank-`1` `nu_R` support premise | not yet packaged as a theorem-grade note | open | missing dependency edge |

The open perimeter of this row is therefore precisely the last
table row: the runner hard-codes a one-dimensional `nu_R` projector at index
`15` in a `dim = 16` toy space and verifies the algebraic implication; the
*premise* that the framework's `nu_R` support is rank `1` is not itself
derived in the runner or in any cited theorem authority on this row.

## What the runner demonstrates exactly

The companion script
[`scripts/frontier_neutrino_majorana_nur_character_boundary.py`](../scripts/frontier_neutrino_majorana_nur_character_boundary.py)
verifies, given the hard-coded rank-`1` projector `P` on a `dim = 16` toy
space:

1. `rank(P) = 1`;
2. every `P M P` for `M` drawn from a deterministic `numpy.random.default_rng(1604)`
   ensemble of four `16 x 16` complex matrices is exactly `lambda P` for some
   scalar `lambda` (residual norm below `1e-12`);
3. the canonical framework transfer family on the line is the `U(1)`
   character family `{exp(i theta)}`;
4. for `z = 0.23 - 0.08i`, the scalar resolvent `1 / (1 - z lambda)` lifts to
   diagonal Nambu blocks (anomalous block norm below `1e-12`);
5. the canonical charge-`2` primitive `J_2 = [[0,1],[-1,0]]` has positive
   distance to the diagonal-block span (distance > `1e-6`).

The runner thus demonstrates the bounded *algebraic implication* (rank-`1`
support → scalar projection → diagonal Nambu lift → `J_2` outside that span).
It does **not** derive the rank-`1` `nu_R` support from the framework;
the flagged repair target is exactly that derivation.

## Repair path

Two non-exclusive routes remain:

1. **Cited authority route.** Identify or package a theorem-grade note that
   derives the anomaly-fixed `nu_R` rank-`1` support directly from
   the framework (one-generation matter closure + chirality structure), and
   add it as an explicit `deps` entry under this row. The runner content
   stays unchanged.
2. **Scope-narrowing route.** Restate the load-bearing step as the
   conditional implication "*if* the `nu_R` support is a rank-`1`
   line, *then* every projected framework transfer/response observable is
   scalar and the Nambu lift has zero anomalous block." This matches the
   runner exactly and leaves the rank-`1` derivation as a separately
   targeted upstream row.

Both routes preserve the runner calculation. The current runner sha256 is
`5dbe03a3ec64f1befbb3c01f0b8ab5968d9e6135d2cb159207229851c077ff38`
and leave any current verdict or effective status to independent audit.

## Verification

```bash
python3 scripts/frontier_neutrino_majorana_nur_character_boundary.py
```

Expected: `PASS=6 FAIL=0`. Runner sha256 `5dbe03a3...7ff38`.
