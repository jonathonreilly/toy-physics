# Charged-Lepton Two-Higgs Observable Inverse Problem

**Date:** 2026-04-15  
**Status:** exact local-generic inverse-problem theorem on the canonical
charged-lepton-side minimal branch  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_charged_lepton_two_higgs_observable_inverse_problem.py`

## Question

On the canonical minimal charged-lepton-side two-Higgs branch, are the seven
canonical quantities real local physical data, or is there hidden continuous
redundancy beyond the exact rephasing quotient?

## Bottom line

They are real local physical data.

On the canonical charged-lepton branch

`Y_e = diag(x^e_1,x^e_2,x^e_3) + diag(y^e_1,y^e_2,y^e_3 e^{i delta_e}) C`

the Hermitian observable

`H_e = Y_e Y_e^dag`

has an exact seven-coordinate local observable grammar:

- three diagonal entries
- three off-diagonal moduli
- one rephasing-invariant triangle phase

The map from the seven canonical quantities

`(x^e_1,x^e_2,x^e_3,y^e_1,y^e_2,y^e_3,delta_e)`

to those seven coordinates has full Jacobian rank on a generic open dense
subset. Those seven coordinates also reconstruct `H_e` exactly.

So no hidden continuous redundancy remains beyond the exact rephasing quotient.

## Atlas and axiom inputs

This theorem reuses:

- `Charged-lepton two-Higgs canonical reduction`
- `Lepton single-Higgs PMNS triviality theorem`

The only new step is to show that the seven-count on the charged-lepton side is
not a formal parameter count hiding extra local redundancy.

## Local observable grammar

Because `H_e` is Hermitian and rephasing acts by diagonal conjugation, a local
coordinate chart on the canonical branch is

- `H_{11}`
- `H_{22}`
- `H_{33}`
- `|H_{12}|`
- `|H_{23}|`
- `|H_{31}|`
- `arg(H_{12} H_{23} H_{31})`

This is the charged-lepton-side analogue of the already derived neutrino-side
observable grammar.

## Theorem-level statement

**Theorem (Charged-lepton two-Higgs local inverse problem).** Assume the exact
charged-lepton two-Higgs canonical reduction theorem. Then on the generic
charged-lepton-side canonical branch:

1. the seven canonical quantities map generically locally one-to-one onto the
   seven-coordinate observable grammar of `H_e = Y_e Y_e^dag`
2. those seven observable coordinates reconstruct `H_e` exactly

Therefore the minimal charged-lepton-side branch is a real local closure target
and not a hidden overcount.

## What this closes

This closes the charged-lepton-side analogue of the neutrino observable
inverse-problem theorem.

It is now exact that:

- the charged-lepton minimal branch is canonical
- it has exactly seven real physical quantities
- those seven quantities are locally identifiable from `H_e`

## What this does not close

This note does **not** derive:

- the seven charged-lepton canonical quantities
- a selector choosing the charged-lepton-side branch over the neutrino-side one
- a bridge relating the charged-lepton-side canonical quantities to the
  neutrino-side ones

It is a local inverse-problem theorem only.

## Command

```bash
python3 scripts/frontier_charged_lepton_two_higgs_observable_inverse_problem.py
```
