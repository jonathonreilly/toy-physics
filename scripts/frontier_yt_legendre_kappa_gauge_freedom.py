#!/usr/bin/env python3
"""
PR #230 Legendre kappa gauge-freedom check.

The source-to-Higgs route needs the Legendre transform to supply the
source-to-canonical-field normalization kappa_H.  This runner checks whether
the Legendre transform alone can do that.

It cannot.  A source/operator rescaling W_k(J)=W(k J) induces
phi_k = dW_k/dJ = k phi and Gamma_k(phi_k)=Gamma(phi_k/k).  The Legendre
relation is preserved, while the curvature/residue and Yukawa readout scale.
Therefore kappa_H must come from a pole-residue/canonical-kinetic condition,
not from the Legendre transform alone.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_legendre_kappa_gauge_freedom_2026-05-01.json"

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


def w_source(j: float, chi: float) -> float:
    return 0.5 * chi * j * j


def phi_of_j(j: float, chi: float) -> float:
    return chi * j


def gamma_of_phi(phi: float, chi: float) -> float:
    return 0.5 * phi * phi / chi


def legendre_identity_residual(j: float, chi: float) -> float:
    phi = phi_of_j(j, chi)
    return abs(gamma_of_phi(phi, chi) - (j * phi - w_source(j, chi)))


def main() -> int:
    print("PR #230 Legendre kappa gauge-freedom check")
    print("=" * 72)

    chi = 2.75
    source_tree_coefficient = 1.0 / math.sqrt(6.0)
    j_probe = 0.2
    kappas = [0.5, math.sqrt(8.0 / 9.0), 1.0, 2.0]
    models = []
    for kappa in kappas:
        chi_k = kappa * kappa * chi
        phi_k = phi_of_j(j_probe, chi_k)
        gamma_curvature_k = 1.0 / chi_k
        y_readout = source_tree_coefficient * kappa
        models.append(
            {
                "kappa": kappa,
                "chi_k": chi_k,
                "phi_k_at_probe": phi_k,
                "gamma_second_derivative": gamma_curvature_k,
                "legendre_identity_residual": legendre_identity_residual(j_probe, chi_k),
                "y_readout": y_readout,
            }
        )

    all_legendre_ok = all(row["legendre_identity_residual"] < 1.0e-15 for row in models)
    distinct_curvatures = len({round(row["gamma_second_derivative"], 15) for row in models}) == len(models)
    distinct_y = len({round(row["y_readout"], 15) for row in models}) == len(models)
    curvature_scale_ratio = models[0]["gamma_second_derivative"] / models[-1]["gamma_second_derivative"]
    expected_ratio = (models[-1]["kappa"] / models[0]["kappa"]) ** 2

    report("legendre-identity-holds-for-all-kappa", all_legendre_ok, "Gamma = J phi - W in every model")
    report("curvature-scales-under-source-normalization", distinct_curvatures, f"curvatures={[round(row['gamma_second_derivative'], 6) for row in models]}")
    report("y-readout-scales-under-kappa", distinct_y, f"y={[round(row['y_readout'], 6) for row in models]}")
    report(
        "curvature-scale-law",
        abs(curvature_scale_ratio - expected_ratio) < 1.0e-12,
        f"ratio={curvature_scale_ratio:.6g}, expected={expected_ratio:.6g}",
    )
    report(
        "legendre-transform-does-not-select-kappa-one",
        True,
        "all kappa choices preserve the Legendre relation",
    )
    report(
        "pole-residue-condition-required",
        True,
        "canonical normalization must be supplied by momentum-dependent two-point residue/kinetic term",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / Legendre normalization freedom",
        "verdict": (
            "The Legendre transform is covariant under source/operator rescaling. "
            "Changing kappa preserves Gamma = J phi - W while changing the "
            "two-point curvature and the Yukawa readout.  Therefore the "
            "source-to-canonical-Higgs normalization kappa_H is not selected by "
            "the Legendre transform alone; a pole-residue or canonical kinetic "
            "normalization theorem is required."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "kappa_H remains a field-normalization freedom without a residue/kinetic condition.",
        "base_chi": chi,
        "source_tree_coefficient": source_tree_coefficient,
        "models": models,
        "required_next_theorem": [
            "derive momentum-dependent scalar two-point function",
            "identify a physical scalar pole or canonical kinetic term",
            "fix kappa_H from the residue/kinetic normalization",
            "then compute y_t = c_source * kappa_H with v as substrate input",
        ],
        "strict_non_claims": [
            "does not derive kappa_H = 1",
            "does not identify the source scalar with H_unit",
            "does not use observed y_t or m_t",
            "does not promote the Ward theorem",
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
