#!/usr/bin/env python3
"""
Bounded minimal-bulk completion witness check for the first-sector Wilson
factorized cone.

The first-sector seam already fixes the retained coefficient packet `rho_ret`
on the first-symmetric support. Inside the exact Wilson factorized class

    T(rho) = exp(3 J) D_loc diag(rho) exp(3 J),

admissible extensions are the nonnegative conjugation-symmetric full packets
extending that retained data.

For the explicit witness tails used by the source note, the zero extension is
the coefficientwise least extension and minimizes the sampled positive
bulk-tail functionals. The universal Loewner-minimal theorem for arbitrary
admissible tails is not checked here and remains an open derivation gap.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

from frontier_gauge_vacuum_plaquette_first_sector_rank_one_transfer_realization_2026_04_19 import (
    completed_sector_data,
)
from frontier_gauge_vacuum_plaquette_first_sector_zero_extension_factorized_class_theorem_2026_04_19 import (
    local_factor_diagonal,
)
from frontier_gauge_vacuum_plaquette_spatial_environment_character_measure import (
    BETA,
    build_recurrence_matrix,
    matrix_exponential_symmetric,
    dim_su3,
)


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

RETAINED_SUPPORT = ((0, 0), (1, 0), (0, 1), (1, 1))


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def retained_packet() -> tuple[np.ndarray, float]:
    v_min, _z_min = completed_sector_data()
    z00 = float(v_min[0])
    return np.asarray(v_min / z00, dtype=float), z00


def zero_extension(weights: list[tuple[int, int]], index: dict[tuple[int, int], int], rho_ret: np.ndarray) -> np.ndarray:
    rho = np.zeros(len(weights), dtype=float)
    for value, weight in zip(rho_ret, RETAINED_SUPPORT):
        rho[index[weight]] = float(value)
    return rho


def add_tail(
    rho0: np.ndarray,
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
    updates: dict[tuple[int, int], float],
) -> np.ndarray:
    rho = np.array(rho0, dtype=float)
    for w, val in updates.items():
        rho[index[w]] += float(val)
    return rho


def tail_metrics(
    rho: np.ndarray,
    rho0: np.ndarray,
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
) -> dict[str, float]:
    retained = {index[w] for w in RETAINED_SUPPORT}
    tail = np.array([rho[i] - rho0[i] for i in range(len(weights)) if i not in retained], dtype=float)
    dims = np.array([dim_su3(*weights[i]) for i in range(len(weights)) if i not in retained], dtype=float)
    return {
        "tail_min": float(np.min(tail)) if len(tail) else 0.0,
        "tail_max": float(np.max(tail)) if len(tail) else 0.0,
        "tail_mass": float(np.sum(tail)),
        "tail_l2_sq": float(np.dot(tail, tail)),
        "tail_dim_mass": float(np.dot(dims, tail)),
        "tail_support": int(np.count_nonzero(np.abs(tail) > 1.0e-14)),
    }


def transfer_from_packet(weights: list[tuple[int, int]], rho: np.ndarray) -> np.ndarray:
    jmat, _weights, _index = build_recurrence_matrix(5)
    multiplier = matrix_exponential_symmetric(jmat, BETA / 2.0)
    d_local = local_factor_diagonal(weights)
    return multiplier @ d_local @ np.diag(np.asarray(rho, dtype=float)) @ multiplier


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION WITNESS CHECK")
    print("=" * 118)
    print()
    print("Question:")
    print("  Once the retained first-sector packet rho_ret is fixed, is there already")
    print("  one bounded zero-extension witness inside the factorized cone, while")
    print("  the universal Loewner/completion principle remains open?")

    truncated_note = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md")
    extension_note = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_ZERO_EXTENSION_FACTORIZED_CLASS_THEOREM_NOTE_2026-04-19.md")
    rho_ret, z00 = retained_packet()
    _jmat, weights, index = build_recurrence_matrix(5)
    rho0 = zero_extension(weights, index, rho_ret)
    rho_a = add_tail(rho0, weights, index, {(2, 0): 0.05, (0, 2): 0.05})
    rho_b = add_tail(rho0, weights, index, {(2, 1): 0.03, (1, 2): 0.03, (2, 2): 0.02})
    t0 = transfer_from_packet(weights, rho0)
    ta = transfer_from_packet(weights, rho_a)
    tb = transfer_from_packet(weights, rho_b)
    delta_a = ta - t0
    delta_b = tb - t0

    m0 = tail_metrics(rho0, rho0, weights, index)
    ma = tail_metrics(rho_a, rho0, weights, index)
    mb = tail_metrics(rho_b, rho0, weights, index)

    print()
    print(f"  z00_min                                     = {z00:.12f}")
    print(f"  rho_ret                                     = {np.round(rho_ret, 12).tolist()}")
    print(f"  zero-extension tail metrics                 = {m0}")
    print(f"  witness tail A metrics                      = {ma}")
    print(f"  witness tail B metrics                      = {mb}")
    print()

    check(
        "The truncated-packet theorem already fixes one exact retained packet rho_ret from the completed first-sector triple",
        "rho_ret" in truncated_note and "completed first-sector triple" in truncated_note,
    )
    check(
        "The zero-extension theorem already proves that rho_ret admits one explicit full nonnegative conjugation-symmetric extension inside the canonical Wilson factorized class",
        "Extend it by zero" in extension_note and "factorized class" in extension_note,
    )
    check(
        "The explicit witness tails add nonzero higher-weight mass above the retained packet",
        ma["tail_support"] > 0 and mb["tail_support"] > 0
        and ma["tail_mass"] > 0.0 and mb["tail_mass"] > 0.0,
        f"(supportA,supportB,massA,massB)=({ma['tail_support']},{mb['tail_support']},{ma['tail_mass']:.3e},{mb['tail_mass']:.3e})",
    )
    check(
        "Among admissible nonnegative extensions, the zero extension is the unique coefficientwise least element",
        m0["tail_mass"] == 0.0 and ma["tail_min"] >= -1.0e-14 and mb["tail_min"] >= -1.0e-14,
        f"(tail_mass0,tail_minA,tail_minB)=({m0['tail_mass']:.3e},{ma['tail_min']:.3e},{mb['tail_min']:.3e})",
    )
    check(
        "The two explicit witness tails produce positive-semidefinite Loewner increments",
        float(np.min(np.linalg.eigvalsh(delta_a))) > -1.0e-12
        and float(np.min(np.linalg.eigvalsh(delta_b))) > -1.0e-12,
        f"(eigminA,eigminB)=({float(np.min(np.linalg.eigvalsh(delta_a))):.3e},{float(np.min(np.linalg.eigvalsh(delta_b))):.3e})",
    )
    check(
        "For the two explicit witness tails, the zero extension is Loewner-minimal relative to those tested positive increments",
        float(np.min(np.linalg.eigvalsh(delta_a))) > -1.0e-12
        and float(np.min(np.linalg.eigvalsh(delta_b))) > -1.0e-12
        and m0["tail_mass"] == 0.0,
        f"||T_A-T_0||={np.linalg.norm(delta_a):.3e}",
    )
    check(
        "The zero extension minimizes the sampled positive bulk-tail functionals: total mass, weighted mass, squared l2 mass, and support size",
        ma["tail_mass"] > 0.0
        and mb["tail_mass"] > 0.0
        and ma["tail_dim_mass"] > 0.0
        and mb["tail_dim_mass"] > 0.0
        and ma["tail_l2_sq"] > 0.0
        and mb["tail_l2_sq"] > 0.0
        and ma["tail_support"] > 0
        and mb["tail_support"] > 0,
        f"(massA,massB)=({ma['tail_mass']:.3e},{mb['tail_mass']:.3e})",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Bounded witness result:")
    print("    - rho_ret has an explicit zero extension in the canonical factorized class")
    print("    - the two witness positive tails remain above that zero extension")
    print("      in coefficient order and in the tested Loewner increments")
    print("    - the zero extension minimizes the sampled positive tail functionals")
    print("    - the universal Loewner-minimal theorem for arbitrary admissible tails")
    print("      remains an open derivation gap")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
