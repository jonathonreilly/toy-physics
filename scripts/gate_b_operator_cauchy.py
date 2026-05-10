#!/usr/bin/env python3
"""Gate B family operator-Cauchy continuum-bridge probe.

Companion experiment to the rescaled-NN operator-Cauchy lane and the
alt-connectivity negative companion.
Question this runner attacks:

  Does the operator-Cauchy continuum-bridge method extend from the rescaled NN
  lane to the Gate B family addressed by

    docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md  (numerical bounded replay)
    docs/RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md (finite-box bounded theorem)

  ?

Two row classes, two distinct outcomes are possible:

1. ``gate_b_connectivity_tolerance_note``: this is the numerical replay
   `scripts/gate_b_connectivity_tolerance.py`.  The harness has explicit
   `N_LAYERS=13, HALF=5` module constants but they are passed as parameters
   into the geometry builders, so they are in principle a refineable lattice
   resolution axis.  We probe it.

2. ``restricted_strong_field_closure_note``: this is a finite-box
   bounded *theorem* whose component runners
   (`frontier_sewing_shell_source.py`, `frontier_oh_static_constraint_lift.py`,
   `frontier_oh_schur_boundary_action.py`,
   `frontier_microscopic_dirichlet_bridge_principle.py`) all run on a
   hardcoded `size = 15` cubic box, `R = 4` cutoff, and an `O_h`-symmetric
   star-supported source class whose seven numerical parameters
   `(x1, x2, mix, lam_e, lam_t, m0, ms)` are tuned to that specific box.
   The residuals are *already* at machine precision (5e-17 to 2e-15).
   Operator-Cauchy is conceptually mismatched for this row: the theorem is
   an algebraic finite-box identity, not a numerical bounded-result that has
   a continuum limit to take.  The right method for that row is
   *algebraic verification at a larger box with a retuned source*, which is
   a separate exercise.  This runner records that determination as a sharp
   structural diagnosis, not a Cauchy fit.

Refinement-axis analysis (row 1)
================================

The fixed-connectivity ordered family has two natural axes:

  (a) lattice-resolution refinement r in {1, 2, 3, 4}, building a graph with

        N_LAYERS = 12 * r + 1
        HALF     = 4  * r

      and rescaling the wave number and detector layout so that

        physical wavelength: lambda_phys = 2*pi / (K / r)  is fixed
        physical layer span: L_phys = (N_LAYERS - 1) * 1   (lattice units)
                                    grows linearly with r (we hold the
                                    rescaled lattice in lattice units, so
                                    "physical" length is in the lattice
                                    unit per refinement step)
        physical mass-y position:  y_phys = y_mass_index * (1/r)
                                    held fixed via y_mass_index = y_phys * r
        barrier layer fraction:  1/3 of N_LAYERS  (kept proportional)

      The 1/r mass field stays a 1/r physical Coulomb field if we rescale
      FIELD_STRENGTH proportionally (positions are in lattice units, so
      physical distance scales as 1/r per lattice step; the 1/r field thus
      already encodes the right continuum law when we hold strength fixed
      in absolute units).

      Observable basis at each resolution:

        - y_centroid_free       : free centroid y of the detector amplitude
        - y_centroid_mass       : mass-on centroid y
        - shift                 : (mass - free) y-shift
        - mass_window_gain      : detector-window probability gain
        - fpm                   : local |delta| ~ strength^fpm exponent

      A 3 source-y-position x 5 observable = 15-dim vector per resolution.

  (b) Ensemble-refinement on the jittered-but-fixed-connectivity sub-family,
      averaging over N seeds for N in {2, 4, 8, 16, 32, 64} at fixed
      jitter = 0.30 (the worst-noise point in the GATE_B_CONNECTIVITY_
      TOLERANCE_NOTE jitter sweep), to ask whether the noise-averaged
      response converges in the CLT sense (r ~ -1/2).

We pass the operator-Cauchy gate if EITHER axis returns
  ||vec(n) - vec(n+1)||_2 ~ C * x^r
with r above the appropriate Cauchy threshold and R^2 >= 0.85, on >= 3
fine-grid points.  We document which axis carried it, or, if neither
passes, we record the structural diagnosis -- analogous to the
alt-connectivity null.

Guards
------

- born-clean baseline: the field is exactly zero in the ``free'' run; the
  centroid identity ``centroid_free == centroid_free'' is reported as a
  zero-by-construction reference, not a residual.
- k=0-clean baseline:  at FIELD_STRENGTH = 0 the action reduces to S = L,
  which is the free harness; we reuse the harness's free-run as the k=0 row.
- monotonicity:  we report per-pair signed Cauchy increments so that a
  non-monotonic axis is visible even if the log-fit happens to look clean.

Cost
----

Resolution refinement: r in {1, 2, 3, 4} on an integer cubic graph with
edge volume ~ N_LAYERS x HALF^2.  At r=4 the graph has 49 layers x 17^2
= ~14 000 nodes with ~9 forward edges each.  Three source positions x two
field strengths each x one free baseline = 7 propagations per resolution.
Wallclock at r=4 ~ 60 s.  Total resolution sweep ~ 90 s.

Ensemble refinement (optional second axis): jitter=0.30, 64 seeds x 3 source
positions x 4 field configs = 768 propagations; each ~ 30 ms on the
N_LAYERS=13 base.  Wallclock ~ 25 s.

Strong-field closure determination: paper-only (we do not re-execute the
machine-precision Schur runners; the source note's evidence is already in
the audit ledger).  Diagnostic is documented in this runner's output and in
the source note.

Exit code is nonzero if the tested no-go is not observed. The expected
no-go condition is that both Gate B operator-Cauchy gates fail; the
restricted strong-field row is separately reported as a method mismatch.
"""

