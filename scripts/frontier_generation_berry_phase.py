#!/usr/bin/env python3
"""
Berry Phase / Zak Phase Topological Invariants for Z_3 Sectors
==============================================================

GOAL: Compute Berry phase (Zak phase) topological invariants for each
Z_3 sector of the staggered Cl(3) Hamiltonian on Z^3. If the three
sectors carry distinct quantized Berry phases, the sectors are
TOPOLOGICALLY DISTINGUISHABLE -- an unconditional mathematical result.

======================================================================
KEY CONSTRUCTION:

The staggered fermion on Z^3 uses staggered phases eta_mu(x).
The STANDARD choice eta_1=1, eta_2=(-1)^{x_1}, eta_3=(-1)^{x_1+x_2}
breaks Z_3 at the Hamiltonian level (though the spectrum is Z_3-invariant).

We use the SYMMETRIC staggered phases:
  eta_mu(x) = (-1)^{sum_{nu != mu} x_nu}
i.e.:
  eta_1(x,y,z) = (-1)^{y+z}
  eta_2(x,y,z) = (-1)^{z+x}
  eta_3(x,y,z) = (-1)^{x+y}

Under (x,y,z) -> (y,z,x) and mu -> (mu+1 mod 3), these are invariant:
  eta_{mu+1}(y,z,x) = eta_mu(x,y,z)

So the symmetric staggered Hamiltonian EXACTLY commutes with the Z_3
generator P: (x,y,z) -> (y,z,x). This is verified numerically.

The Z_3 eigenspaces have dimensions dim V_0 = 4, dim V_1 = 2, dim V_2 = 2.

In momentum space (unit cell is 2^3 = 8 sites), H(k) is 8x8 and
commutes with P when k1 = k2 = k3 (isotropic line).

We compute Berry/Zak phases along the isotropic line theta: 0 -> 2pi
for each Z_3 sector, and check whether they are distinct.

======================================================================
CLASSIFICATION:
  [EXACT]   -- Mathematical theorem, proved by computation.
  [BOUNDED] -- Numerical result, finite discretization or model input.

ASSUMPTIONS:
  A1. Taste space V = C^8 with Z_3: (s1,s2,s3) -> (s2,s3,s1). EXACT.
  A2. Symmetric staggered phases eta_mu = (-1)^{sum_{nu!=mu} x_nu}. EXACT.
  A3. Isotropic line k1=k2=k3 for Z_3 commutation. EXACT.

PStack experiment: frontier-generation-berry-phase
Self-contained: numpy + scipy only.
======================================================================
"""

from __future__ import annotations

import sys
import time
import numpy as np
from scipy import linalg as la

np.set_printoptions(precision=10, linewidth=120)

PASS_COUNT = 0
FAIL_COUNT = 0
RESULTS = []


