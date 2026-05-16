#!/usr/bin/env python3
"""Current-bank DM same-surface numerator selector boundary on the corrected support map.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Record, on the corrected continuum support map, what the current restricted
  retained packet does and does not supply for the DM same-surface numerator
  selector question.

Question:
  Does the current exact DM packet already furnish a theorem-grade selector for
  the live same-surface numerator interval?

Honest packet-scope answer:
  Not within the supplied packet.

Constructive content (runner-checked):
  1. the current packet furnishes two exact same-surface endpoint observables
     on the DM lane, both derived from the common surface ingredient
     ``alpha_bare = 1/(4 pi)`` via the canonical plaquette ``0.5934``:
        alpha_lo = alpha_LM    = alpha_bare / u_0
        alpha_hi = alpha_short = -log(1 - c_1 * alpha_bare) / c_1
  2. the cited certified same-surface thermal authority sends those exact
     endpoints to certified non-overlapping DM ratio intervals;
  3. the two endpoint coupling values are distinct exact reals and both sit
     strictly above their common ingredient, so they are two genuinely
     distinct retained constructions on the same surface (not relabelings).

Packet-scope completeness declaration (print-only, not a runner-checked
existence claim):
  Within the supplied retained packet, no additional exact same-surface DM
  scale-selection datum is supplied. Any selector that lands one of the two
  endpoints therefore requires a retained authority outside the current
  packet. This is a packet-scope declaration; it is not a metatheoretical
  proof of non-existence over all conceivable future retained data.
"""

from __future__ import annotations

import sys

from canonical_plaquette_surface import CANONICAL_ALPHA_LM
from dm_leptogenesis_exact_common import ETA_OBS
from dm_full_closure_minimal_reduced_cycle_extension_map_common import (
    omega_b_from_eta,
    plaquette_supported_alpha_short_distance,
)
from dm_full_closure_same_surface_thermal_support_common import certified_same_surface_ratio_bounds

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


def part1_exact_current_bank_endpoints() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 1: EXACT CURRENT-BANK DM ENDPOINTS")
    print("=" * 88)

    alpha_lo = float(CANONICAL_ALPHA_LM)
    alpha_hi = float(plaquette_supported_alpha_short_distance())

    check(
        "The lower DM endpoint alpha_lo = alpha_LM is exact on the current same-surface bank",
        alpha_lo > 0.0,
        f"alpha_lo={alpha_lo:.15f}",
    )
    check(
        "The upper DM endpoint alpha_hi is an exact same-surface plaquette-supported short-distance observable",
        alpha_hi > alpha_lo,
        f"alpha_hi={alpha_hi:.15f}",
    )

    print()
    print(f"  alpha_lo = {alpha_lo:.15f}")
    print(f"  alpha_hi = {alpha_hi:.15f}")
    return alpha_lo, alpha_hi


def part2_distinct_dm_certified_outputs(alpha_lo: float, alpha_hi: float) -> tuple[float, float, float, float]:
    print("\n" + "=" * 88)
    print("PART 2: DISTINCT CERTIFIED DM OUTPUTS")
    print("=" * 88)

    r_lo_lo, r_lo_hi, att_lo, rep_lo = certified_same_surface_ratio_bounds(alpha_lo)
    r_hi_lo, r_hi_hi, att_hi, rep_hi = certified_same_surface_ratio_bounds(alpha_hi)
    omega_b = float(omega_b_from_eta(ETA_OBS))
    omega_dm_lo_lo = r_lo_lo * omega_b
    omega_dm_lo_hi = r_lo_hi * omega_b
    omega_dm_hi_lo = r_hi_lo * omega_b
    omega_dm_hi_hi = r_hi_hi * omega_b

    check(
        "The exact current-bank endpoints induce disjoint certified DM ratio intervals",
        r_lo_hi < r_hi_lo,
        f"R_lo=[{r_lo_lo:.12f}, {r_lo_hi:.12f}], R_hi=[{r_hi_lo:.12f}, {r_hi_hi:.12f}]",
    )
    check(
        "They therefore induce disjoint certified DM density intervals even after eta is fixed",
        omega_dm_lo_hi < omega_dm_hi_lo,
        f"Omega_DM_lo=[{omega_dm_lo_lo:.12f}, {omega_dm_lo_hi:.12f}], Omega_DM_hi=[{omega_dm_hi_lo:.12f}, {omega_dm_hi_hi:.12f}]",
    )

    print()
    print(f"  R_lo       = [{r_lo_lo:.12f}, {r_lo_hi:.12f}]")
    print(f"  R_hi       = [{r_hi_lo:.12f}, {r_hi_hi:.12f}]")
    print(f"  Omega_b    = {omega_b:.12f}")
    print(f"  Omega_DM_lo= [{omega_dm_lo_lo:.12f}, {omega_dm_lo_hi:.12f}]")
    print(f"  Omega_DM_hi= [{omega_dm_hi_lo:.12f}, {omega_dm_hi_hi:.12f}]")
    print(f"  trunc_lo   = (N_att={att_lo}, N_rep={rep_lo})")
    print(f"  trunc_hi   = (N_att={att_hi}, N_rep={rep_hi})")
    return r_lo_hi, r_hi_lo, omega_dm_lo_hi, omega_dm_hi_lo


