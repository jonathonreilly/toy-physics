# Reproduce Guide

Run these from the repo root on this branch.

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
- do not elevate bounded lanes from raw stdout alone
- runner names are historical in a few places:
  - `frontier_born_rule_derived.py` supports the retained `I_3 = 0` theorem,
    not a freestanding full Born-rule derivation
  - `frontier_newton_derived.py` supports the retained weak-field Newton /
    Poisson claim, not the full GR-signature bundle

## Packaging rule

For GitHub or submission support:

- pin the exact commit hash
- archive raw stdout logs per runner under `outputs/` or `logs/`
- keep a one-line status ledger: `retained`, `bounded`, or `open`
- before release, check [SUBMISSION_CHECKLIST.md](./SUBMISSION_CHECKLIST.md)
