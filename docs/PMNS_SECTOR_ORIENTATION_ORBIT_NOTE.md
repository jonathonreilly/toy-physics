# PMNS Sector-Orientation Orbit Reduction

**Date:** 2026-04-15
**Status:** support - structural or confirmatory support note
freedom of the non-universal one-sided PMNS surface
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_sector_orientation_orbit.py`

## Question

After the current exact bank isolates the minimal PMNS-producing branches, what
exact discrete freedom is still left on the non-universal one-sided surface?

## Bottom line

The residual one-sided PMNS problem is smaller than “pick a branch.”

On the non-universal surface, the current bank already fixes the unordered core

`{single-offset monomial lane, two-offset canonical lane}`.

What remains is only one discrete orientation bit

`tau in Z_2`

choosing whether the two-offset canonical lane is realized on:

- `Y_nu`, with `Y_e` still monomial, or
- `Y_e`, with `Y_nu` still monomial.

So the missing selector is no longer a local texture classifier. It is an
**oriented inter-sector bridge**.

## Atlas and package inputs

This theorem reuses:

- `PMNS minimal-branch nonselection`
- `Lepton shared-Higgs universality underdetermination`
- `PMNS selector-bank nonrealization`

And, from the GR atlas bank as reusable structural framing:

- `Universal A1 invariant section`
- `Universal GR polarization-frame bundle blocker`

The GR import is not a dynamics import. It is a safe structural reuse: the GR
bank already isolates the pattern “exact invariant core without a canonical
complementary section.” The lepton PMNS lane now exhibits the same exact shape.

## Why this is an exact theorem

The exact bank already proves:

1. the one-sided minimal PMNS branches exist
2. the two surviving one-sided branches are canonical
3. no retained bridge theorem selects among them
4. no existing selector row in the atlas secretly realizes the missing branch
   selector

So there is one more reduction available:

- once the unordered support core is fixed, the only remaining non-universal
  difference is sector orientation.

## The theorem-level statement

**Theorem (Reduction of the non-universal one-sided PMNS surface to a
sector-orientation orbit).**
Assume the exact minimal PMNS-branch nonselection theorem, the exact
shared-Higgs universality underdetermination theorem, and the exact
selector-bank nonrealization theorem. Then on the non-universal one-sided
minimal PMNS surface:

1. the current exact bank fixes the unordered support core consisting of one
   single-offset monomial lane and one two-offset canonical lane
2. there are exactly two oriented realizations of that core, obtained by
   placing the two-offset lane on `Y_nu` or on `Y_e`
3. the current atlas contains no retained oriented inter-sector bridge theorem
   selecting between those two realizations

Therefore the residual non-universal discrete freedom is exactly one
sector-orientation bit `tau in Z_2`.

## What this closes

This closes one more layer of the finish-line ambiguity.

It is now exact that the remaining non-universal selector problem is not:

- another local support-family classification
- another canonical reduction problem
- another hidden selector already sitting in the atlas

It is instead:

- an inter-sector universality theorem, or
- an inter-sector orientation bridge after universality failure, or
- a stronger impossibility theorem ruling that out

## What this does not close

This note does **not** prove:

- that shared-Higgs universality is true
- that shared-Higgs universality fails
- that `Y_nu` must be the active two-Higgs lane
- that `Y_e` must be the active two-Higgs lane
- any positive coefficient derivation on either surviving branch

It is a current-bank reduction theorem only.

## Command

```bash
python3 scripts/frontier_pmns_sector_orientation_orbit.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `publication/ci3_z3/DERIVATION_ATLAS.md` (publication aggregator; backticked to avoid length-2 cycle — citation graph direction is *atlas → this_note*)
- [pmns_minimal_branch_nonselection_note](PMNS_MINIMAL_BRANCH_NONSELECTION_NOTE.md)
- [lepton_shared_higgs_universality_underdetermination_note](LEPTON_SHARED_HIGGS_UNIVERSALITY_UNDERDETERMINATION_NOTE.md)
- [pmns_selector_bank_nonrealization_note](PMNS_SELECTOR_BANK_NONREALIZATION_NOTE.md)
- [universal_gr_a1_invariant_section_note](UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md)
- [universal_gr_polarization_frame_bundle_blocker_note](UNIVERSAL_GR_POLARIZATION_FRAME_BUNDLE_BLOCKER_NOTE.md)
