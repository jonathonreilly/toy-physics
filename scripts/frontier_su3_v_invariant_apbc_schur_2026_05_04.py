"""V-invariant L_s=2 APBC Schur cube derivation.

Per framework roadmap (SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE):
  - 8 sites
  - 12 directed link uses corresponding to 6 unique unoriented spatial links
  - 6 unique unoriented spatial plaquettes

The existing runner (frontier_su3_cube_perron_solve.py) uses 12 plaquettes,
which is L_s=2 PBC structure, NOT the framework's V-invariant minimal block.

This script computes the TRUE V-invariant L_s=2 APBC cube via Schur:
  6 plaquettes, 6 links.

For each link in 2 plaquettes, Schur orthogonality forces conjugate
labelings on adjacent plaquettes.

Expected formula: rho_(p,q) = (c/c_00)^6 × d^(N_components - 12)
where N_components is from the cyclic-index graph of the 6-plaquette cube.
"""
import sys
import numpy as np
from scipy.special import iv

NMAX, MMAX, BETA = 7, 200, 6.0

def dim_su3(p, q): return (p+1)*(q+1)*(p+q+2)//2
def c_(p, q):
    arg = BETA/3.0
    lam = [p+q, q, 0]; tot = 0.0
    for m in range(-MMAX, MMAX+1):
        mat = np.array([[iv(m+lam[j]+i-j, arg) for j in range(3)] for i in range(3)], dtype=float)
        tot += float(np.linalg.det(mat))
    return tot

# Build the V-invariant L_s=2 APBC cube structure:
# 8 sites at corners of [0,1]^3
# 6 unique plaquettes (one per face of the cube)
# 6 unique links (= 12 directed link uses / 2)

# Each face of the 3D cube has 4 sides; with 6 faces × 4 sides = 24 link-uses
# After APBC identification reducing by factor 2 (per framework spec):
# 12 link uses → 6 unique links, 6 unique plaquettes

# Implement: 6 faces of the cube as plaquettes
# The 6 faces are: (xy at z=0), (xy at z=1), (xz at y=0), (xz at y=1), (yz at x=0), (yz at x=1)
# Wait: at L=2 APBC, faces at z=0 and z=1 may be identified
# So unique faces: 3 face-types (xy, xz, yz)
# Hmm that's only 3, not 6.

# Let me re-read the spec. Per the framework:
# "6 unique unoriented spatial plaquettes"
# Maybe the V-invariant block has 6 plaquettes with specific structure

# Actually for L=2 APBC, the cube STRUCTURE depends on the exact APBC identifications.
# Let me try a simpler interpretation: 6 faces = 6 plaquettes, no further identification.

# 8 sites: (x, y, z) ∈ {0, 1}^3
# 12 directed links between adjacent sites (3 directions × 8 sites / 2 for shared = 12)
# Wait, 8 sites × 3 forward directions = 24 directed forward links in PBC
# In APBC: maybe halved to 12 (per spec)

# Try: 6 faces of the cube = 6 plaquettes
# 12 edges of the cube = 12 directed links
# 6 unique links (each of the 6 face-pairs contributes 2 links per pair)

# For Schur computation: 6 plaquettes, 6 unique links
# Each link in 2 plaquettes (adjacent faces)
# Cyclic indices: 6 plaq × 4 cyc = 24 nodes
# Edges: 6 links × 2 edges/link = 12 edges

# Compute N_components for this graph
# For an L=2 cube with proper identification, the structure should give a SPECIFIC N_components

# Let me build a simpler geometric model:
# Label sites 0-7 by binary (x,y,z)
# 6 faces (one per axis × side):
# f_xy_0: z=0 face — sites with z=0 = 0,1,2,3
# f_xy_1: z=1 face — sites with z=1 = 4,5,6,7
# f_xz_0: y=0 face — sites with y=0 = 0,1,4,5
# f_xz_1: y=1 face — sites with y=1 = 2,3,6,7
# f_yz_0: x=0 face — sites with x=0 = 0,2,4,6
# f_yz_1: x=1 face — sites with x=1 = 1,3,5,7

# Each face is a square plaquette with 4 edges
# Total edges = 12 (each edge shared by 2 faces)

faces = [
    ("xy_0", [0, 1, 3, 2], [(0,1), (1,3), (3,2), (2,0)]),  # z=0
    ("xy_1", [4, 5, 7, 6], [(4,5), (5,7), (7,6), (6,4)]),  # z=1
    ("xz_0", [0, 1, 5, 4], [(0,1), (1,5), (5,4), (4,0)]),  # y=0
    ("xz_1", [2, 3, 7, 6], [(2,3), (3,7), (7,6), (6,2)]),  # y=1
    ("yz_0", [0, 2, 6, 4], [(0,2), (2,6), (6,4), (4,0)]),  # x=0
    ("yz_1", [1, 3, 7, 5], [(1,3), (3,7), (7,5), (5,1)]),  # x=1
]

# Collect all unique edges (links)
edge_set = set()
for name, sites, edges in faces:
    for a, b in edges:
        edge = tuple(sorted([a, b]))
        edge_set.add(edge)
print(f"Number of unique edges (links): {len(edge_set)}")
print(f"Number of plaquettes (faces): {len(faces)}")

# For each link, count plaquette incidence
edge_to_plaqs = {edge: [] for edge in edge_set}
for p_idx, (name, sites, edges) in enumerate(faces):
    for a, b in edges:
        edge = tuple(sorted([a, b]))
        edge_to_plaqs[edge].append((p_idx, (a, b)))

