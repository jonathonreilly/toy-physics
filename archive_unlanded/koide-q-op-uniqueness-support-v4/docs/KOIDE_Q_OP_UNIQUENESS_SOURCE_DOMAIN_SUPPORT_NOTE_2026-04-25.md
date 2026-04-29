# Koide Q OP-Uniqueness Source-Domain Support Note (V4)

**Date:** 2026-04-25 (post-V3 review by Codex)
**Status:** **support-grade**, not retained closure. Articulates the
OP-uniqueness Path (a) interpretation precisely and addresses each of
Codex's V3 review findings. The closure remains conditional on a separate
theorem proving the OP-uniqueness → scalar source-domain exclusivity
bridge for ALL scalar-observable backgrounds (not just source perturbations),
including Z exclusion.
**Runner:** `scripts/frontier_koide_q_op_uniqueness_source_domain_support.py`
**Supersedes:** the V3 closure-claim framing in
`KOIDE_Q_CLOSURE_VIA_OP_UNIQUE_GENERATOR_DOMAIN_THEOREM_NOTE_2026-04-25.md`
on `koide-q-closure-via-op-uniqueness` (commit `9df758bc`).

---

## 0. Headline

Codex's review of V3
([review.md](https://github.com/jonathonreilly/cl3-lattice-framework/blob/koide-q-closure-via-op-uniqueness/review.md)
on the V3 branch) verdict: NOT READY to land as retained closure. Three
specific findings:

- **P1 (interpretive bridge):** V3's "OP Theorem 1 uniqueness implies
  scalar source-domain exclusivity" is an interpretive inference, not
  stated verbatim in OP. V3 itself acknowledges this caveat (§4 of V3
  closure note). For retained closure, this inference would need to be
  PROVED as a separate theorem.
- **P1 (runner asserts):** The V3 runner sets `z_in_framework_source_domain
  = False` directly and then derives Q = 2/3. This ASSERTS the load-
  bearing source-domain exclusion rather than CERTIFYING it from disk-
  level checks of retained authorities.
- **P2 (stale branch):** V3 was branched from a stale `main`. Direct merge
  would delete unrelated packages (Napoleon, cosmology single-ratio
  reconstruction, etc.).

This V4 note + runner addresses all three:

1. **Reframes** the OP-uniqueness inference as a **defended hypothesis**
   (not a closure step). The note honestly identifies the inference as
   interpretive, articulates the BEST defense, and explicitly defers the
   closure to a future separate theorem.
2. **Updates the runner** to AUDIT retained authorities from disk:
   - Reads `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` from disk and
     verifies it contains the "unique" clause.
   - Reads `KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`
     and verifies it contains the "Z is not onsite" claim.
   - Reads `KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`
     and verifies it contains the "K = 0 ⇔ Q = 2/3" criterion.
   - Does NOT assert the disputed source-domain exclusion as a Boolean.
3. **Rebased** on current `origin/main` (`0e7d2a2b` Napoleon, etc.); no
   unrelated packages deleted.

---

## 1. The OP-uniqueness Path (a) interpretation (defended hypothesis, not closure)

**Hypothesis (PATH-A-INTERP):** OP Theorem 1's "**unique** additive CPT-even
scalar generator" implies that the framework's scalar observable source
domain is exclusively `span{P_x}`. Therefore commutant Z (which has
cross-site entries via cyclic shift `C`, hence `Z ∉ span{P_x}` per ONSITE
§3) is excluded from the framework's scalar observable source domain.

**Defense (per V3 note §4):**

1. OP Theorem 1's chain (Grassmann factorization + scalar additivity +
   CPT-even insensitivity to fermionic phase) gives `W = log|det(D+J)|`
   with a SPECIFIC source structure `J = Σ_x j_x P_x`.

2. If there were an alternative scalar generator `W'` on a broader source
   domain (e.g., including commutant Z), it would need to satisfy the
   same chain. By OP's uniqueness clause, no such `W'` exists; OR, `W'`
   must reduce to OP's `W` after restriction.

3. Therefore the framework's scalar observable structure is contained in
   OP's framework. Sources outside `span{P_x}` (like Z) don't generate
   independent scalar observables.

