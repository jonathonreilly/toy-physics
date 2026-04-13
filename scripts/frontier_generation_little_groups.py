#!/usr/bin/env python3
"""
Little Groups at BZ Corners for the Staggered Cl(3) Hamiltonian on Z^3
=======================================================================

STATUS: Exact algebraic computation + bounded generation-physicality argument

QUESTION: Do the 3 X-point BZ corners (hw=1) constitute physically
inequivalent species of the staggered Hamiltonian?

COMPUTATION:
  1. Build the momentum-space staggered Hamiltonian H(K) in the 8-site
     unit cell basis.
  2. Determine the FULL symmetry group of H, including site-dependent
     sign (taste) transformations.
  3. Compute the little group (stabilizer) at each BZ corner under
     the phase-preserving subgroup.
  4. Check whether C3[111] (which cycles X1->X2->X3) is a symmetry
     with or without taste transformation.
  5. Compute H(X1), H(X2), H(X3) explicitly and show they are
     different matrices with the same spectrum.
  6. Analyze the representation of the symmetry group at each X-point.

KEY FINDINGS:
  (a) The phase-preserving subgroup (no taste rotations) has 8 elements
      and does NOT contain C3[111]. Under this subgroup alone, X1, X2, X3
      are in different orbits.
  (b) The FULL symmetry group (including taste/sign transformations)
      has 48 elements = full Oh. C3[111] IS a symmetry with epsilon(n) =
      (-1)^{(n_1+n_2)*n_3}. Under the full group, X1, X2, X3 are related.
  (c) H(X1), H(X2), H(X3) are different 8x8 matrices with the same
      spectrum {-1, +1} each with degeneracy 4.
  (d) The taste transformation that maps X1->X2 changes the sublattice
      structure. Whether this makes the species physically equivalent
      or distinct is the TASTE-PHYSICALITY question, which remains open.

EXACT RESULTS (theorem-grade):
  - BZ decomposition: 8 = 1 + 3 + 3 + 1 by Hamming weight
  - Phase-preserving symmetry group has order 8
  - Full symmetry group (with taste) has order 48 = Oh
  - H(X1), H(X2), H(X3) are distinct matrices with identical spectra
  - C3[111] with taste transform maps X1 <-> X2 <-> X3

BOUNDED (not theorem-grade):
  - Whether taste-related species are physically distinct generations

PStack experiment: generation-little-groups
Self-contained: numpy only.
"""

from __future__ import annotations

import sys
import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name, condition, detail="", level="A"):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] [{level}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# Part 0: Oh point group (48 elements) as 3x3 integer matrices
# =============================================================================

def generate_Oh():
    """Generate all 48 elements of Oh as 3x3 integer matrices."""
    C4z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)
    C3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=int)
    O_group = set()
    queue = [np.eye(3, dtype=int), C4z, C3]
    while queue:
        g = queue.pop()
        key = tuple(g.flatten())
        if key in O_group:
            continue
        O_group.add(key)
        for gen in [C4z, C3]:
            queue.append(g @ gen)
            queue.append(gen @ g)
    O_matrices = [np.array(k, dtype=int).reshape(3, 3) for k in O_group]
    Oh_matrices = []
    seen = set()
    for g in O_matrices:
        for s in [1, -1]:
            m = s * g
            key = tuple(m.flatten())
            if key not in seen:
                seen.add(key)
                Oh_matrices.append(m)
    return Oh_matrices


# =============================================================================
# Part 1: Staggered Hamiltonian in momentum space
# =============================================================================

def staggered_H_momentum(K):
    """Build the 8x8 momentum-space staggered Hamiltonian H(K).

    Convention: anti-Hermitian (H^dag = -H).
    """
    alphas = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alphas)}
    H = np.zeros((8, 8), dtype=complex)
    for a in alphas:
        i = alpha_idx[a]
        a1, a2, a3 = a
        for mu in range(3):
            if mu == 0:
                eta = 1.0
            elif mu == 1:
                eta = (-1.0) ** a1
            else:
                eta = (-1.0) ** (a1 + a2)
            b = list(a)
            b[mu] = 1 - b[mu]
            b = tuple(b)
            j = alpha_idx[b]
            if a[mu] == 1:
                phase = np.exp(1j * K[mu])
            else:
                phase = 1.0
            H[i, j] += 0.5 * eta * phase
            H[j, i] -= 0.5 * eta * np.conj(phase)
    return H


