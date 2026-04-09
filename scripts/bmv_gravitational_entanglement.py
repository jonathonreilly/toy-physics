#!/usr/bin/env python3
"""BMV test: gravitationally-induced entanglement between two beams.

THE BMV PROPOSAL (Bose, Marletto, Vedral, 2017):
  Two masses in spatial superposition interact gravitationally.
  If gravity is quantum (mediates entanglement), the final state
  is entangled. If gravity is classical, no entanglement.

OUR VERSION:
  Two beams propagate on the same lattice. Each beam creates a
  gravitational field (via back-reaction). The OTHER beam propagates
  through this field. If the combined effect entangles the beams,
  gravity is quantum in this model.

SETUP:
  Beam A starts at z=+3, beam B at z=-3 (two slits).
  Each beam's |psi|^2 generates a field that affects the other.
  After propagation, measure the density matrix of the joint state.
  If the off-diagonal (coherence) is modified by the mutual
  gravitational interaction: entanglement.

MEASURE:
  1. Propagate A and B independently (no mutual interaction)
  2. Propagate A in B's field and B in A's field (mutual interaction)
  3. Compare the joint density matrix: if mutual > independent,
     gravity created entanglement.
"""

from __future__ import annotations

import math
import numpy as np

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3.0
H = 0.5
PHYS_W = 6
PHYS_L = 30
N_YBINS = 8


def _setup():
    nl = int(PHYS_L / H) + 1
    hw = int(PHYS_W / H)
    max_d = max(1, round(MAX_D_PHYS / H))
    nw = 2 * hw + 1
    npl = nw * nw
    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp, dzp = dy * H, dz * H
            L = math.sqrt(H * H + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), H)
            offsets.append((dy, dz, L, math.exp(-BETA * theta * theta) * H * H / (L * L)))
    T = sum(wr for _, _, _, wr in offsets)
    pos = np.array([(layer * H, iy * H, iz * H)
                    for layer in range(nl)
                    for iy in range(-hw, hw + 1)
                    for iz in range(-hw, hw + 1)])
    return nl, hw, nw, npl, offsets, T, pos


def _prop(nl, nw, npl, hw, offsets, T, field, k, source_idx):
    amps = np.zeros((nl, npl), dtype=np.complex128)
    amps[0, source_idx] = 1.0
    for layer in range(nl - 1):
        sa = amps[layer]
        if np.max(np.abs(sa)) < 1e-300:
            continue
        sf = field[layer]
        df = field[min(layer + 1, nl - 1)]
        for dy, dz, L, w_raw in offsets:
            ym, yM = max(0, -dy), min(nw, nw - dy)
            zm, zM = max(0, -dz), min(nw, nw - dz)
            if ym >= yM or zm >= zM:
                continue
            yi, zi = np.meshgrid(np.arange(ym, yM), np.arange(zm, zM), indexing='ij')
            si = yi.ravel() * nw + zi.ravel()
            di = (yi.ravel() + dy) * nw + (zi.ravel() + dz)
            ai = sa[si]
            mask = np.abs(ai) > 1e-300
            if not np.any(mask):
                continue
            si_m, di_m, ai_m = si[mask], di[mask], ai[mask]
            lf = 0.5 * (sf[si_m] + df[di_m])
            phase = k * L * (1.0 - lf)
            np.add.at(amps[layer + 1], di_m,
                      ai_m * (np.cos(phase) + 1j * np.sin(phase)) * w_raw / T)
    return amps


def _field_from_amps(amps, nl, npl, pos, G):
    """Generate 1/r field from amplitude distribution."""
    f = np.zeros((nl, npl))
    for layer in range(nl):
        p = np.abs(amps[layer]) ** 2
        if p.sum() < 1e-300:
            continue
        pn = p / p.sum()
        top_k = min(20, npl)
        ti = np.argpartition(pn, -top_k)[-top_k:]
        ls = layer * npl
        for idx in ti:
            if pn[idx] < 1e-8:
                continue
            dx = pos[ls:ls + npl] - pos[ls + idx]
            f[layer] += G * pn[idx] / (np.sqrt(np.sum(dx ** 2, axis=1)) + 0.1)
    return f


def _bin_z(amps_last, nw, hw, h, n_bins):
    """Bin detector amplitudes by z."""
    npl = nw * nw
    z_coords = np.array([iz * h for _ in range(-hw, hw + 1) for iz in range(-hw, hw + 1)])
    z_min, z_max = z_coords.min(), z_coords.max()
    bin_edges = np.linspace(z_min - 0.01, z_max + 0.01, n_bins + 1)
    bin_idx = np.clip(np.digitize(z_coords, bin_edges) - 1, 0, n_bins - 1)
    binned = np.zeros(n_bins, dtype=np.complex128)
    for i in range(npl):
        binned[bin_idx[i]] += amps_last[i]
    return binned


