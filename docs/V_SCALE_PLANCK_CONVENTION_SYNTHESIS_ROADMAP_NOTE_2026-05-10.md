# v-Scale Planck Convention Synthesis Roadmap

**Date:** 2026-05-10
**Claim type:** meta
**Status authority:** independent audit lane only. This source note
does **not** request audit ratification; it is a forward-looking
roadmap that explicitly does NOT carry load-bearing closure content.
**Source-note proposal disclaimer:** `proposal_allowed: false`. No
audit verdict is requested or implied; this note catalogs in-flight
narrow sub-pieces of the v-scale-planck-convention campaign and
records the synthesis chain conditional on their future retention.

## 0. Purpose and scope discipline

This note is a **forward-looking sketch / roadmap** for the v-scale
campaign chain. It is **not** a synthesis closure of the formula
`v = M_Pl × α_LM^16 × (7/8)^(1/4)`. Per `feedback_meta_framings_backward_not_forward`,
synthesis notes that catalog already-audited narrow content may land
using repo-canonical vocabulary, but **forward-looking framings that
introduce closure scaffolding for not-yet-audited sub-pieces should
not claim load-bearing status**. Three of the four named sub-pieces
(T1, T2, the substep-4 ratchet) are currently `unaudited` source-note
proposals on separate branches. This roadmap records the synthesis
chain **conditional on their future retention** and stands as
forward-looking text only.

This note's `Claim type: meta` reflects that it is **not** a new
derivation. The audit lane is **not** asked to ratify a new theorem;
the load-bearing content lives in the constituent narrow notes
named below.

## 1. The campaign chain (forward-looking sketch)

The campaign aims to derive the framework's EWSB scale formula on the
retained surface as a fully-derived dimensionless ratio:

```text
v  =  M_Pl × α_LM^16 × (7/8)^(1/4)  ≈  246.28 GeV.                     (chain)
```

The campaign decomposes (chain) into named sub-pieces. The cycle 3 and
cycle 4 outputs of the campaign are the first two of these:

| Sub-piece | Content | Source note | Status (2026-05-10) |
|---|---|---|---|
| T1 | `L_t = 4` Klein-four sin² uniformity (trig + group-orbit) | `HIERARCHY_LT4_KLEIN_FOUR_SIN_SQUARED_UNIFORMITY_NARROW_THEOREM_NOTE_2026-05-10.md` (branch: science/lt4-klein-four-...; commit f01fd5e37) | unaudited (proposed positive_theorem); not yet on origin/main |
| T2 (this cycle) | Cl(3) γ-involution det identity (per-element) | `CL3_GAMMA_INVOLUTION_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-10.md` (this branch) | unaudited (proposed positive_theorem); narrow positive (G1)-(G3) salvaged from no-go on full T2 advertised scope |
| Anchor (7/8) | Riemann-Dirichlet triple coincidence at d=4 | `HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md` | unaudited (proposed positive_theorem) per live ledger row tag |
| Anchor (1/4) | Heat-kernel D=4 compression — bounded reframe of (1/4) exponent | `HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md` | unaudited (proposed bounded_theorem); admits per-det readout |
| Anchor α_LM | α_LM geometric mean identity | `ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md` | reclassified positive_theorem 2026-05-10 (per `efa6c9997`); live ledger pipeline-derived |
| Anchor decomposition | Matsubara product structure at L_s = 2 | `HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md` | retained / positive_theorem |
| Anchor selector | Bosonic-bilinear orbit closure for L_t = 4 | `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md` | unaudited / bounded_theorem |
| Anchor SSB observables | Observable principle from axiom | `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` | audited_conditional / bounded_theorem (conditional on P1) |

