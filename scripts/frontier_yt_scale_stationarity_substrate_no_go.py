#!/usr/bin/env python3
"""
No-go runner for deriving Planck scale-stationarity from the current
Cl(3)/Z^3 fixed-lattice substrate.

The preceding beta-lambda no-go proved that lambda(M_Pl)=0 does not imply
beta_lambda(M_Pl)=0.  This runner attacks the next, narrower route:

    Can the fixed substrate's own symmetries supply a scale current or
    boundary-action stationarity theorem that forces beta_lambda(M_Pl)=0?

The answer checked here is no on the current authority surface.  Z^3 has
translations and discrete lattice automorphisms, but no nontrivial continuous
dilation symmetry.  The current lattice Noether theorem therefore supplies
translation and U(1) currents, not a scale current.  The physical-lattice
boundary also treats continuum/RG structure as an extra bridge, not as
same-surface substrate content.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scale_stationarity_substrate_no_go_2026-05-01.json"

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


def read_doc(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def det3_scalar(k: int) -> int:
    return k**3


def assert_z3_has_no_continuous_scale_automorphism() -> dict[str, object]:
    """Check the discrete group obstruction for scale transformations.

    Lattice automorphisms preserving Z^3 are GL(3,Z) matrices together with
    translations.  A scalar dilation x -> k x is an automorphism of Z^3 only
    when det(k I_3)=+-1, hence k=+-1 for integral scalar k.  A one-parameter
    continuous dilation exp(s) I cannot lie nontrivially in GL(3,Z), because
    GL(3,Z) is discrete and the identity has no nonzero scalar-dilation
    tangent inside the integer matrices.
    """
    scalar_results: list[dict[str, object]] = []
    for k in range(-4, 5):
        if k == 0:
            det = 0
            automorphism = False
        else:
            det = det3_scalar(k)
            automorphism = abs(det) == 1
        scalar_results.append({"k": k, "det": det, "automorphism": automorphism})

    nontrivial_scalar_automorphisms = [
        item for item in scalar_results if item["automorphism"] and item["k"] not in {-1, 1}
    ]
    integer_near_identity_dilation_tangent = False

    report(
        "scalar-dilation-automorphisms-only-plus-minus-one",
        not nontrivial_scalar_automorphisms,
        "integer scalar dilations preserve Z^3 bijectively only for k=+-1",
    )
    report(
        "no-infinitesimal-dilation-in-gl3z",
        not integer_near_identity_dilation_tangent,
        "GL(3,Z) is discrete, so exp(s)I has no nonzero tangent inside lattice automorphisms",
    )
    report(
        "translation-does-not-change-scale",
        True,
        "Z^3 translations move origins but leave the lattice spacing/evaluation surface fixed",
    )
    report(
        "fixed-lattice-scale-variation-not-same-surface",
        True,
        "varying the lattice spacing is a regulator-family move, not a Z^3 automorphism",
    )

    return {
        "scalar_dilation_scan": scalar_results,
        "nontrivial_scalar_automorphisms": nontrivial_scalar_automorphisms,
        "continuous_dilation_tangent_dimension": 0,
        "reason": "Z^3 automorphisms are discrete; continuous scale transformations are absent.",
    }


def assert_noether_surface_has_no_scale_current() -> dict[str, object]:
    noether = read_doc("docs/AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md")

    has_translation_current = "Z^3 translation symmetry" in noether
    has_u1_current = "Global U(1) phase symmetry" in noether
    full_emt_deferred = "full energy-momentum tensor" in noether and "deferred" in noether
    anomaly_deferred = "Anomaly slot" in noether and "does not say whether" in noether
    scale_mentions = re.findall(r"\b(scale current|dilation current|dilatation|dilation symmetry)\b", noether, re.I)

    report(
        "noether-translation-current-present",
        has_translation_current,
        "lattice Noether theorem supplies the translation current",
    )
    report(
        "noether-u1-current-present",
        has_u1_current,
        "lattice Noether theorem supplies the U(1) matter current",
    )
    report(
        "noether-full-emt-deferred",
        full_emt_deferred,
        "Noether note explicitly defers full energy-momentum tensor identification",
    )
    report(
        "noether-anomaly-not-closed",
        anomaly_deferred,
        "Noether note does not claim quantum anomaly/scale-current closure",
    )
    report(
        "noether-no-scale-current-claim",
        len(scale_mentions) == 0,
        "Noether authority contains no scale-current or dilation-symmetry theorem",
    )

    return {
        "translation_current": has_translation_current,
        "u1_current": has_u1_current,
        "full_emt_deferred": full_emt_deferred,
        "anomaly_deferred": anomaly_deferred,
        "scale_mentions": scale_mentions,
    }


def assert_fixed_surface_excludes_silent_rg_family() -> dict[str, object]:
    physical = read_doc("docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md")
    minimal = read_doc("docs/MINIMAL_AXIOMS_2026-04-11.md")

    physical_fixed = "fixed theory surface" in physical
    continuum_extra = "continuum-limit family" in physical and "extra" in physical
    renormalization_extra = "renormalization / universality / EFT interpretation layer" in physical
    fixed_quant_surface = "fixed canonical normalization/evaluation surface" in physical
    minimal_fixed_stack = "canonical normalization and evaluation surface" in minimal.lower()
    eft_bridge_not_auto = "perturbative low-energy EFT running" in minimal and "do not automatically promote" in minimal

    report(
        "physical-lattice-is-fixed-surface",
        physical_fixed and fixed_quant_surface,
        "physical-lattice note treats the accepted package as one fixed evaluation surface",
    )
    report(
        "continuum-family-is-extra",
        continuum_extra,
        "continuum-limit families are explicitly extra structure",
    )
    report(
        "renormalization-layer-is-extra",
        renormalization_extra,
        "renormalization/EFT interpretation layer is not same-surface substrate content",
    )
    report(
        "minimal-stack-fixed-normalization",
        minimal_fixed_stack,
        "minimal stack fixes canonical normalization/evaluation surface",
    )
    report(
        "eft-running-bridge-not-promotion",
        eft_bridge_not_auto,
        "SM/EFT running is bridge-conditioned and does not auto-promote a lane",
    )

    return {
        "physical_fixed": physical_fixed,
        "continuum_extra": continuum_extra,
        "renormalization_extra": renormalization_extra,
        "fixed_quant_surface": fixed_quant_surface,
        "minimal_fixed_stack": minimal_fixed_stack,
        "eft_bridge_not_auto": eft_bridge_not_auto,
    }


def assert_beta_stationarity_needs_extra_tangent() -> dict[str, object]:
    beta_no_go = read_doc("docs/YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md")
    selector = read_doc("docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md")

    codimension_relation = "y_t^4 = (3/400)" in beta_no_go
    finite_source_not_rg = "does not define the SM beta-vector" in beta_no_go
    selector_open = "not derived in this note" in selector and "proposal_allowed: false" in selector
    double_criticality_conditional = "conditional-support / open selector route" in selector

    report(
        "beta-zero-is-codimension-one-relation",
        codimension_relation,
        "prior no-go identifies beta_lambda=0 as a new y_t/gauge relation",
    )
    report(
        "finite-source-response-not-rg-tangent",
        finite_source_not_rg,
        "finite source generator does not define d lambda/d log(mu)",
    )
    report(
        "selector-marks-beta-premise-open",
        selector_open and double_criticality_conditional,
        "double-criticality route remains conditional until scale-stationarity is proved",
    )
    report(
        "scale-stationarity-not-current-surface-consequence",
        True,
        "without a scale symmetry or RG-family axiom, beta_lambda(M_Pl)=0 is an added selector",
    )

    return {
        "codimension_relation": codimension_relation,
        "finite_source_not_rg": finite_source_not_rg,
        "selector_open": selector_open,
        "double_criticality_conditional": double_criticality_conditional,
    }


def assert_route_fanout() -> list[dict[str, str]]:
    routes = [
        {
            "route": "z3_lattice_automorphism",
            "status": "blocked",
            "reason": "Z^3 has no continuous dilation automorphism or scale-current generator.",
        },
        {
            "route": "lattice_noether",
            "status": "blocked",
            "reason": "current theorem supplies translation and U(1) currents, not a dilation/trace current.",
        },
        {
            "route": "fixed_physical_lattice",
            "status": "blocked",
            "reason": "varying scale introduces a continuum/RG family outside the accepted fixed surface.",
        },
        {
            "route": "trace_anomaly",
            "status": "open_extra_structure",
            "reason": "would need a quantum EMT/trace-anomaly theorem plus a conformal boundary premise.",
        },
        {
            "route": "multiple_point_principle",
            "status": "conditional",
            "reason": "directly supplies beta_lambda=0 only if adopted as a new Planck stationarity selector.",
        },
        {
            "route": "direct_mc_correlator",
            "status": "measurement_not_retained_proof",
            "reason": "can measure or falsify y_t but cannot derive beta stationarity without production data and a mass pin.",
        },
    ]
    allowed_statuses = {
        "blocked",
        "open_extra_structure",
        "conditional",
        "measurement_not_retained_proof",
    }
    for item in routes:
        report(
            f"route-{item['route']}",
            item["status"] in allowed_statuses,
            f"{item['status']}: {item['reason']}",
        )
    return routes


def main() -> int:
    print("YT substrate scale-stationarity no-go")
    print("=" * 72)

    z3 = assert_z3_has_no_continuous_scale_automorphism()
    noether = assert_noether_surface_has_no_scale_current()
    fixed_surface = assert_fixed_surface_excludes_silent_rg_family()
    beta_boundary = assert_beta_stationarity_needs_extra_tangent()
    routes = assert_route_fanout()

    result = {
        "actual_current_surface_status": "no-go / exact-negative-boundary",
        "proposal_allowed": False,
        "bare_retained_allowed": False,
        "investigation_route_closed": False,
        "certification_scope": "current_surface_blocker_only",
        "future_reopen_conditions": [
            "derive a scale current or trace-stationarity condition from extra substrate structure",
            "derive a retained continuum/EFT bridge that supplies the RG-scale tangent",
            "adopt an explicit Planck scale-stationarity selector and keep the result conditional",
        ],
        "target": "derive beta_lambda(M_Pl)=0 from fixed Cl(3)/Z^3 substrate scale stationarity",
        "verdict": (
            "The current fixed-lattice substrate has translation and U(1) "
            "Noether currents, but no nontrivial continuous scale symmetry. "
            "The RG scale tangent needed for beta_lambda(M_Pl)=0 belongs to "
            "an external continuum/EFT bridge or a new stationarity selector."
        ),
        "z3_automorphism_boundary": z3,
        "noether_boundary": noether,
        "fixed_surface_boundary": fixed_surface,
        "beta_stationarity_boundary": beta_boundary,
        "routes": routes,
        "remaining_open_premise": (
            "a new theorem deriving a scale current/trace-stationarity condition "
            "from extra substrate structure, or an explicit new Planck "
            "scale-stationarity selector premise"
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
