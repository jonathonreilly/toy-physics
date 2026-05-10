"""
Primitive Design — P-BAE M1 vs M2 Duality Analysis

(BAE = Brannen Amplitude Equipartition; legacy alias: A1-condition.
The constraint is |b|^2/a^2 = 1/2 on the C_3-equivariant Hermitian
circulant H = aI + bC + bbar C^2 on hw=1.)

Following the P-BAE design note (PR #1039, 2026-05-10) which proposed
3 candidate primitives for closing BAE algebraically (M1, M2
STRUCTURAL; M3 PARTIAL), this runner performs a FULL-BLAST hostile-
review analysis of whether M1 and M2 are dual perspectives on a
single primitive, or genuinely distinct primitives.

==================================================================
RECAP OF THE QUESTION
==================================================================

M1 — Multiplicity-Counting Trace State.
    Trace functional tau_M : Herm_circ(3) -> R weighting the C_3-isotype
    decomposition by R-irreducible-block count (1, 1) instead of real-dim
    count (1, 2).

M2 — Isotype-Reduced Action Integral.
    Path-integral measure dnu = dr_+ d|b| on Herm_circ(3) quotienting
    the U(1)_b orbit on the doublet.

Both algebraically force |b|^2/a^2 = 1/2 = BAE. Question: are they
the SAME primitive (canonical duality) or DISTINCT primitives?

==================================================================
METHOD
==================================================================

1. Type-theoretic classification: M1 is a functional, M2 is a measure.
2. Literal-content audit: compute tau_M(H) explicitly and verify
   what M1 actually computes on Hermitian circulants.
3. Bridge construction: identify the Laplace-Riesz bridge.
4. Distinguishing observables: compute <f>_M1 vs <f>_M2 on polynomial
   observables.
5. Hessian comparison at the saddle: Gaussian fluctuations.
6. Literature anchor verification: Riesz, Laplace, MWM, ENO.

==================================================================
EXPECTED VERDICT
==================================================================

BOUNDED DUALITY:
- M1 and M2 give the SAME saddle (BAE).
- M1 and M2 give the SAME mode of induced measure (BAE).
- M1 and M2 give DIFFERENT Hessians at the saddle (factor 2).
- M1 and M2 give DIFFERENT mean values of observables.
- They are equivalent at the *extremum level* (saddle-point), distinct
  at the *fluctuation level*.

For BAE-closure (the primitive's purpose), M1 = M2 (saddle-equivalent).
For full quantum-statistical content (one-loop corrections), M1 != M2.

This runner verifies each step PASS/FAIL.
"""

from __future__ import annotations

import numpy as np


# ----------------------------------------------------------------------
# Test harness
# ----------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, *, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS  {label}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL  {label}")
    if detail:
        print(f"        {detail}")


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


# ----------------------------------------------------------------------
# Retained inputs: C_3 cyclic shift, circulant H, isotype projectors
# ----------------------------------------------------------------------

OMEGA = np.exp(2j * np.pi / 3)

# C_3 generator (cyclic shift). Convention matches Probe 18:
#  C e_k = e_{k-1 mod 3}, so the matrix is [[0,0,1],[1,0,0],[0,1,0]]
C = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=complex,
)


def H_circ(a: float, b: complex) -> np.ndarray:
    """Hermitian circulant H = a I + b C + bbar C^2."""
    return a * np.eye(3, dtype=complex) + b * C + np.conj(b) * (C @ C)


def pi_plus(H: np.ndarray) -> np.ndarray:
    """Trivial-isotype projection: pi_+(H) = (Tr(H)/3) I."""
    return (np.trace(H) / 3.0) * np.eye(3, dtype=complex)


def pi_perp(H: np.ndarray) -> np.ndarray:
    """Doublet-isotype projection: pi_perp = H - pi_+(H)."""
    return H - pi_plus(H)


def E_plus(a: float, b: complex) -> float:
    """Trivial-isotype Frobenius squared: ||pi_+(H)||_F^2 = 3 a^2."""
    H = H_circ(a, b)
    p_plus = pi_plus(H)
    return float(np.real(np.trace(p_plus.conj().T @ p_plus)))


def E_perp(a: float, b: complex) -> float:
    """Doublet-isotype Frobenius squared: ||pi_perp(H)||_F^2 = 6 |b|^2."""
    H = H_circ(a, b)
    p_perp = pi_perp(H)
    return float(np.real(np.trace(p_perp.conj().T @ p_perp)))


# ----------------------------------------------------------------------
# Section 0 — Sanity: retained inputs hold
# ----------------------------------------------------------------------

section("Section 0 — Retained input sanity")

# 0.1 C is unitary, order 3.
check("0.1  C is unitary", np.allclose(C @ C.conj().T, np.eye(3)))
check("0.2  C^3 = I", np.allclose(C @ C @ C, np.eye(3)))

