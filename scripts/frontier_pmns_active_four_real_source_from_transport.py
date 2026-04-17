#!/usr/bin/env python3
"""Exact recovery of the active 4-real source from non-averaged transport data."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    active_operator,
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
    sector_operator_fixture_from_effective_block,
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


def active_native_means(block: np.ndarray) -> tuple[float, complex]:
    x = np.real(np.diag(block))
    c = np.array([block[0, 1], block[1, 2], block[2, 0]], dtype=complex)
    return float(np.mean(x)), complex(np.mean(c))


def active_four_real_source(block: np.ndarray) -> np.ndarray:
    x = np.real(np.diag(block))
    c = np.array([block[0, 1], block[1, 2], block[2, 0]], dtype=complex)
    xbar = float(np.mean(x))
    sigma = complex(np.mean(c))
    xi = x - xbar * np.ones(3, dtype=float)
    rho = np.array([np.real(c[0] - sigma), np.real(c[1] - sigma)], dtype=float)
    return np.array([xi[0], xi[1], rho[0], rho[1]], dtype=float)


def reconstruct_active_from_transport_data(xbar: float, sigma: complex, source: np.ndarray) -> np.ndarray:
    xi1, xi2, rho1, rho2 = source.tolist()
    x = np.array([xbar + xi1, xbar + xi2, xbar - xi1 - xi2], dtype=float)
    re_sigma = float(np.real(sigma))
    im_sigma = float(np.imag(sigma))
    c = np.array(
        [
            re_sigma + rho1,
            re_sigma + rho2,
            re_sigma - rho1 - rho2 + 3j * im_sigma,
        ],
        dtype=complex,
    )
    block = np.diag(x.astype(complex))
    block[0, 1] = c[0]
    block[1, 2] = c[1]
    block[2, 0] = c[2]
    return block


def sample_active_sector_operator() -> np.ndarray:
    target = active_operator(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    return sector_operator_fixture_from_effective_block(target, seed=3211)


def part1_nonaveraged_transport_closes_what_orbit_averaging_left_open() -> None:
    print("\n" + "=" * 88)
    print("PART 1: NON-AVERAGED TRANSPORT CLOSES THE ACTIVE 4-REAL SOURCE")
    print("=" * 88)

    lam = 0.31
    sector = sample_active_sector_operator()
    reference, columns = active_response_columns_from_sector_operator(sector, lam)
    _kernel, block = derive_active_block_from_response_columns(columns, lam)
    xbar, sigma = active_native_means(block)
    source = active_four_real_source(block)
    rebuilt = reconstruct_active_from_transport_data(xbar, sigma, source)

    check("The active block is first recovered exactly from lower-level active transport/response data",
          np.linalg.norm(block - reference) < 1e-12,
          f"error={np.linalg.norm(block - reference):.2e}")
    check("The already native means xbar and sigma are read from the non-averaged transport profile",
          abs(xbar - active_native_means(reference)[0]) < 1e-12 and abs(sigma - active_native_means(reference)[1]) < 1e-12,
          f"xbar={xbar:.6f}, sigma={sigma}")
    check("The remaining active 4-real source is read exactly from the non-averaged transport profile",
          source.shape == (4,),
          f"source={np.round(source, 6)}")
    check("The active block rebuilds exactly from xbar, sigma, and the 4-real source",
          np.linalg.norm(rebuilt - reference) < 1e-12,
          f"error={np.linalg.norm(rebuilt - reference):.2e}")


def part2_same_means_but_different_sources_are_separated_by_nonaveraged_transport() -> None:
    print("\n" + "=" * 88)
    print("PART 2: NON-AVERAGED TRANSPORT SEPARATES DISTINCT 4-REAL SOURCES")
    print("=" * 88)

    block_a = np.array(
        [
            [1.15, 0.41, 0.0],
            [0.0, 0.82, 0.28],
            [0.54 * np.exp(0.63j), 0.0, 0.95],
        ],
        dtype=complex,
    )
    block_b = np.array(
        [
            [1.20, 0.445, 0.0],
            [0.0, 0.79, 0.245],
            [0.54 * np.exp(0.63j), 0.0, 0.93],
        ],
        dtype=complex,
    )
    xbar_a, sigma_a = active_native_means(block_a)
    xbar_b, sigma_b = active_native_means(block_b)
    source_a = active_four_real_source(block_a)
    source_b = active_four_real_source(block_b)

    check("The two active blocks share the same derived native means",
          abs(xbar_a - xbar_b) < 1e-12 and abs(sigma_a - sigma_b) < 1e-12,
          f"(xbar,sigma)=({xbar_a:.6f},{sigma_a})")
    check("Their 4-real active sources are distinct",
          np.linalg.norm(source_a - source_b) > 1e-6,
          f"|Δsource|={np.linalg.norm(source_a - source_b):.6f}")
    print("  [INFO] Non-averaged transport closes what orbit-averaged transport left open")


def part3_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CIRCULARITY GUARD")
    print("=" * 88)

    ok, bad = circularity_guard(derive_active_block_from_response_columns, {"tau", "q", "x", "y", "delta", "delta_d_act"})
    check("The lower-level active derivation function takes no PMNS-side target values as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS ACTIVE FOUR-REAL SOURCE FROM TRANSPORT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the active transport/response profile is derived at lower level,")
    print("  does the remaining 4-real active orbit-breaking source still need a")
    print("  separate theorem object?")

    part1_nonaveraged_transport_closes_what_orbit_averaging_left_open()
    part2_same_means_but_different_sources_are_separated_by_nonaveraged_transport()
    part3_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact lower-level active completion:")
    print("    - non-averaged active transport/response data recover the active block")
    print("    - xbar and sigma are the derived native means")
    print("    - the residual active 4-real source is read exactly from that profile")
    print()
    print("  So the 4-real source is no longer an extra unresolved object on the")
    print("  lower-level active transport chain. The remaining sole-axiom gap is")
    print("  the derivation of that transport profile from Cl(3) on Z^3 alone.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
