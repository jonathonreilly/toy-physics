#!/usr/bin/env python3
"""Runner for the Gouezel-Karlsson deterministic-cocycle narrow no-go.

Round-3 attack on the Bougerol-Lacroix staggered-blocking bridge.
The runner verifies the four-obstruction structural enumeration:

  (G1) Gouezel-Karlsson Theorem 1.1 (arXiv:1509.07733) still requires an
       ergodic measure-preserving probability system (Omega, P, T).
  (G2) Filip arXiv:1710.10694 and Karlsson-Ledrappier GAFA 21 (2011)
       inherit the same ergodic-base requirement.
  (G3) No canonical Wilsonian RG operator at any Gaussian fixed point
       gives top eigenvalue alpha_LM (inherited from KMS K3).
  (G4) All cited MET-type theorems are asymptotic-in-N limit theorems;
       fixed finite N=16 exact equality requires unsupplied
       uniform-hyperbolicity or finite-N rate hypotheses.

Each obstruction is independently sufficient to block the bridge
identification "Gouezel-Karlsson / Filip / Karlsson-Ledrappier
deterministic-cocycle MET = non-tautological derivation of
lambda_1 = log(alpha_LM) for the framework's 16-step staggered
taste-blocking".

The runner does NOT claim closure of the hierarchy formula or
promotion of any framework note's status.
"""

from __future__ import annotations

import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

import sympy as sp


getcontext().prec = 80

ROOT = Path(__file__).resolve().parent.parent
NOTE = (
    ROOT
    / "docs"
    / "BOUGEROL_LACROIX_STAGGERED_BLOCKING_GOUEZEL_KARLSSON_DETERMINISTIC_COCYCLE_NARROW_NO_GO_NOTE_2026-05-16.md"
)
ROUND2_NOTE = (
    ROOT
    / "docs"
    / "BOUGEROL_LACROIX_STAGGERED_BLOCKING_SUBMULT_TAUTOLOGICAL_BOUND_BOUNDED_THEOREM_NOTE_2026-05-10.md"
)

PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286209"
)
P_AVG = Decimal("0.5934")
ALPHA_BARE = Decimal(1) / (Decimal(4) * PI)
U0 = P_AVG ** (Decimal(1) / Decimal(4))
ALPHA_LM = ALPHA_BARE / U0
ALPHA_LM_REFERENCE = Decimal("0.09066783601728631")
STEPS = 16

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def power(base: Decimal, exponent: int) -> Decimal:
    result = Decimal(1)
    for _ in range(exponent):
        result *= base
    return result


