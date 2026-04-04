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

2. **3D dense spent-delay extension**
   - Keep the retained 3D dense spent-delay family fixed.
   - Use the gravity-observable hierarchy, not centroid alone.
   - The current canonical extension reaches `z = 6`; future passes should
     only try to push beyond that window or strengthen MI / decoherence
     without changing the action law.
   - Deliverables:
     - one bounded geometry-extension script/log/note chain
     - one decision on whether the current hierarchy-clean window can be
       pushed beyond `z = 6` on the same family

3. **NN continuum hardening**
   - Keep the NN story narrow and artifact-backed.
   - Prefer cleanup of companion-audit wording and stale claim surfaces over
     new speculative physics.
   - Deliverables:
     - tighten any remaining places where `k=0`, Born, or MI/purity are
       described too strongly on the NN branch
     - reconcile any mismatch between branch-history claims and on-disk notes
     - do not promote a continuum theorem unless the RG side is also canonical

4. **Action-power branch claim-surface cleanup**
   - Treat the action-power lane as a new branch with no inherited claims.
   - The 3D barrier signal issue is fixed enough to freeze a card, and the
     current ordered-family gravity-sign lane is now a bounded negative.
   - Focus on keeping the no-barrier Newtonian-style read and the barrier-card
     read clearly separated in the docs.
   - Deliverables:
     - one wording pass that keeps 3D no-barrier law claims from reading as
       same-harness closure
     - no new 3D sign-fishing unless the architecture changes topologically

5. **Repo claim-surface cleanup**
   - Reduce the gap between canonical notes and nearby exploratory files.
   - Focus on filenames and top-level docs that a new reader will see first.
   - Deliverables:
     - retire or relabel stale exploratory `*_test.py` files where practical
     - keep `README`, `START_HERE`, and the program notes synchronized

6. **Mirror-vs-lattice synthesis**
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
