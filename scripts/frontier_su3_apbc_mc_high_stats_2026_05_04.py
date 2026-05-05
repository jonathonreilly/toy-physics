"""High-statistics MC on framework geometries: confirm V-inv L_s=2 vs L_s=3 APBC values.

Tests three framework-native cube setups at β=6 with direct SU(3) MC:
  (1) V-invariant L_s=2 APBC: 8 sites, 12 links, 6 plaquettes (incidence 2)
  (2) L_s=2 PBC: 8 sites, 12 links, 12 plaquettes (incidence 4)
  (3) L_s=3 APBC: 27 sites, 81 links, 81 plaquettes (incidence 4)

Compare to:
  - Naive Schur 0.4225 (V-invariant analytic)
  - L→∞ MC value 0.5934 (standard 4D Wilson)

Resolves whether ANY framework-relevant cube setup at finite volume
can reach 0.5934 without going to L→∞.
"""
import numpy as np
import time

np.random.seed(123)

BETA = 6.0

# ---------------------------------------------------------------
# SU(3) MC primitives
# ---------------------------------------------------------------

# Gell-Mann matrices (traceless Hermitian)
GM = np.array([
    [[0,1,0],[1,0,0],[0,0,0]],
    [[0,-1j,0],[1j,0,0],[0,0,0]],
    [[1,0,0],[0,-1,0],[0,0,0]],
    [[0,0,1],[0,0,0],[1,0,0]],
    [[0,0,-1j],[0,0,0],[1j,0,0]],
    [[0,0,0],[0,0,1],[0,1,0]],
    [[0,0,0],[0,0,-1j],[0,1j,0]],
    [[1,0,0],[0,1,0],[0,0,-2]] / np.sqrt(3),
], dtype=complex)

def random_perturbation(epsilon):
    """U = exp(i ε ∑_a a_a λ_a / 2) for random Gaussian a_a, normalized."""
    a = np.random.randn(8) * epsilon
    H = sum(a[k] * GM[k] for k in range(8)) / 2.0
    eigvals, eigvecs = np.linalg.eigh(H)
    return eigvecs @ np.diag(np.exp(1j * eigvals)) @ eigvecs.conj().T

# ---------------------------------------------------------------
# Geometry constructors
# ---------------------------------------------------------------

def build_v_invariant_l2_apbc():
    """V-invariant L_s=2 APBC cube: 6 plaquettes (cube faces only)."""
    faces = [
        [(0,1), (1,3), (3,2), (2,0)],  # xy z=0
        [(4,5), (5,7), (7,6), (6,4)],  # xy z=1
        [(0,1), (1,5), (5,4), (4,0)],  # xz y=0
        [(2,3), (3,7), (7,6), (6,2)],  # xz y=1
        [(0,2), (2,6), (6,4), (4,0)],  # yz x=0
        [(1,3), (3,7), (7,5), (5,1)],  # yz x=1
    ]
    edge_set = set()
    for face_edges in faces:
        for a, b in face_edges:
            edge_set.add(tuple(sorted([a, b])))
    edges_list = sorted(edge_set)
    edge_idx = {e: i for i, e in enumerate(edges_list)}
    face_link_data = []
    for face_edges in faces:
        flink = []
        for (a, b) in face_edges:
            edge = tuple(sorted([a, b]))
            orient = +1 if a < b else -1
            flink.append((edge_idx[edge], orient))
        face_link_data.append(flink)
    return len(edges_list), face_link_data

def build_l2_pbc():
    """L_s=2 PBC: full standard cube with 12 plaquettes (4 per plane × 3 planes)."""
    L = 2
    def site(x, y, z): return x + L*y + L*L*z

    # Build links: 8 sites × 3 directions = 24 directed; 12 unique (with PBC at L=2)
    links = []  # list of (start_site, end_site, dir)
    link_idx = {}
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for d in range(3):
                    coords = [x, y, z]
                    coords[d] = (coords[d] + 1) % L
                    end = site(*coords)
                    start = site(x, y, z)
                    key = (start, d)
                    link_idx[key] = len(links)
                    links.append((start, end, d))

    # For PBC L=2, the link (s, d) and (s', d) where s' = s_with_d_incremented might be the SAME unique edge
    # Build unique-edge mapping
    edge_to_unique = {}
    unique_edges = []
    for i, (s, e, d) in enumerate(links):
        edge = tuple(sorted([s, e]))
        if edge not in edge_to_unique:
            edge_to_unique[edge] = len(unique_edges)
            unique_edges.append(edge)

    # Build plaquettes: at each site, 3 planes (xy, xz, yz)
    plaquettes = []
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for i in range(3):
                    for j in range(i+1, 3):
                        # Plaquette in plane (i,j) at site (x,y,z)
                        s0 = (x, y, z)
                        s1 = list(s0); s1[i] = (s1[i]+1) % L; s1 = tuple(s1)
                        s2 = list(s1); s2[j] = (s2[j]+1) % L; s2 = tuple(s2)
                        s3 = list(s0); s3[j] = (s3[j]+1) % L; s3 = tuple(s3)
                        # Path: s0 → s1 → s2 → s3 → s0
                        edges = [
                            (site(*s0), site(*s1)),
                            (site(*s1), site(*s2)),
                            (site(*s2), site(*s3)),  # backward in i
                            (site(*s3), site(*s0)),  # backward in j
                        ]
                        flink = []
                        for (a, b) in edges:
                            edge = tuple(sorted([a, b]))
                            uidx = edge_to_unique[edge]
                            orient = +1 if a < b else -1
                            flink.append((uidx, orient))
                        plaquettes.append(flink)
    return len(unique_edges), plaquettes

