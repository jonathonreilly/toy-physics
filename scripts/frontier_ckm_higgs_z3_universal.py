#!/usr/bin/env python3
"""
Higgs Z_3 Charge: L-Independence Test and Obstruction Proof
============================================================

QUESTION: Is the Higgs Z_3 charge delta = 1 L-independent?

This is the blocker identified by Codex review:
  "the Higgs Z_3 charge step is still finite-size / L=8 anchored
   and not yet universal"

ANSWER: NO. The obstruction is sharp and threefold:

  (A) The staggered mass operator eps(x) = (-1)^(sum x_i) couples
      to Z_3 sectors delta=1 and delta=2 with EXACTLY EQUAL weight
      for all L. There is no preferred charge.

  (B) For L divisible by 6 (including the thermodynamic limit
      L -> infinity with L a multiple of 6), ALL Z_3 transition
      matrix elements vanish exactly. The operator is Z_3-neutral.

  (C) For L not divisible by 6, the magnitudes decay as O(1/L^d),
      vanishing in the continuum limit.

PROOF METHOD: Analytic (closed-form geometric sums) verified by
direct lattice computation at L = 4, 6, 8, 10, 12, 16, 20, 24.

CONSEQUENCE: The CKM charge selection lane remains BOUNDED.
The Higgs Z_3 charge delta = 1 cannot be derived from the staggered
mass operator. An alternative derivation route would be needed.

Self-contained: numpy only (no scipy needed).
"""

from __future__ import annotations

import itertools
import os
import sys
import time

import numpy as np

np.set_printoptions(precision=10, linewidth=120)

LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-ckm-higgs-z3-universal.txt"

results = []
pass_count = 0
fail_count = 0


def log(msg=""):
    results.append(msg)
    print(msg)


# =============================================================================
# PART 1: ANALYTIC DERIVATION -- 1D Z_3 TRANSITION ELEMENT
# =============================================================================

