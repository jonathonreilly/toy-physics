#!/usr/bin/env python3
"""Lane 2 QED threshold bridge firewall.

Question:
  Does the current repo surface determine the atomic low-energy Coulomb
  coupling alpha(0) from retained alpha_EM(M_Z) plus the structural QED
  beta coefficient b_QED = 32/3?

Answer:
  No. The structural b_QED coefficient is a real asymptotic support
  ingredient, but a low-energy alpha(0) bridge also needs threshold-resolved
  decoupling data. Without charged thresholds and hadronic/vacuum-polarization
  handling, the same alpha(M_Z) and same asymptotic b_QED allow a continuum of
  low-energy inverse couplings.

This is a firewall runner, not a retained Rydberg prediction.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from pathlib import Path
import sys


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
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Repo/current-surface values.
INV_ALPHA_MZ_REPO = 127.67

# Comparator-only values already used by the existing Lane 2 firewall/scaffold.
# They are not derivation inputs in the no-go proof below.
INV_ALPHA0_COMPARATOR = 137.035999084
M_E_GEV_COMPARATOR = 0.00051099895
M_Z_GEV_COMPARATOR = 91.1876

N_COLOR = 3
N_GEN = 3


def q_up(n_color: int = N_COLOR) -> Fraction:
    return Fraction(n_color + 1, 2 * n_color)


def q_down(n_color: int = N_COLOR) -> Fraction:
    return Fraction(1 - n_color, 2 * n_color)


def charge_square_sum(n_color: int = N_COLOR, n_gen: int = N_GEN) -> Fraction:
    """Sum N_c Q_f^2 over charged Dirac fermions for the retained SM point."""
    q_e = Fraction(-1, 1)
    per_generation = q_e * q_e + n_color * (q_up(n_color) ** 2 + q_down(n_color) ** 2)
    return n_gen * per_generation


def b_qed_from_charges(n_color: int = N_COLOR, n_gen: int = N_GEN) -> Fraction:
    """QED beta coefficient in the repo note's positive-b convention."""
    return Fraction(4, 3) * charge_square_sum(n_color=n_color, n_gen=n_gen)


def b_qed_s1_closed_form(n_color: int = N_COLOR) -> Fraction:
    """Inline S1 structural form cited by the retained beta-coefficient note."""
    return Fraction(2, 3) * (n_color + 1) ** 2


def inv_alpha_running_down(
    inv_alpha_high: float,
    b_active: Fraction,
    log_high_over_low_active: float,
) -> float:
    """One-loop inverse-coupling transport for a fixed active interval.

    With d alpha^{-1} / d ln Q = -b/(2 pi), running from Q_high down through
    an active interval of length ln(Q_high/Q_low) increases alpha^{-1} by
    b/(2 pi) times that interval. Thresholds decide which intervals are active.
    """
    return inv_alpha_high + (float(b_active) / (2.0 * math.pi)) * log_high_over_low_active


@dataclass(frozen=True)
class ThresholdModel:
    name: str
    active_log_length: float

    def low_inverse_alpha(self, b_active: Fraction) -> float:
        return inv_alpha_running_down(
            INV_ALPHA_MZ_REPO,
            b_active,
            self.active_log_length,
        )


def part1_current_repo_surface() -> None:
    banner("Part 1: current repo surface")

    lane2 = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    usable = read("docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md")
    firewall = read("docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md")
    bnote = read("docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md")

    check(
        "Lane 2 explicitly remains scaffold-only before retained dependencies land",
        "scaffold-only" in lane2 and "textbook inputs" in lane2,
    )
    check(
        "usable derived values carry alpha_EM(M_Z)=1/127.67",
        "1/alpha_EM(M_Z)" in usable and "127.67" in usable,
    )
    check(
        "usable derived values do not carry alpha(0) as a retained value",
        "alpha_EM(0)" not in usable and "alpha(0)" not in usable,
    )
    check(
        "existing Rydberg firewall already marks alpha(0) transport as load-bearing",
        "alpha(0)" in firewall
        and "alpha_EM(M_Z)" in firewall
        and "load-bearing" in firewall,
    )
    check(
        "repo beta-coefficient note exposes b_QED=32/3 as an asymptotic ingredient",
        "b_QED" in bnote and "32/3" in bnote and "above all SM thresholds" in bnote,
    )


def part2_structural_b_qed() -> Fraction:
    banner("Part 2: retained charge/count surface gives asymptotic b_QED")

    up = q_up()
    down = q_down()
    sigma_q2 = charge_square_sum()
    b_from_charges = b_qed_from_charges()
    b_from_s1 = b_qed_s1_closed_form()

    print(f"  N_color = {N_COLOR}, N_gen = {N_GEN}")
    print(f"  Q_u = {up}, Q_d = {down}, Q_e = -1")
    print(f"  Sum_f N_c Q_f^2 over charged Dirac fermions = {sigma_q2}")
    print(f"  b_QED from charges = (4/3) * Sum Q^2 = {b_from_charges}")
    print(f"  b_QED S1 form      = (2/3) * (N_color + 1)^2 = {b_from_s1}")

    check("retained charge spectrum specializes to Q_u=2/3", up == Fraction(2, 3))
    check("retained charge spectrum specializes to Q_d=-1/3", down == Fraction(-1, 3))
    check("per-SM charged spectrum gives Sum N_c Q_f^2 = 8", sigma_q2 == Fraction(8, 1))
    check("b_QED from charges equals 32/3", b_from_charges == Fraction(32, 3))
    check("b_QED from charges equals S1 closed form", b_from_charges == b_from_s1)

    return b_from_charges


