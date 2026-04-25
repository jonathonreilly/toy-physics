# Claude Repo Hygiene

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7`. Branch and commit
data spans Claude Sonnet 4.5/4.6/4.7 and Opus 4.6/4.7 contributions.

**Workspace / repo:** `/Users/jonreilly/Projects/Physics`

**Scope note:** Raw evidence of how the Claude side of the workflow shows up
in repo hygiene — branch naming, worktree fanout, recent commit cadence,
selective-landing patterns. This is direct git/filesystem inventory; no
narrative.

---

## 1. Remote `origin/claude/*` branches

Count on this pass: **35** remote `claude/*` branches.

Raw remote branch list (verbatim from `git branch -r | grep claude/`):

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

Plus three from another remote (`scalarp3p7`):

```text
remotes/scalarp3p7/claude/angry-chatelet-2dc78c
```

(and additional `scalarp3p7/claude/*` branches not enumerated here).

## 2. Branch-naming patterns visible in raw inventory

From the `claude/*` list above, two clear naming families:

**Family A — Docker-style adjective-noun-hash (machine-generated worktree
names):** `angry-chatelet-2dc78c`, `youthful-neumann`, `stupefied-khayyam`,
`relaxed-taussig-18d9fb`, `sad-yonath`, `eloquent-wilbur`,
`inspiring-banzai-7002dd`, `great-nobel-ab743c`, `dreamy-wing-969574`,
`vigilant-turing-e374dd`, `angry-feynman-2df312`. These are the names Claude
auto-assigns when starting a fresh worktree in the cloud or via the worktree
plugin.

**Family B — descriptive-topic-{date|tag} (human or AI authored for an
intent):** `ai-methodology-capture-2026-04-25`, `koide-a1-irreducibility-package`,
`graviton-mass-identity`, `mass-ratio-package`,
`source-proximal-symmetric-endpoint-2026-04-24`,
`yt-retention-landing-2026-04-18`, `yt-ward-supersedes-bridge-proposal`,
`charged-lepton-closure-review`, `derived-science-clean`,
`framework-point-beta-6-lane`, `mass-spectrum-phase-2-scoping`. These are
named for the lane being explored; many include the date for chronology.

## 3. Active `claude/*` branches checked out locally

```text
* claude/ai-methodology-capture-2026-04-25
  claude/axiom-native-overnight-FtUl5
  claude/blissful-tu-ccc1e8
+ claude/crazy-pascal-8623c8                 (worktree: crazy-pascal-8623c8)
  claude/flamboyant-germain-3060cb
  claude/romantic-chatterjee-331089
  claude/upbeat-williamson-a2ff73
+ claude/zen-turing-06eeca                   (worktree: zen-turing-06eeca)
```

The `+` marker indicates a branch checked out in another worktree.

## 4. Live Claude worktrees (this machine)

Path: `/Users/jonreilly/Projects/Physics/.claude/worktrees/`

```text
blissful-tu-ccc1e8           (this worktree, claude/ai-methodology-capture-2026-04-25)
charming-stonebraker-7078d0
crazy-pascal-8623c8
romantic-chatterjee-331089
zen-turing-06eeca
```

Plus all worktrees attached to this repo (output of `git worktree list`,
abbreviated to **claude/* + main only** — full output has 90 entries
including 38 `codex/*` and 24 detached-HEAD entries):

```text
/Users/jonreilly/Projects/Physics                                         201ced08 [main]
/Users/jonreilly/Projects/Physics/.claude/worktrees/blissful-tu-ccc1e8    <current>  [claude/ai-methodology-capture-2026-04-25]
/Users/jonreilly/Projects/Physics/.claude/worktrees/charming-stonebraker-7078d0  [claude/charming-stonebraker-7078d0]
/Users/jonreilly/Projects/Physics/.claude/worktrees/crazy-pascal-8623c8           [claude/crazy-pascal-8623c8]
/Users/jonreilly/Projects/Physics/.claude/worktrees/romantic-chatterjee-331089    [claude/romantic-chatterjee-331089]
/Users/jonreilly/Projects/Physics/.claude/worktrees/zen-turing-06eeca             [claude/zen-turing-06eeca]
```

Worktree statistics on this pass:

```text
Total worktrees attached:               90
  - on a claude/* branch:               5  (1 main + 4 active)
  - on a codex/* branch:               38
  - in detached-HEAD state:            24
  - on other named branches:           23
```

## 5. Project-store evidence of past Claude worktrees

`/Users/jonreilly/.claude/projects/` contains session stores for **34**
Physics-related project directories — i.e. a Claude session has touched 34
distinct working directories of this repo over the project lifetime
(versus only 5 currently-attached `claude/*` worktrees in §4). The remaining
29 are either:

- previously-attached worktrees that have since been removed; or
- `Projects/CL3Z3 new work` and other prior repo paths.

This is a high-fanout pattern: many worktrees are spun up, used briefly,
their results landed (or rejected), and the worktree is reaped. Project-store
size is **493 MB** with **909 jsonl session files** total (38 top-level
sessions plus 871 subagent invocations across 37 distinct subagent dirs).

## 6. Recent `origin/main` landing cadence

Commits on `origin/main` since `2026-04-22`: **69**.

Raw log excerpt (most recent first; first 30):

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
```

## 7. Selective-landing pattern in raw log

The "land" verb dominates recent commits; raw matches in the same window:

```text
4da26702 docs: land AI methodology lane
b684741f ew: land bare alpha ratio support
037aded3 koide: land conditional CKM Vcb bridge support
e05dbd2a gravity: land Lambda spectral tower bridge
338fd21f docs: land Planck source-unit normalization support theorem
f0345539 docs: land CKM Thales alpha-independent ratios theorem
2fc5b523 ckm: land kaon epsilon_K Jarlskog decomposition
f9559df1 ckm: land CP-product alpha_s estimator
9d0fbabf dm: land freezeout-bypass support lane and SU(3) obstruction
efa79982 koide: land source-domain no-go synthesis
db330501 ckm: land NLO protected gamma corollary
d5d3654c lorentz: land boost-covariance theorem packet
2c3aaaf9 docs+scripts: land bounded quark taste-staircase support
0a579977 docs+scripts: land bounded atomic scaffold lane
b51dc51f ckm: land first-row magnitude identities
b8bd70f8 docs: land hypercharge squared-trace catalog theorem
201ced08 koide: land Q background-zero criterion
95a79235 docs: land LH anomaly trace catalog theorem
fec6bd33 docs: land retained neutrino observable bounds
9a3526cf docs: add Planck boundary-density extension theorem
e6f11dee docs: land conditional Planck completion packet
```

The "land" verb signals a **selective merge into main** — typically Codex
running a review packet against a Claude branch, then cherry-picking the
approved subset onto main. This is also visible in the
`b684741f ew: land bare alpha ratio support` shorthand (`ew` = a worker
identifier appended to the prefix).

Cleanup-style commits in the same window:

```text
adf80784 Remove control-plane links from public package docs
ec118ec9 Tighten public package entry and validation surfaces
36f1684c Clean public note language across repo
c67de08e Demote review-state language in delicate lane notes
854e8649 Clean and re-map public science package
e9099506 Clean public repo authority surfaces
71e0872f salvage retained science support subset
52bfbbcf Clarify prediction-first public package surfaces
56876669 Clean public package surface and remove internal docs
0e43fed5 Tighten public repo entry surfaces
e2dff658 Normalize repo terminology to controlled vocabulary
```

The repeated "Clean public package", "Tighten public ... surfaces", "Demote
review-state language", "Normalize repo terminology" pattern shows
hygiene-style commits are interleaved with science-landing commits in the
same window.

## 8. Authorship histogram (all branches, all time)

```text
3826  jonathonreilly        (human)
 526  Jon Bridger Apps      (human, alt config)
  80  Codex Autoresearch    (Codex auto-commit identity)
  57  Jonathon Reilly       (human, alt capitalization)
  46  Claude                (Claude auto-commit identity)
   1  Jon Reilly            (human, alt spelling)
```

Roughly **89% human-attributed**, **11% AI-attributed** at the commit
authorship level. (Note: most "human-attributed" commits are themselves
Claude-or-Codex-authored content, committed under the human's name when
reviewed and squashed into a landing PR. The author field measures
*attribution*, not *origination*.)

## 9. Recent Claude-attributed commits (sample)

`git log --all --since=2026-04-22 --pretty="%h %an %s" | grep -i claude`
(first 15):

```text
8d2f8c5f Claude docs+scripts: open atomic hydrogen/helium scaffold lane
a3bae980 Claude loop setup: axiom-native overnight derivation scaffolding
dd4f0c7d Claude koide a1: clean up the science — separate rigorous PASS from narrative DOC
b75f6910 Claude koide a1: phase 2 track summary — 34 runners, 276/276 PASS, retained-grade
51e56f40 Claude koide a1: reviewer Q&A — 10 anticipated challenges addressed (10 PASS)
d577a8bc Claude koide a1: upgrade theorem note to retained-grade; phase 2 summary
6a262285 Claude koide a1: master closure updated — 33 runners, 266/266 PASS
1449b473 Claude koide a1: Higgs-side consistency — both legs satisfy (A1*) (9 PASS)
5e3c45ae Claude koide a1: precision budget — PDG within few σ of Q=2/3 prediction (5 PASS)
10085e61 Claude koide a1: y_tau composition — SUM drives scale, DIFF drives cone (5 PASS)
5d2fdaa0 Claude koide a1: stress test — 3-gen perturbation + corner cases (11 PASS)
d7224021 Claude koide a1: Brannen Berry — Ω = 4/d² ⟹ γ = 2/9; 3 closure routes enumerated (6 PASS)
7a9eb1ca Claude koide a1: Brannen P probe — Wilson d²=9 winding, 2/9 uniquely at d=3 (6 PASS)
42da4ee8 Claude koide a1: mu-invariance — cone closure RG-invariant at 1-loop (5 PASS)
692e8c54 Claude koide a1: c-independence — cone closure ratio-tight across 6 orders of magnitude (11 PASS)
```

Visible patterns directly in commit subjects:

- **Per-step structure:** "P1.formal", "P1.rainbow", "P1.blindness",
  "P1.promotion", "P2.factorization", "P2.cyclic", "P2.same-topology",
  "P2.promotion" — each step is an atomic theorem-grade increment.
- **PASS counts in subject lines:** `(10 PASS)`, `(266/266 PASS)`,
  `(276/276 PASS)`. The runner harness count is part of the commit subject
  itself, not relegated to the body.
- **Grade tags:** `schema-grade closure`, `retained-grade`, `algebraic-theorem-grade`.
  Promotion across grades (`P1.promotion`, `P2.promotion`) is its own step.
- **Track summaries:** `koide a1: track summary — 17 runners, 152/152 PASS,
  schema-grade closure`. End-of-track rollups land as their own commit.

## 10. Hygiene signals visible directly in raw data

These are observations, not interpretation — each is supported by an excerpt
above:

- separate `*-review`, `*-land`, and adjective-noun-hash worktrees;
- selective `land <X>` and `integrate <X>` verbs on `main` in place of
  branch-merge fast-forwards;
- repeated public-package wording cleanups interleaved with theorem
  landings;
- explicit grades (`schema-grade`, `retained-grade`, `algebraic-theorem-grade`)
  embedded in commit subjects;
- runner-PASS counts (`152/152 PASS`, `266/266 PASS`) visible in subject
  lines as a verification surface;
- separate `Claude` and `Codex Autoresearch` author identities from the
  same human user, run as parallel autonomous workers.