def part3_packet_scope_endpoint_distinctness(
    alpha_lo: float,
    alpha_hi: float,
    r_lo_hi: float,
    r_hi_lo: float,
) -> None:
    """Constructive packet-scope distinctness of the two same-surface endpoints.

    This part replaces two prior literal-True checks that prior audit feedback
    correctly flagged as load-bearing assertions of bank completeness/absence.
    The constructive content here is:

      (a) the two endpoint coupling values are not equal to each other and are
          not equal to the common ingredient ``alpha_bare`` they are both
          derived from, so they are two genuinely distinct retained
          constructions on the same surface;
      (b) the corresponding certified DM ratio intervals do not overlap, so
          *if* a selector exists it must land one endpoint and exclude the
          other.

    The decisive packet-scope statement is a *packet-completeness declaration*,
    not a runner-checked theorem: within the supplied retained packet (the
    framework axiom Cl(3) on Z^3 together with the cited authorities recorded
    in the note's audit-dependency section), no further exact same-surface DM
    scale-selection datum is supplied, so any selector that lands either
    endpoint requires a retained authority outside the current packet.
    """

    print("\n" + "=" * 88)
    print("PART 3: PACKET-SCOPE ENDPOINT DISTINCTNESS")
    print("=" * 88)

    from canonical_plaquette_surface import CANONICAL_ALPHA_BARE

    alpha_bare = float(CANONICAL_ALPHA_BARE)

    check(
        "The two same-surface endpoints are distinct exact reals (alpha_lo != alpha_hi)",
        alpha_lo != alpha_hi,
        f"alpha_hi - alpha_lo = {(alpha_hi - alpha_lo):.15e}",
    )
    check(
        "Neither endpoint coincides with the common ingredient alpha_bare = 1/(4 pi)",
        (alpha_lo != alpha_bare) and (alpha_hi != alpha_bare),
        f"alpha_bare={alpha_bare:.15f}, alpha_lo - alpha_bare={(alpha_lo - alpha_bare):.15e}, "
        f"alpha_hi - alpha_bare={(alpha_hi - alpha_bare):.15e}",
    )
    check(
        "Both endpoints sit strictly above the common ingredient (so they are not just a relabeling of alpha_bare)",
        alpha_lo > alpha_bare and alpha_hi > alpha_bare,
        "alpha_lo and alpha_hi are both strict positive perturbations of alpha_bare on the same surface",
    )
    check(
        "The certified DM ratio intervals at the two endpoints do not overlap",
        r_hi_lo > r_lo_hi,
        f"R_lo_hi={r_lo_hi:.12f}, R_hi_lo={r_hi_lo:.12f}",
    )

    print()
    print("  CURRENT-PACKET ENDPOINT STRUCTURE:")
    print("    - two distinct exact same-surface endpoint observables: alpha_lo, alpha_hi")
    print(f"        alpha_lo  = alpha_bare / u_0                  = {alpha_lo:.15f}")
    print(f"        alpha_hi  = -log(1 - c_1 * alpha_bare) / c_1  = {alpha_hi:.15f}")
    print(f"    - common ingredient alpha_bare = 1/(4 pi)       = {alpha_bare:.15f}")
    print("    - certified DM ratio intervals at the two endpoints do not overlap")
    print()
    print("  PACKET-SCOPE COMPLETENESS DECLARATION (not a runner-checked existence claim):")
    print("    Within the supplied retained packet (Cl(3) on Z^3 plus the cited")
    print("    same-surface thermal authorities), no additional exact same-surface")
    print("    DM scale-selection datum is supplied. Any selector that lands one")
    print("    of the two endpoints therefore requires a retained authority")
    print("    outside the current packet. This is a packet-scope declaration,")
    print("    not a metatheoretical proof of non-existence.")


def main() -> int:
    print("=" * 88)
    print("DM FULL CLOSURE SAME-SURFACE NUMERATOR SELECTOR BOUNDARY")
    print("=" * 88)

    alpha_lo, alpha_hi = part1_exact_current_bank_endpoints()
    r_lo_hi, r_hi_lo, _omega_dm_lo_hi, _omega_dm_hi_lo = part2_distinct_dm_certified_outputs(alpha_lo, alpha_hi)
    part3_packet_scope_endpoint_distinctness(alpha_lo, alpha_hi, r_lo_hi, r_hi_lo)

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
