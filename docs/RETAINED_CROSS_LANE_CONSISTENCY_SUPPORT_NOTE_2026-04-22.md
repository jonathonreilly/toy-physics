# Retained Cross-Lane Numerical Consistency Support

**Date:** 2026-04-22
**Status:** single-file support harness. Does NOT derive anything new; it cross-checks 26 retained numerical and algebraic identities across eight separately retained lanes in a single executable.
**Primary runner:** `scripts/frontier_retained_cross_lane_consistency.py`

## 0. Scope

Retained Cl(3)/Z³ lanes on `main` are documented and validated separately (each with its own runner). This note packages the **algebraic identities that couple those lanes** into a single runner so that reviewers can verify cross-lane numerical coherence in one place.

The runner is organized into eight blocks, each touching a different retained lane:

| Block | Lane | Identities checked |
|-------|------|--------------------|
| A | Plaquette / coupling | u_0, α_bare, α_LM, α_s(v) cross-relations |
| B | CKM atlas | `|V_us|²`, `|V_cb|`, 5/6 Casimir arithmetic |
| C | Koide chart | SELECTOR, E1, E2, doublet-magnitude identity |
| D | Hierarchy / v_EW | Retained v_EW = M_Pl · (7/8)^(1/4) · α_LM^16 |
| E | Anomaly arithmetic | ANOMALY_FORCES_TIME Tr[Y] = 0, Tr[Y³] = −16/9, Witten |
| F | Q = 3δ triple | Three independent Koide routes converge |
| G | Cosmology | Retained Λ · c² = 3 H_inf² spectral-gap identity |
| H | Neutrino staircase | k_B − k_A = 1, ρ = α_LM, η_break = α_LM/2 |

## 1. Why this is useful

Each block's identities are already retained separately. The support runner:

- makes cross-block identities explicit (e.g. `(E2/2)² = SELECTOR²/3 = Q/3 = 2/9` ties Koide chart to Brannen phase);
- gives reviewers a single check-list entry for cross-lane coherence;
- isolates any single identity that might silently drift in future updates before it propagates;
- provides downstream notes a clean citation target ("see cross-lane consistency runner").

## 2. Running

```
python3 scripts/frontier_retained_cross_lane_consistency.py
```

Expected: 26/26 PASS.

## 3. What this note does NOT claim

- No new derivation, theorem, or closure.
- Does NOT promote any bounded or open lane.
- Does NOT discharge any residual (Q = 2/3 extremal-principle bridge, Brannen radian bridge, solar Δm²₂₁ gap, etc.) — all retain their prior status.

## 4. Cross-references

All identities verified by the runner are re-statements of retained content from:

- `docs/ALPHA_S_DERIVED_NOTE.md`
- `docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md`
- `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
- `docs/KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md`
- `docs/PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md`
- `docs/ANOMALY_FORCES_TIME_THEOREM.md`
- `docs/COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`
- `docs/DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`
- `docs/NEUTRINO_MASS_DERIVED_NOTE.md`
- `docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`
