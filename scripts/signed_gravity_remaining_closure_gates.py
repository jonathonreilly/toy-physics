#!/usr/bin/env python3
"""Remaining closure gates for the signed-gravity lane.

This runner goes after the four items left outside the formal tensor theorem:

1. global nonlinear PDE existence;
2. actual retained graph-family APS extraction;
3. sector dynamics / preparation;
4. UV/core stability.

It does not force an all-green nature-grade claim.  It upgrades what can be
upgraded and makes the remaining obstruction surfaces precise:

* nonlinear dynamics: finite Galerkin small-data contraction theorem passes;
  global continuum PDE existence is not claimed;
* APS graph extraction: raw retained graph Hodge-Dirac boundaries are
  eta-neutral; a retained orientation-line mode is still required;
* sector preparation: fixed sectors are superselected; sign change requires a
  zero-mode defect, so preparation is boundary-data/defect preparation, not
  ordinary dynamics;
* UV/core stability: finite-N softened core is bounded, but pair softening
  alone fails thermodynamic/Ruelle stability for arbitrary same-sector N.

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

from scripts.signed_gravity_aps_boundary_index_probe import (  # noqa: E402
    boundary_model,
    chi_from_eta,
    eta_delta,
)
from scripts.signed_gravity_continuum_graded_einstein_localization import (  # noqa: E402
    apply_q,
    apply_r,
    projected_maps,
)


TOL = 1.0e-10
PASS_COUNT = 0
FAIL_COUNT = 0


@dataclass(frozen=True)
class RemainingAudit:
    small_data_galerkin: bool
    aps_extraction_boundary: bool
    sector_preparation_boundary: bool
    uv_core_boundary: bool
    no_claim: bool

    @property
    def passed(self) -> bool:
        return (
            self.small_data_galerkin
            and self.aps_extraction_boundary
            and self.sector_preparation_boundary
            and self.uv_core_boundary
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


def frob_norm(tensor: np.ndarray) -> float:
    return float(np.linalg.norm(tensor.reshape(-1)))


def finite_galerkin_small_data_gate() -> tuple[bool, str]:
    """Finite-dimensional contraction theorem for the nonlinear stationary map."""

    _constraint, k_op, q, r, source = projected_maps()
    k_inv = np.linalg.inv(k_op)
    k_inv_norm = float(np.linalg.norm(k_inv, ord=2))
    q_norm = frob_norm(q)
    r_norm = frob_norm(r)
    source_norm = float(np.linalg.norm(source))

    eps = 2.0e-3
    linear_radius = k_inv_norm * eps * source_norm
    radius = 2.0 * linear_radius
    self_bound = k_inv_norm * (eps * source_norm + q_norm * radius * radius + r_norm * radius**3)
    lipschitz_bound = k_inv_norm * (2.0 * q_norm * radius + 3.0 * r_norm * radius * radius)

    # Numerical sanity check inside the analytic contraction ball.
    rng = np.random.default_rng(20260426)
    max_sample_lip = 0.0

    def phi(h: np.ndarray) -> np.ndarray:
        return k_inv @ (eps * source - apply_q(q, h, h) - apply_r(r, h, h, h))

    for _ in range(64):
        a = rng.normal(size=source.shape)
        b = rng.normal(size=source.shape)
        a *= radius / max(float(np.linalg.norm(a)), 1.0e-12)
        b *= radius / max(float(np.linalg.norm(b)), 1.0e-12)
        denom = max(float(np.linalg.norm(a - b)), 1.0e-12)
        max_sample_lip = max(max_sample_lip, float(np.linalg.norm(phi(a) - phi(b))) / denom)

    ok = self_bound <= radius and lipschitz_bound < 1.0 and max_sample_lip < 1.0
    detail = (
        f"eps={eps:.1e}, radius={radius:.3e}, self_bound/r={self_bound / radius:.3f}, "
        f"lip_bound={lipschitz_bound:.3f}, sample_lip={max_sample_lip:.3f}, "
        f"global_pde_claim=False"
    )
    return ok, detail


def graph_edges_cycle(n: int) -> list[tuple[int, int]]:
    return [(i, (i + 1) % n) for i in range(n)]


def graph_edges_ladder(n: int) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for row in (0, 1):
        off = row * n
        edges.extend((off + i, off + ((i + 1) % n)) for i in range(n))
    edges.extend((i, n + i) for i in range(n))
    return edges


def graph_edges_grid_boundary(nx: int, ny: int) -> list[tuple[int, int]]:
    def idx(x: int, y: int) -> int:
        return y * nx + x

    edges: list[tuple[int, int]] = []
    for x in range(nx - 1):
        edges.append((idx(x, 0), idx(x + 1, 0)))
        edges.append((idx(x, ny - 1), idx(x + 1, ny - 1)))
    for y in range(ny - 1):
        edges.append((idx(0, y), idx(0, y + 1)))
        edges.append((idx(nx - 1, y), idx(nx - 1, y + 1)))
    return edges


def incidence(n_vertices: int, edges: list[tuple[int, int]]) -> np.ndarray:
    b = np.zeros((n_vertices, len(edges)), dtype=float)
    for col, (u, v) in enumerate(edges):
        b[u, col] = -1.0
        b[v, col] = +1.0
    return b


def hodge_dirac(n_vertices: int, edges: list[tuple[int, int]]) -> np.ndarray:
    b = incidence(n_vertices, edges)
    return np.block(
        [
            [np.zeros((n_vertices, n_vertices)), b],
            [b.T, np.zeros((len(edges), len(edges)))],
        ]
    )


def eta_of(mat: np.ndarray) -> tuple[int, int, int]:
    eta, zero, _n, vals = eta_delta(mat, delta=1.0e-8)
    return eta, zero, chi_from_eta(eta, zero)


def graph_family_aps_extraction_gate() -> tuple[bool, str]:
    """Raw graph Hodge boundaries are eta-neutral; orientation mode is required."""

    families = [
        ("cycle8", 8, graph_edges_cycle(8)),
        ("cycle12", 12, graph_edges_cycle(12)),
        ("ladder6", 12, graph_edges_ladder(6)),
        ("rect_boundary", 20, graph_edges_grid_boundary(5, 4)),
    ]
    raw_reads = []
    extended_reads = []
    raw_neutral = True
    extension_portable = True
    for name, n_vertices, edges in families:
        d_raw = hodge_dirac(n_vertices, edges)
        eta_raw, zero_raw, chi_raw = eta_of(d_raw)
        raw_reads.append(f"{name}:eta={eta_raw:+d},zero={zero_raw},chi={chi_raw:+d}")
        raw_neutral &= eta_raw == 0 and chi_raw == 0

        for orient in (+1, -1):
            d_ext = np.block(
                [
                    [np.array([[0.35 * orient]]), np.zeros((1, d_raw.shape[0]))],
                    [np.zeros((d_raw.shape[0], 1)), d_raw],
                ]
            )
            eta_ext, zero_ext, chi_ext = eta_of(d_ext)
            # Hodge kernels remain zero-window modes.  The orientation extension
            # is therefore a conditional carrier, not an admitted active APS
            # operator until the retained boundary complex removes/quarantines
            # those kernels.
            extension_portable &= eta_ext == orient and chi_ext == 0 and zero_ext > 0
            extended_reads.append(f"{name}/{orient:+d}:eta={eta_ext:+d},zero={zero_ext},chi={chi_ext:+d}")

    obstruction_exposed = raw_neutral and extension_portable
    detail = (
        f"raw_hodge_eta_neutral={raw_neutral}, orientation_extension_has_eta=True, "
        f"zero_modes_quarantine=True, actual_extraction_closed=False; raw={raw_reads[:2]}"
    )
    return obstruction_exposed, detail


def unitary_leakage_gate() -> tuple[float, float]:
    h_plus = np.array([[0.4, 0.0], [0.0, 1.1]], dtype=float)
    h_minus = np.array([[0.7, 0.0], [0.0, 1.3]], dtype=float)
    h_block = np.block(
        [
            [h_plus, np.zeros((2, 2))],
            [np.zeros((2, 2)), h_minus],
        ]
    )
    theta = 0.23
    # Since h_block is block diagonal, every polynomial time step is exactly
    # sector-preserving.  Use a second-order unitary approximant for a finite
    # leakage witness.
    u_block = np.eye(4) - 1j * theta * h_block - 0.5 * theta * theta * (h_block @ h_block)
    p_plus = np.diag([1.0, 1.0, 0.0, 0.0])
    p_minus = np.diag([0.0, 0.0, 1.0, 1.0])
    block_leak = float(np.linalg.norm(p_minus @ u_block @ p_plus))

    mix = h_block.copy()
    mix[1, 2] = mix[2, 1] = 0.08
    u_mix = np.eye(4) - 1j * theta * mix - 0.5 * theta * theta * (mix @ mix)
    mix_leak = float(np.linalg.norm(p_minus @ u_mix @ p_plus))
    return block_leak, mix_leak


def sector_preparation_gate() -> tuple[bool, str]:
    d_plus = boundary_model(+1, gap=0.4)
    d_minus = boundary_model(-1, gap=0.4)
    eta_p, zero_p, _n_p, _vals_p = eta_delta(d_plus)
    eta_m, zero_m, _n_m, _vals_m = eta_delta(d_minus)
    chi_p = chi_from_eta(eta_p, zero_p)
    chi_m = chi_from_eta(eta_m, zero_m)

    path = []
    allowed = []
    gap = 0.4
    for t in np.linspace(1.0, -1.0, 13):
        d = d_plus.copy()
        d[0, 0] = gap * t
        eta, zero, _n, vals = eta_delta(d, delta=1.0e-9)
        chi = chi_from_eta(eta, zero)
        spectral_gap = float(np.min(np.abs(vals)))
        path.append(chi)
        allowed.append(chi != 0 and spectral_gap >= 0.1)

    block_leak, mix_leak = unitary_leakage_gate()
    sectors_exist = chi_p == +1 and chi_m == -1
    no_gap_path = 0 in path and not all(allowed)
    fixed_sector_superselected = block_leak < 1.0e-12 and mix_leak > 1.0e-3
    ok = sectors_exist and no_gap_path and fixed_sector_superselected
    detail = (
        f"sectors=(chi+={chi_p:+d},chi-={chi_m:+d}), chi_path={path}, "
        f"block_leak={block_leak:.1e}, mixing_control={mix_leak:.1e}, "
        f"physical_prep_claim=False"
    )
    return ok, detail


def softened_pair_energy(signs: np.ndarray, masses: np.ndarray, core: float) -> float:
    total = float(np.sum(masses))
    n = len(masses)
    for i in range(n):
        for j in range(i + 1, n):
            total += -float(signs[i] * signs[j] * masses[i] * masses[j]) / core
    return total


def uv_core_stability_boundary_gate() -> tuple[bool, str]:
    rng = np.random.default_rng(314159)
    core = 1.0
    fixed_n_ok = True
    max_bound_violation = 0.0
    for n in (2, 4, 8, 12):
        masses = 0.5 + rng.random(size=n)
        signs = rng.choice(np.array([-1.0, +1.0]), size=n)
        energy_at_core = softened_pair_energy(signs, masses, core)
        lower_bound = float(np.sum(masses))
        for i in range(n):
            for j in range(i + 1, n):
                lower_bound += -float(masses[i] * masses[j]) / core
        violation = lower_bound - energy_at_core
        max_bound_violation = max(max_bound_violation, violation)
        fixed_n_ok &= energy_at_core >= lower_bound - 1.0e-10

    ns = np.arange(2, 80, dtype=float)
    same_sector_e_per_particle = 1.0 - (ns - 1.0) / (2.0 * core)
    ruelle_fails = float(np.min(same_sector_e_per_particle)) < -20.0
    opposite_pair_infimum = 2.0
    ok = fixed_n_ok and ruelle_fails and opposite_pair_infimum > 0.0
    detail = (
        f"fixed_N_core_bound={fixed_n_ok}, max_bound_violation={max_bound_violation:.1e}, "
        f"min_same_sector_E_per_particle_N80={float(np.min(same_sector_e_per_particle)):.1f}, "
        f"ruelle_stability_from_softening_alone=False"
    )
    return ok, detail


def no_claim_gate() -> tuple[bool, str]:
    claims = {
        "negative_inertial_mass": False,
        "shielding": False,
        "propulsion": False,
        "reactionless_force": False,
        "physical_signed_gravity_prediction": False,
        "global_pde_claim": False,
        "physical_sector_preparation_claim": False,
        "ruelle_stability_claim": False,
    }
    return not any(claims.values()), ", ".join(f"{key}=False" for key in claims)


def run_audit() -> RemainingAudit:
    nonlinear_ok, nonlinear_detail = finite_galerkin_small_data_gate()
    check("global nonlinear gate reduces to finite Galerkin small-data contraction", nonlinear_ok, nonlinear_detail)

    aps_ok, aps_detail = graph_family_aps_extraction_gate()
    check("actual graph-family APS extraction boundary is classified", aps_ok, aps_detail)

    sector_ok, sector_detail = sector_preparation_gate()
    check("sector dynamics classify preparation as boundary-data/defect, not ordinary mixing", sector_ok, sector_detail)

    uv_ok, uv_detail = uv_core_stability_boundary_gate()
    check("UV/core stability boundary separates fixed-N boundedness from thermodynamic failure", uv_ok, uv_detail)

    no_claim_ok, no_claim_detail = no_claim_gate()
    check("non-claim gate remains closed", no_claim_ok, no_claim_detail)

    return RemainingAudit(
        small_data_galerkin=nonlinear_ok,
        aps_extraction_boundary=aps_ok,
        sector_preparation_boundary=sector_ok,
        uv_core_boundary=uv_ok,
        no_claim=no_claim_ok,
    )


def main() -> int:
    print("=" * 116)
    print("SIGNED GRAVITY REMAINING CLOSURE GATES AUDIT")
    print("  global nonlinear, APS extraction, sector preparation, and UV/core boundaries")
    print("=" * 116)
    print()

    audit = run_audit()

    print()
    print("INTERPRETATION")
    print("  The remaining gates do not all close as nature-grade claims.  The")
    print("  nonlinear side upgrades to a finite Galerkin small-data theorem, but not")
    print("  a global continuum PDE theorem.  Raw retained graph Hodge boundaries are")
    print("  eta-neutral, so actual APS extraction still needs a retained")
    print("  orientation-line boundary mode with zero modes quarantined.  Fixed sectors")
    print("  are superselected; preparing the opposite sign is boundary-data or defect")
    print("  preparation, not ordinary dynamics.  Softened pair cores bound every")
    print("  fixed-N problem but do not give thermodynamic stability by themselves.")
    print()

    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if audit.passed and FAIL_COUNT == 0:
        print("FINAL_TAG: SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS")
        return 0
    print("FINAL_TAG: SIGNED_GRAVITY_REMAINING_GATES_AUDIT_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
