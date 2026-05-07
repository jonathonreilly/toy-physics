"""Heat-kernel SU(3) single-plaquette expectation at the framework's β=6 point.

Probe computation for the new-physics opening identified by the round-3
action-form-derivation agent. The framework's gauge action has been imported
as Wilson without being derived from Cl(3)/Z³. The Casimir-natural alternative
is heat-kernel:

    P_β(U) = Σ_λ d_λ · exp(-β · C₂(λ) / 2) · χ_λ(U)

where C₂ is the framework-retained quadratic Casimir (SU3_CASIMIR_FUNDAMENTAL
gives C₂(1,0) = 4/3 exact from Cl(3) trace form).

This script computes the heat-kernel single-plaquette expectation
⟨(1/3) Re Tr U⟩ at β=6 by summing over SU(3) irreps λ=(p,q) with truncation
NMAX, comparing to:
  - Wilson single-plaquette ⟨P⟩_W(6) = 0.4225317396 (V=1 PF ODE certified)
  - Lattice MC thermodynamic ⟨P⟩(6) ≈ 0.5934 (canonical comparator)

This is a probe, not a derivation. The framework's actually-derived action
remains an open question; this only shows what heat-kernel would give IF
it's the right Cl(3)-native action.
"""
from fractions import Fraction
import math


def dim_su3(p: int, q: int) -> int:
    """Dimension of SU(3) irrep (p,q)."""
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def casimir_su3(p: int, q: int) -> Fraction:
    """Quadratic Casimir of SU(3) irrep (p,q): exact rational.

    C_2(p,q) = (1/3)(p² + pq + q² + 3p + 3q)
    """
    return Fraction(p * p + p * q + q * q + 3 * p + 3 * q, 3)


def heat_kernel_partition_su3(beta: float, NMAX: int) -> float:
    """Heat-kernel single-plaquette partition function via character sum.

    Z_HK(β) = Σ_λ d_λ² · exp(-β · C_2(λ) / 2)

    The sum-over-(p,q) gives the partition function of a single SU(3) link
    under heat-kernel measure (no source). Truncation at NMAX (p+q ≤ NMAX).
    """
    Z = 0.0
    for p in range(NMAX + 1):
        for q in range(NMAX + 1 - p):
            d = dim_su3(p, q)
            C2 = float(casimir_su3(p, q))
            Z += d * d * math.exp(-beta * C2 / 2.0)
    return Z


def heat_kernel_avg_plaquette_su3(beta: float, NMAX: int) -> float:
    """Heat-kernel single-plaquette ⟨(1/3) Re Tr U⟩.

    Re Tr(U) = (1/2)(Tr U + Tr U†) = (1/2)(χ_{(1,0)} + χ_{(0,1)}).

    Using Schur orthogonality: ∫ χ_λ(U) χ_{(1,0)}(U) dU = δ_{λ, (0,1)}
    (conjugate-rep delta, since χ_{(0,1)} = conjugate of χ_{(1,0)}).

    The single-plaquette expectation under heat-kernel measure
    P_β(U) = Σ_λ d_λ exp(-β C_2/2) χ_λ(U) gives:

        ⟨(1/3) Re Tr U⟩ = (1/6) · 2 · d_{(1,0)} · exp(-β C_2(1,0) / 2) / Z_HK
                        =      d_{(1,0)} · exp(-β · 2/3)              / Z_HK
                        =      3 · exp(-2β/3)                          / Z_HK

    where C_2(1,0) = 4/3 from the framework retained theorem.
    """
    Z = heat_kernel_partition_su3(beta, NMAX)
    # The (1,0) and (0,1) reps are non-self-conjugate; their character sum
    # gives 2 · d · exp(-β · C_2/2) for the symmetric Re Tr observable.
    # After (1/3) normalization: contribution is (2 · d / 6) = d/3 = 1.
    # Wait — let me re-derive carefully:
    # Re Tr U = (1/2)(Tr U + Tr U†) = (1/2)(χ_{(1,0)}(U) + χ_{(0,1)}(U))
    # ⟨χ_{(1,0)}⟩ = (1/Z) Σ_λ d_λ exp(-β C_2/2) ∫ dU χ_{(1,0)}(U) χ_λ(U)
    #              = (1/Z) Σ_λ d_λ exp(-β C_2/2) δ_{λ, conjugate of (1,0)}
    #              = (1/Z) Σ_λ d_λ exp(-β C_2/2) δ_{λ, (0,1)}
    #              = (1/Z) · d_{(0,1)} · exp(-β C_2(0,1) / 2)
    #              = (1/Z) · 3 · exp(-β · (4/3) / 2)
    #              = (1/Z) · 3 · exp(-2β/3)
    # Similarly ⟨χ_{(0,1)}⟩ = (1/Z) · 3 · exp(-2β/3) (same value by symmetry)
    # ⟨Re Tr U⟩ = (1/2)(3 + 3) exp(-2β/3) / Z = 3 exp(-2β/3) / Z
    # ⟨(1/3) Re Tr U⟩ = exp(-2β/3) / Z
    numerator = math.exp(-2.0 * beta / 3.0)
    return numerator / Z


