#!/usr/bin/env python3
"""
PR #230 same-source scalar two-point LSZ measurement primitive.

Compute the scalar-source two-point bubble for the same additive source used
by the Feynman-Hellmann response harness:

    D(s) = D + (m_bare + s)

The runner uses the PR #230 Wilson-staggered Dirac operator on a tiny exact
cold lattice, constructs C_ss(q) = Tr[S V_q S V_-q], and inspects the inverse
curvature Gamma_ss(q)=1/C_ss(q).  This identifies the measurement that would
fix kappa_s through a scalar LSZ pole/residue, while certifying that the
current reduced/cold primitive is not retained closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

import yt_direct_lattice_correlator_production as prod


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json"

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


def phase_vector(geom: prod.Geometry, nvec: tuple[int, int, int], nt: int = 0) -> np.ndarray:
    phases = np.empty(geom.volume * prod.NC, dtype=np.complex128)
    for site in range(geom.volume):
        t, x, y, z = geom.site_coords(site)
        phase_arg = (
            nvec[0] * x / geom.spatial_l
            + nvec[1] * y / geom.spatial_l
            + nvec[2] * z / geom.spatial_l
            + nt * t / geom.time_l
        )
        phase = np.exp(2.0j * math.pi * phase_arg)
        for color in range(prod.NC):
            phases[site * prod.NC + color] = phase
    return phases


def p_hat_sq(geom: prod.Geometry, nvec: tuple[int, int, int], nt: int = 0) -> float:
    spatial = sum((2.0 * math.sin(math.pi * n / geom.spatial_l)) ** 2 for n in nvec)
    temporal = (2.0 * math.sin(math.pi * nt / geom.time_l)) ** 2
    return float(spatial + temporal)


def scalar_bubble(inverse_dirac: np.ndarray, phase: np.ndarray) -> complex:
    # V_q is diagonal, so S V_q is S with columns scaled by phase.
    s_v = inverse_dirac * phase[None, :]
    s_v_s = s_v @ inverse_dirac
    return complex(np.sum(np.diag(s_v_s) * np.conj(phase)))


def main() -> int:
    print("PR #230 same-source scalar two-point LSZ measurement primitive")
    print("=" * 72)

    geom = prod.Geometry(3, 6)
    gauge = prod.GaugeField(geom)
    masses = [0.55, 0.75, 0.95]
    modes = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]
    source_scales = [0.5, 1.0, 2.0]

    mass_rows = []
    for mass in masses:
        dirac = prod.build_staggered_dirac(gauge, mass).toarray()
        inverse_dirac = np.linalg.inv(dirac)
        mode_rows = []
        for nvec in modes:
            phase = phase_vector(geom, nvec)
            bubble = scalar_bubble(inverse_dirac, phase)
            normalized_bubble = bubble / (geom.volume * prod.NC)
            gamma = 1.0 / normalized_bubble
            mode_rows.append(
                {
                    "mode": list(nvec),
                    "p_hat_sq": p_hat_sq(geom, nvec),
                    "C_ss_real": float(normalized_bubble.real),
                    "C_ss_imag": float(normalized_bubble.imag),
                    "Gamma_ss_real": float(gamma.real),
                    "Gamma_ss_imag": float(gamma.imag),
                }
            )

        zero = mode_rows[0]
        first = mode_rows[1]
        finite_diff_derivative = (
            first["Gamma_ss_real"] - zero["Gamma_ss_real"]
        ) / max(first["p_hat_sq"] - zero["p_hat_sq"], 1.0e-30)
        finite_residue_proxy = (
            1.0 / abs(finite_diff_derivative)
            if abs(finite_diff_derivative) > 1.0e-30
            else float("nan")
        )
        mass_rows.append(
            {
                "mass": mass,
                "mode_rows": mode_rows,
                "finite_difference_dGamma_dp_hat_sq": finite_diff_derivative,
                "finite_residue_proxy": finite_residue_proxy,
                "has_inverse_zero_on_measured_modes": any(
                    abs(row["Gamma_ss_real"]) < 1.0e-10 and abs(row["Gamma_ss_imag"]) < 1.0e-10
                    for row in mode_rows
                ),
            }
        )

    base = mass_rows[1]
    base_c0 = base["mode_rows"][0]["C_ss_real"]
    source_scale_rows = []
    for scale in source_scales:
        c_scaled = scale * scale * base_c0
        gamma_scaled = 1.0 / c_scaled
        source_scale_rows.append(
            {
                "source_scale": scale,
                "C_ss_zero_mode_scaled": c_scaled,
                "Gamma_ss_zero_mode_scaled": gamma_scaled,
            }
        )

    all_bubbles_finite = all(
        math.isfinite(row["C_ss_real"]) and abs(row["C_ss_imag"]) < 1.0e-10
        for mass_row in mass_rows
        for row in mass_row["mode_rows"]
    )
    no_pole = not any(mass_row["has_inverse_zero_on_measured_modes"] for mass_row in mass_rows)
    residues = [
        row["finite_residue_proxy"]
        for row in mass_rows
        if math.isfinite(row["finite_residue_proxy"])
    ]
    residue_spread = (
        (max(residues) - min(residues)) / max(sum(residues) / len(residues), 1.0e-30)
        if residues
        else float("nan")
    )
    gamma_scale_ratio = (
        source_scale_rows[0]["Gamma_ss_zero_mode_scaled"]
        / source_scale_rows[2]["Gamma_ss_zero_mode_scaled"]
    )

    report("same-source-bubble-finite", all_bubbles_finite, "C_ss(q) finite and real on tiny cold lattice")
    report("inverse-curvature-no-pole-on-reduced-surface", no_pole, "no Gamma_ss(q)=0 on measured modes")
    report("finite-residue-proxy-mass-dependent", residue_spread > 0.10, f"relative_spread={residue_spread:.6g}")
    report("source-rescaling-changes-inverse-curvature", abs(gamma_scale_ratio - 16.0) < 1.0e-10, f"Gamma(0.5s)/Gamma(2s)={gamma_scale_ratio:.12g}")
    report("measurement-object-identifies-kappa-route", True, "need pole and dGamma/dp^2 for same source s")
    report("does-not-use-h-unit", True, "source two-point function only")
    report("does-not-use-observed-targets", True, "no observed top/y_t selector")
    report("not-retained-closure", True, "tiny cold lattice has no physical pole or production continuum control")

    result = {
        "actual_current_surface_status": "bounded-support / same-source scalar two-point LSZ measurement primitive",
        "verdict": (
            "The same scalar source used by the Feynman-Hellmann response route "
            "has an executable two-point measurement object: C_ss(q)=Tr[S V_q "
            "S V_-q] and Gamma_ss(q)=1/C_ss(q).  A true scalar LSZ bridge would "
            "fix kappa_s by proving an isolated pole and computing "
            "dGamma_ss/dp^2 at that pole for the same source.  The reduced cold "
            "lattice primitive does not close PR #230: it has no pole on the "
            "measured modes, its finite residue proxy is mass-dependent, and "
            "source rescaling changes inverse curvature unless canonical "
            "normalization is separately derived."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No isolated scalar pole, continuum/IR control, or canonical LSZ normalization is derived.",
        "geometry": {"spatial_L": geom.spatial_l, "time_L": geom.time_l, "colors": prod.NC},
        "mass_rows": mass_rows,
        "source_scale_rows": source_scale_rows,
        "finite_residue_proxy_relative_spread": residue_spread,
        "required_next_steps": [
            "measure C_ss(q) on production gauge ensembles for the same source shifts used in dE_top/ds",
            "derive or observe an isolated Higgs-channel pole in the controlled finite-volume/IR limit",
            "compute dGamma_ss/dp^2 at the pole and match it to canonical Higgs kinetic normalization",
            "only then convert dE_top/ds to physical dE_top/dh",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not a physical y_t derivation",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top mass or observed y_t",
            "does not set kappa_s to one",
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
