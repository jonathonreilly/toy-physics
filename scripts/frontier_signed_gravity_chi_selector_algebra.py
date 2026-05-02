#!/usr/bin/env python3
"""Algebra scan for a native signed-gravity branch selector.

This is the first P0 selector/no-go harness for the signed gravitational
response lane.  It asks whether the retained 8D Kogut-Susskind taste cell
contains a nontrivial Hermitian involution Q_chi that can do all of:

  1. define nonempty +/- sectors, Q_chi^2 = I
  2. be conserved by the free massive parity-correct staggered generators
  3. preserve the parity-correct scalar coupling operator epsilon
  4. pin the scalar source sign by branch, rather than only label a neutral
     taste degeneracy

The scan is intentionally strict.  A conserved label that does not fix the
scalar source sign is not enough for a physical signed gravitational sector.
"""

from __future__ import annotations

import itertools
import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np


EPS = 1e-12


def kron(*mats: np.ndarray) -> np.ndarray:
    out = mats[0]
    for mat in mats[1:]:
        out = np.kron(out, mat)
    return out


I2 = np.eye(2, dtype=np.complex128)
I8 = np.eye(8, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)

PAULIS = {"I": I2, "X": X, "Y": Y, "Z": Z}

# Retained KS taste generators, matching verify_cl3_sm_embedding.py.
G1 = kron(X, I2, I2)
G2 = kron(Z, X, I2)
G3 = kron(Z, Z, X)
GAMMAS = (G1, G2, G3)

# Parity/scalar mass-gap operator.  The retained scalar coupling is
# H_diag = (m + Phi) * epsilon.
EPSILON = kron(Z, Z, Z)

OMEGA = G1 @ G2 @ G3
I_OMEGA = 1j * OMEGA
C_TASTE = kron(X, X, X)


@dataclass(frozen=True)
class Candidate:
    name: str
    matrix: np.ndarray
    comm_kinetic: float
    comm_massive: float
    anticomm_kinetic: float
    comm_epsilon: float
    scalar_offdiag: float
    scalar_pin_error: float
    scalar_trace_plus: float
    scalar_trace_minus: float
    dim_plus: int
    dim_minus: int
    c_transform: str

    @property
    def kinetic_conserved(self) -> bool:
        return self.comm_kinetic < EPS

    @property
    def massive_conserved(self) -> bool:
        return self.comm_massive < EPS

    @property
    def epsilon_preserving(self) -> bool:
        return self.comm_epsilon < EPS and self.scalar_offdiag < EPS

    @property
    def scalar_pinned(self) -> bool:
        return self.scalar_pin_error < EPS

    @property
    def strict_selector(self) -> bool:
        return self.massive_conserved and self.epsilon_preserving and self.scalar_pinned


def fro_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, ord="fro"))


def max_comm(q: np.ndarray, ops: tuple[np.ndarray, ...]) -> float:
    return max(fro_norm(q @ op - op @ q) for op in ops)


def max_anticomm(q: np.ndarray, ops: tuple[np.ndarray, ...]) -> float:
    return max(fro_norm(q @ op + op @ q) for op in ops)


def transform_signature(unitary: np.ndarray, q: np.ndarray) -> str:
    transformed = unitary @ q @ unitary.conj().T
    if fro_norm(transformed - q) < EPS:
        return "even"
    if fro_norm(transformed + q) < EPS:
        return "odd"
    return "mixed"


def scalar_pin_metrics(q: np.ndarray) -> tuple[float, float, float, float, int, int]:
    p_plus = 0.5 * (I8 + q)
    p_minus = 0.5 * (I8 - q)
    dim_plus = int(round(float(np.trace(p_plus).real)))
    dim_minus = int(round(float(np.trace(p_minus).real)))

    offdiag = fro_norm(p_plus @ EPSILON @ p_minus) + fro_norm(p_minus @ EPSILON @ p_plus)

    # Strict branch-pinning means epsilon acts as +I on the plus sector and -I
    # on the minus sector, or vice versa.  This is stronger than block
    # diagonalization; it is the condition needed for branch sign alone to set
    # the scalar source sign for every state in that branch.
    err_pm = fro_norm(p_plus @ (EPSILON - I8) @ p_plus) + fro_norm(
        p_minus @ (EPSILON + I8) @ p_minus
    )
    err_mp = fro_norm(p_plus @ (EPSILON + I8) @ p_plus) + fro_norm(
        p_minus @ (EPSILON - I8) @ p_minus
    )
    pin_error = min(err_pm, err_mp)

    trace_plus = float(np.trace(p_plus @ EPSILON).real / max(dim_plus, 1))
    trace_minus = float(np.trace(p_minus @ EPSILON).real / max(dim_minus, 1))
    return offdiag, pin_error, trace_plus, trace_minus, dim_plus, dim_minus


