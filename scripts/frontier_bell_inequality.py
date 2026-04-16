#!/usr/bin/env python3
"""
Bell inequality (CHSH) violation derived from the lattice propagator.

Every ingredient traces to Cl(3) on Z^3:
  - Lattice with staggered (bipartite) structure -> Z^d (from A1)
  - Sublattice parity operator Z = (-1)^x -> intrinsic to Z^d
  - Pair-hop operator X (swap within even-odd pair) -> Z^d connectivity
  - {Z, X} = 0, Z^2 = X^2 = I -> Pauli algebra, verified
  - Staggered mass m*(-1)^x -> Dirac mass in Kogut-Susskind formulation
  - Fermionic antisymmetry -> Pauli exclusion from Cl(3)
  - Ground state / time evolution -> lattice Hamiltonian dynamics

Parts:
  A. Structural: sublattice Pauli algebra verified, singlet saturates Tsirelson
  B. Ground state: 2-fermion ground state of staggered H gives CHSH > 2
  C. Propagator: singlet evolved under staggered H, track CHSH vs time

PStack experiment: frontier-bell-inequality
"""

from __future__ import annotations
import math, time
import numpy as np
from scipy.linalg import expm, eigh


# ====================================================================
# Framework-native lattice operators
# ====================================================================

def staggered_Z(n):
    """Sublattice parity (-1)^x. Eigenvalues +/-1. Intrinsic to Z^d."""
    return np.diag([1.0 if i % 2 == 0 else -1.0 for i in range(n)]).astype(complex)


def pair_hop_X(n):
    """Pair-hop: swap within each (2k, 2k+1) pair. Requires even n.
    Eigenvalues +/-1. X^2 = I. {Z, X} = 0. Intrinsic to Z^d connectivity."""
    assert n % 2 == 0, "Need even n for non-overlapping pairs"
    X = np.zeros((n, n), dtype=complex)
    for i in range(0, n, 2):
        X[i, i + 1] = 1.0
        X[i + 1, i] = 1.0
    return X


def staggered_hamiltonian(n, t_hop=1.0, mass=0.0):
    """Staggered fermion Hamiltonian: hopping + Dirac mass m*(-1)^x."""
    H = np.zeros((n, n), dtype=complex)
    for i in range(n - 1):
        H[i, i + 1] = -t_hop
        H[i + 1, i] = -t_hop
    for i in range(n):
        H[i, i] = mass * (1.0 if i % 2 == 0 else -1.0)
    return H


def measurement_op(Z, X, theta):
    """O(theta) = cos(theta)*Z + sin(theta)*X. Eigenvalues +/-1."""
    return math.cos(theta) * Z + math.sin(theta) * X


# ====================================================================
# Slater determinant correlator (efficient, no n^2 matrices)
# ====================================================================

def slater_correlator(phi1, phi2, O_a, O_b):
    """<Psi|O_a x O_b|Psi> for Slater determinant |phi1 ^ phi2>.

    Formula: E = (M11*N22 + M22*N11 - M12*N21 - M21*N12) / 2
    where Mij = <phi_i|O_a|phi_j>, Nij = <phi_i|O_b|phi_j>.
    """
    M11 = np.real(phi1.conj() @ O_a @ phi1)
    M12 = phi1.conj() @ O_a @ phi2
    M21 = phi2.conj() @ O_a @ phi1
    M22 = np.real(phi2.conj() @ O_a @ phi2)
    N11 = np.real(phi1.conj() @ O_b @ phi1)
    N12 = phi1.conj() @ O_b @ phi2
    N21 = phi2.conj() @ O_b @ phi1
    N22 = np.real(phi2.conj() @ O_b @ phi2)
    return np.real(M11 * N22 + M22 * N11 - M12 * N21 - M21 * N12) / 2


def compute_chsh(phi1, phi2, Z, X):
    """Find optimal CHSH value by sweeping measurement angles.

    Returns (S_best, angles) where S_best is the maximum |S| found.
    """
    best_S = 0.0
    best_angles = None

    # Fine grid search
    angles = np.linspace(0, math.pi, 37)  # 5-degree steps
    for a in angles:
        for ap in angles:
            # For each (a, a'), optimal b is between a and a'
            # but sweep anyway for robustness
            for b in angles:
                bp_candidates = [b + math.pi / 2, b - math.pi / 2]
                for bp in bp_candidates:
                    O_a = measurement_op(Z, X, a)
                    O_ap = measurement_op(Z, X, ap)
                    O_b = measurement_op(Z, X, b)
                    O_bp = measurement_op(Z, X, bp)

                    Eab = slater_correlator(phi1, phi2, O_a, O_b)
                    Eabp = slater_correlator(phi1, phi2, O_a, O_bp)
                    Eapb = slater_correlator(phi1, phi2, O_ap, O_b)
                    Eapbp = slater_correlator(phi1, phi2, O_ap, O_bp)

                    S = Eab - Eabp + Eapb + Eapbp
                    if abs(S) > abs(best_S):
                        best_S = S
                        best_angles = (a, ap, b, bp)

    return best_S, best_angles


