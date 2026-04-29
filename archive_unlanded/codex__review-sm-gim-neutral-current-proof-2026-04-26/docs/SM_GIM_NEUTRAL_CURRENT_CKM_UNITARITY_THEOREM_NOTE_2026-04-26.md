# Standard Model GIM Neutral-Current and CKM Projector Theorem

**Date:** 2026-04-26

**Status:** retained Standard Model flavor/gauge structural guardrail on the
active one-Higgs field content. This note proves that, for the active
one-Higgs Standard Model with generation-universal gauge representations and
arbitrary complex Yukawa matrices, passing to the fermion mass basis leaves
photon, gluon, and `Z` neutral currents flavor diagonal at tree level. All
quark flavor change in the renormalizable gauge sector is confined to the
charged `W` current through a single unitary matrix

```text
V_CKM = U_uL^dagger U_dL.
```

The same unitarity gives the exact GIM projector cancellation of every
generation-independent charged-current loop kernel. The theorem does not
derive any CKM entry, CP phase, quark mass, PMNS angle, rare-decay rate,
baryogenesis asymmetry, or beyond-SM flavor completion.

**Primary runner:** `scripts/frontier_sm_gim_neutral_current_ckm_unitarity.py`

## 1. Claim

Work after electroweak symmetry breaking, with canonical kinetic terms and
the retained one-Higgs Yukawa operator pattern. Let the three-generation
Yukawa matrices be arbitrary complex matrices:

```text
Y_u, Y_d, Y_e.
```

Choose singular-value decompositions

```text
U_uL^dagger Y_u U_uR = D_u,
U_dL^dagger Y_d U_dR = D_d,
U_eL^dagger Y_e U_eR = D_e,
```

where `D_f` are real nonnegative diagonal matrices. Define mass-basis fields
by

```text
u_L^gauge = U_uL u_L^mass,       u_R^gauge = U_uR u_R^mass,
d_L^gauge = U_dL d_L^mass,       d_R^gauge = U_dR d_R^mass,
e_L^gauge = U_eL e_L^mass,       e_R^gauge = U_eR e_R^mass.
```

Then:

1. every tree-level neutral gauge current remains generation diagonal in the
   mass basis;
2. the charged quark current becomes

```text
J_W^mu = bar u_L^mass gamma^mu V_CKM d_L^mass,
V_CKM = U_uL^dagger U_dL;
```

3. `V_CKM` is unitary;
4. for any generation-independent loop kernel `c I_3`,

```text
V_CKM (c I_3) V_CKM^dagger = c I_3,
V_CKM^dagger (c I_3) V_CKM = c I_3,
```

so the off-diagonal flavor-changing neutral amplitude from the common part of
a charged-current loop cancels exactly:

```text
sum_i V_ai V_bi^* = 0       for a != b.
```

This is the exact local gauge-theory core of the GIM mechanism. Nondegenerate
internal masses or higher-dimensional operators can leave residual loop-level
or EFT flavor change; those are outside this tree-level/projector theorem.

## 2. Why This Moves the Program Forward

The retained one-Higgs Yukawa theorem correctly leaves the Yukawa matrices
free. The retained CKM notes study numerical and geometric structure of the
CKM surface. What is useful as a separate proof is the gauge-theory bridge
between those facts:

- arbitrary Yukawa diagonalization does not create tree-level neutral-current
  flavor change;
- the only quark flavor matrix in the renormalizable gauge sector is the
  left-handed up/down mismatch `U_uL^dagger U_dL`;
- CKM unitarity is not an optional phenomenological fit condition at this
  level; it follows from canonical field redefinitions;
- every mass-independent charged-current loop contribution has an exact
  off-diagonal cancellation before any model-specific loop integral is used.

This closes a structural reviewer gap without promoting any numerical CKM,
kaon, `B`-physics, or PMNS prediction.

## 3. Input Surface

The theorem uses only standard consequences of the retained SM field content:

| input | role |
| --- | --- |
| three replicated generations with identical gauge representations | gauge generators act as identity on generation space |
| one-Higgs Yukawa operator pattern | supplies arbitrary complex `Y_u,Y_d,Y_e` mass matrices |
| canonical kinetic terms | allow unitary flavor rotations without changing kinetic normalization |
| electroweak gauge diagonalization | identifies photon, `Z`, and `W^pm` currents |

No observed mass, mixing angle, CKM phase, rare-decay datum, or loop
matching coefficient is used.

## 4. Diagonalization Lemma

For any complex matrix `Y_f`, the positive Hermitian matrix `Y_f Y_f^dagger`
has an orthonormal eigenbasis. Let `U_fL` collect those eigenvectors. Let
`U_fR` be the corresponding right singular-vector matrix on the support of
`Y_f`, completed arbitrarily on any null singular subspace. Then

```text
U_fL^dagger Y_f U_fR = D_f
```

with `D_f` diagonal and nonnegative.

Degenerate singular values leave a unitary freedom inside the degenerate
subspace. That freedom does not affect the theorem because every neutral
gauge generator below is proportional to the identity in generation space,
and the charged-current matrix remains a product of unitary matrices.

## 5. Neutral-Current Universality Lemma

