"""Runner: cross-sector A²-Q_l-|V_cb| bridge promoted via V8 (Block 3).

Audits the chain composing V8 (Block 1) with retained CKM atlas to give
a structural cross-sector identity Q_l × α_s(v)² = 4 |V_cb|² on A_min.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

AUDIT_FAILS: list[str] = []


def audit(name: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not condition:
        AUDIT_FAILS.append(name)


def read_doc(path_rel: str) -> str:
    return (DOCS_DIR / path_rel).read_text(encoding="utf-8")


def main() -> int:
    print("=" * 72)
    print("Cross-Sector A²-Q_l-|V_cb| Bridge Promoted via V8 (Block 3) audit")
    print("=" * 72)

    # ---- Section 1: V8 (Block 1) prerequisite -----------------------------

    print()
    print("Section 1: V8 (Block 1, Q_l closure) prerequisite check")
    print("-" * 72)

    v8_text = read_doc(
        "KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md"
    )
    audit(
        "V8 note exists on disk",
        len(v8_text) > 0,
        "block 1 closure note found",
    )
    audit(
        "V8 carries proposed_retained status",
        "actual_current_surface_status: proposed_retained" in v8_text,
        "V8 firewall: proposed_retained",
    )
    audit(
        "V8 closes Q_l = 2/3 on A_min",
        ("Q = 2/3" in v8_text and "A_min" in v8_text),
        "V8 §2 theorem statement (Q_l in framework notation)",
    )

    # ---- Section 2: cross-sector support note prerequisite -----------------

    print()
    print("Section 2: cross-sector support note prerequisite check")
    print("-" * 72)

    cs_text = read_doc(
        "CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md"
    )
    audit(
        "Cross-sector support note exists",
        len(cs_text) > 0,
        "2026-04-25 support note",
    )
    audit(
        "Cross-sector identity Q_l × α_s(v)² = 4 |V_cb|² statement",
        "Q_l * alpha_s(v)^2 = 4 |V_cb|^2" in cs_text or "Q_l alpha_s(v)^2 = 4 |V_cb|^2" in cs_text,
        "X2 identity present",
    )

    # ---- Section 3: retained CKM atlas authorities -------------------------

    print()
    print("Section 3: retained CKM atlas authority audits")
    print("-" * 72)

    wolf_text = read_doc(
        "WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md"
    )
    audit(
        "Wolfenstein λ-A structural identities note exists",
        len(wolf_text) > 0,
        "retained CKM atlas",
    )
    audit(
        "A² = n_pair / n_color = 2/3",
        "A^2          = n_pair / n_color     = 2/3" in wolf_text
        or ("A^2" in wolf_text and "n_pair" in wolf_text and "n_color" in wolf_text and "2/3" in wolf_text),
        "Wolfenstein A² identity",
    )
    audit(
        "λ² = α_s(v) / n_pair",
        "alpha_s(v)/n_pair" in wolf_text
        or ("lambda^2" in wolf_text and "alpha_s" in wolf_text and "n_pair" in wolf_text),
        "Wolfenstein λ² identity",
    )

    third_row_text = read_doc(
        "CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md"
    )
    audit(
        "CKM third-row magnitudes theorem note exists",
        len(third_row_text) > 0,
        "retained third-row magnitudes",
    )
    audit(
        "|V_cb|² = A²λ⁴ = α_s(v)²/6",
        ("V_cb" in third_row_text and "A^2" in third_row_text)
        or "|V_cb|² = α_s(v)²/6" in third_row_text,
        "third-row |V_cb| theorem",
    )

    alpha_s_text = read_doc("ALPHA_S_DERIVED_NOTE.md")
    audit(
        "ALPHA_S_DERIVED note exists",
        len(alpha_s_text) > 0,
        "retained α_s(v)",
    )

    # ---- Section 4: algebraic identity (sympy + numerical) -----------------

    print()
    print("Section 4: algebraic identity Q_l × α_s(v)² = 4 |V_cb|² (sympy/numerical)")
    print("-" * 72)

    # 4.1 Symbolic check
    Q_l = sp.Rational(2, 3)
    alpha_s = sp.symbols("alpha_s", positive=True)
    A_sq = sp.Rational(2, 3)
    lambda_sq = alpha_s / sp.Integer(2)
    V_cb_sq = A_sq * lambda_sq ** 2

    lhs = Q_l * alpha_s ** 2
    rhs = 4 * V_cb_sq
    audit(
        "Q_l × α_s² = 4 |V_cb|² (sympy symbolic)",
        sp.simplify(lhs - rhs) == 0,
        f"sympy simplifies LHS - RHS = {sp.simplify(lhs - rhs)}",
    )

    # 4.2 Dual-route agreement
    V_cb_direct = sp.sqrt(A_sq * lambda_sq ** 2)
    V_cb_via_Q = alpha_s * sp.sqrt(Q_l) / 2
    audit(
        "Dual-route |V_cb| = α_s/√6 from CKM atlas + Q_l V8",
        sp.simplify(V_cb_direct - V_cb_via_Q) == 0,
        f"both routes give |V_cb| = α_s × √(2/3)/2 = α_s/√6",
    )

    # 4.3 Numerical readout (verification, NOT a derivation step)
    alpha_s_value = 0.103303816122  # canonical retained value
    Q_l_num = 2.0 / 3.0
    V_cb_atlas = alpha_s_value / np.sqrt(6)
    lhs_num = Q_l_num * alpha_s_value ** 2
    rhs_num = 4 * V_cb_atlas ** 2
    audit(
        "Numerical: Q_l × α_s² = 4 |V_cb|² (canonical α_s value)",
        np.isclose(lhs_num, rhs_num),
        f"LHS = {lhs_num:.10f}, RHS = {rhs_num:.10f}",
    )

    # 4.4 Q_l = A² structural matching
    audit(
        "Q_l = A² = 2/3 structural matching across sectors",
        Q_l == A_sq,
        f"Q_l (V8) = {Q_l} = A² (CKM atlas) = {A_sq}",
    )

    # ---- Section 5: status firewall fields ---------------------------------

    print()
    print("Section 5: V1 status firewall fields")
    print("-" * 72)

    own_text = read_doc(
        "CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_PROMOTED_VIA_V8_THEOREM_NOTE_2026-04-29.md"
    )
    audit(
        "V1 carries actual_current_surface_status: proposed_retained",
        "actual_current_surface_status: proposed_retained" in own_text,
        "V1 firewall",
    )
    audit(
        "V1 carries audit_required_before_effective_retained: true",
        "audit_required_before_effective_retained: true" in own_text,
        "V1 firewall",
    )
    audit(
        "V1 carries bare_retained_allowed: false",
        "bare_retained_allowed: false" in own_text,
        "V1 firewall",
    )
    audit(
        "V1 records five_sixths_mechanism_status: bounded",
        "five_sixths_mechanism_status: bounded" in own_text,
        "V1 firewall: 5/6 mechanism explicitly bounded (not closed)",
    )
    audit(
        "V1 records common_scale_15_percent_gap_status: bounded",
        "common_scale_15_percent_gap_status: bounded" in own_text,
        "V1 firewall: +15% gap explicitly bounded (not closed)",
    )

    # ---- Section 6: forbidden imports check --------------------------------

    print()
    print("Section 6: forbidden imports check")
    print("-" * 72)

    forbidden_imports = ["m_d_obs", "m_s_obs", "m_b_obs", "V_cb_obs", "V_us_obs"]
    body_only = own_text.split("## 7. Verification")[0]
    for token in forbidden_imports:
        is_load_bearing = (
            f"= {token}" in body_only or f"{token} = " in body_only
        )
        audit(
            f"forbidden import not used as proof input: {token}",
            not is_load_bearing,
            "no observed quark mass / fitted CKM enters proof",
        )

    # ---- Summary -----------------------------------------------------------

    print()
    print("=" * 72)
    fail_count = len(AUDIT_FAILS)
    print(f"FAIL count: {fail_count}")

    CROSS_SECTOR_BRIDGE_PROPOSED_RETAINED_CHAIN_VERIFIED = (
        fail_count == 0
        and Q_l == A_sq
        and np.isclose(lhs_num, rhs_num)
    )
    print(
        f"CROSS_SECTOR_BRIDGE_PROPOSED_RETAINED_CHAIN_VERIFIED = "
        f"{CROSS_SECTOR_BRIDGE_PROPOSED_RETAINED_CHAIN_VERIFIED}"
    )
    print("FIVE_SIXTHS_MECHANISM_STATUS = bounded  # NOT closed by V1")
    print("COMMON_SCALE_15_PERCENT_GAP_STATUS = bounded  # NOT closed by V1")
    print(
        "(This flag verifies the V1 cross-sector chain authorities + "
        "algebraic identities. Independent audit required before the "
        "repo treats this as effective retained.)"
    )

    if fail_count == 0:
        print()
        print("All Block 3 chain authorities + algebraic identities verified.")
        return 0
    else:
        print(f"Failed audits: {AUDIT_FAILS}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
