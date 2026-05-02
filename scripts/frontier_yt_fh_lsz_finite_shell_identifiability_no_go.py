#!/usr/bin/env python3
"""
PR #230 FH/LSZ finite-shell pole-fit identifiability no-go.

Finite Euclidean momentum-shell values of the same-source inverse scalar
correlator do not determine the LSZ pole derivative by themselves.  This
runner constructs analytic inverse-propagator deformations that agree on the
finite shell set and keep the same negative-p^2 pole, while changing
dGamma_ss/dp^2 at the pole.  The result is a postprocessor claim boundary, not
production evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PARENT_POSTPROCESSOR = ROOT / "outputs" / "yt_fh_lsz_pole_fit_postprocessor_2026-05-01.json"
PARENT_KINEMATICS = ROOT / "outputs" / "yt_fh_lsz_pole_fit_kinematics_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json"

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def product(values: list[float]) -> float:
    out = 1.0
    for value in values:
        out *= value
    return out


def vanish_polynomial(x: float, shells: list[float]) -> float:
    return product([x - shell for shell in shells])


def gamma_value(x: float, *, pole: float, slope: float, epsilon: float, shells: list[float]) -> float:
    return slope * (x - pole) + epsilon * (x - pole) * vanish_polynomial(x, shells)


def gamma_derivative_at_pole(*, pole: float, slope: float, epsilon: float, shells: list[float]) -> float:
    return slope + epsilon * vanish_polynomial(pole, shells)


def build_models() -> dict[str, Any]:
    one_link = 4.0 * math.sin(math.pi / 12.0) ** 2
    shells = [0.0, one_link, 2.0 * one_link, 1.0]
    pole = -0.25
    base_slope = 1.0
    pole_polynomial = vanish_polynomial(pole, shells)
    targets = {
        "half_derivative": 0.5,
        "base_derivative": 1.0,
        "double_derivative": 2.0,
    }
    rows: list[dict[str, Any]] = []
    sample_reference = [gamma_value(x, pole=pole, slope=base_slope, epsilon=0.0, shells=shells) for x in shells]
    for name, target_derivative in targets.items():
        epsilon = (target_derivative - base_slope) / pole_polynomial
        sample_values = [gamma_value(x, pole=pole, slope=base_slope, epsilon=epsilon, shells=shells) for x in shells]
        derivative = gamma_derivative_at_pole(pole=pole, slope=base_slope, epsilon=epsilon, shells=shells)
        rows.append(
            {
                "name": name,
                "epsilon": epsilon,
                "shell_values": sample_values,
                "same_pole_gamma": gamma_value(pole, pole=pole, slope=base_slope, epsilon=epsilon, shells=shells),
                "dGamma_dp2_at_pole": derivative,
                "relative_lsz_y_proxy_for_fixed_dE_ds": math.sqrt(derivative / base_slope),
            }
        )
    max_shell_mismatch = max(
        abs(value - reference)
        for row in rows
        for value, reference in zip(row["shell_values"], sample_reference)
    )
    max_pole_abs = max(abs(row["same_pole_gamma"]) for row in rows)
    derivatives = [row["dGamma_dp2_at_pole"] for row in rows]
    return {
        "shells_p_hat_sq": shells,
        "pole_p_hat_sq": pole,
        "base_slope": base_slope,
        "vanishing_polynomial_at_pole": pole_polynomial,
        "sample_reference": sample_reference,
        "models": rows,
        "checks": {
            "zero_plus_three_positive_shells": shells[0] == 0.0 and sum(1 for x in shells if x > 0.0) >= 3,
            "max_shell_mismatch": max_shell_mismatch,
            "max_pole_abs": max_pole_abs,
            "derivative_min": min(derivatives),
            "derivative_max": max(derivatives),
            "derivative_span_factor": max(derivatives) / min(derivatives),
        },
    }


def main() -> int:
    print("PR #230 FH/LSZ finite-shell pole-fit identifiability no-go")
    print("=" * 72)

    postprocessor = load_json(PARENT_POSTPROCESSOR)
    kinematics = load_json(PARENT_KINEMATICS)
    construction = build_models()
    checks = construction["checks"]

    report("parent-postprocessor-loaded", bool(postprocessor), str(PARENT_POSTPROCESSOR.relative_to(ROOT)))
    report("parent-kinematics-gate-loaded", bool(kinematics), str(PARENT_KINEMATICS.relative_to(ROOT)))
    report("zero-plus-three-positive-shells-constructed", checks["zero_plus_three_positive_shells"], str(construction["shells_p_hat_sq"]))
    report("finite-shell-values-identical", checks["max_shell_mismatch"] < 1e-12, f"max mismatch={checks['max_shell_mismatch']:.3e}")
    report("same-negative-pole-preserved", checks["max_pole_abs"] < 1e-12, f"max |Gamma(pole)|={checks['max_pole_abs']:.3e}")
    report("pole-derivative-not-identified", checks["derivative_span_factor"] >= 4.0, f"span={checks['derivative_span_factor']:.6g}")
    report("does-not-authorize-retained-proposal", True, "finite-shell data require an analytic model/theorem before LSZ use")

    result = {
        "actual_current_surface_status": "exact negative boundary / FH-LSZ finite-shell pole-fit identifiability no-go",
        "verdict": (
            "A finite set of same-source Euclidean Gamma_ss(p^2) shell values, "
            "even with zero plus three positive shells and a named negative-p^2 "
            "pole, does not determine dGamma_ss/dp^2 at the pole.  The "
            "constructed analytic deformations vanish on every sampled shell "
            "and at the pole, but change the pole derivative and therefore the "
            "fixed-dE/ds FH/LSZ readout.  A future pole-fit postprocessor needs "
            "either a production-backed analytic model class, continuum/pole "
            "saturation theorem, or additional acceptance gate before finite "
            "Euclidean shell rows can be load-bearing retained evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-shell pole fits are underidentified without a model-class or scalar-pole theorem.",
        "parent_certificates": {
            "postprocessor": str(PARENT_POSTPROCESSOR.relative_to(ROOT)),
            "kinematics_gate": str(PARENT_KINEMATICS.relative_to(ROOT)),
        },
        "construction": construction,
        "strict_non_claims": [
            "does not use observed top mass or observed y_t",
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use alpha_LM, plaquette, or u0 as proof input",
            "does not treat reduced pilots or finite-shell fits as production evidence",
        ],
        "exact_next_action": (
            "Add a pole-fit model-class/analytic-continuation acceptance gate, "
            "or derive the scalar denominator theorem that excludes these "
            "finite-shell deformations before using dGamma_ss/dp^2 as retained evidence."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
