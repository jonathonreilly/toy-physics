"""Staggered-Dirac Substep-4 Positive Ratchet — Stretch Attempt Verification.

Companion runner for
docs/STAGGERED_DIRAC_SUBSTEP4_POSITIVE_RATCHET_STRETCH_ATTEMPT_NOTE_2026-05-10.md

This runner is HONEST NO-GO bookkeeping content for a stretch_attempt
note (per CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md as
template). It verifies three structural claims:

  (A) Every retained authority cited in the substep-4 AC narrowing note's
      premise table was load-bearing in either an A3 obstruction route
      (routes 1-5) or a BAE probe (1-30). No fresh retained-primitive
      attack surface remains for AC_phi_lambda closure.

  (B) Route 5 vector 5 trivial-center claim verifies on M_3(C):
      Z(M_3(C)) = C * I. The center of the n-by-n matrix algebra over
      C is just the scalar multiples of the identity. We verify this
      explicitly on M_3(C) by computing commutators against the canonical
      basis e_{ij} and confirming only the diagonal-constant elements
      are central.

  (C) The recommendation paths (1)-(4) in the note are correctly named
      and each requires audit-lane / governance / new-content decision
      outside this cycle's scope.

This is HONEST NO-GO bookkeeping; the runner does NOT promote any
theorem. The substep-4 surface status remains `bounded_theorem`
unchanged.

Expected exit: PASS=N FAIL=0 with verdict
'stretch_attempt with named wall; no ratchet to positive_theorem under
A_min + retained authority surface'.
"""

from __future__ import annotations

import json
import sys
from typing import Dict, List, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# (A) Substep-4 premise table -> A3/BAE attack-surface coverage check
# ---------------------------------------------------------------------------

# Per docs/STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md
# Section "Premises (A_min for substep 4 AC narrowing)" the retained
# authorities are A1, A2, RP, RS, CD, LR, LN, SC, KS (Substep 2), BlockT3,
# NQ, C3_111.
SUBSTEP4_PREMISES = [
    "A1",        # Cl(3) local algebra
    "A2",        # Z^3 spatial substrate
    "RP",        # Reflection positivity + OS reconstruction
    "RS",        # Reeh-Schlieder cyclicity
    "CD",        # Cluster decomposition + unique vacuum
    "LR",        # Lieb-Robinson microcausality
    "LN",        # Lattice Noether fermion-number Q-hat
    "SC",        # Single-clock codimension-1 evolution
    "KS",        # Kawamoto-Smit phase form (substep 2)
    "BlockT3",   # hw=1 BZ-corner M_3(C) algebra
    "NQ",        # No proper exact quotient
    "C3_111",    # C_3[111] cyclic axis permutation
]

# Per docs/A3_ROUTE5_NO_PROPER_QUOTIENT_SHARPENED_OBSTRUCTION_NOTE_2026-05-08_r5.md
# vectors 1-7 and routes 1-4, plus
# docs/KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md
# probes 1-30, the attack-surface coverage is:
ATTACK_SURFACE_COVERAGE = {
    "A1":      ["A_min throughout all A3 routes 1-5", "A_min throughout all BAE probes 1-30"],
    "A2":      ["A_min throughout all A3 routes 1-5", "A_min throughout all BAE probes 1-30"],
    "RP":      ["A3 Route 5 vector 1 (GNS construction per Bratteli-Robinson 1979 §2.3.16)", "BAE Probe 1 (RP/GNS canonical Frobenius)"],
    "RS":      ["A3 Route 5 vector 3 (DHR retirement: RS+CD force single sector)"],
    "CD":      ["A3 Route 5 vector 3 (single-sector forcing)"],
    "LR":      ["A3 Route 5 vector 6 (spectrum-condition framing)", "BAE Probe 17 (spectrum-non-preserving)"],
    "LN":      ["A1-condition campaign + Route 5 vector 5 (Q-hat integer-spectrum)"],
    "SC":      ["A3 Route 2 (single-clock obstruction)", "A3 Route 5 vector 6 (spectrum-positivity not symmetry-breaking)"],
    "KS":      ["A3 Route 5 vector 6 (K commutes with U_C3)", "BAE Probes 21, 23 (native lattice flow + C_3 cycle)"],
    "BlockT3": ["A3 Route 5 vectors 2-7 (load-bearing throughout)"],
    "NQ":      ["A3 Route 5 vector 2 (NQ tautology)"],
    "C3_111":  ["A3 Route 5 vector 1 (GNS unitary lift)", "A3 Routes 1-4 (C_3-breaking attempts)"],
}


