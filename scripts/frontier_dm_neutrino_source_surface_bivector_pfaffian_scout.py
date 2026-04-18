#!/usr/bin/env python3
"""
DM Neutrino Source-Surface Bivector / Pfaffian Scout

Goal:
  Drop assumption A2.4 (W[J] = log|det(D+J)| is THE canonical retained scalar
  generator) from the Case 3 Microscopic Polynomial Impossibility Theorem.
  Does the Cl(3) bivector grade (via the Z_3 doublet eigenvector bilinear
  v_2^T H v_2) supply an axiom-native polynomial scalar on H_src that is
  delta-ODD, thereby escaping the delta-evenness trap?

Verdict:
  DEAD (strict). Candidate scalar Im(K_22^3) = 3 sqrt(3) delta (m^2 - 3 delta^2)
  is (a) phase-gauge-dependent, (b) q_+-blind, (c) not CPT-even (so not a
  derivative of W[J] at any order).

  PARTIAL (relaxed). If phase-gauge-fix and CPT-admission are both granted,
  the scalar pins delta up to Z_3 ambiguity but still leaves q_+ open.

Script content:
  Part 1: Compute the six Z_3 bilinears K_ij = v_i^T H_src v_j in closed form
          and verify the symbolic identities.
  Part 2: Verify delta-parity of each bilinear (even/odd).
  Part 3: Verify Z_3-invariance of the cubic Im(K_22^3) under H -> C_3 H C_3^-1.
  Part 4: Demonstrate phase-gauge-dependence: under v_2 -> e^{i phi} v_2, the
          delta-odd combination rotates into the delta-even combination.
  Part 5: Verify that Im(K_22^3) is NOT in the W[J] source-derivative family:
          log|det(m I + H_src)| is exactly delta-even, so no derivative can be
          delta-odd.
  Part 6: Demonstrate q_+-blindness of the candidate scalar.
  Part 7: Print verdict classification.

All checks use the axiom-native affine chart from
frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

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


# ----------------------------------------------------------------------------
# Axiom-native constants and generators
# ----------------------------------------------------------------------------

OMEGA = np.exp(2j * math.pi / 3.0)
I3 = np.eye(3, dtype=complex)

# C_3[111] on H_hw=1 in basis (X_1, X_2, X_3): X_1 -> X_2 -> X_3 -> X_1.
C3 = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=complex)
C3_INV = C3.conj().T

# C_3 eigenvectors (defined up to a phase, which is the key gauge).
V0 = np.array([1.0, 1.0, 1.0], dtype=complex) / math.sqrt(3)
V1 = np.array([1.0, OMEGA, OMEGA ** 2], dtype=complex) / math.sqrt(3)
V2 = np.array([1.0, OMEGA ** 2, OMEGA], dtype=complex) / math.sqrt(3)


def tm() -> np.ndarray:
    return np.array(
        [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex
    )


def tdelta() -> np.ndarray:
    return np.array(
        [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=complex
    )


def tq() -> np.ndarray:
    return np.array(
        [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=complex
    )


def h_src(m: float, delta: float, q_plus: float) -> np.ndarray:
    return m * tm() + delta * tdelta() + q_plus * tq()


def bilinear(va: np.ndarray, vb: np.ndarray, M: np.ndarray) -> complex:
    """Complex BILINEAR (not sesquilinear) contraction v_a^T M v_b."""
    return complex(va @ M @ vb)


# ----------------------------------------------------------------------------
# Part 1: Closed-form evaluation of the six Z_3 bilinears
# ----------------------------------------------------------------------------


def part1_closed_form_bilinears() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CLOSED-FORM Z_3 BILINEARS K_ij = v_i^T H_src v_j")
    print("=" * 88)

    rng = np.random.default_rng(20260418)
    samples = [(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5))
               for _ in range(6)]

    ok_K00 = True
    ok_K11 = True
    ok_K22 = True
    ok_K01 = True
    ok_K02 = True
    ok_K12 = True
    for m, delta, q in samples:
        H = h_src(m, delta, q)
        K00 = bilinear(V0, V0, H)
        K11 = bilinear(V1, V1, H)
        K22 = bilinear(V2, V2, H)
        K01 = bilinear(V0, V1, H)
        K02 = bilinear(V0, V2, H)
        K12 = bilinear(V1, V2, H)
        exp_K00 = m + 2.0 * q
        exp_K11 = m - 1j * math.sqrt(3.0) * delta
        exp_K22 = m + 1j * math.sqrt(3.0) * delta
        exp_K12 = -q
        ok_K00 &= abs(K00 - exp_K00) < 1e-12
        ok_K11 &= abs(K11 - exp_K11) < 1e-12
        ok_K22 &= abs(K22 - exp_K22) < 1e-12
        ok_K01 &= abs(K01) < 1e-12
        ok_K02 &= abs(K02) < 1e-12
        ok_K12 &= abs(K12 - exp_K12) < 1e-12

    check("K_00 = v_0^T H_src v_0 = m + 2 q_+  (singlet-singlet, real, delta-blind)",
          ok_K00)
    check("K_11 = v_1^T H_src v_1 = m - i sqrt(3) delta  (conjugate of K_22)",
          ok_K11)
    check("K_22 = v_2^T H_src v_2 = m + i sqrt(3) delta  (the delta-bearing bilinear)",
          ok_K22)
    check("K_01 = v_0^T H_src v_1 = 0  (singlet-doublet block vanishes)", ok_K01)
    check("K_02 = v_0^T H_src v_2 = 0  (singlet-doublet block vanishes)", ok_K02)
    check("K_12 = v_1^T H_src v_2 = -q_+  (cross-doublet, real, delta-blind)", ok_K12)


# ----------------------------------------------------------------------------
# Part 2: delta-parity of each bilinear and selected cubics
# ----------------------------------------------------------------------------


def part2_delta_parity() -> None:
    print("\n" + "=" * 88)
    print("PART 2: delta-PARITY OF BILINEARS AND CUBICS")
    print("=" * 88)

    test_points = [(0.3, 0.5, 1.0), (-0.2, 0.7, -0.4), (0.5, 1.0, 0.0), (0.0, 0.3, 0.5)]

    ok_K22_odd_imag = True
    ok_K22_even_real = True
    ok_K22_cubed_imag_odd = True
    ok_K22_cubed_real_even = True
    ok_K00_even = True
    ok_K12_even = True
    ok_magn_even = True
    for m, d, q in test_points:
        Hp = h_src(m, d, q)
        Hn = h_src(m, -d, q)
        K22p = bilinear(V2, V2, Hp)
        K22n = bilinear(V2, V2, Hn)
        K00p = bilinear(V0, V0, Hp)
        K00n = bilinear(V0, V0, Hn)
        K12p = bilinear(V1, V2, Hp)
        K12n = bilinear(V1, V2, Hn)
        ok_K22_odd_imag &= abs(K22p.imag + K22n.imag) < 1e-12  # odd
        ok_K22_even_real &= abs(K22p.real - K22n.real) < 1e-12  # even
        Kp3 = K22p ** 3
        Kn3 = K22n ** 3
        ok_K22_cubed_imag_odd &= abs(Kp3.imag + Kn3.imag) < 1e-12
        ok_K22_cubed_real_even &= abs(Kp3.real - Kn3.real) < 1e-12
        ok_K00_even &= abs(K00p - K00n) < 1e-12
        ok_K12_even &= abs(K12p - K12n) < 1e-12
        ok_magn_even &= abs(abs(K22p) - abs(K22n)) < 1e-12

    check("Im K_22 is delta-ODD", ok_K22_odd_imag)
    check("Re K_22 is delta-EVEN", ok_K22_even_real)
    check("Im K_22^3 is delta-ODD", ok_K22_cubed_imag_odd)
    check("Re K_22^3 is delta-EVEN", ok_K22_cubed_real_even)
    check("K_00 is delta-EVEN", ok_K00_even)
    check("K_12 is delta-EVEN", ok_K12_even)
    check("|K_22|^2 = m^2 + 3 delta^2 is delta-EVEN (magnitude invariant)",
          ok_magn_even)

    # closed form check
    ok_closed = True
    for m, d, q in test_points:
        H = h_src(m, d, q)
        val = (bilinear(V2, V2, H) ** 3).imag
        expected = 3.0 * math.sqrt(3.0) * d * (m * m - d * d)
        ok_closed &= abs(val - expected) < 1e-10
    check("Im K_22^3 = 3 sqrt(3) delta (m^2 - delta^2)  (closed form)", ok_closed)


# ----------------------------------------------------------------------------
# Part 3: Z_3-invariance of Im(K_22^3) under H -> C_3 H C_3^-1
# ----------------------------------------------------------------------------


def part3_z3_invariance() -> None:
    print("\n" + "=" * 88)
    print("PART 3: Z_3-INVARIANCE OF K_22^3")
    print("=" * 88)

    test_points = [(0.3, 0.5, 1.0), (-0.2, 0.7, -0.4), (0.5, 0.3, 0.8)]
    ok = True
    ok_cube_same = True
    for m, d, q in test_points:
        H = h_src(m, d, q)
        H_c3 = C3 @ H @ C3_INV
        K = bilinear(V2, V2, H)
        K_c3 = bilinear(V2, V2, H_c3)
        # K -> omega * K under H -> C_3 H C_3^-1
        ok &= abs(K_c3 - OMEGA * K) < 1e-12
        # but K^3 is invariant
        ok_cube_same &= abs(K ** 3 - K_c3 ** 3) < 1e-12

    check("K_22 picks up phase omega under H -> C_3 H C_3^-1", ok)
    check("K_22^3 is exactly Z_3-invariant (since omega^3 = 1)", ok_cube_same)


# ----------------------------------------------------------------------------
# Part 4: Phase-gauge dependence of Im(K_22^3)
# ----------------------------------------------------------------------------


def part4_phase_gauge_dependence() -> None:
    print("\n" + "=" * 88)
    print("PART 4: PHASE-GAUGE DEPENDENCE UNDER v_2 -> e^{i phi} v_2")
    print("=" * 88)

    m, d, q = 0.4, 0.6, 0.7
    H = h_src(m, d, q)
    K_original = bilinear(V2, V2, H)
    Im_K3_original = (K_original ** 3).imag
    Re_K3_original = (K_original ** 3).real

    # Apply phase v_2 -> e^{i phi} v_2
    for phi_deg in [0, 30, 60, 90, 180]:
        phi = math.radians(phi_deg)
        v2_rot = np.exp(1j * phi) * V2
        K_rot = bilinear(v2_rot, v2_rot, H)  # picks up e^{2 i phi}
        Im_K3_rot = (K_rot ** 3).imag
        Re_K3_rot = (K_rot ** 3).real
        # Expected rotation: (Re, Im) rotates by 6 phi
        c = math.cos(6 * phi)
        s = math.sin(6 * phi)
        Re_expected = c * Re_K3_original - s * Im_K3_original
        Im_expected = s * Re_K3_original + c * Im_K3_original
        ok_re = abs(Re_K3_rot - Re_expected) < 1e-10
        ok_im = abs(Im_K3_rot - Im_expected) < 1e-10
        check(
            f"phase phi={phi_deg} deg: (Re, Im) K_22^3 rotates by 6 phi",
            ok_re and ok_im,
            f"Im rotated = {Im_K3_rot:.4f}, expected = {Im_expected:.4f}",
        )

    # At phi = 15 deg (6 phi = 90 deg), the "delta-odd" Im component of K_22^3
    # rotates into the ORIGINAL "delta-even" Re component.  So the rotated
    # "Im K_22^3" is delta-EVEN: f(+d) + f(-d) != 0.
    v2_15 = np.exp(1j * math.radians(15)) * V2
    Hp = h_src(0.4, 0.6, 0.7)
    Hn = h_src(0.4, -0.6, 0.7)
    Kp = bilinear(v2_15, v2_15, Hp)
    Kn = bilinear(v2_15, v2_15, Hn)
    Im_cube_sum = (Kp ** 3).imag + (Kn ** 3).imag
    # At phi = 15, Im K^3 -> sin(90) Re K^3_orig + cos(90) Im K^3_orig = Re K^3_orig.
    # Re K^3_orig = m^3 - 3 m (sqrt3 d)^2 = m^3 - 9 m d^2 which is delta-EVEN.
    # So Im(K+)_rotated + Im(K-)_rotated = 2 * Re K^3_orig, typically NONZERO.
    ok_even = abs(Im_cube_sum) > 1e-6  # NOT delta-odd at phi=15 deg
    check(
        "At phi = 15 deg, rotated-v_2 Im K_22^3 picks up the delta-EVEN Re K_22^3 piece",
        ok_even,
        f"Im(K+)+Im(K-) = {Im_cube_sum:.4f} (nonzero => delta-parity destroyed by generic phase)",
    )


# ----------------------------------------------------------------------------
# Part 5: Im K_22^3 is NOT in the W[J] = log|det(D+J)| source-derivative family
# ----------------------------------------------------------------------------


def part5_not_in_W_J() -> None:
    print("\n" + "=" * 88)
    print("PART 5: W[J] ON SCHUR BASELINE IS EXACTLY delta-EVEN")
    print("=" * 88)

    # W[J = H_src] at baseline D = m_b I
    def W(m_b, m_s, delta, q):
        D = m_b * I3 + h_src(m_s, delta, q)
        return math.log(abs(np.linalg.det(D)))

    ok_all = True
    for m_b in [1.5, 2.0, 3.0]:
        for m_s in [0.0, 0.3, -0.2]:
            for q in [0.5, 1.0]:
                for d in [0.3, 0.7]:
                    wp = W(m_b, m_s, d, q)
                    wn = W(m_b, m_s, -d, q)
                    ok_all &= abs(wp - wn) < 1e-10
    check(
        "W[J] = log|det(m_b I + H_src)| is exactly delta-EVEN for all (m_b, m_s, q)",
        ok_all,
        "every source derivative of W is delta-even -> Im K_22^3 is NOT in the W family",
    )

    # Extra: all cubic source-derivative coefficients of W are delta-even at m_b.
    # They factor through Tr[(m_b I)^{-k} P_a P_b P_c] -- real, delta-parity follows
    # delta-parity of the Tr(H_src^k) expansion.
    ok_tr = True
    for m_s, d, q in [(0.3, 0.5, 1.0), (0.0, 0.7, -0.4), (-0.2, 0.3, 0.8)]:
        H = h_src(m_s, d, q)
        Hn = h_src(m_s, -d, q)
        for k in (1, 2, 3, 4, 5):
            Hk = np.linalg.matrix_power(H, k)
            Hnk = np.linalg.matrix_power(Hn, k)
            tr_p = np.trace(Hk).real
            tr_n = np.trace(Hnk).real
            ok_tr &= abs(tr_p - tr_n) < 1e-10
    check(
        "Tr(H_src^k) is delta-EVEN for k=1..5 (via Theorem 3 of impossibility note)",
        ok_tr,
    )


# ----------------------------------------------------------------------------
# Part 6: q_+-blindness of Im K_22^3
# ----------------------------------------------------------------------------


def part6_q_plus_blindness() -> None:
    print("\n" + "=" * 88)
    print("PART 6: q_+-BLINDNESS OF Im K_22^3")
    print("=" * 88)

    ok = True
    for m, d in [(0.3, 0.5), (-0.2, 0.7), (0.1, 1.0)]:
        vals = []
        for q in [-1.0, -0.3, 0.0, 0.5, 1.2]:
            H = h_src(m, d, q)
            vals.append((bilinear(V2, V2, H) ** 3).imag)
        # all values equal (q-independent)
        ok &= max(vals) - min(vals) < 1e-10
    check(
        "Im K_22^3 is INDEPENDENT of q_+ (so it cannot pin the q_+ coordinate)",
        ok,
        "v_2^T T_q v_2 = 0 -> T_q does not enter K_22",
    )

    # Verify v_2^T T_q v_2 = 0 exactly
    val = bilinear(V2, V2, tq())
    check(
        "v_2^T T_q v_2 = 0 exactly (T_q is Z_3-singlet; v_2 is doublet; bilinear vanishes)",
        abs(val) < 1e-12,
        f"value = {val}",
    )


# ----------------------------------------------------------------------------
# Part 7: Verdict
# ----------------------------------------------------------------------------


def part7_verdict() -> None:
    print("\n" + "=" * 88)
    print("PART 7: VERDICT CLASSIFICATION")
    print("=" * 88)

    print("""
  Candidate bivector-grade delta-ODD scalar on H_src:

      f(H_src) = Im [(v_2^T H_src v_2)^3] = 3 sqrt(3) delta (m^2 - delta^2).

  Defects (cumulative; each is independently fatal under the theorem's framing):

    (1) PHASE-GAUGE-DEPENDENCE.  Under v_2 -> e^{i phi} v_2 (a U(1) freedom that
        the Cl(3)/Z^3 axiom does not fix), (Re, Im) of K_22^3 rotate by 6 phi.
        Generic phi rotates the delta-odd signal into the delta-even signal;
        delta-parity is not a phase-invariant property.  The retained atlas
        supplies NO canonical phase for v_2.

    (2) q_+-BLINDNESS.  v_2^T T_q v_2 = 0 exactly, so Im K_22^3 does not depend
        on q_+.  Even if delta were pinned by this scalar, q_+ would remain
        free.  The joint (delta_*, q_+*) selector is NOT closed by this
        scalar alone.

    (3) NOT-IN-W[J].  The complex bilinear v_2^T H v_2 is NOT CPT-even and NOT
        derivable as a source derivative of W[J] = log|det(D+J)|.  The
        Observable Principle theorem (additivity + CPT-even) forces the unique
        retained scalar generator to take the form c log|Z|.  Even DROPPING
        A2.4 does not rescue Im K_22^3 from the CPT-obstruction, because CPT
        comes from scalarity, not from the |det| choice per se.

  Verdict:  DEAD (strict reading).

  Relaxed verdict:  PARTIAL (with phase-axiom and CPT-admission).  With a
  canonical phase for v_2 (derivable from some as-yet-unretained axiom-native
  principle) AND admission of non-CPT-even scalars, Im K_22^3 would partially
  pin delta (to delta = 0 or delta = +/- m).  q_+ would still be
  unpinned.  Neither relaxation is currently on the retained atlas.

  Implication for Case 3 Microscopic Polynomial Impossibility Theorem:
    the theorem is ROBUST under A2.4 relaxation, because the CPT-obstruction
    (from Grassmann-additivity + scalarity) is INDEPENDENT of A2.4 and
    independently excludes complex-bilinear scalars.
""")


def main() -> None:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE BIVECTOR / PFAFFIAN SCOUT")
    print("Axiom: Cl(3) on Z^3 (single framework axiom)")
    print("=" * 88)

    part1_closed_form_bilinears()
    part2_delta_parity()
    part3_z3_invariance()
    part4_phase_gauge_dependence()
    part5_not_in_W_J()
    part6_q_plus_blindness()
    part7_verdict()

    print("\n" + "=" * 88)
    print(f"TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    print("=" * 88)


if __name__ == "__main__":
    main()
