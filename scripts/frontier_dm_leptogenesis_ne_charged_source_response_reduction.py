#!/usr/bin/env python3
"""
DM leptogenesis N_e charged source-response reduction.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Record two pieces of content:

  (A) Algebraic Schur-pushforward identities showing that, GIVEN a
      charged-lepton projected Hermitian source law dW_e^H, the PMNS-assisted
      flavored DM chain is algorithmic from there on (Parts 1 and 2). These
      are exact at retained grade.

  (B) A consistency check at a stipulated canonical N_e benchmark sample,
      showing that the chain reproduces the same residual ~1.01x miss
      already documented in the sibling LAST_MILE note's
      ETA_NE_CANONICAL = 0.9895125971972334 (Part 3). This is NOT a
      sole-axiom derivation: the canonical (x, y, delta) triple and the
      target H_e are stipulated inputs, and the
      build_charge_preserving_operator_with_target_le routine is a
      construction-by-target, not a derivation of D_- from Cl(3) on Z^3.

  See DM_LEPTOGENESIS_NE_ACTIVE_COLUMN_AXIOM_BOUNDARY_NOTE_2026-04-16.md
  for the explicit negative boundary: the selected N_e column is not fixed
  by the currently native PMNS data on its own.
"""

from __future__ import annotations

import sys

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

PASS_COUNT = 0
FAIL_COUNT = 0

# Stipulated benchmark values (NOT derived from the sole axiom).
# These are the canonical N_e off-seed sample reused across sibling notes;
# see DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE for the published
# benchmark and DM_LEPTOGENESIS_NE_ACTIVE_COLUMN_AXIOM_BOUNDARY for the
# negative axiom-boundary result on the selected column.
ETA_NE_CANONICAL_SIBLING = 0.9895125971972334
ETA_ONE_FLAVOR_AUTHORITY = 0.188785929502


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


def schur_eff(a: np.ndarray, b: np.ndarray, c: np.ndarray, f: np.ndarray) -> np.ndarray:
    return a - b @ np.linalg.inv(f) @ c


def logabsdet(m: np.ndarray) -> float:
    sign, val = np.linalg.slogdet(m)
    _ = sign
    return float(val)


def source_response(d: np.ndarray, j: np.ndarray) -> float:
    return logabsdet(d + j) - logabsdet(d)


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


def reconstruct_h_from_responses(responses: list[float]) -> np.ndarray:
    h = np.zeros((3, 3), dtype=complex)
    h[0, 0] = responses[0]
    h[1, 1] = responses[1]
    h[2, 2] = responses[2]
    idx = 3
    for i in range(3):
        for j in range(i + 1, 3):
            sym = responses[idx]
            asym = responses[idx + 1]
            h[i, j] = 0.5 * (sym - 1j * asym)
            h[j, i] = 0.5 * (sym + 1j * asym)
            idx += 2
    return h


def packet_from_h_e(h_e: np.ndarray) -> np.ndarray:
    _evals, u_e = canonical_left_diagonalizer(h_e)
    return (np.abs(u_e) ** 2).T