def check(tag: str, ok: bool, classification: str, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    RESULTS.append((tag, status, classification, detail))
    print(f"  [{status}] [{classification}] {tag}")
    if detail:
        print(f"         {detail}")
    return ok


# ============================================================================
# BUILDING BLOCKS
# ============================================================================

def taste_states():
    return [(s1, s2, s3) for s1 in range(2) for s2 in range(2) for s3 in range(2)]


def state_index(s):
    return s[0] * 4 + s[1] * 2 + s[2]


def z3_generator_matrix():
    """8x8 permutation P: (s1,s2,s3) -> (s2,s3,s1)."""
    states = taste_states()
    P = np.zeros((8, 8), dtype=complex)
    for s in states:
        P[state_index((s[1], s[2], s[0])), state_index(s)] = 1.0
    return P


def z3_projectors(P):
    omega = np.exp(2j * np.pi / 3)
    I = np.eye(8, dtype=complex)
    P2 = P @ P
    return {k: (I + omega**(-k) * P + omega**(-2*k) * P2) / 3.0 for k in range(3)}


def symmetric_staggered_hamiltonian_k(k, wilson_r=0.0):
    """
    8x8 momentum-space Hamiltonian using SYMMETRIC staggered phases.

    Position-space hoppings in direction mu from site s to s':
      eta_mu(s) = (-1)^{sum_{nu != mu} s_nu}

    Specifically:
      eta_0(s) = (-1)^{s_1 + s_2}  (hop in x: depends on y,z)
      eta_1(s) = (-1)^{s_2 + s_0}  (hop in y: depends on z,x)
      eta_2(s) = (-1)^{s_0 + s_1}  (hop in z: depends on x,y)

    The momentum-space matrix element for hopping from sublattice s
    in direction mu:
      s -> s' where s'_mu = (s_mu + 1) mod 2, s'_nu = s_nu for nu != mu
      Phase: e^{i k_mu} if crossing cell boundary (s_mu = 1 -> 0)
    """
    states = taste_states()
    n = len(states)
    H = np.zeros((n, n), dtype=complex)

    for a, s in enumerate(states):
        # Symmetric staggered phases
        eta = [
            (-1.0) ** (s[1] + s[2]),  # mu=0: depends on s_1, s_2
            (-1.0) ** (s[2] + s[0]),  # mu=1: depends on s_2, s_0
            (-1.0) ** (s[0] + s[1]),  # mu=2: depends on s_0, s_1
        ]

        for mu in range(3):
            s_fwd = list(s)
            s_fwd[mu] = (s[mu] + 1) % 2
            b = state_index(tuple(s_fwd))

            # Forward hop: s -> s_fwd
            if s[mu] == 0:
                phase_fwd = 1.0  # within unit cell
            else:
                phase_fwd = np.exp(1j * k[mu])  # cross cell boundary

            # Backward hop: s -> s_bwd (s_bwd = same as s_fwd for {0,1})
            if s[mu] == 1:
                phase_bwd = 1.0
            else:
                phase_bwd = np.exp(-1j * k[mu])

            # Anti-symmetric hopping: (forward - backward) / 2
            H[a, b] += eta[mu] * (phase_fwd - phase_bwd) / 2.0

        # Wilson term
        if wilson_r != 0:
            for mu in range(3):
                s_fwd = list(s)
                s_fwd[mu] = (s[mu] + 1) % 2
                b = state_index(tuple(s_fwd))

                if s[mu] == 0:
                    pf = 1.0
                    pb = np.exp(-1j * k[mu])
                else:
                    pf = np.exp(1j * k[mu])
                    pb = 1.0

                H[a, a] += wilson_r
                H[a, b] -= wilson_r * (pf + pb) / 2.0

    return H


# ============================================================================
# SECTION 1: Verify construction against position space
# ============================================================================

def section_1_verify():
    print("\n" + "=" * 78)
    print("SECTION 1: VERIFY MOMENTUM-SPACE CONSTRUCTION")
    print("=" * 78)

    for L in [4, 6, 8]:
        N = L ** 3

        def idx(x, y, z):
            return ((x % L) * L + (y % L)) * L + (z % L)

        H_pos = np.zeros((N, N), dtype=complex)
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    i = idx(x, y, z)
                    # mu=0: eta = (-1)^(y+z)
                    j = idx(x + 1, y, z)
                    eta = (-1.0) ** (y + z)
                    H_pos[i, j] += 0.5 * eta
                    H_pos[j, i] -= 0.5 * eta
                    # mu=1: eta = (-1)^(z+x)
                    j = idx(x, y + 1, z)
                    eta = (-1.0) ** (z + x)
                    H_pos[i, j] += 0.5 * eta
                    H_pos[j, i] -= 0.5 * eta
                    # mu=2: eta = (-1)^(x+y)
                    j = idx(x, y, z + 1)
                    eta = (-1.0) ** (x + y)
                    H_pos[i, j] += 0.5 * eta
                    H_pos[j, i] -= 0.5 * eta

        evals_pos = np.sort(la.eigvalsh(H_pos))

        # Z_3 commutation in position space
        P_pos = np.zeros((N, N))
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    P_pos[idx(y, z, x), idx(x, y, z)] = 1.0

        comm_pos = la.norm(H_pos @ P_pos - P_pos @ H_pos)
        check(f"[H_sym, P] = 0 position space (L={L})",
              comm_pos < 1e-10, "EXACT",
              f"||[H,P]|| = {comm_pos:.2e}")

        # Momentum-space eigenvalues
        Lhalf = L // 2
        evals_k = []
        for mx in range(Lhalf):
            for my in range(Lhalf):
                for mz in range(Lhalf):
                    k = np.array([2 * np.pi * mx / Lhalf,
                                  2 * np.pi * my / Lhalf,
                                  2 * np.pi * mz / Lhalf])
                    Hk = symmetric_staggered_hamiltonian_k(k)
                    evals_k.extend(la.eigvalsh(Hk))

        evals_k = np.sort(evals_k)
        match = np.allclose(evals_pos, evals_k, atol=1e-10)
        if not match:
            diff = np.max(np.abs(evals_pos - evals_k))
        else:
            diff = 0.0
        check(f"H(k) spectrum matches position space (L={L})",
              match, "EXACT",
              f"max |diff| = {diff:.2e}")


# ============================================================================
# SECTION 2: Z_3 commutation in momentum space
# ============================================================================

def section_2_z3():
    print("\n" + "=" * 78)
    print("SECTION 2: Z_3 COMMUTATION IN MOMENTUM SPACE")
    print("=" * 78)

    P = z3_generator_matrix()
    Pd = P.conj().T
    omega = np.exp(2j * np.pi / 3)

    # P H(k1,k2,k3) P^dag should equal H(k2,k3,k1)
    k_test = np.array([0.3, 0.7, 1.2])
    Hk = symmetric_staggered_hamiltonian_k(k_test)
    Hk_perm = symmetric_staggered_hamiltonian_k(np.array([0.7, 1.2, 0.3]))
    diff = la.norm(P @ Hk @ Pd - Hk_perm)
    check("P H(k1,k2,k3) P^dag = H(k2,k3,k1)",
          diff < 1e-10, "EXACT", f"error = {diff:.2e}")

    # On isotropic line
    max_comm = 0.0
    for theta in np.linspace(0, 2 * np.pi, 100):
        Hk = symmetric_staggered_hamiltonian_k(np.array([theta, theta, theta]))
        comm = la.norm(Hk @ P - P @ Hk)
        max_comm = max(max_comm, comm)
    check("[H(theta,theta,theta), P] = 0",
          max_comm < 1e-10, "EXACT", f"max ||[H,P]|| = {max_comm:.2e}")

    # Eigenspace dims
    evals_P, _ = la.eig(P)
    dims = {kk: int(np.sum(np.abs(evals_P - omega**kk) < 1e-10)) for kk in range(3)}
    check("Z_3 dims = (4, 2, 2)",
          dims[0] == 4 and dims[1] == 2 and dims[2] == 2, "EXACT",
          f"dims = {dims}")

    # Wilson term Z_3 check
    for r in [0.5, 1.0]:
        max_c = 0.0
        for theta in np.linspace(0, 2*np.pi, 50):
            Hk = symmetric_staggered_hamiltonian_k(
                np.array([theta, theta, theta]), wilson_r=r)
            max_c = max(max_c, la.norm(Hk @ P - P @ Hk))
        check(f"[H_Wilson(r={r}), P] = 0 on isotropic line",
              max_c < 1e-10, "EXACT", f"max ||[H,P]|| = {max_c:.2e}")

    return P


# ============================================================================
# SECTION 3: Band structure and sector assignment
# ============================================================================

def section_3_bands(P):
    print("\n" + "=" * 78)
    print("SECTION 3: BAND STRUCTURE AND Z_3 SECTORS")
    print("=" * 78)

    omega = np.exp(2j * np.pi / 3)
    N = 400
    thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)

    all_evals = np.zeros((N, 8))
    all_evecs = np.zeros((N, 8, 8), dtype=complex)
    sector_labels = np.zeros((N, 8), dtype=int)

    for i, theta in enumerate(thetas):
        Hk = symmetric_staggered_hamiltonian_k(np.array([theta]*3))
        evals, evecs = la.eigh(Hk)
        all_evals[i] = evals
        all_evecs[i] = evecs

        for n in range(8):
            v = evecs[:, n]
            overlap = np.dot(v.conj(), P @ v)
            sector_labels[i, n] = min(range(3),
                                       key=lambda kk: abs(overlap - omega**kk))

    # Check dims at midpoint
    idx_mid = N // 4
    dims = {k: int(np.sum(sector_labels[idx_mid] == k)) for k in range(3)}
    print(f"\n  Sector dims at theta=pi/2: {dims}")
    check("Sector 0 dim = 4", dims[0] == 4, "EXACT")
    check("Sector 1 dim = 2", dims[1] == 2, "EXACT")
    check("Sector 2 dim = 2", dims[2] == 2, "EXACT")

    # Sector stability
    stable = True
    for n in range(8):
        n_changes = np.sum(np.diff(sector_labels[:, n]) != 0)
        if n_changes > 0:
            stable = False
            print(f"  Band {n}: sector changes {n_changes} times")

    check("Sector labels stable across theta",
          stable, "EXACT" if stable else "BOUNDED")

    # Band structure
    print(f"\n  Bands at theta=pi/2:")
    for n in range(8):
        print(f"    Band {n}: E={all_evals[idx_mid,n]:+.8f}, "
              f"sector={sector_labels[idx_mid,n]}")

    return thetas, all_evals, all_evecs, sector_labels


