"""Direct MC on V-invariant L_s=2 APBC cube — sanity check vs naive Schur.

This is FRAMEWORK-NATIVE: same Wilson action, same V-invariant L_s=2 APBC
cube structure, β=6 (g_bare=1) — just numerical SU(3) integration via
Metropolis MC instead of analytic Schur formula.

If MC ⟨P⟩ ≈ 0.4225 → naive Schur formula is correct → V-invariant cube
genuinely gives 0.4225 (gap to MC L→∞ value 0.5934 is finite-volume
artifact).

If MC ⟨P⟩ ≠ 0.4225 → naive Schur formula misses something → full
Wigner intertwiner contraction needed.

V-invariant L_s=2 APBC cube structure:
  - 8 sites at corners of unit cube
  - 12 links (one per cube edge)
  - 6 plaquettes (one per cube face)
  - link-incidence=2 per link
"""
import numpy as np
import math

np.random.seed(42)

BETA = 6.0
N_SU3 = 3

# Cube structure (matches frontier_su3_v_invariant_apbc_schur_2026_05_04.py)
# Sites 0-7 at (x,y,z) ∈ {0,1}^3, indexed: idx = x + 2y + 4z
faces = [
    ("xy_0", [0, 1, 3, 2], [(0,1), (1,3), (3,2), (2,0)]),  # z=0
    ("xy_1", [4, 5, 7, 6], [(4,5), (5,7), (7,6), (6,4)]),  # z=1
    ("xz_0", [0, 1, 5, 4], [(0,1), (1,5), (5,4), (4,0)]),  # y=0
    ("xz_1", [2, 3, 7, 6], [(2,3), (3,7), (7,6), (6,2)]),  # y=1
    ("yz_0", [0, 2, 6, 4], [(0,2), (2,6), (6,4), (4,0)]),  # x=0
    ("yz_1", [1, 3, 7, 5], [(1,3), (3,7), (7,5), (5,1)]),  # x=1
]

# Build unique edges
edge_set = set()
for name, sites, edges in faces:
    for a, b in edges:
        edge_set.add(tuple(sorted([a, b])))
edges_list = sorted(edge_set)
N_LINKS = len(edges_list)
print(f"V-invariant L_s=2 APBC cube: {N_LINKS} links, {len(faces)} plaquettes")

# For each face, get the ordered list of links with orientation (+1 forward, -1 backward)
# Loop direction (a→b→c→d→a) gives forward/backward link uses
edge_idx = {e: i for i, e in enumerate(edges_list)}

def link_in_face(face_edges):
    """Return list of (link_idx, orientation) for each edge in cyclic order."""
    result = []
    for (a, b) in face_edges:
        edge = tuple(sorted([a, b]))
        link_id = edge_idx[edge]
        orientation = +1 if a < b else -1  # forward if site index increases
        result.append((link_id, orientation))
    return result

face_link_data = [link_in_face(face[2]) for face in faces]

# SU(3) sampling: parameterize via small random updates
def random_su3():
    """Random SU(3) matrix via QR decomposition of Gaussian matrix."""
    A = (np.random.randn(3, 3) + 1j * np.random.randn(3, 3)) / np.sqrt(2)
    Q, R = np.linalg.qr(A)
    D = np.diag(np.diagonal(R) / np.abs(np.diagonal(R)))
    Q = Q @ D
    # Ensure det = 1
    detQ = np.linalg.det(Q)
    Q = Q * np.exp(-1j * np.angle(detQ) / 3.0)
    return Q

def random_perturbation(epsilon):
    """Small SU(3) perturbation U = exp(i ε H) where H is random Hermitian traceless."""
    # Random Hermitian traceless 3x3
    a = np.random.randn(8) * epsilon
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
    H = sum(a[k] * GM[k] for k in range(8))
    # Hmm need GM[7] normalization right
    # Use 1st-order: U ≈ I + i ε H — for small ε
    # For larger ε, exp the matrix
    eigvals, eigvecs = np.linalg.eigh(H)
    U = eigvecs @ np.diag(np.exp(1j * eigvals)) @ eigvecs.conj().T
    return U

def plaquette_value(links, face_data):
    """Compute (1/3) Re Tr of plaquette product."""
    U = np.eye(3, dtype=complex)
    for (lid, orient) in face_data:
        if orient == +1:
            U = U @ links[lid]
        else:
            U = U @ links[lid].conj().T
    return np.real(np.trace(U)) / 3.0

def total_action(links):
    """S = -(β/3) Σ_p Re Tr U_p for the 6 V-invariant cube faces.
    Wilson action wants exp[+(β/3) Σ Re Tr U_p], so action S = -(β/3) Σ Re Tr U_p."""
    s = 0.0
    for face_data in face_link_data:
        s += np.real(np.trace(plaquette_total(links, face_data)))
    return -(BETA / 3.0) * s

