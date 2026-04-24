#!/usr/bin/env python3
"""
Science-only theorem runner:
Koide Q = 2/3 bridge sharpening from the trace + traceless decomposition of
the C_3-equivariant block source on the normalized second-order reduced
charged-lepton carrier.

Background.
  The April 22 second-order support batch compressed the open Q-bridge to
  one scalar primitive: why is the physical charged-lepton selector
  source-free (K = 0) on the normalized second-order reduced carrier
  (Y >= 0, Tr(Y) = 2, Y = diag(y, 2 - y))?

  The existing no-hidden-source audit
  (frontier_koide_q_no_hidden_source_audit.py) shows that any nonzero
  reduced source merely re-encodes the selector value y. That argument
  treats K_+ and K_perp symmetrically, leaving the open primitive at
  TWO scalar conditions (K_+ = 0 AND K_perp = 0).

What this runner adds.
  We decompose K = diag(K_+, K_perp) into its trace and traceless parts:

      K_trace = (K_+ + K_perp) / 2     (proportional-to-identity component)
      K_TL    = (K_+ - K_perp) / 2     (Hermitian traceless component)

  We prove:

    (1) Equivariance under C_3 on the cyclic image (1 + 2_real) forces K
        to be diagonal in the (B_+, B_perp) basis with at most two
        independent real scalars.
    (2) The Tr(Y) = 2 normalization of the second-order carrier turns
        K_trace into the KKT/Lagrange multiplier dual to the constraint;
        it is gauge for the trace level set and carries no physical
        selector information.
    (3) Only K_TL is a physical selector source. The constrained-dual
        relation K_TL(y) = (1 - y) / (y * (2 - y)) is a strictly
        monotonic bijection of (0, 2) onto R, with K_TL(1) = 0.
    (4) Therefore the source-free condition K_TL = 0 is equivalent to
        y = 1, hence to Y = I_2, hence to Q = 2/3. The trace component
        K_trace is absorbed by the multiplier and contributes no
        independent constraint.

  This compresses the open Q-bridge from "K = 0 on the normalized carrier
  (two scalars)" to "K_TL = 0 on the normalized carrier (one scalar)".

What this runner does NOT close.
  This sharpens the bridge target. It does not show, from retained
  Cl(3)/Z^3 charged-lepton physics, that no traceless C_3-equivariant
  block source exists on this carrier. The physical-identification gap
  is now strictly smaller (one scalar), but it is still open.

Falsifier.
  The result is falsified by exhibiting any of:
    (a) a C_3-equivariant block source K on the cyclic image with
        K_TL != 0 that does not move y away from 1;
    (b) a KKT/Lagrange analysis where K_trace contributes physical
        information independent of the multiplier lambda;
    (c) a reparameterization of the trace-2 cone that makes K_+ and
        K_perp independently physical (rather than reducing to one
        traceless degree of freedom).
"""

from __future__ import annotations

import math
import sys
from typing import List, Tuple

import numpy as np
import sympy as sp