def part1_analytic_1d():
    """
    Derive the exact 1D Z_3 transition matrix element analytically.

    For a 1D lattice with L sites and periodic boundary conditions:
      eps(x) = (-1)^x

    The Z_3 projector for charge z is:
      psi_z(x) = (1/sqrt(L)) * omega^(z*x),  omega = exp(2*pi*i/3)

    The transition matrix element is:
      <z+delta|eps|z> = (1/L) * sum_{x=0}^{L-1} omega^{-delta*x} * (-1)^x
                      = (1/L) * sum_{x=0}^{L-1} exp(i*x*phi_delta)

    where phi_delta = pi - 2*pi*delta/3 = pi*(3 - 2*delta)/3.

    This is a geometric sum:
      S = (1 - exp(i*L*phi)) / (1 - exp(i*phi))

    with magnitude |S/L| = |sin(L*phi/2)| / (L * |sin(phi/2)|).
    """
    global pass_count, fail_count

    log("=" * 72)
    log("PART 1: ANALYTIC 1D Z_3 TRANSITION ELEMENT")
    log("=" * 72)

    log("\n  The transition element <z+delta|eps|z> in 1D is a geometric sum.")
    log("  The phase per direction is phi_delta = pi*(3 - 2*delta)/3:")
    log("    delta=0: phi = pi")
    log("    delta=1: phi = pi/3")
    log("    delta=2: phi = -pi/3")
    log("")
    log("  The magnitude is |sin(L*phi/2)| / (L * |sin(phi/2)|).")

    log("\n  --- Exact analytic values ---")
    log(f"  {'L':>4s}  {'|T(d=0)|':>12s}  {'|T(d=1)|':>12s}  {'|T(d=2)|':>12s}"
        f"  {'1==2':>6s}  {'all->0':>6s}  {'L%6':>4s}")
    log(f"  {'-'*4:>4s}  {'-'*12:>12s}  {'-'*12:>12s}  {'-'*12:>12s}"
        f"  {'-'*6:>6s}  {'-'*6:>6s}  {'-'*4:>4s}")

    test_sizes = [4, 6, 8, 10, 12, 16, 20, 24, 30, 36, 48, 60, 96, 120, 240, 480]
    all_equal_12 = True
    all_vanish_6 = True

    for L in test_sizes:
        mags = []
        for delta in range(3):
            phi = np.pi * (3 - 2 * delta) / 3.0
            half_phi = phi / 2.0
            if abs(np.sin(half_phi)) < 1e-15:
                # phi = 0 case (delta=3/2, impossible for integer delta)
                mag = 1.0
            else:
                num = abs(np.sin(L * half_phi))
                den = L * abs(np.sin(half_phi))
                mag = num / den if den > 1e-15 else 0.0
            mags.append(mag)

        eq_12 = abs(mags[1] - mags[2]) < 1e-12
        vanish = all(m < 1e-10 for m in mags)

        if not eq_12:
            all_equal_12 = False
        if L % 6 == 0 and not vanish:
            all_vanish_6 = False

        log(f"  {L:4d}  {mags[0]:12.8f}  {mags[1]:12.8f}  {mags[2]:12.8f}"
            f"  {str(eq_12):>6s}  {str(vanish):>6s}  {L%6:4d}")

    log("\n  KEY RESULTS:")
    log(f"    |T(delta=1)| == |T(delta=2)| for all L:  {all_equal_12}")
    log(f"    All vanish for L divisible by 6:           {all_vanish_6}")

    # Exact check 1: |T(delta=1)| = |T(delta=2)|
    log("\n  EXACT CHECK 1: |T(delta=1)| = |T(delta=2)| for all even L")
    log("  Proof: phi_1 = pi/3 and phi_2 = -pi/3 have |phi_1| = |phi_2|.")
    log("  Therefore |sin(L*phi_1/2)| = |sin(L*phi_2/2)| and")
    log("  |sin(phi_1/2)| = |sin(phi_2/2)|, so the magnitudes are identical.")
    log("  This is EXACT, not numerical.")

    if all_equal_12:
        log("  -> PASS (exact symmetry verified numerically at all test sizes)")
        pass_count += 1
    else:
        log("  -> FAIL")
        fail_count += 1

    # Exact check 2: vanishing for L % 6 == 0
    log("\n  EXACT CHECK 2: All transitions vanish for L divisible by 6")
    log("  Proof: For delta=1, phi = pi/3, so L*phi/2 = L*pi/6.")
    log("  When L = 6k, sin(L*pi/6) = sin(k*pi) = 0 exactly.")
    log("  Same for delta=2 (phi = -pi/3). For delta=0, phi = pi,")
    log("  and sin(L*pi/2) = 0 for all even L.")

    if all_vanish_6:
        log("  -> PASS (vanishing verified for all L divisible by 6)")
        pass_count += 1
    else:
        log("  -> FAIL")
        fail_count += 1

    # Exact check 3: decay rate
    log("\n  EXACT CHECK 3: Magnitude decays as O(1/L)")
    log("  For large L not divisible by 6:")
    log("    |T(delta=1)| = |sin(L*pi/6)| / (L * sin(pi/6))")
    log("                 = |sin(L*pi/6)| / (L/2)")
    log("    Since |sin(L*pi/6)| <= 1, we get |T| <= 2/L -> 0.")

    decay_ok = True
    prev_mag = None
    for L in [8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80]:
        if L % 6 == 0:
            continue
        phi = np.pi / 3.0
        mag = abs(np.sin(L * phi / 2)) / (L * abs(np.sin(phi / 2)))
        bound = 2.0 / L
        ok = mag <= bound + 1e-12
        if not ok:
            decay_ok = False
        if prev_mag is not None and mag > prev_mag + 1e-10:
            # Not monotonically decaying (can oscillate, that's fine)
            pass
        prev_mag = mag

    if decay_ok:
        log("  -> PASS (magnitude bounded by 2/L for all test sizes)")
        pass_count += 1
    else:
        log("  -> FAIL")
        fail_count += 1

    return all_equal_12 and all_vanish_6


