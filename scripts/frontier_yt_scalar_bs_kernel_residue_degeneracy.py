#!/usr/bin/env python3
"""
PR #230 scalar Bethe-Salpeter kernel / pole-residue degeneracy.

This is a direct follow-up to the same-source scalar two-point LSZ
measurement.  Even if we grant an isolated scalar pole for the same source,
finite current-surface measurements do not fix the inverse-propagator
derivative at that pole unless the interacting Bethe-Salpeter/RPA denominator
is derived.

The executable check constructs analytic denominator deformations that:

  * preserve all currently measured same-source Euclidean Gamma_ss(q) values;
  * preserve the granted pole location;
  * change d Gamma / d p^2 at the pole, hence the LSZ residue and kappa_s.

This is not a physical model of the Higgs channel.  It is a no-go witness for
using finite same-source samples, pole naming, or large-Nc intuition as a
substitute for the missing interacting kernel/residue theorem.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "outputs" / "yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_bs_kernel_residue_degeneracy_2026-05-01.json"

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


def load_same_source_row(target_mass: float = 0.75) -> tuple[np.ndarray, np.ndarray, dict]:
    cert = json.loads(INPUT.read_text(encoding="utf-8"))
    for row in cert["mass_rows"]:
        if abs(float(row["mass"]) - target_mass) < 1.0e-12:
            x_samples = np.asarray(
                [float(mode["p_hat_sq"]) for mode in row["mode_rows"]],
                dtype=float,
            )
            gamma_samples = np.asarray(
                [float(mode["Gamma_ss_real"]) for mode in row["mode_rows"]],
                dtype=float,
            )
            return x_samples, gamma_samples, row
    raise RuntimeError(f"target mass {target_mass} not found in {INPUT}")


def interpolation_denominator(
    x_samples: np.ndarray,
    gamma_samples: np.ndarray,
    pole_x: float,
) -> np.poly1d:
    xs = np.concatenate([np.asarray([pole_x], dtype=float), x_samples])
    ys = np.concatenate([np.asarray([0.0], dtype=float), gamma_samples])
    coeffs = np.polyfit(xs, ys, deg=len(x_samples))
    return np.poly1d(coeffs)


def deformation_unit(x: float | np.ndarray, pole_x: float, x_samples: np.ndarray) -> np.ndarray:
    """Polynomial that vanishes at the pole and samples, with unit pole derivative."""
    values = np.asarray(x, dtype=float) - pole_x
    for sample in x_samples:
        values = values * (np.asarray(x, dtype=float) - sample)
    pole_derivative = float(np.prod(pole_x - x_samples))
    return values / pole_derivative


def main() -> int:
    print("PR #230 scalar Bethe-Salpeter kernel / pole-residue degeneracy")
    print("=" * 72)

    nc = 3
    pole_x = -1.0
    x_samples, gamma_samples, source_row = load_same_source_row()
    reference = interpolation_denominator(x_samples, gamma_samples, pole_x)
    reference_derivative = float(reference.deriv()(pole_x))
    derivative_scale = reference_derivative

    etas = [-0.25, -1.0 / (nc * nc), 0.0, 1.0 / (nc * nc), 0.25]
    rows = []
    for eta in etas:
        def gamma_eta(x: float | np.ndarray) -> np.ndarray:
            return reference(x) + eta * derivative_scale * deformation_unit(x, pole_x, x_samples)

        sample_values = np.asarray(gamma_eta(x_samples), dtype=float)
        pole_value = float(gamma_eta(pole_x))
        derivative = reference_derivative * (1.0 + eta)
        residue_proxy = 1.0 / abs(derivative)
        kappa_proxy = 1.0 / math.sqrt(abs(derivative))
        rows.append(
            {
                "eta": eta,
                "eta_in_units_of_1_over_Nc_sq": eta * nc * nc,
                "sample_max_abs_error": float(np.max(np.abs(sample_values - gamma_samples))),
                "pole_residual": pole_value,
                "dGamma_dp2_at_pole": derivative,
                "LSZ_residue_proxy": residue_proxy,
                "kappa_s_proxy": kappa_proxy,
            }
        )

    sample_errors = [abs(row["sample_max_abs_error"]) for row in rows]
    pole_residuals = [abs(row["pole_residual"]) for row in rows]
    derivative_values = [row["dGamma_dp2_at_pole"] for row in rows]
    residue_values = [row["LSZ_residue_proxy"] for row in rows]
    kappa_values = [row["kappa_s_proxy"] for row in rows]
    nc3_rows = [row for row in rows if abs(abs(row["eta"]) - 1.0 / (nc * nc)) < 1.0e-14]
    nc3_kappas = [row["kappa_s_proxy"] for row in nc3_rows]
    nc3_residues = [row["LSZ_residue_proxy"] for row in nc3_rows]
    nc3_kappa_spread = (
        (max(nc3_kappas) - min(nc3_kappas)) / max(sum(nc3_kappas) / len(nc3_kappas), 1.0e-30)
        if nc3_kappas
        else float("nan")
    )
    nc3_residue_spread = (
        (max(nc3_residues) - min(nc3_residues)) / max(sum(nc3_residues) / len(nc3_residues), 1.0e-30)
        if nc3_residues
        else float("nan")
    )
    full_kappa_spread = (
        (max(kappa_values) - min(kappa_values)) / max(sum(kappa_values) / len(kappa_values), 1.0e-30)
    )

    report(
        "same-source-input-loaded",
        len(x_samples) == 4 and len(gamma_samples) == 4,
        f"mass={source_row['mass']}, samples={len(x_samples)}",
    )
    report(
        "reference-denominator-preserves-samples-and-pole",
        max(sample_errors) < 1.0e-10 and max(pole_residuals) < 1.0e-10,
        f"max_sample_error={max(sample_errors):.3e}, max_pole_residual={max(pole_residuals):.3e}",
    )
    report(
        "deformation-changes-pole-derivative",
        max(derivative_values) - min(derivative_values) > 0.25 * abs(reference_derivative),
        f"dGamma range=[{min(derivative_values):.12g}, {max(derivative_values):.12g}]",
    )
    report(
        "lsz-residue-not-fixed-by-finite-samples",
        max(residue_values) / min(residue_values) > 1.5,
        f"residue range=[{min(residue_values):.12g}, {max(residue_values):.12g}]",
    )
    report(
        "nc3-natural-remainder-moves-kappa",
        nc3_kappa_spread > 0.05 and nc3_residue_spread > 0.10,
        f"kappa_spread={nc3_kappa_spread:.6g}, residue_spread={nc3_residue_spread:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "finite same-source samples plus a named pole do not derive the interacting denominator derivative",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / scalar Bethe-Salpeter pole-residue degeneracy",
        "verdict": (
            "The same-source scalar two-point object can be embedded in analytic "
            "Bethe-Salpeter denominator families that preserve all currently "
            "measured Euclidean Gamma_ss(q) samples and preserve a granted "
            "isolated pole, while changing dGamma/dp^2 at that pole.  The LSZ "
            "residue and kappa_s therefore remain underdetermined until PR #230 "
            "derives the interacting scalar-channel kernel, finite-volume/IR "
            "limit, and pole-residue derivative.  At Nc=3, natural 1/Nc^2-sized "
            "denominator remainders already move the kappa proxy by more than "
            "five percent without changing the finite samples."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No retained theorem fixes the interacting Bethe-Salpeter/RPA "
            "denominator derivative or bounds finite-Nc pole-residue remainders."
        ),
        "source_certificate": str(INPUT.relative_to(ROOT)),
        "source_mass_row": source_row,
        "pole_x_granted_for_no_go": pole_x,
        "x_samples": x_samples.tolist(),
        "gamma_samples": gamma_samples.tolist(),
        "reference_polynomial_coefficients": reference.coefficients.tolist(),
        "reference_dGamma_dp2_at_pole": reference_derivative,
        "deformation_definition": (
            "Gamma_eta(x)=Gamma_ref(x)+eta*dGamma_ref(x_pole)*(x-x_pole)"
            "*prod_i(x-x_i)/prod_i(x_pole-x_i)"
        ),
        "rows": rows,
        "nc3_kappa_proxy_relative_spread": nc3_kappa_spread,
        "nc3_residue_proxy_relative_spread": nc3_residue_spread,
        "full_eta_kappa_proxy_relative_spread": full_kappa_spread,
        "required_next_theorem": [
            "derive the interacting scalar-channel Bethe-Salpeter/RPA denominator rather than fitting it",
            "derive the scalar source/projector normalization in the same denominator",
            "prove the finite-volume, gauge-zero-mode, and IR limiting order",
            "prove or measure pole saturation/continuum bounds at Nc=3",
            "compute dGamma_ss/dp^2 at the pole before converting dE_top/ds to dE_top/dh",
        ],
        "strict_non_claims": [
            "not a y_t derivation",
            "not production evidence",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, or Z_match to one",
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
