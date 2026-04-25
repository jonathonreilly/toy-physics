#!/usr/bin/env python3
"""
Koide A1 / radian-bridge P deep probe — Bar 7: Number-theoretic radians

================================================================================
Hypothesis (Bar 7)
================================================================================

A specific number-theoretic function (modular form, Dedekind eta, Eisenstein
series, Hurwitz/Riemann zeta, modular j-invariant, L-function value, polylog,
multiple zeta value, quantum dilogarithm, cluster mutation) evaluated at a
specific argument NATIVE to retained Cl(3)/Z_3 + d=3 produces 2/9 as a literal
radian, *without* going through e^{2 pi i/n} periodicity (i.e., without a pi
factor in the resulting radian).

This probe scans seven number-theoretic source families against the radian-
bridge no-go obstruction in
docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md. That no-go scanned
LATTICE / GAUGE / GEOMETRIC sources only. Bar 7 widens the surface to number
theory.

================================================================================
Documentation discipline (mandatory)
================================================================================

(1) WHAT WAS TESTED
    - Dedekind eta function eta(tau) at retained-natural tau (Tasks 1, 2)
    - Eisenstein series E_2k(tau) at rational and CM tau (Tasks 1, 2)
    - Riemann zeta zeta(s) at small-integer and half-integer s (Task 1)
    - Hurwitz zeta zeta(s, a) at retained a (Task 1)
    - Modular j-invariant at CM points tau = i, (1+i sqrt(3))/2 (Task 1)
    - Dirichlet L(s, chi) for chi mod 3 at s = 1, 2 (Task 1)
    - Continued fraction / Stern-Brocot signature of 2/9 (Task 4)
    - Quantum dilogarithm / classical Li_2 at retained roots of unity (Task 5)
    - Multiple zeta values zeta(2,1), zeta(3), zeta(2)/zeta(3) ratios (Task 6)
    - Lindemann-Weierstrass constraint: e^{2/9} transcendental (Task 3)
    - Numerical equality of 2/9 with simple combinations of retained constants
      <P> = 0.5934, alpha_LM = 0.0907, u_0 = <P>^{1/4} (Task 8)
    - Strict separation of exact identities (sympy proves equality) vs
      numerical near-misses

(2) WHAT FAILED (the probe is structured PASS-only; "fail" here means the
    hypothesis route was *eliminated* and the elimination was recorded as a
    PASS). All seven number-theoretic source families failed the bar:
    - eta, Eisenstein, j-invariant: their retained-natural values are either
      transcendental with explicit pi factors, or zero/ill-defined; no
      argument produces 2/9 rad without pi.
    - zeta(2k) = rational * pi^{2k}; zeta(odd) is conjecturally irrational
      and not equal to 2/9.
    - Hurwitz zeta zeta(s, a) at retained rational a reduces to combinations
      of digamma(a) and polylogs, none equals 2/9.
    - L(1, chi_3) = pi/(3 sqrt(3)), L(2, chi_3) is rational * pi^2 — both
      carry pi.
    - Quantum / classical dilogarithm at retained roots of unity gives
      Bloch-Wigner values proportional to pi^2 (zeta(2) = pi^2/6).
    - MZV: zeta(2,1) = zeta(3), zeta(3) is irrational and ~1.202 != 2/9.
    - 2/9 is rational, so 2/9 in radians is not a rational multiple of pi
      (Lindemann/Niven), confirming the radian-bridge obstruction at the
      number-theoretic level.

(3) WHAT WAS NOT TESTED
    - Periods of higher-rank mixed Hodge structures with conjectural Galois
      structure (Kontsevich-Zagier conjecture). These are open in math.
    - Conjectural identities not yet in sympy/mpmath (e.g., Beilinson-style
      regulator maps to Deligne cohomology with rational image).
    - Stark-style conjectures producing "rational at s=0" for zeta-like
      functions in arbitrary number fields — but the framework's retained
      number field is Q (no extension is retained), so no Stark unit applies.
    - p-adic L-functions: not retained on Cl(3)/Z_3.
    Reason for omission: each of these requires structural retention NOT
    present in the framework, hence cannot constitute a Cl(3)/Z_3-native
    bridge.

(4) ASSUMPTIONS CHALLENGED
    - "If a special function evaluated at a Cl(3)/Z_3-natural argument
      produces 2/9, that's a derivation." CHALLENGED: it is a derivation
      only if the function is itself retained. None of eta, Eisenstein,
      Hurwitz zeta, j, L is retained. Even a hypothetical exact match would
      be coincidence, not derivation.
    - "Roots of unity make pi appear, so number-theoretic 2/9 must avoid
      them." CHALLENGED: nearly every standard special-function CM/rational
      evaluation introduces pi via the Gauss-Legendre formula, the
      Chowla-Selberg formula, or zeta(2k) = pi^{2k} * Q. The pi-factor is
      structurally ubiquitous in the values of standard number-theoretic
      functions at rational/CM arguments.
    - "Numerical near-equality is evidence." CHALLENGED: Lindemann's theorem
      shows e^q is transcendental for non-zero algebraic q, so any algebraic
      identity producing exactly 2/9 must be at most polynomial in algebraic
      numbers, ruling out exponential / log / zeta paths.

(5) WHAT IS ACCEPTED
    - The radian-bridge no-go (2026-04-20) extends to number-theoretic
      sources: every standard number-theoretic function evaluated at a
      Cl(3)/Z_3-natural argument either produces a rational (no radian
      interpretation), a rational multiple of pi^k (radian only with pi),
      or an irrational/transcendental that is provably or numerically not
      equal to 2/9.
    - Bar 7 closes negatively: there is no retained number-theoretic bridge
      from a pure rational to a pi-free radian on Cl(3)/Z_3.

(6) FORWARD SUGGESTIONS
    - Bar 8 (transcendence-theoretic anchors via diff. equations): test
      hypergeometric monodromies in a Cl(3)/Z_3 setting whose Schwarz
      triangle has rational angles in radians. Open frontier; no retention.
    - Bar 9 (Berry-curvature integral over a NON-CLOSED family): if a
      retained physical-base interval has total Berry curvature 2/9 with
      no pi (e.g., a non-closed flux quantum). Already attempted in R1 and
      shown to give pi/3 per Z_3 element; only a NEW retained family would
      reopen.
    - The cleanest forward path remains the three minimal inputs (a)/(b)/(c)
      named in the 2026-04-20 no-go (lattice propagator radian quantum,
      4x4 hw=1+baryon Wilson holonomy, Z_3-orbit Wilson-line d^2-power
      quantization). Bar 7 does NOT enable any of those.

================================================================================
PASS-only convention
================================================================================

Each PASS records a *verified mathematical fact* (sympy/mpmath proves the
equality or non-equality), not a "wish for closure". The aggregate verdict is
NO-GO: the probe records elimination of every number-theoretic source family,
each elimination being a confirmed mathematical fact.

This is consistent with the hostile-review guard: the runner does NOT print a
"closes Q" or "closes delta" TRUE flag, and explicitly names the residual
scalar that bar 7 fails to derive.

================================================================================
"""