def build_l3_apbc():
    """L_s=3 APBC: 27 sites, 81 links, 81 plaquettes; APBC in z direction."""
    L = 3
    APBC_DIR = 2  # z
    def site(x, y, z): return x + L*y + L*L*z

    links = []
    link_idx = {}
    link_signs = []  # sign factor for APBC links
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for d in range(3):
                    coords = [x, y, z]
                    sign = 1
                    if d == APBC_DIR and coords[d] == L - 1:
                        sign = -1
                    coords[d] = (coords[d] + 1) % L
                    end = site(*coords)
                    start = site(x, y, z)
                    link_idx[(start, d)] = len(links)
                    links.append((start, end, d))
                    link_signs.append(sign)

    plaquettes = []
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for i in range(3):
                    for j in range(i+1, 3):
                        s0 = (x, y, z)
                        # forward link in i
                        l1_idx = link_idx[(site(*s0), i)]
                        s1_coords = list(s0); s1_coords[i] = (s1_coords[i]+1) % L; s1 = tuple(s1_coords)
                        # forward link in j from s1
                        l2_idx = link_idx[(site(*s1), j)]
                        # backward link in i from s2 → corresponds to forward link in i from s3
                        s3_coords = list(s0); s3_coords[j] = (s3_coords[j]+1) % L; s3 = tuple(s3_coords)
                        l3_idx = link_idx[(site(*s3), i)]
                        # backward link in j from s3 → forward link in j from s0
                        l4_idx = link_idx[(site(*s0), j)]

                        # Combine plaquette sign from APBC link signs
                        plaq_sign = link_signs[l1_idx] * link_signs[l2_idx] * link_signs[l3_idx] * link_signs[l4_idx]

                        flink = [
                            (l1_idx, +1, link_signs[l1_idx]),
                            (l2_idx, +1, link_signs[l2_idx]),
                            (l3_idx, -1, link_signs[l3_idx]),
                            (l4_idx, -1, link_signs[l4_idx]),
                        ]
                        plaquettes.append((flink, plaq_sign))
    return len(links), plaquettes

# ---------------------------------------------------------------
# MC engine (works for both formats)
# ---------------------------------------------------------------

def plaquette_matrix(face_data, links):
    """Compute plaquette matrix product."""
    if len(face_data[0]) == 2:
        # Format: [(lid, orient)]
        flink = face_data
        sign = 1
    else:
        # Format: ([(lid, orient, sign)], plaq_sign)
        flink = [(l[0], l[1]) for l in face_data[0]]
        sign = face_data[1]
    U = np.eye(3, dtype=complex)
    for (lid, orient) in flink:
        if orient == +1:
            U = U @ links[lid]
        else:
            U = U @ links[lid].conj().T
    return U, sign

def avg_plaquette(face_data_list, links):
    s = 0.0
    for fd in face_data_list:
        M, sign = plaquette_matrix(fd, links)
        s += sign * np.real(np.trace(M)) / 3.0
    return s / len(face_data_list)

def metropolis_sweep(links, face_data_list, eps, link_to_faces):
    """Single Metropolis sweep."""
    n_accept = 0
    n_total = 0
    n_links = len(links)
    for lid in range(n_links):
        U_old = links[lid].copy()
        V = random_perturbation(eps)
        U_new = V @ U_old
        # Compute action change
        S_old = 0.0
        S_new = 0.0
        for fidx in link_to_faces[lid]:
            fd = face_data_list[fidx]
            M_old, sign = plaquette_matrix(fd, links)
            s_old_val = sign * np.real(np.trace(M_old))
            links[lid] = U_new
            M_new, sign = plaquette_matrix(fd, links)
            s_new_val = sign * np.real(np.trace(M_new))
            links[lid] = U_old
            S_old += s_old_val
            S_new += s_new_val
        dS = -(BETA / 3.0) * (S_new - S_old)
        n_total += 1
        if dS < 0 or np.random.rand() < np.exp(-dS):
            links[lid] = U_new
            n_accept += 1
    return n_accept / n_total

def build_link_to_faces(face_data_list, n_links):
    """For each link, list of face indices that include it."""
    l2f = [[] for _ in range(n_links)]
    for fidx, fd in enumerate(face_data_list):
        if len(fd[0]) == 2:
            flink = fd
        else:
            flink = [(l[0], l[1]) for l in fd[0]]
        for (lid, orient) in flink:
            if fidx not in l2f[lid]:
                l2f[lid].append(fidx)
    return l2f

