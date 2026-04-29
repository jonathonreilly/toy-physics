# [physics-loop] Lane 3 quark mass retention block 02: open conditional bridge

## Summary

This stacked science block continues Lane 3 from block 01 and attacks the
Route-2 E-center/source readout residual for the up-type scalar-law target.

It proves a sharp conditional bridge:

```text
gamma_T(center)/gamma_E(center) = -R_conn = -8/9
=> q_E = 15/8
=> beta_E/alpha_E = 21/4.
```

It also proves the import boundary: current Route-2 carrier columns do not
type the missing source-domain identification from the retained SU(3)
connected color projection to the E/T center endpoint ratio.

Honest status: `open`. This is not retained `m_u`/`m_c` closure.

## Artifacts

- Loop handoff:
  `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/HANDOFF.md`
- Review history:
  `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/REVIEW_HISTORY.md`
- Note:
  `docs/QUARK_ROUTE2_RCONN_CENTER_RATIO_BRIDGE_OBSTRUCTION_NOTE_2026-04-28.md`
- Runner:
  `scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py`
- Log:
  `logs/2026-04-28-quark-route2-rconn-center-ratio-bridge-obstruction.txt`

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py
TOTAL: PASS=26, FAIL=0

python3 -m py_compile scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_readout_map.py
PASS=11 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
TOTAL: PASS=28, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_endpoint_ratio_chain_law.py
PASS=14 FAIL=0
```

## Review Disposition

The block uses `R_conn=8/9` as retained support and a conditional bridge
candidate only. It does not use observed quark masses, fitted Yukawa entries,
CKM/J target minimization, or nearest-live-endpoint selection as proof inputs.

Remaining blocker:

```text
derive a typed source-domain theorem for
gamma_T(center)/gamma_E(center) = -R_conn.
```
