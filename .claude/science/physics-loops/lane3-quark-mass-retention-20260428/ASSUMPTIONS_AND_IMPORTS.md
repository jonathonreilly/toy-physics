# Lane 3 Assumptions And Imports

**Updated:** 2026-04-28T09:26:03Z
**Branch:** `physics-loop/lane3-quark-mass-retention-20260428-block10-20260428`
**Head:** block-10 working checkpoint; see `git log`

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
| `S_3` action on `hw=1` generation triplet, `A_1 + E` | Tests whether retained generation symmetry can itself stratify quark Ward eigenvalues | exact support theorem | `S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`, `THREE_GENERATION_STRUCTURE_NOTE.md`, `QUARK_GENERATION_EQUIVARIANT_WARD_DEGENERACY_NO_GO_NOTE_2026-04-28.md` | yes for 3C equivariant route | yes if claiming generation-stratified Ward values | add a source/readout/symmetry-breaking primitive that orients or splits the `E` doublet | equivariant route closed negatively; carrier alone gives at most singlet/doublet split |
| Oriented `C3[111]` Ward splitter on `hw=1` | Smallest exact local primitive tested for splitting the `S_3` `E` doublet | exact support/boundary theorem | `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, `QUARK_C3_ORIENTED_WARD_SPLITTER_SUPPORT_NOTE_2026-04-28.md` | yes for the 3C source/readout route | yes only if promoted with a source/readout law | derive a physical source law for `c` and `b/a`, or a readout theorem mapping cyclic Fourier strata to quark Yukawa channels | exact splitter support only; coefficients remain free and mass closure remains open |
| `C3` Hermitian circulant hierarchy carrier plus A1/P1 | Tests whether inherited circulant hierarchy support can become quark Ward source law | exact support/boundary theorem; A1/P1 remain open primitives | `YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`, `YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md`, `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`, `KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md`, `QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md` | yes for 3C source-law route | yes if claiming quark generation-stratified Ward identities | derive A1 or equivalent from quark Ward source, derive P1/readout for quark Yukawa amplitudes, and derive sector phases/scales | exact carrier support only; without those imports it can fit arbitrary real triples and does not predict quark masses |
| Koide A1 support scalar `1/2` to quark `C3` source ratio | Tests whether existing A1 support faces already type the quark source ratio `|q_quark|^2/a_quark^2 = 1/2` | exact current-bank no-go / support boundary | `KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`, `KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md`, `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`, `QUARK_C3_A1_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md` | yes for A1 source-law route | yes if claiming A1-derived quark Ward identities | prove a typed source-domain bridge from A1 support scalar to the physical quark Ward source ratio | no existing typed edge; adding it is new theorem content |
| Positive-parent square-root dictionary to quark P1 readout | Tests whether exact `M -> M^(1/2)` algebra already identifies quark Yukawa amplitudes | exact current-bank no-go / support boundary | `KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md`, `QUARK_C3_P1_POSITIVE_PARENT_READOUT_NO_GO_NOTE_2026-04-28.md`, `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` | yes for P1 readout route | yes if claiming quark `C3` source eigenvalues are physical Yukawa amplitudes | derive a retained positive quark `C3` parent and a physical readout theorem for `eig(M^(1/2))` | exact dictionary only; parent and readout edges remain new theorem content |
| One-Higgs Yukawa gauge selection | Gives allowed SM Dirac operator skeleton | exact support theorem | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` | yes | yes | combine with new Ward/source theorem | usable boundary; leaves Yukawa matrices free |
| Down-type GST / NNI relation `|V_us|^2 = m_d/m_s` | Converts CKM `V_us` to `m_d/m_s` | support-only / structural bridge | `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`, `CKM_FROM_MASS_HIERARCHY_NOTE.md` | yes for down route | yes for retained down ratios | theorem route deriving GST on retained framework surface | open load-bearing bridge |
| `5/6 = C_F - T_F` bridge `|V_cb| = (m_s/m_b)^(5/6)` | Converts CKM `V_cb` to `m_s/m_b` | bounded support | `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`, `QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25.md` | yes for down route | yes for retained down ratios | non-perturbative theorem at lattice scale | open Nature-grade blocker |
| Threshold-local self-scale convention | Comparator scale for strong down-type numerical match | admitted normalization / observational comparator convention | `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` | yes for match statement | yes if claiming precision | exact scale-selection theorem or demote to bounded comparator | open scale-selection blocker |
| One-loop transport between `m_s(2 GeV)/m_b(m_b)` and `m_s(m_b)/m_b(m_b)` | Exposes whether the `5/6` bridge is scale-blind or scale-selected | inherited comparator / admitted convention | `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`, `QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md` | yes for 3A scale audit | yes for retained down ratios | derive threshold-local scale selection or an RG-covariant transport theorem from framework primitives | inherited values only; not a derivation input |
| Up-type interior partition `(f_12, f_23)` | Bounded up-sector extension | fitted input / support-only | `UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md`, review packet | yes for up route | yes | derive partition from retained source law or retire route | not retained |
| Up-type scalar amplitude shortlist (`7/9`, `sqrt(3/5)`, native projector laws) | Candidate law for `m_u/m_c` and related up-sector ratios | support-only / bounded candidate grammar | `QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md`, native-expression and affine no-go notes | yes for 3B | yes | first-principles scalar-law theorem or no-go narrowing | open |
| STRC/RPSR reduced up-amplitude theorem | Exact retained support for a dimensionless up-sector reduced amplitude on the `1(+)5` projector carrier | exact support/boundary theorem | `STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`, `QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`, `QUARK_UP_AMPLITUDE_RPSR_MASS_RETENTION_BOUNDARY_NOTE_2026-04-28.md` | yes for 3B support | yes if claiming up-type mass ratios | derive an amplitude-to-Yukawa readout theorem and sector/scale bridge to the top Ward anchor | exact amplitude support only; not retained `m_u/m_c` or `m_c/m_t` closure |
| Route-2 endpoint readout map entry `beta_E / alpha_E = 21/4` | Reduced missing readout primitive for up-sector endpoint law | exact boundary plus unresolved map entry | `QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md`, `QUARK_ROUTE2_EXACT_TIME_COUPLING_NOTE_2026-04-19.md`, `QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md` | yes for route-2 scalar law | yes if route used | derive E-center ratio `gamma_T(center)/gamma_E(center) = -8/9` or supply a new readout/source primitive | minimal naturality route closed negatively; open hard residual remains |
| `R_conn = (N_c^2 - 1)/N_c^2 = 8/9` | Conditional source-domain bridge candidate for `gamma_T(center)/gamma_E(center) = -8/9` | retained support / conditional bridge | `RCONN_DERIVED_NOTE.md`, `QUARK_ROUTE2_RCONN_CENTER_RATIO_BRIDGE_OBSTRUCTION_NOTE_2026-04-28.md` | yes if used to select the E-center ratio | yes for this 3B route | prove a typed bridge from SU(3) connected color projection to the Route-2 E/T center endpoint ratio | conditional exact bridge only; source-domain identification remains open |
| Typed current-bank edge `R_conn -> gamma_T(center)/gamma_E(center)` | Would promote the Rconn conditional bridge into an actual Route-2 source-domain theorem | missing theorem / exact current-bank no-go | `QUARK_ROUTE2_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md` | yes for this 3B route | yes | add a new cross-domain source theorem or find an alternate readout primitive | current support bank has no typed edge; direct promotion closed negatively |
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
3. a new typed source-domain bridge theorem for
   `gamma_T(center)/gamma_E(center) = -R_conn`, because the current bank lacks
   this edge;
