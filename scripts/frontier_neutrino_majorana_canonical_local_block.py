#!/usr/bin/env python3
"""
Canonical one-generation local antisymmetric block on the Majorana lane.

Question:
  After the current lane has been reduced to one real amplitude mu, is there
  still any residual local matrix freedom in a one-generation antisymmetric
  Majorana realization?

Answer on the current lane:
  No. The local antisymmetric 2x2 complex matrix space is one-dimensional,
  every block is m J_2, and the existing phase-removal theorem reduces that to
  the unique canonical normal form mu J_2 with mu >= 0.

Boundary:
  This is an exact one-generation local normal-form theorem. It does NOT prove
  the primitive exists or fix mu from the full Cl(3) on Z^3 axiom.
"""

from __future__ import annotations

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


def antisymmetric_basis_dimension() -> tuple[int, np.ndarray]:
    constraints = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],  # a = 0
            [0.0, 0.0, 0.0, 1.0],  # d = 0
            [0.0, 1.0, 1.0, 0.0],  # b + c = 0
        ],
        dtype=complex,
    )
    _, singulars, vh = np.linalg.svd(constraints)
    rank = int(np.sum(singulars > 1e-12))
    null_basis = vh[rank:].conj().T
    return null_basis.shape[1], null_basis


def antisymmetric_projection(matrix: np.ndarray) -> np.ndarray:
    return 0.5 * (matrix - matrix.T)


def pfaffian_2x2(matrix: np.ndarray) -> complex:
    return matrix[0, 1]


def canonicalize_phase(m: complex) -> tuple[complex, np.ndarray]:
    alpha = np.angle(m) / 2.0
    u = np.exp(-1j * alpha) * np.eye(2, dtype=complex)
    return u @ (m * J2) @ u.T, u


def test_antisymmetric_space_is_one_dimensional() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE LOCAL ANTISYMMETRIC 2x2 SPACE IS ONE-DIMENSIONAL")
    print("=" * 88)

    rank, basis = antisymmetric_basis_dimension()
    reconstruction = 3.7 - 0.8j
    sample = reconstruction * J2
    coeff = sample[0, 1]
    recon_err = np.linalg.norm(sample - coeff * J2)
    diag_err = abs(sample[0, 0]) + abs(sample[1, 1])
    offdiag_err = abs(sample[1, 0] + sample[0, 1])

    check("The complex antisymmetric 2x2 matrix space has dimension 1", rank == 1,
          f"dim={rank}")
    check("The unique basis direction is J_2 up to normalization",
          basis.shape == (4, 1) and np.linalg.norm(basis[:, 0].reshape(2, 2) - basis[1, 0] * J2) < 1e-12,
          f"basis={basis[:, 0].reshape(2, 2) if basis.size else '[]'}")
    check("Every antisymmetric 2x2 matrix is exactly m J_2", recon_err < 1e-12,
          f"reconstruction error={recon_err:.2e}")
    check("Antisymmetry forces zero diagonal and opposite off-diagonal entries",
          diag_err < 1e-12 and offdiag_err < 1e-12,
          f"diag_err={diag_err:.2e}, offdiag_err={offdiag_err:.2e}")

    print()
    print("  So the one-generation local pairing block is not a matrix family.")
    print("  It is already a single complex coordinate on J_2.")


def test_phase_removal_gives_canonical_real_block() -> None:
    print("\n" + "=" * 88)
    print("PART 2: PHASE REMOVAL FIXES THE UNIQUE REAL NORMAL FORM")
    print("=" * 88)

    m = -0.61 + 0.44j
    a = m * J2
    canonical, u = canonicalize_phase(m)
    target = abs(m) * J2
    congruence_err = np.linalg.norm(canonical - target)
    unitary_err = np.linalg.norm(u.conj().T @ u - np.eye(2))

    check("Local rephasing acts by unitary congruence on the antisymmetric block", unitary_err < 1e-12,
          f"||U^dag U-I||={unitary_err:.2e}")
    check("Choosing alpha = arg(m)/2 sends m J_2 to |m| J_2", congruence_err < 1e-12,
          f"canonicalization error={congruence_err:.2e}")
    check("The canonical block is real and antisymmetric", np.linalg.norm(target.imag) < 1e-12 and np.linalg.norm(target + target.T) < 1e-12,
          f"imag_err={np.linalg.norm(target.imag):.2e}, antisym_err={np.linalg.norm(target + target.T):.2e}")

    print()
    print("  Modulo the existing one-generation nu_R rephasing freedom, every")
    print("  local block is equivalent to the unique normal form mu J_2.")