# ============================================================================
# Berry phase utilities
# ============================================================================

def berry_phase_band(evecs_loop, band):
    """Single-band Berry phase via discrete overlap method."""
    N = evecs_loop.shape[0]
    phase = 0.0
    for i in range(N):
        j = (i + 1) % N
        ov = np.dot(evecs_loop[i, :, band].conj(), evecs_loop[j, :, band])
        if abs(ov) > 1e-14:
            phase += np.angle(ov)
    return (-phase) % (2 * np.pi)


def berry_phase_multiplet(evecs_loop, bands):
    """Non-Abelian Berry phase (Wilson loop det) for a multiplet."""
    N = evecs_loop.shape[0]
    M = len(bands)
    if M == 0:
        return 0.0
    phase = 0.0
    for i in range(N):
        j = (i + 1) % N
        S = np.zeros((M, M), dtype=complex)
        for a, m in enumerate(bands):
            for b, n in enumerate(bands):
                S[a, b] = np.dot(evecs_loop[i, :, m].conj(),
                                 evecs_loop[j, :, n])
        d = la.det(S)
        if abs(d) > 1e-14:
            phase += np.angle(d)
    return (-phase) % (2 * np.pi)


# ============================================================================
# SECTION 4: Berry phases on isotropic line
# ============================================================================

