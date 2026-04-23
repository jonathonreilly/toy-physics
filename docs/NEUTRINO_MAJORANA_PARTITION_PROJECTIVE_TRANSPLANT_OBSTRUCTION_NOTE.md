# Majorana Partition / Projective Transplant Obstruction

**Date:** 2026-04-15
**Status:** exact frontier boundary on the universal partition/projective
transplant route
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_partition_projective_transplant_obstruction.py`

## Question

After the current exact Majorana lane already has:

- the admitted Nambu-complete local source family,
- the exact background-normalized response curve,
- the exact local self-dual selector `rho = 1`,
- the proof that the current `Z_3` lift is still homogeneous on the selected
  source ray,
- and the proof that the direct-universal tensor/local-closure family does not
  break that homogeneity,

can the **measure side** still rescue the denominator?

More specifically:

- maybe the exact universal UV-finite partition density supplies the missing
  absolute datum
- maybe exact Schur/projective coarse-graining changes the source law
- maybe the canonical refinement-net pullback / density cocycle introduces a
  nontrivial scale selector even when the local action family does not

## Bottom line

No.

On the current exact stack, if the selected Majorana data still enter the
universal partition/projective family only through a homogeneous source ray

`J_lambda = lambda J_0`, `lambda > 0`,

then:

- the exact local partition density changes only by

  `Delta log rho(lambda) = 1/2 lambda^2 <J_0, K^-1 J_0>`

- exact Schur/projective coarse-graining preserves the same source law

  `J_eff,lambda = lambda J_eff,0`

- the refinement/atlas density cocycle is exactly lambda-blind after Jacobian
  compensation

So this QG/measure class also fails to produce a finite absolute Majorana
staircase selector on the current stack.

## Inputs

This theorem combines already-retained exact atlas objects:

- [UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md](./UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md)
- [UNIVERSAL_QG_PROJECTIVE_SCHUR_CLOSURE_NOTE.md](./UNIVERSAL_QG_PROJECTIVE_SCHUR_CLOSURE_NOTE.md)
- [UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md](./UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md)
- [NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md)
- [NEUTRINO_MAJORANA_TENSOR_VARIATIONAL_TRANSPLANT_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_TENSOR_VARIATIONAL_TRANSPLANT_OBSTRUCTION_NOTE.md)

Those already establish:

1. the universal local gravity family defines an exact UV-finite partition
   density on the discrete `3+1` route
2. exact Schur/projective coarse-graining keeps the family inside the same
   Gaussian/universal class
3. the canonical refinement net gives exact section pullback and exact
   density-cocycle behavior
4. the current selected Majorana local data still reduce only to a positive
   homogeneous source ray together with a homogeneous current `Z_3` lift

So the live loophole was:

> maybe the measure/projective side of the exact universal route breaks the
> remaining homogeneity even though the local action family does not

## Exact theorem

### 1. The exact local partition density is still quadratic in the source ray

On the positive-background class, the exact universal local action is

`I_GR(F ; D, J) = 1/2 <F, K(D) F> - <J, F>`

with positive-definite `K(D)`.

The exact measure-compensated local partition density therefore satisfies

`log rho(D, J) = const(D) + 1/2 <J, K(D)^-1 J>`.

So on the current homogeneous source ray

`J_lambda = lambda J_0`

one gets

`Delta log rho(lambda) = 1/2 lambda^2 <J_0, K(D)^-1 J_0>`.

That is nontrivial, but still only one monotone quadratic source law.

### 2. It still has no finite positive selector

Since `K(D)` is positive definite and `J_0 != 0`,

`c := <J_0, K(D)^-1 J_0> > 0`.

Therefore

`Delta log rho(lambda) = 1/2 c lambda^2`

and

`d/dlambda (Delta log rho) = c lambda > 0`

for every `lambda > 0`.

So the partition-density side has no interior finite selector on the current
source ray; only the trivial boundary `lambda = 0` is stationary.

### 3. Exact Schur/projective closure preserves the same source law

The exact Schur/projective theorem says that under an admissible coarse/fine
split the effective coarse family is again Gaussian:

`K_eff = A - B C^-1 B^T`,
`J_eff = eta - B C^-1 xi`.

If the full source lies on the current homogeneous ray

`J_lambda = lambda J_0`,

then the effective source also lies on a homogeneous ray

`J_eff,lambda = lambda J_eff,0`.

So the exact coarse partition density again has the form

`Delta log rho_eff(lambda) = 1/2 lambda^2 <J_eff,0, K_eff^-1 J_eff,0>`.

Exact coarse-graining therefore preserves the same absence of a finite
selector.

### 4. The refinement / overlap cocycle introduces no new lambda dependence

The exact refinement-net theorem says raw partition scalars transform by the
Jacobian cocycle, while the measure-compensated density is invariant.

That Jacobian factor depends on the chart/refinement map, not on `lambda`.

So after compensation, the refinement/overlap law adds no new source-scale
dependence at all.

Therefore the exact refinement-net structure cannot rescue the staircase law on
the current homogeneous source class either.

## The theorem-level statement

**Theorem (Partition/projective transplant obstruction on the current exact
Majorana stack).**
Assume:

1. the exact universal UV-finite partition-density family
2. the exact universal Schur/projective coarse-graining closure
3. the exact canonical refinement-net density cocycle
4. the current Majorana selected data still enter that family only through a
   homogeneous source ray `J_lambda = lambda J_0`

Then:

1. the exact local partition-density response is quadratic in `lambda`
2. it has no finite positive stationary selector
3. exact Schur/projective closure preserves the same homogeneous source law
4. the refinement/atlas density cocycle adds no new lambda dependence

Therefore the universal partition/projective/refinement family does **not** by
itself provide the missing non-homogeneous Majorana local-to-generation bridge
or absolute staircase anchor on the current stack.

## What this closes

This closes the strongest remaining QG/measure rescue path of the form:

- maybe the exact finite partition density, exact projective Schur closure, or
  exact refinement net break the last Majorana homogeneity even if the local
  tensor action family does not

Answer: no, not on the current source class.

So the branch no longer needs vague wording like:

> maybe the measure/projective side of the universal route will supply the
> absolute scale selector

The current exact universal measure/projective family does not do that.

## What this does not close

This note does **not** prove:

- that no future non-Gaussian or non-homogeneous partition family can help
- that no future source insertion beyond the present homogeneous class can work
- that the universal-theory program is ruled out

It is an exact obstruction theorem on the **current** partition/projective
transplant class only.

## Consequence for DM

For the DM denominator this means:

- the universal measure/projective side is real and exact on its own lane
- but it does not rescue the Majorana staircase law on the present selected
  source class

So full zero-import `eta`, and therefore full zero-import DM closure, remains
blocked by the absence of a genuinely new non-homogeneous local-to-generation
bridge or absolute-scale datum beyond all currently exhausted classes.

## Safe wording

**Can claim**

- the exact universal partition/projective/refinement family is present on the
  atlas
- feeding the current self-dual Majorana source ray into that family preserves
  the source-scale law
- so this QG/measure route is not the missing absolute staircase selector on
  the current stack

**Cannot claim**

- that no future non-Gaussian extension can ever help
- that the negative answer is final in principle

## Command

```bash
python3 scripts/frontier_neutrino_majorana_partition_projective_transplant_obstruction.py
```
