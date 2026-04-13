# Discrete Event-Network Physics Repo

This repo contains multiple historical physics programs, but this branch is
organized around the current `Cl(3)` on `Z^3` publication package.

## Start Here

- Publication package:
  [`docs/publication/ci3_z3/README.md`](docs/publication/ci3_z3/README.md)
- Full claim ledger:
  [`docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md`](docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md)
- Submission checklist:
  [`docs/publication/ci3_z3/SUBMISSION_CHECKLIST.md`](docs/publication/ci3_z3/SUBMISSION_CHECKLIST.md)
- Figure plan:
  [`docs/publication/ci3_z3/FIGURE_PLAN.md`](docs/publication/ci3_z3/FIGURE_PLAN.md)
- Current paper state:
  [`docs/CI3_Z3_PUBLICATION_STATE_2026-04-12.md`](docs/CI3_Z3_PUBLICATION_STATE_2026-04-12.md)
- Paper outline:
  [`docs/PAPER_OUTLINE_2026-04-12.md`](docs/PAPER_OUTLINE_2026-04-12.md)
- Flagship contribution statement:
  [`docs/FLAGSHIP_PAPER_CONTRIBUTION_STATEMENT_NOTE.md`](docs/FLAGSHIP_PAPER_CONTRIBUTION_STATEMENT_NOTE.md)
- Retained runner map:
  [`docs/CANONICAL_HARNESS_INDEX.md`](docs/CANONICAL_HARNESS_INDEX.md)
- Work-history lane:
  [`docs/work_history/README.md`](docs/work_history/README.md)

## Current Branch Reality

- **Framework statement:** `Cl(3)` on `Z^3` is the physical theory
- **Retained paper core:** exact native `SU(2)`, graph-first structural
  `SU(3)`, weak-field gravity from the Poisson / Newton chain together with
  weak-field WEP and time dilation, anomaly-forced `3+1`, retained `S^3`
  compactification / topology closure, full-framework one-generation closure,
  and three-generation matter structure
- **Three live paper gates:** DM relic mapping, renormalized `y_t`, and CKM /
  flavor closure

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

- Use the publication package before trusting an old note by filename alone.
- Keep retained, bounded, and open lanes separate.
- If a result is not represented by a runner + note + explicit status, treat
  it as exploratory.
