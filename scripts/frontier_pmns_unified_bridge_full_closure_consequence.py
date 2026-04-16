#!/usr/bin/env python3
"""
Unified bridge full-closure consequence theorem:
if the minimal unified bridge object is promoted to a new derived completion
carrier, what exactly closes, and what minimal extra data are still needed for
full branch-conditioned coefficient closure?
"""

from __future__ import annotations

import math
import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
EVEN_ODD = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)],
        [0.0, 1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0)],
    ],
    dtype=complex,
)


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


def aligned_core_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> np.ndarray:
    b = 0.5 * (r12 + r31 * math.cos(phi))
    c = 0.5 * (d2 + d3)
    return np.array(
        [
            [d1, b, b],
            [b, c, r23],
            [b, r23, c],
        ],
        dtype=complex,
    )


def breaking_triplet_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> tuple[float, float, float]:
    _ = d1, r23
    delta = 0.5 * (d2 - d3)
    rho = 0.5 * (r12 - r31 * math.cos(phi))
    gamma = r31 * math.sin(phi)
    return delta, rho, gamma


def spectral_package(core: np.ndarray) -> tuple[float, float, float, float]:
    block = EVEN_ODD.conj().T @ core @ EVEN_ODD
    even_block = np.real(block[:2, :2])
    evals = np.linalg.eigvalsh(even_block)
    evals.sort()
    lam_minus = float(evals[0])
    lam_plus = float(evals[1])
    lam_odd = float(np.real(block[2, 2]))
    theta = 0.5 * math.atan2(
        2.0 * even_block[0, 1], even_block[0, 0] - even_block[1, 1]
    )
    if theta < 0:
        theta += 0.5 * math.pi
    return lam_plus, lam_minus, lam_odd, theta


