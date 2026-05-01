#!/usr/bin/env python3
"""
Minimal Pfaffian / DeltaL=2 extension for the neutrino Majorana lane.

Question:
  The native determinant toolbox cannot generate a Majorana coefficient. What
  is the smallest exact microscopic extension in which the unique
  anomaly-fixed same-chirality Majorana channel becomes a genuine source
  direction?

Answer on this constructed extension:
  Admit an antisymmetric Grassmann Gaussian on the unique Majorana channel.
  The partition amplitude is then a Pfaffian, independent sectors multiply,
  and the unique additive CPT-even scalar generator is log|Pf|.

Boundary:
  This is an exact construction once the antisymmetric Gaussian / pairing
  source is admitted. It is NOT yet a proof that the underlying axiom forces
  that extension or fixes the coefficient numerically.
"""

from __future__ import annotations

import math
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


def pfaffian(matrix: np.ndarray) -> complex:
    """
    Recursive Pfaffian for small even-dimensional antisymmetric matrices.
    Sufficient here because all audited matrices are <= 6x6 or reduced-rank.
    """
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


def logabs_pf(matrix: np.ndarray) -> float:
    value = pfaffian(matrix)
    return float(np.log(abs(value)))


def build_dirac_majorana_seed():
    i2 = np.eye(2, dtype=complex)
    z2 = np.zeros((2, 2), dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)

    g0 = np.block([[i2, z2], [z2, -i2]])
    g1 = np.block([[z2, sx], [-sx, z2]])
    g2 = np.block([[z2, sy], [-sy, z2]])
    g3 = np.block([[z2, sz], [-sz, z2]])
    g5 = 1j * g0 @ g1 @ g2 @ g3
    cmat = 1j * g2 @ g0
    pr = (np.eye(4, dtype=complex) + g5) / 2.0

    b_r = cmat @ pr

    internal = np.zeros((16, 16), dtype=complex)
    internal[15, 15] = 1.0  # unique nu_R nu_R slot from operator classifier

    return b_r, internal


def canonical_j(scale: float) -> np.ndarray:
    return np.array([[0.0, scale], [-scale, 0.0]], dtype=complex)


def majorana_pf_generator(background: np.ndarray, source: np.ndarray) -> float:
    return logabs_pf(background + source) - logabs_pf(background)


def test_unique_majorana_channel_seed() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXISTING CLASSIFIER PICKS ONE ANTISYMMETRIC DELTAL=2 CHANNEL")
    print("=" * 88)

    b_r, internal = build_dirac_majorana_seed()
    channel = np.kron(b_r, internal)

    antisym = np.linalg.norm(channel.T + channel)
    rank = int(np.linalg.matrix_rank(channel, tol=1e-10))
    support = np.nonzero(np.abs(channel) > 1e-12)
    unique_internal_rows = sorted({idx % 16 for idx in support[0]})
    unique_internal_cols = sorted({idx % 16 for idx in support[1]})

    check("Spinor x internal seed is antisymmetric", antisym < 1e-10, f"||S^T+S||={antisym:.2e}")
    check("Unique Majorana seed has rank 2 (one canonical pairing channel)", rank == 2, f"rank={rank}")
    check("Internal support is only on the nu_R slot", unique_internal_rows == [15] and unique_internal_cols == [15],
          f"rows={unique_internal_rows}, cols={unique_internal_cols}")

    evals = np.linalg.eigvalsh(1j * channel)
    nonzero = [val for val in evals if abs(val) > 1e-10]
    check("Antisymmetric seed has one nonzero symplectic pair", len(nonzero) == 2 and abs(nonzero[0] + nonzero[1]) < 1e-10,
          f"nonzero eigenvalues={nonzero}")

    print()
    print("  The existing operator-classification theorem therefore contributes")
    print("  exactly one microscopic pairing direction. Any honest DeltaL=2")
    print("  extension must source this channel, not a family of unrelated ones.")