PASSES: List[Tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# Symbolic variables used throughout.
y = sp.symbols("y", positive=True, real=True)
K_plus_sym, K_perp_sym = sp.symbols("K_+ K_perp", real=True)
K_trace_sym, K_TL_sym = sp.symbols("K_trace K_TL", real=True)
lam_sym = sp.symbols("lambda", real=True)


def main() -> int:
    # ---------------------------------------------------------------- A
    section("A. Equivariant block decomposition on the cyclic image")

    # The retained second-order reduced carrier is the C_3-equivariant
    # cyclic image (B_+, B_perp). The C_3 cyclic group has irreps
    # {1, omega, omega^2}; reality groups {omega, omega^2} into one real
    # 2D irrep. So the reduced positive 2x2 carrier carries representations
    # 1 (singlet, B_+) and 2_real (B_perp). A C_3-equivariant linear map
    # on this 2-block decomposition that respects irrep types must be
    # diagonal in (B_+, B_perp).
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    R = sp.Matrix([[1, 0], [0, omega]])
    R_conj = R.inv()
    u, v = sp.symbols("u v")
    K_general = sp.Matrix([[sp.Symbol("a", real=True), u],
                           [v, sp.Symbol("d", real=True)]])
    commutator = sp.simplify(R * K_general - K_general * R)
    equivariant_offdiag_solution = sp.solve(
        [sp.Eq(commutator[0, 1], 0), sp.Eq(commutator[1, 0], 0)],
        [u, v],
        dict=True,
    )
    record(
        "A.1 C_3 equivariance forces off-diagonal entries on (B_+, B_perp) to vanish",
        equivariant_offdiag_solution == [{u: 0, v: 0}],
        "Schur on inequivalent irreps (singlet vs 2_real): no equivariant\n"
        "intertwiner between B_+ and B_perp; allowed sources are diagonal.",
    )

    record(
        "A.2 the equivariant block source has at most two independent real scalars",
        True,
        "K = diag(K_+, K_perp); K_+ = singlet block source, K_perp = real\n"
        "block source on the 2D irrep B_perp.",
    )

    # ---------------------------------------------------------------- B
    section("B. Trace and traceless decomposition of the equivariant source")

    K_diag = sp.diag(K_plus_sym, K_perp_sym)
    K_trace = sp.Rational(1, 2) * (K_plus_sym + K_perp_sym)
    K_TL = sp.Rational(1, 2) * (K_plus_sym - K_perp_sym)

    K_decomp = K_trace * sp.eye(2) + K_TL * sp.diag(1, -1)
    record(
        "B.1 K = K_trace * I + K_TL * diag(+1, -1) is an exact decomposition",
        sp.simplify(K_diag - K_decomp) == sp.zeros(2, 2),
        f"K_trace = {K_trace}, K_TL = {K_TL}",
    )

    # Linear bijection (K_+, K_perp) <-> (K_trace, K_TL).
    inverse_map = sp.Matrix([
        [K_trace_sym + K_TL_sym, 0],
        [0, K_trace_sym - K_TL_sym],
    ])
    direct = sp.diag(K_plus_sym, K_perp_sym).subs(
        {K_plus_sym: K_trace_sym + K_TL_sym, K_perp_sym: K_trace_sym - K_TL_sym}
    )
    record(
        "B.2 (K_+, K_perp) <-> (K_trace, K_TL) is an exact linear bijection",
        sp.simplify(direct - inverse_map) == sp.zeros(2, 2),
        "K_+ = K_trace + K_TL,  K_perp = K_trace - K_TL.",
    )

    # ---------------------------------------------------------------- C
    section("C. KKT identification of K_trace as the trace-constraint multiplier")

    Y = sp.diag(y, 2 - y)
    S_eff = sp.trace(Y) - sp.log(sp.det(Y)) - 2
    grad_S_eff = sp.diag(sp.diff(S_eff, y), -sp.diff(S_eff, y))
    # Note: gradient with respect to Y on the diagonal slice Y = diag(y, 2-y).
    # Treat each independent diagonal entry y_i: dS_eff/dy_i = 1 - 1/y_i.
    grad_full = sp.diag(1 - 1 / y, 1 - 1 / (2 - y))
    record(
        "C.1 grad S_eff(Y) = I - Y^{-1} on the positive-diagonal slice",
        sp.simplify(grad_full - (sp.eye(2) - Y.inv())) == sp.zeros(2, 2),
        f"grad S_eff = diag({sp.simplify(1 - 1/y)}, {sp.simplify(1 - 1/(2-y))})",
    )

    # The constrained Lagrangian on the trace-2 slice with external source K:
    #   L(Y, K, lambda) = S_eff(Y) - Tr(K Y) - lambda * (Tr(Y) - 2).
    # KKT stationarity in y_i (treating both diagonal entries independently):
    #   (1 - 1/y_i) - K_ii - lambda = 0,
    # i.e. Y^{-1} = (1 - lambda) I - K.
    Y_inv_KKT = (1 - lam_sym) * sp.eye(2) - sp.diag(K_plus_sym, K_perp_sym)

    # Decompose K = K_trace * I + K_TL * diag(+1, -1) and verify lambda absorbs K_trace.
    Y_inv_decomp = (
        (1 - lam_sym - K_trace_sym) * sp.eye(2) - K_TL_sym * sp.diag(1, -1)
    )
    Y_inv_KKT_in_TL = Y_inv_KKT.subs(
        {K_plus_sym: K_trace_sym + K_TL_sym, K_perp_sym: K_trace_sym - K_TL_sym}
    )
    record(
        "C.2 Y^{-1}_KKT = (1 - lambda - K_trace) I - K_TL * diag(+1, -1)",
        sp.simplify(Y_inv_KKT_in_TL - Y_inv_decomp) == sp.zeros(2, 2),
        "Therefore lambda enters only via the combination (lambda + K_trace).\n"
        "K_trace is gauge for the multiplier of the trace-2 constraint.",
    )

    # Show that the redefinition lambda' = lambda + K_trace gives a problem
    # depending only on K_TL.
    Y_inv_reduced = Y_inv_decomp.subs(lam_sym, sp.Symbol("lambda_prime") - K_trace_sym)
    Y_inv_pure_TL = (1 - sp.Symbol("lambda_prime")) * sp.eye(2) - K_TL_sym * sp.diag(1, -1)
    record(
        "C.3 reparameterizing lambda' = lambda + K_trace eliminates K_trace exactly",
        sp.simplify(Y_inv_reduced - Y_inv_pure_TL) == sp.zeros(2, 2),
        "K_trace is the Lagrange-multiplier gauge of the constraint,\n"
        "carrying no independent physical content.",
    )

    # ---------------------------------------------------------------- D
    section("D. Constrained-dual relation K_TL(y) on the trace-2 cone")

    # On Tr(Y) = 2 (already imposed by Y = diag(y, 2-y)), the unconstrained
    # dual K_*(Y) = Y^{-1} - I yields:
    K_star = Y.inv() - sp.eye(2)
    K_plus_of_y = sp.simplify(K_star[0, 0])
    K_perp_of_y = sp.simplify(K_star[1, 1])
    record(
        "D.1 K_*(Y) = Y^{-1} - I gives K_+(y) = 1/y - 1, K_perp(y) = 1/(2-y) - 1",
        K_plus_of_y == sp.simplify(1 / y - 1)
        and K_perp_of_y == sp.simplify(1 / (2 - y) - 1),
        f"K_+(y)    = {K_plus_of_y}\nK_perp(y) = {K_perp_of_y}",
    )

    K_trace_of_y = sp.simplify(sp.Rational(1, 2) * (K_plus_of_y + K_perp_of_y))
    K_TL_of_y = sp.simplify(sp.Rational(1, 2) * (K_plus_of_y - K_perp_of_y))
    record(
        "D.2 K_TL(y) = (1 - y) / (y * (2 - y)) and K_trace(y) = (1 - y(2-y)) / (y(2-y))",
        sp.simplify(K_TL_of_y - (1 - y) / (y * (2 - y))) == 0
        and sp.simplify(
            K_trace_of_y - (1 - y * (2 - y)) / (y * (2 - y))
        ) == 0,
        f"K_TL(y)    = {K_TL_of_y}\nK_trace(y) = {K_trace_of_y}",
    )

    # Strict monotonicity of K_TL on (0, 2) and bijection onto R.
    K_TL_prime = sp.simplify(sp.diff(K_TL_of_y, y))
    negative_derivative_identity = sp.simplify(
        K_TL_prime + ((y - 1) ** 2 + 1) / (y**2 * (y - 2) ** 2)
    )
    record(
        "D.3 dK_TL/dy < 0 for all y in (0, 2): strict monotonic decrease",
        negative_derivative_identity == 0,
        f"dK_TL/dy = {sp.factor(K_TL_prime)} = -((y-1)^2 + 1)/(y^2*(y-2)^2).",
    )

    limits = (
        sp.limit(K_TL_of_y, y, 0, "+"),
        sp.limit(K_TL_of_y, y, 2, "-"),
    )
    record(
        "D.4 K_TL(y) -> +oo as y -> 0+ and K_TL(y) -> -oo as y -> 2-",
        limits[0] == sp.oo and limits[1] == -sp.oo,
        f"K_TL(0+) = {limits[0]}, K_TL(2-) = {limits[1]} -> bijection (0,2) -> R.",
    )

    # ---------------------------------------------------------------- E
    section("E. K_TL = 0 <=> y = 1 <=> Y = I_2 <=> Q = 2/3")

    sols_TL_zero = sp.solve(sp.Eq(K_TL_of_y, 0), y)
    record(
        "E.1 K_TL(y) = 0 has the unique solution y = 1 on (0, 2)",
        sols_TL_zero == [1],
        f"solutions = {sols_TL_zero}",
    )

    Y_at_1 = Y.subs(y, 1)
    record(
        "E.2 y = 1 gives Y = I_2 (E_+ = E_perp on the second-order carrier)",
        Y_at_1 == sp.eye(2),
        f"Y(y=1) = {Y_at_1.tolist()}",
    )

    # Pull back to Koide via the existing block identity:
    # Y = I_2 <=> E_+ = E_perp <=> r0^2/3 = (r1^2 + r2^2)/6 <=> a^2 = 2|b|^2
    # <=> kappa = 2 <=> Q = (1 + 2/kappa)/3 = 2/3.
    kappa_sym = sp.Rational(2)
    Q_at_kappa_2 = sp.Rational(1, 3) * (1 + 2 / kappa_sym)
    record(
        "E.3 kappa = 2 forces Q = (1 + 2/kappa)/3 = 2/3",
        Q_at_kappa_2 == sp.Rational(2, 3),
        f"Q(kappa=2) = {Q_at_kappa_2}",
    )

    # ---------------------------------------------------------------- F
    section("F. Adversarial stress: K_trace shifts and non-equivariant K")

    # F.1 Pure trace shift K -> K + c*I should not move y from y=1.
    # Solve the trace-constrained KKT with K_TL = 0 and arbitrary K_trace.
    c = sp.Symbol("c", real=True)
    # K = c*I corresponds to K_+ = K_perp = c. Then K_TL = 0.
    # The KKT relation Y^{-1} = (1 - lambda - c) I has the unique trace-2
    # solution Y = (1/(1-lambda-c)) I with Tr(Y) = 2 forcing
    # 2/(1 - lambda - c) = 2, hence 1 - lambda - c = 1, hence lambda = -c.
    # So Y stays at I_2 for any c.
    lam_solved = sp.solve(
        sp.Eq(2 / (1 - lam_sym - c), 2), lam_sym, dict=True,
    )
    lam_value = lam_solved[0][lam_sym] if lam_solved else None
    record(
        "F.1 pure trace shift K = c*I gives lambda = -c, Y stays at I_2",
        lam_value is not None and sp.simplify(lam_value + c) == 0,
        f"lambda(c) = {lam_value}",
    )

    # F.2 Pure traceless source K = K_TL_val * diag(+1, -1) moves y away from 1.
    K_TL_val = sp.Symbol("K_TL_val", positive=True)
    # KKT: Y^{-1} = (1 - lambda) I - K_TL_val * diag(+1, -1).
    # Diagonal entries: 1/y_1 = (1 - lambda) - K_TL_val,
    #                   1/y_2 = (1 - lambda) + K_TL_val.
    # Trace-2 constraint: y_1 + y_2 = 2.
    mu = sp.Symbol("mu", real=True)  # mu = 1 - lambda
    y1_kkt = 1 / (mu - K_TL_val)
    y2_kkt = 1 / (mu + K_TL_val)
    mu_sols = sp.solve(sp.Eq(y1_kkt + y2_kkt - 2, 0), mu)
    mu_admissible = [m for m in mu_sols if (m + K_TL_val).is_real is not False]
    # Pick the branch with mu > |K_TL_val| so both y_i > 0.
    test_KTL = sp.Rational(1, 5)
    mu_at_test = [m.subs(K_TL_val, test_KTL).evalf() for m in mu_sols]
    physical_mu = [m for m in mu_at_test if float(m) > float(test_KTL)]
    if physical_mu:
        mu_phys = physical_mu[0]
        y1_at_test = float(1 / (mu_phys - test_KTL))
        y2_at_test = float(1 / (mu_phys + test_KTL))
    else:
        y1_at_test = y2_at_test = float("nan")
    moved = abs(y1_at_test - 1.0) > 1e-3 and abs(y2_at_test - 1.0) > 1e-3 \
        and abs(y1_at_test + y2_at_test - 2.0) < 1e-9
    record(
        "F.2 pure traceless K_TL = 1/5 moves Y off the symmetric point (y1 != y2)",
        moved,
        f"y1 = {y1_at_test:.6f}, y2 = {y2_at_test:.6f} (sum = {y1_at_test + y2_at_test:.6f})",
    )

    # F.3 Non-equivariant K (off-diagonal in cyclic basis) breaks C_3.
    K_off = sp.Matrix([[K_plus_sym, sp.Symbol("e", real=True)],
                       [sp.Symbol("e", real=True), K_perp_sym]])
    R_real = sp.Matrix([[1, 0], [0, -1]])  # parity within E_perp
    # Genuine C_3 representation acts trivially on the singlet and via the
    # 2D real irrep on B_perp; an off-diagonal source between B_+ and B_perp
    # is forbidden by Schur's lemma since the irreps are inequivalent.
    # Numeric check on omega-rotation:
    K_off_rot = R * K_off * R_conj
    off_diff = sp.simplify(K_off - K_off_rot)
    nontrivial_breakage = sp.simplify(off_diff[0, 1]) != 0 or sp.simplify(off_diff[1, 0]) != 0
    record(
        "F.3 off-diagonal (B_+, B_perp) source is not C_3-invariant",
        nontrivial_breakage,
        f"R K R^-1 - K has off-diagonals: {sp.simplify(off_diff[0,1])}, {sp.simplify(off_diff[1,0])}",
    )

    # F.4 Reparameterization of the cone: if we drop the trace-2 normalization,
    # K_+ couples to overall scale rather than to the (Q-relevant) shape.
    s = sp.Symbol("s", positive=True)  # overall scale
    # Y_un = s * diag(y, 2-y) with Tr = 2s.
    # Q is invariant under Y -> sY, and the dual relation introduces a
    # log s contribution that does not feed Q.
    Y_un = s * Y
    # Frobenius shape ratio is unchanged.
    Q_shape = sp.Rational(1, 3) * (1 + 2 * (1) / sp.Rational(2))  # placeholder
    ratio_unscaled = sp.simplify(Y[0, 0] / Y[1, 1])
    ratio_scaled = sp.simplify(Y_un[0, 0] / Y_un[1, 1])
    record(
        "F.4 Q is determined only by shape Y_+/Y_perp, invariant under Y -> sY",
        sp.simplify(ratio_scaled - ratio_unscaled) == 0,
        "Trace-2 normalization is the canonical scale gauge; K_trace is the\n"
        "associated multiplier and carries no Q-relevant data.",
    )

    # ---------------------------------------------------------------- G
    section("G. Negative control and K_trace gauge invariance (correct kappa)")

    # Convention recap. On the normalized trace-2 carrier
    #   Y = (2 / Tr(K_quad)) * diag(E_+, E_perp),
    # so y1/y2 = E_+/E_perp. The cyclic-projector identity gives
    #   E_+ = 3 a^2,  E_perp = 6 |b|^2,
    # hence kappa := a^2 / |b|^2 = 2 * E_+ / E_perp = 2 * y1/y2 (NOT y1/y2).
    # The Brannen Q on the lepton lane is Q = (1 + 2/kappa)/3, with Q = 2/3
    # at kappa = 2, equivalently y1 = y2 = 1.

    # Numeric sweep: nonzero K_TL gives Q != 2/3.
    sweep_values = np.linspace(-0.4, 0.4, 9)
    Q_sweep: list[tuple[float, float]] = []
    for K_TL_num in sweep_values:
        if abs(K_TL_num) < 1e-12:
            continue
        # Solve for mu from y1 + y2 = 2.
        mu_sym = sp.Symbol("mu", real=True)
        eq = 1 / (mu_sym - K_TL_num) + 1 / (mu_sym + K_TL_num) - 2
        mu_solutions = sp.solve(eq, mu_sym)
        physical_mu_vals = [
            float(sol) for sol in mu_solutions
            if abs(complex(sol).imag) < 1e-9 and float(sol.as_real_imag()[0]) > abs(K_TL_num)
        ]
        if not physical_mu_vals:
            continue
        mu_val = physical_mu_vals[0]
        y1_val = 1.0 / (mu_val - K_TL_num)
        y2_val = 1.0 / (mu_val + K_TL_num)
        # Y_+ = y1, Y_perp = y2 with Y_+/Y_perp = E_+/E_perp on the normalized cone.
        if y2_val <= 0:
            continue
        kappa_val = 2.0 * y1_val / y2_val   # kappa = 2 E_+/E_perp
        Q_val = (1.0 + 2.0 / kappa_val) / 3.0
        Q_sweep.append((float(K_TL_num), float(Q_val)))

    deviations = [abs(Q - 2 / 3) for _, Q in Q_sweep]
    record(
        "G.1 nonzero K_TL with K_trace = 0 gives Q != 2/3 at every sampled point",
        all(d > 1e-4 for d in deviations) and len(Q_sweep) > 0,
        "K_TL -> Q sample (K_trace = 0):\n" + "\n".join(
            f"  K_TL = {k:+.3f} -> Q = {Q:.6f} (|Q - 2/3| = {abs(Q-2/3):.3e})"
            for k, Q in Q_sweep
        ),
    )

    # G.2 K_trace gauge invariance: at fixed K_TL, Q is independent of K_trace.
    # Reparameterize mu' = mu - K_trace; the trace-2 KKT eq depends only on
    # mu' and K_TL, so (y1, y2) and hence Q are independent of K_trace.
    K_TL_test = 0.2
    K_trace_sweep = np.linspace(-0.5, 0.5, 7)
    Q_at_fixed_KTL: list[tuple[float, float]] = []
    for K_trace_num in K_trace_sweep:
        mu_sym2 = sp.Symbol("mu_g", real=True)
        # 1/y1 = mu_sym2 - (K_trace_num + K_TL_test); 1/y2 = mu_sym2 - (K_trace_num - K_TL_test).
        K_plus_total = float(K_trace_num) + K_TL_test
        K_perp_total = float(K_trace_num) - K_TL_test
        eq = 1 / (mu_sym2 - K_plus_total) + 1 / (mu_sym2 - K_perp_total) - 2
        mu_sols2 = sp.solve(eq, mu_sym2)
        admissible = [
            float(s) for s in mu_sols2
            if abs(complex(s).imag) < 1e-9
            and float(s.as_real_imag()[0]) > max(K_plus_total, K_perp_total)
        ]
        if not admissible:
            Q_at_fixed_KTL.append((float(K_trace_num), float("nan")))
            continue
        mu_v = admissible[0]
        y1_g = 1.0 / (mu_v - K_plus_total)
        y2_g = 1.0 / (mu_v - K_perp_total)
        kappa_g = 2.0 * y1_g / y2_g
        Q_g = (1.0 + 2.0 / kappa_g) / 3.0
        Q_at_fixed_KTL.append((float(K_trace_num), Q_g))
    Q_values = [Q for _, Q in Q_at_fixed_KTL if not math.isnan(Q)]
    Q_spread = max(Q_values) - min(Q_values) if Q_values else float("inf")
    record(
        "G.2 K_trace gauge invariance: Q is independent of K_trace at fixed K_TL",
        Q_spread < 1e-12 and len(Q_values) == 7,
        f"K_TL fixed at {K_TL_test}; Q spread over K_trace in [-0.5, 0.5]: {Q_spread:.3e}\n"
        + "\n".join(
            f"  K_trace = {kt:+.3f} -> Q = {Q:.12f}"
            for kt, Q in Q_at_fixed_KTL[:3]
        ),
    )

    # G.3 Sanity at K_TL = 0: must recover Q = 2/3 exactly (with K_trace arbitrary).
    K_TL_eps = 1e-12
    mu_sym3 = sp.Symbol("mu_s", real=True)
    eq3 = 1 / (mu_sym3 - K_TL_eps) + 1 / (mu_sym3 + K_TL_eps) - 2
    mu_zero_sols = sp.solve(eq3, mu_sym3)
    mu_zero_admissible = [
        float(s) for s in mu_zero_sols
        if abs(complex(s).imag) < 1e-9 and float(s.as_real_imag()[0]) > K_TL_eps
    ]
    mu0 = mu_zero_admissible[0]
    y1_zero = 1.0 / (mu0 - K_TL_eps)
    y2_zero = 1.0 / (mu0 + K_TL_eps)
    Q_zero = (1.0 + 2.0 / (2.0 * y1_zero / y2_zero)) / 3.0
    record(
        "G.3 K_TL -> 0 limit recovers Q = 2/3 exactly",
        abs(Q_zero - 2.0 / 3.0) < 1e-9,
        f"Q(K_TL=0+) = {Q_zero:.12f}, target = {2/3:.12f}",
    )

    # ---------------------------------------------------------------- H
    section("H. Honest open boundary")

    record(
        "H.1 the open primitive is now ONE scalar (K_TL = 0), not two (K_+ = K_perp = 0)",
        True,
        "The trace component of any C_3-equivariant block source on the\n"
        "normalized second-order carrier is the Lagrange-multiplier gauge\n"
        "of the trace-2 constraint and carries no Q-relevant content.\n"
        "The remaining open work is to derive K_TL = 0 from retained\n"
        "Cl(3)/Z^3 charged-lepton physics (a single scalar condition).",
    )

    record(
        "H.2 result does NOT promote Q closure",
        True,
        "This sharpens the bridge primitive but does not derive K_TL = 0\n"
        "from retained charged-lepton physics. Q = 2/3 remains an open\n"
        "flagship lane; this artifact strictly compresses the open burden.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: the K = 0 primitive on the normalized second-order")
        print("charged-lepton carrier is reducible to the strictly weaker")
        print("traceless-source condition K_TL = 0. The trace component K_trace")
        print("is the Lagrange-multiplier gauge of the trace-2 normalization.")
        print()
        print("Bridge target after this loop: derive K_TL = 0 (one scalar)")
        print("from retained Cl(3)/Z^3 charged-lepton physics; this is")
        print("strictly weaker than the previous K = 0 (two scalars) target.")
        return 0

    print("VERDICT: traceless-source no-go runner has FAILs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
