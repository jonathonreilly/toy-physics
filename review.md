# Review: Path-A Sylvester Branch Theorem

Reviewed branch tip: `5fc73b2d`

## Verdict

Not cleared for `main`.

The determinant polynomial appears numerically consistent with direct
evaluation, so this is not blocked by an obvious algebra mistake. The blockers
are theorem-scope and evidence-surface blockers.

## Findings

### [P1] Linear-path witness does not derive the physical branch rule

The note proves at most that the P3 pin lies on the same non-singular
signature component as `H_base` along one chosen path. It does not derive the
missing physical principle that the baseline-connected component is the live
sheet. Without that extra step, Basins 2/X are excluded only if the old
imposed branch-choice rule is kept. The promotion table and the claim that the
theorem excludes Basins 2/X "by proof" therefore overstate what has actually
been established.

Affected surface:
- `docs/DM_FLAGSHIP_PATH_A_SYLVESTER_BRANCH_THEOREM_NOTE_2026-04-18.md`

### [P1] Step 2/3 are sampled evidence, not a theorem-grade positivity proof

The load-bearing claim is interval-wide non-singularity of `H(t)` on
`t ∈ [0,1]`, but the proof only samples 11 values of `t` and then performs a
1107-point tube scan. That is numerical support, not a proof over a
continuous segment or neighborhood. Since `det(H(t))` is the decisive object,
this needs an exact 1D argument, such as the explicit cubic in `t` together
with derivative/root analysis or an equivalent certified bound.

Affected surface:
- `docs/DM_FLAGSHIP_PATH_A_SYLVESTER_BRANCH_THEOREM_NOTE_2026-04-18.md`

### [P2] New authority note conflicts with the still-live primary evidence surface and has no dedicated verifier

This branch adds only the new note. The primary selector runner still
explicitly says the branch-choice rule is imposed and not retained, and there
is no new runner here that audits the closed-form determinant, the path
minimum, or the claimed Basin-2/X exclusion. So the note is ahead of the
certifying evidence surface. It is also not woven through the package
control-plane files required for a `main` landing.

Affected surfaces:
- `docs/DM_FLAGSHIP_PATH_A_SYLVESTER_BRANCH_THEOREM_NOTE_2026-04-18.md`
- `scripts/frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py`

## What would be needed

1. Add a dedicated runner for the Path-A theorem itself.
2. Replace sampled path positivity with an exact interval argument.
3. Keep the result pointwise/conditional unless the missing physical
   branch-selection principle is also derived.
4. Only after that, align the package/control-plane surfaces if promotion is
   still justified.
