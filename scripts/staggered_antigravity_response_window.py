#!/usr/bin/env python3
"""Staggered signed-response window for the gravity discovery lane.

The file name keeps the lane shorthand, but the script does not claim
antigravity. It asks a smaller question: on the parity-correct staggered
scalar coupling H_diag = (m + V) * epsilon(x), does the branch product
source_sign * response_sign control the packet-envelope response while norm
and the zero-field reduction remain clean?
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gravity_signed_sector_harness import (  # noqa: E402
    MODES,
    PAIRS,
    _build_branch_hamiltonian,
    _cn_evolve,
    _label_pair,
    _passfail,
    sign_roles,
)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime  # noqa: E402

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np


N = 81
MASS = 0.30
SOURCE_SITE = 57.0
PACKET_CENTER = 35.0
SIGMA = 5.0
STEPS = 46
DT = 0.075


def packet() -> np.ndarray:
    xs = np.arange(N, dtype=float)
    psi = np.exp(-0.5 * ((xs - PACKET_CENTER) / SIGMA) ** 2).astype(np.complex128)
    return psi / np.linalg.norm(psi)


def centroid(psi: np.ndarray) -> float:
    rho = np.abs(psi) ** 2
    total = float(np.sum(rho))
    if total <= 1e-30:
        return 0.0
    return float(np.dot(rho, np.arange(len(psi), dtype=float)) / total)


def field_for_source(source_sign: int, strength: float) -> np.ndarray:
    xs = np.arange(N, dtype=float)
    # The positive branch source creates a local well in the parity scalar
    # channel. A locked negative branch responds with the opposite sign, so
    # same-sector pairs still see the same effective well.
    raw_well = -strength / np.sqrt((xs - SOURCE_SITE) ** 2 + 1.0)
    return source_sign * raw_well


def run_response(source_sign: int, response_sign: int, strength: float) -> tuple[float, float, float]:
    psi0 = packet()
    zero_h = _build_branch_hamiltonian(N, np.zeros(N), response_sign=+1, mass=MASS)
    free = _cn_evolve(zero_h, psi0, steps=STEPS, dt=DT)
    free_centroid = centroid(free)

    field = field_for_source(source_sign, strength)
    hamiltonian = _build_branch_hamiltonian(N, field, response_sign=response_sign, mass=MASS)
    evolved = _cn_evolve(hamiltonian, psi0, steps=STEPS, dt=DT)
    disp = centroid(evolved) - free_centroid
    norm_drift = abs(float(np.vdot(evolved, evolved).real) - 1.0)
    gap_at_source = MASS + response_sign * field[int(SOURCE_SITE)]
    return disp, norm_drift, gap_at_source


def main() -> None:
    strengths = (0.0, 0.015, 0.030, 0.060, 0.090, 0.120)
    fixed_strength = 0.060

    print("=" * 94)
    print("STAGGERED SIGNED-RESPONSE WINDOW")
    print("  bounded response probe; antigravity is shorthand only")
    print("=" * 94)
    print(f"N={N}, mass={MASS:.2f}, source_site={SOURCE_SITE:.1f}, packet_center={PACKET_CENTER:.1f}")
    print("positive displacement means packet envelope moves toward the source")
    print()

    print("LOCKED BRANCH WINDOW")
    print(f"  {'strength':>9s}  {'++ disp':>11s} {'+- disp':>11s} {'-+ disp':>11s} {'-- disp':>11s}  max norm drift")
    print("  " + "-" * 76)
    for strength in strengths:
        disps = []
        drifts = []
        for chi_a, chi_b in PAIRS:
            src, resp = sign_roles("locked", chi_a)
            # A test packet of branch chi_a responds to a source of branch chi_b.
            src = chi_b
            resp = chi_a
            disp, drift, _ = run_response(src, resp, strength)
            disps.append(disp)
            drifts.append(drift)
        print(
            f"  {strength:9.3f}  "
            f"{disps[0]:+11.4e} {disps[1]:+11.4e} {disps[2]:+11.4e} {disps[3]:+11.4e}  "
            f"{max(drifts):.2e}"
        )
    print()

    print(f"MODE COMPARISON AT strength={fixed_strength:.3f}")
    print(
        f"  {'mode':<14s} {'pair':>4s} {'src':>4s} {'resp':>5s} "
        f"{'src*resp':>8s} {'disp':>12s} {'gap(src)':>10s} {'norm':>9s} read"
    )
    print("  " + "-" * 88)
    for mode in MODES:
        for chi_test, chi_source in PAIRS:
            source_sign, _ = sign_roles(mode, chi_source)
            _, response_sign = sign_roles(mode, chi_test)
            disp, drift, gap = run_response(source_sign, response_sign, fixed_strength)
            if abs(disp) < 1e-10:
                read = "ZERO"
            else:
                read = "TOWARD" if disp > 0.0 else "AWAY"
            print(
                f"  {mode:<14s} {_label_pair(chi_test, chi_source):>4s} "
                f"{source_sign:+4d} {response_sign:+5d} {source_sign * response_sign:+8d} "
                f"{disp:+12.4e} {gap:+10.4f} {drift:9.1e} {read}"
            )
    print()

    zero_disp, zero_drift, _ = run_response(+1, +1, 0.0)
    same_ok = run_response(+1, +1, fixed_strength)[0] > 0.0 and run_response(-1, -1, fixed_strength)[0] > 0.0
    opposite_ok = run_response(+1, -1, fixed_strength)[0] < 0.0 and run_response(-1, +1, fixed_strength)[0] < 0.0
    print("CONTROLS")
    print(f"  zero-strength displacement: {zero_disp:+.3e}")
    print(f"  zero-strength norm drift: {zero_drift:.3e}")
    print(f"  locked same-sector TOWARD: {_passfail(same_ok)}")
    print(f"  locked opposite-sector AWAY: {_passfail(opposite_ok)}")
    print()
    print("SAFE READ")
    print("  The staggered parity response can host a branch-product sign window.")
    print("  This is a response-hosting check, not a derivation of a conserved chi_g sector.")


if __name__ == "__main__":
    main()
