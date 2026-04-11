#!/usr/bin/env python3
"""
Gravitational Memory -- Unscreened Recheck
==========================================
Same protocol as frontier_gravitational_memory.py but sweeps ring size N
with TWO mass-gap values:
  - MU2 = 0.22  (screening length ~2.13, original -- memory killed at large N)
  - MU2 = 0.001 (screening length ~31.6, effectively unscreened on these rings)

Key question: does the memory signal PERSIST at N=101,121 when screening
is removed?

Protocol:
  1D periodic staggered ring, markers at n/4 and 3n/4, pulse at n/2.
  Retarded wave: d^2 Phi/dt^2 = -c^2 (L + mu^2) Phi - gamma dPhi/dt + beta source
  Pulse amplitude = 1.0, active for 10 steps.
  c=1.0, gamma=0.05, beta=5.0
  DT_MATTER=0.12, DT_FIELD=0.03, 4 field substeps, 60 matter steps.
"""

from __future__ import annotations
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve

# ── Fixed parameters ────────────────────────────────────────────────
MASS = 0.30
DT_MATTER = 0.12
DT_FIELD = 0.03
N_FIELD_SUBSTEPS = 4
C_SPEED = 1.0
GAMMA = 0.05
BETA = 5.0
N_STEPS = 60
PULSE_AMPLITUDE = 1.0
PULSE_DURATION = 10       # active for 10 matter steps starting at step 10

RING_SIZES = [41, 61, 81, 101, 121]
MU2_VALUES = [0.001, 0.22]

def steps_for_ring(n):
    """Enough steps for wave to reach markers and memory to settle.
    Wave speed c=1, field time per matter step = N_FIELD_SUBSTEPS * DT_FIELD = 0.12.
    Source-to-marker distance = n//4.  Need ~2x travel time for memory to settle."""
    dist = n // 4
    travel_steps = int(np.ceil(dist / (N_FIELD_SUBSTEPS * DT_FIELD)))
    # 2x for arrival + settling, minimum 60
    return max(60, int(travel_steps * 2.5))


# ── Lattice Laplacian (periodic 1D ring) ────────────────────────────
def build_ring_laplacian(n):
    L = lil_matrix((n, n), dtype=float)
    for i in range(n):
        ip = (i + 1) % n
        im = (i - 1) % n
        L[i, i] += 2.0
        L[i, ip] -= 1.0
        L[i, im] -= 1.0
    return L.tocsr()


# ── Parity vector ───────────────────────────────────────────────────
def parity_vector(n):
    return np.array([(-1)**i for i in range(n)], dtype=float)


# ── Hamiltonian builder ─────────────────────────────────────────────
def build_hamiltonian(n, phi, par):
    H = lil_matrix((n, n), dtype=complex)
    H.setdiag((MASS + phi) * par)
    for i in range(n):
        ip = (i + 1) % n
        H[i, ip] += -0.5j
        H[ip, i] += 0.5j
    return H.tocsr()


# ── Crank-Nicolson step ────────────────────────────────────────────
def cn_step(H, psi, dt):
    n = H.shape[0]
    I = speye(n, format='csc')
    ap = (I + 1j * H * dt / 2).tocsc()
    am = I - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


# ── Centroid on ring ────────────────────────────────────────────────
def ring_centroid(psi, n):
    prob = np.abs(psi) ** 2
    prob /= prob.sum() + 1e-30
    angles = 2 * np.pi * np.arange(n) / n
    cx = np.sum(prob * np.cos(angles))
    cy = np.sum(prob * np.sin(angles))
    return np.arctan2(cy, cx) / (2 * np.pi) * n % n


def ring_distance(c1, c2, n):
    d = abs(c1 - c2)
    return min(d, n - d)