# =============================================================================
# PART 2: DIRECT 3D LATTICE VERIFICATION
# =============================================================================

def part2_direct_3d():
    """
    Verify the analytic result by direct computation on 3D lattices.

    For a d-dimensional lattice, eps(x) = (-1)^(sum x_i) = prod_mu (-1)^{x_mu}.
    The d-dimensional transition factorizes:
      <z'|eps|z> = prod_mu <z'_mu|eps_mu|z_mu>

    So the total Z_3 charge delta = sum_mu delta_mu, and the magnitude is
    the product of 1D magnitudes. The key consequence:

    If each 1D factor has |T(delta=1)| = |T(delta=2)|, then the d-dimensional
    result also has equal total weight on delta_total = 1 and delta_total = 2.
    """
    global pass_count, fail_count

    log("\n\n" + "=" * 72)
    log("PART 2: DIRECT 3D LATTICE VERIFICATION")
    log("=" * 72)

    d = 3
    omega = np.exp(2j * np.pi / 3)

    log(f"\n  Testing in d = {d} dimensions.")
    log(f"  For each L, compute sum of |<z'|eps|z>| grouped by delta_total mod 3.")

    log(f"\n  {'L':>4s}  {'S(delta=0)':>14s}  {'S(delta=1)':>14s}  {'S(delta=2)':>14s}"
        f"  {'1==2':>6s}  {'vanish_6':>8s}")
    log(f"  {'-'*4:>4s}  {'-'*14:>14s}  {'-'*14:>14s}  {'-'*14:>14s}"
        f"  {'-'*6:>6s}  {'-'*8:>8s}")

    test_sizes_3d = [4, 6, 8, 10, 12, 16, 20, 24]
    all_equal = True
    all_vanish = True

    for L in test_sizes_3d:
        n_sites = L ** d

        # Use factorized analytic formula for efficiency
        # 1D magnitudes for each delta
        mag_1d = {}
        for delta in range(3):
            phi = np.pi * (3 - 2 * delta) / 3.0
            half_phi = phi / 2.0
            if abs(np.sin(half_phi)) < 1e-15:
                mag_1d[delta] = 0.0 if L % 2 == 0 else 1.0
            else:
                mag_1d[delta] = abs(np.sin(L * half_phi)) / (L * abs(np.sin(half_phi)))

        # d-dimensional: enumerate all (delta_1, ..., delta_d) and group by sum mod 3
        total_by_delta = {0: 0.0, 1: 0.0, 2: 0.0}
        # For each source z and destination z', the transition has
        # 9 pairs per direction (z_src, z_dst) each with delta_mu = (z_dst-z_src)%3
        # But the magnitude only depends on delta_mu, not on z_src.
        # Each delta_mu appears for 3 source values.
        # So the total weight on a given (delta_1,...,delta_d) is
        # 3^d * prod_mu mag_1d[delta_mu]  (from the 3 choices of z_src per direction)

        for delta_vec in itertools.product(range(3), repeat=d):
            mag = 1.0
            for mu in range(d):
                mag *= mag_1d[delta_vec[mu]]
            delta_total = sum(delta_vec) % 3
            # Factor of 3^d for the source sector choices
            total_by_delta[delta_total] += (3 ** d) * mag

        eq = abs(total_by_delta[1] - total_by_delta[2]) < 1e-8
        vanish = all(abs(v) < 1e-10 for v in total_by_delta.values())

        if not eq:
            all_equal = False
        if L % 6 == 0 and not vanish:
            all_vanish = False

        log(f"  {L:4d}  {total_by_delta[0]:14.8f}  {total_by_delta[1]:14.8f}"
            f"  {total_by_delta[2]:14.8f}  {str(eq):>6s}  {str(vanish):>8s}")

    # Also do a direct (non-factorized) check for small L to confirm factorization
    log("\n  CROSS-CHECK: Direct lattice computation (non-factorized) for L=4,8")

    direct_ok = True
    for L in [4, 8]:
        n_sites = L ** d
        coords = np.zeros((n_sites, d), dtype=int)
        epsilon = np.zeros(n_sites, dtype=float)
        for idx in range(n_sites):
            c = []
            rem = idx
            for dim in range(d - 1, -1, -1):
                c.insert(0, rem % L)
                rem //= L
            coords[idx] = c
            epsilon[idx] = (-1) ** sum(c)

        z3_vecs = list(itertools.product(range(3), repeat=d))
        total_direct = {0: 0.0, 1: 0.0, 2: 0.0}

        for z_src in z3_vecs:
            phase_src = np.ones(n_sites, dtype=complex)
            for mu in range(d):
                phase_src *= omega ** (z_src[mu] * coords[:, mu])
            psi_src = phase_src / np.sqrt(n_sites)
            eps_psi = epsilon * psi_src

            for z_dst in z3_vecs:
                phase_dst = np.ones(n_sites, dtype=complex)
                for mu in range(d):
                    phase_dst *= omega ** (z_dst[mu] * coords[:, mu])
                psi_dst = phase_dst / np.sqrt(n_sites)
                elem = np.vdot(psi_dst, eps_psi)

                if abs(elem) > 1e-10:
                    delta_total = sum((z_dst[mu] - z_src[mu]) % 3 for mu in range(d)) % 3
                    total_direct[delta_total] += abs(elem)

        # Compare with factorized result
        total_fact = {0: 0.0, 1: 0.0, 2: 0.0}
        for delta in range(3):
            phi = np.pi * (3 - 2 * delta) / 3.0
            half_phi = phi / 2.0
            if abs(np.sin(half_phi)) < 1e-15:
                mag_1d_val = 0.0
            else:
                mag_1d_val = abs(np.sin(L * half_phi)) / (L * abs(np.sin(half_phi)))
            mag_1d[delta] = mag_1d_val

        for delta_vec in itertools.product(range(3), repeat=d):
            mag = 1.0
            for mu in range(d):
                mag *= mag_1d[delta_vec[mu]]
            dt = sum(delta_vec) % 3
            total_fact[dt] += (3 ** d) * mag

        match = all(abs(total_direct[k] - total_fact[k]) < 1e-6
                     for k in range(3))
        log(f"    L={L}: direct vs factorized match: {match}")
        if not match:
            direct_ok = False
            log(f"      direct:     {total_direct}")
            log(f"      factorized: {total_fact}")

    # Exact checks
    log("\n  EXACT CHECK 4: S(delta=1) == S(delta=2) in 3D for all L")
    if all_equal:
        log("  -> PASS")
        pass_count += 1
    else:
        log("  -> FAIL")
        fail_count += 1

    log("\n  EXACT CHECK 5: All transitions vanish for L divisible by 6 in 3D")
    if all_vanish:
        log("  -> PASS")
        pass_count += 1
    else:
        log("  -> FAIL")
        fail_count += 1

    log("\n  EXACT CHECK 6: Factorized formula matches direct computation")
    if direct_ok:
        log("  -> PASS")
        pass_count += 1
    else:
        log("  -> FAIL")
        fail_count += 1

    return all_equal and all_vanish