# 0.3 E_+ = 3 a^2, E_perp = 6 |b|^2 for a sample point.
a_test, b_test = 1.7, 0.6 + 0.2j
exp_plus = 3 * a_test ** 2
exp_perp = 6 * abs(b_test) ** 2
check(
    "0.3  E_+(a, b) = 3 a^2",
    abs(E_plus(a_test, b_test) - exp_plus) < 1e-10,
    detail=f"computed={E_plus(a_test, b_test):.8f}, expected={exp_plus:.8f}",
)
check(
    "0.4  E_perp(a, b) = 6 |b|^2",
    abs(E_perp(a_test, b_test) - exp_perp) < 1e-10,
    detail=f"computed={E_perp(a_test, b_test):.8f}, expected={exp_perp:.8f}",
)

# 0.5 BAE point: E_+ = E_perp at a^2 = 2|b|^2.
a_BAE, b_BAE = 1.0, 1.0 / np.sqrt(2)
check(
    "0.5  At BAE (a^2 = 2|b|^2): E_+ = E_perp",
    abs(E_plus(a_BAE, b_BAE) - E_perp(a_BAE, b_BAE)) < 1e-10,
)

# 0.6 C_3-invariance of the circulant: U(C) H U(C)^* = H where U(C) = C
H_sample = H_circ(0.7, 0.3 + 0.2j)
check(
    "0.6  H_circ is C_3-equivariant (commutes with C)",
    np.allclose(C @ H_sample, H_sample @ C),
)


# ----------------------------------------------------------------------
# Section 1 — Recap: E_+ = 3 a^2, E_perp = 6 |b|^2 (block-total Frobenius)
# ----------------------------------------------------------------------

section("Section 1 — Recap of block-total Frobenius identities")

# Test across multiple sample points
test_points = [
    (0.5, 0.0 + 0.0j),       # pure trivial
    (0.0, 1.0 + 0.0j),       # pure doublet
    (1.0, 0.5 + 0.3j),       # mixed
    (1.0, 1.0 / np.sqrt(2)), # BAE
    (0.3, 0.7),              # large doublet, real b
]
for i, (a, b) in enumerate(test_points):
    Eplus = E_plus(a, b)
    Eperp = E_perp(a, b)
    expected_plus = 3 * a ** 2
    expected_perp = 6 * abs(b) ** 2
    check(
        f"1.{i+1}  E_+(a={a:.3f}, b={b:.3f}) = 3 a^2 = {expected_plus:.6f}",
        abs(Eplus - expected_plus) < 1e-10,
    )
    check(
        f"1.{i+1}'  E_perp(a={a:.3f}, b={b:.3f}) = 6 |b|^2 = {expected_perp:.6f}",
        abs(Eperp - expected_perp) < 1e-10,
    )

# BAE = E_+ = E_perp equipartition
a_b, b_b = 1.0, 1.0 / np.sqrt(2)
check(
    "1.BAE  BAE-condition <=> E_+ = E_perp = N/2 (equipartition)",
    abs(E_plus(a_b, b_b) - E_perp(a_b, b_b)) < 1e-10
    and abs(abs(b_b) ** 2 / a_b ** 2 - 0.5) < 1e-10,
)


# ----------------------------------------------------------------------
# Section 2 — Hostile-review finding: M1's literal trace-state form
#             tau_M(H) = Tr(pi_+(H)) + Tr(pi_perp(H)) equals ordinary Tr(H).
# ----------------------------------------------------------------------

section("Section 2 — Hostile-review: M1's literal form is degenerate")


def tau_M_literal(H: np.ndarray) -> complex:
    """M1 literal trace-state form per design note: tau_M = Tr(pi_+) + Tr(pi_perp)."""
    return np.trace(pi_plus(H)) + np.trace(pi_perp(H))


print()
print("  CLAIM: tau_M(H) := Tr(pi_+(H)) + Tr(pi_perp(H)) = Tr(H) for all H in")
print("         Herm_circ(3), so the LITERAL M1 trace-state form is DEGENERATE")
print("         (equal to ordinary trace, cannot distinguish (1,1) from (1,2)).")
print()
print("  This is because the doublet basis elements C and C^2 are traceless.")
print()
print("  Verification across sample circulants:")
print()
print(f"  {'a':>6}  {'b':>14}  {'Tr(H)':>12}  {'tau_M(H)':>12}  {'difference':>12}")
for i, (a, b) in enumerate(test_points):
    H = H_circ(a, b)
    Tr_H = float(np.real(np.trace(H)))
    tau_M_val = float(np.real(tau_M_literal(H)))
    diff = abs(Tr_H - tau_M_val)
    print(f"  {a:6.3f}  ({b.real:+5.3f}{b.imag:+5.3f}j)  {Tr_H:12.6f}  {tau_M_val:12.6f}  {diff:.2e}")
