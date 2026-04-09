#!/usr/bin/env python3
"""Natural-weight spectral averaging: does probability-equalized weighting flip AWAY to TOWARD?

Previous spectral tests used EQUAL-AMPLITUDE Gaussian weighting across k.
But detector probability varies by ~10^23 across the k range, so low-k modes
dominate the equal-weight sum.

This script tests FOUR weighting schemes:
  A) Equal amplitude (baseline, same as previous test)
  B) Probability-weighted: w(k) = sqrt(P_det(k))
     Each k contributes equally in probability, not amplitude.
  C) Inverse-probability: w(k) = 1/P_det(k)
     Suppresses high-probability low-k modes.
  D) Centroid-contribution equalized: w(k) = 1/sqrt(P_det(k))
     Each k contributes equally to the centroid calculation.

Uses BOTH Euclidean (S = L(1-f)) and Lorentzian (S = L*sqrt(1-f)) actions
on the 3D lattice (h=0.5, W=6, L=12).

HYPOTHESIS: Probability-equalized spectral averaging gives TOWARD because
most k values in the attractive window contribute equally.

FALSIFICATION: If all weighting schemes give AWAY.
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5


class Lattice3D:
    """3D lattice propagator with selectable action type."""

    def __init__(self, phys_l, phys_w, h):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 2
        self.n = self.nl * self.npl
        self._hm = h * h
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
                w = math.exp(-BETA * theta * theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set, action_type="euclidean"):
        """Propagate with either Euclidean or Lorentzian action."""
        n = self.n; nl = self.nl; nw = self._nw; hm = self._hm
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
                if action_type == "euclidean":
                    act = L * (1 - lf)
                elif action_type == "lorentzian":
                    act = L * np.sqrt(np.maximum(1 - lf, 0.0))
                else:
                    raise ValueError(f"Unknown action type: {action_type}")
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_spatial(lat, z_mass_phys, strength):
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r = np.sqrt((lat.pos[:, 1] - my)**2 + (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r, mi


def setup_slits(lat):
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
    return blocked


def main():
    print("=" * 72)
    print("NATURAL-WEIGHT SPECTRAL AVERAGING")
    print("Does probability-equalized weighting flip AWAY to TOWARD?")
    print("=" * 72)
    print()

    h = 0.5
    phys_w = 6
    phys_l = 12
    z_mass = 3

    t0 = time.time()
    lat = Lattice3D(phys_l, phys_w, h)
    blocked = setup_slits(lat)
    field_flat = np.zeros(lat.n)
    field_mass, _ = make_field_spatial(lat, z_mass, STRENGTH)

    det = [lat.nmap[(lat.nl - 1, iy, iz)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)
           if (lat.nl - 1, iy, iz) in lat.nmap]
    pos = lat.pos

    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={h}")
    print(f"Mass at z={z_mass}, strength={STRENGTH}")
    print(f"Setup: {time.time() - t0:.1f}s")
    print()

    k_fine = np.arange(0.5, 12.01, 0.5)

    action_types = ["euclidean", "lorentzian"]

    for action_type in action_types:
        print()
        print("=" * 72)
        print(f"ACTION TYPE: {action_type.upper()}")
        print("=" * 72)

        # ==============================================================
        # Pre-compute detector amplitudes and probabilities for all k
        # ==============================================================
        print(f"\nPre-computing {len(k_fine)} propagations ({action_type})...")
        t1 = time.time()

        flat_det_amps = {}
        mass_det_amps = {}
        flat_det_prob = {}
        mass_det_prob = {}

        for k in k_fine:
            af = lat.propagate(field_flat, k, blocked, action_type)
            am = lat.propagate(field_mass, k, blocked, action_type)

            flat_det_amps[k] = {d: af[d] for d in det}
            mass_det_amps[k] = {d: am[d] for d in det}

            flat_det_prob[k] = sum(abs(af[d])**2 for d in det)
            mass_det_prob[k] = sum(abs(am[d])**2 for d in det)

        print(f"Done in {time.time() - t1:.0f}s")

        # ==============================================================
        # Part 1: Single-k sweep (for reference)
        # ==============================================================
        print(f"\n--- Single-k sweep ({action_type}) ---")
        print(f"{'k':>6} | {'delta':>12} | {'dir':>7} | {'P_det':>12} | {'log10(P)':>9}")
        print("-" * 60)

        single_results = {}
        for k in k_fine:
            pf = flat_det_prob[k]
            pm = mass_det_prob[k]
            zf = sum(abs(flat_det_amps[k][d])**2 * pos[d, 2] for d in det) / pf if pf > 1e-30 else 0
            zm = sum(abs(mass_det_amps[k][d])**2 * pos[d, 2] for d in det) / pm if pm > 1e-30 else 0
            delta = zm - zf
            direction = "TOWARD" if delta > 1e-10 else "AWAY" if delta < -1e-10 else "~zero"
            logp = math.log10(pm) if pm > 1e-30 else -30
            single_results[k] = {"delta": delta, "dir": direction, "prob": pm, "logp": logp}
            print(f"{k:>6.1f} | {delta:>+12.6f} | {direction:>7} | {pm:>12.3e} | {logp:>9.1f}")

        n_toward = sum(1 for r in single_results.values() if r["dir"] == "TOWARD")
        n_away = sum(1 for r in single_results.values() if r["dir"] == "AWAY")
        print(f"\n  TOWARD: {n_toward}/{len(k_fine)}, AWAY: {n_away}/{len(k_fine)}")

        # Show probability range
        probs = [r["prob"] for r in single_results.values() if r["prob"] > 1e-30]
        if probs:
            print(f"  P_det range: {min(probs):.2e} to {max(probs):.2e} "
                  f"(ratio: {max(probs)/min(probs):.1e})")

        # ==============================================================
        # Part 2: Four weighting schemes
        # ==============================================================
        print(f"\n--- Weighting scheme comparison ({action_type}) ---")

        schemes = {
            "A_equal": {},
            "B_prob_wt": {},
            "C_inv_prob": {},
            "D_inv_sqrt_prob": {},
        }

        # Compute weights for each scheme
        for k in k_fine:
            pm = mass_det_prob[k]
            pf = flat_det_prob[k]
            # Use the average of flat and mass prob as the characteristic probability
            p_char = 0.5 * (pm + pf) if (pm + pf) > 1e-30 else 1e-30

            schemes["A_equal"][k] = 1.0
            schemes["B_prob_wt"][k] = math.sqrt(p_char) if p_char > 1e-30 else 0.0
            schemes["C_inv_prob"][k] = 1.0 / p_char if p_char > 1e-30 else 0.0
            schemes["D_inv_sqrt_prob"][k] = 1.0 / math.sqrt(p_char) if p_char > 1e-30 else 0.0

        # Normalize each scheme
        for name in schemes:
            w_sum = sum(schemes[name].values())
            if w_sum > 0:
                schemes[name] = {k: w / w_sum for k, w in schemes[name].items()}

        scheme_labels = {
            "A_equal": "A: Equal amplitude (w=1)",
            "B_prob_wt": "B: Prob-weighted (w=sqrt(P))",
            "C_inv_prob": "C: Inverse-prob (w=1/P)",
            "D_inv_sqrt_prob": "D: Inv-sqrt-prob (w=1/sqrt(P))",
        }

        print()
        print(f"{'Scheme':>35} | {'delta_coh':>12} {'dir':>7} | {'delta_inc':>12} {'dir':>7}")
        print("-" * 82)

        scheme_results = {}
        for name, weights in schemes.items():
            # Coherent sum: psi_total(d) = sum_k w(k) * psi_k(d)
            coh_mass = {}
            coh_flat = {}
            for d in det:
                coh_mass[d] = sum(weights[k] * mass_det_amps[k][d] for k in k_fine)
                coh_flat[d] = sum(weights[k] * flat_det_amps[k][d] for k in k_fine)

            pm_coh = sum(abs(coh_mass[d])**2 for d in det)
            pf_coh = sum(abs(coh_flat[d])**2 for d in det)
            zm_coh = sum(abs(coh_mass[d])**2 * pos[d, 2] for d in det) / pm_coh if pm_coh > 1e-30 else 0
            zf_coh = sum(abs(coh_flat[d])**2 * pos[d, 2] for d in det) / pf_coh if pf_coh > 1e-30 else 0
            delta_coh = zm_coh - zf_coh
            dir_coh = "TOWARD" if delta_coh > 1e-10 else "AWAY" if delta_coh < -1e-10 else "~zero"

            # Incoherent sum: P_total(d) = sum_k w(k)^2 * |psi_k(d)|^2
            inc_mass = {}
            inc_flat = {}
            for d in det:
                inc_mass[d] = sum(weights[k]**2 * abs(mass_det_amps[k][d])**2 for k in k_fine)
                inc_flat[d] = sum(weights[k]**2 * abs(flat_det_amps[k][d])**2 for k in k_fine)

            pm_inc = sum(inc_mass[d] for d in det)
            pf_inc = sum(inc_flat[d] for d in det)
            zm_inc = sum(inc_mass[d] * pos[d, 2] for d in det) / pm_inc if pm_inc > 1e-30 else 0
            zf_inc = sum(inc_flat[d] * pos[d, 2] for d in det) / pf_inc if pf_inc > 1e-30 else 0
            delta_inc = zm_inc - zf_inc
            dir_inc = "TOWARD" if delta_inc > 1e-10 else "AWAY" if delta_inc < -1e-10 else "~zero"

            print(f"{scheme_labels[name]:>35} | {delta_coh:>+12.6f} {dir_coh:>7} | "
                  f"{delta_inc:>+12.6f} {dir_inc:>7}")

            scheme_results[name] = {
                "delta_coh": delta_coh, "dir_coh": dir_coh,
                "delta_inc": delta_inc, "dir_inc": dir_inc,
            }

        # ==============================================================
        # Part 3: Weight distribution analysis
        # ==============================================================
        print(f"\n--- Weight distribution ({action_type}) ---")
        print(f"  Which k values dominate under each scheme?")
        print()
        print(f"{'k':>6} | {'A_equal':>10} | {'B_prob':>10} | {'C_inv_p':>10} | {'D_inv_sq':>10} | {'dir':>7}")
        print("-" * 72)

        for k in k_fine:
            wa = schemes["A_equal"][k]
            wb = schemes["B_prob_wt"][k]
            wc = schemes["C_inv_prob"][k]
            wd = schemes["D_inv_sqrt_prob"][k]
            d = single_results[k]["dir"]
            print(f"{k:>6.1f} | {wa:>10.4f} | {wb:>10.4f} | {wc:>10.4f} | {wd:>10.4f} | {d:>7}")

        # ==============================================================
        # Part 4: Majority-vote analysis
        # ==============================================================
        print(f"\n--- Majority vote analysis ({action_type}) ---")

        # For each scheme, compute weighted vote
        for name, weights in schemes.items():
            w_toward = sum(weights[k] for k in k_fine if single_results[k]["dir"] == "TOWARD")
            w_away = sum(weights[k] for k in k_fine if single_results[k]["dir"] == "AWAY")
            w_zero = sum(weights[k] for k in k_fine if single_results[k]["dir"] == "~zero")
            winner = "TOWARD" if w_toward > w_away else "AWAY"
            print(f"  {scheme_labels[name]:>35}: "
                  f"TOWARD={w_toward:.4f}, AWAY={w_away:.4f}, ~zero={w_zero:.4f} -> {winner}")

        # ==============================================================
        # Part 5: Coherent sum with ONLY attractive-window k values
        # ==============================================================
        print(f"\n--- Window-filtered coherent sum ({action_type}) ---")

        toward_ks = [k for k in k_fine if single_results[k]["dir"] == "TOWARD"]
        away_ks = [k for k in k_fine if single_results[k]["dir"] == "AWAY"]

        for label, ks in [("TOWARD-only", toward_ks), ("AWAY-only", away_ks)]:
            if not ks:
                print(f"  {label}: no k values in this window")
                continue

            # Equal weight on selected k values
            w = {k: 1.0 / len(ks) for k in ks}
            coh_m = {d: sum(w[k] * mass_det_amps[k][d] for k in ks) for d in det}
            coh_f = {d: sum(w[k] * flat_det_amps[k][d] for k in ks) for d in det}
            pm = sum(abs(coh_m[d])**2 for d in det)
            pf = sum(abs(coh_f[d])**2 for d in det)
            zm = sum(abs(coh_m[d])**2 * pos[d, 2] for d in det) / pm if pm > 1e-30 else 0
            zf = sum(abs(coh_f[d])**2 * pos[d, 2] for d in det) / pf if pf > 1e-30 else 0
            delta = zm - zf
            direction = "TOWARD" if delta > 1e-10 else "AWAY" if delta < -1e-10 else "~zero"
            print(f"  {label} (k={ks[0]:.1f}-{ks[-1]:.1f}, n={len(ks)}): "
                  f"delta={delta:+.6f} ({direction})")

    # ==================================================================
    # FINAL VERDICT
    # ==================================================================
    print()
    print("=" * 72)
    print("FINAL VERDICT")
    print("=" * 72)
    print()
    print("HYPOTHESIS: Probability-equalized spectral averaging gives TOWARD")
    print("because most k values in the attractive window contribute equally.")
    print()
    print("Test: Do schemes C or D (which suppress high-P low-k modes)")
    print("produce TOWARD when scheme A gives AWAY?")
    print()
    print(f"Total time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