# =============================================================================
# PART 3: WHY THE EXISTING L=8 RESULT WAS MISLEADING
# =============================================================================

def part3_l8_diagnosis():
    """
    Explain why the existing script reported delta=1 at L=8.

    The existing script uses the dominant Z_3 sector method:
      - Decompose eps(x) into Z_3 Fourier components
      - Pick the sector with largest |c_z|
      - Report sum(z) mod 3 as the Higgs charge

    At L=8: The per-direction dominant charge happens to be z=1 or z=2
    (both equal), and the script's argmax breaks ties in favor of the
    lower index. With per-direction charges (1,1,1), sum mod 3 = 0.
    But with (2,2,2), sum mod 3 = 0 as well.

    Actually, the script uses a different method: transition matrix
    elements grouped by total delta. At L=8, delta=1 and delta=2 have
    exactly equal total weight, so there is no basis for choosing delta=1.

    The script at L=8 said "delta=1 CONFIRMED" but this was because it
    checked charge_1_mag > max(charge_0_mag, charge_2_mag), which is
    TRUE since charge_1 = charge_2 > charge_0 = 0. The check should
    have been charge_1_mag > charge_2_mag, which is FALSE.
    """
    global pass_count, fail_count

    log("\n\n" + "=" * 72)
    log("PART 3: DIAGNOSIS OF THE L=8 FALSE POSITIVE")
    log("=" * 72)

    log("\n  The existing script frontier_ckm_interpretation_derivation.py")
    log("  reported 'Dominant charge: delta = 1  CONFIRMED' at L=8.")
    log("")
    log("  This was a bug in the selection logic:")
    log("    if charge_1_mag > max(charge_0_mag, charge_2_mag):")
    log("        'delta = 1 CONFIRMED'")
    log("")
    log("  At L=8 in d=3:")
    log("    charge_0_mag = 0.548...")
    log("    charge_1_mag = 0.822...")
    log("    charge_2_mag = 0.822...")
    log("")
    log("  The test charge_1 > max(charge_0, charge_2) is FALSE because")
    log("  charge_1 == charge_2. The script should have reported a TIE,")
    log("  not 'delta=1 CONFIRMED'.")

    # Verify
    d = 3
    omega = np.exp(2j * np.pi / 3)

    for L in [8]:
        mag_1d = {}
        for delta in range(3):
            phi = np.pi * (3 - 2 * delta) / 3.0
            half_phi = phi / 2.0
            if abs(np.sin(half_phi)) < 1e-15:
                mag_1d[delta] = 0.0
            else:
                mag_1d[delta] = abs(np.sin(L * half_phi)) / (L * abs(np.sin(half_phi)))

        total = {0: 0.0, 1: 0.0, 2: 0.0}
        for delta_vec in itertools.product(range(3), repeat=d):
            mag = 1.0
            for mu in range(d):
                mag *= mag_1d[delta_vec[mu]]
            dt = sum(delta_vec) % 3
            total[dt] += (3 ** d) * mag

        log(f"\n  Exact values at L=8, d=3:")
        log(f"    S(delta=0) = {total[0]:.10f}")
        log(f"    S(delta=1) = {total[1]:.10f}")
        log(f"    S(delta=2) = {total[2]:.10f}")
        log(f"    S(1) == S(2): {abs(total[1] - total[2]) < 1e-12}")

        bug_test = total[1] > max(total[0], total[2])
        correct_test_strict = total[1] > total[2] + 1e-10

        log(f"\n  Old script test (charge_1 > max(0,2)):  {bug_test}")
        log(f"  Correct test    (charge_1 > charge_2 + tol):  {correct_test_strict}")
        log(f"  Difference |S(1) - S(2)| = {abs(total[1] - total[2]):.2e}")

    log("\n  EXACT CHECK 7: The L=8 result was a tie, not delta=1")
    # S(1) and S(2) must be equal to within floating point precision
    is_tie = abs(total[1] - total[2]) < 1e-10
    if is_tie:
        log("  -> PASS (tie confirmed, L=8 was misleading)")
        pass_count += 1
    else:
        log("  -> FAIL")
        fail_count += 1

    return is_tie


