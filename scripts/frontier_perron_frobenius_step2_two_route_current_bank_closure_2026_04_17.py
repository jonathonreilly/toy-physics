#!/usr/bin/env python3
"""
Closure of the step-2A route analysis on the current PF bank.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_TWO_ROUTE_CURRENT_BANK_CLOSURE_NOTE_2026-04-17.md")
    operator_form = read("docs/PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md")
    microscopic_target = read("docs/PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md")
    direct_dweh = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")
    nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 TWO-ROUTE CURRENT-BANK CLOSURE")
    print("=" * 108)
    print()

    check(
        "Step-2 operator-form boundary note fixes the only admissible upstream schematic forms as Wilson -> D_- or Wilson -> dW_e^H",
        "`I_e^* T_Wilson I_e -> D_-`" in operator_form
        and "`P_e T_Wilson P_e -> dW_e^H`" in operator_form,
        bucket="SUPPORT",
    )
    check(
        "Step-2 microscopic-channel target note identifies Wilson -> D_- as the cleanest strong target",
        "Wilson-to-charged microscopic channel" in microscopic_target
        and "Wilson-to-`D_-` law" in microscopic_target,
        bucket="SUPPORT",
    )
    check(
        "Step-2 direct-dW_e^H route reduction note identifies Wilson -> dW_e^H as the fully typed compressed target",
        "the compressed target: `Wilson -> dW_e^H`" in direct_dweh
        and "fully reduced and honest" in direct_dweh,
        bucket="SUPPORT",
    )
    check(
        "Current-bank nonrealization note says the bank realizes neither Wilson -> D_- nor Wilson -> dW_e^H under another name",
        "does **not** already contain the missing" in nonreal
        and "Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem" in nonreal,
        bucket="SUPPORT",
    )

    check(
        "Two-route current-bank closure note records that the honest upstream step-2A route space is exhausted by exactly the strong and compressed routes",
        "route space is exhausted by exactly two routes" in note
        and "`Wilson -> D_-`" in note
        and "`Wilson -> dW_e^H`" in note,
    )
    check(
        "Two-route current-bank closure note records that the current bank realizes neither surviving route",
        "current exact bank already realizes neither route" in note,
    )
    check(
        "Two-route current-bank closure note records that the next science is positive construction rather than more route taxonomy",
        "next science is positive construction" in note
        and "not more route taxonomy" in note,
        detail="route-analysis phase is now closed",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
