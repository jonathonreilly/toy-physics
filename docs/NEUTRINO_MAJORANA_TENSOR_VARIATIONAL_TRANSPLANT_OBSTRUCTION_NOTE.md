# Majorana Tensor-Variational Transplant Obstruction

**Date:** 2026-04-15
**Status:** exact frontier boundary on the direct-universal tensor/local-closure
transplant route
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_tensor_variational_transplant_obstruction.py`

## Question

After the exact local Majorana lane has already fixed:

- the admitted Nambu-complete local family,
- the exact background-normalized response curve,
- the exact self-dual local selector `rho = 1`,
- and the fact that the current `Z_3` lift is still homogeneous on the
  selected ray,

can the **direct-universal tensor variational / positive-background local
closure family** from the atlas act as the missing absolute staircase bridge?

Equivalently:

- maybe the gravity-side tensor Hessian is the genuinely new non-scalar object
  we needed
- maybe its exact local action family breaks the old homogeneity
- maybe the unique stationary tensor field fixes a finite Majorana scale even
  though the current local/generation source class does not

## Bottom line

No.

The direct-universal tensor/local-closure family is exact and useful, but if
the current selected Majorana local-to-generation data still enter it only as
a homogeneous source ray

`J_lambda = lambda J_0`, `lambda > 0`,

then the universal local family stays homogeneous under that same rescaling:

- the exact stationary field is

  `F_*(lambda) = K(D)^-1 J_lambda = lambda K(D)^-1 J_0`

- the exact stationary action is

  `I_*(lambda) = -1/2 <J_lambda, K(D)^-1 J_lambda>
                = -1/2 lambda^2 <J_0, K(D)^-1 J_0>`

- normalized stationary profiles are identical across `lambda`
- the stationary action has no intrinsic finite selector on `lambda > 0`

So this transplant route does **not** supply the missing non-homogeneous
Majorana local-to-generation bridge on the current stack.

## Inputs

This theorem uses only already-retained exact atlas objects:

- [UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md](./UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md)
- [UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md](./UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md)
- [NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md)

Those notes already establish:

1. the direct-universal route has the exact tensor-valued Hessian candidate
2. on the positive-background family `D`, the local action family is exact and
   has a unique stationary solution for every source
3. the current exact Majorana selected local data still reduce only to a
   positive source ray together with a homogeneous `Z_3` lift

So the live loophole was narrower:

> maybe the gravity-side tensor/local-closure family turns that projective
> source ray into an absolute scale selector

## Exact theorem

### 1. The direct-universal local family is linear/quadratic in the source

On the exact positive-background local family, the action is

`I_GR(F ; D, J) = 1/2 <F, K(D) F> - <J, F>`

with `K(D)` symmetric positive definite.

Therefore the unique stationary field is

`F_*(D, J) = K(D)^-1 J`

and the stationary value is

`I_*(D, J) = -1/2 <J, K(D)^-1 J>`.

So the exact local family is:

- linear in `J` at the stationary field level
- quadratic in `J` at the stationary action level

### 2. A homogeneous Majorana source ray stays homogeneous after transplant

Take the current exact selected Majorana ray and any current homogeneous
generation representative, and feed that family into the universal local
closure route as

`J_lambda = lambda J_0`, `lambda > 0`.

Then

`F_*(lambda) = lambda F_*(1)`

and

`I_*(lambda) = lambda^2 I_*(1)`.

So:

- normalized stationary field profiles are unchanged across `lambda`
- dimensionless stationary-field ratios are unchanged across `lambda`
- the stationary value carries only the same common scale factor `lambda^2`

### 3. No finite staircase selector appears on that family

Since `K(D)` is positive definite,

`c := <J_0, K(D)^-1 J_0> > 0`

for every nonzero `J_0`.

Therefore

`I_*(lambda) = -1/2 c lambda^2`

and hence

`d I_* / d lambda = -c lambda`.

So on `lambda > 0`:

- there is no interior stationary point
- there is no finite preferred `lambda`
- only the trivial boundary `lambda = 0` is stationary

That is not an absolute Majorana staircase selector.

## The theorem-level statement

**Theorem (Tensor-variational transplant obstruction on the current exact
Majorana stack).**
Assume:

1. the exact direct-universal tensor/local-closure family
   `I_GR(F ; D, J) = 1/2 <F, K(D) F> - <J, F>`
   with positive-definite `K(D)`
2. the exact local Majorana self-dual-selected data already reduce to a
   homogeneous positive source ray and a homogeneous current `Z_3` lift
3. the attempted bridge feeds the current Majorana data into the universal
   tensor/local-closure family only through a source ray `J_lambda = lambda J_0`

Then:

1. the exact stationary field scales linearly in `lambda`
2. the exact stationary action scales quadratically in `lambda`
3. normalized stationary profiles are identical across `lambda`
4. no intrinsic finite positive selector for `lambda` is generated

Therefore the direct-universal tensor/local-closure family does **not** by
itself provide the missing non-homogeneous Majorana local-to-generation bridge
or absolute staircase anchor on the current stack.

## What this closes

This closes the strongest remaining gravity/atlas rescue path of the form:

- maybe the exact universal tensor Hessian and exact positive-background local
  closure family are the missing absolute Majorana selector after all

Answer: no, not on the present source class.

So the branch no longer needs vague wording like:

> maybe the gravity-side tensor route will break the remaining homogeneity

The current exact tensor/local-closure family does not do that.

## What this does not close

This note does **not** prove:

- that no future tensor-valued axiom-side bridge can work
- that no future non-homogeneous source insertion into a tensor family can be
  derived
- that the universal-theory program is ruled out

It is an exact obstruction theorem on the **current** direct-universal
tensor/local-closure transplant class only.

## Consequence for DM

For the DM denominator this means:

- the current gravity/atlas tensor family is real and exact
- but it does not rescue the Majorana staircase law on the present selected
  source class

So full zero-import `eta`, and therefore full zero-import DM closure, is still
blocked not by missing local tensor structure, but by the absence of a
genuinely new **non-homogeneous** local-to-generation bridge or absolute-scale
datum beyond all currently exhausted classes.

## Safe wording

**Can claim**

- the direct-universal tensor/local-closure family is exact on its own lane
- feeding the current self-dual Majorana source ray into that family leaves
  the overall scale homogeneous
- so this gravity/atlas route is not the missing absolute staircase selector
  on the current stack

**Cannot claim**

- that no future tensor-side extension can ever help
- that the negative answer is final in principle

## Command

```bash
python3 scripts/frontier_neutrino_majorana_tensor_variational_transplant_obstruction.py
```
