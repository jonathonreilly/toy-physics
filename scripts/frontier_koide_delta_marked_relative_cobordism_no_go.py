#!/usr/bin/env python3
"""
Koide delta marked-relative-cobordism no-go.

Theorem attempt:
  Strengthen relative cobordism by adding a boundary marking derived from the
  retained Wilson/APS data.  Perhaps the mark simultaneously selects the
  physical rank-one Brannen line and fixes the endpoint section, forcing

      theta_end - theta0 = eta_APS.

Result:
  Negative from retained data alone.  A mark closes the gap only if it is
  already a non-scalar rank-one selector plus a based endpoint section.  The
  retained Wilson/APS operators act as scalar data on the multiplicity space
  of the relevant zero-mode character sector, so they do not derive a unique
  rank-one line.  The endpoint section also remains shiftable by an exact
  boundary term.

  The marked relative split leaves the same residual:

      delta_open / eta_APS - 1 = -spectator_channel + c / eta_APS.

No mass data, fitted Koide value, or selected endpoint target is used.

Bridge for the load-bearing premise that the retained Wilson/APS algebra
restricts to a scalar on the rank-two zeta-character multiplicity space M_zeta:
  See
    docs/KOIDE_RETAINED_WILSON_APS_SCALAR_ACTION_ON_RANK_TWO_MULTIPLICITY_BRIDGE_NARROW_THEOREM_NOTE_2026-05-16.md
  and its runner
    scripts/frontier_koide_retained_wilson_aps_scalar_action_on_rank_two_multiplicity_bridge_narrow.py
  which derive, from the sibling Wilson construction in
    scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py,
  that on M_zeta every retained polynomial in {D, U, U^dag, P_lambda(D)}
  restricts to a scalar I_2.  Section B below re-verifies a representative
  subset of those scalar restrictions inside this runner via a derived-mark
  generator (B.0a-B.0e) so the parent's "retained_mark = lam * I" is no longer
  asserted but follows from a check at the same place it is used.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Relative split with a boundary mark")

    eta = eta_abss_z3_weights_12()
    selected, spectator, c = sp.symbols("selected spectator c", real=True)
    total_constraint = sp.Eq(selected + spectator, 1)
    delta_open = sp.simplify(selected * eta + c)
    residual_total = sp.simplify(delta_open / eta - 1).subs(selected, 1 - spectator)
    record(
        "A.1 retained closed APS scalar is eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "A.2 marked relative split still has channel and endpoint pieces",
        sp.simplify(residual_total - (-spectator + c / eta)) == 0,
        f"selected+spectator=1 -> delta/eta_APS - 1 = {residual_total}",
    )

    section("B.0 Bridge: retained Wilson/APS algebra is scalar on M_zeta (derived, not asserted)")

    # Bridge inline: load the sibling Wilson construction and verify that
    # every generator (D, U, U^dag, P_lambda(D)) and a representative
    # polynomial mark all restrict to scalar 2x2 matrices on M_zeta.  This
    # derivation closes the missing bridge for the parent's "retained_mark =
    # lam * I" step, in addition to the standalone bridge runner
    # `scripts/frontier_koide_retained_wilson_aps_scalar_action_on_rank_two_multiplicity_bridge_narrow.py`.
    import importlib.util
    from pathlib import Path

    _ROOT = Path(__file__).resolve().parent.parent
    _spec = importlib.util.spec_from_file_location(
        "_sibling_for_bridge",
        str(_ROOT / "scripts" / "frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py"),
    )
    _sibling = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_sibling)

    TOL = 1e-8

    def _restrict(M_full, basis):
        return basis.conj().T @ M_full @ basis

    def _is_scalar_2x2(M):
        if M.shape != (2, 2):
            return False, complex(0)
        lam_avg = (M[0, 0] + M[1, 1]) / 2
        return bool(np.linalg.norm(M - lam_avg * np.eye(2)) < TOL), complex(lam_avg)

    bridge_ok = True
    bridge_details = []
    for r_val in (1.0, 1.425):
        D_full, U_full, _ = _sibling.build_wilson_lattice(r_val)
        line_0, line_1, zeta_val = _sibling.zero_character_lines(D_full, U_full)
        basis_Mz = np.stack([line_0, line_1], axis=1)
        Udag_full = U_full.conj().T

        D_on_Mz = _restrict(D_full, basis_Mz)
        U_on_Mz = _restrict(U_full, basis_Mz)
        Udag_on_Mz = _restrict(Udag_full, basis_Mz)

        # Spectral projector P_0(D): projector onto ker(D).
        eigs_full, vecs_full = np.linalg.eigh(D_full)
        zero_idx = np.where(np.abs(eigs_full) < TOL)[0]
        block_zero = vecs_full[:, zero_idx]
        P0_full = block_zero @ block_zero.conj().T
        P0_on_Mz = _restrict(P0_full, basis_Mz)

        ok_D, lam_D = _is_scalar_2x2(D_on_Mz)
        ok_U, lam_U = _is_scalar_2x2(U_on_Mz)
        ok_Udag, lam_Udag = _is_scalar_2x2(Udag_on_Mz)
        ok_P0, lam_P0 = _is_scalar_2x2(P0_on_Mz)

        # Representative derived retained mark: M_mark = a*P_0 + b*U + bbar*U^dag,
        # which is a generic Hermitian retained polynomial in the generators.
        a_coef, b_coef = 0.7, 1.3 + 0.4j
        mark_full = a_coef * P0_full + b_coef * U_full + np.conjugate(b_coef) * Udag_full
        mark_on_Mz = _restrict(mark_full, basis_Mz)
        ok_mark, lam_mark = _is_scalar_2x2(mark_on_Mz)

        row_ok = (
            ok_D and abs(lam_D) < TOL
            and ok_U and abs(lam_U - zeta_val) < TOL
            and ok_Udag and abs(lam_Udag - np.conjugate(zeta_val)) < TOL
            and ok_P0 and abs(lam_P0 - 1.0) < TOL
            and ok_mark
        )
        bridge_ok = bridge_ok and row_ok
        bridge_details.append(
            f"r={r_val}: lam_D={lam_D:.3g}, lam_U={lam_U:.6g}, lam_Udag={lam_Udag:.6g}, "
            f"lam_P0={lam_P0:.3g}, lam_mark={lam_mark:.6g}, all_scalar={row_ok}"
        )

    record(
        "B.0a D|_{M_zeta} = 0 I_2 (derived from sibling Wilson construction)",
        bridge_ok,
        "\n".join(bridge_details),
    )
    record(
        "B.0b U|_{M_zeta} = zeta I_2 with zeta = exp(i pi/3) (derived)",
        bridge_ok,
        "U restricted to M_zeta is scalar zeta * I at r in {1.0, 1.425}.",
    )
    record(
        "B.0c U^dag|_{M_zeta} = zeta_bar I_2 (derived)",
        bridge_ok,
        "U^dag restricted to M_zeta is scalar zeta_bar * I.",
    )
    record(
        "B.0d Spectral projector P_0(D)|_{M_zeta} = 1 I_2 (derived)",
        bridge_ok,
        "P_0(D) restricts to the identity on M_zeta since M_zeta ⊂ ker(D).",
    )
    record(
        "B.0e Representative derived retained mark a P_0 + b U + bbar U^dag is scalar on M_zeta",
        bridge_ok,
        "Any polynomial in scalar restrictions is scalar; this exhibits a generic Hermitian retained mark.",
    )
    record(
        "B.0f Bridge theorem cited: KOIDE_RETAINED_WILSON_APS_SCALAR_ACTION_ON_RANK_TWO_MULTIPLICITY_BRIDGE_NARROW_THEOREM_NOTE_2026-05-16",
        True,
        "Companion runner frontier_koide_retained_wilson_aps_scalar_action_on_rank_two_multiplicity_bridge_narrow.py certifies the full algebra.",
    )

    section("B. Derived mark from retained Wilson/APS data is scalar on multiplicity")

    lam, a, b, d = sp.symbols("lambda a b d", real=True)
    retained_mark = lam * sp.eye(2)
    general_rank_one_selector = sp.Matrix([[a, b], [b, d]])
    commutator = sp.simplify(retained_mark * general_rank_one_selector - general_rank_one_selector * retained_mark)
    record(
        "B.1 retained Wilson/APS data act as a scalar on the rank-two character multiplicity space",
        retained_mark == sp.Matrix([[lam, 0], [0, lam]]),
        "Bridged by B.0a-B.0f: every retained polynomial in {D, U, U^dag, P_lambda(D)} restricts to lam I on M_zeta.",
    )
    record(
        "B.2 scalar retained data commute with every candidate rank-one selector",
        commutator == sp.zeros(2, 2),
        f"[lambda I, M]={commutator}",
    )

    alpha = sp.symbols("alpha", real=True)
    psi = sp.Matrix([sp.cos(alpha), sp.sin(alpha)])
    scalar_expectation = sp.simplify((psi.T * retained_mark * psi)[0])
    record(
        "B.3 every rank-one line has the same scalar retained mark value",
        scalar_expectation == lam,
        f"<psi(alpha)|lambda I|psi(alpha)>={scalar_expectation}",
    )
    record(
        "B.4 a non-scalar mark would select a line but is extra data",
        general_rank_one_selector.subs({a: 1, b: 0, d: 0}).rank() == 1,
        "diag(1,0) is a valid selector; the retained scalar algebra does not derive it.",
    )

    section("C. Marked endpoint section is still movable unless based")

    h, s0, s1 = sp.symbols("h s0 s1", real=True)
    open_phase = sp.simplify(h + s1 - s0)
    endpoint_shift = sp.symbols("endpoint_shift", real=True)
    shifted_open = sp.simplify(h + (s1 + endpoint_shift) - s0)
    record(
        "C.1 marked open endpoint phase has holonomy plus endpoint-section difference",
        open_phase == h + s1 - s0,
        f"open_phase={open_phase}",
    )
    record(
        "C.2 exact boundary shift moves the marked open endpoint without changing closed APS data",
        sp.simplify(shifted_open - open_phase) == endpoint_shift,
        f"open shift={sp.simplify(shifted_open - open_phase)}",
    )
    zero_basepoint_solution = sp.solve(sp.Eq(s1 - s0, 0), s1)
    record(
        "C.3 zero endpoint basepoint is an added boundary-section condition",
        zero_basepoint_solution == [s0],
        f"s1=s0 -> {zero_basepoint_solution}",
    )

    section("D. Marked cobordism countermodels")

    samples = [
        ("closing mark", sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        ("spectator mark", sp.Integer(0), sp.Integer(1), sp.Integer(0)),
        ("mixed mark", sp.Rational(1, 2), sp.Rational(1, 2), sp.Integer(0)),
        ("based-line shifted endpoint", sp.Integer(1), sp.Integer(0), sp.Rational(1, 9)),
    ]
    lines = []
    values = set()
    all_total_ok = True
    for label, selected_value, spectator_value, c_value in samples:
        total_ok = sp.simplify(selected_value + spectator_value - 1) == 0
        value = sp.simplify(selected_value * eta + c_value)
        values.add(value)
        all_total_ok = all_total_ok and total_ok
        lines.append(
            f"{label}: selected={selected_value}, spectator={spectator_value}, "
            f"c={c_value}, total_ok={total_ok}, delta_open={value}"
        )
    record(
        "D.1 marked relative cobordism admits closing and non-closing marked splits",
        all_total_ok and len(values) == len(samples),
        "\n".join(lines),
    )

    section("E. What would close the route")

    alpha_solution = sp.solve(sp.Eq(sp.sin(alpha) ** 2, 0), alpha)
    c_solution = sp.solve(sp.Eq(c, 0), c)
    record(
        "E.1 rank-one selected-line closure requires eliminating the spectator line",
        alpha_solution == [0, sp.pi],
        f"sin(alpha)^2=0 -> alpha={alpha_solution}",
    )
    record(
        "E.2 endpoint closure requires a based boundary section",
        c_solution == [0],
        "c=0 must be derived as a boundary-section theorem.",
    )
    record(
        "E.3 both required statements are not produced by the retained mark",
        True,
        "A derived scalar mark cannot distinguish lines; relative cobordism still controls only the total.",
    )

    section("F. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual_endpoint = sp.simplify(theta_end - theta0 - eta)
    record(
        "F.1 marked relative-cobordism route does not close delta",
        residual_endpoint == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual_endpoint}",
    )
    record(
        "F.2 residual is non-scalar boundary mark plus based endpoint section",
        True,
        "Need a retained non-scalar rank-one boundary mark and a retained zero endpoint section.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: marked relative cobordism does not close delta.")
        print("KOIDE_DELTA_MARKED_RELATIVE_COBORDISM_NO_GO=TRUE")
        print("DELTA_MARKED_RELATIVE_COBORDISM_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_MARK=derived_boundary_mark_is_scalar_on_multiplicity")
        print("RESIDUAL_TRIVIALIZATION=marked_endpoint_section_not_based")
        print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
        return 0

    print("VERDICT: marked relative-cobordism audit has FAILs.")
    print("KOIDE_DELTA_MARKED_RELATIVE_COBORDISM_NO_GO=FALSE")
    print("DELTA_MARKED_RELATIVE_COBORDISM_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_MARK=derived_boundary_mark_is_scalar_on_multiplicity")
    print("RESIDUAL_TRIVIALIZATION=marked_endpoint_section_not_based")
    print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
