# Abstract-Algebraic Core Extraction

Use this reference when a `/physics-loop` route is likely to produce a
source note and runner, especially when the broad target mixes algebra,
physical imports, and numerical checks.

## When To Use

- Fresh derivation work where the narrow theorem is not obvious yet.
- Repair or salvage of a stuck audit row where the review finding points
  to a missing bridge, hidden import, runner artifact issue, or overbroad
  scope.
- Literature-backed external scaffold work where the theorem must stay
  separate from framework-specific physical identification.

Do not use it to manufacture a positive theorem. If the artifact only
supports a no-go, open gate, bounded theorem, or meta note, use that
claim type.

## Steps

1. **Assumptions inventory:** classify every load-bearing premise as
   framework baseline, local derivation, retained dependency, imported
   input, fitted/observed value, or open gate.
2. **First-principles narrowing:** strip parent ambitions and ask what
   the current algebra actually proves.
3. **Literature check:** find the standard theorem name and check that
   the result is not being misstated.
4. **Artifact check:** make the runner test the bridge and include a
   counterexample when a hypothesis is load-bearing.

## Required Source-Note Boundaries

- State the intended `claim_type`.
- Name all imports and admitted premises.
- Use markdown links only for real dependencies.
- Keep non-load-bearing relation/context references out of the dependency
  graph.
- Include a "does not claim" section.
- Keep audit-status authority with the independent audit lane.

## Anti-Patterns

- Definition-as-derivation.
- Numerical match without a symbolic or structural bridge.
- Parent-promotion language.
- New repo vocabulary or new axioms.
- Treating PR numbers, campaign success rates, or branch-local packets as
  authority.
- Hiding a literature import as if it were framework-derived.

## Review Outcome

The honest output can be a positive theorem, bounded theorem, no-go,
open gate, decoration, or meta note. The goal is an auditable claim
boundary, not a preselected status.
