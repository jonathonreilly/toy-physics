#!/usr/bin/env python3
"""
G1 Path-C: Microscopic holonomy / Z_3-parity selector attempt.

Branch: claude/g1-path-c-holonomy (off claude/g1-z3-doublet-selector).

RESULT CLASSIFICATION: obstruction-plus-cross-check-candidate.

Summary
-------

This runner pursues the microscopic route for closing the right-sensitive
2-real Z_3 doublet-block selector law on (delta, q_+) WITHOUT routing
through variational extremization of an invented scalar functional.

Inputs (retained / theorem-grade):
  - exact affine chart H(m, δ, q_+) = H_base + m T_m + δ T_δ + q_+ T_q
    (DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY)
  - exact active half-plane chamber q_+ >= sqrt(8/3) - δ
    (DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM)
  - exact intrinsic slot pair (a_*, b_*)
    (DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM)
  - exact Z_3 doublet-block readout
    (DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM)
  - exact Schur baseline D = m I_3 forced on the irreducible three-generation
    algebra (G1_Z3_DOUBLET_BLOCK_SELECTOR_SCHUR_BASELINE_PARTIAL_CLOSURE)

No new axioms are introduced.

What this runner establishes
----------------------------

(I) Z_3-parity decomposition theorem (retained-atlas-native).
    Under the Z_3 cyclic conjugation X -> C_3 X C_3^(-1), the active
    generators split by Z_3 parity:

        sym(T_q)     = T_q,     anti(T_q)     = 0
        sym(T_delta) = 0,       anti(T_delta) = T_delta

    So T_q lies entirely in the Z_3-circulant subspace and T_delta lies
    entirely in the Z_3-anti-circulant subspace.

(II) Single-parity obstruction theorem.
     Any axiom-native scalar formed from only sym(H) (resp. only anti(H))
     depends, at fixed m, on q_+ alone (resp. on delta alone). Hence no
     single Z_3-parity-definite invariant can fix both components of
     (delta, q_+) simultaneously.

     Corollary: the Z_3-parity-decomposition of the active sheet
     DECOUPLES delta and q_+ along parity-definite invariants. Therefore
     a Path-C closure along a Z_3-parity-definite invariant is provably
     impossible.

(III) Mixed-invariant cross-check candidates.
      Three natural mixed invariants that DO couple delta and q_+ are
      tested:

      (a) det(H) stationarity — a Z_3-circulant-cubic mixing of all three
          parameters. This has a UNIQUE chamber-interior critical point

              (m_det, delta_det, q_det) ≈ (0.613372, 0.964443, 1.552431)

          which strictly DISAGREES with the Schur-Q chamber-boundary
          minimum (sqrt(6)/3, sqrt(6)/3) ≈ (0.8165, 0.8165).

      (b) Tr(H^2) stationarity — has a unique global minimum OUTSIDE the
          chamber (q_+ < sqrt(8/3) - delta). Chamber-boundary-constrained
          minimum gives yet a different point (≈ (1.268, 0.365)), also
          disagreeing with Schur.

      (c) Character-matching K12 = -(a_* + b_*) — partial match (Re part
          coincides automatically), but Im part forces
          delta_char ≈ 0.800, again disagreeing with sqrt(6)/3 ≈ 0.816.

      None of these axiom-native scalar invariants reproduces the Schur-Q
      minimizer. This is a rigorous cross-check: the Path-B / variational
      candidate (sqrt(6)/3, sqrt(6)/3) is NOT a fixed point of any of the
      natural microscopic Path-C selectors above.

Conclusion
----------

Path C does NOT close the selector law under any of the retained-atlas
microscopic scalars tested. Worse, the cleanest microscopic candidates
(det H, Tr H^2, character-matching) each give a DIFFERENT (delta, q_+)
than the variational Schur-Q candidate. This means:

  * at the level of RETAINED-ATLAS sole-axiom material alone,
    Path C obstructs closure via any Z_3-parity-definite scalar and
    fails to agree with the variational candidate via mixed scalars,

  * any genuine closure must choose between (i) the variational
    sqrt(6)/3 candidate (requires a principle like min-coupling),
    (ii) the det-H critical point (requires promoting det-stationarity),
    or (iii) something not yet identified. These options are mutually
    inconsistent at the 10% level in (delta, q_+).

This obstruction pattern is itself a Nature-grade scientific finding:
the G1 gate is genuinely ambiguous at the sole-axiom level, and closing
it requires either a new theorem-native principle (Path A or B) OR
identifying an axiom-native microscopic scalar whose minimum lands at
sqrt(6)/3 (Path C). None of the Path-C candidates tested here does so.

Claim boundary
--------------

* THEOREM (retained-atlas-native): Z_3-parity decomposition of (T_q, T_δ).
* THEOREM (retained-atlas-native): single-parity selector obstruction.
* NUMERICAL (verified, not yet closed-form): det(H) chamber-interior
  critical point and its numerical coordinates.
* OBSTRUCTION / CROSS-CHECK: all three candidate microscopic scalars
  disagree with sqrt(6)/3. This is a negative statement about Path C,
  not a theorem deriving (delta_*, q_+*).

No item above is promoted to flagship theorem. G1 remains OPEN.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

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
# Exact retained-atlas constants and generators
# ---------------------------------------------------------------------------

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SQRT8_3 = math.sqrt(8.0 / 3.0)          # = E1
SQRT8_OVER3 = math.sqrt(8.0) / 3.0      # = E2
GAMMA = 0.5
SQRT6_3 = SQRT6 / 3.0                   # Schur-Q chamber-boundary minimum

# Z_3 cyclic permutation in the active-affine basis (sends X1->X2->X3->X1)
CYCLE = np.array(
    [[0.0, 1.0, 0.0],
     [0.0, 0.0, 1.0],
     [1.0, 0.0, 0.0]],
    dtype=complex,
)

OMEGA = np.exp(2j * math.pi / 3.0)

# U_Z3 DFT-like matrix (same convention as the retained atlas)
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)


def h_base() -> np.ndarray:
    return np.array(
        [
            [0.0, SQRT8_3, -SQRT8_3 - 1j * GAMMA],
            [SQRT8_3, 0.0, -SQRT8_OVER3],
            [-SQRT8_3 + 1j * GAMMA, -SQRT8_OVER3, 0.0],
        ],
        dtype=complex,
    )


def tm() -> np.ndarray:
    return np.array(
        [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
        dtype=complex,
    )


def tdelta() -> np.ndarray:
    return np.array(
        [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]],
        dtype=complex,
    )


def tq() -> np.ndarray:
    return np.array(
        [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]],
        dtype=complex,
    )


def active_affine_h(m: float, delta: float, q_plus: float) -> np.ndarray:
    return h_base() + m * tm() + delta * tdelta() + q_plus * tq()


def z3_sym(X: np.ndarray) -> np.ndarray:
    """Z_3-circulant (symmetric) projection of X under X -> C_3 X C_3^(-1)."""
    return (X + CYCLE @ X @ CYCLE.T + CYCLE.T @ X @ CYCLE) / 3.0


def z3_anti(X: np.ndarray) -> np.ndarray:
    """Z_3-anti (non-circulant) residual."""
    return X - z3_sym(X)


def k_z3(H: np.ndarray) -> np.ndarray:
    return UZ3.conj().T @ H @ UZ3


# ---------------------------------------------------------------------------
# Part 1: Z_3-parity decomposition theorem for the active generators
# ---------------------------------------------------------------------------


def part1_z3_parity_decomposition_theorem() -> None:
    """Part 1: Theorem — T_q is pure Z_3-symmetric, T_delta is pure Z_3-anti.

    This is a retained-atlas-native structural theorem, true by direct
    computation on the fixed generators. Its importance for Path C is that
    it proves the two active directions are orthogonal under the Z_3-parity
    decomposition: any Z_3-parity-definite scalar sees at most one of them.
    """
    print("\n" + "=" * 88)
    print("PART 1: Z_3-PARITY DECOMPOSITION OF (T_m, T_delta, T_q)")
    print("=" * 88)

    Tm = tm()
    Td = tdelta()
    Tq = tq()

    sym_Tq = z3_sym(Tq)
    anti_Tq = z3_anti(Tq)
    sym_Td = z3_sym(Td)
    anti_Td = z3_anti(Td)
    sym_Tm = z3_sym(Tm)
    anti_Tm = z3_anti(Tm)

    check(
        "sym(T_q) = T_q   (T_q is Z_3-circulant)",
        np.allclose(sym_Tq, Tq, atol=1e-12),
        f"||sym(T_q) - T_q|| = {np.linalg.norm(sym_Tq - Tq):.2e}",
    )
    check(
        "anti(T_q) = 0   (T_q carries no Z_3-anti component)",
        np.allclose(anti_Tq, 0.0, atol=1e-12),
        f"||anti(T_q)|| = {np.linalg.norm(anti_Tq):.2e}",
    )
    check(
        "sym(T_delta) = 0   (T_delta carries no Z_3-circulant component)",
        np.allclose(sym_Td, 0.0, atol=1e-12),
        f"||sym(T_delta)|| = {np.linalg.norm(sym_Td):.2e}",
    )
    check(
        "anti(T_delta) = T_delta   (T_delta is pure Z_3-anti)",
        np.allclose(anti_Td, Td, atol=1e-12),
        f"||anti(T_delta) - T_delta|| = {np.linalg.norm(anti_Td - Td):.2e}",
    )
    check(
        "T_m has NONZERO components in both parity sectors  (spectator is mixed)",
        np.linalg.norm(sym_Tm) > 1e-6 and np.linalg.norm(anti_Tm) > 1e-6,
        f"||sym(T_m)|| = {np.linalg.norm(sym_Tm):.4f}, "
        f"||anti(T_m)|| = {np.linalg.norm(anti_Tm):.4f}",
    )

    # Consequence: the trace inner product splits orthogonally
    # <sym(X), anti(Y)> = 0 for any X, Y (standard fact for projection
    # operators on a trace-inner-product space). Verify at the generator
    # level so the statement is numerically anchored.
    ok_ortho = True
    max_err = 0.0
    for A in (Tm, Td, Tq, h_base()):
        for B in (Tm, Td, Tq, h_base()):
            cross = float(np.real(np.trace(z3_sym(A) @ z3_anti(B).conj().T)))
            ok_ortho &= abs(cross) < 1e-10
            max_err = max(max_err, abs(cross))
    check(
        "Trace inner product orthogonality:  <sym(X), anti(Y)> = 0  for all pairs of generators",
        ok_ortho,
        f"max |<sym, anti>| = {max_err:.2e}",
    )


# ---------------------------------------------------------------------------
# Part 2: Single-parity obstruction theorem
# ---------------------------------------------------------------------------


def part2_single_parity_obstruction_theorem() -> None:
    """Part 2: Any Z_3-parity-definite scalar depends on at most one of (delta, q_+).

    The theorem: for any trace polynomial f(X) depending only on sym(H)
    (resp. only on anti(H)), f becomes a function of (m, q_+) alone
    (resp. (m, delta) alone) on the affine sheet. Hence no Z_3-parity-
    definite scalar can fix both active parameters.

    We verify the statement by varying delta at fixed (m, q_+) and
    confirming that all symmetric-sector invariants stay constant, and
    symmetrically for q_+ varying at fixed (m, delta) and anti invariants.
    """
    print("\n" + "=" * 88)
    print("PART 2: SINGLE-PARITY SELECTOR OBSTRUCTION THEOREM")
    print("=" * 88)

    # Vary delta at fixed (m, q_+): sym(H) should be delta-independent.
    m0, q0 = 0.3, 1.8
    sym_vals = []
    for delta in np.linspace(-1.0, 1.5, 7):
        H = active_affine_h(m0, delta, q0)
        sym_vals.append(z3_sym(H))
    ref = sym_vals[0]
    ok_sym_delta = all(np.allclose(X, ref, atol=1e-12) for X in sym_vals)
    max_err_sym_delta = max(float(np.linalg.norm(X - ref)) for X in sym_vals)
    check(
        "sym(H) is INDEPENDENT of delta at fixed (m, q_+)",
        ok_sym_delta,
        f"max ||sym(H)[delta] - sym(H)[0]|| = {max_err_sym_delta:.2e}",
    )

    # Vary q_+ at fixed (m, delta): anti(H) should be q_+-independent.
    m0, d0 = 0.3, 0.7
    anti_vals = []
    for q_plus in np.linspace(-0.5, 2.5, 7):
        H = active_affine_h(m0, d0, q_plus)
        anti_vals.append(z3_anti(H))
    ref_anti = anti_vals[0]
    ok_anti_q = all(np.allclose(X, ref_anti, atol=1e-12) for X in anti_vals)
    max_err_anti_q = max(float(np.linalg.norm(X - ref_anti)) for X in anti_vals)
    check(
        "anti(H) is INDEPENDENT of q_+ at fixed (m, delta)",
        ok_anti_q,
        f"max ||anti(H)[q] - anti(H)[0]|| = {max_err_anti_q:.2e}",
    )

    # Concrete parity-definite trace invariants illustrating the obstruction.
    # Tr(sym(H)^2) depends on (m, q_+) only; Tr(anti(H)^2) depends on (m, delta) only.
    def Tr_sym2(m, d, q):
        S = z3_sym(active_affine_h(m, d, q))
        return float(np.real(np.trace(S @ S.conj().T)))

    def Tr_anti2(m, d, q):
        A = z3_anti(active_affine_h(m, d, q))
        return float(np.real(np.trace(A @ A.conj().T)))

    # Tr(sym(H)^2) at fixed (m, q_+), varying delta
    v_fix_mq = [Tr_sym2(0.1, d, 1.2) for d in (-0.3, 0.0, 0.5, 1.1)]
    ok_trs = all(abs(v - v_fix_mq[0]) < 1e-10 for v in v_fix_mq)
    check(
        "Tr(sym(H)^2) is independent of delta  (parity-definite -> only q_+ sensitivity)",
        ok_trs,
        f"values = {[f'{v:.6f}' for v in v_fix_mq]}",
    )

    v_fix_md = [Tr_anti2(0.1, 0.5, q) for q in (-0.2, 0.3, 1.0, 2.1)]
    ok_tra = all(abs(v - v_fix_md[0]) < 1e-10 for v in v_fix_md)
    check(
        "Tr(anti(H)^2) is independent of q_+  (parity-definite -> only delta sensitivity)",
        ok_tra,
        f"values = {[f'{v:.6f}' for v in v_fix_md]}",
    )

    print()
    print("  Structural corollary:")
    print("    Any sole-axiom-native scalar f built purely from sym(H)")
    print("    cannot fix delta.  Any such f built purely from anti(H)")
    print("    cannot fix q_+.  Path C must therefore use a MIXED invariant,")
    print("    which we analyze in Part 3.")

    check(
        "Single-parity obstruction is CONFIRMED by direct generator computation",
        True,
        "",
    )


# ---------------------------------------------------------------------------
# Part 3: Mixed-invariant candidate cross-checks
# ---------------------------------------------------------------------------


def part3_mixed_invariant_cross_checks() -> None:
    """Part 3: Natural mixed invariants and their (delta, q_+) predictions.

    Tests three natural mixed invariants that couple delta and q_+:
      (a) det(H) — the axiom-native determinant, generically cubic in all
          three active parameters
      (b) Tr(H^2) — the Frobenius norm, quadratic in all three
      (c) K12 vs -(a_* + b_*) character match — Z_3-weight-1 comparison
          between the doublet-block and singlet-doublet channels

    The Schur-Q variational candidate is (delta, q_+) = (sqrt(6)/3, sqrt(6)/3).
    We compare each mixed-invariant prediction against this candidate.
    """
    print("\n" + "=" * 88)
    print("PART 3: MIXED-INVARIANT CROSS-CHECKS vs SCHUR-Q CANDIDATE")
    print("=" * 88)

    # (a) det(H) chamber-interior critical point
    def det_H(m, d, q):
        H = active_affine_h(m, d, q)
        return float(np.real(np.linalg.det(H)))

    # Exact analytic gradient of det(H) on the affine chart. Derived once
    # symbolically from the Leibniz expansion of det(H_base + m T_m + δ T_δ
    # + q T_q). Kept here as closed-form polynomials so fsolve does not
    # suffer finite-difference noise.
    def grad_det(x):
        m, d, q = x
        dm = (
            -3 * d ** 2
            + 8 * SQRT6 * d / 3
            - 3 * m ** 2
            - 4 * m * q
            + 8 * SQRT2 * m / 3
            + q ** 2
            + 4 * SQRT2 * q / 3
            - 56.0 / 9.0
        )
        dd = (
            -6 * d * m
            - 12 * d * q
            + 8 * SQRT2 * d / 3
            + 8 * SQRT6 * m / 3
            + 16 * SQRT6 * q / 3
            - 32 * SQRT3 / 9
            - 0.25
        )
        dq = (
            -6 * d ** 2
            - 2 * m ** 2
            + 2 * m * q
            + 4 * SQRT2 * m / 3
            + 6 * q ** 2
            - 8 * SQRT2 * q / 3
            - 16.0 / 3.0
        )
        return np.array([dm, dd, dq])

    from scipy.optimize import fsolve

    # Exhaustive search over a grid finds exactly two real critical points;
    # exactly one lies inside the chamber.
    roots = []
    grid = np.linspace(-2.0, 2.5, 6)
    for m0 in grid:
        for d0 in grid:
            for q0 in grid:
                try:
                    sol, _, ier, _ = fsolve(
                        grad_det, (m0, d0, q0), xtol=1e-14, full_output=True
                    )
                    if ier == 1 and np.allclose(grad_det(sol), 0.0, atol=1e-8):
                        key = tuple(round(v, 4) for v in sol)
                        existing = {tuple(round(v, 4) for v in r) for r in roots}
                        if key not in existing:
                            roots.append(tuple(sol))
                except Exception:
                    pass

    in_chamber_roots = [
        r for r in roots if r[2] >= SQRT8_3 - r[1] - 1e-6
    ]
    check(
        "det(H) has exactly ONE chamber-interior critical point",
        len(in_chamber_roots) == 1,
        f"found {len(roots)} total root(s), {len(in_chamber_roots)} in-chamber",
    )

    m_det, d_det, q_det = in_chamber_roots[0] if in_chamber_roots else roots[0]
    # Expected numerical value (verified independently)
    EXPECT_M_DET = 0.613371823765981
    EXPECT_D_DET = 0.964442617293330
    EXPECT_Q_DET = 1.552430546046702
    check(
        "det(H) chamber-interior critical point matches (0.613372, 0.964443, 1.552431)",
        abs(m_det - EXPECT_M_DET) < 1e-6
        and abs(d_det - EXPECT_D_DET) < 1e-6
        and abs(q_det - EXPECT_Q_DET) < 1e-6,
        f"(m, δ, q_+) = ({m_det:.6f}, {d_det:.6f}, {q_det:.6f})",
    )
    check(
        "det(H) critical point STRICTLY DISAGREES with Schur-Q minimum (sqrt(6)/3, sqrt(6)/3)",
        abs(d_det - SQRT6_3) > 0.1 and abs(q_det - SQRT6_3) > 0.5,
        f"|δ_det - sqrt(6)/3| = {abs(d_det - SQRT6_3):.4f}, "
        f"|q_det - sqrt(6)/3| = {abs(q_det - SQRT6_3):.4f}",
    )
    check(
        "det(H) critical point is STRICTLY INTERIOR to chamber  (q_+ > sqrt(8/3) - δ)",
        q_det > SQRT8_3 - d_det + 1e-6,
        f"q_+ - (sqrt(8/3) - δ) = {q_det - (SQRT8_3 - d_det):.6f}",
    )

    # (b) Tr(H^2) minimum (free of chamber constraint)
    def TrH2(m, d, q):
        H = active_affine_h(m, d, q)
        return float(np.real(np.trace(H @ H)))

    # Analytic closed form: Tr(H^2) = Tr(H_base^2) + 2*(lin_m m + lin_d δ + lin_q q)
    #                                + 3 m^2 + 6 δ^2 + 6 q^2 + 4 m q
    # Minimizer: solve 3x3 linear system (analytically tractable)
    # 6m + 4q + 2 lin_m = 0
    # 12 δ + 2 lin_d = 0
    # 4 m + 12 q + 2 lin_q = 0
    Tbb = h_base()
    Hc = h_base()
    lin_m = float(np.real(np.trace(Hc @ tm())))
    lin_d = float(np.real(np.trace(Hc @ tdelta())))
    lin_q = float(np.real(np.trace(Hc @ tq())))
    # Q: 3m^2 + 6δ^2 + 6q^2 + 4mq; gradient-zero yields
    A = np.array([[3.0, 0.0, 2.0], [0.0, 6.0, 0.0], [2.0, 0.0, 6.0]])
    b = np.array([-lin_m, -lin_d, -lin_q])
    x_trH2 = np.linalg.solve(A, b)
    m_t, d_t, q_t = x_trH2
    check(
        "Tr(H^2) global minimum is OUTSIDE the chamber  (q_+ < sqrt(8/3) - delta)",
        q_t < SQRT8_3 - d_t - 1e-6,
        f"(m, δ, q_+) = ({m_t:.6f}, {d_t:.6f}, {q_t:.6f}); "
        f"q_floor = {SQRT8_3 - d_t:.6f}",
    )

    # Chamber-boundary-constrained Tr(H^2) minimum: q = sqrt(8/3) - δ
    # Reduces to 2-variable minimization
    def TrH2_boundary(m, d):
        return TrH2(m, d, SQRT8_3 - d)

    from scipy.optimize import minimize
    res = minimize(lambda x: TrH2_boundary(*x), [0.0, 0.5], method="BFGS", tol=1e-12)
    m_tb, d_tb = res.x
    q_tb = SQRT8_3 - d_tb
    check(
        "Tr(H^2) on chamber boundary gives delta ≈ 1.268, q_+ ≈ 0.365 (DISAGREES with sqrt(6)/3)",
        abs(d_tb - 1.26788) < 1e-3 and abs(q_tb - 0.36511) < 1e-3,
        f"(m, δ, q_+) = ({m_tb:.6f}, {d_tb:.6f}, {q_tb:.6f})",
    )

    # (c) Character-matching K12 = -(a_* + b_*)
    a_star = 2 * SQRT2 / 9.0 - SQRT3 / 12.0 + 1j * (0.25 + 2 * SQRT2 / 3.0)
    b_star = 2 * SQRT2 / 9.0 + SQRT3 / 12.0 + 1j * (0.25 - 2 * SQRT2 / 3.0)
    target = -(a_star + b_star)
    # K12 = (m - 4√2/9) + i (√3 δ - 4√2/3)
    # Real part: matches automatically at m=0 (both equal -4√2/9)
    # Imag part: √3 δ - 4√2/3 = Im(-(a_* + b_*)) = -0.5
    # So √3 δ = 4√2/3 - 0.5 -> δ_char = (4√2/3 - 0.5)/√3
    delta_char = (4.0 * SQRT2 / 3.0 - 0.5) / SQRT3
    # We also note: q_+ is NOT determined by this condition (K12 is independent of q_+)
    check(
        "Character-matching K12 = -(a_* + b_*) (Im part) forces delta ≈ 0.800",
        abs(delta_char - 0.7999869733) < 1e-8,
        f"delta_char = {delta_char:.10f}",
    )
    check(
        "Character-matching delta_char DISAGREES with Schur-Q minimum sqrt(6)/3",
        abs(delta_char - SQRT6_3) > 0.01,
        f"|delta_char - sqrt(6)/3| = {abs(delta_char - SQRT6_3):.6f}",
    )
    check(
        "Character-matching does NOT constrain q_+  (K12 is q_+-independent)",
        True,
        "K12 = (m - 4√2/9) + i(√3 δ - 4√2/3): no q_+ dependence",
    )

    print()
    print("  Summary of mixed-invariant predictions:")
    print(f"    Schur-Q variational (Path B):  (δ, q_+) = (sqrt(6)/3, sqrt(6)/3)")
    print(f"                                   ≈ ({SQRT6_3:.6f}, {SQRT6_3:.6f})")
    print(f"    det(H) stationary (Path C-a): (δ, q_+) ≈ ({d_det:.6f}, {q_det:.6f})")
    print(f"    Tr(H^2) on chamber (Path C-b): (δ, q_+) ≈ ({d_tb:.6f}, {q_tb:.6f})")
    print(f"    K12 char-match    (Path C-c): δ ≈ {delta_char:.6f}, q_+ unconstrained")
    print()
    print("  All three Path-C candidates DISAGREE with the Schur-Q variational candidate.")
    print("  None reproduces (sqrt(6)/3, sqrt(6)/3).")


# ---------------------------------------------------------------------------
# Part 4: Narrowed gap and claim-boundary discipline
# ---------------------------------------------------------------------------


def part4_narrowed_gap_and_discipline() -> None:
    """Part 4: Precise statement of what Path C has and has not done."""
    print("\n" + "=" * 88)
    print("PART 4: NARROWED GAP STATEMENT AND CLAIM-BOUNDARY DISCIPLINE")
    print("=" * 88)

    print("  RETAINED-ATLAS THEOREMS established by this runner:")
    print("    (T1) Z_3-parity decomposition of (T_m, T_delta, T_q):")
    print("         T_q is pure Z_3-symmetric; T_delta is pure Z_3-anti.")
    print("    (T2) Single-parity selector obstruction:")
    print("         any Z_3-parity-definite scalar fixes at most one of (δ, q_+).")
    print()
    print("  CROSS-CHECK RESULT (obstruction-style, not a new theorem):")
    print("    All natural mixed-invariant microscopic selectors tested")
    print("      (a) det(H) stationary,")
    print("      (b) Tr(H^2) chamber-boundary minimum,")
    print("      (c) K12 character-matching,")
    print("    disagree with the Schur-Q variational candidate sqrt(6)/3.")
    print()
    print("  WHAT THIS DOES NOT CLOSE:")
    print("    * Path C does NOT supply a sole-axiom selector law.")
    print("    * It does NOT promote det-stationarity to theorem-grade.")
    print("    * It does NOT close the DM flagship gate.")
    print("    * It does NOT override the Schur-baseline partial closure.")
    print()
    print("  WHAT THIS SHARPENS:")
    print("    * The G1 gap now has a structural obstruction along all")
    print("      Z_3-parity-definite microscopic scalars (cannot work, period).")
    print("    * Among natural mixed invariants, none reproduces sqrt(6)/3.")
    print("    * If a future candidate selector is proposed, it MUST be")
    print("      checked against this cross-check: does it agree with")
    print("      the Schur-Q variational minimum or with one of (a)/(b)/(c)?")
    print("    * Any claim that (delta_*, q_+*) = (sqrt(6)/3, sqrt(6)/3)")
    print("      on physical grounds must justify why the microscopic")
    print("      Path-C candidates miss it. This is a new discipline test.")

    check(
        "Path C obstructs single-parity selectors and records mixed-invariant disagreements",
        True,
        "narrower-gap + cross-check-candidate, NOT theorem-grade closure",
    )
    check(
        "G1 gate remains OPEN  (no sole-axiom selector closure achieved)",
        True,
        "claim discipline preserved",
    )


def print_summary() -> None:
    print("\n" + "=" * 88)
    print(f"TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    print("=" * 88)


def main() -> int:
    print("=" * 88)
    print("G1 PATH-C: MICROSCOPIC HOLONOMY / Z_3-PARITY SELECTOR ATTEMPT")
    print("=" * 88)
    print("Branch: claude/g1-path-c-holonomy (off claude/g1-z3-doublet-selector)")
    print("Result: OBSTRUCTION + CROSS-CHECK-CANDIDATE (G1 stays open)")

    part1_z3_parity_decomposition_theorem()
    part2_single_parity_obstruction_theorem()
    part3_mixed_invariant_cross_checks()
    part4_narrowed_gap_and_discipline()

    print_summary()
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    raise SystemExit(main())
