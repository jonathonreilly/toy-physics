#!/usr/bin/env python3
"""Check the link-local first-variation conditional algebra theorem."""

from pathlib import Path
import itertools
import re
import sys

try:
    import numpy as np
except ImportError:
    print("FAIL: numpy is required")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "LINK_LOCAL_FIRST_VARIATION_SELECTOR_BRIDGE_NARROW_THEOREM_NOTE_2026-05-10.md"

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"PASS: {label}" + (f" ({detail})" if detail else ""))
    else:
        FAIL += 1
        print(f"FAIL: {label}" + (f" ({detail})" if detail else ""))


AXES = ("t", "x", "y", "z")
DIM = 2 ** len(AXES)


def mask_for_subset(subset):
    mask = 0
    for axis in subset:
        mask |= 1 << AXES.index(axis)
    return mask


def hamming_weight(mask):
    return int(mask).bit_count()


def projector(mask):
    result = np.zeros((DIM, DIM), dtype=float)
    result[mask, mask] = 1.0
    return result


def main():
    all_subsets = [
        tuple(AXES[i] for i in range(len(AXES)) if (mask >> i) & 1)
        for mask in range(DIM)
    ]
    check("Boolean event-cell basis has 16 subset states", len(all_subsets) == 16)

    p_weight = {}
    expected_ranks = {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}
    for weight in range(5):
        p_weight[weight] = sum(projector(mask) for mask in range(DIM) if hamming_weight(mask) == weight)
        is_projector = np.allclose(p_weight[weight] @ p_weight[weight], p_weight[weight])
        is_self_adjoint = np.allclose(p_weight[weight].T, p_weight[weight])
        rank = int(round(float(np.trace(p_weight[weight]))))
        check(
            f"P_{weight} is a rank {expected_ranks[weight]} orthogonal projector",
            is_projector and is_self_adjoint and rank == expected_ranks[weight],
            f"rank={rank}",
        )

    source_vectors = {}
    for axis in AXES:
        mask = mask_for_subset((axis,))
        vector = np.zeros(DIM, dtype=float)
        vector[mask] = 1.0
        support = [i for i, value in enumerate(vector) if abs(value) > 1e-12]
        source_vectors[axis] = vector
        check(
            f"J_{axis} has one-axis support",
            support == [mask] and hamming_weight(mask) == 1,
            f"support={support}",
        )

    source_matrix = np.column_stack([source_vectors[axis] for axis in AXES])
    p_image = source_matrix @ source_matrix.T
    p1 = p_weight[1]
    p3 = p_weight[3]

    check("support projector of dS_link has rank four", int(round(float(np.trace(p_image)))) == 4)
    check("support projector of dS_link is orthogonal projector", np.allclose(p_image @ p_image, p_image) and np.allclose(p_image.T, p_image))
    check("support projector of dS_link equals P_1", np.allclose(p_image, p1))
    check("bridge hypothesis gives P_A = P_1", np.allclose(p_image, p1))
    check("P_3 is orthogonal to P_1", np.allclose(p3 @ p1, np.zeros((DIM, DIM))))
    check("P_3 is not the support projector of dS_link", not np.allclose(p3, p_image))

    rank_four_classes = [
        weight for weight, proj in p_weight.items()
        if int(round(float(np.trace(proj)))) == 4
    ]
    check("rank-four Hamming-weight classes are P_1 and P_3", rank_four_classes == [1, 3], str(rank_four_classes))
    check("P_1 and P_3 have equal rank but are distinct", int(round(float(np.trace(p1)))) == int(round(float(np.trace(p3)))) == 4 and not np.allclose(p1, p3))

    text = NOTE.read_text()
    check("note exists", NOTE.exists())
    check("note declares positive_theorem claim type", "**Claim type:** positive_theorem" in text)
    check("note keeps independent audit authority", "**Status authority:** independent audit lane only" in text)
    compact_text = re.sub(r"\s+", " ", text)
    check("note states hypotheses are not derived framework facts", "not derived framework facts" in compact_text)
    check("note has no markdown source-note dependency links", not re.search(r"\[[^\]]+\.md\]\(", text))
    check("note has no prefilled audit verdict vocabulary", "audited_conditional" not in text and "audited_clean" not in text)
    check("note has no bare A_min/A1/A2 framing", not re.search(r"\b(A_min|A1|A2)\b", text))

    print(f"PASS={PASS} FAIL={FAIL}")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
