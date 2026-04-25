# Claude Git Evidence (full dump)

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7`. Commits below
span Claude Sonnet/Opus 4.x authoring on this repo.

**Workspace:** `/Users/jonreilly/Projects/Physics`

**Repo:** `https://github.com/jonathonreilly/cl3-lattice-framework`

**Scope note:** Verbatim full-body dump of git evidence directly relevant to
the Claude side of the workflow: complete worktree list, complete remote
branch list, complete recent-window commit log, complete hygiene-commit
filter, complete Claude-attributed commit list (all-time), and the full
authorship histogram. Counts and excerpts are NOT summarized — the entire
output of each `git` invocation is reproduced.

---

## 1. Full `git worktree list` (verbatim)

This is every worktree currently attached to this repo, regardless of
which tool created it. Includes Claude `claude/*` branches, Codex
`codex/*` branches, named-topic branches (`ckm-*`, `gravity-*`,
`koide-*`, etc.), and detached-HEAD review packets.

**Total entries:** 92

```text
/Users/jonreilly/Projects/Physics                                                201ced08 [main]
/private/tmp/afternoon-4-21-review                                               1a7f2e02 (detached HEAD)
/private/tmp/ai-method-land                                                      4da26702 [codex/land-ai-methodology-lane-2026-04-25]
/private/tmp/ai-method-review                                                    91b52c8e [codex/review-ai-methodology-capture-2026-04-25]
/private/tmp/atomic-land                                                         0a579977 [codex/atomic-hydrogen-helium-land]
/private/tmp/autonomous-loop-retained-science-review                             0009ff9f (detached HEAD)
/private/tmp/canonical-landing                                                   9e1263df (detached HEAD)
/private/tmp/ckm-bs-land                                                         ee036eab [codex/ckm-bs-mixing-phase-land]
/private/tmp/ckm-bs-review                                                       874a42da (detached HEAD)
/private/tmp/ckm-first-row-land                                                  b51dc51f [codex/ckm-first-row-magnitudes-land]
/private/tmp/ckm-first-row-review                                                ae96c10b (detached HEAD)
/private/tmp/ckm-kaon-land.8vQzCS                                                2fc5b523 [codex/ckm-kaon-epsilon-land]
/private/tmp/ckm-nlo-gamma-land                                                  db330501 [codex/ckm-nlo-protected-gamma-land]
/private/tmp/ckm-nlo-gamma-review                                                3aad9277 (detached HEAD)
/private/tmp/ckm-scale-convention                                                085585ac [ckm-scale-convention-theorem]
/private/tmp/ckm-structcounts-land                                               4da26702 [codex/land-ckm-structcounts-2026-04-25]
/private/tmp/ckm-structcounts-review                                             908d5c83 [codex/review-ckm-structcounts-dim-2026-04-25]
/private/tmp/ckm-thales-alpha-ind.o9I7mf                                         e54d32fd (detached HEAD)
/private/tmp/ckm-thales-land.eZ6PDB                                              f0345539 [codex/land-ckm-thales-alpha-independent]
/private/tmp/cross-lane-consistency                                              ba980d1b [cross-lane-consistency-support]
/private/tmp/cross-sector-koide-land.naD0Rv                                      037aded3 [codex/cross-sector-koide-vcb-land]
/private/tmp/evening-4-21-review                                                 18e51c20 (detached HEAD)
/private/tmp/framework-bare-alpha-land.JYk6FJ                                    b684741f [codex/framework-bare-alpha-ratio-land]
/private/tmp/great-nobel-land.TInIX3                                             db330501 [codex/land-great-nobel-ab743c]
/private/tmp/great-nobel-land2.ndu3MV                                            9d0fbabf [codex/land-great-nobel-ab743c-v2]
/private/tmp/great-nobel-review.cpqYSB                                           a7898f83 (detached HEAD)
/private/tmp/hypercharge2-land                                                   b8bd70f8 [codex/land-hypercharge-squared-trace-catalog-2026-04-25]
/private/tmp/hypercharge2-review                                                 29a2b8c9 (detached HEAD)
/private/tmp/koide-a1-frac-land                                                  ab860f31 [codex/land-koide-a1-fractional-topology-2026-04-25]
/private/tmp/koide-a1-frac-review                                                5e9ce500 (detached HEAD)
/private/tmp/koide-brannen-ch-three-gap-review                                   f68dc664 [koide-brannen-ch-three-gap-review]
/private/tmp/koide-charged-lepton-axiom-native-review                            1055aefc (detached HEAD)
/private/tmp/koide-dimensionless-objection-review                                970933e6 (detached HEAD)
/private/tmp/koide-equivariant-berry-aps-selector-review                         451f5f9c (detached HEAD)
/private/tmp/koide-equivariant-review                                            1f2dd411 (detached HEAD)
/private/tmp/koide-q-3delta-doublet                                              65ff07a9 [koide-q-eq-3delta-doublet-magnitude-route]
/private/tmp/koide-q-land                                                        b51dc51f (detached HEAD)
/private/tmp/koide-q-minsel-land                                                 0a116fa1 [codex/land-koide-q-minimal-selector-convention-2026-04-25]
/private/tmp/lambda-qcd                                                          2eb8ad8a [lambda-qcd-derivation-support]
/private/tmp/lh-anomaly-land                                                     95a79235 [codex/land-lh-anomaly-trace-catalog-2026-04-25]
/private/tmp/lh-anomaly-review                                                   8b649a42 (detached HEAD)
/private/tmp/loop-index                                                          62c3d57a [autonomous-loop-index-2026-04-22]
/private/tmp/loop-index-v2                                                       77e56f41 [autonomous-loop-index-update-2026-04-22]
/private/tmp/lorentz-boost-covariance-review                                     3faae6d6 [lorentz-boost-covariance-review-note]
/private/tmp/lorentz-land                                                        d5d3654c [codex/land-lorentz-boost-covariance-2026-04-25]
/private/tmp/mbb-prediction                                                      d8f7ba81 [neutrinoless-double-beta-mbb-prediction]
/private/tmp/mbeta-prediction                                                    4e832629 [tritium-beta-effective-mass-prediction]
/private/tmp/monopole-consol                                                     71521980 [monopole-mass-consolidation-theorem]
/private/tmp/morning-4-21-review                                                 1e675110 (detached HEAD)
/private/tmp/neutrino-mass-sum                                                   0bf1405b [neutrino-mass-sum-prediction]
/private/tmp/nu-3-level                                                          d413f696 [neutrino-three-level-staircase-proposal]
/private/tmp/nu-solar                                                            7dc55449 [neutrino-solar-gap-alpha-lm-squared]
/private/tmp/omega-lambda-bridge                                                 c337c4ff [omega-lambda-matter-bridge-theorem]
/private/tmp/physics-area-law-review-EsJ2Ju                                      30ddf585 [codex/land-area-law-quarter-2026-04-25]
/private/tmp/physics-ckm-bs-review-rh9gyX                                        1e1aa10d [codex/land-ckm-bs-mixing-2026-04-25]
/private/tmp/physics-ckm-cp-product-review-dX4RpC                                f9559df1 [codex/land-ckm-cp-product-alpha-s-2026-04-25]
/private/tmp/physics-ckm-second-row-main                                         0aa82972 [codex/land-ckm-second-row-main-2026-04-25]
/private/tmp/physics-ckm-second-row-review                                       30499852 [codex/land-ckm-second-row-2026-04-25]
/private/tmp/physics-ckm-thales-review-CGeHpK                                    b1bb09ba [codex/land-ckm-thales-cp-ratio-2026-04-25]
/private/tmp/physics-grav-lambda-tower-review-5ZzddS                             e05dbd2a [codex/land-gravity-lambda-tower-bridge-2026-04-25]
/private/tmp/physics-koide-full-review-U0ERtI                                    efa79982 [codex/land-koide-full-workstream-science-2026-04-25]
/private/tmp/physics-lorentz-kernel-review-SNh7BI                                2e0ae229 [codex/land-lorentz-kernel-positive-closure-2026-04-25]
/private/tmp/physics-three-sector-land-SpZoaT                                    fc5bcceb [codex/land-three-sector-support-2026-04-25]
/private/tmp/physics-three-sector-review-ZYqozl                                  0a116fa1 [codex/review-three-sector-dim-color-2026-04-25-092340]
/private/tmp/planck-srcunit-land.z4Psgi                                          338fd21f [codex/land-planck-source-unit-support]
/private/tmp/planck-srcunit-review.Tuw0BU                                        00c1f7a2 (detached HEAD)
/private/tmp/q23-anomaly                                                         2ea22b13 [koide-q23-anomaly-structural-attack]
/private/tmp/q23-oh                                                              d50d5ebf [koide-q23-lattice-oh-stabilizer]
/private/tmp/q23-spin1                                                           71bb52e1 [koide-q23-spin1-structural-route]
/private/tmp/q23-status                                                          297f9f81 [koide-q23-spin1-subroute-status]
/private/tmp/q23-variational                                                     3db3f3e3 [koide-q23-variational-coupling-conjecture]
/private/tmp/quark-taste-land                                                    2c3aaaf9 [codex/quark-taste-staircase-support-land]
/private/tmp/r-consolidation                                                     1cd9dcde [tensor-scalar-ratio-consolidation-theorem]
/private/tmp/raw-method-kickoff                                                  2c624192 [claude/raw-methodology-dump-2026-04-25]
/private/tmp/relaxed-taussig-actual                                              ec9c2fd3 (detached HEAD) prunable
/private/tmp/relaxed-taussig-review                                              18d9d5ff (detached HEAD)
/private/tmp/retained-pkg                                                        0009ff9f [autonomous-loop-retained-science-package-2026-04-22]
/private/tmp/review                                                              f38e9fe9 [autonomous-loop-nature-grade-review]
/private/tmp/review-scalar-cycle1                                                21ddc045 (detached HEAD)
/private/tmp/scalar-selector-cycle1-land-0422                                    870030c2 [codex/scalar-selector-cycle1-land]
/private/tmp/scalar-selector-cycle1-theorems-review-0421                         003724b8 (detached HEAD)
/private/tmp/three-sector-review                                                 527864cb [codex/review-three-sector-dim-color-2026-04-25]
/Users/jonreilly/.codex/worktrees/7872/CL3Z3 new work                            0a116fa1 [codex/koide-q-physical-carrier-source-selection]
/Users/jonreilly/.codex/worktrees/8805/CL3Z3 new work                            037aded3 (detached HEAD)
/Users/jonreilly/.codex/worktrees/e76c/hierarchy-review-packet                   e8877356 [codex/hierarchy-retained-close-2026-04-22]
/Users/jonreilly/.codex/worktrees/e76c/koide-q-review-packet                     b2192666 [codex/koide-q-review-packet-2026-04-22]
/Users/jonreilly/.codex/worktrees/e76c/planck-scale-program                      ceb6d0f9 [codex/planck-scale-program-2026-04-23]
/Users/jonreilly/Projects/CL3Z3 new work                                         00677a06 [codex/koide-resume-2026-04-18]
/Users/jonreilly/Projects/Physics/.claude/worktrees/blissful-tu-ccc1e8           1543fd81 [claude/ai-methodology-capture-2026-04-25]
/Users/jonreilly/Projects/Physics/.claude/worktrees/charming-stonebraker-7078d0  200621a9 [review/scalar-selector-cycle1-theorems]
/Users/jonreilly/Projects/Physics/.claude/worktrees/crazy-pascal-8623c8          adf80784 [claude/crazy-pascal-8623c8]
/Users/jonreilly/Projects/Physics/.claude/worktrees/romantic-chatterjee-331089   0aebc41f [ckm-magnitudes-structural-counts-dimension-uniqueness]
```

