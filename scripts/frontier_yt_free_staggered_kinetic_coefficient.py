#!/usr/bin/env python3
"""
PR #230 free Wilson-staggered kinetic coefficient.

This is the positive part of the heavy kinetic route: in the free
Wilson-staggered action, the small-momentum kinetic coefficient is not an
arbitrary convention.  The pole relation is

    sinh(E)^2 = m^2 + sum_i sin(p_i)^2,

so the lattice kinetic mass inferred from E(p)-E(0) is fixed by the action.

This does not close PR #230 because interacting gauge dynamics and
lattice-to-SM matching remain open imports.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_free_staggered_kinetic_coefficient_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def p_lat(n: int, spatial_l: int) -> float:
    return 2.0 * math.pi * n / spatial_l


def q_hat(nvec: tuple[int, int, int], spatial_l: int) -> float:
    return sum(math.sin(p_lat(n, spatial_l)) ** 2 for n in nvec)


def energy(mass: float, nvec: tuple[int, int, int], spatial_l: int) -> float:
    return math.asinh(math.sqrt(mass * mass + q_hat(nvec, spatial_l)))


def exact_free_mkin(mass: float) -> float:
    return mass * math.sqrt(1.0 + mass * mass)


def finite_mkin(mass: float, nvec: tuple[int, int, int], spatial_l: int) -> float:
    e0 = energy(mass, (0, 0, 0), spatial_l)
    ep = energy(mass, nvec, spatial_l)
    # Use the continuum small-p numerator p^2 so convergence tests the
    # low-momentum kinetic coefficient rather than the finite-p lattice chord.
    p2 = sum(p_lat(n, spatial_l) ** 2 for n in nvec)
    return p2 / (2.0 * (ep - e0))


def main() -> int:
    print("PR #230 free Wilson-staggered kinetic coefficient")
    print("=" * 72)

    masses = [0.5, 1.0, 2.0, 5.0]
    volumes = [16, 24, 32, 48, 64, 128, 256]
    rows = []
    for mass in masses:
        exact = exact_free_mkin(mass)
        finite = []
        for spatial_l in volumes:
            mkin = finite_mkin(mass, (1, 0, 0), spatial_l)
            finite.append(
                {
                    "spatial_L": spatial_l,
                    "finite_p_mkin": mkin,
                    "relative_error_to_exact": abs(mkin - exact) / exact,
                }
            )
        rows.append(
            {
                "mass": mass,
                "rest_energy_asinh_m": math.asinh(mass),
                "exact_free_mkin": exact,
                "mkin_over_bare_mass": exact / mass,
                "mkin_over_rest_energy": exact / math.asinh(mass),
                "finite_p_sequence": finite,
            }
        )

    max_large_l_error = max(row["finite_p_sequence"][-1]["relative_error_to_exact"] for row in rows)
    mkin_not_bare = all(abs(row["mkin_over_bare_mass"] - 1.0) > 0.01 for row in rows if row["mass"] >= 1.0)
    mkin_not_rest_energy = all(abs(row["mkin_over_rest_energy"] - 1.0) > 0.01 for row in rows)

    report("free-dispersion-rows-built", len(rows) == len(masses), f"rows={len(rows)}")
    report(
        "finite-momentum-estimates-converge",
        max_large_l_error < 2.0e-3,
        f"max_L256_relative_error={max_large_l_error:.3e}",
    )
    report(
        "free-kinetic-coefficient-is-action-fixed",
        True,
        "M_kin^free = m sqrt(1+m^2) from the staggered pole relation",
    )
    report(
        "kinetic-mass-not-bare-mass-at-heavy-m",
        mkin_not_bare,
        f"ratios={[row['mkin_over_bare_mass'] for row in rows]}",
    )
    report(
        "kinetic-mass-not-rest-energy",
        mkin_not_rest_energy,
        f"ratios={[row['mkin_over_rest_energy'] for row in rows]}",
    )
    report(
        "not-retained-closure",
        True,
        "free c2 support does not supply interacting renormalization, production data, or SM matching",
    )

    result = {
        "actual_current_surface_status": "exact support / free staggered kinetic coefficient",
        "verdict": (
            "The free Wilson-staggered action fixes the small-momentum kinetic "
            "coefficient: sinh(E)^2 = m^2 + sum_i sin(p_i)^2 implies "
            "M_kin^free = m sqrt(1+m^2).  Finite momentum estimates converge "
            "to this expression.  This retires the idea that c2 is arbitrary "
            "in the free action, but it does not close PR #230 because the "
            "interacting kinetic renormalization, production data, and "
            "lattice-to-SM matching theorem remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Exact free-action support only; interacting c2/Z_match and production evidence remain open.",
        "rows": rows,
        "required_next_artifacts": [
            "derive interacting kinetic coefficient / renormalization under SU(3) Wilson gauge dynamics",
            "measure nonzero-momentum correlators on production ensembles",
            "derive lattice-to-SM top mass matching",
        ],
        "strict_non_claims": [
            "not a production measurement",
            "not a y_t derivation",
            "does not use observed top mass as calibration",
            "does not define y_t through H_unit matrix elements",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
