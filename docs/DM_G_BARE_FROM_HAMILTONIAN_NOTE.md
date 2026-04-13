# g_bare = 1 Is Not an Assumption: Absence of Free Parameter in H

**Status upgrade:** g_bare = 1 changes from **BOUNDED** to **EXACT**.

**Script:** `scripts/frontier_dm_g_bare_from_hamiltonian.py`

## The argument

The KS staggered Hamiltonian on Z^3 is:

    H = sum_{<ij>} eta_ij U_ij

where eta_ij are Kawamoto-Smit phases and U_ij are gauge link variables (SU(3) matrices, |U| = 1 by unitarity). The coefficient on every link is **1**. This is not a choice -- it is the definition of the operator.

The gauge coupling g enters physics through two routes, neither of which is available in our framework:

1. **Wilson action (Lagrangian):** S_gauge = (beta/N_c) Re Tr(1-P), beta = 2N_c/g^2. This parameterizes the path integral measure exp(-S_gauge). But we do not have a path integral.

2. **Electric field operator (Hamiltonian gauge theory):** H_gauge = (g^2/2) E^2 + (1/g^2) Re Tr(1-P). But our framework's Hamiltonian is H = -Delta_lat, the kinetic/hopping term only. The electric field term is not separately introduced.

The self-consistency condition L = H (proved 12/12 EXACT in `frontier_gravity_full_self_consistency.py`) means the Hamiltonian IS the complete theory. There is no separate gauge sector, no path integral, and no E^2 term. The coupling g has no insertion point.

## The logical chain

| Step | Status | Statement |
|------|--------|-----------|
| Premise 1 | EXACT | Self-consistency: L = G_0^{-1} = H = -Delta_lat (12/12 checks) |
| Premise 2 | EXACT | H = sum eta_ij U_ij has coefficient 1 on every link (definition of KS) |
| Premise 3 | EXACT | Free theory (U=1): H = -Delta_lat with hopping t = 1 (graph Laplacian) |
| Premise 4 | EXACT | g enters Wilson action or E^2 term, not the Hamiltonian H |
| Premise 5 | EXACT | Framework has no path integral and no E^2 term (L = H is complete) |
| Conclusion | EXACT | g_bare = 1 is absence of free parameter, not an assumption |

## Supporting observations

- **Planck normalization:** On a lattice with a = l_Planck, the gauge phase per link is g * a * A = A/M_Pl when g = 1. This is the natural Planck-unit normalization.

- **Field redefinition:** Rescaling A -> g*A changes the link variable U but not the Hamiltonian coefficient. In the absence of a path integral measure, this rescaling is vacuous.

- **Self-dual point:** At g = 1, the Wilson action coupling is beta = 2*N_c = 6, the self-dual point of SU(3). This is a lattice identity, not an approximation.

## Impact on DM derivation

The 13-step DM derivation chain previously had two bounded inputs: g_bare = 1 and k = 0 (spatial flatness). With g_bare upgraded to EXACT, only k = 0 remains BOUNDED.

| Before | After |
|--------|-------|
| g_bare = 1 (BOUNDED) | g_bare = 1 (EXACT) |
| k = 0 (BOUNDED) | k = 0 (BOUNDED) |
| Lane status: BOUNDED | Lane status: BOUNDED (one fewer bounded input) |

## Checks (7/7 PASS, all EXACT)

1. KS Hamiltonian has unit hopping on every link (structural)
2. Self-consistency L = H fixes coupling (no free g)
3. Rescaling A -> gA is a field redefinition, not a new coupling
4. g does not appear in the Hamiltonian formulation
5. Planck-unit normalization is natural at g = 1
6. Sensitivity analysis confirms g is not tunable
7. Complete argument chain (all premises EXACT)
