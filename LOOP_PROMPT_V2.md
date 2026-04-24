# Overnight Axiom-Native Loop V2 — Tighter Rules

This replaces LOOP_PROMPT.md for the "V2" runs on this branch.
Key change: every iteration must try to BREAK its own claim, not just
verify it.

## Mission (unchanged)

Derive kit-native facts. Import count zero.

## New hard rules

V2-HR1. **Pre-commit falsification test.** Every runner must include
  at least one test that would INVALIDATE the claim if it failed.
  The test must be a genuinely independent computation, not a
  rewording of the claim.

V2-HR2. **No reverse-engineered polynomials.** If a formula has
  adjustable coefficients, the runner must demonstrate that the
  specific coefficients are FORCED by kit structure (not merely
  chosen to match a target). If they are only fitted, label the
  result "ansatz" not "derivation".

V2-HR3. **No restatement closures.** A new ledger entry must not
  follow from prior entries by trivial rewriting (multiplying by 1,
  rearranging, renaming). The hostile audit checks: does the new
  fact add informational content beyond the closure of prior facts
  under {+,-,*,/,log,exp}?

V2-HR4. **Structural-absence claims are blockers, not closures.**
  A target section that relies on "the kit doesn't have X" is a
  blocker. To CLOSE a target requires either (a) a specific
  numerical prediction testable against an external value, or (b) a
  non-trivial mathematical theorem with falsifiable consequences.

V2-HR5. **Closure requires an adversarial test that passed.** Not
  just "my runner recorded PASS on its own booleans".

## Per-iteration procedure (V2)

1. Pick a SINGLE claim to test.
2. State it in one sentence, with a precise mathematical content.
3. Identify what computation, if it produced a different result,
   would falsify the claim.
4. Run both the confirming computation AND the adversarial test.
5. If the adversarial test passes (i.e., the claim survives), the
   iteration is a genuine advance.
6. If the adversarial test produces a result inconsistent with the
   claim, the iteration REPORTS THE FAILURE with a precise
   characterization of the regime where the claim breaks.
7. Either way, commit the runner. Failure reports are as valuable
   as confirmations.
