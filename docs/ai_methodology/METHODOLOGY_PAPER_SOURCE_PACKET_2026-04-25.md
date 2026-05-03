# AI Theoretical Physics Methodology Paper Source Packet

**Date:** 2026-04-25
**Status:** working source packet for the methodology-paper lane; not a final
paper draft

This packet turns the raw AI-methodology archive into a usable paper source
surface. It is intentionally balanced: part paper skeleton, part evidence map,
and part reusable method handoff.

## Central Thesis

The methodological claim is not just that AI systems helped write a physics
paper. The claim is that AI-assisted theoretical physics can be made auditable
when high-throughput model work is embedded in a repository control system with:

- isolated off-main production lanes;
- paired theorem notes and executable runners;
- explicit retained / bounded / open / no-go status language;
- preserved failed routes and negative results;
- adversarial reviewer backpressure;
- selective landing of only the honest subset onto `main`;
- public-facing claim boundaries that are narrower than the raw exploration
  surface.

This is the "AI theoretical physics as method" lane: LLMs generate, attack,
compress, and integrate candidate science, while the repo structure decides
what becomes live.

## Paper Shape

Recommended posture: methods paper plus case studies.

Working title:

> AI-Assisted Theoretical Physics As Auditable Repository Science

The paper should argue that the workflow is reusable without pretending that
every raw model output is reliable. The useful point is the set of checks:
turning LLM abundance into theorem candidates, obstruction searches, review
pressure, and bounded claim boundaries.

Proposed sections:

1. **Introduction.** AI systems change the economics of theoretical search, but
   only if the outputs are forced through audit surfaces.
2. **Repository-Governed Theorem Production.** Define lanes, notes, runners,
   retained logs, status labels, review queues, and selective landing.
3. **Division Of Labor.** Claude-style forward production, Codex-style review
   and integration, and human judgment over targets, acceptance, interpretation,
   and publication posture.
4. **Reviewer Backpressure Methodology.** Show how hostile review, no-go
   generation, support-only demotion, and narrow honest fixes prevent
   overclaiming.
5. **Case Studies.** Use a small number of repo-grounded derivation stories
   where AI expanded the route space and the repo bounded the resulting
   physics claims.
6. **Reusable Skill Protocols.** Present the LLM skill pack as the transferable
   method.
7. **Disclosure, Accountability, And Limits.** Keep authorship and
   responsibility with the human author; distinguish auditability from truth.
8. **Implications.** AI theoretical physics is strongest when it is adversarial,
   executable, and historically archived.

## Evidence Corpus

Use these surfaces as the primary source material:

- lane front door: [`README.md`](./README.md)
- curated overview: `../AI_METHODOLOGY_NOTE_2026-04-25.md` (sibling
  artifact; cross-reference only — not a one-hop dep of this note)
- accountability note:
  [`AI_ACCOUNTABILITY_AND_DISCLOSURE_NOTE_2026-04-25.md`](./AI_ACCOUNTABILITY_AND_DISCLOSURE_NOTE_2026-04-25.md)
- raw annex: [`raw/README.md`](./raw/README.md)
- synthesized methodology surface:
  [`METHODOLOGY_SYNTHESIS_2026-04-25.md`](./METHODOLOGY_SYNTHESIS_2026-04-25.md)
- case-study packet:
  [`METHODOLOGY_CASE_STUDIES_2026-04-25.md`](./METHODOLOGY_CASE_STUDIES_2026-04-25.md)
- first paper draft:
  [`METHODOLOGY_PAPER_DRAFT_2026-04-25.md`](./METHODOLOGY_PAPER_DRAFT_2026-04-25.md)
- repo trajectory and governance evidence:
  [`REPO_TRAJECTORY_AND_GOVERNANCE_EVIDENCE_2026-04-25.md`](./REPO_TRAJECTORY_AND_GOVERNANCE_EVIDENCE_2026-04-25.md)
- reusable LLM skill pack:
  [`LLM_SKILL_PACK_2026-04-25.md`](./LLM_SKILL_PACK_2026-04-25.md)

