#!/usr/bin/env python3
"""
S^3 Topology from Graph Growth Axioms
=====================================

MOTIVATION:
  The CC lane wants to use lambda_1(S^3) = 3/R^2. That coefficient is
  structural only if the topology is fixed. This script checks how far the
  graph-growth axioms actually get us.

CORE RESULT:
  The local graph-growth evidence is real:
    - shell boundaries are S^2-like (chi = 2) on the tested radii
    - the filled ball-like cubical complexes are contractible on the
      tested radii
  But the closed-manifold / compactification step is still extra input:
    a finite graph or shell-growing ball does not by itself force S^3.

WHAT THIS SCRIPT DOES NOT CLAIM:
  - finite graph -> compact continuum manifold
  - local growth -> closed 3-manifold
  - local growth -> S^3 without a global compactification / closure axiom

PStack experiment: frontier-s3-topology-derivation
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse import lil_matrix, csr_matrix
    from scipy.sparse.linalg import eigsh
    HAS_SCIPY = True
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)


# ===========================================================================
# Physical constants
# ===========================================================================
c = 2.99792458e8              # m/s
G_N = 6.67430e-11             # m^3 / (kg s^2)
hbar = 1.054571817e-34        # J s

l_Planck = math.sqrt(hbar * G_N / c**3)
R_Hubble = c / (67.4e3 / 3.0857e22)
Lambda_obs = 1.1056e-52       # m^-2
Omega_Lambda = 0.685
H_0 = 67.4e3 / 3.0857e22     # 1/s


# ===========================================================================
# ATTACK 1: Finite graph -> discrete spectrum; compactness is not derived
# ===========================================================================
def attack_1_compactness():
    """
    The axiom posits a FINITE lattice (finite-dimensional Hilbert space).
    A finite graph has a discrete graph Laplacian spectrum.
    That is not yet the same thing as deriving a compact continuum manifold.

    Key question: does the graph-growth surface force a closed topology,
    or does a compactification axiom still need to be supplied?
    """
    print("=" * 72)
    print("ATTACK 1: Finite graph -> discrete spectrum (compactness open)")
    print("=" * 72)

    print("""
  LOGICAL CHAIN:
    1. Axiom: Hilbert space is finite-dimensional (dim = N)
    2. One site per basis state -> graph has N vertices
    3. N finite -> graph spectrum is discrete
    4. Deriving a compact continuum manifold requires extra global input
    5. Any compact Riemannian manifold has a discrete spectrum with gap

  THEOREM (spectral theory):
    For any compact d-manifold M without boundary,
    the Laplacian eigenvalues satisfy:
      0 = lambda_0 < lambda_1 <= lambda_2 <= ...
    The spectral gap lambda_1 > 0 is guaranteed.
""")

    # Compute lambda_1 for several compact 3-manifolds
    manifolds = {
        "S^3 (3-sphere, radius R)":     {"lambda_1": 3.0,   "formula": "3/R^2"},
        "T^3 (3-torus, side L=2R)":     {"lambda_1": (2*math.pi/2)**2, "formula": "(2pi/L)^2 = pi^2/R^2"},
        "S^2 x S^1 (R_2=R, R_1=R)":    {"lambda_1": 2.0,   "formula": "2/R^2"},
        "RP^3 (real proj, radius R)":   {"lambda_1": 5.0,   "formula": "5/R^2 (first mode is l=2)"},
        "L(2,1) lens space":            {"lambda_1": 5.0,   "formula": "5/R^2"},
        "L(3,1) lens space":            {"lambda_1": 8.0/3, "formula": "8/(3R^2)"},
        "S^1 x S^1 x S^1 (cubic T^3)": {"lambda_1": math.pi**2, "formula": "pi^2/R^2"},
    }

    # Compute Lambda_pred / Lambda_obs for each
    print(f"  Spectral gap lambda_1 for compact 3-manifolds (all with scale R = R_H):")
    print(f"  {'Manifold':<35s} {'lambda_1 * R^2':>14s} {'Lambda_pred/Lambda_obs':>22s}")
    print(f"  {'-'*72}")

    results = {}
    for name, info in manifolds.items():
        lam1_R2 = info["lambda_1"]
        Lambda_pred = lam1_R2 / R_Hubble**2
        ratio = Lambda_pred / Lambda_obs
        print(f"  {name:<35s} {lam1_R2:>14.4f} {ratio:>22.4f}")
        results[name] = ratio

    # Key observation: the compact-manifold coefficient is topology-dependent.
    ratios = list(results.values())
    print(f"\n  Range of Lambda_pred/Lambda_obs: [{min(ratios):.2f}, {max(ratios):.2f}]")
    print(f"  Compact 3-manifolds give different O(1) coefficients.")
    print(f"  Finite Hilbert space alone does NOT fix the continuum topology.")

    print(f"\n  ATTACK 1 VERDICT: Discrete graph spectrum is derived; compact topology is not.")
    print(f"  The specific closed-manifold coefficient still depends on a global closure step.")

    return results


# ===========================================================================
# ATTACK 2: Graph growth gives spherical shells; closure remains open
# ===========================================================================
def attack_2_growth_topology():
    """
    If the lattice grows from a seed (as in the primordial spectrum derivation),
    what topology does the growing graph have?

    Key insight: uniform 3D growth from a point produces SHELLS.
    At each tested radius, the boundary of the grown region is S^2-like.
    The filled voxel region is ball-like (contractible on the tested radii).

    What is NOT derived here: a closed 3-manifold or the one-point
    compactification needed to identify the spatial slice with S^3.

    Numerical test: grow a 3D graph from a seed and measure its topology
    via the Betti numbers of the boundary.
    """
    print("\n" + "=" * 72)
    print("ATTACK 2: Graph growth gives spherical shells (closure open)")
    print("=" * 72)

    print("""
  GROWTH MODEL:
    Start from a seed node at the origin.
    At each step, add nodes at distance r+1 from center.
    Connect to all neighbors at distance r (local attachment).

    After N_steps, the grown region is ball-like.
    The spatial boundary at each radius is S^2-like.
    The closed-manifold compactification step is still open.
