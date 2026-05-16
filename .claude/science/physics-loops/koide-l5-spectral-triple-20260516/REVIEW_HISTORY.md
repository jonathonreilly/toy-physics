# Review History

**Loop:** koide-l5-spectral-triple-20260516

## Cycle 1 — Z_3-equivariant anti-commuting subalgebra disjointness (block01)

### Hostile review 2026-05-16T07:55Z

**Reviewer:** internal special-forces hostile reviewer (general-purpose agent)
**Brief:** Challenge semantics; specifically attack the γ_CL ↔ Γ_χ identification, the V1-V5 promotion value gate, the §3 four reformulations, and the runner integrity.

**Findings (verbatim severity tags):**

- **[DEMOTE]** Main theorem is a 2-line corollary of L3 + L4 + Schur orthogonality. L4 §6.1 already states `(R-R^T)/i` "COMMUTES with Γ_χ (not anti-commutes)". L3 Lightcone Primitive places Z_3-equivariant H in the circulant algebra `aI+bR+cR²`. Once these are on the table, the no-go is a one-paragraph corollary. V3 "audit lane can derive it" objection lands.
- **[DEMOTE]** V2's "new derivation" is reformulation, not new content. The Z_3 Fourier diagonalization is the canonical proof.
- **[BLOCK candidate / NOTE]** §3 "four equivalent reformulations" are the same statement in different dress. Theatrical width.
- **[NOTE]** Runner Part 5 prints `(-1)**(2/3)` symbolic garbage (cosmetic, PASS holds).
- **[NOTE]** Hermiticity caveat half-buried (Part 3 line 165): real symmetric forces `c=b`. Conclusion holds, but note never tightens.

**Semantic attacks:**
- γ_CL ↔ Γ_χ identification in §4 is a strawman. Standard Connes-Lott uses
  `H = H_L ⊕ H_R` with γ_CL = diag(I, -I) (Z_2 chirality grading on
  left-right doubling). Γ_χ is a Z_3 character grading on a single R³
  (generation space). These live in different Hilbert spaces and grade
  different physical structures. The corollary's "we identify γ_CL = Γ_χ"
  is not a Connes-Lott candidate any NCG practitioner has ever proposed.
- The correct CL structure for generations is `C³ ⊗ (H_L ⊕ H_R)`, with
  γ_CL = I⊗σ_3 on chirality and Γ_χ as SEPARATE grading on the C³ factor.
  The L4 anti-commutation `{H, Γ_χ}=0` is a SEPARATE constraint orthogonal
  to γ_CL chirality grading. The no-go does NOT apply.

**Alternative framings (reviewer's escape hatches for a savvy NCG builder):**
1. "γ_CL and Γ_χ are different gradings on different factors. Your
   identification is not a Connes-Lott construction."
2. "First-order condition forces M Z_3-equivariant only when A acts via
   regular rep on a single R³. Use C³ ⊗ C² with diagonal A-action; M
   is unconstrained by first-order."
3. "Twisted/modular spectral triples (Connes-Moscovici 2008) relax this
   anti-commutation."

**Verdict:** DEMOTE
**Justification (verbatim):** "The main theorem is true and the runner is
clean (20/0 PASS, all class-A, no hidden imports for the core algebra).
But (a) the result is a one-paragraph corollary of L3+L4+Schur
orthogonality that V3 admits is 'borderline reconstructable' and
'marginal new content'; (b) the §4 Connes-Lott corollary kills a hybrid
γ_CL/Γ_χ identification no NCG practitioner uses; (c) the §3 'four
equivalent reformulations' are theatrical width. The artifact has
positive but narrow value: a clean algebraic identity
(`comm(R) ∩ anticomm(Γ_χ) = {0}` in Sym(R³)) plus an explicit-corollary-
style closure of one specific (forced) Connes-Lott identification. That
value is real but support-tier, not positive_theorem."

### Disposition applied 2026-05-16T08:00Z

**Local disposition:** demote (not pass, not block).

**Edits applied to the source note:**
- Title changed from "No-Go" to "Subalgebra Disjointness".
- Type field changed from `no_go` to `exact_support`.
- Front-matter rewritten: removed "pure algebraic no-go" framing;
  added explicit scope clarification re: standard multi-factor
  Connes-Lott NOT addressed.
- §3 trimmed: four "equivalent reformulations" → one algebraic
  + one geometric statement.
- §4 rewritten as "Scope-narrow Connes-Lott observation"; explicitly
  acknowledges standard multi-factor constructions are NOT addressed;
  documents escape hatches.
- §5 retitled "What this support note does NOT establish".
- §9 retitled "Narrow exact support identity"; removed "structural
  no-go for Connes-Lott" overclaim.

**Edits applied to the certificate:**
- Status field changed from `no_go` to `exact_support`.
- Added "Hostile review record" section quoting verdict and findings.
- Updated "Next cycle plan" with three options (A, B, C) preferring
  Candidate A (staggered-Dirac taste route — most independent).

**Runner left as-is.** 20/0 PASS, all class-A. The runner verifies the
algebraic core which remains correct; only the framing of the
surrounding source note was demoted.