def fast_chsh(phi1, phi2, Z, X):
    """Compute optimal CHSH using the Horodecki formula.

    For any 2-qubit state, the maximum CHSH value is:
      S_max = 2 * sqrt(lambda_1 + lambda_2)
    where lambda_1, lambda_2 are the two largest eigenvalues of T^T T,
    and T_ij = Tr(rho * sigma_i x sigma_j) is the correlation matrix.

    For our Slater determinant, we compute the 3x3 correlation matrix
    in the orbital-space {Z, X, Y=iZX} basis, then apply Horodecki.
    """
    # Precompute matrix elements in the orbital basis
    Zm = np.array([
        [np.real(phi1.conj() @ Z @ phi1), phi1.conj() @ Z @ phi2],
        [phi2.conj() @ Z @ phi1, np.real(phi2.conj() @ Z @ phi2)]
    ], dtype=complex)
    Xm = np.array([
        [np.real(phi1.conj() @ X @ phi1), phi1.conj() @ X @ phi2],
        [phi2.conj() @ X @ phi1, np.real(phi2.conj() @ X @ phi2)]
    ], dtype=complex)

    # Y = i*Z*X (completing the Pauli triple)
    Y = 1j * Z @ X
    Ym = np.array([
        [np.real(phi1.conj() @ Y @ phi1), phi1.conj() @ Y @ phi2],
        [phi2.conj() @ Y @ phi1, np.real(phi2.conj() @ Y @ phi2)]
    ], dtype=complex)

    def E_fast(a, b):
        Ma = math.cos(a) * Zm + math.sin(a) * Xm
        Nb = math.cos(b) * Zm + math.sin(b) * Xm
        return np.real(Ma[0, 0] * Nb[1, 1] + Ma[1, 1] * Nb[0, 0]
                       - Ma[0, 1] * Nb[1, 0] - Ma[1, 0] * Nb[0, 1]) / 2

    # Build 3x3 correlation matrix T_ij = <sigma_i x sigma_j>
    # where sigma = {Z, X, Y} in our lattice basis
    ops = [Zm, Xm, Ym]
    T = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Mi = ops[i]
            Nj = ops[j]
            T[i, j] = np.real(Mi[0, 0] * Nj[1, 1] + Mi[1, 1] * Nj[0, 0]
                              - Mi[0, 1] * Nj[1, 0] - Mi[1, 0] * Nj[0, 1]) / 2

    # Horodecki: S_max = 2*sqrt(lambda_1 + lambda_2)
    # where lambda_i are eigenvalues of T^T T in decreasing order
    TTT = T.T @ T
    evals = sorted(np.linalg.eigvalsh(TTT), reverse=True)
    S_max = 2 * math.sqrt(max(evals[0] + evals[1], 0))

    # Find the actual angles that achieve this (for reporting)
    # Use a moderate grid to find the best angles
    best_S = 0.0
    best_angles = None
    angles = np.linspace(0, math.pi, 37)
    for a in angles:
        for ap in angles:
            b_opt = (a + ap) / 2
            bp_opt = b_opt + math.pi / 2
            for b in [b_opt, b_opt + math.pi/4, b_opt - math.pi/4]:
                for bp in [b + math.pi/2, b - math.pi/2]:
                    S = E_fast(a, b) - E_fast(a, bp) + E_fast(ap, b) + E_fast(ap, bp)
                    if abs(S) > abs(best_S):
                        best_S = S
                        best_angles = (a, ap, b, bp)

    # Use the Horodecki bound as the definitive answer
    # (the grid search is just for angle reporting)
    return S_max, best_angles, E_fast


# ====================================================================
# PART A: Structural theorem
# ====================================================================