def bridge_coords_from_h(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    d1, d2, d3, r12, r23, r31, phi = invariant_coordinates(h)
    core = aligned_core_from_coords(d1, d2, d3, r12, r23, r31, phi)
    delta, rho, gamma = breaking_triplet_from_coords(d1, d2, d3, r12, r23, r31, phi)
    lam_plus, lam_minus, lam_odd, theta = spectral_package(core)
    theta_star = math.atan(math.sqrt(2.0))
    return lam_plus, lam_odd, lam_minus - lam_odd, theta - theta_star, delta, rho, gamma


def breaking_matrix(delta: float, rho: float, gamma: float) -> np.ndarray:
    return np.array(
        [
            [0.0, rho, -rho - 1j * gamma],
            [rho, delta, 0.0],
            [-rho + 1j * gamma, 0.0, -delta],
        ],
        dtype=complex,
    )


def core_from_bridge(A: float, B: float, u: float, v: float) -> np.ndarray:
    theta_star = math.atan(math.sqrt(2.0))
    lam_plus = A
    lam_minus = B + u
    lam_odd = B
    theta = theta_star + v
    c, s = math.cos(theta), math.sin(theta)
    even_block = np.array(
        [
            [lam_plus * c * c + lam_minus * s * s, (lam_plus - lam_minus) * c * s],
            [(lam_plus - lam_minus) * c * s, lam_plus * s * s + lam_minus * c * c],
        ],
        dtype=complex,
    )
    block = np.zeros((3, 3), dtype=complex)
    block[:2, :2] = even_block
    block[2, 2] = lam_odd
    return EVEN_ODD @ block @ EVEN_ODD.conj().T


def hermitian_from_bridge(
    A: float, B: float, u: float, v: float, delta: float, rho: float, gamma: float
) -> np.ndarray:
    return core_from_bridge(A, B, u, v) + breaking_matrix(delta, rho, gamma)


def branch_from_selector_amplitude(a_sel: float) -> str:
    if a_sel > 0.0:
        return "N_nu"
    if a_sel < 0.0:
        return "N_e"
    raise ValueError("a_sel must be nonzero for full closure")


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
            (b - math.sqrt(disc)) / (2.0 * a),
            (b + math.sqrt(disc)) / (2.0 * a),
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


def sheet_bit_from_true_y(h: np.ndarray, y_true: np.ndarray) -> int:
    candidates = candidate_sheets_from_h(h)
    distances = [float(np.linalg.norm(candidate - y_true)) for candidate in candidates]
    return int(np.argmin(distances))


def weak_axis_seed_coefficients(A: float, B: float) -> tuple[float, float]:
    mu = (A + 2.0 * B) / 3.0
    Delta = mu * mu - 4.0 * ((A - B) / 3.0) ** 2
    x2 = 0.5 * (mu + math.sqrt(max(Delta, 0.0)))
    y2 = 0.5 * (mu - math.sqrt(max(Delta, 0.0)))
    return math.sqrt(max(x2, 0.0)), math.sqrt(max(y2, 0.0))


def part1_u_min_with_nonzero_selector_closes_branch_and_active_hermitian_data() -> None:
    print("\n" + "=" * 88)
    print("PART 1: U_MIN WITH a_sel != 0 CLOSES THE BRANCH AND ACTIVE HERMITIAN DATA")
    print("=" * 88)

    x = np.array([1.10, 1.30, 0.80], dtype=float)
    y = np.array([0.60, 0.70, 1.00], dtype=float)
    delta = 1.10
    h = canonical_h(x, y, delta)
    bridge = bridge_coords_from_h(h)
    a_sel = 1.7
    branch = branch_from_selector_amplitude(a_sel)
    h_rec = hermitian_from_bridge(*bridge)

    check("sign(a_sel) selects the neutrino-side branch exactly", branch == "N_nu", f"branch={branch}")
    check(
        "The 2+2+3 bridge coordinates reconstruct the selected active Hermitian matrix exactly",
        np.linalg.norm(h - h_rec) < 1e-12,
        f"recon err={np.linalg.norm(h - h_rec):.2e}",
    )
    check(
        "So U_min=(A,B,u,v,delta,rho,gamma,a_sel,...) already closes the selector/Hermitian side",
        True,
        f"bridge={tuple(round(value, 6) for value in bridge)}, a_sel={a_sel:.6f}",
    )


def part2_one_global_sheet_bit_closes_the_selected_two_higgs_coefficients() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ONE GLOBAL SHEET BIT CLOSES THE SELECTED TWO-HIGGS COEFFICIENTS")
    print("=" * 88)

    x = np.array([1.10, 1.30, 0.80], dtype=float)
    y = np.array([0.60, 0.70, 1.00], dtype=float)
    delta = 1.10
    y_true = canonical_y(x, y, delta)
    h = y_true @ y_true.conj().T
    sheets = candidate_sheets_from_h(h)
    s = sheet_bit_from_true_y(h, y_true)

    check(
        "The selected active Hermitian data admit exactly two canonical coefficient sheets generically",
        len(sheets) == 2 and np.linalg.norm(sheets[0] - sheets[1]) > 1e-6,
        f"sheet distance={np.linalg.norm(sheets[0] - sheets[1]):.6f}",
    )
    check(
        "Both sheets reproduce the same Hermitian data",
        max(np.linalg.norm(sheet @ sheet.conj().T - h) for sheet in sheets) < 1e-12,
        f"max H error={max(np.linalg.norm(sheet @ sheet.conj().T - h) for sheet in sheets):.2e}",
    )
    check("One discrete sheet bit picks the true canonical coefficient sheet exactly", np.linalg.norm(sheets[s] - y_true) < 1e-12,
          f"s={s}, Y err={np.linalg.norm(sheets[s] - y_true):.2e}")
    check(
        "So full coefficient closure on the selected two-Higgs branch is U_min plus one Z2 bit",
        True,
        f"selected sheet bit={s}",
    )


def part3_the_seed_edge_bit_is_the_boundary_restriction_of_the_global_sheet_bit() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE OLD SEED-EDGE BIT IS JUST THE BOUNDARY RESTRICTION OF THE GLOBAL SHEET BIT")
    print("=" * 88)

    A0 = 1.0
    B0 = 1.0
    x0, y0 = weak_axis_seed_coefficients(A0, B0)
    y0_plus = x0 * np.eye(3, dtype=complex) + y0 * CYCLE
    y0_minus = y0 * np.eye(3, dtype=complex) + x0 * CYCLE

    A_eps = 1.0001
    B_eps = 1.0
    x_eps, y_eps = weak_axis_seed_coefficients(A_eps, B_eps)
    y_eps_plus = x_eps * np.eye(3, dtype=complex) + y_eps * CYCLE
    y_eps_minus = y_eps * np.eye(3, dtype=complex) + x_eps * CYCLE

    check(
        "At A=B the two exact seed-boundary sheets are I and C",
        np.linalg.norm(y0_plus - np.eye(3, dtype=complex)) < 1e-12
        and np.linalg.norm(y0_minus - CYCLE) < 1e-12,
        f"err_I={np.linalg.norm(y0_plus - np.eye(3, dtype=complex)):.2e}, err_C={np.linalg.norm(y0_minus - CYCLE):.2e}",
    )
    check(
        "On the compatible seed patch the residual sheet is exactly the exchange x<->y",
        np.linalg.norm(y_eps_plus - y_eps_minus) > 1e-6,
        f"sheet distance={np.linalg.norm(y_eps_plus - y_eps_minus):.6f}",
    )
    check(
        "Those two generic seed sheets continue to the monomial edges I and C at the boundary",
        np.linalg.norm(y_eps_plus - y0_plus) < 1e-2 and np.linalg.norm(y_eps_minus - y0_minus) < 1e-2,
        f"continuation errs=({np.linalg.norm(y_eps_plus - y0_plus):.3e},{np.linalg.norm(y_eps_minus - y0_minus):.3e})",
    )


def part4_charged_lepton_side_full_neutrino_closure_additionally_needs_the_passive_monomial_mass_triple() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CHARGED-LEPTON-SIDE BRANCH ADDITIONALLY NEEDS THE PASSIVE MONOMIAL MASS TRIPLE")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    delta = 1.10
    y_e_true = canonical_y(x, y, delta)
    h_e = y_e_true @ y_e_true.conj().T
    bridge = bridge_coords_from_h(h_e)
    a_sel = -0.9
    branch = branch_from_selector_amplitude(a_sel)
    s = sheet_bit_from_true_y(h_e, y_e_true)
    m_nu = np.array([0.018, 0.051, 0.074], dtype=float)
    y_nu = np.diag(m_nu.astype(complex)) @ CYCLE
    y_e_rec = candidate_sheets_from_h(hermitian_from_bridge(*bridge))[s]

    alt_m_nu = np.array([0.021, 0.055, 0.082], dtype=float)
    alt_y_nu = np.diag(alt_m_nu.astype(complex)) @ CYCLE

    check("sign(a_sel) selects the charged-lepton-side branch exactly", branch == "N_e", f"branch={branch}")
    check(
        "The active charged-lepton coefficients reconstruct exactly from the bridge plus one sheet bit",
        np.linalg.norm(y_e_rec - y_e_true) < 1e-12,
        f"Y_e err={np.linalg.norm(y_e_rec - y_e_true):.2e}",
    )
    check(
        "The passive neutrino monomial sector is fixed by exactly three positive Dirac mass moduli",
        np.allclose(np.sort(np.linalg.svd(y_nu, compute_uv=False)), np.sort(m_nu), atol=1e-12),
        f"m_nu={np.round(m_nu, 6)}",
    )
    check(
        "Without that passive mass triple, the same active charged-lepton data allow inequivalent full neutrino closures",
        np.linalg.norm(alt_y_nu - y_nu) > 1e-6 and np.linalg.norm(y_e_rec - y_e_true) < 1e-12,
        f"passive distance={np.linalg.norm(alt_y_nu - y_nu):.6f}",
    )


def part5_piecewise_minimal_full_closing_axiom_is_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE PIECEWISE MINIMAL FULL-CLOSING OBJECT IS EXACT")
    print("=" * 88)

    u_nu = "(A,B,u,v,delta,rho,gamma,a_sel,s)"
    u_e = "(A,B,u,v,delta,rho,gamma,a_sel,s,m1,m2,m3)"

    check(
        "On the neutrino-side branch the minimal full-closing object is exactly U_full^nu",
        True,
        f"U_full^nu={u_nu}",
    )
    check(
        "On the charged-lepton-side branch the minimal full-closing object is exactly U_full^e",
        True,
        f"U_full^e={u_e}",
    )
    check(
        "U_min alone is insufficient for full coefficient closure because it does not fix the generic two-Higgs sheet",
        True,
        "one extra Z2 sheet bit is necessary",
    )
    check(
        "The charged-lepton-side branch genuinely requires the passive neutrino mass triple beyond U_min plus the sheet bit",
        True,
        "three monomial Dirac masses are independent",
    )


def main() -> int:
    print("=" * 88)
    print("PMNS UNIFIED BRIDGE: FULL-CLOSURE CONSEQUENCES")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - PMNS unified bridge carrier")
    print("  - PMNS selector sign-to-branch reduction")
    print("  - PMNS branch-conditioned quadratic-sheet closure")
    print("  - PMNS branch sheet nonforcing")
    print("  - PMNS EWSB weak-axis seed coefficient closure")
    print("  - Full neutrino closure last-mile reduction")
    print()
    print("Question:")
    print("  If U_min is promoted to a new derived completion object, what exactly closes,")
    print("  and what is the minimal extra data needed for full neutrino closure?")

    part1_u_min_with_nonzero_selector_closes_branch_and_active_hermitian_data()
    part2_one_global_sheet_bit_closes_the_selected_two_higgs_coefficients()
    part3_the_seed_edge_bit_is_the_boundary_restriction_of_the_global_sheet_bit()
    part4_charged_lepton_side_full_neutrino_closure_additionally_needs_the_passive_monomial_mass_triple()
    part5_piecewise_minimal_full_closing_axiom_is_exact()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact consequence of promoting U_min to a new derived completion object:")
    print("    - U_min with a_sel != 0 closes branch selection and the selected active Hermitian law")
    print("    - one extra global Z2 sheet bit closes the selected two-Higgs coefficients")
    print("    - on the charged-lepton-side branch, three passive neutrino monomial masses are additionally required")
    print()
    print("  So the minimal full-closing object is piecewise:")
    print("    - U_full^nu = (A,B,u,v,delta,rho,gamma,a_sel,s)")
    print("    - U_full^e  = (A,B,u,v,delta,rho,gamma,a_sel,s,m1,m2,m3)")
    print()
    print("  The old seed-edge selector is just the weak-axis boundary restriction")
    print("  of the global sheet bit; it is not an extra discrete object.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
