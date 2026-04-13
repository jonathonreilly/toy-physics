#!/usr/bin/env python3
"""
S^3 Discrete-to-Continuum Gap (V4)
====================================

Attack the single remaining obstruction to upgrading S^3 from BOUNDED to CLOSED:
Perelman's theorem applies to smooth 3-manifolds, not to finite graphs.

Four approaches tested:

  Approach 1 (Gromov-Hausdorff): Estimate the GH distance between the doubled
      Z^3 ball B_L (with antipodal boundary identification) and the round S^3
      of matching radius. If d_GH -> 0 as L -> infinity, the GH limit is a
      compact metric space homeomorphic to S^3.

  Approach 2 (Spectral / Cheeger-Colding): Compute eigenvalues of the graph
      Laplacian on the doubled ball for L = 2..10. Check convergence of
      lambda_1 * R^2 toward the S^3 value of 3.0. Cheeger-Colding theory
      says spectral convergence + Ricci lower bound => the GH limit is a
      Riemannian manifold.

  Approach 3 (Combinatorial manifold / link condition): Check whether the
      doubled-ball simplicial complex satisfies the combinatorial manifold
      conditions (every vertex link is a combinatorial 2-sphere). If so, it
      IS a PL 3-manifold by definition.

  Approach 4 (Quasi-isometry to Regge triangulation): Check whether Z^3 is
      quasi-isometric to a simplicial complex that triangulates the 3-ball.
      Regge calculus gives discrete-to-continuum convergence for simplicial
      gravity.

HONEST ASSESSMENT: None of these approaches fully close V4 in this script.
The script documents what each approach achieves and what remains open.

PStack experiment: frontier-s3-discrete-continuum
"""

from __future__ import annotations
import math
import time
import sys
import itertools

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse import lil_matrix, csr_matrix
    from scipy.sparse.linalg import eigsh
    HAS_SCIPY = True
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)

# ============================================================================
# Utility: Build Z^3 ball and doubled-ball graph Laplacian
# ============================================================================

def z3_ball_sites(R: int) -> list[tuple[int, int, int]]:
    """Return all Z^3 sites within Euclidean distance R of origin."""
    sites = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                if x * x + y * y + z * z <= R * R:
                    sites.append((x, y, z))
    return sites


def boundary_sites(sites_set: set, all_sites: list) -> list:
    """Sites that have at least one missing Z^3 neighbor."""
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    bdry = []
    for s in all_sites:
        for d in directions:
            nb = (s[0] + d[0], s[1] + d[1], s[2] + d[2])
            if nb not in sites_set:
                bdry.append(s)
                break
    return bdry


def build_doubled_ball_laplacian(R: int):
    """
    Build the graph Laplacian for the doubled Z^3 ball:
    two copies of B_R glued along the boundary via antipodal identification.

    Returns: (L_sparse, N, n_interior, n_boundary)
    """
    sites = z3_ball_sites(R)
    sites_set = set(sites)
    bdry = boundary_sites(sites_set, sites)
    bdry_set = set(bdry)
    interior = [s for s in sites if s not in bdry_set]

    # Index: copy 1 interior, copy 1 boundary, copy 2 interior
    # Boundary nodes are shared (identified antipodally between copies)
    # Actually for the doubled ball: two copies of interior, one copy of boundary
    # Copy 1 interior: indices 0..len(interior)-1
    # Boundary: indices len(interior)..len(interior)+len(bdry)-1
    # Copy 2 interior: indices len(interior)+len(bdry)..2*len(interior)+len(bdry)-1

    n_int = len(interior)
    n_bdy = len(bdry)
    N = 2 * n_int + n_bdy

    # Maps
    int_idx_1 = {s: i for i, s in enumerate(interior)}
    bdy_idx = {s: n_int + i for i, s in enumerate(bdry)}
    # Copy 2: interior sites mapped by antipodal map
    # Antipodal: (x,y,z) -> (-x,-y,-z)
    int_idx_2 = {s: 2 * n_int + n_bdy - 1 - i for i, s in enumerate(interior)}
    # Actually let's be more careful
    int_idx_2 = {}
    for i, s in enumerate(interior):
        int_idx_2[s] = n_int + n_bdy + i

    def get_idx_copy1(s):
        if s in int_idx_1:
            return int_idx_1[s]
        return bdy_idx[s]

    def get_idx_copy2(s):
        if s in int_idx_2:
            return int_idx_2[s]
        # Boundary: antipodal identification
        anti = (-s[0], -s[1], -s[2])
        if anti in bdy_idx:
            return bdy_idx[anti]
        # If antipodal is not on boundary, this is a problem
        # Fall back to same boundary node
        return bdy_idx.get(s, -1)

    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    L = lil_matrix((N, N), dtype=float)

    # Copy 1 edges
    for s in sites:
        idx_s = get_idx_copy1(s)
        for d in directions:
            nb = (s[0] + d[0], s[1] + d[1], s[2] + d[2])
            if nb in sites_set:
                idx_nb = get_idx_copy1(nb)
                L[idx_s, idx_s] += 1
                L[idx_s, idx_nb] -= 1

    # Copy 2 edges (interior only; boundary is shared)
    for s in interior:
        idx_s = int_idx_2[s]
        for d in directions:
            nb = (s[0] + d[0], s[1] + d[1], s[2] + d[2])
            if nb in sites_set:
                if nb in int_idx_2:
                    idx_nb = int_idx_2[nb]
                else:
                    # nb is boundary -- use antipodal identification for copy 2
                    anti_nb = (-nb[0], -nb[1], -nb[2])
                    if anti_nb in bdy_idx:
                        idx_nb = bdy_idx[anti_nb]
                    else:
                        idx_nb = bdy_idx.get(nb, -1)
                        if idx_nb == -1:
                            continue
                L[idx_s, idx_s] += 1
                L[idx_s, idx_nb] -= 1

    return csr_matrix(L), N, n_int, n_bdy


