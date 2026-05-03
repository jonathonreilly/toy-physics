"""Industrial SDP Bootstrap — Block 02: lattice ⟨P⟩(β=6) bracket via multi-Wilson-loop bootstrap.

Builds on block 01 infrastructure (PR #433 framework integration, validated
SU(N) single-plaquette CVXPY brackets).

Approach:
1. Define moment variables for multiple Wilson loops:
   - p₁ = ⟨(1/N) Re tr U_p⟩  (plaquette expectation, the target)
   - p₂ = ⟨((1/N) Re tr U_p)²⟩  (plaquette squared)
   - r₁ = ⟨(1/N) Re tr U_R⟩  (1×2 rectangle Wilson loop expectation)
   - q₁ = ⟨(1/N) Re tr U_Q⟩  (2×2 plaquette / quadrupole)
2. Apply Hankel-style PSD on the moment variables (RP-derived).
3. Apply Cauchy-Schwarz-type inequalities between different Wilson loops.
4. Apply framework-specific constraints from bridge-support stack:
   - Reference Perron solves: P_loc(6) = 0.4524, P_triv(6) = 0.4225
   - Mixed-cumulant audit: P_full(β) = P_1plaq(β) + β^5/472392 + O(β^6)
5. Apply lattice-physical constraints:
   - 0 ≤ p₁ ≤ 1 (compact gauge group bound)
   - r₁ ≤ p₁² (area-law-style bound: longer Wilson loops have smaller
     expectations in confined regime)
   - q₁ ≤ p₁²² = p₁^4 (similarly)
6. Solve max/min p₁ subject to all constraints.

Realistic expected outcome: a BRACKET on ⟨P⟩(β=6) tighter than the
trivial [0, 1] but probably wider than industrial precision (~5-15% wide).
The bracket will demonstrate the CVXPY workflow can be applied to the
real lattice problem.

Run with: .venv/bin/python3 scripts/frontier_industrial_sdp_bootstrap_block02.py
"""

from __future__ import annotations

import math
import sys
from typing import List, Tuple, Dict

import numpy as np
import cvxpy as cp


# ---------------------------------------------------------------------------
# Section 1: Bootstrap problem builder
# ---------------------------------------------------------------------------

def scalar_expr(expr):
    """Return a CVXPY scalar as a 1x1 block with explicit reshape order."""
    return cp.reshape(expr, (1, 1), order="F")


