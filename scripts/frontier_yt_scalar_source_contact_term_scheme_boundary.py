#!/usr/bin/env python3
"""
PR #230 scalar source contact-term scheme boundary.

This runner checks another tempting scalar-LSZ shortcut: using a chosen
source-curvature renormalization condition as a substitute for the same-source
pole residue.  Local J^2 contact terms in the source functional can shift
analytic low-momentum curvature data without fixing the isolated pole residue.
Therefore a contact-renormalized C_ss(0) or C_ss'(0) convention cannot replace
the LSZ pole-residue measurement needed for kappa_s.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FH_LSZ_INVARIANT = ROOT / "outputs" / "yt_fh_lsz_invariant_readout_theorem_2026-05-01.json"
SPECTRAL_NO_GO = ROOT / "outputs" / "yt_scalar_spectral_saturation_no_go_2026-05-01.json"
BS_DEGENERACY = ROOT / "outputs" / "yt_scalar_bs_kernel_residue_degeneracy_2026-05-01.json"
RENORM_OVERLAP = ROOT / "outputs" / "yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json"

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


def contact_terms_for_low_q_targets(
    *, pole_residue: float, pole_mass_sq: float, target_c0: float, target_c1: float
) -> tuple[float, float]:
    """Return a,b for C(x)=Z/(x+m^2)+a+b*x with fixed C(0), C'(0)."""

    contact_a = target_c0 - pole_residue / pole_mass_sq
    contact_b = target_c1 + pole_residue / (pole_mass_sq * pole_mass_sq)
    return contact_a, contact_b


def model(pole_residue: float, target_c0: float, target_c1: float) -> dict[str, float]:
    pole_mass_sq = 1.0
    contact_a, contact_b = contact_terms_for_low_q_targets(
        pole_residue=pole_residue,
        pole_mass_sq=pole_mass_sq,
        target_c0=target_c0,
        target_c1=target_c1,
    )
    source_overlap = math.sqrt(pole_residue)
    canonical_y_h = 0.8
    d_e_dh = canonical_y_h / math.sqrt(2.0)
    d_e_ds = source_overlap * d_e_dh
    contact_normalized_wrong_readout = d_e_ds / math.sqrt(target_c0)
    pole_residue_readout = d_e_ds / math.sqrt(pole_residue)
    return {
        "pole_residue": pole_residue,
        "pole_mass_squared": pole_mass_sq,
        "source_overlap_sqrt_residue": source_overlap,
        "contact_a": contact_a,
        "contact_b": contact_b,
        "C0_after_contact": target_c0,
        "C1_after_contact": target_c1,
        "dE_dh": d_e_dh,
        "dE_ds": d_e_ds,
        "wrong_readout_using_contact_C0": contact_normalized_wrong_readout,
        "same_source_pole_residue_readout": pole_residue_readout,
    }


def main() -> int:
    print("PR #230 scalar source contact-term scheme boundary")
    print("=" * 72)

    parents = {
        "fh_lsz_invariant_readout": load_json(FH_LSZ_INVARIANT),
        "scalar_spectral_saturation": load_json(SPECTRAL_NO_GO),
        "bs_kernel_residue_degeneracy": load_json(BS_DEGENERACY),
        "renormalization_condition_overlap": load_json(RENORM_OVERLAP),
    }
    parent_paths = {
        "fh_lsz_invariant_readout": FH_LSZ_INVARIANT,
        "scalar_spectral_saturation": SPECTRAL_NO_GO,
        "bs_kernel_residue_degeneracy": BS_DEGENERACY,
        "renormalization_condition_overlap": RENORM_OVERLAP,
    }
    for name, data in parents.items():
        report(f"{name}-loaded", bool(data), str(parent_paths[name].relative_to(ROOT)))

    target_c0 = 1.0
    target_c1 = -0.25
    pole_residues = [0.25, 1.0, 4.0]
    models = [model(residue, target_c0, target_c1) for residue in pole_residues]

    same_low_q_scheme = (
        len({round(row["C0_after_contact"], 12) for row in models}) == 1
        and len({round(row["C1_after_contact"], 12) for row in models}) == 1
    )
    residue_varies = max(pole_residues) / min(pole_residues) == 16.0
    wrong_readouts = [row["wrong_readout_using_contact_C0"] for row in models]
    correct_readouts = [row["same_source_pole_residue_readout"] for row in models]
    wrong_spread = (max(wrong_readouts) - min(wrong_readouts)) / max(sum(wrong_readouts) / len(wrong_readouts), 1e-30)
    correct_spread = max(correct_readouts) - min(correct_readouts)
    parents_keep_open = all(data.get("proposal_allowed") is False for data in parents.values())

    report("parents-keep-proposal-closed", parents_keep_open, "all parent certificates proposal_allowed=false")
    report("low-q-curvature-scheme-held-fixed", same_low_q_scheme, f"C0={target_c0}, C1={target_c1}")
    report("pole-residue-varies-under-contact-scheme", residue_varies, f"residues={pole_residues}")
    report(
        "contact-normalized-readout-varies",
        wrong_spread > 1.0,
        f"wrong_readouts={wrong_readouts}, relative_spread={wrong_spread:.6g}",
    )
    report(
        "pole-residue-readout-remains-fixed",
        correct_spread < 1e-12,
        f"pole_readouts={correct_readouts}",
    )
    report(
        "not-retained-closure",
        True,
        "source contact renormalization is a scheme convention, not an LSZ pole-residue theorem",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / scalar source contact-term scheme boundary",
        "verdict": (
            "A local source contact term can enforce the same low-momentum "
            "source-curvature convention C_ss(0), C_ss'(0) for different "
            "isolated pole residues.  The contact-normalized curvature surface "
            "therefore does not determine the source overlap or kappa_s.  The "
            "same-source pole-residue readout remains invariant only when the "
            "actual pole residue Res C_ss is included.  PR #230 cannot replace "
            "the scalar LSZ pole measurement with a source-curvature "
            "renormalization convention."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Contact-renormalized low-q source curvature is a scheme choice and does not derive Res C_ss."
        ),
        "parent_certificates": {name: str(path.relative_to(ROOT)) for name, path in parent_paths.items()},
        "contact_scheme": {
            "C0_target": target_c0,
            "C1_target": target_c1,
            "model_form": "C(x)=Z/(x+m_H^2)+a+b*x",
        },
        "models": models,
        "strict_non_claims": [
            "does not add a source contact counterterm to A_min",
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
            "does not treat reduced pilots as production evidence",
        ],
        "exact_next_action": (
            "Use an isolated same-source pole-residue fit/theorem; do not use "
            "contact-renormalized C_ss(0) or C_ss'(0) as the source-to-Higgs normalization."
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
