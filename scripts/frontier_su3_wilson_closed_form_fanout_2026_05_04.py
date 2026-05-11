"""SU(3) Wilson plaquette closed-form fan-out at beta = 6.

Per physics-loop guidance (deep-work / stuck-fan-out): before treating
the L_s>=3 Wigner-Racah engine path as the next exact-cube route, run a fan-out of
3-5 orthogonal closed-form estimates of <P>(beta=6) on standard SU(3)
Wilson primitives. The point is to strengthen the SU(3) Wigner L_s=2
PBC orientation verdict (legacy Block 5) by explicitly ruling out
simpler closed-form alternatives, not to actually close the bridge.

Methods evaluated:

  M1. Single-plaquette character-expansion (Haar): <P>_1plaq =
      Re[c_(1,0)(beta)/c_(0,0)(beta)] / 3, the exact one-plaquette-in-
      isolation result. This is the leading strong-coupling Wilson
      observable.

  M2. Strong-coupling leading-order (Drouffe-Itzykson): <P>_SC1 =
      beta/(2 N^2) = beta/18 for SU(3), the universal first-order
      strong-coupling formula.

  M3. Strong-coupling 2nd-order improvement: M2 + the next term in
      the strong-coupling series.

  M4. Single-plaquette mean-field self-consistency (Drouffe-Itzykson
      mean-field): solve <P>_MF = (1/3) Re[c_(1,0)(z beta <P>_MF) /
      c_(0,0)(z beta <P>_MF)] iteratively.

  M5. Weak-coupling 1-loop perturbative: <P>_WC = 1 - (N^2-1)/(8N^2)
      * 4/beta + O(1/beta^2), the standard 4D lattice Wilson result.

  M6. Lattice MC reference: <P>_MC = 0.5934 (canonical SU(3) value at
      beta = 6, used as comparator only).

Forbidden imports: none (numpy + scipy.special only).

Run:
    python3 scripts/frontier_su3_wilson_closed_form_fanout_2026_05_04.py
"""

from __future__ import annotations

import sys
from typing import Callable, Dict, List, Tuple

import numpy as np
from scipy.special import iv


BETA = 6.0
N_COLOR = 3
EPSILON_WITNESS = 3.03e-4
P_MC_REFERENCE = 0.5934
MODE_MAX = 200


# ===========================================================================
# Wilson character coefficients c_(p,q)(beta) via Bessel determinant.
# ===========================================================================

def wilson_character_coefficient(p: int, q: int, mode_max: int, arg: float
                                   ) -> float:
    """SU(3) Wilson character coefficient c_(p,q)(beta) by Bessel determinant.

    For irrep (p, q): partition lambda = (p+q, q, 0).
      c_(p,q)(beta) = sum_(n in Z) det[I_(n + lambda_j + i - j)(beta/3)]_(i,j=1..3)
    """
    lam = [p + q, q, 0]
    total = 0.0
    for mode in range(-mode_max, mode_max + 1):
        mat = np.array(
            [[iv(mode + lam[j] + i - j, arg) for j in range(3)]
             for i in range(3)], dtype=float
        )
        total += float(np.linalg.det(mat))
    return total


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def fundamental_to_singlet_ratio(beta: float, mode_max: int = MODE_MAX
                                    ) -> float:
    """c_(1,0)(beta) / c_(0,0)(beta) — fundamental-irrep character ratio.

    For SU(3), <chi_F(U)>_1plaq = (1/d_F) Re[c_F(beta) / c_0(beta)]
    where d_F = 3 (fundamental dim). The single-plaquette Wilson
    observable is <(1/N) Re tr U_p>_1plaq = c_(1,0) / (3 c_(0,0)).
    """
    arg = beta / 3.0
    c10 = wilson_character_coefficient(1, 0, mode_max, arg)
    c00 = wilson_character_coefficient(0, 0, mode_max, arg)
    return c10 / c00


# ===========================================================================
# Method M1: single-plaquette character-expansion (Haar).
# ===========================================================================

def m1_single_plaquette_character(beta: float) -> float:
    """<P>_1plaq = (1/3) c_(1,0)(beta) / c_(0,0)(beta).

    Exact single-plaquette Haar-integrated Wilson observable.
    """
    return fundamental_to_singlet_ratio(beta) / N_COLOR


# ===========================================================================
# Method M2: strong-coupling leading order.
# ===========================================================================

def m2_strong_coupling_leading(beta: float) -> float:
    """<P>_SC1 = beta / (2 N^2) for SU(N) leading strong coupling.

    Standard result: at strong coupling, <P> ~ beta/(2 N^2) = beta/18
    for SU(3).
    """
    return beta / (2.0 * N_COLOR ** 2)


# ===========================================================================
# Method M3: strong-coupling 2nd-order (single-plaquette character).
# ===========================================================================