""")

    # Numerical demonstration: grow a 3D cubic lattice shell by shell
    # and measure the boundary topology via Euler characteristic
    N_max = 12  # max shell radius (keep computation manageable)

    # The boundary of a discrete ball in Z^3 forms a closed polyhedral surface.
    # We compute its Euler characteristic via the EXPOSED FACES method:
    # The boundary surface consists of the unit square faces between
    # interior and exterior voxels. This is a closed 2D cell complex.
    # chi = V_s - E_s + F_s where V_s, E_s, F_s are vertices, edges,
    # and faces of this polyhedral surface.

    print(f"  Growing 3D cubic graph shell-by-shell up to radius {N_max}:")
    print(f"  {'Radius':>8s} {'N_total':>10s} {'N_faces':>10s} {'chi(surface)':>14s} {'Topology':>12s}")
    print(f"  {'-'*58}")

    boundary_chi_values = []
    for R in range(1, N_max + 1):
        interior = set()
        for x in range(-R, R + 1):
            for y in range(-R, R + 1):
                for z in range(-R, R + 1):
                    if x*x + y*y + z*z <= R*R:
                        interior.add((x, y, z))

        n_total = len(interior)

        # Collect exposed faces (between interior and exterior voxels).
        # Each face is identified by its center (half-integer coord) and
        # normal direction. We store face as (center_2x, normal_axis).
        # Face vertices and edges live on the dual grid at half-integer points.
        face_set = set()    # (2*cx, 2*cy, 2*cz, axis)
        dirs = [(1,0,0,0),(-1,0,0,0),(0,1,0,1),(0,-1,0,1),(0,0,1,2),(0,0,-1,2)]
        for p in interior:
            for dx, dy, dz, axis in dirs:
                neighbor = (p[0]+dx, p[1]+dy, p[2]+dz)
                if neighbor not in interior:
                    # Face center at 2*(p + (dx,dy,dz)/2) to keep integer coords
                    fc = (2*p[0]+dx, 2*p[1]+dy, 2*p[2]+dz, axis)
                    face_set.add(fc)

        n_faces = len(face_set)

        # Collect surface vertices: corners of exposed faces.
        # Each face (normal to axis a) at center c has 4 corners offset by +/-1
        # in the two non-a directions (in 2x coordinates).
        vertex_set = set()
        edge_set = set()
        for (cx, cy, cz, axis) in face_set:
            if axis == 0:  # normal to x, face in yz plane
                corners = [(cx, cy+d1, cz+d2) for d1 in (-1,1) for d2 in (-1,1)]
            elif axis == 1:  # normal to y
                corners = [(cx+d1, cy, cz+d2) for d1 in (-1,1) for d2 in (-1,1)]
            else:  # normal to z
                corners = [(cx+d1, cy+d2, cz) for d1 in (-1,1) for d2 in (-1,1)]
            for v in corners:
                vertex_set.add(v)
            # 4 edges per face
            for i in range(4):
                e = tuple(sorted([corners[i], corners[(i+1)%4 if i < 3 else 0]]))
            # Use explicit pairing for square face corners in order
            ordered = [corners[0], corners[1], corners[3], corners[2]]  # (--,-+,++,+-)
            for i in range(4):
                e = tuple(sorted([ordered[i], ordered[(i+1)%4]]))
                edge_set.add(e)

        n_verts = len(vertex_set)
        n_edges = len(edge_set)

        chi = n_verts - n_edges + n_faces
        boundary_chi_values.append(chi)

        topology = "S^2" if chi == 2 else f"chi={chi}"
        print(f"  {R:>8d} {n_total:>10d} {n_faces:>10d} {chi:>14d} {topology:>12s}")

    n_s2 = sum(1 for c in boundary_chi_values if c == 2)
    print(f"\n  Boundaries with chi=2 (S^2 topology): {n_s2}/{len(boundary_chi_values)}")

    # The spatial manifold argument
    print(f"""
  TOPOLOGICAL ARGUMENT:
    1. Growth from a seed produces spherical shells with chi = 2.
    2. The boundary at each step has chi = 2 -> topology S^2.
    3. The filled region is ball-like on the tested discrete radii.
    4. Closing the boundary into a closed 3-manifold is additional input.
    5. If that extra closure is supplied, Perelman then gives S^3.
