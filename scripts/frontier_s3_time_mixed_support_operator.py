#!/usr/bin/env python3
"""Route 2 mixed support operator blocker on A1 x {E_x, T1x}.

This runner asks the exact microscopic question:

    does the current exact support algebra contain a nonzero mixed operator
    on A1 x {E_x, T1x} before exterior projection?

The candidate is the mixed block of the exact support Green matrix in the
adapted basis:

    M_mix = P_A1^T G_S P_bright

If that block vanishes and the support-to-active map is rank one / charge
only, then the current support stack cannot produce the desired exact tensor
observable.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"

same = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
support_amp = SourceFileLoader(
    "support_renorm_active_amp",
    f"{ROOT}/scripts/frontier_support_renormalized_active_amplitude.py",
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def support_green_matrix() -> np.ndarray:
    h0, interior = same.build_neg_laplacian_sparse(15)
    center = interior // 2
    support = [
        same.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same.SUPPORT_COORDS
    ]
    g0p = same.solve_columns(h0, support)
    return g0p[support, :]


def support_delta(gs: np.ndarray, q: np.ndarray) -> float:
    vals = gs @ q
    q_total = float(np.sum(q))
    return float(vals[0] / q_total - np.mean(vals[1:]) / q_total)


def main() -> int:
    print("Route 2 mixed support operator blocker")
    print("=" * 78)

    gs = support_green_matrix()
    basis = same.build_adapted_basis()

    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0

    a1 = basis[:, :2]
    bright = np.column_stack([e_x, t1x])

    mixed = a1.T @ gs @ bright
    mixed_norm = float(np.max(np.abs(mixed)))

    print("Mixed A1-bright support block candidate:")
    print(np.array2string(mixed, precision=12, floatmode="fixed"))
    print(f"max |mixed block| = {mixed_norm:.3e}")

    active_op, pair_op = support_amp.support_to_active_operator()
    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))
    bright_image_norm = float(
        max(
            np.max(np.abs(active_op @ e_x)),
            np.max(np.abs(active_op @ t1x)),
        )
    )

    print("\nExact support-to-active operator:")
    print(np.array2string(active_op, precision=6, floatmode="fixed"))
    print(f"active rank = {active_rank}")
    print(f"pair rank = {pair_rank}")
    print(f"max bright-channel image norm = {bright_image_norm:.3e}")

    eps = 1e-6
    q_family = [
        ("e0", e0),
        ("s/sqrt(6)", s / np.sqrt(6.0)),
        ("r=1", (e0 + s) / (1.0 + np.sqrt(6.0))),
        ("r=1.5", (e0 + 1.5 * s) / (1.0 + 1.5 * np.sqrt(6.0))),
    ]
    bright_dir_max = 0.0
    for label, q in q_family:
        for chan_name, v in [("E_x", e_x), ("T1x", t1x)]:
            d = (
                support_delta(gs, q + eps * v) - support_delta(gs, q - eps * v)
            ) / (2.0 * eps)
            bright_dir_max = max(bright_dir_max, abs(float(d)))
            print(f"{label:>8} along {chan_name}: d delta_A1 = {float(d):+.3e}")

    record(
        "the exact mixed support operator candidate P_A1^T G_S P_bright vanishes",
        mixed_norm < 1e-12,
        f"max |P_A1^T G_S P_bright| = {mixed_norm:.3e}",
    )
    record(
        "the exact support-to-active operator is rank one",
        active_rank == 1 and pair_rank == 1,
        f"active rank={active_rank}, pair rank={pair_rank}",
    )
    record(
        "the exact support-to-active operator annihilates the bright E_x and T1x channels",
        bright_image_norm < 1e-12,
        f"max bright-channel image norm = {bright_image_norm:.3e}",
    )
    record(
        "the exact support scalar delta_A1 is blind to bright-channel perturbations on the tested projective A1 family",
        bright_dir_max < 1e-10,
        f"max bright directional derivative = {bright_dir_max:.3e}",
    )

    print("\nVerdict:")
    print(
        "The current exact support algebra is scalar/rank-one on the A1 block. "
        "Its mixed A1-bright support operator candidate is zero to machine "
        "precision, the support-to-active response is charge-only, and the "
        "exact support scalar delta_A1 is blind to E_x and T1x. So the current "
        "support stack cannot supply a nonzero exact mixed operator on "
        "A1 x {E_x, T1x}; the missing tensor observable needs a new microscopic "
        "operator beyond this support algebra."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
        return 0
    print("Some checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
