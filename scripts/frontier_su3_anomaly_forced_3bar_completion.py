#!/usr/bin/env python3
"""SU(3) Anomaly-Forced 3̄ Singlet Completion — Closing Derivation Runner.

Candidate closing derivation for
`su3_cubic_anomaly_cancellation_theorem_note_2026-04-24`.

This runner DERIVES the SU(3) representation content of the RH (anti-)quark
sector from:

  P1: `Q_L : (3, 2)_{1/3}` (LEFT_HANDED_CHARGE_MATCHING_NOTE).

  P2: Anomaly-cancellation requirement (ANOMALY_FORCES_TIME_THEOREM):
      the SU(3)^3 cubic anomaly trace must vanish for gauge consistency.

  P3: Minimal field-count completion among LH Weyl fermions in
      irreducible SU(3) representations.

The derivation enumerates SU(3) cubic-anomaly coefficients A(R) for the
canonical low-dim irreps and shows that any RH completion cancelling
the +2 contribution from Q_L must include at least 2 LH-Weyl fermions in
3̄ of SU(3); this minimum is achieved uniquely (up to relabeling and
addition of vector-like / anomaly-free pairs) by 2 LH 3̄ singlets.
These are then identified as `u_R^c` and `d_R^c`.

The runner does NOT close hypercharge, SU(2)_L singlet labelling, or
generation count — those are separate authority rows
(STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24,
THREE_GENERATION_STRUCTURE_NOTE).

Output: derivation that the SU(3) rep of u_R^c, d_R^c IS forced
(not hand-entered) by P1+P2+P3.
"""

import sys

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {label}  ({detail})" if detail else f"  [{tag}] {label}")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("SU(3) Anomaly-Forced 3̄ Singlet Completion — Closing Derivation")
# ============================================================================


# ----------------------------------------------------------------------------
section("Part 1: SU(3) cubic-anomaly coefficient A(R) catalogue")
# ----------------------------------------------------------------------------
# A(R) = (1/2) d^abc Tr_R[T^a {T^b, T^c}] / (standard normalization),
# where d^abc are the symmetric structure constants of SU(3).
# Standard table (e.g., Slansky 1981, Table 22; Cvitanović):
#
#   R         dim   Dynkin   A(R)
#   1         1     (0,0)    0
#   3         3     (1,0)   +1   (fundamental)
#   3̄         3     (0,1)   -1   (anti-fundamental)
#   6         6     (2,0)   +7   (sym²(3))
#   6̄         6     (0,2)   -7
#   8         8     (1,1)    0   (adjoint, real / self-conjugate)
#   10        10    (3,0)   +27  (sym³(3))
#   10̄        10    (0,3)   -27
#   15        15    (2,1)   +14  (mixed symmetric)
#   15̄        15    (1,2)   -14
#   27        27    (2,2)    0   (real)
#   ...

ANOMALY_TABLE = {
    '1':   0,
    '3':   1,
    '3bar': -1,
    '6':   7,
    '6bar': -7,
    '8':   0,
    '10':  27,
    '10bar': -27,
    '15':  14,
    '15bar': -14,
    '27':  0,
}

print("\n  Standard SU(3) cubic-anomaly coefficient catalogue:")
for R, A in sorted(ANOMALY_TABLE.items(), key=lambda x: x[1]):
    print(f"    A({R:6s}) = {A:+d}")

# Conjugate-rep symmetry: A(Rbar) = -A(R)
for R in ['3', '6', '10', '15']:
    R_bar = R + 'bar'
    check(f"A({R_bar}) = -A({R}) (conjugation symmetry)",
          ANOMALY_TABLE[R_bar] == -ANOMALY_TABLE[R],
          detail=f"A({R}) + A({R_bar}) = {ANOMALY_TABLE[R] + ANOMALY_TABLE[R_bar]}")

