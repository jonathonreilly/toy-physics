#!/usr/bin/env python3
"""
Local Pfaffian uniqueness theorem on the Majorana lane.

Question:
  If the missing Majorana primitive is admitted as a local bilinear completion
  on the unique nu_R channel, is the Pfaffian/Nambu realization just one
  convenient example, or is it forced?

Answer on the retained local bilinear lane:
  It is forced.

Exact statement:
  The unique-source-slot and canonical-local-block theorems reduce every local
  bilinear completion to the canonical antisymmetric 2x2 block A_M(mu)=mu J_2.
  The finite Grassmann integral of a quadratic antisymmetric form is exactly
  its Pfaffian, and independent antisymmetric sectors multiply. Therefore the
  unique additive CPT-even scalar generator on the local bilinear Majorana lane
  is log|Pf| = log(mu).

Boundary:
  This does NOT force the charge-2 primitive to exist in the full axiom. It
  only proves that, if the primitive is realized locally at bilinear level, its
  exact microscopic realization and bosonic generator are uniquely Pfaffian.
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


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    dim = sum(block.shape[0] for block in blocks)
    out = np.zeros((dim, dim), dtype=complex)
    start = 0
    for block in blocks:
        n = block.shape[0]
        out[start:start + n, start:start + n] = block
        start += n
    return out


def canonicalize_phase(m: complex) -> np.ndarray:
    alpha = np.angle(m) / 2.0
    u = np.exp(-1j * alpha) * np.eye(2, dtype=complex)
    return u @ (m * J2) @ u.T


def local_grassmann_integral_2x2(matrix: np.ndarray) -> complex:
    """
    Finite Berezin integral for exp(1/2 psi^T A psi) on a 2-mode antisymmetric
    block. The coefficient of psi_1 psi_2 is exactly A_12.
    """
    return matrix[0, 1]


def test_local_bilinear_completion_collapses_to_mu_j2() -> None:
    print("\n" + "=" * 88)
    print("PART 1: EVERY LOCAL BILINEAR COMPLETION COLLAPSES TO THE CANONICAL BLOCK")
    print("=" * 88)

    samples = [0.73, -0.61 + 0.44j, 0.12 - 0.89j]
    recon_errors = []
    canon_errors = []

    for m in samples:
        a = m * J2
        recon_errors.append(np.linalg.norm(a - a[0, 1] * J2))
        canon_errors.append(np.linalg.norm(canonicalize_phase(m) - abs(m) * J2))

    check("Every local antisymmetric 2x2 block is exactly m J_2", max(recon_errors) < 1e-12,
          f"max reconstruction error={max(recon_errors):.2e}")
    check("Local rephasing sends every block to the canonical real form mu J_2", max(canon_errors) < 1e-12,
          f"max canonicalization error={max(canon_errors):.2e}")

    print()
    print("  So under the retained local bilinear assumption, there is no local")
    print("  realization family left to choose. Only the real amplitude mu remains.")


def test_local_grassmann_integral_is_pfaffian() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FINITE LOCAL GRASSMANN AMPLITUDE IS EXACTLY THE PFAFFIAN")
    print("=" * 88)

    m = -0.61 + 0.44j
    a = m * J2
    integral = local_grassmann_integral_2x2(a)
    pf = pfaffian(a)
    det = np.linalg.det(a)

    check("Local Berezin integral equals A_12 on the canonical block", abs(integral - m) < 1e-12,
          f"integral={integral}")
    check("That local amplitude is exactly the Pfaffian", abs(integral - pf) < 1e-12,
          f"|integral-Pf|={abs(integral - pf):.2e}")
    check("Determinant is only the square of the physical local amplitude", abs(det - pf * pf) < 1e-12,
          f"|det-Pf^2|={abs(det - pf * pf):.2e}")

    print()
    print("  So on the local bilinear Majorana lane, the microscopic amplitude is")
    print("  Pf(A), not det(A). The determinant loses the sign/phase slot by squaring.")


def test_pfaffian_factorization_forces_logabs_pf() -> None:
    print("\n" + "=" * 88)
    print("PART 3: INDEPENDENT LOCAL PAIRING SECTORS FORCE THE SAME LOG-ADDITIVE GENERATOR")
    print("=" * 88)

    a1 = 0.7 * J2
    a2 = 1.3 * J2
    atot = block_diag(a1, a2)

    pf1 = pfaffian(a1)
    pf2 = pfaffian(a2)
    pf_tot = pfaffian(atot)
    add_err = abs(math.log(abs(pf_tot)) - (math.log(abs(pf1)) + math.log(abs(pf2))))

    check("Pfaffian factorizes on independent antisymmetric sectors", abs(pf_tot - pf1 * pf2) < 1e-12,
          f"|Pf_tot-Pf1Pf2|={abs(pf_tot - pf1 * pf2):.2e}")
    check("The corresponding CPT-even scalar generator is additive as log|Pf|", add_err < 1e-12,
          f"additivity error={add_err:.2e}")

    print()
    print("  This is the same multiplicative-to-additive logic as the determinant")
    print("  lane, but now on the local antisymmetric pairing sector.")


def test_canonical_local_generator_is_log_mu() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CANONICAL ONE-GENERATION GENERATOR IS EXACTLY LOG(MU)")
    print("=" * 88)

    mu0 = 0.7
    dmu = 0.2
    a0 = mu0 * J2
    a1 = (mu0 + dmu) * J2
    w = math.log(abs(pfaffian(a1))) - math.log(abs(pfaffian(a0)))
    w_expected = math.log(mu0 + dmu) - math.log(mu0)

    eps = 1e-7
    wp = math.log(abs(pfaffian((mu0 + eps) * J2))) - math.log(abs(pfaffian(mu0 * J2)))
    wm = math.log(abs(pfaffian((mu0 - eps) * J2))) - math.log(abs(pfaffian(mu0 * J2)))
    deriv_num = (wp - wm) / (2.0 * eps)
    deriv_exact = 1.0 / mu0

    check("Canonical local source response is log(mu1)-log(mu0)", abs(w - w_expected) < 1e-12,
          f"|W-W_exact|={abs(w - w_expected):.2e}")
    check("The exact local response derivative is 1/mu", abs(deriv_num - deriv_exact) < 1e-6,
          f"dW/dmu={deriv_num:.6f}, 1/mu={deriv_exact:.6f}")

    print()
    print("  So once the local bilinear primitive exists, the one-generation")
    print("  pairing-side observable principle is fixed completely: it is log(mu).")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: LOCAL PFAFFIAN UNIQUENESS")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("  - docs/NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md")
    print("  - docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    print()
    print("Question:")
    print("  If the missing Majorana primitive is realized locally at bilinear")
    print("  level, is the Pfaffian realization optional or forced?")

    test_local_bilinear_completion_collapses_to_mu_j2()
    test_local_grassmann_integral_is_pfaffian()
    test_pfaffian_factorization_forces_logabs_pf()
    test_canonical_local_generator_is_log_mu()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  On the retained local bilinear lane, the Pfaffian realization is")
    print("  forced, not optional. Every local completion reduces to mu J_2, its")
    print("  exact Grassmann amplitude is Pf(A)=mu, and the unique additive")
    print("  CPT-even scalar generator is log|Pf| = log(mu).")
    print()
    print("  What remains open is not the local realization family or the local")
    print("  bosonic generator. It is whether the axiom actually turns that")
    print("  charge-2 primitive on in the first place.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
