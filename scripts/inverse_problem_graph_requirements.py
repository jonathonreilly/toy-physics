#!/usr/bin/env python3
"""Bounded inverse-problem graph-requirements harness.

This is a review-safe follow-up to the doc-only inverse-problem note.

Question:
  On the retained 3D valley-linear family, how much graph structure is
  actually required for Newton+Born to survive?

We test a small, bounded perturbation set:
  - baseline regular lattice
  - 70% random edge deletion
  - asymmetric graph (edges into z > 0 removed)
  - transverse jitter of node positions
  - sparse NN-only connectivity

Controls:
  - k = 0 with field on
  - no-field with k > 0

This is intentionally bounded. It is a graph-robustness probe, not a theorem.
"""

from __future__ import annotations

import math
import os
import sys
import time
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


K = 5.0
BETA = 0.8
H = 0.5
PHYS_L = 12
PHYS_W = 8
MAX_D_PHYS = 3
STRENGTH = 5e-5
MASS_Z = 3.0
JITTER = 0.5
EDGE_DELETE_PROB = 0.7
SEED = 20260404


@dataclass(frozen=True)
class VariantSpec:
    name: str
    max_d_phys: int = MAX_D_PHYS
    jitter: float = 0.0
    edge_delete_prob: float = 0.0
    asym_zpos_removed: bool = False


class GraphLattice3D:
    def __init__(
        self,
        phys_l: int,
        phys_w: int,
        h: float,
        max_d_phys: int,
        jitter: float = 0.0,
        edge_delete_prob: float = 0.0,
        asym_zpos_removed: bool = False,
        seed: int = SEED,
    ) -> None:
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
        self._nw = 2 * self.hw + 1
        self.npl = self._nw**2
        self.n = self.nl * self.npl
        self._hm = h * h

        self.grid_pos = np.zeros((self.n, 3), dtype=float)
        self.pos = np.zeros((self.n, 3), dtype=float)
        self.nmap: dict[tuple[int, int, int], int] = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.grid_pos[idx] = (x, iy * h, iz * h)
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(layer, iy, iz)] = idx
                    idx += 1

        if jitter > 0.0:
            rng = np.random.default_rng(seed)
            # Keep the layer ordering intact while perturbing transverse geometry.
            self.pos[:, 0] += rng.uniform(-0.25 * h, 0.25 * h, size=self.n)
            self.pos[:, 1] += rng.uniform(-jitter * h, jitter * h, size=self.n)
            self.pos[:, 2] += rng.uniform(-jitter * h, jitter * h, size=self.n)

        self._off: list[tuple[int, int, float, float]] = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
                self._off.append((dy, dz, L, math.exp(-BETA * theta * theta)))

        self._src_iz = np.tile(np.arange(-self.hw, self.hw + 1), self._nw)
        self._edge_masks = self._build_edge_masks(edge_delete_prob, asym_zpos_removed, seed)

    def _build_edge_masks(
        self,
        edge_delete_prob: float,
        asym_zpos_removed: bool,
        seed: int,
    ) -> list[list[np.ndarray]] | None:
        if edge_delete_prob <= 0.0 and not asym_zpos_removed:
            return None

        rng = np.random.default_rng(seed)
        masks: list[list[np.ndarray]] = []
        for layer in range(self.nl - 1):
            layer_masks: list[np.ndarray] = []
            for dy, dz, _, _ in self._off:
                mask = np.ones(self.npl, dtype=bool)
                if edge_delete_prob > 0.0:
                    mask &= rng.random(self.npl) >= edge_delete_prob
                if asym_zpos_removed:
                    dest_z = self._src_iz + dz
                    mask &= dest_z <= 0
                layer_masks.append(mask)
            masks.append(layer_masks)
        return masks

    def detector_indices(self) -> list[int]:
        return [
            self.nmap[(self.nl - 1, iy, iz)]
            for iy in range(-self.hw, self.hw + 1)
            for iz in range(-self.hw, self.hw + 1)
            if (self.nl - 1, iy, iz) in self.nmap
        ]

    def barrier_indices(self) -> list[int]:
        bl = self.nl // 3
        return [
            self.nmap[(bl, iy, iz)]
            for iy in range(-self.hw, self.hw + 1)
            for iz in range(-self.hw, self.hw + 1)
            if (bl, iy, iz) in self.nmap
        ]

    def propagate(self, field: np.ndarray, k: float, blocked_set: set[int]) -> np.ndarray:
        amps = np.zeros(self.n, dtype=np.complex128)
        amps[self.nmap[(0, 0, 0)]] = 1.0

        blocked = np.zeros(self.n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True

        for layer in range(self.nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1]
            sa = amps[ls : ls + self.npl].copy()
            sa[blocked[ls : ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue

            sf = field[ls : ls + self.npl]
            df = field[ld : ld + self.npl]
            db = blocked[ld : ld + self.npl]

            for off_idx, (dy, dz, L, w) in enumerate(self._off):
                ym = max(0, -dy)
                yM = min(self._nw, self._nw - dy)
                zm = max(0, -dz)
                zM = min(self._nw, self._nw - dz)
                if ym >= yM or zm >= zM:
                    continue

                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing="ij")
                si = siy.ravel() * self._nw + siz.ravel()
                di = (siy.ravel() + dy) * self._nw + (siz.ravel() + dz)
                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue

                src = si[nz]
                dst = di[nz]
                if self._edge_masks is not None:
                    keep = self._edge_masks[layer][off_idx][src]
                    if not np.any(keep):
                        continue
                    src = src[keep]
                    dst = dst[keep]
                    a = a[nz][keep]
                else:
                    a = a[nz]

                lf = 0.5 * (sf[src] + df[dst])
                act = L * (1.0 - lf)
                c = a * np.exp(1j * k * act) * w * self._hm / (L * L)
                c[db[dst]] = 0
                np.add.at(amps[ld : ld + self.npl], dst, c)

        return amps


def centroid_z(amps: np.ndarray, det: list[int], pos: np.ndarray) -> float:
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return float("nan")
    return float(np.dot(probs, pos[det, 2]) / total)


def make_field(lat: GraphLattice3D, z_mass_phys: float, strength: float) -> np.ndarray:
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n, dtype=float)
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx) ** 2 + (lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2) + 0.1
    return strength / r


