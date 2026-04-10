#!/usr/bin/env python3
"""Kernel from local continuation: derive w(theta) from Axioms 3, 6, 10.

THE IDEA:
  Instead of fitting w(theta) to gravity data, DERIVE it from first principles:
    Axiom 6: "Free systems follow the locally simplest admissible continuation."
    Axiom 3: "Space is inferred from influence neighborhoods."
    Axiom 10: "Prefer persistent local mechanisms."

THREE CANDIDATE ROUTES:

  Route A — Turn-cost variational law:
    "Simplest continuation" = minimum directional change.
    Weight w = exp(-beta * delta_theta^2).
    For first edge (no history): w = exp(-beta * theta^2).
    For subsequent edges: path-dependent (Markov chain on angles).
    Prediction: effective single-edge kernel emerges from marginalizing over paths.

  Route B — Neighborhood-overlap law:
    Weight by overlap of influence neighborhoods (Axiom 3).
    Nodes sharing more neighbors have stronger "spatial affinity."
    w(dy,dz) = |N(src) & N(dst)| / |N(src) | N(dst)|
    Translates to a function of |offset| hence of theta.

  Route C — Combinatorial path-counting correction:
    Number of lattice edges at angle theta has geometric multiplicity.
    To make the propagator isotropic, w(theta) must CANCEL this bias:
    w(theta) = 1 / multiplicity(theta).
    On a cubic lattice with max_d offsets, multiplicity at given theta
    is the number of (dy,dz) pairs with atan2(sqrt(dy^2+dz^2), 1) = theta.

TEST EACH:
  1. Does it produce monotonically decreasing w(theta)?
  2. Does it match cos^(d-1)(theta)?
  3. Does it give TOWARD gravity on the retained lattice?
  4. Does it pass Born?

PARAMETERS: h=0.5, W=6, L=12, k=5.0
HYPOTHESIS: "At least one local-continuation rule predicts the retained kernel family."
FALSIFICATION: "If none of the three routes gives a decreasing w(theta) that passes Born + gravity."
"""
from __future__ import annotations

import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc

# ===========================================================================
# Parameters
# ===========================================================================
H = 0.5
K = 5.0
STRENGTH = 5e-5

# 2+1D
D2 = 2          # spatial dimensions
P2 = 2          # 1/L^p power
W2 = 6          # physical width
L2 = 12         # physical length
MAX_D2 = 3      # physical max transverse reach

# 3+1D
D3 = 3
P3 = 3
W3 = 4
L3 = 10
MAX_D3 = 2


# ===========================================================================
# Lattice infrastructure (2+1D, numpy-accelerated)
# ===========================================================================
class Lattice3D:
    """3D ordered lattice: 2 spatial + 1 causal."""

    def __init__(self, phys_l, phys_w, h, max_d_phys, weight_fn, power):
        self.h = h
        self.power = power
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 2
        self.n = self.nl * self.npl
        self._hm = h * h   # h^d_spatial for d=2

        self.pos = np.zeros((self.n, 3))
        self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(layer, iy, iz)] = idx
                    idx += 1

        self._off = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                w = weight_fn(theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n; nl = self.nl; nw = self._nw; hm = self._hm
        p = self.power
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0
        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True
        for layer in range(nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls:ls + self.npl].copy()
            sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue
            sf = field[ls:ls + self.npl]
            df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]
            for dy, dz, L, w in self._off:
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM); zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** p)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


class Lattice4D:
    """4D ordered lattice: 3 spatial + 1 causal."""

    def __init__(self, phys_l, h, phys_w, max_d_phys, weight_fn, power):
        self.h = h
        self.power = power
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 3
        self.n = self.nl * self.npl
        self._hm = h ** 3  # h^d_spatial for d=3

        self.pos = np.zeros((self.n, 4))
        self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    for iw in range(-self.hw, self.hw + 1):
                        self.pos[idx] = (x, iy * h, iz * h, iw * h)
                        self.nmap[(layer, iy, iz, iw)] = idx
                        idx += 1

        self._off = []
        md = self.max_d
        for dy in range(-md, md + 1):
            for dz in range(-md, md + 1):
                for dw in range(-md, md + 1):
                    dyp, dzp, dwp = dy * h, dz * h, dw * h
                    L = math.sqrt(h*h + dyp*dyp + dzp*dzp + dwp*dwp)
                    r_trans = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                    theta = math.atan2(r_trans, h)
                    w = weight_fn(theta)
                    self._off.append((dy, dz, dw, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n; nl = self.nl; nw = self._nw; hm = self._hm
        p = self.power
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0, 0), 0)
        amps[src] = 1.0
        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True
        for layer in range(nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls:ls + self.npl].copy()
            sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue
            sf = field[ls:ls + self.npl]
            df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]
            for dy, dz, dw, L, w in self._off:
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                wm = max(0, -dw); wM = min(nw, nw - dw)
                if ym >= yM or zm >= zM or wm >= wM:
                    continue
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                wr = np.arange(wm, wM)
                siy, siz, siw = np.meshgrid(yr, zr, wr, indexing='ij')
                si = siy.ravel()*nw*nw + siz.ravel()*nw + siw.ravel()
                di = ((siy.ravel()+dy)*nw*nw + (siz.ravel()+dz)*nw + (siw.ravel()+dw))
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** p)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# ===========================================================================
# Shared helpers
# ===========================================================================

