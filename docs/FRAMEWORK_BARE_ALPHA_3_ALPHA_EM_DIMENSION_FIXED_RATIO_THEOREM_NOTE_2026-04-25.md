# Framework Bare α_3/α_em Dimension-Fixed Ratio Theorem

**Date:** 2026-04-25

**Status:** Retained derivation theorem on `main`. **Pushes the framework
forward** by deriving a NEW dimension-specific cross-sector identity
binding the **color** and **electroweak** sectors at the framework's
bare lattice scale into a single integer ratio:

```text
alpha_3(bare) / alpha_em(bare)  =  2d + 3.
```

For the framework's retained spatial dimension `d = 3`, this yields
the **integer prediction**

```text
alpha_3(bare) / alpha_em(bare)  =  9.
```

The identity binds three independent retained inputs from two
sectors:

1. **Color sector** (Cl(3) clock-shift axiom): `g_3^2(bare) = 1`
2. **Weak sector** (Z_2 bipartite, d-spatial): `g_2^2(bare) = 1/(d+1) = 1/4`
3. **Hypercharge sector** (chirality): `g_Y^2(bare) = 1/(d+2) = 1/5`

These give the bare-scale electroweak structure:

```text
(D1)  1/g_2^2 + 1/g_Y^2  =  (d+1) + (d+2)  =  2d + 3  =  9       [d=3]
(D2)  alpha_em(bare)      =  1/((2d+3) × 4 pi)  =  1/(36 pi)     [d=3]
(D3)  sin^2(theta_W)(bare) =  (d+1)/(2d+3)      =  4/9            [d=3]
(D3a) cos^2(theta_W)(bare) =  (d+2)/(2d+3)      =  5/9            [d=3]
(D4)  alpha_3(bare) / alpha_em(bare)  =  g_3^2 (2d+3)  =  9       [d=3]
```

**Dimension uniqueness:** the integer ratio `2d + 3` is dimension-specific.
Other dimensions would give different integers:

```text
d = 2  ->  alpha_3/alpha_em = 7
d = 3  ->  alpha_3/alpha_em = 9     [framework value]
d = 4  ->  alpha_3/alpha_em = 11
d = 5  ->  alpha_3/alpha_em = 13
```

The framework's specific `d = 3` is encoded in the integer 9. Any
running calculation that connects bare to observed must respect this
boundary condition.

**Comparison to standard SU(5) GUT:**

```text
SU(5) GUT prediction:        sin^2(theta_W)(M_GUT)  =  3/8  =  0.375
Framework bare prediction:   sin^2(theta_W)(bare)   =  4/9  =  0.444
                                                     DIFFERENT
```

The framework is **NOT** SU(5) at the bare lattice scale. The
specific value `4/9` arises from the d=3 lattice's `(d+1, d+2)
direction count`, which is structurally distinct from SU(5)'s
hypercharge embedding.

**Primary runner:**
`scripts/frontier_framework_bare_alpha_3_alpha_em_dimension_fixed_ratio.py`

## Statement

In the framework's d=3 spatial lattice, the bare gauge couplings at
the lattice scale satisfy:

```text
g_3^2(bare)  =  1                 [Cl(3) clock-shift axiom]
g_2^2(bare)  =  1/(d+1)  =  1/4   [Z_2 bipartite, weak sector]
g_Y^2(bare)  =  1/(d+2)  =  1/5   [chirality sector]
```

These give the following structural identities at the bare scale:

```text
(D1)  1/g_2^2 + 1/g_Y^2  =  2d + 3  =  9        (sum rule)
(D2)  g_2^2 g_Y^2/(g_2^2 + g_Y^2)
       =  1/(2d+3)  =  1/9                       (effective EM coupling)
(D3)  sin^2(theta_W)(bare)
       =  g_Y^2/(g_2^2 + g_Y^2)  =  (d+1)/(2d+3)  =  4/9
(D4)  alpha_3(bare) / alpha_em(bare)
       =  g_3^2 (1/g_2^2 + 1/g_Y^2)  =  g_3^2 (2d+3)  =  9
(D5)  alpha_em(bare)  =  1/(36 pi)  =  1/((2d+3) × 4 pi)
                      ≈  1/113.10
(D6)  1/alpha_3(bare) + 1/alpha_2(bare) + 1/alpha_Y(bare)
       =  4 pi (1 + (d+1) + (d+2))
       =  4 pi (2d + 4)
       =  40 pi  ≈  125.66                       [d = 3]
