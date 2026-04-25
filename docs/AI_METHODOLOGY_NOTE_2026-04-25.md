# AI Methodology Note — Cl(3)/Z³ Framework

**Branch:** `claude/ai-methodology-capture-2026-04-25` (off `origin/main` at `9d0fbabf`)
**Date:** 2026-04-25
**Status:** RAW INFO CAPTURE — to be cleaned, groomed, and organized later
**Scope:** Claude/Anthropic interaction history only on this pass. Codex/OpenAI history will be added in a later pass. Other tools (Gemini, etc.) will be added if used.

This note is the seed file for the AI-methodology paper that frames the Cl(3)/Z³ retained content as a case study in AI-assisted theoretical physics. The objective on this pass is **information capture, not synthesis**. Subsequent passes will compress, organize, and shape into a publishable methodology paper.

---

## 1. Headline Statistics (as of 2026-04-25)

### 1.1 Project timeline

- **Initial commit:** 2026-03-13 14:10:05 EDT (`7a5f1dca` "Initial commit")
- **Current main tip:** `9d0fbabf` (2026-04-25)
- **Active duration:** ~6 weeks (43 days)
- **Total commits on main:** 2,658
- **Average commit rate:** ~62 commits/day across the active window
- **Recent peak day:** 2026-04-24 → 2026-04-25 = 46 commits with ~30 new theorems in 24 hours

### 1.2 Repository state

- **Markdown documents (`docs/`):** 1,454 (.md files in `docs/` and subdirectories)
- **Top-level docs (`docs/*.md`):** 1,379
- **Python scripts (`scripts/`):** 2,089
- **Frontier runner scripts (`scripts/frontier_*.py`):** TBD — to be enumerated in repo audit pass
- **Total git LFS objects, output JSONs, log files:** TBD

### 1.3 Claude session activity (top-level interactions only)

| Session ID | User prompts | Lines | File size | Last modified |
|---|---|---|---|---|
| `04c820e1-77cd-416f-8917-21767de255fd` | 589 | 5,708 | 16.7 MB | 2026-04-14 |
| `855ddec4-8a61-4b04-8c8f-cbb32f2cd422` | 220 | 1,690 | 7.1 MB | 2026-04-15 |
| `67759a49-0b85-4460-86fd-ddf608bae7ff` | 53 | 588 | 2.0 MB | 2026-04-16 |
| `0729b510-1268-452e-bb49-24ce9cebfdb7` | 1 | 43 | 286 KB | 2026-04-14 |
| `586a2dfb-e949-4b30-a5ad-681b371800dd` | 2 | 23 | 126 KB | 2026-04-14 |
| `93f278f6-1fa3-408c-9c6a-65a110f60d3d` | 2 | 14 | 44 KB | 2026-04-15 |
| **TOTAL (top-level Claude)** | **867** | **8,066** | **~26.3 MB** | — |
| **Current session (in progress)** | TBD | — | — | 2026-04-25 |

### 1.4 Worktree / agent activity (subagent invocations)

- **Top-level Claude project directories:** 26 (1 main + 25 worktrees)
- **Total Claude session jsonl files (incl. subagent invocations):** 751
- **Subagent invocation jsonl files:** ~745 across worktrees
- **Total Claude session storage:** 284 MB

### 1.5 Codex/OpenAI activity

To be added on next pass. Expected scope based on memory file: Codex runs review on `codex/review-active` branch and `codex/*` branches. The repo has dozens of `codex/*` branch names visible in git history.

---

## 2. AI Toolchain Inventory

### 2.1 Primary tools used

- **Claude (Anthropic Sonnet 4.5 / Sonnet 4.7):** primary theorem-production / derivation / write-up surface. Session history captured in `~/.claude/projects/-Users-jonBridger-Toy-Physics/`.
- **Codex (OpenAI):** adversarial review, independent re-derivation, branch-wise verification. Visible via `codex/*` branch names on `origin`.
- **Other:** TBD — to be enumerated on next pass.

### 2.2 Workflow tooling — custom slash commands

Located in `/Users/jonBridger/Toy Physics/.claude/commands/`. These are user-defined research-process commands that scaffold the AI workflow:

