# Quark Endpoint Ratio-Chain Law Audited-Scope Narrowing Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_quark_endpoint_ratio_chain_law.py`](../scripts/frontier_quark_endpoint_ratio_chain_law.py)

## Why this note exists

The 2026-05-05 audit pass on the parent
[`QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md`](QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md)
returned `audited_numerical_match` with the explicit verdict:

> On the live endpoint data,
> `gamma_T(center) / gamma_T(shell)`,
> `gamma_T(shell) / gamma_E(shell)`, and
> `gamma_T(center) / gamma_E(center)` are nearest to the small rational
> candidates `5/6`, `-2`, and `-8/9`. The algebraic multiplication
> from `{5/6, -2, -8/9}` to `15/8` closes, but the ratio candidates
> themselves are selected by numerical proximity to imported live
> endpoint data. The restricted packet does not derive those endpoint
> ratios from the Route-2 tensor observable or first principles.

with re-audit guidance:

> *Re-check whether a future packet includes an independent first-
> principles derivation of `endpoint_readout()` and the exact ratio
> chain from the Route-2 tensor observable.*

This note narrows the parent's audited scope into the explicit
within-scope content the runner does close (the closed-form
chain-multiplication algebra that translates three small-rational
endpoint factors into the chain output `15/8` and downstream
`r_E = 21/4`, `D_E = 21/8`), separated from the open numerical-match
identification of the three input small rationals from live tensor
endpoint data.

This is a bounded scope-narrowing companion of an existing audited
note. It does not add a new axiom, does not add a new repo-wide theory
class, does not propose a status promotion, and does not modify the
parent note's audit ledger row.

## Audited verdict (verbatim, for clarity)

- `audit_status: audited_numerical_match`
- `load_bearing_step_class: G`
- `chain_closes: false`
- `claim_scope` (audited): "Audited whether the provided note and runner
  derive the endpoint ratio chain `{5/6, -2, -8/9}` and its consequences
  `15/8`, `r_E = 21/4`, and `D_E = 21/8` from the restricted packet."

The parent note's `Safe statement` and `Honest endpoint` sections
already record the same boundary in source form. This narrowing
companion isolates the **within-scope content** the audit verdict
accepts as a numerical match and explicitly names the missing
first-principles derivation.

## Narrow within-scope content (what the audited row does close)

Inside the audited bounded scope, the runner verifies the following
closed-form algebraic facts. Each is independent of any claim that
the three input small rationals are themselves derived:

| Audited content | Status |
|---|---|
| Exact chain identity: `gamma_E(center)/gamma_E(shell) = [gamma_E(center)/gamma_T(center)] [gamma_T(center)/gamma_T(shell)] [gamma_T(shell)/gamma_E(shell)]` | audited PASS (parent runner) |
| The T-chain factor `gamma_T(center)/gamma_T(shell)` lies within `0.001%` of the exact-support candidate `5/6`, the same identification already privileged by the partner E-quotient note | audited PASS |
| Inside the controlled rational class, the nearest small rationals to the live endpoint ratios are `5/6`, `-2`, `-8/9` (each within `0.3%` of the live values) | audited PASS as nearest-rational matches (G-class) |
| Closed-form chain multiplication `(-9/8)(5/6)(-2) = 15/8` is exact algebra, verified to `< 1e-12` against the live chain product | audited PASS |
| Conditional on the three nearest-rational identifications, the chain forces `gamma_E(center)/gamma_E(shell) = 15/8`, `r_E = 21/4`, and `D_E = 21/8` exactly, and lands on the same anchored CKM+J branch as the live bounded endpoint solve | audited PASS as conditional algebra |

The within-scope conclusion is conditional: *given* the three
nearest-rational identifications `{5/6, -2, -8/9}`, the closed-form
chain algebra forces `15/8`, `r_E = 21/4`, and `D_E = 21/8` exactly.
This is a non-trivial reduction of the open problem from one
floating bounded number to three named numerical-match identifications,
but it is **not** a derivation of any of the three input small
rationals from framework primitives.

