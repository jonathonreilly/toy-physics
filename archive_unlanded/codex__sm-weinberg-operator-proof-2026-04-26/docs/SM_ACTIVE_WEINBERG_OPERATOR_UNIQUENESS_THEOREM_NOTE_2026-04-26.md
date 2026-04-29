# Standard Model Active Weinberg Operator Uniqueness Theorem

**Date:** 2026-04-26

**Status:** standalone positive Standard Model/neutrino operator theorem.
This note proves that, in the one-Higgs-doublet Standard Model active field
content, the Weinberg operator is the unique independent dimension-five
gauge-invariant lepton-number-violating operator, modulo integration by
parts and equations of motion. It gives the exact post-EWSB Majorana mass
readout but does not select the coefficient, scale, rank, PMNS matrix, or
neutrino mass spectrum.

## 1. Claim

Use the doubled-hypercharge convention of the retained anomaly notes:

```text
Q_em = T_3 + Y/2,
Y(L_L) = -1,
Y(H) = +1.
```

In the active Standard Model field content

```text
Q_L, L_L, u_R, d_R, e_R, H,
```

with no neutral-singlet insertion inside the operator, the unique
independent dimension-five operator that is Lorentz invariant, invariant
under

```text
SU(3)_c x SU(2)_L x U(1)_Y,
```

and violates lepton number is

```text
O_5^{ij} = (epsilon_ab L_i^a H^b)^T C (epsilon_cd L_j^c H^d),
```

plus its Hermitian conjugate. Here `a,b,c,d` are `SU(2)` indices, `i,j` are
generation indices, and `C` is the Lorentz charge-conjugation matrix. In
two-component notation the same operator is

```text
O_5^{ij} = epsilon_alpha_beta
           (epsilon_ab L_i^{a alpha} H^b)
           (epsilon_cd L_j^{c beta} H^d).
```

The coefficient matrix is symmetric:

```text
kappa_ij = kappa_ji.
```

After electroweak symmetry breaking,

```text
<H> = (0, v/sqrt(2))^T,
```

the effective Lagrangian term

```text
L_5 = -(1/2) kappa_ij O_5^{ij} + h.c.
```

gives the active Majorana mass matrix

```text
(M_nu)_ij = kappa_ij v^2 / 2
```

up to the sign convention absorbed in `kappa`.

This is an operator-classification theorem only. The matrix `kappa`, its
scale, rank, eigenvalues, and diagonalizing PMNS data remain separate open
physics.

## 2. Why This Adds Value

The retained one-Higgs Yukawa theorem proves the exact renormalizable Dirac
Yukawa skeleton and explicitly parks the Weinberg operator outside that
dimension-four classification. The Majorana operator notes classify bare
right-handed singlet pairings and emphasize that their coefficient and scale
are still not selected.

This note fills the active-sector gap:

- it proves that the first gauge-invariant active-neutrino Majorana mass
  source appears at dimension five;
- it proves that the source is unique in the one-Higgs active SM field
  content;
- it gives the exact `v^2` mass readout without choosing the coefficient;
- it separates active Weinberg physics from the repo's distinct neutral
  singlet Majorana lane.

## 3. Field Dimensions and Conventions

Canonical mass dimensions are

```text
dim(H) = 1,
dim(fermion) = 3/2,
dim(D_mu) = 1,
dim(X_munu) = 2,
```

where `X_munu` is any gauge field strength.

For dimension-five Lorentz scalars, the possible field-count patterns are
severely limited:

```text
5 scalars,
2 fermions + 2 scalars,
2 fermions + 1 derivative + 1 scalar,
2 fermions + 1 field strength,
bosonic terms with field strengths and scalars.
```

Four-fermion operators start at dimension six, so they are not part of this
classification.

For the exhaustion proof it is cleanest to use the left-handed Weyl basis

```text
Q, L, u^c, d^c, e^c, H, H^dagger,
```

with doubled hypercharges

```text
Y(Q) = +1/3,    Y(L) = -1,
Y(u^c) = -4/3, Y(d^c) = +2/3, Y(e^c) = +2,
Y(H) = +1,     Y(H^dagger) = -1.
```