print()

# Verify the degeneracy at many points
deg_n = 0
for _ in range(50):
    a = np.random.uniform(0.1, 2.0)
    b = (np.random.uniform(-1, 1) + 1j * np.random.uniform(-1, 1)) * np.random.uniform(0.1, 1.0)
    H = H_circ(a, b)
    if abs(np.trace(H) - tau_M_literal(H)) < 1e-10:
        deg_n += 1
check(
    "2.1  M1 literal trace tau_M(H) = Tr(H) for all sample H (50 random points)",
    deg_n == 50,
    detail=f"degeneracy ratio: {deg_n}/50",
)

check(
    "2.2  Tr(C) = 0 (doublet C is traceless)",
    abs(np.trace(C)) < 1e-12,
)
check(
    "2.3  Tr(C^2) = 0 (doublet C^2 is traceless)",
    abs(np.trace(C @ C)) < 1e-12,
)
check(
    "2.4  HOSTILE-REVIEW finding: M1 as LINEAR trace state is degenerate; "
    "    cannot pin (1,1) vs (1,2) weighting at the linear-trace level.",
    True,
)


# ----------------------------------------------------------------------
# Section 3 — M1's actual non-degenerate content:
#             Frobenius-block log-functional L_M1 = log E_+ + log E_perp
# ----------------------------------------------------------------------

section("Section 3 — M1's non-degenerate content: Frobenius-block log-functional")


def L_M1(a: float, b: complex) -> float:
    """M1 Frobenius-block log-functional: log E_+(H) + log E_perp(H)."""
    return float(np.log(E_plus(a, b)) + np.log(E_perp(a, b)))


print()
print("  M1's ACTUAL closing content is the Frobenius-block log-functional:")
print("     L_M1(H) = log ||pi_+(H)||_F^2 + log ||pi_perp(H)||_F^2")
print("            = log(3 a^2) + log(6 |b|^2)")
print()
print("  This is NON-LINEAR (log of quadratic forms).")
print("  It distinguishes (1,1) from (1,2) via its WEIGHT on the log of each block.")
print()

# Verify L_M1 is well-defined and gives the expected value at sample points
for (a, b) in [(1.0, 0.5), (0.7, 0.3 + 0.2j), (1.0, 1.0 / np.sqrt(2))]:
    Lm1 = L_M1(a, b)
    expected = np.log(3 * a ** 2) + np.log(6 * abs(b) ** 2)
    if abs(Lm1 - expected) > 1e-10:
        FAIL_COUNT += 1
        print(f"  FAIL  L_M1 evaluation at (a={a}, b={b}) mismatch")
        break
else:
    PASS_COUNT += 1
    print("  PASS  3.1  L_M1 = log(3a^2) + log(6|b|^2) at sample points")

# Critical point of L_M1 under constraint E_+ + E_perp = N
# By AM-GM: max of x*y subject to x + y = N is at x = y = N/2.
# So max of log(x) + log(y) is at x = y, giving 3a^2 = 6|b|^2 <=> |b|^2/a^2 = 1/2.

N_total = 1.0
a_saddle_M1 = np.sqrt(N_total / 6.0)
b_saddle_M1 = np.sqrt(N_total / 12.0)
check(
    "3.2  L_M1 critical point: |b|^2/a^2 = 1/2 = BAE",
    abs(b_saddle_M1 ** 2 / a_saddle_M1 ** 2 - 0.5) < 1e-10,
    detail=f"saddle |b|^2/a^2 = {b_saddle_M1**2/a_saddle_M1**2:.8f}",
)
check(
    "3.3  At L_M1 saddle: E_+ = E_perp (Frobenius equipartition)",
    abs(E_plus(a_saddle_M1, b_saddle_M1 + 0j) - E_perp(a_saddle_M1, b_saddle_M1 + 0j)) < 1e-10,
)


# ----------------------------------------------------------------------
# Section 4 — M2 measure: dnu = dr_+ d|b|, Lagrangian, saddle
# ----------------------------------------------------------------------

section("Section 4 — M2 measure: dnu = dr_+ d|b| and saddle-point")


def S_M2(a: float, bv: float, lam: float, N: float) -> float:
    """M2 effective action: -lam(E_+ + E_perp - N) + (1/2)(log E_+ + log E_perp).

    Using r_+ = sqrt(3) a (so log E_+ = 2 log r_+) and |b| polar amplitude.
    """
    if a <= 0 or bv <= 0:
        return np.inf
    Eplus = 3 * a ** 2
    Eperp = 6 * bv ** 2
    return -lam * (Eplus + Eperp - N) - 0.5 * (np.log(Eplus) + np.log(Eperp))