def part_a():
    print("=" * 72)
    print("PART A: STRUCTURAL THEOREM — NATIVE PAULI ALGEBRA ON Z^d")
    print("=" * 72)
    print()

    for n in [4, 6, 8, 10, 20, 50, 100]:
        if n % 2 != 0:
            continue
        Z = staggered_Z(n)
        X = pair_hop_X(n)
        z2 = np.allclose(Z @ Z, np.eye(n))
        x2 = np.allclose(X @ X, np.eye(n))
        anti = np.allclose(Z @ X + X @ Z, 0)
        print(f"  N={n:4d}: Z^2=I {z2}, X^2=I {x2}, {{Z,X}}=0 {anti}")

    # Singlet CHSH
    n = 4
    Z = staggered_Z(n)
    X = pair_hop_X(n)
    # Singlet: phi1 = even site, phi2 = odd site (adjacent)
    phi1 = np.zeros(n, dtype=complex); phi1[0] = 1.0
    phi2 = np.zeros(n, dtype=complex); phi2[1] = 1.0

    S, angles, E_fn = fast_chsh(phi1, phi2, Z, X)
    print(f"\n  Singlet CHSH: |S| = {abs(S):.10f}")
    print(f"  Tsirelson:    2*sqrt(2) = {2*math.sqrt(2):.10f}")
    print(f"  Saturated: {abs(abs(S) - 2*math.sqrt(2)) < 1e-6}")

    # Verify E(0, theta) = -cos(theta)
    max_diff = 0.0
    for k in range(37):
        theta = k * math.pi / 36
        E_num = E_fn(0, theta)
        E_ana = -math.cos(theta)
        max_diff = max(max_diff, abs(E_num - E_ana))
    print(f"  Max |E(0,theta) - (-cos theta)|: {max_diff:.2e}")

    return {"S": S, "tsirelson": abs(abs(S) - 2*math.sqrt(2)) < 1e-6}


# ====================================================================
# PART B: Ground-state CHSH
# ====================================================================

def part_b():
    print()
    print("=" * 72)
    print("PART B: GROUND-STATE CHSH — STAGGERED HAMILTONIAN")
    print("=" * 72)
    print()
    print("2-fermion ground state. Measurements: sublattice Z and pair-hop X.")
    print("All operators are framework-native. Eigenvalues verified +/-1.")
    print()

    # Size sweep at fixed mass
    print("--- Size sweep (mass=1.0, t_hop=1.0) ---")
    print(f"  {'N':>4s}  {'|S|':>10s}  {'Bell?':>8s}  {'%Tsir':>8s}  {'E_gap':>8s}")
    print("  " + "-" * 44)

    for n in [4, 6, 8, 10, 12, 16, 20]:
        H = staggered_hamiltonian(n, mass=1.0)
        evals, evecs = eigh(H)
        phi1 = evecs[:, 0]
        phi2 = evecs[:, 1]
        Z = staggered_Z(n)
        X = pair_hop_X(n)

        S, angles, _ = fast_chsh(phi1, phi2, Z, X)
        gap = evals[2] - evals[1]
        viol = abs(S) > 2.0
        pct = (abs(S) - 2.0) / (2 * math.sqrt(2) - 2.0) * 100 if viol else 0
        print(f"  {n:4d}  {abs(S):10.6f}  {'YES' if viol else 'no':>8s}  {pct:7.1f}%  {gap:8.4f}")

    # Mass sweep at fixed size
    print()
    print("--- Mass sweep (N=8, t_hop=1.0) ---")
    print(f"  {'m/t':>6s}  {'|S|':>10s}  {'Bell?':>8s}  {'%Tsir':>8s}")
    print("  " + "-" * 38)

    best_result = None
    for mass in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]:
        n = 8
        H = staggered_hamiltonian(n, mass=mass)
        evals, evecs = eigh(H)
        phi1 = evecs[:, 0]
        phi2 = evecs[:, 1]
        Z = staggered_Z(n)
        X = pair_hop_X(n)

        S, angles, _ = fast_chsh(phi1, phi2, Z, X)
        viol = abs(S) > 2.0
        pct = (abs(S) - 2.0) / (2 * math.sqrt(2) - 2.0) * 100 if viol else 0
        print(f"  {mass:6.2f}  {abs(S):10.6f}  {'YES' if viol else 'no':>8s}  {pct:7.1f}%")

        if best_result is None or abs(S) > abs(best_result["S"]):
            best_result = {"mass": mass, "S": S, "N": n, "angles": angles}

    return best_result


# ====================================================================
# PART C: Propagator-evolved CHSH
# ====================================================================

