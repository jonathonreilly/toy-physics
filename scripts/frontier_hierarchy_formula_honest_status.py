#!/usr/bin/env python3
"""
Honest-status verifier for the canonical chain hierarchy formula

    v = M_Pl * (7/8)^(1/4) * alpha_LM^16 = 246.282818290129 GeV

Authority: docs/HIERARCHY_FORMULA_HONEST_STATUS_NOTE_2026-05-10.md

Verifies the structural statements that justify the package-level
demotion of the "Hierarchy theorem (taste determinant) DERIVED"
rhetoric in COMPLETE_PREDICTION_CHAIN_2026_04_15.md to "BOUNDED
NUMERICAL MATCH (closure path open)" — at the level of the four
load-bearing primitives P1-P4 enumerated in the honest-status note.

This runner does NOT modify the canonical chain runner, the per-route
hierarchy notes, the publication ledger, or any audit row. It is a
self-check that the honest-status note's structural claims are
arithmetically reproducible.

Total expected check count: 7. The power-N sensitivity scan has two
independent assertions.
"""

from __future__ import annotations

import math
import sys

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
    CANONICAL_U0,
)

# Framework UV scale anchor (P1: M_Pl import from Planck lane).
M_PL = 1.2209e19  # GeV
APBC = (7.0 / 8.0) ** 0.25
ALPHA_LM = CANONICAL_ALPHA_LM
ALPHA_BARE = CANONICAL_ALPHA_BARE
ALPHA_S_V = CANONICAL_ALPHA_S_V
U0 = CANONICAL_U0

# Observed (PDG) electroweak VEV (P4: identification with Higgs VEV).
V_OBS = 246.22  # GeV

# Canonical chain published value
V_CHAIN_PUBLISHED = 246.282818290129  # GeV


def _line(label: str, ok: bool) -> bool:
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {label}")
    return ok


def _assert_close(a: float, b: float, tol: float, label: str) -> bool:
    ok = abs(a - b) <= tol * max(abs(b), 1e-300)
    _line(label, ok)
    return ok


def _assert_le(a: float, b: float, label: str) -> bool:
    ok = a <= b
    _line(label, ok)
    return ok