```

Identities `(D1)-(D6)` are NEW packaged structural predictions of
the framework's bare gauge structure.

## Retained Inputs

| Input | Authority |
| --- | --- |
| `g_3^2(bare) = 1` (Cl(3) axiom) | [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md), [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_2^2(bare) = 1/(d+1) = 1/4` | [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md), [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| `g_Y^2(bare) = 1/(d+2) = 1/5` | [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md), [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| Spatial dimension `d = 3` | [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md), Cl(3) framework axiom |

No PDG observable is used as a derivation input. Comparators with
PDG `alpha_s(M_Z)` and `alpha_em(M_Z)` below are post-derivation
consistency checks on the framework's running pipeline.

## Derivation

The bare gauge couplings give the following at the lattice scale:

### `(D1)`: Sum rule `1/g_2^2 + 1/g_Y^2 = 2d + 3`

```text
1/g_2^2 + 1/g_Y^2  =  (d+1) + (d+2)  =  2d + 3.
```

For `d = 3`: `1/g_2^2 + 1/g_Y^2 = 4 + 5 = 9`.

### `(D2)`: Effective bare EM coupling-squared

```text
g_em^2(bare)  =  g_2^2 g_Y^2 / (g_2^2 + g_Y^2)
              =  1/((d+1)(d+2)) / (1/(d+1) + 1/(d+2))
              =  1/((d+1)(d+2)) × (d+1)(d+2)/((d+1)+(d+2))
              =  1/(2d + 3).
```

For `d = 3`: `g_em^2(bare) = 1/9`.

### `(D3)`: Bare Weinberg angle

```text
sin^2(theta_W)(bare)  =  g_Y^2 / (g_2^2 + g_Y^2)
                       =  1/(d+2) / (1/(d+1) + 1/(d+2))
                       =  1/(d+2) × (d+1)(d+2)/((2d+3))
                       =  (d+1) / (2d+3).
```

For `d = 3`: `sin^2(theta_W)(bare) = 4/9`. Equivalently
`cos^2(theta_W)(bare) = 5/9`.

### `(D4)`: NEW α_3(bare)/α_em(bare) identity

```text
alpha_3(bare) / alpha_em(bare)
   =  (g_3^2 / 4 pi) / (g_em^2 / 4 pi)
   =  g_3^2 / g_em^2
   =  g_3^2 (g_2^2 + g_Y^2) / (g_2^2 g_Y^2)
   =  g_3^2 (1/g_2^2 + 1/g_Y^2)
   =  g_3^2 (2d + 3)
   =  1 × (2d + 3)         [Cl(3) axiom]
   =  2d + 3
   =  9                    [d = 3].
```

This is the **new dimension-specific cross-sector identity**. The
factor `2d + 3` is an integer at integer `d`, and only `d = 3` gives
the framework's value `9`.

### `(D5)`: Bare α_em closed form

```text
alpha_em(bare)  =  g_em^2(bare) / (4 pi)  =  1/((2d+3) × 4 pi)  =  1/(36 pi).
```

Numerically `~ 1/113.10`.

### `(D6)`: Sum of inverse fine-structure constants

```text
1/alpha_3 + 1/alpha_2 + 1/alpha_Y
   =  4 pi/g_3^2 + 4 pi/g_2^2 + 4 pi/g_Y^2
   =  4 pi (1 + (d+1) + (d+2))
   =  4 pi (2d + 4)
   =  40 pi          [d = 3]
   ≈  125.66.
```

## Numerical Predictions

| Quantity | Closed form | Framework (d=3) | PDG comparator |
| --- | --- | ---: | ---: |
| `g_2^2(bare)` | `1/(d+1)` | `1/4 = 0.250` | -- |
| `g_Y^2(bare)` | `1/(d+2)` | `1/5 = 0.200` | -- |
| `g_3^2(bare)` | (axiom) | `1.0` | -- |
| `1/g_2^2 + 1/g_Y^2` | `2d+3` | `9` (integer) | -- |
| `sin^2(theta_W)(bare)` | `(d+1)/(2d+3)` | `4/9 = 0.4444` | (running to MZ) |
| `cos^2(theta_W)(bare)` | `(d+2)/(2d+3)` | `5/9 = 0.5556` | -- |
| `alpha_em(bare)` | `1/((2d+3) 4 pi)` | `1/113.1` | -- |
| `alpha_3(bare)/alpha_em(bare)` | `2d+3` | `9` (integer) | (running comparator) |

PDG running-pipeline check at v scale and M_Z:

```text
alpha_s(v)        =  0.10330  (canonical CMT/plaquette)
alpha_em(v)       ~  1/127.5  (PDG approximate)
ratio(v)          =  13.17

alpha_s(M_Z)      =  0.1181
alpha_em(M_Z)     =  1/127.95
ratio(M_Z)        =  15.11
```

The framework's bare ratio `9` runs UP to `~13` at v scale and
`~15` at M_Z. The increase is consistent with standard SM running
(α_3 grows faster at low energy due to QCD asymptotic freedom +
larger β_3 coefficient than β_em).

## Why This Pushes the Framework Forward

The bare gauge couplings `g_3^2 = 1`, `g_2^2 = 1/4`, `g_Y^2 = 1/5`
have been retained for some time in the framework, derived from the
Cl(3) lattice geometry. What is **new** here:

1. **Dimension-specific cross-sector identity** `(D4)`: the ratio
   `alpha_3(bare)/alpha_em(bare) = 2d + 3 = 9` at d=3 binds the
   color and electroweak sectors into a single integer test of the
   framework's spatial dimension.

2. **Framework distinction from SU(5)**: the bare `sin^2(theta_W) =
   4/9` is structurally distinct from the SU(5) GUT prediction
   `3/8`. The framework is **not** SU(5) at the bare lattice scale.
   This is a NEW negative-claim packaging that sharpens the
   framework's identity.

3. **Sum rule** `(D1)`: `1/g_2^2 + 1/g_Y^2 = 2d + 3 = 9` at d=3, a
   clean integer prediction following from the framework's specific
   `(d+1, d+2)` direction-count structure.

4. **Bare α_em closed form** `(D5)`: `1/(36 pi)`, derived directly
   from the bare gauge structure.

5. **Inverse fine-structure sum** `(D6)`: `1/alpha_3 + 1/alpha_2 +
   1/alpha_Y = 40 pi` at d=3, a sum rule binding all three SM gauge
   couplings at the bare scale.

These identities provide **quantitative falsification targets** for
the framework's specific `d = 3` lattice and `(d+1, d+2)` weak +
hypercharge direction count. A future framework alternative with
different spatial dimensions or different direction counts would
predict different integer ratios.

In standard SM phenomenology, the bare-scale gauge structure is not
fixed by any axiomatic principle -- the couplings are running
parameters with arbitrary boundary conditions at high scale. The
framework's d=3 lattice fixes these as exact rational functions of
d, providing a distinctly **non-arbitrary** bare structure.

## Falsification

The bare-scale identities `(D1)-(D6)` are not directly testable
because the lattice scale is around `M_Pl`, where direct measurement
is impossible. Falsification proceeds through the running pipeline:

1. **Bare `(D4)`** says `alpha_3/alpha_em = 9`.
2. **Standard SM running** takes this to a specific value at lower
   scales.
3. **PDG observed** at M_Z: `alpha_s(M_Z)/alpha_em(M_Z) = 15.1`.

The increase from 9 (bare) to 15 (M_Z) is structurally consistent
with SM running. A precise framework calculation of the running
should reproduce 15.1 at M_Z. Any non-trivial discrepancy would
falsify the framework's bare boundary condition or the running
pipeline.

The framework's specific `2d + 3 = 9` at d=3 is also testable in
principle: if a future analysis computes the bare ratio from a
different starting point and obtains a value other than 9, the
framework's d=3 axiom would be falsified.

## What This Claims

- `1/g_2^2(bare) + 1/g_Y^2(bare) = 2d + 3 = 9` at d=3.
- `sin^2(theta_W)(bare) = (d+1)/(2d+3) = 4/9` at d=3.
- `alpha_em(bare) = 1/((2d+3) × 4 pi) = 1/(36 pi)` at d=3.
- `alpha_3(bare)/alpha_em(bare) = 2d + 3 = 9` at d=3 (NEW
  cross-sector identity).
- Framework's bare structure is **distinct from SU(5) GUT**:
  framework gives `4/9` vs SU(5) `3/8` for sin^2(theta_W).
- The integer `9` uniquely identifies `d = 3`; other dimensions give
  different integer ratios.

## What This Does Not Claim

- It does not derive `g_3^2(bare) = 1` (that is an Cl(3)
  clock-shift axiom).
- It does not derive the spatial dimension `d = 3` (that is a
  framework axiom).
- It does not promote the bare predictions to direct observable
  predictions; the running pipeline is required for quantitative
  comparison with PDG.
- It does not modify the parent CL3_SM_EMBEDDING_THEOREM,
  YT_EW_COLOR_PROJECTION_THEOREM, or related notes.
- It does not promote any GUT-style unification at a specific scale
  M_GUT; the framework's bare structure is at the lattice cutoff,
  not at a GUT scale.

## Reproduction

```bash
python3 scripts/frontier_framework_bare_alpha_3_alpha_em_dimension_fixed_ratio.py
```

Expected result:

```text
TOTAL: PASS=31, FAIL=0
```

The runner uses the Python standard library only.

## Cross-References

- [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
  -- retained Cl(3) embedding with bare couplings.
- [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
  -- retained `g_2^2 = 1/(d+1) = 1/4` and `g_Y^2 = 1/(d+2) = 1/5`.
- [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)
  -- retained spatial dimension `d = 3` axiom.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  -- retained hypercharge uniqueness, complementary to bare g_Y^2.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` from plaquette/CMT.