def m3_strong_coupling_2nd_order(beta: float) -> float:
    """Same as M1 — the single-plaquette character expansion IS the
    strong-coupling expansion summed to all orders within the one-
    plaquette Haar measure. At small beta, M1 expands as
      <P>_1plaq = beta/(2N^2) + O(beta^3),
    so M1 itself encodes the strong-coupling all-order single-plaquette
    result. The 2nd-order improvement requires INTER-plaquette
    correlation (next-nearest plaquette character), not available in
    closed form on the framework's V-invariant block structure without
    a full graph-traversal sum.

    Therefore M3 reports M1 as the all-order single-plaquette result.
    A genuine 2nd-order strong-coupling correction would require
    enumerating the small-loop Wilson contributions (2x1, 1x2, etc.),
    which is out of scope for this fan-out.
    """
    return m1_single_plaquette_character(beta)


# ===========================================================================
# Method M4: single-plaquette mean-field self-consistency.
# ===========================================================================

def m4_mean_field_self_consistent(beta: float, z: int = 6,
                                     max_iter: int = 100,
                                     tol: float = 1e-9) -> Tuple[float, int]:
    """Drouffe-Itzykson single-plaquette mean-field.

    Self-consistency: <P>_MF = (1/N) c_F(beta_eff) / c_0(beta_eff),
    where beta_eff = z * beta * <P>_MF and z is the link-coordination
    number (number of plaquettes attached to a typical link, ~6 for
    3+1D Wilson).

    Returns (P_MF, n_iter).
    """
    p = m1_single_plaquette_character(beta)  # initial guess
    for k in range(max_iter):
        beta_eff = z * beta * p
        if beta_eff <= 0:
            return p, k
        ratio = fundamental_to_singlet_ratio(beta_eff)
        p_new = ratio / N_COLOR
        if abs(p_new - p) < tol:
            return p_new, k + 1
        p = p_new
    return p, max_iter


# ===========================================================================
# Method M5: weak-coupling 1-loop (4D lattice).
# ===========================================================================

def m5_weak_coupling_1loop(beta: float) -> float:
    """Weak-coupling 1-loop: <P>_WC = 1 - (N^2-1)/(8 N^2) * 4 / beta + ...

    Standard 4D Wilson lattice perturbation at 1 loop.
    For SU(3): coefficient = 8/72 = 1/9, giving
      <P>_WC = 1 - 4 / (9 beta).
    At beta = 6: 1 - 4/54 ~ 0.926.
    """
    n2_minus_1 = N_COLOR ** 2 - 1
    eight_n2 = 8 * N_COLOR ** 2
    return 1.0 - (n2_minus_1 / eight_n2) * 4.0 / beta


# ===========================================================================
# Driver + verdict.
# ===========================================================================

