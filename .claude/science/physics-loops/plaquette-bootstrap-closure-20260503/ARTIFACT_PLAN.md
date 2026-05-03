# ARTIFACT PLAN — Plaquette Bootstrap Closure

**Date:** 2026-05-03

## Block 01 — Bootstrap framework integration + smallest analytical bound

**Branch:** `physics-loop/plaquette-bootstrap-closure-block01-20260503` (from origin/main)

**Artifacts:**
1. **Theorem note** `docs/PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md`
   - Integration plan: framework's RP theorem (A11) ⟹ Wilson-loop Gram matrix PSD
   - Smallest non-trivial Gram matrix on minimal block: 2x2 with `{1, P}`
   - Combine with simple loop / Cauchy-Schwarz inequalities
   - Derive analytical bound on `⟨P⟩(β=6)` (likely loose but NEW)
   - Compare to bridge-support stack analytic upper-bound + Kazakov-Zheng literature bracket
2. **Runner** `scripts/frontier_plaquette_bootstrap_framework_integration.py`
   - Verifies the 2x2 Gram matrix PSD condition
   - Numerically tests sample `⟨P⟩` values to find the cutoff above/below which 2x2 PSD + simple inequalities hold
   - Computes the analytical bound symbolically using sympy (if available) or numpy
3. **Claim status certificate** in `block01/CLAIM_STATUS_CERTIFICATE.md`
4. **Review history** in `block01/REVIEW_HISTORY.md` with V1-V5
5. **PR** opened, named-obstruction or exact-support depending on bound tightness

## Block 02 — Framework-specific positivity refinement

**Branch:** `physics-loop/plaquette-bootstrap-closure-block02-20260503` (from origin/main)

**Artifacts:**
1. **Theorem note** `docs/PLAQUETTE_BOOTSTRAP_FRAMEWORK_SPECIFIC_POSITIVITY_NOTE_2026-05-03.md`
   - 3x3 truncation `{1, P, P²}` Gram matrix
   - Framework-specific positivity: Cl(3) Hilbert-Schmidt structure + Klein-four V-invariant subspace
   - Refined analytical bound on `⟨P⟩(β=6)`
   - Integration with bridge-support stack (analytic upper-bound 0.59353)
2. **Runner** `scripts/frontier_plaquette_bootstrap_framework_specific_positivity.py`
3. **Claim status certificate** in `block02/CLAIM_STATUS_CERTIFICATE.md`
4. **Review history** in `block02/REVIEW_HISTORY.md` with V1-V5
5. **PR** opened (cluster cap REACHED at 2 PRs in `gauge_vacuum_plaquette_*`)

## Cap policy

- 5 PRs / 24h volume cap (well below — only 2 expected)
- 2 PRs / parent-row family cluster cap — REACHED at block 02
- Stop after block 02 unless an orthogonal target emerges in OPPORTUNITY_QUEUE refresh
