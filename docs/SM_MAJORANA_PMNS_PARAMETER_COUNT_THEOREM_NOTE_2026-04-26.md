# Standard Model Majorana PMNS Parameter-Count Theorem

**Date:** 2026-04-26

**Status:** standalone positive Standard Model lepton-flavor theorem. This
note proves that the generic active one-Higgs Standard Model lepton sector
augmented by the active Majorana Weinberg operator contains exactly twelve
physical real parameters: three charged-lepton masses, three Majorana
neutrino masses, three PMNS mixing angles, one Dirac CP phase, and two
Majorana phases. It is a structural guardrail for the retained neutrino and
PMNS boundary notes. It does not derive any charged-lepton mass, neutrino
mass, PMNS angle, Dirac phase, Majorana phase, neutrinoless-double-beta
rate, baryogenesis asymmetry, time-travel, teleportation, or antigravity
claim.

**Primary runner:** `scripts/frontier_sm_majorana_pmns_parameter_count.py`

## 1. Claim

Work on the active one-Higgs Standard Model lepton sector with three
generations and canonical kinetic terms. The renormalizable charged-lepton
Yukawa matrix is an arbitrary complex `3 x 3` matrix,

```text
Y_e.
```

Add the active dimension-five Majorana Weinberg operator

```text
(L H) kappa (L H) / Lambda + h.c.,
```

where the generation matrix `kappa` is complex symmetric. After electroweak
symmetry breaking, `Y_e` gives the charged-lepton Dirac mass matrix and
`kappa` gives the active Majorana neutrino mass matrix.

At a generic full-rank point with nondegenerate charged-lepton and neutrino
singular values/eigenvalues, and with no accidental flavor stabilizer, the
physical lepton-flavor parameter space has real dimension

```text
12.
```

Equivalently, the generic active Majorana lepton sector is coordinatized by

```text
3 charged-lepton masses
+ 3 Majorana neutrino masses
+ 3 PMNS mixing angles
+ 1 Dirac CP phase
+ 2 Majorana phases.
```

The theorem is a parameter-count theorem, not a numerical prediction theorem.

## 2. Scope and Guardrails

The word "generic" is load-bearing. If charged-lepton masses or neutrino
masses are exactly degenerate, if either mass matrix loses rank, if the PMNS
matrix has texture zeros, or if extra flavor symmetries are imposed, the
quotient develops special lower-dimensional strata. Those boundaries are not
the generic active Majorana lepton surface.

This theorem also does not claim that the Weinberg operator coefficient is
derived by the retained framework. It answers a different question: once an
active Majorana mass matrix is admitted, how many independent physical
parameters must any claimed PMNS or Majorana-phase closure account for?

## 3. Input Surface

Before `Y_e` and `kappa` are specified, the active lepton kinetic terms have
generation flavor symmetry

```text
G_flavor = U(3)_L x U(3)_e.
```

The transformations act as

```text
L   -> U_L L,
e_R -> U_e e_R.
```

The flavor tensors transform as

```text
Y_e   -> U_L^dagger Y_e U_e,
kappa -> U_L^T kappa U_L.
```

The symmetry action preserves canonical kinetic terms. It is therefore a
basis redundancy, not a physical operation.

## 4. Raw Parameter Count

The charged-lepton Yukawa matrix has

```text
2 * 3^2 = 18
```

real parameters. The Majorana Weinberg coefficient is complex symmetric, so
it has `3(3+1)/2 = 6` complex entries, or

```text
12
```

real parameters. The raw lepton-flavor data therefore carry

```text
18 + 12 = 30
```

real parameters.

The flavor group has dimension

```text
dim U(3)_L + dim U(3)_e = 3^2 + 3^2 = 18.
```

At a generic Majorana point, the continuous stabilizer is trivial. The reason
is simple in a charged-lepton mass basis. Nondegenerate charged-lepton masses
leave only equal left/right diagonal charged-lepton rephasings. The Majorana
matrix then transforms by

```text
kappa_ab -> e^(i alpha_a) kappa_ab e^(i alpha_b).
```

For a generic symmetric `kappa` with all entries nonzero, invariance of the
diagonal entries already gives `2 alpha_a = 0` infinitesimally for each
`a`. Thus all `alpha_a` vanish as continuous directions. Only discrete sign
choices can remain after the Majorana masses are made positive.

Therefore the generic orbit dimension is `18`, and the physical quotient
dimension is

```text
30 - 18 = 12.
```

This proves the raw twelve-parameter quotient count.

## 5. Mass-Basis Identification

The charged-lepton mass matrix is diagonalized by a singular-value
decomposition:

```text
U_eL^dagger Y_e U_eR = D_e,
```

