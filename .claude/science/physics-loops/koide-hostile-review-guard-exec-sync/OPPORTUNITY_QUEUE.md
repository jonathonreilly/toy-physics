# Opportunity Queue

1. Koide hostile-review guard executable script-output verification.
   - Status: completed in this block.
   - Landability: high; narrow runner and note patch.

2. Independent audit of `koide_hostile_review_guard_note_2026-04-24`.
   - Status: pending outside this author branch.
   - Needed to decide audited-clean vs further failure.

3. Optional future hardening: require all target no-go runners to exit zero
   after emitting their labels, if the repository decides that should become a
   guard invariant.
   - Status: deliberately not included here because it is stronger than the
     prompt's stated repair target.
