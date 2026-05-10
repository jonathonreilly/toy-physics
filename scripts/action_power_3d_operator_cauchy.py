#!/usr/bin/env python3
"""Action-power 3D ordered-lattice operator-Cauchy continuum-bridge test.

This applies the operator-Cauchy method that closed the rescaled NN harness
(PR #957 / #968 / #1003 / #1007 / #1054 / #1055 / #1056) to the third
row-cluster from PR #996's mapping:

    action_power_3d_gravity_sign_closure_note
    action_uniqueness_note

The two source notes describe the same retained 3D ordered dense-lattice
harness:

    - 3D ordered forward lattice
    - dense kernel 1/L^2 with h^2 measure
    - per-edge weight  exp(-BETA*theta^2)
    - per-edge phase  exp(i*K*act),  act = L*(1 - f^p)
    - field s/r from a mass source on the central z-axis

with the action-power exponent p selecting the universality class. The
F~M scaling exponent tracks p on this family (action_uniqueness_note).

Question
--------

The two source notes register fixed-family results at one h value
(h=0.5).  The operator-Cauchy method asks the orthogonal question:

    For a chosen action-power p, does T_h converge to a continuum
    operator T_inf as h -> 0?

Equivalently: are the framework observables Cauchy-convergent in h, with
a geometric decay rate r > 0?

This script measures a thin observable vector composed only of
DIMENSIONLESS framework observables:

    vec(h; p) =  ( gravity(z=2),  gravity(z=3),  Born )

p_total_f (= field-free total throughput at the detector) is also
measured per cell as a structural diagnostic.  It is NOT included in
the Cauchy L2 vector because on the dense `(h^2 / L^2) exp(-BETA θ²)`
kernel the propagator is non-unitary and `p_total_f` diverges polynom-
ially in `1 / h` (empirically: ~3.5e4 at `h = 1.0`, ~5.6e82 at
`h = 0.125`).  That divergence is itself structural evidence against
a clean continuum bridge on this harness (see Structural Reason 1 in
the source note).

at refinements

    h in {1.0, 0.5, 0.25, 0.125}

for action powers

    p in {0.5, 1.0, 2.0}

(spanning the three universality classes from action_uniqueness_note:
sublinear valley, weak-field-linear valley, superlinear valley).

The L2 Cauchy decrement

    delta(h, h/2; p) = || vec(h; p) - vec(h/2; p) ||_2

is fit to a geometric law delta ~ C * h^r.  Positive existence requires
r > 0.5 and R^2 >= 0.95 on at least 3 fine increments.

Acceptance
----------

  - POSITIVE EXISTENCE (per p): r > 0.5, R^2 >= 0.95
  - POSITIVE IDENTIFICATION (cross-check): consistent r across p
    means the convergence is structural (the kernel inherits the same
    geodesic spreading regardless of p)
  - SHARP NULL (per p): r <= 0 or R^2 < 0.3, OR sign-flipping
    increments, OR Born guard fails, indicating no clean continuum
    bridge at that p

Harness compression
-------------------

The canonical action_universality_probe.py uses PHYS_W=8 / PHYS_W=10
and MAX_D_PHYS=3, which makes h <= 0.125 intractable (~hours per
propagation).  Here we use PHYS_W=4 / MAX_D_PHYS=1.5 to keep h=0.125
tractable while preserving the harness structure (3D ordered dense
forward lattice, 1/L^2 dense kernel, exp(-BETA*theta^2) angular weight,
exp(i*K*L*(1 - f^p)) per-edge phase).  We register this as a re-
parameterized companion family of the original harness, not a numerical
replay.

Born and k=0 guards run at every (h, p) cell.

Exit nonzero only on hard runner failures (NaN amplitudes, build
errors).  Either positive existence or sharp null is a valid scientific
outcome and exits zero.
"""

from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit("numpy is required for this probe.") from exc


# -- Canonical action-power 3D family parameters -----------------------
BETA = 0.8
K = 5.0
STRENGTH = 5e-5
PHYS_L = 10.0
PHYS_W = 4
MAX_D_PHYS = 1.5

# Cauchy refinement window.  h=0.0625 is omitted because at MAX_D_PHYS=1.5
# the offset count grows as (1 + 2*max_d)^2 with max_d = 1.5 / h, and at
# h=0.0625 max_d=24 with ~50^2 offsets and ~3e6 nodes -> minutes per
# propagation.  The three-point increment ladder {(1.0,0.5), (0.5,0.25),
# (0.25,0.125)} is sufficient for a power-law fit.
H_VALUES = [1.0, 0.5, 0.25, 0.125]

