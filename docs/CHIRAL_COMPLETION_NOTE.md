# Chiral Completion: Conditional Right-Handed Singlet Completion and Anomaly Cancellation

**Script:** `scripts/frontier_chiral_completion.py`
**Depends on:** `frontier_su3_formal_theorem.py`, `frontier_hypercharge_identification.py`
**Status:** 32/32 checks pass

## Problem Statement

The SU(3) commutant theorem derives one generation of **left-handed** SM fermions
from the 8-dim taste space of staggered fermions in d=3:

    C^8 = (2, 3)_{+1/3} + (2, 1)_{-1} = Q_L + L_L

The Standard Model also requires **right-handed** fermions:
u_R, d_R, e_R (and possibly nu_R), which are SU(2)_weak singlets.
This note proves the anomaly-completion theorem **conditional on** the
singlet template and `y4 = 0`. The stronger graph-canonical template theorem
remains open, and the 3D one-particle surface does not generate the right-
handed template by itself.

## Lattice Origin

In d=3 spatial dimensions, the staggered lattice has 2^3 = 8 taste degrees of
freedom, giving the left-handed content.  Including the temporal direction
(d = 3+1) doubles the taste space to 2^4 = 16 = C^2 x C^2 x C^2 x C^2.
The 4D chirality operator gamma_5 splits C^16 = C^8_L + C^8_R.

This doubling is the correct counting surface for one SM generation and is
consistent with prior repo work noting `8 Dirac = 16 Weyl = 1 SO(10)
generation`, but the existence of a 16-state count does **not** by itself
derive the right-handed representation template.

The right-handed fermions are SU(2)_weak **singlets** because SU(2) is a
chiral gauge symmetry coupling only to left-handed fermions.  In this note the
right-handed sector is treated as a completion ansatz:

    u_R = (1, 3)_{y1}, d_R = (1, 3)_{y2}, e_R = (1, 1)_{y3}, nu_R = (1, 1)_{y4}

The hypercharges are then fixed by anomaly cancellation once the singlet
template and the neutral-neutrino condition `y4 = 0` are imposed.

What is still missing is the graph-canonical theorem that produces this
right-handed singlet template from the retained graph/taste surface itself.

## Conditional Derivation of Right-Handed Hypercharges

Parametrise the right-handed sector as:

| Field | Representation | Count |
|-------|---------------|-------|
| u_R   | (1, 3)_{y1}   | 3     |
| d_R   | (1, 3)_{y2}   | 3     |
| e_R   | (1, 1)_{y3}   | 1     |
| nu_R  | (1, 1)_{y4}   | 1     |

The anomaly conditions are:

1. **Tr[Y] = 0** (gravitational): 3y1 + 3y2 + y3 + y4 = 0
2. **Tr[Y^3] = 0** (U(1)^3 cubic): nonlinear constraint
3. **Tr[SU(3)^2 Y] = 0** (mixed colour-hypercharge): y1 + y2 = 2/3
4. **Tr[SU(2)^2 Y] = 0** (mixed weak-hypercharge): automatically satisfied
5. **Witten SU(2)** (global anomaly): 4 doublets (even) -- satisfied

### Solution

From (3): y2 = 2/3 - y1.
From (1): y3 + y4 = -2.
Setting y4 = 0 (sterile neutrino) gives y3 = -2.
Substituting into (2) yields the quadratic:

    18 y1^2 - 12 y1 - 16 = 0

with discriminant 1296 = 36^2.  Solutions: y1 = 4/3 or y1 = -2/3.
These give the same set {y1, y2} = {4/3, -2/3}.

**Result:**

| Field | Y     | Q = Y/2 |
|-------|-------|---------|
| u_R   | +4/3  | +2/3    |
| d_R   | -2/3  | -1/3    |
| e_R   | -2    | -1      |
| nu_R  | 0     | 0       |

These are the Standard Model hypercharge assignments.

## Full Anomaly Cancellation (16-state generation)

All anomaly coefficients are verified both analytically (exact fractions)
and numerically (8x8 matrix traces):

| Anomaly                 | Value | Status |
|-------------------------|-------|--------|
| Tr[Y]                   | 0     | PASS   |
| Tr[Y^3]                 | 0     | PASS   |
| Tr[SU(3)^2 Y]           | 0     | PASS   |
| Tr[SU(2)^2 Y]           | 0     | PASS   |
| Tr[SU(3)^3] (d-symbol)  | 0     | PASS   |
| Witten SU(2) (mod 2)    | even  | PASS   |

Additional: Tr[Y^2] = 40/3, matching the SU(5) GUT normalisation.

## SU(5) GUT Embedding

The full 16-state generation decomposes into SU(5) representations:

    5-bar = (3*, 1)_{+2/3} + (1, 2)_{-1}     = d_R^c + L_L
    10    = (3*, 1)_{-4/3} + (3, 2)_{+1/3} + (1, 1)_{+2} = u_R^c + Q_L + e_R^c
    1     = (1, 1)_{0}                         = nu_R^c

Tr[Y] vanishes within each SU(5) multiplet independently.

## Uniqueness

With the constraint y4 = 0 (neutrino is electrically neutral),
the anomaly system has a **unique** rational solution.  This is verified
by exhaustive scan over rational y4 values: for each y4, a one-parameter
family of solutions exists, but y4 = 0 is the unique choice consistent
with a right-handed neutrino carrying no gauge charges.

Without the `y4 = 0` input, the anomaly equations leave a one-parameter family
of completions. So the theorem is sharp but conditional:

- theorem proved: anomaly cancellation uniquely fixes the SM right-handed
  hypercharges **given** the singlet template and neutral neutrino condition
- theorem still missing: a graph-canonical derivation of the singlet template
  itself

## Significance

The left-handed sector (2,3)_{+1/3} + (2,1)_{-1} derived from the 8-dim
taste space of the 3D staggered lattice, together with anomaly cancellation,
**uniquely determines** the right-handed hypercharges of one generation
once the right-handed singlet template is supplied.

That is the exact result this note proves. It is not yet a graph-canonical
derivation of the right-handed template from the retained surface.
