"""
Cl(3) -> KS symmetric 2x2x2 spatial torus (Z^3 PBC).

Geometry: 2x2x2 spatial torus with PBC. 8 sites, 24 links, 12 plaquettes.

Each link has Casimir energy and is shared by 4 plaquettes (3D-cubic).

Approach: Casimir-diagonal Wilson-loop character basis (Option C from
the 2x2 v3 analysis). Each chi_lambda(W) for closed loop W is an
eigenstate of sum_e Chat(e) with eigenvalue |W| * C_2(lambda).

Basis (3D torus has many short Wilson loops):
  - 12 plaquettes (length 4 each)
  - 12 non-contractible 2-loops (X loops, Y loops, Z loops)
  - Possibly longer loops

We use a Monte Carlo Haar-sample approach: sample 24 SU(3) variables,
build basis of Wilson-loop characters at samples, build H + Gram via MC,
diagonalize.

Output: <P>_avg over the 12 plaquettes.

This is computationally heavier than 2x2 but still tractable.
"""

from __future__ import annotations

import time
import numpy as np
from numpy.linalg import eigh

from cl3_ks_single_plaquette_2026_05_07 import casimir, dim_irrep
from cl3_ks_two_plaquette_2026_05_07 import sample_su3, chi_pq


def haar_sample_24links(N: int, seed: int = 42):
    """Generate 24 independent SU(3) link variables for 2x2x2 torus.

    Convention: U_d_(i,j,k) = link from (i,j,k) to (i+1, j, k) for d=x,
                                                  (i, j+1, k) for d=y,
                                                  (i, j, k+1) for d=z,
    all mod 2.
    """
    samples = {}
    counter = 0
    for d in ['x', 'y', 'z']:
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    key = f'{d}_{i}{j}{k}'
                    samples[key] = sample_su3(N, seed=seed + counter)
                    counter += 1
    return samples


def matprod(*Us):
    out = Us[0]
    for U in Us[1:]:
        out = np.einsum('nij,njk->nik', out, U)
    return out


def matinv(U):
    return np.conj(U.transpose(0, 2, 1))


def re_trace_over_Nc(M, N_c=3):
    return np.trace(M, axis1=1, axis2=2).real / N_c


def shift(coord, axis, delta=1):
    """Shift coord by delta along axis (0=x, 1=y, 2=z), mod 2."""
    new = list(coord)
    new[axis] = (new[axis] + delta) % 2
    return tuple(new)


def link_holonomy(samples, coord, axis):
    """U_axis_(i,j,k) for outgoing link from coord."""
    d = ['x', 'y', 'z'][axis]
    i, j, k = coord
    return samples[f'{d}_{i}{j}{k}']


def plaquette_holonomy(samples, coord, axes):
    """
    Plaquette in plane (axes[0], axes[1]) starting at coord.

    P = U_a(coord) U_b(coord+a) U_a(coord+b)^-1 U_b(coord)^-1
    where a, b are axes[0], axes[1].
    """
    a, b = axes
    coord_a = shift(coord, a)
    coord_b = shift(coord, b)
    U1 = link_holonomy(samples, coord, a)
    U2 = link_holonomy(samples, coord_a, b)
    U3_inv = matinv(link_holonomy(samples, coord_b, a))
    U4_inv = matinv(link_holonomy(samples, coord, b))
    return matprod(U1, U2, U3_inv, U4_inv)


