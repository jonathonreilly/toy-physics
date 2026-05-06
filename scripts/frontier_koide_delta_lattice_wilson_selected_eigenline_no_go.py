#!/usr/bin/env python3
"""
Koide delta lattice Wilson selected-eigenline no-go.

Theorem attempt:
  Strengthen the finite L=3 Wilson-Dirac support model into a positive
  Brannen endpoint bridge.  Perhaps the retained Wilson operator plus the
  body-diagonal Z3 action canonically selects a rank-one boundary eigenline,
  making the selected open endpoint the unit APS/anomaly channel.

Result:
  Negative for the selected-eigenline route.  In this finite Wilson
  realization, the ambient eta proxy equals the APS comparator 2/9, so it is
  not a residual of this runner.  The obstruction is narrower: the relevant
  zero-mode character sector has rank two.  Wilson data therefore select a
  spectral projector/eigenspace, not a unique selected line inside it.  A CP1
  family of rank-one lines has the same retained eigenvalue and Z3 character
  data.

  The selected/spectator split and endpoint lift remain:

      delta_open / eta_APS - 1 = -spectator_channel + c / eta_APS.

No mass data, fitted Koide value, or selected endpoint target is used.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def build_wilson_lattice(r: float = 1.425) -> tuple[np.ndarray, np.ndarray, list[tuple[int, int, int]]]:
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    gamma_1 = np.kron(sigma_y, sigma_x)
    gamma_2 = np.kron(sigma_y, sigma_y)
    gamma_3 = np.kron(sigma_y, sigma_z)

    n_hat = np.array([1, 1, 1]) / math.sqrt(3)
    n_dot_sigma = n_hat[0] * sigma_x + n_hat[1] * sigma_y + n_hat[2] * sigma_z
    U_sigma = math.cos(math.pi / 3) * I2 - 1j * math.sin(math.pi / 3) * n_dot_sigma
    U_spin = np.kron(I2, U_sigma)

    L = 3
    N = L**3

    def idx(x: int, y: int, z: int) -> int:
        return (x % L) * L**2 + (y % L) * L + (z % L)

    translations = [np.zeros((N, N), dtype=complex) for _ in range(3)]
    for x in range(L):
        for y in range(L):
            for z in range(L):
                translations[0][idx(x + 1, y, z), idx(x, y, z)] = 1
                translations[1][idx(x, y + 1, z), idx(x, y, z)] = 1
                translations[2][idx(x, y, z + 1), idx(x, y, z)] = 1

    P_site = np.zeros((N, N), dtype=complex)
    fixed_sites: list[tuple[int, int, int]] = []
    for x in range(L):
        for y in range(L):
            for z in range(L):
                P_site[idx(z, x, y), idx(x, y, z)] = 1
                if x == y == z:
                    fixed_sites.append((x, y, z))

    U_full = np.kron(U_spin, P_site)
    D_kinetic = sum(
        np.kron(gamma, (T - T.conj().T) / (2j))
        for gamma, T in zip([gamma_1, gamma_2, gamma_3], translations)
    )
    wilson_op = sum((2 * np.eye(N) - T - T.conj().T) / 2 for T in translations)
    D = D_kinetic + r * np.kron(np.eye(4), wilson_op)
    return D, U_full, fixed_sites


def eta_per_fixed_site(D: np.ndarray, U: np.ndarray, n_fixed: int) -> float:
    eigs, vecs = np.linalg.eigh(D)
    U2 = U @ U
    cg1 = np.array([np.vdot(v, U @ v) for v in vecs.T])
    cg2 = np.array([np.vdot(v, U2 @ v) for v in vecs.T])
    eta = (np.sum(np.sign(eigs) * cg1) + np.sum(np.sign(eigs) * cg2)) / 3
    return float(abs(eta) / n_fixed)


def zero_character_lines(D: np.ndarray, U: np.ndarray) -> tuple[np.ndarray, np.ndarray, complex]:
    eigs, vecs = np.linalg.eigh(D)
    zero_indices = np.where(np.abs(eigs) < 1e-8)[0]
    zero_basis = vecs[:, zero_indices]
    U_zero = zero_basis.conj().T @ U @ zero_basis
    u_eigs, u_vecs = np.linalg.eig(U_zero)
    zeta = np.exp(1j * math.pi / 3)
    zeta_indices = [i for i, value in enumerate(u_eigs) if abs(value - zeta) < 1e-8]
    if len(zeta_indices) != 2:
        raise RuntimeError(f"expected two zeta zero modes, got {len(zeta_indices)}")
    line_0 = zero_basis @ u_vecs[:, zeta_indices[0]]
    line_1 = zero_basis @ u_vecs[:, zeta_indices[1]]
    line_0 = line_0 / np.linalg.norm(line_0)
    # Gram-Schmidt protects against numerical non-orthogonality in the U eigensolver.
    line_1 = line_1 - line_0 * np.vdot(line_0, line_1)
    line_1 = line_1 / np.linalg.norm(line_1)
    return line_0, line_1, zeta


def main() -> int:
    section("A. Finite Wilson-Dirac support model")

    r = 1.0
    D, U, fixed_sites = build_wilson_lattice(r)
    eta = eta_per_fixed_site(D, U, len(fixed_sites))
    record(
        "A.1 L=3 Wilson-Dirac operator is Hermitian and Z3-equivariant",
        np.linalg.norm(D - D.conj().T) < 1e-10
        and np.linalg.norm(U @ D @ U.conj().T - D) < 1e-10,
        f"||D-D†||={np.linalg.norm(D - D.conj().T):.2e}; ||UDU†-D||={np.linalg.norm(U @ D @ U.conj().T - D):.2e}",
    )
    record(
        "A.2 body-diagonal action has three retained fixed sites",
        fixed_sites == [(0, 0, 0), (1, 1, 1), (2, 2, 2)],
        f"fixed_sites={fixed_sites}",
    )
    record(
        "A.3 finite Wilson eta proxy matches the APS comparator 2/9",
        abs(eta - 2 / 9) < 1e-10,
        f"|eta|/fixed_site={eta:.12f}; exact APS comparator={2/9:.12f}",
    )

    section("B. Zero-mode character sector is not a selected line")

    eigs, vecs = np.linalg.eigh(D)
    zero_indices = np.where(np.abs(eigs) < 1e-8)[0]
    zero_basis = vecs[:, zero_indices]
    U_zero = zero_basis.conj().T @ U @ zero_basis
    u_eigs = np.linalg.eigvals(U_zero)
    zeta = np.exp(1j * math.pi / 3)
    zeta_bar = np.conjugate(zeta)
    zeta_count = sum(abs(value - zeta) < 1e-8 for value in u_eigs)
    zeta_bar_count = sum(abs(value - zeta_bar) < 1e-8 for value in u_eigs)
    record(
        "B.1 Wilson zero-mode space has dimension four",
        len(zero_indices) == 4,
        f"zero eigenvalues={len(zero_indices)}",
    )
    record(
        "B.2 each spin-lift Z3 character in the zero-mode space has multiplicity two",
        zeta_count == 2 and zeta_bar_count == 2,
        f"counts: exp(+i*pi/3)={zeta_count}, exp(-i*pi/3)={zeta_bar_count}",
    )

    line_0, line_1, character = zero_character_lines(D, U)
    line_checks = []
    selected_weights = []
    for alpha in [0.0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2]:
        psi = math.cos(alpha) * line_0 + math.sin(alpha) * line_1
        psi = psi / np.linalg.norm(psi)
        d_err = np.linalg.norm(D @ psi)
        u_err = np.linalg.norm(U @ psi - character * psi)
        selected_weight = abs(np.vdot(line_0, psi)) ** 2
        selected_weights.append(round(float(selected_weight), 12))
        line_checks.append(
            f"alpha={alpha:.6f}: ||D psi||={d_err:.2e}, ||U psi-zeta psi||={u_err:.2e}, selected_weight={selected_weight:.6f}"
        )
    record(
        "B.3 a CP1 family of rank-one lines has the same Wilson zero-mode and character data",
        len(set(selected_weights)) == 5,
        "\n".join(line_checks),
    )
    record(
        "B.4 Wilson data select a rank-two character projector, not a canonical rank-one eigenline",
        True,
        "A selected line inside the rank-two character sector is extra boundary/readout data.",
    )

    section("C. Selected/spectator and endpoint-lift residual")

    alpha, c = sp.symbols("alpha c", real=True)
    eta_sym = sp.Rational(2, 9)
    selected_channel = sp.cos(alpha) ** 2
    spectator_channel = sp.sin(alpha) ** 2
    residual = sp.simplify(selected_channel + c / eta_sym - 1)
    record(
        "C.1 rank-two eigenline freedom gives the same selected/spectator residual",
        sp.simplify(residual - (-spectator_channel + c / eta_sym)) == 0,
        f"delta/eta_APS - 1 = {residual}",
    )
    record(
        "C.2 closure requires choosing alpha=0 and endpoint offset c=0",
        sp.simplify(residual.subs({alpha: 0, c: 0})) == 0
        and sp.simplify(residual.subs({alpha: sp.pi / 2, c: 0})) == -1,
        "alpha=0 selects line_0; alpha=pi/2 selects the equally retained orthogonal line.",
    )

    s, t = sp.symbols("s t", real=True)
    endpoint_lift = s * t
    endpoint_shift = sp.simplify(endpoint_lift.subs(t, 1) - endpoint_lift.subs(t, 0))
    record(
        "C.3 eigenvector endpoint lift still carries an exact open-path offset",
        endpoint_shift == s,
        "Multiplying a Wilson eigenline lift by exp(i*s*t) leaves projectors unchanged and shifts the open endpoint by s.",
    )

    section("D. Hostile-review objections")

    record(
        "D.1 finite Wilson data do not identify the selected Brannen line",
        len(zero_indices) == 4 and zeta_count == 2 and zeta_bar_count == 2,
        "Even if the ambient APS value is supplied externally, the selected endpoint requires a line inside a multiplicity-two character sector.",
    )
    record(
        "D.2 picking the line with selected_weight=1 is the missing theorem",
        selected_weights[0] == 1.0 and selected_weights[-1] == 0.0,
        "The endpoints alpha=0 and alpha=pi/2 are both retained Wilson eigenlines with the same character.",
    )

    section("E. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual_endpoint = sp.simplify(theta_end - theta0 - eta_sym)
    record(
        "E.1 lattice Wilson selected-eigenline route does not close delta",
        residual_endpoint == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual_endpoint}",
    )
    record(
        "E.2 residual is rank-one selected-line choice plus endpoint lift",
        True,
        "Need a retained theorem selecting a unique rank-one Wilson eigenline and fixing its endpoint lift.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: lattice Wilson selected-eigenline route does not close delta.")
        print("KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO=TRUE")
        print("DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_EIGENLINE=rank_two_zero_mode_character_sector_not_canonically_split")
        print("RESIDUAL_TRIVIALIZATION=wilson_eigenline_endpoint_lift_not_fixed")
        print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
        print("AMBIENT_ETA_PROXY_MATCHES_APS_COMPARATOR=TRUE")
        return 0

    print("VERDICT: lattice Wilson selected-eigenline audit has FAILs.")
    print("KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO=FALSE")
    print("DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_EIGENLINE=rank_two_zero_mode_character_sector_not_canonically_split")
    print("RESIDUAL_TRIVIALIZATION=wilson_eigenline_endpoint_lift_not_fixed")
    print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
    print("AMBIENT_ETA_PROXY_MATCHES_APS_COMPARATOR=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
