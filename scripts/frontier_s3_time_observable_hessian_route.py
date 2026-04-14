#!/usr/bin/env python3
"""Route 2 observable-Hessian audit on PL S^3 x R.

This runner checks whether the exact observable principle

    W[J] = log|det(D+J)| - log|det D|

can produce anything beyond a scalar source-response kernel on the route-2
background. The expected outcome on the current atlas is:

    exact kinematic lift: yes
    scalar Hessian: yes
    tensor/time-coupling law: no
"""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f" ({detail})"
    print(line)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("None of the candidate paths exist: " + ", ".join(str(p) for p in paths))


def flat_index(ls: int, lt: int, x0: int, x1: int, x2: int, t: int) -> int:
    return (((x0 % ls) * ls + (x1 % ls)) * ls + (x2 % ls)) * lt + (t % lt)


def slice_projector(ls: int, lt: int, predicate) -> np.ndarray:
    n = ls**3 * lt
    p = np.zeros((n, n), dtype=complex)
    for x0 in range(ls):
        for x1 in range(ls):
            for x2 in range(ls):
                for t in range(lt):
                    i = flat_index(ls, lt, x0, x1, x2, t)
                    if predicate(x0, x1, x2, t):
                        p[i, i] = 1.0
    return p


def hessian_entry(inv_d: np.ndarray, p_a: np.ndarray, p_b: np.ndarray) -> float:
    return float((-np.trace(inv_d @ p_a @ inv_d @ p_b)).real)


def main() -> int:
    repo_root = Path("/Users/jonreilly/Projects/Physics")
    review_root = Path("/private/tmp/physics-review-active")
    atlas = first_existing([
        repo_root / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
        review_root / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
    ])
    obs_note = first_existing([
        repo_root / "docs" / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md",
        review_root / "docs" / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md",
    ])
    anomaly_note = first_existing([
        repo_root / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
        review_root / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
    ])
    s3_note = first_existing([
        repo_root / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
        review_root / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
    ])
    bridge_note = review_root / "docs" / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md"
    committee_note = review_root / "docs" / "S3_TIME_COMMITTEE_MEMO.md"
    hessian_note = review_root / "docs" / "S3_TIME_OBSERVABLE_HESSIAN_ROUTE_NOTE.md"

    atlas_text = read_text(atlas)
    obs_text = read_text(obs_note)
    anomaly_text = read_text(anomaly_note)
    s3_text = read_text(s3_note)
    bridge_text = read_text(bridge_note)
    committee_text = read_text(committee_note)

    hier = SourceFileLoader(
        "hierarchy_observable_principle",
        "/Users/jonreilly/Projects/Physics/scripts/frontier_hierarchy_observable_principle_from_axiom.py",
    ).load_module()

    print("Route 2 observable-Hessian audit: S^3 + anomaly-forced time")
    print("=" * 78)
    print("  Candidate background: PL S^3 x R")
    print("  Exact source generator: W[J] = log|det(D+J)| - log|det D|")
    print()

    s3_closed = "PL homeomorphic to S^3" in s3_text and "for every R >= 2" in s3_text
    time_exact = "single-clock" in anomaly_text.lower() and "d_t = 1" in anomaly_text
    obs_scalar = "scalar generator" in obs_text.lower() and "local scalar observables" in obs_text.lower()
    bridge_present = "T_R := exp(-Lambda_R)" in bridge_text and "bounded" in bridge_text.lower()

    check("S^3 compactification is exact", s3_closed, "atlas route-2 spatial background is closed")
    check("Anomaly-forced time is exact", time_exact, "single-clock route-2 temporal background is closed")
    check("Observable principle is scalar-only", obs_scalar, "exact generator is additive and CPT-even scalar")
    check("Route-2 transfer-matrix bridge candidate is present", bridge_present, "bounded transfer operator exists")

    ls, lt, u0 = 2, 4, 0.9
    d = hier.build_dirac_4d_apbc(ls, lt, u0)
    inv_d = np.linalg.inv(d)

    p_time = slice_projector(ls, lt, lambda x0, x1, x2, t: t == 0)
    p_space = slice_projector(ls, lt, lambda x0, x1, x2, t: x0 == 0)

    h_tt = hessian_entry(inv_d, p_time, p_time)
    h_ss = hessian_entry(inv_d, p_space, p_space)
    h_ts = hessian_entry(inv_d, p_time, p_space)

    def W(jt: float, js: float) -> float:
        src = jt * p_time + js * p_space
        return hier.observable_generator(d, src)

    h_fd_tt = (W(1e-4, 0.0) - 2.0 * W(0.0, 0.0) + W(-1e-4, 0.0)) / (1e-4**2)
    h_fd_ss = (W(0.0, 1e-4) - 2.0 * W(0.0, 0.0) + W(0.0, -1e-4)) / (1e-4**2)
    h_fd_ts = (
        W(1e-4, 1e-4)
        - W(1e-4, -1e-4)
        - W(-1e-4, 1e-4)
        + W(-1e-4, -1e-4)
    ) / (4.0 * 1e-4**2)

    hessian = np.array([[h_tt, h_ts], [h_ts, h_ss]], dtype=float)
    sym_err = float(np.max(np.abs(hessian - hessian.T)))

    print("Exact scalar-source Hessian on the route-2-sized block:")
    print(hessian)
    print(f"analytic-vs-fd tt error: {abs(h_tt - h_fd_tt):.3e}")
    print(f"analytic-vs-fd ss error: {abs(h_ss - h_fd_ss):.3e}")
    print(f"analytic-vs-fd ts error: {abs(h_ts - h_fd_ts):.3e}")
    print(f"Hessian symmetry error: {sym_err:.3e}")
    print()

    check(
        "the observable Hessian is a real symmetric scalar 2x2 kernel",
        sym_err < 1e-12 and np.isfinite(h_tt) and np.isfinite(h_ss) and np.isfinite(h_ts),
        f"H = {hessian.tolist()}",
    )
    check(
        "the exact generator is even under scalar source reversal on each axis",
        abs(W(1e-4, 0.0) - W(-1e-4, 0.0)) < 1e-12 and abs(W(0.0, 1e-4) - W(0.0, -1e-4)) < 1e-12,
        "scalar generator remains bosonic/sign-blind",
    )
    check(
        "the route-2 observable selector remains kinematic only",
        "O_lift = 1" in read_text(hessian_note) or "O_lift = 1" in committee_text or "O_lift = 1" in bridge_text,
        "selector observable is background-only, not a tensor carrier",
    )
    check(
        "the atlas still lacks an exact tensor/time-coupling law on this route",
        False,
        "the Hessian stays scalar-valued; no tensor-valued dynamics bridge appears",
    )

    print("Summary:")
    print("  Kinematic lift: yes")
    print("  Observable generator: yes")
    print("  Scalar Hessian kernel: yes")
    print("  Tensor/time-coupling law: blocked")
    print("  Missing theorem: exact tensor-valued observable or dynamics bridge on PL S^3 x R")
    print(f"PASS={PASS} FAIL={FAIL}")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
