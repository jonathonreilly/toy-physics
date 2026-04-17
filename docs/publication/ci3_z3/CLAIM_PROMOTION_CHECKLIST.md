# Claim Promotion Checklist

**Purpose:** reviewer workflow for moving newly landed science into the actual
`main` publication package without letting stale notes, runner drift, or
overclaim leak into the front door.

Use this checklist together with
[PUBLICATION_CONTROL_PLANE.md](./PUBLICATION_CONTROL_PLANE.md).

## 1. Define the exact claim

Before promoting anything, write down:

- the exact statement being claimed
- whether it is `promoted`, `bounded`, `open`, or `frozen-out`
- the minimal assumptions it needs
- the exact import class
- the single authority note that should own the claim
- the single primary runner that should defend it

If there is no single authority note and single primary runner, the claim is
not ready to promote.

## 2. Audit the science surface

Review the authority note and runner together.

- read the note top-to-bottom
- read the runner header, inputs, and printed claim language
- identify observed inputs, fitted constants, and imported sub-results
- identify any wording stronger than the runner actually supports
- confirm what the result computes, versus what the note says it proves

If the note outruns the runner, downgrade the note or fence it off before
promotion.

## 3. Verify the evidence

Minimum evidence package:

1. syntax check such as `py_compile`
2. runner replay or honest bounded-runtime sanity check
3. output or archived log that matches the note wording
4. any negative control or comparison mode the lane depends on
5. exact list of external inputs still present

If full replay is too expensive, record the bounded check honestly and do not
present it as a full reproduction.

## 4. Compare against the package surfaces

Check whether the result conflicts with:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md) if retained promotion is being proposed
- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) if retained promotion is being proposed
- [DERIVATION_ATLAS.md](./DERIVATION_ATLAS.md) if the lane reuses an existing tool
- any current authority note already serving the same lane

If two package docs disagree on status, numbers, or import class, fix that
before promotion.

## 5. Decide the package class

Use one of these outcomes:

- `promoted`
- `bounded`
- `open`
- `frozen-out`

Do not promote because the result is impressive. Promote only because the
claim boundary is clean.

## 6. Weave it through the real package

Once the class is decided, update the required package surfaces:

1. authority note
2. primary runner header / printed summary
3. [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
4. [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
5. if retained, also:
   - [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
   - [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
   - [RESULTS_INDEX.md](./RESULTS_INDEX.md)
6. if reusable, [DERIVATION_ATLAS.md](./DERIVATION_ATLAS.md)
7. front-door summaries only after the package rows are correct

Also fence off older conflicting notes as historical or supporting-only if
they would otherwise act like competing authorities.

## 7. Define the main-safe promotion set

For `main`, include only:

- the canonical authority note
- the primary runner
- the minimum supporting notes needed to defend the claim

Do not merge the whole iteration history by default.

## 8. Record recheck triggers

Every promoted or bounded claim should list what invalidates the review:

- authority note changed
- runner changed
- external input route changed
- quantitative output changed
- a stronger or weaker status is now justified

If one of those moves, re-run the audit instead of assuming the older review
still holds.