## 2. Full `git branch -r` (remote branches, verbatim)

Includes all `origin/*`, `scalarp3p7/*`, and other remote refs.

**Total remote refs:** 321

```text
  origin/HEAD -> origin/main
  origin/afternoon-4-21
  origin/afternoon-4-21-proposal
  origin/alpha-lm-geometric-mean-identity
  origin/area-law-update
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
  origin/ckm-magnitudes-structural-counts-dimension-uniqueness
  origin/ckm-nlo-protected-gamma-derivation
  origin/ckm-scale-convention-theorem
  origin/ckm-second-row-magnitudes
  origin/ckm-thales-cross-system-cp-ratio
  origin/ckm-thales-pinned-alpha-s-independent-ratios
  origin/ckm-third-row-magnitudes
  origin/ckm-unitarity-triangle-right-angle
  origin/claude/ai-methodology-capture-2026-04-25
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
  origin/claude/raw-methodology-dump-2026-04-25
  origin/claude/relaxed-taussig-18d9fb
  origin/claude/sad-yonath
  origin/claude/source-proximal-symmetric-endpoint-2026-04-24
  origin/claude/stupefied-khayyam
  origin/claude/taste-scalar-isotropy
  origin/claude/update-interest-scores-wMCAI
  origin/claude/vigilant-turing-e374dd
  origin/claude/ward-identity-derivation
  origin/claude/youthful-neumann
  origin/claude/yt-retention-landing-2026-04-18
  origin/claude/yt-ward-supersedes-bridge-proposal
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
  origin/codex/land-three-sector-support-2026-04-25
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
  origin/cosmology-frw-kinematic-reduction
  origin/cross-lane-consistency-support
  origin/cross-sector-koide-ckm-vcb-bridge
  origin/evening-4-20
  origin/evening-4-21
  origin/fractional-charge-denominator-from-n-c
  origin/framework-bare-alpha-3-alpha-em-dimension-ratio
  origin/framework-three-sector-dimension-color-quadratic-identity
  origin/fresh/clean-slate
  origin/frontier/cl3-sm-embedding
  origin/frontier/dm-leptons-review
  origin/frontier/framework-review
  origin/frontier/hydrogen-helium-review
  origin/frontier/lepton-mass-tower
  origin/graviton-spectral-tower
  origin/gravity-cosmology-tower-lambda-spectral-bridge
  origin/hypercharge-squared-trace-catalog
  origin/koide-brannen-ch-three-gap-review
  origin/koide-equivariant-berry-aps-selector
  origin/koide-q-eq-3delta-doublet-magnitude-route
  origin/koide-q23-anomaly-structural-attack
  origin/koide-q23-lattice-oh-stabilizer
  origin/koide-q23-spin1-structural-route
  origin/koide-q23-spin1-subroute-status
  origin/koide-q23-variational-coupling-conjecture
  origin/lambda-qcd-derivation-support
  origin/lh-anomaly-trace-catalog
  origin/lorentz-boost-covariance
  origin/lorentz-kernel-positive-closure-v2
  origin/main
  origin/matter-radiation-equality-structural-identity
  origin/monopole-mass-consolidation-theorem
  origin/morning-4
  origin/morning-4-20
  origin/morning-4-21
  origin/morning3-4-20
  origin/morning4-4-20
  origin/n-eff-from-three-generations
  origin/neutrino-mass-sum-prediction
  origin/neutrino-native-axiom-observable-bounds
  origin/neutrino-solar-gap-alpha-lm-squared
  origin/neutrino-three-level-staircase-proposal
  origin/neutrinoless-double-beta-mbb-prediction
  origin/omega-lambda-matter-bridge-theorem
  origin/one-more-for-the-canonical
  origin/physical-bridge
  origin/r-base-group-theory-derivation
  origin/review-active
  origin/review/bell-inequality-clean
  origin/review/bell-inequality-structural
  origin/review/dm-blocker-3-deep-impossibility-triangulation
  origin/review/koide-charged-lepton-axiom-native
  origin/review/koide-charged-lepton-for-main
  origin/review/koide-circulant-character-derivation
  origin/review/koide-one-scalar-obstruction-triangulation
  origin/review/lepton-pmns-integration-package
  origin/review/path-a-sylvester-branch-theorem
  origin/review/scalar-selector-cycle1-theorems
  origin/scalar-harmonic-tower
  origin/scalar-selector-cycle1-latest-review
  origin/sm-hypercharge-uniqueness
  origin/su2-witten-z2-anomaly
  origin/su3-cubic-anomaly-cancellation
  origin/tensor-scalar-ratio-consolidation-theorem
  origin/tritium-beta-effective-mass-prediction
  origin/universal-theta-induced-edm-vanishing
  origin/vector-gauge-field-kk-tower
  origin/wolfenstein-lambda-a-structural-identities
  origin/worktree-bonus-predictions
  origin/worktree-confinement
  origin/worktree-continuum-id
  origin/worktree-lorentz-invariance
  origin/worktree-plaquette-self-consistency
  origin/worktree-session-delta
  origin/worktree-strong-cp-nature
  scalarp3p7/HEAD -> scalarp3p7/codex/scalar-selector-p3-p7-package
  scalarp3p7/claude/angry-chatelet-2dc78c
  scalarp3p7/claude/charged-lepton-closure-review
  scalarp3p7/claude/charming-hopper-7dd4fe
  scalarp3p7/claude/charming-stonebraker-7078d0
  scalarp3p7/claude/cl3-minimality
  scalarp3p7/claude/clever-lewin-1f8af5
  scalarp3p7/claude/dreamy-wing-969574
  scalarp3p7/claude/eloquent-bouman
  scalarp3p7/claude/flamboyant-bose-6ac105
  scalarp3p7/claude/frosty-wu-53fb11
  scalarp3p7/claude/g-bare-closure-2026-04-18
  scalarp3p7/claude/g1-complete
  scalarp3p7/claude/goofy-mendeleev
  scalarp3p7/claude/graviton-mass-identity
  scalarp3p7/claude/happy-goldwasser-3d61bc
  scalarp3p7/claude/inspiring-banzai-7002dd
  scalarp3p7/claude/keen-cray
  scalarp3p7/claude/main-derived
  scalarp3p7/claude/naughty-kowalevski-d14f8c
  scalarp3p7/claude/naughty-shannon-32369e
  scalarp3p7/claude/nice-gauss-9b7133
  scalarp3p7/claude/quizzical-aryabhata-a135bb
  scalarp3p7/claude/silly-perlman
  scalarp3p7/claude/tender-mendeleev-a4ed81
  scalarp3p7/claude/vigilant-turing-e374dd
  scalarp3p7/claude/ward-identity-derivation
  scalarp3p7/claude/xenodochial-dubinsky-512435
  scalarp3p7/claude/youthful-neumann
  scalarp3p7/claude/yt-retention-landing-2026-04-18
  scalarp3p7/claude/yt-ward-supersedes-bridge-proposal
  scalarp3p7/codex/bell-cleanup-2026-04-17
  scalarp3p7/codex/bell-promotion-2026-04-17
  scalarp3p7/codex/bh-entropy-main-land-2026-04-17
  scalarp3p7/codex/charged-lepton-propagation-2026-04-17
  scalarp3p7/codex/ckm-edm-split-2026-04-17
  scalarp3p7/codex/ckm-scope-fix
  scalarp3p7/codex/cl3-minimality-review
  scalarp3p7/codex/derived-science-salvage
  scalarp3p7/codex/dm-boundary-arrest-review
  scalarp3p7/codex/dm-leptons-land
  scalarp3p7/codex/dm-parity-observable-route-2026-04-17
  scalarp3p7/codex/dm-science-review-2026-04-18
  scalarp3p7/codex/dm-thermal-landing-2026-04-17
  scalarp3p7/codex/ew-scope-fix
  scalarp3p7/codex/five-cleanups
  scalarp3p7/codex/framework-land
  scalarp3p7/codex/framework-point-beta6-cleanup-2026-04-17
  scalarp3p7/codex/framework-review
  scalarp3p7/codex/g-bare-closure-review
  scalarp3p7/codex/g-bare-land-2026-04-18
  scalarp3p7/codex/g-bare-salvage-2026-04-18
  scalarp3p7/codex/g-bare-support-land
  scalarp3p7/codex/g-bare-two-ward-land
  scalarp3p7/codex/g1-complete-review
  scalarp3p7/codex/higgs-top-scope-fix
  scalarp3p7/codex/hydrogen-helium-land
  scalarp3p7/codex/hydrogen-helium-review-audit
  scalarp3p7/codex/hydrogen-helium-salvage
  scalarp3p7/codex/i5-local-selector-no-go
  scalarp3p7/codex/i5-ne-seed-manifold
  scalarp3p7/codex/issr1-closure-push
  scalarp3p7/codex/koide-resume-2026-04-18
  scalarp3p7/codex/land-charged-lepton-2026-04-17
  scalarp3p7/codex/land-cl3-support-2026-04-18
  scalarp3p7/codex/land-cosmology-eos-2026-04-18
  scalarp3p7/codex/land-dm-p3-sylvester-2026-04-18
  scalarp3p7/codex/land-dm-path-a-sylvester-2026-04-18
  scalarp3p7/codex/land-graviton-mass-identity
  scalarp3p7/codex/land-lepton-pmns-2026-04-19
  scalarp3p7/codex/land-quark-science-2026-04-19
  scalarp3p7/codex/land-yt-retention-2026-04-18
  scalarp3p7/codex/lepto-selector-closeout-main-2026-04-17
  scalarp3p7/codex/leptogenesis-science-review-2026-04-16
  scalarp3p7/codex/local-preserve-2026-04-18
  scalarp3p7/codex/main-graph-first
  scalarp3p7/codex/main-preserve-2026-04-18
  scalarp3p7/codex/matter-lane
  scalarp3p7/codex/neutrino-dm-package-2026-04-16
  scalarp3p7/codex/neutrino-package-date-review
  scalarp3p7/codex/neutrino-package-review
  scalarp3p7/codex/one-axiom-scope-fix
  scalarp3p7/codex/p-derived
  scalarp3p7/codex/pf-salvage-2026-04-18
  scalarp3p7/codex/pf-science-review-2026-04-18
  scalarp3p7/codex/plaquette-env-review
  scalarp3p7/codex/plaquette-env-transfer
  scalarp3p7/codex/plaquette-main-land
  scalarp3p7/codex/publication-prep
  scalarp3p7/codex/qg-continuum-update
  scalarp3p7/codex/quark-route2-land
  scalarp3p7/codex/quark-route2-review
  scalarp3p7/codex/quark-shell-normalization-publish-2026-04-19
  scalarp3p7/codex/quark-shell-normalization-publish-2026-04-19-v2
  scalarp3p7/codex/quark-shell-normalization-publish-2026-04-19-v3
  scalarp3p7/codex/quark-shell-normalization-publish-2026-04-19-v4
  scalarp3p7/codex/repo-landing-surface
  scalarp3p7/codex/review-active
  scalarp3p7/codex/review-frontier-cl3-sm-embedding
  scalarp3p7/codex/root-dirty-preserve-2026-04-14
  scalarp3p7/codex/root-publication-mainline
  scalarp3p7/codex/root-release-entry
  scalarp3p7/codex/sad-yonath-atlas-sweep-2026-04-17
  scalarp3p7/codex/scalar-selector-cycle1-berry-push
  scalarp3p7/codex/scalar-selector-cycle1-issr1-push
  scalarp3p7/codex/scalar-selector-cycle1-proof-review
  scalarp3p7/codex/scalar-selector-cycle1-retained-closeout
  scalarp3p7/codex/scalar-selector-cycle1-review
  scalarp3p7/codex/scalar-selector-cycle1-theorems-push
  scalarp3p7/codex/scalar-selector-p3-p7-package
  scalarp3p7/codex/science-3plus1-line-law
  scalarp3p7/codex/science-3plus1-line-law-support
  scalarp3p7/codex/science-workspace-2026-04-18
  scalarp3p7/codex/status-standardization-2026-04-17
  scalarp3p7/codex/strong-cp-scope-fix
  scalarp3p7/codex/vigilant-turing-land
  scalarp3p7/codex/ward-promotion-2026-04-17
  scalarp3p7/codex/yt-lane-primary-2026-04-17
  scalarp3p7/frontier/cl3-sm-embedding
  scalarp3p7/frontier/dm-leptons-review
  scalarp3p7/frontier/framework-review
  scalarp3p7/frontier/hydrogen-helium
  scalarp3p7/frontier/hydrogen-helium-review
  scalarp3p7/frontier/lepton-mass-tower
  scalarp3p7/main
  scalarp3p7/morning-4-20
  scalarp3p7/review/bell-inequality-clean
  scalarp3p7/review/bell-inequality-structural
  scalarp3p7/review/scalar-selector-cycle1-theorems
  scalarp3p7/review/scalar-selector-cycle1-theorems-push
  scalarp3p7/scalar-selector-cycle1-latest-review
```