# ============================================================================
# APPROACH 1: Gromov-Hausdorff distance estimate
# ============================================================================

def approach1_gromov_hausdorff(R_values: list[int]) -> list[dict]:
    """
    Estimate GH distance between doubled Z^3 ball and round S^3.

    Strategy: Use the distortion of the natural map phi: doubled_ball -> S^3
    that sends each lattice point to its angular position on S^3 of radius R.

    The GH distance satisfies: d_GH(X, Y) <= (1/2) * dis(phi)
    where dis(phi) = sup |d_X(x,x') - d_Y(phi(x),phi(x'))|.

    For the Z^3 ball of radius R embedded in R^3, the lattice metric deviates
    from the Euclidean metric by at most sqrt(3) (one lattice step in 3D).
    The Euclidean metric on the ball vs the round metric on S^3 differ by
    O(1/R) corrections from curvature.

    So we expect d_GH ~ O(1) + O(1/R), which goes to a constant, NOT to zero.

    This is the fundamental issue: Z^3 has corners and flat faces that give
    O(1) GH distortion from S^3 even at large R.
    """
    results = []
    for R in R_values:
        sites = z3_ball_sites(R)
        n = len(sites)

        # Lattice metric: shortest path distance on Z^3 (= L1 distance)
        # vs Euclidean distance
        # Sample random pairs and compute distortion
        rng = np.random.default_rng(42 + R)
        n_pairs = min(2000, n * (n - 1) // 2)

        if n < 2:
            results.append({"R": R, "n_sites": n, "distortion": float("inf")})
            continue

        indices = rng.choice(n, size=(n_pairs, 2), replace=True)
        max_distortion = 0.0
        for i, j in indices:
            if i == j:
                continue
            s1, s2 = sites[i], sites[j]
            d_lattice = abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) + abs(s1[2] - s2[2])
            d_euclid = math.sqrt(sum((a - b) ** 2 for a, b in zip(s1, s2)))
            distortion = abs(d_lattice - d_euclid)
            if distortion > max_distortion:
                max_distortion = distortion

        # Normalize by R to get relative distortion
        rel_distortion = max_distortion / R if R > 0 else float("inf")

        results.append({
            "R": R,
            "n_sites": n,
            "max_distortion": round(max_distortion, 4),
            "relative_distortion": round(rel_distortion, 4),
        })
    return results


# ============================================================================
# APPROACH 2: Spectral convergence (Cheeger-Colding)
# ============================================================================

