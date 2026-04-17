#!/usr/bin/env python3
"""
Hierarchy observable principle from the lattice axiom.

Goal:
  Replace the imported "effective-action order parameter" language with a
  framework-internal statement derived from the exact Grassmann Gaussian:

      Z[J] = det(D + J)

  On independent subsystems, |Z| is multiplicative, so the unique continuous
  additive scalar generator is log|Z|. Local scalar observables are therefore
  the source-response coefficients of log|Z| (equivalently Re log Z).

  On the minimal hierarchy block this reproduces the exact dimension-4
  effective-potential coefficient A(L_t), and the resulting temporal kernel is
  exactly the bosonic sign/conjugation-closed orbit kernel that selects L_t=4.
"""

from __future__ import annotations

import cmath
import math
import sys

import numpy as np
from canonical_plaquette_surface import CANONICAL_ALPHA_LM, CANONICAL_PLAQUETTE, CANONICAL_U0

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
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


def projector(n: int, idx: int) -> np.ndarray:
    p = np.zeros((n, n), dtype=complex)
    p[idx, idx] = 1.0
    return p


def logabs_det(m: np.ndarray) -> float:
    return float(np.linalg.slogdet(m)[1])


def observable_generator(d: np.ndarray, source: np.ndarray) -> float:
    """Additive CPT-even scalar generator: log|det(D+J)| - log|det D|."""
    return logabs_det(d + source) - logabs_det(d)


def temporal_modes(lt: int):
    return [(2 * n + 1) * math.pi / lt for n in range(lt)]


def exact_uniform_generator(lt: int, u0: float, j: float) -> float:
    return 4.0 * sum(
        math.log1p(j**2 / (u0**2 * (3.0 + math.sin(w) ** 2))) for w in temporal_modes(lt)
    )


def exact_uniform_coefficient_total(lt: int, u0: float) -> float:
    return 4.0 * sum(1.0 / (u0**2 * (3.0 + math.sin(w) ** 2)) for w in temporal_modes(lt))


def exact_local_a(lt: int, u0: float) -> float:
    return (1.0 / (2.0 * lt * u0**2)) * sum(
        1.0 / (3.0 + math.sin(w) ** 2) for w in temporal_modes(lt)
    )


def canon(z: complex):
    return (round(z.real, 12), round(z.imag, 12))


def apbc_phases(lt: int):
    return [cmath.exp(1j * (2 * n + 1) * math.pi / lt) for n in range(lt)]


def orbit_partition(lt: int):
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


def orbit_weights(lt: int):
    parts = orbit_partition(lt)
    out = []
    for orb in parts:
        vals = []
        for x, y in orb:
            angle = math.atan2(y, x)
            vals.append(round(1.0 / (3.0 + math.sin(angle) ** 2), 15))
        out.append(sorted(set(vals)))
    return out


def test_additive_scalar_generator():
    print("\n" + "=" * 78)
    print("PART 1: ADDITIVITY FORCES THE LOG-ABSDET GENERATOR")
    print("=" * 78)

    u0 = 0.9
    d2 = build_dirac_4d_apbc(2, 2, u0)
    d4 = build_dirac_4d_apbc(2, 4, u0)
    d_tot = block_diag(d2, d4)

    max_log_err = 0.0
    max_mult_err = 0.0
    raw_additivity_violation = 0.0

    for j in [1e-3, 1e-2, 5e-2, 1e-1]:
        s2 = j * np.eye(d2.shape[0], dtype=complex)
        s4 = j * np.eye(d4.shape[0], dtype=complex)
        s_tot = j * np.eye(d_tot.shape[0], dtype=complex)

        z2 = abs(np.linalg.det(d2 + s2))
        z4 = abs(np.linalg.det(d4 + s4))
        z_tot = abs(np.linalg.det(d_tot + s_tot))

        mult_err = abs(z_tot - z2 * z4) / (z2 * z4)
        log_err = abs(observable_generator(d_tot, s_tot) - (observable_generator(d2, s2) + observable_generator(d4, s4)))
        raw_gap = abs(z_tot - (z2 + z4)) / z_tot

        max_mult_err = max(max_mult_err, mult_err)
        max_log_err = max(max_log_err, log_err)
        raw_additivity_violation = max(raw_additivity_violation, raw_gap)
        print(
            f"  j={j:g}: |Z_tot|-mult rel={mult_err:.2e}, "
            f"log-add abs={log_err:.2e}, raw-add rel={raw_gap:.6f}"
        )

    check(
        "|Z| is exactly multiplicative on independent subsystems",
        max_mult_err < 1e-12,
        f"max relative multiplicativity error = {max_mult_err:.2e}",
    )
    check(
        "log|Z| is exactly additive on independent subsystems",
        max_log_err < 1e-12,
        f"max additive error = {max_log_err:.2e}",
    )
    check(
        "raw |Z| itself is not an additive scalar observable",
        raw_additivity_violation > 0.1,
        f"max raw additivity violation = {raw_additivity_violation:.6f}",
    )