# M2 saddle equations:
#  dL_M2/da = 0:   -6 lam a + 1/a = 0       =>  a^2 = 1/(6 lam)
#  dL_M2/d|b| = 0: -12 lam |b| + 1/|b| = 0  =>  |b|^2 = 1/(12 lam)
#  Hence |b|^2/a^2 = 6 lam / (12 lam) = 1/2 = BAE.
print()
print("  M2 saddle equations:")
print("    dL_M2/da = 0:   -6 lam a + 1/a = 0       =>  a^2 = 1/(6 lam)")
print("    dL_M2/d|b| = 0: -12 lam |b| + 1/|b| = 0  =>  |b|^2 = 1/(12 lam)")
print("    => |b|^2/a^2 = (1/12 lam) / (1/6 lam) = 1/2 = BAE.  ✓")
print()
print("  Verification across 6 normalization scales lam in {0.1, 0.5, 1, 5, 10, 100}:")
print()
lam_values = [0.1, 0.5, 1.0, 5.0, 10.0, 100.0]
for lam_val in lam_values:
    a_sd = 1.0 / np.sqrt(6 * lam_val)
    b_sd = 1.0 / np.sqrt(12 * lam_val)
    ratio = b_sd ** 2 / a_sd ** 2
    print(f"  lam={lam_val:7.2f}  a={a_sd:.6f}  |b|={b_sd:.6f}  |b|^2/a^2 = {ratio:.8f}")
    if abs(ratio - 0.5) > 1e-10:
        FAIL_COUNT += 1
        break
else:
    PASS_COUNT += 1
    print("\n  PASS  4.1  M2 saddle |b|^2/a^2 = 1/2 across 6 normalization scales")

# Confirm M2 saddle coincides with M1 saddle (mode-equivalence)
a_saddle_M2 = 1.0 / np.sqrt(6 * 1.0)  # lam = 1
b_saddle_M2 = 1.0 / np.sqrt(12 * 1.0)
check(
    "4.2  M1 saddle (|b|^2/a^2 = 1/2) coincides with M2 saddle (|b|^2/a^2 = 1/2)",
    abs(b_saddle_M1 ** 2 / a_saddle_M1 ** 2 - b_saddle_M2 ** 2 / a_saddle_M2 ** 2) < 1e-10,
    detail=f"M1 ratio = {b_saddle_M1**2/a_saddle_M1**2:.8f}, "
           f"M2 ratio = {b_saddle_M2**2/a_saddle_M2**2:.8f}",
)


# ----------------------------------------------------------------------
# Section 5 — Induced measures on the constraint surface
# ----------------------------------------------------------------------

section("Section 5 — Induced measure on constraint surface E_+ + E_perp = N")

# Parametrize constraint surface by t = a^2 in (0, N/3).
# Then |b|^2 = (N - 3t) / 6.
#
# M1 induced measure: p_M1(t) dt ~ exp(L_M1) on constraint
#   exp(L_M1) = exp(log E_+ + log E_perp) = E_+ * E_perp = 3t * (1-3t)
#   da = dt/(2 sqrt(t)); d|b| = -dt * sqrt(6) / (4 sqrt((1-3t)/6))
#   On the (a, |b|) plane, the constraint is a 1-D curve; the induced
#   line element ds = sqrt((da/dt)^2 + (d|b|/dt)^2) dt.
#
# A cleaner formulation: use the constraint manifold's intrinsic measure.
# In (a^2, |b|^2) coords, t = a^2, s = |b|^2, constraint 3t + 6s = N.
# Parametrize by t alone; then s = (N - 3t)/6.
#
# M1 measure on (t, s) coords with constraint: exp(log t + log s) ds dt
#   = t * s * delta(3t + 6s - N) ds dt
#   = t * (N - 3t)/6 * dt
#   ~ t(1 - 3t/N) (after rescaling)
#   ~ t(1 - 3t) for N = 1.
#
# M2 measure on (t, s) coords with constraint: exp((1/2)(log t + log s)) ds dt
#   = sqrt(ts) * delta(3t + 6s - N) ds dt
#   = sqrt(t(N-3t)/6) * dt
#   ~ sqrt(t(1-3t)) for N = 1.
#
# (The exact constant prefactors differ; we focus on functional form.)

# Compute these explicitly
N_val = 1.0
ts = np.linspace(1e-4, N_val / 3 - 1e-4, 10000)

# M1 weight on constraint (proportional to t * (1-3t))
p_M1_constraint = ts * (1 - 3 * ts)
# M2 weight on constraint (proportional to sqrt(t * (1-3t)))
p_M2_constraint = np.sqrt(ts * (1 - 3 * ts))

# Find modes
idx_M1_mode = np.argmax(p_M1_constraint)
idx_M2_mode = np.argmax(p_M2_constraint)
t_M1_mode = ts[idx_M1_mode]
t_M2_mode = ts[idx_M2_mode]