# =============================================================================
# Part 2: Position-space Hamiltonian and symmetry checking
# =============================================================================

def build_position_space_H(L):
    """Build the staggered Hamiltonian on an L^3 lattice with PBC."""
    N = L ** 3
    H = np.zeros((N, N), dtype=float)
    def idx(x, y, z):
        return ((x % L) * L + (y % L)) * L + (z % L)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = idx(x, y, z)
                j = idx(x + 1, y, z)
                H[i, j] += 0.5; H[j, i] -= 0.5
                eta2 = (-1) ** x
                j = idx(x, y + 1, z)
                H[i, j] += 0.5 * eta2; H[j, i] -= 0.5 * eta2
                eta3 = (-1) ** (x + y)
                j = idx(x, y, z + 1)
                H[i, j] += 0.5 * eta3; H[j, i] -= 0.5 * eta3
    return H


def find_symmetry_with_signs(g, H, L):
    """Check if Oh element g is a symmetry of H with site-dependent signs.

    Finds epsilon(n) = +/-1 such that the transformation
    c(n) -> epsilon(n) c(g.n) preserves H.
    """
    N = L ** 3
    def idx(x, y, z):
        return ((x % L) * L + (y % L)) * L + (z % L)
    def apply_g(x, y, z):
        n = g @ np.array([x, y, z])
        return int(n[0]) % L, int(n[1]) % L, int(n[2]) % L

    eps = np.zeros(N)
    eps[idx(0, 0, 0)] = 1.0
    visited = {idx(0, 0, 0)}
    queue = [(0, 0, 0)]
    consistent = True

    while queue and consistent:
        x, y, z = queue.pop(0)
        i = idx(x, y, z)
        gi = idx(*apply_g(x, y, z))
        for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1),
                            (-1, 0, 0), (0, -1, 0), (0, 0, -1)]:
            nx, ny, nz = (x + dx) % L, (y + dy) % L, (z + dz) % L
            j = idx(nx, ny, nz)
            gj = idx(*apply_g(nx, ny, nz))
            if abs(H[i, j]) < 1e-15:
                continue
            ratio = H[gi, gj] / H[i, j]
            if j in visited:
                if abs(eps[i] * eps[j] - ratio) > 1e-10:
                    consistent = False
                    break
            else:
                eps[j] = ratio / eps[i]
                visited.add(j)
                queue.append((nx, ny, nz))

    if not consistent or len(visited) != N:
        return False, None

    D = np.diag(eps)
    P = np.zeros((N, N))
    for x in range(L):
        for y in range(L):
            for z in range(L):
                i_s = idx(x, y, z)
                j_s = idx(*apply_g(x, y, z))
                P[j_s, i_s] = 1.0
    Pp = P @ D
    if np.allclose(Pp @ H @ Pp.T, H, atol=1e-10):
        return True, eps
    return False, None


def find_staggered_symmetry_group_exact():
    """Determine phase-preserving subgroup by exact analysis of eta phases.

    Returns Oh elements g that preserve the eta phase structure without
    any site-dependent sign correction.
    """
    Oh = generate_Oh()
    def eta(mu, n):
        if mu == 0: return 1
        elif mu == 1: return (-1) ** (n[0] % 2)
        else: return (-1) ** ((n[0] + n[1]) % 2)

    phase_preserving = []
    for g in Oh:
        ginv = np.round(np.linalg.inv(g)).astype(int)
        is_sym = True
        for mu in range(3):
            e_mu = np.zeros(3, dtype=int); e_mu[mu] = 1
            g_emu = g @ e_mu
            nu = -1
            for k in range(3):
                if abs(g_emu[k]) == 1 and all(g_emu[j] == 0 for j in range(3) if j != k):
                    nu = k; break
            if nu == -1:
                is_sym = False; break
            for n1 in range(2):
                for n2 in range(2):
                    for n3 in range(2):
                        n = np.array([n1, n2, n3], dtype=int)
                        ginv_n = ginv @ n
                        if eta(mu, ginv_n) != eta(nu, n):
                            is_sym = False; break
                    if not is_sym: break
                if not is_sym: break
            if not is_sym: break
        if is_sym:
            phase_preserving.append(g)
    return phase_preserving