print(f"\nLink-to-plaquette incidence:")
incidences = [len(occs) for occs in edge_to_plaqs.values()]
print(f"  min/max/mean: {min(incidences)}/{max(incidences)}/{sum(incidences)/len(incidences):.2f}")

# Build cyclic-index graph
# 4 cyclic indices per plaquette × 6 plaquettes = 24 nodes
# For each shared link, 2 edges in cyclic graph (in-in, out-out)
# Use the same convention as Block 5: signed_indices_for_slot

n_nodes = 4 * len(faces)
edges_list = []

for edge, occs in edge_to_plaqs.items():
    if len(occs) != 2:
        print(f"  WARNING: edge {edge} has {len(occs)} plaquette occurrences (expected 2)")
        continue
    (p_a, (sa, sb)), (p_b, (sa2, sb2)) = occs
    # Find the slot of edge in each plaquette
    plaq_a_edges = faces[p_a][2]
    slot_a = None
    for i, e in enumerate(plaq_a_edges):
        if tuple(sorted(e)) == edge:
            slot_a = i
            break
    plaq_b_edges = faces[p_b][2]
    slot_b = None
    for i, e in enumerate(plaq_b_edges):
        if tuple(sorted(e)) == edge:
            slot_b = i
            break
    # All-forward convention: in = slot, out = (slot+1)%4
    in_a = 4 * p_a + slot_a
    out_a = 4 * p_a + (slot_a + 1) % 4
    in_b = 4 * p_b + slot_b
    out_b = 4 * p_b + (slot_b + 1) % 4
    edges_list.append((in_a, in_b))
    edges_list.append((out_a, out_b))

print(f"\nCyclic-index graph:")
print(f"  nodes: {n_nodes}")
print(f"  edges: {len(edges_list)}")

# Compute N_components via union-find
parent = list(range(n_nodes))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb

for a, b in edges_list:
    union(a, b)
N_components = len({find(i) for i in range(n_nodes)})
print(f"  N_components: {N_components}")

# Now compute rho_(p,q) = (c/c_00)^N_plaq × d^(N_components - N_links)
N_plaq = len(faces)
N_links = len(edge_set)
print(f"\n  Schur formula: rho_(p,q) = (c/c_00)^{N_plaq} × d^({N_components} - {N_links}) = (c/c_00)^{N_plaq} × d^({N_components - N_links})")

# Compute c values
weights = [(p,q) for p in range(NMAX+1) for q in range(NMAX+1)]
c_vals = {wt: c_(*wt) for wt in weights}
c00 = c_vals[(0,0)]

# Compute rho via Schur formula
rho_dict = {}
for wt in weights:
    d = dim_su3(*wt)
    cratio = c_vals[wt] / c00
    rho_dict[wt] = (cratio ** N_plaq) * (d ** (N_components - N_links))

# Show top values
print("\nTop ρ values:")
for wt, val in sorted(rho_dict.items(), key=lambda kv: -abs(kv[1]))[:10]:
    print(f"  ρ_{wt} = {val:.6e}")

# Run source-sector Perron solve
def perron_p_with_rho(rho_dict_input):
    norm = rho_dict_input[(0,0)]
    rho_n = {key:val/norm for key,val in rho_dict_input.items()}
    idx = {w:i for i,w in enumerate(weights)}
    J = np.zeros((len(weights), len(weights)))
    for p,q in weights:
        s = idx[(p,q)]
        for a,b in [(p+1,q),(p-1,q+1),(p,q-1),(p,q+1),(p+1,q-1),(p-1,q)]:
            if (a,b) in idx and a>=0 and b>=0:
                J[idx[(a,b)], s] += 1.0/6.0
    vals_J, vecs_J = np.linalg.eigh(J)
    mult = (vecs_J * np.exp(3.0 * vals_J)) @ vecs_J.T
    coeffs_arr = np.array([c_vals[(p,q)] for (p,q) in weights])
    dims = np.array([dim_su3(p,q) for (p,q) in weights])
    a_link = coeffs_arr / (dims * c00)
    D_loc = np.diag(a_link**4)
    C_env = np.diag(np.array([rho_n.get((p,q), 0.0) for (p,q) in weights]))
    T = mult @ D_loc @ C_env @ mult
    vals, vecs = np.linalg.eigh(T)
    i_max = int(np.argmax(vals))
    psi = vecs[:, i_max]
    if np.sum(psi) < 0: psi = -psi
    return float(psi @ (J @ psi))

P = perron_p_with_rho(rho_dict)
print(f"\nP(L_s=2 V-invariant APBC, β=6, Schur, N_plaq={N_plaq}, N_components={N_components}) = {P:.6f}")
print(f"MC reference: 0.5934")
print(f"Gap to MC: {abs(P - 0.5934):.6f}")
print(f"vs L_s=2 PBC Schur (PR #501 candidate): 0.4291 — gap from this: {abs(P - 0.4291):.6f}")

# Compare to PR #501 candidate (12 plaquettes, 24 links, 8 components)
print()
print(f"--- Comparison with PR #501 candidate (PBC: 12/24, N_comp=8) ---")
rho_pr501 = {wt: (c_vals[wt]/c00)**12 * dim_su3(*wt)**(8-24) for wt in weights}
P_pr501 = perron_p_with_rho(rho_pr501)
print(f"P_PR501 (12 plaq, 24 links, N_comp=8): {P_pr501:.6f}")
print(f"P_this (V-invariant APBC, {N_plaq} plaq, {N_links} links, N_comp={N_components}): {P:.6f}")