def all_plaquettes(samples):
    """All 12 plaquettes on the 2x2x2 torus.

    For each axis pair (a, b) in {(0,1), (1,2), (2,0)} (xy, yz, zx),
    and each base coord (i,j,k) in {0,1}^3, there's a plaquette.

    Total: 3 plane-orientations x 8 base coords = 24, but each plaquette
    is counted by 1 base coord (the convention of "starting corner").

    Wait: For each plane (e.g., xy), and each value of the orthogonal
    axis (z), there are 4 plaquettes (2x2 = 4). With 3 orthogonal axes
    and 2 z-values per orthogonal axis, total = 3 * 2 * 4 = 24...
    but every plaquette is at one specific (corner, plane), counted once.

    Actually: a plaquette is uniquely identified by its 4 corner sites
    and its plane orientation. The "starting corner" can be any of the
    4 corners. To avoid double-counting, fix the convention that the
    plaquette is identified by its "lowest-coordinate corner" (lex order)
    and the plane (xy, yz, zx) it lies in.

    For 2x2x2 torus:
        Number of plaquettes per axis pair = 4 (one per 2D face on
        each fixed value of the third coordinate, summed over both
        third-coordinate values: 2 * 2 = 4)
    Wait, with PBC the count is different. Let me re-derive.

    A plaquette in the xy-plane is identified by (i, j, k) base corner.
    There are 8 such triples, BUT with 2x2 in xy direction and PBC,
    each plaquette is counted ONCE per base corner (since plaquettes
    don't repeat under translation of base corner by 2 in either x or y).

    So total: 8 base corners x 3 plane orientations / (counting per
    plaquette) = 24, but each unique plaquette appears... 4 times because
    the 4 corners can be chosen as base?

    No, each plaquette has 4 corners but only ONE is chosen as the base
    (by convention, e.g., the lex-smallest). So the count is 8 base
    corners x 3 planes / 4 = 6 plaquettes per plane * 3 planes = NO,
    that's wrong too.

    Let me think again. On a 2x2x2 torus:
    - Each axis has 2 lattice spacings.
    - Each plaquette is in a plane orthogonal to one axis.
    - Plaquettes orthogonal to z-axis: each is uniquely identified by
      its z-coordinate (2 values: z=0 or z=1) and its (i,j) base
      corner in the xy-plane (4 values: (0,0), (1,0), (0,1), (1,1)).
      Total: 2 * 4 = 8 plaquettes orthogonal to z.

    Actually no. The 2x2 lattice in (i,j) has only 4 sites = 4 plaquettes
    (with PBC). Each plaquette is at base corner (i,j) for i,j ∈ {0,1}.
    With PBC, plaquette at (1,1) wraps around — but it's still a unique
    plaquette.

    In 2x2 lattice with PBC, there are 4 plaquettes per orthogonal axis.

    So in 2x2x2 with 3 orthogonal axes: 3 * 4 = 12 plaquettes total.
    YES — that matches the user's description.

    Implementation: enumerate all 12 plaquettes by (plane, base coord).
    """
    plaqs = []
    plane_pairs = [(0, 1), (1, 2), (2, 0)]  # xy, yz, zx
    for axes in plane_pairs:
        a, b = axes
        # For each orthogonal axis value (the axis NOT in plane)
        c_axis = 3 - a - b
        for c_val in [0, 1]:
            for ai in [0, 1]:
                for bi in [0, 1]:
                    # Build base coord: ai on axis a, bi on axis b, c_val on axis c
                    coord = [0, 0, 0]
                    coord[a] = ai
                    coord[b] = bi
                    coord[c_axis] = c_val
                    plaqs.append(plaquette_holonomy(samples, tuple(coord), axes))
    # Total = 3 planes * 2 c-values * 4 (a,b)-choices = 24, but each plaquette
    # is counted... let me think. For plane xy (axes 0,1), c_axis=2.
    # For c_val=0: (ai, bi) gives 4 plaquettes (each at z=0). For c_val=1:
    # 4 plaquettes (each at z=1). Total 8 in xy.
    # WAIT: this is more than the 4 expected. Hmm.
    # Let me recount.

    # Actually for 2x2 lattice in (a,b) with PBC, there are 4 plaquettes
    # (one starting at each of (0,0), (1,0), (0,1), (1,1)). With 2 z-values,
    # we get 4 * 2 = 8 plaquettes orthogonal to z.
    # Total over all 3 planes: 3 * 8 = 24. But user said 12.
    # Discrepancy — let me re-examine.

    # User: "8 sites, 24 links, 12 unique plaquettes"
    # 8 sites: 2^3 = 8 ✓
    # 24 links: 3 directions * 8 sites = 24 ✓
    # Plaquettes: a 2x2x2 torus is small. Each plaquette is 1x1 face.
    # Per axis pair, with 2 values in each in-plane direction and 2 values
    # of the orthogonal axis: 2*2*2 = 8 plaquettes orthogonal to one axis.
    # Total over 3 axes: 24. But user says 12.

    # OH — 2x2x2 has only 2x2=4 plaquettes per face plane (since 2x2
    # in plane), and 2 values of the orthogonal direction, but maybe by
    # convention plaquettes are counted per "site" times 3 directions?
    # 8 sites * 3 plaq/site = 24, but each plaquette is shared by 4 sites
    # in that plane, so 24 / 4 = 6 unique per axis * 3 axes = 18?
    # Hmm, 24 / 2 = 12 makes sense if each plaquette is shared by 2 sites
    # along the orthogonal axis with PBC.

    # Actually I think the right count for 2x2x2 PBC torus:
    # Each plaquette orthogonal to z is a 1x1 face in the xy-plane at fixed z.
    # With 2x2 PBC in xy and 2 PBC in z, the number of distinct 1x1 faces
    # orthogonal to z is 2x2x2 = 8 (per z-position, 4 plaquettes; for 2
    # z-values, 8 plaquettes orthogonal to z). Total over 3 axes: 24.
    # But the user said 12.

    # Maybe the user is counting "plaquette types" not all plaquettes.
    # With 2-PBC in each direction, maybe the user views the torus as
    # having 4 plaquettes per face direction (one per 2x2 face) and 3
    # face directions, but per-position only 1 face per direction (since
    # 2-PBC means there are 2 distinct positions but only 1 face per
    # position?).

    # Let me reconsider. In 2x2x2 with PBC:
    # - 8 vertices: (i,j,k) with i,j,k in {0,1}
    # - Each vertex has 6 outgoing/incoming links: 1 in each of +/- x, +/- y, +/- z. With PBC, +x and -x at the same vertex are different links unless 2x2 is degenerate.
    # - Wait. 2x2 PBC in x: from vertex (0,j,k), going +x gets to (1,j,k); going +x AGAIN from (1,j,k) gets to (0,j,k). So the two x-links from each vertex are: one going (0,j,k) -> (1,j,k), and one going (1,j,k) -> (0,j,k). These are TWO distinct links.
    # - Total x-links: 4 (one per (j,k) pair, going (0,j,k)->(1,j,k))
    #   PLUS 4 (going (1,j,k)->(0,j,k))? But these are DIFFERENT from the first 4.
    # WAIT: in lattice gauge theory, each link has a unique starting vertex AND direction. So link "x at (0,j,k)" goes from (0,j,k) to (1,j,k). Link "x at (1,j,k)" goes from (1,j,k) to (0,j,k). These are 2 different links per (j,k) pair. With 4 (j,k) pairs, that's 8 x-links. Times 3 directions = 24 links ✓
    #
    # Now plaquettes: a plaquette in the xy-plane goes around a 1x1 face.
    # Starting at (i,j,k), going +x, +y, -x, -y returns to (i,j,k):
    #     U_x(i,j,k) U_y(i+1,j,k) U_x(i,j+1,k)^-1 U_y(i,j,k)^-1
    # For 2x2 in xy, there are 4 such plaquettes per z-value (one per (i,j) base).
    # With 2 z-values, that's 8 plaquettes orthogonal to z. Total: 3 axes x 8 = 24.

    # But maybe with 2-PBC, plaquettes orthogonal to z at z=0 and z=1
    # are the SAME plaquette? They share all 4 links (since x-links
    # depend on z, but if links at z=0 and z=1 are different, plaquettes
    # are different)... hmm, links at different z ARE different (24 links
    # total accounts for that).

    # I think the user's "12 unique plaquettes" might be a typo or different
    # counting convention. Let me just enumerate and use what I have.

    # For now, use the 24 plaquettes (or the de-duplicated list if any
    # are repeated). Actually probably 24 is correct.
    return plaqs


