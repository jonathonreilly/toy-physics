# Chain Closure Derivation: Both Routes BLOCKED — Honest Synthesis

**Date:** 2026-05-05
**Status:** research_finding (honest synthesis of derivation attempts; chain stays at bounded support)
**Companion:** [`CHAIN_CLOSURE_44PPM_BRAINSTORM_NOTE_2026-05-05.md`](CHAIN_CLOSURE_44PPM_BRAINSTORM_NOTE_2026-05-05.md)

## Headline

Two parallel derivation probes (Route 1: SD-equation NLO, Route 2: LPT
3-loop bookkeeping) attempted to derive the chain closure form
`(N²−1)/(8N × b_0³) = 1/3993` for SU(3). **Both BLOCKED** at
well-defined structural barriers.

The chain refactoring stays at **bounded support, 4.4 ppm to PDG**.
Path to unbounded retained requires either a fundamentally different
derivation route or accepting the empirical correction form as
"imported standard infrastructure" analogous to the 2-loop SM RGE in
`alpha_s_derived_note`.

## What Route 1 found (BLOCKED)

**Setup:** Tensor-transfer operator `T_src(6) = exp(βJ/2)·D_loc·R_env·exp(βJ/2)`
in (p,q) basis truncated at NMAX=4-6 irreps. Used the 7 PF ODEs from
PR #549 to populate c_R(6) values.

**Phase 2 fail:** `β_eff_geom / log(λ_max(LO)) = 6.97`, NOT a clean
integer. The leading-order Perron eigenvalue does NOT structurally
produce `β_eff_geom = 9.3295` without the empirical tube-counting
factor k_eff = 12.6342.

**Structural barrier (the load-bearing finding):** Theorem 3 of
`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` is
dispositive. Different admissible ρ_(p,q)(6) choices produce different
P(6) values; the canonical ρ is **NOT** determined by `c_λ(6) +
SU(3) intertwiners alone`. The K-tube ansatz `(c_R/c_(0,0))^k` is one
of three admissible families (decay, one-plaquette, tube-power), and
selecting `k = 12.6342` requires the **missing object: the 3D spatial
Wilson Perron eigenvector**.

