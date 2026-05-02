#!/usr/bin/env python3
"""Pattern A narrow runner for `Z3_CONJUGATE_SUPPORT_TRICHOTOMY_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone Z_3 character-arithmetic identity:

  Let q_L = (q_L_1, q_L_2, q_L_3) be a permutation of Z_3 = {0, 1, 2}
  (i.e., the three q_L_i values are distinct mod 3), and let
  q_R = (q_R_1, q_R_2, q_R_3) be its pointwise conjugate
  q_R_i = -q_L_i mod 3.

  Let q_H be any element of Z_3.

  Define the support
      S(q_L, q_R, q_H) = { (i, j) in {1,2,3}^2 :
                            q_L_i + q_H + q_R_j = 0 mod 3 }.

  THEN:
    (i)  S is a permutation pattern (one entry per row, one per column);
    (ii) the three supports S(q_L, q_R, q_H) over q_H ∈ {0, 1, 2} are
         pairwise disjoint and their union is the full 3x3 grid;
    (iii) the three supports are exactly the diagonal pattern, the
         forward cyclic pattern, and the backward cyclic pattern, in
         some order determined by q_L.

This is class-A pure number theory / Z_3-character arithmetic. No DM-side
/ neutrino-side / Higgs-doublet authority is consumed, and no specific
physical assignment of the charges is claimed.

The distinct-Z_3-values hypothesis on q_L is essential: when q_L is
constant (e.g., (0, 0, 0)) the trichotomy fails (one q_H gives the full
grid as support, the other two give empty supports). The framework's
specific (q_L, q_R) = ((0, +1, -1), (0, -1, +1)) is one of the 6
permutations of (0, 1, 2).

Companion role: this is a Pattern A new narrow claim row carving out the
load-bearing class-(A) algebraic core of
`neutrino_dirac_z3_support_trichotomy_note` (claim_type=bounded_theorem,
audit_status=audited_conditional, td=77). The narrow theorem isolates the
Z_3-character arithmetic from any specific charge assignment, so it can be
audit-ratified independently of the parent's hypothesized
(q_L, q_R, q_H) values.
"""

from pathlib import Path
import sys
import json
from itertools import product, permutations

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


def support(q_L, q_R, q_H):
    """Return the set of (i, j) with q_L_i + q_H + q_R_j ≡ 0 mod 3."""
    return frozenset(
        (i, j)
        for i in range(3)
        for j in range(3)
        if (q_L[i] + q_H + q_R[j]) % 3 == 0
    )


def is_permutation_pattern(S):
    """A permutation pattern has exactly one entry per row and one per column."""
    if len(S) != 3:
        return False
    rows = {i for (i, j) in S}
    cols = {j for (i, j) in S}
    return rows == {0, 1, 2} and cols == {0, 1, 2}


# ============================================================================
section("Pattern A narrow theorem: Z_3 conjugate-pair support trichotomy")
# Statement: any conjugate pair (q_L, q_R) of Z_3-charge triples + any q_H
# in Z_3 forces the support S(q_L, q_R, q_H) into a permutation pattern.
# Over q_H in {0, 1, 2}, the three supports are disjoint and cover the
# full 3x3 grid. Pure number theory.
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: framework instance q_L = (0, 1, -1), q_R = (0, -1, 1) at q_H ∈ {0, 1, -1}")
# ----------------------------------------------------------------------------
q_L_fw = (0, 1, 2)  # representing (0, +1, -1) since -1 ≡ 2 mod 3
q_R_fw = tuple((-x) % 3 for x in q_L_fw)  # = (0, 2, 1) = (0, -1, +1)
print(f"\n  q_L (framework instance) = {q_L_fw} (i.e. (0, +1, -1))")
print(f"  q_R = -q_L mod 3 = {q_R_fw} (i.e. (0, -1, +1))")

# At q_H = 0: support should be diagonal {(0,0), (1,1), (2,2)} (1-indexed: (1,1), (2,2), (3,3))
S0 = support(q_L_fw, q_R_fw, 0)
expected_S0 = frozenset({(0, 0), (1, 1), (2, 2)})
check("framework instance, q_H = 0: support is diagonal {(1,1), (2,2), (3,3)}",
      S0 == expected_S0,
      detail=f"S = {sorted(S0)}")

# At q_H = +1: support should be forward cyclic {(1,2), (2,3), (3,1)} (0-indexed: (0,1), (1,2), (2,0))
S1 = support(q_L_fw, q_R_fw, 1)
expected_S1 = frozenset({(0, 1), (1, 2), (2, 0)})
check("framework instance, q_H = +1: support is forward cyclic {(1,2), (2,3), (3,1)}",
      S1 == expected_S1,
      detail=f"S = {sorted(S1)}")

# At q_H = -1 (= 2 mod 3): support should be backward cyclic {(1,3), (2,1), (3,2)}
S2 = support(q_L_fw, q_R_fw, 2)
expected_S2 = frozenset({(0, 2), (1, 0), (2, 1)})
check("framework instance, q_H = -1: support is backward cyclic {(1,3), (2,1), (3,2)}",
      S2 == expected_S2,
      detail=f"S = {sorted(S2)}")


# ----------------------------------------------------------------------------
section("Part 2: each support is a permutation pattern (one per row, one per column)")
# ----------------------------------------------------------------------------
for q_H, label in [(0, "q_H = 0"), (1, "q_H = +1"), (2, "q_H = -1")]:
    S = support(q_L_fw, q_R_fw, q_H)
    check(f"{label}: |S| = 3 and permutation (one per row, one per column)",
          is_permutation_pattern(S),
          detail=f"|S| = {len(S)}, rows = {sorted({i for (i,j) in S})}, cols = {sorted({j for (i,j) in S})}")


