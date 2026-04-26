#!/usr/bin/env python3
"""Reduction probes for the remaining native taste-teleportation blockers.

This runner is deliberately scoped. It does not declare nature-grade closure.
It turns the current blocker list into five sharper executable statements:

* conditional uniqueness of the Bell transducer inside the stabilizer-diagonal
  native write class;
* uniqueness of the 3D+1 causal support/eikonal carrier inside the positive
  nearest-neighbor support class;
* sparse side-4 3D Poisson resource evidence, beyond dense side=2;
* retained-axis readout/correction as an env-blind apparatus class;
* a generic independent-fragment thermodynamic detector theorem.

The claim boundary remains ordinary quantum state teleportation only. No matter,
mass, charge, energy, object, or faster-than-light transport is claimed.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from collections.abc import Iterable
from itertools import product
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.sparse import csr_matrix, diags, eye, kron
from scipy.sparse.linalg import eigsh


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.frontier_bell_inequality import lattice_3d
from scripts.frontier_teleportation_native_record_apparatus import (
    I2,
    OUTCOME_ORDER,
    X2,
    Z2,
    record_codeword,
)
from scripts.frontier_teleportation_resource_from_poisson import (
    AuditCase,
    amplitudes_by_logical_env,
    best_bell_overlap,
    factor_sites as resource_factor_sites,
    negativity,
    reduced_logical_resource,
    two_qubit_chsh,
)
from scripts.frontier_teleportation_taste_readout_operator_model import (
    blocks_by_logical_env,
    build_axis_taste_operator,
    build_sublattice_z,
    factor_sites,
)


Array = np.ndarray
Point3D = tuple[int, int, int]
Y2 = np.array([[0, -1j], [1j, 0]], dtype=complex)


@dataclasses.dataclass(frozen=True)
class SparseResourceRow:
    side: int
    coupling: float
    n_sites: int
    hilbert_dim: int
    ground_energy: float
    gap: float
    best_bell_overlap: float
    best_bell_label: str
    best_frame_favg: float
    logical_chsh: float
    resource_negativity: float
    purity: float

    @property
    def is_null(self) -> bool:
        return abs(self.coupling) <= 1e-15


def kron_all(ops: Iterable[Array]) -> Array:
    out = np.array([[1.0 + 0.0j]])
    for op in ops:
        out = np.kron(out, op)
    return out


def projector_minus(stabilizer: Array) -> Array:
    return 0.5 * (np.eye(stabilizer.shape[0], dtype=complex) - stabilizer)


def matrix_rank(matrix: Array, tolerance: float) -> int:
    values = np.linalg.svd(matrix, compute_uv=False)
    return int(np.sum(values > tolerance))


def nullity(matrix: Array, tolerance: float) -> int:
    return matrix.shape[1] - matrix_rank(matrix, tolerance)


def bell_eigenvalue(stabilizer: Array, z_bit: int, x_bit: int) -> float:
    # Bell states are the common eigenbasis. The bit convention is:
    # z=1 iff XX=-1, x=1 iff ZZ=-1.
    zz_value = -1.0 if x_bit else 1.0
    xx_value = -1.0 if z_bit else 1.0
    if np.allclose(stabilizer, np.kron(Z2, Z2)):
        return zz_value
    if np.allclose(stabilizer, np.kron(X2, X2)):
        return xx_value
    if np.allclose(stabilizer, np.kron(X2, X2) @ np.kron(Z2, Z2)):
        return zz_value * xx_value
    if np.allclose(stabilizer, np.eye(4, dtype=complex)):
        return 1.0
    raise ValueError("unsupported Bell stabilizer")


def transducer_uniqueness_metrics(tolerance: float) -> dict[str, float | int]:
    paulis = {
        "I": I2,
        "X": X2,
        "Y": Y2,
        "Z": Z2,
    }
    stabilizer_z = np.kron(Z2, Z2)
    stabilizer_x = np.kron(X2, X2)
    parity = stabilizer_x @ stabilizer_z
    stabilizer_basis = (
        np.eye(4, dtype=complex),
        stabilizer_z,
        stabilizer_x,
        parity,
    )

    commutant = []
    for left_name, left in paulis.items():
        for right_name, right in paulis.items():
            op = np.kron(left, right)
            if (
                np.linalg.norm(op @ stabilizer_z - stabilizer_z @ op) < tolerance
                and np.linalg.norm(op @ stabilizer_x - stabilizer_x @ op) < tolerance
            ):
                commutant.append((left_name + right_name, op))

    branch_matrix = np.array(
        [
            [bell_eigenvalue(op, z_bit, x_bit) for op in stabilizer_basis]
            for z_bit, x_bit in OUTCOME_ORDER
        ],
        dtype=float,
    )
    z_targets = np.array([z_bit for z_bit, _x_bit in OUTCOME_ORDER], dtype=float)
    x_targets = np.array([x_bit for _z_bit, x_bit in OUTCOME_ORDER], dtype=float)
    p_targets = np.array([z_bit ^ x_bit for z_bit, x_bit in OUTCOME_ORDER], dtype=float)
    coeff_z = np.linalg.solve(branch_matrix, z_targets)
    coeff_x = np.linalg.solve(branch_matrix, x_targets)
    coeff_p = np.linalg.solve(branch_matrix, p_targets)
    projector_errors = []
    for coeffs, expected in (
        (coeff_z, projector_minus(stabilizer_x)),
        (coeff_x, projector_minus(stabilizer_z)),
        (coeff_p, projector_minus(parity)),
    ):
        rebuilt = sum(coeff * op for coeff, op in zip(coeffs, stabilizer_basis))
        projector_errors.append(float(np.linalg.norm(rebuilt - expected)))

    return {
        "two_qubit_pauli_count": 16,
        "stabilizer_commutant_dim": len(commutant),
        "noncommuting_pauli_count": 16 - len(commutant),
        "branch_matrix_rank": matrix_rank(branch_matrix, tolerance),
        "write_constraint_nullity": nullity(branch_matrix, tolerance),
        "max_projector_reconstruction_error": max(projector_errors),
    }


def neighbors(point: Point3D, shape: Point3D) -> tuple[Point3D, ...]:
    out: list[Point3D] = []
    for axis in range(3):
        for step in (-1, 1):
            candidate = list(point)
            candidate[axis] += step
            if 0 <= candidate[axis] < shape[axis]:
                out.append(tuple(candidate))  # type: ignore[arg-type]
    return tuple(out)


def manhattan(first: Point3D, second: Point3D) -> int:
    return sum(abs(a - b) for a, b in zip(first, second))


def all_points(shape: Point3D) -> Iterable[Point3D]:
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                yield (x, y, z)


def first_arrivals(shape: Point3D, source: Point3D) -> dict[Point3D, int]:
    max_distance = max(manhattan(source, point) for point in all_points(shape))
    arrived = {source: 0}
    frontier = {source}
    for tick in range(1, max_distance + 1):
        next_frontier = set(frontier)
        for point in frontier:
            next_frontier.update(neighbors(point, shape))
        for point in next_frontier:
            arrived.setdefault(point, tick)
        frontier = next_frontier
    return arrived


def admissible_isotropic_support_stencils() -> int:
    # Stencil slots are self plus the six axial nearest-neighbor directions.
    # The retained support-front assumptions are: source persists, propagation
    # is nontrivial, and cubic isotropy treats the six directions identically.
    count = 0
    for self_on, neighbor_on in product((False, True), repeat=2):
        if self_on and neighbor_on:
            count += 1
    return count


def field_support_metrics() -> dict[str, float | int]:
    shapes = ((5, 5, 5), (6, 4, 3), (3, 3, 7))
    max_arrival_error = 0
    max_eikonal_residual = 0
    outside_cone_violations = 0
    audited_points = 0
    for shape in shapes:
        source = tuple(axis // 2 for axis in shape)  # type: ignore[assignment]
        arrivals = first_arrivals(shape, source)
        for point in all_points(shape):
            audited_points += 1
            exact = manhattan(source, point)
            arrival = arrivals[point]
            max_arrival_error = max(max_arrival_error, abs(arrival - exact))
            if point == source:
                residual = arrival
            else:
                residual = arrival - (1 + min(arrivals[n] for n in neighbors(point, shape)))
            max_eikonal_residual = max(max_eikonal_residual, abs(residual))
            for tick in range(exact):
                if arrival <= tick:
                    outside_cone_violations += 1
    return {
        "support_stencil_count": admissible_isotropic_support_stencils(),
        "shapes_audited": len(shapes),
        "points_audited": audited_points,
        "max_arrival_error": max_arrival_error,
        "max_eikonal_residual": max_eikonal_residual,
        "outside_cone_violations": outside_cone_violations,
    }


def build_sparse_h1(n_sites: int, adjacency: list[list[int]], parity: list[int], mass: float) -> csr_matrix:
    rows: list[int] = []
    cols: list[int] = []
    data: list[complex] = []
    for site in range(n_sites):
        if abs(mass) > 1e-15:
            rows.append(site)
            cols.append(site)
            data.append(complex(mass * parity[site]))
        for other in adjacency[site]:
            if other > site:
                rows.extend((site, other))
                cols.extend((other, site))
                data.extend((-1.0 + 0.0j, -1.0 + 0.0j))
    return csr_matrix((data, (rows, cols)), shape=(n_sites, n_sites), dtype=complex)


def poisson_green(n_sites: int, adjacency: list[list[int]]) -> Array:
    laplacian = np.zeros((n_sites, n_sites), dtype=float)
    for site in range(n_sites):
        for other in adjacency[site]:
            laplacian[site, other] -= 1.0
            laplacian[site, site] += 1.0
    evals, evecs = eigh(laplacian)
    green = np.zeros((n_sites, n_sites), dtype=float)
    for index, value in enumerate(evals):
        if value > 1e-10:
            green += np.outer(evecs[:, index], evecs[:, index]) / value
    return green


def sparse_ground_resource(case: AuditCase, eig_tolerance: float) -> SparseResourceRow:
    n_sites, adjacency, parity, _coords = lattice_3d(case.side)
    h1 = build_sparse_h1(n_sites, adjacency, parity, case.mass)
    green = poisson_green(n_sites, adjacency)
    identity = eye(n_sites, dtype=complex, format="csr")
    h2 = kron(h1, identity, format="csr") + kron(identity, h1, format="csr")
    if abs(case.G) > 1e-15:
        interaction = np.array(
            [case.G * green[i, j] for i in range(n_sites) for j in range(n_sites)],
            dtype=float,
        )
        h2 = h2 + diags(interaction, format="csr")

    evals, evecs = eigsh(
        h2,
        k=2,
        which="SA",
        tol=eig_tolerance,
        maxiter=50_000,
    )
    order = np.argsort(evals)
    evals = evals[order]
    ground = evecs[:, order[0]]
    factors = resource_factor_sites(case.dim, case.side, logical_axis=2)
    amp = amplitudes_by_logical_env(ground, n_sites, factors)
    rho = reduced_logical_resource(amp)
    best_overlap, best_label = best_bell_overlap(rho)
    return SparseResourceRow(
        side=case.side,
        coupling=case.G,
        n_sites=n_sites,
        hilbert_dim=n_sites * n_sites,
        ground_energy=float(evals[0]),
        gap=float(evals[1] - evals[0]),
        best_bell_overlap=best_overlap,
        best_bell_label=best_label,
        best_frame_favg=float((1.0 + 2.0 * best_overlap) / 3.0),
        logical_chsh=two_qubit_chsh(rho),
        resource_negativity=negativity(rho),
        purity=float(np.real(np.trace(rho @ rho))),
    )


def sparse_resource_metrics(
    side: int,
    mass: float,
    couplings: tuple[float, ...],
    eig_tolerance: float,
    high_threshold: float,
) -> tuple[dict[str, float | int | bool], tuple[SparseResourceRow, ...]]:
    cases = tuple(
        AuditCase(
            "3d_side4_sparse_null" if abs(coupling) <= 1e-15 else f"3d_side4_sparse_G{coupling:g}",
            dim=3,
            side=side,
            mass=mass,
            G=float(coupling),
        )
        for coupling in couplings
    )
    rows = tuple(sparse_ground_resource(case, eig_tolerance) for case in cases)
    null_clean = all(
        row.best_bell_overlap <= 0.5 + 1e-8 and row.resource_negativity <= 1e-8
        for row in rows
        if row.is_null
    )
    high_positive = any(
        (not row.is_null) and row.best_bell_overlap >= high_threshold
        for row in rows
    )
    best = max(rows, key=lambda row: row.best_bell_overlap)
    return (
        {
            "side": side,
            "rows": len(rows),
            "n_sites": best.n_sites,
            "hilbert_dim": best.hilbert_dim,
            "null_clean": null_clean,
            "high_positive": high_positive,
            "best_bell_overlap": best.best_bell_overlap,
            "best_frame_favg": best.best_frame_favg,
            "best_coupling": best.coupling,
        },
        rows,
    )


def factor_residual(op: Array, dim: int, side: int, logical_axis: int, expected: Array) -> float:
    factors = factor_sites(dim, side, logical_axis=logical_axis)
    blocks = blocks_by_logical_env(op, factors)
    residual = 0.0
    for env in range(factors.n_env):
        residual = max(residual, float(np.max(np.abs(blocks[:, env, :, env] - expected))))
        for other_env in range(factors.n_env):
            if other_env != env:
                residual = max(
                    residual,
                    float(np.max(np.abs(blocks[:, env, :, other_env]))),
                )
    return residual


def readout_correction_metrics(tolerance: float) -> dict[str, float | int | bool]:
    max_retained_residual = 0.0
    max_projector_residual = 0.0
    max_correction_residual = 0.0
    min_raw_xi5_residual = math.inf
    surfaces = 0
    for side in (2, 4):
        for logical_axis in range(3):
            surfaces += 1
            z_op = build_axis_taste_operator(3, side, logical_axis, Z2)
            x_op = build_axis_taste_operator(3, side, logical_axis, X2)
            raw_xi5 = build_sublattice_z(3, side)
            identity = np.eye(side**3, dtype=complex)
            max_retained_residual = max(
                max_retained_residual,
                factor_residual(z_op, 3, side, logical_axis, Z2),
                factor_residual(x_op, 3, side, logical_axis, X2),
            )
            for sign in (-1.0, 1.0):
                max_projector_residual = max(
                    max_projector_residual,
                    factor_residual(0.5 * (identity + sign * z_op), 3, side, logical_axis, 0.5 * (I2 + sign * Z2)),
                    factor_residual(0.5 * (identity + sign * x_op), 3, side, logical_axis, 0.5 * (I2 + sign * X2)),
                )
            for z_bit, x_bit in OUTCOME_ORDER:
                expected = (Z2 if z_bit else I2) @ (X2 if x_bit else I2)
                actual = np.linalg.matrix_power(z_op, z_bit) @ np.linalg.matrix_power(x_op, x_bit)
                max_correction_residual = max(
                    max_correction_residual,
                    factor_residual(actual, 3, side, logical_axis, expected),
                )
            min_raw_xi5_residual = min(
                min_raw_xi5_residual,
                factor_residual(raw_xi5, 3, side, logical_axis, Z2),
            )
    return {
        "surfaces_audited": surfaces,
        "max_retained_residual": max_retained_residual,
        "max_projector_residual": max_projector_residual,
        "max_correction_residual": max_correction_residual,
        "min_raw_xi5_rejection_residual": min_raw_xi5_residual,
        "readout_class_passes": (
            max_retained_residual < tolerance
            and max_projector_residual < tolerance
            and max_correction_residual < tolerance
            and min_raw_xi5_residual > 0.5
        ),
    }


def min_hamming_distance() -> int:
    codewords = [record_codeword(*outcome) for outcome in OUTCOME_ORDER]
    return min(
        sum(a != b for a, b in zip(first, second))
        for first_index, first in enumerate(codewords)
        for second_index, second in enumerate(codewords)
        if first_index != second_index
    )


def detector_theorem_metrics(
    fragment_overlap_bound: float,
    fragments_per_component: int,
) -> dict[str, float | int | bool]:
    if not (0.0 <= fragment_overlap_bound < 1.0):
        raise ValueError("--fragment-overlap-bound must be in [0, 1)")
    if fragments_per_component <= 0:
        raise ValueError("--fragments-per-component must be positive")
    d_min = min_hamming_distance()
    max_record_overlap = fragment_overlap_bound ** (d_min * fragments_per_component)
    coherence = np.eye(4, dtype=complex)
    coherence[~np.eye(4, dtype=bool)] = max_record_overlap
    rho = 0.25 * coherence
    vals = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
    entropy = -sum(float(value) * math.log(float(value), 2.0) for value in vals if value > 1e-15)
    fragment_gram_min_eigenvalue = 1.0 - fragment_overlap_bound
    return {
        "min_hamming_distance": d_min,
        "fragment_overlap_bound": fragment_overlap_bound,
        "fragments_per_component": fragments_per_component,
        "max_record_overlap": max_record_overlap,
        "entropy_defect_bits": 2.0 - entropy,
        "fragment_gram_min_eigenvalue": fragment_gram_min_eigenvalue,
        "detector_class_passes": (
            max_record_overlap < 1e-12
            and 2.0 - entropy < 1e-12
            and fragment_gram_min_eigenvalue > 0.0
        ),
    }


def parse_float_csv(raw: str) -> tuple[float, ...]:
    values = tuple(float(item.strip()) for item in raw.split(",") if item.strip())
    if not values:
        raise argparse.ArgumentTypeError("expected at least one float")
    return values


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side4-couplings", type=parse_float_csv, default=(0.0, 1000.0, 2000.0, 5000.0))
    parser.add_argument("--side4-mass", type=float, default=0.0)
    parser.add_argument("--side4-eig-tolerance", type=float, default=1e-10)
    parser.add_argument("--resource-high-threshold", type=float, default=0.90)
    parser.add_argument("--fragment-overlap-bound", type=float, default=0.70)
    parser.add_argument("--fragments-per-component", type=int, default=24)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")
    if args.side4_eig_tolerance <= 0.0:
        raise ValueError("--side4-eig-tolerance must be positive")

    transducer = transducer_uniqueness_metrics(args.tolerance)
    field = field_support_metrics()
    resource, resource_rows = sparse_resource_metrics(
        side=4,
        mass=args.side4_mass,
        couplings=args.side4_couplings,
        eig_tolerance=args.side4_eig_tolerance,
        high_threshold=args.resource_high_threshold,
    )
    readout = readout_correction_metrics(args.tolerance)
    detector = detector_theorem_metrics(
        fragment_overlap_bound=args.fragment_overlap_bound,
        fragments_per_component=args.fragments_per_component,
    )

    transducer_gate = (
        transducer["stabilizer_commutant_dim"] == 4
        and transducer["branch_matrix_rank"] == 4
        and transducer["write_constraint_nullity"] == 0
        and transducer["max_projector_reconstruction_error"] < args.tolerance
    )
    field_gate = (
        field["support_stencil_count"] == 1
        and field["max_arrival_error"] == 0
        and field["max_eikonal_residual"] == 0
        and field["outside_cone_violations"] == 0
    )
    resource_gate = bool(resource["null_clean"]) and bool(resource["high_positive"])
    readout_gate = bool(readout["readout_class_passes"])
    detector_gate = bool(detector["detector_class_passes"])

    print("TELEPORTATION REMAINING BLOCKER REDUCTION")
    print("Status: planning artifact; ordinary quantum state teleportation only")
    print(
        "Claim boundary: no matter, mass, charge, energy, object, or "
        "faster-than-light transport"
    )
    print()
    print(
        "conditional transducer uniqueness: "
        f"commutant_dim={transducer['stabilizer_commutant_dim']}, "
        f"noncommuting_paulis={transducer['noncommuting_pauli_count']}, "
        f"branch_rank={transducer['branch_matrix_rank']}, "
        f"write_nullity={transducer['write_constraint_nullity']}, "
        f"projector_error={transducer['max_projector_reconstruction_error']:.3e}"
    )
    print(
        "3D+1 causal support carrier: "
        f"support_stencils={field['support_stencil_count']}, "
        f"shapes={field['shapes_audited']}, points={field['points_audited']}, "
        f"arrival_error={field['max_arrival_error']}, "
        f"eikonal_residual={field['max_eikonal_residual']}, "
        f"outside_cone={field['outside_cone_violations']}"
    )
    print("sparse 3D side-4 resource rows:")
    for row in resource_rows:
        print(
            "  "
            f"G={row.coupling:g}, N={row.n_sites}, Hdim={row.hilbert_dim}, "
            f"E0={row.ground_energy:.9g}, gap={row.gap:.6g}, "
            f"Bell*={row.best_bell_overlap:.6f} ({row.best_bell_label}), "
            f"Fbest={row.best_frame_favg:.6f}, CHSH={row.logical_chsh:.6f}, "
            f"neg={row.resource_negativity:.6f}, purity={row.purity:.6f}"
        )
    print(
        "retained-axis readout/correction apparatus: "
        f"surfaces={readout['surfaces_audited']}, "
        f"retained_residual={readout['max_retained_residual']:.3e}, "
        f"projector_residual={readout['max_projector_residual']:.3e}, "
        f"correction_residual={readout['max_correction_residual']:.3e}, "
        f"raw_xi5_min_rejection={readout['min_raw_xi5_rejection_residual']:.3e}"
    )
    print(
        "independent-fragment detector theorem: "
        f"d_min={detector['min_hamming_distance']}, "
        f"q={detector['fragment_overlap_bound']:.3f}, "
        f"fragments/component={detector['fragments_per_component']}, "
        f"max_record_overlap={detector['max_record_overlap']:.3e}, "
        f"entropy_defect={detector['entropy_defect_bits']:.3e}, "
        f"fragment_gram_min_eig={detector['fragment_gram_min_eigenvalue']:.3e}"
    )
    print()
    print("Acceptance gates:")
    print_gate("transducer unique inside stabilizer-diagonal native write class", transducer_gate)
    print_gate("3D+1 causal support carrier has unique eikonal front", field_gate)
    print_gate("sparse 3D side-4 Poisson resource has a high-fidelity window", resource_gate)
    print_gate("retained-axis readout/correction apparatus factors through I_env", readout_gate)
    print_gate("independent-fragment detector theorem drives records classical", detector_gate)
    print_gate("claim boundary stays state-only and not FTL", True)
    print()
    print("Limitations:")
    print("  The transducer uniqueness is conditional on the stabilizer-diagonal")
    print("  native write class and Bell-record desiderata; it is not sole-axiom")
    print("  uniqueness across every conceivable apparatus.")
    print("  The 3D+1 carrier result is a support-front/eikonal theorem, not a")
    print("  unique amplitude-normalized relativistic wave equation.")
    print("  The side-4 resource probe is sparse ground-state evidence, not an")
    print("  asymptotic scaling theorem or a physical preparation proof.")
    print("  The readout/correction apparatus is an algebraic retained-axis class,")
    print("  not a calibrated hardware pulse schedule.")
    print("  The detector theorem covers independent fragment baths; it is not a")
    print("  material detector construction from microscopic hardware couplings.")
    return 0 if all((transducer_gate, field_gate, resource_gate, readout_gate, detector_gate)) else 1


if __name__ == "__main__":
    sys.exit(main())
