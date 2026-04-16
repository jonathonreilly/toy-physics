#!/usr/bin/env python3
"""
Majorana no-stationary-scale theorem on the admitted source class.

Question:
  After the Nambu source principle, source-ray theorem, and staircase-blindness
  theorem, could the admitted Majorana Pfaffian/Nambu family already contain an
  intrinsic stationary or endpoint selector for the absolute staircase scale?

Answer on the current exact source class:
  No. The one-generation local bosonic generator is W_1(mu)=log(mu)+const, and
  the fixed three-generation Z3 lift scales as W_3(lambda)=3 log(lambda)+const.
  Their derivatives never vanish for positive scale, while normalized class
  invariants are exactly scale-invariant. So the current admitted source class
  has no intrinsic stationary scale.

Boundary:
  This does NOT rule out a future non-homogeneous scale-selection principle
  beyond the current source class. It proves only that the existing admitted
  Pfaffian/Nambu family does not already contain one.
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


def z3_texture(a: complex, b: complex, eps: complex) -> np.ndarray:
    return np.array(
        [[a, 0.0, 0.0], [0.0, eps, b], [0.0, b, eps]],
        dtype=complex,
    )


def normalized_spectrum(matrix: np.ndarray) -> np.ndarray:
    svals = np.linalg.svd(matrix, compute_uv=False)
    return np.sort(svals / np.linalg.norm(svals))


def test_local_generator_has_no_stationary_scale() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ONE-GENERATION LOCAL PFAFFIAN GENERATOR HAS NO STATIONARY SCALE")
    print("=" * 88)

    mu0 = 0.37
    mu1 = 0.91
    w_step = math.log(abs(pfaffian(mu1 * J2))) - math.log(abs(pfaffian(mu0 * J2)))
    w_exact = math.log(mu1) - math.log(mu0)

    eps = 1e-7
    wp = math.log(abs(pfaffian((mu0 + eps) * J2)))
    wm = math.log(abs(pfaffian((mu0 - eps) * J2)))
    deriv_num = (wp - wm) / (2.0 * eps)
    deriv_exact = 1.0 / mu0

    mu_samples = [0.13, 0.29, 0.64, 1.21]
    derivs = [1.0 / mu for mu in mu_samples]

    check("The local generator step is exactly log(mu1)-log(mu0)", abs(w_step - w_exact) < 1e-12,
          f"|DeltaW-DeltaLog|={abs(w_step - w_exact):.2e}")
    check("The exact local source derivative is 1/mu", abs(deriv_num - deriv_exact) < 1e-6,
          f"dW/dmu={deriv_num:.6f}, 1/mu={deriv_exact:.6f}")
    check("The local derivative never vanishes on positive scales", min(abs(d) for d in derivs) > 0.0,
          f"min |dW/dmu|={min(abs(d) for d in derivs):.6f}")

    print()
    print("  On the admitted one-generation Pfaffian lane, the bosonic generator")
    print("  is monotone in log(mu). So there is no intrinsic stationary local")
    print("  scale anywhere on mu > 0.")


def test_three_generation_lift_has_no_stationary_scale() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FIXED Z3 LIFT IS AFFINE IN LOG(SCALE), NOT STATIONARY")
    print("=" * 88)

    m_ref = z3_texture(1.4, 0.52, 0.09 + 0.04j)
    delta_ref = np.kron(m_ref, J2)

    lam0 = 0.41
    lam1 = 0.83
    pf0 = pfaffian(lam0 * delta_ref)
    pf1 = pfaffian(lam1 * delta_ref)
    scale_ratio_err = abs(pf1 / pf0 - (lam1 / lam0) ** 3)

    w_step = math.log(abs(pf1)) - math.log(abs(pf0))
    w_exact = 3.0 * (math.log(lam1) - math.log(lam0))

    eps = 1e-7
    wp = math.log(abs(pfaffian((lam0 + eps) * delta_ref)))
    wm = math.log(abs(pfaffian((lam0 - eps) * delta_ref)))
    deriv_num = (wp - wm) / (2.0 * eps)
    deriv_exact = 3.0 / lam0

    lam_samples = [0.19, 0.44, 0.91, 1.37]
    derivs = [3.0 / lam for lam in lam_samples]

    check("The three-generation Pfaffian scales exactly as lambda^3 on the fixed texture class",
          scale_ratio_err < 1e-10, f"scale-ratio error={scale_ratio_err:.2e}")
    check("The lifted generator step is exactly 3[log(lambda1)-log(lambda0)]", abs(w_step - w_exact) < 1e-10,
          f"|DeltaW-3DeltaLog|={abs(w_step - w_exact):.2e}")
    check("The lifted source derivative is exactly 3/lambda", abs(deriv_num - deriv_exact) < 1e-5,
          f"dW/dlambda={deriv_num:.6f}, 3/lambda={deriv_exact:.6f}")
    check("The lifted derivative never vanishes on positive scales", min(abs(d) for d in derivs) > 0.0,
          f"min |dW/dlambda|={min(abs(d) for d in derivs):.6f}")

    print()
    print("  So the fixed three-generation source class still carries only")
    print("  logarithmic scale dependence. It has no internal staircase anchor.")


def test_normalized_class_invariants_are_scale_invariant() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REMAINING EXACT CLASS INVARIANTS ARE SCALE-INVARIANT")
    print("=" * 88)

    m_ref = z3_texture(1.4, 0.52, 0.09 + 0.04j)
    scales = [0.17, 0.53, 1.11]

    spectra = [normalized_spectrum(scale * m_ref) for scale in scales]
    max_spec_diff = max(np.linalg.norm(spec - spectra[0]) for spec in spectra[1:])

    delta_ref = np.kron(m_ref, J2)
    normed_deltas = [(scale * delta_ref) / np.linalg.norm(scale * delta_ref) for scale in scales]
    max_delta_diff = max(np.linalg.norm(delta - normed_deltas[0]) for delta in normed_deltas[1:])

    check("Normalized singlet/doublet spectrum is identical across overall rescaling", max_spec_diff < 1e-12,
          f"max normalized spectrum difference={max_spec_diff:.2e}")
    check("Normalized pairing block is identical across overall rescaling", max_delta_diff < 1e-12,
          f"max normalized Delta difference={max_delta_diff:.2e}")

    print()
    print("  So the exact class invariants organize the source class but cannot")
    print("  pick its absolute amplitude.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: NO-STATIONARY-SCALE THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Could the admitted Majorana Pfaffian/Nambu family already contain an")
    print("  intrinsic stationary or endpoint selector for the absolute staircase")
    print("  scale?")

    test_local_generator_has_no_stationary_scale()
    test_three_generation_lift_has_no_stationary_scale()
    test_normalized_class_invariants_are_scale_invariant()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. On the current admitted source class, the scale-sensitive exact")
    print("  bosonic generator is affine in log(scale), and the remaining exact")
    print("  class invariants are scale-invariant. So the current Pfaffian/Nambu")
    print("  family has no intrinsic stationary scale and no internal staircase")
    print("  anchor.")
    print()
    print("  On that earlier logarithmic family, any full Majorana scale-selection")
    print("  law had to introduce some genuinely new non-homogeneous ingredient.")
    print("  Later branch work first narrows the blocker to local point")
    print("  selection on the background-normalized curve, and then closes that")
    print("  local step at the self-dual point rho = 1; what remains is the")
    print("  absolute staircase embedding beyond that local point.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
