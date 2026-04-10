#!/usr/bin/env python3
"""Kernel from unitarity: does norm-preservation constrain w(theta)?

THE IDEA:
  If the transfer matrix M must be unitary (norm-preserving), the condition
    sum_offsets |M[out,in]|^2 = 1  for all in
  constrains the angular kernel w(theta).

  With M[out,in] = exp(ikS) * w(theta) * h^d / L^p, and |exp(ikS)|=1:
    sum_offsets w(theta)^2 * h^(2d) / L^(2p) = 1

  This constrains the normalization AND functional form of w(theta).

WHAT WE COMPUTE:
  Part 1: Normalization sum N = sum w(theta)^2 * h^(2d) / L^(2p) for each kernel
  Part 2: Unitarity-normalized kernels w_norm = w / sqrt(N)
  Part 3: Isotropy test -- propagate N layers with normalized kernels
  Part 4: Gravity test -- compare gravitational signal with normalized kernels

HYPOTHESIS: "Unitarity constrains w(theta) and the optimal kernel matches cos^(d-1)."
FALSIFICATION: "If the unitarity-normalized kernel has no relation to the empirical best."

Uses 2D DAG infrastructure from toy_event_physics. Pure Python (no numpy).
"""
from __future__ import annotations

import cmath
import math
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import build_rectangular_nodes

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
H = 0.5          # lattice spacing
D_SPATIAL = 2    # spatial dimensions (2+1D)
P = 2            # distance-law exponent in 1/L^p
K = 5.0          # wavenumber
WIDTH = 20
HEIGHT = 8
SOURCE_Y = HEIGHT // 2
MASS_POS_Y = HEIGHT // 2 + 2
STRENGTH = 5e-4

# For 3+1D comparison
D_SPATIAL_3D = 3
P_3D = 2


# ---------------------------------------------------------------------------
# Offset geometry
# ---------------------------------------------------------------------------
def get_offsets_2d():
    """All forward offsets on 2D lattice with spacing h.
    From (x,y) to (x+h, y+dy*h) for dy in {-1, 0, 1}."""
    offsets = []
    for dy in [-1, 0, 1]:
        dx = H
        ddy = dy * H
        L = math.sqrt(dx**2 + ddy**2)
        theta = math.atan2(abs(ddy), dx)
        offsets.append((dy, L, theta))
    return offsets


def get_offsets_3d():
    """All forward offsets on 3D lattice with spacing h.
    From (x,y,z) to (x+h, y+dy*h, z+dz*h) for dy,dz in {-1,0,1}."""
    offsets = []
    for dy in [-1, 0, 1]:
        for dz in [-1, 0, 1]:
            dx = H
            ddy = dy * H
            ddz = dz * H
            L = math.sqrt(dx**2 + ddy**2 + ddz**2)
            theta = math.acos(dx / L)  # polar angle from forward
            offsets.append((dy, dz, L, theta))
    return offsets


# ---------------------------------------------------------------------------
# Kernels
# ---------------------------------------------------------------------------
def kernel_uniform(theta):
    return 1.0

def kernel_cos(theta):
    return math.cos(theta)

def kernel_cos2(theta):
    return math.cos(theta)**2

def kernel_exp(theta):
    return math.exp(-0.8 * theta**2)

def kernel_cos_d_minus_1(theta, d):
    """cos^(d-1)(theta) -- the conjectured dimension-dependent kernel."""
    return math.cos(theta)**(d - 1)


KERNELS = {
    "uniform": kernel_uniform,
    "cos": kernel_cos,
    "cos^2": kernel_cos2,
    "exp(-0.8t^2)": kernel_exp,
}


# ---------------------------------------------------------------------------
# Part 1: Normalization sums
# ---------------------------------------------------------------------------
def compute_norm_sum(offsets_list, kernel_fn, d_spatial, p):
    """Compute N = sum_offsets w(theta)^2 * h^(2d) / L^(2p).
    d = d_spatial (number of spatial dims crossed per edge on avg -- here it's
    the dimension of the spatial lattice, so h^d is the lattice volume element).
    """
    total = 0.0
    for offset in offsets_list:
        if len(offset) == 3:
            _, L, theta = offset
        else:
            _, _, L, theta = offset
        w = kernel_fn(theta)
        total += w**2 * H**(2 * d_spatial) / L**(2 * p)
    return total


