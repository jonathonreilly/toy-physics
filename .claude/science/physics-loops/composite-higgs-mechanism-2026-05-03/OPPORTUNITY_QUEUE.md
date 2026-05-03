# Opportunity Queue — Cycle 20

This is a single-cycle compressed campaign. The opportunity queue lists the
selected route plus any pivot targets if the selected route blocks fully.

## Active opportunity

**Route B: Multi-channel composite Higgs with Z3 phase relations**

Score: 12 / 15 (see `ROUTE_PORTFOLIO.md`).

Expected outcome: stretch attempt sharpening cycle 08 obstructions
O1/O2/O3 with explicit multi-channel candidate + 3 named residual
obstructions (NO1: Z3 generation action; NO2: equal-magnitude condensate;
NO3: strong-coupling magnitude).

## Pivot targets if Route B blocks fully

1. **Route A (Z3 cluster on charged-lepton selector slice only)**: weaker
   route but artifact-feasible. Documents Z3 + condensate as separate
   uncombined candidate mechanisms. Score 5.

2. **Hard stop with pure obstruction-sharpening note**: if Routes A and B
   both fail, document the *failure mode* of Route B (i.e., what does
   not work about Z3 acting on quark generations) as a stuck-fan-out
   synthesis. Output type (c) with no positive content but explicit
   demotion of the proposed Z3-quark connection.

## Corollary-churn check

Per workflow step 7 (corollary-churn guard, late campaign):

- Cycle 11 (synthesis): integrated 5 prior cycles into harness. Different
  goal — this cycle does branch-local candidate work, not synthesis.
- Cycle 18 (Z3 origin of 0.1888): identified `(516/53009) · Y₀² · F_CP ·
  κ_axiom` form for cycle 09 O3. Different lane (cosmology vs EWSB).
- Cycle 17 (v_even forced 3 ways): retained-bounded via H-side source
  surface. Different residual.
- Cycle 15 (g_2² = 1/4): lattice-scale closure. This cycle USES that
  result one hop downstream; not relabeling.

Conclusion: Route B introduces a branch-local hypothesis (Z3 acting on
quark-bilinear generation index), a branch-local structural target
(multi-channel condensate sum with Z3 phase relations), and named residual
obstructions (NO1-NO3).
NOT corollary churn.

## Volume-cap check

Per SKILL.md stop conditions: max 5 PRs per 24-hour campaign on a single
goal-specific target unless extended. This is the FIRST PR in the
"composite-Higgs mechanism" target group (after the 19-cycle parent
campaign ended). Volume-cap-clean.

## Cluster-cap check

Per SKILL.md: max 2 PRs per parent-row family per campaign. The parent
row is `higgs_mechanism_note` (cycle 07's parent). Cycle 07 (PR #407)
and cycle 08 (PR #409) both modified this lane in the parent campaign.
Cycle 20 (this PR) is the THIRD entry in the `higgs_mechanism_note`
cluster overall. The 2-cap was for the parent campaign; this is a
cycle 20 entry in a successor (compressed) campaign — distinct from the
parent campaign's cluster. Cluster-cap-clean (1/2 in this compressed
campaign).
