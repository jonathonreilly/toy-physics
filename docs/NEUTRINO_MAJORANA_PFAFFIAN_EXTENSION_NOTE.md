# Minimal Pfaffian `Delta L = 2` Extension

**Date:** 2026-04-15  
**Status:** exact construction on a constructed microscopic extension; not yet
axiom-forced  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_pfaffian_extension.py`

## Question

The current determinant/native Gaussian surface does not generate a Majorana
coefficient. What is the smallest exact microscopic extension that can carry
the unique anomaly-fixed same-chirality Majorana operator?

## Bottom line

The smallest honest extension is an **antisymmetric Grassmann Gaussian**.

On that surface:

- the partition amplitude is a **Pfaffian**
- independent sectors multiply under `Pf(A_1 ⊕ A_2) = Pf(A_1) Pf(A_2)`
- the unique additive CPT-even scalar generator is therefore
  `W = log|Pf(A)|`
- the unique anomaly-fixed Majorana coefficient is the amplitude of the unique
  antisymmetric pairing block

So the exact next object beyond the determinant toolbox is not another fit.
It is a Pfaffian/Nambu microscopic sector.

## Inputs

This construction uses:

- the existing operator-classification result in
  [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md)
- the native-surface no-go in
  [NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md](./NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md)
- the finite-normal-grammar no-go in
  [NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md](./NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md)
- the atlas observable-principle logic on `main`

The classifier contributes one exact fact that matters here:

- there is exactly **one** anomaly-fixed same-chirality Majorana channel

That means a `Delta L = 2` microscopic extension should not introduce an
arbitrary family of independent coefficients. It should source one unique
antisymmetric channel.

## Exact statement

If the microscopic Grassmann Gaussian is extended from the number-conserving
determinant form to an antisymmetric pairing form

`Z[A] = Pf(A)`,

then:

1. `Pf(A)^2 = det(A)`
2. `Pf(A_1 ⊕ A_2) = Pf(A_1) Pf(A_2)`
3. by the same multiplicative-to-additive logic as the determinant lane, the
   unique additive CPT-even scalar generator is `log|Pf(A)|`

For a minimal unique-channel block

`A_M(mu) = (m_0 + mu) J_2`, with
`J_2 = [[0,1],[-1,0]]`,

the Pfaffian is

`Pf(A_M(mu)) = m_0 + mu`.

So the microscopic coefficient `mu` is a genuine exact source parameter on the
extended surface, not a phenomenological placeholder.

## What this closes

This closes the next mathematical step after the native-surface no-go:

- what exact beyond-determinant object could carry the unique Majorana
  coefficient?

Answer:

- a Pfaffian / antisymmetric Grassmann Gaussian on the unique channel

The new finite-normal-grammar no-go makes the reason cleaner: the missing
ingredient is not additional charge-zero interaction complexity inside the
retained grammar, but a genuine change of microscopic symmetry class.

That reduction target is now separated explicitly in:

- [NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md](./NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md)
- `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py`

So the Pfaffian construction should now be read as one admitted realization of
the missing charge-`2` primitive, not yet as the uniquely correct one.

The exact local-form companion is now:

- [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
- `scripts/frontier_neutrino_majorana_unique_source_slot.py`

That note says the local source completion, if admitted at bilinear level,
carries one complex slot `m`; the present Pfaffian note is one antisymmetric
Gaussian realization of that same slot.

The one-generation phase-removal companion is now:

- [NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md](./NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md)
- `scripts/frontier_neutrino_majorana_phase_removal.py`

Current result there: on the one-generation local block, the phase of `m` is
removable, so the retained CPT-even invariant is one real amplitude
`mu = |m|`.

The canonical local-block companion is now:

- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- `scripts/frontier_neutrino_majorana_canonical_local_block.py`

Current result there: every one-generation antisymmetric local realization is
equivalent to the canonical block `mu J_2`, so the Pfaffian extension carries
no residual local matrix freedom beyond the real amplitude `mu`.

## What this does not close

This note does **not** yet prove:

- that `Cl(3)` on `Z^3` forces such a Pfaffian/Nambu sector
- that the coefficient is nonzero in the full microscopic theory
- that the coefficient value is fixed
- that the three-generation neutrino texture is closed

So this is a precise construction step, not a closure claim.

That exact boundary question is now separated cleanly in:

- [NEUTRINO_MAJORANA_PFAFFIAN_AXIOM_BOUNDARY_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_AXIOM_BOUNDARY_NOTE.md)
- `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py`

Current result there: the Pfaffian/Nambu sector is still an admitted
extension, not yet a forced one.

## Safe wording

**Can claim**

- the exact operator classifier and the native-surface no-go together force the
  next honest microscopic object to be a unique-channel Pfaffian extension
- once such an antisymmetric Gaussian is admitted, `log|Pf|` is the exact
  additive CPT-even scalar generator on that surface

**Cannot claim**

- the framework already derives a nonzero Majorana mass
- the Pfaffian extension is already axiom-forced

## Command

```bash
python3 scripts/frontier_neutrino_majorana_pfaffian_extension.py
```