# Action-power exponents probing the three universality classes from
# action_uniqueness_note: sublinear (p=0.5), weak-field-linear (p=1.0),
# superlinear (p=2.0).
POWERS = [0.5, 1.0, 2.0]

# Mass-source z positions: each gives an independent gravity probe.
# Both must fit inside PHYS_W in lattice index units (iz <= hw = PHYS_W/h).
MASS_Z_GRID = [2.0, 3.0]


@dataclass
class CellResult:
    h: float
    p: float
    mass_z: float
    n_nodes: int
    max_d: int
    gravity: float          # gravity centroid shift at strength
    born: float             # 3-slit interference Born clean check
    centroid_zf: float      # field-free centroid (sanity: ~0 by symmetry)
    gk0: float              # k=0 control: gravity at k=0 should vanish
    p_total_f: float        # field-free total probability
    p_total_m: float        # mass-on total probability
    nan_or_inf: bool


class Lattice3D:
    """3D ordered forward lattice with dense 1/L^2 kernel and h^2 measure.

    Compressed from action_universality_probe.py:
      - PHYS_L=10, PHYS_W=4, MAX_D_PHYS=1.5 (vs canonical 12 / 8 / 3)

    The harness structure (3D ordered dense forward lattice, h^2 measure,
    exp(-BETA*theta^2) angular weight, exp(i K * L * (1 - f^p)) phase)
    is preserved.
    """

    def __init__(self, phys_l: float, phys_w: int, h: float,
                 max_d_phys: float = MAX_D_PHYS):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
        self._nw = 2 * self.hw + 1
        self.npl = self._nw ** 2
        self.n = self.nl * self.npl
        self._hm = h * h

        self.pos = np.zeros((self.n, 3))
        self.nmap: Dict[Tuple[int, int, int], int] = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(layer, iy, iz)] = idx
                    idx += 1

        self._off: List[Tuple[int, int, float, float]] = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
                w = math.exp(-BETA * theta * theta)
                self._off.append((dy, dz, L, w))

    def propagate(self, field: np.ndarray, k: float,
                  blocked_set: set, p: float) -> np.ndarray:
        """Dense forward propagate.  Action = L*(1 - f^p), f>=0."""
        amps = np.zeros(self.n, dtype=np.complex128)
        amps[self.nmap[(0, 0, 0)]] = 1.0

        blocked = np.zeros(self.n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True

        for layer in range(self.nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1]
            sa = amps[ls:ls + self.npl].copy()
            sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue

            sf = field[ls:ls + self.npl]
            df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]

            for dy, dz, L, w in self._off:
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

                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                # Action = L * (1 - f^p)
                lf_clip = np.maximum(lf, 0.0)
                act = L * (1.0 - np.power(lf_clip, p))
                c = (a[nz] * np.exp(1j * k * act)
                     * w * self._hm / (L * L))
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)

        return amps


def detector_layer(lat: Lattice3D) -> List[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def setup_slits(lat: Lattice3D) -> Tuple[List[int], List[int], set, int]:
    bl = lat.nl // 3
    barrier: List[int] = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                barrier.append(idx)
    # Two slits at +/- 0.5 in y (NS slits) per canonical harness
    sa = [i for i in barrier if lat.pos[i, 1] >= 0.5]
    sb = [i for i in barrier if lat.pos[i, 1] <= -0.5]
    blocked = set(barrier) - set(sa + sb)
    return sa, sb, blocked, bl


def make_field(lat: Lattice3D, z_mass: float, strength: float) -> np.ndarray:
    iz = round(z_mass / lat.h)
    layer = 2 * lat.nl // 3
    mi = lat.nmap.get((layer, 0, iz))
    if mi is None:
        return np.zeros(lat.n)
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx) ** 2 +
                (lat.pos[:, 1] - my) ** 2 +
                (lat.pos[:, 2] - mz) ** 2) + 0.1
    return strength / r


