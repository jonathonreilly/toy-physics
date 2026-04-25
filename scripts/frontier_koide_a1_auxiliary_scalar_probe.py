#!/usr/bin/env python3
"""
Koide A1 closure — auxiliary scalar integration probe

TARGET: derive V_KN(Φ) = [2(Tr Φ)² − 3 Tr(Φ²)]² (the charged-lepton A1
forcing quartic) as a one-loop INDUCED effective potential obtained by
integrating out one or more auxiliary scalars coupled to gauge-invariant
Φ = Y†Y observables.

Prior probes established V_KN is NOT a single-trace Seeley-DeWitt heat
kernel coefficient (single-trace vs multi-trace obstruction), and NOT a
Coleman-Weinberg 1-loop potential at leading order (the CW form is
Tr f(Φ) which is single-trace).  The question here: does a PAIR of heat
kernels coupled through an auxiliary scalar generate the
specific multi-trace cross term (Tr Φ)²·Tr(Φ²) with the required
4:−12:9 ratio against (Tr Φ)⁴ and (Tr(Φ²))²?

ASSUMPTION-QUESTIONING HEAD (A1–A5)
-----------------------------------
A1  "Auxiliary scalars extend the retained framework."  An auxiliary
    scalar IS a new primitive unless it can be identified with an
    already-retained field (e.g., a composite of the Higgs or a gauge
    singlet allowed by CL3_SM_EMBEDDING).  This probe treats the scalar
    as a proxy for an as-yet-unidentified retained degree of freedom;
    if the resulting effective potential matches V_KN then the
    hypothesis "a scalar with this coupling exists in the retained
    spectrum" becomes falsifiable against the atlas.

A2  "1-loop is the right order."  Tree-level integration of a LINEAR-
    in-φ source already produces the leading multi-trace structure.
    One-loop (Gaussian) integration of a QUADRATIC-in-φ mass
    perturbation produces single-trace log structure at leading order.
    We test both tree-level (linear couplings) and 1-loop (quadratic
    couplings).  Higher-loop pieces only provide perturbative
    corrections to the leading algebraic structure and cannot overturn
    it — if the algebraic signature is wrong at leading order, loops
    will not fix it.

A3  "The induced potential should match V_KN EXACTLY."  Matching "up to
    positive multiplicative corrections" is sufficient: V_KN is a square,
    so multiplying by a positive overall factor preserves both the
    V_KN = 0 locus and the A1 vacuum.  What MUST match exactly is the
    RATIO 4:−12:9 between the three coefficients {T₁⁴, T₁²T₂, T₂²}, and
    the absence of T₁T₃ and T₄ at quartic order (otherwise the vacuum
    is shifted off A1).

A4  "Coupling the scalar to a gauge Casimir is natural."  This is false
    for fixed-irrep Casimirs (they are c-numbers).  What IS natural is
    coupling to FLAVOR-dependent gauge-invariant observables built from
    the Yukawa matrix Y — specifically Tr(Y†Y), Tr((Y†Y)²), det Y, etc.
    We restrict attention to polynomial couplings of this form.

A5  "The charged-lepton Yukawa is fundamental."  If Y is composite
    (e.g., Y = M_heavy⁻¹ · M_mix), V_KN might arise as a constraint on
    the compositeness structure rather than an effective potential.
    This probe does not explore compositeness; it treats Y as a
    fundamental scalar background and tests whether induced potentials
    on Y match V_KN.

STRATEGY
--------
Define Φ = Y†Y (Hermitian, 3×3).  V_KN expanded:

    V_KN = [2T₁ − 3T₂]²   with T₁ = Tr Φ, T₂ = Tr(Φ²)
         = 4T₁⁴ − 12T₁²T₂ + 9T₂²

so V_KN projects onto the mass-dim-8 trace-invariant basis
{T₁⁴, T₁²T₂, T₁T₃, T₂², T₄} with coefficients {4, −12, 0, 9, 0}.

For each vector Vk we:
  1. Write the full Lagrangian L[Y, φ] explicitly.
  2. Integrate out φ via Gaussian path integral (1-loop where mass²
     depends on Y; tree-level where a linear source exists).
  3. Expand V_eff[Y] to quartic order in Y.
  4. Project onto the 5-dim basis by explicit symbolic computation on
     a generic 3×3 Hermitian Φ.
  5. Extract coefficients and compare to V_KN's {4, −12, 0, 9, 0}.

Tested vectors: V1, V2, V3, V5 (with V4 and V6 addressed in discussion).
"""
from __future__ import annotations

import sys

import sympy as sp


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


# ---------------------------------------------------------------------------
# Basis projection helper
# ---------------------------------------------------------------------------

def generic_hermitian_phi() -> tuple[sp.Matrix, list[sp.Symbol]]:
    """Return a generic 3x3 real-diagonal Phi = diag(p1, p2, p3).

    Using a diagonal Hermitian is sufficient for projecting onto trace
    invariants because all traces depend only on eigenvalues.  We work
    with diagonal entries as independent symbols.
    """
    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)
    Phi = sp.diag(p1, p2, p3)
    return Phi, [p1, p2, p3]


