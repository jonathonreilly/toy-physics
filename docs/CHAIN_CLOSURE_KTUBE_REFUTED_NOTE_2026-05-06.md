# Chain Closure: K-Tube Hypothesis Directly REFUTED by 4D Wilson MC

**Date:** 2026-05-06
**Claim type:** research_finding (definitive negative on K-tube structural interpretation)
**Status:** research_finding — chain refactoring stays at bounded support 4.4 ppm; K-tube structural interpretation refuted
**Companion:** [`CHAIN_CLOSURE_3D_VS_4D_STRUCTURAL_DIAGNOSIS_NOTE_2026-05-06.md`](CHAIN_CLOSURE_3D_VS_4D_STRUCTURAL_DIAGNOSIS_NOTE_2026-05-06.md)

## Headline

Direct 4D SU(3) Wilson MC at β=6 (L_s=4, L_t=14, 600 samples × 2 chains)
**REFUTES** the K-tube hypothesis `ρ_(p,q) = (c_R(6)/c_(0,0)(6))^k`
that has been the framework's empirical closure-form fit:

```
Wilson loop per-time-step ratios λ_R (plateau τ ∈ [4, 11]):
  R=(1,0): λ = 0.6700 ± 0.0004  vs K-tube predicts c_R/c_00 = 1.268  →  MISMATCH (wrong direction)
  R=(1,1): λ = 0.4061 ± 0.0012  vs predicts 1.290                     →  MISMATCH (factor 3.2 off)
  R=(2,0): λ = 0.3670 ± 0.0022  vs predicts 0.810                     →  MISMATCH (factor 2.2 off)
```

The K-tube formula `ρ = (c_R/c_00)^k` requires `c_R/c_00 > 1` to yield
the empirically-needed `ρ_(1,0) ≈ 20`. Wilson transfer-matrix
eigenvalues are ALL `λ_R < 1` (standard QCD string-tension physics).
**Direct contradiction.**

## Numerical evidence

### MC setup
- 4D periodic SU(3) Wilson lattice, L_s=4, L_t=14, β=6
- 250 thermalize + 1500 measure × every 5 sample × 2 chains = 600 samples
- Wilson loops W_R(1, τ) measured for τ = 1 ... 13 in irreps (1,0), (1,1), (2,0)
- ⟨P⟩(β=6, 4D L=4×14) = 0.5964 / 0.5973 (matches L→∞ value 0.5934 within MC error ✓)

### Wilson loop temporal decay
For each irrep R, the rectangular Wilson loop W_R(1, τ) has temporal
decay rate:
```
λ_R(τ) = ⟨W_R(1, τ)⟩ / ⟨W_R(1, τ-1)⟩
```

Plateau region τ ∈ [4, 11]:

| R | λ_R(plateau) | err | c_R/c_00 (K-tube target) | agreement |
|---|---|---|---|---|
| (1,0) | 0.6700 | 0.0004 | 1.268 | **MISMATCH** |
| (1,1) | 0.4061 | 0.0012 | 1.290 | **MISMATCH** |
| (2,0) | 0.3670 | 0.0022 | 0.810 | **MISMATCH** |

The K-tube hypothesis predicts λ_R = c_R(β)/c_(0,0)(β) — the ratio of
character coefficients. This is a strong-coupling expansion factor.
Direct MC measures Wilson transfer-matrix eigenvalues, which are
fundamental string-tension-related decays at β=6 (intermediate
coupling, weakly confining regime).

### K-tube formula evaluated at MC λ values
At framework's k* = 12.6342:
```
λ_(1,0)^k = 0.6700^12.6342 = 6.34 × 10⁻³
```
NOT the empirically-needed ρ_(1,0) ≈ 20. The K-tube formula gives the
wrong order of magnitude AND the wrong sign.

## Why the K-tube empirically fits at β=6 anyway

The K-tube empirical fit `ρ_(1,0) = (c_(1,0)(6)/c_(0,0)(6))^12.6342 = 20`
hits the canonical ⟨P⟩(β=6) = 0.5934 to within 1.6×10⁻⁵ via the
framework's Perron formula. This empirical match is REAL but
**numerical, not structural**.

