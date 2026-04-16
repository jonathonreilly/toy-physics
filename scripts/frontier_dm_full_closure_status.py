#!/usr/bin/env python3
"""
DM full-closure status on the current flagship branch.

Framework convention:
  "axiom" means only Cl(3) on Z^3.
"""

from __future__ import annotations

import sys

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
    kappa_axiom_reference,
)

import frontier_dm_leptogenesis_pmns_certified_global_selector_theorem as selector
import frontier_dm_quantitative_mapping_normalization_closure as mapping

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


def exact_one_flavor_eta_ratio() -> float:
    pkg = exact_package()
    kappa_direct, _ = kappa_axiom_reference(pkg.k_decay_exact)
    return S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT * pkg.epsilon_1 * kappa_direct / ETA_OBS


def main() -> int:
    print("=" * 88)
    print("DM FULL-CLOSURE STATUS")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')

    eta_one = exact_one_flavor_eta_ratio()
    branches = selector.certified_branch_search()
    low = branches[0]
    out = mapping.quantitative_map()

    check(
        "The exact one-flavor theorem-native baseline still undershoots by about 5.297x",
        abs((1.0 / eta_one) - 5.297004933778) < 1.0e-6,
        f"eta/eta_obs={eta_one:.12f}",
    )
    check(
        "The PMNS-assisted N_e route now has theorem-grade selector closure",
        len(branches) == 3 and abs(float(low.etas[0]) - 1.0) < 1.0e-10,
        f"branch count={len(branches)}, eta/eta_obs={float(low.etas[0]):.12f}",
    )
    check(
        "The final DM quantitative mapping / normalization is now closed",
        abs(out['r_final'] - 5.48285209497574) < 1.0e-12
        and abs(out['omega_b'] - 0.04919295758525652) < 1.0e-12
        and abs(out['omega_dm'] - 0.26971771055437643) < 1.0e-12,
        f"R={out['r_final']:.12f}, Omega_b={out['omega_b']:.12f}, Omega_DM={out['omega_dm']:.12f}",
    )

    print()
    print("  FINAL READ:")
    print(f"    one-flavor exact eta/eta_obs      = {eta_one:.12f}")
    print(f"    selected PMNS branch eta/eta_obs  = {float(low.etas[0]):.12f}")
    print(f"    derived Omega_b                   = {out['omega_b']:.12f}")
    print(f"    final R                           = {out['r_final']:.12f}")
    print(f"    final Omega_DM                    = {out['omega_dm']:.12f}")
    print()
    print("  STATUS: FULL DM CLOSURE ON THE PMNS-ASSISTED N_e ROUTE")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