| Command | Purpose (inferred from filename) |
|---|---|
| `/analyze` | Result analysis & interpretation |
| `/autopilot` | Launch or monitor autonomous science loop |
| `/design-experiment` | Simulation experiment design |
| `/first-principles` | Derive from model axioms |
| `/frontier` | Frontier map & gap analysis |
| `/hypothesis` | Research question framing |
| `/investigate-physics` | Anomaly investigation |
| `/progress` | Research retrospective |
| `/pstack` | Physics science stack index |
| `/sanity` | Physical sanity check |
| `/sweep` | Parameter sweep generator |
| `/theory-review` | Theoretical consistency check |
| `/validate` | Reproducibility & robustness check |
| `/write-up` | Scientific write-up |

**Full content of each command should be extracted into the methodology paper as evidence of the structured AI workflow.** See [docs/ai_methodology/raw/workflow_tooling.md](./ai_methodology/raw/workflow_tooling.md) for raw command bodies.

### 2.3 Science workflow scaffolding

Located in `/Users/jonBridger/Toy Physics/.claude/science/`. Subdirectory structure:

| Subdirectory | File count | Purpose |
|---|---|---|
| `analyses/` | TBD | Result analyses |
| `derivations/` | 15 | Step-by-step derivations |
| `experiments/` | TBD | Simulation experiment specifications |
| `frontier/` | TBD | Frontier mapping |
| `hypotheses/` | 6 | Research questions / framing |
| `investigations/` | 1 | Anomaly investigations |
| `sanity/` | TBD | Physical-sanity checks |
| `theory-reviews/` | TBD | Theoretical-consistency checks |
| `write-ups/` | TBD | Scientific write-ups |

**Sample content from each subdirectory should be captured.** See [docs/ai_methodology/raw/science_scaffolding.md](./ai_methodology/raw/science_scaffolding.md).

### 2.4 Process protocols

Located in repo root and `docs/`:

- `AUTOPILOT_PROTOCOL.md`
- `AUTOPILOT_JANITOR_PROTOCOL.md`
- `AUTOPILOT_SUMMARY_PROTOCOL.md`
- `AUTOPILOT_WORKLOG.md`
- `docs/REVIEW_HARDENING_BACKLOG.md` (now archived to `docs/work_history/repo/backlog/REVIEW_HARDENING_BACKLOG.md`)
- `docs/CANONICAL_HARNESS_INDEX.md`
- `docs/REPRODUCIBILITY_FREEZE_2026-04-14.md` (in publication package)
- `docs/publication/ci3_z3/AI_ASSISTANCE_AND_ACCOUNTABILITY_NOTE.md` (existing public AI-disclosure document)

### 2.5 Memory files (Claude project memory)

Located in `~/.claude/projects/-Users-jonBridger-Toy-Physics/memory/`:

- `MEMORY.md` (top-level index)
- `project_context.md`
- `feedback_review_standards.md`
- `gate_status_2026_04_14.md`
- `ckm_gate_closed_2026_04_25.md`
- `dm_eta_freezeout_bypass_2026_04_25.md`

Full content extracted to [docs/ai_methodology/raw/memory_files.md](./ai_methodology/raw/memory_files.md).

---

## 3. Branch / Worktree Inventory

The project uses a high-velocity worktree-per-branch pattern. Each worktree is a separate parallel investigation. Worktrees encountered (from `~/.claude/projects/`):

```
adoring-curran-2fd11b
angry-sanderson-a5158e
bonus-predictions
brave-lederberg-639ffb
confinement
cool-solomon-996597
eloquent-wilbur
epic-euclid-651ffa
gifted-mirzakhani
great-nobel-ab743c
great-swartz-9b2299
inspiring-meitner
laughing-ardinghelli
lorentz-invariance
nifty-mestorf
quirky-jepsen
quizzical-shockley-537438 (current)
relaxed-taussig-18d9fb
sad-yonath
session-delta
stoic-almeida
stupefied-khayyam
upbeat-bartik-6d6d03
vigilant-goldstine-e369dc
wonderful-napier-5a2a60
```

