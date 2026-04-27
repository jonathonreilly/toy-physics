# Charged-Lepton Direct Ward Free-Yukawa No-Go

**Date:** 2026-04-26

**Status:** support / exact negative boundary / target-closure no-go. This note
blocks a direct lift of the retained top Ward identity to a charged-lepton
`y_tau` theorem using only one-Higgs gauge selection and the existing top
Ward template. It does not claim charged-lepton mass closure, Koide closure,
a tau mass prediction, or any numerical charged-lepton Yukawa eigenvalue.

**Primary runner:**
`scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py`

## 1. Claim

The one-Higgs Standard Model gauge-selection theorem proves that the
charged-lepton Dirac monomial

```text
bar L_L H e_R
```

is allowed, while

```text
bar L_L tilde H e_R
```

is rejected by hypercharge. For three generations the allowed operator is

```text
- bar L_L Y_e H e_R + h.c.
```

with an arbitrary complex `3 x 3` matrix `Y_e`.

Therefore one-Higgs gauge selection does not determine `y_tau`, any
charged-lepton Yukawa eigenvalue, any hierarchy, or any charged-lepton
mass ratio. A retained absolute charged-lepton mass theorem needs an
additional primitive beyond direct top-Ward analogy: a generation-selection,
loop-normalization, or source-domain law.

## 2. Exact Gauge Bookkeeping

Use the doubled-hypercharge convention

```text
Q_em = T_3 + Y/2.
```

The retained one-Higgs theorem uses

```text
L_L : (1, 2)_{-1},
e_R : (1, 1)_{-2},
H   : (1, 2)_{+1},
tilde H : (1, 2)_{-1}.
```

For a Dirac Yukawa monomial `bar F_L S f_R`, the doubled-hypercharge sum is

```text
-Y(F_L) + Y(S) + Y(f_R).
```

Thus

```text
bar L_L H e_R:       -(-1) + 1 + (-2) = 0,
bar L_L tilde H e_R: -(-1) - 1 + (-2) = -2.
```

The charged-lepton operator is selected only with `H`. The wrong-Higgs
operator is exactly rejected.

## 3. Free Generation Matrix

The gauge group acts identically on each generation copy of `L_L` and `e_R`.
Consequently every entry

```text
(Y_e)_{ij} bar L_{L,i} H e_{R,j}
```

has the same gauge quantum numbers. Diagonal and off-diagonal entries are
equally gauge invariant.

Under generation-basis rotations,

```text
L_L -> U_L L_L,
e_R -> U_R e_R,
Y_e -> U_L Y_e U_R^dagger,
```

the entries of `Y_e` change but the operator remains in the same allowed
gauge class. Gauge selection therefore cannot select diagonal form, rank,
hierarchy, phase, texture, eigenvalues, or a tau-generation entry.

This is the exact obstruction to the direct retained objective:

```text
one-Higgs gauge selection + SM bridge M_e = Y_e v/sqrt(2)
```

does not remove the charged-lepton Yukawa import. It only names where the
import sits.

## 4. Why the Top Ward Factor Does Not Transfer

The retained top Ward theorem states the top-channel identity

```text
y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)
```

on its stated surface. The load-bearing normalization is the unit-norm
scalar-singlet composite on the `Q_L` block, with

```text
N_c x N_iso = 3 x 2 = 6.
```

The charged-lepton monomial is colorless:

```text
N_color = 1.
```

Its direct gauge-index normalization options are:

```text
post-EWSB charged component: 1,
lepton weak doublet:         1 x 2 = 2.
```

Neither gives `6`. Producing a formal `2 x 3 = 6` would require adding a
generation-triplet averaging primitive. That is not one-Higgs gauge
selection, and it does not select `tau`; it is precisely the kind of new
generation/source law this no-go says is still missing.

So the top Ward identity remains retained for its top-sector surface, but it
does not by itself become a charged-lepton `y_tau` theorem.

## 5. Comparator Firewall

The runner prints charged-lepton masses only as comparator values. They are
not proof inputs. This matters because the bounded charged-lepton package
currently uses PDG charged-lepton masses as a three-real observational pin.

This no-go does not retire that pin. It narrows the retirement task.

## 6. Retained-Objective Consequence

The retained absolute charged-lepton mass objective remains open. The first
gate is now sharper:

```text
Required next primitive:
  a generation-selection / loop-normalization / source-domain law
  that fixes Y_e eigenvalues or at least a retained y_tau scale
  without using PDG charged-lepton masses as inputs.
```

Safe downstream wording:

```text
The direct top-Ward lift is closed. One-Higgs gauge selection proves the
charged-lepton operator skeleton and the SM mass bridge, but leaves Y_e free.
```

Unsafe downstream wording:

```text
The top Ward identity derives y_tau.
```

## 7. Relationship to Existing Notes

- `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` supplies
  the exact one-Higgs operator selection and states that generation matrices
  remain free.
- `YT_WARD_IDENTITY_DERIVATION_THEOREM.md` supplies the retained top-sector
  Ward identity on the `Q_L` scalar-singlet surface.
- `YUKAWA_COLOR_PROJECTION_THEOREM.md` concerns top-sector color projection
  corrections and does not supply a charged-lepton `Y_e` selector.
- `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` remains the
  bounded charged-lepton review: charged-lepton masses are not retained on
  the current surface without an observational pin or new primitive.
