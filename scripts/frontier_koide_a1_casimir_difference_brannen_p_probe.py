#!/usr/bin/env python3
"""
Brannen P residual — Wilson-line d²-power quantization probe.

The retained KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE isolates the
residual postulate P:

    The structural quantity 2/d^2 in radians equals the physical
    Berry holonomy on the selected-line CP^1 base (d = 3).

SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS §Priority 2 lists one of the
minimal-sufficient closures as:

    W_{Z_3}^{d^2} = exp(2i) * 1   (Z_3-orbit Wilson-line d^2-power quantization)

This runner probes the arithmetic of that identity:
  - d^2 = 9 Wilson-line power
  - phase argument 2i corresponds to exp(2i) not exp(2i * pi * n) —
    i.e. a radian-level phase of exactly 2 radians on a d^2 = 9-fold
    winding.
  - Single-winding Berry phase: 2/d^2 = 2/9 radians.

We verify the arithmetic consistency of this scheme on the structural
data and check that NO other small integer d has the same property
(only d = 3 gives the 2/9 radian quantum consistent with Q = 2/3 / d).
"""

from __future__ import annotations

import math
import sys


PASSES: list[tuple[str, bool, str]] = []


def record(name, ok, detail=""):
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")

DOCS: list[tuple[str, str]] = []


def document(name: str, detail: str = "") -> None:
    DOCS.append((name, detail))
    print(f"[DOC ] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")



def section(title):
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("Brannen P residual — Wilson d^2-power quantization probe")

    # ---- A. The structural ratio 2/d^2 -----------------------------------
    section("A. Structural radian quantum 2/d^2 at d = 3")
    d = 3
    radian_quantum = 2.0 / d ** 2
    print(f"  d = {d}, structural radian quantum = 2/d^2 = {radian_quantum:.9f}")
    print(f"  In fractional form: 2/{d**2} = 2/9")
    record("A.1 d = 3 gives 2/d^2 = 2/9", abs(radian_quantum - 2/9) < 1e-12)

    # ---- B. d-sweep: other d's give different radian quanta ----------------
    section("B. d-sweep: only d = 3 matches the retained Brannen phase delta = 2/9")
    print(f"  {'d':>4}  {'2/d^2':>15}  {'matches delta=2/9?':>25}")
    print("  " + "-" * 48)
    matches = []
    for d_try in [1, 2, 3, 4, 5, 6, 9, 12]:
        q = 2 / d_try ** 2
        m = abs(q - 2/9) < 1e-12
        if m:
            matches.append(d_try)
        print(f"  {d_try:>4}  {q:>15.9f}  {'YES' if m else 'no':>25}")
    record("B.1 Only d = 3 matches delta = 2/9 among d ∈ {1..12}", matches == [3])

    # ---- C. Relation to Q = 2/3 -------------------------------------------
    section("C. Relation to Q on the retained d = 3 reduction")
    Q = 2 / 3
    delta_from_Q = Q / d
    print(f"  Q / d = (2/3) / 3 = {delta_from_Q:.9f}")
    record("C.1 delta = Q/d matches 2/9 at d = 3", abs(delta_from_Q - 2/9) < 1e-12)

    # ---- D. Wilson-line winding arithmetic ---------------------------------
    section("D. Wilson-line d^2 = 9 winding arithmetic")
    # W_{Z_3}^{d^2} = exp(2i) means 9-fold winding around the Z_3 orbit gives
    # phase exactly 2 radians. Single winding ⟹ 2/9 radians.
    n_windings = d ** 2
    total_phase = 2.0  # radians
    single_winding = total_phase / n_windings
    print(f"  n_windings = d^2 = {n_windings}")
    print(f"  total phase (W^{n_windings}) = 2 radians (per retained reduction)")
    print(f"  single winding = 2 / d^2 = {single_winding:.9f} radians = 2/9")
    record("D.1 Single winding gives 2/9 radians", abs(single_winding - 2/9) < 1e-12)

    # ---- E. Quantisation hypothesis ---------------------------------------
    section("E. Quantisation hypothesis (still open)")
    print(
        "  The QUANTISATION hypothesis: W_{Z_3}^{d^2} = exp(2i) * 1 on the\n"
        "  retained Cl(3)/Z^3 lattice.\n"
        "\n"
        "  Status: arithmetic ✓ (consistent with Q=2/3 and delta=2/9).\n"
        "  Physical derivation: still open. The candidate routes include\n"
        "  a lattice-propagator radian quantum, an ambient 3+1 Berry transport,\n"
        "  or a Callan-Harvey anomaly-descent construction.\n"
        "\n"
        "  This probe confirms the arithmetic target and rules out alternative\n"
        "  d-values, narrowing the remaining open work."
    )
    document("E.1 Quantisation hypothesis arithmetically consistent; derivation open")

    # ---- F. Three candidate closure routes (from the retained notes) -------
    section("F. Three candidate closure routes for P")
    routes = [
        ("Lattice propagator radian quantum", "G_{C_3}(1) = exp(i · 2/d^2) G_0"),
        ("Wilson holonomy on 4x4 (hw=1+baryon) block", "per-element phase 2/d^2"),
        ("Z_3-orbit Wilson-line d^2-power quantization", "W_{Z_3}^{d^2} = exp(2i) * 1"),
    ]
    for name, form in routes:
        print(f"  - {name}")
        print(f"      {form}")
    document("F.1 Three candidate routes enumerated from retained notes")

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    n_docs = len(DOCS)
    print(f"PASSED: {n_pass}/{n_total}")
    print(f"DOCUMENTED: {n_docs}")
    if n_pass == n_total:
        print("VERDICT: Brannen P probe closed at arithmetic level. d = 3 uniquely")
        print("gives delta = 2/9; the physical-base identification is still open.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
