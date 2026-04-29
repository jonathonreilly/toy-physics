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

## Lane 1 Hadron Imports Added In Cycle 5

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Confinement at `T=0` | Structural prerequisite for bound hadrons | retained structural theorem | `CONFINEMENT_STRING_TENSION_NOTE.md` | Yes | Yes | Already retained as confinement, not mass closure | Reuse with firewall |
| `sqrt(sigma) ~= 465 MeV` | Bounded scale support | bounded bridge | `CONFINEMENT_STRING_TENSION_NOTE.md` | Yes | Yes as scale support | Tighten EFT/screening bridge to retained | Open/bounded |
| Light-quark masses | GMOR and nucleon mass inputs | open dependency | Lane 3 firewall | Yes | Yes | Retain Lane 3 light-quark masses | Open |
| Chiral condensate `Sigma` and `f_pi` | GMOR pion-mass closure inputs | open dependency | Lane 1 open stub | Yes | Yes | Derive chiral-SB inputs from staggered-Dirac partition | Open |
| Hadronic-scale matching and correlator extraction | Proton/neutron/spectrum closure | open methodology bridge | Lane 1 open stub | Yes | Yes | Instantiate lattice-QCD-equivalent calculation on framework substrate | Open |
| Observed hadron masses | Spectral-coefficient sensitivity examples | comparator | standard hadron values | No | No | Keep out of derivation chain | Comparator only |

## Lane 4F Sigma m_nu Imports Added In Cycle 6

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| `L = Omega_Lambda,0 = (H_inf/H_0)^2` | Structural variable in Sigma m_nu functional form | retained structural identity | `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`; `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` | Yes | Yes for structural form | Already retained as structural variable, not numerical closure | Reuse |
| `R = Omega_r,0` | Radiation fraction in matter-budget split | admitted cosmology layer | `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md` | Yes | Yes for numerical Sigma m_nu | Retain radiation/CMB readout or keep admitted | Open/admitted |
| `h = H_0 / 100 km/s/Mpc` | Converts Omega_nu h^2 to Sigma m_nu | open Lane 5 variable | Lane 5 two-gate dependency firewall and Hubble C1/C2 audits | Yes | Yes for numerical Sigma m_nu | Close Lane 5 `(C1)` plus `(C2)` or `(C3)` | Open |
| `Omega_b`, `Omega_DM` | Matter-budget split subtracting baryon and dark matter fractions | admitted observational layer | Lane 4F theorem-plan note | Yes | Yes for numerical Sigma m_nu | Retain baryon and dark-matter density fractions or keep admitted | Open/admitted |
| `C_nu = 93.14 eV` | Standard CMB-neutrino relic conversion constant | admitted convention | Lane 4F functional-form note | Yes | Yes for conventional physical-units form | Derive from retained `N_eff`, `T_CMB`, entropy transfer, and unit conventions | Admitted convention |

## Lane 5 C1 A1 Imports Added In Cycle 7

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Bulk finite Grassmann / CAR structure | Starting point for A1 stretch attempt | accepted framework input | `MINIMAL_AXIOMS_2026-04-11.md` | Yes | Yes | Already in `A_min` | Reuse |
| `P_A H_cell`, rank-four primitive boundary block | Boundary target for C1 G1 edge-statistics principle | retained/support Planck packet | `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`; `HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md` | Yes | Yes | Already identified, but not CAR-forcing by rank alone | Reuse with boundary |
| `P_A` Clifford/CAR module-morphism or reducing-subspace property | Newly exposed missing premise for A1 direct descent | open import | `HUBBLE_LANE5_C1_A1_GRASSMANN_BOUNDARY_CAR_OBSTRUCTION_NOTE_2026-04-29.md` | Yes | Yes for A1 positive closure | Prove `P_A` reduces selected edge modes from coframe response or another retained primitive | Open |
| Non-CAR rank-four semantics | Countermodel class for rank-only closure | exact negative boundary | `AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md`; A1 obstruction runner | Yes for no-go | Yes | Closed as a direct A1 shortcut | Guardrail |

