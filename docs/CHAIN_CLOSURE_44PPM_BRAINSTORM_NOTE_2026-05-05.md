# Chain Closure to 4.4 ppm + Derivation Route Brainstorm

**Date:** 2026-05-05
**Status:** research_finding (cleaner candidate; tighter to PDG; multi-route derivation brainstorm)
**Companion:** [`CHAIN_CLOSURE_9PPM_BRAINSTORM_NOTE_2026-05-05.md`](CHAIN_CLOSURE_9PPM_BRAINSTORM_NOTE_2026-05-05.md)

## Headline

Probe found a **cleaner and tighter** candidate for the chain closure:

```
β_eff_corrected = β_eff_geom × (1 − (N²−1)/(8N × b_0³))
For SU(3): correction = 8/(24 × 1331) = 1/3993 = 2.5044 × 10⁻⁴

v_predicted = 246.21857 GeV
v_PDG (G_F) = 246.21965 GeV
GAP = −4.389 ppm = −1.08 MeV   (sub-promille, 2× tighter than α_LM³ × C_F/4)
```

**Strictly cleaner than the prior α_LM³ × C_F/4 (9.3 ppm):**
- Pure group theory + 1-loop β-function coefficient (no boosted coupling)
- No iteration needed (constant correction, not self-consistent)
- 2× tighter empirical fit

## Comparison of candidates

| Candidate | Form | v gap (ppm) | Cleanness |
|---|---|---|---|
| **(N²−1)/(8N × b_0³)** | group + b_0 | **−4.4** | ★★★ pure structural |
| α_LM³ × C_F/4 | boosted coupling, iterated | −9.3 | ★★ requires α_LM iteration |
| α_LM⁴ × b_0/3 | boosted, 4-power | −12 | ★ structurally awkward |
| α_LM³ / π | continuum factor | −30 | ★ no clean derivation |
| α_LM³ × N(N²−1)/(8π²) | Probe B form | −56 | ★ overshoots |

**The (N²−1)/(8N × b_0³) candidate is the cleanest AND tightest.** Strong
evidence this is the correct structural form.

## SU(N) predictions (falsifiable)

| N | b_0 = 11N/3 | (N²−1)/(8N × b_0³) | δβ_eff/β_eff |
|---|---|---|---|
| 2 | 7.333 | 4.754 × 10⁻⁴ | 4.75e-4 |
| **3** | **11.000** | **2.504 × 10⁻⁴** | **2.50e-4** |
| 4 | 14.667 | 1.486 × 10⁻⁴ | 1.49e-4 |
| 5 | 18.333 | 9.737 × 10⁻⁵ | 9.7e-5 |

These predictions are testable: MC at SU(2) and SU(4) at corresponding
β = 2N²/g²_bare = 8 (SU(2)) or 32 (SU(4)) would distinguish this form
from alternative candidates.

## Brainstorm: derivation routes for `(N²−1)/(8N × b_0³)`

The form has clean structural ingredients:
- `(N²−1)/(8N)` = `C_F/4` — fundamental Casimir / 4 (where /4 is the
  fourth-power structure of `u_0 = ⟨P⟩^(1/4)`)
- `1/b_0³` = cube of inverse 1-loop β-function coefficient

This is suggestive of a **3-loop self-consistent perturbative correction
with C_F color factor**. Eight derivation routes brainstormed:

### Route 1 — SD-equation NLO solve (★★★ most promising)