def part1():
    print("=" * 70)
    print("PART 1: NORMALIZATION SUMS (non-unitarity measure)")
    print("=" * 70)

    offsets_2d = get_offsets_2d()
    offsets_3d = get_offsets_3d()

    print(f"\nParameters: h={H}, p={P}")
    print(f"  2+1D: d_spatial={D_SPATIAL}, {len(offsets_2d)} offsets")
    print(f"  3+1D: d_spatial={D_SPATIAL_3D}, {len(offsets_3d)} offsets")

    print("\n--- 2+1D (d_spatial=2) ---")
    print(f"{'Kernel':<16} {'N (norm sum)':<16} {'sqrt(N)':<12} {'1/sqrt(N)':<12}")
    print("-" * 56)

    norms_2d = {}
    for name, kfn in KERNELS.items():
        N = compute_norm_sum(offsets_2d, kfn, D_SPATIAL, P)
        norms_2d[name] = N
        print(f"{name:<16} {N:<16.8f} {math.sqrt(N):<12.8f} {1/math.sqrt(N):<12.4f}")

    # Also test cos^(d-1) = cos^1
    N_cd1 = compute_norm_sum(offsets_2d, lambda t: kernel_cos_d_minus_1(t, D_SPATIAL), D_SPATIAL, P)
    norms_2d["cos^(d-1)=cos^1"] = N_cd1
    print(f"{'cos^(d-1)=cos^1':<16} {N_cd1:<16.8f} {math.sqrt(N_cd1):<12.8f} {1/math.sqrt(N_cd1):<12.4f}")

    print("\n--- 3+1D (d_spatial=3) ---")
    print(f"{'Kernel':<16} {'N (norm sum)':<16} {'sqrt(N)':<12} {'1/sqrt(N)':<12}")
    print("-" * 56)

    norms_3d = {}
    for name, kfn in KERNELS.items():
        N = compute_norm_sum(offsets_3d, kfn, D_SPATIAL_3D, P_3D)
        norms_3d[name] = N
        print(f"{name:<16} {N:<16.8f} {math.sqrt(N):<12.8f} {1/math.sqrt(N):<12.4f}")

    # cos^(d-1) = cos^2
    N_cd1_3d = compute_norm_sum(offsets_3d, lambda t: kernel_cos_d_minus_1(t, D_SPATIAL_3D), D_SPATIAL_3D, P_3D)
    norms_3d["cos^(d-1)=cos^2"] = N_cd1_3d
    print(f"{'cos^(d-1)=cos^2':<16} {N_cd1_3d:<16.8f} {math.sqrt(N_cd1_3d):<12.8f} {1/math.sqrt(N_cd1_3d):<12.4f}")

    print("\nInterpretation:")
    print("  N > 1  =>  amplitude GROWS each layer (unstable, non-unitary)")
    print("  N < 1  =>  amplitude DECAYS each layer (dissipative)")
    print("  N = 1  =>  norm preserved (unitary transfer)")

    return norms_2d, norms_3d


# ---------------------------------------------------------------------------
# Part 2: Unitarity-normalized kernels
# ---------------------------------------------------------------------------
def part2(norms_2d, norms_3d):
    print("\n\n" + "=" * 70)
    print("PART 2: UNITARITY-NORMALIZED KERNELS")
    print("=" * 70)

    offsets_2d = get_offsets_2d()
    offsets_3d = get_offsets_3d()

    print("\n--- 2+1D: Normalized kernel values at each offset ---")
    for name, kfn in KERNELS.items():
        N = norms_2d[name]
        scale = 1.0 / math.sqrt(N)
        print(f"\n  {name} (scale factor = {scale:.6f}):")
        for dy, L, theta in offsets_2d:
            w_orig = kfn(theta)
            w_norm = w_orig * scale
            theta_deg = math.degrees(theta)
            print(f"    dy={dy:+d}  theta={theta_deg:5.1f} deg  L={L:.4f}  "
                  f"w_orig={w_orig:.6f}  w_norm={w_norm:.6f}  "
                  f"contrib={w_norm**2 * H**(2*D_SPATIAL) / L**(2*P):.8f}")

    print("\n--- 3+1D: Normalized kernel values at each offset ---")
    for name, kfn in KERNELS.items():
        N = norms_3d[name]
        scale = 1.0 / math.sqrt(N)
        print(f"\n  {name} (scale factor = {scale:.6f}):")
        for dy, dz, L, theta in offsets_3d:
            w_orig = kfn(theta)
            w_norm = w_orig * scale
            theta_deg = math.degrees(theta)
            print(f"    dy={dy:+d} dz={dz:+d}  theta={theta_deg:5.1f} deg  L={L:.4f}  "
                  f"w_orig={w_orig:.6f}  w_norm={w_norm:.6f}")