Fix a fermion species `f` with a definite gauge representation: for example
`u_L`, `d_L`, `u_R`, `d_R`, `e_L`, or `e_R`. In the gauge basis, any neutral
gauge current has generation-space form

```text
bar f^gauge gamma^mu (c_f I_3) f^gauge X_mu,
```

where `X_mu` is a neutral gauge boson or gluon field, and `c_f` may include
electric charge, weak isospin, hypercharge, color generator, and coupling
factors. The important point is not the numerical value of `c_f`; it is that
`c_f` is the same for all three generations of the same species.

Apply the mass-basis rotation

```text
f^gauge = U_f f^mass.
```

Then the generation matrix in the neutral current becomes

```text
U_f^dagger (c_f I_3) U_f = c_f U_f^dagger U_f = c_f I_3.
```

Thus the transformed current is still diagonal in generation:

```text
bar f^mass gamma^mu (c_f I_3) f^mass X_mu.
```

This proves absence of tree-level neutral-current flavor changing couplings
for photon, gluon, and `Z` exchange.

For gluons the color generator acts on color space, not generation space:

```text
T^A_color tensor I_generation.
```

Generation rotations commute with `T^A_color`, so the same identity applies.

## 6. Charged-Current Mismatch Lemma

In the gauge basis, the quark charged current is

```text
J_W^mu = bar u_L^gauge gamma^mu d_L^gauge.
```

Rotate to the mass basis:

```text
u_L^gauge = U_uL u_L^mass,
d_L^gauge = U_dL d_L^mass.
```

The current becomes

```text
J_W^mu
  = bar u_L^mass U_uL^dagger gamma^mu U_dL d_L^mass
  = bar u_L^mass gamma^mu (U_uL^dagger U_dL) d_L^mass.
```

Therefore

```text
V_CKM = U_uL^dagger U_dL.
```

Since `U_uL` and `U_dL` are unitary,

```text
V_CKM V_CKM^dagger
  = U_uL^dagger U_dL U_dL^dagger U_uL
  = U_uL^dagger U_uL
  = I_3,
```

and similarly

```text
V_CKM^dagger V_CKM = I_3.
```

So the charged-current flavor matrix is exactly unitary.

Right-handed rotations do not enter this charged current, because the
renormalizable `W` interaction couples only to left-handed weak doublets.

## 7. GIM Projector Corollary

Consider a charged-current loop contribution between two external up-type
flavors `a,b` with internal down-type generation index `i`. Its CKM factor
has the form

```text
A_ab = sum_i V_ai F_i V_bi^*,
```

where `F_i` is the loop kernel attached to the internal generation. Split the
kernel into a generation-independent part and a residual:

```text
F_i = F_0 + Delta F_i.
```

The common part contributes

```text
A_ab(common)
  = F_0 sum_i V_ai V_bi^*
  = F_0 (V V^dagger)_ab
  = F_0 delta_ab.
```

Hence for `a != b`,

```text
A_ab(common) = 0.
```

The same identity holds for down-type external flavors with the projector
`V^dagger V = I_3`.

The residual term

```text
sum_i V_ai Delta F_i V_bi^*
```

need not vanish when the internal masses are nondegenerate. This theorem is
therefore the exact GIM cancellation of the common projector piece, not a
claim that all loop-level flavor-changing neutral processes vanish.

## 8. Theorem Proof

Start from arbitrary complex Yukawa matrices. By Section 4, choose unitary
left and right rotations that diagonalize the fermion mass matrices.

For each neutral current, the gauge generator is proportional to the
identity on generation space for a fixed species. Section 5 shows that any
unitary mass-basis rotation conjugates this identity back to itself. Thus
neutral currents are flavor diagonal at tree level.

For the charged quark current, the up- and down-type members of the weak
doublet may require different left rotations. Section 6 shows that the only
surviving generation matrix is `V_CKM = U_uL^dagger U_dL`, and that it is
unitary.

Finally, Section 7 applies this unitarity to charged-current loop projectors,
showing exact cancellation of every generation-independent off-diagonal
neutral amplitude. This proves the theorem.

## 9. Scope Boundaries

This theorem does not claim:

- that CKM entries, phases, or Wolfenstein parameters are derived;
- that loop-level flavor-changing neutral processes vanish once internal
  masses are nondegenerate;
- that higher-dimensional SMEFT operators such as
  `(H^dagger i D_mu H)(bar q_i gamma^mu q_j)` are absent;
- that PMNS angles are fixed;
- that any rare-decay branching ratio, kaon observable, baryogenesis
  asymmetry, or beyond-SM flavor completion follows.

It proves the renormalizable SM gauge-structure fact needed before those
lanes can be interpreted: tree-level neutral-current flavor change is
forbidden by generation universality and unitary mass-basis rotations, while
charged-current flavor change is controlled by one unitary mismatch matrix.

## 10. Executable Audit

The runner

```bash
python3 scripts/frontier_sm_gim_neutral_current_ckm_unitarity.py
```

checks the retained authority files, exact rational unitary witness
rotations, nontrivial Yukawa diagonalization, neutral-current identity
conjugation, CKM unitarity, exact common-kernel GIM projector cancellation,
and a nondegenerate-kernel residual guardrail.

Expected:

```text
TOTAL: PASS=72, FAIL=0
```
