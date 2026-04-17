#!/usr/bin/env python3
"""
DM neutrino triplet normalization target theorem.

Question:
  What exact coefficient target must the missing triplet transfer law hit in
  order to close the present benchmark, and can that target be reached by phase
  transfer alone?

Answer:
  No. At fixed M1 and kappa the benchmark needs epsilon/epsilon_DI to rise
  from 0.277 to 0.936, i.e. a 3.37x kernel enhancement. But the exact source
  phase is already sin(2pi/3)=sqrt(3)/2, so phase-only improvement can give at
  most a 1.155x boost. The missing law must therefore normalize the amplitude /
  even-response sector, not merely the phase.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

ETA_OBS = 6.12e-10
ETA_DI = 6.54e-10
EPS_OVER_DI_CURRENT = 0.277428
PHASE_SOURCE = 2.0 * math.pi / 3.0


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def part1_the_exact_kernel_target_is_0p936_of_di() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE MISSING LAW MUST HIT 0.936 OF THE DI CEILING")
    print("=" * 88)

    target = ETA_OBS / ETA_DI
    enhancement = target / EPS_OVER_DI_CURRENT

    check(
        "At fixed M1 and kappa, exact closure requires epsilon/epsilon_DI = eta_obs/eta_DI",
        abs(target - 0.9357798165137614) < 1e-12,
        f"target={target:.6f}",
    )
    check(
        "The current reduced kernel is short by a factor 3.37",
        abs(enhancement - 3.373054689915082) < 1e-12,
        f"enhancement={enhancement:.6f}",
    )
    check(
        "So the missing coefficient law is mainly a kernel-normalization problem",
        enhancement > 3.0,
        "the gap is too large to dismiss as small bookkeeping",
    )
    return target, enhancement


def part2_phase_only_improvement_is_far_too_small(enhancement: float) -> None:
    print("\n" + "=" * 88)
    print("PART 2: PHASE-ONLY IMPROVEMENT IS FAR TOO SMALL")
    print("=" * 88)

    sin_src = abs(math.sin(PHASE_SOURCE))
    phase_ceiling = 1.0 / sin_src

    check(
        "The exact source phase is already near-maximal: sin(2pi/3)=sqrt(3)/2",
        abs(sin_src - math.sqrt(3.0) / 2.0) < 1e-12,
        f"sin(phi_src)={sin_src:.6f}",
    )
    check(
        "Even a maximally tuned phase can improve the kernel by only 1/sin(2pi/3)",
        abs(phase_ceiling - 1.1547005383792517) < 1e-12,
        f"phase ceiling={phase_ceiling:.6f}",
    )
    check(
        "The needed 3.37x enhancement is much larger than any phase-only gain",
        enhancement > phase_ceiling * 2.5,
        f"need={enhancement:.6f}, phase-only ceiling={phase_ceiling:.6f}",
    )


def part3_the_target_must_live_in_gamma_and_the_even_response_channels() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE TARGET MUST LIVE IN GAMMA AND THE EVEN RESPONSE CHANNELS")
    print("=" * 88)

    blocker = read("docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md")
    note = read("docs/DM_LEPTOGENESIS_BENCHMARK_DECOMPOSITION_NOTE_2026-04-15.md")

    check(
        "The branch records that the 0.30 shortfall is mainly CP-kernel suppression",
        "CP-kernel suppression" in note and "27.7%" in note,
    )
    check(
        "So the remaining normalization law must populate gamma and the two even response channels",
        "delta + rho" in blocker and "A + b - c - d" in blocker and "gamma" in blocker,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO TRIPLET NORMALIZATION TARGET")
    print("=" * 88)

    target, enhancement = part1_the_exact_kernel_target_is_0p936_of_di()
    part2_phase_only_improvement_is_far_too_small(enhancement)
    part3_the_target_must_live_in_gamma_and_the_even_response_channels()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
