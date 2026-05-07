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

---

## Block 03 review (2026-05-06)

**Artifact:** `docs/BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md`
**Type:** internal hostile-review on stretch + named obstruction

### Semantic challenges

**Challenge A — Casimir-diagonal factorization claim is correct?**
Response: (T3.a) factorization Z = Σ (Π W_λ) F_Λ is a structural fact
about HK character expansion. W_λ(t) = d_λ exp(-t·C_2/2) is the
per-plaquette character expansion coefficient under HK measure (Step 2
of Block 01). F_Λ is the t-INDEPENDENT Wigner-Racah graph trace —
it depends only on the lattice geometry and irrep labels, not on β/t.
This separation is NOT possible for Wilson (whose Bessel-determinant
character coefficients couple t/β nontrivially with d_λ). PASS.

**Challenge B — Named obstruction (cluster-decomposition) genuinely
identifies the gap?** Response: per
[`GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md`](../../../../docs/GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md),
the framework's primitives don't pin Perron moments tightly enough.
The cluster-decomposition / exponential-clustering estimate for HK
would need to come from RP-A11 + Lieb-Robinson + per-site Cl(3) dim 2,
but per Block 04's no-go these primitives don't resolve action-form
uniqueness either. The named obstruction is genuine. PASS.

**Disposition:** PASS at named-obstruction tier. No closure claim.

---

## Block 04 review (2026-05-06)

**Artifact:** `docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`
**Type:** internal hostile-review on no-go theorem

### Semantic challenges

**Challenge A — Are {Wilson, HK, Manton} truly all jointly compatible?**
Response: each is a well-defined gauge action. Wilson per
G_BARE_DERIVATION's "accepted Wilson surface". HK derived in Block 01
under canonical Tr-form. Manton uses canonical bi-invariant metric
(Block 01 Step 1). All three give the same continuum limit at small a
(Step 1.1 in note). At finite β, they give distinct ⟨P⟩(6) values
(Block 02 + Block 06 confirm: HK ≠ Wilson). PASS.

**Challenge B — No-new-axiom rule applied correctly?**
Response: the protocol forbids enlarging the axiom stack (A1+A2). The
no-go shows that under A1+A2 + currently-retained primitives + standard
machinery + continuum-limit matching, action-form is not pinned. To
pin it would require a NEW PRIMITIVE (forbidden) or a CONVENTION-LAYER
ADMISSION (governance, Resolution B). The no-go is structural. PASS.

**Challenge C — Range-bounding ~5-10% is honest?**
Response: u_0 = ⟨P⟩^(1/4) under Wilson 1-plaq 0.4225 vs HK 1-plaq
0.5134 gives u_0_W = 0.806 vs u_0_HK = 0.847 (~5% range). α_s ~ u_0²
gives ~10% range. These are honest scaling estimates; tight bounds
require Block 06+'s thermodynamic-limit values, but Block 03's named
obstruction means those values are themselves open. Honest framing. PASS.

**Disposition:** PASS at named-obstruction no-go tier. Reusable
negative evidence.

---

## Block 05 review (2026-05-06)

**Artifact:** `docs/BRIDGE_GAP_GAUGE_GROUP_TASTE_CUBE_EXPLORATION_NOTE_2026-05-06.md`
**Type:** internal hostile-review on exploratory finding

### Semantic challenges

**Challenge A — gl(3) ⊕ gl(1) commutant claim is correct?**
Response: standard Lie-algebra commutant analysis on the tensor
product C^2 ⊗ V_8 (per-site dim × taste cube) gives the commutant of
SU(3)_c on V_8 = sum of trivial+standard S_3 reps on each Hamming
weight stratum. The 4-dim "trivial" part has 4 independent U(1) factors;
the 4-dim "standard" part is acted on by SU(3) traceless generators.
Commutant has rank 4 (four independent U(1)) plus 8 SU(3) generators.
PASS.

**Challenge B — SU(3)×U(1)^k → SM hypercharge identification?**
Response: the note explicitly DOES NOT make this identification load-
bearing. Section 4 lists three required structural arguments (collapse
to single generator, taste-vertex SM-fermion assignment, Y = T_3 - Q
match) — none in retained chain. Honest open-gate framing. PASS.

**Challenge C — Does this break Block 04's no-go?**
Response: Step 5 explicitly checks this. Adding U(1)-symmetry to the
gauge action constrains the U(1) sector but doesn't break SU(3)
action-form ambiguity (Wilson/HK/Manton are all SU(3)-invariant by
construction). Block 04's no-go stands. PASS.

**Disposition:** PASS at exploration / open-gate tier. Useful for
future research direction; not a Resolution-A closure.

---

## Block 06 review (2026-05-06)

**Artifact:** `docs/BRIDGE_GAP_HK_CUBE_PERRON_NOTE_2026-05-06.md`
**Runner:** `scripts/probe_hk_cube_perron_l2_2026_05_06.py`
**Type:** internal hostile-review on numerical artifact

### Semantic challenges

**Challenge A — Candidate ρ ansatz transfers from Wilson to HK?**
Response: per the existing Block 5 / `SU3_CUBE_FULL_RHO_PERRON_2026-05-04`,
the formula `(d c/c_00)^12 · d^(-16)` is justified by the cube's
8-component / 24-link topology (`d^(N_components - N_links) = d^(-16)`)
and per-plaquette character contributions (`(d c/c_00)^12` for 12
plaquettes). The topology factor is character-coefficient-agnostic.
PASS.

**Challenge B — Numerical convergence at NMAX 7-8?**
Response: runner shows P_cube_HK stable to 12 decimal places across
NMAX ∈ {6, 7, 8}: 0.5223243151. The HK Casimir-suppression factor
exp(-6t·C_2) at high (p,q) is exponentially small, so NMAX truncation
converges fast. PASS.

**Challenge C — Suggestive observation that HK is closer to MC?**
Response: at L_s=2, |HK_cube - MC| / ε_witness = 235; |Wilson_cube - MC|
/ ε_witness = 543. Factor 2.3× closer. The note explicitly labels this
as suggestive comparator, not load-bearing for action-form selection.
Honest framing. PASS.

**Challenge D — Does this break Block 04's no-go?**
Response: Block 06's L_s=2 result is consistent with Block 04 — the
two actions give different finite-β values (0.5223 vs 0.4291). It
DOES NOT prove HK is "the right" action; both are computed. Block 06
adds empirical comparator data; doesn't close the structural ambiguity.
PASS.

**Disposition:** PASS at bounded-support tier. Numerical comparator
artifact under HK candidate action.
