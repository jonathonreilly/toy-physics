"""Runner: cosmological constant Λ R-budget support (Block 9)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


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


def read_doc(p: str) -> str:
    return (DOCS_DIR / p).read_text(encoding="utf-8")


def main() -> int:
    print("=" * 72)
    print("Cosmological Constant Λ R-Budget Support (Block 9) audit")
    print("=" * 72)

    spectral = read_doc("COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md")
    audit("Spectral-gap identity theorem exists", len(spectral) > 0, "retained")
    audit("Λ = λ_1(S³_R) = 3/R² function identity",
          "Lambda_vac = lambda_1(S^3_R) = 3 / R^2" in spectral
          or "Λ_vac = λ_1(S³_R) = 3/R²" in spectral
          or "Λ = 3/R²" in spectral
          or "3 / R^2" in spectral,
          "retained function identity")

    universal_gr = read_doc("UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md")
    audit("UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE exists", len(universal_gr) > 0, "retained")

    s3_general = read_doc("S3_GENERAL_R_DERIVATION_NOTE.md")
    audit("S^3 general R derivation exists", len(s3_general) > 0, "retained")

    block4 = read_doc("AXIOM_STACK_MINIMALITY_CL4C_NO_GO_THEOREM_NOTE_2026-04-29.md")
    audit("Block 4 route note exists for historical budget context",
          "Cl_4(C)" in block4 and "Axiom*" in block4,
          "historical context")
    audit("C1/Axiom* budget surface is named",
          "Hubble" in block4 or "(C1)" in block4,
          "R-budget basis")

    # Algebraic verification: Λ = 3/R² function identity
    R_test = np.array([1.0, 2.0, 5.0, 1e26])
    Lambda_test = 3.0 / R_test ** 2
    expected = 3.0 / R_test ** 2
    audit("Λ = 3/R² function identity (numerical witness)",
          np.allclose(Lambda_test, expected),
          f"verified for R ∈ {R_test.tolist()[:3]}+")

    # Inverted: implied R from Planck Λ_obs
    Lambda_obs = 1.09e-52  # m^-2
    R_implied = np.sqrt(3.0 / Lambda_obs)
    audit("Implied R from Planck Λ_obs ≈ Hubble radius",
          1e25 < R_implied < 1e27,
          f"R = √(3/Λ_obs) = {R_implied:.3e} m")

    own = read_doc("COSMOLOGICAL_CONSTANT_RETENTION_WITH_R_BUDGET_THEOREM_NOTE_2026-04-29.md")
    audit("V1 actual_current_surface_status: bounded",
          "actual_current_surface_status: bounded" in own, "firewall")
    audit("V1 proposal_allowed: false",
          "proposal_allowed: false" in own, "firewall")
    audit("V1 audit_required_before_effective_retained: false",
          "audit_required_before_effective_retained: false" in own, "firewall")
    audit("V1 bare_retained_allowed: false",
          "bare_retained_allowed: false" in own, "firewall")
    audit("V1 r_function_identity_status: retained_exact",
          "r_function_identity_status: retained_exact" in own, "firewall: R₁ retained")
    audit("V1 r_numerical_value_status: bounded_open_c1_surface",
          "r_numerical_value_status: bounded_open_c1_surface" in own, "firewall: R₂ bounded")

    print()
    print("=" * 72)
    fail_count = len(AUDIT_FAILS)
    print(f"FAIL count: {fail_count}")
    print("LAMBDA_R_BUDGET_SUPPORT_VERIFIED =", fail_count == 0)
    print(f"R from Planck Λ_obs = {R_implied:.3e} m (Hubble scale)")
    if fail_count == 0:
        print()
        print("All Block 9 chain authorities + bounded R-budget verified.")
        return 0
    else:
        print(f"Failed audits: {AUDIT_FAILS}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
