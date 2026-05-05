#!/usr/bin/env python3
"""
Wilson open-lattice distance-law sweep versus screening mass.

Goal:
  test whether the steep open-lattice Wilson distance exponent is primarily a
  screening-mass artifact by sweeping mu^2 while keeping the rest of the open
  surface fixed.

Protocol:
  - open 3D Wilson lattice
  - SHARED vs SELF_ONLY only
  - same packet width, same G, same side set, same separations
  - fit |a_mut| ~ d^alpha on clean attractive rows
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import time
from dataclasses import dataclass

import numpy as np

import frontier_wilson_two_body_open as base


MU2_VALUES = (0.22, 0.05, 0.01, 0.005, 0.001)
SIDES = (11, 13, 15)
G_VAL = 5.0
DISTANCES = (3, 4, 5, 6)


@dataclass
class FitSummary:
    mu2: float
    alpha: float
    r2: float
    n_clean: int
    n_total: int


def power_law_fit(xs, ys):
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(lx, ly, 1)
    fit = slope * lx + intercept
    ss_res = float(np.sum((ly - fit) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2


def collect_rows(mu2: float):
    rows = []
    for side in SIDES:
        lat = base.OpenWilsonLattice(side)
        for d in DISTANCES:
            if d >= side - 2:
                continue
            row = base.run_config(side, G_VAL, mu2, d)
            signal, quality = base.label(row["a_mutual_early_mean"], row["snr"])
            amp = abs(row["a_mutual_early_mean"])
            rows.append(
                {
                    "side": side,
                    "d": d,
                    "amp": amp,
                    "snr": row["snr"],
                    "signal": signal,
                    "quality": quality,
                    "row": row,
                }
            )
            print(
                f"  side={side:2d} d={d}: "
                f"a_mut={row['a_mutual_early_mean']:+.6f} "
                f"SNR={row['snr']:.2f} [{signal}] [{quality}] "
                f"dsep SH={row['dsep_shared']:+.4f} SELF={row['dsep_self']:+.4f} FREE={row['dsep_free']:+.4f}"
            )
    return rows


def summarize_mu2(mu2: float, rows):
    clean = [(r["d"], r["amp"]) for r in rows if r["signal"] == "ATTRACT" and r["quality"] == "CLEAN"]
    if len(clean) < 2:
        return FitSummary(mu2=mu2, alpha=float("nan"), r2=float("nan"), n_clean=len(clean), n_total=len(rows))
    alpha, _, r2 = power_law_fit([d for d, _ in clean], [amp for _, amp in clean])
    return FitSummary(mu2=mu2, alpha=float(alpha), r2=float(r2), n_clean=len(clean), n_total=len(rows))


def main():
    print("=" * 92)
    print("WILSON OPEN-LATTICE DISTANCE-LAW SWEEP VS MU^2")
    print("=" * 92)
    print(f"Surface: sides={SIDES}, G={G_VAL}, separations={DISTANCES}")
    print(f"Packet width fixed at base SIGMA={base.SIGMA}")
    print(f"mu^2 sweep={MU2_VALUES}")
    print()

    summaries: list[FitSummary] = []
    for mu2 in MU2_VALUES:
        t0 = time.time()
        print(f"--- mu^2={mu2} ---")
        rows = collect_rows(mu2)
        summary = summarize_mu2(mu2, rows)
        summaries.append(summary)
        elapsed = time.time() - t0
        if np.isfinite(summary.alpha):
            print(
                f"  fit: |a_mut| ~ d^{summary.alpha:.3f}  "
                f"(R^2={summary.r2:.4f}, clean={summary.n_clean}/{summary.n_total}, "
                f"{elapsed:.1f}s)"
            )
        else:
            print(
                f"  fit: insufficient clean attractive rows "
                f"(clean={summary.n_clean}/{summary.n_total}, {elapsed:.1f}s)"
            )
        print()

    print("=" * 92)
    print("SUMMARY")
    print("=" * 92)
    for summary in summaries:
        if np.isfinite(summary.alpha):
            print(
                f"mu^2={summary.mu2:>7g}: alpha={summary.alpha:+.3f}  "
                f"R^2={summary.r2:.4f}  clean={summary.n_clean}/{summary.n_total}"
            )
        else:
            print(f"mu^2={summary.mu2:>7g}: insufficient clean rows ({summary.n_clean}/{summary.n_total})")


if __name__ == "__main__":
    main()
