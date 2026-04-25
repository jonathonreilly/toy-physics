# Codex Desktop Review And Repo Hygiene - 2026-04-25

**Capture date:** 2026-04-25

**Tool / model / machine context:** Codex desktop app; local session turn
context records `model: gpt-5.5`, host `Jonathons-Mac-mini.local`, user path
`/Users/jonBridger`.

**Workspace / repo:** `/Users/jonBridger/CI3Z2 Main`;
remote `https://github.com/jonathonreilly/cl3-lattice-framework.git`.

**Scope note:** raw branch/worktree/review-hygiene evidence for the
methodology archive. This is not synthesis and not an endorsement of any
physics claim.

---

## 1. Remote Branch Inventory

Counts after `git fetch origin --prune`:

```text
origin/claude/* branches: 32
origin/codex/* branches: 59
```

Raw `origin/claude/*` list:

```text
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
```

Raw `origin/codex/*` list:

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

## 2. Worktree Inventory

Raw counts from `git worktree list`:

```text
total worktrees listed: 194
worktrees on codex/* branches: 47
worktrees on claude/* branches: 27
```

Representative Codex worktree paths observed:

```text
/private/tmp/ci3z2-pf-review                                                8afbd4c5 [codex/pf-science-review-2026-04-18] prunable
/Users/jonBridger/CI3Z2-koide-full-workstream-science-20260425              7b2531e0 [codex/koide-full-workstream-science-2026-04-25]
/Users/jonBridger/CI3Z2-koide-q-science-review                              42600308 [codex/koide-q-source-domain-science-2026-04-25]
/Users/jonBridger/CI3Z2-planck-boundary-action-closure-20260425             00c1f7a2 [codex/planck-source-unit-resubmission-clean-2026-04-25]
/Users/jonBridger/Toy Physics-ckm-package-review                            48719613 [codex/ckm-full-package-review]
/Users/jonBridger/Toy Physics-dm-science-reviewed                           b1f98a96 [codex/dm-science-reviewed-2026-04-17]
/Users/jonBridger/Toy Physics-neutrino-main-derived-review                  85a3d8ec [codex/neutrino-science-main-derived-2026-04-16]
```

Representative Claude worktree paths observed:

```text
/Users/jonBridger/CI3Z2 Main                                                f3223abd [claude/source-proximal-symmetric-endpoint-2026-04-24]
/Users/jonBridger/Toy Physics/.claude/worktrees/g1-rebuild                  cce78fab [claude/g1-complete]
/Users/jonBridger/Toy Physics/.claude/worktrees/quizzical-shockley-537438   6eddc6f4 [claude/ai-methodology-capture-2026-04-25]
/Users/jonBridger/Toy Physics/.claude/worktrees/mass-ratio-package          7f869e3f [claude/mass-ratio-package]
/Users/jonBridger/Toy Physics/.claude/worktrees/taste-isotropy              8181d5e6 [claude/taste-scalar-isotropy]
```

## 3. Review Packet Evidence

Raw `review.md` search output from `/private/tmp` and `/Users/jonBridger`
during this capture:

```text
/Users/jonBridger/Toy Physics-p-derived-science-review/review.md
/Users/jonBridger/Toy Physics/.claude/worktrees/g1-rebuild/review.md
/Users/jonBridger/Toy Physics/.claude/worktrees/agent-aa8b9ba2/review.md
/Users/jonBridger/Toy Physics/review.md
/Users/jonBridger/Toy Physics-p-derivation-review/review.md
/Users/jonBridger/.codex/.tmp/plugins/plugins/cloudflare/skills/workers-best-practices/references/review.md
/Users/jonBridger/Toy Physics-dm/review.md
```

The plugin-path `review.md` is not project science evidence, but it is included
because the raw command output returned it.

## 4. Recent Main Landing Cadence

Count:

```text
git log --since='2026-04-24 00:00' --oneline origin/main | wc -l
      58
```

Raw recent log excerpt:

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
```

## 5. Selective Landing Evidence From This Capture

The remote kickoff branch carried only the instruction file:

```text
A       RAW_METHODOLOGY_DUMP_INSTRUCTION.md
```

The methodology archive branch carried raw files plus branch-local surfaces:

```text
raw annex files: docs/ai_methodology/raw/*.md
branch-local note: docs/AI_METHODOLOGY_NOTE_2026-04-25.md
branch-local review: review.md
```

This landing intentionally selected only:

```text
docs/ai_methodology/raw/
docs/ai_methodology/README.md
docs/AI_METHODOLOGY_NOTE_2026-04-25.md
```

The README and top-level note changes are index/scope updates so the new raw
annex is discoverable and the previous "not on main" language is no longer
false. The remote instruction file and branch-local `review.md` were not
landed as top-level main surfaces.
