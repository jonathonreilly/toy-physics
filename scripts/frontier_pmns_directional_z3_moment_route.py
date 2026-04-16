#!/usr/bin/env python3
r"""
Directional Z_3^3 moment route for the PMNS microscopic lepton lane.

Question:
  Can the native generation-orbit moment algebra fix the unresolved
  microscopic data on the lepton lane, starting from the Cl(3) on Z^3
  carrier and using only Z_3-structural moments as the selection device?

Answer:
  The directional moment route does fix a useful subset exactly:

    - the passive monomial offset q
    - the active/passive sector orientation bit tau

  But the same moment algebra is blind to the five-real active corner source
  beyond the already closed weak-axis seed averages.

  So this route is axiom-native and exact on the passive/orientation side, but
  it is not sufficient for full top-to-bottom microscopic closure.

Implementation note:
  This uses the same Z_3 orbit template as the CKM-directional-charge lane,
  but only as a structural guide. No quark fit data are imported.
"""

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


def monomial_triplet(coeffs: np.ndarray, offset: int) -> np.ndarray:
    return diagonal(coeffs) @ PERMUTATIONS[offset]


def active_triplet(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(np.asarray(x, dtype=complex)) + diagonal(y_eff) @ CYCLE


def support_trace_moments(D: np.ndarray) -> np.ndarray:
    r"""
    Directional Z_3 moment vector:

        m_r(D) = tr(D P_r^\dagger),   r = 0,1,2.

    For a monomial lane diag(a) P_q, exactly one component is nonzero.
    For the active I + C lane, two components are nonzero and the remaining
    component vanishes.
    """
    return np.array(
        [
            np.trace(D @ PERMUTATIONS[0].conj().T),
            np.trace(D @ PERMUTATIONS[1].conj().T),
            np.trace(D @ PERMUTATIONS[2].conj().T),
        ],
        dtype=complex,
    )


def recover_passive_offset(D: np.ndarray) -> tuple[int, complex]:
    m = support_trace_moments(D)
    idx = int(np.argmax(np.abs(m)))
    return idx, m[idx]


def moment_support_count(D: np.ndarray, tol: float = 1e-10) -> int:
    return int(np.count_nonzero(np.abs(support_trace_moments(D)) > tol))


def decompose_active_seed_source(x: np.ndarray, y: np.ndarray, delta: float) -> dict:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xbar = float(np.mean(x))
    ybar = float(np.mean(y))
    xi = x - xbar * np.ones(3, dtype=float)
    eta = y - ybar * np.ones(3, dtype=float)
    y_eff = y.copy().astype(complex)
    y_eff[2] *= np.exp(1j * delta)
    return {
        "xbar": xbar,
        "ybar": ybar,
        "xi": xi,
        "eta": eta,
        "delta": float(delta),
        "moment_vector": support_trace_moments(active_triplet(x, y, delta)),
        "y_eff_sum": complex(np.sum(y_eff)),
    }


def build_full_pair(tau: int, q: int, passive_coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float) -> tuple[np.ndarray, np.ndarray]:
    active = active_triplet(x, y, delta)
    passive = monomial_triplet(passive_coeffs, q)
    if tau == 0:
        return active, passive
    if tau == 1:
        return passive, active
    raise ValueError("tau must be 0 or 1")


def part1_passive_offset_is_recovered_exactly_by_directional_moments() -> None:
    print("\n" + "=" * 88)
    print("PART 1: PASSIVE MONOMIAL OFFSET q IS RECOVERED EXACTLY")
    print("=" * 88)

    coeffs = np.array([0.07, 0.11, 0.23], dtype=complex)
    coeff_sum = np.sum(coeffs)

    for q in (0, 1, 2):
        D = monomial_triplet(coeffs, q)
        m = support_trace_moments(D)
        recovered_q, recovered_amp = recover_passive_offset(D)
        support = np.flatnonzero(np.abs(m) > 1e-10).tolist()
        check(f"q={q}: exactly one directional moment survives", len(support) == 1, f"support={support}")
        check(f"q={q}: recovered offset equals the true passive offset", recovered_q == q, f"recovered={recovered_q}")
        check(f"q={q}: the surviving moment equals the passive coefficient sum", abs(recovered_amp - coeff_sum) < 1e-12,
              f"amp={recovered_amp}, sum={coeff_sum}")

    print()
    print("  So the passive monomial lane is fixed exactly by the Z_3 support-trace")
    print("  moments, and the offset q is a native discrete output.")


def part2_sector_orientation_is_the_support_cardinality_of_the_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SECTOR ORIENTATION IS READ OFF FROM MOMENT-SUPPORT CARDINALITY")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    passive_coeffs = np.array([0.07, 0.11, 0.23], dtype=complex)

    pair_nu = build_full_pair(0, 2, passive_coeffs, x, y, delta)
    pair_e = build_full_pair(1, 2, passive_coeffs, x, y, delta)

    counts_nu = [moment_support_count(block) for block in pair_nu]
    counts_e = [moment_support_count(block) for block in pair_e]

    tau_nu = int(np.argmax(counts_nu))  # active block has support count 2
    tau_e = int(np.argmax(counts_e))

    check("Neutrino-oriented branch has the active block in the first slot", tau_nu == 0,
          f"counts={counts_nu}")
    check("Charged-lepton-oriented branch has the active block in the second slot", tau_e == 1,
          f"counts={counts_e}")
    check("The passive block has exactly one surviving directional moment", sorted(counts_nu) == [1, 2],
          f"counts={counts_nu}")
    check("The same moment support pattern flips under sector exchange", counts_nu == counts_e[::-1],
          f"nu={counts_nu}, e={counts_e}")

    print()
    print("  Thus the directional moment route does not need a separate branch")
    print("  selector: the active sector is the one with two surviving moments.")


def part3_directional_moments_do_not_fix_the_five_real_active_corner_source() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SAME MOMENTS DO NOT FIX THE 5-REAL ACTIVE CORNER SOURCE")
    print("=" * 88)

    # Two distinct active operators with the same directional moment vector.
    # They have identical sums xbar and y_eff_sum, but different corner-source
    # coordinates (xi, eta).
    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    delta_a = 0.63

    x_b = np.array([1.05, 0.97, 0.90], dtype=float)  # same sum as x_a
    y_b = np.array([0.60, 0.09, 0.54], dtype=float)  # same y1+y2 and same phase-bearing third entry
    delta_b = 0.63

    A = active_triplet(x_a, y_a, delta_a)
    B = active_triplet(x_b, y_b, delta_b)
    m_a = support_trace_moments(A)
    m_b = support_trace_moments(B)
    dec_a = decompose_active_seed_source(x_a, y_a, delta_a)
    dec_b = decompose_active_seed_source(x_b, y_b, delta_b)

    check("The two active operators have identical directional moment vectors", np.linalg.norm(m_a - m_b) < 1e-12,
          f"m_a={np.round(m_a, 6)}, m_b={np.round(m_b, 6)}")
    check("The two active operators have different zero-sum diagonal breaking coordinates", np.linalg.norm(dec_a["xi"] - dec_b["xi"]) > 1e-6,
          f"xi_a={np.round(dec_a['xi'], 6)}, xi_b={np.round(dec_b['xi'], 6)}")
    check("The two active operators have different cycle-magnitude breaking coordinates", np.linalg.norm(dec_a["eta"] - dec_b["eta"]) > 1e-6,
          f"eta_a={np.round(dec_a['eta'], 6)}, eta_b={np.round(dec_b['eta'], 6)}")
    check("The route only sees the seed averages and the phase-bearing summed moment", abs(dec_a["xbar"] - dec_b["xbar"]) < 1e-12 and abs(dec_a["y_eff_sum"] - dec_b["y_eff_sum"]) < 1e-12,
          f"xbar={dec_a['xbar']:.6f}, y_eff_sum={dec_a['y_eff_sum']}")

    print()
    print("  So the directional Z_3 moment route is exact on the passive offset and")
    print("  sector-orientation bit, but it cannot determine the active 5-real")
    print("  corner source. The kernel contains distinct off-seed source data.")


def main() -> int:
    print("=" * 88)
    print("PMNS DIRECTIONAL Z_3 MOMENT ROUTE")
    print("=" * 88)
    print()
    print("Native inputs:")
    print("  - Cl(3) on Z^3 as the only axiom-level substrate")
    print("  - the retained lepton supports E_nu and E_e")
    print("  - the CKM Z_3 directional-charge template, used only structurally")
    print()
    print("Question:")
    print("  What does the directional Z_3^3 / generation-orbit moment algebra fix")
    print("  on the microscopic lepton lane?")

    part1_passive_offset_is_recovered_exactly_by_directional_moments()
    part2_sector_orientation_is_the_support_cardinality_of_the_pair()
    part3_directional_moments_do_not_fix_the_five_real_active_corner_source()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact native law:")
    print("    - the passive monomial offset q is fixed exactly by the unique")
    print("      surviving directional support moment")
    print("    - the active/passive sector orientation tau is read off from the")
    print("      moment-support cardinality of the lepton pair")
    print()
    print("  Exact elimination:")
    print("    - the same moment algebra cannot determine the active 5-real")
    print("      corner source; distinct source data share the same moments")
    print()
    print("  So this route yields a native passive-offset law and a native")
    print("  orientation law, but it is not enough for complete microscopic")
    print("  closure.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