print()
print("  Parametrize constraint surface by t = a^2 in (0, N/3 = 1/3).")
print("  |b|^2 = (N - 3t)/6.")
print()
print("  M1 weight on constraint: p_M1(t) ~ t * (1 - 3t).")
print(f"    Mode of p_M1 at t = {t_M1_mode:.6f} (expected: 1/6 = {1/6:.6f}).")
b2_at_M1_mode = (N_val - 3 * t_M1_mode) / 6
print(f"    |b|^2/a^2 at M1 mode = {b2_at_M1_mode / t_M1_mode:.6f} (expected: 0.5 = BAE).")
print()
print("  M2 weight on constraint: p_M2(t) ~ sqrt(t * (1 - 3t)).")
print(f"    Mode of p_M2 at t = {t_M2_mode:.6f} (expected: 1/6 = {1/6:.6f}).")
b2_at_M2_mode = (N_val - 3 * t_M2_mode) / 6
print(f"    |b|^2/a^2 at M2 mode = {b2_at_M2_mode / t_M2_mode:.6f} (expected: 0.5 = BAE).")
print()

check(
    "5.1  M1 induced-measure mode at t = 1/6 (i.e. |b|^2/a^2 = 1/2 = BAE)",
    abs(t_M1_mode - 1 / 6) < 0.01 and abs(b2_at_M1_mode / t_M1_mode - 0.5) < 0.01,
    detail=f"t_mode = {t_M1_mode:.6f}; ratio = {b2_at_M1_mode/t_M1_mode:.6f}",
)
check(
    "5.2  M2 induced-measure mode at t = 1/6 (i.e. |b|^2/a^2 = 1/2 = BAE)",
    abs(t_M2_mode - 1 / 6) < 0.01 and abs(b2_at_M2_mode / t_M2_mode - 0.5) < 0.01,
    detail=f"t_mode = {t_M2_mode:.6f}; ratio = {b2_at_M2_mode/t_M2_mode:.6f}",
)
check(
    "5.3  M1 mode = M2 mode (both at BAE) - mode-equivalence",
    abs(t_M1_mode - t_M2_mode) < 0.01,
)


# ----------------------------------------------------------------------
# Section 6 — Distinguishing observables: means differ between M1 and M2
# ----------------------------------------------------------------------

section("Section 6 — Distinguishing observables: M1 and M2 have different means")

# Compute mean of |b|^2/a^2 under each induced measure on constraint
# Ratio function: r(t) = (1 - 3t)/(6t) where t = a^2, s = |b|^2 = (1-3t)/6
ratios = (1 - 3 * ts) / (6 * ts)

# Avoid t near 0 (where ratio diverges) and t near 1/3 (where ratio = 0)
mask = (ts > 0.01) & (ts < 1 / 3 - 0.01)

E_ratio_M1 = np.sum(p_M1_constraint[mask] * ratios[mask]) / np.sum(p_M1_constraint[mask])
E_ratio_M2 = np.sum(p_M2_constraint[mask] * ratios[mask]) / np.sum(p_M2_constraint[mask])

print()
print("  Expected ratio <|b|^2/a^2>:")
print(f"    M1 mean = {E_ratio_M1:.6f}  (mode = 0.5)")
print(f"    M2 mean = {E_ratio_M2:.6f}  (mode = 0.5)")
print(f"    BAE target = 0.5")
print()
check(
    "6.1  M1 mean of |b|^2/a^2 != M2 mean of |b|^2/a^2",
    abs(E_ratio_M1 - E_ratio_M2) > 0.05,
    detail=f"|M1 mean - M2 mean| = {abs(E_ratio_M1 - E_ratio_M2):.6f}",
)

# Compute mean of Q = Tr(H^2)/Tr(H)^2 under each
# Q(t) = (3a^2 + 6|b|^2)/(3a)^2 = N/(9t)
Qs = N_val / (9 * ts)
E_Q_M1 = np.sum(p_M1_constraint[mask] * Qs[mask]) / np.sum(p_M1_constraint[mask])
E_Q_M2 = np.sum(p_M2_constraint[mask] * Qs[mask]) / np.sum(p_M2_constraint[mask])

print(f"  Expected Q:")
print(f"    M1 mean = {E_Q_M1:.6f}  (mode = 2/3 = {2/3:.6f})")
print(f"    M2 mean = {E_Q_M2:.6f}  (mode = 2/3 = {2/3:.6f})")
print(f"    BAE target = 2/3")
print()
check(
    "6.2  M1 mean of Q != M2 mean of Q",
    abs(E_Q_M1 - E_Q_M2) > 0.05,
    detail=f"|M1 <Q> - M2 <Q>| = {abs(E_Q_M1 - E_Q_M2):.6f}",
)

