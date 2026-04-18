#!/usr/bin/env python3
"""
Reduction of the strong Wilson->D_- route to the off-seed breaking-source law
on the active charged-lepton branch.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_STRONG_ROUTE_BREAKING_SOURCE_TARGET_NOTE_2026-04-17.md")
    microscopic_target = read("docs/PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md")
    d_last = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md")
    direct_dweh = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 STRONG-ROUTE BREAKING-SOURCE TARGET")
    print("=" * 108)
    print()

    check(
        "Step-2 microscopic-channel target note identifies Wilson -> D_- as the cleanest strong target",
        "Wilson-to-charged microscopic channel" in microscopic_target
        and "Wilson-to-`D_-` law" in microscopic_target,
        bucket="SUPPORT",
    )
    check(
        "PMNS microscopic D last-mile note says the aligned seed patch is already exact but insufficient and the active branch is genuinely off-seed",
        "aligned weak-axis seed patch is" in d_last
        and "already positively closed at the `D` level" in d_last
        and "genuinely" in d_last
        and "off-seed:" in d_last,
        bucket="SUPPORT",
    )
    check(
        "PMNS microscopic D last-mile note reduces the remaining D-level object to the off-seed 5-real breaking source",
        "remaining `D`-level object is only the active `5`-real breaking source" in d_last
        and "(xi_1, xi_2, eta_1, eta_2, delta)" in d_last,
        bucket="SUPPORT",
    )
    check(
        "Direct dW_e^H route reduction note says the compressed route matches the smallest honest PMNS-side microscopic last-mile object",
        "direct `dW_e^H` route already matches the smallest honest" in direct_dweh
        and "PMNS-side" in direct_dweh
        and "microscopic target on the active charged-lepton branch" in direct_dweh,
        bucket="SUPPORT",
    )

    check(
        "Strong-route breaking-source target note records that the live strong-route content is only the off-seed breaking-source law beyond the aligned seed patch",
        "live strong-route content is only the" in note
        and "off-seed breaking-source law" in note
        and "aligned seed patch" in note,
    )
    check(
        "Strong-route breaking-source target note records that the strong route is reduced to a sharply typed breaking-source target rather than an unconstrained full-operator search",
        "sharply" in note
        and "typed breaking-source target" in note
        and "unconstrained full-operator search" in note,
    )
    check(
        "Strong-route breaking-source target note records that the strong and compressed routes can share the same live off-seed microscopic work packet",
        "same live off-seed breaking-source content" in note
        and "strong and compressed routes are not disagreeing" in note,
        detail="strong-route construction target is now much narrower",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