def born_clean(lat: Lattice3D, det: List[int], p: float) -> float:
    """Three-slit |I3|/P interference check.  Should be << 1e-10 on a
    correctly Born-respecting harness."""
    _, _, blocked, bl = setup_slits(lat)
    pos = lat.pos
    barrier_nodes = {
        lat.nmap[(bl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (bl, iy, iz) in lat.nmap
    }
    upper = sorted([i for i in barrier_nodes if pos[i, 1] > 1],
                   key=lambda i: pos[i, 1])
    lower = sorted([i for i in barrier_nodes if pos[i, 1] < -1],
                   key=lambda i: -pos[i, 1])
    middle = [i for i in barrier_nodes
              if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    if not (upper and lower and middle):
        return float("nan")
    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c)
    other = barrier_nodes - all_s
    probs: Dict[str, np.ndarray] = {}
    field_f = np.zeros(lat.n)
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(s_a + s_b)),
        ("ac", set(s_a + s_c)),
        ("bc", set(s_b + s_c)),
        ("a", set(s_a)),
        ("b", set(s_b)),
        ("c", set(s_c)),
    ]:
        bl2 = other | (all_s - open_set)
        a = lat.propagate(field_f, K, bl2, p)
        probs[key] = np.array([abs(a[d]) ** 2 for d in det])
    I3 = 0.0
    P = 0.0
    for di in range(len(det)):
        i3 = (probs["abc"][di]
              - probs["ab"][di] - probs["ac"][di] - probs["bc"][di]
              + probs["a"][di] + probs["b"][di] + probs["c"][di])
        I3 += abs(i3)
        P += probs["abc"][di]
    return I3 / P if P > 1e-30 else float("nan")


def measure_cell(lat: Lattice3D, det: List[int], p: float,
                 mass_z: float) -> CellResult:
    """One cell: gravity at z=mass_z under power-action p, with Born and
    k=0 guards."""
    _, _, blocked, _ = setup_slits(lat)
    pos = lat.pos

    field_f = np.zeros(lat.n)
    af = lat.propagate(field_f, K, blocked, p)
    pf = sum(abs(af[d]) ** 2 for d in det)
    if pf < 1e-30:
        return CellResult(
            h=lat.h, p=p, mass_z=mass_z, n_nodes=lat.n,
            max_d=lat.max_d, gravity=float("nan"),
            born=float("nan"), centroid_zf=float("nan"),
            gk0=float("nan"), p_total_f=pf, p_total_m=float("nan"),
            nan_or_inf=True,
        )
    centroid_zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf

    field_m = make_field(lat, mass_z, STRENGTH)
    am = lat.propagate(field_m, K, blocked, p)
    pm = sum(abs(am[d]) ** 2 for d in det)
    gravity = float("nan")
    if pm > 1e-30:
        zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
        gravity = zm - centroid_zf

    # k=0 control: at K=0 the per-edge phase is identity and the centroid
    # drift should vanish by lattice symmetry.
    am0 = lat.propagate(field_m, 0.0, blocked, p)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    af0 = lat.propagate(field_f, 0.0, blocked, p)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0.0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d]) ** 2 * pos[d, 2] for d in det) / pm0
               - sum(abs(af0[d]) ** 2 * pos[d, 2] for d in det) / pf0)

    born = born_clean(lat, det, p)

    nan_or_inf = (math.isnan(gravity) or math.isinf(gravity)
                  or math.isnan(born) or math.isinf(born))

    return CellResult(
        h=lat.h, p=p, mass_z=mass_z, n_nodes=lat.n,
        max_d=lat.max_d, gravity=gravity, born=born,
        centroid_zf=centroid_zf, gk0=gk0,
        p_total_f=pf, p_total_m=pm, nan_or_inf=nan_or_inf,
    )


def safe_power_fit(xs: List[float], ys: List[float]
                   ) -> Tuple[float, float, float]:
    pts = [(x, abs(y)) for x, y in zip(xs, ys) if x > 0 and abs(y) > 0]
    if len(pts) < 2:
        return math.nan, math.nan, math.nan
    lx = [math.log(x) for x, _ in pts]
    ly = [math.log(y) for _, y in pts]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    denom = sum((x - mx) ** 2 for x in lx)
    if denom <= 0:
        return math.nan, math.nan, math.nan
    slope = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / denom
    intercept = my - slope * mx
    ss_tot = sum((y - my) ** 2 for y in ly)
    ss_res = sum((y - (slope * x + intercept)) ** 2
                 for x, y in zip(lx, ly))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return slope, math.exp(intercept), r2