# ---------------------------------------------------------------------------
# Part 3: Isotropy test with normalized propagation
# ---------------------------------------------------------------------------
def build_dag_2d(nodes):
    dag = defaultdict(list)
    for node in nodes:
        x, y = node
        for dy in [-1, 0, 1]:
            nb = (x + 1, y + dy)
            if nb in nodes:
                dag[node].append(nb)
    return dag


def spatial_only_field(nodes, mass_y, strength):
    field = {}
    for n in nodes:
        r = abs(n[1] - mass_y) + 0.1
        field[n] = strength / r
    return field


def propagate_normalized(nodes, source, node_field, dag, k, kernel_fn, norm_sum,
                         d_spatial, p, width):
    """Propagate with unitarity-normalized kernel.
    Edge amplitude = exp(ikS) * w_norm(theta) * h^d / L^p
    where w_norm = w / sqrt(norm_sum).
    """
    scale = 1.0 / math.sqrt(norm_sum) if norm_sum > 0 else 1.0
    order = sorted(nodes, key=lambda n: n[0])
    states = defaultdict(complex)
    states[source] = 1.0 + 0j
    detector = {}

    for node in order:
        amp = states.get(node, 0j)
        if abs(amp) < 1e-30:
            continue
        if node[0] == width:
            detector[node[1]] = detector.get(node[1], 0j) + amp
            continue
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            theta = math.atan2(abs(nb[1] - node[1]), nb[0] - node[0])
            w = kernel_fn(theta) * scale
            f = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            act = L * (1.0 - f)
            edge_amp = cmath.exp(1j * k * act) * w * H**d_spatial / L**p
            states[nb] += amp * edge_amp

    return detector


def propagate_unnormalized(nodes, source, node_field, dag, k, kernel_fn,
                           d_spatial, p, width):
    """Propagate WITHOUT unitarity normalization for comparison.
    Edge amplitude = exp(ikS) * w(theta) * h^d / L^p.
    """
    order = sorted(nodes, key=lambda n: n[0])
    states = defaultdict(complex)
    states[source] = 1.0 + 0j
    detector = {}

    for node in order:
        amp = states.get(node, 0j)
        if abs(amp) < 1e-30:
            continue
        if node[0] == width:
            detector[node[1]] = detector.get(node[1], 0j) + amp
            continue
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            theta = math.atan2(abs(nb[1] - node[1]), nb[0] - node[0])
            w = kernel_fn(theta)
            f = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            act = L * (1.0 - f)
            edge_amp = cmath.exp(1j * k * act) * w * H**d_spatial / L**p
            states[nb] += amp * edge_amp

    return detector


def centroid_shift(det, source_y):
    total = sum(abs(a)**2 for a in det.values())
    if total < 1e-30:
        return 0.0, total
    c = sum(y * abs(a)**2 for y, a in det.items()) / total
    return c - source_y, total


