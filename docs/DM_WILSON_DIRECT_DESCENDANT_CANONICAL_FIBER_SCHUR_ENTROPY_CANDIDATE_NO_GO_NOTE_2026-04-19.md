# DM Wilson Direct-Descendant Canonical-Fiber Schur-Entropy Candidate / No-Go

**Date:** 2026-04-19  
**Status:** exact follow-on note on the DM source-fiber lane. The new
canonical transport-column theorem reduces the live object to the
orbit-level source fiber over the canonical favored column. On that fiber,
the plateau slogan

```text
choose the most isotropic normalized Schur spectrum
```

does **not** extend canonically. Standard coefficient-free normalized
Schur-spectral laws disagree on exact positive-fiber points. If one adds one
extra axiom selecting Shannon entropy, that does produce an explicit endpoint
candidate on the canonical fiber, but the resulting aligned-seed -> endpoint
exact crossing leaves the constructive chamber. So the physical selector is
still open.

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_canonical_fiber_schur_entropy_candidate_no_go_2026_04_19.py`

**Follow-on same-day sharpening:**  
`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_FIBER_MIXED_SPECTRAL_BRANCH_WEIGHT_NO_GO_NOTE_2026-04-19.md`
shows that even after adding the exact local branch scalar `log Delta_src`,
the resulting mixed family still carries one free weighting coefficient.

## Question

After the canonical transport-column fiber theorem, the cleanest next positive
idea was:

1. keep the canonical favored-column orbit fixed;
2. look only at local Schur-side data on that fiber;
3. choose the source with the "most isotropic" normalized Schur spectrum.

That would be ideal if true, because it would be:

- source-visible,
- coefficient-free,
- local to `L_e / H_e`,
- and strong enough to collapse the residual `3`-real fiber.

Does that slogan actually define a unique law on the full canonical fiber?

## Bottom line

No, not by itself.

On the orbit-level canonical fiber, the normalized Schur spectra are no longer
totally ordered by majorization. The runner certifies two exact positive-fiber
points:

- a **Shannon point** `S_H`,
- and a **Renyi-2 / participation point** `S_R`,

both satisfying the exact canonical orbit constraints and the retained
positive-branch conditions

```text
gamma > 0, E1 > 0, E2 > 0, Delta_src > 0.
```

But the two laws rank them oppositely:

- Shannon entropy prefers `S_H`,
- Renyi-2 entropy and participation ratio prefer `S_R`.

Their normalized spectra are majorization-incomparable, so there is no
law-independent notion of "most isotropic spectrum" on the full fiber.

That is the no-go.

There is also one honest conditional positive result:

- if one adds the extra axiom that the normalized spectral law must be the
  unique continuous symmetric additive entropy, then Shannon is selected;
- that picks an explicit canonical-fiber endpoint candidate `S_H`.

But even then the source problem is not closed physically, because the unique
exact `eta_1 = 1` crossing on the aligned-seed -> `S_H` segment already has
`E1 < 0`, so it leaves the constructive chamber.

So the remaining gap is sharper again:

> generic Schur-spectral isotropy is insufficient, and even the
> entropy-additivity refinement does not yet produce the physical source.

## Setup: the orbit-level canonical fiber

The canonical favored-column theorem fixed the transport object to the unique
orbit represented by

```text
col_* = (0.0356443..., 0.0356443..., 0.9287114...)
```

up to flavor permutation.

At orbit level, this is equivalent to fixing the two permutation-invariant
moments

```text
p2 := sum_i c_i^2 = 0.865045882813...
p3 := sum_i c_i^3 = 0.801108643385...
```

together with `sum_i c_i = 1`.

So the orbit-level canonical source fiber is the set of direct-descendant
sources on the fixed native `N_e` seed surface with those exact moment values.

The follow-on question is then:

> what local Schur-side scalar law selects a point on that fiber?

## Theorem 1: plateau spectral isotropy does not extend canonically

On the certified plateau witness set `W0..W3`, the earlier same-day plateau
note proved a clean majorization statement, so all strictly Schur-concave
symmetric normalized spectral laws agreed there and selected `W1`.

That agreement does **not** survive promotion to the full canonical fiber.

The runner constructs two exact positive-fiber points:

### Shannon point `S_H`

Direct-descendant source in source-5 coordinates:

```text
S_H = (0.68897954, 0.63297204, 0.11110204, 0.23146031, 1.43769822)
```

with normalized Schur spectrum

```text
p_H = (0.63244590, 0.32076736, 0.04678674)
```

and projected-source pack

```text
(gamma, E1, E2, Delta_src)
= (0.39432401, 0.00143109, 0.00184739, 0.02661580).
```

### Renyi-2 / participation point `S_R`

Direct-descendant source in source-5 coordinates:

```text
S_R = (0.81041468, 0.64850569, 0.07186022, 0.58457279, 2.88995859)
```

with normalized Schur spectrum

```text
p_R = (0.51180785, 0.47455234, 0.01363981)
```

and projected-source pack

```text
(gamma, E1, E2, Delta_src)
= (0.05318324, 0.44644652, 0.00414285, 0.01226713).
```

Both lie on the exact same canonical orbit-level fiber and both satisfy

```text
gamma > 0, E1 > 0, E2 > 0, Delta_src > 0.
```

But their scalar orderings disagree:

```text
H(p_H)  > H(p_R)
R2(p_R) > R2(p_H)
PR(p_R) > PR(p_H).
```

Since `p_H` and `p_R` are majorization-incomparable, that disagreement is not
accidental. It is exactly what one expects once the total-order property from
the finite plateau witness set is lost.

### Consequence

The statement

```text
choose the most isotropic normalized Schur spectrum
```

is **not** a theorem-grade law on the full canonical fiber. It becomes a law
only after one supplies an extra axiom specifying which spectral isotropy
functional is physical.

## Theorem 2: the plateau-selected witness `W1` is not the full-fiber answer

The runner also checks that both `S_H` and `S_R` beat the earlier plateau
witness `W1` in their respective laws:

- `H(S_H) > H(W1)`,
- `R2(S_R) > R2(W1)`.

So the plateau selector does not simply transplant unchanged to the full
canonical fiber.

That matters because it closes a tempting but false shortcut:

> prove something on the four certified plateau witnesses, then treat that as
> the law on the whole fiber.

The new theorem shows that extension step is exactly where the difficulty
returns.

## Conditional candidate: entropy additivity singles out Shannon

There is one clean extra axiom that does pick a specific spectral law.

If one requires the normalized spectral law to be:

- continuous,
- permutation-symmetric,
- scale-free after normalization,
- and additive in the entropy sense on independent positive spectral factors,

then Shannon entropy is the unique law in that class up to an overall scale.

Under that extra axiom, the branch gets a concrete source-fiber endpoint
candidate:

> choose `S_H`, the maximizer of normalized Schur spectral Shannon entropy on
> the positive canonical orbit-level fiber.

That is a real scientific sharpening, because it identifies exactly what extra
axiom would be load-bearing if one wanted a single scalar law here.

## Why this still does not close the physical selector

Even the Shannon endpoint is not enough to finish.

The aligned-seed -> `S_H` affine segment still has a unique exact
`eta_1 = 1` crossing, but the runner certifies that the crossing pack is

```text
(eta_1, gamma, E1, E2, Delta_src)
= (1.0, 0.34109295..., -0.01679389..., 0.03008909..., 0.02972000...)
```

So the crossing leaves the constructive chamber because `E1 < 0`.

That means:

- the entropy-additivity axiom would select an explicit endpoint candidate,
- but it still would **not** supply the physical point required by the older
  constructive/positive route.

## What this closes

- the vague hope that the full canonical fiber is already canonically ordered
  by generic normalized Schur-spectral isotropy;
- the shortcut from the certified plateau witness set to the whole canonical
  fiber;
- the idea that "most isotropic spectrum" is already a theorem-grade law
  without specifying the isotropy functional.

## What this does not close

- a retained derivation of the entropy-additivity axiom from `Cl(3)` on `Z^3`;
- a theorem that the Shannon endpoint is the physical direct-descendant source;
- the constructive physical selector on the DM source-fiber lane.

## Exact remaining gap

The remaining law must be stronger than:

- generic normalized Schur-spectral isotropy,
- and stronger than plateau-only spectral isotropy.

It must at least:

1. specify the microscopic scalar itself, not just the slogan "isotropy";
2. be compatible with the direct-descendant canonical orbit-level fiber;
3. connect back to the constructive physical route rather than sending the
   exact crossing out of the chamber.

That is the sharpest honest post-fiber statement now available.

## Cross-references

- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_SCHUR_SPECTRAL_ISOTROPY_SELECTOR_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_canonical_fiber_schur_entropy_candidate_no_go_2026_04_19.py
```

Expected:

- exact positive-fiber Shannon point `S_H`;
- exact positive-fiber Renyi-2 / participation point `S_R`;
- opposite Shannon / Renyi-2 ordering;
- majorization incomparability of `p_H` and `p_R`;
- unique aligned-seed -> `S_H` exact crossing with `E1 < 0`;
- `PASS` with `FAIL=0`.