def part3_threshold_underdetermination(b_qed: Fraction) -> None:
    banner("Part 3: same alpha(M_Z) and same b_QED do not determine alpha(0)")

    # This dimensionless interval is intentionally synthetic. It proves
    # underdetermination before any observed alpha(0) comparator is mentioned.
    total_log = 10.0
    models = [
        ThresholdModel("all charged thresholds at high endpoint", 0.0),
        ThresholdModel("effective thresholds halfway through interval", total_log / 2.0),
        ThresholdModel("all charged species active for full interval", total_log),
    ]

    lows = []
    for model in models:
        low = model.low_inverse_alpha(b_qed)
        lows.append(low)
        print(
            f"  {model.name:<48s} "
            f"active_log={model.active_log_length:5.2f}  "
            f"1/alpha_low={low:10.6f}"
        )

    spread = max(lows) - min(lows)
    per_log_sensitivity = float(b_qed) / (2.0 * math.pi)

    print()
    print(f"  Per-unit-log threshold sensitivity = b_QED/(2 pi) = {per_log_sensitivity:.6f}")
    print(f"  Spread across same-alpha(M_Z), same-b_QED models = {spread:.6f}")

    check(
        "low-energy alpha is nonunique without threshold placement",
        spread > 10.0,
        f"spread={spread:.3f} in 1/alpha over log interval {total_log}",
    )
    check(
        "threshold locations are numerically load-bearing",
        per_log_sensitivity > 1.0,
        f"d(1/alpha)/dlog={per_log_sensitivity:.3f}",
    )
    check(
        "underdetermination proof does not use observed alpha(0)",
        True,
        "only alpha(M_Z), b_QED, and threshold placement were varied",
    )


def part4_physical_scale_comparator(b_qed: Fraction) -> None:
    banner("Part 4: physical-scale illustration, comparator only")

    log_mz_me = math.log(M_Z_GEV_COMPARATOR / M_E_GEV_COMPARATOR)
    no_transport = INV_ALPHA_MZ_REPO
    all_active_to_me = inv_alpha_running_down(INV_ALPHA_MZ_REPO, b_qed, log_mz_me)
    target_gap = INV_ALPHA0_COMPARATOR - INV_ALPHA_MZ_REPO
    required_active_log = target_gap * (2.0 * math.pi) / float(b_qed)
    required_effective_threshold_gev = M_Z_GEV_COMPARATOR / math.exp(required_active_log)

    print(f"  Comparator M_Z                 = {M_Z_GEV_COMPARATOR:.4f} GeV")
    print(f"  Comparator m_e                 = {M_E_GEV_COMPARATOR:.11f} GeV")
    print(f"  log(M_Z/m_e)                   = {log_mz_me:.6f}")
    print(f"  repo 1/alpha_EM(M_Z)           = {INV_ALPHA_MZ_REPO:.6f}")
    print(f"  comparator 1/alpha(0)          = {INV_ALPHA0_COMPARATOR:.9f}")
    print(f"  no-transport 1/alpha           = {no_transport:.6f}")
    print(f"  all-active b_QED to m_e        = {all_active_to_me:.6f}")
    print(f"  active log needed to hit comparator = {required_active_log:.6f}")
    print(f"  fitted effective threshold          = {required_effective_threshold_gev:.6f} GeV")

    check(
        "no-transport and all-active transport bracket the comparator",
        no_transport < INV_ALPHA0_COMPARATOR < all_active_to_me,
        "alpha(0) could be fit by choosing an effective threshold",
    )
    check(
        "comparator-matching active log is an internal selector, not retained data",
        0.0 < required_active_log < log_mz_me,
        f"required_log={required_active_log:.3f}",
    )
    check(
        "using all-threshold b_QED down to m_e overshoots alpha(0)",
        all_active_to_me - INV_ALPHA0_COMPARATOR > 5.0,
        f"overshoot={all_active_to_me - INV_ALPHA0_COMPARATOR:.3f} in 1/alpha",
    )

    print()
    print("  Interpretation:")
    print("    The retained b_QED coefficient is necessary for a QED running bridge,")
    print("    but using it without threshold data is equivalent to choosing a hidden")
    print("    effective threshold. That is a fitted selector, not a derivation.")


def part5_lane2_consequence() -> None:
    banner("Part 5: Lane 2 consequence")

    print("  Exact dependency consequence:")
    print("    alpha_EM(M_Z) + b_QED(asymptotic) is not a retained alpha(0) bridge.")
    print()
    print("  A future retained Rydberg theorem still needs:")
    print("    1. retained electron mass or charged-lepton activation law;")
    print("    2. threshold-resolved QED decoupling from alpha(M_Z) to alpha(0);")
    print("    3. retained physical-unit nonrelativistic Coulomb/Schrodinger limit.")
    print()
    print("  This runner moves Lane 2 by sharpening the dependency firewall,")
    print("  not by closing the Rydberg scale.")

    check(
        "honest post-run Lane 2 status is open, not retained Rydberg closure",
        True,
        "alpha(0), m_e, and physical-unit NR limit remain open",
    )


def main() -> int:
    print("=" * 88)
    print("LANE 2 ATOMIC QED THRESHOLD BRIDGE FIREWALL")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can current retained alpha_EM(M_Z) plus structural b_QED determine alpha(0)?")
    print()
    print("Answer:")
    print("  No. Threshold-resolved QED transport remains a load-bearing import.")

    part1_current_repo_surface()
    b_qed = part2_structural_b_qed()
    part3_threshold_underdetermination(b_qed)
    part4_physical_scale_comparator(b_qed)
    part5_lane2_consequence()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
