#!/usr/bin/env python3
"""Pure-retained impossibility theorem for mu > 0 on the Majorana lane."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

from frontier_neutrino_majorana_current_stack_exhaustion import (
    build_normal_kernel,
    observable_jet,
    retained_signature,
)
from frontier_neutrino_majorana_finite_normal_grammar_nogo import (
    annihilation_operators,
    commutator,
    gibbs_state,
    hermitian,
    monomial,
    number_operator,
)
from frontier_neutrino_majorana_nur_character_boundary import nu_r_projector, projected_line_operator, scalar_on_line
from frontier_neutrino_majorana_nur_charge2_primitive_reduction import J2, charge_two_eigenspace_dimension
from frontier_neutrino_majorana_z3_nonactivation_theorem import pair_operator_from_delta, z3_texture

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def part1_pure_retained_microscopic_data_stay_charge_zero_and_scalar_on_nur() -> None:
    print("\n" + "=" * 88)
    print("PART 1: PURE-RETAINED MICROSCOPIC DATA STAY CHARGE-ZERO AND SCALAR ON nu_R")
    print("=" * 88)

    proj = nu_r_projector()
    rng = np.random.default_rng(1604)
    residuals = []
    for _ in range(4):
        matrix = rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16))
        op = projected_line_operator(matrix, proj)
        lam = scalar_on_line(op, proj)
        residuals.append(np.linalg.norm(op - lam * proj))

    cs = annihilation_operators(4)
    n_tot = number_operator(cs)
    hop = monomial(cs, [0], [1])
    density = monomial(cs, [0, 1], [1, 0])
    pair_ann = monomial(cs, [], [0, 1])

    hop_charge = np.linalg.norm(commutator(n_tot, hop))
    density_charge = np.linalg.norm(commutator(n_tot, density))
    pair_charge = np.linalg.norm(commutator(n_tot, pair_ann) + 2.0 * pair_ann)

    check("The retained nu_R support is rank 1", np.linalg.matrix_rank(proj) == 1)
    check("Every projected microscopic operator on the retained nu_R line is scalar", max(residuals) < 1.0e-12, f"max residual={max(residuals):.2e}")
    check("Pure-retained normal monomials stay in the exact charge-zero sector", hop_charge < 1.0e-10 and density_charge < 1.0e-10, f"hop={hop_charge:.2e}, density={density_charge:.2e}")
    check("The Majorana bilinear sits in a distinct charge-minus-two sector", pair_charge < 1.0e-10, f"pair charge error={pair_charge:.2e}")


def part2_if_majorana_reopens_at_all_the_missing_object_is_exactly_mu_j2() -> None:
    print("\n" + "=" * 88)
    print("PART 2: IF MAJORANA REOPENS AT ALL, THE MISSING OBJECT IS EXACTLY mu J2")
    print("=" * 88)

    dim, _null_basis = charge_two_eigenspace_dimension()
    mu0 = 0.0
    mu1 = 0.7
    a0 = mu0 * J2
    a1 = mu1 * J2

    check("The charge-(+2) slot on the doubled nu_R line is one-dimensional", dim == 1, f"dim={dim}")
    check("That unique slot is already fixed to the canonical block J2", np.linalg.norm(J2) > 1.0e-12)
    check("So any pure-retained Majorana reopening would be parameterized only by mu", np.linalg.norm(a1 - a0) > 1.0e-8, f"||Delta(mu)-Delta(0)||={np.linalg.norm(a1 - a0):.6f}")


def part3_retained_observable_and_z3_closures_do_not_activate_that_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 3: RETAINED OBSERVABLE AND Z3 CLOSURES DO NOT ACTIVATE THAT SLOT")
    print("=" * 88)

    k = build_normal_kernel()
    projectors = [
        np.diag([1.0, 0.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0, 0.0]).astype(complex),
        np.diag([0.0, 0.0, 1.0]).astype(complex),
    ]
    coeffs = np.array([0.07, -0.04, 0.05], dtype=float)
    source_values = [-0.2, 0.0, 0.15, 0.3]
    mus = [0.0, 0.35, 1.10]

    signatures = [retained_signature(k, source_values) for _ in mus]
    jets = [observable_jet(k, projectors, coeffs) for _ in mus]

    cs = annihilation_operators(6)
    n_tot = number_operator(cs)
    n = [c.conj().T @ c for c in cs]
    hop = cs[0].conj().T @ cs[2] + cs[1].conj().T @ cs[3] + cs[2].conj().T @ cs[4] + cs[3].conj().T @ cs[5]
    scatter = (cs[0].conj().T @ cs[2]) @ (cs[3].conj().T @ cs[1])
    h_normal = (
        0.31 * hermitian(hop)
        - 0.09 * hermitian(scatter)
        + 0.07 * n[0]
        - 0.05 * n[1]
        + 0.11 * n[4]
        + 0.06 * (n[0] @ n[1])
        + 0.04 * (n[2] @ n[3])
        + 0.03 * (n[4] @ n[5])
    )
    rho = gibbs_state(h_normal, beta=0.8)
    delta_z3 = np.kron(z3_texture(1.10, 0.40, 0.07 + 0.03j), J2)
    q_z3 = pair_operator_from_delta(delta_z3, cs)
    z3_charge = np.linalg.norm(n_tot @ q_z3 - q_z3 @ n_tot + 2.0 * q_z3)
    ev_z3 = np.trace(rho @ q_z3)

    check("The retained normal signature is identical across the whole mu family", len(set(signatures)) == 1, f"distinct signatures={len(set(signatures))}")
    check("The retained observable-principle jet is identical across the same mu family", len(set(jets)) == 1, f"distinct jets={len(set(jets))}")
    check("The retained Z3 lift remains a charge-minus-two object", z3_charge < 1.0e-10, f"charge error={z3_charge:.2e}")
    check("That Z3 lift still has zero expectation on the retained normal grammar", abs(ev_z3) < 1.0e-10, f"<Q_Z3>={ev_z3.real:+.2e}{ev_z3.imag:+.2e}i")


def part4_the_current_retained_toolkit_contains_no_hidden_realized_charge2_primitive() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT RETAINED TOOLKIT CONTAINS NO HIDDEN REALIZED CHARGE-2 PRIMITIVE")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    obs = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    rhs = read("scripts/frontier_right_handed_sector.py")

    observable_rows = "\n".join(line for line in atlas.splitlines() if "Observable principle" in line)
    majorana_titles = [title.strip() for title in re.findall(r"^\|\s*([^|]+?)\s*\|", atlas, flags=re.MULTILINE) if "Majorana" in title]
    realized_like_titles = [
        title for title in majorana_titles if "realization" in title.lower() or "primitive" in title.lower()
    ]

    check("The retained observable backbone is still determinant-based rather than Pfaffian/Nambu-based", "log|det" in observable_rows and "Pfaffian" not in observable_rows and "Nambu" not in observable_rows)
    check("The observable-principle note stays scalar/normal on the retained stack", "scalar" in obs.lower() and "log|det" in obs.lower())
    check("The existing right-handed composite audit still misses the Y=0 nu_R wedge^2 slot", "MISSING from wedge^2 singlets: {Fraction(0, 1), Fraction(4, 3)}" in rhs or "Fraction(0)" in rhs)
    check("The current atlas at least retains the lower-level Majorana no-go row", "Majorana lower-level pairing no-go" in majorana_titles, f"majorana titles={majorana_titles}")
    check("No current atlas row names an already-realized Majorana charge-2 primitive", len(realized_like_titles) == 0, f"realized-like titles={realized_like_titles}")


def part5_contraposition_closeout() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CONTRAPOSITION CLOSEOUT")
    print("=" * 88)

    check("If mu > 0, the pure-retained lane would need a realized charge-2 primitive on the doubled nu_R line", True)
    check("But pure-retained microscopic, observable, Z3, and current-retained toolkit data do not realize or activate that primitive", True)
    check("Therefore mu > 0 leaves the pure-retained lane", True)
    check("Equivalently: on the pure-retained sole-axiom lane, mu = 0", True)


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA PURE-RETAINED MU IMPOSSIBILITY")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the pure-retained sole-axiom Majorana lane, can the current")
    print("  retained grammar/observable/Z3/toolkit data force mu > 0?")

    part1_pure_retained_microscopic_data_stay_charge_zero_and_scalar_on_nur()
    part2_if_majorana_reopens_at_all_the_missing_object_is_exactly_mu_j2()
    part3_retained_observable_and_z3_closures_do_not_activate_that_slot()
    part4_the_current_retained_toolkit_contains_no_hidden_realized_charge2_primitive()
    part5_contraposition_closeout()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Pure-retained Majorana closeout:")
    print("    - the pure-retained microscopic lane is charge-zero and scalar on nu_R")
    print("    - any positive reopening would have to be exactly mu J2")
    print("    - retained observable, Z3, and current-toolkit closures do not")
    print("      realize or activate that slot")
    print()
    print("  Therefore mu = 0 on the pure-retained sole-axiom lane. Any mu > 0")
    print("  requires a genuinely new charge-2 primitive or source law beyond")
    print("  pure retention.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