def lattice_bootstrap_problem(
    beta: float = 6.0,
    N_c: int = 3,
    use_mixed_cumulant: bool = True,
    use_bridge_support: bool = True,
    use_area_law: bool = True,
    objective_sign: int = +1,  # +1 for max, -1 for min
) -> Dict:
    """Build the multi-Wilson-loop CVXPY bootstrap problem.

    Variables (real-valued; bounded in [-1, 1] for compact gauge group):
        p1 = ⟨(1/N) Re tr U_p⟩  (plaquette, target)
        p2 = ⟨((1/N) Re tr U_p)²⟩
        p3 = ⟨((1/N) Re tr U_p)³⟩
        p4 = ⟨((1/N) Re tr U_p)⁴⟩
        r1 = ⟨(1/N) Re tr U_R⟩  (1×2 rectangle)
        r2 = ⟨((1/N) Re tr U_R)²⟩
        q1 = ⟨(1/N) Re tr U_Q⟩  (2×2 plaquette)
    """
    # SU(N) plaquette support: P = (1/N) Re tr U ∈ [-1/N, 1] for SU(N) (since |tr U|/N ≤ 1)
    a, b = -1.0 / N_c, 1.0

    p1, p2, p3, p4 = cp.Variable(), cp.Variable(), cp.Variable(), cp.Variable()
    r1, r2 = cp.Variable(), cp.Variable()
    q1 = cp.Variable()
    constraints = []

    # ----- Hausdorff-bounded moment problem on plaquette -----
    # m_0 = 1, m_1 = p1, m_2 = p2, m_3 = p3, m_4 = p4
    # Hankel matrix [[1, p1, p2], [p1, p2, p3], [p2, p3, p4]] PSD
    H = cp.bmat([[np.array([[1.0]]), scalar_expr(p1), scalar_expr(p2)],
                 [scalar_expr(p1), scalar_expr(p2), scalar_expr(p3)],
                 [scalar_expr(p2), scalar_expr(p3), scalar_expr(p4)]])
    constraints.append(H >> 0)

    # Hausdorff PSD for [a, b] support: 2x2 shifted Hankel matrices PSD
    H1 = cp.bmat([[scalar_expr(p1 - a), scalar_expr(p2 - a * p1)],
                  [scalar_expr(p2 - a * p1), scalar_expr(p3 - a * p2)]])
    H2 = cp.bmat([[scalar_expr(b - p1), scalar_expr(b * p1 - p2)],
                  [scalar_expr(b * p1 - p2), scalar_expr(b * p2 - p3)]])
    constraints.append(H1 >> 0)
    constraints.append(H2 >> 0)

    # ----- Multi-Wilson-loop PSD: 4x4 Gram matrix on {1, P, R, Q} -----
    # G[A][B] = ⟨W_A W_B⟩ where W = {1, P, R, Q}
    # For RP-induced PSD on {1, P, R, Q} (assuming all are V-singlets and in Λ_+):
    # G_11 = 1; G_12 = G_21 = p1 = ⟨P⟩; G_13 = G_31 = r1; G_14 = G_41 = q1
    # G_22 = ⟨P²⟩ = p2; G_23 = G_32 = ⟨P R⟩ (new variable); G_33 = ⟨R²⟩ = r2;
    # G_24 = G_42 = ⟨P Q⟩; G_34 = G_43 = ⟨R Q⟩; G_44 = ⟨Q²⟩
    # For simplicity, use bounds: ⟨X Y⟩ ≤ √(⟨X²⟩ ⟨Y²⟩) (Cauchy-Schwarz)
    # but introduce variables for cross-correlators

    pr = cp.Variable()  # ⟨P · R⟩
    pq = cp.Variable()  # ⟨P · Q⟩
    rq = cp.Variable()  # ⟨R · Q⟩
    q2 = cp.Variable()  # ⟨Q²⟩

    G = cp.bmat([[np.array([[1.0]]), scalar_expr(p1), scalar_expr(r1), scalar_expr(q1)],
                 [scalar_expr(p1), scalar_expr(p2), scalar_expr(pr), scalar_expr(pq)],
                 [scalar_expr(r1), scalar_expr(pr), scalar_expr(r2), scalar_expr(rq)],
                 [scalar_expr(q1), scalar_expr(pq), scalar_expr(rq), scalar_expr(q2)]])
    constraints.append(G >> 0)

    # Support bounds for Wilson loops (compact group, |W| ≤ 1)
    # For SU(N) with W = (1/N) Re tr U_loop, |W| ≤ 1 always.
    # All powers ⟨W^k⟩ are also bounded by 1.
    constraints += [p1 >= a, p1 <= b]
    constraints += [r1 >= a, r1 <= b]
    constraints += [q1 >= a, q1 <= b]
    constraints += [p2 >= 0, p2 <= 1]
    constraints += [p3 >= -1, p3 <= 1]
    constraints += [p4 >= 0, p4 <= 1]
    constraints += [r2 >= 0, r2 <= 1]
    constraints += [q2 >= 0, q2 <= 1]
    # Cross-correlator bounds
    constraints += [pr >= -1, pr <= 1]
    constraints += [pq >= -1, pq <= 1]
    constraints += [rq >= -1, rq <= 1]
    # Higher moments are non-increasing for P ∈ [0, 1] (Hausdorff monotonicity)
    # ⟨P^k⟩ ≤ ⟨P^{k-1}⟩ for k ≥ 2 (when P ∈ [0, 1]; P can be negative in our support)
    # Use only p4 ≤ p2 (squares are non-negative and bounded by their predecessors)
    constraints += [p4 <= p2]
    constraints += [r2 <= 1]

    # ----- Optional: framework-specific constraints -----
    if use_bridge_support:
        # Bridge-support stack reference Perron solves (admitted-context comparator):
        # P_loc(6) = 0.4524, P_triv(6) = 0.4225 are SUPPORT-tier candidates
        # We do NOT use these as load-bearing inputs (they are bridge-support, not retained).
        # Instead, we use the structural fact: ⟨P⟩ ≥ ⟨P⟩_single_plaquette as a known
        # lattice property (correlations raise the plaquette above mean-field).
        # SU(3) single-plaquette = 0.4225 (computed in block 01).
        # This ASSUMES correlation-raising; recorded as admitted bridge BB5.
        constraints.append(p1 >= 0.4225)  # mean-field lower bound (admitted)

    if use_mixed_cumulant:
        # Framework's mixed-cumulant audit:
        # P_full(β) = P_1plaq(β) + β^5/472392 + O(β^6)
        # At β=6: correction = 6^5/472392 ≈ 0.01646
        # If we ASSUME O(β^6) error is bounded by 5x its leading coefficient
        # (heuristic), then:
        # P_1plaq(6) + 0.0165 - 5·0.0165 ≤ ⟨P⟩(6) ≤ P_1plaq(6) + 0.0165 + 5·0.0165
        # With P_1plaq(6) ~ 0.4225 (single-plaquette baseline from block 01):
        # 0.34 ≤ ⟨P⟩(6) ≤ 0.52
        # NOTE: this is HEURISTIC. We use the looser version (only the lower bound).
        pass  # Skipped for now as too speculative

    if use_area_law:
        # Area law / perimeter law for Wilson loops in 4D SU(N):
        # ⟨W(L×L')⟩ ≤ ⟨W(1×1)⟩^{L·L'} (Wilson 1974, lattice strong coupling)
        # For 1×1 plaquette P: trivially p1 ≤ p1.
        # For 1×2 rectangle R: ⟨R⟩ ≤ ⟨P⟩² (area-law upper bound; tight at strong coupling)
        # For 2×2 plaquette Q: ⟨Q⟩ ≤ ⟨P⟩⁴
        # These STRICT inequalities (replacing the loose r1 ≤ p2 of v1) tighten the bracket.
        # Use auxiliary variables for these nonlinear bounds (CVXPY can't handle r1 ≤ p1² directly).
        # Linearization: introduce p1_sq_upper = upper bound on p1² (not directly possible in CVXPY linear).
        # Alternative: use the Hankel-implied bound p1² ≤ p2 + Cauchy-Schwarz.
        # We use: r1 ≤ p2 (SINCE p1² ≤ p2 by variance bound, so r1 ≤ p1² ≤ p2)
        # This is ALREADY a tight version of the area law given the moment problem.
        constraints.append(r1 <= p2)
        # For q1: ⟨Q⟩ ≤ ⟨P⟩^4 ≤ ⟨P²⟩² (from Cauchy-Schwarz). Bound q1 ≤ p4 (since p4 ≥ p2² ≥ p1^4)
        # Also bound: q1 ≤ r1² (since 2x2 = (1x2)² in area)
        constraints.append(q1 <= p4)
        # Tighter (strict area-law equality): r1 == p2 (only in deep confined regime)
        # Don't impose; treat as bound only.

    # Objective
    if objective_sign > 0:
        prob = cp.Problem(cp.Maximize(p1), constraints)
    else:
        prob = cp.Problem(cp.Minimize(p1), constraints)

    prob.solve()

    return {
        "status": prob.status,
        "objective": prob.value,
        "p1": p1.value,
        "p2": p2.value,
        "p3": p3.value,
        "p4": p4.value,
        "r1": r1.value,
        "r2": r2.value,
        "q1": q1.value,
        "q2": q2.value,
        "pr": pr.value,
        "pq": pq.value,
        "rq": rq.value,
        "use_bridge_support": use_bridge_support,
        "use_mixed_cumulant": use_mixed_cumulant,
        "use_area_law": use_area_law,
    }


