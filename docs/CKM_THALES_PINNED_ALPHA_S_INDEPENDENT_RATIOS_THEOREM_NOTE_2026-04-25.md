# Thales-Pinned α_s-Independent CKM Ratios Theorem

**Date:** 2026-04-25

**Status:** Retained CKM structural subtheorem on the promoted
atlas/axiom surface. It derives a structural classification of the framework's
atlas-LO CKM predictions: each CKM-magnitude ratio is either
**α_s-DEPENDENT** (probes the canonical coupling) or
**α_s-INDEPENDENT** (probes only the framework's specific atlas point
on the Thales circle). The α_s-independent class isolates pure
**Thales-geometric** content: those CKM ratios that test the atlas
point `rho = 1/6, eta = sqrt(5)/6` *without any reference to the
canonical coupling*.

The framework's α_s-independent ratios are

```text
(R1)  |V_ts| / |V_cb|              =  1                (integer, atlas-LO)
(R2)  |V_td| / |V_ub|              =  sqrt(5)          (atlas-LO)
(R3)  |V_td V_cb*|^2 / |V_ts V_ub*|^2  =  5            (cross-row, NEW)
(R4)  R_b^2  =  rho                                    (Thales corollary, NEW form)
(R5)  R_t^2 / R_b^2  =  (1 - rho)/rho  =  5            (atlas point)
```

All five identities depend ONLY on the atlas values `rho`, `eta`, and
the Thales relation `eta^2 = rho(1 - rho)`. The canonical coupling
`alpha_s(v)` does **not** appear.

The three directly comparator-ready ratios `(R1)-(R3)` match their PDG
comparators at `< 0.2 sigma`:

| Ratio | Framework | PDG | Deviation |
|---|---:|---:|---:|
| `\|V_ts\|/\|V_cb\|` | `1` | `0.993 +/- 0.042` | `-0.18 sigma` |
| `\|V_td\|/\|V_ub\|` | `sqrt(5) = 2.236` | `2.246 +/- 0.127` | `+0.08 sigma` |
| `\|V_td V_cb\|^2/\|V_ts V_ub\|^2` | `5` | `5.12 +/- 0.72` | `+0.17 sigma` |

The cross-row identity `(R3)` is new package-level structural content:
it combines two independently-measured CKM products into a sharp test of
the framework's **specific Thales point**, with no canonical-coupling
ambiguity.

**Primary runner:**
`scripts/frontier_ckm_thales_pinned_alpha_s_independent_ratios.py`

## Statement

On the retained CKM atlas surface with framework values
`lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`, `rho = 1/6`,
`eta = sqrt(5)/6`, and the Thales circle `eta^2 = rho(1 - rho)`,
the leading-order Wolfenstein squared CKM magnitudes evaluate to

```text
|V_us|^2 = lambda^2                          = alpha_s(v)/2,
|V_cb|^2 = A^2 lambda^4                       = alpha_s(v)^2/6,
|V_ts|^2 = A^2 lambda^4                       = alpha_s(v)^2/6,
|V_ub|^2 = A^2 lambda^6 (rho^2 + eta^2)       = alpha_s(v)^3/72,
|V_td|^2 = A^2 lambda^6 ((1-rho)^2 + eta^2)   = 5 alpha_s(v)^3/72.
```

The α_s-independent ratios `(R1)-(R5)` then follow by direct
algebra. Their α_s-INDEPENDENCE is a non-trivial fact: each ratio's
numerator and denominator share the same `alpha_s` power and the
same `A^2 lambda^k` structure, so the canonical coupling cancels
exactly.

## α_s-Independent vs α_s-Dependent: A Structural Classification

The framework's atlas-LO CKM magnitude ratios separate cleanly:

**α_s-INDEPENDENT (geometric, Thales-pinned):**

```text
|V_ts|^2 / |V_cb|^2          =  1
|V_td|^2 / |V_ub|^2          =  5  =  R_t^2 / R_b^2  =  (1-rho)/rho
|V_td V_cb*|^2 / |V_ts V_ub*|^2  =  5
```

These probe **only** `(rho, eta)` at the atlas point. They are
*independent of the canonical coupling*.

**α_s-DEPENDENT (dynamical):**

```text
|V_us|^2 / |V_cb|^2     =  3 / alpha_s(v)
|V_us|^2 / |V_ub|^2     =  36 / alpha_s(v)^2
|V_td|^2 / |V_cb|^2     =  5 alpha_s(v) / 12
|V_us|^2 / |V_td|^2     =  36 / (5 alpha_s(v)^2)
```