This is equivalent to the retained right-handed table after replacing each
right-handed field by its left-handed conjugate.

## 4. Excluding Purely Bosonic Dimension-Five Operators

A bosonic dimension-five operator must be made from five units of bosonic
dimension. Possible ingredients are scalars, derivatives, and field
strengths.

### 4.1 Five-scalar terms

A five-scalar term contains `n` copies of `H` and `5-n` copies of
`H^dagger`. Its hypercharge is

```text
Y = n - (5-n) = 2n - 5.
```

This is always odd, hence never zero. Therefore no five-scalar monomial is
`U(1)_Y` invariant.

### 4.2 Field-strength and derivative bosonic terms

One field strength plus three scalars has dimension five, but a single
antisymmetric Lorentz tensor cannot form a Lorentz scalar without another
antisymmetric tensor. Two field strengths plus one scalar also has dimension
five, but a single Higgs doublet or conjugate doublet cannot be an
`SU(2)_L` singlet. Derivatives do not change hypercharge or remove the odd
number of doublets in a dimension-five purely bosonic term.

Thus there is no independent purely bosonic dimension-five Standard Model
operator.

## 5. Excluding Derivative and Dipole Patterns with Two Fermions

### 5.1 Two fermions plus a field strength

A field-strength pattern has the schematic form

```text
psi chi X_munu.
```

The two left-handed Weyl fermions must already form a gauge singlet, because
`X_munu` transforms in an adjoint representation or is abelian. There is no
pair in

```text
Q, L, u^c, d^c, e^c
```

whose product is simultaneously color singlet, weak singlet, and
hypercharge zero:

- `L L` is colorless but has `Y=-2` and is not neutral without two Higgs
  fields;
- `Q u^c`, `Q d^c`, and `L e^c` have the quantum numbers that become
  Yukawa operators only after one Higgs insertion, making dipoles dimension
  six;
- quark-quark and conjugate-quark pairs either carry color or have nonzero
  hypercharge.

Therefore no dimension-five dipole operator exists in the active SM field
content. The familiar dipoles first appear at dimension six after inserting
`H` or `tilde H`.

### 5.2 Two fermions plus one derivative plus one scalar

A derivative pattern has schematic dimension

```text
psi chi D H       or       psi chi H D.
```

The scalar contributes one weak doublet with hypercharge `+1` or `-1`.
The fermion pair must therefore carry the opposite hypercharge and a weak
doublet representation. The only such pairs are exactly the Yukawa-type
pairs

```text
Q u^c,  Q d^c,  L e^c
```

and, if a neutral singlet is admitted, `L nu^c`. These are already made
gauge invariant by one scalar at dimension four. Adding a derivative gives
either a total derivative, an equation-of-motion descendant of the
renormalizable Yukawa operator, or a non-scalar Lorentz structure. Modulo
integration by parts and equations of motion, these do not generate a new
independent dimension-five operator.

Thus every independent dimension-five operator must be of the `psi psi H H`
type.

## 6. Exhaustion of `psi psi H H`

For two fermions and two scalars, hypercharge requires

```text
Y(psi) + Y(chi) + Y(S_1) + Y(S_2) = 0,
```

where each scalar has hypercharge `+1` or `-1`. Therefore the scalar
hypercharge sum is one of

```text
-2, 0, +2.
```

The fermion-pair hypercharge must be the opposite value. Listing the
left-handed Weyl pairs:

| Pair | Pair hypercharge | Can two Higgs fields cancel it? | Result |
| --- | ---: | --- | --- |
| `L L` | `-2` | yes, with `H H` | candidate |
| `Q Q` | `+2/3` | no | rejected |
| `Q L` | `-2/3` | no | rejected |
| `Q u^c` | `-1` | no | rejected |
| `Q d^c` | `+1` | no | rejected |
| `Q e^c` | `+7/3` | no | rejected |
| `L u^c` | `-7/3` | no | rejected |
| `L d^c` | `-1/3` | no | rejected |
| `L e^c` | `+1` | no | rejected |
| `u^c u^c` | `-8/3` | no | rejected |
| `u^c d^c` | `-2/3` | no | rejected |
| `u^c e^c` | `+2/3` | no | rejected |
| `d^c d^c` | `+4/3` | no | rejected |
| `d^c e^c` | `+8/3` | no | rejected |
| `e^c e^c` | `+4` | no | rejected |

