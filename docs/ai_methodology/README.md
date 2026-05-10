# AI Methodology Lane

This directory is the front door for the repository's AI-methodology surface.

Use it to answer:

- how AI systems were used to generate and audit the science;
- how the repo kept claim-surface drift under control;
- how disclosure and accountability are framed for papers and talks;
- where to find the review/hygiene documents that made the process auditable.

## Start Here

1. `../AI_METHODOLOGY_NOTE_2026-04-25.md` (sibling artifact;
   cross-reference only — not a one-hop dep of this note)
   Curated overview of the methodology lane and its operating rules.

2. [`../WRITING_VOICE_GUIDE_2026-04-25.md`](../WRITING_VOICE_GUIDE_2026-04-25.md)
   The active voice rule for paper-facing prose: plain physical question,
   calculation, support surface, and open caveat.

3. [`CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md`](./CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md)
   The short per-paper disclosure paragraph to reuse in manuscripts,
   preprints, and talks.

4. [`AI_ACCOUNTABILITY_AND_DISCLOSURE_NOTE_2026-04-25.md`](./AI_ACCOUNTABILITY_AND_DISCLOSURE_NOTE_2026-04-25.md)
   The longer package-level accountability statement.

5. [`raw/README.md`](./raw/README.md)
   Raw methodology annex: prompt excerpts, machine-local stores, branch/worktree
   inventories, review evidence, and repo-hygiene traces for later grooming.

6. [`METHODOLOGY_SYNTHESIS_2026-04-25.md`](./METHODOLOGY_SYNTHESIS_2026-04-25.md)
   Full synthesis of the raw annex into the observed AI-theory workflow:
   evidence chains, review backpressure, selective landing, no-go preservation,
   and skill implications.

7. [`METHODOLOGY_CASE_STUDIES_2026-04-25.md`](./METHODOLOGY_CASE_STUDIES_2026-04-25.md)
   Derivation-centered case-study packet showing key physics unlocks, why they
   were hard, how AI accelerated them, and how repo review bounded the claims.

8. [`METHODOLOGY_PAPER_DRAFT_2026-04-25.md`](./METHODOLOGY_PAPER_DRAFT_2026-04-25.md)
   First synthesized methods-paper draft.

9. [`METHODOLOGY_SYNTHESIS_REVIEW_2026-04-25.md`](./METHODOLOGY_SYNTHESIS_REVIEW_2026-04-25.md)
   Adversarial review of the synthesis packet: what is now usable, what was
   narrowed, and what remains before publication.

10. `METHODOLOGY_PAPER_SOURCE_PACKET_2026-04-25.md` (downstream consumer
   packet; backticked to avoid length-2 cycle — that source packet
   already lists this README as its lane front door, so citation graph
   direction is *source_packet → this_readme*)
   Working methods-paper source packet: thesis, paper shape, evidence corpus,
   case-study candidates, and synthesis path.

11. [`REPO_TRAJECTORY_AND_GOVERNANCE_EVIDENCE_2026-04-25.md`](./REPO_TRAJECTORY_AND_GOVERNANCE_EVIDENCE_2026-04-25.md)
   Repo-history, trajectory, governance, reviewer-backpressure, and
   selective-landing evidence missing from the first raw capture.

12. [`LLM_SKILL_PACK_2026-04-25.md`](./LLM_SKILL_PACK_2026-04-25.md)
    Reusable LLM skill pack derived from the synthesis and case studies:
    lane building, claim review, review loops, backpressure integration, and
    methodology synthesis.

13. [`ABSTRACT_ALGEBRAIC_CORE_EXTRACTION_TECHNIQUE_2026-05-10.md`](./ABSTRACT_ALGEBRAIC_CORE_EXTRACTION_TECHNIQUE_2026-05-10.md)
    Reproducible technique for converting ostensibly-blocked audit-graph
    rows into retainable narrow `positive_theorem` source notes via a
    four-exercise protocol (assumptions, first-principles, literature,
    math). Empirically validated by a 100% retainable-artifact rate
    across 23 attempts in the 2026-05-10 parallel-agent campaign.
    Tactical agent-facing doctrine companion at
    [`skills/physics-loop/references/abstract-algebraic-core-extraction.md`](./skills/physics-loop/references/abstract-algebraic-core-extraction.md).

## Core Workflow Surfaces Elsewhere In The Repo

- review workflow:
  [`../repo/REVIEW_FEEDBACK_WORKFLOW.md`](../repo/REVIEW_FEEDBACK_WORKFLOW.md)
- active review queue:
  [`../repo/ACTIVE_REVIEW_QUEUE.md`](../repo/ACTIVE_REVIEW_QUEUE.md)
- canonical runner/index surface:
  `../CANONICAL_HARNESS_INDEX.md` (cross-reference only — backticked to
  avoid length-3 cycle through ACTIVE_WORKING_LANES; the harness index is
  the master surface and lists this readme as a downstream lane entry)
- branch-side retainability examples:
  [`../CLAUDE_BRANCH_RETAINABILITY_NOTE.md`](../CLAUDE_BRANCH_RETAINABILITY_NOTE.md),
  [`../UNPROMOTED_BRANCH_RETAINABILITY_AUDIT_NOTE.md`](../UNPROMOTED_BRANCH_RETAINABILITY_AUDIT_NOTE.md)
- automation / hygiene protocols:
  [`../../AUTOPILOT_PROTOCOL.md`](../../AUTOPILOT_PROTOCOL.md),
  [`../../AUTOPILOT_JANITOR_PROTOCOL.md`](../../AUTOPILOT_JANITOR_PROTOCOL.md),
  [`../../AUTOPILOT_SUMMARY_PROTOCOL.md`](../../AUTOPILOT_SUMMARY_PROTOCOL.md)
- reusable methodology skills:
  [`skills/ai-physics-lane-builder/SKILL.md`](./skills/ai-physics-lane-builder/SKILL.md),
  [`skills/physics-loop/SKILL.md`](./skills/physics-loop/SKILL.md),
  [`skills/physics-claim-reviewer/SKILL.md`](./skills/physics-claim-reviewer/SKILL.md),
  [`skills/review-loop/SKILL.md`](./skills/review-loop/SKILL.md),
  [`skills/audit-loop/SKILL.md`](./skills/audit-loop/SKILL.md),
  [`skills/reviewer-backpressure-integrator/SKILL.md`](./skills/reviewer-backpressure-integrator/SKILL.md),
  [`skills/methodology-paper-synthesizer/SKILL.md`](./skills/methodology-paper-synthesizer/SKILL.md)

## Scope Boundary

This methodology lane is not part of the live physics claim boundary. It exists
to document the production, review, and accountability method around the
science.

The curated notes above are the citable front-door surface. The raw annex under
[`raw/`](./raw/README.md) is deliberately unpolished source evidence for a later
methodology paper. It contains machine-local paths, prompt excerpts, and direct
command outputs, and should be groomed before reuse in polished prose. The
skill pack is a reusable method surface, not a physics authority surface.