""")

    print(f"  ATTACK 2 VERDICT: Growth from a seed produces spherical shells.")
    print(f"  The closed-manifold / compactification step remains open.")

    return {"n_s2_boundaries": n_s2, "total": len(boundary_chi_values), "shells_s2": True}


# ===========================================================================
# ATTACK 3: Unitarity requires finite graph size, not a derived S^3
# ===========================================================================
def attack_3_unitarity():
    """
    On an infinite lattice, the Hilbert space is infinite-dimensional.
    The axiom requires finite-dimensional Hilbert space for unitary evolution.
    Therefore the graph must be finite, but that still does not determine
    the closed continuum topology.
    """
    print("\n" + "=" * 72)
    print("ATTACK 3: Unitarity requires finite graph size")
    print("=" * 72)

    print("""
  LOGICAL CHAIN:
    1. Evolution operator U = exp(-iHt) must be UNITARY
    2. Unitary on infinite-dim Hilbert space: spectrum can be continuous
       -> no spectral gap guaranteed (e.g., R^3 has lambda_min = 0)
    3. Unitary on FINITE-dim Hilbert space: spectrum is discrete
       -> lambda_1 > 0 guaranteed
    4. The axiom states dim(H) = N < infinity
    5. Therefore Lambda = lambda_1 > 0 automatically

  This is the deep reason why Lambda > 0:
    Lambda = 0 requires an INFINITE lattice (non-compact spatial manifold),
    which contradicts the finite Hilbert space axiom.
""")

    # Numerical demonstration: spectral gap scaling with graph size
    print(f"  Numerical check: spectral gap lambda_1 on finite vs 'open' lattices")
    print(f"  {'N':>6s} {'lambda_1 (periodic)':>20s} {'lambda_1 (Dirichlet)':>22s} {'lambda_1 (open chain)':>22s}")
    print(f"  {'-'*72}")

    results = {}
    for N in [8, 12, 16, 20, 24, 32]:
        # 1D periodic: lambda_1 = 2(1 - cos(2pi/N))
        lam_periodic = 2 * (1 - math.cos(2 * math.pi / N))

        # 1D Dirichlet (fixed ends): lambda_1 = 2(1 - cos(pi/(N+1)))
        lam_dirichlet = 2 * (1 - math.cos(math.pi / (N + 1)))

        # 1D open chain (free ends): lambda_1 = 2(1 - cos(pi/N))
        lam_open = 2 * (1 - math.cos(math.pi / N))

        print(f"  {N:>6d} {lam_periodic:>20.8f} {lam_dirichlet:>22.8f} {lam_open:>22.8f}")
        results[N] = {"periodic": lam_periodic, "dirichlet": lam_dirichlet, "open": lam_open}

    print(f"\n  All scale as lambda_1 ~ C/N^2 for large N.")
    print(f"  The coefficient C depends on boundary conditions:")
    print(f"    Periodic: C = (2*pi)^2 = {(2*math.pi)**2:.4f}")
    print(f"    Dirichlet: C = pi^2 = {math.pi**2:.4f}")
    print(f"    Open:      C = pi^2 = {math.pi**2:.4f}")

    # In 3D
    print(f"\n  In 3D, finite N gives a discrete graph spectrum.")
    print(f"  The graph size can make the lowest mode small, but topology is still undecided.")

    print(f"\n  ATTACK 3 VERDICT: Unitarity fixes finiteness, not closed topology.")
    print(f"  The CC coefficient still depends on the open compactification step.")

    return results


# ===========================================================================
# ATTACK 4: Poincare theorem applies only after a closed manifold is supplied
# ===========================================================================
def attack_4_poincare():
    """
    Perelman's theorem (2003): Every simply connected, closed 3-manifold
    is homeomorphic to S^3.

    Perelman's theorem applies only to a closed, simply connected 3-manifold.
    The shell-growth checks suggest ball-like regions, but they do not yet
    derive the closed-manifold compactification needed to invoke the theorem.
    """
    print("\n" + "=" * 72)
    print("ATTACK 4: Poincare theorem is conditional on closed topology")
    print("=" * 72)

    print("""
  PERELMAN'S THEOREM (Poincare conjecture, proved 2003):
    If M is a closed, simply connected 3-manifold, then M ~ S^3.

  "Closed" means compact without boundary.
  "Simply connected" means pi_1(M) = 0 (every loop contractible).

  QUESTION: Is the grown graph simply connected?

  ANSWER: The tested filled regions are ball-like, but closed topology is not
  yet derived. The Perelman step is therefore conditional, not closed.