## 3. Full `git branch -a` (all branches, local + remote)

**Total branches:** 471

```text
  alpha-lm-geometric-mean-identity
+ autonomous-loop-index-2026-04-22
+ autonomous-loop-index-update-2026-04-22
+ autonomous-loop-nature-grade-review
+ autonomous-loop-retained-science-package-2026-04-22
  bminusl-anomaly-freedom
  ckm-bs-mixing-phase-derivation
  ckm-cp-phase-structural-identity
  ckm-cp-product-alpha-s-cross-sector-extraction
  ckm-first-row-magnitudes
  ckm-kaon-epsilon-k-jarlskog-decomposition
+ ckm-magnitudes-structural-counts-dimension-uniqueness
  ckm-nlo-protected-gamma-derivation
+ ckm-scale-convention-theorem
  ckm-second-row-magnitudes
  ckm-thales-cross-system-cp-ratio
  ckm-thales-pinned-alpha-s-independent-ratios
  ckm-third-row-magnitudes
  ckm-unitarity-triangle-right-angle
* claude/ai-methodology-capture-2026-04-25
  claude/axiom-native-overnight-FtUl5
  claude/blissful-tu-ccc1e8
+ claude/crazy-pascal-8623c8
  claude/flamboyant-germain-3060cb
+ claude/raw-methodology-dump-2026-04-25
  claude/romantic-chatterjee-331089
  claude/upbeat-williamson-a2ff73
  claude/zen-turing-06eeca
+ codex/atomic-hydrogen-helium-land
+ codex/ckm-bs-mixing-phase-land
+ codex/ckm-first-row-magnitudes-land
  codex/ckm-first-row-magnitudes-salvage
+ codex/ckm-kaon-epsilon-land
+ codex/ckm-nlo-protected-gamma-land
  codex/close-open-physics-2026-04-22
+ codex/cross-sector-koide-vcb-land
  codex/emergent-geometry-metric-audit
+ codex/framework-bare-alpha-ratio-land
+ codex/hierarchy-retained-close-2026-04-22
  codex/high-impact-retain-native
  codex/koide-q-carrier-selection-obstruction
  codex/koide-q-closure-obstruction
  codex/koide-q-criterion-support
+ codex/koide-q-physical-carrier-source-selection
+ codex/koide-q-review-packet-2026-04-22
+ codex/koide-resume-2026-04-18
+ codex/land-ai-methodology-lane-2026-04-25
+ codex/land-area-law-quarter-2026-04-25
+ codex/land-ckm-bs-mixing-2026-04-25
+ codex/land-ckm-cp-product-alpha-s-2026-04-25
+ codex/land-ckm-second-row-2026-04-25
+ codex/land-ckm-second-row-main-2026-04-25
+ codex/land-ckm-structcounts-2026-04-25
+ codex/land-ckm-thales-alpha-independent
+ codex/land-ckm-thales-cp-ratio-2026-04-25
+ codex/land-gravity-lambda-tower-bridge-2026-04-25
+ codex/land-great-nobel-ab743c
+ codex/land-great-nobel-ab743c-v2
+ codex/land-hypercharge-squared-trace-catalog-2026-04-25
+ codex/land-koide-a1-fractional-topology-2026-04-25
+ codex/land-koide-full-workstream-science-2026-04-25
+ codex/land-koide-q-minimal-selector-convention-2026-04-25
+ codex/land-lh-anomaly-trace-catalog-2026-04-25
+ codex/land-lorentz-boost-covariance-2026-04-25
+ codex/land-lorentz-kernel-positive-closure-2026-04-25
+ codex/land-planck-source-unit-support
+ codex/land-three-sector-support-2026-04-25
  codex/open-item-closure-2026-04-24
  codex/planck-boundary-density-extension-2026-04-24
+ codex/planck-scale-program-2026-04-23
+ codex/quark-taste-staircase-support-land
+ codex/review-ai-methodology-capture-2026-04-25
+ codex/review-ckm-structcounts-dim-2026-04-25
+ codex/review-three-sector-dim-color-2026-04-25
+ codex/review-three-sector-dim-color-2026-04-25-092340
+ codex/scalar-selector-cycle1-land
  cosmology-frw-kinematic-reduction
  cosmology-matter-bridge-scout
+ cross-lane-consistency-support
  cross-sector-koide-ckm-vcb-bridge
  fractional-charge-denominator-from-n-c
  framework-bare-alpha-3-alpha-em-dimension-ratio
  framework-three-sector-dimension-color-quadratic-identity
  fresh/clean-slate
  graviton-spectral-tower
  gravity-cosmology-tower-lambda-spectral-bridge
  hypercharge-squared-trace-catalog
+ koide-brannen-ch-three-gap-review
+ koide-q-eq-3delta-doublet-magnitude-route
+ koide-q23-anomaly-structural-attack
+ koide-q23-lattice-oh-stabilizer
+ koide-q23-spin1-structural-route
+ koide-q23-spin1-subroute-status
+ koide-q23-variational-coupling-conjecture
+ lambda-qcd-derivation-support
  lh-anomaly-trace-catalog
+ lorentz-boost-covariance-review-note
+ main
  matter-radiation-equality-structural-identity
+ monopole-mass-consolidation-theorem
  n-eff-from-three-generations
+ neutrino-mass-sum-prediction
  neutrino-native-axiom-observable-bounds
+ neutrino-solar-gap-alpha-lm-squared
+ neutrino-three-level-staircase-proposal
+ neutrinoless-double-beta-mbb-prediction
+ omega-lambda-matter-bridge-theorem
  physical-bridge
  r-base-group-theory-derivation
+ review/scalar-selector-cycle1-theorems
  scalar-harmonic-tower
  scout-eighteenth-closure
  scout-eighth-closure
  scout-eleventh-closure
  scout-fifteenth-closure
  scout-fifth-closure
  scout-fourteenth-closure
  scout-fourth-closure
  scout-next-closure
  scout-nineteenth-closure
  scout-ninth-closure
  scout-seventeenth-closure
  scout-seventh-closure
  scout-sixteenth-closure
  scout-sixth-closure
  scout-tenth-closure
  scout-third-closure
  scout-thirteenth-closure
  scout-thirtieth-closure
  scout-thirtyfirst-closure
  scout-thirtysecond-closure
  scout-twelfth-closure
  scout-twentieth-closure
  scout-twentyeighth-closure
  scout-twentyfifth-closure
  scout-twentyfirst-closure
  scout-twentyfourth-closure
  scout-twentyninth-closure
  scout-twentysecond-closure
  scout-twentyseventh-closure
  scout-twentysixth-closure
  scout-twentythird-closure
  sm-hypercharge-uniqueness
  su2-witten-z2-anomaly
  su3-cubic-anomaly-cancellation
+ tensor-scalar-ratio-consolidation-theorem
+ tritium-beta-effective-mass-prediction
  universal-theta-induced-edm-vanishing
  vector-gauge-field-kk-tower
  wolfenstein-lambda-a-structural-identities
  remotes/origin/HEAD -> origin/main
  remotes/origin/afternoon-4-21
  remotes/origin/afternoon-4-21-proposal
  remotes/origin/alpha-lm-geometric-mean-identity
  remotes/origin/area-law-update
  remotes/origin/autonomous-loop-index-2026-04-22
  remotes/origin/autonomous-loop-index-update-2026-04-22
  remotes/origin/autonomous-loop-nature-grade-review
  remotes/origin/autonomous-loop-retained-science-package-2026-04-22
  remotes/origin/bminusl-anomaly-freedom
  remotes/origin/ckm-bs-mixing-phase-derivation
  remotes/origin/ckm-cp-phase-structural-identity
  remotes/origin/ckm-cp-product-alpha-s-cross-sector-extraction
  remotes/origin/ckm-first-row-magnitudes
  remotes/origin/ckm-kaon-epsilon-k-jarlskog-decomposition
  remotes/origin/ckm-magnitudes-structural-counts-dimension-uniqueness
  remotes/origin/ckm-nlo-protected-gamma-derivation
  remotes/origin/ckm-scale-convention-theorem
  remotes/origin/ckm-second-row-magnitudes
  remotes/origin/ckm-thales-cross-system-cp-ratio
  remotes/origin/ckm-thales-pinned-alpha-s-independent-ratios
  remotes/origin/ckm-third-row-magnitudes
  remotes/origin/ckm-unitarity-triangle-right-angle
  remotes/origin/claude/ai-methodology-capture-2026-04-25
  remotes/origin/claude/angry-chatelet-2dc78c
  remotes/origin/claude/angry-feynman-2df312
  remotes/origin/claude/axiom-native-overnight-FtUl5
  remotes/origin/claude/charged-lepton-closure-review
  remotes/origin/claude/cl3-minimality
  remotes/origin/claude/derived-science-clean
  remotes/origin/claude/dreamy-wing-969574
  remotes/origin/claude/eloquent-wilbur
  remotes/origin/claude/framework-point-beta-6-lane
  remotes/origin/claude/g1-complete
  remotes/origin/claude/graviton-mass-identity
  remotes/origin/claude/great-nobel-ab743c
  remotes/origin/claude/inspiring-banzai-7002dd
  remotes/origin/claude/koide-a1-casimir-difference-FtUl5
  remotes/origin/claude/koide-a1-irreducibility-package
  remotes/origin/claude/koide-a1-round10-fractional-topology
  remotes/origin/claude/main-derived
  remotes/origin/claude/mass-ratio-package
  remotes/origin/claude/mass-spectrum-phase-2-scoping
  remotes/origin/claude/raw-methodology-dump-2026-04-25
  remotes/origin/claude/relaxed-taussig-18d9fb
  remotes/origin/claude/sad-yonath
  remotes/origin/claude/source-proximal-symmetric-endpoint-2026-04-24
  remotes/origin/claude/stupefied-khayyam
  remotes/origin/claude/taste-scalar-isotropy
  remotes/origin/claude/update-interest-scores-wMCAI
  remotes/origin/claude/vigilant-turing-e374dd
  remotes/origin/claude/ward-identity-derivation
  remotes/origin/claude/youthful-neumann
  remotes/origin/claude/yt-retention-landing-2026-04-18
  remotes/origin/claude/yt-ward-supersedes-bridge-proposal
  remotes/origin/codex/area-law-quarter-coefficient
  remotes/origin/codex/area-law-quarter-residual-carriers
  remotes/origin/codex/area-law-target2-algebraic-spectrum
  remotes/origin/codex/area-law-target2-primitive-edge
  remotes/origin/codex/baryogenesis-frozen-2026-04-16
  remotes/origin/codex/ckm-bs-mixing-phase-land
  remotes/origin/codex/ckm-first-row-magnitudes-land
  remotes/origin/codex/ckm-full-package-review
  remotes/origin/codex/ckm-kaon-epsilon-land
  remotes/origin/codex/ckm-nlo-protected-gamma-land
  remotes/origin/codex/clean-main-2026-04-24
  remotes/origin/codex/cross-sector-koide-vcb-land
  remotes/origin/codex/dm-close-last-two
  remotes/origin/codex/dm-leptons-land
  remotes/origin/codex/dm-science-reviewed-2026-04-17
  remotes/origin/codex/dm-selector-closeout-main-2026-04-17
  remotes/origin/codex/dm-thermal-review-2026-04-17
  remotes/origin/codex/framework-bare-alpha-ratio-land
  remotes/origin/codex/g-bare-land-2026-04-18
  remotes/origin/codex/g-bare-two-ward-land
  remotes/origin/codex/hierarchy-retained-close-2026-04-22
  remotes/origin/codex/hydrogen-helium-salvage
  remotes/origin/codex/koide-dimensionless-closure-proposal-2026-04-24
  remotes/origin/codex/koide-dimensionless-objection-closure-2026-04-24
  remotes/origin/codex/koide-dimensionless-objection-closure-main-2026-04-24
  remotes/origin/codex/koide-full-workstream-science-2026-04-25
  remotes/origin/codex/koide-native-dimensionless-closure-2026-04-24
  remotes/origin/codex/koide-p-3plus1-transport
  remotes/origin/codex/land-graviton-mass-identity
  remotes/origin/codex/land-three-sector-support-2026-04-25
  remotes/origin/codex/lepto-selector-closeout-main-2026-04-17
  remotes/origin/codex/leptogenesis-science-review-2026-04-16
  remotes/origin/codex/main-derived-quark-route2-science-stack
  remotes/origin/codex/main-derived-quark-science-stack
  remotes/origin/codex/main-graph-first
  remotes/origin/codex/neutrino-dm-package-2026-04-16
  remotes/origin/codex/neutrino-retained-lanes-review
  remotes/origin/codex/neutrino-science-main-derived-2026-04-16
  remotes/origin/codex/p-derivation-package
  remotes/origin/codex/p-derived-science-review
  remotes/origin/codex/pf-path-ground-2026-04-17
  remotes/origin/codex/pf-salvage-2026-04-18
  remotes/origin/codex/pf-science-review-2026-04-18
  remotes/origin/codex/planck-scale-program-2026-04-23
  remotes/origin/codex/planck-source-unit-clean-science-2026-04-25
  remotes/origin/codex/planck-source-unit-resubmission-clean-2026-04-25
  remotes/origin/codex/plaquette-env-review
  remotes/origin/codex/plaquette-env-transfer
  remotes/origin/codex/publication-prep
  remotes/origin/codex/qg-continuum-update
  remotes/origin/codex/repo-landing-surface
  remotes/origin/codex/review-active
  remotes/origin/codex/root-publication-mainline
  remotes/origin/codex/root-release-entry
  remotes/origin/codex/scalar-selector-cycle1-review
  remotes/origin/codex/science-3plus1-line-law
  remotes/origin/codex/taste-scalar-isotropy-main-2026-04-16
  remotes/origin/codex/three-generation-observable-main-2026-04-15
  remotes/origin/codex/wip-isolation-2026-04-14
  remotes/origin/codex/yt-unbounded-main-package-2026-04-15
  remotes/origin/cosmology-frw-kinematic-reduction
  remotes/origin/cross-lane-consistency-support
  remotes/origin/cross-sector-koide-ckm-vcb-bridge
  remotes/origin/evening-4-20
  remotes/origin/evening-4-21
  remotes/origin/fractional-charge-denominator-from-n-c
  remotes/origin/framework-bare-alpha-3-alpha-em-dimension-ratio
  remotes/origin/framework-three-sector-dimension-color-quadratic-identity
  remotes/origin/fresh/clean-slate
  remotes/origin/frontier/cl3-sm-embedding
  remotes/origin/frontier/dm-leptons-review
  remotes/origin/frontier/framework-review
  remotes/origin/frontier/hydrogen-helium-review
  remotes/origin/frontier/lepton-mass-tower
  remotes/origin/graviton-spectral-tower
  remotes/origin/gravity-cosmology-tower-lambda-spectral-bridge
  remotes/origin/hypercharge-squared-trace-catalog
  remotes/origin/koide-brannen-ch-three-gap-review
  remotes/origin/koide-equivariant-berry-aps-selector
  remotes/origin/koide-q-eq-3delta-doublet-magnitude-route
  remotes/origin/koide-q23-anomaly-structural-attack
  remotes/origin/koide-q23-lattice-oh-stabilizer
  remotes/origin/koide-q23-spin1-structural-route
  remotes/origin/koide-q23-spin1-subroute-status
  remotes/origin/koide-q23-variational-coupling-conjecture
  remotes/origin/lambda-qcd-derivation-support
  remotes/origin/lh-anomaly-trace-catalog
  remotes/origin/lorentz-boost-covariance
  remotes/origin/lorentz-kernel-positive-closure-v2
  remotes/origin/main
  remotes/origin/matter-radiation-equality-structural-identity
  remotes/origin/monopole-mass-consolidation-theorem
  remotes/origin/morning-4
  remotes/origin/morning-4-20
  remotes/origin/morning-4-21
  remotes/origin/morning3-4-20
  remotes/origin/morning4-4-20
  remotes/origin/n-eff-from-three-generations
  remotes/origin/neutrino-mass-sum-prediction
  remotes/origin/neutrino-native-axiom-observable-bounds
  remotes/origin/neutrino-solar-gap-alpha-lm-squared
  remotes/origin/neutrino-three-level-staircase-proposal
  remotes/origin/neutrinoless-double-beta-mbb-prediction
  remotes/origin/omega-lambda-matter-bridge-theorem
  remotes/origin/one-more-for-the-canonical
  remotes/origin/physical-bridge
  remotes/origin/r-base-group-theory-derivation
  remotes/origin/review-active
  remotes/origin/review/bell-inequality-clean
  remotes/origin/review/bell-inequality-structural
  remotes/origin/review/dm-blocker-3-deep-impossibility-triangulation
  remotes/origin/review/koide-charged-lepton-axiom-native
  remotes/origin/review/koide-charged-lepton-for-main
  remotes/origin/review/koide-circulant-character-derivation
  remotes/origin/review/koide-one-scalar-obstruction-triangulation
  remotes/origin/review/lepton-pmns-integration-package
  remotes/origin/review/path-a-sylvester-branch-theorem
  remotes/origin/review/scalar-selector-cycle1-theorems
  remotes/origin/scalar-harmonic-tower
  remotes/origin/scalar-selector-cycle1-latest-review
  remotes/origin/sm-hypercharge-uniqueness
  remotes/origin/su2-witten-z2-anomaly
  remotes/origin/su3-cubic-anomaly-cancellation
  remotes/origin/tensor-scalar-ratio-consolidation-theorem
  remotes/origin/tritium-beta-effective-mass-prediction
  remotes/origin/universal-theta-induced-edm-vanishing
  remotes/origin/vector-gauge-field-kk-tower
  remotes/origin/wolfenstein-lambda-a-structural-identities
  remotes/origin/worktree-bonus-predictions
  remotes/origin/worktree-confinement
  remotes/origin/worktree-continuum-id
  remotes/origin/worktree-lorentz-invariance
  remotes/origin/worktree-plaquette-self-consistency
  remotes/origin/worktree-session-delta
  remotes/origin/worktree-strong-cp-nature
  remotes/scalarp3p7/HEAD -> scalarp3p7/codex/scalar-selector-p3-p7-package
  remotes/scalarp3p7/claude/angry-chatelet-2dc78c
  remotes/scalarp3p7/claude/charged-lepton-closure-review
  remotes/scalarp3p7/claude/charming-hopper-7dd4fe
  remotes/scalarp3p7/claude/charming-stonebraker-7078d0
  remotes/scalarp3p7/claude/cl3-minimality
  remotes/scalarp3p7/claude/clever-lewin-1f8af5
  remotes/scalarp3p7/claude/dreamy-wing-969574
  remotes/scalarp3p7/claude/eloquent-bouman
  remotes/scalarp3p7/claude/flamboyant-bose-6ac105
  remotes/scalarp3p7/claude/frosty-wu-53fb11
  remotes/scalarp3p7/claude/g-bare-closure-2026-04-18
  remotes/scalarp3p7/claude/g1-complete
  remotes/scalarp3p7/claude/goofy-mendeleev
  remotes/scalarp3p7/claude/graviton-mass-identity
  remotes/scalarp3p7/claude/happy-goldwasser-3d61bc
  remotes/scalarp3p7/claude/inspiring-banzai-7002dd
  remotes/scalarp3p7/claude/keen-cray
  remotes/scalarp3p7/claude/main-derived
  remotes/scalarp3p7/claude/naughty-kowalevski-d14f8c
  remotes/scalarp3p7/claude/naughty-shannon-32369e
  remotes/scalarp3p7/claude/nice-gauss-9b7133
  remotes/scalarp3p7/claude/quizzical-aryabhata-a135bb
  remotes/scalarp3p7/claude/silly-perlman
  remotes/scalarp3p7/claude/tender-mendeleev-a4ed81
  remotes/scalarp3p7/claude/vigilant-turing-e374dd
  remotes/scalarp3p7/claude/ward-identity-derivation
  remotes/scalarp3p7/claude/xenodochial-dubinsky-512435
  remotes/scalarp3p7/claude/youthful-neumann
  remotes/scalarp3p7/claude/yt-retention-landing-2026-04-18
  remotes/scalarp3p7/claude/yt-ward-supersedes-bridge-proposal
  remotes/scalarp3p7/codex/bell-cleanup-2026-04-17
  remotes/scalarp3p7/codex/bell-promotion-2026-04-17
  remotes/scalarp3p7/codex/bh-entropy-main-land-2026-04-17
  remotes/scalarp3p7/codex/charged-lepton-propagation-2026-04-17
  remotes/scalarp3p7/codex/ckm-edm-split-2026-04-17
  remotes/scalarp3p7/codex/ckm-scope-fix
  remotes/scalarp3p7/codex/cl3-minimality-review
  remotes/scalarp3p7/codex/derived-science-salvage
  remotes/scalarp3p7/codex/dm-boundary-arrest-review
  remotes/scalarp3p7/codex/dm-leptons-land
  remotes/scalarp3p7/codex/dm-parity-observable-route-2026-04-17
  remotes/scalarp3p7/codex/dm-science-review-2026-04-18
  remotes/scalarp3p7/codex/dm-thermal-landing-2026-04-17
  remotes/scalarp3p7/codex/ew-scope-fix
  remotes/scalarp3p7/codex/five-cleanups
  remotes/scalarp3p7/codex/framework-land
  remotes/scalarp3p7/codex/framework-point-beta6-cleanup-2026-04-17
  remotes/scalarp3p7/codex/framework-review
  remotes/scalarp3p7/codex/g-bare-closure-review
  remotes/scalarp3p7/codex/g-bare-land-2026-04-18
  remotes/scalarp3p7/codex/g-bare-salvage-2026-04-18
  remotes/scalarp3p7/codex/g-bare-support-land
  remotes/scalarp3p7/codex/g-bare-two-ward-land
  remotes/scalarp3p7/codex/g1-complete-review
  remotes/scalarp3p7/codex/higgs-top-scope-fix
  remotes/scalarp3p7/codex/hydrogen-helium-land
  remotes/scalarp3p7/codex/hydrogen-helium-review-audit
  remotes/scalarp3p7/codex/hydrogen-helium-salvage
  remotes/scalarp3p7/codex/i5-local-selector-no-go
  remotes/scalarp3p7/codex/i5-ne-seed-manifold
  remotes/scalarp3p7/codex/issr1-closure-push
  remotes/scalarp3p7/codex/koide-resume-2026-04-18
  remotes/scalarp3p7/codex/land-charged-lepton-2026-04-17
  remotes/scalarp3p7/codex/land-cl3-support-2026-04-18
  remotes/scalarp3p7/codex/land-cosmology-eos-2026-04-18
  remotes/scalarp3p7/codex/land-dm-p3-sylvester-2026-04-18
  remotes/scalarp3p7/codex/land-dm-path-a-sylvester-2026-04-18
  remotes/scalarp3p7/codex/land-graviton-mass-identity
  remotes/scalarp3p7/codex/land-lepton-pmns-2026-04-19
  remotes/scalarp3p7/codex/land-quark-science-2026-04-19
  remotes/scalarp3p7/codex/land-yt-retention-2026-04-18
  remotes/scalarp3p7/codex/lepto-selector-closeout-main-2026-04-17
  remotes/scalarp3p7/codex/leptogenesis-science-review-2026-04-16
  remotes/scalarp3p7/codex/local-preserve-2026-04-18
  remotes/scalarp3p7/codex/main-graph-first
  remotes/scalarp3p7/codex/main-preserve-2026-04-18
  remotes/scalarp3p7/codex/matter-lane
  remotes/scalarp3p7/codex/neutrino-dm-package-2026-04-16
  remotes/scalarp3p7/codex/neutrino-package-date-review
  remotes/scalarp3p7/codex/neutrino-package-review
  remotes/scalarp3p7/codex/one-axiom-scope-fix
  remotes/scalarp3p7/codex/p-derived
  remotes/scalarp3p7/codex/pf-salvage-2026-04-18
  remotes/scalarp3p7/codex/pf-science-review-2026-04-18
  remotes/scalarp3p7/codex/plaquette-env-review
  remotes/scalarp3p7/codex/plaquette-env-transfer
  remotes/scalarp3p7/codex/plaquette-main-land
  remotes/scalarp3p7/codex/publication-prep
  remotes/scalarp3p7/codex/qg-continuum-update
  remotes/scalarp3p7/codex/quark-route2-land
  remotes/scalarp3p7/codex/quark-route2-review
  remotes/scalarp3p7/codex/quark-shell-normalization-publish-2026-04-19
  remotes/scalarp3p7/codex/quark-shell-normalization-publish-2026-04-19-v2
  remotes/scalarp3p7/codex/quark-shell-normalization-publish-2026-04-19-v3
  remotes/scalarp3p7/codex/quark-shell-normalization-publish-2026-04-19-v4
  remotes/scalarp3p7/codex/repo-landing-surface
  remotes/scalarp3p7/codex/review-active
  remotes/scalarp3p7/codex/review-frontier-cl3-sm-embedding
  remotes/scalarp3p7/codex/root-dirty-preserve-2026-04-14
  remotes/scalarp3p7/codex/root-publication-mainline
  remotes/scalarp3p7/codex/root-release-entry
  remotes/scalarp3p7/codex/sad-yonath-atlas-sweep-2026-04-17
  remotes/scalarp3p7/codex/scalar-selector-cycle1-berry-push
  remotes/scalarp3p7/codex/scalar-selector-cycle1-issr1-push
  remotes/scalarp3p7/codex/scalar-selector-cycle1-proof-review
  remotes/scalarp3p7/codex/scalar-selector-cycle1-retained-closeout
  remotes/scalarp3p7/codex/scalar-selector-cycle1-review
  remotes/scalarp3p7/codex/scalar-selector-cycle1-theorems-push
  remotes/scalarp3p7/codex/scalar-selector-p3-p7-package
  remotes/scalarp3p7/codex/science-3plus1-line-law
  remotes/scalarp3p7/codex/science-3plus1-line-law-support
  remotes/scalarp3p7/codex/science-workspace-2026-04-18
  remotes/scalarp3p7/codex/status-standardization-2026-04-17
  remotes/scalarp3p7/codex/strong-cp-scope-fix
  remotes/scalarp3p7/codex/vigilant-turing-land
  remotes/scalarp3p7/codex/ward-promotion-2026-04-17
  remotes/scalarp3p7/codex/yt-lane-primary-2026-04-17
  remotes/scalarp3p7/frontier/cl3-sm-embedding
  remotes/scalarp3p7/frontier/dm-leptons-review
  remotes/scalarp3p7/frontier/framework-review
  remotes/scalarp3p7/frontier/hydrogen-helium
  remotes/scalarp3p7/frontier/hydrogen-helium-review
  remotes/scalarp3p7/frontier/lepton-mass-tower
  remotes/scalarp3p7/main
  remotes/scalarp3p7/morning-4-20
  remotes/scalarp3p7/review/bell-inequality-clean
  remotes/scalarp3p7/review/bell-inequality-structural
  remotes/scalarp3p7/review/scalar-selector-cycle1-theorems
  remotes/scalarp3p7/review/scalar-selector-cycle1-theorems-push
  remotes/scalarp3p7/scalar-selector-cycle1-latest-review
```