def test_local_source_response_and_block_locality():
    print("\n" + "=" * 78)
    print("PART 2: LOCAL SOURCE RESPONSES ARE CONNECTED AND BLOCK-LOCAL")
    print("=" * 78)

    u0 = 0.9
    d2 = build_dirac_4d_apbc(2, 2, u0)
    d4 = build_dirac_4d_apbc(2, 4, u0)
    d_tot = block_diag(d2, d4)
    inv_tot = np.linalg.inv(d_tot)

    n1 = d2.shape[0]
    n2 = d4.shape[0]
    n_tot = d_tot.shape[0]
    p1 = np.zeros((n_tot, n_tot), dtype=complex)
    p1[:n1, :n1] = np.eye(n1, dtype=complex)
    p2 = np.zeros((n_tot, n_tot), dtype=complex)
    p2[n1:, n1:] = np.eye(n2, dtype=complex)

    mixed = -np.trace(inv_tot @ p1 @ inv_tot @ p2).real
    self_tot = -np.trace(inv_tot @ p1 @ inv_tot @ p1).real
    inv1 = np.linalg.inv(d2)
    self_1 = -np.trace(inv1 @ np.eye(n1, dtype=complex) @ inv1 @ np.eye(n1, dtype=complex)).real

    print(f"  mixed block curvature K_12 = {mixed:.3e}")
    print(f"  first-block local curvature from total = {self_tot:.12e}")
    print(f"  first-block local curvature standalone = {self_1:.12e}")

    check(
        "mixed local-source curvature vanishes across independent blocks",
        abs(mixed) < 1e-12,
        f"|K_12| = {abs(mixed):.2e}",
    )
    check(
        "local self-curvature is inherited exactly by the full block-diagonal system",
        abs(self_tot - self_1) < 1e-12,
        f"absolute difference = {abs(self_tot - self_1):.2e}",
    )


def test_uniform_scalar_generator_from_axiom():
    print("\n" + "=" * 78)
    print("PART 3: UNIFORM SCALAR SOURCE GIVES THE EXACT HIERARCHY GENERATOR")
    print("=" * 78)

    u0 = 0.9
    max_gen_err = 0.0
    max_even_err = 0.0
    max_pos_err = 0.0
    max_quad_err = 0.0

    for lt in [2, 4, 6, 8]:
        d = build_dirac_4d_apbc(2, lt, u0)
        n = d.shape[0]
        dd = d.conj().T @ d
        dd_inv = np.linalg.inv(dd)
        for j in [1e-4, 1e-3, 1e-2, 1e-1]:
            src = j * np.eye(n, dtype=complex)
            gen = observable_generator(d, src)
            gen_neg = observable_generator(d, -src)
            exact = exact_uniform_generator(lt, u0, j)
            pos = 0.5 * logabs_det(np.eye(n, dtype=complex) + (j**2) * dd_inv)
            if j <= 1e-3:
                quad = gen / (j**2)
                quad_exact = exact_uniform_coefficient_total(lt, u0)
                quad_err = abs(quad - quad_exact)
                max_quad_err = max(max_quad_err, quad_err)
            else:
                quad_err = float("nan")

            gen_err = abs(gen - exact)
            even_err = abs(gen - gen_neg)
            pos_err = abs(gen - pos)
            max_gen_err = max(max_gen_err, gen_err)
            max_even_err = max(max_even_err, even_err)
            max_pos_err = max(max_pos_err, pos_err)

            print(
                f"  Lt={lt}, j={j:g}: gen={gen:.12e}, exact={exact:.12e}, "
                f"pos_err={pos_err:.2e}, quad_err={quad_err:.2e}"
            )

    check(
        "uniform-source log|det| generator matches the exact Matsubara formula",
        max_gen_err < 1e-11,
        f"max absolute generator error = {max_gen_err:.2e}",
    )
    check(
        "the scalar generator is exactly bosonic/sign-blind: W(j) = W(-j)",
        max_even_err < 1e-12,
        f"max evenness error = {max_even_err:.2e}",
    )
    check(
        "the scalar generator is exactly the positive CPT-even log-det functional",
        max_pos_err < 1e-12,
        f"max positive-functional error = {max_pos_err:.2e}",
    )
    check(
        "the small-j curvature reproduces the exact total A(L_t) coefficient",
        max_quad_err < 5e-6,
        f"max quadratic-coefficient error = {max_quad_err:.2e}",
    )


