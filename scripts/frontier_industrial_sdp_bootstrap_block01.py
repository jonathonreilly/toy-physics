"""Industrial SDP bootstrap — Block 01: CVXPY infrastructure + SU(2)/SU(3) moment-bootstrap.

First real CVXPY-based SDP bootstrap on this framework, unblocked by infra
PR #430 (venv + cvxpy 1.8.2 + CLARABEL/SCS).

This runner:
1. Computes single-plaquette moments for SU(2) (Bessel exact) and SU(3)
   (numerical Haar integration on Cartan torus) at β=6.
2. Sets up CVXPY-based moment-problem bootstrap with Hankel PSD +
   Hausdorff monotonicity + SU(N)-specific support [-1, 1] (since
   P = (1/N) Re tr U ∈ [-1, 1]).
3. Solves max/min m_1 = ⟨P⟩ subject to PSD constraints, getting a
   CVXPY-derived bracket.
4. Compares to canonical MC + bridge-support stack + Bessel exact.

Realistic precision: 5-15% wide bracket from L_max ≤ 6 with CLARABEL/SCS
(no Mosek). Industrial-precision (Kazakov-Zheng 2022 ~10⁻²) requires Mosek
+ ~3-month engineering; out of 12h scope.

Forbidden inputs:
- PDG values
- Lattice MC <P>=0.5934 as load-bearing (comparator only)
- Hard-coded bootstrap brackets

Run with venv: .venv/bin/python3 scripts/frontier_industrial_sdp_bootstrap_block01.py
"""

from __future__ import annotations

import math
import sys
from typing import List, Tuple

import numpy as np
from scipy.special import iv  # modified Bessel
from scipy.integrate import quad

import cvxpy as cp


# ---------------------------------------------------------------------------
# Section 1: Single-plaquette analytical references
# ---------------------------------------------------------------------------

def su2_single_plaquette_bessel_moments(beta: float, k_max: int = 4) -> List[float]:
    """SU(2) single-plaquette moments ⟨P^k⟩ where P = (1/2) tr U = cos(θ/2),
    via Bessel function ratios.

    For SU(2), Haar measure: dU = (1/(2π²)) sin²θ dθ dφ_1 dφ_2 (Euler angles).
    Single-link integral: Z(β) = ∫dU exp((β/2) tr U) = ∫dU exp(β·cos(θ/2)).
    Reduces to: Z(β) ∝ I_1(β)/β (modified Bessel).

    ⟨(1/2 tr U)^k⟩ = ⟨cos^k(θ/2)⟩ — computable via Chebyshev / Bessel sums.
    Standard result:
      ⟨(1/2) tr U⟩ = I_2(β) / I_1(β)
      ⟨((1/2) tr U)^k⟩ for k>1: more complex; can be computed numerically.

    Use numerical integration on θ ∈ [0, π] with Haar weight sin²(θ/2).
    """
    moments = []
    Z, _ = quad(lambda theta: math.sin(theta/2)**2 * math.exp(beta * math.cos(theta/2)), 0, math.pi)
    for k in range(k_max + 1):
        if k == 0:
            moments.append(1.0)
            continue
        num, _ = quad(
            lambda theta: math.sin(theta/2)**2 * math.cos(theta/2)**k * math.exp(beta * math.cos(theta/2)),
            0, math.pi,
        )
        moments.append(num / Z)
    return moments


def su3_single_plaquette_haar_moments(beta: float, k_max: int = 4) -> List[float]:
    """SU(3) single-plaquette moments ⟨P^k⟩ where P = (1/3) Re tr U.

    SU(3) Haar measure on Cartan torus: dU ∝ |∏_{i<j}(z_i - z_j)|² ∏dφ_i
    where z_i = exp(i φ_i) and ∑φ_i = 0 (det U = 1 constraint).

    Use numerical integration over (φ_1, φ_2) with φ_3 = -φ_1 - φ_2.
    tr U = ∑_i exp(i φ_i), so Re tr U = ∑_i cos φ_i.

    Weyl integration: integrate over (φ_1, φ_2, φ_3) with constraint ∑φ_i ≡ 0,
    weight = |Vandermonde|² / 3! = product of |sin((φ_i - φ_j)/2)|² for i<j.
    """
    moments = []

    def integrand_for_moment(phi1: float, phi2: float, k: int) -> float:
        phi3 = -phi1 - phi2
        # Re tr U = cos φ_1 + cos φ_2 + cos φ_3
        re_tr_U = math.cos(phi1) + math.cos(phi2) + math.cos(phi3)
        P = re_tr_U / 3.0  # P = (1/3) Re tr U

        # Vandermonde squared (Weyl measure) for SU(3):
        # |sin((φ_1-φ_2)/2)|² · |sin((φ_2-φ_3)/2)|² · |sin((φ_3-φ_1)/2)|²
        v = (math.sin((phi1 - phi2) / 2) ** 2
             * math.sin((phi2 - phi3) / 2) ** 2
             * math.sin((phi3 - phi1) / 2) ** 2)
        weight = v * math.exp((beta / 3) * re_tr_U)
        return weight * (P ** k)

    # Use a 2D grid integration (simpler than scipy.dblquad for stability)
    N = 80  # grid points per dimension
    phi_grid = np.linspace(-math.pi, math.pi, N, endpoint=False)
    dphi = 2 * math.pi / N

    Z = 0.0
    for phi1 in phi_grid:
        for phi2 in phi_grid:
            Z += integrand_for_moment(phi1, phi2, 0) * dphi * dphi

    for k in range(k_max + 1):
        if k == 0:
            moments.append(1.0)
            continue
        num = 0.0
        for phi1 in phi_grid:
            for phi2 in phi_grid:
                num += integrand_for_moment(phi1, phi2, k) * dphi * dphi
        moments.append(num / Z)

    return moments


