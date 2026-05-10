# Neutrino Majorana `nu_R` Transfer-Character Boundary

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Script:** [`scripts/frontier_neutrino_majorana_nur_character_boundary.py`](../scripts/frontier_neutrino_majorana_nur_character_boundary.py)
**Runner sha256:** `d5887c148bcee7946e0bde0a4301542c3f6ce964ab617f7c98d5312b79816ade`

## Audit-conditional perimeter (2026-05-05)

The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and load-bearing step
class `A`. The audit chain-closure explanation is exact:

> "The rank-1-line-to-scalar-response-to-diagonal-Nambu conclusion is a valid
> algebraic closure once the `nu_R` line projector is granted. The restricted
> packet does not derive the anomaly-fixed retained `nu_R` support or its
> rank-1 projector from the sole axiom; the runner hard-codes that
> projector."

The audit-stated repair target is verbatim:

> "missing_dependency_edge: provide a retained derivation or cited retained
> authority establishing the anomaly-fixed retained `nu_R` rank-1 support
> from the sole axiom."

This rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status. The runner's `PASS=6 FAIL=0`
demonstrates the bounded *algebraic implication* (rank-`1` line → scalar
projection → diagonal Nambu lift), not the *premise* (anomaly-fixed retained
`nu_R` line is rank `1`).

## Question
On the sole-axiom retained Majorana lane, can the lower-level transport /
transfer / response data on the unique anomaly-fixed `nu_R` line generate or
force a nonzero charge-`2` Majorana pairing law by themselves?

## Answer
No.

On the current exact bank, the retained `nu_R` support is a one-dimensional
line. That forces every projected linear observable on that support to be
scalar. So the sole-axiom transfer/holonomy family on `nu_R` is at most a
`U(1)` character family, and its lower-level response data remain scalar
resolvents.

After Nambu doubling, those scalar responses lift only to diagonal `2 x 2`
blocks. Their anomalous off-diagonal block vanishes identically.

Therefore the current sole-axiom bank still does not produce a nonzero
Majorana pairing law on the retained `nu_R` lane.

## Exact Content

The theorem proves:

1. the anomaly-fixed retained `nu_R` support is rank `1`
2. every projected microscopic operator on that support is exactly of the form
   `lambda P_{nu_R}`
3. the canonical transfer/holonomy data therefore form only a scalar `U(1)`
   character family
4. the induced lower-level responses are scalar resolvents
5. the associated Nambu lifts are diagonal and have zero anomalous block
6. the canonical charge-`2` Majorana primitive is not contained in that scalar
   Nambu-lift span

So the strongest next honest statement is not just “charge-preserving normal
response does not reopen Majorana.” It is:

> the whole sole-axiom transfer/response family on the retained `nu_R` line is
> scalar, so it cannot generate the required off-diagonal charge-`2` Nambu
> primitive.

## Consequence

This sharpens the blocker for full sole-axiom neutrino closure:

- the missing Dirac/PMNS object is still a nontrivial retained response law
- the missing Majorana object is now identified more precisely as a genuinely
  new off-diagonal charge-`2` primitive on the Nambu-doubled `nu_R` line

So the current exact bank does not merely fail to pick a Majorana amplitude. It
does not generate the correct kind of object on the retained `nu_R` line at
all.

## Cited authority chain (audit-conditional perimeter register)

The audit ledger entry for this row records `deps = []`, so the conditional
perimeter is the *unstated* citation surface. The table below registers the
neighbouring cluster authorities the note implicitly leans on, together with
their current ledger statuses, to make the conditional perimeter explicit.

| Cited authority | Note | Effective status (2026-05-10) | Conditional on |
|---|---|---|---|
| Anomaly-fixed unique `nu_R` Majorana channel (one-generation) | [`NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`](NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md) | unaudited | uniqueness of `S_unique = nu_R^T C P_R nu_R` |
| Local one-complex-coefficient reduction (`mu J_2`) | [`NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md`](NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md) | unaudited | local Nambu pairing-plane structure |
| Charge-`2` primitive sibling (this cluster) | [`NEUTRINO_MAJORANA_NUR_CHARGE2_PRIMITIVE_REDUCTION_NOTE.md`](NEUTRINO_MAJORANA_NUR_CHARGE2_PRIMITIVE_REDUCTION_NOTE.md) | `audited_conditional` | local `2 x 2` doubled-line algebra |
| Lower-level pairing no-go (this cluster) | [`NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md`](NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md) | `audited_conditional` | charge-preserving normal-kernel class on the retained lane |
| Retained Majorana lane packet | [`NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md`](NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md) | unaudited | aggregate listing of the cluster |
| Retained `nu_R` rank-`1` support (the audit-flagged premise) | not yet packaged as a retained-grade note | not retained | the missing dependency edge the audit verdict requires |

The audit-conditional perimeter of this row is therefore precisely the last
table row: the runner hard-codes a one-dimensional `nu_R` projector at index
`15` in a `dim = 16` toy space and verifies the algebraic implication; the
*premise* that the framework's retained `nu_R` support is rank `1` is not
itself derived in the runner or in any cited retained authority on this row.

## What the runner demonstrates exactly

The companion script
[`scripts/frontier_neutrino_majorana_nur_character_boundary.py`](../scripts/frontier_neutrino_majorana_nur_character_boundary.py)
verifies, given the hard-coded rank-`1` projector `P` on a `dim = 16` toy
space:

1. `rank(P) = 1`;
2. every `P M P` for `M` drawn from a deterministic `numpy.random.default_rng(1604)`
   ensemble of four `16 x 16` complex matrices is exactly `lambda P` for some
   scalar `lambda` (residual norm below `1e-12`);
3. the canonical sole-axiom transfer family on the line is the `U(1)`
   character family `{exp(i theta)}`;
4. for `z = 0.23 - 0.08i`, the scalar resolvent `1 / (1 - z lambda)` lifts to
   diagonal Nambu blocks (anomalous block norm below `1e-12`);
5. the canonical charge-`2` primitive `J_2 = [[0,1],[-1,0]]` has positive
   distance to the diagonal-block span (distance > `1e-6`).

The runner thus demonstrates the bounded *algebraic implication* (rank-`1`
support → scalar projection → diagonal Nambu lift → `J_2` outside that span).
It does **not** derive the rank-`1` `nu_R` support from the framework axiom;
the audit-flagged repair target is exactly that derivation.

## Audit-stated repair path

The audit's `notes_for_re_audit_if_any` is a single dependency-edge ask. Two
non-exclusive routes match it:

1. **Cited authority route.** Identify or package a retained-grade note that
   derives the anomaly-fixed retained `nu_R` rank-`1` support directly from
   the sole axiom (one-generation matter closure + chirality structure), and
   add it as an explicit `deps` entry under this row. The runner content
   stays unchanged.
2. **Scope-narrowing route.** Restate the load-bearing step as the
   conditional implication "*if* the retained `nu_R` support is a rank-`1`
   line, *then* every projected sole-axiom transfer/response observable is
   scalar and the Nambu lift has zero anomalous block." This matches the
   runner exactly and leaves the rank-`1` derivation as a separately
   targeted upstream row.

Both routes preserve the runner sha256 `d5887c148bcee7946e0bde0a4301542c3f6ce964ab617f7c98d5312b79816ade`
and respect the ledger's `audit_status = audited_conditional`.

## Verification

```bash
python3 scripts/frontier_neutrino_majorana_nur_character_boundary.py
```

Expected: `PASS=6 FAIL=0`. Runner sha256 `d5887c14...16ade`.
