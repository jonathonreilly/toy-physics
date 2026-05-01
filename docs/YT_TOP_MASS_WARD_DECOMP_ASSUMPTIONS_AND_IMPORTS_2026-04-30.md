# Assumptions and Imports Ledger — Ward-Decomposition Pass

**Loop slug:** yt-top-mass-substrate-pin-ward-clean-20260430  
**Date:** 2026-04-30  
**Note:** `YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md`  
**Runner:** `scripts/frontier_yt_top_mass_ward_decomp_no_go.py`

---

## Section A: Permitted Proof Inputs

| ID | Input | Class | Source |
|---|---|---|---|
| AX1 | Cl(3) local algebra (Clifford) | AXIOM | framework |
| AX2 | Z³ spatial substrate | AXIOM | framework |
| D9 | Bare Cl(3)×Z³ action = Wilson plaquette + staggered Dirac, NO independent Yukawa term; phi = composite taste condensate | EXACT RETAINED | YUKAWA_COLOR_PROJECTION_THEOREM:33-40 |
| D12 | Exact SU(N_c) color-singlet Fierz identity: Σ_a (T^a)_{ij}(T^a)_{kl}\|_{singlet} = -1/(2N_c) | EXACT STRUCTURAL | YT_EW_COLOR_PROJECTION_THEOREM:169-172 |
| S2 | Lorentz-Clifford scalar projection \|c_S\| = 1 | EXACT STRUCTURAL (Clifford algebra) | Itzykson-Zuber §2-5 |
| D16 | Tree-level Feynman-rule completeness: at O(α_LM) on Q_L scalar-singlet channel, OGE is the only diagram (no bare contact 4-fermion, no fundamental Higgs) | EXACT RETAINED | MINIMAL_AXIOMS:18-20 + D9 |
| D17 | Unique unit-normalized scalar-singlet composite on Q_L is H_unit = (1/√(N_c·N_iso)) ψ̄ψ, with Z² = N_c·N_iso = 6 | EXACT RETAINED | YCP:33-40 + runner Block 5 (used only for consistency context; its role in the forbiddance analysis is explicit) |
| QFT-WTI | Standard Ward-Takahashi / Slavnov-Taylor / PCAC identities of QFT | STANDARD QFT (textbook bridge, no framework content) | Any QFT textbook |
| g_bare=1 | Canonical surface axiom | AXIOM | MINIMAL_AXIOMS:18-20 |
| N_c=3, N_iso=2 | Retained counts | EXACT RETAINED | framework |

---

## Section B: Forbidden Inputs (Forbiddance Set)

| Input | Why forbidden |
|---|---|
| H_unit-to-top matrix element **as definition of y_t_bare** (eq. 3.7 in Ward note) | audited_renaming obstruction; this is the step being re-examined |
| Any definition y_t_bare := ⟨0\|op\|state⟩ | Equivalent to the above |
| Observed m_t or y_t values | Non-MC route requirement |
| alpha_LM / plaquette / tadpole normalization | Forbidden by loop goal |
| Fitted selectors | Forbidden by loop goal |

---

## Section C: Comparators Only (Not Proof Inputs)

| Input | Role |
|---|---|
| y_t_bare_RepB = 1/√6 from Ward note | Reference for numerical comparison in runner; NOT used as proof input |
| PDG top-quark mass m_t ≈ 173 GeV | Context only; not imported into any derivation |

---

## Section D: Literature / Textbook Bridges

| Reference | Role | Class |
|---|---|---|
| Itzykson-Zuber §2-5 | Clifford Fierz identity (S2) | STANDARD, textbook |
| Peskin-Schroeder §9 | QFT path-integral and Ward identities | STANDARD, textbook bridge |
| Peskin-Schroeder §15 | Slavnov-Taylor / BRST identities | STANDARD, textbook bridge |
| NJL model (Nambu-Jona-Lasinio) | Context for HS rewrite in composite models | STANDARD, textbook bridge |

No PDG numerical values are used as proof inputs.

---

## Section E: Imports Retired by This Pass

None. This pass produces a no-go / exact-negative-boundary.  No prior imports
are retired, and no new imports are introduced as proof inputs.

---

## Section F: Imports Exposed (Newly Identified Load-Bearing Primitives)

| Import | Role | Status |
|---|---|---|
| D17 (H_unit uniqueness) | Load-bearing normalization node for all four Ward-clean routes | exact retained; its *role* as obstruction node is newly made explicit |

D17 was previously noted as "retained exact" in the Ward note's input table.
This pass makes precise that D17 is the **single load-bearing obstruction**:
every authorized route through the Ward-decomposition pass requires D17's
scalar-uniqueness result, either explicitly (W-II, W-III) or implicitly (W-IV)
to canonically normalize the scalar field.

The observation that "D17 is H_unit identification" is the core audit-clean
no-go.  D17 IS derivable from the substrate (it is retained), but using it
as a **definition source** for y_t_bare (as opposed to a consistency check)
is precisely the step the `audited_renaming` flag identified.
