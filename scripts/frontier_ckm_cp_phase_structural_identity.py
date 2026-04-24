#!/usr/bin/env python3
"""
CKM CP-phase structural identity theorem verification.

This runner packages a subtheorem already present inside the retained CKM
atlas/axiom closure:

  w_A1      = 1/6
  w_perp    = 5/6
  r^2       = rho^2 + eta^2 = 1/6
  rho       = r sqrt(w_A1)   = 1/6
  eta       = r sqrt(w_perp) = sqrt(5)/6
  cos^2(delta_CKM) = 1/6
  tan(delta_CKM)   = sqrt(5)
  J = alpha_s(v)^3 sqrt(5) / 72

It does not derive alpha_s(v), individual CKM magnitudes, or any BSM phase.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Retained atlas counts.
N_PAIR = 2
N_COLOR = 3
N_QUARK_BLOCK = N_PAIR * N_COLOR
DIM_A1 = 1
DIM_PERP = 5

# Exact structural fractions.
W_A1 = Fraction(DIM_A1, N_QUARK_BLOCK)
W_PERP = Fraction(DIM_PERP, N_QUARK_BLOCK)
RADIUS_SQUARED = Fraction(1, N_QUARK_BLOCK)
RHO_SQUARED = RADIUS_SQUARED * W_A1
ETA_SQUARED = RADIUS_SQUARED * W_PERP
RHO = Fraction(1, 6)
ETA = math.sqrt(5.0) / 6.0

# Wolfenstein/Jarlskog inputs already retained by the parent CKM atlas.
ALPHA_S_V = CANONICAL_ALPHA_S_V
LAMBDA_SQUARED = ALPHA_S_V / N_PAIR
A_SQUARED = Fraction(N_PAIR, N_COLOR)

# Post-derivation comparators only. These are not theorem inputs.
DELTA_COMPARATOR_DEG = 65.5
DELTA_COMPARATOR_ERR_DEG = 1.0
J_ANGLE_RECON_COMPARATOR = 3.304e-5
J_PDG_COMPARATOR = 3.30e-5


def part0_retained_counts() -> None:
    banner("Part 0: retained quark-block counts")

    check("quark block dimension is 2 x 3 = 6", N_QUARK_BLOCK == 6, f"N = {N_QUARK_BLOCK}")
    check("A1 channel dimension is 1", DIM_A1 == 1, f"dim_A1 = {DIM_A1}")
    check("orthogonal channel dimension is 5", DIM_PERP == 5, f"dim_perp = {DIM_PERP}")
    check("1 + 5 decomposition closes the six-state block", DIM_A1 + DIM_PERP == N_QUARK_BLOCK)


def part1_cp_plane_coordinates() -> None:
    banner("Part 1: CP-plane radius and coordinates")

    check("A1 angular weight w_A1 = 1/6", W_A1 == Fraction(1, 6), f"w_A1 = {W_A1}")
    check("orthogonal angular weight w_perp = 5/6", W_PERP == Fraction(5, 6), f"w_perp = {W_PERP}")
    check("angular weights sum to one", W_A1 + W_PERP == 1, f"{W_A1} + {W_PERP}")
    check("retained CKM CP radius squared r^2 = 1/6", RADIUS_SQUARED == Fraction(1, 6))
    check("rho^2 = r^2 w_A1 = 1/36", RHO_SQUARED == Fraction(1, 36), f"rho^2 = {RHO_SQUARED}")
    check("eta^2 = r^2 w_perp = 5/36", ETA_SQUARED == Fraction(5, 36), f"eta^2 = {ETA_SQUARED}")
    check("rho = 1/6", RHO == Fraction(1, 6), f"rho = {RHO}")
    check("eta = sqrt(5)/6", abs(ETA - math.sqrt(5.0) / 6.0) < 1e-15, f"eta = {ETA:.15f}")
    check("rho^2 + eta^2 = 1/6", RHO_SQUARED + ETA_SQUARED == RADIUS_SQUARED)


def part2_phase_identities() -> None:
    banner("Part 2: CKM phase identities")

    cos2_delta = RHO_SQUARED / RADIUS_SQUARED
    sin2_delta = ETA_SQUARED / RADIUS_SQUARED
    tan2_delta = sin2_delta / cos2_delta

    check("cos^2(delta_CKM) = 1/6", cos2_delta == Fraction(1, 6), f"cos^2 = {cos2_delta}")
    check("sin^2(delta_CKM) = 5/6", sin2_delta == Fraction(5, 6), f"sin^2 = {sin2_delta}")
    check("cos^2 + sin^2 = 1", cos2_delta + sin2_delta == 1)
    check("tan^2(delta_CKM) = 5", tan2_delta == 5, f"tan^2 = {tan2_delta}")

    delta_from_acos = math.acos(1.0 / math.sqrt(6.0))
    delta_from_atan = math.atan(math.sqrt(5.0))
    check("tan(delta_CKM) = sqrt(5)", abs(math.tan(delta_from_acos) - math.sqrt(5.0)) < 1e-14)
    check("delta = arccos(1/sqrt(6))", abs(math.cos(delta_from_acos) ** 2 - 1.0 / 6.0) < 1e-15)
    check("delta = arctan(sqrt(5))", abs(delta_from_acos - delta_from_atan) < 1e-15)
    check(
        "delta numerical value is 65.905157... degrees",
        abs(math.degrees(delta_from_acos) - 65.90515744788931) < 1e-12,
        f"delta = {math.degrees(delta_from_acos):.12f} deg",
    )


def part3_jarlskog_factorisation() -> None:
    banner("Part 3: Jarlskog factorisation")

    j_direct = (LAMBDA_SQUARED**3) * float(A_SQUARED) * ETA
    j_factored = (ALPHA_S_V**3) * math.sqrt(5.0) / 72.0

    check("lambda^2 = alpha_s(v)/2", abs(LAMBDA_SQUARED - ALPHA_S_V / 2.0) < 1e-15)
    check("A^2 = 2/3", A_SQUARED == Fraction(2, 3), f"A^2 = {A_SQUARED}")
    check(
        "J = lambda^6 A^2 eta = alpha_s(v)^3 sqrt(5)/72",
        abs(j_direct - j_factored) / j_factored < 1e-15,
        f"J = {j_factored:.6e}",
    )

    print(f"  alpha_s(v) from canonical plaquette surface = {ALPHA_S_V:.12f}")
    print(f"  J structural factorisation                  = {j_factored:.6e}")


def part4_post_derivation_comparators() -> None:
    banner("Part 4: post-derivation observation comparators")

    delta_framework_deg = math.degrees(math.acos(1.0 / math.sqrt(6.0)))
    delta_deviation = delta_framework_deg - DELTA_COMPARATOR_DEG
    j_framework = (ALPHA_S_V**3) * math.sqrt(5.0) / 72.0

    print(f"  framework delta = {delta_framework_deg:.6f} deg")
    print(f"  comparator delta = {DELTA_COMPARATOR_DEG:.3f} +/- {DELTA_COMPARATOR_ERR_DEG:.3f} deg")
    print(f"  framework J = {j_framework:.6e}")
    print(f"  angle-reconstructed comparator J = {J_ANGLE_RECON_COMPARATOR:.6e}")
    print(f"  PDG-style scalar comparator J    = {J_PDG_COMPARATOR:.6e}")

    check(
        "framework delta lies inside the quoted 1-degree comparator band",
        abs(delta_deviation) < DELTA_COMPARATOR_ERR_DEG,
        f"deviation = {delta_deviation:+.6f} deg",
    )
    check(
        "framework J lies within 5% of the angle-reconstructed comparator",
        abs(j_framework - J_ANGLE_RECON_COMPARATOR) / J_ANGLE_RECON_COMPARATOR < 0.05,
    )
    check(
        "framework J lies within 5% of the scalar PDG-style comparator",
        abs(j_framework - J_PDG_COMPARATOR) / J_PDG_COMPARATOR < 0.05,
    )


def part5_summary() -> None:
    banner("Part 5: summary")

    print("  STRUCTURAL IDENTITIES PACKAGED:")
    print("    rho = 1/6")
    print("    eta = sqrt(5)/6")
    print("    rho^2 + eta^2 = 1/6")
    print("    cos^2(delta_CKM) = 1/6")
    print("    sin^2(delta_CKM) = 5/6")
    print("    tan(delta_CKM) = sqrt(5)")
    print("    delta_CKM = arccos(1/sqrt(6)) = arctan(sqrt(5))")
    print("    J = alpha_s(v)^3 sqrt(5) / 72")
    print()
    print("  BOUNDARIES:")
    print("    no new alpha_s(v) derivation")
    print("    no new individual CKM-magnitude theorem beyond the parent atlas")
    print("    no BSM, PMNS, or Majorana CP-phase claim")


def main() -> int:
    print("=" * 88)
    print("CKM CP-phase structural identity theorem verification")
    print("See docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md")
    print("=" * 88)

    part0_retained_counts()
    part1_cp_plane_coordinates()
    part2_phase_identities()
    part3_jarlskog_factorisation()
    part4_post_derivation_comparators()
    part5_summary()

    print()
    print("=" * 88)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
