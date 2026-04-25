# Repository Audit — 2026-04-25

**Branch:** `claude/ai-methodology-capture-2026-04-25` (off origin/main at `9d0fbabf`)

**Capture timestamp:** 2026-04-25T13:08:20Z

---

## 1. Top-level repo structure

```
total 4840
drwxr-xr-x@   22 jonBridger  staff      704 Apr 25 09:01 .
drwxr-xr-x@  136 jonBridger  staff     4352 Apr 25 07:10 ..
drwxr-xr-x@    5 jonBridger  staff      160 Apr 18 14:05 .claude
-rw-r--r--@    1 jonBridger  staff       79 Apr 18 14:05 .git
-rw-r--r--@    1 jonBridger  staff      160 Apr 18 14:05 .gitignore
-rw-r--r--@    1 jonBridger  staff     2405 Apr 18 14:05 ARCHITECTURE_OPTIONS.md
-rw-r--r--@    1 jonBridger  staff     3780 Apr 18 14:05 AUTOPILOT_JANITOR_PROTOCOL.md
-rw-r--r--@    1 jonBridger  staff     7381 Apr 18 14:05 AUTOPILOT_PROTOCOL.md
-rw-r--r--@    1 jonBridger  staff     2269 Apr 18 14:05 AUTOPILOT_SUMMARY_PROTOCOL.md
-rw-r--r--@    1 jonBridger  staff  1208450 Apr 18 14:05 AUTOPILOT_WORKLOG.md
-rw-r--r--@    1 jonBridger  staff     1071 Apr 18 14:05 LICENSE
-rw-r--r--@    1 jonBridger  staff     8518 Apr 25 09:01 README.md
-rw-r--r--@    1 jonBridger  staff     1673 Apr 18 14:05 SCALING_BENCHMARK_TABLE.md
-rw-r--r--@    1 jonBridger  staff     2347 Apr 18 14:05 SCALING_FAILURE_MECHANISMS.md
-rw-r--r--@    1 jonBridger  staff     2247 Apr 18 14:05 SCALING_TARGETS.md
drwxr-xr-x@ 1387 jonBridger  staff    44384 Apr 25 09:05 docs
drwxr-xr-x@  572 jonBridger  staff    18304 Apr 18 18:13 logs
drwxr-xr-x@    7 jonBridger  staff      224 Apr 23 22:00 outputs
-rw-r--r--@    1 jonBridger  staff       27 Apr 23 22:00 requirements-release.txt
-rw-r--r--@    1 jonBridger  staff       24 Apr 18 14:05 requirements.txt
drwxr-xr-x@ 2091 jonBridger  staff    66912 Apr 25 09:01 scripts
-rw-r--r--@    1 jonBridger  staff  1196935 Apr 18 14:05 toy_event_physics.py
```

## 2. File counts by directory

| Directory | .md count | .py count | other |
|---|---|---|---|
| docs | 1465 | 0 | 9 |
| scripts | 1 | 2087 | 1 |
| logs | 3 | 0 | 628 |
| outputs | 3 | 0 | 3 |

## 3. Frontier runner inventory

**Total frontier_*.py:** 1030

**Sample (first 30):**

```
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_2d_dispersion.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_2d_gravity_sign_diagnosis.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3d_continuum_spectrum.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3d_convergence_test.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3d_dynamic_growth.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3d_laplacian_closure.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3d_two_body_superposition.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3plus1d_closure_card.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3plus1d_distance_law.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3plus1d_distance_wider.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3plus1d_h05_card.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_3plus1d_same_geometry_refinement.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_abcc_cp_phase_no_go_theorem.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_accessible_prediction.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_action_normalization.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_alpha_lm_geometric_mean_identity.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_alpha_s_determination.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_analytic_continuum_limit.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_anderson_phase_unscreened_periodic.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_angular_kernel_investigation.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_angular_kernel_underdetermination_nogo.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_anomaly_forces_time.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_architecture_portability_sweep.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_area_law_quarter_broader_no_go.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_atomic_helium_hartree_companion.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_atomic_helium_jastrow_companion.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_atomic_hydrogen_helium_probe.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_atomic_hydrogen_lattice_companion.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_axioms_16card.py
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/scripts/frontier_background_independence.py
```

## 4. docs/ subdirectory map

```
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/ai_methodology
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/ai_methodology/raw
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes/action-law
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes/coin-walks
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes/controls
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes/generated-geometry
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes/mirror
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes/moonshots
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes/ordered-lattice
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/lanes/staggered
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/publication
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/publication/ci3_z3
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/repo
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/work_history
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/work_history/atomic
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/work_history/ckm
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/work_history/dm
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/work_history/pf
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/work_history/repo
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/docs/work_history/yt
```

## 5. Top-level theorem-grade docs by category (filename pattern matches)

- `*THEOREM*`: 234 files
- `*NO_GO*`: 45 files
- `*OBSTRUCTION*`: 34 files
- `*CLOSURE*`: 66 files
- `*BRIDGE*`: 60 files
- `*NOTE*`: 1276 files

## 6. Git activity summary

**Total commits on origin/main:** 2658

**Earliest commit:** 2026-03-13 14:10:05 -0400 7a5f1dca Initial commit

**Latest commit:** 2026-04-25 08:21:06 -0400 9d0fbabf dm: land freezeout-bypass support lane and SU(3) obstruction