Only `L L H H` survives hypercharge. It is colorless because `L` and `H`
are color singlets.

It remains to count the `SU(2)_L` singlets in

```text
2_L x 2_L x 2_H x 2_H.
```

The two possible epsilon-pairing patterns can be represented as

```text
(L_i H)(L_j H),
(L_i L_j)(H H).
```

The second vanishes for a single commuting Higgs doublet because

```text
epsilon_ab H^a H^b = 0.
```

The Schouten identity on two-dimensional `SU(2)` indices then makes every
nonzero contraction proportional to

```text
O_5^{ij} =
epsilon_alpha_beta
(epsilon_ab L_i^{a alpha} H^b)
(epsilon_cd L_j^{c beta} H^d).
```

Thus there is exactly one independent active dimension-five operator,
carrying `Delta L = 2`.

## 7. Symmetry of the Flavor Coefficient

Interchanging the generation labels in `O_5^{ij}` gives two minus signs:

1. one minus sign from exchanging the two fermion fields;
2. one minus sign from the antisymmetric Lorentz contraction
   `epsilon_alpha_beta`.

The two signs cancel, and the Higgs fields commute. Therefore

```text
O_5^{ij} = O_5^{ji}.
```

Only the symmetric part of the coefficient matrix contributes:

```text
kappa_ij = kappa_ji.
```

For three generations this is a complex symmetric `3 x 3` matrix, with six
complex entries before field redefinitions. Gauge symmetry alone does not
fix those entries.

## 8. Post-EWSB Majorana Mass Readout

In unitary gauge, keep only the vacuum component

```text
H = (0, v/sqrt(2))^T.
```

Then

```text
epsilon_ab L_i^a H^b = (v/sqrt(2)) nu_{Li}
```

up to the conventional sign set by the ordering of the doublet components.
Substituting into

```text
L_5 = -(1/2) kappa_ij O_5^{ij} + h.c.
```

gives

```text
L_mass = -(1/2) (kappa_ij v^2/2) nu_{Li}^T C nu_{Lj} + h.c.
```

Therefore

```text
(M_nu)_ij = kappa_ij v^2 / 2.
```

The mass matrix is symmetric because `kappa` is symmetric. Its eigenvalues,
mixing matrix, phases, and absolute scale are not determined by this
operator-classification theorem.

## 9. Scope and Guardrails

This note claims:

- the active Standard Model has no independent dimension-five bosonic,
  derivative, or dipole operator;
- the only independent active `psi psi H H` dimension-five invariant is
  `L L H H`;
- the unique invariant can be written as `(L H)^T C (L H)`;
- it violates lepton number by two units;
- after EWSB it gives `M_nu = kappa v^2/2`.

This note does not claim:

- a value for `kappa` or the scale suppressing it;
- a neutrino mass hierarchy, PMNS matrix, or neutrinoless-double-beta rate;
- a Majorana scale selector;
- a closure of the right-handed singlet Majorana lane;
- a classification including explicit `nu_R` insertions, where singlet-sector
  operators such as `nu_R nu_R` and `nu_R nu_R H^dagger H` belong to the
  separate Majorana operator stack;
- any two-Higgs-doublet, triplet-Higgs, leptoquark, vectorlike-fermion, or
  dimension-six SMEFT classification;
- any time-travel, teleportation, antigravity, dark-sector, or cosmology
  statement.

## 10. Relationship to Existing Notes

- `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` proves the
  dimension-four Dirac Yukawa skeleton and explicitly places the Weinberg
  operator outside its renormalizable classification.
- `EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md` supplies
  the one-Higgs doublet and neutral-vacuum convention used for the `v^2`
  readout.
- `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md` supplies
  the retained hypercharge table.
- `NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md` classifies the bare
  right-handed singlet Majorana operator. This note is the complementary
  active-sector dimension-five classification.