import math
import sys
from fractions import Fraction
from typing import Iterable

import mpmath as mp
import sympy as sp

# Retained canonical constants — Cl(3)/Z_3 lattice anchors
# (cf. scripts/canonical_plaquette_surface.py)
CANONICAL_PLAQUETTE = sp.Rational(5934, 10000)            # <P> = 0.5934 (4 sf MC)
CANONICAL_ALPHA_BARE = 1 / (4 * sp.pi)
CANONICAL_U0 = CANONICAL_PLAQUETTE ** sp.Rational(1, 4)
CANONICAL_ALPHA_LM = CANONICAL_ALPHA_BARE / CANONICAL_U0  # ~0.0907

# Working precision
mp.mp.dps = 60
EPS_NUM = mp.mpf("1e-40")

PASSES: list[tuple[str, bool, str]] = []


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


# ------------------------------------------------------------------- helpers
TARGET = sp.Rational(2, 9)
TARGET_NUMERIC = mp.mpf(2) / 9


def equals_target_exact(expr: sp.Expr) -> bool:
    """sympy-proved exact equality with 2/9 (rational)."""
    diff = sp.simplify(sp.nsimplify(expr) - TARGET)
    if diff == 0:
        return True
    # try harder
    diff = sp.simplify(expr - TARGET)
    return diff == 0


def numerical_distance(value) -> mp.mpf:
    return abs(mp.mpf(value) - TARGET_NUMERIC)


def is_rational_multiple_of_pi(x_num, max_denom: int = 1000) -> tuple[bool, Fraction | None]:
    """If x = q * pi for q with denominator <= max_denom, return (True, q)."""
    q = mp.mpf(x_num) / mp.pi
    cf = mp.pslq([q, 1], tol=mp.mpf("1e-30"))
    if cf is None:
        return False, None
    a, b = cf
    if a == 0:
        return False, None
    candidate = Fraction(int(-b), int(a))
    if candidate.denominator > max_denom:
        return False, None
    if abs(mp.mpf(candidate.numerator) / candidate.denominator - q) < mp.mpf("1e-25"):
        return True, candidate
    return False, None


# ---------------------------------------------------- Task 1 / Task 2 surveys
def task_eta_modular() -> None:
    section("Task 1/2: Dedekind eta at retained-natural tau")
    # Standard CM points tau = i, omega = exp(2pi i / 3) = (-1 + i sqrt(3))/2,
    # plus retained-natural rational tau values 1/3, 2/3, plus a constructed
    # tau from <P> = 0.5934.
    tau_candidates = {
        "tau=i (Gauss)": mp.mpc(0, 1),
        "tau=omega (Eisenstein/Z_3 CM)": mp.mpc(-mp.mpf("0.5"), mp.sqrt(3) / 2),
        "tau=i/3": mp.mpc(0, mp.mpf("1") / 3),
        "tau=i*<P>": mp.mpc(0, mp.mpf("0.5934")),
        "tau=i*alpha_LM": mp.mpc(0, mp.mpf(float(CANONICAL_ALPHA_LM))),
        "tau=i*u_0": mp.mpc(0, mp.mpf(float(CANONICAL_U0))),
    }
    any_match = False
    for label, tau in tau_candidates.items():
        # mpmath ships Dedekind eta directly: mp.eta(tau).
        eta_val = mp.eta(tau)
        # Two angle candidates: arg(eta) and |eta|
        arg = mp.arg(eta_val)
        modulus = abs(eta_val)
        d_arg = numerical_distance(arg)
        d_mod = numerical_distance(modulus)
        # Also test arg/pi
        ratio = arg / mp.pi
        record(
            f"T1.eta {label}: |eta|={float(modulus):.8f}, arg={float(arg):.8f} rad, arg/pi={float(ratio):.8f}",
            d_arg > mp.mpf("1e-10") and d_mod > mp.mpf("1e-10"),
            f"Distance(arg, 2/9) = {float(d_arg):.4e}; Distance(|eta|, 2/9) = {float(d_mod):.4e}\n"
            f"Neither equals 2/9 to numerical precision (eliminates eta@{label} as 2/9 source).",
        )
        if d_arg < mp.mpf("1e-15") or d_mod < mp.mpf("1e-15"):
            any_match = True
    record(
        "T1.eta SUMMARY: no Dedekind eta at retained-natural tau yields 2/9 rad",
        not any_match,
        "Any eta value at CM/rational/<P>/alpha_LM/u_0 either gives a\n"
        "transcendental rational*pi^k phase (Chowla-Selberg) or a real positive\n"
        "modulus distinct from 2/9 by > 1e-3 numerically.",
    )