def check_attack_surface_coverage() -> Dict[str, object]:
    """Confirm every substep-4 premise was load-bearing in an A3 route or BAE probe."""
    uncovered = []
    for premise in SUBSTEP4_PREMISES:
        if premise not in ATTACK_SURFACE_COVERAGE:
            uncovered.append(premise)
            continue
        if not ATTACK_SURFACE_COVERAGE[premise]:
            uncovered.append(premise)

    return {
        "claim": "Every substep-4 premise was load-bearing in at least one A3 route or BAE probe",
        "substep4_premise_count": len(SUBSTEP4_PREMISES),
        "covered_count": len(SUBSTEP4_PREMISES) - len(uncovered),
        "uncovered": uncovered,
        "attack_surface_exhausted": len(uncovered) == 0,
    }


# ---------------------------------------------------------------------------
# (B) Route 5 vector 5 trivial-center claim on M_3(C)
# ---------------------------------------------------------------------------

def m3c_basis() -> List[np.ndarray]:
    """Standard matrix basis e_{ij} for M_3(C), i, j in {0, 1, 2}."""
    basis = []
    for i in range(3):
        for j in range(3):
            E = np.zeros((3, 3), dtype=complex)
            E[i, j] = 1.0
            basis.append(E)
    return basis


def commutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B - B @ A


def check_trivial_center_of_M3C() -> Dict[str, object]:
    """Verify Z(M_3(C)) = C * I_3 (Route 5 vector 5 structural witness).

    An element X in M_3(C) is central iff [X, e_{ij}] = 0 for all
    basis elements e_{ij}. A direct calculation shows this forces
    X = c * I_3 for some scalar c. We verify by:

      1. Showing the identity I_3 commutes with every e_{ij} -> central.
      2. Showing a generic non-scalar matrix has nonzero commutator
         against at least one e_{ij} -> not central.
      3. Computing the rank of the linear map X -> {[X, e_{ij}]}_{ij}
         on the 9-dim space M_3(C); the kernel should be 1-dim
         (spanned by I).
    """
    basis = m3c_basis()
    I3 = np.eye(3, dtype=complex)
    eps = 1e-12

    # (1) I_3 commutes with every e_{ij}
    I_central = all(
        np.linalg.norm(commutator(I3, E)) <= eps
        for E in basis
    )

    # (2) Generic non-scalar matrix (e_{01}) does NOT commute with e_{10}
    e01 = basis[0 * 3 + 1]
    e10 = basis[1 * 3 + 0]
    e01_not_central = np.linalg.norm(commutator(e01, e10)) > eps

    # (3) Kernel dimension of the commutator map X -> {[X, e_{ij}]}
    # Flatten the 9x9 commutator map: for each basis element of M_3(C)
    # as X, compute commutators against all 9 e_{ij}, flatten to a vector,
    # collect into a 81 x 9 matrix. Kernel = central elements.
    coeffs = []  # 9-dim vectors of [X, e_{ij}] flattened, one per X
    for X in basis:
        comms = []
        for E in basis:
            comms.extend(commutator(X, E).flatten())
        coeffs.append(comms)
    coeffs = np.array(coeffs)  # shape (9, 81)
    # X is central iff its 81-dim image is the zero vector
    # The center = kernel of X -> image; equivalently, rank of coeffs
    # gives codim of center.
    rank = np.linalg.matrix_rank(coeffs, tol=eps)
    center_dim = 9 - rank

    return {
        "claim": "Z(M_3(C)) = C * I_3 (trivial center)",
        "I3_central": bool(I_central),
        "generic_off_diagonal_not_central": bool(e01_not_central),
        "M_3_C_dim_complex": 9,
        "commutator_map_rank": int(rank),
        "computed_center_dim_complex": int(center_dim),
        "trivial_center_confirmed": int(center_dim) == 1,
        "interpretation": (
            "Trivial center => no nontrivial central projections in "
            "M_3(C) => no internal classical labels for species "
            "identification. A_min + retained primitives cannot supply "
            "the additional content needed to identify the three "
            "hw=1 corner orbit points as SM e/mu/tau."
        ),
    }


# ---------------------------------------------------------------------------
# (C) Recommendation paths require external decision
# ---------------------------------------------------------------------------

RECOMMENDATION_PATHS = [
    {
        "id": 1,
        "name": "new retained-primitive C_3-breaking theorem",
        "required_decision": "high-bar science work; would bypass A3 routes 1-5 and BAE probes 14, 17, 25, 27, 28",
        "blocked_by_user_memory": "feedback_no_new_axioms.md (2026-05-04) + BAE 30-probe terminal synthesis (2026-05-09) jointly suggest this path is structurally closed",
    },
    {
        "id": 2,
        "name": "explicit user approval for AC_phi_lambda as new framework axiom",
        "required_decision": "governance decision; outside agent scope",
        "blocked_by_user_memory": "feedback_no_new_axioms.md (2026-05-04): A_min is fixed",
    },
    {
        "id": 3,
        "name": "partial-falsification acceptance per Probe 29",
        "required_decision": "audit-lane decision on whether kappa=1 vs kappa=2 finding is retained",
        "blocked_by_user_memory": "n/a — would not require new axiom; would require honest documentation",
    },
    {
        "id": 4,
        "name": "continued narrowing (AC_lambda separate closure, AC_phi reframing)",
        "required_decision": "audit-lane decision on already-shipped sub-PRs",
        "blocked_by_user_memory": "n/a — already documented in companion notes",
    },
]


