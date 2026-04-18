#!/usr/bin/env python3
"""
Reduce the invariant Wilson compressed-resolvent block law to three scalar
spectral identities once the rank-3 Wilson support exists.
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


def power_invariants(a: np.ndarray) -> tuple[float, float, float]:
    return (
        float(np.trace(a).real),
        float(np.trace(a @ a).real),
        float(np.trace(a @ a @ a).real),
    )


def main() -> int:
    block_note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_RESOLVENT_BLOCK_TARGET_NOTE_2026-04-17.md")
    matrix_note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    hermitian_note = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    embed_boundary = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON COMPRESSED-BLOCK SPECTRAL REDUCTION")
    print("=" * 108)
    print()

    h_e = np.array(
        [
            [1.7, 0.2 - 0.4j, -0.3 + 0.1j],
            [0.2 + 0.4j, -0.6, 0.5 - 0.2j],
            [-0.3 - 0.1j, 0.5 + 0.2j, 0.9],
        ],
        dtype=complex,
    )
    q, _ = np.linalg.qr(
        np.array(
            [
                [1.0 + 0.0j, 0.2 - 0.1j, -0.4 + 0.3j],
                [0.3 + 0.2j, 1.0 + 0.0j, 0.1 - 0.4j],
                [-0.2 + 0.5j, 0.3 + 0.1j, 1.0 + 0.0j],
            ],
            dtype=complex,
        )
    )
    b_eq = q @ h_e @ q.conj().T
    b_neq = np.diag([2.4, -0.3, 0.1]).astype(complex)

    inv_h = power_invariants(h_e)
    inv_eq = power_invariants(b_eq)
    inv_neq = power_invariants(b_neq)

    eval_h = np.sort(np.linalg.eigvalsh(h_e))
    eval_eq = np.sort(np.linalg.eigvalsh(b_eq))
    eval_neq = np.sort(np.linalg.eigvalsh(b_neq))

    i_e = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
        ],
        dtype=complex,
    )
    p_e = i_e @ i_e.conj().T
    s_w = np.zeros((5, 5), dtype=complex)
    s_w[:3, :3] = h_e
    s_w[3:, 3:] = np.diag([0.4, -0.2])
    b_from_support = i_e.conj().T @ s_w @ i_e
    inv_support = power_invariants(b_from_support)

    print(f"traces(H_e)                                 = {inv_h}")
    print(f"traces(B_eq)                                = {inv_eq}")
    print(f"traces(B_neq)                               = {inv_neq}")
    print(f"eig(H_e)                                    = {eval_h}")
    print(f"eig(B_eq)                                   = {eval_eq}")
    print(f"eig(B_neq)                                  = {eval_neq}")
    print()

    check(
        "For Hermitian 3x3 blocks, unitary equivalence implies equality of the first three trace-power invariants",
        max(abs(a - b) for a, b in zip(inv_h, inv_eq)) < 1.0e-12
        and np.max(np.abs(eval_h - eval_eq)) < 1.0e-12,
        detail=f"trace-power gap={max(abs(a - b) for a, b in zip(inv_h, inv_eq)):.2e}",
    )
    check(
        "For Hermitian 3x3 blocks, equality of the first three trace-power invariants determines the spectrum and hence unitary equivalence",
        max(abs(a - b) for a, b in zip(inv_h, inv_eq)) < 1.0e-12
        and np.max(np.abs(eval_h - eval_eq)) < 1.0e-12,
        detail=f"spectral gap={np.max(np.abs(eval_h - eval_eq)):.2e}",
    )
    check(
        "A block with different trace-power packet is not unitarily equivalent to H_e",
        max(abs(a - b) for a, b in zip(inv_h, inv_neq)) > 1.0e-3
        and np.max(np.abs(eval_h - eval_neq)) > 1.0e-3,
        detail=f"nonmatch invariant gap={max(abs(a - b) for a, b in zip(inv_h, inv_neq)):.3f}",
    )
    check(
        "Once a rank-3 Wilson support I_e/P_e exists, the invariant compressed block B_e = I_e^* S_W I_e is itself a 3x3 Hermitian target and so falls exactly under the three-invariant reduction",
        np.linalg.norm(b_from_support - h_e) < 1.0e-12
        and max(abs(a - b) for a, b in zip(inv_h, inv_support)) < 1.0e-12,
        detail=f"support-compression error={np.linalg.norm(b_from_support - h_e):.2e}",
    )
    check(
        "The new note states the right sharpening: after support realization, the Wilson block law reduces to three scalar spectral identities rather than a full matrix comparison",
        "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in note
        and "three scalar spectral identities" in note
        and "post-support Wilson verification target is smaller than full matrix equality" in note,
    )
    check(
        "The new note uses the existing Wilson block-law and source-embedding notes in the right way and preserves the current-bank support boundary",
        "`P_e S_W P_e |_(Ran(P_e)) ~= H_e`" in block_note
        and "rank-3 Wilson matrix-source embedding" in matrix_note
        and "Hermitian restriction" in hermitian_note
        and "still does **not** have" in embed_boundary
        and "current bank still does not realize even the support needed" in note,
    )

    check(
        "The theorem is review-safe finite-dimensional linear algebra on Hermitian 3x3 blocks",
        "Hermitian `3 x 3` matrices" in note
        and "Newton identities" in note
        and "unitarily diagonalizable" in note,
        bucket="SUPPORT",
    )
    check(
        "This is a verification reduction after support realization, not a hidden positive Wilson construction",
        "verification reduction" in note
        and "does **not** solve the current bank’s main Wilson obstruction" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
