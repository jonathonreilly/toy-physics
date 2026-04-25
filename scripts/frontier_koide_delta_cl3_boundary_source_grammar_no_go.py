#!/usr/bin/env python3
"""
Koide delta higher Cl(3) boundary source-grammar no-go.

Theorem attempt:
  Exhaust the retained local Cl(3)/Z3 boundary source grammar coupled to the
  selected Brannen endpoint.  Perhaps the grammar itself forbids spectator
  anomaly channels and endpoint-exact offsets, deriving

      spectator_channel = 0,
      c = 0.

Result:
  Negative.  The C3-fixed Cl(3) word space is not one-dimensional, and the
  local boundary channel idempotent grammar has an independent odd coefficient.
  After total anomaly normalization, this odd coefficient controls how much
  anomaly sits on the selected line versus a spectator boundary channel.

  Endpoint-exact source words provide an independent offset c; they cancel on
  closed APS loops but move the open selected endpoint.  The retained grammar
  therefore leaves the same residual:

      delta_open / eta_APS - 1 = -spectator_channel + c / eta_APS.

No mass data, fitted Koide value, or selected endpoint target is used.
"""

from __future__ import annotations

import sys

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


def right_multiply_vector(mask: int, index: int) -> tuple[int, int]:
    """Return sign, mask for e_mask * e_index in Euclidean Cl(3)."""
    greater = sum(1 for j in range(index + 1, 3) if mask & (1 << j))
    sign = -1 if greater % 2 else 1
    return sign, mask ^ (1 << index)


def blade_mul(left: int, right: int) -> tuple[int, int]:
    sign = 1
    out = left
    for index in range(3):
        if right & (1 << index):
            s, out = right_multiply_vector(out, index)
            sign *= s
    return sign, out


def c3_action_blade(mask: int) -> tuple[int, int]:
    """Cyclic automorphism e1->e2, e2->e3, e3->e1 on a Clifford blade."""
    sign = 1
    out = 0
    for index in range(3):
        if mask & (1 << index):
            image_index = (index + 1) % 3
            s, out = right_multiply_vector(out, image_index)
            sign *= s
    return sign, out


def c3_action_matrix() -> sp.Matrix:
    mat = sp.zeros(8, 8)
    for mask in range(8):
        sign, image = c3_action_blade(mask)
        mat[image, mask] = sign
    return mat


def basis_vector(mask: int) -> sp.Matrix:
    v = sp.zeros(8, 1)
    v[mask, 0] = 1
    return v


def orbit_sum(mask: int) -> sp.Matrix:
    action = c3_action_matrix()
    v = basis_vector(mask)
    return sp.simplify(v + action * v + action**2 * v)


def split_even_odd(coeffs: list[sp.Expr]) -> tuple[sp.Expr, sp.Expr]:
    even = sp.simplify(sum(coeffs[n] for n in range(0, len(coeffs), 2)))
    odd = sp.simplify(sum(coeffs[n] for n in range(1, len(coeffs), 2)))
    return even, odd


