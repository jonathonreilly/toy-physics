# Handoff

## Current State

Cycle 1 complete. The branch selected Lane 1 route 3E B2 because
higher-priority open-science loops on `origin/main` already record
honest-stop state.

The landed result is negative/progress:

- the rough x0.96 screening factor cannot promote `sqrt(sigma)`;
- a PDG backsolve is circular;
- a literal asymptotic full-QCD string-tension target is underdefined
  because full QCD strings break;
- B2 is repaired into B2a/B2b;
- modern static-energy literature gives a bounded bridge, not a retained
  screening closure. TUMQCD fit-window `sqrt(sigma)` gives about
  `467.39 +/- 9.57 MeV` or `481.71 +/- 9.70 MeV` depending the
  static-potential convention; CLS `N_f=2+1` gives clean `r0`/`r1`
  force scales but not a unique `sqrt(sigma)` map;
- B5 current-surface shortcut is closed negatively: structural `SU(3)` +
  `g_bare -> beta=6` + current `4^4` check supports the bridge but does
  not retain it;
- B5 ladder budget is now explicit: `L=4,6,8` is a scout, not closure;
  `L=8,12,16` is the first compute class that can close B5.
- the fixed low-stat `L=4,6,8` pure-gauge scout validates local
  plaquette/Wilson-loop/Creutz measurement plumbing but remains explicitly
  non-closing.
- a resumable B5 Wilson/Creutz ladder runner now exists. Its smoke
  profile is verified; production `L=8,12,16` statistics remain to be
  accumulated before B5 can be promoted.

Verification:

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_gate_repair.py
# PASS=16 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py
# PASS=14 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py
# PASS=16 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_ladder_budget.py
# PASS=13 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_lowstat_scout.py
# PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py \
  --profile smoke \
  --fresh \
  --checkpoint-dir outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_checkpoints_smoke
# PASS=13 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_confinement_to_mass_firewall.py
# PASS=16 FAIL=0
```

## Next Exact Action

Pick one of two next blocks:

1. Run the resumable B5 ladder with `--profile production` under repeated
   wall-clock checkpoints until the `L=8,12,16` statistics can support or
   reject the bridge with uncertainties.
2. Retained-with-budget draft that chooses `r0`/`r1` as the Lane 1
   force-scale observable and keeps `sqrt(sigma)` as a bounded
   comparator, with static-potential convention split explicit.

## Do Not Reopen

- Rough x0.96 promotion.
- PDG backsolve factor.
- Pure quenched large-volume route as a direct B2 closure.
