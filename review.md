# Review: `claude/dreamy-wing-969574`

Reviewed branch tip: `e4ca8c67`

## Verdict

Still not cleared for `main` as a retained-status promotion.

The self-review fixed the note-quality issues cleanly: notation, DESI wording,
matrix-row formatting, and the forced dual-status rhetoric are all better now.
The runner still replays at `PASS=16 FAIL=0`, so this is not a runtime
rejection. The remaining blocker is narrower and unchanged in substance: the
note still promotes `w = -1` to a retained structural corollary even though the
load-bearing vacuum-identification premise is still described by the repo as a
companion/conditional cosmology lane.

## Replay

Verified directly:

- `python3 scripts/frontier_dark_energy_eos_retained_corollary.py`
  -> `PASS=16 FAIL=0`

## Findings

### [P1] The retained-corollary upgrade still rests on a companion-surface premise

The theorem is stated from four inputs, and one of them is the exact status
problem:

- condition (3) is the spectral-gap vacuum identification
  `Lambda = lambda_1(S^3_R) = 3/R^2`,
- that condition is sourced to `COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`,
- but that authority note is still explicitly classified as a
  bounded/conditional cosmology companion, not a retained flagship theorem.

The updated note is more honest than the previous draft: it now explicitly
calls the status "proposed retained structural corollary on the companion-lane
spectral-gap vacuum identification" and consistently labels the identification
as companion-lane in the safe-claim boundary. But that wording still leaves the
same claim-strength problem. A retained corollary cannot be promoted off a
premise the repo still classifies as bounded/conditional. As written, this is a
clean conditional corollary on the fixed-gap vacuum route, not a retained
promotion.

Affected surfaces:
- `docs/DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`
- `docs/COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`
- `docs/publication/ci3_z3/PUBLICATION_MATRIX.md`

### [P2] The runner certifies the corollary once the premises are assumed, but not the retained-status step

The new runner is disciplined about scope, but that scope is exactly why it
does not justify the promotion:

- it restates the theorem as "given ... spectral-gap vacuum identification ...
  and fixed `R`",
- it verifies the `w = -1` consequence of those assumptions,
- it does not certify that the vacuum identification itself is retained on
  `main`,
- and it does not certify that the fixed-`R` vacuum surface has been promoted
  beyond the current cosmology companion framing.

So the script supports a conditional theorem packet, not the claim-strength
upgrade from bounded/conditional cosmology companion to retained structural
corollary. The dead-code cleanup in Check 5 improves code quality but does not
change that boundary.

Affected surface:
- `scripts/frontier_dark_energy_eos_retained_corollary.py`

## Best Next Step

There are two honest ways forward:

1. **Derive the missing status step.**
   Promote the spectral-gap vacuum identification / fixed-`R` vacuum surface
   itself onto a retained theorem surface, and then this `w = -1` split can be
   landed as a retained corollary with package updates.

2. **Downgrade the new note/runner packet.**
   Keep the new note as a cleaner conditional corollary on the existing
   cosmology companion lane, keep the publication row bounded/conditional, and
   use the new runner as a support tool rather than a retained promotion.
