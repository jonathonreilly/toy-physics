#!/usr/bin/env python3
"""
S^3 Boundary-Link Disk Theorem: Computational Verification for All R
=====================================================================

STATUS: EXACT (all tests exact, no bounded claims)

PURPOSE:
  Prove computationally for R=2..10 that every boundary-vertex link
  link(v, B_R) is a PL 2-disk, and verify ALL four properties that the
  general-R theorem (S3_BOUNDARY_LINK_THEOREM_NOTE.md) establishes:

    (P1) Connected
    (P2) Simply connected (H_1 = 0, equivalently pi_1 = 0)
    (P3) Has nonempty boundary (proper subcomplex of the octahedral S^2)
    (P4) chi = 1

  Together: connected + simply connected + nonempty boundary + subset of S^2
  => PL 2-disk by the classification of compact surfaces with boundary.

  This script provides computational evidence supporting the general-R proof.
  The proof itself is purely combinatorial and holds for all R >= 2.

THEOREM (proved in S3_BOUNDARY_LINK_THEOREM_NOTE.md):
  For every R >= 2 and every boundary vertex v of B_R,
  link(v, B_R) is a PL 2-disk.

PROOF STRATEGY (general R, no citation needed):
  (a) B_R is a full cubical subcomplex of Z^3 (convex by construction)
  (b) link(v, Z^3) = octahedron boundary = PL S^2 (6 verts, 8 tris)
  (c) link(v, B_R) = subcomplex of link(v, Z^3) induced by neighbors in B_R
  (d) Convexity of B_R => the "present" octahedral triangles form a
      connected, simply connected proper subset of S^2
  (e) Connected + simply connected + has boundary + subset of S^2
      => PL 2-disk (classification of compact surfaces with boundary)

PStack experiment: frontier-s3-boundary-link-theorem
Self-contained: numpy only.
"""

from __future__ import annotations
import sys
import time
from collections import defaultdict, deque

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0
EXACT_COUNT = 0
BOUNDED_COUNT = 0


def check(name: str, condition: bool, detail: str = "",
          check_type: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT, EXACT_COUNT, BOUNDED_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
        if check_type == "EXACT":
            EXACT_COUNT += 1
        else:
            BOUNDED_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f"[{status}] [{check_type}]"
    msg = f"  {tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# Infrastructure: cubical ball, vertex classification, link computation
# =============================================================================

def cubical_ball(R: int) -> tuple[set, set]:
    """
    Build cubical ball B_R: union of all unit cubes whose 8 corners lie
    within Euclidean distance R of origin.
    Returns (vertex_set, cube_set_by_min_corner).
    """
    euc_sites = set()
    for x in range(-R - 1, R + 2):
        for y in range(-R - 1, R + 2):
            for z in range(-R - 1, R + 2):
                if x * x + y * y + z * z <= R * R:
                    euc_sites.add((x, y, z))
    cubes = set()
    for s in euc_sites:
        x, y, z = s
        corners = [(x + dx, y + dy, z + dz)
                    for dx in (0, 1) for dy in (0, 1) for dz in (0, 1)]
        if all(c in euc_sites for c in corners):
            cubes.add(s)
    cb_sites = set()
    for cube in cubes:
        x, y, z = cube
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    cb_sites.add((x + dx, y + dy, z + dz))
    return cb_sites, cubes


def classify_vertices(sites: set) -> tuple[set, set]:
    """Interior vs boundary vertices of B_R."""
    interior, boundary = set(), set()
    for v in sites:
        x, y, z = v
        is_int = all(
            (x + dx, y + dy, z + dz) in sites
            for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)
            if not (dx == 0 and dy == 0 and dz == 0)
        )
        (interior if is_int else boundary).add(v)
    return interior, boundary