def trace_invariants(Phi: sp.Matrix) -> dict[str, sp.Expr]:
    T1 = Phi.trace()
    Phi2 = Phi * Phi
    Phi3 = Phi2 * Phi
    Phi4 = Phi2 * Phi2
    T2 = Phi2.trace()
    T3 = Phi3.trace()
    T4 = Phi4.trace()
    return {"T1": sp.expand(T1), "T2": sp.expand(T2),
            "T3": sp.expand(T3), "T4": sp.expand(T4)}


def project_quartic(expr: sp.Expr, eigs: list[sp.Symbol]) -> dict[str, sp.Expr]:
    """Project a quartic symmetric polynomial in {p1, p2, p3} onto the
    4-dim basis {T1^4, T1^2 T2, T1 T3, T2^2}.

    Symmetric quartic polynomials in 3 variables form a 4-dim space
    (partitions of 4 into ≤3 parts: (4), (3,1), (2,2), (2,1,1)).  The
    conventional "5-dim" basis {T1^4, T1^2 T2, T1 T3, T2^2, T4} has one
    linear relation, Newton-Girard:

        T4 = T1^4/6 − T1^2 T2 + (4/3) T1 T3 + T2^2/2

    So we work in the 4-dim basis, converting any T4 content into the
    other four basis elements.  Any T4 in the input expression is first
    rewritten via this Newton-Girard relation.
    """
    p1, p2, p3 = eigs

    basis_syms = sp.symbols("c1 c2 c3 c4")
    c1, c2, c3, c4 = basis_syms

    # Build symbolic basis entries in the same variables.
    T1 = p1 + p2 + p3
    T2 = p1**2 + p2**2 + p3**2
    T3 = p1**3 + p2**3 + p3**3

    basis = [T1**4, T1**2 * T2, T1 * T3, T2**2]
    model = sum(ci * bi for ci, bi in zip(basis_syms, basis))

    # Evaluate on several numeric points to form a linear system.
    points = [
        (1, 2, 3),
        (2, 3, 5),
        (1, 1, 2),
        (1, 3, 7),
        (2, 5, 11),
        (3, 5, 7),
    ]
    equations = []
    for pt in points:
        subs = {p1: pt[0], p2: pt[1], p3: pt[2]}
        lhs = sp.simplify(sp.expand(expr).subs(subs))
        rhs = sp.simplify(model.subs(subs))
        equations.append(sp.Eq(lhs, rhs))

    sol = sp.solve(equations, basis_syms, dict=True)
    if not sol:
        raise RuntimeError("Projection failed; quartic polynomial may be out of basis span.")
    s = sol[0]
    for sym in basis_syms:
        if sym not in s:
            raise RuntimeError(f"Projection underdetermined; {sym} unresolved in {s}.")
    coeffs = {
        "T1^4":     sp.simplify(s[c1]),
        "T1^2 T2":  sp.simplify(s[c2]),
        "T1 T3":    sp.simplify(s[c3]),
        "T2^2":     sp.simplify(s[c4]),
    }

    # Also report the T4 coefficient IF the input is written as a pure
    # T4 monomial we should see a nonzero redistribution; compute the
    # projection of T4 onto the 4-dim basis explicitly: T4 = T1^4/6 −
    # T1^2 T2 + (4/3) T1 T3 + T2^2/2.
    coeffs["T4 (redistributed)"] = sp.Integer(0)  # we absorbed it

    # Sanity check: rebuild and compare.
    rebuilt = (coeffs["T1^4"] * T1**4
               + coeffs["T1^2 T2"] * T1**2 * T2
               + coeffs["T1 T3"] * T1 * T3
               + coeffs["T2^2"] * T2**2)
    diff = sp.simplify(sp.expand(expr) - sp.expand(rebuilt))
    if diff != 0:
        raise RuntimeError(f"Projection self-check failed; residual {diff}.")
    return coeffs


def coeff_ratio_signature(coeffs: dict[str, sp.Expr]) -> str:
    """Return a human-readable ratio signature as string."""
    keys = ["T1^4", "T1^2 T2", "T1 T3", "T2^2"]
    vals = [coeffs[k] for k in keys]
    # Try to extract a normalization: the first non-zero coefficient.
    nz = next((v for v in vals if sp.simplify(v) != 0), None)
    if nz is None:
        return "all zero"
    normalized = [sp.simplify(v / nz) for v in vals]
    return (f"[{normalized[0]} : {normalized[1]} : {normalized[2]} : "
            f"{normalized[3]}] (normalized by first nonzero)")


def v_kn_signature() -> dict[str, int]:
    """V_KN expanded coefficients in the 4-dim basis."""
    # V_KN = [2 T1^2 - 3 T2]^2 = 4 T1^4 - 12 T1^2 T2 + 9 T2^2
    return {"T1^4": 4, "T1^2 T2": -12, "T1 T3": 0, "T2^2": 9}


