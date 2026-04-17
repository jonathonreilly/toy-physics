# Submission Claim Narrowing Plan

**Date:** 2026-04-15  
**Purpose:** exact checklist of claim-surface narrowing and repo/front-door
cleanup needed before public submission.

This is not a theorem note. It is a packaging and submission-hardening plan.

## Scope

The current repo is stronger than the current paper story. The main submission
problem is not missing work everywhere; it is mismatch between:

- what the code and authority notes actually support
- what the front door, claims tables, and paper still imply

This checklist tracks only the narrowing and cleanup work required to align
those surfaces.

## Priority 0: must narrow before any serious submission

### 1. Electroweak scale `v`

**Problem**

- The package still says `v` is not an external datum:
  - [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
  - [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- The code still uses a hardcoded baseline and a hardcoded Planck scale:
  - [frontier_hierarchy_observable_principle_from_axiom.py](/Users/jonreilly/Projects/Physics/scripts/frontier_hierarchy_observable_principle_from_axiom.py)
  - [frontier_yt_zero_import_chain.py](/Users/jonreilly/Projects/Physics/scripts/frontier_yt_zero_import_chain.py)

**Action**

- Resolved on `main`: the hierarchy lane now uses the single canonical surface
  `v = M_Pl * (7/8)^(1/4) * alpha_LM^16 = 246.282818290129 GeV`.
- Keep the public disclosure of:
  - `M_Pl`
  - exponent `16`
  - the role of the plaquette / `u_0` surface

**Files to edit**

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [README.md](/Users/jonreilly/Projects/Physics/README.md)
- [CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md](/Users/jonreilly/Projects/Physics/docs/CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)

### 2. Gravity / QG / continuum chain framing

**Problem**

- This item was previously a live submission blocker because the manuscript and
  front-door package language read broader than the actual chosen-target
  theorem surface.

**Action**

- Resolved on `main`:
  - the paper claim is now stated as exact discrete `3+1` gravity on the
    project route plus exact Gaussian/weak-form/continuum identification on
    one chosen canonical textbook target
  - broad blanket “all continuum packaging” wording has been removed from the
    live paper/front-door surfaces
  - the stale Lorentz contradiction in
    [CONTINUUM_IDENTIFICATION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/CONTINUUM_IDENTIFICATION_NOTE.md)
    is fixed
- Remaining optional hardening:
  - add one compact proof-sketch appendix/section pointer for the gravity/QG
    chain so the manuscript does not read like repo links standing in for an
    argument

**Files to edit**

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md) (done)
- [CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md](/Users/jonreilly/Projects/Physics/docs/CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md) (done)
- [REVIEWER_SUMMARY.md](/Users/jonreilly/Projects/Physics/docs/REVIEWER_SUMMARY.md) (done)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md) (done)
- [CONTINUUM_IDENTIFICATION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/CONTINUUM_IDENTIFICATION_NOTE.md) (done)

### 3. Strong CP

**Problem**

