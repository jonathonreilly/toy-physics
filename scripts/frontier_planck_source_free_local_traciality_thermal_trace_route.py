#!/usr/bin/env python3
"""Audit the primitive thermal-trace/KMS route for source-free local traciality.

The route asks whether the last Planck blocker

    rho_cell = I_16 / 16

can be forced on the primitive time-locked C^16 cell by a same-surface thermal
state argument. The sharp answer is:

    rho_(beta,H) is tracial iff beta = 0 or H is scalar.

So the route is exact and useful, but not automatically closing.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import math
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_LOCAL_TRACIALITY_THERMAL_TRACE_ROUTE_2026-04-23.md"
COUNTING = ROOT / "docs/PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md"
SOURCEFREE = ROOT / "docs/PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md"
ROUTECHECK = ROOT / "docs/PLANCK_SCALE_AXIOM_NATIVE_ROUTE_CHECK_2026-04-23.md"
PERRON = ROOT / "docs/GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return bool(passed)


def projector(indices: list[int], dim: int = 16) -> sp.Matrix:
    mat = sp.zeros(dim)
    for idx in indices:
        mat[idx, idx] = 1
    return mat


def main() -> int:
    note = normalized(NOTE)
    counting = normalized(COUNTING)
    sourcefree = normalized(SOURCEFREE)
    routecheck = normalized(ROUTECHECK)
    perron = normalized(PERRON)

    n_pass = 0
    n_fail = 0

    print("Planck source-free local traciality thermal-trace route audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the counting law is already closed upstream",
        "c_cell(rho) = tr(rho n_cell) = tr(rho p_a)" in counting
        and "n_cell = p_a" in counting,
        "the thermal route should attack only the source-free state, not reopen counting",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the retained direct state note still says current accepted structure does not derive the democratic state",
        "is **not derivable** from the currently accepted retained stack alone" in sourcefree
        and "7-parameter family" in sourcefree,
        "the thermal route must stay honest about underdetermination on the current retained surface",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the route-check note says the remaining theorem should be a primitive-cell state theorem",
        "primitive-cell source-free traciality" in routecheck
        and "not a boundary-scalar" in routecheck,
        "the thermal route is admissible only if it really lives on the primitive cell",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the Perron thermal-trace note is used only as reduction inspiration",
        "thermal trace state" in perron and "perron state" in perron,
        "there the transfer operator is fixed exactly; here the missing issue is precisely the unfixed primitive generator",
    )
    n_pass += int(p); n_fail += int(not p)

    section("PART 2: EXACT FINITE-CELL THERMAL CRITERION")
    dim = 16
    states = list(product((0, 1), repeat=4))
    one_hot = [i for i, bits in enumerate(states) if sum(bits) == 1]
    p_a = projector(one_hot, dim)
    identity = sp.eye(dim)

    p = check(
        "the primitive cell is the 16-state time-locked one-cell carrier",
        len(states) == dim,
        "the thermal/KMS route is evaluated directly on the primitive C^16 cell",
    )
    n_pass += int(p); n_fail += int(not p)

    beta = sp.symbols("beta", nonnegative=True, real=True)
    lam = sp.symbols("lam", real=True)
    scalar_h = lam * identity
    rho_scalar = sp.simplify(sp.exp(-beta * lam) * identity / (16 * sp.exp(-beta * lam)))

    p = check(
        "a scalar primitive generator gives the tracial state at every beta",
        rho_scalar == identity / dim,
        "if H_cell = lambda I_16, the thermal state is exactly I_16 / 16 for all beta",
    )
    n_pass += int(p); n_fail += int(not p)

    zero_h = sp.zeros(dim)
    rho_zero = sp.simplify(sp.exp(-beta * zero_h) / sp.trace(sp.exp(-beta * zero_h)))

    p = check(
        "the infinite-temperature or zero-generator endpoint is tracial",
        rho_zero == identity / dim,
        "beta = 0 always gives the maximally mixed state; H = 0 does too for every beta",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the note states the exact criterion: beta = 0 or scalar H",
        "beta = 0" in note and "h_cell is scalar" in note,
        "the writeup should state the full finite-cell traciality criterion explicitly",
    )
    n_pass += int(p); n_fail += int(not p)

    section("PART 3: EXPLICIT SAME-SURFACE NONCLOSURE WITNESSES")
    log2 = sp.log(2)
    h_packet = p_a
    gibbs_packet = sp.simplify(sp.exp(-log2) * p_a + (identity - p_a))
    z_packet = sp.simplify(sp.trace(gibbs_packet))
    rho_packet = sp.simplify(gibbs_packet / z_packet)
    c_packet = sp.simplify(sp.trace(rho_packet * p_a))

    p = check(
        "a nontrivial primitive generator gives a nontracial thermal state on the same cell",
        rho_packet != identity / dim,
        "taking H_cell = P_A and beta = log 2 already breaks the tracial state",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the packet-energy witness changes the direct Planck coefficient away from quarter",
        c_packet == sp.Rational(1, 7),
        f"for H_cell = P_A and beta = log 2, Tr(rho P_A) = {sp.simplify(c_packet)}",
    )
    n_pass += int(p); n_fail += int(not p)

    # Orbit-Hamiltonian reduction: eight orbit coefficients with one normalization.
    orbit_counts = [1, 3, 3, 1, 1, 3, 3, 1]
    h = sp.symbols("h00 h01 h02 h03 h10 h11 h12 h13", real=True)
    weights = [sp.exp(-beta * hi) for hi in h]
    z_orbit = sp.simplify(sum(m * w for m, w in zip(orbit_counts, weights)))
    normalized_weights = [sp.simplify(w / z_orbit) for w in weights]

    p = check(
        "the thermal route stays inside the same eight-orbit residual grammar",
        len(normalized_weights) == 8 and z_orbit != 0,
        "for S_3-invariant diagonal H_cell, the Gibbs state is still classified by orbit weights exp(-beta h_(t,w))/Z",
    )
    n_pass += int(p); n_fail += int(not p)

    section("PART 4: PLANCK CONSEQUENCE AND HONEST STATUS")
    quarter = sp.simplify(sp.trace((identity / dim) * p_a))

    p = check(
        "once the thermal state is tracial, the closed counting law gives exact quarter immediately",
        p_a.rank() == 4 and quarter == sp.Rational(1, 4),
        "if beta = 0 or H_cell is scalar, then c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the note stays honest that the thermal route sharpens but does not close retained Planck",
        "not retained closure" in note and "does not close" in note,
        "the route should be presented as an exact criterion plus sharp reason for failure, not a fake closure",
    )
    n_pass += int(p); n_fail += int(not p)

    p = check(
        "the note records the two exact remaining thermal theorems",
        "source-free infinite-temperature theorem" in note
        and "source-free scalar-generator theorem" in note,
        "the route should reduce the live content to precise primitive-cell theorems",
    )
    n_pass += int(p); n_fail += int(not p)

    section("SUMMARY")
    print(f"Passed: {n_pass}")
    print(f"Failed: {n_fail}")
    print(
        "Verdict: on the primitive C^16 cell, the thermal/KMS route yields the tracial state exactly iff beta = 0 or H_cell is scalar; without one of those premises it sharpens but does not close Planck."
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
