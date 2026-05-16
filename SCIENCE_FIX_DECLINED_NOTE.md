# science-fix declined: dm_selector_first_shoulder_exit_threshold_support_note_2026-04-21

**Claim id:** `dm_selector_first_shoulder_exit_threshold_support_note_2026-04-21`
**Source note:** `docs/DM_SELECTOR_FIRST_SHOULDER_EXIT_THRESHOLD_SUPPORT_NOTE_2026-04-21.md`
**Runner:** `scripts/frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21.py`
**Date:** 2026-05-16
**Decision:** decline — the open-gate scope is already `audited_clean`
with two-auditor fresh-context cross-confirmation against a critical-
leverage snapshot, and the only post-audit edit to the source note
narrows the scope further (it adds the explicit "no physical threshold
law is claimed" disclaimer plus algebraic detail). The current
`audit_status: unaudited` is a re-audit eligibility flag triggered by
the note-hash drift, not a re-opened scope failure.

## PROMPT.md target

- `audit_status`: `unaudited` (current row), but PROMPT body cites the
  `audited_clean` second-audit snapshot
- `claim_type`: `open_gate`
- `load_bearing_step_class`: A
- `claim_scope` (from PROMPT, second-audit snapshot): "The exact
  threshold-volume family contains a unique earliest middle-branch
  breakpoint tau_b,min at recovered lift 0, this breakpoint lies inside
  the prior stabilization window, and evaluating the field there
  selects lift 0; no physical threshold law is claimed."

The auditor-quoted load-bearing step in the PROMPT:

> For each recovered lift, tau_b(i) = log(1 + b_i); on the recovered
> bank the minimum is unique, belongs to lift 0, lies inside the
> stabilization window, and V_tau at that breakpoint makes lift 0 the
> unique minimizer.

And the auditor's verdict rationale:

> The load-bearing step is an algebraic check over existing
> recovered-bank inputs ... The cached runner completes with PASS=11
> FAIL=0 and its substantive checks match the note's reported tau_b
> values and selector values. The runner does not derive a physical
> law, but the source note does not claim one; it states the remaining
> selector-side burden explicitly. Residual risk is dependency-grade
> rather than scope failure, but under the audited open-gate scope the
> chain closes.

So the auditor already affirmed chain closure at the stated open-gate
scope. The PROMPT goal ("close the chain so a re-audit of this same
note can land audited_clean at retained-grade") describes the state
that already exists in `previous_audits`, not a new requirement.

## Ledger / cross-confirmation history (from `docs/audit/data/audit_ledger.json`)

`rows["dm_selector_first_shoulder_exit_threshold_support_note_2026-04-21"].previous_audits`
contains two prior audits:

1. **2026-05-02** — `claude-opus-4.7-1m`, fresh_context.
   `audited_clean`, `chain_closes: true`, bounded_theorem framing on
   the same algebraic claim (PASS=11 FAIL=0 expected from the runner).
   Invalidated by `criticality_increased:leaf->critical`, not by a
   scope error.
2. **2026-05-05** — `codex-fresh-second-dm_selector_first_shoulder_exit_threshold_support_note-20260505`,
   fresh_context, against the criticality=critical, transitive
   descendants=287 snapshot. `audited_clean`, `chain_closes: true`,
   class A. `cross_confirmation.status: "confirmed"` against the
   immediately-prior fresh_context first-audit by the sibling auditor
   (`codex-fresh-first-...-20260505`). Both audits agreed on the
   open_gate scope wording, the class-A grading, and the
   `audited_clean` verdict.

The second audit was therefore the regime that matches the current
ledger row's criticality (critical, descendants now 283), and it ruled
clean with explicit cross-confirmation.

## Note-hash drift since the cross-confirmed audit

- Audit-2 archived against `note_hash =
  27974cf3d96605b26780884d27790446e927cdb5282711864c3e1b895b8cd745`.
- Current note SHA-256 (this worktree, equal to the live ledger
  `note_hash`) is
  `5ed33df184be15fff3b1847497c16fc22e2948a64fb996aace768651c8b57f5d`.

`git log` shows exactly one substantive change to the note between
those hashes: commit `0e9873624 review-loop: land DM selector
shoulder support` (2026-05-06). The diff is purely additive and
*narrows* the scope toward the open-gate framing the auditors already
ruled clean:

- Adds the line "This note does not assert a physical threshold law.
  Its closed claim is the algebraic open-gate statement: on the
  recovered bank, the first middle-branch breakpoint of the exact
  threshold-volume family is unique, belongs to lift `0`, lies in the
  previously certified stabilization window, and selects lift `0`
  when the exact field is evaluated there."
- Adds the explicit recovered-bank `(a, b, g)` parameter table for the
  five lifts that the runner already loads from
  `dm_selector_branch_support.recovered_bank`.
- Adds the strict `tau_b,min - tau_star` and
  `tau_zero(next) - tau_b,min` margins.
- Adds the symbolic two-piece evaluation of `V_tau_b,min(H_0) =
  (a_0 - b_0)/(a_0 - g_0) = 0.724251528642812` on the `c = b_0` branch
  boundary.
- Adds the strict minimum competitor gap
  `min_{j>0} V_tau_b,min(H_j) - V_tau_b,min(H_0) = 0.146091270049196 > 0`.

None of these additions promotes the claim to a physical threshold law,
none introduces a new admission, and none alters the runner contract.
The change strengthens the open-gate scope rather than reopening it.

## Runner reproduction (this worktree)

`PYTHONPATH=scripts python3 scripts/frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21.py`
reproduces:

```
SUMMARY: PASS=11 FAIL=0
```

against the current note hash, matching the cached
`logs/runner-cache/frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21.txt`
(`exit_code: 0`, `status: ok`, `PASS=11 FAIL=0`).

The eleven substantive checks the runner reports are exactly the
algebraic and bookkeeping facts the two prior auditors used to close
the chain:

- preferred recovered lift identity check
- `tau_b(i) = log(1+b_i)` finite and positive on all five lifts
- uniqueness of the minimum at lift 0 with strict tau-margin
- `tau_star` recorded by the stabilization theorem note
- `tau_b,min > tau_star` strict
- `tau_b,min < tau_zero(next)` strict
- `argmin_i V_tau_b,min(H_i) = {0}` with strict gap to all competitors
- the open-gate framing of the older nonrealization note still in
  place
- the scope-narrowing wording itself (no promotion)
- the remaining selector burden remains the physical-threshold-law
  derivation

## Why "open_gate" is the correct stable verdict, not a fix target

The note's own `Boundary` section is explicit:

> This is a support theorem only. It does **not** prove that the
> physical threshold law must be `tau_phys = tau_b,min`. It proves
> only that `tau_b,min` is now the cleanest intrinsic selector
> candidate already present on the exact family.

And the `Consequence` section names what the open gate is:

> derive why the physical threshold law is the earliest middle-branch
> breakpoint `tau_b,min`, or else derive a stronger microscopic
> selector law that bypasses the threshold-volume family.

The science-fix prompt instructs: "open_gate repair = close the gate
substantively (write the missing theorem) OR document why it remains
open as a real research question." This note already does the second
option — and the runner certifies the algebraic boundary of what is
closed vs what is left open. The missing physical-threshold-law
derivation is a genuine open research question (it requires
microscopic dynamical input to the threshold-volume family that the
recovered bank alone does not supply), not a packet-completeness gap
that can be repaired by an algebraic edit to this note.

Closing the open gate substantively from inside this worktree would
require:

1. A new physical principle picking out `tau_b,min` from the
   stabilization window (none is in scope of the recovered-bank
   inputs), or
2. A stronger microscopic selector that bypasses the threshold-volume
   family entirely (out of scope of this note, would have its own
   theorem and runner).

Either path is a new theorem note + runner pair, not a re-edit of the
existing support theorem. Producing a fresh theorem here without the
microscopic input would either invent a retained-grade premise (a
hard rule violation) or duplicate the support theorem under a new
title without adding content.

## What this PR contains

Only this `SCIENCE_FIX_DECLINED_NOTE.md`. No edits to
`docs/DM_SELECTOR_FIRST_SHOULDER_EXIT_THRESHOLD_SUPPORT_NOTE_2026-04-21.md`,
no edits to the runner, no edits to cached runner output, no edits to
audit-data or audit-docs, no edits to publication. Reviewers can
confirm by inspecting the diff: a single new file at repo root.

## Honest assessment

Decline — the prompt targets a row whose open-gate scope has already
been cross-confirmed `audited_clean` at the current criticality regime,
and whose only post-audit edit narrows the scope further. The current
`unaudited` flag is a re-audit eligibility marker driven by note-hash
drift, not by a reopened scope question. The correct next step is a
fresh re-audit pass on the existing PASS=11 FAIL=0 evidence, not a new
derivation attempt that would either invent a premise or duplicate the
support theorem.
