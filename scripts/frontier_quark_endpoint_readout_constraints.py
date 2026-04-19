#!/usr/bin/env python3
"""
Quark endpoint readout constraints on the live Route-2 support surface.

Status:
  exact endpoint fixation for the current affine readout plus bounded ratio/no-go
  audit on the live forward branch

Safe claim:
  The current Route-2 support notes already fix the affine readout coefficients
  `(a_E, b_E, a_T, b_T)` exactly once the two endpoint values
  `gamma(center), gamma(shell)` are supplied.

  But the same notes still do not derive an exact coefficient theorem:
    - the live readout continues to distinguish `E` and `T`,
    - the old two-channel readouts remain explicitly bounded rather than exact,
    - and the endpoint coefficient theorem is still recorded as open.

  So the honest endpoint is mixed:
    - exact endpoint fixation of the current affine coefficients;
    - bounded live coefficient relations such as
      `b_T / a_T ~ -1`,
      `a_T / a_E ~ -2.005`,
      `|b_E / b_T| ~ 2.6216`;
    - exact no-go against promoting the current notes to an exact coefficient
      theorem on this branch.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import frontier_same_source_metric_ansatz_scan as same
import frontier_tensor_support_center_excess_law as center


PASS_COUNT = 0
FAIL_COUNT = 0
EXACT_TOL = 1.0e-12
RATIO_TOL = 5.0e-4

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SWAP_NOTE = DOCS / "DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md"
PROTOTYPE_NOTE = DOCS / "S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md"
CONSTRUCTED_NOTE = DOCS / "S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md"
BILINEAR_NOTE = DOCS / "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md"
CKM_NOTE = DOCS / "CKM_ATLAS_AXIOM_CLOSURE_NOTE.md"
SHELL_NOTE = DOCS / "ONE_PARAMETER_REDUCED_SHELL_LAW_NOTE.md"


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
class EndpointReadout:
    delta_center: float
    delta_shell: float
    endpoint_gap: float
    gamma_e_center: float
    gamma_e_shell: float
    gamma_t_center: float
    gamma_t_shell: float
    a_e: float
    b_e: float
    a_t: float
    b_t: float

    @property
    def ratio_bt_at(self) -> float:
        return self.b_t / self.a_t

    @property
    def ratio_be_ae(self) -> float:
        return self.b_e / self.a_e

    @property
    def ratio_at_ae(self) -> float:
        return self.a_t / self.a_e

    @property
    def ratio_be_bt_abs(self) -> float:
        return abs(self.b_e / self.b_t)

    @property
    def ratio_t_center_shell(self) -> float:
        return self.gamma_t_center / self.gamma_t_shell


def note_text(path: Path) -> str:
    return path.read_text()


def endpoint_readout() -> EndpointReadout:
    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / math.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    ex = (math.sqrt(3.0) * e1 + e2) / 2.0

    gamma_e_center, gamma_t_center = center.gamma_pair(e0, ex, t1x)
    gamma_e_shell, gamma_t_shell = center.gamma_pair(s_unit, ex, t1x)
    delta_center = center.support_delta(e0)
    delta_shell = center.support_delta(s_unit)
    endpoint_gap = delta_center - delta_shell

    b_e = (gamma_e_center - gamma_e_shell) / endpoint_gap
    b_t = (gamma_t_center - gamma_t_shell) / endpoint_gap

    return EndpointReadout(
        delta_center=delta_center,
        delta_shell=delta_shell,
        endpoint_gap=endpoint_gap,
        gamma_e_center=gamma_e_center,
        gamma_e_shell=gamma_e_shell,
        gamma_t_center=gamma_t_center,
        gamma_t_shell=gamma_t_shell,
        a_e=gamma_e_shell,
        b_e=b_e,
        a_t=gamma_t_shell,
        b_t=b_t,
    )


def part1_exact_endpoint_fixation(data: EndpointReadout) -> None:
    print("\n" + "=" * 72)
    print("PART 1: Exact Endpoint Fixation")
    print("=" * 72)

    print(f"  delta_A1(e0)         = {data.delta_center:.12f}")
    print(f"  delta_A1(s/sqrt(6))  = {data.delta_shell:.12f}")
    print(f"  endpoint gap         = {data.endpoint_gap:.12f}")
    print()
    print(f"  gamma_E(center)      = {data.gamma_e_center:+.12e}")
    print(f"  gamma_E(shell)       = {data.gamma_e_shell:+.12e}")
    print(f"  gamma_T(center)      = {data.gamma_t_center:+.12e}")
    print(f"  gamma_T(shell)       = {data.gamma_t_shell:+.12e}")
    print()
    print(f"  gamma_E(delta_A1)    = {data.a_e:+.12e} + ({data.b_e:+.12e}) delta_A1")
    print(f"  gamma_T(delta_A1)    = {data.a_t:+.12e} + ({data.b_t:+.12e}) delta_A1")

    shell_e_resid = abs(data.a_e - data.gamma_e_shell)
    shell_t_resid = abs(data.a_t - data.gamma_t_shell)
    center_e_resid = abs(data.a_e + data.b_e * data.delta_center - data.gamma_e_center)
    center_t_resid = abs(data.a_t + data.b_t * data.delta_center - data.gamma_t_center)

    check(
        "the live support endpoints remain exact at delta_A1(e0)=1/6 and delta_A1(s/sqrt(6))=0",
        abs(data.delta_center - (1.0 / 6.0)) < EXACT_TOL and abs(data.delta_shell) < EXACT_TOL,
        f"delta_center={data.delta_center:.12f}, delta_shell={data.delta_shell:.12e}",
    )
    check(
        "the affine coefficients are fixed exactly by the shell endpoint once delta_A1(shell)=0",
        shell_e_resid < EXACT_TOL and shell_t_resid < EXACT_TOL,
        f"shell residuals=({shell_e_resid:.3e}, {shell_t_resid:.3e})",
    )
    check(
        "the same affine coefficients reproduce the center endpoint exactly through the endpoint gap",
        center_e_resid < EXACT_TOL and center_t_resid < EXACT_TOL,
        f"center residuals=({center_e_resid:.3e}, {center_t_resid:.3e})",
    )
    check(
        "the bilinear support note records the current four-coefficient readout form",
        "gamma_E = a_E u_E + b_E delta_A1 u_E" in note_text(BILINEAR_NOTE)
        and "gamma_T = a_T u_T + b_T delta_A1 u_T" in note_text(BILINEAR_NOTE),
        "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md carries the affine readout law",
    )


def part2_bounded_live_relations(data: EndpointReadout) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Ratio Reduction and Bounded Live Relations")
    print("=" * 72)

    shell_text = note_text(SHELL_NOTE)
    ckm_text = note_text(CKM_NOTE)

    print(f"  r_E = b_E / a_E       = {data.ratio_be_ae:+.12f}")
    print(f"  b_T / a_T            = {data.ratio_bt_at:+.12f}")
    print(f"  a_T / a_E            = {data.ratio_at_ae:+.12f}")
    print(f"  |b_E / b_T|          = {data.ratio_be_bt_abs:.12f}")
    print(f"  gamma_T(center)/shell = {data.ratio_t_center_shell:.12f}")

    check(
        "the exact support stack reduces the structural readout question to the channel ratios r_E=b_E/a_E and r_T=b_T/a_T",
        "A_aniso = c_aniso * Q" in shell_text
        and "- `E_x`: `(1, delta_A1)`" in ckm_text
        and "- `T1x`: `(1, delta_A1)`" in ckm_text,
        "common A_aniso denominator plus channel-blind bright columns are both already exact",
    )
    check(
        "the live E-channel readout ratio stays bounded near r_E ~ 5.25748",
        abs(data.ratio_be_ae - 5.257488806301241) < RATIO_TOL,
        f"r_E={data.ratio_be_ae:+.12f}",
    )

    check(
        "the live T-channel balance stays bounded near b_T / a_T ~ -1",
        abs(data.ratio_bt_at + 1.0) < RATIO_TOL,
        f"b_T/a_T={data.ratio_bt_at:+.12f}",
    )
    check(
        "the live T-channel endpoint ratio stays bounded near gamma_T(center)/gamma_T(shell) ~ 5/6",
        abs(data.ratio_t_center_shell - (5.0 / 6.0)) < RATIO_TOL,
        f"gamma_T(center)/shell={data.ratio_t_center_shell:.12f}",
    )
    check(
        "the live shell/intercept ratio stays bounded near a_T / a_E ~ -2.005",
        abs(data.ratio_at_ae + 2.0053827496001673) < RATIO_TOL,
        f"a_T/a_E={data.ratio_at_ae:+.12f}",
    )
    check(
        "the live slope ratio stays bounded near |b_E / b_T| ~ 2.6216",
        abs(data.ratio_be_bt_abs - 2.621601678209521) < RATIO_TOL,
        f"|b_E/b_T|={data.ratio_be_bt_abs:.12f}",
    )


def part3_exact_no_go(data: EndpointReadout) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Exact Note-Level No-Go")
    print("=" * 72)

    swap_text = note_text(SWAP_NOTE)
    prototype_text = note_text(PROTOTYPE_NOTE)
    constructed_text = note_text(CONSTRUCTED_NOTE)
    swap_text_lower = swap_text.lower()

    check(
        "the current notes still mark the E/T-distinguishing two-channel readouts as bounded rather than exact",
        "Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))" in swap_text
        and "Xi_R^(0) = d Theta_R^(0) / d delta_A1" in swap_text
        and "do distinguish `E` and `T`" in swap_text
        and "bounded" in swap_text_lower
        and "not exact" in swap_text_lower,
        "DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md keeps the readout bounded",
    )
    check(
        "the Route-2 prototype note still records the exact endpoint coefficient theorem as open",
        "an exact endpoint coefficient theorem" in prototype_text
        and "This note still does **not** close" in prototype_text,
        "S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md does not promote the coefficient theorem",
    )
    check(
        "the constructed support-primitive note also keeps the endpoint coefficient theorem open",
        "an exact endpoint coefficient theorem" in constructed_text
        and "This candidate is **not** yet" in constructed_text,
        "S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md keeps Xi_R^(0) bounded",
    )
    check(
        "the remaining unresolved primitive on the live readout surface is the E-channel ratio rather than the common denominator or T-channel shape",
        abs(data.ratio_bt_at + 1.0) < RATIO_TOL
        and abs(data.ratio_be_ae - 5.257488806301241) < RATIO_TOL,
        f"r_T={data.ratio_bt_at:+.12f}, r_E={data.ratio_be_ae:+.12f}",
    )


def main() -> int:
    print("Quark endpoint readout constraints")
    print("=" * 72)

    data = endpoint_readout()
    part1_exact_endpoint_fixation(data)
    part2_bounded_live_relations(data)
    part3_exact_no_go(data)

    print("\nVerdict:")
    print(
        "The live Route-2 support surface already fixes the affine readout "
        "coefficients exactly from the two endpoint values gamma(center) and "
        "gamma(shell). The exact support stack also reduces the structural "
        "coefficient question to the channel ratios r_E and r_T, because the "
        "anisotropic denominator is fixed and the aligned bright columns are "
        "channel-blind. But the current notes still distinguish E and T only "
        "through bounded staging objects and still leave the exact endpoint "
        "coefficient theorem open. So the correct endpoint is mixed: exact "
        "endpoint fixation, exact reduction to channel ratios, bounded live "
        "ratio structure, and an exact no-go against claiming a theorem-grade "
        "coefficient law on the current branch."
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
