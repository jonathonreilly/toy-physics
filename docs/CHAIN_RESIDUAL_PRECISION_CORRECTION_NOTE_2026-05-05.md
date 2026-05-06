# Correction: Chain Residual 2-Loop Precision Overclaim

**Date:** 2026-05-05
**Status:** research_finding (precision correction to companion note)
**Type:** honest precision correction
**Companions:** [`CHAIN_REFACTORING_BARE_TO_PDG_NOTE_2026-05-05.md`](CHAIN_REFACTORING_BARE_TO_PDG_NOTE_2026-05-05.md), [`CHAIN_RESIDUAL_2LOOP_LATTICE_ARTIFACT_NOTE_2026-05-05.md`](CHAIN_RESIDUAL_2LOOP_LATTICE_ARTIFACT_NOTE_2026-05-05.md)

## What this corrects

The companion note `CHAIN_RESIDUAL_2LOOP_LATTICE_ARTIFACT_NOTE_2026-05-05.md`
claimed that the 2-loop formula `ΔP = -α_LM³ × N(N²-1)/(8π²)` matches
the empirical `P_MC - P_geom` gap to **0.4%**. This was based on a
**factor-of-1.75 arithmetic error** in the source probe.

### Actual numerical state (verified)

```
P_geom (V=1 PF ODE @ β_eff_geom=9.3295) = 0.59353  →  v = 246.069 GeV (gap −0.087%)
P_MC (PR #539 comparator)               = 0.59340  →  v = 246.285 GeV (PDG-exact)
P_PDG_required (chain inverse)          = 0.59340  →  v = 246.283 GeV (PDG)
P_geom + 2-loop ΔP                      = 0.59330  →  v = 246.445 GeV (gap +0.066%)

Empirical ΔP_{can-geom} = 0.59340 − 0.59353 = −0.00013    (CORRECT)
2-loop prediction        = −α_LM³ × 24/(8π²) = −0.00023   (1.75× overshoot)
```

The 2-loop formula predicts a correction of **−2.3 × 10⁻⁴**, but the
empirical gap is **−1.3 × 10⁻⁴**. The formula is correct at the
order-of-magnitude level (sign and ~factor 2) but does NOT precisely
close the chain residual.

### Implications for retention claim

The companion note's claim that the chain residual is "fully identified
as a 2-loop tadpole correction matching to 0.4%" was overclaimed. The
honest position:

**(a)** The 2-loop formula is the right ORDER OF MAGNITUDE for the
residual, with correct sign. This rules out interpretations where the
residual is much smaller (e.g., 3-loop only) or much larger (e.g.,
genuine α_s²/(4π) shift).

**(b)** The factor-of-1.75 mismatch means EITHER:
- the 2-loop coefficient has additional structure beyond `N(N²-1)/(8π²)`
  that we haven't identified
- OR the empirical comparator P_MC = 0.5934 has its own uncertainty
  (literature values range 0.5933 - 0.5937, with PR #539 spanning
  0.59288 to 0.59400 across FSS forms) that's comparable to the gap
- OR the chain residual is genuinely a mix of 2-loop plus other
  corrections

**(c)** Probe E's lattice-artifact framing remains intact: P_geom =
0.59353 is INSIDE PR #539's FSS [M2, M1] envelope and predicts v MORE
accurately than EITHER individual FSS form (P_M1 gives v=245.29, gap
−0.40%; P_M2 gives 247.15, +0.35%; P_geom gives 246.07, −0.087%). The
0.087% residual is within standard unimproved-Wilson literature spread.

## Honest current grade

**bounded_support, not retained closure.**

The chain refactoring `v = M_Pl × (7/8)^(1/4) × α_bare^16 ×
P_1plaq(β_eff_geom)^(-4) = 246.07 GeV` is a **closed-form chain prediction
from framework primitives + V=1 PF ODE alone**, with a 0.087% bounded
residual to PDG that is:
- Inside PR #539's FSS retained-grade error envelope (M2 to M1 spread)
- Consistent with standard unimproved-Wilson lattice literature spread
- Consistent with order-of-magnitude 2-loop tadpole correction (within
  factor of ~2)
