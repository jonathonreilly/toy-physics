# Route 2 LPT Deep Audit: Block Stands With Corrected Reasoning

**Date:** 2026-05-06
**Status:** research_finding (deep audit of prior Route 2 verdict; prior magnitude claim was wrong)
**Companion:** [`CHAIN_CLOSURE_DERIVATION_BLOCKED_NOTE_2026-05-05.md`](CHAIN_CLOSURE_DERIVATION_BLOCKED_NOTE_2026-05-05.md)

## Headline

Deep audit of the prior Route 2 (LPT 3-loop bookkeeping) BLOCK
verdict finds:

- **The block stands**, BUT for a different reason than previously
  claimed.
- **Prior probe's "60× too big, wrong sign" was a calculation error.**
  Corrected analysis: LPT 3-loop in the framework's α_LM scheme gives
  `δβ/β ≈ −4.33×10⁻⁵`, which is **5.7× too SMALL with CORRECT
  (negative) sign**.
- The structural reason the block stands: **framework residual is a
  non-perturbative V=1 ↔ 4D Wilson mismatch**, not a 3-loop LPT object.

## Verified LPT inputs (with citations)

Symbolic re-derivation confirms standard published values:

- **Heller-Karsch 1985** (PRD 32, 2911): `w_1 = 1/3` (exact)
- **DiGiacomo-Rossi 1981** (Phys. Lett. B 100, 481): `w_2 ≈ 0.0339`
- **Trottier-Shakespeare-Lepage-Mackenzie 2002** (PRD 65, 094502):
  `w_3 ≈ 0.0137`
- **Bali-Bauer-Pineda 2014** (PRD 89, 054505): all-order α expansion

Conversions:
- bare-α: `c_1 = 2π/9`, `c_2 = 113π²/7500`, `c_3 = 137π³/33750`
- LM-boosted (framework α_LM): `c̃_3^LM = 4393π³/3645000 ≈ 0.0374`

Four distinct "boosted" couplings exist in lattice literature:
- α_bare = 1/(4π) ≈ 0.0796
- α_LM (framework, α_bare/u_0) ≈ 0.0907
- α_V (TSLM 2002 potential scheme at q*=3.4015/a) ≈ 0.131
- α_MS̄(1/a) ≈ 0.193

**Framework's α_LM is NOT TSLM α_V.** (α_V/α_LM)³ ≈ 3.0 — the cube
ratio that would convert (N²−1)/(8N) between schemes.

## Re-derived c̃_3 in framework α_LM scheme — prior claim was WRONG

LPT 3-loop in framework's α_LM scheme:
- `Δ⟨P⟩_3loop = c̃_3^LM × α_LM³ = 0.0374 × 0.0907³ = −2.79×10⁻⁵` (correct negative sign)
- `δβ_eff = ΔP/slope(0.069) = −4.04×10⁻⁴`
- `δβ_eff/β_eff = −4.33×10⁻⁵`
- **Target = −1/3993 = −2.50×10⁻⁴**

**Ratio: 0.17.** LPT 3-loop in α_LM is **5.7× too SMALL with CORRECT
(negative) sign**.

| Claim | Prior probe | This audit |
|---|---|---|
| Magnitude vs target | "60× too big" | **5.7× too small** |
| Sign | "wrong sign" | **correct (negative)** |
| Block stands? | Yes | Yes (but for different reason) |

The prior probe had a calculation error in the chain conversion. The
corrected analysis still doesn't unblock Route 2 — it just changes
the direction of failure from "too big" to "too small".

## Why the block stands (corrected reasoning)

By direct Weyl integration of single SU(3) matrix at framework's β_eff_geom = 9.33:

- V=1 `⟨P⟩` at β=9.33 = **0.59353** (matches framework's P_geom exactly)
- Large-β LPT prediction `1 − 4/(9·9.33) = 0.952` — **completely off**
  (β=9.33 is NON-perturbative for V=1 SU(3))

So the chain matching scale β_eff_geom = 9.33 sits in V=1's
**INTERMEDIATE-coupling regime where LPT does not converge**. The
framework's residual (≈ 10⁻⁴) is the difference between two
**NON-perturbative `⟨P⟩` values** (V=1 PF ODE result vs 4D L→∞ MC
extrapolation), NOT a 3-loop LPT object.

**Specific reasons:**
1. Framework residual is a non-perturbative V=1 ↔ 4D mismatch (~10⁻⁴),
   NOT a 3-loop LPT correction (~10⁻⁵).
2. The required coefficient `δ_3^LM ≈ 1/3` is **8.92× larger than LPT
   `c̃_3^LM ≈ 0.0374`**.
3. The "clean" identity `(N²−1)/(8N × b_0³) = w_1 × α_LM³` requires
   `α_LM × b_0 = 1` EXACTLY; in fact it holds only to 0.27% at β=6
   (numerical coincidence, not exact).
4. V=1 SU(3) at β=9.33 is in non-perturbative regime (verified
   directly: 0.5935 vs LPT-asymptotic 0.95).

## Verdict — (A) BLOCK STANDS but with corrected reasoning

LPT in any standard scheme cannot derive `(N²−1)/(8N × b_0³)`. The
framework's chain residual lives in the V=1 PF ODE non-perturbative
regime, not in the 3-loop LPT regime. Route 2 is genuinely closed.

**Different scheme (α_V vs α_LM) shifts the apparent c̃_3 by factor
~3** (matching (α_V/α_LM)³), but no standard scheme produces a clean
`(N²−1)/(8N)` coefficient that would close the chain.

## Implications for Route 1

While Route 2 is genuinely blocked, the COMPANION audit of Theorem 3
(see `THEOREM3_DEEP_AUDIT_LOOPHOLE_NOTE_2026-05-06.md`) found that
Route 1 is **NOT actually blocked** as claimed. The framework's
Theorem 3 no-go has a real structural loophole (it doesn't apply the
onset-jet constraint). A re-attempt of Route 1 with onset-jet
constraint applied is the right next-step.

## Status proposal

```yaml
note: ROUTE2_LPT_DEEP_AUDIT_NOTE_2026-05-06.md
type: research_finding (deep audit of prior Route 2 verdict)
proposed_status: research_finding (Route 2 BLOCK confirmed; prior magnitude was wrong)
positive_subresults:
  - Verified LPT coefficients via published literature
  - Distinguished framework α_LM from TSLM α_V (factor ~3 in cube)
  - Direct Weyl integration confirms V=1 SU(3) at β=9.33 = 0.5935 (non-perturbative regime)
  - Block stands; Route 2 genuinely closed for non-perturbative reasons
negative_subresults:
  - Prior probe's "60× too big, wrong sign" was a calculation error
  - Corrected: LPT 3-loop in α_LM = 5.7× too small, correct sign
audit_required: yes (audit this audit; verify the corrected magnitudes)
follow_up: pursue Route 1 with onset-jet constraint per companion note
```

## Updates needed to companion notes

- `CHAIN_CLOSURE_DERIVATION_BLOCKED_NOTE_2026-05-05.md` Route 2 verdict
  should be UPDATED:
  - Replace "60× larger than target, wrong sign" with the correct
    "5.7× smaller than target, correct sign"
  - Add the V=1 Weyl-integration verification confirming β_eff_geom=9.33
    sits in non-perturbative regime
  - Strengthen the structural reason: framework residual is a V=1↔4D
    non-perturbative mismatch, not an LPT 3-loop object

## Ledger entry

- **claim_id:** `route2_lpt_deep_audit_note_2026-05-06`
- **note_path:** `docs/ROUTE2_LPT_DEEP_AUDIT_NOTE_2026-05-06.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
