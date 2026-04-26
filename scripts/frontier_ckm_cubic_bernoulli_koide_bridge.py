#!/usr/bin/env python3
"""Cubic Bernoulli W(N) and triple-level factorization Koide-bridge support audit.

Verifies the new identities in
  docs/CKM_CUBIC_BERNOULLI_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md

Bernoulli tower M^(k)(N) = (N-1)/N^k for k in {0, 1, 2, 3} and N in {N_pair, N_color, N_quark}:

  W1: W(N_pair) = (N_pair - 1)/N_pair^3 = 1/8       [framework-native]
  W2: W(N_color) = 2/27                              [NEW]
  W3: W(N_quark) = 5/216                             [NEW]

  C1: Universal cubic relation W(N) = V(N)/N = M(N)/N^2

Triple-level factorizations (NEW):
  T1: eta^2 = V(N_pair) * M(N_color) * M(N_quark)    [TRIPLE-level]
  T2: M1 = V(N_pair) * M(N_color)^2 = V(N_pair) * A^4

Cubic identities (NEW):
  C2: rho * eta^2 = W(N_quark) = 5/216
  C3: rho * V(N_color) = 1/N_color^3 = 1/27

Cross-sector reading (SUPPORT, NOT closure, not counted as proof checks):
  CS: cos^6(theta_K) = 1/8 = W(N_pair) [NEW Koide-cubic reading]

ALL INPUTS RETAINED on current main:
- W2 A^2 = N_pair/N_color = M(N_color)
- rho = 1/N_quark, eta^2 = (N_quark-1)/N_quark^2 = V(N_quark) (Thales)
- N_pair=2, N_color=3, N_quark=6
- M(N_quark) = 1 - rho = (N_quark-1)/N_quark

NO SUPPORT-tier or open inputs used as DERIVATION inputs. Cross-sector reading
is commentary only.

Uses Python's fractions.Fraction for exact-rational arithmetic.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Retained framework structural integers
N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR  # = 6

# Retained closed forms
A_SQ = Fraction(N_PAIR, N_COLOR)              # W2: 2/3
RHO = Fraction(1, N_QUARK)                    # CP: 1/6
ETA_SQ = Fraction(N_QUARK - 1, N_QUARK ** 2)  # 5/36


def M(N: int) -> Fraction:
    """Bernoulli mean (k=1)."""
    return Fraction(N - 1, N)


def V(N: int) -> Fraction:
    """Bernoulli variance (k=2)."""
    return Fraction(N - 1, N ** 2)


def W(N: int) -> Fraction:
    """Bernoulli cube (k=3) — NEW level."""
    return Fraction(N - 1, N ** 3)


def audit_inputs() -> None:
    banner("Retained inputs on current main")

    print(f"  N_pair = {N_PAIR}, N_color = {N_COLOR}, N_quark = {N_QUARK}")
    print(f"  A^2 = N_pair/N_color = {A_SQ} (W2)")
    print(f"  rho = 1/N_quark      = {RHO}")
    print(f"  eta^2 = rho(1-rho)   = {ETA_SQ} (Thales)")

    check("N_pair = 2", N_PAIR == 2)
    check("N_color = 3", N_COLOR == 3)
    check("N_quark = 6", N_QUARK == 6)
    check("A^2 = 2/3 (W2)", A_SQ == Fraction(2, 3))
    check("rho = 1/6 (CP)", RHO == Fraction(1, 6))
    check("eta^2 = 5/36 (Thales)", ETA_SQ == Fraction(5, 36))

    repo_root = Path(__file__).resolve().parents[1]
    upstream_retained = (
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
    )
    for rel in upstream_retained:
        path = repo_root / rel
        check(f"retained on main: {rel}", path.exists())


def audit_4x3_bernoulli_tower() -> None:
    banner("4x3 Bernoulli tower: M^(k)(N) = (N-1)/N^k for k in {0,1,2,3}, N in {2,3,6}")

    print("            | k = 0  | k = 1     | k = 2      | k = 3")
    for N, name in [(N_PAIR, "N_pair  "), (N_COLOR, "N_color "), (N_QUARK, "N_quark ")]:
        deficit = N - 1
        m_val = M(N)
        v_val = V(N)
        w_val = W(N)
        print(f"  {name}={N} | {deficit:6d} | {str(m_val):10s}| {str(v_val):11s}| {w_val}")

    print()
    print("  NEW k=3 cubic Bernoulli W(N) = (N-1)/N^3:")
    print(f"    W(N_pair)  = 1/8   = 1/N_pair^3            [framework-native]")
    print(f"    W(N_color) = 2/27  = (N_color-1)/N_color^3 [NEW]")
    print(f"    W(N_quark) = 5/216 = (N_quark-1)/N_quark^3 [NEW]")

    check("W(N_pair) = 1/8", W(N_PAIR) == Fraction(1, 8))
    check("W(N_color) = 2/27 [NEW]", W(N_COLOR) == Fraction(2, 27))
    check("W(N_quark) = 5/216 [NEW]", W(N_QUARK) == Fraction(5, 216))


def audit_c1_universal_cubic_relation() -> None:
    banner("(C1) Universal cubic relation: W(N) = V(N)/N = M(N)/N^2 at all three N")

    print("  W(N) = V(N)/N = M(N)/N^2 for N in {N_pair, N_color, N_quark}:")
    for N, name in [(N_PAIR, "N_pair"), (N_COLOR, "N_color"), (N_QUARK, "N_quark")]:
        w = W(N)
        v_over_n = V(N) / N
        m_over_n_sq = M(N) / (N ** 2)
        ok_v = w == v_over_n
        ok_m = w == m_over_n_sq
        print(f"    W({name})    = {w}")
        print(f"    V({name})/{name} = {v_over_n}  (= W? {ok_v})")
        print(f"    M({name})/{name}^2 = {m_over_n_sq}  (= W? {ok_m})")
        check(f"(C1) W({name}) = V({name})/{name}", ok_v)
        check(f"(C1) W({name}) = M({name})/{name}^2", ok_m)


def audit_t1_triple_level_eta_sq() -> None:
    banner("(T1) NEW: eta^2 = V(N_pair) * M(N_color) * M(N_quark) [TRIPLE-level]")

    triple = V(N_PAIR) * M(N_COLOR) * M(N_QUARK)

    print(f"  V(N_pair)  = (N_pair  - 1)/N_pair^2  = {V(N_PAIR)}")
    print(f"  M(N_color) = (N_color - 1)/N_color   = {M(N_COLOR)}  [= A^2]")
    print(f"  M(N_quark) = (N_quark - 1)/N_quark   = {M(N_QUARK)}  [= 1 - rho]")
    print(f"  Product V(N_pair)*M(N_color)*M(N_quark) = {triple}")
    print(f"  eta^2 retained                            = {ETA_SQ}")

    check("(T1) eta^2 = V(N_pair) * M(N_color) * M(N_quark) EXACTLY",
          triple == ETA_SQ)


def audit_t2_alt_m1_decomposition() -> None:
    banner("(T2) NEW alternate decomposition: M1 = V(N_pair) * A^4")

    M1 = RHO * A_SQ
    T2 = V(N_PAIR) * (A_SQ ** 2)

    print(f"  M1 = rho * A^2                    = {M1}")
    print(f"  V(N_pair) * A^4                    = {V(N_PAIR)} * {A_SQ ** 2} = {T2}")
    print(f"  (= V(N_pair) * M(N_color)^2)")

    check("(T2) M1 = V(N_pair) * A^4 EXACTLY", T2 == M1)
    check("(T2) Equivalent: M1 = V(N_pair) * M(N_color)^2",
          T2 == V(N_PAIR) * M(N_COLOR) ** 2)


def audit_c2_rho_eta_sq_w_quark() -> None:
    banner("(C2) NEW: rho * eta^2 = W(N_quark) = 5/216")

    product = RHO * ETA_SQ
    expected = W(N_QUARK)

    print(f"  rho * eta^2                        = {RHO} * {ETA_SQ} = {product}")
    print(f"  W(N_quark) = (N_quark - 1)/N_quark^3 = {expected}")
    print(f"  In structural integers: rho * eta^2 = (N_quark - 1)/N_quark^3 EXACTLY")

    check("(C2) rho * eta^2 = W(N_quark) = 5/216", product == expected)


def audit_c3_rho_v_color_cubic() -> None:
    banner("(C3) NEW: rho * V(N_color) = 1/N_color^3 = 1/27")

    product = RHO * V(N_COLOR)
    expected = Fraction(1, N_COLOR ** 3)

    print(f"  rho * V(N_color)              = {RHO} * {V(N_COLOR)} = {product}")
    print(f"  1/N_color^3                    = {expected}")
    print(f"  Identity uses N_pair = N_color - 1 (framework primitive)")

    check("(C3) rho * V(N_color) = 1/N_color^3 EXACTLY", product == expected)

    # C4: equivalent reading M1/N_color = 1/N_color^3
    M1 = RHO * A_SQ
    M1_over_N_color = M1 / N_COLOR
    print(f"\n  (C4 equivalent): M1/N_color = {M1} / {N_COLOR} = {M1_over_N_color}")
    check("(C4) M1/N_color = 1/N_color^3 (equivalent to C3)",
          M1_over_N_color == expected)


def audit_cross_sector_cubic() -> None:
    banner("Cross-sector reading (SUPPORT, NOT closure; printed only)")

    cos_sq_conj = Fraction(1, 2)
    cos_4_conj = cos_sq_conj ** 2
    cos_6_conj = cos_sq_conj ** 3

    print("  Under conjectural Q_l = A^2 = 2/3 and a separate Koide-angle premise,")
    print("  cos^2(theta_K) = 1/(3 Q_l) = 1/2. The equalities below are conditional")
    print("  target-class matches, not retained CKM proof obligations:")
    print()
    print(f"    cos^2(theta_K) = {cos_sq_conj} = M(N_pair) = {M(N_PAIR)}  [conjectural]")
    print(f"    cos^4(theta_K) = {cos_4_conj} = V(N_pair) = {V(N_PAIR)}  [conditional]")
    print(f"    cos^6(theta_K) = {cos_6_conj} = W(N_pair) = {W(N_PAIR)}  [NEW Koide-cubic reading]")
    print()
    print("  Five Koide-relevant ratios with framework counterparts (across k=1,2,3 and N_pair, N_color):")
    print(f"    M(N_color) = Q_l = 2/3            [k=1]")
    print(f"    V(N_color) = Koide variance = 2/9 [k=2]")
    print(f"    M(N_pair)  = cos^2(theta_K) = 1/2  [k=1]")
    print(f"    V(N_pair)  = cos^4(theta_K) = 1/4  [k=2]")
    print(f"    W(N_pair)  = cos^6(theta_K) = 1/8  [k=3 NEW]")

    print()
    print("  These lines are deliberately not counted as PASS conditions because")
    print("  this runner does not prove Koide, cos^2(theta_K), or a structural Koide mechanism.")


def audit_summary() -> None:
    banner("Summary of new content")

    print("  NEW (W1-W3):  Cubic Bernoulli W(N) = (N-1)/N^3 at three N-levels.")
    print("                W(N_pair) = 1/8, W(N_color) = 2/27, W(N_quark) = 5/216")
    print()
    print("  NEW (C1):     Universal cubic relation W(N) = V(N)/N = M(N)/N^2.")
    print()
    print("  NEW (T1):     TRIPLE-level factorization of eta^2:")
    print("                eta^2 = V(N_pair) * M(N_color) * M(N_quark) = 5/36 EXACTLY")
    print()
    print("  NEW (T2):     Alternate M1 decomposition: M1 = V(N_pair) * A^4 = 1/9")
    print()
    print("  NEW (C2):     rho * eta^2 = W(N_quark) = 5/216")
    print("                Retained-product factorization through cubic level.")
    print()
    print("  NEW (C3):     rho * V(N_color) = 1/N_color^3 = 1/27")
    print("                Pure cubic structural identity (uses N_pair = N_color - 1).")
    print()
    print("  NEW (CS):     cos^6(theta_K) = 1/8 = W(N_pair) [conditional support reading]")
    print()
    print("  Complete 4x3 Bernoulli tower (12 elements) derivable from retained inputs.")
    print("  Conditional Koide-relevant target matches are printed but not counted.")
    print()
    print("  Does NOT close Koide 2/9, cos^2(theta_K),")
    print("  or any structural Koide mechanism beyond retained N_gen = N_color = 3.")
    print("  All counted checks use retained CKM inputs only; no open inputs are used.")


def main() -> int:
    print("=" * 88)
    print("Cubic Bernoulli W(N) and triple-level factorization Koide-bridge support audit")
    print("See docs/CKM_CUBIC_BERNOULLI_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_4x3_bernoulli_tower()
    audit_c1_universal_cubic_relation()
    audit_t1_triple_level_eta_sq()
    audit_t2_alt_m1_decomposition()
    audit_c2_rho_eta_sq_w_quark()
    audit_c3_rho_v_color_cubic()
    audit_cross_sector_cubic()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