def part3(norms_2d):
    print("\n\n" + "=" * 70)
    print("PART 3: PROPAGATION -- NORMALIZED vs UNNORMALIZED")
    print("=" * 70)

    nodes = build_rectangular_nodes(WIDTH, HEIGHT)
    dag = build_dag_2d(nodes)
    source = (0, SOURCE_Y)

    # Flat field (no mass)
    flat_field = {n: 0.0 for n in nodes}
    # Mass field
    mass_field = spatial_only_field(nodes, MASS_POS_Y, STRENGTH)

    print(f"\nGrid: {WIDTH}x{HEIGHT}, h={H}, k={K}, source_y={SOURCE_Y}, mass_y={MASS_POS_Y}")
    print(f"Strength={STRENGTH}")

    print("\n--- Flat-field total probability (norm preservation check) ---")
    print(f"{'Kernel':<16} {'Unnorm P_total':<18} {'Norm P_total':<18} {'Ratio':<12}")
    print("-" * 64)

    for name, kfn in KERNELS.items():
        N = norms_2d[name]

        det_un = propagate_unnormalized(nodes, source, flat_field, dag, K, kfn,
                                        D_SPATIAL, P, WIDTH)
        _, p_un = centroid_shift(det_un, SOURCE_Y)

        det_n = propagate_normalized(nodes, source, flat_field, dag, K, kfn, N,
                                     D_SPATIAL, P, WIDTH)
        _, p_n = centroid_shift(det_n, SOURCE_Y)

        ratio = p_n / p_un if p_un > 1e-30 else 0.0
        print(f"{name:<16} {p_un:<18.10e} {p_n:<18.10e} {ratio:<12.6f}")

    print("\n--- Gravity signal (centroid shift toward mass) ---")
    print(f"{'Kernel':<16} {'Unnorm shift':<16} {'Norm shift':<16} {'Direction':<12}")
    print("-" * 60)

    results = {}
    for name, kfn in KERNELS.items():
        N = norms_2d[name]

        # Flat baseline
        det_flat_n = propagate_normalized(nodes, source, flat_field, dag, K, kfn, N,
                                          D_SPATIAL, P, WIDTH)
        c_flat_n, _ = centroid_shift(det_flat_n, SOURCE_Y)

        # With mass
        det_mass_n = propagate_normalized(nodes, source, mass_field, dag, K, kfn, N,
                                          D_SPATIAL, P, WIDTH)
        c_mass_n, _ = centroid_shift(det_mass_n, SOURCE_Y)

        # Unnormalized
        det_flat_un = propagate_unnormalized(nodes, source, flat_field, dag, K, kfn,
                                             D_SPATIAL, P, WIDTH)
        c_flat_un, _ = centroid_shift(det_flat_un, SOURCE_Y)

        det_mass_un = propagate_unnormalized(nodes, source, mass_field, dag, K, kfn,
                                              D_SPATIAL, P, WIDTH)
        c_mass_un, _ = centroid_shift(det_mass_un, SOURCE_Y)

        shift_un = c_mass_un - c_flat_un
        shift_n = c_mass_n - c_flat_n

        # Positive shift = toward higher y = toward mass (mass is at y+2)
        direction = "TOWARD" if shift_n > 0 else "AWAY"
        results[name] = (shift_un, shift_n, direction)
        print(f"{name:<16} {shift_un:<16.8e} {shift_n:<16.8e} {direction:<12}")

    return results


