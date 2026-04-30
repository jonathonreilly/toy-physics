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
  force scales but not a unique `sqrt(sigma)` map.

Verification:

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_gate_repair.py
# PASS=16 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py
# PASS=14 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_confinement_to_mass_firewall.py
# PASS=16 FAIL=0
```

## Next Exact Action

Pick one of two next blocks:

1. B5 large-volume framework-to-standard-QCD link check. This is the
   stronger science route because it would reduce the residual on all
   imported lattice-QCD bridge values.
2. Retained-with-budget draft that chooses `r0`/`r1` as the Lane 1
   force-scale observable and keeps `sqrt(sigma)` as a bounded
   comparator, with static-potential convention split explicit.

## Do Not Reopen

- Rough x0.96 promotion.
- PDG backsolve factor.
- Pure quenched large-volume route as a direct B2 closure.
