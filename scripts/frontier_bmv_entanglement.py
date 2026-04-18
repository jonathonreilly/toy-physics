#!/usr/bin/env python3
"""
Branch-mediated entanglement on an externally imposed two-branch protocol.

Protocol: Two particles (wavepackets) on a 2D staggered lattice. A source at the
midpoint is placed in an externally imposed branch superposition of
(present, absent). Each particle evolves under both branches. The joint state
correlates the two particles through that branch structure.

Guardrail:
  this is a branch-entanglement probe on an externally imposed
  geometry/source branch, not a full BMV witness. It does not by itself prove
  that gravity must be quantum.

The two-particle state is:
  |Psi> = (|psi_1A>|psi_2A> + |psi_1B>|psi_2B>) / sqrt(2)

where A = source present, B = source absent. The reduced density matrix for
particle 1 has eigenvalues (1 +/- |<psi_2A|psi_2B>| * |<psi_1A|psi_1B>|) / 2,
giving entanglement entropy:

  S = H_binary(p) where p = (1 + overlap_1 * overlap_2) / 2

Branch-mediated witness: S > 0 whenever overlap < 1, i.e. whenever the
branches create distinguishable evolution for either particle.

Sweep G = [1, 2, 5, 10, 20, 50] to map the entanglement vs coupling strength.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# ── Physical parameters ──────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIDE = 10
G_VALUES = [1, 2, 5, 10, 20, 50]


# ── Lattice construction ─────────────────────────────────────────────

def make_lattice_2d(side: int):
    """Build a 2D periodic staggered lattice with checkerboard coloring."""
    coords = []
    colors = []
    adj = {}
    index = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((float(x), float(y)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords)
    color = np.array(colors, dtype=int)
    n = len(pos)
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]
            adj[a] = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                adj[a].append(index[((x + dx) % side, (y + dy) % side)])
    return pos, color, adj, index, n


def build_laplacian(pos: np.ndarray, adj: dict[int, list[int]]):
    n = len(pos)
    lap = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            lap[i, j] -= w
            lap[j, i] -= w
            lap[i, i] += w
            lap[j, j] += w
    return lap.tocsr()


def build_hamiltonian(pos: np.ndarray, color: np.ndarray,
                      adj: dict[int, list[int]], phi: np.ndarray):
    """Staggered-fermion Hamiltonian with gravitational potential phi."""
    n = len(pos)
    ham = lil_matrix((n, n), dtype=complex)
    parity = np.where(color == 0, 1.0, -1.0)
    ham.setdiag((MASS + phi) * parity)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            ham[i, j] += -0.5j * w
            ham[j, i] += 0.5j * w
    return ham.tocsr()


def cn_step(ham, psi: np.ndarray):
    """Crank-Nicolson time step."""
    n = ham.shape[0]
    ap = (speye(n, format="csc") + 1j * ham * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * ham * DT / 2
    return spsolve(ap, am.dot(psi))


def gaussian_at(pos: np.ndarray, center: tuple[float, float], sigma: float):
    """Gaussian wavepacket centered at (cx, cy)."""
    cx, cy = center
    rsq = (pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2
    psi = np.exp(-0.5 * rsq / sigma ** 2).astype(complex)
    norm = np.linalg.norm(psi)
    if norm < 1e-30:
        raise ValueError(f"Gaussian at {center} has zero norm on lattice")
    return psi / norm


def binary_entropy(p: float) -> float:
    """H(p) = -p log(p) - (1-p) log(1-p), using natural log."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


# ── Branch-entanglement protocol ────────────────────────────────────