Plus codex/* branches visible in git history. Full enumeration deferred to next pass.

---

## 4. Repository Audit (Top-Level)

### 4.1 Directory structure (top-level)

```
ARCHITECTURE_OPTIONS.md
AUTOPILOT_JANITOR_PROTOCOL.md
AUTOPILOT_PROTOCOL.md
AUTOPILOT_SUMMARY_PROTOCOL.md
AUTOPILOT_WORKLOG.md
LICENSE
README.md
SCALING_BENCHMARK_TABLE.md
SCALING_FAILURE_MECHANISMS.md
SCALING_TARGETS.md
docs/
logs/
outputs/
requirements.txt
scripts/
toy_event_physics.py
```

### 4.2 docs/ structure (selected)

- `docs/publication/ci3_z3/` — manuscript surface (claims table, prediction surface, derivation atlas, etc.)
- `docs/work_history/` — archived material (repo, ckm, dm, atomic, pf, yt subdirs)
- `docs/lanes/` — lane-specific tracking
- `docs/repo/` — repo organizational notes
- 1,379 top-level `docs/*.md` files

### 4.3 Retained results inventory (current main, summarized)

See [docs/publication/ci3_z3/CLAIMS_TABLE.md](publication/ci3_z3/CLAIMS_TABLE.md) and [docs/publication/ci3_z3/QUANTITATIVE_SUMMARY_TABLE.md](publication/ci3_z3/QUANTITATIVE_SUMMARY_TABLE.md) for current retained-claim surface.

Summary at branch creation (`9d0fbabf`, 2026-04-25):

- **One axiom:** Cl(3) on Z³ as the physical theory
- **Zero free dimensionless parameters:** g_bare = 1 derived (two-Ward same-1PI pinning theorem)
- **One dimensional pin:** `a^(-1) = M_Pl` (conditional completion theorem with 3 named blockers)
- **Sub-percent quantitative agreements:** v, α_s(M_Z), sin²θ_W, 1/α_EM, g_1, g_2, y_t, m_t, |V_us|, |V_cb|, |V_ub|, δ_CKM, J — 13 SM observables
- **Retained structural theorems:** SU(2), SU(3), 3+1, hypercharge uniqueness, fractional charge denominator, all anomaly cancellations, B-L freedom, three-generation, exact CPT, I_3=0 (Born forced), CHSH Bell, emergent Lorentz with dim-6 ℓ=4, exact 1+1D and 3+1D boost-covariant continuum, strong CP θ_eff=0, universal θ-EDM vanishing, exact discrete 3+1 GR, canonical textbook Einstein-Hilbert continuum equivalence, three KK spectral towers (scalar, vector, graviton TT)
- **CKM structurally closed:** every entry + B_s phase + Thales CP ratio + NLO γ̄ in closed form
- **DM flagship CLOSED package:** exact-target PMNS, sin δ_CP = −0.9874, θ_23 ≥ 0.5410
- **Open flagship lane:** charged-lepton Koide (Q=2/3, δ=2/9), 2 named bridges
- **Conditional lane:** Planck-scale pin (3 named blockers; Widom carrier route closed negative)

---

## 5. Raw Data Captures (this pass)

The following raw extracts are produced on this info-capture pass. Each file is verbatim data, not narrative.

### 5.1 Claude session prompt extracts

- [docs/ai_methodology/raw/prompts_session_04c820e1.md](./ai_methodology/raw/prompts_session_04c820e1.md) — **589 user prompts, 12,131 lines**, 2026-04-12 to 2026-04-14
- [docs/ai_methodology/raw/prompts_session_855ddec4.md](./ai_methodology/raw/prompts_session_855ddec4.md) — **220 user prompts, 5,338 lines**, 2026-04-14 to 2026-04-15
- [docs/ai_methodology/raw/prompts_session_67759a49.md](./ai_methodology/raw/prompts_session_67759a49.md) — **53 user prompts, 391 lines**, 2026-04-14 to 2026-04-16
- [docs/ai_methodology/raw/prompts_session_small.md](./ai_methodology/raw/prompts_session_small.md) — **5 prompts combined**, 277 lines, 3 short sessions
- [docs/ai_methodology/raw/prompts_session_current.md](./ai_methodology/raw/prompts_session_current.md) — **24 prompts**, current session 2026-04-25, in-progress

**Total extracted user prompts (top-level Claude only, all sessions):** 891 across 5 files, ~18,300 lines verbatim.

### 5.2 Workflow tooling

- [docs/ai_methodology/raw/workflow_tooling.md](./ai_methodology/raw/workflow_tooling.md) — **full content of all 14 custom slash commands**, 1,375 lines
- [docs/ai_methodology/raw/science_scaffolding.md](./ai_methodology/raw/science_scaffolding.md) — **content of `~/.claude/science/` subdirectories** with one full sample per subdir, 994 lines

### 5.3 Process protocols

- [docs/ai_methodology/raw/protocols.md](./ai_methodology/raw/protocols.md) — **autopilot protocols (full) + review hardening backlog + canonical harness index + reproducibility freeze**, 18,503 lines (1.3 MB — the AUTOPILOT_WORKLOG dominates)

### 5.4 Memory + accountability

- [docs/ai_methodology/raw/memory_files.md](./ai_methodology/raw/memory_files.md) — **full memory file content** (6 files), 319 lines
- [docs/ai_methodology/raw/ai_accountability_note.md](./ai_methodology/raw/ai_accountability_note.md) — **AI-assistance disclosure note recovered from git history** (`56876669^`); the note was removed from public package on 2026-04-23 in commit `56876669` "Clean public package surface and remove internal docs" and is preserved here for methodology-paper precedent

### 5.5 Repo audit

- [docs/ai_methodology/raw/repo_audit.md](./ai_methodology/raw/repo_audit.md) — **directory tree, file counts, frontier inventory, branch list, commits-per-day timeline, top-level theorem-grade pattern counts, claims-table + quantitative-summary headers**, 457 lines

### 5.6 Total info-capture volume

**40,009 lines, ~2.4 MB of raw verbatim data** across 11 files in `docs/ai_methodology/raw/`. All material is unprocessed source data ready for cleaning, organization, and synthesis on subsequent passes.

---

## 6. Open Items for Subsequent Passes

1. **Codex prompt history extraction** — locate Codex session logs (likely at `~/.codex/` or similar; investigate)
2. **Subagent prompt capture** — extract prompts FROM Claude TO subagents from the 745 subagent jsonl files; this captures the tree-search / parallel-attack patterns
3. **Branch-summary extraction** — every `BRANCH_SUMMARY_*.md` and `SESSION_SYNTHESIS_*.md` in `docs/` documents an AI-driven research session and should be inventoried
4. **Commit message corpus** — 2,658 commit messages document the actual research increments; should be extracted as a research-velocity time series
5. **Codex review notes** — `codex/review-active` branch and historical Codex review surfaces; cross-reference with current Claude work
6. **Time-on-task analysis** — from session timestamps, derive actual human attention vs AI autonomous time
7. **Failure / no-go inventory** — every `*NO_GO*.md` and `*FAILURE*.md` is an AI-generated obstruction theorem; these are key methodology evidence
8. **Worktree purpose documentation** — each of 25 worktrees represents a parallel investigation; document what each was for
9. **Cross-tool reconciliation events** — places where Codex caught Claude errors (or vice versa) — these are critical methodology evidence

---

## 7. Methodology Paper Outline (Draft, for Later Cleanup)

This is a placeholder outline for the eventual methodology paper. To be filled in once raw capture is complete.

### Sections (proposed):

1. Abstract
2. Introduction: AI-assisted theoretical physics
3. The Cl(3)/Z³ framework as a case study
4. Methodology
   - Tool stack (Claude, Codex, custom slash commands)
   - Workflow scaffolding (science/ subdirs, autopilot protocols)
   - Self-audit discipline (bounded vs retained labels, no-go theorems, runner harness)
   - Worktree-per-branch parallel investigation pattern
   - Cross-tool adversarial review (Claude ↔ Codex)
5. Quantitative results
   - Production-rate analysis (commits/day, theorems/day)
   - Verification cost (PASS counts, runner suite)
   - Time-on-task vs autonomous time
6. Failure modes and mitigations
   - AI hallucination (mitigated by runner harness)
   - Bounded-vs-retained drift (mitigated by explicit labeling)
   - Verifiability (mitigated by full audit trail in public repo)
7. Reproducibility
   - Public repo, frozen runners, regression gate
   - Methodology checklist for other groups
8. Limitations and risks
9. Conclusion: implications for the field

---

## 8. Style and Voice Notes (to inform later cleanup)

- This is a methodology paper, not a physics paper. Audience: physicists + AI-research community + journal editors evaluating AI-assisted submissions.
- Tone: matter-of-fact, evidence-driven, no apologies for the AI-method angle, no hype either.
- Volume of evidence is the credibility lever. The full audit trail IS the methodological contribution.
- Disclose everything; concealment is fragile and the repo is public anyway.
- Compare productivity rates against historical baseline explicitly.
- Place this work as the first credible AI-assisted theoretical-physics framework with full self-audit discipline; that priority claim is time-limited.