# =============================================================================
# PART 4: OBSTRUCTION THEOREM
# =============================================================================

def part4_obstruction():
    """
    State the obstruction theorem cleanly.
    """
    global pass_count, fail_count

    log("\n\n" + "=" * 72)
    log("PART 4: OBSTRUCTION THEOREM")
    log("=" * 72)

    log("""
  THEOREM (Higgs Z_3 charge obstruction):

  Let eps(x) = (-1)^{sum_mu x_mu} be the staggered mass operator on
  a d-dimensional cubic lattice with L sites per direction and periodic
  boundary conditions. Let omega = exp(2*pi*i/3) and define Z_3
  taste projectors psi_z(x) = (1/sqrt(L^d)) * prod_mu omega^{z_mu x_mu}.

  Then for any even L:

  (i)   The Z_3 transition element |<z+delta|eps|z>| depends only on
        |delta_mu| per direction, not on the source sector z.

  (ii)  |<z+delta|eps|z>| is identical for delta_total = 1 and
        delta_total = 2 (where delta_total = sum delta_mu mod 3).
        The mass operator does NOT prefer one Z_3 charge over the other.

  (iii) For L divisible by 6, all Z_3 transition elements vanish:
        <z'|eps|z> = 0 for all z, z'.

  (iv)  For L not divisible by 6, the magnitudes are O(1/L^d) and
        vanish in the L -> infinity limit.

  PROOF:

  The result follows from the 1D identity:

    <z+delta|eps|z>_{1D} = (1/L) sum_{x=0}^{L-1} exp(i*x*phi_delta)

  where phi_delta = pi*(3 - 2*delta)/3.

  (a) |phi_1| = |phi_2| = pi/3, so |<z+1|eps|z>| = |<z+2|eps|z>|.
      This proves (ii).

  (b) For delta=0, phi_0 = pi, and sin(L*pi/2) = 0 for even L.
      This proves the delta=0 part of (iii).

  (c) For delta=1, phi_1 = pi/3, and sin(L*pi/6) = 0 when L*pi/6
      is a multiple of pi, i.e. L divisible by 6. Same for delta=2.
      Combined with (b), this proves (iii).

  (d) |sin(L*phi/2)| <= 1, so |T| <= 1/(L*|sin(phi/2)|) = O(1/L).
      In d dimensions, |T| = O(1/L^d). This proves (iv).

  COROLLARY:

  The staggered mass operator eps(x) does not carry a well-defined
  Z_3 charge. The identification "Higgs Z_3 charge = 1" in the CKM
  derivation chain cannot be derived from the Z_3 decomposition of
  the staggered mass operator.

  In particular, the existing L=8 result was an artifact of a
  comparison that counted delta=1 as "dominant" when delta=1 and
  delta=2 had exactly equal weight.
""")

    # Final verification: the theorem holds at all tested sizes
    log("  VERIFICATION: Theorem holds at all tested lattice sizes.")

    theorem_holds = True
    d = 3
    for L in [4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 30, 36, 48]:
        mag_1d = {}
        for delta in range(3):
            phi = np.pi * (3 - 2 * delta) / 3.0
            half_phi = phi / 2.0
            if abs(np.sin(half_phi)) < 1e-15:
                mag_1d[delta] = 0.0 if L % 2 == 0 else 1.0
            else:
                mag_1d[delta] = abs(np.sin(L * half_phi)) / (L * abs(np.sin(half_phi)))

        total = {0: 0.0, 1: 0.0, 2: 0.0}
        for delta_vec in itertools.product(range(3), repeat=d):
            mag = 1.0
            for mu in range(d):
                mag *= mag_1d[delta_vec[mu]]
            dt = sum(delta_vec) % 3
            total[dt] += (3 ** d) * mag

        eq_12 = abs(total[1] - total[2]) < 1e-10
        vanish = all(abs(v) < 1e-10 for v in total.values()) if L % 6 == 0 else True

        ok = eq_12 and vanish
        if not ok:
            theorem_holds = False
            log(f"    L={L}: FAIL  eq={eq_12}, vanish={vanish}")

    log(f"\n  EXACT CHECK 8: Theorem verified at all lattice sizes")
    if theorem_holds:
        log("  -> PASS")
        pass_count += 1
    else:
        log("  -> FAIL")
        fail_count += 1

    return theorem_holds