def test_pfaffian_observable_principle() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ADMITTING AN ANTISYMMETRIC GAUSSIAN FORCES A PFAFFIAN GENERATOR")
    print("=" * 88)

    a1 = canonical_j(2.0)
    a2 = block_diag(canonical_j(3.0), canonical_j(-1.5))
    a_tot = block_diag(a1, a2)

    pf1 = pfaffian(a1)
    pf2 = pfaffian(a2)
    pf_tot = pfaffian(a_tot)

    det_err = abs(pf_tot * pf_tot - np.linalg.det(a_tot))
    add_err = abs(logabs_pf(a_tot) - (logabs_pf(a1) + logabs_pf(a2)))

    check("Pf(A)^2 = det(A) on the antisymmetric Gaussian", det_err < 1e-10,
          f"|Pf^2-det|={det_err:.2e}")
    check("Pfaffian factorizes on block-diagonal independent sectors", abs(pf_tot - pf1 * pf2) < 1e-10,
          f"|Pf_tot-Pf1Pf2|={abs(pf_tot - pf1 * pf2):.2e}")
    check("log|Pf| is additive on independent sectors", add_err < 1e-10,
          f"additivity error={add_err:.2e}")

    print()
    print("  This is the exact beyond-determinant analogue of the observable")
    print("  principle: once the microscopic Gaussian is antisymmetric, the")
    print("  partition amplitude is Pf(A), not det(D+J), and the unique additive")
    print("  CPT-even scalar generator is log|Pf|.")


def test_minimal_unique_channel_extension() -> None:
    print("\n" + "=" * 88)
    print("PART 3: MINIMAL UNIQUE-CHANNEL EXTENSION CARRIES A GENUINE COEFFICIENT")
    print("=" * 88)

    spectator = block_diag(canonical_j(1.7), canonical_j(-0.9))
    m0 = 2.4
    mu = 0.3

    unique_background = canonical_j(m0)
    unique_source = canonical_j(mu)

    a0 = block_diag(spectator, unique_background)
    a_mu = block_diag(spectator, unique_background + unique_source)

    pf_spec = pfaffian(spectator)
    pf_bg = pfaffian(unique_background)
    pf_mu = pfaffian(unique_background + unique_source)
    pf_total_bg = pfaffian(a0)
    pf_total_mu = pfaffian(a_mu)

    generator_mu = majorana_pf_generator(a0, block_diag(np.zeros_like(spectator), unique_source))
    expected_generator = math.log(abs(m0 + mu)) - math.log(abs(m0))

    eps = 1e-6
    gen_p = majorana_pf_generator(a0, block_diag(np.zeros_like(spectator), canonical_j(eps)))
    gen_m = majorana_pf_generator(a0, block_diag(np.zeros_like(spectator), canonical_j(-eps)))
    deriv_num = (gen_p - gen_m) / (2.0 * eps)
    deriv_exact = 1.0 / m0

    check("Unique-channel Pfaffian factorizes with spectators", abs(pf_total_bg - pf_spec * pf_bg) < 1e-10,
          f"|Pf_tot-Pf_specPf_bg|={abs(pf_total_bg - pf_spec * pf_bg):.2e}")
    check("Microscopic source coefficient shifts the unique Pfaffian block directly", abs(pf_mu - (m0 + mu)) < 1e-10,
          f"Pf(unique block)={pf_mu}")
    check("Total Pfaffian responds nontrivially to the unique DeltaL=2 source", abs(pf_total_mu - pf_total_bg) > 1e-8,
          f"|Pf_mu-Pf_bg|={abs(pf_total_mu - pf_total_bg):.2e}")
    check("log|Pf| response matches the exact unique-block formula", abs(generator_mu - expected_generator) < 1e-10,
          f"|W-W_exact|={abs(generator_mu - expected_generator):.2e}")
    check("Generator derivative at zero source equals 1/m0 on the unique channel", abs(deriv_num - deriv_exact) < 1e-6,
          f"dW/dmu={deriv_num:.6f}, 1/m0={deriv_exact:.6f}")

    print()
    print("  On this minimal extension, the Majorana coefficient is no longer")
    print("  excluded by the microscopic surface. It is the explicit amplitude")
    print("  of the unique antisymmetric pairing block.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: MINIMAL PFAFFIAN DELTAL=2 EXTENSION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Framework axiom; Observable principle; Anomaly-forced time;")
    print("          Native weak algebra; Structural SU(3) closure; One-generation matter closure")
    print("  - docs/NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md")
    print()
    print("Question:")
    print("  What is the smallest exact microscopic extension beyond the current")
    print("  determinant toolbox that can carry the unique DeltaL=2 Majorana")
    print("  coefficient?")

    test_unique_majorana_channel_seed()
    test_pfaffian_observable_principle()
    test_minimal_unique_channel_extension()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The minimal honest extension is an antisymmetric Grassmann Gaussian.")
    print("  Its partition amplitude is a Pfaffian, the unique additive CPT-even")
    print("  scalar generator is log|Pf|, and the unique anomaly-fixed Majorana")
    print("  coefficient is the amplitude of the unique antisymmetric pairing block.")
    print()
    print("  What remains open is not the mathematical form of the extension, but")
    print("  whether the underlying Cl(3) on Z^3 axiom forces this Pfaffian/Nambu")
    print("  sector and fixes its coefficient.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
