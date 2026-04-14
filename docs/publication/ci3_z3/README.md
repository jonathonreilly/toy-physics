# CI(3) / Z^3 Publication Package

This directory is the publication-facing entrypoint for the current `Cl(3)` on
`Z^3` paper.

Use this package instead of browsing raw repo chronology.

## External reviewer read order

If you are new to the repo, read these first:

1. [External reviewer guide](./EXTERNAL_REVIEWER_GUIDE.md)
2. [Publication state](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md)
3. [Publication matrix](./PUBLICATION_MATRIX.md)
4. [Quantitative summary table](./QUANTITATIVE_SUMMARY_TABLE.md)
5. [Claims table](./CLAIMS_TABLE.md)
6. [Frozen-out registry](./FROZEN_OUT_REGISTRY.md)

That path makes four things explicit:

- retained core
- observation-facing bounded portfolio
- live gates
- frozen-out but documented work

## Start here

- [External reviewer guide](./EXTERNAL_REVIEWER_GUIDE.md)
- [Nature package](./NATURE_PACKAGE.md)
- [arXiv package](./ARXIV_PACKAGE.md)
- [Publication control plane](./PUBLICATION_CONTROL_PLANE.md)
- [Claims table](./CLAIMS_TABLE.md)
- [Publication matrix](./PUBLICATION_MATRIX.md)
- [Quantitative summary table](./QUANTITATIVE_SUMMARY_TABLE.md)
- [Reproducibility freeze](./REPRODUCIBILITY_FREEZE_2026-04-14.md)
- [Stale-authority audit](./STALE_AUTHORITY_AUDIT_2026-04-14.md)
- [Frozen-out registry](./FROZEN_OUT_REGISTRY.md)
- [Remote branch audit](./REMOTE_BRANCH_AUDIT_2026-04-14.md)
- [Derivation / validation map](./DERIVATION_VALIDATION_MAP.md)
- [Full claim ledger](./FULL_CLAIM_LEDGER.md)
- [Results index](./RESULTS_INDEX.md)
- [Reproduce guide](./REPRODUCE.md)
- [Submission checklist](./SUBMISSION_CHECKLIST.md)
- [Submission sequence](./SUBMISSION_SEQUENCE_2026-04-14.md)
- [Figure plan](./FIGURE_PLAN.md)
- [Figure captions](./FIGURE_CAPTIONS.md)
- [Nature draft](./NATURE_DRAFT.md)
- [arXiv draft](./ARXIV_DRAFT.md)
- [Publication card](./PUBLICATION_CARD.md)
- [Impact map](./IMPACT_MAP.md)

## Core authority docs on this branch

- [Publication state](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md)
- [Paper outline](../../PAPER_OUTLINE_2026-04-12.md)
- [Flagship contribution statement](../../FLAGSHIP_PAPER_CONTRIBUTION_STATEMENT_NOTE.md)
- [Gauge/matter closure gates](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md)
- [Remote branch audit](./REMOTE_BRANCH_AUDIT_2026-04-14.md)

## Current paper surface

Framework sentence:

> We take `Cl(3)` on `Z^3` as the physical theory. Everything else is derived.

Retained backbone:

- weak-field gravity from the Poisson / Newton chain
- weak-field WEP and time dilation as retained corollaries on that gravity surface
- restricted strong-field gravity closure on the current star-supported
  finite-rank class under the exact static conformal bridge
- exact native `Cl(3)` / `SU(2)`
- graph-first structural `SU(3)`
- anomaly-forced `3+1`
- electroweak hierarchy / `v`:
  - `245.080424447914 GeV`
  - `0.4628%` low relative to `246.22 GeV`
- retained `S^3` compactification / topology closure
- full-framework one-generation closure
- three-generation matter structure in the framework
- exact `I_3 = 0` theorem on the Hilbert surface
- exact CPT theorem on the free staggered lattice

Reviewer-facing framing notes:

- `v` is a retained exact minimal-block theorem together with a pinned
  numerical evaluation on the current `u_0` / plaquette surface; do not read
  the number as a separate claim from the theorem.
- graph-first structural `SU(3)` is presented as a selector-uniqueness
  statement on the canonical cube-shift graph, not as an arbitrary commutant
  observation.
- the three-generation claim is a physical-species statement, not a disposable
  taste-artifact statement.
- the gravity claim uses a self-consistency principle: Poisson is the unique
  local fixed point in the audited operator family.
- the paper is positioned against other discrete/unification programs only at a
  compact framing level; it is not trying to be a survey.

Observation-facing bounded portfolio:

- DM ratio `R = 5.48` vs `5.47`
- zero-import `\alpha_s(M_Z) = 0.1181`
- best import-allowed `m_t = 171.0 GeV`
- zero-import `m_t = 169.4 GeV` on the current 2-loop bounded route
- CKM magnitude package with strong `|V_us|`, `|V_cb|`, `|V_ub|`
- cosmology companions such as `\Omega_\Lambda`, `n_s`, `w = -1`
- Higgs and sharp companion predictions

Live high-impact gates:

1. DM relic mapping
2. renormalized `y_t` matching
3. CKM / quantitative flavor closure

## Publication rule

The Nature surface should carry the retained backbone and only the tightest
bounded companions. The arXiv surface can carry the full derivation chain, SI,
and clearly labeled bounded lanes.

Every promoted claim must have both:

- one derivation authority note
- one validation path, usually a runner with a pinned pass summary

That contract lives in
[DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md).

The repo-wide capture contract now also includes:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)
- [PUBLICATION_CONTROL_PLANE.md](./PUBLICATION_CONTROL_PLANE.md)

Those files exist so bounded and frozen-out work is not silently lost while the
flagship claims remain disciplined.

## Immediate editorial objective

Before the three live gates close, the repo should already be ready to publish:

- one canonical claim ledger
- one derivation / validation map
- one manuscript source for the letter
- one longer arXiv source
- one reproducibility surface for GitHub
- one checklist that makes the final promotion to submission mechanical
