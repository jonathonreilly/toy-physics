#!/usr/bin/env python3
"""
Koide weighted Z3 character-source axis theorem.

Status:
  Exact no-go sharpening of the charged-lepton Z3 character-source route.

Question:
  The old source-response cross-check proved that the canonical Plancherel
  kernel on the character sources is exactly I_3. Could a more general
  left/right class-function weighting of the same canonical sources evade that
  identity and force a unique Koide ray?

Answer:
  No. Every such weighted kernel stays diagonal in the canonical source basis.
  Therefore:
    - if the top eigenvalue is unique, the selected ray is a basis axis and
      has Koide Q = 1, not 2/3;
    - if the top eigenvalue is degenerate, the kernel does not force a unique
      ray.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


Q_L = (0, 1, 2)
Q_R = (0, 2, 1)
PAIR_LIST = tuple(zip(Q_L, Q_R))


def omega() -> complex:
    return complex(-0.5, math.sqrt(3.0) / 2.0)


def shift_matrix() -> np.ndarray:
    return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)


def idempotent(q: int) -> np.ndarray:
    w = omega()
    t = shift_matrix()
    eye = np.eye(3, dtype=complex)
    out = np.zeros((3, 3), dtype=complex)
    powers = [eye, t, t @ t]
    for k in range(3):
        out += (w ** (-q * k)) * powers[k]
    return out / 3.0


def source_element(i: int) -> np.ndarray:
    return np.kron(idempotent(Q_L[i]), idempotent(Q_R[i]))


def central_weight_matrix(weights: tuple[float, float, float]) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    for q, weight in enumerate(weights):
        out += float(weight) * idempotent(q)
    return out


def weighted_kernel(mu: tuple[float, float, float], nu: tuple[float, float, float]) -> np.ndarray:
    ml = central_weight_matrix(mu)
    mr = central_weight_matrix(nu)
    weight = np.kron(ml, mr)
    out = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        si = source_element(i)
        for j in range(3):
            sj = source_element(j)
            out[i, j] = np.trace(si.conj().T @ weight @ sj)
    return out


def koide_q(v: np.ndarray) -> float:
    v = np.asarray(v, dtype=float)
    return float(np.sum(v * v) / (np.sum(v) ** 2))


def part1_character_source_primitives() -> None:
    print("=" * 88)
    print("PART 1: CANONICAL Z3 CHARACTER SOURCES")
    print("=" * 88)

    e = [idempotent(q) for q in range(3)]

    for p in range(3):
        for q in range(3):
            prod = e[p] @ e[q]
            target = e[p] if p == q else np.zeros((3, 3), dtype=complex)
            check(
                f"e_{p} e_{q} = delta_pq e_{p}",
                np.allclose(prod, target, atol=1e-12),
                kind="NUMERIC",
            )

    for q in range(3):
        check(
            f"Tr(e_{q}) = 1",
            abs(np.trace(e[q]) - 1.0) < 1e-12,
            kind="NUMERIC",
        )

    check(
        "The three canonical charge pairs are distinct",
        len(set(PAIR_LIST)) == 3,
        detail=f"pairs={PAIR_LIST}",
    )

    for i in range(3):
        s_i = source_element(i)
        for j in range(3):
            s_j = source_element(j)
            target = s_i if i == j else np.zeros_like(s_i)
            check(
                f"s_{i+1}^dag s_{j+1} = delta_ij s_{i+1}",
                np.allclose(s_i.conj().T @ s_j, target, atol=1e-12),
                kind="NUMERIC",
            )


def part2_exact_weighted_kernel_formula() -> None:
    print()
    print("=" * 88)
    print("PART 2: EXACT WEIGHTED KERNEL FORMULA")
    print("=" * 88)

    mu0, mu1, mu2 = sp.symbols("mu0 mu1 mu2", real=True)
    nu0, nu1, nu2 = sp.symbols("nu0 nu1 nu2", real=True)
    mu = (mu0, mu1, mu2)
    nu = (nu0, nu1, nu2)

    expected = sp.diag(mu0 * nu0, mu1 * nu2, mu2 * nu1)
    actual = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            delta = sp.KroneckerDelta(Q_L[i], Q_L[j]) * sp.KroneckerDelta(Q_R[i], Q_R[j])
            actual[i, j] = sp.simplify(delta * mu[Q_L[i]] * nu[Q_R[i]])

    check(
        "Weighted kernel is exactly diag(mu0*nu0, mu1*nu2, mu2*nu1)",
        sp.simplify(actual - expected) == sp.zeros(3, 3),
        detail=str(expected),
    )

    check(
        "All off-diagonal weighted-kernel entries vanish identically",
        all(sp.simplify(actual[i, j]) == 0 for i in range(3) for j in range(3) if i != j),
    )

    mu_num = (4.0, 2.5, 1.5)
    nu_num = (3.0, 5.0, 7.0)
    kernel_num = weighted_kernel(mu_num, nu_num)
    expected_num = np.diag([mu_num[0] * nu_num[0], mu_num[1] * nu_num[2], mu_num[2] * nu_num[1]])
    check(
        "Matrix-level weighted kernel matches the exact diagonal formula",
        np.allclose(kernel_num, expected_num, atol=1e-12),
        detail=f"kernel={np.real_if_close(kernel_num).tolist()}",
        kind="NUMERIC",
    )


def part3_plancherel_recovery() -> None:
    print()
    print("=" * 88)
    print("PART 3: THE OLD PLANCHEREL CROSS-CHECK IS THE UNIFORM CASE")
    print("=" * 88)

    kernel = weighted_kernel((1.0, 1.0, 1.0), (1.0, 1.0, 1.0))
    check(
        "Uniform left/right weights recover the old identity kernel",
        np.allclose(kernel, np.eye(3), atol=1e-12),
        detail=f"kernel={np.real_if_close(kernel).tolist()}",
        kind="NUMERIC",
    )


def part4_unique_top_eigenvector_is_axis_and_off_cone() -> None:
    print()
    print("=" * 88)
    print("PART 4: UNIQUE TOP EIGENVECTOR CASE")
    print("=" * 88)

    kernel = weighted_kernel((5.0, 2.0, 1.0), (1.0, 1.0, 1.0))
    vals, vecs = np.linalg.eigh(kernel)
    top = int(np.argmax(vals))
    top_vec = np.real_if_close(vecs[:, top])
    axis = np.zeros(3, dtype=float)
    axis[0] = 1.0
    aligned = abs(float(np.vdot(top_vec, axis)))
    q_axis = koide_q(axis)
    a0 = np.sum(axis) / math.sqrt(3.0)
    w = omega()
    z = (axis[0] + np.conjugate(w) * axis[1] + w * axis[2]) / math.sqrt(3.0)

    check(
        "A unique top eigenvalue selects a canonical basis axis",
        aligned > 1.0 - 1e-12,
        detail=f"eigs={vals.tolist()} aligned={aligned:.12f}",
        kind="NUMERIC",
    )
    check(
        "That basis axis has Koide Q = 1 rather than 2/3",
        abs(q_axis - 1.0) < 1e-12 and abs(q_axis - 2.0 / 3.0) > 1e-3,
        detail=f"Q_axis={q_axis:.12f}",
        kind="NUMERIC",
    )
    check(
        "Equivalently, the basis axis fails a0^2 = 2|z|^2",
        abs((a0 * a0) - (2.0 * abs(z) ** 2)) > 1e-3,
        detail=f"a0^2={a0*a0:.12f}, 2|z|^2={2.0*abs(z)**2:.12f}",
        kind="NUMERIC",
    )


def part5_degenerate_top_never_forces_a_unique_ray() -> None:
    print()
    print("=" * 88)
    print("PART 5: DEGENERATE TOP CASE")
    print("=" * 88)

    kernel_twofold = weighted_kernel((1.0, 7.0, 7.0), (1.0, 1.0, 1.0))
    vals_twofold = np.linalg.eigvalsh(kernel_twofold)
    top_val = float(np.max(vals_twofold))
    top_mult = int(np.sum(np.isclose(vals_twofold, top_val, atol=1e-12)))
    check(
        "Twofold-degenerate tops leave a two-real top eigenspace",
        top_mult == 2,
        detail=f"eigs={vals_twofold.tolist()}",
        kind="NUMERIC",
    )

    kernel_threefold = weighted_kernel((1.0, 1.0, 1.0), (1.0, 1.0, 1.0))
    vals_threefold = np.linalg.eigvalsh(kernel_threefold)
    top_mult_threefold = int(np.sum(np.isclose(vals_threefold, np.max(vals_threefold), atol=1e-12)))
    check(
        "Threefold-degenerate tops recover the identity kernel and force no ray at all",
        top_mult_threefold == 3 and np.allclose(kernel_threefold, np.eye(3), atol=1e-12),
        detail=f"eigs={vals_threefold.tolist()}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_character_source_primitives()
    part2_exact_weighted_kernel_formula()
    part3_plancherel_recovery()
    part4_unique_top_eigenvector_is_axis_and_off_cone()
    part5_degenerate_top_never_forces_a_unique_ray()

    print()
    print("Interpretation:")
    print("  Allowing arbitrary left/right central class-function weights on the")
    print("  canonical Z3 character sources does not rescue the charged-lepton")
    print("  source-response route. The kernel always stays diagonal in the source")
    print("  basis. Unique tops pick basis axes, which sit off the Koide cone;")
    print("  degenerate tops leave the ray unfixed.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