# ---------------------------------------------------------------------------
# Part 4: What does unitarity PREDICT for the kernel?
# ---------------------------------------------------------------------------
def part4(norms_2d, norms_3d):
    print("\n\n" + "=" * 70)
    print("PART 4: UNITARITY PREDICTION -- WHAT KERNEL DOES N=1 PREFER?")
    print("=" * 70)

    offsets_2d = get_offsets_2d()
    offsets_3d = get_offsets_3d()

    # For cos^alpha kernel, compute N(alpha) and find alpha where N is "natural"
    # i.e. closest to 1 without needing large rescaling
    print("\n--- 2+1D: N(alpha) for cos^alpha kernel ---")
    print(f"{'alpha':<10} {'N':<16} {'sqrt(N)':<12} {'|1-N|':<12}")
    print("-" * 50)

    best_alpha_2d = None
    best_dev_2d = float('inf')
    for alpha_10 in range(0, 51):  # 0.0 to 5.0
        alpha = alpha_10 / 10.0
        def kfn(t, a=alpha):
            return math.cos(t)**a
        N = compute_norm_sum(offsets_2d, kfn, D_SPATIAL, P)
        dev = abs(1.0 - N)
        if dev < best_dev_2d:
            best_dev_2d = dev
            best_alpha_2d = alpha
        if alpha_10 % 5 == 0:
            print(f"{alpha:<10.1f} {N:<16.8f} {math.sqrt(N):<12.8f} {dev:<12.8f}")

    print(f"\n  Best alpha (closest to N=1): {best_alpha_2d:.1f}  "
          f"(deviation: {best_dev_2d:.8f})")
    print(f"  d-1 = {D_SPATIAL - 1}  =>  cos^(d-1) prediction: alpha = {D_SPATIAL - 1}")

    print("\n--- 3+1D: N(alpha) for cos^alpha kernel ---")
    print(f"{'alpha':<10} {'N':<16} {'sqrt(N)':<12} {'|1-N|':<12}")
    print("-" * 50)

    best_alpha_3d = None
    best_dev_3d = float('inf')
    for alpha_10 in range(0, 51):
        alpha = alpha_10 / 10.0
        def kfn(t, a=alpha):
            return math.cos(t)**a
        N = compute_norm_sum(offsets_3d, kfn, D_SPATIAL_3D, P_3D)
        dev = abs(1.0 - N)
        if dev < best_dev_3d:
            best_dev_3d = dev
            best_alpha_3d = alpha
        if alpha_10 % 5 == 0:
            print(f"{alpha:<10.1f} {N:<16.8f} {math.sqrt(N):<12.8f} {dev:<12.8f}")

    print(f"\n  Best alpha (closest to N=1): {best_alpha_3d:.1f}  "
          f"(deviation: {best_dev_3d:.8f})")
    print(f"  d-1 = {D_SPATIAL_3D - 1}  =>  cos^(d-1) prediction: alpha = {D_SPATIAL_3D - 1}")

    # Finer search around the best
    print("\n--- Fine search for N=1 alpha ---")
    for label, offsets, d_sp, p_val, coarse_best in [
        ("2+1D", offsets_2d, D_SPATIAL, P, best_alpha_2d),
        ("3+1D", offsets_3d, D_SPATIAL_3D, P_3D, best_alpha_3d),
    ]:
        best_a = coarse_best
        best_d = float('inf')
        for a_100 in range(max(0, int(coarse_best * 100) - 100),
                           int(coarse_best * 100) + 101):
            alpha = a_100 / 100.0
            def kfn(t, a=alpha):
                return math.cos(t)**a
            N = compute_norm_sum(offsets, kfn, d_sp, p_val)
            dev = abs(1.0 - N)
            if dev < best_d:
                best_d = dev
                best_a = alpha
        print(f"  {label}: alpha_opt = {best_a:.2f}  (N deviation = {best_d:.10f})")
        print(f"         d-1 = {d_sp - 1}")

    return best_alpha_2d, best_alpha_3d


