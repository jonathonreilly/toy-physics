"""4D SU(3) Wilson MC on framework's 3+1D structure (3 spatial + 1 temporal).

CRITICAL: previous MC was 3D spatial-only — this is the missing temporal
direction that the framework explicitly claims (3+1D structure).

Test: 4D SU(3) Wilson at β=6 on small lattices, see if it converges to
standard MC value 0.5934 (validating framework's gauge sector at L→∞).

Geometry: L_s × L_s × L_s × L_t (3 spatial + 1 temporal)
- Spatial APBC (matching V-invariant convention)
- Temporal PBC (standard for thermal)
- Both spatial and temporal plaquettes
"""
import numpy as np
import time

np.random.seed(42)

BETA = 6.0
N_DIM = 4  # 3+1D = 4D Wilson

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

def build_4d_lattice(Ls, Lt, apbc_dirs=(2,)):
    """4D lattice: 3 spatial + 1 temporal. APBC in spatial dir 2, PBC elsewhere."""
    Ls_dims = [Ls, Ls, Ls, Lt]
    n_sites = Ls * Ls * Ls * Lt

    def site(x, y, z, t):
        return x + Ls*y + Ls*Ls*z + Ls*Ls*Ls*t

    def coords_for(s):
        t = s // (Ls**3)
        s2 = s - t*Ls**3
        z = s2 // (Ls**2)
        s3 = s2 - z*Ls**2
        y = s3 // Ls
        x = s3 - y*Ls
        return [x, y, z, t]

    links = []
    link_signs = []
    link_idx = {}
    for s in range(n_sites):
        coords = coords_for(s)
        for d in range(4):
            sign = 1
            new_coords = coords.copy()
            if d in apbc_dirs and new_coords[d] == Ls_dims[d] - 1:
                sign = -1
            new_coords[d] = (new_coords[d] + 1) % Ls_dims[d]
            link_idx[(s, d)] = len(links)
            links.append(s)
            link_signs.append(sign)

    plaquettes = []
    for s in range(n_sites):
        coords = coords_for(s)
        for i in range(4):
            for j in range(i+1, 4):
                # Plaquette in plane (i,j)
                l1 = link_idx[(s, i)]
                s1_coords = coords.copy(); s1_coords[i] = (s1_coords[i]+1) % Ls_dims[i]
                s1 = site(*s1_coords)
                l2 = link_idx[(s1, j)]
                s3_coords = coords.copy(); s3_coords[j] = (s3_coords[j]+1) % Ls_dims[j]
                s3 = site(*s3_coords)
                l3 = link_idx[(s3, i)]
                l4 = link_idx[(s, j)]
                plaq_sign = link_signs[l1] * link_signs[l2] * link_signs[l3] * link_signs[l4]
                plaquettes.append(([(l1, +1), (l2, +1), (l3, -1), (l4, -1)], plaq_sign))

    return len(links), plaquettes

def build_link_to_faces(plaquettes, n_links):
    l2f = [[] for _ in range(n_links)]
    for fidx, (flink, _) in enumerate(plaquettes):
        for (lid, _) in flink:
            if fidx not in l2f[lid]:
                l2f[lid].append(fidx)
    return l2f

def avg_plaquette(plaquettes, links):
    s = 0.0
    for (flink, sign) in plaquettes:
        U = np.eye(3, dtype=complex)
        for (lid, orient) in flink:
            if orient == +1:
                U = U @ links[lid]
            else:
                U = U @ links[lid].conj().T
        s += sign * np.real(np.trace(U)) / 3.0
    return s / len(plaquettes)

def metropolis_sweep(links, plaquettes, eps, link_to_faces):
    n_accept = 0
    n_total = 0
    n_links = len(links)
    for lid in range(n_links):
        U_old = links[lid].copy()
        V = random_perturbation(eps)
        U_new = V @ U_old
        S_old = 0.0
        S_new = 0.0
        for fidx in link_to_faces[lid]:
            flink, sign = plaquettes[fidx]
            U_p_old = np.eye(3, dtype=complex)
            for (l, orient) in flink:
                if orient == +1: U_p_old = U_p_old @ links[l]
                else: U_p_old = U_p_old @ links[l].conj().T
            s_old_val = sign * np.real(np.trace(U_p_old))
            links[lid] = U_new
            U_p_new = np.eye(3, dtype=complex)
            for (l, orient) in flink:
                if orient == +1: U_p_new = U_p_new @ links[l]
                else: U_p_new = U_p_new @ links[l].conj().T
            s_new_val = sign * np.real(np.trace(U_p_new))
            links[lid] = U_old
            S_old += s_old_val
            S_new += s_new_val
        dS = -(BETA / 3.0) * (S_new - S_old)
        n_total += 1
        if dS < 0 or np.random.rand() < np.exp(-dS):
            links[lid] = U_new
            n_accept += 1
    return n_accept / n_total

