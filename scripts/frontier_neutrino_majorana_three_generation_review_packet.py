#!/usr/bin/env python3
"""
Self-contained three-generation reviewer packet for the neutrino Majorana lane.

Question:
  Does the retained three-generation matter surface, including inter-generation
  mixing and neutral spectator dressing, reopen a nonzero right-handed
  Majorana texture on the current Cl(3) on Z^3 stack?

Answer on the current retained stack:
  No. The retained three-generation right-handed Majorana texture space is the
  six-dimensional symmetric space Sym^2(C^3) on the nu_R triplet, but every
  texture entry carries fermion-number charge -2. The retained finite normal
  grammar preserves exact fermion-number U(1), so every texture entry and
  every neutral-spectator-dressed entry vanish exactly. Therefore

      M_R,current = 0_(3x3).

Boundary:
  Exact current-stack theorem only. This does not rule out a genuinely new
  charge-2 primitive or a new observable grammar beyond the retained
  normal/determinant stack.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def null_space(matrix: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    _, s, vh = np.linalg.svd(matrix, full_matrices=False)
    rank = int(np.sum(s > tol))
    return vh.conj().T[:, rank:]


def build_dirac_data() -> tuple[np.ndarray, np.ndarray, list[np.ndarray], list[np.ndarray]]:
    i2 = np.eye(2, dtype=complex)
    z2 = np.zeros((2, 2), dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)

    g0 = np.block([[i2, z2], [z2, -i2]])
    g1 = np.block([[z2, sx], [-sx, z2]])
    g2 = np.block([[z2, sy], [-sy, z2]])
    g3 = np.block([[z2, sz], [-sz, z2]])
    gammas = [g0, g1, g2, g3]
    g5 = 1j * g0 @ g1 @ g2 @ g3
    cmat = 1j * g2 @ g0
    pr = (np.eye(4, dtype=complex) + g5) / 2.0

    lorentz = []
    for mu in range(4):
        for nu in range(mu + 1, 4):
            lorentz.append(0.25 * (gammas[mu] @ gammas[nu] - gammas[nu] @ gammas[mu]))

    basis = [np.eye(4, dtype=complex)]
    basis.extend(gammas)
    for mu in range(4):
        for nu in range(mu + 1, 4):
            basis.append(0.5 * (gammas[mu] @ gammas[nu] - gammas[nu] @ gammas[mu]))
    basis.append(g5)
    basis.extend(gamma @ g5 for gamma in gammas)
    return cmat, pr, lorentz, basis


def build_internal_generators() -> list[np.ndarray]:
    n = 16
    generators: list[np.ndarray] = []

    lam = []
    lam.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
    lam.append((1.0 / np.sqrt(3.0)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex))

    for matrix in lam:
        gen = np.zeros((n, n), dtype=complex)
        t = matrix / 2.0
        gen[0:3, 0:3] = t
        gen[3:6, 3:6] = t
        gen[8:11, 8:11] = t
        gen[11:14, 11:14] = t
        generators.append(gen)

    sx = np.array([[0, 1], [1, 0]], dtype=complex) / 2.0
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex) / 2.0
    sz = np.array([[1, 0], [0, -1]], dtype=complex) / 2.0
    i3 = np.eye(3, dtype=complex)

    for s in [sx, sy, sz]:
        gen = np.zeros((n, n), dtype=complex)
        gen[0:6, 0:6] = np.kron(s, i3)
        gen[6:8, 6:8] = s
        generators.append(gen)

    y = np.diag([1 / 3] * 6 + [-1] * 2 + [4 / 3] * 3 + [-2 / 3] * 3 + [-2] + [0]).astype(complex)
    generators.append(y)
    return generators


def symmetric_basis(n: int) -> list[np.ndarray]:
    basis: list[np.ndarray] = []
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
    return basis


def invariant_nu_r_template() -> tuple[np.ndarray, np.ndarray]:
    cmat, pr, lorentz, basis = build_dirac_data()
    columns = []
    for gamma in basis:
        bilinear = cmat @ gamma
        residual = []
        for generator in lorentz:
            residual.append((generator.T @ bilinear + bilinear @ generator).reshape(-1))
        columns.append(np.concatenate(residual))
    spinor_ns = null_space(np.column_stack(columns))
    b_r = cmat @ pr
    b_r_res = max(np.linalg.norm(s.T @ b_r + b_r @ s) for s in lorentz)

    check("C P_R is a nonzero Lorentz-invariant same-chirality form", np.linalg.norm(b_r) > 1e-10 and b_r_res < 1e-10,
          f"norm={np.linalg.norm(b_r):.3f}, residual={b_r_res:.2e}")
    check("Lorentz-invariant psi^T B psi space has dimension 2 before chirality fixing", spinor_ns.shape[1] == 2,
          f"dim={spinor_ns.shape[1]}")
    check("C P_R is antisymmetric", np.linalg.norm(b_r.T + b_r) < 1e-10,
          f"antisym err={np.linalg.norm(b_r.T + b_r):.2e}")

    generators = build_internal_generators()
    basis_internal = symmetric_basis(16)
    columns = []
    for matrix in basis_internal:
        residual = []
        for generator in generators:
            residual.append((generator.T @ matrix + matrix @ generator).reshape(-1))
        columns.append(np.concatenate(residual))
    internal_ns = null_space(np.column_stack(columns))
    coeffs = internal_ns[:, 0]
    invariant = sum(c * m for c, m in zip(coeffs, basis_internal))
    template = np.zeros((16, 16), dtype=complex)
    template[15, 15] = invariant[15, 15]
    support_residual = np.linalg.norm(invariant - template)

    check("One-generation symmetric internal invariant space has dimension 1", internal_ns.shape[1] == 1,
          f"dim={internal_ns.shape[1]}")
    check("The unique one-generation support is the nu_R nu_R slot", support_residual < 1e-10,
          f"off-slot norm={support_residual:.2e}")
    return b_r, template


def classify_three_generation_texture_space() -> tuple[np.ndarray, list[np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 1: THE RETAINED THREE-GENERATION MAJORANA TEXTURE SPACE IS SYM^2(C^3)")
    print("=" * 88)

    b_r, template = invariant_nu_r_template()
    generators_3g = [np.kron(np.eye(3, dtype=complex), gen) for gen in build_internal_generators()]
    gen_basis = symmetric_basis(3)
    texture_basis = [np.kron(gb, template) for gb in gen_basis]

    max_err = 0.0
    for candidate in texture_basis:
        candidate_err = max(np.linalg.norm(gen.T @ candidate + candidate @ gen) for gen in generators_3g)
        max_err = max(max_err, candidate_err)

    basis_rank = np.linalg.matrix_rank(np.column_stack([candidate.reshape(-1) for candidate in texture_basis]), tol=1e-10)
    diag_channel = np.kron(b_r, texture_basis[0])
    offdiag_channel = np.kron(b_r, texture_basis[3])

    check("The symmetric 3x3 generation space contributes 6 basis matrices", len(gen_basis) == 6)
    check("Every lifted Sym^2(C^3) channel is gauge-invariant on the full 3-generation surface", max_err < 1e-10,
          f"max residual={max_err:.2e}")
    check("The retained 3-generation texture space has dimension 6", basis_rank == 6,
          f"rank={basis_rank}")
    check("Diagonal flavor channels remain antisymmetric after spinor contraction", np.linalg.norm(diag_channel.T + diag_channel) < 1e-10,
          f"antisym err={np.linalg.norm(diag_channel.T + diag_channel):.2e}")
    check("Off-diagonal flavor channels also remain antisymmetric after spinor contraction", np.linalg.norm(offdiag_channel.T + offdiag_channel) < 1e-10,
          f"antisym err={np.linalg.norm(offdiag_channel.T + offdiag_channel):.2e}")
    check("Diagonal and off-diagonal channels are both nontrivial", np.linalg.matrix_rank(diag_channel, tol=1e-10) == 2 and np.linalg.matrix_rank(offdiag_channel, tol=1e-10) == 4,
          f"ranks=({np.linalg.matrix_rank(diag_channel, tol=1e-10)},{np.linalg.matrix_rank(offdiag_channel, tol=1e-10)})")

    print()
    print("  The retained three-generation right-handed Majorana texture space is")
    print("  the symmetric 3 x 3 flavor space on the nu_R triplet, not a unique")
    print("  one-parameter lane. The current stack question is therefore whether")
    print("  the retained grammar activates any of those six entries.")
    return template, gen_basis


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


def gibbs_state(h: np.ndarray, beta: float) -> np.ndarray:
    evals, vecs = np.linalg.eigh(hermitian(h))
    weights = np.exp(-beta * (evals - np.min(evals)))
    rho = vecs @ np.diag(weights) @ vecs.conj().T
    return rho / np.trace(rho)


def expect(rho: np.ndarray, op: np.ndarray) -> complex:
    return complex(np.trace(rho @ op))


def majorana_channel(cs: list[np.ndarray], i: int, j: int) -> np.ndarray:
    ai, bi = 2 * i, 2 * i + 1
    aj, bj = 2 * j, 2 * j + 1
    if i == j:
        return monomial(cs, [], [ai, bi])
    return (monomial(cs, [], [ai, bj]) - monomial(cs, [], [bi, aj])) / np.sqrt(2.0)


def current_three_generation_zero_matrix() -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: INTER-GENERATION MIXING AND NEUTRAL SPECTATORS STILL GIVE ZERO")
    print("=" * 88)

    cs = annihilation_operators(8)
    n_tot = number_operator(cs)
    occupancies = [c.conj().T @ c for c in cs]

    normal_terms = [
        0.31 * hermitian(monomial(cs, [0], [2])),
        -0.27 * hermitian(monomial(cs, [1], [3])),
        0.22 * hermitian(monomial(cs, [2], [4])),
        0.18 * hermitian(monomial(cs, [3], [5])),
        0.25 * hermitian(monomial(cs, [0], [6])),
        -0.21 * hermitian(monomial(cs, [5], [7])),
        0.17 * hermitian(monomial(cs, [6], [7])),
        0.14 * occupancies[0] - 0.09 * occupancies[1] + 0.07 * occupancies[2] + 0.05 * occupancies[3],
        -0.04 * occupancies[4] + 0.03 * occupancies[5] + 0.11 * occupancies[6] - 0.06 * occupancies[7],
        0.13 * (occupancies[0] @ occupancies[6]) - 0.08 * (occupancies[3] @ occupancies[7]) + 0.05 * (occupancies[1] @ occupancies[2]),
    ]
    h_normal = sum(normal_terms)
    rho = gibbs_state(h_normal, beta=0.9)

    mix_ev = expect(rho, hermitian(monomial(cs, [0], [2])))
    spectator_mix_ev = expect(rho, hermitian(monomial(cs, [0], [6])))

    channels: dict[tuple[int, int], np.ndarray] = {}
    texture = np.zeros((3, 3), dtype=complex)
    dressed_texture = np.zeros((3, 3), dtype=complex)
    max_charge_err = 0.0
    max_pair_ev = 0.0
    max_dressed_ev = 0.0

    neutral_spectator = (
        occupancies[6]
        + 0.7 * occupancies[7]
        + 0.2 * (occupancies[0] @ occupancies[6])
        + 0.1 * hermitian(monomial(cs, [6], [7]))
    )

    for i in range(3):
        for j in range(i, 3):
            channel = majorana_channel(cs, i, j)
            charge_err = np.linalg.norm((n_tot @ channel - channel @ n_tot) + 2.0 * channel)
            pair_ev = expect(rho, channel)
            dressed_ev = expect(rho, neutral_spectator @ channel)
            channels[(i, j)] = channel
            texture[i, j] = pair_ev
            texture[j, i] = pair_ev
            dressed_texture[i, j] = dressed_ev
            dressed_texture[j, i] = dressed_ev
            max_charge_err = max(max_charge_err, charge_err)
            max_pair_ev = max(max_pair_ev, abs(pair_ev))
            max_dressed_ev = max(max_dressed_ev, abs(dressed_ev))

    h_comm = np.linalg.norm(h_normal @ n_tot - n_tot @ h_normal)
    rho_comm = np.linalg.norm(rho @ n_tot - n_tot @ rho)
    spectator_charge = np.linalg.norm(n_tot @ neutral_spectator - neutral_spectator @ n_tot)
    neutral_ev = expect(rho, neutral_spectator)

    check("The retained test Hamiltonian has exact fermion-number U(1)", h_comm < 1e-12,
          f"||[H,N]||={h_comm:.2e}")
    check("The finite Gibbs state remains U(1)-invariant", rho_comm < 1e-12,
          f"||[rho,N]||={rho_comm:.2e}")
    check("The test state has genuine inter-generation normal mixing", abs(mix_ev) > 1e-3,
          f"<nu1^dag nu2 + h.c.>={mix_ev.real:.6f}")
    check("The test state also has genuine neutral spectator coupling", abs(spectator_mix_ev) > 1e-3,
          f"<nu1^dag s + h.c.>={spectator_mix_ev.real:.6f}")
    check("Every three-generation Majorana texture entry carries charge -2", max_charge_err < 1e-10,
          f"max charge residual={max_charge_err:.2e}")
    check("Every retained-stack texture entry vanishes exactly", max_pair_ev < 1e-12,
          f"max |<S_ij>|={max_pair_ev:.2e}")
    check("Neutral spectator dressing leaves the Majorana texture identically zero", spectator_charge < 1e-12 and max_dressed_ev < 1e-12,
          f"||[N,F0]||={spectator_charge:.2e}, max |<F0 S_ij>|={max_dressed_ev:.2e}")
    check("Neutral spectator observables themselves remain nontrivial", abs(neutral_ev) > 1e-4,
          f"<F0>={neutral_ev.real:.6f}")
    check("The full retained three-generation Majorana matrix is exactly zero", np.linalg.norm(texture) < 1e-12,
          f"||M_R,current||_F={np.linalg.norm(texture):.2e}")
    check("The full neutral-spectator-dressed response matrix is also zero", np.linalg.norm(dressed_texture) < 1e-12,
          f"||M_R,dressed||_F={np.linalg.norm(dressed_texture):.2e}")

    print()
    print("  So neither inter-generation mixing nor charge-zero spectator")
    print("  structure changes the retained answer. They remain inside the same")
    print("  fermion-number-neutral grammar, and every Majorana entry still")
    print("  vanishes exactly.")
    return texture, dressed_texture


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: THREE-GENERATION REVIEW PACKET")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Framework axiom")
    print("  - Observable principle")
    print("  - Anomaly-forced 3+1")
    print("  - One-generation matter closure")
    print("  - Three-generation matter structure")
    print("  - Generation axiom boundary")
    print()
    print("Question:")
    print("  Does the retained three-generation matter surface, including")
    print("  inter-generation mixing and neutral spectator dressing, reopen")
    print("  a nonzero right-handed Majorana texture on the current stack?")

    classify_three_generation_texture_space()
    texture, dressed_texture = current_three_generation_zero_matrix()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-stack answer on the retained 3-generation surface:")
    print("    - allowed RH-Majorana texture space: Sym^2(C^3) on the nu_R triplet")
    print(f"    - current retained-stack matrix norm ||M_R,current||_F: {np.linalg.norm(texture):.1f}")
    print(f"    - neutral-spectator-dressed matrix norm ||M_R,dressed||_F: {np.linalg.norm(dressed_texture):.1f}")
    print("    - exact current law: M_R,current = 0_(3x3)")
    print()
    print("  Any future nonzero entry requires a genuinely new axiom-side")
    print("  fermionic charge-2 primitive outside the retained normal/")
    print("  determinant stack.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
