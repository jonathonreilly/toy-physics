# CKM Wolfenstein `eta^2` Inverse-Square Structural Reading Theorem

**Date:** 2026-04-26

**Status:** proposed_retained CKM-structure corollary on current `main`

**Primary runner:** `scripts/frontier_ckm_wolfenstein_eta_inverse_square_gap.py`

## Claim

Using only retained `main` authorities, the retained CKM value

```text
eta^2 = 5/36
```

admits a new exact structural reading from the same quark-doublet source that
now grounds `A^2` below `W2`:

```text
(W1)  eta^2
    = 1/N_pair^2 - 1/N_color^2
    = 1/(dim_SU2(Q_L))^2 - 1/(dim_SU3(Q_L))^2
    = 1/4 - 1/9
    = 5/36.
```

Here `N_pair = 2` and `N_color = 3` are read directly from the retained
matter-content literal

```text
Q_L : (2,3)_{+1/3}.
```

This is a **new retained structural reading** of the already-retained CKM
parameter `eta^2`. It is **not** a below-`Wn` closure claim and it does **not**
promote any non-main authority.

## Additional Exact Identities

The same retained package gives four companion algebraic identities:

```text
(W2)  rho A^2 = 1/N_color^2 = 1/9

(W3)  eta^2 + rho A^2 = 1/N_pair^2 = 1/4

(W4)  eta^2 + 2 rho A^2 = 1/N_pair^2 + 1/N_color^2 = 13/36

(W5)  rho = 1/(N_pair N_color) = 1/6

(W6)  eta^2 = (N_color^2 - N_pair^2)/N_quark^2 = 5/36.
```

The theorem packages these as CKM-side structural readouts on the retained
source surface. In particular:

- `W2` is an exact factorization of retained `rho` and retained `A^2`; it is
  **not** an SM-uniqueness theorem.
- `W1`, `W3`, `W4`, and `W6` are exact retained-value identities at the
  sourced `Q_L:(2,3)` counts.

## Structural Interpretation

The new content is the interpretation of CP violation as an inverse-square gap
between the non-abelian gauge-representation dimensions acting on the retained
left-handed quark doublet:

```text
eta^2
= 1/(SU(2)_L doublet dimension)^2
  - 1/(SU(3)_c triplet dimension)^2.
```

Equivalently, the CKM CP-phase package may now be read as

```text
rho      = 1/(N_pair N_color),
eta^2    = 1/N_pair^2 - 1/N_color^2,
rho A^2  = 1/N_color^2,
```

so that `rho`, `eta^2`, and `rho A^2` split naturally into factorizations over
the same sourced structural integers `(N_pair, N_color) = (2,3)`.

## Retained Inputs