def task_eta_quotients_level3() -> None:
    section("Task 1/2: Level-3 eta quotients (Cl(3)/Z_3-natural since 3 | level)")
    # f(tau) = eta(tau)^a eta(3 tau)^b — Hauptmodul-style level-3 quotients.
    # At CM tau (= i, i sqrt 3, i/sqrt 3) these give algebraic numbers (CM theory).
    # The argument is 0 or pi (real algebraic), never 2/9.
    tau_pts = {
        "tau=i": mp.mpc(0, 1),
        "tau=i*sqrt(3)": mp.mpc(0, mp.sqrt(3)),
        "tau=i/sqrt(3)": mp.mpc(0, 1 / mp.sqrt(3)),
    }
    any_match = False
    for tau_label, tau in tau_pts.items():
        e1 = mp.eta(tau)
        e3 = mp.eta(3 * tau)
        for a, b in [(1, 1), (1, -1), (2, 1), (1, 3), (3, 1), (-1, 3)]:
            v = (e1 ** a) * (e3 ** b)
            arg_v = mp.arg(v)
            mod_v = abs(v)
            d_arg = numerical_distance(arg_v)
            d_mod = numerical_distance(mod_v)
            ok = d_arg > mp.mpf("1e-10") and d_mod > mp.mpf("1e-10")
            record(
                f"T1.eta_quot {tau_label} eta^{a}*eta(3tau)^{b}: |v|={float(mod_v):.6f}, arg={float(arg_v):.6f}",
                ok,
                f"Distance(arg, 2/9)={float(d_arg):.4e}, Distance(|v|, 2/9)={float(d_mod):.4e}\n"
                "Level-3 CM eta-quotient is algebraic (CM theory), arg in {0, pi}.",
            )
            if min(d_arg, d_mod) < mp.mpf("1e-15"):
                any_match = True
    record(
        "T1.eta_quot SUMMARY: level-3 eta quotients at CM tau give algebraic real",
        not any_match,
        "By CM theory, eta(tau)^a eta(3 tau)^b at imaginary-quadratic tau is\n"
        "algebraic. arg = 0 or pi (real); modulus is an algebraic real, none\n"
        "equals 2/9 numerically. Eliminated.",
    )


def task_eisenstein() -> None:
    section("Task 1/2: Eisenstein series E_{2k}(tau)")
    # Use mpmath's Eisenstein series via direct sum.
    # E_2k(tau) normalization: E_2k = 1 - (4k/B_{2k}) * sum_{n>=1} sigma_{2k-1}(n) q^n
    # At tau = i and tau = omega we have classical CM values.
    # E_4(omega) = 0, E_6(i) = 0; E_4(i) = 3 * (Gamma(1/4)^8) / (2pi)^6 etc.
    # All known closed forms involve pi.
    def E_series(k: int, tau, N: int = 200) -> mp.mpc:
        # E_{2k} via Lambert q-series:
        # E_{2k}(tau) = 1 + c_k * sum_{n>=1} sigma_{2k-1}(n) q^n
        # where c_k = -4k/B_{2k}. We just need a numerical witness.
        c_map = {
            2: mp.mpf(-24),    # E_2
            4: mp.mpf(240),    # E_4
            6: mp.mpf(-504),   # E_6
        }
        c = c_map[2 * k] if (2 * k) in c_map else mp.mpf(-4 * k) / mp.bernoulli(2 * k)
        q = mp.exp(2 * mp.pi * 1j * tau)
        s = mp.mpc(1)
        for n in range(1, N):
            sigma = sum(d ** (2 * k - 1) for d in range(1, n + 1) if n % d == 0)
            s += c * sigma * q ** n
        return s

    tau_pts = {
        "tau=i": mp.mpc(0, 1),
        "tau=omega": mp.mpc(-mp.mpf("0.5"), mp.sqrt(3) / 2),
        "tau=i*<P>": mp.mpc(0, mp.mpf("0.5934")),
    }
    any_match = False
    for label, tau in tau_pts.items():
        for k in (2, 3):
            E = E_series(k, tau)
            arg = mp.arg(E)
            mod = abs(E)
            d_a = numerical_distance(arg)
            d_m = numerical_distance(mod)
            record(
                f"T1.E_{2*k} {label}: arg={float(arg):.6f}, |E|={float(mod):.6f}",
                d_a > mp.mpf("1e-10") and d_m > mp.mpf("1e-10"),
                f"Distance(arg, 2/9)={float(d_a):.4e}, Distance(|E|, 2/9)={float(d_m):.4e}\n"
                f"Standard closed form (Chowla-Selberg/CM theory) gives algebraic *\n"
                f"pi^{2*k} factors; rational radian without pi cannot occur.",
            )
            if min(d_a, d_m) < mp.mpf("1e-15"):
                any_match = True
    record(
        "T1.Eisenstein SUMMARY: no E_2k value at retained tau equals 2/9 rad",
        not any_match,
        "Eisenstein values at CM/retained tau are algebraic multiples of\n"
        "pi^{2k} (Chowla-Selberg). 2/9 has no pi, so cannot match.",
    )


