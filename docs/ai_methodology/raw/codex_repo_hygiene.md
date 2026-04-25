# Codex Repo Hygiene

**Capture date:** 2026-04-25

This file captures raw evidence of Codex-side repo hygiene work: branch
inventory, worktree inventory, and recent `main` landing cadence.

---

## 1. Remote `origin/codex/*` branches

Count on this pass:

```text
59
```

Raw branch list:

```text
origin/codex/area-law-quarter-coefficient
origin/codex/area-law-quarter-residual-carriers
origin/codex/area-law-target2-algebraic-spectrum
origin/codex/area-law-target2-primitive-edge
origin/codex/baryogenesis-frozen-2026-04-16
origin/codex/ckm-bs-mixing-phase-land
origin/codex/ckm-first-row-magnitudes-land
origin/codex/ckm-full-package-review
origin/codex/ckm-kaon-epsilon-land
origin/codex/ckm-nlo-protected-gamma-land
origin/codex/clean-main-2026-04-24
origin/codex/cross-sector-koide-vcb-land
origin/codex/dm-close-last-two
origin/codex/dm-leptons-land
origin/codex/dm-science-reviewed-2026-04-17
origin/codex/dm-selector-closeout-main-2026-04-17
origin/codex/dm-thermal-review-2026-04-17
origin/codex/framework-bare-alpha-ratio-land
origin/codex/g-bare-land-2026-04-18
origin/codex/g-bare-two-ward-land
origin/codex/hierarchy-retained-close-2026-04-22
origin/codex/hydrogen-helium-salvage
origin/codex/koide-dimensionless-closure-proposal-2026-04-24
origin/codex/koide-dimensionless-objection-closure-2026-04-24
origin/codex/koide-dimensionless-objection-closure-main-2026-04-24
origin/codex/koide-full-workstream-science-2026-04-25
origin/codex/koide-native-dimensionless-closure-2026-04-24
origin/codex/koide-p-3plus1-transport
origin/codex/land-graviton-mass-identity
origin/codex/lepto-selector-closeout-main-2026-04-17
origin/codex/leptogenesis-science-review-2026-04-16
origin/codex/main-derived-quark-route2-science-stack
origin/codex/main-derived-quark-science-stack
origin/codex/main-graph-first
origin/codex/neutrino-dm-package-2026-04-16
origin/codex/neutrino-retained-lanes-review
origin/codex/neutrino-science-main-derived-2026-04-16
origin/codex/p-derivation-package
origin/codex/p-derived-science-review
origin/codex/pf-path-ground-2026-04-17
origin/codex/pf-salvage-2026-04-18
origin/codex/pf-science-review-2026-04-18
origin/codex/planck-scale-program-2026-04-23
origin/codex/planck-source-unit-clean-science-2026-04-25
origin/codex/planck-source-unit-resubmission-clean-2026-04-25
origin/codex/plaquette-env-review
origin/codex/plaquette-env-transfer
origin/codex/publication-prep
origin/codex/qg-continuum-update
origin/codex/repo-landing-surface
origin/codex/review-active
origin/codex/root-publication-mainline
origin/codex/root-release-entry
origin/codex/scalar-selector-cycle1-review
origin/codex/science-3plus1-line-law
origin/codex/taste-scalar-isotropy-main-2026-04-16
origin/codex/three-generation-observable-main-2026-04-15
origin/codex/wip-isolation-2026-04-14
origin/codex/yt-unbounded-main-package-2026-04-15
```

## 2. Live `codex/*` worktrees

Count on this pass:

```text
37
```

Raw worktree list:

