#!/usr/bin/env python3
"""
PR #230 FH/LSZ scalar-pole fit kinematics gate.

The same-source FH/LSZ readout requires d Gamma_ss / dp^2 at an isolated
scalar pole.  The current production manifests measure C_ss(q) at q=0 and
three axis-equivalent one-step spatial modes.  This runner verifies that those
kinematics are a finite-difference scout only: they provide one nonzero
momentum shell, not enough data to identify a pole location, pole derivative,
or continuum remainder without an imported model.
"""

from __future__ import annotations

import json
import math
import shlex
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_MANIFEST = ROOT / "outputs" / "yt_fh_lsz_production_manifest_2026-05-01.json"
CHUNK_MANIFEST = ROOT / "outputs" / "yt_fh_lsz_chunked_production_manifest_2026-05-01.json"
POSTPROCESS_GATE = ROOT / "outputs" / "yt_fh_lsz_production_postprocess_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_pole_fit_kinematics_gate_2026-05-01.json"

MIN_DISTINCT_SHELLS_FOR_POLE_FIT = 4
MIN_NONZERO_SHELLS_FOR_POLE_FIT = 3

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


def arg_after(tokens: list[str], flag: str) -> str | None:
    prefix = f"{flag}="
    for index, token in enumerate(tokens):
        if token == flag and index + 1 < len(tokens):
            return tokens[index + 1]
        if token.startswith(prefix):
            return token[len(prefix) :]
    return None


def parse_modes(command: str) -> list[tuple[int, int, int]]:
    tokens = shlex.split(command)
    raw = arg_after(tokens, "--scalar-two-point-modes")
    if raw is None:
        return []
    modes = []
    for item in raw.split(";"):
        if not item.strip():
            continue
        parts = [int(value.strip()) for value in item.split(",")]
        if len(parts) != 3:
            continue
        modes.append((parts[0], parts[1], parts[2]))
    return modes


def parse_spatial_l(command: str) -> int | None:
    tokens = shlex.split(command)
    raw = arg_after(tokens, "--volumes")
    if raw is None:
        return None
    spatial = raw.lower().split("x", 1)[0]
    try:
        return int(spatial)
    except ValueError:
        return None


def p_hat_sq(mode: tuple[int, int, int], spatial_l: int) -> float:
    return sum((2.0 * math.sin(math.pi * n / spatial_l)) ** 2 for n in mode)


def analyze_command(command: str) -> dict[str, Any]:
    spatial_l = parse_spatial_l(command)
    modes = parse_modes(command)
    if spatial_l is None:
        return {"spatial_l": None, "modes": modes, "issues": ["missing spatial volume"]}
    shells = sorted({round(p_hat_sq(mode, spatial_l), 12) for mode in modes})
    nonzero_shells = [value for value in shells if abs(value) > 1.0e-12]
    return {
        "spatial_l": spatial_l,
        "modes": [list(mode) for mode in modes],
        "mode_count": len(modes),
        "distinct_p_hat_sq_shells": shells,
        "distinct_shell_count": len(shells),
        "nonzero_shell_count": len(nonzero_shells),
        "has_zero_shell": any(abs(value) <= 1.0e-12 for value in shells),
        "pole_fit_kinematics_ready": (
            len(shells) >= MIN_DISTINCT_SHELLS_FOR_POLE_FIT
            and len(nonzero_shells) >= MIN_NONZERO_SHELLS_FOR_POLE_FIT
        ),
    }


def command_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    if not manifest:
        return []
    rows = manifest.get("commands")
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    examples = manifest.get("example_commands")
    if isinstance(examples, list):
        return [row for row in examples if isinstance(row, dict)]
    return []


