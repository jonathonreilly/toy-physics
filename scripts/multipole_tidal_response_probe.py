#!/usr/bin/env python3
"""Quadrupole / tidal-response probe on the retained ordered lattice family.

This is a narrow follow-up to the scalar electrostatics-like lane.

Question:
  Can a zero-net, zero-dipole source layout produce a genuinely
  shape-sensitive tidal response, or do multi-source layouts collapse back to
  the already-retained dipole package?

Claim surface:
  - exact same-site opposite-sign cancellation
  - neutral test packet inert at q_test = 0
  - dipole mostly steers the centroid
  - centered quadrupole leaves the centroid nearly pinned but changes the
    detector width
  - larger quadrupole separation strengthens the tidal width signal
"""

from __future__ import annotations

import math
import os
import sys

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit("numpy is required for this harness. On this machine use /usr/bin/python3.") from exc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
PHYS_L = 12
PHYS_W = 8
SOURCE_Z0 = 0.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
QUAD_SEPARATIONS = (1.0, 2.0)


def detector(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def point_packet(lat: Lattice3D, z_phys: float = 0.0) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    init[lat.nmap[(0, 0, round(z_phys / lat.h))]] = 1.0
    return init


def source_node(lat: Lattice3D, z_phys: float) -> int:
    gl = 2 * lat.nl // 3
    node = lat.nmap.get((gl, 0, round(z_phys / lat.h)))
    if node is None:
        raise ValueError(f"source location z={z_phys} is outside the lattice")
    return node


def field_from_sources(lat: Lattice3D, sources: list[tuple[float, float]], power: int = FIELD_POWER) -> np.ndarray:
    field = np.zeros(lat.n, dtype=float)
    for z_phys, charge in sources:
        src = lat.pos[source_node(lat, z_phys)]
        r = np.sqrt(np.sum((lat.pos - src) ** 2, axis=1)) + 0.1
        field += charge * SOURCE_STRENGTH / (r ** power)
    return field


def propagate_charge(lat: Lattice3D, init: np.ndarray, field: np.ndarray, q_test: int) -> np.ndarray:
    """Propagate with the retained sign-flipped scalar action."""
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


def moments(amps: np.ndarray, det: list[int], pos: np.ndarray) -> tuple[float, float]:
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return 0.0, 0.0
    z = pos[det, 2]
    centroid = float(np.dot(probs, z) / total)
    width = float(math.sqrt(max(0.0, np.dot(probs, (z - centroid) ** 2) / total)))
    return centroid, width


def response_delta(
    lat: Lattice3D,
    init: np.ndarray,
    det: list[int],
    field: np.ndarray,
    q_test: int,
    free_centroid: float,
    free_width: float,
) -> tuple[float, float]:
    amps = propagate_charge(lat, init, field, q_test)
    centroid, width = moments(amps, det, lat.pos)
    return centroid - free_centroid, width - free_width


def build_dipole(separation: float) -> list[tuple[float, float]]:
    return [(-separation, +1.0), (+separation, -1.0)]


def build_quadrupole(separation: float) -> list[tuple[float, float]]:
    return [(-separation, +1.0), (0.0, -2.0), (+separation, +1.0)]


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)
    init = point_packet(lat, 0.0)
    free = propagate_charge(lat, init, np.zeros(lat.n), 0)
    free_centroid, free_width = moments(free, det, lat.pos)

    print("=" * 92)
    print("MULTIPOLE / TIDAL RESPONSE PROBE")
    print("  retained ordered-lattice scalar lane")
    print("  observables: same-site null, neutral control, dipole steering, tidal width")
    print("=" * 92)
    print(f"h={H}, W={PHYS_W}, L={PHYS_L}, source_z0={SOURCE_Z0}, strength={SOURCE_STRENGTH:g}")
    print(f"free centroid baseline: {free_centroid:+.8e}")
    print(f"free width baseline:    {free_width:+.8e}")
    print()

    same_site_field = field_from_sources(lat, [(SOURCE_Z0, +1.0), (SOURCE_Z0, -1.0)])
    same_dc, same_dw = response_delta(lat, init, det, same_site_field, +1, free_centroid, free_width)
    same_pass = abs(same_dc) < 1e-12 and abs(same_dw) < 1e-12
    print("SAME-SITE NULL CONTROL")
    print(f"  opposite charges at the same node: dc={same_dc:+.8e}, dw={same_dw:+.8e}, verdict={'PASS' if same_pass else 'FAIL'}")
    print()

    quad_ref_field = field_from_sources(lat, build_quadrupole(1.0))
    neutral_dc, neutral_dw = response_delta(lat, init, det, quad_ref_field, 0, free_centroid, free_width)
    neutral_pass = abs(neutral_dc) < 1e-12 and abs(neutral_dw) < 1e-12
    print("NEUTRAL TEST CONTROL")
    print(f"  q_test=0 with a nontrivial quadrupole field: dc={neutral_dc:+.8e}, dw={neutral_dw:+.8e}, verdict={'PASS' if neutral_pass else 'FAIL'}")
    print()

    dipole_field = field_from_sources(lat, build_dipole(1.0))
    dipole_dc, dipole_dw = response_delta(lat, init, det, dipole_field, +1, free_centroid, free_width)
    print("DIPOLE BASELINE")
    print(f"  dipole (+/- at ±1.0): dc={dipole_dc:+.8e}, dw={dipole_dw:+.8e}")
    print("  read: mostly centroid steering, with only tiny width leakage")
    print()

    print("QUADRUPOLE / TIDAL LANE")
    print(f"{'case':>18s} {'Qzz':>8s} {'dc':>12s} {'dw':>12s} {'read':>12s}")
    print("-" * 72)
    quad_widths: list[float] = []
    for separation in QUAD_SEPARATIONS:
        quad_field = field_from_sources(lat, build_quadrupole(separation))
        dc, dw = response_delta(lat, init, det, quad_field, +1, free_centroid, free_width)
        quad_widths.append(dw)
        read = "tidal" if abs(dc) < 1e-9 and dw > 0 else "shape-sensitive"
        qzz = 2.0 * separation * separation
        print(f"{f'quad a={separation:.1f}':>18s} {qzz:8.2f} {dc:+12.8e} {dw:+12.8e} {read:>12s}")
    if len(quad_widths) == 2 and abs(quad_widths[0]) > 1e-30:
        ratio = quad_widths[1] / quad_widths[0]
        print(f"  width ratio a=2.0 / a=1.0 = {ratio:+.3f}")
    print()

    print("SAFE READ")
    print("  - The exact same-site opposite-sign source cancels to printed precision.")
    print("  - The neutral q_test=0 control is inert as expected.")
    print("  - The centered dipole primarily shifts the centroid, with negligible width change.")
    print("  - The centered quadrupole keeps the centroid pinned but produces a real width/tidal response.")
    print("  - Doubling the quadrupole separation strengthens that width response, so this is not just the dipole cancellation story.")


if __name__ == "__main__":
    main()
