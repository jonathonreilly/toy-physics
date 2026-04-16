#!/usr/bin/env python3
"""
Finite normal-grammar no-go for a Majorana coefficient on the current lane.

Question:
  The native-Gaussian note already rules out a Majorana coefficient on the
  current quadratic determinant surface. Does the obstruction survive if the
  microscopic surface is enlarged to arbitrary finite interactions that remain
  inside the current number-preserving normal grammar?

Answer on the present surface:
  Yes. Any finite grammar built only from charge-zero monomials with equal
  counts of c and c^dag preserves exact fermion-number U(1). Therefore every
  charge-q observable with q != 0 has zero expectation in any finite invariant
  state on that grammar. The Majorana bilinear carries q = +/-2, so it still
  cannot acquire a coefficient on the retained normal surface.

Boundary:
  This is exact on the current finite retained normal grammar. It does NOT
  rule out explicit DeltaL=2 / pairing insertions, admitted Pfaffian/Nambu
  extensions, or thermodynamic-limit symmetry breaking beyond the current
  finite exact stack.
"""

from __future__ import annotations

import math
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


def rotation_from_number(n_tot: np.ndarray, theta: float) -> np.ndarray:
    evals, vecs = np.linalg.eigh(n_tot)
    phase = np.exp(1j * theta * evals)
    return vecs @ np.diag(phase) @ vecs.conj().T


def rotate(op: np.ndarray, n_tot: np.ndarray, theta: float) -> np.ndarray:
    u = rotation_from_number(n_tot, theta)
    return u @ op @ u.conj().T


def gibbs_state(h: np.ndarray, beta: float) -> np.ndarray:
    evals, vecs = np.linalg.eigh(hermitian(h))
    weights = np.exp(-beta * (evals - np.min(evals)))
    rho = vecs @ np.diag(weights) @ vecs.conj().T
    return rho / np.trace(rho)


def expect(rho: np.ndarray, op: np.ndarray) -> complex:
    return complex(np.trace(rho @ op))


def test_charge_zero_grammar_is_u1_invariant() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE RETAINED NORMAL GRAMMAR HAS EXACT FERMION-NUMBER U(1)")
    print("=" * 88)

    cs = annihilation_operators(4)
    n_tot = number_operator(cs)
    theta = math.pi / 7.0

    hop = monomial(cs, [0], [1])
    density = monomial(cs, [0, 1], [1, 0])
    scatter = monomial(cs, [0, 2], [3, 1])
    triple_density = density @ (cs[2].conj().T @ cs[2])
    pair_ann = monomial(cs, [], [0, 1])
    pair_cre = pair_ann.conj().T

    hop_comm = np.linalg.norm(commutator(n_tot, hop))
    density_comm = np.linalg.norm(commutator(n_tot, density))
    scatter_comm = np.linalg.norm(commutator(n_tot, scatter))
    triple_comm = np.linalg.norm(commutator(n_tot, triple_density))
    pair_ann_comm = np.linalg.norm(commutator(n_tot, pair_ann) + 2.0 * pair_ann)
    pair_cre_comm = np.linalg.norm(commutator(n_tot, pair_cre) - 2.0 * pair_cre)

    check("Quadratic hopping monomial has charge 0", hop_comm < 1e-10,
          f"||[N,hop]||={hop_comm:.2e}")
    check("Quartic density monomial has charge 0", density_comm < 1e-10,
          f"||[N,density]||={density_comm:.2e}")
    check("Quartic scattering monomial has charge 0", scatter_comm < 1e-10,
          f"||[N,scatter]||={scatter_comm:.2e}")
    check("Higher normal-grammar monomial still has charge 0", triple_comm < 1e-10,
          f"||[N,triple]||={triple_comm:.2e}")
    check("Majorana pair-annihilation carries charge -2", pair_ann_comm < 1e-10,
          f"||[N,cc]+2cc||={pair_ann_comm:.2e}")
    check("Majorana pair-creation carries charge +2", pair_cre_comm < 1e-10,
          f"||[N,c^dag c^dag]-2c^dag c^dag||={pair_cre_comm:.2e}")

    hop_rot = np.linalg.norm(rotate(hop, n_tot, theta) - hop)
    scatter_rot = np.linalg.norm(rotate(scatter, n_tot, theta) - scatter)
    pair_phase_err = np.linalg.norm(rotate(pair_ann, n_tot, theta) - np.exp(-2j * theta) * pair_ann)

    check("Charge-zero monomials are exactly U(1)-invariant", max(hop_rot, scatter_rot) < 1e-10,
          f"max rotation error={max(hop_rot, scatter_rot):.2e}")
    check("Majorana pair rotates with the exact e^(-2 i theta) phase", pair_phase_err < 1e-10,
          f"rotation error={pair_phase_err:.2e}")

    n0 = cs[0].conj().T @ cs[0]
    n1 = cs[1].conj().T @ cs[1]
    n2 = cs[2].conj().T @ cs[2]
    n3 = cs[3].conj().T @ cs[3]

    h_normal = (
        0.37 * hermitian(hop)
        - 0.21 * hermitian(scatter)
        + 0.63 * density
        - 0.17 * triple_density
        + 0.19 * n3
    )
    h_sourced = h_normal + 0.14 * n0 - 0.09 * n1 + 0.06 * n2 + 0.04 * density

    sourced_comm = np.linalg.norm(commutator(n_tot, h_sourced))
    check("Any finite sum of admitted charge-zero monomials still commutes with N", sourced_comm < 1e-10,
          f"||[N,H_sourced]||={sourced_comm:.2e}")

    print()
    print("  Conclusion: the retained normal grammar is the charge-zero sector.")
    print("  Adding more number-preserving interaction complexity does not leave")
    print("  that symmetry class.")

    return n_tot, h_sourced, pair_ann, density, n0


