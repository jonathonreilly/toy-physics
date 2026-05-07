# Review History — Bridge Gap New Physics Loop

**Date:** 2026-05-06
**Loop:** bridge-gap-new-physics-20260506

---

## Block 01 review (2026-05-06)

**Artifact:** `docs/BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md`
**Runner:** `scripts/probe_hk_time_derivation.py` PASS=7/0
**Type:** internal hostile-review (per user-memory feedback that hostile
reviews must challenge SEMANTICS, not just algebra)

### Semantic challenges and responses

**Challenge A — Leading-order match privileging.** The leading-order
small-U match is one specific match between Wilson and HK; why is it
the right one? Response: explicitly captured in conditional clause (d)
of the Status section. The leading-order match corresponds to the
continuum limit / canonical Brownian-time-Wilson-coupling correspondence;
finite-β / O(a²) corrections are Block 02 / Block 04 targets. The note
does NOT claim leading-order is the only valid match — only that under
this specific selection criterion, t = 2 N_c / β. PASS.

**Challenge B — Menotti-Onofri / Drouffe-Zuber load-bearing?** The note
cites these as cross-validation. Are they doing derivation work? Response:
Step 5 (the actual matching) is done from first principles (Wilson
small-U expansion + HK small-U expansion + match coefficients) without
using Menotti-Onofri or Drouffe-Zuber as derivation inputs. The Cross-
validation section explicitly states these are "admitted-context
cross-checks, NOT load-bearing derivation inputs." PASS.

**Challenge C — `S_HK = -log P_t(U)` is a definition / admitted import?**
Yes — but the note frames this as conditional (c): "heat-kernel as the
Cl(3)-native action candidate (Block 04 target — uniqueness vs Wilson
NOT yet derived)." Block 01 derives the value t given HK as a candidate;
Block 04 attacks whether HK is actually forced. Honest conditional
structure. PASS.

**Challenge D — Is `Tr(T_a T_b) = δ_{ab}/2` forced by Cl(3)/Z³?** This
is genuinely conditional on G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM
(retained) which sets it as the canonical convention. The G_BARE
normalization is itself an open gate per MINIMAL_AXIOMS_2026-05-03. So
Tr-form is admitted at the canonical-convention layer, not derived from
A1+A2 directly. Captured in conditional (a). PASS.

**Challenge E — Block 02 preview legitimate?** Section 8 explicitly
labeled "Numerical preview for Block 02 (to be derived in Block 02)".
Not a closure claim. PASS.

**Challenge F — User-memory feedback "consistency-equality is not
derivation".** Is t = 2 N_c / β a consistency equality (matching two
already-known-equal forms) or a derivation? Response: the small-U
expansions of Wilson and HK are computed FROM the action functionals,
each giving a quadratic form in X. They are NOT equal a priori — they
share the leading quadratic shape (both are SU(N)-Casimir-like at
leading order) but differ in coefficient. The match Wilson/HK at
leading order FORCES a specific relation between β and t. This is a
derivation: given Wilson with coupling β and HK with time t, the
small-U-match condition uniquely determines t in terms of β. PASS, with
the caveat that (per Challenge A) the matching criterion is one specific
choice; alternatives (full character match, deconfinement match, etc.)
might give different t. Block 04's uniqueness analysis attacks this.

**Challenge G — User-memory feedback "trace-ratio derivations can be
arithmetically perfect while comparing against convention-defined
sources rather than physical couplings".** Am I identifying t with g²
as a physical coupling? Response: g_bare is NOT a physical coupling in
the framework — it's the canonical-normalization parameter (open gate).
At g_bare = 1 (canonical), t = 1 is the canonical heat-kernel time. The
PHYSICAL value of ⟨P⟩(6) under HK action is what Block 02 derives. The
identification "t = 1 at canonical g_bare = 1" is convention-internal
and explicitly conditional on the canonical-convention layer (clause
(a)+(b)). Honest framing. PASS.

### Disposition

**PASS** — bounded support theorem at honest tier. Status text uses
"bounded support theorem" / "conditional support" consistently; no bare
retained or promoted language. All conditionals explicit. Forbidden
imports observed (no PDG/MC values as derivation inputs).

### Local action

- No demotion needed.
- No additional artifact required for Block 01.
- Open PR with clear "independent audit required" notice.
- Continue to Block 02.

---

## Block 02 review (2026-05-06)

**Artifact:** `docs/BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md`
**Runner:** `scripts/probe_hk_plaquette_closed_form.py` PASS=8/0
**Type:** internal hostile-review

### Semantic challenges and responses

**Challenge A — Is "exact in 2 characters" really exact, or just leading-order truncation?**
Response: Genuinely exact. Schur orthogonality forces ALL irreps (p,q)
with p + q ≥ 2 to integrate to zero against the (1,0) + (0,1) sum that
defines Re Tr U. Verified numerically: NMAX=2, NMAX=5, NMAX=10 all give
identical symbolic 3 exp(-2t/3). PASS.

**Challenge B — Does this depend on the HK character expansion form?**
Response: Yes, but the HK character expansion is derived from
Brownian-motion + bi-invariant metric (Block 01). Not an independent
ansatz. PASS.

**Challenge C — Is the 21% structural difference from Wilson load-bearing?**
Response: Real consequence of action choice. Both values are exact
arithmetic. Framework needs to derive which action is forced (Block 04).
PASS.

**Challenge D — Is "264× ε_witness BELOW MC" meaningful?**
Response: Comparator only. Thermodynamic limit (Block 03) may shift.
Note explicitly labels comparator-only. PASS.

**Challenge E — Consistency-equality vs derivation?**
Response: Forward derivation from Schur + retained Casimir + Block 01.
The exact-in-2-characters structural finding is new content. PASS.

**Challenge F — V3 "audit lane could complete" check.**
Response: Schur + Casimir + standard HK form is in principle audit-
derivable. But the project's framing (until 2026-05-06) was Wilson; HK
evaluation under that framing was not a question. Block 02 does the HK
evaluation under the new-physics opening's reframing — generally pass,
strictly marginal.

### Disposition

**PASS** at bounded-support tier. No demotion needed locally.
Independent audit required.

### Local action

- Open stacked PR (base = Block 01 branch) with explicit "depends on Block 01" notice.
- Continue to Block 03 (thermodynamic Casimir-diagonal closure attempt).
