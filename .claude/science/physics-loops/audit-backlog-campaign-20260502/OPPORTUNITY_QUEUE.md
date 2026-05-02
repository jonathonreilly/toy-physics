# Opportunity Queue — Audit Backlog Retained Campaign

**Last refresh:** 2026-05-02 (post cycle 1)

## Methodology

Candidates mined from `docs/audit/data/audit_ledger.json` and ranked by:

```
rank = blast_radius_score + dep_clean_score + named_residual_score + audit_state_score
```

where:
- blast_radius_score: 0–10 from min(transitive_descendants, 500)/50
- dep_clean_score: 0–5 from fraction of deps with retained-grade effective
  status × 5
- named_residual_score: +3 if verdict names a specific repair target with candidate retained chain
- audit_state_score: +2 if proposed_retained, +1 if audited_conditional

## Cycle 1 Output (closed)

- **physics-loop/rh-sector-anomaly-cancellation-block01-20260502** — PR #254
  - Closes (R-A,B,C) of LHCM verdict residuals as exact Fraction identities
  - Status: exact-support; PASS=41/0; certificate: proposal_allowed=false (Criterion 4 fails)

## Top 12 Active Queue (refreshed)

| # | Candidate | td | dep_clean | rank | Cycle target | Status hypothesis |
|--:|---|--:|--:|--:|---|---|
| 1 | left_handed_charge_matching_note → repair item (1) matter assignment | 267 | 1.00 | 16.34 | derive Sym²(3)=quark, Anti²(1)=lepton from SU(3) rep content on graph-first surface | exact-support; would narrow LHCM to single residual (item 2) |
| 2 | three_generation_observable_theorem_note | 302 | 0.60 | 15.04 | audit/repair multiple conditional upstream theorems | conditional → support |
| 3 | observable_principle_from_axiom_note | 294 | 1.00 | 14.88 | derive scalar-source rule from bare axioms | unclear; may demote |
| 4 | gauge_vacuum_plaquette_constant_lift_obstruction_note | 267 | 1.00 | 14.34 | derive β-dependent reduction law β_eff(β) at β=6 | hard residual; stretch attempt |
| 5 | gauge_scalar_temporal_completion_theorem_note | 266 | 1.00 | 14.32 | derive interacting plaquette → scalar source observable bridge | hard residual |
| 6 | yukawa_color_projection_theorem (M residual) | 265 | 1.00 | 14.30 | physical EW current → adjoint channel matching theorem | hard residual; stretch attempt |
| 7 | yt_color_projection_correction_note | 261 | 1.00 | 14.22 | derive R_conn = 8/9 bridge from CMT partition-function identity | hard residual |
| 8 | higgs_mass_from_axiom_note | 264 | 1.00 | 14.28 | derive scalar normalization theorem | hard residual |
| 9 | g_bare_derivation_note | 263 | 1.00 | 14.26 | identify canonical Cl(3) connection normalization with unit gauge coupling | hard residual; stretch attempt |
| 10 | physical_lattice_necessity_note | 301 | (deps=[]) | 17.02 | dep declaration repair / demotion | likely demotion |
| 11 | alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30 | 259 | 0.50 | 9.52+? | dep firewall — prove minimal_axioms not load-bearing | proposed_retained eligible if firewall closes |
| 12 | kubo_fam2_refinement_note | 1 | 0.00 (cyclic) | low blast | resolve cycle with kubo_continuum_limit_families_note | small cert candidate |

## Cycle 2 Selection: LHCM repair item (1) matter assignment

**Rationale:**
- Highest dep_clean (1.00) and named residual on top of cycle 1's surface.
- Builds on cycle 1's exact-support work narrowing LHCM verdict.
- Structural representation-theory derivation tractable in 30–60 min.
- Closes 2 of 5 LHCM repair items, leaving only item (2) Y normalization unclosed (deepest item, requires SM photon derivation).

**Forbidden imports:**
- PDG observed colors / charges
- Literature SU(3) representation tables (only as audit comparators)
- Hypercharge eigenvalues from HYPERCHARGE_IDENTIFICATION (independent derivation, not citation)
- Same-surface arguments

**Goal:** prove that on the graph-first selected-axis surface, the Sym²(C²)
subspace carries SU(3) fundamental (label "quark color"), and the Anti²(C²)
subspace carries SU(3) trivial representation (label "lepton, SU(3)-neutral").

**Expected status:** exact algebraic identity / support theorem on the
retained graph-first surface. Promotes LHCM repair item (1) from "admitted"
to "structurally derived modulo SM-definition labels."

## Cycles 3+ planned

- Cycle 3: stretch attempt on a hard residual (queue rank 4-9)
- Cycle 4: continuation of LHCM chain (item 2: Y normalization stretch attempt)
- Cycle 5+: pivot to fresh lane based on refreshed queue

## No-Go Memory (campaign so far)

(Empty — no routes have been attempted-and-failed yet)
