#!/usr/bin/env python3
"""
Irregular-Graph Directional Observable Probe
=============================================

Goal:
  Find one graph-native, sign-selective dynamical observable on the
  endogenous lane |psi|^2 -> Phi -> H, or prove a strong blocker.

This is intentionally NOT a shell-profile probe. It measures short-time
wavefunction response on the retained irregular graph families under the
endogenous self-gravity loop.

Tested couplings:
  - identity: H_diag = mass * parity + mass * Phi      (retired control)
  - parity:   H_diag = (mass + Phi) * parity           (correct staggered scalar)

Observables:
  O1  depth shift        Δ<depth> relative to free evolution
  O2  signed cut flux    inward-minus-outward current across BFS depth cuts
  O3  local current bias inward current around the source-adjacent frontier

Sign-selective success means a metric changes sign between identity and parity
coupling on the same graph family at the same operating point, without any
external +/-Phi injection.

If no metric separates robustly across the retained families, this script
reports a blocker rather than forcing a victory.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass

import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve

from frontier_staggered_self_gravity import (
    MASS,
    MU2,
    DT,
    G_SELF,
    _bfs,
    _laplacian,
    _solve_phi,
    make_growing,
    make_layered_cycle,
    make_random_geometric,
)


N_STEPS = 8
G_SWEEP = (10.0, 50.0, 100.0)
SIGMA = 0.65
K0 = 0.25


@dataclass(frozen=True)
class Result:
    family: str
    g: float
    steps: int
    coupling: str
    depth_shift: float
    cut_flux: float
    frontier_bias: float
    norm: float


def _build_h(pos, colors, adj, mass, phi, coupling: str):
    n = len(pos)
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(colors == 0, 1.0, -1.0)
    if coupling == "parity":
        H.setdiag((mass + phi) * parity)
    elif coupling == "identity":
        H.setdiag(mass * parity + mass * phi)
    else:
        raise ValueError(coupling)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            hop = -0.5j * w
            H[i, j] += hop
            H[j, i] += np.conj(hop)
    return H.tocsr()


def _cn_step(H, psi):
    n = H.shape[0]
    ap = (speye(n, format="csc") + 1j * H * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def _offcenter_state(pos, src, tgt):
    center = pos[tgt]
    rel = pos - center
    coord = rel[:, 0] + 0.25 * rel[:, 1]
    psi = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / SIGMA**2) * np.exp(1j * K0 * coord)
    psi = psi.astype(complex)
    return psi / np.linalg.norm(psi)


def _farthest_node(pos, src):
    d = np.linalg.norm(pos - pos[src], axis=1)
    return int(np.argmax(d))


def _depth_expect(depth, psi):
    rho = np.abs(psi) ** 2
    rho /= max(np.sum(rho), 1e-30)
    return float(np.sum(rho * depth))


def _signed_cut_flux(adj, depth, psi, H):
    total = 0.0
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            di = depth[i]
            dj = depth[j]
            if not np.isfinite(di) or not np.isfinite(dj) or di == dj:
                continue
            J = 2.0 * np.imag(np.conj(psi[i]) * H[i, j] * psi[j])
            # Positive = inward current toward smaller BFS depth.
            total += J if dj < di else -J
    return float(total)


def _frontier_bias(adj, depth, psi, H):
    src_depth = 0.0
    inward = 0.0
    outward = 0.0
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            di = depth[i]
            dj = depth[j]
            if not np.isfinite(di) or not np.isfinite(dj) or di == dj:
                continue
            if min(di, dj) != src_depth:
                continue
            J = 2.0 * np.imag(np.conj(psi[i]) * H[i, j] * psi[j])
            if dj > di:
                outward += J
            else:
                inward += J
    return float(inward - outward)


def _run_family(name, pos, colors, adj, src):
    depth = _bfs(adj, src, len(pos))
    tgt = _farthest_node(pos, src)
    psi0 = _offcenter_state(pos, src, tgt)
    L = _laplacian(pos, adj, len(pos))

    rows: list[Result] = []
    for g_val in G_SWEEP:
        # Free baseline at the same short time
        psi_free = psi0.copy()
        H_free = _build_h(pos, colors, adj, MASS, np.zeros(len(pos)), coupling="identity")
        for _ in range(N_STEPS):
            psi_free = _cn_step(H_free, psi_free)
        free_depth = _depth_expect(depth, psi_free)
        free_flux = _signed_cut_flux(adj, depth, psi_free, H_free)
        free_bias = _frontier_bias(adj, depth, psi_free, H_free)

        for coupling in ("identity", "parity"):
            psi = psi0.copy()
            for _ in range(N_STEPS):
                rho = np.abs(psi) ** 2
                phi = _solve_phi(L, len(pos), g_val * rho)
                H = _build_h(pos, colors, adj, MASS, phi, coupling=coupling)
                psi = _cn_step(H, psi)
            rho = np.abs(psi) ** 2
            phi = _solve_phi(L, len(pos), g_val * rho)
            H = _build_h(pos, colors, adj, MASS, phi, coupling=coupling)
            rows.append(
                Result(
                    family=name,
                    g=g_val,
                    steps=N_STEPS,
                    coupling=coupling,
                    depth_shift=_depth_expect(depth, psi) - free_depth,
                    cut_flux=_signed_cut_flux(adj, depth, psi, H) - free_flux,
                    frontier_bias=_frontier_bias(adj, depth, psi, H) - free_bias,
                    norm=float(np.linalg.norm(psi)),
                )
            )
    return rows


def _print_rows(rows):
    print(f"{'family':<16s} {'G':>5s} {'cpl':<8s} {'dDepth':>10s} {'dFlux':>11s} {'dBias':>11s} {'norm':>9s}")
    print("-" * 74)
    for r in rows:
        print(
            f"{r.family:<16s} {r.g:5.1f} {r.coupling:<8s} "
            f"{r.depth_shift:+10.4e} {r.cut_flux:+11.4e} {r.frontier_bias:+11.4e} {r.norm:9.6f}"
        )


def _sign(x):
    if abs(x) < 1e-12:
        return 0
    return 1 if x > 0 else -1


def main():
    t0 = time.time()
    print("=" * 88)
    print("IRREGULAR-GRAPH DIRECTIONAL OBSERVABLE PROBE")
    print("=" * 88)
    print("Endogenous lane: |psi|^2 -> Phi -> H")
    print("Observable candidates: short-time depth shift, signed cut flux, frontier current bias")
    print("Coupling comparison: identity (retired control) vs parity (correct staggered scalar)")
    print()

    families = [
        make_random_geometric(seed=42, side=6),
        make_growing(seed=42, n_target=48),
        make_layered_cycle(seed=42, layers=6, width=4),
    ]

    all_rows: list[Result] = []
    for name, pos, colors, adj, n, src in families:
        rows = _run_family(name, pos, colors, adj, src)
        all_rows.extend(rows)
        print(f"\nFAMILY: {name}  n={n}  src={src}")
        _print_rows(rows)

    print("\nSIGN-SELECTION CHECK")
    print("-" * 88)
    for metric in ("depth_shift", "cut_flux", "frontier_bias"):
        hits = 0
        total = 0
        for fam in {r.family for r in all_rows}:
            fam_rows = [r for r in all_rows if r.family == fam]
            for g_val in G_SWEEP:
                id_r = next(r for r in fam_rows if r.g == g_val and r.coupling == "identity")
                pa_r = next(r for r in fam_rows if r.g == g_val and r.coupling == "parity")
                s_id = _sign(getattr(id_r, metric))
                s_pa = _sign(getattr(pa_r, metric))
                total += 1
                if s_id != 0 and s_pa != 0 and s_id != s_pa:
                    hits += 1
        print(f"{metric:<16s}: {hits}/{total} sign-separated parity-vs-identity cases")

    print("\nINTERPRETATION")
    print("- If a metric has high sign-separation count, it is a candidate directional observable.")
    print("- If counts stay near zero or flip by family/G, the endogenous lane does not yet have a frozen sign-selective observable.")
    print(f"Time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
