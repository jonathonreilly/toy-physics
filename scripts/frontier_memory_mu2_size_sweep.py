#!/usr/bin/env python3
"""
Memory screening sweep versus mu^2 and lattice size.

Goal:
  Test whether the retained 1D memory signal survives once the screening
  length exceeds the source-marker distance, and whether the effect persists
  on larger rings.

Protocol:
  - keep the retained ring geometry logic from frontier_gravitational_memory.py
  - sweep mu^2 downward, including the massless limit
  - sweep ring size upward
  - keep the source/marker geometry in the same relative positions
  - report control drift, memory shift, and screening length

This is a diagnostic script, not a publication claim.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve


MASS = 0.30
DT_MATTER = 0.12
DT_FIELD = 0.03
N_FIELD_SUBSTEPS = 4
C_SPEED = 1.0
GAMMA = 0.05
BETA = 5.0
PULSE_AMP = 1.0

N_SIZES = (61, 81, 101, 121)
MU2_VALUES = (0.22, 0.10, 0.05, 0.01, 0.005, 0.001, 0.0)


def build_ring_laplacian(n: int):
    L = lil_matrix((n, n), dtype=float)
    for i in range(n):
        ip = (i + 1) % n
        im = (i - 1) % n
        L[i, i] += 2.0
        L[i, ip] -= 1.0
        L[i, im] -= 1.0
    return L.tocsr()


def parity_vector(n: int):
    return np.array([(-1) ** i for i in range(n)], dtype=float)


def build_ring_hamiltonian(n: int, phi, par):
    H = lil_matrix((n, n), dtype=complex)
    H.setdiag((MASS + phi) * par)
    for i in range(n):
        ip = (i + 1) % n
        H[i, ip] += -0.5j
        H[ip, i] += 0.5j
    return H.tocsr()


def cn_step(H, psi, dt):
    n = H.shape[0]
    I = speye(n, format="csc")
    ap = (I + 1j * H * dt / 2).tocsc()
    am = I - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


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


def make_wavepacket(center, n, sigma=2.0):
    x = np.arange(n)
    dx = x - center
    dx = dx - n * np.round(dx / n)
    psi = np.exp(-dx**2 / (2 * sigma**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


def run_memory_sim(
    n: int,
    mu2: float,
    pulse_amplitude: float = PULSE_AMP,
    pos_a: int | None = None,
    pos_b: int | None = None,
    source_pos: int | None = None,
):
    steps = max(60, n)
    pulse_start = steps // 6
    pulse_end = pulse_start + max(1, steps // 6)

    par = parity_vector(n)
    L = build_ring_laplacian(n)
    field_op = -C_SPEED**2 * (L + mu2 * speye(n, format="csr"))

    phi = np.zeros(n)
    pi_field = np.zeros(n)

    source_pos = n // 2 if source_pos is None else source_pos
    pos_a = n // 4 if pos_a is None else pos_a
    pos_b = 3 * n // 4 if pos_b is None else pos_b
    source_profile = np.zeros(n)
    source_profile[source_pos] = 1.0

    psi_a = make_wavepacket(pos_a, n)
    psi_b = make_wavepacket(pos_b, n)

    sep_history = []
    for step in range(steps):
        ca = ring_centroid(psi_a, n)
        cb = ring_centroid(psi_b, n)
        sep_history.append(ring_distance(ca, cb, n))

        pulse_active = pulse_start <= step < pulse_end
        for _ in range(N_FIELD_SUBSTEPS):
            source = BETA * pulse_amplitude * source_profile if pulse_active else np.zeros(n)
            acc = field_op.dot(phi) - GAMMA * pi_field + source
            pi_field += 0.5 * DT_FIELD * acc
            phi += DT_FIELD * pi_field
            acc = field_op.dot(phi) - GAMMA * pi_field + source
            pi_field += 0.5 * DT_FIELD * acc

        H = build_ring_hamiltonian(n, phi, par)
        psi_a = cn_step(H, psi_a, DT_MATTER)
        psi_b = cn_step(H, psi_b, DT_MATTER)

    ca = ring_centroid(psi_a, n)
    cb = ring_centroid(psi_b, n)
    sep_history.append(ring_distance(ca, cb, n))

    return {
        "steps": steps,
        "pulse_start": pulse_start,
        "pulse_end": pulse_end,
        "source_pos": source_pos,
        "pos_a": pos_a,
        "pos_b": pos_b,
        "separation": np.array(sep_history),
    }


def main():
    print("=" * 88)
    print("GRAVITATIONAL MEMORY MU2 / SIZE SWEEP")
    print("=" * 88)
    print("Retained ring protocol with downward mu^2 scan")
    print(f"MASS={MASS}, DT_MATTER={DT_MATTER}, DT_FIELD={DT_FIELD}, GAMMA={GAMMA}, BETA={BETA}")
    print(f"N_SIZES={N_SIZES}")
    print(f"MU2_VALUES={MU2_VALUES}")
    print()

    print(f"{'N':>5s}  {'mu2':>8s}  {'ell_screen':>10s}  {'d_src':>7s}  {'ctrl':>10s}  {'memory':>10s}  {'memory/amp':>11s}")
    rows = []
    for n in N_SIZES:
        d_src = n // 4
        ctrl = run_memory_sim(n, MU2_VALUES[0], pulse_amplitude=0.0)
        ctrl_drift = ctrl["separation"][-1] - ctrl["separation"][0]
        for mu2 in MU2_VALUES:
            res = run_memory_sim(n, mu2, pulse_amplitude=PULSE_AMP)
            sep = res["separation"]
            raw = sep[-1] - sep[0]
            net = raw - ctrl_drift
            ell_screen = math.inf if mu2 == 0.0 else 1.0 / math.sqrt(mu2)
            rows.append((n, mu2, ell_screen, d_src, ctrl_drift, net))
            print(
                f"{n:5d}  {mu2:8.3g}  "
                f"{ell_screen:10.3f}  {d_src:7d}  "
                f"{ctrl_drift:+10.6f}  {net:+10.6f}  {net / PULSE_AMP:+11.6f}"
            )

    print()
    print("Fixed-geometry slice: posA=15, posB=45, source=30")
    print("This keeps the marker separation constant while N grows.")
    print(f"{'N':>5s}  {'mu2':>8s}  {'ell_screen':>10s}  {'d_src':>7s}  {'ctrl':>10s}  {'memory':>10s}")
    for n in N_SIZES:
        if n < 61:
            continue
        pos_a = 15
        pos_b = 45
        source_pos = 30
        d_src = min(abs(source_pos - pos_a), n - abs(source_pos - pos_a))
        ctrl = run_memory_sim(
            n,
            MU2_VALUES[0],
            pulse_amplitude=0.0,
            pos_a=pos_a,
            pos_b=pos_b,
            source_pos=source_pos,
        )
        ctrl_drift = ctrl["separation"][-1] - ctrl["separation"][0]
        for mu2 in MU2_VALUES:
            res = run_memory_sim(
                n,
                mu2,
                pulse_amplitude=PULSE_AMP,
                pos_a=pos_a,
                pos_b=pos_b,
                source_pos=source_pos,
            )
            sep = res["separation"]
            raw = sep[-1] - sep[0]
            net = raw - ctrl_drift
            ell_screen = math.inf if mu2 == 0.0 else 1.0 / math.sqrt(mu2)
            print(
                f"{n:5d}  {mu2:8.3g}  "
                f"{ell_screen:10.3f}  {d_src:7d}  "
                f"{ctrl_drift:+10.6f}  {net:+10.6f}"
            )

    print()
    print("Threshold check: ell_screen > d_src")
    for n, mu2, ell_screen, d_src, ctrl_drift, net in rows:
        if ell_screen == math.inf:
            okay = True
        else:
            okay = ell_screen > d_src
        if okay:
            print(
                f"  N={n:3d} mu2={mu2:8.3g} ell={ell_screen:8.3f} > d_src={d_src:2d} "
                f"memory={net:+.6f}"
            )


if __name__ == "__main__":
    main()
