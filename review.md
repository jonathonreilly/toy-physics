# Review: `codex/pf-science-review-2026-04-18`

## Current Call

I do **not** clear this branch for landing on `main`.

My current disposition is:

- **No** as a `main` landing
- **Potentially yes** as a source branch for later salvage of individual
  lower-level science notes, after the evidence surface is rebuilt honestly

The core issue is not that the branch has no math in it. The branch contains a
large amount of real route decomposition and many exact negative / boundary
statements. The problem is that the top PF “closure” layer is not certified at
the repo’s normal theorem-runner standard, and the branch is not integrated
into the repo truth surfaces.

## Branch Hygiene

At the time of this pass:

- branch is **1 behind / 4 ahead** `origin/main`

That is not the main blocker, but it does mean even an accepted landing would
need a clean rebase.

## Replay Status

Representative scripts replay cleanly:

- `frontier_perron_frobenius_selection_axiom_boundary.py` → `PASS = 126, FAIL = 0, SUPPORT = 63`
- `frontier_perron_frobenius_current_bank_full_frontier_closure_2026_04_18.py` → `THEOREM PASS=4 SUPPORT=1 FAIL=0`
- `frontier_perron_frobenius_step2_wilson_local_nilpotent_charpoly_certificate_2026_04_18.py` → `THEOREM PASS=4 SUPPORT=1 FAIL=0`
- `frontier_pmns_graph_first_fixed_slice_scalar_production_discriminant_2026_04_18.py` → `THEOREM PASS=4 SUPPORT=1 FAIL=0`
- `frontier_gauge_vacuum_plaquette_beta6_first_hankel_certificate_2026_04_18.py` → `THEOREM PASS=4 SUPPORT=1 FAIL=0`

So this is **not** a runtime failure.

## Main Blockers

### 1. The top PF closure runners are citation / phrase auditors, not theorem verifiers

The umbrella PF scripts pass by checking whether the expected Markdown phrases
exist in earlier notes.

Representative examples:

- `frontier_perron_frobenius_selection_axiom_boundary.py` spends the bulk of
  its logic reading note files and checking for specific strings such as
  “one unique normalized strictly positive Perron vector,”
  “current exact bank does **not** already contain,” etc.
- `frontier_perron_frobenius_current_bank_full_frontier_closure_2026_04_18.py`
  does not compute the claimed branch-wide closure; it just checks whether the
  Wilson / PMNS / plaquette notes already say the relevant closure sentences.

That is useful as a note-consistency audit, but it is **not** enough to serve
as the primary evidence surface for claims such as:

- “all three frontier certificates are negatively closed on the current bank”
- “the present exact bank has no remaining positive PF route left open”
- “the current bank is fully closed negatively for a positive global sole-axiom PF selector theorem”

Those are branch-wide theorem-grade claims. On this repo, the primary runner
needs to verify the mathematics or object-level reductions directly, not just
verify that earlier notes say the right words.

### 2. Several “frontier certificate” runners only prove toy generic lemmas, then promote note conclusions

The layer just below the umbrella runners is also not yet at theorem-runner
grade for `main`.

Representative pattern:

- the Wilson `1+1` certificate script proves a generic fact using a toy
  Hermitian `3x3` matrix `h` with `b = h.copy()`, then checks note strings;
  it does **not** certify the actual Wilson objects `B_e`, `H_e`, or the
  branch’s concrete compressed route.
- the PMNS scalar discriminant script proves a generic positive-definiteness
  fact for a hand-built two-angle matrix, then checks note strings; it does
  **not** certify the branch’s actual PMNS-native production object.
- the plaquette first-Hankel script proves a generic equivalence between
  `(m_1, m_2)`, `H_1`, and `Delta_1` using made-up witness matrices, then
  checks note strings; it does **not** certify the actual propagated retained
  triple or the branch’s concrete plaquette data.

That is good scaffolding math, but it does not justify promoting the resulting
branch-wide closures as exact current-bank theorems.

### 3. The branch creates a large new authority surface without weaving it into the repo truth surfaces

This branch adds a very large root-level theorem stack:

- 100+ new `docs/PERRON_FROBENIUS_*`, plaquette-PF, and PMNS-PF notes
- matching frontier scripts

But it does **not** update the repo’s publication / truth-control surfaces:

- no `docs/publication/ci3_z3/PUBLICATION_MATRIX.md`
- no `DERIVATION_ATLAS.md`
- no `DERIVATION_VALIDATION_MAP.md`
- no `CLAIMS_TABLE.md`
- no `RESULTS_INDEX.md`
- no `EXTERNAL_REVIEWER_GUIDE.md`
- no package/root README wiring

So even if some subset of the science were acceptable, this branch still is not
packaged for `main`. As-is it creates a competing root-level authority surface
outside the package control plane.

## What I Do Think Is Real Here

There is real salvageable science in this branch:

- the route-decomposition work
- the exact negative / nonrealization / insufficiency statements
- the constructive narrowing of the Wilson / PMNS / plaquette frontiers

Those are worth keeping.

But they need to be split apart and promoted honestly:

1. keep or land lower-level exact notes whose runners actually certify the
   branch objects they discuss
2. downgrade or remove umbrella “current-bank full closure” notes until they
   have real object-level verifiers
3. if anything is promoted to `main`, weave only the accepted subset through
   the publication matrix / atlas / validation map / reviewer guide

## Best Outcome From Here

The fastest honest path is **not** to land this whole branch.

It is:

1. treat this as a science-review / work-history branch
2. identify the small number of lower-level notes with genuine computational
   backing
3. rebuild the top PF lane from those accepted pieces with real theorem
   runners
4. only then package the accepted subset through the repo truth surfaces

## Bottom Line

This branch is not ready for `main`.

The strongest blocker is evidentiary:

- the top-level PF closures are currently certified by note-audit scripts and
  toy generic reductions, not by branch-object theorem verification

So my recommendation is:

- **do not land this branch as-is**
- **keep it as a review / salvage source**
- **promote individual lower-level results later, one by one, once their
  runners certify the actual branch objects and the accepted subset is wired
  through the package surfaces**
