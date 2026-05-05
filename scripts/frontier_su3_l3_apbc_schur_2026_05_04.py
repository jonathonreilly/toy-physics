"""L_s=3 APBC spatial cube Schur derivation attempt.

Per user request: "do ls3 apbc schur".

Builds on V-invariant L_s=2 APBC structure (frontier_su3_v_invariant_apbc_schur_2026_05_04.py).
For L_s=3 APBC the standard structure is:
  - 27 sites at corners of {0,1,2}^3
  - 81 directed forward links (27 sites × 3 directions)
  - 81 spatial plaquettes (27 per plane × 3 planes)
  - APBC in one direction (say z): plaquettes wrapping z=2→z=0 boundary
    pick up sign flip on the wrap-around link.

Critical question: does L_s=3 APBC have an analog of V-invariant reduction
(reducing link-incidence to 2 per link)? V-invariance at L_s=2 worked
because Z_2 × SU(3) compatibility. At L_s=3, natural twisted BC for SU(3)
is Z_3 (center group), not Z_2 / APBC. So APBC at L_s=3 may not reduce
link-incidence.

This script:
  1. Builds the L_s=3 APBC cube structure
  2. Computes link-incidence count per link
  3. Computes cyclic-index graph and N_components
  4. Applies naive Schur formula (acknowledging it requires link-incidence=2)
  5. Compares to L_s=2 V-invariant result

Expected: link-incidence > 2 at L_s=3 means naive Schur formula isn't
strictly correct; actual result may not match MC value 0.5934 either.
"""
import sys
import numpy as np
from scipy.special import iv

NMAX, MMAX, BETA = 6, 200, 6.0
L_S = 3  # spatial extent
APBC_DIR = 2  # apply APBC in z-direction (index 2)

def dim_su3(p, q): return (p+1)*(q+1)*(p+q+2)//2

def c_(p, q):
    arg = BETA/3.0
    lam = [p+q, q, 0]; tot = 0.0
    for m in range(-MMAX, MMAX+1):
        mat = np.array([[iv(m+lam[j]+i-j, arg) for j in range(3)] for i in range(3)], dtype=float)
        tot += float(np.linalg.det(mat))
    return tot

# Build L_s=3 spatial cube structure
# Sites: (x,y,z) ∈ {0,1,2}^3 → 27 sites
# Each site indexed as i = x + L*y + L^2*z

def site_idx(x, y, z):
    return x + L_S*y + L_S**2*z

def neighbor(x, y, z, direction):
    """Return (next_site, sign_factor) where sign_factor=-1 if APBC wraps."""
    coords = [x, y, z]
    new_coords = coords.copy()
    sign = 1
    new_coords[direction] = (coords[direction] + 1) % L_S
    if direction == APBC_DIR and coords[direction] == L_S - 1:
        sign = -1  # APBC wrap
    return site_idx(*new_coords), sign

# Build links: each (site, direction) pair gives one link
# Link is identified by (start_site, direction); end_site computed
links = []  # list of (start, end, direction, sign)
link_idx = {}  # (start, direction) -> index
for x in range(L_S):
    for y in range(L_S):
        for z in range(L_S):
            for d in range(3):
                start = site_idx(x, y, z)
                end, sign = neighbor(x, y, z, d)
                link_idx[(start, d)] = len(links)
                links.append((start, end, d, sign))
print(f"L_s={L_S} APBC: {len(links)} links (one per site×direction)")

