# Cross-Sector A^2-Q_l-|V_cb| Bridge Support Note

**Date:** 2026-04-25

**Status:** conditional cross-sector support corollary on current `main`.
This note does **not** promote charged-lepton Koide to retained status.
It packages the algebraic bridge that becomes available if the current
open Koide support target `Q_l = 2/3` is accepted:

```text
Q_l * alpha_s(v)^2 = 4 |V_cb|^2.
```

The retained inputs are the CKM atlas identities

```text
A^2 = 2/3,
lambda^2 = alpha_s(v) / 2,
|V_cb|^2 = A^2 lambda^4 = alpha_s(v)^2 / 6,
```

and the canonical `alpha_s(v)` value. The non-retained/open input is
the charged-lepton Koide target

```text
Q_l = 2/3.
```

Thus the bridge is useful as a falsification and cross-extraction
target, not as a retained closure of the lepton sector.

**Primary runner:**
`scripts/frontier_cross_sector_a_squared_koide_vcb_bridge.py`

## Statement

On the retained CKM atlas surface,

```text
(K1)  A^2 = N_pair / N_color = 2/3,
(K2)  lambda^2 = alpha_s(v) / 2,
(K3)  |V_cb|^2 = A^2 lambda^4 = alpha_s(v)^2 / 6.
```

Condition on the current charged-lepton Koide support target

```text
(L1)  Q_l = 2/3.
```

Then

```text
(X1)  |V_cb|^2 = Q_l lambda^4 = Q_l alpha_s(v)^2 / 4,

(X2)  Q_l alpha_s(v)^2 = 4 |V_cb|^2,

(X3)  Q_l = 4 |V_cb|^2 / alpha_s(v)^2,

(X4)  alpha_s(v) = 2 |V_cb| / sqrt(Q_l).
```

`(X2)` is the symmetric cross-sector test. `(X3)` extracts the Koide
ratio target from quark plus gauge-vacuum inputs. `(X4)` extracts the
canonical coupling from quark plus Koide-target inputs.

## Inputs And Status

| Input | Sector | Status | Authority |
| --- | --- | --- | --- |
| `A^2 = 2/3` | CKM/quark | retained CKM atlas | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `lambda^2 = alpha_s(v)/2` | CKM/quark | retained CKM atlas | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `|V_cb|^2 = A^2 lambda^4` | CKM/quark | retained CKM atlas | [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md) |
| canonical `alpha_s(v)` | gauge-vacuum | retained quantitative input | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| `Q_l = 2/3` | charged lepton | open/support target, not retained closure | [`KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`](KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md), [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md), [`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md) |

No PDG observable is used as a derivation input. The PDG values below
are comparators only.

## Derivation

From the retained CKM atlas,

```text
|V_cb|^2 = A^2 lambda^4.
```

Using `A^2 = 2/3` and the conditional Koide target `Q_l = 2/3`,

```text
|V_cb|^2 = Q_l lambda^4.
```

Substitute the retained `lambda^2 = alpha_s(v)/2`:

```text
|V_cb|^2 = Q_l (alpha_s(v)/2)^2
         = Q_l alpha_s(v)^2 / 4.
```

Rearranging gives

```text
Q_l alpha_s(v)^2 = 4 |V_cb|^2.
```

The extraction forms follow algebraically:

```text
Q_l = 4 |V_cb|^2 / alpha_s(v)^2,
alpha_s(v) = 2 |V_cb| / sqrt(Q_l).
```

## Numerical Comparator

With canonical `alpha_s(v) = 0.103303816...` and atlas-leading
`|V_cb|^2 = alpha_s(v)^2/6`:

| Quantity | Closed form | Value |
| --- | --- | ---: |
| `Q_l` target | `2/3` | `0.6667` |
| `|V_cb|^2` atlas | `alpha_s(v)^2/6` | `0.001778` |
| `Q_l alpha_s(v)^2` | `4 |V_cb|^2` | `0.00711` |
| extracted `Q_l` | `4 |V_cb|^2/alpha_s(v)^2` | `0.6667` |
| extracted `alpha_s(v)` | `2 |V_cb|/sqrt(Q_l)` | `0.1033` |

Using PDG-style comparator `|V_cb| = 0.0410 +/- 0.0014`:

| Comparator | Value | Conditional target | Deviation |
| --- | ---: | ---: | ---: |
| `Q_l = 4 |V_cb|^2 / alpha_s(v)^2` | `0.6301 +/- 0.0430` | `2/3` | `-0.85 sigma` |
| `alpha_s(v) = 2 |V_cb| / sqrt(Q_l)` | `0.1004 +/- 0.0034` | `0.1033` | `-0.85 sigma` |
| `4 |V_cb|^2` | `0.00672 +/- 0.00046` | `0.00711` | `+0.85 sigma` |

This is not evidence that the Koide target is retained. It is a
clean, measurable cross-sector consistency test of the retained CKM
surface together with the open Koide target.

## Falsification Roadmap

The current uncertainty is dominated by `sigma(|V_cb|)`.

| Era | `sigma(|V_cb|)` | `sigma(Q_l extracted)` | Approximate test sharpness |
| --- | ---: | ---: | ---: |
| PDG-style 2024 comparator | `0.0014` | `0.043` | `0.85 sigma` |
| Belle II / LHCb upgrade target | `0.0007` | `0.022` | `1.5 sigma` |
| HL-LHC scale target | `0.0003` | `0.010` | `3 sigma` |

If future `|V_cb|` precision stays centered near the current value, the
conditional bridge will put pressure on either the CKM atlas readout,
the Koide `Q_l = 2/3` target, or the canonical `alpha_s(v)` input.

## What This Claims

- The retained CKM atlas identities imply `|V_cb|^2 = alpha_s(v)^2/6`.
- Conditional on the open Koide support target `Q_l = 2/3`, the bridge
  `Q_l alpha_s(v)^2 = 4 |V_cb|^2` follows exactly at atlas-leading
  Wolfenstein order.
- The extraction formulas `(X3)` and `(X4)` are valid algebraic
  consequences under that same conditional scope.
- Current `|V_cb|` comparator data do not falsify the conditional
  bridge.

## What This Does Not Claim

- It does not close the charged-lepton Koide lane.
- It does not promote `Q_l = 2/3` to retained status.
- It does not assert three independently retained sector closures.
- It does not introduce a new retained framework constant named `2/3`.
- It does not replace the canonical plaquette/CMT `alpha_s(v)`
  determination.
- It does not include higher-order Wolfenstein corrections; the bridge
  is atlas-leading.
- It does not derive the PDG `|V_cb|` extraction or its experimental
  systematics.

## Reproduction

```bash
python3 scripts/frontier_cross_sector_a_squared_koide_vcb_bridge.py
```

Expected result:

```text
TOTAL: PASS=37, FAIL=0
```

The runner verifies the algebra and checks that current package control
surfaces still mark Koide as open/support rather than retained.

## Cross-References

- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `A^2 = N_pair/N_color = 2/3` and
  `lambda^2 = alpha_s(v)/2`.
- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
  -- retained `|V_cb|^2 = A^2 lambda^4 = alpha_s(v)^2/6`.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` input.
- [`KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`](KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md),
  [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md),
  [`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md)
  -- current Koide support/open-lane authority.
- [`CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md`](CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md)
  -- companion retained CKM cross-system `alpha_s(v)` estimator.
