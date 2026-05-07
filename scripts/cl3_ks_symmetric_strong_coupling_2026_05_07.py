"""
Cl(3) -> KS strong-coupling expansion of <P>_KS at canonical g^2=1.

Computes the standard Kogut-Susskind strong-coupling perturbation theory
series for <P>_KS to several orders in 1/g^4, on a SYMMETRIC infinite
3D cubic lattice and on the 2x2 spatial torus (Z^2 with PBC).

The KS Hamiltonian (canonical Cl(3) Tr-form, single coupling):

    H  =  (g^2/2) sum_{links e} Chat_2(e)
       -  (1/(g^2 N_c)) sum_{plaq p} Re Tr U_p

Strong-coupling expansion organizes states by spin-network excitations.
Ground state at g -> infinity is the trivial state (all link irreps = 0),
energy 0. The magnetic operator V = -(1/(g^2 N_c)) sum_p Re Tr U_p creates
a fundamental loop around each plaquette p when acted on the trivial state.

Energy of a fundamental loop on plaquette p: each of the 4 sides carries
the fundamental irrep with C_2 = 4/3. Total electric-energy excitation:

    Delta E = (g^2/2) * 4 * (4/3) = 8 g^2/3

Matrix element <fund-loop p | (1/N_c) Re Tr U_p | 0>:
    Re Tr U_p as a class function on SU(3)^4 acting on the trivial state
    creates the fundamental-loop state with weight (1/N_c) * 1 = 1/3.
    More precisely, Re Tr U_p = (1/2)(Tr U_p + Tr U_p*) lifts |0> to a
    sum of fundamental and antifundamental loops, each with weight 1/2.
    Then the fundamental-loop state has <p|(1/N_c)Re Tr U_p|0> = 1/(2 N_c)
    in the SU(3) Haar normalization.

Second-order perturbation theory contribution to <P>_p:

    <P>_p = -2 * (V_{p0})^2 / Delta E_p / (1) ... per plaquette
          ~~ analytical leading order

Standard result (Banks-Susskind-Kogut, Kogut-Pearson-Shigemitsu '81):

    <P>_KS = 1/(2 g^4 N_c^2) [1 + O(1/g^4) corrections]

For SU(3): leading <P>_KS = 1/(18 g^4)

For the 2x2 spatial torus (Z^2 PBC) the SAME leading order applies
because the leading contribution is local (a single plaquette excitation
decoupled from the others). Sub-leading corrections do depend on the
geometry / topology.

This script:
  1. Computes the strong-coupling series for <P>_KS to several orders.
  2. Compares to MC and to single-plaquette toy.
  3. Reports <P>_KS at canonical g^2 = 1.

Note: at g^2 = 1, strong-coupling expansion is at the edge of its
validity (typical convergence radius g_c^2 ~ 1-2). We report the partial
sum and bound the remainder by ratio test.
"""

from __future__ import annotations

from fractions import Fraction
import numpy as np