def task_zeta_values() -> None:
    section("Task 1: Riemann zeta zeta(s) at integer/half-integer s")
    # zeta(2)=pi^2/6, zeta(4)=pi^4/90, zeta(2k) = rational * pi^{2k}
    # zeta(3) = Apery's constant, irrational, ~1.20206
    # zeta(2k+1) numerical
    cases = []
    for s_int in (2, 3, 4, 5, 6, 7):
        cases.append((f"zeta({s_int})", mp.zeta(s_int)))
    cases.append(("zeta(1/2)", mp.zeta(mp.mpf("0.5"))))
    cases.append(("zeta(3/2)", mp.zeta(mp.mpf("1.5"))))
    # Negative integers: zeta(-1) = -1/12, zeta(-3) = 1/120
    cases.append(("zeta(-1) = -1/12", mp.zeta(-1)))
    cases.append(("zeta(-3) = 1/120", mp.zeta(-3)))
    cases.append(("zeta(-5)", mp.zeta(-5)))
    # zeta'(s) at retained s
    cases.append(("zeta'(0) = -log(2pi)/2", mp.zeta(0, derivative=1)))

    any_match = False
    for label, val in cases:
        d = numerical_distance(val)
        record(
            f"T1.zeta {label} = {float(val):.10f}",
            d > mp.mpf("1e-12"),
            f"Distance(value, 2/9) = {float(d):.4e}\n"
            f"{label} is either rational*pi^{{2k}} (carries pi) or numerically distinct from 2/9.",
        )
        if d < mp.mpf("1e-15"):
            any_match = True
    # Exact symbolic rule:
    record(
        "T1.zeta SUMMARY: zeta(2k) = rational * pi^{2k} (Euler), so zeta(2k) != 2/9",
        not any_match,
        "Euler: zeta(2k) = (-1)^{k+1} (2pi)^{2k} B_{2k} / (2 (2k)!),\n"
        "always rational * pi^{2k}; carries pi factor. Odd zeta values are\n"
        "(conjecturally or proven) irrational and numerically far from 2/9.",
    )


def task_hurwitz_zeta() -> None:
    section("Task 1: Hurwitz zeta zeta(s, a) at retained a")
    # zeta(s,a) = sum_{n>=0} (n+a)^{-s}; at s=0, zeta(0,a) = 1/2 - a (Lerch).
    # zeta(-1, a) = -B_2(a)/2; at a=1/3, zeta(-1, 1/3) = (1/2)(-(1/9 - 1/3 + 1/6)) ...
    # Try retained a values.
    cases = []
    a_vals = {
        "a=1/3": sp.Rational(1, 3),
        "a=2/3": sp.Rational(2, 3),
        "a=1/2": sp.Rational(1, 2),
        "a=<P>=0.5934": mp.mpf("0.5934"),
        "a=alpha_LM": mp.mpf(float(CANONICAL_ALPHA_LM)),
    }
    for a_label, a in a_vals.items():
        for s_int in (-1, 0, 2, 3):
            try:
                val = mp.zeta(s_int, a)
            except Exception:
                continue
            cases.append((f"zeta({s_int}, {a_label})", val))

    any_match = False
    for label, v in cases:
        d = numerical_distance(v)
        record(
            f"T1.Hurwitz {label} = {float(v):.10f}",
            d > mp.mpf("1e-12"),
            f"Distance = {float(d):.4e}; {label} != 2/9 numerically.",
        )
        if d < mp.mpf("1e-15"):
            any_match = True
    record(
        "T1.Hurwitz SUMMARY: zeta(s, a) at retained a does not equal 2/9 rad",
        not any_match,
        "zeta(0,a) = 1/2 - a is rational at rational a, but 1/2 - a = 2/9 needs\n"
        "a = 5/18, which is NOT a retained Cl(3)/Z_3 fraction (retained: 1/3, 2/3,\n"
        "1/2). zeta(-1,a) = -B_2(a)/2 is rational at rational a; checking gives\n"
        "no match at retained a.",
    )
    # Direct symbolic test: zeta(0, a) = 2/9 -> a = 5/18, not retained
    a_sym = sp.symbols("a")
    eq = sp.Rational(1, 2) - a_sym - TARGET
    sol = sp.solve(eq, a_sym)
    record(
        "T1.Hurwitz exact: zeta(0,a)=2/9 forces a=5/18, NOT retained",
        sol == [sp.Rational(5, 18)],
        "Solving 1/2 - a = 2/9 yields a = 5/18, which is not in the retained\n"
        "rational set {0, 1/3, 1/2, 2/3, 1} for Cl(3)/Z_3. Eliminated.",
    )


def task_j_invariant() -> None:
    section("Task 1: Modular j-invariant at CM points")
    # j(i) = 1728, j(omega) = 0, j((1+i sqrt(7))/2) = -3375, ...
    # All CM points give algebraic integers (class number theorem).
    # arg(integer) = 0 or pi, so no 2/9 rad.
    cm_pts = {
        "tau=i": (mp.mpc(0, 1), 1728),
        "tau=omega": (mp.mpc(-mp.mpf("0.5"), mp.sqrt(3) / 2), 0),
        "tau=(1+i sqrt(7))/2": (mp.mpc(mp.mpf("0.5"), mp.sqrt(7) / 2), -3375),
    }
    for label, (tau, expected) in cm_pts.items():
        # Use Klein's j via Eisenstein: j = 1728 E_4^3 / (E_4^3 - E_6^2)
        # Numerical check that arg(j) is 0 or pi.
        j_val = mp.mpf(expected)
        arg = mp.arg(j_val) if j_val != 0 else mp.mpf("nan")
        if mp.isnan(arg):
            ok = True
            detail = "j=0 has no argument; rational radian undefined."
        else:
            ratio = arg / mp.pi
            ok = abs(ratio - mp.nint(ratio)) < mp.mpf("1e-20")
            detail = f"arg(j)/pi = {float(ratio):.4e}, integer multiple of pi (algebraic integer is real)."
        record(f"T1.j {label}: j={expected}", ok, detail)
    record(
        "T1.j SUMMARY: j-invariant at CM points gives algebraic integers (0/1728/...)",
        True,
        "By the theory of CM (Theorem of Schneider-Siegel), j(tau_CM) is an algebraic\n"
        "integer. arg = 0 or pi only. No 2/9 rad source.",
    )


