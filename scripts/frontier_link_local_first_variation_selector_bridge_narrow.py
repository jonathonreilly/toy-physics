#!/usr/bin/env python3
"""Pattern A narrow runner for
`LINK_LOCAL_FIRST_VARIATION_SELECTOR_BRIDGE_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone algebraic-substitution implication:

  GIVEN
      (i)  H_cell ~= Lambda^* span(t,x,y,z) ~= (C^2)^4 with subset-indexed
           basis |S>, S subset E = {t,x,y,z}, and Hamming-weight projector
           classes P_k = sum_{|S|=k} P_S.

      (ii) An affine-linear link-local source map
               S_link : U -> H_cell,
               U = span(u_t, u_x, u_y, u_z),
               S_link(u) = sum_a u_a J_a,
           with the one-link support property
               support(J_a) = {a}   for each a in E.

     (iii) The bridge premise
               P_A = proj_{span(image(dS_link))}.

  THEN
      (C1) P_A = P_1 = sum_{a in E} P_{{a}}                       (Boolean
           Hamming-weight-one rank-four projector class).
      (C2) P_3 != proj_{span(image(dS_link))}; i.e. the Hodge-dual rank-four
           Hamming-weight-three class is excluded as the support of dS_link
           under hypothesis (ii).

This narrow theorem treats hypotheses (ii) and (iii) as ABSTRACT INPUT
HYPOTHESES. It does NOT derive
  - the four-variable one-link source domain (the staggered-Dirac /
    Grassmann realization is an open derivation gate per
    MINIMAL_AXIOMS_2026-05-03.md);
  - the bridge premise (active primitive response = first-variation
    support), which is exactly the load-bearing premise flagged by the
    parent broad row's two prior audit verdicts;
  - any value, audit-grade status, or upstream closure of either premise.

It claims only the algebraic implication (C1)-(C2) on the explicit Boolean
event-cell algebra under (ii) and (iii).

Pattern A precedent: frontier_ckm_magnitudes_structural_counts_narrow.py.
"""

from pathlib import Path
import sys
import json
import itertools

try:
    import numpy as np
except ImportError:
    print("FAIL: numpy required for projector arithmetic")
    sys.exit(1)

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


# ============================================================================
# Setup: construct H_cell explicitly as Lambda^* span(t,x,y,z) ~= (C^2)^4
# ============================================================================

# Axis labels indexed 0..3 corresponding to (t, x, y, z).
AXES = ('t', 'x', 'y', 'z')
N_AXES = len(AXES)  # = 4
DIM = 2 ** N_AXES   # = 16

# Subsets of E = {t,x,y,z} indexed by binary masks 0..15.
# For subset S with bitmask m, basis state |S> is the standard basis vector
# e_m in C^16.

def subset_from_mask(m):
    """Return the subset S of AXES corresponding to bitmask m."""
    return tuple(AXES[i] for i in range(N_AXES) if (m >> i) & 1)


def mask_for_subset(S):
    """Return the bitmask for subset S given as a tuple of axis labels."""
    m = 0
    for ax in S:
        m |= 1 << AXES.index(ax)
    return m


def hamming_weight(m):
    """Return the Hamming weight of bitmask m."""
    return bin(m).count('1')


# Basis indexing dictionary: maps subset S to its index in the C^16 basis.
SUBSETS = [subset_from_mask(m) for m in range(DIM)]


# ----------------------------------------------------------------------------
section("Part 1: Boolean event-cell H_cell construction (16 basis states)")
# ----------------------------------------------------------------------------

# Identity on H_cell.
I = np.eye(DIM, dtype=np.float64)

# Basis projectors P_S = |S><S|.
def P_S(mask):
    P = np.zeros((DIM, DIM), dtype=np.float64)
    P[mask, mask] = 1.0
    return P

# Verify dimension and basis-state count.
check("dim(H_cell) = 16 (basis index 0..15 via subset bitmasks)",
      DIM == 16, detail=f"DIM = {DIM}")
check("16 subset-indexed basis states enumerated",
      len(SUBSETS) == 16, detail=f"len(SUBSETS) = {len(SUBSETS)}")


# ----------------------------------------------------------------------------
section("Part 2: Hamming-weight projector classes P_0, P_1, P_2, P_3, P_4")
# ----------------------------------------------------------------------------

# Build P_k = sum_{|S|=k} P_S.
P_k_dict = {}
for k in range(N_AXES + 1):
    P_k_dict[k] = sum(P_S(m) for m in range(DIM) if hamming_weight(m) == k)

# Expected ranks: binomial(4, k).
expected_ranks = {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}