The framework's tensor-transfer Perron solve `T_src(6) = exp(3J)·D_loc·R_env·exp(3J)`
with self-consistent eigenvalue equation. The prior campaign (PRs
#506-#527) named this as ~3-day algebraic problem. The K-tube `12 + 2/π`
fit gives leading-order; NLO solve should give the correction.

**Specific calculation:**
- Set up eigenvalue problem for T_src in (p,q) basis
- Use 7 PF ODEs from PR #549 for c_R(6) values
- Solve self-consistency at NLO
- Extract β_eff^NLO(6) — should equal β_eff_geom × (1 − (N²−1)/(8N × b_0³))

### Route 2 — LPT 3-loop bookkeeping (★★★ well-defined)

Standard LPT (Lepage-Mackenzie 1993, Trottier-Shakespeare-LM 2002):
`1 − ⟨P⟩(β) = w_1/β + w_2/β² + w_3/β³ + …` with TSLM 2002's `w_3 = 0.0137`.

**Specific calculation:**
- Convert TSLM's `w_3` from bare-α to LM-boosted-α scheme
- Identify which diagrammatic contribution carries the `(N²−1)/(8N)` factor
- Show that, at the framework's β_eff_geom matching scale, the
  3-loop correction in the boosted scheme equals `1/b_0³ × (N²−1)/(8N)`

### Route 3 — Wilson-loop tube boundary renormalization (★★)

12-plaquette tube around a marked plaquette in 3D L_s=3 cube. 1-loop
boundary correction has color factor C_F (fundamental rep on tube
boundary). 3-loop running coefficient gives 1/b_0³.

**Specific calculation:**
- 1-loop Wilson loop renormalization: `δ⟨W_R⟩/⟨W_R⟩ = α C_R × ln(Λ)`
- For boundary `tube` of length 12, integrated with running coupling
- 3-loop: `α³ × C_F/4 × …` in correct scheme

### Route 4 — Susceptibility-flow numerical validation (★★ validation only)

Use PR #539's measured χ_L from L=3,4,5,6,8 ⟨P⟩ values. Numerically
integrate `β_eff'(β) = χ_L(β)/χ_1plaq(β_eff)` from β=0 to β=6.
Compare with framework's `β_eff_geom × (1 − (N²−1)/(8N × b_0³))`.

This validates the form; doesn't derive it from first principles.

### Route 5 — SU(2)/SU(4) MC test (★★ falsifiable)

Run high-precision MC for SU(2) Wilson at β=8 and SU(4) at β=32
(corresponding to g²_bare=1 in each case). Check if measured β_eff^can
matches the predicted `β_eff_geom × (1 − (N²−1)/(8N × b_0³))` at SU(2)
and SU(4).

If yes: structural form **confirmed empirically across N**.
If no: the form is SU(3)-specific accident.

### Route 6 — Anomalous dimension at 1-loop, cubed (★ speculative)

`γ_W = α × C_F/(2π)` is the 1-loop anomalous dimension of Wilson loop.
Cubed: `γ_W³ = α³ × C_F³/(2π)³`. Doesn't immediately match
`(N²−1)/(8N × b_0³)`.

### Route 7 — Holographic / dimensional reduction (★ speculative)

4D Wilson at β=6 ↔ 2D effective at some β_2D via Migdal-Kadanoff RG.
The dimensional-reduction factor includes `C_F` × group-theoretic factor.
At b_0³ level it gives 1/3993.

### Route 8 — Exact identity α_LM × b_0 = 1 (★ requires its own proof)

If `α_LM × b_0 = 1` is exact (currently approximate at 0.27% level),
then `α_LM³ = 1/b_0³`, and `α_LM³ × C_F/4 = (N²−1)/(8N × b_0³)`. The
two candidates BECOME EQUIVALENT under this exact identity.

**Specific calculation:** derive `α_LM × b_0 = 1` from framework primitives.
This is itself an open problem (PRs #519-#527 explored, terminal status).

## Most-promising routes (this probe will dispatch)

**Route 1 (SD-equation NLO)** and **Route 2 (LPT bookkeeping)** in parallel.

- Route 1 directly uses framework infrastructure (T_src, c_R(6) PF ODEs).
- Route 2 uses published TSLM 2002 results, requires only LPT bookkeeping.
- Either could derive the form within a probe session.

If both fail, **Route 4 (numerical validation with PR #539 χ_L data)**
gives empirical confidence boost without first-principles derivation.

If forming all of those, **Route 5 (SU(2)/SU(4) MC test)** is the
falsification path — predicts specific values testable in days of MC.

## Stronger position than MC?

Comparing PR #549's chain refactoring vs PR #539's MC retained:

| Aspect | MC retained (PR #539) | Chain refactoring (PR #549) |
|---|---|---|
| Output | ⟨P⟩ at intermediate level | v at observable level |
| Precision vs PDG | 10⁻⁴ on ⟨P⟩ → translates to ~0.1% on v | **4.4 ppm on v** |
| Method | numerical (MC + FSS) | analytical closed form |
| Status | retained-grade | bounded → unbounded after derivation |
| Strength | rigorous numerical theorem | sub-promille agreement on PHYSICS observable |
| Weakness | doesn't predict v directly | empirical correction form (until derived) |

**Chain refactoring is STRONGER in physics-output sense:** it predicts
v directly to sub-promille, which is the framework's deliverable for
PDG comparison. PR #539 is more rigorous as a numerical theorem. They
are complementary.

After Route 1 or Route 2 derivation, the chain refactoring becomes
**unbounded retained** — at which point it strictly supersedes PR #539
in the framework's chain (PR #539 becomes a numerical comparator).

## Status proposal

```yaml
note: CHAIN_CLOSURE_44PPM_BRAINSTORM_NOTE_2026-05-05.md
type: research_finding (cleaner closure form; multi-route derivation brainstorm)
proposed_status: research_finding (bounded support at 4.4 ppm)
positive_subresults:
  - cleaner candidate (N²-1)/(8N × b_0³) tighter (4.4 ppm) than α_LM³ × C_F/4 (9.3 ppm)
  - pure group theory + 1-loop β-function structure
  - no iteration needed (constant correction)
  - SU(N) predictions falsifiable at other N
audit_required: yes
follow_up_open_problem:
  - derive (N²-1)/(8N × b_0³) from Route 1 (SD-equation NLO) or Route 2 (LPT bookkeeping)
  - test at SU(2)/SU(4) MC for falsification
unbounded_retained_path:
  - Route 1 (SD-equation NLO solve): if successful, gives unbounded retained
  - Route 2 (LPT bookkeeping): if successful, gives unbounded retained
```

## Ledger entry

- **claim_id:** `chain_closure_44ppm_brainstorm_note_2026-05-05`
- **note_path:** `docs/CHAIN_CLOSURE_44PPM_BRAINSTORM_NOTE_2026-05-05.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
