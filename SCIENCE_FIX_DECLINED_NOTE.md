# science-fix declined: lensing_deflection_note

**Claim id:** `lensing_deflection_note`
**Source note:** `docs/LENSING_DEFLECTION_NOTE.md`
**Date:** 2026-05-16
**Decision:** decline — repair target is already satisfied on `origin/main`.

## PROMPT.md verdict (stale snapshot)

The science-fix prompt was generated against an earlier audit snapshot
that reported:

- `audit_status: audited_conditional`
- `load_bearing_step_class: C`
- `category: runner_artifact_issue`

with the repair target:

> Provide the fine H=0.25 single-b runner outputs plus the combined L+
> analysis runner/source, or a cached certificate for the H=0.25
> b ∈ {3,4,5,6} slope fit.

## Current ledger state on `origin/main`

`docs/audit/data/audit_ledger.json` (current row, last audit
2026-05-10T14:26:26Z) records:

- `audit_status: audited_clean`
- `effective_status: retained_bounded`
- `intrinsic_status: retained_bounded`
- `claim_type: bounded_theorem`
- `load_bearing_step_class: A`
- `cross_confirmation.status: confirmed` — both `first_audit` and
  `second_audit` independent fresh-context auditors landed
  `audited_clean` at `load_bearing_step_class: A`.
- `claim_scope`: "Bounded four-point log-log fit: for the supplied
  H=0.25 cached values at b ∈ {3,4,5,6}, kubo_true has slope -1.433549
  and R² 0.998404, with |slope+1| > 0.1."
- `runner_hash` matches the SHA-256 of
  `scripts/lensing_deflection_h025_slope_fit_certificate.py`.

`docs/audit/data/audit_queue.json` has no own-row entry for
`lensing_deflection_note` — it is not pending re-audit.

`docs/audit/data/runner_classification.json` lists the primary runner
for the claim as
`scripts/lensing_deflection_h025_slope_fit_certificate.py`
with `dominant_class: A` and zero class-C/D assertions.

## Artifact-chain verification (this worktree)

The certificate the auditor's repair target asked for already exists,
is registered, and is framework-faithful:

- `scripts/lensing_deflection_fine_single.py` — single-b H=0.25 runner
  (per-b OOM workaround documented in the note).
- `scripts/lensing_deflection_lane_lplus.py` — combined L+ analysis
  runner.
- `scripts/lensing_deflection_h025_slope_fit_certificate.py` —
  bounded certificate runner: parses the cached fine-asymptotic log,
  cross-checks against the combined-L+ DATA dict, recomputes the
  log-log slope/R², asserts `|slope - (-1)| > 0.1`, and *live-replays*
  the fine-single runner at the cheap H=0.5 b=3 reference point
  (`kubo_true = +7.061910`, `dM = +0.034642`) so the certificate
  cannot be reduced to constant-printing.
- `logs/2026-04-07-lensing-fine-asymptotic.txt` — checked-in per-b
  H=0.25 outputs for b ∈ {3,4,5,6}.
- `logs/runner-cache/lensing_deflection_h025_slope_fit_certificate.txt`
  — cached `PASS=24/24` runner output, sha-pinned to the runner.
- `outputs/lensing_deflection_h025_slope_fit_certificate.json` —
  structured slope-fit certificate output.

Local re-execution of the certificate runner in this worktree
reproduces `PASS=24/24` / `STATUS: BOUNDED H=0.25 SLOPE-FIT
CERTIFICATE PASS`, with the H=0.5 b=3 live replay matching the
reference values to the documented tolerances. Stage-3 fit:
`kubo_slope = -1.433549`, `kubo_R² = 0.998404`,
`|slope - (-1)| = 0.4335 > 0.1`.

## Why this is a decline rather than a no-op fix

The auditor's repair target is *to supply the certificate*. The
certificate is supplied, registered as the claim's primary runner,
sha-pinned in the ledger, cached, and cross-confirmed clean by two
independent fresh-context audits. Any further "repair" in this
worktree would either:

1. Touch the immutable audit-data files (forbidden by the
   science-fix worktree rules), or
2. Re-edit the note to repeat what it already says (`claim_scope`
   already matches the certified bounded statement; the note's
   "Bottom line" already downgrades the original 1/b headline to the
   non-standard ≈ -1.43 power law).

The remaining open items the note itself enumerates (continuum-stable
exponent, family portability, large-b asymptotics, full
deflection-angle measurement) are explicitly listed under
"**What this does NOT establish**" and are out of scope for the
bounded retained claim. Closing them is research-grade work, not a
runner-artifact repair.

## What this PR contains

Only this note. No source, runner, log, or audit-data file is
modified. Reviewers should confirm by inspecting
`docs/audit/data/audit_ledger.json` on `origin/main` for the current
`lensing_deflection_note` row and verifying the
`audited_clean / retained_bounded / class A` snapshot above is still
the live state.

## Honest assessment

Partial — in the precise sense that the science-fix queue row should
be retired against the already-landed certificate rather than acted
on with new code. The chain is already closed at retained-bounded
grade with cross-confirmation. No further runner work is warranted
under the stated repair target.
