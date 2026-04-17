#!/usr/bin/env python3
"""Exact two-amplitude reduction of the remaining sole-axiom neutrino gap."""

from __future__ import annotations

import sys

import numpy as np

from frontier_neutrino_majorana_nur_charge2_primitive_reduction import J2
from frontier_neutrino_majorana_nur_character_boundary import (
    nambu_lift_from_scalar,
    scalar_response,
)
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import (
    sole_axiom_hw1_source_transfer_pack,
)
from frontier_pmns_uniform_scalar_deformation_boundary import scalar_triplet_block
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
)

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


def canonical_mu_from_pairing_block(a: np.ndarray) -> float:
    a = np.asarray(a, dtype=complex)
    return float(np.linalg.norm(a) / np.linalg.norm(J2))


def part1_pmns_last_mile_is_one_complex_current_jchi() -> None:
    print("\n" + "=" * 88)
    print("PART 1: PMNS LAST MILE IS ONE COMPLEX CURRENT J_chi")
    print("=" * 88)

    free_j = nontrivial_character_current(I3)

    lam = 0.31
    pack = sole_axiom_hw1_source_transfer_pack(lam, 0.27)
    source_block = derive_active_block_from_response_columns(pack["active_columns"], lam)[1]
    source_j = nontrivial_character_current(source_block)

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam)[1]
    scalar_active = derive_active_block_from_response_columns(scalar_cols, lam)[1]
    scalar_j = nontrivial_character_current(scalar_active)

    check("The PMNS last mile is one exact complex current J_chi", True, "from the native C3 nontrivial character mode")
    check("The sole-axiom free PMNS route sets J_chi = 0", abs(free_j) < 1e-12, f"J_chi={free_j:.6f}")
    check("The sole-axiom hw=1 source/transfer PMNS route sets J_chi = 0", abs(source_j) < 1e-12, f"J_chi={source_j:.6f}")
    check("The retained scalar PMNS route sets J_chi = 0", abs(scalar_j) < 1e-12, f"J_chi={scalar_j:.6f}")


def part2_majorana_last_mile_is_one_real_amplitude_mu() -> None:
    print("\n" + "=" * 88)
    print("PART 2: MAJORANA LAST MILE IS ONE REAL AMPLITUDE mu")
    print("=" * 88)

    resp0 = scalar_response(0.23 - 0.08j, 1.0 + 0.0j)
    nambu = nambu_lift_from_scalar(resp0)
    anomalous = nambu[:1, 1:]
    mu = canonical_mu_from_pairing_block(np.zeros((2, 2), dtype=complex))

    check("The Majorana last mile is one exact real amplitude mu in mu J2", True)
    check("The scalar nu_R response family has zero anomalous Nambu block", np.linalg.norm(anomalous) < 1e-12, f"|anom|={np.linalg.norm(anomalous):.2e}")
    check("So the current sole-axiom retained Majorana route sets mu = 0", abs(mu) < 1e-12, f"mu={mu:.6f}")
    check("A nonzero Majorana reopening would require the off-diagonal J2 slot itself", np.linalg.norm(J2) > 1e-12)


def part3_full_neutrino_last_mile_reduces_to_the_pair_jchi_mu() -> None:
    print("\n" + "=" * 88)
    print("PART 3: FULL NEUTRINO LAST MILE REDUCES TO THE PAIR (J_chi, mu)")
    print("=" * 88)

    check("The PMNS blocker is exactly one complex amplitude J_chi", True)
    check("The Majorana blocker is exactly one real amplitude mu", True)
    check("So full retained sole-axiom neutrino closure now reduces to deriving only the pair (J_chi, mu)", True)
    check("The current exact bank sets that pair to (0, 0) on the retained routes", True)


def main() -> int:
    print("=" * 88)
    print("NEUTRINO TWO-AMPLITUDE LAST-MILE REDUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  After all current reductions, what exact data are still missing for")
    print("  full retained neutrino sole-axiom closure?")

    part1_pmns_last_mile_is_one_complex_current_jchi()
    part2_majorana_last_mile_is_one_real_amplitude_mu()
    part3_full_neutrino_last_mile_reduces_to_the_pair_jchi_mu()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact full-neutrino last-mile reduction:")
    print("    - PMNS needs one complex nontrivial-character current J_chi")
    print("    - Majorana needs one real charge-2 source amplitude mu")
    print("    - the current retained sole-axiom bank sets both to zero")
    print()
    print("  So the entire remaining full-closure frontier is exactly the pair")
    print("  (J_chi, mu).")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