def main() -> int:
    print("PR #230 FH/LSZ scalar-pole fit kinematics gate")
    print("=" * 72)

    production = load_json(PRODUCTION_MANIFEST)
    chunked = load_json(CHUNK_MANIFEST)
    postprocess = load_json(POSTPROCESS_GATE)
    production_rows = command_rows(production)
    chunk_rows = command_rows(chunked)
    production_analyses = [analyze_command(str(row.get("command", ""))) for row in production_rows]
    chunk_analyses = [analyze_command(str(row.get("command", ""))) for row in chunk_rows]
    all_analyses = production_analyses + chunk_analyses

    all_have_modes = bool(all_analyses) and all(item.get("mode_count", 0) > 0 for item in all_analyses)
    all_have_only_one_nonzero_shell = bool(all_analyses) and all(
        item.get("nonzero_shell_count") == 1 for item in all_analyses
    )
    none_pole_fit_ready = bool(all_analyses) and not any(
        item.get("pole_fit_kinematics_ready") for item in all_analyses
    )
    postprocess_requires_pole = "isolated_scalar_pole_and_inverse_derivative_fit" in str(
        postprocess.get("postprocess_requirements", "")
    )

    report("production-manifest-loaded", bool(production), str(PRODUCTION_MANIFEST.relative_to(ROOT)))
    report("chunk-manifest-loaded", bool(chunked), str(CHUNK_MANIFEST.relative_to(ROOT)))
    report("scalar-modes-present", all_have_modes, f"analyses={len(all_analyses)}")
    report(
        "current-modes-one-nonzero-shell-only",
        all_have_only_one_nonzero_shell,
        "axis modes are degenerate p_hat^2 shells",
    )
    report(
        "current-kinematics-not-pole-fit-ready",
        none_pole_fit_ready,
        f"required_shells={MIN_DISTINCT_SHELLS_FOR_POLE_FIT}, required_nonzero={MIN_NONZERO_SHELLS_FOR_POLE_FIT}",
    )
    report("postprocess-gate-requires-isolated-pole", postprocess_requires_pole, "pole derivative is already a hard gate")
    report("not-retained-closure", True, "finite positive-p^2 secant is not dGamma/dp^2 at an isolated pole")

    result = {
        "actual_current_surface_status": "open / FH-LSZ scalar-pole kinematics gate blocks four-mode manifest as pole-fit evidence",
        "verdict": (
            "The current FH/LSZ production and chunk manifests measure the "
            "scalar two-point object at q=0 plus three axis-equivalent one-step "
            "spatial modes.  On each volume this is only two distinct p_hat^2 "
            "shells, with one nonzero shell.  That can form a finite "
            "positive-momentum secant, but it cannot locate an isolated scalar "
            "pole, determine dGamma_ss/dp^2 at that pole, or bound continuum "
            "remainders without importing a model.  Completed chunks therefore "
            "still need a richer pole-fit postprocess or a theorem before they "
            "can contribute to a retained y_t proposal."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The current four-mode scalar-LSZ kinematics are finite-difference support only, not an isolated-pole derivative.",
        "production_manifest": str(PRODUCTION_MANIFEST.relative_to(ROOT)),
        "chunk_manifest": str(CHUNK_MANIFEST.relative_to(ROOT)),
        "production_analyses": production_analyses,
        "chunk_analyses": chunk_analyses,
        "minimum_pole_fit_requirements": {
            "distinct_p_hat_sq_shells": MIN_DISTINCT_SHELLS_FOR_POLE_FIT,
            "nonzero_shells": MIN_NONZERO_SHELLS_FOR_POLE_FIT,
            "plus": [
                "isolated scalar pole or controlled analytic continuation class",
                "finite-volume/IR/zero-mode limiting control",
                "same-source provenance matching the FH response source",
                "no fitted selector, kappa_s=1, H_unit, observed target, alpha/plaquette/u0, c2=1, or Z_match=1 proof input",
            ],
        },
        "strict_non_claims": [
            "does not reject the chunks as measurement support",
            "does not treat four-mode finite differences as a pole derivative",
            "does not claim retained or proposed_retained closure",
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
