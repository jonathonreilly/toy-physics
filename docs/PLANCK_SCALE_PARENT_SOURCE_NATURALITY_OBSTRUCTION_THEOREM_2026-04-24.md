# Planck-Scale Parent-Source Naturality Obstruction Theorem

**Date:** 2026-04-24
**Status:** parent-source object-class reduction/no-go; not a bare closure
**Verifier:** `scripts/frontier_planck_parent_source_naturality_obstruction_theorem_2026_04_24.py`

## Question

Can the gravitational parent-source boundary-action object class be derived
from the bare gravity sector, rather than retained as the object class in which
the Schur/event Ward bridge is interpreted?

Equivalently:

> if the primitive event source `exp(s P_A)` is applied before microscopic
> Schur reduction, floor subtraction, and multiplicity lift, does the resulting
> Schur scalar necessarily equal the primitive event insertion generator?

## Result

The parent-source carrier diagram commutes, but the scalar action-source
normalization still has a one-dimensional obstruction.

The finite event Ward derivative is exact:

`d/ds log Tr(rho_cell exp(s P_A))|_(s=0) = Tr(rho_cell P_A) = 1/4`.

The Schur/event equality is a different statement:

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

The bare Schur gravity data determine `L_Sigma`, its floor
`lambda_min(L_Sigma)`, the quotient carrier `H_q`, and the multiplicity lift
`P_q -> P_A`. They do not determine the additive scalar `nu`.

Therefore the functorial Schur representation remains an object-class input:

> the Schur normal-ordered boundary action must be stipulated or derived as a
> functorial representation of the same parent source, with no extra
> source-free one-dimensional character.

Without that input, the family

`nu(delta) = lambda_min(L_Sigma) + Tr(rho_cell P_A) + delta`

has the same bare Schur carrier, same Schur floor, same quotient map, same
multiplicity lift, and same finite event derivative, but gives

`p_Schur(delta) = Tr(rho_cell P_A) + delta`.

The quotient of Schur and event source groups is the hidden character

`chi_delta(s) = exp(s delta)`.

So the parent-source object-class derivation is **still open**, but sharply
reduced to one theorem target:

> derive from the gravity sector that `delta = 0`, equivalently that no
> source-free one-dimensional boundary-action character may be attached to the
> Schur normal-ordered scalar.

## Inputs

The attempt uses the currently retained gravity/boundary stack:

1. the primitive event source

   `B_parent = (H_A, P_A)`,

   where

   `H_A = span{|t>, |x>, |y>, |z>}`

   and

   `P_A = P_t + P_x + P_y + P_z`;

2. the source-free cell state

   `rho_cell = I_16 / 16`;

3. the minimal Schur quotient

   `H_q = span{|t>, |s>}`,

   where

   `|s> = (|x> + |y> + |z>) / sqrt(3)`;

4. the Schur witness

   `L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`

   with

   `lambda_min(L_Sigma) = 1`;

5. the retained spatial-doublet multiplicity

   `H_A = H_q (+) E`,

   with

   `P_A = P_q + P_E`;

6. the multiplicity mass identity

   `Tr(rho_cell P_A) = 2 Tr(rho_cell P_q) = 1/4`.

None of these inputs contains `nu = 5/4`.

## The Diagram Attempt

Let

`Q : H_A -> H_q`

be the canonical quotient map

`Q|t> = |t>`,

`Q|x> = Q|y> = Q|z> = |s>/sqrt(3)`.

Apply the primitive event source before Schur reduction:

`U_A(s) = exp(s P_A)`.

On `H_A`, the parent projector is the identity, so

`U_A(s)|_(H_A) = exp(s) I_(H_A)`.

Reducing after applying the source gives

`Q U_A(s) Q^* = exp(s) I_(H_q)`.

Reducing the projector first and then exponentiating gives the same quotient
source:

`exp(s Q P_A Q^*) = exp(s) I_(H_q)`.

Thus primitive source insertion and microscopic Schur quotient reduction
commute at the parent-source carrier level.

Now floor-subtract the Schur carrier:

`L_0 = L_Sigma - lambda_min(L_Sigma) I`.

Because the reduced source is scalar on `H_q`, it commutes with the
floor-subtracted Schur shape:

`exp(s) I_(H_q) L_0 = L_0 exp(s) I_(H_q)`.

Finally multiplicity-lift the quotient source by restoring the retained
doublet:

`P_q -> P_q + P_E = P_A`.

At the projector/source-group level this gives back

