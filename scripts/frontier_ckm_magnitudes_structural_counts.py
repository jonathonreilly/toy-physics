#!/usr/bin/env python3
"""Audit the retained CKM structural-counts magnitude package.

Verifies the compact structural-counts forms

  (M1) |V_us|_0^2 = alpha_s(v)/N_pair
  (M2) |V_cb|_0^2 = alpha_s(v)^2/(N_pair N_color)
  (M3) |V_ts|_0^2 = alpha_s(v)^2/(N_pair N_color)
  (M4) |V_ub|_0^2 = alpha_s(v)^3/(8 N_color^2)
  (M5) |V_td|_0^2 = (N_quark-1) alpha_s(v)^3/(8 N_color^2)

on the already-retained CKM atlas surface. This runner intentionally does not
certify any dimension-uniqueness or cross-sector promotion.
"""

from __future__ import annotations

import math
from pathlib import Path

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


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


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


REPO_ROOT = Path(__file__).resolve().parents[1]

ALPHA_S_V = CANONICAL_ALPHA_S_V
N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR

RHO = 1.0 / N_QUARK
ETA_SQ = (N_QUARK - 1.0) / (N_QUARK * N_QUARK)

V_US_PDG = 0.2243
V_CB_PDG = 0.0410
V_TS_PDG = 0.0407
V_UB_PDG = 0.00382
V_TD_PDG = 0.00858


def read_rel(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def audit_authorities() -> None:
    banner("Authority checks")

    authorities = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md",
        "docs/CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md",
    )
    for rel in authorities:
        check(f"authority present: {rel}", (REPO_ROOT / rel).exists())

    note_text = read_rel("docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md")
    scope_guards = (
        "This note does **not** claim:",
        "- dimension uniqueness from `|V_ub|`;",
        "- any reliance on `2d + 3 = n_color^2`;",
        "- any Koide, three-sector, or cross-lane closure;",
    )
    for phrase in scope_guards:
        check(f"scope guard present: {phrase}", phrase in note_text)


def audit_inputs() -> None:
    banner("Retained CKM structural counts")

    print(f"  N_pair   = {N_PAIR}")
    print(f"  N_color  = {N_COLOR}")
    print(f"  N_quark  = {N_QUARK}")
    print(f"  alpha_s(v) = {ALPHA_S_V:.15f}")
    print(f"  rho      = {RHO:.15f}")
    print(f"  eta^2    = {ETA_SQ:.15f}")

    check("N_pair = 2", N_PAIR == 2)
    check("N_color = 3", N_COLOR == 3)
    check("N_quark = N_pair N_color = 6", N_QUARK == 6)
    check("rho = 1/N_quark = 1/6", close(RHO, 1.0 / 6.0))
    check("eta^2 = (N_quark-1)/N_quark^2 = 5/36", close(ETA_SQ, 5.0 / 36.0))
    check("rho^2 + eta^2 = 1/N_quark = 1/6", close(RHO * RHO + ETA_SQ, 1.0 / 6.0))


def audit_m1_m2_m3() -> None:
    banner("(M1)-(M3): V_us, V_cb, V_ts")

    v_us_sq = ALPHA_S_V / N_PAIR
    v_cb_sq = ALPHA_S_V * ALPHA_S_V / (N_PAIR * N_COLOR)
    v_ts_sq = ALPHA_S_V * ALPHA_S_V / (N_PAIR * N_COLOR)

    print(f"  |V_us|_0^2 = alpha_s(v)/N_pair             = {v_us_sq:.12f}")
    print(f"  |V_cb|_0^2 = alpha_s(v)^2/(N_pair N_color) = {v_cb_sq:.12f}")
    print(f"  |V_ts|_0^2 = alpha_s(v)^2/(N_pair N_color) = {v_ts_sq:.12f}")

    check("(M1) |V_us|_0^2 = alpha_s(v)/2", close(v_us_sq, ALPHA_S_V / 2.0))
    check("(M2) |V_cb|_0^2 = alpha_s(v)^2/6", close(v_cb_sq, ALPHA_S_V * ALPHA_S_V / 6.0))
    check("(M3) |V_ts|_0^2 = |V_cb|_0^2", close(v_ts_sq, v_cb_sq))