def all_plaquettes_v2(samples):
    """Cleaner enumeration: each plaquette identified by (plane, base_coord)."""
    plaqs = []
    plane_pairs = [(0, 1), (1, 2), (2, 0)]
    base_coords_3d = [(i, j, k) for i in [0, 1] for j in [0, 1] for k in [0, 1]]
    for axes in plane_pairs:
        for base in base_coords_3d:
            plaqs.append(plaquette_holonomy(samples, base, axes))
    return plaqs  # 3 * 8 = 24 plaquettes


def plaquette_link_set(coord, axes):
    """Return the set of link IDs in plaquette starting at coord, plane axes.

    Link IDs: '<dir>_<i><j><k>' where dir in 'x','y','z'.
    """
    a, b = axes
    coord_a = shift(coord, a)
    coord_b = shift(coord, b)
    d_a = ['x', 'y', 'z'][a]
    d_b = ['x', 'y', 'z'][b]
    return frozenset([
        f'{d_a}_{coord[0]}{coord[1]}{coord[2]}',
        f'{d_b}_{coord_a[0]}{coord_a[1]}{coord_a[2]}',
        f'{d_a}_{coord_b[0]}{coord_b[1]}{coord_b[2]}',
        f'{d_b}_{coord[0]}{coord[1]}{coord[2]}',
    ])


