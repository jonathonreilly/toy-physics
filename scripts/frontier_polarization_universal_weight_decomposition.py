#!/usr/bin/env python3
"""Decompose the universal complement under the shared-axis SO(2) stabilizer.

After the glue reduction, the remaining connected common gauge is rotation
around the shared bright axis. This runner decomposes the universal symmetric
`3+1` complement under that stabilizer and identifies the available weight
sectors.

This is useful for the phase-lift problem because the support dark phase has
charge 1 under the residual SO(2), so any canonical universal lift must land
in a weight-1 sector.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
U = SourceFileLoader(
    "universal_conn",
    str(ROOT / "scripts" / "frontier_universal_gr_canonical_projector_connection.py"),
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def main() -> int:
    Gx = U.generator("x")
    projector = U.pi_a1()
    # Remove A1 core, keep complement.
    comp_idx = [i for i in range(10) if i not in (0, 4)]
    Gc = Gx[np.ix_(comp_idx, comp_idx)]

    vals, _ = np.linalg.eig(Gc)
    weights = sorted(round(abs(v.imag), 6) for v in vals if abs(v) > 1e-8)

    # Identify obvious invariant/weight-1 blocks directly from the x-rotation rep.
    Rx = U.rep_matrix(U.rotation("x", math.pi / 6.0), U.canonical_polarization_frame())
    # complement indices in canonical basis:
    # 1 shift_x, 2 shift_y, 3 shift_z, 5 shear1, 6 shear2, 7 h12, 8 h13, 9 h23
    shift_yz = Rx[np.ix_([2, 3], [2, 3])]
    offdiag_x = Rx[np.ix_([7, 8], [7, 8])]
    shear_block = Rx[np.ix_([5, 6, 9], [5, 6, 9])]

    shift_err = float(np.max(np.abs(shift_yz - np.array([[math.cos(math.pi / 6.0), math.sin(math.pi / 6.0)], [-math.sin(math.pi / 6.0), math.cos(math.pi / 6.0)]]))))
    offdiag_err = float(np.max(np.abs(offdiag_x - np.array([[math.cos(math.pi / 6.0), math.sin(math.pi / 6.0)], [-math.sin(math.pi / 6.0), math.cos(math.pi / 6.0)]]))))
    shear_eval = np.linalg.eigvals(shear_block)
    shear_weights = sorted(round(abs(np.angle(v) / (math.pi / 6.0)), 6) for v in shear_eval if abs(v - 1.0) > 1e-8)

    invariant_dim = int(sum(abs(v) < 1e-8 for v in vals))
    weight1_mult = int(sum(abs(abs(v.imag) - 1.0) < 1e-6 for v in vals))
    weight2_mult = int(sum(abs(abs(v.imag) - 2.0) < 1e-6 for v in vals))

    print("POLARIZATION UNIVERSAL WEIGHT DECOMPOSITION")
    print("=" * 78)
    print(f"complement weights(abs imag eigvals) = {weights}")
    print(f"invariant dim = {invariant_dim}")
    print(f"weight-1 multiplicity = {weight1_mult}")
    print(f"weight-2 multiplicity = {weight2_mult}")
    print(f"shift_yz block error = {shift_err:.3e}")
    print(f"offdiag_x block error = {offdiag_err:.3e}")
    print(f"shear block phase weights ~ {shear_weights}")

    record(
        "the universal complement under the shared-axis stabilizer has nontrivial weight decomposition",
        invariant_dim >= 2 and weight1_mult >= 4 and weight2_mult >= 2,
        f"invariant={invariant_dim}, weight1={weight1_mult}, weight2={weight2_mult}",
    )
    record(
        "the shift-yz pair is an exact weight-1 SO(2) doublet",
        shift_err < 1e-12,
        f"block error={shift_err:.3e}",
    )
    record(
        "the x-offdiagonal shear pair is an exact weight-1 SO(2) doublet",
        offdiag_err < 1e-12,
        f"block error={offdiag_err:.3e}",
    )
    record(
        "the remaining shear block contains a weight-2 sector",
        any(abs(w - 2.0) < 1e-6 for w in shear_weights),
        f"shear weights={shear_weights}",
    )

    print("\nVerdict:")
    print(
        "Under the shared-axis SO(2) stabilizer, the universal complement is not "
        "featureless. It contains two exact weight-1 doublets and a separate "
        "weight-2 shear sector. Since the support dark phase carries charge 1, "
        "any canonical universal lift must land in a weight-1 sector, not in the "
        "weight-2 shear block."
    )
    print(
        "So the curvature-side phase-lift problem is narrowed again: the missing "
        "primitive is not an arbitrary localization on the full complement, but a "
        "canonical choice among the universal weight-1 sectors."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
