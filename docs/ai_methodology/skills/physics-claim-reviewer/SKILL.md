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
6. **Scrutinize no-go claims with the same rigor as positive theorems.**
   A wrongly scoped no-go is just as bad as a wrongly scoped positive theorem,
   and can be worse because it forecloses investigation paths prematurely.
   For any `claim_type: no_go` candidate, run the no-go battery in the
   dedicated section below before recommending disposition.
7. **Check science naming.** Reject new bare shorthand labels that can be
   confused with axioms, assumptions, Lie types, lane stages, route codes, or
   branch blocks. Require explicit scientific names from the controlled
   vocabulary, with shorthand only as a parenthetical alias when needed.
8. **Classify findings.** Use the local disposition buckets:
   `fix on main`, `support-only demotion`, `science-needed`, `reject`,
   `historical only`.
9. **Recommend the narrowest honest fix.** Prefer wording fixes for wording
   problems; demotion for overclaimed support; new science only when a real
   theorem step is missing.
10. **Write review output.** Lead with findings and file/line references when
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

## No-Go Scrutiny Battery

A wrongly scoped no-go forecloses investigation paths prematurely and can
poison-pill future work that would otherwise close positively. Apply the
same review battery to no-gos as to positive theorems. For any candidate
with `claim_type: no_go` or "bounded obstruction" / "structural foreclosure"
framing in prose:

1. **Scope precision.** State the no-go formally with explicit premises and
   forbidden conclusion class. Could a reader reasonably read it as a wider
   no-go than intended? If yes, narrow the language. (Example failure:
   `first_order_coframe_unconditionality_no_go` is correctly scoped to
   "substrate symmetries alone cannot break Hodge degeneracy" but gets
   misread by downstream notes as "Wald-Noether BP section 5 impossible.")
2. **Reframe-as-positive check.** Is there a positive theorem with the same
   algebraic content and a different framing? For example, a Schur calculation
   that blocks one primitive may also expose a positive finite-spectrum
   structure once labels are treated as conventions. If yes, the right
   delivery may be the no-go plus the positive reframe, not foreclosure alone.
3. **Labeling vs physics check.** Is the no-go on a labeling / convention
   question (dissolvable by convention parallel to u/c/t naming) or on a
   physics question (genuinely foreclosing)? If labeling, the right outcome
   is a `meta` convention note, not a `no_go` theorem note.
4. **Premise-retention check.** No-go theorems depend on premise lists
   just like positive theorems. Verify each premise via live ledger
   `effective_status`. An "unaudited no-go" with an unaudited premise can
   be just as wrong as an "unaudited positive."
5. **Literature bypass check.** Has the published literature gotten around
   this obstruction class via a different route? Causal-set BH entropy
   bypasses Wald-Noether entirely; Connes NCG bypasses gauge-coupling
   lattice derivation. A no-go of "X requires Y" may be a no-go FOR THE
   PARTICULAR ROUTE Y, not for X itself.

When a no-go passes the five-check battery, ship it with the same confidence
as any other reviewed claim boundary, while leaving `audit_status` and
`retained_no_go` effective status to the independent audit lane. When it fails
any check, recommend either narrowing scope, shipping a parallel positive
reframe, or demoting to bounded.

## Guardrails

- Do not reward novelty over correctness.
- Do not treat review as cosmetic copyediting.
- Do not invent fixes that would require missing science.
- Do not approve arithmetic-only closure when the semantic bridge is open.
- Do not bury useful no-go results; preserve them as route-pruning evidence.
- Do not approve overclaimed no-gos. A wrongly scoped no-go is at least
  as harmful as a wrongly scoped positive theorem; apply the No-Go
  Scrutiny Battery before treating any `claim_type: no_go` candidate as
  review-ready for independent audit.
- Do not approve new science names that are only ambiguous shorthand. Use
  explicit names such as `physical Cl(3) local algebra`, `Z^3 spatial
  substrate`, `Koide Frobenius-equipartition condition`, or `Lie type A_1`.
