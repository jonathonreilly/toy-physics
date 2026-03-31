# PStack: Physics Science Stack for Claude Code

## Context

The physics repo is a discrete event-network toy model exploring emergent physics from minimal axioms. It has a mature Python simulator (`toy_event_physics.py`, ~30K lines, 599 functions), 193+ analysis scripts, and automated science loops (AUTOPILOT). The project workflow is: **hypothesize → design experiment → run simulation → analyze → validate → translate to physics language**.

Gary Tan's **gstack** maps software team roles (CEO, engineer, QA, designer, release engineer) to Claude Code slash commands that form a complete development pipeline. We want the equivalent for **computational physics research** — mapping scientific roles (research director, theorist, experimentalist, analyst, reviewer, etc.) to slash commands forming a complete research pipeline.

## Design Philosophy: Three Core Principles

Adapted from gstack's ethos to science:

1. **Exhaust the Parameter Space** (cf. "Boil the Lake") — AI makes sweeps cheap. Always run the complete parameter scan, not spot checks. The marginal cost of 100 runs vs 10 is near-zero.

2. **Search the Literature Before Deriving** (cf. "Search Before Building") — Check whether known physics already explains your observation before inventing new theory. Three layers: known results (textbook), recent work (arxiv), first principles (the valuable part).

3. **Nature Decides** (cf. "User Sovereignty") — The simulation results are ground truth, not the theory. When theory and simulation disagree, investigate the simulation — don't dismiss it.

## The PStack: 14 Skills in 6 Categories

### RESEARCH DIRECTION (cf. gstack Planning)

#### `/hypothesis` — Research Question Framing
**Role:** Research Director / PI
**cf. gstack:** `/office-hours`

Structured interrogation of a research question before any code is written:
- What specific prediction does this hypothesis make?
- What would falsify it? (Popper test)
- What's the null hypothesis / simplest alternative explanation?
- What parameter regime should show the effect most clearly?
- What existing results (in `logs/`) already bear on this question?
- Is this question well-posed given the model's axioms?

**Output:** Hypothesis document at `.claude/hypotheses/{name}.md` with predictions, falsification criteria, and proposed experiments.

#### `/theory-review` — Theoretical Consistency Check
**Role:** Theoretical Physicist
**cf. gstack:** `/plan-eng-review`

