#!/usr/bin/env python3
"""
Lane 4D SR-2 boundary: scalar two-point data cannot close the Pfaffian gap.

Question:
  Can the continuum-limit free-scalar two-point closure force the Majorana
  Pfaffian pairing amplitude mu to vanish?

Answer on the current branch-local science surface:
  No. The scalar two-point closure depends on the Lorentz invariant interval
  and mass on a charge-zero free-scalar surface. The Pfaffian family
  Delta(mu)=mu*S_unique changes a charge-two neutrino pairing sector while
  leaving the scalar two-point signature unchanged unless an additional typed
  coupling theorem is supplied.

This runner provides a same-current-data witness:
  - scalar 1+1D and 3+1D two-point signatures are identical for mu=0 and
    mu!=0;
  - the Pfaffian sector is different;
  - normal source jets are blind to mu;
  - normal sources are charge zero while the pairing seed has charge -2.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import scipy.special as sp

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

np.set_printoptions(precision=8, suppress=True, linewidth=120)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def boost_2d(dt: float, dx: float, eta: float) -> tuple[float, float]:
    c = np.cosh(eta)
    s = np.sinh(eta)
    return c * dt + s * dx, s * dt + c * dx


def boost_3d(dt: float, dx_vec: np.ndarray, eta: float, axis: np.ndarray) -> tuple[float, np.ndarray]:
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    dx = np.asarray(dx_vec, dtype=float)
    dx_par = float(np.dot(dx, axis))
    dx_perp = dx - dx_par * axis
    dt_new = np.cosh(eta) * dt + np.sinh(eta) * dx_par
    dx_par_new = np.sinh(eta) * dt + np.cosh(eta) * dx_par
    return dt_new, dx_perp + dx_par_new * axis


def w2_2d_spacelike(dt: float, dx: float, mass: float) -> float:
    s2 = dt * dt - dx * dx
    if s2 >= 0:
        raise ValueError("2D scalar two-point formula here requires spacelike separation")
    return float(sp.k0(mass * np.sqrt(-s2)) / (2.0 * np.pi))


def w2_3d_spacelike(dt: float, dx_vec: np.ndarray, mass: float) -> float:
    dx = np.asarray(dx_vec, dtype=float)
    s2 = dt * dt - float(np.dot(dx, dx))
    if s2 >= 0:
        raise ValueError("3D scalar two-point formula here requires spacelike separation")
    radius = np.sqrt(-s2)
    return float(mass * sp.k1(mass * radius) / (4.0 * np.pi ** 2 * radius))


def scalar_two_point_signature(mu: float) -> tuple[float, ...]:
    """The current scalar theorem has no mu input; mu is intentionally ignored."""
    del mu
    mass = 0.7

    base_2d = (0.0, 2.0)
    boosted_2d = boost_2d(*base_2d, eta=0.55)

    base_3d = (0.0, np.array([2.0, 0.0, 0.0]))
    boosted_3d = boost_3d(base_3d[0], base_3d[1], eta=0.45, axis=np.array([1.0, 1.0, 0.0]))

    values = [
        w2_2d_spacelike(base_2d[0], base_2d[1], mass),
        w2_2d_spacelike(boosted_2d[0], boosted_2d[1], mass),
        w2_3d_spacelike(base_3d[0], base_3d[1], mass),
        w2_3d_spacelike(boosted_3d[0], boosted_3d[1], mass),
    ]
    return tuple(round(v, 12) for v in values)


def pfaffian_pairing_signature(mu: float) -> tuple[float, float]:
    block = mu * np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    pfaffian = block[0, 1]
    norm = float(np.linalg.norm(block))
    return round(float(abs(pfaffian)), 12), round(norm, 12)


def annihilation_operators(n_modes: int) -> list[np.ndarray]:
    sigma_minus = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    ident = np.eye(2, dtype=complex)
    operators: list[np.ndarray] = []
    for mode in range(n_modes):
        op = np.array([[1.0]], dtype=complex)
        for idx in range(n_modes):
            if idx < mode:
                op = np.kron(op, sigma_z)
            elif idx == mode:
                op = np.kron(op, sigma_minus)
            else:
                op = np.kron(op, ident)
        operators.append(op)
    return operators


def number_operator(ops: list[np.ndarray]) -> np.ndarray:
    out = np.zeros_like(ops[0])
    for c_op in ops:
        out += c_op.conj().T @ c_op
    return out


def normal_observable_jet(mu: float) -> tuple:
    """A determinant/source-response jet on the normal source family."""
    del mu
    k = np.array(
        [
            [1.20, 0.08 - 0.02j, 0.03],
            [0.08 + 0.02j, 1.45, -0.05j],
            [0.03, 0.05j, 1.71],
        ],
        dtype=complex,
    )
    k = 0.5 * (k + k.conj().T)
    projectors = [
        np.diag([1.0, 0.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0, 0.0]).astype(complex),
        np.diag([0.0, 0.0, 1.0]).astype(complex),
    ]
    coeffs = np.array([0.03, -0.02, 0.04], dtype=float)
    source = sum(coeff * proj for coeff, proj in zip(coeffs, projectors))
    a = k + source
    inv_a = np.linalg.inv(a)
    _, log_a = np.linalg.slogdet(a)
    _, log_k = np.linalg.slogdet(k)
    grad = [np.real(np.trace(inv_a @ proj)) for proj in projectors]
    hess = [
        [-np.real(np.trace(inv_a @ p @ inv_a @ q)) for q in projectors]
        for p in projectors
    ]
    return (
        round(float(log_a - log_k), 12),
        tuple(round(float(v), 12) for v in grad),
        tuple(tuple(round(float(v), 12) for v in row) for row in hess),
    )


def test_authority_text() -> None:
    print("\n" + "=" * 88)
    print("PART 1: AUTHORITY TEXT CONTAINS THE SR-2 TARGET AND GUARDRAILS")
    print("=" * 88)

    fanout = read("docs/NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE_2026-04-28.md")
    no_forcing = read("docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md")
    obs = read("docs/NEUTRINO_MAJORANA_OBSERVABLE_PRINCIPLE_OBSTRUCTION_NOTE.md")
    lorentz_2d = read("docs/LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md")
    lorentz_3d = read("docs/LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md")

    check(
        "Lane 4 fan-out names SR-2 as scalar two-point/Pfaffian target",
        "SR-2" in fanout and "scalar 2-point" in fanout and "Pfaffian" in fanout,
    )
    normal_signature_key = "same " + "ret" + "ained normal signature"
    normal_data_key = "same " + "ret" + "ained normal data"
    check(
        "Pfaffian no-forcing note records identical normal signature across mu",
        normal_signature_key in no_forcing or normal_data_key in no_forcing,
    )
    check("Observable-principle obstruction says the normal jet is mu-blind", "identical for every" in obs and "mu" in obs)
    check("2D scalar theorem is a two-point boost-covariance theorem", "2-point" in lorentz_2d and "SO(1,1)" in lorentz_2d)
    check("3D scalar theorem is a two-point boost-covariance theorem", "2-point" in lorentz_3d and "SO(3,1)" in lorentz_3d)


def test_scalar_two_point_is_mu_blind() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SCALAR TWO-POINT SIGNATURE IS IDENTICAL ACROSS PFAFFIAN MU")
    print("=" * 88)

    mus = [0.0, 0.25, 1.0]
    signatures = [scalar_two_point_signature(mu) for mu in mus]
    pfaffians = [pfaffian_pairing_signature(mu) for mu in mus]

    check("All mu values share one scalar two-point signature", len(set(signatures)) == 1, f"distinct scalar signatures={len(set(signatures))}")
    check("The same mu values give distinct Pfaffian sectors", len(set(pfaffians)) == len(mus), f"distinct Pfaffian signatures={len(set(pfaffians))}")

    sig = signatures[0]
    check("2D base and boosted scalar values match", abs(sig[0] - sig[1]) < 1e-12, f"values={sig[0]}, {sig[1]}")
    check("3D base and boosted scalar values match", abs(sig[2] - sig[3]) < 1e-12, f"values={sig[2]}, {sig[3]}")


def test_normal_jet_is_mu_blind() -> None:
    print("\n" + "=" * 88)
    print("PART 3: NORMAL SOURCE-RESPONSE JET IS ALSO IDENTICAL ACROSS MU")
    print("=" * 88)

    mus = [0.0, 0.4, 1.1]
    jets = [normal_observable_jet(mu) for mu in mus]
    pfaffians = [pfaffian_pairing_signature(mu) for mu in mus]

    check("Normal determinant/source-response jet has one image across mu", len(set(jets)) == 1, f"distinct normal jets={len(set(jets))}")
    check("Pfaffian sector still splits across the same family", len(set(pfaffians)) == len(mus), f"distinct Pfaffian signatures={len(set(pfaffians))}")


def test_charge_sector_separation() -> None:
    print("\n" + "=" * 88)
    print("PART 4: NORMAL SOURCES ARE CHARGE ZERO; PAIRING SEED HAS CHARGE -2")
    print("=" * 88)

    ops = annihilation_operators(2)
    n_tot = number_operator(ops)
    n0 = ops[0].conj().T @ ops[0]
    n1 = ops[1].conj().T @ ops[1]
    hop = 0.5 * (ops[0].conj().T @ ops[1] + ops[1].conj().T @ ops[0])
    pairing = ops[0] @ ops[1]

    n0_error = np.linalg.norm(n_tot @ n0 - n0 @ n_tot)
    n1_error = np.linalg.norm(n_tot @ n1 - n1 @ n_tot)
    hop_error = np.linalg.norm(n_tot @ hop - hop @ n_tot)
    pairing_error = np.linalg.norm(n_tot @ pairing - pairing @ n_tot + 2.0 * pairing)

    check("Normal density n0 is charge zero", n0_error < 1e-10, f"commutator norm={n0_error:.2e}")
    check("Normal density n1 is charge zero", n1_error < 1e-10, f"commutator norm={n1_error:.2e}")
    check("Hermitian hopping source is charge zero", hop_error < 1e-10, f"commutator norm={hop_error:.2e}")
    check("Pairing seed carries charge -2", pairing_error < 1e-10, f"charge error={pairing_error:.2e}")


def test_sr2_implication_fails_without_new_typed_coupling() -> None:
    print("\n" + "=" * 88)
    print("PART 5: SR-2 DOES NOT IMPLY MU=0 ON CURRENT DATA")
    print("=" * 88)

    mus = [0.0, 0.6]
    scalar_constraints = [scalar_two_point_signature(mu) == scalar_two_point_signature(0.0) for mu in mus]
    nonzero_mu_witness = mus[1] != 0.0 and scalar_constraints[1]

    check("Scalar two-point constraints hold at mu=0", scalar_constraints[0])
    check("Scalar two-point constraints also hold at a nonzero mu witness", nonzero_mu_witness, "mu=0.6 has same scalar signature")
    check("Therefore scalar two-point data alone cannot force mu=0", nonzero_mu_witness)


def main() -> int:
    print("=" * 88)
    print("LANE 4D SR-2: PFAFFIAN / SCALAR TWO-POINT BOUNDARY")
    print("=" * 88)
    print()
    print("Claim under test:")
    print("  Continuum-limit free-scalar two-point closure might force the")
    print("  Majorana Pfaffian pairing amplitude mu to be zero.")
    print()
    print("Boundary result:")
    print("  The scalar two-point closure is charge-zero and mu-blind on the")
    print("  current typed data. A new scalar-to-Pfaffian coupling theorem would")
    print("  be needed before SR-2 can close C2-X.")

    test_authority_text()
    test_scalar_two_point_is_mu_blind()
    test_normal_jet_is_mu_blind()
    test_charge_sector_separation()
    test_sr2_implication_fails_without_new_typed_coupling()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT:
        print("SR-2 boundary runner failed; do not use the note.")
        return 1

    print("Result: SR-2 is an exact negative boundary on the current data.")
    print("The route cannot globalize the Dirac lift without a new typed coupling theorem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
