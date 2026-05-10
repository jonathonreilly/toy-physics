# Cosmological Constant R-Budget Support Note (V1)

---

**This is a support / R-budget formalization note. It does not
establish any retained claim and is conditional on non-retained
upstream authorities.**
For retained claims on the cosmological-constant spectral-gap surface
or its upstream dependencies, see the per-claim notes referenced from
the `## Audit scope` block below.

---

**Date:** 2026-04-29
**Status:** support / R-budget formalization record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / R-budget formalization record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no
**Primary runner:** `scripts/frontier_cosmological_constant_retention_with_r_budget.py`

Formalizes the spectral-gap identity `Λ = λ_1(S^3_R) = 3/R²`
(retained on `main`) into an explicit R-budget statement. The
numerical value of Λ depends on R, and the current framework surface
does not derive that numerical R. Axiom* remains a conditional/human
decision surface rather than a forced premise. No retained or promoted
publication relabel is proposed here. Bare `retained` / `promoted` is
NOT used.

## Audit scope (relabel 2026-05-10)

This file is an **R-budget formalization / support note** layered on
non-retained one-hop upstream authorities. It is **not** a single
retained theorem and **must not** be audited as one. The audit ledger
row for
`cosmological_constant_retention_with_r_budget_theorem_note_2026-04-29`
classified this source as conditional/bounded_theorem with auditor's
repair target:

> audit or repair the listed dependency rows
> (cosmological_constant_spectral_gap_identity_theorem_note,
> universal_gr_discrete_global_closure_note, s3_general_r_derivation_note)
> to retained/equivalent closure, then re-audit this claim.

The minimal-scope response in this PR is to **relabel** this document
as an R-budget formalization support record rather than to repair the
upstream dependency rows here. That repair belongs in dedicated
upstream review-loop passes. Until that work is done:

- This file makes **no** retained-claim assertions of its own.
- The R-budget statement `Λ_framework = 3/R²` with `R = R_Λ`,
  Axiom* conditional decision-surface narrative, and downstream
  numerical-Λ accounting below are **conditional support content
  only** — every step rests on the named non-retained upstream
  authorities.
- The retained-status surface for the spectral-gap identity, the
  S^3_R topology, the discrete GR closure, or any Λ closure is the
  audit ledger (`docs/audit/AUDIT_LEDGER.md`) plus the per-claim
  upstream notes, **not** this R-budget note.
- Retained-grade does **NOT** propagate from this R-budget note to
  any sub-claim, Axiom* decision, or successor closure.

For any retained claim about cosmological-constant retention,
spectral-gap identity, or S^3 topology with general R, audit the
corresponding dedicated upstream note and its runner as a separate
scoped claim — not this R-budget formalization record.

---

