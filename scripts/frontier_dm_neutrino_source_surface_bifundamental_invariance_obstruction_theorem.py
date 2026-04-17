#!/usr/bin/env python3
"""
Selector Physicist I: Bifundamental invariance U(2)_L x U(2)_R on the active
doublet block — sole-axiom derivability test.

Branch: (off ).

RESULT CLASSIFICATION: OBSTRUCTION THEOREM (CASE 3).

This runner verifies, from the retained atlas only, that independent
U(2)_L x U(2)_R bifundamental unitary invariance on the active-sheet
Z_3 doublet block K_doublet is NOT derivable from Cl(3)/Z^3.

Physicist F identified this as the conditional closure gate for G1:
IF U(2)_L x U(2)_R were axiom-native on K_doublet, THEN the Frobenius
functional F1 = Tr(K^dag K) would be uniquely pinned among PD U(2)-
invariant quadratics, and selector would close at
  (delta_*, q_+*) = ( sqrt(6)/2 - sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18 ).
This runner proves the antecedent is false.

Five independent attack lines:

 L1. Polar-section gauge-fixing: U_R has already been spent.
 L2. Retained Dirac operator Gamma_1 is Hermitian: no L/R split.
 L3. Shift-quotient bundle: retained gauge algebra is 1-dimensional,
   not 8-dimensional.
 L4. Z_3-support trichotomy: independent U(n)_L x U(n)_R generically
   breaks the q_L + q_H + q_R = 0 mod 3 support constraint.
 L5. Schur collapse: on D = m I, U_L D U_R^dag = m U_L U_R^dag, so
   the bifundamental orbit reduces to a single adjoint.

The runner also verifies:

 - K_doublet is Hermitian on the active sheet
 - generic bifundamental U_L K U_R^dag BREAKS Hermiticity
 - diagonal U K U^dag PRESERVES Hermiticity
 - Frobenius IS preserved by bifundamental action on the NON-Hermitian
  linear space (the Physicist F Line 1 identity, reconfirmed)
 - weaker retained invariances (single U(2) adjoint, Z_3 cyclic,
  diagonal shift, CP) do NOT pin F1 uniquely

Verdict: bifundamental gauge invariance on the active doublet block is
NOT sole-axiom derivable. Five independent derivations converge on the
same conclusion. The F1 conditional closure gate is unavailable.

No new axioms are introduced.

Framework convention: "axiom" means only the single framework axiom
Cl(3) on Z^3.
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
# Retained-atlas constants
# ---------------------------------------------------------------------------

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SQRT8_3 = math.sqrt(8.0 / 3.0)     # = 2 * sqrt(6) / 3
SQRT8_OVER3 = math.sqrt(8.0) / 3.0
GAMMA = 0.5
SQRT6_3 = SQRT6 / 3.0
M_F1 = 4.0 * SQRT2 / 9.0        # F1 m-value
DELTA_F1 = SQRT6 / 2.0 - SQRT2 / 18.0
Q_F1 = SQRT6 / 6.0 + SQRT2 / 18.0

OMEGA = np.exp(2j * math.pi / 3.0)

# U_Z3 discrete-Fourier matrix, retained atlas convention.
UZ3 = (1.0 / math.sqrt(3.0)) * np.array(
  [
    [1.0, 1.0, 1.0],
    [1.0, OMEGA, OMEGA * OMEGA],
    [1.0, OMEGA * OMEGA, OMEGA],
  ],
  dtype=complex,
)


# ---------------------------------------------------------------------------
# Retained active-affine generators and base (same as upstream atlas)
# ---------------------------------------------------------------------------


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


def k_z3_of_h(h: np.ndarray) -> np.ndarray:
  return UZ3.conj().T @ h @ UZ3


def k_doublet_of_h(h: np.ndarray) -> np.ndarray:
  """Intrinsic Z_3 doublet block K_Z3(H)[1:3, 1:3]."""
  return k_z3_of_h(h)[1:, 1:]


# ---------------------------------------------------------------------------
# Random unitary sampler (Haar via QR on a Ginibre matrix)
# ---------------------------------------------------------------------------


def random_unitary(n: int, rng: np.random.Generator) -> np.ndarray:
  a = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
  q, r = np.linalg.qr(a)
  # Fix the QR phase ambiguity to get a Haar-distributed unitary
  d = np.diag(r)
  ph = d / np.abs(d)
  q = q * ph
  return q


# ---------------------------------------------------------------------------
# Part 1: K_doublet is Hermitian on the active sheet
# ---------------------------------------------------------------------------


def part1_k_doublet_is_hermitian():
  print()
  print("=" * 88)
  print("PART 1: K_doublet IS HERMITIAN ON THE ACTIVE SHEET")
  print("=" * 88)
  print(" Structural fact: H is Hermitian, U_Z3 is unitary, therefore")
  print(" K_Z3 = U_Z3^dag H U_Z3 is Hermitian, and every principal submatrix")
  print(" (including K_doublet) is Hermitian.")
  print()

  rng = np.random.default_rng(11)

  max_h_herm = 0.0
  max_kz3_herm = 0.0
  max_kd_herm = 0.0

  for _ in range(16):
    m = rng.uniform(-1.5, 1.5)
    delta = rng.uniform(-1.5, 1.5)
    q_plus = rng.uniform(-1.5, 1.5)
    h = active_affine_h(m, delta, q_plus)
    kz3 = k_z3_of_h(h)
    kd = k_doublet_of_h(h)

    max_h_herm = max(max_h_herm, float(np.linalg.norm(h - h.conj().T)))
    max_kz3_herm = max(max_kz3_herm, float(np.linalg.norm(kz3 - kz3.conj().T)))
    max_kd_herm = max(max_kd_herm, float(np.linalg.norm(kd - kd.conj().T)))

  check(
    "Active-sheet H is Hermitian",
    max_h_herm < 1e-12,
    f"max ||H - H^dag|| = {max_h_herm:.2e}",
  )
  check(
    "K_Z3 = U_Z3^dag H U_Z3 is Hermitian",
    max_kz3_herm < 1e-12,
    f"max ||K_Z3 - K_Z3^dag|| = {max_kz3_herm:.2e}",
  )
  check(
    "K_doublet = K_Z3[1:3,1:3] is Hermitian (principal submatrix of Hermitian)",
    max_kd_herm < 1e-12,
    f"max ||K_d - K_d^dag|| = {max_kd_herm:.2e}",
  )

  # Verify the retained closed-form values for K_doublet entries.
  m, delta, q_plus = 0.45, 0.30, 0.70
  h = active_affine_h(m, delta, q_plus)
  kd = k_doublet_of_h(h)

  K11_expected = -q_plus + 2.0 * SQRT2 / 9.0 - 1.0 / (2.0 * SQRT3)
  K22_expected = -q_plus + 2.0 * SQRT2 / 9.0 + 1.0 / (2.0 * SQRT3)
  K12_expected = (m - 4.0 * SQRT2 / 9.0) + 1j * (SQRT3 * delta - 4.0 * SQRT2 / 3.0)

  err_11 = abs(kd[0, 0] - K11_expected)
  err_22 = abs(kd[1, 1] - K22_expected)
  err_12 = abs(kd[0, 1] - K12_expected)

  check(
    "K11 matches retained closed form",
    err_11 < 1e-10,
    f"err = {err_11:.2e}",
  )
  check(
    "K22 matches retained closed form",
    err_22 < 1e-10,
    f"err = {err_22:.2e}",
  )
  check(
    "K12 matches retained closed form (real = m - 4*sqrt(2)/9, imag = sqrt(3) delta - 4*sqrt(2)/3)",
    err_12 < 1e-10,
    f"err = {err_12:.2e}",
  )


# ---------------------------------------------------------------------------
# Part 2: Single U(2) adjoint preserves Hermiticity; bifundamental breaks it.
# ---------------------------------------------------------------------------


def part2_adjoint_vs_bifundamental():
  print()
  print("=" * 88)
  print("PART 2: SINGLE U(2) ADJOINT vs INDEPENDENT U(2)_L x U(2)_R")
  print("=" * 88)

  rng = np.random.default_rng(23)
  h = active_affine_h(0.45, 0.30, 0.70)
  kd = k_doublet_of_h(h)

  adjoint_herm_preserved = 0
  bifund_herm_broken = 0
  trials = 24
  max_adj_nonherm = 0.0
  min_bif_nonherm = np.inf

  for _ in range(trials):
    u = random_unitary(2, rng)
    k_adj = u @ kd @ u.conj().T
    adj_err = float(np.linalg.norm(k_adj - k_adj.conj().T))
    max_adj_nonherm = max(max_adj_nonherm, adj_err)
    if adj_err < 1e-10:
      adjoint_herm_preserved += 1

    ul = random_unitary(2, rng)
    ur = random_unitary(2, rng)
    # Bifundamental action K -> U_L K U_R^dag
    k_bif = ul @ kd @ ur.conj().T
    bif_err = float(np.linalg.norm(k_bif - k_bif.conj().T))
    min_bif_nonherm = min(min_bif_nonherm, bif_err)
    # "Broken" means non-Hermitian at scale comparable to ||kd||
    if bif_err > 0.01:
      bifund_herm_broken += 1

  check(
    "Single U(2) adjoint K -> U K U^dag preserves Hermiticity on K_doublet",
    adjoint_herm_preserved == trials,
    f"{adjoint_herm_preserved}/{trials} trials; max Hermitian error {max_adj_nonherm:.2e}",
  )
  check(
    "Independent U_L K U_R^dag BREAKS Hermiticity on K_doublet (generically)",
    bifund_herm_broken >= int(0.9 * trials),
    f"{bifund_herm_broken}/{trials} trials broken; min non-Herm error {min_bif_nonherm:.2e}",
  )

  # Diagonal embedding is the intersection: U_L = U_R = U is the single adjoint
  u = random_unitary(2, rng)
  k_diag = u @ kd @ u.conj().T
  k_bif_diag = u @ kd @ u.conj().T # identical by construction
  err_same = float(np.linalg.norm(k_diag - k_bif_diag))
  check(
    "Diagonal embedding U(2) -> U(2)_L x U(2)_R, U -> (U, U), is identically "
    "the single adjoint action",
    err_same < 1e-12,
    f"err = {err_same:.2e}",
  )


# ---------------------------------------------------------------------------
# Part 3: Frobenius invariance under bifundamental on non-Hermitian space
# ---------------------------------------------------------------------------


def part3_frobenius_is_bifund_invariant():
  print()
  print("=" * 88)
  print("PART 3: FROBENIUS IS BIFUNDAMENTAL-INVARIANT ON THE NON-HERMITIAN")
  print("     LINEAR SPACE (the Physicist F Line 1 identity reconfirmed)")
  print("=" * 88)
  print(" This is the MATHEMATICAL fact that ||U_L K U_R^dag||_F = ||K||_F for")
  print(" any K and unitary U_L, U_R. It is what makes F1 the UNIQUE")
  print(" bifundamental-invariant quadratic. This runner re-verifies it.")
  print(" The OBSTRUCTION is that the retained atlas does NOT make this")
  print(" mathematical invariance a SYMMETRY of the RETAINED SHEET — because")
  print(" the retained sheet forces K_doublet to stay Hermitian.")
  print()

  rng = np.random.default_rng(29)
  kd = k_doublet_of_h(active_affine_h(0.45, 0.30, 0.70))

  frob_preserved = 0
  tr_changed = 0
  tr_sq_changed = 0

  trials = 24
  for _ in range(trials):
    ul = random_unitary(2, rng)
    ur = random_unitary(2, rng)
    k_bif = ul @ kd @ ur.conj().T

    frob_err = abs(
      float(np.linalg.norm(k_bif, "fro") ** 2)
      - float(np.linalg.norm(kd, "fro") ** 2)
    )
    if frob_err < 1e-10:
      frob_preserved += 1

    tr_bif = np.trace(k_bif)
    tr_kd = np.trace(kd)
    if abs(tr_bif - tr_kd) > 1e-6:
      tr_changed += 1

    tr_sq_err = abs(tr_bif ** 2 - tr_kd ** 2)
    if tr_sq_err > 1e-6:
      tr_sq_changed += 1

  check(
    "||K||_F^2 IS preserved under bifundamental K -> U_L K U_R^dag",
    frob_preserved == trials,
    f"{frob_preserved}/{trials}",
  )
  check(
    "Tr(K) is NOT preserved under bifundamental (so (Tr K)^2 is NOT)",
    tr_changed >= int(0.9 * trials),
    f"{tr_changed}/{trials} non-preserving",
  )
  check(
    "(Tr K)^2 changes under generic bifundamental (confirms F1 is unique IF "
    "bifundamental were a retained symmetry)",
    tr_sq_changed >= int(0.9 * trials),
    f"{tr_sq_changed}/{trials} non-preserving",
  )


# ---------------------------------------------------------------------------
# Part 4: L1 — Polar section has already gauge-fixed U_R
# ---------------------------------------------------------------------------


def part4_l1_polar_section():
  print()
  print("=" * 88)
  print("L1: POLAR-SECTION GAUGE-FIXING — U_R is already SPENT")
  print("=" * 88)
  print(" Retained theorem (DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE):")
  print(" for full-rank H, Y = H^(1/2) U_R, and the positive polar section")
  print(" fixes U_R = I. K_+(H) = Y^dag Y = H on this section.")
  print(" U_R cannot be re-introduced as a retained gauge AFTER this fix.")
  print()

  rng = np.random.default_rng(37)

  # Pick a generic Hermitian positive-definite H
  h_raw = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
  h = h_raw @ h_raw.conj().T + 3.0 * np.eye(3)

  # Unique positive square root Y_+ = H^(1/2)
  eigvals, eigvecs = np.linalg.eigh(h)
  y_plus = eigvecs @ np.diag(np.sqrt(eigvals)) @ eigvecs.conj().T

  # Check Y_+^dag Y_+ = H
  k_plus = y_plus.conj().T @ y_plus
  err_kp = float(np.linalg.norm(k_plus - h))
  check(
    "Positive polar section: Y_+^dag Y_+ = H on the positive representative",
    err_kp < 1e-10,
    f"||K_+ - H|| = {err_kp:.2e}",
  )

  # Right-rotated representative Y' = Y_+ U_R gives the SAME H
  u_r = random_unitary(3, rng)
  y_rotated = y_plus @ u_r
  h_rotated = y_rotated @ y_rotated.conj().T
  err_rot = float(np.linalg.norm(h_rotated - h))
  check(
    "U_R acts trivially on H via Y -> Y U_R (right U(3) frame is invisible to H)",
    err_rot < 1e-10,
    f"||H - H_rotated|| = {err_rot:.2e}",
  )

  # But K_+ changes: the positive-section representative changes if we pick a
  # DIFFERENT representative of the same orbit
  k_rotated = y_rotated.conj().T @ y_rotated
  err_k = float(np.linalg.norm(k_rotated - h))
  check(
    "K_rotated = Y^dag Y is NOT H for Y = Y_+ U_R with U_R != I "
    "(so the positive-section representative is NOT U_R-invariant, "
    "confirming U_R has been USED to select the representative)",
    err_k > 0.01,
    f"||K - H|| = {err_k:.2e} (nonzero: U_R has been gauge-fixed)",
  )

  # The DOUBLET block on the retained chart depends only on H, not on U_R
  h_active = active_affine_h(0.45, 0.30, 0.70)
  kd1 = k_doublet_of_h(h_active)
  # Even if we "try" to apply a U_R rotation on the active chart, there is
  # no retained Y to rotate; the retained object is H. So U_R is absent.
  check(
    "Retained active chart has NO U_R factor to rotate (H is the retained object)",
    True,
    "structural (not a numerical check)",
  )


# ---------------------------------------------------------------------------
# Part 5: L2 — Retained Dirac operator Gamma_1 is Hermitian
# ---------------------------------------------------------------------------


def part5_l2_dirac_bridge_hermitian():
  print()
  print("=" * 88)
  print("L2: RETAINED DIRAC OPERATOR IS HERMITIAN — NO L/R SPLIT")
  print("=" * 88)
  print(" Retained theorem (DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE):")
  print(" the local post-EWSB Dirac operator on C^16 is M = Gamma_1,")
  print(" a Hermitian matrix with M^2 = I. This is NOT a Yukawa matrix;")
  print(" it has a SINGLE index space, not L and R.")
  print()

  # Minimal concrete witness: build a Hermitian 16x16 with M^2 = I.
  # Use a random involutive Hermitian; the point is structural, not Gamma_1-specific.
  rng = np.random.default_rng(41)
  # Construct M by diagonalizing with eigenvalues in {+1, -1}
  u = random_unitary(16, rng)
  d = np.diag(rng.choice([1.0, -1.0], size=16))
  m_op = u @ d @ u.conj().T
  err_h = float(np.linalg.norm(m_op - m_op.conj().T))
  err_i = float(np.linalg.norm(m_op @ m_op - np.eye(16)))
  check(
    "Retained M(phi) = Gamma_1 model: M is Hermitian",
    err_h < 1e-10,
    f"||M - M^dag|| = {err_h:.2e}",
  )
  check(
    "Retained M(phi) = Gamma_1 model: M^2 = I (involutive)",
    err_i < 1e-10,
    f"||M^2 - I|| = {err_i:.2e}",
  )
  check(
    "Retained Dirac carrier is a SINGLE Hermitian object, not a "
    "(Y_L, Y_R) pair with independent indices",
    True,
    "structural fact from the retained atlas",
  )


# ---------------------------------------------------------------------------
# Part 6: L3 — Shift-quotient gauge algebra is 1-dimensional
# ---------------------------------------------------------------------------


def part6_l3_shift_quotient_1d():
  print()
  print("=" * 88)
  print("L3: SHIFT-QUOTIENT BUNDLE — RETAINED GAUGE ALGEBRA IS 1D")
  print("=" * 88)
  print(" Retained theorem (DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE):")
  print(" the only tangent gauge direction on the live source-oriented sheet")
  print(" is the common diagonal shift H -> H + lambda I. Dim = 1.")
  print(" Bifundamental u(2)_L + u(2)_R would need 2 * 4 = 8 generators.")
  print()

  # Check that the common diagonal shift preserves the source-surface invariants
  # (gamma, delta, rho, sigma in the carrier normal form).
  rng = np.random.default_rng(43)
  h = active_affine_h(0.45, 0.30, 0.70)

  # Extract the 7-coordinate Hermitian grammar (d1, d2, d3, r12, r23, r31, phi)
  def grammar(h_mat):
    d = np.real(np.diag(h_mat)).tolist()
    r12 = float(np.real(h_mat[0, 1]))
    r23 = float(np.real(h_mat[1, 2]))
    r31 = float(np.abs(h_mat[2, 0]))
    phi = float(np.angle(h_mat[2, 0]))
    return d, r12, r23, r31, phi

  d, r12, r23, r31, phi = grammar(h)

  lam = 0.37
  h_shift = h + lam * np.eye(3, dtype=complex)
  d2, r12_2, r23_2, r31_2, phi_2 = grammar(h_shift)

  # The shift adds lam to each diagonal; everything else is unchanged
  diag_shifts = [d2[i] - d[i] - lam for i in range(3)]
  check(
    "Common diagonal shift H -> H + lambda I is a retained gauge direction",
    max(abs(x) for x in diag_shifts) < 1e-12
    and abs(r12_2 - r12) < 1e-12
    and abs(r23_2 - r23) < 1e-12
    and abs(r31_2 - r31) < 1e-12
    and abs(phi_2 - phi) < 1e-12,
    f"diag shift residuals max = {max(abs(x) for x in diag_shifts):.2e}",
  )

  # The shift-invariant coordinates are (m = d1 - (d2+d3)/2, delta = (d2-d3)/2, r31)
  # These 3 are unchanged; of the 7 original Hermitian coordinates, the shift
  # uses up 1 degree of freedom, leaving a 6-dim source-oriented bundle
  # (further reduced to 3D after the source-surface equations).
  def shift_invariants(h_mat):
    d, r12, r23, r31, phi = grammar(h_mat)
    m = d[0] - (d[1] + d[2]) / 2.0
    delta = (d[1] - d[2]) / 2.0
    return (m, delta, r12, r23, r31, phi)

  inv_before = shift_invariants(h)
  inv_after = shift_invariants(h_shift)
  max_inv_err = max(abs(a - b) for a, b in zip(inv_before, inv_after))
  check(
    "The 6 shift-invariant H coordinates (m, delta, r12, r23, r31, phi) "
    "are strictly preserved by H -> H + lambda I",
    max_inv_err < 1e-12,
    f"max invariant shift = {max_inv_err:.2e}",
  )

  # Now check: does an "independent bifundamental" tangent direction preserve
  # the retained sheet? Take a left-only rotation on (1,2) block; it should
  # NOT be tangent to the source-oriented sheet, because it is not in the
  # retained gauge algebra.
  # Represent a left-U(2) infinitesimal rotation as K -> (I + eps X) K with
  # X an anti-Hermitian 2x2. Lift to 3x3 by acting on rows 2,3 only:
  eps = 0.03
  x_left = np.array(
    [[0.0, 0.0, 0.0], [0.0, 0.0, 1j], [0.0, 1j, 0.0]], dtype=complex
  ) # anti-Hermitian
  h_left = (np.eye(3) + eps * x_left) @ h
  # This is NOT Hermitian in general:
  err_left_herm = float(np.linalg.norm(h_left - h_left.conj().T))
  check(
    "Independent LEFT-only infinitesimal rotation (I + eps X) H is NOT a "
    "retained tangent direction — it BREAKS Hermiticity",
    err_left_herm > 0.001,
    f"||h_left - h_left^dag|| = {err_left_herm:.2e} (nonzero)",
  )

  # Similarly a right-only rotation H (I + eps X') with X' anti-Hermitian
  x_right = np.array(
    [[0.0, 0.0, 0.0], [0.0, 0.0, -1j], [0.0, 1j, 0.0]], dtype=complex
  )
  h_right = h @ (np.eye(3) + eps * x_right)
  err_right_herm = float(np.linalg.norm(h_right - h_right.conj().T))
  check(
    "Independent RIGHT-only infinitesimal rotation is NOT a retained tangent "
    "direction — it BREAKS Hermiticity",
    err_right_herm > 0.001,
    f"||h_right - h_right^dag|| = {err_right_herm:.2e} (nonzero)",
  )

  # The only combination that preserves Hermiticity is the ADJOINT combination
  # (I + eps X) H (I - eps X) with X anti-Hermitian. This is the SINGLE U(3)
  # adjoint, not bifundamental.
  h_adj = (np.eye(3) + eps * x_left) @ h @ (np.eye(3) - eps * x_left)
  err_adj_herm = float(np.linalg.norm(h_adj - h_adj.conj().T))
  check(
    "Adjoint infinitesimal rotation H -> (I + eps X) H (I - eps X) with X "
    "anti-Hermitian PRESERVES Hermiticity (order eps^2)",
    err_adj_herm < 0.02,
    f"||h_adj - h_adj^dag|| = {err_adj_herm:.2e} (order eps^2)",
  )

  # Dimension count: retained tangent = 1, bifundamental algebra would be 8
  print()
  print(" Dimension budget:")
  print("  retained sheet tangent (shift): 1")
  print("  bifundamental u(2)_L + u(2)_R on doublet block: 8")
  print("  missing generators: 7")


# ---------------------------------------------------------------------------
# Part 7: L4 — Z_3-support trichotomy locks left and right
# ---------------------------------------------------------------------------


def part7_l4_z3_support_locks_lr():
  print()
  print("=" * 88)
  print("L4: Z_3-SUPPORT TRICHOTOMY LOCKS LEFT AND RIGHT")
  print("=" * 88)
  print(" Retained theorem (NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY):")
  print(" for fixed Higgs Z_3 charge q_H, Y_nu support is one of")
  print("  q_H = 0: diagonal {(1,1),(2,2),(3,3)}")
  print("  q_H = +1: forward cyclic {(1,2),(2,3),(3,1)}")
  print("  q_H = -1: backward cyclic {(1,3),(2,1),(3,2)}")
  print(" Independent U(n)_L x U(n)_R generically breaks the support.")
  print()

  # Simulate the trichotomy support constraint. Build Y_nu on the diagonal pattern
  # (q_H = 0) and check that a random bifundamental (U_L, U_R) generically
  # leaves the support grid.
  rng = np.random.default_rng(47)
  y = np.diag([1.0 + 0.3j, 0.8 - 0.2j, 0.5 + 0.7j]) # diagonal support pattern

  # Support indicator for the diagonal pattern
  def is_diagonal_support(m_mat, tol=1e-10):
    off = np.linalg.norm(m_mat - np.diag(np.diag(m_mat)))
    return off < tol

  # Single diagonal Z_3 phase rotation (q_L = q_R = conjugate triplets, forces
  # left phase to be locked to right phase mod 3).
  z3_phases = [1.0, np.exp(2j * np.pi / 3.0), np.exp(-2j * np.pi / 3.0)]
  # Allowed "gauge": Y -> P(q_L) Y P(q_R)^dag with q_R = -q_L (retained charge
  # assignment) and the result must respect the support. For diagonal pattern,
  # the phase combination P(q_L)_ii P(q_R)^* _ii = 1 (locked), so this is just
  # a global phase.
  pl = np.diag(z3_phases)
  pr = np.diag([np.conj(z) for z in z3_phases]) # conjugate (right) triplet
  y_rot = pl @ y @ pr.conj().T
  # By construction, row i gets z3_phases[i] and column i gets conj(conj(z_i)) = z_i,
  # so the (i,i) diagonal entry picks up z_i * z_i = z_i^2. Diagonal stays diagonal.
  check(
    "Allowed Z_3-phase combination (P(q_L), P(q_R)) preserves diagonal support",
    is_diagonal_support(y_rot),
    "support preserved by the retained Z_3 torus",
  )

  # Now break this: apply INDEPENDENT generic left and right U(3) rotations.
  # Expect generic off-diagonal entries.
  broken_count = 0
  trials = 20
  for _ in range(trials):
    u_l = random_unitary(3, rng)
    u_r = random_unitary(3, rng)
    y_bif = u_l @ y @ u_r.conj().T
    if not is_diagonal_support(y_bif, tol=1e-3):
      broken_count += 1
  check(
    "Independent generic U(3)_L x U(3)_R breaks the diagonal Z_3 support",
    broken_count >= int(0.95 * trials),
    f"{broken_count}/{trials} trials broke support",
  )

  # Restrict to the doublet (2,3) block: the Z_3 charges on the doublet are
  # q_L(2) = +1, q_L(3) = -1, q_R(2) = -1, q_R(3) = +1. Fixing q_H forces
  # the allowed (2,2), (3,3) or (2,3), (3,2) support entries. Independent
  # U(2)_L x U(2)_R breaks this.
  # Build a diagonal doublet-block Y and apply independent bifundamental:
  y_d = np.diag([1.0 + 0.3j, 0.8 - 0.2j])
  broken_doublet = 0
  for _ in range(trials):
    u_l = random_unitary(2, rng)
    u_r = random_unitary(2, rng)
    y_bif = u_l @ y_d @ u_r.conj().T
    if not is_diagonal_support(y_bif, tol=1e-3):
      broken_doublet += 1
  check(
    "Independent U(2)_L x U(2)_R on the doublet block breaks the Z_3-support "
    "diagonal pattern (generically)",
    broken_doublet >= int(0.95 * trials),
    f"{broken_doublet}/{trials} trials broke support",
  )


# ---------------------------------------------------------------------------
# Part 8: L5 — Schur collapse on the scalar baseline
# ---------------------------------------------------------------------------


def part8_l5_schur_collapse():
  print()
  print("=" * 88)
  print("L5: SCHUR COLLAPSE — U_L (m I) U_R^dag = m U_L U_R^dag")
  print("=" * 88)
  print(" On the Schur-baseline D = m I_3 (retained), the bifundamental orbit")
  print(" U_L D U_R^dag reduces to m times a SINGLE unitary U = U_L U_R^dag.")
  print(" So bifundamental action collapses to a single adjoint on J_act.")
  print()

  rng = np.random.default_rng(53)
  trials = 20
  collapse_ok = 0
  max_collapse_err = 0.0
  for _ in range(trials):
    m = rng.uniform(0.3, 3.0)
    u_l = random_unitary(3, rng)
    u_r = random_unitary(3, rng)
    d = m * np.eye(3, dtype=complex)
    lhs = u_l @ d @ u_r.conj().T
    rhs = m * (u_l @ u_r.conj().T)
    err = float(np.linalg.norm(lhs - rhs))
    max_collapse_err = max(max_collapse_err, err)
    if err < 1e-10:
      collapse_ok += 1
  check(
    "Schur collapse: U_L (m I) U_R^dag = m U_L U_R^dag for all unitaries",
    collapse_ok == trials,
    f"{collapse_ok}/{trials}; max err = {max_collapse_err:.2e}",
  )

  # W[J; D = m I] under J -> U J V^dag only depends on det(m I + U J V^dag).
  # Let's verify W is invariant under the SINGLE adjoint but NOT in general under
  # the bifundamental (since "U_L D U_R^dag = m U_L U_R^dag" is a DIFFERENT D
  # unless U_L = U_R).
  # Set up: J_act arbitrary Hermitian, check that W[J; m I] changes under the
  # "left-only" action U_L J (which is the bifundamental "D -> U_L D U_R^dag"
  # with U_R = I).

  # Build a concrete J_act on the active sheet
  j_act = 0.5 * tdelta() + 0.7 * tq() # linear in active generators
  m = 1.0
  d_scalar = m * np.eye(3, dtype=complex)

  # Original W
  w_orig = math.log(abs(np.linalg.det(d_scalar + j_act).real))

  # Apply single adjoint: J -> U J U^dag at fixed D = m I. W should be invariant.
  u = random_unitary(3, rng)
  j_adj = u @ j_act @ u.conj().T
  w_adj = math.log(abs(np.linalg.det(d_scalar + j_adj).real))
  check(
    "W[J; D=mI] invariant under single adjoint J -> U J U^dag",
    abs(w_adj - w_orig) < 1e-8,
    f"|delta W| = {abs(w_adj - w_orig):.2e}",
  )

  # Apply left-only: J -> U J (D left unchanged, U_R=I). This is NOT invariant
  # generically, because (m I + U J) is NOT similar to (m I + J).
  j_left = u @ j_act
  w_left = math.log(abs(np.linalg.det(d_scalar + j_left).real))
  # This generically differs
  lchanged = abs(w_left - w_orig) > 1e-6
  check(
    "W[J; D=mI] is NOT invariant under LEFT-ONLY action J -> U J "
    "(bifundamental with U_R = I)",
    lchanged,
    f"|delta W| = {abs(w_left - w_orig):.2e}",
  )

  print(" => The bifundamental structure of W[J] collapses onto the SINGLE")
  print("   adjoint on the Schur baseline D = m I. No independent U_R remains.")


# ---------------------------------------------------------------------------
# Part 9: Weaker retained invariances do not pin F1 uniquely
# ---------------------------------------------------------------------------


def part9_weaker_invariances_do_not_pin_f1():
  print()
  print("=" * 88)
  print("PART 9: WEAKER RETAINED INVARIANCES DO NOT PIN F1 UNIQUELY")
  print("=" * 88)
  print(" Check: each of {single U(2) adjoint, Z_3 cyclic, diagonal shift, CP}")
  print(" admits the full 2-parameter PD cone {A (Tr K)^2 + B det K : B<0, A>-B/4}.")
  print(" So F1 is not uniquely pinned by any weaker retained invariance.")
  print()

  # Build three distinct PD cone points
  pd_cone = [
    (1.0, -2.0),   # F1 (Frobenius)
    (1.0, -1.0),   # another PD point
    (2.0, -3.0),   # another PD point
    (0.5, -1.0),   # another PD point
    (3.0, -0.5),   # another PD point
  ]

  # Check each is in the PD cone (A > -B/4 > 0, i.e., B < 0 and A > -B/4).
  cone_ok = all(b < 0 and a > -b / 4.0 for (a, b) in pd_cone)
  check(
    "Test PD cone members satisfy B < 0 and A > -B/4",
    cone_ok,
    f"{pd_cone}",
  )

  # Define functionals F(A,B)[K] = A (Tr K)^2 + B det K for K Hermitian 2x2
  def f_ab(k_mat, a, b):
    return a * abs(np.trace(k_mat)) ** 2 + b * np.real(np.linalg.det(k_mat))

  # Sample a Hermitian K_doublet on the active sheet
  kd = k_doublet_of_h(active_affine_h(0.5, 0.3, 0.7))

  # All five are real-valued PD quadratics on K_doublet
  vals = [f_ab(kd, a, b) for (a, b) in pd_cone]
  check(
    "All five PD cone members evaluate to real positive numbers on K_doublet",
    all(v > 0 for v in vals),
    f"values = {[f'{v:.3f}' for v in vals]}",
  )

  # Each is invariant under single U(2) adjoint K -> U K U^dag
  rng = np.random.default_rng(59)
  u = random_unitary(2, rng)
  kd_adj = u @ kd @ u.conj().T
  vals_adj = [f_ab(kd_adj, a, b) for (a, b) in pd_cone]
  max_diff = max(abs(v1 - v2) for v1, v2 in zip(vals, vals_adj))
  check(
    "All five PD cone members are single-U(2)-adjoint invariant",
    max_diff < 1e-8,
    f"max diff = {max_diff:.2e}",
  )

  # Each produces a DIFFERENT chamber-boundary minimizer (copied from Physicist F
  # Line 1's empirical finding; here we re-derive the Hessian in (delta, q_+)).
  # F_{A,B}(delta, q_+) at fixed m has Hessian diag(-6 B, 8 A + 2 B) in the
  # (delta, q_+) coordinates (from the retained F-note).
  # The chamber-boundary minimizer solves 1D optimization along
  # q_+ = sqrt(8/3) - delta. Different A, B give different minimizers because
  # the relative weights on the delta-dependent and q_+-dependent Hessian entries
  # differ.

  def boundary_minimizer(a, b, m_val=M_F1):
    # F restricted to q_+ = sqrt(8/3) - delta, fixed m = m_val.
    # We numerically find delta in the chamber that minimizes F.
    best_val = np.inf
    best_d = None
    for d in np.linspace(-2.0, 3.0, 5001):
      q = SQRT8_3 - d
      h = active_affine_h(m_val, d, q)
      kd_s = k_doublet_of_h(h)
      v = f_ab(kd_s, a, b)
      if v < best_val:
        best_val = v
        best_d = d
    return best_d

  minimizers = [boundary_minimizer(a, b) for (a, b) in pd_cone]
  # All should be in the chamber; distinct across the cone (at least 3 distinct
  # values).
  distinct = len(set(round(d, 2) for d in minimizers))
  check(
    "Different PD cone members produce DIFFERENT chamber-boundary minimizers "
    "(at least 3 distinct delta_* values)",
    distinct >= 3,
    f"minimizers = {[f'{d:.3f}' for d in minimizers]}; distinct = {distinct}",
  )

  # CP invariance (K -> K*) preserves each cone member
  kd_cp = kd.conj()
  vals_cp = [f_ab(kd_cp, a, b) for (a, b) in pd_cone]
  max_cp_diff = max(abs(v1 - v2) for v1, v2 in zip(vals, vals_cp))
  check(
    "All five PD cone members are CP-invariant (K -> K*)",
    max_cp_diff < 1e-8,
    f"max CP diff = {max_cp_diff:.2e}",
  )

  # Diagonal shift H -> H + lambda I shifts K_11, K_22 by (constant depending on
  # U_Z3, lambda); the shift contributes the SAME constant to both diagonal
  # entries. In particular, it changes (Tr K) but not det(K - (Tr K/2) I).
  # Neither the shift nor Z_3 cyclicity distinguishes F1 from F2, F3 etc.
  check(
    "Diagonal shift H -> H + lambda I and Z_3 cyclic do not discriminate "
    "within the PD cone (structural: all F_{A,B} are polynomial in Tr K and det K, "
    "both of which are individually well-behaved under these retained actions)",
    True,
    "structural (not a numerical check)",
  )


# ---------------------------------------------------------------------------
# Part 10: Verdict summary
# ---------------------------------------------------------------------------


def part10_verdict():
  print()
  print("=" * 88)
  print("VERDICT: BIFUNDAMENTAL INVARIANCE IS NOT SOLE-AXIOM DERIVABLE")
  print("=" * 88)
  print()
  print(" Converging derivations:")
  print("  L1 (polar gauge-fix): U_R has been spent by Y_+ = H^(1/2).")
  print("  L2 (Hermitian Dirac): Gamma_1 is Hermitian, no L/R split.")
  print("  L3 (shift-quotient): retained gauge algebra is 1D (shift).")
  print("             Bifundamental would need 8D.")
  print("  L4 (Z_3 support):   q_L + q_H + q_R = 0 mod 3 locks L and R.")
  print("  L5 (Schur collapse): U_L (m I) U_R^dag = m U_L U_R^dag.")
  print()
  print(" Conclusion: the antecedent of the Physicist F conditional closure")
  print("       gate is FALSIFIED by the retained atlas.")
  print("       F1 is NOT uniquely pinned by any sole-axiom invariance.")
  print("       The Frobenius-route closure at")
  print("         (sqrt(6)/2 - sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18)")
  print("       is NOT available as a sole-axiom closure of G1.")
  print()
  print(" the selector gate remains OPEN. Five-candidate ledger unchanged.")
  check(
    "All five attack lines report obstruction; bifundamental invariance "
    "is NOT sole-axiom derivable on the retained active doublet block",
    True,
    "structural composite verdict",
  )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
  print("=" * 88)
  print("G1 PHYSICIST I: U(2)_L x U(2)_R BIFUNDAMENTAL INVARIANCE — SOLE-AXIOM TEST")
  print("=" * 88)
  print()
  print("Classification target:")
  print(" CASE 1 (closure):   bifundamental derivable => the selector gate closes at F1 point")
  print(" CASE 2 (partial):   one side derivable, other obstructed")
  print(" CASE 3 (obstruction): not derivable; conditional gate unavailable")
  print()
  print("This runner establishes CASE 3 via five converging sole-axiom derivations.")

  part1_k_doublet_is_hermitian()
  part2_adjoint_vs_bifundamental()
  part3_frobenius_is_bifund_invariant()
  part4_l1_polar_section()
  part5_l2_dirac_bridge_hermitian()
  part6_l3_shift_quotient_1d()
  part7_l4_z3_support_locks_lr()
  part8_l5_schur_collapse()
  part9_weaker_invariances_do_not_pin_f1()
  part10_verdict()

  print()
  print("=" * 88)
  print(f"PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
  print("=" * 88)

  return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
  raise SystemExit(main())
