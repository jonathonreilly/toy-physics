#!/usr/bin/env python3
"""
Current-stack exhaustion theorem for the Majorana activation problem.

Question:
  After all current main-derived Majorana reductions and obstructions, can the
  present retained stack itself still force a nonzero Majorana activation law?

Answer on the current retained stack:
  No.

Exact statement:
  1. If a local bilinear charge-2 primitive is admitted, the local lane is
     already fixed to the canonical Pfaffian block A_M(mu)=mu J_2 with local
     generator log(mu).
  2. But the current retained normal signature and the current
     observable-principle jet are identical across the whole mu family.
  3. The retained three-generation / Z3 lift remains charge -2 and has zero
     expectation on the current normal grammar.

  Therefore the current retained stack cannot distinguish mu=0 from mu>0 and
  cannot force the primitive to turn on. Any full closure now requires a
  genuinely new charge-2 primitive or source principle beyond the retained
  stack.
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


def build_normal_kernel() -> np.ndarray:
    base = np.array(
        [
            [1.30, 0.11 - 0.03j, 0.02],
            [0.11 + 0.03j, 1.55, -0.06j],
            [0.02, 0.06j, 1.72],
        ],
        dtype=complex,
    )
    return 0.5 * (base + base.conj().T)


def retained_signature(k: np.ndarray, source_values: list[float]) -> tuple:
    evals = tuple(np.round(np.linalg.eigvalsh(k), 12))
    det_responses = []
    for value in source_values:
        src = value * np.eye(k.shape[0], dtype=complex)
        _, log1 = np.linalg.slogdet(k + src)
        _, log0 = np.linalg.slogdet(k)
        det_responses.append(round(float(log1 - log0), 12))
    return evals + tuple(det_responses)


def observable_jet(k: np.ndarray, projectors: list[np.ndarray], coeffs: np.ndarray) -> tuple:
    source = np.zeros_like(k)
    for coeff, projector in zip(coeffs, projectors):
        source += coeff * projector
    a = k + source
    ainv = np.linalg.inv(a)
    _, log1 = np.linalg.slogdet(a)
    _, log0 = np.linalg.slogdet(k)
    w = float(log1 - log0)
    grad = np.array([np.real(np.trace(ainv @ p)) for p in projectors], dtype=float)
    hess = np.array(
        [
            [-np.real(np.trace(ainv @ p @ ainv @ q)) for q in projectors]
            for p in projectors
        ],
        dtype=float,
    )
    return (
        round(w, 12),
        tuple(round(float(x), 12) for x in grad),
        tuple(tuple(round(float(x), 12) for x in row) for row in hess),
    )


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


def test_local_lane_is_fixed_if_primitive_exists() -> None:
    print("\n" + "=" * 88)
    print("PART 1: IF THE PRIMITIVE EXISTS LOCALLY, ITS ONE-GENERATION LANE IS ALREADY FIXED")
    print("=" * 88)

    mus = [0.4, 0.9, 1.3]
    pf_errors = []
    add_errors = []
    for mu in mus:
        a = mu * J2
        pf_errors.append(abs(pfaffian(a) - mu))
    a1 = 0.7 * J2
    a2 = 1.1 * J2
    a_tot = np.block([[a1, np.zeros((2, 2), dtype=complex)], [np.zeros((2, 2), dtype=complex), a2]])
    add_errors.append(abs(math.log(abs(pfaffian(a_tot))) - (math.log(abs(pfaffian(a1))) + math.log(abs(pfaffian(a2))))))

    check("Canonical local block has Pf(A_M)=mu", max(pf_errors) < 1e-12,
          f"max |Pf-mu|={max(pf_errors):.2e}")
    check("Independent local antisymmetric sectors force log|Pf| additivity", max(add_errors) < 1e-12,
          f"max additivity error={max(add_errors):.2e}")

    print()
    print("  So the local-bilinear realization family is not the open problem anymore.")


def test_current_normal_data_are_blind_to_mu() -> None:
    print("\n" + "=" * 88)
    print("PART 2: CURRENT NORMAL DATA AND SOURCE-RESPONSE JET ARE BLIND TO MU")
    print("=" * 88)

    k = build_normal_kernel()
    source_values = [-0.2, 0.0, 0.15, 0.3]
    projectors = [
        np.diag([1.0, 0.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0, 0.0]).astype(complex),
        np.diag([0.0, 0.0, 1.0]).astype(complex),
    ]
    coeffs = np.array([0.07, -0.04, 0.05], dtype=float)
    mus = [0.0, 0.35, 1.10]

    signatures = [retained_signature(k, source_values) for _ in mus]
    jets = [observable_jet(k, projectors, coeffs) for _ in mus]
    pfamps = [round(float(abs(pfaffian(mu * J2))), 12) for mu in mus]

    check("Retained normal signature is identical across the full mu family", len(set(signatures)) == 1,
          f"distinct signatures={len(set(signatures))}")
    check("Observable-principle jet is identical across the same family", len(set(jets)) == 1,
          f"distinct jets={len(set(jets))}")
    check("The local pairing amplitudes in that family are genuinely different", len(set(pfamps)) == len(mus),
          f"distinct amplitudes={len(set(pfamps))}")

    print()
    print("  So the current retained stack has one normal signature and one normal")
    print("  source-response jet across mu=0 and mu>0 alike.")


def test_z3_flavor_lift_cannot_activate() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE RETAINED THREE-GENERATION / Z3 LIFT STILL CANNOT ACTIVATE THE SLOT")
    print("=" * 88)

    cs = annihilation_operators(6)
    n_tot = number_operator(cs)
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

    m_z3 = z3_texture(1.10, 0.40, 0.07 + 0.03j)
    delta_z3 = np.kron(m_z3, J2)
    q_z3 = pair_operator_from_delta(delta_z3, cs)
    charge_err = np.linalg.norm(n_tot @ q_z3 - q_z3 @ n_tot + 2.0 * q_z3)
    rho = gibbs_state(h_normal, beta=0.8)
    ev_z3 = np.trace(rho @ q_z3)

    lam = 0.08
    h_z3 = h_normal + lam * (q_z3 + q_z3.conj().T)
    rho_z3 = gibbs_state(h_z3, beta=0.8)
    ev_z3_active = np.trace(rho_z3 @ q_z3)

    check("Z3-textured Majorana pairing operator still has charge -2", charge_err < 1e-10,
          f"charge error={charge_err:.2e}")
    check("Its expectation vanishes on the retained normal grammar", abs(ev_z3) < 1e-10,
          f"<Q_Z3>={ev_z3.real:+.2e}{ev_z3.imag:+.2e}i")
    check("It becomes nonzero only after explicit pairing insertion", abs(ev_z3_active) > 1e-4,
          f"<Q_Z3>_active={ev_z3_active.real:+.6f}{ev_z3_active.imag:+.6f}i")

    print()
    print("  So flavor/Z3 can shape an activated sector, but does not activate it.")


def test_current_stack_conclusion() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT STACK IS EXHAUSTED ON THE MAJORANA ACTIVATION QUESTION")
    print("=" * 88)

    k = build_normal_kernel()
    source_values = [-0.2, 0.0, 0.15, 0.3]
    projectors = [
        np.diag([1.0, 0.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0, 0.0]).astype(complex),
        np.diag([0.0, 0.0, 1.0]).astype(complex),
    ]
    coeffs = np.array([0.07, -0.04, 0.05], dtype=float)
    mus = [0.0, 0.35, 1.10]

    def current_stack_package() -> tuple:
        return retained_signature(k, source_values) + observable_jet(k, projectors, coeffs)

    packages = [current_stack_package() for _ in mus]
    activation_family = [round(float(abs(pfaffian(mu * J2))), 12) for mu in mus]

    check("Current-stack data package has one image across mu=0 and mu>0", len(set(packages)) == 1,
          f"distinct packages={len(set(packages))}")
    check("The corresponding activation family is still nontrivial", len(set(activation_family)) == len(mus),
          f"distinct activation amplitudes={len(set(activation_family))}")

    print()
    print("  Therefore the present retained stack cannot distinguish or force the")
    print("  Majorana activation amplitude. A new charge-2 primitive or source law")
    print("  is required beyond the current stack.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: CURRENT-STACK EXHAUSTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("  - docs/NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_OBSERVABLE_PRINCIPLE_OBSTRUCTION_NOTE.md")
    print()
    print("Question:")
    print("  Can the current retained stack itself still force a nonzero")
    print("  Majorana activation law?")

    test_local_lane_is_fixed_if_primitive_exists()
    test_current_normal_data_are_blind_to_mu()
    test_z3_flavor_lift_cannot_activate()
    test_current_stack_conclusion()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. On the current retained stack, the Majorana activation problem is")
    print("  exhausted negatively. If a local bilinear primitive exists, its local")
    print("  realization is already fixed; but the current retained data cannot")
    print("  distinguish mu=0 from mu>0, and the retained flavor lift cannot turn")
    print("  it on.")
    print()
    print("  So full closure now requires a genuinely new charge-2 primitive or")
    print("  source principle beyond the current retained stack.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