def slit_sets(lat: GraphLattice3D) -> tuple[list[int], list[int], list[int], set[int]]:
    barrier = lat.barrier_indices()
    upper = [i for i in barrier if lat.grid_pos[i, 1] > 1]
    lower = [i for i in barrier if lat.grid_pos[i, 1] < -1]
    middle = [i for i in barrier if abs(lat.grid_pos[i, 1]) <= 1 and abs(lat.grid_pos[i, 2]) <= 1]
    blocked = set(barrier) - set(upper + lower + middle)
    return upper, lower, middle, blocked


def born_ratio(lat: GraphLattice3D) -> float:
    det = lat.detector_indices()
    upper, lower, middle, blocked = slit_sets(lat)
    if not (upper and lower and middle):
        return float("nan")

    field = np.zeros(lat.n, dtype=float)
    a, b, c = upper[0], lower[0], middle[0]
    all_s = {a, b, c}
    other = set(lat.barrier_indices()) - all_s
    probs: dict[str, np.ndarray] = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", {a, b}),
        ("ac", {a, c}),
        ("bc", {b, c}),
        ("a", {a}),
        ("b", {b}),
        ("c", {c}),
    ]:
        blocked2 = other | (all_s - open_set)
        amps = lat.propagate(field, K, blocked2)
        probs[key] = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)

    i3_sum = 0.0
    p_sum = 0.0
    for di in range(len(det)):
        i3 = (
            probs["abc"][di]
            - probs["ab"][di]
            - probs["ac"][di]
            - probs["bc"][di]
            + probs["a"][di]
            + probs["b"][di]
            + probs["c"][di]
        )
        i3_sum += abs(i3)
        p_sum += probs["abc"][di]
    return i3_sum / p_sum if p_sum > 1e-30 else float("nan")


def gravity_delta(lat: GraphLattice3D, field: np.ndarray, k: float) -> float:
    det = lat.detector_indices()
    _, _, _, blocked = slit_sets(lat)
    free = lat.propagate(np.zeros(lat.n, dtype=float), k, blocked)
    grav = lat.propagate(field, k, blocked)
    z_free = centroid_z(free, det, lat.pos)
    z_grav = centroid_z(grav, det, lat.pos)
    if not (np.isfinite(z_free) and np.isfinite(z_grav)):
        return float("nan")
    return z_grav - z_free


def measure_variant(spec: VariantSpec) -> dict[str, float | str]:
    lat = GraphLattice3D(
        PHYS_L,
        PHYS_W,
        H,
        spec.max_d_phys,
        jitter=spec.jitter,
        edge_delete_prob=spec.edge_delete_prob,
        asym_zpos_removed=spec.asym_zpos_removed,
        seed=SEED,
    )
    born = born_ratio(lat)
    field = make_field(lat, MASS_Z, STRENGTH)
    grav = gravity_delta(lat, field, K)
    grav_k0 = gravity_delta(lat, field, 0.0)
    grav_no_field = gravity_delta(lat, np.zeros(lat.n, dtype=float), K)
    return {
        "variant": spec.name,
        "born": born,
        "grav": grav,
        "grav_sign": "TOWARD" if grav > 0 else "AWAY" if grav < 0 else "ZERO",
        "k0": grav_k0,
        "no_field": grav_no_field,
    }