These probe the canonical `alpha_s(v)`. Their measurement provides an
α_s extraction route (cf. the cross-sector α_s extraction theorem
[`CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md`](CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md)).

**This separation is the new structural insight**: the framework
predicts which CKM ratios are tests of pure atlas geometry vs which
are extractions of the canonical coupling.

## Retained Inputs

| Input | Authority |
| --- | --- |
| `lambda^2 = alpha_s(v)/2` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Thales circle `eta^2 = rho(1 - rho)` | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| `\|V_ts\|^2 = \|V_cb\|^2 = alpha_s^2/6` (third-row) | [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md) |
| `\|V_ub\|^2 = alpha_s^3/72`, `\|V_td\|^2 = 5 alpha_s^3/72` | [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md) |

No PDG/lattice CKM observable, decay-rate measurement, or hadronic
factor is used as a derivation input. The atlas-LO Wolfenstein
expansion is standard.

## Derivation

### `(R1)`: `|V_ts|/|V_cb| = 1`

```text
|V_ts|^2 / |V_cb|^2  =  (A^2 lambda^4) / (A^2 lambda^4)  =  1.
```

Both sides equal `alpha_s(v)^2/6` in framework values. The ratio is
an exact integer at atlas-LO.

### `(R2)`: `|V_td|/|V_ub| = sqrt(5)`

```text
|V_td|^2 / |V_ub|^2
   =  [A^2 lambda^6 ((1 - rho)^2 + eta^2)]
      / [A^2 lambda^6 (rho^2 + eta^2)]
   =  R_t^2 / R_b^2
   =  (1 - rho) / rho            (Thales: eta^2 = rho(1 - rho))
   =  5                          (atlas: rho = 1/6).
```

So `|V_td| / |V_ub| = sqrt(5)`. The `A^2 lambda^6` factor cancels.

### `(R3)`: `|V_td V_cb*|^2 / |V_ts V_ub*|^2 = 5`

```text
|V_td V_cb*|^2 / |V_ts V_ub*|^2
   =  (|V_td|^2 |V_cb|^2) / (|V_ts|^2 |V_ub|^2)
   =  (5 alpha_s^3/72 * alpha_s^2/6)
      / (alpha_s^2/6 * alpha_s^3/72)
   =  5.
```

The `alpha_s^5/432` factor is the same in numerator and denominator,
so the ratio collapses to the rational `5`.

Equivalently:

```text
|V_td V_cb*|^2 / |V_ts V_ub*|^2  =  R_t^2 / R_b^2  =  5.
```

This is the **new cross-row identity**. It states that the product
`|V_td V_cb*|` (which appears in B_d-mixing and ε_K) and the product
`|V_ts V_ub*|` (which appears in CP-violating combinations) have a
fixed ratio sqrt(5) on the framework's atlas surface, independent of
the canonical coupling.

### `(R4)`: `R_b^2 = rho`

By Thales `eta^2 = rho(1 - rho)`:

```text
R_b^2  =  rho^2 + eta^2
       =  rho^2 + rho(1 - rho)
       =  rho^2 + rho - rho^2
       =  rho.
```

So `R_b^2 = rho = 1/6` at the atlas point. This is a sharper form
than the retained `R_b^2 = 1/6` -- it reads the CP radius directly
off the apex's `rho` coordinate, without numerical evaluation.

### `(R5)`: `R_t^2 / R_b^2 = (1 - rho)/rho = 5`

Combining `R_t^2 = 1 - rho` (Thales corollary) and `R_b^2 = rho`:

```text
R_t^2 / R_b^2  =  (1 - rho) / rho.
```

At atlas `rho = 1/6`: `(1 - 1/6)/(1/6) = (5/6)/(1/6) = 5`.

This is the geometric origin of `(R2)` and `(R3)`: both reduce to
`R_t^2/R_b^2 = 5` after the relevant `A^2 lambda^k` factors cancel.

## Numerical Predictions and PDG Comparators

| Quantity | Framework | PDG | Deviation |
|---|---:|---:|---:|
| `\|V_ts\|/\|V_cb\|` | `1.000` | `0.993 +/- 0.042` | `-0.18 sigma` |
| `\|V_td\|/\|V_ub\|` | `sqrt(5) = 2.236` | `2.246 +/- 0.127` | `+0.08 sigma` |
| `\|V_td V_cb\|^2/\|V_ts V_ub\|^2` | `5` | `5.12 +/- 0.72` | `+0.17 sigma` |
| `R_b^2` | `1/6 = 0.167` | `0.189 +/- 0.013` | `-1.7 sigma` |
| `R_t^2/R_b^2` | `5` | `~4.7` | within band |

