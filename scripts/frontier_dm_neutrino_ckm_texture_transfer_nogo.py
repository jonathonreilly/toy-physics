#!/usr/bin/env python3
"""
No-transfer theorem for CKM/NNI atlas tools on the current DM neutrino lane.

Question:
  Can the current flavor atlas tools on main -- GST mass-hierarchy logic,
  mass-basis NNI normalization, Schur-complement texture generation, and
  phase-only Jarlskog companions -- be transplanted directly onto the exact
  universal neutrino Dirac bridge to derive the non-universal texture needed
  for leptogenesis?

Answer:
  No on the current stack.

  The retained DM Dirac bridge is Y = y_0 I. Under any unitary left/right
  basis changes, Y remains a scalar times a unitary, so:

      Y'^dag Y' = y_0^2 I

  and the singular-value spectrum stays exactly triple-degenerate
  (y_0, y_0, y_0).

  Therefore:
    1. The GST / mass-hierarchy route collapses: all singular-value ratios are 1.
    2. The mass-basis NNI normalization collapses to the identity map.
    3. The Schur-complement identity can only reorganize O(1) coefficients on a
       degenerate seed; it does not generate the lambda, A lambda^2,
       A lambda^3 hierarchy.
    4. Phase-only Z3/Jarlskog insertions do not help, because Y^dag Y remains
       proportional to the identity and the leptogenesis CP tensor stays zero.

Boundary:
  This does not prove a non-universal neutrino Dirac texture is impossible in
  principle. It proves only that the current CKM/NNI atlas tools do not
  transfer to the current exact universal Dirac bridge without adding new
  non-universal structure first.
"""

from __future__ import annotations

import math
import sys

import numpy as np

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


def z3_bridge() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3.0)
    return (1.0 / np.sqrt(3.0)) * np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega * omega],
            [1.0, omega * omega, omega],
        ],
        dtype=complex,
    )


def right_unitary() -> np.ndarray:
    phi = 2.0 * np.pi / 3.0
    phase = np.diag([1.0, np.exp(1j * phi), np.exp(-1j * phi)]).astype(complex)
    rot = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
            [0.0, -1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
        ],
        dtype=complex,
    )
    return phase @ rot


def singular_mass_ratios(singular_values: np.ndarray) -> tuple[float, float, float]:
    s_sorted = np.sort(np.real_if_close(singular_values))
    return (
        math.sqrt(float(s_sorted[0] / s_sorted[1])),
        math.sqrt(float(s_sorted[1] / s_sorted[2])),
        math.sqrt(float(s_sorted[0] / s_sorted[2])),
    )


def schur_c13_geom(c12: float, c23: float) -> float:
    # For equal singular scales m1=m2=m3 the NNI Schur-complement identity is
    # still c13 = c12*c23. The key point is that no extra hierarchy factor
    # appears when all mass-ratio suppressions are unity.
    return c12 * c23