# ---------------------------------------------------------------------------
# Part 5: Layer-by-layer norm evolution
# ---------------------------------------------------------------------------
def part5(norms_2d):
    print("\n\n" + "=" * 70)
    print("PART 5: LAYER-BY-LAYER NORM EVOLUTION")
    print("=" * 70)
    print("Track total probability |psi|^2 at each x-layer to check if")
    print("unitarity normalization actually preserves the norm over many steps.\n")

    nodes = build_rectangular_nodes(WIDTH, HEIGHT)
    dag = build_dag_2d(nodes)
    source = (0, SOURCE_Y)
    flat_field = {n: 0.0 for n in nodes}

    for name, kfn in KERNELS.items():
        N = norms_2d[name]
        scale = 1.0 / math.sqrt(N) if N > 0 else 1.0

        # Layer-by-layer propagation tracking norm
        states = defaultdict(complex)
        states[source] = 1.0 + 0j

        order = sorted(nodes, key=lambda n: n[0])
        layer_norms_n = {}  # normalized
        layer_norms_u = {}  # unnormalized

        # Normalized
        states_n = defaultdict(complex)
        states_n[source] = 1.0 + 0j
        states_u = defaultdict(complex)
        states_u[source] = 1.0 + 0j

        # Group nodes by x
        layers = defaultdict(list)
        for n in nodes:
            layers[n[0]].append(n)

        for x in sorted(layers.keys()):
            # Compute norm at this layer
            norm_n = sum(abs(states_n.get(n, 0j))**2 for n in layers[x])
            norm_u = sum(abs(states_u.get(n, 0j))**2 for n in layers[x])
            layer_norms_n[x] = norm_n
            layer_norms_u[x] = norm_u

            # Propagate to next layer
            for node in layers[x]:
                amp_n = states_n.get(node, 0j)
                amp_u = states_u.get(node, 0j)
                if abs(amp_n) < 1e-30 and abs(amp_u) < 1e-30:
                    continue
                for nb in dag.get(node, []):
                    L = math.dist(node, nb)
                    theta = math.atan2(abs(nb[1] - node[1]), nb[0] - node[0])
                    w = kfn(theta)
                    f = 0.0  # flat field
                    act = L * (1.0 - f)
                    phase = cmath.exp(1j * K * act)

                    # Normalized
                    edge_n = phase * w * scale * H**D_SPATIAL / L**P
                    states_n[nb] = states_n.get(nb, 0j) + amp_n * edge_n

                    # Unnormalized
                    edge_u = phase * w * H**D_SPATIAL / L**P
                    states_u[nb] = states_u.get(nb, 0j) + amp_u * edge_u

        print(f"  {name}:")
        print(f"    {'Layer x':<10} {'Norm (normalized)':<22} {'Norm (unnormalized)':<22}")
        for x in sorted(layer_norms_n.keys()):
            if x <= WIDTH:
                nn = layer_norms_n.get(x, 0.0)
                nu = layer_norms_u.get(x, 0.0)
                print(f"    {x:<10} {nn:<22.10e} {nu:<22.10e}")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("FRONTIER: KERNEL FROM UNITARITY")
    print("Does norm-preservation constrain the angular kernel w(theta)?")
    print("=" * 70)

    norms_2d, norms_3d = part1()
    part2(norms_2d, norms_3d)
    grav_results = part3(norms_2d)
    best_2d, best_3d = part4(norms_2d, norms_3d)
    part5(norms_2d)

    # ---------------------------------------------------------------------------
    # VERDICT
    # ---------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    print(f"\n  2+1D: alpha that gives N closest to 1 = {best_2d:.1f}  (d-1 = {D_SPATIAL - 1})")
    print(f"  3+1D: alpha that gives N closest to 1 = {best_3d:.1f}  (d-1 = {D_SPATIAL_3D - 1})")

    match_2d = abs(best_2d - (D_SPATIAL - 1)) < 0.5
    match_3d = abs(best_3d - (D_SPATIAL_3D - 1)) < 0.5

    print(f"\n  cos^(d-1) match in 2+1D: {'YES' if match_2d else 'NO'}")
    print(f"  cos^(d-1) match in 3+1D: {'YES' if match_3d else 'NO'}")

    # Check gravity
    print("\n  Gravity with normalized kernels:")
    for name, (shift_un, shift_n, direction) in grav_results.items():
        print(f"    {name:<16}: {direction}  (shift = {shift_n:.2e})")

    # Overall
    if match_2d and match_3d:
        print("\n  HYPOTHESIS SUPPORTED: Unitarity naturally selects cos^(d-1).")
        print("  The N=1 condition (norm-preservation) picks the same kernel")
        print("  that empirical isotropy tests identified.")
    elif match_2d or match_3d:
        print("\n  PARTIAL SUPPORT: Unitarity selects cos^(d-1) in one dimension")
        print("  but not the other. Relationship is suggestive but not definitive.")
    else:
        print("\n  HYPOTHESIS FALSIFIED: Unitarity-preferred alpha does not match d-1.")
        print("  The unitarity constraint on normalization is separate from the")
        print("  functional form that gives best isotropy/gravity.")

    print("\n  NOTE: Unitarity constrains the NORMALIZATION (overall scale) of w,")
    print("  not its functional form. All kernels can be made unitary by rescaling.")
    print("  The question is which kernel NATURALLY has N~1 without rescaling,")
    print("  i.e. which is the 'natural' kernel for the lattice geometry.")


if __name__ == "__main__":
    main()
