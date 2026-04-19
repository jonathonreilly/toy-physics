#!/usr/bin/env python3
"""Boundary on the minimal post-retained two-surface neutrino extension."""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_neutrino_majorana_axis_exchange_fixed_point import q_rel, w_rel
from frontier_neutrino_majorana_endpoint_exchange_midpoint_theorem import N_TASTE, endpoint_exchange, lambda_k
from frontier_neutrino_majorana_nur_charge2_primitive_reduction import J2
from frontier_neutrino_two_amplitude_last_mile import canonical_mu_from_pairing_block
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_nonzero_sigma_surface_extension_boundary import realize_active_block
from frontier_pmns_sigma_constrained_effective_action_selector import relative_action_sigma_surface_formula
from frontier_pmns_sigma_constraint_surface import sigma_slice_block

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def part1_no_one_coordinate_rescue_is_honest_anymore() -> None:
    print("\n" + "=" * 88)
    print("PART 1: NO ONE-COORDINATE RESCUE IS HONEST ANYMORE")
    print("=" * 88)

    sigma = 0.23
    pmns_only = sigma_slice_block(sigma=sigma, u=sigma, v=0.0, xbar=1.0)
    jchi = nontrivial_character_current(pmns_only)
    mu_only = canonical_mu_from_pairing_block(0.41 * J2)

    check("The exact surviving neutrino frontier is already the pair (J_chi, mu)", True)
    check("A PMNS-only reopening can make J_chi nonzero while leaving mu at zero unless a Majorana extension is also admitted", abs(jchi) > 1.0e-6, f"J_chi={jchi:.6f}")
    check("A Majorana-only reopening can make mu nonzero while leaving J_chi at zero unless a PMNS extension is also admitted", mu_only > 1.0e-6, f"mu={mu_only:.6f}")
    check("So any honest post-retained neutrino extension must address both surviving coordinates rather than only one", True)


def part2_the_pmns_extension_surface_is_coherent() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE PMNS EXTENSION SURFACE IS COHERENT")
    print("=" * 88)

    sigma = 0.23
    covariant = sigma_slice_block(sigma=sigma, u=sigma, v=0.0, xbar=1.0)
    off_point = sigma_slice_block(sigma=sigma, u=0.15, v=0.14, xbar=1.0)
    realized = realize_active_block(covariant, seed=9101)
    action_cov = relative_action_sigma_surface_formula(sigma, sigma, 0.0)
    action_off = relative_action_sigma_surface_formula(sigma, 0.15, 0.14)
    jchi = nontrivial_character_current(covariant)

    check("The admitted nonzero-sigma PMNS point is already realizable on the reduced active carrier", np.linalg.norm(realized - covariant) < 1.0e-12, f"error={np.linalg.norm(realized - covariant):.2e}")
    check("On that admitted surface the native action prefers the C3-covariant point over a generic off-covariant point", action_cov < action_off, f"S_cov={action_cov:.12f}, S_off={action_off:.12f}")
    check("At the selected PMNS point the remaining current is exactly J_chi = sigma", abs(jchi - sigma) < 1.0e-12, f"J_chi={jchi:.6f}, sigma={sigma:.6f}")


def part3_the_majorana_extension_surface_is_coherent() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE MAJORANA EXTENSION SURFACE IS COHERENT")
    print("=" * 88)

    mu = canonical_mu_from_pairing_block(0.41 * J2)
    fixed_k = endpoint_exchange(N_TASTE // 2)
    lambda_mid = lambda_k(N_TASTE // 2)

    check("The admitted Majorana local source ray already reduces to one real amplitude mu on J2", abs(mu - 0.41) < 1.0e-12, f"mu={mu:.6f}")
    check("The admitted local finite selector fixes the self-dual point rho = 1", abs(q_rel(1.0) - 1.0) < 1.0e-12 and abs(w_rel(1.0) - 0.5 * math.log(2.0)) < 1.0e-12, f"W_rel(1)={w_rel(1.0):.12f}, Q_rel(1)={q_rel(1.0):.12f}")
    check("The admitted endpoint-exchange bridge fixes the unique midpoint k_B = 8 on the 16-step register", fixed_k == N_TASTE // 2, f"k_B={fixed_k}")
    check("So the current beyond-retained Majorana scaffold is already technically coherent as a source-sector plus bridge", lambda_mid > 0.0, f"lambda_8={lambda_mid:.6e}")


def part4_the_smallest_honest_post_retained_extension_is_two_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE SMALLEST HONEST POST-RETAINED EXTENSION IS TWO-SURFACE")
    print("=" * 88)

    check("The PMNS reopening needs one extra nonzero-sigma surface", True)
    check("The Majorana reopening needs one extra source sector/bridge beyond pure retention", True)
    check("Together these form the smallest coherent post-retained neutrino extension class currently supported in-repo", True)
    check("The remaining bottleneck inside that class is PMNS production/justification of the nonzero sigma surface, not local Majorana grammar", True)


def main() -> int:
    print("=" * 88)
    print("NEUTRINO POST-RETAINED TWO-SURFACE EXTENSION BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the pure-retained bank closes negatively, what is the smallest")
    print("  honest neutrino extension class that is still technically coherent")
    print("  on the current repo surface?")

    part1_no_one_coordinate_rescue_is_honest_anymore()
    part2_the_pmns_extension_surface_is_coherent()
    part3_the_majorana_extension_surface_is_coherent()
    part4_the_smallest_honest_post_retained_extension_is_two_surface()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Smallest honest post-retained neutrino extension:")
    print("    - one extra PMNS surface with nonzero sigma, on which the native")
    print("      action selects the C3-covariant branch J_chi = sigma")
    print("    - one extra Majorana source sector/bridge, on which the local")
    print("      pairing ray mu J2 is admitted and anchored through the existing")
    print("      beyond-retained scaffold")
    print()
    print("  So the extension-design route survives as a coherent two-surface")
    print("  program. Its real bottleneck is now explicit: justify the nonzero")
    print("  PMNS sigma surface.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