## 4. Full recent commit log (since 2026-04-22, verbatim)

`git log --since="2026-04-22" --pretty="%h %ai %an %s"`

**Total commits in window:** 69

```text
1543fd81 2026-04-25 10:02:44 -0400 jonathonreilly ai-methodology: add Claude raw capture from jonreilly machine
91b52c8e 2026-04-25 09:45:08 -0400 jonathonreilly docs: add codex raw capture to methodology archive
c36cbe81 2026-04-25 09:28:34 -0400 jonathonreilly docs: add review for ai methodology capture branch
6eddc6f4 2026-04-25 09:16:39 -0400 Codex Autoresearch ai-methodology: move canonical framing paragraph into raw/ bucket
78eace31 2026-04-25 09:13:44 -0400 Codex Autoresearch ai-methodology: land canonical per-paper framing paragraph
070aefa2 2026-04-25 09:11:55 -0400 Codex Autoresearch ai-methodology: seed methodology paper with raw info capture
9d0fbabf 2026-04-25 08:21:06 -0400 jonathonreilly dm: land freezeout-bypass support lane and SU(3) obstruction
efa79982 2026-04-25 08:12:37 -0400 jonathonreilly koide: land source-domain no-go synthesis
db330501 2026-04-25 07:46:03 -0400 jonathonreilly ckm: land NLO protected gamma corollary
d5d3654c 2026-04-25 07:42:09 -0400 jonathonreilly lorentz: land boost-covariance theorem packet
b1bb09ba 2026-04-25 07:40:40 -0400 jonathonreilly ckm: integrate Thales CP-ratio theorem
37796022 2026-04-25 07:27:00 -0400 jonathonreilly ckm: derive cross-system CP-asymmetry ratio mediated by Thales circle
30ddf585 2026-04-25 07:26:16 -0400 jonathonreilly planck: integrate area-law quarter no-go lane
654cb77a 2026-04-25 06:54:46 -0400 Codex Autoresearch area-law: land simple-fiber Widom no-go
ee036eab 2026-04-25 07:21:56 -0400 jonathonreilly ckm: tighten Bs mixing phase guardrail
2c3aaaf9 2026-04-25 07:19:25 -0400 jonathonreilly docs+scripts: land bounded quark taste-staircase support
1e1aa10d 2026-04-25 07:15:13 -0400 jonathonreilly ckm: integrate B_s mixing phase package
4431d3ba 2026-04-25 06:44:17 -0400 jonathonreilly ckm: derive B_s mixing phase from retained inputs
0a579977 2026-04-25 07:02:49 -0400 jonathonreilly docs+scripts: land bounded atomic scaffold lane
8d2f8c5f 2026-04-19 00:51:07 +0000 Claude docs+scripts: open atomic hydrogen/helium scaffold lane
0aa82972 2026-04-25 07:02:04 -0400 jonathonreilly ckm: integrate second-row magnitude package
1f3bb000 2026-04-25 06:13:59 -0400 jonathonreilly ckm: second-row magnitudes structural identities theorem
b51dc51f 2026-04-25 06:42:06 -0400 jonathonreilly ckm: land first-row magnitude identities
b8bd70f8 2026-04-25 06:40:19 -0400 jonathonreilly docs: land hypercharge squared-trace catalog theorem
201ced08 2026-04-25 06:40:01 -0400 jonathonreilly koide: land Q background-zero criterion
95a79235 2026-04-25 06:28:24 -0400 jonathonreilly docs: land LH anomaly trace catalog theorem
ab860f31 2026-04-25 06:21:27 -0400 jonathonreilly docs: land Koide A1 fractional-topology no-go packet
59f7e4f0 2026-04-25 06:04:47 -0400 jonathonreilly gravity: land scalar harmonic tower
200d9e03 2026-04-24 22:54:05 -0400 jonathonreilly ckm: land third-row magnitude identities
7d1ce8ca 2026-04-24 22:41:35 -0400 jonathonreilly koide: land A1 radian bridge audit
d34408bf 2026-04-24 22:22:43 -0400 jonathonreilly ckm: land atlas triangle right-angle identity
f5b67622 2026-04-24 21:59:46 -0400 jonathonreilly gravity: land vector gauge-field compactness tower
2d4618f2 2026-04-24 21:49:52 -0400 jonathonreilly koide: land dimensionless objection review packet
56c6dd5a 2026-04-24 21:19:58 -0400 jonathonreilly strong-cp: land universal theta-induced EDM response
d8dd1bf2 2026-04-24 21:08:24 -0400 jonathonreilly cosmology: land N_eff active-neutrino support
f4633759 2026-04-24 20:47:22 -0400 jonathonreilly cosmology: land matter-radiation equality identity
da2c5b07 2026-04-24 20:35:16 -0400 jonathonreilly ckm: land Wolfenstein structural identities
16c7ecdd 2026-04-24 20:20:40 -0400 jonathonreilly gauge: land fractional charge denominator theorem
e06d8d62 2026-04-24 20:04:28 -0400 jonathonreilly cosmology: land R_base group-theory identity
6668d8d5 2026-04-24 19:48:15 -0400 jonathonreilly anomaly: land SU(3) cubic cancellation theorem
1a226c6d 2026-04-24 19:28:14 -0400 jonathonreilly anomaly: land SU(2) Witten Z2 theorem
b529f37b 2026-04-24 19:14:54 -0400 jonathonreilly Land alpha_LM geometric mean identity
6d8077db 2026-04-24 19:04:21 -0400 jonathonreilly Land Koide pointed-origin exhaustion theorem
e49d201d 2026-04-24 18:53:58 -0400 jonathonreilly Land B-L anomaly freedom theorem
cfd621dd 2026-04-24 18:43:08 -0400 jonathonreilly Land CKM CP-phase structural identity
084e9797 2026-04-24 18:22:47 -0400 jonathonreilly Land SM hypercharge uniqueness theorem
89b04ca5 2026-04-24 18:12:32 -0400 jonathonreilly Land graviton TT compactness spectral tower
25956cac 2026-04-24 18:00:14 -0400 jonathonreilly Land Koide native dimensionless no-go packet
d740bd12 2026-04-24 17:39:56 -0400 jonathonreilly Land FRW cosmology kinematic reduction
fec6bd33 2026-04-24 17:23:37 -0400 jonathonreilly docs: land retained neutrino observable bounds
a55c4717 2026-04-24 17:07:10 -0400 jonathonreilly docs: tighten Planck boundary density scope
9a3526cf 2026-04-24 16:47:17 -0400 jonathonreilly docs: add Planck boundary-density extension theorem
e9a5a2d2 2026-04-24 16:41:38 -0400 jonathonreilly docs: close Planck open routes negatively
e6f11dee 2026-04-24 15:52:26 -0400 jonathonreilly docs: land conditional Planck completion packet
adf80784 2026-04-23 13:17:41 -0400 jonathonreilly Remove control-plane links from public package docs
ec118ec9 2026-04-23 13:16:59 -0400 jonathonreilly Tighten public package entry and validation surfaces
36f1684c 2026-04-23 11:38:27 -0400 jonathonreilly Clean public note language across repo
c67de08e 2026-04-23 11:18:41 -0400 jonathonreilly Demote review-state language in delicate lane notes
854e8649 2026-04-23 10:34:49 -0400 jonathonreilly Clean and re-map public science package
e9099506 2026-04-23 09:57:59 -0400 jonathonreilly Clean public repo authority surfaces
b4b46ae3 2026-04-23 08:57:22 -0400 jonathonreilly open planck scale package lane
71e0872f 2026-04-22 22:24:04 -0400 jonathonreilly salvage retained science support subset
52bfbbcf 2026-04-22 21:27:14 -0400 jonathonreilly Clarify prediction-first public package surfaces
ffe965c7 2026-04-22 21:22:51 -0400 jonathonreilly Land Koide Q second-order support batch
dfe98943 2026-04-22 15:39:12 -0400 jonathonreilly koide: salvage physical-bridge as candidate support route
3f03f0de 2026-04-22 14:37:45 -0400 jonathonreilly koide: land brannen geometry and dirac support addendum
84da12b5 2026-04-22 11:18:46 -0400 jonathonreilly koide: land axiom-native support batch honestly
8e3bef18 2026-04-22 10:57:22 -0400 jonathonreilly docs: sync g_bare obstruction note with runner semantics
56876669 2026-04-22 10:17:48 -0400 jonathonreilly Clean public package surface and remove internal docs
```

