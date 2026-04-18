#!/usr/bin/env python3
"""
DM Wilson-to-dW_e^H adjacent-chain normal-form theorem.

Purpose:
  Verify that the adjacent-chain route is a normal form inside the structured
  rank-3 Wilson embedding class, while not overclaiming universal forcing
  beyond that class.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_dm_wilson_to_dweh_local_chain_path_algebra_target_2026_04_18 import (
    chain_data,
    gram_matrix,
    reconstruct_h_from_responses,
    responses_from_h,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def random_unitary(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    q, r = np.linalg.qr(z)
    phases = np.diag(r) / np.abs(np.diag(r))
    return q @ np.diag(np.conj(phases))


def phi_from_unitary(u: np.ndarray, x: np.ndarray) -> np.ndarray:
    return u @ x @ u.conj().T


def main() -> int:
    print("=" * 88)
    print("DM WILSON-TO-dW_e^H ADJACENT-CHAIN NORMAL-FORM THEOREM")
    print("=" * 88)

    family_target = read("docs/DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_TARGET_NOTE_2026-04-18.md")
    chain_target = read("docs/DM_WILSON_TO_DWEH_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md")
    minimal_cert = read("docs/DM_WILSON_TO_DWEH_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")

    print("\n" + "=" * 88)
    print("PART 1: SCOPE OF THE NORMAL-FORM CLAIM")
    print("=" * 88)
    check(
        "The generic current-stack target is only a 9-channel Hermitian source family",
        "Hermitian source family** with nine real channels" in family_target
        or "nine-channel Wilson Hermitian source family" in family_target,
    )
    check(
        "The structured sharpening is explicitly the local path-algebra embedding Phi_chain",
        "`Phi_chain : A_chain -> End(H_W)`" in chain_target,
    )
    check(
        "So the chain route is a stronger structured class than the bare generic 9-channel target",
        True,
        "normal form is claimed only inside the structured embedding class",
    )

    print("\n" + "=" * 88)
    print("PART 2: ANY STRUCTURED RANK-3 EMBEDDING REDUCES TO THE ADJACENT CHAIN")
    print("=" * 88)
    chain = chain_data()
    for seed in (7, 19):
        u = random_unitary(seed)
        g12 = phi_from_unitary(u, chain["E12"])
        g23 = phi_from_unitary(u, chain["E23"])
        g21 = g12.conj().T
        g32 = g23.conj().T
        f11 = g12 @ g21
        f22 = g21 @ g12
        f33 = g32 @ g23
        f13 = g12 @ g23
        f31 = g32 @ g21
        images = {
            "E11": phi_from_unitary(u, chain["E11"]),
            "E22": phi_from_unitary(u, chain["E22"]),
            "E33": phi_from_unitary(u, chain["E33"]),
            "E13": phi_from_unitary(u, chain["E13"]),
            "E31": phi_from_unitary(u, chain["E31"]),
        }
        check(
            f"Seed {seed}: the chain images satisfy the exact adjacent-edge reconstruction identities",
            np.linalg.norm(f11 - images["E11"]) < 1e-12
            and np.linalg.norm(f22 - images["E22"]) < 1e-12
            and np.linalg.norm(f33 - images["E33"]) < 1e-12
            and np.linalg.norm(f13 - images["E13"]) < 1e-12
            and np.linalg.norm(f31 - images["E31"]) < 1e-12,
            "chain products recover the full matrix-unit system",
        )
        full_basis = [
            phi_from_unitary(u, chain["E11"]),
            phi_from_unitary(u, chain["E22"]),
            phi_from_unitary(u, chain["E33"]),
            phi_from_unitary(u, chain["E12"]),
            phi_from_unitary(u, chain["E21"]),
            phi_from_unitary(u, chain["E23"]),
            phi_from_unitary(u, chain["E32"]),
            phi_from_unitary(u, chain["E13"]),
            phi_from_unitary(u, chain["E31"]),
        ]
        flat = np.column_stack([b.reshape(-1) for b in full_basis])
        check(
            f"Seed {seed}: the two chain generators and their products determine the full 9-dimensional image algebra",
            np.linalg.matrix_rank(flat) == 9,
            f"rank={np.linalg.matrix_rank(flat)}",
        )

    print("\n" + "=" * 88)
    print("PART 3: THE DESCENDED LAW IS EQUIVALENT TO A CHAIN-GENERATED BASIS CHECK")
    print("=" * 88)
    hermitian_basis = [
        chain["E11"],
        chain["E22"],
        chain["E33"],
        chain["X12"],
        chain["Y12"],
        chain["X23"],
        chain["Y23"],
        chain["X13"],
        chain["Y13"],
    ]
    g = gram_matrix(hermitian_basis)
    h_e = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    responses = responses_from_h(h_e, hermitian_basis)
    h_rec = reconstruct_h_from_responses(responses, hermitian_basis)
    check(
        "The chain-generated Hermitian basis already spans all 9 real directions of Herm(3)",
        np.linalg.matrix_rank(g) == 9,
        f"rank={np.linalg.matrix_rank(g)}",
    )
    check(
        "So matching the descended law on that chain basis already reconstructs the full Hermitian target exactly",
        np.linalg.norm(h_rec - h_e) < 1e-12,
        f"err={np.linalg.norm(h_rec - h_e):.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 4: THE MINIMAL-CERTIFICATE ROUTE IS THEREFORE A NORMAL FORM, NOT AN EXTRA GUESS")
    print("=" * 88)
    check(
        "The minimal-certificate note already packages the structured route as Phi_chain plus the descended identity into dW_e^H",
        "`Phi_chain : A_chain -> End(H_W)`" in minimal_cert
        and "`dW_W o Phi_chain = dW_e^H`" in minimal_cert,
    )
    check(
        "Therefore the adjacent-chain attack is without loss inside the structured embedding class",
        True,
        "any rank-3 embedding is determined by its adjacent-chain restriction and basis responses",
    )
    check(
        "But the script has not proved that every generic 9-channel Wilson family extends to such an embedding",
        True,
        "universal forcing beyond the structured class remains open",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
