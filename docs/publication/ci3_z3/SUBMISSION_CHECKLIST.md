# Submission Checklist

This is the operational checklist for turning the current package into a public
submission without re-litigating claim status at the last minute.

## 1. Claim hygiene

- every statement in the manuscript appears in [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- every retained claim appears in [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
- every retained claim has one authority note and one validation path
- every reviewer-facing quantitative row appears in
  [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- every row in the quantitative summary also appears in both
  [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) and
  [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- every bounded lane is labeled `bounded` in both the manuscript and GitHub
- no stale review packet or pitch memo is linked as science authority
- every stale-authority family is either quarantined in
  [STALE_AUTHORITY_AUDIT_2026-04-14.md](./STALE_AUTHORITY_AUDIT_2026-04-14.md)
  or documented in [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)

## 2. Public arXiv package

- keep the main text on the retained backbone only
- state the one live flagship gate in one disciplined paragraph
- move exact `I_3 = 0` and CPT to compact support or Extended Data if space is tight
- keep DM and bounded renormalized `y_t` out of the core claim stack
- ensure title, abstract, and discussion do not say or imply “full closure”

## 3. Private journal adaptation

- derive from the public arXiv package rather than maintaining a competing public draft
- shorten presentation without changing the claim surface
- keep exact supporting theorems and honest bounded companions private if venue format requires it
- do not create a second public authority surface on `main`

## 4. GitHub surface

- front door is [README.md](../../../README.md)
- publication navigation starts at [README.md](./README.md)
- package architecture is defined by
  [PUBLICATION_CONTROL_PLANE.md](./PUBLICATION_CONTROL_PLANE.md)
- every linked runner executes from the repo root
- raw logs for retained runners are archived under `logs/retained/`
- figure-prep artifacts are archived under `outputs/figures/`
- obsolete scratch notes stay in work history, not the front-door package

## 5. Figures and tables

- each planned figure has one source runner or one explicit data-prep note
- the claims table is the manuscript truth source
- the derivation / validation map is the evidence truth source
- the quantitative summary table is the reviewer truth source for
  prediction/observation rows
- the results index maps every section to one authority note and runner
- venue-facing figure captions use `retained`, `bounded`, or `open` wording consistently

## 6. Before submission

- freeze one commit hash for the public package
- freeze [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) with the same commit hash
- freeze [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md) with the same commit hash
- freeze [REPRODUCIBILITY_FREEZE_2026-04-14.md](./REPRODUCIBILITY_FREEZE_2026-04-14.md) or its successor with the same commit hash
- record exact runner versions and expected pass summaries
- regenerate manuscript figures from pinned data
- proofread title, abstract, and conclusion against the claims table
- confirm the one live flagship gate is still described honestly if it remains open

## 7. If the remaining live gate closes before submission

- update [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- update [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- promote the newly retained note+runner pairs into the results index
- tighten the abstract and discussion only after the claim ledger changes