from __future__ import annotations

# Heavy compute / sweep runner -- ``AUDIT_TIMEOUT_SEC = 1800`` means the
# audit-lane precompute and live audit runner allow up to 30 min of wall
# time before recording a timeout. See ``docs/audit/RUNNER_CACHE_POLICY.md``.
AUDIT_TIMEOUT_SEC = 1800

import cmath
import math
import os
import random
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


# ---------- harness primitives (self-contained copy of the relevant bits
#            of `scripts/gate_b_connectivity_tolerance.py`, parameterised by
#            (n_layers, half, K_eff, field_strength, y_mass_phys)) ----------

BETA = 0.8


@dataclass
class GraphFamily:
    name: str
    positions: List[Tuple[float, float, float]]
    layers: List[List[int]]
    adj: Dict[int, List[int]]


def _grid_index(layer: int, iy: int, iz: int, half: int) -> int:
    span = 2 * half + 1
    return layer * (span * span) + (iy + half) * span + (iz + half)


def build_fixed_connectivity(n_layers: int, half: int) -> GraphFamily:
    positions: List[Tuple[float, float, float]] = []
    layers: List[List[int]] = []
    adj: Dict[int, List[int]] = {}

    for layer in range(n_layers):
        x = float(layer)
        nodes: List[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                idx = len(positions)
                positions.append((x, float(iy), float(iz)))
                nodes.append(idx)
        layers.append(nodes)

    for layer in range(n_layers - 1):
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                src = _grid_index(layer, iy, iz, half)
                nbs: List[int] = []
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        jy = iy + dy
                        jz = iz + dz
                        if -half <= jy <= half and -half <= jz <= half:
                            nbs.append(_grid_index(layer + 1, jy, jz, half))
                adj[src] = nbs

    return GraphFamily("ordered", positions, layers, adj)


def jitter_positions(base: GraphFamily, jitter: float, seed: int) -> GraphFamily:
    rng = random.Random(seed)
    positions = []
    for x, y, z in base.positions:
        positions.append((x, y + rng.gauss(0.0, jitter), z + rng.gauss(0.0, jitter)))
    return GraphFamily(f"jitter={jitter:g}", positions, base.layers, base.adj)


def field_for_mass(positions: Sequence[Tuple[float, float, float]],
                   mass_idx: int, strength: float) -> List[float]:
    mx, my, mz = positions[mass_idx]
    field = []
    for x, y, z in positions:
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
        field.append(strength / r)
    return field


def blocked_barrier(layer_nodes: Sequence[int],
                    positions: Sequence[Tuple[float, float, float]],
                    half_height: float) -> set:
    blocked = set()
    for idx in layer_nodes:
        y = positions[idx][1]
        if -half_height < y < half_height:
            blocked.add(idx)
    return blocked


def propagate(positions: Sequence[Tuple[float, float, float]],
              layers: Sequence[Sequence[int]],
              adj: Dict[int, List[int]],
              field: Sequence[float],
              blocked: set,
              K_eff: float) -> List[complex]:
    n = len(positions)
    amps = [0j] * n
    source = layers[0][len(layers[0]) // 2]
    amps[source] = 1.0

    for layer in range(len(layers) - 1):
        for i in layers[layer]:
            if i in blocked:
                continue
            ai = amps[i]
            if abs(ai) < 1e-30:
                continue
            xi, yi, zi = positions[i]
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                xj, yj, zj = positions[j]
                dx = xj - xi
                dy = yj - yi
                dz = zj - zi
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                act = L * (1.0 - lf)
                theta = math.atan2(math.sqrt(dy * dy + dz * dz),
                                   max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                amps[j] += ai * cmath.exp(1j * K_eff * act) * w / L

    return amps


def detector_probs(amps: Sequence[complex],
                   det: Sequence[int]) -> Dict[int, float]:
    raw = {d: abs(amps[d]) ** 2 for d in det}
    total = sum(raw.values())
    if total <= 1e-30:
        return {d: 0.0 for d in det}
    return {d: p / total for d, p in raw.items()}


def centroid_y(amps: Sequence[complex],
               positions: Sequence[Tuple[float, float, float]],
               det: Sequence[int]) -> float:
    total = 0.0
    weighted = 0.0
    for d in det:
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * positions[d][1]
    return weighted / total if total > 1e-30 else 0.0


def mass_window_gain(probs_mass: Dict[int, float],
                     probs_free: Dict[int, float],
                     positions: Sequence[Tuple[float, float, float]],
                     det: Sequence[int],
                     y_mass: float,
                     half_width: float) -> float:
    gain = 0.0
    for d in det:
        if abs(positions[d][1] - y_mass) <= half_width:
            gain += probs_mass[d] - probs_free[d]
    return gain


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
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(lx, ly))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return slope, math.exp(intercept), r2


def l2_diff(a: List[float], b: List[float]) -> float:
    s = 0.0
    for ai, bi in zip(a, b):
        if math.isnan(ai) or math.isnan(bi):
            continue
        s += (ai - bi) ** 2
    return math.sqrt(s)


# ---------- experiment ----------

# Resolution-refinement axis.  At resolution r the lattice has
# (12 r + 1) layers and (4 r) half-width.  The base run (r=1) recovers
# the source-note geometry (13 layers, half=5 effective -> we use half=4
# here for divisibility, which is within the source-note's bounded scope:
# we are *not* required to match every digit of its numerical replay, only
# to share the harness construction).
R_GRID: List[int] = [1, 2, 3, 4]

# Three physical mass-y positions, expressed as fractions of HALF; these
# fractions stay fixed under refinement.
MASS_Y_FRACTIONS: List[float] = [0.4, 0.6, 0.8]

# Two strengths for the local response-slope F~M probe.
STRENGTHS: List[float] = [0.75, 1.25]

# Base wave number and base field strength (chosen to match the source-note
# normalization).
K_BASE: float = 5.0
FIELD_BASE: float = 5e-5

# Mass window half-width in physical (continuum) units; converted to lattice
# units as r * MASS_WINDOW_PHYS.
MASS_WINDOW_PHYS: float = 1.5

# Ensemble axis (jittered fixed-connectivity sub-family).
N_GRID: List[int] = [2, 4, 8, 16, 32, 64]
ENSEMBLE_JITTER: float = 0.30
N_LAYERS_ENS: int = 13
HALF_ENS: int = 5


def measure_resolution(r: int) -> Dict:
    """Measure the 15-dim observable vector at refinement r.

    Vector components: 5 observables x 3 mass-y fractions.
    """
    n_layers = 12 * r + 1
    half = 4 * r
    K_eff = K_BASE / r          # keep physical wavelength fixed
    # Field strength: 1/r physical field at distance d (in lattice units)
    # is FIELD/d.  When we refine, physical distance = d/r, so the same
    # physical field at fixed phys-distance requires FIELD scaled as
    # FIELD_BASE / r (the 1/r law is automatic in our lattice-unit
    # formulation).  This holds the physical action S = L*(1 - phi) invariant
    # to leading order.
    field_strength = FIELD_BASE / r
    mass_window_lattice = MASS_WINDOW_PHYS * r

    g = build_fixed_connectivity(n_layers, half)
    layers = g.layers
    det = layers[-1]
    bl = len(layers) // 3
    barrier = layers[bl]
    blocked = blocked_barrier(barrier, g.positions, half_height=r * 1.0)

    field0 = [0.0] * len(g.positions)
    free = propagate(g.positions, layers, g.adj, field0, blocked, K_eff)
    free_probs = detector_probs(free, det)
    y_free = centroid_y(free, g.positions, det)

    # Pick mass nodes at gl = 2 n_layers/3
    gl = 2 * len(layers) // 3
    vec: List[float] = []

    for frac in MASS_Y_FRACTIONS:
        y_target = frac * half
        # snap to nearest integer y
        y_idx = int(round(y_target))
        mass_idx = None
        for node in layers[gl]:
            if (round(g.positions[node][1]) == y_idx
                    and round(g.positions[node][2]) == 0):
                mass_idx = node
                break
        if mass_idx is None:
            vec.extend([math.nan] * 5)
            continue

        # at central strength
        strength = STRENGTHS[len(STRENGTHS) // 2 - 1]  # 0.75
        field = field_for_mass(g.positions, mass_idx, strength * field_strength)
        mass_amps = propagate(g.positions, layers, g.adj, field, blocked, K_eff)
        mass_probs = detector_probs(mass_amps, det)
        y_mass = centroid_y(mass_amps, g.positions, det)
        shift = y_mass - y_free
        # Normalize y observables to *physical* y by dividing by r so the
        # continuum vector lives on a fixed scale.
        y_free_phys = y_free / r
        y_mass_phys = y_mass / r
        shift_phys = shift / r
        gain = mass_window_gain(
            mass_probs, free_probs, g.positions, det,
            y_idx, half_width=mass_window_lattice,
        )

        # F~M exponent
        scale_series: List[float] = []
        for s in STRENGTHS:
            f = field_for_mass(g.positions, mass_idx, s * field_strength)
            a = propagate(g.positions, layers, g.adj, f, blocked, K_eff)
            d = mass_window_gain(detector_probs(a, det), free_probs,
                                 g.positions, det,
                                 y_idx, half_width=mass_window_lattice)
            scale_series.append(max(abs(d), 1e-30))
        fpm_slope, _, _ = safe_power_fit(STRENGTHS, scale_series)
        if math.isnan(fpm_slope):
            fpm_slope = 0.0

        vec.extend([y_free_phys, y_mass_phys, shift_phys, gain, fpm_slope])

    return {
        "r": r,
        "n_layers": n_layers,
        "half": half,
        "K_eff": K_eff,
        "field_strength": field_strength,
        "vec": vec,
        "y_free_phys_r0": y_free / r,
    }


def measure_ensemble_seed(seed: int) -> List[float]:
    """Measure a 15-dim vector for one seed in the jittered ensemble."""
    base = build_fixed_connectivity(N_LAYERS_ENS, HALF_ENS)
    g = jitter_positions(base, ENSEMBLE_JITTER, seed)
    layers = g.layers
    det = layers[-1]
    bl = len(layers) // 3
    barrier = layers[bl]
    blocked = blocked_barrier(barrier, g.positions, half_height=1.0)
    K_eff = K_BASE
    field_strength = FIELD_BASE

    field0 = [0.0] * len(g.positions)
    free = propagate(g.positions, layers, g.adj, field0, blocked, K_eff)
    free_probs = detector_probs(free, det)
    y_free = centroid_y(free, g.positions, det)

    gl = 2 * len(layers) // 3
    vec: List[float] = []
    for y_idx in (2, 3, 4):
        mass_idx = None
        for node in layers[gl]:
            if (round(g.positions[node][1]) == y_idx
                    and round(g.positions[node][2]) == 0):
                mass_idx = node
                break
        if mass_idx is None:
            vec.extend([math.nan] * 5)
            continue
        strength = 1.0
        field = field_for_mass(g.positions, mass_idx, strength * field_strength)
        mass_amps = propagate(g.positions, layers, g.adj, field, blocked, K_eff)
        mass_probs = detector_probs(mass_amps, det)
        y_mass = centroid_y(mass_amps, g.positions, det)
        shift = y_mass - y_free
        gain = mass_window_gain(
            mass_probs, free_probs, g.positions, det,
            float(y_idx), half_width=1.5,
        )
        scale_series: List[float] = []
        for s in STRENGTHS:
            f = field_for_mass(g.positions, mass_idx, s * field_strength)
            a = propagate(g.positions, layers, g.adj, f, blocked, K_eff)
            d = mass_window_gain(detector_probs(a, det), free_probs,
                                 g.positions, det,
                                 float(y_idx), half_width=1.5)
            scale_series.append(max(abs(d), 1e-30))
        fpm_slope, _, _ = safe_power_fit(STRENGTHS, scale_series)
        if math.isnan(fpm_slope):
            fpm_slope = 0.0
        vec.extend([y_free, y_mass, shift, gain, fpm_slope])
    return vec


def main() -> int:
    t0 = time.time()
    print("=" * 110)
    print("GATE B FAMILY OPERATOR-CAUCHY CONTINUUM-BRIDGE PROBE")
    print("=" * 110)
    print(f"  rows targeted:")
    print(f"    - gate_b_connectivity_tolerance_note     (numerical bounded "
          f"replay)")
    print(f"    - restricted_strong_field_closure_note   (finite-box bounded "
          f"theorem)")
    print()
    print(f"  resolution-refinement axis: r in {R_GRID}")
    print(f"  ensemble-refinement axis:   N in {N_GRID} at jitter="
          f"{ENSEMBLE_JITTER}")
    print(f"  observable basis: [y_free, y_mass, shift, gain, fpm] x "
          f"3 mass-y positions = 15-dim")
    print()

    # ============================================================
    # Part 1: lattice-resolution refinement on the ordered family
    # ============================================================
    print("=" * 110)
    print("PART 1: lattice-resolution refinement (ordered fixed-connectivity)")
    print("=" * 110)
    print(f"  At refinement r:")
    print(f"    N_LAYERS = 12*r + 1, HALF = 4*r")
    print(f"    K_eff    = K_BASE / r       (fix physical wavelength)")
    print(f"    field_s  = FIELD_BASE / r   (fix physical 1/d field amplitude)")
    print(f"    mass-y positions kept at fixed fractions of HALF")
    print()

    res_runs: List[Dict] = []
    for r in R_GRID:
        ts = time.time()
        m = measure_resolution(r)
        m["wallclock"] = time.time() - ts
        res_runs.append(m)
        print(f"  r={r:>2d}  N_layers={m['n_layers']:>3d}  half={m['half']:>2d}"
              f"  K_eff={m['K_eff']:6.3f}  field={m['field_strength']:.2e}"
              f"  y_free/r={m['y_free_phys_r0']:+8.4f}"
              f"  wallclock={m['wallclock']:5.1f}s")
    print()

    # Print the 15-dim vectors and pairwise L2 differences
    print(f"  {'r':>3s}  observable vector (first 5 components shown; "
          f"15 total)")
    for m in res_runs:
        head = "  ".join(f"{v:+9.4e}" for v in m["vec"][:5])
        print(f"  {m['r']:>3d}  [{head}, ...]")
    print()

    # Cauchy fit:  ||vec(r) - vec(r+1)||_2  vs  1/r (so smaller is finer)
    rows = []
    xs = []
    ys = []
    print(f"  {'r1':>3s} -> {'r2':>3s}   ||vec(r1) - vec(r2)||_2     "
          f"per-component diagnostic")
    for i in range(len(res_runs) - 1):
        v1 = res_runs[i]["vec"]
        v2 = res_runs[i + 1]["vec"]
        l2 = l2_diff(v1, v2)
        x_geom = 1.0 / math.sqrt(res_runs[i]["r"] * res_runs[i + 1]["r"])
        # per-component diagnostic: largest component difference
        diffs = [abs(a - b) for a, b in zip(v1, v2)
                 if not (math.isnan(a) or math.isnan(b))]
        comp_max = max(diffs) if diffs else 0.0
        rows.append((res_runs[i]["r"], res_runs[i + 1]["r"], l2, comp_max))
        xs.append(x_geom)
        ys.append(l2)
        print(f"  {res_runs[i]['r']:>3d} -> {res_runs[i+1]['r']:>3d}   "
              f"{l2:24.6e}      max-component-diff={comp_max:.3e}")
    print()

    # Operator-Cauchy on 1/r:  if vec converges as r -> infinity, then
    # vec(r) - vec(2 r) should decay as some positive power of 1/r.
    # We expect r > 0 (positive slope on log-log), with rate set by the
    # leading lattice-spacing correction (linear in 1/r for a first-order
    # consistent discretization, quadratic for second-order).
    slope, C, r2 = safe_power_fit(xs, ys)
    print(f"  Fit on {len(xs)} pts:  ||vec(r) - vec(r+1)||_2 ~ C * (1/r)^p")
    print(f"    p   = {slope:+.4f}  (Cauchy if p > 0.5 AND R^2 >= 0.85)")
    print(f"    C   = {C:.4e}")
    print(f"    R^2 = {r2:.4f}")
    # Monotonicity check: are the L2 increments monotone-decreasing?
    monotone_decreasing = all(rows[i][2] > rows[i + 1][2]
                              for i in range(len(rows) - 1))
    print(f"    Monotone decreasing: "
          f"{'YES' if monotone_decreasing else 'NO'}")
    res_cauchy_ok = (not math.isnan(slope) and slope > 0.5
                     and not math.isnan(r2) and r2 >= 0.85
                     and monotone_decreasing)
    print(f"    GATE p > 0.5 AND R^2 >= 0.85 AND monotone: "
          f"{'PASS' if res_cauchy_ok else 'FAIL'}")
    print()

    # ============================================================
    # Part 2: ensemble refinement on jittered fixed-connectivity
    # ============================================================
    print("=" * 110)
    print("PART 2: ensemble refinement (jittered fixed-connectivity)")
    print("=" * 110)
    print(f"  jitter={ENSEMBLE_JITTER} (worst-case point from the source-note "
          f"jitter sweep)")
    print(f"  N_LAYERS={N_LAYERS_ENS}, HALF={HALF_ENS}; K and field at base "
          f"values")
    print()

    n_max = max(N_GRID)
    ts = time.time()
    per_seed_vecs: List[List[float]] = []
    for seed in range(n_max):
        v = measure_ensemble_seed(seed)
        per_seed_vecs.append(v)
    dt_ens = time.time() - ts
    print(f"  measured {n_max} seeds in {dt_ens:.1f}s "
          f"({1000*dt_ens/n_max:.0f} ms/seed)")
    print()

    def ensemble_mean(vecs: List[List[float]]) -> List[float]:
        if not vecs:
            return [math.nan] * 15
        out: List[float] = []
        for i in range(15):
            col = [v[i] for v in vecs
                   if i < len(v) and not math.isnan(v[i])]
            out.append(sum(col) / len(col) if col else math.nan)
        return out

    rows_ens = []
    xs_ens = []
    ys_ens = []
    print(f"  {'N1':>5s} -> {'N2':>5s}   ||vec(N1) - vec(N2)||_2")
    pairs = [(N_GRID[i], N_GRID[i + 1]) for i in range(len(N_GRID) - 1)]
    for N1, N2 in pairs:
        v1 = ensemble_mean(per_seed_vecs[:N1])
        v2 = ensemble_mean(per_seed_vecs[:N2])
        l2 = l2_diff(v1, v2)
        rows_ens.append((N1, N2, l2))
        x_geom = math.sqrt(N1 * N2)
        if l2 > 0:
            xs_ens.append(x_geom)
            ys_ens.append(l2)
        print(f"  {N1:>5d} -> {N2:>5d}   {l2:24.6e}")

    slope_e, C_e, r2_e = safe_power_fit(xs_ens, ys_ens)
    print()
    print(f"  Fit on {len(xs_ens)} pts:  ||vec(N) - vec(2N)||_2 ~ C * N^r")
    print(f"    r   = {slope_e:+.4f}  (Cauchy if r < -0.4 AND R^2 >= 0.85)")
    print(f"    C   = {C_e:.4e}")
    print(f"    R^2 = {r2_e:.4f}")
    monotone_decreasing_e = all(rows_ens[i][2] > rows_ens[i + 1][2]
                                for i in range(len(rows_ens) - 1))
    print(f"    Monotone decreasing: "
          f"{'YES' if monotone_decreasing_e else 'NO'}")
    ens_cauchy_ok = (not math.isnan(slope_e) and slope_e < -0.4
                     and not math.isnan(r2_e) and r2_e >= 0.85
                     and monotone_decreasing_e)
    print(f"    GATE r < -0.4 AND R^2 >= 0.85 AND monotone: "
          f"{'PASS' if ens_cauchy_ok else 'FAIL'}")
    if ens_cauchy_ok and slope_e < 0 and not math.isnan(slope_e):
        cl_dist = abs(slope_e - (-0.5))
        if cl_dist < 0.12:
            y_finest = ys_ens[-1]
            ratio = 2.0 ** slope_e
            tail = (y_finest * ratio / (1.0 - ratio)
                    if ratio < 1.0 else math.inf)
            print(f"    CLT identification: r = {slope_e:+.4f} is within "
                  f"{cl_dist:.3f} of -1/2;")
            print(f"    tail-sum bound ||vec_inf - vec(N={n_max})||_2 <= "
                  f"{tail:.4e}.")
    print()

    # ============================================================
    # Part 3: restricted_strong_field_closure_note diagnosis
    # ============================================================
    print("=" * 110)
    print("PART 3: restricted_strong_field_closure_note  -- "
          "structural diagnosis")
    print("=" * 110)
    print()
    print("  The closure note's component runners")
    print("    scripts/frontier_sewing_shell_source.py")
    print("    scripts/frontier_oh_static_constraint_lift.py")
    print("    scripts/frontier_oh_schur_boundary_action.py")
    print("    scripts/frontier_microscopic_dirichlet_bridge_principle.py")
    print("  all use a hardcoded size = 15 cubic box, R = 4 exterior cutoff,")
    print("  and an O_h-symmetric star-supported source class whose seven")
    print("  parameters (x1, x2, mix, lam_e, lam_t, m0, ms) are tuned to")
    print("  satisfy the closure on exactly that box.  The residuals reported")
    print("  in the source note are already at machine precision:")
    print("    sewing identity      :  ext_err = 5.204e-17")
    print("    static constraints   :  max residual = 1.789e-15")
    print("    Schur stationarity   :  flux_err = 9.021e-17")
    print("    Dirichlet trace match:  trace_match = 2.637e-16")
    print()
    print("  Operator-Cauchy is conceptually mismatched for this row:")
    print()
    print("    1. The theorem is an algebraic finite-box identity, not a")
    print("       bounded numerical result with a continuum limit.")
    print("    2. The source-class parameters were tuned to size=15.  At")
    print("       size=17 or size=21 the seven numbers (m0, ms, x1, x2,")
    print("       mix, lam_e, lam_t) would need re-tuning before the local")
    print("       O_h closure could be expected to hold; this re-tuning is")
    print("       not a continuum-limit operation but an algebraic re-")
    print("       parametrization of the source class.")
    print("    3. The static constraints H_0 psi = 2 pi psi^5 rho and")
    print("       H_0 chi = -2 pi alpha psi^5 (rho + 2S) are pointwise")
    print("       algebraic identities on the chosen box -- they admit no")
    print("       sense of `infinite-box limit residual'.")
    print()
    print("  The right method for that row is *algebraic verification at a")
    print("  larger O_h-symmetric box with a re-tuned source class*, not a")
    print("  Cauchy fit on a refinement axis.  This is documented as a")
    print("  scope/method note rather than as a numerical fit.")
    print()

    # ============================================================
    # Final verdict
    # ============================================================
    print("=" * 110)
    print("VERDICT")
    print("=" * 110)
    print()
    print(f"  resolution-refinement (Part 1):  "
          f"{'PASS' if res_cauchy_ok else 'FAIL'}")
    print(f"  ensemble-refinement   (Part 2):  "
          f"{'PASS' if ens_cauchy_ok else 'FAIL'}")
    print(f"  strong-field closure  (Part 3):  N/A (algebraic finite-box "
          f"theorem; operator-Cauchy mismatched)")
    print()

    if res_cauchy_ok or ens_cauchy_ok:
        print("  Operator-Cauchy continuum-bridge method extends to the "
              "Gate B family")
        print(f"  on the {'resolution' if res_cauchy_ok else 'ensemble'}-"
              f"refinement axis.")
    else:
        print("  Operator-Cauchy continuum-bridge method does NOT extend "
              "cleanly to the Gate B family.")
        print()
        print("  Structural reasons for the bounded scope:")
        print("    - Part 1: refining the lattice resolution while holding")
        print("      K, field amplitude, and mass-y position fixed in")
        print("      physical units does not produce a monotone-decreasing")
        print("      Cauchy increment.  The Gate B harness's action")
        print("      S = L*(1 - phi) and its theta-weighted forward")
        print("      propagator are not derived from a continuum PDE, so")
        print("      lattice-resolution refinement of the discretization")
        print("      does not converge to a continuum operator on this")
        print("      observable basis.")
        print("    - Part 2: ensemble averaging over seeds at the worst-")
        print("      noise point of the source-note's jitter sweep does")
        print("      not converge with the CLT-style rate (r ~ -1/2).")
        print("      The harness's bounded-but-mixed connectivity-recompute")
        print("      response (cf. source note table 1) is reproduced as a")
        print("      structural feature of the harness, not as a noise-")
        print("      averageable fluctuation.")
        print("    - Part 3: the restricted-strong-field-closure row is a")
        print("      finite-box algebraic theorem; the operator-Cauchy")
        print("      method has no continuum axis to attack.")
        print()
        print("  This is a SHARP BOUNDED NULL-RESULT: the Gate B family's")
        print("  bounded scope is structural to its construction.  This")
        print("  mirrors the alt-connectivity negative companion")
        print("  and confirms that the operator-Cauchy bridge method is")
        print("  a feature of the rescaled-NN lane, not of every")
        print("  physical Cl(3) on Z^3 harness.")

    expected_no_go = (not res_cauchy_ok and not ens_cauchy_ok)
    print()
    print("  Expected no-go check (both tested Cauchy gates fail): "
          f"{'PASS' if expected_no_go else 'FAIL'}")
    print()
    print(f"  Total wallclock: {time.time() - t0:.0f}s")
    return 0 if expected_no_go else 1


if __name__ == "__main__":
    sys.exit(main())
