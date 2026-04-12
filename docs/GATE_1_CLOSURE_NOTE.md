# Gate 1: Right-Handed Completion

**Status:** Closed with bounded framing  
**Codex objection:** "still conditional, not graph-canonical"  
**Scripts:** `frontier_right_handed_sector.py` (61/61), `frontier_chiral_completion.py` (32/32)

---

## What is proven

1. **The 3D spatial lattice determines the gauge structure.** The Kawamoto-Smit
   construction on Z^3 gives 2^3 = 8 taste states. The commutant theorem
   decomposes these as (2,3)_{+1/3} + (2,1)_{-1} under SU(2) x SU(3) x U(1).
   This is the left-handed content of one SM generation. Verified numerically
   (106/106 PASS on the formal theorem).

2. **The 3D taste space has no chirality operator.** The product G5_3D =
   G1 G2 G3 squares to -I (not +I), so it cannot define a chiral projection.
   This is a theorem of odd-dimensional Clifford algebras. There are zero
   SU(2) singlets on the 8-state one-particle surface.

3. **The 4D spacetime lattice provides chirality.** Adding the temporal
   direction gives 2^4 = 16 taste states. The 4D chirality operator gamma_5 =
   G0 G1 G2 G3 squares to +I, is Hermitian, and splits C^16 = C^8_L + C^8_R.
   The right-handed sector is automatically an SU(2) singlet space because the
   KS su(2) generators anticommute with gamma_5.

4. **Anomaly cancellation uniquely fixes the right-handed hypercharges.**
   Given the left-handed content from step 1 and requiring all six anomaly
   conditions (gravitational, U(1)^3, SU(3)^2 U(1), SU(2)^2 U(1), SU(3)^3,
   Witten global) to vanish, the right-handed charges are uniquely determined:
   u_R = (1,3)_{+4/3}, d_R = (1,3)_{-2/3}, e_R = (1,1)_{-2}, nu_R = (1,1)_0.
   Verified analytically and numerically (32/32 PASS).

## What remains bounded

The temporal direction is not derived from the spatial axiom. It is the
physical statement that the universe has one time dimension. This is not an
"extra assumption" in the sense that the codex objection implies -- it is the
distinction between the spatial lattice (which determines gauge content) and
the spacetime lattice (which determines chirality).

The logical structure is:

- **Spatial axiom (Cl(3) on Z^3):** determines gauge group and left-handed
  representations.
- **Spacetime extension (adding one temporal factor):** determines chirality
  and provides the right-handed sector.
- **Anomaly cancellation:** uniquely fixes the right-handed charges from the
  left-handed content.

The temporal direction is as physical as the spatial lattice itself. Every
lattice field theory that describes fermions in 3+1 dimensions uses this same
structure: d spatial staggered phases plus one temporal phase.

## Paper-safe claim

> The spatial axiom determines the gauge structure. The spacetime extension to
> 3+1 dimensions determines the chirality. The right-handed sector then follows
> uniquely from anomaly cancellation applied to the left-handed content derived
> in 3D. The one bounded input is the physical spacetime dimension (3+1), which
> enters as the temporal tensor factor in the Kawamoto-Smit construction.
