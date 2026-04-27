# Artifact Plan

## Cycle 1: Lane 4 Dirac/Seesaw Fork Guardrail

Deliverables:

- `docs/NEUTRINO_LANE4_DIRAC_SEESAW_FORK_NO_GO_NOTE_2026-04-27.md`
- `scripts/frontier_neutrino_lane4_dirac_seesaw_fork_no_go.py`
- `logs/2026-04-27-neutrino-lane4-dirac-seesaw-fork-no-go.txt`
- refreshed workstream pack files under this directory

Verification:

- run the new runner with `PYTHONPATH=scripts`;
- compile the new runner;
- rerun focused source authorities:
  - `frontier_neutrino_majorana_current_stack_zero_law.py`
  - `frontier_neutrino_mass_derived.py`
  - `frontier_neutrino_retained_observable_bounds.py`
- run `git diff --check`;
- emulate review-loop locally and record findings in `REVIEW_HISTORY.md`.

Expected claim movement:

- no retained closure;
- exact negative boundary against a hidden one-surface closure conflation;
- sharper next-action fork for Lane 4.

## Cascade After Lane 4

If Lane 4 reaches a genuine stop condition, continue in this order:

1. Lane 2 atomic-scale predictions;
2. Lane 5 Hubble constant derivation;
3. Lane 3 quark mass retention;
4. Lane 1 hadron mass program;
5. Lane 6 charged-lepton mass retention only if a new premise is discovered.

## Cycle 2: Lane 2 Rydberg Dependency Firewall

Deliverables:

- `docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`
- `scripts/frontier_atomic_rydberg_dependency_firewall.py`
- `logs/2026-04-27-atomic-rydberg-dependency-firewall.txt`

Verification:

- run the new runner with `PYTHONPATH=scripts`;
- compile the new runner;
- rerun the existing atomic hydrogen/helium scaffold;
- run the audit pipeline and strict lint;
- run `git diff --check`;
- record review-loop emulation in `REVIEW_HISTORY.md`.

Expected claim movement:

- no retained Rydberg closure;
- exact dependency firewall showing `m_e` and `alpha(0)` transport are
  load-bearing;
- Lane 2 stop boundary unless a new charged-lepton or low-energy QED premise
  is supplied.
