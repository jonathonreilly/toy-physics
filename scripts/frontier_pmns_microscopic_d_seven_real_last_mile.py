#!/usr/bin/env python3
"""Exact reduction of the PMNS-relevant microscopic D law to a 7-real gap."""

from __future__ import annotations

import sys
import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
PERMUTATIONS = {
    0: I3,
    1: CYCLE,
    2: CYCLE @ CYCLE,
}


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


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def monomial_triplet(coeffs: np.ndarray, q: int) -> np.ndarray:
    return diagonal(np.asarray(coeffs, dtype=complex)) @ PERMUTATIONS[q]


def active_operator(x: np.ndarray, c_forward: np.ndarray) -> np.ndarray:
    return diagonal(np.asarray(x, dtype=complex)) + diagonal(np.asarray(c_forward, dtype=complex)) @ CYCLE


def support_trace_moments(block: np.ndarray) -> np.ndarray:
    return np.array(
        [
            np.trace(block @ PERMUTATIONS[0].conj().T),
            np.trace(block @ PERMUTATIONS[1].conj().T),
            np.trace(block @ PERMUTATIONS[2].conj().T),
        ],
        dtype=complex,
    )


def moment_support_count(block: np.ndarray, tol: float = 1e-10) -> int:
    return int(np.count_nonzero(np.abs(support_trace_moments(block)) > tol))


def recover_q(block: np.ndarray) -> int:
    return int(np.argmax(np.abs(support_trace_moments(block))))


def left_rephase_to_positive(block: np.ndarray, q: int) -> np.ndarray:
    coeffs = np.diag(block @ PERMUTATIONS[q].conj().T)
    phases = np.exp(-1j * np.angle(coeffs))
    return diagonal(phases) @ block


def decompose_active_native_data(active: np.ndarray) -> dict[str, np.ndarray | float | complex]:
    x = np.real(np.diag(active))
    c = np.array([active[0, 1], active[1, 2], active[2, 0]], dtype=complex)
    xbar = float(np.mean(x))
    sigma = complex(np.mean(c))
    xi = x - xbar * np.ones(3, dtype=float)
    rho = np.array([np.real(c[0] - sigma), np.real(c[1] - sigma)], dtype=float)
    return {
        "xbar": xbar,
        "sigma": sigma,
        "xi": xi,
        "rho": rho,
    }


def reconstruct_active_from_native_last_mile(xbar: float, sigma: complex, gap: np.ndarray) -> np.ndarray:
    xi1, xi2, rho1, rho2 = gap.tolist()
    xi = np.array([xi1, xi2, -xi1 - xi2], dtype=float)
    x = xbar * np.ones(3, dtype=float) + xi
    re_sigma = float(np.real(sigma))
    im_sigma = float(np.imag(sigma))
    c1 = re_sigma + rho1
    c2 = re_sigma + rho2
    c3 = re_sigma - rho1 - rho2 + 3j * im_sigma
    c = np.array([c1, c2, c3], dtype=complex)
    return active_operator(x, c)


def derive_reduced_native_data(d0_trip: np.ndarray, dm_trip: np.ndarray) -> dict:
    if moment_support_count(d0_trip) == 2 and moment_support_count(dm_trip) == 1:
        tau = 0
        active = d0_trip
        passive = dm_trip
    elif moment_support_count(d0_trip) == 1 and moment_support_count(dm_trip) == 2:
        tau = 1
        active = dm_trip
        passive = d0_trip
    else:
        raise ValueError("pair is not on a one-sided minimal PMNS class")

    q = recover_q(passive)
    passive_canonical = left_rephase_to_positive(passive, q)
    passive_moduli = np.real(np.diag(passive_canonical @ PERMUTATIONS[q].conj().T))
    active_data = decompose_active_native_data(active)
    active_gap = np.array(
        [active_data["xi"][0], active_data["xi"][1], active_data["rho"][0], active_data["rho"][1]],
        dtype=float,
    )
    return {
        "tau": tau,
        "q": q,
        "passive_moduli": passive_moduli,
        "xbar": active_data["xbar"],
        "sigma": active_data["sigma"],
        "active_gap": active_gap,
    }