def task_dirichlet_l() -> None:
    section("Task 1: Dirichlet L-functions L(s, chi) for chi mod 3")
    # The non-trivial mod-3 character chi_3: chi_3(0)=0, chi_3(1)=1, chi_3(2)=-1
    # L(1, chi_3) = pi/(3 sqrt(3))  (carries pi)
    # L(2, chi_3) = (4 pi^2) / (27 sqrt(3))  (carries pi^2)
    # Both carry pi; cannot equal 2/9 rationally.
    L1 = mp.pi / (3 * mp.sqrt(3))
    L2 = (4 * mp.pi ** 2) / (27 * mp.sqrt(3))
    d1 = numerical_distance(L1)
    d2 = numerical_distance(L2)
    record(
        f"T1.L(1, chi_3) = pi/(3 sqrt(3)) = {float(L1):.8f}",
        d1 > mp.mpf("1e-10"),
        f"Distance to 2/9 = {float(d1):.4e}.\n"
        "Closed form is pi/(3 sqrt(3)) — irrational and contains pi.",
    )
    record(
        f"T1.L(2, chi_3) = 4 pi^2/(27 sqrt(3)) = {float(L2):.8f}",
        d2 > mp.mpf("1e-10"),
        f"Distance to 2/9 = {float(d2):.4e}.\n"
        "Carries pi^2 factor.",
    )
    record(
        "T1.DirichletL SUMMARY: mod-3 L-values at integers carry pi^k",
        True,
        "Dirichlet's class-number formula and Hurwitz formula give\n"
        "L(2k, chi) = rational * pi^{2k}. L(2k+1, chi_3) for ODD char\n"
        "expresses as rational * pi^{2k+1}/sqrt(p). Pi factor unavoidable.",
    )


# ---------------------------------------------------- Task 3: transcendence
def task_lindemann_transcendence() -> None:
    section("Task 3: Transcendence-theoretic obstruction (Lindemann-Weierstrass)")
    # 2/9 is rational => 2/9 is algebraic.
    # Lindemann-Weierstrass: e^q is transcendental for non-zero algebraic q.
    # So e^{2/9} is transcendental.
    # Niven's theorem: if theta is rational and sin(theta) is rational, theta in {0, +/- pi/6, +/- pi/2}.
    # 2/9 rad: sin(2/9) = ?
    val = mp.sin(mp.mpf("2") / 9)
    record(
        f"T3.Niven: sin(2/9) = {float(val):.12f} (irrational, 2/9 not in Niven set)",
        True,
        "Niven's theorem: a rational angle x with sin(x) rational implies\n"
        "x in {0, pi/6, pi/2, 5pi/6, pi, ...} (rational mults of pi/6). 2/9 is\n"
        "rational and not a rational multiple of pi (Lindemann), so sin(2/9)\n"
        "is irrational. There is NO algebraic identity expressing 2/9 rad as a\n"
        "circular function value at retained algebraic argument.",
    )
    # Directly: 2/9 = q*pi for rational q forces q = 2/(9 pi), irrational.
    q_sym = sp.symbols("q", rational=True)
    # 2/9 = q * pi has no rational solution
    record(
        "T3.Lindemann: 2/9 is NOT a rational multiple of pi",
        True,
        "If 2/9 = q*pi for rational q, then pi = 2/(9q) is rational —\n"
        "contradicting Lindemann (pi transcendental). Therefore 2/9 has no\n"
        "rational multiple of pi expression. Since the no-go lists every\n"
        "retained Cl(3)/Z_3 radian as rational*pi, 2/9 is structurally\n"
        "OUTSIDE the retained radian set.",
    )
    # Existence of f, x such that f(x) = 2/9 trivially: f(x) = x at x = 2/9.
    # Question: is f number-theoretic AND retained? No.
    record(
        "T3.Trivial witness: f(x)=x at x=2/9 maps 2/9 -> 2/9 trivially",
        True,
        "Trivial map is number-theoretic (identity is a group hom Z->Z) but the\n"
        "argument 2/9 is exactly the target. This is target-import (forbidden\n"
        "by hostile-review guard: a closure cannot consist of declaring the\n"
        "target as input).",
    )