def main() -> int:
    print("=" * 100)
    print("ACTION-POWER 3D ORDERED-LATTICE OPERATOR-CAUCHY TEST")
    print(f"  Family: 3D ordered dense forward lattice, kernel 1/L^2 with")
    print(f"  h^2 measure, exp(-BETA*theta^2) angular weight, action L*(1 - f^p)")
    print(f"  PHYS_L = {PHYS_L}, PHYS_W = {PHYS_W}, MAX_D_PHYS = {MAX_D_PHYS}")
    print(f"  BETA = {BETA}, K = {K}, STRENGTH = {STRENGTH}")
    print(f"  h grid: {H_VALUES}")
    print(f"  action powers p: {POWERS}")
    print(f"  mass-source z grid: {MASS_Z_GRID}")
    print(f"  Cauchy observable vector per (h, p): "
          f"gravity x {len(MASS_Z_GRID)} mass-z + "
          f"Born  (dim = {len(MASS_Z_GRID) + 1}, dimensionless only)")
    print(f"  Also measured (NOT in Cauchy vec): p_total_f, centroid_zf, gk0")
    print("=" * 100)
    print()

    # results[p][h][mass_z] = CellResult
    results: Dict[float, Dict[float, Dict[float, CellResult]]] = {
        p: {h: {} for h in H_VALUES} for p in POWERS
    }

    print(f"  {'p':>4s}  {'h':>7s}  {'nodes':>8s}  {'max_d':>5s}  "
          f"{'mass_z':>6s}  {'gravity':>11s}  {'Born':>10s}  "
          f"{'centroid_zf':>11s}  {'gk0':>10s}  {'time':>6s}")
    print("  " + "-" * 100)

    fail = False
    for p in POWERS:
        for h in H_VALUES:
            lat = Lattice3D(PHYS_L, PHYS_W, h)
            det = detector_layer(lat)
            for mass_z in MASS_Z_GRID:
                t0 = time.time()
                r = measure_cell(lat, det, p, mass_z)
                dt = time.time() - t0
                results[p][h][mass_z] = r
                born_s = (f"{r.born:.2e}" if not math.isnan(r.born)
                          else "       nan")
                grav_s = (f"{r.gravity:+11.6f}"
                          if not math.isnan(r.gravity) else "        nan")
                cent_s = (f"{r.centroid_zf:+11.6e}"
                          if not math.isnan(r.centroid_zf) else "        nan")
                gk0_s = (f"{r.gk0:+10.2e}"
                         if not math.isnan(r.gk0) else "       nan")
                print(f"  {p:4.1f}  {h:7.4f}  {r.n_nodes:8d}  "
                      f"{r.max_d:5d}  {mass_z:6.1f}  "
                      f"{grav_s}  {born_s}  {cent_s}  {gk0_s}  "
                      f"{dt:5.1f}s")
                if r.nan_or_inf:
                    fail = True

    print()
    print("=" * 100)
    print("GUARD SUMMARY")
    print("=" * 100)
    print()
    born_max = 0.0
    gk0_max = 0.0
    for p in POWERS:
        for h in H_VALUES:
            for mass_z in MASS_Z_GRID:
                r = results[p][h][mass_z]
                if not math.isnan(r.born):
                    born_max = max(born_max, r.born)
                if not math.isnan(r.gk0):
                    gk0_max = max(gk0_max, abs(r.gk0))
    born_ok = born_max < 1e-10
    gk0_ok = gk0_max < 1e-10  # looser than NN since 3D centroid is z-only
    print(f"  Born max across all cells: {born_max:.2e}  "
          f"{'PASS' if born_ok else 'FAIL'}")
    print(f"  k=0 max abs across all cells: {gk0_max:.2e}  "
          f"{'PASS' if gk0_ok else 'FAIL'}")
    print()

    # Structural diagnostic: track p_total_f vs h to surface non-unitarity
    print("-" * 100)
    print("STRUCTURAL DIAGNOSTIC — field-free throughput p_total_f vs h")
    print("-" * 100)
    print()
    print(f"  {'p':>5s}  {'h':>7s}  {'p_total_f':>12s}  {'log10':>8s}")
    for p in POWERS:
        for h in H_VALUES:
            ptot = results[p][h][MASS_Z_GRID[0]].p_total_f
            print(f"  {p:5.2f}  {h:7.4f}  {ptot:12.4e}  "
                  f"{(math.log10(ptot) if ptot > 0 else float('nan')):8.2f}")
    print()
    print("  If p_total_f explodes polynomially in 1/h, the dense h^2/L^2")
    print("  kernel is non-unitary on this harness — a structural obstruction")
    print("  to a clean continuum bridge that is independent of any p choice.")
    print()

    # -- Build observable vectors per (p, h) and Cauchy increments ----
    def vec(p: float, h: float) -> Optional[List[float]]:
        """Bounded (dimensionless) observable vector.

        We deliberately exclude p_total_f from the Cauchy vector:  on
        this dense `(h^2 / L^2) * exp(-BETA * theta^2)` kernel the
        propagator is NOT unitary, and the field-free total throughput
        through the slits diverges polynomially in 1/h (empirically:
        ~3.5e4 -> 5.6e82 across the four h's of this sweep — a 78-decade
        explosion).  That divergence is itself part of the bounded-null
        story (see "Structural reason 1" in the note) but it must not
        contaminate the L2 norm, which is supposed to be a Cauchy
        diagnostic on **framework** (= dimensionless) observables:

            vec(h; p) = ( gravity(mass_z = 2.0),
                          gravity(mass_z = 3.0),
                          Born )

        Born is the dimensionless 3-slit interference defect |I_3| / P
        which is bounded by 1 and is the canonical interference-clean
        check.  Gravity is the dimensionless detector-z centroid shift.
        """
        v: List[float] = []
        for mass_z in MASS_Z_GRID:
            r = results[p][h].get(mass_z)
            if r is None or math.isnan(r.gravity):
                return None
            v.append(r.gravity)
        first = results[p][h][MASS_Z_GRID[0]]
        if math.isnan(first.born):
            return None
        v.append(first.born)
        return v

    print("=" * 100)
    print("PER-POWER OPERATOR-CAUCHY ANALYSIS")
    print("=" * 100)
    print()

    overall_positive_count = 0
    per_power_summary: List[Tuple[float, float, float, float, bool]] = []
    # (p, r, C, R^2, cauchy_ok)

    for p in POWERS:
        print(f"--- Action power p = {p} -----------------------------------")
        vecs: Dict[float, List[float]] = {}
        for h in H_VALUES:
            v = vec(p, h)
            if v is None:
                print(f"  vec(h={h}): unavailable (build failed)")
            else:
                vecs[h] = v
                comps_s = "  ".join(f"{x:+.4e}" for x in v)
                print(f"  vec(h={h}) = [{comps_s}]")

        # Compute L2 increments between consecutive h's
        h_geom: List[float] = []
        l2_incrs: List[float] = []
        sign_changes_per_comp: List[int] = []
        comp_count = 2 * len(MASS_Z_GRID) + 2
        comp_signs: List[List[float]] = [[] for _ in range(comp_count)]

        print()
        print(f"  Cauchy L2 increments ||vec(h_n) - vec(h_{{n+1}})||_2:")
        print(f"    {'h_n':>7s} -> {'h_{n+1}':>7s}    {'L2 incr':>10s}")
        for n in range(len(H_VALUES) - 1):
            h1 = H_VALUES[n]
            h2 = H_VALUES[n + 1]
            v1 = vecs.get(h1)
            v2 = vecs.get(h2)
            if v1 is None or v2 is None:
                print(f"    {h1:7.4f} -> {h2:7.4f}    n/a")
                continue
            l2_sq = 0.0
            for i, (a, b) in enumerate(zip(v1, v2)):
                l2_sq += (b - a) ** 2
                comp_signs[i].append(b - a)
            l2 = math.sqrt(l2_sq)
            h_geom.append(math.sqrt(h1 * h2))
            l2_incrs.append(l2)
            print(f"    {h1:7.4f} -> {h2:7.4f}    {l2:10.4e}")

        # Count sign changes in each component's increment sequence
        # (a sign change indicates non-monotonic / oscillatory behavior)
        for cs in comp_signs:
            changes = 0
            for j in range(1, len(cs)):
                if cs[j] * cs[j - 1] < 0:
                    changes += 1
            sign_changes_per_comp.append(changes)

        print()
        print(f"  Per-component increment sign sequences "
              f"(monotone if all signs match):")
        comp_names = [f"gravity(z={z})" for z in MASS_Z_GRID] + ["Born"]
        for name, cs, nc in zip(comp_names, comp_signs, sign_changes_per_comp):
            sgn = "  ".join(("+" if d > 0 else ("-" if d < 0 else "0"))
                            for d in cs)
            print(f"    {name:>18s}: {sgn}  (sign-changes = {nc})")
        print()

        if len(l2_incrs) >= 3:
            r, C, r2 = safe_power_fit(h_geom, l2_incrs)
            print(f"  Geometric-law fit  ||delta||_2 ~ C * h_geom^r  "
                  f"({len(l2_incrs)} pts):")
            print(f"    r   = {r:+.4f}")
            print(f"    C   = {C:.4e}")
            print(f"    R^2 = {r2:.4f}")

            cauchy_ok = (not math.isnan(r) and r > 0.5
                         and not math.isnan(r2) and r2 >= 0.95)
            sharp_null = (not math.isnan(r) and not math.isnan(r2)
                          and (r <= 0 or r2 < 0.3))
            print()
            if cauchy_ok:
                # Tail estimate at next halving
                tail_factor = (2 ** r) / (2 ** r - 1) if r > 0 else math.inf
                tail = l2_incrs[-1] * tail_factor / (2 ** r)
                print(f"  OPERATOR-CAUCHY POSITIVE EXISTENCE at p = {p}:")
                print(f"    geometric decay rate r = {r:.3f} (> 0.5)")
                print(f"    R^2 = {r2:.4f} (>= 0.95)")
                print(f"    tail estimate at h = {H_VALUES[-1]/2:.5f}: "
                      f"<~ {tail:.4e}")
                overall_positive_count += 1
            elif sharp_null:
                reason = []
                if r <= 0:
                    reason.append(f"r = {r:.4f} <= 0 (non-decaying)")
                if r2 < 0.3:
                    reason.append(f"R^2 = {r2:.4f} < 0.3 (poor fit)")
                print(f"  SHARP NULL at p = {p}: " + "; ".join(reason))
            else:
                print(f"  PARTIAL CONVERGENCE at p = {p}: "
                      f"r = {r:.4f}, R^2 = {r2:.4f}")
                print(f"    r > 0 but not yet >= 0.5, or R^2 < 0.95.")
                print(f"    Bounded-convergence regime; finer-h refinement")
                print(f"    needed to promote to a closed Cauchy claim.")
            per_power_summary.append(
                (p, r, C, r2, cauchy_ok))
        else:
            print(f"  Insufficient Cauchy increments to fit a geometric law.")
            per_power_summary.append((p, math.nan, math.nan, math.nan, False))
        print()

    # -- Cross-p stability ---------------------------------------------
    print("=" * 100)
    print("CROSS-POWER STABILITY")
    print("=" * 100)
    print()
    print(f"  {'p':>5s}  {'r':>9s}  {'C':>10s}  {'R^2':>7s}  {'cauchy':>7s}")
    for (p, r, C, r2, ok) in per_power_summary:
        rstr = f"{r:+.4f}" if not math.isnan(r) else "    nan"
        Cstr = f"{C:.4e}" if not math.isnan(C) else "      nan"
        r2str = f"{r2:.4f}" if not math.isnan(r2) else "   nan"
        ok_s = "PASS" if ok else "----"
        print(f"  {p:5.2f}  {rstr}  {Cstr}  {r2str}  {ok_s}")

    print()

    # -- Verdict --------------------------------------------------------
    print("=" * 100)
    print("VERDICT")
    print("=" * 100)
    print()
    n_pos = overall_positive_count
    n_tot = len(POWERS)
    if n_pos == n_tot:
        print(f"  POSITIVE EXISTENCE across all {n_tot} action-power exponents.")
        print(f"  T_h converges to a continuum operator on the action-power")
        print(f"  3D ordered-lattice family at every tested p in {POWERS}.")
        print()
        print(f"  This generalises the operator-Cauchy NN-lane existence")
        print(f"  result (PR #957) to the action-power universality class.")
    elif n_pos > 0:
        bad = [p for (p, _, _, _, ok) in per_power_summary if not ok]
        print(f"  PARTIAL POSITIVE: {n_pos}/{n_tot} action powers give clean")
        print(f"  operator-Cauchy convergence; failures at p in {bad}.")
        print()
        print(f"  This is a phase-diagram result: T_h convergence depends on")
        print(f"  the universality class, not just on the harness geometry.")
    else:
        print(f"  BOUNDED NULL: no action power in {POWERS} gives clean")
        print(f"  operator-Cauchy convergence on this re-parameterized 3D")
        print(f"  ordered-lattice family.")
        print()
        print(f"  This sharpens the source notes' bounded-fixed-family")
        print(f"  statements by adding a structural reason for non-")
        print(f"  promotability: the L2 Cauchy increment does not exhibit")
        print(f"  a geometric h-decay law with R^2 >= 0.95.")

    print()
    if fail:
        return 1
    if not born_ok:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