where `D_e` has three positive entries at a generic full-rank point:

```text
m_e, m_mu, m_tau.
```

The complex symmetric Majorana matrix is diagonalized by a Takagi
factorization:

```text
U_nu^T kappa U_nu = D_nu,
```

where `D_nu` has three nonnegative entries, positive and nondegenerate at a
generic point:

```text
m_1, m_2, m_3.
```

The charged-current mismatch is the PMNS matrix

```text
U_PMNS = U_eL^dagger U_nu.
```

Thus six of the twelve parameters are masses, and the rest live in the
physical PMNS matrix.

## 6. Majorana PMNS Rephasing Count

A unitary `3 x 3` matrix has real dimension

```text
dim U(3) = 9.
```

After charged-lepton masses are diagonal and positive, the charged-lepton
mass eigenfields may still be rephased:

```text
e_a -> e^(i alpha_a) e_a.
```

This rephases the rows of `U_PMNS` and removes three continuous phases.

Majorana neutrino mass eigenfields cannot be continuously rephased while
keeping positive Majorana masses. A rephasing

```text
nu_i -> e^(i beta_i) nu_i
```

changes the Majorana mass term by `e^(2 i beta_i)`. It preserves a positive
mass only for discrete signs, not for a continuous `U(1)` phase. Discrete
signs do not reduce the real dimension.

Therefore the physical PMNS space has dimension

```text
9 - 3 = 6.
```

The real orthogonal submanifold `SO(3)` supplies

```text
3
```

mixing angles. The remaining

```text
6 - 3 = 3
```

dimensions are CP-odd phases. Conventionally they split into

```text
1 Dirac phase + 2 Majorana phases.
```

Combining with the six masses gives

```text
3 charged-lepton masses
+ 3 neutrino masses
+ 3 PMNS angles
+ 3 PMNS phases
= 12.
```

## 7. General-N Cross-Check

For `N` generations:

```text
Y_e raw parameters:          2 N^2,
kappa raw parameters:        N(N+1),
flavor group dimension:      2 N^2,
generic stabilizer:          0,
physical count:              N^2 + N.
```

The physical coordinates split as

```text
N charged-lepton masses,
N Majorana neutrino masses,
N(N-1)/2 mixing angles,
N(N-1)/2 CP-odd PMNS phases.
```

The CP-odd phases further decompose as

```text
(N-1)(N-2)/2 Dirac-type phases,
N-1 Majorana phases.
```

For `N=1`, there are two masses and no mixing or CP phase. For `N=2`, there
are four masses, one mixing angle, and one Majorana phase. For `N=3`, there
are six masses, three mixing angles, one Dirac phase, and two Majorana
phases.

This contrasts with a purely Dirac neutrino sector, where continuous
neutrino mass-eigenstate rephasings remove `N-1` additional phases and the
CKM-like mixing matrix has only `(N-1)(N-2)/2` CP phases.

## 8. Theorem Proof

The raw active Majorana lepton data are `(Y_e,kappa)`. Their real dimension
is `18 + 12 = 30`. The canonical lepton kinetic terms permit the basis group
`U(3)_L x U(3)_e`, dimension `18`, to act on these tensors. At a generic
full-rank nondegenerate Majorana point, the continuous stabilizer is
trivial, because the Majorana term breaks the otherwise available continuous
lepton-number rephasings down to discrete signs. The physical quotient
therefore has dimension `30 - 18 = 12`.

Singular-value decomposition of `Y_e` gives three charged-lepton masses.
Takagi factorization of `kappa` gives three Majorana neutrino masses. The
remaining mismatch is a unitary `3 x 3` PMNS matrix. Three charged-lepton
row rephasings remove three phases from this unitary matrix, while Majorana
neutrino columns cannot be continuously rephased. The PMNS space therefore
has six dimensions, split as three real mixing angles and three CP-odd
phases. The three CP-odd phases are conventionally one Dirac phase and two
Majorana phases.

Thus the generic active Majorana lepton sector has exactly twelve physical
real parameters. This proves the theorem.

## 9. Program Consequences

This theorem gives a sharp review-facing boundary:

- any claimed PMNS closure on an active Majorana surface must account for a
  six-dimensional PMNS space, not a four-dimensional CKM-like space;
- two Majorana phases are physical in the generic three-generation Majorana
  problem and cannot be removed by the one-generation Majorana rephasing
  used in narrower local notes;
- retained neutrino observable bounds that are uniform in Majorana phases
  are correctly phase-agnostic, not phase-selecting;
- no PMNS angle, Dirac phase, Majorana phase, neutrino mass value,
  baryogenesis result, time-travel, teleportation, or antigravity claim is
  promoted by this count.