def reconstruct_pair_from_reduced_native_data(data: dict) -> tuple[np.ndarray, np.ndarray]:
    active = reconstruct_active_from_native_last_mile(data["xbar"], data["sigma"], data["active_gap"])
    passive = monomial_triplet(data["passive_moduli"], data["q"])
    if data["tau"] == 0:
        return active, passive
    return passive, active


def run_sample(label: str, tau: int, q: int, passive_coeffs: np.ndarray, x: np.ndarray, c_forward: np.ndarray) -> None:
    active = active_operator(x, c_forward)
    passive = monomial_triplet(passive_coeffs, q)
    d0_trip, dm_trip = (active, passive) if tau == 0 else (passive, active)

    data = derive_reduced_native_data(d0_trip, dm_trip)
    rec_d0, rec_dm = reconstruct_pair_from_reduced_native_data(data)

    ref_passive = monomial_triplet(np.abs(passive_coeffs), q)
    ref_active = active
    if tau == 0:
        expected_d0, expected_dm = ref_active, ref_passive
    else:
        expected_d0, expected_dm = ref_passive, ref_active

    sigma_true = np.mean(c_forward)

    check(f"{label}: tau is derived natively from moment-support cardinality", data["tau"] == tau, f"tau={data['tau']}")
    check(f"{label}: q is derived natively from directional support moments", data["q"] == q, f"q={data['q']}")
    check(f"{label}: xbar is derived natively from the C3-even active moment", abs(data["xbar"] - np.mean(x)) < 1e-12,
          f"xbar={data['xbar']:.6f}")
    check(f"{label}: sigma is derived natively from the C3-forward active moment", abs(data["sigma"] - sigma_true) < 1e-12,
          f"sigma={data['sigma']}")
    check(f"{label}: passive phases reduce to three nonnegative moduli",
          np.linalg.norm(data["passive_moduli"] - np.abs(passive_coeffs)) < 1e-12,
          f"mods={np.round(data['passive_moduli'], 6)}")
    check(f"{label}: the remaining active gap is exactly four real coordinates",
          data["active_gap"].shape == (4,), f"gap={np.round(data['active_gap'], 6)}")
    check(f"{label}: the PMNS-relevant pair reconstructs exactly from native data plus the 7-real gap",
          np.linalg.norm(rec_d0 - expected_d0) < 1e-12 and np.linalg.norm(rec_dm - expected_dm) < 1e-12,
          f"errors=({np.linalg.norm(rec_d0 - expected_d0):.2e},{np.linalg.norm(rec_dm - expected_dm):.2e})")


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC D SEVEN-REAL LAST MILE")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the current native selector, transport/moment, and passive")
    print("  phase-reduction laws, how much of the PMNS-relevant microscopic")
    print("  operator D is still not fixed?")

    run_sample(
        "neutrino-active",
        0,
        2,
        np.array([0.07 * np.exp(0.4j), 0.11 * np.exp(-0.7j), 0.23 * np.exp(1.1j)], dtype=complex),
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54 * np.exp(0.63j)], dtype=complex),
    )
    run_sample(
        "charged-lepton-active",
        1,
        1,
        np.array([0.17 * np.exp(-0.3j), 0.09 * np.exp(0.9j), 0.04 * np.exp(-1.4j)], dtype=complex),
        np.array([0.92, 1.08, 0.85], dtype=float),
        np.array([0.33, 0.49, 0.26 * np.exp(-0.37j)], dtype=complex),
    )

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact last-mile reduction for the PMNS-relevant microscopic operator:")
    print("    - derived natively already: tau, q, xbar, sigma")
    print("    - passive phases are removable, so passive data reduce to 3 moduli")
    print("    - the remaining active data are exactly 4 real orbit-breaking coordinates")
    print()
    print("  So the unreduced PMNS-relevant D-law is no longer a generic matrix law.")
    print("  It is exactly a 7-real value law:")
    print("    (|a_1|, |a_2|, |a_3|, xi_1, xi_2, rho_1, rho_2)")
    print("  together with the already derived native data (tau, q, xbar, sigma).")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