def all_plaquette_specs():
    """All (plane, base_coord, link_set) for 2x2x2 plaquettes."""
    plane_pairs = [(0, 1), (1, 2), (2, 0)]
    base_coords_3d = [(i, j, k) for i in [0, 1] for j in [0, 1] for k in [0, 1]]
    specs = []
    for axes in plane_pairs:
        for base in base_coords_3d:
            specs.append((axes, base, plaquette_link_set(base, axes)))
    return specs


def deduplicate_plaquettes(specs):
    """Plaquettes are identified by their link set (as a closed loop, modulo
    starting corner). Return unique link-sets.

    Note: 4-link plaquette with PBC: at base corner (i,j,k) in plane (a,b),
    the link set is {U_a(coord), U_b(coord_a), U_a(coord_b), U_b(coord)}.

    For different base corners (i,j,k), (i+1,j,k), (i,j+1,k), (i+1,j+1,k)
    in the same plane and at the same orthogonal coord, do they form the
    SAME plaquette?

    On 2x2 lattice with PBC, the plaquette at base (0,0,k) uses links
    x_{00k}, y_{10k}, x_{01k}, y_{00k}.
    Plaquette at base (1,1,k) uses x_{11k}, y_{01k}, x_{10k}, y_{11k}.
    These have DISJOINT link sets! So they are DIFFERENT plaquettes.

    Plaquette at base (1,0,k) uses x_{10k}, y_{00k}, x_{11k}, y_{10k}.
    This shares y_{10k} and x_{11k} with the (1,1,k) plaquette.
    Different from (0,0,k) plaquette.

    Plaquette at base (0,1,k) uses x_{01k}, y_{11k}, x_{00k}, y_{01k}.
    Different from others.

    So all 4 base coords in 2x2 PBC give 4 DISTINCT plaquettes per (plane, c_val).
    Total = 4 * 2 (c-values) * 3 planes = 24 plaquettes. NOT 12.

    Hmm. The user's claim of "12 unique plaquettes" might be wrong, or
    they may be referring to something else.

    Actually for 2x2x2 PBC: in each plane (e.g. xy), there are 4 plaquettes
    per fixed z. With 2 values of z, that's 8 plaquettes orthogonal to z.
    Times 3 axes = 24. So 24 is the correct count.

    Unless the user meant "plaquettes per direction" or something else.
    Let me just go with 24.
    """
    seen = set()
    out = []
    for axes, base, lset in specs:
        if lset not in seen:
            seen.add(lset)
            out.append((axes, base, lset))
    return out


def loop_holonomies_3d(samples, plaq_specs):
    """Compute all plaquette holonomies, indexed by spec index."""
    holos = {}
    for idx, (axes, base, lset) in enumerate(plaq_specs):
        holos[f'P{idx}'] = plaquette_holonomy(samples, base, axes)
    return holos


def build_basis_3d_torus(samples, plaq_specs, irrep_set, holos,
                          include_plaquettes=True,
                          include_disjoint_pairs=False):
    """Casimir-diagonal basis for 3D torus."""
    N = next(iter(holos.values())).shape[0]
    F_list = [np.ones(N, dtype=complex)]
    labels = [{'loops': [], 'cas': 0.0}]

    if include_plaquettes:
        for idx, (axes, base, lset) in enumerate(plaq_specs):
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[f'P{idx}'], *lam))
                cas = 4 * casimir(*lam)  # 4 links per plaquette
                labels.append({'loops': [(f'P{idx}', lam, lset)],
                                'cas': cas})

    if include_disjoint_pairs:
        # Two plaquettes are disjoint if their link sets don't intersect.
        n_p = len(plaq_specs)
        low_irreps = [(1, 0), (0, 1)]
        for i in range(n_p):
            for j in range(i + 1, n_p):
                _, _, lset_i = plaq_specs[i]
                _, _, lset_j = plaq_specs[j]
                if lset_i.isdisjoint(lset_j):
                    for lam_i in low_irreps:
                        for lam_j in low_irreps:
                            F_list.append(
                                chi_pq(holos[f'P{i}'], *lam_i)
                                * chi_pq(holos[f'P{j}'], *lam_j)
                            )
                            cas = 4 * casimir(*lam_i) + 4 * casimir(*lam_j)
                            labels.append({
                                'loops': [(f'P{i}', lam_i, lset_i),
                                          (f'P{j}', lam_j, lset_j)],
                                'cas': cas,
                            })

    F = np.array(F_list)
    return F, labels