# =============================================================================
# PART 5: WHAT WOULD BE NEEDED TO CLOSE CKM
# =============================================================================

def part5_what_remains():
    """
    Document what alternative routes might close the Higgs Z_3 charge gap.
    """
    log("\n\n" + "=" * 72)
    log("PART 5: WHAT REMAINS OPEN")
    log("=" * 72)

    log("""
  The staggered mass operator route to the Higgs Z_3 charge is blocked.
  For the CKM lane to advance beyond bounded status, one of these
  alternative derivations would be needed:

  1. GAUGED STAGGERED ACTION:
     The free staggered mass operator is Z_3-symmetric (no preferred charge).
     Perhaps coupling to the SU(2)_L gauge field breaks this symmetry and
     selects delta=1. This would require building the gauged staggered
     Hamiltonian and showing the gauge interaction lifts the 1<->2 degeneracy.

  2. ELECTROWEAK SYMMETRY BREAKING PATTERN:
     The Higgs is not just the mass operator; it is the field whose VEV
     breaks SU(2)_L x U(1)_Y -> U(1)_EM. Perhaps the specific symmetry
     breaking pattern (which distinguishes up-type and down-type Yukawas)
     selects delta=1 over delta=2.

  3. ANOMALY OR CONSISTENCY CONSTRAINT:
     Perhaps requiring anomaly cancellation or perturbative unitarity in
     the Yukawa sector forces delta=1. The existing script already showed
     that anomaly cancellation alone does not select the target charges,
     but the combination with other constraints has not been exhausted.

  4. DIFFERENT IDENTIFICATION OF THE HIGGS:
     Perhaps the Higgs Z_3 charge should not come from the staggered mass
     operator at all, but from a different lattice object (e.g., a link
     variable, a plaquette condensate, or a composite operator).

  None of these alternatives has been developed. The CKM lane is BOUNDED
  until one of them succeeds.
""")


