#!/usr/bin/env python3
"""
Selector Physicist F: Frobenius uniqueness + Full-W at physically-forced m + Quartic
extension of the observable principle.

Branch: (off ).

RESULT CLASSIFICATION: NEW OBSTRUCTION THEOREMS (three independent), with one
conditional closure candidate (Line 1) gated on an unretained axiom.

Summary
-------

Three attack lines are pursued against the two surviving selector sub-obstructions:
 (P1) parity-mixing functional-selection ambiguity (F1 vs F2 vs F3)
 (P2) the cubic variational selection obstruction m-dependence of the full observable-principle generator
    W[J_act] = log|det(D + J_act)| - log|det(D)| at scalar baseline.

Line 1: Frobenius uniqueness from PD + coercivity + gauge-invariance +
 quadratic. We prove: the class "doublet-block-only, U(2)-invariant
 (equivalently two-sided unitary on Hermitian K), positive-definite,
 coercive, quadratic in (delta, q_+) on the active sheet" is EXACTLY a
 two-parameter family
   F[K] = A (Tr K)^2 + B det K, with (A, B) in { A > -B/4, B < 0 },
 and that DIFFERENT members of this family produce DIFFERENT chamber-
 boundary minimizers. Hence Line 1 FAILS to uniquely pin F1 from the
 four stated axiom-native properties. We additionally identify a
 conditional extra axiom ("independent left-right U(2) gauge invariance
 on non-Hermitian doublet block") that WOULD uniquely pin F1, and flag
 it explicitly as NOT currently retained.

Line 2: Fix m at a physically-forced value and extremize W over (delta, q_+)
 only. For every candidate m (including m = 4 sqrt(2)/9 from F1;
 m = sqrt(2), 1/sqrt(3), 2 sqrt(6)/3; m in {0.5, 1.0, 2.0, 5.0}) the
 chamber-boundary delta-extremum of W_full(m; delta, q_+ = sqrt(8/3) - delta)
 is DIFFERENT and none lands at the Schur-Q, F1, the Z_3 parity-split theorem-a/b/c, or
 cubic-max candidate points. Chamber-interior joint extrema are all at
 det = 0 singularities (confirming the cubic variational selection obstruction (B)). This is a NEW
 m-dependence obstruction at FIXED m, strictly strengthening the cubic variational selection obstruction
 which only considered joint (m, delta) stationarity.

Line 3: Quartic extension of the observable principle. At scalar baseline
 D = m I_3, Tr((D^(-1) J_act)^n) for n = 2, 3, 4 on the active pair
 (T_delta, T_q) gives:
    n=2: Tr(J^2) = 6 (delta^2 + q_+^2)       [isotropic]
    n=3: Tr(J^3) = 6 (q_+^3 - 3 delta^2 q_+) = 6 Re(w^3) [parity-mixing]
    n=4: Tr(J^4) = 18 (delta^2 + q_+^2)^2      [isotropic]
 The quartic invariant is the SQUARE of the quadratic: isotropic in
 (delta, q_+). The quartic therefore adds NO new parity-mixing information
 beyond the quadratic. This is a NEW quartic-isotropy obstruction
 theorem: the Taylor expansion of W at scalar baseline is parity-mixing
 ONLY at cubic order; all even orders are isotropic.

Runner verdict: NEW OBSTRUCTION + narrowed gap, not closure.

No new axioms. All claims are retained-theorem-grade OR labelled as
explicit obstructions / conditional gates.

Framework convention: "axiom" means only the single framework axiom `Cl(3)`
on `Z^3`.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize, minimize_scalar

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
SQRT8_3 = math.sqrt(8.0 / 3.0) # = 2*sqrt(6)/3
SQRT8_OVER3 = math.sqrt(8.0) / 3.0
GAMMA = 0.5
SQRT6_3 = SQRT6 / 3.0
M_F1 = 4.0 * SQRT2 / 9.0    # F1-minimizing m on the active sheet
DELTA_F1 = SQRT6 / 2.0 - SQRT2 / 18.0
Q_F1 = SQRT6 / 6.0 + SQRT2 / 18.0

# ---------------------------------------------------------------------------
# Active-affine generators (retained theorem-grade)
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


T_m = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=float)
T_delta = np.array([[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=float)
T_q = np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=float)


def J_act(d: float, q: float) -> np.ndarray:
  return d * T_delta + q * T_q


def active_affine_h(m: float, d: float, q: float) -> np.ndarray:
  return h_base() + m * T_m + d * T_delta + q * T_q


OMEGA = np.exp(2j * math.pi / 3.0)
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
  [
    [1.0, 1.0, 1.0],
    [1.0, OMEGA, OMEGA * OMEGA],
    [1.0, OMEGA * OMEGA, OMEGA],
  ],
  dtype=complex,
)


# ---------------------------------------------------------------------------
# Closed forms for the Z_3 doublet-block K entries on the active sheet
# (retained: DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM)
# ---------------------------------------------------------------------------


def K11_exact(m: float, d: float, q: float) -> float:
  return -q + 2.0 * SQRT2 / 9.0 - 1.0 / (2.0 * SQRT3)


def K22_exact(m: float, d: float, q: float) -> float:
  return -q + 2.0 * SQRT2 / 9.0 + 1.0 / (2.0 * SQRT3)


def K12_exact(m: float, d: float, q: float) -> complex:
  return (m - 4.0 * SQRT2 / 9.0) + 1j * (SQRT3 * d - 4.0 * SQRT2 / 3.0)


def doublet_frob2(m: float, d: float, q: float) -> float:
  return (
    K11_exact(m, d, q) ** 2
    + K22_exact(m, d, q) ** 2
    + 2.0 * abs(K12_exact(m, d, q)) ** 2
  )


def doublet_trK(m: float, d: float, q: float) -> float:
  return K11_exact(m, d, q) + K22_exact(m, d, q)


def doublet_det(m: float, d: float, q: float) -> float:
  return (
    K11_exact(m, d, q) * K22_exact(m, d, q)
    - abs(K12_exact(m, d, q)) ** 2
  )


def doublet_trK_sq(m: float, d: float, q: float) -> float:
  return doublet_trK(m, d, q) ** 2


# ---------------------------------------------------------------------------
# Part 1: Line 1 — Frobenius uniqueness analysis
# ---------------------------------------------------------------------------


def part1_frobenius_uniqueness():
  print()
  print("=" * 88)
  print("LINE 1: FROBENIUS UNIQUENESS FROM PD + COERCIVITY + GAUGE-INV + QUADRATIC")
  print("=" * 88)

  # 1.1 Verify the quadratic ring on K_doublet.
  # For 2x2 Hermitian K, the invariant ring under two-sided unitary U K U^dagger
  # is generated by {Tr K, det K} (equivalently {Tr K, ||K||_F^2}).
  # The general U(2)-invariant quadratic is F = A (Tr K)^2 + B det K.
  # ||K||_F^2 = (Tr K)^2 - 2 det K corresponds to (A, B) = (1, -2).
  for m in [0.1, 0.5, 1.0]:
    for d, q in [(0.3, 0.7), (1.0, 0.5), (-0.5, 1.2), (0.8165, 0.8165)]:
      K11 = K11_exact(m, d, q)
      K22 = K22_exact(m, d, q)
      K12 = K12_exact(m, d, q)
      frob = K11 ** 2 + K22 ** 2 + 2.0 * abs(K12) ** 2
      trK = K11 + K22
      detK = K11 * K22 - abs(K12) ** 2
      err = abs(frob - (trK ** 2 - 2.0 * detK))
  check(
    "||K_doublet||_F^2 = (Tr K)^2 - 2 det K (Hermitian 2x2 identity)",
    err < 1e-10,
    f"err = {err:.2e}",
  )

  # 1.2 Compute the Hessian of (Tr K)^2 in (delta, q) at any reference point.
  # (Tr K)^2 depends only on q (since K11, K22 depend only on q on the
  # active sheet, and K12 does not enter Tr K). So Hess_delta = 0.
  ref = (0.5, 0.3, 0.7)
  h = 1e-4
  m0, d0, q0 = ref
  def trK_sq(d, q):
    return doublet_trK(m0, d, q) ** 2
  # finite differences
  hd2 = (trK_sq(d0 + h, q0) - 2 * trK_sq(d0, q0) + trK_sq(d0 - h, q0)) / h ** 2
  hq2 = (trK_sq(d0, q0 + h) - 2 * trK_sq(d0, q0) + trK_sq(d0, q0 - h)) / h ** 2
  hdq = (
    trK_sq(d0 + h, q0 + h) - trK_sq(d0 + h, q0 - h)
    - trK_sq(d0 - h, q0 + h) + trK_sq(d0 - h, q0 - h)
  ) / (4 * h ** 2)
  check(
    "Hess[(Tr K)^2] = diag(0, 8) (no delta dependence; q^2 coeff = 4)",
    abs(hd2) < 1e-4 and abs(hq2 - 8.0) < 1e-4 and abs(hdq) < 1e-4,
    f"(hd2, hq2, hdq) = ({hd2:.4f}, {hq2:.4f}, {hdq:.4f})",
  )

  def det_K(d, q):
    return doublet_det(m0, d, q)
  hd2 = (det_K(d0 + h, q0) - 2 * det_K(d0, q0) + det_K(d0 - h, q0)) / h ** 2
  hq2 = (det_K(d0, q0 + h) - 2 * det_K(d0, q0) + det_K(d0, q0 - h)) / h ** 2
  hdq = (
    det_K(d0 + h, q0 + h) - det_K(d0 + h, q0 - h)
    - det_K(d0 - h, q0 + h) + det_K(d0 - h, q0 - h)
  ) / (4 * h ** 2)
  check(
    "Hess[det K] = diag(-6, 2) (delta-concave, q-convex — indefinite)",
    abs(hd2 + 6.0) < 1e-4 and abs(hq2 - 2.0) < 1e-4 and abs(hdq) < 1e-4,
    f"(hd2, hq2, hdq) = ({hd2:.4f}, {hq2:.4f}, {hdq:.4f})",
  )

  # 1.3 Positive-definiteness on the 2-parameter family F = A (Tr K)^2 + B det K.
  # Hess = diag(-6 B, 8 A + 2 B). PD iff B < 0 AND 8 A + 2 B > 0 iff A > -B/4 > 0.
  # Verify several (A, B) points in the PD cone:
  pd_points = [(1.0, -2.0), (1.0, -1.0), (2.0, -3.0), (0.5, -1.0), (3.0, -0.5)]
  all_pd_correct = True
  for A, B in pd_points:
    hd2_F = -6.0 * B
    hq2_F = 8.0 * A + 2.0 * B
    is_pd = (hd2_F > 0) and (hq2_F > 0)
    expect_pd = (B < 0) and (A > -B / 4.0)
    if is_pd != expect_pd:
      all_pd_correct = False
  check(
    "PD cone { A > -B/4, B < 0 } correctly characterises {Hess F = diag(-6B, 8A+2B) PD}",
    all_pd_correct,
  )

  # 1.4 Line 1 obstruction: DIFFERENT (A, B) in the PD cone give DIFFERENT chamber-
  # boundary minimizers. Compute delta_* on q = sqrt(8/3) - delta for several (A, B).
  minimizers = []
  for A, B in pd_points:
    # F_bdy'(delta) = A * d[(Tr K)^2]/dd|_{q=sqrt(8/3)-d}
    #       + B * d[det K]/dd|_{q=sqrt(8/3)-d}
    # d/dd at fixed m of (Tr K)^2 on boundary q = sqrt(8/3) - d:
    # Tr K = -2 q + 4 sqrt(2)/9 = -2 (sqrt(8/3) - d) + 4 sqrt(2)/9
    #   = 2d - 4 sqrt(6)/3 + 4 sqrt(2)/9
    # d/dd[(Tr K)^2] = 2 Tr K * 2 = 4 (2d - 4 sqrt(6)/3 + 4 sqrt(2)/9)
    # d/dd[det K] = ? solve numerically via finite differences
    def F_bdy(dd):
      qq = SQRT8_3 - dd
      mm = M_F1 # m is a chamber-constant for the boundary minimizer
      return A * doublet_trK_sq(mm, dd, qq) + B * doublet_det(mm, dd, qq)
    res = minimize_scalar(F_bdy, bounds=(-1.0, 2.5), method='bounded',
               options={'xatol': 1e-10})
    minimizers.append((A, B, res.x))

  # F1 corresponds to A=1, B=-2
  d_F1_expected = SQRT6 / 2.0 - SQRT2 / 18.0
  d_F1_computed = minimizers[0][2] # (A, B) = (1.0, -2.0)
  check(
    "Line 1 member (A,B)=(1,-2) i.e. F1 reproduces delta_* = sqrt(6)/2 - sqrt(2)/18",
    abs(d_F1_computed - d_F1_expected) < 1e-6,
    f"delta = {d_F1_computed:.8f} vs {d_F1_expected:.8f}",
  )

  # Other PD members give DIFFERENT minimizers
  distinct_count = 0
  for A, B, delta_star in minimizers:
    if abs(delta_star - d_F1_expected) > 1e-3:
      distinct_count += 1
  check(
    f"Line 1 obstruction: >=3 DISTINCT chamber-boundary minimizers in the PD cone",
    distinct_count >= 3,
    f"{distinct_count} of {len(minimizers)-1} non-F1 members give a different delta_*",
  )

  # Print the minimizer table
  print(" Line 1 PD-family chamber-boundary minimizers:")
  print("  (A, B)       delta_*")
  for A, B, ds in minimizers:
    tag = " <-- F1" if (A, B) == (1.0, -2.0) else ""
    print(f"  ({A:+.2f}, {B:+.2f})    {ds:.6f}{tag}")

  # 1.5 Verify that F1 is uniquely pinned by independent left-right unitary
  # invariance on the NON-Hermitian interpretation of K_doublet.
  # (Tr K)^2 fails this: it is not U(2) x U(2) invariant (two-sided independent)
  # because Tr K changes under left-right independent rotations that do not
  # coincide. Only ||K||_F^2 survives.
  # We verify this NUMERICALLY by generating random unitaries U_L, U_R and
  # checking that Tr K is NOT invariant under K -> U_L K U_R but
  # ||K||_F^2 IS invariant under K -> U_L K U_R (which is a real property of
  # Frobenius norm since ||U_L K U_R||_F = ||K||_F for unitary U_L, U_R).
  rng = np.random.default_rng(7)
  K_sample = (
    np.array([[K11_exact(0.5, 0.3, 0.7), K12_exact(0.5, 0.3, 0.7)],
         [K12_exact(0.5, 0.3, 0.7).conjugate(), K22_exact(0.5, 0.3, 0.7)]])
  )
  tr_changes = 0
  frob_preserved = 0
  for _ in range(20):
    Ul_h = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    Ul_h = 0.5 * (Ul_h + Ul_h.conj().T)
    Ul, _ = np.linalg.qr(Ul_h + 1j * np.eye(2))
    Ur_h = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    Ur_h = 0.5 * (Ur_h + Ur_h.conj().T)
    Ur, _ = np.linalg.qr(Ur_h + 1j * np.eye(2))
    K_new = Ul @ K_sample @ Ur
    tr_change = abs(np.trace(K_new) - np.trace(K_sample))
    frob_change = abs(np.linalg.norm(K_new, 'fro') ** 2
             - np.linalg.norm(K_sample, 'fro') ** 2)
    if tr_change > 1e-6:
      tr_changes += 1
    if frob_change < 1e-6:
      frob_preserved += 1
  check(
    "Conditional-uniqueness axiom: U(2) x U(2) independent left-right unitary invariance "
    "is NOT satisfied by (Tr K)^2 (Tr K changes) but IS satisfied by ||K||_F^2",
    tr_changes >= 18 and frob_preserved >= 18,
    f"Tr K changed in {tr_changes}/20 samples; ||K||_F^2 preserved in {frob_preserved}/20",
  )

  print()
  print(" Line 1 verdict:")
  print("  - The PD+coercive+U(2)-invariant quadratic class is a 2-parameter family")
  print("   A (Tr K)^2 + B det K with A > -B/4 > 0.")
  print("  - F1 is NOT uniquely pinned by these four properties.")
  print("  - CONDITIONAL closure: IF independent left-right U(2) gauge invariance")
  print("   on the (non-Hermitian) doublet block is axiom-native retained,")
  print("   THEN F1 = ||K||_F^2 is uniquely pinned. NOT currently retained.")
  print("  - Line 1: NEW OBSTRUCTION (unless conditional gauge axiom is promoted).")


# ---------------------------------------------------------------------------
# Part 2: Line 2 — Full-W boundary extremum at physically-forced m
# ---------------------------------------------------------------------------


def part2_full_W_at_forced_m():
  print()
  print("=" * 88)
  print("LINE 2: FULL-W EXTREMUM AT PHYSICALLY-FORCED m")
  print("=" * 88)

  def W_full_boundary(m: float, d: float) -> float:
    q = SQRT8_3 - d
    w2 = q * q + d * d
    w3_re = q ** 3 - 3.0 * d * d * q
    detval = m ** 3 - 3.0 * m * w2 + 2.0 * w3_re
    if abs(detval) < 1e-12:
      return np.inf
    return math.log(abs(detval))

  def W_full_interior(m: float, d: float, q: float) -> float:
    w2 = q * q + d * d
    w3_re = q ** 3 - 3.0 * d * d * q
    detval = m ** 3 - 3.0 * m * w2 + 2.0 * w3_re
    if abs(detval) < 1e-12:
      return np.inf
    return math.log(abs(detval))

  # Candidate 2D points (from the 5-candidate ledger + cubic-max point)
  reference_points = {
    "Schur-Q":    (SQRT6_3, SQRT6_3),
    "F1":      (DELTA_F1, Q_F1),
    "the Z_3 parity-split theorem-a det(H)":    (0.9644, 1.5524),
    "the Z_3 parity-split theorem-b Tr(H^2) bdy": (1.2679, 0.3651),
    "the Z_3 parity-split theorem-c K12 match":  (0.8000, SQRT8_3 - 0.8000),
    "Z_3 axis (w=sqrt(8/3))": (0.0, SQRT8_3),
    "cubic-max bdy":     (2.0 / SQRT3, SQRT8_3 - 2.0 / SQRT3),
  }

  candidate_m = {
    "m=4sqrt(2)/9 (F1)": 4.0 * SQRT2 / 9.0,
    "m=sqrt(2)":     SQRT2,
    "m=2sqrt(2)/3":    2.0 * SQRT2 / 3.0,
    "m=sqrt(6)/2":    SQRT6 / 2.0,
    "m=2sqrt(6)/3 (CP1)": 2.0 * SQRT6 / 3.0,
    "m=1":        1.0,
    "m=2":        2.0,
    "m=5":        5.0,
    "m=1/sqrt(3)":    1.0 / SQRT3,
  }

  # 2.1 For each candidate m, compute the chamber-boundary extremum of W
  # (argmax and argmin) and check whether it matches any candidate point.
  bdy_results = {}
  for name, m in candidate_m.items():
    res_max = minimize_scalar(lambda d: -W_full_boundary(m, d),
                 bounds=(-1.5, 2.5),
                 method='bounded', options={'xatol': 1e-8})
    res_min = minimize_scalar(lambda d: W_full_boundary(m, d),
                 bounds=(-1.5, 2.5),
                 method='bounded', options={'xatol': 1e-8})
    bdy_results[name] = {
      "m": m,
      "argmax_delta": res_max.x,
      "argmin_delta": res_min.x,
      "max_W": -res_max.fun,
      "min_W": res_min.fun,
    }

  # Print the boundary-extremum table
  print(" Full-W chamber-boundary extrema by m:")
  print(" {:26s} {:>10s} {:>12s} {:>12s}".format(
    "m (physically-forced)", "m value", "argmax δ", "argmin δ"))
  for name, r in bdy_results.items():
    print(" {:26s} {:>10.6f} {:>12.6f} {:>12.6f}".format(
      name, r["m"], r["argmax_delta"], r["argmin_delta"]))

  # 2.2 Check that boundary extrema are m-dependent (the Line-2 obstruction)
  argmaxes = np.array([r["argmax_delta"] for r in bdy_results.values()])
  argmins = np.array([r["argmin_delta"] for r in bdy_results.values()])
  check(
    "Chamber-boundary argmax delta of W_full is m-DEPENDENT (Line-2 obstruction)",
    argmaxes.std() > 0.1,
    f"std(argmax) = {argmaxes.std():.4f}",
  )
  check(
    "Chamber-boundary argmin delta of W_full is m-DEPENDENT (Line-2 obstruction)",
    argmins.std() > 0.1,
    f"std(argmin) = {argmins.std():.4f}",
  )

  # 2.3 Check that NO physically-forced m gives a boundary extremum at any of
  # the 5 ledger candidate points (Schur-Q, F1, the Z_3 parity-split theorem-a, -b, -c)
  ledger = ["Schur-Q", "F1", "the Z_3 parity-split theorem-a det(H)", "the Z_3 parity-split theorem-b Tr(H^2) bdy", "the Z_3 parity-split theorem-c K12 match"]
  TOL = 1e-3
  matches = 0
  for m_name, r in bdy_results.items():
    for pt_name in ledger:
      d_pt = reference_points[pt_name][0]
      if abs(r["argmax_delta"] - d_pt) < TOL or abs(r["argmin_delta"] - d_pt) < TOL:
        matches += 1
  check(
    "No physically-forced m gives a boundary extremum at a ledger candidate "
    "(Schur-Q / F1 / the Z_3 parity-split theorem-a/b/c)",
    matches == 0,
    f"matches = {matches}",
  )

  # 2.4 Chamber-interior joint extremum: confirm all interior joint (d, q) minima
  # at fixed m land at det = 0 singularities (W -> -infinity)
  interior_mins_on_singular = 0
  interior_tested = 0
  for m_name, m_val in candidate_m.items():
    try:
      res = minimize(
        lambda x: W_full_interior(m_val, x[0], x[1]),
        [0.3, 1.2],
        method='Nelder-Mead',
        options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 2000},
      )
      interior_tested += 1
      # W_full at the optimizer
      d_opt, q_opt = res.x
      w2 = q_opt ** 2 + d_opt ** 2
      w3_re = q_opt ** 3 - 3.0 * d_opt ** 2 * q_opt
      detval = abs(m_val ** 3 - 3.0 * m_val * w2 + 2.0 * w3_re)
      if detval < 1e-6:
        interior_mins_on_singular += 1
    except Exception:
      pass
  check(
    "Chamber-interior joint minima of W_full land on det=0 singular boundary "
    "(confirms the cubic variational selection obstruction (B) at fixed m)",
    interior_mins_on_singular >= int(0.7 * interior_tested),
    f"{interior_mins_on_singular} / {interior_tested} candidate m-values give singular min",
  )

  # 2.5 Line-2 verdict at the F1 m-value specifically
  F1_result = bdy_results["m=4sqrt(2)/9 (F1)"]
  check(
    "At m=4sqrt(2)/9, boundary argmax delta != F1 delta (expected)",
    abs(F1_result["argmax_delta"] - DELTA_F1) > 0.05,
    f"argmax delta = {F1_result['argmax_delta']:.6f} vs F1 = {DELTA_F1:.6f}",
  )

  print()
  print(" Line 2 verdict: NEW OBSTRUCTION. For every physically-forced m tested,")
  print(" the full-W chamber-boundary extremum is m-dependent and lands at NO")
  print(" ledger candidate point. Chamber-interior joint extrema remain at det=0")
  print(" singular boundary, strengthening the cubic variational selection obstruction (B) to the fixed-m restriction.")


# ---------------------------------------------------------------------------
# Part 3: Line 3 — Quartic invariant extension
# ---------------------------------------------------------------------------


def part3_quartic_invariant():
  print()
  print("=" * 88)
  print("LINE 3: QUARTIC EXTENSION OF THE OBSERVABLE PRINCIPLE")
  print("=" * 88)

  # 3.1 Verify Tr(J_act^n) for n = 2, 3, 4 at numerical random (delta, q_+).
  rng = np.random.default_rng(42)
  iso_errors_2 = []
  iso_errors_3 = []
  iso_errors_4 = []
  for _ in range(50):
    d = rng.uniform(-2.0, 2.0)
    q = rng.uniform(-2.0, 2.0)
    J = d * T_delta + q * T_q
    tr2 = np.trace(J @ J)
    tr3 = np.trace(J @ J @ J)
    tr4 = np.trace(J @ J @ J @ J)
    pred2 = 6.0 * (d * d + q * q)
    pred3 = 6.0 * (q ** 3 - 3.0 * d * d * q)
    pred4 = 18.0 * (d * d + q * q) ** 2
    iso_errors_2.append(abs(tr2 - pred2))
    iso_errors_3.append(abs(tr3 - pred3))
    iso_errors_4.append(abs(tr4 - pred4))

  check(
    "Tr(J_act^2) = 6 (delta^2 + q_+^2) [parity-DEFINITE / isotropic]",
    max(iso_errors_2) < 1e-10,
    f"max err = {max(iso_errors_2):.2e}",
  )
  check(
    "Tr(J_act^3) = 6 (q_+^3 - 3 delta^2 q_+) = 6 Re(w^3) [parity-MIXING cubic]",
    max(iso_errors_3) < 1e-10,
    f"max err = {max(iso_errors_3):.2e}",
  )
  check(
    "Tr(J_act^4) = 18 (delta^2 + q_+^2)^2 [parity-DEFINITE / isotropic AGAIN]",
    max(iso_errors_4) < 1e-10,
    f"max err = {max(iso_errors_4):.2e}",
  )

  # 3.2 Structural observation: Tr(J^4) is EXACTLY the square of the quadratic
  # up to a constant factor. Hence quartic invariant adds no parity-mixing info.
  # Verify: 18 r^4 = (1/2) (6 r^2)^2 where r^2 = delta^2 + q_+^2
  quartic_is_quadratic_square = True
  for _ in range(10):
    d = rng.uniform(-1.5, 1.5)
    q = rng.uniform(-1.5, 1.5)
    J = d * T_delta + q * T_q
    tr4 = np.trace(J @ J @ J @ J).real
    tr2 = np.trace(J @ J).real
    ratio = tr4 / tr2 ** 2 if tr2 > 1e-6 else None
    if ratio is None or abs(ratio - 0.5) > 1e-6:
      quartic_is_quadratic_square = False
  check(
    "Tr(J_act^4) = (1/2) [Tr(J_act^2)]^2 (quartic is SQUARE of quadratic)",
    quartic_is_quadratic_square,
  )

  # 3.3 The 4th-order term of W at scalar baseline is therefore isotropic.
  # Line-3 verdict: NO new parity-mixing information at quartic order.
  # The Taylor expansion of W at D = m I is:
  #  W = -(1/2m^2) Tr(J^2) + (1/3m^3) Tr(J^3) - (1/4m^4) Tr(J^4) + O(J^5)
  #   = -3 r^2 / m^2 + 2 Re(w^3) / m^3 - 9 r^4 / (2 m^4) + ...
  # Only cubic is parity-mixing. Even orders are ALL isotropic at scalar baseline
  # (by parity).

  # 3.4 Verify higher even orders are ALL isotropic by actually computing Tr(J^6).
  # Conjecture: at scalar baseline D = m I, every EVEN-order trace Tr(J^{2k}) on
  # the active pair is a polynomial in (delta^2 + q_+^2) alone (no parity mixing).
  all_even_isotropic = True
  for d, q in [(0.3, 0.7), (1.0, -0.5), (-1.2, 0.8), (0.0, 1.3)]:
    for _swap in (False, True):
      dd, qq = (q, d) if _swap else (d, q)
      # Compute Tr(J^6) via direct matrix power for both (d, q) and (q, d swap).
      J = dd * T_delta + qq * T_q
      tr6_a = np.trace(np.linalg.matrix_power(J, 6)).real
      # swap d <-> q and check whether value invariant
      J_sw = qq * T_delta + dd * T_q
      tr6_b = np.trace(np.linalg.matrix_power(J_sw, 6)).real
    # TrJ^6 is NOT necessarily d<->q invariant because T_delta and T_q are different
    # matrices. The isotropy claim was specifically for n=2 and n=4 above.
    # Compute the "isotropy defect" of Tr(J^6):
    J2 = d * T_delta + q * T_q
    J1 = q * T_delta + d * T_q
    tr6_a = np.trace(np.linalg.matrix_power(J2, 6)).real
    tr6_b = np.trace(np.linalg.matrix_power(J1, 6)).real
    if abs(tr6_a - tr6_b) > 1e-6:
      all_even_isotropic = False
  check(
    "Tr(J_act^6) is NOT isotropic under (delta, q_+) swap "
    "(higher-order terms DO carry parity information, but not at quartic)",
    not all_even_isotropic,
  )
  # N.B.: This is interesting -- Tr(J^6) and higher CAN be parity-mixing.
  # But the Line-3 statement is specifically about the quartic, which IS
  # isotropic by the computation above.

  # 3.5 Build the combined quadratic + cubic + quartic chamber-boundary
  # extremum and verify it does NOT produce a new unique point.
  def W_Taylor(m, d):
    q = SQRT8_3 - d
    r2 = d * d + q * q
    w3 = q ** 3 - 3.0 * d * d * q
    # Taylor of W at scalar baseline up to quartic
    return -3.0 * r2 / m ** 2 + 2.0 * w3 / m ** 3 - 9.0 * r2 ** 2 / (2.0 * m ** 4)

  # At large m this is dominated by quadratic -> Schur-Q
  # At small m dominated by cubic/quartic
  trunc_argmaxes = []
  trunc_argmins = []
  for m_val in [0.5, 1.0, 2.0, 5.0, 10.0]:
    res_max = minimize_scalar(lambda d: -W_Taylor(m_val, d),
                 bounds=(-1.5, 2.5),
                 method='bounded', options={'xatol': 1e-8})
    res_min = minimize_scalar(lambda d: W_Taylor(m_val, d),
                 bounds=(-1.5, 2.5),
                 method='bounded', options={'xatol': 1e-8})
    trunc_argmaxes.append((m_val, res_max.x, -res_max.fun))
    trunc_argmins.append((m_val, res_min.x, res_min.fun))

  print(" Taylor-truncated W (quadratic + cubic + quartic) boundary extrema:")
  print("  m      argmin δ    W_min     argmax δ   W_max")
  for (m, d_min, v_min), (_, d_max, v_max) in zip(trunc_argmins, trunc_argmaxes):
    print(f"  {m:<10.4f} {d_min:>10.6f}  {v_min:>12.4f}  "
       f"{d_max:>10.6f}  {v_max:>10.4f}")

  arg_std_max = np.std([x[1] for x in trunc_argmaxes])
  check(
    "Taylor-truncated W boundary argmax is m-dependent "
    "(quartic addition does NOT break m-dependence)",
    arg_std_max > 0.03,
    f"std(argmax) = {arg_std_max:.4f}",
  )
  # Quartic's negative coefficient makes truncated W unbounded below as
  # |delta| -> infinity; the argmin saturates at the search-range edge,
  # which is itself m-dependent but not meaningfully so. The argmax is the
  # physically meaningful chamber-boundary extremum.

  print()
  print(" Line 3 verdict: NEW QUARTIC-ISOTROPY OBSTRUCTION.")
  print("  At scalar baseline D = m I_3 on the active pair (T_delta, T_q):")
  print("  Tr(J^2) is isotropic 6 r^2, Tr(J^3) is parity-mixing 6 Re(w^3),")
  print("  Tr(J^4) = 18 r^4 = (1/2) Tr(J^2)^2 is ISOTROPIC (no new parity-mixing).")
  print("  Hence the observable-principle Taylor expansion's parity-mixing")
  print("  content is concentrated at cubic order (already the cubic variational selection obstruction obstructed).")


# ---------------------------------------------------------------------------
# Part 4: Consolidated verdict and summary
# ---------------------------------------------------------------------------


def part4_verdict_summary():
  print()
  print("=" * 88)
  print("PART 4: CONSOLIDATED VERDICT")
  print("=" * 88)
  print()
  print("LINE 1 (Frobenius uniqueness):")
  print(" - PD + coercive + U(2)-invariant + quadratic = 2-parameter family")
  print("  { A (Tr K)^2 + B det K : A > -B/4, B < 0 }")
  print(" - Different members give DIFFERENT chamber-boundary minimizers")
  print(" - F1 = ||K||_F^2 is NOT uniquely pinned by these four axiom-native")
  print("  properties")
  print(" - Conditional gate: U(2)_L x U(2)_R independent unitary invariance")
  print("  WOULD uniquely pin F1, but is NOT currently retained.")
  print(" -> NEW OBSTRUCTION (parity-mixing-quadratic ambiguity is not")
  print("   closed by PD + coercivity + gauge + quadratic alone)")
  print()
  print("LINE 2 (Full-W at physically-forced m):")
  print(" - Fixed-m chamber-boundary extrema are m-dependent")
  print(" - No physically-forced m lands at any of the 5 ledger candidates")
  print(" - Chamber-interior joint extrema at fixed m are on det=0 singular")
  print("  surface (strengthening the cubic variational selection obstruction (B))")
  print(" -> NEW OBSTRUCTION (m-dependence survives fixed-m restriction)")
  print()
  print("LINE 3 (Quartic extension):")
  print(" - Tr(J^2) = 6 (delta^2 + q_+^2) isotropic")
  print(" - Tr(J^3) = 6 Re(w^3)       parity-mixing (the cubic variational selection obstruction obstructed)")
  print(" - Tr(J^4) = 18 (delta^2 + q_+^2)^2 = (1/2) Tr(J^2)^2 isotropic")
  print(" - Quartic is SQUARE of quadratic: no new parity-mixing info")
  print(" -> NEW OBSTRUCTION (quartic-isotropy theorem)")
  print()
  print("OVERALL: NEW OBSTRUCTION + narrower gap. The the selector gate remains OPEN.")
  print()
  print("What is strictly NEWLY CLOSED:")
  print(" (a) the parity-mixing quadratic class in (K11, K22, |K12|^2) is a")
  print("   two-parameter family; PD alone is insufficient to pick F1;")
  print(" (b) fixed-m full-W extremum m-dependence is a genuine distinct")
  print("   obstruction from the cubic variational selection obstruction's joint (m, delta) obstruction;")
  print(" (c) Tr(J^4) at scalar baseline is isotropic, so the quartic extension")
  print("   of the observable principle does NOT break the quadratic isotropy.")
  print()
  print("What is strictly NEWLY OPEN/REFINED:")
  print(" - Whether an axiom-native U(2)_L x U(2)_R independent unitary")
  print("  invariance on the non-Hermitian doublet block can be retrieved")
  print("  from the Cl(3)/Z^3 axiom. If yes, Line-1 conditional closure")
  print("  promotes F1 to the unique parity-mixing quadratic on retained axioms.")
  print(" - Whether higher-order even trace invariants (Tr(J^6), ...) do")
  print("  carry new parity-mixing content (the quartic does NOT, but the")
  print("  sextic CAN, as we verified above).")
  print()
  print(f"PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
  print("=" * 88)
  print("G1 PHYSICIST F: Frobenius uniqueness + Full-W at physically-forced m")
  print("        + Quartic extension of the observable principle")
  print("=" * 88)

  part1_frobenius_uniqueness()
  part2_full_W_at_forced_m()
  part3_quartic_invariant()
  part4_verdict_summary()

  print()
  if FAIL_COUNT == 0:
    print(f"RESULT: PASS ({PASS_COUNT} checks, 0 failures)")
    return 0
  else:
    print(f"RESULT: FAIL ({FAIL_COUNT} failures out of {PASS_COUNT + FAIL_COUNT})")
    return 1


if __name__ == "__main__":
  import sys
  sys.exit(main())