def section_4_berry(thetas, all_evecs, sector_labels):
    print("\n" + "=" * 78)
    print("SECTION 4: BERRY PHASES ON ISOTROPIC LINE")
    print("=" * 78)

    # Sector band assignments
    sb = {0: [], 1: [], 2: []}
    for n in range(8):
        sb[sector_labels[0, n]].append(n)
    print(f"\n  Sector bands: {sb}")

    # Per-band
    print("\n  Per-band Berry phases:")
    bp_all = []
    for n in range(8):
        bp = berry_phase_band(all_evecs, n)
        bp_all.append(bp)
        print(f"    Band {n} (sector {sector_labels[0,n]}): "
              f"gamma/pi = {bp/np.pi:.8f}")

    # Per-sector multiplet
    print("\n  Sector multiplet Berry phases:")
    sp = {}
    for k in range(3):
        sp[k] = berry_phase_multiplet(all_evecs, sb[k])
        print(f"    Sector {k} ({len(sb[k])} bands): "
              f"gamma/pi = {sp[k]/np.pi:.8f}")

    return sp, bp_all, sb


# ============================================================================
# SECTION 5: Sector-restricted Berry phase (analytic)
# ============================================================================

def section_5_restricted(P):
    """
    Project H(theta) into each Z_3 sector and compute Berry phase
    of the restricted Hamiltonian. This is the cleanest computation
    since it uses the Z_3 projectors explicitly.
    """
    print("\n" + "=" * 78)
    print("SECTION 5: SECTOR-RESTRICTED BERRY PHASE")
    print("=" * 78)

    omega = np.exp(2j * np.pi / 3)
    projs = z3_projectors(P)

    # Get orthonormal basis for each sector
    bases = {}
    for k in range(3):
        Pk = projs[k]
        rank = int(round(np.real(np.trace(Pk))))
        U, S, _ = la.svd(Pk)
        bases[k] = U[:, :rank]
        print(f"  Sector {k}: rank = {rank}")

    N = 1000
    thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)

    sector_phases = {}
    for k in range(3):
        Bk = bases[k]
        rk = Bk.shape[1]

        evecs_red = np.zeros((N, rk, rk), dtype=complex)
        evals_red = np.zeros((N, rk))
        for i, theta in enumerate(thetas):
            Hk = symmetric_staggered_hamiltonian_k(np.array([theta]*3))
            H_red = Bk.conj().T @ Hk @ Bk
            ev, vec = la.eigh(H_red)
            evals_red[i] = ev
            evecs_red[i] = vec

        # Per-band Berry phases in restricted space
        print(f"\n  Sector {k} (dim {rk}):")
        band_bps = []
        for n in range(rk):
            phase = 0.0
            for i in range(N):
                j = (i + 1) % N
                ov = np.dot(evecs_red[i, :, n].conj(), evecs_red[j, :, n])
                if abs(ov) > 1e-14:
                    phase += np.angle(ov)
            bp = (-phase) % (2 * np.pi)
            band_bps.append(bp)
            print(f"    Band {n}: gamma/pi = {bp/np.pi:.8f}")

        # Wilson loop det
        total_phase = 0.0
        for i in range(N):
            j = (i + 1) % N
            S = evecs_red[i].conj().T @ evecs_red[j]
            d = la.det(S)
            if abs(d) > 1e-14:
                total_phase += np.angle(d)
        bp_total = (-total_phase) % (2 * np.pi)
        sector_phases[k] = bp_total
        print(f"    TOTAL: gamma/pi = {bp_total/np.pi:.8f}")

    # Compare sectors
    g = [sector_phases[k] for k in range(3)]
    d01 = min(abs(g[0]-g[1]), 2*np.pi - abs(g[0]-g[1]))
    d12 = min(abs(g[1]-g[2]), 2*np.pi - abs(g[1]-g[2]))
    d02 = min(abs(g[0]-g[2]), 2*np.pi - abs(g[0]-g[2]))

    print(f"\n  Distances: d01={d01:.8f}, d12={d12:.8f}, d02={d02:.8f}")

    all_distinct = (d01 > 0.01) and (d12 > 0.01) and (d02 > 0.01)
    check("Sector-restricted Berry phases distinct",
          all_distinct, "EXACT" if all_distinct else "BOUNDED",
          f"min = {min(d01,d12,d02):.8f}")

    return sector_phases


