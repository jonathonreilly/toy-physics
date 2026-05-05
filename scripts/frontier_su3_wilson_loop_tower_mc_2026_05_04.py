"""Compute Wilson loop tower {W(1,1), W(1,2), W(2,2), W(2,3), W(3,3)} via
direct framework-native MC at β=6.

These will provide the matrix elements for the SDP bootstrap.

Wilson loop W(m,n) at site x in plane (μ,ν):
  W(m,n) = (1/N) Re Tr [product of U links around m×n rectangle]

Standard MC literature values for SU(3) at β=6 (large lattice):
  W(1,1) = 0.5934 (plaquette)
  W(1,2) = 0.357
  W(2,2) = 0.135
  W(1,3) = 0.225
  W(2,3) = 0.0858
  W(3,3) = 0.0228
"""
import numpy as np
import time

np.random.seed(2026 + 100)
BETA = 6.0

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
    a = np.random.randn(8) * epsilon
    H = sum(a[k] * GM[k] for k in range(8)) / 2.0
    eigvals, eigvecs = np.linalg.eigh(H)
    return eigvecs @ np.diag(np.exp(1j * eigvals)) @ eigvecs.conj().T

def build_4d_lattice(Ls, Lt):
    Ls_dims = [Ls, Ls, Ls, Lt]
    n_sites = Ls * Ls * Ls * Lt
    def site(x, y, z, t): return x + Ls*y + Ls*Ls*z + Ls*Ls*Ls*t
    def coords_for(s):
        t = s // (Ls**3); s2 = s - t*Ls**3
        z = s2 // (Ls**2); s3 = s2 - z*Ls**2
        y = s3 // Ls; x = s3 - y*Ls
        return [x, y, z, t]
    links = []
    link_idx = {}
    for s in range(n_sites):
        coords = coords_for(s)
        for d in range(4):
            new_coords = coords.copy()
            new_coords[d] = (new_coords[d] + 1) % Ls_dims[d]
            link_idx[(s, d)] = len(links)
            links.append(s)
    plaquettes = []
    for s in range(n_sites):
        coords = coords_for(s)
        for i in range(4):
            for j in range(i+1, 4):
                l1 = link_idx[(s, i)]
                s1_coords = coords.copy(); s1_coords[i] = (s1_coords[i]+1) % Ls_dims[i]
                s1 = site(*s1_coords)
                l2 = link_idx[(s1, j)]
                s3_coords = coords.copy(); s3_coords[j] = (s3_coords[j]+1) % Ls_dims[j]
                s3 = site(*s3_coords)
                l3 = link_idx[(s3, i)]
                l4 = link_idx[(s, j)]
                plaquettes.append([(l1, +1), (l2, +1), (l3, -1), (l4, -1)])
    return n_sites, link_idx, plaquettes

def wilson_loop_links(site_start, plane, m, n, link_idx, Ls_dims, site_fn, coords_fn):
    """Build link list for m×n Wilson loop in plane (i,j) starting at site_start.
    Path: forward m in i, forward n in j, backward m in i, backward n in j.
    Returns list of (link_idx, +1/-1 orientation)."""
    i, j = plane
    coords = coords_fn(site_start)
    path = []
    cur = list(coords)
    # Forward m steps in direction i
    for k in range(m):
        s = site_fn(*cur)
        path.append((link_idx[(s, i)], +1))
        cur[i] = (cur[i] + 1) % Ls_dims[i]
    # Forward n steps in direction j
    for k in range(n):
        s = site_fn(*cur)
        path.append((link_idx[(s, j)], +1))
        cur[j] = (cur[j] + 1) % Ls_dims[j]
    # Backward m steps in direction i (= forward from end)
    for k in range(m):
        cur[i] = (cur[i] - 1) % Ls_dims[i]
        s = site_fn(*cur)
        path.append((link_idx[(s, i)], -1))
    # Backward n steps in direction j (= forward from end)
    for k in range(n):
        cur[j] = (cur[j] - 1) % Ls_dims[j]
        s = site_fn(*cur)
        path.append((link_idx[(s, j)], -1))
    return path

def avg_wilson_loop(m, n, links, link_idx, Ls_dims, site_fn, coords_fn, n_samples=None):
    """Average over (m,n) Wilson loops in all 6 planes at all positions."""
    Ls, _, _, Lt = Ls_dims
    n_sites_total = Ls**3 * Lt
    total_W = 0.0
    n_loops = 0
    for s in range(n_sites_total):
        coords = coords_fn(s)
        for i in range(4):
            for j in range(i+1, 4):
                if (i < 3 and Ls_dims[i] >= m + 1) and (j < 3 and Ls_dims[j] >= n + 1) or (i == 3 and Lt >= m + 1) or (j == 3 and Lt >= n + 1):
                    if Ls_dims[i] < m or Ls_dims[j] < n: continue
                    path = wilson_loop_links(s, (i, j), m, n, link_idx, Ls_dims, site_fn, coords_fn)
                    U = np.eye(3, dtype=complex)
                    for (lid, orient) in path:
                        if orient == +1: U = U @ links[lid]
                        else: U = U @ links[lid].conj().T
                    total_W += np.real(np.trace(U)) / 3.0
                    n_loops += 1
                if n_samples is not None and n_loops >= n_samples:
                    return total_W / n_loops
    return total_W / n_loops if n_loops > 0 else 0.0

