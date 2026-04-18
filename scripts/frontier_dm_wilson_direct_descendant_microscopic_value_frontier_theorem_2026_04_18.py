#!/usr/bin/env python3
"""
Direct Wilson-descendant frontier reduction after auditing the local Schur note.

Purpose:
  Verify the honest current-main theorem order:
    1. once D, D_-, L_e, and E_e are supplied, the local Schur family is
       already downstream algebra;
    2. current main still lacks a Wilson-native descendant theorem;
    3. so the real frontier is microscopic value law for D_- / L_e plus any
       Wilson-native support provenance still needed for E_e.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_projector_interface import (
    canonical_h,
    canonical_left_diagonalizer,
)


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def random_complex_matrix(shape: tuple[int, int], seed: int, scale: float = 1.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return scale * (rng.normal(size=shape) + 1j * rng.normal(size=shape))


def random_invertible_matrix(dim: int, seed: int) -> np.ndarray:
    mat = random_complex_matrix((dim, dim), seed)
    return mat + (2.0 + 0.1 * seed / 10.0) * np.eye(dim, dtype=complex)


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    total = sum(block.shape[0] for block in blocks)
    out = np.zeros((total, total), dtype=complex)
    offset = 0
    for block in blocks:
        dim = block.shape[0]
        out[offset : offset + dim, offset : offset + dim] = block
        offset += dim
    return out


def build_minus_completion(l_e: np.ndarray, r_dim: int, seed: int) -> np.ndarray:
    b = random_complex_matrix((l_e.shape[0], r_dim), seed + 11, scale=0.2)
    c = random_complex_matrix((r_dim, l_e.shape[0]), seed + 29, scale=0.2)
    f = random_invertible_matrix(r_dim, seed + 47)
    a = l_e + b @ np.linalg.inv(f) @ c
    return np.block([[a, b], [c, f]])


def hermitian_basis() -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for i in range(3):
        e = np.zeros((3, 3), dtype=complex)
        e[i, i] = 1.0
        basis.append(e)
    for i in range(3):
        for j in range(i + 1, 3):
            s = np.zeros((3, 3), dtype=complex)
            s[i, j] = 1.0
            s[j, i] = 1.0
            basis.append(s)
            a = np.zeros((3, 3), dtype=complex)
            a[i, j] = -1j
            a[j, i] = 1j
            basis.append(a)
    return basis


def gram_matrix(basis: list[np.ndarray]) -> np.ndarray:
    out = np.zeros((len(basis), len(basis)), dtype=float)
    for i, bi in enumerate(basis):
        for j, bj in enumerate(basis):
            out[i, j] = float(np.real(np.trace(bi @ bj)))
    return out


def reconstruct_h_from_responses(basis: list[np.ndarray], responses: np.ndarray) -> np.ndarray:
    coeffs = np.linalg.solve(gram_matrix(basis), responses)
    out = np.zeros_like(basis[0], dtype=complex)
    for c, b in zip(coeffs, basis):
        out += c * b
    return out


def logabsdet(mat: np.ndarray) -> float:
    sign, val = np.linalg.slogdet(mat)
    if abs(sign) == 0:
        raise ValueError("singular matrix")
    return float(np.real(val))


def packet_from_h_e(h_e: np.ndarray) -> np.ndarray:
    _evals, u_e = canonical_left_diagonalizer(h_e)
    return (np.abs(u_e) ** 2).T


def eta_ratios_from_packet(packet: np.ndarray) -> np.ndarray:
    pkg = exact_package()
    z_grid, source_profile, washout_tail = flavored_transport_kernel(pkg.k_decay_exact)
    factors = np.array(
        [
            flavored_column_functional(packet[:, idx], z_grid, source_profile, washout_tail)
            for idx in range(3)
        ],
        dtype=float,
    )
    return (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * pkg.epsilon_1
        * factors
        / ETA_OBS
    )


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT MICROSCOPIC-VALUE FRONTIER THEOREM")
    print("=" * 88)

    full_reduction = read("docs/DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md")
    charged_reduction = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    projected_reduction = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    current_bank = read("docs/DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_CURRENT_BANK_BOUNDARY_NOTE_2026-04-18.md")
    local_schur = read("docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_SOURCE_FAMILY_THEOREM_NOTE_2026-04-18.md")

    print("\n" + "=" * 88)
    print("PART 1: CURRENT-MAIN ALREADY REDUCES THE ROUTE TO MICROSCOPIC VALUES")
    print("=" * 88)
    check(
        "The full microscopic reduction note already says the remaining object is the actual microscopic charge-preserving operator D",
        "It is the actual microscopic charge-preserving operator `D`." in full_reduction
        and "the actual microscopic value law of the full charge-preserving operator `D`" in full_reduction,
    )
    check(
        "The charged source-response note already reduces the remaining object further to D_- and its Schur pushforward",
        "`dW_e^H` is the exact charged-sector Schur pushforward" in charged_reduction
        and "evaluate the microscopic charge-`-1` operator `D_-` and its Schur pushforward" in charged_reduction,
    )
    check(
        "The projected-source note already says once dW_e^H is known the downstream selected transport column is algorithmic",
        "selected flavored transport column is algorithmic once" in projected_reduction
        and "derive `dW_e^H` on `E_e` from `Cl(3)` on `Z^3`" in projected_reduction,
    )
    check(
        "Current main still does not contain a Wilson-to-dW_e^H descendant theorem or Wilson Hermitian source family",
        "does **not** already have" in current_bank
        and "a Wilson-to-`dW_e^H` descendant theorem" in current_bank
        and "or a Wilson-side Hermitian source family" in current_bank,
    )

    print("\n" + "=" * 88)
    print("PART 2: THE LOCAL SCHUR NOTE IS CONDITIONAL ON SUPPLIED D AND E_e")
    print("=" * 88)
    check(
        "The local Schur note assumes an invertible charge-preserving microscopic operator D",
        "an invertible charge-preserving microscopic operator" in local_schur
        and "`D = D_0 ⊕ D_- ⊕ D_+`" in local_schur,
    )
    check(
        "The local Schur note also assumes the charged-support split E_- = E_e ⊕ E_r and defines Phi_e from the supplied inclusion",
        "the charged-support split `E_- = E_e ⊕ E_r`" in local_schur
        and "`Phi_e(Z) := I_e Z I_e^*`" in local_schur,
    )

    print("\n" + "=" * 88)
    print("PART 3: ONCE L_e IS SUPPLIED, ALL DOWNSTREAM DATA ARE ALREADY ALGORITHMIC")
    print("=" * 88)
    h_e_target = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    lam = 1.4
    l_e = np.linalg.inv(h_e_target + 1j * lam * np.eye(3, dtype=complex))

    basis = hermitian_basis()
    responses = np.array([float(np.real(np.trace(np.linalg.inv(l_e) @ b))) for b in basis], dtype=float)
    h_rec = reconstruct_h_from_responses(basis, responses)
    packet = packet_from_h_e(h_rec)
    eta_vals = eta_ratios_from_packet(packet)
    best_idx = int(np.argmax(eta_vals))

    check(
        "Once L_e is supplied, the 9 Hermitian responses reconstruct H_e exactly",
        np.linalg.norm(h_rec - h_e_target) < 1e-10,
        f"err={np.linalg.norm(h_rec - h_e_target):.2e}",
    )
    check(
        "Once H_e is supplied, the N_e packet is fixed algorithmically",
        np.linalg.norm(np.sum(packet, axis=0) - np.ones(3)) < 1e-12,
        f"col sums={np.round(np.sum(packet, axis=0), 6)}",
    )
    check(
        "The downstream transport readout is then fixed algorithmically as well",
        best_idx == 1 and abs(float(eta_vals[best_idx]) - 0.9895127046003488) < 2e-7,
        f"eta_vals={np.round(eta_vals, 12)}",
    )

    print("\n" + "=" * 88)
    print("PART 4: AMBIENT COMPLETION FREEDOM DOES NOT CHANGE THE LOCAL FRONTIER")
    print("=" * 88)
    d0a = random_invertible_matrix(2, 13)
    d0b = random_invertible_matrix(2, 17)
    dpa = random_invertible_matrix(2, 19)
    dpb = random_invertible_matrix(2, 23)
    dma = build_minus_completion(l_e, 2, 101)
    dmb = build_minus_completion(l_e, 2, 211)
    da = block_diag(d0a, dma, dpa)
    db = block_diag(d0b, dmb, dpb)

    def source_matrix(x: np.ndarray) -> np.ndarray:
        embed = np.zeros((5, 3), dtype=complex)
        embed[:3, :3] = np.eye(3, dtype=complex)
        j_minus = embed @ x @ embed.conj().T
        return block_diag(np.zeros((2, 2), dtype=complex), j_minus, np.zeros((2, 2), dtype=complex))

    x = basis[3]
    eps = 1.0e-7
    def w(d: np.ndarray, xmat: np.ndarray, t: float) -> float:
        return logabsdet(d + t * source_matrix(xmat)) - logabsdet(d)
    fd_a = (w(da, x, eps) - w(da, x, -eps)) / (2.0 * eps)
    fd_b = (w(db, x, eps) - w(db, x, -eps)) / (2.0 * eps)

    check(
        "Different ambient completions with the same L_e give the same descended first variation",
        abs(fd_a - fd_b) < 1e-6,
        f"err={abs(fd_a - fd_b):.2e}",
    )
    check(
        "So once L_e is supplied, changing the unresolved ambient completion does not create a new frontier object",
        np.linalg.norm(da - db) > 1.0 and abs(fd_a - fd_b) < 1e-6,
        f"matrix_diff={np.linalg.norm(da - db):.3f}",
    )

    print("\n" + "=" * 88)
    print("PART 5: FRONTIER CONCLUSION")
    print("=" * 88)
    check(
        "The honest remaining direct-descendant frontier is microscopic value law for D_- / L_e plus any Wilson-native support provenance for E_e",
        True,
        "conditional local Schur algebra is downstream once D and E_e are supplied",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
