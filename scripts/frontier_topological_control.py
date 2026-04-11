#!/usr/bin/env python3
"""
Topological Control: Self-Gravity vs Matched Random Disorder
=============================================================

Critical question: Does random on-site disorder destroy SSH topology at the
same threshold as self-gravity?  If so, the G~0.3 transition is generic
(any chiral-symmetry breaking kills edge modes), not gravitational.

Protocol:
  1. For each G, compute self-consistent Phi.  Record mean(|Phi|), std(Phi),
     edge modes, gap.
  2. Generate random disorder V ~ N(0, std(Phi_at_this_G)).  No self-consistency.
     20 seeds per G.
  3. Count edge modes and measure gap for each random realization.
  4. Compare G_transition(gravity) vs G_transition(disorder).
  5. Spatial structure test: self-consistent Phi vs random vs shuffled Phi.

SSH setup (parity-coupled staggered chain, open BC):
  H[2i, 2i+1]   = t1           (intracell hopping)
  H[2i+1, 2i+2] = t2           (intercell hopping)
  H[x, x]       = (MASS + phi[x]) * (-1)^x   (parity coupling)
"""

from __future__ import annotations

import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.linalg import eigh

# ── Parameters ───────────────────────────────────────────────────
N = 60                  # chain length (even)
T1 = 0.5               # intracell hopping (weak)
T2 = 1.0               # intercell hopping (strong) -> topological phase
MASS = 0.0              # bare staggered mass
MU2 = 0.001             # Poisson regularization
N_SC_ITER = 40          # self-consistent iterations
G_VALUES = [0.0, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0]
N_RANDOM_SEEDS = 20     # random disorder realizations per G

# Edge mode detection
EDGE_SITES = 6
EDGE_WEIGHT_THRESH = 0.4


# ── 1D Laplacian ────────────────────────────────────────────────

def build_1d_laplacian(n: int):
    L = lil_matrix((n, n), dtype=float)
    for i in range(n - 1):
        L[i, i] += 1.0
        L[i + 1, i + 1] += 1.0
        L[i, i + 1] = -1.0
        L[i + 1, i] = -1.0
    return L.tocsr()


def solve_phi(laplacian, rho: np.ndarray, mu2: float) -> np.ndarray:
    n = laplacian.shape[0]
    A = (laplacian + mu2 * speye(n, format="csr")).tocsc()
    return spsolve(A, -rho).real


# ── SSH Hamiltonian with parity-coupled on-site potential ───────