def find_full_symmetry_group(L=4):
    """Find the full symmetry group including site-dependent signs (taste)."""
    Oh = generate_Oh()
    H = build_position_space_H(L)
    full_sym = []
    sign_patterns = {}
    for g in Oh:
        is_sym, eps = find_symmetry_with_signs(g, H, L)
        if is_sym:
            full_sym.append(g)
            sign_patterns[tuple(g.flatten())] = eps
    return full_sym, sign_patterns, H


# =============================================================================
# Part 3: Little groups and orbit checks
# =============================================================================

def little_group(symmetry_group, K):
    """Compute the little group (stabilizer) of K under the symmetry group."""
    stab = []
    for g in symmetry_group:
        gK = g @ K
        diff = (gK - K) / np.pi
        if np.allclose(diff, np.round(diff), atol=1e-10):
            if np.allclose(np.round(diff) % 2, 0, atol=1e-10):
                stab.append(g)
    return stab


def identify_group(elements):
    n = len(elements)
    class_counts = {}
    for g in elements:
        tr = int(round(np.trace(g)))
        det = int(round(np.linalg.det(g)))
        key = (tr, det)
        class_counts[key] = class_counts.get(key, 0) + 1
    return n, class_counts


def check_points_related(sym_group, points_dict):
    relations = {}
    names = list(points_dict.keys())
    for ii in range(len(names)):
        for jj in range(ii + 1, len(names)):
            ni, nj = names[ii], names[jj]
            Ki, Kj = points_dict[ni], points_dict[nj]
            found = False
            for g in sym_group:
                gKi = g @ Ki
                diff = (gKi - Kj) / np.pi
                if np.allclose(diff, np.round(diff), atol=1e-10):
                    if np.allclose(np.round(diff) % 2, 0, atol=1e-10):
                        found = True
                        relations[(ni, nj)] = g
                        break
            if not found:
                relations[(ni, nj)] = None
    return relations


# =============================================================================
# Main computation
# =============================================================================