## 5. Hygiene/review-related commits (since 2026-04-15, verbatim)

`git log --all --since="2026-04-15" --pretty="%h %s" | grep -iE "review|land|salvage|clean|hygiene|integrate|tighten|demote|retire|normalize"`

**Total matching commits:** 401

```text
fc5bcceb framework: land three-sector dimension-color support
e7147163 docs: add review for three-sector dimension-color identity
794b015b area-law: land algebraic spectrum entropy no-go
a60d5614 area-law: land primitive-edge entropy selector no-go
cb4f4f27 area-law: land multipocket selector no-go
c36cbe81 docs: add review for ai methodology capture branch
4da26702 docs: land AI methodology lane
5c912604 area-law: land simple-fiber Widom no-go
b684741f ew: land bare alpha ratio support
68abeea2 index on codex/koide-q-physical-carrier-source-selection: f9559df1 ckm: land CP-product alpha_s estimator
527864cb docs: add review for three-sector dimension-color identity
78eace31 ai-methodology: land canonical per-paper framing paragraph
037aded3 koide: land conditional CKM Vcb bridge support
e05dbd2a gravity: land Lambda spectral tower bridge
338fd21f docs: land Planck source-unit normalization support theorem
2e0ae229 lorentz: land fixed-H_lat kernel closure
f0345539 docs: land CKM Thales alpha-independent ratios theorem
2fc5b523 ckm: land kaon epsilon_K Jarlskog decomposition
f9559df1 ckm: land CP-product alpha_s estimator
a86d1a1f planck: tighten resubmission closure wording
715d9925 planck: prove normalized Gauss mass readout
952d3ce6 planck: land clean source-unit normalization theorem
9d0fbabf dm: land freezeout-bypass support lane and SU(3) obstruction
efa79982 koide: land source-domain no-go synthesis
f237b0d7 lorentz: land Phase 5 kernel closure as derived corollary (v2)
f569517d planck: prove normalized Gauss mass readout
bdfe5e5f planck: land clean source-unit normalization theorem
db330501 ckm: land NLO protected gamma corollary
727d6c49 dm: adversarial review of freeze-out-bypass theorem; fixes F1-F4
7b2531e0 science: package Koide workstream review surface
3faae6d6 docs: add Lorentz boost-covariance review note
d5d3654c lorentz: land boost-covariance theorem packet
b1bb09ba ckm: integrate Thales CP-ratio theorem
30ddf585 planck: integrate area-law quarter no-go lane
654cb77a area-law: land simple-fiber Widom no-go
6e90d030 lorentz: update ACTIVE_REVIEW_QUEUE with Phase 5 closure
43aad166 lorentz: land Phase 5 positive closure of the angular kernel
ee036eab ckm: tighten Bs mixing phase guardrail
dbf3dc7a area-law: land algebraic spectrum entropy no-go
2c3aaaf9 docs+scripts: land bounded quark taste-staircase support
1e1aa10d ckm: integrate B_s mixing phase package
e98d7747 area-law: land primitive-edge entropy selector no-go
f7801086 lorentz: add boost-covariance lane to ACTIVE_REVIEW_QUEUE
6a10a97f lorentz: land 3+1D SO(3,1) boost-covariance theorem
d0c17053 area-law: land multipocket selector no-go
0a579977 docs+scripts: land bounded atomic scaffold lane
0aa82972 ckm: integrate second-row magnitude package
312f41c3 lorentz: land angular kernel underdetermination no-go + Phase 4 decoupling
0a9677da area-law: land simple-fiber Widom no-go
7e6902f8 lorentz: land 1+1D SO(1,1) boost-covariance theorem
d1fb8aee lorentz: land boost-covariance gap audit
b51dc51f ckm: land first-row magnitude identities
b8bd70f8 docs: land hypercharge squared-trace catalog theorem
201ced08 koide: land Q background-zero criterion
29a2b8c9 hypercharge: land squared-trace catalog theorem
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
dcd2be08 Codex worktree snapshot: archive-cleanup
e6f11dee docs: land conditional Planck completion packet
7abab14d Discharge Planck reviewer objections
73e1a92f Integrate Planck closure reductions
8fdca153 docs: package generated geometry reviewer branch
3593efc2 Periodic torus audit batch-1 manual review: 8 false positives + 1 TRUE BUG
e3b2c09a Add periodic 2D torus diagnostics code audit (review-hardening)
aeba1c72 Add emergent-geometry multisize null-control review-hardening note
4599b458 Harden Planck review scope and action-source lane
aed038e1 Close Planck review contract airtight
7ede5166 Add Planck clean closure criterion
e1fb0e91 Add Planck hostile review hardening audits
ec118ec9 Tighten public package entry and validation surfaces
36f1684c Clean public note language across repo
c67de08e Demote review-state language in delicate lane notes
854e8649 Clean and re-map public science package
e9099506 Clean public repo authority surfaces
71e0872f salvage retained science support subset
0009ff9f package: retained science from autonomous-loop session (post-hostile-review)
f38e9fe9 review: Nature-grade hostile audit of 19-branch autonomous-loop session
297f9f81 koide: Q=2/3 attack landscape status index (reviewer navigation)
ffe965c7 Land Koide Q second-order support batch
dd4f0c7d koide a1: clean up the science — separate rigorous PASS from narrative DOC
51e56f40 koide a1: reviewer Q&A — 10 anticipated challenges addressed (10 PASS)
b2192666 docs: strengthen koide q reviewer derivations
7f5889cc docs: add koide q reviewer packet
dfe98943 koide: salvage physical-bridge as candidate support route
3f03f0de koide: land brannen geometry and dirac support addendum
ea6d99a8 koide: package brannen phase lane 2 closure review stack
84da12b5 koide: land axiom-native support batch honestly
56876669 Clean public package surface and remove internal docs
0e43fed5 Tighten public repo entry surfaces
e2dff658 Normalize repo terminology to controlled vocabulary
cea32c63 science(koide-A1): Vectors A and B tested - neither provides clean closure
7ffe68c7 science(koide-A1): iter 14 - S_3 orbit analysis lands at same Isotype Democracy
4df9abb7 Sync publication surfaces with landed scalar-selector status
c710891d science(koide-A1): iter 13 - AS index also lands at Isotype Democracy
870030c2 land scalar selector review package
a9cefc1b science(koide-A1): iter 9 RIGOROUS REVIEW - iter 8 insight RETRACTED
200621a9 koide: salvage april 22 support batch
1f2dd411 docs(koide): final cleanup - update master note runner count + add review_imports README
48aed9d2 docs(koide-A1): iter 14 final status - /loop halted with comprehensive landscape
35471de3 science(koide-A1): import review-branch theorems + 5th failed bridge attempt
7c810fb6 science(koide-A1): A1 = dim(spinor)/dim(Cl+(3)) — cleanest axiom-native form
043de3fc docs: align review package with canonical science state
bd250458 dm: close review-surface selector on recovered packet
0462d9aa reviewer closure loop iter 34: proposed Atlas entry edits for retention landing
83f6de7a reviewer closure loop iter 33: update retention note with iter 32 sign-pinning
e9ac6271 reviewer closure loop iter 32: SIGN-PINNING of η_APS from conjugate-pair structure (9/9)
b6c65818 reviewer closure loop iter 31: comprehensive Koide lane science package
17e83198 reviewer closure loop iter 30: STRESS-TEST of Koide Selector Theorem (12/12)
e33e69ed reviewer closure loop iter 29: canonical retention note for Atlas extension
4af75e94 reviewer closure loop iter 28: END-TO-END RIGOROUS VERIFICATION (15/15)
3ac167e7 reviewer closure loop iter 27: SOLID single-retention proposal closes ALL 3 items (12/12)
05492fea reviewer closure loop iter 26: retention requirement REDUCED to ONE axiom (14/14)
89747877 reviewer closure loop iter 25: BREAKTHROUGH — refined tau Yukawa theorem (13/13)
43353e05 reviewer closure loop iter 24: consolidated 3-item closure proposal document
4b1c18e3 reviewer closure loop iter 23: NEW Charged-Lepton Thermal Yukawa Theorem proposed (11/11)
98173800 reviewer closure loop iter 22: NEW Brannen-APS identification theorem proposed (10/10)
1ccf84bc reviewer closure loop iter 21: honest state summary — diminishing returns without Atlas extension (10/10)
333328ee reviewer closure loop iter 20: v_0 (7/8) double-counting reframed as independent factors (10/10)
7dfa1ea8 reviewer closure loop iter 19: multi-route convergence to rational 2/9 (7/7)
4213ba2e reviewer closure loop iter 18: 3 Koide items consolidated to ONE postulate P (δ = η_APS)
5a29d585 reviewer closure loop iter 17: Bridge B amplitude-vs-spectral unit concern characterized
ed8a7581 reviewer closure loop iter 16: framework-exact η_APS = -2/9 via G-signature formula (12/12)
709ef0a0 reviewer closure loop iter 15: v_0 overall lepton scale narrowed (10/10)
c00a4b12 reviewer closure loop iter 14: observable principle with D=H_sel ruled out as Bridge A source (7/8)
faa6c096 reviewer closure loop iter 13: Bridge A (Q = 2/3) narrowed further (15/15)
1131217f reviewer closure loop iter 12: Brannen-phase Bridge B strong-reading REDUCED to Bridge A (18/18)
738ae0d4 dm: land mapping closeout and split2 support packet
155aaedb reviewer closure loop evening-4-21 final summary: ALL 4 Gate-2 items CLOSED at Nature-grade
d102b059 reviewer closure loop iter 11: current-bank quantitative DM mapping CLOSED at Nature-grade (17/17)
687412c6 reviewer closure loop iter 10: split-2 carrier-side dominance CLOSED at dense-grid + Lipschitz rigor (9/9)
ca429900 reviewer closure loop iter 9: A-BCC axiomatic derivation CLOSED at Nature-grade (14/14)
924439ee reviewer closure loop iter 8: chamber-wide σ_hier = (2,1,0) CLOSED at Nature-grade (10/11)
cc556b53 reviewer closure loop iter 7: Bridge B structural derivation narrowed (5/5)
0f648ce7 reviewer closure loop iter 6: Tr(H²) Casimir attack on N1 (negative, 0/3)
52e324e2 reviewer closure loop iter 5: N1 is the primitive bottleneck (honest Nature-grade verdict)
833f237a reviewer closure loop iter 4: N1 δ·q_+ = Q_Koide narrowed to SELECTOR-quadrature (8/8)
cfd8a85f reviewer closure loop iter 3: Bridge B CLOSED at PDG precision (9/9); N1/N2/N3 added
614b71cf reviewer closure loop iter 2: Bridge A narrowed via multi-principle + γ identity (14/14)
eba83bfd dm: salvage pmns three-identity support proposal
6611ffd4 reviewer closure loop iter 1: audit of afternoon-4-21-proposal vs reviewer items (11/11)
1a7f2e02 pmns I5 angle-triple selector closure — proposal for canonical review
ce980686 docs: reopen Koide bridges on review surfaces
003724b8 docs: clean review package claim surfaces
04d17559 docs: clean canonical review surfaces after Koide closure
305b6e17 koide: finalize morning-4-21 closure on canonical review
96d32fd6 koide morning-4-21: publication-grade cleanup of I1/I2 package
09d07431 koide morning-4-21: publication-grade cleanup of I1/I2 package
a146cc23 koide loop iter 6: I1/I2 reviewer stress-test (35/35)
1a65008f koide: unify reviewer packet to unconditional closure status
99dc9cb6 koide: Round 3 integrated closure - BOTH I1 AND I2/P CLOSE (non-circular)
012d663c koide: land conditional I1/I2 support packet
589d7a96 dm: land honest I5 exact-manifold reduction
ec7b4e94 docs: add review note for remaining koide gaps
4c1a768c science: land 3plus1 Wilson DM support packet
ce1cdd57 dm: land I12 closure and reduce I5 to PMNS angle triple
b8dcf134 docs: close quark provenance review gaps
118347b9 Merge remote-tracking branch 'origin/main' into codex/scalar-selector-cycle2-landing
02963753 koide: land morning route-closure stack
c5b8746c docs: add 3plus1 line law review note
c1347e99 koide: land cycle-2 import closures and no-go notes
1a058d86 charged-lepton: land I2 Brannen phase reduction theorem
b5750b20 feat: Nature-grade cleanup + reviewer-facing package doc for scalar-selector cycle 1
4dbc6b51 docs: open-imports register for scalar-selector cycle 1 + runner cleanup
4ede775e docs: reviewer-facing proof chains for all Tier-1 closures
d284ef3c koide: retire Berry closure route on natural lifts
a8fa9cfb feat: cycle 16 strict-reviewer corrections — PNS, κ measure, BICAC residue
4a7aa854 dm: land PNS attack cascade — A-BCC fully closed in retained framework (cycle 13)
0c4967a2 feat(quark): add shell-normalized LO closure theorem
c32d43b2 dm: land A-BCC Sylvester signature-forcing theorem (cycle 12)
4edb5c9a feat: add DM normalized Schur determinant selector
f317a511 dm: land A-BCC PMNS Non-Singularity conditional theorem (cycle 11)
528df939 docs: land g_bare two-ward closure route
db20faf3 dm: land A-BCC assumptions audit — full no-go on all 5 derivation routes
ed2a62ba docs: add koide circulant review verdict
0c5eb3ee docs: land honest scalar-selector cycle1 review status
eb572506 docs: add scalar-selector cycle1 science review note
daa7b685 docs: add scalar-selector cycle1 science review note
7d9085fe feat: cycle 1-10 final scalar-selector science stack (clean reset)
c02e1aab framework: land reviewed CL3 support and selector-gap packet
9be65b54 docs: cross-branch review feedback, running-mass route, cleanup
90c78a87 docs: package quark route-2 science review stack
20e89b7d docs: package quark route-2 science review stack
1adfbfb6 gauge: land g_bare ward support candidate with honest status
ceca44b6 docs: land selective lepton PMNS integration subset
5eb140f8 charged-lepton: land scale-selector identity and Q=2/3 eigenvalue surface
32e2d8bb docs: weave bounded quark review packet through main surfaces
4c3906a2 Integrate lepton/PMNS work from 12 branches into single review package
de6a472e Add quark science review stack
e62b630d Add quark science review stack
222d1a06 docs: land Cl(3) selector gap investigation note
89e04fda charged-lepton: land Cl(3) selector gap analysis
f3c7aa23 docs(cl3): review pass — fix six substantive errors in embedding theorem docs
367dd75a charged-lepton: apply review cleanups and extend Tr(K_frozen)=0 lemma
58f14e42 docs: add independent review note for lepton mass tower (CONFIRMED, promotable after cleanups)
116534ac docs: add cl3-sm-embedding review note
1cbb91c8 feat(cl3): land Cl(3)→SM embedding theorem with 94/94 algebraic checks
f6659518 feat: land dm lepton support packet
3b020383 dm-leptons: land three new theorems and synthesis note
6f2e66fc atomic: salvage hydrogen-helium companion packet
4128417d docs: archive operational review backlog surfaces
b5708019 feat: land g_bare structural normalization support
984fc862 chore: salvage g_bare science for landing
02210876 docs: land graviton spectral identity
f124537d cosmology: review pass on graviton-mass identity theorem note
814f70f3 cosmology: review pass on graviton-mass identity theorem note
12f14a6a docs: normalize historical runner links
430211f7 docs: retire five redesign-only audit items
7e141142 docs: salvage PF route history
86fcf616 feat: land CL3 support-route minimality packet
55fee87c feat: land CL3 support-route minimality packet
d423f8ad charged-lepton: land koide review support stack
7e9aae2c docs(review): refresh PF review for latest tip
8afbd4c5 Wire PF review entrypoint into verifier
48c8e0ed docs(review): refresh PF science review
0b011c16 docs: refresh dark-energy EOS review after self-review fixes
c3bf2b66 dm: land retained P3 Sylvester local theorem
e4ca8c67 cosmology: review pass on dark-energy EOS retained-corollary note
15b99832 docs: add dark-energy EOS review packet
8d27f7ac Path A Sylvester theorem: address first-round reviewer findings
2da8cf79 docs: add koide charged-lepton review packet
d5b3c67e docs: add review for path-a sylvester theorem
1fd33ca1 dm: land science-only selector obstruction packet
db8df07c Koide charged-lepton review packet — derived-from-main clean package
29fb7282 Add PF review status note
f4e81b2f dm: add reviewed Wilson direct-descendant science stack
00677a06 Koide review packet and frozen-bank reduction
362243e6 docs: add PF science review note
c0fd45b0 docs: address first-round reviewer findings on YT retention submission
82f124bd docs: land YT UV-to-IR transport retention program
0d9e1306 docs(review): update CL3 review for forcing v3
76ddff5a dm: add reviewed Wilson direct-descendant science stack
98449dea docs(review): update PF review for current tip
6d2cf065 Fix PF review-note consistency
5606a6dc docs(review): update CL3 review for forcing v2
922692cd docs(review): update CL3 forcing-theorem review
ff607ed8 docs(review): update CL3 review for Recipe-R closure claim
cf918121 docs: approve YT retention review
d5e1610c docs(review): add PF science review
7ce36790 docs: refresh cl3 minimality review note
cd25be85 docs: refresh cl3 retained review guidance
803fa272 docs: add retained upgrade path for cl3 review
61f0993a docs: refresh cl3 minimality review note
cd8f5b49 Native-gauge scope theorem: address reviewer blocker for retention
78ef9deb docs: refresh cl3 minimality review note
c7033614 docs: refresh cl3 minimality review status
ee9d6e63 docs: update cl3 minimality review note
84102d5b Address review: dependency table + real four-generation no-go theorem
d0424ef7 docs: refresh cl3 minimality review note
1cc27721 Add CL3 minimality review note
471ddcf7 docs: retire stale decoherence sweep blocker
946f9139 docs: address first-round reviewer findings on YT retention submission
06a2ee76 docs: refresh YT retention review note
0c47dc12 docs: retire branch-entanglement GHZ review blocker
2ab4fb34 docs: add YT retention review note
6700b7ae docs: retire stale Wilson Newton review blocker
108c013b docs: land YT UV-to-IR transport retention program
c9edde73 docs: finish repo-wide vocabulary cleanup
8dcfc86e docs: retire bmv overclaim review item
89935c56 docs: retire old area-law evidence lane
093a46f2 docs: retire old staggered two-body review item
668c16ce review: demote symmetrized DAG claims
3851f7a5 review: retire resolved self-consistency control finding
2679fe30 review: rerun-correct two-field wave family audit
66010112 review: resolve retarded probe R9 scoring finding
879a7117 cleanup(ckm-dual): back P-AT out of live package — branch-local proposal only
8ca2eace review: update angry-chatelet findings for P-AT proposal
e762dc36 docs: refresh cl3 minimality review note
e2f93e0f Tighten BH Widom evidence routing
2f464afd fix(ckm-dual): address review — three-layer status with proposed P-AT primitive
90d8d989 Add BH Widom review note
2ec7047e feat(bh-entropy): land retained RT-ratio Widom no-go theorem
07717ea8 docs: refresh cl3 retained review guidance
93eb5acf docs: add retained upgrade path for cl3 review
c8a59d7e docs: refresh cl3 minimality review note
e838b86a Native-gauge scope theorem: address reviewer blocker for retention
66599580 docs: refresh cl3 minimality review note
398fb076 docs: refresh cl3 minimality review status
3d07a891 docs: update cl3 minimality review note
b705768a Address review: dependency table + real four-generation no-go theorem
6ec96ace docs: refresh cl3 minimality review note
4eb2178f Add CL3 minimality review note
b86955d8 feat(bh-entropy): land retained RT-ratio Widom no-go theorem
4e517dae Add review note for CKM dual bridge branch
5101eafd Update YT authority lane after Ward landing
123539f1 docs: drop charged-lepton review note from main
de294c49 Merge branch 'claude/charged-lepton-closure-review'
1d0f818c y_t proposal v2: honest accounting after first reviewer pass
583fdbc5 Refresh G1 review after 87ec25fb check
1b2fc235 docs: refresh charged-lepton review status
87ec25fb Load-bearing science review: scope-accurate status, Z_3-trichotomy primary route
270d29e1 Address remaining review blockers: single uniqueness story, unified 518 count
da7016bd docs: refresh charged-lepton review status
04fbf960 Refresh G1 review after current check
3dc46cb4 Address review.md blockers 1-4 for charged-lepton closure package
c01521a1 Notes deep-review: fix Paths/Agents residuals, broken cross-ref, awkward phrasings
374a56a9 Add charged-lepton review findings
5c500d28 Update G1 review note after re-review
7f6abe4a Polish theorem notes: clean titles, fix sed-aftermath phrasing
ce945cd6 Add G1 review note
9b756c76 Charged-lepton mass hierarchy + Koide's relation — review package
14ff9eac Add CL3 minimality review note
6cb88b80 Integrate G1 Physicist J: perturbative-uniqueness theorem (fixes CRITICAL 1+2)
b2899d83 G1 Physicist-J: perturbative-scale uniqueness tightening of PMNS-as-f(H) closure
ce9cb66b Integrate G1 Physicist K: theta_23 upper-octant retained prediction (fixes SERIOUS 3)
d393dc99 Integrate G1 Physicist L: Z_3 trichotomy q_H=0 U_e=I route (fixes MEDIUM 4)
73958957 G1 inline tightening: delta_CP reframe + adversarial-review cross-refs
0e166f09 Tighten plaquette evidence boundaries
ca323a87 Land DM parity-compatible observable selector route theorem
65326822 Merge main into g1-complete: integrate codex DM/PMNS/plaquette parallel work
3ad3b098 Add G1 omnibus closure review note
247864f9 Integrate G1 physicist H: PMNS-as-f(H) CLOSURE theorem (G1 CLOSED)
1d941938 Integrate G1 physicist I: bifundamental-invariance obstruction theorem
94a951d1 Integrate G1 physicist G: microscopic axiom-level impossibility theorem
d9fd23ad Integrate G1 physicist F: Frobenius uniqueness obstruction + quartic-isotropy
22f05859 Integrate G1 physicist E: observable-bank exhaustion theorem
ca1740d8 Integrate G1 parity-mixing selector law narrower-gap
99ddc680 Integrate G1 physics-validation: eta/eta_obs chamber-blindness theorem
b3f3499d Land accepted DM thermal support stack and clean package claims
08be2ba4 Integrate claude/g1-path-c-holonomy
81bc1c4a Integrate claude/g1-path-b-z3-cubic-selector
dccf8244 Integrate claude/g1-path-a-information-geometric
eaeae7c1 Integrate G1 Schur-baseline partial closure
6972f719 Update DM review summaries for selector closeout packet
445aad99 Add DM thermal hardening review stack
49ba432f Land flavor representation support packet
1bd22cf5 Expand derivation atlas with reviewed candidate tools
eeb42790 Refocus selector review package honestly
d3f92249 Add selector closeout review feedback
ee3181fa fix(bell): address reviewer P0/P1 — stale 2D numbers and taste gap
ffd102cd Add selector closeout review feedback
db89b872 Add derivation-atlas candidate list for reviewer sweep
bf79dc7a Land scalar-baseline DM quadratic diagnostic
d30105e1 Drop historical note churn from leptogenesis review branch
ff502e98 chore: remove dimension selection note from Bell review branch
f6dfb70e fix(bell): audit cleanup — remove dead code, fix overclaims, honest boundaries
cd5dd5dd fix(bell): complete Bell inequality derivation — four clean surfaces
68f33330 Land plaquette analytic support stack
c0481ac4 Land plaquette analytic support stack
02789b6b Land ordered-lattice matter lane status
6eb73456 Land plaquette same-surface support stack
3aca62f3 Land partial neutrino boundary support packet
fe782707 Land taste-scalar isotropy support theorem
50845b0b Tighten PMNS branch-count wording after certified theorem
1c9b5318 Reconcile PMNS review surface with certified selector theorem
1523ca35 Add DM closure review package
e416140b Tighten PMNS branch-count wording after certified theorem
ee6bcda5 Reconcile PMNS review surface with certified selector theorem
6b979bea Add DM closure review package
39027463 Close active transport source and clean passive kernel law
f3776f00 Package retained neutrino lanes for review
853d14ba Tighten physical-lattice rigor accounting
66e49b85 refactor(cosmology): tighten baryogenesis scalar matching boundary
d7cf51f6 refactor(generation): tighten review-ready theorem package
f431054b refactor(generation): tighten review-ready theorem package
8f64e6cb refactor(generation): tighten observable theorem boundary
148a56fd Tighten strong CP closure accounting
9d14a2c5 Tighten front door and reviewer path
45473ea2 Add review for plaquette derivation package
3091544d Tighten arXiv-first manuscript front door
361014d0 Promote YT explicit-systematic package and clean live path
fe34ab91 chore(docs): clean YT package note whitespace
9d8cc7dc docs(qg): mark continuum claim cleanup resolved
e2090393 Tighten gravity and QG claim boundary
06aab9ee Salvage strong CP support cleanup
512cce20 Tighten Higgs/top package surfaces
0a697c5b Clean up EW and alpha_s authority paths
38d810d0 Tighten CKM package wording and placement
e8fcfda7 Land individual companion lanes and tighten package notes
fad9f48d docs: session deliverables — 5 lanes, adversarial-tightened
4810429a fix(confinement): tighten after adversarial review
1e67a1f0 fix(strong-cp): tighten after adversarial review
b67af952 fix(lorentz): tighten claims after adversarial review
6b994330 docs(arxiv): tighten manuscript framing and prose
828d757c docs(package): land full 3-loop Higgs authority on main
3cdf5d55 docs(yt-higgs): tighten bounded authority surface
ea8a74d3 docs(yt-higgs): tighten bounded authority surface
383f0935 docs(ckm): tighten front-door package hygiene
```

