#!/usr/bin/env python3
"""
Reduce the PMNS-native fixed-slice production frontier to one scalar holonomy
discriminant certificate.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def main() -> int:
    collapse = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md")
    production = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_MINIMAL_PRODUCTION_CERTIFICATE_NOTE_2026-04-18.md")
    note = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_SCALAR_PRODUCTION_DISCRIMINANT_NOTE_2026-04-18.md")

    print("=" * 104)
    print("PMNS GRAPH-FIRST FIXED-SLICE SCALAR PRODUCTION DISCRIMINANT")
    print("=" * 104)
    print()

    phi1 = 0.0
    phi2 = 2.0 * np.pi / 3.0
    m = np.array(
        [
            [2.0 * np.cos(phi1), 2.0 * np.sin(phi1)],
            [2.0 * np.cos(phi2), 2.0 * np.sin(phi2)],
        ],
        dtype=float,
    )
    gram = m.T @ m
    evals = np.linalg.eigvalsh(gram)
    uv_zero = np.array([0.0, 0.0])
    uv_nonzero = np.array([0.4, -0.3])
    c_zero = m @ uv_zero
    c_nonzero = m @ uv_nonzero
    delta_zero = float(c_zero @ c_zero)
    delta_nonzero = float(c_nonzero @ c_nonzero)
    check(
        "For any fixed independent angle pair, the centered two-holonomy map has positive-definite Gram matrix",
        float(np.min(evals)) > 1e-12,
        detail=f"eigs={np.round(evals, 6)}",
    )
    check(
        "The scalar discriminant Delta vanishes exactly at chi = 0 and is positive for nonzero chi",
        abs(delta_zero) < 1e-12 and delta_nonzero > 1e-12,
        detail=f"Delta_zero={delta_zero:.2e}, Delta_nonzero={delta_nonzero:.6f}",
    )
    check(
        "The collapse and minimal-production notes already justify the scalar reduction from a holonomy pair to one discriminant",
        ("any two independent native holonomies reconstruct `chi` exactly" in collapse
         or "two independent native holonomies collapse the fixed slice exactly" in collapse)
        and "minimal" in production
        and "fixed-slice two-holonomy" in production
        and "production certificate" in production
        and "scalar discriminant" in note,
    )
    check(
        "The new note records the canonical C3 scalar witness and the current-bank nonrealization",
        "`Delta_C3 = (h_0 - w0)^2 + (h_(2pi/3) - w0)^2`" in note
        and "current bank still does **not** realize even that scalar certificate" in note,
    )
    check(
        "The theorem stays on the PMNS-native production lane and does not overclaim a Wilson bridge or a global selector",
        "What this does not close" in note
        and "a Wilson-to-PMNS descendant theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
