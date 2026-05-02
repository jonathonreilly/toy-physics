# Retained-Promotion Campaign Prompt (replaces audit-backlog-rescope prompt)

**Why this prompt exists:** The 2026-05-02 audit-backlog-campaign produced 40 PRs in
one session, of which only ~10–13 added genuine value. The campaign was framed as
"promote bounded → retained" but actually delivered audit-lane review-prep:
narrow rescopes that create new audit-pending rows (don't promote anything),
audit companions that re-verify identities the primary runners already verified,
and source-note tightenings (the only category that did real housekeeping).

This prompt is structured to make that failure mode hard.

## Invocation

```text
/physics-loop "Promote ONE bounded_theorem or audited_conditional row to retained by closing
its verdict-identified obstruction with new derivation work" --mode run --runtime <DURATION>
```

## Required behavior

### Target selection — SPECIFIC and NAMED

Pick exactly ONE row from `docs/audit/data/audit_ledger.json` such that:

1. Its `audit_status` is `audited_conditional` or `bounded_theorem`.
2. Its `verdict_rationale` field names a SPECIFIC obstruction (e.g.,
   "requires Sommer scale derived from framework primitives", or
   "scalar-additivity premise must be axiomatized or derived"). Vague
   verdicts like "the upstream is unratified" do NOT qualify — those
   are dependency-chain issues, not derivation gaps.
3. The named obstruction is in the framework's actual research scope —
   not "ratify upstream X" but a concrete physics/math question.

Record the target row, the verdict text, and the named obstruction in
`OPPORTUNITY_QUEUE.md`. If no row in the backlog has a SPECIFIC named
obstruction, stop the campaign and report.

### Required output — one of three honest outcomes

Each cycle must produce exactly ONE of:

**(a) Closing derivation.** A new theorem note + runner that derives the
named obstruction from retained framework primitives. The runner must
compute the answer, not check a hypothesis. The derivation must be
admitted-context-free on the obstruction itself (admitted-context on
genuinely external mathematics — e.g., standard QFT machinery — is
allowed and labeled).

**(b) No-go closure.** A new no-go note + runner that proves the
obstruction CANNOT be derived from retained primitives. The no-go must
exhibit the obstruction concretely (e.g., a counterexample that
satisfies the retained primitives but fails the candidate derivation).

**(c) Stretch-attempt failure.** A documented attempt that worked the
obstruction for ≥1 deep block (90 minutes), records the named hard
residual it could not close, and lists 3–5 fan-out attack frames for
future cycles. Committed as `proposed_support+stretch`, NOT as
retained-positive movement.

### Forbidden output

The cycle MUST NOT produce:

1. **Pattern A narrow rescope** of an algebraic identity that the audit
   lane already understands (e.g., "carve out the polynomial-algebra
   core as a new audit-pending row"). These don't promote anything;
   they create new audit-lane review work.

2. **Pattern B audit companion** that re-verifies an identity the
   existing primary runner already verifies at machine precision.
   Sympy-exact verification of cube-root-of-unity arithmetic, Pauli
   matrix anticommutation, or Schur complement formulas is performative
   when the primary runner already uses Python `Fraction` or numpy at
   1e-12.

3. **Pattern C source-note tightening** that doesn't address the
   verdict's named obstruction. Tightenings that correct
   `proposed_retained` author-side labels are real housekeeping and
   are still allowed AS A SEPARATE LANE under the
   `--mode source-note-hygiene` flag — but they are not retained-
   promotion work and should not be conflated with it.

## Value gate — write the answers before opening any PR

Before `gh pr create`, answer these questions in writing in the cycle's
`CLAIM_STATUS_CERTIFICATE.md`:

| Question | Required answer for "open PR" |
|---|---|
| What is the SPECIFIC verdict-identified obstruction this PR closes? | Named, quoted from verdict text |
| What NEW derivation does this PR contain that the audit lane doesn't already have? | One paragraph describing the new content |
| Could the audit lane already complete this derivation from existing retained primitives + standard math machinery? | "No" — explain why the framework's retained primitives are necessary |
| Is the marginal content non-trivial (i.e., not a textbook identity, not a definition restated)? | "Yes" with one-sentence justification |
| Is this a one-step variant of an already-landed cycle? | "No" — name the closest cycle and explain the distinction |

If any answer is "yes" to a forbidden question or "no" to a required
question, the PR must NOT be opened.

## Anti-churn hard stops

1. **Volume cap:** maximum 5 PRs per 24-hour campaign unless the user
   extends. After 5, stop and ask for direction. (The 2026-05-02
   campaign's 40-PR volume was the failure mode.)

2. **Cluster cap:** maximum 2 PRs per parent-row family
   (`koide_*`, `dm_neutrino_*`, `gauge_vacuum_plaquette_*`,
   `ckm_*_2026-04-25`, etc.) per campaign. After 2 in a cluster,
   pivot to a different family or stop.

3. **Stretch-after-fail:** After 2 cycles in a row that produced
   stretch-attempt failures (no closing derivation, no no-go), stop
   and report the global queue exhaustion to the user.

4. **No filler tier between cycles:** if a cycle produces output that
   doesn't meet the required-output criteria, do NOT downgrade to
   Pattern A/B/C "since I have something already." Discard the cycle's
   work and pivot.

## Audit-graph honesty

- Promotion claims must come from the audit lane, never from this campaign.
- New theorem notes use `Status: audit pending` with the actual ledger
  state. No `proposed_retained`, `DERIVED`, `EXACT WITHIN` author-side
  labels.
- The campaign's checkpoint should report **how many rows actually moved
  on the audit ledger** during the campaign window, not "how many PRs
  were opened". Audit-lane state is the metric.

## Source-note hygiene as a separate lane

Pattern C (correcting author-side `proposed_retained` / `DERIVED` /
`EXACT` labels that conflict with audit-lane verdicts) is genuine
housekeeping the audit lane wants done. Run it under a separate flag:

```text
/physics-loop --mode source-note-hygiene "Correct author-side tier-status
conflicts on source notes whose ledger state is audited_conditional or
unaudited" --max-cycles 5
```

Each such cycle produces one source-note edit replacing author-side
labels with explicit `Type / Claim scope / Status: audit pending` headers
and an "Out of scope (admitted-context to this note)" section. Volume
cap: 5 per session. This is NOT framed as bounded → retained promotion.

## Example: what an actual retained-promotion cycle looks like

**Bad cycle (don't do):** "Cycle 19 carves out the CKM magnitudes
structural-counts algebra as a Pattern A narrow theorem with zero ledger
deps; the substitution is mechanical algebra given the parametric input
identities."

**Good cycle (do):** "The audit verdict on `alpha_s_wilson_loop` names
the Sommer scale as the principal external admitted-context. This cycle
attempts to derive the Sommer parameter `r_0` from the framework's
graph-first SU(3) integration on the static-potential Cornell ansatz.
The derivation works the static-force fit at multiple physical scales,
attempts to express `r_0/a` in terms of retained framework primitives
(plaquette expectation `<P>`, Wilson coefficient `c_lambda`), and records
either (i) a closing derivation if the framework primitives suffice,
(ii) a no-go if a non-framework input is provably required, or (iii) a
stretch-attempt failure if neither is reached in one deep block."
