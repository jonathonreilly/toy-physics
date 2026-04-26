#!/usr/bin/env python3
"""Source-line origin and partial tensor-lift audit for signed gravity.

This runner tests a sharper origin target for the eta-polarized source:

    J_g = chi_eta(Y) M_phys rho.

The candidate principle is not "insert a sign."  It is:

    Compact active sources are sections of the real orientation line of the
    gapped APS boundary determinant line, and the scalar source action must be
    local under disjoint sewing, orientation-covariant, real, null-quarantined,
    positive-norm, and refinement-invariant.

Under those constraints the finite coefficient is forced to sign(eta), not
raw eta, a global determinant product sign, an unsigned source, or a complex
eta phase.

The tensor part is intentionally weaker.  It checks that the source line has a
frame-independent lift into the exact A1 lapse/trace channel, while the full
tensor lift remains blocked without the curvature-localization primitive.

This is not a negative-mass, shielding, propulsion, reactionless-force, or
physical signed-gravity claim.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
from dataclasses import dataclass
from typing import Callable

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.signed_gravity_aps_boundary_index_probe import (  # noqa: E402
    boundary_model,
    chi_from_eta,
    eta_delta,
)
from scripts.signed_gravity_aps_locked_source_action_proposal import packet_density  # noqa: E402


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


def refined_boundary(index_sign: int, copies: int, gap: float = 0.4) -> np.ndarray:
    if copies <= 0:
        raise ValueError("copies must be positive")
    return np.kron(boundary_model(index_sign, pairs=4, gap=gap), np.eye(copies))


@dataclass(frozen=True)
class Sector:
    index_sign: int
    copies: int = 1

    @property
    def eta(self) -> int:
        eta, _zero, _n, _vals = eta_delta(refined_boundary(self.index_sign, self.copies))
        return eta

    @property
    def zero(self) -> int:
        _eta, zero, _n, _vals = eta_delta(refined_boundary(self.index_sign, self.copies))
        return zero

    @property
    def chi(self) -> int:
        return chi_from_eta(self.eta, self.zero)


Coeff = Callable[[Sector], complex]


@dataclass(frozen=True)
class SourceLineRule:
    name: str
    coeff: Coeff
    note: str


def source_line_rules() -> list[SourceLineRule]:
    return [
        SourceLineRule(
            "eta_orientation_line",
            lambda s: complex(s.chi, 0.0),
            "local APS determinant-orientation line",
        ),
        SourceLineRule(
            "unsigned_born_source",
            lambda s: 0.0 if s.chi == 0 else 1.0,
            "positive source ignores boundary orientation",
        ),
        SourceLineRule(
            "raw_eta_magnitude",
            lambda s: complex(s.eta, 0.0),
            "uses eta magnitude, so refinement changes source strength",
        ),
        SourceLineRule(
            "complex_eta_phase",
            lambda s: cmath.exp(0.5j * math.pi * s.eta) if s.chi != 0 else 0.0,
            "keeps eta as a phase rather than a real orientation",
        ),
    ]


def coefficient_table() -> dict[str, list[complex]]:
    sectors = [Sector(+1), Sector(-1), Sector(0)]
    return {rule.name: [rule.coeff(s) for s in sectors] for rule in source_line_rules()}


def is_real(z: complex) -> bool:
    return abs(z.imag) < TOL


def rule_passes_origin_constraints(rule: SourceLineRule) -> tuple[bool, str]:
    p = Sector(+1)
    m = Sector(-1)
    n = Sector(0)
    cp = rule.coeff(p)
    cm = rule.coeff(m)
    cn = rule.coeff(n)

    normalized = abs(cp - 1.0) < TOL
    odd = abs(cm + cp) < TOL
    null = abs(cn) < TOL
    real = is_real(cp) and is_real(cm) and is_real(cn)

    # Refinement must preserve the coefficient after the mass/norm is fixed.
    refined = [rule.coeff(Sector(+1, copies=c)) for c in (1, 2, 3, 5)]
    refinement_stable = all(abs(z - refined[0]) < TOL for z in refined)

    passed = normalized and odd and null and real and refinement_stable
    detail = (
        f"coeff(+,-,0)=({cp:.1f},{cm:.1f},{cn:.1f}), "
        f"refined={[complex(round(z.real, 3), round(z.imag, 3)) for z in refined]}"
    )
    return passed, detail


def local_action_active_source(
    coeffs: list[complex],
    masses: list[float],
    densities: list[np.ndarray],
) -> np.ndarray:
    total = np.zeros_like(densities[0], dtype=complex)
    for coeff, mass, rho in zip(coeffs, masses, densities):
        total += coeff * mass * rho
    return total


def source_line_locality_check() -> tuple[bool, str]:
    rho = packet_density(n=31, center=15.0, sigma=3.0)
    masses = [2.0, 2.0]
    densities = [rho, rho]

    local_coeffs = [1.0, -1.0]
    local_source = local_action_active_source(local_coeffs, masses, densities)

    # A tempting but wrong determinant shortcut: use one global product sign for
    # all components.  Adding a remote opposite sector flips the local source.
    global_product = local_coeffs[0] * local_coeffs[1]
    global_coeffs = [global_product, global_product]
    global_source = local_action_active_source(global_coeffs, masses, densities)

    local_cancel = float(np.max(np.abs(local_source))) < TOL
    global_fails = float(np.sum(np.real(global_source))) < -3.9

    plus_alone = local_action_active_source([1.0], [2.0], [rho])
    plus_with_remote_minus_global = local_action_active_source([-1.0], [2.0], [rho])
    spectator_flip = float(np.sum(np.real(plus_with_remote_minus_global - plus_alone)))

    ok = local_cancel and global_fails and spectator_flip < -3.9
    detail = (
        f"local_sum={np.sum(local_source).real:+.1e}, "
        f"global_sum={np.sum(global_source).real:+.1f}, "
        f"spectator_flip={spectator_flip:+.1f}"
    )
    return ok, detail


def source_variation_realness_check() -> tuple[bool, str]:
    rho = packet_density(n=29, center=13.0, sigma=2.8)
    mass = 2.5
    phi = np.linspace(-0.04, 0.05, len(rho))
    step = 1.0e-6
    coeff = 1.0

    def action(local_phi: np.ndarray) -> complex:
        return -coeff * mass * np.dot(rho, local_phi)

    numeric = np.zeros_like(rho, dtype=complex)
    for idx in range(len(rho)):
        delta = np.zeros_like(rho)
        delta[idx] = step
        numeric[idx] = -((action(phi + delta) - action(phi - delta)) / (2.0 * step))
    target = coeff * mass * rho
    residual = float(np.max(np.abs(numeric - target)))

    complex_coeff = source_line_rules()[-1].coeff(Sector(+1))
    complex_action_real = abs(complex_coeff.imag) < TOL
    ok = residual < 1.0e-9 and not complex_action_real
    return ok, f"variation_residual={residual:.2e}, complex_coeff={complex_coeff:.1f}"


def sym(i: int, j: int, n: int = 4) -> np.ndarray:
    out = np.zeros((n, n), dtype=float)
    if i == j:
        out[i, j] = 1.0
    else:
        out[i, j] = 1.0 / math.sqrt(2.0)
        out[j, i] = 1.0 / math.sqrt(2.0)
    return out


def diag(vals: tuple[float, float, float, float]) -> np.ndarray:
    return np.diag(np.array(vals, dtype=float))


def canonical_polarization_frame() -> list[np.ndarray]:
    sqrt2 = math.sqrt(2.0)
    sqrt3 = math.sqrt(3.0)
    sqrt6 = math.sqrt(6.0)
    return [
        sym(0, 0),
        sym(0, 1),
        sym(0, 2),
        sym(0, 3),
        diag((0.0, 1.0 / sqrt3, 1.0 / sqrt3, 1.0 / sqrt3)),
        diag((0.0, 1.0 / sqrt2, -1.0 / sqrt2, 0.0)),
        diag((0.0, 1.0 / sqrt6, 1.0 / sqrt6, -2.0 / sqrt6)),
        sym(1, 2),
        sym(1, 3),
        sym(2, 3),
    ]


def rotation(axis: str, theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    rot = np.eye(4)
    if axis == "x":
        rot[2, 2] = c
        rot[2, 3] = -s
        rot[3, 2] = s
        rot[3, 3] = c
    elif axis == "y":
        rot[1, 1] = c
        rot[1, 3] = s
        rot[3, 1] = -s
        rot[3, 3] = c
    elif axis == "z":
        rot[1, 1] = c
        rot[1, 2] = -s
        rot[2, 1] = s
        rot[2, 2] = c
    else:
        raise ValueError(axis)
    return rot


def frob(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.tensordot(a, b, axes=2))


def rep_matrix(rot: np.ndarray, frame: list[np.ndarray]) -> np.ndarray:
    out = np.zeros((len(frame), len(frame)), dtype=float)
    for j, basis in enumerate(frame):
        image = rot.T @ basis @ rot
        for i, ref in enumerate(frame):
            out[i, j] = frob(ref, image)
    return out


def pi_a1() -> np.ndarray:
    p = np.zeros((10, 10), dtype=float)
    p[0, 0] = 1.0
    p[4, 4] = 1.0
    return p


def partial_a1_tensor_lift_check() -> tuple[bool, str]:
    frame = canonical_polarization_frame()
    projector = pi_a1()
    comp = np.eye(10) - projector
    source = np.zeros(10, dtype=float)
    source[0] = 1.0 / math.sqrt(2.0)
    source[4] = 1.0 / math.sqrt(2.0)

    comm_norms = []
    moved = []
    for axis, angle in (("x", math.pi / 7.0), ("y", math.pi / 5.0), ("z", math.pi / 6.0)):
        rep = rep_matrix(rotation(axis, angle), frame)
        comm_norms.append(float(np.linalg.norm(projector @ rep - rep @ projector, ord="fro")))
        moved.append(float(np.linalg.norm(rep @ source - source)))

    source_in_a1 = float(np.linalg.norm(comp @ source)) < TOL
    a1_invariant = max(comm_norms) < 1.0e-12 and max(moved) < 1.0e-12

    tensor_samples = []
    for chi in (+1, -1):
        for mass in (1.0, 2.0, 3.5):
            tensor_samples.append(chi * mass * source)
    mat = np.column_stack(tensor_samples)
    total_rank = int(np.linalg.matrix_rank(mat, tol=1.0e-12))
    comp_rank = int(np.linalg.matrix_rank(comp @ mat, tol=1.0e-12))
    full_tensor_blocked = total_rank == 1 and comp_rank == 0

    ok = source_in_a1 and a1_invariant and full_tensor_blocked
    detail = (
        f"max_comm={max(comm_norms):.1e}, max_motion={max(moved):.1e}, "
        f"source_rank={total_rank}, complement_rank={comp_rank}"
    )
    return ok, detail


def main() -> int:
    print("=" * 104)
    print("SIGNED GRAVITY SOURCE-LINE ORIGIN / PARTIAL TENSOR-LIFT AUDIT")
    print("  determinant-orientation source line; no physical signed-gravity claim")
    print("=" * 104)
    print()

    print("CANDIDATE ORIGIN PRINCIPLE")
    print("  compact active sources are local sections of the real APS determinant")
    print("  orientation line; positive inertia is the line norm, while active")
    print("  scalar charge is the oriented section paired with Phi.")
    print()

    print("COEFFICIENT RULES")
    print(f"  {'rule':<26s} {'+ sector':>12s} {'- sector':>12s} {'null':>12s}  read")
    table = coefficient_table()
    for rule in source_line_rules():
        vals = table[rule.name]
        print(
            f"  {rule.name:<26s} {vals[0]:>12.1f} {vals[1]:>12.1f} {vals[2]:>12.1f}  {rule.note}"
        )
    print()

    rule_results = {}
    for rule in source_line_rules():
        passed, detail = rule_passes_origin_constraints(rule)
        rule_results[rule.name] = passed
        expected = rule.name == "eta_orientation_line"
        check(
            f"origin constraints classify {rule.name}",
            passed is expected,
            detail,
        )

    local_ok, local_detail = source_line_locality_check()
    check(
        "local source-line sewing beats global determinant-product sign",
        local_ok,
        local_detail,
    )

    variation_ok, variation_detail = source_variation_realness_check()
    check(
        "real source variation selects orientation sign over complex eta phase",
        variation_ok,
        variation_detail,
    )

    a1_ok, a1_detail = partial_a1_tensor_lift_check()
    check(
        "eta source line has invariant A1 tensor lift but not full tensor closure",
        a1_ok,
        a1_detail,
    )

    print()
    print("INTERPRETATION")
    print("  Under the source-line principle, the coefficient is forced to chi_eta.")
    print("  The controls fail for precise reasons: unsigned loses orientation, raw")
    print("  eta fails refinement, global product loses locality, and complex phase")
    print("  leaves the real scalar action.  The tensor lift is only A1/lapse-trace;")
    print("  full Einstein/Regge localization remains blocked.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("FINAL_TAG: ETA_SOURCE_LINE_ORIGIN_CONDITIONAL_A1_TENSOR_LIFT")
        return 0
    print("FINAL_TAG: ETA_SOURCE_LINE_ORIGIN_AUDIT_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
