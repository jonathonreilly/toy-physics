# No-Go Discipline — Case Studies

Three archetypal failure modes from the 2026-05-10 v-scale-planck-convention
physics-loop campaign. Each shipped a negative claim that was later caught by
a stress-test review. Each is now the canonical example for one or more N1-N8
checks.

## F1 — Untested alternative route (Cycle 4, PR #1124)

**Claim shipped:** the Cl(3) γ-norm identity `|M|_γ = √|det(M)|` on
`M_2(C) ≅ Cl(3)` does NOT lift to the framework's lattice determinant
readout. The exponent `1/(N_taste · L_t)` was claimed to be "a reciprocal
mode-count fact, not a Cl(3)-algebra fact." The result was framed as a
**derived no-go**, not a bounded admission.

**What the agent tested:** per-element γ-norm on a 4×4 block-diagonal example.
With block-diagonal `D = M_1 ⊕ M_2`, `|det|^{1/2} = |M_1|_γ · |M_2|_γ` (a
per-block product). With off-diagonal hopping `H`, the determinant changes
by a gap (`-27/16` in the runner example) that the per-block product
cannot see. This was correctly observed.

**What the agent did not test:** the per-Matsubara-mode γ-norm. The framework's
own retained Matsubara note (`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02`)
gives the exact factorization
`|det(D + m)| = ∏_ω [m² + u_0²(3 + sin²ω)]^4`. This product structure IS a
per-mode decomposition, and the per-mode determinants ARE 4th powers, so a
per-mode application of `|M|_γ = √|det(M)|` would naturally produce the
exponent `1/(4 L_t) = 1/(N_taste · L_t)` at the spatial-corner block. The
agent's runner did not compare `(∏_ω |M_ω|_γ)^{1/N_modes}` against the
framework's readout. This route was untested but ruled out by phrasing.

**Why the rhetoric was over-broad:** the agent said `N_taste · L_t` is "not
a Cl(3)-algebra fact." But `N_taste = 2^d` comes from `CL3_FAITHFUL_IRREP_DIM_TWO`
(Cl(3) per-site algebra dim 2) raised to the spatial Z³ dimension; `L_t = 4`
is selected by the Klein-four orbit on the staggered Dirac APBC temporal
circle. Both ARE Cl(3)+Z³ facts. The agent's dichotomy "algebra fact vs
mode-count fact" was too sharp.

**Which N-checks would have caught this:**

- **N1** (alternative route enumeration) — only one route tested; per-mode
  γ-norm, geometric mean of spectrum, mode-γ-norm distinct from per-element
  γ-norm, lattice γ-norm via tensor product, and Matsubara-mode product
  structure are five plausible routes; only the first was attempted.
- **N5** (rhetoric audit) — "X is not a Cl(3)-algebra fact" was checked at
  per-element resolution but not at per-mode, per-block, or lattice-wide
  resolution.

**Right framing the cycle should have used:** "the per-element identity (G2')
does not close the framework's per-determinant geometric-mean readout via
the per-site product route. The per-Matsubara-mode route remains
untested and is the natural next cycle." That is a narrow honest result.
The claim "the exponent is not a Cl(3)-algebra fact" is broader than the
evidence supports.

## F2 — Independent walls that are not independent, plus hidden walls (Cycle 3, PR #1118)

**Claim shipped:** T1 "L_t = 4 is the unique PHYSICAL temporal block for
EWSB" closes as `bounded_theorem` conditional on **three independent named
walls**:

- A-W-A: staggered-Dirac realization gate (`staggered_dirac_realization_gate_note_2026-05-03`, `open_gate`);
- A-W-B: scalar-additivity P1 admission (`observable_principle_from_axiom_note`, `audited_conditional`);
- A-W-C: CPT-even phase blindness (`cpt_exact_note`, `unaudited`).

**Why A-W-C is not independent of A-W-A:** the 2026-05-09 revision of
OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE explicitly retires P2 (CPT-even phase
blindness) to a runner-local algebraic consequence of CPT_EXACT_NOTE's
real-anti-Hermitian-D structure. Specifically, D real antisymmetric on the
even-dim staggered block gives `det(D + jI) = det(D − jI)`, hence `|Z(j)| =
|Z(-j)|`. Once A-W-A retains (the staggered-Dirac realization gate),
A-W-C reduces to a finite verification on the L_s=2, L_t=4 block — not a
separate admission. The three-wall framing double-counts.

**Hidden fourth wall buried as "bridge context":** the identification "the
physical EWSB order parameter IS the local bosonic CPT-even bilinear
`∂²_φ ΔV_eff`" is sourced from `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE`,
which is **unaudited** (not retained, not even audited_conditional). The
cycle-3 note treated this as Step (b) "bridge context" rather than promoting
it to an explicit wall. But this identification is load-bearing for the
proof: without it, the algebraic Klein-four orbit at L_t=4 has no claim
on the PHYSICAL EWSB temporal block.

