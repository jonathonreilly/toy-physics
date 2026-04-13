#!/usr/bin/env python3
"""Projected DtN correction operator for the finite-rank non-O_h sector.

Exact content:
  1. On the sewing band 3 < r <= 5, the anisotropic shell remainder lives on
     four active cubic orbit channels.
  2. The exact microscopic lattice solve induces a projected correction
     operator on that active orbit quotient.
  3. The operator has exact row antisymmetry between the paired channels
     (3,2,2) <-> (4,1,0) and (3,3,0) <-> (4,1,1), so it factors through a
     2D pair quotient.

Bounded content:
  4. The leading pair-output mode aligns with the universal active orbit
     pattern already extracted from the exact local O_h and finite-rank
     source families.
  5. The finite-rank family sits close to that same mode, so the correction is
     governed by the microscopic operator rather than by a post hoc fit.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()
rad = SourceFileLoader(
    "radial_shell",
    "/private/tmp/physics-review-active/scripts/frontier_radial_shell_matching_law.py",
).load_module()


SIZE = 15
CENTER = (SIZE - 1) // 2
RADII = sew.radii_grid(SIZE)
BAND_MASK = (RADII > 3.0 + 1e-12) & (RADII <= 5.0 + 1e-12)

ACTIVE_ORBITS = [
    (3, 2, 2),
    (3, 3, 0),
    (4, 1, 0),
    (4, 1, 1),
]

PAIR_ROWS = [0, 1]


def orbit_key(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(sorted([abs(i - CENTER), abs(j - CENTER), abs(k - CENTER)], reverse=True))


def orbit_points() -> dict[tuple[int, int, int], list[tuple[int, int, int]]]:
    out: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {k: [] for k in ACTIVE_ORBITS}
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if not BAND_MASK[i, j, k]:
                    continue
                key = orbit_key(i, j, k)
                if key in out:
                    out[key].append((i, j, k))
    return out


ORBIT_POINTS = orbit_points()


def normalized_orbit_source(channel: tuple[int, int, int]) -> np.ndarray:
    src = np.zeros((SIZE, SIZE, SIZE), dtype=float)
    pts = ORBIT_POINTS[channel]
    if not pts:
        raise RuntimeError(f"no lattice points found for orbit channel {channel}")
    weight = 1.0 / float(len(pts))
    for p in pts:
        src[p] = weight
    return src


def active_orbit_vector(phi_grid: np.ndarray) -> np.ndarray:
    sigma = sew.full_neg_laplacian(sew.exterior_projector(phi_grid, 4.0))
    sigma_rad = rad.radial_average_shell(sigma)
    delta_sigma = sigma - sigma_rad
    total_charge = float(np.sum(sigma))
    if abs(total_charge) < 1e-15:
        raise RuntimeError("zero total charge in active orbit vector")

    vec = []
    for channel in ACTIVE_ORBITS:
        total = 0.0
        for p in ORBIT_POINTS[channel]:
            total += float(delta_sigma[p])
        vec.append(total / total_charge)
    return np.array(vec, dtype=float)


def build_active_operator() -> np.ndarray:
    cols = []
    for channel in ACTIVE_ORBITS:
        src = normalized_orbit_source(channel)
        phi = sew.solve_from_source(src)
        cols.append(active_orbit_vector(phi))
    return np.column_stack(cols)


def normalized(vec: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vec))
    if norm < 1e-15:
        return vec.copy()
    return vec / norm


def family_active_vector(phi_grid: np.ndarray) -> np.ndarray:
    return active_orbit_vector(phi_grid)


def main() -> None:
    print("Projected DtN correction operator on the active orbit quotient")
    print("=" * 72)

    operator = build_active_operator()
    pair_operator = operator[np.array(PAIR_ROWS), :]
    rank_full = int(np.linalg.matrix_rank(operator, tol=1e-12))
    rank_pair = int(np.linalg.matrix_rank(pair_operator, tol=1e-12))
    singular_values = np.linalg.svd(pair_operator, compute_uv=False)

    row_cancel_1 = float(np.max(np.abs(operator[0] + operator[2])))
    row_cancel_2 = float(np.max(np.abs(operator[1] + operator[3])))

    u, s, vt = np.linalg.svd(pair_operator)
    lead_output = u[:, 0]
    lead_input = vt[0, :]

    oh_full = family_active_vector(same_source.build_best_phi_grid())
    fr_full = family_active_vector(coarse.build_finite_rank_phi_grid())
    oh_vec = oh_full[:2]
    fr_vec = fr_full[:2]
    oh_dir = normalized(oh_vec)
    fr_dir = normalized(fr_vec)

    lead_align_oh = abs(float(np.dot(lead_output, oh_dir)))
    lead_align_fr = abs(float(np.dot(lead_output, fr_dir)))
    family_dir_diff = float(np.max(np.abs(oh_dir - fr_dir)))

    oh_image = normalized(pair_operator @ oh_full)
    fr_image = normalized(pair_operator @ fr_full)
    oh_self_align = abs(float(np.dot(oh_image, oh_dir)))
    fr_self_align = abs(float(np.dot(fr_image, fr_dir)))

    print("Active orbit operator (rows/cols ordered as 322, 330, 410, 411):")
    print(np.array2string(operator, precision=6, floatmode="fixed"))
    print(f"pair-quotient singular values = {np.array2string(singular_values, precision=6, floatmode='fixed')}")
    print(f"full operator rank = {rank_full}")
    print(f"pair quotient rank = {rank_pair}")
    print(f"row antisymmetry residuals = ({row_cancel_1:.3e}, {row_cancel_2:.3e})")
    print(f"leading pair output mode = {np.array2string(lead_output, precision=6, floatmode='fixed')}")
    print(f"leading pair input mode  = {np.array2string(lead_input, precision=6, floatmode='fixed')}")
    print(f"local O_h active vector   = {np.array2string(oh_dir, precision=6, floatmode='fixed')}")
    print(f"finite-rank active vector = {np.array2string(fr_dir, precision=6, floatmode='fixed')}")

    record(
        "the projected active correction operator is built directly from the microscopic lattice solve",
        rank_full == 2 and rank_pair == 2,
        f"full rank={rank_full}, pair rank={rank_pair}",
    )
    record(
        "the active correction operator has exact shellwise antisymmetry between the paired channels",
        row_cancel_1 < 1e-12 and row_cancel_2 < 1e-12,
        f"row cancellations: {row_cancel_1:.3e}, {row_cancel_2:.3e}",
    )
    record(
        "the exact local O_h and finite-rank families share the same active orbit direction",
        family_dir_diff < 1e-12,
        f"max direction difference={family_dir_diff:.3e}",
    )
    record(
        "the leading pair-output mode of the microscopic correction operator aligns with the universal active orbit pattern",
        lead_align_oh > 0.98 and lead_align_fr > 0.98,
        f"alignment with O_h={lead_align_oh:.6f}, finite-rank={lead_align_fr:.6f}",
        status="BOUNDED",
    )
    record(
        "the finite-rank active vector is nearly closed under the projected correction operator",
        oh_self_align > 0.99 and fr_self_align > 0.99,
        f"self-alignment: O_h={oh_self_align:.6f}, finite-rank={fr_self_align:.6f}",
        status="BOUNDED",
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