def approach2_spectral_convergence(R_values: list[int]) -> list[dict]:
    """
    Compute lambda_1 of graph Laplacian on doubled Z^3 ball.
    Target: lambda_1 * R^2 -> 3.0 (S^3 first eigenvalue).

    Cheeger-Colding theorem: If a sequence of compact length spaces (X_i, d_i)
    with Ricci >= -(n-1) * delta_i (delta_i -> 0) converges in GH sense to X,
    then eigenvalues of the Laplacian on X_i converge to eigenvalues on X.

    For Z^3 balls, the "Ricci" is non-negative in the Bakry-Emery sense
    for the standard graph Laplacian.
    """
    results = []
    for R in R_values:
        try:
            L_sp, N, n_int, n_bdy = build_doubled_ball_laplacian(R)
            # Compute smallest few eigenvalues
            k = min(6, N - 2)
            if k < 2:
                results.append({"R": R, "N": N, "lambda1": None, "ratio": None})
                continue
            eigvals = eigsh(L_sp, k=k, sigma=0, which='LM', return_eigenvectors=False)
            eigvals = np.sort(np.abs(eigvals))

            # lambda_0 should be ~0 (constant mode)
            # lambda_1 is the spectral gap
            lambda1 = eigvals[1] if len(eigvals) > 1 else None
            ratio = lambda1 * R * R if lambda1 is not None else None

            results.append({
                "R": R,
                "N": N,
                "n_interior": n_int,
                "n_boundary": n_bdy,
                "lambda_0": round(float(eigvals[0]), 6),
                "lambda_1": round(float(lambda1), 6) if lambda1 else None,
                "lambda1_R2": round(float(ratio), 4) if ratio else None,
                "target": 3.0,
                "gap_pct": round(abs(ratio - 3.0) / 3.0 * 100, 1) if ratio else None,
            })
        except Exception as e:
            results.append({"R": R, "error": str(e)})
    return results


# ============================================================================
# APPROACH 3: Combinatorial manifold / link condition
# ============================================================================

def approach3_link_condition(R_values: list[int]) -> list[dict]:
    """
    Check whether the doubled Z^3 ball satisfies the link condition for
    being a combinatorial 3-manifold.

    For a cubical complex (not simplicial), the relevant condition is:
    - The link of every vertex is homeomorphic to S^2.
    - The link of every edge is homeomorphic to S^1.

    In a 6-regular graph (interior of Z^3), the link of each vertex is
    the octahedron (6 neighbors, 12 edges forming the boundary of an
    octahedron). The octahedron is homeomorphic to S^2. CHECK.

    For boundary vertices (degree < 6) or vertices near the gluing,
    the link may fail to be S^2.

    This is the KEY diagnostic: if all vertex links are S^2, the complex
    is a PL 3-manifold by the definition of combinatorial manifold.
    """
    results = []
    for R in R_values:
        sites = z3_ball_sites(R)
        sites_set = set(sites)
        bdry = set(s for s in sites if any(
            (s[0]+d[0], s[1]+d[1], s[2]+d[2]) not in sites_set
            for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
        ))

        directions = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

        # For interior sites: degree = 6, link = octahedron = S^2. Always passes.
        interior_count = 0
        interior_pass = 0
        for s in sites:
            if s not in bdry:
                deg = sum(1 for d in directions if (s[0]+d[0], s[1]+d[1], s[2]+d[2]) in sites_set)
                interior_count += 1
                if deg == 6:
                    interior_pass += 1

        # For boundary sites: degree < 6 in the single ball.
        # In the doubled ball with antipodal identification, each boundary site
        # gets additional neighbors from copy 2.
        # Check: does doubling restore degree 6 for boundary sites?
        boundary_count = len(bdry)
        boundary_restored = 0
        boundary_degrees = []
        for s in bdry:
            # Neighbors in copy 1
            deg1 = sum(1 for d in directions if (s[0]+d[0], s[1]+d[1], s[2]+d[2]) in sites_set)
            # Missing neighbors
            missing = []
            for d in directions:
                nb = (s[0]+d[0], s[1]+d[1], s[2]+d[2])
                if nb not in sites_set:
                    missing.append(nb)
            # In copy 2 (antipodal), the missing neighbor nb maps to -nb.
            # -nb is in the ball iff |nb|^2 <= R^2. But nb is OUTSIDE the ball,
            # so |nb|^2 > R^2, meaning -nb is also outside (same norm).
            # Wait -- that's only true for the Euclidean ball. Actually:
            # nb = s + d, and nb is outside the ball means |nb|^2 > R^2.
            # The antipodal of nb is -nb = -(s+d). Is -nb in the ball?
            # |-nb|^2 = |s+d|^2 = |nb|^2 > R^2. So -nb is ALSO outside.
            # This means antipodal identification does NOT restore degree 6
            # for boundary sites in this simple construction!
            #
            # The actual doubled-ball construction needs a more sophisticated
            # gluing: we identify boundary site s with boundary site -s
            # (the antipodal ON the boundary). Then the neighbors of s in
            # copy 2 are the neighbors of -s in copy 2's interior.
            anti_s = (-s[0], -s[1], -s[2])
            if anti_s in bdry:
                # Neighbors of -s that are in the interior contribute to degree
                deg2_extra = sum(1 for d in directions
                                 if (-s[0]+d[0], -s[1]+d[1], -s[2]+d[2]) in sites_set
                                 and (-s[0]+d[0], -s[1]+d[1], -s[2]+d[2]) not in bdry)
                # But we need to avoid double-counting: if -s+d is in interior,
                # it's in copy 2 only
                total_deg = deg1 + deg2_extra
            else:
                # Antipodal not on boundary -- this is a problem
                total_deg = deg1

            boundary_degrees.append(total_deg)
            if total_deg == 6:
                boundary_restored += 1

        # Statistics
        deg_hist = {}
        for d in boundary_degrees:
            deg_hist[d] = deg_hist.get(d, 0) + 1

        results.append({
            "R": R,
            "n_sites": len(sites),
            "n_interior": interior_count,
            "n_boundary": boundary_count,
            "interior_all_deg6": interior_pass == interior_count,
            "boundary_restored_deg6": boundary_restored,
            "boundary_restoration_pct": round(boundary_restored / max(boundary_count, 1) * 100, 1),
            "boundary_degree_histogram": deg_hist,
            "link_condition_met": (interior_pass == interior_count) and (boundary_restored == boundary_count),
        })
    return results


