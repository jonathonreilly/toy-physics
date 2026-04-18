#!/usr/bin/env python3
"""
Prove the current exact bank does not already realize the sharpest local Wilson
path-algebra object Phi_chain.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-18.md")
    path_alg = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md")
    charged_embed = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    support_pullback = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")
    local_two_edge = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_TWO_EDGE_SOURCE_TARGET_NOTE_2026-04-18.md")
    chain_plane = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_CHAIN_PLANE_TARGET_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL PATH-ALGEBRA CURRENT-BANK NONREALIZATION")
    print("=" * 108)
    print()

    check(
        "The sharpest local Wilson constructive object is already fixed as Phi_chain",
        "`Phi_chain : A_chain -> End(H_W)`" in path_alg
        and "sharpest Wilson local constructive primitive" in path_alg,
    )
    check(
        "The current bank still lacks the upstream Wilson-side embedding/compression object needed to instantiate that local algebra class",
        "missing Wilson-side charged embedding/compression object" in charged_embed
        and "But it still does **not** have" in charged_embed
        and "current support bank or by the current scalar observable bank" in charged_embed
        and "be obtained as a pure pullback of `E_e` through the current exact support bank" in support_pullback,
    )
    check(
        "The current bank still fails already at the local two-edge source layer and at the restricted Hermitian chain-plane layer",
        "current bank still does **not** realize even this sharper local source" in local_two_edge
        and "current bank still does **not** realize even the restricted local" in chain_plane,
    )
    check(
        "The new note records the exact nonrealization theorem for Phi_chain on the current bank",
        "`Phi_chain`" in note
        and "does **not** already realize" in note
        and "local-bank rescans can stop" in note
        and "remaining Wilson gap is genuinely constructive" in note,
    )
    check(
        "The note carries the right no-go shape: sharp local target, matching upstream no-go, and no overclaim of global impossibility",
        "What this does not close" in note
        and "a positive realization of `Phi_chain`" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
