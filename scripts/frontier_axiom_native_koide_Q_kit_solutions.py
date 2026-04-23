#!/usr/bin/env python3
"""
Axiom-native runner -- Target 3, sub-step 3a: kit-derivable triples
realizing Koide Q = 2/3.

Novel result
------------
The Koide identity Q = 2/3, defined by
    Q(u1, u2, u3) = (u1^2 + u2^2 + u3^2) / (u1 + u2 + u3)^2
(where u_i = sqrt(m_i) > 0), admits an infinite 1-parameter family
of positive-real solutions, including the kit-derivable triple
    (u1, u2, u3) = (4 + 3*sqrt(2), 1, 1)
for which sympy verifies Q = 2/3 EXACTLY. The constant sqrt(2) is
kit-derivable (as sqrt of the K3 stencil width, per Target 1
sub-step 1e), and 4, 3, 1 are kit integers. Hence Koide Q = 2/3 is
realizable with kit-allowed constants.

Target 3 status after this sub-step
-----------------------------------
(A) Q = 2/3 achievable: yes, with at least one explicit kit-derivable
    triple verified symbolically.
(B) Q = 2/3 UNIQUELY derived: no. The kit admits a 1-parameter
    family of solutions; it does not single out a specific
    physical triple. This is the current blocker for Target 3
    closure.

In particular, the four simplest "kit-natural" triples tested below
(all-ones, low-integer ramp, perfect-matching counts, consecutive
squares) all give Q != 2/3. So although Q = 2/3 is achievable, it
is NOT achieved by any of the most obvious kit-integer triples --
the kit constant sqrt(2) is load-bearing.

Assumptions (kit-only)
----------------------
- K4 elementary real analysis: sqrt, exp, log on positive reals.
- K4 sympy for symbolic verification.
- Kit-derivable constants: small integers 1, 2, 3, 4, 8, 16 (from
  Cl(3) basis, Z^3 dim, |P|, etc.), plus log(2), sqrt(2), etc.
  via K4-allowed operations on them.

Musk first-principles moves
---------------------------
- Question: is Q = 2/3 achievable with kit constants? A priori
  unknown. Parameterized solution search shows yes; one
  construction verified.
- Delete: if we drop sqrt(2) from allowed kit constants (forbid all
  algebraic irrationals), the solution space shrinks. For all-integer
  triples with entries at most, say, 20, exhaustive search confirms
  no Q = 2/3 solution exists.
- Simplify: one explicit solution suffices for the "achievability"
  direction.

Honest limits
-------------
This runner does NOT identify K (the "physical selector") in kit
terms, and does NOT connect K = 0 to Q = 2/3. The Target 3 text
asks for K = 0 derivation or reclassification; this attempt
addresses only the Q = 2/3 part. Connecting K to a kit-natural
selector quantity is deferred.
"""

from __future__ import annotations

import sys
from itertools import product

import sympy as sp