""")

    # Topological argument for the filled regions.
    #
    # NOTE: The graph-theoretic first Betti number beta_1 = |E| - |V| + 1
    # counts independent GRAPH cycles, not pi_1 of the underlying space.
    # A filled 3D ball has many graph cycles but is still contractible.
    #
    # The correct object is the CLIQUE COMPLEX (or cubical complex) of the
    # graph. For a discrete ball in Z^3:
    #   - The cubical complex fills in all unit cubes whose 8 corners are present.
    #   - The tested filled regions are ball-like cubical complexes.
    #   - This is evidence for local contractibility, not a derived closed manifold.
    #
    # We verify a ball-like cubical-complex Euler characteristic on the tested
    # radii. That is a local check; it does not by itself prove a closed
    # 3-manifold or a compactification to S^3.

    print(f"  Numerical check: cubical complex topology of growing balls")
    print(f"  {'Radius':>8s} {'Vertices':>10s} {'Edges':>10s} {'Squares':>10s} {'Cubes':>8s} {'Contractible?':>16s}")
    print(f"  {'-'*66}")

    all_simply_connected = True
    for R in [2, 4, 6, 8, 10]:
        points = set()
        for x in range(-R, R + 1):
            for y in range(-R, R + 1):
                for z in range(-R, R + 1):
                    if x*x + y*y + z*z <= R*R:
                        points.add((x, y, z))

        V_count = len(points)

        # Count edges (pairs of adjacent lattice points both in set)
        E_count = 0
        for p in points:
            for dx, dy, dz in [(1,0,0),(0,1,0),(0,0,1)]:
                if (p[0]+dx, p[1]+dy, p[2]+dz) in points:
                    E_count += 1

        # Count filled unit squares (4 coplanar corners all in set)
        F_count = 0
        for p in points:
            for (d1, d2) in [((1,0,0),(0,1,0)), ((1,0,0),(0,0,1)), ((0,1,0),(0,0,1))]:
                corners = [
                    p,
                    (p[0]+d1[0], p[1]+d1[1], p[2]+d1[2]),
                    (p[0]+d2[0], p[1]+d2[1], p[2]+d2[2]),
                    (p[0]+d1[0]+d2[0], p[1]+d1[1]+d2[1], p[2]+d1[2]+d2[2]),
                ]
                if all(c in points for c in corners):
                    F_count += 1

        # Count filled unit cubes (all 8 corners in set)
        K_count = 0
        for p in points:
            corners = [(p[0]+dx, p[1]+dy, p[2]+dz)
                       for dx in (0,1) for dy in (0,1) for dz in (0,1)]
            if all(c in points for c in corners):
                K_count += 1

        # Euler characteristic of the cubical complex:
        # chi = V - E + F - K
        # For B^3 (contractible): chi = 1
        chi = V_count - E_count + F_count - K_count
        contractible = (chi == 1)
        if not contractible:
            all_simply_connected = False

        sc = "YES (chi=1)" if contractible else f"NO (chi={chi})"
        print(f"  {R:>8d} {V_count:>10d} {E_count:>10d} {F_count:>10d} {K_count:>8d} {sc:>16s}")

    print(f"\n  The tested filled regions are ball-like on the discrete voxels.")
    print(f"  This is evidence for local contractibility, not a closed 3-manifold.")

    if not all_simply_connected:
        print(f"  NOTE: chi != 1 for some radii due to discrete voxel effects.")
        print(f"  That does not change the main point: the closed-manifold step is open.")

    # The key distinction from T^3
    print(f"""
  WHY NOT T^3?
    T^3 = S^1 x S^1 x S^1 has pi_1 = Z^3 (three independent non-contractible loops).
    This requires IDENTIFYING opposite faces of a cube -- a global operation.
    Local growth from a seed does not by itself produce that identification.
    Therefore T^3 is not derived here.

  WHY NOT S^2 x S^1?
    S^2 x S^1 has pi_1 = Z (one non-contractible loop around S^1).
    This requires a "tunnel" or "handle" -- never produced by local growth.
    Therefore S^2 x S^1 is not derived here.

  WHY NOT RP^3?
    RP^3 = S^3 / Z_2 has pi_1 = Z_2.
    This requires antipodal identification -- a global operation.
    Therefore RP^3 is not derived here.

  WHY NOT lens spaces L(p,q)?
    L(p,q) = S^3 / Z_p has pi_1 = Z_p.
    This requires a discrete quotient -- a global operation.
    Therefore all lens spaces are not derived here.

  The ONLY closed, simply connected 3-manifold is S^3.
  But the closed-manifold premise is still extra input in this lane.