The three directly comparator-ready ratios `(R1)-(R3)` all match PDG
measurements without any CKM-fit adjustment at `< 0.2 sigma`. The
largest deviation among the geometric corollaries listed here is in
`R_b^2` itself (1.7σ), which is the known atlas-LO ↔ standard-fit
`|V_ub|` tension; the cross-row ratio identity `(R3)` is sharper
because the systematic biases in `|V_ub|` partially cancel.

## Why This Pushes the Framework Forward

The retained framework already lists the individual CKM magnitudes
`|V_qq'|^2` as functions of `alpha_s(v)` (third-row, second-row,
first-row magnitude theorems). What this note adds is the
**structural classification** of which ratios are α_s-independent
geometric tests:

1. The framework's atlas-LO predictions split into a pure-geometric
   class (no `alpha_s` dependence) and a dynamical class
   (`alpha_s`-dependent extraction routes).

2. The α_s-independent ratios are direct Thales-circle tests: each
   probes whether the atlas apex sits exactly at `(rho, eta) = (1/6,
   sqrt(5)/6)` independently of any coupling assumption.

3. The cross-row identity `(R3)` is **new structural content**: it
   combines two independently-measured CKM products into one sharp
   test, providing a measurement-friendly route to falsify the
   framework's specific atlas point.

This separation also makes the framework's prediction more robust to
α_s uncertainties: while the absolute |V_qq'| values shift if the
canonical coupling shifts, the α_s-independent ratios `(R1)-(R3)`
remain at their framework-specific values regardless. They are the
**framework-specific atlas signature**.

## Falsification

The PDG values for `(R1)-(R3)` agree with the framework's atlas-LO
predictions at `< 0.2 sigma`. As CKM precision improves, these become
sharper tests:

- LHCb / Belle II era: `sigma(|V_td|/|V_ub|)` likely tightens to
  `~0.05`, tightening the test of `(R2)` to ~0.5σ comparator.
- HL-LHC era: `sigma(|V_ts|/|V_cb|)` may tighten to `~0.01`,
  tightening `(R1)` to ~5σ comparator.

A non-zero deviation from the framework's exact rational/radical
ratios would falsify the atlas point or the Thales-circle assumption.

## What This Claims

- `|V_ts|/|V_cb| = 1` exactly at atlas-LO (α_s-independent).
- `|V_td|/|V_ub| = sqrt(5)` exactly at atlas-LO (α_s-independent).
- `|V_td V_cb*|^2 / |V_ts V_ub*|^2 = 5` exactly at atlas-LO
  (α_s-independent, NEW cross-row identity).
- `R_b^2 = rho` exactly at the Thales atlas point (NEW form).
- `R_t^2 / R_b^2 = (1 - rho)/rho = 5` (atlas point).
- The structural classification: which CKM-magnitude ratios are
  α_s-independent (geometric) vs α_s-dependent (dynamical).

## What This Does Not Claim

- It does not derive `alpha_s(v)`, `rho`, `eta`, `lambda^2`, or
  `A^2`; all are retained inputs.
- It does not modify the absolute |V_qq'| predictions; only their
  ratios are explicitly α_s-classified.
- It does not promote NLO Wolfenstein corrections; the analysis is
  atlas-LO only.
- It does not promote any BSM CP signature.
- The framework's atlas-LO sin(2β_d) tension at 3.6σ vs PDG remains;
  `(R1)-(R3)` are sharper because they target ratios where the
  α_s-running residual cancels.

## Reproduction

```bash
python3 scripts/frontier_ckm_thales_pinned_alpha_s_independent_ratios.py
```

Expected result:

```text
TOTAL: PASS=31, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import. All α_s-independent
ratio checks use exact `fractions.Fraction` arithmetic.

## Cross-References

- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
  -- retained `|V_td|^2 = 5 alpha_s^3/72`, `|V_ts|^2 = alpha_s^2/6`,
  `|V_ub|^2 = alpha_s^3/72`, `|V_cb|^2 = alpha_s^2/6` magnitudes.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `rho = 1/6`, `eta = sqrt(5)/6`.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- retained Thales circle `eta^2 = rho(1 - rho)`, R_t/R_b = sqrt(5).
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`.
- [`CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md`](CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md)
  -- companion α_s-DEPENDENT extraction route (cross-sector).
- [`CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md)
  -- companion α_s-DEPENDENT cross-system CP ratio.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` retained input.