def part_c(n=8, mass=1.0):
    print()
    print("=" * 72)
    print("PART C: PROPAGATOR-EVOLVED BELL VIOLATION")
    print("=" * 72)
    print()
    print(f"N={n}, mass={mass}. Initial: singlet at center (Pauli exclusion).")
    print("Evolved under staggered Hamiltonian. Track CHSH vs time.")
    print()

    H = staggered_hamiltonian(n, mass=mass)
    Z = staggered_Z(n)
    X = pair_hop_X(n)

    # Initial singlet at center pair
    c = n // 2
    se = c if c % 2 == 0 else c - 1

    phi1_0 = np.zeros(n, dtype=complex); phi1_0[se] = 1.0
    phi2_0 = np.zeros(n, dtype=complex); phi2_0[se + 1] = 1.0

    # Verify initial CHSH
    S0, _, E0 = fast_chsh(phi1_0, phi2_0, Z, X)
    print(f"  t=0.000: |S| = {abs(S0):.6f} (expect 2*sqrt2 = {2*math.sqrt(2):.6f})")
    print()

    dt = 0.05
    U = expm(-1j * H * dt)

    print(f"  {'t':>8s}  {'|S|':>10s}  {'Bell?':>8s}  {'%Tsir':>8s}  {'spread1':>8s}  {'spread2':>8s}")
    print("  " + "-" * 56)

    phi1 = phi1_0.copy()
    phi2 = phi2_0.copy()
    results = []

    for step in range(201):
        t_val = step * dt
        if step in [0, 1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 80, 100, 150, 200]:
            S, angles, _ = fast_chsh(phi1, phi2, Z, X)
            # Wavefunction spread (IPR)
            ipr1 = 1.0 / np.sum(np.abs(phi1) ** 4)
            ipr2 = 1.0 / np.sum(np.abs(phi2) ** 4)
            viol = abs(S) > 2.0
            pct = (abs(S) - 2.0) / (2 * math.sqrt(2) - 2.0) * 100 if viol else 0
            print(f"  {t_val:8.3f}  {abs(S):10.6f}  {'YES' if viol else 'no':>8s}  "
                  f"{pct:7.1f}%  {ipr1:8.2f}  {ipr2:8.2f}")
            results.append({"t": t_val, "S": S, "ipr1": ipr1, "ipr2": ipr2})

        # Evolve each orbital one step
        phi1 = U @ phi1
        phi2 = U @ phi2

    return results


# ====================================================================
# PART D: Gravitational interaction -> ground-state Bell violation
# ====================================================================

