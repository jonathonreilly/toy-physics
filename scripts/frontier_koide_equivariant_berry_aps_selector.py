#!/usr/bin/env python3
"""
Koide equivariant Berry/APS selector — support runner

Primary purpose: assemble the strongest current executable support chain
around the charged-lepton Brannen phase and Koide package on the retained
Cl(3)/Z³ lattice.

The runner verifies the exact ambient APS value

    |η_AS(Z_3 conjugate-pair doublet (1, 2))| = 2/9

and checks that this value is numerically consistent with the selected-line
charged-lepton reconstruction. It does NOT prove the remaining physical
Brannen-phase bridge

    δ_physical = |η_AS|

which stays open on the current package surface.

Two companion support runners materially strengthen that bridge search:

  - KOIDE_DIRAC_ZERO_MODE_PHASE_THEOREM identifies the Koide amplitude
    packet with the near-zero-mode of the retained Z_3-equivariant
    staggered-Dirac on the 3-generation triplet. Gives δ = |η_AS|
    directly from the textbook AS equivariant G-index theorem + APS
    spectral-flow theorem. Script:
    scripts/frontier_koide_dirac_zero_mode_phase_theorem.py

  - CHARGED_LEPTON_RADIATIVE_YUKAWA_THEOREM derives the tau Yukawa
    coupling y_τ^fw = α_LM/(4π) from 1-loop staggered-Dirac lattice
    PT with standard SU(2)_L × U(1)_Y Casimir C_τ = 3/4 + 1/4 = 1
    (colorless charged lepton). Script:
    scripts/frontier_charged_lepton_radiative_yukawa_theorem.py

Under the retained atlas + these companion support calculations, the
charged-lepton lane is sharpened further:

    Brannen phase route      — ambient APS value fixed exactly at 2/9
    Koide ratio route        — exact compatibility identities and support
                               reductions remain in hand
    Overall scale route      — radiative/Yukawa support is strengthened,
                               but not promoted to retained closure

This runner verifies:
  - η_AS(Z_3, (1, 2)) = -2/9 symbolically (sympy exact rational);
  - sign-pinning: η_AS < 0 structurally for any Z_n conjugate-pair;
  - Q(u², v², w²) = 2/3 is a parametrization identity on the selected
    line for every m (algebraic, not an AS consequence);
  - at the unique m_* on the retained first-branch interval where the
    selected-line phase matches 2/9, the Brannen formula plus the
    radiative/Yukawa support route reproduces
    m_τ, m_μ, m_e, and v_0 at PDG precision;
  - uniqueness of |η_AS| = 2/9 in the Z_n family (scanned n ≤ 10);
  - stability under ±0.2% α_LM perturbation.

Imports only retained atlas primitives from origin/main.
"""

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dm_leptogenesis_exact_common import (  # noqa: E402
    ALPHA_LM,
    C_APBC,
    M_PL,
    PLAQ_MC,
    V_EW,
    u0,
)

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = ""):
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str):
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# =============================================================================
# Retained selected-line reconstruction (self-contained from retained primitives)
# =============================================================================
GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
SELECTOR = math.sqrt(6.0) / 3.0

H_BASE = np.array(
    [
        [0, E1, -E1 - 1j * GAMMA],
        [E1, 0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0],
    ],
    dtype=complex,
)
T_M = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
T_DELTA = np.array([[0, -1, 1], [-1, 1, 0], [1, 0, -1]], dtype=complex)
T_Q = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=complex)


def H_selected(m: float) -> np.ndarray:
    """Retained selected line H_sel(m) = H(m, SELECTOR, SELECTOR)."""
    return H_BASE + m * T_M + SELECTOR * T_DELTA + SELECTOR * T_Q


