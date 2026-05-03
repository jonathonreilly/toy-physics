# Assumptions and Imports — Cycle 20 (Route B)

## Retained / exact-support inputs (load-bearing, cited at one hop)

| Premise | Class | Source |
|---|---|---|
| Derived SM matter content and conditional EWSB harness | exact/support | [`UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md`](../../../../docs/UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md) |
| Doubled-Y normalization and `Q = T_3 + Y/2` convention | support/convention | [`LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md`](../../../../docs/LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md) |
| One-Higgs Yukawa gauge-selection boundary | bounded/support | [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](../../../../docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md) |
| Higgs `Y_H=+1` from LHCM hypercharges plus admitted Yukawa structure | support theorem | [`HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md`](../../../../docs/HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md) |
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

## Branch-local hypotheses used by Route B

These are branch-local hypotheses for the candidate, not repo-wide axioms or
retained premises. Each becomes a named residual obstruction in the cycle-20
note for future research.

| Premise | New name | Status |
|---|---|---|
| Z3 acts on the generation index of quark-bilinear scalars (extending Koide Z3 from charged-lepton selector slice to generation labels of u_R, d_R, e_R) | NO1 | branch-local structural HYPOTHESIS |
| The three condensates `⟨q̄_L u_R⟩`, `⟨q̄_L d_R⟩`, `⟨l̄_L e_R⟩` have equal magnitude | NO2 | branch-local structural HYPOTHESIS |
| The strong-coupling sector of the framework produces the multi-channel condensate with magnitude consistent with EW scale (NOT m_top, NOT v as input) | NO3 | inherited from cycle 08 O1 |

## Status

```yaml
all_retained_inputs_at_one_hop: true
forbidden_imports_audit_clean: true
branch_local_hypotheses_named: 3 (NO1, NO2, NO3)
honest_status: open-gate stretch attempt with named residual obstructions
```
