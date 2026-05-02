# Campaign-Wide Assumptions And Imports

This file is the campaign-wide ledger of what may be consumed as proof input
and what cannot. Each cycle must extend a per-block subset to its own
`ASSUMPTIONS_AND_IMPORTS_block<NN>.md` under the cycle directory.

## Retained Primitives (allowed as proof inputs)

| Item | Role | Source | Notes |
|---|---|---|---|
| graph_first_su3_integration_note | retained framework | docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md | structural SU(3) closure on selected axis; td=312 |
| graph_first_selector_derivation_note | retained selector | docs/GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md | selector unique up to graph automorphism; td=311 |
| native_gauge_closure_note | retained gauge closure | docs/NATIVE_GAUGE_CLOSURE_NOTE.md | native gauge closure; td=308 |
| cpt_exact_note | retained exact theorem | docs/CPT_EXACT_NOTE.md | exact discrete symmetry |
| electric_sign_law_note | retained | docs/ELECTRIC_SIGN_LAW_NOTE.md | propagator/charge sign law |
| electrostatics_card_note | retained | docs/ELECTROSTATICS_CARD_NOTE.md | Coulomb-law sector retained |
| distance_law_3d_64_closure_note_2026-04-11 | retained | distance_law (1/L^p attenuation, gravity from phase) | |
| dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_note_2026-04-18 | retained | dm-neutrino source surface | |
| charged_lepton_koide_ratio_source_selector_firewall_note_2026-04-27 | retained | charged-lepton Koide selector firewall | |
| charged_lepton_radiative_tau_selector_firewall_note_2026-04-26 | retained | charged-lepton tau selector firewall | |
| atomic_rydberg_dependency_firewall_note_2026-04-27 | retained | dep firewall pattern reference | |

## Recently Established Exact Identities (PR #249, PR #253)

| Item | Role | Source |
|---|---|---|
| Fierz channel exact (N_c²-1)/N_c² | exact group-theory derivation | PR #249 |
| SU(2)²×U(1)_Y anomaly cancellation for LH doublets | exact algebraic identity | PR #253 |

## Admitted Conventions (narrow non-derivation role only)

| Item | Role | Convention | Restriction |
|---|---|---|---|
| g_bare = 1 | Wilson-action canonical normalization input | β = 2N_c/g_bare² = 6 | structural choice, not phenomenological fit |
| Q = T_3 + Y/2 | SM charge-formula readout convention | Halzen-Martin convention | identification of eigenvalues with Y is what blocks LHCM closure |
| Sommer scale r_0 = 0.5 fm | scale-setting external input | external matching number | this is a load-bearing import for alpha_s lane; NOT an axiom-only route |
| MSbar 4-loop QCD running | running bridge to M_Z | standard high-loop QCD beta + threshold matching | retained running bridge, not framework-native |

## Forbidden Imports (cannot be load-bearing proof inputs)

| Item | Why forbidden |
|---|---|
| PDG observed alpha_s, m_W, m_Z, theta_W, ... | target observables |
| Literature numerical comparators | only allowed as audit comparators with explicit role label |
| Fitted selectors | tuning to target |
| Admitted unit conventions when retention depends on them | bare retention requires unit-derivation |
| Same-surface A² family arguments for CKM | sister-surface circular |
| u_0 plaquette-tadpole as running coupling input | decoration trap (audited_decoration) |
| alpha_LM = alpha_bare/u_0 as authority | decoration trap |
| alpha_bare/u_0² as alpha_s definition | decoration trap |

## Open Imports (per-candidate, populated per cycle)

Will be populated per cycle in
`.claude/science/physics-loops/audit-backlog-campaign-20260502/cycle<NN>/ASSUMPTIONS_block<NN>.md`.
