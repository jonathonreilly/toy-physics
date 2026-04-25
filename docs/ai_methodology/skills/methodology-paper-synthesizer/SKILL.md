---
name: methodology-paper-synthesizer
description: Use when an LLM agent needs to synthesize raw prompt captures, repo history, review packets, branch/landing traces, and governance docs into a polished AI-methodology paper source packet or case study.
---

# Methodology Paper Synthesizer

Use this skill to turn raw AI/repo evidence into paper-ready methodology
material without confusing raw prompt history with public authority.

Before drafting, read `docs/WRITING_VOICE_GUIDE_2026-04-25.md`. The paper
voice is plain: question, object, check, result, caveat. Do not add importance
language where evidence would do the work.

## Workflow

1. **Start from curated surfaces.** Read the methodology front door,
   accountability note, repo-governance docs, publication package, and raw
   annex index before using prompt dumps.
2. **Use the synthesized surfaces first.** Read
   `METHODOLOGY_SYNTHESIS_2026-04-25.md` and
   `METHODOLOGY_CASE_STUDIES_2026-04-25.md` if present, then verify against raw
   evidence.
3. **Define the derivation story.** For each case study, identify the hard
   physics target, why it was difficult, what AI made tractable, and which repo
   skill kept the result honest.
4. **Trace the evidence chain.** Connect prompt/session evidence, branch or
   worktree evidence, review findings, landed artifacts, and final public
   status.
5. **Select representative evidence.** Use small, sanitized excerpts or
   paraphrased summaries. Keep machine-local paths and long raw outputs in the
   annex unless they are necessary evidence.
6. **Separate method from science.** Explain the workflow without promoting
   raw scientific claims beyond the current publication surface.
7. **Write as methods plus case studies.** State what another group can reuse:
   roles, artifacts, review gates, status vocabulary, and landing discipline.
8. **Name limits.** Disclosure, human responsibility, non-authorship of AI
   systems, privacy/sanitization, and auditability versus truth must be
   explicit.
9. **Keep the voice physical.** For each paragraph, make clear what was asked,
   what object was checked, what evidence supports it, or what remains open.

## Case Study Template

Use this structure:

- hard physics problem;
- why the target was difficult;
- AI/repo move;
- artifact outcome;
- current claim boundary;
- reusable lesson.

## Required Outputs

- synthesized methodology claim;
- case-study evidence table;
- paper-draft or section-draft text;
- list of raw excerpts still needing sanitization;
- explicit statement that the methodology paper does not widen the physics
  claim boundary.

## Guardrails

- Do not cite raw chat as if it were a theorem.
- Do not expose unnecessary machine-local or private prompt material in polished
  prose.
- Do not let the methodology paper widen the physics claim boundary.
- Do not imply AI authorship; keep human responsibility explicit.