```text
/private/tmp/ai-method-land                                                      4da26702 [codex/land-ai-methodology-lane-2026-04-25]
/private/tmp/ai-method-review                                                    c36cbe81 [codex/review-ai-methodology-capture-2026-04-25]
/private/tmp/atomic-land                                                         0a579977 [codex/atomic-hydrogen-helium-land]
/private/tmp/ckm-bs-land                                                         ee036eab [codex/ckm-bs-mixing-phase-land]
/private/tmp/ckm-first-row-land                                                  b51dc51f [codex/ckm-first-row-magnitudes-land]
/private/tmp/ckm-kaon-land.8vQzCS                                                2fc5b523 [codex/ckm-kaon-epsilon-land]
/private/tmp/ckm-nlo-gamma-land                                                  db330501 [codex/ckm-nlo-protected-gamma-land]
/private/tmp/ckm-thales-land.eZ6PDB                                              f0345539 [codex/land-ckm-thales-alpha-independent]
/private/tmp/cross-sector-koide-land.naD0Rv                                      037aded3 [codex/cross-sector-koide-vcb-land]
/private/tmp/framework-bare-alpha-land.JYk6FJ                                    b684741f [codex/framework-bare-alpha-ratio-land]
/private/tmp/great-nobel-land.TInIX3                                             db330501 [codex/land-great-nobel-ab743c]
/private/tmp/great-nobel-land2.ndu3MV                                            9d0fbabf [codex/land-great-nobel-ab743c-v2]
/private/tmp/hypercharge2-land                                                   b8bd70f8 [codex/land-hypercharge-squared-trace-catalog-2026-04-25]
/private/tmp/koide-a1-frac-land                                                  ab860f31 [codex/land-koide-a1-fractional-topology-2026-04-25]
/private/tmp/koide-q-minsel-land                                                 0a116fa1 [codex/land-koide-q-minimal-selector-convention-2026-04-25]
/private/tmp/lh-anomaly-land                                                     95a79235 [codex/land-lh-anomaly-trace-catalog-2026-04-25]
/private/tmp/lorentz-land                                                        d5d3654c [codex/land-lorentz-boost-covariance-2026-04-25]
/private/tmp/physics-area-law-review-EsJ2Ju                                      30ddf585 [codex/land-area-law-quarter-2026-04-25]
/private/tmp/physics-ckm-bs-review-rh9gyX                                        1e1aa10d [codex/land-ckm-bs-mixing-2026-04-25]
/private/tmp/physics-ckm-cp-product-review-dX4RpC                                f9559df1 [codex/land-ckm-cp-product-alpha-s-2026-04-25]
/private/tmp/physics-ckm-second-row-main                                         0aa82972 [codex/land-ckm-second-row-main-2026-04-25]
/private/tmp/physics-ckm-second-row-review                                       30499852 [codex/land-ckm-second-row-2026-04-25]
/private/tmp/physics-ckm-thales-review-CGeHpK                                    b1bb09ba [codex/land-ckm-thales-cp-ratio-2026-04-25]
/private/tmp/physics-grav-lambda-tower-review-5ZzddS                             e05dbd2a [codex/land-gravity-lambda-tower-bridge-2026-04-25]
/private/tmp/physics-koide-full-review-U0ERtI                                    efa79982 [codex/land-koide-full-workstream-science-2026-04-25]
/private/tmp/physics-lorentz-kernel-review-SNh7BI                                2e0ae229 [codex/land-lorentz-kernel-positive-closure-2026-04-25]
/private/tmp/physics-three-sector-review-ZYqozl                                  0a116fa1 [codex/review-three-sector-dim-color-2026-04-25-092340]
/private/tmp/planck-srcunit-land.z4Psgi                                          338fd21f [codex/land-planck-source-unit-support]
/private/tmp/quark-taste-land                                                    2c3aaaf9 [codex/quark-taste-staircase-support-land]
/private/tmp/scalar-selector-cycle1-land-0422                                    870030c2 [codex/scalar-selector-cycle1-land]
/private/tmp/three-sector-review                                                 527864cb [codex/review-three-sector-dim-color-2026-04-25]
/Users/jonreilly/.codex/worktrees/7872/CL3Z3 new work                            0a116fa1 [codex/koide-q-physical-carrier-source-selection]
/Users/jonreilly/.codex/worktrees/8805/CL3Z3 new work                            037aded3 (detached HEAD)
/Users/jonreilly/.codex/worktrees/e76c/hierarchy-review-packet                   e8877356 [codex/hierarchy-retained-close-2026-04-22]
/Users/jonreilly/.codex/worktrees/e76c/koide-q-review-packet                     b2192666 [codex/koide-q-review-packet-2026-04-22]
/Users/jonreilly/.codex/worktrees/e76c/planck-scale-program                      ceb6d0f9 [codex/planck-scale-program-2026-04-23]
/Users/jonreilly/Projects/CL3Z3 new work                                         00677a06 [codex/koide-resume-2026-04-18]
```

## 3. Recent `origin/main` landing cadence

Commits on `origin/main` since `2026-04-22`:

```text
74
```

Raw log excerpt:

```text
4da26702 docs: land AI methodology lane
b684741f ew: land bare alpha ratio support
0a116fa1 koide: fix minimal selector ratio convention
037aded3 koide: land conditional CKM Vcb bridge support
e05dbd2a gravity: land Lambda spectral tower bridge
338fd21f docs: land Planck source-unit normalization support theorem
2e0ae229 lorentz: land fixed-H_lat kernel closure
f0345539 docs: land CKM Thales alpha-independent ratios theorem
2fc5b523 ckm: land kaon epsilon_K Jarlskog decomposition
f9559df1 ckm: land CP-product alpha_s estimator
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
```

## 4. Hygiene signals visible directly in the raw data

The raw branch/worktree/commit evidence above already shows several process
signals without later interpretation:

- separate `review-*` and `land-*` worktrees;
- selective landings to `main` instead of direct branch merges;
- repeated wording/package cleanups interleaved with theorem landings;
- explicit distinction between support, no-go, closure, and review packets.