**Cited authorities (one-hop deps):**
- [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
  — retained: `Λ_vac = λ_1(S^3_R) = 3/R²` exact function identity.
- [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)
  — retained discrete 3+1 GR closure.
- [S3_GENERAL_R_DERIVATION_NOTE.md](S3_GENERAL_R_DERIVATION_NOTE.md)
  — retained S³ spatial topology with general R.
- [AXIOM_STACK_MINIMALITY_CL4C_NO_GO_THEOREM_NOTE_2026-04-29.md](AXIOM_STACK_MINIMALITY_CL4C_NO_GO_THEOREM_NOTE_2026-04-29.md)
  — historical Block 4 route note for the C1/Axiom* budget surface;
  its forced-Axiom* framing is not used as a live premise here.

---

## 0. Headline

The COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM established
on retained surfaces:

```text
Λ_vac = λ_1(S³_R) = 3/R²    (exact function identity)
```

valid for any R > 0.

The numerical value of Λ requires the absolute value of R, which is
the same `R_Λ` quantity that the Hubble C1 closure target depends on.
The current C1 surface does not derive that numerical value. Axiom*
(Cl_4(C) module on P_A H_cell) is therefore a conditional decision
surface for later science review, not a premise forced by this note.

V1 records this as an explicit R-budget support statement:

```text
Λ_framework = 3/R²    (retained function identity)
R = R_Λ              (bounded; numerical value waits on Axiom* decision)
```

The live result is bounded support: the exact function identity is
available, while the numerical R input remains open on the current
framework surface.

---

## 1. The R-budget support statement

### 1.1 Retained components

```text
Λ_vac = λ_1(S³_R) = 3/R²    (retained, COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM)
exact function identity in R for any R > 0
```

### 1.2 Explicit R-budget

| Budget item | Status | Path to tighten |
|---|---|---|
| R₁: function identity Λ(R) = 3/R² | retained exact | none required |
| R₂: numerical R = R_Λ value | bounded | requires a later C1/Axiom* decision or another derivation |
| R₃: H_inf vacuum-energy match | bounded | gated on R_Λ |
| R₄: Planck observation comparator | retained `Λ_obs ≈ 1.09 × 10⁻⁵² m⁻²` | (admitted observational comparator) |

R₁ is retained exactly. R₂ is the load-bearing open item. R₃ is a
downstream consequence of R₂. R₄ is the comparator.

### 1.3 Numerical readout

With Λ_obs ≈ 1.09 × 10⁻⁵² m⁻², the implied R is:

```text
R = √(3/Λ_obs) ≈ √(2.752 × 10⁵² m²) ≈ 1.66 × 10²⁶ m
```

This is the Hubble radius. The framework's `Λ = 3/R²` identity is
exactly consistent with this R, but the framework does NOT yet derive
this R from internal structure. R remains an open budget item.

---

## 2. Bounded support statement

**Statement (Cosmological Constant R-budget support).**
On the framework's retained discrete 3+1 GR closure surface + retained
S³ spatial topology + spectral-gap identity:

```text
Λ_framework = 3/R²
```

has a bounded support R-budget reading on the actual current surface,
with the budget table:

- R₁ (function identity): retained exact
- R₂ (numerical R): bounded, requires a later C1/Axiom* decision or another derivation
- R₃ (H_inf match): downstream of R₂
- R₄ (Planck Λ_obs): observational comparator

**Status:** bounded support. This note does not propose an effective
retained or promoted relabel.

### Proof

**Step 1.** By COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM,
`Λ_vac = λ_1(S³_R) = 3/R²` is an exact retained function identity
for all R > 0.

**Step 2.** The R numerical value is not derived by the cited current
surface. Axiom* (Cl_4(C) module on P_A H_cell) remains a conditional
route for later science review; without such a decision or another
derivation, R remains open. This is the structural budget item.

**Step 3.** Combining: Λ_framework = 3/R² is exactly budgeted as a
function of R. The budget is honestly decomposed; numerical retention
is not claimed.

---

## 3. Status firewall fields

```yaml
actual_current_surface_status: bounded
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: |
  V1 formalizes COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM
  (retained Λ = 3/R² function identity) into an explicit R-budget
  support statement. No new computation; no retained or promoted
  relabel is proposed.
audit_required_before_effective_retained: false
bare_retained_allowed: false
r_function_identity_status: retained_exact
r_numerical_value_status: bounded_open_c1_surface
h_inf_status: bounded_downstream_of_r
```

---

## 4. What is and is NOT closed

### Closed by V1

1. explicit R-budget formalization
2. separation of the exact function identity from the numerical R input
3. bounded support packaging for later science review

### NOT closed (carried forward)

1. **Numerical R = R_Λ** — open pending a C1/Axiom* decision or another derivation
2. **H_inf vacuum-energy match** — downstream of R
3. **Vacuum-energy hierarchy puzzle** — separate issue (why
   `Λ_obs · M_Pl² ~ 10⁻¹²² × (M_Pl)⁴` is so small) — out of scope

---

## 5. No cascade unlocked

This PR proposes no publication-matrix relabel and no cascade unlock.
Any future Λ relabel requires a separate science decision on the
numerical R budget.

---

## 6. Verification

```bash
python3 scripts/frontier_cosmological_constant_retention_with_r_budget.py
```

PASS=N FAIL=0.

---

## 7. Honest residual

The exact Λ(R) identity remains available, but this note does not make
Λ a retained numerical framework prediction. Full numerical retention
requires a later derivation or an explicit science decision about the
C1/Axiom* surface.
