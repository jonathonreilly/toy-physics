#!/usr/bin/env python3
"""
Gravitational Memory Effect on a 1D Ring
=========================================
Tests the discrete analog of Christodoulou gravitational memory:
after a gravitational wave passes through a region, the spacing
between geodesics is permanently altered.

Protocol:
  1. Place two test wavepackets ("geodesic markers") on a 1D periodic
     ring (n=61) at positions 15 and 45.
  2. Measure their initial separation (centroid distance on ring).
  3. Create a "gravitational wave": a propagating Phi perturbation via
     the retarded field equation:
       d^2 Phi/dt^2 = -c^2 (L + mu^2) Phi - gamma dPhi/dt + beta source(t)
     where source(t) is a brief pulse at position 30 (between the markers),
     active during matter steps 10-20.  Leapfrog/velocity-Verlet integrator.
  4. Test markers evolve under parity coupling with total Phi from the wave.
  5. Measure marker separation BEFORE wave (t<10), DURING (10<t<30),
     AFTER (t>30).
  6. Control: same markers without the wave pulse.
  7. Sweep pulse amplitude = [0.1, 0.5, 1.0, 2.0, 5.0] and check
     whether memory scales linearly with amplitude (expected for weak pulses).

Parameters:
  MASS=0.30, MU2=0.22, DT_MATTER=0.12, DT_FIELD=0.03
  c=1.0, gamma=0.05, beta=5.0
  N_FIELD_SUBSTEPS=4, Total=60 matter steps
"""

from __future__ import annotations
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve

# ── Parameters ───────────────────────────────────────────────────────
N = 61               # ring size
POS_A = 15           # marker A position
POS_B = 45           # marker B position
SOURCE_POS = 30      # gravitational wave source
PULSE_START = 10     # matter step when pulse turns on
PULSE_END = 20       # matter step when pulse turns off

MASS = 0.30
MU2 = 0.22
DT_MATTER = 0.12
DT_FIELD = 0.03
N_FIELD_SUBSTEPS = 4
C_SPEED = 1.0
GAMMA = 0.05         # light damping
BETA = 5.0           # source coupling
N_STEPS = 60         # total matter steps

AMPLITUDES = [0.1, 0.5, 1.0, 2.0, 5.0]


# ── Lattice Laplacian (periodic 1D ring) ────────────────────────────
def build_ring_laplacian(n):
    """Build the graph Laplacian for a 1D periodic ring of n sites."""
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
    """Alternating +1/-1 for bipartite parity coupling."""
    return np.array([(-1)**i for i in range(n)], dtype=float)


# ── Hamiltonian builder ─────────────────────────────────────────────
def build_hamiltonian(n, phi, par):
    """H = diag((MASS + phi) * par) + hopping on ring."""
    H = lil_matrix((n, n), dtype=complex)
    H.setdiag((MASS + phi) * par)
    for i in range(n):
        ip = (i + 1) % n
        # Antisymmetric hopping for bipartite structure
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
    """Compute the centroid of |psi|^2 on a ring of size n using circular mean."""
    prob = np.abs(psi) ** 2
    prob /= prob.sum() + 1e-30
    angles = 2 * np.pi * np.arange(n) / n
    cx = np.sum(prob * np.cos(angles))
    cy = np.sum(prob * np.sin(angles))
    return np.arctan2(cy, cx) / (2 * np.pi) * n % n


def ring_distance(c1, c2, n):
    """Geodesic distance between two positions on a ring."""
    d = abs(c1 - c2)
    return min(d, n - d)