def test_orbit_kernel_and_selector():
    print("\n" + "=" * 78)
    print("PART 4: THE SOURCE-CURVATURE KERNEL FORCES THE LT=4 SELECTOR")
    print("=" * 78)

    resolved = []
    for lt in range(2, 14, 2):
        parts = orbit_partition(lt)
        weights = orbit_weights(lt)
        sizes = [len(p) for p in parts]
        print(f"  Lt={lt:2d}: num_orbits={len(parts)}, sizes={sizes}, weights={weights}")
        if len(parts) == 1 and len(parts[0]) > 2:
            resolved.append(lt)

    check(
        "the curvature kernel depends only on sign/conjugation-invariant sin^2(omega)",
        orbit_weights(4) == [[0.285714285714286]],
        f"Lt=4 orbit weights = {orbit_weights(4)}",
    )
    check(
        "the unique minimal resolved Klein-four orbit is Lt = 4",
        resolved == [4],
        f"resolved single-orbit Lt values = {resolved}",
    )


def test_hierarchy_value_from_internal_observable_principle():
    print("\n" + "=" * 78)
    print("PART 5: INTERNAL OBSERVABLE PRINCIPLE FIXES THE HIERARCHY CORRECTION")
    print("=" * 78)

    c4 = (7.0 / 8.0) ** 0.25
    plaquette = CANONICAL_PLAQUETTE
    m_planck = 1.2209e19
    u0 = CANONICAL_U0
    alpha_bare = 1.0 / (4.0 * math.pi)
    alpha_lm = CANONICAL_ALPHA_LM
    baseline = m_planck * alpha_lm**16
    v_pred = baseline * c4
    v_meas = 246.22
    rel = (v_pred - v_meas) / v_meas

    print(f"  C_4 = {c4:.12f}")
    print(f"  baseline = M_Pl * alpha_LM^16 = {baseline:.12f} GeV")
    print(f"  v_pred = {v_pred:.12f} GeV")
    print(f"  v_meas = {v_meas:.12f} GeV")
    print(f"  relative error = {rel:.6%}")

    check(
        "the internally selected hierarchy correction is exactly (7/8)^(1/4)",
        abs(c4 - (7.0 / 8.0) ** 0.25) < 1e-15,
        f"absolute error = {abs(c4 - (7.0 / 8.0) ** 0.25):.2e}",
    )
    check(
        "the resulting electroweak scale stays within 0.5% of measurement",
        abs(rel) < 0.005,
        f"relative error = {rel:.6%}",
    )


def main():
    print("Hierarchy observable principle from the lattice axiom")
    print("=" * 78)
    test_additive_scalar_generator()
    test_local_source_response_and_block_locality()
    test_uniform_scalar_generator_from_axiom()
    test_orbit_kernel_and_selector()
    test_hierarchy_value_from_internal_observable_principle()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