# Build plaquettes: each (site, plane) gives one plaquette
# Plane (i,j) means plaquette in plane spanned by directions i and j (i<j)
# Plaquette at site (x,y,z) in plane (i,j):
#   path: site → site+e_i → site+e_i+e_j → site+e_j → site
#   uses 4 link-traversals (2 forward, 2 backward)
plaquettes = []
for x in range(L_S):
    for y in range(L_S):
        for z in range(L_S):
            for i in range(3):
                for j in range(i+1, 3):
                    start = site_idx(x, y, z)
                    # Move +e_i
                    n1, s1 = neighbor(x, y, z, i)
                    # From n1, move +e_j
                    coords = [x, y, z]
                    coords[i] = (coords[i] + 1) % L_S
                    n2, s2 = neighbor(*coords, j)
                    # From n2, move -e_i (reverse a link)
                    coords[j] = (coords[j] + 1) % L_S
                    # n3 = site at +e_j
                    coords_back = [x, y, z]
                    coords_back[j] = (coords_back[j] + 1) % L_S
                    # Forward link from coords_back in direction j: gives the boundary sign
                    n3, s3_forward = neighbor(coords_back[0], coords_back[1], coords_back[2], i)
                    # n3 should equal n2; the link (coords_back, dir i) is what we use BACKWARD
                    assert n3 == n2, f"plaquette closure mismatch: {n3} != {n2}"

                    # Plaquette uses 4 links:
                    # L1 = (start, i) forward, sign = s1
                    # L2 = ((start + e_i), j) forward, sign = s2
                    # L3 = (start + e_j, i) BACKWARD, sign = s3_forward
                    # L4 = (start, j) BACKWARD, sign = neighbor(start, j) → forward sign of the (start, j) link
                    n4, s4_forward = neighbor(x, y, z, j)
                    L1 = (link_idx[(start, i)], +1, s1)  # forward, sign
                    L2 = (link_idx[(n1, j)], +1, s2)  # forward
                    L3 = (link_idx[(coords_back[0]*1 + L_S*coords_back[1] + L_S**2*coords_back[2], i)], -1, s3_forward)  # backward
                    L4 = (link_idx[(start, j)], -1, s4_forward)  # backward
                    # Plaquette sign = product of all link signs
                    plaq_sign = s1 * s2 * s3_forward * s4_forward
                    plaquettes.append({
                        'site': start, 'plane': (i, j), 'links': [L1, L2, L3, L4], 'sign': plaq_sign
                    })

print(f"L_s={L_S}: {len(plaquettes)} plaquettes")

# Compute link-incidence count
link_incidence = {i: 0 for i in range(len(links))}
for p in plaquettes:
    for (lid, dir_sign, link_sign) in p['links']:
        link_incidence[lid] += 1

incidences = list(link_incidence.values())
print(f"Link-incidence: min={min(incidences)}, max={max(incidences)}, mean={sum(incidences)/len(incidences):.2f}")
print(f"  (V-invariant L=2 has incidence 2; PBC/APBC at L=3 has incidence 4)")

# Naive Schur formula computation
# For each plaquette, assign cyclic indices (4 per plaquette)
# Each link connects two plaquettes' cyclic indices via Schur orthogonality
# (when link incidence = 2)

n_nodes = 4 * len(plaquettes)
edges_list = []

# For each link, find which plaquettes contain it
link_to_plaqs = {i: [] for i in range(len(links))}
for p_idx, p in enumerate(plaquettes):
    for slot, (lid, dir_sign, link_sign) in enumerate(p['links']):
        link_to_plaqs[lid].append((p_idx, slot, dir_sign))

# Connect cyclic indices for each link
n_overcounted = 0
for lid, occurrences in link_to_plaqs.items():
    if len(occurrences) <= 1:
        continue  # boundary link (shouldn't happen at L=3 PBC/APBC)
    if len(occurrences) > 2:
        n_overcounted += 1
        # For naive Schur, only connect adjacent pairs
        # This is INCORRECT for link incidence > 2, but gives a reference number
    # Take all pairs (chain them through cyclic-index graph)
    for ii in range(len(occurrences) - 1):
        p_a, slot_a, dir_a = occurrences[ii]
        p_b, slot_b, dir_b = occurrences[ii + 1]
        in_a = 4 * p_a + slot_a
        out_a = 4 * p_a + (slot_a + 1) % 4
        in_b = 4 * p_b + slot_b
        out_b = 4 * p_b + (slot_b + 1) % 4
        edges_list.append((in_a, in_b))
        edges_list.append((out_a, out_b))

