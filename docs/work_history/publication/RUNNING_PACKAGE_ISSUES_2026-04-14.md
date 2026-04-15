# Historical Running Package Issues

**Date:** 2026-04-14  
**Status:** historical package-audit log; not part of the live authority path
**Purpose:** consistency register for publication/package mismatches found
during the main-branch audit.

This file records package issues whether they are already fixed here or still
need follow-up. It is not a science scorecard.

## Fixed in this audit

### `I01` Echo-family authority mismatch

**Problem:** `main` carried the older positive `GW echo timing` surface even
though later work had already resolved the accepted framework result to **no
detectable echoes**.

**Fix:** the package now carries the null-echo result through:

- [GW_ECHO_NULL_RESULT_NOTE.md](../../GW_ECHO_NULL_RESULT_NOTE.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)

The older positive timing note has been moved out of the main authority path
into work history.

### `I02` No reusable derivation/toolbox index

**Problem:** the package had a claim-level derivation/validation map, but no
single place to find reusable subderivations and theorem tools for closing the
remaining stack.

**Fix:** added and expanded [DERIVATION_ATLAS.md](./DERIVATION_ATLAS.md) into
the canonical main-branch toolbox for:

- retained derivation components
- closed subderivations on open lanes
- canonical authority selection when multiple route variants existed

### `I07` Matter rows depended on one umbrella route memo

**Problem:** several retained matter rows still pointed at
`GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md` instead of standalone canonical
main-branch authority notes.

**Fix:** the package now carries dedicated canonical matter notes:

- [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](../../LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](../../ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
- [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md)

The atlas, derivation/validation map, matrix, claims table, ledger, results
index, and figure plan now point to those notes directly.

### `I08` Imported tool notes carried branch-local headers

**Problem:** several main-branch authority/tool notes still carried
`codex/review-active`, `claude/youthful-neumann`, or
`codex/publication-prep` header lines even after they became authoritative on
`main`.

**Fix:** branch-local headers were stripped from the imported main-branch
authority/tool notes. Main-branch status is now expressed through the package
control plane rather than in per-note branch tags.

### `I09` Retained-claim atlas completeness was not explicitly audited

**Problem:** the atlas had been expanded substantially, but retained-claim
coverage had not yet been checked row-by-row against the actual retained claim
surface.

**Fix:** the atlas now carries an explicit last-audited coverage note, and the
row-by-row pass found and fixed two real omissions:

- generation-axiom boundary theorem was added as an explicit atlas tool
- hierarchy exponent `16 = 2 x 2^3` was added as an explicit atlas tool

### `I10` Atlas rows did not expose import class explicitly

**Problem:** the derivation atlas mixed pure framework tools with
bridge-conditioned and observation-conditioned rows, but it did not surface
that distinction explicitly enough for safe reuse.

**Fix:** the atlas now carries import class inline in the
`Status / import class` field, and the most easily misread `\alpha_s` / `y_t`
rows no longer read like clean zero-input tools.

## Still open / follow-up

### `I03` Bounded companion authority normalization is incomplete

Some bounded companion lanes still rely on older notes whose framing predates
the current matrix/ledger terminology. The package is much cleaner than before,
but not every companion row yet has a freshly normalized single-note authority
surface on `main`.

Current sharpened read:

- normalized in this pass:
  - `\Omega_\Lambda`
  - `n_s`
  - `w`
  - `\Lambda`
  - graviton mass
  - BH entropy
  - gravitational decoherence
  - proton lifetime
  - Lorentz-violation fingerprint
  - monopole mass
  - CKM mass-basis NNI bounded route
- fixed in a later pass:
  - Cabibbo/Jarlskog combined route note split into:
    - active bounded Cabibbo authority on `main`
    - active bounded Jarlskog authority on `main`
    - historical combined route note in work history
- still needing separate authority refresh:
  - `y_t` bounded authority surfaces once the lane itself settles

### `I04` Legacy docs tree remains noisy outside the curated package

The front door is now clean, but `docs/` still contains a large amount of
historical route material. That is not a front-door problem anymore, but it is
still a discoverability problem for deep repo browsing.

### `I05` Figures and equation density still lag the package organization

The package organization is now substantially cleaner than the manuscripts.
The next writing pass still needs:

- actual figures
- more explicit derivation content in the arXiv draft
- final table/figure synchronization

### `I06` Every bounded reviewer-facing row should converge toward one main-branch authority note

The matrix already captures the rows, but some families still point to mixed
route-history notes. Over time, each bounded row should converge toward one
current authority note on `main`.

## Audit rule

If a package inconsistency is discovered during review, add it here before it
is forgotten, even if the fix will land in a later pass.