## Lane 5 C1 A2 Imports Added In Cycle 8

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| `g_bare = 1` and `beta = 6` | Dimensionless Wilson gauge normalization tested as possible action-unit anchor | retained support | `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`; `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`; A2 runner | Yes for A2 test | Not sufficient for `(C1)` | Pair with a physical metrology/carrier theorem; cannot alone choose `kappa` | Reuse with guardrail |
| Plaquette `<P>`, `u_0`, `alpha_LM`, `alpha_s(v)` | Dimensionless same-surface lattice/coupling data tested as possible action-unit anchor | computed lattice input / framework-derived support | `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`; `scripts/canonical_plaquette_surface.py`; A2 runner | Yes for A2 test | Not sufficient for `(C1)` | Need theorem coupling plaquette action to primitive boundary/action carrier | Reuse with guardrail |
| Minimal APBC hierarchy block and `(7/8)^(1/4)` | Dimensionless hierarchy/tadpole support tested as possible action-unit anchor | retained support | `HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`; A2 runner | Yes for A2 test | Not sufficient for `(C1)` | Need action-unit metrology theorem, not only dimensionless APBC scaling | Reuse with guardrail |
| `P_A` coefficient `c_cell = 1/4` | Projected primitive boundary coefficient in the A2 test | retained/proposed_retained support on conditional Planck packet | `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`; `PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md`; A2 runner | Yes | Yes | Coupled carrier/metrology theorem or conditional carrier axiom | Open/conditional |
| Physical clock/source/action metrology map selecting dimensional `kappa` | Newly exposed missing premise for A2 positive closure | open import | `HUBBLE_LANE5_C1_A2_ACTION_UNIT_METROLOGY_OBSTRUCTION_NOTE_2026-04-29.md`; `PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md` | Yes | Yes for `(C1)` G2 | Derive a non-rescaling-invariant map from lattice action to the primitive boundary/action carrier | Open |

## Lane 5 C1 A4 Imports Added In Cycle 9

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Primitive residual `Z_2` parity/half-zone gate | Selector tested as possible CAR/coframe derivation route | conditional support theorem | `AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`; A4 runner | Yes for A4 test | Not sufficient for `(C1)` | Pair with a native Clifford/CAR coframe-response theorem | Reuse with guardrail |
| Primitive-CAR edge carrier | Conditional positive carrier class in which the parity gate fixes `c_Widom=1/4` | conditional support theorem | `AREA_LAW_PRIMITIVE_CAR_EDGE_IDENTIFICATION_THEOREM_NOTE_2026-04-25.md`; `AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md` | Yes | Yes | Derive the native CAR/coframe response rather than assume carrier semantics | Open/conditional |
| Orientation/statistics lift from even `Z_2` gate to odd Clifford/CAR coframe generators | Newly exposed missing premise for A4 positive closure | open import | `HUBBLE_LANE5_C1_A4_PARITY_GATE_CAR_BOUNDARY_NOTE_2026-04-29.md` | Yes | Yes for `(C1)` G1 | Prove a theorem that the primitive parity gate determines metric-compatible odd edge generators on `P_A H_cell` | Open |
| Non-CAR rank-four semantics compatible with the same gate data | Countermodel class for gate-only closure | exact negative boundary | A4 runner; `PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md` | Yes for no-go | Yes | Closed as a direct A4 shortcut | Guardrail |

## Lane 5 C1 A5 Imports Added In Cycle 10

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Hamming-weight-one `P_A` packet | Active block tested for direct inherited coframe response | retained/proposed_retained support | `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`; A5 runner | Yes | Yes | Already selected as carrier; not by itself a reducing odd-coframe module | Reuse with guardrail |
| Natural full-cell Boolean/Jordan-Wigner odd coframe generators | Candidate direct inherited `Cl_4` response from `H_cell=(C^2)^4` | proof infrastructure / candidate route | A5 runner | Yes for A5 test | Not sufficient for `(C1)` | Need a different intrinsic active-block theorem, quotient/bilinear theorem, or carrier premise | Blocked as direct restriction |
| Intrinsic active-block metric-compatible `Cl_4` law | Newly sharpened missing premise after A5 | open import | `HUBBLE_LANE5_C1_A5_BOOLEAN_COFRAME_RESTRICTION_OBSTRUCTION_NOTE_2026-04-29.md`; `PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md` | Yes | Yes for `(C1)` G1 | Derive `Cl_4` response directly on `P_A H_cell`, not by compressing full-cell odd maps | Open |

## Lane 5 C1 A6 Imports Added In Cycle 11

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| Number-preserving bilinears `a_i^dagger a_j` on the one-particle `P_A` sector | Candidate quotient/intrinsic active-block route after A5 | exact support/boundary theorem | `HUBBLE_LANE5_C1_A6_BILINEAR_ACTIVE_BLOCK_SUPPORT_BOUNDARY_NOTE_2026-04-29.md` | Yes | Not sufficient for `(C1)` | Add primitive metric/orientation/phase selector and metrology theorem | Support only |
| Primitive metric/orientation/phase selector on the active `M_4(C)` algebra | Newly exposed missing selector for the bilinear route | open import | A6 note and runner | Yes | Yes for `(C1)` G1 | Derive which active bilinear combinations are the coframe axes and oriented CAR pairings | Open |
| Dimensional action-unit map on the bilinear active-block route | Newly exposed metrology dependency remains after A6 | open import | A2 and A6 notes | Yes | Yes for `(C1)` G2 | Derive non-rescaling-invariant clock/source/action metrology | Open |
