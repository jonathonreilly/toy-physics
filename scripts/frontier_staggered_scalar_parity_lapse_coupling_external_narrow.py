#!/usr/bin/env python3
"""Runner for the staggered scalar parity / lapse coupling external narrow theorem.

The note records the algebraic content of the literature-correct staggered scalar
coupling forms (parity (P), lapse (L)) and the per-site distinction from the
additive identity coupling (I). This runner verifies the algebraic identities
with exact Fraction arithmetic on small staggered lattices, and runs the
source-note boundary checks.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "STAGGERED_SCALAR_PARITY_LAPSE_COUPLING_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-16.md"

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {label}")
    if detail:
        print(f"         {detail}")


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def epsilon(coords: tuple) -> int:
    """Staggered sign factor (-1)^{sum_i x_i}."""
    s = sum(coords)
    return 1 if s % 2 == 0 else -1


def test_staggered_sign_alternates() -> None:
    section("T1: staggered sign epsilon(x) = (-1)^{sum_i x_i} alternates between NN sites")
    # 1D: every site flips with its neighbour
    n1d = 8
    eps_1d = [epsilon((x,)) for x in range(n1d)]
    nn_flips_1d = all(eps_1d[x] != eps_1d[x + 1] for x in range(n1d - 1))
    in_pm1 = all(e in (-1, 1) for e in eps_1d)
    check("epsilon(x) in {-1, +1} for 1D sites x = 0..7", in_pm1, f"eps_1d = {eps_1d}")
    check("epsilon flips between every nearest-neighbour pair in 1D", nn_flips_1d)

    # 3D: every site flips with each neighbour along each axis
    side = 3
    fail_axis = []
    for axis in range(3):
        for coords in product(range(side), repeat=3):
            nbr = list(coords)
            nbr[axis] = (nbr[axis] + 1) % side
            if epsilon(coords) == epsilon(tuple(nbr)) and ((nbr[axis] - coords[axis]) % side != 0):
                # NN along axis must flip (modulo wraparound where side parity matters)
                if (nbr[axis] - coords[axis]) in (1, -1):
                    fail_axis.append((axis, coords, tuple(nbr)))
    check("epsilon flips between NN sites on 3D cubic lattice (axis-aligned)",
          len(fail_axis) == 0,
          f"violations = {fail_axis}")


def test_parity_diagonal_value() -> None:
    section("T2: parity-coupled diagonal (m + Phi(x)) * epsilon(x) hand-check")
    # Choose rational m and a rational Phi profile so values are exact in Fraction.
    m = Fraction(3, 10)  # 0.3
    # Phi on a 1D 4-site lattice
    phi = [Fraction(1, 10), Fraction(-1, 5), Fraction(2, 5), Fraction(0)]
    # Expected H_diag^{parity}(x) = (m + phi[x]) * epsilon(x)
    n = len(phi)
    expected = [(m + phi[x]) * Fraction(epsilon((x,))) for x in range(n)]
    # Hand-verified values:
    # x=0: eps=+1; (0.3 + 0.1)*1 = 2/5
    # x=1: eps=-1; (0.3 - 0.2)*-1 = -1/10
    # x=2: eps=+1; (0.3 + 0.4)*1 = 7/10
    # x=3: eps=-1; (0.3 + 0)*-1 = -3/10
    hand = [Fraction(2, 5), Fraction(-1, 10), Fraction(7, 10), Fraction(-3, 10)]
    check("computed (m + Phi(x)) * eps(x) matches hand values at x = 0..3",
          expected == hand,
          f"computed = {expected}, hand = {hand}")


def test_lapse_hermiticity_diagonal_kernel() -> None:
    section("T3: lapse Hamiltonian sqrt(N) H_flat sqrt(N) Hermitian for real Phi >= -m")
    # Take a small 4x4 Hermitian H_flat (real symmetric is a special case) with rational entries.
    # H_flat[i][j] = H_flat[j][i] (real symmetric => Hermitian).
    n = 4
    H_flat = [
        [Fraction(0), Fraction(1, 2), Fraction(0), Fraction(0)],
        [Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(0)],
        [Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)],
        [Fraction(0), Fraction(0), Fraction(1, 2), Fraction(0)],
    ]
    # H_flat hermitian
    H_flat_hermitian = all(H_flat[i][j] == H_flat[j][i] for i in range(n) for j in range(n))
    check("test H_flat is Hermitian (real symmetric)", H_flat_hermitian)

    # Pick rational lapse values; require Phi(x) >= -m so N(x) >= 0.
    # Use perfect squares so sqrt is exact in Fraction.
    # N values: 1/4, 1, 9/4, 4 -> sqrt: 1/2, 1, 3/2, 2 -> exact rationals.
    sqrt_N = [Fraction(1, 2), Fraction(1, 1), Fraction(3, 2), Fraction(2, 1)]
    # D H_flat D entry (i, j) = sqrt_N[i] * H_flat[i][j] * sqrt_N[j]
    H_grav = [[sqrt_N[i] * H_flat[i][j] * sqrt_N[j] for j in range(n)] for i in range(n)]
    # Verify Hermiticity
    grav_hermitian = all(H_grav[i][j] == H_grav[j][i] for i in range(n) for j in range(n))
    check("sqrt(N) H_flat sqrt(N) is Hermitian (entry-by-entry equality)", grav_hermitian)

    # Spot-check a specific entry: H_grav[0][1] = (1/2) * (1/2) * 1 = 1/4
    spot = H_grav[0][1] == Fraction(1, 4) and H_grav[1][0] == Fraction(1, 4)
    check("H_grav[0][1] = H_grav[1][0] = 1/4 (specific spot-check)", spot,
          f"H_grav[0][1] = {H_grav[0][1]}, H_grav[1][0] = {H_grav[1][0]}")


def test_per_site_difference_identity() -> None:
    section("T4: per-site identity H_diag^{parity}(x) - H_diag^{identity,+}(x) = Phi(x) * (eps(x) - 1)")
    m = Fraction(3, 10)
    phi = [Fraction(1, 10), Fraction(-1, 5), Fraction(2, 5), Fraction(0), Fraction(3, 7)]
    n = len(phi)
    for x in range(n):
        e = epsilon((x,))
        H_parity = (m + phi[x]) * Fraction(e)
        H_identity_plus = m * Fraction(e) + phi[x]  # m*eps + Phi
        rhs = phi[x] * (Fraction(e) - 1)
        ok = (H_parity - H_identity_plus) == rhs
        if not ok:
            check(f"per-site identity at x = {x} (eps={e}, Phi={phi[x]})", False,
                  f"H_parity - H_identity_plus = {H_parity - H_identity_plus}, expected {rhs}")
            return
    check("per-site identity holds on all 5 sites for the test profile", True,
          "matches phi*(eps-1): 0 on even sites, -2*phi on odd sites")


def test_parity_flips_identity_does_not() -> None:
    section("T5: (P) diagonal flips sign by epsilon; (I) diagonal does not")
    m = Fraction(2, 5)
    Phi_const = Fraction(1, 10)
    n = 6
    # Constant Phi(x) = Phi_const so we isolate the eps-driven sign flip
    parity_diag = [(m + Phi_const) * Fraction(epsilon((x,))) for x in range(n)]
    identity_diag = [m * Fraction(epsilon((x,))) + Phi_const for x in range(n)]
    # Parity must alternate; identity must NOT alternate when |Phi| < m * epsilon (constant +Phi shifts)
    parity_alternates = all(parity_diag[x] == -parity_diag[x + 1] for x in range(n - 1))
    # Identity values: on even sites: m + Phi = 1/2; on odd sites: -m + Phi = -3/10. Not alternating in sign-by-eps.
    identity_alternates_by_eps = all(identity_diag[x] == -identity_diag[x + 1] for x in range(n - 1))
    check("parity diagonal alternates: (P)[x] = -(P)[x+1]", parity_alternates,
          f"parity = {parity_diag}")
    check("identity diagonal does NOT alternate by eps when Phi is constant",
          not identity_alternates_by_eps,
          f"identity = {identity_diag}")


def test_lapse_reduces_to_flat_at_zero_phi() -> None:
    section("T6: lapse coupling reduces to H_flat at Phi(x) = 0")
    n = 4
    # H_flat as in T3
    H_flat = [
        [Fraction(0), Fraction(1, 2), Fraction(0), Fraction(0)],
        [Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(0)],
        [Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)],
        [Fraction(0), Fraction(0), Fraction(1, 2), Fraction(0)],
    ]
    sqrt_N = [Fraction(1)] * n  # all 1 since Phi == 0 implies N == 1
    H_grav = [[sqrt_N[i] * H_flat[i][j] * sqrt_N[j] for j in range(n)] for i in range(n)]
    equals_flat = all(H_grav[i][j] == H_flat[i][j] for i in range(n) for j in range(n))
    check("sqrt(N) H_flat sqrt(N) with N(x)=1 equals H_flat exactly", equals_flat)


def test_well_hill_distinction_under_parity() -> None:
    section("T7: well (Phi<0) vs hill (Phi>0) under (P) gives sub-lattice-distinguishable shifts that (I) does not")
    m = Fraction(3, 10)
    # well: Phi at site
    Phi_well = Fraction(-1, 10)
    Phi_hill = Fraction(1, 10)
    # On odd site (eps = -1)
    parity_odd_well = (m + Phi_well) * Fraction(-1)  # = -(0.3 - 0.1) = -0.2
    parity_odd_hill = (m + Phi_hill) * Fraction(-1)  # = -(0.3 + 0.1) = -0.4
    identity_odd_well = m * Fraction(-1) + Phi_well  # = -0.3 - 0.1 = -0.4
    identity_odd_hill = m * Fraction(-1) + Phi_hill  # = -0.3 + 0.1 = -0.2
    # Parity odd: well -> -1/5, hill -> -2/5 (well greater than hill)
    # Identity odd: well -> -2/5, hill -> -1/5 (well less than hill -- opposite ordering)
    parity_well_greater = parity_odd_well > parity_odd_hill
    identity_well_less = identity_odd_well < identity_odd_hill
    check("under (P), odd-site diagonal is GREATER for well than hill (Phi*(eps=-1) widens hill)",
          parity_well_greater,
          f"parity well = {parity_odd_well}, parity hill = {parity_odd_hill}")
    check("under (I), odd-site diagonal is LESS for well than hill (opposite ordering)",
          identity_well_less,
          f"identity well = {identity_odd_well}, identity hill = {identity_odd_hill}")
    # The two on-site operators distinguish well from hill in OPPOSITE directions on odd sub-lattice.
    # Even sub-lattice (eps = +1): parity even well = m + Phi_well = 0.2; parity even hill = 0.4 -- hill is greater
    # So under (P), sub-lattice ordering is asymmetric: hill widens both sub-lattices toward higher local |H|.
    parity_even_well = (m + Phi_well) * Fraction(1)
    parity_even_hill = (m + Phi_hill) * Fraction(1)
    even_hill_greater = parity_even_hill > parity_even_well
    check("under (P), even-site diagonal is GREATER for hill than well (different sub-lattice ordering than odd)",
          even_hill_greater,
          f"parity even well = {parity_even_well}, parity even hill = {parity_even_hill}")


def test_note_boundary() -> None:
    section("T8: source-note boundary")
    text = NOTE.read_text(encoding="utf-8")
    lower = text.lower()
    # Forbidden ASSERTING phrasings this note must NOT contain.
    # (We look for assertion-positive phrasings, since the Boundary section
    #  legitimately mentions disclaim-form phrases like "does not claim
    #  universal irregular-graph closure".)
    forbidden_asserts = [
        "this note closes the staggered-dirac realization gate",
        "this note derives the parity coupling from a1",
        "we derive the parity coupling from a1",
        "the parity coupling is derived from a1 + a2",
        "this note closes the universal irregular-graph",
        "this note closes the trajectory-sign",
        "we close the trajectory-sign",
        "this note proves a new framework axiom",
        "we add a new framework axiom",
        "pipeline-derived status: retained",
    ]
    # Required disclaimers / structural markers
    required = [
        "does not claim",
        "minimal_axioms_2026-05-03",
        "external",
        "honestly open",
        "**claim type:** bounded_theorem",
    ]
    check("note declares bounded_theorem", "**Claim type:** bounded_theorem" in text)
    check("note has Boundary section", "## Boundary" in text)
    missing = [item for item in required if item not in lower]
    check("note contains required disclaimers / references",
          len(missing) == 0,
          f"missing = {missing}" if missing else "all required disclaimers present")
    found_forbidden = [item for item in forbidden_asserts if item in lower]
    check("note avoids assertion-form over-claims (axiom-forcing, universal-graph, trajectory-sign, retained-status)",
          len(found_forbidden) == 0,
          f"found = {found_forbidden}" if found_forbidden else "no asserting-form over-claims found")


def main() -> int:
    print("# Staggered scalar parity / lapse coupling external narrow theorem runner")
    print(f"# Source note: {NOTE.relative_to(ROOT)}")
    test_staggered_sign_alternates()
    test_parity_diagonal_value()
    test_lapse_hermiticity_diagonal_kernel()
    test_per_site_difference_identity()
    test_parity_flips_identity_does_not()
    test_lapse_reduces_to_flat_at_zero_phi()
    test_well_hill_distinction_under_parity()
    test_note_boundary()
    print(f"\n=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
