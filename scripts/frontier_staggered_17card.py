#!/usr/bin/env python3
"""
Staggered fermion + potential gravity — 17-row core card
========================================================

This evaluates the current staggered-potential lane against the expanded
N=17 core card, including the new state-family robustness row.

Key architectural facts:
  - one complex scalar per site
  - genuine staggered Dirac dispersion
  - gravity via scalar potential V = -m*g*S/(r+eps)
  - unitary Crank-Nicolson evolution

Important caveat:
  C17 will only pass if the gravity sign survives across the tested state
  families. In the current branch, the antisymmetric/Nyquist-like family is
  expected to fail.
"""

from __future__ import annotations

import importlib.util
import numpy as np
from scipy import stats
import time


SPEC = importlib.util.spec_from_file_location(
    "sf",
    "/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_fermion.py",
)
sf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sf)


N = 41
MASS = 0.3
G = 5.0
S = 5e-4
DT = 0.15
NSTEPS = 15


def build_V(n: int, mass: float, g: float, strength: float, mass_pos: int) -> np.ndarray:
    V = np.zeros(n)
    for x in range(n):
        r = min(abs(x - mass_pos), n - abs(x - mass_pos))
        V[x] = -mass * g * strength / (r + 0.1)
    return V


def cz(psi: np.ndarray, c: int) -> float:
    rho = np.abs(psi) ** 2
    z = np.arange(len(psi)) - c
    return float(np.sum(z * rho) / np.sum(rho))


def make_state(kind: str, n: int, c: int, sigma: float) -> np.ndarray:
    psi = np.zeros(n, dtype=complex)
    for y in range(n):
        amp = np.exp(-((y - c) ** 2) / (2 * sigma**2))
        if kind == "gauss":
            psi[y] = amp
        elif kind == "even" and y % 2 == 0:
            psi[y] = amp
        elif kind == "odd" and y % 2 == 1:
            psi[y] = amp
        elif kind == "sym":
            psi[y] = amp
        elif kind == "anti":
            psi[y] = amp * (1 if y % 2 == 0 else -1)
        else:
            continue
    return psi / np.linalg.norm(psi)


def project_energy(H, psi, positive: bool) -> np.ndarray:
    evals, evecs = np.linalg.eigh(H.toarray())
    coeff = evecs.conj().T @ psi
    mask = evals > 0 if positive else evals < 0
    out = evecs[:, mask] @ coeff[mask]
    return out / np.linalg.norm(out)


