# Quark Generation-Stratified Ward Free-Matrix No-Go

**Date:** 2026-04-28

**Status:** proposed_retained exact negative boundary for Lane 3 target 3C.
This note blocks a direct derivation of generation-stratified non-top quark
Yukawa Ward identities from the currently retained one-Higgs gauge-selection
surface, the retained top-channel Ward theorem, the retained three-generation
structure, and the retained CKM atlas alone. It does not claim retained
`m_u`, `m_d`, `m_s`, `m_c`, or `m_b`.

**Primary runner:**
`scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py`

## 1. Question

Lane 3 target 3C asks for generation-stratified Yukawa Ward identities:

```text
y_d/y_t, y_s/y_t, y_b/y_t, y_u/y_t, y_c/y_t
```

analogous in strength to the retained top-channel identity

```text
y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6).
```

The direct tempting route is:

```text
one-Higgs gauge selection
+ top Ward template
+ three-generation structure
+ CKM atlas
=> generation-stratified quark Yukawa values.
```

This note proves that this direct route does not close.

## 2. Minimal Premise Set

Allowed premises:

1. the retained one-Higgs Yukawa gauge-selection theorem;
2. the retained top-channel Ward identity on the `Q_L` block;
3. the retained three-generation matter structure;
4. the retained CKM atlas as a mixing surface;
5. standard linear algebra for singular-value decompositions.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa entries;
3. hidden generation projectors;
4. species-uniform physical reuse of the top Ward identity;
5. treating CKM mixing closure as mass-eigenvalue closure.

## 3. Gauge Selection Leaves Quark Flavor Matrices Free

The one-Higgs theorem selects the quark Dirac monomials

```text
bar Q_L tilde H u_R,
bar Q_L H       d_R.
```

For three generations it therefore permits

```text
- bar Q_L Y_u tilde H u_R
- bar Q_L Y_d H       d_R
+ h.c.
```

where `Y_u` and `Y_d` are arbitrary complex `3 x 3` matrices. The gauge group
acts identically on each generation copy of `Q_L`, `u_R`, and `d_R`, so every
entry of `Y_u` and `Y_d` carries the same gauge quantum numbers inside its
sector. Gauge selection therefore does not force diagonal form, rank,
hierarchy, phases, texture, or eigenvalues.

The exact gauge result is useful: it selects `H` versus `tilde H` and excludes
wrong-Higgs and quark-lepton crossed monomials. But it names the Yukawa matrix
slot; it does not fill it.

## 4. The Top Ward Normalization Is Not A Generation Selector

The retained top Ward theorem derives the exact top-channel normalization

```text
1/sqrt(N_c N_iso) = 1/sqrt(3 * 2) = 1/sqrt(6)
```

from the unit-norm scalar-singlet composite on the `Q_L = (2,3)` block. That
normalization is a color-times-isospin statement. It is not a generation
hierarchy theorem and it does not contain a selector for the `u`, `c`, `t` or
`d`, `s`, `b` eigen-directions.

If one tries to apply the top Ward identity species-uniformly to physical
non-top quarks, the existing bottom-Yukawa analysis already closes that route
negatively: the species-uniform physical reading overshoots `m_b` by about
`35x`. If instead one tries to average over the retained three-generation
triplet, the normalization changes to a new `3 x 2 x 3` or generation-times-
block object and requires a generation/source primitive. That new primitive
is exactly what target 3C is missing; it is not supplied by the top Ward
theorem itself.

## 5. CKM Mixing Does Not Determine Yukawa Singular Values

The CKM atlas fixes a relative left-unitary mixing surface. It does not fix
the singular values of `Y_u` and `Y_d`.

Linear algebra gives the obstruction. For arbitrary positive diagonal
matrices

```text
D_u = diag(y_u, y_c, y_t),
D_d = diag(y_d, y_s, y_b)
```

and a fixed unitary matrix `V`, choose

```text
Y_u = D_u,
Y_d = V D_d.
```

Then the left diagonalizers satisfy

```text
U_u = I,
U_d = V,
U_u^dag U_d = V,
```

while the singular values are exactly the freely chosen diagonal entries of
`D_u` and `D_d`. Changing `D_u` and `D_d` changes all quark Yukawa eigenvalues
but leaves the same CKM matrix `V`.

Therefore CKM closure can cross-check or constrain a mass model once the
Yukawa singular values are supplied, but it cannot by itself derive those
singular values.

## 6. Theorem

**Theorem (direct generation-stratified Ward free-matrix no-go).** On the
current retained Lane 3 support surface consisting of one-Higgs Yukawa gauge
selection, the top-channel `Q_L` Ward identity, retained three-generation
structure, and retained CKM atlas mixing, no generation-stratified non-top
quark Yukawa Ward identities follow.

More precisely, the current surface fixes:

1. the allowed quark Yukawa operator skeletons;
2. the top-channel `1/sqrt(6)` Ward normalization on its stated surface;
3. the existence of three generation sectors;
4. the CKM relative left-unitary mixing package.

It does not fix:

1. the entries, singular values, or eigenvalue hierarchy of `Y_u` or `Y_d`;
2. a generation projector selecting `u`, `c`, `d`, `s`, or `b`;
3. an absolute non-top Yukawa scale;
4. the missing ratios `y_u/y_t`, `y_c/y_t`, `y_d/y_t`, `y_s/y_t`, or
   `y_b/y_t`.

Thus target 3C still requires an additional generation/source-domain,
readout-map, loop-normalization, or equivalent species-differentiation
primitive.

## 7. What This Retires

This note retires the direct route:

```text
one-Higgs gauge selection + top Ward + three generations + CKM
=> non-top quark Yukawa Ward identities.
```

It also blocks two common overreads:

```text
CKM atlas closure => quark mass singular values.
```

```text
top Ward normalization => physical non-top Yukawa boundary conditions.
```

## 8. What Remains Open

Lane 3 remains open. Viable 3C progress now needs a new primitive with a
falsifiable target, for example:

1. a generation/source-domain operator that fixes the Yukawa eigen-directions
   and singular values;
2. a quark endpoint/readout theorem that supplies the missing scalar law;
3. a loop-normalization theorem that differentiates top, charm, up and
   bottom, strange, down without observed-mass input;
4. a no-go theorem proving that a broader primitive class cannot supply the
   needed stratification.

This no-go is compatible with future closure from such a primitive. It only
blocks the direct current-bank route.

## 9. Verification

Run:

```bash
python3 scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py
```

Expected result:

```text
TOTAL: PASS=42, FAIL=0
VERDICT: direct generation-stratified quark Ward route remains open.
```

The runner verifies:

1. exact quark one-Higgs gauge bookkeeping;
2. all nine entries in each quark Yukawa matrix remain gauge allowed;
3. the top Ward normalization is color-times-isospin, not a generation
   selector;
4. a same-CKM/two-spectrum witness showing CKM mixing does not determine
   singular values;
5. the note records comparator and overclaim firewalls.

## 10. Safe Wording

Can claim:

- the direct 3C route from current retained primitives is closed negatively;
- one-Higgs gauge selection leaves `Y_u` and `Y_d` free;
- CKM closure is not quark Yukawa eigenvalue closure;
- non-top absolute quark scales still require a species-differentiated
  primitive.

Cannot claim:

- retained `m_u`, `m_d`, `m_s`, `m_c`, or `m_b`;
- a retained generation-stratified Ward identity;
- a proof that no future source-domain or readout-map primitive can close 3C;
- any observed quark mass as a derivation input.
