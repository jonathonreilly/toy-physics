# Three-Sector Dimension-Color Quadratic Identity Support Note

**Date:** 2026-04-25

**Status:** conditional cross-sector support corollary on current `main`.
This note does **not** promote charged-lepton Koide closure or the
bare-α₃/α_em ratio to retained status. It packages the algebraic
bridge that becomes available **if** the current open/support
targets are simultaneously accepted:

```text
(alpha_3 / alpha_em)(bare)  ×  Q_l  =  N_quark  =  6
```

with the **conditional** consequence (NEW algebraic content):

```text
2d + 3  =  N_color^2,    d  =  (N_color^2 - 3) / 2.
```

For framework `N_color = 3`: `d = 3` is the smallest integer solution.

This is a **falsification and cross-extraction target**, not a
retained closure. The bare-α₃/α_em ratio carrier note on `main` is
itself a support note (`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`),
and the charged-lepton Koide ratio `Q_l = 2/3` remains an open
support target with active investigation across the `KOIDE_*` notes
on `main`.

**Primary runner:**
`scripts/frontier_framework_three_sector_dimension_color_quadratic_identity.py`

## Statement (Conditional)

If the following two open/support inputs are accepted:

```text
(P1)  (alpha_3 / alpha_em)(bare)  =  2d + 3            [conditional, support]
(P2)  Q_l  =  N_pair / N_color  =  2/3                  [conditional, open]
```

together with the framework gauge-counting

```text
(G1)  N_pair = 2,  N_color = 3,  N_quark = N_pair x N_color = 6,
```

then the algebraic identity

```text
(I1)  (alpha_3 / alpha_em)(bare)  ×  Q_l  =  N_quark  =  6
```

holds at framework values, and substituting closed forms gives:

```text
(I2)  (2d + 3)  ×  (N_pair / N_color)  =  N_pair  ×  N_color
(I3)  2d + 3  =  N_color^2
(I4)  d  =  (N_color^2 - 3) / 2.
```

For `N_color = 3` this gives `d = 3`. Integer solutions to `(I4)`:

```text
N_color = 3  ->  d = 3       [framework-consistent, smallest integer solution]
N_color = 5  ->  d = 11      [algebraically allowed; phenomenologically excluded by SM]
N_color = 7  ->  d = 23
N_color = 2  ->  d = 1/2     [non-integer, excluded]
N_color = 4  ->  d = 13/2    [non-integer, excluded]
```

When composed with the **separately retained** atlas CKM CP-phase
`eta = sqrt(5)/6`, identity `(I1)` extends to:

```text
(I5)  (alpha_3 / alpha_em)(bare)  ×  Q_l  ×  eta  =  6 × sqrt(5)/6  =  sqrt(5).
```

`(I5)` is conditional on `(P1)` and `(P2)`.

## Inputs And Status

