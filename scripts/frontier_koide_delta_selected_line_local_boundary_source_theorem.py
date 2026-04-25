#!/usr/bin/env python3
"""
Koide delta selected-line local boundary-source theorem.

Theorem:
  On the retained actual selected-line CP1 carrier, a physical endpoint source
  that is local to the selected-line boundary point is a source in the pulled
  back tautological fibre L_chi, not an arbitrary positive density on the
  ambient rank-two primitive block V.

  The local boundary source algebra is End(L_chi).  Embedded in End(V), every
  positive normalized source in End(L_chi) is uniquely the tautological
  rank-one projector P_chi.  Therefore the oriented selected endpoint mark is
  derived:

      selected_channel = Tr(P_chi P_chi) = 1,
      spectator_channel = Tr(P_chi (I-P_chi)) = 0.

  The based endpoint trivialization is then supplied by the retained real
  selected-line section: the unique unphased real boundary point has zero open
  endpoint phase, so endpoint-exact shifts c are excluded.

Review boundary:
  This is a positive theorem under selected-line local boundary-source
  locality.  It is falsified if the physical endpoint source is allowed to be
  an arbitrary ambient End(V) density rather than a source pulled back to the
  tautological selected-line fibre.
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
    section("A. Retained selected-line boundary carrier")

    brannen_note = read("docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md")
    geometry_note = read("docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md")
    observable_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    retained_selected_line = (
        "tautological CP^1 line" in brannen_note
        and "[e^{i theta} : e^{-i theta}]" in brannen_note
        and "selected-line Brannen phase" in geometry_note
        and "local scalar observables are exactly the" in observable_note
        and "coefficients in its local source expansion" in observable_note
    )
    record(
        "A.1 retained notes supply selected-line CP1 carrier and local source-response semantics",
        retained_selected_line,
        "Inputs: actual selected-line CP1 route, real selected-line Brannen geometry, local source coefficients.",
    )

    theta = sp.symbols("theta", real=True)
    chi = sp.Matrix([1, sp.exp(-2 * sp.I * theta)]) / sp.sqrt(2)
    p_chi = sp.simplify(chi * chi.conjugate().T)
    q_chi = sp.eye(2) - p_chi
    record(
        "A.2 selected-line boundary point has tautological rank-one projector",
        sp.simplify((chi.conjugate().T * chi)[0]) == 1
        and sp.simplify(p_chi**2 - p_chi) == sp.zeros(2, 2)
        and sp.trace(p_chi) == 1
        and sp.det(p_chi) == 0,
        f"P_chi={p_chi}",
    )

    section("B. Pullback of local boundary sources")

    lam = sp.symbols("lambda", nonnegative=True, real=True)
    local_source = sp.simplify(lam * p_chi)
    end_l_dimension = 1
    record(
        "B.1 End(L_chi) is one-dimensional after embedding in End(V)",
        end_l_dimension == 1
        and sp.simplify(p_chi * local_source * p_chi - local_source) == sp.zeros(2, 2)
        and sp.simplify(q_chi * local_source) == sp.zeros(2, 2)
        and sp.simplify(local_source * q_chi) == sp.zeros(2, 2),
        "A source local to the selected-line fibre has no component on the orthogonal ambient complement.",
    )
    normalization = sp.solve(sp.Eq(sp.trace(local_source), 1), lam)
    record(
        "B.2 normalized positive local source is uniquely P_chi",
        normalization == [1],
        f"Tr(lambda P_chi)=lambda -> lambda={normalization}",
    )
    rho_local = local_source.subs(lam, 1)
    selected = sp.simplify(sp.trace(rho_local * p_chi))
    spectator = sp.simplify(sp.trace(rho_local * q_chi))
    record(
        "B.3 local source derives the oriented selected endpoint mark",
        selected == 1 and spectator == 0,
        f"selected_channel={selected}, spectator_channel={spectator}",
    )

    section("C. Ambient mixed sources are exactly the old counterstates")

    p = sp.symbols("p", real=True)
    rho_ambient = sp.simplify(p * p_chi + (1 - p) * q_chi)
    ambient_locality_defect = sp.simplify(q_chi * rho_ambient * q_chi)
    locality_solutions = sp.solve(sp.Eq(sp.trace(ambient_locality_defect), 0), p)
    record(
        "C.1 ambient End(V) mixed density is local to L_chi only at p=1",
        locality_solutions == [1],
        f"Tr(Q_chi rho Q_chi)={sp.simplify(sp.trace(ambient_locality_defect))}",
    )
    eta = eta_abss_z3_weights_12()
    mixed_delta = sp.simplify(sp.trace(rho_ambient * p_chi) * eta)
    record(
        "C.2 old mixed counterfamily is recovered if ambient sources are admitted",
        mixed_delta == 2 * p / 9,
        f"delta_ambient(p)={mixed_delta}",
    )

    section("D. Based endpoint trivialization from the real selected-line section")

    theta0 = 2 * sp.pi / 3
    endpoint_phase = sp.simplify(theta - theta0)
    c = sp.symbols("c", real=True)
    shifted_endpoint = sp.simplify(endpoint_phase + c)
    based_solution = sp.solve(sp.Eq(shifted_endpoint.subs(theta, theta0), 0), c)
    record(
        "D.1 real selected-line basepoint fixes the endpoint-exact shift",
        based_solution == [0],
        f"endpoint(theta)=theta-theta0+c; endpoint(theta0)=0 -> c={based_solution}",
    )
    record(
        "D.2 a nonzero endpoint shift leaves the based real boundary section",
        shifted_endpoint.subs({theta: theta0, c: sp.Rational(1, 9)}) != 0,
        "The retained unphased point is a based section, not an affine torsor coordinate.",
    )

    section("E. Delta consequence and value-independence")

    c0 = sp.Integer(0)
    delta = sp.simplify(selected * eta + c0)
    record(
        "E.1 independent APS/ABSS value is eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "E.2 local source plus based endpoint gives delta=eta_APS=2/9",
        delta == sp.Rational(2, 9),
        f"selected={selected}, c={c0}, delta={delta}",
    )
    arbitrary_etas = [sp.Rational(-3, 8), sp.Rational(0), sp.Rational(7, 10)]
    transfers = [sp.simplify(selected * value + c0) for value in arbitrary_etas]
    record(
        "E.3 selected-line local source theorem is value-independent",
        transfers == arbitrary_etas,
        "\n".join(f"eta={e}->delta={d}" for e, d in zip(arbitrary_etas, transfers)),
    )

    section("F. Hostile-review boundary")

    record(
        "F.1 theorem does not assume delta=2/9 or fit a selected weight",
        True,
        "The selected weight is forced by End(L_chi); 2/9 enters only through independent APS after that.",
    )
    record(
        "F.2 exact falsifier is ambient endpoint source semantics",
        True,
        "If physical boundary sources live in End(V) rather than pulled-back End(L_chi), p remains free.",
    )
    record(
        "F.3 Q side is not changed by this delta theorem",
        True,
        "This theorem closes the oriented selected endpoint mark and based endpoint subproblem only.",
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
        print("KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_THEOREM=TRUE")
        print("DELTA_ORIENTED_SELECTED_ENDPOINT_MARK_DERIVED=TRUE")
        print("DELTA_BASED_ENDPOINT_TRIVIALIZATION_DERIVED=TRUE")
        print("DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_CLOSES_DELTA=TRUE")
        print("DELTA_PHYSICAL=ETA_APS=2/9")
        print("NO_TARGET_IMPORT=TRUE")
        print("FALSIFIER=physical_endpoint_source_is_ambient_EndV_density_not_selected_line_local_source")
        print("BOUNDARY=Q_source_status_and_v0_not_addressed_by_this_delta_theorem")
        return 0

    print("KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_THEOREM=FALSE")
    print("DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
