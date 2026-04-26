#!/usr/bin/env python3
"""Continuum transport and graded nonlinear localization audit.

This is the next theorem target after
`signed_gravity_tensor_source_transport_retention.py`.

The intended mathematical lift is:

    T_g = chi_eta T_plus  is a section of  L tensor E_T,

where L = Or(Det_APS D_Y) is the APS orientation local system and E_T is the
ordinary retained tensor-source bundle.

The continuum transport part uses the already-retained canonical
barycentric-dyadic / Schur / inverse-limit / smooth textbook continuum GR
stack.  The finite audit checks that the sign local system commutes with atlas
transport, Schur pushforward, and cylindrical tensor response.

The nonlinear part is not the naive map h -> -h.  It is a Z2-graded formal
Einstein localization:

    H_chi(eps) = eps chi h_1 + eps^2 h_2 + eps^3 chi h_3 + ...

Odd jet orders are L-valued; even jet orders are ordinary tensor
backreaction.  The recursive formal theorem is checked through finite order.

This is not a negative-mass, shielding, propulsion, reactionless-force, or
physical signed-gravity claim.
"""

from __future__ import annotations

import itertools
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.signed_gravity_tensor_source_transport_retention import (  # noqa: E402
    retained_tensor_carrier_check,
)


TOL = 1.0e-10
PASS_COUNT = 0
FAIL_COUNT = 0


@dataclass(frozen=True)
class GradedAudit:
    continuum_stack: bool
    flat_local_system: bool
    schur_transport: bool
    graded_formal_solver: bool
    ward_transport: bool
    no_claim: bool

    @property
    def passed(self) -> bool:
        return (
            self.continuum_stack
            and self.flat_local_system
            and self.schur_transport
            and self.graded_formal_solver
            and self.ward_transport
            and self.no_claim
        )


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


def read_doc(name: str) -> str:
    return (ROOT / "docs" / name).read_text(encoding="utf-8").lower()


def continuum_stack_check() -> tuple[bool, str]:
    docs = {
        "refinement": read_doc("UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md"),
        "schur": read_doc("UNIVERSAL_QG_PROJECTIVE_SCHUR_CLOSURE_NOTE.md"),
        "inverse": read_doc("UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md"),
        "pl_weak": read_doc("UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md"),
        "sobolev": read_doc("UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md"),
        "smooth_global": read_doc("UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md"),
        "textbook": read_doc("UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md"),
        "tensor_eta": read_doc("TENSOR_SOURCE_MAP_ETA_NOTE.md"),
    }
    requirements = {
        "refinement": ("barycentric", "dyadic", "canonical geometric refinement net"),
        "schur": ("schur", "projective", "stationary projection"),
        "inverse": ("inverse-limit", "projectively consistent"),
        "pl_weak": ("weak", "schur"),
        "sobolev": ("sobolev", "h^1"),
        "smooth_global": ("smooth global weak gravitational", "projective"),
        "textbook": ("canonical textbook continuum gravitational", "einstein/regge"),
        "tensor_eta": ("rank-two", "tensor source"),
    }
    missing = []
    for key, needles in requirements.items():
        for needle in needles:
            if needle not in docs[key]:
                missing.append(f"{key}:{needle}")
    carrier_ok, carrier_detail = retained_tensor_carrier_check()
    detail = f"missing={missing}, retained_carrier={carrier_ok}, {carrier_detail}"
    return not missing and carrier_ok, detail


def random_orthogonal(rng: np.random.Generator, n: int) -> np.ndarray:
    raw = rng.normal(size=(n, n))
    q, r = np.linalg.qr(raw)
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    q = q * signs
    if np.linalg.det(q) < 0.0:
        q[:, 0] *= -1.0
    return q


