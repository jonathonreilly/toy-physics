#!/usr/bin/env python3
"""Retained-lane spectral weighting controls on the split-delay Lorentzian model.

This is the follow-up the review asked for:

  1. use the retained split-delay Lorentzian action
       S = L * (1 - f * cos(2*theta))
  2. compare raw spectral sums against controls that are independent of
     detector outputs
  3. keep the old detector-flux equalization as an explicit comparison

The key distinction is where the weighting information comes from:

  raw prior
      the source-side k prior only (flat or Gaussian)

  source-coupled
      weights multiplied by sqrt(P_ref_flat(k)), where P_ref_flat is the
      no-field probability on a reference layer immediately after the slit
      plane. This is a source/boundary-proximal outgoing-beam prior.

  source-equalized
      weights divided by sqrt(P_ref_flat(k)), so each k contributes equal
      post-slit incident flux at that reference plane

  detector-equalized
      the old control: each psi_k is normalized to unit detector flux before
      summation. This depends on detector outputs and is included only as a
      comparison benchmark, not as a source model.

Review-safe question:
  On the retained Euclidean and split-delay Lorentzian lattices, do
  source-side weighting controls rescue broadband TOWARD, or does only the
  detector-equalized counterfactual flip the sign?
"""

from __future__ import annotations

import math
import time

import numpy as np

BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5
PHYS_W = 6
PHYS_L = 12
H = 0.5


class Lattice3D:
    """3D ordered lattice with Euclidean and split-delay Lorentzian actions."""

    def __init__(self, phys_l: float, phys_w: float, h: float) -> None:
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw**2
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
                lorentz_factor = math.cos(2 * theta)
                self._off.append((dy, dz, L, w, lorentz_factor))
        self._nw = nw

    def propagate(self, field: np.ndarray, k: float, blocked_set: set[int], lorentzian: bool) -> np.ndarray:
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
            sa = amps[ls : ls + self.npl].copy()
            sa[blocked[ls : ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue

            sf = field[ls : ls + self.npl]
            df = field[ld : ld + self.npl]
            db = blocked[ld : ld + self.npl]

            for dy, dz, L, w, lf_factor in self._off:
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
                if lorentzian:
                    act = L * (1 - lf * lf_factor)
                else:
                    act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld : ld + self.npl], di[nz], c)

        return amps


