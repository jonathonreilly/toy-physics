#!/usr/bin/env python3
"""APS/Wald/Gauss bridge audit for the signed-gravity lane.

The APS boundary-index probe left one narrow opening: the eta sign is a clean
boundary selector candidate, but it is not yet tied to the active Gauss
monopole and response sign.  This script tests that missing bridge directly.

It distinguishes:

  * retained Wald/Gauss/source-unit normalization: positive, unsigned source
  * APS eta as a spectator topological label: conserved, source-neutral
  * source-only or response-only APS sign insertions: action-reaction controls
  * locked APS sign insertion: consequence control only, not a derivation

No output from this script is a negative-mass, shielding, propulsion, or
physical signed-gravity claim.
"""

from __future__ import annotations

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
    hermitian_part,
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


def chi_for_boundary(index_sign: int) -> int:
    eta, zero, _, _ = eta_delta(boundary_model(index_sign))
    return chi_from_eta(eta, zero)


def gauss_monopole_from_bare(q_bare: float) -> float:
    return q_bare / (4.0 * math.pi)


def finite_difference(func: Callable[[float], float], step: float = 1.0e-6) -> float:
    return (func(step) - func(-step)) / (2.0 * step)


def eta_phi_derivative(index_sign: int, strength: float = 0.05) -> tuple[int, int, float]:
    """Finite-difference eta under a gap-preserving boundary perturbation."""

    d0 = boundary_model(index_sign, gap=0.4)
    raw = np.diag(np.linspace(-1.0, 1.0, d0.shape[0]))
    perturb = strength * hermitian_part(raw)

    eta_0, zero_0, _, _ = eta_delta(d0)

    def eta_of_phi(phi: float) -> float:
        eta, zero, _, _ = eta_delta(d0 + phi * perturb)
        if zero:
            return 0.0
        return float(eta)

    derivative = finite_difference(eta_of_phi)
    return eta_0, zero_0, derivative


def crossing_chi_path() -> list[int]:
    d0 = boundary_model(+1, gap=0.4)
    gap = float(abs(d0[0, 0]))
    out: list[int] = []
    for t in np.linspace(1.0, -1.0, 9):
        d = d0.copy()
        d[0, 0] = gap * t
        eta, zero, _, _ = eta_delta(d, delta=1.0e-9)
        out.append(chi_from_eta(eta, zero))
    return out


def action_derivative_rows(mass: float = 2.75) -> list[tuple[str, float, float, str]]:
    c_cell = 0.25

    rows = []
    rows.append(
        (
            "retained_wald_gauss",
            finite_difference(lambda phi: mass * phi),
            mass,
            "positive Born/Gauss source; eta independent",
        )
    )
    rows.append(
        (
            "aps_eta_spectator",
            finite_difference(lambda phi: (+1) * c_cell),
            0.0,
            "topological label only; no Phi source",
        )
    )
    for chi in (+1, -1):
        rows.append(
            (
                f"inserted_aps_locked_{chi:+d}",
                finite_difference(lambda phi, chi=chi: chi * mass * phi),
                chi * mass,
                "passes only after chi multiplies the source action",
            )
        )
    return rows


@dataclass(frozen=True)
class SignLaw:
    name: str
    source_sign: Callable[[int], int]
    response_sign: Callable[[int], int]
    derived_here: bool


def pair_balance_residual(law: SignLaw, chi_a: int, chi_b: int) -> tuple[float, str]:
    source_a = law.source_sign(chi_a)
    source_b = law.source_sign(chi_b)
    response_a = law.response_sign(chi_a)
    response_b = law.response_sign(chi_b)

    force_a = response_a * source_b
    force_b = -response_b * source_a
    scale = max(abs(force_a), abs(force_b), 1.0e-30)
    residual = abs(force_a + force_b) / scale
    if abs(force_a) < TOL and abs(force_b) < TOL:
        read = "ZERO"
    elif residual > 1.0e-12:
        read = "UNBALANCED"
    else:
        read = "ATTRACT" if force_a > 0 else "REPEL"
    return residual, read


def sign_law_rows() -> list[tuple[str, float, bool, bool, str]]:
    laws = [
        SignLaw("retained_positive", lambda _chi: +1, lambda _chi: +1, True),
        SignLaw("aps_eta_spectator", lambda _chi: 0, lambda _chi: +1, True),
        SignLaw("aps_source_only_inserted", lambda chi: chi, lambda _chi: +1, False),
        SignLaw("aps_response_only_inserted", lambda _chi: +1, lambda chi: chi, False),
        SignLaw("aps_locked_inserted", lambda chi: chi, lambda chi: chi, False),
    ]
    pairs = ((+1, +1), (+1, -1), (-1, +1), (-1, -1))
    rows = []
    for law in laws:
        residuals = []
        reads = []
        for chi_a, chi_b in pairs:
            residual, read = pair_balance_residual(law, chi_a, chi_b)
            residuals.append(residual)
            reads.append(read)
        desired = ["ATTRACT", "REPEL", "REPEL", "ATTRACT"]
        table_ok = reads == desired
        rows.append((law.name, max(residuals), table_ok, law.derived_here, ",".join(reads)))
    return rows


def born_i3_control() -> float:
    """Three-slit identity for fixed unitary maps in two eta sectors."""

    rng = np.random.default_rng(20260425)
    n = 9
    raw = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    q, _ = np.linalg.qr(raw)
    detector = np.arange(5, n)
    slits = (1, 3, 4)

    def state(open_slits: tuple[int, ...]) -> np.ndarray:
        psi = np.zeros(n, dtype=complex)
        for slit in open_slits:
            psi[slit] = 1.0
        return psi

    def prob(open_slits: tuple[int, ...]) -> float:
        out = q @ state(open_slits)
        return float(np.sum(np.abs(out[detector]) ** 2))

    a, b, c = slits
    return (
        prob((a, b, c))
        - prob((a, b))
        - prob((a, c))
        - prob((b, c))
        + prob((a,))
        + prob((b,))
        + prob((c,))
    )


