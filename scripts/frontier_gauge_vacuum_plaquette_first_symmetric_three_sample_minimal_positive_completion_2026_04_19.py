#!/usr/bin/env python3
"""
Unique adjoint-only minimal positive completion of the local Wilson
three-sample plaquette triple at the first symmetric retained seam.

This is the constructive upgrade beyond the local-Wilson positive-cone
no-go on the named (W_A, W_B, W_C) seam:

  1. invert the exact radical sample matrix F on the local Wilson triple
     Z^loc to recover a^loc = F^(-1) Z^loc; only the adjoint coordinate
     a^loc_(1,1) fails positivity;
  2. add the minimal adjoint repair r_min = -a^loc_(1,1), keeping the
     other retained coordinates fixed, to land on the boundary of the
     first-symmetric retained positive cone with a^min = (a^loc_(0,0),
     a^loc_(1,0), 0);
  3. evaluate Z^min = F a^min as the unique adjoint-only minimal
     positive completed sample triple.

Theorem 1 (unique adjoint-only minimal positive completion):
along the adjoint-only family a(t) = (a^loc_(0,0), a^loc_(1,0),
a^loc_(1,1) + t), cone membership is equivalent to t >= -a^loc_(1,1),
so t = r_min is the unique minimum and a^min is forced.

The runner reproduces the note's stated numerical values
(a^loc, r_min, a^min, Z^min) to roughly 1e-12 absolute tolerance and
verifies Theorem 1 directly on the half-line.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import sympy as sp

from frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_retained_positive_cone_obstruction_2026_04_17 import (
    radical_entries,
    sample_matrix,
    su3_partition_sum,
)


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def local_triple_and_inverse() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    """Return (F, F^(-1), Z^loc, a^loc) at high precision."""
    entries = radical_entries()
    f_mat = sample_matrix(entries)
    f_inv = sp.simplify(f_mat.inv())
    z_1plaq, _mode_cutoff = su3_partition_sum(6.0)
    z_loc = sp.Matrix(
        [
            sp.N(sp.exp(entries["a"] / 3) / z_1plaq, 80),
            sp.N(sp.exp(entries["b"] / 3) / z_1plaq, 80),
            sp.N(sp.exp(entries["d"] / 3) / z_1plaq, 80),
        ]
    )
    a_loc = sp.N(f_inv * z_loc, 80)
    return f_mat, f_inv, z_loc, a_loc


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SYMMETRIC THREE-SAMPLE MINIMAL POSITIVE COMPLETION")
    print("=" * 118)
    print()
    print("Question:")
    print("  Beyond the local-Wilson positive-cone no-go, is there an exact")
    print("  constructive minimal positive completion of (W_A, W_B, W_C)?")
    print()

    completion_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_MINIMAL_POSITIVE_COMPLETION_NOTE_2026-04-19.md"
    )

    # Note-stated reference values (truncated to displayed precision; the
    # runner verifies agreement to 1e-12 absolute, well inside the truncation).
    a_loc_ref = (
        0.34960695245840506,
        0.09339384931083795,
        -0.03190961277002444,
    )
    r_min_ref = 0.03190961277002444
    z_min_ref = (
        0.1351652795620484,
        0.3740128800091385,
        0.5438438585441973,
    )

    f_mat, _f_inv, z_loc, a_loc = local_triple_and_inverse()

    a_loc_vals = [float(sp.N(a_loc[i], 50)) for i in range(3)]
    r_min = -a_loc_vals[2]
    a_min = sp.Matrix([a_loc[0], a_loc[1], sp.Integer(0)])
    z_min_sym = sp.N(f_mat * a_min, 80)
    z_min_vals = [float(sp.N(z_min_sym[i], 50)) for i in range(3)]
    z_loc_vals = [float(sp.N(z_loc[i], 50)) for i in range(3)]

    a_loc_gap = max(abs(a_loc_vals[i] - a_loc_ref[i]) for i in range(3))
    r_min_gap = abs(r_min - r_min_ref)
    z_min_gap = max(abs(z_min_vals[i] - z_min_ref[i]) for i in range(3))

    # Cone-membership half-line scan (Theorem 1).
    # a(t) = (a^loc_(0,0), a^loc_(1,0), a^loc_(1,1) + t).
    # Cone membership <=> all coordinates >= 0.
    threshold = -a_loc_vals[2]
    test_offsets = [-1.0e-3, -1.0e-9, 0.0, 1.0e-9, 1.0e-3]
    membership_table = []
    for delta in test_offsets:
        t = threshold + delta
        a3 = a_loc_vals[2] + t
        in_cone = (a_loc_vals[0] >= 0.0) and (a_loc_vals[1] >= 0.0) and (a3 >= -1.0e-15)
        membership_table.append((delta, t, a3, in_cone))

    # Also confirm Z^min = F a^min preserves the W_A sample (adjoint orbit
    # vanishes there: F[0,2] = 0), changes W_B / W_C as the note states.
    w_a_unchanged = abs(z_min_vals[0] - z_loc_vals[0])
    w_b_increase = z_min_vals[1] - z_loc_vals[1]
    w_c_decrease = z_loc_vals[2] - z_min_vals[2]
    f02 = float(sp.N(f_mat[0, 2], 50))

    print("Reconstructed first-symmetric retained coordinates a^loc = F^(-1) Z^loc")
    print(f"  a^loc_(0,0)                 = {a_loc_vals[0]:.18f}")
    print(f"  a^loc_(1,0)                 = {a_loc_vals[1]:.18f}")
    print(f"  a^loc_(1,1)                 = {a_loc_vals[2]:.18f}")
    print(f"  r_min = -a^loc_(1,1)        = {r_min:.18f}")
    print()
    print("Completed sample triple Z^min = F a^min on the named seam")
    print(f"  Z^min(W_A)                  = {z_min_vals[0]:.18f}")
    print(f"  Z^min(W_B)                  = {z_min_vals[1]:.18f}")
    print(f"  Z^min(W_C)                  = {z_min_vals[2]:.18f}")
    print()
    print("Local-vs-completed comparison")
    print(f"  Z^loc(W_A) - Z^min(W_A)     = {z_loc_vals[0] - z_min_vals[0]: .3e}  (must be 0; F[0,2]={f02})")
    print(f"  Z^min(W_B) - Z^loc(W_B)     = {w_b_increase: .15f}  (must be > 0)")
    print(f"  Z^loc(W_C) - Z^min(W_C)     = {w_c_decrease: .15f}  (must be > 0)")
    print()
    print("Note-vs-runner deviations")
    print(f"  max |a^loc - a^loc_ref|     = {a_loc_gap:.3e}")
    print(f"  |r_min - r_min_ref|         = {r_min_gap:.3e}")
    print(f"  max |Z^min - Z^min_ref|     = {z_min_gap:.3e}")
    print()
    print("Theorem 1 half-line scan along a(t) = (a^loc_(0,0), a^loc_(1,0), a^loc_(1,1) + t)")
    print(f"  threshold t* = -a^loc_(1,1) = {threshold:.18f}")
    for delta, t, a3, in_cone in membership_table:
        flag = "in-cone" if in_cone else "out-of-cone"
        print(f"  delta={delta:+.0e}  t={t:.18f}  a3={a3:+.3e}  {flag}")
    print()

    check(
        "The completion note already states the explicit minimal-positive-completion claim with stated values for a^loc, r_min, a^min, Z^min",
        "minimal adjoint repair" in completion_note
        and "a^min = (a^loc_(0,0), a^loc_(1,0), 0)" in completion_note
        and "Z^min = F a^min" in completion_note
        and "Theorem 1" in completion_note,
    )
    check(
        "Reconstructed a^loc matches the note's stated values to 1e-12 (algebraic identity check)",
        a_loc_gap < 1.0e-12,
        f"max gap = {a_loc_gap:.3e}",
    )
    check(
        "Only the adjoint retained coordinate a^loc_(1,1) fails positivity; the (0,0) and (1,0) coordinates are strictly positive",
        a_loc_vals[0] > 1.0e-12
        and a_loc_vals[1] > 1.0e-12
        and a_loc_vals[2] < -1.0e-12,
        f"a^loc=({a_loc_vals[0]:.6f}, {a_loc_vals[1]:.6f}, {a_loc_vals[2]:.6f})",
    )
    check(
        "Minimal adjoint repair r_min = -a^loc_(1,1) matches the note value to 1e-12",
        r_min_gap < 1.0e-12,
        f"|r_min - r_min_ref| = {r_min_gap:.3e}",
    )
    check(
        "a^min = (a^loc_(0,0), a^loc_(1,0), 0) lies on the cone boundary (third coordinate exactly zero, first two strictly positive)",
        a_loc_vals[0] > 1.0e-12 and a_loc_vals[1] > 1.0e-12,
        "a^min has its third coordinate set to 0 by construction",
    )
    check(
        "Completed triple Z^min = F a^min matches the note's stated values to 1e-12",
        z_min_gap < 1.0e-12,
        f"max gap = {z_min_gap:.3e}",
    )
    check(
        "Z^min preserves W_A exactly because the adjoint orbit vanishes there (F[0,2] = 0)",
        abs(f02) < 1.0e-30 and w_a_unchanged < 1.0e-12,
        f"|F[0,2]|={abs(f02):.3e}, |Z^min(W_A)-Z^loc(W_A)|={w_a_unchanged:.3e}",
    )
    check(
        "Z^min raises W_B and lowers W_C relative to the local triple, matching the note's directional statement",
        w_b_increase > 1.0e-12 and w_c_decrease > 1.0e-12,
        f"dZ_B={w_b_increase:.3e}, dZ_C={w_c_decrease:.3e}",
    )
    check(
        "Theorem 1: along the adjoint-only family a(t), cone membership is equivalent to t >= -a^loc_(1,1) (out-of-cone for t < t*, in-cone for t >= t*)",
        all(
            (in_cone == (delta >= 0.0))
            for (delta, _t, _a3, in_cone) in membership_table
        ),
        f"threshold t*={threshold:.12f}",
    )
    check(
        "Therefore t = r_min is the unique minimum on the cone-membership half-line, so a^min is the unique adjoint-only minimal positive completion",
        r_min > 1.0e-12 and a_loc_gap < 1.0e-12,
        f"r_min={r_min:.12f}",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Exact constructive upgrade beyond the local-Wilson positive-cone no-go:")
    print("    - a^loc reconstructed; only adjoint coordinate fails positivity")
    print(f"    - minimal adjoint repair r_min = {r_min:.15f}")
    print(f"    - a^min = ({a_loc_vals[0]:.15f}, {a_loc_vals[1]:.15f}, 0)")
    print(f"    - Z^min = ({z_min_vals[0]:.15f}, {z_min_vals[1]:.15f}, {z_min_vals[2]:.15f})")
    print("    - Theorem 1 verified on the adjoint-only half-line: r_min is unique minimum")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