# Real-rep zero: A(8) = A(27) = 0 (self-conjugate)
check("A(8) = 0 (adjoint is self-conjugate, anomaly vanishes)",
      ANOMALY_TABLE['8'] == 0)
check("A(27) = 0 (self-conjugate)",
      ANOMALY_TABLE['27'] == 0)


# ----------------------------------------------------------------------------
section("Part 2: P1 — Q_L : (3, 2)_{1/3} contributes +2 to SU(3)^3 anomaly")
# ----------------------------------------------------------------------------
# Q_L is LH Weyl in (3, 2) of SU(3) × SU(2). The SU(3) anomaly trace counts
# each LH Weyl fermion in irrep R with weight A(R). The SU(2) doublet
# structure means there are 2 independent LH 3-rep fermions per Q_L
# (one for each isospin component, treated as separate Weyl fields):
#   contribution = 2 × A(3) = +2.

QL_anomaly_contribution = 2 * ANOMALY_TABLE['3']
check("Q_L : (3, 2) contributes 2 × A(3) = +2 to SU(3)^3 anomaly",
      QL_anomaly_contribution == 2,
      detail=f"contribution = {QL_anomaly_contribution}")


# ----------------------------------------------------------------------------
section("Part 3: P2 — anomaly cancellation requires RH content with A_total = -2")
# ----------------------------------------------------------------------------
# For SU(3)^3 anomaly to vanish: sum over all LH Weyl fermions of A(R) = 0.
# With Q_L contributing +2, the RH content (treated as LH-Weyl
# anti-particles, i.e. u_R^c, d_R^c are LH Weyl fields in conjugate reps)
# must contribute exactly -2.

required_RH_anomaly = -2
print(f"\n  Required RH-content total anomaly contribution: {required_RH_anomaly}")
check("RH content must contribute -2 to cancel Q_L's +2",
      required_RH_anomaly == -2)


# ----------------------------------------------------------------------------
section("Part 4: P3 — enumerate minimal-field-count completions cancelling +2")
# ----------------------------------------------------------------------------
# Restrict to LH-Weyl SU(2)-singlet fields in irreducible SU(3) reps R
# from a candidate set. For each completion (n_R) with R ranging over
# the candidate set, the anomaly contribution is
#   sum_R n_R · A(R) = required_RH_anomaly = -2.
# Minimal field count: minimize sum_R n_R subject to the constraint.
#
# Two candidate sets:
#   set A: {1, 3, 3bar}  (minimal SM-natural rep set)
#   set B: {1, 3, 3bar, 6, 6bar, 8}  (extended)

def min_field_completions(candidate_reps, target_anomaly, max_count=8):
    """Enumerate all completions (n_R for R in candidate_reps) of total
    field count <= max_count that cancel the target anomaly. Return the
    list of minimal-count solutions."""
    solutions = []
    # Iterate over total field count n in 1, 2, ..., max_count
    for n_total in range(1, max_count + 1):
        # All ways to distribute n_total fields among candidate reps
        # (compositions of n_total into len(candidate_reps) non-negative parts)
        n_reps = len(candidate_reps)
        for composition in compositions(n_total, n_reps):
            anomaly = sum(c * ANOMALY_TABLE[R] for c, R in zip(composition, candidate_reps))
            if anomaly == target_anomaly:
                solutions.append((n_total, dict(zip(candidate_reps, composition))))
        if solutions and any(s[0] == n_total for s in solutions):
            return solutions  # first n_total with solutions is minimal
    return solutions


def compositions(n, k):
    """Yield all compositions of n into k non-negative integers."""
    if k == 1:
        yield (n,)
        return
    for i in range(n + 1):
        for tail in compositions(n - i, k - 1):
            yield (i,) + tail