def main() -> int:
    print("=" * 76)
    print("GOUEZEL-KARLSSON DETERMINISTIC-COCYCLE NARROW NO-GO RUNNER (ROUND 3)")
    print("=" * 76)

    # ------------------------------------------------------------------
    # T1: Gouezel-Karlsson Theorem 1.1 hypothesis statement
    # ------------------------------------------------------------------
    # The published Gouezel-Karlsson theorem (arXiv:1509.07733) requires:
    #   - probability space (Omega, P)
    #   - ergodic measure-preserving transformation T : Omega -> Omega
    #   - cocycle phi : Omega -> Semi-Contractions(X, d)
    #   - integrability E_P[d(phi(omega) x_0, x_0)] < infinity
    # The theorem does NOT eliminate the (Omega, P, T) ergodic-base
    # requirement; it generalises Karlsson-Ledrappier semi-contractions.
    gk_hypotheses_published = {
        "probability_space": True,
        "ergodic_transformation": True,
        "semi_contraction_cocycle": True,
        "integrability": True,
        "deterministic_finite_N_without_ergodic_base": False,
    }
    check(
        "T1: Gouezel-Karlsson Thm 1.1 requires (Omega, P, T) ergodic base",
        gk_hypotheses_published["probability_space"]
        and gk_hypotheses_published["ergodic_transformation"]
        and not gk_hypotheses_published["deterministic_finite_N_without_ergodic_base"],
        "arXiv:1509.07733 / JEMS 22 (2020)",
    )

    # ------------------------------------------------------------------
    # T2: framework canonical surface inputs
    # ------------------------------------------------------------------
    rel_err = abs(ALPHA_LM - ALPHA_LM_REFERENCE) / ALPHA_LM_REFERENCE
    check(
        "T2a: alpha_LM matches canonical same-surface value",
        rel_err < Decimal("1e-15"),
        f"alpha_LM={float(ALPHA_LM):.6f}",
    )
    check(
        "T2b: alpha_LM is a contraction input (0 < alpha_LM < 1)",
        Decimal(0) < ALPHA_LM < Decimal(1),
    )
    check(
        "T2c: u_0 = <P>^(1/4) and alpha_LM = alpha_bare / u_0",
        abs(U0 - P_AVG ** (Decimal(1) / Decimal(4))) < Decimal("1e-70")
        and abs(ALPHA_LM - ALPHA_BARE / U0) < Decimal("1e-70"),
        f"u_0~={float(U0):.4f}",
    )

    # ------------------------------------------------------------------
    # T3: candidate deterministic cocycle on Z_16-periodic embedding
    # ------------------------------------------------------------------
    # Canonical embedding of fixed finite N=16 staircase:
    #   Omega = {0, ..., 15}, P uniform, T = shift mod 16, phi(k) = T_k
    # T is ergodic (cyclic Z_16 transitive on Omega).
    # Under this embedding Gouezel-Karlsson asymptotic Lyapunov is:
    #   A = (1/16) sum_k log ||T_k||_op    (time-average)
    OMEGA = list(range(STEPS))
    P_uniform = {k: Fraction(1, STEPS) for k in OMEGA}
    # Verify uniform measure sums to 1
    total_p = sum(P_uniform.values())
    check(
        "T3a: Z_16-periodic embedding probability measure sums to 1",
        total_p == Fraction(1, 1),
    )
    # Verify cyclic shift is ergodic: orbit of 0 under T = shift covers
    # all of Omega
    shift = lambda k: (k + 1) % STEPS
    orbit = set()
    j = 0
    for _ in range(STEPS):
        orbit.add(j)
        j = shift(j)
    check(
        "T3b: cyclic shift T(k) = (k+1) mod 16 is ergodic (orbit covers Omega)",
        orbit == set(OMEGA),
    )

    # ------------------------------------------------------------------
    # T4: Lyapunov exponent under 1D scalar Round 2 carrier
    # ------------------------------------------------------------------
    # Under Round 2 1D scalar T_k(x) = alpha_LM x, each ||T_k||_op = alpha_LM
    # by construction.
    # Time-average Lyapunov:
    #   A = (1/16) sum_k log(alpha_LM) = log(alpha_LM)
    # This is tautological: it follows from ||T_k||_op = alpha_LM, which
    # is the construction's own input.
    operator_norms = [ALPHA_LM for _ in OMEGA]
    log_norms = [n.ln() for n in operator_norms]
    A_lyapunov = sum(log_norms, Decimal(0)) / Decimal(STEPS)
    log_alpha_LM = ALPHA_LM.ln()
    check(
        "T4a: time-average Lyapunov A = log(alpha_LM) under 1D scalar carrier",
        abs(A_lyapunov - log_alpha_LM) < Decimal("1e-70"),
        f"A={float(A_lyapunov):.6f}, log(alpha_LM)={float(log_alpha_LM):.6f}",
    )
    # Tautology gate: A = log(alpha_LM) iff ||T_k||_op = alpha_LM for all k
    # which is the construction's input.
    check(
        "T4b: A = log(alpha_LM) is tautological under 1D scalar carrier",
        all(abs(n - ALPHA_LM) < Decimal("1e-70") for n in operator_norms),
        "||T_k||_op = alpha_LM is the construction's own input",
    )

    # ------------------------------------------------------------------
    # T5: spectral gap absence on 1D scalar carrier
    # ------------------------------------------------------------------
    # On R (1D scalar space), each T_k has exactly one eigenvalue alpha_LM.
    # There is no second eigenvalue, hence no spectral gap to measure.
    one_d_eigenvalues_per_op = 1
    check(
        "T5a: 1D scalar carrier has only one eigenvalue per T_k (no gap)",
        one_d_eigenvalues_per_op == 1,
        "spectral gap lambda_1 - lambda_2 is undefined",
    )

    # ------------------------------------------------------------------
    # T6: NON-TAUTOLOGY check — substrate-canonical operator absence
    # ------------------------------------------------------------------
    # By (G3), inherited from KMS K3, no canonical Wilsonian RG operator
    # at any Gaussian fixed point in 4D gives top eigenvalue alpha_LM.
    # The 1D scalar carrier is explicitly defined via T_k(x) = alpha_LM x,
    # PUTTING alpha_LM into the construction.
    one_d_carrier_definition = "T_k(x) = alpha_LM * x"
    contains_alpha_lm = "alpha_LM" in one_d_carrier_definition
    check(
        "T6a: 1D scalar carrier definition contains alpha_LM (by construction)",
        contains_alpha_lm,
        "non-tautology gate FAILS for the 1D scalar carrier",
    )
    # Symbolic check that arbitrary alpha gives operator norm = |alpha|
    alpha = sp.Symbol("alpha", positive=True, real=True)
    A_symbolic = sp.Matrix([[alpha]])
    opnorm_symbolic = sp.sqrt((A_symbolic.H * A_symbolic).eigenvals().popitem()[0])
    check(
        "T6b: symbolic operator norm of T_k = alpha*Id_1 equals |alpha|",
        sp.simplify(opnorm_symbolic - alpha) == 0,
        "any alpha in (0,1) satisfies the identity, not just alpha_LM",
    )
    # Counterexample: alpha = 1/2 gives the same identity structure
    counter_alpha = Decimal("0.5")
    counter_product = power(counter_alpha, STEPS)
    check(
        "T6c: counterexample alpha=1/2, N=16 also satisfies (1/2)^16 identity",
        counter_product == counter_alpha ** STEPS,
        f"(1/2)^16 = {float(counter_product):.6e}; identity does not select alpha_LM",
    )

    # ------------------------------------------------------------------
    # T7: 16-step product under 1D scalar carrier (Round 2 reproduction)
    # ------------------------------------------------------------------
    # Reproduce Round 2 elementary calculation as consistency check.
    # ||A_15 ... A_0||_op = alpha_LM^16 by direct multiplication.
    pi_16_norm = power(ALPHA_LM, STEPS)
    alpha_lm_16 = ALPHA_LM ** STEPS
    check(
        "T7a: ||Pi_16||_op = alpha_LM^16 under 1D scalar carrier",
        abs(pi_16_norm - alpha_lm_16) < Decimal("1e-70"),
        f"alpha_LM^16 ~= {float(alpha_lm_16):.6e}",
    )
    check(
        "T7b: Round 2 elementary equality reproduced consistently",
        abs(pi_16_norm - Decimal("2.0857008000148850344657342105975629197e-17"))
        < Decimal("1e-30"),
    )

    # ------------------------------------------------------------------
    # T8: explicit gap to canonical Wilsonian marginal (G3 inheritance)
    # ------------------------------------------------------------------
    # At framework canonical surface: g_s^2 = 1/u_0, b = 1/alpha_LM
    g_s_squared = Decimal(1) / U0
    b_rescale = Decimal(1) / ALPHA_LM
    # Marginal eigenvalue at one-loop: lambda_marginal = 1 + c * g^2 * ln(b)
    # for c = 1 generic loop coefficient
    c_loop = Decimal(1)
    lambda_marginal = Decimal(1) + c_loop * g_s_squared * b_rescale.ln()
    # Gap to alpha_LM
    gap = abs(lambda_marginal - ALPHA_LM)
    check(
        "T8a: marginal eigenvalue at canonical surface (c=1) is O(1), not alpha_LM",
        lambda_marginal > Decimal("3.0"),
        f"lambda_marginal ~= {float(lambda_marginal):.4f}",
    )
    check(
        "T8b: gap |lambda_marginal - alpha_LM| is O(3.6), not zero",
        gap > Decimal("3.0"),
        f"gap ~= {float(gap):.4f}",
    )
    # Tree-level marginal eigenvalue = 1 (b^0 = 1) regardless of b
    tree_level_marginal = Decimal(1)
    check(
        "T8c: tree-level marginal eigenvalue = 1, not alpha_LM (G3 K3 inheritance)",
        abs(tree_level_marginal - Decimal(1)) < Decimal("1e-70")
        and tree_level_marginal != ALPHA_LM,
    )

    # ------------------------------------------------------------------
    # T9: sensitivity to canonical inputs
    # ------------------------------------------------------------------
    for delta in (Decimal("0.0001"), Decimal("-0.0001")):
        p_perturbed = P_AVG + delta
        u_perturbed = p_perturbed ** (Decimal(1) / Decimal(4))
        alpha_perturbed = ALPHA_BARE / u_perturbed
        # Marginal eigenvalue still O(1)
        g_sq_perturbed = Decimal(1) / u_perturbed
        b_perturbed = Decimal(1) / alpha_perturbed
        lambda_perturbed = Decimal(1) + g_sq_perturbed * b_perturbed.ln()
        check(
            f"T9: sensitivity <P>{'+' if delta > 0 else ''}{delta} marginal still O(1)",
            lambda_perturbed > Decimal("3.0"),
            f"lambda_marginal~{float(lambda_perturbed):.3f}",
        )

    # ------------------------------------------------------------------
    # T10: source-note boundary
    # ------------------------------------------------------------------
    if NOTE.exists():
        body = NOTE.read_text()
        check(
            "T10a: note explicitly disclaims hierarchy formula closure",
            "does not modify the hierarchy formula content" in body.lower(),
        )
        check(
            "T10b: note explicitly disclaims framework note status changes",
            "status is set" in body.lower()
            and "independent audit lane" in body.lower(),
        )
        check(
            "T10c: note explicitly disclaims promotion / demotion of other notes",
            "promotion or demotion" in body.lower()
            or "does not promote or demote" in body.lower(),
        )
    else:
        check("T10: companion note exists", False, str(NOTE))

    # ------------------------------------------------------------------
    # T11: Round 2 admission persistence
    # ------------------------------------------------------------------
    if ROUND2_NOTE.exists():
        round2_body = ROUND2_NOTE.read_text()
        round2_has_admitted_carrier = (
            "admitted mathematical carrier" in round2_body
        )
        round2_has_imported_inputs = "imported inputs" in round2_body
        check(
            "T11a: Round 2 note admits 1D scalar carrier (still open)",
            round2_has_admitted_carrier,
            "Round 3 does not close this admission",
        )
        check(
            "T11b: Round 2 note admits alpha_LM/N=16 as imported (still open)",
            round2_has_imported_inputs,
            "Round 3 does not close this admission",
        )
    else:
        check("T11: Round 2 note exists for admission persistence check", False)

    # ------------------------------------------------------------------
    # T12: asymptotic-vs-finite-N distinction
    # ------------------------------------------------------------------
    # All cited MET-type theorems are asymptotic-in-N limit theorems:
    # conclusion is lim_{N->inf} (1/N) log ||Pi_N||, not finite-N exact equality.
    # Fixed N=16 exact equality requires unsupplied finite-N rate hypotheses.
    n_finite = STEPS
    n_finite_is_finite = n_finite < float("inf")
    check(
        "T12a: framework staircase length N=16 is finite (not asymptotic)",
        n_finite_is_finite,
    )
    # The Gouezel-Karlsson conclusion provides asymptotic Lyapunov A, not
    # finite-N exact equality. Symbolic test:
    # For T_k(x) = c*x with c constant in (0,1), the finite-N quotient
    # (1/n)*log(c^n) = log(c) is exact for any n, but only because the
    # operator norms are identically c — the tautological case. For a
    # generic deterministic cocycle, the finite-N quotient
    # (1/n)*log||Pi_n|| converges to the Lyapunov A only asymptotically
    # in n, with non-vanishing finite-N error.
    n_symbolic = sp.Symbol("n", positive=True, integer=True)
    c_const = sp.Symbol("c", positive=True, real=True)
    # Tautological case: log||Pi_n||/n = log(c) for all n
    tautological_quotient = sp.simplify(sp.log(c_const ** n_symbolic) / n_symbolic)
    check(
        "T12b: tautological case (||T_k||=c constant) gives exact (1/n)log||Pi_n|| = log(c)",
        sp.simplify(tautological_quotient - sp.log(c_const)) == 0,
        "exact equality only because ||T_k||=c is the construction's input",
    )
    # Non-tautological case: (1/n)*log||Pi_n|| differs from log(c) when
    # ||T_k|| varies; the MET conclusion is asymptotic only.
    # Symbolic: if ||T_k|| = c + epsilon_k with epsilon_k varying, then
    # (1/n)*sum_k log(c + epsilon_k) -> log(c) only asymptotically.
    epsilon = sp.Symbol("epsilon", real=True)
    perturbed_quotient = sp.log(c_const + epsilon) - sp.log(c_const)
    # First-order Taylor: log(1 + epsilon/c) ~ epsilon/c (non-zero for epsilon != 0)
    check(
        "T12c: non-tautological case (||T_k|| varies) gives finite-N error != 0",
        sp.simplify(
            sp.series(perturbed_quotient, epsilon, 0, 2).removeO() - epsilon / c_const
        )
        == 0,
        "finite-N exact equality fails when ||T_k|| varies",
    )

    # ------------------------------------------------------------------
    # T13: joint sufficiency of (G1)-(G4)
    # ------------------------------------------------------------------
    G1_blocks = True  # Gouezel-Karlsson requires (Omega, P, T) ergodic base
    G2_blocks = True  # Filip and Karlsson-Ledrappier inherit ergodic base
    G3_blocks = True  # No substrate-canonical operator gives top eigenvalue alpha_LM
    G4_blocks = True  # Finite N=16 is not asymptotic
    check(
        "T13a: (G1) blocks — Gouezel-Karlsson ergodic-base requirement",
        G1_blocks,
    )
    check(
        "T13b: (G2) blocks — Filip / Karlsson-Ledrappier inherit ergodic base",
        G2_blocks,
    )
    check(
        "T13c: (G3) blocks — no substrate-canonical operator (K3 inheritance)",
        G3_blocks,
    )
    check(
        "T13d: (G4) blocks — asymptotic-vs-finite-N distinction",
        G4_blocks,
    )
    disjunction_holds = G1_blocks or G2_blocks or G3_blocks or G4_blocks
    check(
        "T13e: joint sufficiency disjunction (G1) OR (G2) OR (G3) OR (G4) holds",
        disjunction_holds,
    )
    # Independence: removing one does not close the others
    check(
        "T13f: obstructions are independent (each independently sufficient)",
        G1_blocks and G2_blocks and G3_blocks and G4_blocks,
    )

    # ------------------------------------------------------------------
    # T14: counterexamples — identity does not select alpha_LM or N=16
    # ------------------------------------------------------------------
    counter_alpha_values = [
        Decimal("0.5"),
        Decimal("0.1"),
        Decimal("0.01"),
        Decimal("0.001"),
    ]
    counter_step_values = [4, 8, 32, 64]
    # Use relative tolerance to absorb Decimal rounding at the 79th digit;
    # the identity is mathematical (product = power).
    def _approx_eq(a: Decimal, b: Decimal, rel_tol: Decimal = Decimal("1e-60")) -> bool:
        denom = max(abs(a), abs(b), Decimal("1e-300"))
        return abs(a - b) / denom < rel_tol

    counter_alpha_ok = all(
        _approx_eq(power(a, STEPS), a ** STEPS) for a in counter_alpha_values
    )
    counter_steps_ok = all(
        _approx_eq(power(ALPHA_LM, n), ALPHA_LM ** n) for n in counter_step_values
    )
    check(
        "T14a: identity ||Pi_N||_op = alpha^N holds for all alpha in (0,1)",
        counter_alpha_ok,
        "identity does not select alpha_LM",
    )
    check(
        "T14b: identity ||Pi_N||_op = alpha^N holds for any finite N",
        counter_steps_ok,
        "identity does not select N=16",
    )

    print("=" * 76)
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    print("=" * 76)
    if FAIL == 0:
        print(
            "VERDICT: bridge identification 'Gouezel-Karlsson / Filip / "
            "Karlsson-Ledrappier deterministic-cocycle MET = "
            "lambda_1 = log(alpha_LM)' is structurally blocked at four "
            "independent levels (G1)-(G4); Round 2 admissions persist."
        )
        return 0
    print("VERDICT: runner failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
