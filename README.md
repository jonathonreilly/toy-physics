# Discrete Event-Network Physics Repo

This repo is a research codebase for discrete graph- and lattice-based toy
physics architectures. It is no longer small enough to navigate by chronology,
so the repo now has an explicit navigation layer.

## Start Here

- Current entrypoint:
  [`docs/START_HERE.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/START_HERE.md)
- Lane map:
  [`docs/repo/LANE_STATUS_BOARD.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/repo/LANE_STATUS_BOARD.md)
- Repo organization:
  [`docs/repo/REPO_ORGANIZATION.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/repo/REPO_ORGANIZATION.md)
- Root-file guide:
  [`docs/repo/ROOT_FILE_GUIDE.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/repo/ROOT_FILE_GUIDE.md)
- Lane manifests:
  [`docs/lanes/README.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/lanes/README.md)
- Publication-discovery log:
  [`docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md)
- Retained runner map:
  [`docs/CANONICAL_HARNESS_INDEX.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/CANONICAL_HARNESS_INDEX.md)
- Bug / rerun workflow:
  [`docs/repo/RETEST_PLAYBOOK.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/repo/RETEST_PLAYBOOK.md)

## Current Repo Reality

- **Primary retained lane:** staggered fermion with corrected parity coupling
- **Cleanest retained directional result:** exact lattice-force canonical card
- **Strongest graph-native companion package:** cycle battery, scaled cycle
  battery, self-gravity, two-field wave, retarded closure, and DAG
  compatibility
- **Main open blocker:** no frozen sign-selective endogenous irregular-graph
  observable
- **Exploratory reopen:** emergent geometry growth

The older mirror, ordered-lattice, action-power, and coin-walk programs are
still in the repo. They are indexed as historical or bounded lanes, not
deleted.

## Whole-Repo Program Families

This repo now treats `main` as a set of major lane families, not one flat pile
of scripts:

- current mainline: staggered fermion + parity coupling
- exact historical flagship: mirror / exact geometry / `Z2 x Z2`
- historical retained bridge: ordered lattice / dense spent-delay
- historical retained bridge: nearest-neighbor refinement
- historical retained bridge: structured chokepoint / generated symmetry
- historical bounded families: action-power / valley-linear / dimension-dependent kernel
- historical bounded families: Gate B / generated geometry / source-resolved
- historical blocked lane: coin / chiral / Dirac-walk
- historical controls: scalar / KG and moonshot horizon probes

Use the lane board, not file-name prominence, to know which one you are in.

## Repo Layout

- `scripts/`
  - runners and probes
  - `frontier_*` is the active frontier namespace
- `scripts/README.md`
  - code-side navigation guide
- `docs/`
  - retained notes, synthesis, audits, and historical writeups
- `docs/repo/`
  - organization and navigation docs
- `docs/lanes/`
  - lane-by-lane manifests for the whole repo
- `outputs/`, `logs/`
  - run artifacts

## Rules For Reading Claims

- Use the lane board before trusting an old flagship note.
- Keep exact lattice-force claims separate from irregular-graph proxy claims.
- If a result is not represented by a runner + retained note + lane status,
  treat it as exploratory.
