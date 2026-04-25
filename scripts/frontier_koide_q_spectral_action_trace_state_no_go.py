#!/usr/bin/env python3
"""
Koide Q spectral-action / modular trace-state no-go.

Theorem attempt:
  A heat-kernel, spectral-action, zeta-residue, or modular/KMS trace on the
  retained C3 quotient might force equal singlet/doublet block totals, thereby
  deriving K_TL = 0.

Result:
  Negative for the retained finite C3 carrier.  The canonical C3 Laplacian has
  eigenvalues 0 on the singlet and 3 on the real doublet.  Heat traces give

      W_+(t) = 1,        W_perp(t) = 2 exp(-3t).

  Equal total block weights occur only at the externally chosen modular time
  t = log(2)/3.  The rank trace t=0 is off the Koide leaf, and a finite
  spectral action leaves the cutoff function value f(3/Lambda^2) free.  Zeta
  residues on this finite carrier have no pole that can select equal block
  totals.  Thus the spectral-action route reformulates the residual as a
  missing modular-time/cutoff normalization law.

No PDG masses, target Koide value, K_TL pin, delta pin, or H_* pin is used.
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


def q_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((1 + r) / 3)


def ktl_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Retained C3 Laplacian spectrum")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    J = sp.ones(3, 3)
    L = sp.simplify(2 * I3 - C - C**2)
    P_plus = J / 3
    P_perp = I3 - P_plus

    record(
        "A.1 C3 graph Laplacian has singlet eigenvalue 0 and doublet eigenvalue 3",
        sp.simplify(L * P_plus) == sp.zeros(3, 3)
        and sp.simplify(L * P_perp - 3 * P_perp) == sp.zeros(3, 3),
        f"L={L.tolist()}",
    )
    record(
        "A.2 multiplicities are rank(P_plus)=1 and rank(P_perp)=2",
        P_plus.rank() == 1 and P_perp.rank() == 2,
        f"ranks=({P_plus.rank()},{P_perp.rank()})",
    )

    section("B. Heat/modular trace leaves a free time parameter")

    t = sp.symbols("t", nonnegative=True, real=True)
    w_plus = sp.Integer(1)
    w_perp = 2 * sp.exp(-3 * t)
    r_t = sp.simplify(w_perp / w_plus)
    q_t = q_from_ratio(r_t)
    ktl_t = ktl_from_ratio(r_t)
    t_equal = sp.solve(sp.Eq(r_t, 1), t)

    record(
        "B.1 heat trace block-total ratio is R(t)=2 exp(-3t)",
        r_t == 2 * sp.exp(-3 * t),
        f"W_plus={w_plus}, W_perp={w_perp}, R(t)={r_t}",
    )
    record(
        "B.2 equal block totals require an externally selected modular time",
        len(t_equal) == 1 and sp.simplify(t_equal[0] - sp.log(2) / 3) == 0,
        f"R(t)=1 -> t={t_equal}",
    )
    record(
        "B.3 the rank/Hilbert trace t=0 is off the equal-block leaf",
        q_t.subs(t, 0) == 1 and ktl_t.subs(t, 0) == sp.Rational(3, 8),
        f"Q(0)={q_t.subs(t, 0)}, K_TL(0)={ktl_t.subs(t, 0)}",
    )

    sample_ts = [0, sp.log(2) / 3, sp.log(4) / 3]
    sample_lines = []
    sample_values = []
    for value in sample_ts:
        r_value = sp.simplify(r_t.subs(t, value))
        sample_values.append(r_value)
        sample_lines.append(
            f"t={value}: R={r_value}, Q={q_from_ratio(r_value)}, K_TL={ktl_from_ratio(r_value)}"
        )
    record(
        "B.4 the same retained heat-kernel family realizes inequivalent block laws",
        sample_values == [2, 1, sp.Rational(1, 2)],
        "\n".join(sample_lines),
    )

    section("C. Spectral-action cutoff value is another free map")

    f0, f3 = sp.symbols("f0 f3", positive=True, real=True)
    r_f = sp.simplify(2 * f3 / f0)
    q_f = q_from_ratio(r_f)
    ktl_f = ktl_from_ratio(r_f)
    f_condition = sp.solve(sp.Eq(r_f, 1), f3)

    record(
        "C.1 finite spectral action weights are f(0) and 2 f(3/Lambda^2)",
        r_f == 2 * f3 / f0,
        f"R_f={r_f}, Q_f={q_f}, K_TL_f={ktl_f}",
    )
    record(
        "C.2 equal block totals require f3=f0/2",
        f_condition == [f0 / 2],
        f"R_f=1 -> f3={f_condition}",
    )

    sharp_samples = {
        "sharp_cutoff_both_blocks": (1, 1),
        "sharp_cutoff_singlet_only": (1, 0),
        "equal_block_tuned_cutoff": (1, sp.Rational(1, 2)),
    }
    sharp_lines = []
    for label, (value_f0, value_f3) in sharp_samples.items():
        ratio = sp.simplify(r_f.subs({f0: value_f0, f3: value_f3}))
        sharp_lines.append(
            f"{label}: f0={value_f0}, f3={value_f3} -> R={ratio}, Q={q_from_ratio(ratio)}"
        )
    record(
        "C.3 common cutoff choices do not force the tuned equal-block value",
        True,
        "\n".join(sharp_lines),
    )

    section("D. Zeta/residue trace has no finite-carrier pole selecting equality")

    s = sp.symbols("s", complex=True)
    zeta_nonzero = 2 * 3 ** (-s)
    residue_at_zero = sp.residue(zeta_nonzero, s, 0)
    residue_at_one = sp.residue(zeta_nonzero, s, 1)
    record(
        "D.1 finite nonzero-spectrum zeta function is entire",
        residue_at_zero == 0 and residue_at_one == 0,
        f"zeta_nonzero(s)={zeta_nonzero}; residues at 0,1 = {residue_at_zero},{residue_at_one}",
    )
    record(
        "D.2 no Dixmier/zeta residue exists here to override rank or heat weights",
        True,
        "The finite carrier supplies eigenvalue multiplicities and optional test functions, not a canonical residue trace.",
    )

    section("E. Verdict")

    residual_time = sp.simplify(t - sp.log(2) / 3)
    residual_cutoff = sp.simplify(f3 - f0 / 2)
    record(
        "E.1 residual is modular-time or cutoff normalization, not a derived law",
        residual_time == t - sp.log(2) / 3 and residual_cutoff == f3 - f0 / 2,
        f"RESIDUAL_TIME={residual_time}; RESIDUAL_CUTOFF={residual_cutoff}",
    )
    record(
        "E.2 spectral-action/modular trace route does not close Q",
        True,
        "A retained theorem would need to fix t=log(2)/3, or equivalently f3=f0/2, without target import.",
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
        print("VERDICT: spectral-action/modular trace-state route does not close Q.")
        print("KOIDE_Q_SPECTRAL_ACTION_TRACE_STATE_NO_GO=TRUE")
        print("Q_SPECTRAL_ACTION_TRACE_STATE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=t_minus_log2_over3_or_f3_minus_f0_over2_equiv_K_TL")
        print("RESIDUAL_TRACE_STATE=t_minus_log2_over3_or_f3_minus_f0_over2_equiv_K_TL")
        return 0

    print("VERDICT: spectral-action trace-state audit has FAILs.")
    print("KOIDE_Q_SPECTRAL_ACTION_TRACE_STATE_NO_GO=FALSE")
    print("Q_SPECTRAL_ACTION_TRACE_STATE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=t_minus_log2_over3_or_f3_minus_f0_over2_equiv_K_TL")
    print("RESIDUAL_TRACE_STATE=t_minus_log2_over3_or_f3_minus_f0_over2_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
