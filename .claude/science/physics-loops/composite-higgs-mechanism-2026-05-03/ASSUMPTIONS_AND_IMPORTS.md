# Assumptions and Imports — Cycle 20 (Route B)

## Retained / exact-support inputs (load-bearing, cited at one hop)

| Premise | Class | Source |
|---|---|---|
| Cycle 06 derived rep `Q_L:(2,3)_{+1/3}, L_L:(2,1)_{-1}, u_R:(1,3)_{+4/3}, d_R:(1,3)_{-2/3}, e_R:(1,1)_{-2}, ν_R:(1,1)_0` | exact-support | `SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md` |
| Cycle 07 conditional `Q = T_3 + Y/2` | conditional-support | `CONDITIONAL_EWSB_Q_FORMULA_ON_DERIVED_REP_THEOREM_NOTE_2026-05-02.md` (PR #407) |
| Cycle 08 quantum-number match for q̄_L u_R singlet | exact-support | `COMPOSITE_HIGGS_QUANTUM_NUMBER_MATCH_STRETCH_ATTEMPT_NOTE_2026-05-02.md` (PR #409) |
| Cycle 15 `g_2² \|_lattice = 1/(d+1) = 1/4` | retained | `YT_EW_COLOR_PROJECTION_THEOREM_NOTE.md` |
| Koide Z3 scalar potential (V₀ + linear + 3m²/2 + m³/6) | exact-support | `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md` |
| EW Fierz channel decomposition (N_c² - 1)/N_c² = 8/9 adjoint fraction | exact group theory | `EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md` |
| Native gauge structure SU(3) × SU(2) × U(1) | retained | `NATIVE_GAUGE_CLOSURE_NOTE.md` |

## Admitted-context external (allowed; not load-bearing on retention)

| Item | Role | Source |
|---|---|---|
| SU(N) representation theory | textbook fusion arithmetic | Halzen-Martin, Sternberg |
| SM Yukawa structural form `q̄_L Φ̃ u_R + h.c.` | structural form (not coefficient) | Peskin-Schroeder ch. 20 |
| Goldstone theorem (3 broken SU(2)×U(1) → 1 unbroken U(1)_em) | textbook | Weinberg vol. 2 |
| Cube root of unity ω = exp(2πi/3) arithmetic (1 + ω + ω² = 0) | textbook | standard |
| Mean-field / NJL Lagrangian factorization for fermion bilinears | structural form | Nambu-Jona-Lasinio, NJL |

## Forbidden imports (must not be load-bearing)

| Item | Why forbidden | Allowed role here |
|---|---|---|
| PDG `m_top = 173 GeV` | observed value | NOT used at all |
| PDG `m_H = 125 GeV` | observed value | NOT used at all |
| PDG `v = 246 GeV` | observed value | NOT used at all |
| PDG `m_W = 80.4 GeV` | observed value | NOT used at all |
| PDG `m_Z = 91.2 GeV` | observed value | NOT used at all |
| BHL 1990 `m_top ~ 600 GeV` prediction | literature numerical comparator | named ONLY in obstruction documentation as admitted-context external authority |
| Hill 1991 / Holdom 1985 walking technicolor | literature | NOT cited |
| Koide ratio fitting | fitted selector | NOT used |

## Load-bearing premises introduced by Route B (NEW)

These are the premises Route B introduces beyond cycles 06/07/08/15/16/17/18.
Each becomes a named obstruction in the cycle-20 note for future research.

| Premise | New name | Status |
|---|---|---|
| Z3 acts on the generation index of quark-bilinear scalars (extending Koide Z3 from charged-lepton selector slice to generation labels of u_R, d_R, e_R) | NO1 | structural HYPOTHESIS — load-bearing premise |
| The three condensates `⟨q̄_L u_R⟩`, `⟨q̄_L d_R⟩`, `⟨l̄_L e_R⟩` have equal magnitude | NO2 | structural HYPOTHESIS — Z3-symmetry assertion |
| The strong-coupling sector of the framework produces the multi-channel condensate with magnitude consistent with EW scale (NOT m_top, NOT v as input) | NO3 | inherited from cycle 08 O1 |

## Status

```yaml
all_retained_inputs_at_one_hop: true
forbidden_imports_audit_clean: true
new_load_bearing_premises_named: 3 (NO1, NO2, NO3)
honest_status: stretch attempt with named obstructions
```
