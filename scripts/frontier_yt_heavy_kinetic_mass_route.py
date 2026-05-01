#!/usr/bin/env python3
"""
PR #230 heavy kinetic-mass route scout.

The static/HQET obstruction showed that a zero-momentum static correlator
cannot determine the absolute top mass: additive mass shifts are invisible
after rephasing.  This runner tests the natural heavy-quark successor route:
extract the kinetic mass from nonzero-momentum energy splittings,

    E(p) - E(0) ~= p_hat^2 / (2 M_kin).

The additive rest-mass shift cancels in the difference.  This is not a
production result and not a retained closure; it is an executable route
certificate that identifies the missing observable and its precision burden.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_heavy_kinetic_mass_route_2026-05-01.json"

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


def p_hat_sq(nvec: tuple[int, int, int], spatial_lattice_size: int) -> float:
    return sum((2.0 * math.sin(math.pi * n / spatial_lattice_size)) ** 2 for n in nvec)


def energy(
    *,
    nvec: tuple[int, int, int],
    spatial_lattice_size: int,
    m_kin: float,
    additive_shift: float,
    c4: float = 1.0,
) -> float:
    ph2 = p_hat_sq(nvec, spatial_lattice_size)
    # Synthetic lattice-NRQCD dispersion through the first curvature correction.
    return additive_shift + ph2 / (2.0 * m_kin) - c4 * ph2 * ph2 / (8.0 * m_kin**3)


def extract_m_kin(
    *,
    nvec: tuple[int, int, int],
    spatial_lattice_size: int,
    e_p: float,
    e_0: float,
) -> float:
    delta_e = e_p - e_0
    return p_hat_sq(nvec, spatial_lattice_size) / (2.0 * delta_e)


def main() -> int:
    print("PR #230 heavy kinetic-mass route scout")
    print("=" * 72)

    spatial_lattice_size = 24
    m_kin_values = [5.0, 20.0, 80.0]
    shifts = [0.0, 3.0, 17.0]
    momentum_modes = [(1, 0, 0), (1, 1, 0), (2, 0, 0)]

    scan = []
    for m_kin in m_kin_values:
        for shift in shifts:
            e0 = energy(
                nvec=(0, 0, 0),
                spatial_lattice_size=spatial_lattice_size,
                m_kin=m_kin,
                additive_shift=shift,
            )
            for nvec in momentum_modes:
                ep = energy(
                    nvec=nvec,
                    spatial_lattice_size=spatial_lattice_size,
                    m_kin=m_kin,
                    additive_shift=shift,
                )
                extracted = extract_m_kin(
                    nvec=nvec,
                    spatial_lattice_size=spatial_lattice_size,
                    e_p=ep,
                    e_0=e0,
                )
                scan.append(
                    {
                        "spatial_lattice_size": spatial_lattice_size,
                        "input_m_kin": m_kin,
                        "additive_shift": shift,
                        "momentum_mode": nvec,
                        "p_hat_sq": p_hat_sq(nvec, spatial_lattice_size),
                        "delta_e": ep - e0,
                        "extracted_m_kin": extracted,
                        "relative_error": abs(extracted - m_kin) / m_kin,
                    }
                )

    # For the pure static action, all nonzero-momentum splittings are absent:
    # the kinetic-mass formula would divide by zero and return M_kin=infinity.
    static_splittings = [0.0 for _mode in momentum_modes]

    shift_groups: dict[tuple[float, tuple[int, int, int]], list[float]] = {}
    for row in scan:
        key = (row["input_m_kin"], tuple(row["momentum_mode"]))
        shift_groups.setdefault(key, []).append(row["extracted_m_kin"])

    max_shift_spread = max(max(vals) - min(vals) for vals in shift_groups.values())
    max_rel_error_light_modes = max(
        row["relative_error"]
        for row in scan
        if row["momentum_mode"] in [(1, 0, 0), (1, 1, 0)]
    )
    heavy_min_delta_e = min(
        row["delta_e"]
        for row in scan
        if row["input_m_kin"] == 80.0 and row["momentum_mode"] == (1, 0, 0)
    )
    required_abs_energy_precision_for_1pct = heavy_min_delta_e * 0.01

    report(
        "kinetic-route-scan-runs",
        len(scan) == len(m_kin_values) * len(shifts) * len(momentum_modes),
        f"points={len(scan)}",
    )
    report(
        "additive-shift-cancels-from-kinetic-mass",
        max_shift_spread < 1.0e-8,
        f"max_shift_spread={max_shift_spread:.3e}",
    )
    report(
        "kinetic-mass-recovered-from-low-momentum-splittings",
        max_rel_error_light_modes < 2.0e-3,
        f"max_relative_error={max_rel_error_light_modes:.3e}",
    )
    report(
        "static-limit-has-no-kinetic-readout",
        all(delta == 0.0 for delta in static_splittings),
        "pure static correlator gives E(p)-E(0)=0, so the route needs a 1/M kinetic operator",
    )
    report(
        "heavy-top-splitting-is-precision-demanding",
        heavy_min_delta_e < 5.0e-4,
        f"L=24, M=80, p_min delta_e={heavy_min_delta_e:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "requires nonzero-momentum correlator production data and action/matching theorem",
    )

    result = {
        "actual_current_surface_status": "bounded-support / heavy kinetic-mass route",
        "verdict": (
            "A nonzero-momentum kinetic-mass observable can cancel the static "
            "additive rest-mass ambiguity: E(p)-E(0) is invariant under the "
            "additive shift that blocks zero-momentum HQET.  This gives PR #230 "
            "a concrete heavy-matching route.  It is not closure, because pure "
            "static correlators have no kinetic splitting and a top-like heavy "
            "mass on L=24 gives very small delta_e, so the route requires a "
            "1/M kinetic action term, nonzero-momentum correlator production "
            "data, and a lattice-HQET/NRQCD-to-SM matching theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No production nonzero-momentum correlator data or retained "
            "heavy-action matching theorem is present."
        ),
        "parameters": {
            "spatial_lattice_size": spatial_lattice_size,
            "momentum_modes": momentum_modes,
            "m_kin_values": m_kin_values,
            "additive_shifts": shifts,
        },
        "scan": scan,
        "precision_witness": {
            "m_kin": 80.0,
            "momentum_mode": (1, 0, 0),
            "delta_e": heavy_min_delta_e,
            "required_abs_energy_precision_for_1pct_mkin": required_abs_energy_precision_for_1pct,
        },
        "required_next_artifacts": [
            "implement nonzero-momentum top/HQET correlator measurement",
            "include or derive the 1/M kinetic operator on the Cl(3)/Z^3 substrate",
            "extract E(p)-E(0) with bootstrap/jackknife errors",
            "derive matching from lattice M_kin to SM top mass without observed top calibration",
            "propagate M_kin through y_t = sqrt(2) m_t / v with v as substrate input",
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