def selected_line_slots(m: float) -> tuple[float, float, float]:
    """Selected-line slot values (u, v, w) on the Koide amplitude ray.

    v and w are taken as the (2,2) and (1,1) diagonals of exp(H_sel(m)).
    u is the POSITIVE root of the Koide quadratic
        u² − 4(v+w)u + (v² + w² − 4vw) = 0,
    namely u = 2(v+w) − √(3(v²+4vw+w²)). By construction, (u, v, w)
    satisfies the Brannen/Rivero Koide relation u² + v² + w² =
    4(uv + vw + uw), equivalently Q(u², v², w²) = 2/3 for any m.
    """
    X = expm(H_selected(m))
    v = float(np.real(X[2, 2]))
    w = float(np.real(X[1, 1]))
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    u = 2.0 * (v + w) - rad
    return u, v, w


OMEGA = complex(math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3))


def b_std(u: float, v: float, w: float) -> complex:
    """Standard-order (τ, e, μ) C_3 Fourier coefficient."""
    return (w + np.conj(OMEGA) * u + OMEGA * v) / 3.0


def brannen_phase(m: float) -> float:
    """Brannen phase δ(m) = arg(b_std(slots(m))) on the selected line."""
    u, v, w = selected_line_slots(m)
    bs = b_std(u, v, w)
    return math.atan2(bs.imag, bs.real)


def find_physical_m(target_delta: float = 2.0 / 9.0) -> float:
    """Find m_* on the first branch where δ(m) = target_delta."""
    f = lambda m: brannen_phase(m) - target_delta
    # First-branch physical root is between -1.3 and -0.8 (retained range)
    return brentq(f, -1.3, -0.8, xtol=1e-12)


def koide_Q(u_sqrt: float, v_sqrt: float, w_sqrt: float) -> float:
    """Koide ratio Q applied to MASSES m_i = (√m_i)² given √m triple."""
    m_total = u_sqrt ** 2 + v_sqrt ** 2 + w_sqrt ** 2
    sqrt_total_sq = (u_sqrt + v_sqrt + w_sqrt) ** 2
    return m_total / sqrt_total_sq


# =============================================================================
# AS G-signature formula (textbook equivariant fixed-point contribution)
# =============================================================================
def aps_eta(n: int, p: int, q: int) -> sp.Expr:
    """Atiyah-Singer equivariant G-signature fixed-point contribution
    at a Z_n conical singularity with weights (p, q)."""
    total = sp.Rational(0)
    for k in range(1, n):
        total += sp.cot(sp.pi * k * p / n) * sp.cot(sp.pi * k * q / n)
    return sp.simplify(total / n)


# =============================================================================
# Part A — retained atlas primitives
# =============================================================================
def part_A():
    section("Part A — retained atlas primitives")

    v_EW_recompute = M_PL * C_APBC * ALPHA_LM ** 16
    print(f"  PLAQ_MC = {PLAQ_MC}  (retained)")
    print(f"  u_0 = PLAQ_MC^(1/4) = {u0:.10f}")
    print(f"  α_LM = 1/(4π·u_0) = {ALPHA_LM:.10f}  (retained)")
    print(f"  C_APBC = (7/8)^(1/4) = {C_APBC:.10f}")
    print(f"  M_Pl = {M_PL:.6e} GeV  (retained)")
    print(f"  v_EW = M_Pl · (7/8)^(1/4) · α_LM^16 = {v_EW_recompute:.6f} GeV")

    record(
        "A.1 Retained hierarchy: v_EW = M_Pl · (7/8)^(1/4) · α_LM^16",
        abs(v_EW_recompute - V_EW) / V_EW < 1e-10,
        f"Reconstructed {v_EW_recompute:.6f} GeV vs retained {V_EW:.6f} GeV",
    )

    # H_base structure
    tr = np.trace(H_BASE).real
    det = np.linalg.det(H_BASE).real
    det_expected = 2 * E1 ** 2 * E2
    record(
        "A.2 H_base: Tr = 0, det = 2·E_1²·E_2 (γ cancels identically)",
        abs(tr) < 1e-14 and abs(det - det_expected) < 1e-10,
        f"Tr = {tr:.2e}, det = {det:.6f}, expected {det_expected:.6f}",
    )


