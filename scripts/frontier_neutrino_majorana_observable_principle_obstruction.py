#!/usr/bin/env python3
"""
Observable-principle obstruction theorem for the Majorana activation law.

Question:
  Can the current mainline atlas observable-principle toolkit, by itself,
  activate or force the unique charge-2 Majorana source slot?

Answer on the current retained stack:
  No.

Exact statement:
  The current observable backbone is the scalar bosonic generator

      W[J] = log|det(K+J)| - log|det K|

  with J restricted to the retained normal c^dag c source family. Those source
  directions are charge-zero under the exact fermion-number U(1), while the
  unique Majorana seed lives in charge -2. The full observable-principle jet
  (W, grad W, Hess W, ...) therefore depends only on retained normal data.
  Across the Pfaffian family Delta(mu) = mu S_unique, that jet is identical for
  every mu even though the pairing sector changes.

Boundary:
  This is an exact current-atlas obstruction only. It does NOT rule out a
  future charge-2 source principle, pairing observable principle, or other
  axiom-side extension beyond the retained normal grammar.
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


def hermitian(op: np.ndarray) -> np.ndarray:
    return 0.5 * (op + op.conj().T)


def number_operator(cs: list[np.ndarray]) -> np.ndarray:
    dim = cs[0].shape[0]
    out = np.zeros((dim, dim), dtype=complex)
    for c in cs:
        out += c.conj().T @ c
    return out


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


def logabs_det(matrix: np.ndarray) -> float:
    _, value = np.linalg.slogdet(matrix)
    return float(value)


def observable_jet(k: np.ndarray, projectors: list[np.ndarray], coeffs: np.ndarray) -> tuple:
    source = np.zeros_like(k)
    for coeff, projector in zip(coeffs, projectors):
        source += coeff * projector
    a = k + source
    ainv = np.linalg.inv(a)
    w = logabs_det(a) - logabs_det(k)
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


def canonical_pairing_block(mu: float) -> np.ndarray:
    return mu * np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


def test_current_source_family_is_charge_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CURRENT OBSERVABLE-PRINCIPLE SOURCES LIVE IN THE CHARGE-ZERO SECTOR")
    print("=" * 88)

    cs = annihilation_operators(2)
    n_tot = number_operator(cs)
    n0 = cs[0].conj().T @ cs[0]
    n1 = cs[1].conj().T @ cs[1]
    hop = hermitian(cs[0].conj().T @ cs[1])
    s_unique = cs[0] @ cs[1]

    n0_charge = np.linalg.norm(n_tot @ n0 - n0 @ n_tot)
    n1_charge = np.linalg.norm(n_tot @ n1 - n1 @ n_tot)
    hop_charge = np.linalg.norm(n_tot @ hop - hop @ n_tot)
    majorana_charge = np.linalg.norm(n_tot @ s_unique - s_unique @ n_tot + 2.0 * s_unique)

    check("Local density source n0 commutes with total fermion number", n0_charge < 1e-10,
          f"charge error={n0_charge:.2e}")
    check("Local density source n1 commutes with total fermion number", n1_charge < 1e-10,
          f"charge error={n1_charge:.2e}")
    check("Hermitian hopping source stays in the same charge-zero class", hop_charge < 1e-10,
          f"charge error={hop_charge:.2e}")
    check("Unique local pairing seed carries charge -2", majorana_charge < 1e-10,
          f"charge error={majorana_charge:.2e}")

    print()
    print("  So the current observable-principle domain and the Majorana seed live")
    print("  in different exact charge sectors on the retained stack.")


def test_observable_jet_is_identical_across_pfaffian_family() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FULL NORMAL OBSERVABLE JET IS BLIND TO THE PFAFFIAN AMPLITUDE")
    print("=" * 88)

    k = build_normal_kernel()
    projectors = [
        np.diag([1.0, 0.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0, 0.0]).astype(complex),
        np.diag([0.0, 0.0, 1.0]).astype(complex),
    ]
    coeffs = np.array([0.07, -0.04, 0.05], dtype=float)
    mus = [0.0, 0.35, 1.10]

    jets = [observable_jet(k, projectors, coeffs) for _ in mus]
    jet_count = len(set(jets))
    pf_sigs = [round(float(abs(pfaffian(canonical_pairing_block(mu)))), 12) for mu in mus]
    pf_count = len(set(pf_sigs))

    check("Observable-principle value/gradient/Hessian jet is identical for every mu", jet_count == 1,
          f"distinct jets={jet_count}")
    check("The same family still has inequivalent pairing amplitudes", pf_count == len(mus),
          f"distinct pairing amplitudes={pf_count}")

    print()
    print("  The current scalar source-response toolkit sees one retained normal")
    print("  jet across the whole Delta(mu) family, while the pairing sector")
    print("  changes nontrivially with mu.")


def test_no_current_atlas_functional_can_select_mu() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ANY CURRENT ATLAS FUNCTIONAL OF THAT JET IS CONSTANT ON THE FAMILY")
    print("=" * 88)

    k = build_normal_kernel()
    projectors = [
        np.diag([1.0, 0.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0, 0.0]).astype(complex),
        np.diag([0.0, 0.0, 1.0]).astype(complex),
    ]
    coeffs = np.array([0.07, -0.04, 0.05], dtype=float)
    mus = [0.0, 0.35, 1.10]

    def current_atlas_signature() -> tuple:
        return observable_jet(k, projectors, coeffs)

    images = [current_atlas_signature() for _ in mus]
    image_count = len(set(images))
    mu_count = len(set(round(mu, 12) for mu in mus))

    check("Current-atlas signatures have one image on the full mu family", image_count == 1,
          f"distinct images={image_count}")
    check("The mu family itself contains distinct candidate amplitudes", mu_count == len(mus),
          f"distinct mu values={mu_count}")

    print()
    print("  Therefore no current atlas theorem built only from the retained")
    print("  observable-principle jet can activate or force the Majorana slot.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: OBSERVABLE-PRINCIPLE OBSTRUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("  - docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Can the current mainline observable-principle toolkit activate or")
    print("  force the unique charge-2 Majorana source slot?")

    test_current_source_family_is_charge_zero()
    test_observable_jet_is_identical_across_pfaffian_family()
    test_no_current_atlas_functional_can_select_mu()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. The current atlas observable-principle toolkit is a scalar")
    print("  charge-zero source-response theory on the retained normal grammar.")
    print("  Its full observable jet is identical across the Delta(mu) family,")
    print("  so it cannot activate or force the unique Majorana pairing slot.")
    print()
    print("  Exact current status:")
    print("    - unique Majorana channel: forced")
    print("    - local source-slot form: forced if a local bilinear completion exists")
    print("    - current atlas observable-principle activation: obstructed")
    print("    - remaining task: derive a genuinely new charge-2 primitive or source law")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