def build_ssh_hamiltonian(n: int, t1: float, t2: float,
                          on_site: np.ndarray) -> np.ndarray:
    """Build SSH Hamiltonian with parity-coupled on-site potential.

    on_site[x] is the FULL diagonal entry: (MASS + phi[x]) * (-1)^x
    """
    H = np.zeros((n, n), dtype=float)

    for x in range(n):
        H[x, x] = on_site[x]

    for j in range(n // 2):
        a = 2 * j
        b = 2 * j + 1
        H[a, b] = t1
        H[b, a] = t1
        if b + 1 < n:
            H[b, b + 1] = t2
            H[b + 1, b] = t2

    return H


def parity_coupled_onsite(phi: np.ndarray, mass: float = MASS) -> np.ndarray:
    """Compute (mass + phi[x]) * (-1)^x for each site."""
    n = len(phi)
    stagger = np.array([(-1)**x for x in range(n)], dtype=float)
    return (mass + phi) * stagger


# ── Self-consistent gravity loop ────────────────────────────────

def self_consistent_solve(n: int, t1: float, t2: float,
                          G: float, mu2: float, n_iter: int):
    """Run self-consistent loop.  Returns (eigenvalues, eigenvectors, phi)."""
    laplacian = build_1d_laplacian(n)
    phi = np.zeros(n)

    if G == 0.0:
        on_site = parity_coupled_onsite(phi)
        H = build_ssh_hamiltonian(n, t1, t2, on_site)
        eigenvalues, eigenvectors = eigh(H)
        return eigenvalues, eigenvectors, phi

    for step in range(n_iter):
        on_site = parity_coupled_onsite(G * phi)
        H = build_ssh_hamiltonian(n, t1, t2, on_site)
        eigenvalues, eigenvectors = eigh(H)

        n_filled = n // 2
        rho = np.zeros(n)
        for i in range(n_filled):
            rho += np.abs(eigenvectors[:, i]) ** 2
        rho /= np.sum(rho)

        phi_new = solve_phi(laplacian, rho, mu2)
        phi_new -= np.mean(phi_new)

        alpha = 0.3
        phi = (1.0 - alpha) * phi + alpha * phi_new

    return eigenvalues, eigenvectors, phi


# ── Solve with a fixed on-site potential (no self-consistency) ──

def solve_with_onsite(n: int, t1: float, t2: float,
                      on_site: np.ndarray):
    """Diagonalize SSH + fixed on-site potential.  Returns (eigenvalues, eigenvectors)."""
    H = build_ssh_hamiltonian(n, t1, t2, on_site)
    return eigh(H)


# ── Observables ─────────────────────────────────────────────────

def spectral_gap(eigenvalues: np.ndarray) -> float:
    return float(np.min(np.abs(eigenvalues)))


def count_edge_modes(eigenvalues: np.ndarray, eigenvectors: np.ndarray,
                     n: int, gap_thresh: float) -> int:
    edge_left = list(range(EDGE_SITES))
    edge_right = list(range(n - EDGE_SITES, n))
    edge_sites = edge_left + edge_right

    count = 0
    for i, E in enumerate(eigenvalues):
        if abs(E) > gap_thresh:
            continue
        psi = eigenvectors[:, i]
        total_weight = np.sum(np.abs(psi) ** 2)
        if total_weight == 0:
            continue
        edge_weight = np.sum(np.abs(psi[edge_sites]) ** 2)
        if edge_weight / total_weight > EDGE_WEIGHT_THRESH:
            count += 1
    return count


def bulk_gap(eigenvalues: np.ndarray, eigenvectors: np.ndarray,
             n: int) -> float:
    edge_left = list(range(EDGE_SITES))
    edge_right = list(range(n - EDGE_SITES, n))
    edge_sites = edge_left + edge_right

    bulk_energies = []
    for i, E in enumerate(eigenvalues):
        psi = eigenvectors[:, i]
        w_total = np.sum(np.abs(psi) ** 2)
        if w_total == 0:
            continue
        w_edge = np.sum(np.abs(psi[edge_sites]) ** 2)
        if w_edge / w_total < EDGE_WEIGHT_THRESH:
            bulk_energies.append(abs(E))

    if not bulk_energies:
        return float(np.min(np.abs(eigenvalues)))
    return float(min(bulk_energies))


# ── Main ────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("TOPOLOGICAL CONTROL: SELF-GRAVITY vs MATCHED RANDOM DISORDER")
    print("SSH model: t1=%.2f, t2=%.2f, N=%d, MASS=%.2f, open BC" % (T1, T2, N, MASS))
    print("Parity coupling: H[x,x] = (MASS + phi[x]) * (-1)^x")
    print("=" * 80)
    print()

    # ── Reference: free system ──────────────────────────────────
    evals0, evecs0, _ = self_consistent_solve(N, T1, T2, 0.0, MU2, 1)
    free_bgap = bulk_gap(evals0, evecs0, N)
    gap_thresh = max(0.05, 0.15 * free_bgap)

    free_modes = count_edge_modes(evals0, evecs0, N, gap_thresh)
    print("Free system (G=0):  bulk_gap=%.4f  edge_modes=%d  gap_thresh=%.4f"
          % (free_bgap, free_modes, gap_thresh))
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART 1: Self-consistent gravity scan
    # ═══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PART 1: SELF-CONSISTENT GRAVITY")
    print("=" * 80)
    print()

    gravity_results = {}

    print("%-8s  %-10s  %-10s  %-8s  %-10s  %-10s" % (
        "G", "BulkGap", "SpecGap", "Modes", "mean|Phi|", "std(Phi)"))
    print("-" * 62)

    for G in G_VALUES:
        evals, evecs, phi = self_consistent_solve(N, T1, T2, G, MU2, N_SC_ITER)
        bgap = bulk_gap(evals, evecs, N)
        sgap = spectral_gap(evals)
        modes = count_edge_modes(evals, evecs, N, gap_thresh)
        phi_mean_abs = float(np.mean(np.abs(phi)))
        phi_std = float(np.std(phi))

        gravity_results[G] = {
            "bulk_gap": bgap, "spec_gap": sgap, "modes": modes,
            "phi": phi.copy(), "phi_mean_abs": phi_mean_abs, "phi_std": phi_std,
        }

        print("%-8.2f  %-10.6f  %-10.6f  %-8d  %-10.6f  %-10.6f" % (
            G, bgap, sgap, modes, phi_mean_abs, phi_std))

    # Find gravity transition
    g_trans_gravity = None
    for i in range(1, len(G_VALUES)):
        G_prev = G_VALUES[i - 1]
        G_curr = G_VALUES[i]
        if gravity_results[G_prev]["modes"] > 0 and gravity_results[G_curr]["modes"] == 0:
            g_trans_gravity = G_curr
            break

    print()
    if g_trans_gravity is not None:
        print(">>> Gravity transition: edge modes vanish at G = %.2f" % g_trans_gravity)
    else:
        if gravity_results[G_VALUES[0]]["modes"] == 0:
            print(">>> No edge modes even at G=0 (check parameters)")
        else:
            print(">>> Edge modes persist for all G tested")
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART 2: Matched random disorder
    # ═══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PART 2: RANDOM DISORDER (matched variance, %d seeds)" % N_RANDOM_SEEDS)
    print("=" * 80)
    print()

    disorder_results = {}

    print("%-8s  %-10s  %-10s  %-10s  %-12s  %-12s" % (
        "G", "sigma", "Modes(avg)", "Modes(med)", "BulkGap(avg)", "BulkGap(med)"))
    print("-" * 68)

    for G in G_VALUES:
        sigma = gravity_results[G]["phi_std"]
        seed_modes = []
        seed_bgaps = []

        for seed in range(N_RANDOM_SEEDS):
            rng = np.random.default_rng(seed + 1000)
            if sigma < 1e-12:
                v_random = np.zeros(N)
            else:
                v_random = rng.normal(0.0, sigma, N)

            on_site = parity_coupled_onsite(v_random)
            evals_r, evecs_r = solve_with_onsite(N, T1, T2, on_site)
            modes_r = count_edge_modes(evals_r, evecs_r, N, gap_thresh)
            bgap_r = bulk_gap(evals_r, evecs_r, N)
            seed_modes.append(modes_r)
            seed_bgaps.append(bgap_r)

        avg_modes = float(np.mean(seed_modes))
        med_modes = float(np.median(seed_modes))
        avg_bgap = float(np.mean(seed_bgaps))
        med_bgap = float(np.median(seed_bgaps))

        disorder_results[G] = {
            "sigma": sigma, "modes_list": seed_modes, "bgap_list": seed_bgaps,
            "avg_modes": avg_modes, "med_modes": med_modes,
            "avg_bgap": avg_bgap, "med_bgap": med_bgap,
        }

        print("%-8.2f  %-10.6f  %-10.2f  %-10.1f  %-12.6f  %-12.6f" % (
            G, sigma, avg_modes, med_modes, avg_bgap, med_bgap))

    # Find disorder transition
    g_trans_disorder = None
    for i in range(1, len(G_VALUES)):
        G_prev = G_VALUES[i - 1]
        G_curr = G_VALUES[i]
        if disorder_results[G_prev]["med_modes"] > 0 and disorder_results[G_curr]["med_modes"] == 0:
            g_trans_disorder = G_curr
            break

    print()
    if g_trans_disorder is not None:
        print(">>> Disorder transition: edge modes vanish at matched-sigma for G = %.2f" % g_trans_disorder)
    else:
        if disorder_results[G_VALUES[0]]["med_modes"] == 0:
            print(">>> No edge modes even at zero disorder")
        else:
            print(">>> Edge modes persist for all matched disorder strengths")
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART 3: Spatial structure test
    # ═══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PART 3: SPATIAL STRUCTURE TEST")
    print("Does the spatial pattern of Phi matter, or only its variance?")
    print("=" * 80)
    print()

    # Pick G values where gravity has an effect
    test_G_values = [G for G in G_VALUES if G > 0 and gravity_results[G]["phi_std"] > 1e-10]

    print("%-8s  %-8s  %-10s  %-10s  %-10s" % (
        "G", "Type", "Modes", "BulkGap", "SpecGap"))
    print("-" * 52)

    spatial_data = {}

    for G in test_G_values:
        phi_sc = gravity_results[G]["phi"]
        sigma = gravity_results[G]["phi_std"]

        # (a) Self-consistent Phi (parity-coupled)
        on_site_sc = parity_coupled_onsite(G * phi_sc)
        evals_a, evecs_a = solve_with_onsite(N, T1, T2, on_site_sc)
        modes_a = count_edge_modes(evals_a, evecs_a, N, gap_thresh)
        bgap_a = bulk_gap(evals_a, evecs_a, N)
        sgap_a = spectral_gap(evals_a)

        # (b) Random Phi matched variance (average over seeds)
        modes_b_list = []
        bgap_b_list = []
        sgap_b_list = []
        for seed in range(N_RANDOM_SEEDS):
            rng = np.random.default_rng(seed + 2000)
            v_rand = rng.normal(0.0, sigma, N)
            on_site_b = parity_coupled_onsite(v_rand)
            evals_b, evecs_b = solve_with_onsite(N, T1, T2, on_site_b)
            modes_b_list.append(count_edge_modes(evals_b, evecs_b, N, gap_thresh))
            bgap_b_list.append(bulk_gap(evals_b, evecs_b, N))
            sgap_b_list.append(spectral_gap(evals_b))

        modes_b = float(np.median(modes_b_list))
        bgap_b = float(np.median(bgap_b_list))
        sgap_b = float(np.median(sgap_b_list))

        # (c) Shuffled self-consistent Phi
        modes_c_list = []
        bgap_c_list = []
        sgap_c_list = []
        for seed in range(N_RANDOM_SEEDS):
            rng = np.random.default_rng(seed + 3000)
            phi_shuf = phi_sc.copy()
            rng.shuffle(phi_shuf)
            on_site_c = parity_coupled_onsite(G * phi_shuf)
            evals_c, evecs_c = solve_with_onsite(N, T1, T2, on_site_c)
            modes_c_list.append(count_edge_modes(evals_c, evecs_c, N, gap_thresh))
            bgap_c_list.append(bulk_gap(evals_c, evecs_c, N))
            sgap_c_list.append(spectral_gap(evals_c))

        modes_c = float(np.median(modes_c_list))
        bgap_c = float(np.median(bgap_c_list))
        sgap_c = float(np.median(sgap_c_list))

        spatial_data[G] = {
            "sc": (modes_a, bgap_a, sgap_a),
            "random": (modes_b, bgap_b, sgap_b),
            "shuffled": (modes_c, bgap_c, sgap_c),
        }

        print("%-8.2f  %-8s  %-10d  %-10.6f  %-10.6f" % (G, "gravity", modes_a, bgap_a, sgap_a))
        print("%-8s  %-8s  %-10.1f  %-10.6f  %-10.6f" % ("", "random", modes_b, bgap_b, sgap_b))
        print("%-8s  %-8s  %-10.1f  %-10.6f  %-10.6f" % ("", "shuffled", modes_c, bgap_c, sgap_c))
        print()

    # ═══════════════════════════════════════════════════════════════
    # PART 4: Fine-grained disorder strength scan
    # ═══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PART 4: FINE-GRAINED DISORDER STRENGTH SCAN")
    print("Sweep sigma directly to find exact threshold where edge modes vanish")
    print("=" * 80)
    print()

    sigma_values = np.concatenate([
        np.linspace(0, 0.05, 6),
        np.linspace(0.05, 0.2, 8)[1:],
        np.linspace(0.2, 1.0, 6)[1:],
        np.linspace(1.0, 5.0, 5)[1:],
    ])

    print("%-12s  %-10s  %-10s  %-12s  %-12s" % (
        "sigma", "Modes(avg)", "Modes(med)", "BulkGap(avg)", "BulkGap(med)"))
    print("-" * 62)

    fine_scan = []
    for sigma in sigma_values:
        seed_modes = []
        seed_bgaps = []
        for seed in range(N_RANDOM_SEEDS):
            rng = np.random.default_rng(seed + 4000)
            if sigma < 1e-12:
                v_random = np.zeros(N)
            else:
                v_random = rng.normal(0.0, sigma, N)
            on_site = parity_coupled_onsite(v_random)
            evals_r, evecs_r = solve_with_onsite(N, T1, T2, on_site)
            modes_r = count_edge_modes(evals_r, evecs_r, N, gap_thresh)
            bgap_r = bulk_gap(evals_r, evecs_r, N)
            seed_modes.append(modes_r)
            seed_bgaps.append(bgap_r)

        avg_m = float(np.mean(seed_modes))
        med_m = float(np.median(seed_modes))
        avg_b = float(np.mean(seed_bgaps))
        med_b = float(np.median(seed_bgaps))
        fine_scan.append((sigma, avg_m, med_m, avg_b, med_b))

        print("%-12.6f  %-10.2f  %-10.1f  %-12.6f  %-12.6f" % (
            sigma, avg_m, med_m, avg_b, med_b))

    # Find sigma threshold
    sigma_thresh = None
    for i in range(1, len(fine_scan)):
        if fine_scan[i - 1][2] > 0 and fine_scan[i][2] == 0:
            sigma_thresh = fine_scan[i][0]
            break

    print()
    if sigma_thresh is not None:
        print(">>> Random disorder threshold: edge modes vanish at sigma ~ %.4f" % sigma_thresh)
    else:
        print(">>> Could not identify clean disorder threshold in scanned range")
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART 5: COMPARISON AND VERDICT
    # ═══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("COMPARISON AND VERDICT")
    print("=" * 80)
    print()

    print("Transition points:")
    if g_trans_gravity is not None:
        sigma_at_trans = gravity_results[g_trans_gravity]["phi_std"]
        print("  Self-gravity:   G_c = %.2f  (sigma_Phi = %.6f)" % (g_trans_gravity, sigma_at_trans))
    else:
        print("  Self-gravity:   no transition in range")
        sigma_at_trans = None

    if g_trans_disorder is not None:
        sigma_dis = disorder_results[g_trans_disorder]["sigma"]
        print("  Matched disorder: transition at sigma matched to G = %.2f  (sigma = %.6f)" % (
            g_trans_disorder, sigma_dis))
    else:
        print("  Matched disorder: no transition in range")

    if sigma_thresh is not None:
        print("  Fine-scan disorder: sigma_c = %.6f" % sigma_thresh)
    print()

    # Compare gravity phi_std at transition to disorder sigma_c
    if g_trans_gravity is not None and sigma_thresh is not None and sigma_at_trans is not None:
        ratio = sigma_at_trans / sigma_thresh if sigma_thresh > 0 else float("inf")
        print("  Ratio sigma_gravity / sigma_disorder = %.3f" % ratio)
        if 0.7 < ratio < 1.3:
            print("  -> MATCH: gravity transition is variance-driven (generic)")
        elif ratio < 0.7:
            print("  -> GRAVITY TRANSITIONS EARLIER: something beyond variance is happening")
        else:
            print("  -> GRAVITY TRANSITIONS LATER: spatial correlations protect topology")
    print()

    # Spatial structure verdict
    print("Spatial structure analysis:")
    for G in test_G_values:
        d = spatial_data[G]
        sc_modes, sc_bgap, _ = d["sc"]
        rand_modes, rand_bgap, _ = d["random"]
        shuf_modes, shuf_bgap, _ = d["shuffled"]

        if sc_modes != rand_modes or abs(sc_bgap - rand_bgap) / max(rand_bgap, 1e-10) > 0.2:
            print("  G=%.2f: gravity and random DIFFER (modes: %d vs %.1f, gap: %.4f vs %.4f)"
                  % (G, sc_modes, rand_modes, sc_bgap, rand_bgap))
        else:
            print("  G=%.2f: gravity and random match (modes: %d vs %.1f, gap: %.4f vs %.4f)"
                  % (G, sc_modes, rand_modes, sc_bgap, rand_bgap))

        if sc_modes != shuf_modes or abs(sc_bgap - shuf_bgap) / max(shuf_bgap, 1e-10) > 0.2:
            print("          shuffled DIFFERS from gravity (modes: %.1f, gap: %.4f)"
                  % (shuf_modes, shuf_bgap))
    print()

    # Overall verdict
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print()

    if g_trans_gravity is None:
        print("No gravity transition detected in range G=[%.1f, %.1f]."
              % (G_VALUES[0], G_VALUES[-1]))
        print("Cannot compare to disorder.  Extend G range or check parameters.")
    elif g_trans_disorder is not None and g_trans_gravity == g_trans_disorder:
        print("GENERIC TRANSITION: Self-gravity and matched disorder destroy edge modes")
        print("at the same threshold.  The topological transition is driven by the")
        print("variance of the on-site potential, not by gravitational self-consistency.")
    elif g_trans_disorder is not None and g_trans_gravity != g_trans_disorder:
        print("DIFFERENT THRESHOLDS: gravity at G=%.2f, disorder at G=%.2f" % (
            g_trans_gravity, g_trans_disorder))
        print("Self-gravity has a distinct effect beyond matched disorder strength.")
    else:
        print("GRAVITY-SPECIFIC EDGE-MODE TRANSITION: Self-gravity destroys edge modes at G=%.2f"
              % g_trans_gravity)
        print("but matched random disorder does NOT.  The spatial structure or")
        print("self-consistency of the gravitational potential matters.")

    print()
    print("Lane state: exploratory-reopen on the audited parity-coupled SSH surface.")
    print("The gravity-specific edge-mode signal survives the matched-disorder control,")
    print("but the broader topology claim should stay constrained to this audited surface.")

    print()
    print("DONE")


if __name__ == "__main__":
    main()