def pauli_string_candidates() -> list[tuple[str, np.ndarray]]:
    out: list[tuple[str, np.ndarray]] = []
    for labels in itertools.product(PAULIS.keys(), repeat=3):
        name = "".join(labels)
        mat = kron(*(PAULIS[label] for label in labels))
        if name == "III":
            continue
        out.append((name, mat))
    return out


def named_candidate_rows() -> list[tuple[str, np.ndarray]]:
    return [
        ("epsilon_ZZZ", EPSILON),
        ("iOmega", I_OMEGA),
        ("C_taste_XXX", C_TASTE),
        ("Gamma1_XII", G1),
        ("Gamma2_ZXI", G2),
        ("Gamma3_ZZX", G3),
    ]


def evaluate(name: str, q: np.ndarray) -> Candidate:
    if not np.allclose(q, q.conj().T, atol=EPS):
        raise ValueError(f"{name} is not Hermitian")
    if not np.allclose(q @ q, I8, atol=EPS):
        raise ValueError(f"{name} is not an involution")
    offdiag, pin_error, trace_plus, trace_minus, dim_plus, dim_minus = scalar_pin_metrics(q)
    return Candidate(
        name=name,
        matrix=q,
        comm_kinetic=max_comm(q, GAMMAS),
        comm_massive=max_comm(q, GAMMAS + (EPSILON,)),
        anticomm_kinetic=max_anticomm(q, GAMMAS),
        comm_epsilon=fro_norm(q @ EPSILON - EPSILON @ q),
        scalar_offdiag=offdiag,
        scalar_pin_error=pin_error,
        scalar_trace_plus=trace_plus,
        scalar_trace_minus=trace_minus,
        dim_plus=dim_plus,
        dim_minus=dim_minus,
        c_transform=transform_signature(C_TASTE, q),
    )


def hamiltonian_k(kvec: tuple[float, float, float], mass: float, phi: float = 0.0) -> np.ndarray:
    h = np.zeros((8, 8), dtype=np.complex128)
    for coeff, gamma in zip((math.sin(kvec[0]), math.sin(kvec[1]), math.sin(kvec[2])), GAMMAS):
        h += coeff * gamma
    h += (mass + phi) * EPSILON
    return h


def leakage_norm(q: np.ndarray, mass: float = 0.3, phi: float = 0.0) -> float:
    p_plus = 0.5 * (I8 + q)
    p_minus = 0.5 * (I8 - q)
    samples = (
        (0.1, 0.2, 0.3),
        (0.4, 0.0, -0.2),
        (0.7, -0.5, 0.25),
        (1.1, 0.8, -0.6),
    )
    return max(fro_norm(p_minus @ hamiltonian_k(k, mass, phi) @ p_plus) for k in samples)


def print_row(row: Candidate) -> None:
    verdict = "STRICT" if row.strict_selector else (
        "CONSERVED_NEUTRAL" if row.massive_conserved else (
            "KINETIC_ONLY" if row.kinetic_conserved else (
                "EPSILON_PIN_BROKEN" if row.scalar_pinned else "NO"
            )
        )
    )
    print(
        f"  {row.name:<14s} {row.dim_plus:2d}/{row.dim_minus:<2d} "
        f"{row.comm_kinetic:10.2e} {row.comm_massive:10.2e} "
        f"{row.scalar_offdiag:10.2e} {row.scalar_pin_error:10.2e} "
        f"{row.scalar_trace_plus:+7.3f} {row.scalar_trace_minus:+7.3f} "
        f"{row.c_transform:>6s}  {verdict}"
    )


def check_clifford() -> bool:
    ok = True
    for idx, gamma in enumerate(GAMMAS, start=1):
        ok = ok and np.allclose(gamma @ gamma, I8, atol=EPS)
        print(f"  Gamma{idx}^2 residual: {fro_norm(gamma @ gamma - I8):.2e}")
    for (i, gi), (j, gj) in itertools.combinations(enumerate(GAMMAS, start=1), 2):
        residual = fro_norm(gi @ gj + gj @ gi)
        ok = ok and residual < EPS
        print(f"  {{Gamma{i}, Gamma{j}}} residual: {residual:.2e}")
    for idx, gamma in enumerate(GAMMAS, start=1):
        residual = fro_norm(EPSILON @ gamma + gamma @ EPSILON)
        ok = ok and residual < EPS
        print(f"  {{epsilon, Gamma{idx}}} residual: {residual:.2e}")
    print(f"  epsilon^2 residual: {fro_norm(EPSILON @ EPSILON - I8):.2e}")
    return ok and fro_norm(EPSILON @ EPSILON - I8) < EPS


