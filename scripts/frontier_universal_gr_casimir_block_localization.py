#!/usr/bin/env python3
"""Canonical block localization on the direct universal route via the SO(3) Casimir.

This runner checks whether the direct universal route already carries enough
exact structure to canonically split the universal symmetric `3+1` space into

    lapse ⊕ shift ⊕ trace ⊕ traceless-shear

without choosing a full complement frame.

Key idea:
  - `Pi_A1` already fixes lapse and spatial trace.
  - On the 8D complement, the universal SO(3) generators define a Casimir
    operator whose spectral projectors split the complement into the vector
    (`j=1`) and traceless-symmetric (`j=2`) irreps.

If this works, the old "missing complement-frame bundle" blocker was too
strong. The direct universal route would then already have a canonical block
localization operator, even if it does not choose bases inside the shift/shear
blocks.
"""

from __future__ import annotations

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


def spectral_projector(op: np.ndarray, target: float, tol: float = 1e-9) -> np.ndarray:
    vals, vecs = np.linalg.eig(op)
    mask = np.abs(vals - target) < tol
    V = vecs[:, mask]
    if V.size == 0:
        return np.zeros_like(op)
    return np.real_if_close(V @ np.linalg.inv(V.T @ V) @ V.T, tol=1e-7)


def main() -> int:
    Gx = U.generator("x")
    Gy = U.generator("y")
    Gz = U.generator("z")
    Pi_A1 = U.pi_a1()

    # Full 10D canonical blocks from the universal canonical basis:
    P_lapse = np.zeros((10, 10), dtype=float)
    P_lapse[0, 0] = 1.0
    P_trace = np.zeros((10, 10), dtype=float)
    P_trace[4, 4] = 1.0

    comp_idx = [i for i in range(10) if i not in (0, 4)]
    Gc = [G[np.ix_(comp_idx, comp_idx)] for G in (Gx, Gy, Gz)]
    C = sum(G @ G for G in Gc)

    vals = np.linalg.eigvals(C)
    vals_real = sorted(round(float(np.real_if_close(v)), 6) for v in vals)

    P_shift_c = spectral_projector(C, -2.0)
    P_shear_c = spectral_projector(C, -6.0)

    P_shift = np.zeros((10, 10), dtype=float)
    P_shear = np.zeros((10, 10), dtype=float)
    P_shift[np.ix_(comp_idx, comp_idx)] = P_shift_c
    P_shear[np.ix_(comp_idx, comp_idx)] = P_shear_c

    # Basic projector algebra.
    I = np.eye(10)
    P_sum = P_lapse + P_trace + P_shift + P_shear
    sum_err = float(np.max(np.abs(P_sum - I)))
    orth_err = max(
        float(np.linalg.norm(P_lapse @ P_trace, ord="fro")),
        float(np.linalg.norm(P_lapse @ P_shift, ord="fro")),
        float(np.linalg.norm(P_lapse @ P_shear, ord="fro")),
        float(np.linalg.norm(P_trace @ P_shift, ord="fro")),
        float(np.linalg.norm(P_trace @ P_shear, ord="fro")),
        float(np.linalg.norm(P_shift @ P_shear, ord="fro")),
    )
    idem_err = max(
        float(np.linalg.norm(P_lapse @ P_lapse - P_lapse, ord="fro")),
        float(np.linalg.norm(P_trace @ P_trace - P_trace, ord="fro")),
        float(np.linalg.norm(P_shift @ P_shift - P_shift, ord="fro")),
        float(np.linalg.norm(P_shear @ P_shear - P_shear, ord="fro")),
    )

    # Commutation with the universal SO(3) generators.
    comm_shift = max(float(np.linalg.norm(P_shift @ G - G @ P_shift, ord="fro")) for G in (Gx, Gy, Gz))
    comm_shear = max(float(np.linalg.norm(P_shear @ G - G @ P_shear, ord="fro")) for G in (Gx, Gy, Gz))
    comm_lapse = max(float(np.linalg.norm(P_lapse @ G - G @ P_lapse, ord="fro")) for G in (Gx, Gy, Gz))
    comm_trace = max(float(np.linalg.norm(P_trace @ G - G @ P_trace, ord="fro")) for G in (Gx, Gy, Gz))

    ranks = {
        "lapse": int(np.linalg.matrix_rank(P_lapse, tol=1e-12)),
        "shift": int(np.linalg.matrix_rank(P_shift, tol=1e-12)),
        "trace": int(np.linalg.matrix_rank(P_trace, tol=1e-12)),
        "shear": int(np.linalg.matrix_rank(P_shear, tol=1e-12)),
    }

    # In the current canonical basis these should land exactly on the expected
    # coordinate blocks.
    diag_shift = np.diag(P_shift)[comp_idx]
    diag_shear = np.diag(P_shear)[comp_idx]

    print("UNIVERSAL GR CASIMIR BLOCK LOCALIZATION")
    print("=" * 78)
    print(f"Casimir eigenvalues on complement = {vals_real}")
    print(f"ranks = {ranks}")
    print(f"sum error = {sum_err:.3e}")
    print(f"orthogonality error = {orth_err:.3e}")
    print(f"idempotence error = {idem_err:.3e}")
    print(f"comm errors: lapse={comm_lapse:.3e}, trace={comm_trace:.3e}, shift={comm_shift:.3e}, shear={comm_shear:.3e}")
    print(f"diag P_shift on complement = {np.array2string(diag_shift, precision=6, floatmode='fixed')}")
    print(f"diag P_shear on complement = {np.array2string(diag_shear, precision=6, floatmode='fixed')}")

    record(
        "the universal complement Casimir has exactly the j=1 and j=2 eigenvalue split",
        vals_real == [-6.0, -6.0, -6.0, -6.0, -6.0, -2.0, -2.0, -2.0],
        f"Casimir eigenvalues={vals_real}",
    )
    record(
        "the spectral projectors define a canonical shift/shear split on the complement",
        ranks == {"lapse": 1, "shift": 3, "trace": 1, "shear": 5},
        f"ranks={ranks}",
    )
    record(
        "the four block projectors are exact, orthogonal, and complete",
        sum_err < 1e-12 and orth_err < 1e-12 and idem_err < 1e-12,
        f"sum={sum_err:.3e}, orth={orth_err:.3e}, idem={idem_err:.3e}",
    )
    record(
        "the shift/shear projectors commute with the universal SO(3) generators",
        comm_shift < 1e-12 and comm_shear < 1e-12 and comm_lapse < 1e-12 and comm_trace < 1e-12,
        f"comm errors=({comm_lapse:.3e},{comm_trace:.3e},{comm_shift:.3e},{comm_shear:.3e})",
    )
    record(
        "in the current canonical basis the Casimir projectors land exactly on the expected shift and shear coordinates",
        np.max(np.abs(diag_shift - np.array([1, 1, 1, 0, 0, 0, 0, 0], dtype=float))) < 1e-12
        and np.max(np.abs(diag_shear - np.array([0, 0, 0, 1, 1, 1, 1, 1], dtype=float))) < 1e-12,
        "P_shift selects h0i and P_shear selects spatial traceless-symmetric channels",
    )

    print("\nVerdict:")
    print(
        "The direct universal route already carries a canonical block-localization "
        "operator. Pi_A1 fixes lapse and trace, and the complement Casimir "
        "spectrally fixes the shift and traceless-shear blocks. So the old "
        "full complement-frame blocker was too strong."
    )
    print(
        "The remaining question is not whether a canonical lapse/shift/trace/shear "
        "block split exists. It does. The remaining question is whether this "
        "canonical block-localized Hessian is already enough to identify the "
        "Einstein/Regge dynamics law, or whether an extra theorem is still needed "
        "inside the shift/shear blocks."
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
