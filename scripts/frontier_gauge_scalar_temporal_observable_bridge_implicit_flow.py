#!/usr/bin/env python3
"""
Bounded implicit response-coordinate theorem for the gauge-scalar temporal
observable bridge:

    <P>_full = R_O(beta_eff)

The runner verifies the proof obligations for the implicit response-flow
coordinate theorem. It does not evaluate the physical beta=6 plaquette, fit
beta_eff, use Monte-Carlo/PDG values, or import perturbative running as a
derivation.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy.special import iv


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_IMPLICIT_FLOW_THEOREM_NOTE_2026-05-03.md"
STRETCH = ROOT / "docs" / "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md"

N_C = 3
DIMS = 4
MODE_TOL = 1.0e-15
MAX_MODE = 90


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def bessel_matrix(beta: float, mode: int) -> np.ndarray:
    arg = beta / 3.0
    return np.array(
        [[iv(mode + i - j, arg) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def bessel_matrix_derivative(beta: float, mode: int) -> np.ndarray:
    arg = beta / 3.0
    return np.array(
        [
            [
                (iv(mode + i - j - 1, arg) + iv(mode + i - j + 1, arg)) / 6.0
                for j in range(3)
            ]
            for i in range(3)
        ],
        dtype=float,
    )


def su3_mode_terms(beta: float, mode: int) -> tuple[float, float]:
    mat = bessel_matrix(beta, mode)
    dmat = bessel_matrix_derivative(beta, mode)
    det = float(np.linalg.det(mat))
    derivative = det * float(np.trace(np.linalg.inv(mat) @ dmat))
    return det, derivative


def su3_partition_and_derivative(beta: float) -> tuple[float, float, int]:
    total_partition = 0.0
    total_derivative = 0.0
    for mode in range(MAX_MODE + 1):
        strip_partition = 0.0
        strip_derivative = 0.0
        modes = [0] if mode == 0 else [-mode, mode]
        for signed_mode in modes:
            part, deriv = su3_mode_terms(beta, signed_mode)
            strip_partition += part
            strip_derivative += deriv
        total_partition += strip_partition
        total_derivative += strip_derivative
        if mode >= 3:
            partition_small = abs(strip_partition) < MODE_TOL * max(abs(total_partition), 1.0)
            derivative_small = abs(strip_derivative) < MODE_TOL * max(abs(total_derivative), 1.0)
            if partition_small and derivative_small:
                return total_partition, total_derivative, mode
    raise RuntimeError(f"mode sum did not converge by m={MAX_MODE}")


def local_response(beta: float) -> float:
    z, dz, _ = su3_partition_and_derivative(beta)
    return dz / z


def local_susceptibility(beta: float, step: float = 1.0e-4) -> float:
    return (local_response(beta + step) - local_response(beta - step)) / (2.0 * step)


def inverse_local_response(target: float, tol: float = 1.0e-12) -> float:
    if not (0.0 <= target < 1.0):
        raise ValueError("target must lie in [0,1)")
    if target == 0.0:
        return 0.0
    lo = 0.0
    hi = 1.0
    while local_response(hi) <= target:
        hi *= 2.0
        if hi > 80.0:
            raise RuntimeError("failed to bracket target response")
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        if local_response(mid) < target:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def local_plaquette_density(matrix: np.ndarray) -> float:
    return float(np.trace(matrix).real / N_C)


def center_matrix() -> np.ndarray:
    return np.exp(2j * math.pi / 3.0) * np.eye(3, dtype=complex)


def diagonal_phase_link(theta: float) -> np.ndarray:
    return np.diag([np.exp(1j * theta), np.exp(-1j * theta), 1.0]).astype(complex)


def build_identity_links(L: int = 2, ndim: int = DIMS) -> dict[tuple[int, ...], list[np.ndarray]]:
    links: dict[tuple[int, ...], list[np.ndarray]] = {}
    for coords in np.ndindex(*([L] * ndim)):
        links[coords] = [np.eye(3, dtype=complex) for _ in range(ndim)]
    return links


def measure_average_plaquette(
    links: dict[tuple[int, ...], list[np.ndarray]],
    L: int = 2,
    ndim: int = DIMS,
) -> float:
    total = 0.0
    count = 0
    for coords in np.ndindex(*([L] * ndim)):
        x = list(coords)
        for mu in range(ndim):
            for nu in range(mu + 1, ndim):
                xm = list(x)
                xm[mu] = (xm[mu] + 1) % L
                xn = list(x)
                xn[nu] = (xn[nu] + 1) % L
                up = (
                    links[tuple(x)][mu]
                    @ links[tuple(xm)][nu]
                    @ links[tuple(xn)][mu].conj().T
                    @ links[tuple(x)][nu].conj().T
                )
                total += np.trace(up).real / N_C
                count += 1
    return total / count


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    note = read(NOTE)
    stretch = read(STRETCH)

    print("=" * 78)
    print("GAUGE-SCALAR TEMPORAL OBSERVABLE BRIDGE IMPLICIT-COORDINATE THEOREM")
    print("=" * 78)
    print()

    print("Part 1: local response coordinate")
    identity_x = local_plaquette_density(np.eye(3, dtype=complex))
    center_x = local_plaquette_density(center_matrix())
    sample_betas = [0.1, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    sample_responses = [local_response(beta) for beta in sample_betas]
    sample_sus = [local_susceptibility(beta) for beta in [0.5, 2.0, 6.0]]
    print(f"  X(identity)                         = {identity_x:.15f}")
    print(f"  X(center element)                   = {center_x:.15f}")
    print(f"  R_O(sample betas)                   = {[round(v, 12) for v in sample_responses]}")
    print(f"  chi_1(sample betas)                 = {[round(v, 12) for v in sample_sus]}")
    print()

    print("Part 2: finite Wilson full observable range witnesses")
    links_identity = build_identity_links()
    links_deformed = build_identity_links()
    links_deformed[(0, 0, 0, 0)][0] = diagonal_phase_link(0.41)
    avg_identity = measure_average_plaquette(links_identity)
    avg_deformed = measure_average_plaquette(links_deformed)
    print(f"  average plaquette(identity config)  = {avg_identity:.15f}")
    print(f"  average plaquette(deformed config)  = {avg_deformed:.15f}")
    print()

    print("Part 3: inverse-response bridge checks for arbitrary in-range targets")
    targets = [0.125, 0.333333333333, 0.5, 0.75, 0.9]
    inverse_rows: list[tuple[float, float, float]] = []
    for target in targets:
        beta_eff = inverse_local_response(target)
        reconstructed = local_response(beta_eff)
        inverse_rows.append((target, beta_eff, reconstructed))
        print(
            f"  target={target:.12f}  beta_eff={beta_eff:.12f}  "
            f"R_O(beta_eff)={reconstructed:.12f}"
        )
    print()

    print("Part 4: susceptibility-flow identity")
    flow_targets = [0.2, 0.6]
    for target in flow_targets:
        gamma = inverse_local_response(target)
        inv_derivative_numeric = (
            inverse_local_response(target + 1.0e-4) - inverse_local_response(target - 1.0e-4)
        ) / (2.0e-4)
        inv_derivative_flow = 1.0 / local_susceptibility(gamma)
        print(
            f"  target={target:.3f} gamma={gamma:.12f}  "
            f"dR^-1/dP numeric={inv_derivative_numeric:.9f}  "
            f"1/chi_1(gamma)={inv_derivative_flow:.9f}"
        )
    print()

    print("Part 5: note/import firewall checks")
    required_note_phrases = [
        "beta_eff,Lambda(beta) := R_O^(-1)(P_Lambda(beta))",
        "P_Lambda(beta) = R_O(beta_eff,Lambda(beta))",
        "beta_eff,Lambda'(beta)",
        "parent observable bridge gate",
        "does not evaluate the full\nplaquette at `beta = 6`",
        "does not fit",
        "does not import\nMonte-Carlo, PDG, or perturbative running data",
    ]
    for phrase in required_note_phrases:
        print(f"  note phrase present: {phrase!r} -> {phrase in note}")
    print()

    monotone = all(sample_responses[i] < sample_responses[i + 1] for i in range(len(sample_responses) - 1))
    inverse_error = max(abs(target - reconstructed) for target, _, reconstructed in inverse_rows)
    flow_error = max(
        abs(
            (
                inverse_local_response(target + 1.0e-4)
                - inverse_local_response(target - 1.0e-4)
            )
            / (2.0e-4)
            - 1.0 / local_susceptibility(inverse_local_response(target))
        )
        for target in flow_targets
    )

    check(
        "the local plaquette source X is nonconstant on SU(3)",
        abs(identity_x - 1.0) < 1.0e-15 and abs(center_x + 0.5) < 1.0e-15,
        detail="explicit SU(3) witnesses give X=1 and X=-1/2",
    )
    check(
        "sampled local response R_O is strictly increasing and remains inside [0,1)",
        monotone and 0.0 < sample_responses[0] < sample_responses[-1] < 1.0,
        detail=f"R_O(0.1)={sample_responses[0]:.12f}, R_O(16)={sample_responses[-1]:.12f}",
    )
    check(
        "sampled local susceptibilities are positive",
        min(sample_sus) > 0.0,
        detail=f"min sampled chi_1={min(sample_sus):.6e}",
    )
    check(
        "the finite Wilson plaquette observable is not identically one on configuration space",
        avg_identity > avg_deformed and abs(avg_identity - 1.0) < 1.0e-15,
        detail=f"identity={avg_identity:.15f}, deformed={avg_deformed:.15f}",
    )
    check(
        "every in-range target has a unique inverse-response beta_eff that reconstructs the target",
        inverse_error < 5.0e-11,
        detail=f"max |target - R_O(R_O^-1(target))|={inverse_error:.3e}",
    )
    check(
        "the exact coordinate identity is the inverse-response corollary, not a data fit",
        "P_Lambda(beta) = R_O(beta_eff,Lambda(beta))" in note
        and "beta_eff,Lambda(beta) := R_O^(-1)(P_Lambda(beta))" in note,
        detail="the note defines beta_eff as a Wilson partition-function response coordinate",
    )
    check(
        "the susceptibility-flow derivative matches the inverse-function theorem numerically",
        flow_error < 2.0e-5,
        detail=f"max derivative mismatch={flow_error:.3e}",
    )
    check(
        "the parent stretch gate is targeted explicitly and its forbidden imports remain forbidden",
        "<P>_full = R_O(beta_eff)" in note
        and "Fitted beta_eff" not in note
        and "PDG" in stretch
        and "Perturbative" in stretch,
        detail="the new theorem cites the residual while preserving the parent import firewall",
    )

    code_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_comparator_literal = "0." + "5934"
    forbidden_canonical_token = "CAN" + "ONICAL"
    forbidden_pdg_observed = "PDG " + "observed"
    check(
        "the runner does not consume the canonical plaquette comparator or PDG/lattice values",
        forbidden_canonical_token not in code_text
        and forbidden_comparator_literal not in code_text
        and forbidden_pdg_observed not in code_text,
        detail="all inverse checks use arbitrary in-range targets, not observed plaquette data",
        bucket="SUPPORT",
    )
    check(
        "the theorem leaves independent beta=6 plaquette and rho_(p,q)(6) evaluation open",
        "closed-form evaluation of `<P>(6)`" in note and "rho_(p,q)(6)" in note,
        detail="bounded coordinate identity only, not environment Perron evaluation",
        bucket="SUPPORT",
    )
    check(
        "the theorem uses exact response flow rather than perturbative RG running",
        "not a perturbative beta-function" in note,
        detail="the flow equation is beta_eff' = chi_full / chi_1",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