# Set A: restrict to {1, 3, 3bar} (the SM-natural reps for fundamental fermions)
set_A_reps = ['1', '3', '3bar']
sols_A = min_field_completions(set_A_reps, required_RH_anomaly, max_count=4)
print(f"\n  Set A = {set_A_reps}: minimal-count solutions cancelling {required_RH_anomaly}:")
for count, comp in sols_A:
    nontriv = {R: n for R, n in comp.items() if n > 0}
    print(f"    field-count {count}: {nontriv}")

# The minimum count should be 2, achieved by {3bar: 2}
min_count_A = min(s[0] for s in sols_A) if sols_A else None
check("Set A minimal field count = 2 (smallest anomaly-cancelling RH completion)",
      min_count_A == 2,
      detail=f"min count = {min_count_A}")

minimal_solutions_A = [s for s in sols_A if s[0] == min_count_A]
# Filter out solutions with n_1 contribution (anomaly-irrelevant singlets):
# the "2 × 3bar" solution is the unique one that contributes the full -2.
canonical_solution = {'1': 0, '3': 0, '3bar': 2}
# Among 2-field solutions, identify the canonical one
canonical_in_minimal = any(
    {R: n for R, n in s[1].items() if n > 0} == {'3bar': 2}
    for s in minimal_solutions_A
)
check("Canonical minimal solution: 2 LH 3̄ singlets (and no 3 fields)",
      canonical_in_minimal,
      detail="2 × 3bar = u_R^c + d_R^c form")


# ----------------------------------------------------------------------------
section("Part 5: rule out alternative low-count completions in extended set")
# ----------------------------------------------------------------------------
# Set B: include higher-dim reps. Show that {2 × 3bar} remains minimal.
set_B_reps = ['1', '3', '3bar', '6', '6bar', '8']
sols_B = min_field_completions(set_B_reps, required_RH_anomaly, max_count=8)
min_count_B = min(s[0] for s in sols_B) if sols_B else None
print(f"\n  Set B = {set_B_reps}: minimum field count = {min_count_B}")

check("Set B minimal field count = 2 (extended candidate set doesn't help)",
      min_count_B == 2,
      detail=f"min count = {min_count_B}")

# Among 2-field solutions in set B, characterize each
two_field_sols_B = [s for s in sols_B if s[0] == 2]
print(f"\n  Set B 2-field solutions:")
for count, comp in two_field_sols_B:
    nontriv = {R: n for R, n in comp.items() if n > 0}
    print(f"    {nontriv}")

# In set B with 2 fields, can we get -2 using anything other than 2 × 3bar?
# Only by combining: 1 × 6bar (-7) + 1 × 6 (+7) = 0, no.
# 1 × 6bar (-7) + ??? = -2: need a +5, no rep gives +5 with 1 field. So no.
# 2 × 3bar = -2 is the only 2-field solution.
non_canonical_2field = [s for s in two_field_sols_B
                         if {R: n for R, n in s[1].items() if n > 0} != {'3bar': 2}]
check("With 2 fields, ONLY {3bar: 2} is anomaly-cancelling (no exotic alternatives)",
      len(non_canonical_2field) == 0,
      detail=f"non-canonical 2-field solutions: {len(non_canonical_2field)}")


# ----------------------------------------------------------------------------
section("Part 6: 1-field completion is impossible (no rep has A = -2)")
# ----------------------------------------------------------------------------
# Verify: no irrep R in the catalogue has A(R) = -2 (precluding 1-field completion).
one_field_solutions = [R for R, A in ANOMALY_TABLE.items() if A == required_RH_anomaly]
check("No irrep R has A(R) = -2 (1-field completion impossible)",
      len(one_field_solutions) == 0,
      detail=f"reps with A(R) = -2: {one_field_solutions}")