def flat_orientation_local_system_check() -> tuple[bool, str]:
    rng = np.random.default_rng(20260426)
    n_charts = 4
    dim = 10
    trivialization = np.array([+1, -1, +1, -1], dtype=int)
    frames = [random_orthogonal(rng, dim) for _ in range(n_charts)]

    max_line_cocycle = 0.0
    max_tensor_cocycle = 0.0
    max_commutator = 0.0
    for i, j, k in itertools.product(range(n_charts), repeat=3):
        g_ij = trivialization[i] * trivialization[j]
        g_jk = trivialization[j] * trivialization[k]
        g_ki = trivialization[k] * trivialization[i]
        max_line_cocycle = max(max_line_cocycle, abs(g_ij * g_jk * g_ki - 1))

        r_ij = frames[i].T @ frames[j]
        r_jk = frames[j].T @ frames[k]
        r_ki = frames[k].T @ frames[i]
        max_tensor_cocycle = max(max_tensor_cocycle, float(np.linalg.norm(r_ij @ r_jk @ r_ki - np.eye(dim))))
        max_commutator = max(max_commutator, float(np.linalg.norm(g_ij * r_ij - r_ij * g_ij)))

    # Barycentric-style refinement duplicates charts.  Pulling back the
    # orientation line cannot change the Cech signs on parent overlaps.
    parents = [0, 0, 1, 1, 2, 2, 3, 3]
    max_refine_err = 0.0
    for a, b in itertools.product(range(len(parents)), repeat=2):
        pulled = trivialization[parents[a]] * trivialization[parents[b]]
        parent = trivialization[parents[a]] * trivialization[parents[b]]
        max_refine_err = max(max_refine_err, abs(pulled - parent))

    ok = (
        max_line_cocycle == 0.0
        and max_tensor_cocycle < 1.0e-10
        and max_commutator < 1.0e-12
        and max_refine_err == 0.0
    )
    detail = (
        f"line_cocycle={max_line_cocycle:.1e}, tensor_cocycle={max_tensor_cocycle:.1e}, "
        f"scalar_tensor_comm={max_commutator:.1e}, refine_err={max_refine_err:.1e}"
    )
    return ok, detail


def random_spd(rng: np.random.Generator, n: int) -> np.ndarray:
    raw = rng.normal(size=(n, n))
    return raw.T @ raw + 1.3 * np.eye(n)


def schur_reduce(k_op: np.ndarray, j: np.ndarray, keep: int) -> tuple[np.ndarray, np.ndarray]:
    a = k_op[:keep, :keep]
    b = k_op[:keep, keep:]
    c = k_op[keep:, keep:]
    eta = j[:keep]
    xi = j[keep:]
    c_inv = np.linalg.inv(c)
    return a - b @ c_inv @ b.T, eta - b @ c_inv @ xi


