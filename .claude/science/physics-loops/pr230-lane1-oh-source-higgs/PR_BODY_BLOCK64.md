## 2026-05-12 - Block64 Finite-Moment Atom-Residue Obstruction

Tested the next scalar shortcut after Blocks60-62: finite source/Stieltjes
moments plus fixed source carrier and compact-source support do not fix the
pole atom mass or scalar LSZ residue without an added
determinacy/extremality certificate.

The runner gives an executable positive-measure counterfamily.  Two measures
on `[0,1]` have identical `m0,m1,m2 = 1,1/2,1/3` but different atom mass at the
candidate pole `x=0`: `1/6` versus `1/4`.  That blocks treating finite moment
agreement, finite-shell Stieltjes checks, or source-carrier normalization as
residue authority.

New artifacts:
- `docs/YT_PR230_BLOCK64_FINITE_MOMENT_ATOM_RESIDUE_OBSTRUCTION_NOTE_2026-05-12.md`
- `scripts/frontier_yt_pr230_block64_finite_moment_atom_residue_obstruction.py`
- `outputs/yt_pr230_block64_finite_moment_atom_residue_obstruction_2026-05-12.json`
- aggregate gate updates in full positive closure and campaign status gates
- physics-loop state/review updates under `.claude/science/physics-loops/pr230-lane1-oh-source-higgs/`

Validation:
- `python3 -m py_compile ...` passed for Block64, full assembly, and campaign status runners.
- Block64 runner: `PASS=12 FAIL=0`
- full positive closure assembly: `PASS=190 FAIL=0`
- campaign status: `PASS=399 FAIL=0`
- assumption/import stress: `PASS=105 FAIL=0`
- retained-route certificate: `PASS=319 FAIL=0`
- positive-closure completion audit: `PASS=73 FAIL=0`
- audit pipeline and strict audit lint: passed with no errors; the pipeline
  seeded the Block64 note, `invalidate_stale_audits` reported `invalidated=0`,
  and strict lint kept the five existing warnings
- `git diff --check`: OK

Current status: no-go / exact negative boundary for this finite-moment residue
shortcut.  PR #230 remains draft/open; `proposal_allowed=false` and no
retained or `proposed_retained` wording is authorized.

Next action: positive closure must supply actual residue authority: an
extremal/determinate moment certificate, direct pole-row residue measurement,
or `K'(pole)` theorem, then still pair it with FV/IR/contact and canonical
`O_H`/physical-response authority.
