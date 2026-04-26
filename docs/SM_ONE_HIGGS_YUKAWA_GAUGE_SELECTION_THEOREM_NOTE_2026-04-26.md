# Standard Model One-Higgs Yukawa Gauge-Selection Theorem

**Date:** 2026-04-26

**Status:** standalone positive Standard Model/EW theorem. This note proves
the exact gauge-selection rule for renormalizable Dirac Yukawa monomials in
the one-Higgs-doublet Standard Model matter surface carried by the retained
hypercharge and EW notes. It does not derive any Yukawa eigenvalue, mixing
angle, CKM/PMNS entry, neutrino Majorana scale, Higgs mass, top-Yukawa
normalization, time-travel, teleportation, or antigravity claim.

## 1. Claim

Use the doubled-hypercharge convention of the retained anomaly notes:

```text
Q_em = T_3 + Y/2.
```

One generation has

```text
Q_L   : (3, 2)_{+1/3},
L_L   : (1, 2)_{-1},
u_R   : (3, 1)_{+4/3},
d_R   : (3, 1)_{-2/3},
e_R   : (1, 1)_{-2},
nu_R  : (1, 1)_0       [if the retained neutral singlet is included],
H     : (1, 2)_{+1}.
```

Define the conjugate Higgs doublet

```text
tilde H = i tau_2 H^*,
```

which transforms as

```text
tilde H : (1, 2)_{-1}.
```

Then the complete set of gauge-invariant, renormalizable, baryon- and
lepton-number preserving Dirac Yukawa monomials built from one left-handed
doublet, one right-handed singlet, and either `H` or `tilde H` is exactly

```text
bar Q_L tilde H u_R,
bar Q_L H       d_R,
bar L_L H       e_R,
bar L_L tilde H nu_R        [if nu_R is present].
```

For three generations the same selection rule holds with arbitrary complex
generation matrices:

```text
L_Y = - bar Q_L Y_d H d_R
      - bar Q_L Y_u tilde H u_R
      - bar L_L Y_e H e_R
      - bar L_L Y_nu tilde H nu_R
      + h.c.
```

After electroweak symmetry breaking,

```text
<H> = (0, v/sqrt(2))^T,
```

these terms give Dirac mass matrices

```text
M_u  = Y_u  v/sqrt(2),
M_d  = Y_d  v/sqrt(2),
M_e  = Y_e  v/sqrt(2),
M_nu = Y_nu v/sqrt(2)       [Dirac nu_R option].
```

Gauge symmetry selects the operator pattern and the `H` versus `tilde H`
choice exactly. It does not select the numerical entries of the Yukawa
matrices.

## 2. Why This Adds Value

The retained hypercharge theorem fixes the one-generation charge table, and
the retained EW Higgs gauge-mass theorem fixes the one-doublet Higgs
bookkeeping. What remains useful as a separate proof is the exact bridge from
those charges to the allowed Dirac mass operators.

This theorem supplies that bridge:

- quark Yukawas cannot mix with lepton singlets because of color;
- up-type and neutrino Dirac Yukawas require `tilde H`, not `H`;
- down-type and charged-lepton Yukawas require `H`, not `tilde H`;
- no additional one-Higgs Dirac Yukawa monomial is hidden in the same field
  content;
- gauge symmetry leaves the generation matrices free, so the flavor problem
  remains open rather than silently solved by charge bookkeeping.

## 3. Higgs Conjugation Lemma

Let

```text
epsilon = i tau_2 = [[0, 1], [-1, 0]].
```

For every `U in SU(2)`,

```text
epsilon U^* = U epsilon.
```

This is the defining pseudoreality identity of the `SU(2)` fundamental
representation. Therefore, if

```text
H -> U H,
```

then

```text
tilde H = epsilon H^* -> epsilon U^* H^* = U epsilon H^* = U tilde H.
```

So `tilde H` is again an `SU(2)` doublet. Since complex conjugation reverses
the abelian phase, the hypercharge of `tilde H` is the negative of the
hypercharge of `H`:

```text
Y(H) = +1,
Y(tilde H) = -1.
```

This proves the Higgs-conjugation transformation rule.

## 4. General Form of a Dirac Yukawa Monomial

A renormalizable Dirac Yukawa monomial with the retained fields has the form

```text
bar F_L S f_R,
```

where

```text
F_L in {Q_L, L_L},
f_R in {u_R, d_R, e_R, nu_R},
S in {H, tilde H}.
```

The operator has mass dimension four:

```text
dim(bar F_L) + dim(S) + dim(f_R) = 3/2 + 1 + 3/2 = 4.
```

It is Lorentz invariant in the usual Dirac-bar contraction. Gauge invariance
then imposes three independent conditions.

### 4.1 SU(2) condition

`bar F_L` transforms as the antifundamental doublet and `S` as a fundamental
doublet. Their singlet contraction is unique up to normalization:

```text
bar F_{L,i} S_i.
```

The right-handed field is an `SU(2)` singlet. Thus the `SU(2)` condition is
equivalent to requiring exactly one Higgs doublet or conjugate-Higgs doublet
in the monomial. This is already satisfied by the candidate form.

### 4.2 SU(3) color condition

The color part of `bar F_L S f_R` is:

- `bar Q_L f_R` if `F_L = Q_L`, where `bar Q_L` is a color antifundamental;
- `bar L_L f_R` if `F_L = L_L`, where `bar L_L` is a color singlet.

Therefore:

```text
Q_L can pair only with color-triplet singlets u_R or d_R,
L_L can pair only with color-singlet singlets e_R or nu_R.
```