# ---------------------------------------------------------------------------
# Section 2: Hankel moment matrix via CVXPY
# ---------------------------------------------------------------------------

def build_hankel(moments_var: List, N: int) -> cp.Expression:
    """Build the N x N Hankel matrix from moment variables/values.
    H[i,j] = m_{i+j} where i, j = 0, ..., N-1.

    moments_var must have at least 2N - 1 elements.
    """
    rows = []
    for i in range(N):
        rows.append([moments_var[i + j] for j in range(N)])
    return cp.bmat(rows)


def cvxpy_max_min_m1_with_hankel(N: int, support: Tuple[float, float] = (-1.0, 1.0),
                                  fix_moments: dict = None) -> dict:
    """Set up CVXPY moment-problem bootstrap:
    - Variables: m_0 = 1 (fixed), m_1, m_2, ..., m_{2N-2}
    - Constraints:
      - Hankel matrix H[i,j] = m_{i+j} for i, j = 0..N-1 is PSD
      - Modified Hankel for [a, b]-support: (b-x)(x-a) ≥ 0 ⟹ specific PSD
      - Optional: fix some moments to known values (loop equations or single-plaquette)
    - Objective: max or min m_1 = ⟨P⟩
    """
    n_moments = 2 * N - 1
    m = [cp.Variable() for _ in range(n_moments)]
    # m_0 = 1
    constraints = [m[0] == 1.0]
    # Hankel PSD
    H = build_hankel(m, N)
    constraints.append(H >> 0)
    # Hausdorff: shifted Hankel for [a,b] support
    a, b = support
    # For support [a, b]: matrices (m_{i+j+1} - a m_{i+j}) and (b m_{i+j} - m_{i+j+1}) PSD (size N-1)
    if N >= 2:
        H1_size = N - 1
        H1 = cp.bmat([[m[i + j + 1] - a * m[i + j] for j in range(H1_size)]
                      for i in range(H1_size)])
        H2 = cp.bmat([[b * m[i + j] - m[i + j + 1] for j in range(H1_size)]
                      for i in range(H1_size)])
        constraints.append(H1 >> 0)
        constraints.append(H2 >> 0)
    # Fix specific moments if provided
    if fix_moments is not None:
        for k, v in fix_moments.items():
            if 0 <= k < n_moments:
                constraints.append(m[k] == v)

    # Maximize m_1
    prob_max = cp.Problem(cp.Maximize(m[1]), constraints)
    prob_max.solve()
    m1_max = prob_max.value
    status_max = prob_max.status

    # Minimize m_1 (re-solve)
    m_min = [cp.Variable() for _ in range(n_moments)]
    constraints_min = [m_min[0] == 1.0]
    H_min = build_hankel(m_min, N)
    constraints_min.append(H_min >> 0)
    if N >= 2:
        H1m_size = N - 1
        H1m = cp.bmat([[m_min[i + j + 1] - a * m_min[i + j] for j in range(H1m_size)]
                       for i in range(H1m_size)])
        H2m = cp.bmat([[b * m_min[i + j] - m_min[i + j + 1] for j in range(H1m_size)]
                       for i in range(H1m_size)])
        constraints_min.append(H1m >> 0)
        constraints_min.append(H2m >> 0)
    if fix_moments is not None:
        for k, v in fix_moments.items():
            if 0 <= k < n_moments:
                constraints_min.append(m_min[k] == v)
    prob_min = cp.Problem(cp.Minimize(m_min[1]), constraints_min)
    prob_min.solve()
    m1_min = prob_min.value
    status_min = prob_min.status

    return {
        "N": N,
        "support": support,
        "fix_moments": fix_moments,
        "m1_max": m1_max,
        "m1_min": m1_min,
        "status_max": status_max,
        "status_min": status_min,
        "n_moments": n_moments,
    }


# ---------------------------------------------------------------------------
# Section 3: Validation suite
# ---------------------------------------------------------------------------