# ── Initial wavepacket ──────────────────────────────────────────────
def make_wavepacket(center, n, sigma=2.0):
    x = np.arange(n)
    dx = x - center
    dx = dx - n * np.round(dx / n)
    psi = np.exp(-dx**2 / (2 * sigma**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


# ── Run one simulation ──────────────────────────────────────────────
def run_simulation(n, mu2, n_steps=None, use_pulse=True):
    if n_steps is None:
        n_steps = steps_for_ring(n)

    pos_a = n // 4
    pos_b = 3 * n // 4
    source_pos = n // 2
    pulse_start = 10
    pulse_end = pulse_start + PULSE_DURATION

    par = parity_vector(n)
    L = build_ring_laplacian(n)
    field_op = -C_SPEED**2 * (L + mu2 * speye(n, format='csr'))

    phi = np.zeros(n)
    pi_field = np.zeros(n)

    source_profile = np.zeros(n)
    source_profile[source_pos] = 1.0

    psi_a = make_wavepacket(pos_a, n)
    psi_b = make_wavepacket(pos_b, n)

    sep_history = []

    for step in range(n_steps):
        ca = ring_centroid(psi_a, n)
        cb = ring_centroid(psi_b, n)
        sep_history.append(ring_distance(ca, cb, n))

        pulse_active = use_pulse and (pulse_start <= step < pulse_end)

        for _ in range(N_FIELD_SUBSTEPS):
            source = BETA * PULSE_AMPLITUDE * source_profile if pulse_active else np.zeros(n)
            acc = field_op.dot(phi) - GAMMA * pi_field + source
            pi_field += 0.5 * DT_FIELD * acc
            phi += DT_FIELD * pi_field
            acc = field_op.dot(phi) - GAMMA * pi_field + source
            pi_field += 0.5 * DT_FIELD * acc

        H = build_hamiltonian(n, phi, par)
        psi_a = cn_step(H, psi_a, DT_MATTER)
        psi_b = cn_step(H, psi_b, DT_MATTER)

    ca = ring_centroid(psi_a, n)
    cb = ring_centroid(psi_b, n)
    sep_history.append(ring_distance(ca, cb, n))

    phi_at_markers = 0.5 * (abs(phi[pos_a]) + abs(phi[pos_b]))

    return {
        'separation': np.array(sep_history),
        'phi_at_markers': phi_at_markers,
        'phi_max': np.max(np.abs(phi)),
        'n_steps': n_steps,
    }


# ── Main ────────────────────────────────────────────────────────────
def main():
    print("=" * 80)
    print("GRAVITATIONAL MEMORY -- UNSCREENED RECHECK")
    print("=" * 80)
    print(f"Parameters: MASS={MASS}, c={C_SPEED}, gamma={GAMMA}, beta={BETA}")
    print(f"  DT_MATTER={DT_MATTER}, DT_FIELD={DT_FIELD}, substeps={N_FIELD_SUBSTEPS}")
    print(f"  Pulse amplitude={PULSE_AMPLITUDE}, duration={PULSE_DURATION} steps (steps 10-19)")
    print(f"  Ring sizes: {RING_SIZES}")
    steps_per_ring = {n: steps_for_ring(n) for n in RING_SIZES}
    print(f"  Steps per ring: {steps_per_ring}")
    print(f"  mu^2 values: {MU2_VALUES}")
    screening_lengths = [1.0 / np.sqrt(mu2) for mu2 in MU2_VALUES]
    print(f"  Screening lengths: {['%.1f' % sl for sl in screening_lengths]}")
    print()

    # ── Control runs (no pulse) ─────────────────────────────────────
    print("-" * 80)
    print("CONTROL RUNS (no pulse)")
    print("-" * 80)
    print(f"{'N':>5s}  {'Steps':>6s}  {'mu2':>8s}  {'Sep_init':>10s}  {'Sep_final':>10s}  {'Drift':>10s}")
    ctrl_drift = {}
    for n in RING_SIZES:
        ns = steps_per_ring[n]
        for mu2 in MU2_VALUES:
            res = run_simulation(n, mu2, n_steps=ns, use_pulse=False)
            sep = res['separation']
            drift = sep[-1] - sep[0]
            ctrl_drift[(n, mu2)] = drift
            print(f"{n:5d}  {ns:6d}  {mu2:8.3f}  {sep[0]:10.6f}  {sep[-1]:10.6f}  {drift:+10.6f}")
    print()

    # ── Memory runs ─────────────────────────────────────────────────
    print("-" * 80)
    print("MEMORY SIGNAL vs RING SIZE")
    print("-" * 80)
    print(f"{'N':>5s}  {'Steps':>6s}  {'mu2':>8s}  {'screen_L':>10s}  {'Sep_init':>10s}  "
          f"{'Sep_final':>10s}  {'Raw_mem':>10s}  {'Net_mem':>10s}  "
          f"{'PhiMax':>10s}  {'Phi@mark':>10s}")

    results = {}
    for n in RING_SIZES:
        ns = steps_per_ring[n]
        for mu2 in MU2_VALUES:
            sl = 1.0 / np.sqrt(mu2)
            res = run_simulation(n, mu2, n_steps=ns, use_pulse=True)
            sep = res['separation']
            raw_mem = sep[-1] - sep[0]
            net_mem = raw_mem - ctrl_drift[(n, mu2)]
            results[(n, mu2)] = net_mem
            print(f"{n:5d}  {ns:6d}  {mu2:8.3f}  {sl:10.1f}  {sep[0]:10.6f}  "
                  f"{sep[-1]:10.6f}  {raw_mem:+10.6f}  {net_mem:+10.6f}  "
                  f"{res['phi_max']:10.6f}  {res['phi_at_markers']:10.6f}")
    print()

    # ── Comparison table ────────────────────────────────────────────
    print("-" * 80)
    print("COMPARISON: Net memory signal")
    print("-" * 80)
    print(f"{'N':>5s}  {'mu2=0.001':>14s}  {'mu2=0.22':>14s}  {'Ratio':>10s}  {'Verdict':>20s}")
    for n in RING_SIZES:
        m_low = results[(n, 0.001)]
        m_high = results[(n, 0.22)]
        if abs(m_high) > 1e-10:
            ratio = m_low / m_high
            ratio_str = f"{ratio:10.2f}"
        else:
            ratio_str = "  inf/undef"
        # Verdict
        if abs(m_low) > 1e-4:
            verdict = "MEMORY SURVIVES"
        elif abs(m_low) > 1e-6:
            verdict = "weak signal"
        else:
            verdict = "NO MEMORY"
        print(f"{n:5d}  {m_low:+14.6f}  {m_high:+14.6f}  {ratio_str}  {verdict:>20s}")
    print()

    # ── Scaling analysis ────────────────────────────────────────────
    print("-" * 80)
    print("SCALING: |memory| vs N")
    print("-" * 80)
    print(f"{'N':>5s}  {'|mem| mu2=0.001':>18s}  {'|mem| mu2=0.22':>18s}")
    for n in RING_SIZES:
        m_low = abs(results[(n, 0.001)])
        m_high = abs(results[(n, 0.22)])
        bar_low = "#" * int(min(m_low * 500, 50))
        bar_high = "#" * int(min(m_high * 500, 50))
        print(f"{n:5d}  {m_low:18.8f}  {bar_low}")
        print(f"{'':5s}  {m_high:18.8f}  {bar_high}")
    print()

    # ── Summary ─────────────────────────────────────────────────────
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    # Check if unscreened memory survives at large N
    large_n_survive = all(abs(results[(n, 0.001)]) > 1e-4 for n in [101, 121])
    large_n_screened = all(abs(results[(n, 0.22)]) < 1e-4 for n in [101, 121])

    if large_n_survive and large_n_screened:
        print("  CONFIRMED: Yukawa screening (mu2=0.22) kills memory at large N,")
        print("             but unscreened (mu2=0.001) memory SURVIVES at N=101,121.")
        print("  -> Gravitational memory is a real wave-propagation effect,")
        print("     not an artifact of small ring size.")
    elif large_n_survive:
        print("  Memory survives at large N for mu2=0.001.")
        if not large_n_screened:
            print("  NOTE: Screened case also shows memory -- screening may be partial.")
    else:
        print("  WARNING: Memory does NOT survive at large N even with mu2=0.001.")
        print("  Possible explanations:")
        print("    - Damping (gamma=0.05) kills signal before arrival")
        print("    - Wavepacket dispersion destroys markers at long evolution times")
        print("    - Need different parameters")

    # Check signal at each N for unscreened
    print()
    print("  Per-N results (mu2=0.001):")
    for n in RING_SIZES:
        ns = steps_per_ring[n]
        m = results[(n, 0.001)]
        status = "OK" if abs(m) > 1e-4 else ("weak" if abs(m) > 1e-6 else "ZERO")
        travel = n // 4
        total_field_time = ns * N_FIELD_SUBSTEPS * DT_FIELD
        print(f"    N={n:3d}: net_mem={m:+.6f}  [{status}]  "
              f"dist={travel}, steps={ns}, field_time={total_field_time:.1f}")
    print()


if __name__ == "__main__":
    main()
