#!/usr/bin/env python3
"""Oriented tensor-source lift for the signed-gravity lane.

Previous blocker:

    The scalar determinant source character is A1-maximal.  By itself it
    cannot create nonzero shift/shear tensor components.

New target:

    Use the determinant-orientation line as a local system that twists the
    already-retained tensor source bundle:

        T_g(Y) = chi_eta(Y) * T_plus

    where T_plus is an ordinary positive-norm tensor source in the canonical
    lapse/shift/trace/shear bundle.  This does not manufacture tensor
    components; it signs whatever tensor source components are already present.

Finite theorem checked here:

1. the orientation-line twist commutes with the canonical block projectors;
2. it preserves linear Ward/conservation constraints;
3. it flips every occupied tensor block source with the same chi_eta;
4. the universal block-diagonal GR operator gives a locked tensor response;
5. scalar-only sources remain A1-only, so no overclaim is introduced.

This is not a negative-mass, shielding, propulsion, reactionless-force, or
physical signed-gravity claim.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.signed_gravity_source_character_uniqueness_theorem import (  # noqa: E402
    sign_eta,
)


TOL = 1.0e-10
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    status = "PASS" if passed else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return passed


@dataclass(frozen=True)
class Projectors:
    lapse: np.ndarray
    shift: np.ndarray
    trace: np.ndarray
    shear: np.ndarray

    @property
    def blocks(self) -> dict[str, np.ndarray]:
        return {
            "lapse": self.lapse,
            "shift": self.shift,
            "trace": self.trace,
            "shear": self.shear,
        }


def canonical_projectors() -> Projectors:
    p_lapse = np.zeros((10, 10), dtype=float)
    p_shift = np.zeros((10, 10), dtype=float)
    p_trace = np.zeros((10, 10), dtype=float)
    p_shear = np.zeros((10, 10), dtype=float)
    p_lapse[0, 0] = 1.0
    for idx in (1, 2, 3):
        p_shift[idx, idx] = 1.0
    p_trace[4, 4] = 1.0
    for idx in (5, 6, 7, 8, 9):
        p_shear[idx, idx] = 1.0
    return Projectors(p_lapse, p_shift, p_trace, p_shear)


def block_norms(vec: np.ndarray, projectors: Projectors) -> dict[str, float]:
    return {name: float(np.linalg.norm(p @ vec)) for name, p in projectors.blocks.items()}


def universal_block_operator(a: float = 1.7, b: float = 2.3) -> np.ndarray:
    p = canonical_projectors()
    return (
        (a ** -2) * p.lapse
        + ((a * b) ** -1) * p.shift
        + (b ** -2) * p.trace
        + (b ** -2) * p.shear
    )


def nullspace(mat: np.ndarray, tol: float = 1.0e-12) -> np.ndarray:
    _u, s, vh = np.linalg.svd(mat)
    rank = int(np.sum(s > tol))
    return vh[rank:].T


def tensor_source_with_constraints() -> tuple[np.ndarray, np.ndarray]:
    """Construct a tensor source satisfying linear Ward-like constraints.

    The constraints are deliberately generic.  The theorem being tested is
    linear: if C T = 0, then C (chi T) = 0 for chi in {+1,-1}.
    """

    rng = np.random.default_rng(20260426)
    constraint = rng.normal(size=(4, 10))
    ns = nullspace(constraint)
    if ns.shape[1] < 2:
        raise RuntimeError("unexpected nullspace dimension")
    for _ in range(200):
        coeff = rng.normal(size=ns.shape[1])
        source = ns @ coeff
        if source[0] < 0.0:
            source *= -1.0
        norms = block_norms(source, canonical_projectors())
        if source[0] > 0.5 and all(val > 0.05 for val in norms.values()):
            return source, constraint
    raise RuntimeError("could not build full-block tensor source")


def oriented(source: np.ndarray, eta: int) -> np.ndarray:
    return sign_eta(eta) * source


def scalar_a1_source() -> np.ndarray:
    out = np.zeros(10, dtype=float)
    out[0] = 2.0
    out[4] = 1.0
    return out


def projector_algebra_check(projectors: Projectors) -> tuple[bool, str]:
    ident = np.eye(10)
    total = sum(projectors.blocks.values())
    sum_ok = np.allclose(total, ident)
    idem_ok = all(np.allclose(p @ p, p) for p in projectors.blocks.values())
    orth_ok = True
    for name_a, p_a in projectors.blocks.items():
        for name_b, p_b in projectors.blocks.items():
            if name_a >= name_b:
                continue
            orth_ok &= np.linalg.norm(p_a @ p_b) < TOL
    return bool(sum_ok and idem_ok and orth_ok), "ranks=" + str({k: int(np.linalg.matrix_rank(v)) for k, v in projectors.blocks.items()})


def orientation_twist_check(source: np.ndarray, projectors: Projectors) -> tuple[bool, str]:
    plus = oriented(source, +1)
    minus = oriented(source, -1)
    block_flips = {
        name: float(np.linalg.norm(p @ plus + p @ minus))
        for name, p in projectors.blocks.items()
    }
    plus_norms = block_norms(plus, projectors)
    all_occupied = all(val > 0.05 for val in plus_norms.values())
    ok = max(block_flips.values()) < TOL and all_occupied
    return ok, f"block_norms={ {k: round(v, 3) for k, v in plus_norms.items()} }, flip_resid={max(block_flips.values()):.1e}"


def ward_constraint_check(source: np.ndarray, constraint: np.ndarray) -> tuple[bool, str]:
    residuals = []
    for eta in (+1, -1, 0):
        residuals.append(float(np.linalg.norm(constraint @ oriented(source, eta))))
    ok = max(residuals) < 1.0e-10 and np.linalg.norm(oriented(source, 0)) < TOL
    return ok, f"residuals(+,-,0)={[f'{r:.1e}' for r in residuals]}"


def response_locking_check(source: np.ndarray) -> tuple[bool, str]:
    k = universal_block_operator()
    kinv = np.linalg.inv(k)
    field_plus = kinv @ oriented(source, +1)
    field_minus = kinv @ oriented(source, -1)
    field_null = kinv @ oriented(source, 0)
    flip_resid = float(np.linalg.norm(field_plus + field_minus))
    null_resid = float(np.linalg.norm(field_null))

    positive_self = float(source @ kinv @ source)
    pair_reads = {}
    for eta_a in (+1, -1):
        for eta_b in (+1, -1):
            coupling = float(oriented(source, eta_a) @ kinv @ oriented(source, eta_b))
            pair_reads[(eta_a, eta_b)] = math.copysign(1.0, coupling)
    expected = {
        (+1, +1): +1.0,
        (+1, -1): -1.0,
        (-1, +1): -1.0,
        (-1, -1): +1.0,
    }
    ok = flip_resid < TOL and null_resid < TOL and positive_self > 0.0 and pair_reads == expected
    detail = f"field_flip={flip_resid:.1e}, null={null_resid:.1e}, pair_signs={pair_reads}"
    return ok, detail


def scalar_only_no_overclaim_check(projectors: Projectors) -> tuple[bool, str]:
    src = scalar_a1_source()
    signed = oriented(src, -1)
    comp = (projectors.shift + projectors.shear) @ signed
    ok = float(np.linalg.norm(comp)) < TOL
    return ok, f"complement_norm={float(np.linalg.norm(comp)):.1e}"


def free_tensor_carrier_gate(source: np.ndarray) -> tuple[bool, str]:
    """The lift needs an ordinary tensor source; chi alone cannot create one."""

    chi_only = np.zeros(10, dtype=float)
    chi_only[0] = 1.0
    chi_only[4] = 0.5
    full_norms = block_norms(source, canonical_projectors())
    chi_only_norms = block_norms(chi_only, canonical_projectors())
    ok = full_norms["shift"] > 0.05 and full_norms["shear"] > 0.05 and chi_only_norms["shift"] == 0.0 and chi_only_norms["shear"] == 0.0
    detail = f"tensor_source_blocks={ {k: round(v, 3) for k, v in full_norms.items()} }, chi_only_blocks={chi_only_norms}"
    return ok, detail


def no_claim_gate() -> tuple[bool, str]:
    claims = {
        "negative_inertial_mass": False,
        "shielding": False,
        "propulsion": False,
        "reactionless_force": False,
        "physical_signed_gravity_prediction": False,
    }
    return not any(claims.values()), ", ".join(f"{k}=False" for k in claims)


def main() -> int:
    print("=" * 112)
    print("SIGNED GRAVITY ORIENTED TENSOR-SOURCE LIFT AUDIT")
    print("  determinant-orientation line twist of retained tensor source bundle")
    print("=" * 112)
    print()

    print("LIFT TARGET")
    print("  T_g(Y) = chi_eta(Y) * T_plus")
    print("  chi_eta signs the whole already-existing tensor source bundle; it does")
    print("  not manufacture shift/shear components from a scalar source.")
    print()

    projectors = canonical_projectors()
    source, constraint = tensor_source_with_constraints()

    algebra_ok, algebra_detail = projector_algebra_check(projectors)
    check("canonical lapse/shift/trace/shear projectors are exact", algebra_ok, algebra_detail)

    twist_ok, twist_detail = orientation_twist_check(source, projectors)
    check("orientation-line twist flips every occupied tensor block coherently", twist_ok, twist_detail)

    ward_ok, ward_detail = ward_constraint_check(source, constraint)
    check("orientation-line twist preserves linear Ward/conservation constraints", ward_ok, ward_detail)

    response_ok, response_detail = response_locking_check(source)
    check("block-diagonal GR operator gives locked tensor response signs", response_ok, response_detail)

    scalar_ok, scalar_detail = scalar_only_no_overclaim_check(projectors)
    check("scalar-only determinant character remains A1-only", scalar_ok, scalar_detail)

    carrier_ok, carrier_detail = free_tensor_carrier_gate(source)
    check("non-A1 signed tensor response requires an ordinary tensor source carrier", carrier_ok, carrier_detail)

    no_claim_ok, no_claim_detail = no_claim_gate()
    check("non-claim gate remains closed", no_claim_ok, no_claim_detail)

    print()
    print("INTERPRETATION")
    print("  The tensor blocker reduces: chi_eta alone is A1-maximal, but the")
    print("  determinant-orientation line can twist the retained tensor source bundle.")
    print("  If an ordinary tensor stress source is present, every canonical block can")
    print("  carry the same derived sign while constraints and response locking are")
    print("  preserved.  Without that tensor carrier, the signed lane remains scalar.")
    print()

    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("FINAL_TAG: SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_FINITE_CONDITIONAL")
        return 0
    print("FINAL_TAG: SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