def metropolis_sweep(links, plaquettes, eps, link_to_faces):
    n_accept = 0
    n_total = 0
    for lid in range(len(links)):
        U_old = links[lid].copy()
        V = random_perturbation(eps)
        U_new = V @ U_old
        S_old = 0.0
        S_new = 0.0
        for fidx in link_to_faces[lid]:
            flink = plaquettes[fidx]
            U_p_old = np.eye(3, dtype=complex)
            for (l, orient) in flink:
                if orient == +1: U_p_old = U_p_old @ links[l]
                else: U_p_old = U_p_old @ links[l].conj().T
            s_old_val = np.real(np.trace(U_p_old))
            links[lid] = U_new
            U_p_new = np.eye(3, dtype=complex)
            for (l, orient) in flink:
                if orient == +1: U_p_new = U_p_new @ links[l]
                else: U_p_new = U_p_new @ links[l].conj().T
            s_new_val = np.real(np.trace(U_p_new))
            links[lid] = U_old
            S_old += s_old_val
            S_new += s_new_val
        dS = -(BETA / 3.0) * (S_new - S_old)
        n_total += 1
        if dS < 0 or np.random.rand() < np.exp(-dS):
            links[lid] = U_new
            n_accept += 1
    return n_accept / n_total

# Setup
Ls = 6  # need at least L=4 to fit 1x3, 2x3, 3x3 loops
Lt = 6
print(f"Wilson loop tower MC at β=6, Ls=Lt={Ls}", flush=True)
n_sites, link_idx, plaquettes = build_4d_lattice(Ls, Lt)
n_links = len(link_idx)
l2f = [[] for _ in range(n_links)]
for fidx, flink in enumerate(plaquettes):
    for (lid, _) in flink:
        if fidx not in l2f[lid]: l2f[lid].append(fidx)
print(f"Sites={n_sites}, Links={n_links}, Plaquettes={len(plaquettes)}", flush=True)

def site_fn(x, y, z, t): return x + Ls*y + Ls*Ls*z + Ls*Ls*Ls*t
def coords_fn(s):
    t = s // (Ls**3); s2 = s - t*Ls**3
    z = s2 // (Ls**2); s3 = s2 - z*Ls**2
    y = s3 // Ls; x = s3 - y*Ls
    return [x, y, z, t]
Ls_dims = [Ls, Ls, Ls, Lt]

# Initialize and thermalize
links = [np.eye(3, dtype=complex) for _ in range(n_links)]
eps = 0.5
t0 = time.time()
print(f"Thermalize 300 sweeps...", flush=True)
for i in range(300):
    acc = metropolis_sweep(links, plaquettes, eps, l2f)
    if (i+1) % 50 == 0:
        print(f"  therm {i+1}: t={time.time()-t0:.0f}s", flush=True)
        if acc > 0.6: eps *= 1.05
        elif acc < 0.4: eps *= 0.95

# Measure Wilson loops
sizes = [(1,1), (1,2), (2,2), (1,3), (2,3), (3,3)]
n_meas = 200
print(f"Measure {n_meas} sweeps, Wilson loops {sizes}...", flush=True)
samples = {sz: [] for sz in sizes}
for i in range(n_meas):
    metropolis_sweep(links, plaquettes, eps, l2f)
    if i % 5 == 0:
        for sz in sizes:
            try:
                W = avg_wilson_loop(*sz, links, link_idx, Ls_dims, site_fn, coords_fn,
                                     n_samples=200)
                samples[sz].append(W)
            except Exception as e:
                pass
    if (i+1) % 50 == 0:
        elapsed = time.time() - t0
        out = f"  meas {i+1}: t={elapsed:.0f}s; "
        for sz in sizes:
            if samples[sz]:
                out += f"W{sz}={np.mean(samples[sz]):.4f} "
        print(out, flush=True)

print("\n" + "="*60, flush=True)
print("WILSON LOOP TOWER RESULTS (β=6, Ls=Lt=4)", flush=True)
print("="*60, flush=True)
print(f"{'Loop':>6s}  {'Framework MC':>14s}  {'Std MC ref':>12s}", flush=True)
std_refs = {(1,1): 0.5934, (1,2): 0.357, (2,2): 0.135, (1,3): 0.225, (2,3): 0.0858, (3,3): 0.0228}
for sz in sizes:
    if samples[sz]:
        m = np.mean(samples[sz])
        e = np.std(samples[sz]) / np.sqrt(len(samples[sz]))
        ref = std_refs.get(sz, '-')
        print(f"  {str(sz):>6s}  {m:.4f}±{e:.4f}  {str(ref):>12s}", flush=True)

# Save data for SDP bootstrap input
import json
results = {str(sz): {'mean': float(np.mean(samples[sz])), 'err': float(np.std(samples[sz])/np.sqrt(max(1, len(samples[sz]))))} for sz in sizes if samples[sz]}
with open('/tmp/wilson_loops_L4.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to /tmp/wilson_loops_L4.json", flush=True)
