#!/usr/bin/env python3
"""Audit-grade native gauge closure runner.

Authority boundary:
  - prove the native cubic Cl(3) / SU(2) algebra directly;
  - verify that the graph-first selector and SU(3) integration rows are
    audit-ratified in the current audit ledger;
  - check only the bounded left-handed abelian eigenvalue surface.

This runner intentionally excludes the old exploratory coloring, internal
cycle, random Wilson-loop, and "SU(3) from tastes alone" probes. Those were
not the retained graph-first SU(3) theorem and should not be authority for
`docs/NATIVE_GAUGE_CLOSURE_NOTE.md`.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

TOL = 1.0e-10
PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def close(a: np.ndarray, b: np.ndarray, tol: float = TOL) -> bool:
    return np.linalg.norm(a - b) < tol


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
I8 = np.eye(8, dtype=complex)


def clifford_generators() -> list[np.ndarray]:
    """Three staggered-taste gamma matrices for the cubic Cl(3) surface."""
    return [
        kron3(SX, I2, I2),
        kron3(SY, SX, I2),
        kron3(SY, SY, SX),
    ]


def verify_native_clifford_su2() -> None:
    print("\n" + "=" * 76)
    print("NATIVE CUBIC Cl(3) / SU(2)")
    print("=" * 76)

    gammas = clifford_generators()

    print("\nClifford algebra")
    for i, gamma in enumerate(gammas, start=1):
        check(f"Gamma_{i} is Hermitian", close(gamma, gamma.conj().T))
        check(f"Gamma_{i}^2 = I_8", close(gamma @ gamma, I8))
    for i in range(3):
        for j in range(i, 3):
            expected = 2.0 * I8 if i == j else np.zeros((8, 8), dtype=complex)
            err = np.linalg.norm(anticommutator(gammas[i], gammas[j]) - expected)
            check(
                f"{{Gamma_{i + 1}, Gamma_{j + 1}}} = 2 delta_ij I_8",
                err < TOL,
                detail=f"err={err:.2e}",
            )

    print("\nSpin SU(2) from Clifford bivectors")
    s1 = -0.5j * gammas[1] @ gammas[2]
    s2 = -0.5j * gammas[2] @ gammas[0]
    s3 = -0.5j * gammas[0] @ gammas[1]
    spin = [s1, s2, s3]

    for i, s in enumerate(spin, start=1):
        check(f"S_{i} is Hermitian", close(s, s.conj().T))
    check("[S_1, S_2] = i S_3", close(commutator(s1, s2), 1j * s3))
    check("[S_2, S_3] = i S_1", close(commutator(s2, s3), 1j * s1))
    check("[S_3, S_1] = i S_2", close(commutator(s3, s1), 1j * s2))

    spin_casimir = s1 @ s1 + s2 @ s2 + s3 @ s3
    spin_casimir_err = np.linalg.norm(spin_casimir - 0.75 * I8)
    check("Spin Casimir S^2 = 3/4 I_8", spin_casimir_err < TOL, detail=f"err={spin_casimir_err:.2e}")

    print("\nWeak/isospin SU(2) on one cubic taste factor")
    t1 = 0.5 * kron3(SX, I2, I2)
    t2 = 0.5 * kron3(SY, I2, I2)
    t3 = 0.5 * kron3(SZ, I2, I2)
    check("[T_1, T_2] = i T_3", close(commutator(t1, t2), 1j * t3))
    check("[T_2, T_3] = i T_1", close(commutator(t2, t3), 1j * t1))
    check("[T_3, T_1] = i T_2", close(commutator(t3, t1), 1j * t2))
    taste_casimir = t1 @ t1 + t2 @ t2 + t3 @ t3
    taste_casimir_err = np.linalg.norm(taste_casimir - 0.75 * I8)
    check("Taste/isospin Casimir T^2 = 3/4 I_8", taste_casimir_err < TOL, detail=f"err={taste_casimir_err:.2e}")


def site_index(side: int, x: int, y: int, z: int) -> int:
    return x * side * side + y * side + z


def verify_cubic_chiral_parity(side: int = 4) -> None:
    print("\n" + "=" * 76)
    print("CUBIC PARITY / CHIRAL CHECK")
    print("=" * 76)

    n = side**3
    hop = np.zeros((n, n), dtype=complex)
    parity = np.zeros(n, dtype=float)

    for x in range(side):
        for y in range(side):
            for z in range(side):
                i = site_index(side, x, y, z)
                parity[i] = 1.0 if (x + y + z) % 2 == 0 else -1.0

                if x + 1 < side:
                    j = site_index(side, x + 1, y, z)
                    hop[i, j] = 1.0
                    hop[j, i] = 1.0
                if y + 1 < side:
                    j = site_index(side, x, y + 1, z)
                    eta_y = -1.0 if x % 2 else 1.0
                    hop[i, j] = eta_y
                    hop[j, i] = eta_y
                if z + 1 < side:
                    j = site_index(side, x, y, z + 1)
                    eta_z = -1.0 if (x + y) % 2 else 1.0
                    hop[i, j] = eta_z
                    hop[j, i] = eta_z

    p = np.diag(parity)
    check("Parity P^2 = I on the finite cubic graph", close(p @ p, np.eye(n)))
    anti_err = np.linalg.norm(hop @ p + p @ hop)
    check("{H_hop, P} = 0 for nearest-neighbor cubic hopping", anti_err < TOL, detail=f"err={anti_err:.2e}")


def load_ledger_rows() -> dict:
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)["rows"]


def verify_retained_graph_first_dependencies() -> None:
    print("\n" + "=" * 76)
    print("RETAINED GRAPH-FIRST DEPENDENCIES")
    print("=" * 76)

    rows = load_ledger_rows()
    native = rows["native_gauge_closure_note"]
    expected_deps = {
        "graph_first_selector_derivation_note",
        "graph_first_su3_integration_note",
    }
    native_deps = set(native.get("deps", []))
    check(
        "Native gauge note cites selector and SU(3) graph-first dependencies",
        expected_deps.issubset(native_deps),
        detail=f"deps={sorted(native_deps)}",
    )

    required = {
        "graph_first_selector_derivation_note": "scripts/frontier_graph_first_selector_derivation.py",
        "graph_first_su3_integration_note": "scripts/frontier_graph_first_su3_integration.py",
    }
    for claim_id, runner in required.items():
        row = rows[claim_id]
        check(f"{claim_id} audit_status = audited_clean", row.get("audit_status") == "audited_clean")
        check(f"{claim_id} effective_status = retained", row.get("effective_status") == "retained")
        check(f"{claim_id} runner path registered", row.get("runner_path") == runner, detail=str(row.get("runner_path")))
        check(f"{claim_id} runner exists", (REPO_ROOT / runner).exists())


def cube_basis() -> list[tuple[int, int, int]]:
    return [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]


def cube_index() -> dict[tuple[int, int, int], int]:
    return {bits: i for i, bits in enumerate(cube_basis())}


def residual_swap(axis: int) -> np.ndarray:
    idx = cube_index()
    others = [i for i in range(3) if i != axis]
    a, b = others
    op = np.zeros((8, 8), dtype=complex)
    for bits, i in idx.items():
        swapped = list(bits)
        swapped[a], swapped[b] = swapped[b], swapped[a]
        op[idx[tuple(swapped)], i] = 1.0
    return op


def verify_bounded_abelian_surface() -> None:
    print("\n" + "=" * 76)
    print("BOUNDED LEFT-HANDED ABELIAN SURFACE")
    print("=" * 76)

    for axis in range(3):
        tau = residual_swap(axis)
        pi_plus = (I8 + tau) / 2.0
        pi_minus = (I8 - tau) / 2.0
        y_like = (1.0 / 3.0) * pi_plus - pi_minus
        eigs = np.linalg.eigvalsh(y_like.real)

        print(f"\nSelected axis {axis + 1}")
        check("rank Pi_+ = 6", np.linalg.matrix_rank(pi_plus, tol=TOL) == 6)
        check("rank Pi_- = 2", np.linalg.matrix_rank(pi_minus, tol=TOL) == 2)
        check("Y_like is Hermitian", close(y_like, y_like.conj().T))
        check("Tr Y_like = 0", abs(np.trace(y_like)) < TOL)
        check("Y_like eigenvalue +1/3 has multiplicity 6", int(np.sum(np.abs(eigs - 1.0 / 3.0) < 1e-8)) == 6)
        check("Y_like eigenvalue -1 has multiplicity 2", int(np.sum(np.abs(eigs + 1.0) < 1e-8)) == 2)

    print("\nBoundary reminder")
    print("  This runner checks only the left-handed +1/3 / -1 eigenvalue surface.")
    print("  It does not assert anomaly-complete U(1)_Y or downstream phenomenology.")


def main() -> int:
    print("=" * 76)
    print("NATIVE GRAPH-FIRST GAUGE CLOSURE")
    print("=" * 76)

    verify_native_clifford_su2()
    verify_cubic_chiral_parity()
    verify_retained_graph_first_dependencies()
    verify_bounded_abelian_surface()

    print("\n" + "=" * 76)
    print("SUMMARY")
    print("=" * 76)
    print("  Exact native cubic Cl(3) / SU(2): checked directly.")
    print("  Graph-first selector and structural SU(3): checked as audit-ratified dependencies.")
    print("  Abelian factor: bounded to the left-handed +1/3 / -1 eigenvalue surface.")

    if FAIL:
        print(f"\nPASS={PASS} FAIL={FAIL}")
        return 1
    print(f"\nPASS={PASS} FAIL=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