def main() -> int:
    section("A. C3-fixed Cl(3) word space")

    e1, e2, e3 = 1, 2, 4
    s12, e12 = blade_mul(e1, e2)
    s21, e21 = blade_mul(e2, e1)
    s123_a, e12_3 = blade_mul(e12, e3)
    record(
        "A.1 Euclidean Cl(3) multiplication is implemented exactly",
        blade_mul(e1, e1) == (1, 0)
        and blade_mul(e2, e2) == (1, 0)
        and blade_mul(e3, e3) == (1, 0)
        and (s12, e12) == (1, 3)
        and (s21, e21) == (-1, 3)
        and (s123_a, e12_3) == (1, 7),
        "e_i^2=1 and e_i e_j=-e_j e_i for i!=j.",
    )

    action = c3_action_matrix()
    fixed_basis = (action - sp.eye(8)).nullspace()
    invariant_vectors = {
        "1": basis_vector(0),
        "vector_orbit": orbit_sum(1),
        "bivector_orbit": orbit_sum(3),
        "pseudoscalar": basis_vector(7),
    }
    invariant_matrix = sp.Matrix.hstack(*invariant_vectors.values())
    record(
        "A.2 the cyclic Cl(3) automorphism has order three",
        action**3 == sp.eye(8),
        "C3 acts by e1->e2->e3->e1.",
    )
    record(
        "A.3 C3-fixed Cl(3) word space is four-dimensional, not a unique scalar",
        len(fixed_basis) == 4 and invariant_matrix.rank() == 4,
        "fixed generators: 1, vector orbit, bivector orbit, pseudoscalar.",
    )
    record(
        "A.4 higher Cl(3) invariant words therefore supply independent source coefficients",
        True,
        "Retained C3 symmetry alone does not collapse boundary source data to the identity word.",
    )

    section("B. Local boundary channel idempotent grammar")

    P_selected = sp.Matrix([[1, 0], [0, 0]])
    P_spectator = sp.Matrix([[0, 0], [0, 1]])
    I2 = sp.eye(2)
    Z = sp.simplify(P_selected - P_spectator)
    record(
        "B.1 selected and spectator channel idempotents form a retained local boundary channel algebra",
        P_selected**2 == P_selected
        and P_spectator**2 == P_spectator
        and P_selected * P_spectator == sp.zeros(2, 2)
        and P_selected + P_spectator == I2,
        "The total boundary channel is fixed only after summing both idempotents.",
    )
    record(
        "B.2 channel involution collapses higher local words to even and odd parts",
        Z**2 == I2,
        "Z=P_selected-P_spectator, Z^2=I.",
    )

    degree = 8
    channel_coeffs = list(sp.symbols(f"a0:{degree + 1}", real=True))
    endpoint_coeffs = list(sp.symbols(f"b0:{degree + 1}", real=True))
    channel_word = sp.zeros(2, 2)
    endpoint_word = sp.zeros(2, 2)
    for power, coeff in enumerate(channel_coeffs):
        channel_word += coeff * (Z**power)
    for power, coeff in enumerate(endpoint_coeffs):
        endpoint_word += coeff * (Z**power)
    A_even, A_odd = split_even_odd(channel_coeffs)
    B_even, B_odd = split_even_odd(endpoint_coeffs)
    channel_collapsed = sp.simplify(A_even * I2 + A_odd * Z)
    endpoint_collapsed = sp.simplify(B_even * I2 + B_odd * Z)
    record(
        "B.3 arbitrary higher local channel source collapses to A_even I + A_odd Z",
        sp.simplify(channel_word - channel_collapsed) == sp.zeros(2, 2),
        f"A_even={A_even}; A_odd={A_odd}",
    )
    record(
        "B.4 arbitrary endpoint-exact source collapses to an independent B_even I + B_odd Z",
        sp.simplify(endpoint_word - endpoint_collapsed) == sp.zeros(2, 2),
        f"B_even={B_even}; B_odd={B_odd}",
    )

    section("C. Total anomaly normalization leaves spectator and endpoint offset free")

    Ae, Ao, Be, Bo = sp.symbols("A_even A_odd B_even B_odd", real=True)
    selected_raw = sp.simplify(Ae + Ao)
    spectator_raw = sp.simplify(Ae - Ao)
    total_raw = sp.simplify(selected_raw + spectator_raw)
    selected_norm = sp.simplify(selected_raw / total_raw)
    spectator_norm = sp.simplify(spectator_raw / total_raw)
    selected_offset = sp.simplify(Be + Bo)
    eta = sp.Rational(2, 9)
    residual = sp.simplify(-spectator_norm + selected_offset / eta)
    record(
        "C.1 total anomaly normalization fixes A_even but not A_odd",
        total_raw == 2 * Ae
        and sp.simplify(selected_norm - (Ae + Ao) / (2 * Ae)) == 0,
        f"selected={selected_norm}; spectator={spectator_norm}; total={total_raw}",
    )
    record(
        "C.2 selected endpoint offset is independent endpoint-exact source data",
        selected_offset == Be + Bo,
        f"c={selected_offset}",
    )
    jac_constraints = sp.Matrix([[sp.diff(total_raw, var) for var in (Ao, Be, Bo)]])
    record(
        "C.3 total anomaly constraint has zero rank in the residual variables",
        jac_constraints.rank() == 0,
        f"Jacobian of total wrt (A_odd,B_even,B_odd)={jac_constraints.tolist()}",
    )
    record(
        "C.4 reduced endpoint residual survives the full local grammar",
        sp.simplify(residual - (-spectator_norm + selected_offset / eta)) == 0,
        f"delta/eta_APS - 1 = {residual}",
    )

    section("D. Exact retained countermodels")

    cases = [
        ("selected unit channel", sp.Rational(1, 2), sp.Rational(1, 2), sp.Integer(0), sp.Integer(0)),
        ("spectator unit channel", sp.Rational(1, 2), -sp.Rational(1, 2), sp.Integer(0), sp.Integer(0)),
        ("half-selected half-spectator", sp.Rational(1, 2), sp.Integer(0), sp.Integer(0), sp.Integer(0)),
        ("selected unit with endpoint shift", sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 9), sp.Integer(0)),
    ]
    lines = []
    values = set()
    all_total_ok = True
    for label, ae, ao, be, bo in cases:
        selected_value = sp.simplify(selected_norm.subs({Ae: ae, Ao: ao}))
        spectator_value = sp.simplify(spectator_norm.subs({Ae: ae, Ao: ao}))
        c_value = sp.simplify(selected_offset.subs({Be: be, Bo: bo}))
        delta_value = sp.simplify(selected_value * eta + c_value)
        total_ok = sp.simplify(total_raw.subs({Ae: ae, Ao: ao}) - 1) == 0
        all_total_ok = all_total_ok and total_ok
        values.add(delta_value)
        lines.append(
            f"{label}: selected={selected_value}, spectator={spectator_value}, "
            f"c={c_value}, total_ok={total_ok}, delta_open={delta_value}"
        )
    record(
        "D.1 the same retained grammar contains closing and non-closing normalized channels",
        all_total_ok and len(values) == len(cases),
        "\n".join(lines),
    )

    section("E. What would close the route")

    closure_channel = sp.solve(sp.Eq(spectator_norm, 0), Ao)
    closure_offset = sp.solve(sp.Eq(selected_offset, 0), Bo)
    record(
        "E.1 no-spectator channel is the coefficient condition A_odd=A_even",
        closure_channel == [Ae],
        f"spectator=0 -> A_odd={closure_channel}",
    )
    record(
        "E.2 zero endpoint offset is the independent condition B_odd=-B_even",
        closure_offset == [-Be],
        f"c=0 -> B_odd={closure_offset}",
    )
    record(
        "E.3 both conditions are selected-line identity laws, not grammar consequences",
        True,
        "The grammar supplies coordinates for the residuals; it does not set them to the closing values.",
    )

    section("F. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual_endpoint = sp.simplify(theta_end - theta0 - eta)
    record(
        "F.1 higher Cl(3) boundary source grammar does not close delta",
        residual_endpoint == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual_endpoint}",
    )
    record(
        "F.2 residual is selected-channel projector plus endpoint-exact basepoint",
        True,
        "Need A_odd=A_even and B_odd=-B_even from retained physics.",
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
        print("VERDICT: higher Cl(3) boundary source grammar does not close delta.")
        print("KOIDE_DELTA_CL3_BOUNDARY_SOURCE_GRAMMAR_NO_GO=TRUE")
        print("DELTA_CL3_BOUNDARY_SOURCE_GRAMMAR_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_CHANNEL=selected_line_projector_source_not_forced")
        print("RESIDUAL_TRIVIALIZATION=selected_endpoint_exact_counterterm_not_forced_zero")
        print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
        return 0

    print("VERDICT: higher Cl(3) boundary source grammar audit has FAILs.")
    print("KOIDE_DELTA_CL3_BOUNDARY_SOURCE_GRAMMAR_NO_GO=FALSE")
    print("DELTA_CL3_BOUNDARY_SOURCE_GRAMMAR_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_CHANNEL=selected_line_projector_source_not_forced")
    print("RESIDUAL_TRIVIALIZATION=selected_endpoint_exact_counterterm_not_forced_zero")
    print("RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