| Input | Sector | Status | Authority on `main` |
| --- | --- | --- | --- |
| `g_3^2(bare) = 1` | color | conditional support | [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) (explicitly support, not minimal-input) |
| `g_2^2(bare) = 1/(d+1) = 1/4` | EW (weak) | conditional support | [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md), [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md) |
| `g_Y^2(bare) = 1/(d+2) = 1/5` | EW (hypercharge) | conditional support | same as above |
| `(alpha_3/alpha_em)(bare) = 2d+3 = 9` | color + EW | **conditional support** (P1) | [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md) |
| `Q_l = 2/3` | charged lepton | **open support target, not retained closure** (P2) | [`KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`](KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md), [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md), [`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md) |
| `N_pair = 2`, `N_color = 3` | gauge structure | retained framework axioms | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md), [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| `N_quark = 6 = N_pair x N_color` | SM quark structure | retained | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| `eta = sqrt(5)/6` | CKM atlas | retained | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |

The two **load-bearing** inputs are flagged in the table above as
"conditional support" (P1) and "open support target" (P2). The
identity `(I1)` follows iff both are accepted simultaneously.

No PDG observable is used as a derivation input.

## Derivation

If `(P1)` and `(P2)` are accepted, then by direct substitution:

```text
(alpha_3 / alpha_em)(bare)  ×  Q_l
   =  (2d + 3)  ×  (N_pair / N_color)
   =  9 × (2/3)
   =  6
   =  N_pair × N_color
   =  N_quark.
```

The conspiracy `9 × 2/3 = 6` is non-trivial: it requires both `(P1)`
and `(P2)` to hold simultaneously at the framework's specific
`(d=3, N_color=3, N_pair=2)`.

Substituting closed forms in `(I1)`:

```text
(2d + 3) × (N_pair / N_color)  =  N_pair × N_color.
```

Multiplying both sides by `N_color/N_pair`:

```text
2d + 3  =  N_color^2.
```

Solving for `d`: `d = (N_color^2 - 3)/2`. For framework `N_color = 3`:
`d = 3`.

Composing with retained atlas CKM CP-phase `η = √5/6`:

```text
(alpha_3 / alpha_em)(bare)  ×  Q_l  ×  η
   =  6 × (√5/6)
   =  √5.
```

The factor 6 cancels, leaving the irrational √5.

## Numerical Verifications (Conditional on P1, P2)

| Quantity | Closed form | Framework value |
| --- | --- | ---: |
| `(alpha_3/alpha_em)(bare)` | `2d + 3` | `9` (integer) |
| `Q_l` | `N_pair/N_color` | `2/3` |
| `(alpha_3/alpha_em) × Q_l` | `(2d+3) × (N_pair/N_color)` | `6 = N_quark` |
| `2d + 3` | `N_color^2` | `9 = 3²` |
| `d` from `N_color` | `(N_color² - 3)/2` | `3` |
| `(α/α) × Q_l × η` | `6 × √5/6` | `√5` |

These are conditional verifications — they hold **iff** both `(P1)`
and `(P2)` hold. If either premise fails, the identity does not hold
in retained form.

## What This Note Claims

- The **conditional algebraic identity** `(I1)` and its consequences
  `(I2)–(I5)`, **assuming** `(P1)` and `(P2)`.
- The cross-sector consistency `(α_3/α_em)(bare) × Q_l = 6` is
  algebraically tight at framework values **iff** both load-bearing
  premises are accepted.
- The dimension-color quadratic `2d + 3 = N_color²` is an algebraic
  consequence of `(I1)`, **conditional** on the same premises.
- `(d, N_color) = (3, 3)` is the smallest integer solution to the
  quadratic `2d + 3 = N_color²`.

## What This Note Does NOT Claim

- It does not promote `Q_l = 2/3` to retained closure. The Koide
  closure remains an open support target.
- It does not promote `(α_3/α_em)(bare) = 2d + 3` to retained
  closure. The bare-α ratio carrier note on `main` is itself a
  support note.
- It does not derive the spatial dimension `d = 3` from PDG or any
  observable. The identity is algebraic, not phenomenological.
- It does not claim retention or closure of the cross-sector
  conspiracy `9 × 2/3 = 6`. The conspiracy emerges only **if** both
  premises are simultaneously accepted.
- It does not modify any retained CKM atlas, Wolfenstein, or
  CP-phase theorem.
- It does not promote any GUT-style unified gauge group, BSM
  extension, or alternative dimensional axiom.
- It is **not part of the accepted minimal-input stack on `main`**.

## Falsification Use

The note's value is as a **falsification and cross-extraction
template** that becomes precise once the load-bearing premises close:

1. If a future Koide-closure theorem retains `Q_l = 2/3` from
   independent first principles, then `(I1)` becomes a sharp
   cross-sector test of the bare-α ratio carrier.
2. If a future bare-α derivation retains `(α_3/α_em)(bare) = 2d + 3`
   on the minimal-input stack, then `(I1)` becomes a sharp
   cross-sector test of the Koide ratio.
3. If both close independently, `(I1)` and the dimension-color
   quadratic become a retained corollary, with the consistency check
   `9 × 2/3 = 6` providing a precision test of the framework's
   `(d=3, N_color=3, N_pair=2)` triple.

Until either premise is independently closed, the note is a
**conditional support corollary**, not a retained derivation.

## Reproduction

```bash
python3 scripts/frontier_framework_three_sector_dimension_color_quadratic_identity.py
```

Expected result:

```text
TOTAL: PASS=27, FAIL=0
```

The runner verifies the conditional algebra **after** the
load-bearing premises `(P1)` and `(P2)` are assumed. It does not
establish retention of those premises.

## Cross-References

- [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md)
  -- conditional support note carrying `(α_3/α_em)(bare) = 2d + 3 = 9` (P1).
- [`CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md)
  -- companion conditional support note for `Q_l × α_s² = 4 |V_cb|²`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `η = √5/6` CKM CP-phase used in `(I5)`.
- [`KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`](KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md),
  [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md),
  [`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md)
  -- open/support targets and active investigation around `Q_l = 2/3` (P2).
- [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
  -- algebraic support theorem (explicitly not part of minimal-input stack).
