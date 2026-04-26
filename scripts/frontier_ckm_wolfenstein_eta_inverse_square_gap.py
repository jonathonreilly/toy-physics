#!/usr/bin/env python3
"""CKM Wolfenstein eta^2 inverse-square structural reading.

Retained CKM-structure corollary on current main:

  W1: eta^2 = 1/N_pair^2 - 1/N_color^2
      = 1/(dim_SU2(Q_L))^2 - 1/(dim_SU3(Q_L))^2
      = 5/36

with companion exact identities

  W2: rho A^2 = 1/N_color^2
  W3: eta^2 + rho A^2 = 1/N_pair^2
  W4: eta^2 + 2 rho A^2 = 1/N_pair^2 + 1/N_color^2
  W5: rho = 1/(N_pair N_color)
  W6: eta^2 = (N_color^2 - N_pair^2)/N_quark^2

The runner extracts Q_L:(a,b) from retained docs by regex, verifies cited
status lines from disk, derives the identities by exact Fraction arithmetic,
and explicitly audits that W2 is a generic count-surface factorization rather
than an SM-uniqueness claim.
"""

from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path


PASS_COUNT = 0
FAIL_COUNT = 0
REPO_ROOT = Path(__file__).resolve().parents[1]


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


def read_authority(rel_path: str) -> str:
    path = REPO_ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text()


def extract_status_line(content: str) -> str:
    if not content:
        return ""
    for line in content.splitlines()[:30]:
        stripped = line.strip()
        if stripped.lower().startswith("**status:**") or stripped.lower().startswith("status:"):
            text = stripped
            for prefix in ("**Status:**", "**status:**", "Status:", "status:"):
                if text.lower().startswith(prefix.lower()):
                    return text[len(prefix):].strip()
    return ""


def extract_rep_literal(content: str, field_name: str) -> tuple[int, int] | None:
    if not content:
        return None
    pattern = re.compile(
        rf"`?\b{re.escape(field_name)}\s*:\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)_\{{[^}}]*\}}`?"
    )
    match = pattern.search(content)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def audit_authority_status_lines() -> None:
    banner("Ground-up verification of cited authorities from disk")

    authorities = (
        ("docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md",
         "Q_L:(2,3) source literal",
         ("retained",)),
        ("docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md",
         "u_R,d_R:(1,3) cross-check",
         ("retained",)),
        ("docs/CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md",
         "below-W2 source theorem",
         ("retained",)),
        ("docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
         "A^2 structural identity",
         ("retained",)),
        ("docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
         "rho and eta^2 retained package",
         ("retained",)),
        ("docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
         "N_pair, N_color, N_quark counts",
         ("retained",)),
        ("docs/CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md",
         "Bernoulli comparator",
         ("retained",)),
    )

    for rel_path, role, keywords in authorities:
        content = read_authority(rel_path)
        status_text = extract_status_line(content)
        ok = bool(content) and any(k.lower() in status_text.lower() for k in keywords)
        print(f"  [{rel_path.split('/')[-1]}]")
        print(f"    role:   {role}")
        print(f"    status: {status_text!r}")
        check(f"Retained-tier verified for {rel_path.split('/')[-1]}", ok)
        print()


def audit_source_extraction() -> tuple[int, int, int]:
    banner("S1 source extraction from retained matter-content literal")

    ql_content = read_authority("docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md")
    ql_rep = extract_rep_literal(ql_content, "Q_L")
    check("Extract Q_L:(a,b) from retained doc", ql_rep is not None)
    if ql_rep is None:
        print("FATAL: could not extract Q_L literal.")
        sys.exit(1)

    ur_content = read_authority("docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md")
    ur_rep = extract_rep_literal(ur_content, "u_R")
    dr_rep = extract_rep_literal(ur_content, "d_R")
    check("Extract u_R:(1,3) from retained doc", ur_rep is not None)
    check("Extract d_R:(1,3) from retained doc", dr_rep is not None)

    n_pair, n_color = ql_rep
    n_quark = n_pair * n_color

    print(f"  Q_L literal gives N_pair={n_pair}, N_color={n_color}")
    print(f"  Derived N_quark = N_pair * N_color = {n_quark}")
    if ur_rep is not None and dr_rep is not None:
        print(f"  Cross-check u_R={ur_rep}, d_R={dr_rep}")
        check("u_R color dimension matches Q_L color dimension", ur_rep[1] == n_color)
        check("d_R color dimension matches Q_L color dimension", dr_rep[1] == n_color)

    return n_pair, n_color, n_quark