def compare_to_v_kn(name: str, coeffs: dict[str, sp.Expr]) -> tuple[bool, str]:
    """Check whether coeffs matches V_KN's {4, -12, 0, 9} up to a
    multiplicative constant (including sign).
    """
    target = v_kn_signature()
    keys = ["T1^4", "T1^2 T2", "T1 T3", "T2^2"]
    c = [sp.simplify(coeffs[k]) for k in keys]
    t = [target[k] for k in keys]

    if sp.simplify(c[0]) == 0:
        if any(sp.simplify(ck) != 0 for ck in c):
            return False, f"{name}: T1^4 coefficient is zero but non-T1^4 coeffs are nonzero; cannot match V_KN."
        return False, f"{name}: all quartic coefficients zero."

    lam = sp.simplify(c[0] / t[0])
    diffs = []
    for i, (ci, ti) in enumerate(zip(c, t)):
        want = sp.simplify(lam * ti)
        if sp.simplify(ci - want) != 0:
            diffs.append(f"{keys[i]}: got {ci}, want {want}")
    if diffs:
        return False, f"{name}: no global rescaling matches V_KN.\n" + "\n".join(diffs)
    # Additional check: sign must be positive (V_KN is non-negative).
    sign_note = ""
    try:
        lam_val = sp.nsimplify(lam)
        # If lambda is a concrete rational/symbolic product of positives, check sign.
        # For symbolic coupling products like g_a^2/(2m^2) this is positive.
        # Where an overall minus appears (from -(coupling^2)/m^2) we flag it.
        numerator = lam.as_numer_denom()[0]
        denominator = lam.as_numer_denom()[1]
        neg = (str(numerator).lstrip().startswith("-")) or (str(denominator).lstrip().startswith("-"))
        if neg:
            sign_note = " [WARNING: overall factor appears NEGATIVE — V_eff is −V_KN, maximum at A1]"
    except Exception:
        pass
    return True, f"{name}: matches V_KN (up to rescaling) with factor lam = {lam}.{sign_note}"


# ---------------------------------------------------------------------------
# Attack vectors
# ---------------------------------------------------------------------------

def vector_V1() -> tuple[dict[str, sp.Expr], str]:
    """V1: single scalar phi, linear source g · phi · Tr(Phi^2).

    L = (1/2)(dphi)^2 - (1/2) m^2 phi^2 - g phi Tr(Phi^2)
    EOM: m^2 phi = -g Tr(Phi^2)
    V_eff = -(g^2/(2 m^2)) [Tr(Phi^2)]^2   (tree-level)
    """
    Phi, eigs = generic_hermitian_phi()
    t = trace_invariants(Phi)
    g, m = sp.symbols("g m", positive=True)
    V_eff = -g**2 / (2 * m**2) * t["T2"]**2
    coeffs = project_quartic(V_eff, eigs)
    # Also include a 1-loop variant: coupling (1/2) g^2 phi^2 Tr(Phi^2)
    # gives mass^2(Phi) = m^2 + g^2 Tr(Phi^2); at 1-loop from ln det:
    # V_1loop ~ [mass^2(Phi)]^2 * (log...) -> proportional to (Tr Phi^2)^2.
    # Structurally same T2^2 signature.  We report the leading piece.
    narrative = (
        "V1 Lagrangian:  L = (1/2)(∂φ)^2 - (1/2) m^2 φ^2 - g φ Tr(Y†Y)^2\n"
        "EOM at Y-background:  m^2 φ* = -g Tr(Y†Y)^2\n"
        "Induced potential:     V_eff = -(g^2 / 2 m^2) [Tr(Y†Y)^2]^2\n"
        "Pure single-trace squared (T2^2).  No T1^4 or T1^2 T2 cross terms."
    )
    return coeffs, narrative


def vector_V2() -> tuple[dict[str, sp.Expr], str]:
    """V2: two scalars phi_1, phi_2, linear sources Tr(Phi) and Tr(Phi^2).

    L = sum_i [(1/2)(dphi_i)^2 - (1/2) m_i^2 phi_i^2]
        - g1 phi_1 (Tr Phi)^2 - g2 phi_2 Tr(Phi^2)
    Tree-level EOMs give additive contributions.
    V_eff = -(g1^2/(2 m1^2)) (Tr Phi)^4 - (g2^2/(2 m2^2)) [Tr Phi^2]^2
    """
    Phi, eigs = generic_hermitian_phi()
    t = trace_invariants(Phi)
    g1, g2, m1, m2 = sp.symbols("g1 g2 m1 m2", positive=True)
    V_eff = -g1**2/(2*m1**2) * t["T1"]**4 - g2**2/(2*m2**2) * t["T2"]**2
    coeffs = project_quartic(V_eff, eigs)
    narrative = (
        "V2 Lagrangian:  L = kinetic + masses - g1 φ_1 (Tr Y†Y)^2 - g2 φ_2 Tr(Y†Y)^2\n"
        "Note: the source for φ_1 is (Tr Y†Y)^2 so V_eff ~ [source]^2 = (Tr Y†Y)^4 = T1^4.\n"
        "Induced potential:  V_eff = -(g1^2/2m1^2) T1^4 - (g2^2/2m2^2) T2^2\n"
        "Signs are both negative; ratio cannot be tuned to 4:-12:9 because the\n"
        "cross term T1^2 T2 is absent (no φ_1-φ_2 mixing)."
    )
    return coeffs, narrative


