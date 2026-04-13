# Graph-Canonical Right-Handed Boundary Theorem

**Script:** `scripts/frontier_graph_canonical_rh_boundary.py`
**Status:** boundary theorem verified; right-handed singlet template remains open

## What survives

The strongest paper-safe statement supported by the current 3D/4D chain is:

> 3D graph/taste structure canonically gives the left-handed gauge algebra,
> the left-handed matter quantum numbers, and the graph-canonical CPT /
> Dirac-sea antiparticle structure.  
> 4D physical spacetime supplies chirality via `gamma_5`, and therefore the
> SU(2)-singlet right-handed sector.  
> Given the 4D singlet template and `nu_R = 0`, anomaly cancellation
> uniquely fixes the right-handed hypercharges.

This is paper-safe.

## What is graph-canonical

- The 3D KS surface gives the left-handed gauge algebra on `C^8`.
- The 3D Clifford algebra is real, so complex conjugation is a symmetry.
- Bipartite parity gives particle-hole symmetry and the Dirac-sea doubling.
- These pieces are graph-canonical in the sense used by the current repo.

## What is not graph-canonical

- The SU(2)-singlet right-handed template.
- The full chirality split into `C^8_L` and `C^8_R`.
- The neutral-neutrino input `nu_R = 0` used to make the anomaly solution
  unique.

## Exact blocker

The 3D surface does not canonically produce SU(2) singlets.  On the 3D
surface, the SU(2) action leaves all eight states in doublets.  The
right-handed singlet sector therefore requires the additional 4D chirality
operator `gamma_5`.

## Open theorem

The remaining theorem is the graph-canonical derivation of the right-handed
singlet template itself.  Until that exists, the correct paper statement is
the boundary theorem above, not a full graph-only right-handed derivation.
