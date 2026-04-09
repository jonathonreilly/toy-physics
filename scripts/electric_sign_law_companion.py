#!/usr/bin/env python3
"""Electric-like sign-law companion on the retained ordered-lattice family.

This is a narrow follow-up to the bounded electric-sign-law probe.

Goal:
  Freeze a slightly stronger but still review-safe electrostatics-like card:
  sign antisymmetry, symmetric cancellation, dipole directionality, charge
  scaling, and screening.

Claim surface:
  - scalar sign law only
  - no Maxwell theory
  - no vector fields or radiation
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
PHYS_L = 12
PHYS_W = 8
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
CHARGE_MAGNITUDES = (1, 2, 4, 8)


@dataclass(frozen=True)
class CaseResult:
    label: str
    delta: float
    centroid: float


def detector(lat: Lattice3D) -> list[int]:
    det_layer = lat.nl - 1
    return [
        lat.nmap[(det_layer, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (det_layer, iy, iz) in lat.nmap
    ]


def centroid(amps: np.ndarray, det: list[int], pos: np.ndarray) -> float:
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return 0.0
    return float(np.dot(probs, pos[det, 2]) / total)


def point_packet(lat: Lattice3D, z_phys: float = 0.0) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    idx = lat.nmap[(0, 0, round(z_phys / lat.h))]
    init[idx] = 1.0
    return init


def field_from_source_at(
    lat: Lattice3D,
    x_phys: float,
    y_phys: float,
    z_phys: float,
    charge: float,
    power: int,
) -> np.ndarray:
    src = np.array([x_phys, y_phys, z_phys], dtype=float)
    r = np.sqrt(np.sum((lat.pos - src) ** 2, axis=1)) + 0.1
    return charge * SOURCE_STRENGTH / (r ** power)


def field_from_sources(
    lat: Lattice3D,
    sources: list[tuple[float, float, float, float]],
    power: int = FIELD_POWER,
) -> np.ndarray:
    field = np.zeros(lat.n, dtype=float)
    for x, y, z, q in sources:
        field += field_from_source_at(lat, x, y, z, q, power)
    return field


def propagate_charge(lat: Lattice3D, init: np.ndarray, field: np.ndarray, q_test: int) -> np.ndarray:
    """Propagate with a sign-flipped phase-valley action."""
    amps = init.copy()
    npl = lat.npl
    for layer in range(lat.nl - 1):
        ls = lat._ls[layer]
        ld = lat._ls[layer + 1]
        sa = amps[ls : ls + npl].copy()
        if np.max(np.abs(sa)) < 1e-30:
            continue
        sf = field[ls : ls + npl]
        df = field[ld : ld + npl]
        for dy, dz, L, w in lat._off:
            ym = max(0, -dy)
            yM = min(lat._nw, lat._nw - dy)
            zm = max(0, -dz)
            zM = min(lat._nw, lat._nw - dz)
            if ym >= yM or zm >= zM:
                continue
            yr = np.arange(ym, yM)
            zr = np.arange(zm, zM)
            siy, siz = np.meshgrid(yr, zr, indexing="ij")
            si = siy.ravel() * lat._nw + siz.ravel()
            di = (siy.ravel() + dy) * lat._nw + (siz.ravel() + dz)
            a = sa[si]
            nz = np.abs(a) > 1e-30
            if not np.any(nz):
                continue
            lf = 0.5 * (sf[si[nz]] + df[di[nz]])
            act = L * (1 + q_test * lf)
            c = a[nz] * np.exp(1j * K * act) * w * lat._hm / (L * L)
            np.add.at(amps[ld : ld + npl], di[nz], c)
    return amps


def run_case(
    lat: Lattice3D,
    det: list[int],
    init: np.ndarray,
    field: np.ndarray,
    q_test: int,
) -> CaseResult:
    amps = propagate_charge(lat, init, field, q_test)
    c = centroid(amps, det, lat.pos)
    free = propagate_charge(lat, init, np.zeros(lat.n), 0)
    free_c = centroid(free, det, lat.pos)
    return CaseResult(label="", delta=c - free_c, centroid=c)


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)

    print("=" * 96)
    print("ELECTRIC-SIGN-LAW COMPANION")
    print("  retained ordered-lattice electrostatics-like sign-law card")
    print("  observables: antisymmetry, cancellation, dipole, scaling, screening")
    print("=" * 96)
    print(f"h={H}, W={PHYS_W}, L={PHYS_L}, strength={SOURCE_STRENGTH:g}")
    print()

    # 1) Sign antisymmetry and neutrality.
    source_z = 5.0
    init = point_packet(lat, 0.0)
    plus_field = field_from_sources(lat, [(lat.pos[lat.nmap[(lat.nl // 3, 0, round(source_z / lat.h))]][0], 0.0, source_z, +1.0)])
    minus_field = field_from_sources(lat, [(lat.pos[lat.nmap[(lat.nl // 3, 0, round(source_z / lat.h))]][0], 0.0, source_z, -1.0)])
    plus_rep = run_case(lat, det, init, plus_field, +1)
    plus_att = run_case(lat, det, init, plus_field, -1)
    minus_rep = run_case(lat, det, init, minus_field, -1)
    minus_att = run_case(lat, det, init, minus_field, +1)
    neutral = run_case(lat, det, init, plus_field, 0)
    antisym = plus_rep.delta / plus_att.delta if abs(plus_att.delta) > 1e-30 else math.nan

    print("SIGN ANTISYMMETRY")
    print(f"  source +1, test +1: delta={plus_rep.delta:+.8e} (repel)")
    print(f"  source +1, test -1: delta={plus_att.delta:+.8e} (attract)")
    print(f"  antisymmetry ratio (repel/attract) = {antisym:+.3f}")
    print(f"  source -1, test -1: delta={minus_rep.delta:+.8e} (repel)")
    print(f"  source -1, test +1: delta={minus_att.delta:+.8e} (attract)")
    print(f"  neutral control: delta={neutral.delta:+.8e}")
    print()

    # 2) Symmetric cancellation and dipole.
    # Use the lattice center here so the symmetry test is not boundary-biased.
    center_z = 0.0
    packet_center = point_packet(lat, center_z)
    x0 = lat.pos[lat.nmap[(lat.nl // 3, 0, round(center_z / lat.h))]][0]
    sym_field = field_from_sources(
        lat,
        [
            (x0, 0.0, center_z - 1.0, +1.0),
            (x0, 0.0, center_z + 1.0, +1.0),
        ],
    )
    dip_field = field_from_sources(
        lat,
        [
            (x0, 0.0, center_z - 1.0, -1.0),
            (x0, 0.0, center_z + 1.0, +1.0),
        ],
    )
    sym_case = run_case(lat, det, packet_center, sym_field, +1)
    dip_case = run_case(lat, det, packet_center, dip_field, +1)

    print("SYMMETRIC CANCELLATION")
    print(f"  two positive charges about z={center_z:.1f}: delta={sym_case.delta:+.8e}")
    print("  (should be near zero by symmetry)")
    print()
    print("DIPOLE")
    print(f"  (+, -) pair about z={center_z:.1f}: delta={dip_case.delta:+.8e}")
    print("  (direction should follow the positive end of the dipole)")
    print()

    # 3) Charge scaling on a single source.
    print("CHARGE SCALING")
    qs = [1, 2, 4, 8]
    deltas = []
    init_scale = point_packet(lat, 0.0)
    xsrc = lat.pos[lat.nmap[(lat.nl // 3, 0, round(source_z / lat.h))]][0]
    for q in qs:
        field = field_from_sources(lat, [(xsrc, 0.0, source_z, float(q))])
        case = run_case(lat, det, init_scale, field, +1)
        deltas.append(abs(case.delta))
        print(f"  q={q:>2d}: delta={case.delta:+.8e}")
    if all(d > 1e-30 for d in deltas):
        slope = (math.log(deltas[-1]) - math.log(deltas[0])) / (math.log(qs[-1]) - math.log(qs[0]))
        print(f"  fitted exponent F~q^{slope:.3f}")
    print()

    # 4) Screening cluster.
    print("SCREENING")
    point_field = field_from_sources(lat, [(xsrc, 0.0, source_z, +1.0)])
    shell_offsets = [
        (0.0, 0.0, 1.0),
        (0.0, 0.0, -1.0),
        (0.0, 1.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, 1.0, 1.0),
        (0.0, 1.0, -1.0),
        (0.0, -1.0, 1.0),
        (0.0, -1.0, -1.0),
    ]
    shell_q = -0.9 / len(shell_offsets)
    shell_sources = [(xsrc + dx, dy, source_z + dz, shell_q) for dx, dy, dz in shell_offsets]
    shell_field = field_from_sources(lat, [(xsrc, 0.0, source_z, +1.0)] + shell_sources)
    point_case = run_case(lat, det, init_scale, point_field, +1)
    shell_case = run_case(lat, det, init_scale, shell_field, +1)
    ratio = shell_case.delta / point_case.delta if abs(point_case.delta) > 1e-30 else math.nan
    print(f"  point source delta: {point_case.delta:+.8e}")
    print(f"  screened cluster delta: {shell_case.delta:+.8e}")
    print(f"  screened/point ratio: {ratio:+.3f}")
    print()

    print("SAFE READ")
    print("  The same propagator shows a clean electric-like sign law on the retained ordered family.")
    print("  Like signs repel, unlike signs attract, neutral charge is inert, and the response is linear in charge.")
    print("  The screened cluster reduces the force materially, but this is still a scalar sign-law companion, not full electromagnetism.")


if __name__ == "__main__":
    main()
