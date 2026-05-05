"""Test: anisotropic Wilson action with framework's (2/√3)^(1/4) temporal ratio.

Question: does the framework's Cl(3)/Z³ structure DEMAND anisotropic
spatial-temporal Wilson coupling? If so, what does ⟨P⟩(β=6) become?

Framework primitives that suggest possible anisotropy:
  - Per-site Cl(3) algebra lives on equal-time slices (spatial Z³)
  - Time direction is the unique reflection axis for RP
  - Staggered-Dirac action uses anisotropic phases η_t vs η_i
  - Temporal completion theorem gives (2/√3)^(1/4) ratio

Test: use anisotropic Wilson action
  S = (β_s/3) Σ_{spatial p} Re Tr U_p + (β_t/3) Σ_{mixed p} Re Tr U_p

with β_t = β_s × (2/√3)^(1/4) = β_s × 0.9576

For β_s = 6:
  β_t = 6 × 0.9576 = 5.745

Compare to isotropic at β = 6 → ⟨P⟩ = 0.5934 (standard MC).

If anisotropic gives DIFFERENT ⟨P⟩, this is potentially new framework physics.

Note: framework's GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM Theorem 1
explicitly rules out anisotropy in its "accepted Wilson surface". This
test EXPLORES whether allowing anisotropy would yield different (and
potentially better-matching) physics.
"""
import numpy as np
import time
import math

np.random.seed(11)
BETA_S = 6.0  # spatial coupling
TEMPORAL_RATIO = (2.0/math.sqrt(3))**0.25  # = 0.957603
BETA_T = BETA_S * TEMPORAL_RATIO  # = 5.745

print(f"Anisotropic Wilson MC test:")
print(f"  β_s = {BETA_S}")
print(f"  β_t = β_s × (2/√3)^(1/4) = {BETA_T:.4f}")
print(f"  Ratio β_t/β_s = {TEMPORAL_RATIO:.6f}")

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

def build_4d_lattice_anisotropic(Ls, Lt):
    """4D PBC lattice with anisotropy marker on plaquettes."""
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
    link_dirs = []  # 0,1,2 = spatial, 3 = temporal
    link_idx = {}
    for s in range(n_sites):
        coords = coords_for(s)
        for d in range(4):
            new_coords = coords.copy()
            new_coords[d] = (new_coords[d] + 1) % Ls_dims[d]
            link_idx[(s, d)] = len(links)
            links.append(s)
            link_dirs.append(d)

    plaquettes = []  # (links, is_temporal)
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
                # Plaquette is "temporal" if it contains a temporal link (i=3 or j=3)
                is_temporal = (i == 3 or j == 3)
                plaquettes.append(([(l1, +1), (l2, +1), (l3, -1), (l4, -1)], is_temporal))
    return len(links), plaquettes

def avg_plaquette_split(plaquettes, links):
    """Return (P_spatial, P_temporal) averages separately."""
    s_spatial = 0.0
    s_temporal = 0.0
    n_spatial = 0
    n_temporal = 0
    for (flink, is_temporal) in plaquettes:
        U = np.eye(3, dtype=complex)
        for (lid, orient) in flink:
            if orient == +1: U = U @ links[lid]
            else: U = U @ links[lid].conj().T
        p = np.real(np.trace(U)) / 3.0
        if is_temporal:
            s_temporal += p
            n_temporal += 1
        else:
            s_spatial += p
            n_spatial += 1
    return (s_spatial/n_spatial if n_spatial else 0,
            s_temporal/n_temporal if n_temporal else 0,
            (s_spatial + s_temporal)/(n_spatial + n_temporal))

def metropolis_sweep_aniso(links, plaquettes, eps, link_to_faces, beta_s, beta_t):
    n_accept = 0
    n_total = 0
    for lid in range(len(links)):
        U_old = links[lid].copy()
        V = random_perturbation(eps)
        U_new = V @ U_old
        S_old = 0.0
        S_new = 0.0
        for fidx in link_to_faces[lid]:
            flink, is_temporal = plaquettes[fidx]
            beta_use = beta_t if is_temporal else beta_s
            U_p_old = np.eye(3, dtype=complex)
            for (l, orient) in flink:
                if orient == +1: U_p_old = U_p_old @ links[l]
                else: U_p_old = U_p_old @ links[l].conj().T
            s_old_val = (beta_use/3.0) * np.real(np.trace(U_p_old))
            links[lid] = U_new
            U_p_new = np.eye(3, dtype=complex)
            for (l, orient) in flink:
                if orient == +1: U_p_new = U_p_new @ links[l]
                else: U_p_new = U_p_new @ links[l].conj().T
            s_new_val = (beta_use/3.0) * np.real(np.trace(U_p_new))
            links[lid] = U_old
            S_old += s_old_val
            S_new += s_new_val
        # Action: S = -(β/3) Σ Re Tr U_p, so action change is -(S_new - S_old)
        dS = -(S_new - S_old)
        n_total += 1
        if dS < 0 or np.random.rand() < np.exp(-dS):
            links[lid] = U_new
            n_accept += 1
    return n_accept / n_total