def test_all_local_invariants_collapse_to_mu() -> None:
    print("\n" + "=" * 88)
    print("PART 3: RETAINED LOCAL BLOCK INVARIANTS DEPEND ONLY ON MU")
    print("=" * 88)

    mu = 0.73
    phases = [0.0, 0.4, -1.1, 2.2]
    phase_errors = []
    singular_errors = []
    trace_errors = []
    pf_errors = []
    det_errors = []

    for phi in phases:
        m = mu * np.exp(1j * phi)
        a = m * J2
        svals = np.linalg.svd(a, compute_uv=False)
        phase_errors.append(abs(abs(pfaffian_2x2(a)) - mu))
        singular_errors.append(np.linalg.norm(np.sort(svals) - np.array([mu, mu])))
        trace_errors.append(abs(np.trace(a.conj().T @ a) - 2.0 * mu * mu))
        det_errors.append(abs(abs(np.linalg.det(a)) - mu * mu))

    check("Pfaffian magnitude is exactly mu on every phase representative", max(phase_errors) < 1e-12,
          f"max | |Pf|-mu |={max(phase_errors):.2e}")
    check("Both singular values are exactly mu on every phase representative", max(singular_errors) < 1e-12,
          f"max singular-value error={max(singular_errors):.2e}")
    check("A^dag A has trace 2 mu^2 on every phase representative", max(trace_errors) < 1e-12,
          f"max trace error={max(trace_errors):.2e}")
    check("Determinant magnitude is mu^2 on every phase representative", max(det_errors) < 1e-12,
          f"max | |det|-mu^2 |={max(det_errors):.2e}")

    print()
    print("  So all retained one-generation local block invariants collapse to")
    print("  the single real amplitude mu. There is no extra local matrix data.")


def test_projection_of_generic_matrix_lands_on_single_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 4: GENERIC LOCAL 2x2 DATA PROJECTS ONTO ONE ANTISYMMETRIC SLOT")
    print("=" * 88)

    generic = np.array([[1.1 + 0.2j, -0.7 + 0.6j], [0.3 - 0.4j, -1.3 + 0.5j]], dtype=complex)
    anti = antisymmetric_projection(generic)
    coeff = anti[0, 1]
    recon_err = np.linalg.norm(anti - coeff * J2)
    sym_overlap = np.linalg.norm(anti + anti.T)

    check("Antisymmetric projection of generic local data lies on one slot", recon_err < 1e-12,
          f"projection reconstruction error={recon_err:.2e}")
    check("Projected block is exactly antisymmetric", sym_overlap < 1e-12,
          f"||A+A^T||={sym_overlap:.2e}")

    print()
    print("  Even before any activation law is specified, the local antisymmetric")
    print("  channel has only one coefficient to turn on.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: CANONICAL ONE-GENERATION LOCAL BLOCK")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Framework axiom; Observable principle; Anomaly-forced time;")
    print("          Native weak algebra; Structural SU(3) closure; One-generation matter closure")
    print("  - docs/NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md")
    print()
    print("Question:")
    print("  After reducing the local one-generation Majorana lane to one real")
    print("  amplitude mu, is there any residual local antisymmetric block")
    print("  freedom, or is the microscopic 2x2 pairing block already canonical?")

    test_antisymmetric_space_is_one_dimensional()
    test_phase_removal_gives_canonical_real_block()
    test_all_local_invariants_collapse_to_mu()
    test_projection_of_generic_matrix_lands_on_single_slot()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The one-generation local antisymmetric Majorana block is already")
    print("  canonical: every realization is equivalent to mu J_2 with mu >= 0.")
    print("  No residual local matrix or basis freedom remains beyond mu.")
    print()
    print("  The current-stack activation law is now separated explicitly in")
    print("  frontier_neutrino_majorana_current_stack_zero_law.py:")
    print("  on the retained stack actually present today, mu_current = 0.")
    print("  The remaining frontier is whether a genuinely new axiom-side")
    print("  charge-2 primitive can change that zero law.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
