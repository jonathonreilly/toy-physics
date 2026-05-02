#!/usr/bin/env python3
"""
PR #230 FH/LSZ pole-fit model-class acceptance gate.

The pole-fit postprocessor can only become evidence if a finite Euclidean
shell fit is paired with an analytic continuation/model-class certificate, a
scalar-denominator theorem, or production continuum/pole-saturation evidence
that excludes shell-vanishing derivative deformations.  The current surface has
none of those inputs, so this runner deliberately blocks retained use.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POSTPROCESSOR = ROOT / "outputs" / "yt_fh_lsz_pole_fit_postprocessor_2026-05-01.json"
FINITE_SHELL_NO_GO = ROOT / "outputs" / "yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json"
MODEL_CLASS_CERT = ROOT / "outputs" / "yt_fh_lsz_pole_fit_model_class_certificate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json"

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


def main() -> int:
    print("PR #230 FH/LSZ pole-fit model-class acceptance gate")
    print("=" * 72)

    postprocessor = load_json(POSTPROCESSOR)
    finite_shell_no_go = load_json(FINITE_SHELL_NO_GO)
    model_class_cert = load_json(MODEL_CLASS_CERT)
    postprocess_ready = bool(postprocessor.get("readiness", {}).get("fit_ready"))
    no_go_loaded = "finite-shell pole-fit identifiability no-go" in finite_shell_no_go.get(
        "actual_current_surface_status", ""
    )
    model_class_ready = bool(model_class_cert.get("model_class_gate_passed"))
    accepted = postprocess_ready and model_class_ready

    acceptance_requirements = [
        {
            "requirement": "combined production same-source FH/LSZ output",
            "current_status": "absent/nonready" if not postprocess_ready else "present",
            "gate": "postprocessor readiness must be true",
        },
        {
            "requirement": "finite-shell ambiguity excluded",
            "current_status": "blocked by finite-shell identifiability no-go",
            "gate": "model-class, scalar-denominator, pole-saturation, or continuum certificate",
        },
        {
            "requirement": "pole derivative is load-bearing only after model-class gate",
            "current_status": "not accepted",
            "gate": "model_class_gate_passed must be true",
        },
    ]

    report("postprocessor-loaded", bool(postprocessor), str(POSTPROCESSOR.relative_to(ROOT)))
    report("finite-shell-no-go-loaded", no_go_loaded, str(FINITE_SHELL_NO_GO.relative_to(ROOT)))
    report("model-class-certificate-absent", not model_class_cert, str(MODEL_CLASS_CERT.relative_to(ROOT)))
    report("postprocessor-not-ready-as-evidence", not postprocess_ready, f"fit_ready={postprocess_ready}")
    report("retained-use-blocked-without-model-class", not accepted, f"accepted={accepted}")
    report("does-not-authorize-retained-proposal", True, "gate is open/blocking, not closure")

    result = {
        "actual_current_surface_status": "open / FH-LSZ pole-fit model-class gate blocks finite-shell fit as evidence",
        "verdict": (
            "The FH/LSZ pole-fit path now has an explicit model-class gate.  "
            "Future finite-shell Gamma_ss fits cannot be used as retained "
            "evidence merely because they produce a negative-p^2 pole and a "
            "finite derivative.  The branch must also supply a model-class, "
            "analytic-continuation, pole-saturation, continuum, or microscopic "
            "scalar-denominator certificate that excludes the finite-shell "
            "derivative ambiguity."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No production fit and no model-class/analytic-continuation certificate are present.",
        "postprocess_ready": postprocess_ready,
        "model_class_gate_passed": accepted,
        "parent_certificates": {
            "postprocessor": str(POSTPROCESSOR.relative_to(ROOT)),
            "finite_shell_no_go": str(FINITE_SHELL_NO_GO.relative_to(ROOT)),
            "future_model_class_certificate": str(MODEL_CLASS_CERT.relative_to(ROOT)),
        },
        "acceptance_requirements": acceptance_requirements,
        "strict_non_claims": [
            "does not accept finite-shell pole fits as retained evidence",
            "does not set kappa_s = 1",
            "does not use observed top mass or observed y_t",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Either derive the scalar denominator/model-class theorem that "
            "excludes shell-vanishing derivative deformations, or wait for "
            "production FH/LSZ data and then provide a model-class certificate "
            "before rerunning this gate."
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
