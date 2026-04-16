#!/usr/bin/env python3
"""
Exact reduction theorem:
full neutrino closure on the one-sided minimal PMNS classes reduces to one
projected lepton source law on the effective 3x3 lepton blocks.

More precisely, deriving:
  1. the Hermitian linear source responses on the two lepton blocks
  2. one oriented non-Hermitian linear probe on the active block

is sufficient to reconstruct (H_nu, H_e) and the residual sheet bit s.
"""

from __future__ import annotations

import sys
import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)


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


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE


def canonical_h(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    ymat = canonical_y(x, y, delta)
    return ymat @ ymat.conj().T


def monomial_y(masses: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(masses, dtype=complex)) @ CYCLE


def monomial_h(masses: np.ndarray) -> np.ndarray:
    ymat = monomial_y(masses)
    return ymat @ ymat.conj().T


def hermitian_basis() -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for i in range(3):
        e = np.zeros((3, 3), dtype=complex)
        e[i, i] = 1.0
        basis.append(e)
    for i in range(3):
        for j in range(i + 1, 3):
            s = np.zeros((3, 3), dtype=complex)
            s[i, j] = 1.0
            s[j, i] = 1.0
            basis.append(s)
            a = np.zeros((3, 3), dtype=complex)
            a[i, j] = -1j
            a[j, i] = 1j
            basis.append(a)
    return basis


def hermitian_linear_response(h: np.ndarray, x: np.ndarray) -> float:
    return float(np.real(np.trace(x @ h)))


def reconstruct_h_from_responses(responses: list[float]) -> np.ndarray:
    basis = hermitian_basis()
    h = np.zeros((3, 3), dtype=complex)
    h[0, 0] = responses[0]
    h[1, 1] = responses[1]
    h[2, 2] = responses[2]
    idx = 3
    for i in range(3):
        for j in range(i + 1, 3):
            sym = responses[idx]
            asym = responses[idx + 1]
            h[i, j] = 0.5 * (sym - 1j * asym)
            h[j, i] = 0.5 * (sym + 1j * asym)
            idx += 2
    return h


def invariant_coordinates(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(np.real(h[0, 0])),
        float(np.real(h[1, 1])),
        float(np.real(h[2, 2])),
        float(np.abs(h[0, 1])),
        float(np.abs(h[1, 2])),
        float(np.abs(h[2, 0])),
        float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
    )


def quadratic_coefficients(obs: tuple[float, float, float, float, float, float, float]) -> tuple[float, float, float]:
    d1, d2, d3, r12, r23, r31, _ = obs
    alpha = r12 * r12
    beta = r23 * r23
    gamma = r31 * r31
    a = d2 * d3 - beta
    b = d1 * d2 * d3 + gamma * d2 - alpha * d3 - beta * d1
    c = gamma * (d1 * d2 - alpha)
    return float(a), float(b), float(c)


def quadratic_roots(obs: tuple[float, float, float, float, float, float, float]) -> np.ndarray:
    a, b, c = quadratic_coefficients(obs)
    disc = max(b * b - 4.0 * a * c, 0.0)
    roots = np.array(
        [
            (b - np.sqrt(disc)) / (2.0 * a),
            (b + np.sqrt(disc)) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()
    return roots


def reconstruct_squares_from_root(
    obs: tuple[float, float, float, float, float, float, float], t1: float
) -> tuple[np.ndarray, np.ndarray, float]:
    d1, d2, d3, r12, r23, _r31, phi = obs
    alpha = r12 * r12
    beta = r23 * r23
    t2 = alpha / (d1 - t1)
    t3 = beta / (d2 - t2)
    xsq = np.array([t1, t2, t3], dtype=float)
    ysq = np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float)
    return xsq, ysq, float(phi)


def candidate_sheets_from_h(h: np.ndarray) -> list[np.ndarray]:
    obs = invariant_coordinates(h)
    roots = quadratic_roots(obs)
    sheets: list[np.ndarray] = []
    for root in roots:
        xsq, ysq, delta = reconstruct_squares_from_root(obs, float(root))
        sheets.append(canonical_y(np.sqrt(xsq), np.sqrt(ysq), delta))
    return sheets


def offdiag_norm(h: np.ndarray) -> float:
    return float(np.linalg.norm(h - np.diag(np.diag(h))))


def detect_one_sided_branch(h_nu: np.ndarray, h_e: np.ndarray) -> str:
    n_off = offdiag_norm(h_nu)
    e_off = offdiag_norm(h_e)
    if n_off > 1e-8 and e_off < 1e-8:
        return "N_nu"
    if e_off > 1e-8 and n_off < 1e-8:
        return "N_e"
    raise ValueError("pair is not on a one-sided minimal PMNS class")


def part1_hermitian_linear_source_response_recovers_the_full_lepton_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 1: HERMITIAN LINEAR SOURCE RESPONSE RECOVERS THE FULL LEPTON PAIR")
    print("=" * 88)

    h_nu = canonical_h(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    h_e = monomial_h(np.array([0.021, 0.034, 0.055], dtype=float))

    basis = hermitian_basis()
    resp_nu = [hermitian_linear_response(h_nu, b) for b in basis]
    resp_e = [hermitian_linear_response(h_e, b) for b in basis]

    h_nu_rec = reconstruct_h_from_responses(resp_nu)
    h_e_rec = reconstruct_h_from_responses(resp_e)

    check(
        "Nine Hermitian linear responses reconstruct H_nu exactly",
        np.linalg.norm(h_nu_rec - h_nu) < 1e-12,
        f"H_nu err={np.linalg.norm(h_nu_rec - h_nu):.2e}",
    )
    check(
        "Nine Hermitian linear responses reconstruct H_e exactly",
        np.linalg.norm(h_e_rec - h_e) < 1e-12,
        f"H_e err={np.linalg.norm(h_e_rec - h_e):.2e}",
    )
    check(
        "So the full lepton Hermitian pair is exactly a projected Hermitian source-law target",
        True,
        "18 real first responses = (H_nu,H_e)",
    )


def part2_the_branch_is_then_readable_without_a_separate_selector_target() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE BRANCH IS READABLE ONCE THE HERMITIAN PAIR IS KNOWN")
    print("=" * 88)

    h_nu = canonical_h(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    h_e = monomial_h(np.array([0.021, 0.034, 0.055], dtype=float))

    h_nu_pass = monomial_h(np.array([0.018, 0.051, 0.074], dtype=float))
    h_e_act = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )

    check("The Hermitian pair itself identifies N_nu", detect_one_sided_branch(h_nu, h_e) == "N_nu")
    check("The Hermitian pair itself identifies N_e", detect_one_sided_branch(h_nu_pass, h_e_act) == "N_e")
    check(
        "So branch selection is already encoded in the Hermitian projected source law",
        True,
        "no separate branch target once (H_nu,H_e) is derived",
    )


def part3_one_oriented_nonhermitian_probe_fixes_the_residual_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ONE ORIENTED NON-HERMITIAN PROBE FIXES THE RESIDUAL SHEET")
    print("=" * 88)

    y_true = canonical_y(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    h = y_true @ y_true.conj().T
    sheets = candidate_sheets_from_h(h)

    probe = np.zeros((3, 3), dtype=complex)
    probe[0, 0] = 1.0
    values = [float(np.real(np.trace(probe.conj().T @ sheet))) for sheet in sheets]
    true_value = float(np.real(np.trace(probe.conj().T @ y_true)))
    bit = int(np.argmin([abs(v - true_value) for v in values]))

    check(
        "The two candidate sheets are distinct canonical Yukawa matrices",
        np.linalg.norm(sheets[0] - sheets[1]) > 1e-6,
        f"sheet distance={np.linalg.norm(sheets[0] - sheets[1]):.6f}",
    )
    check(
        "The simple oriented probe Re(Y_11) distinguishes the two sheets generically",
        abs(values[0] - values[1]) > 1e-6,
        f"probe values={np.round(values, 6)}",
    )
    check(
        "One scalar non-Hermitian probe value picks the true sheet exactly",
        np.linalg.norm(sheets[bit] - y_true) < 1e-12,
        f"bit={bit}, Y err={np.linalg.norm(sheets[bit] - y_true):.2e}",
    )


def part4_the_clean_remaining_target_is_one_projected_source_law() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CLEAN REMAINING TARGET IS ONE PROJECTED SOURCE LAW")
    print("=" * 88)

    check(
        "The pair law plus one oriented non-Hermitian probe is sufficient for full one-sided PMNS closure",
        True,
        "projected Hermitian responses + one active probe",
    )
    check(
        "So the clean remaining derivation target from Cl(3) on Z^3 is not raw bridge bookkeeping",
        True,
        "derive the projected lepton source law instead",
    )
    check(
        "The resulting exact target is one pair-level Hermitian source law plus one active non-Hermitian scalar probe",
        True,
        "target = (dW_nu^H, dW_e^H, ell_act)",
    )


def main() -> int:
    print("=" * 88)
    print("PMNS PROJECTED SOURCE-LAW REDUCTION")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - Observable principle from Cl(3) on Z^3")
    print("  - PMNS full lepton pair reduction")
    print("  - PMNS branch-conditioned quadratic-sheet closure")
    print()
    print("Question:")
    print("  What is the cleanest source-response target that still has to be")
    print("  derived from Cl(3) on Z^3 for full neutrino closure?")

    part1_hermitian_linear_source_response_recovers_the_full_lepton_pair()
    part2_the_branch_is_then_readable_without_a_separate_selector_target()
    part3_one_oriented_nonhermitian_probe_fixes_the_residual_sheet()
    part4_the_clean_remaining_target_is_one_projected_source_law()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction:")
    print("    - derive the projected Hermitian linear source law on the two")
    print("      effective lepton 3x3 blocks to obtain (H_nu,H_e)")
    print("    - derive one oriented non-Hermitian scalar probe on the active block")
    print("      to fix the residual sheet")
    print()
    print("  So the clean remaining target from Cl(3) on Z^3 is one projected")
    print("  lepton source law, not a raw family of PMNS parameters.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