## 6. All-time Claude-attributed commits (full list, verbatim)

`git log --all --pretty="%an %h %s" | grep "^Claude "`

**Total Claude-attributed commits:** 46

```text
Claude 8d2f8c5f docs+scripts: open atomic hydrogen/helium scaffold lane
Claude a3bae980 loop setup: axiom-native overnight derivation scaffolding
Claude dd4f0c7d koide a1: clean up the science — separate rigorous PASS from narrative DOC
Claude b75f6910 koide a1: phase 2 track summary — 34 runners, 276/276 PASS, retained-grade
Claude 51e56f40 koide a1: reviewer Q&A — 10 anticipated challenges addressed (10 PASS)
Claude d577a8bc koide a1: upgrade theorem note to retained-grade; phase 2 summary
Claude 6a262285 koide a1: master closure updated — 33 runners, 266/266 PASS
Claude 1449b473 koide a1: Higgs-side consistency — both legs satisfy (A1*) (9 PASS)
Claude 5e3c45ae koide a1: precision budget — PDG within few σ of Q=2/3 prediction (5 PASS)
Claude 10085e61 koide a1: y_tau composition — SUM drives scale, DIFF drives cone (5 PASS)
Claude 5d2fdaa0 koide a1: stress test — 3-gen perturbation + corner cases (11 PASS)
Claude d7224021 koide a1: Brannen Berry — Ω = 4/d² ⟹ γ = 2/9; 3 closure routes enumerated (6 PASS)
Claude 7a9eb1ca koide a1: Brannen P probe — Wilson d²=9 winding, 2/9 uniquely at d=3 (6 PASS)
Claude 42da4ee8 koide a1: mu-invariance — cone closure RG-invariant at 1-loop (5 PASS)
Claude 692e8c54 koide a1: c-independence — cone closure ratio-tight across 6 orders of magnitude (11 PASS)
Claude c5fe9a32 koide a1: P2.promotion — (P2) upgraded to retained-grade; A1 cone algebraic-theorem-grade (5 PASS)
Claude 1c945e66 koide a1: P2.same-topology — common-c theorem at 1-loop (6 PASS)
Claude e4b7a598 koide a1: P2.cyclic — cyclic Phi on hw=1, unit-mag E eigenvalues (8 PASS)
Claude e510cf3b koide a1: P2.factorization — linear-Casimir accounting on sqrt-mass (7 PASS)
Claude ae9dec11 koide a1: P1.promotion — (P1) upgraded to retained-grade (6 PASS)
Claude e0ca1607 koide a1: P1.blindness — K_loop generation-blind by MS-bar + Ward (6 PASS)
Claude a5ef3336 koide a1: P1.rainbow — 1-loop rainbow enumeration, shared topology (8 PASS)
Claude 62b154eb koide a1: P1.formal — Ward-identity derivation of (P1) at schema grade (10 PASS)
Claude 49461e2d koide a1: track summary — 17 runners, 152/152 PASS, schema-grade closure
Claude 9051b212 koide a1: master closure runner — 17 step runners, 152/152 PASS
Claude 31a3e8d9 koide a1: surface promotion in KOIDE_A1_DERIVATION_STATUS_NOTE (Route F now schema-grade)
Claude 6e3ed580 koide a1: promote to formal theorem note; closure schema documented
Claude 5f396320 koide a1: X7 — consistency w/ existing yukawa_casimir_identity runner (6 PASS)
Claude debcf16c koide a1: X6 — Brannen corollary δ=Q/d=2/9, P residual flagged (7 PASS)
Claude 0179597a koide a1: X5 — no-go evasion audit, all 9 retained no-gos avoided (10 PASS)
Claude 13a34215 koide a1: X4 — compose with hw=1 Theorem 1, end-to-end chain (7 PASS)
Claude a4690b97 koide a1: X3 — symbolic iff A1 ⟺ (3Y²=T(T+1)) via sympy (11 PASS)
Claude bd2f81f6 koide a1: X2 — perturbation sensitivity, ∂r/∂Y=-3/2, ∂r/∂T=1 (5 PASS)
Claude 855a6aec koide a1: X1 — uniqueness sweep, A1* admits no other rational (T,Y) (4 PASS)
Claude ab866c72 koide a1: O3.c — same-c synthesis ⟹ Q = 2/3, lemma stated (9 PASS)
Claude a126f22f koide a1: O3.b — same K_loop on diag/off-diag, common c (7 PASS)
Claude 4f67c7c5 koide a1: O3.a — E-isotype = C_W± = T(T+1)-T_3^2; only W± carries E (8 PASS)
Claude f209ef77 koide a1: O2.c — pin proportionality constant c (6 PASS); O2 closed
Claude 23155a65 koide a1: O2.b — trivial-character weight inherits Casimir SUM (6 PASS)
Claude ffb6dcbd koide a1: O2.a — gauge-by-gauge SUM enumeration; clarify SUM=1 not unique to {L,H} (15 PASS)
Claude ec12c6c4 koide a1: O1.c — mass-matrix Frobenius split aligns with hw=1 A_1/E (10 PASS)
Claude 9a2e0007 koide a1: O1.b — hw=1 S_3-irrep alignment matches C_3 Fourier (17 PASS)
Claude 9118acd7 koide a1: O1.a — C_3 Plancherel + A_1/E projector split (12 PASS)
Claude 206aea27 koide a1: scaffold casimir-difference lemma derivation track
Claude 18d9d5ff docs+scripts: open atomic hydrogen/helium scaffold lane
Claude 28a65665 docs: update interest scores on latest main
```

## 7. Full author histogram (all branches, all time)

`git log --all --pretty="%an" | sort | uniq -c | sort -nr`

```text
3834 jonathonreilly
 526 Jon Bridger Apps
  84 Codex Autoresearch
  57 Jonathon Reilly
  46 Claude
   1 Jon Reilly
```

Three of the top four are human-name variants of the same author
(`jonathonreilly`, `Jon Bridger Apps`, `Jonathon Reilly`, `Jon Reilly`).
The two AI identities are `Codex Autoresearch` (84 commits) and `Claude` (46
commits). At the commit *attribution* level, ~3% of commits are AI-attributed.
This severely undercounts AI *origination*: most commits authored by the
human identities are squashed landings of AI-produced content. The
attribution histogram is included here as raw signal, not as a
contribution-fraction estimate.

## 8. Total commit count (project lifetime)

`git log --since="2026-03-13" --pretty="%h" | wc -l`

```text
    2664
```

Project initial commit: 2026-03-13 (first 'Initial commit' on the day the
repo was created). Capture date: 2026-04-25. Active duration: 43 days.
Implied average commit rate: ~62 commits/day across the active window.
