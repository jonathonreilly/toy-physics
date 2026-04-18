#!/usr/bin/env python3
"""
Bulk-side cyclic reduction after the plaquette beta=6 identity-rim reduction.

This sharpens the remaining operator-side closure target in two exact ways:

1. the live upstream bulk object is only the eta_6(e)-cyclic compression of the
   compressed bulk operator S_6^env;
2. even fixed eta_6(e) together with the exact propagated retained triple still
   does not determine that reduced cyclic bulk object on the current bank.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

SAMPLES = {
    "W_A": (-13 * math.pi / 16.0, 5 * math.pi / 8.0),
    "W_B": (-5 * math.pi / 16.0, -7 * math.pi / 16.0),
    "W_C": (7 * math.pi / 16.0, -11 * math.pi / 16.0),
}
ORBITS = [(0, 2), (0, 3), (0, 4), (0, 5)]
BASELINE = np.ones(4, dtype=float)
EPSILON = 4.0 / 5.0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def su3_character(p: int, q: int, theta1: float, theta2: float) -> complex:
    x = [
        cmath.exp(1j * theta1),
        cmath.exp(1j * theta2),
        cmath.exp(-1j * (theta1 + theta2)),
    ]
    lam = [p + q, q, 0]
    num = np.array([[x[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    den = np.array([[x[i] ** (2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    return complex(np.linalg.det(num) / np.linalg.det(den))


def orbit_sample_row(p: int, q: int) -> np.ndarray:
    d = dim_su3(p, q)
    row = []
    for theta1, theta2 in SAMPLES.values():
        ch = su3_character(p, q, theta1, theta2)
        value = d * ch if p == q else 2.0 * (d * ch).real
        row.append(float(np.real_if_close(value)))
    return np.array(row, dtype=float)


def sample_matrix() -> np.ndarray:
    return np.column_stack([orbit_sample_row(*orbit) for orbit in ORBITS])


def normalize(vec: np.ndarray) -> np.ndarray:
    return vec / np.linalg.norm(vec)


def bulk_from_target(v: np.ndarray, eta: np.ndarray) -> np.ndarray:
    scale = float(np.dot(v, eta))
    return np.outer(v, v) / scale


def block_diag(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    out = np.zeros((a.shape[0] + b.shape[0], a.shape[1] + b.shape[1]), dtype=float)
    out[: a.shape[0], : a.shape[1]] = a
    out[a.shape[0] :, a.shape[1] :] = b
    return out


def moments(op: np.ndarray, eta: np.ndarray, nmax: int) -> list[float]:
    return [float(eta @ (np.linalg.matrix_power(op, n) @ eta)) for n in range(nmax + 1)]


def main() -> int:
    identity_rim_note = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_REDUCTION_NOTE_2026-04-17.md")
    spectral_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md")
    perron_note = read("docs/GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md")
    operator_nonclosure_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_OPERATOR_SIDE_NONCLOSURE_NOTE_2026-04-17.md"
    )

    e3 = sample_matrix()
    _, _, vh = np.linalg.svd(e3)
    kernel = vh[-1]
    kernel_residual = float(np.max(np.abs(e3 @ kernel)))

    v_p = BASELINE + EPSILON * kernel
    v_q = BASELINE - EPSILON * kernel
    eta = normalize(np.ones(4, dtype=float))

    s_p = bulk_from_target(v_p, eta)
    s_q = bulk_from_target(v_q, eta)
    propagated_p = s_p @ eta
    propagated_q = s_q @ eta
    triple_p = e3 @ propagated_p
    triple_q = e3 @ propagated_q
    triple_gap = float(np.max(np.abs(triple_p - triple_q)))

    moments_p = moments(s_p, eta, 3)
    moments_q = moments(s_q, eta, 3)
    moment1_gap = abs(moments_p[1] - moments_q[1])
    moment2_gap = abs(moments_p[2] - moments_q[2])

    ext_a = block_diag(s_p, np.diag([0.2, 0.3]))
    ext_b = block_diag(s_p, np.diag([0.9, 1.4]))
    eta_ext = np.concatenate([eta, np.zeros(2, dtype=float)])
    orbit_gaps = [
        float(np.max(np.abs(np.linalg.matrix_power(ext_a, n) @ eta_ext - np.linalg.matrix_power(ext_b, n) @ eta_ext)))
        for n in range(4)
    ]
    triple_ext_gap = float(
        np.max(np.abs(e3 @ (ext_a[:4, :4] @ eta) - e3 @ (ext_b[:4, :4] @ eta)))
    )
    complement_gap = float(np.max(np.abs(ext_a - ext_b)))

    eig_p = np.linalg.eigvalsh(s_p)
    eig_q = np.linalg.eigvalsh(s_q)

    print("=" * 124)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 IDENTITY-RIM CYCLIC BULK REDUCTION")
    print("=" * 124)
    print()
    print(f"higher-orbit slice                           = {ORBITS}")
    print(f"sample matrix shape / rank                   = {e3.shape} / {np.linalg.matrix_rank(e3)}")
    print(f"kernel direction                             = {kernel}")
    print(f"kernel residual max-norm                     = {kernel_residual:.12e}")
    print()
    print(f"fixed identity rim eta                       = {eta}")
    print(f"v_P                                          = {v_p}")
    print(f"v_Q                                          = {v_q}")
    print(f"max propagated triple gap                    = {triple_gap:.12e}")
    print(f"triple_P                                     = {triple_p}")
    print(f"triple_Q                                     = {triple_q}")
    print()
    print(f"moment sequence P                            = {[round(x, 12) for x in moments_p]}")
    print(f"moment sequence Q                            = {[round(x, 12) for x in moments_q]}")
    print(f"moment gaps (m1, m2)                         = ({moment1_gap:.12f}, {moment2_gap:.12f})")
    print()
    print(f"PSD eigenvalue floors (P, Q)                 = ({eig_p[0]:.12e}, {eig_q[0]:.12e})")
    print(f"orthogonal-complement block gap              = {complement_gap:.12f}")
    print(f"orbit gaps under complement variation        = {[f'{x:.3e}' for x in orbit_gaps]}")
    print(f"triple gap under complement variation        = {triple_ext_gap:.12e}")
    print()

    check(
        "The identity-rim reduction note already reduces explicit class-sector beta=6 closure to bulk data plus the identity rim datum eta_6(e), with generic W dependence already downstream through K(W)",
        "`eta_6(e) = P_cls B_6(e)`" in identity_rim_note
        and "bulk operator together with the" in identity_rim_note
        and "generic marked-holonomy dependence is already carried by the universal" in identity_rim_note,
        bucket="SUPPORT",
    )
    check(
        "The spectral-measure theorem already licenses spectral-measure language only at the level of one state-seen generating object",
        "unique exact" in spectral_note
        and "compact positive spectral measure" in spectral_note
        and "Hausdorff moment uniqueness" in spectral_note,
        bucket="SUPPORT",
    )
    check(
        "The Perron-reduction theorem already licenses the equivalent Jacobi-data reading on the cyclic subspace generated by one state under repeated application of the operator",
        "equivalent to one unique Jacobi operator" in perron_note
        and "source-cyclic subspace" in perron_note
        and "Perron moments" in perron_note,
        bucket="SUPPORT",
    )
    check(
        "The propagated-triple operator-side nonclosure note already states that the propagated retained triple is the right finite target but not itself an operator-side closure datum",
        "propagated retained triple is the correct finite *target*" in operator_nonclosure_note
        and "still not an operator-side *closure* datum" in operator_nonclosure_note,
        bucket="SUPPORT",
    )

    check(
        "Two positive self-adjoint bulk operators with the same eta-cyclic core but different orthogonal-complement blocks induce the same propagated eta-orbit and the same boundary triple",
        max(orbit_gaps) < 1.0e-12 and triple_ext_gap < 1.0e-12 and complement_gap > 1.0,
        detail=f"max orbit gap={max(orbit_gaps):.3e}, triple gap={triple_ext_gap:.3e}, complement gap={complement_gap:.3f}",
    )
    check(
        "So the live upstream bulk object is only the eta-cyclic compression, not the whole compressed bulk operator",
        max(orbit_gaps) < 1.0e-12 and complement_gap > 1.0,
        detail="orthogonal-complement changes are class-sector invisible once eta is fixed",
    )
    check(
        "On the explicit four-orbit slice there are two distinct nonnegative propagated beta-side vectors with the same exact propagated retained triple",
        kernel_residual < 1.0e-10 and np.min(v_p) > 0.0 and np.min(v_q) > 0.0 and triple_gap < 1.0e-10,
        detail=f"min(v_P)={np.min(v_p):.12f}, min(v_Q)={np.min(v_q):.12f}, triple gap={triple_gap:.3e}",
    )
    check(
        "The rank-one positive bulk witnesses S_P and S_Q map the same fixed identity rim state eta to those two distinct vectors",
        np.max(np.abs(propagated_p - v_p)) < 1.0e-12
        and np.max(np.abs(propagated_q - v_q)) < 1.0e-12
        and eig_p[0] > -1.0e-12
        and eig_q[0] > -1.0e-12,
        detail=f"map errors=({np.max(np.abs(propagated_p - v_p)):.3e}, {np.max(np.abs(propagated_q - v_q)):.3e})",
    )
    check(
        "Even with the same fixed identity rim state and the same exact propagated retained triple, the cyclic moment sequences of S_P and S_Q already differ",
        moment1_gap > 1.0e-6 and moment2_gap > 1.0e-6,
        detail=f"moment gaps=(m1:{moment1_gap:.12f}, m2:{moment2_gap:.12f})",
    )
    check(
        "Therefore the present finite propagated target still does not determine the reduced cyclic bulk spectral / Jacobi object on the current bank",
        triple_gap < 1.0e-10 and moment1_gap > 1.0e-6 and moment2_gap > 1.0e-6,
        detail="same eta, same propagated triple, different cyclic bulk moments",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
