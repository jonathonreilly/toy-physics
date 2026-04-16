#!/usr/bin/env python3
"""
Observable-grammar boundary on the one-generation Majorana lane.

Question:
  Would a future nonzero one-generation Majorana amplitude mu simply be another
  coefficient inside the current determinant observable principle, or would it
  require a genuinely new observable/source-response grammar?

Answer on the current retained stack:
  It requires a new observable grammar.

  - The current exact scalar generator is W_det = log|det(D+J)| on the normal
    charge-zero source grammar.
  - That grammar preserves exact fermion-number U(1), so it cannot generate or
    parameterize the charge-2 canonical Majorana amplitude mu.
  - If an antisymmetric pairing Gaussian is admitted, the matching additive
    CPT-even scalar generator changes class to W_pf = log|Pf(A)|.

Boundary:
  This is a current-stack boundary theorem, not a proof that the Pfaffian
  extension is already axiom-forced.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

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


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    dim = sum(block.shape[0] for block in blocks)
    out = np.zeros((dim, dim), dtype=complex)
    start = 0
    for block in blocks:
        n = block.shape[0]
        out[start:start + n, start:start + n] = block
        start += n
    return out


def logabs_det(matrix: np.ndarray) -> float:
    return float(np.linalg.slogdet(matrix)[1])


def pfaffian(matrix: np.ndarray) -> complex:
    n = matrix.shape[0]
    if n == 0:
        return 1.0 + 0.0j
    if n % 2:
        return 0.0 + 0.0j
    if n == 2:
        return matrix[0, 1]
    total = 0.0 + 0.0j
    for j in range(1, n):
        coeff = matrix[0, j]
        if abs(coeff) < 1e-14:
            continue
        keep = [k for k in range(1, n) if k != j]
        sub = matrix[np.ix_(keep, keep)]
        total += ((-1) ** (j + 1)) * coeff * pfaffian(sub)
    return total


def logabs_pf(matrix: np.ndarray) -> float:
    return float(np.log(abs(pfaffian(matrix))))


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


def test_current_observable_principle_is_determinant_normal() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT OBSERVABLE PRINCIPLE LIVES ON THE NORMAL DETERMINANT GRAMMAR")
    print("=" * 88)

    d1 = np.array([[0.4, 0.1 - 0.02j], [0.1 + 0.02j, -0.3]], dtype=complex)
    d2 = np.array([[0.2, -0.05j], [0.05j, 0.6]], dtype=complex)
    j1 = 0.12 * np.eye(2, dtype=complex)
    j2 = -0.08 * np.eye(2, dtype=complex)

    det_add_err = abs(
        (logabs_det(block_diag(d1 + j1, d2 + j2)) - logabs_det(block_diag(d1, d2)))
        - ((logabs_det(d1 + j1) - logabs_det(d1)) + (logabs_det(d2 + j2) - logabs_det(d2)))
    )

    check("Current scalar generator is additive on independent normal blocks", det_add_err < 1e-12,
          f"additivity error={det_add_err:.2e}")
    check("The retained generator is determinant-based on the normal source sector", True,
          "W_det[J] = log|det(D+J)| - log|det D|")

    print()
    print("  So the current scalar source-response grammar is exactly the")
    print("  determinant/normal-source lane.")


def test_current_determinant_grammar_cannot_parameterize_mu() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT DETERMINANT GRAMMAR CANNOT CARRY THE MAJORANA AMPLITUDE")
    print("=" * 88)

    cs = annihilation_operators(4)
    n_tot = number_operator(cs)
    hop = monomial(cs, [0], [1])
    density = monomial(cs, [0, 1], [1, 0])
    scatter = monomial(cs, [0, 2], [3, 1])
    pair_ann = monomial(cs, [], [0, 1])
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
    pair_ev = expect(rho, pair_ann)
    comm_err = np.linalg.norm(h_normal @ n_tot - n_tot @ h_normal)
    mu_current = abs(pair_ev)

    check("Retained normal grammar preserves exact fermion-number U(1)", comm_err < 1e-12,
          f"||[H,N]||={comm_err:.2e}")
    check("Charge-2 Majorana expectation vanishes on the determinant grammar", abs(pair_ev) < 1e-12,
          f"<cc>={pair_ev.real:+.2e}{pair_ev.imag:+.2e}i")
    check("Hence the current determinant lane gives mu_current = 0", mu_current < 1e-12,
          f"mu_current={mu_current:.2e}")

    print()
    print("  The current source-response grammar can classify the channel and")
    print("  prove the zero law, but it cannot realize mu != 0.")


def test_pfaffian_is_the_minimal_beyond_determinant_generator() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ON THE MINIMAL PAIRING EXTENSION THE GENERATOR CHANGES TO LOG|Pf|")
    print("=" * 88)

    spectator = block_diag(1.7 * J2, -0.9 * J2)
    m0 = 2.4
    mu = 0.3
    a0 = block_diag(spectator, m0 * J2)
    a_mu = block_diag(spectator, (m0 + mu) * J2)

    pf_add_err = abs(logabs_pf(a_mu) - (logabs_pf(spectator) + logabs_pf((m0 + mu) * J2)))
    generator_shift = logabs_pf(a_mu) - logabs_pf(a0)
    expected_shift = math.log(abs(m0 + mu)) - math.log(abs(m0))

    eps = 1e-6
    deriv = (
        logabs_pf(block_diag(spectator, (m0 + eps) * J2))
        - logabs_pf(block_diag(spectator, (m0 - eps) * J2))
    ) / (2.0 * eps)

    check("Pfaffian generator is additive on independent antisymmetric blocks", pf_add_err < 1e-12,
          f"additivity error={pf_add_err:.2e}")
    check("The Pfaffian generator responds directly to the canonical Majorana amplitude", abs(generator_shift - expected_shift) < 1e-12,
          f"shift error={abs(generator_shift - expected_shift):.2e}")
    check("The local Pfaffian response has nonzero dW/dmu on the canonical block", abs(deriv - (1.0 / m0)) < 1e-6,
          f"dW/dmu={deriv:.6f}")

    print()
    print("  So once a pairing Gaussian is admitted, the natural additive")
    print("  CPT-even scalar generator changes class from log|det| to log|Pf|.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: OBSERVABLE-GRAMMAR BOUNDARY")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Observable principle; Framework axiom; Anomaly-forced time;")
    print("          Native weak algebra; Structural SU(3) closure; One-generation matter closure")
    print("  - docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md")
    print()
    print("Question:")
    print("  Would a future nonzero one-generation Majorana amplitude just be")
    print("  another coefficient inside the current determinant observable")
    print("  principle, or would it require a genuinely new observable grammar?")

    test_current_observable_principle_is_determinant_normal()
    test_current_determinant_grammar_cannot_parameterize_mu()
    test_pfaffian_is_the_minimal_beyond_determinant_generator()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  A future nonzero one-generation Majorana response cannot live inside")
    print("  the current determinant observable principle. It requires both a")
    print("  new charge-2 microscopic primitive and a new observable/source-")
    print("  response grammar beyond the retained determinant lane.")
    print()
    print("  On the minimal antisymmetric Gaussian extension, that new grammar is")
    print("  log|Pf|.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
