# g_bare Derivation Note — Status Correction Audit

**Date:** 2026-05-02
**Status:** demotion / status correction packet for
[`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) (currently
`unknown / audited_conditional`, td=263, lbs=14.26).
**Primary runner:** `scripts/frontier_g_bare_derivation_status_audit.py`
**Authority role:** dep-declaration / status correction / missing-runner
audit packet for the g_bare derivation residual.

## 0. Audit context

The parent note `G_BARE_DERIVATION_NOTE.md` proposes that the canonical
Cl(3) connection normalization is identified with unit gauge coupling
`g_bare = 1`. The audit verdict flagged:

> *"the decisive step identifies the canonical Cl(3) connection
> normalization with unit gauge coupling, while the note explicitly leaves
> open whether that is a constraint or a convention. Why this blocks: with
> no one-hop dependencies and a missing primary runner, the audit cannot
> verify the advertised normalization chain or its negative checks. Repair
> target: restore or replace `scripts/frontier_g_bare_derivation.py` and
> supply a retained theorem that removes the A → A/g rescaling freedom."*

The verdict identifies three issues:
1. **Constraint vs. convention ambiguity** — the note is ambiguous whether
   `g_bare = 1` is a structural constraint or a convention choice.
2. **Missing primary runner** — `scripts/frontier_g_bare_derivation.py`
   does not exist (verified at 2026-05-02).
3. **A → A/g rescaling freedom** — the retention claim requires a theorem
   that removes the rescaling freedom; not currently provided.

## 1. Verification of missing runner

The audit verdict claims the runner is missing. Confirmed at 2026-05-02:

```bash
$ ls scripts/frontier_g_bare_derivation.py
ls: scripts/frontier_g_bare_derivation.py: No such file or directory
```

The ledger row's `runner_path` field would be needed to verify the parent
note's claims; without it, the audit cannot proceed past the structural
review of the note text alone.

## 2. The constraint vs. convention ambiguity

`g_bare = 1` can mean either:

**(a) Structural constraint.** A theorem stating that the Cl(3) framework
*forces* `g_bare = 1` as the unique compatible value, with all other
values disallowed by the framework's algebraic structure.

**(b) Convention choice.** A normalization choice fixing the scale of the
gauge connection field A, with `g_bare = 1` chosen as the canonical value.
Equivalent to a units choice for A.

Without explicit derivation, the parent note conflates (a) and (b). Under
(a), `g_bare = 1` is load-bearing for retention. Under (b), it's an
admitted convention with narrow non-derivation role.

## 3. The A → A/g rescaling freedom

The continuum gauge action is invariant under field rescaling `A → A/g`:

```text
S_gauge[A; g] = (1/4 g²) ∫ d⁴x F_μν F^μν
            = (1/4) ∫ d⁴x (∂_μ A'_ν - ∂_ν A'_μ + ...)²    (with A' = g A)
```

This means `g_bare` and the field normalization are reciprocally related
gauge-fixing choices. To force `g_bare = 1` uniquely, a theorem must:
- either pin the field normalization (removing the A → A/g freedom by
  another convention), OR
- prove a structural identity in the Cl(3) framework that fixes the
  combination `g_bare × |A|` non-trivially.

Neither is provided in the parent note.

## 4. Seven retained-proposal certificate criteria

| # | Criterion | Pass? |
|---|---|---|
| 1 | `proposal_allowed: true` | **NO** |
| 2 | No open imports | **NO** (constraint vs. convention ambiguity is itself an open import) |
| 3 | No load-bearing observed/fitted/admitted | **NO** if (a) / **YES** if (b); ambiguity prevents resolution |
| 4 | Every dep retained | **N/A** (deps=[] but missing runner means audit cannot proceed) |
| 5 | Runner checks dep classes | **NO** (missing runner) |
| 6 | Review-loop disposition `pass` | **PENDING** |
| 7 | PR body says independent audit required | **YES** |

**Result:** Criteria 1, 2, 3, 5 fail. The note CANNOT be retained until
the constraint/convention ambiguity is resolved AND a runner is supplied.

## 5. Recommended status correction

```yaml
# g_bare_derivation_note (parent)
current_status: bounded normalization proposal  # was: unknown
audit_status: audited_conditional                # unchanged
proposal_allowed: false
proposal_allowed_reason: |
  (a) constraint-vs-convention ambiguity unresolved
  (b) primary runner missing (frontier_g_bare_derivation.py)
  (c) A → A/g rescaling freedom not removed by theorem
```

## 6. Path to retention

| Required step | Difficulty |
|---|---|
| Restore or replace `scripts/frontier_g_bare_derivation.py` | medium (engineering) |
| Resolve constraint vs. convention ambiguity in note | medium (clarification) |
| Supply theorem removing A → A/g rescaling freedom | hard (Nature-grade) — requires a structural identity in Cl(3) that fixes `g_bare × |A|` |

The third step is the substantive obstruction. The first two are housekeeping.

## 7. Audit-graph effect

After this PR lands:
- The parent's `current_status` corrects from `unknown` to `bounded
  normalization proposal`.
- 263 transitive descendants inherit the corrected status.
- The G_BARE_* family closure (which requires `g_bare_derivation_note` +
  6 G_BARE_* sister theorems) remains an open Nature-grade target.

## 8. Cross-references

- Parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md)
- Sister G_BARE_* family rows (all conditional):
  - `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18`
  - `G_BARE_RIGIDITY_THEOREM_NOTE`
  - `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18`
  - `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19`
  - `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19`
  - `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18`
- Cycle 4 connection: `alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30`
  imports `g_bare = 1` as a load-bearing structural input — that cycle
  flagged the same admission.