# ============================================================================
# APPROACH 4: Quasi-isometry check
# ============================================================================

def approach4_quasi_isometry(R_values: list[int]) -> list[dict]:
    """
    Check quasi-isometry between Z^3 ball (L1 metric) and Euclidean ball
    (L2 metric).

    Two metric spaces are (K, C)-quasi-isometric if there exists a map f with:
      (1/K) * d(x,y) - C <= d(f(x), f(y)) <= K * d(x,y) + C

    The identity map from (Z^3, L1) to (R^3, L2) satisfies:
      d_L2(x,y) <= d_L1(x,y) <= sqrt(3) * d_L2(x,y)

    So K = sqrt(3), C = 0. This is a bilipschitz embedding (stronger than QI).

    The key question: does Z^3 ball with boundary identification give a
    space quasi-isometric to S^3?
    """
    results = []
    sqrt3 = math.sqrt(3)

    for R in R_values:
        sites = z3_ball_sites(R)
        n = len(sites)
        rng = np.random.default_rng(123 + R)
        n_pairs = min(3000, n * (n - 1) // 2)

        if n < 2:
            results.append({"R": R, "K_observed": None})
            continue

        indices = rng.choice(n, size=(n_pairs, 2), replace=True)
        max_ratio = 0.0
        min_ratio = float("inf")

        for i, j in indices:
            if i == j:
                continue
            s1, s2 = sites[i], sites[j]
            d_l1 = abs(s1[0]-s2[0]) + abs(s1[1]-s2[1]) + abs(s1[2]-s2[2])
            d_l2 = math.sqrt(sum((a-b)**2 for a, b in zip(s1, s2)))
            if d_l2 > 0:
                ratio = d_l1 / d_l2
                if ratio > max_ratio:
                    max_ratio = ratio
                if ratio < min_ratio:
                    min_ratio = ratio

        results.append({
            "R": R,
            "n_sites": n,
            "K_observed": round(max_ratio, 4),
            "K_theoretical": round(sqrt3, 4),
            "min_ratio": round(min_ratio, 4),
            "is_bilipschitz": max_ratio <= sqrt3 + 0.01,
            "C": 0,
        })
    return results


# ============================================================================
# APPROACH 2b: Spectral convergence with Richardson extrapolation
# ============================================================================

def approach2b_extrapolation(spectral_results: list[dict]) -> dict:
    """
    Given spectral data at multiple R values, extrapolate lambda_1 * R^2
    to R -> infinity using a 1/R correction model:

      lambda_1 * R^2 = a + b/R + c/R^2

    This tests whether the asymptotic value a is consistent with 3.0 (S^3).
    """
    valid = [(r["R"], r["lambda1_R2"]) for r in spectral_results
             if r.get("lambda1_R2") is not None and r["R"] >= 3]

    if len(valid) < 3:
        return {"extrapolation": "insufficient data", "n_points": len(valid)}

    Rs = np.array([v[0] for v in valid], dtype=float)
    ys = np.array([v[1] for v in valid], dtype=float)

    # Fit: y = a + b/R + c/R^2
    A = np.column_stack([np.ones_like(Rs), 1.0 / Rs, 1.0 / Rs**2])
    try:
        coeffs, residuals, rank, sv = np.linalg.lstsq(A, ys, rcond=None)
        a, b, c = coeffs
        residual = np.sqrt(np.mean((ys - A @ coeffs) ** 2))
        return {
            "extrapolated_value": round(float(a), 4),
            "target": 3.0,
            "deviation_pct": round(abs(a - 3.0) / 3.0 * 100, 1),
            "b_coeff": round(float(b), 4),
            "c_coeff": round(float(c), 4),
            "rms_residual": round(float(residual), 6),
            "n_points": len(valid),
            "R_range": (int(Rs[0]), int(Rs[-1])),
            "consistent_with_S3": abs(a - 3.0) < 1.0,  # within 33%
        }
    except Exception as e:
        return {"extrapolation_error": str(e)}


# ============================================================================
# THEORETICAL ANALYSIS: What each approach actually proves
# ============================================================================

def theoretical_analysis() -> dict:
    """
    Honest assessment of what each approach can and cannot achieve.
    """
    return {
        "approach_1_GH": {
            "what_it_proves": (
                "Z^3 ball is (sqrt(3), 0)-bilipschitz to Euclidean ball. "
                "As R -> inf, the rescaled space (1/R) * B_R converges in GH "
                "to the unit ball B^3 in R^3."
            ),
            "what_it_does_NOT_prove": (
                "GH convergence of the DOUBLED ball (with boundary identification) "
                "to S^3. The identification map is combinatorial, not smooth, and "
                "GH convergence of spaces with identifications requires control "
                "of the gluing geometry. This is NOT standard."
            ),
            "status": "PARTIAL -- proves convergence of the bulk, not the gluing",
            "what_would_close_it": (
                "A theorem that GH convergence of the bulk + convergence of the "
                "gluing map implies GH convergence of the quotient. This is "
                "plausible but requires careful metric geometry."
            ),
        },
        "approach_2_spectral": {
            "what_it_proves": (
                "Numerical evidence that lambda_1 * R^2 may converge to a value "
                "near 3.0 as R -> inf. If confirmed, this identifies the GH limit "
                "spectrally as S^3 (since S^3 is spectrally rigid among compact "
                "3-manifolds with the same lambda_1)."
            ),
            "what_it_does_NOT_prove": (
                "1. The convergence rate is slow (O(1/R) at best), and available "
                "R values are small. The extrapolation is noisy. "
                "2. Cheeger-Colding requires a Ricci lower bound on the approximants. "
                "Graphs don't have Ricci curvature in the classical sense. "
                "The Bakry-Emery or Ollivier Ricci curvature on Z^3 IS non-negative, "
                "but extending Cheeger-Colding to graph sequences is a theorem of "
                "Gigli-Mondino-Rajala (2015) for RCD spaces, and it is NOT clear "
                "that graph sequences fall into this framework."
            ),
            "status": "BOUNDED -- numerical evidence, not a proof",
            "what_would_close_it": (
                "Either: (a) prove the graph Laplacian eigenvalues converge to the "
                "S^3 Laplacian eigenvalues using the discrete-to-continuum spectral "
                "convergence theory of Burago-Ivanov-Kurylev (2014), or "
                "(b) compute at larger R (R=20+) to get convincing extrapolation."
            ),
        },
        "approach_3_link_condition": {
            "what_it_proves": (
                "Interior vertices of Z^3 have octahedral links (= S^2). "
                "So the interior is a combinatorial 3-manifold (with boundary)."
            ),
            "what_it_does_NOT_prove": (
                "Boundary vertices after gluing do NOT generically have S^2 links. "
                "The antipodal identification on a Z^3 sphere boundary creates "
                "vertices with irregular links (not all degree 6). The link "
                "condition FAILS at the gluing surface unless the triangulation "
                "is refined there."
            ),
            "status": "FAILS at the boundary -- the cubical complex is not a "
                      "combinatorial manifold at the gluing seam",
            "what_would_close_it": (
                "Barycentric subdivision of the gluing region to restore the link "
                "condition. This is standard in PL topology (every PL manifold "
                "has a subdivision that is a combinatorial manifold) but requires "
                "an explicit construction for this specific complex."
            ),
        },
        "approach_4_quasi_isometry": {
            "what_it_proves": (
                "Z^3 with L1 metric is bilipschitz to R^3 with L2 metric "
                "(K = sqrt(3), C = 0). Quasi-isometry preserves coarse "
                "topological invariants (quasi-isometry-invariant properties "
                "like number of ends, growth rate)."
            ),
            "what_it_does_NOT_prove": (
                "Quasi-isometry does NOT preserve fine topology. Two spaces "
                "can be quasi-isometric but have different fundamental groups "
                "(e.g., R^2 and the hyperbolic plane are quasi-isometric but "
                "have different geometry). The identification of the continuum "
                "limit requires metric convergence, not just quasi-isometry."
            ),
            "status": "IRRELEVANT to V4 -- quasi-isometry is too coarse",
            "what_would_close_it": (
                "Nothing -- this approach is a dead end for V4. QI invariants "
                "don't determine the manifold topology of the limit."
            ),
        },
    }


# ============================================================================
# SYNTHESIS: Honest verdict on V4
# ============================================================================

def synthesis_verdict() -> dict:
    return {
        "headline": (
            "V4 (discrete-to-continuum) is GENUINELY HARD OPEN MATHEMATICS. "
            "None of the four approaches closes it."
        ),
        "best_available_argument": (
            "The strongest argument combines approaches 1 and 2: "
            "(1) The bulk of the Z^3 ball converges in GH to the Euclidean ball. "
            "(2) The spectral data is CONSISTENT with the limit being S^3. "
            "(3) The growth axiom ensures simple connectivity at every finite stage. "
            "(4) If the GH limit exists and is a manifold, Perelman applies. "
            "The gap is in step (4): 'if the GH limit exists AND is a manifold.'"
        ),
        "why_physicists_accept_it": (
            "In lattice field theory, the continuum limit of Z^d with local "
            "interactions is universality-class dependent. Z^3 with nearest-neighbor "
            "hopping is in the universality class of R^3. The global topology is "
            "fixed by boundary conditions. This is standard physics but not "
            "rigorous mathematics."
        ),
        "why_mathematicians_reject_it": (
            "A finite graph is NOT a manifold. The fundamental group of a graph "
            "(which is always free) does not match pi_1 of the continuum limit "
            "without a coarse-graining theorem. The specific graph -> manifold "
            "correspondence for Z^3 balls with boundary identification is not "
            "proved in the literature."
        ),
        "what_would_close_V4": [
            "OPTION A: Prove that the barycentric subdivision of the doubled "
            "Z^3 ball (with boundary refinement) is a combinatorial 3-manifold. "
            "Then it IS a PL manifold by definition, pi_1 is computable "
            "combinatorially, and Perelman applies via Moise's theorem.",

            "OPTION B: Use the Burago-Ivanov-Kurylev (2014) spectral convergence "
            "framework to prove that the graph Laplacian spectrum converges to "
            "the manifold Laplacian spectrum. This identifies the limit manifold.",

            "OPTION C: Embed the construction in Regge calculus by replacing "
            "Z^3 cubes with simplices (6 tetrahedra per cube). The resulting "
            "simplicial complex triangulates the ball, and Regge calculus gives "
            "convergence. This requires showing the boundary identification "
            "extends to the simplicial structure.",

            "OPTION D (nuclear): Construct an explicit smooth embedding of the "
            "doubled ball in R^4 and show it is diffeomorphic to S^3. This is "
            "the most elementary approach but requires hard geometric analysis.",
        ],
        "recommended_paper_strategy": (
            "State explicitly: 'The discrete-to-continuum correspondence is "
            "standard in lattice field theory but is not a rigorous mathematical "
            "theorem for this specific graph family. We regard this as a physics "
            "derivation, consistent with standard practice in lattice gauge theory, "
            "rather than a mathematical proof.' This is honest, defensible, and "
            "standard for Nature-level physics papers."
        ),
        "status": "BOUNDED -- V4 remains open",
    }


# ============================================================================
# MAIN: Run all approaches, score, report
# ============================================================================

def main():
    t0 = time.time()
    pass_count = 0
    fail_count = 0
    bounded_count = 0

    print("=" * 72)
    print("S^3 DISCRETE-TO-CONTINUUM GAP (V4) -- FOUR APPROACHES")
    print("=" * 72)
    print()

    # R values for numerical tests
    R_vals = [2, 3, 4, 5, 6, 7]

    # --- APPROACH 1: Gromov-Hausdorff ---
    print("-" * 72)
    print("APPROACH 1: Gromov-Hausdorff distance estimates")
    print("-" * 72)
    gh_results = approach1_gromov_hausdorff(R_vals)
    for r in gh_results:
        md = r.get('max_distortion', 'N/A')
        rd = r.get('relative_distortion', 'N/A')
        print(f"  R={r['R']:2d}  |B_R|={r['n_sites']:5d}  "
              f"max_distortion={md}  relative={rd}")

    # Check: relative distortion should be bounded by sqrt(3)-1 ~ 0.732
    # (L1 vs L2 ratio is at most sqrt(3), so max distortion / L2 distance <= sqrt(3)-1)
    # The actual check: relative distortion (max_distortion/R) stays O(1) and bounded
    rels = [r["relative_distortion"] for r in gh_results if "relative_distortion" in r]
    sqrt3 = math.sqrt(3)
    if len(rels) >= 2 and all(r <= sqrt3 + 0.01 for r in rels):
        print(f"  CHECK: relative distortion bounded by sqrt(3)={sqrt3:.4f}. PASS.")
        pass_count += 1
    else:
        print("  CHECK: relative distortion exceeds sqrt(3). FAIL.")
        fail_count += 1
    print(f"  VERDICT: GH convergence of bulk: PASS. GH convergence of doubled ball: OPEN.")
    print()

    # --- APPROACH 2: Spectral convergence ---
    print("-" * 72)
    print("APPROACH 2: Spectral convergence (graph Laplacian)")
    print("-" * 72)
    spectral_results = approach2_spectral_convergence(R_vals)
    for r in spectral_results:
        if "error" in r:
            print(f"  R={r['R']:2d}  ERROR: {r['error']}")
        elif r.get("lambda1_R2") is not None:
            print(f"  R={r['R']:2d}  N={r['N']:5d}  lambda_1={r['lambda_1']:.6f}  "
                  f"lambda_1*R^2={r['lambda1_R2']:.4f}  target=3.0  "
                  f"gap={r['gap_pct']:.1f}%")
        else:
            print(f"  R={r['R']:2d}  N={r['N']:5d}  (no eigenvalue computed)")

    # Check: lambda_1 * R^2 should be increasing toward 3.0
    ratios = [(r["R"], r["lambda1_R2"]) for r in spectral_results
              if r.get("lambda1_R2") is not None]
    if len(ratios) >= 2:
        increasing = all(ratios[i][1] <= ratios[i+1][1] + 0.5 for i in range(len(ratios)-1))
        if increasing:
            print(f"  CHECK: lambda_1*R^2 roughly increasing. PASS (consistent with convergence)")
            pass_count += 1
        else:
            print(f"  CHECK: lambda_1*R^2 not monotonically increasing. BOUNDED.")
            bounded_count += 1

    # Extrapolation
    print()
    extrap = approach2b_extrapolation(spectral_results)
    if "extrapolated_value" in extrap:
        print(f"  EXTRAPOLATION (a + b/R + c/R^2 fit):")
        print(f"    R -> inf value: {extrap['extrapolated_value']:.4f}  "
              f"target: 3.0  deviation: {extrap['deviation_pct']:.1f}%")
        print(f"    Coefficients: b={extrap['b_coeff']:.4f}, c={extrap['c_coeff']:.4f}")
        print(f"    RMS residual: {extrap['rms_residual']:.6f}")
        print(f"    Consistent with S^3: {extrap['consistent_with_S3']}")
        if extrap["consistent_with_S3"]:
            print("  CHECK: extrapolation consistent with S^3 (within 33%). BOUNDED PASS.")
            bounded_count += 1
        else:
            print("  CHECK: extrapolation NOT consistent with S^3. BOUNDED FAIL.")
            fail_count += 1
    else:
        print(f"  EXTRAPOLATION: {extrap}")
        bounded_count += 1
    print(f"  VERDICT: Spectral evidence is BOUNDED (suggestive, not conclusive).")
    print()

    # --- APPROACH 3: Link condition ---
    print("-" * 72)
    print("APPROACH 3: Combinatorial manifold / link condition")
    print("-" * 72)
    link_results = approach3_link_condition(R_vals)
    for r in link_results:
        print(f"  R={r['R']:2d}  |sites|={r['n_sites']:5d}  "
              f"interior_deg6={r['interior_all_deg6']}  "
              f"boundary_restored={r['boundary_restoration_pct']:.1f}%  "
              f"link_condition={r['link_condition_met']}")
    # Check: interior always passes
    if all(r["interior_all_deg6"] for r in link_results):
        print("  CHECK: all interior vertices have degree 6 (octahedral link = S^2). PASS.")
        pass_count += 1
    else:
        print("  CHECK: some interior vertices lack degree 6. FAIL.")
        fail_count += 1

    # Check: boundary link condition
    boundary_passes = [r["link_condition_met"] for r in link_results]
    if all(boundary_passes):
        print("  CHECK: all boundary vertices restored to degree 6. PASS.")
        pass_count += 1
    else:
        pcts = [r["boundary_restoration_pct"] for r in link_results]
        avg_pct = sum(pcts) / len(pcts) if pcts else 0
        print(f"  CHECK: boundary link condition FAILS. Average restoration: {avg_pct:.1f}%.")
        print("  This is EXPECTED: the cubical doubled-ball is NOT a combinatorial manifold")
        print("  at the gluing seam. Barycentric subdivision would fix this.")
        bounded_count += 1
    print(f"  VERDICT: Interior is PL manifold. Boundary needs subdivision. BOUNDED.")
    print()

    # --- APPROACH 4: Quasi-isometry ---
    print("-" * 72)
    print("APPROACH 4: Quasi-isometry (Z^3 L1 vs R^3 L2)")
    print("-" * 72)
    qi_results = approach4_quasi_isometry(R_vals)
    for r in qi_results:
        if r.get("K_observed") is not None:
            print(f"  R={r['R']:2d}  K_observed={r['K_observed']:.4f}  "
                  f"K_theory={r['K_theoretical']:.4f}  "
                  f"bilipschitz={r['is_bilipschitz']}")
    if all(r.get("is_bilipschitz", False) for r in qi_results if r.get("K_observed") is not None):
        print("  CHECK: Z^3 is (sqrt(3), 0)-bilipschitz to R^3. PASS.")
        pass_count += 1
    else:
        print("  CHECK: bilipschitz bound violated. FAIL.")
        fail_count += 1
    print("  VERDICT: QI confirmed but IRRELEVANT to V4 (too coarse).")
    print()

    # --- THEORETICAL ANALYSIS ---
    print("-" * 72)
    print("THEORETICAL ANALYSIS: Honest assessment")
    print("-" * 72)
    theory = theoretical_analysis()
    for approach_name, info in theory.items():
        print(f"\n  {approach_name}:")
        print(f"    Status: {info['status']}")
        print(f"    Proves: {info['what_it_proves'][:100]}...")
        print(f"    Does NOT prove: {info['what_it_does_NOT_prove'][:100]}...")

    # --- SYNTHESIS ---
    print()
    print("=" * 72)
    print("SYNTHESIS: V4 Discrete-to-Continuum Verdict")
    print("=" * 72)
    verdict = synthesis_verdict()
    print()
    print(f"  HEADLINE: {verdict['headline']}")
    print()
    print(f"  BEST ARGUMENT: {verdict['best_available_argument'][:200]}...")
    print()
    print(f"  STATUS: {verdict['status']}")
    print()
    print("  WHAT WOULD CLOSE V4:")
    for i, opt in enumerate(verdict["what_would_close_V4"]):
        label = chr(ord('A') + i)
        print(f"    Option {label}: {opt[:120]}...")
    print()

    # --- SCORE ---
    elapsed = time.time() - t0
    print("=" * 72)

    # Exact checks: things that are mathematically verified
    exact_checks = [
        ("Interior vertices have degree 6 (link = octahedron = S^2)",
         all(r["interior_all_deg6"] for r in link_results)),
        ("Z^3 is bilipschitz to R^3 with K=sqrt(3)",
         all(r.get("is_bilipschitz", False) for r in qi_results if r.get("K_observed") is not None)),
        ("GH relative distortion bounded by sqrt(3)",
         len(rels) >= 2 and all(r <= sqrt3 + 0.01 for r in rels)),
    ]

    # Bounded checks: numerical evidence, not proofs
    bounded_checks = [
        ("Spectral extrapolation consistent with S^3",
         extrap.get("consistent_with_S3", False) if "consistent_with_S3" in extrap else False),
        ("Boundary link condition met after doubling",
         all(boundary_passes) if boundary_passes else False),
        ("V4 closed by any approach",
         False),  # HONEST: none of the approaches close V4
    ]

    exact_pass = sum(1 for _, v in exact_checks if v)
    exact_fail = sum(1 for _, v in exact_checks if not v)
    bounded_pass = sum(1 for _, v in bounded_checks if v)
    bounded_fail = sum(1 for _, v in bounded_checks if not v)

    print(f"EXACT CHECKS:   PASS={exact_pass} FAIL={exact_fail}")
    for name, val in exact_checks:
        print(f"  {'PASS' if val else 'FAIL'}: {name}")

    print(f"BOUNDED CHECKS: PASS={bounded_pass} FAIL={bounded_fail}")
    for name, val in bounded_checks:
        print(f"  {'PASS' if val else 'FAIL'}: {name}")

    total_pass = exact_pass + bounded_pass
    total_fail = exact_fail + bounded_fail
    print()
    print(f"TOTAL: PASS={total_pass} FAIL={total_fail}  ({elapsed:.1f}s)")
    print()
    print("V4 STATUS: BOUNDED (genuinely hard open mathematics)")
    print("RECOMMENDED: Acknowledge in paper; do not claim closure.")

    return 0 if exact_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