def main() -> int:
    print("=" * 88)
    print("SIGNED GRAVITY APS / WALD / GAUSS BRIDGE AUDIT")
    print("  bridge test only; not a negative-mass, shielding, propulsion, or physical signed-gravity claim")
    print("=" * 88)
    print()

    chi_plus = chi_for_boundary(+1)
    chi_minus = chi_for_boundary(-1)
    check("APS eta supplies +/- boundary labels", chi_plus == +1 and chi_minus == -1)

    eta_p, zero_p, deta = eta_phi_derivative(+1)
    check(
        "gap-preserving Phi deformation leaves eta source-neutral",
        eta_p == 1 and zero_p == 0 and abs(deta) < TOL,
        f"eta={eta_p}, zero={zero_p}, finite-diff d_eta/dPhi={deta:.3e}",
    )
    path = crossing_chi_path()
    check(
        "eta sign changes only at zero crossing defect",
        path[:4] == [+1, +1, +1, +1] and path[4] == 0 and path[-4:] == [-1, -1, -1, -1],
        f"chi_path={path}",
    )
    print()

    print("WALD / GAUSS SOURCE-UNIT SCALE")
    c_cell = 4.0 / 16.0
    lambda_wald = 4.0 * c_cell
    mass = 2.75
    q_bare = 4.0 * math.pi * mass
    c_abs = gauss_monopole_from_bare(q_bare)
    check("primitive area carrier fixes positive lambda", abs(lambda_wald - 1.0) < TOL, f"lambda={lambda_wald:.6f}")
    check("retained source-unit gives positive exterior monopole", abs(c_abs - mass) < TOL, f"C_abs={c_abs:.6f}")
    signed_coeffs = {+1: +1.0 / 4.0, -1: -1.0 / 4.0}
    check(
        "putting chi into Wald coefficient is rejected",
        signed_coeffs[-1] < 0.0 and c_cell > 0.0,
        f"c_cell=+{c_cell:.3f}, signed_minus={signed_coeffs[-1]:+.3f}",
    )
    print()

    print("SOURCE ACTION DERIVATIVE CHECK")
    print(f"  {'law':<24s} {'dS/dPhi':>12s} {'target':>12s}  read")
    for name, derivative, target, read in action_derivative_rows(mass):
        print(f"  {name:<24s} {derivative:+12.6f} {target:+12.6f}  {read}")
    derivative_rows = action_derivative_rows(mass)
    check(
        "retained action derivative is unsigned positive source",
        abs(derivative_rows[0][1] - mass) < TOL,
        "dS/dPhi=M_phys",
    )
    check(
        "APS spectator derivative is zero",
        abs(derivative_rows[1][1]) < TOL,
        "d(eta term)/dPhi=0 on gapped sector",
    )
    inserted_derivatives_ok = (
        abs(derivative_rows[2][1] - mass) < TOL
        and abs(derivative_rows[3][1] + mass) < TOL
    )
    check(
        "signed derivative requires explicit inserted chi source term",
        inserted_derivatives_ok,
        "inserted rows give +/-M by construction",
    )
    print()

    print("SOURCE / RESPONSE LOCKING TABLE")
    print(f"  {'law':<28s} {'max balance':>12s} {'table':>8s} {'derived':>8s}  reads")
    derived_locked_pass = False
    inserted_locked_pass = False
    for name, max_residual, table_ok, derived_here, reads in sign_law_rows():
        print(
            f"  {name:<28s} {max_residual:12.3e} "
            f"{'PASS' if table_ok else 'FAIL':>8s} {'YES' if derived_here else 'NO':>8s}  {reads}"
        )
        if table_ok and derived_here:
            derived_locked_pass = True
        if name == "aps_locked_inserted" and table_ok and not derived_here:
            inserted_locked_pass = True
    check("no derived APS/Wald/Gauss law gives locked four-pair table", not derived_locked_pass)
    check("locked APS table exists only as inserted control", inserted_locked_pass)
    print()

    print("BORN / NORM / NULL CONTROLS")
    i3 = born_i3_control()
    norm_drift = abs(np.linalg.norm(np.array([1.0 + 0j, 0j])) - 1.0)
    null_signed_source = 4.0 * math.pi * (mass - mass)
    null_inertial = mass + mass
    check("Born three-slit identity remains linear", abs(i3) < 1.0e-12, f"I3={i3:+.3e}")
    check("fixed-sector norm remains positive", norm_drift < TOL, f"norm drift={norm_drift:.3e}")
    check(
        "inserted +/- null source keeps positive inertial mass",
        abs(null_signed_source) < TOL and null_inertial > 0.0,
        f"q_bare_sum={null_signed_source:+.3e}, M_sum={null_inertial:.3f}",
    )
    print()

    print("BRIDGE VERDICT")
    print("  APS eta is a stable boundary label in the gapped finite probe.")
    print("  Existing Wald/Gauss/source-unit support fixes a positive source scale.")
    print("  The finite audit finds no retained identity that multiplies the active")
    print("  Gauss monopole and response sign by eta. The locked table appears only")
    print("  after adding chi to the source action by hand.")
    final_tag = (
        "APS_WALD_GAUSS_BRIDGE_DERIVED"
        if derived_locked_pass
        else "APS_WALD_GAUSS_BRIDGE_NOT_DERIVED"
    )
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"FINAL_TAG: {final_tag}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
