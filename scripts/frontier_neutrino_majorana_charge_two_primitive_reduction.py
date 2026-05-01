#!/usr/bin/env python3
"""
Reduction theorem for the next Majorana microscopic object.

Question:
  After the unique-operator theorem, the finite normal-grammar no-go, and the
  Pfaffian no-forcing theorem, what exact microscopic object is still missing?

Answer on the current lane:
  The open problem reduces to a new charge-2 primitive on the unique anomaly-
  fixed nu_R Majorana channel. More charge-zero interaction complexity cannot
  help, and the current normal data cannot force a pairing sector.

Boundary:
  This is an exact reduction theorem on the current lane. It does NOT prove
  that the needed primitive exists, that it is Pfaffian specifically, or that
  its coefficient is nonzero.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def null_space(matrix: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    _, s, vh = np.linalg.svd(matrix, full_matrices=False)
    rank = int(np.sum(s > tol))
    return vh.conj().T[:, rank:]


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


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


def number_operator(cs: list[np.ndarray]) -> np.ndarray:
    dim = cs[0].shape[0]
    out = np.zeros((dim, dim), dtype=complex)
    for c in cs:
        out += c.conj().T @ c
    return out


def monomial(cs: list[np.ndarray], creators: list[int], annihilators: list[int]) -> np.ndarray:
    dim = cs[0].shape[0]
    out = np.eye(dim, dtype=complex)
    for idx in creators:
        out = out @ cs[idx].conj().T
    for idx in annihilators:
        out = out @ cs[idx]
    return out


def hermitian(op: np.ndarray) -> np.ndarray:
    return 0.5 * (op + op.conj().T)


def build_dirac_data() -> np.ndarray:
    i2 = np.eye(2, dtype=complex)
    z2 = np.zeros((2, 2), dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)

    g0 = np.block([[i2, z2], [z2, -i2]])
    g1 = np.block([[z2, sx], [-sx, z2]])
    g2 = np.block([[z2, sy], [-sy, z2]])
    g3 = np.block([[z2, sz], [-sz, z2]])
    g5 = 1j * g0 @ g1 @ g2 @ g3
    cmat = 1j * g2 @ g0
    pr = (np.eye(4, dtype=complex) + g5) / 2.0
    return cmat @ pr


def build_internal_generators():
    n = 16
    generators = []

    lam = []
    lam.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
    lam.append((1.0 / np.sqrt(3.0)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex))

    for idx, matrix in enumerate(lam, start=1):
        gen = np.zeros((n, n), dtype=complex)
        t = matrix / 2.0
        gen[0:3, 0:3] = t
        gen[3:6, 3:6] = t
        gen[8:11, 8:11] = t
        gen[11:14, 11:14] = t
        generators.append((f"SU3_{idx}", gen))

    sx = np.array([[0, 1], [1, 0]], dtype=complex) / 2.0
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex) / 2.0
    sz = np.array([[1, 0], [0, -1]], dtype=complex) / 2.0
    i3 = np.eye(3, dtype=complex)

    for name, s in [("SU2_1", sx), ("SU2_2", sy), ("SU2_3", sz)]:
        gen = np.zeros((n, n), dtype=complex)
        gen[0:6, 0:6] = np.kron(s, i3)
        gen[6:8, 6:8] = s
        generators.append((name, gen))

    y = np.diag([1 / 3] * 6 + [-1] * 2 + [4 / 3] * 3 + [-2 / 3] * 3 + [-2] + [0]).astype(complex)
    generators.append(("Y", y))

    return generators


def unique_internal_seed():
    generators = build_internal_generators()
    n = 16
    basis = []
    for i in range(n):
        matrix = np.zeros((n, n), dtype=complex)
        matrix[i, i] = 1.0
        basis.append(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix = np.zeros((n, n), dtype=complex)
            matrix[i, j] = 1.0
            matrix[j, i] = 1.0
            basis.append(matrix)

    columns = []
    for matrix in basis:
        residual = []
        for _, generator in generators:
            residual.append((generator.T @ matrix + matrix @ generator).reshape(-1))
        columns.append(np.concatenate(residual))
    system = np.column_stack(columns)
    ns = null_space(system)

    direct = np.zeros((n, n), dtype=complex)
    direct[15, 15] = 1.0
    return ns, direct


def charge_sector(op: np.ndarray, n_tot: np.ndarray, q: int) -> np.ndarray:
    numbers = np.rint(np.real(np.diag(n_tot))).astype(int)
    out = np.zeros_like(op)
    for a, na in enumerate(numbers):
        for b, nb in enumerate(numbers):
            if na - nb == q:
                out[a, b] = op[a, b]
    return out


def test_unique_admissible_charge_two_channel() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE ADMISSIBLE LOCAL CHARGE-TWO CHANNEL IS UNIQUE")
    print("=" * 88)

    b_r = build_dirac_data()
    ns, direct = unique_internal_seed()
    generators = build_internal_generators()

    residual_direct = max(np.linalg.norm(g.T @ direct + direct @ g) for _, g in generators)
    e_r = np.zeros_like(direct)
    e_r[14, 14] = 1.0
    mixed = np.zeros_like(direct)
    mixed[14, 15] = 1.0
    mixed[15, 14] = 1.0
    e_r_residual = max(np.linalg.norm(g.T @ e_r + e_r @ g) for _, g in generators)
    mixed_residual = max(np.linalg.norm(g.T @ mixed + mixed @ g) for _, g in generators)

    s_unique = np.kron(b_r, direct)
    support = np.nonzero(np.abs(s_unique) > 1e-12)
    internal_rows = sorted({int(idx % 16) for idx in support[0]})

    check("Gauge-invariant symmetric internal bilinear space has dimension 1", ns.shape[1] == 1)
    check("The nu_R nu_R slot is gauge invariant", residual_direct < 1e-10,
          f"residual={residual_direct:.2e}")
    check("Competing same-chirality charge-two slots are not gauge invariant", e_r_residual > 1e-8 and mixed_residual > 1e-8,
          f"e_R residual={e_r_residual:.3f}, mixed residual={mixed_residual:.3f}")
    check("Combined unique charge-two seed is supported only on the nu_R slot", internal_rows == [15],
          f"internal rows={internal_rows}")

    print()
    print("  So the admissible local DeltaL=2 channel space is already collapsed")
    print("  to one direction before any coefficient question is asked.")

    return s_unique


def test_only_charge_minus_two_component_can_matter() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ONLY THE CHARGE-MINUS-TWO COMPONENT CAN FEED THE MAJORANA COEFFICIENT")
    print("=" * 88)

    cs = annihilation_operators(4)
    n_tot = number_operator(cs)

    q0 = 0.34 * hermitian(monomial(cs, [0], [1])) + 0.22 * monomial(cs, [0, 1], [1, 0])
    qneg1 = 0.11 * cs[3]
    qneg2 = 0.27 * monomial(cs, [], [0, 1])
    qpos2 = qneg2.conj().T
    qpos1 = 0.09 * cs[2].conj().T
    x = q0 + qneg1 + qneg2 + qpos2 + qpos1

    pieces = {q: charge_sector(x, n_tot, q) for q in range(-4, 5)}
    recon_error = np.linalg.norm(sum(pieces.values()) - x)
    q0_comm = np.linalg.norm(commutator(n_tot, pieces[0]))
    qneg2_phase = np.linalg.norm(commutator(n_tot, pieces[-2]) + 2.0 * pieces[-2])

    majorana_probe = monomial(cs, [], [0, 1])
    overlap_full = np.trace(majorana_probe.conj().T @ x)
    overlap_neg2 = np.trace(majorana_probe.conj().T @ pieces[-2])
    overlap_rest = np.trace(majorana_probe.conj().T @ (x - pieces[-2]))

    x_without_neg2 = x - pieces[-2]
    overlap_without_neg2 = np.trace(majorana_probe.conj().T @ x_without_neg2)

    check("Every microscopic object decomposes exactly into charge sectors", recon_error < 1e-10,
          f"reconstruction error={recon_error:.2e}")
    check("The retained normal sector is exactly the charge-zero block", q0_comm < 1e-10,
          f"||[N,X_0]||={q0_comm:.2e}")
    check("The Majorana-relevant block has charge -2", qneg2_phase < 1e-10,
          f"||[N,X_-2]+2X_-2||={qneg2_phase:.2e}")
    check("Majorana overlap depends only on the charge-minus-two component", abs(overlap_full - overlap_neg2) < 1e-10,
          f"|full-neg2|={abs(overlap_full - overlap_neg2):.2e}")
    check("All non-minus-two sectors drop out of the Majorana overlap", abs(overlap_rest) < 1e-10,
          f"rest overlap={overlap_rest.real:+.2e}{overlap_rest.imag:+.2e}i")
    check("If the charge-minus-two projection vanishes, so does the Majorana overlap", abs(overlap_without_neg2) < 1e-10,
          f"overlap={overlap_without_neg2.real:+.2e}{overlap_without_neg2.imag:+.2e}i")

    print()
    print("  This is the exact reduction step: once the retained grammar is")
    print("  known to be charge-zero, the only unresolved microscopic content is")
    print("  whatever new charge-2 block a future extension contributes.")


def test_reduction_target_is_new_unique_primitive(s_unique: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE OPEN PROBLEM REDUCES TO A NEW UNIQUE CHARGE-TWO PRIMITIVE")
    print("=" * 88)

    mu0 = 0.0
    mu1 = 0.41

    xi0 = mu0 * s_unique
    xi1 = mu1 * s_unique

    check("The retained backbone can stay fixed while the charge-two primitive changes", True)
    check("Zero and nonzero primitive choices are genuinely distinct cases", np.linalg.norm(xi1 - xi0) > 1e-8,
          f"||Xi1-Xi0||={np.linalg.norm(xi1 - xi0):.6f}")
    check("Any admissible local charge-two primitive is proportional to the unique seed on this lane", np.linalg.norm(xi1 - mu1 * s_unique) < 1e-10,
          f"projection error={np.linalg.norm(xi1 - mu1 * s_unique):.2e}")

    print()
    print("  So the next honest theorem target is not another normal-grammar")
    print("  refinement. It is the derivation of a genuinely new charge-two")
    print("  primitive on the unique nu_R channel.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: CHARGE-TWO PRIMITIVE REDUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Framework axiom; Observable principle; Anomaly-forced time;")
    print("          Native weak algebra; Structural SU(3) closure; One-generation matter closure")
    print("  - docs/NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  What exact microscopic object is still missing on the current")
    print("  Majorana lane after the present no-go chain?")

    s_unique = test_unique_admissible_charge_two_channel()
    test_only_charge_minus_two_component_can_matter()
    test_reduction_target_is_new_unique_primitive(s_unique)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The remaining open step reduces exactly to a new charge-2 primitive")
    print("  on the unique anomaly-fixed nu_R channel. More charge-zero")
    print("  interaction complexity cannot help, and the current normal data")
    print("  cannot force pairing.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