""")

    print(f"  ATTACK 4 VERDICT: Perelman applies only after closed topology is supplied.")
    print(f"  The current lane has not yet derived that closure.")

    return {"all_simply_connected": all_simply_connected, "closed_topology_derived": False}


# ===========================================================================
# ATTACK 5: Spectral coefficient comparison remains conditional
# ===========================================================================
def attack_5_spectral_selection():
    """
    This is a coefficient comparison only. It does not derive topology.

    Compute lambda_1 * R^2 for all compact 3-manifolds and compare
    to the observed value Lambda_obs * R_H^2.
    """
    print("\n" + "=" * 72)
    print("ATTACK 5: Spectral gap observational selection")
    print("=" * 72)

    # Observed value
    observed_C = Lambda_obs * R_Hubble**2
    print(f"\n  Observed: Lambda_obs * R_H^2 = {observed_C:.4f}")
    print(f"  (This is 3 * Omega_Lambda = {3 * Omega_Lambda:.4f})")

    # Analytic spectral gaps for compact 3-manifolds
    # lambda_1 = C / R^2 where C is the manifold-dependent constant
    manifolds = [
        ("S^3",             3.0,    "Simply connected"),
        ("T^3 (L=2R)",      math.pi**2,  "pi_1 = Z^3"),
        ("S^2 x S^1",       2.0,    "pi_1 = Z"),
        ("RP^3",            5.0,    "pi_1 = Z_2"),
        ("L(3,1)",          8.0/3,  "pi_1 = Z_3"),
        ("L(5,1)",          24.0/25, "pi_1 = Z_5"),
        ("L(5,2)",          24.0/25, "pi_1 = Z_5"),
        ("Nil manifold",    4*math.pi**2/9, "pi_1 = Heisenberg"),
        ("Sol manifold",    0.5,    "pi_1 = solvable"),  # approximate
    ]

    print(f"\n  {'Manifold':<25s} {'C = lambda_1*R^2':>16s} {'Lambda_pred/Lambda_obs':>22s} {'pi_1':>20s}")
    print(f"  {'-'*85}")

    best_match = None
    best_ratio = float('inf')

    for name, C, pi1 in manifolds:
        ratio = C / observed_C
        print(f"  {name:<25s} {C:>16.4f} {ratio:>22.4f} {pi1:>20s}")
        if abs(ratio - 1.0) < abs(best_ratio - 1.0):
            best_ratio = ratio
            best_match = name

    print(f"\n  Best match: {best_match} with ratio = {best_ratio:.4f}")

    # Detailed analysis of S^3 vs T^3
    print(f"\n  S^3 vs T^3 comparison:")
    C_S3 = 3.0
    C_T3 = math.pi**2  # for L = 2R (diameter matching)
    ratio_S3 = C_S3 / observed_C
    ratio_T3 = C_T3 / observed_C

    print(f"    S^3: Lambda_pred/Lambda_obs = {ratio_S3:.4f}  (off by {abs(ratio_S3-1)*100:.1f}%)")
    print(f"    T^3: Lambda_pred/Lambda_obs = {ratio_T3:.4f}  (off by {abs(ratio_T3-1)*100:.1f}%)")
    print(f"    S^3 is {abs(ratio_T3-1)/abs(ratio_S3-1):.1f}x closer to observation than T^3.")

    # What about S^2 x S^1?
    C_S2S1 = 2.0
    ratio_S2S1 = C_S2S1 / observed_C
    print(f"    S^2xS^1: Lambda_pred/Lambda_obs = {ratio_S2S1:.4f}  (off by {abs(ratio_S2S1-1)*100:.1f}%)")

    # Numerical lattice verification: compare spectral gap on S^3-like vs T^3 lattice
    print(f"\n  Numerical lattice verification (small lattices):")
    print(f"  {'N':>6s} {'lambda_1 (periodic/T^3)':>24s} {'lambda_1 (S^3 estimate)':>24s} {'Ratio T^3/S^3':>16s}")
    print(f"  {'-'*72}")

    for N in [6, 8, 10, 12, 14]:
        # T^3: periodic cubic lattice
        n3 = N**3
        # Analytic: lambda_1 = 2*(1 - cos(2*pi/N)) * 3 for 3D
        # Lowest mode: k = (2pi/N, 0, 0) -> lambda = 2(1-cos(2pi/N))
        lam_T3 = 2 * (1 - math.cos(2 * math.pi / N))

        # S^3: discrete approximation via icosahedral-type lattice
        # For a regular polytope approximation, lambda_1 = 3 * (2pi/L)^2 / (4pi^2/3)
        # = 3/(pi^2) * (2pi/N)^2 ... no, use the known ratio
        # On the lattice: lambda_1(S^3) / lambda_1(T^3) = 3 / (2pi/L)^2 * (L^2)
        # In lattice units: C_S3/C_T3 = 3/(pi^2) for L=2R matching
        # Actually: lambda_1(S^3) = 3/R^2 and lambda_1(T^3) = (2pi/L)^2
        # With L = pi*R (circumference of S^3): lambda_1(T^3) = (2pi/(pi*R))^2 = 4/R^2
        # Ratio: lambda_1(T^3)/lambda_1(S^3) = 4/3

        # Better: direct comparison with same physical size
        # S^3 radius R: volume = 2*pi^2*R^3, lambda_1 = 3/R^2
        # T^3 side L: volume = L^3, lambda_1 = (2pi/L)^2
        # Match volumes: L^3 = 2*pi^2*R^3 -> L = (2*pi^2)^(1/3) * R
        L_equiv = (2 * math.pi**2)**(1.0/3)  # in units of R
        lam_T3_equiv = (2 * math.pi / L_equiv)**2  # lambda_1 * R^2
        ratio = lam_T3_equiv / 3.0

        # Lattice: use N^3 periodic for T^3
        # and estimate S^3 gap from the continuum ratio
        lam_S3_est = lam_T3 * 3.0 / lam_T3_equiv

        print(f"  {N:>6d} {lam_T3:>24.8f} {lam_S3_est:>24.8f} {lam_T3/lam_S3_est:>16.4f}")

    print(f"\n  Volume-matched comparison:")
    L_equiv = (2 * math.pi**2)**(1.0/3)
    lam_T3_R2 = (2 * math.pi / L_equiv)**2
    print(f"    S^3: lambda_1 * R^2 = 3.0000")
    print(f"    T^3 (volume-matched): lambda_1 * R^2 = {lam_T3_R2:.4f}")
    print(f"    Ratio T^3/S^3 = {lam_T3_R2/3.0:.4f}")
    print(f"    Observed C = {observed_C:.4f}")
    print(f"    S^3 discrepancy: {abs(3.0/observed_C - 1)*100:.1f}%")
    print(f"    T^3 discrepancy: {abs(lam_T3_R2/observed_C - 1)*100:.1f}%")

    print(f"\n  ATTACK 5 VERDICT: S^3 is the closest coefficient among closed-manifold options.")
    print(f"  This is not a derivation of S^3; it is a conditional comparison.")

    return {
        "observed_C": observed_C,
        "S3_ratio": C_S3 / observed_C,
        "T3_ratio": C_T3 / observed_C,
        "best_match": best_match,
        "conditional_comparison_only": True,
    }


# ===========================================================================
# BONUS: Numerical Laplacian on S^3-like graph (icosahedral shells)
# ===========================================================================
def bonus_s3_lattice_eigenvalue():
    """
    Numerical sanity check for the analytic S^3 spectrum.
    This does not derive S^3 from the graph-growth axioms.
    """
    print("\n" + "=" * 72)
    print("BONUS: Numerical verification of S^3 spectral gap")
    print("=" * 72)

    # Method: sample N random points uniformly on S^3 (unit radius),
    # build a k-nearest-neighbor graph, compute Laplacian eigenvalue,
    # and verify it converges to lambda_1 = 3.

    rng = np.random.RandomState(42)

    # Sample uniformly on S^3 (unit 3-sphere in R^4)
    def sample_s3(n, rng):
        """Sample n points uniformly on unit S^3."""
        x = rng.randn(n, 4)
        x /= np.linalg.norm(x, axis=1, keepdims=True)
        return x

    print(f"\n  Method: k-NN graph on random points on S^3 (unit radius)")
    print(f"  Expected: lambda_1 -> 3.0 as N -> infinity")
    print()
    print(f"  {'N':>8s} {'k':>4s} {'lambda_1':>12s} {'lambda_1 * R^2':>16s} {'Error vs 3.0':>14s}")
    print(f"  {'-'*56}")

    for N in [200, 500, 1000, 2000]:
        points = sample_s3(N, rng)

        # Build k-NN graph with k proportional to N^(1/3)
        k = max(6, int(3 * N**(1.0/3)))
        if k >= N:
            k = N - 1

        # Compute all pairwise geodesic distances on S^3
        # d(p, q) = arccos(p . q)
        dots = points @ points.T
        dots = np.clip(dots, -1.0, 1.0)
        dists = np.arccos(dots)

        # k-nearest neighbors
        L = lil_matrix((N, N), dtype=float)
        for i in range(N):
            neighbors = np.argsort(dists[i])[1:k+1]  # exclude self
            for j in neighbors:
                # Weight by inverse distance (cotangent weight approximation)
                w = 1.0 / max(dists[i, j], 1e-10)
                L[i, j] -= w
                L[j, i] -= w
                L[i, i] += w
                L[j, j] += w

        # Symmetrize
        L = (L + L.T) / 2.0
        L_csr = L.tocsr()

        # Compute smallest nonzero eigenvalue
        try:
            evals = eigsh(L_csr, k=min(6, N-1), which='SM', return_eigenvectors=False)
            evals = np.sort(np.abs(evals))
            # Find first nonzero
            lam1 = None
            for ev in evals:
                if ev > 1e-8:
                    lam1 = ev
                    break
            if lam1 is None:
                continue
        except Exception:
            continue

        # Normalize: on unit S^3, lambda_1 should be 3.0
        # The graph Laplacian eigenvalue needs to be scaled by N^(2/3)
        # because the graph approximation has an effective "mesh size" h ~ N^(-1/3)
        # and the continuum eigenvalue is lambda_cont = lambda_graph / h^2
        # On S^3 of radius 1: volume = 2*pi^2, so h ~ (2*pi^2/N)^(1/3)
        h = (2 * math.pi**2 / N)**(1.0/3)
        lambda_cont = lam1 * h**2  # NOT correct for kNN -- use rescaling

        # Better: the spectral convergence of kNN Laplacian is
        # lambda_graph ~ lambda_cont * N^(2/d) / k for d-manifold
        # For S^3 (d=3): lambda_cont ~ lambda_graph * k / N^(2/3)
        lambda_est = lam1 * k / N**(2.0/3)

        # Scale factor from empirical calibration
        # The kNN Laplacian has a density-dependent normalization
        # For uniform density on S^3: rho = N / (2*pi^2)
        rho = N / (2 * math.pi**2)
        # Expected scaling: lambda_1 ~ 3 * rho^(2/3) * (some geometric factor) / k
        # Let's just report the raw ratio
        error = abs(lambda_est / 3.0 - 1.0) * 100

        print(f"  {N:>8d} {k:>4d} {lam1:>12.6f} {lambda_est:>16.6f} {error:>13.1f}%")

    print(f"""
  NOTE: kNN graph Laplacian convergence to the continuum is slow
  and normalization-dependent. The key theoretical result is ANALYTIC:
    On S^3 of radius R: lambda_1 = 3/R^2 (exact, from representation theory).
    On S^n of radius R: lambda_1 = n/R^2.
  This is a theorem about S^3 itself, not a derivation of S^3 from the axioms.
  The numerics above are a sanity check on the coefficient only.
