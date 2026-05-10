# Quark E-Channel Endpoint Quotient Law Audited-Scope Narrowing Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_quark_e_channel_endpoint_quotient_law.py`](../scripts/frontier_quark_e_channel_endpoint_quotient_law.py)

## Why this note exists

The 2026-05-05 audit pass on the parent
[`QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md`](QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md)
returned `audited_numerical_match` with the explicit verdict:

> Inside the controlled low-rational endpoint class, the live E-channel
> shell/center quotient is best rationalized by 15/8, implying
> `r_E = 21/4` and `D_E = 21/8` under the shell-multiplicity bridge.
> The algebra from `q_E = 15/8` to `r_E = 21/4` closes, but the
> load-bearing identification `q_E = 15/8` is only a nearest-rational
> match to an imported live endpoint value. The packet does not derive
> the endpoint quotient or the shell-multiplicity bridge
> `a_T / a_E = -2` from retained first-principles tensor machinery.

with re-audit guidance:

> *missing_bridge_theorem: provide a retained first-principles
> derivation of `gamma_E(center) / gamma_E(shell) = 15/8`, and
> separately close the `a_T / a_E = -2` bridge before promoting the
> denominator law.*

This note narrows the parent's audited scope into the explicit
within-scope content the runner does close (the closed-form algebra
that translates a small-rational endpoint quotient candidate into a
ratio law and an anchored denominator candidate), separated from the
two missing bridge theorems that would be needed to promote the row
from numerical-match grade to a derivation.

This is a bounded scope-narrowing companion of an existing audited
note. It does not add a new axiom, does not add a new repo-wide theory
class, does not propose a status promotion, and does not modify the
parent note's audit ledger row.

## Audited verdict (verbatim, for clarity)

- `audit_status: audited_numerical_match`
- `load_bearing_step_class: G`
- `chain_closes: false`
- `claim_scope` (audited): "Audited the bounded endpoint-rationalization
  claim that the live E-channel quotient near 1.876246 selects 15/8 in
  a numerator <= 96, denominator <= 32 rational scan, yielding
  `r_E = 21/4` and conditionally `D_E = 21/8`."

The parent note's `Safe statement` and `Honest endpoint` sections
already record the same boundary in source form. This narrowing
companion isolates the **within-scope content** the audit verdict
accepts as a numerical match, and explicitly names the two missing
bridge theorems that re-auditing this row would expect to find
retained.

## Narrow within-scope content (what the audited row does close)

Inside the audited bounded scope, the runner verifies the following
closed-form algebraic facts. Each is independent of any claim that the
selected small rational `q_E = 15/8` is itself derived:

| Audited content | Status |
|---|---|
| Exact endpoint identity `r_E = 6 (gamma_E(center)/gamma_E(shell) - 1)` | audited PASS (parent runner) |
| Exact endpoint identity `r_T = 6 (gamma_T(center)/gamma_T(shell) - 1)` | audited PASS |
| The live T-channel quotient `gamma_T(center)/gamma_T(shell)` lies within `0.001%` of the exact-support candidate `5/6`, implying `r_T = -1` exactly under that promotion | audited PASS |
| The closed-form chain `q_E -> r_E -> D_E` is exact algebra: under `r_T = -1` and the shell-multiplicity bridge `a_T / a_E = -2`, `D_E = r_E / 2` exactly | audited PASS (parent runner) |
| Inside the controlled rational class `numerator <= 96, denominator <= 32`, the nearest small rational to the live `gamma_E(center)/gamma_E(shell) = 1.876246...` is `15/8 = 1.875`, gap `~ 0.066%` | audited PASS as a nearest-rational match (G-class) |
| Conditional on `q_E = 15/8` and the shell-multiplicity bridge, `r_E = 21/4` and `D_E = 21/8` follow from the closed-form algebra, and the implied amplitude lands on the same anchored CKM+J branch as the live bounded endpoint solve | audited PASS as conditional algebra |

The within-scope conclusion is conditional: *given* the nearest-rational
identification `q_E = 15/8` and the shell-multiplicity bridge
`a_T / a_E = -2`, the closed-form algebra forces `r_E = 21/4` and
`D_E = 21/8` exactly. This is a non-trivial reduction of the open
problem to two named numerical-match identifications, but it is
**not** a derivation of either identification from framework primitives.

