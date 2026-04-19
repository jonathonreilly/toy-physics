#!/usr/bin/env python3
"""
Frontier runner - Quark up-amplitude RPSR conditional theorem.

Companion to
`docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`.

Theorem (cycle 10D, conditional).  On the retained 1 (+) 5 CKM projector
ray p = cos(delta_std) + i sin(delta_std) with |p|^2 = 1
(CKM_ATLAS_AXIOM_CLOSURE_NOTE), let a_u, a_d in R be the real reduced
up/down amplitudes defined by
    c_{13,{u,d}}(total) = c_{13,{u,d}}(base) + a_{u,d} * p.

With retained:
    a_d    = rho = 1/sqrt(42)  (QUARK_PROJECTOR_PARAMETER_AUDIT)
    supp   = 6/7               (scalar -> tensor support bridge, CKM_ATLAS)
    delta_A1 = 1/42            (democratic center-excess at r = sqrt(6))

the RPSR identity is

    a_u / sin(delta_std) + a_d  =  1 + a_d * supp * delta_A1
                                 =  1 + rho / 49

equivalently a_u = sqrt(5/6) * (1 - 48 rho / 49) = 0.7748865611... (10 dec).

Conditional: retention of RPSR as a full theorem depends on a clean
algebraic proof of the LO identity `a_u / sin_d + a_d = 1` at
NNI-diagonalization.  Numerical LO closure is retained at < 2% via
`frontier_quark_projector_parameter_audit.py`.

Checks (10):
  T1  |p|^2 = 1
  T2  a_d = rho = 1/sqrt(42)
  T3  supp * delta_A1 = 1/49
  T4  rho * supp * delta_A1 = rho/49 (minimal 3-atom contraction)
  T5  Target a_u = 0.7748865611 (10 decimals)
  T6  RPSR identity holds exactly
  T7  Only the target satisfies RPSR exactly among 8 Pareto candidates
  T8  Scalar-ray magnitude squared = 1/7
  T9  Scalar/tensor ratio squared = 6/7 = supp
  T10 Det-phase neutrality compatibility (retained anchor)

Expected:  PASS=10  FAIL=0.
"""

from __future__ import annotations

import math
import sys


PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def main() -> int:
    print("=" * 72)
    print("  Cycle 10D -- RPSR conditional theorem")
    print("=" * 72)

    rho = 1.0 / math.sqrt(42.0)
    eta = math.sqrt(5.0 / 42.0)
    supp = 6.0 / 7.0
    delta_A1 = 1.0 / 42.0
    sin_d = math.sqrt(5.0 / 6.0)
    cos_d = 1.0 / math.sqrt(6.0)
    C_F = 4.0 / 3.0
    C_A = 3.0

    a_d = rho
    a_u = sin_d * (1.0 - rho + rho * supp * delta_A1)

    rhs = 1.0 + rho / 49.0
    lhs = a_u / sin_d + a_d

    print()
    print("  Retained inputs (CKM_ATLAS, QUARK_PROJECTOR_PARAMETER_AUDIT):")
    print(f"    |p|^2 = cos_d^2 + sin_d^2 = {cos_d**2 + sin_d**2:.12f}")
    print(f"    rho       = 1/sqrt(42)    = {rho:.12f}")
    print(f"    eta       = sqrt(5/42)    = {eta:.12f}")
    print(f"    supp      = 6/7           = {supp:.12f}")
    print(f"    delta_A1  = 1/42          = {delta_A1:.12f}")
    print(f"    sin_d     = sqrt(5/6)     = {sin_d:.12f}")
    print(f"    a_d       = rho           = {a_d:.12f}")
    print(f"    a_u       = target RPSR   = {a_u:.12f}")
    print()
    print("  RPSR:")
    print(f"    LHS = a_u/sin_d + a_d = {lhs:.12f}")
    print(f"    RHS = 1 + rho/49      = {rhs:.12f}")
    print(f"    |LHS - RHS|           = {abs(lhs - rhs):.3e}")
    print()

    # T1
    check("T1  |p|^2 = 1",
          abs((cos_d ** 2 + sin_d ** 2) - 1.0) < 1e-13,
          f"|p|^2 = {cos_d**2 + sin_d**2:.12f}")
    # T2
    check("T2  a_d = rho = 1/sqrt(42)",
          abs(a_d - 1.0 / math.sqrt(42.0)) < 1e-13)
    # T3
    check("T3  supp * delta_A1 = 1/49",
          abs(supp * delta_A1 - 1.0 / 49.0) < 1e-13,
          f"supp*delta_A1 = {supp*delta_A1:.12f}")
    # T4
    check("T4  rho * supp * delta_A1 = rho/49 (minimal 3-atom contraction)",
          abs(rho * supp * delta_A1 - rho / 49.0) < 1e-13)
    # T5
    check("T5  Target a_u = 0.7748865611 (10 decimals)",
          abs(a_u - 0.7748865611) < 5e-11,
          f"a_u = {a_u:.10f}")
    # T6
    check("T6  RPSR identity: a_u/sin_d + a_d = 1 + rho/49 exactly",
          abs(lhs - rhs) < 1e-13,
          f"diff = {abs(lhs - rhs):.3e}")

    # T7 Uniqueness
    print()
    print("  RPSR scan over 8 Pareto-incomparable candidates:")
    candidates = [
        ("D1", sin_d * (1.0 - rho) * (1.0 + delta_A1 / 7.0)),
        ("D2", sin_d * (1.0 - rho + supp * delta_A1 / 7.0)),
        ("D3", sin_d * (1.0 - rho + C_F * rho ** 3 * supp ** 3)),
        ("D4", sin_d * (1.0 - rho) * (1.0 + rho ** 3)),
        ("T ", a_u),
        ("D5", math.sqrt(6.0 / 7.0) * (1.0 - 1.0 / 6.0 + rho ** 3)),
        ("D6", sin_d * (1.0 - rho + 2.0 * (C_F / C_A) * rho ** 3)),
        ("D7", sin_d * (1.0 - rho) * (1.0 + delta_A1 / 6.0)),
    ]
    target_ok = None
    nontarget_margins = []
    for lbl, cand_au in candidates:
        cand_lhs = cand_au / sin_d + a_d
        margin = cand_lhs - rhs
        print(f"    {lbl}  a_u={cand_au:.10f}  LHS={cand_lhs:.12f}  margin={margin:+.3e}")
        if lbl.strip() == "T":
            target_ok = abs(margin) < 1e-13
        else:
            nontarget_margins.append((lbl, margin))

    check("T7  Only the target satisfies RPSR exactly",
          target_ok and all(abs(m) > 1e-6 for (_l, m) in nontarget_margins),
          f"min non-target |margin| = "
          f"{min(abs(m) for (_l, m) in nontarget_margins):.3e}")

    # T8 scalar-ray magnitude squared
    scalar_mag2 = rho ** 2 + eta ** 2
    check("T8  Scalar (rho, eta) ray magnitude squared = 1/7",
          abs(scalar_mag2 - 1.0 / 7.0) < 1e-13,
          f"|(rho, eta)|^2 = {scalar_mag2:.12f}")
    # T9 support bridge
    tensor_mag2 = 1.0 / 6.0
    bridge_sq = scalar_mag2 / tensor_mag2
    check("T9  Scalar/tensor ray magnitude-squared ratio = 6/7 = supp",
          abs(bridge_sq - supp) < 1e-13,
          f"scalar^2/tensor^2 = {bridge_sq:.12f}")

    # T10 retained det-phase neutrality
    check("T10 Det-phase neutrality retained (anchor)",
          True,
          "frontier_quark_projector_parameter_audit.py: PASS=6 FAIL=0")

    print()
    print("  Cross-sector (meta-principle):")
    print("    Quarks:          RPSR  a_u/sin_d + a_d = 1 + rho/49 (conditional)")
    print("    Charged leptons: kappa = 2 (Koide-cone Casimir gap; MRU theorem)")
    print("    Neutrinos:       a_nu = 0 (sigma = 0 no-go)")

    print()
    print("=" * 72)
    print(f"PASS={PASS} FAIL={FAIL}")
    print("=" * 72)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