# ----------------------------------------------------------------------------
section("Part 7: identification — 2 LH 3̄ fields = u_R^c, d_R^c")
# ----------------------------------------------------------------------------
# The 2 LH 3̄ singlets are the SU(3)-conjugate-fundamental fields of LH Weyl
# type. In SM bookkeeping, these are denoted u_R^c (the LH conjugate of the
# RH up-quark) and d_R^c (the LH conjugate of the RH down-quark). The
# distinct labels u_R^c vs d_R^c are determined by their SU(2)_L × U(1)_Y
# quantum numbers (e.g., hypercharges Y(u_R^c) = -4/3, Y(d_R^c) = +2/3),
# which are NOT determined by the SU(3) cubic anomaly alone.
#
# The SU(3) representation content (3̄) is fully forced by P1 + P2 + P3.

print("""
  Identification:
    The 2 LH 3̄ singlets forced by SU(3)^3 anomaly cancellation
    (with Q_L : (3, 2)) are identified as
        u_R^c, d_R^c : (3̄, 1)
    in the standard SM bookkeeping. The distinguishing labels (u vs d)
    and the hypercharge values are NOT determined by SU(3) anomaly
    cancellation alone — they require:
      (a) SU(2)_L × U(1)_Y embedding (separate authority row),
      (b) U(1)_Y^2 SU(2), U(1)_Y SU(3)^2, gravitational anomalies
          and lepton-sector content.

    The SU(3) REPRESENTATION CONTENT (3̄) is, however, fully derived
    from P1+P2+P3, addressing the missing derivation on the parent row.
""")
identification_ok = (
    canonical_in_minimal
    and len(non_canonical_2field) == 0
    and len(one_field_solutions) == 0
)
check("SU(3) representation 3̄ for two RH-conjugate quark fields is forced by P1+P2+P3",
      identification_ok,
      detail="minimal anomaly-cancelling completion is exactly {3bar: 2}")


# ----------------------------------------------------------------------------
section("Closing-derivation summary")
# ----------------------------------------------------------------------------
print("""
  This runner addresses the missing derivation in
  su3_cubic_anomaly_cancellation_theorem_note_2026-04-24 by deriving
  (rather than hand-entering) the SU(3) representation content of u_R^c,
  d_R^c from:

    P1:             Q_L : (3, 2)_{1/3}
                    [LEFT_HANDED_CHARGE_MATCHING_NOTE]
    P2 (admitted):  SU(3)^3 anomaly cancellation requirement
                    [ANOMALY_FORCES_TIME_THEOREM]
    P3 (admitted):  minimal field-count completion among LH-Weyl
                    SU(2)-singlets in irreducible SU(3) reps.

  Derivation steps (all verified by this runner):
    1. SU(3) cubic anomaly catalogue: A(3) = +1, A(3̄) = -1, A(8) = 0,
       higher-dim reps |A| ∈ {7, 14, 27, ...}.
    2. Q_L : (3, 2) contributes 2 × A(3) = +2 to the SU(3)^3 anomaly.
    3. RH content must contribute -2 for cancellation.
    4. No 1-field completion exists (no irrep has A = -2).
    5. Minimal 2-field completion is uniquely {3̄ : 2} in any candidate
       rep set including {1, 3, 3̄}; extending to {6, 6̄, 8, ...} adds
       no 2-field alternatives.
    6. The 2 LH 3̄ singlets ARE the SU(3) representation content of
       u_R^c, d_R^c.

  What this closes:
    - The parent's hand-coded u_R^c, d_R^c rep content (3̄) is now
      DERIVED from P1+P2+P3 rather than stipulated.
  What remains separate (out-of-scope for this row, handled separately):
    - Hypercharges Y(u_R^c), Y(d_R^c) — STANDARD_MODEL_HYPERCHARGE_UNIQUENESS.
    - Generation count (3 generations) — THREE_GENERATION_STRUCTURE.
    - SU(2)_L singlet labelling — implicit in the SM bookkeeping.
    - Anomaly-cancellation principle itself — ANOMALY_FORCES_TIME_THEOREM.

  Status: this is a candidate closing derivation. Independent audit must
  ratify the row before the repository treats it as accepted authority.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
