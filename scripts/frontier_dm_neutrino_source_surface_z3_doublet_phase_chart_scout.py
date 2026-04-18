#!/usr/bin/env python3
"""
DM source-surface Z_3-doublet-phase chart-change scout.

Stress-tests the Case 3 microscopic polynomial impossibility theorem by
allowing the operator class to include non-Hermitian omega-eigenvectors
of C_3-conjugation on the retained hw=1 operator algebra M_3(C).

Goal.
  Determine whether Im(z^3) = 3 q_+^2 delta - delta^3 with z = q_+ + i delta
  is an axiom-native Z_3-invariant scalar, and (independently) whether any
  Z_3-irrep-natural complex doublet coordinate yields a delta-odd axiom-
  native scalar that also pins q_+.

Verdict.
  PARTIAL.

  (1) The prompt's z = q_+ + i delta is NOT Z_3-irrep-natural: q_+ is a
      singlet and delta is a doublet-real-slice, so (q_+, delta) does
      not transform as a single complex under C_3. Im(z^3) is NOT
      axiom-native as a retained Z_3-invariant scalar.

  (2) The correct Z_3-irrep-natural construction uses A(H) := Tr(H T_{d,w})
      where T_{d,w} is the omega-eigenvector of C_3-conjugation on T_delta.
      Direct computation gives A(H) = 3 delta + i sqrt(3) m and

        S(H) := A^3 + conj(A)^3 = 54 delta (delta^2 - m^2)

      which is a REAL Z_3-invariant DELTA-ODD polynomial in H.

  (3) S(H) depends only on (m, delta), NOT on q_+. So the axiom-native
      delta-odd content, once admitted, pins delta (modulo the Schur-fixed
      m) at delta in {0, m} (positive-delta gauge), but does NOT constrain
      q_+. The q_+-silence component of the impossibility theorem
      survives; the delta-evenness component is modified.

Deliverable.
  PASS count on (1) Z_3 irrep structure of T_delta and its omega-eigenvector
  decomposition; (2) prompt z = q_+ + i delta failing Z_3-irrep-naturalness;
  (3) A(H) identity; (4) S(H) explicit formula and delta-parity; (5)
  impossibility-theorem scope boundary; (6) exit classification.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    h_base,
    tdelta,
    tm,
    tq,
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


# ---------------------------------------------------------------------------
# Axiom-native constants and retained operators
# ---------------------------------------------------------------------------

OMEGA = np.exp(2j * math.pi / 3.0)

# Retained C_3[111] generator on H_hw=1 basis (X1, X2, X3) with X1->X2->X3->X1
C3 = np.array(
    [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=complex,
)
C3_INV = C3.conj().T
I3 = np.eye(3, dtype=complex)


def proj_c3_eigen(X: np.ndarray, eigenvalue: complex) -> np.ndarray:
    """Project X onto the C_3-conjugation eigenspace with given eigenvalue."""
    X0 = X
    X1 = C3 @ X @ C3_INV
    X2 = C3 @ C3 @ X @ C3_INV @ C3_INV
    return (X0 + np.conj(eigenvalue) * X1 + eigenvalue * X2) / 3.0


# ---------------------------------------------------------------------------
# Part 1: Z_3-irrep structure of T_delta and omega-eigenvector construction
# ---------------------------------------------------------------------------


def part1_doublet_omega_eigenvector() -> tuple[np.ndarray, np.ndarray]:
    """Part 1. Construct the omega- and omega-bar-eigenvectors of C_3
    conjugation on T_delta, and verify the eigenvalue equations.
    """
    print("\n" + "=" * 88)
    print("PART 1: DOUBLET OMEGA-EIGENVECTOR CONSTRUCTION")
    print("=" * 88)

    Td = tdelta()

    Td_w = proj_c3_eigen(Td, OMEGA)
    Td_wb = proj_c3_eigen(Td, OMEGA.conjugate())

    check(
        "Td_w is the omega-eigenvector: C_3 Td_w C_3^{-1} = omega Td_w",
        np.linalg.norm(C3 @ Td_w @ C3_INV - OMEGA * Td_w) < 1e-12,
        f"residual = {np.linalg.norm(C3 @ Td_w @ C3_INV - OMEGA * Td_w):.2e}",
    )
    check(
        "Td_wb is the omega-bar-eigenvector",
        np.linalg.norm(C3 @ Td_wb @ C3_INV - OMEGA.conjugate() * Td_wb) < 1e-12,
        "",
    )
    check(
        "Td_w + Td_wb = Td (completeness on the doublet)",
        np.linalg.norm(Td_w + Td_wb - Td) < 1e-12,
        f"residual = {np.linalg.norm(Td_w + Td_wb - Td):.2e}",
    )
    check(
        "Td_wb = (Td_w)^dagger (Hermitian conjugate structure)",
        np.linalg.norm(Td_w.conj().T - Td_wb) < 1e-12,
        "",
    )
    check(
        "Td_w is NOT Hermitian: ||Td_w - Td_w^dagger|| > 0",
        np.linalg.norm(Td_w - Td_w.conj().T) > 0.1,
        f"||Td_w - Td_w^dagger|| = {np.linalg.norm(Td_w - Td_w.conj().T):.4f}",
    )

    return Td_w, Td_wb


# ---------------------------------------------------------------------------
# Part 2: prompt's z = q_+ + i delta is NOT Z_3-irrep-natural
# ---------------------------------------------------------------------------


def part2_prompt_z_not_z3_natural() -> None:
    """Part 2. Show that the prompt's complex coordinate z = q_+ + i delta
    mixes a Z_3-singlet (q_+) with a Z_3-doublet-real-slice (delta), and
    therefore does not transform as an omega-eigenvector under C_3.
    """
    print("\n" + "=" * 88)
    print("PART 2: PROMPT z = q_+ + i delta IS NOT Z_3-IRREP-NATURAL")
    print("=" * 88)

    Tm = tm()
    Td = tdelta()
    Tq = tq()

    # Under C_3, Tq is singlet (fixed), Td rotates within doublet.
    check(
        "T_q is C_3-invariant (singlet): [C_3, T_q] = 0",
        np.allclose(C3 @ Tq @ C3_INV, Tq),
        "",
    )
    check(
        "T_delta is NOT C_3-invariant (doublet real-slice)",
        not np.allclose(C3 @ Td @ C3_INV, Td),
        f"||C3 Td C3^-1 - Td|| = {np.linalg.norm(C3 @ Td @ C3_INV - Td):.4f}",
    )

    # Z_3-irrep-natural complex doublet coords would have BOTH components
    # in the 2-D doublet. q_+ is not in the doublet; it's in the singlet.
    # Mixing q_+ with delta gives a chart-level complex number, not a
    # doublet coordinate in the irrep sense.

    # Check: the C_3-orbit of (q_+ = 1, delta = 1, m = 0) under conjugation
    # lands on a point with nontrivial Td_perp component — i.e., off the chart.
    H = 0.0 * Tm + 1.0 * Td + 1.0 * Tq
    H_rot = C3 @ H @ C3_INV
    # Project onto the chart span {Tm, Td, Tq}:
    basis = np.array([Tm.flatten(), Td.flatten(), Tq.flatten()])
    target = H_rot.flatten()
    coeffs, *_ = np.linalg.lstsq(basis.T, target, rcond=None)
    reconstructed = basis.T @ coeffs
    residual_off_chart = np.linalg.norm(target - reconstructed)
    check(
        "C_3(H(m=0, delta=1, q_+=1)) lands OFF the (m, delta, q_+) chart",
        residual_off_chart > 0.5,
        f"off-chart residual = {residual_off_chart:.4f}",
    )

    # So under C_3, the chart-level (q_+, delta) does NOT map to a rotated
    # (q_+, delta) — it picks up an off-chart doublet component.
    # Therefore z = q_+ + i delta does NOT transform as an omega-eigenvector.
    print("  => z = q_+ + i delta does NOT transform as omega-eigenvector under C_3;")
    print("     Im(z^3) = 3 q_+^2 delta - delta^3 is NOT a Z_3-invariant scalar.")


# ---------------------------------------------------------------------------
# Part 3: The correct Z_3-irrep-natural doublet coordinate A(H) = Tr(H T_{d,w})
# ---------------------------------------------------------------------------


def part3_axiom_native_doublet_coordinate(
    Td_w: np.ndarray, Td_wb: np.ndarray
) -> None:
    """Part 3. Establish A(H) = 3 delta + i sqrt(3) m as the Z_3-irrep-natural
    doublet complex coordinate on the chart.
    """
    print("\n" + "=" * 88)
    print("PART 3: CORRECT AXIOM-NATIVE DOUBLET COORDINATE A(H) = Tr(H T_{d,w})")
    print("=" * 88)

    Tm = tm()
    Td = tdelta()
    Tq = tq()

    def A_val(m, d, q):
        H = m * Tm + d * Td + q * Tq
        return np.trace(H @ Td_w)

    # Sample a grid and verify A(H) = 3 delta + i sqrt(3) m
    rng = np.random.default_rng(20260418)
    max_err = 0.0
    for _ in range(50):
        m = rng.uniform(-2.0, 2.0)
        d = rng.uniform(-2.0, 2.0)
        q = rng.uniform(-2.0, 2.0)
        A_num = A_val(m, d, q)
        A_pred = 3.0 * d + 1j * math.sqrt(3.0) * m
        err = abs(A_num - A_pred)
        if err > max_err:
            max_err = err
    check(
        "A(H) = Tr(H T_{d,w}) = 3*delta + i*sqrt(3)*m (exact)",
        max_err < 1e-10,
        f"max err = {max_err:.2e}",
    )

    # Observe: A has NO q_+-dependence. q_+ is singlet and cannot enter
    # a doublet coordinate.
    A_q_dep = A_val(0, 0, 1) - A_val(0, 0, 0)
    check(
        "A(H) has NO q_+ dependence (q_+ is singlet, not doublet)",
        abs(A_q_dep) < 1e-12,
        f"|A(q=1) - A(q=0)| at m=d=0: {abs(A_q_dep):.2e}",
    )

    # Under C_3 conjugation of H, A picks up omega^{-1} = omega-bar:
    H = 0.7 * Tm + 0.3 * Td + 0.5 * Tq
    A_H = np.trace(H @ Td_w)
    H_c3 = C3 @ H @ C3_INV
    A_H_c3 = np.trace(H_c3 @ Td_w)
    # Expected: A(C_3 H C_3^{-1}) = Tr(C_3 H C_3^{-1} Td_w) = Tr(H C_3^{-1} Td_w C_3)
    #   = omega^{-1} Tr(H Td_w) = omega-bar * A(H)
    check(
        "A(C_3 H C_3^{-1}) = omega-bar * A(H) (doublet transformation)",
        abs(A_H_c3 - OMEGA.conjugate() * A_H) < 1e-10,
        f"|A_rot - omega-bar * A| = {abs(A_H_c3 - OMEGA.conjugate() * A_H):.2e}",
    )


# ---------------------------------------------------------------------------
# Part 4: S(H) = A^3 + conj(A)^3 = 54 delta (delta^2 - m^2) is delta-odd axiom-native
# ---------------------------------------------------------------------------


def part4_doublet_phase_cubic(Td_w: np.ndarray, Td_wb: np.ndarray) -> None:
    """Part 4. Verify the real Z_3-invariant polynomial S(H) = A^3 +
    conj(A)^3 = 54 delta (delta^2 - m^2) and establish its delta-parity.
    """
    print("\n" + "=" * 88)
    print("PART 4: S(H) = A^3 + conj(A)^3 = 54 delta (delta^2 - m^2)")
    print("=" * 88)

    Tm = tm()
    Td = tdelta()
    Tq = tq()

    def S_val(m, d, q):
        H = m * Tm + d * Td + q * Tq
        A = np.trace(H @ Td_w)
        return (A ** 3 + np.conj(A) ** 3).real

    # Identity check
    rng = np.random.default_rng(20260419)
    max_err = 0.0
    for _ in range(60):
        m = rng.uniform(-2.0, 2.0)
        d = rng.uniform(-2.0, 2.0)
        q = rng.uniform(-2.0, 2.0)
        S_num = S_val(m, d, q)
        S_pred = 54.0 * d * (d * d - m * m)
        err = abs(S_num - S_pred)
        if err > max_err:
            max_err = err
    check(
        "S(H) = 54 * delta * (delta^2 - m^2)  (exact identity)",
        max_err < 1e-8,
        f"max err = {max_err:.2e}",
    )

    # Delta-parity: S(m, -d, q) = -S(m, d, q) (delta-ODD)
    max_err_parity = 0.0
    for _ in range(30):
        m = rng.uniform(-2.0, 2.0)
        d = rng.uniform(-2.0, 2.0)
        q = rng.uniform(-2.0, 2.0)
        err = abs(S_val(m, -d, q) + S_val(m, d, q))
        if err > max_err_parity:
            max_err_parity = err
    check(
        "S(H) is DELTA-ODD: S(m, -d, q) = -S(m, d, q)",
        max_err_parity < 1e-8,
        f"max violation = {max_err_parity:.2e}",
    )

    # q_+-independence
    max_err_q = 0.0
    for _ in range(30):
        m = rng.uniform(-2.0, 2.0)
        d = rng.uniform(-2.0, 2.0)
        q1 = rng.uniform(-2.0, 2.0)
        q2 = rng.uniform(-2.0, 2.0)
        err = abs(S_val(m, d, q1) - S_val(m, d, q2))
        if err > max_err_q:
            max_err_q = err
    check(
        "S(H) is INDEPENDENT of q_+ (singlet blindness)",
        max_err_q < 1e-8,
        f"max q-variation = {max_err_q:.2e}",
    )

    # Z_3-invariance: S(C_3 H C_3^{-1}) = S(H)
    max_err_z3 = 0.0
    for _ in range(30):
        m = rng.uniform(-2.0, 2.0)
        d = rng.uniform(-2.0, 2.0)
        q = rng.uniform(-2.0, 2.0)
        H = m * Tm + d * Td + q * Tq
        A_H = np.trace(H @ Td_w)
        S_H = (A_H ** 3 + np.conj(A_H) ** 3).real
        # Conjugated
        H_c = C3 @ H @ C3_INV
        A_c = np.trace(H_c @ Td_w)
        S_c = (A_c ** 3 + np.conj(A_c) ** 3).real
        err = abs(S_H - S_c)
        if err > max_err_z3:
            max_err_z3 = err
    check(
        "S(H) is Z_3-invariant: S(C_3 H C_3^{-1}) = S(H)",
        max_err_z3 < 1e-8,
        f"max violation = {max_err_z3:.2e}",
    )


# ---------------------------------------------------------------------------
# Part 5: Prompt's Im(z^3) is NOT axiom-native
# ---------------------------------------------------------------------------


def part5_prompt_imz3_not_axiom_native() -> None:
    """Part 5. Show that Im(z^3) = 3 q_+^2 delta - delta^3 with
    z = q_+ + i delta is NOT a Z_3-invariant scalar of H.
    """
    print("\n" + "=" * 88)
    print("PART 5: PROMPT'S Im(z^3) = 3 q_+^2 delta - delta^3 FAILS Z_3-INVARIANCE")
    print("=" * 88)

    Tm = tm()
    Td = tdelta()
    Tq = tq()

    def imz3(m, d, q):
        return 3.0 * q * q * d - d ** 3

    # Under C_3 of H, the "chart projection" of the rotated point takes
    # (m, delta, q) to (m', delta', q') with an off-chart residual.
    # Compute the chart-projected imz3 after C_3 and compare.
    basis = np.array([Tm.flatten(), Td.flatten(), Tq.flatten()])
    rng = np.random.default_rng(20260420)
    violations = []
    for _ in range(20):
        m = rng.uniform(-1.0, 1.0)
        d = rng.uniform(-1.0, 1.0)
        q = rng.uniform(-1.0, 1.0)
        H = m * Tm + d * Td + q * Tq
        H_c = C3 @ H @ C3_INV
        # Project H_c onto chart:
        coeffs, *_ = np.linalg.lstsq(basis.T, H_c.flatten(), rcond=None)
        m_c, d_c, q_c = coeffs[0].real, coeffs[1].real, coeffs[2].real
        imz3_orig = imz3(m, d, q)
        imz3_rot = imz3(m_c, d_c, q_c)
        if abs(imz3_orig - imz3_rot) > 1e-6:
            violations.append(abs(imz3_orig - imz3_rot))

    check(
        "Im(z^3) with z=q_+ + i delta is NOT Z_3-invariant under chart projection",
        len(violations) > 0,
        f"max violation = {max(violations):.4f} on 20 random points",
    )


# ---------------------------------------------------------------------------
# Part 6: Selector content and chamber analysis
# ---------------------------------------------------------------------------


def part6_selector_content(Td_w: np.ndarray) -> None:
    """Part 6. S(H) = 0 selects delta in {0, +m, -m}. In the positive-delta
    gauge (chamber), candidates are delta in {0, m}, q_+ remains free.
    """
    print("\n" + "=" * 88)
    print("PART 6: SELECTOR CONTENT OF S(H) = 0 AND CHAMBER ANALYSIS")
    print("=" * 88)

    # S = 54 d (d^2 - m^2). Zeros: d = 0, d = +m, d = -m.
    # Positive-delta gauge (Z_2 fix): delta >= 0.
    # Retained candidates: delta = 0 or delta = m (assuming m >= 0).
    # q_+ is unconstrained by S.

    # Numerical verification
    Tm = tm()
    Td = tdelta()
    Tq = tq()

    def S_val(m, d, q):
        H = m * Tm + d * Td + q * Tq
        A = np.trace(H @ Td_w)
        return (A ** 3 + np.conj(A) ** 3).real

    for m_val in [0.3, 0.7, 1.2]:
        for q_val in [0.5, 1.5, 2.5]:
            S0 = S_val(m_val, 0.0, q_val)
            Sm = S_val(m_val, m_val, q_val)
            Smn = S_val(m_val, -m_val, q_val)
            check(
                f"S(m={m_val}, d=0, q={q_val}) = 0",
                abs(S0) < 1e-8,
                f"S = {S0:.2e}",
            )
            check(
                f"S(m={m_val}, d={m_val}, q={q_val}) = 0",
                abs(Sm) < 1e-8,
                f"S = {Sm:.2e}",
            )
            check(
                f"S(m={m_val}, d=-{m_val}, q={q_val}) = 0",
                abs(Smn) < 1e-8,
                f"S = {Smn:.2e}",
            )

    # Confirm S is NONZERO off the zero locus
    off_vals = [S_val(1.0, 0.5, 0.0), S_val(1.0, 1.5, 0.0), S_val(0.5, 0.7, 0.0)]
    for v in off_vals:
        check(
            f"S is nonzero off the zero locus: S = {v:.4f}",
            abs(v) > 0.1,
            "",
        )

    print("")
    print("  Residual after S(H) = 0 selection in positive-delta chamber:")
    print("    delta ∈ {0, m}  (finite set)")
    print("    q_+     free")
    print("  => delta IS axiom-pinned (modulo m), q_+ is NOT.")


# ---------------------------------------------------------------------------
# Part 7: Scope boundary of the Case 3 impossibility theorem
# ---------------------------------------------------------------------------


def part7_scope_boundary(Td_w: np.ndarray) -> None:
    """Part 7. Confirm that the Case 3 impossibility theorem's Theorem 3
    (delta-evenness of Tr(H^k), det(H)) holds literally — S(H) is delta-odd
    because it uses the NON-HERMITIAN operator insertion T_{d,w}.
    """
    print("\n" + "=" * 88)
    print("PART 7: IMPOSSIBILITY-THEOREM SCOPE BOUNDARY")
    print("=" * 88)

    Tm = tm()
    Td = tdelta()
    Tq = tq()

    # Verify delta-evenness of Tr(H^k) and det(H)  — original theorem's claim
    rng = np.random.default_rng(20260421)
    max_err_t2 = 0.0
    max_err_t3 = 0.0
    max_err_det = 0.0
    for _ in range(30):
        m = rng.uniform(-1.5, 1.5)
        d = rng.uniform(-1.5, 1.5)
        q = rng.uniform(-1.5, 1.5)
        Hp = m * Tm + d * Td + q * Tq
        Hn = m * Tm + (-d) * Td + q * Tq
        err_t2 = abs(np.trace(Hp @ Hp) - np.trace(Hn @ Hn))
        err_t3 = abs(np.trace(Hp @ Hp @ Hp) - np.trace(Hn @ Hn @ Hn))
        err_det = abs(np.linalg.det(Hp) - np.linalg.det(Hn))
        max_err_t2 = max(max_err_t2, err_t2)
        max_err_t3 = max(max_err_t3, err_t3)
        max_err_det = max(max_err_det, err_det)
    check(
        "Tr(H^2) IS delta-even (original theorem's Thm 3)",
        max_err_t2 < 1e-10,
        f"max violation = {max_err_t2:.2e}",
    )
    check(
        "Tr(H^3) IS delta-even (original theorem's Thm 3)",
        max_err_t3 < 1e-10,
        f"max violation = {max_err_t3:.2e}",
    )
    check(
        "det(H) IS delta-even (original theorem's Thm 3)",
        max_err_det < 1e-10,
        f"max violation = {max_err_det:.2e}",
    )

    # Scope clarification: S(H) uses NON-HERMITIAN insertion T_{d,w}.
    check(
        "T_{d,w} is NOT Hermitian (NOT a retained Hermitian observable operator)",
        np.linalg.norm(Td_w - Td_w.conj().T) > 0.1,
        f"||Td_w - Td_w^dagger|| = {np.linalg.norm(Td_w - Td_w.conj().T):.4f}",
    )

    # S(H) IS Z_3-invariant but not covered by Thm 3's Hermitian-insertion scope.
    print("")
    print("  Scope reading:")
    print("   Original Thm 3: delta-evenness holds for Hermitian trace moments.")
    print("   This scout:     non-Hermitian omega-eigenvector insertions,")
    print("                   cubed into Z_3-invariants, yield delta-odd content.")
    print("                   Specifically: S(H) = A^3 + conj(A)^3 is delta-odd.")
    print("  => Thm 3 scope boundary is literally respected; its phrasing needs")
    print("     amendment to explicitly exclude omega-eigenvector-cubed insertions.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 88)
    print("DM SOURCE-SURFACE Z_3-DOUBLET-PHASE CHART-CHANGE SCOUT")
    print("=" * 88)
    print("Unit system: dimensionless chart (m, delta, q_+) on H_hw=1 affine chart")
    print("Axioms: Cl(3) on Z^3 only")

    Td_w, Td_wb = part1_doublet_omega_eigenvector()
    part2_prompt_z_not_z3_natural()
    part3_axiom_native_doublet_coordinate(Td_w, Td_wb)
    part4_doublet_phase_cubic(Td_w, Td_wb)
    part5_prompt_imz3_not_axiom_native()
    part6_selector_content(Td_w)
    part7_scope_boundary(Td_w)

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    print("=" * 88)
    print("")
    print("Exit classification: PARTIAL")
    print("  - delta-odd axiom-native scalar EXISTS: S(H) = 54 delta (delta^2 - m^2)")
    print("  - but S(H) is q_+-BLIND: no q_+ constraint from doublet-phase-cubic")
    print("  - prompt's Im(z^3) = 3 q_+^2 delta - delta^3 is NOT axiom-native")
    print("  - named gap: q_+-silence of the impossibility theorem survives")

    if FAIL_COUNT > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