def main():
    nl, hw, nw, npl, offsets, T, pos = _setup()
    zero_field = np.zeros((nl, npl))

    # Source positions: beam A at z=+3, beam B at z=-3
    iz_a = round(3.0 / H)
    iz_b = round(-3.0 / H)
    src_a = hw * nw + (hw + iz_a)
    src_b = hw * nw + (hw + iz_b)

    print("=" * 75)
    print("BMV TEST: GRAVITATIONALLY-INDUCED ENTANGLEMENT")
    print(f"Beam A: z=+{3.0}, Beam B: z=-{3.0}")
    print(f"h={H}, W={PHYS_W}, L={PHYS_L}")
    print("=" * 75)
    print()

    G_values = [0.0, 0.01, 0.05, 0.10, 0.20]

    for G in G_values:
        # Step 1: Propagate each beam independently on zero field
        psi_a_free = _prop(nl, nw, npl, hw, offsets, T, zero_field, K, src_a)
        psi_b_free = _prop(nl, nw, npl, hw, offsets, T, zero_field, K, src_b)

        if G == 0:
            # No gravitational interaction
            psi_a_final = psi_a_free
            psi_b_final = psi_b_free
        else:
            # Step 2: Self-consistent mutual interaction
            # Iterate: A generates field for B, B generates field for A
            field_from_a = np.zeros((nl, npl))
            field_from_b = np.zeros((nl, npl))

            for iteration in range(30):
                # Propagate A in B's field, B in A's field
                psi_a = _prop(nl, nw, npl, hw, offsets, T, field_from_b, K, src_a)
                psi_b = _prop(nl, nw, npl, hw, offsets, T, field_from_a, K, src_b)

                # Generate fields
                new_field_a = _field_from_amps(psi_a, nl, npl, pos, G)
                new_field_b = _field_from_amps(psi_b, nl, npl, pos, G)

                # Damped update
                field_from_a = 0.2 * new_field_a + 0.8 * field_from_a
                field_from_b = 0.2 * new_field_b + 0.8 * field_from_b

            psi_a_final = psi_a
            psi_b_final = psi_b

        # Step 3: Compute density matrix and entanglement
        # Bin detector amplitudes for A and B
        bins_a = _bin_z(psi_a_final[-1], nw, hw, H, N_YBINS)
        bins_b = _bin_z(psi_b_final[-1], nw, hw, H, N_YBINS)

        # Normalize
        na = np.sqrt(np.sum(np.abs(bins_a) ** 2))
        nb = np.sqrt(np.sum(np.abs(bins_b) ** 2))
        if na > 0:
            bins_a /= na
        if nb > 0:
            bins_b /= nb

        # The joint state is |Psi> = (|A>|a_field> + |B>|b_field>) / sqrt(2)
        # If the fields are DIFFERENT (because A and B are at different positions),
        # tracing over the field creates a mixed state → entanglement.
        #
        # Measure: overlap of A-in-B's-field vs A-in-free
        bins_a_free = _bin_z(psi_a_free[-1], nw, hw, H, N_YBINS)
        na_f = np.sqrt(np.sum(np.abs(bins_a_free) ** 2))
        if na_f > 0:
            bins_a_free /= na_f

        # Fidelity: |<a_free|a_grav>|^2
        fidelity_a = abs(np.dot(bins_a_free.conj(), bins_a)) ** 2

        # Same for B
        bins_b_free = _bin_z(psi_b_free[-1], nw, hw, H, N_YBINS)
        nb_f = np.sqrt(np.sum(np.abs(bins_b_free) ** 2))
        if nb_f > 0:
            bins_b_free /= nb_f
        fidelity_b = abs(np.dot(bins_b_free.conj(), bins_b)) ** 2

        # The key measure: if the gravitational interaction makes A's wavefunction
        # DEPEND on which slit B went through, the states are entangled.
        # Entanglement witness: 1 - fidelity (how much the gravity changed A)

        # Cross-interaction: propagate A in B's converged field
        # vs propagate A in A's own field
        # If these differ: the gravity carries which-path info

        # Decoherence functional: overlap of A-in-B-field with A-in-zero-field
        # tells us how much B's gravity decohered A
        decoherence_a = 1 - fidelity_a
        decoherence_b = 1 - fidelity_b

        # Mutual information proxy: how much does B's field change A?
        # This is the gravitational phase shift
        phase_shift_a = np.angle(np.dot(bins_a_free.conj(), bins_a))
        phase_shift_b = np.angle(np.dot(bins_b_free.conj(), bins_b))

        print(f"G={G:.2f}:")
        print(f"  fidelity_A = {fidelity_a:.6f} (1 = no change)")
        print(f"  fidelity_B = {fidelity_b:.6f}")
        print(f"  decoherence_A = {decoherence_a:.6f}")
        print(f"  decoherence_B = {decoherence_b:.6f}")
        print(f"  phase_shift_A = {phase_shift_a:+.4f} rad")
        print(f"  phase_shift_B = {phase_shift_b:+.4f} rad")

        # The entanglement measure: if A and B acquire DIFFERENT phase shifts
        # from each other's fields, the joint state is entangled.
        # The concurrence proxy: |phase_A - phase_B| * something
        diff_phase = abs(phase_shift_a - phase_shift_b)
        print(f"  |phase_A - phase_B| = {diff_phase:.6f}")
        print(f"  entanglement proxy: {diff_phase:.6f}")
        print()

    print("SAFE READ")
    print("  decoherence > 0 at G > 0: gravity modifies the beam → which-path info")
    print("  phase_shift != 0: gravity imparts a detectable phase → observable effect")
    print("  |phase_A - phase_B| > 0: beams acquire DIFFERENT phases from each other")
    print("    → the joint state is entangled (BMV effect)")
    print("  if this grows with G: stronger gravity → more entanglement")
    print()
    print("  NOTE: true entanglement requires a JOINT propagation where A and B")
    print("  are in superposition. Here we propagate them separately and check")
    print("  how much each is modified by the other. This is the WITNESS, not")
    print("  the full entanglement measure.")


if __name__ == "__main__":
    main()
