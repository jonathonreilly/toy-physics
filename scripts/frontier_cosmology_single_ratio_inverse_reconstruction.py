#!/usr/bin/env python3
"""Single-ratio inverse reconstruction for late-time FRW cosmology.

Verifies:
  docs/COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md

Scope:
  retained/admitted flat-FRW + matter/radiation/Lambda surface only.
  This audits inverse reconstruction of L = Omega_Lambda,0 = (H_inf/H_0)^2.
  It does not derive the numerical value of L, Omega_m, q_0, z_*, or z_mLambda.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0
ROOT = Path(__file__).resolve().parents[1]


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


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def extract_status(content: str) -> str:
    for line in content.splitlines()[:30]:
        stripped = line.strip()
        if stripped.lower().startswith("**status:**") or stripped.lower().startswith("status:"):
            text = stripped
            for prefix in ("**Status:**", "**status:**", "Status:", "status:"):
                if text.lower().startswith(prefix.lower()):
                    text = text[len(prefix):].strip()
                    break
            return text
    return ""


def audit_authorities() -> None:
    banner("Authority status audit")

    authorities = (
        (
            "docs/COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md",
            ("retained/admitted", "structural"),
        ),
        (
            "docs/OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md",
            ("retained", "structural"),
        ),
        (
            "docs/DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md",
            ("retained", "structural"),
        ),
        (
            "docs/COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md",
            ("retained", "structural"),
        ),
    )

    for rel_path, required in authorities:
        content = read_text(rel_path)
        status = extract_status(content)
        print(f"  {Path(rel_path).name}: {status!r}")
        status_low = status.lower()
        check(
            f"authority status carries {', '.join(required)}: {Path(rel_path).name}",
            bool(content) and all(token in status_low for token in required),
        )


def audit_note_scope() -> None:
    banner("Scope boundary audit")

    note = read_text("docs/COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md")
    required_phrases = (
        "does not derive the numerical value",
        "does not promote `Omega_Lambda`",
        "does not close the matter-content bridge",
        "**Primary runner:** `scripts/frontier_cosmology_single_ratio_inverse_reconstruction.py`",
    )

    for phrase in required_phrases:
        check(f"note preserves scope phrase: {phrase}", phrase in note)


def audit_symbolic_inverses() -> None:
    banner("Symbolic inverse reconstruction")

    R, L, a, s, q0, E2 = sp.symbols("R L a s q0 E2", positive=True)
    M = 1 - L - R

    frw_E2 = R * a ** -4 + M * a ** -3 + L
    L_H = sp.simplify((E2 - R * a ** -4 - (1 - R) * a ** -3) / (1 - a ** -3))
    L_H_forward = sp.simplify(L_H.subs(E2, frw_E2) - L)
    print(f"  L_H(a) after substituting FRW E(a)^2: {L_H_forward}")
    check("H(a) inverse reconstructs L for a != 1", L_H_forward == 0)

    floor_expr = sp.simplify(frw_E2 - L)
    floor_expected = sp.simplify(M * a ** -3 + R * a ** -4)
    print(f"  E(a)^2 - L = {floor_expr}")
    check("Hubble floor: E(a)^2 - L = M a^-3 + R a^-4",
          sp.simplify(floor_expr - floor_expected) == 0)
    check("asymptotic floor: lim_{a->infinity} E(a)^2 = L",
          sp.limit(frw_E2, a, sp.oo) == L)

    q_forward = sp.Rational(1, 2) * (1 + R - 3 * L)
    L_q = sp.simplify((1 + R - 2 * q0) / 3)
    q_recon = sp.simplify(L_q.subs(q0, q_forward) - L)
    print(f"  L_q after substituting q_0(L): {q_recon}")
    check("q_0 inverse reconstructs L", q_recon == 0)

    L_qzero = sp.simplify((1 + R) / 3)
    check("q_0 < 0 threshold is L > (1+R)/3 algebraically identified",
          sp.simplify(q_forward.subs(L, L_qzero)) == 0)

    y = sp.symbols("y", positive=True)  # y = s_mL^3
    L_mL = sp.simplify(y * (1 - R) / (1 + y))
    mL_recon = sp.simplify(L_mL.subs(y, L / M) - L)
    print(f"  L_mL after substituting s_mL^3 = L/M: {mL_recon}")
    check("matter-Lambda equality inverse reconstructs L", mL_recon == 0)
    dLdy = sp.simplify(sp.diff(L_mL, y))
    print(f"  dL_mL/d(s^3) = {dLdy}")
    check("matter-Lambda inverse is increasing for R < 1, y > 0",
          sp.simplify(dLdy - (1 - R) / (1 + y) ** 2) == 0)

    a_star = sp.symbols("a_star", positive=True)
    L_acc = sp.simplify((a_star * (1 - R) + 2 * R) / (a_star + 2 * a_star ** 4))
    onset_eq = 2 * L * a_star ** 4 - M * a_star - 2 * R
    onset_residual = sp.simplify(onset_eq.subs(L, L_acc))
    print(f"  acceleration-onset residual after substituting L_acc: {onset_residual}")
    check("acceleration-onset inverse solves the exact quartic equation", onset_residual == 0)

    y_gap = sp.Rational(1, 2) / a_star ** 3
    R0_limit = sp.simplify(L_acc.subs(R, 0) - y_gap / (1 + y_gap))
    check("R -> 0 gap relation: a_*^3 = 1/(2 s_mL^3) reconciles both inverses",
          R0_limit == 0)


def audit_cross_consistency() -> None:
    banner("Cross-consistency certificate")

    # A concrete exact packet inside the physical interval.
    R = sp.Rational(1, 10000)
    L = sp.Rational(7, 10)
    M = 1 - L - R
    a = sp.Rational(2, 3)
    y = L / M
    a_star = sp.Rational(3, 5)

    E2 = R * a ** -4 + M * a ** -3 + L
    q0 = sp.Rational(1, 2) * (1 + R - 3 * L)
    L_H = sp.simplify((E2 - R * a ** -4 - (1 - R) * a ** -3) / (1 - a ** -3))
    L_q = sp.simplify((1 + R - 2 * q0) / 3)
    L_mL = sp.simplify(y * (1 - R) / (1 + y))
    L_acc = sp.simplify((a_star * (1 - R) + 2 * R) / (a_star + 2 * a_star ** 4))

    print(f"  sample R={R}, L={L}, M={M}, a={a}")
    print(f"  L_H={L_H}, L_q={L_q}, L_mL={L_mL}")
    check("sample H/q/matter-Lambda reconstructions agree with L",
          L_H == L_q == L_mL == L)

    M_acc = 1 - L_acc - R
    onset_residual = sp.simplify(2 * L_acc * a_star ** 4 - M_acc * a_star - 2 * R)
    physical_interval = bool(L_acc >= 0) and bool(L_acc <= 1 - R)
    check("sample acceleration inverse defines a compatible FRW packet",
          onset_residual == 0 and physical_interval)


def audit_package_wiring() -> None:
    banner("Package wiring")

    note = "COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md"
    runner = "frontier_cosmology_single_ratio_inverse_reconstruction.py"
    surfaces = (
        ("docs/CANONICAL_HARNESS_INDEX.md", (note, runner)),
        ("docs/publication/ci3_z3/CLAIMS_TABLE.md", (note,)),
        ("docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md", (note, runner)),
        ("docs/publication/ci3_z3/DERIVATION_ATLAS.md", (note, runner)),
        ("docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md", (note,)),
        ("docs/publication/ci3_z3/PUBLICATION_MATRIX.md", (note, runner)),
        ("docs/publication/ci3_z3/RESULTS_INDEX.md", (note, runner)),
        ("docs/publication/ci3_z3/SCIENCE_MAP.md", (note, runner)),
        ("docs/publication/ci3_z3/README.md", (note,)),
        ("docs/publication/ci3_z3/REPRODUCE.md", (runner,)),
        ("docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md", (note,)),
    )

    for rel_path, needles in surfaces:
        content = read_text(rel_path)
        missing = [needle for needle in needles if needle not in content]
        print(f"  {rel_path}: {'OK' if not missing else 'MISSING ' + ', '.join(missing)}")
        check(f"package surface wired: {rel_path}", not missing)


def main() -> int:
    print("=" * 88)
    print("Cosmology single-ratio inverse reconstruction audit")
    print("See docs/COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_authorities()
    audit_note_scope()
    audit_symbolic_inverses()
    audit_cross_consistency()
    audit_package_wiring()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
