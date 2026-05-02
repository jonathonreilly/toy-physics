# Cycle 04 (Retained-Promotion) Claim Status Certificate — SM Hypercharge Uniqueness Without ν_R Input (closing derivation)

**Block:** physics-loop/sm-hypercharge-no-nu-r-derivation-2026-05-02
**Note:** docs/SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_sm_hypercharge_no_nu_r_derivation.py
**Target rows:**
- direct: `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` (claim_type=positive_theorem, audit_status=unaudited, td=132, lbs_score=16.6)
- indirect (decoupled): `hypercharge_identification_note` (claim_type=positive_theorem, audit_status=audited_renaming, td=193, lbs=F)

## Block type

**Closing derivation** (output type (a) per the new retained-promotion
campaign prompt). New theorem note + runner that **removes the
load-bearing dependency on a demoted upstream row** by deriving the
SM right-handed hypercharges from anomaly cancellation alone, with NO
neutral-singlet input.

## Promotion Value Gate (V1–V5)

### V1: SPECIFIC verdict-identified obstruction this PR closes

The direct parent row (`standard_model_hypercharge_uniqueness_theorem_note_2026-04-24`)
is unaudited but has a known load-bearing weakness in its own
self-statement (§5 "Does NOT claim"):

> Does NOT claim a native-axiom derivation of `Y(ν_R) = 0`; the
> neutral-singlet identification is treated here as an input

This input is imported from `HYPERCHARGE_IDENTIFICATION_NOTE.md`,
which has audit_status=`audited_renaming` (DEMOTED). Quoted from
the demoted upstream's `verdict_rationale`:

> Repair target: provide a retained theorem constructing the physical
> map from the C^8 taste sectors to SM left-handed fermion
> representations and deriving the allowed normalization/readout
> without importing the target labels.

The demoted upstream's verdict is substantial (full C^8 → SM map +
normalization). This PR does NOT close that verdict directly. Instead:

**This PR's closing-derivation theorem demonstrates that
`standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` does
NOT actually need the `Y(ν_R) = 0` input from the demoted upstream:
the SM hypercharge values for u_R, d_R, e_R are forced uniquely by
anomaly cancellation ALONE on the framework's retained LH content
(Q_L, L_L) plus minimal SU(2)-singlet RH completion (u_R, d_R, e_R) —
without ν_R in the system at all.**

The result: the direct parent row's hypercharge uniqueness statement
becomes audit-ready WITHOUT depending on the demoted upstream.

### V2: NEW derivation contained

Existing parent note explicitly states (§5):

> Does NOT claim a native-axiom derivation of `Y(ν_R) = 0`; the
> neutral-singlet identification is treated here as an input

This PR's derivation:

1. Sets up the anomaly-cancellation system on retained LH content
   (Q_L, L_L) + minimal RH completion (u_R, d_R, e_R), WITHOUT ν_R.
2. Solves the resulting 3-equation × 3-unknown system in exact
   rational arithmetic.
3. Verifies that the system closes uniquely up to u_R↔d_R relabelling
   (same residual symmetry as the parent's 4-unknown system with
   y_4=0 input).
4. Verifies the same SM hypercharge values: y_1=+4/3, y_2=-2/3,
   y_3=-2 (exactly the SM u_R, d_R, e_R hypercharges in the doubled
   convention).
5. Q(u_R) > 0 labelling (convention) breaks the u_R↔d_R degeneracy.
6. Demonstrates that adding ν_R as a 4th species (with free y_4)
   reopens a 1-parameter family — confirming that the parent's
   neutrality input IS load-bearing IF ν_R is included, and IS NOT
   needed if ν_R is omitted.
7. Connects to the framework's anomaly-graph: the no-ν_R variant is
   the minimal anomaly-cancelling extension of (Q_L + L_L); ν_R is
   optional (its addition is consistent but not anomaly-required).

The reduction "drop ν_R → drop neutrality input → same SM hypercharges"
is the genuine new derivation.

### V3: Audit lane couldn't already do this from existing retained primitives + standard math machinery

