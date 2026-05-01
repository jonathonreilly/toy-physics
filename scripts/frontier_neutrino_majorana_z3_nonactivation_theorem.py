#!/usr/bin/env python3
"""
Three-generation / Z3 non-activation theorem for the Majorana lane.

Question:
  Once the one-generation Majorana slot is lifted to a three-generation
  texture, can the retained three-generation / Z3 structure itself activate
  the missing Majorana sector on the current stack?

Answer:
  No.

Exact statement:
  For any symmetric three-generation coefficient matrix M, the canonical
  pairing block

      Delta(M) = M (x) J_2

  still defines a charge-minus-two operator on the finite fermionic surface.
  In particular, the usual Z3 texture

      M_Z3 = [[A, 0, 0], [0, eps, B], [0, B, eps]]

  remains in the same charge-minus-two sector. Therefore the exact U(1)
  selection rule on the retained finite normal grammar forces its expectation
  to vanish. Generation structure and Z3 can shape a Majorana matrix once a
  pairing sector is admitted; they cannot activate that sector from the
  current charge-zero grammar.

Boundary:
  This is an exact non-activation theorem on the current finite retained stack.
  It does NOT rule out a future genuinely new charge-two primitive or a future
  axiom-side activation law beyond the retained normal grammar.
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


def hermitian(op: np.ndarray) -> np.ndarray:
    return 0.5 * (op + op.conj().T)


def gibbs_state(h: np.ndarray, beta: float) -> np.ndarray:
    evals, vecs = np.linalg.eigh(hermitian(h))
    weights = np.exp(-beta * (evals - np.min(evals)))
    rho = vecs @ np.diag(weights) @ vecs.conj().T
    return rho / np.trace(rho)


def pair_operator_from_delta(delta: np.ndarray, cs: list[np.ndarray]) -> np.ndarray:
    n = len(cs)
    out = np.zeros_like(cs[0])
    for a in range(n):
        for b in range(a + 1, n):
            out += delta[a, b] * (cs[a] @ cs[b])
    return out


def z3_texture(a: complex, b: complex, eps: complex) -> np.ndarray:
    return np.array(
        [[a, 0.0, 0.0], [0.0, eps, b], [0.0, b, eps]],
        dtype=complex,
    )


def test_generation_texture_lives_in_pairing_sector() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE THREE-GENERATION / Z3 TEXTURE IS STILL A CHARGE-MINUS-TWO PAIRING BLOCK")
    print("=" * 88)

    cs = annihilation_operators(6)
    n_tot = number_operator(cs)
    j2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)

    m_generic = np.array(
        [
            [0.50, 0.10 + 0.05j, -0.07],
            [0.10 + 0.05j, 0.90, 0.20j],
            [-0.07, 0.20j, 1.20],
        ],
        dtype=complex,
    )
    m_z3 = z3_texture(1.10, 0.40, 0.07 + 0.03j)

    delta_generic = np.kron(m_generic, j2)
    delta_z3 = np.kron(m_z3, j2)

    q_generic = pair_operator_from_delta(delta_generic, cs)
    q_z3 = pair_operator_from_delta(delta_z3, cs)

    generic_antisym = np.linalg.norm(delta_generic + delta_generic.T)
    z3_antisym = np.linalg.norm(delta_z3 + delta_z3.T)
    generic_charge = np.linalg.norm(n_tot @ q_generic - q_generic @ n_tot + 2.0 * q_generic)
    z3_charge = np.linalg.norm(n_tot @ q_z3 - q_z3 @ n_tot + 2.0 * q_z3)

    eigs_z3 = np.linalg.eigvals(m_z3)
    target_eigs = np.array([1.10, 0.07 + 0.03j + 0.40, 0.07 + 0.03j - 0.40], dtype=complex)
    eig_err = np.linalg.norm(np.sort_complex(eigs_z3) - np.sort_complex(target_eigs))

    check("Generic symmetric generation matrix gives an antisymmetric pairing block", generic_antisym < 1e-10,
          f"||Delta+Delta^T||={generic_antisym:.2e}")
    check("Z3 A/B/eps texture gives an antisymmetric pairing block", z3_antisym < 1e-10,
          f"||Delta+Delta^T||={z3_antisym:.2e}")
    check("Generic three-generation pairing operator has charge -2", generic_charge < 1e-10,
          f"charge error={generic_charge:.2e}")
    check("Z3-textured pairing operator has charge -2", z3_charge < 1e-10,
          f"charge error={z3_charge:.2e}")
    check("Z3 texture organizes one singlet and one doublet pair of eigenvalues", eig_err < 1e-10,
          f"eigenvalue error={eig_err:.2e}")

    print()
    print("  So the three-generation / Z3 lift changes the internal texture, not")
    print("  the fermion-number charge sector. It remains a charge-minus-two object.")

    return n_tot, q_generic, q_z3, cs[0].conj().T @ cs[0]


def test_normal_grammar_cannot_activate_generation_texture(
    n_tot: np.ndarray,
    q_generic: np.ndarray,
    q_z3: np.ndarray,
    n0: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: THE RETAINED NORMAL GRAMMAR KILLS THE THREE-GENERATION TEXTURE TOO")
    print("=" * 88)

    cs = annihilation_operators(6)
    n = [c.conj().T @ c for c in cs]
    hop = cs[0].conj().T @ cs[2] + cs[1].conj().T @ cs[3] + cs[2].conj().T @ cs[4] + cs[3].conj().T @ cs[5]
    scatter = (cs[0].conj().T @ cs[2]) @ (cs[3].conj().T @ cs[1])

    h_normal = (
        0.31 * hermitian(hop)
        - 0.09 * hermitian(scatter)
        + 0.07 * n[0]
        - 0.05 * n[1]
        + 0.11 * n[4]
        + 0.06 * (n[0] @ n[1])
        + 0.04 * (n[2] @ n[3])
        + 0.03 * (n[4] @ n[5])
    )

    rho = gibbs_state(h_normal, beta=0.8)
    rho_comm = np.linalg.norm(n_tot @ rho - rho @ n_tot)
    ev_generic = np.trace(rho @ q_generic)
    ev_z3 = np.trace(rho @ q_z3)
    density_ev = np.trace(rho @ n0)

    check("Finite Gibbs state on the retained six-mode normal grammar is U(1)-invariant", rho_comm < 1e-10,
          f"||[N,rho]||={rho_comm:.2e}")
    check("Generic three-generation pairing expectation vanishes on the retained grammar", abs(ev_generic) < 1e-10,
          f"<Q_generic>={ev_generic.real:+.2e}{ev_generic.imag:+.2e}i")
    check("Z3-textured pairing expectation vanishes on the retained grammar", abs(ev_z3) < 1e-10,
          f"<Q_Z3>={ev_z3.real:+.2e}{ev_z3.imag:+.2e}i")
    check("Charge-zero observables remain nontrivial on the same state", abs(density_ev) > 1e-4,
          f"<n0>={density_ev.real:.6f}")

    print()
    print("  So promoting the one-generation slot to a three-generation texture")
    print("  does not evade the exact finite-grammar U(1) selection rule.")

    return h_normal, rho


def test_texture_shapes_after_activation_but_does_not_cause_it(
    h_normal: np.ndarray,
    q_generic: np.ndarray,
    q_z3: np.ndarray,
    n_tot: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: TEXTURE SHAPES AN ADMITTED PAIRING SECTOR AFTER ACTIVATION")
    print("=" * 88)

    lam = 0.08
    h_z3 = h_normal + lam * (q_z3 + q_z3.conj().T)
    h_generic = h_normal + lam * (q_generic + q_generic.conj().T)

    rho_z3 = gibbs_state(h_z3, beta=0.8)
    rho_generic = gibbs_state(h_generic, beta=0.8)

    broken_z3 = np.linalg.norm(n_tot @ h_z3 - h_z3 @ n_tot)
    broken_generic = np.linalg.norm(n_tot @ h_generic - h_generic @ n_tot)
    ev_z3 = np.trace(rho_z3 @ q_z3)
    ev_generic = np.trace(rho_generic @ q_generic)

    check("Explicit Z3 pairing insertion breaks the retained U(1)", broken_z3 > 1e-8,
          f"||[N,H_z3]||={broken_z3:.2e}")
    check("Explicit generic pairing insertion also breaks the retained U(1)", broken_generic > 1e-8,
          f"||[N,H_generic]||={broken_generic:.2e}")
    check("After explicit activation, the Z3-textured pairing expectation is nonzero", abs(ev_z3) > 1e-4,
          f"<Q_Z3>={ev_z3.real:+.6f}{ev_z3.imag:+.6f}i")
    check("After explicit activation, the generic pairing expectation is nonzero", abs(ev_generic) > 1e-4,
          f"<Q_generic>={ev_generic.real:+.6f}{ev_generic.imag:+.6f}i")
    check("Different generation textures give genuinely different activated responses", abs(ev_z3 - ev_generic) > 1e-4,
          f"|<Q_Z3>-<Q_generic>|={abs(ev_z3 - ev_generic):.6f}")

    print()
    print("  This is the exact boundary needed for DM:")
    print("  generation / Z3 structure can organize an activated Majorana sector,")
    print("  but it does not activate that sector on the current stack.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: THREE-GENERATION / Z3 NON-ACTIVATION THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: One-generation matter closure; three-generation matter structure;")
    print("          Majorana charge-two reduction; Majorana unique source slot")
    print("  - docs/NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md")
    print("  - docs/THREE_GENERATION_STRUCTURE_NOTE.md")
    print("  - docs/DM_LEPTOGENESIS_NOTE.md")
    print()
    print("Question:")
    print("  Can the retained three-generation / Z3 texture itself turn on the")
    print("  missing Majorana sector on the current finite retained stack?")

    n_tot, q_generic, q_z3, n0 = test_generation_texture_lives_in_pairing_sector()
    h_normal, _ = test_normal_grammar_cannot_activate_generation_texture(n_tot, q_generic, q_z3, n0)
    test_texture_shapes_after_activation_but_does_not_cause_it(h_normal, q_generic, q_z3, n_tot)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. The three-generation / Z3 lift remains a charge-minus-two pairing")
    print("  object, so the exact U(1) selection rule of the retained normal grammar")
    print("  still kills it. Generation structure and Z3 can shape A/B/epsilon once")
    print("  a pairing sector is admitted, but they cannot activate that sector from")
    print("  the current stack.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