## What the narrow scope does **not** close

The audit verdict and the parent note's own scope-qualifier sections
already flag these explicitly. This companion note records them in
one place for re-audit traceability:

- a retained first-principles derivation of the endpoint
  small-rational chain `{5/6, -2, -8/9}` from the exact Route-2 tensor
  support observable. The current selection inside the controlled
  rational class is a triple of nearest-rational matches to live
  numerical values, not a derivation;
- a retained derivation of the `endpoint_readout()` interface itself.
  The audit verdict explicitly flags the imported live endpoint values
  as the load-bearing input that is not first-principles;
- promotion of the row from `bounded numerical-match` to `retained`.
  The audit verdict's `chain_closure_explanation` explicitly cites the
  missing first-principles derivation as the obstruction to promotion.

A complementary single-quotient companion is recorded in
[`QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md`](QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md);
that note records the same `15/8` candidate as a single nearest-rational
match (without the chain refinement), and is also independently
classified `audited_numerical_match`. Its scope-narrowing companion is
[`QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md`](QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md).

## What would close the open dependency (Path A future work)

Promoting the parent row from `audited_numerical_match` to a retained
theorem-grade derivation would require, per the audit verdict's
repair target:

1. an independent retained theorem deriving the three endpoint
   factors
   `gamma_T(center) / gamma_T(shell) = 5/6`,
   `gamma_T(shell) / gamma_E(shell) = -2`, and
   `gamma_T(center) / gamma_E(center) = -8/9`
   from the exact Route-2 tensor support observable, with explicit
   tensor-stack derivations rather than nearest-rational matches;
2. an updated parent runner that **tests** the three derived values
   (rejecting if they deviate from the derived chain) rather than
   identifies them by nearest-rational scan inside a controlled
   rational class;
3. a retained statement of why the three endpoint factors collapse
   to those specific small rationals in the framework's
   shell/center decomposition, not just to *any* small rationals.

The chain-multiplication algebra `(-9/8)(5/6)(-2) = 15/8` and the
downstream reductions to `r_E = 21/4` and `D_E = 21/8` would then
follow as the existing exact closed-form steps. Until the three
input identifications are independently retained, the row remains a
bounded numerical-match support note at the audited scope.

## Dependencies

- [`QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md`](QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md)
  for the parent audited bounded note.
- [`QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md`](QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md)
  for the complementary single-quotient form (independently audited
  at the same numerical-match grade).

These are imported authorities for a bounded scope-narrowing companion
note. The row remains unaudited until the independent audit lane
reviews this companion, its dependencies, and the runner.

## Boundaries

This companion note does **not**:

- modify the parent note's audit-ledger row;
- promote the parent's `audit_status` from `audited_numerical_match`;
- derive any of `5/6`, `-2`, or `-8/9` from framework primitives;
- claim that the chain-multiplication algebra alone constitutes a
  theorem-grade promotion of the parent row;
- extend the audited scope beyond what the parent already declares.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_endpoint_ratio_chain_law.py
```

Expected (unchanged from parent):

```text
PASS=14 FAIL=0
```

The runner is the same one cited by the parent note. This narrowing
companion does not introduce a new runner because the within-scope
conditional algebra is already exercised. The new content is the
explicit scope-narrowing recording of what the audit verdict accepts
as within-scope numerical-match content versus what remains open as
the missing first-principles derivation.

```yaml
claim_id: quark_endpoint_ratio_chain_law_audited_scope_narrow_bounded_note_2026-05-10
note_path: docs/QUARK_ENDPOINT_RATIO_CHAIN_LAW_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md
runner_path: scripts/frontier_quark_endpoint_ratio_chain_law.py
proposed_claim_type: bounded_theorem
deps:
  - quark_endpoint_ratio_chain_law_note_2026-04-19
audit_authority: independent audit lane only
```
