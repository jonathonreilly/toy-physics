---
name: reviewer-backpressure-integrator
description: Use when an LLM agent needs to turn adversarial review feedback into narrow honest repo changes, selective landing decisions, demotions, active review queue updates, or historical archiving.
---

# Reviewer Backpressure Integrator

Use this skill after review has found pressure points. Its job is not to defend
the original branch. Its job is to make the repo state honest.

For any paper-facing rewrite, read `docs/WRITING_VOICE_GUIDE_2026-04-25.md`
and keep the prose plain: what was claimed, what failed, what survived, and
what remains open.

## Workflow

1. **Group findings by disposition.** Use `fix on main`,
   `support-only demotion`, `science-needed`, `reject`, and `historical only`.
2. **Apply the narrowest honest fix.**
   - wording or stale packaging: fix the live surface;
   - missing theorem step: mark open, demote, or leave off-main;
   - useful but non-live material: archive in work history;
   - false or misleading route: reject or convert to no-go.
3. **Align evidence chain and status.** If the note, runner, log, README, and
   claim table disagree, weaken the strongest surface or add the missing
   artifact before promotion.
4. **Perform selective landing.** Land only the honest subset of a branch.
   Keep branch-local review packets and raw traces out of the public front door
   unless they belong in a raw annex.
5. **Update authority surfaces.** If the claim boundary changes, update the
   relevant package table, validation map, active review queue, lane board, or
   work-history note.
6. **Preserve provenance.** Record why a branch was narrowed, demoted, or
   rejected. Link detailed packets from the active queue or archive.
7. **Close the loop.** Remove active review items only after the repo-facing
   state is correct.

## Backpressure Rules

- If a reviewer is right, change the claim boundary.
- If a reviewer found a real missing derivation, do not patch it with prose.
- If only part of a branch is safe, land only that part.
- If a result is negative but meaningful, keep it as a no-go or boundary note.
- If a lane is historical, route it to work history rather than live authority.
- If raw evidence is useful but messy, land it under a raw annex with a curated
  front door rather than making it public authority.

## Output

Produce:

- disposition summary;
- exact repo-facing changes needed;
- retained / bounded / open / rejected final status;
- files/surfaces that must be updated together;
- active queue or archive placement;
- remaining science question, if any.
