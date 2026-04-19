#!/usr/bin/env python3
"""
Bounded CKM scalar-comparison bridge for the reduced up-sector quark amplitude.

Status:
  bounded scalar-comparison bridge / no-go on the exact-support quark anchor

Safe claim:
  The current branch still does not derive the remaining reduced up-sector
  amplitude `a_u` from the CKM scalar-comparison package alone.

  But the exact scalar-comparison package does more than provide one isolated
  candidate. Combined with the exact support anchor, it defines a natural
  bridge family

      a_u = sin(delta_std) * (1 - rho_scalar * kappa)

  with

      kappa in [sqrt(6/7), 1].

  Result:
    - the exact scalar package constrains the anchored branch to a narrow band;
    - a continuous scalar bridge beats the current external refit baseline on
      one kappa-window and beats the current external anchored baseline on a
      different kappa-window;
    - those two windows are disjoint;
    - the current theorem stack explicitly blocks promoting the scalar
      comparison surface to the bright/tensor `1 -> 3` theorem value.

  So this lane yields a sharp bounded bridge/no-go, not a retained derivation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from scipy.optimize import brentq, minimize_scalar

from frontier_quark_projector_parameter_audit import solve_anchored_surface
from frontier_quark_up_amplitude_candidate_scan import evaluate_candidate


PASS_COUNT = 0
FAIL_COUNT = 0

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = REPO_ROOT / "docs"
ATLAS_NOTE = DOC_ROOT / "CKM_ATLAS_AXIOM_CLOSURE_NOTE.md"
TENSOR_NOTE = DOC_ROOT / "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md"

SIN_DELTA_STD = math.sqrt(5.0 / 6.0)
RHO_SCALAR = 1.0 / math.sqrt(42.0)
ETA_SCALAR = math.sqrt(5.0 / 42.0)
RADIAL_SCALAR = 1.0 / math.sqrt(7.0)
KAPPA_CP = math.sqrt(6.0 / 7.0)


def check(name: str, condition: bool, detail: str = "") -> None:
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


def require_text(path: Path, snippets: tuple[str, ...]) -> bool:
    text = " ".join(path.read_text().split())
    return all(" ".join(snippet.split()) in text for snippet in snippets)


@dataclass(frozen=True)
class BridgeWindow:
    lower: float
    upper: float

    @property
    def width(self) -> float:
        return self.upper - self.lower


@dataclass(frozen=True)
class BridgeOptimum:
    kappa: float
    amplitude: float
    refit_objective: float
    anchor_aggregate: float
    refit_max: float
    anchor_max: float


@dataclass(frozen=True)
class BridgeSetup:
    anchor_r_uc: float
    anchor_r_ct: float
    anchored_a_u: float
    kappa_anchor: float
    lower_amplitude: float
    upper_amplitude: float
    baseline_refit: float
    baseline_anchor: float


def amplitude_from_kappa(kappa: float) -> float:
    return SIN_DELTA_STD * (1.0 - RHO_SCALAR * kappa)


def kappa_from_amplitude(amplitude: float) -> float:
    return (1.0 - amplitude / SIN_DELTA_STD) / RHO_SCALAR


def part1_exact_package() -> None:
    print("\n" + "=" * 72)
    print("PART 1: Exact Scalar-Comparison Bridge Data")
    print("=" * 72)

    print(f"\n  sin(delta_std)          = sqrt(5/6)   = {SIN_DELTA_STD:.12f}")
    print(f"  rho_scalar              = 1/sqrt(42)  = {RHO_SCALAR:.12f}")
    print(f"  eta_scalar              = sqrt(5/42)  = {ETA_SCALAR:.12f}")
    print(f"  radial scalar surface   = 1/sqrt(7)   = {RADIAL_SCALAR:.12f}")
    print(f"  kappa_cp                = sqrt(6/7)   = {KAPPA_CP:.12f}")
    print(f"  scalar lower bracket    = 1-rho_s     = {1.0 - RHO_SCALAR:.12f}")
    print(f"  scalar upper bracket    = 1-rho_s*kcp = {1.0 - RHO_SCALAR * KAPPA_CP:.12f}")
    print(f"  support fraction        = 6/7         = {6.0 / 7.0:.12f}")

    check(
        "Scalar-comparison radius is exactly sqrt(rho_scalar^2 + eta_scalar^2) = 1/sqrt(7)",
        abs(math.hypot(RHO_SCALAR, ETA_SCALAR) - RADIAL_SCALAR) < 1.0e-12,
        f"radius = {math.hypot(RHO_SCALAR, ETA_SCALAR):.12f}",
    )
    check(
        "The CKM scalar contraction factor is exactly kappa_cp = sqrt(6/7)",
        abs(RADIAL_SCALAR / (1.0 / math.sqrt(6.0)) - KAPPA_CP) < 1.0e-12,
        f"ratio = {RADIAL_SCALAR / (1.0 / math.sqrt(6.0)):.12f}",
    )
    check(
        "The support endpoint rewrites exactly in scalar-package language as 1 - rho_scalar * kappa_cp = 6/7",
        abs((1.0 - RHO_SCALAR * KAPPA_CP) - 6.0 / 7.0) < 1.0e-12,
        f"value = {1.0 - RHO_SCALAR * KAPPA_CP:.12f}",
    )


def part2_obstruction_and_anchor() -> BridgeSetup:
    print("\n" + "=" * 72)
    print("PART 2: Theorem Obstruction and Exact Bridge Band")
    print("=" * 72)

    anchored = solve_anchored_surface()
    kappa_anchor = kappa_from_amplitude(anchored.amp_u)
    lower_amplitude = amplitude_from_kappa(1.0)
    upper_amplitude = amplitude_from_kappa(KAPPA_CP)

    baseline_refit = evaluate_candidate(
        "7/9",
        "external",
        7.0 / 9.0,
        anchored.r_uc,
        anchored.r_ct,
    ).refit_objective
    baseline_anchor = evaluate_candidate(
        "sqrt(3/5)",
        "external",
        math.sqrt(3.0 / 5.0),
        anchored.r_uc,
        anchored.r_ct,
    ).anchor_aggregate

    print(f"\n  anchored a_u            = {anchored.amp_u:.12f}")
    print(f"  anchored kappa          = {kappa_anchor:.12f}")
    print(f"  bridge lower endpoint   = {lower_amplitude:.12f}")
    print(f"  bridge upper endpoint   = {upper_amplitude:.12f}")
    print(f"  amplitude band width    = {upper_amplitude - lower_amplitude:.12f}")
    print(
        f"  relative band width     = {100.0 * (upper_amplitude - lower_amplitude) / anchored.amp_u:.3f}%"
    )
    print(f"  refit baseline (7/9)    = {baseline_refit:.12f}")
    print(f"  anchor baseline sqrt(3/5)= {baseline_anchor:.12f}%")

    check(
        "Atlas note still classifies 1/sqrt(7) as scalar comparison only, not the bright/tensor theorem value",
        require_text(
            ATLAS_NOTE,
            (
                "scalar democratic contraction `1/sqrt(7)`",
                "exact scalar support comparison surface",
                "not the theorem value for the bright/tensor",
            ),
        ),
        "checked CKM atlas obstruction wording",
    )
    check(
        "Bilinear carrier note still keeps unit leading bright columns with only lower-row delta_A1 dressing",
        require_text(
            TENSOR_NOTE,
            (
                "carrier columns are exact",
                "[[1,0],[delta_A1(r),0]]",
                "[[0,1],[0,delta_A1(r)]]",
            ),
        ),
        "checked exact carrier-column theorem wording",
    )
    check(
        "Anchored reduced solve lies inside the exact scalar-comparison bridge band",
        lower_amplitude < anchored.amp_u < upper_amplitude,
        f"a_u = {anchored.amp_u:.12f} in [{lower_amplitude:.12f}, {upper_amplitude:.12f}]",
    )
    check(
        "Exact scalar-comparison bridge band is narrower than 1.5% of the anchored amplitude",
        100.0 * (upper_amplitude - lower_amplitude) / anchored.amp_u < 1.5,
        f"relative width = {100.0 * (upper_amplitude - lower_amplitude) / anchored.amp_u:.3f}%",
    )

    return BridgeSetup(
        anchor_r_uc=anchored.r_uc,
        anchor_r_ct=anchored.r_ct,
        anchored_a_u=anchored.amp_u,
        kappa_anchor=kappa_anchor,
        lower_amplitude=lower_amplitude,
        upper_amplitude=upper_amplitude,
        baseline_refit=baseline_refit,
        baseline_anchor=baseline_anchor,
    )


def part3_continuous_bridge(setup: BridgeSetup) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Continuous Scalar-Comparison Bridge")
    print("=" * 72)

    @lru_cache(maxsize=None)
    def bridge_eval(kappa: float):
        amplitude = amplitude_from_kappa(kappa)
        return evaluate_candidate(
            f"kappa={kappa:.12f}",
            "scalar-bridge",
            amplitude,
            setup.anchor_r_uc,
            setup.anchor_r_ct,
        )

    def refit_gap(kappa: float) -> float:
        return bridge_eval(kappa).refit_objective - setup.baseline_refit

    def anchor_gap(kappa: float) -> float:
        return bridge_eval(kappa).anchor_aggregate - setup.baseline_anchor

    refit_opt = minimize_scalar(
        lambda value: bridge_eval(float(value)).refit_objective,
        bounds=(KAPPA_CP, 1.0),
        method="bounded",
        options={"xatol": 1.0e-12},
    )
    anchor_opt = minimize_scalar(
        lambda value: bridge_eval(float(value)).anchor_aggregate,
        bounds=(KAPPA_CP, 1.0),
        method="bounded",
        options={"xatol": 1.0e-12},
    )

    refit_eval = bridge_eval(float(refit_opt.x))
    anchor_eval = bridge_eval(float(anchor_opt.x))

    def negative_window(fn) -> BridgeWindow | None:
        sample_points = [
            KAPPA_CP + (1.0 - KAPPA_CP) * index / 200.0
            for index in range(201)
        ]
        values = [fn(float(point)) for point in sample_points]

        roots: list[float] = []
        for left, right, value_left, value_right in zip(
            sample_points[:-1],
            sample_points[1:],
            values[:-1],
            values[1:],
        ):
            if value_left == 0.0:
                roots.append(left)
            elif value_left * value_right < 0.0:
                roots.append(
                    brentq(
                        lambda variable: fn(float(variable)),
                        left,
                        right,
                        xtol=1.0e-12,
                        rtol=1.0e-12,
                        maxiter=200,
                    )
                )

        if len(roots) >= 2:
            return BridgeWindow(lower=roots[0], upper=roots[-1])

        negative_points = [point for point, value in zip(sample_points, values) if value < 0.0]
        if not negative_points:
            return None
        return BridgeWindow(lower=min(negative_points), upper=max(negative_points))

    refit_window = negative_window(refit_gap)
    anchor_window = negative_window(anchor_gap)

    print(f"\n  best refit kappa        = {float(refit_opt.x):.12f}")
    print(f"  best refit a_u          = {amplitude_from_kappa(float(refit_opt.x)):.12f}")
    print(f"  best refit objective    = {refit_eval.refit_objective:.12f}")
    print(f"  best refit anchor score = {refit_eval.anchor_aggregate:.12f}%")
    print()
    print(f"  best anchor kappa       = {float(anchor_opt.x):.12f}")
    print(f"  best anchor a_u         = {amplitude_from_kappa(float(anchor_opt.x)):.12f}")
    print(f"  best anchor score       = {anchor_eval.anchor_aggregate:.12f}%")
    print(f"  best anchor refit obj   = {anchor_eval.refit_objective:.12f}")
    print()
    if refit_window is not None:
        print(
            f"  refit-better kappa window  = [{refit_window.lower:.12f}, {refit_window.upper:.12f}]"
        )
    if anchor_window is not None:
        print(
            f"  anchor-better kappa window = [{anchor_window.lower:.12f}, {anchor_window.upper:.12f}]"
        )
    print(f"  anchored kappa             = {setup.kappa_anchor:.12f}")

    check(
        "Continuous scalar bridge beats the 7/9 baseline on the refit axis",
        refit_eval.refit_objective < setup.baseline_refit,
        f"{refit_eval.refit_objective:.12f} < {setup.baseline_refit:.12f}",
    )
    check(
        "Continuous scalar bridge beats the sqrt(3/5) baseline on the anchored axis",
        anchor_eval.anchor_aggregate < setup.baseline_anchor,
        f"{anchor_eval.anchor_aggregate:.12f}% < {setup.baseline_anchor:.12f}%",
    )
    check(
        "Anchored reduced solve lands essentially on the refit-optimal scalar bridge",
        abs(setup.kappa_anchor - float(refit_opt.x)) < 2.0e-5,
        f"|delta kappa| = {abs(setup.kappa_anchor - float(refit_opt.x)):.6e}",
    )
    check(
        "Refit-better and anchor-better scalar-bridge windows are disjoint",
        refit_window is not None
        and anchor_window is not None
        and refit_window.upper < anchor_window.lower,
        (
            f"refit window = [{refit_window.lower:.12f}, {refit_window.upper:.12f}], "
            f"anchor window = [{anchor_window.lower:.12f}, {anchor_window.upper:.12f}]"
            if refit_window is not None and anchor_window is not None
            else "missing comparison window"
        ),
    )


def part4_summary() -> None:
    print("\n" + "=" * 72)
    print("PART 4: Summary")
    print("=" * 72)

    print("\n  honest scalar-bridge endpoint:")
    print("    - the scalar-comparison CKM package does not derive the bright/tensor")
    print("      1->3 amplitude, because the atlas and bilinear-carrier notes")
    print("      explicitly classify 1/sqrt(7) as comparison-only and keep unit")
    print("      leading bright columns on the exact carrier;")
    print("    - but that same scalar package does define a natural exact bridge")
    print("      interval and a one-parameter bridge family on the reduced quark")
    print("      anchor;")
    print("    - the anchored branch sits tightly inside that interval and almost")
    print("      exactly on the refit-optimal scalar bridge;")
    print("    - the scalar bridge still splits into a refit-better window and an")
    print("      anchor-better window with no overlap.")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Quark Up-Amplitude Scalar-Comparison Bridge")
    print("=" * 72)

    part1_exact_package()
    setup = part2_obstruction_and_anchor()
    part3_continuous_bridge(setup)
    part4_summary()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
