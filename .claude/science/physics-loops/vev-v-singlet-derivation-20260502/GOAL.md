# GOAL — VEV V-Singlet Derivation Campaign

**Slug:** `vev-v-singlet-derivation-20260502`
**Date launched:** 2026-05-02
**Mode:** campaign (12h budget, literature allowed)
**Source-note authority:** branch-local; later audit lane decides ratified status

## Net call

The user's net-call assessment (frozen here as the science framing):

> Three things would shift this from "structural-consistency framework" to "yes,
> new physics":
>
> 1. **H1.** Close the plaquette ⟨P⟩(β=6) = 0.5934 analytically (not MC).
> 2. **H2.** Derive the structural integers (k_A=7, k_B=8, the 7/8, the 16) from
>    a single underlying principle rather than separate counting arguments.
> 3. A non-SM prediction.

H2 is reachable in days–weeks. H1 is a famous open lattice problem (~6 months
optimistically, decades for the strong form).

## Campaign target

**Primary (H2 reformulation):** Reformulate the load-bearing observable in
the v-derivation chain as the V=Z₂×Z₂-invariant free-energy density f_vac on
the minimal Klein-four APBC block, retiring bridges 1-3 of the 5-bridge audit
on `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` (cycle 8 of audit-backlog,
PR #267):

| Bridge | Original status | Under H2 reformulation |
|---|---|---|
| (1) scalar additivity `W[J_1⊕J_2] = W[J_1]+W[J_2]` | admitted | retires to **extensivity** (intensive `f_vac` per spacetime volume) |
| (2) CPT-even phase blindness `W` depends on \|Z\| | admitted | retires to **real-positive Z** (staggered det D positive on real masses) |
| (3) continuity (regularity for functional equation) | admitted | retires to **analyticity of Z[J] in J** (standard finite-dimensional Grassmann) |
| (4) normalization choice | admitted | unchanged (or retires to natural zero) |
| (5) hierarchy baseline import (M_Pl·α_LM^16) | admitted | unchanged — separate lane |

The reformulation REPLACES the W = log\|det(D+J)\| - log\|det D\| route with a
direct claim about f_vac and its V-singlet source curvature. The (7/8)^(1/4) =
(A_2/A_4)^(1/4) factor follows exactly from the existing kernel ratio, but
without admitting bridges 1-3 as load-bearing.

**Side benefit:** the m_H paradox dissolves into a representation-theoretic
distinction. m_H is the curvature at the **minimum** of V_eff (which is
V-broken once EWSB happens), while v is set by the curvature at the
**origin** (V-singlet vacuum). Different observables, different selectors.

## Secondary (H1 Route 2 cheap probe)

If H2 lands cleanly, attempt the Cl(3) + Klein-four counting probe for β=6:
does the framework's algebraic structure force β=6 (i.e., g_bare²=1) from
group-theoretic counting alone? Half-day attempt. Likely no-go but cheap.

## Tertiary (H1 Route 1 deep stretch, runtime permitting)

Self-consistent saddle on the minimal Klein-four block for ⟨P⟩(β=6).
Already partially closed by the bridge-support stack (Perron solves give
P(6) = 0.4524 to 0.4225 depending on environment input). Hard step:
minimal-block-equals-bulk on the V-invariant subspace.

## Stop conditions

- Runtime exhaustion (12h)
- Volume cap reached (5 PRs / 24h)
- Cluster cap reached (2 PRs per parent-row family)
- Corollary exhaustion (no new load-bearing premise, residual, or stretch
  remains)
- Value-gate exhaustion (V1-V5 fail on every remaining queue item)
- Required tooling unavailable for every viable route

## Forbidden imports

- PDG `v_meas = 246.22 GeV` as derivation input (comparator only)
- Lattice-MC `⟨P⟩ = 0.5934` as a *retained* input (it is bounded same-surface)
- Hierarchy baseline `M_Pl·α_LM^16 = 254.6432` as derivation input (admitted)
- Any (7/8)^(1/4) hard-coded into the runner — the runner must DERIVE the
  ratio from kernel sums, not assert it
- Any consistency-equality dressed as derivation (per memory feedback
  `consistency_vs_derivation_below_w2.md`)
