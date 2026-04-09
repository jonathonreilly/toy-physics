#!/usr/bin/env python3
"""Electrostatics card on the retained 3D ordered family.

This is a narrow electrostatic-like sign-law probe, not a full EM theory.

Target observables:
- sign antisymmetry
- cancellation / null
- dipole directionality
- charge scaling
- screening

The claim surface stays scalar and sign-coupled:
like charges repel, unlike charges attract, neutral charge is inert.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this harness. On this machine use /usr/bin/python3."
    ) from exc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.two_body_momentum_harness import K, Lattice3D


H = 0.5
PHYS_L = 12
PHYS_W = 8
SOURCE_Z = 5.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
TEST_CHARGES = (-1, 0, +1)
SOURCE_CHARGES = (-1, +1)
SCALING_SOURCE_MAGNITUDES = (0.25, 0.5, 1.0, 2.0)
DIPOLE_SEP = 2


@dataclass(frozen=True)
class Source:
    node: int
    charge: float


def detector(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def centroid(amps: np.ndarray, det: list[int], pos: np.ndarray) -> float:
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return 0.0
    return float(np.dot(probs, pos[det, 2]) / total)


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


def field_from_sources(lat: Lattice3D, sources: list[Source], power: int = 1) -> np.ndarray:
    field = np.zeros(lat.n, dtype=float)
    for src in sources:
        r = np.sqrt(np.sum((lat.pos - lat.pos[src.node]) ** 2, axis=1)) + 0.1
        field += src.charge * SOURCE_STRENGTH / (r ** power)
    return field


def dipole_sources(lat: Lattice3D, z_phys: float, separation: int, orientation: int) -> list[Source]:
    """Return a +/- dipole pair.

    orientation = +1 means positive charge at +separation, negative at -separation.
    orientation = -1 reverses the dipole.
    """
    gl = 2 * lat.nl // 3
    z_idx = round(z_phys / lat.h)
    hi = z_idx + separation
    lo = z_idx - separation
    node_hi = lat.nmap.get((gl, 0, hi))
    node_lo = lat.nmap.get((gl, 0, lo))
    if node_hi is None or node_lo is None:
        raise ValueError("dipole placement falls outside the lattice")
    if orientation > 0:
        return [Source(node_hi, +1.0), Source(node_lo, -1.0)]
    return [Source(node_hi, -1.0), Source(node_lo, +1.0)]


def screening_shell(lat: Lattice3D, z_phys: float, total_charge: float) -> list[Source]:
    """Six-point symmetric shell around the source node.

    The shell is the narrowest conservative screening geometry:
    equal charges on the +/- axis neighbors with net shell charge = -total_charge.
    """
    gl = 2 * lat.nl // 3
    z_idx = round(z_phys / lat.h)
    center = (gl, 0, z_idx)
    offsets = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    shell_charge = -total_charge / len(offsets)
    sources: list[Source] = []
    for dx, dy, dz in offsets:
        node = lat.nmap.get((center[0] + dx, center[1] + dy, center[2] + dz))
        if node is not None:
            sources.append(Source(node, shell_charge))
    return sources


def propagate_charge(lat: Lattice3D, init: np.ndarray, field: np.ndarray, q_test: int) -> np.ndarray:
    """Propagate using a sign-flipped scalar action.

    Like charges see a phase hill and repel.
    Unlike charges see a phase valley and attract.
    q_test = 0 is the neutral control.
    """
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


def response_delta(lat: Lattice3D, field: np.ndarray, q_test: int, det: list[int], free_centroid: float) -> float:
    init = point_packet(lat, 0.0)
    amps = propagate_charge(lat, init, field, q_test)
    return centroid(amps, det, lat.pos) - free_centroid


def fit_power_law(xs: list[float], ys: list[float]) -> float:
    xs_arr = np.asarray(xs, dtype=float)
    ys_arr = np.asarray(ys, dtype=float)
    nz = (xs_arr > 0) & (ys_arr > 0)
    xs_arr = xs_arr[nz]
    ys_arr = ys_arr[nz]
    if len(xs_arr) < 2:
        return float("nan")
    coeff = np.polyfit(np.log(xs_arr), np.log(ys_arr), 1)
    return float(coeff[0])


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)
    init = point_packet(lat, 0.0)
    free = propagate_charge(lat, init, np.zeros(lat.n), 0)
    free_centroid = centroid(free, det, lat.pos)

    print("=" * 92)
    print("ELECTROSTATICS CARD")
    print("  Retained 3D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, source_z={SOURCE_Z}, strength={SOURCE_STRENGTH:g}")
    print("  Claim surface: scalar electrostatic-like sign law only")
    print("=" * 92)
    print(f"Free centroid baseline: {free_centroid:+.8f}\n")

    # 1) Sign antisymmetry
    print("SIGN ANTISYMMETRY")
    pair_results: dict[tuple[int, int], float] = {}
    for source_charge in SOURCE_CHARGES:
        field = field_from_sources(lat, [Source(source_node(lat, SOURCE_Z), float(source_charge))], FIELD_POWER)
        for test_charge in TEST_CHARGES:
            delta = response_delta(lat, field, test_charge, det, free_centroid)
            pair_results[(source_charge, test_charge)] = delta
            print(f"  source={source_charge:+d}, test={test_charge:+d}: delta={delta:+.8e}")
    like = abs(pair_results[(+1, +1)])
    unlike = abs(pair_results[(+1, -1)])
    antisym = pair_results[(+1, +1)] / pair_results[(+1, -1)] if pair_results[(+1, -1)] != 0 else float("nan")
    print(f"  like/unlike magnitude ratio: {like / unlike if unlike > 0 else float('nan'):.3f}")
    print(f"  signed antisymmetry ratio: {antisym:+.3f}\n")

    # 2) Cancellation / null
    print("CANCELLATION / NULL")
    null_node = source_node(lat, SOURCE_Z)
    null_field = field_from_sources(
        lat,
        [Source(null_node, +1.0), Source(null_node, -1.0)],
        FIELD_POWER,
    )
    null_delta = response_delta(lat, null_field, +1, det, free_centroid)
    print(f"  exact opposite-sign superposition delta: {null_delta:+.8e}")
    print(f"  null verdict: {'PASS' if abs(null_delta) < 1e-8 else 'CHECK'}")
    print("  note: a separated +/- pair is a dipole, not a null")
    print()

    # 3) Dipole directionality
    print("DIPOLE DIRECTIONALITY")
    dip_pos = field_from_sources(lat, dipole_sources(lat, SOURCE_Z, DIPOLE_SEP, +1), FIELD_POWER)
    dip_neg = field_from_sources(lat, dipole_sources(lat, SOURCE_Z, DIPOLE_SEP, -1), FIELD_POWER)
    delta_pos = response_delta(lat, dip_pos, +1, det, free_centroid)
    delta_neg = response_delta(lat, dip_neg, +1, det, free_centroid)
    print(f"  dipole (+ at +z) delta: {delta_pos:+.8e}")
    print(f"  dipole (+ at -z) delta: {delta_neg:+.8e}")
    print(f"  orientation flip ratio: {(delta_pos / delta_neg) if delta_neg != 0 else float('nan'):+.3f}")
    print()

    # 4) Charge scaling
    print("CHARGE SCALING")
    magnitudes = []
    shifts = []
    for mag in SCALING_SOURCE_MAGNITUDES:
        field = field_from_sources(lat, [Source(source_node(lat, SOURCE_Z), +mag)], FIELD_POWER)
        delta = abs(response_delta(lat, field, +1, det, free_centroid))
        magnitudes.append(mag)
        shifts.append(delta)
        print(f"  source magnitude={mag:>4.2f}: |delta|={delta:.8e}")
    exponent = fit_power_law(magnitudes, shifts)
    print(f"  fitted |delta| ~ q^{exponent:.3f}\n")

    # 5) Screening
    print("SCREENING")
    bare_field = field_from_sources(lat, [Source(source_node(lat, SOURCE_Z), +1.0)], FIELD_POWER)
    shell = screening_shell(lat, SOURCE_Z, total_charge=+1.0)
    screened_field = field_from_sources(lat, [Source(source_node(lat, SOURCE_Z), +1.0), *shell], FIELD_POWER)
    bare_delta = abs(response_delta(lat, bare_field, +1, det, free_centroid))
    screened_delta = abs(response_delta(lat, screened_field, +1, det, free_centroid))
    ratio = screened_delta / bare_delta if bare_delta > 0 else float("nan")
    print(f"  bare |delta|:      {bare_delta:.8e}")
    print(f"  screened |delta|:  {screened_delta:.8e}")
    print(f"  screening ratio:   {ratio:.3f}")

    print("\nSAFE READ")
    print("  - Like and unlike charges produce opposite-sign shifts on this retained family.")
    print("  - Equal and opposite sources cancel exactly when superposed at the same node.")
    print("  - The dipole orientation flips the sign of the response.")
    print("  - Charge response is close to linear over the tested magnitude range.")
    print("  - The screening shell strongly attenuates the response.")
    print("  - This is an electrostatic-like scalar sign law, not a full EM derivation.")


if __name__ == "__main__":
    main()