`I_(H_A) + (exp(s)-1)(P_q + P_E) = exp(s) I_(H_A)`.

So the carrier-level naturality diagram commutes:

```text
parent event source exp(s P_A)
        |
        | quotient Schur reduction Q
        v
quotient source exp(s I_q)
        |
        | floor subtraction L_Sigma -> L_Sigma - lambda_min I
        v
same quotient source on the normal-ordered Schur shape
        |
        | multiplicity lift P_q -> P_q + P_E
        v
lifted parent source exp(s P_A)
```

This is the strongest positive result of the attempt.

## Theorem 1: the finite event Ward derivative is not the Schur/event equality

The finite event source functional is

`Z_A(s) = Tr(rho_cell exp(s P_A))`.

Since `P_A` is a projector,

`Z_A(s) = 1 + (exp(s)-1) Tr(rho_cell P_A)`.

Therefore

`d/ds log Z_A(s)|_(s=0) = Tr(rho_cell P_A) = 1/4`.

This theorem does not mention `L_Sigma` or `nu`.

The Schur/event equality is the additional scalar identification

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

It identifies the Schur normal-ordered pressure with the event source
generator. That is not a consequence of the finite derivative alone.

## Theorem 2: the Schur parent-source carrier diagram commutes

With `Q` as above,

`Q P_A Q^* = I_(H_q)`.

Therefore

`Q exp(s P_A) Q^* = exp(s I_(H_q))`.

The Schur floor subtraction

`L_Sigma -> L_Sigma - lambda_min(L_Sigma) I`

does not disturb that source, because the reduced source is scalar on `H_q`.

The multiplicity lift restores the invisible doublet:

`P_q + P_E = P_A`.

Hence applying `exp(s P_A)` before Schur quotient reduction, then
normal-ordering the Schur carrier, then restoring retained multiplicity returns
the same parent source group on `H_A`.

This closes the naturality diagram at the level of carriers, projectors, and
source-group support.

## Theorem 3: bare Schur gravity still leaves an affine scalar obstruction

The Schur normal-ordered scalar has the form

`p_Schur = nu - lambda_min(L_Sigma)`.

For every real `delta`, define

`nu(delta) = lambda_min(L_Sigma) + Tr(rho_cell P_A) + delta`.

Then

`p_Schur(delta) = Tr(rho_cell P_A) + delta`.

Changing `delta` leaves all carrier data used above unchanged:

1. `L_Sigma` is unchanged;
2. `lambda_min(L_Sigma)` is unchanged;
3. the quotient map `Q` is unchanged;
4. the decomposition `P_A = P_q + P_E` is unchanged;
5. the finite event derivative remains `Tr(rho_cell P_A) = 1/4`;
6. the carrier-level naturality diagram still commutes.

But the Schur/event scalar equality holds only when `delta = 0`.

For `delta != 0`, the quotient of the Schur scalar source group by the event
source group is

`chi_delta(s) = exp(s delta)`.

This is a source-free one-dimensional boundary-action character: it changes no
Schur carrier, no quotient, no multiplicity, and no event derivative. It only
changes the scalar action-source normalization.

Therefore any theorem that uses only the current bare Schur gravity data is
invariant under `delta`, while the desired equality is not invariant under
`delta`. Such a theorem cannot force `delta = 0`.

This is the theorem-grade obstruction.

## Consequence

The gravitational parent-source boundary-action object-class item is not
closed from the bare gravity sector in this pass.

What is now closed:

1. finite event Ward derivative;
2. quotient reduction of `exp(s P_A)`;
3. compatibility of source insertion with Schur floor subtraction;
4. multiplicity lift of the quotient source back to `P_A`;
5. carrier-level commutativity of the Schur parent-source diagram.

What remains open:

> derive from the gravity sector that the Schur normal-ordered scalar carries
> no extra source-free one-dimensional character.

Equivalently:

> derive that the Schur normal-ordered boundary action is a functorial
> representation of the same parent source, not the same carrier plus
> `chi_delta`.

Until that theorem is proved, the Schur/event equality remains conditional on
the retained parent-source boundary-action object class.

## Safe Claim

Use:

> The parent-source naturality diagram now commutes through Schur quotient
> reduction, floor subtraction, and multiplicity lift. The remaining bare
> obstruction is exactly one affine source-free character in the Schur scalar
> normalization.

Do not use:

> Bare gravity already derives the parent-source boundary-action object class.

Do not use:

> The finite event Ward derivative alone proves the Schur/event equality.