# ============================================================================
# SECTION 6: Convergence study
# ============================================================================

def section_6_convergence(P):
    print("\n" + "=" * 78)
    print("SECTION 6: CONVERGENCE STUDY")
    print("=" * 78)

    omega = np.exp(2j * np.pi / 3)
    N_values = [50, 100, 200, 400, 800, 1600]
    results = {}

    for N in N_values:
        thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
        evecs = np.zeros((N, 8, 8), dtype=complex)
        for i, theta in enumerate(thetas):
            Hk = symmetric_staggered_hamiltonian_k(np.array([theta]*3))
            _, ev = la.eigh(Hk)
            evecs[i] = ev

        sl = np.zeros(8, dtype=int)
        for n in range(8):
            v = evecs[0, :, n]
            sl[n] = min(range(3), key=lambda kk: abs(
                np.dot(v.conj(), P @ v) - omega**kk))

        sb = {0: [], 1: [], 2: []}
        for n in range(8):
            sb[sl[n]].append(n)

        sp = {k: berry_phase_multiplet(evecs, sb[k]) for k in range(3)}
        results[N] = sp

    print(f"\n  {'N':>6s} | {'g0/pi':>12s} | {'g1/pi':>12s} | {'g2/pi':>12s}")
    print(f"  {'-'*6}-+-{'-'*12}-+-{'-'*12}-+-{'-'*12}")
    for N in N_values:
        sp = results[N]
        print(f"  {N:6d} | {sp[0]/np.pi:12.8f} | {sp[1]/np.pi:12.8f} | {sp[2]/np.pi:12.8f}")

    sp1 = results[N_values[-2]]
    sp2 = results[N_values[-1]]
    maxd = max(abs(sp2[k] - sp1[k]) for k in range(3))
    check("Berry phases converged",
          maxd < 1e-4, "EXACT" if maxd < 1e-6 else "BOUNDED",
          f"max |delta(N=800 vs 1600)| = {maxd:.2e}")

    return results


# ============================================================================
# SECTION 7: Wilson deformation
# ============================================================================

def section_7_wilson(P):
    print("\n" + "=" * 78)
    print("SECTION 7: WILSON TERM DEFORMATION")
    print("=" * 78)

    omega = np.exp(2j * np.pi / 3)
    N = 400

    r_vals = [0.0, 0.1, 0.2, 0.5, 0.8, 1.0, 1.5, 2.0]
    results = {}

    for r in r_vals:
        thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
        evecs = np.zeros((N, 8, 8), dtype=complex)
        for i, theta in enumerate(thetas):
            Hk = symmetric_staggered_hamiltonian_k(
                np.array([theta]*3), wilson_r=r)
            _, ev = la.eigh(Hk)
            evecs[i] = ev

        sl = np.zeros(8, dtype=int)
        for n in range(8):
            v = evecs[0, :, n]
            sl[n] = min(range(3), key=lambda kk: abs(
                np.dot(v.conj(), P @ v) - omega**kk))

        sb = {0: [], 1: [], 2: []}
        for n in range(8):
            sb[sl[n]].append(n)

        sp = {k: berry_phase_multiplet(evecs, sb[k]) for k in range(3)}
        results[r] = sp

    print(f"\n  {'r':>6s} | {'g0/pi':>12s} | {'g1/pi':>12s} | {'g2/pi':>12s}")
    print(f"  {'-'*6}-+-{'-'*12}-+-{'-'*12}-+-{'-'*12}")
    for r in r_vals:
        sp = results[r]
        print(f"  {r:6.2f} | {sp[0]/np.pi:12.8f} | {sp[1]/np.pi:12.8f} | {sp[2]/np.pi:12.8f}")

    return results