| input | authority on `main` | role |
| --- | --- | --- |
| `Q_L:(2,3)_{+1/3}` | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | retained source literal fixing `N_pair=2`, `N_color=3` |
| `u_R:(1,3)`, `d_R:(1,3)` | [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | same-sector color cross-check |
| below-`W2` quark-doublet source theorem | [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md) | mainline source theorem reusing the same retained literal |
| `A^2 = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | retained Wolfenstein count ratio |
| `rho = 1/N_quark`, `eta^2 = (N_quark-1)/N_quark^2` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained CKM CP-phase package |
| `N_quark = N_pair N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained structural counts |
| Bernoulli-family comparator | `CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md` | consistency cross-check only |

No support-tier authority is load-bearing.

## Derivation

From the retained source literal `Q_L:(2,3)_{+1/3}`:

```text
N_pair  = 2,
N_color = 3,
N_quark = N_pair N_color = 6.
```

From the retained CKM package:

```text
A^2   = N_pair/N_color = 2/3,
rho   = 1/N_quark = 1/6,
eta^2 = (N_quark - 1)/N_quark^2 = 5/36.
```

Then:

```text
1/N_pair^2 - 1/N_color^2
= 1/4 - 1/9
= 5/36
= eta^2,
```

which is `(W1)`.

Also:

```text
rho A^2
= (1/N_quark)(N_pair/N_color)
= (1/(N_pair N_color))(N_pair/N_color)
= 1/N_color^2,
```

which is `(W2)`.

Then:

```text
eta^2 + rho A^2
= (1/N_pair^2 - 1/N_color^2) + 1/N_color^2
= 1/N_pair^2,
```

giving `(W3)`, and

```text
eta^2 + 2 rho A^2
= (1/N_pair^2 - 1/N_color^2) + 2/N_color^2
= 1/N_pair^2 + 1/N_color^2,
```

giving `(W4)`.

Finally,

```text
eta^2
= 5/36
= (9 - 4)/36
= (N_color^2 - N_pair^2)/N_quark^2,
```

which is `(W6)` at the retained sourced values.

## Comparator and Scope

This theorem is deliberately narrow.

It does:

- add a new retained structural reading of `eta^2`,
- package exact companion identities `W2`-`W6`,
- cross-check compatibility with the retained Bernoulli-family reading
  `eta^2 = V(N_pair) M(N_color) M(N_quark)`.

It does not:

- claim a new below-`Wn` closure,
- claim `rho A^2 = 1/N_color^2` is SM-unique,
- rely on any unmerged or support-only theorem to carry the derivation.

## Science Value

The retained CKM value `eta^2 = 5/36` already had two exact structural
packagings on `main`:

```text
eta^2 = (N_quark - 1)/N_quark^2,
eta^2 = V(N_pair) M(N_color) M(N_quark).
```

This theorem adds a third:

```text
eta^2 = 1/N_pair^2 - 1/N_color^2.
```

That new form is sharper geometrically. It interprets CKM CP violation as a
gap between inverse-squared non-abelian representation dimensions read off the
same retained `Q_L` source that now grounds `A^2` below `W2`. It also exposes
the exact sum identities `W3` and `W4`, which were not previously packaged on
`main`.

## Verification

The runner:

- extracts `Q_L:(2,3)` by regex from disk,
- verifies the cited authority status lines from disk,
- derives `W1`-`W6` by exact `Fraction` arithmetic,
- cross-checks Bernoulli compatibility,
- audits that `W2` is a generic factorization on the count surface rather than
  an SM-uniqueness statement.

---

## Current audit-lane disposition (informational)

This row was audited on 2026-05-05 by
`codex-cli-gpt-5.5-20260505-225305-c0ea7096-ckm_wolfenstein_eta_inve-090`
and returned `audited_conditional`. The verdict identifies a
concrete local extraction gap, not just upstream-conditional propagation:

> *Direct authorities in the restricted packet are not retained-grade:
> several are marked unaudited and CKM_MAGNITUDES is audited_conditional;
> additionally, the runner exits nonzero because it cannot extract the
> asserted Q_L literal from LEFT_HANDED_CHARGE_MATCHING_NOTE.*

The six declared upstream authorities now sit at:

| Upstream authority | Effective status (current) |
|---|---|
| [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | `unaudited` |
| [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | `unaudited` |
| [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md) | `audited_conditional` |
| [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | `unaudited` (PR #764 added exact-symbolic verification, awaiting re-audit) |
| [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | `unaudited` |
| [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | `unaudited` (PR #766 added exact-symbolic magnitude-count verification, awaiting re-audit) |

### Local extraction gap (report-only)

The ledger-recorded runner failure at
`scripts/frontier_ckm_wolfenstein_eta_inverse_square_gap.py` reports

```text
S1 source extraction from retained matter-content literal
  [FAIL (D)] Extract Q_L:(a,b) from retained doc
FATAL: could not extract Q_L literal.
```

This is the same Q_L-literal extraction failure that affects
[`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md):
`LEFT_HANDED_CHARGE_MATCHING_NOTE.md` does discuss the `(2,3)` and
`(2,1)` blocks of the LH-doublet sector, but does not write the Q_L
literal in the `Q_L : (a,b)_{Y}` form the runner pattern expects. Two
repair paths remain, both deferred to a separate proof-walk PR rather
than this audit-sweep:

1. *Source-side repair*: amend `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` to
   include the explicit literal `Q_L : (2,3)_{+1/3}` so the extractor
   succeeds.
2. *Runner-side repair*: relax the extractor pattern to accept the
   existing `(2,3)` block discussion plus the surrounding
   "LH-doublet sector" context.

Until one of those lands, this row is upstream-conditional on the
unaudited matter-content authorities AND additionally fails its own
local extraction step, so it cannot be promoted. The local
class-(A) algebra in §§W1--W6 is unaffected.