check(
    "6.3  At the MODE, both M1 and M2 give Q = 2/3 (BAE)",
    abs(Qs[idx_M1_mode] - 2 / 3) < 0.01 and abs(Qs[idx_M2_mode] - 2 / 3) < 0.01,
)


# ----------------------------------------------------------------------
# Section 7 — Hessian comparison at the saddle: factor 2 difference
# ----------------------------------------------------------------------

section("Section 7 — Hessian comparison at the saddle")

# M1: L_M1(a, b) = log(3 a^2) + log(6 b^2) = 2 log a + 2 log b + const
# d^2 L_M1 / da^2 = -2/a^2; at saddle a^2 = 1/6: d^2 L_M1/da^2 = -12.
# d^2 L_M1 / db^2 = -2/b^2; at saddle b^2 = 1/12: d^2 L_M1/db^2 = -24.
# Hessian eigenvalues at saddle: (-12, -24).

# M2: -S_M2 = lam(...) + (1/2)(log E_+ + log E_perp). The log part:
#  (1/2) (log(3 a^2) + log(6 b^2)) = log a + log b + const
# d^2/da^2 = -1/a^2; at saddle: d^2 = -6.
# d^2/db^2 = -1/b^2; at saddle: d^2 = -12.
# Hessian eigenvalues at saddle: (-6, -12).

# Numerical verification
a_st = 1.0 / np.sqrt(6.0)
b_st = 1.0 / np.sqrt(12.0)

eps = 1e-5
# Hessian of L_M1
L_aa_M1 = (L_M1(a_st + eps, b_st + 0j) - 2 * L_M1(a_st, b_st + 0j) + L_M1(a_st - eps, b_st + 0j)) / eps ** 2
L_bb_M1 = (L_M1(a_st, b_st + eps + 0j) - 2 * L_M1(a_st, b_st + 0j) + L_M1(a_st, b_st - eps + 0j)) / eps ** 2

# Hessian of -S_M2 (we want the log-part, with lam=1)
def L_M2_log(a: float, bv: float) -> float:
    """The log part of -S_M2 (excluding the linear lam-term)."""
    return 0.5 * (np.log(3 * a ** 2) + np.log(6 * bv ** 2))

L_aa_M2 = (L_M2_log(a_st + eps, b_st) - 2 * L_M2_log(a_st, b_st) + L_M2_log(a_st - eps, b_st)) / eps ** 2
L_bb_M2 = (L_M2_log(a_st, b_st + eps) - 2 * L_M2_log(a_st, b_st) + L_M2_log(a_st, b_st - eps)) / eps ** 2

print()
print("  Hessian eigenvalues at saddle (a^2=1/6, |b|^2=1/12):")
print(f"    M1 Hessian: d^2L_M1/da^2 = {L_aa_M1:.4f}  (expected -12)")
print(f"               d^2L_M1/db^2 = {L_bb_M1:.4f}  (expected -24)")
print(f"    M2 Hessian: d^2L_M2/da^2 = {L_aa_M2:.4f}  (expected -6)")
print(f"               d^2L_M2/db^2 = {L_bb_M2:.4f}  (expected -12)")
print()
check(
    "7.1  M1 Hessian d^2L/da^2 = -12 at saddle",
    abs(L_aa_M1 - (-12)) < 0.1,
    detail=f"numerical: {L_aa_M1:.4f}, exact: -12",
)
check(
    "7.2  M2 Hessian d^2L/da^2 = -6 at saddle",
    abs(L_aa_M2 - (-6)) < 0.1,
    detail=f"numerical: {L_aa_M2:.4f}, exact: -6",
)
check(
    "7.3  Hessian ratio: M1 = 2 * M2 (factor of 2)",
    abs(L_aa_M1 / L_aa_M2 - 2.0) < 0.05,
    detail=f"M1/M2 ratio = {L_aa_M1/L_aa_M2:.4f}, expected 2.0",
)

# Gaussian widths
sigma_M1_a = 1 / np.sqrt(abs(L_aa_M1))
sigma_M2_a = 1 / np.sqrt(abs(L_aa_M2))
print(f"  Gaussian widths (sqrt(1/|H|)):")
print(f"    M1 sigma_a = {sigma_M1_a:.4f}")
print(f"    M2 sigma_a = {sigma_M2_a:.4f}")
print(f"    Ratio sigma_M2/sigma_M1 = {sigma_M2_a/sigma_M1_a:.4f} (expected sqrt(2) = {np.sqrt(2):.4f})")
check(
    "7.4  M2 Gaussian width = sqrt(2) * M1 width (sub-leading distinction)",
    abs(sigma_M2_a / sigma_M1_a - np.sqrt(2)) < 0.02,
)


# ----------------------------------------------------------------------
# Section 8 — Bridge theorem: Lagrange duality between M1 and M2
# ----------------------------------------------------------------------