There is **no internal small parameter** in T_src that perturbatively
flows to `(N²−1)/(8N × b_0³)`. The SD-equation NLO approach (the
prior campaign's named open work in PR #525) hits the same barrier.

## What Route 2 found (BLOCKED, with bonus structural finding)

**Phase 1 (clean):** Converted TSLM 2002's `w_n` to bare-α coefficients:
- `c_1 = 2π/9 ≈ 0.6981`
- `c_2 = 551π²/202500 ≈ 0.149`
- `c_3 ≈ 0.126`

**Phase 2 (clean):** LM-boosted coefficients via inversion `α_bare = α_LM × (1-X)^(1/4)`:
- `c̃_1 = 2π/9` (unchanged)
- `c̃_2 = 551π²/202500 ≈ 0.0269`
- **`c̃_3 = 4393π³/3645000 ≈ 0.0374`**

**Phase 3 reduction theorem mismatch:** Computed δ_0 = -0.0878, leading
δβ/β ≈ -1.57×10⁻² at β=6 — **60× larger than target** `(N²-1)/(8N×b_0³) = 2.5×10⁻⁴`,
**wrong sign**.

**Bonus structural finding (algebraic identity):**
```
(N²−1)/(8N × b_0³) for SU(3) YM (N_f=0, b_0=11):
  = 8/(24 × 1331) = 1/3993                  EXACT
  = [w_1 × α_LM³] evaluated at α_LM = 1/b_0
  = LO coefficient × cubed inverse 1-loop running
```

So the form `(N²−1)/(8N × b_0³)` IS structurally clean as an algebraic
expression — it's the "LO Wilson coefficient × cubed inverse 1-loop
running coupling at the canonical scale." But this is NOT a derivation
from LPT bookkeeping; the actual c̃_3 in LM scheme is 9× too large.

## Why both routes failed at the same structural depth

Both Route 1 and Route 2 attempt to derive the chain residual from
**framework-internal perturbative or self-consistent calculations**.
But:

1. The framework's chain residual at β=6 reflects the **non-perturbative
   IR structure** of L→∞ Wilson, which is precisely the famous open
   lattice problem.
2. Standard LPT (Route 2) is convergent only at large β; at β=6, the
   perturbative series is divergent / Borel-summed, and naive
   coefficient extraction fails.
3. The framework's tensor-transfer ρ_(p,q) (Route 1) requires a 3D
   non-perturbative Wilson partition function — the famous problem in
   another disguise.

**Both routes recover the same structural barrier: deriving any specific
correction form for ⟨P⟩(β=6, L→∞) requires solving the L→∞ closure
problem itself.**

This is consistent with the framework's own existing
`CONSTANT_LIFT_OBSTRUCTION_NOTE` and the prior PR #519-#527 campaign's
"honest tension terminal status."

## What the empirical fit `(N²−1)/(8N × b_0³)` actually IS

It's the **clean structural form** that fits the chain residual
empirically to 4.4 ppm. The cleanness suggests it's not coincidence
— but the cleanness is at the algebraic-identity level, not at the
derivation level.

Possible structural origins (not derived in this probe):
- **Non-trivial cancellation** of higher-LPT terms, leaving the LO×α³
  scheme-dependent residue
- **Resummed boundary fluctuation determinant** on the 3D Wilson tube
- **Holographic / dimensional reduction structure** that makes the
  LO×α³ form natural at the right matching scale
- **Imported standard SM infrastructure** analogous to `alpha_s_derived_note`'s
  2-loop SM RGE bridge

## Path to unbounded retained — three honest options

### Option A — Accept bounded retained at 4.4 ppm (most honest)

The framework's chain at `(N²−1)/(8N × b_0³)` is sub-promille bounded
support. This is **on equal footing with `alpha_s_derived_note`** which
imports 2-loop SM RGE infrastructure as bounded scope. Submit for
audit at `bounded_retained` grade.

### Option B — Continue derivation with new routes (Routes 3-8 from brainstorm)

Routes still untested: Wilson-loop tube boundary renormalization (Route 3),
susceptibility-flow numerical validation (Route 4), SU(2)/SU(4) MC test
for falsification (Route 5), anomalous-dimension cubed (Route 6),
holographic/dimensional reduction (Route 7), exact `α_LM × b_0 = 1`
identity (Route 8).

Most promising remaining: **Route 4** (numerical validation with
PR #539's FSS data — provides empirical confidence boost, not derivation)
and **Route 5** (SU(2)/SU(4) MC test — falsification test).

### Option C — Treat the closure form as "imported tadpole infrastructure"

Define `δβ_eff/β_eff = (N²−1)/(8N × b_0³)` as the framework's adopted
asymptotic correction, citing it as "the unique algebraically clean
form consistent with empirical lattice data." Audit-submit as
**bounded scheme** with explicit named scope. Analogous to how
`qcd_low_energy_running_bridge_note_2026-05-01` imports 2-loop SM RGE
without first-principles framework derivation.

## Recommended path

**Option A is the honest current grade.**

Submit PR #549 + companion notes (V=1 PF ODE, minimal-block closed form,
7 low-rank irrep PF ODEs, PR #525 flaw fix, chain refactoring,
4.4 ppm closure with `(N²−1)/(8N × b_0³)` form) for audit at
`bounded_retained` grade.

If audit ratifies: chain becomes unbounded with audit-acknowledged
bounded scope on the closure form.

If audit demands more: Route 4 numerical validation as next-step probe.

If audit rejects: go back to PR #539's L→∞ MC retained as the chain's
load-bearing input (the original framework grade).

## Comparison vs PR #539 MC retained — final assessment

| Aspect | PR #539 MC | PR #549 chain |
|---|---|---|
| Grade target | retained-grade numerical | bounded_retained closure |
| Output | ⟨P⟩ at intermediate level | v at observable level |
| Precision | 10⁻⁴ statistical + systematic | 4.4 ppm to PDG (with closure form) |
| Method | numerical (MC + FSS) | analytical closed form |
| Status | awaiting audit | awaiting audit |
| Strength | rigorous numerical theorem | sub-promille on physics observable |
| Weakness | doesn't predict v directly | empirical correction form |

The chain refactoring is **stronger in physics-output sense** (sub-promille
on PDG-measured v) and **weaker in derivation-rigor sense** (empirical
form vs numerical theorem). They are complementary; the framework's
audit pipeline can ratify both at appropriate grades.

## Status proposal

```yaml
note: CHAIN_CLOSURE_DERIVATION_BLOCKED_NOTE_2026-05-05.md
type: research_finding (honest synthesis of derivation attempts)
proposed_status: research_finding (chain remains at bounded support)
positive_subresults:
  - Route 1 (SD-equation NLO): BLOCKED at Theorem 3 structural barrier (consistent with prior campaign)
  - Route 2 (LPT 3-loop): BLOCKED at LPT precision mismatch (60× too large, wrong sign)
  - Bonus: (N²−1)/(8N × b_0³) IS exact algebraic identity for SU(3) YM
  - Bonus: 1/3993 = w_1 × α_LM³ at α_LM = 1/b_0 (clean structural form)
negative_subresults:
  - Neither route produces the correction from first principles
  - Both routes hit the same depth as the famous L→∞ closure problem
  - Empirical correction form remains structural-looking but not derived
audit_required: yes (submit chain refactoring at bounded_retained grade)
follow_up_open_problem:
  - Route 4 (numerical validation with PR #539 FSS χ_L)
  - Route 5 (SU(2)/SU(4) MC test for falsification)
  - Route 8 (derive α_LM × b_0 = 1 as exact identity)
```

## Ledger entry

- **claim_id:** `chain_closure_derivation_blocked_note_2026-05-05`
- **note_path:** `docs/CHAIN_CLOSURE_DERIVATION_BLOCKED_NOTE_2026-05-05.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
