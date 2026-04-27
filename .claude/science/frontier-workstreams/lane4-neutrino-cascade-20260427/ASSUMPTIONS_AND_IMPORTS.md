# Assumptions And Imports

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| `Cl(3)` on `Z^3` framework axiom | Base structural surface | zero-input structural | repo retained framework notes and atlas | Yes | Yes | Already retained upstream | Reuse only |
| Three generations and active neutrino count | Neutrino sector cardinality and `N_eff` support | retained support | `THREE_GENERATION_STRUCTURE_NOTE.md`, `N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md` | Yes | Yes | Already retained upstream | Reuse only |
| `alpha_LM`, `v_EW`, plaquette-derived constants | Quantitative mass-scale inputs | framework-derived | `USABLE_DERIVED_VALUES_INDEX.md`, `NEUTRINO_MASS_DERIVED_NOTE.md` | Yes | Yes | Retire only by upstream plaquette/EW closure, not in Lane 4 | Reuse with qualifier |
| `y_nu^eff = g_weak^2/64` | Local coefficient in atmospheric benchmark | retained support | `NEUTRINO_MASS_DERIVED_NOTE.md` | Yes | Yes for benchmark, no for pure Dirac closure | Distinguish local/seesaw use from direct Dirac mass use | Kept, guarded |
| `mu_current = 0` | Current-stack Majorana zero law | exact current-stack theorem | `NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` | Yes | Yes for Dirac/Majorana fork | A nonzero charge-2 primitive would change the surface | Kept as fork boundary |
| Diagonal right-handed Majorana benchmark | Atmospheric-scale support route | bounded/support Majorana extension surface | `DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md` | Yes | Not enough for global closure | Derive nonzero charge-2 primitive and full `M_R` texture | Open |
| Normal ordering | Observable-bound input | retained support | `NEUTRINO_MASS_DERIVED_NOTE.md`, `NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md` | Yes | Yes for bounds | Already retained as structural prediction on current package | Reuse with qualifier |
| PMNS unitarity | Bound on `m_beta` and `m_betabeta` | zero-input structural / SM convention | neutrino observable bounds note | Yes | Yes for bounds | Standard structural input | Reuse |
| Observed neutrino splittings and PMNS angles | Comparators only | observational comparator | NuFit/PDG values cited in existing notes | No for new no-go | No | Keep out of derivation chain | Comparator only |
| One-Higgs Dirac mass convention `m = y v/sqrt(2)` | Guard against direct-Dirac misuse | retained/exact SM gauge-selection convention | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` | Yes for fork no-go | Yes | Already retained upstream | Reuse |

## Open Load-Bearing Imports

- Nonzero Majorana/seesaw activation: not derived on the current retained
  stack.
- Full off-diagonal `M_R` texture: not derived; needed for `Delta m^2_21`.
- Tiny Dirac `Y_nu` activation law: not derived; needed if the lane chooses
  the Dirac route.
- PMNS value-selection law: current retained bank leaves the nontrivial
  character current unselected.

## Lane 2 Atomic Imports Added In Cycle 2

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Electron mass `m_e` | Sets the Rydberg energy scale linearly | observational comparator in current scaffold | `ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md`, Lane 2 open stub | Yes | Yes | Charged-lepton/electron mass retention | Open |
| `alpha_EM(M_Z)=1/127.67` | Existing high-energy EW coupling value | framework-derived | `USABLE_DERIVED_VALUES_INDEX.md` | Yes, but not sufficient | Bridge only | QED running / low-energy transport to `alpha(0)` | Kept with firewall |
| Low-energy atomic `alpha(0)` | Coulomb coupling in Rydberg formula | standard comparator in current firewall | atomic standard formula | Yes | Yes | Derive or bridge from retained EW package | Open |
| Nonrelativistic Schrodinger/Coulomb limit | Atomic Hamiltonian in physical units | scaffold import | `ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md` | Yes | Yes | Retain physical-unit NR limit from framework substrate | Open |

## Lane 5 Hubble Imports Added In Cycle 3

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| `L = (H_inf/H_0)^2` | Exact bridge exposing the two required degrees | retained structural identity | `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`, `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md` | Yes | Yes | Already retained as structural bridge, not numerical closure | Reuse with firewall |
| `(C1)` primitive Clifford/CAR coframe response | Absolute-scale premise for numerical `H_inf`/`R_Lambda` | open gate | `HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md` | Yes | Yes | Derive metric-compatible primitive Clifford/CAR coframe response with natural phase/action units | Open |
| `(C2)` right-sensitive `Z_3` doublet-block selector | Dimensionless cosmic-history-ratio route through bounded cascade | open gate | `HUBBLE_LANE5_ETA_RETIREMENT_GATE_AUDIT_NOTE_2026-04-26.md` | Yes | Yes, unless `(C3)` lands | Derive right-sensitive selector and retire surrounding cascade dependencies | Open |
| `(C3)` direct cosmic-`L` route | Alternative dimensionless route to `L` | no active route | `HUBBLE_LANE5_C3_VACUUM_TOPOLOGY_NO_ACTIVE_ROUTE_NOTE_2026-04-27.md` | Yes if opened | Yes, as alternative to `(C2)` | Fresh vacuum/topology or inflation-history premise | Empty/open |
| Structural lock `H(a)=H_0 E(a;L,R)` | Late-time falsifier and consistency relation | proposed-retained support | `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md` | Yes for falsifier, no for numerical closure | No | Keep separate from numerical `H_0` derivation | Guarded |
| Planck 2018 comparator triple | Numerical family demonstration only | comparator | existing Hubble runners/status notes | No | No | Keep out of derivation chain | Comparator only |

## Lane 3 Quark Imports Added In Cycle 4

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| retained `m_t` and `y_t/g_s = 1/sqrt(6)` | Top-channel retained anchor and Ward template | retained | `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, Lane 3 open stub | Yes | Yes | Already retained for top only | Reuse with top-only scope |
| Down-type CKM-dual ratios | Strong down-type ratio support | bounded bridge | `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` | Yes | Yes | Retain GST, `5/6` bridge, and scale selection | Open |
| Up-type partition/scalar support | Up-sector ratio support | bounded candidate grammar | `QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md`, review packet | Yes | Yes | Derive partition or scalar amplitude law from retained core | Open |
| Species-uniform b-Yukawa scope analysis | Negative boundary for uniform Ward reuse | retention-analysis no-go | `YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md` | Yes | Yes | Derive species-differentiated Yukawa Ward primitive | Open |
| PDG quark mass values | Comparator/sensitivity only | observational comparator | existing quark runners | No | No | Keep out of derivation chain | Comparator only |