def run_aniso(Ls, Lt, beta_s, beta_t, label, n_thermalize=400, n_measure=1000):
    print(f"\n{'='*60}", flush=True)
    print(f"{label} (Ls={Ls}, Lt={Lt}, β_s={beta_s}, β_t={beta_t:.4f})", flush=True)
    print(f"{'='*60}", flush=True)
    n_links, plaquettes = build_4d_lattice_anisotropic(Ls, Lt)
    l2f = [[] for _ in range(n_links)]
    for fidx, (flink, _) in enumerate(plaquettes):
        for (lid, _) in flink:
            if fidx not in l2f[lid]: l2f[lid].append(fidx)
    print(f"  Sites={Ls**3*Lt}, Links={n_links}, Plaquettes={len(plaquettes)}", flush=True)
    links = [np.eye(3, dtype=complex) for _ in range(n_links)]
    eps = 0.5
    t0 = time.time()
    for i in range(n_thermalize):
        acc = metropolis_sweep_aniso(links, plaquettes, eps, l2f, beta_s, beta_t)
        if (i+1) % 100 == 0:
            P_s, P_t, P_avg = avg_plaquette_split(plaquettes, links)
            print(f"  therm {i+1}: P_s={P_s:.4f}, P_t={P_t:.4f}, P_avg={P_avg:.4f}, t={time.time()-t0:.0f}s", flush=True)
            if acc > 0.6: eps *= 1.05
            elif acc < 0.4: eps *= 0.95
    P_s_samples = []
    P_t_samples = []
    P_avg_samples = []
    for i in range(n_measure):
        metropolis_sweep_aniso(links, plaquettes, eps, l2f, beta_s, beta_t)
        if i % 5 == 0:
            P_s, P_t, P_avg = avg_plaquette_split(plaquettes, links)
            P_s_samples.append(P_s); P_t_samples.append(P_t); P_avg_samples.append(P_avg)
        if (i+1) % 200 == 0:
            print(f"  meas {i+1}: P_s={np.mean(P_s_samples):.4f}, P_t={np.mean(P_t_samples):.4f}, t={time.time()-t0:.0f}s", flush=True)
    return {
        'P_s': (np.mean(P_s_samples), np.std(P_s_samples)/np.sqrt(len(P_s_samples))),
        'P_t': (np.mean(P_t_samples), np.std(P_t_samples)/np.sqrt(len(P_t_samples))),
        'P_avg': (np.mean(P_avg_samples), np.std(P_avg_samples)/np.sqrt(len(P_avg_samples))),
    }

# Test 1: ISOTROPIC reference (β_s = β_t = 6)
print("\n" + "#"*60)
print("# Test 1: ISOTROPIC β_s = β_t = 6 (framework's accepted Wilson)")
print("#"*60)
iso = run_aniso(3, 3, 6.0, 6.0, "ISOTROPIC reference")

# Test 2: ANISOTROPIC with framework's temporal ratio
print("\n" + "#"*60)
print(f"# Test 2: ANISOTROPIC β_t/β_s = (2/√3)^(1/4) = {TEMPORAL_RATIO:.4f}")
print("# β_s = 6.0, β_t = 5.745")
print("#"*60)
aniso = run_aniso(3, 3, BETA_S, BETA_T, "ANISOTROPIC (2/√3)^(1/4) ratio")

# Compare results
print(f"\n{'='*60}")
print(f"COMPARISON")
print(f"{'='*60}\n")
print(f"  Quantity       ISOTROPIC (β=6)       ANISOTROPIC (β_s=6, β_t=5.745)")
print(f"  ------------   --------------------  -----------------------------")
print(f"  ⟨P_spatial⟩    {iso['P_s'][0]:.4f}±{iso['P_s'][1]:.4f}      {aniso['P_s'][0]:.4f}±{aniso['P_s'][1]:.4f}")
print(f"  ⟨P_temporal⟩   {iso['P_t'][0]:.4f}±{iso['P_t'][1]:.4f}      {aniso['P_t'][0]:.4f}±{aniso['P_t'][1]:.4f}")
print(f"  ⟨P_avg⟩        {iso['P_avg'][0]:.4f}±{iso['P_avg'][1]:.4f}      {aniso['P_avg'][0]:.4f}±{aniso['P_avg'][1]:.4f}")
print(f"\n  Standard 4D Wilson MC L→∞ at β=6: 0.5934")
print(f"  Framework Ls=Lt=3 PBC at β=6: 0.6034 (from PR #528)")
print()
print(f"INTERPRETATION:")
diff_avg = aniso['P_avg'][0] - iso['P_avg'][0]
print(f"  ⟨P_avg⟩ shift due to anisotropy: {diff_avg:+.4f}")
print(f"  (~{abs(diff_avg)/iso['P_avg'][0]*100:.1f}% change)")

if abs(diff_avg) > 3*max(iso['P_avg'][1], aniso['P_avg'][1]):
    print("  → Anisotropy SIGNIFICANTLY shifts ⟨P⟩ (statistically detectable)")
    print("  → Framework's chosen isotropy IS a substantive specification")
    print("  → Anisotropic version is a candidate alternative framework physics")
else:
    print("  → Anisotropy shift is below statistical noise")
    print("  → Framework's isotropy choice may not be load-bearing for ⟨P⟩")
print()
print(f"TEMPORAL/SPATIAL ASYMMETRY (anisotropic case):")
asym = aniso['P_t'][0] - aniso['P_s'][0]
print(f"  P_temporal - P_spatial = {asym:+.4f}")
print(f"  (Expected: P_t < P_s since β_t < β_s)")
print(f"  Confirmed: P_t = {aniso['P_t'][0]:.4f} < P_s = {aniso['P_s'][0]:.4f}: {aniso['P_t'][0] < aniso['P_s'][0]}")
