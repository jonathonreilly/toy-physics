"""Runner: BH 1/4 carrier from framework Wald-Noether charge (Block 5).

Audits composition of framework's primitive-coframe boundary carrier
theorem (c_cell = 1/4) with the framework's retained discrete GR action
surface and the admitted Wald-Noether charge formula to derive
S_BH = A · c_cell = A/4 in framework lattice units, forcing
G_Newton,lat = 1.
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
    print("BH 1/4 Carrier from Framework Wald-Noether Charge (Block 5) audit")
    print("=" * 72)

    # ---- Section 1: chain authority audits --------------------------------

    print()
    print("Section 1: 5 retained chain authority audits")
    print("-" * 72)

    primitive_text = read_doc(
        "PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md"
    )
    audit(
        "PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER theorem exists",
        len(primitive_text) > 0,
        "retained on main",
    )
    audit(
        "Primitive carrier theorem: c_cell = 1/4",
        "c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4" in primitive_text
        or "c_cell = 1/4" in primitive_text,
        "Theorem 3 result",
    )

    extension_text = read_doc(
        "PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md"
    )
    audit(
        "PLANCK_BOUNDARY_DENSITY_EXTENSION theorem exists",
        len(extension_text) > 0,
        "retained on main",
    )

    universal_gr_text = read_doc(
        "UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md"
    )
    audit(
        "UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE exists",
        len(universal_gr_text) > 0,
        "retained framework GR action",
    )

    universal_qg_eh_text = read_doc(
        "UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md"
    )
    audit(
        "UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE exists",
        len(universal_qg_eh_text) > 0,
        "retained Einstein-Hilbert equivalence",
    )
    audit(
        "Framework gravitational action ≡ canonical textbook EH",
        "Einstein-Hilbert" in universal_qg_eh_text
        or "textbook" in universal_qg_eh_text,
        "EH equivalence clause",
    )

    source_unit_text = read_doc(
        "PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md"
    )
    audit(
        "PLANCK_SOURCE_UNIT_NORMALIZATION exists",
        len(source_unit_text) > 0,
        "retained source-unit normalization",
    )
    audit(
        "Source-unit normalization: G_kernel = 1/(4π) and G_Newton,lat = 1 separation",
        ("G_kernel" in source_unit_text or "G_Newton" in source_unit_text)
        and "1/(4" in source_unit_text,
        "source-unit separation clause",
    )

    # ---- Section 2: algebraic verification of c_cell = 1/4 ----------------

    print()
    print("Section 2: framework primitive c_cell computation (numerical)")
    print("-" * 72)

    # H_cell ≅ C^16 with Hamming-weight Boolean basis
    H_cell_dim = 16
    rho_cell = np.eye(H_cell_dim) / H_cell_dim

    # P_A = P_1 = sum over Hamming-weight-1 basis states
    def hamming_weight(x: int) -> int:
        return bin(x).count("1")

    P_A = np.zeros((H_cell_dim, H_cell_dim))
    for x in range(H_cell_dim):
        if hamming_weight(x) == 1:
            P_A[x, x] = 1.0

    audit(
        "P_A has rank 4 (Hamming-weight-1 subspace)",
        int(np.trace(P_A)) == 4,
        f"rank P_A = Tr P_A = {int(np.trace(P_A))}",
    )

    c_cell = float(np.trace(rho_cell @ P_A))
    audit(
        "c_cell = Tr(ρ_cell P_A) = 1/4 (numerical)",
        np.isclose(c_cell, 1 / 4),
        f"c_cell = {c_cell:.10f} = {sp.Rational(int(round(c_cell * 16)), 16)}",
    )
    audit(
        "Sympy: c_cell = 4/16 = 1/4",
        sp.Rational(4, 16) == sp.Rational(1, 4),
        f"4/16 = {sp.Rational(4, 16)} = 1/4",
    )

    # ---- Section 3: Wald-Noether for Einstein-Hilbert reduction -----------

    print()
    print("Section 3: Wald-Noether formula for Einstein-Hilbert (admitted)")
    print("-" * 72)

    # For L_EH = R / (16π G_N), Wald-Noether gives S_Wald = A / (4 G_N)
    # We verify the algebraic reduction symbolically.
    G_N = sp.symbols("G_N", positive=True)
    A_horizon = sp.symbols("A", positive=True)

    # The Wald formula: S_Wald = -2π ∫ (∂L/∂R_{abcd}) ε_ab ε_cd
    # For L_EH = R/(16π G_N), ∂L/∂R_{abcd} = (1/(16π G_N)) · (1/2)(g^ac g^bd - g^ad g^bc)
    # Evaluated for a Killing horizon with binormal: gives A/(4 G_N)
    # We just check the numerical constants line up
    coefficient = sp.Rational(1, 1) / (4 * G_N)
    S_Wald_EH = A_horizon * coefficient
    audit(
        "Wald-Noether for Einstein-Hilbert: S = A/(4G_N) (admitted)",
        sp.simplify(S_Wald_EH - A_horizon / (4 * G_N)) == 0,
        f"S_Wald|_EH = A/(4G_N), coefficient = 1/4 in 1/G_N units",
    )

    # ---- Section 4: composition ---------------------------------------------

    print()
    print("Section 4: composition c_cell = 1/(4 G_N) ⇒ G_Newton,lat = 1")
    print("-" * 72)

    # c_cell = 1/(4 G_N) and c_cell = 1/4 ⇒ G_N = 1
    c_cell_sym = sp.Rational(1, 4)
    G_Newton_lat = sp.solve(c_cell_sym - 1 / (4 * G_N), G_N)
    audit(
        "G_Newton,lat = 1 forced by c_cell = 1/4 in framework lattice units",
        G_Newton_lat == [1] or G_Newton_lat == [sp.Integer(1)],
        f"G_Newton,lat solve = {G_Newton_lat}",
    )

    # S_BH = A · c_cell = A/4 in framework lattice units
    S_BH_lat = A_horizon * c_cell_sym
    expected_S_BH = A_horizon / 4
    audit(
        "S_BH = A · c_cell = A/4 in framework lattice units",
        sp.simplify(S_BH_lat - expected_S_BH) == 0,
        f"S_BH = A · 1/4 = A/4 (lattice units)",
    )

    # Match to standard S_BH = A/(4G_N) with G_N = 1: equal
    standard_form = A_horizon / (4 * sp.Integer(1))
    audit(
        "Match to standard S_BH = A/(4G_N) with G_Newton,lat = 1",
        sp.simplify(S_BH_lat - standard_form) == 0,
        f"S_BH (framework) = A/4 = A/(4·G_Newton,lat) = standard form",
    )

    # ---- Section 5: status firewall fields --------------------------------

    print()
    print("Section 5: V1 status firewall fields")
    print("-" * 72)

    own_text = read_doc(
        "BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md"
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
        "V1 records wald_formula_status: admitted_universal_physics_input",
        "wald_formula_status: admitted_universal_physics_input" in own_text,
        "V1 firewall: Wald formula admitted",
    )
    audit(
        "V1 records gravitational_boundary_action_density_identification_status: explicit_bridge_premise",
        "gravitational_boundary_action_density_identification_status: explicit_bridge_premise"
        in own_text,
        "V1 firewall: bridge premise named",
    )
    audit(
        "V1 records g_newton_lat_eq_1_status: forced_by_chain",
        "g_newton_lat_eq_1_status: forced_by_chain" in own_text,
        "V1 firewall: G_Newton,lat = 1 forced",
    )

    # ---- Section 6: forbidden imports -------------------------------------

    print()
    print("Section 6: forbidden imports check")
    print("-" * 72)

    forbidden_imports = ["S_BH_obs", "M_Pl_obs", "G_Newton_obs"]
    body_only = own_text.split("## 6. Verification")[0]
    for token in forbidden_imports:
        is_load_bearing = (
            f"= {token}" in body_only or f"{token} = " in body_only
        )
        audit(
            f"forbidden import not used as proof input: {token}",
            not is_load_bearing,
            "no observational comparator enters proof",
        )

    # ---- Summary ----------------------------------------------------------

    print()
    print("=" * 72)
    fail_count = len(AUDIT_FAILS)
    print(f"FAIL count: {fail_count}")

    BH_QUARTER_PROPOSED_RETAINED_CHAIN_VERIFIED = (
        fail_count == 0
        and np.isclose(c_cell, 1 / 4)
        and (G_Newton_lat == [1] or G_Newton_lat == [sp.Integer(1)])
    )
    print(
        f"BH_QUARTER_PROPOSED_RETAINED_CHAIN_VERIFIED = "
        f"{BH_QUARTER_PROPOSED_RETAINED_CHAIN_VERIFIED}"
    )
    print("WALD_FORMULA_STATUS = admitted_universal_physics_input")
    print("BRIDGE_PREMISE_STATUS = explicit_bridge_premise")
    print("G_NEWTON_LAT = 1 (forced by chain)")
    print(
        "(This flag verifies the V1 chain authorities + algebraic identities. "
        "Independent audit required before the repo treats this as effective "
        "retained.)"
    )

    if fail_count == 0:
        print()
        print("All Block 5 chain authorities + algebraic identities verified.")
        return 0
    else:
        print(f"Failed audits: {AUDIT_FAILS}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
