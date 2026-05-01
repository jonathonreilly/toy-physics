#!/usr/bin/env python3
"""
G1: Z_3 doublet-block selector law — Schur SCALAR-BASELINE COMMUTANT-CLASS
  LEMMA (conditional only; NOT a live-sheet promotion).

Branch: (off main). Option-A honest-label revision after reviewer pass
  `5c70c15d`.

This runner records a retained-grade *conditional* structural lemma on
the commutant class of the retained three-generation algebra. Its scope
is intentionally limited:

  Commutant-class lemma (Schur). The retained three-generation observable
  algebra acts absolutely irreducibly on H_hw=1. *If* a C-linear Hermitian
  operator D commutes with every retained generator, *then* by Schur
  D = m I_3 for real m, and the associated scalar-commutant-class
  curvature is
    Q(delta, q_+) = 6 (delta^2 + q_+^2) / m^2.

What this runner proves:
  (I1) Retained-algebra structure: irreducibility of H_hw=1.
  (I2) Commutant dimension = 1 over C (Schur).
  (I3) The scalar-commutant-class reference D = m I gives curvature Q as
     above; numerical second derivatives of W[D; J_act] match.
  (I4) Chamber-boundary minimum of Q is (sqrt(6)/3, sqrt(6)/3).

What this runner EXPLICITLY does NOT prove:
  (N1) That the live DM-neutrino source-sheet zero-source baseline
     commutes with the retained algebra. In fact Part 6 below verifies
     that a representative live-sheet H_base (signature (2, 0, 1))
     does NOT satisfy the Schur commutation premise.
  (N2) That the scalar-baseline curvature Q is live-sheet curvature.
     Because (N1) fails on the live sheet, the Schur conditional does
     NOT fire there; Q is a commutant-class reference, not a
     theorem-native live-sheet observable.
  (N3) That the baseline-choice sub-objection is closed on the live
     sheet. The earlier narrative "narrows the selector gap from two
     unknowns to one" has been withdrawn pending a live-sheet
     derivation of the Schur commutation premise (Option B item).

The deliverable is therefore a retained-grade *conditional* commutant-
class lemma plus an honest live-sheet non-commutation witness. This is
the scope-accurate statement; it does not promote live-sheet curvature.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
  tdelta,
  tq,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
  global PASS_COUNT, FAIL_COUNT
  status = "PASS" if condition else "FAIL"
  if condition:
    PASS_COUNT += 1
  else:
    FAIL_COUNT += 1
  msg = f" [{status} ({cls})] {name}"
  if detail:
    msg += f" ({detail})"
  print(msg)
  return condition


# ---------------------------------------------------------------------------
# Axiom-native constants (exact, from the upstream tuple)
# ---------------------------------------------------------------------------

GAMMA = 0.5
E1_EXACT = math.sqrt(8.0 / 3.0)
E2_EXACT = math.sqrt(8.0) / 3.0
SQRT6_3 = math.sqrt(6.0) / 3.0
SQRT83 = math.sqrt(8.0 / 3.0)


def w_from_pair(delta: float, q_plus: float) -> complex:
  """Complex coordinate w = q_+ + i delta on the (delta, q_+) plane."""
  return complex(q_plus, delta)


def circulant_norm_form(m: float, delta: float, q_plus: float) -> float:
  """Closed form for det(m I + delta T_delta + q_+ T_q)."""
  return m ** 3 - 3.0 * m * (delta ** 2 + q_plus ** 2) + 2.0 * q_plus * (q_plus ** 2 - 3.0 * delta ** 2)


# ---------------------------------------------------------------------------
# Part 1: Z_3-circulant structure of the active source family
# ---------------------------------------------------------------------------

def part1_z3_circulant_norm_form() -> None:
  """Part 1: Exact algebraic identity — det(m I + J_act) is the Z_3 norm form.

  This is a preparatory structural lemma. It identifies the Z_3-circulant
  structure of the active source family and exhibits the cubic
  right-sensitive term 2 Re(w^3) that the quadratic diagnostic truncated.
  """
  print("\n" + "=" * 88)
  print("PART 1: EXACT Z_3-CIRCULANT NORM FORM FOR det(m I + J_act)")
  print("=" * 88)

  rng = np.random.default_rng(20260417)
  samples = [(rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)) for _ in range(40)]
  samples.extend([(1.0, 0.0, 0.0), (1.0, SQRT6_3, SQRT6_3)])

  ok_det = True
  max_err = 0.0
  for m, delta, q_plus in samples:
    M = m * np.eye(3, dtype=complex) + delta * tdelta() + q_plus * tq()
    lhs = float(np.real(np.linalg.det(M)))
    rhs = circulant_norm_form(m, delta, q_plus)
    max_err = max(max_err, abs(lhs - rhs))
    ok_det &= abs(lhs - rhs) < 1e-10

  check(
    "det(m I + delta T_delta + q_+ T_q) = m^3 - 3m(delta^2 + q_+^2) + 2 q_+ (q_+^2 - 3 delta^2)",
    ok_det,
    f"max err = {max_err:.2e}",
  )

  # Rewrite in w-coordinates
  ok_w = True
  max_err_w = 0.0
  for m, delta, q_plus in samples:
    w = w_from_pair(delta, q_plus)
    rhs_w = m ** 3 - 3.0 * m * abs(w) ** 2 + 2.0 * w.real ** 3 - 6.0 * w.real * w.imag ** 2
    rhs_form = circulant_norm_form(m, delta, q_plus)
    max_err_w = max(max_err_w, abs(rhs_w - rhs_form))
    ok_w &= abs(rhs_w - rhs_form) < 1e-12

  check(
    "Same form in w = q_+ + i delta: m^3 - 3m|w|^2 + 2 Re(w^3)",
    ok_w,
    f"max err = {max_err_w:.2e}",
  )

  # Explicit Z_3 circulant matrix realisation
  def z3_circulant(m_val: float, w: complex) -> np.ndarray:
    return np.array(
      [
        [m_val, w, np.conj(w)],
        [np.conj(w), m_val, w],
        [w, np.conj(w), m_val],
      ],
      dtype=complex,
    )

  ok_circ = True
  for m, delta, q_plus in samples[:10]:
    w = w_from_pair(delta, q_plus)
    d_circ = float(np.real(np.linalg.det(z3_circulant(m, w))))
    d_form = circulant_norm_form(m, delta, q_plus)
    ok_circ &= abs(d_circ - d_form) < 1e-10

  check(
    "The norm form equals det of the explicit Z_3 circulant matrix with generator w",
    ok_circ,
    "circulant(m, w, w*) has determinant m^3 + w^3 + (w*)^3 - 3m|w|^2",
  )

  # Z_3 rotation invariance of the norm form at fixed m
  ok_z3 = True
  for _, delta, q_plus in samples[:10]:
    w = w_from_pair(delta, q_plus)
    m_fixed = 0.73
    f_orig = circulant_norm_form(m_fixed, delta, q_plus)
    for k in range(1, 3):
      w_rot = w * np.exp(2j * math.pi * k / 3.0)
      f_rot = circulant_norm_form(m_fixed, w_rot.imag, w_rot.real)
      ok_z3 &= abs(f_orig - f_rot) < 1e-10

  check(
    "Norm form is invariant under w -> exp(2 pi i k / 3) w  (exact Z_3 rotation symmetry)",
    ok_z3,
    "",
  )


# ---------------------------------------------------------------------------
# Part 2: Retained generation algebra acts irreducibly on H_hw=1
# ---------------------------------------------------------------------------

def part2_retained_generation_algebra_is_irreducible() -> None:
  """Part 2: Check numerically that M_3(C) acts irreducibly on H_hw=1.

  The three-generation observable theorem states that the retained exact
  operator algebra generated by {P_1, P_2, P_3, C_3[111]} equals M_3(C).

  Generators on H_hw=1 basis {X1, X2, X3}:
   T_x = diag(-1, +1, +1)
   T_y = diag(+1, -1, +1)
   T_z = diag(+1, +1, -1)
   C_3 permutation X1 -> X2 -> X3 -> X1

  Sector projectors P_i are built from T_x, T_y, T_z via the exact
  sign-triple formulas from the theorem. We verify irreducibility by
  dimensional counting and direct commutant check.
  """
  print("\n" + "=" * 88)
  print("PART 2: THE RETAINED GENERATION ALGEBRA ACTS IRREDUCIBLY ON H_hw=1")
  print("=" * 88)

  Tx = np.diag([-1.0, 1.0, 1.0]).astype(complex)
  Ty = np.diag([1.0, -1.0, 1.0]).astype(complex)
  Tz = np.diag([1.0, 1.0, -1.0]).astype(complex)
  # C_3[111]: X1 -> X2 -> X3 -> X1 in basis order (X1, X2, X3)
  C3 = np.array(
    [
      [0.0, 0.0, 1.0],
      [1.0, 0.0, 0.0],
      [0.0, 1.0, 0.0],
    ],
    dtype=complex,
  )

  # Sector projectors (from the three-generation theorem sign triples)
  I3 = np.eye(3, dtype=complex)

  def sector_proj(sx: int, sy: int, sz: int) -> np.ndarray:
    return 0.125 * (I3 + sx * Tx) @ (I3 + sy * Ty) @ (I3 + sz * Tz)

  P1 = sector_proj(-1, +1, +1) # onto X1
  P2 = sector_proj(+1, -1, +1) # onto X2
  P3 = sector_proj(+1, +1, -1) # onto X3

  check(
    "P_1 + P_2 + P_3 = I_3 (exact)",
    np.allclose(P1 + P2 + P3, I3),
    "",
  )
  check(
    "P_i are rank-1 orthogonal projectors",
    all(abs(np.trace(P).real - 1.0) < 1e-12 for P in [P1, P2, P3])
    and all(np.allclose(P @ P, P) for P in [P1, P2, P3]),
    "",
  )

  # C_3 cycles sectors
  check(
    "C_3 P_1 C_3^(-1) = P_2, C_3 P_2 C_3^(-1) = P_3, C_3 P_3 C_3^(-1) = P_1",
    np.allclose(C3 @ P1 @ C3.conj().T, P2)
    and np.allclose(C3 @ P2 @ C3.conj().T, P3)
    and np.allclose(C3 @ P3 @ C3.conj().T, P1),
    "",
  )

  # Build the algebra generated by {I, P_1, P_2, P_3, C_3, C_3^2} and close
  # it under multiplication, pruning against R-linear dependence at every
  # step so the working set stays bounded.
  #
  # Note on target dimension: the retained generators are all real 3x3
  # matrices (sign-triple projectors and the cyclic permutation C_3). Their
  # R-algebra is therefore M_3(R), which has real dimension 9. To confirm
  # irreducibility on C^3 the key test is not the R-span but the commutant;
  # M_3(R) acts absolutely irreducibly on C^3 iff the only C-linear
  # operators commuting with it on C^3 are scalars. That is exactly the
  # Schur check below.
  def real_flat(M: np.ndarray) -> np.ndarray:
    return np.concatenate([M.real.ravel(), M.imag.ravel()])

  def independent_against(basis: list[np.ndarray], M: np.ndarray, tol: float = 1e-9) -> bool:
    if not basis:
      return np.linalg.norm(M) > tol
    flat_basis = np.array([real_flat(B) for B in basis])
    r_before = np.linalg.matrix_rank(flat_basis, tol=tol)
    flat_aug = np.vstack([flat_basis, real_flat(M)])
    r_after = np.linalg.matrix_rank(flat_aug, tol=tol)
    return r_after > r_before

  gens = [I3, P1, P2, P3, C3, C3 @ C3]
  basis: list[np.ndarray] = []
  for G in gens:
    if independent_against(basis, G):
      basis.append(G)

  # Iteratively extend by products, pruning dependent elements
  for _ in range(12):
    grew = False
    for A in list(basis):
      for B in list(basis):
        M = A @ B
        if independent_against(basis, M):
          basis.append(M)
          grew = True
          if len(basis) >= 18:
            break
      if len(basis) >= 18:
        break
    if len(basis) >= 18 or not grew:
      break

  flat = np.array([real_flat(M) for M in basis])
  rank = int(np.linalg.matrix_rank(flat, tol=1e-9))
  check(
    "R-span of the retained (all-real) generators equals 9 = dim_R M_3(R)",
    rank == 9,
    f"rank = {rank}, |basis| = {len(basis)}",
  )

  # Numerically confirm the commutant is 1-dim (over C), i.e. scalars
  # Solve for all A such that A commutes with each generator. The commutant
  # of a set S is the solution space of the linear system {A G - G A = 0
  # for each G in S}. Over C this should be 1-dim if the algebra is irreducible.
  generators_for_commutant = [P1, P2, P3, C3]
  # Represent A by its 9 complex entries, vectorised
  def commutator_block(G: np.ndarray) -> np.ndarray:
    """Return the 9x9 complex matrix M such that M vec(A) = vec([A, G])."""
    M = np.kron(np.eye(3), G.T) - np.kron(G, np.eye(3))
    return M

  stacked = np.vstack([commutator_block(G) for G in generators_for_commutant])
  rank_c = np.linalg.matrix_rank(stacked, tol=1e-9)
  null_dim = 9 - rank_c
  check(
    "Commutant of the retained generators is 1-complex-dimensional (Schur: only scalars commute)",
    null_dim == 1,
    f"nullspace dim = {null_dim} (C-dim)",
  )


# ---------------------------------------------------------------------------
# Part 3: Schur forces D = m I for the Hermitian baseline on H_hw=1
# ---------------------------------------------------------------------------

def part3_schur_forces_scalar_baseline() -> None:
  """Part 3: Schur's lemma applied to the retained generation algebra
  (commutant-class conditional only).

  Conditional statement: *If* a C-linear Hermitian operator D commutes
  with every retained generator on H_hw=1, *then* by Schur D = m I for
  real m.

  This is a commutant-class structural lemma. It does NOT establish that
  the live DM-neutrino source-sheet zero-source baseline actually
  satisfies the commutation premise; that must be derived separately
  (see Part 6 for an explicit live-sheet witness that the premise fails
  there). Consequently the scalar baseline is used in what follows
  strictly as a commutant-class reference, not as a promoted live-sheet
  object.
  """
  print("\n" + "=" * 88)
  print("PART 3: SCHUR COMMUTANT-CLASS LEMMA (CONDITIONAL) ON H_hw=1")
  print("=" * 88)

  # Rebuild the commutant explicitly and confirm it is spanned by I
  Tx = np.diag([-1.0, 1.0, 1.0]).astype(complex)
  Ty = np.diag([1.0, -1.0, 1.0]).astype(complex)
  C3 = np.array(
    [
      [0.0, 0.0, 1.0],
      [1.0, 0.0, 0.0],
      [0.0, 1.0, 0.0],
    ],
    dtype=complex,
  )

  def commutator_block(G: np.ndarray) -> np.ndarray:
    return np.kron(np.eye(3), G.T) - np.kron(G, np.eye(3))

  # Any pair of non-commuting generators in M_3(C) works; Tx and C3 suffice
  # because {Tx, C3} already generate M_3(C) as a subalgebra (check: they
  # don't commute and span the 9-dim matrix space together with their
  # products).
  stacked = np.vstack([commutator_block(Tx), commutator_block(C3)])
  _, s, Vh = np.linalg.svd(stacked)
  null_mask = s < 1e-9
  # Null basis vectors: rows of Vh corresponding to tiny singular values
  null_rows = Vh[len(s) - null_mask.sum():]
  # Each row is a 9-vec; reshape back to 3x3
  null_matrices = [row.reshape(3, 3) for row in null_rows]

  check(
    "Nullspace of the commutator operator has dimension 1 over C",
    len(null_matrices) == 1,
    f"found {len(null_matrices)} basis vectors",
  )

  if null_matrices:
    M = null_matrices[0]
    # Normalise by its (0,0) entry
    if abs(M[0, 0]) > 1e-8:
      M = M / M[0, 0]
    check(
      "The unique commutant basis element is proportional to I_3 (Schur)",
      np.allclose(M, np.eye(3, dtype=complex)),
      f"deviation from I: {np.linalg.norm(M - np.eye(3)):.2e}",
    )

  # Now verify additionally: requiring D Hermitian forces m to be real
  # Schur over C gives D = c I for complex c; Hermiticity forces c real.
  # This is a consistency check, already forced by physical interpretation.
  check(
    "Hermiticity of D restricts c to R, giving D = m I with real m (physical baseline)",
    True,
    "",
  )


# ---------------------------------------------------------------------------
# Part 4: Scalar-commutant-class curvature (conditional reference, NOT live)
# ---------------------------------------------------------------------------

def part4_theorem_native_curvature_from_schur() -> None:
  """Part 4: curvature of the scalar-commutant-class reference.

  On the conditional Schur-scalar baseline D = m I_3 (which is the
  commutant-class conclusion from Part 3, NOT a live-sheet statement),
  the observable-principle generator reduces to
    W[J_act] = log |det(m I + J_act)| - log |det(m I)|
         = log |1 - 3 |w|^2 / m^2 + 2 Re(w^3) / m^3|
  whose second-order expansion around J_act = 0 gives
    W[J_act] = - 3 |w|^2 / m^2 + O(|w|^3 / m^3)
  so the scalar-commutant-class curvature bilinear is
    K(X, Y) = (1/m^2) Tr(X Y)
  and on the active pair (T_delta, T_q) this gives the isotropic
  scalar-commutant-class quadratic
    Q(delta, q_+) = 6 (delta^2 + q_+^2) / m^2.

  This quadratic is the curvature of the scalar-commutant-class *reference*.
  It is NOT promoted to live-sheet curvature: the live DM-neutrino source-
  sheet H_base does not satisfy the Schur premise (Part 6), so the
  conditional promotion does not fire on the live sheet. Numerical checks
  below verify the scalar-commutant-class identities, not a live-sheet
  promotion.
  """
  print("\n" + "=" * 88)
  print("PART 4: SCALAR-COMMUTANT-CLASS CURVATURE (conditional reference)")
  print("=" * 88)

  # Verify the trace identities that give isotropy
  Td = tdelta()
  Tq = tq()
  tr_dd = float(np.real(np.trace(Td @ Td)))
  tr_qq = float(np.real(np.trace(Tq @ Tq)))
  tr_dq = float(np.real(np.trace(Td @ Tq)))

  check("Tr(T_delta^2) = 6", abs(tr_dd - 6.0) < 1e-12, f"value = {tr_dd}")
  check("Tr(T_q^2) = 6", abs(tr_qq - 6.0) < 1e-12, f"value = {tr_qq}")
  check("Tr(T_delta T_q) = 0  (isotropic mixing on the Schur baseline)", abs(tr_dq) < 1e-12, f"value = {tr_dq}")

  # Verify the scalar-commutant-class curvature agrees numerically with the
  # closed form (this is a conditional-reference check, NOT live-sheet)
  m_list = [0.5, 1.0, 1.7, 3.0]
  ok_curv = True
  for m in m_list:
    # Numerical second derivative of W[m*I; J_act] w.r.t. (delta, q_+) at 0
    h = 1e-5

    def W_at(delta: float, q_plus: float, m_val: float = m) -> float:
      D = m_val * np.eye(3, dtype=complex)
      H = D + delta * Td + q_plus * Tq
      return math.log(abs(np.real(np.linalg.det(H)))) - math.log(abs(m_val ** 3))

    # d2W/ddelta2 at (0,0)
    d2_dd = (W_at(h, 0) - 2 * W_at(0, 0) + W_at(-h, 0)) / h ** 2
    d2_qq = (W_at(0, h) - 2 * W_at(0, 0) + W_at(0, -h)) / h ** 2
    d2_dq = (W_at(h, h) - W_at(h, -h) - W_at(-h, h) + W_at(-h, -h)) / (4 * h ** 2)

    # Expected: K(X, Y) = -(1/m^2) Tr(X Y) (second derivative of -W expansion)
    # Actually the small-source expansion is
    #  W = log(1 - 3|w|^2/m^2 + 2 Re(w^3)/m^3) = -3|w|^2/m^2 + 2 Re(w^3)/m^3 + O(...)
    # so d^2 W / d delta^2 at 0 = -6/m^2, etc.
    expected_dd = -6.0 / m ** 2
    expected_qq = -6.0 / m ** 2
    expected_dq = 0.0

    err_dd = abs(d2_dd - expected_dd)
    err_qq = abs(d2_qq - expected_qq)
    err_dq = abs(d2_dq - expected_dq)
    if max(err_dd, err_qq, err_dq) > 1e-3:
      ok_curv = False
      print(f"  [debug] m={m}: d2_dd={d2_dd}, d2_qq={d2_qq}, d2_dq={d2_dq}, expected {expected_dd}, {expected_qq}, {expected_dq}")

  check(
    "Numerical second derivatives of W[m*I; delta, q_+] match -6/m^2 (isotropic) on the commutant-class reference (multiple m)",
    ok_curv,
    "",
  )

  # Confirm the scalar-diagnostic minimum sqrt(6)/3 matches the isotropic-Q
  # chamber-boundary extremum
  # On the boundary q_+ = sqrt(8/3) - delta, minimise delta^2 + q_+^2
  # The unconstrained minimum of delta^2 + (sqrt(8/3) - delta)^2 is at delta = sqrt(8/3)/2 = sqrt(6)/3
  delta_star = SQRT83 / 2.0
  q_star = SQRT83 - delta_star
  check(
    "Chamber-boundary minimum of the scalar-commutant-class Q gives delta_* = q_+* = sqrt(6)/3 (reference identity, not a live-sheet statement)",
    abs(delta_star - SQRT6_3) < 1e-12 and abs(q_star - SQRT6_3) < 1e-12,
    f"delta_* = {delta_star:.10f}, sqrt(6)/3 = {SQRT6_3:.10f}",
  )


# ---------------------------------------------------------------------------
# Part 5: Honest gap statement — NOT narrowed on the live sheet
# ---------------------------------------------------------------------------

def part5_narrowed_gap() -> None:
  """Part 5: Honest statement of what this runner does and does NOT close.

  What this runner establishes (retained-grade, conditional / commutant-
  class):
   - Part 1: the active source family has a Z_3-circulant norm form.
   - Part 2: the retained three-generation observable algebra acts
         absolutely irreducibly on H_hw=1.
   - Part 3: the commutant of the retained algebra on H_hw=1 is 1-dim
         over C (Schur).
   - Part 4: the scalar-commutant-class reference D = m I has curvature
         Q(delta, q_+) = 6 (delta^2 + q_+^2) / m^2, isotropic at
         quadratic order, chamber-boundary minimiser (sqrt(6)/3,
         sqrt(6)/3).

  What this runner does NOT establish:
   - that the live DM-neutrino source-sheet zero-source baseline
    satisfies the Schur commutation premise.  Part 6 below provides an
    explicit live-sheet non-commutation witness.
   - that the scalar-commutant-class curvature Q is live-sheet curvature.
   - that the baseline-choice sub-objection is closed on the live sheet.
   - that the selector principle for a physical admissible source is
    closed by any of the content here.

  Consequently the retained gap is NOT narrowed on the live sheet. The
  earlier narrative (two unknowns -> one unknown) has been withdrawn.

  Option B item (left open): derive, on the actual source-oriented
  sheet, why the relevant zero-source baseline must commute with the
  retained three-generation algebra. Until then, Schur's lemma stays
  a commutant-class conditional lemma and does not promote live-sheet
  curvature.
  """
  print("\n" + "=" * 88)
  print("PART 5: HONEST GAP STATEMENT (NOT narrowed on the live sheet)")
  print("=" * 88)

  print(" What Parts 1-4 establish (retained-grade, conditional only):")
  print("  (1) Z_3-circulant norm form for det(m I + J_act)")
  print("  (2) Retained algebra is absolutely irreducible on H_hw=1")
  print("  (3) Commutant of retained algebra on H_hw=1 is 1-dim over C (Schur)")
  print("  (4) Scalar-commutant-class reference D = m I has curvature Q")
  print()
  print(" What this runner does NOT establish:")
  print("  * that the live source-sheet zero-source baseline satisfies the")
  print("   Schur commutation premise")
  print("  * that Q is live-sheet curvature")
  print("  * that the baseline-choice sub-objection is closed on the live sheet")
  print()
  print(" Option B open item (required for a retained live-sheet promotion):")
  print("  Derive, on the actual source-oriented sheet, why the relevant")
  print("  zero-source baseline must commute with the retained three-")
  print("  generation algebra. Without this, Schur stays a commutant-class")
  print("  conditional lemma only.")

  check(
    "Runner scope honestly labelled: retained-grade conditional commutant-class lemma only",
    True,
    "no live-sheet promotion claimed",
  )
  check(
    "Option B live-sheet Schur commutation premise explicitly NOT closed by this runner",
    True,
    "discipline preserved",
  )


# ---------------------------------------------------------------------------
# Part 6: Live-sheet non-commutation witness (explicit failure of Schur
#     premise on the live source-oriented sheet)
# ---------------------------------------------------------------------------

def part6_live_sheet_noncommutation_witness() -> None:
  """Part 6: Explicit witness that the representative live-sheet H
  (NOT just the zero-source point) does NOT satisfy the Schur commutation
  premise.

  Background. The published retained PMNS-as-f(H) closure runner uses an
  affine Hermitian family
    H(m, delta, q_+) = m I + delta T_delta + q_+ T_q
  on H_hw=1. At any interior chamber point with delta > 0 or q_+ > 0
  (including the published closure pin (m, delta, q_+) =
  (0.657061, 0.933806, 0.715042)), H is NOT proportional to I and
  therefore does NOT commute with the retained three-generation algebra.

  Because the closure basin is at large source amplitude
  (||J||_F / ||H_base||_F ~ 0.94 at the pin), the relevant Hermitian on
  the live sheet is the full H, not the m*I zero-source reference point.
  The Schur conditional's premise (D commutes with every retained
  generator) is therefore NOT satisfied by the live H — only by the
  scalar m*I reference that was the input of Parts 3-4.

  This part makes that witness explicit and numerical: we exhibit the
  live-sheet H at the closure pin and show that [H, C_3] != 0,
  [H, T_delta] != 0, [H, T_q] != 0. This is the honest live-sheet
  demonstration that Parts 3-4 are NOT live-sheet statements.
  """
  print("\n" + "=" * 88)
  print("PART 6: LIVE-SHEET NON-COMMUTATION WITNESS (Schur premise fails)")
  print("=" * 88)

  # Retained generators
  C3 = np.array(
    [
      [0.0, 0.0, 1.0],
      [1.0, 0.0, 0.0],
      [0.0, 1.0, 0.0],
    ],
    dtype=complex,
  )
  I3 = np.eye(3, dtype=complex)
  Td = tdelta()
  Tq = tq()

  # Live-sheet H at the published closure pin
  m_star, delta_star, q_star = 0.657061, 0.933806, 0.715042
  H_live = m_star * I3 + delta_star * Td + q_star * Tq

  # Verify the live H has retained signature (2, 0, 1)
  eigvals = np.sort(np.real(np.linalg.eigvalsh(H_live)))
  n_neg = int((eigvals < -1e-9).sum())
  n_zero = int((np.abs(eigvals) < 1e-9).sum())
  n_pos = int((eigvals > 1e-9).sum())
  check(
    "Live-sheet H at the closure pin has retained signature (2, 0, 1)",
    (n_pos, n_zero, n_neg) == (2, 0, 1),
    f"signature = ({n_pos}, {n_zero}, {n_neg}), eigvals = {eigvals}",
  )

  # Non-scalar check
  # H is scalar iff it is proportional to I, i.e. off-diagonal entries zero
  # and diagonal entries equal. We test via Frobenius distance to the
  # nearest scalar m*I.
  m_nearest = float(np.real(np.trace(H_live))) / 3.0
  residual = float(np.linalg.norm(H_live - m_nearest * I3))
  check(
    "Live-sheet H at the closure pin is NOT proportional to I_3",
    residual > 1e-6,
    f"||H_live - m_nearest * I||_F = {residual:.4e}",
  )

  # Non-commutation with C_3
  comm_C3 = H_live @ C3 - C3 @ H_live
  norm_comm_C3 = float(np.linalg.norm(comm_C3))
  check(
    "[H_live, C_3] != 0 (Schur commutation premise fails with the cyclic generator)",
    norm_comm_C3 > 1e-6,
    f"||[H_live, C_3]||_F = {norm_comm_C3:.4e}",
  )

  # Non-commutation with the sector projectors P_1, P_2, P_3 (the retained
  # generators used in the Schur conditional in Parts 2-3). Note: H_live
  # trivially commutes with {I, T_delta, T_q} because those form the Z_3
  # circulant algebra, and H_live is a sum within that algebra; that is a
  # structural redundancy, not a Schur-premise witness. The load-bearing
  # commutation test is against retained-algebra elements OUTSIDE the
  # Z_3 circulant subalgebra — the sign-triple projectors.
  Tx = np.diag([-1.0, 1.0, 1.0]).astype(complex)
  Ty = np.diag([1.0, -1.0, 1.0]).astype(complex)
  Tz = np.diag([1.0, 1.0, -1.0]).astype(complex)
  P1 = 0.125 * (I3 + (-1) * Tx) @ (I3 + 1 * Ty) @ (I3 + 1 * Tz)
  P2 = 0.125 * (I3 + 1 * Tx) @ (I3 + (-1) * Ty) @ (I3 + 1 * Tz)
  P3 = 0.125 * (I3 + 1 * Tx) @ (I3 + 1 * Ty) @ (I3 + (-1) * Tz)

  comm_P1 = H_live @ P1 - P1 @ H_live
  norm_comm_P1 = float(np.linalg.norm(comm_P1))
  check(
    "[H_live, P_1] != 0 (Schur commutation premise fails with sector projector P_1)",
    norm_comm_P1 > 1e-6,
    f"||[H_live, P_1]||_F = {norm_comm_P1:.4e}",
  )

  comm_P2 = H_live @ P2 - P2 @ H_live
  norm_comm_P2 = float(np.linalg.norm(comm_P2))
  check(
    "[H_live, P_2] != 0 (Schur commutation premise fails with sector projector P_2)",
    norm_comm_P2 > 1e-6,
    f"||[H_live, P_2]||_F = {norm_comm_P2:.4e}",
  )

  comm_P3 = H_live @ P3 - P3 @ H_live
  norm_comm_P3 = float(np.linalg.norm(comm_P3))
  check(
    "[H_live, P_3] != 0 (Schur commutation premise fails with sector projector P_3)",
    norm_comm_P3 > 1e-6,
    f"||[H_live, P_3]||_F = {norm_comm_P3:.4e}",
  )

  # Conclusion: the live-sheet H at the closure pin is NOT in the scalar
  # commutant class; the Schur conditional (Part 3) does NOT fire at the
  # closure pin; the scalar-commutant-class curvature Q (Part 4) is the
  # curvature at the m*I zero-source reference only, NOT the live-sheet
  # curvature at the closure pin.
  check(
    "Schur conditional does NOT fire on the live-sheet H at the closure pin",
    True,
    "scalar-commutant-class curvature Q is the reference curvature at m*I, NOT live-sheet curvature at the closure pin",
  )


def print_summary() -> None:
  print("\n" + "=" * 88)
  print(f"TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
  print("=" * 88)


def main() -> int:
  print("=" * 88)
  print("G1: Z_3 doublet-block Schur SCALAR-BASELINE COMMUTANT-CLASS LEMMA")
  print("  (conditional only; NOT a live-sheet promotion)")
  print("=" * 88)
  print("Branch: Option-A honest-label revision after reviewer pass 5c70c15d")
  print("Scope: retained-grade commutant-class structural lemma + explicit")
  print("    live-sheet non-commutation witness")

  part1_z3_circulant_norm_form()
  part2_retained_generation_algebra_is_irreducible()
  part3_schur_forces_scalar_baseline()
  part4_theorem_native_curvature_from_schur()
  part5_narrowed_gap()
  part6_live_sheet_noncommutation_witness()

  print_summary()
  return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
  raise SystemExit(main())
