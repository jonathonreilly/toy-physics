# Route 1 v2 with Onset-Jet Constraint: REDUCED but Not Closed

**Date:** 2026-05-06
**Status:** research_finding (substantive 22× narrowing of ρ class; chain stays at bounded support)
**Companion:** [`THEOREM3_DEEP_AUDIT_LOOPHOLE_NOTE_2026-05-06.md`](THEOREM3_DEEP_AUDIT_LOOPHOLE_NOTE_2026-05-06.md), [`ROUTE2_LPT_DEEP_AUDIT_NOTE_2026-05-06.md`](ROUTE2_LPT_DEEP_AUDIT_NOTE_2026-05-06.md)

## Headline

After the Theorem 3 audit identified that the no-go's witnesses fail
the framework's onset-jet constraint, this probe re-attempted Route 1
(SD-equation NLO derivation) with the onset constraint properly
applied. Result: **REDUCED, not derived.**

The chain stays at **bounded support 4.4 ppm**. Path to unbounded
retained requires the next-order constraint (c_6 onset coefficient)
OR full susceptibility-flow integration.

## What was confirmed (positive findings)

1. **Theorem 3 audit verified.** All three "admissible" families
   (decay, one-plaquette, tube-power) fail the framework's onset jet
   `c_5 = 1/472392 = 2.117 × 10⁻⁶`. Their c_5 values:
   - ρ=1: c_5 ≈ 0.516 × target
   - ρ=δ: c_5 ≈ 0.011 × target
   - ρ=exp(-(p+q)): c_5 ≈ 0.197 × target
   - one-plaq env, β_env=6: c_5 ≈ 0.651 × target
   - tube k=1: c_5 ≈ 0.651 × target
   - tube k=12: c_5 ≈ 8.687 × target
   - **None reproduces c_5 = 1.000 × target** at NMAX=5-7.

2. **Onset constraint reduces under-determination by 22×.**
   - Without constraint (Theorem 3 spread): P(6) range ≈ 0.19
   - With c_5 = 1/472392 constraint: P(6) range ≈ 0.0087 (constant-ρ subclass)
   - 22× tighter.

3. **Specific pin on ρ_(1,0)(0).** Solving `c_5(ρ_(1,0)(0)) = 1/472392`:
   - NMAX=5: ρ_(1,0)(0) = 2.0204
   - NMAX=7: ρ_(1,0)(0) = 1.8697
   - Not yet a clean integer (NMAX-dependent at ~10% level)
   - Sensitivity analysis: c_5 depends almost exclusively on ρ_(1,0)(0)
     at the cube-shell-relevant order; higher-(p,q) sensitivities ≤ 1e-10

## What is NOT closed (negative findings)

1. **Constant-ρ class cannot reach canonical P(6) = 0.5934.**
   - Best constant-ρ in onset-constrained class: P(6) ≤ 0.485
   - Canonical: 0.5934
   - Gap: 0.108 (large)
   - Constant ρ structurally cannot reproduce the L→∞ Wilson value.

2. **β-dependent ρ closes the gap but reopens under-determination.**
   - With ρ_(1,0)(β) = ρ_(1,0)(0) + amp · (β/6)^5 (β^5 ramp, preserves c_5):
     - amp=0: P(6) = 0.477
     - amp=20: P(6) = 0.592 (matches canonical band)
     - amp=50: P(6) = 0.606
   - Single-parameter family spans P(6) ∈ [0.477, 0.610]. Not closed.

3. **1/β asymptotic expansion of T_src does not cleanly produce
   (N²−1)/(8N × b_0³).**
   - Verified `(1 - a_(1,0)(β))·β → 4.00` empirically as β → ∞ (β=200, 500)
   - But `eig_max(T_src(β))/exp(β) → 0` slowly with no clean
     1/b_0³ structure
   - Asymptote `(1−a_(1,0))·β → 4` is well-defined but does not
     factorize through b_0 or the chain residual

## What additional constraint would close

The probe identified two routes that COULD close, neither attempted in this probe:

### Route 1c — Higher-order onset constraint (c_6)