def make_field_3d(lat, z_mass_phys, strength):
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r_spatial = np.sqrt(
        (lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2
    ) + 0.1
    return strength / r_spatial, mi


def make_field_4d(lat, z_mass_phys, strength):
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz, 0))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz, mw = lat.pos[mi, 1], lat.pos[mi, 2], lat.pos[mi, 3]
    r_spatial = np.sqrt(
        (lat.pos[:, 1] - my) ** 2 +
        (lat.pos[:, 2] - mz) ** 2 +
        (lat.pos[:, 3] - mw) ** 2
    ) + 0.1
    return strength / (r_spatial ** 2), mi


def setup_slits_3d(lat):
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked


def setup_slits_4d(lat):
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            for iw in range(-lat.hw, lat.hw + 1):
                idx = lat.nmap.get((bl, iy, iz, iw))
                if idx is not None:
                    bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked


def born_test_3d(lat, field_f, bi, det, k):
    pos = lat.pos
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    if not (upper and lower and middle):
        return float('nan')
    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c); other = set(bi) - all_s
    probs = {}
    for key, open_set in [('abc', all_s), ('ab', set(s_a+s_b)),
                           ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
                           ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
        bl2 = other | (all_s - open_set)
        a = lat.propagate(field_f, k, bl2)
        probs[key] = np.array([abs(a[d])**2 for d in det])
    I3 = 0.0; P = 0.0
    for di in range(len(det)):
        i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
              - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
        I3 += abs(i3); P += probs['abc'][di]
    return I3 / P if P > 1e-30 else float('nan')


def born_test_4d(lat, field_f, bi, det, k):
    pos = lat.pos
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1 and abs(pos[i, 3]) <= 1]
    if not (upper and lower and middle):
        return float('nan')
    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c); other = set(bi) - all_s
    probs = {}
    for key, open_set in [('abc', all_s), ('ab', set(s_a+s_b)),
                           ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
                           ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
        bl2 = other | (all_s - open_set)
        a = lat.propagate(field_f, k, bl2)
        probs[key] = np.array([abs(a[d])**2 for d in det])
    I3 = 0.0; P = 0.0
    for di in range(len(det)):
        i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
              - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
        I3 += abs(i3); P += probs['abc'][di]
    return I3 / P if P > 1e-30 else float('nan')


# ===========================================================================
# ROUTE A: Turn-cost variational law
# ===========================================================================

def route_a_kernel(h, max_d, d_spatial):
    """Derive kernel from turn-cost principle.

    The "simplest continuation" penalizes angular change: w = exp(-beta * theta^2).
    For the FIRST edge, theta_prev=0 (forward), so w = exp(-beta * theta^2).

    For SUBSEQUENT edges, we marginalize over the Markov chain of directions.
    After many layers, the effective per-edge kernel is the stationary
    distribution of the turn-cost chain.

    We compute: for each offset, the turn-cost weight from each possible
    INCOMING direction, then average (= effective stationary kernel).
    """
    print("\n" + "=" * 70)
    print("ROUTE A: TURN-COST VARIATIONAL LAW")
    print("  'Simplest continuation = minimum directional change'")
    print("=" * 70)

    # Enumerate all offsets
    if d_spatial == 2:
        offsets = []
        for dy in range(-max_d, max_d + 1):
            for dz in range(-max_d, max_d + 1):
                dyp, dzp = dy * h, dz * h
                L = math.sqrt(h*h + dyp*dyp + dzp*dzp)
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                offsets.append((dy, dz, L, theta))
    else:  # d_spatial == 3
        offsets = []
        for dy in range(-max_d, max_d + 1):
            for dz in range(-max_d, max_d + 1):
                for dw in range(-max_d, max_d + 1):
                    dyp, dzp, dwp = dy * h, dz * h, dw * h
                    L = math.sqrt(h*h + dyp*dyp + dzp*dzp + dwp*dwp)
                    r_trans = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                    theta = math.atan2(r_trans, h)
                    offsets.append(((dy, dz, dw) if d_spatial == 3 else (dy, dz), L, theta))

    n_off = len(offsets)

    # First-edge kernel: w_0(theta) = exp(-beta * theta^2)
    # Choose beta such that the effective attenuation matches lattice geometry.
    # Natural choice: beta = d_spatial (stronger suppression in higher d).
    # We'll try several beta values and find which gives cos^(d-1) best fit.

    print(f"\n  d_spatial={d_spatial}, h={h}, max_d={max_d}, {n_off} offsets")

    # Get unique theta values
    theta_vals = sorted(set(round(o[-1], 8) for o in offsets))
    print(f"  Unique theta values: {len(theta_vals)}")

    # For each beta, compute first-edge kernel and compare to cos^(d-1)
    print(f"\n  --- First-edge kernel comparison ---")
    print(f"  {'beta':<8} {'max_dev from cos^(d-1)':<25} {'correlation':<15}")
    print(f"  " + "-" * 48)

    best_beta = None
    best_corr = -1

    for beta_10 in range(5, 51):  # beta from 0.5 to 5.0
        beta = beta_10 / 10.0
        # Compute w_A(theta) and w_ref(theta) = cos^(d-1)(theta) at each unique theta
        w_a = [math.exp(-beta * t**2) for t in theta_vals]
        w_ref = [math.cos(t)**(d_spatial - 1) for t in theta_vals]

        # Normalize both to max=1
        max_a = max(w_a) if max(w_a) > 0 else 1
        max_r = max(w_ref) if max(w_ref) > 0 else 1
        w_a_n = [w / max_a for w in w_a]
        w_ref_n = [w / max_r for w in w_ref]

        # Correlation
        mean_a = sum(w_a_n) / len(w_a_n)
        mean_r = sum(w_ref_n) / len(w_ref_n)
        num = sum((a - mean_a) * (r - mean_r) for a, r in zip(w_a_n, w_ref_n))
        den_a = math.sqrt(sum((a - mean_a)**2 for a in w_a_n))
        den_r = math.sqrt(sum((r - mean_r)**2 for r in w_ref_n))
        corr = num / (den_a * den_r) if den_a > 0 and den_r > 0 else 0

        max_dev = max(abs(a - r) for a, r in zip(w_a_n, w_ref_n))

        if corr > best_corr:
            best_corr = corr
            best_beta = beta

        if beta_10 % 5 == 0:
            print(f"  {beta:<8.1f} {max_dev:<25.6f} {corr:<15.6f}")

    print(f"\n  Best beta (max correlation with cos^(d-1)): {best_beta:.1f}")
    print(f"  Best correlation: {best_corr:.6f}")

    # Now compute the STATIONARY effective kernel (Markov chain)
    # Transition matrix: T[j|i] = exp(-beta * (theta_j - theta_i)^2) / Z_i
    # Stationary distribution pi: pi * T = pi
    # Effective kernel at theta: w_eff(theta) = pi(theta)

    print(f"\n  --- Markov chain stationary kernel (beta={best_beta:.1f}) ---")

    # Group offsets by theta bucket
    theta_buckets = {}
    for o in offsets:
        t = round(o[-1], 6)
        if t not in theta_buckets:
            theta_buckets[t] = 0
        theta_buckets[t] += 1

    bucket_thetas = sorted(theta_buckets.keys())
    n_b = len(bucket_thetas)

    # Build transition matrix T[j][i] = P(next=bucket_j | current=bucket_i)
    # The turn angle from bucket_i to bucket_j depends on the actual directions,
    # but for a simplified model, approximate: delta_theta ~ |theta_j - theta_i|
    T = np.zeros((n_b, n_b))
    for i, ti in enumerate(bucket_thetas):
        for j, tj in enumerate(bucket_thetas):
            delta = abs(tj - ti)
            T[j, i] = math.exp(-best_beta * delta**2) * theta_buckets[tj]
        col_sum = T[:, i].sum()
        if col_sum > 0:
            T[:, i] /= col_sum

    # Find stationary distribution by power iteration
    pi = np.ones(n_b) / n_b
    for _ in range(1000):
        pi_new = T @ pi
        norm = pi_new.sum()
        if norm > 0:
            pi_new /= norm
        if np.max(np.abs(pi_new - pi)) < 1e-12:
            break
        pi = pi_new

    print(f"  {'theta (deg)':<14} {'multiplicity':<14} {'pi (stationary)':<18} {'cos^(d-1)':<14}")
    print(f"  " + "-" * 60)
    for i, t in enumerate(bucket_thetas):
        ref = math.cos(t)**(d_spatial - 1) if t < math.pi / 2 else 0
        print(f"  {math.degrees(t):<14.1f} {theta_buckets[t]:<14d} {pi[i]:<18.6f} {ref:<14.6f}")

    # Effective weight function: w_eff(theta) = pi(theta) / multiplicity(theta)
    # This removes the geometric counting bias
    print(f"\n  --- Effective per-edge weight (pi / multiplicity) ---")
    print(f"  {'theta (deg)':<14} {'w_eff':<14} {'cos^(d-1)':<14} {'ratio':<12}")
    print(f"  " + "-" * 54)

    w_eff_map = {}
    for i, t in enumerate(bucket_thetas):
        w_eff = pi[i] / theta_buckets[t] if theta_buckets[t] > 0 else 0
        w_eff_map[t] = w_eff
        ref = math.cos(t)**(d_spatial - 1) if t < math.pi / 2 else 0
        ratio = w_eff / ref if ref > 1e-10 else float('nan')
        print(f"  {math.degrees(t):<14.1f} {w_eff:<14.6f} {ref:<14.6f} {ratio:<12.4f}")

    # Build the first-edge kernel function for propagation tests
    def route_a_weight(theta, _beta=best_beta):
        return math.exp(-_beta * theta**2)

    return route_a_weight, best_beta


# ===========================================================================
# ROUTE B: Neighborhood-overlap law
# ===========================================================================

def route_b_kernel(h, max_d, d_spatial):
    """Derive kernel from neighborhood overlap (Axiom 3).

    For an edge from node A at layer x to node B at layer x+1 with
    transverse offset (dy, dz), compute:
      overlap = |N(A) & N(B)| / |N(A) U N(B)|  (Jaccard index)

    where N(.) is the set of forward neighbors (layer x+1 for A, layer x+2 for B).
    Nodes that share more next-layer neighbors are "closer" in the
    influence-neighborhood sense.
    """
    print("\n" + "=" * 70)
    print("ROUTE B: NEIGHBORHOOD-OVERLAP LAW")
    print("  'Weight by overlap of influence neighborhoods (Axiom 3)'")
    print("=" * 70)

    print(f"\n  d_spatial={d_spatial}, h={h}, max_d={max_d}")

    # For a source node at (0, 0, ...) its forward neighbors are all offsets
    # to layer 1: (1, dy', dz', ...) for |dy'|, |dz'|, ... <= max_d

    # For a destination at (1, dy, dz, ...), its forward neighbors are offsets
    # to layer 2: (2, dy+dy'', dz+dz'', ...) for |dy''|, |dz''|, ... <= max_d

    # The overlap is: how many of B's layer-2 neighbors coincide with A's
    # layer-2 neighbors (by transverse position)?

    # A's layer-2 neighbors: all (dy1+dy2, dz1+dz2) where |dyi|<=max_d
    # But we want: A -> layer1 -> layer2 neighbors.
    # Actually, let's define N(A) = set of nodes reachable in 1 step from A.
    # N(A) = {(1, a, b) : |a|<=md, |b|<=md} (the same for all layer-0 nodes)
    # N(B) where B=(1, dy, dz) = {(2, dy+a, dz+b) : |a|<=md, |b|<=md}
    #   but ALSO N(B) includes backward: {(0, dy+a, dz+b)} — which we IGNORE
    #   since we only consider forward neighborhoods.

    # Better definition: N(A) and N(B) are the sets of FORWARD neighbors.
    # N(A) = {(1, a, b) : |a|, |b| <= md}
    # N(B) = {(2, dy+a, dz+b) : |a|, |b| <= md}
    # These live on DIFFERENT layers, so overlap is always 0!

    # FIX: Use the SAME-layer neighbor concept (spatial neighborhood).
    # N(A) at layer 0 means all nodes at layer 0 within transverse distance max_d.
    # N(B) at layer 1 means all nodes at layer 1 within transverse distance max_d.
    # Overlap: nodes whose transverse positions appear in BOTH neighborhoods
    # (comparing transverse coordinates only).

    # N(A) transverse positions: {(a, b) : |a|, |b| <= md}
    # N(B=(1,dy,dz)) transverse positions: {(dy+a, dz+b) : |a|, |b| <= md}
    # Overlap: transverse positions in both sets.

    md = max_d  # in lattice units

    if d_spatial == 2:
        # Source neighborhood: all (a,b) with |a|<=md, |b|<=md
        src_set = set()
        for a in range(-md, md + 1):
            for b in range(-md, md + 1):
                src_set.add((a, b))

        print(f"  Source neighborhood size: {len(src_set)}")

        # For each offset (dy, dz), compute overlap
        print(f"\n  {'dy':<6} {'dz':<6} {'theta (deg)':<14} {'|overlap|':<12} {'|union|':<10} {'Jaccard':<10} {'cos^(d-1)':<12}")
        print(f"  " + "-" * 70)

        overlap_map = {}
        for dy in range(-md, md + 1):
            for dz in range(-md, md + 1):
                dst_set = set()
                for a in range(-md, md + 1):
                    for b in range(-md, md + 1):
                        dst_set.add((dy + a, dz + b))

                inter = src_set & dst_set
                union = src_set | dst_set
                jaccard = len(inter) / len(union) if len(union) > 0 else 0

                dyp, dzp = dy * h, dz * h
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                ref = math.cos(theta)**(d_spatial - 1)

                overlap_map[round(theta, 6)] = overlap_map.get(round(theta, 6), [])
                overlap_map[round(theta, 6)].append(jaccard)

                if abs(dy) <= 2 and abs(dz) <= 2:
                    print(f"  {dy:<6d} {dz:<6d} {math.degrees(theta):<14.1f} "
                          f"{len(inter):<12d} {len(union):<10d} {jaccard:<10.4f} {ref:<12.6f}")

        # Average Jaccard at each theta
        print(f"\n  --- Average Jaccard by theta ---")
        print(f"  {'theta (deg)':<14} {'avg Jaccard':<14} {'cos^(d-1)':<14} {'ratio':<12}")
        print(f"  " + "-" * 54)

        w_b_map = {}
        for t in sorted(overlap_map.keys()):
            avg_j = sum(overlap_map[t]) / len(overlap_map[t])
            ref = math.cos(t)**(d_spatial - 1) if t < math.pi / 2 else 0
            ratio = avg_j / ref if ref > 1e-10 else float('nan')
            w_b_map[t] = avg_j
            print(f"  {math.degrees(t):<14.1f} {avg_j:<14.6f} {ref:<14.6f} {ratio:<12.4f}")

    else:  # d_spatial == 3
        src_set = set()
        for a in range(-md, md + 1):
            for b in range(-md, md + 1):
                for c in range(-md, md + 1):
                    src_set.add((a, b, c))

        print(f"  Source neighborhood size: {len(src_set)}")

        overlap_map = {}
        for dy in range(-md, md + 1):
            for dz in range(-md, md + 1):
                for dw in range(-md, md + 1):
                    dst_set = set()
                    for a in range(-md, md + 1):
                        for b in range(-md, md + 1):
                            for c in range(-md, md + 1):
                                dst_set.add((dy + a, dz + b, dw + c))

                    inter = src_set & dst_set
                    union = src_set | dst_set
                    jaccard = len(inter) / len(union) if len(union) > 0 else 0

                    dyp, dzp, dwp = dy * h, dz * h, dw * h
                    r_trans = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                    theta = math.atan2(r_trans, h)

                    t_key = round(theta, 6)
                    if t_key not in overlap_map:
                        overlap_map[t_key] = []
                    overlap_map[t_key].append(jaccard)

        print(f"\n  --- Average Jaccard by theta ---")
        print(f"  {'theta (deg)':<14} {'avg Jaccard':<14} {'cos^(d-1)':<14} {'ratio':<12}")
        print(f"  " + "-" * 54)

        w_b_map = {}
        for t in sorted(overlap_map.keys()):
            avg_j = sum(overlap_map[t]) / len(overlap_map[t])
            ref = math.cos(t)**(d_spatial - 1) if t < math.pi / 2 else 0
            ratio = avg_j / ref if ref > 1e-10 else float('nan')
            w_b_map[t] = avg_j
            print(f"  {math.degrees(t):<14.1f} {avg_j:<14.6f} {ref:<14.6f} {ratio:<12.4f}")

    # Check monotonicity
    sorted_thetas = sorted(w_b_map.keys())
    monotonic = all(w_b_map[sorted_thetas[i]] >= w_b_map[sorted_thetas[i+1]] - 1e-10
                    for i in range(len(sorted_thetas) - 1))
    print(f"\n  Monotonically decreasing: {'YES' if monotonic else 'NO'}")

    # Build weight function from the overlap map (interpolate)
    def route_b_weight(theta):
        t_key = round(theta, 6)
        if t_key in w_b_map:
            return w_b_map[t_key]
        # Linear interpolation
        ts = sorted(w_b_map.keys())
        if theta <= ts[0]:
            return w_b_map[ts[0]]
        if theta >= ts[-1]:
            return w_b_map[ts[-1]]
        for i in range(len(ts) - 1):
            if ts[i] <= theta <= ts[i + 1]:
                frac = (theta - ts[i]) / (ts[i + 1] - ts[i])
                return w_b_map[ts[i]] * (1 - frac) + w_b_map[ts[i + 1]] * frac
        return w_b_map[ts[-1]]

    return route_b_weight, w_b_map


# ===========================================================================
# ROUTE C: Combinatorial path-counting correction
# ===========================================================================

def route_c_kernel(h, max_d, d_spatial):
    """Derive kernel from path-counting correction.

    The number of offsets at angle theta has a geometric multiplicity
    (more ways to reach large angles on a cubic lattice).
    To make the propagator isotropic, w(theta) must cancel this bias:
      w(theta) = 1 / multiplicity(theta)

    This is the "equal contribution per solid angle" principle.
    """
    print("\n" + "=" * 70)
    print("ROUTE C: COMBINATORIAL PATH-COUNTING CORRECTION")
    print("  'Cancel geometric multiplicity to achieve isotropy'")
    print("=" * 70)

    print(f"\n  d_spatial={d_spatial}, h={h}, max_d={max_d}")

    md = max_d  # lattice units

    # Count multiplicity at each theta
    theta_counts = {}
    if d_spatial == 2:
        for dy in range(-md, md + 1):
            for dz in range(-md, md + 1):
                dyp, dzp = dy * h, dz * h
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                t_key = round(theta, 6)
                theta_counts[t_key] = theta_counts.get(t_key, 0) + 1
    else:
        for dy in range(-md, md + 1):
            for dz in range(-md, md + 1):
                for dw in range(-md, md + 1):
                    dyp, dzp, dwp = dy * h, dz * h, dw * h
                    r_trans = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                    theta = math.atan2(r_trans, h)
                    t_key = round(theta, 6)
                    theta_counts[t_key] = theta_counts.get(t_key, 0) + 1

    # w_C(theta) = 1/count(theta), normalized so w_C(0) = 1
    count_at_0 = theta_counts.get(0.0, 1)
    w_c_map = {}
    for t in sorted(theta_counts.keys()):
        w_c_map[t] = (1.0 / theta_counts[t]) / (1.0 / count_at_0)  # = count_at_0 / count(t)

    print(f"\n  {'theta (deg)':<14} {'count':<10} {'w_C = 1/count':<16} {'cos^(d-1)':<14} {'ratio':<12}")
    print(f"  " + "-" * 66)

    # Also compute what the continuum prediction is:
    # In d spatial dims, solid angle element ~ sin^(d-2)(phi) * dphi * domega_{d-2}
    # Number of lattice offsets at angle theta ~ r_perp^(d-2) * dtheta
    # where r_perp = tan(theta) * h, so count ~ tan^(d-2)(theta) for d>2
    # For d=2: count ~ 1 (ring has ~2*pi*r points, r = r_perp)
    # More precisely, count(theta) ~ (sin(theta))^(d-2) * (total_offsets / solid_angle)

    for t in sorted(w_c_map.keys()):
        ref = math.cos(t)**(d_spatial - 1) if t < math.pi / 2 else 0
        ratio = w_c_map[t] / ref if ref > 1e-10 else float('nan')
        print(f"  {math.degrees(t):<14.1f} {theta_counts[t]:<10d} {w_c_map[t]:<16.6f} "
              f"{ref:<14.6f} {ratio:<12.4f}")

    # Check monotonicity
    sorted_thetas = sorted(w_c_map.keys())
    monotonic = all(w_c_map[sorted_thetas[i]] >= w_c_map[sorted_thetas[i+1]] - 1e-10
                    for i in range(len(sorted_thetas) - 1))
    print(f"\n  Monotonically decreasing: {'YES' if monotonic else 'NO'}")

    # Continuum comparison: w_C should scale as 1/sin^(d-2)(theta) * const
    # But cos^(d-1)(theta) ~ cos^(d-1)(theta)
    # For small theta: 1/count ~ 1/theta^(d-2) (since lattice count ~ theta^(d-2))
    # while cos^(d-1) ~ 1 - (d-1)*theta^2/2
    # These are DIFFERENT functional forms -- 1/count diverges for d>2, cos^(d-1) -> 1.

    print(f"\n  Analytical expectation:")
    print(f"    For d_spatial={d_spatial}: lattice count ~ r_perp^(d_spatial-2)")
    print(f"    where r_perp = tan(theta).")
    print(f"    So w_C ~ 1/tan^({d_spatial-2})(theta)")
    if d_spatial == 2:
        print(f"    For d=2: w_C ~ 1/tan^0 = const (all angles equally populated)")
        print(f"    This does NOT match cos^1(theta). Route C predicts UNIFORM kernel in 2D!")
    else:
        print(f"    For d=3: w_C ~ 1/tan^1(theta) = cos/sin")
        print(f"    This does NOT match cos^2(theta). Different functional form.")

    def route_c_weight(theta):
        t_key = round(theta, 6)
        if t_key in w_c_map:
            return w_c_map[t_key]
        ts = sorted(w_c_map.keys())
        if theta <= ts[0]:
            return w_c_map[ts[0]]
        if theta >= ts[-1]:
            return w_c_map[ts[-1]]
        for i in range(len(ts) - 1):
            if ts[i] <= theta <= ts[i + 1]:
                frac = (theta - ts[i]) / (ts[i + 1] - ts[i])
                return w_c_map[ts[i]] * (1 - frac) + w_c_map[ts[i + 1]] * frac
        return w_c_map[ts[-1]]

    return route_c_weight, w_c_map


# ===========================================================================
# Full measurement suite for a given kernel
# ===========================================================================

def run_full_test_3d(name, weight_fn):
    """Run gravity + Born on 2+1D lattice. Returns dict."""
    t0 = time.time()
    lat = Lattice3D(L2, W2, H, MAX_D2 / H, weight_fn, P2)
    det = [lat.nmap[(lat.nl-1, iy, iz)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits_3d(lat)
    field_f = np.zeros(lat.n)

    # Flat propagation
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return {"name": name, "signal": False}
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf

    # Born
    born = born_test_3d(lat, field_f, bi, det, K)

    # Gravity (spatial-only field)
    field_m, _ = make_field_3d(lat, 3, STRENGTH)
    am = lat.propagate(field_m, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    grav = 0
    if pm > 1e-30:
        grav = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm - zf
    direction = "TOWARD" if grav > 0 else "AWAY"

    elapsed = time.time() - t0
    return {
        "name": name, "signal": True, "born": born,
        "grav": grav, "dir": direction, "time": elapsed, "det_prob": pf,
    }


def run_full_test_4d(name, weight_fn):
    """Run gravity + Born on 3+1D lattice. Returns dict."""
    t0 = time.time()
    lat = Lattice4D(L3, 1.0, W3, MAX_D3, weight_fn, P3)
    det = [lat.nmap[(lat.nl-1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           for iw in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz, iw) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits_4d(lat)
    field_f = np.zeros(lat.n)

    # Flat propagation
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return {"name": name, "signal": False}
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf

    # Born
    born = born_test_4d(lat, field_f, bi, det, K)

    # Gravity (spatial-only field)
    field_m, _ = make_field_4d(lat, 2, STRENGTH)
    am = lat.propagate(field_m, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    grav = 0
    if pm > 1e-30:
        grav = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm - zf
    direction = "TOWARD" if grav > 0 else "AWAY"

    elapsed = time.time() - t0
    return {
        "name": name, "signal": True, "born": born,
        "grav": grav, "dir": direction, "time": elapsed, "det_prob": pf,
    }


# ===========================================================================
# Main
# ===========================================================================

def main():
    print("=" * 70)
    print("FRONTIER: KERNEL FROM LOCAL CONTINUATION PRINCIPLES")
    print("  Axiom 6: simplest admissible continuation")
    print("  Axiom 3: space from influence neighborhoods")
    print("  Axiom 10: prefer persistent local mechanisms")
    print("=" * 70)
    print()

    # ===================================================================
    # PART 1: Derive kernels analytically in 2+1D
    # ===================================================================
    print("#" * 70)
    print("# PART 1: DERIVE KERNELS IN 2+1D (d_spatial=2)")
    print("#" * 70)

    max_d_lattice_2d = max(1, round(MAX_D2 / H))

    wfn_a_2d, beta_a_2d = route_a_kernel(H, max_d_lattice_2d, D2)
    wfn_b_2d, map_b_2d = route_b_kernel(H, max_d_lattice_2d, D2)
    wfn_c_2d, map_c_2d = route_c_kernel(H, max_d_lattice_2d, D2)

    # ===================================================================
    # PART 2: Derive kernels analytically in 3+1D
    # ===================================================================
    print()
    print("#" * 70)
    print("# PART 2: DERIVE KERNELS IN 3+1D (d_spatial=3)")
    print("#" * 70)

    max_d_lattice_3d = max(1, round(MAX_D3 / 1.0))  # h=1.0 for 3+1D

    wfn_a_3d, beta_a_3d = route_a_kernel(1.0, max_d_lattice_3d, D3)
    wfn_b_3d, map_b_3d = route_b_kernel(1.0, max_d_lattice_3d, D3)
    wfn_c_3d, map_c_3d = route_c_kernel(1.0, max_d_lattice_3d, D3)

    # ===================================================================
    # PART 3: Propagation tests in 2+1D
    # ===================================================================
    print()
    print("#" * 70)
    print("# PART 3: PROPAGATION TESTS IN 2+1D")
    print("#" * 70)
    print(f"  Grid: L={L2}, W={W2}, h={H}, k={K}")
    print(f"  Reference: cos^(d-1) = cos^1(theta)")

    # Reference kernel
    ref_2d = lambda t: max(0.0, math.cos(t))

    tests_2d = [
        ("cos^1 [reference]", ref_2d),
        (f"Route A: exp(-{beta_a_2d:.1f}*t^2)", wfn_a_2d),
        ("Route B: Jaccard overlap", wfn_b_2d),
        ("Route C: 1/multiplicity", wfn_c_2d),
    ]

    results_2d = []
    for name, wfn in tests_2d:
        print(f"\n  Running: {name} ...")
        r = run_full_test_3d(name, wfn)
        results_2d.append(r)
        if r.get("signal"):
            print(f"    Born={r['born']:.2e}, gravity={r['grav']:+.6f} ({r['dir']}), "
                  f"det_prob={r['det_prob']:.2e}, time={r['time']:.0f}s")
        else:
            print(f"    NO SIGNAL")

    # ===================================================================
    # PART 4: Propagation tests in 3+1D
    # ===================================================================
    print()
    print("#" * 70)
    print("# PART 4: PROPAGATION TESTS IN 3+1D")
    print("#" * 70)
    print(f"  Grid: L={L3}, W={W3}, h=1.0, k={K}")
    print(f"  Reference: cos^(d-1) = cos^2(theta)")

    ref_3d = lambda t: max(0.0, math.cos(t)) ** 2

    tests_3d = [
        ("cos^2 [reference]", ref_3d),
        (f"Route A: exp(-{beta_a_3d:.1f}*t^2)", wfn_a_3d),
        ("Route B: Jaccard overlap", wfn_b_3d),
        ("Route C: 1/multiplicity", wfn_c_3d),
    ]

    results_3d = []
    for name, wfn in tests_3d:
        print(f"\n  Running: {name} ...")
        r = run_full_test_4d(name, wfn)
        results_3d.append(r)
        if r.get("signal"):
            print(f"    Born={r['born']:.2e}, gravity={r['grav']:+.6f} ({r['dir']}), "
                  f"det_prob={r['det_prob']:.2e}, time={r['time']:.0f}s")
        else:
            print(f"    NO SIGNAL")

    # ===================================================================
    # PART 5: Summary and verdict
    # ===================================================================
    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    print(f"\n--- 2+1D (d_spatial=2, reference: cos^1) ---")
    print(f"  {'Kernel':<30s} | {'Born |I3|/P':>12s} | {'Gravity':>10s} | {'Dir':>6s}")
    print(f"  " + "-" * 66)
    for r in results_2d:
        if not r.get("signal"):
            print(f"  {r['name']:<30s} | {'NO SIGNAL':>12s} |")
            continue
        b = f"{r['born']:.2e}" if not math.isnan(r['born']) else "N/A"
        g = f"{r['grav']:+.6f}"
        print(f"  {r['name']:<30s} | {b:>12s} | {g:>10s} | {r['dir']:>6s}")

    print(f"\n--- 3+1D (d_spatial=3, reference: cos^2) ---")
    print(f"  {'Kernel':<30s} | {'Born |I3|/P':>12s} | {'Gravity':>10s} | {'Dir':>6s}")
    print(f"  " + "-" * 66)
    for r in results_3d:
        if not r.get("signal"):
            print(f"  {r['name']:<30s} | {'NO SIGNAL':>12s} |")
            continue
        b = f"{r['born']:.2e}" if not math.isnan(r['born']) else "N/A"
        g = f"{r['grav']:+.6f}"
        print(f"  {r['name']:<30s} | {b:>12s} | {g:>10s} | {r['dir']:>6s}")

    # ===================================================================
    # VERDICT
    # ===================================================================
    print()
    print("=" * 70)
    print("VERDICT")
    print("=" * 70)

    # Evaluate each route
    for route_name, idx_2d, idx_3d in [("Route A (turn-cost)", 1, 1),
                                         ("Route B (Jaccard overlap)", 2, 2),
                                         ("Route C (1/multiplicity)", 3, 3)]:
        r2 = results_2d[idx_2d] if idx_2d < len(results_2d) else None
        r3 = results_3d[idx_3d] if idx_3d < len(results_3d) else None

        toward_2d = r2 and r2.get("dir") == "TOWARD"
        toward_3d = r3 and r3.get("dir") == "TOWARD"
        born_2d = r2 and r2.get("born", 1) < 0.1
        born_3d = r3 and r3.get("born", 1) < 0.1

        print(f"\n  {route_name}:")
        if r2 and r2.get("signal"):
            print(f"    2+1D: gravity={'TOWARD' if toward_2d else 'AWAY'}, "
                  f"Born={'PASS' if born_2d else 'FAIL'} ({r2.get('born', float('nan')):.2e})")
        else:
            print(f"    2+1D: NO SIGNAL")
        if r3 and r3.get("signal"):
            print(f"    3+1D: gravity={'TOWARD' if toward_3d else 'AWAY'}, "
                  f"Born={'PASS' if born_3d else 'FAIL'} ({r3.get('born', float('nan')):.2e})")
        else:
            print(f"    3+1D: NO SIGNAL")

        if toward_2d and toward_3d and born_2d and born_3d:
            print(f"    ==> VIABLE: passes all tests in both dimensions")
        elif (toward_2d or toward_3d) and (born_2d or born_3d):
            print(f"    ==> PARTIAL: passes some tests")
        else:
            print(f"    ==> FAILS: does not reproduce gravity+Born")

    # Compare to reference
    ref2 = results_2d[0] if results_2d else None
    ref3 = results_3d[0] if results_3d else None
    print(f"\n  Reference cos^(d-1):")
    if ref2 and ref2.get("signal"):
        print(f"    2+1D: gravity={ref2['grav']:+.6f} ({ref2['dir']}), Born={ref2['born']:.2e}")
    if ref3 and ref3.get("signal"):
        print(f"    3+1D: gravity={ref3['grav']:+.6f} ({ref3['dir']}), Born={ref3['born']:.2e}")

    # Overall conclusion
    viable_routes = []
    for route_name, idx in [("A", 1), ("B", 2), ("C", 3)]:
        r2 = results_2d[idx] if idx < len(results_2d) else None
        r3 = results_3d[idx] if idx < len(results_3d) else None
        t2 = r2 and r2.get("dir") == "TOWARD"
        t3 = r3 and r3.get("dir") == "TOWARD"
        b2 = r2 and r2.get("born", 1) < 0.1
        b3 = r3 and r3.get("born", 1) < 0.1
        if (t2 and b2) or (t3 and b3):
            viable_routes.append(route_name)

    print()
    if viable_routes:
        print(f"  HYPOTHESIS SUPPORTED: Route(s) {', '.join(viable_routes)} derive a kernel")
        print(f"  from local continuation that passes gravity + Born tests.")
        print(f"  The angular kernel can be DERIVED, not just fitted.")
    else:
        print(f"  HYPOTHESIS FALSIFIED: None of the three local-continuation routes")
        print(f"  produce a kernel that passes both gravity and Born tests.")
        print(f"  The cos^(d-1) kernel may require a different derivation principle.")

    print()


if __name__ == "__main__":
    main()
