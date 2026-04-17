#!/usr/bin/env python3
"""
Exact generic conditional theorem:
the full-rank PMNS right orbit already has a canonical positive polar section
Y_+(H) = H^(1/2); that section realizes the reduced branch selector from
Hermitian data, but remains sheet-even and cannot fix the residual Z2 sheet.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
PERM_1 = CYCLE.copy()


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


def monomial_y(diag: np.ndarray) -> np.ndarray:
    return np.diag(diag.astype(complex)) @ PERM_1


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


def reconstruct_from_observables(obs: np.ndarray) -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:
    d1, d2, d3, r12, r23, r31, phi = obs
    alpha = r12 * r12
    beta = r23 * r23
    gamma = r31 * r31
    a = d2 * d3 - beta
    b = d1 * d2 * d3 + gamma * d2 - alpha * d3 - beta * d1
    c = gamma * (d1 * d2 - alpha)
    disc = float(b * b - 4.0 * a * c)
    roots = np.array(
        [
            (b - np.sqrt(max(disc, 0.0))) / (2.0 * a),
            (b + np.sqrt(max(disc, 0.0))) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()

    def sheet(root: float) -> tuple[np.ndarray, np.ndarray]:
        t1 = root
        t2 = alpha / (d1 - t1)
        t3 = beta / (d2 - t2)
        x = np.sqrt(np.array([t1, t2, t3], dtype=float))
        y = np.sqrt(np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float))
        return x, y

    return sheet(float(roots[0])), sheet(float(roots[1]))


def sqrt_psd(h: np.ndarray) -> np.ndarray:
    evals, vecs = np.linalg.eigh(h)
    evals = np.clip(evals, 0.0, None)
    return vecs @ np.diag(np.sqrt(evals)) @ vecs.conj().T


def rotation12(theta: float) -> np.ndarray:
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]], dtype=complex)


def upper_offdiag_score(m: np.ndarray) -> int:
    vals = np.array([m[0, 1], m[1, 2], m[0, 2]])
    return int(np.count_nonzero(np.abs(vals) > 1e-10))


def part1_generic_right_orbit_has_unique_positive_polar_representative() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE GENERIC RIGHT ORBIT HAS A UNIQUE POSITIVE POLAR REPRESENTATIVE")
    print("=" * 88)

    y = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    u_r = rotation12(0.47) @ np.diag(np.array([1.0, np.exp(0.23j), np.exp(-0.41j)], dtype=complex))
    y_rot = y @ u_r.conj().T
    h = y @ y.conj().T
    h_rot = y_rot @ y_rot.conj().T
    p = sqrt_psd(h)
    p_rot = sqrt_psd(h_rot)
    u = np.linalg.solve(p, y)

    check("The right orbit preserves H", np.linalg.norm(h - h_rot) < 1e-12,
          f"H difference={np.linalg.norm(h - h_rot):.2e}")
    check("The polar representative is Hermitian", np.linalg.norm(p - p.conj().T) < 1e-12,
          f"Hermitian error={np.linalg.norm(p - p.conj().T):.2e}")
    check("The polar representative squares to H", np.linalg.norm(p @ p - h) < 1e-10,
          f"P^2-H error={np.linalg.norm(p @ p - h):.2e}")
    check("The same right orbit yields the same positive polar representative", np.linalg.norm(p - p_rot) < 1e-10,
          f"polar difference={np.linalg.norm(p - p_rot):.2e}")
    check("The original Yukawa factorizes as Y = H^(1/2) U_R with U_R unitary",
          np.linalg.norm(y - p @ u) < 1e-10 and np.linalg.norm(u.conj().T @ u - np.eye(3)) < 1e-10,
          f"factorization error={np.linalg.norm(y - p @ u):.2e}, unitarity error={np.linalg.norm(u.conj().T @ u - np.eye(3)):.2e}")

    print()
    print("  So the generic full-rank right orbit is not sectionless. It already")
    print("  has the canonical positive representative Y_+(H) = H^(1/2).")


def part2_positive_section_realizes_the_reduced_selector_from_hermitian_data() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE POSITIVE SECTION REALIZES THE REDUCED SELECTOR FROM H")
    print("=" * 88)

    # Universal one-offset class: both monomial
    h_u1_nu = monomial_y(np.array([0.21, 0.34, 0.55], dtype=float)) @ monomial_y(np.array([0.21, 0.34, 0.55], dtype=float)).conj().T
    h_u1_e = monomial_y(np.array([0.02, 0.11, 0.90], dtype=float)) @ monomial_y(np.array([0.02, 0.11, 0.90], dtype=float)).conj().T

    # Universal two-offset class: both canonical / non-monomial
    h_u2_nu = canonical_h(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    h_u2_e = canonical_h(np.array([0.24, 0.38, 1.07], dtype=float), np.array([0.09, 0.22, 0.61], dtype=float), 1.10)

    # One-sided classes
    h_nu_side_nu = h_u2_nu
    h_nu_side_e = h_u1_e
    h_e_side_nu = h_u1_nu
    h_e_side_e = h_u2_e

    def a_pol(h_nu: np.ndarray, h_e: np.ndarray) -> int:
        return upper_offdiag_score(sqrt_psd(h_nu)) - upper_offdiag_score(sqrt_psd(h_e))

    # Genericity check on canonical patch
    rng = np.random.default_rng(7)
    generic_dense = True
    for _ in range(5):
        x = rng.uniform(0.4, 1.6, size=3)
        y = rng.uniform(0.3, 1.4, size=3)
        delta = float(rng.uniform(0.2, 2.6))
        p = sqrt_psd(canonical_h(x, y, delta))
        if upper_offdiag_score(p) != 3:
            generic_dense = False
            break

    check("On a monomial branch the positive polar section stays diagonal", upper_offdiag_score(sqrt_psd(h_u1_nu)) == 0 and upper_offdiag_score(sqrt_psd(h_u1_e)) == 0)
    check("On generic canonical two-Higgs branches the positive polar section has full upper off-diagonal support", generic_dense)
    check("The intrinsic polar-section selector vanishes on the universal one-offset class", a_pol(h_u1_nu, h_u1_e) == 0,
          f"a_pol(U1)={a_pol(h_u1_nu, h_u1_e)}")
    check("The intrinsic polar-section selector vanishes on the universal two-offset class", a_pol(h_u2_nu, h_u2_e) == 0,
          f"a_pol(U2)={a_pol(h_u2_nu, h_u2_e)}")
    check("The intrinsic polar-section selector is positive on the neutrino-side one-sided class", a_pol(h_nu_side_nu, h_nu_side_e) > 0,
          f"a_pol(N_nu)={a_pol(h_nu_side_nu, h_nu_side_e)}")
    check("The intrinsic polar-section selector is negative on the charged-lepton-side one-sided class", a_pol(h_e_side_nu, h_e_side_e) < 0,
          f"a_pol(N_e)={a_pol(h_e_side_nu, h_e_side_e)}")

    print()
    print("  So once H_nu and H_e are available, the one-sided branch is already")
    print("  intrinsically readable from the positive polar section.")


def part3_positive_section_is_sheet_even_and_cannot_fix_the_residual_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE POSITIVE SECTION IS SHEET-EVEN AND CANNOT FIX THE RESIDUAL SHEET")
    print("=" * 88)

    h = canonical_h(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    obs = invariant_coordinates(h)
    (x0, y0), (x1, y1) = reconstruct_from_observables(obs)
    h0 = canonical_h(x0, y0, 1.10)
    h1 = canonical_h(x1, y1, 1.10)
    p0 = sqrt_psd(h0)
    p1 = sqrt_psd(h1)
    sheet_distance = float(np.linalg.norm(x0 - x1) + np.linalg.norm(y0 - y1))

    check("The two reconstructed coefficient sheets are distinct", sheet_distance > 1e-6,
          f"sheet distance={sheet_distance:.6f}")
    check("They share the same Hermitian matrix H", np.linalg.norm(h0 - h1) < 1e-10,
          f"H difference={np.linalg.norm(h0 - h1):.2e}")
    check("The positive polar section is identical on both sheets", np.linalg.norm(p0 - p1) < 1e-10,
          f"polar difference={np.linalg.norm(p0 - p1):.2e}")
    check("So every positive-section scalar depending only on H is sheet-even", abs(np.abs((p0.conj().T @ p0)[0, 1]) - np.abs((p1.conj().T @ p1)[0, 1])) < 1e-12,
          f"values=({abs((p0.conj().T @ p0)[0,1]):.6f}, {abs((p1.conj().T @ p1)[0,1]):.6f})")

    print()
    print("  So the polar section removes the generic right-orbit ambiguity, but")
    print("  it does not close the residual canonical-sheet bit.")


def part4_the_bank_records_the_new_polar_section_endpoint() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE BANK RECORDS THE NEW POLAR-SECTION ENDPOINT")
    print("=" * 88)

    note = read("docs/PMNS_RIGHT_POLAR_SECTION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    packet = read("docs/publication/ci3_z3/NEUTRINO_DIRAC_PMNS_BOUNDARY_PACKET_2026-04-15.md")
    intrinsic = read("docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md")

    check("The new note identifies Y_+(H) = H^(1/2) as the canonical positive section",
          "Y_+(H)" in note and "H^(1/2)" in note)
    check("The atlas carries the PMNS right polar section row",
          "| PMNS right polar section |" in atlas)
    check("The reviewer packet records that the positive polar section makes the branch intrinsically readable from H",
          "positive polar section" in packet and "sheet-even" in packet)
    check("The intrinsic-boundary note now says the remaining gap is Hermitian-data law plus sheet-fixing datum",
          "selected-branch Hermitian data law" in intrinsic and "sheet-fixing datum" in intrinsic)

    print()
    print("  So the exact endpoint is sharper than before: on the generic")
    print("  Hermitian patch, branch readability is no longer the missing object.")


def main() -> int:
    print("=" * 88)
    print("PMNS RIGHT POLAR SECTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - neutrino and charged-lepton two-Higgs observable inverse problems")
    print("  - PMNS branch-conditioned quadratic-sheet closure")
    print("  - PMNS branch sheet nonforcing")
    print("  - PMNS right-frame orbit obstruction")
    print("  - PMNS right-conjugacy-invariant no-go")
    print()
    print("Question:")
    print("  Does the generic selected-branch right orbit already admit a")
    print("  canonical intrinsic representative from Hermitian data alone?")

    part1_generic_right_orbit_has_unique_positive_polar_representative()
    part2_positive_section_realizes_the_reduced_selector_from_hermitian_data()
    part3_positive_section_is_sheet_even_and_cannot_fix_the_residual_sheet()
    part4_the_bank_records_the_new_polar_section_endpoint()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact generic conditional answer:")
    print("    - the full-rank PMNS right orbit already has a unique positive")
    print("      representative Y_+(H) = H^(1/2)")
    print("    - on the one-sided minimal PMNS branches, comparing the positive")
    print("      off-diagonal support of H_nu^(1/2) and H_e^(1/2) realizes the")
    print("      reduced branch selector intrinsically from Hermitian data")
    print("    - but because the positive section factors only through H, it is")
    print("      sheet-even and cannot fix the residual selected-branch Z2 sheet")
    print()
    print("  So the remaining exact PMNS gap is sharper than 'find any right")
    print("  frame law'. Once branch Hermitian data are derived, the branch side")
    print("  is intrinsically readable. The truly remaining post-Hermitian datum")
    print("  is the residual non-Hermitian/right-sensitive sheet-fixing input.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