Reviews a hypothesis or proposed mechanism for theoretical soundness:
- Dimensional consistency (do units/scales make sense?)
- Conservation law compliance (does it respect the model's symmetries?)
- Limiting behavior (does it reduce to known results in simple limits?)
- Relationship to known physics (does this map to an established phenomenon?)
- Mathematical rigor of any derivations
- Whether the mechanism is genuinely emergent vs. put-in-by-hand

**Output:** Theory review document with pass/fail on each check, suggested refinements.

---

### EXPERIMENT DESIGN (cf. gstack Design)

#### `/design-experiment` — Simulation Design
**Role:** Experimental Physicist / Simulation Designer
**cf. gstack:** `/plan-design-review`

Plans a computational experiment before writing the script:
- What observables will be measured?
- What parameters will be varied and over what ranges?
- What controls are needed (baseline / null runs)?
- Sample size / ensemble size for statistical significance
- What systematic errors could contaminate results?
- What existing scripts in `scripts/` can be adapted vs. written fresh?
- Expected runtime and resource requirements

**Output:** Experiment design document with parameter table, observable list, and control strategy. Identifies reusable code from existing scripts.

#### `/sweep` — Parameter Sweep Generator
**Role:** Computational Physicist
**cf. gstack:** `/design-shotgun` (generates variants)

Generates a family of analysis scripts that systematically sweep a parameter space:
- Takes a base script and parameter ranges
- Generates N variants covering the space (grid, random, or adaptive)
- Creates a runner script that executes all variants
- Produces a collector script that aggregates results into a single summary
- Handles edge cases (parameter combinations that crash, timeouts)

**Output:** Script family in `scripts/`, runner script, and results aggregator.

---

### ANALYSIS & VALIDATION (cf. gstack Review/QA)

#### `/analyze` — Result Analysis & Interpretation
**Role:** Data Analyst / Experimentalist
**cf. gstack:** `/review`

Systematic analysis of simulation output:
- Read log files from `logs/` and extract key observables
- Statistical summary (mean, variance, distributions, outliers)
- Trend detection across parameter sweeps
- Anomaly flagging (results that break expected patterns)
- Comparison to theoretical predictions from `/hypothesis`
- Visualization suggestions (what plots would be most informative)
- Does the data support, refute, or remain ambiguous on the hypothesis?

**Output:** Analysis report with quantitative findings, verdict on hypothesis, and suggested follow-up experiments.

#### `/validate` — Reproducibility & Robustness Check
**Role:** QA Physicist / Reproducibility Officer
**cf. gstack:** `/qa`

Validates that a claimed result is real, not an artifact:
- Re-run with different random seeds (stochastic robustness)
- Vary parameters slightly around claimed regime (sensitivity analysis)
- Check for finite-size effects (does result persist at larger N?)
- Check for initialization artifacts (different starting conditions)
- Verify code correctness of the analysis script (logic review)
- Check for cherry-picking (does the effect appear in the full ensemble or just selected runs?)

**Output:** Validation report with confidence level (HIGH / MEDIUM / LOW / FAILED), reproducibility statistics, and identified fragilities.

#### `/sanity` — Physical Sanity Check
**Role:** Senior Physicist / Skeptic
**cf. gstack:** `/cso` (security audit → physics audit)

Audits results for physical plausibility:
- Does the result violate any conservation laws in the model?
- Are magnitudes reasonable? (order-of-magnitude checks)
- Does it survive dimensional analysis?
- Does it reduce correctly in known limits?
- Could this be a numerical artifact (precision, discretization, boundary effects)?
- Could this be a coding bug masquerading as physics?
- What would a skeptical reviewer's first objection be?

**Output:** Sanity report with pass/fail per check, list of potential objections and responses.

---

### INVESTIGATION (cf. gstack Debug)

#### `/investigate-physics` — Anomaly Investigation
**Role:** Detective Physicist
**cf. gstack:** `/investigate`

When simulation results are unexpected — systematically determine why:
1. **Characterize** — What exactly is unexpected? Quantify the discrepancy.
2. **Hypothesize** — Three candidate explanations: bug, artifact, or new physics.
3. **Discriminate** — Design minimal tests that distinguish between the three.
4. **Resolve** — Run tests, collect evidence, determine root cause.

**Iron Law:** No interpretation without investigation first. "Interesting" results get more scrutiny, not less.

**Output:** Investigation report with root cause determination and evidence trail.

#### `/bridge` — Map to Known Physics
**Role:** Translator / Phenomenologist
**cf. gstack:** `/codex` (outside perspective)

Attempts to connect emergent behavior to established physics:
- WebSearch arxiv and physics literature for similar phenomena
- Identify closest analogue in known physics (QFT, GR, condensed matter, etc.)
- Map the model's vocabulary to standard physics vocabulary
- Identify where the analogy breaks down
- Suggest what additional observables would strengthen or weaken the mapping
- Could this be a discrete version of a known continuum result?

**Output:** Bridge document mapping model concepts ↔ known physics, with confidence ratings and gap analysis.

---

### DOCUMENTATION & PROGRESS (cf. gstack Release/Docs)

#### `/write-up` — Scientific Write-Up
**Role:** Scientific Writer
**cf. gstack:** `/document-release`

Produces a structured scientific summary of a completed investigation:
- Abstract (one paragraph, result + significance)
- Background (what question, why it matters)
- Method (what was computed, key parameters)
- Results (quantitative findings with uncertainty)
- Discussion (interpretation, caveats, relationship to prior work)
- Next steps (what questions remain)

**Output:** Write-up document suitable for sharing or archiving.

#### `/progress` — Research Retrospective
**Role:** Research Manager
**cf. gstack:** `/retro`

Analyzes recent research activity:
- Review git log for recent commits and their themes
- Scan `logs/` for recent experiment results
- Identify which hypotheses were tested and their outcomes
- Track frontier status (what's been explored vs. unexplored)
- Highlight the strongest new result from the period
- Identify stalled investigations or dead ends
- Suggest highest-value next experiment

**Output:** Progress report with metrics, highlights, and recommended next steps.

---

### AUTOMATION & SAFETY (cf. gstack Safety/Setup)

#### `/autopilot` — Launch Autonomous Science Loop
**Role:** Lab Automation Controller
**cf. gstack:** `/ship` + `/canary`

Launches or manages the autonomous science loop:
- Read current AUTOPILOT_PROTOCOL.md and handoff state
- Validate the next experiment is well-defined
- Launch the science worker with proper locking
- Monitor for completion or errors
- Report results when done

**Output:** Launches automation, returns status.

#### `/frontier` — Frontier Map & Gap Analysis
**Role:** Research Strategist
**cf. gstack:** `/benchmark`

Maps the current state of explored parameter/mechanism space:
- Scan all `logs/` for completed experiments
- Scan all `scripts/` for experiment types
- Build a map of what's been tested where
- Identify gaps (unexplored parameter regions, untested mechanisms)
- Rank gaps by expected scientific value
- Identify redundant experiments that could be pruned

**Output:** Frontier map document with gap analysis and prioritized exploration targets.

---

## Pipeline Flow

```
/hypothesis → /theory-review → /design-experiment → [write script] → [run] → /analyze → /validate → /sanity → /bridge → /write-up
                                       ↓
                                   /sweep (if parameter scan needed)

Side channels:
  /investigate-physics (when results are unexpected)
  /frontier (to decide what to work on next)
  /progress (periodic retrospective)
  /autopilot (for unattended runs)
```

## Implementation Plan

### Files to Create

All skills go in `.claude/commands/` as markdown files:

| File | Skill |
|------|-------|
| `.claude/commands/hypothesis.md` | `/hypothesis` |
| `.claude/commands/theory-review.md` | `/theory-review` |
| `.claude/commands/design-experiment.md` | `/design-experiment` |
| `.claude/commands/sweep.md` | `/sweep` |
| `.claude/commands/analyze.md` | `/analyze` |
| `.claude/commands/validate.md` | `/validate` |
| `.claude/commands/sanity.md` | `/sanity` |
| `.claude/commands/investigate-physics.md` | `/investigate-physics` |
| `.claude/commands/bridge.md` | `/bridge` |
| `.claude/commands/write-up.md` | `/write-up` |
| `.claude/commands/progress.md` | `/progress` |
| `.claude/commands/autopilot.md` | `/autopilot` |
| `.claude/commands/frontier.md` | `/frontier` |

Plus a `.claude/commands/pstack.md` index file that lists all skills with one-line descriptions.

### Implementation Order

1. **Core science loop** (5 skills): `/hypothesis`, `/design-experiment`, `/analyze`, `/validate`, `/sanity`
2. **Investigation** (2 skills): `/investigate-physics`, `/bridge`
3. **Documentation** (2 skills): `/write-up`, `/progress`
4. **Automation** (2 skills): `/frontier`, `/autopilot`
5. **Advanced** (2 skills): `/theory-review`, `/sweep`
6. **Index**: `/pstack`

### Key Design Decisions

- Each skill is a standalone `.md` file in `.claude/commands/` (Claude Code's native skill format)
- Skills reference project-specific paths (`logs/`, `scripts/`, `toy_event_physics.py`)
- Output documents go to `.claude/science/` (hypotheses, analyses, write-ups)
- Skills are opinionated about scientific rigor (require falsification criteria, statistical significance, controls)
- No external dependencies — pure Claude Code slash commands

### Verification

After implementation:
1. Run `/pstack` to verify the index lists all 14 skills
2. Test `/hypothesis` with a sample question about the model
3. Test `/analyze` on a recent log file
4. Test `/frontier` to map current exploration state
5. Verify all output directories are created properly