for k in range(N_AXES + 1):
    Pk = P_k_dict[k]
    # Projector check: P_k = P_k^T and P_k^2 = P_k.
    is_proj = np.allclose(Pk @ Pk, Pk) and np.allclose(Pk.T, Pk)
    rank = int(np.round(np.trace(Pk)))
    check(f"P_{k} is a projector of rank C(4,{k}) = {expected_ranks[k]}",
          is_proj and rank == expected_ranks[k],
          detail=f"rank = {rank}, projector check = {is_proj}")


# ----------------------------------------------------------------------------
section("Part 3: hypothesis (ii) — four basis source images J_a with support(J_a) = {a}")
# ----------------------------------------------------------------------------

# Hypothesis (ii) says S_link : U -> H_cell, S_link(u) = sum_a u_a J_a,
# with support(J_a) = {a}. We instantiate J_a = P_{{a}} |{a}> = |{a}>.

J = {}
for ax_idx, ax in enumerate(AXES):
    # J_a is the basis vector for the one-axis subset {a}.
    one_axis_subset = (ax,)
    m = mask_for_subset(one_axis_subset)
    v = np.zeros(DIM, dtype=np.float64)
    v[m] = 1.0
    J[ax] = v
    # Verify support: J_a is nonzero only at index m corresponding to {a}.
    support = [i for i in range(DIM) if abs(v[i]) > 1e-12]
    check(f"J_{ax} support is exactly the one-axis basis state |{{{ax}}}|",
          support == [m] and hamming_weight(m) == 1,
          detail=f"support indices: {support}, mask {m} has weight {hamming_weight(m)}")


# ----------------------------------------------------------------------------
section("Part 4: differential dS_link and support projector (Step 2 of proof)")
# ----------------------------------------------------------------------------

# Step 1 of proof: dS_link(du_a) = J_a (algebraic differential, affine-linear).
# Step 2: the support projector onto span(J_t, J_x, J_y, J_z) is P_1.

# Build the matrix whose columns are the J_a's (4 columns in C^16).
J_matrix = np.column_stack([J[ax] for ax in AXES])

# Compute the orthogonal projector onto its column span.
# Since J_a are orthonormal basis vectors of the one-axis subspace, the
# orthogonal projector is J_matrix @ J_matrix.T.
P_image = J_matrix @ J_matrix.T

# Verify rank.
rank_P_image = int(np.round(np.trace(P_image)))
check("rank(proj_{span(image(dS_link))}) = 4",
      rank_P_image == 4,
      detail=f"trace = {rank_P_image}")

# Verify projector property.
check("proj_{span(image(dS_link))} is a projector (P^2 = P, P^T = P)",
      np.allclose(P_image @ P_image, P_image) and np.allclose(P_image.T, P_image))

# Verify it equals P_1.
P_1 = P_k_dict[1]
check("proj_{span(image(dS_link))} = P_1 (Boolean Hamming-weight-one projector)",
      np.allclose(P_image, P_1),
      detail=f"max abs diff = {np.max(np.abs(P_image - P_1)):.2e}")


# ----------------------------------------------------------------------------
section("Part 5: (C1) bridge premise (iii) forces P_A = P_1 = P_A")
# ----------------------------------------------------------------------------

# Under hypothesis (iii): P_A = proj_{span(image(dS_link))}.
# By Part 4, that projector is P_1. So P_A = P_1 = P_A.
# (Algebraic equality of operators on H_cell.)
P_A = P_image  # by hypothesis (iii)
check("(C1) hypothesis (iii) + Step 2 ==> P_A = P_1",
      np.allclose(P_A, P_1),
      detail=f"P_A - P_1 max abs = {np.max(np.abs(P_A - P_1)):.2e}")

# Sanity check: P_1 = sum_a P_{{a}} explicitly.
P_1_sum_of_axes = sum(P_S(mask_for_subset((ax,))) for ax in AXES)
check("P_1 = sum_{a in E} P_{{a}} (axis-additivity sanity check)",
      np.allclose(P_1, P_1_sum_of_axes))


# ----------------------------------------------------------------------------
section("Part 6: (C2) P_3 is excluded as support projector of dS_link")
# ----------------------------------------------------------------------------

P_3 = P_k_dict[3]

# Step 4 of proof: each J_a has Hamming weight 1, so is orthogonal to all
# weight-3 basis states. Hence P_3 J_a = 0 for all a, so P_3 * P_image = 0.

P_3_times_P_image = P_3 @ P_image
check("(C2) P_3 * proj_{span(image(dS_link))} = 0 (J_a orthogonal to weight-3 states)",
      np.allclose(P_3_times_P_image, np.zeros_like(P_3)),
      detail=f"max abs entry = {np.max(np.abs(P_3_times_P_image)):.2e}")

check("(C2) P_3 != proj_{span(image(dS_link))} (P_3 != P_1)",
      not np.allclose(P_3, P_image),
      detail=f"P_3 vs P_image diff max = {np.max(np.abs(P_3 - P_image)):.2e}")