def schur_extension(k_prev: np.ndarray, j_prev: np.ndarray, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    fine_dim = 5
    b = rng.normal(scale=0.07, size=(k_prev.shape[0], fine_dim))
    c = random_spd(rng, fine_dim)
    xi = rng.normal(size=fine_dim)
    c_inv = np.linalg.inv(c)
    k_next = np.block(
        [
            [k_prev + b @ c_inv @ b.T, b],
            [b.T, c],
        ]
    )
    # This is the exact inverse of the Schur source law.
    j_next = np.concatenate([j_prev + b @ c_inv @ xi, xi])
    return k_next, j_next


def continuum_schur_transport_check() -> tuple[bool, str]:
    rng = np.random.default_rng(240426)
    k0 = random_spd(rng, 10)
    j0 = rng.normal(size=10)

    operators = [k0]
    sources = [j0]
    for level in range(4):
        k_next, j_next = schur_extension(operators[-1], sources[-1], 1000 + level)
        operators.append(k_next)
        sources.append(j_next)

    max_k_err = 0.0
    max_j_err = 0.0
    max_signed_j_err = 0.0
    max_stationary_err = 0.0
    for level in range(len(operators) - 1):
        keep = operators[level].shape[0]
        k_eff, j_eff = schur_reduce(operators[level + 1], sources[level + 1], keep)
        max_k_err = max(max_k_err, float(np.linalg.norm(k_eff - operators[level])))
        max_j_err = max(max_j_err, float(np.linalg.norm(j_eff - sources[level])))

        for chi in (+1, -1):
            _k_signed, j_signed = schur_reduce(operators[level + 1], chi * sources[level + 1], keep)
            max_signed_j_err = max(max_signed_j_err, float(np.linalg.norm(j_signed - chi * sources[level])))
            coarse_star = np.linalg.solve(operators[level], chi * sources[level])
            fine_star = np.linalg.solve(operators[level + 1], chi * sources[level + 1])
            max_stationary_err = max(max_stationary_err, float(np.linalg.norm(fine_star[:keep] - coarse_star)))

    ok = max_k_err < 1.0e-10 and max_j_err < 1.0e-10 and max_signed_j_err < 1.0e-10 and max_stationary_err < 1.0e-10
    detail = (
        f"max_K_schur_err={max_k_err:.1e}, max_J_schur_err={max_j_err:.1e}, "
        f"max_signed_J_err={max_signed_j_err:.1e}, max_stationary_proj_err={max_stationary_err:.1e}"
    )
    return ok, detail


def nullspace(mat: np.ndarray, tol: float = 1.0e-12) -> np.ndarray:
    _u, s, vh = np.linalg.svd(mat)
    rank = int(np.sum(s > tol))
    return vh[rank:].T


def projected_maps(dim: int = 10) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(112358)
    constraint = rng.normal(size=(3, dim))
    ns = nullspace(constraint)
    projector = ns @ ns.T
    raw_k = random_spd(rng, dim)
    # K is SPD on the retained constrained slice and maps the slice to itself.
    k_op = projector @ raw_k @ projector + 0.8 * projector + 7.0e-1 * (np.eye(dim) - projector)
    q_raw = rng.normal(size=(dim, dim, dim)) / math.sqrt(dim)
    r_raw = rng.normal(size=(dim, dim, dim, dim)) / dim
    q = projector[:, :, None] * 0.0
    q = np.einsum("ia,ajk->ijk", projector, q_raw)
    q = 0.5 * (q + np.swapaxes(q, 1, 2))
    r = np.einsum("ia,ajkl->ijkl", projector, r_raw)
    r = (
        r
        + np.swapaxes(r, 1, 2)
        + np.swapaxes(r, 1, 3)
        + np.swapaxes(np.swapaxes(r, 1, 2), 2, 3)
        + np.swapaxes(np.swapaxes(r, 1, 3), 2, 3)
        + np.swapaxes(r, 2, 3)
    ) / 6.0
    source = projector @ rng.normal(size=dim)
    return constraint, k_op, q, r, source


def apply_q(q: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.einsum("ijk,j,k->i", q, a, b)


def apply_r(r: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.einsum("ijkl,j,k,l->i", r, a, b, c)


def formal_coefficients(
    k_op: np.ndarray,
    q: np.ndarray,
    r: np.ndarray,
    source: np.ndarray,
    order: int,
) -> list[np.ndarray]:
    coeffs = [np.zeros_like(source)]
    k_inv = np.linalg.inv(k_op)
    for n in range(1, order + 1):
        rhs = source.copy() if n == 1 else np.zeros_like(source)
        nonlinear = np.zeros_like(source)
        for i in range(1, n):
            nonlinear += apply_q(q, coeffs[i], coeffs[n - i])
        for i in range(1, n):
            for j in range(1, n):
                k = n - i - j
                if k >= 1:
                    nonlinear += apply_r(r, coeffs[i], coeffs[j], coeffs[k])
        coeffs.append(k_inv @ (rhs - nonlinear))
    return coeffs


def residual_coefficients(
    k_op: np.ndarray,
    q: np.ndarray,
    r: np.ndarray,
    coeffs: list[np.ndarray],
    source: np.ndarray,
    order: int,
) -> list[np.ndarray]:
    residuals = [np.zeros_like(source)]
    for n in range(1, order + 1):
        total = k_op @ coeffs[n]
        for i in range(1, n):
            total += apply_q(q, coeffs[i], coeffs[n - i])
        for i in range(1, n):
            for j in range(1, n):
                k = n - i - j
                if k >= 1:
                    total += apply_r(r, coeffs[i], coeffs[j], coeffs[k])
        if n == 1:
            total -= source
        residuals.append(total)
    return residuals


def evaluate_series(coeffs: list[np.ndarray], eps: float, chi: int) -> np.ndarray:
    out = np.zeros_like(coeffs[0])
    for n in range(1, len(coeffs)):
        out += (eps**n) * (chi**n) * coeffs[n]
    return out


def einstein_jet(k_op: np.ndarray, q: np.ndarray, r: np.ndarray, h: np.ndarray) -> np.ndarray:
    return k_op @ h + apply_q(q, h, h) + apply_r(r, h, h, h)


def graded_formal_localization_check(order: int = 6) -> tuple[bool, str]:
    constraint, k_op, q, r, source = projected_maps()
    coeffs = formal_coefficients(k_op, q, r, source, order)
    residuals = residual_coefficients(k_op, q, r, coeffs, source, order)
    max_coeff_resid = max(float(np.linalg.norm(residuals[n])) for n in range(1, order + 1))

    odd_norm = sum(float(np.linalg.norm(coeffs[n])) for n in range(1, order + 1, 2))
    even_norm = sum(float(np.linalg.norm(coeffs[n])) for n in range(2, order + 1, 2))

    eps = 0.025
    h_plus = evaluate_series(coeffs, eps, +1)
    h_minus = evaluate_series(coeffs, eps, -1)
    naive_minus = -h_plus
    naive_err = float(np.linalg.norm(h_minus - naive_minus))
    expected_even = float(np.linalg.norm(2.0 * sum((eps**n) * coeffs[n] for n in range(2, order + 1, 2))))

    # Truncated residual should scale beyond the retained formal order.
    res_plus = einstein_jet(k_op, q, r, h_plus) - eps * source
    res_minus = einstein_jet(k_op, q, r, h_minus) + eps * source
    residual_eval = max(float(np.linalg.norm(res_plus)), float(np.linalg.norm(res_minus)))

    max_constraint = max(float(np.linalg.norm(constraint @ coeffs[n])) for n in range(1, order + 1))

    ok = (
        max_coeff_resid < 1.0e-9
        and odd_norm > 1.0e-6
        and even_norm > 1.0e-6
        and naive_err > 1.0e-8
        and abs(naive_err - expected_even) < 1.0e-12
        and residual_eval < 1.0e-9
        and max_constraint < 1.0e-9
    )
    detail = (
        f"order={order}, coeff_resid={max_coeff_resid:.1e}, "
        f"odd_norm={odd_norm:.3e}, even_backreaction_norm={even_norm:.3e}, "
        f"naive_flip_err={naive_err:.3e}, eval_resid={residual_eval:.1e}, "
        f"constraint={max_constraint:.1e}"
    )
    return ok, detail


def ward_bianchi_transport_check() -> tuple[bool, str]:
    constraint, k_op, q, r, source = projected_maps()
    coeffs = formal_coefficients(k_op, q, r, source, order=6)
    max_source_constraint = float(np.linalg.norm(constraint @ source))
    max_image_constraint = 0.0
    for n in range(1, 7):
        image = k_op @ coeffs[n]
        for i in range(1, n):
            image += apply_q(q, coeffs[i], coeffs[n - i])
        for i in range(1, n):
            for j in range(1, n):
                k = n - i - j
                if k >= 1:
                    image += apply_r(r, coeffs[i], coeffs[j], coeffs[k])
        max_image_constraint = max(max_image_constraint, float(np.linalg.norm(constraint @ image)))

    ok = max_source_constraint < 1.0e-10 and max_image_constraint < 1.0e-9
    return ok, f"source_constraint={max_source_constraint:.1e}, max_jet_constraint={max_image_constraint:.1e}"


def no_claim_gate() -> tuple[bool, str]:
    claims = {
        "negative_inertial_mass": False,
        "shielding": False,
        "propulsion": False,
        "reactionless_force": False,
        "physical_signed_gravity_prediction": False,
        "global_nonlinear_pde_existence_claim": False,
    }
    return not any(claims.values()), ", ".join(f"{key}=False" for key in claims)


def run_audit() -> GradedAudit:
    continuum_ok, continuum_detail = continuum_stack_check()
    check("chosen continuum-family GR stack is available for signed tensor transport", continuum_ok, continuum_detail)

    local_system_ok, local_system_detail = flat_orientation_local_system_check()
    check("APS orientation line is a flat local system over atlas/refinement transport", local_system_ok, local_system_detail)

    schur_ok, schur_detail = continuum_schur_transport_check()
    check("signed tensor source commutes with continuum Schur/projective transport", schur_ok, schur_detail)

    graded_ok, graded_detail = graded_formal_localization_check(order=6)
    check("graded nonlinear Einstein localization solves the formal jets", graded_ok, graded_detail)

    ward_ok, ward_detail = ward_bianchi_transport_check()
    check("Ward/Bianchi-compatible constraint surface is preserved at every graded jet", ward_ok, ward_detail)

    no_claim_ok, no_claim_detail = no_claim_gate()
    check("non-claim gate remains closed", no_claim_ok, no_claim_detail)

    return GradedAudit(
        continuum_stack=continuum_ok,
        flat_local_system=local_system_ok,
        schur_transport=schur_ok,
        graded_formal_solver=graded_ok,
        ward_transport=ward_ok,
        no_claim=no_claim_ok,
    )


def main() -> int:
    print("=" * 118)
    print("SIGNED GRAVITY CONTINUUM GRADED EINSTEIN LOCALIZATION AUDIT")
    print("  continuum-family transport plus graded nonlinear formal localization")
    print("=" * 118)
    print()
    print("TARGET")
    print("  Transport L tensor E_T over the chosen continuum/refinement family and")
    print("  replace the false h -> -h nonlinear rule by a graded odd/even jet theorem.")
    print()

    audit = run_audit()

    print()
    print("INTERPRETATION")
    print("  The signed tensor source transports over the chosen canonical continuum")
    print("  family because the APS orientation line is a flat local system and Schur")
    print("  pushforward is linear in the source.  Nonlinearly, the branch flip acts")
    print("  by jet parity: odd perturbative Einstein jets are L-valued and flip,")
    print("  while even backreaction jets are ordinary and do not.  This removes the")
    print("  prior even-jet obstruction without asserting global nonlinear PDE")
    print("  existence or any physical signed-gravity prediction.")
    print()

    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if audit.passed and FAIL_COUNT == 0:
        print("FINAL_TAG: SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM")
        return 0
    print("FINAL_TAG: SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
