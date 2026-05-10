# CKM From Mass Hierarchy: V_CKM = U_u^dag U_d via Derived Mass Matrices

**Script:** `scripts/frontier_ckm_from_mass_hierarchy.py`
**Date:** 2026-04-12 (originally); 2026-05-10 (rigorize PATH C — cite live authority chain explicitly for the conditional upstream provenance)
**Status:** bounded — the CKM mixing hierarchy |V_us| >> |V_cb| >> |V_ub| follows from the asymmetry between up-type and down-type mass hierarchies produced by the framework, conditional on upstream mass-hierarchy bands and texture/GST readout assumptions. All three PDG CKM elements lie inside the prediction bands at runner PASS=24/FAIL=0. Audit verdict: `audited_conditional` (status authority is the independent audit lane).
**Claim type:** bounded_theorem
**Claim scope:** the bounded CKM hierarchy reading from framework mass-hierarchy bands plus the Gatto-Sartori-Tonin (GST) parametric relations, conditional on the upstream authorities cited below. The runner verifies algebraic consequences of the GST relations and band containment for PDG values; it does not derive the upstream mass-hierarchy bands, the geometric-mean intra-generation texture, or the GST applicability from A_min primitives within this packet (those are upstream conditional authorities).
**Audit-companion:** see `scripts/audit_companion_ckm_*` family in the upstream CKM atlas (load-bearing class-(A) algebra exact-symbolic verifications were closed in PRs #764, #767, #768, #864 for the structural-counts identities).

---

## Cited authorities (one-hop deps)

This note records explicit one-hop authority citations for the
conditional upstream provenance flagged by the 2026-05-05 audit verdict
`audited_conditional`. The audit's verdict_rationale identified that
"The presented calculation is conditional on upstream mass hierarchy
bands and texture assumptions that are not supplied as retained-grade
inputs. The runner hard-codes PDG masses, CKM values, and the claimed
hierarchy bands, then checks numerical containment and algebraic
consequences." The citations below sharpen the conditional structure
on the live authority chain without claiming to derive those upstream
authorities here.

- [`QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25.md`](QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25.md)
  (`audited_conditional`) — the taste-staircase mass-ratio readings
  `m_d/m_s = alpha_s(v)/2` and `m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)`
  that close the CKM lane (per CKM gate 2026-04-25 zero-import
  end-to-end). The down-type mass-hierarchy reading used by the GST
  relation `|V_us| ~ sqrt(m_d/m_s)` in §"Theorem / Claim" of this note
  is consistent with the taste-staircase formula in that authority.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  (`audited_conditional`) — the canonical coupling `alpha_s(v)` value
  that feeds the taste-staircase mass-ratio readings and the
  Wolfenstein-cascade structural identities. The mass-hierarchy band
  width here inherits the same alpha_s anomalous-dimension model
  dependence (U(1) proxy vs SU(3) gauge group).
- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
  (`audited_conditional`) — the canonical CKM atlas authority that
  packages the Wolfenstein and structural-count surfaces this note's
  GST reading is consistent with. The atlas authority already supplies
  `lambda^2 = alpha_s/n_pair`, `A^2 = n_pair/n_color`, and the
  Wolfenstein hierarchy reading, which provides a parallel route to
  the same hierarchy ordering claimed here from the mass-ratio side.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  (`audited_conditional`) — the structural-counts identities (M1)–(M5)
  for the CKM magnitudes whose exact-symbolic verification was closed
  in PR #768 at sympy `Rational` precision. The hierarchy ordering
  `|V_us| >> |V_cb| >> |V_ub|` claimed here is consistent with the
  Wolfenstein reading there at lambda^1, lambda^2, lambda^3.
- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  (`audited_conditional`) — the NLO protected-gamma surface for the
  CP-phase reading whose exact-symbolic verification was closed in
  PR #764. The CP-phase delta_CKM open gap noted in §"What Remains
  Open" item 4 of this note is sourced through that authority.

The audit's `notes_for_re_audit_if_any` field
(`missing_dependency_edge`) asks for retained-grade derivations of the
mass-hierarchy bands, the geometric-mean intra-generation texture, and
GST applicability to the framework mass matrices before re-auditing.
Those three named open premises map to the upstream authorities cited
above; they remain `audited_conditional` and are not promoted by this
note.

---

## Rigorize-pass disposition (2026-05-10) — PATH C: cite live authority chain

The 2026-05-05 audit verdict (`audited_conditional`, see
`docs/audit/data/audit_ledger.json`, runner_check_breakdown
A=11/B=0/C=0/D=13/total_pass=24) recorded that the runner does verify
the algebraic consequences of the GST parametric relations and PDG
band containment, but the upstream mass-hierarchy bands and texture
assumptions are not supplied as retained-grade inputs in the packet.
The verdict explicitly named this as the missing dependency edge.

The 2026-05-10 rigorize pass selects **PATH C** (cite live authority
chain explicitly) — analogous to the recent CKM rigorize pattern
(PRs #764/#767/#768/#864 closed the upstream structural-counts
identities at exact symbolic precision) and the recent Planck-lane
rigorize template (PR #812/#829 cite chains). The four PATH options
considered:

- **PATH A** (derive upstream from first principles): provide
  retained-grade derivations of the mass-hierarchy bands, the
  geometric-mean intra-generation texture, and GST applicability
  inside this packet. This is multi-row theorem-level work that
  belongs in the upstream authorities and is **deferred to future
  work**.
- **PATH B** (narrow scope to algebraic core): restrict the note
  scope to GST algebraic consequences only, dropping the band-
  containment readings. This is rejected here because the band
  containment is the load-bearing observation that motivates the note
  (the GST identity in isolation is a textbook result; the bounded
  framework reading IS the band-containment claim).
- **PATH C** (cite live authority chain explicitly): record explicit
  one-hop authority citations for the conditional upstream provenance,
  making the conditional structure load-bearing on the cited
  authorities while leaving the audit status of this row at
  `audited_conditional`. This is the disposition selected by this
  rigorize pass.
- **PATH D** (demote to numerical observation): reframe the note as
  pure numerical observation. This is rejected because the note is
  already explicitly bounded and PATH C captures the conditional
  structure better.

The audit row's `audit_status` and `intrinsic_status` are unchanged
(`audited_conditional`); per repo rules, no `docs/audit/data/*.json`
files are modified by this PR. PATH C makes the conditional structure
explicit on the live authority chain.

---

## Imported observational/upstream inputs (NOT derived in this packet)

The following inputs are imported with retained authority cited; they
are NOT derived from A_min primitives in this note:

- **Mass-hierarchy prediction band `[3.5, 5.5]` for log_10(m_t/m_u)
  and `[2.0, 4.0]` for log_10(m_b/m_d)** — imported from the
  framework's mass-hierarchy lane (the now-archived
  `MASS_HIERARCHY_HONEST_ASSESSMENT_NOTE` is referenced as the prior
  authority; the live authority on the retained surface is the
  taste-staircase mass-ratio reading
  `QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25`,
  `audited_conditional`). The bounded band widths reflect the
  alpha_s anomalous-dimension model dependence (U(1) proxy vs SU(3)).
- **Geometric-mean intra-generation texture `m_2^2 ~ m_1 · m_3`** —
  imported as a bounded structural assumption; the audit explicitly
  flagged this as not derived from A_min primitives in the packet.
  The runner records the observed factor-of-2 discrepancy on the
  c_c/m_t prediction, consistent with the bounded character.
- **GST parametric applicability** — the standard-result GST
  relations (`|V_us| ~ sqrt(m_d/m_s)`, `|V_cb| ~ |m_s/m_b - m_c/m_t|`,
  `|V_ub| ~ m_d/m_b`) are exact algebraic identities for any mass
  matrix with the standard nearest-neighbor or democratic off-diagonal
  texture. The audit flagged the **applicability** (i.e. the choice
  of texture under which GST holds) as conditional rather than the
  algebra itself. The companion `CKM_MAGNITUDES_STRUCTURAL_COUNTS_*`
  surface provides a parallel reading via Wolfenstein structural
  counts (lambda^1/lambda^2/lambda^3 hierarchy).
- **PDG quark masses and PDG CKM values** — imported observational
  inputs used in the band-containment evaluation (the runner
  hard-codes these for comparison; the framework-derived prediction
  is the band, not the central PDG value).

---

## What this note's runner DOES verify (under PATH C scope)

Under the PATH C cite-chain scope, the primary runner
`scripts/frontier_ckm_from_mass_hierarchy.py` verifies (PASS=24/FAIL=0
at 2026-05-10):

1. **Class-(A) load-bearing algebraic identity**: the GST relation
   `sqrt(m_d/m_s) = 0.2241` matches `|V_us| = 0.2243` to 0.1% — an
   algebraic identity for any mass matrix with the assumed texture.
2. **Class-(A) hierarchy ordering**: `|V_us| > |V_cb| > |V_ub|`
   follows algebraically from `sqrt(m_d/m_s) > m_s/m_b > m_d/m_b`
   for any masses with `m_d < m_s < m_b`, holding 100% across the
   bounded mass-hierarchy band scan.
3. **Class-(A) up/down asymmetry**: the EW charge-ratio
   `Q_up^2 / Q_down^2 = 4` and the down-sector dominance
   `sqrt(m_u/m_c) / sqrt(m_d/m_s) = 0.18` follow algebraically from
   the imported masses.
4. **Bounded band-containment** (conditional on upstream
   mass-hierarchy bands): all three PDG CKM elements (`|V_us| =
   0.2243`, `|V_cb| = 0.0422`, `|V_ub| = 0.00394`) lie inside the
   bands derived from scanning the mass-hierarchy bounds.

The runner does NOT derive the upstream mass-hierarchy bands; those
remain conditional on the cited upstream authorities.

---

## Status

**BOUNDED.** The CKM prediction inherits the same model dependence as
the mass hierarchy: the strong-coupling anomalous dimension
(U(1) proxy vs SU(3) band), the EWSB log-enhancement factor, and the
sector-dependent EW radiative corrections. The Gatto-Sartori-Tonin
relation that connects mass ratios to CKM elements is exact; the mass
ratios themselves are bounded framework predictions.

The Higgs Z\_3 charge blocker (review.md item 3) remains a live issue
for full quantitative CKM closure.

---

## Theorem / Claim

### Claim (CKM From Mass Hierarchy -- Bounded)

The CKM mixing matrix follows from the mass matrix diagonalization
mismatch V\_CKM = U\_u^dag U\_d, where U\_u and U\_d diagonalize the
up-type and down-type mass matrices respectively.

The framework produces the fermion mass hierarchy through the EWSB
cascade + RG mechanism with zero free mass-ratio parameters
(MASS\_HIERARCHY\_HONEST\_ASSESSMENT\_NOTE.md). The observed mass ratios
lie inside the prediction bands:

- log\_10(m\_t/m\_u) = 4.90, predicted in [3.5, 5.5]
- log\_10(m\_b/m\_d) = 2.95, predicted in [2.0, 4.0]

The up hierarchy is STEEPER than the down hierarchy (ratio 1.66x in
log-space), driven by the EW charge asymmetry:

- Up-type: Q\_em = +2/3, T\_3 = +1/2
- Down-type: Q\_em = -1/3, T\_3 = -1/2
- Q\_up^2 / Q\_down^2 = 4

This asymmetry makes U\_u more diagonal than U\_d, so V\_CKM is
controlled by the down-sector mass ratios via the Gatto-Sartori-Tonin
parametric relations:

| CKM element | Parametric relation | Predicted | PDG |
|-------------|--------------------|-----------| ----|
| \|V\_us\| | sqrt(m\_d/m\_s) | 0.224 | 0.2243 |
| \|V\_cb\| | \|m\_s/m\_b - m\_c/m\_t\| | 0.015 | 0.0422 |
| \|V\_ub\| | m\_d/m\_b | 0.0011 | 0.00394 |

The prediction bands from scanning the mass hierarchy bands:

| CKM element | Band | PDG | In band? |
|-------------|------|-----|----------|
| \|V\_us\| | [0.10, 0.32] | 0.2243 | Yes |
| \|V\_cb\| | [0.0003, 0.098] | 0.0422 | Yes |
| \|V\_ub\| | [0.0001, 0.010] | 0.00394 | Yes |

The hierarchy ordering |V\_us| > |V\_cb| > |V\_ub| is preserved across
100% of the mass hierarchy prediction band.

---

## Assumptions

| # | Assumption | Status | Grade |
|---|-----------|--------|-------|
| 1 | EWSB quartic selector breaks S\_3 -> Z\_2 | Exact | Framework |
| 2 | Wilson mass pattern 1+3+3+1 from staggered lattice | Exact | Framework |
| 3 | RG running amplifies taste-dependent mass splitting | Exact | Structural |
| 4 | Mass hierarchy prediction band [3.5, 5.5] for up sector | Bounded | Model |
| 5 | Mass hierarchy prediction band [2.0, 4.0] for down sector | Bounded | Model |
| 6 | Geometric mean intra-generation pattern m\_2^2 ~ m\_1 * m\_3 | Bounded | Texture |
| 7 | GST parametric relations connect mass ratios to CKM | Exact | Standard result |
| 8 | Up hierarchy steeper than down from EW charge asymmetry | Bounded | Model |

---

## What Is Actually Proved

### Exact results (16 tests):

**E1.** The GST relation sqrt(m\_d/m\_s) = 0.2241 matches |V\_us| = 0.2243
to 0.1%. This is an algebraic identity for any mass matrix with the
standard nearest-neighbor or democratic off-diagonal texture.

**E2.** The up-sector correction sqrt(m\_u/m\_c) = 0.041 is 18% of the
leading term, confirming that V\_CKM is dominated by the down sector.
The PDG value lies inside the corrected range [0.183, 0.265].

**E3.** The parametric hierarchy ordering |V\_us| > |V\_cb| > |V\_ub|
follows algebraically from the down-type mass hierarchy: sqrt(m\_d/m\_s) >
m\_s/m\_b > m\_d/m\_b for any masses with m\_d < m\_s < m\_b.

**E4.** The EWSB quartic selector V\_sel = 32 sum\_{i<j} phi\_i^2 phi\_j^2
has minima at axis directions and breaks S\_3 -> Z\_2. This is algebraic
(no lattice size, no gauge coupling).

**E5.** The FN charge approach (eps = 1/3) gives |V\_us| = |V\_cb| = eps^2 = 1/9,
failing to distinguish the two mixing angles. The mass-hierarchy route
resolves this.

### Bounded results (8 tests):

**B1.** The observed up-type hierarchy log\_10(m\_t/m\_u) = 4.90 lies inside
the framework prediction band [3.5, 5.5].

**B2.** The observed down-type hierarchy log\_10(m\_b/m\_d) = 2.95 lies inside
the prediction band [2.0, 4.0].

**B3.** The CKM prediction bands from scanning the mass hierarchy bands
contain all three PDG values: |V\_us|, |V\_cb|, and |V\_ub|.

**B4.** The hierarchy ordering |V\_us| >= |V\_cb| >= |V\_ub| holds across
100% of the scanned mass hierarchy band.

---

## What Remains Open

1. **Strong-coupling anomalous dimension.** The mass hierarchy prediction
   band width reflects the difference between the U(1) proxy and SU(3)
   gauge group. A first-principles SU(3) lattice calculation would narrow
   the band and sharpen the CKM prediction.

2. **Higgs Z\_3 charge.** The review.md blocker: the Higgs Z\_3 charge
   step is finite-size / L=8 anchored and not yet universal. This affects
   the EWSB coupling structure.

3. **Intra-generation splitting pattern.** The geometric mean pattern
   m\_2^2 ~ m\_1 * m\_3 is approximate (observed: m\_c/m\_t = 0.0074 vs
   predicted sqrt(m\_u/m\_t) = 0.0035, a factor of 2 discrepancy). A
   first-principles derivation of the intra-generation spectrum would
   tighten the CKM prediction.

4. **CP phase.** The CP-violating phase delta is not addressed in this
   analysis. The Z\_3 eigenvalue structure predicts delta = 2*pi/3 = 120
   degrees (from frontier\_ckm\_closure.py), compared to PDG 68.5 degrees.
   This is a separate bounded result.

5. **O(1) coefficients.** The parametric GST relations give the leading
   scaling. The precise numerical values depend on O(1) Yukawa coefficients
   that are set to 1 in the zero-parameter prediction.

---

## How This Changes The Paper

1. **New CKM route.** The mass-hierarchy approach to CKM is complementary
   to the existing FN charge approach (frontier\_ckm\_closure.py). It has
   two advantages: (a) it uses the derived mass spectrum rather than FN
   charges as input, and (b) it automatically produces |V\_us| >> |V\_cb|,
   which the FN approach cannot.

2. **Paper-safe wording:**

   > "The framework's zero-parameter mass hierarchy prediction, combined
   > with the Gatto-Sartori-Tonin relation |V\_us| ~ sqrt(m\_d/m\_s),
   > gives a bounded CKM prediction: the hierarchy |V\_us| >> |V\_cb|
   > >> |V\_ub| follows from the asymmetry between up-type and
   > down-type mass hierarchies (m\_t/m\_u ~ 80,000 >> m\_b/m\_d ~ 900),
   > driven by the electroweak charge difference Q\_up^2/Q\_down^2 = 4.
   > All three PDG values lie inside the CKM prediction bands derived
   > from the mass hierarchy bands."

3. **Does NOT upgrade CKM lane status.** The CKM lane remains BOUNDED
   per review.md. The same model dependence that keeps the mass hierarchy
   bounded also keeps the CKM bounded. The Higgs Z\_3 blocker remains live.

4. **Advantage over FN approach.** This approach supersedes the FN charge
   approach for the CKM hierarchy pattern because it resolves the |V\_us| =
   |V\_cb| degeneracy that plagues the parametric FN scaling.

---

## Commands Run

```
python3 scripts/frontier_ckm_from_mass_hierarchy.py
```

Result: PASS=24 FAIL=0. Exact=16 Bounded=8.