**Commits per day (recent):**

```
  12 2026-04-12
  12 2026-04-13
  22 2026-04-14
  65 2026-04-15
  50 2026-04-16
  40 2026-04-17
  55 2026-04-18
  11 2026-04-19
   1 2026-04-20
   1 2026-04-21
  13 2026-04-22
   7 2026-04-23
  26 2026-04-24
  21 2026-04-25
```

**All branches on origin (with codex/* etc.):**

```
  origin/HEAD -> origin/main
  origin/afternoon-4-21
  origin/afternoon-4-21-proposal
  origin/alpha-lm-geometric-mean-identity
  origin/autonomous-loop-index-2026-04-22
  origin/autonomous-loop-index-update-2026-04-22
  origin/autonomous-loop-nature-grade-review
  origin/autonomous-loop-retained-science-package-2026-04-22
  origin/bminusl-anomaly-freedom
  origin/ckm-bs-mixing-phase-derivation
  origin/ckm-cp-phase-structural-identity
  origin/ckm-cp-product-alpha-s-cross-sector-extraction
  origin/ckm-first-row-magnitudes
  origin/ckm-kaon-epsilon-k-jarlskog-decomposition
  origin/ckm-nlo-protected-gamma-derivation
  origin/ckm-scale-convention-theorem
  origin/ckm-second-row-magnitudes
  origin/ckm-thales-cross-system-cp-ratio
  origin/ckm-thales-pinned-alpha-s-independent-ratios
  origin/ckm-third-row-magnitudes
  origin/ckm-unitarity-triangle-right-angle
  origin/claude/angry-chatelet-2dc78c
  origin/claude/angry-feynman-2df312
  origin/claude/axiom-native-overnight-FtUl5
  origin/claude/charged-lepton-closure-review
  origin/claude/cl3-minimality
  origin/claude/derived-science-clean
  origin/claude/dreamy-wing-969574
  origin/claude/eloquent-wilbur
  origin/claude/framework-point-beta-6-lane
  origin/claude/g1-complete
  origin/claude/graviton-mass-identity
  origin/claude/great-nobel-ab743c
  origin/claude/inspiring-banzai-7002dd
  origin/claude/koide-a1-casimir-difference-FtUl5
  origin/claude/koide-a1-irreducibility-package
  origin/claude/koide-a1-round10-fractional-topology
  origin/claude/main-derived
  origin/claude/mass-ratio-package
  origin/claude/mass-spectrum-phase-2-scoping
```

## 7. Recent commit log (last 100)

```
9d0fbabf dm: land freezeout-bypass support lane and SU(3) obstruction
efa79982 koide: land source-domain no-go synthesis
db330501 ckm: land NLO protected gamma corollary
d5d3654c lorentz: land boost-covariance theorem packet
b1bb09ba ckm: integrate Thales CP-ratio theorem
37796022 ckm: derive cross-system CP-asymmetry ratio mediated by Thales circle
30ddf585 planck: integrate area-law quarter no-go lane
654cb77a area-law: land simple-fiber Widom no-go
ee036eab ckm: tighten Bs mixing phase guardrail
2c3aaaf9 docs+scripts: land bounded quark taste-staircase support
1e1aa10d ckm: integrate B_s mixing phase package
4431d3ba ckm: derive B_s mixing phase from retained inputs
0a579977 docs+scripts: land bounded atomic scaffold lane
8d2f8c5f docs+scripts: open atomic hydrogen/helium scaffold lane
0aa82972 ckm: integrate second-row magnitude package
1f3bb000 ckm: second-row magnitudes structural identities theorem
b51dc51f ckm: land first-row magnitude identities
b8bd70f8 docs: land hypercharge squared-trace catalog theorem
201ced08 koide: land Q background-zero criterion
95a79235 docs: land LH anomaly trace catalog theorem
ab860f31 docs: land Koide A1 fractional-topology no-go packet
59f7e4f0 gravity: land scalar harmonic tower
200d9e03 ckm: land third-row magnitude identities
7d1ce8ca koide: land A1 radian bridge audit
d34408bf ckm: land atlas triangle right-angle identity
f5b67622 gravity: land vector gauge-field compactness tower
2d4618f2 koide: land dimensionless objection review packet
56c6dd5a strong-cp: land universal theta-induced EDM response
d8dd1bf2 cosmology: land N_eff active-neutrino support
f4633759 cosmology: land matter-radiation equality identity
da2c5b07 ckm: land Wolfenstein structural identities
16c7ecdd gauge: land fractional charge denominator theorem
e06d8d62 cosmology: land R_base group-theory identity
6668d8d5 anomaly: land SU(3) cubic cancellation theorem
1a226c6d anomaly: land SU(2) Witten Z2 theorem
b529f37b Land alpha_LM geometric mean identity
6d8077db Land Koide pointed-origin exhaustion theorem
e49d201d Land B-L anomaly freedom theorem
cfd621dd Land CKM CP-phase structural identity
084e9797 Land SM hypercharge uniqueness theorem
89b04ca5 Land graviton TT compactness spectral tower
25956cac Land Koide native dimensionless no-go packet
d740bd12 Land FRW cosmology kinematic reduction
fec6bd33 docs: land retained neutrino observable bounds
a55c4717 docs: tighten Planck boundary density scope
9a3526cf docs: add Planck boundary-density extension theorem
e9a5a2d2 docs: close Planck open routes negatively
e6f11dee docs: land conditional Planck completion packet
adf80784 Remove control-plane links from public package docs
ec118ec9 Tighten public package entry and validation surfaces
36f1684c Clean public note language across repo
c67de08e Demote review-state language in delicate lane notes
854e8649 Clean and re-map public science package
e9099506 Clean public repo authority surfaces
b4b46ae3 open planck scale package lane
71e0872f salvage retained science support subset
52bfbbcf Clarify prediction-first public package surfaces
ffe965c7 Land Koide Q second-order support batch
dfe98943 koide: salvage physical-bridge as candidate support route
3f03f0de koide: land brannen geometry and dirac support addendum
84da12b5 koide: land axiom-native support batch honestly
8e3bef18 docs: sync g_bare obstruction note with runner semantics
56876669 Clean public package surface and remove internal docs
0e43fed5 Tighten public repo entry surfaces
e2dff658 Normalize repo terminology to controlled vocabulary
4df9abb7 Sync publication surfaces with landed scalar-selector status
ea0054a0 Clarify current live flagship gate count
870030c2 land scalar selector review package
677b258b docs: clarify koide atlas observational dependencies
4c1a768c science: land 3plus1 Wilson DM support packet
528df939 docs: land g_bare two-ward closure route
c02e1aab framework: land reviewed CL3 support and selector-gap packet
03d427d3 docs: weave quark route2 support stack through repo surfaces
90c78a87 docs: package quark route-2 science review stack
1adfbfb6 gauge: land g_bare ward support candidate with honest status
ceca44b6 docs: land selective lepton PMNS integration subset
32e2d8bb docs: weave bounded quark review packet through main surfaces
de6a472e Add quark science review stack
84670604 docs: open atomic lattice companion lane
f6659518 feat: land dm lepton support packet
6f2e66fc atomic: salvage hydrogen-helium companion packet
4128417d docs: archive operational review backlog surfaces
b5708019 feat: land g_bare structural normalization support
49a470f1 docs: surface bounded wilson side lane
d0bbe1cd docs: clarify bounded irregular sign packet
02210876 docs: land graviton spectral identity
f124537d cosmology: review pass on graviton-mass identity theorem note
1bddec47 cosmology: retain graviton-mass structural identity via Lambda identity theorem
b1f98a96 docs: scrub evaluation scorecards from main
12f14a6a docs: normalize historical runner links
ff5edd0a docs: surface three-generation chirality defense
430211f7 docs: retire five redesign-only audit items
7e141142 docs: salvage PF route history
f2d4ecdf docs: narrow higgs and top package surfaces
00d73223 docs: resolve ew claim-surface drift
5332f39f docs: narrow CKM package claim surface
68077dff docs: narrow strong cp action-surface claims
2f51ff2c cosmology: retain spectral-gap identity and dark-energy EOS corollary
86fcf616 feat: land CL3 support-route minimality packet
69d45c78 docs: clarify one-axiom reduction scope
```

## 8. Key publication-package files

```
total 1688
drwxr-xr-x@ 26 jonBridger  staff     832 Apr 25 09:01 .
drwxr-xr-x@  3 jonBridger  staff      96 Apr 18 14:05 ..
-rw-r--r--@  1 jonBridger  staff   49295 Apr 25 08:20 ARXIV_DRAFT.md
-rw-r--r--@  1 jonBridger  staff    3639 Apr 23 22:00 ARXIV_PACKAGE.md
-rw-r--r--@  1 jonBridger  staff   19981 Apr 25 09:01 CLAIMS_TABLE.md
-rw-r--r--@  1 jonBridger  staff  276111 Apr 25 09:01 DERIVATION_ATLAS.md
-rw-r--r--@  1 jonBridger  staff   89681 Apr 25 09:01 DERIVATION_VALIDATION_MAP.md
-rw-r--r--@  1 jonBridger  staff   19553 Apr 25 08:20 EXTERNAL_REVIEWER_GUIDE.md
-rw-r--r--@  1 jonBridger  staff    4082 Apr 23 22:00 FIGURE_CAPTIONS.md
-rw-r--r--@  1 jonBridger  staff    6218 Apr 18 14:05 FIGURE_PLAN.md
-rw-r--r--@  1 jonBridger  staff   63173 Apr 25 09:01 FULL_CLAIM_LEDGER.md
-rw-r--r--@  1 jonBridger  staff    8013 Apr 23 22:00 GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md
-rw-r--r--@  1 jonBridger  staff    9003 Apr 25 08:20 INPUTS_AND_QUALIFIERS_NOTE.md
-rw-r--r--@  1 jonBridger  staff     948 Apr 23 22:00 NEUTRINO_DIRAC_PMNS_BOUNDARY_PACKET_2026-04-15.md
-rw-r--r--@  1 jonBridger  staff   17711 Apr 25 08:20 PREDICTION_SURFACE_2026-04-15.md
-rw-r--r--@  1 jonBridger  staff   76050 Apr 25 09:01 PUBLICATION_MATRIX.md
-rw-r--r--@  1 jonBridger  staff   14712 Apr 25 08:20 QUANTITATIVE_SUMMARY_TABLE.md
-rw-r--r--@  1 jonBridger  staff    8751 Apr 25 08:20 README.md
-rw-r--r--@  1 jonBridger  staff     812 Apr 23 22:00 RELEASE_ENVIRONMENT.md
-rw-r--r--@  1 jonBridger  staff    6681 Apr 25 08:20 REPRODUCE.md
-rw-r--r--@  1 jonBridger  staff    4631 Apr 23 22:00 REPRODUCIBILITY_FREEZE_2026-04-14.md
-rw-r--r--@  1 jonBridger  staff   84751 Apr 25 09:01 RESULTS_INDEX.md
-rw-r--r--@  1 jonBridger  staff   18105 Apr 25 08:20 SCIENCE_MAP.md
-rw-r--r--@  1 jonBridger  staff   29359 Apr 25 08:20 USABLE_DERIVED_VALUES_INDEX.md
-rw-r--r--@  1 jonBridger  staff    7225 Apr 25 08:20 WHAT_THIS_PAPER_DOES_NOT_CLAIM.md
drwxr-xr-x@ 10 jonBridger  staff     320 Apr 23 22:00 figures
```

## 9. Outputs / logs sizes

```
420K	/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/outputs
3.3M	/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438/logs
```

## 10. CLAIMS_TABLE.md and QUANTITATIVE_SUMMARY_TABLE.md headers (current)

### CLAIMS_TABLE.md (first 60 lines)

```markdown
# Manuscript Claims Surface

Use [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) alongside
this file. This is the short public surface for what the paper may claim. It
is intentionally not the full package ledger.

For broader inventory and companion lanes, use:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)

## Status Legend

- `retained`: safe as a core paper claim on the current package surface
- `retained companion`: exact or structural companion that belongs in Extended
  Data, theorem boxes, or discussion rather than as a headline claim
- `promoted quantitative`: quantitative row the package is prepared to present
  explicitly
- `flagship closed package`: major package-level closeout on the manuscript
  surface
- `open flagship lane`: scientifically central lane still open
- `bounded companion`: useful package result kept outside the manuscript core

## External Inputs

The current manuscript conditions phenomenology on:

- `T_CMB = 2.7255 K`
- `H_0 = 67.4 km/s/Mpc`

The accepted package statement is `Cl(3)` on `Z^3` as the physical theory.
The electroweak scale is not treated as an external input on the manuscript
surface.

## Manuscript-Core Claims

| Claim | Status | Placement | Authority | Primary runner |
|---|---|---|---|---|
| `Cl(3)` on `Z^3` is the working physical theory | retained | main text | [ARXIV_DRAFT.md](./ARXIV_DRAFT.md), [MINIMAL_AXIOMS_2026-04-11.md](../../MINIMAL_AXIOMS_2026-04-11.md) | n/a |
| Weak-field gravity from the Poisson self-consistency / Newton chain on `Z^3` | retained | main text | [SELF_CONSISTENCY_FORCES_POISSON_NOTE.md](../../SELF_CONSISTENCY_FORCES_POISSON_NOTE.md), [POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md](../../POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md), [NEWTON_LAW_DERIVED_NOTE.md](../../NEWTON_LAW_DERIVED_NOTE.md) | [frontier_self_consistent_field_equation.py](../../../scripts/frontier_self_consistent_field_equation.py), [frontier_poisson_exhaustive_uniqueness.py](../../../scripts/frontier_poisson_exhaustive_uniqueness.py), [frontier_newton_derived.py](../../../scripts/frontier_newton_derived.py) |
| Full discrete `3+1` GR on the project route | retained | main text / theorem box | [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](../../UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md) | [frontier_universal_gr_discrete_global_closure.py](../../../scripts/frontier_universal_gr_discrete_global_closure.py) |
| Chosen continuum/QG identification chain on the project route | retained companion | Extended Data / theorem box | [UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md), [GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md](./GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md) | [frontier_universal_qg_canonical_textbook_continuum_gr_closure.py](../../../scripts/frontier_universal_qg_canonical_textbook_continuum_gr_closure.py) |
| Exact native `SU(2)` and graph-first structural `SU(3)` on the accepted package surface | retained | main text | [NATIVE_GAUGE_CLOSURE_NOTE.md](../../NATIVE_GAUGE_CLOSURE_NOTE.md), [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_non_abelian_gauge.py](../../../scripts/frontier_non_abelian_gauge.py), [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| Anomaly-forced `3+1`, LH anomaly trace catalog, hypercharge squared-trace catalog, one-generation matter closure, SM hypercharge uniqueness/electric-charge quantization, fractional-charge denominator from `N_c`, `SU(2)` Witten global-anomaly cancellation, `SU(3)^3` cubic gauge anomaly cancellation, B-L anomaly freedom as a gaugeable option, and retained three-generation matter structure | retained | main text | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md), [LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md](../../LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md), [HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md](../../HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md), [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](../../ONE_GENERATION_MATTER_CLOSURE_NOTE.md), [STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md](../../STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md), [FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md](../../FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md), [SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md](../../SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md), [SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md](../../SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md), [BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md](../../BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md), [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md), [PHYSICAL_LATTICE_NECESSITY_NOTE.md](../../PHYSICAL_LATTICE_NECESSITY_NOTE.md) | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py), [frontier_lh_anomaly_trace_catalog.py](../../../scripts/frontier_lh_anomaly_trace_catalog.py), [frontier_hypercharge_squared_trace_catalog.py](../../../scripts/frontier_hypercharge_squared_trace_catalog.py), [frontier_sm_hypercharge_uniqueness.py](../../../scripts/frontier_sm_hypercharge_uniqueness.py), [frontier_fractional_charge_denominator_from_n_c.py](../../../scripts/frontier_fractional_charge_denominator_from_n_c.py), [frontier_su2_witten_z2_anomaly.py](../../../scripts/frontier_su2_witten_z2_anomaly.py), [frontier_su3_cubic_anomaly_cancellation.py](../../../scripts/frontier_su3_cubic_anomaly_cancellation.py), [frontier_bminusl_anomaly_freedom.py](../../../scripts/frontier_bminusl_anomaly_freedom.py), [frontier_three_generation_observable_theorem.py](../../../scripts/frontier_three_generation_observable_theorem.py) |
| Emergent Lorentz invariance plus exact continuum-limit 1+1D / 3+1D boost-covariant free-scalar 2-point closure | retained companion | main text / discussion + Extended Data | [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](../../EMERGENT_LORENTZ_INVARIANCE_NOTE.md), [LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](../../LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md), [LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md](../../LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md), [ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md](../../ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md) | [frontier_emergent_lorentz_invariance.py](../../../scripts/frontier_emergent_lorentz_invariance.py), [frontier_lorentz_boost_2d.py](../../../scripts/frontier_lorentz_boost_2d.py), [frontier_lorentz_boost_3plus1d.py](../../../scripts/frontier_lorentz_boost_3plus1d.py), [frontier_angular_kernel_underdetermination_nogo.py](../../../scripts/frontier_angular_kernel_underdetermination_nogo.py) |
| Strong CP closure on the retained action surface at `theta_eff = 0` | retained | main text / theorem box | [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md) | [frontier_strong_cp_theta_zero.py](../../../scripts/frontier_strong_cp_theta_zero.py) |
| Universal theta-induced EDM response vanishing on the retained strong-CP surface | retained corollary | SI / strong-CP support surface | [UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md](../../UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md) | [frontier_universal_theta_induced_edm_vanishing.py](../../../scripts/frontier_universal_theta_induced_edm_vanishing.py) |
| Electroweak hierarchy row `v = 246.282818290129 GeV` on the accepted package surface | promoted quantitative | quantitative section; still uses the Planck-scale package pin, with finite-response, parent-source, and simple-fiber Widom entropy-carrier shortcuts closed negatively | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md), [PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md](../../PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md), [AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md](../../AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py), [frontier_area_law_quarter_broader_no_go.py](../../../scripts/frontier_area_law_quarter_broader_no_go.py) |
| `alpha_s(M_Z)`, the `alpha_LM` geometric-mean identity, electroweak normalization, and retained YT/top transport package | promoted quantitative + retained support | quantitative section / Extended Data | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md), [ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md), [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md), [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md) | [frontier_complete_prediction_chain.py](../../../scripts/frontier_complete_prediction_chain.py), [frontier_alpha_lm_geometric_mean_identity.py](../../../scripts/frontier_alpha_lm_geometric_mean_identity.py), [frontier_yt_ward_identity_derivation.py](../../../scripts/frontier_yt_ward_identity_derivation.py) |
| CKM atlas/axiom package on the canonical tensor/projector surface, including standalone Wolfenstein identities `lambda^2=alpha_s(v)/2`, `A^2=2/3`, CP-phase identity `cos^2(delta_CKM)=1/6`, atlas-triangle right-angle identity `alpha_0=90 deg`, atlas-leading first-row identities `|V_us|_0^2=alpha_s(v)/2`, `|V_ub|_0^2=alpha_s(v)^3/72`, `|V_ud|_0^2=1-alpha_s(v)/2-alpha_s(v)^3/72`, atlas-leading second-row identities `|V_cd|_0^2=alpha_s(v)/2`, `|V_cs|_0^2=1-alpha_s(v)/2-alpha_s(v)^2/6`, `|V_cb|_0^2=alpha_s(v)^2/6`, atlas-leading third-row identities `|V_td|_0^2=5 alpha_s(v)^3/72`, `|V_ts|_0^2=alpha_s(v)^2/6`, atlas-leading B_s mixing phase `phi_s=-alpha_s(v)sqrt(5)/6`, and Thales-mediated CP ratio `phi_s/sin(2 beta_d)=-alpha_s(v)/2` | promoted quantitative | quantitative section / theorem box | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md), [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md), [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md), [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md](../../CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md), [CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md), [CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md](../../CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md), [CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md), [CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md](../../CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md), [CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md) | [frontier_ckm_atlas_axiom_closure.py](../../../scripts/frontier_ckm_atlas_axiom_closure.py), [frontier_wolfenstein_lambda_a_structural_identities.py](../../../scripts/frontier_wolfenstein_lambda_a_structural_identities.py), [frontier_ckm_cp_phase_structural_identity.py](../../../scripts/frontier_ckm_cp_phase_structural_identity.py), [frontier_ckm_atlas_triangle_right_angle.py](../../../scripts/frontier_ckm_atlas_triangle_right_angle.py), [frontier_ckm_first_row_magnitudes.py](../../../scripts/frontier_ckm_first_row_magnitudes.py), [frontier_ckm_second_row_magnitudes.py](../../../scripts/frontier_ckm_second_row_magnitudes.py), [frontier_ckm_third_row_magnitudes.py](../../../scripts/frontier_ckm_third_row_magnitudes.py), [frontier_ckm_bs_mixing_phase_derivation.py](../../../scripts/frontier_ckm_bs_mixing_phase_derivation.py), [frontier_ckm_thales_cross_system_cp_ratio.py](../../../scripts/frontier_ckm_thales_cross_system_cp_ratio.py), [frontier_ckm_no_import_audit.py](../../../scripts/frontier_ckm_no_import_audit.py) |
| CKM NLO barred-triangle protected invariant `gamma_bar=arctan(sqrt(5))` with `rho_bar=(4-alpha_s(v))/24` and `eta_bar=sqrt(5)(4-alpha_s(v))/24` on the standard NLO barred-apex map | retained NLO CKM-structure corollary | quantitative section / theorem box | [CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md](../../CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | [frontier_ckm_nlo_barred_triangle_protected_gamma.py](../../../scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py) |
| Dark-matter exact-target PMNS package on the manuscript surface | flagship closed package | dedicated manuscript package section | [DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md](../../DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md), [DM_ABCC_RETAINED_MEASUREMENT_CLOSURE_THEOREM_NOTE_2026-04-21.md](../../DM_ABCC_RETAINED_MEASUREMENT_CLOSURE_THEOREM_NOTE_2026-04-21.md), [DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md](../../DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md) | [frontier_dm_leptogenesis_transport_status.py](../../../scripts/frontier_dm_leptogenesis_transport_status.py), [frontier_dm_abcc_retained_measurement_closure_2026_04_21.py](../../../scripts/frontier_dm_abcc_retained_measurement_closure_2026_04_21.py), [frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py](../../../scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py) |

## Open Flagship Lane

| Lane | Status | Current boundary | Main authority | Primary runner |
|---|---|---|---|---|
| Charged-lepton Koide (`Q = 2/3`, `delta = 2/9`) | open flagship lane | strong support package, but retained dimensionless closure remains open; the April 25 criterion theorem closes the exact background-zero / `Z`-erasure algebra for `Q` on the admitted reduced carrier, and the onsite source-domain synthesis proves that strict onsite C3-invariant sources would erase `Z` while the retained central/projected commutant source grammar still admits it; the physical source-domain / source-free reduced-carrier selection theorem remains open; `delta` still needs selected-line local boundary-source, based-endpoint, and Type-B `2/9` rational-to-radian readout theorems; the A1/radian audit and Round-10 fractional-topology no-go batch add that retained periodic phase sources are `q*pi`, canonical fractional-topological phase maps still land in `(rational)*pi`, and the surviving Type-B readout is sharpened to a period convention choice on the selected-line observable; the separate overall lepton scale `v_0` remains open | [KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md](../../KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md), [CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md](../../CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md), [KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md](../../KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md), [KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md](../../KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md), [KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md](../../KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md), [KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md](../../KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md), [KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md](../../KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md), [KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md](../../KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md) | [frontier_koide_lane_regression.py](../../../scripts/frontier_koide_lane_regression.py), [frontier_koide_reviewer_stress_test.py](../../../scripts/frontier_koide_reviewer_stress_test.py), [frontier_koide_pointed_origin_exhaustion_theorem.py](../../../scripts/frontier_koide_pointed_origin_exhaustion_theorem.py), [frontier_koide_dimensionless_objection_closure_review.py](../../../scripts/frontier_koide_dimensionless_objection_closure_review.py), [frontier_koide_q_background_zero_z_erasure_criterion.py](../../../scripts/frontier_koide_q_background_zero_z_erasure_criterion.py), [frontier_koide_q_onsite_source_domain_no_go_synthesis.py](../../../scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py), [frontier_koide_a1_radian_bridge_irreducibility_audit.py](../../../scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py), [frontier_koide_a1_cheeger_simons_rz_probe.py](../../../scripts/frontier_koide_a1_cheeger_simons_rz_probe.py) |

```

### QUANTITATIVE_SUMMARY_TABLE.md (first 60 lines)

```markdown
# Quantitative Summary Table

**Date:** 2026-04-15
**Purpose:** public summary of the current quantitative lanes plus the
remaining bounded companions

This is the fastest single table for the package's current quantitative
prediction/comparator surface. For the broader falsification surface, open
bridges, and delayed-observability rows, pair it with
[PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md).

In this table:

- `Claim-strength status` says what kind of quantitative row this is
- `Qualifier` carries the bridge / import / caveat language
- publication-capture placement lives in [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)

| Quantity / lane | Predicted / framework result | Observed / comparator | Error / comparison | Claim-strength status | Qualifier | Primary authority |
|---|---|---|---|---|---|---|
| `alpha_s(M_Z)` | `0.1181` | `0.1179` | `+0.14%` | retained | canonical same-surface plaquette chain for `alpha_s(v)` plus the retained one-decade running bridge to `M_Z` | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) |
| `alpha_LM` geometric-mean identity | `alpha_LM^2 = alpha_bare alpha_s(v)` | n/a | exact identity | retained support | coupling-chain bookkeeping identity on the retained definitions; not an independent empirical prediction and not part of the `alpha_s(M_Z)` running bridge | [ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `SU(3)` string tension `\sqrt{\sigma}` | `465 MeV` | `440 ± 20 MeV` | `+5.6%` | bounded companion | `T = 0` confinement is structural on the graph-first `SU(3)` gauge sector; the numeric `\sqrt{\sigma}` row is bounded through retained `\alpha_s` plus the low-energy EFT bridge and screening correction | [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) |
| `sin^2(theta_W)(M_Z)` | `0.2306` | `0.2312` | `-0.26%` | retained | standalone EW lane; bare geometry + same-surface plaquette chain + derived `R_conn` support + retained running bridge, with explicit retained matching uncertainty from the EW `Δ_R` audit | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md), [YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md) |
| `1/alpha_EM(M_Z)` | `127.67` | `127.95` | `-0.22%` | retained | standalone EW lane; derived `g_1(v), g_2(v)` package after color projection plus the retained running bridge, with explicit retained matching uncertainty from the EW `Δ_R` audit | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md), [YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md) |
| `g_1(v)` | `0.4644` | `0.4640` | `+0.08%` | retained | standalone EW lane; bare geometry + same-surface plaquette chain + derived `R_conn = 8/9 + O(1/N_c^4)` support, with explicit retained matching uncertainty from the EW `Δ_R` audit | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md), [YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md) |
| `g_2(v)` | `0.6480` | `0.6463` | `+0.26%` | retained | standalone EW lane; bare geometry + same-surface plaquette chain + derived `R_conn = 8/9 + O(1/N_c^4)` support, with explicit retained matching uncertainty from the EW `Δ_R` audit | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md), [YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md) |
| `M_W` same-surface probe | `M_W^tree = 79.80 GeV`, `M_W^RGE = 80.5573 GeV` | PDG `80.3692 GeV`; CDF `80.4335 GeV` | tree `-0.71%`, RGE `+0.23%` vs PDG; RGE `+0.15%` vs CDF | bounded companion | same-surface fixed-point solve from retained `g_2(v)` and `v` with SM 1-loop SU(2) running; the residual tracks the retained `g_2(v)` precision and is not a few-MeV SM-indirect `M_W` prediction | [W_MASS_DERIVED_NOTE.md](../../W_MASS_DERIVED_NOTE.md) |
| `y_t(v)` | `0.9176` | `~0.917` | `+0.06%` | retained | exact lattice-scale Ward theorem `y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6)` plus retained UV-to-IR transport obstruction stack and canonical full-staggered-PT `Δ_R = -3.77% ± 0.45%`; the older bridge-path budget now survives only as an independent cross-check | [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md), [YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](../../YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md) |
| `m_t(pole)` 2-loop | `172.57 GeV` | `172.69 GeV` | `-0.07%` | retained | retained YT/top transport lane; canonical full-staggered-PT central `172.57 ± 6.50 GeV` with explicit through-2-loop structural / bound-constrained continuation on the same surface | [YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](../../YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md), [YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md](../../YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md) |
| `m_t(pole)` 3-loop | `173.10 GeV` | `172.69 GeV` | `+0.24%` | derived | older 3-loop continuation remains a derived cross-check against the retained 2-loop canonical lane; it is no longer the primary YT authority surface | [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md) |
| `m_H` 2-loop | `119.8 GeV` | `125.25 GeV` | `-4.4%` | derived | corrected-input 2-loop support route; inherits the retained YT transport lane and the explicit Higgs-native retention-gap audit on the accepted package route | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md), [HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md) |
| `m_H` framework-side 3-loop | `125.1 GeV` | `125.25 GeV` | `-0.1%` | derived | direct framework-native 3-loop computation exists, and the lane now carries an explicit retention-decomposed budget `125.04 ± 3.17 GeV` rather than an unstructured inherited YT caveat | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md), [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md) |
| Vacuum stability | qualitatively favorable | SM metastability comparator | qualitative prediction | derived | qualitative vacuum readout on the same route; inherits the current Yukawa/Higgs precision caveat rather than a separate closure failure | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md) |
| Taste-scalar pair | `124.91 GeV` | no confirmed observation | near-Higgs search surface | bounded companion | exact taste-block fermion-CW isotropy plus bounded gauge-only split; scalar-only thermal-cubic estimate gives `v_c/T_c = 0.3079` | [TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md](../../TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md) |
| DM transport / PMNS gate status | exact one-flavor branch `0.1888`; reduced-surface PMNS support branch `1.0` | asymmetry target `1.0` | mixed | closed for the exact PMNS-target formulation treated here | exact transport chain plus source-side closeout to the `2`-real `Z_3` doublet-block law, retained-measurement A-BCC closure, interval-certified split-2 carrier closure, shifted same-law recovered-packet closure, exact target-surface source-cubic closure, graph-first ordered-chain current activation, affine current-coordinate reduction, and ordered-chain graded-current delta closure | [DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md](../../DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md), [DM_ABCC_RETAINED_MEASUREMENT_CLOSURE_THEOREM_NOTE_2026-04-21.md](../../DM_ABCC_RETAINED_MEASUREMENT_CLOSURE_THEOREM_NOTE_2026-04-21.md), [DM_SPLIT2_INTERVAL_CERTIFIED_DOMINANCE_CLOSURE_THEOREM_NOTE_2026-04-21.md](../../DM_SPLIT2_INTERVAL_CERTIFIED_DOMINANCE_CLOSURE_THEOREM_NOTE_2026-04-21.md), [DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md](../../DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md) |
| `R_base` DM/cosmology base factor | `31/9 = 3.444...` | n/a | exact identity | retained support | group-theory support identity for the bounded DM/cosmology cascade; depends on admitted `3/5` GUT normalization and does not include Sommerfeld or the full `Omega_DM/Omega_b` value | [R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md](../../R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md) |
| Matter-radiation equality | `1 + z_mr = Omega_m,0/Omega_r,0`; supplied-density readout `z_mr = 3423` | CMB-inferred `3387 +/- 21` | `+1.1%` | retained/admitted structural support | exact FRW/EOS ratio identity; the numerical readout is conditioned on supplied `Omega_m,0` and observational `Omega_r,0`, not a native density derivation | [MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `N_eff` active-neutrino count | retained count `N_active = 3`; standard readout `N_eff = 3.046` | Planck comparator `2.99 +/- 0.17` | `+0.33 sigma` | retained/admitted structural support | retained three-generation matter content fixes three light active neutrino flavours; `+0.046`, `T_CMB`, and `Omega_r,0` conversion remain standard/observational cosmology inputs | [N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md](../../N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md) |
| Neutrino absolute-mass observable bounds | `Σm_ν > 50.58 meV`, `m_β ≤ 50.58 meV`, `m_ββ ≤ 50.58 meV`, `0 < Δm²_21 < Δm²_31` | listed cosmology, tritium, and `0νββ` bounds are comparators only | bounded retained-package inequalities | bounded companion | follows algebraically from the retained atmospheric-scale package and retained normal ordering; not a point prediction for `Σm_ν`, `m_1`, `m_2`, PMNS angles, Majorana phases, or the solar gap | [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md) |
| CKM algebraic atlas/axiom package | atlas-leading `|V_ud|_0=0.973824`, `|V_us|_0=0.22727`, `|V_ub|_0=0.003913`, atlas-leading `|V_cd|_0=0.22727`, atlas-leading `|V_cs|_0=0.97292`, `|V_cb|=0.04217`, atlas-leading `|V_td|_0=0.008750`, `|V_ts|_0=0.04217`, `|V_tb|_0=0.99907`, `\lambda^2=\alpha_s(v)/2`, `A^2=2/3`, `\delta=65.905^\circ`, atlas `\alpha_0=90^\circ`, exact standard-matrix `J=3.331 x 10^-5`, atlas-leading `phi_s(B_s)=-0.03850 rad`, Thales ratio `phi_s/sin(2\beta_d)=-0.05165` | PDG magnitudes plus coherent angle package `\delta=65.5^\circ`, `J_{recon}=3.304 x 10^-5`, LHCb `phi_s=-0.039 +/- 0.022`, cross-system ratio `-0.055 +/- 0.031` | first-/second-/third-row atlas-leading values are comparator-facing; exact right-angle statement is atlas-only; B_s phase and cross-system ratio are leading-Wolfenstein rather than all-orders mixing | promoted quantitative package | atlas/axiom package with canonical CMT `\alpha_s(v)` as the quantitative coupling input and no quark-mass or fitted CKM observables in the derivation; exact atlas counts + exact Wolfenstein identities + exact `1/6` projector + exact tensor slot + Schur cascade on the canonical tensor/projector surface; the rescaled atlas triangle has `\alpha_0=90^\circ`, while finite-`\lambda` barred unitarity-triangle, row-level standard-matrix corrections, and exact-sine corrections are not promoted away | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md), [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md), [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md), [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md](../../CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md), [CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md), [CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md](../../CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md), [CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md), [CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md](../../CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md), [CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md) |
| CKM NLO barred-triangle protected gamma | `gamma_bar=65.905^\circ` protected at NLO, `rho_bar=0.16236`, `eta_bar=0.36305`, `beta_bar=23.433^\circ`, `alpha_bar=90.662^\circ`, `sin(2 beta_bar)=0.72976` | PDG barred-angle and `sin(2 beta)` comparators | `gamma_bar` within `0.13 sigma`; `sin(2 beta_bar)` reduces the atlas-leading tension to `2.16 sigma` | retained NLO CKM-structure corollary | uses the promoted CKM atlas inputs plus the standard NLO barred-apex map; protected `gamma_bar` is an NLO invariant and is not claimed beyond the `O(lambda^4)` remainder | [CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md](../../CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) |
| down-type CKM-dual mass-ratio lane | `m_d/m_s = 0.05165`, `m_s/m_b = 0.02239`, `m_d/m_b = 0.001156` | threshold-local self-scale comparators `0.05000`, `0.02234`, `0.001117` | `+3.3%`, `+0.2%`, `+3.5%`; common-scale `m_s(m_b)/m_b(m_b)` stays `+15.0%` away | bounded secondary lane | promoted CKM atlas/axiom package plus GST and bounded `5/6` bridge support; no observed masses as derivation inputs, with threshold-local self-scale comparison supported but theorem-grade scale closure still open | [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](../../DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md) |

## Reading rule

- `derived` rows are safe current-main quantitative values, but their bridge /
  import caveats still live in the qualifier column
- `bounded companion` and `bounded secondary lane` rows remain package-captured
  and must carry their explicit qualifiers
- `open flagship lane` rows are live status rows, not closed quantitative
  predictions
```