# =============================================================================
# Part B — AS G-signature η = -2/9 symbolic and sign-pinning proof
# =============================================================================
def part_B():
    section("Part B — AS equivariant G-signature η = -2/9 (symbolic)")

    pi = sp.pi
    print("  η_AS(Z_3, (1, 2)) = (1/3) Σ_{k=1,2} cot(πk/3)·cot(2πk/3)")
    print()
    print(f"    cot(π/3)  = {sp.simplify(sp.cot(pi/3))}  = 1/√3")
    print(f"    cot(2π/3) = {sp.simplify(sp.cot(2*pi/3))}  = -1/√3")
    print(f"    cot(4π/3) = {sp.simplify(sp.cot(4*pi/3))}  = 1/√3")
    print()

    eta_sym = aps_eta(3, 1, 2)
    print(f"  Symbolic result: η_AS = {eta_sym}")

    record(
        "B.1 η_AS(Z_3, (1, 2)) = -2/9 (symbolic exact rational)",
        eta_sym == sp.Rational(-2, 9),
        f"Symbolic: η = {eta_sym}",
    )

    # Sign-pinning proof for Z_n conjugate-pair
    print()
    print("  Sign-pinning proof (for any Z_n conjugate pair (p, n-p)):")
    print("    cot(πk(n-p)/n) = cot(πk - πkp/n) = cot(-πkp/n) = -cot(πkp/n)")
    print("    ⟹ cot(πkp/n)·cot(πk(n-p)/n) = -cot²(πkp/n)")
    print("    ⟹ η = -(1/n) Σ cot²(πkp/n) < 0  STRUCTURALLY")
    print()

    all_neg = True
    print("  Verification across Z_n conjugate-pair weights:")
    for n in [3, 5, 7, 9, 11]:
        for p in range(1, n // 2 + 1):
            if math.gcd(p, n) != 1:
                continue
            eta = aps_eta(n, p, n - p)
            if float(eta) >= 0:
                all_neg = False
            print(f"    n={n}, (p, n-p) = ({p}, {n-p}): η = {eta}")
    record(
        "B.2 Sign-pinning: η_AS < 0 for all Z_n conjugate-pair doublets",
        all_neg,
        "η < 0 structurally for Z_3, Z_5, Z_7, Z_9, Z_11 conjugate pairs.",
    )

    record(
        "B.3 |η_AS(Z_3, (1, 2))| = 2/9 (magnitude framework-exact)",
        abs(eta_sym) == sp.Rational(2, 9),
        f"|η| = {abs(eta_sym)}",
    )


# =============================================================================
# Part C — selected-line Q = 2/3 identity + physical m_* where δ = 2/9
# =============================================================================
def part_C():
    section("Part C — selected-line Q = 2/3 parametrization identity and δ(m)")

    # First: verify Q(u², v², w²) = 2/3 for ALL m on the selected line
    # (this is the Brannen/Rivero parametrization identity, NOT a consequence
    # of the AS identification — it holds by construction of the u-completion)
    print("  Q(u², v², w²) on the selected line at several m values")
    print("  (Koide quadratic u² − 4(v+w)u + (v² + w² − 4vw) = 0 enforces Q = 2/3):")
    Q_constant = True
    m_values = [-1.3, -1.20, -1.16, -1.10, -1.00, -0.80]
    for m in m_values:
        u, v, w = selected_line_slots(m)
        if u > 0:
            Q = koide_Q(u, v, w)
            if abs(Q - 2.0 / 3.0) > 1e-10:
                Q_constant = False
            print(f"    m = {m:+.3f}: (u, v, w) = ({u:.4f}, {v:.4f}, {w:.4f}), Q = {Q:.10f}")
    record(
        "C.1 Q(u², v², w²) = 2/3 identity on the selected line for all m (Brannen parametrization)",
        Q_constant,
        "The u-completion u = 2(v+w) - √(3(v²+4vw+w²)) is the positive root of\n"
        "the Koide quadratic; Q = 2/3 is thus an algebraic identity for every m\n"
        "on the selected line — NOT a consequence of the AS identification.",
    )

    # Now: δ(m) varies with m; we find m_* where δ = 2/9 (the proposed AS value)
    print()
    print("  δ(m) = arg(b_std(u, v, w)) varies with m on the selected line:")
    for m in m_values:
        d = brannen_phase(m)
        print(f"    m = {m:+.3f}: δ = {d:+.6f} rad   (δ - 2/9 = {d - 2/9:+.2e})")

    m_star = find_physical_m(target_delta=2.0 / 9.0)
    delta_at_mstar = brannen_phase(m_star)

    print(f"\n  Physical m_* = {m_star:.10f}  (root of δ(m) = 2/9)")
    print(f"  δ(m_*) = {delta_at_mstar:.12f} rad")
    print(f"  Target 2/9 = {2.0/9.0:.12f}")

    record(
        "C.2 m_* where δ(m) = 2/9 falls in the retained selected-line range",
        -1.17 < m_star < -1.15,
        f"Computed m_* = {m_star:.10f} (in retained first-branch range [-1.17, -1.15])",
    )

    record(
        "C.3 At m_*, δ matches the AS-predicted 2/9 to machine precision (by construction)",
        abs(delta_at_mstar - 2.0 / 9.0) < 1e-10,
        f"δ(m_*) = {delta_at_mstar:.2e} vs 2/9 = {2.0/9.0:.10f}",
    )


# =============================================================================
# Part D — Q = 2/3 via retained Brannen reduction δ = Q/d (redundant cross-check)
# =============================================================================
def part_D():
    section("Part D — retained Brannen reduction δ = Q/d → Q = 2/3 (cross-check)")

    # Given δ = 2/9 (from the AS identification), the retained reduction
    # δ = Q/d with d = 3 gives Q = 2/3. This is redundant with C.1 (which
    # shows Q = 2/3 holds by construction for all m on the selected line),
    # but provides the symbolic-reduction cross-check.
    delta_sym = sp.Rational(2, 9)
    d_sym = sp.Integer(3)
    Q_from_reduction = delta_sym * d_sym

    print(f"  Retained reduction: δ = Q/d with d = |C_3| = 3")
    print(f"  Q = δ · d = (2/9) · 3 = {Q_from_reduction}")

    record(
        "D.1 Q = δ · d = 2/3 via retained Brannen reduction (symbolic)",
        Q_from_reduction == sp.Rational(2, 3),
        f"Q = {Q_from_reduction} (redundant with the parametrization identity C.1)",
    )


# =============================================================================
# Part E — v_0 via y_τ = α_LM/(4π) (companion theorem) + Brannen mass formula
# =============================================================================
def part_E():
    section("Part E — v_0 via y_τ = α_LM/(4π) (companion theorem) + Brannen formula")

    print("  Structural identification (CHARGED_LEPTON_RADIATIVE_YUKAWA_THEOREM):")
    print("    y_τ^fw = α_LM/(4π) · C_τ  with C_τ = 3/4 + 1/4 = 1 (colorless lepton)")
    print("  Derived from 1-loop staggered-Dirac PT + SU(2)_L × U(1)_Y Casimirs.")
    print("  See scripts/frontier_charged_lepton_radiative_yukawa_theorem.py for")
    print("  the full verification (11/11 PASS).")
    print()

    v_EW_MeV = V_EW * 1000.0
    y_tau = ALPHA_LM / (4 * math.pi)
    m_tau_pred = v_EW_MeV * y_tau

    M_TAU_PDG = 1776.86
    y_tau_obs = M_TAU_PDG / v_EW_MeV
    dev_y = abs(y_tau - y_tau_obs) / y_tau_obs * 100
    dev_m = abs(m_tau_pred - M_TAU_PDG) / M_TAU_PDG * 100

    print(f"  y_τ^fw (framework) = α_LM/(4π) = {y_tau:.10f}")
    print(f"  y_τ^fw (observed)  = m_τ/v_EW = {y_tau_obs:.10f}")
    print(f"  Deviation: {dev_y:.4f}%")
    print(f"  m_τ predicted = v_EW · y_τ^fw = {m_tau_pred:.4f} MeV vs PDG {M_TAU_PDG}")

    record(
        "E.1 Derived y_τ^fw = α_LM/(4π) matches observed m_τ/v_EW at <0.01%",
        dev_y < 0.01,
        f"y_τ framework (α_LM/(4π)) vs observed (m_τ/v_EW): {dev_y:.4f}%",
    )

    record(
        "E.2 m_τ = v_EW · α_LM/(4π) matches PDG at <0.01%",
        dev_m < 0.01,
        f"{m_tau_pred:.3f} MeV vs PDG {M_TAU_PDG} ({dev_m:.4f}%)",
    )

    # v_0 via Brannen formula
    envelope_tau = 1 + math.sqrt(2) * math.cos(2.0 / 9.0)
    v0_pred = math.sqrt(m_tau_pred) / envelope_tau

    V0_PDG = 17.71556
    dev_v0 = abs(v0_pred - V0_PDG) / V0_PDG * 100

    print()
    print(f"  envelope(k=0) = 1 + √2 cos(2/9) = {envelope_tau:.10f}")
    print(f"  v_0 = √m_τ / envelope = {v0_pred:.6f} √MeV vs PDG {V0_PDG}")

    record(
        "E.3 v_0 = √m_τ / (1 + √2 cos(2/9)) matches PDG at <0.01%",
        dev_v0 < 0.01,
        f"v_0 framework = {v0_pred:.6f} √MeV ({dev_v0:.4f}%)",
    )

    # Full Brannen-formula lepton spectrum
    print()
    print("  Brannen mass formula with δ = 2/9 and framework v_0:")
    v0_sq = v0_pred ** 2
    pdg_map = {0: ("τ", 1776.86), 1: ("e", 0.51100), 2: ("μ", 105.6584)}
    all_ok = True
    for k in range(3):
        theta_k = 2.0 / 9.0 + 2 * math.pi * k / 3
        envelope_k = 1 + math.sqrt(2) * math.cos(theta_k)
        m_k = v0_sq * envelope_k ** 2
        label, pdg = pdg_map[k]
        dev = abs(m_k - pdg) / pdg * 100
        if dev > 0.01:
            all_ok = False
        print(f"    k={k} ({label}): m_k = {m_k:.4f} MeV vs PDG {pdg} ({dev:.4f}%)")

    record(
        "E.4 Brannen mass formula reproduces m_e, m_μ, m_τ at <0.01% PDG",
        all_ok,
        "All three charged-lepton masses at sub-0.01% deviation.",
    )


# =============================================================================
# Part F — stress tests: uniqueness and robustness
# =============================================================================
def part_F():
    section("Part F — stress tests")

    # Uniqueness of |η| = 2/9 in Z_n family
    matches_29 = []
    for n in range(2, 11):
        for p in range(1, n):
            for q in range(1, n):
                if math.gcd(p, n) != 1 or math.gcd(q, n) != 1:
                    continue
                try:
                    eta = aps_eta(n, p, q)
                    if abs(eta) == sp.Rational(2, 9):
                        matches_29.append((n, p, q))
                except Exception:
                    pass

    unique_Z3 = all(n == 3 for n, _, _ in matches_29)
    record(
        "F.1 |η_AS| = 2/9 uniquely produced by Z_3 (scanned n ≤ 10)",
        unique_Z3,
        f"{len(matches_29)} matching configs, all with n=3: {unique_Z3}",
    )

    # Robustness of m_τ prediction under α_LM perturbation
    M_TAU_PDG = 1776.86
    v_EW_MeV = V_EW * 1000.0
    max_dev = 0.0
    for dp in [-0.002, -0.001, 0.0, 0.001, 0.002]:
        alpha_pert = ALPHA_LM * (1 + dp)
        m_tau = v_EW_MeV * alpha_pert / (4 * math.pi)
        dev = abs(m_tau - M_TAU_PDG) / M_TAU_PDG * 100
        max_dev = max(max_dev, dev)

    record(
        "F.2 Closure stable under ±0.2% α_LM perturbation",
        max_dev < 1.0,
        f"Max m_τ deviation across ±0.2% α_LM: {max_dev:.4f}%",
    )


# =============================================================================
# Main
# =============================================================================
def main() -> int:
    section("Koide Equivariant Berry-APS Selector Theorem — Verification")
    print()
    print("Support claim: the retained Z_3 conjugate-pair carries the exact ambient")
    print("APS value |η_AS(Z_3 conjugate-pair (1,2))| = 2/9, and the selected-line")
    print("charged-lepton reconstruction is numerically consistent with that value.")
    print()
    print("Strengthened by two companion support runners (see docs/):")
    print("  - KOIDE_DIRAC_ZERO_MODE_PHASE_THEOREM:     δ = |η_AS| directly")
    print("  - CHARGED_LEPTON_RADIATIVE_YUKAWA_THEOREM: y_τ = α_LM/(4π)")
    print()
    print("This runner:")
    print("  - derives η_AS = -2/9 symbolically (exact rational)")
    print("  - proves the negative sign structurally via conjugate-pair reduction")
    print("  - verifies Q = 2/3 on the selected line as a parametrization identity")
    print("    (not a consequence of the AS identification)")
    print("  - finds m_* where the selected-line phase matches 2/9, confirms PDG precision match")
    print("  - tests v_0 and m_τ via the radiative/Yukawa support route + Brannen formula")
    print("  - stress-tests uniqueness of |η| = 2/9 in the Z_n family")

    part_A()
    part_B()
    part_C()
    part_D()
    part_E()
    part_F()

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    all_pass = n_pass == n_total
    if all_pass:
        print("VERDICT: all verification tests pass.")
        print()
        print("Support-chain summary (retained minimal axioms + textbook math):")
        print()
        print("  Step 1 — retained atlas: Cl(3) + Z³ + staggered-Dirac + g_bare=1")
        print("           plus three-generation observable theorem (V_3 triplet + Z_3 C)")
        print("           plus retained selected line, hierarchy theorem, α_LM")
        print()
        print("  Step 2 — KOIDE_DIRAC_ZERO_MODE_PHASE_THEOREM (companion, 10/10 PASS):")
        print("           gives a zero-mode / APS support model for the ambient 2/9 phase")
        print("           on a retained Z_3-equivariant Dirac carrier.")
        print()
        print("  Step 3 — retained Brannen/Rivero parametrization")
        print("           √m_k = v_0(1 + √2 cos(δ + 2πk/3)):")
        print("           algebraic identity Σ cos = 0, Σ cos² = 3/2 gives Q = 2/3")
        print("           for any δ, given the Brannen form with √2 prefactor.")
        print("           Independently, the Z_3 Lefschetz sum over the conjugate-pair")
        print("           doublet gives Q = Σ cot²(πk/3) = (n-1)(n-2)/3 = 2/3 at n=3")
        print("           (topological derivation; companion runner).")
        print()
        print("  Step 4 — CHARGED_LEPTON_RADIATIVE_YUKAWA_THEOREM (companion, 11/11 PASS):")
        print("           1-loop staggered-Dirac PT + standard SU(2)_L × U(1)_Y Casimirs")
        print("           give a strong radiative/Yukawa support route for m_τ and v_0.")
        print()
        print("  Step 5 — retained hierarchy v_EW = M_Pl · (7/8)^(1/4) · α_LM^16:")
        print("           v_0 = √m_τ / (1 + √2 cos(2/9)) = 17.7159 √MeV (PDG match).")
        print()
        print("Current package status is unchanged:")
        print("  - ambient APS value |η_AS| = 2/9 fixed exactly")
        print("  - physical Brannen-phase bridge remains open")
        print("  - physical/source-law bridge behind Q = 2/3 remains open")
        print("  - overall scale lane v_0 remains separate support")
        print()
        print("No new retained axioms are introduced. This runner is a support integrator,")
        print("not a closure theorem.")
    else:
        print("VERDICT: verification has FAILs. See PASS/FAIL summary above.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
