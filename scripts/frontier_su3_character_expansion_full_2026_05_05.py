#!/usr/bin/env python3
"""Full character expansion of ⟨P⟩(β=6) on the framework's 3+1D Wilson surface.

KEY PATH 2 INSIGHT: the gap P_full - P_1plaq is in HIGHER IRREP contributions,
not in the connected mixed-cumulant series. Let me make this concrete.

Framework's character expansion:
  exp[(β/3) Re Tr U] = Σ_λ c_λ(β) χ_λ(U) / d_λ × d_λ
                    = Σ_λ c_λ(β) χ_λ(U)  (with proper convention)

For ⟨P⟩ at single plaquette: only χ_(1,0) term survives (Schur), giving:
  ⟨P⟩_1plaq = c_(1,0)/(3 c_(0,0))

For ⟨P⟩ at multi-plaquette (cube, larger): higher irreps couple via
plaquette joinings. The L→∞ value is the FULL sum over all irrep
configurations.

Question: can we compute the L→∞ value framework-natively from character
coefficients alone (not MC)?
"""
from __future__ import annotations
import numpy as np
from scipy.special import iv

BETA = 6.0
NMAX_IRREP = 8
NMAX_BESSEL = 200


def dim_su3(p, q):
    return (p+1) * (q+1) * (p+q+2) // 2


def c_lambda(p, q, beta=BETA):
    """SU(3) Wilson character coefficient via Bessel determinant."""
    arg = beta / 3.0
    lam = [p+q, q, 0]
    tot = 0.0
    for m in range(-NMAX_BESSEL, NMAX_BESSEL+1):
        mat = np.array([[iv(m+lam[j]+i-j, arg) for j in range(3)]
                        for i in range(3)], dtype=float)
        tot += float(np.linalg.det(mat))
    return tot