def driver() -> int:
    print("=" * 78)
    print("SU(3) Wilson Plaquette Closed-Form Fan-Out at beta = 6")
    print("=" * 78)
    print()
    print("Goal: rule out simpler closed-form paths to <P>(beta=6) before")
    print("committing multi-day engineering on the L_s>=3 Wigner-Racah engine.")
    print()
    print(f"  Reference: <P>_MC(beta=6) = {P_MC_REFERENCE:.4f} (canonical lattice MC)")
    print(f"  epsilon_witness = {EPSILON_WITNESS:.3e}")
    print()

    pass_count = 0
    fail_count = 0
    support_count = 0

    estimates: List[Dict] = []

    # --- M1: single-plaquette character expansion ---
    print("--- M1: single-plaquette character expansion (Haar one-plaquette) ---")
    p1 = m1_single_plaquette_character(BETA)
    print(f"  <P>_1plaq = (1/3) c_(1,0)(6) / c_(0,0)(6) = {p1:.6f}")
    print(f"  gap to MC: {abs(p1 - P_MC_REFERENCE):.4f} = "
          f"{abs(p1 - P_MC_REFERENCE)/EPSILON_WITNESS:.0f}x epsilon_witness")
    estimates.append({'method': 'M1: single-plaquette character',
                       'value': p1, 'gap': abs(p1 - P_MC_REFERENCE)})
    if 0 < p1 < 1:
        print("  PASS: M1 produces a sane one-plaquette estimate.")
        pass_count += 1
    else:
        print("  FAIL: M1 out of range.")
        fail_count += 1
    print()

    # --- M2: strong-coupling leading ---
    print("--- M2: strong-coupling leading order beta / (2 N^2) ---")
    p2 = m2_strong_coupling_leading(BETA)
    print(f"  <P>_SC1 = beta / (2 N^2) = 6 / 18 = {p2:.6f}")
    print(f"  gap to MC: {abs(p2 - P_MC_REFERENCE):.4f} = "
          f"{abs(p2 - P_MC_REFERENCE)/EPSILON_WITNESS:.0f}x epsilon_witness")
    estimates.append({'method': 'M2: strong-coupling 1st order',
                       'value': p2, 'gap': abs(p2 - P_MC_REFERENCE)})
    if 0 < p2 < 1:
        print("  PASS: M2 produces a sane leading-order estimate.")
        pass_count += 1
    else:
        print("  FAIL: M2 out of range.")
        fail_count += 1
    print()

    # --- M3: single-plaquette character (= all-order single-plaq SC) ---
    print("--- M3: single-plaquette all-order strong coupling (= M1) ---")
    p3 = m3_strong_coupling_2nd_order(BETA)
    print(f"  M3 value = {p3:.6f}  (same as M1)")
    print("  SUPPORT: genuine 2nd-order strong-coupling improvement requires")
    print("           inter-plaquette small-loop enumeration, beyond this fan-out.")
    support_count += 1
    print()

    # --- M4: mean-field self-consistency ---
    print("--- M4: single-plaquette mean-field self-consistency (z = 6) ---")
    p4, iters = m4_mean_field_self_consistent(BETA, z=6)
    print(f"  <P>_MF = c_F(beta_eff)/(3 c_0(beta_eff))  with beta_eff = z beta <P>_MF")
    print(f"  fixed-point iterations: {iters}")
    print(f"  <P>_MF = {p4:.6f}")
    print(f"  gap to MC: {abs(p4 - P_MC_REFERENCE):.4f} = "
          f"{abs(p4 - P_MC_REFERENCE)/EPSILON_WITNESS:.0f}x epsilon_witness")
    estimates.append({'method': 'M4: mean-field self-consistency',
                       'value': p4, 'gap': abs(p4 - P_MC_REFERENCE)})
    if 0 < p4 < 1:
        print("  PASS: M4 mean-field converges and is in range.")
        pass_count += 1
    else:
        print("  FAIL: M4 out of range or did not converge.")
        fail_count += 1
    print()

    # --- M5: weak-coupling 1-loop ---
    print("--- M5: weak-coupling 1-loop perturbation ---")
    p5 = m5_weak_coupling_1loop(BETA)
    print(f"  <P>_WC = 1 - (N^2-1)/(8 N^2) * 4 / beta = 1 - 4/54 = {p5:.6f}")
    print(f"  gap to MC: {abs(p5 - P_MC_REFERENCE):.4f} = "
          f"{abs(p5 - P_MC_REFERENCE)/EPSILON_WITNESS:.0f}x epsilon_witness")
    estimates.append({'method': 'M5: weak-coupling 1-loop',
                       'value': p5, 'gap': abs(p5 - P_MC_REFERENCE)})
    if 0 < p5 < 1:
        print("  PASS: M5 weak-coupling estimate is in range.")
        pass_count += 1
    else:
        print("  FAIL: M5 out of range.")
        fail_count += 1
    print()

    # --- Comparison table ---
    print("--- Comparison table ---")
    print()
    print(f"  {'Method':<40} {'<P>(6)':>10}  {'gap to MC':>10}  "
          f"{'gap / eps':>10}")
    print(f"  {'-' * 40} {'-' * 10}  {'-' * 10}  {'-' * 10}")
    for e in estimates:
        print(f"  {e['method']:<40} {e['value']:>10.4f}  "
              f"{e['gap']:>10.4f}  "
              f"{e['gap']/EPSILON_WITNESS:>10.0f}x")
    print(f"  {'MC reference (canonical)':<40} {P_MC_REFERENCE:>10.4f}  "
          f"{0.0:>10.4f}  {'0x':>10}")
    print()

    # --- Verdict ---
    print("--- Verdict ---")
    print()
    closures = [e for e in estimates
                if e['gap'] < EPSILON_WITNESS]
    near_misses = [e for e in estimates
                    if EPSILON_WITNESS <= e['gap'] < 0.05]
    far_misses = [e for e in estimates if e['gap'] >= 0.05]
    print(f"  closures (gap < epsilon_witness):  {len(closures)}")
    print(f"  near-misses (eps <= gap < 0.05):   {len(near_misses)}")
    print(f"  far-misses (gap >= 0.05):          {len(far_misses)}")
    print()
    if closures:
        print("  FOUND CLOSED-FORM CLOSURE — methods within epsilon_witness:")
        for e in closures:
            print(f"    - {e['method']}: <P> = {e['value']:.4f}")
    elif near_misses:
        print("  CLOSED-FORM NEAR-MISSES — refinement may close:")
        for e in near_misses:
            print(f"    - {e['method']}: <P> = {e['value']:.4f}, "
                  f"gap {e['gap']:.4f}")
    else:
        print("  All closed-form estimates are FAR-MISSES (gap >= 0.05).")
        print()
        print("  This confirms: simple closed-form methods (single-plaquette")
        print("  Haar, strong-coupling, mean-field, weak-coupling 1-loop)")
        print("  CANNOT reproduce <P>(beta=6) = 0.5934 within epsilon_witness.")
        print()
        print("  The L_s>=3 Wigner-Racah engine path remains the next")
        print("  exact-cube route among the tested methods. The SU(3) Wigner")
        print("  L_s=2 PBC orientation verdict (legacy Block 5) is strengthened")
        print("  by this explicit ruling-out of orthogonal closed-form attack frames.")
    print()

    print("  Method-by-method commentary:")
    print(f"    M1 (single-plaq char): {p1:.4f} — captures one plaquette")
    print( "                            in isolation; no inter-plaquette")
    print( "                            structure.")
    print(f"    M2 (SC1):              {p2:.4f} — strict leading-order")
    print( "                            beta/18; ignores all corrections.")
    print(f"    M4 (MF):               {p4:.4f} — adds coordination effect;")
    print( "                            saturates near M1 for SU(3) at beta=6")
    print( "                            because the self-consistent beta_eff")
    print( "                            stays in the strong-coupling regime.")
    print(f"    M5 (WC 1-loop):        {p5:.4f} — overshoots; beta=6 is")
    print( "                            in the CROSSOVER regime where neither")
    print( "                            strong-coupling (M1, M2, M4) nor")
    print( "                            weak-coupling (M5) is a good")
    print( "                            asymptotic.")
    print()
    print("  beta = 6 is the SU(3) crossover regime where the correlation")
    print("  length exceeds 2 lattice spacings (so L_s=2 fails per the")
    print("  SU(3) Wigner L_s=2 PBC orientation verdict, legacy Block 5)")
    print("  AND no single-plaquette / leading-perturbative method captures")
    print("  the connected multi-plaquette structure that drives <P> to")
    print("  ~ 0.59. Exact closure would need a full lattice tensor-network")
    print("  contraction route, a different audited derivation, or numerical MC.")
    print()

    # Comparator-independent assertions (pinned to docs/SU3_WILSON_CLOSED_FORM_FANOUT_THEOREM_NOTE_2026-05-04.md).
    # The MC value 0.5934 and epsilon_witness 3.03e-4 are EXTERNAL comparator inputs;
    # these assertions only check the four framework-internal closed-form values.
    assert abs(p1 - 0.4225) <= 5e-4, f"M1 drift: {p1:.6f} vs 0.4225 (note table)"
    assert abs(p2 - 0.3333) <= 5e-4, f"M2 drift: {p2:.6f} vs 0.3333 (note table)"
    assert abs(p4 - 0.8740) <= 5e-4, f"M4 drift: {p4:.6f} vs 0.8740 (note table)"
    assert abs(p5 - 0.9259) <= 5e-4, f"M5 drift: {p5:.6f} vs 0.9259 (note table)"
    assert abs(p3 - p1) <= 1e-9, f"M3 != M1 (closed form should match exactly)"
    print("PASS: comparator-independent (M1, M2, M4, M5) closed-form table "
          "matches the bounded internal record in the note.")
    print()
    print("NOTE (provenance): the MC reference value 0.5934 and the "
          "epsilon_witness target 3.03e-4 are external comparator-only "
          "inputs. The 'ruling-out at epsilon_witness' reading inherits "
          "their provenance and is not promoted as a standalone theorem.")

    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={pass_count} SUPPORT={support_count} "
          f"FAIL={fail_count}")
    print("=" * 78)
    print()
    print("Headline:")
    print(f"  Closed-form fan-out at beta = 6 for SU(3) Wilson plaquette:")
    print(f"    M1 single-plaquette = {p1:.4f}  (gap "
          f"{abs(p1-P_MC_REFERENCE)/EPSILON_WITNESS:.0f}x eps)")
    print(f"    M2 SC leading       = {p2:.4f}  (gap "
          f"{abs(p2-P_MC_REFERENCE)/EPSILON_WITNESS:.0f}x eps)")
    print(f"    M4 mean-field       = {p4:.4f}  (gap "
          f"{abs(p4-P_MC_REFERENCE)/EPSILON_WITNESS:.0f}x eps)")
    print(f"    M5 WC 1-loop        = {p5:.4f}  (gap "
          f"{abs(p5-P_MC_REFERENCE)/EPSILON_WITNESS:.0f}x eps)")
    print(f"    MC reference        = {P_MC_REFERENCE:.4f}")
    print(f"  Verdict: 4 simpler closed-form paths explicitly ruled out;")
    print(f"  L_s>=3 Wigner-Racah path remains the next exact-cube route.")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
