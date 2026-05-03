# Wolfenstein Lambda and A Structural Identities Theorem

**Date:** 2026-04-24

**Status:** proposed_retained structural-identity subtheorem of the proposed_promoted CKM
atlas/axiom package. This note names and regression-tests the `lambda` and `A`
identities already present inside
`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`. It is a
companion to
`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`
and does not expand the parent CKM theorem's scope.

The first-row companion
`CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`
uses these same `lambda` and `A` identities to name
`|V_us|_0^2 = alpha_s(v)/2`, `|V_ub|_0^2 = alpha_s(v)^3/72`, and
`|V_ud|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3/72` on the atlas-leading
surface. The third-row companion
`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`
uses these same `lambda` and `A` identities to name
`|V_td|_0^2 = 5 alpha_s(v)^3/72` and
`|V_ts|_0^2 = alpha_s(v)^2/6` on the atlas-leading surface.

**Primary runner:** `scripts/frontier_wolfenstein_lambda_a_structural_identities.py`

## Statement

On the retained CKM atlas/axiom surface, let

```text
n_pair  = 2,
n_color = 3,
n_quark = n_pair n_color = 6.
```

Then the Wolfenstein parameters obey

```text
(W1)  lambda^2     = alpha_s(v) / n_pair  = alpha_s(v) / 2,
(W2)  A^2          = n_pair / n_color     = 2/3,
(W3)  A^2 lambda^2 = alpha_s(v) / n_color = alpha_s(v) / 3.
```

The first identity carries the separately retained canonical `alpha_s(v)`
input. The second is a pure rational group-counting identity. The third is the
product identity in which the weak-pair factor cancels exactly.

## Retained Inputs

| Input | Authority |
| --- | --- |
| Parent CKM atlas/axiom surface | `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` |
| `n_pair = 2` weak-pair structure | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md), parent CKM atlas |
| `n_color = 3` graph-first color structure | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md), parent CKM atlas |
| Canonical `alpha_s(v)` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| CKM CP radius and phase identities | `CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md` |

No observed CKM matrix element, quark mass, or fitted flavor observable enters
these identities.

## Derivation

The parent CKM atlas defines the Cabibbo-scale parameter from the canonical
coupling on the exact weak-pair split:

```text
lambda^2 = alpha_s(v) / n_pair.
```

With `n_pair = 2`,

```text
lambda^2 = alpha_s(v) / 2.
```

The same atlas defines the Wolfenstein `A` parameter from the exact weak-pair
to color-count ratio:

```text
A^2 = n_pair / n_color.
```

With `(n_pair, n_color) = (2, 3)`,

```text
A^2 = 2/3.
```

Multiplying the two identities gives

```text
A^2 lambda^2
  = (n_pair / n_color) (alpha_s(v) / n_pair)
  = alpha_s(v) / n_color
  = alpha_s(v) / 3.
```

The `n_pair` factor cancels exactly.

## CKM Magnitude Corollaries

The leading Wolfenstein forms on the parent atlas surface give

```text
|V_us|_0 = lambda,
|V_cb| = A lambda^2,
|V_ub|_0 = A lambda^3 sqrt(rho^2 + eta^2).
```

Using `(W1)` and `(W2)`,

```text
|V_us|_0 = sqrt(alpha_s(v)/2),
|V_cb| = sqrt(2/3) alpha_s(v)/2 = alpha_s(v)/sqrt(6).
```

Using the CP-phase subtheorem `rho^2 + eta^2 = 1/6`,

```text
|V_ub|_0 = sqrt(2/3) (alpha_s(v)/2)^(3/2) sqrt(1/6)
          = alpha_s(v)^(3/2) / (6 sqrt(2)).
```

The cleanest structural readout is therefore

```text
|V_cb| = alpha_s(v)/sqrt(n_quark) = alpha_s(v)/sqrt(6).
```

## Canonical Numerical Read

With the canonical plaquette/CMT value

```text
alpha_s(v) = 0.103303816122267...
```

the identities give

| Quantity | Structural expression | Canonical value |
| --- | --- | ---: |
| `lambda^2` | `alpha_s(v)/2` | `0.0516519080611` |
| `lambda` | `sqrt(alpha_s(v)/2)` | `0.227270561361` |
| `A^2` | `2/3` | `0.666666666667` |
| `A` | `sqrt(2/3)` | `0.816496580928` |
| `A^2 lambda^2` | `alpha_s(v)/3` | `0.0344346053741` |
| `|V_cb|` | `alpha_s(v)/sqrt(6)` | `0.0421736063303` |
| atlas-leading `|V_ub|_0` | `alpha_s(v)^(3/2)/(6 sqrt(2))` | `0.0039129860468` |

These are the same CKM magnitude values carried by the parent atlas package;
the first-row entries are atlas-leading values, with finite-`lambda`
standard-matrix readouts guarded by the first-row companion note.
Observation-facing comparison remains the parent atlas' downstream comparator,
not an input to this theorem.

## Joint Wolfenstein Surface

Together with the CKM CP-phase structural identity note, the named structural
surface is:

| Parameter | Structural identity | Authority |
| --- | --- | --- |
| `lambda^2` | `alpha_s(v)/2` | this note |
| `A^2` | `2/3` | this note |
| `rho` | `1/6` | CKM CP-phase structural identity |
| `eta` | `sqrt(5)/6` | CKM CP-phase structural identity |
| `rho^2 + eta^2` | `1/6` | CKM CP-phase structural identity |
| `cos^2(delta_CKM)` | `1/6` | CKM CP-phase structural identity |
| atlas `J_0` | `alpha_s(v)^3 sqrt(5)/72` | combined package |

This is an extraction of the parent CKM atlas identities into named,
regression-tested rows.

## Scope

This note claims:

- `lambda^2 = alpha_s(v)/2` on the retained CKM atlas surface;
- `A^2 = 2/3` as an exact counting identity;
- `A^2 lambda^2 = alpha_s(v)/3`;
- `|V_cb| = alpha_s(v)/sqrt(6)` and atlas-leading
  `|V_ub|_0 = alpha_s(v)^(3/2)/(6 sqrt(2))` as CKM atlas corollaries when
  paired with the CP-radius theorem.

This note does not claim:

- a new derivation of `alpha_s(v)`;
- independence from the parent CKM atlas/axiom surface;
- higher-order Wolfenstein corrections beyond the parent package;
- quark mass-ratio closure;
- BSM flavor or CP phases.

## Reproduction

```bash
python3 scripts/frontier_wolfenstein_lambda_a_structural_identities.py
```

Expected result:

```text
TOTAL: PASS=19, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` constants.

## Cross-References

- `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
  - parent CKM package.
- `CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`
  - companion `rho`, `eta`, phase, and `J` identities.
- `CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`
  - companion first-row atlas-leading magnitude identities.
- `CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`
  - companion third-row atlas-leading magnitude identities.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  - canonical `alpha_s(v)` input.
- `ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`
  - adjacent coupling-chain identity; plain-text pointer only, not a
    load-bearing authority for the Wolfenstein identities.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  - retained `n_color = 3` color structure.
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md)
  - retained weak-pair structure.
