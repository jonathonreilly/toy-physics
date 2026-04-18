#!/usr/bin/env python3
"""Reduction of the live strong-route D_- target to the active off-seed
five-real source on the charged-lepton branch."""

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
    note = read("docs/PERRON_FROBENIUS_STEP2_ACTIVE_FIVE_REAL_TARGET_NOTE_2026-04-17.md")
    active = read("docs/DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md")
    d_last = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md")
    strong = read("docs/PERRON_FROBENIUS_STEP2_STRONG_ROUTE_BREAKING_SOURCE_TARGET_NOTE_2026-04-17.md")
    direct = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 ACTIVE FIVE-REAL D_- TARGET")
    print("=" * 108)
    print()

    check(
        "PMNS active-projector reduction note says the one-sided transport-facing object already reduces to the active five-real source",
        "remaining PMNS-relevant object is exactly the active five-real" in active
        or "remaining DM-relevant PMNS object is exactly the active five-real" in active,
        bucket="SUPPORT",
    )
    check(
        "PMNS microscopic D last-mile note says the remaining D-level object is the active off-seed 5-real source",
        "remaining `D`-level object is only the active `5`-real breaking source" in d_last
        and "(xi_1, xi_2, eta_1, eta_2, delta)" in d_last,
        bucket="SUPPORT",
    )
    check(
        "PF strong-route target note says Wilson -> D_- is already reduced to that same off-seed breaking-source law",
        "off-seed breaking-source law" in strong
        and "`Wilson -> D_-`" in strong,
        bucket="SUPPORT",
    )
    check(
        "PF direct-dW_e^H route reduction note says the compressed route already factors through the smaller charged projected-source law dW_e^H",
        "direct `dW_e^H` route already matches the smallest honest PMNS-side" in direct
        and "microscopic last-mile object on the active charged-lepton branch" in direct,
        bucket="SUPPORT",
    )

    check(
        "Active five-real target note records that the smallest live D_-level step-2A target is exactly the active off-seed five-real source",
        "smallest live `D_-`-level target on step 2A is exactly the" in note
        and "off-seed `5`-real source" in note,
    )
    check(
        "Active five-real target note records that the compressed route already factors further while the strong route is pinned to this packet",
        "smaller charged Hermitian projected-source" in note
        and "smallest live target on the strong" in note
        and "`Wilson -> D_-`" in note,
    )
    check(
        "Active five-real target note records that larger D_-side unknowns are no longer honest live targets",
        "larger `D_-`-side unknowns are no longer honest live targets" in note
        and "full pair law" in note
        and "full PMNS matrix law" in note,
        detail="next constructive benchmark is now one exact data packet",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
