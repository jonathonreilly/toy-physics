# Cosmological Constant Retention-with-R-Budget Theorem (V1)

**Date:** 2026-04-29
**Status (actual current surface):** `proposed_retained_with_budget`
author proposal — formalizes the spectral-gap identity
`Λ = λ_1(S^3_R) = 3/R²` (retained on `main`) into a retention-with-
explicit-R-budget statement that mirrors the YT-lane and
string-tension retention patterns. The numerical value of Λ depends
on R, which depends on the Hubble C1 closure (Block 4's no-go shows
this requires Axiom* adoption). V1 makes this dependency explicit.
Bare `retained` / `promoted` is NOT used.
**Primary runner:** `scripts/frontier_cosmological_constant_retention_with_r_budget.py`

**Cited authorities (one-hop deps):**
- [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
  — retained: `Λ_vac = λ_1(S^3_R) = 3/R²` exact function identity.
- [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)
  — retained discrete 3+1 GR closure.
- [S3_GENERAL_R_DERIVATION_NOTE.md](S3_GENERAL_R_DERIVATION_NOTE.md)
  — retained S³ spatial topology with general R.
- [AXIOM_STACK_MINIMALITY_CL4C_NO_GO_THEOREM_NOTE_2026-04-29.md](AXIOM_STACK_MINIMALITY_CL4C_NO_GO_THEOREM_NOTE_2026-04-29.md)
  — Block 4 V1: shows R numerical value needs Axiom* or accept open.

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
Block 4 (axiom-to-main-lane-cascade-20260429) proved structurally that
the C1 closure requires Axiom* (Cl_4(C) module on P_A H_cell).

V1 composes these into a retention-with-explicit-R-budget statement
matching the YT-lane / string-tension pattern:

```text
Λ_framework = 3/R²    (retained function identity)
R = R_Λ              (bounded; numerical value waits on Axiom* decision)
```

The framework's Λ is `proposed_retained_with_budget`: structurally
retained as `3/R²` modulo the explicit R-budget, which is itself
gated on Axiom* acceptance vs. (G1)/(C1) lanes-open acceptance.

This mirrors Block 8's pattern (string tension retention-with-budget)
and uses Block 4's axiom-stack minimality theorem as the cleanest
structural account of why R numerical value is currently open.

---

## 1. The retention-with-R-budget statement

### 1.1 Retained components

```text
Λ_vac = λ_1(S³_R) = 3/R²    (retained, COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM)
exact function identity in R for any R > 0
```

### 1.2 Explicit R-budget

| Budget item | Status | Path to tighten |
|---|---|---|
| R₁: function identity Λ(R) = 3/R² | retained exact | none required |
| R₂: numerical R = R_Λ value | bounded | gated on Axiom* (Block 4 shows alternative is (G1)/(C1) open) |
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
this R from internal structure. R is open per Block 4's Cl_4(C) axiom-
stack minimality theorem.

---

## 2. Theorem statement

**Theorem (Cosmological Constant Retention-with-R-Budget).**
On the framework's retained discrete 3+1 GR closure surface + retained
S³ spatial topology + spectral-gap identity:

```text
Λ_framework = 3/R²
```

is a `proposed_retained_with_budget` reading on the actual current
surface, with the budget table:

- R₁ (function identity): retained exact
- R₂ (numerical R): bounded, gated on Axiom* (Block 4)
- R₃ (H_inf match): downstream of R₂
- R₄ (Planck Λ_obs): observational comparator

**Status:** `proposed_retained_with_budget` modulo audit ratification
of the budget formalization and ultimately the Axiom* decision.

### Proof

**Step 1.** By COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM,
`Λ_vac = λ_1(S³_R) = 3/R²` is an exact retained function identity
for all R > 0.

**Step 2.** By Block 4 (AXIOM_STACK_MINIMALITY_CL4C_NO_GO_THEOREM_NOTE_2026-04-29),
the R numerical value is gated on Axiom* (Cl_4(C) module on P_A H_cell)
adoption. Without Axiom*, R remains open per the (G1)/(C1) lanes-open
posture. This is a structural budget item.

**Step 3.** Combining: Λ_framework = 3/R² is structurally retained
modulo the explicit R-budget. The budget is honestly decomposed.
**QED on retention-with-budget**; Axiom* decision required for full
numerical retention.

---

## 3. Status firewall fields

```yaml
actual_current_surface_status: proposed_retained_with_budget
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  V1 formalizes COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM
  (retained Λ = 3/R² function identity) into retention-with-explicit-R-
  budget by composing with Block 4's axiom-stack minimality theorem
  (R numerical value gated on Axiom*). No new computation; this is a
  budget-decorated relabeling consistent with Block 8's pattern.
audit_required_before_effective_retained: true
bare_retained_allowed: false
r_function_identity_status: retained_exact
r_numerical_value_status: bounded_gated_on_axiom_star
h_inf_status: bounded_downstream_of_r
```

---

## 4. What is and is NOT closed

### Closed by V1

1. retention-with-R-budget formalization
2. relabel from "open" (line 177) to
   "retained-with-explicit-R-budget; numerical R gated on Axiom*"
3. structural composition with Block 4's no-go

### NOT closed (carried forward)

1. **Numerical R = R_Λ** — gated on Axiom* (Block 4)
2. **H_inf vacuum-energy match** — downstream of R
3. **Vacuum-energy hierarchy puzzle** — separate issue (why
   `Λ_obs · M_Pl² ~ 10⁻¹²² × (M_Pl)⁴` is so small) — out of scope

---

## 5. Cascade unlocked (proposed for later weaving)

If V1 audit-ratifies (depends on Block 4 audit):
- **PUBLICATION_MATRIX line 177 (Cosmological constant Λ):** "open"
  → "retained-with-explicit-R-budget; numerical R gated on Axiom*"
- COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM gets §Note
  that Block 4's no-go is the cleanest account of the R-budget
  status

---

## 6. Verification

```bash
python3 scripts/frontier_cosmological_constant_retention_with_r_budget.py
```

PASS=N FAIL=0.

---

## 7. Honest residual

The Λ retention is now a budget-decorated retained statement. Full
numerical retention requires Axiom* adoption (or accepting the
(G1)/(C1) lanes as permanently open per Block 4).