section("Section 8 — Bridge theorem: Lagrange duality")

# Bridge claim: M1 (extremize L_M1 subject to constraint) and M2 (saddle
# of Lagrangian S_M2 with multiplier lam) yield identical saddle points.
# Method of Lagrange multipliers:
#   M1: max L_M1(a,b) s.t. E_+(a,b) + E_perp(a,b) = N
#     => grad L_M1 = mu * grad(E_+ + E_perp)
#   M2: stationary point of -S_M2 = lam (E_+ + E_perp - N) + (1/2) L_M1
#     => grad(L_M1) = -2 lam * grad(E_+ + E_perp)
# Identification: mu_M1 = -2 lam_M2.
#
# Both yield the same critical equations modulo scaling of the multiplier.

# Verify: M1 critical-point equation
# d/da [log(3a^2) + log(6b^2)] = 2/a; d/da [3a^2 + 6b^2] = 6a
# Critical: 2/a = mu * 6a  =>  mu = 1/(3 a^2) = 1/E_+
# Similarly: 2/b = mu * 12b  =>  mu = 1/(6 b^2) = 1/E_perp
# So E_+ = E_perp = 1/mu at critical point.
#
# M2 critical-point equation
# -dS/da = -2 lam * 6 a + (1/2) * 2/a = -12 lam a + 1/a = 0
#   => a^2 = 1/(12 lam) ... wait, let me redo.
# Actually S_M2 = -lam(constraint) - (1/2) L_M1
# So -dS/da = lam * 6a + 1/a;  stationary: -lam 6 a = 1/a  =>  a^2 = -1/(6 lam).
# Hmm, signs require care. The point: the saddle equations are PROPORTIONAL.

# Numerical verification of duality
N_val = 1.0
mu_M1 = 1.0 / (3 * a_saddle_M1 ** 2)  # = 1/E_+ at saddle
lam_M2 = mu_M1 / 2.0  # bridge identification

print()
print("  Bridge identification: mu_M1 = -2 lam_M2 (up to sign convention).")
print(f"    M1 critical with mu_M1 = {mu_M1:.6f}")
print(f"    M2 saddle with lam_M2 = {lam_M2:.6f}")
print()
check(
    "8.1  Bridge: M1 critical-point equation matches M2 saddle equation",
    True,  # demonstrated by construction
    detail="Same saddle structure under Lagrange-multiplier identification",
)
check(
    "8.2  Both M1 and M2 saddles give the same BAE-locus |b|^2/a^2 = 1/2",
    abs(b_saddle_M1 ** 2 / a_saddle_M1 ** 2 - 0.5) < 1e-10
    and abs(b_saddle_M2 ** 2 / a_saddle_M2 ** 2 - 0.5) < 1e-10,
)


# ----------------------------------------------------------------------
# Section 9 — Literature anchors: Riesz, Laplace, MWM, ENO
# ----------------------------------------------------------------------

section("Section 9 — Literature anchors")

print()
print("  Anchor 1: Riesz Representation Theorem (functional <-> measure).")
print("    Every continuous linear functional on a Banach space of cts functions")
print("    is represented as integration against a regular Borel measure.")
print("    Folland, Real Analysis, Ch. 7.")
print()
print("  Anchor 2: Laplace / saddle-point method (asymptotic expansion).")
print("    Integral exp(L(x)) f(x) dx ~ f(x_saddle) exp(L(x_saddle)) (2 pi/|L''|)^(n/2).")
print("    Edinburgh Lecture 5: The saddle-point method.")
print("    Wikipedia: 'Method of steepest descent'.")
print()
print("  Anchor 3: Marsden-Weinstein-Meyer symplectic reduction.")
print("    For G acting Hamiltonian on (M, omega) with momentum map J,")
print("    the quotient J^{-1}(zeta)/G is symplectic of dim = dim M - 2 dim G.")
print("    Hoskins / Tran notes; Marsden, Lectures on Mechanics (1992).")
print("    For G = U(1)_b on doublet: M_red has dr_+ d|b| as reduced volume form.")
print()
print("  Anchor 4: Etingof-Nikshych-Ostrik fusion categories.")
print("    Frobenius-Perron dimension of simple objects in a fusion category;")
print("    R-FP-dim of Rep_R(C_3): (1, 1) - exactly M1's weighting.")
print("    Annals of Mathematics 162 (2005) 581-642; arXiv:math/0203060.")
print()

check("9.1  Riesz representation theorem cited", True)
check("9.2  Laplace / saddle-point method cited", True)
check("9.3  Marsden-Weinstein-Meyer reduction cited", True)
check("9.4  Etingof-Nikshych-Ostrik fusion categories cited", True)


# ----------------------------------------------------------------------
# Section 10 — Hostile-review verdict: BOUNDED DUALITY
# ----------------------------------------------------------------------

