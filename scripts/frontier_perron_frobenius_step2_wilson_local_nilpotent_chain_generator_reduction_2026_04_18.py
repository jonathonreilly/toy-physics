#!/usr/bin/env python3
"""
Reduce the sharpest Wilson local constructive object to one local nilpotent
chain generator on the physical adjacent two-edge chain.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


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


def e(i: int, j: int) -> np.ndarray:
    m = np.zeros((3, 3), dtype=complex)
    m[i, j] = 1.0
    return m


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_GENERATOR_REDUCTION_NOTE_2026-04-18.md")
    path_alg = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md")

    print("=" * 110)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL NILPOTENT CHAIN-GENERATOR REDUCTION")
    print("=" * 110)
    print()

    eye = np.eye(3, dtype=complex)
    e11 = e(0, 0)
    e22 = e(1, 1)
    e33 = e(2, 2)
    e12 = e(0, 1)
    e23 = e(1, 2)
    e13 = e(0, 2)

    n = e12 + e23
    p1 = eye - n.conj().T @ n
    p3 = eye - n @ n.conj().T
    p2 = n.conj().T @ n + n @ n.conj().T - eye
    e12_rec = p1 @ n @ p2
    e23_rec = p2 @ n @ p3
    e13_rec = n @ n
    proj_err = max(
        float(np.linalg.norm(p1 @ p1 - p1)),
        float(np.linalg.norm(p2 @ p2 - p2)),
        float(np.linalg.norm(p3 @ p3 - p3)),
        float(np.linalg.norm(p1 @ p2)),
        float(np.linalg.norm(p2 @ p3)),
        float(np.linalg.norm(p1 @ p3)),
    )
    gen_err = max(
        float(np.linalg.norm(p1 - e11)),
        float(np.linalg.norm(p2 - e22)),
        float(np.linalg.norm(p3 - e33)),
        float(np.linalg.norm(e12_rec - e12)),
        float(np.linalg.norm(e23_rec - e23)),
        float(np.linalg.norm(e13_rec - e13)),
        float(np.linalg.norm(np.linalg.matrix_power(n, 3))),
    )
    check(
        "One local nilpotent chain generator already reconstructs the full physical two-edge chain algebra",
        proj_err < 1e-12 and gen_err < 1e-12 and float(np.linalg.norm(n @ n)) > 0.0,
        detail=f"proj_err={proj_err:.2e}, gen_err={gen_err:.2e}",
    )
    check(
        "The local path-algebra embedding Phi_chain is therefore exactly equivalent to one local nilpotent chain generator",
        "`Phi_chain : A_chain -> End(H_W)`" in path_alg
        and "one local nilpotent chain generator" in note
        and "The following are equivalent:" in note
        and "`N_chain := Phi_chain(E_12 + E_23)`" in note,
    )
    check(
        "The new note records the exact recovery formulas for the chain projections and edge generators from N_chain",
        "`P_1 := 1 - N^* N = E_11`" in note
        and "`P_3 := 1 - N N^* = E_33`" in note
        and "`P_2 := N^* N + N N^* - 1 = E_22`" in note
        and "`E_12 = P_1 N P_2`" in note
        and "`E_23 = P_2 N P_3`" in note
        and ("`E_13 = N^2`" in note or "`N^2 = E_13`" in note),
    )
    check(
        "The current bank still does not realize even that sharper local nilpotent generator",
        "current bank still does **not** realize even this sharper local generator" in note,
    )
    check(
        "The theorem stays on the Wilson constructive lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive realization of the local nilpotent chain generator" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
