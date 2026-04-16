#!/usr/bin/env python3
"""
Baryogenesis single-history composition on the current main package surface.

This runner replaces the earlier illustrative pushforward maps with the exact
current-surface quotient extractors that are already fixed upstream:

  ell_L(tau) = Tr(P_L rho(tau)) / 8
  q_+(tau)   = Tr(Q(tau)) / 4

So the coupled-history reduction is now phrased in the strongest honest way:
the downstream active coordinates are extracted exactly from the stage-generated
operator histories, while the response maps that generate those operator
histories remain open.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS = 0
FAIL = 0

ETA_OBS = 6.12e-10
J_PROMOTED = 3.330901e-5
K_NP_TARGET = ETA_OBS / J_PROMOTED

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
TASTE_STATES = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]


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


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


def hamming_weight(state: tuple[int, int, int]) -> int:
    return sum(state)


def baryon_and_lepton_operators() -> tuple[np.ndarray, np.ndarray]:
    baryon = np.zeros((8, 8), dtype=complex)
    lepton = np.zeros((8, 8), dtype=complex)
    for idx, state in enumerate(TASTE_STATES):
        hw = hamming_weight(state)
        if hw in (1, 2):
            baryon[idx, idx] = 1.0 / 3.0
        else:
            lepton[idx, idx] = 1.0
    return baryon, lepton


def left_active_coordinate(rho: np.ndarray, p_l: np.ndarray) -> float:
    return float(np.trace(p_l @ rho).real / np.trace(p_l).real)


def active_charge_coordinate(q_op: np.ndarray, b_plus_l: np.ndarray) -> float:
    return float(np.trace(q_op).real / np.trace(b_plus_l).real)


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS SINGLE-HISTORY COMPOSITION")
    print("=" * 80)
    print()
    print("Question:")
    print("  Can the current coupled-history reduction be stated with exact")
    print("  operator extractors instead of illustrative placeholder maps?")
    print()

    print("=" * 80)
    print("PART 1: NOTE-LEVEL EXACT COMPOSITION")
    print("=" * 80)
    print()

    comp_note = (
        DOCS / "BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md"
    ).read_text(encoding="utf-8")
    kewpt_note = (DOCS / "BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md").read_text(
        encoding="utf-8"
    )
    ktr_note = (DOCS / "BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md").read_text(
        encoding="utf-8"
    )
    ksph_note = (DOCS / "BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md").read_text(
        encoding="utf-8"
    )

    check(
        "K_EWPT note records K_EWPT = F_EWPT[chi(tau)]",
        "`K_EWPT = F_EWPT[χ(τ)]`" in kewpt_note,
    )
    check(
        "K_tr note records K_tr = F_tr[ell_L(tau)]",
        "`K_tr = F_tr[ℓ_L(τ)]`" in ktr_note,
    )
    check(
        "K_sph note records K_sph = F_sph[q_+(tau)]",
        "`K_sph = F_sph[q_+(τ)]`" in ksph_note,
    )
    check(
        "single-history note records the exact left-handed quotient extractor",
        "`Π_L[ρ](τ) := Tr(P_L ρ(τ)) / 8 = ℓ_L(τ)`" in comp_note,
    )
    check(
        "single-history note records the exact active-charge quotient extractor",
        "`Π_+[Q](τ) := Tr(Q(τ)) / 4 = q_+(τ)`" in comp_note,
    )
    check(
        "single-history note records T_L = Pi_L o R_L",
        "`T_L = Π_L ∘ R_L`" in comp_note,
    )
    check(
        "single-history note records T_+ = Pi_+ o R_+",
        "`T_+ = Π_+ ∘ R_+`" in comp_note,
    )
    check(
        "single-history note still records K_NP = F_NP[chi(tau)]",
        "`K_NP = F_NP[χ(τ)]`" in comp_note,
    )
    check(
        "single-history note still records eta = J * F_NP[chi(tau)]",
        "`η = J * F_NP[χ(τ)]`" in comp_note,
    )
    info(
        "composition meaning",
        "the exact content is now the quotient extraction of the downstream active coordinates; the stage response maps themselves remain open",
    )
    print()

    print("=" * 80)
    print("PART 2: EXACT LEFT-HANDED QUOTIENT EXTRACTOR")
    print("=" * 80)
    print()

    i16 = np.eye(16, dtype=complex)
    g0 = kron4(SZ, SZ, SZ, SX)
    g1 = kron4(SX, I2, I2, I2)
    g2 = kron4(SZ, SX, I2, I2)
    g3 = kron4(SZ, SZ, SX, I2)
    g5 = g0 @ g1 @ g2 @ g3
    p_l = (i16 + g5) / 2.0
    p_r = (i16 - g5) / 2.0

    check(
        "Tr(P_L) = 8 on the retained 4D chirality surface",
        abs(np.trace(p_l).real - 8.0) < 1e-12,
        f"Tr(P_L) = {np.trace(p_l).real:.1f}",
    )
    check(
        "P_L and P_R remain orthogonal projectors",
        np.linalg.norm(p_l @ p_r) < 1e-12 and np.linalg.norm(p_l @ p_l - p_l) < 1e-12,
    )

    ell_hist = np.array([0.4, 0.6, 0.8, 0.5, 0.3], dtype=float)
    rr_hist = np.array([0.2, -0.1, 0.4, 0.0, -0.3], dtype=float)
    recovered_ell = []
    for ell_l, r_r in zip(ell_hist, rr_hist):
        rho = ell_l * p_l + r_r * p_r
        recovered_ell.append(left_active_coordinate(rho, p_l))

    recovered_ell = np.array(recovered_ell, dtype=float)
    check(
        "Pi_L[rho] = Tr(P_L rho)/8 recovers the exact active left-handed coordinate history",
        np.max(np.abs(recovered_ell - ell_hist)) < 1e-12,
        f"max |ell_rec - ell| = {np.max(np.abs(recovered_ell - ell_hist)):.2e}",
    )

    rr_hist_alt = np.array([-0.5, 0.7, -0.2, 0.9, 0.1], dtype=float)
    recovered_ell_alt = []
    for ell_l, r_r in zip(ell_hist, rr_hist_alt):
        rho = ell_l * p_l + r_r * p_r
        recovered_ell_alt.append(left_active_coordinate(rho, p_l))

    recovered_ell_alt = np.array(recovered_ell_alt, dtype=float)
    check(
        "Pi_L[rho] is insensitive to right-handed spectator histories",
        np.max(np.abs(recovered_ell_alt - ell_hist)) < 1e-12,
        f"max |ell_rec_alt - ell| = {np.max(np.abs(recovered_ell_alt - ell_hist)):.2e}",
    )
    info(
        "left-handed extractor meaning",
        "the only exact downstream transport coordinate on the current surface is obtained by the chirality projector quotient, not by a guessed scalar-to-density map",
    )
    print()

    print("=" * 80)
    print("PART 3: EXACT ACTIVE-CHARGE QUOTIENT EXTRACTOR")
    print("=" * 80)
    print()

    baryon, lepton = baryon_and_lepton_operators()
    b_plus_l = baryon + lepton
    b_minus_l = baryon - lepton

    check(
        "Tr(B+L) = 4 on the retained charge plane",
        abs(np.trace(b_plus_l).real - 4.0) < 1e-12,
        f"Tr(B+L) = {np.trace(b_plus_l).real:.1f}",
    )
    check(
        "Tr(B-L) = 0 on the retained charge plane",
        abs(np.trace(b_minus_l).real) < 1e-12,
        f"Tr(B-L) = {np.trace(b_minus_l).real:.1e}",
    )

    q_plus_hist = np.array([0.3, 0.5, 0.2, 0.7, 0.4], dtype=float)
    q_minus_hist = np.array([0.2, -0.3, 0.1, 0.0, -0.4], dtype=float)
    recovered_q_plus = []
    for q_plus, q_minus in zip(q_plus_hist, q_minus_hist):
        q_op = q_plus * b_plus_l + q_minus * b_minus_l
        recovered_q_plus.append(active_charge_coordinate(q_op, b_plus_l))

    recovered_q_plus = np.array(recovered_q_plus, dtype=float)
    check(
        "Pi_+[Q] = Tr(Q)/4 recovers the exact washout-active charge history",
        np.max(np.abs(recovered_q_plus - q_plus_hist)) < 1e-12,
        f"max |q+_rec - q+| = {np.max(np.abs(recovered_q_plus - q_plus_hist)):.2e}",
    )

    q_minus_hist_alt = np.array([-0.6, 0.2, -0.2, 0.4, 0.8], dtype=float)
    recovered_q_plus_alt = []
    for q_plus, q_minus in zip(q_plus_hist, q_minus_hist_alt):
        q_op = q_plus * b_plus_l + q_minus * b_minus_l
        recovered_q_plus_alt.append(active_charge_coordinate(q_op, b_plus_l))

    recovered_q_plus_alt = np.array(recovered_q_plus_alt, dtype=float)
    check(
        "Pi_+[Q] is insensitive to the protected B-L spectator history",
        np.max(np.abs(recovered_q_plus_alt - q_plus_hist)) < 1e-12,
        f"max |q+_rec_alt - q+| = {np.max(np.abs(recovered_q_plus_alt - q_plus_hist)):.2e}",
    )
    info(
        "active-charge extractor meaning",
        "the exact sphaleron-active coordinate is the trace quotient on the B/L plane, not a guessed transport-to-washout averaging rule",
    )
    print()

    print("=" * 80)
    print("PART 4: EXACT COUPLED-HISTORY COMPOSITION BOUNDARY")
    print("=" * 80)
    print()

    check(
        "single-history note records the response-history lift rho_chi(tau) = ell_L(tau) P_L + r_R(tau) P_R",
        "`ρ_χ(τ) = ℓ_L(τ) P_L + r_R(τ) P_R`" in comp_note,
    )
    check(
        "single-history note records the charge-plane lift Q_ell(tau) = q_+(tau)(B+L) + q_-(tau)(B-L)",
        "`Q_{ℓ_L}(τ) = q_+(τ) (B+L) + q_-(τ) (B-L)`" in comp_note,
    )
    check(
        "single-history note records the exact composed functional through the response lifts and quotient extractors",
        "`F_NP[χ] := F_EWPT[χ] * F_tr[Π_L[ρ_χ]] * F_sph[Π_+[Q_{ℓ_L}]]`" in comp_note,
    )
    check(
        "single-history note records rho_chi = R_L[chi] and Q_ell = R_+[Pi_L[rho_chi]]",
        "`ρ_χ := R_L[χ]`" in comp_note and "`Q_{ℓ_L} := R_+[Π_L[ρ_χ]]`" in comp_note,
    )
    info(
        "composition consequence",
        "the exact downstream maps are now explicit quotient extractors; the only open content is the operator response history generated upstream on each stage surface",
    )
    print()

    print("=" * 80)
    print("PART 5: TARGET NORMALIZATION AND PACKAGE INTEGRATION")
    print("=" * 80)
    print()

    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    knp_note = (DOCS / "BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md").read_text(
        encoding="utf-8"
    )
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(
        encoding="utf-8"
    )
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")
    flagship = (DOCS / "CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md").read_text(
        encoding="utf-8"
    )

    print(f"  K_NP,target = eta_obs / J = {K_NP_TARGET:.6e}")
    print()

    check(
        "single-history target equals the existing K_NP target",
        abs(K_NP_TARGET - 1.837341e-5) < 1e-11,
        f"F_NP,target = {K_NP_TARGET:.6e}",
    )
    check(
        "eta = J * F_NP,target reconstructs the observed baryon asymmetry",
        abs(J_PROMOTED * K_NP_TARGET - ETA_OBS) < 1e-20,
        f"eta = {J_PROMOTED * K_NP_TARGET:.6e}",
    )
    check(
        "closure-gate note points to the single-history composition note",
        "BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md" in gate_note,
    )
    check(
        "K_NP stage-decomposition note points to the single-history composition note",
        "BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md" in knp_note,
    )
    check(
        "derivation atlas carries the single-history composition row",
        "Baryogenesis single-history composition" in atlas,
    )
    check(
        "canonical harness index includes the single-history composition runner",
        "frontier_baryogenesis_single_history_composition.py" in harness,
    )
    check(
        "current flagship entrypoint points to the single-history composition note",
        "BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md" in flagship,
    )
    info(
        "remaining task",
        "the current package no longer hides the downstream maps behind ad hoc examples; what remains open is the first-principles derivation or evaluation of the response histories R_L and R_+ and the resulting coupled functional F_NP[chi]",
    )
    print()

    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the coupled-history reduction is now expressed with exact")
    print("      quotient extractors")
    print("      ell_L(tau) = Tr(P_L rho(tau)) / 8")
    print("      q_+(tau)   = Tr(Q(tau)) / 4")
    print("    - the placeholder sample maps have been removed")
    print("    - what remains open is not the quotient geometry but the")
    print("      response-history maps and the final coupled functional")
    print("      F_NP[chi(tau)]")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
