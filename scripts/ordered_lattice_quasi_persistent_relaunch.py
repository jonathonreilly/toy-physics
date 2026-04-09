#!/usr/bin/env python3
"""Quasi-persistent relaunch probe on the retained ordered-lattice family.

This is the smallest honest attempt to go beyond the test-particle regime
without leaving the retained 3D ordered lattice:

1. Launch a compact packet on the source plane.
2. Propagate it through the valley-linear 1/L^2 lattice.
3. Re-identify the detector profile as a compact packet surrogate.
4. Relaunch that surrogate on the same family.
5. Compare free vs mass response for the relaunch packet.

The goal is not to prove a persistent inertial mass theorem. The goal is to
see whether the retained ordered-lattice family can support a localized packet
that survives re-identification well enough to behave like a quasi-persistent
surrogate for a second propagation stage.
"""

from __future__ import annotations

import math
import os
import sys
import time

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

from scripts.lattice_3d_valley_linear_card import (  # noqa: E402
    K,
    STRENGTH,
    Lattice3D,
    make_field,
    setup_slits,
)


H = 0.5
PHYS_L = 12
PHYS_W = 8
MASS_Z = 3.0
PACKET_WEIGHTS = {
    -2: 0.10,
    -1: 0.40,
    0: 1.00,
    1: 0.40,
    2: 0.10,
}
TOPK_REIDENTIFY = 5


