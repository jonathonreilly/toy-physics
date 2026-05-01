# Review History — ew-current-fierz-channel-derivation-20260501

Branch-local self-review log. Disposition: `pass`, `passed_with_notes`,
`demote`, or `block`.

## Block — EW current Fierz-channel decomposition

**Date:** 2026-05-01T22:30Z
**Artifact:** docs/EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md
**Runner:** scripts/frontier_ew_current_fierz_channel_decomposition.py
**Branch:** physics-loop/ew-current-fierz-channel-derivation-block01-20260501

### Goal

Break the 2026-05-01 audit ledger's 3-node citation cycle:

```
yt_ew_color_projection_theorem  ↔  rconn_derived_note  ↔
    ew_current_matching_ozi_suppression_theorem_note_2026-04-27
```

by writing one new note that derives the (N_c^2 − 1)/N_c^2 connected-channel
ratio from a different chain than the existing 1/N_c topological derivation,
with citations only to retained upstream notes.

### 6-criterion self-review

1. **Bugs / logic errors / silent failures**: PASS. Runner gave PASS=31
   FAIL=0 on first execution. Numerically verifies the Fierz identity
   (max error ~10^-14) for N_c = 2, 3, 4, 5 across 40 random matrices.
   Dimension count and exact 8/9 = `Fraction(8,9)` verified.
2. **Dead code / debug**: PASS. Runner uses standard helpers
   consistently. `su_n_generators(n)` builds the standard SU(N) basis
   from scratch (symmetric off-diagonal, antisymmetric off-diagonal,
   diagonal traceless) and verifies trace normalization at machine
   precision.
3. **Naming consistency**: PASS. The two halves of the load-bearing
   chain are named explicitly throughout: `(F)` exact group-theory
   ratio (derived) vs `(M)` matching rule (admitted structural input,
   not derived).
4. **Missing accessibility**: N/A.
5. **Hardcoded magic numbers**: PASS. The only "magic numbers" are
   N_c values 2, 3, 4, 5 used for verification. The N_c = 3 special
   case is sourced from `GRAPH_FIRST_SU3_INTEGRATION_NOTE` (retained).
6. **Project convention compliance**: PASS. Status language follows
   `CONTROLLED_VOCABULARY.md`: uses `support / exact group-theory
   derivation (cycle-breaking)`. No bare retained/promoted status line. The note
   explicitly disclaims promotion of the 9/8 package-level coefficient.

### Cycle-breaking verification

Critical for this block: the new note must NOT cite the 3 cycle nodes
via markdown link. Verified by runner Part 2:

- `[YT_EW_COLOR_PROJECTION_THEOREM.md](...)` — not present
- `[RCONN_DERIVED_NOTE.md](...)` — not present
- `[EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md](...)` — not present

The 3 cycle node names DO appear in the note (in §0 explanation, §6 cycle
discussion, §9 forbidden imports, §11 cross-references), but only as
plain prose / unlinked filenames. Citation graph builder parses
`[text](path)` markdown links, so plain prose mention does not create a
graph edge.

### Forbidden-imports check

PASS. The note explicitly names the 3 cycle nodes in its forbidden-imports
section (§9) and explains that retroactively citing them would re-introduce
the cycle. The Fierz identity is admitted as textbook math (proved inline
in §2), not as a citation to any non-retained note.

### Honest scope check

PASS. The note carefully separates:

- **Derived (exact group theory on the support surface):** the ratio
  `dim(adj)/dim(q-qbar) = (N_c^2 − 1)/N_c^2 = 8/9` at N_c = 3.
- **Not derived (named admitted input):** the matching rule (M) — that
  the physical EW vacuum polarization projects onto the adjoint channel.

The package-level 9/8 EW coupling correction depends on BOTH (F) and (M).
This note closes only (F). The 9/8 coefficient remains bounded until (M)
is independently derived. The note explicitly states this in §5, §6, §10.

### What this PR does NOT do

- Does not edit the 3 cycle nodes. Cycle-cleanup PRs that update those
  notes to cite this new note are explicitly out-of-scope follow-up work.
- Does not promote any claim to `retained`.
- Does not derive the matching rule (M).

### Disposition

**pass** — coherent cycle-breaking derivation with verified group-theory
arithmetic and honest scope on the matching-rule limitation. Runner gives
PASS=31 FAIL=0. PR is review-only.
