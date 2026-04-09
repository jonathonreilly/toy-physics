#!/usr/bin/env python3
"""Geometric growth with amplitude-guided node placement.

Instead of building a uniform graph and pruning, BUILD the graph
layer by layer with a local rule that uses the amplitude distribution
from the previous layer to guide where new nodes appear.

Rule:
  1. Build pre-barrier layers uniformly (including source, barrier, slits)
  2. For each post-barrier layer:
     a. Propagate amplitude from source through current graph
     b. Compute amplitude density per y-bin at the previous layer
     c. Sample new node y-positions from this density
     d. Connect to previous layers within connect_radius
  3. This naturally creates channels: high-amplitude regions attract
     more nodes, low-amplitude regions (gap) get fewer nodes

Physics: "new events appear where amplitude is concentrated."
This is a causal, local growth rule — each layer depends only on
the state at previous layers.

PStack experiment: geometric-growth-emergence
"""

from __future__ import annotations
import cmath, math, random
from collections import defaultdict, deque

BETA = 0.8; N_YBINS = 12; LAM = 10.0; K_BAND = (3.0, 5.0, 7.0)


def propagate_partial(positions, adj, src, k):
    """Propagate amplitude through current (partial) graph."""
    n = len(positions)
    in_deg = [0]*n
    for nbs in adj.values():
        for j in nbs: in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0); order = []
    while q:
        i = q.popleft(); order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0: q.append(j)
    amps = [0j]*n
    for s in src: amps[s] = 1.0/len(src)
    field = [0.0]*n
    for i in order:
        if abs(amps[i]) < 1e-30: continue
        pi = positions[i]
        for j in adj.get(i, []):
            pj = positions[j]; dx = pj[0]-pi[0]
            L = math.sqrt(sum((a-b)**2 for a, b in zip(pi, pj)))
            if L < 1e-10: continue
            theta = math.acos(min(max(dx/L,-1),1)); w = math.exp(-BETA*theta*theta)
            amps[j] += amps[i]*cmath.exp(1j*k*L)*w/L
    return amps


def amplitude_density_ybins(amps, positions, layer_nodes, yz_range, n_bins=N_YBINS):
    """Compute amplitude probability density in y-bins for a layer."""
    bin_width = 2*yz_range / n_bins
    bins = [0.0]*n_bins
    for i in layer_nodes:
        p = abs(amps[i])**2
        y = positions[i][1]
        b = int((y + yz_range) / bin_width)
        b = max(0, min(n_bins-1, b))
        bins[b] += p
    total = sum(bins)
    if total > 1e-30:
        bins = [b/total for b in bins]
    else:
        bins = [1.0/n_bins]*n_bins  # uniform fallback
    return bins


def sample_from_density(density, yz_range, rng, n_bins=N_YBINS, sharpness=2.0):
    """Sample a y-position from the amplitude density with tunable sharpness."""
    bin_width = 2*yz_range / n_bins
    # Sharpen the distribution
    weights = [d**sharpness for d in density]
    total = sum(weights)
    if total < 1e-30:
        return rng.uniform(-yz_range, yz_range)
    weights = [w/total for w in weights]
    # Weighted random bin selection
    r = rng.random()
    cumulative = 0
    chosen_bin = 0
    for i, w in enumerate(weights):
        cumulative += w
        if r <= cumulative:
            chosen_bin = i
            break
    # Random position within chosen bin
    bin_start = -yz_range + chosen_bin * bin_width
    return bin_start + rng.uniform(0, bin_width)


