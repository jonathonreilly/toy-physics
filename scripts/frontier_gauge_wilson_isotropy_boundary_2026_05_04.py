#!/usr/bin/env python3
"""Boundary checks for proposed SU(3) gauge-action isotropy mechanisms.

The runner verifies two narrow algebraic facts used by the companion note:

1. The Cl(3) pseudoscalar squares to -I in the Pauli irrep but commutes with
   the three Cl(3) generators, so it cannot by itself be a fourth Clifford
   generator that anticommutes with them.
2. Standard staggered eta-products around all plaquette orientations have the
   same sign, so this sign check does not create a spatial/temporal gauge
   coupling split from an isotropic input lattice.

These are boundary checks, not a derivation of the accepted Wilson surface.
"""

from __future__ import annotations

import itertools

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def staggered_eta(mu: int, x: tuple[int, int, int, int]) -> int:
    if mu == 0:
        return 1
    if mu == 1:
        return (-1) ** x[0]
    if mu == 2:
        return (-1) ** (x[0] + x[1])
    if mu == 3:
        return (-1) ** (x[0] + x[1] + x[2])
    raise ValueError(f"bad direction {mu}")


def eta_plaquette_product(mu: int, nu: int, x: tuple[int, int, int, int]) -> int:
    x_mu = list(x)
    x_mu[mu] += 1
    x_nu = list(x)
    x_nu[nu] += 1
    return (
        staggered_eta(mu, x)
        * staggered_eta(nu, tuple(x_mu))
        * staggered_eta(mu, tuple(x_nu))
        * staggered_eta(nu, x)
    )


def main() -> int:
    print("=" * 78)
    print("GAUGE WILSON ISOTROPY BOUNDARY CHECKS")
    print("=" * 78)

    identity = np.eye(2, dtype=complex)
    generators = [
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    ]

    print("\nPart 1: Cl(3) Pauli-irrep checks")
    for i, gi in enumerate(generators, start=1):
        for j, gj in enumerate(generators, start=1):
            anticomm = gi @ gj + gj @ gi
            expected = 2 * (1 if i == j else 0) * identity
            check(f"{{G_{i}, G_{j}}} = 2 delta_{i}{j}", np.allclose(anticomm, expected))

    pseudoscalar = generators[0] @ generators[1] @ generators[2]
    check("Cl(3) pseudoscalar squares to -I", np.allclose(pseudoscalar @ pseudoscalar, -identity))

    commutators = []
    anticommutators = []
    for i, generator in enumerate(generators, start=1):
        comm = pseudoscalar @ generator - generator @ pseudoscalar
        anticomm = pseudoscalar @ generator + generator @ pseudoscalar
        commutators.append(float(np.max(np.abs(comm))))
        anticommutators.append(float(np.max(np.abs(anticomm))))
        check(f"pseudoscalar commutes with G_{i}", np.allclose(comm, 0.0))
        check(
            f"pseudoscalar does not anticommute with G_{i}",
            not np.allclose(anticomm, 0.0),
            detail=f"max |{{I_cl3, G_{i}}}| = {np.max(np.abs(anticomm)):.3g}",
        )

    check(
        "pseudoscalar is not a standalone fourth Clifford generator for Cl(3,1)",
        max(commutators) < 1e-12 and min(anticommutators) > 1.0,
        detail="it is central in odd-dimensional Cl(3)",
    )

    print("\nPart 2: staggered eta-product orientation check")
    sites = list(itertools.product((0, 1), repeat=4))
    products: dict[tuple[int, int], set[int]] = {}
    for mu, nu in itertools.combinations(range(4), 2):
        values = {eta_plaquette_product(mu, nu, site) for site in sites}
        products[(mu, nu)] = values
        labels = "xyzt"
        print(f"  {labels[mu]}{labels[nu]} values: {sorted(values)}")

    all_values = set().union(*products.values())
    check(
        "all six staggered plaquette orientation products have the same sign",
        all_values == {-1},
        detail=f"orientation value sets = {products}",
    )
    check(
        "the eta-product check supplies no spatial/temporal gauge-coupling split",
        all(values == {-1} for values in products.values()),
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