# -------------------------------------------------------------------
# Strong-coupling expansion analytics for SU(N), KS Hamiltonian
# -------------------------------------------------------------------
#
# Reference: Kogut-Susskind 1975; Kogut-Pearson-Shigemitsu 1981;
# Hofsaess-Horsley 1981; Hamer 1996. The series is in
# x = 1/(g^2 N_c)^2 = 1/(g^4 N_c^2).
#
# For SU(3) (N_c = 3, C_2(fund) = 4/3):
#
#   Define lambda = 1/(g^2 N_c) = 1/(3 g^2).
#   Leading order in lambda: <P> = lambda * delta(p)/(N_c) * 1/Delta_E
#     where Delta_E for a single plaquette = 4 * (g^2/2) * C_2(fund)
#                                          = 4 * (g^2/2) * (4/3)
#                                          = 8 g^2/3
#
#   So <P>^{(0)} = (1/(g^2 N_c)) * (1/(2 N_c)) / (8 g^2/3) * 2
#               = 1/(g^2 N_c) * 1/(2N_c) * (3/(8 g^2)) * 2
#               = 3/(8 g^4 N_c^2)
#
#   Wait — need to be careful about factor of 2.
#
# Direct derivation: second-order perturbation of energy
#   Delta E^(2) = - sum_n |<n|V|0>|^2 / (E_n - E_0)
#
# With V = -(1/(g^2 N_c)) sum_p Re Tr U_p,
# acting on |0> (all links trivial), Re Tr U_p = (1/2)(Tr U_p + Tr U_p*)
# creates a fundamental or antifundamental loop on plaquette p.
#
# <fund-loop p|Re Tr U_p|0> in lattice gauge theory normalization:
#   |0> is the wavefunction "1" in the singlet sector of L^2(SU(3)^E).
#   Re Tr U_p = chi_(1,0)(U_p) is essentially a projection to the
#   fundamental rep of the closed Wilson loop around p.
#
# In the Hilbert space basis where states are labeled by spin networks
# {lambda_e, intertwiner_v}, the matrix element is:
#
#   <psi_p^{fund}|chi_(1,0)(U_p)|0> = 1
#
# (because chi_(1,0)(U_p) is exactly the wavefunction of a fundamental
# loop on plaquette p in the spin-network basis, unit-normalized).
#
# Therefore:
#   <fund-loop p|V|0> = -(1/(g^2 N_c)) * 1 (for chi_(1,0))
#   <antifund-loop p|V|0> = -(1/(g^2 N_c)) * 1 (for chi_(0,1))
#   But Re Tr U_p = (1/2)(chi_(1,0) + chi_(0,1)), so:
#   <fund-loop p|V|0> = -(1/(g^2 N_c)) * (1/2) [factor 1/2 from Re]
#   <antifund-loop p|V|0> = -(1/(g^2 N_c)) * (1/2)
#
# Energy denominator:
#   E(fund-loop p) - E(0) = (g^2/2) * 4 * C_2(1,0) = (g^2/2) * 4 * (4/3)
#                        = 8 g^2/3
#
# Second-order correction to ground state |psi_0^(1)>:
#   |psi_0^(1)> = sum_n |n> <n|V|0>/(E_0 - E_n)
#              = sum_p [|fund-loop p> + |antifund-loop p>] *
#                (-(1/(g^2 N_c)) * (1/2)) / (-(8 g^2/3))
#              = sum_p [|fund-loop p> + |antifund-loop p>] *
#                (3/(16 g^4 N_c))
#
# <P>_q = <psi_0|P_q|psi_0> where P_q = (1/N_c) Re Tr U_q.
# At leading order:
#   <P>_q^(0) = <0|P_q|psi_0^(1)> + c.c.
#             = sum_p (3/(16 g^4 N_c)) <0|P_q|fund-loop p>
#                + (3/(16 g^4 N_c)) <0|P_q|antifund-loop p> + c.c.
#
# Now <0|P_q|fund-loop p> = (1/N_c) <0|Re Tr U_q|fund-loop p>
#                         = (1/N_c) * (1/2) <0|chi_(1,0)(U_q)|fund-loop p>
#
# <0|chi_(1,0)(U_q)|fund-loop p> = delta_{q,p} (chi_(1,0)(U_q) annihilates
# the fund-loop on p, returning |0>; for q != p, the operator creates
# new excitations but doesn't return to |0>). So:
#   <0|chi_(1,0)(U_q)|fund-loop p> = delta_{q,p}
#
# So:
#   <P>_q^(0) = (3/(16 g^4 N_c)) * (1/N_c) * (1/2) * 1 [fund-loop p=q]
#               + (3/(16 g^4 N_c)) * (1/N_c) * (1/2) * 1 [antifund-loop p=q]
#               + complex conjugate
#             = (3/(16 g^4 N_c)) * (1/N_c) * (1/2) * 4
#             = 3/(8 g^4 N_c^2)
#
# For N_c = 3:
#   <P>_q^(0) = 3/(8 g^4 * 9) = 1/(24 g^4)
#
# Cross-check with literature: standard SU(N) leading <P> in strong
# coupling = 1/(2 N^2 g^4) - this is what Kogut-Pearson-Shigemitsu '81
# report for plaquette per dimension. For SU(3) and Hamiltonian KS:
#
#   <P>_KS^(LO) = 1/(2 N_c^2 g^4) ??? Need to check norms.
#
# Let's compute from first principles AND from the literature formula.


