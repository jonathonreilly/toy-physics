# Rep-B Bare-Scale Independence Theorem for the Two-Ward `g_bare` Route

**Date:** 2026-04-19
**Type:** bounded_theorem
**Status authority:** independent audit lane only.
**Role:** bounded Rep-B independence step for the two-Ward `g_bare` route,
scoped to the retained narrow overlap authority rather than the terminal
top-Yukawa Ward-identification row.

---

## Theorem

Fix the retained `Cl(3) × Z^3` Wilson-plaquette + staggered-Dirac bare action
on the `Q_L = (2,3)` block, but do **not** preselect the canonical value
`g_bare = 1`.

Define the unique unit-normalized scalar-singlet composite operator on `Q_L`
by D17:

```
H_unit(x) = (1 / sqrt(N_c N_iso)) sum_{alpha,a} psibar_{alpha,a}(x) psi_{alpha,a}(x)
          = (1 / sqrt(6)) (psibar psi)_(1,1)(x)
```

Then the tree-level bare top-channel form factor

```
F_Htt^(0)(g_bare) := <0 | H_unit(0) | tbar_(top,up) t_(top,up)>_tree
```

is exactly

```
F_Htt^(0)(g_bare) = 1 / sqrt(6)
```

for **all** values of `g_bare`.

Equivalently, Rep B's bare Yukawa datum

```
y_t_bare^(0)(g_bare) = 1 / sqrt(6)
```

is genuinely independent of the preselected canonical surface.

---

## Proof

### 1. The narrow `H_unit` overlap authority is independent of `g_bare`

The retained narrow authority
[UNIT_SINGLET_OVERLAP_NARROW_THEOREM_NOTE_2026-05-02.md](UNIT_SINGLET_OVERLAP_NARROW_THEOREM_NOTE_2026-05-02.md)
states the unit-normalized scalar-singlet operator as

```
H_unit = (1 / sqrt(N_c N_iso)) sum_{alpha,a} psibar_{alpha,a} psi_{alpha,a}
```

and proves that its tree-level matrix element with any single basis pair is
`1 / sqrt(N_c N_iso)`, with no gauge-coupling parameter in the calculation.
This note consumes that narrow overlap identity only. It does not consume the
broader `YT_WARD_IDENTITY_DERIVATION_THEOREM.md` identification of the same
matrix element with the Standard Model top-Yukawa readout.

### 2. The top-channel overlap is pure group theory

The `(1,1)` singlet on `Q_L ⊗ Q_L*` is the uniform unit vector over the six
basis components. Therefore the overlap with any basis top-pair component is

```
<top-pair | S> = 1 / sqrt(N_c N_iso) = 1 / sqrt(6),
```

again independent of `g_bare`.

### 3. The tree-level matrix element has no gauge-coupling insertion

At tree order, the operator `H_unit` contains no gauge field and no explicit
coupling constant. The external top-pair state is evaluated in canonical
fermion normalization. So the only tree-order contribution to

```
<0 | H_unit | tbar t>_tree
```

is the local bilinear Wick contraction

```
<0 | psibar_(top,up) psi_(top,up) | tbar_(top,up) t_(top,up)>_tree = 1.
```

No gluon propagator, no gauge vertex, and no factor of `g_bare` can appear at
this order.

### 4. Combine the three ingredients

Multiplying the operator normalization from Step 1 by the group-theory overlap
from Step 2 and the unit Wick contraction from Step 3 gives

```
F_Htt^(0)(g_bare)
  = (1 / sqrt(6)) * 1
  = 1 / sqrt(6),
```

with no `g_bare` dependence.

This proves the theorem.

---

## Corollary

The candidate Rep-B datum used in the two-Ward route,

```
y_t_bare^(0) = 1 / sqrt(6),
```

is not a statement tied to the preselected canonical surface. It is a
tree-level bare-scale identity on the retained `Q_L` block itself.

The remaining Path-2 step is supplied separately by
`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`,
which upgrades the same-`Gamma^(4)` coefficient identity itself to an
off-surface theorem and then solves `g_bare = 1`.