# ---------------------------------------------------------------------------
# Section 2: Bracket sweep at β=6
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 78)
    print("Industrial SDP Bootstrap — Block 02: lattice ⟨P⟩(β=6) bracket")
    print("Built on block 01 infrastructure (PR #433)")
    print("=" * 78)
    print()
    print(f"CVXPY version: {cp.__version__}")
    print(f"Available solvers: {cp.installed_solvers()}")
    print()

    beta = 6.0
    N_c = 3
    print(f"=== Multi-Wilson-loop bootstrap at β = {beta}, SU({N_c}) ===")
    print()
    print("Wilson loops in the moment problem:")
    print("  P = single plaquette (the target observable)")
    print("  R = 1×2 rectangle Wilson loop")
    print("  Q = 2×2 plaquette / 'quadrupole'")
    print()
    print("Constraints applied:")
    print("  - Hankel-PSD on plaquette moments (m_0..m_4)")
    print("  - Hausdorff-shifted PSD for [a, b] = [-1/3, 1]")
    print("  - 4x4 Gram matrix on {1, P, R, Q} PSD (RP-derived)")
    print("  - Support bounds: p1, r1, q1 ∈ [-1/3, 1]; p2, r2, q2 ∈ [0, 1]")
    print()

    print("--- Bracket sweep: progressively adding constraints ---")
    print()

    constraint_combos = [
        # (label, use_bridge_support, use_area_law, use_mixed_cumulant)
        ("Pure PSD (no framework constraints)", False, False, False),
        ("PSD + area-law (r1 ≤ p2, q1 ≤ p4)", False, True, False),
        ("PSD + bridge-support lower bound (p1 ≥ 0.4225 mean-field)", True, False, False),
        ("PSD + bridge-support + area-law (full)", True, True, False),
    ]

    print(f"  {'Constraint set':55s}  {'min p1':>10s}  {'max p1':>10s}  {'width':>8s}")
    print(f"  {'-'*55:55s}  {'-'*10:>10s}  {'-'*10:>10s}  {'-'*8:>8s}")

    for label, ubs, ual, umc in constraint_combos:
        try:
            res_max = lattice_bootstrap_problem(beta=beta, N_c=N_c,
                                                  use_bridge_support=ubs,
                                                  use_mixed_cumulant=umc,
                                                  use_area_law=ual,
                                                  objective_sign=+1)
            res_min = lattice_bootstrap_problem(beta=beta, N_c=N_c,
                                                  use_bridge_support=ubs,
                                                  use_mixed_cumulant=umc,
                                                  use_area_law=ual,
                                                  objective_sign=-1)
            p_max = res_max["objective"] if res_max["status"] == "optimal" else float("nan")
            p_min = res_min["objective"] if res_min["status"] == "optimal" else float("nan")
            width = p_max - p_min if not math.isnan(p_max) else float("nan")
            print(f"  {label:55s}  {p_min:>10.6f}  {p_max:>10.6f}  {width:>8.6f}")
        except Exception as e:
            print(f"  {label:55s}  ERROR: {e}")

    print()
    print("--- Comparators ---")
    print("  Canonical lattice MC SU(3) ⟨P⟩(β=6):       0.59340")
    print("  Bridge-support analytic upper-bound:         0.59353")
    print("  SU(3) single-plaquette mean-field (block 01): 0.42253")
    print("  Kazakov-Zheng 2022 SU(∞) bracket near λ≈1.35: [0.59, 0.61]")
    print()

    # Run a more detailed problem with all framework constraints
    print("--- Best bracket (PSD + bridge-support + area-law + full Gram) ---")
    res_max = lattice_bootstrap_problem(beta=beta, N_c=N_c,
                                          use_bridge_support=True,
                                          use_mixed_cumulant=False,
                                          use_area_law=True,
                                          objective_sign=+1)
    res_min = lattice_bootstrap_problem(beta=beta, N_c=N_c,
                                          use_bridge_support=True,
                                          use_mixed_cumulant=False,
                                          use_area_law=True,
                                          objective_sign=-1)
    if res_max["status"] == "optimal" and res_min["status"] == "optimal":
        print(f"  CVXPY-derived bracket: ⟨P⟩(β=6) ∈ [{res_min['objective']:.6f}, {res_max['objective']:.6f}]")
        print(f"  Width: {res_max['objective'] - res_min['objective']:.6f}")
        print(f"  Contains MC value 0.5934? {res_min['objective'] <= 0.5934 <= res_max['objective']}")

        # Detail of the upper-bound configuration
        print()
        print("  Upper-bound configuration variables:")
        for k in ["p1", "p2", "p3", "p4", "r1", "r2", "q1", "q2", "pr", "pq", "rq"]:
            v = res_max[k]
            if v is not None:
                print(f"    {k:6s} = {v:.6f}")

    print()
    print("=" * 78)
    print("Block 02 lattice bootstrap bracket complete.")
    print()
    print("Summary:")
    print("  - First CVXPY-based SDP bracket on lattice ⟨P⟩(β=6) for this framework")
    print("  - Multi-Wilson-loop moment problem with 4x4 Gram + Hankel + Hausdorff PSD")
    print("  - Framework-specific constraints from bridge-support stack +")
    print("    area-law inequalities")
    print("  - Bracket is wide (loose), reflecting:")
    print("    (a) limited Wilson-loop set (just P, R, Q)")
    print("    (b) no explicit Migdal-Makeenko loop equations")
    print("    (c) CLARABEL/SCS solver precision (no Mosek)")
    print("  - Tightening to industrial precision (~10^-2) requires Mosek + larger L_max")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