def detector_nodes(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def source_packet(lat: Lattice3D, weights: dict[int, float]) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    norm = math.sqrt(sum(w * w for w in weights.values()))
    for z_idx, weight in weights.items():
        idx = lat.nmap[(0, 0, z_idx)]
        init[idx] = weight / norm
    return init


def z_profile(amps: np.ndarray, det: list[int], pos: np.ndarray, h: float) -> dict[int, float]:
    profile: dict[int, float] = {}
    for d in det:
        z_idx = int(round(pos[d, 2] / h))
        profile[z_idx] = profile.get(z_idx, 0.0) + float(abs(amps[d]) ** 2)
    total = sum(profile.values())
    if total > 0:
        profile = {k: v / total for k, v in profile.items()}
    return dict(sorted(profile.items()))


def profile_centroid(profile: dict[int, float], h: float) -> float:
    total = sum(profile.values())
    if total <= 0:
        return 0.0
    return sum((z * h) * p for z, p in profile.items()) / total


def profile_spread(profile: dict[int, float], h: float) -> float:
    total = sum(profile.values())
    if total <= 0:
        return 0.0
    mu = profile_centroid(profile, h)
    return math.sqrt(sum((((z * h) - mu) ** 2) * p for z, p in profile.items()) / total)


def topk_reidentify(profile: dict[int, float], k: int) -> tuple[dict[int, float], float]:
    if not profile:
        return {}, 0.0
    items = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    selected_items = items[: min(k, len(items))]
    selected = dict(selected_items)
    capture = sum(p for _, p in selected_items)
    total = sum(selected.values())
    if total <= 0:
        return {}, 0.0
    return {z: p / total for z, p in selected.items()}, capture


def packet_from_profile(lat: Lattice3D, profile: dict[int, float]) -> np.ndarray:
    """Relaunch a probability profile as a real, positive amplitude packet."""
    init = np.zeros(lat.n, dtype=np.complex128)
    norm = math.sqrt(sum(p for p in profile.values()))
    if norm <= 0:
        return init
    for z_idx, p in profile.items():
        idx = lat.nmap[(0, 0, z_idx)]
        init[idx] = math.sqrt(p) / norm
    return init


def propagate_profile(lat: Lattice3D, init: np.ndarray, field: np.ndarray, blocked: set[int], det: list[int]) -> dict[int, float]:
    # The lattice propagator always starts from the built-in source, so we need
    # a small wrapper here: inject the desired initial packet on the first layer.
    # We reuse the lattice internals by relaunching the packet on a fresh lattice
    # state encoded as the first layer of the source plane.
    #
    # The compact ordered-lattice family is small enough that a thin wrapper is
    # acceptable here and keeps the experiment honest and local.
    if init is None:
        raise ValueError("init packet must be provided")

    # Reuse the lattice propagation logic by manually injecting the initial
    # amplitudes into the source layer and running the same forward update.
    n = lat.n
    amps = np.zeros(n, dtype=np.complex128)
    amps[: lat.npl] = init[: lat.npl]
    blocked_arr = np.zeros(n, dtype=bool)
    for b in blocked:
        blocked_arr[b] = True

    for layer in range(lat.nl - 1):
        ls = lat._ls[layer]
        ld = lat._ls[layer + 1] if layer + 1 < lat.nl else n
        sa = amps[ls : ls + lat.npl].copy()
        sa[blocked_arr[ls : ls + lat.npl]] = 0
        if np.max(np.abs(sa)) < 1e-30:
            continue
        sf = field[ls : ls + lat.npl]
        df = field[ld : ld + lat.npl]
        db = blocked_arr[ld : ld + lat.npl]
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
            act = L * (1 - lf)
            c = a[nz] * np.exp(1j * K * act) * w * lat._hm / (L * L)
            c[db[di[nz]]] = 0
            np.add.at(amps[ld : ld + lat.npl], di[nz], c)

    return z_profile(amps, det, lat.pos, lat.h)


def centroid_shift(lat: Lattice3D, free_profile: dict[int, float], mass_profile: dict[int, float]) -> float:
    return profile_centroid(mass_profile, lat.h) - profile_centroid(free_profile, lat.h)


def main() -> None:
    t_total = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector_nodes(lat)
    _, _, _, blocked, _ = setup_slits(lat)
    free_field = np.zeros(lat.n)
    mass_field, _ = make_field(lat, MASS_Z, STRENGTH)

    print("=" * 88)
    print("ORDERED-LATTICE QUASI-PERSISTENT RELAUNCH PROBE")
    print("  Goal: relaunch a localized packet surrogate and see whether it carries")
    print("  through a second propagation stage on the retained ordered family.")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, z_mass={MASS_Z}, strength={STRENGTH:g}")
    print("=" * 88)
    print()

    baseline = {
        "point": source_packet(lat, {0: 1.0}),
        "compact5": source_packet(lat, PACKET_WEIGHTS),
    }

    for name, init in baseline.items():
        print(f"CASE: {name}")
        t0 = time.time()
        free_profile = propagate_profile(lat, init, free_field, blocked, det)
        mass_profile = propagate_profile(lat, init, mass_field, blocked, det)

        topk, capture = topk_reidentify(free_profile, TOPK_REIDENTIFY)
        carry = sum(
            math.sqrt(free_profile.get(z, 0.0) * topk.get(z, 0.0))
            for z in set(free_profile) | set(topk)
        )
        shift = centroid_shift(lat, free_profile, mass_profile)
        spread = profile_spread(free_profile, lat.h)
        support90 = 0.0
        accum = 0.0
        for _, p in sorted(free_profile.items(), key=lambda kv: kv[1], reverse=True):
            support90 += 1
            accum += p
            if accum >= 0.90:
                break
        print(f"  free centroid z = {profile_centroid(free_profile, lat.h):+.4f}")
        print(f"  free spread    = {spread:.4f}")
        print(f"  support for 90% = {support90:.0f} z-bins")
        print(f"  top-{TOPK_REIDENTIFY} capture fraction = {capture:.3f}")
        print(f"  stage-1 carry overlap = {carry:.4f}")
        print(f"  field-induced centroid shift = {shift:+.6f}")

        relaunch = packet_from_profile(lat, topk if topk else free_profile)
        relaunch_free = propagate_profile(lat, relaunch, free_field, blocked, det)
        relaunch_mass = propagate_profile(lat, relaunch, mass_field, blocked, det)
        relaunch_shift = centroid_shift(lat, relaunch_free, relaunch_mass)
        relaunch_carry = sum(
            math.sqrt(free_profile.get(z, 0.0) * relaunch_free.get(z, 0.0))
            for z in set(free_profile) | set(relaunch_free)
        )
        print(f"  relaunch carry overlap = {relaunch_carry:.4f}")
        print(f"  relaunch field shift   = {relaunch_shift:+.6f}")
        print(f"  runtime = {time.time() - t0:.1f}s")
        print()

    print("SAFE READ")
    print("  - If the compact packet re-identifies cleanly and the relaunch overlap stays")
    print("    high, that is a quasi-persistent surrogate on the ordered lattice.")
    print("  - If the relaunch overlap collapses or the packet re-identifies poorly,")
    print("    the ordered-lattice family still does not support a persistent inertial object.")
    print()
    print(f"Total runtime: {time.time() - t_total:.1f}s")


if __name__ == "__main__":
    main()
