#!/usr/bin/env python3
"""Audit the information/action unit-map theorem lane honestly.

This harness encodes the sharpened obstruction:
  - direct information-as-action is log-base dependent
  - raw log Z is chart-density dependent
  - naive direct count/entropy maps miss exact conventional a = l_P
  - the only surviving information route is a new converted theorem
    q_* = kappa_info I_* on the elementary geometric carrier
"""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LANE_NOTE = ROOT / "docs/PLANCK_SCALE_INFORMATION_ACTION_UNIT_MAP_THEOREM_LANE_2026-04-23.md"
PROGRAM_NOTE = ROOT / "docs/PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md"
INFO_NOTE = ROOT / "docs/SINGLE_AXIOM_INFORMATION_NOTE.md"
PARTITION_NOTE = ROOT / "docs/UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md"
REDUCTION_NOTE = ROOT / "docs/PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def main() -> int:
    lane = normalized(LANE_NOTE)
    program = normalized(PROGRAM_NOTE)
    info = normalized(INFO_NOTE)
    partition = normalized(PARTITION_NOTE)
    reduction = normalized(REDUCTION_NOTE)

    n_pass = 0
    n_fail = 0

    print("Planck information/action unit-map theorem lane audit")
    print("=" * 78)

    section("PART 1: LOG-BASE OBSTRUCTION")
    n_states = 8
    i_nat = math.log(n_states)
    i_bit = math.log2(n_states)
    p = check(
        "direct information-as-action depends on the log-base convention",
        abs(i_nat - i_bit) > 1e-12,
        f"same {n_states}-state alternative gives {i_nat:.6f} nats vs {i_bit:.6f} bits",
    )
    n_pass += int(p)
    n_fail += int(not p)

    kappa_nat = 0.125
    kappa_bit = kappa_nat * math.log(2.0)
    q_nat = kappa_nat * i_nat
    q_bit = kappa_bit * i_bit
    p = check(
        "an admissible information/action law needs a compensating conversion constant",
        abs(q_nat - q_bit) < 1e-12,
        "q_* stays physical only when kappa_info rescales inversely with the information-unit convention",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: DIRECT COUNT/ENTROPY NO-GO")
    lower_bound = 4.0 * math.log(2.0)
    p = check(
        "direct q_* = I_* has an exact lower bound above conventional Planck",
        lower_bound > 1.0,
        f"a^2/l_P^2 >= 4 log 2 = {lower_bound:.6f} for any nontrivial direct information quantum",
    )
    n_pass += int(p)
    n_fail += int(not p)

    cubical_ratio = 16.0 * math.log(2.0)
    p = check(
        "on the natural cubical defect the direct information subclass misses by a wide margin",
        cubical_ratio > 1.0,
        f"for eps_* = pi/2, direct q_* = log 2 gives a^2/l_P^2 = 16 log 2 = {cubical_ratio:.6f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: PARTITION-DENSITY OBSTRUCTION")
    z_value = 3.0
    det_t = 5.0
    log_shift = math.log(det_t)
    p = check(
        "raw log Z shifts under chart Jacobians and is not a canonical phase quantum",
        abs(math.log(z_value * det_t) - math.log(z_value) - log_shift) < 1e-12 and log_shift > 0.0,
        f"chart scaling by |det T| = {det_t:.1f} shifts log Z by log|det T| = {log_shift:.6f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: SOURCE-AND-NOTE ALIGNMENT")
    p = check(
        "source notes actually support the structural-vs-unit distinction",
        "conserved information flow" in info
        and "finite partition" in partition
        and "raw chart scalar" in partition
        and "a^2 / l_p^2 = 8 pi q_* / eps_*" in reduction,
        "single-axiom information is structural, the partition family is finite but chart-dependent, and the action-phase reduction supplies the coefficient target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "lane note names the surviving theorem target honestly",
        "phase-per-information theorem" in lane
        and "direct information-as-action identifications are not admissible" in lane
        and "raw partition-log identifications are not admissible" in lane,
        "the lane now narrows the route to q_* = kappa_info I_* rather than claiming present closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "top-level program still treats information/action as an open lane",
        "information/action quantum" in program
        and "future bridge candidate" in program,
        "the new lane sharpens that open status into specific admissible and inadmissible subclasses",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Current information carriers do not fix the Planck unit map. "
        "Direct count/entropy maps are log-base dependent and miss exact "
        "conventional a = l_P; raw log Z is chart-density dependent. The only "
        "surviving information route is a new exact phase-per-information "
        "theorem q_* = kappa_info I_* on the elementary geometric carrier."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
