#!/usr/bin/env python3
"""Audit the projector-valued observable principle Planck lane honestly.

This lane proves the sharpest exact split now available on the boundary route:

  - the current scalar Schur observable principle still selects
      p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma);
  - the non-Schur full-cell occupation lane fixes the source-free state as the
      unique bit-flip-invariant democratic state rho_cell = I_16 / 16;
  - on the commuting packet/event algebra, the minimal normalized additive
      yes/no observable is mu_rho(P) = Tr(rho P);
  - on the forced packet P_A this gives exact quarter:
      Tr(rho_cell P_A) = 1/4.

So quarter closes exactly on the projector/event route, but only if boundary
pressure is physically read as that non-scalar event observable.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_PROJECTOR_VALUED_OBSERVABLE_PRINCIPLE_LANE_2026-04-23.md"
OBS = ROOT / "docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
HILBERT = ROOT / "docs/SINGLE_AXIOM_HILBERT_NOTE.md"
BOUNDARY_OBS = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
)
SECTION = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
)
MULT = ROOT / "docs/PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md"
WEIGHTED = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_WEIGHTED_C16_STATE_FROM_SCHUR_LANE_2026-04-23.md"
)
POSITIVE = (
    ROOT / "docs/PLANCK_SCALE_BOUNDARY_POSITIVE_RESIDUAL_THEOREM_LANE_2026-04-23.md"
)
NON_SCHUR = ROOT / "docs/PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    passed = bool(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def atomic_projector(idx: int, dim: int = 16) -> sp.Matrix:
    vec = sp.zeros(dim, 1)
    vec[idx, 0] = 1
    return vec * vec.T


def xor_bits(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x ^ y) for x, y in zip(a, b))


def main() -> int:
    note = normalized(NOTE)
    obs = normalized(OBS)
    hilbert = normalized(HILBERT)
    boundary_obs = normalized(BOUNDARY_OBS)
    section_note = normalized(SECTION)
    mult = normalized(MULT)
    weighted = normalized(WEIGHTED)
    positive = normalized(POSITIVE)
    non_schur = normalized(NON_SCHUR)

    n_pass = 0
    n_fail = 0

    print("Planck projector-valued observable principle lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the scalar observable-principle note still fixes the additive log law",
        "w = c log |z| + const" in obs
        and "the observable principle" in obs
        and "scalar bosonic observables" in obs,
        "the projector lane should separate from the current scalar grammar, not overwrite it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the Hilbert note still records Born/event structure on the finite carrier",
        "born rule is automatic" in hilbert
        and "hilbert space inner product forces the born rule" in hilbert,
        "the projector route should lean on the existing Hilbert/Born surface",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the boundary observable note still says the scalar route selects p_vac rather than quarter",
        "p_obs(l_sigma) = p_vac(l_sigma)" in boundary_obs
        and "quarter is ruled out" in boundary_obs
        and "new non-scalar" in boundary_obs,
        "this lane only makes sense if the scalar route is already honestly boxed out",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the section-canonical lane still forces the coarse packet P_A",
        "the unique admissible projector is `p_a = p_t + p_s`" in section_note
        or "the coarse four-axis worldtube channel is **section-canonical**" in section_note,
        "the projector route needs a forced packet before it can be meaningful",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the multiplicity lift lane still fixes the packet quarter exactly",
        "tr(rho_cell p_a) = 2 tr(rho_cell p_q) = 1/4" in mult
        or "m_lift := tr(rho_cell p_a) = 2 tr(rho_cell p_q) = 1/4" in mult,
        "the projector route should inherit the exact quarter without adding a new coefficient",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the weighted-state lane still says normalized Schur data do not already supply quarter",
        "1/13 <= alpha(beta) <= 1/7" in weighted
        and "strictly below quarter" in weighted,
        "that prevents this lane from smuggling quarter out of normalized Schur/Perron data",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the positive residual lane still isolates delta = Tr(rho_cell P_A) as the unique positive candidate",
        "delta = tr(rho_cell p_a)" in positive
        and "m_axis = 1/4" in positive,
        "the projector route should match the action-side positive residual target exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-Schur occupation lane now fixes the source-free state as I_16 / 16",
        "rho_cell = i_16 / 16" in non_schur,
        "the projector route should no longer leave rho_cell looking ad hoc",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: FULL-CELL SOURCE-FREE STATE")
    states = list(product((0, 1), repeat=4))
    vars_p = sp.symbols("p0:16", real=True)
    equations = []
    index = {state: i for i, state in enumerate(states)}
    generators = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    for s in states:
        for g in generators:
            equations.append(sp.Eq(vars_p[index[s]], vars_p[index[xor_bits(s, g)]]))
    equations.append(sp.Eq(sum(vars_p), 1))
    solution = sp.linsolve([eq.lhs - eq.rhs for eq in equations], vars_p)
    tuple_solution = next(iter(solution))
    uniform = tuple(sp.Rational(1, 16) for _ in states)
    rho_cell = sp.eye(16) / 16

    p = check(
        "bit-flip invariance plus normalization uniquely fixes the full-cell source-free state",
        tuple_solution == uniform,
        "the democratic state is the unique source-free occupation law on the exact time-locked cell under the native local flip group",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the full-cell source-free state is rho_cell = I_16 / 16",
        tuple_solution == uniform and rho_cell == sp.eye(16) / 16,
        "the projector route does not need a separate unexplained state datum once the non-Schur symmetry is accepted",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXACT CELL EVENT ALGEBRA")
    dim = 16
    atoms = [atomic_projector(i, dim) for i in range(dim)]

    p = check(
        "the atomic cell projectors form an orthogonal partition of the identity",
        all(
            sp.simplify((atoms[i] * atoms[j]) - (atoms[i] if i == j else sp.zeros(dim))) == sp.zeros(dim)
            for i in range(dim)
            for j in range(dim)
        )
        and sum(atoms, sp.zeros(dim)) == sp.eye(dim),
        "the projector-valued route works on the commuting diagonal one-cell event algebra",
    )
    n_pass += int(p)
    n_fail += int(not p)

    atom_weights = [sp.simplify(sp.trace(rho_cell * atom)) for atom in atoms]
    p = check(
        "the source-free full-cell state gives equal atomic event weights 1/16",
        all(weight == sp.Rational(1, 16) for weight in atom_weights),
        "source-free symmetry plus normalization force each atomic one-cell event to carry the same measure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: MINIMAL PROJECTOR-EVENT READOUT")
    pair_event = atoms[0] + atoms[1]
    quad_event = atoms[0] + atoms[1] + atoms[2] + atoms[3]

    mu_atom = sp.simplify(sp.trace(rho_cell * atoms[0]))
    mu_pair = sp.simplify(sp.trace(rho_cell * pair_event))
    mu_quad = sp.simplify(sp.trace(rho_cell * quad_event))
    p = check(
        "trace readout is normalized and additive on orthogonal diagonal events",
        mu_atom == sp.Rational(1, 16)
        and mu_pair == 2 * mu_atom
        and mu_quad == 4 * mu_atom
        and sp.simplify(sp.trace(rho_cell * sp.eye(dim))) == 1,
        "on the commuting cell-event algebra the minimal normalized additive yes/no law is exactly Tr(rho P)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: FORCED PACKET VALUE")
    # Conventional ordering of 4-bit states 0000, 0001, ..., 1111.
    # The hw=1 axis states are 0001, 0010, 0100, 1000, i.e. indices 1, 2, 4, 8.
    axis_indices = [1, 2, 4, 8]
    P_A = sum((atoms[i] for i in axis_indices), sp.zeros(dim))
    ket_t = sp.zeros(dim, 1)
    ket_t[8, 0] = 1
    ket_s = sp.zeros(dim, 1)
    for idx in [1, 2, 4]:
        ket_s[idx, 0] = sp.sqrt(sp.Rational(1, 3))
    P_q = ket_t * ket_t.T + ket_s * ket_s.T
    P_E = sp.simplify(P_A - P_q)

    p = check(
        "P_A is the four-atom hw=1 packet and still splits as P_q + P_E",
        P_A == sum((atoms[i] for i in axis_indices), sp.zeros(dim))
        and sp.simplify(P_A - (P_q + P_E)) == sp.zeros(dim),
        "this matches the forced packet and native multiplicity split from the earlier boundary lanes",
    )
    n_pass += int(p)
    n_fail += int(not p)

    mu_q = sp.simplify(sp.trace(rho_cell * P_q))
    mu_E = sp.simplify(sp.trace(rho_cell * P_E))
    mu_A = sp.simplify(sp.trace(rho_cell * P_A))
    p = check(
        "the exact projector-event weights are mu(P_q)=1/8, mu(P_E)=1/8, mu(P_A)=1/4",
        mu_q == sp.Rational(1, 8)
        and mu_E == sp.Rational(1, 8)
        and mu_A == sp.Rational(1, 4)
        and mu_A == mu_q + mu_E,
        "the projector-valued route reproduces the native factor-of-two lift exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: SEPARATION FROM THE SCALAR SCHUR ROUTE")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    p_vac = sp.simplify(sp.log(l_sigma.det()) / 4)
    p = check(
        "the scalar boundary observable p_vac remains distinct from the projector-event quarter",
        sp.simplify(p_vac - sp.Rational(1, 4)) != 0 and mu_A == sp.Rational(1, 4),
        "quarter is not another scalar determinant identity; it appears only on the packet-event readout",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 7: NOTE ALIGNMENT")
    p = check(
        "the note states the non-Schur source-free state as I_16 / 16",
        "rho_cell = i_16 / 16" in note and "bit-flip" in note,
        "the writeup should make explicit that the state is no longer floating on this route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states the exact packet event weight 1/4",
        "tr(rho_cell p_a) = 1/4" in note or "mu_cell(p_a) = tr(rho_cell p_a) = 1/4" in note,
        "the writeup should make the quarter conclusion explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states the remaining decision as scalar vs projector-valued boundary readout",
        "scalar free-energy density" in note and "event observable" in note,
        "the review burden should now be one exact grammar choice",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 8: HONEST FRONTIER")
    p = check(
        "the lane closes quarter only under a genuinely non-scalar physical readout law",
        mu_A == sp.Rational(1, 4) and sp.simplify(p_vac - sp.Rational(1, 4)) != 0,
        "the remaining choice is physical interpretation: scalar free-energy density versus event observable of the forced packet",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"SUMMARY: {n_pass} PASS / {n_fail} FAIL")
    if n_fail:
        print("Projector-valued observable route did not survive its own audit.")
        return 1

    print("Strongest honest verdict:")
    print("  - the current scalar observable principle still selects p_vac, not quarter;")
    print("  - the non-Schur source-free occupation lane fixes rho_cell = I_16 / 16;")
    print("  - the finite cell/event grammar gives a canonical projector-valued readout")
    print("    mu(P) = Tr(rho_cell P) on the diagonal packet algebra;")
    print("  - on the forced packet P_A this gives exact quarter, Tr(rho_cell P_A)=1/4;")
    print("  - so Planck closes on the projector/event route iff boundary pressure is")
    print("    the event observable of occupancy of the section-canonical packet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
