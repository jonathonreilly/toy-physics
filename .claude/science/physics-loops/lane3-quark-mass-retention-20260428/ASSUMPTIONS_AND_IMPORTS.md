# Lane 3 Assumptions And Imports

**Updated:** 2026-04-28T07:30:44Z
**Branch:** `physics-loop/lane3-quark-mass-retention-block01-20260428`
**Head:** `e3c108de`

This ledger uses the physics-loop schema. It separates retained framework
inputs, support-only bridges, comparator values, and hidden selectors that
block retained five-mass closure.

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| `Cl(3) x Z^3` retained matter/gauge surface | Primitive framework surface for gauge, generation, and Ward notes | zero-input structural | `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, `THREE_GENERATION_STRUCTURE_NOTE.md` | yes | yes | already retained on current package surface | usable retained input |
| `N_c = 3`, `N_pair = 2`, `N_quark = 6` | Structural counts in CKM, EW, and quark formulas | retained support | `CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`, `CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md` | yes | yes | atlas reuse | usable retained support |
| `alpha_s(v) = 0.103303816122` | Canonical same-surface coupling in down-type ratios and CKM atlas | framework-derived | `ALPHA_S_DERIVED_NOTE.md`, `QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25.md` | yes | yes | already retained for current package role | usable retained input |
| CKM atlas/axiom package | Supplies retained mixing magnitudes and CP geometry | retained support / promoted quantitative package | `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` and canonical harness index | yes for bridge routes | yes as cross-check, not as mass derivation | atlas reuse plus explicit mass-bridge theorem | usable support; not mass closure |
| `m_t` and `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)` | Top-channel retained mass/Ward anchor | retained / exact support theorem | `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, Lane 3 open-lane stub | yes | yes for absolute-scale chain | already retained for top only | top-channel scoped; not species-uniform |
| Three `hw=1` generation structure | Supplies physical three-generation sectors | retained structural theorem | `THREE_GENERATION_STRUCTURE_NOTE.md` | yes | yes | atlas reuse plus new flavor/source primitive | retained structure, but no hierarchy |
| One-Higgs Yukawa gauge selection | Gives allowed SM Dirac operator skeleton | exact support theorem | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` | yes | yes | combine with new Ward/source theorem | usable boundary; leaves Yukawa matrices free |
| Down-type GST / NNI relation `|V_us|^2 = m_d/m_s` | Converts CKM `V_us` to `m_d/m_s` | support-only / structural bridge | `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`, `CKM_FROM_MASS_HIERARCHY_NOTE.md` | yes for down route | yes for retained down ratios | theorem route deriving GST on retained framework surface | open load-bearing bridge |
| `5/6 = C_F - T_F` bridge `|V_cb| = (m_s/m_b)^(5/6)` | Converts CKM `V_cb` to `m_s/m_b` | bounded support | `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`, `QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25.md` | yes for down route | yes for retained down ratios | non-perturbative theorem at lattice scale | open Nature-grade blocker |
| Threshold-local self-scale convention | Comparator scale for strong down-type numerical match | admitted normalization / observational comparator convention | `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` | yes for match statement | yes if claiming precision | exact scale-selection theorem or demote to bounded comparator | open scale-selection blocker |
| Up-type interior partition `(f_12, f_23)` | Bounded up-sector extension | fitted input / support-only | `UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md`, review packet | yes for up route | yes | derive partition from retained source law or retire route | not retained |
| Up-type scalar amplitude shortlist (`7/9`, `sqrt(3/5)`, native projector laws) | Candidate law for `m_u/m_c` and related up-sector ratios | support-only / bounded candidate grammar | `QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md`, native-expression and affine no-go notes | yes for 3B | yes | first-principles scalar-law theorem or no-go narrowing | open |
| Route-2 endpoint readout map entry `beta_E / alpha_E = 21/4` | Reduced missing readout primitive for up-sector endpoint law | exact boundary plus unresolved map entry | `QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md`, `QUARK_ROUTE2_EXACT_TIME_COUPLING_NOTE_2026-04-19.md`, `QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md` | yes for route-2 scalar law | yes if route used | derive E-center ratio `gamma_T(center)/gamma_E(center) = -8/9` or supply a new readout/source primitive | minimal naturality route closed negatively; open hard residual remains |
| Species-differentiated Yukawa Ward primitive | Needed to avoid species-uniform `m_b` failure and set absolute non-top scales | unsupported import / missing theorem | `YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`, Lane 3 stub | yes | yes | 3C theorem or exact no-go/demotion | open hard residual |
| PDG quark masses | Used only to compare bounded matches and expose failure modes | observational comparator | existing quark runners and notes | no as derivation input | no for proof, yes for review context | keep comparator-only; do not import into theorem | firewall |
| Literature QCD/RGE corrections | Standard correction context when scale/running is discussed | standard correction / literature theorem if used | down-type and YT notes | no unless a route requires it | not for zero-input closure | record in `LITERATURE_BRIDGES.md` if used | none added in this block so far |

## Immediate Audit Result

The 2026-04-27 Lane 3 firewall is controlling: CKM closure, bounded down-type
ratios, bounded up-type extensions, and top Ward species-uniformity do not
retain `m_u`, `m_d`, `m_s`, `m_c`, or `m_b`.

The highest-leverage unresolved imports for this block are:

1. species-differentiated Yukawa Ward primitive for 3C;
2. up-type scalar/readout law for 3B;
3. non-perturbative `5/6` bridge plus threshold-local scale-selection theorem
   for 3A.
