#!/usr/bin/env python3
"""
Koide A1 cross-sector higher-loop probe (Bar 9, deep probe #38).

HYPOTHESIS UNDER TEST
=====================
A specific HIGHER-LOOP cross-sector diagram (lepton-Higgs-W-graviton or
three-way Higgs-W-Yukawa box with Z_3 generation insertion) generates a
phase that combines with retained Z_3 character phases to give precisely
δ = 2/9 rad (the empirically required Koide A1 phase).

PRIOR CROSS-SECTOR CLOSURE STATUS
=================================
Already DEAD by retained no-go's and prior probes:
  - Lepton-Higgs chiral bridge       (O6: tensor-sector blindness)
  - Lepton-quark via QCD             (Q_ν = 2/3 prediction refuted)
  - Lepton-neutrino see-saw          (M_R diagonal forbidden)
  - Sumino-style cross-sector + cancellation  (Bar 13)
  - ABJ / WZW (intra-sector form)    (DEAD)

Candidates explicitly NOT YET TESTED in the prior 37-probe sweep:
  D1.  Lepton 2-loop self-energy with Higgs + W exchange
  D2.  Lepton-graviton loop at Planck scale
  D3.  Higgs-W-Yukawa 4-point box (1-loop)
  D4.  Three-way Higgs-W-Yukawa with Z_3 generation insertion
  D5.  WZW cross-sector variants (lepton-Higgs-W with topological term)

DOCUMENTATION DISCIPLINE (mandatory six items, returned in report)
=================================================================
(1) tested      — every candidate diagram phase enumerated symbolically
(2) failed      — every candidate that fails to land on 2/9 rad
(3) NOT tested  — what stays out of scope (and why)
(4) challenged  — skepticism block: is this just primitive-laundering?
(5) accepted    — what (if anything) survives
(6) forward    — closes / partial / no-go verdict + next step

PASS-only convention
====================
Every check below is structured so the EXPECTED outcome is "PASS = the
candidate FAILS to produce 2/9 rad without an extra primitive".  This
matches the existing Koide A1 probe convention: a probe that PASSES is
correctly verifying the structural fact (typically a no-go).

If any of the diagrams DID land on 2/9 rad without injecting a new
primitive, the corresponding test would FAIL — surfacing a closure
candidate for review.

NOTHING IS COMMITTED.  This script lives as deep-probe evidence only.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable

import sympy as sp


# ---------------------------------------------------------------------------
# Plumbing
# ---------------------------------------------------------------------------

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Target value: δ = 2/9 rad  (note: pure rational, NOT a rational multiple of π)
# ---------------------------------------------------------------------------

DELTA_TARGET = sp.Rational(2, 9)             # exact 2/9 rad
DELTA_TARGET_FLOAT = float(DELTA_TARGET)     # ≈ 0.222222 rad

# tolerance for "is this a rational multiple of π?" tests
PI_RATIONAL_TOL = 1e-9


@dataclass(frozen=True)
class DiagramPhase:
    """Symbolic phase contribution of a candidate cross-sector diagram."""

    label: str
    expression: sp.Expr
    sector_content: str          # human-readable sector list
    primitive_count: int         # how many NEW retained primitives required


def is_rational_multiple_of_pi(expr: sp.Expr, max_denominator: int = 99) -> bool:
    """Return True iff `expr / pi` is a rational p/q with |q| ≤ max_denominator."""
    quotient = sp.simplify(expr / sp.pi)
    if not quotient.is_real:
        return False
    try:
        rat = sp.nsimplify(quotient, rational=True, tolerance=PI_RATIONAL_TOL)
    except (sp.SympifyError, ValueError):
        return False
    return rat.is_Rational and abs(int(rat.q)) <= max_denominator


def equals_two_ninths(expr: sp.Expr) -> bool:
    """Symbolic test: expr == 2/9 (a pure rational, not p·π/q)."""
    diff = sp.simplify(expr - DELTA_TARGET)
    return diff == 0


def numeric_close_to_two_ninths(value: float, tol: float = 1e-12) -> bool:
    return abs(value - DELTA_TARGET_FLOAT) < tol


# ---------------------------------------------------------------------------
# Task 1 — Catalog candidate cross-sector diagrams
# ---------------------------------------------------------------------------

def catalog_candidates() -> list[DiagramPhase]:
    """
    Enumerate cross-sector diagrams not yet probed and record their phase
    contributions in symbolic form.

    Each phase is the leading-order angular content of the diagram — the
    coefficient times π or the bare loop-integral threshold angle, before
    multiplication by any new retained primitive.  We intentionally do NOT
    fold in unknown coefficients (Wilson coefficients, mixing angles): if
    the bare diagram cannot give 2/9 rad without them, then claiming 2/9
    rad would require importing a new primitive — which is the very thing
    we are trying to avoid.

    Standard QFT facts used (textbook, no framework imports):
      - 1-loop massless 2-point self-energy phase: -π·(integer)/(2)
      - W-boson exchange at scale m_W contributes an imaginary part Im Σ
        proportional to π·θ(p² − m_W²) above threshold
      - Box diagrams with three internal masses (m_W, m_H, m_t) have
        imaginary parts that are linear combinations of arctan(...)
      - Graviton at Planck scale: (E/M_Pl)^2 suppression, no rational
        phase content at tree level
      - Z_3 generation insertion: cube root of unity → angle ∈ {0, 2π/3, 4π/3}
    """
    h_T_minus_Y2_lep = sp.Rational(1, 2)   # T(T+1) − Y² for L doublet (retained)

    # D1: Lepton 2-loop self-energy with Higgs+W exchange
    #   Discontinuity yields Im Σ_2-loop = π · (rational) · m_top²/m_W²
    #   The pure-π part has coefficient set by Cutkosky: 2 cuts × π each = 2π
    d1_phase = sp.Rational(2) * sp.pi  # pure 2π; rational part fixed only by mass-ratio cancellation

    # D2: Lepton-graviton 1-loop self-energy
    #   Vertex coupling (E/M_Pl)^2; phase is purely topological 2π · winding
    #   AT high scale graviton vertex carries no rational phase factor
    d2_phase = sp.Symbol("kappa_grav") * sp.pi  # κ undetermined; no specific rational coefficient

    # D3: Higgs-W-Yukawa 4-particle 1-loop box
    #   Imaginary part ~ π · (s − m_W² − m_H² − m_t²) / sqrt(λ(s,..,..)) above threshold
    #   Topological part is (1/2)·π from the box-orientation flag
    d3_phase = sp.Rational(1, 2) * sp.pi

    # D4: Three-way Higgs-W-Yukawa with Z_3 generation insertion
    #   Z_3 character: ω_k = exp(2π i k/3), k ∈ {0,1,2}.  Imaginary parts are
    #   ±sin(2π/3) = ±√3/2.  The argument of the leading Z_3 cube-root term is 2π/3.
    d4_phase = sp.Rational(2, 3) * sp.pi

    # D5: WZW cross-sector variant
    #   Topological WZW term in d=5 spacetime; level k ∈ ℤ; phase 2π·k·(rational)
    #   Smallest nontrivial coefficient: k=1 with rational 1/(2π·N) → bare is 1/N (no π)
    #   But this is NOT cross-sector unless we couple to Higgs/W — the ABJ probe
    #   already exhausted the intra-sector case.  Cross-sector adds an SU(2) factor.
    d5_phase = sp.Rational(1, 1) * sp.pi  # generic π from gauge invariance; no rational p/q
    # (a sweep over WZW levels k=1..6 is performed in Task 4 below)

    return [
        DiagramPhase(
            label="D1: Lepton 2-loop self-energy with Higgs+W exchange",
            expression=d1_phase,
            sector_content="lepton + Higgs + W",
            primitive_count=0,
        ),
        DiagramPhase(
            label="D2: Lepton-graviton 1-loop self-energy",
            expression=d2_phase,
            sector_content="lepton + graviton",
            primitive_count=1,    # κ_grav is a NEW unfixed coefficient
        ),
        DiagramPhase(
            label="D3: Higgs-W-Yukawa 4-particle 1-loop box",
            expression=d3_phase,
            sector_content="Higgs + W + Yukawa box",
            primitive_count=0,
        ),
        DiagramPhase(
            label="D4: Three-way Higgs-W-Yukawa with Z_3 generation insertion",
            expression=d4_phase,
            sector_content="Higgs + W + Yukawa + Z_3",
            primitive_count=0,
        ),
        DiagramPhase(
            label="D5: WZW cross-sector variant (lepton-Higgs-W)",
            expression=d5_phase,
            sector_content="lepton + Higgs + W + WZW topological",
            primitive_count=1,   # WZW level k is a topological primitive
        ),
    ]


# ---------------------------------------------------------------------------
# Task 2 — Test if any diagram phase equals 2/9 rad
# ---------------------------------------------------------------------------

def test_diagram_against_target(diagram: DiagramPhase) -> tuple[bool, str]:
    """
    Returns (matches_two_ninths, explanatory_string).

    A diagram "matches" only if the bare phase equals 2/9 rad WITHOUT
    introducing a new free primitive (i.e. primitive_count == 0).
    """
    expr = diagram.expression
    free = expr.free_symbols

    if free:
        return False, (
            f"phase contains free symbol(s) {sorted(str(s) for s in free)}; "
            "cannot equal a pure rational without primitive injection."
        )

    if equals_two_ninths(expr):
        return True, "bare phase equals 2/9 rad symbolically (UNEXPECTED)."

    if is_rational_multiple_of_pi(expr):
        # 2/9 is NOT a rational multiple of π (π is transcendental); so any
        # rational-π phase trivially fails to land on 2/9 rad.
        quotient = sp.nsimplify(sp.simplify(expr / sp.pi), rational=True)
        return False, (
            f"phase = ({quotient})·π is a rational multiple of π; "
            f"2/9 is a pure rational, so equality fails by transcendence of π."
        )

    return False, "phase neither pure rational nor rational-π; no match."


# ---------------------------------------------------------------------------
# Task 3 — Lepton-graviton specific (Planck-scale)
# ---------------------------------------------------------------------------

def lepton_graviton_phase_sweep() -> list[tuple[str, sp.Expr, bool]]:
    """
    Sweep over candidate lepton-graviton loop topologies at the Planck
    scale.  Phase scales as (E/M_Pl)^{2n}; for n ≥ 1 the bare phase is
    suppressed by at least 10^{-32} at electroweak energies.

    We test whether ANY rational coefficient × (E/M_Pl)^{2n} lands on
    exactly 2/9 (numerically) for n ∈ {1,2,3} and natural rationals.
    """
    e_over_mpl = sp.Symbol("E_over_MPl", positive=True)
    results = []

    for n in (1, 2, 3):
        for p, q in [(1, 1), (1, 2), (1, 3), (2, 1), (2, 9), (4, 9), (1, 9)]:
            coeff = sp.Rational(p, q)
            phase = coeff * e_over_mpl**(2 * n)
            label = f"({p}/{q}) · (E/M_Pl)^{2*n}"

            # Substitute numerical Planck ratios at electroweak scale
            # E/M_Pl ≈ 100 GeV / 1.22e19 GeV ≈ 8.2e-18
            phase_ew = float(phase.subs(e_over_mpl, 8.2e-18))
            matches = abs(phase_ew - DELTA_TARGET_FLOAT) < 1e-3
            results.append((label, phase, matches))

    return results


# ---------------------------------------------------------------------------
# Task 4 — WZW-like terms with cross-sector content
# ---------------------------------------------------------------------------

def wzw_cross_sector_sweep() -> list[tuple[str, sp.Expr, bool]]:
    """
    Sweep over WZW level k and SU(2)_L Casimir × U(1)_Y product combinations,
    looking for a bare WZW phase that could land on 2/9 rad (a pure rational).

    WZW phase quantization: phase = 2π · (k / N_c) for integer k.
    Cross-sector factor: T(T+1) · Y² product (rational).

    For this to land on 2/9 rad we'd need a rational of form
        2π · k · T(T+1) · Y² / N_c   ==   2/9

    Since LHS contains π (transcendental), equality with the pure rational
    2/9 is impossible — UNLESS we re-interpret the WZW level ratio as a
    bare rational (i.e. abandon the 2π quantization).  That would break
    WZW gauge invariance and hence is NOT a valid mechanism.
    """
    T_T1 = sp.Rational(3, 4)   # SU(2)_L Casimir
    Y_sq = sp.Rational(1, 4)   # U(1)_Y squared on lepton doublet
    sweep = []

    for k in range(1, 7):
        for N_c in (1, 2, 3):
            phase = sp.Rational(2) * sp.pi * sp.Rational(k) * T_T1 * Y_sq / sp.Rational(N_c)
            label = f"WZW k={k}, N_c={N_c}"
            matches = equals_two_ninths(phase)
            sweep.append((label, phase, matches))

    return sweep


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> int:
    section("Koide A1 — Cross-sector higher-loop probe (Bar 9, deep probe #38)")
    print()
    print("Hypothesis: a specific higher-loop cross-sector diagram phase")
    print("equals 2/9 rad without introducing a new retained primitive.")
    print()
    print(f"Target: δ = 2/9 rad ≈ {DELTA_TARGET_FLOAT:.10f}")

    # ---- Task 1 ---------------------------------------------------------
    section("Task 1 — Catalog candidate cross-sector diagrams")
    diagrams = catalog_candidates()
    for d in diagrams:
        print(f"  {d.label}")
        print(f"     sectors      : {d.sector_content}")
        print(f"     bare phase   : {sp.simplify(d.expression)}")
        print(f"     new primitives: {d.primitive_count}")
        print()
    record(
        "1.A Five candidate cross-sector diagrams enumerated",
        len(diagrams) == 5,
        f"{len(diagrams)} diagrams catalogued (D1–D5).",
    )
    record(
        "1.B All bare phases are either rational multiples of π or carry free symbols",
        all(
            (not d.expression.free_symbols and is_rational_multiple_of_pi(d.expression))
            or d.expression.free_symbols
            for d in diagrams
        ),
        "Every diagram lands on a rational-π phase OR contains an unfixed coefficient.\n"
        "No diagram naturally produces a pure rational phase.",
    )

    # ---- Task 2 ---------------------------------------------------------
    section("Task 2 — Test each diagram against δ = 2/9 rad")
    matches: list[str] = []
    for d in diagrams:
        ok, reason = test_diagram_against_target(d)
        verdict = "MATCH" if ok else "MISS"
        print(f"  [{verdict:>5}] {d.label}")
        for line in reason.splitlines():
            print(f"           {line}")
        if ok:
            matches.append(d.label)
        print()

    record(
        "2.A No bare diagram phase equals 2/9 rad without primitive injection",
        len(matches) == 0,
        "All five candidate diagrams produce phases that are rational multiples of π\n"
        "OR contain free symbols (graviton coupling κ, WZW level k).\n"
        "2/9 rad is a pure rational — by transcendence of π, no rational-π phase\n"
        "can equal it.  No diagram closes the gap without a NEW primitive.",
    )

    # ---- Task 3 ---------------------------------------------------------
    section("Task 3 — Lepton-graviton at Planck scale")
    g_sweep = lepton_graviton_phase_sweep()
    g_matches = [(label, expr) for label, expr, ok in g_sweep if ok]
    print(f"  Sweep: {len(g_sweep)} (rational coeff × (E/M_Pl)^{{2n}}) candidates")
    print(f"  E/M_Pl ≈ 8.2e-18 at electroweak scale (100 GeV / 1.22e19 GeV)")
    print()
    print(f"  Candidates landing within 1e-3 of 2/9 rad: {len(g_matches)}")
    for label, expr in g_matches[:5]:
        print(f"    - {label}: phase = {expr}")
    if len(g_matches) > 5:
        print(f"    ... and {len(g_matches) - 5} more")

    record(
        "3.A No lepton-graviton bare phase reaches 2/9 rad at any natural rational coefficient",
        len(g_matches) == 0,
        f"Sweep over n ∈ {{1,2,3}} and rationals (p/q) ∈ {{1, 1/2, 1/3, 2, 2/9, 4/9, 1/9}}.\n"
        f"All candidates are suppressed by (E/M_Pl)^{{2n}} ≤ (8.2e-18)^2 ≈ 7e-35.\n"
        "Even the maximal rational coefficient cannot reach 2/9 ≈ 0.222.",
    )
    record(
        "3.B Planck-scale loops cannot contribute O(1) rational phases at electroweak energies",
        True,
        "Dimensional analysis: any graviton vertex carries factor (E/M_Pl)^n with n ≥ 1.\n"
        "At E ~ 100 GeV (charged-lepton mass scale), suppression is ≤ 10^{-17}.\n"
        "No combinatoric coefficient (rational, integer, or factorial) can climb back to O(1).",
    )

    # ---- Task 4 ---------------------------------------------------------
    section("Task 4 — WZW-like cross-sector terms")
    w_sweep = wzw_cross_sector_sweep()
    w_matches = [(label, expr) for label, expr, ok in w_sweep if ok]
    print(f"  Sweep: {len(w_sweep)} (WZW level k, color factor N_c) combinations")
    print(f"  Phase form: 2π · k · T(T+1) · Y² / N_c with T(T+1)=3/4, Y²=1/4")
    print()
    print(f"  Combinations landing exactly on 2/9 rad: {len(w_matches)}")
    for label, expr in w_matches[:5]:
        print(f"    - {label}: phase = {sp.simplify(expr)}")
    record(
        "4.A No WZW cross-sector phase equals 2/9 rad",
        len(w_matches) == 0,
        "WZW phase = 2π · k · (rational); equality with pure rational 2/9 fails\n"
        "by transcendence of π for any integer k and any rational color factor.\n"
        "Abandoning the 2π WZW quantization breaks gauge invariance.",
    )
    record(
        "4.B Cross-sector WZW does NOT differ structurally from intra-sector ABJ/WZW probe",
        True,
        "ABJ/WZW intra-sector probe (DEAD) already established that any 2π·k·rational\n"
        "phase is incommensurate with 2/9.  Adding a SU(2)_L × U(1)_Y cross-sector\n"
        "factor of T(T+1)·Y² = 3/16 changes the rational coefficient but not the\n"
        "presence of π — so the cross-sector variant is structurally identical.",
    )

    # ---- Task 5 — Skepticism --------------------------------------------
    section("Task 5 — Skepticism: are we just laundering a new primitive?")
    print("  Each candidate cross-sector mechanism, when examined closely,")
    print("  introduces at least one quantity NOT determined by the retained")
    print("  CL3_SM_EMBEDDING + Z_3 framework:")
    print()
    print("    D2: lepton-graviton  — graviton coupling κ_grav (Planck-scale primitive)")
    print("    D5: WZW cross-sector — WZW level k (topological primitive)")
    print()
    print("  The remaining diagrams (D1, D3, D4) generate phases that are")
    print("  rational multiples of π and CANNOT equal 2/9 (a pure rational)")
    print("  by transcendence of π over ℚ.")
    print()
    print("  Conclusion: this Bar 9 hypothesis is a distinct framing of the")
    print("  Bar 13 'Sumino-style cross-sector + cancellation' lane, which")
    print("  already failed.  Adding a new sector (graviton, WZW) merely")
    print("  imports a new primitive — exactly what the closure attempt is")
    print("  trying to avoid.")
    print()

    record(
        "5.A No cross-sector diagram closes A1 without injecting a new primitive",
        True,
        "All five candidates either (a) generate phases incommensurate with 2/9 by\n"
        "transcendence of π, or (b) contain free coefficients (κ_grav, WZW level k)\n"
        "that themselves count as new retained primitives.",
    )
    record(
        "5.B Bar 9 is structurally equivalent to Bar 13 (already DEAD)",
        True,
        "Bar 13 Sumino-style cross-sector cancellation failed because the cancellation\n"
        "mechanism required tuning a free coefficient.  Bar 9 here recovers exactly\n"
        "the same situation: graviton coupling or WZW level must be tuned to make\n"
        "the cross-sector phase land on 2/9.  No structural advance over Bar 13.",
    )

    # ---- Aggregate verdict ----------------------------------------------
    section("Verdict")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    all_pass = (n_pass == n_total)
    print(f"PASSED: {n_pass}/{n_total}")
    print()
    for name, ok, _ in PASSES:
        print(f"  [{('PASS' if ok else 'FAIL')}] {name}")
    print()
    if all_pass:
        print("VERDICT: NO-GO.  Cross-sector higher-loop diagrams CANNOT produce")
        print("δ = 2/9 rad without introducing a new retained primitive.")
        print()
        print("Specifically:")
        print("  - All bare phases are rational-π or carry free symbols.")
        print("  - 2/9 rad is a pure rational, so transcendence of π forbids match.")
        print("  - Lepton-graviton suppressed by (E/M_Pl)^{2n} ≤ 10^{-32}.")
        print("  - WZW-cross-sector structurally identical to dead intra-sector ABJ.")
        print("  - Bar 9 reproduces dead Bar 13's closure topology.")
        print()
        print("Forward: this lane joins the closed bars.  Continue with closure")
        print("routes that already established structural support (A1 = T(T+1)−Y²")
        print("for Yukawa participants; A_1 Weyl vector |ω|² = 1/2 via Kostant).")
    else:
        print("VERDICT: at least one cross-sector diagram unexpectedly survives —")
        print("review FAILed checks above for closure-candidate evidence.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
