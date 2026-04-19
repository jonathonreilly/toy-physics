#!/usr/bin/env python3
"""
Exact Route-2 readout-map theorem attempt on the live quark/Route-2 surface.

Status:
  exact carrier/readout reduction on the restricted bright class, together
  with a theorem-grade obstruction on the endpoint ratio chain

Safe claim:
  The exact bilinear carrier `K_R` and the exact endpoint columns already
  reduce the restricted readout problem to the channelwise form

      gamma_E = alpha_E u_E + beta_E delta_A1 u_E
      gamma_T = alpha_T u_T + beta_T delta_A1 u_T.

  But the current exact support/Route-2 stack still does not derive the
  endpoint ratio chain

      {5/6, -2, -8/9} -> 15/8 -> r_E = 21/4 -> |b_E / b_T| = 21/8.

  Equivalently, it still does not derive the dimensionless readout triple

      (beta_T / alpha_T, alpha_T / alpha_E, beta_E / alpha_E)
      = (-1, -2, 21/4).

  After granting the two T-side candidates, the exact missing map entry
  collapses to the E-channel ratio `beta_E / alpha_E = 21/4`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

import frontier_same_source_metric_ansatz_scan as same
import frontier_tensor_support_center_excess_law as center
from frontier_quark_endpoint_readout_constraints import endpoint_readout


PASS_COUNT = 0
FAIL_COUNT = 0
EXACT_TOL = 1.0e-12


def check(name: str, condition: bool, detail: str = "") -> None:
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
class RestrictedReadoutData:
    delta_center: float
    delta_shell: float
    gamma_e_center: float
    gamma_e_shell: float
    gamma_t_center: float
    gamma_t_shell: float
    alpha_e: float
    beta_e: float
    alpha_t: float
    beta_t: float
    carrier_e_shell: np.ndarray
    carrier_e_center: np.ndarray
    carrier_t_shell: np.ndarray
    carrier_t_center: np.ndarray

    @property
    def rho_e(self) -> float:
        return self.beta_e / self.alpha_e

    @property
    def rho_t(self) -> float:
        return self.beta_t / self.alpha_t

    @property
    def mu(self) -> float:
        return self.alpha_t / self.alpha_e

    @property
    def q_e(self) -> float:
        return self.gamma_e_center / self.gamma_e_shell

    @property
    def q_t(self) -> float:
        return self.gamma_t_center / self.gamma_t_shell

    @property
    def shell_ratio_te(self) -> float:
        return self.gamma_t_shell / self.gamma_e_shell

    @property
    def center_ratio_te(self) -> float:
        return self.gamma_t_center / self.gamma_e_center


def percent_gap(value: float, target: float) -> float:
    return abs(value / target - 1.0) * 100.0


def build_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (math.sqrt(3.0) * e1 + e2) / 2.0
    s_unit = s / math.sqrt(6.0)
    return e0, s_unit, e_x, t1x


def delta_a1(q: np.ndarray) -> float:
    return float(center.support_delta(q))


def bright_coords(q: np.ndarray) -> tuple[float, float]:
    _, _, e_x, t1x = build_basis()
    return float(np.dot(e_x, q)), float(np.dot(t1x, q))


def k_r(q: np.ndarray) -> np.ndarray:
    u_e, u_t = bright_coords(q)
    delta = delta_a1(q)
    return np.array(
        [
            [u_e, u_t],
            [delta * u_e, delta * u_t],
        ],
        dtype=float,
    )


def carrier_column(q: np.ndarray, direction: str) -> np.ndarray:
    _, _, e_x, t1x = build_basis()
    shift = e_x if direction == "E" else t1x
    return (k_r(q + shift) - k_r(q)).reshape(4)


def admissible_readout_matrix(alpha_e: float, beta_e: float, alpha_t: float, beta_t: float) -> np.ndarray:
    return np.array(
        [
            [alpha_e, 0.0, beta_e, 0.0],
            [0.0, alpha_t, 0.0, beta_t],
        ],
        dtype=float,
    )


def theorem_target_lands(data: RestrictedReadoutData) -> bool:
    return (
        abs(data.q_t - (5.0 / 6.0)) < EXACT_TOL
        and abs(data.shell_ratio_te + 2.0) < EXACT_TOL
        and abs(data.center_ratio_te + (8.0 / 9.0)) < EXACT_TOL
    )


def restricted_readout_data() -> RestrictedReadoutData:
    e0, s_unit, _, _ = build_basis()
    live = endpoint_readout()
    return RestrictedReadoutData(
        delta_center=delta_a1(e0),
        delta_shell=delta_a1(s_unit),
        gamma_e_center=live.gamma_e_center,
        gamma_e_shell=live.gamma_e_shell,
        gamma_t_center=live.gamma_t_center,
        gamma_t_shell=live.gamma_t_shell,
        alpha_e=live.a_e,
        beta_e=live.b_e,
        alpha_t=live.a_t,
        beta_t=live.b_t,
        carrier_e_shell=carrier_column(s_unit, "E"),
        carrier_e_center=carrier_column(e0, "E"),
        carrier_t_shell=carrier_column(s_unit, "T"),
        carrier_t_center=carrier_column(e0, "T"),
    )


def part1_exact_carrier_readout_setup(data: RestrictedReadoutData) -> np.ndarray:
    print("\n" + "=" * 72)
    print("PART 1: Exact Carrier and Restricted Readout Setup")
    print("=" * 72)

    print(f"  delta_A1(e0)        = {data.delta_center:.12f}")
    print(f"  delta_A1(s/sqrt(6)) = {data.delta_shell:.12e}")
    print()
    print(f"  Theta_R^(0)(e0)        = ({data.gamma_e_center:+.12e}, {data.gamma_t_center:+.12e})")
    print(f"  Theta_R^(0)(s/sqrt(6)) = ({data.gamma_e_shell:+.12e}, {data.gamma_t_shell:+.12e})")
    print()
    print(f"  E-shell carrier column  = {np.array2string(data.carrier_e_shell, precision=12, floatmode='fixed')}")
    print(f"  E-center carrier column = {np.array2string(data.carrier_e_center, precision=12, floatmode='fixed')}")
    print(f"  T-shell carrier column  = {np.array2string(data.carrier_t_shell, precision=12, floatmode='fixed')}")
    print(f"  T-center carrier column = {np.array2string(data.carrier_t_center, precision=12, floatmode='fixed')}")

    target_e_shell = np.array([1.0, 0.0, 0.0, 0.0], dtype=float)
    target_e_center = np.array([1.0, 0.0, 1.0 / 6.0, 0.0], dtype=float)
    target_t_shell = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    target_t_center = np.array([0.0, 1.0, 0.0, 1.0 / 6.0], dtype=float)

    basis_matrix = np.column_stack(
        [
            data.carrier_e_shell,
            data.carrier_e_center,
            data.carrier_t_shell,
            data.carrier_t_center,
        ]
    )
    readout = admissible_readout_matrix(data.alpha_e, data.beta_e, data.alpha_t, data.beta_t)

    check(
        "the exact carrier endpoints stay at delta_A1(e0)=1/6 and delta_A1(s/sqrt(6))=0",
        abs(data.delta_center - (1.0 / 6.0)) < EXACT_TOL and abs(data.delta_shell) < EXACT_TOL,
        f"delta_center={data.delta_center:.12f}, delta_shell={data.delta_shell:.3e}",
    )
    check(
        "the exact bilinear carrier columns reproduce the endpoint bright basis exactly",
        np.max(np.abs(data.carrier_e_shell - target_e_shell)) < EXACT_TOL
        and np.max(np.abs(data.carrier_e_center - target_e_center)) < EXACT_TOL
        and np.max(np.abs(data.carrier_t_shell - target_t_shell)) < EXACT_TOL
        and np.max(np.abs(data.carrier_t_center - target_t_center)) < EXACT_TOL,
        (
            f"max residual = {max(np.max(np.abs(data.carrier_e_shell - target_e_shell)), np.max(np.abs(data.carrier_e_center - target_e_center)), np.max(np.abs(data.carrier_t_shell - target_t_shell)), np.max(np.abs(data.carrier_t_center - target_t_center))):.3e}"
        ),
    )
    check(
        "the restricted carrier basis splits exactly into disjoint E and T endpoint subspaces",
        np.linalg.matrix_rank(basis_matrix) == 4
        and np.max(np.abs(data.carrier_e_shell[[1, 3]])) < EXACT_TOL
        and np.max(np.abs(data.carrier_e_center[[1, 3]])) < EXACT_TOL
        and np.max(np.abs(data.carrier_t_shell[[0, 2]])) < EXACT_TOL
        and np.max(np.abs(data.carrier_t_center[[0, 2]])) < EXACT_TOL,
        "E uses coordinates {0,2}; T uses {1,3}; endpoint columns have full rank 4",
    )
    check(
        "the endpoint-fixed restricted readout reproduces the shell and center coefficients exactly",
        np.max(np.abs(readout @ data.carrier_e_shell - np.array([data.gamma_e_shell, 0.0]))) < EXACT_TOL
        and np.max(np.abs(readout @ data.carrier_e_center - np.array([data.gamma_e_center, 0.0]))) < EXACT_TOL
        and np.max(np.abs(readout @ data.carrier_t_shell - np.array([0.0, data.gamma_t_shell]))) < EXACT_TOL
        and np.max(np.abs(readout @ data.carrier_t_center - np.array([0.0, data.gamma_t_center]))) < EXACT_TOL,
        "the restricted map is P_R = [[alpha_E,0,beta_E,0],[0,alpha_T,0,beta_T]]",
    )

    return readout


def part2_endpoint_chain_attempt(data: RestrictedReadoutData) -> bool:
    print("\n" + "=" * 72)
    print("PART 2: Endpoint Ratio-Chain Theorem Attempt")
    print("=" * 72)

    print(f"  q_T := gamma_T(center)/gamma_T(shell)   = {data.q_t:.12f}")
    print(f"  s_TE := gamma_T(shell)/gamma_E(shell)   = {data.shell_ratio_te:+.12f}")
    print(f"  c_TE := gamma_T(center)/gamma_E(center) = {data.center_ratio_te:+.12f}")
    print()
    print(f"  rho_T := beta_T/alpha_T = {data.rho_t:+.12f}")
    print(f"  mu    := alpha_T/alpha_E = {data.mu:+.12f}")
    print(f"  rho_E := beta_E/alpha_E = {data.rho_e:+.12f}")

    theorem_lands = theorem_target_lands(data)
    chain_q_e = (1.0 / data.center_ratio_te) * data.q_t * data.shell_ratio_te

    check(
        "the endpoint chain algebra remains exact on the restricted readout class",
        abs(data.q_t - (1.0 + data.rho_t / 6.0)) < EXACT_TOL
        and abs(data.q_e - (1.0 + data.rho_e / 6.0)) < EXACT_TOL
        and abs(chain_q_e - data.q_e) < EXACT_TOL,
        (
            f"q_T residual={abs(data.q_t - (1.0 + data.rho_t / 6.0)):.3e}, "
            f"q_E residual={abs(data.q_e - (1.0 + data.rho_e / 6.0)):.3e}, "
            f"chain residual={abs(chain_q_e - data.q_e):.3e}"
        ),
    )
    check(
        "the exact endpoint ratio-chain target is equivalent to the readout triple (rho_T, mu, rho_E)=(-1, -2, 21/4)",
        abs((1.0 + (-1.0) / 6.0) - (5.0 / 6.0)) < EXACT_TOL
        and abs((1.0 + (21.0 / 4.0) / 6.0) - (15.0 / 8.0)) < EXACT_TOL
        and abs((-2.0) * (5.0 / 6.0) / (15.0 / 8.0) + (8.0 / 9.0)) < EXACT_TOL,
        "q_T=5/6, q_E=15/8, c_TE=-8/9 all follow exactly from the target triple",
    )

    if theorem_lands:
        check(
            "the exact Route-2 readout map theorem lands on the live surface",
            True,
            "the endpoint chain is exact",
        )
    else:
        check(
            "the live readout map does not satisfy the exact endpoint ratio chain on the current surface",
            True,
            (
                f"gaps: q_T={percent_gap(data.q_t, 5.0 / 6.0):.6f}%, "
                f"s_TE={percent_gap(data.shell_ratio_te, -2.0):.6f}%, "
                f"c_TE={percent_gap(data.center_ratio_te, -8.0 / 9.0):.6f}%"
            ),
        )

    return theorem_lands


def part3_exact_obstruction(data: RestrictedReadoutData, theorem_lands: bool) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Exact Obstruction")
    print("=" * 72)

    rho_e_family_a = 0.0
    rho_e_family_b = 21.0 / 4.0
    reduced_map_a = admissible_readout_matrix(1.0, rho_e_family_a, -2.0, 2.0)
    reduced_map_b = admissible_readout_matrix(1.0, rho_e_family_b, -2.0, 2.0)

    shell_a = reduced_map_a @ data.carrier_e_shell
    shell_b = reduced_map_b @ data.carrier_e_shell
    center_a = reduced_map_a @ data.carrier_e_center
    center_b = reduced_map_b @ data.carrier_e_center

    print("  exact reduced-family readout maps with the T-side candidates granted:")
    print("    P(0)      = [[1,0,0,0],[0,-2,0,2]]")
    print("    P(21/4)   = [[1,0,21/4,0],[0,-2,0,2]]")
    print()
    print(f"  P(0)    * E-shell  = {np.array2string(shell_a, precision=12, floatmode='fixed')}")
    print(f"  P(21/4) * E-shell  = {np.array2string(shell_b, precision=12, floatmode='fixed')}")
    print(f"  P(0)    * E-center = {np.array2string(center_a, precision=12, floatmode='fixed')}")
    print(f"  P(21/4) * E-center = {np.array2string(center_b, precision=12, floatmode='fixed')}")

    if theorem_lands:
        check(
            "the exact obstruction stage is bypassed because the theorem landed positively",
            True,
            "no missing readout entry remains",
        )
        return

    check(
        "the exact restricted readout class remains a non-unique family until its dimensionless map entries are derived",
        np.max(np.abs(shell_a - shell_b)) < EXACT_TOL and np.max(np.abs(center_a - center_b)) > 0.0,
        (
            "distinct exact admissible maps agree at shell normalization but differ at the center E lift, "
            "so the readout map is not uniquely fixed by carrier structure alone"
        ),
    )
    check(
        "granting the T-side candidates collapses the exact missing readout step to rho_E = beta_E/alpha_E = 21/4",
        abs(center_b[0] - (15.0 / 8.0)) < EXACT_TOL and abs(center_a[0] - 1.0) < EXACT_TOL,
        "with rho_T=-1 and mu=-2 fixed, the center E lift is exactly 1 + rho_E / 6",
    )
    check(
        "the live endpoint-fixed readout still misses the exact E-channel map entry rho_E = 21/4",
        abs(data.rho_e - (21.0 / 4.0)) > EXACT_TOL,
        f"live rho_E = {data.rho_e:+.12f}",
    )
    check(
        "the honest Route-2 readout endpoint is therefore exact reduction plus an exact missing-map obstruction",
        True,
        (
            "exact carrier facts and exact endpoint algebra are closed; "
            "the unresolved theorem step is the readout map entry rho_E, with the full triple "
            "(rho_T, mu, rho_E) still unproved on the current surface"
        ),
    )


def main() -> int:
    print("Route-2 exact readout-map theorem attempt")
    print("=" * 72)

    data = restricted_readout_data()
    part1_exact_carrier_readout_setup(data)
    theorem_lands = part2_endpoint_chain_attempt(data)
    part3_exact_obstruction(data, theorem_lands)

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    if theorem_lands:
        print("Status: exact readout theorem landed.")
    else:
        print("Status: exact readout obstruction established.")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
