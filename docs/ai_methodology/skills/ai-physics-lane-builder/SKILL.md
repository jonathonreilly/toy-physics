---
name: ai-physics-lane-builder
description: Use when an LLM agent needs to open, extend, or package an AI-assisted theoretical-physics research lane with bounded scope, note/runner evidence, explicit claim status, and honest landing gates.
---

# AI Physics Lane Builder

Use this skill to turn a physics idea into a controlled repo lane rather than a
free-floating speculative draft. It is based on the methodology synthesis and
case studies in `docs/ai_methodology/`.

For paper-facing prose, also read `docs/WRITING_VOICE_GUIDE_2026-04-25.md`.
Write from the plain physical question, the calculation, the support surface,
and the caveat. Do not use sales language to promote an open lane.

## Workflow

1. **Ground first.** Inspect current notes, runners, logs, lane maps,
   controlled vocabulary, publication surfaces, and relevant no-go history.
2. **Define the lane question.** State one target, current status, existing
   evidence, and smallest honest forward step.
3. **Set status gates before work.** Define what would make the result
   `retained`, `bounded`, `support`, `open`, `no-go`, or `reject`.
4. **Build an evidence chain.** Pair each claim with a note plus executable
   runner, retained log, symbolic derivation, exact audit, theorem import, or
   explicit no-go proof.
5. **Check the decisive step.** The artifact must test the load-bearing bridge,
   not only surrounding algebra. Literal assertion checks are not closure.
6. **Run narrow tests first.** Prefer the smallest honest surface over broad
   ladders. Add sentinels only when a rule-family or regime changes.
7. **Preserve negatives.** If the lane fails, write the obstruction clearly and
   keep it as route-pruning evidence.
8. **Prepare for review.** Include assumptions, imports, known caveats,
   reproduction commands, and exact evidence paths.
9. **Keep branch truth off `main`.** Branch output is not part of the main
   claim boundary until reviewed and selectively landed.
10. **Write plainly.** When the lane becomes prose, say what was asked, what was
    checked, what was found, and what remains open.

## Required Output

Produce a compact lane packet with:

- lane question and current status;
- artifact pair and evidence path;
- decisive-step check or missing-artifact warning;
- assumptions and imports;
- retained/bounded/open/no-go decision rule;
- next runner or proof step;
- landing gate and review request.

## Guardrails

- Do not let a plausible story become a theorem without the support surface.
- Do not silently upgrade bounded support into retained closure.
- Do not replace a missing derivation with narrative confidence.
- Do not cite a placeholder runner as if it checks the claim.
- Do not summarize from memory when repo evidence exists.
- Keep historical or superseded material out of the current claim boundary.