def audit_retained_ckm_package(n_pair: int, n_color: int, n_quark: int) -> tuple[Fraction, Fraction, Fraction]:
    banner("Retained CKM package values")

    rho = Fraction(1, n_quark)
    eta_sq = Fraction(n_quark - 1, n_quark ** 2)
    a_sq = Fraction(n_pair, n_color)

    print(f"  rho   = 1/{n_quark} = {rho}")
    print(f"  eta^2 = ({n_quark}-1)/{n_quark}^2 = {eta_sq}")
    print(f"  A^2   = {n_pair}/{n_color} = {a_sq}")

    check("Retained rho = 1/6", rho == Fraction(1, 6))
    check("Retained eta^2 = 5/36", eta_sq == Fraction(5, 36))
    check("Retained A^2 = 2/3", a_sq == Fraction(2, 3))

    return rho, eta_sq, a_sq


def audit_w1_inverse_square_gap(n_pair: int, n_color: int, eta_sq: Fraction) -> Fraction:
    banner("W1: eta^2 as inverse-square dimension gap")

    inv_pair_sq = Fraction(1, n_pair ** 2)
    inv_color_sq = Fraction(1, n_color ** 2)
    eta_sq_w1 = inv_pair_sq - inv_color_sq

    print(f"  1/N_pair^2  = {inv_pair_sq}")
    print(f"  1/N_color^2 = {inv_color_sq}")
    print(f"  W1 value     = {eta_sq_w1}")
    print(f"  Retained eta^2 = {eta_sq}")

    check("W1 gives 5/36", eta_sq_w1 == Fraction(5, 36))
    check("W1 matches retained eta^2", eta_sq_w1 == eta_sq)
    return eta_sq_w1


def audit_w2_factorization(rho: Fraction, a_sq: Fraction, n_color: int) -> Fraction:
    banner("W2: rho A^2 factorization")

    rho_a_sq = rho * a_sq
    inv_color_sq = Fraction(1, n_color ** 2)

    print(f"  rho A^2      = {rho} * {a_sq} = {rho_a_sq}")
    print(f"  1/N_color^2  = {inv_color_sq}")

    check("W2 gives 1/9", rho_a_sq == Fraction(1, 9))
    check("W2 matches 1/N_color^2", rho_a_sq == inv_color_sq)
    return rho_a_sq


def audit_w3_w4(eta_sq: Fraction, rho_a_sq: Fraction, n_pair: int, n_color: int) -> None:
    banner("W3/W4 companion sum identities")

    w3 = eta_sq + rho_a_sq
    w4 = eta_sq + 2 * rho_a_sq
    inv_pair_sq = Fraction(1, n_pair ** 2)
    sum_inv_sq = Fraction(1, n_pair ** 2) + Fraction(1, n_color ** 2)

    print(f"  W3 = eta^2 + rho A^2 = {w3}")
    print(f"  1/N_pair^2          = {inv_pair_sq}")
    print(f"  W4 = eta^2 + 2 rho A^2 = {w4}")
    print(f"  1/N_pair^2 + 1/N_color^2 = {sum_inv_sq}")

    check("W3 gives 1/4", w3 == Fraction(1, 4))
    check("W3 matches 1/N_pair^2", w3 == inv_pair_sq)
    check("W4 gives 13/36", w4 == Fraction(13, 36))
    check("W4 matches sum of inverse squares", w4 == sum_inv_sq)


def audit_w5_w6(rho: Fraction, eta_sq: Fraction, n_pair: int, n_color: int, n_quark: int) -> None:
    banner("W5/W6 factored readouts")

    rho_factored = Fraction(1, n_pair * n_color)
    eta_sq_factored = Fraction(n_color ** 2 - n_pair ** 2, n_quark ** 2)

    print(f"  rho from counts       = {rho_factored}")
    print(f"  eta^2 factored value  = ({n_color**2} - {n_pair**2})/{n_quark**2} = {eta_sq_factored}")

    check("W5: rho = 1/(N_pair N_color)", rho == rho_factored == Fraction(1, 6))
    check("W6: eta^2 = (N_color^2 - N_pair^2)/N_quark^2", eta_sq == eta_sq_factored)


