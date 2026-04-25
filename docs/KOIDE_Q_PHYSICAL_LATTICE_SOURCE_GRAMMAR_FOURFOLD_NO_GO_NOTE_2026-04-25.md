# Koide Q physical-lattice source-grammar fourfold audit

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_physical_lattice_source_grammar_fourfold_no_go.py`  
**Status:** conditional support; retained no-go; Q not closed

## Theorem attempt

Take the `Cl(3)` on `Z^3` lattice as physical and try to derive that the
undeformed microscopic charged-lepton lattice action has no native traceless
scalar source

```text
z Z,  Z = P_plus - P_perp.
```

If this were retained, the source-response coefficient would be read at the
undeformed source, the normalized two-channel carrier would have `z=0`, and
the conditional chain would give:

```text
z = 0 -> K_TL = 0 -> Q = 2/3.
```

## Four routes tested

The runner attacks the four live physical-lattice variants in parallel:

1. `Z` might not be a microscopic local lattice operator before reduction.
2. The bare physical lattice action might admit only common scalar `sI`.
3. `zZ` might be classified as probe/source deformation, not undeformed data.
4. Microscopic symmetry/locality might forbid the linear `Z` scalar term.

It also tests the inversion:

```text
the retained central/projected source grammar admits zZ.
```

## Conditional positive result

Strict onsite `C3`-invariant scalar locality is strong enough to remove `zZ`.
For an onsite scalar potential

```text
diag(a,b,c),
```

the equation

```text
C diag(a,b,c) C^-1 = diag(a,b,c)
```

forces

```text
a = b = c.
```

So, if the undeformed charged-lepton scalar source grammar is retained as
strictly onsite-only, the bare scalar action is only:

```text
s I.
```

That would close the dimensionless Q bridge modulo the already-retained
source-response theorem.

## Why this is not retained closure

The current retained Q source domain is broader than onsite diagonal scalar
potentials.  On the physical three-generation `C3` carrier,

```text
P_plus = (I + C + C^2)/3,
P_perp = I - P_plus,
Z = P_plus - P_perp
```

are retained central/projected source directions.  `Z` is `C3`-invariant and
satisfies:

```text
Z^2 = I.
```

Therefore a central source

```text
sI + zZ
```

preserves the retained `C3` symmetry.  The local `C3` polynomial source
exhaustion already showed the same obstruction:

```text
F(Z) = A_even I + A_odd Z.
```

Trace normalization removes `A_even`, but leaves `A_odd`, exactly the
traceless Q source.

The observable principle helps by classifying `J` as a probe deformation:

```text
D[J] = D + J,
W[J] = log |det(D+J)| - log |det D|.
```

The charged-lepton scalar observable is the coefficient at the undeformed
source.  But this does not prove the undeformed physical lattice action lacks a
native `zZ` background.  It says that if `zZ` is present, the undeformed
background is `D+zZ` and the source-response coefficient must be read there.

Finally, microscopic `C3` symmetry does not forbid the linear term:

```text
V(z) = ell*z + m*z^2.
```

For `m > 0`, this is convex and has the stationary point

```text
z* = -ell/(2m).
```

Zero follows only after adding `ell=0`, a `Z -> -Z` parity, a plus/perp mixer,
or an onsite-only source grammar.

## Countermodel

The conditional closing case is:

```text
z = 0 -> Q = 2/3, K_TL = 0.
```

The same retained central-source grammar admits:

```text
z = -1/3 -> Q = 1, K_TL = 3/8.
```

This countermodel is physical-lattice compatible at the retained
central/projected source level.

## Hostile review

- No Koide target is assumed.  The closing and counterclosing source
  backgrounds are compared under the same symbolic source algebra.
- No PDG masses, observational `H_*` pin, `delta=2/9`, or Brannen-phase input
  appears.
- The conditional onsite theorem is not promoted as retained closure.
- The missing theorem is named directly: the package would need to retain
  onsite-only undeformed charged-lepton scalar source grammar, or an equivalent
  law excluding central/projected `Z` as an undeformed source.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_onsite_only_undeformed_lattice_source_grammar_excluding_Z
RESIDUAL_SOURCE = physical_lattice_keeps_central_projected_Z_source_visible
COUNTERMODEL = physical_C3_lattice_with_central_source_z_minus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 -m py_compile scripts/frontier_koide_q_physical_lattice_source_grammar_fourfold_no_go.py
python3 scripts/frontier_koide_q_physical_lattice_source_grammar_fourfold_no_go.py
```

Expected result:

```text
KOIDE_Q_PHYSICAL_LATTICE_SOURCE_GRAMMAR_FOURFOLD_NO_GO=TRUE
Q_PHYSICAL_LATTICE_SOURCE_GRAMMAR_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_ONSITE_ONLY_UNDEFORMED_LATTICE_SOURCE_GRAMMAR=TRUE
RESIDUAL_SCALAR=derive_retained_onsite_only_undeformed_lattice_source_grammar_excluding_Z
```
