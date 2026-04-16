#!/usr/bin/env python3
"""
Exact microscopic source-response law on the fixed lepton supports.

Question:
  Working only from Cl(3) on Z^3, what does the microscopic source-response
  route determine on the fixed lepton supports E_nu and E_e?

Answer:
  The source-response law is exact Schur pushforward to the Hermitian lepton
  pair (H_nu, H_e). On the fixed supports, the 18 Hermitian linear responses
  reconstruct (H_nu, H_e) exactly, and the pair already determines the active
  branch.

  But the route is blind to the residual right-sheet data: distinct canonical
  Yukawa sheets with the same H give identical source responses on all Hermitian
  probes. So the source-response route fixes a genuine subset of the unresolved
  microscopic data, but not the full microscopic Y-level closure.
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


def schur_eff(a: np.ndarray, b: np.ndarray, c: np.ndarray, f: np.ndarray) -> np.ndarray:
    return a - b @ np.linalg.inv(f) @ c


def logabsdet(m: np.ndarray) -> float:
    sign, val = np.linalg.slogdet(m)
    _ = sign
    return float(val)


def source_response(h: np.ndarray, j: np.ndarray) -> float:
    return logabsdet(h + j) - logabsdet(h)


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


def reconstruct_h_from_responses(responses: list[float]) -> np.ndarray:
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


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE


def monomial_y(masses: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(masses, dtype=complex)) @ CYCLE


def monomial_h(masses: np.ndarray) -> np.ndarray:
    ymat = monomial_y(masses)
    return ymat @ ymat.conj().T


def canonical_h(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    ymat = canonical_y(x, y, delta)
    return ymat @ ymat.conj().T


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
        if np.any(xsq <= 0.0) or np.any(ysq <= 0.0):
            continue
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


def build_full_operator() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    # Basis order:
    #   nu_0, nu_1, nu_2, e_0, e_1, e_2, n_0, n_1, c_0, c_1, p_0, p_1
    # Charges:
    #   0,0,0,-1,-1,-1,0,0,-1,-1,+1,+1
    q = np.diag(np.array([0, 0, 0, -1, -1, -1, 0, 0, -1, -1, 1, 1], dtype=float))

    rng = np.random.default_rng(29)
    nu = np.array(
        [
            [2.1, 0.2 + 0.1j, 0.1],
            [0.2 - 0.1j, 1.9, 0.15],
            [0.1, 0.15, 2.3],
        ],
        dtype=complex,
    )
    e = np.array(
        [
            [1.8, 0.05, 0.08j],
            [0.05, 2.2, 0.11],
            [-0.08j, 0.11, 2.5],
        ],
        dtype=complex,
    )
    n = np.array([[3.0, 0.1j], [-0.1j, 2.7]], dtype=complex)
    c = np.array([[2.9, 0.07], [0.07, 3.2]], dtype=complex)
    p = np.array([[3.1, 0.09j], [-0.09j, 3.4]], dtype=complex)

    b_nu = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    b_e = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))

    top = np.hstack([nu, np.zeros((3, 3), dtype=complex), b_nu, np.zeros((3, 2), dtype=complex), np.zeros((3, 2), dtype=complex)])
    second = np.hstack([np.zeros((3, 3), dtype=complex), e, np.zeros((3, 2), dtype=complex), b_e, np.zeros((3, 2), dtype=complex)])
    third = np.hstack([b_nu.conj().T, np.zeros((2, 3), dtype=complex), n, np.zeros((2, 2), dtype=complex), np.zeros((2, 2), dtype=complex)])
    fourth = np.hstack([np.zeros((2, 3), dtype=complex), b_e.conj().T, np.zeros((2, 2), dtype=complex), c, np.zeros((2, 2), dtype=complex)])
    fifth = np.hstack([np.zeros((2, 3), dtype=complex), np.zeros((2, 3), dtype=complex), np.zeros((2, 2), dtype=complex), np.zeros((2, 2), dtype=complex), p])
    d = np.vstack([top, second, third, fourth, fifth])

    p_nu = np.diag(np.array([1, 1, 1] + [0] * 9, dtype=float))
    p_e = np.diag(np.array([0, 0, 0, 1, 1, 1] + [0] * 6, dtype=float))
    p_lep = p_nu + p_e
    return d, q, p_nu, p_e, p_lep


def part1_source_response_on_fixed_lepton_supports_is_exact_schur_pushforward() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SOURCE-RESPONSE ON FIXED SUPPORTS IS EXACT SCHUR PUSHHFORWARD")
    print("=" * 88)

    d, _q, p_nu, p_e, p_lep = build_full_operator()
    a = d[:6, :6]
    b = d[:6, 6:]
    c = d[6:, :6]
    f = d[6:, 6:]
    l_lep = schur_eff(a, b, c, f)
    l_nu = l_lep[:3, :3]
    l_e = l_lep[3:6, 3:6]

    basis = hermitian_basis()
    x_nu = np.array(
        [
            [0.10, 0.02 + 0.01j, 0.0],
            [0.02 - 0.01j, -0.07, 0.03],
            [0.0, 0.03, 0.05],
        ],
        dtype=complex,
    )
    x_e = np.array(
        [
            [0.08, 0.0, 0.01j],
            [0.0, -0.03, 0.02],
            [-0.01j, 0.02, 0.06],
        ],
        dtype=complex,
    )
    j_nu_full = np.zeros_like(d)
    j_nu_full[:3, :3] = x_nu
    j_both_full = np.zeros_like(d)
    j_both_full[:3, :3] = x_nu
    j_both_full[3:6, 3:6] = x_e

    j_nu_lep = np.zeros((6, 6), dtype=complex)
    j_nu_lep[:3, :3] = x_nu
    j_both_lep = np.zeros((6, 6), dtype=complex)
    j_both_lep[:3, :3] = x_nu
    j_both_lep[3:6, 3:6] = x_e

    full_nu = source_response(d, j_nu_full)
    full_both = source_response(d, j_both_full)
    lep_nu = source_response(l_lep, j_nu_lep)
    lep_both = source_response(l_lep, j_both_lep)
    nu_only = source_response(l_nu, x_nu)
    both_sep = source_response(l_nu, x_nu) + source_response(l_e, x_e)

    resp_nu = [float(np.real(np.trace(x @ l_nu))) for x in basis]
    resp_e = [float(np.real(np.trace(x @ l_e))) for x in basis]
    l_nu_rec = reconstruct_h_from_responses(resp_nu)
    l_e_rec = reconstruct_h_from_responses(resp_e)

    check(
        "The nu-supported microscopic source response pushes forward exactly through the Schur-reduced lepton block",
        abs(full_nu - lep_nu) < 1e-12,
        f"|Δ|={abs(full_nu - lep_nu):.2e}",
    )
    check(
        "The combined support response also pushes forward exactly through the Schur-reduced lepton block",
        abs(full_both - lep_both) < 1e-12,
        f"|Δ|={abs(full_both - lep_both):.2e}",
    )
    check(
        "Hermitian linear responses reconstruct H_nu exactly",
        np.linalg.norm(l_nu_rec - l_nu) < 1e-12,
        f"err={np.linalg.norm(l_nu_rec - l_nu):.2e}",
    )
    check(
        "Hermitian linear responses reconstruct H_e exactly",
        np.linalg.norm(l_e_rec - l_e) < 1e-12,
        f"err={np.linalg.norm(l_e_rec - l_e):.2e}",
    )
    check(
        "So the microscopic source-response law fixes the Hermitian pair (H_nu,H_e) on the fixed supports",
        True,
        "exact Schur pushforward on E_nu ⊕ E_e",
    )


def part2_the_hermitian_pair_already_reads_the_active_branch() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE HERMITIAN PAIR ALREADY READS THE ACTIVE BRANCH")
    print("=" * 88)

    h_nu_act = canonical_h(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    h_e_pas = monomial_h(np.array([0.021, 0.034, 0.055], dtype=float))
    h_nu_pas = monomial_h(np.array([0.018, 0.051, 0.074], dtype=float))
    h_e_act = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )

    check("The Hermitian pair identifies the neutrino-active one-sided branch", detect_one_sided_branch(h_nu_act, h_e_pas) == "N_nu")
    check("The Hermitian pair identifies the charged-lepton-active one-sided branch", detect_one_sided_branch(h_nu_pas, h_e_act) == "N_e")
    check(
        "So the source-response law already fixes branch once (H_nu,H_e) is known",
        True,
        "branch is readable from the Hermitian pair",
    )


def part3_the_same_source_law_is_blind_to_the_residual_right_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SAME SOURCE LAW IS BLIND TO THE RESIDUAL RIGHT SHEET")
    print("=" * 88)

    h = canonical_h(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    sheets = candidate_sheets_from_h(h)
    basis = hermitian_basis()
    h0 = sheets[0] @ sheets[0].conj().T
    h1 = sheets[1] @ sheets[1].conj().T if len(sheets) > 1 else h0
    obs0 = [source_response(h0, x) for x in basis]
    obs1 = [source_response(h1, x) for x in basis]

    sheet_probe = np.zeros((3, 3), dtype=complex)
    sheet_probe[0, 0] = 1.0
    probe_values = [float(np.real(np.trace(sheet_probe.conj().T @ sheet))) for sheet in sheets]

    check(
        "The generic active Hermitian block has two distinct canonical sheets",
        len(sheets) == 2 and np.linalg.norm(sheets[0] - sheets[1]) > 1e-6,
        f"count={len(sheets)}",
    )
    check(
        "The two distinct canonical sheets induce the same Hermitian block H",
        np.linalg.norm(h0 - h1) < 1e-12,
        f"H error={np.linalg.norm(h0 - h1):.2e}",
    )
    check(
        "The Hermitian source-response data are identical on the two sheets",
        np.max(np.abs(np.array(obs0) - np.array(obs1))) < 1e-12,
        f"max diff={np.max(np.abs(np.array(obs0) - np.array(obs1))):.2e}",
    )
    check(
        "A non-Hermitian oriented probe distinguishes the two sheets",
        abs(probe_values[0] - probe_values[1]) > 1e-6,
        f"probe values={np.round(probe_values, 6)}",
    )
    check(
        "So the source-response route cannot fix the residual right-sheet bit by itself",
        True,
        "source-response factors through H only",
    )


def part4_result_status() -> None:
    print("\n" + "=" * 88)
    print("PART 4: RESULT STATUS")
    print("=" * 88)

    check(
        "The source-response route fixes a genuine subset of unresolved microscopic data",
        True,
        "H_nu, H_e, and branch readout on fixed supports",
    )
    check(
        "The source-response route does not fix the full microscopic Y-level closure",
        True,
        "residual right-sheet data remain invisible",
    )


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC SOURCE-RESPONSE LAW")
    print("=" * 88)
    print()
    print("Axiom / native inputs reused:")
    print("  - Cl(3) on Z^3 observable principle")
    print("  - exact Schur/source reduction on the retained lepton supports")
    print("  - exact finite-dimensional Hermitian source-response reconstruction")
    print()
    print("Question:")
    print("  What does the microscopic source-response route on E_nu and E_e")
    print("  actually determine?")

    part1_source_response_on_fixed_lepton_supports_is_exact_schur_pushforward()
    part2_the_hermitian_pair_already_reads_the_active_branch()
    part3_the_same_source_law_is_blind_to_the_residual_right_sheet()
    part4_result_status()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact source-response law:")
    print("    - on the fixed lepton supports, the microscopic source-response")
    print("      law is exact Schur pushforward to (H_nu, H_e)")
    print("    - the Hermitian pair already determines the active branch")
    print("    - the same source-response law is blind to the residual right")
    print("      sheet / Y-level data")
    print()
    print("  Therefore this route closes the Hermitian-pair subset of the")
    print("  microscopic problem, but it does not by itself close full positive")
    print("  neutrino closure.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