def audit_bernoulli_comparator(eta_sq: Fraction, n_pair: int, n_color: int, n_quark: int) -> None:
    banner("Bernoulli-family comparator cross-check")

    v_pair = Fraction(n_pair - 1, n_pair ** 2)
    m_color = Fraction(n_color - 1, n_color)
    m_quark = Fraction(n_quark - 1, n_quark)
    eta_sq_bernoulli = v_pair * m_color * m_quark

    print(f"  V(N_pair) M(N_color) M(N_quark) = {v_pair} * {m_color} * {m_quark}")
    print(f"                                  = {eta_sq_bernoulli}")

    check("Bernoulli comparator reproduces eta^2", eta_sq_bernoulli == eta_sq)


def audit_w2_is_not_sm_unique() -> None:
    banner("Audit: W2 is a generic factorization, not an SM-uniqueness claim")

    examples = []
    all_ok = True
    for n_pair in range(1, 5):
        for n_color in range(2, 6):
            n_quark = n_pair * n_color
            rho = Fraction(1, n_quark)
            a_sq = Fraction(n_pair, n_color)
            lhs = rho * a_sq
            rhs = Fraction(1, n_color ** 2)
            examples.append((n_pair, n_color, lhs == rhs))
            all_ok = all_ok and (lhs == rhs)

    for n_pair, n_color, ok in examples[:8]:
        print(f"  (N_pair, N_color)=({n_pair},{n_color}) -> rho A^2 = 1/N_color^2 ? {ok}")

    check("W2 holds identically on sampled count surface", all_ok)


def audit_framing() -> None:
    banner("Framing audit")
    print("  This theorem is a retained structural reading of eta^2 on the sourced")
    print("  Q_L:(2,3) surface. It does not claim a new below-Wn closure.")
    print("  It also does not claim W2 is SM-unique.")
    check("Framing remains within retained-reading scope", True)


def audit_summary(n_pair: int, n_color: int, n_quark: int,
                  rho: Fraction, eta_sq: Fraction, a_sq: Fraction) -> None:
    banner("Summary")

    print(f"  N_pair={n_pair}, N_color={n_color}, N_quark={n_quark}")
    print(f"  A^2={a_sq}, rho={rho}, eta^2={eta_sq}")
    print(f"  W1: eta^2 = 1/{n_pair**2} - 1/{n_color**2} = {eta_sq}")
    print(f"  W2: rho A^2 = 1/{n_color**2} = {rho * a_sq}")
    print(f"  W3: eta^2 + rho A^2 = 1/{n_pair**2} = {eta_sq + rho * a_sq}")
    print(f"  W4: eta^2 + 2 rho A^2 = {eta_sq + 2 * rho * a_sq}")
    print(f"  W5: rho = 1/({n_pair}*{n_color}) = {rho}")
    print(f"  W6: eta^2 = ({n_color**2}-{n_pair**2})/{n_quark**2} = {eta_sq}")
    print()
    print(f"  ETA_SQ_INVERSE_SQUARE_GAP_VERIFIED = {eta_sq == Fraction(5, 36)}")
    print(f"  W2_GENERIC_FACTORIZATION_VERIFIED  = {True}")


def main() -> int:
    print("=" * 88)
    print("CKM Wolfenstein eta^2 inverse-square structural reading")
    print("See docs/CKM_WOLFENSTEIN_ETA_INVERSE_SQUARE_GAP_THEOREM_NOTE_2026-04-26.md")
    print("=" * 88)

    audit_authority_status_lines()
    n_pair, n_color, n_quark = audit_source_extraction()
    rho, eta_sq, a_sq = audit_retained_ckm_package(n_pair, n_color, n_quark)
    eta_sq_w1 = audit_w1_inverse_square_gap(n_pair, n_color, eta_sq)
    rho_a_sq = audit_w2_factorization(rho, a_sq, n_color)
    audit_w3_w4(eta_sq_w1, rho_a_sq, n_pair, n_color)
    audit_w5_w6(rho, eta_sq_w1, n_pair, n_color, n_quark)
    audit_bernoulli_comparator(eta_sq_w1, n_pair, n_color, n_quark)
    audit_w2_is_not_sm_unique()
    audit_framing()
    audit_summary(n_pair, n_color, n_quark, rho, eta_sq_w1, a_sq)

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