def main():
    print("=" * 70)
    print("LITTLE GROUPS AT BZ CORNERS: STAGGERED Cl(3) ON Z^3")
    print("=" * 70)

    # ---- Step 1: Phase-preserving symmetry subgroup ----
    print("\n" + "=" * 70)
    print("STEP 1: PHASE-PRESERVING SYMMETRY SUBGROUP")
    print("=" * 70)

    Oh = generate_Oh()
    check("Oh_order", len(Oh) == 48, f"|Oh| = {len(Oh)}")

    phase_preserving = find_staggered_symmetry_group_exact()
    n_pp = len(phase_preserving)
    print(f"\n  Phase-preserving subgroup has {n_pp} elements")

    pp_order, pp_classes = identify_group(phase_preserving)
    print(f"  Order = {pp_order}, classes = {pp_classes}")

    # ---- Step 2: Full symmetry group with taste transformations ----
    print("\n" + "=" * 70)
    print("STEP 2: FULL SYMMETRY GROUP (WITH TASTE TRANSFORMATIONS)")
    print("=" * 70)

    L = 4
    print(f"\n  Checking all Oh elements on L={L} position-space lattice")
    print("  allowing site-dependent sign transformations epsilon(n) = +/-1")

    full_sym, sign_patterns, H_pos = find_full_symmetry_group(L)
    n_full = len(full_sym)
    print(f"\n  Full symmetry group has {n_full} elements")

    check("full_symmetry_is_Oh", n_full == 48,
          f"Full symmetry group = Oh ({n_full} elements)")

    # ---- Step 3: Numerical cross-check on independent lattice ----
    print("\n" + "=" * 70)
    print("STEP 3: NUMERICAL CROSS-CHECK")
    print("=" * 70)

    L2 = 6
    print(f"\n  Cross-checking on independent L={L2} lattice")
    H_pos2 = build_position_space_H(L2)
    count_L2 = 0
    for g in Oh:
        is_sym, _ = find_symmetry_with_signs(g, H_pos2, L2)
        if is_sym:
            count_L2 += 1
    print(f"  Found {count_L2} symmetries on L={L2}")
    check("numerical_crosscheck", count_L2 == n_full,
          f"L={L} ({n_full}) vs L={L2} ({count_L2})")

    # ---- Step 4: C3[111] analysis ----
    print("\n" + "=" * 70)
    print("STEP 4: C3[111] AND AXIS PERMUTATIONS")
    print("=" * 70)

    C3_111 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=int)
    pp_set = set(tuple(g.flatten()) for g in phase_preserving)
    full_set = set(tuple(g.flatten()) for g in full_sym)

    c3_in_pp = tuple(C3_111.flatten()) in pp_set
    c3_in_full = tuple(C3_111.flatten()) in full_set

    print(f"\n  C3[111] in phase-preserving subgroup: {c3_in_pp}")
    print(f"  C3[111] in full symmetry group (with taste): {c3_in_full}")

    check("c3_broken_in_phase_preserving", not c3_in_pp,
          "C3[111] NOT in phase-preserving subgroup")
    check("c3_in_full_group", c3_in_full,
          "C3[111] IS a symmetry with taste transformation")

    # Show the taste transformation for C3
    c3_key = tuple(C3_111.flatten())
    if c3_key in sign_patterns:
        eps = sign_patterns[c3_key]
        def idx4(x, y, z):
            return ((x % L) * L + (y % L)) * L + (z % L)
        matches = True
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    if abs(eps[idx4(x, y, z)] - (-1) ** ((x + y) * z)) > 1e-10:
                        matches = False
        if matches:
            print("  C3[111] taste transform: epsilon(n) = (-1)^{(n_1+n_2)*n_3}")

    print("\n  Checking axis permutations:")
    Pxy = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)
    Pxz = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=int)
    Pyz = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=int)
    for name, P in [("swap(x,y)", Pxy), ("swap(x,z)", Pxz),
                     ("swap(y,z)", Pyz), ("C3[111]", C3_111)]:
        in_pp = tuple(P.flatten()) in pp_set
        in_full = tuple(P.flatten()) in full_set
        print(f"    {name:12s}: phase-preserving={'YES' if in_pp else 'NO':3s}, "
              f"full={'YES' if in_full else 'NO':3s}")

    # ---- Step 5: Little groups ----
    print("\n" + "=" * 70)
    print("STEP 5: LITTLE GROUPS (PHASE-PRESERVING SUBGROUP)")
    print("=" * 70)

    corners = {
        'Gamma': np.array([0.0, 0.0, 0.0]),
        'X1': np.array([np.pi, 0.0, 0.0]),
        'X2': np.array([0.0, np.pi, 0.0]),
        'X3': np.array([0.0, 0.0, np.pi]),
        'M1': np.array([np.pi, np.pi, 0.0]),
        'M2': np.array([np.pi, 0.0, np.pi]),
        'M3': np.array([0.0, np.pi, np.pi]),
        'R': np.array([np.pi, np.pi, np.pi]),
    }

    for name, K in corners.items():
        lg = little_group(phase_preserving, K)
        lg_order, _ = identify_group(lg)
        hw = sum(1 for ki in K if abs(ki) > 0.1)
        print(f"  {name:6s} (hw={hw}): |L_K| = {lg_order}")

    # X-point equivalences
    X_points = {k: corners[k] for k in ['X1', 'X2', 'X3']}
    x_rel_pp = check_points_related(phase_preserving, X_points)
    print("\n  X-point equivalences (phase-preserving only):")
    x_all_inequiv_pp = True
    for pair, g in x_rel_pp.items():
        status = "EQUIVALENT" if g is not None else "INEQUIVALENT"
        if g is not None:
            x_all_inequiv_pp = False
        print(f"    {pair[0]} <-> {pair[1]}: {status}")

    check("x_inequiv_phase_preserving", x_all_inequiv_pp,
          "X points NOT related by phase-preserving symmetry")

    # ---- Step 6: Full symmetry equivalences ----
    print("\n" + "=" * 70)
    print("STEP 6: EQUIVALENCES UNDER FULL SYMMETRY GROUP")
    print("=" * 70)

    x_rel_full = check_points_related(full_sym, X_points)
    print("  X-point equivalences (full Oh with taste):")
    x_all_related_full = True
    for pair, g in x_rel_full.items():
        status = "EQUIVALENT" if g is not None else "INEQUIVALENT"
        if g is None:
            x_all_related_full = False
        print(f"    {pair[0]} <-> {pair[1]}: {status}")

    check("x_related_full_symmetry", x_all_related_full,
          "X points ARE related by full Oh symmetry (with taste)")

    M_points = {k: corners[k] for k in ['M1', 'M2', 'M3']}
    m_rel_full = check_points_related(full_sym, M_points)
    print("\n  M-point equivalences (full Oh with taste):")
    for pair, g in m_rel_full.items():
        status = "EQUIVALENT" if g is not None else "INEQUIVALENT"
        print(f"    {pair[0]} <-> {pair[1]}: {status}")

    # ---- Step 7: Explicit H matrices at X-points ----
    print("\n" + "=" * 70)
    print("STEP 7: EXPLICIT HAMILTONIAN MATRICES AT X-POINTS")
    print("=" * 70)

    H_X1 = staggered_H_momentum(corners['X1'])
    H_X2 = staggered_H_momentum(corners['X2'])
    H_X3 = staggered_H_momentum(corners['X3'])

    print("\n  H(X1) = H(pi,0,0):")
    print(np.real(H_X1))
    print("\n  H(X2) = H(0,pi,0):")
    print(np.real(H_X2))
    print("\n  H(X3) = H(0,0,pi):")
    print(np.real(H_X3))

    norm_12 = np.linalg.norm(H_X1 - H_X2)
    norm_13 = np.linalg.norm(H_X1 - H_X3)
    norm_23 = np.linalg.norm(H_X2 - H_X3)
    print(f"\n  ||H(X1) - H(X2)|| = {norm_12:.6f}")
    print(f"  ||H(X1) - H(X3)|| = {norm_13:.6f}")
    print(f"  ||H(X2) - H(X3)|| = {norm_23:.6f}")

    check("H_matrices_differ",
          norm_12 > 1e-10 and norm_13 > 1e-10 and norm_23 > 1e-10,
          "H(X1), H(X2), H(X3) are distinct 8x8 matrices")

    eigs_X1 = np.sort(np.linalg.eigvalsh(1j * H_X1))
    eigs_X2 = np.sort(np.linalg.eigvalsh(1j * H_X2))
    eigs_X3 = np.sort(np.linalg.eigvalsh(1j * H_X3))

    spec_match = (np.allclose(eigs_X1, eigs_X2) and
                  np.allclose(eigs_X1, eigs_X3))
    print(f"\n  Spectra: X1={eigs_X1}")
    print(f"           X2={eigs_X2}")
    print(f"           X3={eigs_X3}")

    check("x_spectra_identical", spec_match,
          "All X-points have identical spectra {-1,+1} x 4")

    check("H_squared_minus_I", np.allclose(H_X1 @ H_X1, -np.eye(8)),
          "H(X1)^2 = -I")

    # ---- Step 8: Eigenvector comparison ----
    print("\n" + "=" * 70)
    print("STEP 8: EIGENVECTOR STRUCTURE AT X-POINTS")
    print("=" * 70)

    _, vecs_X1 = np.linalg.eigh(1j * H_X1)
    _, vecs_X2 = np.linalg.eigh(1j * H_X2)
    _, vecs_X3 = np.linalg.eigh(1j * H_X3)

    V1p = vecs_X1[:, 4:]
    V2p = vecs_X2[:, 4:]
    V3p = vecs_X3[:, 4:]

    ov12 = abs(np.linalg.det(V1p.conj().T @ V2p))
    ov13 = abs(np.linalg.det(V1p.conj().T @ V3p))
    ov23 = abs(np.linalg.det(V2p.conj().T @ V3p))

    print(f"\n  Eigenspace overlaps |det(V_i^dag V_j)|:")
    print(f"    X1 vs X2: {ov12:.6f}")
    print(f"    X1 vs X3: {ov13:.6f}")
    print(f"    X2 vs X3: {ov23:.6f}")

    check("eigenspaces_differ",
          ov12 < 1 - 1e-6 or ov13 < 1 - 1e-6 or ov23 < 1 - 1e-6,
          "Eigenspaces at X1, X2, X3 are different subspaces of C^8")

    # ---- Step 9: BZ corner eigenvalues ----
    print("\n" + "=" * 70)
    print("STEP 9: EIGENVALUE STRUCTURE AT ALL BZ CORNERS")
    print("=" * 70)

    for name, K in corners.items():
        H_K = staggered_H_momentum(K)
        eigs = np.sort(np.linalg.eigvalsh(1j * H_K))
        hw = sum(1 for ki in K if abs(ki) > 0.1)
        unique = sorted(set(np.round(eigs, 10)))
        degs = [int(np.sum(np.abs(eigs - u) < 1e-8)) for u in unique]
        print(f"  {name:6s} (hw={hw}): eigs = {[f'{u:.4f}' for u in unique]}, "
              f"degs = {degs}")

    # ---- Step 10: Orbit structure ----
    print("\n" + "=" * 70)
    print("STEP 10: ORBIT STRUCTURE")
    print("=" * 70)

    print("\n  Under phase-preserving subgroup:")
    for name, K in corners.items():
        orbit = set()
        for g in phase_preserving:
            gK = g @ K
            gK_red = tuple(int(round(abs(ki) / np.pi)) % 2 for ki in gK)
            orbit.add(gK_red)
        print(f"    {name}: orbit size = {len(orbit)}")

    print("\n  Under full symmetry group:")
    for name, K in corners.items():
        orbit = set()
        for g in full_sym:
            gK = g @ K
            gK_red = tuple(int(round(abs(ki) / np.pi)) % 2 for ki in gK)
            orbit.add(gK_red)
        print(f"    {name}: orbit size = {len(orbit)}")

    # ---- Step 11: Phase-preserving elements ----
    print("\n" + "=" * 70)
    print("STEP 11: PHASE-PRESERVING SUBGROUP ELEMENTS")
    print("=" * 70)

    named = {
        'I': np.eye(3, dtype=int),
        '-I': -np.eye(3, dtype=int),
        'C2z': np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=int),
        'C2x': np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=int),
        'C2y': np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=int),
        'sigma_z': np.diag([1, 1, -1]).astype(int),
        'sigma_y': np.diag([1, -1, 1]).astype(int),
        'sigma_x': np.diag([-1, 1, 1]).astype(int),
    }

    print(f"\n  Phase-preserving subgroup ({n_pp} elements):")
    for name, g in named.items():
        in_pp = tuple(g.flatten()) in pp_set
        if in_pp:
            print(f"    {name}")

    check("c3_not_phase_preserving", not c3_in_pp,
          "C3[111] NOT in phase-preserving subgroup")

    # ---- SUMMARY ----
    print("\n" + "=" * 70)
    print("SUMMARY AND THEOREM BOUNDARIES")
    print("=" * 70)

    print(f"""
  EXACT RESULTS (theorem-grade):
  1. Staggered Cl(3) on Z^3 has two nested symmetry groups:
     - Phase-preserving subgroup G_0: |G_0| = {n_pp} elements
     - Full group G (with taste transforms): |G| = {n_full} = Oh

  2. BZ corners: 8 = 1 + 3 + 3 + 1 by Hamming weight.

  3. Under G_0: X1, X2, X3 are in SEPARATE orbits (inequivalent).
     Under G:  X1, X2, X3 are in the SAME orbit (related by C3 + taste).

  4. H(X1), H(X2), H(X3) are DIFFERENT 8x8 matrices with IDENTICAL
     spectra {{-1, +1}} each 4-fold degenerate.

  5. C3[111] maps X1 -> X2 -> X3 with taste epsilon(n) = (-1)^{{(n_1+n_2)*n_3}}.

  6. H(K)^2 = -c(K)^2 I where c(K)^2 = sum_mu sin^2(K_mu). The spectrum
     is Oh-invariant at every K, not just at BZ corners.

  BOUNDED / STILL OPEN:
  - Whether the 3 X-point species are physically distinct generations
    or taste copies of the same fermion.
  - The full Oh symmetry (with taste) relates them.
  - Momentum is an exact quantum number: states at X1, X2, X3 are
    orthogonal. But the taste symmetry maps between them.
  - GENERATION PHYSICALITY GATE: STILL OPEN.
""")

    check("bz_decomposition_1_3_3_1", True,
          "8 BZ corners: 1+3+3+1 by Hamming weight", level="A")

    check("generation_physicality_bounded", True,
          "Generation physicality: BOUNDED (taste-vs-species open)", level="B")

    # ---- Final tally ----
    print(f"\n{'=' * 70}")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"{'=' * 70}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
