# /pstack — Physics Science Stack Index

You are running PStack — a physics science stack for the discrete event-network toy model.

## Available Skills

### Research Direction
| Skill | Role | What It Does |
|-------|------|-------------|
| `/hypothesis` | Research Director | Frame a falsifiable research question before any experiment |
| `/theory-review` | Theoretical Physicist | Check a hypothesis for internal consistency and minimality |

### Experiment Design
| Skill | Role | What It Does |
|-------|------|-------------|
| `/design-experiment` | Experimental Physicist | Plan a simulation run with observables, controls, and parameters |
| `/sweep` | Computational Physicist | Generate parameter sweep scripts from a base script |

### Analysis & Validation
| Skill | Role | What It Does |
|-------|------|-------------|
| `/analyze` | Data Analyst | Systematically analyze simulation output against predictions |
| `/validate` | Reproducibility Officer | 6-check battery: seeds, sensitivity, finite-size, initialization, logic, cherry-picking |
| `/sanity` | Senior Skeptic | 7-check audit for physical plausibility and artifact detection |
| `/review-loop` | Review Board | Parallel physics review loop: code/runner, claim boundary, imports/support, Nature-grade retention, repo governance |

### Investigation
| Skill | Role | What It Does |
|-------|------|-------------|
| `/investigate-physics` | Detective Physicist | 4-phase anomaly investigation: characterize, hypothesize, discriminate, resolve |
| `/first-principles` | First-Principles Theorist | Derive emergent behavior from model axioms alone (no known physics) |

### Documentation
| Skill | Role | What It Does |
|-------|------|-------------|
| `/write-up` | Scientific Writer | Produce archival-quality summary of a completed investigation |
| `/progress` | Research Manager | Weekly retrospective with frontier status and next-step recommendations |

### Automation & Strategy
| Skill | Role | What It Does |
|-------|------|-------------|
| `/autopilot` | Lab Automation | Launch, monitor, or check the autonomous science loop (with repo lock) |
| `/frontier` | Research Strategist | Map explored vs. unexplored territory, rank highest-value gaps |
| `/physics-loop` | Physics Loop Lead | Run or resume a deep long-form physics loop on clean science block branches with import audits, no-go memory, stretch attempts, checkpoints, review-loop backpressure, and review PRs |

## Science Pipeline

```
/hypothesis --> /theory-review --> /design-experiment --> [write script] --> [run]
                                         |
                                      /sweep (if parameter scan)
                                         |
                                         v
                              /analyze --> /validate --> /sanity --> /review-loop
                                         |
                                      /first-principles (derive from axioms)
                                         |
                                         v
                                      /write-up
```

Side channels (run anytime):
- `/investigate-physics` — when results are unexpected
- `/frontier` — to decide what to work on next
- `/physics-loop` — to pursue a major open lane/problem as a stateful long-running loop
- `/progress` — periodic research retrospective
- `/autopilot` — for unattended science runs
- `/review-loop` — before promoting retained/support claims or asking for external review

## Core Principles

1. **Exhaust the Parameter Space** — AI makes sweeps cheap. Run the full scan, not spot checks.
2. **Import Discipline** — Derive from model primitives when making framework claims; use known physics and literature only as disclosed comparators, bridges, or admitted context.
3. **Nature Decides** — Simulation results are ground truth. When theory and data disagree, investigate the data.

## Lock Protocol

Skills that modify files or run scripts acquire the cooperative repo lock:
```bash
python3 scripts/automation_lock.py acquire --owner pstack-{skill} --purpose "{description}" --ttl-hours N
```

Skills that only read and think (hypothesis, theory-review, sanity, first-principles, write-up, progress, frontier, pstack) do NOT need the lock.

## Output Directory

All PStack documents live in `.claude/science/`:
```
.claude/science/
  hypotheses/
  experiments/
  analyses/
  validations/
  sanity/
  investigations/
  derivations/
  write-ups/
  progress/
  frontier/
  physics-loops/
  theory-reviews/
  reviews/
```

Print this index when invoked. Ask the user which skill they want to run.