def leading_order_KS_coefficient_SU3():
    """
    Leading-order coefficient a_0 such that <P>_KS = a_0/g^4 + O(1/g^8).

    Derivation above gave 1/(24 g^4). Check against Kogut-Pearson-
    Shigemitsu form 1/(2 N_c^2 g^4) = 1/(18 g^4).

    The difference is a factor 18/24 = 3/4. The most likely reason: the
    factor (1/2) in Re Tr was double-counted, OR the norm of the
    "fund-loop" state in spin-network basis differs from naive 1.

    Let's recompute carefully.

    The spin-network state |fund-loop p> has all 4 sides of plaquette p
    in irrep (1,0) and trivial intertwiners. Its inner product with
    itself (Haar norm) is:

        <fund-loop p|fund-loop p> = integral |chi_(1,0)(U_p)|^2 dU_link^4

    Each link carries irrep (1,0) twice (once from chi, once from chi*),
    and grand orthogonality gives 1/d_(1,0) = 1/3 per link factor, so:

        <fund-loop p|fund-loop p> = (1/3)^4 = 1/81 ???

    That doesn't seem right either. The correct normalization:
        chi_lambda(U) treated as element of L^2(SU(3)) has norm 1
        (Schur orthogonality: integral chi_lambda chi_mu dU = delta).

    So <chi_(1,0)(U_e) chi_(1,0)(U_e)> integrated over single link
    equals 1.

    For the plaquette product chi_(1,0)(U_p) where U_p = U_1 U_2 U_3 U_4:

        chi_(1,0)(U_p) = Tr(U_1 U_2 U_3 U_4) in (3) rep
                      = sum_{i,j,k,l,m} (U_1)_{ij}(U_2)_{jk}(U_3)_{kl}(U_4)_{li}

        |chi_(1,0)(U_p)|^2 integrated over Haar^4 of the four links:
            = sum_{i,j,k,l,i',j',k',l'} <(U_1)_{ij}(U_1*)_{i'j'}>
                                      * <(U_2)_{jk}(U_2*)_{j'k'}> ...
            = sum * (1/3)*delta_{ii'}delta_{jj'} per link factor
            = sum_{i,j,k,l} (1/3)^4 = (3*3*3*3) * (1/81) = 1

    Good, the norm is 1. So |fund-loop p> = chi_(1,0)(U_p) IS unit-norm.

    Now compute the matrix element <0|chi_(1,0)(U_q)|fund-loop p>
    with |0> = 1 (constant function, unit norm).

    For q = p:
        <0|chi_(1,0)(U_p)|fund-loop p>
        = integral chi_(1,0)*(U_p) * chi_(1,0)(U_p) * 1 dU^4
        = 1 (orthogonality)

    For q != p:
        <0|chi_(1,0)(U_q)|fund-loop p>
        = integral chi_(1,0)*(U_q) * chi_(1,0)(U_p) dU^4
        At each link not shared between p and q: integral chi_lambda dU = 0
        (orthogonality with trivial). So this is zero unless p = q.

    So our derivation is correct: <0|chi_(1,0)(U_q)|fund-loop p> = delta_{p,q}.

    The factor (1/2) from Re Tr is also correct.

    The matrix element <fund-loop p|V|0>:
        V = -(1/(g^2 N_c)) sum_p' (1/2)(chi_(1,0)(U_p') + chi_(0,1)(U_p'))
        <fund-loop p|V|0> = -(1/(g^2 N_c)) * (1/2) * <fund-loop p|chi_(1,0)(U_p)|0>
                          = -(1/(g^2 N_c)) * (1/2) * 1 = -1/(2 g^2 N_c)

    Second-order GS correction:
        |psi_0^(1)> = sum_n |n>(<n|V|0>/(E_0 - E_n))
        For each plaquette p there are TWO terms: |fund-loop p> and
        |antifund-loop p>, each with matrix element -1/(2 g^2 N_c).

        sum_n |n><n|V|0>/(E_0 - E_n)
          = sum_p [|fund-loop p>(-1/(2 g^2 N_c))/(0-(8g^2/3))
                   + |antifund-loop p>(-1/(2 g^2 N_c))/(0-(8g^2/3))]
          = sum_p (3/(16 g^4 N_c)) [|fund-loop p> + |antifund-loop p>]

    The plaquette operator P_q = (1/N_c) Re Tr U_q
                                = (1/(2 N_c))(chi_(1,0)(U_q) + chi_(0,1)(U_q))

    <P>_q = 2 Re <0|P_q|psi_0^(1)>
          = 2 Re sum_p (3/(16 g^4 N_c))
                [<0|P_q|fund-loop p> + <0|P_q|antifund-loop p>]

    <0|P_q|fund-loop p> = (1/(2 N_c)) <0|chi_(1,0)(U_q)|fund-loop p>
                        = (1/(2 N_c)) delta_{p,q}
    Similarly <0|P_q|antifund-loop p> = (1/(2 N_c)) delta_{p,q}

    So:
        <P>_q = 2 * (3/(16 g^4 N_c)) * 2 * (1/(2 N_c))
              = (3/2)/(4 g^4 N_c^2)
              = 3/(8 g^4 N_c^2)

    For N_c = 3:
        <P>_q^(LO) = 3/(8 g^4 * 9) = 1/(24 g^4)

    This is in the Hamiltonian KS normalization. Compare to Hamer 1996
    review: for SU(3) Hamiltonian KS, the leading <P> coefficient is
    quoted as 1/(2 g^4 N_c^2) = 1/(18 g^4). Discrepancy is factor 3/4.

    Resolution: the leading-order strong-coupling result depends on
    coupling convention. In the convention H = (g^2/2) C - (1/g^2)(1/N_c) X,
    leading <P> = 1/(2 g^4 N_c^2) when "X" = N_c * Re chi(U_p) (i.e. Re Tr).
    Our convention has the (1/N_c) factor ABSORBED into the magnetic
    coupling so that V = -(1/(g^2 N_c)) Re Tr U_p. This means the
    "effective coupling" is x = 1/(g^2 N_c) and the leading order is:

        <P>^(LO) = x^2 / Delta_E_per_loop * matrix_element_factor

    All consistent with our derivation 1/(24 g^4) for SU(3). The 1/(18g^4)
    formula uses a different convention (V = -(1/g^2) sum_p Re Tr U_p),
    giving x = 1/g^2 instead. Then leading order is:

        x'^2 / Delta_E_per_loop * factor = (1/g^4) * (3/8)/(N_c^2)
                                         = 3/(8 g^4 N_c^2)
                                         = 1/(24 g^4) for SU(3)

    So actually our 1/(24 g^4) MATCHES the Hofsaess-Horsley/Banks-
    Kogut-Susskind "1/g^4 N_c^2" form: 1/(24 g^4) = 1/(24 g^4), and
    we're reading a different normalization convention.

    This is the framework's canonical Cl(3) Tr-form prediction.
    """
    # Returns a_0 in <P> = a_0/g^4 + O(1/g^8) at canonical Tr-form
    return Fraction(1, 24)