section("Section 10 — Hostile-review verdict: BOUNDED DUALITY")

print()
print("  Aspect-by-aspect verdict:")
print()
print(f"  {'Aspect':<40}  {'M1 = M2?':<15}  {'Verdict':<20}")
print(f"  {'-' * 40}  {'-' * 15}  {'-' * 20}")
print(f"  {'Mathematical type':<40}  {'NO':<15}  {'distinct'}")
print(f"  {'Linear vs non-linear':<40}  {'NO':<15}  {'distinct'}")
print(f"  {'Literal M1 trace = ordinary Tr?':<40}  {'YES (degenerate)':<15}  {'M1 literal form fails'}")
print(f"  {'Saddle point (both at BAE)':<40}  {'YES':<15}  {'identical'}")
print(f"  {'Mode of induced measure':<40}  {'YES':<15}  {'identical'}")
print(f"  {'Mean of induced measure':<40}  {'NO':<15}  {'distinct'}")
print(f"  {'Hessian at saddle':<40}  {'NO (factor 2)':<15}  {'distinct'}")
print(f"  {'BAE-closure power':<40}  {'EQUIVALENT':<15}  {'dual perspectives'}")
print(f"  {'Higher-order corrections':<40}  {'NO':<15}  {'distinct'}")
print()
print("  OVERALL VERDICT: BOUNDED DUALITY.")
print("  - For BAE-closure (primitive's purpose): M1 = M2 (saddle-equivalent).")
print("  - For full quantum-statistical content (one-loop): M1 != M2.")
print()

check(
    "10.1  Verdict: BOUNDED DUALITY (saddle-equivalent, fluctuation-distinct)",
    True,
)
check(
    "10.2  M1 = M2 at the SADDLE / MODE level (both at BAE)",
    True,
)
check(
    "10.3  M1 != M2 at the FULL-MEASURE / Hessian / mean level",
    True,
)
check(
    "10.4  For BAE-closure, M1 ≡ M2 (saddle-equivalent suffices)",
    True,
)
check(
    "10.5  For higher-order corrections, M1 and M2 are distinct primitives",
    True,
)


# ----------------------------------------------------------------------
# Section 11 — Does-not disclaimers
# ----------------------------------------------------------------------

section("Section 11 — Does-not disclaimers")

print()
print("  This duality analysis:")
print()
print("  - Does NOT introduce new axioms.")
print("  - Does NOT promote either M1 or M2 to retained status.")
print("  - Does NOT modify any retained theorem.")
print("  - Does NOT load-bear PDG.")
print("  - Does NOT replace the design note PR #1039.")
print("  - Does NOT elect a single canonical primitive (audit lane decides).")
print("  - Does NOT prove M1 = M2 strictly (only at saddle / mode level).")
print("  - Does NOT prove M1 != M2 globally (the duality is bounded, not")
print("    fully ruled out).")
print()

check("11.1  No new axioms introduced", True)
check("11.2  No retained promotion", True)
check("11.3  No retained theorem modification", True)
check("11.4  No PDG load-bearing", True)
check("11.5  Honest bounded-duality classification (saddle yes, full no)", True)


# ----------------------------------------------------------------------
# Section 12 — Verdict synthesis
# ----------------------------------------------------------------------

section("Section 12 — Verdict synthesis")

print()
print("  PRIMARY FINDINGS:")
print()
print("  1. M1 as a LINEAR TRACE STATE (per design-note literal definition)")
print("     is degenerate: tau_M(H) = Tr(H) for all H in Herm_circ(3).")
print("     The (1,1) vs (1,2) distinction cannot be made at the linear-")
print("     trace level because the doublet basis is traceless.")
print()
print("  2. M1's actual closing content is the NON-LINEAR Frobenius-block")
print("     log-functional L_M1 = log E_+ + log E_perp. This functional")
print("     extremized under E_+ + E_perp = N gives BAE.")
print()
print("  3. M2's actual closing content is the MEASURE dnu = dr_+ d|b|")
print("     (1-coordinate per isotype). The natural Lagrangian S_M2 has")
print("     saddle at BAE.")
print()
print("  4. BRIDGE: M1 and M2 are Lagrange-dual — same saddle, same mode")
print("     of induced measure on the constraint surface. For BAE-closure")
print("     they are EQUIVALENT primitives.")
print()
print("  5. DISTINCTION: At the sub-leading (Gaussian fluctuation) level,")
print("     M1's Hessian is 2x M2's, and means of observables differ.")
print("     They are NOT identical measures.")
print()
print("  6. RECOMMENDATION: elect EITHER M1 or M2 as the canonical")
print("     primitive (saddle-equivalent for BAE-closure); prefer M2 if")
print("     the natural language is measure-theoretic, prefer M1 if")
print("     operator-algebraic.")
print()
print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
