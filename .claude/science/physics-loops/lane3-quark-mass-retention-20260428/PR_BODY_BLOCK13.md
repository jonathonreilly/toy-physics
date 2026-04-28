# [physics-loop] Lane 3 quark mass retention block13: stuck fan-out synthesis

## Summary

Block 13 is the required stuck fan-out after the deep RPSR/C3 work in blocks
10 through 12.

It asks whether any current-bank route now reaches retained non-top quark
masses. The answer is no: all six orthogonal frames terminate at named missing
theorem content.

## Artifacts

- `docs/QUARK_LANE3_STUCK_FANOUT_SYNTHESIS_2026-04-28.md`
- `scripts/frontier_quark_lane3_stuck_fanout_synthesis.py`
- `logs/2026-04-28-quark-lane3-stuck-fanout-synthesis.txt`
- `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/STOP_REQUESTED`
- loop-pack updates under `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Result

Fan-out frames checked:

```text
1. gauge/operator
2. Ward-normalization
3. CKM/singular-value
4. endpoint/source
5. C3/RPSR readout
6. down-type NP/scale
```

The typed-edge graph has no path from current support nodes to:

```text
retained_non_top_quark_masses
```

Successful proposed paths all require new theorem edges:

```text
C3_coefficient_source_law
physical_channel_assignment
two_ratio_readout
five_sixths_NP_scale_theorem
Route2_source_domain_bridge
species_differentiated_non_top_Ward
```

This does not claim future Lane 3 closure is impossible. It records that
retained closure is not latent in the current artifacts.

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_stuck_fanout_synthesis.py
TOTAL: PASS=68, FAIL=0

python3 -m py_compile scripts/frontier_quark_lane3_stuck_fanout_synthesis.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_rpsr_c3_joint_readout_rank_boundary.py
TOTAL: PASS=87, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py
TOTAL: PASS=80, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_five_sixths_scale_selection_boundary.py
TOTAL: PASS=34, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_source_domain_bridge_no_go.py
TOTAL: PASS=33, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0
```

## Honest Claim Status

Lane 3 remains open.

This block supports a supervisor stop for human science judgment:

```text
all viable current-bank routes are blocked after deep-work and fan-out;
the remaining progress requires choosing or deriving new theorem content.
```