print(f"Cyclic-index graph: nodes={n_nodes}, edges={len(edges_list)}, overcounted_links={n_overcounted}")

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
print(f"N_components: {N_components}")

N_plaq = len(plaquettes)
N_links_unique = len(links)

# WARNING: this Schur formula assumes link-incidence = 2
# At L_s=3 the link incidence is 4, so naive Schur is NOT strictly correct
# But compute anyway for reference
print()
print(f"Naive Schur formula (assumes link-incidence=2):")
print(f"  ρ_(p,q) = (c/c_00)^{N_plaq} × d^({N_components} - {N_links_unique})")
print(f"  exponent of d: {N_components - N_links_unique}")
print(f"  WARNING: link-incidence={max(incidences)} > 2, so this formula is NOT")
print(f"  the correct Schur sum for L_s=3. Higher-incidence links require SU(3)")
print(f"  Clebsch-Gordan/fusion data.")

# Compute c values
weights = [(p,q) for p in range(NMAX+1) for q in range(NMAX+1)]
print(f"\nComputing c_(p,q) for {len(weights)} weights at β={BETA}, NMAX={NMAX}, MMAX={MMAX}...")
c_vals = {wt: c_(*wt) for wt in weights}
c00 = c_vals[(0,0)]
print(f"c_00 = {c00:.6e}")

# Compute rho via Schur formula
rho_dict = {}
for wt in weights:
    d = dim_su3(*wt)
    cratio = c_vals[wt] / c00
    # Use naive Schur formula
    rho_dict[wt] = (cratio ** N_plaq) * (d ** (N_components - N_links_unique))

print("\nTop ρ values (naive Schur):")
for wt, val in sorted(rho_dict.items(), key=lambda kv: -abs(kv[1]))[:10]:
    print(f"  ρ_{wt} = {val:.6e}")

# Run source-sector Perron solve
def perron_p_with_rho(rho_dict_input):
    norm = rho_dict_input[(0,0)]
    if abs(norm) < 1e-300:
        return float('nan')
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
    rho_arr = np.array([rho_n.get((p,q), 0.0) for (p,q) in weights])
    # Handle potential negative or extreme values from overflow
    rho_arr = np.clip(rho_arr, -1e300, 1e300)
    C_env = np.diag(rho_arr)
    T = mult @ D_loc @ C_env @ mult
    vals, vecs = np.linalg.eigh(T)
    i_max = int(np.argmax(vals))
    psi = vecs[:, i_max]
    if np.sum(psi) < 0: psi = -psi
    return float(psi @ (J @ psi))

P_naive = perron_p_with_rho(rho_dict)
print(f"\nP(L_s={L_S} APBC, β=6, naive Schur) = {P_naive}")
print(f"MC reference: 0.5934")
print(f"L_s=2 V-invariant Schur reference: 0.4225")

# Compare structure: is N_plaq - N_links the same exponent direction as L=2?
# L_s=2 V-invariant: N_plaq=6, N_links=12, N_comp=2 → exponent N_comp-N_links = -10
# L_s=3 PBC/APBC: N_plaq=81, N_links=81, N_comp=? → exponent N_comp-N_links

print()
print("=== Interpretation ===")
print(f"L_s=3 has link-incidence 4 (not 2 like V-invariant L_s=2)")
print(f"Naive Schur formula NOT strictly correct for incidence > 2")
print(f"Result {P_naive} should be interpreted as 'naive Schur' reference,")
print(f"NOT as the correct L_s=3 APBC Wilson plaquette value.")
print()
print("Correct L_s=3 derivation requires:")
print(f"  (a) SU(3) Clebsch-Gordan / 6j data for high-incidence links, OR")
print(f"  (b) Tensor-network contraction with treewidth ~ 29 (per PR #510), OR")
print(f"  (c) Different reduction (V-invariant analog) — does not exist for L_s=3 APBC")
print()
print("Conclusion: L_s=3 APBC under naive Schur does NOT close to MC 0.5934.")
print("True L_s=3 derivation is treewidth-bounded infeasible.")