# ----------------------------------------------------------------------------
section("Part 7: Step 5 — P_1 is unique rank-four Hamming-weight match")
# ----------------------------------------------------------------------------

# Rank-four projectors among Hamming-weight classes are exactly P_1 and P_3.
rank_four_classes = [k for k in range(N_AXES + 1)
                     if int(np.round(np.trace(P_k_dict[k]))) == 4]
check("exactly two rank-four Hamming-weight classes: P_1 and P_3",
      rank_four_classes == [1, 3],
      detail=f"rank-four classes = {rank_four_classes}")

# Under hypothesis (ii) + (iii), the algebraic support projector of dS_link
# is uniquely P_1 (Step 2). P_3 is excluded (Step 4). So P_1 is the unique
# rank-four Hamming-weight match.
check("P_1 is the unique rank-four Hamming-weight class consistent with (ii) and (iii)",
      np.allclose(P_image, P_1) and not np.allclose(P_image, P_3))


# ----------------------------------------------------------------------------
section("Part 8: Hodge-complement degeneracy consistency check (no-go respected)")
# ----------------------------------------------------------------------------

# The retained no-go records *: P_1 <-> P_3 as exchanges on the substrate-
# symmetry surface, but P_1 and P_3 are NOT equal as projectors on H_cell.
# This narrow theorem's Step 4 is consistent with the no-go: the source-map
# (i) is the structure that breaks the Hodge degeneracy on the source domain.
# Verify P_1 and P_3 are both rank-four but distinct projectors.

P_1_eq_P_3 = np.allclose(P_1, P_3)
check("P_1 != P_3 as projectors on H_cell (consistency with retained no-go)",
      not P_1_eq_P_3,
      detail="substrate symmetries alone cannot distinguish; (i)+(iii) does")

# P_1 and P_3 have the same rank (4) — Hodge-isomorphic in dimension.
check("rank(P_1) == rank(P_3) == 4 (Hodge-isomorphic in rank)",
      int(np.round(np.trace(P_1))) == 4 and int(np.round(np.trace(P_3))) == 4)


# ----------------------------------------------------------------------------
section("Part 9: parent broad row context (no ledger modification)")
# ----------------------------------------------------------------------------

LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent_cid = 'planck_link_local_first_variation_p_a_forcing_theorem_note_2026-04-30'
parent = ledger['rows'].get(parent_cid, {})

print(f"\n  Parent broad row state on origin/main:")
print(f"    claim_id: {parent_cid}")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    effective_status: {parent.get('effective_status')}")
print(f"    intrinsic_status: {parent.get('intrinsic_status')}")
print(f"    previous_audits count: {len(parent.get('previous_audits') or [])}")

check("parent broad row exists in audit ledger",
      bool(parent),
      detail=f"claim_type = {parent.get('claim_type')}")

check("parent broad row is positive_theorem (matches narrow rescope target)",
      parent.get('claim_type') == 'positive_theorem')

prev_audits = parent.get('previous_audits') or []
check("parent broad row carries prior audit verdicts (at least 1)",
      len(prev_audits) >= 1,
      detail=f"prior audit count = {len(prev_audits)}")

# Confirm at least one prior verdict was audited_conditional with the
# selector-bridge rationale.
selector_verdicts = [a for a in prev_audits
                     if a.get('audit_status') == 'audited_conditional']
check("at least one prior verdict is audited_conditional",
      len(selector_verdicts) >= 1,
      detail=f"audited_conditional prior verdicts = {len(selector_verdicts)}")


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESES (input, NOT derived here):
      (ii) S_link : U -> H_cell, U = span(u_t, u_x, u_y, u_z),
           S_link(u) = sum_a u_a J_a, support(J_a) = {a} for each a in E.
     (iii) P_A = proj_{span(image(dS_link))}.

  CONCLUSION (algebraic-substitution forced):
      (C1) P_A = P_1 = sum_{a in E} P_{{a}}.
      (C2) P_3 != proj_{span(image(dS_link))}; P_3 is excluded as a
           fundamental first variation of S_link under (ii).

  Audit-lane class:
    (A) — pure algebraic substitution on the explicit Boolean event-cell
    algebra H_cell ~= (C^2)^4. No external observed/fitted/literature
    input. No new axiom proposed. Hypothesis (ii) (one-link source domain)
    and hypothesis (iii) (bridge premise) are stated abstractly; their
    audit-grade derivation is the responsibility of the parent broad row
    and its upstream authorities.

  The narrow theorem drops the parent row's dependencies on
  staggered-Dirac realization / anomaly-time / CPT / observable-principle
  by stating (ii) and (iii) as input hypotheses.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
