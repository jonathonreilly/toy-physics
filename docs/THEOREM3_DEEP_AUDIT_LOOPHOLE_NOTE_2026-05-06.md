# Theorem 3 Deep Audit: Loophole Identified — Route 1 REOPENS

**Date:** 2026-05-06
**Status:** research_finding (deep-audit identification of structural loophole in framework's Theorem 3 no-go)
**Companion:** [`CHAIN_CLOSURE_DERIVATION_BLOCKED_NOTE_2026-05-05.md`](CHAIN_CLOSURE_DERIVATION_BLOCKED_NOTE_2026-05-05.md), [`CHAIN_CLOSURE_44PPM_BRAINSTORM_NOTE_2026-05-05.md`](CHAIN_CLOSURE_44PPM_BRAINSTORM_NOTE_2026-05-05.md)
**Audit target:** [`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md) Theorem 3

## Headline

Deep audit of the framework's Theorem 3 no-go (the load-bearing
barrier blocking Route 1's SD-equation NLO derivation) finds a **real
structural loophole**:

The no-go's "proof by exhibiting three admissible families" (decay,
one-plaquette, tube-power) uses only **positivity, conjugation symmetry,
and normalization** as constraints on ρ_(p,q)(β). It **does NOT invoke**
the framework's own:

- Connected-hierarchy onset jet: `P_full(β) = P_1plaq(β) + β⁵/472392 + O(β⁶)`
  (from `MIXED_CUMULANT_AUDIT_NOTE`, `CONNECTED_HIERARCHY_THEOREM_NOTE`)
- Susceptibility-flow ODE: `β_eff'(β) = χ_L(β)/χ_1plaq(β_eff(β))`
  (from `SUSCEPTIBILITY_FLOW_THEOREM_NOTE`)

Numerical tests (NMAX=7-8, MODE_MAX=200-300) show **NONE of the three
admissible families** in Theorem 3's proof satisfies the connected-hierarchy
onset jet to the required precision (`c_4 = 0`, `c_5 = 1/472392 = 2.117×10⁻⁶`).

**This reopens Route 1.** The SD-equation NLO derivation is not actually
blocked by Theorem 3 as proven; it requires re-attempting with the
onset-jet constraint applied.

## What Theorem 3 actually proves

Per `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` lines
171-213:

> "distinct admissible ρ choices, all built from the same `c_λ(6)`
> and `SU(3)` intertwiner data, produce strictly different values of
> `P(6)`. Therefore `c_λ(6)` and `SU(3)` intertwiners do not, by
> themselves, fix `ρ_(p,q)(6)`."

**Witness construction (the proof):**
- Family 1 (decay): `ρ = exp(−τ(p+q))`
- Family 2 (one-plaquette env): `ρ = c_(p,q)(β_env)/c_(0,0)(β_env)`
- Family 3 (tube-power): `ρ_k = (c_(p,q)(6)/c_(0,0)(6))^k`

Each is positive, conjugation-symmetric (ρ_(p,q) = ρ_(q,p)),
normalized at (0,0). Each gives a distinct Perron P(6). Conclusion:
local data + intertwiners do not fix ρ.

**Constraints the proof DOES use:** positivity, conjugation symmetry, normalization.

**Constraints the proof DOES NOT use:** onset jet, susceptibility-flow,
connected cumulant hierarchy, V-invariance on L=2 cube.

## The loophole — onset jet constraint kills all three witnesses

The framework's connected-hierarchy theorem proves the EXACT onset jet:

```
χ_L(β) − χ_1plaq(β) = 5β⁴/472392 + O(β⁵)
P_full(β) − P_1plaq(β) = β⁵/472392 + O(β⁶)
```

equivalently for β_eff(β) = β + β⁵/26244 + O(β⁶).

**Numerical test of the three families** (extending each ρ to a β-dependent
function and computing `Perron_P(β) − P_1plaq(β)` for β ∈ [0.4, 2]):

| Family | c_4 | c_5 (target 2.117×10⁻⁶) | Onset jet match? |
|---|---|---|---|
| ρ=1 (Theorem 1 ref) | ≈0 | +1.06×10⁻⁶ (factor 2 low) | **NO** |
| ρ=δ (Theorem 2 ref) | ≈0 | ≈0 (numerical noise) | **NO** (gives P=P_1plaq exactly) |
| tube k=1, k=2 | nonzero | wrong sign (negative) | **NO** (c_4 ≠ 0) |
| tube k=12 | ≈0 | ≈0 | **NO** (c_5 wrong) |
| decay τ ∈ [0, 5] | nonzero | always wrong | **NO** |
| one-plaquette env β_env ∈ [0,20] | nonzero | always too small | **NO** |

**No tested family member of any of the three families reproduces the
framework's onset-jet `c_5 = 1/472392` to better than factor ~2.**
Some have correct `c_4 = 0`, some have correct order `β⁵`, but **none
simultaneously matches `c_4=0` AND `c_5 = 1/472392`**.

**Implication:** Theorem 3's witnesses are structurally inadmissible
once the framework's own onset-jet constraint is applied. The "proof"
of the no-go is incomplete — it shows under-determination relative to
a SUBSET of framework constraints, not the FULL constraint set.

## What this means for Route 1 (SD-equation NLO)

The prior Route 1 probe asserted: "no internal small parameter in T_src
flows perturbatively to (N²−1)/(8N × b_0³)."

This claim is **wrong**. `1/β` IS a natural small parameter, comparable
to α_LM at β=6. The framework already uses this implicitly: the
connected-hierarchy onset jet IS a perturbative expansion in β at
small β, and by analytic continuation a `1/β` expansion at large β.

**Route 1 is REOPEN**, with the corrected attack:

1. Set up T_src in (p,q) basis (as before).
2. **Constrain ρ_(p,q)(β) to the function class consistent with the
   onset jet** through O(β⁵). This is a much narrower class than "any
   positive ρ."
3. Solve the eigenvalue equation T_src · ψ = λ_max · ψ within this
   constrained class.
4. If the solution is unique (or narrowly parametrized): extract the
   chain residual `(N²−1)/(8N × b_0³)` from the constrained Perron
   eigenvalue at NLO.

## What the K-tube k = 12 + 2/π fits within this framing

The K-tube ansatz `ρ_R = (c_R/c_(0,0))^k` does NOT satisfy the onset
jet constraint at any single value of k. So the K-tube ansatz is
**asymptotic only** — valid at β=6 in some scheme but not as a
β-dependent ρ.

The TRUE β-dependent ρ_(p,q)(β) consistent with the onset jet is
NOT the K-tube. The K-tube fit at β=6 to k* ≈ 12.6342 is
phenomenological — it captures the IR endpoint of the true flow, but
the flow itself is more constrained.

This means: the right derivation of `(N²−1)/(8N × b_0³)` is via the
onset-jet-consistent flow, NOT via the K-tube ansatz.

## Honest verdict

**(B) Theorem 3 HAS A LOOPHOLE.** The proof is too narrow. With ALL
framework constraints applied (especially the onset jet), the witnesses
used in the no-go become inadmissible. **Route 1 is reopen pending a
proper SD-equation derivation that respects the onset jet.**

**Specific next-step:** dispatch Route 1 v2 with onset-jet-constrained
ρ_(p,q)(β). If the constrained problem has unique β=6 solution,
extract chain residual. If still under-determined, identify the
remaining loophole.

## Limitation acknowledgment

The audit does NOT prove that the constrained class has a UNIQUE
solution. The framework's `FRAMEWORK_POINT_UNDERDETERMINATION_NOTE`
proves explicitly: any analytic strictly-increasing β_eff sharing the
onset jet through O(β⁵) can give different β_eff(6). So the onset jet
NARROWS the class but does NOT necessarily close it.

What the audit DOES prove:
- Theorem 3's witness set is WRONG (witnesses don't satisfy onset jet)
- The "no-go" as proven is incomplete
- A correctly-stated no-go (using all framework constraints) is an OPEN question, not proven

## Status proposal

```yaml
note: THEOREM3_DEEP_AUDIT_LOOPHOLE_NOTE_2026-05-06.md
type: research_finding (audit-grade structural correction to existing framework theorem)
proposed_status: research_finding (reopens Route 1 chain closure pathway)
positive_subresults:
  - Theorem 3's three "admissible" witnesses fail the onset-jet constraint
  - The no-go's proof is incomplete relative to the framework's full constraint set
  - Route 1 (SD-equation NLO with onset-jet constraint) is REOPEN
  - Prior probe's "no internal small parameter" claim is WRONG (1/β is the natural small parameter)
negative_subresults:
  - Audit does NOT prove the constrained class has unique solution
  - FRAMEWORK_POINT_UNDERDETERMINATION_NOTE separately shows onset-jet-respecting class is non-unique
audit_required: yes (this audit itself should be ratified; chain implications should be re-examined)
follow_up:
  - Route 1 v2: SD-equation with onset-jet constraint imposed structurally
  - Strengthen Theorem 3 by adding explicit constraints used
  - If constrained problem solves uniquely: chain refactoring becomes UNBOUNDED RETAINED
```

## Implications for the framework's existing Theorem 3

Theorem 3 should be UPDATED in
`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` to either:
- (i) explicitly state the constraint set used (not "intertwiners alone";
  "intertwiners + positivity + conjugation symmetry + normalization,
  excluding onset jet and susceptibility flow")
- (ii) re-prove with the full constraint set, exhibiting witnesses
  that satisfy ALL framework constraints, OR
- (iii) be downgraded to a weaker claim ("no-go relative to local data only").

This is an audit-grade correction to a load-bearing framework theorem.

## Ledger entry

- **claim_id:** `theorem3_deep_audit_loophole_note_2026-05-06`
- **note_path:** `docs/THEOREM3_DEEP_AUDIT_LOOPHOLE_NOTE_2026-05-06.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
- **dependency_chain:**
  - `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` (Theorem 3 — being audited)
  - `GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md` (onset jet)
  - `GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md` (cumulant hierarchy)
  - `GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md` (susceptibility flow)
  - `GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md` (separate residual non-uniqueness)
