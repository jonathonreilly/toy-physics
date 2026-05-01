#!/usr/bin/env python3
"""
DM neutrino source-surface scalar-baseline active quadratic diagnostic.

This runner records a bounded comparison tool, not a selector theorem.
On the chosen scalar baseline D = m I_3, the observable-principle zero-source
curvature on the live active pair is isotropic and gives the exact diagnostic
quadratic

    Q_scalar(delta, q_+) = 6(delta^2 + q_+^2).

Minimizing that diagnostic on the exact active chamber

    q_+ >= sqrt(8/3) - delta

returns the point delta_* = q_+* = sqrt(6)/3.

This does not prove that the physical selector law is already closed. The
runner therefore also checks that generic positive baselines are not isotropic
on the active pair.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    tdelta,
    tq,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import (
    active_half_plane_h,
    q_floor,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def active_source(delta: float, q_plus: float) -> np.ndarray:
    return delta * tdelta() + q_plus * tq()


def exact_det_formula(mass: float, delta: float, q_plus: float) -> float:
    return (mass + 2.0 * q_plus) * ((mass - q_plus) ** 2 - 3.0 * delta * delta)


def diagnostic_curvature(diagonal: np.ndarray, x: np.ndarray, y: np.ndarray) -> float:
    dinv = np.diag(1.0 / diagonal)
    return float(np.real(np.trace(dinv @ x @ dinv @ y)))


def delta_star() -> float:
    return math.sqrt(6.0) / 3.0


def q_star() -> float:
    return math.sqrt(6.0) / 3.0


def part1_scalar_baseline_source_response_is_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SCALAR-BASELINE SOURCE RESPONSE IS EXACT ON THE ACTIVE PAIR")
    print("=" * 88)

    obs_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    diag_note = read(
        "docs/DM_NEUTRINO_SOURCE_SURFACE_SCALAR_BASELINE_ACTIVE_QUADRATIC_DIAGNOSTIC_NOTE_2026-04-17.md"
    )

    mass = 2.3
    samples = [(0.2, 1.1), (-0.4, 1.7), (0.8, 0.9)]
    ok_det = True
    max_err = 0.0
    for delta, q_plus in samples:
        det_direct = float(np.real(np.linalg.det(mass * np.eye(3) + active_source(delta, q_plus))))
        det_exact = exact_det_formula(mass, delta, q_plus)
        err = abs(det_direct - det_exact)
        max_err = max(max_err, err)
        ok_det &= err < 1e-10

    check(
        "The observable-principle note records the unique additive scalar generator",
        "W[J] = log|det(D+J)| - log|det D|" in obs_note
        or "W[J] = log |det(D+J)| - log |det D|" in obs_note,
    )
    check(
        "The diagnostic note is explicitly framed as a bounded diagnostic tool",
        "bounded diagnostic tool" in diag_note and "does **not** close the DM selector law" in diag_note,
    )
    check(
        "On a scalar baseline, the active determinant family matches the exact closed formula",
        ok_det,
        f"max det error={max_err:.2e}",
    )


def part2_scalar_baseline_curvature_is_isotropic() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SCALAR-BASELINE CURVATURE IS EXACTLY ISOTROPIC")
    print("=" * 88)

    td = tdelta()
    tqm = tq()
    mass = 1.9
    diagonal = np.array([mass, mass, mass], dtype=float)

    kdd = diagnostic_curvature(diagonal, td, td)
    kqq = diagnostic_curvature(diagonal, tqm, tqm)
    kdq = diagnostic_curvature(diagonal, td, tqm)

    check(
        "The active generators are Frobenius-orthogonal with equal norm",
        abs(float(np.real(np.trace(td @ td))) - 6.0) < 1e-12
        and abs(float(np.real(np.trace(tqm @ tqm))) - 6.0) < 1e-12
        and abs(float(np.real(np.trace(td @ tqm)))) < 1e-12,
    )
    check(
        "The scalar-baseline curvature gives K(T_delta,T_delta) = 6/m^2",
        abs(kdd - 6.0 / (mass * mass)) < 1e-12,
        f"Kdd={kdd:.12f}",
    )
    check(
        "The scalar-baseline curvature gives K(T_q,T_q) = 6/m^2",
        abs(kqq - 6.0 / (mass * mass)) < 1e-12,
        f"Kqq={kqq:.12f}",
    )
    check(
        "The scalar-baseline curvature gives K(T_delta,T_q) = 0",
        abs(kdq) < 1e-12,
        f"Kdq={kdq:.12f}",
    )


def part3_generic_positive_baselines_do_not_define_the_same_tool() -> None:
    print("\n" + "=" * 88)
    print("PART 3: GENERIC POSITIVE BASELINES ARE NOT ISOTROPIC ON THE ACTIVE PAIR")
    print("=" * 88)

    td = tdelta()
    tqm = tq()
    diagonal = np.array([1.0, 2.0, 3.0], dtype=float)

    kdd = diagnostic_curvature(diagonal, td, td)
    kqq = diagnostic_curvature(diagonal, tqm, tqm)
    kdq = diagnostic_curvature(diagonal, td, tqm)

    check(
        "A generic positive baseline breaks the scalar-baseline isotropy",
        abs(kdd - kqq) > 1e-6 or abs(kdq) > 1e-6,
        f"(Kdd,Kqq,Kdq)=({kdd:.12f},{kqq:.12f},{kdq:.12f})",
    )
    check(
        "So the recorded quadratic is a scalar-baseline diagnostic, not a baseline-independent selector law",
        abs(kdq) > 1e-6,
        f"Kdq={kdq:.12f}",
    )


def part4_the_diagnostic_minimizer_is_exact_on_the_active_chamber() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE DIAGNOSTIC MINIMIZER IS EXACT ON THE ACTIVE CHAMBER")
    print("=" * 88)

    d_sel = delta_star()
    q_sel = q_star()

    def qb_action(delta: float) -> float:
        q_plus = q_floor(delta)
        return 6.0 * (delta * delta + q_plus * q_plus)

    deriv = 24.0 * d_sel - 8.0 * math.sqrt(6.0)
    center = qb_action(d_sel)
    left = qb_action(d_sel - 0.2)
    right = qb_action(d_sel + 0.2)
    boundary_ok = abs(q_sel - q_floor(d_sel)) < 1e-12
    _, r31, phi = active_half_plane_h(d_sel, q_sel, m=0.0)

    check(
        "The chamber minimizer lies on the exact active boundary",
        boundary_ok,
        f"(delta_*,q_+*)=({d_sel:.12f},{q_sel:.12f})",
    )
    check(
        "The boundary diagnostic is stationary at delta_* = sqrt(6)/3",
        abs(deriv) < 1e-12,
        f"Q'_bdy(delta_*)={deriv:.12f}",
    )
    check(
        "Strict convexity makes that point the unique chamber minimizer",
        center < left and center < right,
        f"Q*=({center:.12f}) left=({left:.12f}) right=({right:.12f})",
    )
    check(
        "The selected chamber point reads back as r31 = 1/2 and phi_+ = pi/2",
        abs(r31 - 0.5) < 1e-12 and abs(phi - 0.5 * math.pi) < 1e-12,
        f"(r31,phi)=({r31:.12f},{phi:.12f})",
    )


def part5_the_note_records_the_boundary_honestly() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE RECORDS THE DIAGNOSTIC BOUNDARY HONESTLY")
    print("=" * 88)

    note = read(
        "docs/DM_NEUTRINO_SOURCE_SURFACE_SCALAR_BASELINE_ACTIVE_QUADRATIC_DIAGNOSTIC_NOTE_2026-04-17.md"
    )

    check(
        "The note records the scalar-baseline quadratic and chamber minimizer",
        "Q_scalar(delta,q_+) = 6(delta^2 + q_+^2)" in note
        and "delta_* = q_+* = sqrt(6)/3" in note,
    )
    check(
        "The note explicitly says this does not close the DM selector law",
        "does **not** close the DM selector law" in note
        and "not authority for the live DM selector closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SCALAR-BASELINE ACTIVE QUADRATIC DIAGNOSTIC")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is there a useful exact comparison quadratic on the live active pair")
    print("  without promoting it into a false selector-closure theorem?")

    part1_scalar_baseline_source_response_is_exact()
    part2_scalar_baseline_curvature_is_isotropic()
    part3_generic_positive_baselines_do_not_define_the_same_tool()
    part4_the_diagnostic_minimizer_is_exact_on_the_active_chamber()
    part5_the_note_records_the_boundary_honestly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Safe landing:")
    print("    - scalar-baseline active quadratic recorded exactly")
    print("    - chamber minimizer recorded exactly")
    print("    - generic baselines do not give the same isotropic law")
    print("    - tool is diagnostic only, not DM selector closure")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