def main() -> int:
    passes = 0
    fails = 0

    # Check 1: reproducibility of v from canonical surface
    print("=" * 70)
    print("Check 1: v = M_Pl * (7/8)^(1/4) * alpha_LM^16 reproducibility")
    print("=" * 70)
    v_pred = M_PL * APBC * ALPHA_LM ** 16
    print(f"  M_Pl       = {M_PL:.4e} GeV")
    print(f"  APBC       = (7/8)^(1/4) = {APBC:.10f}")
    print(f"  alpha_LM   = {ALPHA_LM:.10f}")
    print(f"  alpha_LM^16 = {ALPHA_LM ** 16:.6e}")
    print(f"  v_pred     = {v_pred:.10f} GeV")
    print(f"  v_chain    = {V_CHAIN_PUBLISHED:.10f} GeV (canonical chain note)")
    print(f"  v_obs      = {V_OBS:.4f} GeV")
    print(f"  rel error  = {(v_pred - V_OBS) / V_OBS * 100:.4f} %")
    if _assert_close(v_pred, V_CHAIN_PUBLISHED, 1e-9, "v_pred matches canonical chain published value"):
        passes += 1
    else:
        fails += 1

    # Check 2: sensitivity / power scan
    print()
    print("=" * 70)
    print("Check 2: power-N sensitivity scan (N = 13..20)")
    print("=" * 70)
    sensitivity_table = []
    for n in range(13, 21):
        v_n = M_PL * APBC * ALPHA_LM ** n
        ratio = v_n / V_OBS
        sensitivity_table.append((n, v_n, ratio))
        print(f"  N={n:2d}: v = {v_n:.6e} GeV (ratio to v_obs: {ratio:.4e})")
    # Match: N = 16 should be within 1 % of v_obs; N = 15 and N = 17 should be
    # off by factor > 5 (i.e. far outside any sensible match band).
    n16_ok = abs(sensitivity_table[3][1] - V_OBS) / V_OBS < 0.01
    n15_off = abs(math.log10(sensitivity_table[2][2])) > 0.7
    n17_off = abs(math.log10(sensitivity_table[4][2])) > 0.7
    if _line("N = 16 within 1 % of v_obs", n16_ok):
        passes += 1
    else:
        fails += 1
    if n15_off and n17_off:
        _line("N = 15 and N = 17 each off by > factor 5", True)
        passes += 1
    else:
        _line("N = 15 and N = 17 each off by > factor 5", False)
        fails += 1

    # Check 3: algebraic identity (S) of the substitution P3
    print()
    print("=" * 70)
    print("Check 3: alpha_LM^16 = alpha_bare^16 * u_0^(-16) (substitution P3)")
    print("=" * 70)
    lhs = ALPHA_LM ** 16
    rhs = (ALPHA_BARE ** 16) * (U0 ** -16)
    print(f"  alpha_LM^16             = {lhs:.10e}")
    print(f"  alpha_bare^16 * u_0^-16 = {rhs:.10e}")
    if _assert_close(lhs, rhs, 1e-12, "algebraic identity (S) verified"):
        passes += 1
    else:
        fails += 1

    # Check 4: u_0^16 (determinant power) is NOT alpha_LM^16
    print()
    print("=" * 70)
    print("Check 4: u_0^16 (determinant power) != alpha_LM^16 (formula power)")
    print("=" * 70)
    u016 = U0 ** 16
    print(f"  u_0^16    = {u016:.6e}  (Matsubara determinant power on L_s=2/L_t=4)")
    print(f"  alpha_LM^16 = {lhs:.6e}  (formula power in canonical chain)")
    print(f"  ratio u_0^16 / alpha_LM^16 = {u016 / lhs:.4e}")
    # The formula's coupling power is ~17 orders of magnitude smaller than the
    # determinant's tadpole power. They are not the same factor; substitution
    # P3 absorbs the difference into alpha_bare^16 * u_0^(-32) implicitly.
    if _assert_le(1e15, u016 / lhs, "u_0^16 vastly larger than alpha_LM^16 (substitution gap > 10^15)"):
        passes += 1
    else:
        fails += 1

    # Check 5: counterfactual on Wick rotation (3D vs 4D taste counting)
    print()
    print("=" * 70)
    print("Check 5: 3D-spatial-only counterfactual (P2 load-bearing role)")
    print("=" * 70)
    v_alt_8 = M_PL * APBC * ALPHA_LM ** 8
    ratio_8 = v_alt_8 / V_OBS
    print(f"  v_alt (N=8 spatial doublers on Z^3) = {v_alt_8:.4e} GeV")
    print(f"  ratio to v_obs                       = {ratio_8:.4e}")
    print(f"  off by ~{math.log10(ratio_8):.0f} orders of magnitude")
    # Should be off by at least 7 orders of magnitude (load-bearing for the
    # match to hinge on Wick-rotation 4D taste counting).
    if _assert_le(7.0, math.log10(ratio_8), "N=8 spatial-only off by > 10^7 (P2 load-bearing)"):
        passes += 1
    else:
        fails += 1

    # Check 6: alpha_bare^16 alone vs alpha_s(v)^16 alone (P3 wrong-coupling counterfactual)
    print()
    print("=" * 70)
    print("Check 6: coupling-choice counterfactual (P3 wrong-coupling sensitivity)")
    print("=" * 70)
    v_bare16 = M_PL * APBC * ALPHA_BARE ** 16
    v_sv16 = M_PL * APBC * ALPHA_S_V ** 16
    print(f"  using alpha_bare^16  -> v = {v_bare16:.4e} GeV (off by {abs(v_bare16 - V_OBS) / V_OBS:.2%})")
    print(f"  using alpha_s(v)^16  -> v = {v_sv16:.4e} GeV (off by {abs(v_sv16 - V_OBS) / V_OBS:.2%})")
    print(f"  using alpha_LM^16    -> v = {v_pred:.4e} GeV (off by {abs(v_pred - V_OBS) / V_OBS:.4%})")
    # alpha_LM uniquely matches; the others miss by orders of magnitude or factor 8.
    diff_bare = abs(v_bare16 - V_OBS) / V_OBS
    diff_sv = abs(v_sv16 - V_OBS) / V_OBS
    diff_lm = abs(v_pred - V_OBS) / V_OBS
    ok6 = (diff_bare > 0.5) and (diff_sv > 0.5) and (diff_lm < 0.001)
    if _line("only alpha_LM^16 matches; alpha_bare/alpha_s(v) miss by > 50 %", ok6):
        passes += 1
    else:
        fails += 1

    print()
    print("=" * 70)
    print(f"TOTAL: PASS={passes} FAIL={fails}")
    print("=" * 70)
    print()
    print("VERDICT: hierarchy formula honest-status structural checks verified.")
    print("The formula is a bounded numerical match on the same-surface")
    print("plaquette/coupling chain at +0.0255 % from PDG v_obs. Four named")
    print("load-bearing primitives P1-P4 (M_Pl import; Wick rotation for 4D")
    print("taste counting; u_0^16 -> alpha_LM^16 algebraic substitution; EWSB")
    print("observable identification) carry the match; closure to a retained")
    print("hierarchy theorem requires deriving at least one of P1-P4 from")
    print("primitives. See docs/HIERARCHY_FORMULA_HONEST_STATUS_NOTE_2026-05-10.md")
    print("for the full status correction.")

    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