4. non-perturbative `5/6` bridge plus threshold-local scale-selection or
   RG-covariant transport theorem for 3A. Block 04 sharpened this into a
   scale-selection boundary: the threshold-local surface gives `p_self =
   0.832890...`, close to `5/6`, while the common-scale surface gives
   `p_same = 0.803802...`; exact `C_F - T_F` alone is not a scale theorem.
5. a generation source/readout/symmetry-breaking primitive for 3C. Block 05
   sharpened the equivariant obstruction: any `S_3`-equivariant Hermitian Ward
   endomorphism on `hw=1 ~= A_1 + E` has an `E` double degeneracy, and any
   diagonal `S_3`-equivariant readout is scalar. Block 06 supplies the exact
   oriented `C3[111]` normal form
   `W(a,b,c) = a I + b(C+C^2) + c(C-C^2)/(i sqrt(3))`; generic nonzero `c`
   splits the doublet, but `a,b,c` and the physical readout remain new
   source/readout theorem content rather than derived quark masses. Block 07
   adds the inherited `C3` circulant hierarchy carrier boundary: without A1/P1
   or an equivalent quark source/readout theorem the carrier can represent any
   real generation spectrum, while with A1/P1 it still leaves phase, scale,
   species assignment, and amplitude-vs-Yukawa readout open. Block 08 closes
   direct A1 support promotion negatively: existing Koide A1 faces all hit
   `1/2`, but no current typed edge maps that scalar to the quark `C3` Ward
   source ratio. Block 09 closes direct P1 promotion negatively: the
   positive-parent square-root dictionary is exact support, but the current
   bank supplies neither a physical quark `C3` parent nor a readout theorem
   identifying its square-root eigenvalues with quark Yukawa amplitudes.
   Block 10 records the constructive 3B support boundary: STRC/RPSR supplies
   an exact reduced up-amplitude law, but the current bank lacks the
   amplitude-to-Yukawa readout and sector/scale bridge needed for retained
   `m_u/m_c` or `m_c/m_t` closure.
