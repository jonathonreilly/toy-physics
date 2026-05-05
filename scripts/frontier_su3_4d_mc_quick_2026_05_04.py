"""Quick 4D MC test: confirm 3+1D framework MC reaches 0.5934 at modest L.

Faster version with smaller measurement counts and unbuffered output.
Goal: just verify the QUALITATIVE claim that 4D MC at β=6 gives ~0.59.
"""
import numpy as np
import time
import sys

np.random.seed(42)
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

def build_4d_lattice(Ls, Lt, apbc_dirs=()):
    """4D lattice. Default: PBC in all 4 directions (standard 4D Wilson)."""
    Ls_dims = [Ls, Ls, Ls, Lt]
    n_sites = Ls * Ls * Ls * Lt

    def site(x, y, z, t): return x + Ls*y + Ls*Ls*z + Ls*Ls*Ls*t

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

def avg_plaquette(plaquettes, links):
    s = 0.0
    for (flink, sign) in plaquettes:
        U = np.eye(3, dtype=complex)
        for (lid, orient) in flink:
            if orient == +1: U = U @ links[lid]
            else: U = U @ links[lid].conj().T
        s += sign * np.real(np.trace(U)) / 3.0
    return s / len(plaquettes)

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

def run_test(Ls, Lt, n_thermalize=500, n_measure=300):
    print(f"\n4D MC: Ls={Ls}, Lt={Lt}", flush=True)
    n_links, plaquettes = build_4d_lattice(Ls, Lt)
    l2f = [[] for _ in range(n_links)]
    for fidx, (flink, _) in enumerate(plaquettes):
        for (lid, _) in flink:
            if fidx not in l2f[lid]:
                l2f[lid].append(fidx)
    print(f"  Sites={Ls**3*Lt}, Links={n_links}, Plaquettes={len(plaquettes)}", flush=True)
    links = [np.eye(3, dtype=complex) for _ in range(n_links)]
    eps = 0.5
    t0 = time.time()
    for i in range(n_thermalize):
        acc = metropolis_sweep(links, plaquettes, eps, l2f)
        if (i+1) % 100 == 0:
            recent_p = avg_plaquette(plaquettes, links)
            print(f"  therm {i+1}: P={recent_p:.4f}, t={time.time()-t0:.0f}s", flush=True)
            if acc > 0.6: eps *= 1.05
            elif acc < 0.4: eps *= 0.95
    P_samples = []
    for i in range(n_measure):
        metropolis_sweep(links, plaquettes, eps, l2f)
        if i % 5 == 0:
            P_samples.append(avg_plaquette(plaquettes, links))
        if (i+1) % 100 == 0:
            print(f"  meas {i+1}: P={np.mean(P_samples):.4f}±{np.std(P_samples)/np.sqrt(len(P_samples)):.4f}, t={time.time()-t0:.0f}s", flush=True)
    P_mean = np.mean(P_samples)
    P_err = np.std(P_samples) / np.sqrt(len(P_samples))
    print(f"  RESULT Ls={Ls},Lt={Lt}: ⟨P⟩ = {P_mean:.4f} ± {P_err:.4f}", flush=True)
    return P_mean, P_err

# Run 4D MC at progressively larger L
print("Test: 4D Wilson SU(3) at β=6 on framework's 3+1D structure (full PBC)")
print("Standard MC reference: 0.5934 at L→∞")

P_22, e_22 = run_test(2, 2, n_thermalize=500, n_measure=300)
P_33, e_33 = run_test(3, 3, n_thermalize=500, n_measure=200)

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"Ls=2, Lt=2 (16 sites):   ⟨P⟩ = {P_22:.4f} ± {e_22:.4f}")
print(f"Ls=3, Lt=3 (81 sites):   ⟨P⟩ = {P_33:.4f} ± {e_33:.4f}")
print(f"Standard 4D L→∞:         ⟨P⟩ = 0.5934")
print()
print("Comparison to 3D-only spatial MC:")
print(f"  3D L=4 spatial APBC: ⟨P⟩ ≈ 0.46  (our previous result)")
print(f"  4D Ls,Lt scaling: P → ?")
print()
if P_33 > 0.55:
    print("✓ 4D MC reaches the 0.5934 region — temporal direction provides the missing piece")
    print("  Framework's gauge sector at full 3+1D matches standard SU(3) Wilson")
elif P_33 > 0.50:
    print("~ 4D MC partially closes the gap (P > 0.50 vs 3D-only ≈ 0.46)")
    print("  Larger L needed for full convergence to 0.5934")
else:
    print("✗ 4D MC still doesn't reach 0.5934 region")
    print("  Suggests something more than just '3D + 1 time' is needed")