def vertex_link_BR(v: tuple, sites: set) -> tuple[list, list, list]:
    """
    Compute link(v, B_R) as a subcomplex of the octahedral link(v, Z^3).

    In Z^3, link(v) has:
      - 6 vertices: the 6 axis-aligned neighbors (+/-x, +/-y, +/-z)
      - 12 edges: pairs of orthogonal axis-neighbors sharing a face-diagonal
      - 8 triangles: triples of mutually orthogonal axis-neighbors sharing a
        cube (one from each axis pair)

    link(v, B_R) is the INDUCED subcomplex: keep only those vertices (axis
    neighbors) that lie in B_R, and keep only edges/triangles whose ALL
    vertices are present.  Additionally, an edge (d1,d2) requires the
    face-diagonal vertex v+d1+d2 to be in B_R (it witnesses the square face),
    and a triangle (d1,d2,d3) requires ALL 7 other cube corners to be in B_R.

    Returns (link_verts_as_dirs, link_edges_as_index_pairs, link_tris_as_index_triples).
    """
    x, y, z = v
    # The 6 possible axis directions
    axis_dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
                 (0, 0, 1), (0, 0, -1)]

    # Vertices of link(v, B_R): axis neighbors that are in B_R
    link_verts = [d for d in axis_dirs
                  if (x + d[0], y + d[1], z + d[2]) in sites]

    # Edges: pairs of orthogonal directions whose face-diagonal is in B_R
    link_edges = []
    for i, d1 in enumerate(link_verts):
        for j, d2 in enumerate(link_verts):
            if j <= i:
                continue
            # Must be orthogonal (non-opposite, non-parallel)
            if sum(d1[k] * d2[k] for k in range(3)) != 0:
                continue
            # Face-diagonal vertex must be in B_R
            corner = (x + d1[0] + d2[0], y + d1[1] + d2[1],
                      z + d1[2] + d2[2])
            if corner in sites:
                link_edges.append((i, j))

    # Triangles: triples of mutually orthogonal directions whose cube is in B_R
    link_tris = []
    for i, d1 in enumerate(link_verts):
        for j, d2 in enumerate(link_verts):
            if j <= i:
                continue
            for k, d3 in enumerate(link_verts):
                if k <= j:
                    continue
                dot12 = sum(d1[l] * d2[l] for l in range(3))
                dot13 = sum(d1[l] * d3[l] for l in range(3))
                dot23 = sum(d2[l] * d3[l] for l in range(3))
                if dot12 != 0 or dot13 != 0 or dot23 != 0:
                    continue
                # All 7 other cube-corner vertices must be in B_R
                pts = [
                    (x + d1[0], y + d1[1], z + d1[2]),
                    (x + d2[0], y + d2[1], z + d2[2]),
                    (x + d3[0], y + d3[1], z + d3[2]),
                    (x + d1[0] + d2[0], y + d1[1] + d2[1],
                     z + d1[2] + d2[2]),
                    (x + d1[0] + d3[0], y + d1[1] + d3[1],
                     z + d1[2] + d3[2]),
                    (x + d2[0] + d3[0], y + d2[1] + d3[1],
                     z + d2[2] + d3[2]),
                    (x + d1[0] + d2[0] + d3[0],
                     y + d1[1] + d2[1] + d3[1],
                     z + d1[2] + d2[2] + d3[2]),
                ]
                if all(p in sites for p in pts):
                    link_tris.append((i, j, k))

    return link_verts, link_edges, link_tris


# =============================================================================
# Topological analysis of a 2-complex
# =============================================================================

