# Assumptions and Imports Ledger
# Top-Sector Bare-Mass Substrate Pin — Physics Loop

**Date:** 2026-04-30
**Loop slug:** yt-top-mass-substrate-pin-20260430
**Purpose:** Explicit ledger of what is and is not permitted as a proof input
  for deriving or blocking a non-MC substrate pin for the top-sector bare mass
  parameter on the `Cl(3)/Z^3` / `g_bare = 1` / staggered-Dirac surface.

---

## A. Permitted Substrate Inputs (Retained/Exact on `main`)

| Input | Class | Source |
|---|---|---|
| Bipartite `Z^3` → `Z_2` parity → `Cl(3)` → `SU(2)` chain | exact / structural | `NATIVE_GAUGE_CLOSURE_NOTE.md` |
| Graph-first weak-axis selector → structural `SU(3)` | exact / structural | `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` |
| `N_gen = N_color = 3` | exact / retained | `THREE_GENERATION_STRUCTURE_NOTE.md` |
| `N_pair = 2`, `N_quark = 6`, `N_color = 3` | exact / retained | CKM structure notes |
| `R_conn = 8/9` | zero-input structural | `RCONN_DERIVED_NOTE.md` |
| `(7/8)^(1/4)` APBC selector factor | exact / structural | `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` |
| SM one-Higgs Yukawa gauge monomial structure (`bar Q_L tilde H u_R`) | exact / retained | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` |
| Staggered Dirac spectrum / Clifford algebra `{Γ_μ, Γ_ν} = 2δ_{μν} I_8` | exact / structural | `NATIVE_GAUGE_CLOSURE_NOTE.md` |
| SU(3) Casimirs: `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` | exact / retained | `YT_EW_COLOR_PROJECTION_THEOREM.md` |
| `g_bare = 1` (axiom) | axiom / exact | `MINIMAL_AXIOMS_2026-04-11.md` |
| 3D taste cube `V = {0,1}^3`, axis shifts `S_1, S_2, S_3` | exact / structural | `GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md` |

## B. Forbidden Proof Inputs (Explicit Prohibition)

| Forbidden Input | Reason for Prohibition | Effect if Used |
|---|---|---|
| `H_unit` or `H_unit`-to-top matrix-element identification | Prior audited-renaming failure | Circular: introduces top Yukawa by re-labeling |
| `yt_ward_identity`: `y_t_bare^2 = g_bare^2/(2 N_c)` | Explicitly banned by loop goal | The only known substrate-native Yukawa constraint; its forbiddance is the core challenge |
| `alpha_LM` | Plaquette-derived coupling | Imports scale from MC calibration |
| Plaquette/tadpole coupling routes (`<P>`, `u_0`) | MC calibration surface | Import scale from MC |
| PDG `m_t` | Observed physical value | Calibration input, not derivation |
| Target `y_t` / SM running Yukawa target | Observed physical value | Calibration input, not derivation |
| Observed top-mass tuning records | MC calibration | Calibration input, not derivation |
| Fitted selectors | Empirical fitting | Calibration input, not derivation |
| Algebraic definitions of `y_t_bare` (e.g., `y_t_bare = m_t_bare / v_bare`) | Definitional circularity | Re-states the problem rather than solving it |

## C. Conditionally Admitted (with explicit role declared)

| Input | Role | Condition |
|---|---|---|
| `alpha_s(v) = 0.1033` (derived via plaquette chain) | Comparator / cross-check ONLY | Must NOT be used as a proof input for the mass pin; can appear only in a posterior consistency check |
| `v = 246.28 GeV` (derived via plaquette chain) | Declared substrate input with separate audit status | May appear in Yukawa readout `y_t = sqrt(2) m_t / v` but not in the mass-pin derivation itself |
| SM RGE beta functions (textbook) | Literature bridge for RG running | Must be declared as literature bridge, not substrate derivation |

## D. Key Structural Facts Relevant to the Search

1. **Yukawa monomial existence**: The SM one-Higgs theorem establishes that the `bar Q_L tilde H u_R` monomial is gauge-allowed. This determines the *form* of the top Yukawa coupling but NOT its coefficient.

2. **Ward identity status**: The identity `y_t_bare^2 = g_bare^2/(2 N_c) = 1/6` IS derivable from the substrate (D16 + D17 + D12 + S2 in the axiom chain). Its forbiddance is the explicit constraint of this loop. The loop seeks alternative routes that do not pass through this identity.

3. **Substrate determines gauge structure, not Yukawa coefficients**: The `Cl(3)/Z^3` substrate fully determines the gauge group (SU(3) x SU(2)_L x U(1)_Y) and the matter representations. Gauge symmetry does not fix the Yukawa coefficients — this is a standard QFT fact that applies here as well.

4. **Spectral structure**: The staggered Dirac operator `D` on `Z^3` has eigenvalues that depend on both the bare mass `m_0` and the gauge configuration `{U_μ(x)}`. The mass-gap structure does not produce a "canonical" heavy mass eigenvalue without additional constraints.

5. **Taste degeneracy**: On `Z^3`, the 8 staggered taste species all carry the same bare mass `m_0`. There is no taste-dependent mass splitting that could identify one taste as "the top quark" with a specific pinned mass.

## E. Import Summary for No-Go Claim

The five attack frames (spectral, topological, taste, representation, anomaly)
draw exclusively from section A permitted inputs. The no-go conclusion holds
on the retained surface with no forbidden inputs. All five frames reach the
same obstruction (Yukawa coupling freedom; see NO_GO theorem note).