The audit lane in restricted one-hop context cannot synthesize:
- Retained Q_L:(2,3) hypercharge from `LEFT_HANDED_CHARGE_MATCHING_NOTE`,
- Retained L_L:(2,1) from `ONE_GENERATION_MATTER_CLOSURE_NOTE`,
- The cycle 01 / cycle 02 anomaly closures
  ([PR #382](https://github.com/jonathonreilly/cl3-lattice-framework/pull/382),
  [PR #383](https://github.com/jonathonreilly/cl3-lattice-framework/pull/383)),
- Anomaly cancellation arithmetic on the no-ν_R sector,
- Closed-form solve of the cubic in y_1, y_2,

simultaneously in one hop. This is the missing standalone derivation.

### V4: Marginal content non-trivial

Yes:
- Explicit derivation that 3 anomaly equations on 3 unknowns close
  uniquely (vs 3 equations on 4 unknowns in the parent note giving
  a 1-parameter family).
- Counterfactual demonstration that adding ν_R reopens the family —
  confirming neutrality IS load-bearing IF ν_R is included.
- Connection to anomaly cancellation as quantum-consistency
  requirement (no neutrality "convention" needed in the no-ν_R
  variant).
- Exact rational arithmetic verification.
- Explicit Q(u_R)>0 labelling step preserved from the parent.
- Independence from the demoted `HYPERCHARGE_IDENTIFICATION_NOTE`.

This is genuine derivation content the parent row didn't have.

### V5: Not a one-step variant of an already-landed cycle

Cycle 01 (PR #382): SU(3)^3 cubic anomaly Diophantine enumeration over
discrete irrep cubic-anomaly coefficients ⇒ forced 3̄ completion of RH
quark sector. Result: rep choice (u_R^c, d_R^c : 3̄).

Cycle 02 (PR #383): SU(2) Witten Z_2 anomaly parity (mod 2) counting
on π_4(SU(2)) ⇒ forced even doublet count. Result: parity (4 doublets
per generation, even).

Cycle 03 (PR #386): Cauchy multiplicative-to-additive functional
equation reduction ⇒ premise reduction. Result: scalar generator
uniqueness.

**Cycle 04**: Cubic equation in continuous Y values from U(1)_Y
anomaly cancellation arithmetic (Tr[Y]=0, Tr[Y³]=0, Tr[SU(3)²Y]=0)
on no-ν_R SM matter content ⇒ forced SM hypercharge values.

Different math (cubic equation in continuous Y vs Diophantine over
discrete reps vs parity vs functional equation), different anomaly
trace (mixed gauge-gauge-Y vs SU(3)^3 vs SU(2) Witten vs Cauchy),
different parent row, different specific result (Y values vs rep
choice vs parity vs scalar generator structure).

Not a one-step variant.

## Outcome classification (per new prompt)

**(a) Closing derivation.** This PR provides a new theorem note +
runner that **removes the load-bearing dependency on a demoted
upstream** by deriving the result without that dependency.

The outcome IS retained-positive movement on the parent row's
hypercharge uniqueness derivation chain, conditional on audit-lane
ratification of:
- the framework's retained LH content (Q_L, L_L);
- the framework's retained RH-completion existence
  (`ANOMALY_FORCES_TIME_THEOREM` Step 2);
- the standard ABJ anomaly cancellation requirement;
- the Q(u_R) > 0 labelling convention.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Adler 1969,
  Bell-Jackiw 1969 are admitted-context external mathematical
  authorities, role-labelled).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention beyond the
  doubled-Y `Q = T_3 + Y/2` convention shared with parent.
- No same-surface family arguments.
- **No load-bearing dependency on the demoted
  `HYPERCHARGE_IDENTIFICATION_NOTE`.** This is the key value
  proposition.

## Audit-graph effect

If independent audit ratifies this derivation:

- Parent row `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24`
  becomes self-contained on retained primitives + admitted-context
  ABJ math + Q-labelling convention. No load-bearing dependency on
  any demoted row.
- The chain to td=132 transitive descendants of the parent row
  becomes verifiable without re-auditing the demoted upstream.
- The demoted `hypercharge_identification_note`'s scope (taste-sector
  C^8 → SM map + normalization) becomes a separately-decidable
  question, not a load-bearing input to hypercharge uniqueness.

## Honesty disclosures

- This PR does NOT close the demoted upstream
  (`hypercharge_identification_note`) — that requires deriving the
  C^8 → SM map and Y normalization, a substantial separate task.
- This PR does NOT claim ν_R is forbidden — only that it's not needed
  for SM hypercharge uniqueness. The framework can include ν_R with
  any y_4 (with anomaly conditions then giving a 1-parameter family),
  or omit it. Cosmological/neutrino-oscillation considerations are
  separate.
- The Q(u_R) > 0 labelling is a convention; without it the system has
  the residual u_R↔d_R relabelling. This PR preserves the parent's
  convention without modification.
- Adler 1969 + Bell-Jackiw 1969 (ABJ anomaly cancellation requirement)
  are admitted-context external mathematical authorities.
- The runner does not modify any audit-ledger file.
- Audit-lane ratification required before any retained-grade status
  applies; no author-side tier asserted.