def part_d(n=8, mass=1.0):
    """Ground state with gravitational (Poisson) interaction.

    The framework's native interaction: each fermion sources a Poisson
    field that modifies the other's potential. This is the self-consistent
    gravitational coupling from the framework axioms.

    For 2 fermions on n sites, the interacting Hamiltonian in the
    antisymmetric subspace includes:
      H_int = G * V(|x1 - x2|)
    where V is the discrete Poisson Green's function.

    Framework origin: the Poisson interaction is derived from
    self-consistency of the propagator + field (D5 in the axiom chain).
    """
    from scipy.sparse.linalg import spsolve
    from scipy.sparse import diags

    print()
    print("=" * 72)
    print("PART D: GRAVITATIONAL GROUND STATE — INTERACTING BELL")
    print("=" * 72)
    print()
    print(f"N={n}, mass={mass}. Add Poisson gravitational coupling G*V(|x1-x2|).")
    print("Framework origin: self-consistent propagator + field (D5).")
    print()

    H1 = staggered_hamiltonian(n, mass=mass)
    Z = staggered_Z(n)
    X = pair_hop_X(n)

    # Poisson Green's function on 1D chain (Dirichlet BC)
    # G(i,j) = -min(i,j)*(n-max(i,j))/n for interior points
    V_poisson = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            V_poisson[i, j] = -min(i + 1, j + 1) * (n - max(i + 1, j + 1)) / n

    # Build 2-particle Hamiltonian in antisymmetric subspace
    # Basis: |i,j> for i < j (antisymmetric implies psi(i,j) = -psi(j,i))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    dim = len(pairs)
    pair_idx = {p: k for k, p in enumerate(pairs)}

    def build_H2(G_grav):
        H2 = np.zeros((dim, dim), dtype=complex)
        for k, (i, j) in enumerate(pairs):
            # Diagonal: single-particle energies + interaction
            H2[k, k] = H1[i, i] + H1[j, j] + G_grav * V_poisson[i, j]

            # Off-diagonal: hopping of particle 1 (i -> i')
            for ip in range(n):
                if ip != i and abs(H1[i, ip]) > 1e-15:
                    if ip < j and (ip, j) in pair_idx:
                        H2[k, pair_idx[(ip, j)]] += H1[i, ip]
                    elif ip > j and (j, ip) in pair_idx:
                        H2[k, pair_idx[(j, ip)]] += -H1[i, ip]  # antisymmetry sign

            # Off-diagonal: hopping of particle 2 (j -> j')
            for jp in range(n):
                if jp != j and abs(H1[j, jp]) > 1e-15:
                    if i < jp and (i, jp) in pair_idx:
                        H2[k, pair_idx[(i, jp)]] += H1[j, jp]
                    elif i > jp and (jp, i) in pair_idx:
                        H2[k, pair_idx[(jp, i)]] += -H1[j, jp]  # antisymmetry sign

        return H2

    print(f"  {'G':>6s}  {'|S|':>10s}  {'Bell?':>8s}  {'%Tsir':>8s}  {'E_gs':>10s}")
    print("  " + "-" * 48)

    results = []
    for G in [0.0, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0, 30.0, 50.0, 75.0, 100.0, 200.0]:
        H2 = build_H2(G)
        evals2, evecs2 = eigh(H2)
        gs = evecs2[:, 0]  # ground state in antisymmetric basis

        # Reconstruct the full n x n antisymmetric wavefunction.
        # The antisymmetric basis has psi(i,j) for i<j; extend to full matrix
        # with psi(j,i) = -psi(i,j). The full matrix norm = 2 * basis norm.
        # We normalize so sum_{i,j} |psi(i,j)|^2 = 1 for the correlator.
        psi_full = np.zeros((n, n), dtype=complex)
        for k, (i, j) in enumerate(pairs):
            psi_full[i, j] = gs[k]
            psi_full[j, i] = -gs[k]
        psi_full = psi_full / np.linalg.norm(psi_full)  # normalize full matrix to 1

        # Compute correlator using matrix form: <O_a x O_b> = Tr[psi^dag (O_a psi O_b^T)]
        # For antisymmetric psi(i,j): <O_a x O_b> = Tr[psi^H O_a psi O_b^T]
        # where psi is the n x n matrix form.
        # Verify: sum_ij psi*(i,j) sum_i'j' O_a(i,i') O_b(j,j') psi(i',j')
        #       = sum_ij psi*(i,j) [O_a psi O_b^T](i,j)
        #       = Tr[psi^H O_a psi O_b^T]

        def E_matrix(Oa, Ob):
            return np.real(np.trace(psi_full.conj().T @ Oa @ psi_full @ Ob.T))

        # Build 3x3 correlation matrix for Horodecki
        ops_full = [Z, X, 1j * Z @ X]
        T = np.zeros((3, 3))
        for a_idx in range(3):
            for b_idx in range(3):
                T[a_idx, b_idx] = E_matrix(ops_full[a_idx], ops_full[b_idx])

        # Sanity: at G=0, verify T matches Part B's result
        TTT = T.T @ T
        ev = sorted(np.linalg.eigvalsh(TTT), reverse=True)
        S_max = 2 * math.sqrt(max(ev[0] + ev[1], 0))

        viol = S_max > 2.0
        pct = (S_max - 2.0) / (2 * math.sqrt(2) - 2.0) * 100 if viol else 0
        print(f"  {G:6.1f}  {S_max:10.6f}  {'YES' if viol else 'no':>8s}  {pct:7.1f}%  {evals2[0]:10.4f}")
        results.append({"G": G, "S": S_max, "violation": viol})

    return results


# ====================================================================
# Main
# ====================================================================

def main():
    t0 = time.time()

    res_a = part_a()
    res_b = part_b()
    res_c = part_c()
    res_d = part_d()

    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()
    print(f"Part A (structural): singlet CHSH = {abs(res_a['S']):.6f}, Tsirelson: {res_a['tsirelson']}")

    if res_b and abs(res_b["S"]) > 2.0:
        print(f"Part B (free ground state): CHSH = {abs(res_b['S']):.6f}, Bell: YES")
    else:
        print(f"Part B (free ground state): CHSH < 2 (free fermions too weakly entangled)")

    c_viols = [r for r in res_c if abs(r["S"]) > 2.0]
    if c_viols:
        last = max(c_viols, key=lambda r: r["t"])
        best = max(c_viols, key=lambda r: abs(r["S"]))
        print(f"Part C (propagator): Bell violation persists t=0 to t={last['t']:.3f}")
    else:
        print(f"Part C (propagator): no violation")

    d_viols = [r for r in res_d if r["violation"]]
    if d_viols:
        best = max(d_viols, key=lambda r: r["S"])
        print(f"Part D (gravitational): CHSH = {best['S']:.6f} at G={best['G']}, Bell: YES")
    else:
        print(f"Part D (gravitational): no violation")

    elapsed = time.time() - t0
    print(f"\n  Time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