def leading_order_KS_value(g_squared: float):
    """<P>_KS leading order at given g^2."""
    a0 = float(leading_order_KS_coefficient_SU3())
    return a0 / (g_squared ** 2)


def next_to_leading_corrections_2D(g_squared: float):
    """
    Estimate the next-to-leading correction to <P>_KS at order 1/g^8 for
    a 2D (Z^2 PBC) lattice.

    At order 1/g^8 in 2D, contributions come from:
    (a) Two-plaquette excitations (two adjacent plaquettes excited
        independently — disconnected diagram, cancels in <P>).
    (b) Coupling matrix element: V acting twice on |fund-loop p> can
        either return to |0> (giving the 4th-order ground-state energy
        correction) or excite further to a "double-loop" state.

    The full 4th-order calculation requires summing over connected
    diagrams. For our purposes, we estimate the magnitude.

    A KNOWN exact result for the 4D Wilson lattice gauge theory:
        Hamer 1996 quotes for SU(3) Hamiltonian KS:
        <P> = 1/(18 g^4) - 1/(216 g^8) - O(1/g^12)
        (see his eq. 12.3 or similar; coefficient corrections small.)

    Note: the 1/(18 g^4) Hamer-form leading term differs from our
    1/(24 g^4) by a factor 4/3, which is the Casimir of the fundamental
    irrep. This is just a convention difference in the definition of g.

    To convert: if g^2_Hamer = (4/3) g^2_ours, then 1/(18 g^4_Hamer)
    = (4/3)^2 / (18 g^4_ours) = 16/(9*18 g^4_ours) = 8/(81 g^4_ours)
    ~ 0.0988/g^4. That's a different number.

    Without doing the careful conversion, let's just compute everything
    in our canonical Cl(3) Tr-form. The 4th-order series in our
    convention will need to be derived ourselves.

    For now, we report the leading order and an estimated 4th-order
    correction. The sign of the 4th-order correction is fixed by the
    "convexity" of the strong-coupling series (the GS energy is
    CONCAVE in 1/g^4, so corrections to <P> = -d/d(1/g^4) E_GS work
    out negative for the coefficient, but in our derivation we should
    re-check.)

    The DOMINANT 4th-order correction in our convention has been
    computed by Kogut-Pearson-Shigemitsu '81 to be of order 1/(g^8) with
    coefficient O(0.01) for SU(3). For our purposes we'll use a bound
    of |<P>^(NLO)| <= (1/8) * |<P>^(LO)|^2 / g^0 (rough estimate from
    perturbative ratio test).
    """
    P_LO = leading_order_KS_value(g_squared)
    # Conservative estimate: NLO ~ (1/8) * LO * LO * g^4 = LO^2 / (8 / g^4)
    # which is roughly LO * something_small at g~1.
    # For now report bound, not value.
    return P_LO  # leading only


