# CKM Alpha_s-Independent Structural Ratios Theorem

**Date:** 2026-04-26

**Status:** retained CKM-structure corollary on the promoted CKM atlas
and NLO Wolfenstein protected-gamma_bar surfaces.

This note packages six dimensionless CKM-magnitude ratios whose
`alpha_s(v)` powers cancel exactly on the retained surface, plus one
near-integer `|V_td/V_ub|^2` ratio whose residual dependence is only the
small NLO barred-apex correction. The content is a structural ratio
corollary, not a new CKM fit and not an all-orders magnitude theorem.

**Primary runner:**
`scripts/frontier_ckm_alpha_s_independent_structural_ratios.py`

## Headline Identities

On the retained surface

```text
lambda^2 = alpha_s(v)/N_pair = alpha_s(v)/2,
A^2      = N_pair/N_color    = 2/3,
rho      = 1/N_quark         = 1/6,
eta^2    = (N_quark - 1)/N_quark^2 = 5/36,
N_quark  = N_pair N_color    = 6,
```

the following ratios are exact:

```text
(P1) |V_cb|^2 / |V_us|^4              = N_pair / N_color  = 2/3.
(P2) |V_us|^4 / |V_cb|^2              = N_color / N_pair  = 3/2.
(P3) |V_ub|^2 / |V_us|^6              = 1 / N_color^2     = 1/9.
(P4) |V_us|^6 / |V_ub|^2              = N_color^2         = 9.
(P5) |V_us|^2 |V_cb|^2 / |V_ub|^2     = N_quark           = 6.
(P6) |V_cb|^4 / (|V_us|^2 |V_ub|^2)   = N_pair^2          = 4.
```

The retained NLO barred-apex surface also gives

```text
(P7) |V_td/V_ub|^2 = (N_quark - 1) + alpha_s(v)^2 / N_pair^4
                   = 5 + alpha_s(v)^2/16.
```

At canonical `alpha_s(v) ~= 0.103`, P7 is `5.00066`, i.e. within
about `0.013 %` of the structural integer `N_quark - 1 = 5`.

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `(rho_bar, eta_bar)` NLO apex coordinates | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| `lambda^2 = alpha_s/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | retained |

No support-tier note, unmerged branch, or fitted CKM input is
load-bearing for the symbolic identities.

## Derivation

The retained Wolfenstein magnitudes carry fixed powers of `alpha_s(v)`:

```text
|V_us|^2 = lambda^2 = alpha_s/2,
|V_cb|^2 = A^2 lambda^4 = alpha_s^2/6,
|V_ub|^2 = A^2 lambda^6 (rho^2 + eta^2) = alpha_s^3/72.
```

Since `rho^2 + eta^2 = 1/N_quark`, ratios with matching total powers of
`alpha_s(v)` collapse to structural integers:

```text
|V_cb|^2 / |V_us|^4 = A^2 = N_pair/N_color.

|V_ub|^2 / |V_us|^6 = A^2 (rho^2 + eta^2)
                    = (N_pair/N_color)(1/N_quark)
                    = 1/N_color^2.

|V_us|^2 |V_cb|^2 / |V_ub|^2
    = (N_pair/N_color) / (1/N_color^2)
    = N_pair N_color
    = N_quark.

|V_cb|^4 / (|V_us|^2 |V_ub|^2)
    = (N_pair/N_color)^2 / (1/N_color^2)
    = N_pair^2.
```

For P7, use the retained NLO barred-apex coordinates directly:

```text
rho_bar = (4 - alpha_s)/24,
eta_bar = sqrt(5)(4 - alpha_s)/24.
```

Then

```text
|V_td/V_ub|^2
  = [A^2 lambda^6 ((1 - rho_bar)^2 + eta_bar^2)]
    / [A^2 lambda^6 (rho^2 + eta^2)]
  = ((1 - rho_bar)^2 + eta_bar^2) / (1/6)
  = 5 + alpha_s^2/16.
```

So P7 is exact on the retained NLO barred-apex surface, while its
integer reading `~= 5` is an excellent approximation at canonical
`alpha_s(v)`.

## PDG-Style Comparator Values

Using the same CKM central values used by the surrounding CKM
validation notes:

| Ratio | Framework | Comparator | Relative offset |
| --- | ---: | ---: | ---: |
| P1: `|V_cb|^2 / |V_us|^4` | 0.6667 | 0.6641 | 0.38 % |
| P2: `|V_us|^4 / |V_cb|^2` | 1.5000 | 1.5057 | 0.38 % |
| P3: `|V_ub|^2 / |V_us|^6` | 0.1111 | 0.1146 | 3.13 % |
| P4: `|V_us|^6 / |V_ub|^2` | 9.0000 | 8.7267 | 3.04 % |
| P5: `|V_us|^2 |V_cb|^2 / |V_ub|^2` | 6.0000 | 5.7956 | 3.41 % |
| P6: `|V_cb|^4 / (|V_us|^2 |V_ub|^2)` | 4.0000 | 3.8490 | 3.77 % |
| P7: `|V_td/V_ub|^2` | 5.0007 | 5.082 | 1.62 % |

These are comparator checks, not derivation inputs. The strongest
current experimental face is P1/P2 because it depends only on the
well-measured `|V_us|` and `|V_cb|`. P3-P6 are more sensitive to
`|V_ub|`, and should be read as future precision tests of the retained
surface rather than as independent closure of the CKM atlas.

## Falsifiable Structural Claim

The retained CKM surface forces the six alpha_s-independent ratios to
the structural values

```text
{2/3, 3/2, 1/9, 9, 6, 4}.
```

Any future high-precision CKM magnitude determination that moves one
of these ratios away from its structural value beyond the stated
NLO/finite-lambda scope would falsify the retained protected-gamma_bar
surface or the retained structural counts `(N_pair, N_color, N_quark)`.

## What This Claims

- `(P1-P6)`: retained alpha_s-independent structural-ratio identities
  for CKM magnitude combinations.
- `(P7)`: retained NLO ratio identity
  `|V_td/V_ub|^2 = (N_quark - 1) + alpha_s(v)^2/N_pair^4`.
- The ratios provide a compact experimental-comparator surface for
  the retained CKM atlas.

## What This Does Not Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing.
- Does **not** introduce a new `d` selector, `N_color` selector, or
  Koide bridge.
- Does **not** depend on an `alpha_s`-running pipeline for P1-P6.
- Does **not** claim all-orders CKM magnitude control beyond the
  retained atlas-leading/NLO surfaces used above.

## Reproduction

```bash
python3 scripts/frontier_ckm_alpha_s_independent_structural_ratios.py
```

Expected:

```text
TOTAL: PASS=18, FAIL=0
```