def main() -> None:
    print("=" * 98)
    print("SIGNED GRAVITY CHI SELECTOR ALGEBRA SCAN")
    print("  P0 gate: native chi_g operator versus conserved-neutral taste label")
    print("=" * 98)
    print()

    print("CLIFFORD / PARITY-SCALAR SURFACE")
    clifford_ok = check_clifford()
    print(f"  surface check: {'PASS' if clifford_ok else 'FAIL'}")
    print()

    rows = [evaluate(name, mat) for name, mat in pauli_string_candidates()]
    strict = [row for row in rows if row.strict_selector]
    massive_conserved = [row for row in rows if row.massive_conserved]
    kinetic_only = [row for row in rows if row.kinetic_conserved and not row.massive_conserved]
    scalar_pinned = [row for row in rows if row.scalar_pinned]

    print("NAMED CANDIDATES")
    print(
        "  name           dim   comm_kin   comm_full  eps_offdiag  pin_error "
        "  tr+     tr-      C  verdict"
    )
    print("  " + "-" * 93)
    for name, mat in named_candidate_rows():
        print_row(evaluate(name, mat))
    print()

    print("BEST PAULI-STRING CANDIDATES")
    print(
        "  name           dim   comm_kin   comm_full  eps_offdiag  pin_error "
        "  tr+     tr-      C  verdict"
    )
    print("  " + "-" * 93)
    interesting = (
        sorted(massive_conserved, key=lambda r: (r.scalar_pin_error, r.name))
        + sorted(kinetic_only, key=lambda r: (r.comm_massive, r.scalar_pin_error, r.name))[:6]
        + sorted(scalar_pinned, key=lambda r: (r.comm_massive, r.name))[:4]
    )
    seen: set[str] = set()
    for row in interesting:
        if row.name in seen:
            continue
        seen.add(row.name)
        print_row(row)
    print()

    print("PROJECTOR LEAKAGE ON SAMPLE H(k) = sum sin(k_i) Gamma_i + (m+Phi) epsilon")
    for row in sorted(massive_conserved + kinetic_only, key=lambda r: (not r.massive_conserved, r.name)):
        leak_massive = leakage_norm(row.matrix, mass=0.3, phi=0.04)
        print(f"  {row.name:<8s} leakage={leak_massive:.2e}  class={'massive' if row.massive_conserved else 'kinetic-only'}")
    print()

    print("SCAN SUMMARY")
    print(f"  Pauli-string involutions scanned: {len(rows)}")
    print(f"  kinetic-conserved candidates: {sum(r.kinetic_conserved for r in rows)}")
    print(f"  massive parity-scalar conserved candidates: {len(massive_conserved)}")
    print(f"  scalar-source pinned candidates: {len(scalar_pinned)}")
    print(f"  strict selector candidates: {len(strict)}")
    print()

    print("INTERPRETATION")
    if strict:
        print("  THEOREM_CANDIDATE: at least one local Pauli-string involution passes")
        print("  the strict conserved signed-source selector gates. This must still be")
        print("  lifted to a source-density and interaction-superselection theorem.")
        tag = "THEOREM_CANDIDATE"
    else:
        print("  NO_GO_STRICT_SELECTOR: this local Pauli-string scan finds no operator")
        print("  that is both conserved on the massive parity-correct scalar surface")
        print("  and branch-pins the scalar source sign.")
        print()
        print("  What survives: conserved neutral taste-degeneracy labels, e.g. the")
        print("  rows marked CONSERVED_NEUTRAL. They commute with the retained free")
        print("  massive scalar generators, but epsilon has zero branch trace and is")
        print("  not pinned to +/- by those labels.")
        print()
        print("  What fails: epsilon itself pins scalar sign but is not conserved by")
        print("  kinetic hopping; iOmega is kinetic-conserved but broken by the")
        print("  parity-scalar mass/coupling. Neither is a physical chi_g selector.")
        tag = "NO_GO_STRICT_SELECTOR"

    print()
    print(f"FINAL_TAG: {tag}")


if __name__ == "__main__":
    main()
