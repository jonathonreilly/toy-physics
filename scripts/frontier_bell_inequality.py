#!/usr/bin/env python3
"""
Bell inequality (CHSH) violation on the lattice propagator.

Physics
-------
The framework (Cl(3) on Z^3) produces:
  1. A staggered lattice with intrinsic sublattice parity (sigma_z)
     and nearest-neighbor hop (sigma_x) forming a Pauli algebra.
  2. A unitary propagator that preserves entanglement.
  3. Dynamics (hopping Hamiltonian) that can create entanglement
     from product initial states.

This script has two parts:

  PART A (structural theorem): The staggered lattice carries a native
  Pauli algebra. Any singlet state on that algebra violates CHSH at
  the Tsirelson bound. This is a structural consequence of the lattice.

  PART B (dynamical test): Starting from a PRODUCT state (zero
  entanglement), the lattice Hamiltonian dynamically generates
  entanglement. We measure CHSH on the dynamically produced state
  and track how the violation grows from zero.

No external spin, polarization, or measurement apparatus is imported.
All operators are intrinsic to Z^3.

PStack experiment: frontier-bell-inequality
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.linalg import expm


# ====================================================================
# Lattice infrastructure (framework-native)
# ====================================================================

def build_1d_hamiltonian(n, t_hop=1.0):
    """1D tight-binding (hopping) Hamiltonian with open boundary conditions.

    This is the kinetic part of the staggered lattice Hamiltonian.
    Framework origin: nearest-neighbor connectivity on Z^1 (the 1D
    restriction of Z^3). The hopping amplitude t_hop is the only scale.
    """
    H = np.zeros((n, n), dtype=complex)
    for i in range(n - 1):
        H[i, i + 1] = -t_hop
        H[i + 1, i] = -t_hop
    return H


def staggered_parity(n):
    """Staggered sublattice parity: +1 on even sites, -1 on odd.

    Framework origin: the cubic lattice Z^d has a natural bipartite
    (checkerboard) structure. The parity operator (-1)^{x_1+...+x_d}
    is intrinsic. On the 2-site subspace of adjacent sites, this is
    exactly sigma_z.
    """
    Z = np.zeros((n, n), dtype=complex)
    for i in range(n):
        Z[i, i] = 1.0 if i % 2 == 0 else -1.0
    return Z


def sublattice_hop(n):
    """Nearest-neighbor hop restricted to even->odd pairs.

    Framework origin: the hopping operator on Z^d connects nearest
    neighbors. Restricted to an even-odd pair, this is sigma_x.
    On the full lattice it is block-diagonal in even-odd pairs.
    """
    X = np.zeros((n, n), dtype=complex)
    for i in range(n - 1):
        if i % 2 == 0:
            X[i, i + 1] = 1.0
            X[i + 1, i] = 1.0
    return X


# ====================================================================
# PART A: Structural theorem — native Pauli algebra on Z^d
# ====================================================================

def part_a_structural_theorem():
    """
    Prove that the staggered lattice carries a native Pauli algebra
    and that any singlet on it saturates the Tsirelson bound.

    This is a STRUCTURAL result: the lattice geometry provides the
    operators; the Hilbert space axiom (A2) provides the state space.
    Together they force CHSH violation.

    What is framework-native:
      - Z = staggered parity (intrinsic to Z^d)
      - X = nearest-neighbor hop (intrinsic to Z^d)
      - Hilbert space (from unitarity, A2)
      - Tensor product (two particles on the same graph)

    What we verify:
      - Z^2 = I, X^2 = I, {Z,X} = 0 on the 2-site subspace
      - These are the Pauli algebra
      - The singlet on this algebra gives |S| = 2*sqrt(2)
    """
    print("=" * 72)
    print("PART A: STRUCTURAL THEOREM — NATIVE PAULI ALGEBRA ON Z^d")
    print("=" * 72)
    print()

    # Build lattice operators on a small chain
    n = 10
    Z_full = staggered_parity(n)
    X_full = sublattice_hop(n)

    # Extract the 2x2 block for adjacent sites at the center
    center = n // 2
    site_e = center if center % 2 == 0 else center - 1
    site_o = site_e + 1
    sites = [site_e, site_o]

    Z2 = Z_full[np.ix_(sites, sites)]
    X2 = X_full[np.ix_(sites, sites)]

    print(f"Lattice: 1D chain, N={n}")
    print(f"Adjacent sites: {site_e} (even), {site_o} (odd)")
    print()
    print("Sublattice operators restricted to 2-site subspace:")
    print(f"  Z = diag(+1, -1) = {Z2.real.tolist()}")
    print(f"  X = off-diag(1)  = {X2.real.tolist()}")
    print()

    # Pauli algebra checks
    z_sq = np.allclose(Z2 @ Z2, np.eye(2))
    x_sq = np.allclose(X2 @ X2, np.eye(2))
    anticomm = np.allclose(Z2 @ X2 + X2 @ Z2, 0)
    z_eig = sorted(np.linalg.eigvalsh(Z2).real)
    x_eig = sorted(np.linalg.eigvalsh(X2).real)

    print("Pauli algebra verification:")
    print(f"  Z^2 = I?    {z_sq}")
    print(f"  X^2 = I?    {x_sq}")
    print(f"  {{Z, X}} = 0? {anticomm}")
    print(f"  Z eigenvalues: {z_eig}")
    print(f"  X eigenvalues: {x_eig}")
    print()

    all_pauli = z_sq and x_sq and anticomm
    if all_pauli:
        print("  CONFIRMED: sublattice operators form a Pauli algebra.")
    else:
        print("  FAILED: operators do not satisfy Pauli algebra.")
        return {"pauli": False}

    # Now prove CHSH violation for the singlet on this algebra.
    # The singlet |psi-> = (|e,o> - |o,e>) / sqrt(2) is the unique
    # antisymmetric state of two particles on adjacent sites.
    print()
    print("Singlet state on the sublattice Pauli algebra:")
    print("  |psi-> = (|even,odd> - |odd,even>) / sqrt(2)")
    print("  This is the antisymmetric state under particle exchange.")
    print()

    psi = np.array([0, 1, -1, 0], dtype=complex) / math.sqrt(2)

    def meas_op(theta):
        return math.cos(theta) * Z2 + math.sin(theta) * X2

    def E(ta, tb):
        AB = np.kron(meas_op(ta), meas_op(tb))
        return np.real(np.conj(psi) @ AB @ psi)

    # Optimal CHSH angles for singlet with E(a,b) = -cos(a-b):
    a, ap, b, bp = 0.0, math.pi/2, math.pi/4, 3*math.pi/4

    Eab = E(a, b)
    Eabp = E(a, bp)
    Eapb = E(ap, b)
    Eapbp = E(ap, bp)
    S = Eab - Eabp + Eapb + Eapbp

    print("CHSH with optimal angles (a=0, a'=pi/2, b=pi/4, b'=3pi/4):")
    print(f"  E(a, b)    = {Eab:+.10f}   (expect -1/sqrt2 = {-1/math.sqrt(2):+.10f})")
    print(f"  E(a, b')   = {Eabp:+.10f}   (expect +1/sqrt2 = {+1/math.sqrt(2):+.10f})")
    print(f"  E(a', b)   = {Eapb:+.10f}   (expect -1/sqrt2)")
    print(f"  E(a', b')  = {Eapbp:+.10f}   (expect -1/sqrt2)")
    print()
    print(f"  S = {S:+.10f}")
    print(f"  |S| = {abs(S):.10f}")
    print(f"  Classical bound: 2.0000000000")
    print(f"  Tsirelson bound: {2*math.sqrt(2):.10f}")
    print()

    violation = abs(S) > 2.0
    at_tsirelson = abs(abs(S) - 2*math.sqrt(2)) < 1e-9

    if violation and at_tsirelson:
        print("  RESULT: TSIRELSON BOUND SATURATED")
        print("  The native sublattice Pauli algebra + singlet -> maximal CHSH.")
    elif violation:
        print(f"  RESULT: BELL VIOLATION (|S| = {abs(S):.6f})")
    else:
        print("  RESULT: NO VIOLATION")

    # Angle sweep: verify E(0, theta) = -cos(theta) across full range
    print()
    print("  Correlator verification: E(0, theta) vs -cos(theta)")
    max_diff = 0.0
    for k in range(13):
        theta = k * math.pi / 12
        E_num = E(0.0, theta)
        E_exact = -math.cos(theta)
        diff = abs(E_num - E_exact)
        max_diff = max(max_diff, diff)
    print(f"  Max |E_lattice - E_analytic| = {max_diff:.2e}")
    print(f"  (across 13 angles from 0 to pi)")

    # Verify this holds on multiple lattice sizes
    print()
    print("  Size independence check:")
    for n_test in [6, 10, 20, 50, 100]:
        Z_t = staggered_parity(n_test)
        X_t = sublattice_hop(n_test)
        c = n_test // 2
        se = c if c % 2 == 0 else c - 1
        so = se + 1
        ss = [se, so]
        Z_t2 = Z_t[np.ix_(ss, ss)]
        X_t2 = X_t[np.ix_(ss, ss)]
        ok = (np.allclose(Z_t2 @ Z_t2, np.eye(2))
              and np.allclose(X_t2 @ X_t2, np.eye(2))
              and np.allclose(Z_t2 @ X_t2 + X_t2 @ Z_t2, 0))
        print(f"    N={n_test:4d}: Pauli algebra = {ok}")

    return {
        "pauli": all_pauli,
        "S": S,
        "violation": violation,
        "tsirelson": at_tsirelson,
    }


# ====================================================================
# PART B: Dynamical test — entanglement from product initial state
# ====================================================================

def part_b_dynamical_bell(n=16):
    """
    Start from a PRODUCT state. Let the lattice Hamiltonian evolve
    the two-particle state. Measure how entanglement and CHSH grow
    from zero.

    This is the key honest test: does the framework's own dynamics
    create Bell-violating correlations, or do we need to hand-insert
    entanglement?

    Protocol:
      1. Two particles start on sites (center-2) and (center+2) in a
         product state: |psi> = |site_A> x |site_B>.
      2. Evolve under H_2 = H x I + I x H (non-interacting hopping).
      3. At each time step, compute the CHSH correlator in the
         sublattice basis.

    Important caveat: non-interacting hopping of distinguishable
    particles does NOT create entanglement in the first-quantized
    tensor product. We need either:
      (a) an interaction (gravity, or contact), or
      (b) indistinguishable (fermionic) statistics with antisymmetrization.

    We test BOTH routes below.
    """
    print()
    print("=" * 72)
    print("PART B: DYNAMICAL BELL — ENTANGLEMENT FROM PRODUCT STATE")
    print("=" * 72)
    print()
    print(f"Lattice: 1D chain, N={n}")
    print()

    H = build_1d_hamiltonian(n)
    Z_full = staggered_parity(n)
    X_full = sublattice_hop(n)

    # Pick measurement sites: one even-odd pair for Alice, one for Bob
    # Alice measures at sites (n//2 - 2, n//2 - 1)
    # Bob measures at sites (n//2, n//2 + 1)
    a_even = n // 2 - 2
    if a_even % 2 != 0:
        a_even -= 1
    a_odd = a_even + 1
    b_even = n // 2
    if b_even % 2 != 0:
        b_even += 1
    b_odd = b_even + 1

    print(f"Alice sites: {a_even} (even), {a_odd} (odd)")
    print(f"Bob sites:   {b_even} (even), {b_odd} (odd)")
    print()

    # Extract 2x2 Pauli blocks for Alice and Bob
    a_sites = [a_even, a_odd]
    b_sites = [b_even, b_odd]
    Z_A = Z_full[np.ix_(a_sites, a_sites)]
    X_A = X_full[np.ix_(a_sites, a_sites)]
    Z_B = Z_full[np.ix_(b_sites, b_sites)]
    X_B = X_full[np.ix_(b_sites, b_sites)]

    def meas_A(theta):
        return math.cos(theta) * Z_A + math.sin(theta) * X_A

    def meas_B(theta):
        return math.cos(theta) * Z_B + math.sin(theta) * X_B

    # ── Route 1: Fermionic antisymmetrization ──────────────────────
    print("--- Route 1: Fermionic antisymmetrization ---")
    print("Two fermions -> antisymmetric spatial wavefunction")
    print()

    # Start: particle 1 at a_even, particle 2 at b_even
    # Antisymmetrize: (|a_even, b_even> - |b_even, a_even>) / sqrt(2)
    psi_f = np.zeros(n * n, dtype=complex)
    psi_f[a_even * n + b_even] = 1.0 / math.sqrt(2)
    psi_f[b_even * n + a_even] = -1.0 / math.sqrt(2)

    # This is a product state in the SPATIAL DOF only if the particles
    # are distinguishable. For identical fermions, the antisymmetrization
    # IS the physics — it's not hand-inserted, it's required by A2
    # (unitarity of the many-body propagator on fermions).

    In = np.eye(n, dtype=complex)
    H2 = np.kron(H, In) + np.kron(In, H)

    dt = 0.05
    times = [0, 5, 10, 20, 40, 60, 80, 100]

    print(f"  {'t':>6s}  {'|S|':>10s}  {'S_ent':>10s}  {'frac_AB':>10s}  {'status':>12s}")
    print("  " + "-" * 56)

    results_f = []
    for n_steps in times:
        if n_steps == 0:
            psi = psi_f.copy()
        else:
            U2 = expm(-1j * H2 * dt * n_steps)
            psi = U2 @ psi_f

        psi = psi / np.linalg.norm(psi)

        # Partial trace for entanglement entropy
        rho1 = np.zeros((n, n), dtype=complex)
        psi_mat = psi.reshape(n, n)
        rho1 = psi_mat @ psi_mat.conj().T
        ev = np.linalg.eigvalsh(rho1)
        ev = ev[ev > 1e-15]
        S_ent = -np.sum(ev * np.log(ev))

        # Project onto Alice x Bob qubit subspaces
        psi_q = np.zeros(4, dtype=complex)
        for ia, sa in enumerate(a_sites):
            for ib, sb in enumerate(b_sites):
                psi_q[ia * 2 + ib] = psi[sa * n + sb]
        nq = np.linalg.norm(psi_q)
        if nq > 1e-12:
            psi_q_norm = psi_q / nq
        else:
            psi_q_norm = psi_q

        # CHSH
        chsh_a, chsh_ap = 0.0, math.pi / 2
        chsh_b, chsh_bp = math.pi / 4, 3 * math.pi / 4

        def Eq(ta, tb):
            A = meas_A(ta)
            B = meas_B(tb)
            AB = np.kron(A, B)
            return np.real(np.conj(psi_q_norm) @ AB @ psi_q_norm)

        if nq > 1e-12:
            S_chsh = Eq(chsh_a, chsh_b) - Eq(chsh_a, chsh_bp) + Eq(chsh_ap, chsh_b) + Eq(chsh_ap, chsh_bp)
        else:
            S_chsh = 0.0

        status = "VIOLATION" if abs(S_chsh) > 2.0 else "sub-classical" if abs(S_chsh) < 1e-6 else "classical"
        t_val = n_steps * dt
        print(f"  {t_val:6.2f}  {abs(S_chsh):10.6f}  {S_ent:10.6f}  {nq**2:10.6f}  {status:>12s}")

        results_f.append({
            "t": t_val, "S": S_chsh, "S_ent": S_ent, "frac": nq**2,
        })

    # ── Route 2: Contact interaction ──────────────────────────────
    print()
    print("--- Route 2: Contact interaction (distinguishable particles) ---")
    print("Two distinguishable particles with on-site repulsion U")
    print()

    U_contact = 4.0  # on-site interaction strength

    # Product initial state (no antisymmetrization)
    psi_d = np.zeros(n * n, dtype=complex)
    # Particle 1 at a_even, particle 2 at b_even
    psi_d[a_even * n + b_even] = 1.0

    # Two-particle Hamiltonian with contact interaction
    H2_int = np.kron(H, In) + np.kron(In, H)
    # Add on-site repulsion: U * delta(x1, x2)
    for i in range(n):
        H2_int[i * n + i, i * n + i] += U_contact

    print(f"  U_contact = {U_contact}")
    print(f"  Initial: product state |{a_even}> x |{b_even}>")
    print()
    print(f"  {'t':>6s}  {'|S|':>10s}  {'S_ent':>10s}  {'frac_AB':>10s}  {'status':>12s}")
    print("  " + "-" * 56)

    results_d = []
    for n_steps in times:
        if n_steps == 0:
            psi = psi_d.copy()
        else:
            U2 = expm(-1j * H2_int * dt * n_steps)
            psi = U2 @ psi_d

        psi = psi / np.linalg.norm(psi)

        # Entanglement entropy
        psi_mat = psi.reshape(n, n)
        rho1 = psi_mat @ psi_mat.conj().T
        ev = np.linalg.eigvalsh(rho1)
        ev = ev[ev > 1e-15]
        S_ent = -np.sum(ev * np.log(ev))

        # Project to Alice x Bob qubit subspaces
        psi_q = np.zeros(4, dtype=complex)
        for ia, sa in enumerate(a_sites):
            for ib, sb in enumerate(b_sites):
                psi_q[ia * 2 + ib] = psi[sa * n + sb]
        nq = np.linalg.norm(psi_q)
        if nq > 1e-12:
            psi_q_norm = psi_q / nq
        else:
            psi_q_norm = psi_q

        if nq > 1e-12:
            S_chsh = Eq(chsh_a, chsh_b) - Eq(chsh_a, chsh_bp) + Eq(chsh_ap, chsh_b) + Eq(chsh_ap, chsh_bp)
        else:
            S_chsh = 0.0

        status = "VIOLATION" if abs(S_chsh) > 2.0 else "sub-classical" if abs(S_chsh) < 1e-6 else "classical"
        t_val = n_steps * dt
        print(f"  {t_val:6.2f}  {abs(S_chsh):10.6f}  {S_ent:10.6f}  {nq**2:10.6f}  {status:>12s}")

        results_d.append({
            "t": t_val, "S": S_chsh, "S_ent": S_ent, "frac": nq**2,
        })

    return {"fermionic": results_f, "contact": results_d}


# ====================================================================
# Main
# ====================================================================

def main():
    t0 = time.time()

    # Part A: structural theorem
    result_a = part_a_structural_theorem()

    # Part B: dynamical test
    result_b = part_b_dynamical_bell()

    # ── Summary ─────────────────────────────────────────────────────
    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()
    print("PART A (structural):")
    print(f"  Sublattice Pauli algebra: {'CONFIRMED' if result_a['pauli'] else 'FAILED'}")
    print(f"  Singlet CHSH |S| = {abs(result_a['S']):.10f}")
    print(f"  Tsirelson saturated: {result_a['tsirelson']}")
    print()
    print("  Interpretation: The staggered lattice Z^d carries a native")
    print("  Pauli algebra (sigma_z = sublattice parity, sigma_x = hop).")
    print("  Any singlet on this algebra saturates the Tsirelson bound.")
    print("  This is a structural theorem: the lattice geometry + Hilbert")
    print("  space axiom together guarantee maximal Bell violation.")
    print()
    print("PART B (dynamical):")

    # Check if any dynamical route produced violation
    f_violations = [r for r in result_b["fermionic"] if abs(r["S"]) > 2.0]
    d_violations = [r for r in result_b["contact"] if abs(r["S"]) > 2.0]

    if f_violations:
        best = max(f_violations, key=lambda r: abs(r["S"]))
        print(f"  Fermionic route: VIOLATION at t={best['t']:.2f}, |S|={abs(best['S']):.6f}")
    else:
        print("  Fermionic route: no violation in qubit subspace")
        max_ent = max(r["S_ent"] for r in result_b["fermionic"])
        print(f"    (max entanglement entropy: {max_ent:.6f} nats)")

    if d_violations:
        best = max(d_violations, key=lambda r: abs(r["S"]))
        print(f"  Contact route: VIOLATION at t={best['t']:.2f}, |S|={abs(best['S']):.6f}")
    else:
        print("  Contact route: no violation in qubit subspace")
        max_ent = max(r["S_ent"] for r in result_b["contact"])
        print(f"    (max entanglement entropy: {max_ent:.6f} nats)")

    print()
    print("CLAIM BOUNDARY:")
    print("  The structural theorem (Part A) is exact and framework-native.")
    print("  The dynamical test (Part B) is exploratory: whether the")
    print("  lattice dynamics produce Bell-violating states in a specific")
    print("  measurement subspace depends on the initial conditions and")
    print("  interaction. The structural result does not depend on dynamics.")

    elapsed = time.time() - t0
    print(f"\n  Time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
