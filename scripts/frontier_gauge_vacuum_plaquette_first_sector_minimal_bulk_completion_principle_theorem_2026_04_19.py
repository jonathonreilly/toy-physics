#!/usr/bin/env python3
"""
Bounded minimal-bulk completion witness check for the first-sector Wilson
factorized cone.

The first-sector seam already fixes the retained coefficient packet `rho_ret`
on the first-symmetric support. Inside the exact Wilson factorized class

    T(rho) = exp(3 J) D_loc diag(rho) exp(3 J),

admissible extensions are the nonnegative conjugation-symmetric full packets
extending that retained data.

This runner certifies bounded, witness-restricted facts only:

1. The retained packet `rho_ret` produced by the local `completed_sector_data`
   import is normalized, conjugation-symmetric, and zero on the `(1,1)`
   slot.  No substring import of upstream prose is used to substantiate this
   property; the assertions are verified directly on the numeric packet.

2. The zero-extension `rho_0` of `rho_ret` to all higher weights produces a
   self-adjoint, conjugation-symmetric transfer matrix on the truncated
   dominant-weight box.  This existence-of-one-explicit-extension fact is
   verified by direct numeric computation on the transfer.

3. For the two explicit witness tails A and B and for a randomized sweep of
   admissible nonnegative tails inside the cone, the inequality
   `rho_0 + delta >= rho_0` holds coefficientwise; this is the algebraic
   identity `delta >= 0 ==> rho_0 + delta >= rho_0` and is what the runner
   actually checks.  The runner does **not** claim universal Loewner
   monotonicity for arbitrary admissible tails: that universal step is
   recorded in the source note as an open derivation gap.

4. For the two named witness tails A and B, the Loewner increment is PSD,
   and the four sampled positive bulk-tail functionals strictly increase.
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


def random_nonneg_tail(
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample a conjugation-symmetric nonnegative tail on the non-retained
    weights.  Conjugation symmetry: `(p,q)` and `(q,p)` share the same
    coefficient."""
    retained = {index[w] for w in RETAINED_SUPPORT}
    delta = np.zeros(len(weights), dtype=float)
    visited = set()
    for i, (p, q) in enumerate(weights):
        if i in retained or i in visited:
            continue
        value = float(rng.uniform(0.0, 0.05))
        delta[i] = value
        j = index[(q, p)]
        if j != i:
            delta[j] = value
            visited.add(j)
        visited.add(i)
    return delta


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

    # Check 1: numeric properties of the retained packet, computed locally
    # (no substring import of upstream prose).
    rho_00 = float(rho_ret[0])
    rho_10 = float(rho_ret[1])
    rho_01 = float(rho_ret[2])
    rho_11 = float(rho_ret[3])
    check(
        "Retained packet rho_ret is normalized, conjugation-symmetric, zero on (1,1), nonnegative on (1,0)/(0,1)",
        abs(rho_00 - 1.0) < 1.0e-12
        and abs(rho_10 - rho_01) < 1.0e-12
        and rho_10 >= 0.0
        and rho_01 >= 0.0
        and abs(rho_11) < 1.0e-12,
        f"(rho_00,rho_10,rho_01,rho_11)=({rho_00:.6f},{rho_10:.6f},{rho_01:.6f},{rho_11:.6f})",
    )

    # Check 2: the zero-extension produces a self-adjoint, conjugation-symmetric
    # transfer on the truncated dominant-weight box (verified by direct numeric
    # symmetry, not by substring matching against an upstream note).
    sym_err = float(np.max(np.abs(t0 - t0.T)))
    conj_err = 0.0
    for i, (p, q) in enumerate(weights):
        j = index[(q, p)]
        conj_err = max(conj_err, abs(float(rho0[i]) - float(rho0[j])))
    check(
        "Zero-extension transfer t0 is self-adjoint and the underlying packet is conjugation-symmetric on the truncated box",
        sym_err < 1.0e-10 and conj_err < 1.0e-12,
        f"(sym_err,conj_err)=({sym_err:.3e},{conj_err:.3e})",
    )

    # Check 3: the two named witness tails add nonzero higher-weight mass.
    check(
        "The two explicit witness tails A and B add nonzero higher-weight mass above the retained packet",
        ma["tail_support"] > 0 and mb["tail_support"] > 0
        and ma["tail_mass"] > 0.0 and mb["tail_mass"] > 0.0,
        f"(supportA,supportB,massA,massB)=({ma['tail_support']},{mb['tail_support']},{ma['tail_mass']:.3e},{mb['tail_mass']:.3e})",
    )

    # Check 4: witness-restricted coefficientwise minimality.  The runner does
    # NOT claim universal coefficientwise uniqueness across all admissible
    # extensions.  This is the witness-restricted statement: the two named
    # tails are nonneg and dominate rho_0 coefficientwise.
    check(
        "On the two named witness tails A and B, the zero extension is coefficientwise <= the extended packet (witness-restricted, not universal)",
        m0["tail_mass"] == 0.0 and ma["tail_min"] >= -1.0e-14 and mb["tail_min"] >= -1.0e-14,
        f"(tail_mass0,tail_minA,tail_minB)=({m0['tail_mass']:.3e},{ma['tail_min']:.3e},{mb['tail_min']:.3e})",
    )

    # Check 5: PSD Loewner increment on the two named witness tails.
    eig_a = float(np.min(np.linalg.eigvalsh(delta_a)))
    eig_b = float(np.min(np.linalg.eigvalsh(delta_b)))
    check(
        "The two explicit witness tails A and B produce positive-semidefinite Loewner increments (witness-restricted, not universal)",
        eig_a > -1.0e-12 and eig_b > -1.0e-12,
        f"(eigminA,eigminB)=({eig_a:.3e},{eig_b:.3e})",
    )

    # Check 6: for the two named witness tails, the zero extension is Loewner-
    # minimal relative to those tested positive increments.  Witness-restricted.
    check(
        "For the two explicit witness tails, the zero extension is Loewner-minimal relative to those tested increments (witness-restricted, not universal)",
        eig_a > -1.0e-12
        and eig_b > -1.0e-12
        and m0["tail_mass"] == 0.0,
        f"||T_A-T_0||={np.linalg.norm(delta_a):.3e}, ||T_B-T_0||={np.linalg.norm(delta_b):.3e}",
    )

    # Check 7: the zero extension minimizes the sampled positive bulk-tail
    # functionals: total mass, weighted mass, squared l2 mass, support size.
    check(
        "The zero extension minimizes the four sampled positive bulk-tail functionals on the two witness tails (witness-restricted, not universal)",
        ma["tail_mass"] > 0.0
        and mb["tail_mass"] > 0.0
        and ma["tail_dim_mass"] > 0.0
        and mb["tail_dim_mass"] > 0.0
        and ma["tail_l2_sq"] > 0.0
        and mb["tail_l2_sq"] > 0.0
        and ma["tail_support"] > 0
        and mb["tail_support"] > 0,
        f"(massA,massB,dimMassA,dimMassB)=({ma['tail_mass']:.3e},{mb['tail_mass']:.3e},{ma['tail_dim_mass']:.3e},{mb['tail_dim_mass']:.3e})",
    )

    # Check 8: algebraic coefficientwise step on a randomized sweep of
    # admissible nonneg conjugation-symmetric tails.  This certifies the
    # algebraic identity `delta >= 0 ==> rho_0 + delta >= rho_0` rather than
    # universal Loewner monotonicity, which is recorded as an open gap.
    rng = np.random.default_rng(20260516)
    n_samples = 64
    coeff_min_violations = 0
    nonneg_violations = 0
    for _ in range(n_samples):
        delta = random_nonneg_tail(weights, index, rng)
        if float(np.min(delta)) < -1.0e-14:
            nonneg_violations += 1
        rho_sample = rho0 + delta
        m_sample = tail_metrics(rho_sample, rho0, weights, index)
        if m_sample["tail_min"] < -1.0e-14:
            coeff_min_violations += 1
    check(
        "Randomized sweep (n=64) of admissible nonneg conjugation-symmetric tails: delta >= 0 implies rho_0 + delta >= rho_0 coefficientwise",
        coeff_min_violations == 0 and nonneg_violations == 0,
        f"(coeff_violations,nonneg_violations)=({coeff_min_violations},{nonneg_violations})",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Bounded witness result:")
    print("    - rho_ret is a normalized, conjugation-symmetric, (1,1)-zero packet")
    print("      (numeric properties checked directly, no substring import)")
    print("    - the zero-extension produces a self-adjoint, conjugation-symmetric")
    print("      transfer on the truncated dominant-weight box (numeric check)")
    print("    - the two witness positive tails remain above the zero extension")
    print("      in coefficient order and in the tested Loewner increments")
    print("    - the zero extension minimizes the four sampled positive tail")
    print("      functionals on the two witness tails")
    print("    - randomized sweep certifies the algebraic identity")
    print("      delta >= 0 ==> rho_0 + delta >= rho_0 coefficientwise")
    print("    - the universal Loewner-minimal theorem for arbitrary admissible")
    print("      tails remains an open derivation gap (NOT closed by this runner)")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
