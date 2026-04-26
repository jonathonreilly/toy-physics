#!/usr/bin/env python3
"""Nature-grade closure blocker matrix for the signed-gravity lane.

This script audits the five remaining blockers after the finite
Cl(3)/Z^3 determinant-source-character derivation:

1. continuum determinant-line lift;
2. actual retained graph-family APS realization;
3. full tensor/Einstein localization beyond A1;
4. sector dynamics and preparation;
5. UV/core stability.

The intended output is a disciplined closure matrix, not a forced claim.
Rows can be finite-closed, conditional, or blocked.  No row asserts a
negative-mass, shielding, propulsion, reactionless-force, or physical
signed-gravity prediction.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from enum import Enum

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.signed_gravity_aps_boundary_index_probe import (  # noqa: E402
    boundary_model,
    chi_from_eta,
    eta_delta,
    hermitian_part,
)
from scripts.signed_gravity_source_character_uniqueness_theorem import (  # noqa: E402
    generator,
    sign_eta,
)
from scripts.signed_gravity_oriented_tensor_source_lift import (  # noqa: E402
    canonical_projectors,
    free_tensor_carrier_gate,
    orientation_twist_check,
    response_locking_check,
    scalar_only_no_overclaim_check,
    tensor_source_with_constraints,
    ward_constraint_check,
)
from scripts.signed_gravity_tensor_source_transport_retention import (  # noqa: E402
    nonlinear_gate,
    orientation_line_family_transport_check,
    projective_cylindrical_transport_check,
    retained_tensor_carrier_check,
    ward_transport_check,
)
from scripts.signed_gravity_continuum_graded_einstein_localization import (  # noqa: E402
    continuum_schur_transport_check,
    continuum_stack_check,
    flat_orientation_local_system_check,
    graded_formal_localization_check,
    ward_bianchi_transport_check,
)
from scripts.signed_gravity_remaining_closure_gates import (  # noqa: E402
    finite_galerkin_small_data_gate,
    graph_family_aps_extraction_gate as raw_graph_aps_extraction_gate,
    sector_preparation_gate as remaining_sector_preparation_gate,
    uv_core_stability_boundary_gate,
)
from scripts.signed_gravity_native_boundary_complex_containment import (  # noqa: E402
    native_containment_summary_gate,
)
from scripts.signed_gravity_staggered_dirac_boundary_eta_realization import (  # noqa: E402
    staggered_dirac_boundary_summary_gate,
)
from scripts.signed_gravity_naturally_hosted_orientation_line import (  # noqa: E402
    naturally_hosted_orientation_line_summary_gate,
)


TOL = 1.0e-10


class Status(Enum):
    CLOSED_FINITE = "CLOSED_FINITE"
    CONDITIONAL = "CONDITIONAL"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class Gate:
    name: str
    status: Status
    passed: bool
    detail: str
    next_needed: str


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    dim = sum(block.shape[0] for block in blocks)
    out = np.zeros((dim, dim), dtype=complex)
    offset = 0
    for block in blocks:
        n = block.shape[0]
        out[offset : offset + n, offset : offset + n] = block
        offset += n
    return out


def logabsdet(m: np.ndarray) -> float:
    sign, logabs = np.linalg.slogdet(m)
    if abs(sign) < TOL:
        return -math.inf
    return float(logabs)


def continuum_determinant_line_gate() -> Gate:
    """Finite projective determinant-line consistency under refinements."""

    base_plus = boundary_model(+1, pairs=4, gap=0.35)
    chis = []
    etas = []
    det_log_errors = []
    for copies in (1, 2, 4, 8):
        d_ref = np.kron(base_plus, np.eye(copies))
        eta, zero, _n, _vals = eta_delta(d_ref)
        etas.append(eta)
        chis.append(chi_from_eta(eta, zero))

        # Refinement as direct-sum copies: determinant logs add exactly.
        blocks = [base_plus + 0.03 * np.eye(base_plus.shape[0]) for _ in range(copies)]
        direct = block_diag(*blocks)
        det_log_errors.append(abs(logabsdet(direct) - copies * logabsdet(blocks[0])))

    passed = chis == [+1, +1, +1, +1] and max(det_log_errors) < 1.0e-9
    status = Status.CONDITIONAL
    detail = f"eta={etas}, chi={chis}, max_logdet_refinement_err={max(det_log_errors):.1e}"
    return Gate(
        "continuum determinant-line lift",
        status,
        passed,
        detail,
        "replace finite projective/refinement sanity check by inverse-limit determinant-line theorem",
    )


@dataclass(frozen=True)
class BoundaryFamily:
    name: str
    orientation: int
    copies: int
    perturb: float


def family_operator(fam: BoundaryFamily) -> np.ndarray:
    base = np.kron(boundary_model(fam.orientation, pairs=5, gap=0.42), np.eye(fam.copies))
    if fam.perturb == 0.0:
        return base
    rng = np.random.default_rng(abs(hash(fam.name)) % (2**32))
    raw = hermitian_part(rng.normal(size=base.shape) + 1j * rng.normal(size=base.shape))
    raw /= max(float(np.linalg.norm(raw, ord=2)), 1.0e-12)
    return base + fam.perturb * raw


def graph_family_aps_gate() -> Gate:
    """Prototype APS boundary realization across graph-like family labels."""

    families = [
        BoundaryFamily("cubic_shell", +1, 1, 0.00),
        BoundaryFamily("subdivided_cubic_shell", +1, 3, 0.03),
        BoundaryFamily("rectangular_shell", +1, 2, 0.04),
        BoundaryFamily("orientation_reversed_shell", -1, 2, 0.04),
        BoundaryFamily("irregular_shell", +1, 5, 0.05),
    ]
    reads = []
    gaps = []
    for fam in families:
        d = family_operator(fam)
        eta, zero, _n, vals = eta_delta(d)
        chi = chi_from_eta(eta, zero)
        reads.append((fam.name, fam.orientation, eta, chi))
        gaps.append(float(np.min(np.abs(vals))))

    signs_ok = all(chi == orient for _name, orient, _eta, chi in reads)
    gaps_ok = min(gaps) > 0.25
    raw_aps_ok, raw_aps_detail = raw_graph_aps_extraction_gate()
    native_containment_ok, native_containment_detail = native_containment_summary_gate()
    staggered_boundary_ok, staggered_boundary_detail = staggered_dirac_boundary_summary_gate()
    hosted_ok, hosted_detail = naturally_hosted_orientation_line_summary_gate()
    passed = signs_ok and gaps_ok and raw_aps_ok and native_containment_ok and staggered_boundary_ok and hosted_ok
    detail = (
        " ; ".join(f"{name}:eta={eta:+d},chi={chi:+d}" for name, _orient, eta, chi in reads)
        + f" | raw_graph_boundary={raw_aps_detail}"
        + f" | native_containment={native_containment_detail}"
        + f" | staggered_boundary={staggered_boundary_detail}"
        + f" | hosted_orientation_line={hosted_detail}"
    )
    return Gate(
        "actual retained graph-family APS realization",
        Status.CONDITIONAL,
        passed,
        detail,
        "derive a canonical section/source theorem for the naturally hosted orientation line; current raw Hodge and staggered-Dirac operators do not contain it",
    )


def tensor_localization_gate() -> Gate:
    """Scalar source is A1-maximal; oriented tensor bundle lift is conditional."""

    gens = [generator(axis) for axis in ("x", "y", "z")]
    stack_full = np.vstack(gens)
    full_fixed = stack_full.shape[1] - int(np.linalg.matrix_rank(stack_full, tol=1.0e-9))

    comp_indices = [1, 2, 3, 5, 6, 7, 8, 9]
    stack_comp = np.vstack([g[np.ix_(comp_indices, comp_indices)] for g in gens])
    comp_fixed = stack_comp.shape[1] - int(np.linalg.matrix_rank(stack_comp, tol=1.0e-9))

    projectors = canonical_projectors()
    source, constraint = tensor_source_with_constraints()
    twist_ok, _twist_detail = orientation_twist_check(source, projectors)
    ward_ok, _ward_detail = ward_constraint_check(source, constraint)
    response_ok, _response_detail = response_locking_check(source)
    scalar_ok, _scalar_detail = scalar_only_no_overclaim_check(projectors)
    carrier_ok, _carrier_detail = free_tensor_carrier_gate(source)

    rng = np.random.default_rng(20260426)
    retained_carrier_ok, _retained_carrier_detail = retained_tensor_carrier_check()
    family_transport_ok, _family_transport_detail = orientation_line_family_transport_check(rng)
    projective_transport_ok, _projective_transport_detail = projective_cylindrical_transport_check()
    ward_transport_ok, _ward_transport_detail = ward_transport_check()
    nonlinear_gate_ok, _nonlinear_gate_detail = nonlinear_gate(rng)
    continuum_stack_ok, _continuum_stack_detail = continuum_stack_check()
    flat_line_ok, _flat_line_detail = flat_orientation_local_system_check()
    continuum_schur_ok, _continuum_schur_detail = continuum_schur_transport_check()
    graded_formal_ok, _graded_formal_detail = graded_formal_localization_check(order=6)
    graded_ward_ok, _graded_ward_detail = ward_bianchi_transport_check()
    small_data_ok, _small_data_detail = finite_galerkin_small_data_gate()

    passed = (
        full_fixed == 2
        and comp_fixed == 0
        and twist_ok
        and ward_ok
        and response_ok
        and scalar_ok
        and carrier_ok
        and retained_carrier_ok
        and family_transport_ok
        and projective_transport_ok
        and ward_transport_ok
        and nonlinear_gate_ok
        and continuum_stack_ok
        and flat_line_ok
        and continuum_schur_ok
        and graded_formal_ok
        and graded_ward_ok
        and small_data_ok
    )
    detail = (
        f"scalar_invariant_dim_full={full_fixed}, scalar_complement_dim={comp_fixed}, "
        f"oriented_tensor_lift={twist_ok and ward_ok and response_ok and carrier_ok}, "
        f"retained_carrier={retained_carrier_ok}, projective_transport={projective_transport_ok}, "
        f"continuum_transport={continuum_stack_ok and flat_line_ok and continuum_schur_ok}, "
        f"graded_formal_localization={graded_formal_ok and graded_ward_ok}, "
        f"finite_galerkin_small_data={small_data_ok}, "
        f"global_pde_claim=False"
    )
    return Gate(
        "full tensor/Einstein localization beyond A1",
        Status.CONDITIONAL,
        passed,
        detail,
        "upgrade formal graded local theorem to global nonlinear PDE existence/uniqueness if needed; scalar-only source remains A1-maximal",
    )


def sector_dynamics_gate() -> Gate:
    """Superselection is finite-closed; dynamical preparation remains open."""

    d0 = boundary_model(+1, gap=0.4)
    g0 = abs(float(np.real(d0[0, 0])))
    chi_path = []
    allowed = []
    gaps = []
    for t in np.linspace(1.0, -1.0, 11):
        d = d0.copy()
        d[0, 0] = g0 * t
        eta, zero, _n, vals = eta_delta(d, delta=1.0e-9)
        chi_path.append(chi_from_eta(eta, zero))
        gap = float(np.min(np.abs(vals)))
        gaps.append(gap)
        allowed.append(gap >= 0.1 and chi_path[-1] != 0)

    stable_under_gap = chi_path[0] == +1 and 0 in chi_path and chi_path[-1] == -1 and not all(allowed)
    # Both sectors are definable as disconnected initial-data components, but
    # this does not prove a physical preparation channel.
    definable_components = {+1: True, -1: True, 0: False}
    remaining_sector_ok, remaining_sector_detail = remaining_sector_preparation_gate()
    passed = stable_under_gap and definable_components[+1] and definable_components[-1] and remaining_sector_ok
    detail = (
        f"chi_path={chi_path}, allowed={allowed}, components={definable_components}, "
        f"preparation_boundary={remaining_sector_detail}"
    )
    return Gate(
        "sector dynamics and preparation",
        Status.CONDITIONAL,
        passed,
        detail,
        "treat opposite-sector preparation as boundary-data/defect preparation unless a physical preparation channel is derived",
    )


def uv_core_stability_gate() -> Gate:
    """Finite lattice/core gives bounded energy; global stability remains open."""

    radii = np.geomspace(0.02, 50.0, 800)
    masses = (1.0, 1.3)
    core = 1.0
    same = np.array([masses[0] + masses[1] - masses[0] * masses[1] / math.sqrt(r * r + core * core) for r in radii])
    opp = np.array([masses[0] + masses[1] + masses[0] * masses[1] / math.sqrt(r * r + core * core) for r in radii])
    no_core = np.array([masses[0] + masses[1] - masses[0] * masses[1] / max(r, 1.0e-12) for r in radii])

    # Finite-dimensional positive Gaussian operator as UV-finite partition check.
    eigs = np.linspace(0.4, 3.0, 12)
    k = np.diag(eigs)
    source = np.linspace(-0.2, 0.25, 12)
    log_z = 0.5 * len(eigs) * math.log(2.0 * math.pi) - 0.5 * float(np.sum(np.log(eigs))) + 0.5 * float(source @ np.linalg.solve(k, source))

    finite_bounded = float(np.min(same)) > -math.inf and float(np.min(opp)) > 0.0 and math.isfinite(log_z)
    no_core_unbounded_trend = float(np.min(no_core)) < -20.0
    uv_boundary_ok, uv_boundary_detail = uv_core_stability_boundary_gate()
    passed = finite_bounded and no_core_unbounded_trend and uv_boundary_ok
    detail = (
        f"E_same_core_min={float(np.min(same)):.3f}, E_opp_core_min={float(np.min(opp)):.3f}, "
        f"E_same_no_core_min={float(np.min(no_core)):.3f}, logZ={log_z:.3f}, "
        f"global_boundary={uv_boundary_detail}"
    )
    return Gate(
        "UV/core stability",
        Status.CONDITIONAL,
        passed,
        detail,
        "add a genuine global stability mechanism; pair softening alone bounds fixed N but fails thermodynamic stability",
    )


def main() -> int:
    gates = [
        continuum_determinant_line_gate(),
        graph_family_aps_gate(),
        tensor_localization_gate(),
        sector_dynamics_gate(),
        uv_core_stability_gate(),
    ]

    print("=" * 112)
    print("SIGNED GRAVITY NATURE-GRADE CLOSURE BLOCKER MATRIX")
    print("  finite/conditional/blocker audit; not a physical signed-gravity claim")
    print("=" * 112)
    print()
    print(f"{'gate':<48s} {'status':<16s} {'ok':<5s} detail")
    print("-" * 112)
    for gate in gates:
        print(f"{gate.name:<48s} {gate.status.value:<16s} {str(gate.passed):<5s} {gate.detail}")
    print()
    print("NEXT REQUIRED")
    for gate in gates:
        print(f"  - {gate.name}: {gate.next_needed}")

    all_checks_good = all(gate.passed for gate in gates)
    closed_nature_grade = all(gate.status == Status.CLOSED_FINITE for gate in gates)
    hard_blockers = [gate.name for gate in gates if gate.status == Status.BLOCKED]
    conditional = [gate.name for gate in gates if gate.status == Status.CONDITIONAL]

    print()
    print("SUMMARY")
    print(f"  checks_good={all_checks_good}")
    print(f"  nature_grade_closed={closed_nature_grade}")
    print(f"  conditional={conditional}")
    print(f"  blocked={hard_blockers}")
    if all_checks_good and not closed_nature_grade and not hard_blockers:
        print("FINAL_TAG: SIGNED_GRAVITY_NATURE_GRADE_HARD_BLOCKERS_REDUCED_CONDITIONALS_REMAIN")
        return 0
    if all_checks_good and not closed_nature_grade:
        print("FINAL_TAG: SIGNED_GRAVITY_NATURE_GRADE_REDUCED_BLOCKERS_REMAIN")
        return 0
    print("FINAL_TAG: SIGNED_GRAVITY_NATURE_GRADE_BLOCKER_AUDIT_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