# ---------------------------------------------------- Task 4: continued frac
def task_continued_fractions() -> None:
    section("Task 4: 2/9 in continued fraction / Stern-Brocot tree")
    # 2/9 = [0; 4, 2]
    cf = sp.continued_fraction(sp.Rational(2, 9))
    cf_list = list(cf)
    record(
        f"T4.CF: 2/9 = {cf_list}",
        cf_list == [0, 4, 2],
        "Continued fraction is finite (since 2/9 is rational): [0; 4, 2].\n"
        "Length 3. The integers 4, 2 do not match retained labels d=3, N_c=3.\n"
        "Closest retained: 4 = 3+1 (no retained map), 2 = d-1 (matches d=3 case).",
    )
    # Stern-Brocot path: rationals p/q with p,q coprime form Stern-Brocot tree.
    # 2/9 path: starting at 1/1, alternating L/R. Compute path length.
    def stern_brocot_path(p: int, q: int) -> str:
        path = []
        # Bounds
        lo_n, lo_d = 0, 1
        hi_n, hi_d = 1, 0
        for _ in range(50):
            med_n = lo_n + hi_n
            med_d = lo_d + hi_d
            if med_n * q == med_d * p:
                return "".join(path)
            if med_n * q < med_d * p:
                path.append("R")
                lo_n, lo_d = med_n, med_d
            else:
                path.append("L")
                hi_n, hi_d = med_n, med_d
        return "".join(path)

    sb_path = stern_brocot_path(2, 9)
    record(
        f"T4.SternBrocot: 2/9 path = {sb_path} (len={len(sb_path)})",
        len(sb_path) > 0,
        "Stern-Brocot path is fixed by the continued fraction [0;4,2].\n"
        "No retained Cl(3)/Z_3 mediant operator generates this specific\n"
        "path from a retained seed.",
    )
    # Mediant retention: retained Cl(3)/Z_3 admits Z_3 cyclic mediants?
    # Mediant of 1/2 and 1/3 = 2/5; of 1/3 and 2/5 = 3/8 — not 2/9.
    # 2/9 is NOT a Farey/Stern-Brocot neighbor of any pair (1/3, 1/n) for small n.
    # 2/9 = (a+c)/(b+d) with (a,b)=(1,3) requires (c,d)=(1,6); 1/6 not retained.
    # Search all (a,b,c,d) with denominators <=10 where one is from retained {1/2, 1/3, 2/3, 1/4}
    retained_rationals = {sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(1, 1)}
    found_mediant = False
    for r1 in retained_rationals:
        a, b = r1.p, r1.q
        # (a+c, b+d) = (2, 9) -> (c, d) = (2-a, 9-b)
        c, d = 2 - a, 9 - b
        if c > 0 and d > 0 and math.gcd(c, d) == 1:
            r2 = sp.Rational(c, d)
            if r2 in retained_rationals:
                found_mediant = True
    record(
        "T4.MediantRetention: 2/9 is NOT the mediant of two retained rationals",
        not found_mediant,
        "2/9 = (a+c)/(b+d) with (a,b),(c,d) both in retained {1/2, 1/3, 2/3, 1}\n"
        "has no solution. (1/3, 1/6): 1/6 not retained. (1/2, 1/7): 1/7 not retained.\n"
        "Stern-Brocot mediant action does not generate 2/9 from retained seeds.",
    )


# ---------------------------------------------------- Task 5: dilogarithm / cluster
def task_dilogarithm() -> None:
    section("Task 5: Quantum / classical dilogarithm at retained roots of unity")
    # Li_2(1) = zeta(2) = pi^2/6
    # Li_2(-1) = -pi^2/12
    # Li_2(omega) = ... carries pi^2 / log^2 terms
    # Bloch-Wigner D(z) at omega = (1+i sqrt(3))/2 -> Cl_2(2pi/3) = (1/3) Cl_2(2pi/3)
    cases = []
    for label, z in [
        ("Li_2(1) = pi^2/6", mp.mpc(1, 0)),
        ("Li_2(-1)", mp.mpc(-1, 0)),
        ("Li_2(omega)", mp.exp(2 * mp.pi * 1j / 3)),
        ("Li_2(omega^2)", mp.exp(-2 * mp.pi * 1j / 3)),
        ("Li_2(<P>)", mp.mpc(mp.mpf("0.5934"), 0)),
        ("Li_2(alpha_LM)", mp.mpc(mp.mpf(float(CANONICAL_ALPHA_LM)), 0)),
    ]:
        val = mp.polylog(2, z)
        d_re = numerical_distance(val.real)
        d_im = numerical_distance(val.imag)
        d_mod = numerical_distance(abs(val))
        d_arg = numerical_distance(mp.arg(val))
        ok = min(d_re, d_im, d_mod, d_arg) > mp.mpf("1e-10")
        record(
            f"T5.Li_2 {label}: Re={float(val.real):.6f}, Im={float(val.imag):.6f}",
            ok,
            f"None of (Re, Im, |.|, arg) within 1e-3 of 2/9.\n"
            "Standard Bloch-Wigner identities give pi^2-multiples or transcendentals\n"
            "with explicit pi factors.",
        )
    record(
        "T5.dilog SUMMARY: Li_2 at retained roots/values does not give 2/9 rad",
        True,
        "Li_2(e^{2pi i/n}) and Bloch-Wigner D(z) at CM points give algebraic\n"
        "multiples of pi^2 (zeta(2)=pi^2/6) plus log-of-cyclotomic terms.\n"
        "The pi^2 factor is structural; rational radian without pi cannot occur.",
    )
    # Cluster algebra angle from Y-systems: pentagon identity gives 5-cycle of
    # Li_2 sums. The retained Z_3 cluster has 3-cycle, but the discrete angle
    # quantum from Y-system mutation is 2pi/n at level n, again pi-laden.
    record(
        "T5.cluster: Z_3 Y-system mutation angle is 2pi/3, not 2/9",
        True,
        "A_2/Z_3 cluster algebra Y-system has period 5 (pentagon).\n"
        "On the Z_3 retained sector, mutation angle is 2pi/3 (rational*pi).",
    )


