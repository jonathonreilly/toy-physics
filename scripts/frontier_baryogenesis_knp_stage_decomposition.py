#!/usr/bin/env python3
"""
Baryogenesis K_NP stage decomposition on the current main package surface.

This runner packages the next honest reduction after the exact flavor
factorization eta = J * K_NP:

  K_NP = K_EWPT * K_tr * K_sph

where the three factors are the transition-history, transport, and
sphaleron-survival stages of the same retained nonperturbative electroweak
route.
"""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS = 0
FAIL = 0

ETA_OBS = 6.12e-10
J_PROMOTED = 3.330901e-5
K_NP_TARGET = ETA_OBS / J_PROMOTED
K_EQUAL_SPLIT = K_NP_TARGET ** (1.0 / 3.0)
K_TWO_STAGE_SPLIT = math.sqrt(K_NP_TARGET)


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"  [{tag}] {name}")
    if detail:
        print(f"         {detail}")


def info(name: str, detail: str = "") -> None:
    print(f"  [INFO] {name}")
    if detail:
        print(f"         {detail}")


def reconstruct_eta(j: float, k_ewpt: float, k_tr: float, k_sph: float) -> float:
    return j * k_ewpt * k_tr * k_sph


def stage_split(j: float, eta: float, k_tr: float, k_sph: float) -> float:
    if j == 0.0 or k_tr == 0.0 or k_sph == 0.0:
        return 0.0
    return eta / (j * k_tr * k_sph)


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS K_NP STAGE DECOMPOSITION")
    print("=" * 80)
    print()
    print("Question:")
    print("  After eta = J * K_NP is fixed, what exact same-surface")
    print("  nonperturbative electroweak object still remains to be computed?")
    print()

    print("=" * 80)
    print("PART 1: EXACT STAGE DECOMPOSITION")
    print("=" * 80)
    print()

    sample_triplets = [
        (K_EQUAL_SPLIT, K_EQUAL_SPLIT, K_EQUAL_SPLIT),
        (1.0, K_TWO_STAGE_SPLIT, K_TWO_STAGE_SPLIT),
        (K_NP_TARGET, 1.0, 1.0),
    ]

    for idx, (k_ewpt, k_tr, k_sph) in enumerate(sample_triplets, start=1):
        eta = reconstruct_eta(J_PROMOTED, k_ewpt, k_tr, k_sph)
        k_ewpt_back = stage_split(J_PROMOTED, eta, k_tr, k_sph)
        label = f"sample decomposition {idx}"
        check(
            f"{label} reconstructs eta exactly",
            abs(eta - J_PROMOTED * k_ewpt * k_tr * k_sph) < 1e-20,
            f"eta = {eta:.6e}",
        )
        check(
            f"{label} inverts exactly back to K_EWPT",
            abs(k_ewpt_back - k_ewpt) < 1e-18,
            f"K_EWPT(back) = {k_ewpt_back:.6e}",
        )

    zero_cases = [
        (0.0, 0.3, 0.2),
        (0.2, 0.0, 0.3),
        (0.2, 0.3, 0.0),
    ]
    for idx, (k_ewpt, k_tr, k_sph) in enumerate(zero_cases, start=1):
        eta = reconstruct_eta(J_PROMOTED, k_ewpt, k_tr, k_sph)
        check(
            f"zero-stage case {idx} kills the final asymmetry",
            eta == 0.0,
            f"eta = {eta:.1e}",
        )

    info(
        "stage meaning",
        "the exact open electroweak object is not one opaque symbol anymore: it is the product of transition-history, transport, and sphaleron-survival stages",
    )
    print()

    print("=" * 80)
    print("PART 2: TARGET GEOMETRY")
    print("=" * 80)
    print()

    print(f"  K_NP,target            = {K_NP_TARGET:.6e}")
    print(f"  equal three-stage split = {K_EQUAL_SPLIT:.6e}")
    print(f"  one ideal, two equal    = {K_TWO_STAGE_SPLIT:.6e}")
    print(f"  two ideal, one limiting = {K_NP_TARGET:.6e}")
    print()

    check(
        "equal three-stage split reconstructs the target product",
        abs(K_EQUAL_SPLIT ** 3 - K_NP_TARGET) < 1e-18,
        f"(K_NP)^(1/3) = {K_EQUAL_SPLIT:.6e}",
    )
    check(
        "one ideal stage leaves the other two at sqrt(K_NP)",
        abs(K_TWO_STAGE_SPLIT ** 2 - K_NP_TARGET) < 1e-18,
        f"sqrt(K_NP) = {K_TWO_STAGE_SPLIT:.6e}",
    )
    check(
        "if all three normalized stage factors were larger than the equal-split value, the target would be overshot",
        (K_EQUAL_SPLIT * 1.0001) ** 3 > K_NP_TARGET,
        f"(1.0001 * K_eq)^3 = {(K_EQUAL_SPLIT * 1.0001) ** 3:.6e}",
    )
    check(
        "any candidate with transport and sphaleron factors both at 10% would force a sub-percent transition-history factor",
        K_NP_TARGET / (0.1 * 0.1) < 0.01,
        f"K_EWPT <= {K_NP_TARGET / (0.1 * 0.1):.6e}",
    )
    info(
        "benchmark meaning",
        "future same-surface calculations can now be scored stage by stage instead of only against one undifferentiated K_NP target",
    )
    print()

    print("=" * 80)
    print("PART 3: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    knp_note = (DOCS / "BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md").read_text(
        encoding="utf-8"
    )
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    fact_note = (DOCS / "BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md").read_text(
        encoding="utf-8"
    )
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(
        encoding="utf-8"
    )
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")
    flagship = (DOCS / "CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md").read_text(
        encoding="utf-8"
    )

    check(
        "stage-decomposition note records K_NP = K_EWPT * K_tr * K_sph",
        "`K_NP = K_EWPT * K_tr * K_sph`" in knp_note,
    )
    check(
        "closure-gate note points to the stage-decomposition note",
        "BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md" in gate_note,
    )
    check(
        "factorization note remains upstream of the stage decomposition",
        "`η = J * K_NP`" in fact_note,
    )
    check(
        "derivation atlas carries the stage-decomposition row",
        "Baryogenesis K_NP stage decomposition" in atlas,
    )
    check(
        "canonical harness index includes the stage-decomposition runner",
        "frontier_baryogenesis_knp_stage_decomposition.py" in harness,
    )
    check(
        "current flagship entrypoint points to the stage-decomposition note",
        "BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md" in flagship,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the exact open electroweak object is")
    print("      K_NP = K_EWPT * K_tr * K_sph")
    print("    - the retained weak-flavor source remains fully closed in J")
    print("    - the stage target product is")
    print(f"      K_EWPT * K_tr * K_sph = {K_NP_TARGET:.6e}")
    print("    - future same-surface work can now be judged stage by stage")
    print("      against explicit target geometry instead of a single opaque symbol")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
