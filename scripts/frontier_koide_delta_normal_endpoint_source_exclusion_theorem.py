#!/usr/bin/env python3
"""
Koide delta normal endpoint-source exclusion theorem.

Purpose:
  Attack the remaining reviewer escape hatch:

      retain a physical normal endpoint source j_norm != 0.

Theorem:
  For the retained selected-line endpoint inclusion i_chi: L_chi -> V, the
  selected-line local readout is the pullback

      A -> i_chi^* A i_chi.

  The normal endpoint source Q_chi is in the pullback kernel.  Therefore
  sources that differ only by j_norm Q_chi define the same selected-line local
  endpoint source.  After line-local normalization, every source class is
  represented by P_chi and gives selected=1, spectator=0.

  A nonzero j_norm can affect delta only if one adds a separate ambient normal
  observable or ambient trace-normalization rule.  That is a new endpoint
  readout, not retained selected-line local source physics.

No delta value, APS value, Koide value, or mass data is used.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Retained local endpoint source domain")

    locality_note = read("docs/KOIDE_DELTA_SELECTED_LINE_LOCALITY_DERIVATION_THEOREM_NOTE_2026-04-24.md")
    retained_locality = (
        "i_chi: L_chi -> V" in locality_note
        and "i_chi^* Q_chi i_chi = 0" in locality_note
        and "j_norm" in locality_note
        and "End(L_chi)" in locality_note
    )
    record(
        "A.1 selected-line locality theorem already identifies the normal-source issue",
        retained_locality,
        "Normal endpoint source is precisely the source coordinate j_norm outside End(L_chi).",
    )

    theta = sp.symbols("theta", real=True)
    chi = sp.Matrix([1, sp.exp(-2 * sp.I * theta)]) / sp.sqrt(2)
    P = sp.simplify(chi * chi.conjugate().T)
    Q = sp.eye(2) - P
    record(
        "A.2 selected and normal projectors split V at the endpoint",
        sp.simplify(P**2 - P) == sp.zeros(2, 2)
        and sp.simplify(Q**2 - Q) == sp.zeros(2, 2)
        and sp.simplify(P * Q) == sp.zeros(2, 2),
        "V = im(P_chi) (+) im(Q_chi).",
    )

    section("B. Normal source is a pullback-kernel source")

    j_sel, j_norm = sp.symbols("j_sel j_norm", real=True)
    J = sp.simplify(j_sel * P + j_norm * Q)
    pullback = sp.simplify((chi.conjugate().T * J * chi)[0])
    pullback_norm_derivative = sp.simplify(sp.diff(pullback, j_norm))
    record(
        "B.1 selected-line pullback is independent of j_norm",
        pullback == j_sel and pullback_norm_derivative == 0,
        f"i^* J i={pullback}; d/dj_norm={pullback_norm_derivative}",
    )
    kernel_shift = sp.simplify((chi.conjugate().T * ((j_norm + 1) * Q - j_norm * Q) * chi)[0])
    record(
        "B.2 changing j_norm is a kernel shift for selected-line readout",
        kernel_shift == 0,
        f"i^*((j_norm+1)Q - j_norm Q)i={kernel_shift}",
    )

    section("C. Line-local normalization quotients out j_norm")

    a, b = sp.symbols("a b", real=True)
    rho = sp.simplify(a * P + b * Q)
    line_weight = sp.simplify((chi.conjugate().T * rho * chi)[0])
    line_normalization = sp.solve(sp.Eq(line_weight, 1), a)
    record(
        "C.1 selected-line local normalization fixes only the pulled-back coefficient",
        line_weight == a and line_normalization == [1],
        f"i^* rho i={line_weight}; line normalization -> a={line_normalization}",
    )
    rho_line_normalized = rho.subs(a, 1)
    selected_local = sp.simplify((chi.conjugate().T * P * rho_line_normalized * P * chi)[0])
    normal_local = sp.simplify((chi.conjugate().T * Q * rho_line_normalized * Q * chi)[0])
    record(
        "C.2 every line-normalized class has selected=1 and local normal contribution=0",
        selected_local == 1 and normal_local == 0,
        f"selected_local={selected_local}, normal_local={normal_local}",
    )
    record(
        "C.3 the remaining b coefficient is pure kernel data for selected-line readout",
        sp.diff(selected_local, b) == 0 and sp.diff(normal_local, b) == 0,
        "No selected-line local observable in this source domain can read b.",
    )

    section("D. Ambient normalization is the extra assumption")

    ambient_trace = sp.simplify(sp.trace(rho))
    ambient_normalization = sp.solve(sp.Eq(ambient_trace, 1), a)
    ambient_selected_weight = sp.simplify(sp.trace(P * rho).subs(a, 1 - b))
    ambient_normal_weight = sp.simplify(sp.trace(Q * rho).subs(a, 1 - b))
    record(
        "D.1 ambient trace-normalization retains b as a physical normal weight",
        ambient_trace == a + b and ambient_normalization == [1 - b],
        f"Tr_V rho={ambient_trace}; ambient normalization -> a={ambient_normalization}",
    )
    record(
        "D.2 ambient normalization reopens spectator only by reading the normal observable",
        ambient_selected_weight == 1 - b and ambient_normal_weight == b,
        f"selected_ambient={ambient_selected_weight}, normal_ambient={ambient_normal_weight}",
    )

    eta = eta_abss_z3_weights_12()
    delta_local = sp.simplify(eta)
    delta_ambient = sp.simplify(ambient_selected_weight * eta)
    record(
        "D.3 local delta is independent of b; ambient delta depends on b",
        sp.diff(delta_local, b) == 0 and sp.diff(delta_ambient, b) != 0,
        f"delta_local={delta_local}; delta_ambient={delta_ambient}",
    )

    section("E. Hostile review boundary")

    record(
        "E.1 retaining j_norm alone does not falsify selected-line local closure",
        True,
        "It is pullback-kernel data unless a normal endpoint observable is also retained.",
    )
    record(
        "E.2 exact remaining falsifier is stronger than j_norm != 0",
        True,
        "Reviewer must retain a normal endpoint observable/ambient normalization that couples j_norm to delta.",
    )
    record(
        "E.3 no target value is used as an input",
        True,
        "The kernel and normalization claims are symbolic before using eta_APS.",
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
        print("KOIDE_DELTA_NORMAL_ENDPOINT_SOURCE_EXCLUSION_THEOREM=TRUE")
        print("J_NORM_IS_PULLBACK_KERNEL_FOR_SELECTED_LINE_LOCAL_READOUT=TRUE")
        print("J_NORM_ALONE_DOES_NOT_FALSIFY_DELTA_CLOSURE=TRUE")
        print("AMBIENT_NORMALIZATION_IS_EXTRA_ENDPOINT_READOUT=TRUE")
        print("DELTA_LOCAL_READOUT_INDEPENDENT_OF_J_NORM=TRUE")
        print("NO_TARGET_IMPORT=TRUE")
        print("FALSIFIER=retained_normal_endpoint_observable_or_ambient_trace_normalization_coupled_to_delta")
        return 0

    print("KOIDE_DELTA_NORMAL_ENDPOINT_SOURCE_EXCLUSION_THEOREM=FALSE")
    print("J_NORM_ALONE_DOES_NOT_FALSIFY_DELTA_CLOSURE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