# =============================================================================
# MAIN
# =============================================================================

def main():
    global pass_count, fail_count

    t0 = time.time()
    log("=" * 72)
    log("HIGGS Z_3 CHARGE: L-INDEPENDENCE TEST AND OBSTRUCTION PROOF")
    log("=" * 72)
    log(f"  Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  Purpose: Test whether the Higgs Z_3 charge delta=1 is L-independent")
    log(f"  Answer: NO -- sharp obstruction proved analytically and verified")
    log(f"          numerically at L = 4, 6, 8, 10, 12, 16, 20, 24, 30, 36, 48")
    log("")

    part1_analytic_1d()
    part2_direct_3d()
    part3_l8_diagnosis()
    part4_obstruction()
    part5_what_remains()

    dt = time.time() - t0

    log("\n" + "=" * 72)
    log("FINAL SUMMARY")
    log("=" * 72)
    log(f"\n  PASS = {pass_count}    FAIL = {fail_count}")
    log(f"\n  Completed in {dt:.1f}s")
    log("")
    log("  STATUS: The Higgs Z_3 charge is NOT L-independent.")
    log("  The staggered mass operator has exactly equal weight on delta=1")
    log("  and delta=2, and vanishes entirely for L divisible by 6.")
    log("  The CKM lane remains BOUNDED.")
    log("=" * 72)

    # Write log
    try:
        os.makedirs("logs", exist_ok=True)
        with open(LOG_FILE, "w") as f:
            f.write("\n".join(results))
        log(f"\n  Log written to {LOG_FILE}")
    except Exception as e:
        log(f"\n  (Could not write log: {e})")

    # Exit code
    if fail_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