def test_selection_rule_kills_majorana_expectation(
    n_tot: np.ndarray,
    h_sourced: np.ndarray,
    pair_ann: np.ndarray,
    density: np.ndarray,
    n0: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FINITE U(1) SELECTION RULE FORCES THE MAJORANA EXPECTATION TO ZERO")
    print("=" * 88)

    beta = 0.9
    rho = gibbs_state(h_sourced, beta=beta)
    theta = math.pi / 5.0

    rho_comm = np.linalg.norm(commutator(n_tot, rho))
    pair_ev = expect(rho, pair_ann)
    density_ev = expect(rho, density)
    n0_ev = expect(rho, n0)

    rotated_pair = rotate(pair_ann, n_tot, theta)
    rotated_pair_ev = expect(rho, rotated_pair)
    rotation_identity_err = abs(rotated_pair_ev - pair_ev)
    phase_identity_err = abs(rotated_pair_ev - np.exp(-2j * theta) * pair_ev)

    neutral_pair_density = expect(rho, pair_ann.conj().T @ pair_ann)

    check("Finite Gibbs state of the retained grammar is U(1)-invariant", rho_comm < 1e-10,
          f"||[N,rho]||={rho_comm:.2e}")
    check("Charge-2 Majorana bilinear expectation vanishes exactly on the finite grammar", abs(pair_ev) < 1e-10,
          f"<cc>={pair_ev.real:+.2e}{pair_ev.imag:+.2e}i")
    check("Charge-zero observables remain nontrivial", abs(density_ev) > 1e-4 and abs(n0_ev) > 1e-4,
          f"<density>={density_ev.real:.6f}, <n0>={n0_ev.real:.6f}")
    check("Symmetry rotation leaves the Majorana expectation unchanged as a state expectation", rotation_identity_err < 1e-10,
          f"rotation identity error={rotation_identity_err:.2e}")
    check("The same expectation obeys the charge-phase relation simultaneously", phase_identity_err < 1e-10,
          f"phase identity error={phase_identity_err:.2e}")
    check("Neutral pair-density observables can still be nonzero", abs(neutral_pair_density) > 1e-4,
          f"<c^dag c^dag c c>={neutral_pair_density.real:.6f}")

    print()
    print("  So the exact finite-state selection rule is the real obstruction:")
    print("  charge-zero observables survive, but the charge-2 Majorana bilinear")
    print("  cannot acquire an expectation anywhere inside the retained grammar.")


def test_explicit_pairing_source_is_new_object() -> None:
    print("\n" + "=" * 88)
    print("PART 3: AN EXPLICIT DELTAL=2 INSERTION IS WHAT CHANGES THE RESULT")
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

    h_normal = 0.41 * hermitian(hop) - 0.16 * hermitian(scatter) + 0.58 * density + 0.12 * n0 - 0.08 * n1 + 0.05 * n2
    mu = 0.27
    h_pair = h_normal + mu * (pair_ann + pair_cre)

    rho_pair = gibbs_state(h_pair, beta=1.1)
    broken_comm = np.linalg.norm(commutator(n_tot, h_pair))
    pair_ev = expect(rho_pair, pair_ann)

    check("A pairing insertion breaks the retained U(1) symmetry", broken_comm > 1e-8,
          f"||[N,H_pair]||={broken_comm:.2e}")
    check("Once DeltaL=2 is inserted, the Majorana expectation becomes nonzero", abs(pair_ev) > 1e-4,
          f"<cc>={pair_ev.real:+.6f}{pair_ev.imag:+.6f}i")

    print()
    print("  This is the exact lane boundary in one line:")
    print("  more charge-zero interaction complexity does nothing, but a genuine")
    print("  DeltaL=2 microscopic insertion changes the symmetry class.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: FINITE NORMAL-GRAMMAR NO-GO")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Framework axiom; Observable principle; Anomaly-forced time;")
    print("          Native weak algebra; Structural SU(3) closure; One-generation matter closure")
    print("  - docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Does enlarging the current lane from the native quadratic Gaussian")
    print("  to arbitrary finite number-preserving interactions inside the")
    print("  retained normal grammar generate a Majorana coefficient?")

    n_tot, h_sourced, pair_ann, density, n0 = test_charge_zero_grammar_is_u1_invariant()
    test_selection_rule_kills_majorana_expectation(n_tot, h_sourced, pair_ann, density, n0)
    test_explicit_pairing_source_is_new_object()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. The entire current finite retained normal grammar has exact")
    print("  fermion-number U(1), so the charge-2 Majorana bilinear vanishes")
    print("  exactly there. The next honest microscopic step is not another")
    print("  charge-zero interaction, but a genuinely new DeltaL=2 object.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
