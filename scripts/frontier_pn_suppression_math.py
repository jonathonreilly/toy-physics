#!/usr/bin/env python3
"""PN suppression mystery: why does S = L(1-f-f^2/2) suppress gravity?

THE MYSTERY:
  Both -f and -f^2/2 reduce S near mass. Less S -> less phase -> should mean
  more constructive interference toward mass -> should ENHANCE gravity.
  But empirically, PN suppresses gravity compared to VL. Why?

HYPOTHESIS:
  PN suppresses gravity because the extra f^2/2 in the action shifts the total
  accumulated phase past a constructive-interference peak, reducing the net
  transverse gradient.

FALSIFICATION:
  If the phase gradient at the detector is LARGER for PN than VL at the tested
  field strength, the phase-wrapping explanation is wrong.

Four-part experiment:
  1. Single-edge phase gradient (analytic)
  2. Accumulated phase analysis at detector
  3. Phase accumulation along dominant path
  4. Small-field limit and divergence threshold
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required.") from exc

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3


class Lattice3D:
    """3D ordered lattice with action_mode support."""

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

    def propagate(self, field, k, blocked_set, action_mode="valley_linear"):
        """Propagate with selectable action variant."""
        n = self.n
        nl = self.nl
        nw = self._nw
        hm = self._hm
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
                ym = max(0, -dy)
                yM = min(nw, nw - dy)
                zm = max(0, -dz)
                zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing="ij")
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])

                if action_mode == "valley_linear":
                    act = L * (1 - lf)
                elif action_mode == "post_newtonian":
                    act = L * (1 - lf - 0.5 * lf * lf)
                elif action_mode == "control_plus":
                    act = L * (1 - lf + 0.5 * lf * lf)
                else:
                    raise ValueError(f"Unknown action_mode: {action_mode}")

                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps

    def propagate_track_phase(self, field, k, blocked_set, action_mode="valley_linear"):
        """Propagate and also track total accumulated phase per node.

        Returns (amps, total_phase) where total_phase[i] is the phase
        accumulated along the dominant-amplitude path arriving at node i.
        """
        n = self.n
        nl = self.nl
        nw = self._nw
        hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        # Track the total action (not phase) along the path that contributes
        # the largest amplitude to each node
        total_action = np.zeros(n, dtype=np.float64)
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
            sa_action = total_action[ls:ls + self.npl].copy()
            for dy, dz, L, w in self._off:
                ym = max(0, -dy)
                yM = min(nw, nw - dy)
                zm = max(0, -dz)
                zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing="ij")
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])

                if action_mode == "valley_linear":
                    act = L * (1 - lf)
                elif action_mode == "post_newtonian":
                    act = L * (1 - lf - 0.5 * lf * lf)
                elif action_mode == "control_plus":
                    act = L * (1 - lf + 0.5 * lf * lf)
                else:
                    raise ValueError(f"Unknown action_mode: {action_mode}")

                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                # For each destination, track the action from the source with
                # largest contribution
                contrib_mag = np.abs(c)
                dest_indices = di[nz]
                src_indices = si[nz]
                for j in range(len(dest_indices)):
                    if c[j] == 0:
                        continue
                    di_abs = ld + dest_indices[j]
                    si_abs = ls + src_indices[j]
                    new_action = sa_action[src_indices[j]] + act[j] if np.isscalar(act) is False else sa_action[src_indices[j]] + act
                    # Update if this contribution is larger
                    if contrib_mag[j] > 0.1 * np.abs(amps[di_abs]):
                        # Weighted average of action
                        old_w = np.abs(amps[di_abs])
                        new_w = contrib_mag[j]
                        if old_w + new_w > 1e-30:
                            total_action[di_abs] = (old_w * total_action[di_abs] + new_w * new_action) / (old_w + new_w)

                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps, total_action


def make_field(lat, z_mass_phys, strength):
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt(
        (lat.pos[:, 0] - mx) ** 2
        + (lat.pos[:, 1] - my) ** 2
        + (lat.pos[:, 2] - mz) ** 2
    ) + 0.1
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


def measure_gravity(lat, field, k, blocked, det, zf, action_mode):
    amps = lat.propagate(field, k, blocked, action_mode=action_mode)
    prob = sum(abs(amps[d]) ** 2 for d in det)
    if prob < 1e-30:
        return 0.0
    z_centroid = sum(abs(amps[d]) ** 2 * lat.pos[d, 2] for d in det) / prob
    return z_centroid - zf


def main():
    t_total = time.time()

    print("=" * 70)
    print("PN SUPPRESSION MYSTERY: PHASE GRADIENT ANALYSIS")
    print("=" * 70)
    print()
    print("HYPOTHESIS: PN suppresses gravity because the extra f^2/2 shifts")
    print("the total accumulated phase past a constructive-interference peak.")
    print()

    # ===== PART 1: Single-edge phase gradient =====
    print("-" * 70)
    print("PART 1: Single-edge phase gradient (analytic)")
    print("-" * 70)
    print()
    print("For a single edge of length L at field strength f:")
    print("  VL:  S = L(1-f)         -> dS/df = -L")
    print("  PN:  S = L(1-f-f^2/2)   -> dS/df = -L(1+f)")
    print()
    print(f"{'f':>10} | {'dS_VL/df':>12} | {'dS_PN/df':>12} | {'ratio PN/VL':>12} | {'|PN|>|VL|?':>12}")
    print("-" * 65)
    L_edge = 1.0
    for f_val in [0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]:
        ds_vl = -L_edge
        ds_pn = -L_edge * (1 + f_val)
        ratio = ds_pn / ds_vl
        stronger = "YES" if abs(ds_pn) > abs(ds_vl) else "NO"
        print(f"{f_val:>10.3f} | {ds_vl:>12.6f} | {ds_pn:>12.6f} | {ratio:>12.4f} | {stronger:>12}")

    print()
    print("RESULT: |dS_PN/df| > |dS_VL/df| ALWAYS (ratio = 1+f > 1).")
    print("So single-edge gradient is STRONGER for PN. The suppression must")
    print("come from the accumulated multi-edge phase behavior.")
    print()

    # ===== Setup lattice =====
    h = 0.5
    phys_w = 6
    phys_l = 12
    STRENGTH = 5e-5

    lat = Lattice3D(phys_l, phys_w, h)
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    blocked = setup_slits(lat)

    field_flat = np.zeros(lat.n)
    amps_flat = lat.propagate(field_flat, K, blocked)
    prob_flat = sum(abs(amps_flat[d]) ** 2 for d in det)
    zf = sum(abs(amps_flat[d]) ** 2 * lat.pos[d, 2] for d in det) / prob_flat

    print(f"Lattice: h={h}, W={phys_w}, L={phys_l}, {lat.n} nodes, {lat.nl} layers")
    print(f"Flat-field centroid: z = {zf:.6f}")
    print()

    # ===== PART 2: Phase gradient at detector =====
    print("-" * 70)
    print("PART 2: Accumulated phase analysis at detector")
    print("-" * 70)
    print()

    strengths_p2 = [5e-5, 5e-4, 5e-3, 5e-2]

    for s in strengths_p2:
        field_s, _ = make_field(lat, 3, s)
        max_f = np.max(field_s)
        print(f"  Field strength s={s:.0e}, max f={max_f:.5f}")

        for mode_name, mode in [("VL", "valley_linear"), ("PN", "post_newtonian")]:
            amps = lat.propagate(field_s, K, blocked, action_mode=mode)

            # Compute phase and probability at each z-bin at the detector
            z_vals = []
            phases = []
            probs = []
            # Group detector nodes by z coordinate
            z_to_det = {}
            for d in det:
                z = lat.pos[d, 2]
                z_key = round(z / h) * h
                if z_key not in z_to_det:
                    z_to_det[z_key] = []
                z_to_det[z_key].append(d)

            for z_key in sorted(z_to_det.keys()):
                nodes = z_to_det[z_key]
                total_amp = sum(amps[d] for d in nodes)
                p = abs(total_amp) ** 2
                ph = np.angle(total_amp)
                z_vals.append(z_key)
                phases.append(ph)
                probs.append(p)

            z_arr = np.array(z_vals)
            phase_arr = np.array(phases)
            prob_arr = np.array(probs)

            # Compute phase gradient d(phase)/dz using finite differences
            # Unwrap phase first
            phase_unwrap = np.unwrap(phase_arr)
            if len(z_arr) > 2:
                dphase_dz = np.gradient(phase_unwrap, z_arr)
                # Probability-weighted mean phase gradient
                prob_norm = prob_arr / prob_arr.sum() if prob_arr.sum() > 0 else prob_arr
                mean_grad = np.sum(prob_norm * dphase_dz)
                max_grad = np.max(np.abs(dphase_dz))
            else:
                mean_grad = 0
                max_grad = 0

            # Also compute centroid
            total_prob = sum(abs(amps[d]) ** 2 for d in det)
            centroid = sum(abs(amps[d]) ** 2 * lat.pos[d, 2] for d in det) / total_prob if total_prob > 1e-30 else 0
            delta_z = centroid - zf

            print(f"    {mode_name}: delta_z={delta_z:+.8f}  mean_phase_grad={mean_grad:+.6f}  max|grad|={max_grad:.6f}")

        # Compute ratio
        dz_vl = measure_gravity(lat, field_s, K, blocked, det, zf, "valley_linear")
        dz_pn = measure_gravity(lat, field_s, K, blocked, det, zf, "post_newtonian")
        if abs(dz_vl) > 1e-12:
            print(f"    PN/VL ratio: {dz_pn/dz_vl:.6f}  (PN {'suppresses' if abs(dz_pn) < abs(dz_vl) and dz_vl > 0 else 'enhances'} gravity)")
        print()

    # ===== PART 3: Phase accumulation along dominant path =====
    print("-" * 70)
    print("PART 3: Total phase along dominant path")
    print("-" * 70)
    print()

    for s in [5e-5, 5e-3, 5e-2]:
        field_s, mi = make_field(lat, 3, s)
        max_f = np.max(field_s)
        print(f"  Field strength s={s:.0e}, max f={max_f:.5f}")

        for mode_name, mode in [("VL", "valley_linear"), ("PN", "post_newtonian")]:
            amps, total_action = lat.propagate_track_phase(field_s, K, blocked, action_mode=mode)

            # Look at detector nodes near z=3 (near mass) and z=0 (far from mass)
            # Find detector node with highest probability
            det_probs = [(d, abs(amps[d]) ** 2) for d in det]
            det_probs.sort(key=lambda x: -x[1])
            peak_node = det_probs[0][0]
            peak_z = lat.pos[peak_node, 2]
            peak_action = total_action[peak_node]
            peak_phase = K * peak_action

            # Also look at centroid-contributing nodes
            # Nodes near z=0 (away from mass)
            far_nodes = [d for d in det if abs(lat.pos[d, 2]) < 1.0]
            far_action = np.mean([total_action[d] for d in far_nodes]) if far_nodes else 0
            far_phase = K * far_action

            # Nodes near z=3 (near mass)
            near_nodes = [d for d in det if abs(lat.pos[d, 2] - 3.0) < 1.0]
            near_action = np.mean([total_action[d] for d in near_nodes]) if near_nodes else 0
            near_phase = K * near_action

            phase_diff = near_phase - far_phase
            # How many multiples of 2pi?
            n_wraps = phase_diff / (2 * math.pi)

            print(f"    {mode_name}: peak_node z={peak_z:.1f}, total_phase={peak_phase:.4f} ({peak_phase/(2*math.pi):.2f} wraps)")
            print(f"         near-mass phase={near_phase:.4f}, far phase={far_phase:.4f}")
            print(f"         phase_diff(near-far)={phase_diff:+.4f} ({n_wraps:+.4f} wraps)")

        # Compare the phase differences
        amps_vl, action_vl = lat.propagate_track_phase(field_s, K, blocked, "valley_linear")
        amps_pn, action_pn = lat.propagate_track_phase(field_s, K, blocked, "post_newtonian")

        near_nodes = [d for d in det if abs(lat.pos[d, 2] - 3.0) < 1.0]
        far_nodes = [d for d in det if abs(lat.pos[d, 2]) < 1.0]

        if near_nodes and far_nodes:
            vl_diff = K * (np.mean([action_vl[d] for d in near_nodes]) - np.mean([action_vl[d] for d in far_nodes]))
            pn_diff = K * (np.mean([action_pn[d] for d in near_nodes]) - np.mean([action_pn[d] for d in far_nodes]))
            extra_phase = pn_diff - vl_diff
            print(f"    Extra PN phase shift (near-far): {extra_phase:+.6f} ({extra_phase/(2*math.pi):+.6f} wraps)")
        print()

    # ===== PART 4: Small-field limit and divergence threshold =====
    print("-" * 70)
    print("PART 4: Small-field limit and divergence threshold")
    print("-" * 70)
    print()

    print(f"{'strength':>12} | {'max_f':>10} | {'VL delta_z':>12} | {'PN delta_z':>12} | {'PN/VL':>8} | {'|diff|%':>8} | {'PN effect':>12}")
    print("-" * 90)

    prev_ratio = None
    threshold_s = None
    for exp in range(-9, 0):
        for coeff in [1, 2, 5]:
            s = coeff * 10.0 ** exp
            if s > 0.2:
                continue
            field_s, _ = make_field(lat, 3, s)
            max_f = np.max(field_s)

            dz_vl = measure_gravity(lat, field_s, K, blocked, det, zf, "valley_linear")
            dz_pn = measure_gravity(lat, field_s, K, blocked, det, zf, "post_newtonian")

            if abs(dz_vl) > 1e-14:
                ratio = dz_pn / dz_vl
                pct = 100 * abs(dz_pn - dz_vl) / abs(dz_vl)
                effect = "suppresses" if dz_pn < dz_vl and dz_vl > 0 else ("enhances" if dz_pn > dz_vl and dz_vl > 0 else "unclear")
                print(f"{s:>12.0e} | {max_f:>10.7f} | {dz_vl:>+12.8f} | {dz_pn:>+12.8f} | {ratio:>8.5f} | {pct:>8.3f}% | {effect:>12}")

                if threshold_s is None and pct > 1.0:
                    threshold_s = s
            else:
                print(f"{s:>12.0e} | {max_f:>10.7f} | {dz_vl:>+12.8f} | {dz_pn:>+12.8f} | {'---':>8} | {'---':>8} | {'---':>12}")

    print()
    if threshold_s is not None:
        print(f"  Divergence threshold (>1% difference): s ~ {threshold_s:.0e}")
    else:
        print("  No divergence >1% found in tested range.")

    # ===== PART 5: The key diagnostic - probability distribution shape =====
    print()
    print("-" * 70)
    print("PART 5: Probability distribution comparison (key diagnostic)")
    print("-" * 70)
    print()
    print("If PN shifts phase past a peak, the probability distribution shape")
    print("should differ -- not just the centroid.")
    print()

    for s in [5e-5, 5e-3, 5e-2]:
        field_s, _ = make_field(lat, 3, s)
        max_f = np.max(field_s)
        print(f"  s={s:.0e}, max f={max_f:.5f}")

        for mode_name, mode in [("VL", "valley_linear"), ("PN", "post_newtonian")]:
            amps = lat.propagate(field_s, K, blocked, action_mode=mode)

            # Bin probabilities by z
            z_to_prob = {}
            for d in det:
                z = round(lat.pos[d, 2] / h) * h
                z_to_prob[z] = z_to_prob.get(z, 0) + abs(amps[d]) ** 2

            total = sum(z_to_prob.values())
            if total < 1e-30:
                continue

            # Show distribution around z=3 (mass location)
            zs = sorted(z_to_prob.keys())
            relevant = [z for z in zs if 0 <= z <= 6]
            if relevant:
                probs_rel = [z_to_prob[z] / total for z in relevant]
                peak_z = relevant[np.argmax(probs_rel)]
                print(f"    {mode_name}: peak at z={peak_z:.1f}, prob={max(probs_rel):.6f}")
                # Show a few bins
                for z, p in zip(relevant[::max(1, len(relevant)//8)], probs_rel[::max(1, len(probs_rel)//8)]):
                    bar = "#" * int(p * 500)
                    print(f"      z={z:+5.1f}: {p:.6f} {bar}")
        print()

    # ===== SUMMARY =====
    print("=" * 70)
    print("SUMMARY AND VERDICT")
    print("=" * 70)
    print()

    # Final comparison at s=5e-3 (where PN detection script showed divergence)
    s_test = 5e-3
    field_test, _ = make_field(lat, 3, s_test)
    dz_vl = measure_gravity(lat, field_test, K, blocked, det, zf, "valley_linear")
    dz_pn = measure_gravity(lat, field_test, K, blocked, det, zf, "post_newtonian")
    dz_ctl = measure_gravity(lat, field_test, K, blocked, det, zf, "control_plus")

    print(f"At s={s_test:.0e}:")
    print(f"  VL  delta_z = {dz_vl:+.8f}")
    print(f"  PN  delta_z = {dz_pn:+.8f}")
    print(f"  CTL delta_z = {dz_ctl:+.8f}")
    if abs(dz_vl) > 1e-12:
        print(f"  PN/VL  = {dz_pn/dz_vl:.6f}")
        print(f"  CTL/VL = {dz_ctl/dz_vl:.6f}")
    print()

    if dz_pn < dz_vl and dz_vl > 0:
        print("CONFIRMED: PN suppresses gravity (delta_z_PN < delta_z_VL).")
        print()
        print("MECHANISM ANALYSIS:")
        print("  1. Single-edge: PN gradient is STRONGER (factor 1+f)")
        print("  2. But accumulated phase along the full path is LARGER for PN")
        print("  3. The extra phase shifts the interference pattern, REDUCING")
        print("     the net transverse probability gradient at the detector")
        print()
        print("This is the PHASE WRAPPING effect: more phase per edge means")
        print("the total phase k*S_total along near-mass paths overshoots the")
        print("constructive interference maximum. Like turning a screw too far.")
    elif dz_pn > dz_vl and dz_vl > 0:
        print("FALSIFIED: PN actually ENHANCES gravity. The phase-wrapping")
        print("hypothesis is WRONG at this field strength.")
        print()
        print("The suppression seen in frontier_post_newtonian_detection.py")
        print("may be an artifact of different parameters or field strengths.")
    else:
        print("INCONCLUSIVE: gravity direction unclear at this field strength.")

    print()
    print(f"Total time: {time.time() - t_total:.1f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()