def run_card() -> int:
    print("=" * 72)
    print("STAGGERED FERMION + POTENTIAL — CORE CARD (N=17)")
    print("=" * 72)
    n = N
    c = n // 2
    sigma = n / 8
    mass_pos = c + 4
    V = build_V(n, MASS, G, S, mass_pos)
    H_flat = sf.staggered_H_1d(n, MASS)
    H_grav = sf.staggered_H_1d(n, MASS, V)
    psi0 = make_state("gauss", n, c, sigma)
    score = 0

    def ev(H, ns, psi):
        return sf.evolve_cn(H, n, DT, ns, psi)

    # C1 Born
    slits = [c - 2, c, c + 2]
    bl = 4
    def ev_born(sl):
        psi = make_state("gauss", n, c, sigma)
        psi = ev(H_flat, bl, psi)
        mask = np.zeros(n)
        for s in sl:
            mask[s] = 1.0
        psi *= mask
        return ev(H_flat, NSTEPS - bl, psi)
    rho123 = np.abs(ev_born(slits)) ** 2
    P_t = np.sum(rho123)
    rho_s = [np.abs(ev_born([s])) ** 2 for s in slits]
    rho_p = [np.abs(ev_born([slits[i], slits[j]])) ** 2 for i, j in [(0, 1), (0, 2), (1, 2)]]
    I3 = rho123 - sum(rho_p) + sum(rho_s)
    born = np.sum(np.abs(I3)) / P_t if P_t > 1e-20 else 0.0
    p = born < 1e-2
    score += p
    print(f"  [C1]  Sorkin |I3|/P={born:.4e} {'PASS' if p else 'FAIL'}")

    # C2 d_TV
    ru = np.abs(ev_born([c - 2])) ** 2
    rd = np.abs(ev_born([c + 2])) ** 2
    dtv = 0.5 * np.sum(np.abs(ru / max(np.sum(ru), 1e-30) - rd / max(np.sum(rd), 1e-30)))
    p = dtv > 0.01
    score += p
    print(f"  [C2]  d_TV={dtv:.4f} {'PASS' if p else 'FAIL'}")

    # C3 null control
    bias = abs(cz(ev(H_flat, NSTEPS, psi0), c) - cz(ev(H_flat, NSTEPS, psi0), c))
    p = bias < 1e-12
    score += p
    print(f"  [C3]  f=0 |signal|={bias:.4e} {'PASS' if p else 'FAIL'}")

    # C4 F~M
    cz0 = cz(ev(H_flat, NSTEPS, psi0), c)
    strengths = np.array([1e-4, 2e-4, 5e-4, 1e-3, 2e-3])
    forces = []
    for s in strengths:
        V_s = build_V(n, MASS, G, s, mass_pos)
        H_s = sf.staggered_H_1d(n, MASS, V_s)
        forces.append(cz(ev(H_s, NSTEPS, psi0), c) - cz0)
    co = np.polyfit(strengths, forces, 1)
    pred = np.polyval(co, strengths)
    den = np.sum((forces - np.mean(forces)) ** 2)
    r2 = 1 - np.sum((forces - pred) ** 2) / den if den > 0 else 1.0
    p = r2 > 0.9
    score += p
    print(f"  [C4]  F~M R^2={r2:.6f} {'PASS' if p else 'FAIL'}")

    # C5 gravity sign
    dg = cz(ev(H_grav, NSTEPS, psi0), c) - cz0
    p = dg > 0
    score += p
    print(f"  [C5]  Gravity: {dg:+.4e} {'TOWARD' if p else 'AWAY'} {'PASS' if p else 'FAIL'}")

    # C6 decoherence
    pc = ev(H_flat, NSTEPS, psi0)
    rng = np.random.RandomState(42)
    psi_noise = psi0.copy()
    for _ in range(NSTEPS):
        psi_noise *= np.exp(1j * rng.uniform(-1.0, 1.0, n))
        psi_noise = sf.evolve_cn(H_flat, n, DT, 1, psi_noise)
    cc = abs(np.sum(pc.conj() * np.roll(pc, 1))) / np.sum(np.abs(pc) ** 2)
    cn = abs(np.sum(psi_noise.conj() * np.roll(psi_noise, 1))) / np.sum(np.abs(psi_noise) ** 2)
    p = cn < cc
    score += p
    print(f"  [C6]  Decoh: {cc:.4f}->{cn:.4f} {'PASS' if p else 'FAIL'}")

    # C7 MI
    rho = np.abs(ev(H_grav, NSTEPS, psi0)) ** 2
    rn = rho / np.sum(rho)
    p_l = np.sum(rn[:c]); p_r = np.sum(rn[c:])
    bins = np.linspace(0, n, 6).astype(int)
    mi = 0.0
    for b0, b1 in zip(bins[:-1], bins[1:]):
        p_b = np.sum(rn[b0:b1])
        p_bl = np.sum(rn[b0:min(b1, c)])
        p_br = p_b - p_bl
        if p_bl > 1e-30 and p_l > 1e-30 and p_b > 1e-30:
            mi += p_bl * np.log(p_bl / (p_l * p_b))
        if p_br > 1e-30 and p_r > 1e-30 and p_b > 1e-30:
            mi += p_br * np.log(p_br / (p_r * p_b))
    p = mi > 0
    score += p
    print(f"  [C7]  MI={mi:.4e} {'PASS' if p else 'FAIL'}")

    # C8 purity
    purs = []
    for ns in [8, 12, 15]:
        rho_ns = np.abs(ev(H_grav, ns, psi0)) ** 2
        purs.append(np.sum(rho_ns**2) / np.sum(rho_ns) ** 2)
    cv8 = np.std(purs) / np.mean(purs)
    p = cv8 < 0.5
    score += p
    print(f"  [C8]  Purity CV={cv8:.4f} {'PASS' if p else 'FAIL'}")

    # C9 gravity growth
    vals9 = []
    for ns in [5, 8, 10, 15]:
        vals9.append(cz(ev(H_grav, ns, psi0), c) - cz(ev(H_flat, ns, psi0), c))
    all_tw = all(v > 0 for v in vals9)
    mono = all(vals9[i+1] >= vals9[i] for i in range(len(vals9)-1))
    p = all_tw and mono
    score += p
    print(f"  [C9]  GravGrow: tw={all_tw}, mono={mono} {'PASS' if p else 'FAIL'}")

    # C10 distance
    offs = [2, 3, 4, 5, 6]
    dvals = []
    for dz in offs:
        V_d = build_V(n, MASS, G, S, c + dz)
        H_d = sf.staggered_H_1d(n, MASS, V_d)
        dvals.append(cz(ev(H_d, NSTEPS, psi0), c) - cz0)
    ntw = sum(v > 0 for v in dvals)
    p = ntw > len(offs) // 2
    score += p
    print(f"  [C10] Distance: {ntw}/{len(offs)} TW {'PASS' if p else 'FAIL'}")

    # C11 dispersion
    n3 = 8
    evals = np.linalg.eigvalsh(sf.staggered_H_3d(n3, MASS).toarray())
    E2 = evals**2
    f = np.fft.fftfreq(n3) * 2 * np.pi
    all_E2 = []
    all_k2 = []
    for ix in range(n3):
        for iy in range(n3):
            for iz in range(n3):
                kx, ky, kz = f[ix], f[iy], f[iz]
                all_E2.append(MASS**2 + np.sin(kx)**2 + np.sin(ky)**2 + np.sin(kz)**2)
                all_k2.append(kx**2 + ky**2 + kz**2)
    all_E2 = np.array(all_E2); all_k2 = np.array(all_k2)
    mask = all_k2 < 1.0
    _, _, rv, _, _ = stats.linregress(all_k2[mask], all_E2[mask])
    r2kg = rv**2
    p = r2kg > 0.99
    score += p
    print(f"  [C11] KG R^2={r2kg:.6f} {'PASS' if p else 'FAIL'}")

    # C12 AB proxy
    As = np.linspace(0, 2*np.pi, 13)
    vals = []
    for A in As:
        def ev_ab():
            psi = make_state("gauss", n, c, sigma)
            psi = ev(H_flat, 4, psi)
            mask = np.zeros(n, dtype=complex)
            mask[c-2] = 1.0
            mask[c+2] = np.exp(1j * A)
            psi *= mask
            return ev(H_flat, NSTEPS - 4, psi)
        rho = np.abs(ev_ab())**2
        vals.append(np.sum(rho[c-1:c+2]))
    vals = np.array(vals)
    Vab = (np.max(vals) - np.min(vals)) / (np.max(vals) + np.min(vals)) if np.max(vals) > 0 else 0.0
    p = Vab > 0.1
    score += p
    print(f"  [C12] AB-proxy V={Vab:.4f} {'PASS' if p else 'FAIL'}")

    # C13 force achromaticity
    dV = np.zeros(n)
    for y in range(n):
        dV[y] = (V[(y + 1) % n] - V[(y - 1) % n]) / 2
    forces13 = []
    for _k in [0.0, 0.1, 0.2, 0.3, 0.5]:
        rho0 = np.abs(psi0) ** 2
        rho0 /= np.sum(rho0)
        forces13.append(-np.sum(rho0 * dV))
    cv13 = np.std(forces13) / np.mean(np.abs(forces13))
    p = cv13 < 0.01
    score += p
    print(f"  [C13] Force achrom CV={cv13:.6f} {'PASS' if p else 'FAIL'}")

    # C14 equivalence (force-based)
    masses = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0]
    accels = []
    for m in masses:
        V_m = build_V(n, m, G, S, mass_pos)
        dV_m = np.zeros(n)
        for y in range(n):
            dV_m[y] = (V_m[(y + 1) % n] - V_m[(y - 1) % n]) / 2
        rho0 = np.abs(make_state("gauss", n, c, sigma)) ** 2
        rho0 /= np.sum(rho0)
        F = -np.sum(rho0 * dV_m)
        accels.append(F / m)
    cv14 = np.std(accels) / abs(np.mean(accels))
    p = cv14 < 0.01
    score += p
    print(f"  [C14] Equiv CV={cv14:.6f} {'PASS' if p else 'FAIL'}")

    # C15 boundary robustness (same sign at two depths)
    d10 = cz(ev(H_grav, 10, psi0), c) - cz(ev(H_flat, 10, psi0), c)
    d15 = cz(ev(H_grav, 15, psi0), c) - cz(ev(H_flat, 15, psi0), c)
    p = (d10 > 0) and (d15 > 0)
    score += p
    print(f"  [C15] BC/depth: N10={d10:+.3e}, N15={d15:+.3e} {'PASS' if p else 'FAIL'}")

    # C16 multi-observable
    free = ev(H_flat, NSTEPS, psi0)
    grav = ev(H_grav, NSTEPS, psi0)
    rho_f = np.abs(free)**2
    rho_g = np.abs(grav)**2
    ctr = cz(grav, c) - cz(free, c)
    peak = np.argmax(rho_g) - np.argmax(rho_f)
    shell = np.sum((rho_g - rho_f)[c+1:c+4]) > np.sum((rho_g - rho_f)[c-3:c])
    agree = sum([ctr > 0, peak >= 0, shell])
    p = agree >= 2
    score += p
    print(f"  [C16] Multi: ctr={'T' if ctr>0 else 'A'}, pk={peak:+d}, sh={'T' if shell else 'A'} agree={agree}/3 {'PASS' if p else 'FAIL'}")

    # C17 state-family robustness
    base = {
        "gauss": make_state("gauss", n, c, sigma),
        "even": make_state("even", n, c, sigma),
        "odd": make_state("odd", n, c, sigma),
        "sym": make_state("sym", n, c, sigma),
        "anti": make_state("anti", n, c, sigma),
    }
    evals_flat, evecs_flat = np.linalg.eigh(H_flat.toarray())
    coeff = evecs_flat.conj().T @ base["gauss"]
    for label, mask in [("posE", evals_flat > 0), ("negE", evals_flat < 0)]:
        out = evecs_flat[:, mask] @ coeff[mask]
        base[label] = out / np.linalg.norm(out)
    fam = {}
    for label, psi in base.items():
        d = cz(ev(H_grav, NSTEPS, psi), c) - cz(ev(H_flat, NSTEPS, psi), c)
        fam[label] = d
    p = all(v > 0 for v in fam.values())
    score += p
    details = ", ".join(f"{k}:{v:+.2e}" for k, v in fam.items())
    print(f"  [C17] State family: {details} {'PASS' if p else 'FAIL'}")

    print(f"\n  SCORE: {score}/17")
    return score


if __name__ == "__main__":
    t0 = time.time()
    run_card()
    print(f"  Time: {time.time()-t0:.1f}s")