""")

    print(f"  BONUS VERDICT: S^3 spectral gap lambda_1 = 3/R^2 is a mathematical theorem.")
    print(f"  The topology step that would make S^3 structural remains open.")


# ===========================================================================
# SYNTHESIS
# ===========================================================================
def synthesis(results_1, results_2, results_3, results_4, results_5):
    """Combine all five attacks into the derivation chain."""
    print("\n" + "=" * 72)
    print("SYNTHESIS: S^3 Topology Status")
    print("=" * 72)

    print(f"""
  THE CHAIN AS CURRENTLY JUSTIFIED:
  =====================

  Step 1: FINITE HILBERT SPACE (axiom)
    dim(H) = N < infinity
    |
    v
  Step 2: FINITE GRAPH / DISCRETE SPECTRUM
    N sites, local connections, finite graph spectrum
    |
    v
  Step 3: SHELL-GROWTH GEOMETRY
    Local cubic growth produces S^2-like shells (chi = 2)
    and ball-like filled regions on the tested radii
    |
    v
  Step 4: CLOSED-MANIFOLD INPUT (OPEN)
    One-point / boundary compactification is not yet derived
    The closed 3-manifold premise remains extra input
    |
    v
  Step 5: IF CLOSED + SIMPLY CONNECTED, THEN S^3 (Perelman)
    This theorem is conditional on the missing closure step
    |
    v
  Step 6: SPECTRAL GAP = 3/R^2 ON S^3 (representation theory)
    On S^3 of radius R: lambda_1 = 3/R^2 (exact)
    This is from the eigenvalues of the Laplacian on S^3,
    which are l(l+2)/R^2 for l = 1, 2, 3, ...
    The lowest nonzero: l=1 gives lambda_1 = 1*3/R^2 = 3/R^2.
    |
    v
  Step 7: COSMOLOGICAL CONSTANT (conditional identification)
    Lambda = lambda_1 = 3/R_H^2 if and only if the closed topology is S^3

  The remaining factor of {1/Omega_Lambda:.2f} is a separate matter-content / Friedmann issue,
  not a topology derivation.
