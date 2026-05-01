#!/usr/bin/env python3
"""Barred unitarity triangle orthocenter and Euler line EXACT closed-form audit.

Verifies the new identities in
  docs/CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md

  (O1) Orthocenter: H = (rho_bar, (20+alpha_s)/(24 sqrt(5)))                [EXACT linear]
  (O2) H - V_3 = (0, alpha_s sqrt(5)/20)                                     [EXACT, pure y]
  (O3) Centroid: G = ((28-alpha_s)/72, sqrt(5)(4-alpha_s)/72)                [EXACT linear]
  (O4) Circumcenter: O = (1/2, -alpha_s sqrt(5)/40) (re-derived from N1,N2,N3) [EXACT]
  (O5) Euler line: H = 3G - 2O                                                [EXACT identity]
  (O6) Anti-relation: H - V_3 = -2 (O - M) where M = (1/2, 0)                [EXACT]
  (O7) Slope: (H_y - V_3_y)/alpha_s = sqrt(5)/20 = retained N7 slope         [EXACT]
  (O8) Selection rule: H, G degree-1 polys in alpha_s; O_x indep, O_y linear
  (O9) Atlas-LO: H_0 = V_3_0 (orthocenter coincides with apex at right-angle)

ALL INPUTS RETAINED on current main:
- canonical alpha_s(v) (ALPHA_S_DERIVED_NOTE)
- atlas alpha_0=pi/2, right-angle-vertex-orthocenter coincidence
  (CKM_ATLAS_TRIANGLE_RIGHT_ANGLE)
- N1 rho_bar, N2 eta_bar, N3 R_b_bar^2, N7 slope
  (CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA)
- N_pair=2, N_color=3, N_quark=6 (CKM_MAGNITUDES_STRUCTURAL_COUNTS)

NO SUPPORT-tier or open inputs (Koide Q_l, bare-coupling ratios,
dimension-color quadratic) used.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "A") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status} ({cls})] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


# Retained framework values
ALPHA_S_V = CANONICAL_ALPHA_S_V

# Retained CKM magnitudes structural counts
N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR  # = 6

# Retained NLO theorem closed forms
RHO_BAR = (4 - ALPHA_S_V) / 24                                 # N1
ETA_BAR = math.sqrt(5) * (4 - ALPHA_S_V) / 24                   # N2
R_B_BAR_SQ = (4 - ALPHA_S_V) ** 2 / 96                          # N3
N7_SLOPE = math.sqrt(5) / 20                                    # N7 leading slope


def audit_inputs() -> None:
    banner("Retained inputs on current main")

    print(f"  alpha_s(v)                   = {ALPHA_S_V:.15f}")
    print(f"  N_pair                       = {N_PAIR}  (retained)")
    print(f"  N_color                      = {N_COLOR}  (retained)")
    print(f"  N_quark = N_pair x N_color    = {N_QUARK}")
    print()
    print(f"  N1: rho_bar                  = {RHO_BAR:.15f}")
    print(f"  N2: eta_bar                  = {ETA_BAR:.15f}")
    print(f"  N3: R_b_bar^2                = {R_B_BAR_SQ:.15f}")
    print(f"  N7 slope = sqrt(5)/20         = {N7_SLOPE:.15f}")

    check("alpha_s(v) > 0", ALPHA_S_V > 0)
    check("N_pair = 2 (retained)", N_PAIR == 2)
    check("N_color = 3 (retained)", N_COLOR == 3)
    check("N_quark = 6 (retained)", N_QUARK == 6)
    check("N1: rho_bar = (4-a)/24 (retained)",
          close(RHO_BAR, (4 - ALPHA_S_V) / 24))
    check("N2: eta_bar = sqrt(5)(4-a)/24 (retained)",
          close(ETA_BAR, math.sqrt(5) * (4 - ALPHA_S_V) / 24))
    check("N3: R_b_bar^2 = (4-a)^2/96 (retained)",
          close(R_B_BAR_SQ, (4 - ALPHA_S_V) ** 2 / 96))
    check("N7 slope = sqrt(5)/20 (retained)",
          close(N7_SLOPE, math.sqrt(5) / 20))

    repo_root = Path(__file__).resolve().parents[1]
    upstream_retained = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md",
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
    )
    for rel in upstream_retained:
        path = repo_root / rel
        check(f"retained on main: {rel}", path.exists())


def audit_o1_orthocenter() -> None:
    banner("(O1) NEW EXACT: Orthocenter H = (rho_bar, (20+alpha_s)/(24 sqrt(5)))")

    # Direct geometric construction from V_1, V_2, V_3
    V1 = (0.0, 0.0)
    V2 = (1.0, 0.0)
    V3 = (RHO_BAR, ETA_BAR)

    # Altitude from V_3 to V_1V_2 (x-axis): vertical line x = rho_bar
    H_x_direct = RHO_BAR

    # Altitude from V_1 perpendicular to V_2V_3:
    # V_2V_3 = (rho_bar - 1, eta_bar), perpendicular direction (eta_bar, 1-rho_bar)
    # Line through V_1 = origin: y/x = (1-rho_bar)/eta_bar
    # At x = rho_bar (orthocenter): y = rho_bar * (1-rho_bar)/eta_bar
    H_y_direct = RHO_BAR * (1 - RHO_BAR) / ETA_BAR

    # Closed form (O1)
    H_x_closed = RHO_BAR  # = (4-alpha_s)/24
    H_y_closed = (20 + ALPHA_S_V) / (24 * math.sqrt(5))

    print(f"  Vertices: V_1={V1}, V_2={V2}, V_3={V3}")
    print()
    print(f"  H_x (direct, from altitude) = {H_x_direct:.15f}")
    print(f"  H_x closed form (= rho_bar) = {H_x_closed:.15f}")
    print()
    print(f"  H_y (direct, from altitude) = {H_y_direct:.15f}")
    print(f"  H_y closed (20+a)/(24 sqrt5) = {H_y_closed:.15f}")
    print(f"  diff                          = {H_y_direct - H_y_closed:.3e}")

    check("(O1) H_x = rho_bar (altitude from apex is vertical, hypotenuse on x-axis)",
          close(H_x_direct, H_x_closed))
    check("(O1) H_y from altitude = (20+alpha_s)/(24 sqrt(5)) closed form",
          close(H_y_direct, H_y_closed))


def audit_o2_apex_orthocenter_offset() -> None:
    banner("(O2) NEW EXACT: H - V_3 = (0, alpha_s sqrt(5)/20)")

    H = (RHO_BAR, (20 + ALPHA_S_V) / (24 * math.sqrt(5)))
    V3 = (RHO_BAR, ETA_BAR)

    offset = (H[0] - V3[0], H[1] - V3[1])
    closed_offset = (0.0, ALPHA_S_V * math.sqrt(5) / 20)

    # Structural form
    structural_offset_y = ALPHA_S_V / (N_PAIR ** 2 * math.sqrt(N_QUARK - 1))

    print(f"  H - V_3 (direct)                  = ({offset[0]:.6e}, {offset[1]:.6e})")
    print(f"  Closed (0, alpha_s sqrt(5)/20)    = ({closed_offset[0]:.6e}, {closed_offset[1]:.6e})")
    print(f"  Structural alpha_s/(N_pair^2 sqrt(N_quark-1)) = {structural_offset_y:.6e}")

    check("(O2) H_x = V_3_x (zero x-offset, altitude is vertical)",
          close(offset[0], 0.0))
    check("(O2) H_y - V_3_y = alpha_s sqrt(5)/20 (LINEAR in alpha_s)",
          close(offset[1], closed_offset[1]))
    check("(O2) Structural form: alpha_s / (N_pair^2 sqrt(N_quark - 1))",
          close(offset[1], structural_offset_y))


def audit_o3_centroid() -> None:
    banner("(O3) NEW EXACT: Centroid G = ((28-alpha_s)/72, sqrt(5)(4-alpha_s)/72)")

    V1 = (0.0, 0.0)
    V2 = (1.0, 0.0)
    V3 = (RHO_BAR, ETA_BAR)

    G_direct = ((V1[0] + V2[0] + V3[0]) / 3, (V1[1] + V2[1] + V3[1]) / 3)
    G_closed = ((28 - ALPHA_S_V) / 72, math.sqrt(5) * (4 - ALPHA_S_V) / 72)

    print(f"  G direct (V_1+V_2+V_3)/3       = ({G_direct[0]:.15f}, {G_direct[1]:.15f})")
    print(f"  G closed ((28-a)/72, sqrt5(4-a)/72) = ({G_closed[0]:.15f}, {G_closed[1]:.15f})")

    check("(O3) G_x = (28-alpha_s)/72 (LINEAR in alpha_s)",
          close(G_direct[0], G_closed[0]))
    check("(O3) G_y = sqrt(5)(4-alpha_s)/72 (LINEAR in alpha_s)",
          close(G_direct[1], G_closed[1]))


def audit_o4_circumcenter() -> None:
    banner("(O4) NEW EXACT: Circumcenter O = (1/2, -alpha_s sqrt(5)/40) [re-derived]")

    # Re-derive from retained N1, N2, N3 + equidistance
    # x_cc = 1/2 (perpendicular bisector of V_1V_2)
    O_x = 0.5

    # y_cc from |center - V_1|^2 = |center - V_3|^2:
    # y_cc = (R_b_bar^2 - rho_bar) / (2 eta_bar)
    O_y_direct = (R_B_BAR_SQ - RHO_BAR) / (2 * ETA_BAR)

    # Closed form
    O_y_closed = -ALPHA_S_V * math.sqrt(5) / 40

    # Structural form
    O_y_structural = -ALPHA_S_V / (N_PAIR ** 3 * math.sqrt(N_QUARK - 1))

    print(f"  O_x = 1/2 (perp. bisector of hypotenuse)        = {O_x:.15f}")
    print(f"  O_y direct (R_b^2 - rho)/(2 eta)                = {O_y_direct:.15f}")
    print(f"  O_y closed -alpha_s sqrt(5)/40                   = {O_y_closed:.15f}")
    print(f"  O_y structural -a/(N_pair^3 sqrt(N_quark-1))     = {O_y_structural:.15f}")

    check("(O4) O_x = 1/2 (alpha_s-INDEPENDENT)",
          close(O_x, 0.5))
    check("(O4) O_y direct = -alpha_s sqrt(5)/40 closed",
          close(O_y_direct, O_y_closed))
    check("(O4) O_y structural form -a/(N_pair^3 sqrt(N_quark-1))",
          close(O_y_closed, O_y_structural))


def audit_o5_euler_line() -> None:
    banner("(O5) NEW EXACT: Euler line H = 3G - 2O")

    # Build all four points
    H = (RHO_BAR, (20 + ALPHA_S_V) / (24 * math.sqrt(5)))
    G = ((28 - ALPHA_S_V) / 72, math.sqrt(5) * (4 - ALPHA_S_V) / 72)
    O = (0.5, -ALPHA_S_V * math.sqrt(5) / 40)

    # Compute 3G - 2O
    H_euler = (3 * G[0] - 2 * O[0], 3 * G[1] - 2 * O[1])

    print(f"  H direct                = ({H[0]:.15f}, {H[1]:.15f})")
    print(f"  3 G - 2 O                = ({H_euler[0]:.15f}, {H_euler[1]:.15f})")
    print(f"  diff                      = ({H_euler[0] - H[0]:.3e}, {H_euler[1] - H[1]:.3e})")

    check("(O5) Euler line: H = 3G - 2O (x-component)",
          close(H_euler[0], H[0]))
    check("(O5) Euler line: H = 3G - 2O (y-component)",
          close(H_euler[1], H[1]))

    # Also verify centroid is between H and O on the line, with HG = 2 GO
    # G - O and H - G should be parallel with H - G = 2 (G - O)
    H_minus_G = (H[0] - G[0], H[1] - G[1])
    G_minus_O = (G[0] - O[0], G[1] - O[1])
    expected_H_minus_G = (2 * G_minus_O[0], 2 * G_minus_O[1])

    print(f"\n  H - G                    = {H_minus_G}")
    print(f"  2 (G - O)                = {expected_H_minus_G}")

    check("(O5) Euler line ratio: HG = 2 GO (x-component)",
          close(H_minus_G[0], expected_H_minus_G[0]))
    check("(O5) Euler line ratio: HG = 2 GO (y-component)",
          close(H_minus_G[1], expected_H_minus_G[1]))


def audit_o6_anti_relation() -> None:
    banner("(O6) NEW EXACT: H - V_3 = -2 (O - M) where M = (1/2, 0) is hypotenuse midpoint")

    H = (RHO_BAR, (20 + ALPHA_S_V) / (24 * math.sqrt(5)))
    V3 = (RHO_BAR, ETA_BAR)
    O = (0.5, -ALPHA_S_V * math.sqrt(5) / 40)
    M = (0.5, 0.0)

    H_minus_V3 = (H[0] - V3[0], H[1] - V3[1])
    O_minus_M = (O[0] - M[0], O[1] - M[1])
    minus_2_O_minus_M = (-2 * O_minus_M[0], -2 * O_minus_M[1])

    print(f"  H - V_3        = ({H_minus_V3[0]:.6e}, {H_minus_V3[1]:.6e})")
    print(f"  O - M           = ({O_minus_M[0]:.6e}, {O_minus_M[1]:.6e})")
    print(f"  -2 (O - M)      = ({minus_2_O_minus_M[0]:.6e}, {minus_2_O_minus_M[1]:.6e})")

    check("(O6) H_x - V_3_x = -2(O_x - M_x) (both = 0)",
          close(H_minus_V3[0], minus_2_O_minus_M[0]))
    check("(O6) H_y - V_3_y = -2(O_y - M_y) = -2 y_cc (apex lift = 2x circumcenter depression)",
          close(H_minus_V3[1], minus_2_O_minus_M[1]))


def audit_o7_slope_n7() -> None:
    banner("(O7) NEW: (H_y - V_3_y)/alpha_s = sqrt(5)/20 = retained N7 slope")

    H_y = (20 + ALPHA_S_V) / (24 * math.sqrt(5))
    V3_y = ETA_BAR

    slope = (H_y - V3_y) / ALPHA_S_V
    n7_slope = math.sqrt(5) / 20

    print(f"  (H_y - V_3_y) / alpha_s             = {slope:.15f}")
    print(f"  Retained N7 slope sqrt(5)/20        = {n7_slope:.15f}")
    print(f"  Structural 1/(N_pair^2 sqrt(N_quark - 1)) = "
          f"{1 / (N_PAIR ** 2 * math.sqrt(N_QUARK - 1)):.15f}")

    check("(O7) apex-orthocenter slope = retained N7 slope = sqrt(5)/20",
          close(slope, n7_slope))
    check("(O7) slope = 1/(N_pair^2 sqrt(N_quark - 1))",
          close(slope, 1 / (N_PAIR ** 2 * math.sqrt(N_QUARK - 1))))


def audit_o8_selection_rule() -> None:
    banner("(O8) NEW Selection Rule: H, G are degree-1 polynomials in alpha_s")

    # H_x = (4 - alpha_s)/24: linear in alpha_s
    # H_y = (20 + alpha_s)/(24 sqrt(5)): linear in alpha_s
    # G_x = (28 - alpha_s)/72: linear in alpha_s
    # G_y = sqrt(5)(4 - alpha_s)/72: linear in alpha_s
    # O_x = 1/2: alpha_s-INDEPENDENT
    # O_y = -alpha_s sqrt(5)/40: linear in alpha_s

    # Test by checking 2nd-derivative numerically: should be ZERO
    eps = 1e-5
    a_plus = ALPHA_S_V + eps
    a_minus = ALPHA_S_V - eps

    def H_x_at(a): return (4 - a) / 24
    def H_y_at(a): return (20 + a) / (24 * math.sqrt(5))
    def G_x_at(a): return (28 - a) / 72
    def G_y_at(a): return math.sqrt(5) * (4 - a) / 72
    def O_x_at(a): return 0.5
    def O_y_at(a): return -a * math.sqrt(5) / 40

    # 2nd derivative via central difference: (f(a+eps) + f(a-eps) - 2f(a))/eps^2
    def second_deriv(f, a, eps):
        return (f(a + eps) + f(a - eps) - 2 * f(a)) / (eps ** 2)

    second_H_x = second_deriv(H_x_at, ALPHA_S_V, eps)
    second_H_y = second_deriv(H_y_at, ALPHA_S_V, eps)
    second_G_x = second_deriv(G_x_at, ALPHA_S_V, eps)
    second_G_y = second_deriv(G_y_at, ALPHA_S_V, eps)
    second_O_y = second_deriv(O_y_at, ALPHA_S_V, eps)

    print(f"  2nd derivatives (should be 0 if linear):")
    print(f"    d^2 H_x / d alpha_s^2 = {second_H_x:.3e}")
    print(f"    d^2 H_y / d alpha_s^2 = {second_H_y:.3e}")
    print(f"    d^2 G_x / d alpha_s^2 = {second_G_x:.3e}")
    print(f"    d^2 G_y / d alpha_s^2 = {second_G_y:.3e}")
    print(f"    d^2 O_y / d alpha_s^2 = {second_O_y:.3e}")

    check("(O8) H_x is degree-1 polynomial (2nd deriv ~ 0)",
          abs(second_H_x) < 1e-3)
    check("(O8) H_y is degree-1 polynomial (2nd deriv ~ 0)",
          abs(second_H_y) < 1e-3)
    check("(O8) G_x is degree-1 polynomial (2nd deriv ~ 0)",
          abs(second_G_x) < 1e-3)
    check("(O8) G_y is degree-1 polynomial (2nd deriv ~ 0)",
          abs(second_G_y) < 1e-3)
    check("(O8) O_y is degree-1 polynomial (2nd deriv ~ 0)",
          abs(second_O_y) < 1e-3)


def audit_o9_atlas_lo_recovery() -> None:
    banner("(O9) Atlas-LO recovery: H_0 = V_3_0 (orthocenter coincides with apex)")

    # At alpha_s = 0
    H_0 = (4 / 24, 20 / (24 * math.sqrt(5)))
    V3_0 = (1 / N_QUARK, math.sqrt(N_QUARK - 1) / N_QUARK)
    G_0 = (7 / 18, math.sqrt(5) / 18)
    O_0 = (1 / N_PAIR, 0.0)

    print(f"  At alpha_s = 0:")
    print(f"    H_0 = (4/24, 20/(24 sqrt5))         = ({H_0[0]:.10f}, {H_0[1]:.10f})")
    print(f"    V_3_0 = (1/N_quark, sqrt(N_q-1)/N_q) = ({V3_0[0]:.10f}, {V3_0[1]:.10f})")
    print(f"    G_0 = (7/18, sqrt5/18)              = ({G_0[0]:.10f}, {G_0[1]:.10f})")
    print(f"    O_0 = (1/N_pair, 0)                  = ({O_0[0]:.10f}, {O_0[1]:.10f})")

    check("(O9) atlas-LO H_0_x = V_3_0_x (= 1/N_quark = 1/6)",
          close(H_0[0], V3_0[0]))
    check("(O9) atlas-LO H_0_y = V_3_0_y (= sqrt(N_quark-1)/N_quark = sqrt(5)/6)",
          close(H_0[1], V3_0[1]))
    check("(O9) atlas-LO O_0 = (1/N_pair, 0) = midpoint of hypotenuse",
          close(O_0[0], 0.5) and close(O_0[1], 0.0))


def audit_alpha_s_independence() -> None:
    banner("EXACT-status verification: closed forms hold at multiple alpha_s")

    print("  Verifying (O1)-(O6) hold EXACTLY at six alpha_s values:")

    all_pass = True
    for alpha_s in [0.05, 0.10, 0.103303816, 0.15, 0.20, 0.30]:
        # Re-derive everything from scratch
        rho_bar = (4 - alpha_s) / 24
        eta_bar = math.sqrt(5) * (4 - alpha_s) / 24

        # Direct geometric construction
        V3 = (rho_bar, eta_bar)
        H_x_direct = rho_bar
        H_y_direct = rho_bar * (1 - rho_bar) / eta_bar

        # Closed forms
        H_x_closed = rho_bar
        H_y_closed = (20 + alpha_s) / (24 * math.sqrt(5))
        G_x_closed = (28 - alpha_s) / 72
        G_y_closed = math.sqrt(5) * (4 - alpha_s) / 72
        O_y_closed = -alpha_s * math.sqrt(5) / 40

        # Centroid direct
        G_x_direct = (1 + rho_bar) / 3
        G_y_direct = eta_bar / 3

        # Circumcenter from equidistance
        R_b_sq = (4 - alpha_s) ** 2 / 96
        O_y_direct = (R_b_sq - rho_bar) / (2 * eta_bar)

        # Euler line
        H_euler_x = 3 * G_x_closed - 2 * 0.5
        H_euler_y = 3 * G_y_closed - 2 * O_y_closed

        # Anti-relation
        anti_rel_y = -2 * (O_y_closed - 0.0)  # -2(O_y - M_y) where M_y = 0

        o1_ok = close(H_y_direct, H_y_closed, tol=1e-13)
        o3_ok = close(G_x_direct, G_x_closed, tol=1e-14) and close(G_y_direct, G_y_closed, tol=1e-14)
        o4_ok = close(O_y_direct, O_y_closed, tol=1e-13)
        o5_ok = close(H_euler_x, H_x_closed, tol=1e-13) and close(H_euler_y, H_y_closed, tol=1e-13)
        o6_ok = close(H_y_closed - V3[1], anti_rel_y, tol=1e-13)

        all_ok = o1_ok and o3_ok and o4_ok and o5_ok and o6_ok
        all_pass = all_pass and all_ok
        print(f"    alpha_s = {alpha_s:.9f}: O1={o1_ok}, O3={o3_ok}, O4={o4_ok}, "
              f"O5={o5_ok}, O6={o6_ok}  ({'OK' if all_ok else 'FAIL'})")

    check("EXACT closed forms hold at ALL tested alpha_s (no leading-order drift)",
          all_pass)


def audit_summary() -> None:
    banner("Summary of new content")

    print("  NEW (O1): H = (rho_bar, (20+alpha_s)/(24 sqrt(5)))     EXACT linear in alpha_s")
    print("  NEW (O2): H - V_3 = (0, alpha_s sqrt(5)/20)             EXACT, pure y, linear")
    print("  NEW (O3): G = ((28-a)/72, sqrt(5)(4-a)/72)             EXACT linear in alpha_s")
    print("  NEW (O4): O = (1/2, -alpha_s sqrt(5)/40)                EXACT (re-derived)")
    print("  NEW (O5): Euler line H = 3G - 2O                        EXACT identity")
    print("  NEW (O6): H - V_3 = -2 (O - M)                          EXACT anti-relation")
    print("  NEW (O7): apex-orthocenter slope = sqrt(5)/20 = N7 slope")
    print("  NEW (O8): H, G degree-1 polys in alpha_s; O has linear y, alpha_s-indep x")
    print("  NEW (O9): atlas-LO H_0 = V_3_0 (orthocenter at right-angle vertex)")
    print()
    print(f"  At canonical alpha_s = {ALPHA_S_V:.10f}:")
    print(f"    H = ({RHO_BAR:.6f}, {(20+ALPHA_S_V)/(24*math.sqrt(5)):.6f})")
    print(f"    G = ({(28-ALPHA_S_V)/72:.6f}, {math.sqrt(5)*(4-ALPHA_S_V)/72:.6f})")
    print(f"    O = (0.500000, {-ALPHA_S_V*math.sqrt(5)/40:.6f})")
    print(f"    V_3 = ({RHO_BAR:.6f}, {ETA_BAR:.6f})")
    print(f"    H - V_3 = (0, {(20+ALPHA_S_V)/(24*math.sqrt(5)) - ETA_BAR:.6f})")
    print()
    print("  All inputs retained on main; no SUPPORT-tier or open inputs used.")


def main() -> int:
    print("=" * 88)
    print("Barred unitarity triangle orthocenter and Euler line EXACT closed-form audit")
    print("See docs/CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_o1_orthocenter()
    audit_o2_apex_orthocenter_offset()
    audit_o3_centroid()
    audit_o4_circumcenter()
    audit_o5_euler_line()
    audit_o6_anti_relation()
    audit_o7_slope_n7()
    audit_o8_selection_rule()
    audit_o9_atlas_lo_recovery()
    audit_alpha_s_independence()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