def transport_column_values(packet: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pkg = exact_package()
    z_grid, source_profile, washout_tail = flavored_transport_kernel(pkg.k_decay_exact)
    factors = np.array(
        [
            flavored_column_functional(packet[:, idx], z_grid, source_profile, washout_tail)
            for idx in range(3)
        ],
        dtype=float,
    )
    eta_vals = (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * pkg.epsilon_1
        * factors
        / ETA_OBS
    )
    return factors, eta_vals


def build_charge_preserving_operator_with_target_le(target_le: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Construct a charge-preserving operator whose charge -1 Schur complement
    equals the supplied target_le.

    This is a CONSTRUCTION-BY-TARGET, not a derivation of D_- from Cl(3) on Z^3.
    Its purpose is to exhibit the algebraic Schur-pushforward identities of
    Parts 1 and 2 on a concrete operator that realises a chosen H_e target,
    not to evaluate D_- on the sole axiom.
    """
    rng = np.random.default_rng(417)
    f0_raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    f0 = 0.5 * (f0_raw + f0_raw.conj().T) + 4.0 * np.eye(2, dtype=complex)
    fm_raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    fm = 0.5 * (fm_raw + fm_raw.conj().T) + 4.0 * np.eye(2, dtype=complex)
    fp_raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    fp = 0.5 * (fp_raw + fp_raw.conj().T) + 4.0 * np.eye(2, dtype=complex)

    b0 = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    bm = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))

    # Choose the charge -1 block so its exact Schur complement is the canonical H_e target.
    am = np.asarray(target_le, dtype=complex) + bm @ np.linalg.inv(fm) @ bm.conj().T

    # Neutral and positive sectors only provide a charge-preserving completion.
    target_lnu = np.diag(np.array([2.1, 2.5, 3.2], dtype=float))
    a0 = target_lnu + b0 @ np.linalg.inv(f0) @ b0.conj().T

    d0 = np.block([[a0, b0], [b0.conj().T, f0]])
    dm = np.block([[am, bm], [bm.conj().T, fm]])
    dplus = fp

    zeros_52 = np.zeros((5, 2), dtype=complex)
    zeros_25 = np.zeros((2, 5), dtype=complex)
    d = np.block(
        [
            [d0, np.zeros((5, 5), dtype=complex), zeros_52],
            [np.zeros((5, 5), dtype=complex), dm, zeros_52],
            [zeros_25, zeros_25, dplus],
        ]
    )
    q = np.diag(np.array([0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 1, 1], dtype=float))
    return d, q


def part1_the_charged_hermitian_source_law_is_exact_schur_pushforward() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE CHARGED HERMITIAN SOURCE LAW IS EXACT SCHUR PUSHFORWARD")
    print("=" * 88)
    print("  Algebraic identity (retained-grade). Inputs (target H_e) are")
    print("  stipulated; this part does not derive H_e from the sole axiom.")
    print()

    # Stipulated canonical N_e off-seed benchmark (also used by the
    # LAST_MILE sibling). NOT derived from Cl(3) on Z^3.
    h_e_target = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    d, q = build_charge_preserving_operator_with_target_le(h_e_target)
    dm = d[5:10, 5:10]
    l_e = schur_eff(dm[:3, :3], dm[:3, 3:5], dm[3:5, :3], dm[3:5, 3:5])

    x_e = np.array(
        [
            [0.08, 0.0, 0.01j],
            [0.0, -0.03, 0.02],
            [-0.01j, 0.02, 0.06],
        ],
        dtype=complex,
    )
    j_full = np.zeros_like(d)
    j_full[5:8, 5:8] = x_e
    j_m = np.zeros_like(dm)
    j_m[:3, :3] = x_e

    full_resp = source_response(d, j_full)
    sector_resp = source_response(dm, j_m)
    le_resp = source_response(l_e, x_e)

    check(
        "The full microscopic operator preserves charge exactly",
        np.linalg.norm(d @ q - q @ d) < 1e-12,
        f"commutator={np.linalg.norm(d @ q - q @ d):.2e}",
    )
    check(
        "A charged-lepton-supported microscopic source pushes forward exactly through the charge -1 sector",
        abs(full_resp - sector_resp) < 1e-12,
        f"|Δ|={abs(full_resp - sector_resp):.2e}",
    )
    check(
        "The charged projected source law then factors exactly through L_e = Schur_{E_e}(D_-)",
        abs(sector_resp - le_resp) < 1e-12,
        f"|Δ|={abs(sector_resp - le_resp):.2e}",
    )
    check(
        "The canonical charged-lepton Hermitian block is therefore an exact charged-sector Schur target",
        np.linalg.norm(l_e - h_e_target) < 1e-12,
        f"err={np.linalg.norm(l_e - h_e_target):.2e}",
    )

    print()
    print("  So dW_e^H is not an ad hoc PMNS object.")
    print("  It is the exact charged-sector Schur pushforward of the microscopic")
    print("  charge -1 source-response law.")

    return l_e


def part2_dweh_reconstructs_he_and_the_ne_packet(l_e: np.ndarray) -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 2: dW_e^H RECONSTRUCTS H_e AND THE N_e PACKET")
    print("=" * 88)
    print("  Algebraic identity (retained-grade). Assumes dW_e^H is supplied;")
    print("  this part does not derive it from the sole axiom.")
    print()

    responses = [float(np.real(np.trace(x @ l_e))) for x in hermitian_basis()]
    h_e = reconstruct_h_from_responses(responses)
    packet = packet_from_h_e(h_e)

    check(
        "Nine charged Hermitian responses reconstruct H_e exactly",
        np.linalg.norm(h_e - l_e) < 1e-12,
        f"err={np.linalg.norm(h_e - l_e):.2e}",
    )
    check(
        "On N_e, H_e alone determines the PMNS transport packet",
        np.linalg.norm(np.sum(packet, axis=0) - np.ones(3)) < 1e-12,
        f"col sums={np.round(np.sum(packet, axis=0), 6)}",
    )

    print()
    print("  recovered N_e packet from dW_e^H:")
    print(np.round(packet, 6))

    return packet


def part3_consistency_check_at_stipulated_canonical_sample(packet: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 3: CONSISTENCY CHECK AT STIPULATED CANONICAL N_e SAMPLE")
    print("=" * 88)
    print("  NOT a derivation. The canonical (x, y, delta) input used in Part 1")
    print("  is the same off-seed benchmark as the LAST_MILE sibling note. This")
    print("  part checks the two routines agree on the same stipulated input.")
    print()

    _factors, eta_vals = transport_column_values(packet)
    best_idx = int(np.argmax(eta_vals))
    pmns_eta_ratio = float(eta_vals[best_idx])
    one_flavor_miss = 1.0 / ETA_ONE_FLAVOR_AUTHORITY
    pmns_miss = 1.0 / pmns_eta_ratio
    improvement = pmns_eta_ratio / ETA_ONE_FLAVOR_AUTHORITY

    check(
        "Selected column on this stipulated sample is the middle column "
        "(matches the sibling LAST_MILE benchmark; column choice is not "
        "sole-axiom-fixed, see the ACTIVE_COLUMN_AXIOM_BOUNDARY note)",
        best_idx == 1,
        f"eta_vals={np.round(eta_vals, 12)}",
    )
    # Two-routine consistency tolerance. The LAST_MILE sibling and this runner
    # use slightly different transport-driver code paths, so the value differs
    # at the ~1e-7 level. The tolerance below records the actually observed
    # cross-runner agreement on the same stipulated input; it is NOT a claim
    # that the value is derived to that precision from the sole axiom.
    cross_runner_tol = 5e-7
    check(
        "Computed eta/eta_obs on this stipulated sample agrees with the sibling "
        "LAST_MILE benchmark ETA_NE_CANONICAL to numerical tolerance "
        "(two-runner consistency check on the same stipulated input, NOT a "
        "derivation of either number)",
        abs(pmns_eta_ratio - ETA_NE_CANONICAL_SIBLING) < cross_runner_tol,
        f"this={pmns_eta_ratio:.12f}, sibling={ETA_NE_CANONICAL_SIBLING:.12f}, "
        f"|delta|={abs(pmns_eta_ratio - ETA_NE_CANONICAL_SIBLING):.2e}",
    )

    print()
    print("  Numbers at this stipulated sample (informational):")
    print(f"    one-flavor authority eta ratio    = {ETA_ONE_FLAVOR_AUTHORITY:.12f}")
    print(f"    one-flavor authority miss factor  = {one_flavor_miss:.12f}")
    print(f"    PMNS-conditioned eta ratio        = {pmns_eta_ratio:.12f}")
    print(f"    PMNS-conditioned miss factor      = {pmns_miss:.12f}")
    print(f"    sample improvement factor         = {improvement:.12f}")
    print("  None of these are derived from Cl(3) on Z^3.")


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    print("  Structural content (load-bearing, retained-grade):")
    print("    - Part 1: dW_e^H is the exact charged-sector Schur pushforward")
    print("      of the microscopic charge -1 source-response law.")
    print("    - Part 2: dW_e^H reconstructs H_e exactly and H_e determines")
    print("      the N_e transport packet.")
    print()
    print("  Conditional / informational content (NOT load-bearing):")
    print("    - Part 3: at a stipulated canonical (x, y, delta) benchmark,")
    print("      the chain reproduces the sibling LAST_MILE value")
    print(f"      eta/eta_obs ~= {ETA_NE_CANONICAL_SIBLING:.12f}.")
    print("      This is consistency between two runners on the same stipulated")
    print("      input, not a sole-axiom derivation. The selected N_e column")
    print("      is not sole-axiom-fixed; see the ACTIVE_COLUMN_AXIOM_BOUNDARY")
    print("      note.")
    print()
    print("  Frontier object (unchanged):")
    print("    - evaluate dW_e^H (equivalently D_-) from Cl(3) on Z^3.")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS N_e CHARGED SOURCE-RESPONSE REDUCTION")
    print("=" * 88)

    l_e = part1_the_charged_hermitian_source_law_is_exact_schur_pushforward()
    packet = part2_dweh_reconstructs_he_and_the_ne_packet(l_e)
    part3_consistency_check_at_stipulated_canonical_sample(packet)
    part4_bottom_line()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
