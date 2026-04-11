#!/usr/bin/env python3
"""
Legacy Topological Phase Scan for Self-Gravity
==============================================

Test whether self-gravity drives a topological phase transition in the
staggered 1D Hamiltonian (SSH analog). This is the legacy direct-on-site
scan, kept for comparison against the parity-coupled control.

Physics:
  The SSH model has two hopping amplitudes t1, t2 on alternating bonds.
  When t1 < t2 (intracell < intercell), the system is topological with
  protected zero-energy edge modes. When t1 > t2, trivial.
  Self-gravity creates an inhomogeneous on-site potential that can break
  the chiral symmetry protecting the topology.

  We start in the topological phase (t1 < t2) and ask: does turning on
  self-gravity close the gap and destroy the edge modes?

Protocol:
  1. Build 1D open-BC SSH chain (N=60 sites, 30 unit cells):
       H[2j, 2j+1]   = t1  (intracell hopping)
       H[2j+1, 2j+2] = t2  (intercell hopping)
       H[x,x] = G * Phi[x]  (self-gravity potential, NO staggering; legacy scan)
  2. Self-consistent loop: rho = |psi_filled|^2 -> Phi = -(Lap + mu2)^{-1} rho
  3. Diagnostics per G:
       a. Spectral gap: min |E_n|
       b. Edge mode count: states with |E| < threshold and edge-localized
       c. Entanglement entropy of left half (von Neumann, single-particle)
       d. Polarization (Zak phase proxy for open BC)

Hypothesis:
  Self-gravity breaks chiral symmetry, lifts the edge modes, and closes
  then reopens the gap: a candidate gravity-driven edge-mode transition on
  this legacy direct-on-site surface.

Falsification:
  If edge modes persist for all G, self-gravity does not break the
  topology. If the gap never closes, there is no transition.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.linalg import eigh

# ── Parameters ───────────────────────────────────────────────────
N = 60                  # chain length (even, for SSH unit cells)
T1 = 0.5               # intracell hopping (weak)
T2 = 1.0               # intercell hopping (strong) -> topological phase
MU2 = 0.001             # Poisson regularization
N_SC_ITER = 30          # self-consistent iterations
G_VALUES = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]

# Edge mode detection
EDGE_SITES = 6          # number of sites on each edge to check
EDGE_WEIGHT_THRESH = 0.4


# ── 1D Laplacian ────────────────────────────────────────────────

def build_1d_laplacian(n: int):
    """Tridiagonal 1D graph Laplacian with open BC."""
    L = lil_matrix((n, n), dtype=float)
    for i in range(n - 1):
        L[i, i] += 1.0
        L[i + 1, i + 1] += 1.0
        L[i, i + 1] = -1.0
        L[i + 1, i] = -1.0
    return L.tocsr()


def solve_phi(laplacian, rho: np.ndarray, mu2: float) -> np.ndarray:
    """Solve (Lap + mu2) Phi = -rho for the gravitational potential.

    Negative sign: gravity is attractive, so density creates a potential well.
    """
    n = laplacian.shape[0]
    A = (laplacian + mu2 * speye(n, format="csr")).tocsc()
    return spsolve(A, -rho).real


# ── SSH Hamiltonian ─────────────────────────────────────────────

def build_ssh_hamiltonian(n: int, t1: float, t2: float,
                          phi: np.ndarray, G: float) -> np.ndarray:
    """Build SSH Hamiltonian with gravitational on-site potential.

    H = sum_j [t1 |2j><2j+1| + t2 |2j+1><2j+2| + h.c.] + G * sum_x phi[x] |x><x|

    The on-site potential G*phi breaks chiral symmetry (which maps E -> -E).
    """
    H = np.zeros((n, n), dtype=float)

    # On-site: gravitational potential (no staggering — pure symmetry breaking)
    for x in range(n):
        H[x, x] = G * phi[x]

    # SSH hopping
    for j in range(n // 2):
        a = 2 * j       # A sublattice
        b = 2 * j + 1   # B sublattice
        # Intracell hopping
        H[a, b] = t1
        H[b, a] = t1
        # Intercell hopping (to next cell)
        if b + 1 < n:
            H[b, b + 1] = t2
            H[b + 1, b] = t2

    return H


# ── Self-consistent gravity loop ────────────────────────────────

def self_consistent_solve(n: int, t1: float, t2: float,
                          G: float, mu2: float, n_iter: int):
    """Run self-consistent loop: diagonalize -> rho -> Phi -> repeat.

    Returns the converged (eigenvalues, eigenvectors, phi).
    """
    if G == 0.0:
        phi = np.zeros(n)
        H = build_ssh_hamiltonian(n, t1, t2, phi, G)
        eigenvalues, eigenvectors = eigh(H)
        return eigenvalues, eigenvectors, phi

    laplacian = build_1d_laplacian(n)
    phi = np.zeros(n)

    for step in range(n_iter):
        H = build_ssh_hamiltonian(n, t1, t2, phi, G)
        eigenvalues, eigenvectors = eigh(H)

        # Half-filling: fill the lower N/2 states
        n_filled = n // 2
        rho = np.zeros(n)
        for i in range(n_filled):
            rho += np.abs(eigenvectors[:, i]) ** 2
        # Normalize density
        rho /= np.sum(rho)

        # Solve for gravitational potential
        phi_new = solve_phi(laplacian, rho, mu2)
        # Subtract mean to prevent runaway (gauge choice)
        phi_new -= np.mean(phi_new)

        # Damped update
        alpha = 0.3
        phi = (1.0 - alpha) * phi + alpha * phi_new

    return eigenvalues, eigenvectors, phi


# ── Observables ─────────────────────────────────────────────────

def spectral_gap(eigenvalues: np.ndarray) -> float:
    """Minimum absolute eigenvalue = spectral gap (includes edge modes)."""
    return float(np.min(np.abs(eigenvalues)))


def bulk_gap(eigenvalues: np.ndarray, eigenvectors: np.ndarray,
             n: int) -> float:
    """Bulk gap: smallest |E| excluding edge-localized modes.

    A mode is edge-localized if > 40% of its weight sits on the
    outermost EDGE_SITES on each end.
    """
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


def edge_mode_energy(eigenvalues: np.ndarray, eigenvectors: np.ndarray,
                     n: int) -> float:
    """Energy of the most edge-localized near-zero mode. Returns inf if none."""
    edge_left = list(range(EDGE_SITES))
    edge_right = list(range(n - EDGE_SITES, n))
    edge_sites = edge_left + edge_right

    best_E = float("inf")
    for i, E in enumerate(eigenvalues):
        psi = eigenvectors[:, i]
        w_total = np.sum(np.abs(psi) ** 2)
        if w_total == 0:
            continue
        w_edge = np.sum(np.abs(psi[edge_sites]) ** 2)
        if w_edge / w_total > EDGE_WEIGHT_THRESH:
            if abs(E) < abs(best_E):
                best_E = E
    return float(best_E)


def count_edge_modes(eigenvalues: np.ndarray, eigenvectors: np.ndarray,
                     n: int, gap_thresh: float) -> int:
    """Count states with |E| < threshold AND weight concentrated on edges."""
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


def entanglement_entropy_half(eigenvectors: np.ndarray, n: int) -> float:
    """Von Neumann entanglement entropy of the left half at half-filling.

    Single-particle correlation matrix method:
    C_ij = sum_{filled} psi_i* psi_j restricted to left subsystem.
    S = -Tr[C ln C + (1-C) ln(1-C)].
    """
    n_filled = n // 2
    n_left = n // 2

    C = np.zeros((n_left, n_left), dtype=complex)
    for k in range(n_filled):
        psi_left = eigenvectors[:n_left, k]
        C += np.outer(psi_left, np.conj(psi_left))

    nu = np.linalg.eigvalsh(C).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)
    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))
    return float(S)


def sublattice_polarization(eigenvectors: np.ndarray, n: int) -> float:
    """Sublattice polarization: weight on A vs B sublattice for near-zero modes.

    P = sum_{filled} (|psi_A|^2 - |psi_B|^2) / sum_{filled} (|psi_A|^2 + |psi_B|^2)
    This measures how much the filled states break sublattice symmetry.
    """
    n_filled = n // 2
    A_sites = np.arange(0, n, 2)
    B_sites = np.arange(1, n, 2)

    w_A = 0.0
    w_B = 0.0
    for k in range(n_filled):
        psi = eigenvectors[:, k]
        w_A += np.sum(np.abs(psi[A_sites]) ** 2)
        w_B += np.sum(np.abs(psi[B_sites]) ** 2)

    total = w_A + w_B
    if total == 0:
        return 0.0
    return float((w_A - w_B) / total)


# ── Main ────────────────────────────────────────────────────────

def main():
    print("=" * 76)
    print("TOPOLOGICAL PHASE TRANSITION DRIVEN BY SELF-GRAVITY")
    print("SSH model: t1=%.2f, t2=%.2f (topological), N=%d, open BC" % (T1, T2, N))
    print("=" * 76)
    print()

    # Reference: free system
    evals0, evecs0, _ = self_consistent_solve(N, T1, T2, 0.0, MU2, 1)
    free_gap = spectral_gap(evals0)
    free_edge = count_edge_modes(evals0, evecs0, N, 0.1 * (T2 - T1))
    free_S = entanglement_entropy_half(evecs0, N)

    print("Free system (G=0):")
    print("  Spectral gap     = %.6f" % free_gap)
    print("  Edge modes       = %d" % free_edge)
    print("  Entanglement S   = %.4f" % free_S)
    print("  t2 - t1          = %.2f (topological if > 0)" % (T2 - T1))

    # Compute the free bulk gap (excluding edge modes)
    free_bulk_gap = bulk_gap(evals0, evecs0, N)
    print("  Bulk gap         = %.6f" % free_bulk_gap)

    # Adaptive gap threshold
    gap_thresh = max(0.05, 0.15 * free_bulk_gap)
    print("  Edge mode |E| threshold = %.4f" % gap_thresh)
    print()

    # Scan
    results = []
    print("%-8s  %-10s  %-10s  %-10s  %-10s  %-10s  %-10s  %-10s" % (
        "G", "Gap", "BulkGap", "EdgeE", "Modes", "S_ent", "Polariz", "phi_rng"))
    print("-" * 86)

    for G in G_VALUES:
        eigenvalues, eigenvectors, phi = self_consistent_solve(
            N, T1, T2, G, MU2, N_SC_ITER
        )

        gap = spectral_gap(eigenvalues)
        bgap = bulk_gap(eigenvalues, eigenvectors, N)
        emode_E = edge_mode_energy(eigenvalues, eigenvectors, N)
        n_edge = count_edge_modes(eigenvalues, eigenvectors, N, gap_thresh)
        S_ent = entanglement_entropy_half(eigenvectors, N)
        pol = sublattice_polarization(eigenvectors, N)
        phi_range = float(np.max(phi) - np.min(phi)) if G > 0 else 0.0

        results.append({
            "G": G, "gap": gap, "bulk_gap": bgap, "edge_E": emode_E,
            "edge_modes": n_edge, "S_ent": S_ent, "polarization": pol,
            "phi_range": phi_range,
        })

        emode_str = "%.4f" % emode_E if emode_E < 1e10 else "---"
        print("%-8.2f  %-10.4f  %-10.4f  %-10s  %-10d  %-10.4f  %-10.6f  %-10.4f" % (
            G, gap, bgap, emode_str, n_edge, S_ent, pol, phi_range))

    print()

    # ── Near-zero spectrum detail ───────────────────────────────
    print("NEAR-ZERO SPECTRUM (closest 8 eigenvalues to E=0)")
    print("-" * 76)
    for G in [0.0, 2.0, 10.0, 50.0, 100.0]:
        eigenvalues, eigenvectors, phi = self_consistent_solve(
            N, T1, T2, G, MU2, N_SC_ITER
        )
        sorted_by_abs = sorted(eigenvalues, key=abs)
        print("  G=%6.1f: " % G, end="")
        print("  ".join(["%+.5f" % e for e in sorted_by_abs[:8]]))
    print()

    # ── Edge mode wavefunctions ─────────────────────────────────
    print("EDGE MODE PROFILE (|psi|^2 on first/last 8 sites)")
    print("-" * 76)
    for G in [0.0, 5.0, 50.0]:
        eigenvalues, eigenvectors, phi = self_consistent_solve(
            N, T1, T2, G, MU2, N_SC_ITER
        )
        # Find the mode closest to E=0
        idx_min = int(np.argmin(np.abs(eigenvalues)))
        psi = eigenvectors[:, idx_min]
        prob = np.abs(psi) ** 2
        print("  G=%6.1f (E=%.5f):" % (G, eigenvalues[idx_min]))
        print("    Left  8: " + "  ".join(["%.4f" % prob[i] for i in range(8)]))
        print("    Right 8: " + "  ".join(["%.4f" % prob[i] for i in range(N - 8, N)]))
    print()

    # ── Analysis ────────────────────────────────────────────────
    print("=" * 76)
    print("ANALYSIS")
    print("=" * 76)
    print()

    # 1. Bulk gap evolution
    print("1. BULK GAP vs G")
    bgaps = [(r["G"], r["bulk_gap"]) for r in results]
    min_bgap_entry = min(bgaps, key=lambda x: x[1])
    print("   Free bulk gap  = %.6f" % free_bulk_gap)
    print("   Minimum bulk gap = %.6f at G = %.2f" % (min_bgap_entry[1], min_bgap_entry[0]))
    gap_ratio = min_bgap_entry[1] / free_bulk_gap if free_bulk_gap > 0 else float("inf")
    print("   Bulk gap ratio (min/free) = %.4f" % gap_ratio)

    gap_closes = gap_ratio < 0.1
    gap_reduces = gap_ratio < 0.5
    if gap_closes:
        print("   -> BULK GAP CLOSES: topological transition signal")
    elif gap_reduces:
        print("   -> Bulk gap significantly reduced; partial transition")
    else:
        print("   -> Bulk gap robust")

    # Edge mode energy evolution
    print()
    print("   Edge mode energy evolution:")
    for r in results:
        if r["edge_E"] < 1e10:
            print("   G=%6.2f: E_edge = %.6f" % (r["G"], r["edge_E"]))
        else:
            print("   G=%6.2f: no edge mode" % r["G"])
    print()

    # 2. Edge modes
    print("2. EDGE MODES vs G")
    transition_G = None
    prev_modes = results[0]["edge_modes"]
    for r in results[1:]:
        if prev_modes > 0 and r["edge_modes"] == 0:
            transition_G = r["G"]
            break
        prev_modes = r["edge_modes"]

    if transition_G is not None:
        print("   Edge modes vanish at G ~ %.2f -> TOPOLOGICAL TRANSITION" % transition_G)
    elif results[0]["edge_modes"] == 0:
        print("   No edge modes even at G=0 (system may be in trivial phase or threshold too tight)")
    else:
        print("   Edge modes persist for all G -> topology protected")
    print()

    # 3. Entanglement entropy
    print("3. ENTANGLEMENT ENTROPY")
    S_vals = [r["S_ent"] for r in results]
    S_max_idx = int(np.argmax(S_vals))
    print("   Peak S = %.4f at G = %.2f" % (S_vals[S_max_idx], results[S_max_idx]["G"]))
    entropy_peak = 0 < S_max_idx < len(results) - 1
    if entropy_peak:
        print("   -> Interior peak: critical point signature")
    else:
        print("   -> Monotonic or boundary peak")
    print()

    # 4. Sublattice polarization
    print("4. SUBLATTICE POLARIZATION (chiral symmetry breaking)")
    for r in results:
        broken = "BROKEN" if abs(r["polarization"]) > 0.01 else "intact"
        print("   G=%6.2f: P = %+.6f (%s)" % (r["G"], r["polarization"], broken))
    print()

    # ── Verdict ─────────────────────────────────────────────────
    print("=" * 76)
    print("VERDICT")
    print("=" * 76)

    modes_change = transition_G is not None
    chiral_broken = any(abs(r["polarization"]) > 0.01 for r in results if r["G"] > 0)

    evidence_for = []
    evidence_against = []

    if gap_closes:
        evidence_for.append("gap closes (ratio %.4f)" % gap_ratio)
    elif gap_reduces:
        evidence_for.append("gap reduces (ratio %.4f)" % gap_ratio)
    else:
        evidence_against.append("gap robust (ratio %.4f)" % gap_ratio)

    if modes_change:
        evidence_for.append("edge modes vanish at G~%.1f" % transition_G)
    else:
        evidence_against.append("edge modes unchanged")

    if entropy_peak:
        evidence_for.append("entanglement peak at G=%.1f" % results[S_max_idx]["G"])

    if chiral_broken:
        evidence_for.append("chiral symmetry broken by self-gravity")
    else:
        evidence_against.append("chiral symmetry intact")

    print()
    if evidence_for:
        print("Evidence FOR topological transition:")
        for e in evidence_for:
            print("  + %s" % e)
    if evidence_against:
        print("Evidence AGAINST topological transition:")
        for e in evidence_against:
            print("  - %s" % e)
    print()

    n_for = len(evidence_for)
    if n_for >= 3:
        print("CANDIDATE TRANSITION: self-gravity drives a topological edge-mode change")
        print("Compare against frontier_topological_control.py before promotion.")
    elif n_for >= 2:
        print("EXPLORATORY: self-gravity partially disrupts topology")
    elif n_for >= 1:
        print("WEAK EVIDENCE: some signatures but inconclusive")
    else:
        print("NO EVIDENCE: self-gravity does not affect the topological phase")

    print()
    print("DONE")


if __name__ == "__main__":
    main()
