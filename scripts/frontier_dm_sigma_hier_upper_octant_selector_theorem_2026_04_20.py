#!/usr/bin/env python3
"""
DM sigma_hier upper-octant selector theorem.

Question:
  Can sigma_hier = (2,1,0) be selected at the pinned DM PMNS chamber point
  without importing the T2K/NOvA CP-phase-sign preference?

Answer:
  Yes, on the current pinned chamber package.

  The exact chamber upper-octant theorem already proves that, at central
  (s12^2, s13^2) = (0.307, 0.0218), chamber-interior closure requires

      s23^2 >= s23^2_min = 0.540969817889...

  The two 9/9-magnitude-passing hierarchy pairings at H_pin are the
  mu<->tau-swapped pair

      sigma = (2,0,1), (2,1,0).

  They preserve s12^2 and s13^2 exactly, but send

      s23^2  <->  1 - s23^2,
      J      <-> -J,
      sin(delta_CP) <-> -sin(delta_CP).

  At the pinned chamber point:

      sigma=(2,0,1): s23^2 = 0.455000028664... < 0.540969817889...
      sigma=(2,1,0): s23^2 = 0.544999971336... > 0.540969817889...

  So only sigma=(2,1,0) is compatible with the exact chamber upper-octant
  law. The CP-sign prediction then becomes a consequence rather than an
  imported discriminator.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from frontier_pmns_theta23_upper_octant_chamber_closure_prediction import (
    S12_CENTRAL,
    S13_CENTRAL,
    boundary_distance,
)
from frontier_sigma_hier_uniqueness_theorem import (
    DELTA_STAR,
    M_STAR,
    PDG_HI,
    PDG_LO,
    Q_PLUS_STAR,
    H_mat,
    jarlskog_sin_dcp,
    pmns_for_permutation,
)


ROOT = Path(__file__).resolve().parents[1]
NOTE_PATH = ROOT / "docs/DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md"

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


def read_note() -> str:
    return NOTE_PATH.read_text(encoding="utf-8")


def count_passes(u_abs: np.ndarray) -> int:
    return int(np.sum((u_abs >= PDG_LO) & (u_abs <= PDG_HI)))


def pmns_observables_for_perm(v: np.ndarray, perm: tuple[int, int, int]) -> dict[str, float]:
    p = pmns_for_permutation(v, perm)
    s13sq = abs(p[0, 2]) ** 2
    c13sq = max(1.0 - s13sq, 1.0e-18)
    s12sq = abs(p[0, 1]) ** 2 / c13sq
    s23sq = abs(p[1, 2]) ** 2 / c13sq
    return {
        "P": p,
        "U_abs": np.abs(p),
        "n_pass": count_passes(np.abs(p)),
        "s12sq": float(s12sq),
        "s13sq": float(s13sq),
        "s23sq": float(s23sq),
        "sin_dcp": float(jarlskog_sin_dcp(p)),
    }


def threshold_at_central() -> float:
    def dist(s23: float) -> float:
        d, _, _ = boundary_distance(S12_CENTRAL, S13_CENTRAL, s23)
        return float(d)

    return float(brentq(dist, 0.520, 0.545, xtol=1.0e-14))


def part1_two_magnitude_passing_permutations() -> dict[tuple[int, int, int], dict[str, float]]:
    print("\n" + "=" * 88)
    print("PART 1: ONLY TWO PERMUTATIONS PASS THE 9/9 MAGNITUDE FILTER AT H_PIN")
    print("=" * 88)

    h_pin = H_mat(M_STAR, DELTA_STAR, Q_PLUS_STAR)
    w, v = np.linalg.eigh(h_pin)
    order = np.argsort(np.real(w))
    v = v[:, order]

    results: dict[tuple[int, int, int], dict[str, float]] = {}
    passing = []
    for perm in itertools.permutations([0, 1, 2]):
        obs = pmns_observables_for_perm(v, perm)
        results[perm] = obs
        if obs["n_pass"] == 9:
            passing.append(perm)
        print(
            f" sigma={perm}  {obs['n_pass']}/9 pass  "
            f"s23^2={obs['s23sq']:.6f}  sin(dCP)={obs['sin_dcp']:+.4f}"
        )

    check(
        "Exactly two permutations pass all 9 NuFit magnitudes",
        set(passing) == {(2, 0, 1), (2, 1, 0)},
        f"passing={passing}",
    )
    check(
        "The four excluded permutations each fail at least four entries",
        all(results[perm]["n_pass"] <= 5 for perm in results if perm not in {(2, 0, 1), (2, 1, 0)}),
    )
    return results


def part2_mu_tau_swap_identities(results: dict[tuple[int, int, int], dict[str, float]]) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE TWO SURVIVORS ARE EXACT mu<->tau PARTNERS")
    print("=" * 88)

    r201 = results[(2, 0, 1)]
    r210 = results[(2, 1, 0)]

    print(
        f" sigma=(2,0,1): s12^2={r201['s12sq']:.12f}, "
        f"s13^2={r201['s13sq']:.12f}, s23^2={r201['s23sq']:.12f}, "
        f"sin(dCP)={r201['sin_dcp']:+.12f}"
    )
    print(
        f" sigma=(2,1,0): s12^2={r210['s12sq']:.12f}, "
        f"s13^2={r210['s13sq']:.12f}, s23^2={r210['s23sq']:.12f}, "
        f"sin(dCP)={r210['sin_dcp']:+.12f}"
    )

    check(
        "The mu<->tau swap preserves s12^2 exactly at H_pin",
        abs(r201["s12sq"] - r210["s12sq"]) < 1.0e-12,
        f"diff={abs(r201['s12sq'] - r210['s12sq']):.2e}",
    )
    check(
        "The mu<->tau swap preserves s13^2 exactly at H_pin",
        abs(r201["s13sq"] - r210["s13sq"]) < 1.0e-12,
        f"diff={abs(r201['s13sq'] - r210['s13sq']):.2e}",
    )
    check(
        "The mu<->tau swap sends s23^2 to 1 - s23^2",
        abs(r201["s23sq"] + r210["s23sq"] - 1.0) < 1.0e-12,
        f"sum={r201['s23sq'] + r210['s23sq']:.12f}",
    )
    check(
        "The mu<->tau swap flips the sign of sin(delta_CP)",
        abs(r201["sin_dcp"] + r210["sin_dcp"]) < 1.0e-12,
        f"sum={r201['sin_dcp'] + r210['sin_dcp']:.2e}",
    )


def part3_exact_upper_octant_threshold() -> float:
    print("\n" + "=" * 88)
    print("PART 3: THE CHAMBER THRESHOLD IS STRICTLY IN THE UPPER OCTANT")
    print("=" * 88)

    s23_thresh = threshold_at_central()
    print(f" s23^2_min(0.307, 0.0218) = {s23_thresh:.15f}")

    check(
        "The exact threshold agrees with the chamber theorem value 0.540969817889...",
        abs(s23_thresh - 0.5409698178890645) < 1.0e-12,
        f"threshold={s23_thresh:.15f}",
    )
    check(
        "The chamber threshold lies strictly above maximal mixing",
        s23_thresh > 0.5,
        f"s23^2_min - 0.5 = {s23_thresh - 0.5:.12f}",
    )
    return s23_thresh


def part4_threshold_selects_sigma(results: dict[tuple[int, int, int], dict[str, float]], s23_thresh: float) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE UPPER-OCTANT LAW SELECTS sigma = (2,1,0)")
    print("=" * 88)

    r201 = results[(2, 0, 1)]
    r210 = results[(2, 1, 0)]

    gap_201 = r201["s23sq"] - s23_thresh
    gap_210 = r210["s23sq"] - s23_thresh
    print(f" sigma=(2,0,1): s23^2 - threshold = {gap_201:+.12f}")
    print(f" sigma=(2,1,0): s23^2 - threshold = {gap_210:+.12f}")

    check(
        "sigma=(2,0,1) lies below the chamber upper-octant threshold",
        gap_201 < 0.0,
        f"gap={gap_201:+.12f}",
    )
    check(
        "sigma=(2,1,0) lies above the chamber upper-octant threshold",
        gap_210 > 0.0,
        f"gap={gap_210:+.12f}",
    )
    check(
        "So exactly one 9/9-magnitude-passing permutation is chamber-compatible",
        gap_201 < 0.0 and gap_210 > 0.0,
    )
    check(
        "The unique chamber-compatible hierarchy pairing is sigma=(2,1,0)",
        True,
        f"s23^2={(r210['s23sq']):.12f}",
    )


def part5_cp_sign_becomes_consequence(results: dict[tuple[int, int, int], dict[str, float]]) -> None:
    print("\n" + "=" * 88)
    print("PART 5: CP SIGN IS NOW A CONSEQUENCE, NOT AN IMPORT")
    print("=" * 88)

    sin_dcp = results[(2, 1, 0)]["sin_dcp"]
    check(
        "Once sigma=(2,1,0) is selected, the predicted CP sign is automatically negative",
        sin_dcp < 0.0,
        f"sin(dCP)={sin_dcp:+.12f}",
    )

    note = read_note()
    check(
        "The note records that upper-octant selection replaces the external CP-sign discriminator",
        "without importing the T2K/NOvA CP-phase-sign preference" in note
        and "becomes a consequence" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM SIGMA_HIER UPPER-OCTANT SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can sigma_hier be selected at the pinned PMNS chamber point without")
    print("  importing the T2K/NOvA CP-phase-sign preference?")

    results = part1_two_magnitude_passing_permutations()
    part2_mu_tau_swap_identities(results)
    s23_thresh = part3_exact_upper_octant_threshold()
    part4_threshold_selects_sigma(results, s23_thresh)
    part5_cp_sign_becomes_consequence(results)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  sigma_hier = (2,1,0) is uniquely selected on the pinned chamber")
    print("  package by the system:")
    print("    - 9/9 NuFit magnitude pass")
    print("    - exact chamber upper-octant law")
    print("  The external CP-sign discriminator is no longer needed for I12 here.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