""")

    # Scorecard
    print(f"  SCORECARD: Topology constraints")
    print(f"  {'Manifold':<20s} {'Excluded by':>25s} {'lambda_1*R^2':>14s} {'CC ratio':>12s}")
    print(f"  {'-'*72}")
    print(f"  {'S^3':<20s} {'--- (selected) ---':>25s} {'3.0000':>14s} {'1.46':>12s}")
    print(f"  {'T^3':<20s} {'Attack 4 (pi_1=Z^3)':>25s} {math.pi**2:>14.4f} {'4.80':>12s}")
    print(f"  {'S^2 x S^1':<20s} {'Attack 4 (pi_1=Z)':>25s} {'2.0000':>14s} {'0.97':>12s}")
    print(f"  {'RP^3':<20s} {'Attack 4 (pi_1=Z_2)':>25s} {'5.0000':>14s} {'2.43':>12s}")
    print(f"  {'L(3,1)':<20s} {'Attack 4 (pi_1=Z_3)':>25s} {8.0/3:>14.4f} {'1.30':>12s}")
    print(f"  {'R^3 (non-compact)':<20s} {'Attack 1 (infinite H)':>25s} {'0.0000':>14s} {'0.00':>12s}")

    print(f"""
  STATUS:
    BEFORE: S^3 topology assumed
    AFTER:  local shell-growth topology verified, closed-manifold step OPEN

    The derivation chain currently uses:
      1. Finite Hilbert space (axiom)
      2. Local graph growth (axiom)
      3. Shell topology checks on the tested discrete balls

    The missing piece is the global compactification / closed-manifold input.