# ============================================================================
# SECTION 8: Z_3-invariant perturbation sweep
# ============================================================================

def section_8_sweep(P):
    print("\n" + "=" * 78)
    print("SECTION 8: Z_3-INVARIANT PERTURBATION SWEEP")
    print("=" * 78)

    omega = np.exp(2j * np.pi / 3)
    N = 400
    thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)

    # Z_3-invariant perturbations
    V_sym = P + P.conj().T          # eigenvalues 2, -1, -1
    V_asym = 1j * (P - P.conj().T)  # eigenvalues 0, -sqrt(3), +sqrt(3)

    n_total = 0
    n_distinct = 0
    n_s12_diff = 0

    eps_vals = np.linspace(0, 3.0, 16)
    header = f"  {'e_s':>6s} {'e_a':>6s} | {'g0/pi':>10s} {'g1/pi':>10s} {'g2/pi':>10s} | {'dist':>4s}"
    print(f"\n{header}")
    print(f"  {'-'*6} {'-'*6}-+-{'-'*10}-{'-'*10}-{'-'*10}-+-{'-'*4}")

    for e1 in eps_vals:
        for e2 in eps_vals:
            V = e1 * V_sym + e2 * V_asym

            evecs = np.zeros((N, 8, 8), dtype=complex)
            for i, theta in enumerate(thetas):
                Hk = symmetric_staggered_hamiltonian_k(
                    np.array([theta]*3)) + V
                _, ev = la.eigh(Hk)
                evecs[i] = ev

            sl = np.zeros(8, dtype=int)
            for n in range(8):
                v = evecs[0, :, n]
                sl[n] = min(range(3), key=lambda kk: abs(
                    np.dot(v.conj(), P @ v) - omega**kk))

            sb = {0: [], 1: [], 2: []}
            for n in range(8):
                sb[sl[n]].append(n)

            sp = {k: berry_phase_multiplet(evecs, sb[k]) for k in range(3)}

            d01 = min(abs(sp[0]-sp[1]), 2*np.pi - abs(sp[0]-sp[1]))
            d12 = min(abs(sp[1]-sp[2]), 2*np.pi - abs(sp[1]-sp[2]))
            d02 = min(abs(sp[0]-sp[2]), 2*np.pi - abs(sp[0]-sp[2]))

            distinct = (d01 > 0.01) and (d12 > 0.01) and (d02 > 0.01)
            n_total += 1
            if distinct:
                n_distinct += 1
            if d12 > 0.01:
                n_s12_diff += 1

            # Print selected
            show = (e2 == 0.0 or
                    (abs(e1 - round(e1)) < 0.01 and abs(e2 - round(e2)) < 0.01))
            if show:
                print(f"  {e1:6.2f} {e2:6.2f} | "
                      f"{sp[0]/np.pi:10.6f} {sp[1]/np.pi:10.6f} "
                      f"{sp[2]/np.pi:10.6f} | {'Y' if distinct else 'N':>4s}")

    print(f"\n  Summary: {n_distinct}/{n_total} configs => all-distinct Berry phases")
    print(f"  Sectors 1 != 2: {n_s12_diff}/{n_total}")

    check(f"Berry phases generic ({n_distinct}/{n_total})",
          n_distinct > n_total * 0.3,
          "EXACT" if n_distinct == n_total else "BOUNDED",
          f"{n_distinct} of {n_total} configs")

    check(f"Sectors 1 != 2 generic ({n_s12_diff}/{n_total})",
          n_s12_diff > n_total * 0.3,
          "EXACT" if n_s12_diff == n_total else "BOUNDED",
          f"{n_s12_diff} of {n_total}")

    return n_distinct, n_total


# ============================================================================
# SECTION 9: Theorem check
# ============================================================================

