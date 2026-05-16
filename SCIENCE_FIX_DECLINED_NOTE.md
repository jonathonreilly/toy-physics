# science-fix declined: source_resolved_exact_green_self_consistent_note

**Claim id:** `source_resolved_exact_green_self_consistent_note`
**Source note:** `docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md`
**Primary runner:** `scripts/source_resolved_exact_green_self_consistent.py`
**Date:** 2026-05-16
**Decision:** decline — second-pass auditor's repair items already
satisfied on `origin/main`; judicial third-pass auditor confirmed
`audited_numerical_match` as the terminal verdict.

## PROMPT.md verdict (stale snapshot)

The science-fix prompt was generated from an earlier
2026-05-03 audit snapshot that reported:

- `audit_status: audited_numerical_match`
- `load_bearing_step_class: D`
- `claim_type: bounded_theorem`

with the repair target quoted in the prompt:

> Repair target: add explicit assertions for zero-source exactness,
> TOWARD sign, exponent tolerances, and declare the calibrated gain
> as an input rather than evidence of independent physical amplitude.

## Current ledger state on `origin/main`

`docs/audit/data/audit_ledger.json` (current row, terminal audit
2026-05-11T23:09:16Z) records a `judicial_third_pass`
cross-confirmation:

- `audit_status: audited_numerical_match`
- `effective_status: audited_numerical_match`
- `intrinsic_status: audited_numerical_match`
- `effective_status_reason: terminal_audit`
- `claim_type: bounded_theorem`
- `load_bearing_step_class: G`
- `cross_confirmation.status: third_confirmed_second` — judicial
  reviewer sided with the second auditor's
  `audited_numerical_match / class G` verdict over the first
  auditor's `audited_clean / class B`.
- `claim_scope`: "Audited the bounded numerical pocket for the
  specified compact lattice, source cluster, kernel, calibrated gain
  input, and one self-consistency update."
- `notes_for_re_audit_if_any`: "Recheck only if a later packet
  derives the calibration gain and field normalization from retained
  dynamics rather than treating them as setup inputs."

Judicial `judgment_rationale`:

> The restricted packet explicitly makes the calibrated gain a frozen
> setup input, and the runner hard-codes that gain while asserting
> that it sets the target base-field cap before reproducing the
> frozen table. That is a bounded numerical pocket at a chosen
> calibration value, not first-principles closure from the axiom.
> Under the rubric, this is class G and the appropriate terminal
> verdict is audited_numerical_match.

## Second-pass repair items: status

Each item the science-fix `PROMPT.md` quotes as a repair target is
already wired into the runner and reflected in the note on
`origin/main`.

1. **Explicit assertions for zero-source exactness** —
   `scripts/source_resolved_exact_green_self_consistent.py` lines
   201-205 record a hard assertion
   `abs(zero_delta) <= ZERO_SOURCE_TOL` with `ZERO_SOURCE_TOL=1e-12`.
2. **Explicit assertions for TOWARD sign** — lines 211-215 record
   `toward == len(green_vals)` per row.
3. **Explicit exponent-tolerance assertions** — lines 216-225 record
   `abs(alpha - 1.0) <= 5e-3` for both the instantaneous comparator
   and the self-consistent Green response.
4. **Declare the calibrated gain as an input, not independent
   physical amplitude** — `CALIBRATED_GAIN` is a named module-level
   constant (line 34) and a paired assertion (lines 206-210) certifies
   `gain * ref_max == FIELD_TARGET_MAX` to certify the gain is
   chosen to set the target base-field cap and is not a derived
   amplitude. The runner prints
   `CALIBRATED_GAIN_IS_INPUT=TRUE` and
   `SOURCE_RESOLVED_GREEN_FULL_SELF_CONSISTENT_FIELD_THEORY=FALSE`
   as final-block status lines.

The note itself reflects all four repairs:

- Line 36-38 admits the gain as a frozen setup input
  ("not evidence of an independently derived physical amplitude").
- Lines 65-71 quote the runner's 6/6 PASS banner and the residual
  scope label.
- Lines 86-101 ("Honest limitation") explicitly enumerate that the
  pocket is bounded, one-update, comparator-dependent, and not a
  fully converged self-consistent field theory.
- Lines 103-111 confine the branch verdict to the bounded refinement
  reading.

## Artifact-chain verification (this worktree)

Local re-execution of the primary runner reproduces the cached
assertion banner exactly:

```
PASSED: 6/6
SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_ASSERTIONS=TRUE
CALIBRATED_GAIN_IS_INPUT=TRUE
SOURCE_RESOLVED_GREEN_FULL_SELF_CONSISTENT_FIELD_THEORY=FALSE
RESIDUAL_SCOPE=fully_converged_self_consistent_field_theory_and_uncalibrated_amplitude
```

with `zero_delta=+0.000000000000e+00`, `toward=4/4`,
`alpha_inst=1.000645`, `alpha_green=1.001886`, and frozen-table
reproduction within `5e-4` relative / `5e-8` absolute tolerance.
The cached output `outputs/source_resolved_exact_green_self_consistent_assertions_2026-05-06.txt`
is byte-equivalent on the assertion block.

## Why this is a decline rather than a no-op fix

The judicial reviewer explicitly states the recheck condition as
"Recheck only if a later packet derives the calibration gain and
field normalization from retained dynamics rather than treating them
as setup inputs." That is a research-grade derivation: it requires
upstream retained-grade physical-amplitude theorems that the present
note's bounded-pocket scope intentionally does not import.

Attempting to "close" this at the science-fix level inside the
existing scope would either:

1. Invent retained-grade premises (a hard-rule violation under both
   the science-fix prompt and the user's project memory
   "Consistency equality is not derivation"), or
2. Repeat what the note already says about the bounded reading, with
   no audit-state change because the row is already at terminal
   verdict.

The only honest action under the science-fix rubric is to record the
decline and retire the queue row against the terminal judicial
verdict.

## What this PR contains

Only `SCIENCE_FIX_DECLINED_NOTE.md` at the repo root. No source,
runner, log, output, audit-data, audit-doc, or publication file is
modified.

## Honest assessment

Partial — the science-fix queue row should be retired against the
already-terminal `judicial_third_pass` verdict. The note is honestly
narrowed, the runner asserts each repair item with hard pass
conditions, and the remaining gap (deriving the calibration gain and
field normalization from retained dynamics) is research-grade
out-of-scope work, not a numerical-match repair.
