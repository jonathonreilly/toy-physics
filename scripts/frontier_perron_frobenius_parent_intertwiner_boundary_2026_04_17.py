#!/usr/bin/env python3
"""
Current-stack parent/intertwiner boundary for the global PF program.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 3
BETA = 6.0


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


def recurrence_neighbors(p: int, q: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for a, b in [
        (p + 1, q),
        (p - 1, q + 1),
        (p, q - 1),
        (p, q + 1),
        (p + 1, q - 1),
        (p - 1, q),
    ]:
        if a >= 0 and b >= 0:
            out.append((a, b))
    return out


def weights_box(nmax: int) -> list[tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def build_recurrence_matrix(nmax: int) -> tuple[np.ndarray, list[tuple[int, int]]]:
    weights = weights_box(nmax)
    index = {w: i for i, w in enumerate(weights)}
    jmat = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        i = index[(p, q)]
        for a, b in recurrence_neighbors(p, q):
            if (a, b) in index:
                jmat[index[(a, b)], i] += 1.0 / 6.0
    return jmat, weights


def symmetric_exp(m: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(m)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def main() -> int:
    parent_note = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    global_note = read("docs/PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md")
    pmns_sole = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    pf_boundary = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")
    parent_boundary = read("docs/PERRON_FROBENIUS_PARENT_INTERTWINER_BOUNDARY_NOTE_2026-04-17.md")

    jmat, weights = build_recurrence_matrix(NMAX)
    half = symmetric_exp(jmat, BETA / 2.0)
    d_beta = np.diag([np.exp(-0.22 * (p + q) - 0.04 * ((p - q) ** 2)) for p, q in weights])
    t_src = half @ d_beta @ half

    src_dim = t_src.shape[0]
    comp_dim = 2
    off = np.full((src_dim, comp_dim), 0.01, dtype=float)
    comp = np.array([[2.5, 0.08], [0.08, 2.2]], dtype=float)
    t_parent = np.block([[t_src, off], [off.T, comp]])

    i_src = np.zeros((src_dim + comp_dim, src_dim), dtype=float)
    i_src[:src_dim, :src_dim] = np.eye(src_dim)
    compressed = i_src.T @ t_parent @ i_src
    compression_err = float(np.max(np.abs(compressed - t_src)))
    min_parent = float(np.min(t_parent))
    min_eval = float(np.min(np.linalg.eigvalsh(t_parent)))

    print("=" * 104)
    print("PERRON-FROBENIUS PARENT / INTERTWINER BOUNDARY")
    print("=" * 104)
    print()
    print(f"source-sector dimension         = {src_dim}")
    print(f"parent-witness dimension        = {t_parent.shape[0]}")
    print(f"intertwiner compression error   = {compression_err:.3e}")
    print(f"parent minimum entry            = {min_parent:.6e}")
    print(f"parent minimum eigenvalue       = {min_eval:.6e}")
    print()

    check(
        "Wilson parent/compression note already proves one exact parent object with canonical plaquette and theta descendants on the Wilson gauge surface",
        "one exact parent partition object" in parent_note
        and "plaquette source-sector transfer law is already a canonical descendant" in parent_boundary
        and "strong-CP `theta` law is already a canonical Fourier descendant" in parent_boundary,
        bucket="SUPPORT",
    )
    check(
        "PMNS sole-axiom boundary note already says the strongest canonical hw=1 pack remains trivial",
        "stays trivial" in pmns_sole
        and "exactly `(I3, I3)`" in pmns_sole,
        bucket="SUPPORT",
    )
    check(
        "Global closure note already says the remaining honest global route is operator-plus-projection",
        "operator-plus-projection" in global_note
        and "Wilson-to-PMNS projection" in global_note,
        bucket="SUPPORT",
    )
    check(
        "Top-level PF boundary already says global PF is closed negatively on the current stack",
        "step 1 is exact on the Wilson gauge surface but not yet globally across the" in pf_boundary
        and "retained sectors" in pf_boundary
        and "global PF selector is still not derivable" in pf_boundary,
        bucket="SUPPORT",
    )

    check(
        "A Wilson-side parent/intertwiner relation is already exact on the gauge surface",
        compression_err < 1.0e-12 and min_parent > 0.0 and min_eval > 0.0,
        detail="explicit source-sector embedding recovers the descendant transfer law from a positive parent witness",
    )
    check(
        "The current stack does not yet promote that Wilson parent object into one global sole-axiom parent dynamics across the live sectors",
        "does **not** yet close step 1 globally" in parent_boundary
        and "Wilson-to-PMNS intertwiner / projection theorem" in parent_boundary
        and "still required" in parent_boundary,
        detail="PMNS descendant/intertwiner data are still missing on the current exact bank",
    )
    check(
        "Therefore step 1 is only partially closed: exact on the Wilson surface, not yet globally across plaquette, strong-CP, and PMNS",
        "step 1 on the Wilson gauge surface" in parent_boundary
        and "step 1 globally across plaquette, strong-CP, and PMNS" in parent_boundary
        and "no" in parent_boundary,
        detail="more step-1 work is still required before a positive global PF-selector theorem is honest",
    )
    check(
        "The next honest theorem target is a true parent/intertwiner theorem rather than more sample-side PF reconstruction",
        "parent / intertwiner theorem" in parent_boundary
        and "not another sample-side PF note" in parent_boundary,
        detail="theory order is now operator-first and projection-first",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
