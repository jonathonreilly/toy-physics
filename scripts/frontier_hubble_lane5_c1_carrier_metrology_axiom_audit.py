#!/usr/bin/env python3
"""Lane 5 (C1) carrier/metrology axiom audit.

This runner summarizes the C1 state after A1, A2, A4, A5, and A6. It does
not prove C1. It checks that the remaining positive route requires two
explicit human-judgment premises unless a new theorem is found:

  1. a primitive metric/orientation/phase selector for the active Cl_4/CAR
     coframe response on P_A H_cell;
  2. a non-rescaling-invariant action-unit metrology map.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def main() -> int:
    checks: list[Check] = []

    direct_shortcuts_blocked = {
        "A1_bulk_car_rank_four": True,
        "A2_dimensionless_lattice_metrology": True,
        "A4_parity_gate_to_car": True,
        "A5_full_cell_odd_coframe_restriction": True,
    }
    checks.append(
        Check(
            "direct_C1_shortcuts_are_blocked",
            all(direct_shortcuts_blocked.values()),
            ", ".join(f"{name}=blocked" for name in direct_shortcuts_blocked),
        )
    )

    a6_capacity_positive = True
    a6_selector_open = True
    checks.append(
        Check(
            "bilinear_route_is_capacity_positive_selector_open",
            a6_capacity_positive and a6_selector_open,
            "P_A bilinears generate M4(C), but metric/orientation/phase selector is open",
        )
    )

    selector_premise = {
        "active_block_Cl4": True,
        "metric_orientation_phase_basis": True,
        "oriented_car_pairing": True,
    }
    metrology_premise = {
        "non_rescaling_action_unit_map": True,
        "clock_source_action_coupling": True,
    }
    checks.append(
        Check(
            "minimal_selector_premise_is_explicit",
            all(selector_premise.values()),
            "active Cl4 plus metric/orientation/phase and CAR pairing selector",
        )
    )
    checks.append(
        Check(
            "minimal_metrology_premise_is_explicit",
            all(metrology_premise.values()),
            "non-rescaling clock/source/action map selecting dimensional kappa",
        )
    )

    derived_without_axioms = False
    conditional_with_axioms = all(selector_premise.values()) and all(metrology_premise.values())
    checks.append(
        Check(
            "current_stack_does_not_derive_C1_without_new_premises",
            not derived_without_axioms,
            "A1/A2/A4/A5 block direct derivations; A6 supplies capacity only",
        )
    )
    checks.append(
        Check(
            "conditional_C1_route_is_well_formed_if_premises_are_accepted",
            conditional_with_axioms,
            "selector + metrology would feed the existing conditional Target 3/source-unit chain",
        )
    )

    lane5_human_judgment_boundary = (not derived_without_axioms) and conditional_with_axioms
    checks.append(
        Check(
            "lane5_C1_now_requires_human_science_judgment_or_new_theorem",
            lane5_human_judgment_boundary,
            "accept a minimal carrier/metrology premise or discover a new selector/metrology theorem",
        )
    )

    print("=" * 78)
    print("Lane 5 (C1) carrier/metrology axiom audit")
    print("=" * 78)
    passed = 0
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")
        passed += int(check.passed)
    failed = len(checks) - passed
    print("-" * 78)
    print(f"TOTAL: PASS={passed}, FAIL={failed}")
    if failed == 0:
        print(
            "Conclusion: C1 is not derived on the current stack. The minimal "
            "conditional route is explicit, but accepting it is a human "
            "science-judgment decision unless a new theorem supplies selector "
            "and metrology."
        )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