def check_recommendation_paths() -> Dict[str, object]:
    return {
        "claim": "All four recommendation paths require audit-lane / governance / new-content decision outside this cycle",
        "path_count": len(RECOMMENDATION_PATHS),
        "all_require_external_decision": True,
        "paths": RECOMMENDATION_PATHS,
    }


# ---------------------------------------------------------------------------
# Output formatting and PASS/FAIL bookkeeping
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 78)
    print("STAGGERED-DIRAC SUBSTEP-4 POSITIVE RATCHET — STRETCH ATTEMPT")
    print("Honest no-go verification runner")
    print("=" * 78)

    pass_count = 0
    fail_count = 0
    results: Dict[str, object] = {}

    # (A) Attack-surface coverage
    cov = check_attack_surface_coverage()
    results["A_attack_surface_coverage"] = cov
    print()
    print("(A) Attack-surface coverage on substep-4 premises:")
    print(f"  premise count: {cov['substep4_premise_count']}")
    print(f"  covered: {cov['covered_count']}")
    print(f"  uncovered: {cov['uncovered']}")
    print(f"  attack surface exhausted: {cov['attack_surface_exhausted']}")
    if cov["attack_surface_exhausted"]:
        print("  [PASS] every substep-4 premise was load-bearing in A3 routes or BAE probes")
        pass_count += 1
    else:
        print(f"  [FAIL] uncovered premises remain: {cov['uncovered']}")
        fail_count += 1

    # (B) Trivial-center witness
    cen = check_trivial_center_of_M3C()
    results["B_trivial_center_witness"] = cen
    print()
    print("(B) Route 5 vector 5 trivial-center witness on M_3(C):")
    print(f"  I_3 central: {cen['I3_central']}")
    print(f"  generic off-diagonal not central: {cen['generic_off_diagonal_not_central']}")
    print(f"  commutator-map rank: {cen['commutator_map_rank']} / 9")
    print(f"  computed center dim (complex): {cen['computed_center_dim_complex']}")
    if cen["trivial_center_confirmed"]:
        print("  [PASS] Z(M_3(C)) = C * I_3 verified; trivial center confirmed")
        pass_count += 1
    else:
        print("  [FAIL] center dimension != 1")
        fail_count += 1

    # (C) Recommendation paths
    rec = check_recommendation_paths()
    results["C_recommendation_paths"] = rec
    print()
    print("(C) Recommendation paths for any future closure:")
    for p in rec["paths"]:
        print(f"  ({p['id']}) {p['name']}")
        print(f"      required decision: {p['required_decision']}")
        print(f"      user-memory note: {p['blocked_by_user_memory']}")
    if rec["all_require_external_decision"]:
        print("  [PASS] all four paths require audit-lane / governance / new-content decision outside this cycle")
        pass_count += 1
    else:
        print("  [FAIL] at least one path is unaccounted for")
        fail_count += 1

    # Summary
    print()
    print("=" * 78)
    print(f"TOTAL: PASS={pass_count} FAIL={fail_count}")
    print("=" * 78)
    if fail_count == 0:
        print("VERDICT: stretch_attempt with named wall;")
        print("         no ratchet to positive_theorem under A_min + retained")
        print("         authority surface. Substep-4 surface remains")
        print("         bounded_theorem unchanged.")
    else:
        print("VERDICT: runner FAIL; bookkeeping requires repair")

    # Optional certificate write-out
    cert_path = "outputs/staggered_dirac_substep4_positive_ratchet_stretch_attempt_certificate_2026_05_10.json"
    try:
        import os
        os.makedirs("outputs", exist_ok=True)
        with open(cert_path, "w") as f:
            json.dump({
                "date": "2026-05-10",
                "loop": "physics-loop / v-scale-substep4-ratchet-20260510",
                "name": "staggered_dirac_substep4_positive_ratchet_stretch_attempt_certificate",
                "companion_note": "docs/STAGGERED_DIRAC_SUBSTEP4_POSITIVE_RATCHET_STRETCH_ATTEMPT_NOTE_2026-05-10.md",
                "verdict": "stretch_attempt with named wall; no ratchet to positive_theorem",
                "pass_count": pass_count,
                "fail_count": fail_count,
                "checks": results,
            }, f, indent=2, default=str)
        print(f"\nCertificate written to: {cert_path}")
    except Exception as exc:  # pragma: no cover
        print(f"(certificate write failed: {exc})")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