def analyze_2complex(n_verts: int, edges: list, triangles: list) -> dict:
    """
    Full topological analysis of a 2-complex.
    Returns chi, connectivity, boundary info, H_1 rank, orientability, type.
    """
    V = n_verts
    E = len(edges)
    F = len(triangles)
    chi = V - E + F

    if V == 0:
        return {"chi": 0, "V": 0, "E": 0, "F": 0, "type": "empty",
                "connected": False, "is_closed": False,
                "has_boundary": False, "H1": 0, "orientable": False,
                "n_boundary_edges": 0, "n_boundary_components": 0}

    # --- Connectivity ---
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    visited = {0}
    queue = deque([0])
    while queue:
        node = queue.popleft()
        for nb in adj[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    connected = len(visited) == V

    # --- Boundary detection ---
    edge_tri_count = defaultdict(int)
    for tri in triangles:
        for a, b in [(tri[0], tri[1]), (tri[0], tri[2]), (tri[1], tri[2])]:
            ek = (min(a, b), max(a, b))
            edge_tri_count[ek] += 1

    boundary_edges = [e for e, c in edge_tri_count.items() if c == 1]
    bad_edges = [e for e, c in edge_tri_count.items() if c > 2]
    is_closed = len(boundary_edges) == 0 and len(bad_edges) == 0
    has_boundary = len(boundary_edges) > 0

    # Count boundary components
    n_boundary_components = 0
    if boundary_edges:
        bd_adj = defaultdict(set)
        for a, b in boundary_edges:
            bd_adj[a].add(b)
            bd_adj[b].add(a)
        bd_visited = set()
        for e in boundary_edges:
            start = e[0]
            if start not in bd_visited:
                n_boundary_components += 1
                bq = deque([start])
                bd_visited.add(start)
                while bq:
                    node = bq.popleft()
                    for nb in bd_adj[node]:
                        if nb not in bd_visited:
                            bd_visited.add(nb)
                            bq.append(nb)

    # --- H_1 via boundary matrix rank (Z_2 coefficients) ---
    # H_1 = rank(ker d_1) - rank(im d_2)
    # = (E - rank(d_1)) - rank(d_2)
    # where d_1: C_1 -> C_0, d_2: C_2 -> C_1

    # Build d_1 (E x V matrix over Z_2) and d_2 (E x F matrix over Z_2)
    # Use numpy for rank computation over Z_2 (mod 2 Gaussian elimination)
    edge_index = {}
    for idx, (i, j) in enumerate(edges):
        ek = (min(i, j), max(i, j))
        edge_index[ek] = idx

    # d_2: boundary of triangles -> edges (over Z_2)
    if F > 0 and E > 0:
        d2 = np.zeros((E, F), dtype=np.int32)
        for fi, tri in enumerate(triangles):
            for a, b in [(tri[0], tri[1]), (tri[0], tri[2]), (tri[1], tri[2])]:
                ek = (min(a, b), max(a, b))
                if ek in edge_index:
                    d2[edge_index[ek], fi] = 1
        rank_d2 = _z2_rank(d2)
    else:
        rank_d2 = 0

    # d_1: boundary of edges -> vertices (over Z_2)
    if E > 0:
        d1 = np.zeros((V, E), dtype=np.int32)
        for ei, (i, j) in enumerate(edges):
            d1[i, ei] = 1
            d1[j, ei] = 1
        rank_d1 = _z2_rank(d1)
    else:
        rank_d1 = 0

    H1 = (E - rank_d1) - rank_d2

    # --- Orientability check ---
    orientable = False
    edge_to_tris = defaultdict(list)
    for idx, tri in enumerate(triangles):
        for a, b in [(tri[0], tri[1]), (tri[0], tri[2]), (tri[1], tri[2])]:
            ek = (min(a, b), max(a, b))
            edge_to_tris[ek].append(idx)

    if len(bad_edges) == 0 and F > 0:
        orientation = [0] * F
        orientation[0] = 1
        orient_queue = deque([0])
        orient_ok = True
        while orient_queue and orient_ok:
            ti = orient_queue.popleft()
            tri = triangles[ti]
            for a, b in [(tri[0], tri[1]), (tri[1], tri[2]),
                         (tri[0], tri[2])]:
                ek = (min(a, b), max(a, b))
                for tj in edge_to_tris[ek]:
                    if tj == ti:
                        continue

                    def edge_sign(tri_verts, va, vb):
                        idx_a = list(tri_verts).index(va) if va in tri_verts else -1
                        idx_b = list(tri_verts).index(vb) if vb in tri_verts else -1
                        if idx_a < 0 or idx_b < 0:
                            return 0
                        return +1 if (idx_b - idx_a) % 3 == 1 else -1

                    sign_i = edge_sign(list(triangles[ti]), a, b) * orientation[ti]
                    raw_j = edge_sign(list(triangles[tj]), a, b)
                    if raw_j == 0:
                        continue
                    needed_orient = -sign_i
                    req = needed_orient * raw_j

                    if orientation[tj] == 0:
                        orientation[tj] = req
                        orient_queue.append(tj)
                    elif orientation[tj] != req:
                        orient_ok = False
                        break
        orientable = orient_ok and all(o != 0 for o in orientation)

    # --- Classification ---
    if is_closed and connected and chi == 2 and orientable:
        ctype = "S^2"
    elif (has_boundary and connected and chi == 1 and len(bad_edges) == 0
          and n_boundary_components == 1 and H1 == 0):
        ctype = "disk"
    else:
        ctype = f"other(chi={chi},H1={H1},bd={n_boundary_components})"

    return {"chi": chi, "V": V, "E": E, "F": F, "type": ctype,
            "connected": connected, "is_closed": is_closed,
            "has_boundary": has_boundary, "H1": H1,
            "orientable": orientable,
            "n_boundary_edges": len(boundary_edges),
            "n_bad_edges": len(bad_edges),
            "n_boundary_components": n_boundary_components}


def _z2_rank(M: np.ndarray) -> int:
    """Compute rank of matrix M over Z_2 (GF(2)) via Gaussian elimination."""
    A = M.copy() % 2
    rows, cols = A.shape
    rank = 0
    for col in range(cols):
        # Find pivot
        pivot = None
        for row in range(rank, rows):
            if A[row, col] % 2 == 1:
                pivot = row
                break
        if pivot is None:
            continue
        # Swap
        A[[rank, pivot]] = A[[pivot, rank]]
        # Eliminate
        for row in range(rows):
            if row != rank and A[row, col] % 2 == 1:
                A[row] = (A[row] + A[rank]) % 2
        rank += 1
    return rank


# =============================================================================
# Main verification
# =============================================================================

def verify_boundary_link_disk(R: int) -> tuple[int, int]:
    """
    For cubical ball B_R, verify that every boundary vertex link is a PL 2-disk.
    Returns (n_pass, n_fail).
    """
    sites, cubes = cubical_ball(R)
    interior, boundary = classify_vertices(sites)

    print(f"\n{'='*70}")
    print(f"  R = {R}:  |B_R| = {len(sites)} vertices, "
          f"{len(interior)} interior, {len(boundary)} boundary")
    print(f"{'='*70}")

    n_pass = 0
    n_fail = 0

    # Group boundary vertices by their link type for compact reporting
    type_counts = defaultdict(int)
    type_examples = {}

    for v in sorted(boundary):
        verts, edges, tris = vertex_link_BR(v, sites)
        info = analyze_2complex(len(verts), edges, tris)

        key = (info["type"], info["chi"], info["H1"],
               info["connected"], info["has_boundary"],
               info["n_boundary_components"])
        type_counts[key] += 1
        if key not in type_examples:
            type_examples[key] = (v, info)

        if info["type"] == "disk":
            n_pass += 1
        else:
            n_fail += 1

    # Report by type
    for key, count in sorted(type_counts.items()):
        v_ex, info_ex = type_examples[key]
        tp, chi, H1, conn, has_bd, n_bd = key
        print(f"  Type: {tp}  (count={count})  "
              f"chi={chi}, H1={H1}, conn={conn}, bd={has_bd}, "
              f"bd_components={n_bd}  "
              f"example: {v_ex}")

    # Four property checks
    all_connected = True
    all_H1_zero = True
    all_has_boundary = True
    all_chi_one = True
    all_disk = True
    for v in boundary:
        verts, edges, tris = vertex_link_BR(v, sites)
        info = analyze_2complex(len(verts), edges, tris)
        if not info["connected"]:
            all_connected = False
        if info["H1"] != 0:
            all_H1_zero = False
        if not info["has_boundary"]:
            all_has_boundary = False
        if info["chi"] != 1:
            all_chi_one = False
        if info["type"] != "disk":
            all_disk = False

    check(f"R={R} P1: all boundary links connected",
          all_connected, f"{len(boundary)} boundary vertices")
    check(f"R={R} P2: all boundary links simply connected (H1=0)",
          all_H1_zero, f"{len(boundary)} boundary vertices")
    check(f"R={R} P3: all boundary links have nonempty boundary",
          all_has_boundary, f"{len(boundary)} boundary vertices")
    check(f"R={R} P4: all boundary links have chi=1",
          all_chi_one, f"{len(boundary)} boundary vertices")
    check(f"R={R} CONCLUSION: all boundary links are PL 2-disks",
          all_disk, f"{n_pass}/{n_pass + n_fail} pass")

    return n_pass, n_fail


def main():
    t0 = time.time()
    print("=" * 70)
    print("  S^3 BOUNDARY-LINK DISK THEOREM: COMPUTATIONAL VERIFICATION")
    print("=" * 70)
    print()
    print("  Theorem: For all R >= 2, every boundary vertex v of B_R has")
    print("           link(v, B_R) = PL 2-disk.")
    print()
    print("  Verification: R = 2..10, checking P1-P4 for each boundary vertex.")
    print()
    print("  P1: Connected")
    print("  P2: Simply connected (H_1 = 0)")
    print("  P3: Has nonempty boundary")
    print("  P4: chi = 1")
    print("  => PL 2-disk by classification of compact surfaces with boundary")
    print()

    R_range = range(2, 11)  # R = 2..10
    total_boundary = 0
    total_pass = 0
    total_fail = 0

    for R in R_range:
        n_pass, n_fail = verify_boundary_link_disk(R)
        total_pass += n_pass
        total_fail += n_fail
        total_boundary += n_pass + n_fail

    elapsed = time.time() - t0

    print()
    print("=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"  R range:         {R_range.start}..{R_range.stop - 1}")
    print(f"  Total boundary:  {total_boundary} vertices")
    print(f"  All disk:        {total_pass}/{total_boundary}")
    print(f"  Failures:        {total_fail}")
    print()
    print(f"  PASS: {PASS_COUNT}   FAIL: {FAIL_COUNT}")
    print(f"  EXACT: {EXACT_COUNT}   BOUNDED: {BOUNDED_COUNT}")
    print(f"  Time: {elapsed:.1f}s")
    print()

    if FAIL_COUNT == 0:
        print("  RESULT: ALL BOUNDARY LINKS ARE PL 2-DISKS (R=2..10)")
        print()
        print("  This computational evidence supports the general-R theorem:")
        print("  For every R >= 2 and every boundary vertex v of B_R,")
        print("  link(v, B_R) is a PL 2-disk.")
        print()
        print("  The theorem proof (see S3_BOUNDARY_LINK_THEOREM_NOTE.md)")
        print("  is purely combinatorial and requires no external citation.")
    else:
        print("  *** FAILURES DETECTED ***")

    sys.exit(0 if FAIL_COUNT == 0 else 1)


if __name__ == "__main__":
    main()