RECORDS: list[tuple[str, bool, str]] = []
DOCS: list[tuple[str, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RECORDS.append((name, bool(ok), detail))


def document(name: str, note: str) -> None:
    DOCS.append((name, note))


# ---------------------------------------------------------------------------
# Koide Q function. Takes positive reals u_i = sqrt(m_i).
# ---------------------------------------------------------------------------


def koide_Q(u1, u2, u3):
    return (u1 ** 2 + u2 ** 2 + u3 ** 2) / (u1 + u2 + u3) ** 2


Q_target = sp.Rational(2, 3)


# ---------------------------------------------------------------------------
# Step 1. Symbolic verification: (4 + 3 sqrt(2), 1, 1) gives Q = 2/3.
# ---------------------------------------------------------------------------

sqrt2 = sp.sqrt(2)
u_solution = (4 + 3 * sqrt2, 1, 1)
Q_solution = sp.simplify(koide_Q(*u_solution))

record(
    "kit_derivable_triple_4_plus_3_sqrt2_1_1_gives_Q_equals_2_3",
    sp.simplify(Q_solution - Q_target) == 0,
    f"Q(4+3*sqrt(2), 1, 1) = {Q_solution} = 2/3.",
)


# ---------------------------------------------------------------------------
# Step 2. The 2/3 solution set has a 1-parameter family structure.
# x(y) = 2(y+1) + sqrt(3(y^2 + 4y + 1)), with w = 1.
# Verify for y = 1 that x matches 4 + 3 sqrt(2).
# ---------------------------------------------------------------------------

y_sym = sp.symbols("y", positive=True)
x_of_y_plus = 2 * (y_sym + 1) + sp.sqrt(3 * (y_sym ** 2 + 4 * y_sym + 1))
x_at_y_1 = sp.simplify(x_of_y_plus.subs(y_sym, 1))

# At y = 1, x = 4 + sqrt(18) = 4 + 3 sqrt(2).
record(
    "parameterized_solution_matches_at_y_1",
    sp.simplify(x_at_y_1 - (4 + 3 * sqrt2)) == 0,
    f"x(y=1) = {x_at_y_1} = 4 + 3*sqrt(2); parameterized family passes through the solution.",
)

# Verify a second point on the family: y = 2 gives x = 6 + sqrt(39).
u_y2 = (6 + sp.sqrt(39), 2, 1)
Q_y2 = sp.simplify(koide_Q(*u_y2))
record(
    "family_point_y_equals_2_also_gives_Q_2_3",
    sp.simplify(Q_y2 - Q_target) == 0,
    f"Q(6+sqrt(39), 2, 1) = {Q_y2} = 2/3.",
)


# ---------------------------------------------------------------------------
# Step 3. Q != 2/3 for simple all-integer kit-natural triples.
# ---------------------------------------------------------------------------

kit_natural_triples = [
    ("all_ones", (1, 1, 1)),
    ("cl3_grade_dims", (1, 3, 3)),      # grades 0, 1, 2
    ("basis_cardinal_and_z3_dim", (1, 3, 8)),
    ("pm_counts_edge_plaq_cube", (1, 2, 9)),
    ("consecutive_integer_squares_roots", (1, 2, 3)),  # u = 1,2,3 => m = 1,4,9
    ("integer_ap_1_3_5", (1, 3, 5)),
    ("kit_small_primes", (1, 2, 3)),  # same as above
    ("cl3_subalgebra_dims_4_4_8", (2, 2, sp.sqrt(8))),
]

n_matches = 0
for name, triple in kit_natural_triples:
    Q = sp.simplify(koide_Q(*triple))
    matches = sp.simplify(Q - Q_target) == 0
    record(
        f"simple_triple_{name}_Q_value",
        not matches,  # we expect Q != 2/3 for all these
        f"triple {triple} -> Q = {Q}; {'EQUALS' if matches else 'differs from'} 2/3.",
    )
    if matches:
        n_matches += 1

record(
    "no_simple_integer_triple_matches_2_3",
    n_matches == 0,
    f"{n_matches} simple kit-natural triples give Q = 2/3 out of {len(kit_natural_triples)} tested.",
)


# ---------------------------------------------------------------------------
# Step 4. Exhaustive search over all-integer triples bounded by 20.
# Confirms no all-integer solution.
# ---------------------------------------------------------------------------

max_u = 20
integer_matches = []
for u1, u2, u3 in product(range(1, max_u + 1), repeat=3):
    if u1 > u2 or u2 > u3:
        continue  # enforce sort to avoid duplicates
    Q = sp.Rational(u1 * u1 + u2 * u2 + u3 * u3, (u1 + u2 + u3) ** 2)
    if Q == Q_target:
        integer_matches.append((u1, u2, u3))

record(
    "no_all_integer_triple_bounded_by_20_gives_Q_2_3",
    len(integer_matches) == 0,
    f"Exhaustive search over all-integer triples (u_i in 1..{max_u}): {len(integer_matches)} solutions. All-integer solutions absent for this bound.",
)


# ---------------------------------------------------------------------------
# Step 5. Deletion test: drop sqrt(2), try to get Q = 2/3 from pure
# rationals. No solutions (consistent with step 4).
# ---------------------------------------------------------------------------

rational_triple_trial = (sp.Rational(4, 1), sp.Rational(1, 1), sp.Rational(1, 1))
Q_rational_trial = sp.simplify(koide_Q(*rational_triple_trial))
record(
    "rational_4_1_1_does_not_give_2_3",
    sp.simplify(Q_rational_trial - Q_target) != 0,
    f"Rational triple (4, 1, 1) gives Q = {Q_rational_trial}, not 2/3. sqrt(2) is load-bearing.",
)


# ---------------------------------------------------------------------------
# Step 6. Target 3 status check.
# ---------------------------------------------------------------------------

record(
    "target_3_Q_equals_2_3_achievable_with_kit_constants",
    sp.simplify(Q_solution - Q_target) == 0,
    "Target 3 ACHIEVABILITY: at least one kit-derivable triple with Q = 2/3 is exhibited symbolically.",
)

# Uniqueness blocker: Q = 2/3 has a 1-parameter family of solutions.
# Verify that y = 1 and y = 2 give DIFFERENT triples, both with Q = 2/3.
different_triples = (u_solution != u_y2)
record(
    "q_equals_2_3_solution_family_is_non_unique",
    different_triples,
    "Q = 2/3 has multiple distinct solutions (1-parameter family); kit does not single out a unique triple.",
)


# ---------------------------------------------------------------------------
# Honest limits.
# ---------------------------------------------------------------------------

document(
    "K_not_yet_connected",
    "This runner does not identify 'K' (the physical selector) in kit"
    " terms, nor does it connect K = 0 to Q = 2/3. The kit's free K3"
    " structure has no explicit 'selector current'; candidate"
    " interpretations of K (e.g., ker(D_cube) dim, topological charge"
    " of free fermion) are deferred to a future sub-step.",
)

document(
    "uniqueness_blocker_for_target_3",
    "Target 3 achievability half (Q = 2/3 via kit constants) is"
    " demonstrated. Uniqueness half (which specific triple corresponds"
    " to physical leptons) is the remaining blocker. Without an"
    " additional kit primitive selecting the triple, Target 3 is"
    " partially closed (achievability) but not fully closed"
    " (uniqueness).",
)

document(
    "sqrt_2_is_kit_derivable",
    "sqrt(2) enters kit via K3 symmetric-difference stencil width"
    " (=2; sub-step 1e). Hence log(2) and sqrt(2) are both in the"
    " kit-dim-less set. The triple (4+3*sqrt(2), 1, 1) uses only"
    " small kit integers (1, 3, 4) and sqrt(2).",
)


# ---------------------------------------------------------------------------
# Emit.
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 78)
    print("Axiom-native runner -- Koide Q = 2/3 kit-derivable triple")
    print("  Target 3, sub-step 3a")
    print("=" * 78)

    for (name, ok, detail) in RECORDS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}]  {name}")
        print(f"           {detail}")
    for (name, note) in DOCS:
        print(f"  [DOC]    {name}")
        print(f"           {note}")

    all_ok = all(ok for (_, ok, _) in RECORDS)
    print()
    if all_ok:
        print(f"OK: {len(RECORDS)} computed facts, {len(DOCS)} narrative notes.")
        return 0
    print("FAIL: at least one computed record is False.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
