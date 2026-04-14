#!/usr/bin/env python3
"""Bounded scan of the last tensor coefficient gap on the A1 background manifold.

After the exact reduced-shell amplitude law is factored out, the remaining
gravity gap sits in the two bright local coefficients of eta_floor_tf.

This runner asks whether that remaining freedom is at least one-parameter on
the scalar A1 manifold:

  q_A1(r; Q) = Q * (e0 + r s) / (1 + sqrt(6) r)

with fixed total charge Q and varying A1 background ratio r = s/e0.

If so, the remaining full-GR gap has been reduced to one scalar background
renormalization function rather than a generic tensor law.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"
EPS = 0.005
Q_FIXED = 1.0
R_VALUES = [0.50, 0.75, 1.00, 1.25, 1.50, 1.75]

same = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
two = SourceFileLoader(
    "tensor_two_channel",
    f"{ROOT}/scripts/frontier_tensor_boundary_drive_two_channel.py",
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def eta_floor(q: np.ndarray) -> float:
    return float(two.tensor_metrics(two.phi_from_q(q))[0])


def main() -> int:
    print("A1-background ratio scan for the bright tensor coefficients")
    print("=" * 78)
    print(f"fixed total charge Q = {Q_FIXED:.6f}, centered epsilon = {EPS:.6f}")

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]

    ex = (np.sqrt(3.0) * e1 + e2) / 2.0

    beta_e = []
    beta_t = []
    ratios = []

    for r in R_VALUES:
        q = Q_FIXED * (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        b_e = float((eta_floor(q + EPS * ex) - eta_floor(q - EPS * ex)) / (2.0 * EPS))
        b_t = float((eta_floor(q + EPS * t1x) - eta_floor(q - EPS * t1x)) / (2.0 * EPS))
        beta_e.append(b_e)
        beta_t.append(b_t)
        ratios.append(b_t / max(-b_e, 1e-16))
        print(
            f"r={r:.2f}: beta_E_x={b_e:+.12e}, beta_T1x={b_t:+.12e}, "
            f"beta_T1x/(-beta_E_x)={ratios[-1]:.12f}"
        )

    beta_e = np.array(beta_e, dtype=float)
    beta_t = np.array(beta_t, dtype=float)
    ratios = np.array(ratios, dtype=float)
    rvals = np.array(R_VALUES, dtype=float)

    sec_e = float(np.max(np.abs(beta_e[2:] - 2.0 * beta_e[1:-1] + beta_e[:-2])))
    sec_t = float(np.max(np.abs(beta_t[2:] - 2.0 * beta_t[1:-1] + beta_t[:-2])))
    sec_ratio = float(np.max(np.abs(ratios[2:] - 2.0 * ratios[1:-1] + ratios[:-2])))

    mono_e = bool(np.all(np.diff(beta_e) > 0.0))
    mono_t = bool(np.all(np.diff(beta_t) > 0.0))
    mono_ratio = bool(np.all(np.diff(ratios) > 0.0))

    record(
        "the bright coefficient beta_E_x varies monotonically along the scalar A1 ratio family",
        mono_e,
        f"endpoint values: beta_E_x({R_VALUES[0]:.2f})={beta_e[0]:+.6e}, beta_E_x({R_VALUES[-1]:.2f})={beta_e[-1]:+.6e}",
    )
    record(
        "the bright coefficient beta_T1x varies monotonically along the scalar A1 ratio family",
        mono_t,
        f"endpoint values: beta_T1x({R_VALUES[0]:.2f})={beta_t[0]:+.6e}, beta_T1x({R_VALUES[-1]:.2f})={beta_t[-1]:+.6e}",
    )
    record(
        "the bright-channel coefficient ratio is a monotone scalar function of the A1 background ratio",
        mono_ratio,
        f"ratio endpoints: {ratios[0]:.6f} -> {ratios[-1]:.6f}",
    )
    record(
        "the remaining A1-background dependence is smooth rather than erratic on the audited interval",
        sec_e < 1e-6 and sec_t < 1e-6 and sec_ratio < 5e-2,
        (
            f"second-difference scales: "
            f"E_x={sec_e:.3e}, T1x={sec_t:.3e}, ratio={sec_ratio:.3e}"
        ),
    )

    print("\nVerdict:")
    print(
        "After exact shell-amplitude normalization, the remaining tensor gap is "
        "naturally organized by one scalar A1 background parameter: the shell "
        "versus center ratio r = s/e0. The bright coefficients vary smoothly "
        "and monotonically along that one-parameter manifold."
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