All quark-lepton crossed Dirac Yukawa monomials are excluded by color before
hypercharge is considered.

### 4.3 U(1)_Y condition

For

```text
bar F_L S f_R,
```

the hypercharge is

```text
-Y(F_L) + Y(S) + Y(f_R).
```

Gauge invariance requires

```text
Y(S) = Y(F_L) - Y(f_R).
```

Since the one-Higgs theory supplies only

```text
Y(H) = +1,
Y(tilde H) = -1,
```

the hypercharge equation either selects `H`, selects `tilde H`, or rejects the
candidate.

## 5. Exhaustion Table

The color-allowed pairings are four. For each, the required scalar
hypercharge is fixed:

| Pairing | Required `Y(S) = Y(F_L) - Y(f_R)` | Selected scalar | Allowed monomial |
| --- | ---: | --- | --- |
| `Q_L -> u_R` | `1/3 - 4/3 = -1` | `tilde H` | `bar Q_L tilde H u_R` |
| `Q_L -> d_R` | `1/3 - (-2/3) = +1` | `H` | `bar Q_L H d_R` |
| `L_L -> e_R` | `-1 - (-2) = +1` | `H` | `bar L_L H e_R` |
| `L_L -> nu_R` | `-1 - 0 = -1` | `tilde H` | `bar L_L tilde H nu_R` |

The rejected Higgs choices fail by nonzero hypercharge:

```text
bar Q_L H u_R:          -1/3 + 1 + 4/3  =  2,
bar Q_L tilde H d_R:    -1/3 - 1 - 2/3  = -2,
bar L_L tilde H e_R:     1   - 1 - 2    = -2,
bar L_L H nu_R:          1   + 1 + 0    =  2.
```

Every quark-lepton crossed candidate is already excluded by the `SU(3)` color
condition. This exhausts all one-left-doublet, one-right-singlet, one-Higgs
Dirac Yukawa monomials.

## 6. Post-EWSB Mass Readout

Write

```text
H = (H^+, (v + h + i chi)/sqrt(2))^T,
tilde H = ((v + h - i chi)/sqrt(2), -H^-)^T.
```

Substituting the vacuum part into the selected monomials gives

```text
bar Q_L tilde H u_R  ->  (v/sqrt(2)) bar u_L u_R,
bar Q_L H d_R        ->  (v/sqrt(2)) bar d_L d_R,
bar L_L H e_R        ->  (v/sqrt(2)) bar e_L e_R,
bar L_L tilde H nu_R ->  (v/sqrt(2)) bar nu_L nu_R.
```

For three generations, the coefficients are matrices in generation space:

```text
M_u  = Y_u  v/sqrt(2),
M_d  = Y_d  v/sqrt(2),
M_e  = Y_e  v/sqrt(2),
M_nu = Y_nu v/sqrt(2).
```

The vacuum component is electrically neutral because

```text
Q_em(H^0) = T_3(H^0) + Y(H)/2 = -1/2 + 1/2 = 0.
```

So the selected Yukawa mass terms preserve the unbroken `U(1)_em`.

## 7. Flavor-Space Consequence

The gauge group acts identically on each generation copy of a given species.
Therefore, if there are three generations, a generation-index coefficient

```text
(Y_f)_{ij}
```

is a gauge singlet for every complex `3 x 3` matrix `Y_f`. Gauge invariance
does not force diagonal form, hierarchy, rank, phase, or texture.

Equivalently, under independent generation-basis rotations,

```text
F_L -> U_L F_L,
f_R -> U_R f_R,
Y_f -> U_L Y_f U_R^dagger,
```

the gauge-selected monomial remains in the same allowed class. Physical CKM
and PMNS data arise from relative diagonalizations of these matrices, not
from the gauge-selection theorem itself.

This is the key boundary: the theorem proves the operator skeleton, while the
program's flavor-normalization and texture lanes remain genuinely open.

## 8. Scope and Guardrails

This note claims:

- the exact `H` versus `tilde H` selection for up, down, charged-lepton, and
  Dirac-neutrino Yukawa monomials;
- exclusion of quark-lepton crossed Dirac Yukawa monomials by color;
- exclusion of the wrong Higgs choice by hypercharge;
- exact post-EWSB Dirac mass matrices `M_f = Y_f v/sqrt(2)`;
- openness of the flavor matrices under gauge symmetry alone.

This note does not claim:

- any numerical Yukawa eigenvalue or hierarchy;
- any CKM or PMNS mixing angle;
- any charged-lepton Koide closure;
- any top-Yukawa Ward normalization;
- any neutrino Majorana mass or seesaw scale;
- any two-Higgs-doublet, triplet-Higgs, leptoquark, vectorlike-fermion, or
  higher-dimensional operator classification;
- any time-travel, teleportation, antigravity, dark-sector, or cosmology
  statement.

The bare right-handed neutrino Majorana term, if allowed by a chosen model,
is a separate gauge-singlet mass operator and is not a one-Higgs Dirac Yukawa
monomial. The Weinberg operator `L_L H L_L H` is dimension five and is also
outside this renormalizable one-Higgs Dirac classification.

## 9. Relationship to Existing Notes

- `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md` supplies
  the hypercharge table used here.
- `EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md` supplies
  the one-Higgs-doublet EW bookkeeping and neutral vacuum convention.
- `YUKAWA_COLOR_PROJECTION_THEOREM.md` concerns a downstream normalization
  factor for the top-Yukawa lane; this note only proves the gauge-allowed
  operator skeleton.
- Neutrino and charged-lepton texture notes may cite this theorem as the
  exact one-Higgs gauge-selection boundary, but their numerical textures and
  normalizations remain separate work.
