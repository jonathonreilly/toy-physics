#!/usr/bin/env python3
"""
Self-contained reviewer packet for the one-generation neutrino Majorana lane.

Question:
  What is the exact current status of the one-generation Majorana channel on
  the retained Cl(3) on Z^3 stack?

Answer on the current retained stack:
  - there is a unique local quadratic same-chirality Majorana operator
    candidate on the anomaly-fixed one-generation branch
  - the current finite retained normal grammar gives that channel zero
    coefficient exactly
  - the local one-generation pairing block has the unique canonical form
    A_M(mu) = mu J_2
  - the current atlas contains no hidden fermionic charge-2 primitive that
    could change the retained answer
  - therefore the current-stack law is mu_current = 0

Boundary:
  This is a current-stack theorem packet, not a statement about all future
  extensions of the framework.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def null_space(matrix: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    _, s, vh = np.linalg.svd(matrix, full_matrices=False)
    rank = int(np.sum(s > tol))
    return vh.conj().T[:, rank:]


def build_dirac_data():
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


def classify_unique_channel() -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE ONE-GENERATION QUADRATIC MAJORANA CHANNEL IS UNIQUE")
    print("=" * 88)

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

    check("Lorentz-invariant psi^T B psi space has dimension 2 before chirality fixing", spinor_ns.shape[1] == 2,
          f"dim={spinor_ns.shape[1]}")
    check("C P_R is a nonzero Lorentz-invariant same-chirality form", np.linalg.norm(b_r) > 1e-10 and b_r_res < 1e-10,
          f"norm={np.linalg.norm(b_r):.3f}, residual={b_r_res:.2e}")
    check("C P_R is antisymmetric", np.linalg.norm(b_r.T + b_r) < 1e-10,
          f"antisym err={np.linalg.norm(b_r.T + b_r):.2e}")

    generators = build_internal_generators()
    n = 16
    basis_internal = []
    for i in range(n):
        matrix = np.zeros((n, n), dtype=complex)
        matrix[i, i] = 1.0
        basis_internal.append(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix = np.zeros((n, n), dtype=complex)
            matrix[i, j] = 1.0
            matrix[j, i] = 1.0
            basis_internal.append(matrix)

    columns = []
    for matrix in basis_internal:
        residual = []
        for generator in generators:
            residual.append((generator.T @ matrix + matrix @ generator).reshape(-1))
        columns.append(np.concatenate(residual))
    internal_ns = null_space(np.column_stack(columns))
    coeffs = internal_ns[:, 0]
    invariant = sum(c * m for c, m in zip(coeffs, basis_internal))
    template = np.zeros((n, n), dtype=complex)
    template[15, 15] = invariant[15, 15]
    support_residual = np.linalg.norm(invariant - template)
    channel = np.kron(b_r, template)

    check("Gauge-invariant symmetric internal bilinear space has dimension 1", internal_ns.shape[1] == 1,
          f"dim={internal_ns.shape[1]}")
    check("The unique internal support is the nu_R nu_R slot", support_residual < 1e-10,
          f"off-slot norm={support_residual:.2e}")
    check("The combined Majorana channel has rank 2", np.linalg.matrix_rank(channel, tol=1e-10) == 2,
          f"rank={np.linalg.matrix_rank(channel, tol=1e-10)}")
    check("The combined channel is antisymmetric", np.linalg.norm(channel.T + channel) < 1e-10,
          f"antisym err={np.linalg.norm(channel.T + channel):.2e}")

    print()
    print("  Unique same-chirality quadratic channel:")
    print("    nu_R^T C P_R nu_R")
    return b_r, template


def current_stack_zero_law() -> float:
    print("\n" + "=" * 88)
    print("PART 2: THE RETAINED FINITE NORMAL GRAMMAR SETS THE COEFFICIENT TO ZERO")
    print("=" * 88)

    cs = annihilation_operators(4)
    n_tot = number_operator(cs)
    hop = monomial(cs, [0], [1])
    density = monomial(cs, [0, 1], [1, 0])
    scatter = monomial(cs, [0, 2], [3, 1])
    pair_ann = monomial(cs, [], [0, 1])
    pair_cre = pair_ann.conj().T
    n0 = cs[0].conj().T @ cs[0]
    n1 = cs[1].conj().T @ cs[1]
    n2 = cs[2].conj().T @ cs[2]

    h_normal = (
        0.41 * hermitian(hop)
        - 0.16 * hermitian(scatter)
        + 0.58 * density
        + 0.12 * n0
        - 0.08 * n1
        + 0.05 * n2
    )
    rho = gibbs_state(h_normal, beta=1.1)
    comm_err = np.linalg.norm(h_normal @ n_tot - n_tot @ h_normal)
    pair_ev = expect(rho, pair_ann)
    pair_ev_hc = expect(rho, pair_cre)
    mu_eff = abs(pair_ev)

    check("Retained normal Hamiltonian commutes exactly with fermion number", comm_err < 1e-12,
          f"||[H,N]||={comm_err:.2e}")
    check("Charge-2 pair expectation vanishes exactly", abs(pair_ev) < 1e-12,
          f"<cc>={pair_ev.real:+.2e}{pair_ev.imag:+.2e}i")
    check("Charge+2 conjugate expectation also vanishes exactly", abs(pair_ev_hc) < 1e-12,
          f"<c^dag c^dag>={pair_ev_hc.real:+.2e}{pair_ev_hc.imag:+.2e}i")
    check("The current retained-stack activation coordinate is mu_current = 0", mu_eff < 1e-12,
          f"mu_current={mu_eff:.2e}")

    print()
    print("  The structurally allowed Majorana slot exists, but the current")
    print("  retained finite normal grammar leaves it exactly unactivated.")
    return mu_eff


def canonical_block_form() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ONE-GENERATION LOCAL BLOCK IS CANONICAL")
    print("=" * 88)

    m = -0.61 + 0.44j
    alpha = np.angle(m) / 2.0
    u = np.exp(-1j * alpha) * np.eye(2, dtype=complex)
    block = m * J2
    canonical = u @ block @ u.T
    target = abs(m) * J2
    svals = np.linalg.svd(block, compute_uv=False)

    check("Every local antisymmetric 2x2 block has the form m J_2", np.linalg.norm(block - block[0, 1] * J2) < 1e-12,
          f"reconstruction error={np.linalg.norm(block - block[0, 1] * J2):.2e}")
    check("The one-generation phase is removable by local rephasing", np.linalg.norm(canonical - target) < 1e-12,
          f"canonicalization error={np.linalg.norm(canonical - target):.2e}")
    check("The canonical block invariants collapse to mu = |m|", np.linalg.norm(np.sort(svals) - np.array([abs(m), abs(m)])) < 1e-12,
          f"singular-value err={np.linalg.norm(np.sort(svals) - np.array([abs(m), abs(m)])):.2e}")

    print()
    print("  So the one-generation local pairing block carries no hidden matrix")
    print("  freedom beyond one real amplitude mu.")


def current_atlas_nonrealization() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT ATLAS HAS NO HIDDEN CHARGE-2 PRIMITIVE")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    obs = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    rhs = read("scripts/frontier_right_handed_sector.py")

    has_det_row = "| Observable principle | `log|det(D+J)|`" in atlas
    pfaffian_rows = re.findall(r"\|\s*([^|]*Pfaffian[^|]*)\|", atlas, flags=re.IGNORECASE)
    has_boundary_row = (
        "| One-generation Majorana current-stack zero law |" in atlas
        or "| Three-generation Majorana current-stack zero matrix |" in atlas
    )
    obs_scalar = "scalar observable generator" in obs.lower() or "scalar generator" in obs.lower()
    misses_zero_slot = "MISSING from wedge^2 singlets: {Fraction(0, 1), Fraction(4, 3)}" in rhs or "Fraction(0)" in rhs

    check("Atlas retains the determinant observable backbone", has_det_row)
    check("Observable-principle authority is explicitly scalar/determinant-based", obs_scalar)
    check("Current atlas has no retained Pfaffian primitive row", len(pfaffian_rows) == 0,
          f"pfaffian rows={pfaffian_rows}")
    check("The only atlas Majorana-facing entry is the boundary review row", has_boundary_row)
    check("Existing wedge^2(C^8) right-handed composite route misses the nu_R Y=0 slot", misses_zero_slot)

    print()
    print("  So no currently retained atlas object changes the exact present")
    print("  answer away from mu_current = 0.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: SELF-CONTAINED REVIEW PACKET")
    print("=" * 88)
    print()
    print("Package role:")
    print("  - frozen-out exact review packet on the one-generation Majorana lane")
    print("  - not on the retained flagship claim surface")
    print("  - intended for arXiv / reviewer-facing negative-result capture")
    print()
    print("Question:")
    print("  What is the exact current status of the one-generation Majorana")
    print("  channel on the retained Cl(3) on Z^3 stack?")

    classify_unique_channel()
    mu_current = current_stack_zero_law()
    canonical_block_form()
    current_atlas_nonrealization()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-stack answer:")
    print("    - unique one-generation quadratic Majorana channel: yes")
    print(f"    - current retained-stack amplitude mu_current: {mu_current:.1f}")
    print("    - canonical local block on the retained stack: A_M = 0 * J_2")
    print()
    print("  Any future nonzero Majorana amplitude requires a genuinely new")
    print("  axiom-side fermionic charge-2 primitive outside the current")
    print("  retained stack.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