## What the narrow scope does **not** close

The audit verdict and the parent note's own scope-qualifier sections
already flag these explicitly. This companion note records them in
one place for re-audit traceability:

- a retained first-principles derivation of
  `gamma_E(center) / gamma_E(shell) = 15/8` from the Route-2 tensor
  support observable. The current selection inside the controlled
  rational class is a nearest-rational match to the live numerical
  value `1.876246...`, not a derivation;
- a retained first-principles derivation of the shell-multiplicity
  bridge `a_T / a_E = -2`. The current identification matches the
  live shell-intercept ratio at `~ 0.27%` numerical gap inside the
  same rational class, again as a nearest-rational match;
- promotion of the row from `bounded numerical-match` to
  `retained`. The audit verdict's
  `chain_closure_explanation` explicitly cites the two missing
  bridge theorems above as the obstruction to promotion.

A complementary chain-form companion is recorded in
[`QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md`](QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md);
that note refines the same `15/8` candidate into a three-factor chain
`{5/6, -2, -8/9}`, and is also independently classified
`audited_numerical_match`. Its scope-narrowing companion is
[`QUARK_ENDPOINT_RATIO_CHAIN_LAW_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md`](QUARK_ENDPOINT_RATIO_CHAIN_LAW_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md).

## What would close the open dependency (Path A future work)

Promoting the parent row from `audited_numerical_match` to a retained
theorem-grade derivation would require, per the audit verdict's
repair target, **either** of the following two bridge theorems
landing as retained, with a corresponding update to the parent runner
that **tests** the derived value rather than identifies it by
nearest-rational scan:

1. **Endpoint-quotient bridge:** an independent retained theorem
   deriving `gamma_E(center) / gamma_E(shell) = 15/8` from the exact
   Route-2 tensor support observable, including its shell/center
   readout convention. The current parent runner identifies `15/8` as
   the nearest small rational inside `numerator <= 96`,
   `denominator <= 32`; a derived theorem would supply `15/8` from
   tensor-stack algebra rather than from a low-rational scan.

2. **Shell-multiplicity bridge:** an independent retained theorem
   promoting `a_T / a_E = -2` from bounded shell multiplicity to
   theorem status, deriving the integer `-2` from the underlying
   shell-counting algebra rather than from rationalization of the
   live `|a_T / a_E|` numerical value.

Each of these is independently bounded today; closing either would
narrow the open derivation problem, and closing both would promote
the combined `D_E = 21/8` chain from numerical-match grade to a
derivation. This companion note does not propose either bridge
theorem; it documents the within-scope content that is closed today
so subsequent work can target the named bridges directly.

## Dependencies

- [`QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md`](QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md)
  for the parent audited bounded note.
- [`QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md`](QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md)
  for the complementary three-factor chain refinement (independently
  audited at the same numerical-match grade).

These are imported authorities for a bounded scope-narrowing companion
note. The row remains unaudited until the independent audit lane
reviews this companion, its dependencies, and the runner.

## Boundaries

This companion note does **not**:

- modify the parent note's audit-ledger row;
- promote the parent's `audit_status` from `audited_numerical_match`;
- derive `gamma_E(center) / gamma_E(shell) = 15/8` from framework
  primitives;
- derive the shell-multiplicity bridge `a_T / a_E = -2` from framework
  primitives;
- claim that the closed-form `q_E -> r_E -> D_E` reduction is itself
  a theorem-grade promotion of the parent row;
- extend the audited scope beyond what the parent already declares.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_e_channel_endpoint_quotient_law.py
```

Expected (unchanged from parent):

```text
PASS=16 FAIL=0
```

The runner is the same one cited by the parent note. This narrowing
companion does not introduce a new runner because the within-scope
conditional algebra is already exercised. The new content is the
explicit scope-narrowing recording of what the audit verdict accepts
as within-scope numerical-match content versus what remains open as
two named bridge theorems.

```yaml
claim_id: quark_e_channel_endpoint_quotient_law_audited_scope_narrow_bounded_note_2026-05-10
note_path: docs/QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md
runner_path: scripts/frontier_quark_e_channel_endpoint_quotient_law.py
proposed_claim_type: bounded_theorem
deps:
  - quark_e_channel_endpoint_quotient_law_note_2026-04-19
audit_authority: independent audit lane only
```
