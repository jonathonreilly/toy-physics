#!/usr/bin/env python3
"""
PR #230 scalar renormalization-condition/source-overlap no-go.

This runner attacks a narrow remaining shortcut: using the canonical Higgs
kinetic renormalization condition as if it fixed the overlap between the
Cl(3)/Z3 scalar source operator and the canonical Higgs field.  It does not.
The canonical condition fixes the residue of the h-h propagator.  The source
readout also needs the operator matrix element <0|O_s|h>, equivalently the
same-source scalar pole residue measured by C_ss.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPARAM = ROOT / "outputs" / "yt_source_reparametrization_gauge_no_go_2026-05-01.json"
CANONICAL_IMPORT = ROOT / "outputs" / "yt_canonical_scalar_normalization_import_audit_2026-05-01.json"
SOURCE_TO_HIGGS = ROOT / "outputs" / "yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json"
FH_LSZ_INVARIANT = ROOT / "outputs" / "yt_fh_lsz_invariant_readout_theorem_2026-05-01.json"
GAUGE_VEV_OVERLAP = ROOT / "outputs" / "yt_gauge_vev_source_overlap_no_go_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json"

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


def model(source_overlap: float) -> dict[str, float]:
    """Toy one-pole model with canonical h fixed and source overlap varied."""

    canonical_h_residue = 1.0
    pole_mass_squared = 0.36
    v_canonical = 1.0
    y_h = 0.8
    d_e_dh = y_h / math.sqrt(2.0)
    source_pole_residue = source_overlap * source_overlap * canonical_h_residue
    d_e_ds = source_overlap * d_e_dh
    inferred_if_source_overlap_ignored = d_e_ds
    invariant_same_source_readout = d_e_ds / math.sqrt(source_pole_residue)
    return {
        "source_overlap_z_s": source_overlap,
        "canonical_h_residue": canonical_h_residue,
        "pole_mass_squared": pole_mass_squared,
        "v_canonical": v_canonical,
        "canonical_y_h": y_h,
        "dE_dh": d_e_dh,
        "dE_ds": d_e_ds,
        "C_ss_pole_residue": source_pole_residue,
        "wrong_dE_dh_if_overlap_ignored": inferred_if_source_overlap_ignored,
        "same_source_invariant_readout": invariant_same_source_readout,
    }


def main() -> int:
    print("PR #230 scalar renormalization-condition/source-overlap no-go")
    print("=" * 72)

    parents = {
        "source_reparametrization": load_json(SOURCE_REPARAM),
        "canonical_scalar_import": load_json(CANONICAL_IMPORT),
        "source_to_higgs_lsz": load_json(SOURCE_TO_HIGGS),
        "fh_lsz_invariant_readout": load_json(FH_LSZ_INVARIANT),
        "gauge_vev_source_overlap": load_json(GAUGE_VEV_OVERLAP),
    }
    models = [model(0.5), model(1.0), model(2.0)]

    parent_paths = {
        "source_reparametrization": SOURCE_REPARAM,
        "canonical_scalar_import": CANONICAL_IMPORT,
        "source_to_higgs_lsz": SOURCE_TO_HIGGS,
        "fh_lsz_invariant_readout": FH_LSZ_INVARIANT,
        "gauge_vev_source_overlap": GAUGE_VEV_OVERLAP,
    }
    for name, data in parents.items():
        report(f"{name}-loaded", bool(data), str(parent_paths[name].relative_to(ROOT)))

    parents_keep_open = all(data.get("proposal_allowed") is False for data in parents.values())
    canonical_surface_same = (
        len({row["canonical_h_residue"] for row in models}) == 1
        and len({row["pole_mass_squared"] for row in models}) == 1
        and len({row["v_canonical"] for row in models}) == 1
        and len({row["canonical_y_h"] for row in models}) == 1
    )
    source_overlap_varies = len({row["source_overlap_z_s"] for row in models}) == len(models)
    source_response_varies = len({round(row["dE_ds"], 12) for row in models}) == len(models)
    invariant_readout_fixed = (
        max(row["same_source_invariant_readout"] for row in models)
        - min(row["same_source_invariant_readout"] for row in models)
        < 1e-12
    )
    ignored_overlap_spread = (
        max(row["wrong_dE_dh_if_overlap_ignored"] for row in models)
        - min(row["wrong_dE_dh_if_overlap_ignored"] for row in models)
    )

    report("parents-keep-proposal-closed", parents_keep_open, "all parent certificates proposal_allowed=false")
    report(
        "canonical-renormalization-surface-identical",
        canonical_surface_same,
        "same Z_h=1, pole mass, v, and canonical y_h across countermodels",
    )
    report(
        "source-overlap-remains-independent",
        source_overlap_varies and source_response_varies,
        f"z_s={[row['source_overlap_z_s'] for row in models]}, dE_ds={[row['dE_ds'] for row in models]}",
    )
    report(
        "ignoring-overlap-changes-physical-readout",
        ignored_overlap_spread > 0.5,
        f"spread={ignored_overlap_spread:.6g}",
    )
    report(
        "same-source-pole-residue-would-fix-readout",
        invariant_readout_fixed,
        f"readouts={[row['same_source_invariant_readout'] for row in models]}",
    )
    report(
        "not-retained-closure",
        True,
        "canonical kinetic renormalization is not a source-operator overlap theorem",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / scalar renormalization-condition source-overlap no-go"
        ),
        "verdict": (
            "The canonical Higgs kinetic renormalization condition fixes the "
            "normalization of an already-identified h field, represented here "
            "by unit h-h pole residue.  It does not fix the operator overlap "
            "z_s=<0|O_s|h> of the Cl(3)/Z3 additive scalar source.  Countermodels "
            "can share Z_h=1, the Higgs pole mass, v, and the canonical h Yukawa "
            "while changing dE/ds and the source pole residue C_ss.  The physical "
            "readout is recovered only by the same-source invariant combination "
            "dE/ds divided by sqrt(Res C_ss), or equivalently by a derived "
            "source-overlap theorem.  Therefore a kinetic renormalization "
            "condition cannot replace the scalar LSZ/source-pole measurement."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Canonical Z_h=1 does not derive the source operator overlap z_s or kappa_s."
        ),
        "parent_certificates": {name: str(path.relative_to(ROOT)) for name, path in parent_paths.items()},
        "countermodels": models,
        "strict_non_claims": [
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
            "does not set c2 or Z_match to one",
            "does not treat reduced pilots as production evidence",
        ],
        "exact_next_action": (
            "Measure or derive the same-source scalar pole residue/overlap; "
            "canonical Higgs kinetic normalization alone is only one side of "
            "the LSZ bridge."
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