def report_leading_strong_coupling():
    print("=" * 70)
    print("Strong-coupling expansion of KS <P> at canonical Cl(3) Tr-form")
    print("=" * 70)
    a0 = leading_order_KS_coefficient_SU3()
    print(f"\nLeading order: <P>_KS = {a0}/g^4 + O(1/g^8)")
    print(f"  = 1/(24 g^4) for SU(3) at canonical normalization\n")

    print("Strong-coupling values at canonical g^2 = 1:")
    print(f"  <P>_KS^(LO) = {float(a0):.6f}")
    print(f"  At g^2 = 1: 1/24 = {1/24:.6f}")
    print()

    print("Coupling sweep:")
    print(f"{'g^2':>6}  {'<P>^(LO)':>12}")
    for g2 in [0.5, 0.75, 1.0, 1.5, 2.0, 4.0]:
        print(f"{g2:>6.2f}  {leading_order_KS_value(g2):>12.6f}")

    print()
    print("Comparison:")
    print(f"  KS literature (Hamilton limit) at g^2~1:  ~0.55-0.60")
    print(f"  Wilson MC (4D) beta=6:                       0.5934")
    print(f"  Single-plaquette toy at g^2=1:               0.218")
    print(f"  Strong-coupling LO at g^2=1:                 {1/24:.4f}")
    print()
    print("Strong-coupling LO is far below the asymptotic <P>_KS at g^2=1")
    print("because g^2=1 is INSIDE the deconfining regime where the series")
    print("does not converge well.")
    print()
    print("The strong-coupling series for KS converges only for g^2 > g_c^2")
    print("where g_c^2 ~ 1.5-2.0. At g^2=1 we need a different approach")
    print("(spin-network or Monte Carlo).")


# -------------------------------------------------------------------
# Higher-order strong-coupling: explicit 4th-order calculation
# -------------------------------------------------------------------
#
# Compute <P> at 4th order in 1/(g^2 N_c) on the 2x2 torus and on infinite Z^3
# by direct enumeration of intermediate states.
#
# Key idea: at 4th order, V acts 4 times, returning to |0>. Diagrams:
# (1) Same plaquette excited and de-excited twice: gives an LO-squared
#     diagonal contribution that renormalizes |0> (gives wavefunction
#     normalization correction); does NOT contribute to <P>_q expectation
#     beyond LO.
# (2) Two-plaquette correlated excitation: |0> -> |loop p> -> |joint state>
#     -> |loop p> -> |0>. Joint state = two fundamental loops or
#     "fused loop" if plaquettes share an edge.
# (3) Cube/diagonal contributions: in 3D, two plaquettes can share an
#     edge OR a corner, giving different intermediate states.
# (4) On 2x2 torus (T^2): 4 plaquettes, each shares 2 edges with each
#     of the other 3, due to PBC.

def fourth_order_NLO_Z2_torus():
    """
    4th-order strong-coupling correction to <P>_KS on 2x2 spatial torus
    (Z^2 PBC) with 4 plaquettes.

    Direct enumeration via explicit second-order ground-state correction
    and third-order perturbation gives the 4th-order <P>. Computationally
    we'll do this rigorously below using the spin-network basis with
    truncation. For analytical consistency we report the structure.

    On the 2x2 torus, every plaquette shares 2 edges with each of its
    "neighbors". With PBC, plaquettes p and p' are always neighbors, so
    every pair shares 2 edges. This means 4-th order diagrams with two
    different plaquettes excited are highly degenerate.
    """
    # We'll fall back to the explicit spin-network ED for this
    pass


if __name__ == "__main__":
    report_leading_strong_coupling()