**Status of the chain as a whole (honest):** *not yet closed at
retained scope*. The bottleneck is the per-determinant geometric-mean
readout admission inside the heat-kernel note §4.3, which is recast
via Stefan-Boltzmann lineage but not derived from the framework's
primitive stack. Cycle 4 (T2) attempted to retire that admission via
Cl(3) γ-involution structure and found that the γ-norm identity
`|M|_γ = √|det(M)|` does **NOT** lift to the lattice readout (cf. the
narrow note's (G4) boundary).

## 2. What this roadmap does NOT claim

- Does **not** claim closure of the v-scale formula (chain).
- Does **not** consume any constituent's effective status as
  load-bearing on a new derivation in this note. The sub-pieces are
  named and their statuses are recorded as snapshots; this note does
  not derive anything new from them.
- Does **not** request audit ratification (`proposal_allowed:
  false`).
- Does **not** introduce new repo vocabulary. All sub-piece names
  are existing repo notes; the "v-scale-planck-convention" campaign
  slug is the campaign tag in `feedback_run_counterfactual_before_compute`
  / cycle log, not a new theorem vocabulary.

## 3. The expected synthesis (forward-looking, not load-bearing)

Conditional on **future** audit retention of:

- T1 (`L_t = 4` Klein-four trigonometric identity),
- the (7/8) Riemann-Dirichlet triple coincidence at d=4,
- the bilinear-selector closure of `L_t = 4`,
- the heat-kernel reframing of the (1/4) exponent (or a replacement
  derivation that retires the per-determinant readout admission),
- the α_LM geometric mean identity,
- the Matsubara product structure at `L_s = 2`,
- the observable principle from axiom (and its P1 admission, or a
  replacement that retires P1),

a future synthesis note could record the v-scale chain (chain) as a
ratified derivation. This roadmap names the chain but does **NOT**
itself ratify it.

## 4. Cycle 4 (T2) explicit no-go boundary

The campaign brief for cycle 4 advertised T2 as:

> "the per-determinant geometric-mean readout `v ∝ |det(D)|^{1/(N_taste
> · L_t)}` is forced by the Cl(3) γ-norm structure, not admitted."

Cycle 4 found that this advertised scope is **NOT** closed by the
Cl(3) γ-norm structure. The narrow positive theorem
`CL3_GAMMA_INVOLUTION_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-10.md`
records:

- (G1)-(G3): the abstract γ-involution algebraic identities on
  `M_2(C) ≅ Cl(3,0)` are exact;
- (G4): per-element γ-norm does NOT force the framework's lattice
  per-determinant geometric-mean readout. The `1/(N_taste · L_t)`
  exponent is a reciprocal mode-count fact on the tensor-product
  lattice, not a Cl(3)-algebra fact.

The per-determinant geometric-mean readout therefore **remains an
admission** in
`HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md`
§4.3, recast via Stefan-Boltzmann source lineage but not retired by
cycle 4's γ-norm attempt. Future cycles of the campaign that wish to
retire this admission must take a different route (candidate paths:
zeta-regularization on the tensor-product space; structural derivation
of `N_taste = 2^D` from the staggered-Dirac realization gate; an
independent heat-kernel argument tighter than the current
Stefan-Boltzmann support).

## 5. Cited authorities (one hop)

None load-bearing. This roadmap records snapshots of constituent
notes' statuses; it does not consume any of their effective statuses
in a derivation.

## 6. Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on the claim.
- No new repo vocabulary introduced.
- No load-bearing chain assembled from the named sub-pieces; the
  chain is forward-looking.
- This note is `Claim type: meta` (synthesis roadmap), `proposal_allowed:
  false`. No audit ratification requested.

## 7. Cross-references (plain-text reader pointers)

Plain-text reader pointers; not markdown links (so the citation-graph
builder does not parse them as upstream dependency edges):

- `CL3_GAMMA_INVOLUTION_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-10.md` — T2 narrow
  positive theorem produced by cycle 4 of this campaign.
- `HIERARCHY_LT4_KLEIN_FOUR_SIN_SQUARED_UNIFORMITY_NARROW_THEOREM_NOTE_2026-05-10.md`
  — T1 narrow positive theorem produced by cycle 3 of this campaign
  (currently on branch `science/lt4-klein-four-...`, not yet on
  origin/main).
- `HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md`
  — companion bounded theorem; its §4.3 per-determinant geometric-mean
  readout admission is the bottleneck T2 attempted to retire.
- `HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md`
  — (7/8) Riemann-Dirichlet triple coincidence anchor.
- `ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`
  — α_LM geometric mean anchor.
- `HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md` — Matsubara product
  structure retained authority.
- `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md` — bilinear-selector
  closure of L_t = 4.
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` — SSB observable principle
  (audited_conditional).
- `feedback_meta_framings_backward_not_forward` (memory entry,
  2026-05-08) — campaign-rule reference for forward-looking meta
  synthesis notes.

## 8. Citation-graph note

This roadmap has zero load-bearing markdown-link upstream
dependencies. All cross-references are plain-text reader pointers; no
note's effective status is consumed as load-bearing in any derivation
on this roadmap. The `meta` claim type and `proposal_allowed: false`
discipline match the campaign rule that forward-looking framings do
not load-bear on yet-to-be-audited sub-pieces.