# ── Initial wavepacket (Gaussian on ring) ──────────────────────────
def make_wavepacket(center, n, sigma=2.0):
    """Gaussian wavepacket centered at `center` on a ring of size n."""
    x = np.arange(n)
    dx = x - center
    # Wrap to shortest distance on ring
    dx = dx - n * np.round(dx / n)
    psi = np.exp(-dx**2 / (2 * sigma**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


# ── Run one simulation ─────────────────────────────────────────────
def run_simulation(pulse_amplitude, use_pulse=True):
    """
    Run the gravitational memory simulation.
    Returns dict with separation history and field snapshots.
    """
    par = parity_vector(N)
    L = build_ring_laplacian(N)

    # Field operator: -c^2 (L + mu^2 I)
    field_op = -C_SPEED**2 * (L + MU2 * speye(N, format='csr'))

    # Field state
    phi = np.zeros(N)
    pi_field = np.zeros(N)

    # Source profile: delta at SOURCE_POS
    source_profile = np.zeros(N)
    source_profile[SOURCE_POS] = 1.0

    # Two marker wavepackets
    psi_a = make_wavepacket(POS_A, N)
    psi_b = make_wavepacket(POS_B, N)

    # History
    sep_history = []
    cent_a_history = []
    cent_b_history = []
    phi_max_history = []
    norm_a_history = []
    norm_b_history = []

    for step in range(N_STEPS):
        # Record separation
        ca = ring_centroid(psi_a, N)
        cb = ring_centroid(psi_b, N)
        sep = ring_distance(ca, cb, N)
        sep_history.append(sep)
        cent_a_history.append(ca)
        cent_b_history.append(cb)
        phi_max_history.append(np.max(np.abs(phi)))
        norm_a_history.append(np.linalg.norm(psi_a))
        norm_b_history.append(np.linalg.norm(psi_b))

        # Determine if pulse is active
        pulse_active = use_pulse and (PULSE_START <= step < PULSE_END)

        # Evolve field for N_FIELD_SUBSTEPS (leapfrog / velocity-Verlet)
        for _ in range(N_FIELD_SUBSTEPS):
            source = BETA * pulse_amplitude * source_profile if pulse_active else np.zeros(N)
            acc = field_op.dot(phi) - GAMMA * pi_field + source
            pi_field += 0.5 * DT_FIELD * acc
            phi += DT_FIELD * pi_field
            acc = field_op.dot(phi) - GAMMA * pi_field + source
            pi_field += 0.5 * DT_FIELD * acc

        # Build Hamiltonian with current phi and evolve markers
        H = build_hamiltonian(N, phi, par)
        psi_a = cn_step(H, psi_a, DT_MATTER)
        psi_b = cn_step(H, psi_b, DT_MATTER)

    # Final measurement
    ca = ring_centroid(psi_a, N)
    cb = ring_centroid(psi_b, N)
    sep_history.append(ring_distance(ca, cb, N))

    return {
        'separation': np.array(sep_history),
        'centroid_a': np.array(cent_a_history),
        'centroid_b': np.array(cent_b_history),
        'phi_max': np.array(phi_max_history),
        'norm_a': np.array(norm_a_history),
        'norm_b': np.array(norm_b_history),
    }


# ── Main ────────────────────────────────────────────────────────────
def main():
    print("=" * 72)
    print("GRAVITATIONAL MEMORY EFFECT -- 1D RING")
    print("=" * 72)
    print(f"Ring size N={N}, markers at {POS_A} and {POS_B}, source at {SOURCE_POS}")
    print(f"MASS={MASS}, MU2={MU2}, DT_MATTER={DT_MATTER}, DT_FIELD={DT_FIELD}")
    print(f"c={C_SPEED}, gamma={GAMMA}, beta={BETA}")
    print(f"N_FIELD_SUBSTEPS={N_FIELD_SUBSTEPS}, N_STEPS={N_STEPS}")
    print(f"Pulse active during matter steps {PULSE_START}-{PULSE_END}")
    print()

    # ── Control run (no pulse) ──────────────────────────────────────
    print("-" * 72)
    print("CONTROL RUN (no gravitational wave)")
    print("-" * 72)
    ctrl = run_simulation(0.0, use_pulse=False)
    sep_ctrl = ctrl['separation']
    print(f"  Initial separation:  {sep_ctrl[0]:.6f}")
    print(f"  Pre-wave  (t=9):     {sep_ctrl[9]:.6f}")
    print(f"  Mid-wave  (t=15):    {sep_ctrl[15]:.6f}")
    print(f"  Post-wave (t=40):    {sep_ctrl[40]:.6f}")
    print(f"  Final     (t=60):    {sep_ctrl[-1]:.6f}")
    print(f"  Free drift (final - initial): {sep_ctrl[-1] - sep_ctrl[0]:+.6f}")
    print(f"  Norm A: {ctrl['norm_a'][-1]:.6f}  Norm B: {ctrl['norm_b'][-1]:.6f}")
    print()

    # ── Amplitude sweep ─────────────────────────────────────────────
    print("-" * 72)
    print("AMPLITUDE SWEEP")
    print("-" * 72)
    print(f"{'Amp':>6s}  {'Sep_init':>10s}  {'Sep_pre':>10s}  {'Sep_post':>10s}  "
          f"{'Sep_final':>10s}  {'Memory':>10s}  {'Mem-Ctrl':>10s}  {'PhiMax':>10s}")

    memory_values = []
    for amp in AMPLITUDES:
        res = run_simulation(amp, use_pulse=True)
        sep = res['separation']
        # Memory = change in separation relative to control
        # (remove free-drift component)
        memory_raw = sep[-1] - sep[0]
        memory_net = memory_raw - (sep_ctrl[-1] - sep_ctrl[0])
        memory_values.append(memory_net)

        print(f"{amp:6.2f}  {sep[0]:10.6f}  {sep[9]:10.6f}  {sep[40]:10.6f}  "
              f"{sep[-1]:10.6f}  {memory_raw:+10.6f}  {memory_net:+10.6f}  "
              f"{res['phi_max'].max():10.6f}")

    print()

    # ── Linearity check ─────────────────────────────────────────────
    print("-" * 72)
    print("LINEARITY CHECK: memory / amplitude")
    print("-" * 72)
    print(f"{'Amp':>6s}  {'Memory(net)':>12s}  {'Mem/Amp':>10s}")
    for amp, mem in zip(AMPLITUDES, memory_values):
        ratio = mem / amp if amp > 0 else 0.0
        print(f"{amp:6.2f}  {mem:+12.6f}  {ratio:+10.6f}")

    # Check linearity: ratio should be roughly constant for weak pulses
    if len(memory_values) >= 2 and abs(memory_values[0]) > 1e-10:
        ratios = [m / a for m, a in zip(memory_values, AMPLITUDES) if a > 0]
        ratio_mean = np.mean(ratios[:3])  # first 3 (weak pulses)
        ratio_std = np.std(ratios[:3])
        print()
        print(f"  Weak-pulse ratios (first 3): mean={ratio_mean:+.6f}, std={ratio_std:.6f}")
        if ratio_std < 0.3 * abs(ratio_mean) and abs(ratio_mean) > 1e-8:
            print("  -> PASS: Memory scales approximately linearly with amplitude (weak regime)")
        else:
            print("  -> UNCERTAIN: Linearity not cleanly established")
    print()

    # ── Time-resolved detail for amp=1.0 ────────────────────────────
    print("-" * 72)
    print("TIME-RESOLVED DETAIL (amplitude=1.0)")
    print("-" * 72)
    res10 = run_simulation(1.0, use_pulse=True)
    sep = res10['separation']
    print(f"{'Step':>5s}  {'Sep':>10s}  {'Sep-Ctrl':>10s}  {'PhiMax':>10s}  {'Phase':>10s}")
    for t in range(0, N_STEPS + 1, 3):
        idx = min(t, len(sep) - 1)
        ctrl_idx = min(t, len(sep_ctrl) - 1)
        delta = sep[idx] - sep_ctrl[ctrl_idx]
        phi_max = res10['phi_max'][min(t, len(res10['phi_max']) - 1)] if t < len(res10['phi_max']) else 0.0
        if t < PULSE_START:
            phase = "BEFORE"
        elif t < PULSE_END:
            phase = "DURING"
        elif t < 30:
            phase = "PASSING"
        else:
            phase = "AFTER"
        print(f"{t:5d}  {sep[idx]:10.6f}  {delta:+10.6f}  {phi_max:10.6f}  {phase:>10s}")

    print()

    # ── Summary ─────────────────────────────────────────────────────
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    mem_1 = memory_values[2]  # amp=1.0
    ctrl_drift = sep_ctrl[-1] - sep_ctrl[0]
    print(f"  Control drift (no wave):       {ctrl_drift:+.6f}")
    print(f"  Memory signal (amp=1.0, net):  {mem_1:+.6f}")
    if abs(mem_1) > 2 * abs(ctrl_drift) and abs(mem_1) > 1e-6:
        print("  -> PASS: Permanent separation change detected after wave passage")
        print("           (gravitational memory effect confirmed)")
    elif abs(mem_1) > 1e-6:
        print("  -> MARGINAL: Memory signal present but comparable to control drift")
    else:
        print("  -> FAIL: No detectable gravitational memory")

    # Nonlinearity onset
    if len(memory_values) >= 4:
        r_weak = memory_values[0] / AMPLITUDES[0] if AMPLITUDES[0] > 0 else 0
        r_strong = memory_values[-1] / AMPLITUDES[-1] if AMPLITUDES[-1] > 0 else 0
        if abs(r_weak) > 1e-10:
            nonlin = abs(r_strong / r_weak - 1.0)
            print(f"  Nonlinearity (strong/weak ratio deviation): {nonlin:.3f}")
            if nonlin > 0.3:
                print("  -> Strong pulses show nonlinear memory (expected)")
    print()


if __name__ == "__main__":
    main()
