#!/usr/bin/env python3
"""
Exact branch-conditioned closure theorem:
once the PMNS selector sign picks a minimal two-Higgs branch, the canonical
coefficients reconstruct explicitly from branch Hermitian data up to one Z2
sheet.

Boundary:
  This is still branch-conditioned. It does not derive the selector amplitude,
  its sign, or the branch Hermitian data themselves.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
PERM_1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE


def canonical_h(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    ymat = canonical_y(x, y, delta)
    return ymat @ ymat.conj().T


def invariant_coordinates(h: np.ndarray) -> np.ndarray:
    return np.array(
        [
            float(np.real(h[0, 0])),
            float(np.real(h[1, 1])),
            float(np.real(h[2, 2])),
            float(np.abs(h[0, 1])),
            float(np.abs(h[1, 2])),
            float(np.abs(h[2, 0])),
            float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
        ],
        dtype=float,
    )


def reconstruct_h(obs: np.ndarray) -> np.ndarray:
    d1, d2, d3, r12, r23, r31, phi = obs
    return np.array(
        [
            [d1, r12, r31 * np.exp(-1j * phi)],
            [r12, d2, r23],
            [r31 * np.exp(1j * phi), r23, d3],
        ],
        dtype=complex,
    )


def quadratic_coefficients(obs: np.ndarray) -> tuple[float, float, float]:
    d1, d2, d3, r12, r23, r31, _ = obs
    alpha = r12 * r12
    beta = r23 * r23
    gamma = r31 * r31
    a = d2 * d3 - beta
    b = d1 * d2 * d3 + gamma * d2 - alpha * d3 - beta * d1
    c = gamma * (d1 * d2 - alpha)
    return float(a), float(b), float(c)


def quadratic_roots(obs: np.ndarray) -> tuple[float, np.ndarray]:
    a, b, c = quadratic_coefficients(obs)
    disc = float(b * b - 4.0 * a * c)
    roots = np.array(
        [
            (b - np.sqrt(max(disc, 0.0))) / (2.0 * a),
            (b + np.sqrt(max(disc, 0.0))) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()
    return disc, roots


def reconstruct_squares_from_root(obs: np.ndarray, t1: float) -> tuple[np.ndarray, np.ndarray, float]:
    d1, d2, d3, r12, r23, _r31, phi = obs
    alpha = r12 * r12
    beta = r23 * r23
    t2 = alpha / (d1 - t1)
    t3 = beta / (d2 - t2)
    xsq = np.array([t1, t2, t3], dtype=float)
    ysq = np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float)
    return xsq, ysq, float(phi)


def check_two_higgs_branch(sample_name: str, x: np.ndarray, y: np.ndarray, delta: float) -> None:
    h = canonical_h(x, y, delta)
    obs = invariant_coordinates(h)
    a, b, c = quadratic_coefficients(obs)
    disc, roots = quadratic_roots(obs)
    true_t1 = float(x[0] ** 2)
    poly_val = float(a * true_t1 * true_t1 - b * true_t1 + c)
    root_idx = int(np.argmin(np.abs(roots - true_t1)))
    dual_idx = 1 - root_idx

    xsq_true, ysq_true, phi_true = reconstruct_squares_from_root(obs, float(roots[root_idx]))
    xsq_dual, ysq_dual, phi_dual = reconstruct_squares_from_root(obs, float(roots[dual_idx]))
    h_true = canonical_h(np.sqrt(xsq_true), np.sqrt(ysq_true), phi_true)
    h_dual = canonical_h(np.sqrt(xsq_dual), np.sqrt(ysq_dual), phi_dual)

    d1 = float(obs[0])
    positive_roots = all(0.0 < root < d1 for root in roots)
    positive_true = bool(np.all(xsq_true > 0.0) and np.all(ysq_true > 0.0))
    positive_dual = bool(np.all(xsq_dual > 0.0) and np.all(ysq_dual > 0.0))
    distinct_sheets = float(np.linalg.norm(xsq_true - xsq_dual) + np.linalg.norm(ysq_true - ysq_dual))

    check(f"{sample_name}: the true first squared modulus satisfies the exact quadratic", abs(poly_val) < 1e-10,
          f"Q(x1^2)={poly_val:.2e}")
    check(f"{sample_name}: the quadratic discriminant is positive on the generic physical patch", disc > 1e-10,
          f"disc={disc:.6f}")
    check(f"{sample_name}: the quadratic gives two positive roots on the physical interval", positive_roots,
          f"roots={np.round(roots, 6)}")
    check(f"{sample_name}: one root reconstructs the original canonical sheet", np.linalg.norm(h - h_true) < 1e-10,
          f"H error={np.linalg.norm(h - h_true):.2e}")
    check(f"{sample_name}: the second root reconstructs a distinct dual sheet with the same Hermitian data",
          np.linalg.norm(h - h_dual) < 1e-10 and distinct_sheets > 1e-6,
          f"H dual error={np.linalg.norm(h - h_dual):.2e}, sheet distance={distinct_sheets:.3e}")
    check(f"{sample_name}: both reconstructed sheets stay on the positive canonical patch", positive_true and positive_dual,
          f"min true={min(np.min(xsq_true), np.min(ysq_true)):.3e}, min dual={min(np.min(xsq_dual), np.min(ysq_dual)):.3e}")
    check(f"{sample_name}: the triangle phase is preserved on both sheets", abs(phi_true - delta) < 1e-12 and abs(phi_dual - delta) < 1e-12,
          f"phi_true={phi_true:.6f}, phi_dual={phi_dual:.6f}, delta={delta:.6f}")


def part1_neutrino_side_branch_has_explicit_quadratic_sheet_reconstruction() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE NEUTRINO-SIDE TWO-HIGGS BRANCH HAS AN EXPLICIT QUADRATIC SHEET RECONSTRUCTION")
    print("=" * 88)

    check_two_higgs_branch(
        "neutrino-side sample",
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )

    rng = np.random.default_rng(17)
    all_good = True
    for _ in range(5):
        x = rng.uniform(0.3, 1.6, size=3)
        y = rng.uniform(0.2, 1.4, size=3)
        delta = float(rng.uniform(0.2, 2.4))
        h = canonical_h(x, y, delta)
        obs = invariant_coordinates(h)
        disc, roots = quadratic_roots(obs)
        if not (disc > 1e-12 and np.all(roots > 0.0) and np.all(roots < obs[0])):
            all_good = False
            break
        for root in roots:
            xsq, ysq, phi = reconstruct_squares_from_root(obs, float(root))
            h_rec = canonical_h(np.sqrt(xsq), np.sqrt(ysq), phi)
            if not (np.all(xsq > 0.0) and np.all(ysq > 0.0) and np.linalg.norm(h - h_rec) < 1e-10):
                all_good = False
                break
        if not all_good:
            break

    check("neutrino-side generic samples all respect the same two-sheet reconstruction pattern", all_good)

    print()
    print("  So on the selected neutrino-side branch, the coefficient problem is")
    print("  already algebraic: one quadratic root, rational back-substitution,")
    print("  and one residual sheet bit.")


def part2_charged_lepton_side_branch_has_the_same_quadratic_sheet_structure() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CHARGED-LEPTON-SIDE TWO-HIGGS BRANCH HAS THE SAME QUADRATIC SHEET STRUCTURE")
    print("=" * 88)

    check_two_higgs_branch(
        "charged-lepton-side sample",
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )

    print()
    print("  So the charged-lepton-side canonical branch is not merely locally")
    print("  identifiable. Its coefficients also reconstruct by the same exact")
    print("  quadratic-sheet logic.")


def part3_charged_lepton_branch_keeps_the_neutrino_monomial_masses_direct() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ON THE CHARGED-LEPTON-SIDE BRANCH, THE NEUTRINO MONOMIAL MASSES STAY DIRECT")
    print("=" * 88)

    d = np.array([0.021, 0.034, 0.055], dtype=float)
    y_nu = np.diag(d.astype(complex)) @ PERM_1
    h_nu = y_nu @ y_nu.conj().T
    singular_values = np.sort(np.linalg.svd(y_nu, compute_uv=False))
    direct = np.sort(np.sqrt(np.real(np.diag(h_nu))))

    check("A monomial neutrino Dirac lane gives a diagonal Hermitian matrix", np.linalg.norm(h_nu - np.diag(np.diag(h_nu))) < 1e-12,
          f"offdiag norm={np.linalg.norm(h_nu - np.diag(np.diag(h_nu))):.2e}")
    check("Its three positive Dirac masses are exactly the monomial singular values", np.allclose(singular_values, d, atol=1e-12),
          f"svd={np.round(singular_values, 6)}")
    check("Those same masses are read directly from the diagonal Hermitian data", np.allclose(direct, d, atol=1e-12),
          f"diag masses={np.round(direct, 6)}")

    print()
    print("  So if the selector chooses the charged-lepton-side PMNS branch, the")
    print("  extra neutrino-side data are not another texture problem. They are")
    print("  the direct monomial Dirac mass moduli.")


def part4_current_bank_records_the_post_selector_endpoint() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT BANK NOW RECORDS THE POST-SELECTOR ENDPOINT")
    print("=" * 88)

    note = read("docs/PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    last_mile = read("docs/NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md")
    packet = read("docs/publication/ci3_z3/NEUTRINO_DIRAC_PMNS_BOUNDARY_PACKET_2026-04-15.md")

    check("The new note states explicit quadratic reconstruction on the selected branch",
          "explicit quadratic" in note.lower() and "rationally" in note.lower() and "Z_2" in note)
    check("The atlas carries the branch-conditioned quadratic-sheet closure row",
          "| PMNS branch-conditioned quadratic-sheet closure |" in atlas)
    check("The two-amplitude last-mile note keeps sole-axiom closure separate",
          "Only two amplitudes remain" in last_mile and "`(J_chi, mu)`" in last_mile)
    check("The reviewer packet records the residual selected-branch sheet boundary",
          "residual selected-branch `Z_2` sheet" in packet)

    print()
    print("  So the coefficient side is now closed as far as the current bank")
    print("  honestly allows: after selector realization, only an explicit sheet")
    print("  bit remains on the selected two-Higgs branch.")


def main() -> int:
    print("=" * 88)
    print("PMNS BRANCH-CONDITIONED QUADRATIC-SHEET CLOSURE")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS selector sign-to-branch reduction")
    print("  - neutrino two-Higgs canonical reduction")
    print("  - charged-lepton two-Higgs canonical reduction")
    print("  - neutrino two-amplitude last-mile boundary")
    print()
    print("Question:")
    print("  Once a future selector sign chooses the active minimal PMNS branch,")
    print("  is the remaining coefficient problem still an open-ended seven-")
    print("  parameter search, or is it already algebraically explicit?")

    part1_neutrino_side_branch_has_explicit_quadratic_sheet_reconstruction()
    part2_charged_lepton_side_branch_has_the_same_quadratic_sheet_structure()
    part3_charged_lepton_branch_keeps_the_neutrino_monomial_masses_direct()
    part4_current_bank_records_the_post_selector_endpoint()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - once sign(a_sel) chooses the active minimal PMNS branch, the")
    print("      selected two-Higgs coefficients reconstruct from Hermitian data")
    print("      by one explicit quadratic equation plus rational back-substitution")
    print("    - on the selected two-Higgs branch the residual global ambiguity is")
    print("      generically one Z_2 sheet, not a continuous family")
    print("    - on the charged-lepton-side branch the extra neutrino-side data")
    print("      remain the direct monomial Dirac mass moduli")
    print()
    print("  So the post-selector coefficient problem is algebraically explicit")
    print("  up to one residual sheet bit on the selected two-Higgs branch.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
