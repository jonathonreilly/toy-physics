# Handoff Note — Ward-Decomposition Pass (Second Pass, PR #230)

**Loop slug:** yt-top-mass-substrate-pin-ward-clean-20260430  
**Date:** 2026-04-30  
**Branch:** `claude/yt-direct-lattice-correlator-2026-04-30` (PR #230)  
**Runtime used:** ~1 deep-block session (Ward-decomposition analysis)  
**Cycles completed:** 1 (two-pass structured no-go now complete)

---

## Summary of Claim-State Movement

| Item | Before | After |
|---|---|---|
| Ward-decomp route | surviving candidate (per prior handoff) | no-go / exact-negative-boundary |
| WTI route (actual QFT Ward identities) | unattempted | ruled out: WTI constrains gauge vertex, not Yukawa |
| HS route | unattempted | ruled out: σ ≡ H_unit via D17 (audited_renaming in disguise) |
| Source-functional route | unattempted | ruled out: canonical normalization requires D17 = H_unit |
| Fierz-alone route | unattempted | ruled out: 4-fermion coeff ≠ Yukawa without scalar ID |
| PR #230 derivational status | one open route remaining | no open routes; calibration confirmed |

**Combined two-pass result:** Complete no-go across all nine route classes
(five-frame pass + four Ward-decomposition routes). No surviving candidate for
a non-MC top-sector substrate pin within the stated forbiddance set.

---

## Artifacts Committed to This Branch (This Pass)

| File | Role |
|---|---|
| `docs/YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md` | Ward-decomposition four-route no-go theorem note |
| `docs/YT_TOP_MASS_WARD_DECOMP_ASSUMPTIONS_AND_IMPORTS_2026-04-30.md` | Import ledger for this pass |
| `docs/YT_TOP_MASS_WARD_DECOMP_CLAIM_STATUS_CERTIFICATE_2026-04-30.md` | Status certificate |
| `docs/YT_TOP_MASS_WARD_DECOMP_HANDOFF_2026-04-30.md` | This file |
| `scripts/frontier_yt_top_mass_ward_decomp_no_go.py` | Verification runner (PASS=24 FAIL=0) |

**Previously committed (Pass 1):**

| File | Role |
|---|---|
| `docs/YT_TOP_MASS_SUBSTRATE_PIN_NO_GO_NOTE_2026-04-30.md` | Five-frame no-go |
| `docs/YT_TOP_MASS_SUBSTRATE_PIN_ASSUMPTIONS_AND_IMPORTS_2026-04-30.md` | Pass-1 import ledger |
| `docs/YT_TOP_MASS_SUBSTRATE_PIN_CLAIM_STATUS_CERTIFICATE_2026-04-30.md` | Pass-1 certificate |
| `docs/YT_TOP_MASS_SUBSTRATE_PIN_HANDOFF_2026-04-30.md` | Pass-1 handoff |
| `scripts/frontier_yt_top_mass_substrate_pin_no_go.py` | Pass-1 runner (PASS=19 FAIL=0) |

---

## The Exact Audit-Clean Obstruction

```
D9  →  No bare Yukawa term in Cl(3)×Z³ action
D12 + S2 + D16  →  Γ^(4)_S = -G_eff O_S / q²  [four-fermion amplitude, G_eff=1/6]
                       ↓
       y_t_bare := √G_eff requires factorization: Γ^(4) = -y²/q² O_S
                       ↓
       Factorization requires: scalar propagator 1/q² + scalar-fermion coupling y
                       ↓
       Scalar field ID on Q_L: D17 → unique composite = H_unit
                       ↓
       Using D17 as a definition source = audited_renaming obstruction
```

No authorized route (WTI, HS, source-functional, Fierz-alone) bypasses the
D17 node.  The four-fermion OGE amplitude is NOT a Yukawa coupling; it requires
a named scalar field to become one.

---

## Implications for PR #230

**The two-pass structured no-go finalizes the claim boundary for PR #230:**

1. **Confirmed calibrated-readout status**: Under the current forbiddance set,
   the direct staggered-correlator lane measures `m_t → y_t` as a calibrated
   physical-observable readout.  No substrate-native non-MC pin was found.

2. **Confirmed recovery path**: The Ward route (H_unit identification) is the
   sole substrate-native pin.  It derives `y_t_bare = 1/√6` exactly.  The
   `audited_renaming` failure arose from the *presentation* of Rep B as a
   definition (eq. 3.7), not from any error in the algebra.

3. **Audit-clean reformulation for future work**: A re-audit of the Ward route
   should focus on whether D17 constitutes a *definition source* or a *consistency
   check* for y_t_bare.  The distinction:
   - **Definition source** (current presentation): y_t_bare is DEFINED as
     `⟨0|H_unit|t̄t⟩`. Then OGE confirms the value. → audited_renaming.
   - **Consistency check** (alternative reading): y_t_bare is the effective
     coupling emergent from the OGE amplitude in the scalar singlet channel.
     D17 then confirms that the unique scalar composite in this channel has
     normalization Z = √6, giving y_t_bare = g/√(2N_c) = 1/√6.  
     This reading makes the OGE amplitude (Rep A) the primary input and D17
     a consistency verification, not a definition.  Whether this reframing
     resolves the `audited_renaming` flag is a question for a future audit.

---

## Proposed Repo Weaving (For Later Review — Do NOT weave during loop)

1. Add row to audit ledger for `yt_top_mass_ward_decomp_no_go_note_2026-04-30`:
   - Status: `unaudited` / `exact-negative-boundary` (author claim)
   - Note: "Two-pass structured search complete.  Four Ward-decomposition routes
     exhausted.  Exact obstruction: D17/H_unit identification is load-bearing for
     all authorized routes."

2. Update PR #230 body to reference the two-pass no-go and add section on
   Ward-decomposition pass results.

3. Consider revising the `audited_renaming` framing for the Ward note: the
   algebraic content is correct; the audit question is whether Rep B's
   presentation (eq. 3.7 as a DEFINITION) is necessary or whether Rep A +
   D17-as-consistency gives a cleaner derivation path.

---

## Stop Condition

The Ward-decomposition pass has closed all authorized routes.  The combined
two-pass structured search has exhausted all non-MC, non-H_unit, non-fitted
route classes under the stated forbiddance set.

A further campaign could:
- Attempt to reformulate the Ward route without equation 3.7 as a definition
  (changing the presentation rather than the algebra)
- Explore dynamical substrate extensions (SUSY, compositeness, new axiom)
- Accept PR #230 at calibrated-readout status (honest current status)

None of these is within the authorized scope of the current two-pass campaign.

---

## Next Actions

1. **Update PR #230 body** to record the Ward-decomposition pass results.

2. **File for independent audit** (when audit queue available): Two-pass
   structured no-go packet:
   - `YT_TOP_MASS_SUBSTRATE_PIN_NO_GO_NOTE_2026-04-30.md` (Pass 1, runner PASS=19)
   - `YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md` (Pass 2, runner PASS=24)

3. **Optional future direction**: Re-examine the Ward note presentation to
   determine if removing eq. 3.7 as a *definition* (replacing with a consistency
   check framing) resolves the `audited_renaming` flag.  This does not change
   the no-go result for the current forbiddance set.
