#!/usr/bin/env python3
"""Bounded regression gate for the current canonical frontier.

This is not a physics-proof script. It is a cheap drift detector for the
artifact-backed frontier that the repo currently presents as canonical.

The gate intentionally checks only review-safe conditions:
  - machine-clean Born / k=0 thresholds where those are retained
  - retained verdict strings on narrow branch reconciliations
  - presence of hierarchy-aligned support where the notes depend on it
  - absence of obvious runtime / formatting regressions

It does not try to re-prove the science or replace the script/log/note chain.
"""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable


class GateFailure(RuntimeError):
    """Raised when a canonical regression check fails."""


def run_script(path: str, *args: str, timeout: int = 240) -> str:
    proc = subprocess.run(
        [PYTHON, str(REPO_ROOT / path), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if proc.returncode != 0:
        raise GateFailure(
            f"{path} failed with exit code {proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateFailure(message)


def extract_float(pattern: str, text: str, label: str) -> float:
    match = re.search(pattern, text)
    if not match:
        raise GateFailure(f"missing {label}")
    return float(match.group(1))


def check_dense_3d_card() -> None:
    out = run_script("scripts/lattice_3d_dense_10prop.py")
    born = extract_float(r"1\. Born \|I3\|/P = ([0-9.eE+-]+)", out, "3D dense Born")
    k0 = extract_float(r"3\. k=0 = ([0-9.eE+-]+)", out, "3D dense k=0")
    mi = extract_float(r"7\. MI = ([0-9.eE+-]+) bits", out, "3D dense MI")
    decoh = extract_float(r"6\. Decoherence = ([0-9.eE+-]+)%", out, "3D dense decoherence")
    require(born < 1e-10, f"3D dense Born drifted: {born}")
    require(abs(k0) < 1e-12, f"3D dense k=0 drifted: {k0}")
    require(mi > 0.05, f"3D dense MI unexpectedly weak: {mi}")
    require(decoh > 5.0, f"3D dense decoherence unexpectedly weak: {decoh}%")
    require("Grows with N: YES  [PASS]" in out, "3D dense N-growth verdict changed")
    require("Hierarchy-aligned support: 4/4" in out, "3D dense hierarchy support changed")


def check_dense_3d_extension() -> None:
    out = run_script("scripts/lattice_3d_dense_window_extension.py")
    require("Decision: BOUNDED EXTENSION." in out, "3D dense extension verdict changed")
    require("z=6" in out, "3D dense extension no longer reports the z=6 boundary")
    require("z=7 is signal-free / mixed" in out, "3D dense extension boundary wording changed")
    require(
        re.search(r"^\s*6\s+\+0\.[0-9]+\s+\+0\.[0-9]+\s+\+0\.[0-9]+\s+6\.[0-9]+e-16", out, re.MULTILINE)
        is not None,
        "3D dense z=6 retained row missing",
    )
    require(
        re.search(r"^\s*7\s+\+0\.000000\s+\+0\.000000\s+\+nan", out, re.MULTILINE) is not None,
        "3D dense z=7 boundary row changed",
    )


def check_dense_3d_reconciliation() -> None:
    out = run_script("scripts/lattice_3d_dense_refinement_reconciliation.py")
    match_h1 = re.search(r"h = 1\.0.*?Born=([0-9.eE+-]+)", out, re.S)
    match_h05 = re.search(r"h = 0\.5.*?Born=([0-9.eE+-]+)", out, re.S)
    if not match_h1:
        raise GateFailure("missing reconciliation h=1 Born")
    if not match_h05:
        raise GateFailure("missing reconciliation h=0.5 Born")
    born_h1 = float(match_h1.group(1))
    born_h05 = float(match_h05.group(1))
    require(born_h1 < 1e-10, f"reconciliation h=1 Born drifted: {born_h1}")
    require(born_h05 < 1e-10, f"reconciliation h=0.5 Born drifted: {born_h05}")
    require("Verdict: FAILS." in out, "dense refinement reconciliation verdict changed")
    require("attractive distance rows=5/5" in out, "h=1.0 attraction-support count changed")
    require("attractive distance rows=0/5" in out, "h=0.5 attraction-support count changed")


def check_gravity_hierarchy() -> None:
    out = run_script("scripts/gravity_observable_hierarchy.py")
    require("2D dense spent-delay                ultra-weak retained" in out, "missing 2D retained hierarchy row")
    require("3D dense spent-delay                retained dense z=3" in out, "missing 3D dense z=3 hierarchy row")
    require("3D power-action close-slit barrier  retained barrier card" in out, "missing 3D power barrier hierarchy row")
    require("genuine attraction" in out, "missing attraction interpretation in hierarchy output")
    require("away / depletion" in out, "missing depletion interpretation in hierarchy output")


def check_structured_bridge() -> None:
    out = run_script("scripts/structured_chokepoint_bridge.py")
    born_values = [float(m) for m in re.findall(r"\s([0-9]+\.[0-9]+e[+-][0-9]+)\s+\+0\.00e\+00", out)]
    require(born_values, "structured bridge Born values missing")
    require(all(v < 1e-10 for v in born_values), f"structured bridge Born drifted: {born_values}")
    require("DECISION: retained structured bridge pocket" in out, "structured bridge verdict changed")
    require(re.search(r"^\s*60\s+0\.[0-9]+\s+0\.8030±0\.04", out, re.MULTILINE) is not None,
            "structured bridge retained N=60 row changed materially")


def check_structured_bridge_extension() -> None:
    out = run_script("scripts/structured_chokepoint_bridge_extension.py")
    require(
        "The structured bridge widens beyond the current narrow slice" in out,
        "structured bridge extension verdict changed",
    )
    require(
        re.search(
            r"^\s*80\s+0\.6925\s+0\.7712±0\.03\s+0\.9910\s+\+4\.3840±0\.666\s+0\.0000±0\.00\s+\+0\.00e\+00\s+16",
            out,
            re.MULTILINE,
        )
        is not None,
        "structured bridge extension retained N=80 row changed materially",
    )
    require(
        re.search(
            r"^\s*100\s+0\.6947\s+0\.8056±0\.03\s+1\.0158\s+\+2\.9007±1\.054\s+0\.0000±0\.00\s+\+0\.00e\+00\s+16",
            out,
            re.MULTILINE,
        )
        is not None,
        "structured bridge extension retained N=100 row changed materially",
    )


def check_mirror_2d_validation() -> None:
    out = run_script("scripts/mirror_2d_validation.py")
    require("seeds=8" in out, "mirror 2D validation default seed count drifted from the retained artifact")
    born = extract_float(r"Born audit: max \|I3\|/P = ([0-9.eE+-]+)", out, "mirror 2D Born")
    require(born < 1e-10, f"mirror 2D Born drifted: {born}")
    require(
        re.search(
            r"^\s*60\s+0\.756118\s+0\.4420\s+0\.8572\s+\+2\.5687\s+1\.08e-15\s+\+0\.00e\+00\s+8$",
            out,
            re.MULTILINE,
        )
        is not None,
        "mirror 2D retained N=60 row changed materially",
    )
    require(
        re.search(
            r"^\s*60\s+0\.050745\s+0\.0596\s+0\.1090\s+\+0\.7867\s+4\.16e-15\s+\+0\.00e\+00\s+8$",
            out,
            re.MULTILINE,
        )
        is not None,
        "mirror 2D random baseline N=60 row changed materially",
    )


def check_mirror_mutual_information() -> None:
    out = run_script("scripts/mirror_mutual_information_chokepoint.py")
    require("npl_half=60 (total 120)" in out, "mirror MI geometry header changed")
    require(
        re.search(
            r"^\s*mirror\s+60\s+0\.1973±0\.041\s+0\.3855\s+0\.8440±0\.03",
            out,
            re.MULTILINE,
        )
        is not None,
        "mirror MI retained N=60 row changed materially",
    )
    require(
        re.search(
            r"^\s*random\s+80\s+0\.0564±0\.018\s+0\.1871\s+0\.9509±0\.02",
            out,
            re.MULTILINE,
        )
        is not None,
        "mirror MI retained random N=80 row changed materially",
    )
    require(
        "Note: if these exponents disagree across N windows, treat them as bounded summaries, not laws." in out,
        "mirror MI bounded-summary guardrail changed",
    )


def check_mirror_chokepoint_baseline() -> None:
    out = run_script("scripts/mirror_chokepoint_joint.py")
    require("NPL_HALF=25 (total 50), k=5.0, 16 seeds" in out, "mirror chokepoint baseline header changed")
    require(
        re.search(
            r"^\s*25\s+mirror p2=0\s+0\.8014\s+0\.7329±0\.05\s+0\.9986\s+\+2\.2748±0\.525\s+6\.54e-16\s+\+0\.00e\+00\s+13",
            out,
            re.MULTILINE,
        )
        is not None,
        "mirror chokepoint retained N=25 row changed materially",
    )
    require(
        re.search(r"^\s*60\s+mirror p2=0\s+FAIL", out, re.MULTILINE) is not None,
        "mirror chokepoint strict N=60 fail row changed",
    )
    require("VALIDATION CRITERIA:" in out, "mirror chokepoint validation footer missing")


def check_mirror_chokepoint_boundary() -> None:
    out = run_script(
        "scripts/mirror_chokepoint_joint.py",
        "--npl-half",
        "60",
        "--connect-radius",
        "5.0",
        "--n-layers",
        "40",
        "60",
        "80",
        "100",
        "120",
        "--layer2-prob",
        "0.0",
        timeout=420,
    )
    require(
        "NPL_HALF=60 (total 120), k=5.0, 16 seeds" in out,
        "mirror chokepoint boundary header changed",
    )
    require(
        re.search(
            r"^\s*80\s+mirror p2=0\s+0\.4291\s+0\.8182±0\.03\s+1\.0029\s+\+3\.0551±0\.672\s+2\.43e-15\s+\+0\.00e\+00\s+16",
            out,
            re.MULTILINE,
        )
        is not None,
        "mirror chokepoint boundary retained N=80 row changed materially",
    )
    require(
        re.search(
            r"^\s*100\s+mirror p2=0\s+0\.2308\s+0\.9043±0\.02\s+1\.0058\s+\+1\.3089±0\.570\s+1\.13e-15\s+\+0\.00e\+00\s+16",
            out,
            re.MULTILINE,
        )
        is not None,
        "mirror chokepoint boundary retained N=100 row changed materially",
    )
    require(
        re.search(
            r"^\s*120\s+mirror p2=0\s+0\.2517\s+0\.8823±0\.04\s+0\.9984\s+\+0\.0000±0\.000\s+nan\s+\+0\.00e\+00\s+11",
            out,
            re.MULTILINE,
        )
        is not None,
        "mirror chokepoint boundary N=120 collapse row changed",
    )
    require("VALIDATION CRITERIA:" in out, "mirror chokepoint boundary validation footer missing")


def check_nn_continuum() -> None:
    out = run_script("scripts/lattice_nn_continuum.py")
    require(
        "SAFE CLAIM: Born-clean positive refinement trend through h = 0.25" in out,
        "NN continuum safe-claim wording changed",
    )
    require(
        re.search(
            r"0\.250\s+25921\s+161\s+\+0\.077415\s+\+0\.00e\+00\s+0\.9470\s+0\.4989\s+0\.9878\s+3\.83e-16",
            out,
        )
        is not None,
        "NN continuum h=0.25 retained row changed materially",
    )
    require("0.125  FAIL" in out, "NN continuum h=0.125 failure row changed")


def check_nn_deterministic_rescale() -> None:
    out = run_script("scripts/lattice_nn_deterministic_rescale.py")
    require(
        re.search(
            r"0\.0625\s+410881\s+641\s+\+0\.014810\s+\+0\.00e\+00\s+1\.0000\s+0\.5000\s+1\.0000\s+[0-9]\.\d{2}e-16",
            out,
        )
        is not None,
        "NN deterministic-rescale h=0.0625 retained row changed materially",
    )
    require(
        "Born-safe extension works only if the Born column stays machine-clean" in out,
        "NN deterministic-rescale interpretation changed",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--slow",
        action="store_true",
        help="include slower supplementary checks such as the large-N mirror boundary extension",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checks = [
        ("mirror 2D validation", check_mirror_2d_validation),
        ("mirror MI chokepoint", check_mirror_mutual_information),
        ("mirror chokepoint baseline", check_mirror_chokepoint_baseline),
        ("dense 3D canonical card", check_dense_3d_card),
        ("dense 3D window extension", check_dense_3d_extension),
        ("dense 3D refinement reconciliation", check_dense_3d_reconciliation),
        ("gravity observable hierarchy", check_gravity_hierarchy),
        ("structured bridge", check_structured_bridge),
        ("structured bridge extension", check_structured_bridge_extension),
        ("NN raw continuum", check_nn_continuum),
        ("NN deterministic rescale", check_nn_deterministic_rescale),
    ]

    print("=" * 88)
    print("CANONICAL REGRESSION GATE")
    print("  Cheap drift checks for the current canonical frontier.")
    if args.slow:
        print("  Slow supplementary checks enabled.")
        checks.append(("mirror chokepoint boundary extension", check_mirror_chokepoint_boundary))
    else:
        print("  Slow supplementary checks skipped. Use --slow for large-N mirror boundary replay.")
    print("=" * 88)

    failed = False
    for label, fn in checks:
        try:
            fn()
            print(f"[PASS] {label}")
        except GateFailure as exc:
            failed = True
            print(f"[FAIL] {label}: {exc}")

    print("=" * 88)
    if failed:
        print("REGRESSION GATE: FAIL")
        raise SystemExit(1)
    print("REGRESSION GATE: PASS")


if __name__ == "__main__":
    main()