def main() -> int:
    print("=" * 88)
    print("DM / FLAVOR: CKM TEXTURE TRANSFER NO-GO")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md")
    print("  - docs/CKM_FROM_MASS_HIERARCHY_NOTE.md")
    print("  - docs/CKM_SCHUR_COMPLEMENT_THEOREM.md")
    print("  - docs/CKM_MASS_BASIS_NNI_NOTE.md")
    print("  - docs/JARLSKOG_PHASE_BOUND_NOTE.md")
    print()
    print("Question:")
    print("  Can the current CKM/NNI atlas toolkit be transplanted directly onto the")
    print("  exact universal neutrino Dirac bridge to derive the non-universal flavor")
    print("  texture needed for leptogenesis?")

    y0 = 0.006662640625
    y_universal = y0 * np.eye(3, dtype=complex)
    ul = z3_bridge()
    ur = right_unitary()
    y_prime = ul.conj().T @ y_universal @ ur
    h_prime = y_prime.conj().T @ y_prime
    singular_values = np.linalg.svd(y_prime, compute_uv=False)
    r12, r23, r13 = singular_mass_ratios(singular_values)

    # Representative phase-only attempt.
    phase_only = np.diag([1.0, np.exp(2j * np.pi / 3.0), 1.0]).astype(complex)
    y_phase = y_prime @ phase_only
    h_phase = y_phase.conj().T @ y_phase

    # Representative Schur-complement attempt on a degenerate NNI seed.
    c12_geom = 1.2
    c23_geom = 0.7
    c13_geom = schur_c13_geom(c12_geom, c23_geom)
    c12_phys = c12_geom * r12
    c23_phys = c23_geom * r23
    c13_phys = c13_geom * r13

    offdiag = h_phase - np.diag(np.diag(h_phase))
    cp_entries = [np.imag(h_phase[0, j] ** 2) for j in (1, 2)]

    print()
    print("Representative transformed Yukawa matrix Y':")
    print(y_prime)
    print()
    print("H' = Y'^dag Y':")
    print(h_prime)
    print()
    print("Singular values of Y':")
    print(singular_values)
    print()
    print("Derived mass-ratio factors from the universal bridge:")
    print(f"  sqrt(s1/s2) = {r12:.6f}")
    print(f"  sqrt(s2/s3) = {r23:.6f}")
    print(f"  sqrt(s1/s3) = {r13:.6f}")
    print()
    print("Representative NNI transfer on a degenerate seed:")
    print(f"  c12^geom = {c12_geom:.6f}  ->  c12^phys = {c12_phys:.6f}")
    print(f"  c23^geom = {c23_geom:.6f}  ->  c23^phys = {c23_phys:.6f}")
    print(f"  c13^geom = c12*c23 = {c13_geom:.6f}  ->  c13^phys = {c13_phys:.6f}")

    check(
        "Unitary left/right basis changes preserve Y^dag Y = y_0^2 I",
        np.allclose(h_prime, (y0 * y0) * np.eye(3), atol=1e-12),
        "H' stays proportional to the identity",
    )
    check(
        "The singular-value spectrum remains exactly triple-degenerate",
        np.max(np.abs(singular_values - y0)) < 1e-12,
        f"max |s_i-y0| = {np.max(np.abs(singular_values - y0)):.2e}",
    )
    check(
        "The GST / hierarchy ratios collapse to unity",
        abs(r12 - 1.0) < 1e-12 and abs(r23 - 1.0) < 1e-12 and abs(r13 - 1.0) < 1e-12,
        "no singular-value hierarchy exists to seed CKM-like suppression",
    )
    check(
        "Mass-basis NNI normalization becomes the identity map",
        abs(c12_phys - c12_geom) < 1e-12
        and abs(c23_phys - c23_geom) < 1e-12
        and abs(c13_phys - c13_geom) < 1e-12,
        "all sqrt(m_i/m_j) factors are exactly 1",
    )
    check(
        "Phase-only Z3 insertions do not rescue the CP kernel",
        np.max(np.abs(offdiag)) < 1e-12 and max(abs(x) for x in cp_entries) < 1e-12,
        f"max offdiag(H_phase) = {np.max(np.abs(offdiag)):.2e}",
    )

    print()
    print("Result:")
    print("  The current CKM/NNI atlas toolkit does not transfer to the current")
    print("  exact universal neutrino Dirac bridge. The bridge has no singular-value")
    print("  hierarchy, mass-basis normalization is trivial, Schur-complement")
    print("  identities do not create lambda-suppressed structure from a degenerate")
    print("  seed, and phase-only companions leave Y^dag Y proportional to I.")
    print()
    print("  So the DM leptogenesis blocker is now sharper: a new non-universal")
    print("  neutrino Dirac flavor texture or equivalent exact extra structure is")
    print("  required before the CKM-style flavor atlas can become relevant here.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