def run_mc(name, n_links, face_data_list, n_thermalize=3000, n_measure=10000, n_skip=10):
    print(f"\n{'='*64}")
    print(f"MC on {name}")
    print(f"{'='*64}")
    print(f"  Links: {n_links}, Plaquettes: {len(face_data_list)}")
    links = [np.eye(3, dtype=complex) for _ in range(n_links)]
    link_to_faces = build_link_to_faces(face_data_list, n_links)
    eps = 0.5
    print(f"  Thermalizing {n_thermalize} sweeps...")
    t0 = time.time()
    acc_history = []
    for i in range(n_thermalize):
        acc = metropolis_sweep(links, face_data_list, eps, link_to_faces)
        acc_history.append(acc)
        if (i+1) % 500 == 0:
            recent = np.mean(acc_history[-500:])
            curp = avg_plaquette(face_data_list, links)
            elapsed = time.time() - t0
            print(f"    sweep {i+1}/{n_thermalize}: acc={recent:.3f}, P={curp:.4f}, elapsed={elapsed:.1f}s")
            if recent > 0.6: eps *= 1.1
            elif recent < 0.4: eps *= 0.9
    print(f"  Measuring {n_measure} sweeps (skip {n_skip})...")
    P_samples = []
    for i in range(n_measure):
        metropolis_sweep(links, face_data_list, eps, link_to_faces)
        if i % n_skip == 0:
            P_samples.append(avg_plaquette(face_data_list, links))
        if (i+1) % 2000 == 0 and len(P_samples) > 0:
            elapsed = time.time() - t0
            print(f"    sweep {i+1}/{n_measure}: ⟨P⟩={np.mean(P_samples):.4f}±{np.std(P_samples)/np.sqrt(len(P_samples)):.4f} (N={len(P_samples)}, t={elapsed:.0f}s)")
    P_mean = np.mean(P_samples)
    P_err = np.std(P_samples) / np.sqrt(len(P_samples))
    print(f"  RESULT: ⟨P⟩ = {P_mean:.4f} ± {P_err:.4f}")
    return P_mean, P_err

# ---------------------------------------------------------------
# Run all geometries
# ---------------------------------------------------------------

print(f"\n{'#'*64}")
print(f"# Framework MC scan: V-inv L_s=2 APBC, L_s=2 PBC, L_s=3 APBC")
print(f"# β=6, comparison to naive Schur and L→∞ MC reference")
print(f"{'#'*64}")

# (1) V-invariant L_s=2 APBC
n_links_1, faces_1 = build_v_invariant_l2_apbc()
P1, e1 = run_mc("V-invariant L_s=2 APBC (6 plaquettes)", n_links_1, faces_1)

# (2) L_s=2 PBC (full 12 plaquettes)
n_links_2, faces_2 = build_l2_pbc()
P2, e2 = run_mc("L_s=2 PBC (12 plaquettes)", n_links_2, faces_2,
                n_thermalize=3000, n_measure=8000)

# (3) L_s=3 APBC
n_links_3, faces_3 = build_l3_apbc()
P3, e3 = run_mc("L_s=3 APBC (81 plaquettes)", n_links_3, faces_3,
                n_thermalize=2000, n_measure=5000)

# Summary
print(f"\n{'='*64}")
print(f"SUMMARY: framework cube MC scan at β=6")
print(f"{'='*64}\n")
print(f"  Geometry                         ⟨P⟩ (MC)         Schur ref")
print(f"  V-invariant L_s=2 APBC (6 pl)   {P1:.4f}±{e1:.4f}   0.4225 (naive)")
print(f"  L_s=2 PBC (12 pl)               {P2:.4f}±{e2:.4f}   0.4291 (naive)")
print(f"  L_s=3 APBC (81 pl)              {P3:.4f}±{e3:.4f}   0.4225 (degenerate)")
print(f"\n  L→∞ standard 4D Wilson MC ref:                   0.5934")
print()
print(f"INTERPRETATION:")
gap_1 = 0.5934 - P1
gap_3 = 0.5934 - P3
trend = (P3 - P1) / max(P1, 1e-9)
print(f"  V-inv L_s=2 APBC: gap to L→∞ = {gap_1:+.4f}")
print(f"  L_s=3 APBC:       gap to L→∞ = {gap_3:+.4f}")
print(f"  Relative L_s=3 vs L_s=2 increase: {trend*100:+.1f}%")
if P3 > P1 + 3*max(e1, e3):
    print(f"  → L_s=3 IS larger than L_s=2 (finite-volume scaling toward L→∞)")
    print(f"  → Suggests V-invariance does NOT enforce L→∞ equivalence")
    print(f"  → To reach 0.5934, framework needs L_s ≥ ?? extrapolation")
elif abs(P3 - P1) < 3*max(e1, e3):
    print(f"  → L_s=3 ≈ L_s=2 (no finite-volume scaling visible)")
    print(f"  → Could indicate V-invariance partial L→∞ equivalence")
    print(f"  → But neither matches 0.5934, so further investigation needed")