**Honest decomposition:** the proof has **two real independent walls**
(A-W-A staggered-Dirac realization gate, A-W-B P1 scalar additivity), plus
**one downstream consequence** (A-W-C follows from A-W-A), plus **one
hidden bilinear-identification admission** (the EWSB order-parameter
identification from unaudited HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE).
The right shape is 2 + 1 + 1, not "three independent walls."

**Which N-checks would have caught this:**

- **N2** (wall-independence audit) — pairwise table would show "closing
  A-W-A automatically closes A-W-C via the 2026-05-09 P2 retirement,"
  collapsing A-W-C into a runner-local consequence.
- **N3** (hidden-wall scan) — re-reading the proof for "bridge context"
  would have surfaced the bilinear-EWSB identification as a load-bearing
  admission, not narrative framing.

**Right framing the cycle should have used:** "T1 conditional on two walls
(A-W-A, A-W-B) plus one hidden admission promoted to explicit (W4: EWSB
order parameter is the bosonic CPT-even bilinear, sourced from unaudited
`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE`)." That is the same bounded
result, honestly counted.

## F3 — Conflated residuals plus dismissed partial-closure path (Cycle 1, PR #1123)

**Claim shipped:** the substep-4 ratchet (`bounded_theorem` →
`positive_theorem` for `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07`)
is "structurally undecidable from A_min retained primitives" without
(a) a new labeling axiom or (b) C_3-breaking dynamics in retained primitives.
The witness count cited "A3 Routes 1-5 (5 routes, 7 vectors in route 5
alone) + BAE 30-probe terminal synthesis" — characterized as "17 retained
mathematical routes."

**Conflation of residuals (N4 failure):** the BAE 30-probe campaign attacks
the `|b|²/a² = 1/2` amplitude-equipartition condition. AC_φλ is the
species-identification residual. These are different residuals, and the
substep-4 stretch-note itself acknowledges this (line 211-217): "The
campaigns are independent (different residuals)." But the synthesis paragraph
still counts the BAE probes as witnesses against substep-4. After dropping
the residual-mismatching citations, the honest witness count is
5 (A3 routes) + 8 (HR5 confirmation attack lines) + 1 (rigorization addendum)
= 14 packets, all on the C_3-equivariance theorem. The "17 routes" framing
was inflated by including 30 BAE probes that attacked a different residual.

**Dismissed partial-closure path (N6 failure):** the substep-4 separate-closure
note plus C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08 plus the
rigorization addendum together argue that AC_φλ decomposes into

- AC_φλ.struct: already closed by the 3-bijection counting theorem (NQ +
  C_3 + Type I_3 ⟹ exactly 3 C_3-equivariant bijections hw=1 ↔ SM
  generations, all related by cyclic relabeling);
- AC_φλ.label: "which cyclic shift" — argued to be a labeling convention
  identical in nature to `{u, c, t}` naming.

The stretch-note categorized this as "Recommendation Path 2: Explicit
user approval to admit AC_φλ as a new framework axiom." But per
`feedback_no_new_axioms.md`, a labeling-convention ratification (PR #728
preserved-C_3 interpretation, PR #729 conventions-unification companion) is
the **import-retirement path**, not a new axiom. Treating convention
ratification as a forbidden new axiom is a misclassification.

**Which N-checks would have caught this:**

- **N4** (residual matching) — the BAE residual (`|b|²/a² = 1/2`) does not
  match the AC_φλ residual (species identification). The pairwise table
  drops 30 of 30 BAE probe citations.
- **N6** (partial-closure path scan) — PR #728 and PR #729 propose
  labeling-convention ratification, which is the legitimate import-retirement
  path. The stretch-note's dismissal as "new axiom required" is the
  misclassification this check is designed to catch.

**Right framing the cycle should have used:** "Substep-4 ratchet via the
direct C_3-equivariance route is structurally closed under A_min + no new
axiom + no C_3-breaking dynamics, witnessed by A3 Routes 1-5 plus the
HR5 confirmation (14 packets, all attacking the species-identification
residual). The labeling-convention ratification path (PR #728, PR #729)
is an open import-retirement route not attempted in this cycle." That is
narrower than "structurally undecidable" and honest about what remains
open.

## Summary

| Case | Cycle | What was overclaimed | N-check that catches it |
|------|-------|----------------------|------------------------|
| F1 | 4 | "X is not a Cl(3)-algebra fact" when only per-element resolution tested | N1, N5 |
| F2 | 3 | "three independent walls" when one is downstream and a fourth is hidden | N2, N3 |
| F3 | 1 | 30 unmatched-residual citations counted as witnesses; convention reframe dismissed as new axiom | N4, N6 |

Each of these would have failed the no-go-discipline gate at the specific
named check. The narrow corrected claims (right column of each case) all
pass N1-N8 — the gate does not block honest narrow results; it blocks
the inflated broader ones.
