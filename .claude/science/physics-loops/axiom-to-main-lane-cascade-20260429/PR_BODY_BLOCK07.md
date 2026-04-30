# [physics-loop] axiom-to-main-lane-cascade block 07: PMNS three-identity Q_Koide-from-V8 support lift

## Summary

Block 7 composes V8 (Block 1, now support/audit-pending on main for
Q_Koide = 2/3 on A_min) with the PMNS three-identity selector support
package (2026-04-21). The PMNS chart constant Q_Koide = 2/3 lifts from
"imported numeric value" to "V8-derived structural value on A_min",
retiring one chart-side import at support tier.

The three open gaps in the PMNS support proposal (proposed selector
laws, basin uniqueness, broader PMNS/DM gate) are unchanged.

## Stacking note

Depends on merged Block 1 (PR #183). V8 is current on main as support
and audit-pending; Block 1's audit ratification is prerequisite for any
stronger tier.

## Status (per skill firewall fields)

- `actual_current_surface_status: support`
- `proposal_allowed: true`
- `audit_required_before_effective_retained: true`
- `bare_retained_allowed: false`
- `proposed_selector_laws_status: open` (PMNS gaps unchanged)
- `basin_uniqueness_status: bounded_multi_start`
- `broader_pmns_dm_gate_status: open`

## Composed chart

```text
V8 (Block 1):    Q_Koide = 2/3 on A_min (support/audit-pending)
                 ⇒ chart constant Q_Koide V8-derived
                 ⇒ SELECTOR = √Q_Koide = √6/3 V8-derived

PMNS chart:      Tr(H) = Q_Koide      (retained chart identity)
                 delta · q_+ = Q_Koide  (proposed selector law, OPEN)
                 det(H) = E2            (proposed selector law, OPEN)
```

## Artifacts

- `docs/PMNS_THREE_IDENTITY_Q_KOIDE_FROM_V8_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md`
- `scripts/frontier_pmns_three_identity_q_koide_from_v8_support_lift.py`
- `outputs/frontier_pmns_three_identity_q_koide_from_v8_support_lift_2026-04-29.txt` (PASS=N FAIL=0)

## What is and is NOT closed

### Support-tier lift recorded
1. PMNS chart constant Q_Koide is now V8-derived (one import retired)
2. SELECTOR = √Q_Koide = √6/3 also V8-derived
3. PMNS three-identity numerical solution structurally V8-supported

### NOT closed
1. Proposed selector law `delta · q_+ = Q_Koide` — still proposed
2. Proposed selector law `det(H) = E2` — still proposed
3. Basin uniqueness — bounded multi-start
4. Broader PMNS/DM gate — open

## Verification

```bash
git checkout physics-loop/axiom-to-main-lane-cascade-20260429-block07-20260429
python3 scripts/frontier_pmns_three_identity_q_koide_from_v8_support_lift.py
```

PASS=N FAIL=0.

## Links

- [V1 theorem note](docs/PMNS_THREE_IDENTITY_Q_KOIDE_FROM_V8_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md)
- [V8 Block 1 (prerequisite)](docs/KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md)
- [PMNS three-identity (cited)](docs/PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