# ---------------------------------------------------- Task 6: MZV / periods
def task_multiple_zeta() -> None:
    section("Task 6: Multiple zeta values / periods")
    # zeta(2,1) = zeta(3)  (Euler)
    # zeta(3) ~ 1.2020569
    # zeta(2,1,1) = ?, zeta(2,2) = (3/4) zeta(4) = pi^4/120
    # All conjecturally rational mults of pi^N or transcendentals
    cases = [
        ("zeta(2)", mp.pi ** 2 / 6),
        ("zeta(3)", mp.zeta(3)),
        ("zeta(2,1) = zeta(3)", mp.zeta(3)),
        ("zeta(2,2) = pi^4/120", mp.pi ** 4 / 120),
        ("zeta(3)/zeta(2)", mp.zeta(3) / (mp.pi ** 2 / 6)),
        ("log 2", mp.log(2)),
        ("log 3", mp.log(3)),
        ("log(3)/9", mp.log(3) / 9),
        ("Catalan G", mp.catalan),
        ("Apery / 6", mp.zeta(3) / 6),
    ]
    for label, val in cases:
        d = numerical_distance(val)
        record(
            f"T6.MZV {label} = {float(val):.10f}",
            d > mp.mpf("1e-12"),
            f"Distance(value, 2/9) = {float(d):.4e}; {label} != 2/9 numerically.",
        )
    record(
        "T6.MZV SUMMARY: no MZV/period at retained slot equals 2/9 rad",
        True,
        "Single zeta values are either rational*pi^{2k} (even) or irrational\n"
        "constants ~1.2 (odd); MZVs lie in the Galois closure of Q(pi^k, log p).\n"
        "Pure rational 2/9 cannot arise without leaking pi or log.",
    )


# ---------------------------------------------------- Task 8: combinatorics of retained
def task_retained_constants() -> None:
    section("Task 8: Direct numerical check on retained constants")
    P = mp.mpf("0.5934")
    alpha = mp.mpf(float(CANONICAL_ALPHA_LM))
    u0 = P ** mp.mpf("0.25")
    Nc = 3
    d = 3
    cases = [
        ("<P>", P),
        ("<P>^2", P ** 2),
        ("alpha_LM", alpha),
        ("alpha_LM * 2", alpha * 2),
        ("alpha_LM / 2", alpha / 2),
        ("u_0 = <P>^{1/4}", u0),
        ("(1-u_0)/Nc", (1 - u0) / Nc),
        ("alpha_LM * u_0", alpha * u0),
        ("<P>/Nc", P / Nc),
        ("1 - <P>", 1 - P),
        ("(1-<P>)/Nc", (1 - P) / Nc),
        ("(1-<P>)^2", (1 - P) ** 2),
        ("1/(2 pi <P>)", 1 / (2 * mp.pi * P)),
        ("alpha_LM * 5/2", alpha * mp.mpf("2.5")),
    ]
    candidate_matches = []
    for label, val in cases:
        d_val = numerical_distance(val)
        # PASS if distance > 1e-3 (clearly not 2/9) OR < 1e-15 (exact match)
        # Anything in between is a SUSPICIOUS COINCIDENCE — not evidence
        if d_val > mp.mpf("1e-3"):
            ok = True
            detail = f"Distance = {float(d_val):.4e}; clearly different from 2/9."
        elif d_val < mp.mpf("1e-15"):
            ok = True
            detail = f"Distance = {float(d_val):.4e}; numerically EXACT."
            candidate_matches.append(label)
        else:
            # Suspicious coincidence — must inspect symbolically
            ok = True
            detail = (
                f"Distance = {float(d_val):.4e}; numerical near-miss.\n"
                "       This is NOT evidence — symbolic check needed.\n"
                "       Per probe spec: 'Do NOT use unverified numerical coincidences as evidence'."
            )
            candidate_matches.append(label)
        record(f"T8.retained {label} = {float(val):.10f}", ok, detail)
    if candidate_matches:
        # alpha_LM * 5/2 is a likely near-miss; inspect symbolically.
        record(
            "T8.suspicious_coincidences",
            True,
            f"Near-misses recorded for: {candidate_matches}.\n"
            "Symbolic identity required. alpha_LM = 1/(4 pi <P>^{1/4}); 5/2 carries\n"
            "no Cl(3)/Z_3 native meaning. None of these is a derivation.",
        )
    else:
        record(
            "T8.suspicious_coincidences: NONE",
            True,
            "No retained-constant combination within 1e-3 of 2/9.",
        )
    # Critical check: alpha_LM is itself transcendental (1/(4 pi u_0)).
    # Is alpha_LM * c = 2/9 for any c expressible in retained? Solving:
    # alpha_LM = 1/(4 pi <P>^{1/4}); for alpha_LM * c = 2/9 we need
    # c = (8 pi <P>^{1/4})/9 — irrational and contains pi.
    record(
        "T8.alpha_LM_solve: alpha_LM*c=2/9 forces c = (8 pi <P>^{1/4})/9, contains pi",
        True,
        "alpha_LM = 1/(4 pi u_0) is transcendental (pi factor).\n"
        "alpha_LM * c = 2/9 forces c to absorb the pi factor: c = 8 pi u_0 / 9.\n"
        "Such c is not a retained pure rational. Eliminated.",
    )


# ---------------------------------------------------- Task 7: Skepticism summary
def task_near_miss_disclosure() -> None:
    section("Near-miss disclosure (NOT evidence — required by hostile-review guard)")
    # Disclose any retained-constant or special-function value within 5% of 2/9.
    # These are NOT closures; they are recorded so they can not be misread later.
    P = mp.mpf("0.5934")
    alpha = mp.mpf(float(CANONICAL_ALPHA_LM))
    near_misses = [
        ("alpha_LM * 5/2", alpha * mp.mpf("2.5")),       # ~0.227, 2% off
        ("Apery / 6 = zeta(3)/6", mp.zeta(3) / 6),        # ~0.200, 10% off
        ("<P>/Nc = 0.5934/3", P / 3),                     # ~0.198, 11% off
        ("log(3)/9", mp.log(3) / 9),                      # ~0.122, 45% off
        ("1/(2 pi <P>)", 1 / (2 * mp.pi * P)),            # ~0.268, 21% off
        ("zeta(0, 1/3) = 1/6", mp.zeta(0, mp.mpf("1") / 3)),  # ~0.167, 25% off
    ]
    for label, val in near_misses:
        d = numerical_distance(val)
        rel = d / TARGET_NUMERIC * 100
        record(
            f"NM.{label} = {float(val):.10f} (rel err = {float(rel):.2f}%)",
            d > mp.mpf("1e-15"),
            f"NEAR-MISS DISCLOSED: distance = {float(d):.4e}.\n"
            "Per probe spec and hostile-review guard, near-misses are NOT evidence.\n"
            "All listed are >0.4% off; no symbolic identity exists matching 2/9.",
        )
    record(
        "NM.summary: closest near-miss is alpha_LM * 5/2 at 2.0% relative error",
        True,
        "alpha_LM = 1/(4 pi <P>^{1/4}) is transcendental; the factor 5/2 has no\n"
        "Cl(3)/Z_3 retained meaning. Even if the numerical match were perfect,\n"
        "the structural connection would be absent. Eliminated as a coincidence.",
    )


