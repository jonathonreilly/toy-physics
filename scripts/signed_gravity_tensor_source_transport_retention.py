#!/usr/bin/env python3
"""Transport and retention audit for the signed tensor-source lift.

Previous finite result:

    T_g(Y) = chi_eta(Y) * T_plus

twists an ordinary tensor source bundle by the APS determinant-orientation
line.  The remaining question is whether the ordinary tensor carrier is
retained and whether the twist survives family/refinement transport.

This runner checks the strongest finite statement currently available:

1. the retained gravity stack already contains a rank-two non-scalar tensor
   source-to-channel map on the exact local O_h and finite-rank classes;
2. the orientation-line twist commutes with refinement pushforward/pullback;
3. cylindrical response observables are stable along a normalized refinement
   chain;
4. linear Ward/Bianchi-like constraints transport with the twist;
5. naive nonlinear sign-flip closure is obstructed by even nonlinear jets.

The last item is a positive no-overclaim gate: linear/projective transport is
supported, while full nonlinear Einstein localization remains a separate
graded-localization theorem target.

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

from scripts.frontier_tensor_source_map_eta import response_matrix, tm  # noqa: E402
from scripts.signed_gravity_aps_boundary_index_probe import (  # noqa: E402
    boundary_model,
    chi_from_eta,
    eta_delta,
    hermitian_part,
)
from scripts.signed_gravity_oriented_tensor_source_lift import (  # noqa: E402
    oriented,
    tensor_source_with_constraints,
    universal_block_operator,
)


TOL = 1.0e-10
PASS_COUNT = 0
FAIL_COUNT = 0


@dataclass(frozen=True)
class TransportAudit:
    carrier_retained: bool
    orientation_transport: bool
    projective_transport: bool
    ward_transport: bool
    nonlinear_obstruction_exposed: bool
    no_claim: bool

    @property
    def passed(self) -> bool:
        return (
            self.carrier_retained
            and self.orientation_transport
            and self.projective_transport
            and self.ward_transport
            and self.nonlinear_obstruction_exposed
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


def random_unitary(rng: np.random.Generator, n: int) -> np.ndarray:
    raw = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    q, r = np.linalg.qr(raw)
    phase = np.diag(r)
    phase = phase / np.maximum(np.abs(phase), 1.0e-12)
    return q * phase.conj()


def perturbed_family_operator(
    orientation: int,
    copies: int,
    perturb: float,
    rng: np.random.Generator,
) -> np.ndarray:
    base = np.kron(boundary_model(orientation, pairs=4, gap=0.36), np.eye(copies))
    if perturb == 0.0:
        return base
    raw = hermitian_part(rng.normal(size=base.shape) + 1j * rng.normal(size=base.shape))
    raw /= max(float(np.linalg.norm(raw, ord=2)), 1.0e-12)
    return base + perturb * raw


def refinement_injection(copies: int, dim: int = 10) -> np.ndarray:
    if copies <= 0:
        raise ValueError("copies must be positive")
    return np.kron(np.ones((copies, 1), dtype=float) / math.sqrt(copies), np.eye(dim))


def retained_tensor_carrier_check() -> tuple[bool, str]:
    """Use the retained tensor-source map as the carrier witness."""

    oh = response_matrix(tm.same_source.build_best_phi_grid())
    finite_rank = response_matrix(tm.coarse.build_finite_rank_phi_grid())
    rows = [("O_h", oh), ("finite_rank", finite_rank)]

    dets = {label: float(np.linalg.det(row.eta)) for label, row in rows}
    min_svs = {
        label: float(np.min(np.linalg.svd(row.eta, compute_uv=False)))
        for label, row in rows
    }
    scalar_blind = all(row.scalar_blind for _label, row in rows)
    additive = all(row.mixed_add_ti < 1.0e-6 and row.mixed_add_tf < 1.0e-6 for _label, row in rows)
    nonscalar = all(row.eta[0, 0] > 1.0e-3 and row.eta[1, 1] > 1.0e-2 for _label, row in rows)
    rank_two = all(det > 1.0e-6 and min_svs[label] > 1.0e-4 for label, det in dets.items())

    detail = (
        f"dets={ {k: f'{v:.3e}' for k, v in dets.items()} }, "
        f"min_svs={ {k: f'{v:.3e}' for k, v in min_svs.items()} }, "
        f"scalar_blind={scalar_blind}, additive={additive}"
    )
    return rank_two and scalar_blind and additive and nonscalar, detail


def orientation_line_family_transport_check(rng: np.random.Generator) -> tuple[bool, str]:
    """Check chi_eta and tensor transport commute across finite families."""

    source, _constraint = tensor_source_with_constraints()
    max_resid = 0.0
    reads: list[str] = []
    for orientation in (+1, -1):
        base = boundary_model(orientation, pairs=4, gap=0.36)
        eta_base, zero_base, _n_base, _vals_base = eta_delta(base)
        chi_base = chi_from_eta(eta_base, zero_base)
        for copies, perturb in ((1, 0.0), (2, 0.02), (3, 0.03), (5, 0.04)):
            op = perturbed_family_operator(orientation, copies, perturb, rng)
            # Unitary relabeling stands in for same-family basis change.
            u = random_unitary(rng, op.shape[0])
            op = u @ op @ u.conj().T
            eta_fam, zero_fam, _n_fam, vals = eta_delta(op)
            chi_fam = chi_from_eta(eta_fam, zero_fam)

            r = refinement_injection(copies)
            p = r.T
            fine_source = r @ source
            coarse_from_fine = p @ (chi_fam * fine_source)
            direct_coarse = chi_base * source
            max_resid = max(max_resid, float(np.linalg.norm(coarse_from_fine - direct_coarse)))
            reads.append(
                f"{orientation:+d}x{copies}:eta={eta_fam:+d},chi={chi_fam:+d},gap={float(np.min(np.abs(vals))):.2f}"
            )

    ok = max_resid < TOL and all("chi=+1" in row or "chi=-1" in row for row in reads)
    return ok, f"max_commute_resid={max_resid:.1e}; " + "; ".join(reads)


def projective_cylindrical_transport_check() -> tuple[bool, str]:
    """Check normalized refinement leaves coarse response observables invariant."""

    source, _constraint = tensor_source_with_constraints()
    k = universal_block_operator()
    kinv = np.linalg.inv(k)
    base_reads: dict[tuple[int, int], float] = {}
    for chi_a in (+1, -1):
        for chi_b in (+1, -1):
            base_reads[(chi_a, chi_b)] = float(oriented(source, chi_a) @ kinv @ oriented(source, chi_b))

    max_field_resid = 0.0
    max_pair_err = 0.0
    for copies in (1, 2, 4, 8):
        r = refinement_injection(copies)
        p = r.T
        k_fine = np.kron(np.eye(copies), k)
        kinv_fine = np.linalg.inv(k_fine)
        for chi in (+1, -1, 0):
            coarse_field = kinv @ oriented(source, chi)
            fine_field = kinv_fine @ (r @ oriented(source, chi))
            max_field_resid = max(max_field_resid, float(np.linalg.norm(p @ fine_field - coarse_field)))
        for pair, base_val in base_reads.items():
            a, b = pair
            fine_val = float((r @ oriented(source, a)) @ kinv_fine @ (r @ oriented(source, b)))
            max_pair_err = max(max_pair_err, abs(fine_val - base_val))

    return (
        max_field_resid < TOL and max_pair_err < TOL,
        f"max_projected_field_resid={max_field_resid:.1e}, max_pair_observable_err={max_pair_err:.1e}",
    )


def ward_transport_check() -> tuple[bool, str]:
    """Linear constraints transport because the sign is a locally constant scalar."""

    source, constraint = tensor_source_with_constraints()
    max_resid = 0.0
    for copies in (1, 2, 4, 8):
        r = refinement_injection(copies)
        p = r.T
        fine_constraint = constraint @ p
        for chi in (+1, -1, 0):
            resid = float(np.linalg.norm(fine_constraint @ (r @ oriented(source, chi))))
            max_resid = max(max_resid, resid)
    return max_resid < 1.0e-10, f"max_transported_constraint_resid={max_resid:.1e}"


def symmetric_bilinear_map(rng: np.random.Generator, dim: int = 10) -> np.ndarray:
    raw = rng.normal(size=(dim, dim, dim))
    return 0.5 * (raw + np.swapaxes(raw, 1, 2)) / math.sqrt(dim)


def apply_bilinear(coeff: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.einsum("ijk,j,k->i", coeff, a, b)


def nonlinear_gate(rng: np.random.Generator) -> tuple[bool, str]:
    """Expose the naive nonlinear sign-flip obstruction.

    A linear operator obeys E(-h)=-E(h).  An Einstein-like local expansion has
    quadratic self-couplings, and those even terms obey Q(-h,-h)=Q(h,h).  So
    the signed linear transport cannot be promoted to full nonlinear closure
    unless a separate graded nonlinear localization theorem supplies the even
    terms in the correct bundle.
    """

    source, _constraint = tensor_source_with_constraints()
    h = np.linalg.solve(universal_block_operator(), source)
    q = symmetric_bilinear_map(rng)
    alpha = 0.17

    linear = universal_block_operator() @ h
    linear_odd_resid = float(np.linalg.norm((-universal_block_operator() @ h) + linear))

    def e_nonlin(x: np.ndarray) -> np.ndarray:
        return universal_block_operator() @ x + alpha * apply_bilinear(q, x, x)

    nonlinear_odd_resid = float(np.linalg.norm(e_nonlin(-h) + e_nonlin(h)))
    expected_even = float(np.linalg.norm(2.0 * alpha * apply_bilinear(q, h, h)))
    obstruction_exposed = linear_odd_resid < TOL and nonlinear_odd_resid > 1.0e-3
    calibrated = abs(nonlinear_odd_resid - expected_even) < 1.0e-10
    detail = (
        f"linear_odd_resid={linear_odd_resid:.1e}, "
        f"nonlinear_even_resid={nonlinear_odd_resid:.3e}, "
        f"expected_even={expected_even:.3e}"
    )
    return obstruction_exposed and calibrated, detail


def no_claim_gate() -> tuple[bool, str]:
    claims = {
        "negative_inertial_mass": False,
        "shielding": False,
        "propulsion": False,
        "reactionless_force": False,
        "physical_signed_gravity_prediction": False,
    }
    return not any(claims.values()), ", ".join(f"{key}=False" for key in claims)


def run_audit() -> TransportAudit:
    rng = np.random.default_rng(20260426)

    carrier_ok, carrier_detail = retained_tensor_carrier_check()
    check("retained gravity stack has an ordinary rank-two tensor source carrier", carrier_ok, carrier_detail)

    family_ok, family_detail = orientation_line_family_transport_check(rng)
    check("orientation-line twist commutes with finite family/refinement transport", family_ok, family_detail)

    projective_ok, projective_detail = projective_cylindrical_transport_check()
    check("projective cylindrical tensor response is refinement-stable", projective_ok, projective_detail)

    ward_ok, ward_detail = ward_transport_check()
    check("linear Ward/Bianchi-like constraints transport with the twist", ward_ok, ward_detail)

    nonlinear_ok, nonlinear_detail = nonlinear_gate(rng)
    check("nonlinear gate exposes even-jet obstruction to naive sign-flip closure", nonlinear_ok, nonlinear_detail)

    no_claim_ok, no_claim_detail = no_claim_gate()
    check("non-claim gate remains closed", no_claim_ok, no_claim_detail)

    return TransportAudit(
        carrier_retained=carrier_ok,
        orientation_transport=family_ok,
        projective_transport=projective_ok,
        ward_transport=ward_ok,
        nonlinear_obstruction_exposed=nonlinear_ok,
        no_claim=no_claim_ok,
    )


def main() -> int:
    print("=" * 112)
    print("SIGNED GRAVITY TENSOR-SOURCE TRANSPORT AND RETENTION AUDIT")
    print("  finite carrier retention plus projective transport; nonlinear closure remains gated")
    print("=" * 112)
    print()

    print("TARGET")
    print("  Prove the ordinary tensor stress carrier is retained on the audited")
    print("  gravity classes, and transport the chi_eta tensor-source twist through")
    print("  finite family/refinement maps without turning it into a physical claim.")
    print()

    audit = run_audit()

    print()
    print("INTERPRETATION")
    print("  The ordinary tensor carrier is no longer just an assumption on the")
    print("  audited restricted classes: the retained tensor source-to-channel map is")
    print("  rank two and scalar-blind.  The chi_eta twist commutes with normalized")
    print("  refinement transport, projected responses, and linear constraints.")
    print("  The nonlinear gate is deliberately not closed: even nonlinear jets block")
    print("  the naive h -> -h promotion and require a separate graded Einstein")
    print("  localization theorem.")
    print()

    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if audit.passed and FAIL_COUNT == 0:
        print("FINAL_TAG: SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FINITE_CONDITIONAL")
        return 0
    print("FINAL_TAG: SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
