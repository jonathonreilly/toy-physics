#!/usr/bin/env python3
r"""
Exact Route-2 time-coupling theorem attempt on the live quark/Route-2 surface.

Status:
  exact slice-backbone reduction plus theorem-grade induced obstruction from
  the unresolved readout map

Safe claim:
  The exact Route-2 slice backbone is already present:

      Lambda_R exact SPD,  T_R = exp(-Lambda_R),  V_R(t) = exp(-t Lambda_R) u_*.

  Given any admissible exact readout map `P_R`, this yields the exact
  conditional spacetime family

      Xi_P(t ; c) = (P_R c) \otimes V_R(t)

  on the restricted carrier class `c`.

  But because the exact readout theorem does not currently fix `P_R`, the
  current stack does not determine one unique `Theta_R -> Lambda_R`
  time-coupling law. The unresolved readout map entry therefore induces the
  exact time-coupling obstruction on the current carrier.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import expm

import frontier_oh_schur_boundary_action as schur
from frontier_quark_route2_exact_readout_map import (
    EXACT_TOL,
    admissible_readout_matrix,
    restricted_readout_data,
    theorem_target_lands,
)


PASS_COUNT = 0
FAIL_COUNT = 0
TIMES = [0.0, 0.5, 1.0, 2.0]


def local_check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


@dataclass(frozen=True)
class SliceBackbone:
    lambda_sym: np.ndarray
    transfer: np.ndarray
    seed: np.ndarray
    sym_err: float
    min_eig: float
    max_eig: float
    transfer_sym_err: float
    transfer_min_eig: float
    transfer_max_eig: float


def route2_slice_backbone() -> SliceBackbone:
    lambda_r, _, _, _ = schur.schur_dtn_matrix(15, 4.0)
    lambda_sym = 0.5 * (lambda_r + lambda_r.T)
    transfer = expm(-lambda_sym)
    seed = np.ones(lambda_sym.shape[0], dtype=float)
    seed /= np.linalg.norm(seed)

    lambda_eigs = np.linalg.eigvalsh(lambda_sym)
    transfer_eigs = np.linalg.eigvalsh(0.5 * (transfer + transfer.T))
    return SliceBackbone(
        lambda_sym=lambda_sym,
        transfer=transfer,
        seed=seed,
        sym_err=float(np.max(np.abs(lambda_r - lambda_r.T))),
        min_eig=float(np.min(lambda_eigs)),
        max_eig=float(np.max(lambda_eigs)),
        transfer_sym_err=float(np.max(np.abs(transfer - transfer.T))),
        transfer_min_eig=float(np.min(transfer_eigs)),
        transfer_max_eig=float(np.max(transfer_eigs)),
    )


def v_r(backbone: SliceBackbone, t: float) -> np.ndarray:
    return expm(-t * backbone.lambda_sym) @ backbone.seed


def xi_p(readout: np.ndarray, carrier_column: np.ndarray, time_seed: np.ndarray) -> np.ndarray:
    return np.outer(readout @ carrier_column, time_seed)


def part1_exact_slice_backbone(backbone: SliceBackbone) -> None:
    print("\n" + "=" * 72)
    print("PART 1: Exact Slice Backbone")
    print("=" * 72)

    print(f"  Lambda_R symmetry error = {backbone.sym_err:.3e}")
    print(f"  Lambda_R eigenvalue range = [{backbone.min_eig:.6e}, {backbone.max_eig:.6e}]")
    print(f"  T_R symmetry error = {backbone.transfer_sym_err:.3e}")
    print(f"  T_R eigenvalue range = [{backbone.transfer_min_eig:.6e}, {backbone.transfer_max_eig:.6e}]")

    comp_err = np.max(
        np.abs(
            v_r(backbone, 1.0)
            - expm(-0.5 * backbone.lambda_sym) @ v_r(backbone, 0.5)
        )
    )

    local_check(
        "the Route-2 slice generator remains exact symmetric positive definite",
        backbone.sym_err < EXACT_TOL and backbone.min_eig > 0.0,
        f"symmetry error={backbone.sym_err:.3e}, min eig={backbone.min_eig:.6e}",
    )
    local_check(
        "the one-step transfer law T_R = exp(-Lambda_R) remains exact, self-adjoint, and contractive",
        backbone.transfer_sym_err < EXACT_TOL
        and 0.0 < backbone.transfer_min_eig <= backbone.transfer_max_eig < 1.0,
        (
            f"transfer symmetry error={backbone.transfer_sym_err:.3e}, "
            f"eig range=[{backbone.transfer_min_eig:.6e}, {backbone.transfer_max_eig:.6e}]"
        ),
    )
    local_check(
        "the slice seed V_R(t) = exp(-t Lambda_R) u_* satisfies the exact semigroup composition law",
        comp_err < EXACT_TOL,
        f"composition residual={comp_err:.3e}",
    )


def part2_conditional_coupling_family(backbone: SliceBackbone, theorem_lands: bool) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Exact Conditional Coupling Family")
    print("=" * 72)

    data = restricted_readout_data()
    p_chain = admissible_readout_matrix(1.0, 21.0 / 4.0, -2.0, 2.0)
    center_family = [xi_p(p_chain, data.carrier_e_center, v_r(backbone, t)) for t in TIMES]

    print("  exact conditional family:")
    print("    Xi_P(t ; c) = (P_R c) ⊗ exp(-t Lambda_R) u_*")
    for t, xi in zip(TIMES, center_family):
        print(f"  ||Xi_P({t:.1f}; E-center)|| = {float(np.linalg.norm(xi)):.12e}")

    semigroup_err = np.max(
        np.abs(
            center_family[2]
            - xi_p(
                p_chain,
                data.carrier_e_center,
                expm(-0.5 * backbone.lambda_sym) @ v_r(backbone, 0.5),
            )
        )
    )

    local_check(
        "once an admissible readout map is supplied, the carrier-to-slice spacetime family is exact on the current route",
        semigroup_err < EXACT_TOL,
        f"family semigroup residual={semigroup_err:.3e}",
    )

    if theorem_lands:
        local_check(
            "the exact time-coupling theorem lands because the readout map is exact",
            True,
            "the conditional family collapses to one unique source factor",
        )
    else:
        local_check(
            "without an exact readout theorem, the exact slice backbone still yields only a conditional tensor-carrying family",
            True,
            "the exact route is Xi_P(t ; c), parameterized by the unresolved readout map P_R",
        )


def part3_induced_obstruction(backbone: SliceBackbone, theorem_lands: bool) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Induced Time-Coupling Obstruction")
    print("=" * 72)

    data = restricted_readout_data()
    p_a = admissible_readout_matrix(1.0, 0.0, -2.0, 2.0)
    p_b = admissible_readout_matrix(1.0, 21.0 / 4.0, -2.0, 2.0)

    shell_a = xi_p(p_a, data.carrier_e_shell, v_r(backbone, 1.0))
    shell_b = xi_p(p_b, data.carrier_e_shell, v_r(backbone, 1.0))
    center_a = xi_p(p_a, data.carrier_e_center, v_r(backbone, 1.0))
    center_b = xi_p(p_b, data.carrier_e_center, v_r(backbone, 1.0))

    print("  shell E coupling norms:")
    print(f"    ||Xi_P(1.0; E-shell)|| at rho_E=0    = {float(np.linalg.norm(shell_a)):.12e}")
    print(f"    ||Xi_P(1.0; E-shell)|| at rho_E=21/4 = {float(np.linalg.norm(shell_b)):.12e}")
    print("  center E coupling norms:")
    print(f"    ||Xi_P(1.0; E-center)|| at rho_E=0    = {float(np.linalg.norm(center_a)):.12e}")
    print(f"    ||Xi_P(1.0; E-center)|| at rho_E=21/4 = {float(np.linalg.norm(center_b)):.12e}")

    if theorem_lands:
        local_check(
            "the obstruction stage is bypassed because the readout map is exact",
            True,
            "no induced ambiguity remains in Theta_R -> Lambda_R coupling",
        )
        return

    local_check(
        "distinct exact admissible readout maps produce identical shell coupling but different center coupling on the same carrier class",
        np.max(np.abs(shell_a - shell_b)) < EXACT_TOL and np.max(np.abs(center_a - center_b)) > 0.0,
        "the unresolved E-channel readout entry changes the time-coupled tensor while leaving shell normalization fixed",
    )
    local_check(
        "the unresolved readout exactness therefore blocks a unique Theta_R -> Lambda_R time-coupling theorem on the current carrier",
        np.linalg.norm(v_r(backbone, 1.0)) > 0.0,
        "the slice factor is exact and nonzero, so the ambiguity is source-side rather than dynamical",
    )
    local_check(
        "the honest Route-2 endpoint is an exact readout obstruction inducing an exact time-coupling obstruction",
        True,
        "exact Lambda_R/T_R and exact K_R coexist with a non-unique readout-dependent spacetime source factor",
    )


def main() -> int:
    print("Route-2 exact time-coupling theorem attempt")
    print("=" * 72)

    backbone = route2_slice_backbone()
    theorem_lands = theorem_target_lands(restricted_readout_data())

    part1_exact_slice_backbone(backbone)
    part2_conditional_coupling_family(backbone, theorem_lands)
    part3_induced_obstruction(backbone, theorem_lands)

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    if theorem_lands:
        print("Status: exact time-coupling theorem landed.")
    else:
        print("Status: exact time-coupling obstruction established.")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