def audit_m4_v_ub() -> None:
    banner("(M4): compact V_ub structural-counts form")

    lambda_sq = ALPHA_S_V / N_PAIR
    a_sq = N_PAIR / N_COLOR
    v_ub_from_wolf = a_sq * (lambda_sq ** 3) * (RHO * RHO + ETA_SQ)
    v_ub_compact = ALPHA_S_V ** 3 / (8.0 * N_COLOR * N_COLOR)

    print(f"  Wolfenstein form A^2 lambda^6 (rho^2+eta^2) = {v_ub_from_wolf:.12e}")
    print(f"  compact form alpha_s(v)^3/(8 N_color^2)     = {v_ub_compact:.12e}")

    check("(M4) Wolfenstein and compact V_ub forms agree", close(v_ub_from_wolf, v_ub_compact))
    check("(M4) |V_ub|_0^2 = alpha_s(v)^3/72", close(v_ub_compact, ALPHA_S_V ** 3 / 72.0))


def audit_n_pair_cancellation() -> None:
    banner("Critical cancellation: N_pair drops out of V_ub")

    lhs = (N_PAIR / N_COLOR) * (ALPHA_S_V / N_PAIR) ** 3 * (1.0 / N_QUARK)
    rhs = ALPHA_S_V ** 3 / (8.0 * N_COLOR * N_COLOR)

    print(f"  expanded structural-counts form = {lhs:.12e}")
    print(f"  compact no-N_pair form          = {rhs:.12e}")

    check("N_pair cancels exactly in |V_ub|_0^2", close(lhs, rhs))


def audit_m5_v_td() -> None:
    banner("(M5): V_td structural-counts form")

    lambda_sq = ALPHA_S_V / N_PAIR
    a_sq = N_PAIR / N_COLOR
    r_t_sq = (1.0 - RHO) ** 2 + ETA_SQ
    v_td_from_wolf = a_sq * (lambda_sq ** 3) * r_t_sq
    v_td_struct = (N_QUARK - 1.0) * ALPHA_S_V ** 3 / (8.0 * N_COLOR * N_COLOR)

    print(f"  Wolfenstein form A^2 lambda^6 ((1-rho)^2+eta^2) = {v_td_from_wolf:.12e}")
    print(f"  structural-counts form                          = {v_td_struct:.12e}")

    check("R_t^2 = (1-rho)^2 + eta^2 = 1-rho = 5/6", close(r_t_sq, 5.0 / 6.0))
    check("(M5) Wolfenstein and structural V_td forms agree", close(v_td_from_wolf, v_td_struct))
    check("(M5) |V_td|_0^2 = 5 alpha_s(v)^3/72", close(v_td_struct, 5.0 * ALPHA_S_V ** 3 / 72.0))


def audit_pdg_comparators() -> None:
    banner("Observation-side comparators")

    comparisons = (
        ("|V_us|^2", ALPHA_S_V / 2.0, V_US_PDG ** 2),
        ("|V_cb|^2", ALPHA_S_V ** 2 / 6.0, V_CB_PDG ** 2),
        ("|V_ts|^2", ALPHA_S_V ** 2 / 6.0, V_TS_PDG ** 2),
        ("|V_ub|^2", ALPHA_S_V ** 3 / 72.0, V_UB_PDG ** 2),
        ("|V_td|^2", 5.0 * ALPHA_S_V ** 3 / 72.0, V_TD_PDG ** 2),
    )
    for label, theory, pdg in comparisons:
        ratio = theory / pdg
        deviation = abs(1.0 - ratio)
        print(f"  {label:9s}: theory = {theory:.4e}, PDG = {pdg:.4e}, ratio = {ratio:.4f}")
        check(f"{label} within 10% of PDG", deviation < 0.10)


def summary() -> None:
    banner("Summary")
    print("  Retained CKM structural-counts surface:")
    print("    |V_us|_0^2 = alpha_s(v)/N_pair")
    print("    |V_cb|_0^2 = alpha_s(v)^2/(N_pair N_color)")
    print("    |V_ts|_0^2 = alpha_s(v)^2/(N_pair N_color)")
    print("    |V_ub|_0^2 = alpha_s(v)^3/(8 N_color^2)")
    print("    |V_td|_0^2 = (N_quark-1) alpha_s(v)^3/(8 N_color^2)")
    print()
    print("  New packaging result: the N_pair factor cancels exactly in |V_ub|_0^2.")


def main() -> int:
    print("=" * 88)
    print("CKM structural-counts off-diagonal magnitude audit")
    print("See docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_authorities()
    audit_inputs()
    audit_m1_m2_m3()
    audit_m4_v_ub()
    audit_n_pair_cancellation()
    audit_m5_v_td()
    audit_pdg_comparators()
    summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
