#!/usr/bin/env python3
"""
Bounded endpoint-ratio chain candidate for the remaining quark E-channel law.

Status:
  theory-first bounded ratio-chain derivation candidate on the exact endpoint
  surface

Safe claim:
  The current branch still does not derive the exact Route-2 tensor readout
  law. But the endpoint data now support a sharper small-rational chain than
  the earlier standalone `15/8` quotient candidate.

  On the live endpoint surface:
    - `gamma_T(center) / gamma_T(shell)` is nearest to `5/6`;
    - `gamma_T(shell) / gamma_E(shell)` is nearest to `-2`;
    - `gamma_T(center) / gamma_E(center)` is nearest to `-8/9`.

  These three endpoint candidates imply

      gamma_E(center) / gamma_E(shell) = 15/8

  exactly by chain multiplication, and therefore reproduce the bounded
  E-channel quotient law `r_E = 21/4` and denominator candidate `D_E = 21/8`.

  This is still bounded candidate structure, not a theorem.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from frontier_quark_e_channel_endpoint_quotient_law import (
    anchored_a_u_from_denominator,
    check,
    percent_gap,
)
from frontier_quark_endpoint_readout_constraints import endpoint_readout
from frontier_quark_projector_parameter_audit import solve_anchored_surface
from frontier_quark_up_amplitude_candidate_scan import evaluate_candidate


PASS_COUNT = 0
FAIL_COUNT = 0
SMALL_Q_MAX = 32
SMALL_P_MAX = 96


@dataclass(frozen=True)
class RationalCandidate:
    label: str
    value: float
    numerator: int
    denominator: int
    rel_gap_percent: float


def nearest_rational(value: float, lower: float, upper: float) -> RationalCandidate:
    best: RationalCandidate | None = None
    seen: set[tuple[int, int]] = set()
    for q in range(1, SMALL_Q_MAX + 1):
        for p in range(-SMALL_P_MAX, SMALL_P_MAX + 1):
            if p == 0:
                continue
            g = math.gcd(abs(p), q)
            num = p // g
            den = q // g
            key = (num, den)
            if key in seen:
                continue
            seen.add(key)
            val = num / den
            if not (lower < val < upper):
                continue
            gap = percent_gap(val, value)
            cand = RationalCandidate(f"{num}/{den}", val, num, den, gap)
            if best is None or cand.rel_gap_percent < best.rel_gap_percent:
                best = cand
    assert best is not None
    return best


def local_check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def part1_live_endpoint_ratio_chain() -> tuple[float, float, float]:
    print("\n" + "=" * 72)
    print("PART 1: Exact Endpoint Ratio Chain")
    print("=" * 72)

    data = endpoint_readout()
    q_t = data.gamma_t_center / data.gamma_t_shell
    s_te = data.gamma_t_shell / data.gamma_e_shell
    c_te = data.gamma_t_center / data.gamma_e_center
    q_e = data.gamma_e_center / data.gamma_e_shell

    print(f"\n  gamma_T(center)/gamma_T(shell) = {q_t:.12f}")
    print(f"  gamma_T(shell)/gamma_E(shell)  = {s_te:.12f}")
    print(f"  gamma_T(center)/gamma_E(center)= {c_te:.12f}")
    print(f"  gamma_E(center)/gamma_E(shell) = {q_e:.12f}")
    print()
    print("  exact chain identity:")
    print("    gamma_E(center)/gamma_E(shell)")
    print("      = [gamma_E(center)/gamma_T(center)]")
    print("        * [gamma_T(center)/gamma_T(shell)]")
    print("        * [gamma_T(shell)/gamma_E(shell)]")

    chain_qe = (1.0 / c_te) * q_t * s_te

    local_check(
        "The endpoint E-quotient is fixed exactly by the three endpoint ratio factors",
        abs(chain_qe - q_e) < 1.0e-12,
        f"residual = {abs(chain_qe - q_e):.3e}",
    )
    local_check(
        "The T-chain factor remains the already-isolated exact-support candidate 5/6",
        percent_gap(q_t, 5.0 / 6.0) < 0.001,
        f"gap = {percent_gap(q_t, 5.0 / 6.0):.6f}%",
    )

    return q_t, s_te, c_te


def part2_small_rational_chain_candidates(q_t: float, s_te: float, c_te: float) -> tuple[RationalCandidate, RationalCandidate, RationalCandidate]:
    print("\n" + "=" * 72)
    print("PART 2: Controlled Small-Rational Chain Candidates")
    print("=" * 72)

    t_cand = nearest_rational(q_t, 0.7, 1.0)
    shell_cand = nearest_rational(s_te, -3.0, -1.0)
    center_cand = nearest_rational(c_te, -1.2, -0.6)

    print(f"\n  T endpoint candidate      = {t_cand.label:>5s} = {t_cand.value:+.12f}  gap = {t_cand.rel_gap_percent:.6f}%")
    print(f"  shell T/E candidate       = {shell_cand.label:>5s} = {shell_cand.value:+.12f}  gap = {shell_cand.rel_gap_percent:.6f}%")
    print(f"  center T/E candidate      = {center_cand.label:>5s} = {center_cand.value:+.12f}  gap = {center_cand.rel_gap_percent:.6f}%")

    local_check(
        "The T endpoint scan recovers 5/6",
        (t_cand.numerator, t_cand.denominator) == (5, 6),
        f"candidate = {t_cand.label}",
    )
    local_check(
        "The shell T/E scan selects -2",
        (shell_cand.numerator, shell_cand.denominator) == (-2, 1),
        f"candidate = {shell_cand.label}",
    )
    local_check(
        "The center T/E scan selects -8/9",
        (center_cand.numerator, center_cand.denominator) == (-8, 9),
        f"candidate = {center_cand.label}",
    )
    local_check(
        "Both shell and center T/E candidates stay within 0.3% of live endpoint ratios",
        shell_cand.rel_gap_percent < 0.3 and center_cand.rel_gap_percent < 0.3,
        (
            f"shell gap = {shell_cand.rel_gap_percent:.6f}%, "
            f"center gap = {center_cand.rel_gap_percent:.6f}%"
        ),
    )

    return t_cand, shell_cand, center_cand


def part3_implied_e_law(
    t_cand: RationalCandidate,
    shell_cand: RationalCandidate,
    center_cand: RationalCandidate,
) -> tuple[float, float]:
    print("\n" + "=" * 72)
    print("PART 3: Implied E-Channel Quotient and Denominator")
    print("=" * 72)

    q_e_chain = (1.0 / center_cand.value) * t_cand.value * shell_cand.value
    r_e_chain = 6.0 * (q_e_chain - 1.0)
    d_chain = r_e_chain / 2.0
    q_e_live = endpoint_readout().gamma_e_center / endpoint_readout().gamma_e_shell
    d_live = endpoint_readout().ratio_be_bt_abs

    print(f"\n  chain-implied E quotient      = {q_e_chain:.12f}")
    print(f"  chain-implied E ratio         = {r_e_chain:.12f}")
    print(f"  chain-implied denominator     = {d_chain:.12f}")
    print(f"  live E quotient               = {q_e_live:.12f}")
    print(f"  live bounded denominator      = {d_live:.12f}")

    local_check(
        "The rational ratio chain implies gamma_E(center)/gamma_E(shell) = 15/8 exactly",
        abs(q_e_chain - 15.0 / 8.0) < 1.0e-12,
        f"chain = {q_e_chain:.12f}",
    )
    local_check(
        "The rational ratio chain implies r_E = 21/4 exactly",
        abs(r_e_chain - 21.0 / 4.0) < 1.0e-12,
        f"chain = {r_e_chain:.12f}",
    )
    local_check(
        "The rational ratio chain implies the anchored denominator D_E = 21/8 exactly",
        abs(d_chain - 21.0 / 8.0) < 1.0e-12,
        f"chain = {d_chain:.12f}",
    )
    local_check(
        "The chain-implied E quotient stays within 0.1% of the live E quotient",
        percent_gap(q_e_chain, q_e_live) < 0.1,
        f"gap = {percent_gap(q_e_chain, q_e_live):.6f}%",
    )
    local_check(
        "The chain-implied denominator stays closer to the live bounded denominator than sqrt(7)",
        percent_gap(d_chain, d_live) < percent_gap(math.sqrt(7.0), d_live),
        (
            f"gap(21/8) = {percent_gap(d_chain, d_live):.6f}%, "
            f"gap(sqrt7) = {percent_gap(math.sqrt(7.0), d_live):.6f}%"
        ),
    )

    return q_e_chain, d_chain


def part4_anchored_quark_branch(d_chain: float) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Anchored Quark Branch")
    print("=" * 72)

    anchored = solve_anchored_surface()
    a_u_chain = anchored_a_u_from_denominator(d_chain)
    a_u_live = anchored_a_u_from_denominator(endpoint_readout().ratio_be_bt_abs)
    eval_chain = evaluate_candidate("21/8", "ratio-chain", a_u_chain, anchored.r_uc, anchored.r_ct)
    eval_live = evaluate_candidate("|b_E/b_T|", "bounded-endpoint", a_u_live, anchored.r_uc, anchored.r_ct)

    print(f"\n  chain-implied amplitude      = {a_u_chain:.12f}")
    print(f"  live bounded amplitude       = {a_u_live:.12f}")
    print(
        f"  chain anchor aggregate       = {eval_chain.anchor_aggregate:.6f}%"
        f"  (max = {eval_chain.anchor_max:.6f}%)"
    )
    print(
        f"  live anchor aggregate        = {eval_live.anchor_aggregate:.6f}%"
        f"  (max = {eval_live.anchor_max:.6f}%)"
    )

    local_check(
        "The ratio-chain denominator keeps the anchored CKM+J package below 1%",
        eval_chain.anchor_max < 1.0,
        f"anchor max = {eval_chain.anchor_max:.6f}%",
    )
    local_check(
        "The ratio-chain amplitude stays within 0.01% of the live bounded anchored amplitude",
        percent_gap(a_u_chain, a_u_live) < 0.01,
        f"gap = {percent_gap(a_u_chain, a_u_live):.6f}%",
    )
    local_check(
        "The ratio-chain anchored branch is numerically indistinguishable from the live bounded endpoint branch",
        abs(eval_chain.anchor_aggregate - eval_live.anchor_aggregate) < 0.001,
        (
            f"chain = {eval_chain.anchor_aggregate:.6f}%, "
            f"live = {eval_live.anchor_aggregate:.6f}%"
        ),
    )


def main() -> int:
    print("Quark endpoint ratio-chain law")
    print("=" * 72)

    q_t, s_te, c_te = part1_live_endpoint_ratio_chain()
    t_cand, shell_cand, center_cand = part2_small_rational_chain_candidates(q_t, s_te, c_te)
    _q_e_chain, d_chain = part3_implied_e_law(t_cand, shell_cand, center_cand)
    part4_anchored_quark_branch(d_chain)

    print("\nVerdict:")
    print(
        "The endpoint data now support a tighter theory-first chain than the "
        "standalone E-quotient candidate. The live tensor endpoint ratios are "
        "simultaneously nearest to the small rational set {5/6, -2, -8/9}. "
        "That chain forces gamma_E(center)/gamma_E(shell) = 15/8 and therefore "
        "reproduces the bounded E-channel law r_E = 21/4 and denominator "
        "candidate D_E = 21/8. So the theorem-grade target narrows again: the "
        "right next derivation problem is no longer an isolated E quotient, "
        "but the exact endpoint ratio chain itself."
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
