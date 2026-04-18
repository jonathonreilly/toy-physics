# Review Note: `claude/inspiring-banzai-7002dd`

## Status

Current verdict: **do not merge as-is**.

The previously reported estimator-alignment issue is fixed:

- the long probe now keys its bottom-line verdict off the same
  two-parameter `RT(L) = c_inf + a / ln(L)` fit on the `L >= 48` tail window
  that the note cites;
- the note citations match the probe output;
- the frontier runner still replays cleanly at `PASS = 11, FAIL = 0`.

So the main science-facing mismatch is gone.

## Remaining blocker

### Package truth surfaces still conflate the frontier runner with the long probe

Two package-facing files still describe the evidence as if one `11/11` runner
verified the `L <= 96` range:

- `docs/publication/ci3_z3/PUBLICATION_MATRIX.md`
- `docs/publication/ci3_z3/DERIVATION_ATLAS.md`

That is not what the branch actually contains.

The actual split is:

- `scripts/frontier_bh_entropy_rt_ratio_widom.py`
  - verifies the retained no-go theorem on the main runner surface
  - uses `L <= 64`
  - returns `PASS = 11, FAIL = 0`
  - cites the `L >= 32` fit with `c_inf = 0.1601`

- `scripts/probe_bh_rt_ratio_asymptotic.py`
  - is the extended probe
  - pushes to `L <= 96`
  - uses the authoritative `L >= 48` verdict fit
  - gives `c_inf = 0.163141`
  - is separate evidence, not the source of the `11/11` frontier verdict

So rows that currently say things like

- "numerically confirmed on `L` up to `96`, `PASS = 11 / FAIL = 0`"
- or "`L = 8..96` passes `11/11`"

are overstating what a single artifact certifies.

## Required fix

Keep the evidence split explicit in the package surfaces:

- frontier runner:
  - `L <= 64`
  - `PASS = 11, FAIL = 0`
  - `c_inf(L>=32) = 0.1601`

- extended probe:
  - `L <= 96`
  - separate long probe / output artifact
  - `c_inf(L>=48) = 0.163141`
  - not the source of the `11/11` frontier verdict

Once the matrix/atlas wording is corrected to match the actual evidence
contract, this branch looks close to clear.
