#!/usr/bin/env python3
"""Bounded localized sewing-band construction for strong-field gravity.

Purpose:
  Starting from the exact shell projector already extracted for star-supported
  sources, build a simple metric-variable sewing construction:

    - exact microscopic interior metric inside r <= R_in
    - charge-fixed radial harmonic exterior metric outside r >= R_out
    - smooth blend of (psi, alpha*psi) across a finite transition band

  The goal is not full nonlinear GR. It is to test whether the remaining
  nonvacuum content can be localized to a finite matching shell while keeping
  the exterior beyond that shell vacuum-close across the exact source families
  already on codex/review-active.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
star = SourceFileLoader(
    "star_shell_projector",
    "/private/tmp/physics-review-active/scripts/frontier_star_shell_projector.py",
).load_module()


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def build_metric(phi_grid: np.ndarray, a: float, r_in: float, r_out: float):
    def metric_fn(point: np.ndarray) -> np.ndarray:
        r = float(np.linalg.norm(point))
        phi_in = coarse.interpolate_phi(phi_grid, point)
        psi_in = 1.0 + phi_in
        alpha_psi_in = 1.0 - phi_in

        phi_out = a / max(r, 1e-12)
        psi_out = 1.0 + phi_out
        alpha_psi_out = 1.0 - phi_out

        if r <= r_in:
            psi = psi_in
            alpha_psi = alpha_psi_in
        elif r >= r_out:
            psi = psi_out
            alpha_psi = alpha_psi_out
        else:
            s = smoothstep((r - r_in) / (r_out - r_in))
            psi = (1.0 - s) * psi_in + s * psi_out
            alpha_psi = (1.0 - s) * alpha_psi_in + s * alpha_psi_out

        alpha = alpha_psi / psi
        return np.diag(np.array([-(alpha**2), psi**4, psi**4, psi**4], dtype=float))

    return metric_fn


def residual_bands(metric_fn, r_in: float, r_out: float) -> tuple[float, float]:
    transition = []
    exterior = []
    for r in [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0]:
        points = [
            np.array([r, 0.0, 0.0]),
            np.array([r / np.sqrt(2.0), r / np.sqrt(2.0), 0.0]),
            np.array([r / np.sqrt(3.0)] * 3),
        ]
        vals = [float(np.max(np.abs(coarse.einstein_tensor(metric_fn, p)))) for p in points]
        if r_out < r:
            exterior.extend(vals)
        elif r_in < r <= r_out:
            transition.extend(vals)
    return max(transition), max(exterior)


def fit_a(phi_grid: np.ndarray, r_match: float = 4.5) -> float:
    r, y = star.shell_profile(phi_grid)
    return star.radial_fit_from_profile(r, y, r_match)


def analyze_family(name: str, phi_grid: np.ndarray, r_in: float, r_out: float):
    a = fit_a(phi_grid)
    metric_fn = build_metric(phi_grid, a, r_in, r_out)
    transition_max, exterior_max = residual_bands(metric_fn, r_in, r_out)
    print(
        f"{name}: a={a:.8f}, band=[{r_in:.1f}, {r_out:.1f}], "
        f"transition_max={transition_max:.3e}, exterior_max={exterior_max:.3e}"
    )
    return a, transition_max, exterior_max


def main() -> None:
    print("Localized sewing band for strong-field gravity")
    print("=" * 72)

    # Best shared band found in exploratory scans across both exact source
    # families: it minimizes the exterior residual while keeping the transition
    # shell finite.
    r_in = 3.0
    r_out = 5.0

    phi_oh = same_source.build_best_phi_grid()
    _, trans_oh, ext_oh = analyze_family("exact local O_h family", phi_oh, r_in, r_out)

    phi_fr = coarse.build_finite_rank_phi_grid()
    _, trans_fr, ext_fr = analyze_family("exact finite-rank family", phi_fr, r_in, r_out)

    record(
        "the sewn local O_h metric is vacuum-close outside the finite matching shell",
        ext_oh < 2e-6,
        f"transition max={trans_oh:.3e}, exterior max={ext_oh:.3e}",
    )
    record(
        "the sewn finite-rank metric is vacuum-close outside the finite matching shell",
        ext_fr < 5e-6,
        f"transition max={trans_fr:.3e}, exterior max={ext_fr:.3e}",
    )
    record(
        "the nonvacuum content is localized to the matching shell rather than the exterior",
        trans_oh > 1000.0 * ext_oh and trans_fr > 1000.0 * ext_fr,
        (
            f"O_h localization={trans_oh / ext_oh:.1f}x, "
            f"finite-rank localization={trans_fr / ext_fr:.1f}x"
        ),
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
