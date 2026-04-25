# Canonical Methodology Framing Paragraph

**Status:** ADOPTED — to appear in every paper submitted from this framework.

**Date adopted:** 2026-04-25

**Source:** authored by the human author during the methodology-paper kickoff session on 2026-04-25 (current session, prompt ~025).

**Purpose:** standardized AI-disclosure + accountability paragraph. Every manuscript submission, arXiv preprint, journal submission, and conference paper from this framework includes this paragraph (verbatim, or adapted only for the specific tools used in the work in question).

This paragraph is the canonical version. Any deviation in a specific submission should be a deliberate scoping decision documented here.

---

## The Paragraph (verbatim)

> This work was developed using AI-assisted theoretical-physics tools (Claude Sonnet 4.5, OpenAI Codex). All derivations are accompanied by executable runner harnesses available at [repo URL]. Each retained claim is supported by explicit no-go theorems on alternative routes and bounded-vs-retained labeling. The accumulated runner trace constitutes a fully auditable derivation history. The author bears full responsibility for all physics claims; AI tools were used for theorem proving, exhaustive structural search, candidate construction, and obstruction identification, with physical interpretation, foundational choices, and scope judgments retained by the author.

---

## What this paragraph does

It performs five distinct moves in one paragraph, each load-bearing:

1. **Discloses AI involvement explicitly and proactively.** Names the specific tools (Claude Sonnet 4.5, OpenAI Codex). Pre-empts any "concealment discovered later" failure mode.

2. **Anchors the disclosure to verifiable infrastructure.** "Executable runner harnesses available at [repo URL]" gives reviewers something concrete to inspect rather than asking them to take the disclosure on faith.

3. **Names the structural defenses against AI hallucination.** "Explicit no-go theorems on alternative routes and bounded-vs-retained labeling" tells the reviewer that the methodology has been designed with hallucination-mitigation in mind.

4. **Asserts the audit trail as a methodological asset.** "Fully auditable derivation history" reframes what would otherwise look like volume bloat (1142 docs, 2089 scripts) as a feature, not a liability.

5. **Defines the human-AI accountability split crisply.** Lists what AI did (theorem proving, exhaustive search, candidate construction, obstruction identification) and what the author retained (physical interpretation, foundational choices, scope judgments). This is the precise division of labor a journal editor or referee needs to evaluate the work.

---

## Per-submission adaptation guidance

For each new paper:

- **Replace `[repo URL]` with the specific public-package URL.** For most submissions this is the canonical Cl(3)/Z³ repository; for stand-alone supplementary code, use the per-paper artifact URL.
- **Update the tool list** if the specific work was done with a subset (e.g., Claude only, or Codex only). Keep the disclosure honest and tool-specific.
- **The "physical interpretation, foundational choices, and scope judgments" clause stays verbatim** — this is the load-bearing accountability statement.

---

## Where this paragraph appears in submissions

- **arXiv preprints:** in the abstract footnote OR as the first paragraph of an "AI assistance and accountability" section in the body. Both are acceptable; pick one consistently across submissions.
- **Journal manuscripts:** in the "Methods" section, or as a dedicated "AI assistance and accountability" subsection per the journal's policy on AI disclosure.
- **Conference papers:** in the methods section or acknowledgments per venue policy.
- **Supplementary material:** restated explicitly in the supplementary methods if there's a separate methods document.
- **Methodology paper itself:** this paragraph is the abstract's tonal anchor; the methodology paper expands every clause into a section.

---

## Relationship to the recovered AI accountability note

The recovered historical [`AI_ASSISTANCE_AND_ACCOUNTABILITY_NOTE.md`](raw/ai_accountability_note.md) (removed from public package on 2026-04-23 in commit `56876669`) was the prior public AI-disclosure document. This canonical framing paragraph is the **paper-facing successor** to that note: shorter, more specific to individual submissions, designed to be inserted directly into a manuscript without further composition.

The longer accountability note remains useful as the **package-level disclosure** — meant for someone reading the repository, not someone reading a single paper. Both should coexist:

- **Per-paper:** this canonical framing paragraph (~80 words)
- **Package-level:** a longer accountability note (the recovered version, possibly updated) on the public repository

---

## Cross-reference

- Master methodology MD: [`docs/AI_METHODOLOGY_NOTE_2026-04-25.md`](../AI_METHODOLOGY_NOTE_2026-04-25.md)
- Recovered package-level note: [`docs/ai_methodology/raw/ai_accountability_note.md`](raw/ai_accountability_note.md)
- This file is referenced from §5.4 of the master methodology MD.
