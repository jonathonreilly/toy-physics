# Koide Weighted Character-Source Axis Theorem

**Date:** 2026-04-20  
**Status:** exact no-go sharpening on the charged-lepton observable-principle /
character-source route  
**Runner:** `scripts/frontier_koide_weighted_character_source_axis_theorem.py`

## Question

The old `Z_3` character-source cross-check already proved that the canonical
Plancherel kernel on the charged-lepton source triplet is exactly
`S = I_3`, so `Z_3` invariance alone does not select a mass ray.

That still left one honest loophole:

> perhaps the same canonical character sources become nontrivial once one
> allows general left/right `Z_3` class-function weights, rather than the
> uniform Plancherel choice.

Does that larger weighted source-kernel class contain a genuine Koide
selector?

## Bottom line

No.

Let the canonical character sources be

```text
s_i = e_{q_L(i)} \otimes e_{q_R(i)},
q_L = (0,1,2), q_R = (0,2,1),
```

with the three distinct charge pairs

```text
(q_L, q_R) = (0,0), (1,2), (2,1).
```

For arbitrary left/right central class-function weights

```text
M_L = sum_q mu_q e_q,
M_R = sum_q nu_q e_q,
```

the weighted kernel

```text
S_(mu,nu)(i,j) = Tr[(M_L \otimes M_R) s_i^dag s_j]
```

is exactly

```text
S_(mu,nu) = diag(mu_0 nu_0, mu_1 nu_2, mu_2 nu_1).
```

So the whole class stays diagonal in the canonical source basis.

That forces a clean dichotomy:

1. if the top eigenvalue is unique, the selected ray is one of the three basis
   axes, and every such axis has Koide `Q = 1`, not `2/3`;
2. if the top eigenvalue is degenerate, the kernel does not force a unique
   ray at all.

Therefore the weighted character-source class cannot furnish a unique Koide
selector.

## Input stack

This sharpens and extends:

1. [STRUCTURAL_NO_GO_SURVEY_NOTE.md](./STRUCTURAL_NO_GO_SURVEY_NOTE.md)
2. [CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](./CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
3. [KOIDE_POSITIVE_PATHS_FIRST_PRINCIPLES_NOTE_2026-04-18.md](./KOIDE_POSITIVE_PATHS_FIRST_PRINCIPLES_NOTE_2026-04-18.md)
4. [KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md)
5. [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)
6. [frontier_charged_lepton_z3_source_response_crosscheck.py](../scripts/frontier_charged_lepton_z3_source_response_crosscheck.py)

## Theorem 1: every weighted character-source kernel is diagonal

The `Z_3` character idempotents satisfy

```text
e_p e_q = delta_(pq) e_p,
Tr(e_q) = 1.
```

Hence for the canonical source elements

```text
s_i = e_{q_L(i)} \otimes e_{q_R(i)},
```

their products obey

```text
s_i^dag s_j = delta_(q_L(i), q_L(j)) delta_(q_R(i), q_R(j)) s_i.
```

Because the three charge pairs `(0,0), (1,2), (2,1)` are distinct, this
reduces to

```text
s_i^dag s_j = delta_(ij) s_i.
```

Now let

```text
M_L = sum_q mu_q e_q,
M_R = sum_q nu_q e_q
```

be arbitrary central left/right class-function weights. Since `M_L e_q = mu_q
e_q` and `M_R e_q = nu_q e_q`,

```text
(M_L \otimes M_R) s_i = mu_(q_L(i)) nu_(q_R(i)) s_i.
```

Therefore

```text
S_(mu,nu)(i,j)
  = Tr[(M_L \otimes M_R) s_i^dag s_j]
  = delta_(ij) mu_(q_L(i)) nu_(q_R(i)) Tr(s_i)
  = delta_(ij) mu_(q_L(i)) nu_(q_R(i)),
```

because `Tr(s_i) = Tr(e_(q_L(i))) Tr(e_(q_R(i))) = 1`.

With the canonical charge ordering this is exactly

```text
S_(mu,nu) = diag(mu_0 nu_0, mu_1 nu_2, mu_2 nu_1).
```

So the whole weighted class is diagonal, not circulant and not generic.

## Corollary 1: the canonical Plancherel kernel is just the uniform case

Setting

```text
mu_0 = mu_1 = mu_2 = 1,
nu_0 = nu_1 = nu_2 = 1
```

gives

```text
S_(mu,nu) = I_3,
```

which recovers the old no-go exactly.

So the earlier identity kernel was not an accident of one pairing convention.
It was the uniform member of a larger diagonal family.

## Corollary 2: a unique top eigenvalue selects a basis axis, not Koide

If one diagonal entry of `S_(mu,nu)` is strictly largest, then the principal
eigenvector is one of the three basis axes

```text
e_1 = (1,0,0), e_2 = (0,1,0), e_3 = (0,0,1).
```

For any basis axis,

```text
Q = (sum v_i^2) / (sum v_i)^2 = 1,
```

not `2/3`.

Equivalently, in the `C_3` Fourier decomposition,

```text
a_0^2 = 1/3,
2 |z|^2 = 2/3,
```

so the Koide cone condition `a_0^2 = 2 |z|^2` fails.

Thus whenever the weighted kernel does select a unique ray, that ray is
structurally the wrong one.

## Corollary 3: degenerate tops never force a unique ray

If the diagonal maximum is repeated, then the top eigenspace has dimension
`>= 2`. In that case the kernel leaves a family of rays unfixed.

So the degenerate branch does not rescue the route either: even if the top
eigenspace happens to contain Koide-admissible vectors, the kernel does not
single one out.

Hence the entire weighted character-source class fails in both possible ways:

- unique top: wrong ray,
- degenerate top: no unique ray.

## Scientific consequence

This closes a natural loophole in the charged-lepton first-principles attack
map.

The observable-principle / source-response route is **not** rescued by
reweighting the canonical `Z_3` character sources with arbitrary central
left/right class functions. That whole class remains too rigid: it can only
produce diagonal source kernels.

So the remaining live observable-principle seam is narrower than before:

- not "find a better weighted character-source pairing,"
- but "derive genuine off-axis circulant Fourier content of `D^(-1)` on the
  retained `hw=1` carrier, and then force the one scalar selector on that
  circulant data."

In the language of the existing scout notes, this means the surviving target is
still the same microscopic scalar on the cyclic Fourier coefficients of
`D^(-1)`:

```text
g_0^2 = 2 |g_1|^2
```

or equivalently the selected-line scalar `m` / `kappa`.

## Reproduction

```bash
PYTHONPATH=scripts python3 \
  scripts/frontier_koide_weighted_character_source_axis_theorem.py
```