# ----------------------------------------------------------------------------
section("Part 3: three supports over q_H ∈ {0, 1, 2} are pairwise disjoint and cover full grid")
# ----------------------------------------------------------------------------
S_all = [support(q_L_fw, q_R_fw, q_H) for q_H in range(3)]
union = set().union(*S_all)
full_grid = {(i, j) for i in range(3) for j in range(3)}

# Pairwise disjoint
pairwise_disjoint = all(
    not (S_all[a] & S_all[b])
    for a in range(3)
    for b in range(a + 1, 3)
)
check("three supports are pairwise disjoint",
      pairwise_disjoint)
check("union of the three supports is the full 3x3 grid",
      union == full_grid,
      detail=f"|union| = {len(union)}, |full grid| = {len(full_grid)}")


# ----------------------------------------------------------------------------
section("Part 4: distinct-Z_3-values hypothesis is essential (constant q_L breaks trichotomy)")
# ----------------------------------------------------------------------------
# When q_L = (0, 0, 0), q_R = (0, 0, 0). At q_H = 0, support is full grid
# (9 entries). At q_H = 1 or 2, support is empty.
q_L_constant = (0, 0, 0)
q_R_constant = tuple((-x) % 3 for x in q_L_constant)
S_constant_0 = support(q_L_constant, q_R_constant, 0)
S_constant_1 = support(q_L_constant, q_R_constant, 1)
S_constant_2 = support(q_L_constant, q_R_constant, 2)

check("at constant q_L = (0,0,0): support at q_H = 0 is the FULL 3x3 grid (not a permutation)",
      len(S_constant_0) == 9,
      detail=f"|S| = {len(S_constant_0)} (not 3)")
check("at constant q_L = (0,0,0): supports at q_H = 1, 2 are empty",
      len(S_constant_1) == 0 and len(S_constant_2) == 0,
      detail=f"|S_1| = {len(S_constant_1)}, |S_2| = {len(S_constant_2)}")
check("constant-q_L counterexample confirms distinct-Z_3-values hypothesis is necessary",
      not is_permutation_pattern(S_constant_0))


# ----------------------------------------------------------------------------
section("Part 5: when q_L is a permutation of (0, 1, 2), the three patterns are diagonal/forward/backward cycle")
# ----------------------------------------------------------------------------
# A "permutation triple" is a triple where {q_L_1, q_L_2, q_L_3} = {0, 1, 2}.
# For each such triple, the three supports over q_H = 0, 1, 2 are exactly
# {diagonal, forward cycle, backward cycle} in some order.
diagonal = frozenset({(0, 0), (1, 1), (2, 2)})
forward_cycle = frozenset({(0, 1), (1, 2), (2, 0)})
backward_cycle = frozenset({(0, 2), (1, 0), (2, 1)})
canonical_three = {diagonal, forward_cycle, backward_cycle}

permutations_pass = True
perm_counter = 0
for q_L_perm in permutations((0, 1, 2)):
    q_R_perm = tuple((-x) % 3 for x in q_L_perm)
    perm_counter += 1
    S_set = {support(q_L_perm, q_R_perm, q_H) for q_H in range(3)}
    if S_set != canonical_three:
        permutations_pass = False
        print(f"   FAILED at q_L permutation = {q_L_perm}: supports = {S_set}")
        break

check(f"all 6 permutations of (0, 1, 2) for q_L give exactly {{diagonal, forward cycle, backward cycle}} over q_H",
      permutations_pass,
      detail=f"verified for {perm_counter} permutations")


# ----------------------------------------------------------------------------
section("Part 6: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('neutrino_dirac_z3_support_trichotomy_note', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")
print(f"    deps: {parent.get('deps')}")

check("parent row class-A load-bearing step (algebraic Z_3 character arithmetic)",
      parent.get('load_bearing_step_class') == 'A')


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let q_L be a permutation of Z_3 = {0, 1, 2} (i.e., q_L_1, q_L_2, q_L_3
    are three distinct values mod 3), and let q_R be its pointwise
    conjugate q_R_i = -q_L_i mod 3. Let q_H ∈ Z_3.
    Define
        S(q_L, q_R, q_H) = { (i, j) : q_L_i + q_H + q_R_j ≡ 0 mod 3 }.

  CONCLUSION:
    (i)  S is a permutation pattern (one entry per row, one per column).
    (ii) The three supports S(q_L, q_R, q_H) over q_H ∈ {0, 1, 2} are
         pairwise disjoint and cover the full 3x3 grid.
    (iii) The three supports are exactly the diagonal pattern, the forward
         cyclic pattern, and the backward cyclic pattern (in some order
         determined by q_L).

  The distinct-Z_3-values hypothesis on q_L is essential: at constant
  q_L (e.g., (0, 0, 0)) the trichotomy fails (one q_H gives the full
  grid; the other two give empty supports).

  Audit-lane class:
    (A) — pure number theory / Z_3-character arithmetic. No DM-side,
    neutrino-side, Higgs-doublet, or framework-specific authority. The
    framework instance q_L = (0, +1, -1), q_R = (0, -1, +1) is one
    permutation case; the algebra closes for any conjugate pair.

  This narrow theorem drops the parent's dependencies on supplied
  generation charges, the Dirac-lane reduction, and the single Higgs
  doublet with definite Z_3 charge. Those are framework-specific
  hypotheses that this narrow theorem treats as abstract Z_3-valued
  symbols.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
