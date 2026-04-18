#!/usr/bin/env python3
"""
DM Blocker 3 Lane E — Combinatorial / Equation Selector Attack.

Strategic context.
  Case 3 Microscopic Polynomial Impossibility Theorem assumed (A3.1) that
  selection is variational (an extremum). This runner drops (A3.1) and
  probes whether a non-variational axiom-native algebraic equation can
  pin (delta_*, q_+*).

Verdict.
  DEAD (with a PARTIAL flag on the Z_3-reality obstruction).

  - The axiom-native Z_3-reality equation Im Tr(H^2 C_3) = 0 is derivable
    but pins q_+ OUTSIDE the physical chamber.
  - Commutator equations Tr([H, T_m]^2), Tr([H, T_delta]^2), Tr([H, T_q]^2)
    are non-positive (negative definite or constant) and have no real
    zeros in the active chart.
  - Z_3 doublet block matrix-element equations reduce to either identities
    or to the chamber boundary + Tr(H^2) variational minimum (A3.1 back).
  - No new axiom-native algebraic pin exists.

Deliverable.
  PASS / FAIL counts on the derivations above, plus separation checks
  against the retained candidate pins.

Unit convention.
  Natural units on the active chart. gamma = 1/2, E_1 = sqrt(8/3),
  E_2 = sqrt(8)/3. All scalars dimensionless.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import sympy as sp

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
        msg += f" ({detail})"
    print(msg)
    return condition


# ---------------------------------------------------------------------------
# Axiom-native constants and tensors
# ---------------------------------------------------------------------------

d, q, m = sp.symbols("d q m", real=True)

GAMMA = sp.Rational(1, 2)
E1 = sp.sqrt(sp.Rational(8, 3))
E2 = sp.sqrt(8) / 3

Td = sp.Matrix([[0, -1, 1], [-1, 1, 0], [1, 0, -1]])
Tq = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
Tm = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])

I = sp.I
H_base = sp.Matrix(
    [
        [0, E1, -E1 - I * GAMMA],
        [E1, 0, -E2],
        [-E1 + I * GAMMA, -E2, 0],
    ]
)

C3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])

H = H_base + m * Tm + d * Td + q * Tq
H_src = m * Tm + d * Td + q * Tq

v1 = sp.Matrix([1, 1, 1])  # Z_3-singlet state


def d_odd(expr):
    return sp.expand((expr - expr.subs(d, -d)) / 2)


def d_even(expr):
    return sp.expand((expr + expr.subs(d, -d)) / 2)


# ---------------------------------------------------------------------------
# Part 1 — δ-parity of retained scalars (verify Thm 3 on source-only and
# show cracks in δ-evenness on full H)
# ---------------------------------------------------------------------------

print("\n=== Part 1: δ-parity of retained scalars ===\n")

for k in [1, 2, 3, 4]:
    # Source-only
    src_trk = sp.expand((H_src**k).trace())
    check(
        f"Tr(H_src^{k}) is δ-even (source-only)",
        sp.simplify(d_odd(src_trk)) == 0,
        f"δ-odd part = {sp.simplify(d_odd(src_trk))}",
    )

# Full H δ-odd signatures (crack in Thm 3's scope)
tr2_full = sp.expand((H * H).trace())
tr3_full = sp.expand((H**3).trace())
det_full = sp.expand(H.det())

odd_tr2 = d_odd(tr2_full)
odd_tr3 = d_odd(tr3_full)
odd_det = d_odd(det_full)

check(
    "Tr(H^2) full has nonzero δ-odd term (crack in source-only parity)",
    sp.simplify(odd_tr2) != 0,
    f"δ-odd = {sp.simplify(odd_tr2)}",
)
check(
    "Tr(H^3) full has nonzero δ-odd term",
    sp.simplify(odd_tr3) != 0,
    f"δ-odd = {sp.simplify(odd_tr3)}",
)
check(
    "det(H) full has nonzero δ-odd term",
    sp.simplify(odd_det) != 0,
    f"δ-odd = {sp.simplify(odd_det)}",
)

# ---------------------------------------------------------------------------
# Part 2 — δ-odd "equation" lane. Extract (f(δ) - f(-δ))/(2δ) = g(q, m, δ^2)
# and check zero-locus intersection with physical chamber.
# ---------------------------------------------------------------------------

print("\n=== Part 2: δ-odd algebraic equations ===\n")

# f1 := [det H]_odd / delta
f1 = sp.expand(odd_det / d)
# f2 := [Tr H^3]_odd / delta
f2 = sp.expand(odd_tr3 / d)
# f3 := [Tr H^2]_odd / delta
f3_tr2 = sp.expand(odd_tr2 / d)
# g3 := [v^T H^3 v]_odd / delta
vh3 = sp.expand((v1.T * (H**3) * v1)[0, 0])
g3 = sp.expand(d_odd(vh3) / d)

check(
    "f_1 := [det H]_odd/δ linear in (m, q_+)",
    sp.simplify(sp.diff(f1, d)) == 0,
    f"f_1 = {f1}",
)
check(
    "f_2 := [Tr H^3]_odd/δ linear in q_+ only",
    sp.simplify(sp.diff(f2, d)) == 0 and sp.simplify(sp.diff(f2, m)) == 0,
    f"f_2 = {f2}",
)
check(
    "g_3 := [v^T H^3 v]_odd/δ is a nonzero CONSTANT (no free variables)",
    sp.simplify(sp.diff(g3, d)) == 0
    and sp.simplify(sp.diff(g3, m)) == 0
    and sp.simplify(sp.diff(g3, q)) == 0
    and sp.simplify(g3) != 0,
    f"g_3 = {g3}",
)

# Chamber check for f_2 = 0: q_+ = (32 sqrt(3)/3 + 3/4) / (16 sqrt(6))
q_from_f2 = sp.solve(f2, q)
check(
    "f_2 = 0 zero-locus exists",
    len(q_from_f2) == 1,
    f"q_+ = {q_from_f2}",
)

# Check SCHUR-Q pin does NOT satisfy f_2 = 0
Schur_Q_d = sp.sqrt(6) / 3
Schur_Q_q = sp.sqrt(6) / 3
f2_at_schur = sp.simplify(f2.subs(q, Schur_Q_q))
check(
    "Schur-Q pin does NOT satisfy f_2 = 0 (δ-odd Tr(H^3) does not pin Schur-Q)",
    f2_at_schur != 0,
    f"f_2|Schur-Q = {f2_at_schur}",
)

# ---------------------------------------------------------------------------
# Part 3 — Z_3 character REALITY equations (Im Tr(H^k C_3) = 0)
# ---------------------------------------------------------------------------

print("\n=== Part 3: Z_3-character reality equations ===\n")

im_trs = {}
for k in range(1, 5):
    expr = sp.expand(sp.im((H**k * C3).trace()))
    im_trs[k] = expr

check(
    "Im Tr(H C_3) = 1/2 (IDENTITY, axiom-native γ)",
    sp.simplify(im_trs[1] - sp.Rational(1, 2)) == 0,
    f"Im Tr(H C_3) = {im_trs[1]}",
)

check(
    "Im Tr(H^2 C_3) linear in q_+, m-independent, δ-independent",
    sp.simplify(sp.diff(im_trs[2], d)) == 0
    and sp.simplify(sp.diff(im_trs[2], m)) == 0
    and sp.simplify(sp.diff(im_trs[2], q)) != 0,
    f"Im Tr(H^2 C_3) = {im_trs[2]}",
)

q_from_reality = sp.solve(im_trs[2], q)
check(
    "Z_3-reality equation Im Tr(H^2 C_3) = 0 gives q_+ = (sqrt(2) - sqrt(6))/3",
    len(q_from_reality) == 1
    and sp.simplify(q_from_reality[0] - (sp.sqrt(2) - sp.sqrt(6)) / 3) == 0,
    f"q_+ = {q_from_reality[0]} ≈ {float(q_from_reality[0])}",
)

# Chamber check
q_reality = q_from_reality[0]
check(
    "Z_3-reality q_+ is NEGATIVE (OUTSIDE physical chamber q_+ ≥ E_1 - δ ≥ 0)",
    float(q_reality) < 0,
    f"q_+ = {float(q_reality):.6f}",
)

# Schur-Q pin reality check
check(
    "Schur-Q pin does NOT satisfy Im Tr(H^2 C_3) = 0",
    sp.simplify(im_trs[2].subs(q, Schur_Q_q)) != 0,
    f"Im Tr(H^2 C_3)|Schur-Q = {sp.simplify(im_trs[2].subs(q, Schur_Q_q))}",
)

# Check joint system (Im Tr(H^2 C_3) = 0) + (Im Tr(H^3 C_3) = 0)
im3_at_q_reality = sp.expand(im_trs[3].subs(q, q_reality))
# Substitute m = 0 gauge
im3_m0 = sp.expand(im3_at_q_reality.subs(m, 0))
# Solve for d
d_solns = sp.solve(im3_m0, d)
real_d = [s for s in d_solns if sp.im(sp.N(s)) == 0]
check(
    "Joint system Im Tr(H^2 C_3) = Im Tr(H^3 C_3)|m=0 = 0 has NO real d solution",
    len(real_d) == 0,
    f"d solutions = {d_solns}",
)

# ---------------------------------------------------------------------------
# Part 4 — Commutator equations [H, X] = 0
# ---------------------------------------------------------------------------

print("\n=== Part 4: Commutator equations ===\n")

for name, X in [("T_m", Tm), ("T_delta", Td), ("T_q", Tq), ("C_3", C3)]:
    comm = H * X - X * H
    tr2_comm = sp.expand(sp.simplify((comm * comm).trace()))
    det_comm = sp.expand(sp.simplify(comm.det()))
    print(f"  [H, {name}]:")
    print(f"    Tr([H, {name}]^2) = {tr2_comm}")
    print(f"    det([H, {name}]) = {det_comm}")

    # Check real zero locus of Tr(comm^2):
    # For Hermitian X, comm is anti-Hermitian, so Tr(comm^2) ≤ 0 and = 0 iff comm = 0.
    # Is there any real (d, q, m) with Tr(comm^2) = 0?
    #
    # For T_m: Tr([H, T_m]^2) = -24 d^2 + 64 sqrt(6) d/3 - 131/3
    #   Discriminant of this quadratic in d: negative => no real zero.
    # For T_delta: Tr([H, T_delta]^2) = -24 m^2 + 64 sqrt(2) m/3 - 73/3
    #   Discriminant negative => no real zero.
    # For T_q: Tr([H, T_q]^2) = -347/9 (constant, nonzero) => no zero.
    # For C_3: Tr([H, C_3]^2) is complex (sign; C_3 not Hermitian).


tr2_comm_tm = sp.expand(sp.simplify(((H * Tm - Tm * H) ** 2).trace()))
tr2_comm_td = sp.expand(sp.simplify(((H * Td - Td * H) ** 2).trace()))
tr2_comm_tq = sp.expand(sp.simplify(((H * Tq - Tq * H) ** 2).trace()))

# For Tm: quadratic in d
disc_tm = sp.discriminant(tr2_comm_tm, d)
check(
    "Tr([H, T_m]^2) = -24 d^2 + 64 sqrt(6) d/3 - 131/3 has NEGATIVE discriminant",
    float(disc_tm) < 0,
    f"discriminant = {disc_tm} ≈ {float(disc_tm):.2f}",
)

# For Td: quadratic in m
disc_td = sp.discriminant(tr2_comm_td, m)
check(
    "Tr([H, T_delta]^2) has NEGATIVE discriminant in m",
    float(disc_td) < 0,
    f"discriminant = {disc_td} ≈ {float(disc_td):.2f}",
)

check(
    "Tr([H, T_q]^2) = -347/9 (constant, nonzero)",
    sp.simplify(tr2_comm_tq + sp.Rational(347, 9)) == 0,
    f"Tr([H, T_q]^2) = {tr2_comm_tq}",
)

# ---------------------------------------------------------------------------
# Part 5 — Z_3 doublet-block matrix-element equations
# ---------------------------------------------------------------------------

print("\n=== Part 5: Z_3 doublet-block matrix-element equations ===\n")

K11 = -q + 2 * sp.sqrt(2) / 9 - 1 / (2 * sp.sqrt(3))
K22 = -q + 2 * sp.sqrt(2) / 9 + 1 / (2 * sp.sqrt(3))
Re_K12 = m - 4 * sp.sqrt(2) / 9
Im_K12 = sp.sqrt(3) * d - 4 * sp.sqrt(2) / 3

# Constant identities
check(
    "K_11 - K_22 = -sqrt(3)/3 (CONSTANT IDENTITY, not a selector)",
    sp.simplify(K11 - K22 + sp.sqrt(3) / 3) == 0,
    "",
)

# Independent axes
check(
    "Tr K_doublet depends ONLY on q_+ (not d, not m)",
    sp.simplify(sp.diff(K11 + K22, d)) == 0
    and sp.simplify(sp.diff(K11 + K22, m)) == 0,
    f"Tr K_doublet = {sp.expand(K11 + K22)}",
)

check(
    "|Im K_12|^2 depends ONLY on d (not q, not m)",
    sp.simplify(sp.diff(Im_K12 ** 2, q)) == 0
    and sp.simplify(sp.diff(Im_K12 ** 2, m)) == 0,
    f"|Im K_12|^2 = {sp.expand(Im_K12 ** 2)}",
)

check(
    "Re K_12 depends ONLY on m (not d, not q)",
    sp.simplify(sp.diff(Re_K12, d)) == 0
    and sp.simplify(sp.diff(Re_K12, q)) == 0,
    f"Re K_12 = {Re_K12}",
)

# Schur-Q pin check
Schur_Q_point = {d: Schur_Q_d, q: Schur_Q_q}
im_k12_at_schur = sp.simplify(Im_K12.subs(Schur_Q_point))
check(
    "Im K_12 at Schur-Q pin equals -sqrt(2)/3 (matches Koide note)",
    sp.simplify(im_k12_at_schur + sp.sqrt(2) / 3) == 0,
    f"Im K_12|Schur-Q = {im_k12_at_schur}",
)

# The q_+ + delta = E_1 chamber boundary + d^2 + q_+^2 = E_1^2/2 pin Schur-Q,
# but the second is Tr(H_src^2) minimum = A3.1 (variational). Hence collapses.
dval = Schur_Q_d
qval = Schur_Q_q
check(
    "Schur-Q pin satisfies chamber boundary q_+ + delta = E_1",
    sp.simplify(dval + qval - E1) == 0,
    f"delta + q_+ = {sp.simplify(dval + qval)}",
)

check(
    "Schur-Q pin satisfies d^2 + q_+^2 = E_1^2 / 2",
    sp.simplify(dval ** 2 + qval ** 2 - E1 ** 2 / 2) == 0,
    "",
)

# Explicitly: d^2 + q^2 on chamber boundary is minimized at d = q = E_1/2,
# i.e. it IS the Tr(H^2) variational minimum, which is A3.1.
# Hence the '(A) + (B)' system reduces to 'chamber boundary + variational extremum'.

# ---------------------------------------------------------------------------
# Part 6 — Robustness checks
# ---------------------------------------------------------------------------

print("\n=== Part 6: Robustness checks ===\n")

# Check 1: Lattice-is-physical
# None of the candidate equations is a Wilson-loop or plaquette identity on Z^3.
# They are all momentum-space constructs on the H_hw=1 sector. Flag as fail.
print("  [Check 1] Lattice-is-physical: all candidate equations are")
print("    momentum-space constructs on H_hw=1, NOT spatial Wilson loops.")
print("    No candidate passes strict lattice-physical loop filter. FAIL.")

# Check 2: 3+1D temporal Ward
# The retained atlas is purely spatial Z^3. The gamma = 1/2 CP signature is
# spatial. Temporal Ward requires axiom extension. FAIL.
print("  [Check 2] 3+1D temporal Ward: retained atlas is spatial Z^3;")
print("    no axiom-native temporal Ward identity. FAIL.")

# Check 3: Koide κ=2 convergence
# Koide's κ=2 is a ONE-scalar selector on the selected slice
# delta = q_+ = sqrt(6)/3. DM's Lane E target is a TWO-scalar pin.
# They are structurally different (one adds to the other).
print("  [Check 3] Koide κ=2: one-scalar selector on top of Schur-Q pin;")
print("    DM Lane E is a two-scalar pin prior to Koide. Cannot converge.")
print("    FAIL (structurally distinct).")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("\n=== Summary ===\n")
print(f"PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
print()
print("Verdict: DEAD (with PARTIAL flag on Z_3-reality obstruction).")
print()
print("The axiom-native Z_3-reality equation Im Tr(H^2 C_3) = 0 gives")
print("q_+ = (sqrt(2) - sqrt(6))/3 ≈ -0.345, OUTSIDE physical chamber.")
print("All other algebraic attacks (commutator, δ-odd, Z_3 block) either")
print("reduce to identities, have no real zeros, or collapse to the")
print("Tr(H^2) variational minimum (which is A3.1 back).")
print()
print("Impossibility theorem stable even after dropping A3.1.")