**Honest interpretive caveat (acknowledging Codex's P1 finding):**

The inference "uniqueness of generator implies uniqueness of source
domain" is NOT stated verbatim in OP. It's an inference that requires
accepting a specific reading of OP's "unique" clause:

- Strict reading: "unique additive CPT-even scalar generator" means there
  is exactly one such generator W with its specific source domain. No
  other generator on a different source domain exists. → Implies source-
  domain exclusivity.
- Loose reading: "unique additive CPT-even scalar generator" means OP's
  W is the unique GENERATOR of its KIND, but other observables might
  exist via different routes (not generators). → Does not imply source-
  domain exclusivity.

The strict reading gives Path (a) closure. The loose reading leaves the
closure open.

For theorem-grade retained closure: a SEPARATE theorem proving the strict
reading is correct (and rigorously deriving source-domain exclusivity for
backgrounds, not just perturbations) is needed. This V4 note does NOT
provide that theorem.

**Closure status:** support-grade. The interpretive bridge is
articulated and defended but not theorem-grade. The Path (a) closure
remains open pending a separate theorem.

---

## 2. CRIT-side conditional implication

CRIT (retained on main, `KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25` §5):

```text
On the admitted normalized reduced carrier:
  K = 0 ⇔ Y = I_2 ⇔ z = 0 ⇔ ⟨Z⟩ = 0 ⇔ Q = 2/3.
```

If the OP-uniqueness Path (a) interpretation IS accepted (per the
hypothesis above), then commutant Z is excluded from the framework's
scalar observable source domain. The "physical undeformed scalar
background" on the lepton orbit has z = 0. By CRIT, Q = 2/3.

The implication is conditional on accepting the OP-uniqueness
interpretation as theorem-grade. With that interpretation: Q closes.
Without it: Q remains support-grade conditional.

---

## 3. Codex V3 review findings — explicit response

### Finding P1.1: Interpretive bridge

**Codex's exact wording:**
> "the inferred reading that OP Theorem 1 uniqueness of the scalar
> generator also proves uniqueness of the scalar source domain. The note
> later explicitly says this is not stated verbatim in OP and may be
> flagged by strict review. That leaves this as a defended support-route
> interpretation, not a theorem-grade retained closure for `main`."

**This V4 response:**
- Reframes V3's "closure" claim as "defended hypothesis" (§1).
- Explicitly identifies strict vs loose readings of OP's "unique" clause.
- Acknowledges that strict reading is needed for closure but is interpretive.
- Notes that a separate theorem proving the strict reading is the path to closure.

This V4 note does NOT promote Q closure. It records the OP-uniqueness
interpretation as the strongest defended PATH that requires a separate
theorem to convert to retained closure.

### Finding P1.2: Runner asserts source-domain exclusion

**Codex's exact wording:**
> "The runner's load-bearing step is not computed or extracted from
> retained authorities. It assigns the framework scalar source domain to
> `span{P_x}`, sets `z_in_framework_source_domain = False`, then hard-
> codes `z_physical = 0` and derives `Q_l = 2/3`. That verifies the
> downstream algebra only after assuming the exact disputed OP uniqueness
> to source-domain uniqueness bridge."

**This V4 response:**

The V4 runner replaces the asserted Boolean with disk-level audits:

```python
# Audit OP retains "unique" clause:
op_text = read_file("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
op_unique_clause_present = "unique additive CPT-even" in op_text  # AUDIT
# ✓ Verified that OP retains the "unique" clause (literal string check).

# Audit ONSITE §3 retains "Z is not onsite":
onsite_text = read_file("docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md")
onsite_z_not_onsite = "not an onsite diagonal source function" in onsite_text  # AUDIT

# Audit CRIT §5 retains "z = 0 ⇔ Q = 2/3":
crit_text = read_file("docs/KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md")
crit_eq_present = "z = 0" in crit_text and "Q = 2/3" in crit_text  # AUDIT
```

The V4 runner does NOT assert that the framework's scalar source domain
EXCLUDES Z. Instead, it audits the existing retained authorities and
articulates the OP-uniqueness inference as a CONDITIONAL implication
(if the strict reading is accepted, then closure follows).

### Finding P2: Stale branch

**Codex's exact wording:**
> "The source branch is stale relative to current `origin/main`. A direct
> branch merge would delete live main packages, including the Napoleon
> closed-form package and the cosmology single-ratio inverse
> reconstruction package."

**This V4 response:**

V4 is rebased on current `origin/main` (HEAD `0e7d2a2b`, includes
Napoleon `0e7d2a2b` + cosmology single-ratio `8036af2a`/`b2d562e7`). No
unrelated packages would be deleted on merge.

---

## 4. Closeout flags (honest)

```text
Q_L_EQ_2_OVER_3_RETAINED_FULL_CLOSURE_ON_ORIGIN_MAIN=FALSE
PATH_A_INTERPRETATION_DEFENDED_AS_HYPOTHESIS=TRUE
PATH_A_INTERPRETATION_THEOREM_GRADE_AUTHORITY=FALSE
RUNNER_AUDITS_RETAINED_AUTHORITIES_FROM_DISK=TRUE
RUNNER_DOES_NOT_ASSERT_DISPUTED_SOURCE_DOMAIN_EXCLUSION=TRUE
BRANCH_REBASED_ON_CURRENT_MAIN=TRUE
NO_UNRELATED_PACKAGES_DELETED=TRUE
RESIDUAL_FOR_FULL_CLOSURE=theorem_grade_authority_for_op_uniqueness_to_source_domain_exclusivity_for_backgrounds
```

These supersede the V3 `=TRUE` closure flags.

---

## 5. Path forward

For genuine closure of Q_l = 2/3 (and hence δ_Brannen = 2/9 rad),
either:

**Option A:** Derive a theorem-grade retained authority proving:
- OP Theorem 1's "unique additive CPT-even scalar generator" implies
  scalar observable source-domain exclusivity for ALL backgrounds
  (not just source perturbations), including exclusion of commutant Z.
- This requires showing that the framework's scalar observable VALUES
  on a state with non-local source background K are equal to their
  values on the canonically-descended state E_loc(K). Equivalently:
  scalar observable values are invariant under the difference K - E_loc(K).

**Option B:** Derive a theorem-grade retained authority specifically
about the physical Y_e structure:
- The framework's physical lepton-sector Yukawa amplitude Y_e satisfies
  a² = 2|b|² (equivalently c² = 2, equivalently Q_l = 2/3) by some
  structural framework principle (gauge bridge, partition function
  saddle, cross-sector consistency, etc.).

**Option C:** Accept the OP-uniqueness Path (a) interpretation as a
framework axiom (changes the input stack):
- Add to A0 / OP a clause stating: "scalar observable backgrounds are
  in span{P_x}; non-local backgrounds are excluded."
- This is not derivation, but explicit axiom.

This V4 note + runner provides the strongest defended SUPPORT for the
OP-uniqueness route, but does not close any of A/B/C.

---

## 6. Verification

```bash
python3 scripts/frontier_koide_q_op_uniqueness_source_domain_support.py
```

The runner audits retained authorities from disk:
1. **OP audit:** reads `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`,
   verifies "unique additive CPT-even" appears in the text.
2. **ONSITE audit:** reads `docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`,
   verifies "not an onsite diagonal source function" appears.
3. **CRIT audit:** reads `docs/KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`,
   verifies "z = 0" and "Q = 2/3" appear together.
4. **Algebraic identities** (no closure assertions):
   - Tr(Z) = -1 (sympy)
   - E_loc(K) = (s − z/3) I (algebra)
   - On the orbit: Z has off-diagonal entries (numerical)
5. **CONDITIONAL implication** explicitly flagged:
   - IF the OP-uniqueness Path (a) interpretation is accepted as theorem-grade, THEN Q = 2/3 follows.
   - This implication is recorded as a conditional, not asserted as a closure.

Expected: PASS=N, FAIL=0. The PASSes verify retained authorities exist on
disk + algebraic identities; they do NOT verify the closure step.

---

## 7. Cross-references

- `review.md` on `origin/koide-q-closure-via-op-uniqueness` (commit `85ff7920`) — Codex review of V3 with explicit findings
- `docs/KOIDE_Q_CLOSURE_VIA_OP_UNIQUE_GENERATOR_DOMAIN_THEOREM_NOTE_2026-04-25.md` (V3, on `koide-q-closure-via-op-uniqueness`) — superseded by this V4 framing
- `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` — OP, retained
- `docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md` — ONSITE, retained
- `docs/KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md` — CRIT, retained
- `docs/KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md` — CD, retained
- `docs/KOIDE_Q_OP_LOCAL_DESCENT_PROTOCOL_BOUNDARY_NOTE_2026-04-25.md` (on `codex/land-koide-closure-targets-ab-v2-2026-04-25`) — Codex's V2 boundary note (named the same residual class)
- `docs/KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md` — SO2 (accepted V1 Q-SO(2) algebra as support)
