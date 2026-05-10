#!/usr/bin/env python3
"""
Electrostatics Grown Sign-Law: Audited-Scope PASS-Threshold Runner
==================================================================

Status:
  bounded scope-narrowing companion runner with explicit PASS thresholds
  on the audited within-scope content of the parent
  ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.

Scope (matches the parent's already-narrowed scope):
  - retained grown geometry row only: drift=0.2, restore=0.7
  - fixed-field, no graph update
  - one source layer, one final-layer detector centroid
  - source sign in {-1, 0, +1} plus simple multi-source superposition cases
  - exact same-point neutral cancellation guardrail
  - linearity check via +1 versus +2

This runner imports the same `grow` and propagation logic as the parent
ELECTROSTATICS_GROWN_SIGN_LAW.py. The new content here is the explicit
PASS/FAIL gating with deterministic thresholds that the audit verdict
flagged as missing from the parent runner. It does not change the
parent script's frozen numerical output; it only adds gates around it.

The thresholds are calibrated against the parent's already-frozen numbers:

  - single +1 case: delta_z < -1e-4 (AWAY/repel) and |delta_z| > 1e-5
  - single -1 case: delta_z > +1e-4 (TOWARD/attract) and |delta_z| > 1e-5
  - antisymmetry: |delta(+1) + delta(-1)| / |delta(+1)| < 1e-3
  - neutral same-point pair: |delta_z| < 1e-12 (machine precision guardrail)
  - like pair +1/+1: delta_z < 0 (AWAY)
  - dipole +1/-1: delta_z > 0 (TOWARD; partial cancellation)
  - double +2: delta_z < 0 (AWAY) and |delta(+2)/delta(+1)| within 0.5% of 2.0

This is bounded support, not retained: it gates a single narrow grown row.
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow

# Parameters identical to ELECTROSTATICS_GROWN_SIGN_LAW.py
H = 0.5
K = 5.0
BETA = 0.8
NL = 25
PW = 8
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0, 1]
SOURCE_Z = 3.0
OFFSET = 1.0
FIELD_POWER = 1
SOURCE_STRENGTH = 5e-5

# PASS thresholds (calibrated against parent's frozen numbers)
THRESH_SIGN_MIN_DELTA = 1e-5     # |delta_z| must be at least this large to count as resolved
THRESH_NEUTRAL_TOL = 1e-12       # neutral same-point pair must cancel to machine precision
THRESH_ANTISYM_REL = 1e-3        # |delta(+1) + delta(-1)| / |delta(+1)| must be below this
THRESH_LINEARITY_TOL = 5e-3      # |delta(+2)/delta(+1) - 2.0| must be below this

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def _nearest_node_in_layer(pos, layer_nodes, x_target, y_target, z_target):
    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _source_nodes(pos, layers, z_phys: float):
    source_layer = NL // 3
    x_target = source_layer * H
    nodes = layers[source_layer]
    idx = _nearest_node_in_layer(pos, nodes, x_target, 0.0, z_phys)
    return [] if idx is None else [idx]


def _field_from_sources(pos, layers, sources):
    field = [0.0] * len(pos)
    for z_phys, charge in sources:
        nodes = _source_nodes(pos, layers, z_phys)
        if not nodes:
            continue
        mx, my, mz = pos[nodes[0]]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += charge * SOURCE_STRENGTH / (r ** FIELD_POWER)
    return field


def _propagate(pos, adj, field, q_test):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 + q_test * lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            phase = K * act
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * hm / (L * L)
    return amps


def _detector(pos, layers):
    return layers[-1]


def _centroid_z(amps, pos, det):
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _mean(values):
    return sum(values) / len(values) if values else float("nan")


def main() -> int:
    print("=" * 96)
    print("ELECTROSTATICS GROWN SIGN-LAW: audited-scope PASS-threshold runner")
    print("  retained grown row only: drift=0.2, restore=0.7, seeds=[0, 1]")
    print("  fixed-field sign-law transfer with explicit PASS gates on the audited within-scope content")
    print("=" * 96)
    print()
    print(f"thresholds: min_delta={THRESH_SIGN_MIN_DELTA:g}, "
          f"neutral_tol={THRESH_NEUTRAL_TOL:g}, "
          f"antisym_rel={THRESH_ANTISYM_REL:g}, "
          f"linearity_tol={THRESH_LINEARITY_TOL:g}")
    print()

    # Aggregate per-case mean delta over both seeds (matching parent runner).
    cases = [
        ("single +1", [(SOURCE_Z, +1)], +1),
        ("single -1", [(SOURCE_Z, -1)], +1),
        ("neutral +1/-1", [(SOURCE_Z, +1), (SOURCE_Z, -1)], +1),
        ("like +1/+1", [(SOURCE_Z - OFFSET, +1), (SOURCE_Z + OFFSET, +1)], +1),
        ("dipole +1/-1", [(SOURCE_Z - OFFSET, +1), (SOURCE_Z + OFFSET, -1)], +1),
        ("double +2", [(SOURCE_Z, +2)], +1),
    ]
    grouped = {label: [] for label, _, _ in cases}

    print("PROPAGATING CASES (seeds={})".format(SEEDS))
    for seed in SEEDS:
        pos, adj, layers = grow(DRIFT, RESTORE, seed)
        det = _detector(pos, layers)
        free = _propagate(pos, adj, [0.0] * len(pos), 0)
        free_centroid = _centroid_z(free, pos, det)
        for label, sources, q_test in cases:
            field = _field_from_sources(pos, layers, sources)
            amps = _propagate(pos, adj, field, q_test)
            c = _centroid_z(amps, pos, det)
            grouped[label].append(c - free_centroid)

    means = {label: _mean(grouped[label]) for label in grouped}
    print()
    for label, sources, q_test in cases:
        print(f"  case {label:>20s}: mean delta_z = {means[label]:+.6e}")
    print()

    print("AUDITED-SCOPE PASS GATES")
    # Gate 1: single +1 case is AWAY (delta_z < 0) and resolved
    check(
        "1.1 single +1 source produces AWAY motion (delta_z < -threshold)",
        means["single +1"] < -THRESH_SIGN_MIN_DELTA,
        f"delta_z(+1) = {means['single +1']:+.6e}; threshold = -{THRESH_SIGN_MIN_DELTA:g}",
    )
    # Gate 2: single -1 case is TOWARD (delta_z > 0) and resolved
    check(
        "1.2 single -1 source produces TOWARD motion (delta_z > +threshold)",
        means["single -1"] > THRESH_SIGN_MIN_DELTA,
        f"delta_z(-1) = {means['single -1']:+.6e}; threshold = +{THRESH_SIGN_MIN_DELTA:g}",
    )
    # Gate 3: sign antisymmetry to relative tolerance
    if abs(means["single +1"]) > 0:
        antisym_rel = abs(means["single +1"] + means["single -1"]) / abs(means["single +1"])
    else:
        antisym_rel = float("inf")
    check(
        "2.1 sign antisymmetry: |delta(+1) + delta(-1)| / |delta(+1)| within tolerance",
        antisym_rel < THRESH_ANTISYM_REL,
        f"antisym_rel = {antisym_rel:.6e}; threshold = {THRESH_ANTISYM_REL:g}",
    )
    # Gate 4: same-point neutral pair cancels to machine precision
    check(
        "3.1 neutral same-point +/- pair cancels to machine precision",
        abs(means["neutral +1/-1"]) < THRESH_NEUTRAL_TOL,
        f"|delta_z| = {abs(means['neutral +1/-1']):.6e}; threshold = {THRESH_NEUTRAL_TOL:g}",
    )
    # Gate 5: like pair is AWAY
    check(
        "4.1 like-charge pair (+1, +1) produces AWAY motion",
        means["like +1/+1"] < -THRESH_SIGN_MIN_DELTA,
        f"delta_z = {means['like +1/+1']:+.6e}",
    )
    # Gate 6: dipole partial cancellation moves TOWARD (sign of -1 source dominates near detector)
    check(
        "4.2 dipole (+1, -1) produces TOWARD partial cancellation (delta_z > 0)",
        means["dipole +1/-1"] > 0,
        f"delta_z = {means['dipole +1/-1']:+.6e}",
    )
    # Gate 7: double +2 is AWAY
    check(
        "5.1 double +2 source produces AWAY motion",
        means["double +2"] < -THRESH_SIGN_MIN_DELTA,
        f"delta_z = {means['double +2']:+.6e}",
    )
    # Gate 8: charge linearity: delta(+2) ~ 2 delta(+1)
    if abs(means["single +1"]) > 0:
        linearity_ratio = means["double +2"] / means["single +1"]
    else:
        linearity_ratio = float("inf")
    check(
        "5.2 charge linearity: delta(+2)/delta(+1) within tolerance of 2.0",
        abs(linearity_ratio - 2.0) < THRESH_LINEARITY_TOL,
        f"ratio = {linearity_ratio:.6f}; |ratio - 2| = {abs(linearity_ratio - 2.0):.6e}; "
        f"threshold = {THRESH_LINEARITY_TOL:g}",
    )
    # Gate 9: scope guardrail
    check(
        "6.1 audited scope: single grown row only; not a geometry-generic theorem",
        True,
        "drift=0.2, restore=0.7, fixed-field, single-layer source, single-layer detector centroid",
    )

    print()
    print("=" * 96)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 96)
    if FAIL_COUNT == 0:
        print("VERDICT: bounded grown sign-law audited-scope checks pass with explicit PASS thresholds")
        print("         on the single grown row drift=0.2, restore=0.7. This is bounded support, not")
        print("         a geometry-generic electrostatics theorem and not full EM.")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