def plaquette_total(links, face_data):
    """Full plaquette matrix product."""
    U = np.eye(3, dtype=complex)
    for (lid, orient) in face_data:
        if orient == +1:
            U = U @ links[lid]
        else:
            U = U @ links[lid].conj().T
    return U

def avg_plaquette(links):
    """Average of (1/3) Re Tr U_p over all 6 plaquettes."""
    return np.mean([plaquette_value(links, fd) for fd in face_link_data])

# Initialize links to identity (cold start)
links = [np.eye(3, dtype=complex) for _ in range(N_LINKS)]

# Metropolis MC sweep
def metropolis_sweep(links, eps, n_hits=1):
    n_accept = 0
    n_total = 0
    for lid in range(N_LINKS):
        for _ in range(n_hits):
            # Compute action change for proposed update U_l → V × U_l
            U_old = links[lid].copy()
            V = random_perturbation(eps)
            U_new = V @ U_old
            # Old plaquette contributions involving this link
            S_old = 0.0
            S_new = 0.0
            for face_data in face_link_data:
                if any(l[0] == lid for l in face_data):
                    # Plaquette involves this link
                    P_old_mat = plaquette_total(links, face_data)
                    s_old = np.real(np.trace(P_old_mat))
                    # Compute new plaquette
                    links[lid] = U_new
                    P_new_mat = plaquette_total(links, face_data)
                    s_new = np.real(np.trace(P_new_mat))
                    links[lid] = U_old
                    S_old += s_old
                    S_new += s_new
            dS = -(BETA / 3.0) * (S_new - S_old)
            n_total += 1
            if dS < 0 or np.random.rand() < np.exp(-dS):
                links[lid] = U_new
                n_accept += 1
    return n_accept / n_total

# Run MC
print("\nRunning Metropolis MC on V-invariant L_s=2 APBC cube...")
print(f"β = {BETA}")

eps = 0.5  # perturbation scale
n_thermalize = 2000
n_measure = 5000
n_skip = 5

# Thermalize
print(f"\nThermalizing ({n_thermalize} sweeps)...")
acc_history = []
for i in range(n_thermalize):
    acc = metropolis_sweep(links, eps)
    acc_history.append(acc)
    if (i+1) % 500 == 0:
        recent_acc = np.mean(acc_history[-500:])
        recent_P = avg_plaquette(links)
        print(f"  sweep {i+1}: acc rate {recent_acc:.3f}, current ⟨P⟩ ≈ {recent_P:.4f}")
        # Adapt epsilon to keep acc rate ~50%
        if recent_acc > 0.6: eps *= 1.1
        elif recent_acc < 0.4: eps *= 0.9

# Measure
print(f"\nMeasuring ({n_measure} sweeps, skip {n_skip})...")
P_samples = []
for i in range(n_measure):
    metropolis_sweep(links, eps)
    if i % n_skip == 0:
        P_samples.append(avg_plaquette(links))
    if (i+1) % 1000 == 0:
        if len(P_samples) > 0:
            print(f"  sweep {i+1}: running ⟨P⟩ = {np.mean(P_samples):.4f} ± {np.std(P_samples)/np.sqrt(len(P_samples)):.4f}  (N={len(P_samples)})")

P_mean = np.mean(P_samples)
P_err = np.std(P_samples) / np.sqrt(len(P_samples))
print()
print("="*68)
print("RESULTS")
print("="*68)
print(f"\n  V-invariant L_s=2 APBC cube, β=6, MC:")
print(f"    ⟨P⟩_MC = {P_mean:.4f} ± {P_err:.4f}  (N_samples={len(P_samples)})")
print()
print(f"  Comparison:")
print(f"    Naive Schur formula:           0.4225 (analytic)")
print(f"    Standard 4D Wilson MC at L→∞:  0.5934 (different surface)")
print()
if abs(P_mean - 0.4225) < 3 * P_err:
    print(f"  → MC AGREES with naive Schur formula (within 3σ)")
    print(f"  → V-invariant L_s=2 APBC cube genuinely gives ~0.42")
    print(f"  → Naive Schur formula is CORRECT for this geometry")
    print(f"  → Gap to MC L→∞ value 0.5934 IS a real finite-volume artifact")
elif abs(P_mean - 0.5934) < 3 * P_err:
    print(f"  → MC matches L→∞ MC value 0.5934!")
    print(f"  → V-invariant L_s=2 APBC has built-in L→∞ equivalence")
    print(f"  → Naive Schur formula was WRONG; full intertwiner needed")
else:
    print(f"  → MC gives intermediate value, neither matches Schur nor MC L→∞")
    print(f"  → Investigate further")