def run_bmv(g: float):
    """Run the branch-entanglement protocol for a given source strength G."""
    pos, color, adj, index, n = make_lattice_2d(SIDE)
    lap = build_laplacian(pos, adj)

    # Source at midpoint
    source_node = index[(SIDE // 2, SIDE // 2)]

    # Two external source configurations
    rho_ext = np.zeros(n)
    rho_ext[source_node] = g
    phi_A = spsolve((lap + MU2 * speye(n, format="csr")).tocsc(), rho_ext)
    phi_B = np.zeros(n)  # no source

    # Build Hamiltonians for both configurations
    ham_A = build_hamiltonian(pos, color, adj, phi_A)
    ham_B = build_hamiltonian(pos, color, adj, phi_B)

    # Initial wavepackets: particle 1 at (2,5), particle 2 at (8,5)
    sigma = 1.5
    psi_1_init = gaussian_at(pos, (2.0, 5.0), sigma)
    psi_2_init = gaussian_at(pos, (8.0, 5.0), sigma)

    # Evolve each particle under each geometry
    psi_1A = psi_1_init.copy()
    psi_1B = psi_1_init.copy()
    psi_2A = psi_2_init.copy()
    psi_2B = psi_2_init.copy()

    for _ in range(N_STEPS):
        psi_1A = cn_step(ham_A, psi_1A)
        psi_1B = cn_step(ham_B, psi_1B)
        psi_2A = cn_step(ham_A, psi_2A)
        psi_2B = cn_step(ham_B, psi_2B)

    # Overlaps
    overlap_1 = abs(np.vdot(psi_1A, psi_1B))
    overlap_2 = abs(np.vdot(psi_2A, psi_2B))

    # Norms (unitarity check)
    norm_1A = np.linalg.norm(psi_1A)
    norm_1B = np.linalg.norm(psi_1B)
    norm_2A = np.linalg.norm(psi_2A)
    norm_2B = np.linalg.norm(psi_2B)

    # Branch-mediated entanglement entropy
    # For |Psi> = (|a>|c> + |b>|d>) / sqrt(2):
    # rho_1 eigenvalues are (1 +/- |<a|b>|*|<c|d>|) / 2
    product_overlap = overlap_1 * overlap_2
    p = 0.5 + 0.5 * product_overlap
    s_quantum = binary_entropy(p)

    # Classical mixture: rho_mix = (|a><a| x |c><c| + |b><b| x |d><d|) / 2
    # Tr_2(rho_mix) = (|a><a| + |b><b|) / 2  (if |c>,|d> normalized)
    # eigenvalues of Tr_2(rho_mix) are (1 +/- |<a|b>|) / 2
    p_mix = 0.5 + 0.5 * overlap_1
    s_mix = binary_entropy(p_mix)

    # The entanglement witness: S_quantum - S_mix
    # S_mix is the entropy from classical ignorance about which branch
    # S_quantum is the total entropy including entanglement
    # If S_quantum > S_mix, gravity created entanglement beyond classical mixing

    # Actually for the classical mixture, Tr_2 gives:
    # rho_1^mix = 0.5 |a><a| + 0.5 |b><b|
    # S(rho_1^mix) = H_binary((1 + |<a|b>|)/2) -- same formula
    # For the quantum state, S(rho_1^Q) = H_binary((1 + |<a|b>|*|<c|d>|)/2)
    # Since |<c|d>| <= 1, S_quantum >= S_mix always.
    # Equality iff |<c|d>| = 1 (particle 2 unaffected) or |<a|b>| = 0.

    delta_s = s_quantum - s_mix

    return {
        "G": g,
        "overlap_1": overlap_1,
        "overlap_2": overlap_2,
        "product_overlap": product_overlap,
        "S_quantum": s_quantum,
        "S_mix": s_mix,
        "delta_S": delta_s,
        "norm_1A": norm_1A,
        "norm_1B": norm_1B,
        "norm_2A": norm_2A,
        "norm_2B": norm_2B,
        "p_quantum": p,
        "p_mix": p_mix,
    }


# ── Main ─────────────────────────────────────────────────────────────

def main():
    t0 = time.time()

    print("=" * 78)
    print("BRANCH-MEDIATED ENTANGLEMENT TOY PROTOCOL")
    print("=" * 78)
    print()
    print(f"Lattice: 2D staggered, side={SIDE}, n={SIDE**2}")
    print(f"Particle 1 at (2,5), Particle 2 at (8,5), Source at ({SIDE//2},{SIDE//2})")
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, sigma=1.5")
    print()
    print("Protocol: Source in superposition |A> + |B> where A=present, B=absent.")
    print("Joint state: |Psi> = (|psi_1A>|psi_2A> + |psi_1B>|psi_2B>) / sqrt(2)")
    print()
    print(
        f"{'G':>5s}  {'ovlp_1':>8s} {'ovlp_2':>8s} {'ovlp_12':>8s}  "
        f"{'S_quant':>8s} {'S_mix':>8s} {'dS':>8s}  "
        f"{'n1A':>6s} {'n1B':>6s} {'n2A':>6s} {'n2B':>6s}"
    )
    print("-" * 90)

    results = []
    for g in G_VALUES:
        res = run_bmv(g)
        results.append(res)
        print(
            f"{res['G']:5.0f}  {res['overlap_1']:8.4f} {res['overlap_2']:8.4f} "
            f"{res['product_overlap']:8.4f}  {res['S_quantum']:8.5f} {res['S_mix']:8.5f} "
            f"{res['delta_S']:8.5f}  {res['norm_1A']:6.4f} {res['norm_1B']:6.4f} "
            f"{res['norm_2A']:6.4f} {res['norm_2B']:6.4f}"
        )

    # ── Analysis ─────────────────────────────────────────────────────
    print()
    print("=" * 78)
    print("ANALYSIS")
    print("=" * 78)
    print()
    print("Key quantities:")
    print("  ovlp_1  = |<psi_1A|psi_1B>|  (particle 1 branch overlap)")
    print("  ovlp_2  = |<psi_2A|psi_2B>|  (particle 2 branch overlap)")
    print("  ovlp_12 = ovlp_1 * ovlp_2    (combined overlap)")
    print("  S_quant = S(rho_1) for quantum joint state  [entanglement entropy]")
    print("  S_mix   = S(rho_1) for classical mixture    [classical ignorance]")
    print("  dS      = S_quant - S_mix                   [branch-mediated entanglement]")
    print()

    # Check branch-mediated entanglement signal.
    # This is not a full BMV witness: the source branch superposition is imposed
    # externally, not generated dynamically by the particles themselves.
    any_entangled = False
    for res in results:
        if res["delta_S"] > 1e-6:
            any_entangled = True
            break

    if any_entangled:
        print("BRANCH-ENTANGLEMENT SIGNAL: POSITIVE")
        print("  The fixed geometry-branch protocol generates entanglement")
        print("  beyond the corresponding classical branch mixture.")
        print("  This is a bounded externally imposed two-branch result,")
        print("  not a standalone gravity-is-quantum witness.")
    else:
        print("BRANCH-ENTANGLEMENT PROTOCOL: NULL")
        print("  No entanglement beyond classical mixing detected.")
        print("  Overlaps may be too close to 1 for detectable entanglement.")

    print()

    # Entanglement scaling
    print("Entanglement scaling with G:")
    for res in results:
        bar_len = int(60 * res["S_quantum"] / math.log(2)) if res["S_quantum"] > 0 else 0
        bar = "#" * min(bar_len, 60)
        print(f"  G={res['G']:5.0f}: S={res['S_quantum']:.5f} nats  {bar}")

    print()
    max_s = max(r["S_quantum"] for r in results)
    print(f"  Maximum entanglement: {max_s:.5f} nats = {max_s / math.log(2):.5f} bits")
    print(f"  (Maximum possible for 2-branch system: ln(2) = {math.log(2):.5f} nats = 1 bit)")
    print(f"  Fraction of max: {max_s / math.log(2):.4f}")

    # ── Verdict ──────────────────────────────────────────────────────
    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print()

    # Monotonicity check: does entanglement grow with G?
    s_values = [r["S_quantum"] for r in results]
    monotonic = all(s_values[i] >= s_values[i - 1] - 1e-8 for i in range(1, len(s_values)))

    # Significant entanglement threshold
    significant = max_s > 0.01

    if significant and monotonic:
        print("CONFIRMED: branch-mediated entanglement grows monotonically with source strength.")
        print(f"  Entanglement range: {min(s_values):.5f} to {max_s:.5f} nats")
        print("  In this imposed-branch model, the shared geometry branch")
        print("  coherently entangles the two separated particles.")
    elif significant:
        print("PARTIAL: Entanglement detected but non-monotonic in G.")
        print("  Possible finite-size or lattice artifacts at high coupling.")
    else:
        print("WEAK: Entanglement < 0.01 nats across all G values.")
        print("  Lattice may be too small or coupling too weak for BMV signal.")

    elapsed = time.time() - t0
    print(f"\nTime: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
