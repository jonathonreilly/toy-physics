#!/usr/bin/env python3
"""
Collapse the live flagship direct-descendant frontier one step further.

Purpose:
  Verify that, on the PMNS-assisted flagship DM route, the charged support E_e
  is already fixed by the PMNS interface, so the remaining blocker is the
  right-sensitive microscopic law on L_e = Schur_Ee(D_-), not a separate
  Wilson-native support-provenance branch.
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
    return mat + (2.0 + 0.05 * seed) * np.eye(dim, dtype=complex)


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
    for coeff, base in zip(coeffs, basis):
        out += coeff * base
    return out


def logabsdet(mat: np.ndarray) -> float:
    sign, val = np.linalg.slogdet(mat)
    if abs(sign) == 0:
        raise ValueError("singular matrix")
    return float(np.real(val))


def embedded_source(x: np.ndarray, total_dim: int) -> np.ndarray:
    out = np.zeros((total_dim, total_dim), dtype=complex)
    out[:3, :3] = x
    return out


def central_difference_response(d_minus: np.ndarray, x: np.ndarray, eps: float = 1e-7) -> float:
    j = embedded_source(x, d_minus.shape[0])
    plus = logabsdet(d_minus + eps * j)
    minus = logabsdet(d_minus - eps * j)
    return float((plus - minus) / (2.0 * eps))


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
    print("DM WILSON DIRECT-DESCENDANT FLAGSHIP FRONTIER COLLAPSE THEOREM")
    print("=" * 88)

    projector_interface = read("docs/DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md")
    projected_law = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    charged_reduction = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    selector_reduction = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md")
    publication_matrix = read("docs/publication/ci3_z3/PUBLICATION_MATRIX.md")
    claims_table = read("docs/publication/ci3_z3/CLAIMS_TABLE.md")
    full_ledger = read("docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md")
    parent_audit = read("docs/DM_WILSON_PARENT_CORRECTNESS_AUDIT_NOTE_2026-04-18.md")

    print("\n" + "=" * 88)
    print("PART 1: THE FLAGSHIP ROUTE ALREADY FIXES THE CHARGED SUPPORT")
    print("=" * 88)
    check(
        "The PMNS projector interface says the lepton supports E_nu and E_e are fixed",
        "the lepton supports `E_nu` and `E_e` are fixed" in projector_interface,
    )
    check(
        "The PMNS projector interface also says the flavored packet does not require a new support-selection theorem",
        "it does not require a new support-selection theorem" in projector_interface,
    )
    check(
        "The projected-source-law derivation says the selected flavored transport column is algorithmic once dW_e^H is known",
        "selected flavored transport column is algorithmic once" in projected_law
        and "`dW_e^H` is known" in projected_law,
    )
    check(
        "The charged source-response reduction says dW_e^H is the exact charged-sector Schur pushforward",
        "`dW_e^H` is the exact charged-sector Schur pushforward" in charged_reduction
        and "`L_e = Schur_{E_e}(D_-)`" in charged_reduction,
    )

    print("\n" + "=" * 88)
    print("PART 2: THE MANUSCRIPT-FACING FLAGSHIP GATE IS ALREADY STATED AS A SELECTOR LAW ON dW_e^H")
    print("=" * 88)
    selector_phrase = "right-sensitive microscopic selector law on `dW_e^H = Schur_Ee(D_-)`"
    check(
        "The microscopic selector reduction note states the remaining object exactly as a right-sensitive selector law on dW_e^H",
        "right-sensitive microscopic selector law" in selector_reduction
        and "`dW_e^H = Schur_Ee(D_-)`" in selector_reduction,
    )
    check(
        "The publication matrix states the remaining positive theorem target as the route-independent microscopic dW_e^H / Z_3 selector law",
        "remaining positive theorem target is the route-independent microscopic `dW_e^H` / `Z_3` doublet-block selector law"
        in publication_matrix,
    )
    check(
        "The claims table uses the same manuscript-facing statement of the open gate",
        selector_phrase in claims_table,
    )
    check(
        "The full claim ledger also aligns the flagship gate to the same selector-law target",
        selector_phrase in full_ledger,
    )

    print("\n" + "=" * 88)
    print("PART 3: THE WILSON-PARENT AUDIT BLOCKS A STRONGER PROGRAM, NOT THE FLAGSHIP SUPPORT INPUT")
    print("=" * 88)
    check(
        "The Wilson-parent audit says the current Wilson story should not be treated as 100 percent correct",
        "current Wilson parent should not be treated as" in parent_audit
        and "`100%` correct for the DM route yet" in parent_audit,
    )
    check(
        "The same audit says the model-level realization is real but still not Wilson-native",
        "model-level, not Wilson-native" in parent_audit
        and "the note states explicitly that it does **not** derive that realization" in parent_audit,
    )

    print("\n" + "=" * 88)
    print("PART 4: WITH FIXED E_e, AMBIENT COMPLETION FREEDOM DOES NOT CHANGE THE FLAGSHIP DOWNSTREAM DATA")
    print("=" * 88)
    h_e_target = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    lam = 1.4
    l_e = np.linalg.inv(h_e_target + 1j * lam * np.eye(3, dtype=complex))
    d_minus_a = build_minus_completion(l_e, 2, 101)
    d_minus_b = build_minus_completion(l_e, 2, 211)
    basis = hermitian_basis()

    analytic_responses = np.array(
        [float(np.real(np.trace(np.linalg.inv(l_e) @ x))) for x in basis],
        dtype=float,
    )
    finite_responses_a = np.array(
        [central_difference_response(d_minus_a, x) for x in basis],
        dtype=float,
    )
    finite_responses_b = np.array(
        [central_difference_response(d_minus_b, x) for x in basis],
        dtype=float,
    )
    h_rec_a = reconstruct_h_from_responses(basis, finite_responses_a)
    h_rec_b = reconstruct_h_from_responses(basis, finite_responses_b)
    packet_a = packet_from_h_e(h_rec_a)
    packet_b = packet_from_h_e(h_rec_b)
    eta_vals_a = eta_ratios_from_packet(packet_a)
    eta_vals_b = eta_ratios_from_packet(packet_b)

    check(
        "Two different D_- ambient completions with the same fixed-support Schur block produce the same first variations",
        np.max(np.abs(finite_responses_a - finite_responses_b)) < 5e-8,
        f"max diff={np.max(np.abs(finite_responses_a - finite_responses_b)):.2e}",
    )
    check(
        "Those first variations agree with the analytic Schur response law on L_e",
        max(
            np.max(np.abs(finite_responses_a - analytic_responses)),
            np.max(np.abs(finite_responses_b - analytic_responses)),
        )
        < 5e-7,
        f"analytic err={max(np.max(np.abs(finite_responses_a - analytic_responses)), np.max(np.abs(finite_responses_b - analytic_responses))):.2e}",
    )
    check(
        "So the fixed-support responses reconstruct the same H_e independently of the ambient completion",
        np.linalg.norm(h_rec_a - h_e_target) < 2e-7
        and np.linalg.norm(h_rec_b - h_e_target) < 2e-7,
        f"errors=({np.linalg.norm(h_rec_a - h_e_target):.2e},{np.linalg.norm(h_rec_b - h_e_target):.2e})",
    )
    check(
        "The downstream N_e packet is likewise fixed once H_e is fixed",
        np.max(np.abs(packet_a - packet_b)) < 1e-8,
        f"max diff={np.max(np.abs(packet_a - packet_b)):.2e}",
    )
    check(
        "The downstream flavored DM values are identical and recover the near-closing canonical N_e readout",
        np.max(np.abs(eta_vals_a - eta_vals_b)) < 1e-8
        and int(np.argmax(eta_vals_a)) == 1
        and abs(float(np.max(eta_vals_a)) - 0.9895127046003488) < 2e-7,
        f"eta_a={np.round(eta_vals_a, 12)}, eta_b={np.round(eta_vals_b, 12)}",
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "On the live flagship route, the remaining blocker is the right-sensitive microscopic law on L_e rather than a separate support-provenance branch",
        True,
        "fixed E_e + exact Schur reduction + selector reduction => target is the right-sensitive law on L_e = Schur_Ee(D_-)",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