def main():
    print("=" * 72)
    print("FULL CHARACTER EXPANSION at β=6")
    print("=" * 72)

    # Compute c_λ for all irreps up to NMAX_IRREP
    print(f"\nCharacter coefficients c_λ(β=6) for (p,q) up to {NMAX_IRREP}:")
    print(f"{'λ=(p,q)':>10s}  {'dim_λ':>6s}  {'c_λ(β=6)':>16s}  {'c_λ/c_(0,0)':>14s}")

    cvals = {}
    c00 = c_lambda(0, 0)
    cvals[(0, 0)] = c00
    for p in range(NMAX_IRREP+1):
        for q in range(NMAX_IRREP+1):
            if p == 0 and q == 0:
                continue
            c = c_lambda(p, q)
            cvals[(p, q)] = c
            ratio = c / c00
            d = dim_su3(p, q)
            if abs(ratio) > 1e-15 or (p+q <= 4):
                print(f"  ({p},{q})    {d:6d}   {c:16.6e}   {ratio:14.6e}")

    # ============================================================================
    # 1-plaquette block: ⟨P⟩_1plaq = c_(1,0)/(3 c_(0,0))
    # ============================================================================
    print(f"\n{'='*72}")
    print(f"1-PLAQUETTE BLOCK (framework's V-invariant single-plaquette value)")
    print(f"{'='*72}")
    P_1plaq = cvals[(1, 0)] / (3 * c00)
    print(f"  P_1plaq(β=6) = c_(1,0)/(3·c_(0,0)) = {P_1plaq:.6f}")
    print(f"  This is the LEADING contribution from the (1,0) irrep only.")

    # ============================================================================
    # Where does the rest come from? Higher-irrep contributions
    # ============================================================================
    print(f"\n{'='*72}")
    print(f"HIGHER-IRREP CONTRIBUTIONS to ⟨P⟩(β=6) at L→∞")
    print(f"{'='*72}")

    # Standard SU(3) MC at L→∞ gives ⟨P⟩ = 0.5934
    # Single plaquette gives 0.4225
    # So ~0.17 comes from collective behavior (multi-plaquette correlations)
    P_MC = 0.5934
    gap = P_MC - P_1plaq
    print(f"\n  Standard MC L→∞: ⟨P⟩ = {P_MC}")
    print(f"  Single-plaquette: ⟨P⟩_1plaq = {P_1plaq:.4f}")
    print(f"  Gap: {gap:.4f} ({gap/P_MC*100:.1f}%)")

    # The gap comes from HIGHER irreps in the character expansion of (1/3) Re Tr U_p
    # AT THE L→∞ SURFACE (full multi-plaquette correlations)

    # On a single plaquette, Schur orthogonality → only (1,0) and (0,1) contribute
    # On multiple plaquettes with shared links, higher irreps appear via fusion

    # For the L→∞ effective single-plaquette description:
    # P_full(β) = c_(1,0)(β_eff)/(3 c_(0,0)(β_eff))
    # where β_eff(6) ≈ 9.30 (from inversion)

    print(f"\n  Reduction-law mapping P_full → P_1plaq(β_eff):")
    # Find β_eff such that P_1plaq(β_eff) = P_MC
    from scipy.optimize import brentq
    def diff(b):
        return c_lambda(1, 0, b) / (3 * c_lambda(0, 0, b)) - P_MC

    try:
        beta_eff = brentq(diff, 6, 15)
        print(f"  β_eff(6) such that P_1plaq(β_eff) = {P_MC}: β_eff = {beta_eff:.4f}")
        print(f"  Ratio β_eff/β = {beta_eff/BETA:.4f}")
    except Exception as e:
        print(f"  brentq failed: {e}")

    # ============================================================================
    # Closure candidate test: can β_eff(β) be derived from framework primitives?
    # ============================================================================
    print(f"\n{'='*72}")
    print(f"CLOSURE CANDIDATE #5: reduction-law β_eff determinacy")
    print(f"{'='*72}")
    print(f"""
Framework's reduction-existence theorem proves UNIQUE β_eff(β) on each
finite Wilson surface. The susceptibility-flow theorem gives ODE:
  β_eff'(β) = χ_L(β) / χ_1plaq(β_eff(β))

Per χ_L MC profile (separate run):
  χ_L(β) ≈ χ_1plaq(β) within MC noise across [1,6]

This implies β_eff'(β) ≈ 1, hence β_eff(6) ≈ 6, predicting P(6) ≈ 0.42.
But MC gives P(6) = 0.59, requiring β_eff(6) ≈ 9.3.

CONFLICT: framework's susceptibility-flow ODE with measured χ_L doesn't
reproduce the L→∞ ⟨P⟩ value.

POSSIBLE RESOLUTIONS:
  A. χ_L MC has statistical noise; better statistics needed
  B. Reduction-law theorem applies to specific reduction class not captured
     by simple flow integration
  C. χ_L → χ_L + corrections from DISCONNECTED multi-plaquette correlations
     not in our local-variance estimate
  D. Framework's reduction-law has additional structure (e.g., multi-step
     reduction) beyond simple ODE

CLOSURE STATUS:
  The reduction-law uniqueness theorem ITSELF doesn't close ⟨P⟩(6) without
  determining β_eff(6). The susceptibility-flow ODE alone (with MC χ_L)
  doesn't reproduce the L→∞ value. So candidate #5 doesn't directly close
  in current form.

POTENTIAL FRAMEWORK-SPECIFIC EXTENSION:
  If the reduction-law theorem can be sharpened to give EXPLICIT β_eff(β)
  in closed form (using framework primitives), we close. This would require
  computing the spectral measure of T_src(6) explicitly, which is the
  framework's "open object" per docs.
""")

    print(f"\n{'='*72}")
    print(f"NEXT INVESTIGATION: which framework primitive could pin β_eff(6)?")
    print(f"{'='*72}")
    print(f"""
The framework's TENSOR_TRANSFER_PERRON_SOLVE_NOTE identifies the open
object as the spectral measure ρ_(p,q)(6) of the unmarked spatial Wilson
environment. Three reference choices give:
  P_loc(6) = 0.4524 (ρ = 1, env = identity)
  P_triv(6) = 0.4225 (ρ = δ_(0,0), trivial env)
  Bridge candidate via constant-lift (DISPROVEN by slope theorem): 0.5935

If framework can derive ρ_(p,q)(6) framework-natively (without MC), we
close. But the framework's own no-go theorem says local Wilson data
doesn't fix ρ uniquely.

IMPLICATION: framework's CURRENT primitives genuinely don't analytically
determine ⟨P⟩(β=6). The closure search (Path 2) requires identifying
a NEW framework primitive that pins ρ_(p,q)(6) — not yet known.

For PRACTICAL PURPOSES: the theorem-grade L→∞ MC chain (separate runner)
gives bounded support for ⟨P⟩(β=6) ≈ 0.59 directly, without needing
analytic closure.

Path 2 closure remains a deep research question. The most promising
avenue is identifying additional Cl(3)/Z³ structural constraints on
the spatial environment ρ_(p,q)(6) — currently no such primitive exists.
""")


if __name__ == "__main__":
    main()
