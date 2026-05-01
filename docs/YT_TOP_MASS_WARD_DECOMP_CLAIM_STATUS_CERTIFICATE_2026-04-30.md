# Claim Status Certificate — Ward-Decomposition Pass

**Block:** ward-decomp-pass-block01  
**Loop slug:** yt-top-mass-substrate-pin-ward-clean-20260430  
**Branch:** `claude/yt-direct-lattice-correlator-2026-04-30` (PR #230)  
**Artifact:** `docs/YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md`  
**Runner:** `scripts/frontier_yt_top_mass_ward_decomp_no_go.py` (PASS=24 FAIL=0)  
**Assumptions ledger:** `YT_TOP_MASS_WARD_DECOMP_ASSUMPTIONS_AND_IMPORTS_2026-04-30.md`  
**Date:** 2026-04-30

---

## Status

```yaml
actual_current_surface_status: no-go / bounded-negative-boundary
conditional_surface_status: >
  W-I (WTI structural) and W-IV (4-fermion definitional) are unconditional.
  W-II (HS) and W-III (source-functional) are conditional on D9 + D17 retained.
  W-V (SDE/BHL gap equation) is blocked by plaquette/alpha_LM forbidden set.
hypothetical_axiom_status: >
  Conditional on: permitting D17 as a definition source (rather than only
  a consistency check), the Ward route gives exact y_t_bare = 1/sqrt(6).
  This conditional status is not on the current surface.
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: >
  This block produces a no-go. There is no positive substrate pin to
  propose for retained-grade promotion. The exact obstruction has been
  identified and runner-verified.
audit_required_before_effective_retained: false
bare_retained_allowed: false
```

---

## What This Block Establishes

1. **Route W-I (actual WTI):** Standard Ward-Takahashi identities (gauge WTI,
   PCAC, BRST/STI) do not constrain the Yukawa coupling. PCAC uses m_t as an
   INPUT. No WTI enforces `y_t = f(g)` from symmetry alone.

2. **Route W-II (HS rewrite):** The HS auxiliary field σ in the Q_L scalar-
   singlet channel is algebraically equivalent to H_unit by D17. The HS route
   reintroduces the H_unit identification under the name "σ". audited_renaming
   obstruction applies.

3. **Route W-III (source-functional):** The 1PI residue gives y_eff = 1/√6
   ONLY when the normalization Z = √6 is provided by D17. Without D17, y_eff is
   undetermined. With D17, the route is equivalent to the H_unit matrix-element
   definition. audited_renaming obstruction applies.

4. **Route W-IV (Fierz/OGE alone):** D12+S2+D16 give the OGE four-fermion
   amplitude Γ^(4) = -G_eff O_S / q². This is NOT a Yukawa coupling (3-point
   function) until a scalar field is identified. The scalar field is H_unit
   (D17). Without D17/H_unit, the factorization step has no canonical definition.

5. **Synthesis:** All four authorized routes require D17 (H_unit uniqueness) at
   the same obstruction node. D9 confirms there is no bare Yukawa parameter, so
   y_t_bare is emergent and its canonical definition requires the composite Higgs
   identification that D17 provides. The Ward route is a consistency check
   (Rep A = Rep B), not an independent derivation of y_t_bare.

---

## Allowed PR/Status Wording

- "no-go / exact-negative-boundary" — allowed
- "Ward-decomposition pass: no audit-clean pin found" — allowed
- "audited_renaming obstruction confirmed across all four authorized routes" — allowed
- "D17/H_unit identification is the single load-bearing obstruction node" — allowed
- "exact obstruction: D9 + D17 + no bare Yukawa ⟹ any y_t_bare definition requires H_unit" — allowed
- "PASS=24 FAIL=0 (runner-verified)" — allowed

## Forbidden PR/Status Wording

- bare "retained" / "promoted"
- "proposed_retained" / "proposed_promoted"
- "closes the top-mass pin blocker"
- "the Ward route is derivationally clean"
- any wording that suggests a positive pin was found

---

## Verification

```bash
python3 scripts/frontier_yt_top_mass_ward_decomp_no_go.py
# Expected: PASS=24  FAIL=0
```

---

## Relationship to Prior Block

The prior block (`yt-top-mass-substrate-pin-20260430`, five-frame no-go) named
the Ward-decomposition route as the only surviving candidate.  This block closes
that candidate with a narrow audit-clean decomposition of the obstruction.

Together, the two blocks establish a **complete two-pass structured no-go**:

| Pass | Routes covered | Status |
|---|---|---|
| Pass 1 (five-frame) | spectral, topological, taste, algebraic, anomaly | exact-negative-boundary |
| Pass 2 (Ward-decomp) | WTI, HS, source-functional, Fierz-alone | exact-negative-boundary |

**Combined claim:** No non-MC top-sector heavy mass/Yukawa parameter pin exists
within the Cl(3)/Z³ substrate under the stated forbiddance set, across all nine
route classes explored in the two-pass structured search.

---

## Independent Audit Guidance

A future auditor should verify:

1. **W-I route:** Confirm that no WTI in the SM gauge theory (SU(3)×SU(2)×U(1))
   mixes the gauge and Yukawa sectors. Check PCAC for heavy-quark PCAC relation.

2. **W-II (HS):** Confirm that the HS auxiliary field in the Q_L scalar-singlet
   channel of the Cl(3)/Z³ framework must be identified with the composite degree
   of freedom picked out by D17.

3. **W-III (source-functional):** Confirm that the canonical normalization of the
   source operator (ψ̄ψ)_{(1,1)} requires D17's result Z² = 6.

4. **W-IV (Fierz):** Confirm that a four-fermion amplitude coefficient cannot be
   called a "Yukawa coupling" without specifying a mediating scalar propagator
   and hence a scalar field.

5. **Synthesis:** Confirm the D9 + D17 claim: in a theory with no bare Yukawa
   (D9), any effective Yukawa must be extracted from the composite structure,
   and D17 is the normalization source for the unique composite in the relevant
   channel.
