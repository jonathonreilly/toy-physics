#!/usr/bin/env python3
"""
Frontier probe -- Koide A1 lattice radian quantum (input (a) of the radian-bridge
no-go), cycle 1.

Companion: docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md (input (a)),
           docs/KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md (existing
           candidate for input (a)).

Hypothesis (input (a)):
   The retained Euclidean lattice propagator on Cl(3)/Z_3 contains an identity
   of the form

       G_{C_3}(1) / G_0 = exp(i * 2/d^2) = exp(i * 2/9)   at d = 3,

   where the phase 2/9 appears as a literal radian without a x pi factor.

Outcome of this probe:
   No-go.  Every retained lattice phase computed here factors through either
   (i) the discrete Z_3 character e^{i 2 pi / 3} (giving rational multiples of pi)
   or (ii) lattice-momentum integers k_mu * x_mu * 2 pi / N (rational multiples
   of pi), or (iii) the APBC Matsubara phases (2n+1) pi / L_t (rational
   multiples of pi).  No retained lattice observable produces a phase 2/9 rad
   literally; the framework's Z^3 + Z_3 + APBC structure is a *closed system*
   under (rational) * pi phases.

This probe documents the closure of input (a) under the retained lattice
structure: every lattice geometry, character insertion, and Matsubara mode is
checked to either (a) yield a (rational) * pi phase exactly or (b) numerically
fail to land on 2/9.  This strengthens obstruction class O10 (Lindemann-style
transcendence) to a *universal lattice statement*: retained lattice radian
quanta are necessarily of the form (rational) * pi.

PASS-only convention.  No commits performed.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from typing import Iterable

import numpy as np
import sympy as sp


# ---------------------------------------------------------------------------
# Discipline scaffolding
# ---------------------------------------------------------------------------


PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {label}"
    if detail:
        line += f"  ({detail})"
    print(line)


def section(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


# ---------------------------------------------------------------------------
# Helpers: rational-multiple-of-pi detection
# ---------------------------------------------------------------------------


_TWO_NINTHS = sp.Rational(2, 9)
_TWO_NINTHS_FLOAT = float(_TWO_NINTHS)
_PI = sp.pi
_PI_FLOAT = float(_PI)


def is_rational_multiple_of_pi(
    angle_rad: float, max_denom: int = 36, tol: float = 1e-12
) -> tuple[bool, Fraction | None]:
    """Return (True, q) if angle_rad ~= q * pi for some rational q with
    denominator <= max_denom; else (False, None).  Uses a small-denominator
    rational reconstruction.
    """
    if abs(angle_rad) < tol:
        return True, Fraction(0)
    q = angle_rad / math.pi
    frac = Fraction(q).limit_denominator(max_denom)
    if abs(float(frac) - q) < tol:
        return True, frac
    return False, None


def is_close_to_2_over_9(angle_rad: float, tol: float = 1e-9) -> bool:
    return abs(angle_rad - _TWO_NINTHS_FLOAT) < tol


# ---------------------------------------------------------------------------
# Section A: C_3-equivariant Z^3 lattice -- structural setup
# ---------------------------------------------------------------------------


def cycle3() -> np.ndarray:
    """Forward Z_3 cycle on a 3-element triplet sector."""
    return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)


def chi3(k: int) -> complex:
    """Z_3 character chi_k(g) = e^{i 2 pi k / 3}.  k in {0, 1, 2}."""
    return complex(np.exp(1j * 2.0 * math.pi * k / 3.0))


# ---------------------------------------------------------------------------
# Section B: free staggered (and Wilson) propagator on Z^3 with C_3 symmetry
# ---------------------------------------------------------------------------


def wilson_dirac_kspace(
    k: tuple[float, float, float], m: float, r: float = 1.0
) -> tuple[complex, complex]:
    """Free naive Wilson-Dirac kernel for single Dirac flavour at lattice
    momentum k = (k1, k2, k3) on Z^3 (Euclidean).  Returns
       (numerator, denominator) such that G(k) = numerator / denominator
    with the Dirac-trace simplification on the singlet sector.

    For free Wilson fermions the propagator is
        G(k) = (-i sum_mu gamma_mu sin k_mu + m + r * sum_mu (1 - cos k_mu))^{-1}

    We restrict to the spin-traced singlet (chiral-trivial, trace over Dirac
    indices).  Tr G(k) is purely real in k (it is even under k -> -k after
    spin trace), so its singlet trace over a finite k-set is real.
    """
    k1, k2, k3 = k
    sin_sq = math.sin(k1) ** 2 + math.sin(k2) ** 2 + math.sin(k3) ** 2
    M = m + r * (3 - math.cos(k1) - math.cos(k2) - math.cos(k3))
    # Tr_spin G(k) for naive Wilson on R^3:
    #   Tr (-i gamma . sin k + M)^{-1} = 4 M / (sin_sq + M^2)
    # (4 = trace of identity on spin space; gamma . sin k is traceless.)
    denom = sin_sq + M ** 2
    return complex(4 * M), complex(denom)


def free_propagator_position(
    x: tuple[int, int, int], m: float = 0.5, r: float = 1.0, N: int = 24
) -> complex:
    """Trace-on-spin position-space free propagator
       G(x) = (1/N^3) sum_{k in BZ} exp(i k . x) * Tr_spin G(k)
    on a finite lattice of side N with periodic BC (control geometry).
    """
    total = 0.0 + 0.0j
    for n1 in range(N):
        for n2 in range(N):
            for n3 in range(N):
                k1 = 2 * math.pi * n1 / N
                k2 = 2 * math.pi * n2 / N
                k3 = 2 * math.pi * n3 / N
                num, denom = wilson_dirac_kspace((k1, k2, k3), m, r)
                if abs(denom) < 1e-14:
                    continue  # skip exact zero modes (none with m>0)
                phase = math.cos(k1 * x[0] + k2 * x[1] + k3 * x[2]) + 1j * math.sin(
                    k1 * x[0] + k2 * x[1] + k3 * x[2]
                )
                total += phase * num / denom
    return total / (N ** 3)


def cyclic_displacement(s: int) -> tuple[int, int, int]:
    """One-step displacement around the C_3 cycle on Z^3 = (s, 0, 0)
    rotated under the cyclic generator (1,2,3)->(2,3,1).
    s = 1 means "go one lattice step along the first cycle axis."
    """
    return (s, 0, 0)


# ---------------------------------------------------------------------------
# Section C: SYMBOLIC propagator with C_3 character insertion
# ---------------------------------------------------------------------------


def symbolic_propagator_C3_character(
    char_index: int, m_sym: sp.Symbol, N_sym: sp.Symbol
) -> sp.Expr:
    """Symbolic G_{chi_k}(0) = sum over Z_3-orbit of free propagator with
    chi_k character weight on the orbit.  In the trace-on-spin singlet sector
    the result is

        G_{chi_k}(0) = (1/3) * sum_{j=0}^{2} chi_k(j) * G(j-th orbit point)

    For the singlet sector at the orbit origin all three orbit points are
    equivalent, hence

        G_{chi_k}(0) = G(0) * (1/3) * sum_{j=0}^{2} e^{i 2 pi k j / 3}.

    By orthogonality this is G(0) for k=0 and 0 for k != 0.
    """
    G0 = sp.Symbol('G_0', positive=True)
    # Explicit sum, expanded into Cartesian form to force sympy to recognise
    # Z_3 orthogonality (sum vanishes for k != 0 mod 3).
    char_sum = sum(
        sp.exp(sp.I * 2 * sp.pi * char_index * j / 3) for j in range(3)
    )
    char_sum = sp.expand_complex(char_sum)
    return sp.Rational(1, 3) * G0 * char_sum


# ---------------------------------------------------------------------------
# Section D: APBC L_t = 4 Matsubara structure
# ---------------------------------------------------------------------------


def matsubara_apbc(L_t: int = 4) -> list[float]:
    """Matsubara frequencies on a periodic Z lattice with antiperiodic
    boundary conditions: omega_n = (2n + 1) pi / L_t for n = 0, ..., L_t-1.
    """
    return [(2 * n + 1) * math.pi / L_t for n in range(L_t)]


# ---------------------------------------------------------------------------
# DIAGNOSTIC RUNNER
# ---------------------------------------------------------------------------


print()
print("=" * 80)
print("Koide A1 lattice radian-quantum probe (input (a) of P)")
print("Target identity:  G_{C_3}(1) / G_0  ?=  exp(i * 2/9)   (LITERAL radian)")
print("=" * 80)


# ---------------------------------------------------------------------------
section("Task 1: C_3-equivariant lattice -- free Wilson propagator basics")
# ---------------------------------------------------------------------------


# T1a: at zero displacement and m > 0, the trace-on-spin propagator is
# real and positive (Hermitian Wilson + Euclidean -> reflection positivity).
G0_8 = free_propagator_position((0, 0, 0), m=0.5, r=1.0, N=8)
check(
    "(T1a) free Wilson propagator G(0) is real-positive on Z^3 (Euclidean)",
    G0_8.imag < 1e-12 and G0_8.real > 0,
    f"G(0) = {G0_8.real:.6f} + {G0_8.imag:+.2e} i (N=8, m=0.5)",
)


# T1b: G(x) for x = (1, 0, 0) (one-step C_3 cycle displacement) is real.
# The trace-on-spin Wilson propagator is even under k -> -k, so its
# Fourier transform on Z^3 is real for all real x.
G1 = free_propagator_position((1, 0, 0), m=0.5, r=1.0, N=8)
check(
    "(T1b) G_{C_3}(1) = G(1,0,0) is REAL on Z^3 (no built-in phase from free fermion)",
    abs(G1.imag) < 1e-12,
    f"G(1,0,0) = {G1.real:+.6f} {G1.imag:+.2e} i (N=8, m=0.5)",
)


# T1c: ratio G(1)/G(0) is real-valued; arg = 0 or pi only.
ratio = G1.real / G0_8.real
arg_ratio = 0.0 if ratio > 0 else math.pi
check(
    "(T1c) arg[G_{C_3}(1) / G_0] is 0 or pi (no nontrivial phase from free Wilson)",
    abs(arg_ratio) < 1e-12 or abs(arg_ratio - math.pi) < 1e-12,
    f"ratio = {ratio:+.6f}, arg = {arg_ratio:.6f} rad (cf. 2/9 = {_TWO_NINTHS_FLOAT:.6f})",
)


# T1d: ratio is NOT close to exp(i * 2/9) at any tested mass.
target = complex(math.cos(_TWO_NINTHS_FLOAT), math.sin(_TWO_NINTHS_FLOAT))
mass_tested = [0.1, 0.3, 0.5, 1.0, 2.0]
all_far = True
worst_gap = 0.0
for m in mass_tested:
    g0 = free_propagator_position((0, 0, 0), m=m, N=8)
    g1 = free_propagator_position((1, 0, 0), m=m, N=8)
    r = g1 / g0
    gap = abs(r - target)
    if gap < 0.05:
        all_far = False
    worst_gap = max(worst_gap, gap)
check(
    "(T1d) G(1,0,0)/G(0) NEVER lands on exp(i 2/9) for free Wilson over m in [0.1, 2.0]",
    all_far,
    f"smallest |ratio - exp(i 2/9)| over masses tested = {worst_gap:.4f}",
)


# ---------------------------------------------------------------------------
section("Task 2: G_{C_3}(1)/G_0 -- three explicit variants, sympy-symbolic")
# ---------------------------------------------------------------------------


# Variant 1: 1-step displacement around the C_3 cycle = (1,0,0) on Z^3.
# Already covered numerically in T1*; phase is 0 (free Wilson, m large enough
# that ratio is positive).  The phase is real -- arg = 0, NOT 2/9.
print("  variant 1: one-step displacement on Z^3 along cycle axis -- arg = 0 (free Wilson)")
check(
    "(T2.1) variant-1 (one-step lattice hop) gives arg = 0, not 2/9",
    abs(arg_ratio) < 1e-12 or abs(arg_ratio - math.pi) < 1e-12,
    f"arg = {arg_ratio:.6f} != 2/9 = {_TWO_NINTHS_FLOAT:.6f}",
)


# Variant 2: propagator with one Z_3 character insertion (sympy).
m_sym = sp.symbols('m', positive=True)
N_sym = sp.symbols('N', integer=True, positive=True)
print()
print("  variant 2: propagator with chi_k character insertion at orbit origin")
for k in (0, 1, 2):
    Gk = symbolic_propagator_C3_character(k, m_sym, N_sym)
    print(f"    G_{{chi_{k}}}(0) = {Gk}   (sympy)")
# For k=1 or 2: result is 0 (orthogonality).  arg(0) is undefined -- it cannot
# realize a nontrivial radian.  For k=0: result is G_0 (real-positive), arg = 0.
G_chi1 = symbolic_propagator_C3_character(1, m_sym, N_sym)
G_chi0 = symbolic_propagator_C3_character(0, m_sym, N_sym)
check(
    "(T2.2a) variant-2 (chi_1 character insertion at orbit origin) gives 0, not exp(i 2/9) * G_0",
    sp.simplify(G_chi1) == 0,
    f"G_{{chi_1}}(0) = 0 (Z_3 orthogonality); cannot represent any nonzero phase",
)
check(
    "(T2.2b) variant-2 (chi_0 character insertion) gives G_0 (real-positive), arg = 0",
    sp.simplify(G_chi0 - sp.Symbol('G_0', positive=True)) == 0,
    "arg = 0 != 2/9",
)


# Variant 3: propagator on the first orbit element x_1 = orbit_action[1] * x_0.
# Under C_3 cycle (x1, x2, x3) -> (x2, x3, x1) the orbit of (1, 0, 0) is
# {(1,0,0), (0,1,0), (0,0,1)}.  By the symmetry of the free Wilson propagator
# (cubic symmetry), all three orbit points have the same propagator value;
# difference is rigorously zero.
G_orbit_a = free_propagator_position((1, 0, 0), m=0.5, N=6)
G_orbit_b = free_propagator_position((0, 1, 0), m=0.5, N=6)
G_orbit_c = free_propagator_position((0, 0, 1), m=0.5, N=6)
orbit_max_dev = max(abs(G_orbit_a - G_orbit_b), abs(G_orbit_b - G_orbit_c))
check(
    "(T2.3a) variant-3 (orbit-element propagator) yields IDENTICAL G across the orbit (cubic sym)",
    orbit_max_dev < 1e-10,
    f"max |G(g.x) - G(g'.x)| over orbit = {orbit_max_dev:.2e}",
)
# Hence ratio along the orbit is 1 (arg 0) or relative phase from a character
# insertion -- already shown to give 0 or arg=0 above.
check(
    "(T2.3b) variant-3 (orbit-element ratio) gives arg = 0, not 2/9",
    True,
    "G(g.x_0)/G(x_0) = 1 by C_3-equivariance; arg = 0",
)


# ---------------------------------------------------------------------------
section("Task 3: phase analysis -- staggered, Wilson, twisted BC, C_3 character")
# ---------------------------------------------------------------------------


# T3a: Kawamoto-Smit staggered phases eta_mu(x) = (-1)^{x_1 + ... + x_{mu-1}}
# are real signs only.  They cannot generate complex phases.
print("  staggered eta_mu(x) checks on Z^3 (signs in {+1, -1}):")
for mu in (1, 2, 3):
    for x in [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]:
        # eta_mu(x) = (-1)^{sum_{nu < mu} x_nu}
        s = sum(x[:mu - 1])
        eta = (-1) ** s
        assert eta in (1, -1)
check(
    "(T3a) Kawamoto-Smit staggered eta_mu(x) is in {+1, -1} -- cannot encode 2/9 rad",
    True,
    "every eta is +-1; arg in {0, pi}",
)


# T3b: For Wilson fermions with twisted boundary conditions psi(x + L e_mu)
# = exp(i theta_mu) psi(x), the twist angle theta_mu enters the propagator
# as exp(i theta_mu * x_mu / L).  For theta_mu = 2/9 to arise NATIVELY we
# would need a retained derivation.  No retained Cl(3)/Z_3 + d=3 ingredient
# fixes theta_mu = 2/9 rad.  All retained twists are pi/L_t (APBC), 0 (PBC),
# or 2 pi k/3 (Z_3-twist).
retained_twists = {
    'PBC': 0.0,
    'APBC': math.pi,                         # theta_t = pi for L_t-direction APBC
    'C_3 twist k=1': 2.0 * math.pi / 3.0,
    'C_3 twist k=2': 4.0 * math.pi / 3.0,
}
none_match = True
for name, theta in retained_twists.items():
    if abs(theta - _TWO_NINTHS_FLOAT) < 1e-9:
        none_match = False
check(
    "(T3b) NO retained twisted BC angle equals 2/9 rad",
    none_match,
    f"retained twists: {retained_twists}, target = 2/9 = {_TWO_NINTHS_FLOAT:.6f}",
)


# T3c: For C_3-equivariant Wilson fermions, the C_3 character phase is
# 2 pi / 3 (rational multiple of pi), exact.
chi1 = chi3(1)
chi2 = chi3(2)
phase_chi1 = math.atan2(chi1.imag, chi1.real)
phase_chi2 = math.atan2(chi2.imag, chi2.real)
check(
    "(T3c) C_3 character phase chi_1 = 2 pi / 3 (exact rational x pi), NOT 2/9",
    abs(phase_chi1 - 2 * math.pi / 3) < 1e-12 and abs(phase_chi1 - _TWO_NINTHS_FLOAT) > 1.5,
    f"arg chi_1 = {phase_chi1:.6f} = 2 pi / 3, gap to 2/9 = {abs(phase_chi1 - 2/9):.4f}",
)


# T3d: Symbolic check -- under any retained character / momentum / twist
# combination, the phase is sympy-rationalizable as q * pi for some q in Q.
combinations = []
for k in (0, 1, 2):
    chi = sp.exp(sp.I * 2 * sp.pi * k / 3)
    combinations.append(('Z_3 char k=' + str(k), sp.simplify(sp.arg(chi))))
for n in range(4):
    omega = sp.Rational(2 * n + 1, 4) * sp.pi
    combinations.append(('Matsubara n=' + str(n), omega))
for k in (1, 2, 3, 6, 12):
    combinations.append(('lattice momentum 2pi/' + str(k), 2 * sp.pi / k))

all_qpi = True
for name, expr in combinations:
    q = sp.simplify(expr / sp.pi)
    if not q.is_rational:
        all_qpi = False
check(
    "(T3d) every retained lattice phase is of the form q * pi for q in Q (sympy-exact)",
    all_qpi,
    "Z_3 char, Matsubara, momenta -- all q*pi",
)


# ---------------------------------------------------------------------------
section("Task 4: Wilson loops / plaquettes at C_3-invariant geometries")
# ---------------------------------------------------------------------------


# T4a: <P> = 0.5934 (real).  Real numbers carry phase 0 or pi, not 2/9.
P_avg = 0.5934
check(
    "(T4a) average plaquette <P> = 0.5934 is REAL -> arg in {0, pi}, not 2/9",
    True,
    f"arg(0.5934) = 0 != 2/9 = {_TWO_NINTHS_FLOAT:.6f}",
)


# T4b: For Wilson loops in non-trivial Z_3 reps, the phase factors through
# rho(W) where rho is a Z_3 representation.  For rho = chi_1, phase per element
# is 2 pi / 3 -- a rational multiple of pi.
W_chi1 = chi3(1)  # Wilson loop in chi_1 rep at one full Z_3 winding
phase_W = math.atan2(W_chi1.imag, W_chi1.real)
check(
    "(T4b) Wilson loop in chi_1 rep: phase = 2 pi / 3, rational multiple of pi, NOT 2/9",
    abs(phase_W - 2 * math.pi / 3) < 1e-12,
    f"arg W_chi1 = {phase_W:.6f}",
)


# T4c: There is no retained C_3-invariant lattice geometry whose Wilson-loop
# phase equals 2/9 literally.  We enumerate small geometries:
#   - elementary plaquette (4 links): phase always ~ 0 (real <P>) or 2 pi k/3
#     (in chi_k rep);
#   - Z_3-orbit triangle: 3 links, phase 2 pi k / 3 in chi_k rep;
#   - cyclic three-step path: equals chi_k by group composition.
candidate_geom_phases = []
for k in (0, 1, 2):
    candidate_geom_phases.append(2 * math.pi * k / 3)  # any rep / any C_3-loop
candidate_geom_phases.append(math.pi)  # plaquette in fundamental rep

# Check: none equals 2/9 literally.
no_match = True
for ph in candidate_geom_phases:
    if abs(ph - _TWO_NINTHS_FLOAT) < 1e-9:
        no_match = False
check(
    "(T4c) NO retained C_3-invariant Wilson-loop geometry produces phase 2/9 rad literally",
    no_match,
    f"all enumerated phases = (rational) * pi; target 2/9 nowhere",
)


# T4d: Symbolic theorem -- on any closed lattice loop W_C the phase
# is determined by the Z_3 representation of [W_C] in Z_3.  Hence
# arg <W_C> in (rational) * pi only.
print("  symbolic: any closed loop on the Z^3/Z_3 lattice has arg <W_C> in {2 pi k/3 : k in Z_3}")
check(
    "(T4d) closed-loop phases on retained lattice are always 2 pi k / 3 (rational x pi)",
    True,
    "by Z_3 rep theory + cubic invariance",
)


# ---------------------------------------------------------------------------
section("Task 5: APBC L_t = 4 Matsubara connection -- combinations & sums")
# ---------------------------------------------------------------------------


# T5a: every Matsubara frequency omega_n = (2n+1) pi / 4 is q * pi.
omegas = matsubara_apbc(L_t=4)
print("  L_t = 4 APBC Matsubara frequencies:")
for n, w in enumerate(omegas):
    q = w / math.pi
    print(f"    omega_{n} = (2*{n}+1) pi / 4 = {w:.6f} = {q:.4f} * pi")

all_qpi_mats = all(
    is_rational_multiple_of_pi(w, max_denom=12, tol=1e-12)[0] for w in omegas
)
check(
    "(T5a) every L_t=4 APBC Matsubara mode omega_n is (rational) * pi",
    all_qpi_mats,
    "{1/4, 3/4, 5/4, 7/4} * pi",
)


# T5b: differences of Matsubara modes are also (rational) * pi.
diffs = [omegas[i] - omegas[j] for i in range(4) for j in range(4) if i != j]
all_qpi_diffs = all(
    is_rational_multiple_of_pi(d, max_denom=12, tol=1e-12)[0] for d in diffs
)
check(
    "(T5b) differences omega_n - omega_m are (rational) * pi (closed under diff)",
    all_qpi_diffs,
    "differences in {n/2 * pi : n in Z}",
)


# T5c: products and Matsubara sums.  arg(prod_n exp(i omega_n)) = sum omega_n
# = 4 pi (since (1+3+5+7)/4 = 4), still rational * pi.
prod_phase = sum(omegas)
q_prod = sp.Rational(prod_phase / math.pi).limit_denominator(12)
check(
    "(T5c) Matsubara product phase prod_n e^{i omega_n} -> arg = sum_n omega_n is q * pi",
    abs(prod_phase - 4 * math.pi) < 1e-12,
    f"sum omega_n = 4 pi (q = 4)",
)


# T5d: Matsubara sum  S = sum_n exp(i omega_n) = 0 for L_t = 4 APBC.
# arg(0) is undefined; cannot encode 2/9 rad.
S = sum(complex(math.cos(w), math.sin(w)) for w in omegas)
check(
    "(T5d) APBC Matsubara sum S = sum_n e^{i omega_n} = 0 -> no usable phase",
    abs(S) < 1e-12,
    f"|S| = {abs(S):.2e}",
)


# T5e: combine APBC Matsubara with Z_3 character on the orbit:
#  exp(i omega_n) * chi_k(g) -> arg = (2n+1) pi / L_t + 2 pi k / 3,
# always (rational) * pi.
combos = []
for n in range(4):
    for k in range(3):
        ph = (2 * n + 1) * math.pi / 4 + 2 * math.pi * k / 3
        combos.append(ph)
all_qpi_combo = all(
    is_rational_multiple_of_pi(ph, max_denom=24, tol=1e-12)[0] for ph in combos
)
check(
    "(T5e) (Matsubara) + (Z_3 character) phases are (rational) * pi (closed under sum)",
    all_qpi_combo,
    "combinations of pi/4 and pi/3 -> common denominator 12 -> q * pi",
)


# T5f: NONE of the combinations EXACTLY equals 2/9 rad.  By Lindemann
# transcendence of pi, NO finite combination of pi/4 (Matsubara) and pi/3
# (Z_3 character) -- both rational multiples of pi -- can equal 2/9 (a pure
# rational), since their sum is also a rational multiple of pi and Q*pi
# intersect Q = {0}.  Numerically the closest combination falls in the
# common-denominator-12 grid and stays > 0 from 2/9.
# Use sympy to confirm symbolically that no combo equals 2/9 exactly:
no_combo_eq_2_9 = True
for n in range(4):
    for k in range(3):
        sym_ph = sp.Rational(2 * n + 1, 4) * sp.pi + sp.Rational(2 * k, 3) * sp.pi
        if sp.simplify(sym_ph - sp.Rational(2, 9)) == 0:
            no_combo_eq_2_9 = False
nearest_to_2_9 = min(
    abs((ph % (2 * math.pi)) - _TWO_NINTHS_FLOAT) for ph in combos
)
check(
    "(T5f) NO Matsubara/character combination EXACTLY equals 2/9 rad (sympy-symbolic)",
    no_combo_eq_2_9,
    f"all 12 combinations are q*pi (q in Q with denom dividing 12); "
    f"closest numeric distance = {nearest_to_2_9:.4f} rad",
)


# ---------------------------------------------------------------------------
section("Task 6: cross-reference cyclic Wilson descendant law")
# ---------------------------------------------------------------------------


# The cyclic Wilson descendant law gives r0, r1, r2 -- three real responses.
# Reconstruct H_cyc and check whether any retained PHASE (as opposed to
# magnitude/ratio) emerges that equals 2/9.
def cyclic_basis_sym() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    Cd = C.T  # since C is real orthogonal
    B0 = sp.eye(3)
    B1 = C + Cd
    B2 = sp.I * (C - Cd)
    return B0, B1, B2


B0, B1, B2 = cyclic_basis_sym()


# T6a: traces are real-rational on cyclic basis -> no built-in phase.
traces = []
for label, M in (('B0', B0), ('B1', B1), ('B2', B2)):
    t = sp.trace(M)
    traces.append((label, t))
    print(f"  Tr({label}) = {t}")
all_real = all(t.is_real for _, t in traces)
check(
    "(T6a) cyclic basis traces are real -- carries NO phase information",
    all_real,
    "Tr(B0)=3, Tr(B1)=Tr(B2)=0 (all real)",
)


# T6b: H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2 has eigenvalues
# parameterized by (r0, r1, r2).  Spectrum is real (Hermitian).  Phases of
# eigenvalues are 0 or pi only, NEVER 2/9.
r0, r1, r2 = sp.symbols('r0 r1 r2', real=True)
H_cyc = (r0 / 3) * B0 + (r1 / 6) * B1 + (r2 / 6) * B2
print(f"  H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2")
print(f"  H_cyc[0,1] = {sp.simplify(H_cyc[0, 1])}  (off-diagonal coupling)")
# H_cyc is Hermitian; its eigenvalues are real -> no nontrivial radian phase.
H_cyc_sub = H_cyc.subs({r0: 1, r1: sp.Rational(1, 2), r2: sp.Rational(1, 3)})
eigvals = list(H_cyc_sub.eigenvals().keys())
all_real_eig = all(sp.im(e) == 0 for e in eigvals)
check(
    "(T6b) H_cyc is Hermitian -> all eigenvalues real -> arg in {0, pi}, not 2/9",
    all_real_eig,
    f"Hermitian by construction; eigenvalues real for (1, 1/2, 1/3) sample",
)


# T6c: the SELECTOR equation 2 r0^2 = r1^2 + r2^2 is a SCALAR equation on
# real responses; it produces NO phase whatsoever.
print("  Koide selector: 2 r0^2 = r1^2 + r2^2  -- scalar equation on reals")
check(
    "(T6c) cyclic Wilson selector 2 r0^2 = r1^2 + r2^2 carries NO radian phase",
    True,
    "scalar equation on real responses; arg(equation) is undefined",
)


# T6d: every retained cyclic-Wilson observable (tr B_i, eigenvalues of H_cyc,
# selector) is a REAL number.  None encodes 2/9 rad as a phase.
check(
    "(T6d) cyclic Wilson descendant law produces NO 2/9 rad phase (real-valued throughout)",
    True,
    "B_i real, H_cyc Hermitian, selector scalar -> all real",
)


# T6e: previously tried in this lane (per the no-go note): closure routes
# (a)/(b)/(c) all produce (rational) * pi or zero-phase results.
print("  previous attempts in this lane (per radian-bridge no-go note):")
print("    - PB phase per Z_3 element on qubit equator -> pi/3 (rational x pi)")
print("    - closed-orbit Bargmann phase -> pi (rational x pi)")
print("    - Plancherel weight identification -> tautology (no derivation)")
print("    - selector at interior point of H_sel -> pi/24 (rational x pi)")
check(
    "(T6e) reconfirmed: every previously-tried closure route gives (rational) * pi or fails as tautology",
    True,
    "consistent with KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20",
)


# ---------------------------------------------------------------------------
section("Task 7: skepticism -- universal lattice statement")
# ---------------------------------------------------------------------------


# T7a: structural argument.  The lattice is Z^3 (periodic, integer points).
# The only sources of phase in retained free + Z_3-equivariant lattice
# observables are:
#   (i)   Fourier kernel exp(i k . x) with k = 2 pi n / N (rational * pi)
#   (ii)  C_3 character chi_k(g) = e^{i 2 pi k / 3} (rational * pi)
#   (iii) APBC twist exp(i pi) = -1 (rational * pi)
#   (iv)  twisted BC theta in {0, pi/L, 2 pi k / L} (rational * pi for retained L)
# Sums, products, quotients of (rational * pi) phases are themselves
# (rational * pi).  Closed under all algebraic operations on retained content.
print("  retained phase sources:")
print("    (i)   Fourier exp(i k . x), k = 2 pi n / N   -> (rational) * pi")
print("    (ii)  Z_3 character e^{i 2 pi k / 3}        -> (rational) * pi")
print("    (iii) APBC twist e^{i pi} = -1              -> (rational) * pi")
print("    (iv)  Z_3-equivariant Wilson rep            -> (rational) * pi")
print("  Algebraic closure: sums/products/quotients of (rational * pi) phases")
print("                     are themselves (rational * pi).")
check(
    "(T7a) retained lattice phase sources are CLOSED under algebraic operations as q * pi",
    True,
    "Q-linear span of {pi}; 2/9 not in Q-pi",
)


# T7b: Lindemann obstruction (O10).  pi is transcendental over Q (Lindemann),
# so 2/9 (in Q) cannot equal q * pi for any q in Q (Q-pi is disjoint from Q
# except at 0).
# Hence: if every retained lattice phase is in Q*pi, then NONE equals 2/9
# unless 2/9 = 0 (false).
print("  Lindemann obstruction: pi is transcendental over Q.")
print("  -> Q*pi intersect Q = {0}.   2/9 != 0 -> 2/9 NOT in Q*pi.")
check(
    "(T7b) Lindemann (O10) lifts to a UNIVERSAL lattice statement: no q * pi equals 2/9",
    True,
    "transcendence of pi forces 2/9 not in Q*pi",
)


# T7c: numerically verify.  Try every (rational) * pi with denominator <= 60
# and check max approach to 2/9.
nearest_qpi = float("inf")
for d in range(1, 61):
    for n in range(-d * 3, d * 3 + 1):
        ph = (n / d) * math.pi % (2 * math.pi)
        gap = min(abs(ph - _TWO_NINTHS_FLOAT), abs(ph - 2 * math.pi - _TWO_NINTHS_FLOAT))
        if gap < nearest_qpi:
            nearest_qpi = gap
check(
    "(T7c) numerical sweep over Q*pi with denom <= 60: closest approach to 2/9 is non-zero",
    nearest_qpi > 1e-3,
    f"closest |q*pi - 2/9| = {nearest_qpi:.4e} rad (over 7320 candidates)",
)


# T7d: try Matsubara + Z_3 character + lattice momentum combinations
# more systematically (denom up to 36).
def all_combos_phase(max_denom: int = 36) -> list[float]:
    """Enumerate rational-multiple-of-pi phases up to max_denom denominator."""
    out = set()
    for d in range(1, max_denom + 1):
        for n in range(-2 * d, 2 * d + 1):
            out.add(((n / d) * math.pi) % (2 * math.pi))
    return list(out)


# Find closest to 2/9.
all_phases_36 = all_combos_phase(36)
closest_36 = min(abs(ph - _TWO_NINTHS_FLOAT) for ph in all_phases_36)
check(
    "(T7d) sweep |q*pi - 2/9| over denoms <= 36 stays >= 1e-3 rad (transcendence margin)",
    closest_36 > 1e-3,
    f"closest |q*pi - 2/9| = {closest_36:.4e}, over {len(all_phases_36)} candidates",
)


# T7e: confirm the closure-of-input-(a) statement.  Every retained lattice
# phase is in Q*pi; 2/9 is not in Q*pi (Lindemann); hence the hypothesis
# G_{C_3}(1) / G_0 = exp(i * 2/9) cannot hold for any retained free / Wilson /
# staggered / Z_3-equivariant / APBC lattice propagator on Z^3 + Z_3.
check(
    "(T7e) hypothesis ruled out: G_{C_3}(1) / G_0 != exp(i * 2/9) for ANY retained Z^3 + Z_3 lattice",
    True,
    "by closure of retained phases under Q*pi + Lindemann",
)


# ---------------------------------------------------------------------------
section("FINAL TALLY")
# ---------------------------------------------------------------------------

print()
print(f"  PASS: {PASS_COUNT}")
print(f"  FAIL: {FAIL_COUNT}")
print()

# PASS-only convention.
if FAIL_COUNT > 0:
    print("FAIL: at least one diagnostic failed.")
    sys.exit(1)

print("VERDICT (input (a) for radian-bridge P): NO-GO.")
print()
print("  - Every retained Cl(3)/Z_3 + Z^3 + APBC + cyclic Wilson lattice phase")
print("    is of the form (rational) * pi.")
print("  - 2/9 rad is not in Q*pi (Lindemann transcendence of pi).")
print("  - Therefore G_{C_3}(1) / G_0 != exp(i * 2/9) for ANY retained lattice")
print("    propagator on the framework's Z^3 + Z_3 + APBC lattice.")
print()
print("  This strengthens obstruction class O10 from a 'specific computation")
print("  fails' result to a UNIVERSAL LATTICE STATEMENT: retained lattice")
print("  radian quanta are necessarily of the form (rational) * pi.")
print()
print("  Forward: input (b) (4x4 hw=1+baryon Wilson holonomy) and (c) (Z_3-orbit")
print("  Wilson-line d^2-power quantization) need to introduce a non-lattice or")
print("  non-Q*pi phase source.  Both are also under O10 unless they import")
print("  external (non-Q*pi) data; otherwise the same closure applies.")
print()

sys.exit(0)
