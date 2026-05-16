# Review History

**Loop:** koide-l5-spectral-triple-20260516

## Cycle 1 — Z_3-equivariant anti-commuting subalgebra disjointness (block01)

### Hostile review 2026-05-16T07:55Z

**Reviewer:** internal special-forces hostile reviewer (general-purpose agent)
**Verdict:** DEMOTE
**Key findings:**
- V3 borderline-reconstructable: main theorem is paragraph-length corollary of L3+L4+Schur orthogonality.
- V2 borderline new content: Z_3 Fourier diagonalization is canonical.
- §3 four reformulations were theatrical width.
- §4 Connes-Lott corollary killed a strawman γ_CL=Γ_χ identification no NCG practitioner uses.

**Disposition:** demote to exact_support, trim §3, rewrite §4 as scope-narrow observation.
**PR opened:** #1176 with honest exact_support status.

## Cycle 2 — Block-Diagonality Obstruction (block02)

### Hostile review 2026-05-16T08:35Z

**Reviewer:** internal special-forces hostile reviewer (general-purpose agent)
**Verdict:** DEMOTE
**Key findings:**

- **F-1 [DEMOTE]:** §2 proof is genuinely simpler than Cycle 1's but uses the same underlying obstruction mechanism. Cycle 1 dresses it in Z_3 Fourier; Cycle 2 strips that dressing. Structural insight (Γ_χ has full-spectrum non-zero eigenvalues on every block) is shared verbatim. Refactoring of proof, not new mechanism.

- **F-2 [NOTE]:** Class of H covered IS strictly larger than Cycle 1 (3 extra real dimensions). Z_3-equivariant: 2-dim (scalar on singlet × scalar on doublet); block-diagonal: 4-dim (scalar on singlet × Sym(2) on doublet). Generalization substantive in raw set-inclusion terms.

- **F-3 [DEMOTE]:** But the new dimensions are NOT physically distinguished. No candidate framework realization in the Koide chain produces H block-diagonal-but-not-Z_3-equivariant. R3/R4/R5 routes either don't preserve Γ_χ in commutant or are already covered by Cycle 1 (R2). The 3-dim "newly excluded" space is dead space.

- **F-4 [DEMOTE]:** V3 reconstruction concern is **WORSE** here than in Cycle 1. Cycle 2's proof is a 3-line block decomposition using only spectral theorem + trivial block-anti-commutator identity. An audit lane derives it from L4 §3 + one-paragraph block argument. No calculator step.

- **F-5 [NOTE]:** §4 corollary's three-case table is breadth without depth. Each case (a/b/c) satisfies the corollary hypothesis trivially by construction. Cases (b) and (c) cover algebras different from Z_3 (semisimple non-cyclic; commutative non-Z_3) but each is comfortably interior. None probes the boundary.

- **F-6 [NIT]:** §5/Part 5 (L4 family escape) restates L4 §3.2's existing observation that "H mixes singlet and doublet" — which IS the negation of block-diagonality in (s,D).

- **F-7 [NIT]:** Part 6 (SO(3) premise fails) is a single passing diagnostic correctly showing Schur's lemma is what kills SO(3)-equivariant H. Useful scope clarification, not content-bearing.

**Semantic attacks:**
- (s, D) IS the Z_3 Fourier basis collapsed: trivial character (singlet) + ω/ω² character pair (doublet) merged into one eigenspace by Γ_χ's spectrum (+1, -1, -1). Cycle 2 works in this coarser decomposition.
- CONTENT in Cycle 2 not in Cycle 1: obstruction needs only Γ_χ eigendecomposition, not full Z_3 Fourier. That's a real generalization. But one-step refactoring, not new physics.

**Marginal content assessment:**
- §4 three-case table is incrementally informative but tautological in the sense the user predicted. No case probes the corollary's boundary. SO(3) test (Part 6) doesn't activate the corollary at all.

**Cluster position:**
- PR #2 in koide_* family. Pattern A (narrow re-scope of algebraic core).
- Cluster-cap evaluator activates at #3 — this PR does NOT trigger cap-based BACKLOG mechanically.
- **PR-density warning:** Cycle 1 and Cycle 2 together fence a single algebraic obstruction
  (anti-commute + grading-respecting structure ⟹ H = 0) with two variations of the
  structural hypothesis. **A Cycle 3 in this family would be churn by inspection.**

**Verdict (verbatim):**
"Cycle 2 IS a strict generalization of Cycle 1 in set-theoretic terms (3 extra real
dimensions of H closed off). The §2 proof is genuinely cleaner. But the
V3-reconstructability concern that demoted Cycle 1 is STRONGER here, not weaker. The §4
corollary's three-case table is tautological breadth. The §5/Part 5 L4-escape insight
duplicates L4 §3.2's existing observation. No candidate framework realization produces
H block-diagonal-but-not-Z_3-equivariant, so the 3 extra dimensions are physically
vacuous. This is honest scholarship — the proof is correct, the generalization is real,
the §3 comparison to Cycle 1 is forthright — but it is an exact_support note tightening
an obstruction whose physically-relevant content was already in Cycle 1. Land as
exact_support; do not promote. Any further cycle in this family (Cycle 3+) would trip
cluster-cap as churn."

### Disposition applied 2026-05-16T08:45Z

**Local disposition:** demote (not pass, not block).

**Edits applied to the source note:**
- Added explicit "Hostile review record" front-matter section quoting verdict.
- Type field is `exact_support` (no change — was already exact_support per claim certificate).
- Note's scope clarification §5 was already honest; no edits needed.

**Edits applied to the certificate:**
- "Hostile review record" Cycle 2 entry added (TBD pending commit).

## Campaign-level signal: corollary exhaustion

The Cycle 2 reviewer's verdict that "any further cycle in this family would trip
cluster-cap as churn" is the **corollary-exhaustion signal** described in the
physics-loop skill's stop conditions:

> "corollary exhaustion: every remaining ranked opportunity would produce only a
> one-step algebraic corollary of an already-landed campaign cycle with no new
> load-bearing premise."

The remaining ranked opportunities in OPPORTUNITY_QUEUE.md are all Pattern A variants:
- "Multi-factor Connes-Lott construction" — requires admitting NCG axioms; bounded_theorem ceiling
- "Twisted modular spectral triple" — requires Connes-Moscovici 2008 import; sibling chain not Level 5
- "Cl(3) dimension-parity obstruction" — independent argument BUT covers same physical content
- "No-go consolidation of R1-R5" — explicit corollary churn warned by reviewer

**Per skill workflow §15:** "Stop the whole campaign only when runtime/max cycles
expires, the target status is genuinely achieved and no further campaign target was
requested, or the queue has been freshly scanned and every viable opportunity is
blocked by human judgment/tooling."

Refreshed queue: every remaining ranked opportunity is either churn (per Cycle 2
reviewer warning) or admits-imports (bounded_theorem ceiling, requiring user
direction on whether to accept that ceiling).

Recommendation: stop the campaign cleanly with comprehensive HANDOFF and final
report to user. User can choose to extend the campaign with a different exit
criterion (e.g., "accept bounded_theorem if it uses Connes-Moscovici").
