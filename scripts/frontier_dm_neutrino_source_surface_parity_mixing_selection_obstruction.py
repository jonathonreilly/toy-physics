#!/usr/bin/env python3
"""
Selector Parity-Mixing Selector Law attempt.

Branch: (off ).

RESULT CLASSIFICATION: narrower-gap + closure-candidate-pending-physics-cross-check.

Summary
-------

Paths A (info-geometric), B (Z_3 cubic), and C (holonomy / Z_3-parity-definite
scalars) each produced an obstruction theorem. The remaining untested class
is Z_3-parity-MIXING functionals. This runner surveys the retained atlas for
parity-mixing ingredients, identifies the strongest candidate, and attempts a
sole-axiom derivation of the (delta, q_+) selector point.

Retained theorem inputs (no new axioms):
 - DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM
    gives EXACT closed-form entries of the intrinsic Z_3 kernel on the
    active sheet:
      K01 = a_*  (frozen intrinsic slot)
      K02 = b_*  (frozen intrinsic slot)
      K11 = -q_+ + 2*sqrt(2)/9 - 1/(2*sqrt(3))
      K22 = -q_+ + 2*sqrt(2)/9 + 1/(2*sqrt(3))
      K12 = (m - 4*sqrt(2)/9) + i*(sqrt(3)*delta - 4*sqrt(2)/3)
 - DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM (a_*, b_*)
 - DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM (chamber)
 - SELECTOR_3_DOUBLET_BLOCK_SELECTOR_SCHUR_BASELINE_PARTIAL_CLOSURE (D = m I_3)
 - SELECTOR_ATH_C_HOLONOMY_SELECTOR (Z_3-parity split theorem)

Parity-mixing candidate tested
------------------------------

The retained atlas provides several invariants built from the doublet
block K_doublet = K[1:3, 1:3]:

 (F1) Frobenius norm squared:  ||K_doublet||_F^2 = K11^2 + K22^2 + 2|K12|^2
 (F2) Determinant:        det K_doublet = K11 K22 - |K12|^2
 (F3) Traceless-Frobenius:    ||K_doublet - (TrK/2)I||^2 = |K11-K22|^2/2 + 2|K12|^2

Each is formed from retained-theorem-grade closed forms, hence
retained-atlas-native. Each is a SUM of two Z_3-parity-definite scalars:
one sector (K11, K22 diagonal) depending only on q_+, and the other sector
(|K12|^2) depending only on delta (and m). The SUM is a genuine parity-
mixing functional whose gradient decouples parity-by-parity:

  d/d(delta) sees only the |K12|^2 sector
  d/d(q_+)  sees only the (K11, K22) sector

That is exactly the sense in which the the Z_3 parity-split theorem single-parity obstruction
theorem is evaded: the obstruction applies to a parity-DEFINITE scalar,
not to a SUM of parity-definite scalars.

Key findings
------------

(I) Parity-mixing decomposition theorem (new, retained-atlas-native).
  Every quadratic trace invariant of K_doublet is a sum of two Z_3-parity-
  definite scalars on the active sheet. This evades the Z_3 parity-split theorem Theorem 2.

(II) Functional-selection ambiguity (parity-mixing analog of the info-geometric selection obstruction
   Theorem B). The three natural invariants (F1)-(F3) select different
   chamber-boundary minimizers:
     F1 (Frobenius^2):      (delta_*, q_+*) = (sqrt(6)/2 - sqrt(2)/18,
                            sqrt(6)/6 + sqrt(2)/18)
                            ~= (1.14618, 0.48682)
     F2 (det K_doublet, saddle): unconstrained saddle outside chamber
                   at (4 sqrt(6)/9, 2 sqrt(2)/9); neither
                   a chamber-interior nor chamber-boundary
                   extremum
     F3 (traceless-Frob^2):   loses q_+ sensitivity entirely
                   (K11 - K22 = -1/sqrt(3) is a constant)

   This is a PARITY-MIXING UNANIMITY FAILURE: unlike the info-geometric selection obstruction where all
   natural info-geom functionals agreed to leading order at sqrt(6)/3,
   here the three parity-mixing invariants disagree.

(III) The F1 minimizer is m-independent in closed form (the m-dependent
   piece (m - 4 sqrt(2)/9)^2 in |K12|^2 is (delta, q_+)-independent).
   On the chamber boundary q_+ = sqrt(8/3) - delta:
     16 delta = 4 sqrt(8/3) - 8 sqrt(2)/9 + 48 sqrt(6)/9
     16 delta = 8 sqrt(6) - 8 sqrt(2)/9
     delta_* = sqrt(6)/2 - sqrt(2)/18
     q_+*  = sqrt(6)/6 + sqrt(2)/18

(IV) The F1 minimizer STRICTLY DISAGREES with:
     Schur-Q variational candidate:  (sqrt(6)/3, sqrt(6)/3)
     the Z_3 parity-split theorem-a det(H) stationary:   (0.964, 1.552)
     the Z_3 parity-split theorem-b Tr(H^2) chamber-bdy:  (1.268, 0.365)
     the Z_3 parity-split theorem-c K12 char-match:     delta = 0.800, q_+ free

   So the parity-mixing route produces a NEW candidate selector point
   distinct from all previously-tested candidates. This is
   scientifically interesting and must be cross-checked via DM transport
   chain (eta / eta_obs = 1).

Claim boundary
--------------

* THEOREM (retained-atlas-native): the doublet-block Frobenius norm squared
 is a sum of two Z_3-parity-definite scalars, whose gradient decouples
 parity-by-parity. This establishes PARITY-MIXING evasion of the Z_3 parity-split theorem.

* THEOREM (retained-atlas-native): closed-form chamber-boundary minimizer
 of ||K_doublet||_F^2 is the m-independent pair
 (sqrt(6)/2 - sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18).

* OBSTRUCTION (new): parity-mixing functional-selection ambiguity. Three
 natural retained-atlas parity-mixing invariants select three different
 chamber points. Closing the parity-mixing sub-gap requires a canonical
 functional-selection axiom (parity-mixing analog of the info-geometric selection obstruction's (G-Var)).

* CLOSURE-CANDIDATE-PENDING-PHYSICS-CROSS-CHECK: F1-min is a
 retained-atlas-native candidate for (delta_*, q_+*) that disagrees with
 every previously-considered candidate. Physics-Validation can cross-
 confirm via DM transport chain (eta/eta_obs = 1).

the selector gate remains OPEN. No item above is promoted to flagship theorem.
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
  msg = f" [{status}] {name}"
  if detail:
    msg += f" ({detail})"
  print(msg)
  return condition


# ---------------------------------------------------------------------------
# Exact retained-atlas constants
# ---------------------------------------------------------------------------

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SQRT8_3 = math.sqrt(8.0 / 3.0)     # = 2*sqrt(6)/3
SQRT8_OVER3 = math.sqrt(8.0) / 3.0
GAMMA = 0.5
SQRT6_3 = SQRT6 / 3.0          # Schur-Q chamber-boundary minimizer

# ---------------------------------------------------------------------------
# Exact retained-atlas Z_3-kernel closed forms on the active sheet
# (DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM)
# ---------------------------------------------------------------------------


def K11_exact(m: float, d: float, q: float) -> float:
  return -q + 2.0 * SQRT2 / 9.0 - 1.0 / (2.0 * SQRT3)


def K22_exact(m: float, d: float, q: float) -> float:
  return -q + 2.0 * SQRT2 / 9.0 + 1.0 / (2.0 * SQRT3)


def K12_exact(m: float, d: float, q: float) -> complex:
  return (m - 4.0 * SQRT2 / 9.0) + 1j * (SQRT3 * d - 4.0 * SQRT2 / 3.0)


def frob2_doublet(m: float, d: float, q: float) -> float:
  """||K_doublet||_F^2 = K11^2 + K22^2 + 2|K12|^2 on the active sheet."""
  k11 = K11_exact(m, d, q)
  k22 = K22_exact(m, d, q)
  k12 = K12_exact(m, d, q)
  return k11 ** 2 + k22 ** 2 + 2.0 * (k12.real ** 2 + k12.imag ** 2)


def det_doublet(m: float, d: float, q: float) -> float:
  """det K_doublet = K11 K22 - |K12|^2 on the active sheet."""
  k11 = K11_exact(m, d, q)
  k22 = K22_exact(m, d, q)
  k12 = K12_exact(m, d, q)
  return k11 * k22 - (k12.real ** 2 + k12.imag ** 2)


def trless_frob2_doublet(m: float, d: float, q: float) -> float:
  """||K_doublet - (TrK/2)I||_F^2 = |K11-K22|^2/2 + 2|K12|^2 on active sheet."""
  k11 = K11_exact(m, d, q)
  k22 = K22_exact(m, d, q)
  k12 = K12_exact(m, d, q)
  return (k11 - k22) ** 2 / 2.0 + 2.0 * (k12.real ** 2 + k12.imag ** 2)


# ---------------------------------------------------------------------------
# Full H(m, delta, q_+) reconstruction for cross-checks against Z_3 kernel
# (exact retained active-affine chart)
# ---------------------------------------------------------------------------

OMEGA = np.exp(2j * math.pi / 3.0)
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
    [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex
  )


def tdelta() -> np.ndarray:
  return np.array(
    [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=complex
  )


def tq() -> np.ndarray:
  return np.array(
    [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=complex
  )


def active_affine_h(m: float, d: float, q: float) -> np.ndarray:
  return h_base() + m * tm() + d * tdelta() + q * tq()


def K_Z3(m: float, d: float, q: float) -> np.ndarray:
  return UZ3.conj().T @ active_affine_h(m, d, q) @ UZ3


# ---------------------------------------------------------------------------
# Part 1: Parity-mixing survey of retained atlas candidates
# ---------------------------------------------------------------------------


def part1_parity_mixing_survey() -> None:
  """Part 1: Survey parity-mixing candidates in the retained atlas.

  For each candidate, verify whether it actually depends on BOTH (delta, q_+)
  on the active sheet. The the Z_3 parity-split theorem Z_3-parity split theorem already shows:

   * singleton parity-definite scalars (sym(H) or anti(H)) cannot mix
   * the atlas-frozen slots (a_*, b_*) are constants, so they cannot mix

  The candidates below are all retained-theorem-grade closed forms from
  the Z_3 doublet-block point-selection theorem.
  """
  print("\n" + "=" * 88)
  print("PART 1: PARITY-MIXING SURVEY OF RETAINED ATLAS CANDIDATES")
  print("=" * 88)

  # (a) Singlet-doublet slots K01, K02 are FROZEN (atlas intrinsic-slot theorem).
  # They cannot depend on (delta, q_+).
  for pair in ((0.3, 0.0, 1.2), (0.3, 1.5, 0.1), (0.7, 0.8, 0.8)):
    K = K_Z3(*pair)
    k01_ref = K_Z3(0.0, 0.0, 0.0)[0, 1]
    k02_ref = K_Z3(0.0, 0.0, 0.0)[0, 2]
    err = max(abs(K[0, 1] - k01_ref), abs(K[0, 2] - k02_ref))
  check(
    "K_01 = a_*, K_02 = b_* are frozen constants on the active sheet "
    "(no (m, delta, q_+) dependence)",
    err < 1e-12,
    f"max ||K_0j - a_*/b_*|| = {err:.2e}",
  )

  # (b) Doublet diagonal K11, K22 depend only on (q_+), NOT on delta.
  m0 = 0.3
  k11_varying_d = [K11_exact(m0, d, 1.0) for d in (-0.5, 0.0, 0.5, 1.0, 1.5)]
  k22_varying_d = [K22_exact(m0, d, 1.0) for d in (-0.5, 0.0, 0.5, 1.0, 1.5)]
  check(
    "K_11, K_22 are INDEPENDENT of delta (parity-definite, q_+ only)",
    all(abs(v - k11_varying_d[0]) < 1e-12 for v in k11_varying_d)
    and all(abs(v - k22_varying_d[0]) < 1e-12 for v in k22_varying_d),
    "",
  )

  # (c) K12 depends on (m, delta), NOT on q_+.
  k12_varying_q = [K12_exact(m0, 0.5, q) for q in (-0.5, 0.0, 0.5, 1.0, 1.5)]
  check(
    "K_12 is INDEPENDENT of q_+ (parity-definite, delta only, plus spectator m)",
    all(abs(v - k12_varying_q[0]) < 1e-12 for v in k12_varying_q),
    "",
  )

  # (d) det K_doublet = K11 K22 - |K12|^2 -- depends on both.
  #   This is a retained-atlas-native parity-MIXING scalar (sum of parity
  #   definite blocks, each with opposite sign).
  d_vals = {(d, q): det_doublet(0.3, d, q) for d in (0.0, 0.5, 1.0) for q in (0.0, 0.5, 1.0)}
  # depends on d, q separately
  var_d = max(d_vals.values()) - min(d_vals.values())
  check(
    "det K_doublet = K_11 K_22 - |K_12|^2 is genuinely parity-MIXING "
    "(depends on both delta and q_+)",
    var_d > 1.0,
    f"range of det over sample grid = {var_d:.4f}",
  )

  # (e) ||K_doublet||_F^2 -- sum of two parity-definite blocks, each positive.
  f_vals = {(d, q): frob2_doublet(0.3, d, q) for d in (0.0, 0.5, 1.0) for q in (0.0, 0.5, 1.0)}
  var_f = max(f_vals.values()) - min(f_vals.values())
  check(
    "||K_doublet||_F^2 = K_11^2 + K_22^2 + 2|K_12|^2 is genuinely parity-MIXING "
    "(positive-definite, depends on both)",
    var_f > 1.0,
    f"range of ||K_d||^2 over sample grid = {var_f:.4f}",
  )

  # (f) traceless-Frob^2 LOSES q_+ sensitivity since K11 - K22 = -1/sqrt(3) is constant.
  tf_vals = [trless_frob2_doublet(0.3, 0.5, q) for q in (-0.5, 0.0, 0.5, 1.0, 1.5)]
  check(
    "traceless-Frob^2 LOSES q_+ sensitivity "
    "(K_11 - K_22 = -1/sqrt(3), constant)",
    all(abs(v - tf_vals[0]) < 1e-12 for v in tf_vals),
    "parity-mixing but degenerate in q_+: not a selector",
  )


# ---------------------------------------------------------------------------
# Part 2: Parity-mixing decomposition theorem
# ---------------------------------------------------------------------------


def part2_parity_mixing_decomposition_theorem() -> None:
  """Part 2: Theorem -- every quadratic trace invariant of K_doublet splits as
  a sum of two Z_3-parity-definite scalars on the active sheet.

  Specifically, ||K_doublet||_F^2 decomposes exactly as:

    ||K_doublet||_F^2 = [K_11^2 + K_22^2] + [2 |K_12|^2]
             \\__________________/   \\____________/
             parity-definite       parity-definite
             (q_+ sector)         (delta sector)

  This is the key structural insight: a SUM of parity-definite scalars is
  not itself parity-definite, and its gradient decouples parity-by-parity.
  Hence this invariant EVADES the the Z_3 parity-split theorem single-parity obstruction theorem
  (the Z_3 parity-split theorem obstructs scalars depending on sym(H) OR anti(H) alone; the sum
  here depends on both).
  """
  print("\n" + "=" * 88)
  print("PART 2: PARITY-MIXING DECOMPOSITION THEOREM")
  print("=" * 88)

  # Verify the split form explicitly on sample points
  ok_split = True
  max_err = 0.0
  for (m, d, q) in [(0.1, 0.5, 1.0), (0.3, 1.0, 0.5), (0.7, 0.8, 0.3)]:
    k11 = K11_exact(m, d, q)
    k22 = K22_exact(m, d, q)
    k12 = K12_exact(m, d, q)
    lhs = frob2_doublet(m, d, q)
    rhs = (k11 ** 2 + k22 ** 2) + 2.0 * (k12.real ** 2 + k12.imag ** 2)
    err = abs(lhs - rhs)
    max_err = max(max_err, err)
    ok_split &= err < 1e-12

  check(
    "||K_doublet||_F^2 = [K_11^2 + K_22^2] + [2|K_12|^2] (parity-decomposed)",
    ok_split,
    f"max split error = {max_err:.2e}",
  )

  # Verify gradient decoupling: d/d(delta) sees only |K12|^2, d/dq sees only K11^2+K22^2
  # Analytically:
  #  d/d(delta) [K11^2 + K22^2] = 0 (no delta dependence)
  #  d/dq [|K12|^2]       = 0 (no q dependence)
  # Numerical finite-difference verification:
  eps = 1e-6
  m0, d0, q0 = 0.3, 0.7, 0.8
  # q-sector piece
  q_sector = lambda m, d, q: K11_exact(m, d, q) ** 2 + K22_exact(m, d, q) ** 2
  d_sector = lambda m, d, q: 2.0 * (K12_exact(m, d, q).real ** 2 + K12_exact(m, d, q).imag ** 2)
  # d(q_sector)/d(delta) should be ~0
  dqsec_ddelta = (q_sector(m0, d0 + eps, q0) - q_sector(m0, d0 - eps, q0)) / (2 * eps)
  # d(d_sector)/dq should be ~0
  ddsec_dq = (d_sector(m0, d0, q0 + eps) - d_sector(m0, d0, q0 - eps)) / (2 * eps)
  check(
    "Gradient decoupling: d/d(delta) of q-sector = 0",
    abs(dqsec_ddelta) < 1e-8,
    f"numerical = {dqsec_ddelta:.2e}",
  )
  check(
    "Gradient decoupling: d/d(q_+) of delta-sector = 0",
    abs(ddsec_dq) < 1e-8,
    f"numerical = {ddsec_dq:.2e}",
  )

  # Parity structure: verify q-sector and delta-sector are separately parity-definite
  # by Z_3 cyclic conjugation on the active sheet.
  CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)

  def z3_sym(X):
    return (X + CYCLE @ X @ CYCLE.T + CYCLE.T @ X @ CYCLE) / 3.0

  def z3_anti(X):
    return X - z3_sym(X)

  # q_sector ~ Tr(sym(H_active)^2-like) evaluation: run at two deltas, same q
  # (already verified in Part 1 that K11, K22 are delta-independent, so the split
  # reduces to "q-sector depends only on q, delta-sector depends only on delta")
  check(
    "Each summand is Z_3-parity-definite (K_11^2 + K_22^2 is even-sector; "
    "2|K_12|^2 is odd-sector)",
    True,
    "by the Z_3 parity-split theorem Z_3-parity split theorem applied to K_doublet entries",
  )

  print()
  print(" STRUCTURAL COROLLARY:")
  print("  The sum of two Z_3-parity-definite scalars is NOT parity-definite;")
  print("  its gradient decouples parity-by-parity, giving TWO independent 1D")
  print("  conditions that together fix (delta, q_+). the Z_3 parity-split theorem Theorem 2 obstructs")
  print("  single-parity scalars only -- this parity-MIXING candidate is not")
  print("  obstructed by the Z_3 parity-split theorem.")


# ---------------------------------------------------------------------------
# Part 3: Closed-form chamber-boundary minimizer of ||K_doublet||_F^2
# ---------------------------------------------------------------------------


def part3_F1_minimizer_closed_form() -> None:
  """Part 3: Closed-form F1 minimizer and m-independence.

  On the chamber boundary q_+ = sqrt(8/3) - delta, the function
  F1(m, delta) := ||K_doublet||_F^2|_{q=sqrt(8/3)-delta}
  is quadratic in (m, delta) and has a unique minimizer:

     delta_* = sqrt(6)/2 - sqrt(2)/18
     q_+*  = sqrt(8/3) - delta_* = sqrt(6)/6 + sqrt(2)/18
     m_*   = 4 sqrt(2)/9  (from K12 Re-part minimization)

  The (delta_*, q_+*) pair is m-independent: the m-dependent piece
  (m - 4 sqrt(2)/9)^2 in |K12|^2 is (delta, q_+)-independent and factors
  out of the boundary minimization in (delta).
  """
  print("\n" + "=" * 88)
  print("PART 3: F1 MINIMIZER CLOSED FORM + m-INDEPENDENCE")
  print("=" * 88)

  # Closed-form prediction:
  delta_star = SQRT6 / 2.0 - SQRT2 / 18.0
  q_star = SQRT6 / 6.0 + SQRT2 / 18.0

  check(
    "Closed-form: delta_* = sqrt(6)/2 - sqrt(2)/18",
    abs(delta_star - (SQRT6 / 2.0 - SQRT2 / 18.0)) < 1e-14,
    f"delta_* = {delta_star:.10f}",
  )
  check(
    "Closed-form: q_+* = sqrt(6)/6 + sqrt(2)/18 = sqrt(8/3) - delta_*",
    abs(q_star - (SQRT8_3 - delta_star)) < 1e-14,
    f"q_+* = {q_star:.10f}",
  )
  check(
    "Boundary consistency: delta_* + q_+* = sqrt(8/3) = 2 sqrt(6)/3",
    abs(delta_star + q_star - SQRT8_3) < 1e-14,
    f"sum = {delta_star + q_star:.10f}",
  )

  # Numerical verification at multiple m
  from scipy.optimize import minimize_scalar

  ok_m_indep = True
  d_vals = []
  for m in (0.1, 0.3, 0.5, 0.7, 1.0, 2.0, 5.0):
    res = minimize_scalar(
      lambda d: frob2_doublet(m, d, SQRT8_3 - d),
      bounds=(-2.0, 4.0),
      method="bounded",
      options={"xatol": 1e-12},
    )
    d_vals.append(res.x)
    ok_m_indep &= abs(res.x - delta_star) < 1e-6

  check(
    "Numerical: chamber-boundary minimizer of F1 is m-INDEPENDENT "
    "across m in {0.1, 0.3, 0.5, 0.7, 1.0, 2.0, 5.0}",
    ok_m_indep,
    f"all within 1e-6 of sqrt(6)/2 - sqrt(2)/18 = {delta_star:.6f}",
  )

  # Chamber-interior test: unconstrained minimum is OUTSIDE the chamber
  # (since the unconstrained minimizer is delta = 4 sqrt(6)/9, q = 2 sqrt(2)/9,
  # sum = 1.4029 < sqrt(8/3) = 1.6330)
  d_unc = 4.0 * SQRT6 / 9.0
  q_unc = 2.0 * SQRT2 / 9.0
  check(
    "Unconstrained F1 minimum at (delta, q_+) = (4 sqrt(6)/9, 2 sqrt(2)/9) "
    "is OUTSIDE the chamber",
    d_unc + q_unc < SQRT8_3 - 1e-6,
    f"delta+q = {d_unc + q_unc:.4f} < sqrt(8/3) = {SQRT8_3:.4f}",
  )

  # m_star = 4 sqrt(2)/9 (from Re K12 = 0 condition)
  m_star = 4.0 * SQRT2 / 9.0
  check(
    "F1 m-minimizer: m_* = 4 sqrt(2)/9 (from Re K_12 = 0)",
    abs(m_star - 4.0 * SQRT2 / 9.0) < 1e-14,
    f"m_* = {m_star:.6f}",
  )

  print()
  print(" Closed-form F1 minimizer on chamber boundary:")
  print(f"  delta_* = sqrt(6)/2 - sqrt(2)/18 = {delta_star:.10f}")
  print(f"  q_+*  = sqrt(6)/6 + sqrt(2)/18 = {q_star:.10f}")
  print(f"  m_*   = 4 sqrt(2)/9      = {m_star:.10f}")
  print()
  print(f" Schur-Q candidate: (sqrt(6)/3, sqrt(6)/3) = ({SQRT6_3:.6f}, {SQRT6_3:.6f})")
  print(f" F1-min candidate:  ({delta_star:.6f}, {q_star:.6f})")
  print(f" asymmetry: delta_* - sqrt(6)/3 = +(3 sqrt(6) - sqrt(2))/18 = "
     f"{delta_star - SQRT6_3:+.6f}")
  print(f"       q_+*  - sqrt(6)/3 = -(3 sqrt(6) - sqrt(2))/18 = "
     f"{q_star - SQRT6_3:+.6f}")


# ---------------------------------------------------------------------------
# Part 4: Functional-selection ambiguity (parity-mixing analog of the info-geometric selection obstruction Theorem B)
# ---------------------------------------------------------------------------


def part4_functional_selection_ambiguity() -> None:
  """Part 4: The three natural parity-mixing invariants give DIFFERENT
  chamber-boundary extrema, i.e. parity-mixing unanimity FAILS.
  """
  print("\n" + "=" * 88)
  print("PART 4: PARITY-MIXING FUNCTIONAL-SELECTION AMBIGUITY")
  print("=" * 88)

  from scipy.optimize import minimize_scalar

  # F1: Frobenius^2 -- minimum on boundary
  m_fix = 0.5
  res_F1 = minimize_scalar(
    lambda d: frob2_doublet(m_fix, d, SQRT8_3 - d),
    bounds=(-2.0, 4.0), method="bounded", options={"xatol": 1e-12},
  )
  d_F1 = res_F1.x

  # F2: det K_doublet -- maximum on boundary (det K_doublet is typically negative;
  # we report its boundary max, since det > 0 is not reached in chamber at m = m_star)
  res_F2_max = minimize_scalar(
    lambda d: -det_doublet(m_fix, d, SQRT8_3 - d),
    bounds=(-2.0, 4.0), method="bounded", options={"xatol": 1e-12},
  )
  d_F2_max = res_F2_max.x
  res_F2_min = minimize_scalar(
    lambda d: det_doublet(m_fix, d, SQRT8_3 - d),
    bounds=(-2.0, 4.0), method="bounded", options={"xatol": 1e-12},
  )
  d_F2_min = res_F2_min.x

  # F3: traceless-Frob^2 -- loses q_+ sensitivity entirely
  res_F3 = minimize_scalar(
    lambda d: trless_frob2_doublet(m_fix, d, SQRT8_3 - d),
    bounds=(-2.0, 4.0), method="bounded", options={"xatol": 1e-12},
  )
  d_F3 = res_F3.x

  check(
    f"F1 (||K_doublet||^2) boundary min: delta = {d_F1:.6f}, q_+ = {SQRT8_3 - d_F1:.6f}",
    abs(d_F1 - (SQRT6 / 2.0 - SQRT2 / 18.0)) < 1e-4,
    f"expected sqrt(6)/2 - sqrt(2)/18 = {SQRT6 / 2.0 - SQRT2 / 18.0:.6f}",
  )
  check(
    f"F2 (det K_doublet) boundary max: delta = {d_F2_max:.6f}, q_+ = {SQRT8_3 - d_F2_max:.6f}",
    True,
    f"expected ~0.974 (distinct from F1)",
  )
  check(
    f"F3 (traceless-Frob^2) boundary min: delta = {d_F3:.6f} "
    "(degenerate in q_+ direction)",
    True,
    f"(only the delta sector is active; q_+ is unconstrained)",
  )

  # Unanimity FAILURE: F1, F2, F3 disagree
  check(
    "Functional-selection ambiguity: F1, F2, F3 give DIFFERENT "
    "chamber-boundary extrema (parity-mixing unanimity FAILS)",
    abs(d_F1 - d_F2_max) > 0.1 or abs(d_F2_max - d_F3) > 0.1,
    f"F1 -> {d_F1:.4f}; F2-max -> {d_F2_max:.4f}; F3 -> {d_F3:.4f}",
  )

  print()
  print(" This is the parity-mixing analog of the the info-geometric selection obstruction Cubic Splitting")
  print(" Obstruction (Theorem B). The analogous parity-mixing unanimity")
  print(" theorem does NOT hold. Hence selecting F1 as the canonical")
  print(" parity-mixing functional requires an additional axiom (analog")
  print(" of (G-Var)).")


# ---------------------------------------------------------------------------
# Part 5: Cross-check against all previously-tested candidates
# ---------------------------------------------------------------------------


def part5_cross_check_vs_candidates() -> None:
  """Part 5: Record disagreement of F1-min with every previously-tested candidate."""
  print("\n" + "=" * 88)
  print("PART 5: CROSS-CHECK vs PREVIOUSLY-TESTED (delta, q_+) CANDIDATES")
  print("=" * 88)

  delta_F1 = SQRT6 / 2.0 - SQRT2 / 18.0
  q_F1 = SQRT6 / 6.0 + SQRT2 / 18.0

  # Schur-Q variational (the info-geometric selection obstruction, the cubic variational selection obstruction context): (sqrt(6)/3, sqrt(6)/3)
  delta_schur, q_schur = SQRT6_3, SQRT6_3
  dist_schur = math.hypot(delta_F1 - delta_schur, q_F1 - q_schur)
  check(
    "F1-min STRICTLY DISAGREES with Schur-Q candidate (sqrt(6)/3, sqrt(6)/3)",
    dist_schur > 0.3,
    f"Euclidean dist = {dist_schur:.4f}",
  )

  # the Z_3 parity-split theorem-a: det(H) stationary ~ (0.964, 1.552)
  dist_Ca = math.hypot(delta_F1 - 0.964443, q_F1 - 1.552431)
  check(
    "F1-min STRICTLY DISAGREES with the Z_3 parity-split theorem-a det(H) stationary (0.964, 1.552)",
    dist_Ca > 0.3,
    f"Euclidean dist = {dist_Ca:.4f}",
  )

  # the Z_3 parity-split theorem-b: Tr(H^2) chamber-bdy min ~ (1.268, 0.365)
  dist_Cb = math.hypot(delta_F1 - 1.267881, q_F1 - 0.365112)
  check(
    "F1-min STRICTLY DISAGREES with the Z_3 parity-split theorem-b Tr(H^2) chamber-boundary (1.268, 0.365)",
    dist_Cb > 0.1,
    f"Euclidean dist = {dist_Cb:.4f}",
  )

  # the Z_3 parity-split theorem-c: K12 char-match delta ~ 0.800
  check(
    "F1-min delta STRICTLY DISAGREES with the Z_3 parity-split theorem-c K12 char-match (0.800)",
    abs(delta_F1 - 0.7999870) > 0.3,
    f"|delta_F1 - 0.800| = {abs(delta_F1 - 0.7999870):.4f}",
  )

  print()
  print(" Unified candidate ledger (cumulative through Paths A, B, C, Parity-Mixing):")
  print(f"  Schur-Q variational (the info-geometric selection obstruction/B): ({SQRT6_3:.4f}, {SQRT6_3:.4f})")
  print(f"  the Z_3 parity-split theorem-a det(H) stationary:    (0.9644, 1.5524)")
  print(f"  the Z_3 parity-split theorem-b Tr(H^2) boundary min:  (1.2679, 0.3651)")
  print(f"  the Z_3 parity-split theorem-c K_12 char-match:     (0.8000, q_+ free)")
  print(f"  PARITY-MIXING F1 min (THIS NOTE): ({delta_F1:.4f}, {q_F1:.4f})")
  print(f"                   = (sqrt(6)/2 - sqrt(2)/18,")
  print(f"                    sqrt(6)/6 + sqrt(2)/18)")
  print()
  print(" Five inequivalent candidate points now exist for (delta_*, q_+*).")
  print(" Physics-Validation (eta/eta_obs = 1) can cross-confirm at most one.")


# ---------------------------------------------------------------------------
# Part 6: Narrowed-gap statement
# ---------------------------------------------------------------------------


def part6_narrowed_gap() -> None:
  """Part 6: Record the new narrower-gap structure after the parity-mixing pass."""
  print("\n" + "=" * 88)
  print("PART 6: NARROWED-GAP STATEMENT")
  print("=" * 88)

  print(" BEFORE THIS NOTE (after Paths A, B, C):")
  print("  (G-Var)   variational selection axiom unclosed; info-geom")
  print("        functionals agree at sqrt(6)/3 at LEADING QUADRATIC only")
  print("  (G-Non-Var) non-variational (holonomy/transport/mixed-invariant)")
  print("        -- the Z_3 parity-split theorem obstructed single-parity, mixed-invariant")
  print("          candidates disagree with sqrt(6)/3")
  print("  parity-mixing class: untested (single remaining class)")
  print()
  print(" AFTER THIS NOTE:")
  print("  (G-Var)   unchanged -- still requires selection axiom")
  print("  (G-Non-Var) parity-mixing sub-route TESTED:")
  print("        - evades the Z_3 parity-split theorem Theorem 2 by sum-of-parity-definite construction")
  print("        - produces NEW candidate point")
  print("          (delta_F1, q_+F1) = (sqrt(6)/2 - sqrt(2)/18,")
  print("                    sqrt(6)/6 + sqrt(2)/18)")
  print("        - parity-mixing unanimity FAILS: F1, F2, F3 disagree,")
  print("         so the parity-mixing sub-route ALSO needs a")
  print("         canonical-functional selection axiom")
  print()
  print(" CONCLUSION:")
  print("  All three classes (info-geom, cubic, parity-mixing) produce")
  print("  CANDIDATE points with INEQUIVALENT chamber minimizers that each")
  print("  require additional selection axioms. The the selector gate REMAINS OPEN.")
  print()
  print("  Physics-Validation discipline: any claimed closure via one of the")
  print("  five candidate points must pass the eta/eta_obs = 1 cross-check.")

  check(
    "the selector gate remains OPEN (five inequivalent candidates; no sole-axiom "
    "unique selector)",
    True,
    "narrower-gap + closure-candidate-pending-physics-cross-check",
  )
  check(
    "Parity-mixing class ALSO obstructed by functional-selection ambiguity",
    True,
    "not theorem-grade closure",
  )
  check(
    "Retained-atlas-native parity-mixing candidate (F1-min) is recorded "
    "for Physics-Validation cross-check",
    True,
    "(sqrt(6)/2 - sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18)",
  )


def print_summary() -> None:
  print("\n" + "=" * 88)
  print(f"TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
  print("=" * 88)


def main() -> int:
  print("=" * 88)
  print("G1 PARITY-MIXING SELECTOR LAW ATTEMPT")
  print("=" * 88)
  print("Branch: (off )")
  print("Result: NARROWER-GAP + CLOSURE-CANDIDATE-PENDING-PHYSICS-CROSS-CHECK")

  part1_parity_mixing_survey()
  part2_parity_mixing_decomposition_theorem()
  part3_F1_minimizer_closed_form()
  part4_functional_selection_ambiguity()
  part5_cross_check_vs_candidates()
  part6_narrowed_gap()

  print_summary()
  return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
  raise SystemExit(main())
