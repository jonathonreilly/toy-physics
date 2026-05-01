#!/usr/bin/env python3
"""
PR #230 scalar-channel ladder kernel input audit.

The active PR #230 blocker is no longer the arithmetic value 1/sqrt(6).
It is the missing physical readout theorem that would turn a staggered scalar
source into a Higgs-carrier pole residue without using the audited H_unit
matrix-element definition.

This runner audits the exact inputs available from the existing full-staggered
PT code and classifies which of them may be reused for a scalar-channel
Bethe-Salpeter route.  It is intentionally not a closure runner.
"""

from __future__ import annotations

import importlib
import json
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SOURCE = SCRIPTS / "frontier_yt_p1_bz_quadrature_full_staggered_pt.py"
OUTPUT = ROOT / "outputs" / "yt_scalar_ladder_kernel_input_audit_2026-05-01.json"

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


def import_full_staggered_pt():
    sys.path.insert(0, str(SCRIPTS))
    return importlib.import_module("frontier_yt_p1_bz_quadrature_full_staggered_pt")


def bounded_ratio(values: np.ndarray) -> tuple[float, float]:
    finite = np.asarray(values, dtype=float)
    finite = finite[np.isfinite(finite)]
    return float(np.min(finite)), float(np.max(finite))


def main() -> int:
    print("PR #230 scalar-channel ladder kernel input audit")
    print("=" * 72)

    source_text = SOURCE.read_text(encoding="utf-8")
    pt = import_full_staggered_pt()

    required_formula_functions = [
        "D_psi_full",
        "D_gluon_full",
        "F_scalar_local",
        "F_scalar_ps_per_mu",
        "F_gauge_vertex_kin",
        "F_conserved_vec_vertex",
        "build_bz_grid",
    ]
    missing = [name for name in required_formula_functions if not hasattr(pt, name)]
    report(
        "full-staggered-formula-functions-present",
        not missing,
        f"missing={missing}",
    )

    forbidden_surface_tokens = [
        "CANONICAL_ALPHA_LM",
        "CANONICAL_PLAQUETTE",
        "CANONICAL_U0",
        "ALPHA_LM",
        "PLAQUETTE",
        "U_0",
        "H_unit",
    ]
    present_forbidden = [token for token in forbidden_surface_tokens if token in source_text]
    report(
        "forbidden-legacy-tokens-identified",
        len(present_forbidden) >= 4,
        f"tokens={present_forbidden}",
    )

    K, _dk = pt.build_bz_grid(8)
    d_psi = pt.D_psi_full(K)
    d_gluon = pt.D_gluon_full(K)
    f_scalar_local = pt.F_scalar_local(K)
    f_scalar_ps = pt.F_scalar_ps_per_mu(K)
    f_gauge = pt.F_gauge_vertex_kin(K)
    f_vec = pt.F_conserved_vec_vertex(K)

    dpsi_min, dpsi_max = bounded_ratio(d_psi)
    dgluon_min, dgluon_max = bounded_ratio(d_gluon)
    report(
        "staggered-fermion-denominator-nonnegative",
        dpsi_min >= 0.0 and dpsi_max > 0.0,
        f"range=[{dpsi_min:.6g}, {dpsi_max:.6g}]",
    )
    report(
        "wilson-gluon-denominator-nonnegative",
        dgluon_min >= 0.0 and dgluon_max > 0.0,
        f"range=[{dgluon_min:.6g}, {dgluon_max:.6g}]",
    )
    report(
        "local-scalar-form-factor-is-identity",
        float(np.max(np.abs(f_scalar_local - 1.0))) < 1.0e-14,
        f"max_abs_delta={float(np.max(np.abs(f_scalar_local - 1.0))):.3e}",
    )

    scalar_gauge_delta = float(np.max(np.abs(f_scalar_ps - f_gauge)))
    report(
        "point-split-scalar-and-gauge-kinematic-factor-match",
        scalar_gauge_delta < 1.0e-14,
        f"max_abs_delta={scalar_gauge_delta:.3e}",
    )

    # The parity-odd conserved vector numerator should average to zero on the
    # symmetric BZ grid.  This is a useful sanity check on the imported
    # staggered-current convention, not a y_t closure step.
    vec_mean = float(np.mean(f_vec))
    report(
        "conserved-vector-numerator-parity-cancels",
        abs(vec_mean) < 1.0e-14,
        f"mean={vec_mean:.3e}",
    )

    # The equality F_scalar_ps == F_gauge is only a kinematic equality.  It
    # cannot fix a pole residue because the bubble and gauge-dressing kernels
    # weight the same numerator with different denominators.
    mass_sq = 0.10 * 0.10
    eps = 1.0e-12
    scalar_weight = (f_scalar_ps * f_scalar_ps) / ((d_psi + mass_sq) ** 2 + eps)
    gauge_weight = f_gauge / ((d_psi + mass_sq) * (d_gluon + 0.10) + eps)
    scalar_mean = float(np.mean(scalar_weight))
    gauge_mean = float(np.mean(gauge_weight))
    denominator_weight_ratio = scalar_mean / gauge_mean
    report(
        "kinematic-match-does-not-force-common-dressing",
        abs(denominator_weight_ratio - 1.0) > 0.10,
        f"scalar_weight/gauge_weight={denominator_weight_ratio:.6g}",
    )

    closure_terms = [
        "pole residue",
        "LSZ",
        "Bethe",
        "Salpeter",
        "lambda_max",
        "eigenvalue",
    ]
    missing_closure_terms = [term for term in closure_terms if term not in source_text]
    report(
        "p1-runner-lacks-pole-residue-closure-objects",
        len(missing_closure_terms) >= 4,
        f"missing_terms={missing_closure_terms}",
    )

    allowed_reuse = [
        "D_psi_full formula",
        "D_gluon_full formula",
        "local scalar source form factor",
        "point-split scalar kinematic form factor as an algebraic formula only",
        "gauge vertex kinematic form factor as an algebraic formula only",
        "color factor C_F = 4/3",
    ]
    forbidden_reuse = [
        "CANONICAL_ALPHA_LM or alpha_LM bridge",
        "CANONICAL_PLAQUETTE or u0/tadpole normalization",
        "H_unit-to-top matrix-element readout",
        "old yt_ward_identity theorem as physical y_t authority",
        "observed top/Higgs/Yukawa values as selectors",
    ]
    still_missing = [
        "exact scalar-channel Bethe-Salpeter kernel from Wilson gauge exchange",
        "scalar color/taste/spin projector independent of H_unit readout",
        "IR and finite-volume limiting theorem for the kernel",
        "eigenvalue-crossing theorem",
        "pole residue from derivative of the inverse scalar two-point function",
        "common scalar/gauge dressing theorem or direct residue measurement",
    ]

    result = {
        "actual_current_surface_status": "exact-support / input audit",
        "verdict": (
            "The repo contains the staggered and Wilson kinematic formulae "
            "needed to build a scalar-channel ladder attempt.  The point-split "
            "scalar and gauge kinematic factors match exactly in the existing "
            "formula code, but that equality is not a physical pole-residue or "
            "common-dressing theorem because the scalar bubble and gauge "
            "dressing use different denominators and require different LSZ "
            "readouts.  The audited/legacy alpha_LM, plaquette, u0, and H_unit "
            "surfaces are present in the source runner but are classified here "
            "as forbidden proof inputs for PR #230 closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The scalar pole residue, projector, and kernel limiting theorem remain open imports.",
        "allowed_reuse": allowed_reuse,
        "forbidden_reuse": forbidden_reuse,
        "still_missing": still_missing,
        "numerical_sanity_checks": {
            "d_psi_range": [dpsi_min, dpsi_max],
            "d_gluon_range": [dgluon_min, dgluon_max],
            "scalar_gauge_kinematic_max_abs_delta": scalar_gauge_delta,
            "conserved_vector_mean": vec_mean,
            "scalar_weight_mean": scalar_mean,
            "gauge_weight_mean": gauge_mean,
            "scalar_to_gauge_weight_ratio": denominator_weight_ratio,
        },
        "strict_non_claims": [
            "not a y_t derivation",
            "not a retained scalar pole theorem",
            "does not use alpha_LM or plaquette normalization",
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
