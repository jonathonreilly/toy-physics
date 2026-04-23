#!/usr/bin/env python3
"""Audit the time-locked converted information/action constant lane honestly.

This lane does not derive Planck outright. It proves a sharper target:

  - the exact 3+1 time-lock forces the democratic four-state carrier
      p_* = (1/4, 1/4, 1/4, 1/4)
  - its canonical Shannon/vN information is exactly log 4 nats = 2 bits
  - therefore exact conventional a = l_P on the minimal cubical defect would
    require kappa_info = 1/(32 log 2) in natural units, equivalently 1/32 per bit
  - but the current retained stack still does not derive that conversion constant
"""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LANE_NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_TIMELOCKED_CONVERTED_INFORMATION_ACTION_CONSTANT_LANE_2026-04-23.md"
)
INFO_LANE = ROOT / "docs/PLANCK_SCALE_INFORMATION_ACTION_UNIT_MAP_THEOREM_LANE_2026-04-23.md"
TIMELOCK_LANE = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
REDUCTION_LANE = ROOT / "docs/PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md"
PARTITION_NOTE = ROOT / "docs/UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md"


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


def weights(beta: float) -> list[float]:
    total = 3.0 + beta
    return [1.0 / total, 1.0 / total, 1.0 / total, beta / total]


def shannon_nats(beta: float) -> float:
    probs = weights(beta)
    return -sum(p * math.log(p) for p in probs)


def shannon_closed(beta: float) -> float:
    return math.log(3.0 + beta) - (beta * math.log(beta)) / (3.0 + beta)


def shannon_derivative(beta: float) -> float:
    return -3.0 * math.log(beta) / (3.0 + beta) ** 2


def main() -> int:
    lane = normalized(LANE_NOTE)
    info_lane = normalized(INFO_LANE)
    timelock_lane = normalized(TIMELOCK_LANE)
    reduction_lane = normalized(REDUCTION_LANE)
    partition_note = normalized(PARTITION_NOTE)

    n_pass = 0
    n_fail = 0

    print("Planck time-locked converted information/action constant lane audit")
    print("=" * 78)

    section("PART 1: SOURCE-BOUNDARY ALIGNMENT")
    p = check(
        "time-lock source still fixes beta = 1 exactly",
        "beta = 1" in timelock_lane and "a_s = c a_t" in timelock_lane,
        "the new lane must inherit the exact spacetime lock rather than refit it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "earlier information lane still leaves only the converted theorem alive",
        "q_* = kappa_info i_*" in info_lane
        and "direct information-as-action identifications are not admissible" in info_lane
        and "raw partition-log identifications are not admissible" in info_lane,
        "the new lane is allowed to sharpen only the converted theorem target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "partition note still says raw log Z is chart-density dependent",
        "z'_gr = |det t| z_gr" in partition_note and "partition density / measure class" in partition_note,
        "time-lock cannot rescue the already-ruled-out raw partition-log route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "action-phase reduction still supplies the exact coefficient target",
        "a^2 / l_p^2 = 8 pi q_* / eps_*" in reduction_lane,
        "the converted constant must still feed the same elementary phase reduction",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT DEMOCRATIC 3+1 INFORMATION CARRIER")
    beta_values = [0.25, 0.5, 1.0, 2.0, 4.0]
    print("  beta       H(sum)              H(closed)           H'(beta)")
    for beta in beta_values:
        h_sum = shannon_nats(beta)
        h_closed = shannon_closed(beta)
        h_prime = shannon_derivative(beta)
        print(f"  {beta:>4.2f}   {h_sum:>16.12f}   {h_closed:>16.12f}   {h_prime:>16.12f}")
        p = check(
            f"closed entropy formula matches direct sum at beta={beta:g}",
            abs(h_sum - h_closed) < 1.0e-12,
            "I(beta) = log(3+beta) - beta log(beta)/(3+beta) is exact on the normalized 3+1 family",
        )
        n_pass += int(p)
        n_fail += int(not p)

    p = check(
        "beta = 1 is the unique entropy extremum on the positive anisotropic family",
        shannon_derivative(0.5) > 0.0
        and abs(shannon_derivative(1.0)) < 1.0e-15
        and shannon_derivative(2.0) < 0.0,
        "I'(beta) = -3 log(beta)/(3+beta)^2 changes sign only at the exact time-lock",
    )
    n_pass += int(p)
    n_fail += int(not p)

    h_star_nat = shannon_nats(1.0)
    p = check(
        "the locked carrier is exactly the democratic four-state carrier with I_* = log 4",
        all(abs(p_i - 0.25) < 1.0e-15 for p_i in weights(1.0))
        and abs(h_star_nat - math.log(4.0)) < 1.0e-15,
        f"beta=1 gives p_*=(1/4,1/4,1/4,1/4) and I_*={h_star_nat:.12f}=log 4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXACT TARGET CONSTANT ON THE LOCKED CARRIER")
    h_star_bits = h_star_nat / math.log(2.0)
    kappa_nat = 1.0 / (16.0 * h_star_nat)
    kappa_bits = kappa_nat * math.log(2.0)
    q_nat = kappa_nat * h_star_nat
    q_bits = kappa_bits * h_star_bits

    p = check(
        "locked-carrier information is exactly 2 bits",
        abs(h_star_bits - 2.0) < 1.0e-15,
        f"log 4 / log 2 = {h_star_bits:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "exact conventional Planck on eps_* = pi/2 reduces to kappa_info(bits) = 1/32",
        abs(kappa_bits - 1.0 / 32.0) < 1.0e-15
        and abs(kappa_nat - 1.0 / (32.0 * math.log(2.0))) < 1.0e-15,
        f"kappa_nat={kappa_nat:.12f}, kappa_bits={kappa_bits:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "base-compensated natural and bit conventions give the same elementary phase",
        abs(q_nat - 1.0 / 16.0) < 1.0e-15
        and abs(q_bits - q_nat) < 1.0e-15,
        f"q_* = kappa_nat log 4 = kappa_bits * 2 = {q_nat:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: TIME-LOCK DOES NOT FIX THE CONSTANT")
    lambdas = [0.25, 0.5, 1.0, 2.0, 4.0]
    values = []
    for lam in lambdas:
        a_s = lam
        c = 2.99792458e8
        a_t = a_s / c
        beta = (c * a_t / a_s) ** 2
        values.append((beta, shannon_nats(beta)))

    p = check(
        "the common spacetime scale ray leaves the locked information content unchanged",
        max(abs(beta - 1.0) for beta, _ in values) < 1.0e-15
        and max(abs(h - h_star_nat) for _, h in values) < 1.0e-15,
        "time-lock removes anisotropy but does not generate a new scale-dependent information coefficient",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "lane note states a sharp target constant rather than a fake closure",
        "kappa_info^(bit) = 1 / 32" in lane
        and "not yet a closure theorem" in lane
        and "time-lock fixes the democratic elementary information content" in lane,
        "the writeup should present this as theorem-grade narrowing, not as a derived Planck theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The exact time-lock fixes the minimal 3+1 information carrier to the "
        "democratic four-state carrier, so the canonical Shannon/vN content is "
        "log 4 nats = 2 bits. Exact conventional Planck on the minimal cubical "
        "defect would therefore require kappa_info = 1/(32 log 2) in natural "
        "units, equivalently 1/32 per bit. That is a sharp target constant, "
        "not yet a derived theorem."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
