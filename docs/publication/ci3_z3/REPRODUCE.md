# Reproduce Guide

Run these from the repo root on `main`.

## Core retained runners

```bash
python3 scripts/frontier_self_consistent_field_equation.py
python3 scripts/frontier_poisson_exhaustive_uniqueness.py
python3 scripts/frontier_newton_derived.py
python3 scripts/frontier_non_abelian_gauge.py
python3 scripts/frontier_graph_first_su3_integration.py
python3 scripts/frontier_anomaly_forces_time.py
python3 scripts/frontier_right_handed_sector.py
python3 scripts/frontier_generation_fermi_point.py
python3 scripts/frontier_generation_rooting_undefined.py
python3 scripts/frontier_generation_axiom_boundary.py
python3 scripts/frontier_cpt_exact.py
python3 scripts/frontier_born_rule_derived.py
```

## Expected use

- use the note paired with each runner as the claim boundary
- use [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) to see
  which derivation note and release artifact each runner supports
- do not elevate bounded lanes from raw stdout alone
- runner names are historical in a few places:
  - `frontier_born_rule_derived.py` supports the retained `I_3 = 0` theorem,
    not a freestanding full Born-rule derivation
  - `frontier_cpt_exact.py` is an exact theorem runner on even periodic
    lattices only
  - `frontier_newton_derived.py` supports the retained weak-field Newton /
    Poisson claim, not the full GR-signature bundle
- `frontier_anomaly_forces_time.py` mixes computed checks with labeled
  assertions; use the theorem note as the claim boundary rather than the raw
  scoreboard

## Packaging rule

For GitHub or submission support:

- pin the exact commit hash
- archive raw stdout logs per runner under `outputs/` or `logs/`
- archive retained logs under `logs/retained/` and figure-prep data under
  `outputs/figures/`
- keep a one-line status ledger: `retained`, `bounded`, or `open`
- before release, check [SUBMISSION_CHECKLIST.md](./SUBMISSION_CHECKLIST.md)

## Current selective freeze

The current pinned release slice is recorded in:

- [REPRODUCIBILITY_FREEZE_2026-04-14.md](./REPRODUCIBILITY_FREEZE_2026-04-14.md)

This freeze includes:

- one retained quantitative log
- one bounded quantitative log
- runner-backed figure-input logs for the current main figure candidates
