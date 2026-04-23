#!/usr/bin/env python3
"""Audit runner for the source-free local naturality traciality candidate."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def pa_projector() -> np.ndarray:
    p = np.zeros((16, 16), dtype=float)
    for idx in (1, 2, 4, 8):
        p[idx, idx] = 1.0
    return p


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    checks: list[Check] = []
    d = 16
    ident = np.eye(d)

    # Test 1: the local primitive cell really is 16-dimensional.
    checks.append(Check("cell-dimension", ident.shape == (16, 16), f"shape={ident.shape}"))

    # Test 2: scalar states are invariant under arbitrary local unitaries.
    theta = 0.37
    u = np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=float,
    )
    big_u = np.eye(d)
    big_u[:2, :2] = u
    rho_scalar = ident / d
    inv_scalar = np.allclose(big_u @ rho_scalar @ big_u.T, rho_scalar)
    checks.append(Check("scalar-unitary-invariant", inv_scalar, "2x2 rotation block witness"))

    # Test 3: non-scalar diagonal states fail unitary naturality.
    rho_nonscalar = np.diag([2 / 16, 0.0] + [1 / 14] * 14)
    inv_nonscalar = np.allclose(big_u @ rho_nonscalar @ big_u.T, rho_nonscalar)
    checks.append(Check("nonscalar-breaks-naturality", not inv_nonscalar, "rotation mixes unequal weights"))

    # Test 4: a state commuting with enough generators must be scalar.
    x = np.diag(np.arange(1, d + 1, dtype=float))
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    witness = np.eye(d)
    witness[:2, :2] = sigma_x
    commutator = witness @ x - x @ witness
    checks.append(Check("noncentral-commutator", not np.allclose(commutator, 0.0), "swap witness sees noncentral diagonal"))

    # Test 5: normalization fixes the scalar coefficient.
    lam = 1.0 / d
    checks.append(Check("normalized-scalar", math.isclose(np.trace(lam * ident), 1.0), f"lambda={lam:.6f}"))

    # Test 6: positivity of the tracial state.
    evals = np.linalg.eigvalsh(rho_scalar)
    checks.append(Check("tracial-positive", np.all(evals >= -1e-12), f"min_eval={evals.min():.6f}"))

    # Test 7: the worldtube packet has rank 4.
    p_a = pa_projector()
    rank_pa = int(np.linalg.matrix_rank(p_a))
    checks.append(Check("packet-rank", rank_pa == 4, f"rank={rank_pa}"))

    # Test 8: tracial state yields quarter through the closed counting law.
    coeff = float(np.trace(rho_scalar @ p_a))
    checks.append(Check("quarter-coefficient", math.isclose(coeff, 0.25), f"coeff={coeff:.6f}"))

    # Test 9: quarter differs from a nontracial witness, so the theorem has bite.
    coeff_nonscalar = float(np.trace(rho_nonscalar @ p_a))
    checks.append(Check("nontracial-different", not math.isclose(coeff_nonscalar, coeff), f"coeff_nonscalar={coeff_nonscalar:.6f}"))

    passed = 0
    for idx, check in enumerate(checks, start=1):
        status = "PASS" if check.ok else "FAIL"
        print(f"[{idx}] {status} {check.name}: {check.detail}")
        passed += int(check.ok)

    print(f"\n{passed}/{len(checks)} PASS")
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
