# Overnight Work Backlog

**Date:** 2026-04-03  
**Status:** conservative overnight priority note

This note is the short-horizon backlog for the next pass through the science
program. It is intentionally conservative: prefer the clearest retained
follow-ups, keep the flagship mirror lane in front, and avoid broadening scope
before the current bridges are tightened.

## Priority order

1. **Mirror-vs-lattice synthesis**
   - Keep the exact mirror lane as the flagship program line.
   - Treat lattice as the strongest secondary branch, not the primary story.
   - Use this synthesis to keep the repo narrative aligned before adding more
     frontier claims.
   - Deliverable:
     - one canonical comparison note that uses only retained artifact chains
     - one short recommended wording block for project-level synthesis

2. **NN continuum hardening**
   - Tighten the NN continuum story so the retained behavior is less tied to a
     single discrete regime.
   - Focus on the cleanest scaling and robustness checks first.
   - Keep this in the secondary/frontier bucket unless the evidence clearly
     graduates.
   - Deliverables:
     - freeze the raw-NN vs deterministic-rescale comparison cleanly
     - reconcile any mismatch between branch-history claims and on-disk notes
     - do not promote a continuum theorem unless the RG side is also canonical

3. **RG reconciliation**
   - Reconcile the RG-facing interpretation with the retained observables.
   - Prefer the smallest consistent bridge over speculative extrapolation.
   - Flag any mismatch explicitly rather than smoothing it over.
   - Deliverables:
     - one alpha-sweep reconciliation note
     - one decision on whether `alpha = 1.5` or `alpha = 2.0` is actually
       artifact-backed in this checkout
     - one narrow recommendation on whether RG is "open", "suggestive", or
       "retained on a bounded window"

4. **Light-cone follow-up**
   - Continue only the follow-up pieces that sharpen the existing light-cone
     picture.
   - Keep the work bounded and diagnostic.
   - Do not widen the scope into a new subprogram unless a clear retained gap
     demands it.
   - Deliverables:
     - one script/log/note chain or one clean negative closure
     - explicit distinction between topological light-cone claims and any
       stronger emergent-relativity language

5. **Generated-symmetry bridge**
   - Push the generated-symmetry line only as a bridge, not as a replacement
     for the flagship mirror story.
   - Treat it as frontier work that should remain grounded in the retained
     mirror/lattice evidence.
   - Deliverables:
     - only bounded Born-safe probes
     - no broad search unless a specific local rule is being tested

## Program stance

- **Flagship:** mirror
- **Secondary / frontier:** lattice and NN
- **Overnight bias:** harden what is already retained before expanding the
  claim surface

## Worker rules

- Use the standard linear propagator only.
- Every promoted claim needs one script, one log, and one note.
- If a result only exists in commit-message narrative, treat it as unretained
  until the artifact chain exists on disk.
- Do not let lattice/NN wording displace the flagship mirror lane unless a
  stronger retained comparison note actually supports it.

## Working rule

If a task does not clearly improve the retained mirror story, the lattice/NN
bridge, or the coherence of the program map, defer it to the next pass.
