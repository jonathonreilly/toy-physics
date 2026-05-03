# ARTIFACT PLAN — VEV V-Singlet Derivation Campaign

**Date:** 2026-05-02

What artifacts each block produces and where they go.

## Block 01 — H2 reformulation

**Branch:** `physics-loop/vev-v-singlet-derivation-block01-20260502` (from origin/main)

**Artifacts to produce:**

1. **Theorem note** `docs/EW_VEV_V_SINGLET_DERIVATION_THEOREM_NOTE_2026-05-02.md`
   - Lemma H2.1: V-invariance of `f_vac` on the minimal Klein-four block
   - Lemma H2.2: m²-curvature `A(L_t)` of `f_vac` is V-invariant when source `m` is V-singlet
   - Lemma H2.3: vacuum at `m=0` is V-singlet (no spontaneous V-breaking on finite minimal block)
   - Theorem H2: `v²(physical) / v²(L_t=2 baseline) = A(L_t=4) / A(L_t=2) = 8/7`, hence `v(physical) = v_baseline · (7/8)^(1/4)`, with `v_baseline = M_Pl · α_LM^16` (admitted B5)
   - Corollary H2-B: `m_H²` is NOT subject to the (7/8)^(1/4) factor because the EWSB-broken minimum is not a V-singlet (representation-theoretic distinction)
   - Section "Bridges retired": precise table mapping B1, B2, B3 → trivialities under the f_vac formulation
   - Section "Admissions remaining": C1 (curvature-of-V_eff identification), C2 (V-singlet vacuum), B4 (normalization), B5 (hierarchy baseline)
   - Section "Status": exact support theorem on retained framework primitives + admitted C1 + admitted B5
2. **Runner** `scripts/frontier_ew_vev_v_singlet_derivation.py`
   - Computes `A(L_t)` from direct sum over Matsubara modes for L_t ∈ {2, 4, 6, 8, ∞}
   - VERIFIES `A(2)/A(4) = 7/8` from sum, not assertion
   - VERIFIES `A(2)/A(∞) = √3/2` from sum + integral, not assertion
   - VERIFIES V-invariance: action on `(z, -z, z*, -z*)` leaves `A(L_t)` fixed, by direct check
   - VERIFIES m²-curvature is V-invariant when source is V-singlet (homogeneous)
   - Reports the (7/8)^(1/4) numerical value as a DERIVED output, not a hard-coded constant
   - Reports the L_t=4 selection from Klein-four orbit closure (counting orbits)
   - Includes a "negative control": shows that a non-V-singlet source gives a different (smaller) curvature, demonstrating the V-singlet condition is load-bearing
3. **Claim status certificate** `.claude/science/physics-loops/vev-v-singlet-derivation-20260502/block01/CLAIM_STATUS_CERTIFICATE.md`
   - Apply 7-criterion test
   - Apply V1-V5 promotion value gate
   - Honest tier: `exact support theorem` if all pass, `bounded support theorem` otherwise
4. **Review-loop output** in `.claude/science/physics-loops/vev-v-singlet-derivation-20260502/block01/REVIEW_HISTORY.md`
5. **PR** `physics-loop/vev-v-singlet-derivation-block01-20260502` → main (do NOT merge)
   - PR title: `[physics-loop] vev-v-singlet-derivation block01: f_vac reformulation retiring B1+B2+B3 (exact support)`
   - PR body: V1-V5 answers; what bridges retire; what bridges remain; cluster-obstruction independence

## Block 02 — H1 Route 2 cheap probe (β=6 from Cl(3) + Klein-four counting)

**Branch:** `physics-loop/vev-v-singlet-derivation-block02-20260502` (from origin/main, NOT stacked)

**Artifacts (likely no-go):**
1. Stretch-attempt note `docs/EW_BETA_FROM_CL3_KLEIN_FOUR_COUNTING_STRETCH_NOTE_2026-05-02.md` — records counting attempts, names obstructions, classifies what works and what doesn't.
2. Runner `scripts/frontier_ew_beta_from_cl3_klein_four_counting_stretch.py` — checks several counting ansätze against the framework's algebraic constraints; reports yes/no for each.
3. Certificate (likely `named-obstruction stretch attempt` tier).
4. Review-loop output.
5. PR (no-go, marked `[physics-loop]` ... `(named-obstruction stretch)`).

## Block 03 — H1 Route 1 deep stretch (minimal-block self-consistent saddle)

**Branch:** `physics-loop/vev-v-singlet-derivation-block03-20260502` (from origin/main)

**Artifacts (deep-block stretch, likely partial):**
1. Stretch-attempt note `docs/PLAQUETTE_MINIMAL_BLOCK_SADDLE_STRETCH_NOTE_2026-05-02.md` — works the saddle equation `⟨P⟩ = u_0⁴ = -∂lnZ_min/∂β\|_{u_0*}` from the existing Class A determinant identity; identifies whether the V-invariant subspace allows a unique saddle.
2. Runner `scripts/frontier_plaquette_minimal_block_saddle_stretch.py` — solves the saddle on the minimal block numerically as a check, reports the V-invariant subspace structure.
3. Certificate (likely `named-obstruction stretch attempt` tier or `bounded support` if partial closure).
4. Review-loop output.
5. PR (named-obstruction or bounded-support).

## Cap policy

- 5 PRs / 24h volume cap
- 2 PRs / parent-row family cluster cap
- Block 01-03 plan: 3 PRs total
- Reserve: 2 PRs available for refresh-queue follow-up if budget remains

## Files allowed in science branches

- New theorem/support/no-go notes under `docs/`
- New runners under `scripts/`
- Loop pack state under `.claude/science/physics-loops/vev-v-singlet-derivation-20260502/`
- Review history and handoff notes (branch-local)

## Files NOT touched in science branches

- `README.md`, `docs/repo/LANE_REGISTRY.yaml`,
  `docs/work_history/repo/LANE_STATUS_BOARD.md`,
  `docs/CANONICAL_HARNESS_INDEX.md`, publication matrices, active review queue
- Any methodology/governance docs
- Any merging/integration of this branch's work into authority surfaces
- Proposed weaving recorded in `HANDOFF.md` for later integration