def fmt(x: float) -> str:
    if math.isnan(x):
        return "nan"
    return f"{x:+.6e}"


def main() -> None:
    t0 = time.time()
    variants = [
        VariantSpec("baseline"),
        VariantSpec("heavy_delete_70", edge_delete_prob=EDGE_DELETE_PROB),
        VariantSpec("asym_zpos_removed", asym_zpos_removed=True),
        VariantSpec("jitter_0.5h", jitter=JITTER),
        VariantSpec("sparse_nn_only", max_d_phys=1),
    ]

    print("=" * 98)
    print("INVERSE PROBLEM GRAPH REQUIREMENTS")
    print("  Retained 3D valley-linear family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={MAX_D_PHYS}")
    print(f"  field strength={STRENGTH:g}, mass_z={MASS_Z}, phase_k={K}")
    print("  Goal: what graph structure is actually required for Newton + Born to survive?")
    print("  Controls: k=0 and no-field")
    print("=" * 98)
    print()
    print(f"{'variant':<20} {'Born':>10} {'grav':>14} {'sign':>8} {'k=0':>14} {'no-field':>14}")
    print("-" * 98)

    rows = []
    for spec in variants:
        row = measure_variant(spec)
        rows.append(row)
        print(
            f"{row['variant']:<20} "
            f"{float(row['born']):>10.2e} "
            f"{fmt(float(row['grav'])):>14s} "
            f"{str(row['grav_sign']):>8s} "
            f"{fmt(float(row['k0'])):>14s} "
            f"{fmt(float(row['no_field'])):>14s}"
        )

    grav_vals = [float(r["grav"]) for r in rows if np.isfinite(float(r["grav"]))]
    born_vals = [float(r["born"]) for r in rows if np.isfinite(float(r["born"]))]
    k0_vals = [float(r["k0"]) for r in rows if np.isfinite(float(r["k0"]))]
    nf_vals = [float(r["no_field"]) for r in rows if np.isfinite(float(r["no_field"]))]

    print()
    print("SAFE READ")
    print("  - Gravity survives the tested graph perturbations if the rows stay TOWARD.")
    print("  - Born stays machine-clean if the Born column remains near zero.")
    print("  - k=0 and no-field controls should stay near zero; that is the phase test.")
    print("  - This is a bounded inverse-problem harness, not a universal graph theorem.")
    if grav_vals:
        print(f"  - gravity range: {min(grav_vals):+.6e} to {max(grav_vals):+.6e}")
    if born_vals:
        print(f"  - Born range: {min(born_vals):.2e} to {max(born_vals):.2e}")
    if k0_vals:
        print(f"  - k=0 range: {min(k0_vals):+.6e} to {max(k0_vals):+.6e}")
    if nf_vals:
        print(f"  - no-field range: {min(nf_vals):+.6e} to {max(nf_vals):+.6e}")

    # Bounded-table assertions tied to docs/INVERSE_PROBLEM_NOTE.md.
    # These pin the narrowed claim: Born stays machine-clean on every
    # variant, TOWARD holds for the four structure-preserving variants,
    # heavy_delete_70 is a known AWAY counterexample, and the k=0 and
    # no-field controls are exactly zero.
    by_name = {r["variant"]: r for r in rows}
    expected_signs = {
        "baseline": "TOWARD",
        "heavy_delete_70": "AWAY",
        "asym_zpos_removed": "TOWARD",
        "jitter_0.5h": "TOWARD",
        "sparse_nn_only": "TOWARD",
    }
    for variant, want in expected_signs.items():
        got = str(by_name[variant]["grav_sign"])
        assert got == want, (
            f"variant {variant} expected {want}, got {got} "
            f"(grav={by_name[variant]['grav']:+.6e}); "
            "the narrowed bounded note table in "
            "docs/INVERSE_PROBLEM_NOTE.md must be re-synced."
        )
    for variant in expected_signs:
        born = float(by_name[variant]["born"])
        assert abs(born) < 1e-13, (
            f"variant {variant} Born drift |{born:.2e}| >= 1e-13 "
            "violates the bounded Born-cleanliness claim."
        )
    for variant in expected_signs:
        k0_val = float(by_name[variant]["k0"])
        nf_val = float(by_name[variant]["no_field"])
        assert k0_val == 0.0, (
            f"variant {variant} k=0 control nonzero: {k0_val:+.6e}"
        )
        assert nf_val == 0.0, (
            f"variant {variant} no-field control nonzero: {nf_val:+.6e}"
        )
    print(
        "PASS: bounded inverse-problem table matches the narrowed note "
        "(Born clean on all five variants; TOWARD on baseline/asym/jitter/"
        "sparse; AWAY on heavy_delete_70; controls exactly zero)."
    )

    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
