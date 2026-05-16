# SCIENCE_FIX_DECLINED — shapiro_static_discriminator_note

**Date:** 2026-05-16
**Worktree branch:** `claude/science-fix/shapiro-static-discriminator-note-2026-05-16-b3`
**Claim:** `shapiro_static_discriminator_note`
**Prompt category:** `audited_failed` (Class A, descendants: 307)

## Self-screen finding

The claim is already re-audited clean in the current ledger snapshot. The
prompt cites an older `audited_failed` verdict that has since been superseded.

### Current ledger state for `shapiro_static_discriminator_note`

From `docs/audit/data/audit_ledger.json` at worktree HEAD:

- `audit_status`: `audited_clean`
- `intrinsic_status`: `retained_no_go`
- `effective_status`: `retained_no_go`
- `claim_type`: `no_go` (re-classified from the original `bounded_theorem`)
- `audit_date`: `2026-05-10T13:12:41.723653+00:00`
- `auditor_family`: `codex-gpt-5.5`
- `auditor_confidence`: `high`

### Re-audit verdict_rationale (2026-05-10, current)

> The scoped no-go closes because the supplied runner contains an explicit
> static-cone construction that is identical to the purported causal cone
> field for matching c, defeating uniqueness of the detector-line phase lag
> within this model. No cited upstream authority is needed for that equality.
> The timeout prevents validating the displayed numeric table and the
> static-scheduling near-flat values, but it is not needed for the
> static-cone mimic boundary that carries the no-go.

### Re-audit claim_scope (current)

> Within the supplied runner's discrete Shapiro model, detector-line phase
> lag is not a unique causal-propagation discriminator because the static
> cone proxy uses the same field construction as the causal cone for each c.

### Audit history (chronological)

1. 2026-04-27: `audited_clean` (codex-gpt-5)
2. 2026-05-03: `audited_conditional` (codex-gpt-5)
3. **2026-05-05: `audited_failed` (codex-gpt-5.5)** — the verdict the prompt cites
4. **2026-05-10: `audited_clean` (codex-gpt-5.5)** — current effective state

## Why the 2026-05-10 re-audit closes the same concern the 2026-05-05 audit raised

The 2026-05-05 failed verdict objected:

> The exact static-cone mimic is supported only because the runner's causal
> and static-cone field builders are algebraically identical; no independent
> causal propagation delay is actually computed in the causal branch.

The 2026-05-10 clean re-audit accepts the same algebraic observation, but
re-frames the claim accordingly:

- The claim's role was retagged from `bounded_theorem` (a positive uniqueness
  result) to `no_go` (a uniqueness-failure result). The intrinsic status
  became `retained_no_go`.
- Under the no-go framing, the algebraic identity between the runner's
  causal and static-cone field builders is *itself* the load-bearing
  evidence: it shows that within this discrete model, a static cone field
  can be constructed to be field-equal to the causal cone for each c, so
  the detector-line phase lag cannot uniquely discriminate causal-vs-static
  within this model.
- The retagged `claim_scope` is explicit that the result is restricted to
  "within the supplied runner's discrete Shapiro model," i.e. it does not
  generalize to any continuum or independent causal-propagation theory.

The 2026-05-05 timeout concern about the static-scheduling near-flat table
is also addressed: the current cached log
(`logs/runner-cache/shapiro_static_discriminator.txt`) shows
`exit_code: 0`, `elapsed_sec: 398.81`, `status: ok`, with the
static-schedule curve `+0.0446, +0.0445, +0.0446, +0.0450` recorded. The
2026-05-10 re-audit also notes the no-go conclusion does not require the
static-scheduling values, only the static-cone mimic equality.

The current `notes_for_re_audit_if_any` recorded by the 2026-05-10 auditor
is the only forward-looking caveat:

> A completed runner or cached log should still be checked before citing
> the reported numeric means or the static-scheduling non-match as audited.

That caveat does not block the current `audited_clean` status; it scopes
which downstream uses of the table are themselves audited. The cached
runner output is now present and matches the note's printed means to four
decimals, so even that residual caveat is materially addressed.

## Why no further single-row repair is appropriate

The candidate repair routes were considered against the current ledger
state, not against the superseded 2026-05-05 verdict:

1. **Rewrite the algebra.** Not appropriate. The algebraic identity between
   the causal and static-cone field builders is precisely what carries the
   no-go under the current `claim_type: no_go` framing. Removing the
   identity would weaken, not strengthen, the load-bearing step.

2. **Narrow the claim.** Already done at the 2026-05-10 re-audit: the
   `claim_type` was changed from `bounded_theorem` to `no_go`, the
   `claim_scope` was tightened to "within the supplied runner's discrete
   Shapiro model," and the `intrinsic_status` was set to `retained_no_go`.
   Further narrowing would either drop the load-bearing equality or
   misrepresent it.

3. **Update numbers to match the runner.** Already in sync. The note's
   printed means (`+0.0372, +0.0446, +0.0569, +0.0662` for causal and
   matching static-cone; `+0.0446, +0.0445, +0.0446, +0.0450` for
   static-scheduling) match the cached runner output to four decimals.

There is no remaining single-row repair the prompt's `audited_failed`
framing would unlock that is not already realized in the current
`audited_clean` row.

## What is and is not in this PR

This PR contains only this `SCIENCE_FIX_DECLINED.md` file at the worktree
root. No `docs/`, `scripts/`, or `docs/audit/**` files are touched. No
audit verdict is claimed and no audit-data file is modified. The current
clean audit status and the load-bearing equality it rests on are
unchanged.

## Recommended next action

None at this row. The claim is in `audited_clean` / `retained_no_go` state
with a current auditor (`codex-gpt-5.5`, high confidence) verdict. The
prompt-generator pipeline appears to be referencing the 2026-05-05
superseded `audited_failed` verdict rather than the 2026-05-10 current
`audited_clean` verdict; that is a prompt-generator issue, not a claim
issue.