def run_4d_mc(Ls, Lt, n_thermalize, n_measure, n_skip):
    print(f"\n{'='*68}")
    print(f"4D SU(3) Wilson MC: L_s={Ls}, L_t={Lt} (3+1D framework)")
    print(f"{'='*68}")
    n_links, plaquettes = build_4d_lattice(Ls, Lt)
    link_to_faces = build_link_to_faces(plaquettes, n_links)
    print(f"  Sites: {Ls**3 * Lt}, Links: {n_links}, Plaquettes: {len(plaquettes)}")
    links = [np.eye(3, dtype=complex) for _ in range(n_links)]
    eps = 0.5
    t0 = time.time()
    print(f"  Thermalizing {n_thermalize} sweeps...")
    acc_history = []
    for i in range(n_thermalize):
        acc = metropolis_sweep(links, plaquettes, eps, link_to_faces)
        acc_history.append(acc)
        if (i+1) % 200 == 0:
            recent = np.mean(acc_history[-200:])
            curp = avg_plaquette(plaquettes, links)
            elapsed = time.time() - t0
            print(f"    sweep {i+1}/{n_thermalize}: acc={recent:.3f}, P={curp:.4f}, t={elapsed:.0f}s")
            if recent > 0.6: eps *= 1.1
            elif recent < 0.4: eps *= 0.9
    print(f"  Measuring {n_measure} sweeps (skip {n_skip})...")
    P_samples = []
    for i in range(n_measure):
        metropolis_sweep(links, plaquettes, eps, link_to_faces)
        if i % n_skip == 0:
            P_samples.append(avg_plaquette(plaquettes, links))
        if (i+1) % 500 == 0 and len(P_samples) > 0:
            elapsed = time.time() - t0
            print(f"    sweep {i+1}: P={np.mean(P_samples):.4f}±{np.std(P_samples)/np.sqrt(len(P_samples)):.4f} (t={elapsed:.0f}s)")
    P_mean = np.mean(P_samples)
    P_err = np.std(P_samples) / np.sqrt(len(P_samples))
    print(f"  RESULT (Ls={Ls}, Lt={Lt}): ⟨P⟩ = {P_mean:.4f} ± {P_err:.4f}")
    return P_mean, P_err

print("\n" + "#"*68)
print("# 4D SU(3) Wilson MC on framework's 3+1D structure")
print("# Test if including temporal direction gives 0.5934 (vs 3D-only 0.46)")
print("#"*68)

# Try a few configurations
results = {}

# Smallest 4D: Ls=2, Lt=2 (16 sites)
results['Ls=2,Lt=2'] = run_4d_mc(2, 2, n_thermalize=1500, n_measure=3000, n_skip=10)

# Ls=Lt=3 (81 sites)
results['Ls=3,Lt=3'] = run_4d_mc(3, 3, n_thermalize=800, n_measure=1500, n_skip=10)

# Ls=Lt=4 (256 sites) - bigger, more useful
results['Ls=4,Lt=4'] = run_4d_mc(4, 4, n_thermalize=400, n_measure=800, n_skip=10)

# Summary
print(f"\n{'='*68}")
print(f"4D MC RESULTS (3+1D framework structure)")
print(f"{'='*68}\n")
print(f"  Geometry             ⟨P⟩         Standard 4D Wilson MC ref")
for label, (P, e) in results.items():
    print(f"  {label:20s} {P:.4f}±{e:.4f}     0.5934 (L→∞)")

print(f"\nINTERPRETATION:")
print(f"  - 3D spatial-only MC at β=6: ⟨P⟩ ≈ 0.46 (different theory)")
print(f"  - 3+1D = 4D Wilson MC at β=6: ⟨P⟩ → 0.5934 at L→∞")
print(f"  - The framework's '3+1D' claim REQUIRES temporal direction for")
print(f"    matching standard SU(3) Wilson value")
print(f"  - V-invariant L_s=2 APBC SPATIAL cube is structurally incomplete")
print(f"    for ⟨P⟩ derivation — it's missing temporal contributions")