def hk_avg_at_time(t: float, NMAX: int = 15) -> float:
    """⟨(1/3) Re Tr U⟩ under heat-kernel measure at Brownian time t.

    For SU(3) Brownian motion starting at identity:
        ⟨χ_λ⟩_t = d_λ · exp(-t · C_2(λ) / 2)
    Trivial rep gives Z_HK = 1 (probability measure).
    Re Tr observable: ⟨(1/3) Re Tr U⟩ = exp(-2t/3) for SU(3) (since
    C_2(1,0) = 4/3 and d_{(1,0)} = 3).

    More precisely, summing the full character expansion (which is exact):
    """
    Z = heat_kernel_partition_su3(1.0 / max(t, 1e-300), 0)  # not used
    # Direct closed form for single-plaquette HK:
    # ⟨P⟩_HK(t) = exp(-2t/3) (from leading (1,0)+(0,1) characters; higher
    # reps contribute zero for 1-plaquette × Re Tr observable due to Schur).
    return math.exp(-2.0 * t / 3.0)


def main() -> None:
    print("=" * 70)
    print("Heat-Kernel SU(3) Single-Plaquette Probe — Multiple Conventions")
    print("=" * 70)
    print()
    print("Framework retained Casimir: C_2(1,0) = 4/3 (exact)")
    print("Framework β=6 evaluation point (g_bare = 1)")
    print()

    print("CONVENTION I: t_HK = β (literal Casimir-suppression weight)")
    print(f"{'NMAX':>6} {'Z_HK(6)':>20} {'⟨P⟩_HK(6)':>20}")
    for NMAX in [1, 2, 3, 4, 5, 6, 8, 10, 12, 15]:
        Z = heat_kernel_partition_su3(6.0, NMAX)
        avg = heat_kernel_avg_plaquette_su3(6.0, NMAX)
        print(f"{NMAX:>6} {Z:>20.15f} {avg:>20.15f}")
    print(f"  ⟨P⟩_HK(t=β=6)   = {math.exp(-4.0):.10f} (closed form: exp(-2β/3))")
    print()

    print("CONVENTION II: t_HK = 1/β (continuum-limit-natural matching)")
    print(f"  ⟨P⟩_HK(t=1/6)   = {math.exp(-2.0/(3.0*6.0)):.10f} = exp(-1/9)")
    print()

    print("CONVENTION III: t_HK = N_c/β = 3/6 = 1/2 (Menotti-Onofri matching)")
    print(f"  ⟨P⟩_HK(t=1/2)   = {math.exp(-2.0*0.5/3.0):.10f} = exp(-1/3)")
    print()

    print("CONVENTION IV: t_HK = 1 (canonical normalization a²·g²/V = 1)")
    print(f"  ⟨P⟩_HK(t=1)     = {math.exp(-2.0/3.0):.10f} = exp(-2/3)")
    print()

    print("CONVENTION V: t_HK = 2N_c²/β = 18/6 = 3 (Drouffe-Zuber)")
    print(f"  ⟨P⟩_HK(t=3)     = {math.exp(-2.0):.10f} = exp(-2)")
    print()

    print("=" * 70)
    print("Convention-dependent values for ⟨P⟩_HK at framework's β=6:")
    print()
    conventions = [
        ("I:   t = β = 6                    ", 6.0),
        ("II:  t = 1/β = 1/6                ", 1.0 / 6.0),
        ("III: t = N_c/β = 1/2 (M-O)         ", 0.5),
        ("IV:  t = 1 (canonical)            ", 1.0),
        ("V:   t = 2N_c²/β = 3 (D-Z)        ", 3.0),
    ]
    for name, t in conventions:
        print(f"  {name} ⟨P⟩_HK = {math.exp(-2.0*t/3.0):.6f}")
    print()
    print("Comparators:")
    print(f"  Wilson ⟨P⟩_W,1plaq(6)    = 0.4225317396     [V=1 PF ODE certified]")
    print(f"  Lattice MC ⟨P⟩(6)        ≈ 0.5934           [canonical comparator]")
    print(f"  4D MC FSS ⟨P⟩(6)         = 0.59400 ± 0.00037 [PR-grade comparator]")
    print()
    print("=" * 70)
    print("KEY OBSERVATION:")
    print("  The HK time convention t_HK is NOT yet derived from Cl(3) axioms.")
    print("  Different conventions give wildly different numerical answers.")
    print("  Under convention III (Menotti-Onofri), ⟨P⟩_HK(6) ≈ 0.7165 — closer")
    print("  to MC 0.5934 than Wilson's 0.4225 is.")
    print("  Under convention I (literal Casimir-suppression), ⟨P⟩_HK(6) ≈ 0.018.")
    print()
    print("  The framework's load-bearing question becomes:")
    print("  'What HK time t is forced by canonical Cl(3) connection")
    print("   normalization + Z³ substrate emergence + g_bare = 1?'")
    print()
    print("  This is a derivation problem with finite-dim algebraic content,")
    print("  NOT the famous open lattice problem. The answer is a specific")
    print("  rational number determined by the framework's axiom chain.")


if __name__ == "__main__":
    main()