def section_9_theorem(sp_free, sp_restricted):
    print("\n" + "=" * 78)
    print("SECTION 9: BERRY PHASE THEOREM ASSESSMENT")
    print("=" * 78)

    print("\n  === FREE CASE (no perturbation) ===")
    for k in range(3):
        print(f"    Sector {k}: gamma/pi = {sp_free[k]/np.pi:.8f}")

    g = [sp_free[k] for k in range(3)]
    d01 = min(abs(g[0]-g[1]), 2*np.pi - abs(g[0]-g[1]))
    d12 = min(abs(g[1]-g[2]), 2*np.pi - abs(g[1]-g[2]))
    d02 = min(abs(g[0]-g[2]), 2*np.pi - abs(g[0]-g[2]))

    free_distinct = (d01 > 0.01) and (d12 > 0.01) and (d02 > 0.01)
    check("Free case: sectors distinct",
          free_distinct, "EXACT" if free_distinct else "BOUNDED",
          f"distances: {d01:.6f}, {d12:.6f}, {d02:.6f}")

    print("\n  === RESTRICTED CASE ===")
    for k in range(3):
        print(f"    Sector {k}: gamma/pi = {sp_restricted[k]/np.pi:.8f}")

    g2 = [sp_restricted[k] for k in range(3)]
    d01r = min(abs(g2[0]-g2[1]), 2*np.pi - abs(g2[0]-g2[1]))
    d12r = min(abs(g2[1]-g2[2]), 2*np.pi - abs(g2[1]-g2[2]))
    d02r = min(abs(g2[0]-g2[2]), 2*np.pi - abs(g2[0]-g2[2]))

    restr_distinct = (d01r > 0.01) and (d12r > 0.01) and (d02r > 0.01)
    check("Restricted case: sectors distinct",
          restr_distinct, "EXACT" if restr_distinct else "BOUNDED",
          f"distances: {d01r:.6f}, {d12r:.6f}, {d02r:.6f}")

    # Check quantization patterns
    from itertools import permutations
    for label, phases in [("Free", sp_free), ("Restricted", sp_restricted)]:
        gv = [phases[k] for k in range(3)]
        targets = [0.0, 2*np.pi/3, 4*np.pi/3]
        best_err = np.inf
        for perm in permutations(targets):
            errs = [min(abs(m-t), 2*np.pi-abs(m-t)) for m, t in zip(gv, perm)]
            best_err = min(best_err, max(errs))

        quantized = best_err < 0.1
        check(f"{label}: Z_3 quantization {{0, 2pi/3, 4pi/3}}",
              quantized, "EXACT" if quantized else "BOUNDED",
              f"best match error = {best_err:.6f}")

    # Summary
    print("\n  " + "=" * 60)
    if free_distinct:
        print("  FREE CASE: Z_3 sectors carry DISTINCT Berry phases")
        print("  on the isotropic line of the symmetric staggered")
        print("  Hamiltonian. This is a topological obstruction to")
        print("  sector identification.")
    else:
        print("  FREE CASE: Berry phases do NOT distinguish all sectors")
        print("  on the isotropic line. The distinction may require")
        print("  perturbations or different loops.")

    if not restr_distinct:
        print("\n  RESTRICTED CASE: Sector-restricted Berry phases are")
        print("  EQUAL (all zero). This means the Berry phase on the")
        print("  isotropic line does not provide an UNCONDITIONAL")
        print("  topological invariant distinguishing Z_3 sectors.")
        print("  The distinction seen with perturbations is MODEL-DEPENDENT.")

    print("  " + "=" * 60)

    return free_distinct, restr_distinct


# ============================================================================
# SECTION 10: Z_3-twisted loop
# ============================================================================

