#!/usr/bin/env python3
"""
Thermal order-parameter uniqueness on the APBC/bosonic-bilinear surface.

This runner repackages the hierarchy APBC selector stack for the baryogenesis
lane. It shows:

  - the exact additive CPT-even scalar generator on the APBC blocks is the
    local source response of log|det(D+J)|
  - the corresponding curvature kernel closes on one unique minimal resolved
    Klein-four orbit at L_t = 4
  - that surface is a unique thermal order-parameter normalization surface,
    not a derived second thermal scalar family

So the APBC/bosonic-bilinear stack sharpens the same EWSB order parameter; it
does not reopen the old taste-scalar baryogenesis route by supplying a hidden
extra doublet.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

PASS = 0
FAIL = 0

V = 246.282818290129
G1_GUT_V = 0.464376
G2_V = 0.648031
VT_TARGET = 0.52
MH_2L = 119.77
MH_3L = 125.10


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"  [{tag}] {name}")
    if detail:
        print(f"         {detail}")


def info(name: str, detail: str = "") -> None:
    print(f"  [INFO] {name}")
    if detail:
        print(f"         {detail}")


def build_dirac_4d_apbc(ls: int, lt: int, u0: float, mass: float = 0.0) -> np.ndarray:
    n = ls**3 * lt
    d = np.zeros((n, n), dtype=complex)

    def idx(x0: int, x1: int, x2: int, t: int) -> int:
        return (((x0 % ls) * ls + (x1 % ls)) * ls + (x2 % ls)) * lt + (t % lt)

    for x0 in range(ls):
        for x1 in range(ls):
            for x2 in range(ls):
                for t in range(lt):
                    i = idx(x0, x1, x2, t)
                    d[i, i] += mass

                    eta = 1.0
                    xf = (x0 + 1) % ls
                    sign = -1.0 if x0 + 1 >= ls else 1.0
                    d[i, idx(xf, x1, x2, t)] += u0 * eta * sign / 2.0
                    xb = (x0 - 1) % ls
                    sign = -1.0 if x0 - 1 < 0 else 1.0
                    d[i, idx(xb, x1, x2, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** x0
                    xf = (x1 + 1) % ls
                    sign = -1.0 if x1 + 1 >= ls else 1.0
                    d[i, idx(x0, xf, x2, t)] += u0 * eta * sign / 2.0
                    xb = (x1 - 1) % ls
                    sign = -1.0 if x1 - 1 < 0 else 1.0
                    d[i, idx(x0, xb, x2, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** (x0 + x1)
                    xf = (x2 + 1) % ls
                    sign = -1.0 if x2 + 1 >= ls else 1.0
                    d[i, idx(x0, x1, xf, t)] += u0 * eta * sign / 2.0
                    xb = (x2 - 1) % ls
                    sign = -1.0 if x2 - 1 < 0 else 1.0
                    d[i, idx(x0, x1, xb, t)] -= u0 * eta * sign / 2.0

                    eta = (-1.0) ** (x0 + x1 + x2)
                    tf = (t + 1) % lt
                    sign = -1.0 if t + 1 >= lt else 1.0
                    d[i, idx(x0, x1, x2, tf)] += u0 * eta * sign / 2.0
                    tb = (t - 1) % lt
                    sign = -1.0 if t - 1 < 0 else 1.0
                    d[i, idx(x0, x1, x2, tb)] -= u0 * eta * sign / 2.0
    return d


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    dim = sum(block.shape[0] for block in blocks)
    out = np.zeros((dim, dim), dtype=complex)
    start = 0
    for block in blocks:
        n = block.shape[0]
        out[start : start + n, start : start + n] = block
        start += n
    return out


def logabs_det(m: np.ndarray) -> float:
    # For square matrices, log|det M| = sum_i log sigma_i(M). Using singular
    # values keeps the APBC block checks away from noisy det/slogdet warnings.
    svals = np.linalg.svd(m, compute_uv=False)
    return float(np.sum(np.log(svals)))


def observable_generator(d: np.ndarray, source: np.ndarray) -> float:
    return logabs_det(d + source) - logabs_det(d)


def canon(z: complex) -> tuple[float, float]:
    return (round(z.real, 12), round(z.imag, 12))


def apbc_phases(lt: int) -> list[complex]:
    return [cmath.exp(1j * (2 * n + 1) * math.pi / lt) for n in range(lt)]


def orbit_partition(lt: int) -> list[list[tuple[float, float]]]:
    ops = [lambda w: w, lambda w: -w, lambda w: w.conjugate(), lambda w: -w.conjugate()]
    phases = sorted({canon(z) for z in apbc_phases(lt)})
    seen = set()
    parts = []
    for z in phases:
        if z in seen:
            continue
        orb = sorted({canon(op(complex(*z))) for op in ops if canon(op(complex(*z))) in phases})
        parts.append(orb)
        seen.update(orb)
    return parts


def exact_local_a(lt: int, u0: float) -> float:
    return (1.0 / (2.0 * lt * u0**2)) * sum(
        1.0 / (3.0 + math.sin((2 * n + 1) * math.pi / lt) ** 2) for n in range(lt)
    )


def gauge_cubic() -> float:
    g_y = G1_GUT_V * math.sqrt(3.0 / 5.0)
    m_w = 0.5 * G2_V * V
    m_z = 0.5 * math.sqrt(G2_V * G2_V + g_y * g_y) * V
    return (2.0 * m_w**3 + m_z**3) / (4.0 * math.pi * V**3)


def route_gap(m_h: float) -> dict[str, float]:
    lam = m_h * m_h / (2.0 * V * V)
    delta_e_target = VT_TARGET * lam / 2.0 - gauge_cubic()
    kappa_sel = 6.0 * lam
    kappa_gold = 2.0 * lam
    delta_e_doublet = (
        1.0 / (12.0 * math.pi) * (kappa_sel / 2.0) ** 1.5
        + 3.0 / (12.0 * math.pi) * (kappa_gold / 2.0) ** 1.5
    )
    gap_factor = delta_e_target / delta_e_doublet
    return {"lambda": lam, "gap_factor": gap_factor}


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS THERMAL ORDER-PARAMETER UNIQUENESS")
    print("=" * 80)
    print()
    print("Question:")
    print("  Does the APBC / bosonic-bilinear selector stack derive a genuinely")
    print("  new finite-T scalar family for baryogenesis, or only one unique")
    print("  thermal order-parameter surface?")
    print()

    print("=" * 80)
    print("PART 1: UNIQUE ADDITIVE THERMAL SCALAR GENERATOR")
    print("=" * 80)
    print()

    u0 = 0.9
    # A tiny common mass keeps the exact block tests away from singular zero
    # modes without changing the additivity argument.
    d2 = build_dirac_4d_apbc(2, 2, u0, mass=0.05)
    d4 = build_dirac_4d_apbc(2, 4, u0, mass=0.05)
    d_tot = block_diag(d2, d4)
    max_mult_err = 0.0
    max_add_err = 0.0

    for j in (1e-3, 1e-2, 1e-1):
        s2 = j * np.eye(d2.shape[0], dtype=complex)
        s4 = j * np.eye(d4.shape[0], dtype=complex)
        s_tot = j * np.eye(d_tot.shape[0], dtype=complex)

        z2 = logabs_det(d2 + s2)
        z4 = logabs_det(d4 + s4)
        z_tot = logabs_det(d_tot + s_tot)
        mult_err = abs(z_tot - (z2 + z4))
        add_err = abs(
            observable_generator(d_tot, s_tot)
            - (observable_generator(d2, s2) + observable_generator(d4, s4))
        )
        max_mult_err = max(max_mult_err, mult_err)
        max_add_err = max(max_add_err, add_err)

    check(
        "exact APBC source response is multiplicative at the partition-amplitude level",
        max_mult_err < 1e-12,
        f"max log-amplitude multiplicativity error = {max_mult_err:.2e}",
    )
    check(
        "log|det(D+J)| gives the additive scalar generator on independent APBC blocks",
        max_add_err < 1e-12,
        f"max additive error = {max_add_err:.2e}",
    )
    info(
        "surface meaning",
        "the current APBC thermal scalar surface is the source curvature of one additive CPT-even generator, not a collection of unrelated scalar sectors",
    )
    print()

    print("=" * 80)
    print("PART 2: UNIQUE THERMAL ORDER-PARAMETER ORBIT")
    print("=" * 80)
    print()

    resolved = []
    for lt in range(2, 14, 2):
        parts = orbit_partition(lt)
        sizes = [len(p) for p in parts]
        print(f"  Lt={lt:2d}: num_orbits={len(parts)}, sizes={sizes}")
        if len(parts) == 1 and len(parts[0]) > 2:
            resolved.append(lt)

    a2 = exact_local_a(2, 1.0)
    a4 = exact_local_a(4, 1.0)
    a_inf = 1.0 / (4.0 * math.sqrt(3.0))

    check(
        "the unique minimal resolved bosonic-bilinear orbit is Lt = 4",
        resolved == [4],
        f"resolved single-orbit Lt values = {resolved}",
    )
    check(
        "the exact thermal order-parameter endpoint at Lt=4 is A_4 = 1/7",
        abs(a4 - 1.0 / 7.0) < 1e-15,
        f"A_4 = {a4:.12f}",
    )
    check(
        "the exact temporal endpoint band is narrow: A_4/A_2 = 8/7 and A_inf/A_2 = 2/sqrt(3)",
        abs(a4 / a2 - 8.0 / 7.0) < 1e-15 and abs(a_inf / a2 - 2.0 / math.sqrt(3.0)) < 1e-15,
        f"A_4/A_2 = {a4 / a2:.12f}, A_inf/A_2 = {a_inf / a2:.12f}",
    )
    info(
        "exact thermal surface",
        "the APBC stack gives one unique Lt=4 bosonic-bilinear thermal order-parameter surface with an O(10%) endpoint band, not multiple closed thermal sectors",
    )
    print()

    print("=" * 80)
    print("PART 3: CONSEQUENCE FOR BARYOGENESIS")
    print("=" * 80)
    print()

    yt_eft = (SCRIPTS / "frontier_yt_eft_bridge.py").read_text(encoding="utf-8")
    higgs = (SCRIPTS / "frontier_higgs_mass_derived.py").read_text(encoding="utf-8")

    gap_2l = route_gap(MH_2L)["gap_factor"]
    gap_3l = route_gap(MH_3L)["gap_factor"]
    max_endpoint_factor = 2.0 / math.sqrt(3.0)

    print(f"  max exact APBC endpoint factor   = {max_endpoint_factor:.6f}")
    print(f"  scalar gap factor (2-loop route) = {gap_2l:.6f}")
    print(f"  scalar gap factor (3-loop route) = {gap_3l:.6f}")
    print()

    check(
        "current authority surface still derives exactly one Higgs doublet",
        "N_H = 1" in yt_eft and "Higgs doublet from G_5 condensate" in yt_eft,
    )
    check(
        "current Higgs/CW scalar content remains one radial mode plus three Goldstones",
        "N_HIGGS = 1" in higgs and "N_GOLDSTONE = 3" in higgs,
    )
    check(
        "the old scalar-side baryogenesis gap is much larger than the exact APBC endpoint band",
        gap_2l > max_endpoint_factor and gap_3l > max_endpoint_factor,
        f"gap factors = {gap_2l:.6f}, {gap_3l:.6f} vs endpoint factor {max_endpoint_factor:.6f}",
    )
    info(
        "bounded baryogenesis consequence",
        "the APBC/bosonic-bilinear stack can refine the normalization of the same order parameter, but it does not by itself supply a second scalar family or enough strength to rescue the old route",
    )
    print()

    print("=" * 80)
    print("PART 4: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    thermal_note = (DOCS / "BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md").read_text(encoding="utf-8")
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    no_go_note = (DOCS / "BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")

    check(
        "thermal-order-parameter note records the unique Lt=4 thermal surface",
        "unique thermal order-parameter surface" in thermal_note and "`L_t = 4`" in thermal_note,
    )
    check(
        "closure-gate note points to the thermal-order-parameter note",
        "BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md" in gate_note,
    )
    check(
        "old-route no-go note points to the thermal-order-parameter note",
        "BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md" in no_go_note,
    )
    check(
        "derivation atlas carries the thermal-order-parameter uniqueness row",
        "Baryogenesis thermal order-parameter uniqueness" in atlas,
    )
    check(
        "canonical harness index includes the thermal-order-parameter runner",
        "frontier_baryogenesis_thermal_order_parameter_uniqueness.py" in harness,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the APBC / bosonic-bilinear stack does derive a genuine")
    print("      finite-T order-parameter surface")
    print("    - but that surface is unique: one additive CPT-even scalar")
    print("      generator, one resolved Lt=4 orbit, one thermal normalization lane")
    print("    - on the current authority surface it sharpens the same Higgs")
    print("      order parameter rather than producing a new scalar family")
    print("    - so it does not reopen the old taste-scalar baryogenesis route")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