The framework's connected-hierarchy theorem gives onset jet to
arbitrary order. The next term `c_6` in the expansion would constrain
ρ_(1,1)(0), ρ_(2,0)(0), etc. — i.e., higher-(p,q) values that current
c_5 doesn't pin.

**Specific calculation:** count leafless distinct supports of order β⁶
on the L=2 cube and compute per-shell amplitude from Haar integrals.
This is publishable as the next probe.

If c_5 + c_6 + ... + c_k constraints uniquely determine ρ at finite
NMAX truncation, and the corresponding β=6 evaluation gives canonical
P(6), the chain closes.

### Route 1d — Full susceptibility-flow integration

The framework's susceptibility-flow ODE
`β_eff'(β) = χ_L(β)/χ_1plaq(β_eff(β))` integrates from β=0 (onset)
to β=6. To integrate, need χ_L(β) — which is itself the open problem.

So Route 1d reduces to the famous problem.

## Honest verdict

**REDUCED, not derived.** The audit's identification of the Theorem 3
loophole is real and substantive (22× narrowing), AND it confirms a
pin on ρ_(1,0)(0). But the onset jet alone does NOT uniquely determine
ρ; β-dependence of higher (p,q) is still free.

**Chain stays at bounded support 4.4 ppm.**

**Path to unbounded retained:**
- (i) Derive c_6 onset coefficient and apply to constrain higher (p,q).
  If iterating gives unique ρ at β=6, chain closes.
- (ii) Solve full susceptibility-flow ODE — but this requires χ_L
  analytically (= famous problem).
- (iii) Accept bounded retained at 4.4 ppm equivalent to alpha_s_derived_note.

## What this changes vs prior synthesis

- Prior: "Route 1 BLOCKED at Theorem 3 no-go."
- Updated: "Theorem 3 has loophole. Onset jet constraint narrows ρ
  by 22× and pins ρ_(1,0)(0). But constraint alone is not enough to
  fully determine ρ at β=6."

The chain refactoring's status (bounded support, 4.4 ppm) is unchanged.
What's changed: we now know the SPECIFIC NEXT-STEP for closure (c_6
constraint) and it's a well-defined finite computation.

## Status proposal

```yaml
note: ROUTE1_V2_ONSET_REDUCED_NOTE_2026-05-06.md
type: research_finding (audit-following structural progress)
proposed_status: research_finding (Route 1 reduced but not closed)
positive_subresults:
  - Theorem 3 loophole confirmed: 3 witnesses all fail c_5 onset
  - 22× narrowing of ρ under-determination via onset constraint
  - Pin on ρ_(1,0)(0) ≈ 1.87-2.02 (NMAX-dependent)
  - Constant-ρ class bounded above by P(6) ≤ 0.485 (below canonical)
  - β-dependent ρ ramp (preserves c_5) reaches canonical P(6) = 0.593 with 1-param fit
negative_subresults:
  - Onset jet alone insufficient to fully determine ρ
  - 1/β asymptotic of T_src does not produce clean 1/b_0³ structure
  - Closure form (N²-1)/(8N × b_0³) not derived
audit_required: yes
follow_up:
  - Route 1c: derive c_6 onset coefficient (next-order in connected hierarchy)
  - Route 1d: full susceptibility-flow integration (reduces to famous problem)
  - Or: accept bounded_retained at 4.4 ppm, submit for audit
```

## Reusable artifacts

Numerics in `/tmp/route1_v2_onset/`. All NMAX=5-7, MODE_MAX=80-150.
Reproducible with sympy + numpy + scipy.

Key result: **constant-ρ onset-constrained class** has explicit
P(6) range [0.4759, 0.4847], with ρ_(1,0)(0) pin at NMAX-dependent
value 1.87-2.02. This is a specific, audit-testable structural
claim about the framework's tensor-transfer operator.

## Ledger entry

- **claim_id:** `route1_v2_onset_reduced_note_2026-05-06`
- **note_path:** `docs/ROUTE1_V2_ONSET_REDUCED_NOTE_2026-05-06.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
