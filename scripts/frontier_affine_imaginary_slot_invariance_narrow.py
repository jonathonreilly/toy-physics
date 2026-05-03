#!/usr/bin/env python3
"""Pattern A narrow runner for `AFFINE_IMAGINARY_SLOT_INVARIANCE_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone Hermitian-matrix algebra identity:

  Let H_base be any Hermitian 3x3 matrix, and let
      T_m = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
      T_delta = [[0, -1, 1], [-1, 1, 0], [1, 0, -1]]
      T_q = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
  be three explicit REAL symmetric 3x3 matrices.

  Define the affine map
      H(m, delta, q_+)  =  H_base + m T_m + delta T_delta + q_+ T_q,
  with real parameters (m, delta, q_+).

  THEN:
    (i)   T_m, T_delta, T_q are each real symmetric (Hermitian).
    (ii)  T_m, T_delta, T_q are linearly independent over R.
    (iii) Tr(T_m) = 1, Tr(T_delta) = 0, Tr(T_q) = 0; hence
              Tr(H(m, delta, q_+))  =  Tr(H_base) + m
          depends ONLY on m (not on delta or q_+).
    (iv)  Im(H(m, delta, q_+)_{ij})  =  Im(H_base_{ij})
          for all (i, j) and all real (m, delta, q_+); the imaginary
          off-diagonal entries are independent of (m, delta, q_+)
          because T_m, T_delta, T_q are real matrices.
    (v)   In particular, if H_base = [[0, E1, -E1 - i gamma],
                                       [E1, 0, -E2],
                                       [-E1 + i gamma, -E2, 0]]
          with real E1, E2, gamma, then Im(H[0, 2]) = -gamma exact for
          all (m, delta, q_+).

This is class-A pure Hermitian-matrix algebra. No DM-neutrino source-
surface / half-plane / m-spectator / intrinsic-slot / slot-torsion
authority is consumed; the narrow theorem treats the three matrices as
explicit numerical inputs.

"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, simplify, symbols, Matrix, eye, zeros, im, re, I as sym_I
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: affine imaginary-slot invariance on Herm(3)")
# ============================================================================

# Define the three explicit real symmetric 3x3 matrices
T_m = Matrix([[1, 0, 0],
              [0, 0, 1],
              [0, 1, 0]])
T_delta = Matrix([[0, -1, 1],
                  [-1, 1, 0],
                  [1, 0, -1]])
T_q = Matrix([[0, 1, 1],
              [1, 0, 1],
              [1, 1, 0]])


# ----------------------------------------------------------------------------
section("Part 1: T_m, T_delta, T_q are real symmetric (Hermitian)")
# ----------------------------------------------------------------------------
for label, T in [("T_m", T_m), ("T_delta", T_delta), ("T_q", T_q)]:
    check(f"{label} is real symmetric (T = T^T)",
          T == T.T)
    # All entries real (no imaginary parts)
    all_real = all(im(T[i, j]) == 0 for i in range(3) for j in range(3))
    check(f"{label} has all real entries (no imaginary part)",
          all_real)


# ----------------------------------------------------------------------------
section("Part 2: T_m, T_delta, T_q are linearly independent over R")
# ----------------------------------------------------------------------------
# Stack as 9-dim vectors and compute the rank.
def flatten(M):
    return [M[i, j] for i in range(3) for j in range(3)]

vecs = Matrix([flatten(T_m), flatten(T_delta), flatten(T_q)])
rank = vecs.rank()
check("rank({T_m, T_delta, T_q}) = 3 (linearly independent)",
      rank == 3,
      detail=f"rank = {rank}")


# ----------------------------------------------------------------------------
section("Part 3: trace structure - Tr(T_m) = 1, Tr(T_delta) = 0, Tr(T_q) = 0")
# ----------------------------------------------------------------------------
check("Tr(T_m) = 1 exact",
      T_m.trace() == 1,
      detail=f"Tr(T_m) = {T_m.trace()}")
check("Tr(T_delta) = 0 exact (0 + 1 + (-1))",
      T_delta.trace() == 0,
      detail=f"Tr(T_delta) = {T_delta.trace()}")
check("Tr(T_q) = 0 exact (0 + 0 + 0)",
      T_q.trace() == 0,
      detail=f"Tr(T_q) = {T_q.trace()}")


# ----------------------------------------------------------------------------
section("Part 4: Tr(H(m, delta, q_+)) = Tr(H_base) + m (depends only on m)")
# ----------------------------------------------------------------------------
m_sym, delta_sym, q_sym = symbols('m delta q_+', real=True)
H_base_entries = symbols('h_00 h_01 h_02 h_10 h_11 h_12 h_20 h_21 h_22', complex=True)
H_base = Matrix([
    [H_base_entries[0], H_base_entries[1], H_base_entries[2]],
    [H_base_entries[3], H_base_entries[4], H_base_entries[5]],
    [H_base_entries[6], H_base_entries[7], H_base_entries[8]],
])

H = H_base + m_sym * T_m + delta_sym * T_delta + q_sym * T_q
trace_H = simplify(H.trace())
trace_H_base = H_base.trace()
expected_trace = trace_H_base + m_sym
check("Tr(H) = Tr(H_base) + m (independent of delta, q_+)",
      simplify(trace_H - expected_trace) == 0,
      detail=f"Tr(H) - Tr(H_base) - m = {simplify(trace_H - expected_trace)}")


# ----------------------------------------------------------------------------
section("Part 5: imaginary-slot invariance Im(H_ij) = Im(H_base_ij) for all i, j")
# ----------------------------------------------------------------------------
# Since T_m, T_delta, T_q are real, the imaginary part of H is the imaginary
# part of H_base, independent of (m, delta, q_+).
for i in range(3):
    for j in range(3):
        H_ij_imag = simplify(im(H[i, j]))
        H_base_ij_imag = simplify(im(H_base[i, j]))
        check(f"Im(H[{i},{j}]) = Im(H_base[{i},{j}]) for all (m, delta, q_+)",
              simplify(H_ij_imag - H_base_ij_imag) == 0)


# ----------------------------------------------------------------------------
section("Part 6: framework instance with H_base = parent's specified matrix")
# ----------------------------------------------------------------------------
# H_base = [[0, E1, -E1 - i gamma],
#           [E1, 0, -E2],
#           [-E1 + i gamma, -E2, 0]]
# with gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3 (real values).
gamma_val = Rational(1, 2)
E1_val = sympy.sqrt(Rational(8, 3))
E2_val = sympy.sqrt(Rational(8)) / 3

H_base_fw = Matrix([
    [0, E1_val, -E1_val - sym_I * gamma_val],
    [E1_val, 0, -E2_val],
    [-E1_val + sym_I * gamma_val, -E2_val, 0],
])

# Check H_base_fw is Hermitian
H_base_fw_dagger = H_base_fw.H
check("framework H_base is Hermitian (H_base = H_base^dagger)",
      simplify(H_base_fw - H_base_fw_dagger) == zeros(3, 3))

H_fw = H_base_fw + m_sym * T_m + delta_sym * T_delta + q_sym * T_q

# Im(H_fw[0, 2]) = -gamma exact for all (m, delta, q_+)
H_fw_02_imag = simplify(im(H_fw[0, 2]))
check("Im(H[0, 2]) = -gamma = -1/2 exact at framework instance for all (m, delta, q_+)",
      simplify(H_fw_02_imag - (-gamma_val)) == 0,
      detail=f"Im(H[0, 2]) = {H_fw_02_imag}")

# Verify Tr(H_fw) = Tr(H_base_fw) + m = 0 + m = m
trace_fw = simplify(H_fw.trace())
check("Tr(H) = m exact at framework instance (Tr(H_base) = 0 + m)",
      simplify(trace_fw - m_sym) == 0,
      detail=f"Tr(H) = {trace_fw}")


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let H_base be any Hermitian 3x3 matrix, and let T_m, T_delta, T_q
    be the three explicit REAL symmetric 3x3 matrices given by:
        T_m = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
        T_delta = [[0, -1, 1], [-1, 1, 0], [1, 0, -1]]
        T_q = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    Define the affine map
        H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q
    with real parameters (m, delta, q_+).

  CONCLUSION:
    (i)   T_m, T_delta, T_q are real symmetric (Hermitian) and linearly
          independent over R.
    (ii)  Tr(H) = Tr(H_base) + m (depends only on m).
    (iii) Im(H_ij) = Im(H_base_ij) for all (i, j) (imaginary off-
          diagonal entries are independent of (m, delta, q_+) because
          T_m, T_delta, T_q are real matrices).
    (iv)  At the framework instance H_base with imaginary slot
          (-gamma) at position [0, 2] and gamma = 1/2:
              Im(H[0, 2]) = -1/2 exact for all (m, delta, q_+);
              Tr(H) = m exact (Tr(H_base) = 0).

  Audit-lane class:
    (A) — pure Hermitian-matrix algebra. No DM-neutrino source-surface
    authority. The framework instance is one application case; the
    algebra closes for any (H_base, m, delta, q_+).

  This narrow theorem drops the parent's five upstream DM-neutrino
  source-surface deps (active-half-plane, m-spectator, intrinsic-slot,
  slot-torsion-boundary).
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