def vector_V2_prime() -> tuple[dict[str, sp.Expr], str]:
    """V2': single scalar with mass^2(Phi) = m^2 + g2 Tr(Phi^2) AND linear
    source g1 (Tr Phi).

    L = (1/2)(dphi)^2 - (1/2)(m^2 + g2 Tr(Phi^2)) phi^2 - g1 phi (Tr Phi)
    Tree-level EOM: (m^2 + g2 Tr(Phi^2)) phi = -g1 Tr(Phi)
      -> phi* = -g1 Tr(Phi) / (m^2 + g2 Tr(Phi^2))
    V_eff = -(1/2) g1^2 (Tr Phi)^2 / (m^2 + g2 Tr(Phi^2))
    Expand to Phi^4:
      V_eff = -(g1^2/2m^2)(Tr Phi)^2 + (g1^2 g2 / 2 m^4)(Tr Phi)^2 Tr(Phi^2) + O(Phi^6)
    Leading quartic: (g1^2 g2 / 2 m^4) T1^2 T2 (pure cross term).
    """
    Phi, eigs = generic_hermitian_phi()
    t = trace_invariants(Phi)
    g1, g2, m = sp.symbols("g1 g2 m", positive=True)
    # Full V_eff:
    V_eff_full = -sp.Rational(1, 2) * g1**2 * t["T1"]**2 / (m**2 + g2 * t["T2"])
    # Series-expand in 1/m^2 ordering: keep to quartic in Phi.
    # Quadratic piece: -(g1^2 / 2m^2) T1^2 (mass-renormalization; not quartic).
    # Quartic piece:    +(g1^2 g2 / 2 m^4) T1^2 T2.
    # Extract quartic piece only (mass-dim-8 projection).
    V_quartic = sp.Rational(1, 2) * g1**2 * g2 / m**4 * t["T1"]**2 * t["T2"]
    coeffs = project_quartic(V_quartic, eigs)
    narrative = (
        "V2' Lagrangian:  L = (1/2)(∂φ)^2 - (1/2)(m^2 + g_2 Tr(Y†Y)^2) φ^2 - g_1 φ (Tr Y†Y)\n"
        "EOM: (m^2 + g_2 T2) φ* = -g_1 T1\n"
        "V_eff = -(1/2) g_1^2 T1^2 / (m^2 + g_2 T2)\n"
        "Quartic piece: +(g_1^2 g_2 / 2 m^4) T1^2 T2 (pure cross term).\n"
        "Lacks T1^4 and T2^2 at same order."
    )
    return coeffs, narrative


def vector_V2_plus() -> tuple[dict[str, sp.Expr], str]:
    """V2++: two scalars phi_1, phi_2 with a phi_1 phi_2 mixing term.

    L = (1/2) sum_i (dphi_i)^2 - (1/2) phi_vec^T M^2 phi_vec
        - g1 phi_1 T1^2 - g2 phi_2 T2
    where M^2 = [[m1^2, mu^2], [mu^2, m2^2]].

    Tree-level: phi_vec* = -(M^2)^{-1} g_vec.  V_eff = -(1/2) g^T (M^2)^{-1} g.
    """
    Phi, eigs = generic_hermitian_phi()
    t = trace_invariants(Phi)
    g1, g2, m1, m2, mu = sp.symbols("g1 g2 m1 m2 mu", positive=True)
    D = m1**2 * m2**2 - mu**4
    V_eff = -sp.Rational(1, 2) / D * (
        g1**2 * m2**2 * t["T1"]**4
        - 2 * g1 * g2 * mu**2 * t["T1"]**2 * t["T2"]
        + g2**2 * m1**2 * t["T2"]**2
    )
    coeffs = project_quartic(V_eff, eigs)

    # Note the constraint that forces V_KN ratio: D = 0 (singular mass matrix).
    # On D = 0, the construction degenerates — one scalar mode is massless,
    # integration is invalid, and the "residual" is a sigma-model constraint.

    narrative = (
        "V2++ Lagrangian (two mixing scalars):\n"
        "  L = (1/2) sum_i (∂φ_i)^2 - (1/2) φ^T M^2 φ - g_1 φ_1 T1^2 - g_2 φ_2 T2\n"
        "    with M^2 = [[m_1^2, μ^2], [μ^2, m_2^2]],  D := det M^2.\n"
        "V_eff = -(1/2D) [ g_1^2 m_2^2 T1^4 - 2 g_1 g_2 μ^2 T1^2 T2\n"
        "                  + g_2^2 m_1^2 T2^2 ].\n"
        "Basis coefficients depend on (g_1, g_2, m_1, m_2, μ, D).\n"
        "\n"
        "TUNING ANALYSIS: V_KN ratio 4:-12:9 requires\n"
        "  (i)  g_1^2 m_2^2 / (g_2^2 m_1^2) = 4/9\n"
        "  (ii) g_1 μ^2 / (g_2 m_1^2) = 2/3\n"
        "From (i)/(ii) one gets μ^4 = m_1^2 m_2^2, i.e. DETERMINANT D = 0.\n"
        "This is a SINGULAR mass matrix — one scalar mode becomes massless\n"
        "(flat direction), the Gaussian integration is invalid, and V_eff\n"
        "diverges.  The residual structure is a SIGMA-MODEL CONSTRAINT:\n"
        "the massless mode enforces g_1 T1^2 + g_2 T2 = 0.\n"
        "For the specific ratio g_1 : g_2 = 2 : -3, this IS the V_KN = 0\n"
        "locus (A1 condition).  But this is no longer a derivation; it is\n"
        "a RESTATEMENT of A1 as a sigma-model constraint."
    )
    return coeffs, narrative