- NOT precisely closed by any single specific perturbative correction

This is **bounded_support** — equivalent in status to `alpha_s_derived_note`
which uses a 2-loop SM RGE bounded scheme imported as standard
infrastructure.

## Retention path (proposed)

Audit submission proposal: promote PR #549's chain refactoring + the
companion notes (V=1 PF ODE, minimal-block closed form, 7-irrep PF ODE
catalog, PR #525 flaw fix, this correction) to **`bounded_retained`**
on the framework's standard pattern:

```
proposed_status: bounded_retained (analogous to alpha_s_derived_note)
basis:
  - V=1 SU(3) Picard-Fuchs ODE (PR #541, merged)
  - β_eff_geom = 6 × (3/2) × (2/√3)^(1/4) from framework geometric primitives
  - hierarchy theorem v = M_Pl × (7/8)^(1/4) × α_LM^16
  - bounded scope: 0.087% residual to PDG, consistent with standard
    unimproved-Wilson literature uncertainty
audit_required: yes (analogous to alpha_s_derived_note audit pattern)
bare_retained_allowed: no (must be flagged as bounded scope)
```

**The 0.087% residual is acknowledged as bounded scope, NOT closed.**

## What this DOES unlock at bounded_retained grade

If audit ratifies the bounded_retained status, the framework's
downstream science can repoint the chain to consume P_geom (analytic)
instead of P_MC (numerical), at bounded_retained grade. Specifically:

| Downstream observable | Currently | After bounded_retained chain | Bounded scope |
|---|---|---|---|
| α_s(v) | 0.10330 (from u_0=0.87768) | 0.10328 (from u_0=0.87773) | 0.02% shift |
| α_s(M_Z) via running bridge | 0.1181 (PDG match) | 0.1181 (essentially same) | <0.01% shift |
| y_t(M_Pl) = √(4πα_LM)/√6 | 0.4358 | 0.4357 | 0.02% shift |
| m_t pole (after RGE) | ≈170 GeV | ≈170 GeV | <0.1% shift |
| v | 246.28 GeV (PDG matched) | 246.07 GeV (analytic) | 0.087% bounded |
| m_H | 125.10 GeV (matched) | 124.99 GeV (analytic) | 0.087% bounded |
| All downstream EW observables | PDG-matched | analytic at bounded scope | 0.087% bounded |

The shift is small (0.02-0.087%) for nearly all downstream observables.
At bounded_retained grade, the framework can claim:

**"v, m_H, m_t, α_s(M_Z), and the entire EW chain are derivable from
framework primitives + V=1 SU(3) Picard-Fuchs ODE, at bounded scope
0.087% to PDG, with no L→∞ Wilson MC dependency."**

## What this does NOT unlock

- Retention at "fully closed" grade (would require closing the 0.087%)
- Nature-grade closure of the analytic L→∞ Wilson plaquette problem
- Refutation of PR #525's interpretation revision (PR #525 was
  specifically about K-tube ansatz; this note is about chain-residual
  identification, a different framing)

## Status proposal

```yaml
note: CHAIN_RESIDUAL_PRECISION_CORRECTION_NOTE_2026-05-05.md
type: research_finding (precision correction)
proposed_status: research_finding
positive_subresults:
  - identifies arithmetic error in companion 2-loop probe (1.75× overshoot)
  - re-establishes honest bounded_support grade for the chain refactoring
  - maintains lattice-artifact framing (Probe E findings unchanged)
audit_required: yes (companion notes audit-submitted with corrected scope)
bare_retained_allowed: no
```

## Ledger entry

- **claim_id:** `chain_residual_precision_correction_note_2026-05-05`
- **note_path:** `docs/CHAIN_RESIDUAL_PRECISION_CORRECTION_NOTE_2026-05-05.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