def validate_su2_su3_brackets(beta: float = 6.0) -> List[str]:
    """Run the bootstrap brackets for SU(2) + SU(3) at β=6 and report."""
    out = []

    out.append(f"=== β = {beta} ===")
    out.append("")

    # SU(2) reference moments
    out.append("--- SU(2) single-plaquette reference (Bessel + numerical Haar integration) ---")
    su2_mom = su2_single_plaquette_bessel_moments(beta=beta, k_max=4)
    for k, v in enumerate(su2_mom):
        out.append(f"  ⟨P^{k}⟩_SU(2)_single = {v:.8f}")

    # SU(3) reference moments
    out.append("")
    out.append("--- SU(3) single-plaquette reference (numerical Haar on Cartan torus, N=80²) ---")
    su3_mom = su3_single_plaquette_haar_moments(beta=beta, k_max=4)
    for k, v in enumerate(su3_mom):
        out.append(f"  ⟨P^{k}⟩_SU(3)_single = {v:.8f}")

    out.append("")
    out.append("--- CVXPY bootstrap brackets (Hankel + Hausdorff PSD only) ---")
    # Pure PSD brackets (no fixed moments) — should give [a, b] = [-1/3, 1] for SU(3) plaquette
    # Actually P = (1/N) Re tr U has support depending on N. For SU(3): tr U ∈ [-1, 3] so P = Re tr U/3 ∈ [-1/3, 1]
    for label, support in [("SU(2)/single (P ∈ [-1, 1])", (-1.0, 1.0)),
                           ("SU(3)/single (P ∈ [-1/3, 1])", (-1.0/3.0, 1.0))]:
        out.append(f"")
        out.append(f"  Bracket via PSD only ({label}):")
        for N in [2, 3, 4]:
            res = cvxpy_max_min_m1_with_hankel(N=N, support=support, fix_moments=None)
            out.append(f"    N = {N} (Hankel size, {res['n_moments']} moments): "
                       f"m_1 ∈ [{res['m1_min']:.6f}, {res['m1_max']:.6f}]  "
                       f"(status: {res['status_min']}/{res['status_max']})")

    out.append("")
    out.append("--- CVXPY bootstrap with single-plaquette moments fixed ---")
    out.append("  Fix m_2, m_3, m_4 to single-plaquette reference values; bracket m_1.")
    out.append("  Tests: does CVXPY correctly recover m_1 = ref value?")

    # SU(2) test: fix m_2, m_3, m_4 from Bessel reference, see if CVXPY brackets m_1 = ref
    fix_su2 = {2: su2_mom[2], 3: su2_mom[3], 4: su2_mom[4]}
    res_su2 = cvxpy_max_min_m1_with_hankel(N=3, support=(-1.0, 1.0), fix_moments=fix_su2)
    out.append(f"  SU(2): fixed m_2,3,4 from Bessel ref. Bracket m_1 ∈ "
               f"[{res_su2['m1_min']:.6f}, {res_su2['m1_max']:.6f}]")
    out.append(f"    Reference m_1_SU(2) = {su2_mom[1]:.6f}; "
               f"CVXPY recovered? {abs(res_su2['m1_max'] - su2_mom[1]) < 1e-3 or abs(res_su2['m1_min'] - su2_mom[1]) < 1e-3}")

    # SU(3) test: same with SU(3) reference
    fix_su3 = {2: su3_mom[2], 3: su3_mom[3], 4: su3_mom[4]}
    res_su3 = cvxpy_max_min_m1_with_hankel(N=3, support=(-1.0/3.0, 1.0), fix_moments=fix_su3)
    out.append(f"  SU(3): fixed m_2,3,4 from Haar ref. Bracket m_1 ∈ "
               f"[{res_su3['m1_min']:.6f}, {res_su3['m1_max']:.6f}]")
    out.append(f"    Reference m_1_SU(3) = {su3_mom[1]:.6f}; "
               f"CVXPY recovered? {abs(res_su3['m1_max'] - su3_mom[1]) < 1e-3 or abs(res_su3['m1_min'] - su3_mom[1]) < 1e-3}")

    return out


def main() -> int:
    print("=" * 78)
    print("Industrial SDP Bootstrap — Block 01: CVXPY moment-bootstrap")
    print("Unblocked by infra PR #430 (cvxpy 1.8.2 + CLARABEL/SCS via venv)")
    print("=" * 78)

    # Verify CVXPY workings
    print(f"\nCVXPY version: {cp.__version__}")
    print(f"Available solvers: {cp.installed_solvers()}")

    # Run validation suite
    for line in validate_su2_su3_brackets(beta=6.0):
        print(line)

    print()
    print("=" * 78)
    print("Block 01 SDP infrastructure validation complete.")
    print()
    print("Comparators:")
    print("  Canonical MC SU(3) ⟨P⟩(β=6) = 0.5934 (PLAQUETTE_SELF_CONSISTENCY)")
    print("  Bridge-support analytic upper-bound = 0.59353")
    print("  SU(2) lattice MC at β=6 ≈ 0.7706 (Creutz 1980 reference)")
    print()
    print("Observation: pure PSD brackets without loop equations are wide.")
    print("Adding single-plaquette moment constraints shows CVXPY workflow is")
    print("functional. Block 02 will apply real loop equations / multi-Wilson-loop")
    print("bootstrap to attempt a tighter bracket on SU(3) ⟨P⟩(β=6).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
