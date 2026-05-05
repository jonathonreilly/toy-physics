# PR #230 Schur A/B/C Definition Derivation Attempt Note

Date: 2026-05-05

Status: exact negative boundary / Schur A/B/C definition not derivable from the current PR230 source-only surface.

## Question

Can the current PR230 source functional, scalar ladder scouts, Feshbach response support, and outside-math tools define the missing Schur pre-elimination rows `A`, `B`, and `C` needed for the `K'(pole)` route?

## Result

No.  The current surface supplies source-denominator support and useful Schur sufficiency/contract gates, but it still does not supply the neutral scalar kernel basis, source/orthogonal projector, `A/B/C` block definitions, block-derivative rows, contact/FV/IR/zero-mode scheme, or canonical bridge.

The runner constructs an explicit row-definition gauge counterfamily.  Several finite nondegenerate block families have the same effective source denominator

```text
D_eff = A - B C^{-1} B
```

on the sampled grid, while assigning different `A`, `B`, `C`, `A'`, `B'`, and `C'` rows at the pole.  Therefore even exact knowledge of the source-only denominator does not identify the pre-Schur rows.

## Outside-Math Boundary

Exact tensor/PEPS contraction, holonomic D-module/Picard-Fuchs/creative-telescoping machinery, free-probability/Weingarten expansions, PSLQ, and motivic searches remain allowed as tools only after the object being computed is defined on the same PR230 surface.  They are not proof selectors for row labels, `O_H`, `kappa_s`, `g2`, `c2`, or `Z_match`.

## Claim Boundary

This block writes no Schur row file and no `O_H`, W/Z, scalar-LSZ, or neutral irreducibility certificate.  It does not claim retained or proposed-retained PR230 closure.  A positive Schur route still needs a same-surface neutral scalar kernel basis and source/orthogonal projector, followed by certified `A/B/C` rows or an equivalent precontracted Schur row certificate with pole-derivative and limiting-order authority.

Certificate:

```text
outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json
```

Runner:

```text
scripts/frontier_yt_pr230_schur_abc_definition_derivation_attempt.py
```
