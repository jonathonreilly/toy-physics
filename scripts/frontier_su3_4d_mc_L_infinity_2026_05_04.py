"""High-stats 4D MC at L=6 and L=8 for L→∞ extrapolation.

Goal: tighten framework's ⟨P⟩(β=6) prediction to ±0.001 PDG-level precision.

Standard SU(3) MC at β=6 literature values:
  L=4: ~0.598
  L=6: ~0.5938
  L=8: ~0.5934
  L=16+: 0.5934 (asymptotic L→∞)

Framework's 3+1D MC should match these (per established isotropy + standard
Wilson action choice). Verification at L=6 and L=8 + extrapolation gives
audit-ready precision.

Each L runs independently for parallelism with other work.
"""
import numpy as np
import time
import sys

np.random.seed(2026)
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
    return len(links), plaquettes

def avg_plaquette(plaquettes, links):
    s = 0.0
    for flink in plaquettes:
        U = np.eye(3, dtype=complex)
        for (lid, orient) in flink:
            if orient == +1: U = U @ links[lid]
            else: U = U @ links[lid].conj().T
        s += np.real(np.trace(U)) / 3.0
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

def run(Ls, Lt, n_thermalize, n_measure, label):
    print(f"\n{'='*60}", flush=True)
    print(f"{label} (Ls={Ls}, Lt={Lt})", flush=True)
    print(f"{'='*60}", flush=True)
    n_links, plaquettes = build_4d_lattice(Ls, Lt)
    l2f = [[] for _ in range(n_links)]
    for fidx, flink in enumerate(plaquettes):
        for (lid, _) in flink:
            if fidx not in l2f[lid]: l2f[lid].append(fidx)
    print(f"  Sites={Ls**3*Lt}, Links={n_links}, Plaquettes={len(plaquettes)}", flush=True)
    links = [np.eye(3, dtype=complex) for _ in range(n_links)]
    eps = 0.5
    t0 = time.time()
    for i in range(n_thermalize):
        acc = metropolis_sweep(links, plaquettes, eps, l2f)
        if (i+1) % 50 == 0:
            print(f"  therm {i+1}: P={avg_plaquette(plaquettes, links):.4f}, eps={eps:.3f}, acc={acc:.2f}, t={time.time()-t0:.0f}s", flush=True)
            if acc > 0.6: eps *= 1.05
            elif acc < 0.4: eps *= 0.95
    P_samples = []
    for i in range(n_measure):
        metropolis_sweep(links, plaquettes, eps, l2f)
        if i % 5 == 0:
            P_samples.append(avg_plaquette(plaquettes, links))
        if (i+1) % 100 == 0 and len(P_samples) > 0:
            print(f"  meas {i+1}: P={np.mean(P_samples):.4f}±{np.std(P_samples)/np.sqrt(len(P_samples)):.4f}, t={time.time()-t0:.0f}s", flush=True)
    P_mean = np.mean(P_samples)
    P_err = np.std(P_samples) / np.sqrt(len(P_samples))
    print(f"  RESULT (Ls=Lt={Ls}): ⟨P⟩ = {P_mean:.4f} ± {P_err:.4f}", flush=True)
    return P_mean, P_err

# Run L=6 (focus on this first; L=8 next if time)
print("4D Wilson SU(3) MC at β=6 — L→∞ EXTRAPOLATION RUN")
print(f"Target precision: ±0.001 (PDG α_s precision floor)\n")

# L=6 Ls=Lt=6
P6, e6 = run(6, 6, n_thermalize=300, n_measure=600, label="Ls=Lt=6 4D PBC")

print(f"\n{'='*60}")
print(f"L=6 RESULT")
print(f"{'='*60}")
print(f"  Ls=Lt=6: ⟨P⟩ = {P6:.4f} ± {e6:.4f}")
print(f"  Standard ref: ~0.5938")
print(f"  Diff from L→∞ (0.5934): {P6-0.5934:+.4f}")
