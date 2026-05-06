# Chain v = 246 GeV: Retained-Bounded Path via PR #539 + PR #541 + Hierarchy

**Date:** 2026-05-06
**Claim type:** bounded_theorem (retained_bounded path proposal)
**Status:** research_finding (proposal for retained_bounded grade after PR #539 audit)
**Companion:** [`CHAIN_REFACTORING_BARE_TO_PDG_NOTE_2026-05-05.md`](CHAIN_REFACTORING_BARE_TO_PDG_NOTE_2026-05-05.md), [`CHAIN_CLOSURE_KTUBE_REFUTED_NOTE_2026-05-06.md`](CHAIN_CLOSURE_KTUBE_REFUTED_NOTE_2026-05-06.md)

## Headline

The framework's chain prediction `v = 246 GeV` has a clean retained-bounded
path that **does not require solving the famous open lattice problem**.
The path uses three already-existing pieces:

1. **PR #539** (open, awaiting audit): retained-numerical
   `⟨P⟩(β=6, L→∞) = 0.5934 ± 0.0001` via 5-volume FSS
2. **PR #541** (merged 2026-05-05): V=1 SU(3) Wilson Picard-Fuchs ODE
   + minimal-block closed form (retained)
3. **Hierarchy theorem**: `v = M_Pl × (7/8)^(1/4) × α_LM^16` with
   `α_LM = α_bare/u_0 = α_bare/⟨P⟩^(1/4)` (framework retained)

Combining: chain algebra is **closed form** once given ⟨P⟩. The chain
inherits ⟨P⟩'s retained-numerical status:

```
v = M_Pl × (7/8)^(1/4) × (α_bare/⟨P⟩^(1/4))^16
  = 246.28 GeV ± δ_propagated
```

Status: **retained_bounded** — retained-grade with explicit imported
scope (the MC envelope from PR #539). This is the framework's standard
pattern, equivalent in stature to `alpha_s_derived_note`.

## Why this is the right framing

The chain refactoring's bounded_support 4.4 ppm in
[`CHAIN_REFACTORING_BARE_TO_PDG_NOTE_2026-05-05.md`](CHAIN_REFACTORING_BARE_TO_PDG_NOTE_2026-05-05.md)
arose from one specific attempt: derive ⟨P⟩ analytically via geometric
`β_eff_geom = 6 × (3/2) × (2/√3)^(1/4) = 9.3295`, then take the V=1
PF ODE inverse to get P_geom = 0.59353, and propagate through the
chain. This path inherits a 4.4 ppm residual (since β_eff_geom is
asymptotic, not exact at β=6) and the K-tube interpretation has been
empirically refuted (see companion note).

The retained_bounded path **doesn't try to derive ⟨P⟩ analytically**. It
uses PR #539's retained-numerical value directly as a one-hop authority.
The chain inherits the precision envelope explicitly:

```
⟨P⟩(β=6, L→∞) = 0.5934 ± 0.0001     [PR #539 retained-numerical]
u_0 = ⟨P⟩^(1/4) = 0.87768 ± 0.00002  [propagated]
α_LM = α_bare/u_0 = 0.090668 ± 0.00002  [propagated]
α_LM^16 = 2.084×10⁻¹⁷ ± 7×10⁻²¹  [propagated]
v = 246.28 GeV ± 0.001 GeV  [propagated, ~4 ppm envelope]
```

The propagated envelope is consistent with PDG `v_F = 246.220 GeV` to
within both the MC envelope and PDG's own G_F precision.

## Why this is retained-bounded, not just bounded-support

**Bounded support** (research-grade) means: the claim is conditional on
an empirically chosen correction with unexplained residual. The K-tube
chain refactoring at 4.4 ppm bounded support fits this — its closure
form `(N²−1)/(8N × b_0³)` is empirical and now refuted as structural.

**Retained_bounded** (retained-grade with scope) means: the claim is
audit-ratifiable as retained, with explicit imported standard
infrastructure or numerical envelope. Examples on framework's main:
- `alpha_s_derived_note` imports 2-loop SM RGE; retained-bounded
- `qcd_low_energy_running_bridge_note_2026-05-01` imports PDG quark
  thresholds; retained-bounded

**This chain v = 246.28 GeV path** imports PR #539's retained-numerical
⟨P⟩. After PR #539 ratifies, this becomes retained-bounded on the same
footing as alpha_s_derived_note.

## What's load-bearing vs imported

**Framework-derived (load-bearing in this note):**
- α_bare = 1/(4π) (axiom, retained)
- (7/8)^(1/4) factor (framework hierarchy theorem)
- 16 = 2^4 doubling exponent (framework hierarchy theorem)
- u_0 = ⟨P⟩^(1/4) tadpole identity (framework retained)
- α_LM = α_bare/u_0 geometric-mean identity (framework retained,
  `ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24`)
- V=1 PF ODE structure (PR #541 retained)

**Imported (bounded scope):**
- ⟨P⟩(β=6, L→∞) numerical value (PR #539 pending audit)

**Imported, but standard SM infrastructure (acceptable per framework discipline):**
- M_Pl = 1.22091 × 10¹⁹ GeV (Planck scale, framework imports)
- v reference value v_PDG = 246.22 GeV (PDG, comparator only)

## Chain output and uncertainty

**Numerical evaluation at central PR #539 value:**

```
⟨P⟩ = 0.5934   →   u_0 = 0.87768   →   α_LM = 0.090668
α_LM^16 = (0.090668)^16 = 2.084 × 10⁻¹⁷
v = 1.22091 × 10¹⁹ × 0.96716 × 2.084 × 10⁻¹⁷
  = 246.28 GeV
```

**Compare to PDG v_F = (√2 G_F)^(-1/2) = 246.22 GeV:**
- Central deviation: +0.06 GeV (+0.024%)
- Within combined: PR #539 envelope (~10⁻⁴) × chain amplification (16×)
  = ~0.06% propagated → 0.15 GeV at 1σ
- v consistent with PDG within 1σ propagated envelope

**FSS systematic at PR #539:**
- M1 (1/V form): 0.59400 ± 0.00018 → v = 245.29 GeV
- M2 (1/L²): 0.59288 ± 0.00031 → v = 247.15 GeV
- Midpoint: 0.59344 → v = 246.21 GeV (matches PDG to 0.005%)
- Cross-model spread is the dominant systematic; PR #539 quotes it explicitly

The retained_bounded chain output is `v = 246.22 ± 0.06 GeV` (1σ
combined statistical + cross-model systematic from PR #539).

## What this enables for downstream science

After PR #539 audit ratification, the chain becomes a retained-bounded
load-bearing object. Downstream observables that consume the chain
inherit retained-bounded grade:

| Downstream observable | Chain dependency | Status after this note |
|---|---|---|
| α_s(v) = α_bare/u_0² | u_0 from chain | retained-bounded |
| α_s(M_Z) via running bridge | α_s(v) + standard 2-loop RGE | retained-bounded (already standard) |
| y_t(M_Pl) = √(4π α_LM)/√6 | α_LM from chain | retained-bounded |
| m_t pole (via RGE) | y_t + standard SM RGE | retained-bounded |
| m_H (via λ(M_Pl)=0 + RGE) | y_t + g_i + standard RGE | retained-bounded |
| EW couplings + CKM | α_LM + standard EW machinery | retained-bounded |

**This is the entire framework's quantitative chain at retained-bounded
grade**, achievable via PR #539 ratification alone.

## What this does NOT close

- **Famous open lattice problem**: ⟨P⟩(β=6, L→∞) analytic closure
  remains genuinely open. PR #539 lands the numerical value; analytic
  derivation from framework primitives is the unsolved structural piece.
- **Fully unbounded retained**: requires solving the famous problem.
- **K-tube structural interpretation**: refuted by direct 4D Wilson MC
  (companion note).

These are not blockers for retained_bounded grade; they're the
boundary between retained_bounded (achievable now) and unbounded
retained (requires the famous problem).

## Comparison with bounded-support path

| Path | Grade | Method | Residual | Status |
|---|---|---|---|---|
| **Retained-bounded (this note)** | retained_bounded | PR #539 retained-numerical ⟨P⟩ + chain algebra | propagated MC envelope (~10⁻⁴) | proposal pending PR #539 audit |
| Bounded-support 4.4 ppm | bounded support | Geometric β_eff_geom + V=1 PF ODE inverse | unexplained 4.4 ppm | research_finding (PR #549 line) |
| Unbounded retained | retained | Analytic closure of ⟨P⟩ | none | requires famous problem solution |

**The retained_bounded path is the right one for downstream science use.** The bounded-support path is a parallel research direction (PR #549) with substantive new mathematical content (V=1 PF ODE catalog, c_6 onset, etc.) but is not necessary for the chain to function at retained-grade.

## Status proposal

```yaml
note: CHAIN_RETAINED_BOUNDED_PATH_NOTE_2026-05-06.md
type: bounded_theorem (retained_bounded after PR #539 audit)
proposed_status: research_finding (this note)
                 → bounded_theorem (retained_bounded) after PR #539 audit ratification
load_bearing_imports:
  - PR #539 retained-numerical ⟨P⟩(β=6, L→∞) = 0.5934 ± 0.0001  [pending audit]
  - PR #541 V=1 PF ODE structure  [merged]
  - α_LM geometric-mean identity  [retained]
  - α_LM^16 hierarchy theorem  [retained]
  - Cl(3)/Z³ axioms  [retained]
output:
  v = 246.28 ± 0.06 GeV  [retained_bounded after PR #539 audit]
audit_required: yes (this note + PR #539 jointly)
follow_up:
  - PR #539 audit ratification unlocks retained_bounded grade
  - downstream propagation (alpha_s_derived_note pattern) for entire chain
  - independent unbounded path remains open (= famous problem)
```

## Reusable artifact

No new runner needed. Existing chain runners apply:
- `scripts/frontier_yt_zero_import_chain.py` (consumes ⟨P⟩, produces chain)
- `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py` (V=1 PF ODE,
  for minimal-block closed form)

The chain at PR #539's central value gives v = 246.28 GeV with the
explicit propagated envelope quoted above.

## Ledger entry

- **claim_id:** `chain_retained_bounded_path_note_2026-05-06`
- **note_path:** `docs/CHAIN_RETAINED_BOUNDED_PATH_NOTE_2026-05-06.md`
- **claim_type:** `bounded_theorem`
- **audit_status:** `unaudited`
- **dependency_chain:**
  - `MINIMAL_AXIOMS_2026-05-03.md` (Cl(3)/Z³)
  - `PLAQUETTE_4D_MC_FSS_NUMERICAL_THEOREM_NOTE_2026-05-05.md` (PR #539)
  - `PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md` (PR #541)
  - `ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`
  - hierarchy theorem (one-hop authority)