def generate_grown_dag(n_layers=20, npl=30, yz_range=10.0, r=3.5,
                       rng_seed=42, sharpness=2.0):
    """Build DAG with amplitude-guided post-barrier node placement."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    bl = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        nodes = []

        if layer == 0:
            positions.append((x, 0.0, 0.0))
            nodes.append(len(positions)-1)
        elif layer <= bl:
            # Pre-barrier: uniform placement
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layer_indices[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r: adj[pi].append(idx)
        else:
            # Post-barrier: amplitude-guided placement
            # Get amplitude density from previous layer
            src = layer_indices[0]
            amps = propagate_partial(positions, adj, src, 5.0)
            prev_layer = layer_indices[-1]
            density = amplitude_density_ybins(amps, positions, prev_layer, yz_range)

            for _ in range(npl):
                y = sample_from_density(density, yz_range, rng, sharpness=sharpness)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layer_indices[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r: adj[pi].append(idx)

        layer_indices.append(nodes)

    return positions, dict(adj), layer_indices


def compute_field(positions, adj, mass_ids, iterations=50):
    n = len(positions); undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs: undirected[i].add(j); undirected[j].add(i)
    ms = set(mass_ids); field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0]*n
        for i in range(n):
            if i in ms: nf[i] = 1.0
            elif undirected.get(i): nf[i] = sum(field[j] for j in undirected[i])/len(undirected[i])
        field = nf
    return field


def propagate(positions, adj, field, src, k, blocked=None):
    n = len(positions); blocked = blocked or set()
    in_deg = [0]*n
    for nbs in adj.values():
        for j in nbs: in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0); order = []
    while q:
        i = q.popleft(); order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0: q.append(j)
    amps = [0j]*n
    for s in src: amps[s] = 1.0/len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked: continue
        pi = positions[i]
        for j in adj.get(i, []):
            if j in blocked: continue
            pj = positions[j]; dx = pj[0]-pi[0]
            L = math.sqrt(sum((a-b)**2 for a, b in zip(pi, pj)))
            if L < 1e-10: continue
            theta = math.acos(min(max(dx/L,-1),1)); w = math.exp(-BETA*theta*theta)
            lf = 0.5*(field[i]+field[j]); dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L,0)); act = dl-ret
            amps[j] += amps[i]*cmath.exp(1j*k*act)*w/L
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list: p = abs(amps[d])**2; total += p; wy += p*positions[d][1]
    return wy/total if total > 1e-30 else 0.0


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys: return 0.0
    y_min, y_max = min(ys)-0.01, max(ys)+0.01; bw = (y_max-y_min)/8
    ba = [0j]*8; bb = [0j]*8
    for m in mid_nodes:
        b = max(0, min(7, int((positions[m][1]-y_min)/bw)))
        ba[b] += amps_a[m]; bb[b] += amps_b[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    d = sum(abs(a)**2 for a in ba) + sum(abs(b)**2 for b in bb)
    return S/d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1,d2)] = (amps_a[d1]*amps_a[d2].conjugate() + amps_b[d1]*amps_b[d2].conjugate() +
                            D*amps_a[d1]*amps_b[d2].conjugate() + D*amps_b[d1]*amps_a[d2].conjugate())
    tr = sum(rho[(d,d)] for d in det_list).real
    if tr <= 1e-30: return math.nan
    for key in rho: rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def measure_decoherence(positions, adj, layer_indices):
    n = len(positions); n_layers = len(layer_indices); bl_idx = n_layers//3
    src = layer_indices[0]; det_list = list(layer_indices[-1])
    if not det_list or n_layers < 7: return math.nan
    all_ys = [positions[i][1] for i in range(n)]; cy = sum(all_ys)/len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
    if not slit_a or not slit_b: return math.nan
    blocked = set(barrier) - set(slit_a+slit_b)
    blocked_a = blocked|set(slit_b); blocked_b = blocked|set(slit_a)
    bath_mass = []
    for li in range(bl_idx+1, min(n_layers, bl_idx+3)):
        for i in layer_indices[li]:
            if abs(positions[i][1]-cy) <= 3: bath_mass.append(i)
    grav_idx = 2*n_layers//3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1]
    all_mass = list(set(bath_mass)|set(grav_mass))
    field = compute_field(positions, adj, all_mass) if all_mass else [0.0]*n
    mid_nodes = [i for li in range(bl_idx+1, n_layers-1) for i in layer_indices[li]
                 if i not in blocked and i not in set(det_list)]
    if len(mid_nodes) < 4: return math.nan
    pur_list = []
    for k in K_BAND:
        aa = propagate(positions, adj, field, src, k, blocked_a)
        ab = propagate(positions, adj, field, src, k, blocked_b)
        Sn = cl_contrast(aa, ab, mid_nodes, positions)
        D = math.exp(-LAM**2*Sn); pur = cl_purity(aa, ab, D, det_list)
        if not math.isnan(pur): pur_list.append(pur)
    return sum(pur_list)/len(pur_list) if pur_list else math.nan


def gap_metric(positions, layer_indices):
    n_layers = len(layer_indices); bl_idx = n_layers//3; det_set = set(layer_indices[-1])
    ys = []
    for li in range(bl_idx+1, n_layers-1):
        for i in layer_indices[li]:
            if i not in det_set: ys.append(positions[i][1])
    if len(ys) < 10: return 0.0
    ys.sort()
    return max(ys[i]-ys[i-1] for i in range(1, len(ys)))


def gen_uniform(n_layers=20, npl=30, yz_range=10.0, r=3.5, rng_seed=42):
    rng = random.Random(rng_seed)
    positions = []; adj = defaultdict(list); layers = []
    for layer in range(n_layers):
        x = float(layer); nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0)); nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range); z = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r: adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def main():
    n_seeds = 16
    print("=" * 74)
    print("GEOMETRIC GROWTH: amplitude-guided node placement")
    print("  Post-barrier nodes placed where amplitude is concentrated")
    print("  Graph is BUILT by the dynamics, not post-hoc modified")
    print("=" * 74)
    print()

    n_layers_list = [20, 25, 30, 40, 50, 60]

    for label, gen_fn, kwargs in [
        ("Uniform baseline", gen_uniform, {}),
        ("Grown sharpness=1.5", generate_grown_dag, {"sharpness": 1.5}),
        ("Grown sharpness=2.0", generate_grown_dag, {"sharpness": 2.0}),
        ("Grown sharpness=3.0", generate_grown_dag, {"sharpness": 3.0}),
    ]:
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_cl':>8s}  {'gap':>6s}  {'n':>3s}")
        print(f"  {'-'*24}")

        for nl in n_layers_list:
            purs = []; gaps = []
            for seed in range(n_seeds):
                positions, adj, layers = gen_fn(n_layers=nl, rng_seed=seed*13+5, **kwargs)
                pur = measure_decoherence(positions, adj, layers)
                if not math.isnan(pur):
                    purs.append(pur)
                    gaps.append(gap_metric(positions, layers))
            if purs:
                print(f"  {nl:4d}  {sum(purs)/len(purs):8.4f}  "
                      f"{sum(gaps)/len(gaps):6.2f}  {len(purs):3d}")
            else: print(f"  {nl:4d}  FAIL")
        print()

    print("=" * 74)
    print("KEY: does amplitude-guided growth create decoherence-friendly topology")
    print("without an imposed gap? If pur_cl < uniform at N=40+: success.")
    print("=" * 74)


if __name__ == "__main__":
    main()