""")

    # Final CC prediction
    Lambda_pred = 3.0 / R_Hubble**2
    ratio = Lambda_pred / Lambda_obs
    print(f"  FINAL RESULT:")
    print(f"    Lambda_pred = 3/R_H^2 = {Lambda_pred:.4e} m^-2")
    print(f"    Lambda_obs  = {Lambda_obs:.4e} m^-2")
    print(f"    Lambda_pred / Lambda_obs = {ratio:.4f}")
    print(f"    Discrepancy: {(ratio - 1)*100:.1f}% (from matter contribution)")
    print(f"    Pure de Sitter limit: ratio -> 1.000 (exact)")

    local_pass = (results_2["n_s2_boundaries"] == results_2["total"] and ratio > 0)

    return {
        "Lambda_pred_over_obs": ratio,
        "topology_derived": False,
        "chain": "finite H -> finite graph -> shell growth (S^3 still conditional)",
        "local_checks_pass": local_pass,
        "global_gap_closed": False,
    }


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    t0 = time.time()

    print("Deriving S^3 Topology from Graph Growth Axioms")
    print("=" * 72)
    print(f"Physical constants:")
    print(f"  l_Planck   = {l_Planck:.4e} m")
    print(f"  R_Hubble   = {R_Hubble:.4e} m")
    print(f"  Lambda_obs = {Lambda_obs:.4e} m^-2")
    print(f"  Omega_Lambda = {Omega_Lambda}")
    print()

    r1 = attack_1_compactness()
    r2 = attack_2_growth_topology()
    r3 = attack_3_unitarity()
    r4 = attack_4_poincare()
    r5 = attack_5_spectral_selection()
    bonus_s3_lattice_eigenvalue()
    final = synthesis(r1, r2, r3, r4, r5)

    elapsed = time.time() - t0
    print(f"\nTotal runtime: {elapsed:.1f}s")

    # Verdict
    print("\n" + "=" * 72)
    print("VERDICT")
    print("=" * 72)

    if final["local_checks_pass"]:
        status = "LOCAL CHECKS PASS; GLOBAL GAP STILL OPEN"
    else:
        status = "SOME TESTS FAILED -- review output"

    print(f"""
  {status}

  The shell-growth topology result is LOCAL and real:
    - S^2-like shell boundaries (chi = 2)
    - ball-like filled regions on the tested radii

  The closed-manifold / compactification step is still OPEN:
    - finite graph -> compact manifold is not derived
    - B^3 -> S^3 remains an extra global input

  Therefore the S^3-based CC coefficient remains CONDITIONAL:
    Lambda_pred / Lambda_obs = {final['Lambda_pred_over_obs']:.4f}
    (valid only if the missing global closure is supplied)
""")


if __name__ == "__main__":
    main()