External-facing scientific context should be drawn from the publication
package, not from raw prompts:

- [`../publication/ci3_z3/README.md`](../publication/ci3_z3/README.md)
- [`../publication/ci3_z3/CLAIMS_TABLE.md`](../publication/ci3_z3/CLAIMS_TABLE.md)
- [`../publication/ci3_z3/DERIVATION_VALIDATION_MAP.md`](../publication/ci3_z3/DERIVATION_VALIDATION_MAP.md)
- [`../publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md`](../publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)

## Immediate Results Hook

The methodology paper can lean into the strategic frame that this is not an
abstract AI-workflow proposal. It is attached to a repo that already exposes a
large retained/bounded theoretical-physics package and immediate paper-facing
results.

The safe way to say that is:

- the methodology paper describes the production and audit method;
- the scientific results remain governed by the publication package;
- examples of high-value outputs should be cited only through the claims,
  prediction, validation, and non-claims surfaces;
- raw prompts should illustrate method, not expand the physics claim boundary.

## Selected Case Studies

The current synthesis pass selects six derivation-centered case studies where
the repo has enough evidence to show the full method loop. Use
[`METHODOLOGY_CASE_STUDIES_2026-04-25.md`](./METHODOLOGY_CASE_STUDIES_2026-04-25.md)
as the authority surface for details.

| Case | Why it matters | Evidence surface |
|---|---|---|
| `Cl(3)/Z^3` to Standard-Model algebra | Turns a numerology-prone target into exact matrix/operator artifacts and a `95/95` regression surface | `../CL3_SM_EMBEDDING_*`, `../CL3_COLOR_AUTOMORPHISM_THEOREM.md`, `../CL3_TASTE_GENERATION_THEOREM.md` |
| Quantitative electroweak/top/hierarchy chain | Shows normalization, color projection, source-response, and Ward-identity traps being separated into explicit claim boundaries | `../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`, `../YT_*`, `../ALPHA_S_DERIVED_NOTE.md`, `../HIGGS_MASS_FROM_AXIOM_NOTE.md` |
| CKM structural atlas | Shows AI-assisted theorem extraction from a dense atlas without using CKM fits as derivation inputs | `../CKM_*`, `../ALPHA_S_DERIVED_NOTE.md` |
| DM/leptogenesis selector problem | Shows no-go audits narrowing a global selector problem into exact target-surface and bounded quantitative results | `../DM_ABCC_*`, `../DM_CURRENT_BANK_QUANTITATIVE_MAPPING_NOTE_2026-04-21.md`, `../DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md` |
| Koide charged-lepton lane | Shows a high-value target becoming support/no-go/bridge-narrowing rather than false closure | `../KOIDE_*`, `../CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md`, raw review evidence |
| Gravity and wave lanes | Shows frozen replay and controls demoting overclaims while preserving retained positives | `../WAVE_3PLUS1D_PROMOTIONS_NOTE.md`, `../LENSING_DEFLECTION_NOTE.md`, gravity/wave correction notes |

Do not use raw chat excerpts as polished evidence until they are sanitized. The
paper should cite representative prompts only when they directly illustrate a
methodological move.

## Reusable Method Claim

The reusable output of the lane is the skill pack, not a conventional software
library. The skills encode how an LLM agent should:

- open a physics lane without polluting `main`;
- pair a claim with a runnable evidence surface;
- review the claim adversarially;
- apply backpressure without replacing missing science with rhetoric;
- synthesize raw history into paper-grade case studies.

That is the core transferable artifact for other groups using language models
to do theoretical work.

## Next Synthesis Pass

The next paper-building pass is now editorial:

1. choose the final three to five case studies from the synthesized packet;
2. sanitize representative excerpts;
3. convert the skill pack into a methods figure or boxed protocol;
4. expand the first paper draft into submission-grade prose with citations;
5. keep the raw annex separate from the polished narrative.

The paper should stay disciplined: "AI makes theoretical physics faster" is
not enough. The defensible claim is that AI plus repository governance creates
an auditable theoretical-production loop.
