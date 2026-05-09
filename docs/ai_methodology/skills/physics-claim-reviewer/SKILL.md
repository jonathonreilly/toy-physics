---
name: physics-claim-reviewer
description: Use when an LLM agent needs to adversarially review a candidate physics claim, theorem note, runner, branch, or publication surface for overclaims, missing assumptions, code/prose drift, and safe disposition.
---

# Physics Claim Reviewer

Use this skill to apply reviewer pressure before a claim lands on the live
surface. The raw synthesis shows that the most common failure is not bad prose;
it is artifact-chain or semantic drift.

## Workflow

1. **Read the claimed authority surface.** Identify the note, runner, log,
   claim table row, or branch being reviewed.
2. **Find the load-bearing statements.** Extract the exact claims, imported
   assumptions, observations, status labels, and reproduction path.
3. **Check artifact-chain alignment.** Compare prose against the runner/output
   or derivation. Flag placeholder scripts, literal `True` checks, stale logs,
   hard-coded baselines, and runners that do not exercise the decisive claim.
4. **Attack semantic bridges.** Ask what is selected, fitted, imposed,
   imported, conventional, finite-order, protocol-specific, or only shown on
   one surface. Correct algebra can still compare the wrong physical objects.
5. **Check status language.** Decide whether the evidence supports retained,
   bounded, support, open, no-go, reject, or historical language.
6. **Check science naming.** Reject new bare shorthand labels that can be
   confused with axioms, assumptions, Lie types, lane stages, route codes, or
   branch blocks. Require explicit scientific names from the controlled
   vocabulary, with shorthand only as a parenthetical alias when needed.
7. **Classify findings.** Use the local disposition buckets:
   `fix on main`, `support-only demotion`, `science-needed`, `reject`,
   `historical only`.
8. **Recommend the narrowest honest fix.** Prefer wording fixes for wording
   problems; demotion for overclaimed support; new science only when a real
   theorem step is missing.
9. **Write review output.** Lead with findings and file/line references when
   possible, then summarize the safe status.

## Review Questions

- Does the note claim more than the runner proves?
- Does the runner check the decisive step or just assert it?
- Is the result exact, bounded, support-only, conditional, or open?
- Is a selector, convention, imported datum, or fitted parameter being treated
  as derived?
- Is the symbol-to-physics identification actually justified?
- Is the claim still true under the stated validation path?
- Does the public package surface match the latest retained evidence?
- Does the name identify the scientific object, or is it a bare overloaded
  code like `A1`, `A2`, `G1`, `R3`, `Route F`, or `Block 2`?
- Should this be live, demoted, archived, or rejected?

## Guardrails

- Do not reward novelty over correctness.
- Do not treat review as cosmetic copyediting.
- Do not invent fixes that would require missing science.
- Do not approve arithmetic-only closure when the semantic bridge is open.
- Do not bury useful no-go results; preserve them as route-pruning evidence.
- Do not approve new science names that are only ambiguous shorthand. Use
  explicit names such as `physical Cl(3) local algebra`, `Z^3 spatial
  substrate`, `Koide Frobenius-equipartition condition`, or `Lie type A_1`.
