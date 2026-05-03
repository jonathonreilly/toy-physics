# ROUTE PORTFOLIO — Plaquette Bootstrap Closure

**Date:** 2026-05-03

## Route BB-1 (PRIMARY) — RP-based 2x2 Gram matrix + Migdal-Makeenko

**Move:** Use the framework's existing
`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` (R2) to
establish `G_ij = ⟨Θ(W_i) W_j⟩ ⪰ 0` for `W_i ∈ {1, P}`. Combine with
the lattice Migdal-Makeenko one-link equation to relate `⟨P²⟩` to `⟨P⟩`
and β. Derive an analytical inequality giving a lower bound on `⟨P⟩(β=6)`.

**Score:** retained-positive probability MEDIUM. Smallest-truncation case;
may give loose bound (e.g., `⟨P⟩(β=6) ≥ 0.3` or similar). New analytical
result on framework surface even if loose.

**Decisive artifact:** new theorem note + runner verifying PSD condition
for sample `⟨P⟩` values, identifying the cutoff above which 2x2 PSD
fails.

**Risk:** the bound may be too loose to be interesting (e.g., trivially
implied by `⟨P⟩ ∈ [0, 1]`).

## Route BB-2 (SECONDARY) — 3x3 Gram matrix + extended loop equations

**Move:** Extend Route BB-1 to `W_i ∈ {1, P, P²}` (3x3 Gram matrix).
Requires more loop equations relating `⟨P³⟩` and `⟨P^4⟩` to lower
moments. May tighten the bound.

**Score:** retained-positive probability LOW-MEDIUM. Extending the
truncation is the standard bootstrap-improvement direction. Without
SDP solver, must derive 3x3 PSD analytically (det ≥ 0 for 3x3 is a
cubic; tractable but messier).

**Risk:** the analytical 3x3 PSD may be too unwieldy without SDP.

## Route BB-3 (FRAMEWORK-SPECIFIC) — Cl(3)/Klein-four positivity refinement

**Move:** Add framework-specific positivity from Cl(3) structure +
Klein-four V-invariance. The V=Z₂×Z₂-invariant subspace of the minimal
block has reduced dimensionality; positivity on this subspace is a
stronger constraint than full RP.

**Score:** retained-positive probability LOW. Tighter framework-specific
bound is plausible but not guaranteed without explicit calculation.

**Risk:** may not add structural content beyond Route BB-1.

## Route BB-4 (NUMERICAL VERIFICATION) — small-matrix scipy/numpy SDP

**Move:** Use scipy's limited optimization (`scipy.optimize.linprog`,
`scipy.optimize.minimize` with PSD constraints) to numerically verify
analytical bounds at small truncation. Not a full SDP solve, but a
numerical check that the analytical PSD conditions are tight.

**Score:** retained-positive probability LOW (this is verification, not
new theorem). Useful as a check on the analytical work.

## Selection rule

1. Block 01: Route BB-1 (smallest non-trivial, primary)
2. Block 02: Route BB-2 OR Route BB-3 (whichever yields tighter bound)
3. Block 03 (if budget remains): Route BB-4 numerical verification
   (likely no PR; record in HANDOFF)

Cluster cap: max 2 PRs in `gauge_vacuum_plaquette_*` family. Plan: 2 PRs.