def make_field_spatial(lat: Lattice3D, z_mass_phys: float, strength: float) -> tuple[np.ndarray, int | None]:
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r = np.sqrt((lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2) + 0.1
    return strength / r, mi


def setup_slits(lat: Lattice3D) -> tuple[set[int], int]:
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
    ref_layer = min(bl + 1, lat.nl - 1)
    return blocked, ref_layer


def detector_indices(lat: Lattice3D) -> list[int]:
    dl = lat.nl - 1
    return [
        lat.nmap[(dl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (dl, iy, iz) in lat.nmap
    ]


def detector_amp_dict(amps: np.ndarray, det: list[int]) -> dict[int, complex]:
    return {d: amps[d] for d in det}


def centroid_from_det_amps(det_amps: dict[int, complex], pos: np.ndarray) -> tuple[float, float]:
    total = sum(abs(a) ** 2 for a in det_amps.values())
    if total < 1e-30:
        return 0.0, total
    zc = sum(abs(a) ** 2 * pos[d, 2] for d, a in det_amps.items()) / total
    return zc, total


def scale_det_amps(det_amps: dict[int, complex], scale: float) -> dict[int, complex]:
    return {d: a * scale for d, a in det_amps.items()}


def normalize_weights(weights: dict[float, float]) -> dict[float, float]:
    w_sum = sum(abs(w) for w in weights.values())
    if w_sum < 1e-30:
        n = len(weights)
        return {k: 1.0 / n for k in weights}
    return {k: w / w_sum for k, w in weights.items()}


def coherent_sum(weights: dict[float, float], amp_dict: dict[float, dict[int, complex]], ks: list[float]) -> dict[int, complex]:
    det_keys = next(iter(amp_dict.values())).keys()
    return {d: sum(weights[k] * amp_dict[k][d] for k in ks) for d in det_keys}


def layer_prob(lat: Lattice3D, amps: np.ndarray, layer_idx: int) -> float:
    ls = lat._ls[layer_idx]
    return float(np.sum(np.abs(amps[ls : ls + lat.npl]) ** 2))


def main() -> None:
    print("=" * 84)
    print("RETAINED-LANE SOURCE-WEIGHT SPECTRAL CONTROLS")
    print("=" * 84)
    print()
    print("Question:")
    print("  On the retained Euclidean and split-delay Lorentzian lattices, does")
    print("  broadband attraction survive under source-side weighting controls, or")
    print("  only under detector-equalized reweighting?")
    print()

    t0 = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    blocked, ref_layer = setup_slits(lat)
    field_flat = np.zeros(lat.n)
    field_mass, _ = make_field_spatial(lat, 3.0, STRENGTH)
    det = detector_indices(lat)
    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={H}")
    print(f"Reference layer: {ref_layer} (post-slit source-side normalization plane)")
    print(f"Mass strength: {STRENGTH}")
    print(f"Setup: {time.time() - t0:.1f}s")
    print()

    k_fine = [round(k, 4) for k in np.arange(0.5, 12.01, 0.5)]

    models = {
        "euclidean": False,
        "lorentzian": True,
    }

    data: dict[str, dict[str, dict[float, object]]] = {}
    print(f"Pre-computing {len(k_fine) * len(models) * 2} propagations...")
    t1 = time.time()
    for name, is_lorentzian in models.items():
        model_data = {
            "flat_det": {},
            "mass_det": {},
            "flat_det_prob": {},
            "mass_det_prob": {},
            "flat_ref_prob": {},
            "single_delta": {},
        }
        for i, k in enumerate(k_fine, start=1):
            af = lat.propagate(field_flat, k, blocked, lorentzian=is_lorentzian)
            am = lat.propagate(field_mass, k, blocked, lorentzian=is_lorentzian)
            det_flat = detector_amp_dict(af, det)
            det_mass = detector_amp_dict(am, det)
            model_data["flat_det"][k] = det_flat
            model_data["mass_det"][k] = det_mass
            zf, pf = centroid_from_det_amps(det_flat, lat.pos)
            zm, pm = centroid_from_det_amps(det_mass, lat.pos)
            model_data["flat_det_prob"][k] = pf
            model_data["mass_det_prob"][k] = pm
            model_data["flat_ref_prob"][k] = layer_prob(lat, af, ref_layer)
            model_data["single_delta"][k] = zm - zf
            if i % 12 == 0:
                elapsed = time.time() - t1
                print(f"  {name}: {i}/{len(k_fine)} k values ({elapsed:.0f}s elapsed)")
        data[name] = model_data
    print(f"Done in {time.time() - t1:.0f}s")
    print()

    print("=" * 84)
    print("SINGLE-k REFERENCE")
    print("=" * 84)
    print(f"{'k':>5} | {'Euclidean':>12} {'':>7} | {'Lorentzian':>12} {'':>7}")
    print(f"{'':>5} | {'delta':>12} {'dir':>7} | {'delta':>12} {'dir':>7}")
    print("-" * 60)
    for k in k_fine:
        de = data["euclidean"]["single_delta"][k]
        dl = data["lorentzian"]["single_delta"][k]
        dir_e = "TOWARD" if de > 1e-10 else "AWAY" if de < -1e-10 else "~zero"
        dir_l = "TOWARD" if dl > 1e-10 else "AWAY" if dl < -1e-10 else "~zero"
        print(f"{k:>5.1f} | {de:>+12.6f} {dir_e:>7} | {dl:>+12.6f} {dir_l:>7}")
    print()

    print("=" * 84)
    print("SOURCE-SIDE PROBABILITY HIERARCHY (FLAT BRANCH)")
    print("=" * 84)
    for name in models:
        ref_probs = [data[name]["flat_ref_prob"][k] for k in k_fine if data[name]["flat_ref_prob"][k] > 1e-30]
        det_probs = [data[name]["flat_det_prob"][k] for k in k_fine if data[name]["flat_det_prob"][k] > 1e-30]
        print(
            f"{name:>10}: P_ref range {min(ref_probs):.2e} .. {max(ref_probs):.2e} "
            f"(ratio {max(ref_probs)/min(ref_probs):.1e}), "
            f"P_det range {min(det_probs):.2e} .. {max(det_probs):.2e} "
            f"(ratio {max(det_probs)/min(det_probs):.1e})"
        )
    print()

    configs = [
        ("flat", None, None),
        ("gauss-5-narrow", 5.0, 0.5),
        ("gauss-5-medium", 5.0, 1.0),
        ("gauss-5-broad", 5.0, 2.0),
        ("gauss-5-vbroad", 5.0, 4.0),
        ("gauss-7-narrow", 7.0, 0.5),
        ("gauss-7-medium", 7.0, 1.0),
        ("gauss-7-broad", 7.0, 2.0),
        ("gauss-7-vbroad", 7.0, 4.0),
    ]

    def prior_weights(k0: float | None, sigma: float | None) -> dict[float, float]:
        if k0 is None:
            return {k: 1.0 / len(k_fine) for k in k_fine}
        raw = {k: math.exp(-((k - k0) ** 2) / (2 * sigma * sigma)) for k in k_fine}
        return normalize_weights(raw)

    print("=" * 84)
    print("WEIGHTING COMPARISON")
    print("=" * 84)

    results = []
    for model_name in models:
        print()
        print(f"{model_name.upper()}:")
        print(
            f"{'config':<16} | {'raw':>11} {'':>7} | {'src_cpl':>11} {'':>7} | "
            f"{'src_eq':>11} {'':>7} | {'det_eq':>11} {'':>7}"
        )
        print(
            f"{'':<16} | {'delta':>11} {'dir':>7} | {'delta':>11} {'dir':>7} | "
            f"{'delta':>11} {'dir':>7} | {'delta':>11} {'dir':>7}"
        )
        print("-" * 108)

        model_data = data[model_name]
        for label, k0, sigma in configs:
            prior = prior_weights(k0, sigma)

            # Raw source prior only.
            raw_weights = prior

            # Source-coupled outgoing spectrum on the reference layer.
            src_cpl = normalize_weights({
                k: prior[k] * math.sqrt(max(model_data["flat_ref_prob"][k], 1e-30))
                for k in k_fine
            })

            # Equal incident flux on the reference layer.
            src_eq = normalize_weights({
                k: prior[k] / math.sqrt(max(model_data["flat_ref_prob"][k], 1e-30))
                for k in k_fine
            })

            # Detector-equalized benchmark.
            flat_det_eq = {
                k: scale_det_amps(
                    model_data["flat_det"][k],
                    1.0 / math.sqrt(max(model_data["flat_det_prob"][k], 1e-30)),
                )
                for k in k_fine
            }
            mass_det_eq = {
                k: scale_det_amps(
                    model_data["mass_det"][k],
                    1.0 / math.sqrt(max(model_data["mass_det_prob"][k], 1e-30)),
                )
                for k in k_fine
            }

            def delta_from(weight_set: dict[float, float], flat_dict: dict[float, dict[int, complex]], mass_dict: dict[float, dict[int, complex]]) -> float:
                flat_sum = coherent_sum(weight_set, flat_dict, k_fine)
                mass_sum = coherent_sum(weight_set, mass_dict, k_fine)
                zf, _ = centroid_from_det_amps(flat_sum, lat.pos)
                zm, _ = centroid_from_det_amps(mass_sum, lat.pos)
                return zm - zf

            d_raw = delta_from(raw_weights, model_data["flat_det"], model_data["mass_det"])
            d_src_cpl = delta_from(src_cpl, model_data["flat_det"], model_data["mass_det"])
            d_src_eq = delta_from(src_eq, model_data["flat_det"], model_data["mass_det"])
            d_det_eq = delta_from(prior, flat_det_eq, mass_det_eq)

            def dir_of(delta: float) -> str:
                return "TOWARD" if delta > 1e-10 else "AWAY" if delta < -1e-10 else "~zero"

            r_raw = dir_of(d_raw)
            r_src_cpl = dir_of(d_src_cpl)
            r_src_eq = dir_of(d_src_eq)
            r_det_eq = dir_of(d_det_eq)
            print(
                f"{label:<16} | {d_raw:>+11.6f} {r_raw:>7} | "
                f"{d_src_cpl:>+11.6f} {r_src_cpl:>7} | "
                f"{d_src_eq:>+11.6f} {r_src_eq:>7} | "
                f"{d_det_eq:>+11.6f} {r_det_eq:>7}"
            )
            results.append({
                "model": model_name,
                "label": label,
                "raw": r_raw,
                "src_cpl": r_src_cpl,
                "src_eq": r_src_eq,
                "det_eq": r_det_eq,
            })

    print()
    print("=" * 84)
    print("SUMMARY COUNTS")
    print("=" * 84)
    for model_name in models:
        subset = [r for r in results if r["model"] == model_name]
        for key in ["raw", "src_cpl", "src_eq", "det_eq"]:
            n_t = sum(1 for r in subset if r[key] == "TOWARD")
            n_a = sum(1 for r in subset if r[key] == "AWAY")
            print(f"{model_name:>10} {key:>7}: TOWARD={n_t}/{len(subset)}, AWAY={n_a}/{len(subset)}")

    print()
    print("Interpretation guide:")
    print("  raw      = source prior only")
    print("  src_cpl  = source-derived outgoing-beam weighting at post-slit reference layer")
    print("  src_eq   = equal incident post-slit flux per k")
    print("  det_eq   = detector-flux equalization benchmark (review caveat control)")


if __name__ == "__main__":
    main()