def build_H_3d(g_squared, F, labels, holos, plaq_specs, N_c=3):
    n = F.shape[0]
    N_samples = F.shape[1]

    # Magnetic operator: average over plaquettes
    n_plaq = len(plaq_specs)
    re_tr_p = sum(re_trace_over_Nc(holos[f'P{i}']) for i in range(n_plaq))
    M_values = -(1.0 / g_squared) * re_tr_p

    Gram = (np.conj(F) @ F.T) / N_samples
    H_mag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N_samples

    H_cas = np.zeros((n, n), dtype=complex)
    for i, lbl in enumerate(labels):
        H_cas[i, i] = (g_squared / 2.0) * lbl['cas']

    H = H_cas + H_mag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))
    return H, Gram


def diagonalize_with_gram(H, Gram, tol=1e-7):
    Gram = 0.5 * (Gram + np.conj(Gram.T))
    g_evals, g_evecs = eigh(Gram)
    keep_mask = g_evals > tol * max(g_evals[-1], 1e-12)
    n_keep = int(np.sum(keep_mask))
    g_inv_sqrt = np.zeros_like(g_evals)
    g_inv_sqrt[keep_mask] = 1.0 / np.sqrt(g_evals[keep_mask])
    P_proj = g_evecs[:, keep_mask] * g_inv_sqrt[keep_mask][np.newaxis, :]
    H_orth = np.conj(P_proj.T) @ H @ P_proj
    H_orth = 0.5 * (H_orth + np.conj(H_orth.T))
    evals, evecs_orth = eigh(H_orth)
    evecs = P_proj @ evecs_orth
    return evals, evecs, n_keep


def expectation_P(psi, F, holos, plaq_specs, N_c=3):
    n_plaq = len(plaq_specs)
    plaqs = [holos[f'P{i}'] for i in range(n_plaq)]
    P_vals = sum(re_trace_over_Nc(p) for p in plaqs) / n_plaq
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    return float(np.mean(np.abs(psi_at) ** 2 * P_vals) / norm)


def expectation_P_indiv(psi, F, holos, plaq_specs):
    n_plaq = len(plaq_specs)
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    return [float(np.mean(np.abs(psi_at) ** 2
                           * re_trace_over_Nc(holos[f'P{i}'])) / norm)
             for i in range(n_plaq)]


def run_one_g(g_squared, irrep_set, N_samples, seed=11,
               include_disjoint_pairs=False, verbose=True):
    if verbose:
        print(f"\n--- 2x2x2 torus, g^2 = {g_squared}, N = {N_samples} ---")
    t0 = time.time()
    samples = haar_sample_24links(N_samples, seed=seed)
    plaq_specs = all_plaquette_specs()
    plaq_specs = deduplicate_plaquettes(plaq_specs)
    if verbose:
        print(f"  N plaquettes: {len(plaq_specs)}")
    holos = loop_holonomies_3d(samples, plaq_specs)
    F, labels = build_basis_3d_torus(samples, plaq_specs, irrep_set, holos,
                                       include_plaquettes=True,
                                       include_disjoint_pairs=include_disjoint_pairs)
    if verbose:
        print(f"  Basis size: {F.shape[0]} (sample+basis: {time.time()-t0:.1f}s)")

    t1 = time.time()
    H, Gram = build_H_3d(g_squared, F, labels, holos, plaq_specs)
    if verbose:
        print(f"  H+Gram: {time.time()-t1:.1f}s")

    t2 = time.time()
    evals, evecs, n_keep = diagonalize_with_gram(H, Gram)
    if verbose:
        print(f"  Diag: {time.time()-t2:.1f}s")

    psi0 = evecs[:, 0]
    P_avg = expectation_P(psi0, F, holos, plaq_specs)
    P_indiv = expectation_P_indiv(psi0, F, holos, plaq_specs)

    if verbose:
        print(f"  E_0 = {evals[0].real:.6f}  (kept {n_keep}/{F.shape[0]})")
        print(f"  <P>_avg = {P_avg:.6f}")
        print(f"  Plaq spread: mean={float(np.mean(P_indiv)):.4f}, "
              f"std={float(np.std(P_indiv)):.4f}")

    return {
        'g_squared': g_squared,
        'P_avg': P_avg,
        'P_indiv': P_indiv,
        'E_0': evals[0].real,
        'n_basis': F.shape[0],
        'n_kept': n_keep,
        'n_plaq': len(plaq_specs),
    }


