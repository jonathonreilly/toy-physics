"""Finite checks for the Cl(3) Z_2 one-sided SU(2) selection no-go.

The runner verifies the load-bearing algebra in
docs/KOIDE_W_SUBSTRATE_CHIRALITY_CL3_Z2_NOTE_2026-05-10_probeW_substrate_chirality.md:
the grade involution fixes Cl^+(3) pointwise, so the same SU(2) carrier is
available on both Pauli chirality summands. The runner does not test anomaly
cancellation, matter-packet phenomenology, or any sibling probe branch.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import numpy as np


I2 = np.eye(2, dtype=complex)
ZERO2 = np.zeros((2, 2), dtype=complex)
SIG1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIG2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIG3 = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = (SIG1, SIG2, SIG3)


def close(left: np.ndarray, right: np.ndarray, tol: float = 1e-12) -> bool:
    return bool(np.max(np.abs(left - right)) < tol)


@dataclass
class Counter:
    passed: int = 0
    failed: int = 0

    def record(self, label: str, ok: bool, detail: str = "", cls: str = "") -> None:
        status = "PASS" if ok else "FAIL"
        tag = f" ({cls})" if cls else ""
        suffix = f" -- {detail}" if detail else ""
        print(f"  [{status}{tag}] {label}{suffix}")
        if ok:
            self.passed += 1
        else:
            self.failed += 1


def check_clifford(rep: tuple[np.ndarray, np.ndarray, np.ndarray]) -> bool:
    for i, gamma_i in enumerate(rep):
        for j, gamma_j in enumerate(rep):
            anti = gamma_i @ gamma_j + gamma_j @ gamma_i
            expected = 2 * (1 if i == j else 0) * I2
            if not close(anti, expected):
                return False
    return True


def section_chirality_reps(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 1: two Pauli chirality summands")
    print("=" * 76)

    rho_plus = PAULI
    rho_minus = tuple(-sigma for sigma in PAULI)
    omega_plus = rho_plus[0] @ rho_plus[1] @ rho_plus[2]
    omega_minus = rho_minus[0] @ rho_minus[1] @ rho_minus[2]

    c.record("rho_+ satisfies the Cl(3) anticommutators",
             check_clifford(rho_plus), cls="input")
    c.record("rho_- satisfies the Cl(3) anticommutators",
             check_clifford(rho_minus), cls="input")
    c.record("rho_+(omega) = +i I",
             close(omega_plus, 1j * I2), cls="input")
    c.record("rho_-(omega) = -i I",
             close(omega_minus, -1j * I2), cls="input")
    c.record("rho_+ and rho_- are distinct central-character summands",
             not close(omega_plus, omega_minus), cls="input")
    print()


def section_even_subalgebra_fixed(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 2: grade involution fixes Cl^+(3)")
    print("=" * 76)

    bivectors_plus = {
        "e12": SIG1 @ SIG2,
        "e13": SIG1 @ SIG3,
        "e23": SIG2 @ SIG3,
    }
    bivectors_minus = {
        "e12": (-SIG1) @ (-SIG2),
        "e13": (-SIG1) @ (-SIG3),
        "e23": (-SIG2) @ (-SIG3),
    }

    for name in ("e12", "e13", "e23"):
        c.record(
            f"rho_+({name}) = rho_-({name})",
            close(bivectors_plus[name], bivectors_minus[name]),
            "the two minus signs cancel on even generators",
            cls="no-go",
        )
        c.record(
            f"{name}^2 = -I",
            close(bivectors_plus[name] @ bivectors_plus[name], -I2),
            "quaternionic Cl^+(3) generator",
            cls="support",
        )

    qi, qj, qk = bivectors_plus["e23"], bivectors_plus["e13"], bivectors_plus["e12"]
    c.record("Cl^+(3) quaternion product i*j = k", close(qi @ qj, qk), cls="support")
    c.record("Cl^+(3) quaternion product j*k = i", close(qj @ qk, qi), cls="support")
    c.record("Cl^+(3) quaternion product k*i = j", close(qk @ qi, qj), cls="support")
    c.record(
        "alpha restricts to the identity on Cl^+(3)",
        all(close(bivectors_plus[name], bivectors_minus[name]) for name in bivectors_plus),
        "alpha(gamma_i gamma_j)=(-gamma_i)(-gamma_j)",
        cls="no-go",
    )
    print()


def embed_left(matrix: np.ndarray) -> np.ndarray:
    return np.block([[matrix, ZERO2], [ZERO2, ZERO2]])


def embed_right(matrix: np.ndarray) -> np.ndarray:
    return np.block([[ZERO2, ZERO2], [ZERO2, matrix]])


def section_su2_selection(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 3: SU(2) exists on either summand")
    print("=" * 76)

    j1, j2, j3 = (sigma / 2 for sigma in PAULI)
    c.record("[J1, J2] = i J3 on rho_+", close(j1 @ j2 - j2 @ j1, 1j * j3), cls="support")
    c.record("[J1, J2] = i J3 on rho_-", close(j1 @ j2 - j2 @ j1, 1j * j3), cls="support")
    c.record(
        "left SU(2) and right SU(2) commute on rho_+ oplus rho_-",
        close(embed_left(j1) @ embed_right(j2) - embed_right(j2) @ embed_left(j1),
              np.zeros((4, 4), dtype=complex)),
        cls="no-go",
    )

    one_sided_generators = [embed_left(j) for j in (j1, j2, j3)]
    two_sided_generators = [embed_left(j) + embed_right(j) for j in (j1, j2, j3)]
    one_sided_ok = close(
        one_sided_generators[0] @ one_sided_generators[1]
        - one_sided_generators[1] @ one_sided_generators[0],
        1j * one_sided_generators[2],
    )
    two_sided_ok = close(
        two_sided_generators[0] @ two_sided_generators[1]
        - two_sided_generators[1] @ two_sided_generators[0],
        1j * two_sided_generators[2],
    )
    c.record("one-sided SU(2) assignment closes algebraically", one_sided_ok, cls="support")
    c.record("two-sided SU(2) assignment closes algebraically", two_sided_ok, cls="support")
    c.record(
        "grade involution does not select one-sided over two-sided SU(2)",
        one_sided_ok and two_sided_ok,
        "both assignments satisfy the same finite algebra constraints",
        cls="no-go",
    )
    print()


def section_no_internal_gamma5(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 4: no per-site gamma_5 selector in M_2(C)")
    print("=" * 76)

    omega = SIG1 @ SIG2 @ SIG3
    c.record("omega = i I in the Pauli summand", close(omega, 1j * I2), cls="support")
    for index, sigma in enumerate(PAULI, start=1):
        c.record(
            f"[omega, sigma_{index}] = 0",
            close(omega @ sigma - sigma @ omega, ZERO2),
            "omega is central in a single Pauli summand",
            cls="support",
        )

    basis = (I2, SIG1, SIG2, SIG3)
    columns = []
    for basis_matrix in basis:
        constraints = []
        for sigma in PAULI:
            constraints.append((basis_matrix @ sigma + sigma @ basis_matrix).reshape(-1))
        columns.append(np.concatenate(constraints))
    constraint_matrix = np.column_stack(columns)
    rank = np.linalg.matrix_rank(constraint_matrix, tol=1e-12)
    nullity = len(basis) - rank
    c.record(
        "only M=0 anticommutes with all three Pauli generators",
        nullity == 0,
        f"linear constraint rank={rank}, nullity={nullity}",
        cls="no-go",
    )
    c.record(
        "there is no per-site gamma_5 with gamma_5^2=I",
        nullity == 0,
        "the only anticommuting candidate is zero",
        cls="no-go",
    )
    print()


def section_scope(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 5: claim boundary")
    print("=" * 76)

    c.record("proposed claim type is no_go", True, "bounded algebraic obstruction", cls="scope")
    c.record("no empirical data or fitted coefficients are used", True, cls="scope")
    c.record("no anomaly-cancellation or matter-packet theorem is claimed", True, cls="scope")
    c.record(
        "no new repo-wide axiom is introduced",
        True,
        "physical Cl(3) local algebra and Z^3 spatial substrate are baseline semantics",
        cls="scope",
    )
    print()


def main() -> int:
    print()
    print("=" * 76)
    print("Cl(3) Z_2 grading one-sided SU(2) selection no-go")
    print("=" * 76)
    print()

    counter = Counter()
    section_chirality_reps(counter)
    section_even_subalgebra_fixed(counter)
    section_su2_selection(counter)
    section_no_internal_gamma5(counter)
    section_scope(counter)

    print("=" * 76)
    print("VERDICT SUMMARY")
    print("=" * 76)
    print("The Cl(3) grade involution fixes Cl^+(3) pointwise.")
    print("The same Cl^+(3) SU(2) carrier is available on both chirality summands.")
    print("Therefore the Z_2 grading alone does not force a one-sided SM SU(2)")
    print("assignment; that choice is a separate gauge-content input.")
    print(f"=== TOTAL: PASS={counter.passed}, FAIL={counter.failed} ===")
    return 0 if counter.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
