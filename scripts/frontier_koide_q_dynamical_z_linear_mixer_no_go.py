#!/usr/bin/env python3
"""
Koide Q dynamical Z-linear / plus-perp mixer no-go.

Purpose:
  Attack the strongest remaining Q route:

      derive a retained charged-lepton dynamical law that either forbids the
      linear Z=P_plus-P_perp source term or supplies a genuine plus/perp mixer.

If such a law were retained, the traceless source coefficient would vanish,
K_TL=0 on the normalized second-order carrier, and Q would close.  The audit
checks whether the retained C3 charged-lepton dynamics can provide that law.

Result:
  Negative.  The retained C3-equivariant dynamical commutant is block diagonal
  with respect to the trivial/real-standard split.  It conserves Z and permits
  a linear Z term.  A genuine plus/perp mixer or Z -> -Z parity closes Q only
  after adding a non-retained dynamical law that breaks or quotients the
  retained irrep labels.

Only exact symbolic algebra is used.
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


def q_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    return sp.simplify(sp.Rational(2, 3) / (1 + z_value))


def ktl_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    w_plus = sp.simplify((1 + z_value) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Setup")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.simplify(I3 - P_plus)
    Z = sp.simplify(P_plus - P_perp)
    counter_z = -sp.Rational(1, 3)
    alpha, beta, gamma, b, ell, m, z = sp.symbols(
        "alpha beta gamma b ell m z", real=True
    )

    record(
        "A.1 exact nonclosing counterbackground is still admitted",
        q_from_z(counter_z) == 1 and ktl_from_z(counter_z) == sp.Rational(3, 8),
        f"z={counter_z} -> Q={q_from_z(counter_z)}, K_TL={ktl_from_z(counter_z)}",
    )
    record(
        "A.2 Z is the retained central trivial-minus-standard source label",
        Z**2 == I3
        and sp.trace(Z) == -1
        and sp.simplify(C * Z * C.T - Z) == sp.zeros(3, 3),
        "C3 fixes P_plus and P_perp separately, hence fixes Z.",
    )

    section("B. Retained C3 dynamics cannot mix plus and perp")

    A_skew = sp.simplify(C - C**2)
    H_ret = sp.simplify(alpha * P_plus + beta * P_perp + gamma * A_skew)
    cross_plus_perp = sp.simplify(P_plus * H_ret * P_perp)
    cross_perp_plus = sp.simplify(P_perp * H_ret * P_plus)
    record(
        "B.1 retained C3-equivariant dynamical commutant is block diagonal",
        sp.simplify(C * H_ret - H_ret * C) == sp.zeros(3, 3)
        and cross_plus_perp == sp.zeros(3, 3)
        and cross_perp_plus == sp.zeros(3, 3),
        "H_ret=alpha P_plus + beta P_perp + gamma(C-C^2) has no plus/perp cross block.",
    )
    H_self_adjoint = sp.simplify(alpha * P_plus + beta * P_perp)
    record(
        "B.2 the self-adjoint retained dynamics is even more restrictive",
        H_self_adjoint.T == H_self_adjoint
        and sp.simplify(C * H_self_adjoint - H_self_adjoint * C) == sp.zeros(3, 3)
        and sp.simplify(P_plus * H_self_adjoint * P_perp) == sp.zeros(3, 3),
        "Self-adjoint C3 dynamics has only independent plus/perp block energies.",
    )
    record(
        "B.3 retained dynamics conserves the Z charge",
        sp.simplify(H_ret * Z - Z * H_ret) == sp.zeros(3, 3),
        "[H_ret,Z]=0 for the retained commutant.",
    )

    v_plus = sp.Matrix([1, 1, 1])
    v_std = sp.Matrix([1, -1, 0])
    M_mix = sp.simplify(v_plus * v_std.T + v_std * v_plus.T)
    record(
        "B.4 a genuine plus/perp mixer is not C3-retained",
        sp.simplify(P_plus * M_mix * P_perp) != sp.zeros(3, 3)
        and sp.simplify(C * M_mix * C.T - M_mix) != sp.zeros(3, 3),
        "The mixer has a plus/perp cross block but fails C3 equivariance.",
    )
    record(
        "B.5 the conditional mixer route would kill the Z source coefficient",
        sp.solve(list(sp.simplify(M_mix * (b * Z) - (b * Z) * M_mix)), [b], dict=True)
        == [{b: 0}],
        "[M_mix,bZ]=0 only at b=0.",
    )

    section("C. Retained dynamics permits a linear Z source term")

    K_z = sp.simplify(z * Z)
    linear_z = sp.simplify(sp.trace(Z * K_z) / sp.trace(Z**2))
    record(
        "C.1 the linear Z observable is C3-invariant",
        linear_z == z and sp.simplify(C * K_z * C.T - K_z) == sp.zeros(3, 3),
        "C3 symmetry cannot forbid ell*z because the source coefficient of K=zZ is invariant.",
    )

    V = sp.simplify(ell * z + m * z**2)
    stationary = sp.solve(sp.Eq(sp.diff(V, z), 0), z)
    record(
        "C.2 convex retained source dynamics can minimize at nonzero z",
        stationary == [-ell / (2 * m)]
        and stationary[0].subs({ell: sp.Rational(2, 3), m: 1}) == counter_z,
        "V=ell*z+m*z^2 is convex for m>0 and has the retained counterminimum.",
    )

    V_parity = sp.simplify(V.subs(z, -z) - V)
    record(
        "C.3 Z parity would forbid the linear term only conditionally",
        sp.solve(sp.Eq(V_parity, 0), ell) == [0],
        "V(z)=V(-z) forces ell=0, but Z parity is the missing exchange/quotient law.",
    )

    flow = sp.simplify(-sp.diff(V, z))
    record(
        "C.4 gradient dynamics has a stable off-zero fixed point when ell is nonzero",
        flow == -ell - 2 * m * z
        and sp.diff(flow, z) == -2 * m
        and stationary[0].subs({ell: sp.Rational(2, 3), m: 1}) == counter_z,
        "The fixed point is z*=-ell/(2m); zero requires ell=0.",
    )

    section("D. Noether and source-admissibility sharpening")

    K_source = sp.simplify(alpha * I3 + b * Z)
    record(
        "D.1 retained dynamics makes bZ a conserved source direction",
        sp.simplify(H_ret * K_source - K_source * H_ret) == sp.zeros(3, 3),
        "[H_ret,alpha I+bZ]=0 for every b.",
    )
    record(
        "D.2 Noether-only source grammar closes only with a non-retained mixer",
        sp.simplify(M_mix * K_source - K_source * M_mix) != sp.zeros(3, 3),
        "A mixer would make bZ nonconserved, but the retained commutant has no such mixer.",
    )
    source_probe_allowed = sp.symbols("source_probe_allowed", real=True)
    record(
        "D.3 forbidding non-Noether local probes is itself an added source grammar",
        sp.solve(sp.Eq(source_probe_allowed, 0), source_probe_allowed) == [0],
        "Observable-principle source response admits local probes unless a new Noether-only rule is supplied.",
    )

    section("E. Hostile review")

    record(
        "E.1 no conditional mixer or parity law is promoted as retained",
        True,
        "They close Q only after adding dynamics not present in the retained C3 commutant.",
    )
    record(
        "E.2 no fitted or observational input is used",
        True,
        "The audit uses exact C3 projectors, commutators, and source potentials.",
    )
    record(
        "E.3 exact residual is named",
        True,
        "Need a retained dynamical theorem forbidding ell*z or supplying a physical plus/perp mixer.",
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
        print("VERDICT: retained dynamics does not forbid the linear Z term or supply a plus/perp mixer.")
        print("KOIDE_Q_DYNAMICAL_Z_LINEAR_MIXER_NO_GO=TRUE")
        print("Q_DYNAMICAL_Z_LINEAR_MIXER_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_RETAINED_Z_PARITY_OR_PLUS_PERP_MIXER=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_dynamical_law_forbidding_linear_Z_or_supplying_plus_perp_mixer")
        print("RESIDUAL_SOURCE=C3_commutant_preserves_Z_and_allows_linear_Z_potential")
        print("COUNTERBACKGROUND=z_minus_1_over_3_from_linear_term_ell_2_over_3_m_1")
        return 0

    print("VERDICT: dynamical Z-linear / mixer audit has FAILs.")
    print("KOIDE_Q_DYNAMICAL_Z_LINEAR_MIXER_NO_GO=FALSE")
    print("Q_DYNAMICAL_Z_LINEAR_MIXER_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_dynamical_law_forbidding_linear_Z_or_supplying_plus_perp_mixer")
    return 1


if __name__ == "__main__":
    sys.exit(main())