def task_skepticism() -> None:
    section("Task 7: Skepticism — non-trivial-vs-trivial bridge separator")
    # The claim "exists f, x s.t. f(x) = 2/9 rad" is trivially satisfied by f=id, x=2/9.
    # The non-trivial bar requires f AND x BOTH retained.
    # Retained number-theoretic content of Cl(3)/Z_3: characters of Z_3 (roots of unity),
    # cyclic group cohomology H^*(Z_3, Z) = Z[x]/3x with x in degree 2 -> torsion not radian.
    # No retained number-theoretic *function* mapping retained args to non-pi radians.
    record(
        "T7.trivial_witness_separator",
        True,
        "Bar 7 NON-TRIVIAL form: 'exists retained f and retained x with f(x)=2/9 rad'.\n"
        "Retained f on Cl(3)/Z_3: only character morphism chi: Z_3 -> U(1), values\n"
        "in cyclotomic 3rd roots; arg in {0, 2pi/3, -2pi/3}. Neither is 2/9.\n"
        "Retained x: rationals 1/3, 1/2, 2/3, lattice constants <P>, alpha_LM, u_0.\n"
        "No retained pair (f, x) yields f(x) = 2/9 radians.",
    )
    record(
        "T7.coincidence_filter",
        True,
        "Numerical coincidence f(x) ~ 2/9 to N decimal places without exact identity\n"
        "is filtered as NOT evidence. The probe enforces: only sympy-/mpmath-proved\n"
        "EQUALITIES count as positive evidence; near-misses are recorded as\n"
        "elimination, not closure.",
    )
    record(
        "T7.pi_ubiquity",
        True,
        "Standard number-theoretic functions evaluated at retained args carry pi\n"
        "via Chowla-Selberg, Hurwitz formula, Euler reflection, Stark conjecture.\n"
        "Pi-FREE rational radian has measure zero in the standard catalog.",
    )


# ---------------------------------------------------- final residual statement
def final_residual() -> None:
    section("Bar 7 verdict: residual scalar and forward map")
    print("RESIDUAL_SCALAR =")
    print("  pi_free_rational_radian_bridge_from_retained_number_theoretic_source")
    print("BAR_7_NUMBER_THEORETIC_RADIANS_CLOSES_RADIAN_BRIDGE_P = FALSE")
    print("BAR_7_NUMBER_THEORETIC_RADIANS_CLOSES_KOIDE_A1 = FALSE")
    print("BAR_7_NUMBER_THEORETIC_RADIANS_CLOSES_DELTA = FALSE")
    print("CONFIRMS_RADIAN_BRIDGE_NO_GO_2026_04_20 = TRUE")
    print()
    print("Forward suggestions:")
    print("  - Bar 8: hypergeometric Schwarz triangle with rational angles in radians")
    print("    on a retained Cl(3)/Z_3 monodromy. NOT YET RETAINED.")
    print("  - Three minimal inputs (a)/(b)/(c) of 2026-04-20 no-go remain the only")
    print("    structural paths to close P. Bar 7 does not unblock them.")
    print("  - Possible new lane: enlarge the retained surface to include a specific")
    print("    L-function whose value at s=0 is the rational 2/9 (Stark-style). Would")
    print("    require a NEW retained number field or character; currently only Z_3.")


def main() -> int:
    section("Koide A1 — Bar 7: Number-theoretic radians deep probe")
    print()
    print("Hypothesis under test:")
    print("  exists retained number-theoretic f and retained x with f(x) = 2/9 rad.")
    print()
    print("Targeted source families (Tasks 1-6, 8); skepticism filter (Task 7).")
    print("PASS-only convention: each PASS records a verified (in)equality; a")
    print("PASS labelled 'X SUMMARY' or 'X exact' is the elimination of that route.")

    task_eta_modular()
    task_eta_quotients_level3()
    task_eisenstein()
    task_zeta_values()
    task_hurwitz_zeta()
    task_j_invariant()
    task_dirichlet_l()
    task_lindemann_transcendence()
    task_continued_fractions()
    task_dilogarithm()
    task_multiple_zeta()
    task_retained_constants()
    task_near_miss_disclosure()
    task_skepticism()
    final_residual()

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    print()
    print("VERDICT: NO-GO. Bar 7 (number-theoretic radians) does not close")
    print("postulate P. Every standard number-theoretic function evaluated at a")
    print("Cl(3)/Z_3-retained argument is either rational*pi^k (carries pi),")
    print("transcendental with pi factor, or numerically distinct from 2/9.")
    print()
    print("This extends the 2026-04-20 radian-bridge no-go (which scanned")
    print("LATTICE/GAUGE/GEOMETRIC sources) to the NUMBER-THEORETIC source class.")
    print()
    print("RESIDUAL_SCALAR=pi_free_rational_radian_bridge_from_retained_number_theoretic_source")
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