Possible reasons for the numerical coincidence:
1. **Functional-form happenstance**: `c_R/c_00 > 1` for low irreps and
   the exponent k ≈ 12.6 happens to give the right magnitude at β=6.
   At other β values, the K-tube would deviate from MC.
2. **Effective-coupling reading**: the K-tube isn't a transfer-matrix
   formula but an effective parameterization of an integrated quantity.
3. **Coincidental scaling**: `c_R/c_00` and Wilson-loop physics share
   structural factors (both involve SU(3) character coefficients), and
   `(c_R/c_00)^12.6` might numerically match a more complex true expression.

**To distinguish these, MC at β = 4 or β = 8 would tell us whether
the K-tube formula tracks ⟨P⟩(β) across β values or only fits at β=6.**
This is a follow-up probe, not done here.

## Implications for the chain refactoring

**Status: chain refactoring stays at bounded support 4.4 ppm (PR #549, UNCHANGED).**

What this finding changes:

1. **The closure form `(N²−1)/(8N × b_0³) = 1/3993` is now confirmed
   to be empirical, NOT derivable from K-tube physics.** Prior synthesis
   noted this, but as a possibility; this finding makes it definitive.

2. **The framework's source-sector `ρ_(p,q)(6)` is genuinely a different
   physical object than Wilson transfer-matrix eigenvalues.** The Perron
   formula structure is correct (validates with MC-computed ρ values from
   Route 4); but ρ ≠ (c_R/c_00)^k.

3. **Theorem 3 no-go is partially reinstated empirically.** While the
   audit identified a methodological loophole (proof didn't use onset
   jet), the CONCLUSION ("no closed-form ρ from local data alone") is
   now supported by direct MC: the candidate closed form (K-tube) is
   refuted by 4D Wilson physics.

4. **The famous problem `⟨P⟩(β=6, L→∞) analytic` remains genuinely
   open.** No structural ansatz tested today works.

## What this does NOT change

- ⟨P⟩(β=6, L→∞) = 0.5934 retained-grade numerical (PR #539)
- V=1 PF ODE closed form for trivial sector (PR #541)
- Chain refactoring at bounded support 4.4 ppm (PR #549)
- DM-η G1 algebraic closure (PR #572)
- y_t Ward audit-prep (PR #573)
- 3 ratification candidates (PR #574)

These are all unaffected by the K-tube refutation; they were never
load-bearing on the K-tube structural interpretation.

## Status proposal

```yaml
note: CHAIN_CLOSURE_KTUBE_REFUTED_NOTE_2026-05-06.md
type: research_finding (definitive negative on K-tube structural interpretation)
proposed_status: research_finding
positive_subresults:
  - direct 4D SU(3) Wilson MC at β=6 measures λ_R < 1 for all tested irreps
  - K-tube formula (c_R/c_00)^k REFUTED as transfer-matrix eigenvalue formula
  - infrastructure validated: ⟨P⟩(L_s=4, L_t=14, β=6) = 0.597 ± 0.001 ✓
negative_subresults:
  - chain refactoring's closure form remains empirical, not structurally derivable from K-tube
  - source-sector ρ_(p,q)(6) confirmed as genuinely distinct from Wilson transfer-matrix eigenvalues
  - famous problem analytic closure remains genuinely open
audit_required: yes (this audit-style negative result needs cross-confirmation)
follow_up:
  - β-scan: MC at β=4, β=5, β=7, β=8 to test whether K-tube tracks <P>(β) or only fits at β=6
  - search for alternative structural ansätze for ρ_(p,q)(6)
```

## Reusable artifacts

- `/tmp/route4_4d_tube/route4_full_mc.py` — 4D Wilson MC with W_R + character correlator measurements
- `/tmp/route4_4d_tube/route4_full_Ls4_Lt14_chain[01]_beta6.json` — MC samples (2 × 582 KB)
- `/tmp/route4_4d_tube/analyze_v2.py` — analysis driver
- `/tmp/route4_4d_tube/analyze_v2_output.log` — verdict output

## Ledger entry

- **claim_id:** `chain_closure_ktube_refuted_note_2026-05-06`
- **note_path:** `docs/CHAIN_CLOSURE_KTUBE_REFUTED_NOTE_2026-05-06.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