def vector_V3() -> tuple[dict[str, sp.Expr], str]:
    """V3: single scalar coupled to the TRACELESS Hermitian projection
    of Phi, Phi~ = Phi - (T1/3) I.  With linear source g · phi · f(Tr Phi~^2)
    where f is linear (so source = g phi Tr(Phi - T1/3 I)^2 = g phi (T2 - T1^2/3)).

    EOM: m^2 phi = -g (T2 - T1^2/3)
    V_eff = -(g^2/(2 m^2)) (T2 - T1^2/3)^2
           = -(g^2/(2 m^2)) [T2^2 - (2/3) T1^2 T2 + T1^4/9]
           = -(g^2/(2 m^2)) (1/9) [T1^4 - 6 T1^2 T2 + 9 T2^2]
    Ratio: {1, -6, 0, 9, 0} (up to overall negative prefactor).
    Compare to V_KN's {4, -12, 0, 9, 0}.
    """
    Phi, eigs = generic_hermitian_phi()
    t = trace_invariants(Phi)
    g, m = sp.symbols("g m", positive=True)
    traceless_sq = t["T2"] - t["T1"]**2 / 3
    V_eff = -g**2/(2*m**2) * traceless_sq**2
    coeffs = project_quartic(V_eff, eigs)
    narrative = (
        "V3 Lagrangian:  L = (1/2)(∂φ)^2 - (1/2) m^2 φ^2 - g φ Tr[(Y†Y - (T1/3) I)^2]\n"
        "Source: g φ · (T2 - T1^2/3) (traceless projection of Tr(Φ^2)).\n"
        "V_eff = -(g^2/2m^2) (T2 - T1^2/3)^2\n"
        "     = -(g^2/18 m^2) [T1^4 - 6 T1^2 T2 + 9 T2^2]\n"
        "Ratio {T1^4 : T1^2 T2 : T2^2} = 1:-6:9.\n"
        "Compare V_KN ratio: 4:-12:9, equivalently 1:-3:9/4 after normalization.\n"
        "Both cross-term (−6 vs −3) and T2^2 (9 vs 9/4) coefficients differ.\n"
        "Also overall sign is NEGATIVE — would MAXIMIZE at A1, not minimize."
    )
    return coeffs, narrative


def vector_V3_adjusted() -> tuple[dict[str, sp.Expr], str]:
    """V3-adjusted: combine V3 (traceless Φ^2 source) with V2's (Tr Φ)^2 source.

    Can we tune couplings g_a, g_b to make the composite V_eff match V_KN?

    Source for a single scalar: g_a (T2 - T1^2/3) + g_b T1^2.
    V_eff = -(1/2m^2) [g_a (T2 - T1^2/3) + g_b T1^2]^2
           = -(1/2m^2) [ g_a^2 (T2 - T1^2/3)^2
                       + 2 g_a g_b T1^2 (T2 - T1^2/3)
                       + g_b^2 T1^4 ]
           = -(1/2m^2) [ g_a^2 (T2^2 - 2 T1^2 T2/3 + T1^4/9)
                       + 2 g_a g_b (T1^2 T2 - T1^4/3)
                       + g_b^2 T1^4 ]

    Collect coefficients in basis {T1^4, T1^2 T2, T2^2}:
        T1^4:   g_a^2/9 - 2 g_a g_b/3 + g_b^2
        T1^2 T2: -2 g_a^2/3 + 2 g_a g_b
        T2^2:   g_a^2

    Target V_KN ratio 4:-12:9  (T1^4 : T1^2 T2 : T2^2 = 4:-12:9).
    Normalize by T2^2: coefficient = g_a^2, so T2^2/T2^2 = 1.  We want 9:1 ratio,
    i.e. we need to rescale overall.  In the target V_KN = 4 T1^4 - 12 T1^2 T2 + 9 T2^2,
    so ratios w.r.t. T2^2 = 9 are: T1^4 = 4/9, T1^2 T2 = -12/9 = -4/3.

    Let x := g_b/g_a.  Then (dividing through by g_a^2):
        T1^4 coefficient: 1/9 - 2x/3 + x^2        = 4/9   ... (i)
        T1^2 T2 coef:     -2/3 + 2x               = -4/3  ... (ii)

    From (ii): 2x = -4/3 + 2/3 = -2/3, so x = -1/3.
    Check (i): 1/9 - 2(-1/3)/3 + 1/9 = 1/9 + 2/9 + 1/9 = 4/9.  ✓
    AND we need overall sign POSITIVE (V_KN ≥ 0).  Our V_eff has overall
    factor -(1/2m^2), so sign is WRONG.  Flip it by requiring mass^2 < 0
    (unphysical, a tachyon) OR using φ^2 with opposite sign, which
    breaks stability.  Without fine-tuning sign we cannot reproduce V_KN.
    """
    Phi, eigs = generic_hermitian_phi()
    t = trace_invariants(Phi)
    g_a, g_b, m = sp.symbols("g_a g_b m", real=True)
    source = g_a * (t["T2"] - t["T1"]**2 / 3) + g_b * t["T1"]**2
    V_eff = -sp.Rational(1, 2) / m**2 * source**2
    V_eff_expanded = sp.expand(V_eff)
    coeffs = project_quartic(V_eff_expanded, eigs)

    # Now specialize to the tuned ratio g_b = -g_a/3 and check if ratio matches V_KN.
    coeffs_tuned = {k: sp.simplify(v.subs(g_b, -g_a/3)) for k, v in coeffs.items()}

    narrative = (
        "V3-adjusted Lagrangian:\n"
        "  L = (1/2)(∂φ)^2 - (1/2) m^2 φ^2\n"
        "      - φ · [g_a (T2 - T1^2/3) + g_b T1^2]\n"
        "V_eff = -(1/2m^2) [g_a (T2 - T1^2/3) + g_b T1^2]^2\n"
        "Basis coefficients (pre-tune):\n"
        "  T1^4:   -(g_a^2/9 - 2 g_a g_b/3 + g_b^2)/(2 m^2)\n"
        "  T1^2 T2: -(-2 g_a^2/3 + 2 g_a g_b)/(2 m^2)\n"
        "  T2^2:   -g_a^2/(2 m^2)\n"
        "TUNING: both T1^4/T2^2 = 4/9 and T1^2T2/T2^2 = -12/9 constraints\n"
        "are simultaneously satisfied by x = g_b/g_a = -1/3 (quadratic roots\n"
        "are x = 1 or -1/3; only -1/3 satisfies BOTH constraints).\n"
        "Resulting V_eff = -(g_a^2/(18 m^2)) · V_KN EXACTLY.\n"
        "Ratio 4:-12:0:9 matched PRECISELY — this is a genuine algebraic hit.\n"
        "HOWEVER the overall coefficient is NEGATIVE: V_eff ≤ 0, with maximum\n"
        "V_eff = 0 ON A1.  The system is DRIVEN AWAY from A1 (prefers V_KN large).\n"
        "Obstructions to flipping sign:\n"
        "  - Tachyonic scalar (m^2 < 0): quantum instability, not a valid\n"
        "    tree-level integration.\n"
        "  - Fermion loop: would flip sign via Grassmann, but single fermion\n"
        "    loops give single-trace structure (ruled out by CW / SdW no-go).\n"
        "  - Constraint interpretation: if phi is forced to zero by other\n"
        "    dynamics (e.g., a Lagrange multiplier enforcing source=0),\n"
        "    then 2T1^2 = 3T2 holds on-shell — that IS V_KN = 0 = A1 locus.\n"
        "    This is the Koide-Nishiura sigma-model route (see Verdict)."
    )
    return coeffs_tuned, narrative


