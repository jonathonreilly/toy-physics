# REVIEW HISTORY — Block 01 (H2 reformulation)

**Date:** 2026-05-02
**Block:** 01 — H2 reformulation: f_vac V-singlet derivation of (7/8)^(1/4)
**Branch:** `physics-loop/vev-v-singlet-derivation-block01-20260502`
**Artifact:** `docs/EW_VEV_V_SINGLET_DERIVATION_THEOREM_NOTE_2026-05-02.md` +
              `scripts/frontier_ew_vev_v_singlet_derivation.py`

## Promotion Value Gate (V1-V5)

The campaign goal includes retained-positive movement (retiring bridges
B1+B2+B3 of the parent OBSERVABLE_PRINCIPLE_FROM_AXIOM 5-bridge audit).
Per skill workflow step 7, V1-V5 are answered in writing here BEFORE any PR
is opened. Failing any single question forbids the PR.

### V1: What SPECIFIC verdict-identified obstruction does this PR close?

**Answer:** The audit verdict on `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
(`audited_conditional`, td=294, lbs=26.70, demoted to bounded by PR #267)
quoted:

> "the note proves the log\|det(D+J)\| source-response result only after
> adding scalar additivity, CPT-even phase blindness, continuity, and
> normalization assumptions, and its electroweak-scale consequence imports
> the current hierarchy baseline rather than deriving that normalization
> here."

This PR closes the *first three* of the four functional-equation bridges
named in that quote — scalar additivity (B1), CPT-even phase blindness (B2),
continuity (B3) — by reformulating the load-bearing observable as the V-invariant
free-energy density `f_vac` and replacing the functional-equation route
with a one-line V-invariance argument from the closed-form determinant
identity (A7). Bridge B4 (normalization) and the hierarchy-baseline B5
remain admitted; the PR honestly says so.

This is a SPECIFIC obstruction directly named in the parent verdict text,
not a "the upstream is unratified" dependency-chain complaint.

### V2: What NEW derivation does this PR contain?

**Answer:** New content (not in any existing framework note):

1. **Lemma H2.1**: A direct proof that `f_vac` on the minimal Klein-four
   block is V-invariant from the closed-form determinant `\|det(D+m)\| =
   ∏_ω [m² + u_0²(3+sin²ω)]^4` and the Klein-four action on phases
   (sin²(ω+π) = sin²ω, sin²(-ω) = sin²ω). One paragraph.

2. **Lemma H2.2**: V-invariance of the m²-curvature `A(L_t)` follows from
   H2.1 by V-singlet-source differentiation, giving an explicit closed
   form `A(L_t) = (1/(L_t · u_0²)) ∑_ω 1/(3+sin²ω)`.

3. **Lemma H2.3**: A finite-volume V-singlet-vacuum proof: SSB cannot
   occur on a finite V-symmetric block, so the m=0 vacuum is V-singlet.

4. **Theorem H2 main**: The `(A_2/A_4)^(1/4) = (7/8)^(1/4)` factor follows
   from these lemmas + Klein-four orbit closure (A8) + textbook EFT
   identification (C1), without admitting B1+B2+B3.

5. **Corollary H2-B**: Representation-theoretic distinction between v
   (V-singlet origin) and m_H (V-broken minimum), explaining why the
   (7/8)^(1/4) factor applies to v but not m_H.

This is **not** a sympy-exact verification of the existing
`OBSERVABLE_PRINCIPLE_FROM_AXIOM` runner. It is a NEW derivation route
that bypasses the 3 functional-equation bridges. The runner verifies
this new route by computing A(2)/A(4) from direct rational sum and
exhibiting the L_t=4 unique-resolved-orbit selection.

### V3: Could the audit lane already complete this from existing primitives + standard math?

**Answer:** PARTIALLY — but not fully.

The audit lane has the closed-form determinant identity (A7), the Klein-four
orbit-closure result (A8), and the rational kernel ratio (A9). The audit
lane could in principle compute A(2)/A(4) = 7/8 from these primitives.

However, the *load-bearing reformulation* — replacing `W = log\|det(D+J)\|
- log\|det D\|` (with B1+B2+B3 admissions) by `f_vac` (without those
admissions) — is a STRUCTURAL move that the audit lane has not made on its
own. The audit lane currently treats the parent note's W route as
canonical and admits B1+B2+B3. Recognizing that the same numerical answer
follows from a SHORTER admission chain via f_vac is the new content.

The standard QFT machinery (Schwinger-Dyson, effective action, RG) does not
give this reformulation directly — the reformulation is framework-specific
because it relies on the specific structure of the minimal Klein-four block
(A7) and the orbit-closure selector (A8). Standard EFT machinery alone
gives the EFT identification (C1); it does not tell the framework to use
f_vac instead of W.

### V4: Is the marginal content non-trivial?

**Answer:** YES.

- The reformulation is not a textbook identity: it depends on the framework's
  Klein-four orbit-closure structure (A8), which is a framework-specific
  result, not standard QFT.
- The reformulation is not a definition restated: it materially changes
  which premises are load-bearing (replacing 3 functional-equation premises
  with one EFT identification).
- The reformulation is not a one-step variant of an existing cycle: it
  fundamentally replaces the W route with an f_vac route.

The Higgs-paradox dissolution (Corollary H2-B) is a non-trivial
representation-theoretic insight that explains why v and m_H carry
different selectors — content NOT in any existing framework note.

### V5: Is this a one-step variant of an already-landed cycle?

**Answer:** NO.

The closest prior cycle is cycle 8 of audit-backlog
(PR [#267](https://github.com/jonathonreilly/cl3-lattice-framework/pull/267)),
which DEMOTED the parent OBSERVABLE_PRINCIPLE_FROM_AXIOM to bounded with the
5-bridge audit packet `OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md`.

The structural distinction:
- Cycle 8 / PR #267 *identified* the 5 bridges and demoted the parent note.
- This PR (block 01) *retires 3 of those 5 bridges* by reformulating the
  load-bearing observable.

Cycle 8 is a status-correction packet ("here are the 5 admissions, parent is
demoted"). Block 01 is a forward derivation ("here is a new route that
needs only 2 admissions instead of 5"). These are different operations on
the lane.

This is also distinct from `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE` (the
sister theorem deriving the same (7/8)^(1/4) via the bilinear-curvature
order-parameter route), which uses a DIFFERENT set of admissions.
Block 01's route is independent.

## Value Gate disposition: PASS

All V1-V5 answers are positive. PR is allowed.

## Self-review of the artifact (per skill workflow #12)

### Findings

| # | Severity | Finding | Disposition |
|---|---|---|---|
| F1 | low | The user's original H2 framing said "v ~ f_vac^(1/4) by mass dimension"; this would give the wrong numerical factor since (7/8) comes from A (m²-curvature), not f_vac itself. | The artifact correctly uses A = ∂²f_vac/∂m²\|_0 as the load-bearing observable. The user's original framing has been corrected in the artifact. |
| F2 | medium | The "(1/4) power" in v ~ A^(1/4) is inherited from the staggered taste-determinant chain (16 = 2^4 doublers; (det D)^(1/4) per taste); this note does not re-derive the (1/4). | Recorded explicitly in §6 of the theorem note ("inherited from the staggered taste-determinant chain"). Not load-bearing for the H2 reformulation. |
| F3 | medium | The negative control originally tried — "non-V-singlet localized source breaks V-invariance" — does NOT actually work in this finite-Matsubara setting. V acts as a permutation on the V-orbit-closed APBC mode set, so any sum over modes is automatically permutation-invariant regardless of the weight function. | Replaced with a SELECTOR DEPENDENCE check (Check 8) showing that only L_t=4 (Klein-four orbit-closure) gives the framework's value; alternatives (L_t=6, 8, 10, ∞) give different values. This demonstrates the orbit-closure selection is non-trivial and load-bearing. |
| F4 | low | Admission C1 ("v² is the curvature of f_vac at origin") may be classified by audit as comparable in load-bearing weight to B1+B2+B3 combined. | Recorded as Risk R1 in HANDOFF; theorem note §7 explicitly addresses this with the "textbook-standard EFT" classification. If audit returns adverse, the H2 reformulation is sideways rather than retiring. |
| F5 | low | The runner does not construct the L_s=2 staggered Dirac matrix explicitly; it relies on the closed-form determinant A7 as a retained primitive. | Acceptable: A7 is independently verified by `scripts/frontier_hierarchy_matsubara_decomposition.py`. Recorded explicitly in Check 7. |
| F6 | low | The numerical readout `v = M_Pl·(7/8)^(1/4)·α_LM^16 = 246.28 GeV` depends on the admitted hierarchy baseline B5; this PR does NOT close B5. | Recorded explicitly in §10 of the theorem note as out-of-scope, admitted-context only. |

### Hostile-review-style stress test (per memory `feedback_hostile_review_semantics`)

**Q1.** Is the "f_vac is V-invariant" claim provable from action V-invariance + Z-invariance, or is there a hidden gauge-fixing or measure-choice that breaks V?

**A1.** The Klein-four V acts on APBC temporal Matsubara phases by Z₂(sign):
ω → ω+π and Z₂(conj): ω → -ω. The action on the gauge degrees of freedom is
trivial (V acts only on temporal mode labels, not on link variables). The
Haar measure for SU(3) link variables is invariant under any global symmetry,
including V. So Z = ∫ dU exp(-S[U]) is V-invariant whenever S is V-invariant
(A6). f_vac = -(1/V_total) log Z is then V-invariant by chain rule. No
hidden gauge-fixing breaks V.

**Q2.** Is C1 ("v² = -∂²f_vac/∂m²\|_0") really textbook-standard, or is it a
framework-specific identification that should be classified as a bridge of
comparable weight to B1+B2+B3?

**A2.** Standard EFT (Coleman-Weinberg 1973; Peskin-Schroeder Ch. 11; Weinberg
Vol. II Ch. 16) defines the effective potential V_eff(φ) such that
∂V_eff/∂φ vanishes at the vacuum and ∂²V_eff/∂φ²|_{vacuum} gives the
inverse propagator at zero momentum. For the Higgs sector, v² is identified
with the curvature at the symmetric point (or equivalently the mass-squared
of the Higgs at the symmetric point, with appropriate sign for SSB). This
is not framework-specific.

The framework's *additional* claim is that f_vac on the minimal Klein-four
block is the right f_vac to use (rather than the continuum effective
potential). That's an extension of standard EFT to the framework's lattice
context, but the curvature-at-origin identification itself is textbook.

The audit's classification of C1 may still pushback; we record this as a
known risk (Risk R1).

**Q3.** Is the (1/4) power in v ~ A^(1/4) load-bearing for H2's claim?

**A3.** No. The (1/4) power is inherited from the staggered taste
determinant via `(det D)^(1/4)` extracting the per-taste amplitude. H2
doesn't change the (1/4); it shows that A (whichever form) is V-invariant
and that the (7/8) ratio (not the (7/8)^(1/4) factor) is the V-invariant
property derivable from f_vac. The (1/4) lives in the existing
HIERARCHY_BOSONIC_BILINEAR_SELECTOR / YT_P2_TASTE_STAIRCASE chain.

### Self-review disposition: PASS

All findings either don't affect the load-bearing claim or are explicitly
recorded with mitigations. The H2 reformulation is honestly stated as
exact-support theorem on retained primitives + admitted C1 (textbook EFT)
+ admitted B5 (separate lane), with explicit acknowledgment that audit
may classify C1 differently.

## Cluster-cap / volume-cap check

- Volume cap: 1 PR proposed for this campaign; cap is 5 / 24h. PASS.
- Cluster cap: this PR is NEW family `vev-v-singlet-derivation-*`, not in
  any existing 2-PR cluster. PASS.
- Corollary-churn: this is the FIRST cycle of the campaign; corollary-churn
  doesn't apply yet. PASS.

## Closure and next action

Block 01 is closure-ready: artifact written, runner passes, V1-V5 PASS,
self-review PASS, no failed checks. Next action: write CLAIM_STATUS_CERTIFICATE,
commit, push, open PR.
