# Overnight Work Backlog

**Date:** 2026-04-04  
**Status:** conservative overnight priority note

This note is the short-horizon backlog for the next pass through the science
program. It is intentionally conservative: prefer the clearest retained
follow-ups, keep the flagship mirror lane in front, and avoid broadening scope
before the current bridges are tightened.

## Priority order

1. **Structured bridge extension**
   - Keep the canonical mirror readout fixed.
   - Extend the retained structured chokepoint bridge without broadening into
     a new generator search.
   - Deliverables:
     - one bounded extension script/log/note chain
     - one clear decision on whether the bridge widens beyond the current
       narrow slice

2. **Action-power 3D barrier signal**
   - Treat the action-power lane as a new branch with no inherited claims.
   - Focus only on the blocker: getting enough 3D barrier signal to measure
     Born / MI / decoherence on the same family.
   - Deliverables:
     - one canonical 3D barrier harness script/log/note
     - one explicit pass/fail on whether the 3D power branch can support a
       full card instead of only no-barrier properties

3. **NN continuum hardening**
   - Keep the NN story narrow and artifact-backed.
   - Prefer cleanup of companion-audit wording and stale claim surfaces over
     new speculative physics.
   - Deliverables:
     - tighten any remaining places where `k=0`, Born, or MI/purity are
       described too strongly on the NN branch
     - reconcile any mismatch between branch-history claims and on-disk notes
     - do not promote a continuum theorem unless the RG side is also canonical

4. **Repo claim-surface cleanup**
   - Reduce the gap between canonical notes and nearby exploratory files.
   - Focus on filenames and top-level docs that a new reader will see first.
   - Deliverables:
     - retire or relabel stale exploratory `*_test.py` files where practical
     - keep `README`, `START_HERE`, and the program notes synchronized

5. **Mirror-vs-lattice synthesis**
   - Keep mirror as the flagship line.
   - Keep lattice / NN as secondary and frontier branches unless a stronger
     retained comparison note truly changes the ranking.
   - Deliverables:
     - one short wording pass whenever a new branch is promoted or demoted

## Program stance

- **Flagship:** mirror
- **Secondary:** ordered lattice
- **Frontier:** NN refinement and bounded axiom forks
- **Overnight bias:** harden what is already retained before expanding the
  claim surface

## Worker rules

- Use the standard linear propagator only.
- Every promoted claim needs one script, one log, and one note.
- If a result only exists in commit-message narrative, treat it as unretained
  until the artifact chain exists on disk.
- If a branch changes the action law, treat it as a new branch with no
  inherited flagship claims.
- Do not let lattice/NN wording displace the flagship mirror lane unless a
  stronger retained comparison note actually supports it.

## Working rule

If a task does not clearly improve the retained mirror story, the lattice/NN
bridge, or the coherence of the program map, defer it to the next pass.
