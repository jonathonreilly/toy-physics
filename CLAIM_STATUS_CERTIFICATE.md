# Claim Status Certificate — Cycle 4 of v-scale-planck-convention campaign

**Date:** 2026-05-10
**Campaign slug:** v-scale-planck-convention
**Cycle:** 4
**Branch:** physics-loop/v-scale-t2-gamma-norm-20260510
**Base:** origin/main

## Cycle goal (as briefed)

> Attempt to derive T2 — "the per-determinant geometric-mean readout
> `v ∝ |det(D)|^{1/(N_taste · L_t)}` is forced by the Cl(3) γ-norm
> structure, not admitted" — and then provide a synthesis sketch (T3)
> tying T1+T2 to the v formula.

## Verdict (honest)

### T2 (γ-norm → per-determinant geometric-mean readout): **NO-GO** at the
**advertised scope**, but a **NARROW POSITIVE THEOREM** salvaged at
reduced scope.

The Cl(3) γ-involution identity `|M|_γ = √|det(M)|` for `M ∈ M_2(C) ≅
Cl(3,0)` is **exact** (verified algebraically and numerically at exact
rational precision). However, this identity applies to **per-element**
γ-norms on single 2×2 matrices; it does **not** force the framework's
**per-determinant geometric-mean readout** `v(L_t) ∝ |det(D + J)|^{1/(N_taste
· L_t)}` on the lattice. The exponent `1/(N_taste · L_t)` is a
reciprocal mode-count fact on the tensor-product lattice, not a Cl(3)
γ-norm fact.

**What is salvaged as positive_theorem:** the abstract algebraic
content (G1)-(G3) of the γ-involution `γ(M) = σ_2 M^T σ_2`:

- (G1) γ = symplectic adjoint (cofactor transpose);
- (G2)/(G2') `|M|_γ = √|det(M)|` per-element identity;
- (G3) γ acts with grade signs `(+, -, -, -, -, -, -, +)` on the
  Pauli realisation.

The note carries (G4) as an **explicit boundary disclaimer**: per-element
γ-norm does NOT close the per-determinant geometric-mean readout
admission of the heat-kernel note §4.3.

**Source note created:**
`docs/CL3_GAMMA_INVOLUTION_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-10.md`
`scripts/frontier_cl3_gamma_involution_determinant_narrow.py`
Runner: `PASS=8 FAIL=0`.

### T3 (synthesis sketch v = M_Pl · (7/8)^{1/4} · α_LM^16): **roadmap drafted**

Written as `docs/V_SCALE_PLANCK_CONVENTION_SYNTHESIS_ROADMAP_NOTE_2026-05-10.md`
with `Claim type: meta` and `proposal_allowed: false`. Records the
expected chain (T1, T2, etc.) and **explicitly does NOT** claim closure
or load-bearing synthesis. The constituents T1 (`L_t=4` Klein-four
uniformity, on branch `science/lt4-klein-four-sin-squared-uniformity-narrow-2026-05-10`)
and T2 (this branch's narrow positive theorem) are themselves
`unaudited` source-note proposals, so T3 stands explicitly as a
forward-looking roadmap, not as a load-bearing closure.

## Honest claim type & status

- T2 narrow note: `Claim type: positive_theorem` (the abstract algebraic
  identities (G1)-(G3) are class-(A) algebra on `M_2(C)`).
  - **NOT a closure of the per-determinant readout admission.**
  - `Status authority: independent audit lane only.`
  - No bare `retained`/`promoted`. `audit_required_before_effective_status_change: true`.
- T3 synthesis: `Claim type: meta` (synthesis roadmap; not a new
  derivation).
  - `Status authority: independent audit lane only.`
  - `proposal_allowed: false` (no audit verdict requested; this is a
    forward-looking sketch).

## V1-V5 answers (written record)

### V1 — Does the cycle attempt a real derivation, or rehearse known facts?

The cycle attempts a real derivation: whether the Cl(3) γ-involution
structure on `M_2(C)` forces the framework's per-determinant
geometric-mean readout via the identity `|M|_γ = √|det(M)|`.

The honest finding is that the identity is **exact** at the
**per-element level** but **does not lift** to the framework's lattice
determinant readout. This is a substantive negative finding (a
no-go-at-advertised-scope plus a narrow positive salvage), not a
rehearsal of known facts. The narrow theorem (G1)-(G4) provides a
single class-(A) algebraic statement that the audit lane can ratify
independently.

### V2 — Is the load-bearing step class-(A)/(B)/(C)?

Class (A) — algebraic identity on `M_2(C)` ≅ `Cl(3,0)`. The
load-bearing computation is symbolic matrix arithmetic verified at
exact rational precision (and `PASS=8 FAIL=0` on the runner). No
admitted physics conventions, no PDG values, no fitted coefficients.
The single one-hop dependency (the sibling complexification-split
narrow theorem K2 for `Cl(3,0) ≅ M_2(C)`) is itself class-(A) abstract
algebra.

### V3 — Could the audit lane already complete this derivation from
existing retained primitives + standard math machinery?

The identity `|M|_γ = √|det(M)|` for `M ∈ M_2(C)` is standard matrix
algebra (the cofactor identity `M · adj(M) = det(M) · I_2` combined
with the symplectic adjoint structure `σ_2 M^T σ_2 = adj(M)` for
`2 × 2`). The audit lane could indeed derive (G1)-(G3) from standard
mathematics + the sibling K2 isomorphism without this note.

**The non-trivial framework-specific content is the BOUNDARY (G4).**
The literature does not record the explicit statement that "the Cl(3)
γ-norm identity does **not** close the per-determinant geometric-mean
readout admission". That boundary is what the cycle adds: it
**falsifies** a plausible-sounding closure conjecture in the campaign
brief, by demonstrating numerically (the runner's Part 8 hopping-block
example with gap `-27/16`) that determinants of non-block-diagonal
lattice operators are **not** products of per-block γ-norms.

So the cycle's content is: standard algebra (G1)-(G3), recorded for
single-note audit ratification ease, plus the explicit no-go boundary
(G4) that retires a plausible-sounding closure path. This boundary is
the non-trivial cycle content; without (G4), a future agent could
mis-attribute the per-determinant readout admission to "the γ-norm
identity I checked is exact, so the readout must follow". The cycle
forecloses this mistake.

### V4 — Status discipline

The narrow note carries:
- `Claim type: positive_theorem` for (G1)-(G3) abstract algebra;
- `Status authority: independent audit lane only`;
- No bare `retained` / `promoted`;
- Forbidden-imports check passes;
- `(G4)` explicit boundary disclaimer that the readout admission is
  **NOT** retired by this note.

The synthesis roadmap (T3) carries:
- `Claim type: meta`;
- `proposal_allowed: false`;
- Honest forward-looking shape, no closure claim.

Both notes use repo-canonical vocabulary only (Cl(3) γ-involution,
symplectic adjoint, cofactor transpose, per-determinant readout) and
mirror the existing template `CL3_COMPLEXIFICATION_SPLIT_NARROW_THEOREM_NOTE_2026-05-10.md`
structure.

### V5 — Closest prior cycle, distinction from it

**Closest prior cycle:** Cycle 3 of the same campaign produced
`HIERARCHY_LT4_KLEIN_FOUR_SIN_SQUARED_UNIFORMITY_NARROW_THEOREM_NOTE_2026-05-10`
(branch `science/lt4-klein-four-sin-squared-uniformity-narrow-2026-05-10`,
commit `f01fd5e37`) which carries the T1 claim: `L_t = 4` Klein-four
sin² uniformity as a narrow trigonometric identity. That cycle's
content is the temporal mode-set structure at `L_s = 2`, not the
γ-norm-to-determinant readout question.

**Distinction:**
- Cycle 3 (T1) closes the **temporal block selection** (`L_t = 4` is
  the unique non-trivial sin²-uniform Matsubara block in scanned
  range), a trigonometric / group-orbit fact independent of any γ-norm
  or Cl(3) algebra content.
- Cycle 4 (this cycle, T2) attempts the **geometric-mean readout** via
  γ-norm. Result: the per-element γ-norm identity `|M|_γ = √|det(M)|`
  is exact in `M_2(C)`, but the **lattice determinant readout** does
  **not** follow from it. The narrow positive (G1)-(G3) records the
  abstract γ-involution identity; (G4) records the no-go boundary.

The two cycles share **no load-bearing steps** and do **not** consume
each other's effective statuses. The synthesis roadmap (T3) names both
as constituents but does not consume their effective statuses; it
explicitly stands as a forward-looking sketch.

There is also no prior "γ-norm sketch" note in the campaign — a search
of `docs/` for keywords `gamma_norm`, `γ-norm`, `Clifford conjugation`,
`gamma_involution`, `symplectic adjoint`, `γ(M)`, `gamma(M)`, etc.
returned zero hits. The narrow note created by this cycle is the
first formal record of the `Cl(3)` γ-involution determinant identity
on the framework's source surface.

## Files touched / created on this branch

- `docs/CL3_GAMMA_INVOLUTION_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-10.md` (new)
- `scripts/frontier_cl3_gamma_involution_determinant_narrow.py` (new)
- `logs/runner-cache/frontier_cl3_gamma_involution_determinant_narrow.txt` (new)
- `docs/V_SCALE_PLANCK_CONVENTION_SYNTHESIS_ROADMAP_NOTE_2026-05-10.md` (new, T3 roadmap)
- `CLAIM_STATUS_CERTIFICATE.md` (this file, new at repo root)

## Cited authorities and their live ledger statuses

| Authority | Cycle role | Live ledger status (2026-05-10) |
|---|---|---|
| `cl3_complexification_split_narrow_theorem_note_2026-05-10` | one-hop markdown-link dep for K2 isomorphism | unaudited / positive_theorem |
| `hierarchy_heat_kernel_d4_compression_bounded_theorem_note_2026-05-10` | named target of (G4) boundary | unaudited / bounded_theorem |
| `hierarchy_bosonic_bilinear_selector_note` | reader pointer; named in narrow note | unaudited / bounded_theorem |
| `hierarchy_matsubara_decomposition_note` | reader pointer | retained / positive_theorem |
| `cpt_exact_note` | reader pointer | unaudited / positive_theorem |
| `cl3_faithful_irrep_dim_two_narrow_theorem_note_2026-05-10` | reader pointer | unaudited / positive_theorem |

All citations are honest about the live ledger statuses. The
load-bearing markdown-link upstream (cl3 complexification split) is
itself unaudited; downstream consumers of this narrow note inherit
that conditional shape.

## Runner result

`scripts/frontier_cl3_gamma_involution_determinant_narrow.py`:
- 8 test parts
- `PASS=8 FAIL=0` at exact symbolic / rational precision
- Cache: `logs/runner-cache/frontier_cl3_gamma_involution_determinant_narrow.txt`

## Audit handoff

- **Proposed claim type:** positive_theorem (abstract algebra (G1)-(G3))
- **Proposed claim scope:** narrow algebraic identities about the
  Cl(3) γ-involution `γ(M) = σ_2 M^T σ_2` on `M_2(C) ≅ Cl(3,0)`:
  symplectic adjoint (G1), γ-norm = √|det| (G2/G2'), grade-action (G3),
  plus explicit boundary (G4) that this does NOT close the
  per-determinant geometric-mean readout admission of the heat-kernel
  note §4.3.
- **Proposed load-bearing step class:** A (abstract algebra on
  `M_2(C)`).
- **Status authority:** independent audit lane only.
- **Forbidden imports used:** false.
- **Proposal allowed:** true (single one-hop dep is sibling narrow
  theorem; status authority pipeline-derived).
- **Audit required before effective status change:** true.