def basis_convergence_3d(g_squared=1.0, N_samples=10000, seed=11):
    print(f"\n=== 2x2x2 basis convergence at g^2 = {g_squared} ===")
    rows = []
    for irreps, lbl in [
        ([(0, 0), (1, 0), (0, 1)], '3 irreps'),
        ([(0, 0), (1, 0), (0, 1), (1, 1)], '4 irreps'),
        ([(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)], '6 irreps'),
    ]:
        for disj in [False, True]:
            print(f"\n--- {lbl} {'with' if disj else 'no'} disjoint pairs ---")
            r = run_one_g(g_squared, irreps, N_samples, seed,
                           include_disjoint_pairs=disj, verbose=True)
            rows.append({**r, 'label': lbl, 'disj': disj})

    print(f"\nBasis convergence summary at g^2 = {g_squared}:")
    print(f"{'config':<20} {'disj':>5} {'#basis':>8} {'E_0':>10} "
          f"{'<P>_avg':>10}")
    for r in rows:
        print(f"{r['label']:<20} {str(r['disj']):>5} {r['n_basis']:>8}  "
              f"{r['E_0']:>10.6f}  {r['P_avg']:>10.6f}")


def coupling_sweep_3d(irrep_set, N_samples=10000, seed=11,
                       include_disjoint_pairs=False):
    print(f"\n=== 2x2x2 coupling sweep ===")
    rows = []
    for g2 in [0.5, 0.75, 1.0, 1.5, 2.0]:
        r = run_one_g(g2, irrep_set, N_samples, seed,
                       include_disjoint_pairs=include_disjoint_pairs,
                       verbose=True)
        rows.append(r)

    print(f"\nCoupling sweep summary:")
    print(f"{'g^2':>6}  {'<P>_avg':>10}  {'E_0':>12}  {'#basis':>7}")
    for r in rows:
        print(f"{r['g_squared']:>6.2f}  {r['P_avg']:>10.6f}  "
              f"{r['E_0']:>12.6f}  {r['n_basis']:>7}")
    return rows


if __name__ == "__main__":
    print("=" * 70)
    print("Cl(3) -> KS, 2x2x2 spatial torus (Z^3 PBC)")
    print("=" * 70)

    # Show plaquette count
    specs = all_plaquette_specs()
    specs_dedup = deduplicate_plaquettes(specs)
    print(f"\nPlaquette enumeration:")
    print(f"  Total plaquette specs: {len(specs)}")
    print(f"  Unique by link-set:    {len(specs_dedup)}")

    # [1] Basis convergence
    basis_convergence_3d(g_squared=1.0, N_samples=10000, seed=11)

    # [2] Coupling sweep
    print("\n[2] Coupling sweep (4 irreps, no disjoint pairs)")
    coupling_sweep_3d(irrep_set=[(0, 0), (1, 0), (0, 1), (1, 1)],
                       N_samples=20000, seed=11,
                       include_disjoint_pairs=False)

    print()
    print("=" * 70)
    print("Reference values:")
    print("  KS Hamilton limit (literature) thermodynamic at g^2~1:  ~0.55-0.60")
    print("  Wilson 4D MC at beta=6:                                   0.5934")
    print("  2x2 torus v3 at g^2=1:                                    0.042")
    print("  Strong-coupling LO at g^2=1:                              0.0417")
    print("=" * 70)