def vector_V5() -> tuple[dict[str, sp.Expr], str]:
    """V5: vector-like heavy lepton E at mass M, Yukawa coupling L̄ H Y_E E_R
    and M E_L bar E_R.  Integrate out E at 1-loop.

    Standard threshold integration yields effective Weinberg-type operators
    in the light sector.  For charged leptons with Y_e, the leading
    mass-dim-6 induced operator is:
        (1/M^2) |L̄ H|^2 Tr(Y_e^† Y_e)  -- single-trace
    At 1-loop with closed heavy loops, quartic Y operators appear:
        (c_a / M^4) Tr((Y^† Y)^2)  (single-trace, T4-type)
        (c_b / M^4) [Tr(Y^† Y)]^2  (double-trace, T2^2-type)
    The double-trace coefficient c_b ~ 1/(16pi^2) comes from the two-loop
    triangle-box diagram with a heavy loop closing back on itself.

    Even if we include single-trace T4 and double-trace T2^2 at comparable
    strength, there is no mechanism at one-loop to generate T1^4 or
    T1^2 T2 (those require DOUBLY closed loops with external Y-insertions
    summing traces of different subsectors — not a standard two-loop
    topology with one heavy field).

    So V5 gives at most {0, 0, 0, c_b, c_a} — no T1^4 or T1^2 T2.
    """
    Phi, eigs = generic_hermitian_phi()
    t = trace_invariants(Phi)
    c_a, c_b, M = sp.symbols("c_a c_b M", positive=True)
    V_eff = c_a / M**4 * t["T4"] + c_b / M**4 * t["T2"]**2
    coeffs = project_quartic(V_eff, eigs)
    narrative = (
        "V5 setup: heavy vector-like lepton E at mass M, integrated out at 1-loop.\n"
        "Induced quartic operators (leading in 1/M^4):\n"
        "  (c_a/M^4) Tr((Y†Y)^2)      [single-trace, T4]\n"
        "  (c_b/M^4) (Tr Y†Y)^2        [double-trace, T2^2]\n"
        "No mechanism generates T1^4 or T1^2 T2 from a single heavy field\n"
        "at 1-loop.  Ratio: {0, 0, 0, c_b, c_a} — missing T1^4 and T1^2 T2.\n"
        "V_KN NOT reproduced."
    )
    return coeffs, narrative


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    section("Koide A1 — auxiliary scalar integration probe")
    print()
    print("Target: V_KN = [2 T1^2 - 3 T2]^2 = 4 T1^4 - 12 T1^2 T2 + 9 T2^2")
    print("In 4-dim basis {T1^4, T1^2 T2, T1 T3, T2^2}: coeffs = {4, -12, 0, 9}.")
    print()
    print("(Newton-Girard relation for n=3: T4 = T1^4/6 - T1^2 T2 + (4/3) T1 T3 +")
    print(" T2^2/2, so the 5-fold basis {T1^4, T1^2 T2, T1 T3, T2^2, T4} is")
    print(" over-complete — symmetric quartics in 3 variables form a 4-dim")
    print(" space.  Any T4 contribution is reabsorbed into the 4-dim basis.)")

    # Sanity check V_KN itself.
    section("Sanity — V_KN expanded in the 4-dim basis")
    Phi, eigs = generic_hermitian_phi()
    t = trace_invariants(Phi)
    V_KN = (2 * t["T1"]**2 - 3 * t["T2"])**2
    kn_coeffs = project_quartic(sp.expand(V_KN), eigs)
    key_list = ["T1^4", "T1^2 T2", "T1 T3", "T2^2"]
    kn_show = {k: kn_coeffs[k] for k in key_list}
    print(f"  V_KN coefficients: {kn_show}")
    expected = v_kn_signature()
    match = all(sp.simplify(kn_coeffs[k] - expected[k]) == 0 for k in expected)
    record("Sanity: V_KN projects to {4, -12, 0, 9}", match,
           f"Got {kn_show}, expected {expected}.")

    # Vector tests.
    vectors = [
        ("V1", vector_V1),
        ("V2", vector_V2),
        ("V2'", vector_V2_prime),
        ("V2++", vector_V2_plus),
        ("V3", vector_V3),
        ("V3-adjusted", vector_V3_adjusted),
        ("V5", vector_V5),
    ]

    results_table: list[tuple[str, dict[str, sp.Expr], bool, str, str]] = []
    for name, fn in vectors:
        section(f"Vector {name}")
        coeffs, narrative = fn()
        print(narrative)
        print()
        print("Basis coefficients (4-dim quartic symmetric basis for 3 vars):")
        for k in ["T1^4", "T1^2 T2", "T1 T3", "T2^2"]:
            print(f"  {k}: {coeffs[k]}")
        matches, reason = compare_to_v_kn(name, coeffs)
        status = "MATCH" if matches else "no-match"
        sig_ratio = coeff_ratio_signature(coeffs)
        print()
        print(f"  signature ratio: {sig_ratio}")
        print(f"  V_KN match: {status} — {reason}")
        results_table.append((name, coeffs, matches, reason, sig_ratio))
        record(f"{name}: V_KN match check executed", True,
               f"match={matches}; signature={sig_ratio}")

    # Summary table
    section("Per-vector summary")
    print()
    print(f"{'Vector':<14} {'T1^4':<18} {'T1^2T2':<18} {'T2^2':<18} {'V_KN?':<12}")
    for name, coeffs, matches, _, _ in results_table:
        t14 = str(coeffs["T1^4"])
        t12t2 = str(coeffs["T1^2 T2"])
        t22 = str(coeffs["T2^2"])
        m = "YES" if matches else "no"
        print(f"{name:<14} {t14:<18} {t12t2:<18} {t22:<18} {m:<12}")

    section("Interpretation")
    print()
    print("  V1:  single scalar, linear source g φ T2.")
    print("       -> V_eff ∝ T2^2 only.  No T1^4, no cross term.  NOT V_KN.")
    print()
    print("  V2:  two scalars with sources T1^2 and T2.")
    print("       -> V_eff ∝ -(T1^4 + T2^2).  No cross term.  NOT V_KN.")
    print()
    print("  V2': single scalar with Φ-dependent mass and T1 source.")
    print("       -> V_eff leading quartic ∝ +T1^2 T2 only.  No T1^4 or T2^2 at")
    print("          same order.  NOT V_KN.")
    print()
    print("  V2++:  two mixing scalars.")
    print("       -> Full 3-term structure present BUT V_KN ratio constraint forces")
    print("          det(M^2) = 0 (massless mode), violating Gaussian integration.")
    print("          The V_KN match is realized as a SIGMA-MODEL CONSTRAINT at the")
    print("          singular-mass-matrix boundary — a restatement of A1, not a")
    print("          derivation.  (This is the Koide-Nishiura-type route.)")
    print()
    print("  V3:  single scalar coupled to trace-free (Φ - T1/3 I)^2.")
    print("       -> V_eff ∝ -[T1^4 - 6 T1^2 T2 + 9 T2^2] (ratio 1:-6:9).")
    print("          Ratios don't match V_KN (1:-3:9/4 when normalized).  Also")
    print("          overall sign wrong.")
    print()
    print("  V3-adjusted: compose traceless + pure-T1^2 sources with tuned ratio.")
    print("       -> By choosing g_b = -g_a/3 the ratio becomes EXACTLY 4:-12:9.")
    print("          BUT overall prefactor is -g_a^2/(2 m^2) — NEGATIVE.")
    print("          V_eff is then -(const) · V_KN, MAXIMIZED at A1.")
    print("          Requires tachyonic scalar (m^2 < 0) to flip sign → unstable.")
    print()
    print("  V5:  heavy vector-like lepton integrated out.")
    print("       -> V_eff ∝ T4 + T2^2.  No T1^4 or T1^2 T2 at 1-loop.  NOT V_KN.")
    print()
    print("  V4:  scalar coupled to gauge Casimir C_τ = T(T+1) + Y^2.")
    print("       -> c-number coupling; gives constant shift, no Φ-dependence.")
    print("          (A4 assumption-check rules this out analytically.)")
    print()
    print("  V6:  instanton-induced operators.")
    print("       -> Standard 't Hooft vertex ∝ det Y + c.c. → |det Y|^2 at quartic")
    print("          order ∝ (λ1 λ2 λ3)^2, which projects onto e_3^2.  Express in")
    print("          power sums: contains T1 T3, T4, (T1^2 - T2)^2 / 4 etc.  Does")
    print("          not give the V_KN ratio on {T1^4, T1^2 T2, T2^2}.")

    section("Status against assumptions A1–A5")
    print()
    print("  A1 Auxiliary scalars extend the framework:")
    print("     Matches V_KN algebraically only under V3-adjusted with TWO tuned")
    print("     couplings AND a tachyonic scalar.  This is NOT a natural")
    print("     retained-primitive extension.  Even the algebraic match requires")
    print("     fine-tuning g_b/g_a = -1/3, which has no atlas motivation.")
    print()
    print("  A2 1-loop is the right order:")
    print("     Tree-level integration (V1–V3) suffices for algebraic coefficient")
    print("     analysis.  1-loop Gaussian closures add ln(det) factors but don't")
    print("     change the basis structure at leading order.  Higher loops cannot")
    print("     rescue a mismatched signature — they only renormalize coefficients.")
    print()
    print("  A3 Match V_KN exactly:")
    print("     V_KN is positive definite.  Any induced V_eff that is NEGATIVE on")
    print("     the V_KN-locus (V3, V3-adjusted at natural sign) has MAXIMUM at A1")
    print("     rather than minimum — it DRIVES the system AWAY from A1.  No")
    print("     vector tested produces +V_KN-like shape.")
    print()
    print("  A4 Casimir coupling naturalness:")
    print("     Gauge Casimirs on FIXED IRREPS are c-numbers.  Flavor-dependent")
    print("     couplings must come from trace invariants of Y itself.  V4 is a")
    print("     dead end — see inline note.")
    print()
    print("  A5 Y composite rather than fundamental:")
    print("     Not tested here.  If Y = v · U / M_heavy is composite, V_KN could")
    print("     arise as a compositeness constraint (e.g., from an NJL-like")
    print("     four-fermion auxiliary field that itself has V_KN potential).")
    print("     This route is not excluded by the present probe; a separate probe")
    print("     on NJL-style compositeness would be needed.")

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total} checks")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    section("VERDICT")
    print()
    print("Algebraic findings:")
    print("  V1, V2, V2', V5:   missing basis elements — cannot form V_KN.")
    print("  V3:                wrong ratio (1:-6:9 vs V_KN's 1:-3:9/4).")
    print("  V3-adjusted:       EXACT V_KN ratio 4:-12:9 — but overall factor is")
    print("                     -g_a^2/(18 m^2), NEGATIVE.  V_eff = -const · V_KN,")
    print("                     maximum at A1, destabilizing.")
    print("  V2++:              can realize V_KN ratio only in det(M^2) -> 0 limit")
    print("                     (singular mass matrix -> Gaussian integration fails).")
    print("                     Residual is a sigma-model constraint g_1 T1^2 + g_2 T2 = 0,")
    print("                     which IS the V_KN = 0 locus if g_1 : g_2 = 2 : -3, but")
    print("                     this is a RESTATEMENT of A1 rather than a derivation.")
    print()
    print("Structural diagnosis:")
    print("  Integrating out a stable bosonic auxiliary with any polynomial source")
    print("  yields V_eff of definite sign — specifically V_eff = -(1/2) source^T M^{-2} source,")
    print("  which is NEGATIVE DEFINITE when M^2 > 0 (stability).  V_KN is positive")
    print("  definite.  So no stable-scalar integration can match V_KN with the")
    print("  correct sign.  The V3-adjusted algebraic hit is real, but the sign")
    print("  mismatch is STRUCTURAL, not a tuning problem.")
    print()
    print("To obtain +V_KN in an induced potential one would need:")
    print("  (i)   Fermionic loop (Grassmann sign flip): but fermion loops give")
    print("        single-trace structure -> ruled out by CW / SdW no-go note.")
    print("  (ii)  Multi-step integration: integrate out auxiliary A, which produces")
    print("        effective coupling for auxiliary B, which in turn is integrated.")
    print("        Each step flips sign, so even-many steps restore positive sign.")
    print("        This is in principle open and not explored here — see")
    print("        future-work note.")
    print("  (iii) Sigma-model constraint (V2++ singular limit): A1 as a constraint")
    print("        surface, not a minimum.  This is the Koide-Nishiura S_3 route,")
    print("        which imports V_KN as a primitive rather than deriving it.")
    print("  (iv)  Compositeness of Y (A5): not tested here.  If Y = M^{-1}·M',")
    print("        V_KN may arise as a constraint on compositeness kinematics.")
    print()
    print("CONCLUSION: within the single-auxiliary-scalar bosonic integration class")
    print("at one loop, V_KN is NOT DERIVABLE with the correct sign.  The ratio")
    print("matches under V3-adjusted fine-tuning, but sign is structurally wrong.")
    print("Obtaining +V_KN requires either (a) a multi-step bosonic cascade (open),")
    print("(b) a compositeness constraint (open), or (c) importing V_KN as a")
    print("primitive (the S_3 Koide-Nishiura route, equivalent to Route A in the")
    print("retained status note).  None is available from the retained framework")
    print("without adding a new primitive.")
    print()
    print("This corroborates the heat-kernel no-go (multi-trace vs single-trace):")
    print("bosonic 1-loop ln det gives single-trace structure, and upgrading to")
    print("multi-trace via auxiliary-scalar integration produces V_KN's ratio but")
    print("not its sign.  Both routes confirm the same underlying obstruction.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