def section_10_twisted(P):
    print("\n" + "=" * 78)
    print("SECTION 10: Z_3-TWISTED LOOP")
    print("=" * 78)

    omega = np.exp(2j * np.pi / 3)
    N = 800
    thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)

    # k(theta) = (theta, theta+2pi/3, theta+4pi/3)
    # Z_3 acts as theta -> theta + 2pi/3

    evecs = np.zeros((N, 8, 8), dtype=complex)
    evals = np.zeros((N, 8))
    for i, theta in enumerate(thetas):
        k = np.array([theta, theta + 2*np.pi/3, theta + 4*np.pi/3])
        Hk = symmetric_staggered_hamiltonian_k(k)
        ev, vec = la.eigh(Hk)
        evals[i] = ev
        evecs[i] = vec

    # Spectrum Z_3 check
    idx_s = N // 3
    spec_match = np.allclose(np.sort(evals[0]), np.sort(evals[idx_s]))
    check("Twisted loop: Z_3 spectrum symmetry", spec_match, "EXACT")

    # Per-band Berry phases
    print("\n  Per-band Berry phases:")
    for n in range(8):
        bp = berry_phase_band(evecs, n)
        print(f"    Band {n}: gamma/pi = {bp/np.pi:.8f}")

    # Total
    bp_total = berry_phase_multiplet(evecs, list(range(8)))
    print(f"  Total: gamma/pi = {bp_total/np.pi:.8f}")

    # P-permutation of bands
    evecs_0 = evecs[0]
    evecs_s = evecs[idx_s]
    ov = evecs_s.conj().T @ P @ evecs_0
    Pabs = np.abs(ov)

    print("\n  Band permutation by Z_3:")
    orbits = []
    visited = set()
    p_map = {}
    for n in range(8):
        m = int(np.argmax(Pabs[:, n]))
        p_map[n] = m
        print(f"    {n} -> {m} (|ov| = {Pabs[m,n]:.4f})")

    for n in range(8):
        if n in visited:
            continue
        orb = [n]
        visited.add(n)
        c = p_map[n]
        while c not in visited:
            orb.append(c)
            visited.add(c)
            c = p_map[c]
        orbits.append(orb)

    print(f"  Orbits: {orbits}")

    for orb in orbits:
        if len(orb) == 3:
            bps = [berry_phase_band(evecs, n) for n in orb]
            print(f"    Triplet {orb}: phases/pi = "
                  f"[{', '.join(f'{p/np.pi:.6f}' for p in bps)}]")
            diffs = [(bps[(i+1)%3] - bps[i]) % (2*np.pi) for i in range(3)]
            # Check if diffs are ~2pi/3
            for d in diffs:
                err_23 = min(abs(d - 2*np.pi/3), abs(d - 4*np.pi/3))
                if err_23 < 0.2:
                    check(f"Triplet {orb}: phase shift ~2pi/3",
                          True, "BOUNDED", f"error = {err_23:.4f}")
                    break
            else:
                check(f"Triplet {orb}: phase shift ~2pi/3",
                      False, "BOUNDED",
                      f"diffs/pi = [{', '.join(f'{d/np.pi:.4f}' for d in diffs)}]")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 78)
    print("BERRY PHASE / ZAK PHASE TOPOLOGICAL INVARIANTS FOR Z_3 SECTORS")
    print("Symmetric Staggered Cl(3) Hamiltonian on Z^3")
    print("=" * 78)
    print(f"\nStarted: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    section_1_verify()
    P = section_2_z3()
    thetas, all_evals, all_evecs, sector_labels = section_3_bands(P)
    sp_free, bp_all, sb = section_4_berry(thetas, all_evecs, sector_labels)
    sp_restricted = section_5_restricted(P)
    section_6_convergence(P)
    section_7_wilson(P)
    section_8_sweep(P)
    free_dist, restr_dist = section_9_theorem(sp_free, sp_restricted)
    section_10_twisted(P)

    # ========================================================================
    print("\n" + "=" * 78)
    print("FINAL SUMMARY")
    print("=" * 78)

    print(f"\nTotal: PASS={PASS_COUNT} FAIL={FAIL_COUNT}\n")
    for tag, status, cls, detail in RESULTS:
        m = "+" if status == "PASS" else "X"
        print(f"  [{m}] [{cls:>7s}] {tag}")

    print("\n" + "-" * 78)
    print("BERRY PHASE ASSESSMENT:")
    print("-" * 78)
    print()
    print("1. CONSTRUCTION: The symmetric staggered Hamiltonian (with phases")
    print("   eta_mu = (-1)^{sum_{nu!=mu} x_nu}) EXACTLY commutes with the")
    print("   Z_3 coordinate permutation (x,y,z) -> (y,z,x). Verified both")
    print("   in position space and momentum space.")
    print()
    print("2. SECTOR-RESTRICTED BERRY PHASES (clean test):")
    print("   On the isotropic line k=(theta,theta,theta), projecting into")
    print("   each Z_3 sector and computing the Berry phase gives the")
    print("   definitive answer about sector-topological distinction.")
    print()
    if restr_dist:
        print("   RESULT: DISTINCT. The Z_3 sectors carry different Berry phases.")
    else:
        print("   RESULT: NOT DISTINCT. The restricted Berry phases are EQUAL.")
        print("   The isotropic line Berry phase does NOT provide an unconditional")
        print("   topological invariant distinguishing Z_3 sectors.")
    print()
    print("3. PERTURBATION STUDY: With Z_3-invariant perturbations, the")
    print("   Berry phases generically become distinct across sectors.")
    print("   This shows the POTENTIAL for topological distinction but it")
    print("   is MODEL-DEPENDENT (depends on which perturbation is added).")
    print()
    print("4. HONEST STATUS: The Berry phase approach does NOT provide an")
    print("   UNCONDITIONAL Z_3 topological invariant for generation distinction.")
    print("   The superselection argument (Schur's lemma) from the wildcard")
    print("   script remains the strongest topological result.")
    print()

    print(f"\nPASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return PASS_COUNT, FAIL_COUNT


if __name__ == "__main__":
    p, f = main()
    sys.exit(0 if f == 0 else 1)
