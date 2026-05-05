"""Compute χ_L(β) profile via MC at multiple β values for susceptibility-flow ODE.

Framework's susceptibility-flow theorem:
  β_eff'(β) = χ_L(β) / χ_1plaq(β_eff(β))

where χ_L(β) = Var(action density)/N_plaq = ⟨P²⟩_conn (per plaquette).

Goal: MC at β = 1, 2, 3, 4, 5, 6 → χ_L profile → integrate ODE → β_eff(6) → P(6).

This is closure candidate #5 implementation: framework's exact reduction-law
theorem says P(β) = P_1plaq(β_eff(β)) UNIQUELY. If we determine β_eff(6),
we close ⟨P⟩(β=6) analytically (P_1plaq is exactly known).
"""
import numpy as np
import time
import json

np.random.seed(7777)
LS = 4  # use L=4 (faster)
LT = 4

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

def metropolis_sweep(links, plaquettes, eps, link_to_faces, beta):
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
        dS = -(beta / 3.0) * (S_new - S_old)
        n_total += 1
        if dS < 0 or np.random.rand() < np.exp(-dS):
            links[lid] = U_new
            n_accept += 1
    return n_accept / n_total

def run_mc_at_beta(beta, n_thermalize=200, n_measure=400):
    print(f"\nβ={beta}: setup...", flush=True)
    n_links, plaquettes = build_4d_lattice(LS, LT)
    l2f = [[] for _ in range(n_links)]
    for fidx, flink in enumerate(plaquettes):
        for (lid, _) in flink:
            if fidx not in l2f[lid]: l2f[lid].append(fidx)
    links = [np.eye(3, dtype=complex) for _ in range(n_links)]
    eps = 0.5
    t0 = time.time()
    print(f"  Thermalize {n_thermalize} sweeps...", flush=True)
    for i in range(n_thermalize):
        acc = metropolis_sweep(links, plaquettes, eps, l2f, beta)
        if (i+1) % 100 == 0:
            print(f"    therm {i+1}: P={avg_plaquette(plaquettes, links):.4f}, t={time.time()-t0:.0f}s", flush=True)
            if acc > 0.6: eps *= 1.05
            elif acc < 0.4: eps *= 0.95
    print(f"  Measure {n_measure} sweeps...", flush=True)
    P_samples = []
    for i in range(n_measure):
        metropolis_sweep(links, plaquettes, eps, l2f, beta)
        if i % 4 == 0:
            P_samples.append(avg_plaquette(plaquettes, links))
        if (i+1) % 100 == 0 and len(P_samples) > 0:
            print(f"    meas {i+1}: P={np.mean(P_samples):.4f}±{np.std(P_samples)/np.sqrt(len(P_samples)):.4f}, t={time.time()-t0:.0f}s", flush=True)
    P_mean = np.mean(P_samples)
    P_err = np.std(P_samples) / np.sqrt(len(P_samples))
    P_var = np.var(P_samples)  # Var(P) — proportional to χ_L per plaquette (with normalization)
    chi_L_estimate = P_var * len(plaquettes)  # χ_L = N_plaq · Var(<P>) since <P> = (1/N_plaq) Σ P_p
    print(f"  RESULT β={beta}: ⟨P⟩={P_mean:.4f}±{P_err:.4f}, Var(P)={P_var:.6f}, χ_L≈{chi_L_estimate:.4f}", flush=True)
    return P_mean, P_err, chi_L_estimate

# Run at multiple β values
results = {}
for beta in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]:
    P, err, chi_L = run_mc_at_beta(beta, n_thermalize=200, n_measure=400)
    results[beta] = {'P': P, 'err': err, 'chi_L': chi_L}

print(f"\n{'='*60}")
print(f"χ_L(β) PROFILE (framework-native MC)")
print(f"{'='*60}")
print(f"{'β':>6s} {'⟨P⟩':>9s} {'err':>8s} {'χ_L':>10s}")
for beta in sorted(results.keys()):
    r = results[beta]
    print(f"{beta:>6.1f} {r['P']:>9.4f} ±{r['err']:>6.4f} {r['chi_L']:>10.4f}")

# Save for ODE integration
with open('/tmp/chi_L_profile_mc.json', 'w') as f:
    json.dump({str(k): v for k, v in results.items()}, f, indent=2)
print(f"\nSaved χ_L profile to /tmp/chi_L_profile_mc.json")

# Compare to framework's χ_1plaq
print(f"\n{'='*60}")
print(f"Compare χ_L (MC) to χ_1plaq (analytic Bessel)")
print(f"{'='*60}")

import sys
sys.path.insert(0, '/Users/jonBridger/Toy Physics/.claude/worktrees/romantic-moore-d6c92d/scripts')
from frontier_su3_lib_2026_05_05 import c_lambda

def chi_1plaq(beta, h=0.01):
    P_minus = c_lambda(1, 0, beta-h) / (3 * c_lambda(0, 0, beta-h))
    P_plus = c_lambda(1, 0, beta+h) / (3 * c_lambda(0, 0, beta+h))
    return (P_plus - P_minus) / (2*h)

print(f"{'β':>6s} {'χ_L (MC)':>10s} {'χ_1plaq':>10s} {'ratio':>8s}")
for beta in sorted(results.keys()):
    chi_1 = chi_1plaq(beta)
    chi_L = results[beta]['chi_L']
    ratio = chi_L / chi_1 if chi_1 > 0 else 0
    print(f"{beta:>6.1f} {chi_L:>10.4f} {chi_1:>10.4f} {ratio:>8.2f}")

print(f"""
INTERPRETATION:
  χ_L(β) is the connected susceptibility (full theory)
  χ_1plaq(β) is the single-plaquette susceptibility (framework analytical)
  Ratio χ_L/χ_1plaq tells us how much "extra" correlation enters at finite β

For framework's susceptibility-flow ODE:
  β_eff'(β) = χ_L(β) / χ_1plaq(β_eff(β))

This integration gives β_eff(6), then P(6) = P_1plaq(β_eff(6)).
The χ_L profile is what's needed to do this integration framework-natively.
""")
