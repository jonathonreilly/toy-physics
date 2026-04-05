#!/usr/bin/env python3
"""Cheap phase-diagram scout for graph perturbations on the retained 3D family.

Goal:
  Compare a few bounded graph perturbation families and identify which
  observable fails first under graph damage:
    - sign
    - Born
    - exponent fidelity

This is intentionally narrow. It reuses the retained 3D valley-linear graph
geometry and only scans a small perturbation set:
  - baseline
  - asymmetric z>0 edge removal
  - transverse jitter
  - sparse NN-only connectivity
  - a short edge-deletion ladder

The output is a bounded phase-diagram note, not a universal graph theorem.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this harness. On this machine use /usr/bin/python3."
    ) from exc

from scripts.inverse_problem_graph_requirements import (  # noqa: E402
    GraphLattice3D,
    VariantSpec,
    K,
    MASS_Z,
    PHYS_L,
    PHYS_W,
    STRENGTH,
    H,
    born_ratio,
    gravity_delta,
    make_field,
    slit_sets,
)


SOURCE_ZS = tuple(range(2, 9))
MASS_STRENGTHS = (1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5)
BORN_TOL = 1e-12
ALPHA_TOL = 0.05


@dataclass(frozen=True)
class ScoutSpec:
    name: str
    variant: VariantSpec
    label: str


@dataclass
class ScoutRow:
    name: str
    label: str
    born: float
    grav_z3: float
    grav_sign: str
    toward_count: int
    toward_total: int
    fm_alpha: float
    born_ok: bool
    sign_ok: bool
    alpha_ok: bool
    first_fail: str


def fit_power(x_data: list[float], y_data: list[float]) -> tuple[float | None, float | None]:
    if len(x_data) < 3:
        return None, None
    x = np.asarray(x_data, dtype=float)
    y = np.asarray(y_data, dtype=float)
    if np.any(x <= 0) or np.any(y <= 0):
        return None, None
    lx = np.log(x)
    ly = np.log(y)
    mx = float(lx.mean())
    my = float(ly.mean())
    sxx = float(np.sum((lx - mx) ** 2))
    if sxx < 1e-12:
        return None, None
    sxy = float(np.sum((lx - mx) * (ly - my)))
    slope = sxy / sxx
    ss_res = float(np.sum((ly - (my + slope * (lx - mx))) ** 2))
    ss_tot = float(np.sum((ly - my) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def source_sign_count(lat: GraphLattice3D) -> tuple[int, int]:
    """Count how many probe positions stay TOWARD on the retained source ladder."""
    toward = 0
    for z_mass in SOURCE_ZS:
        delta = gravity_delta(
            lat,
            make_field(lat, z_mass, STRENGTH),
            K,
        )
        if delta > 0:
            toward += 1
    return toward, len(SOURCE_ZS)


def measure_alpha(lat: GraphLattice3D) -> float:
    """Estimate F~M exponent on the same perturbed graph."""
    _, _, _, blocked = slit_sets(lat)
    deltas: list[float] = []
    strengths: list[float] = []
    free = lat.propagate(np.zeros(lat.n, dtype=float), K, blocked)
    det = lat.detector_indices()
    z_free = sum(abs(free[d]) ** 2 * lat.pos[d, 2] for d in det) / max(
        sum(abs(free[d]) ** 2 for d in det), 1e-30
    )
    for strength in MASS_STRENGTHS:
        amps = lat.propagate(make_field(lat, MASS_Z, strength), K, blocked)
        pm = sum(abs(amps[d]) ** 2 for d in det)
        if pm <= 1e-30:
            continue
        z_mass = sum(abs(amps[d]) ** 2 * lat.pos[d, 2] for d in det) / pm
        delta = z_mass - z_free
        if delta > 0:
            strengths.append(strength)
            deltas.append(delta)
    slope, _ = fit_power(strengths, deltas)
    return float("nan") if slope is None else float(slope)


def measure(spec: ScoutSpec) -> ScoutRow:
    lat = GraphLattice3D(
        PHYS_L,
        PHYS_W,
        H,
        spec.variant.max_d_phys,
        jitter=spec.variant.jitter,
        edge_delete_prob=spec.variant.edge_delete_prob,
        asym_zpos_removed=spec.variant.asym_zpos_removed,
    )
    born = born_ratio(lat)
    field = make_field(lat, MASS_Z, STRENGTH)
    grav_z3 = gravity_delta(lat, field, K)
    grav_sign = "TOWARD" if grav_z3 > 0 else "AWAY" if grav_z3 < 0 else "ZERO"
    toward_count, toward_total = source_sign_count(lat)
    fm_alpha = measure_alpha(lat)

    born_ok = bool(np.isfinite(born) and born <= BORN_TOL)
    sign_ok = grav_z3 > 0 and toward_count == toward_total
    alpha_ok = bool(np.isfinite(fm_alpha) and abs(fm_alpha - 1.0) <= ALPHA_TOL)

    if not sign_ok:
        first_fail = "sign"
    elif not born_ok:
        first_fail = "Born"
    elif not alpha_ok:
        first_fail = "exponent"
    else:
        first_fail = "none"

    return ScoutRow(
        name=spec.name,
        label=spec.label,
        born=born,
        grav_z3=grav_z3,
        grav_sign=grav_sign,
        toward_count=toward_count,
        toward_total=toward_total,
        fm_alpha=fm_alpha,
        born_ok=born_ok,
        sign_ok=sign_ok,
        alpha_ok=alpha_ok,
        first_fail=first_fail,
    )


def fmt_float(x: float) -> str:
    if not np.isfinite(x):
        return "nan"
    return f"{x:+.6f}"


def main() -> None:
    specs = [
        ScoutSpec("baseline", VariantSpec("baseline"), "baseline"),
        ScoutSpec("asym_zpos_removed", VariantSpec("asym_zpos_removed", asym_zpos_removed=True), "asym"),
        ScoutSpec("jitter_0.5h", VariantSpec("jitter_0.5h", jitter=0.5 * H), "jitter"),
        ScoutSpec("sparse_nn_only", VariantSpec("sparse_nn_only", max_d_phys=1), "sparse"),
        ScoutSpec("delete_10", VariantSpec("delete_10", edge_delete_prob=0.10), "edge delete 10%"),
        ScoutSpec("delete_20", VariantSpec("delete_20", edge_delete_prob=0.20), "edge delete 20%"),
        ScoutSpec("delete_30", VariantSpec("delete_30", edge_delete_prob=0.30), "edge delete 30%"),
        ScoutSpec("delete_50", VariantSpec("delete_50", edge_delete_prob=0.50), "edge delete 50%"),
        ScoutSpec("delete_70", VariantSpec("delete_70", edge_delete_prob=0.70), "edge delete 70%"),
    ]

    rows = [measure(spec) for spec in specs]

    print("=" * 96)
    print("GRAPH PHASE-DIAGRAM SCOUT")
    print("  Retained 3D valley-linear family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={GraphLattice3D(PHYS_L, PHYS_W, H, 3).max_d}")
    print(f"  controls: Born, sign, exponent fidelity")
    print(f"  thresholds: Born <= {BORN_TOL:.0e}, |F~M-1| <= {ALPHA_TOL:.2f}")
    print("=" * 96)
    print(
        f"{'family':<18} {'label':<16} {'Born':>10} {'z3':>11} {'sign':>8} "
        f"{'toward':>8} {'F~M':>7} {'Born?':>6} {'Sign?':>6} {'Exp?':>6} {'first':>8}"
    )
    print("-" * 96)
    for row in rows:
        print(
            f"{row.name:<18} {row.label:<16} {row.born:10.2e} {fmt_float(row.grav_z3):>11} "
            f"{row.grav_sign:>8} {row.toward_count:>3d}/{row.toward_total:<3d} "
            f"{row.fm_alpha:7.3f} {('Y' if row.born_ok else 'N'):>6} "
            f"{('Y' if row.sign_ok else 'N'):>6} {('Y' if row.alpha_ok else 'N'):>6} "
            f"{row.first_fail:>8}"
        )

    # Summarize the earliest failure pattern across the bounded families.
    sign_failures = [r.name for r in rows if not r.sign_ok]
    born_failures = [r.name for r in rows if not r.born_ok]
    exp_failures = [r.name for r in rows if not r.alpha_ok]

    print()
    print("SCOUT SUMMARY")
    print(
        "  sign failures: "
        + (", ".join(sign_failures) if sign_failures else "none in this bounded sweep")
    )
    print(
        "  Born failures: "
        + (", ".join(born_failures) if born_failures else "none in this bounded sweep")
    )
    print(
        "  exponent failures: "
        + (", ".join(exp_failures) if exp_failures else "none in this bounded sweep")
    )

    if sign_failures:
        recommendation = (
            "The short scout ladder first fails at sign, but the retained 0.75-1.00 "
            "boundary sweep did not reproduce a flip on the same family. If we keep "
            "pushing this lane, use a harsher damage ladder or a different graph family."
        )
    elif born_failures:
        recommendation = (
            "Next hardening lane: born-sensitive perturbation sweep, because Born is the "
            "first observable to fail in this bounded run."
        )
    elif exp_failures:
        recommendation = (
            "Next hardening lane: exponent-fidelity sweep, because sign and Born survive "
            "this bounded run but F~M drifts first."
        )
    else:
        recommendation = (
            "Next hardening lane: this bounded sweep did not find a failure; widen the "
            "perturbation ladder or move to a new graph family."
        )

    print(f"  recommendation: {recommendation}")


if __name__ == "__main__":
    main()