- The current public claim reads as if strong CP is solved in the broad sense:
  - [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
  - [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
  - [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- The actual note contains a Leg C that is exclusion-by-axiom, not a
  dynamical instanton/measure theorem:
  - [STRONG_CP_THETA_ZERO_NOTE.md](/Users/jonreilly/Projects/Physics/docs/STRONG_CP_THETA_ZERO_NOTE.md)

**Action**

- Narrow the paper/public claim to:
  - the axiom-determined action surface is CP-even and carries no bare
    `theta`
  - the real-mass staggered determinant carries no phase
  - CKM CP remains weak-sector only on that surface
- Stop presenting this as a full dynamical strong-CP solution unless the
  instanton/measure side is actually computed.
- Reframe “no axion required” as a framework consequence, not a standalone
  prediction.

**Files to edit**

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [REVIEWER_SUMMARY.md](/Users/jonreilly/Projects/Physics/docs/REVIEWER_SUMMARY.md)
- [README.md](/Users/jonreilly/Projects/Physics/README.md)

### 4. CKM

**Problem**

- The current package says “closed / derived” and “no-import closure package”
  in the public-facing surfaces:
  - [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
  - [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- The authority note still depends on chosen exact atlas counts and a selected
  tensor-slot surface:
  - [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](/Users/jonreilly/Projects/Physics/docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)

**Action**

- Keep the promoted CKM package in the repo.
- Narrow the flagship-paper wording from “closed / no-import” to a more
  specific statement:
  - promoted algebraic/atlas CKM package on the current chosen surface
- Add one explicit qualifier that the package depends on selected exact atlas
  counts and the canonical tensor-slot choice.
- Remove any wording that sounds stronger than the actual selection theorem.

**Files to edit**

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [README.md](/Users/jonreilly/Projects/Physics/README.md)
- [publication README](./README.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)

## Priority 1: quantitative language cleanup

### 5. `alpha_s` and EW normalization

**Problem**

- Public surfaces still say “retained / derived” and “all else derived”:
  - [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- The note itself admits the `9/8` factor is not derived from the CMT alone:
  - [YT_EW_COLOR_PROJECTION_THEOREM.md](/Users/jonreilly/Projects/Physics/docs/YT_EW_COLOR_PROJECTION_THEOREM.md)
- `M_Z`-quoted values depend on threshold-running infrastructure.

**Action**

- Keep the lanes if desired, but narrow the description:
  - canonical same-surface plaquette evaluation
  - connected-color-trace condition
  - threshold-running bridge
- Stop saying “all else derived.”
- Distinguish framework-scale values from `M_Z`-quoted bridge values.

**Files to edit**

- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [README.md](/Users/jonreilly/Projects/Physics/README.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)

### 6. Higgs / top

**Problem**

- The package currently presents very sharp central-value matches while also
  admitting a `~3%` inherited surrogate systematic:
  - [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
  - [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](/Users/jonreilly/Projects/Physics/docs/HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)

**Action**

- Lead with bounded intervals/systematics, not central-value “hits.”
- Treat the 3-loop Higgs row as bounded support, not headline closure.
- Keep Higgs/top fully out of the retained theorem core.

**Files to edit**

- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [README.md](/Users/jonreilly/Projects/Physics/README.md)
- [publication README](./README.md)

## Priority 1: structural clarification

### 7. Three-generation / chirality story

**Problem**

- The package is still exposed on Nielsen–Ninomiya/chiral-regulator questions.
- Even if the framework stance is intentional, the public story does not yet
  say clearly enough that this is an axiomatic physical-lattice stance rather
  than a conventional rooting-resolution claim.

**Action**

- Add one explicit reviewer-facing note:
  - physical-lattice stance
  - no-rooting stance
  - what is and is not claimed relative to conventional staggered rooting
- If there is no true Nielsen–Ninomiya answer yet, say so and scope the claim
  accordingly.

**Files to edit**

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)
- [REVIEWER_SUMMARY.md](/Users/jonreilly/Projects/Physics/docs/REVIEWER_SUMMARY.md)
- possibly add a dedicated note under `docs/`

## Priority 1: front-door consistency

### 8. One public inputs/qualifiers surface

**Problem**

- The current package spreads inputs, qualifiers, and status language across
  multiple files.
- That makes it too easy for the paper and front door to drift.

**Action**

- Add one canonical public note:
  - explicit inputs
  - exact rows
  - bounded rows
  - open rows
  - imported bridge pieces
- Link it from:
  - root README
  - package README
  - reviewer guide
  - arXiv draft

**Suggested filename**

- `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md`

### 9. Root/front-door wording audit

**Problem**

- Root/package fronts still use language like:
  - `derived`
  - `zero-import`
  - `exact ... closure`
  too loosely in a few places.

**Action**

- Audit and narrow the following files together, not one by one:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
  - [START_HERE.md](/Users/jonreilly/Projects/Physics/docs/START_HERE.md)
  - [CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md](/Users/jonreilly/Projects/Physics/docs/CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md)
  - [REVIEWER_SUMMARY.md](/Users/jonreilly/Projects/Physics/docs/REVIEWER_SUMMARY.md)
  - [publication README](./README.md)
  - [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)
  - [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)

## Priority 2: paper architecture

### 10. Section the paper more aggressively without splitting it

**Problem**

- The current paper reads as one giant claim surface.
- The user’s instruction is to keep one paper, not split the repo into
  multiple papers.

**Action**

- Keep one manuscript but restructure it into hard boundaries:
  1. retained structural theorem core
  2. exact support theorems
  3. bounded quantitative package
  4. bounded companion portfolio
  5. one live gate
  6. explicit non-claims / scope
- This preserves one paper while stopping reviewers from reading every lane as
  equally load-bearing.

**Files to edit**

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [FIGURE_PLAN.md](./FIGURE_PLAN.md)
- [FIGURE_CAPTIONS.md](./FIGURE_CAPTIONS.md)

### 11. Add one forward-prediction section or explicitly disclaim it

**Problem**

- The current package is mostly postdictive in the eyes of a hostile reviewer.

**Action**

- Either:
  - add one genuinely forward, falsifiable prediction with a framework error
    bar, or
  - explicitly say the current package is structural and explanatory first,
    not yet prediction-first
- Do not leave this ambiguous.

**Files to edit**

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [README.md](/Users/jonreilly/Projects/Physics/README.md)
- [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md)

## Suggested execution order

1. Fix stale contradiction in
   [CONTINUUM_IDENTIFICATION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/CONTINUUM_IDENTIFICATION_NOTE.md)
2. Demote / relabel the `v` row
3. Narrow strong CP wording
4. Narrow CKM wording
5. Narrow EW / `alpha_s` language
6. Recast Higgs/top as bounded intervals
7. Add the `Inputs And Qualifiers` note
8. Rewrite abstract / intro / sectioning in the arXiv draft
9. Sweep root and reviewer-facing front door files

## Success condition

The package is ready to submit when:

- no front-door file says `v` is derived unless the baseline is truly derived
- no front-door file presents strong CP as dynamically solved beyond what the
  note actually proves
- no front-door file presents CKM/EW/Higgs with stronger wording than their
  authority notes support
- no file contains stale contradictions about Lorentz or continuum scope
- the manuscript reads as one paper with sharply sectioned claim classes,
  rather than one undifferentiated grand-closure story
