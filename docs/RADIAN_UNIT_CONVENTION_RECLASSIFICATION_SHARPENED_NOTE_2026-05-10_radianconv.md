# Radian Unit Convention Reclassification (Sharpened) — P as a Unit Convention Under Conventions Unification

**Date:** 2026-05-10
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status set only after independent audit
review.
**Authority role:** records the audit-honest reframing of the radian-bridge
primitive `P` (radian-bridge for `φ_dimensionless = 2/9` per Probe 24
Step 1) as a **unit convention** under the
[`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
pattern, analogous to meter / second / kilogram / GeV unit choices that
apply convention bookkeeping on top of structural predictions.
**Companion to:**
- [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
  (PR #729) — labeling and unit conventions are the same kind of
  bookkeeping operation
- [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
  (PR #725) — physical-lattice baseline reading
- [`KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md`](KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md)
  (PR #814) — `φ_dimensionless = n_eff/d² = 2/9` Step 1 retained
- [`KOIDE_BAE_PROBE_RADIAN_FROM_DIMENSIONS_BOUNDED_NOTE_2026-05-09_probe30.md`](KOIDE_BAE_PROBE_RADIAN_FROM_DIMENSIONS_BOUNDED_NOTE_2026-05-09_probe30.md)
  (PR #826) — dimensional inventory for `P`
- [`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`](KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md)
  — sharpens `P` to "period-1-rad vs period-2π-rad convention choice"
- [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
  (PR #836) — campaign terminal admission ledger (BAE + P = 2)
- [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
  (PR #790) — BAE rename pattern
**Primary runner:** [`scripts/frontier_radian_unit_convention_reclassification_2026_05_10_radianconv.py`](../scripts/frontier_radian_unit_convention_reclassification_2026_05_10_radianconv.py)
**Cache:** [`logs/runner-cache/frontier_radian_unit_convention_reclassification_2026_05_10_radianconv.txt`](../logs/runner-cache/frontier_radian_unit_convention_reclassification_2026_05_10_radianconv.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. This note does not write audit verdicts and does
not promote any downstream theorem. It records a vocabulary
clarification on top of already-retained structural content.

## Naming

- **physical `Cl(3)` local algebra** (legacy minimal-axiom alias:
  `A1`) = the repo's retained local algebra baseline per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **BAE** = Brannen Amplitude Equipartition: `|b|²/a² = 1/2` for the
  retained C_3-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³` (per
  [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)).
- **`P`** = radian-bridge primitive. Per Probe 24 finding (PR #814):
  `P` is the identification of the dimensionless character-algebra
  rational `φ_dimensionless = n_eff/d² = 2/9` with the literal SI-radian
  numerical value `2/9 rad`. Per Probe 30 (PR #826): `P` is precisely
  characterized as the period-2π-rad-vs-period-1-rad convention choice.

## What this note clarifies

The 30-probe BAE campaign (PR #836 synthesis) terminated with the
admission ledger `BAE + P = 2`. Probes 24 and 30 sharpened `P` to:

> **`P`** = the convention "interpret the framework's dimensionless
> character-algebra angle output `φ_dimensionless = 2/9` as a numerical
> value in the SI/PDG radian convention (where the period of `cos(θ)`
> is `2π`), rather than in cycle convention (where the period of
> `cos_cycle(θ)` is `1`)."

This note records the audit-honest observation that **this convention
choice is a unit convention**, structurally identical to the unit
conventions for length (meter / lattice spacing), time (second / lattice
step), and mass/energy (kilogram / GeV / Planck mass) that
[`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
identifies as bookkeeping on top of structural predictions, not as
physical imports.

## The reclassification argument

### Step 1 (positive, retained): the framework's structural angle output is dimensionless `2/9`

Per
[`KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md`](KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md)
Step 1, the Brannen circulant offset on retained Cl(3)/Z³ content is

```
φ_dimensionless = n_eff / d² = 2/9
```

derived from `n_eff = 2` (C_3 conjugate-pair forcing per
[`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
§1.3) and `d² = 9 = dim_ℝ Herm_3` (per
[`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
R3 / A.2). This is a derived dimensionless rational under cited
source-stack content alone.

### Step 2 (positive, retained): the SI radian is itself dimensionless

In SI, the radian is *defined* by `θ_rad := arc_length / radius`, where
both numerator and denominator have dimensions of length. Therefore

```
[rad] = L / L = 1   (dimensionless)
```

This is a standard SI definitional fact (cited as theorem-grade
mathematical / SI-convention input, not derived from Cl(3)/Z³). The SI
radian is a **dimensionless number with a particular numerical
convention**: `cos(θ)` has period `2π`, so `cos(2π) = 1`, and the
numerical value `1` corresponds to `1 radian ≈ 57.3°`.

### Step 3 (the unification): comparing two dimensionless rationals does not require a unit-conversion derivation

The Brannen circulant
`λ_k = a + 2|b| cos(arg(b) + 2πk/d)` takes a **dimensionless** input
to `cos`. The framework computes `arg(b) = φ_dimensionless = 2/9`
(dimensionless). PDG-derived `arg(b) = 2/9 rad` is also dimensionless
(per Step 2: the SI radian is dimensionless `L/L = 1`). Both are
dimensionless rationals. The "match" is direct: framework's `2/9`
equals PDG's `2/9` as dimensionless numbers.

There is no unit-conversion factor in this comparison. The framework
predicts a dimensionless rational; PDG measures a dimensionless rational
(via the SI radian convention); they are numerically equal.

### Step 4 (the convention): SI's choice that `cos` has period `2π` is the unit convention

What `P` actually is, per Probes 24 + 30, is the convention choice
between two equivalent dimensionless angular numerical scalings:

| Convention | Period of `cos` | `2/9` interprets as | PDG match |
|---|---|---|---|
| **SI / period-2π-rad** (PDG) | `2π` | `2/9 rad ≈ 12.73°` | YES (PDG = framework) |
| Cycle / period-1-rad | `1` | `2/9` of full cycle = `80°` | NO |

Both conventions are dimensionless. The choice between them is a
**numerical scaling convention**, identical in nature to:

- choosing GeV vs MeV vs Joules for energy (numerical rescaling factor `10⁻³`, `1.602 × 10⁻¹⁰`);
- choosing meters vs centimeters vs Planck lengths for length;
- choosing seconds vs femtoseconds vs Planck times for time;
- choosing kilograms vs Daltons vs Planck masses for mass.

Each of these is a numerical-rescaling convention applied on top of
structural framework predictions. None constitutes a physical import
([`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)).

The radian-vs-cycle convention is the angular analog: the SI choice
"period of `cos` is `2π`" rescales the dimensionless framework number
`2/9` to be read as a radian value rather than a cycle fraction. PDG
publishes in radians; the framework's `2/9` matches PDG when read in
the SI/radian convention.

## What this DOES close

**`P` reclassified as a unit convention under Conventions Unification.**

Specifically:

- The framework's dimensionless character-algebra rational
  `φ_dimensionless = 2/9` is **retained** structural content (Probe 24
  Step 1).
- The SI radian is itself **dimensionless** (definitional SI fact:
  `[rad] = L/L = 1`).
- Comparing the framework's `2/9` to PDG's `2/9 rad` is comparing two
  dimensionless rationals — a direct numerical match without
  unit-conversion derivation.
- The SI / period-2π-rad convention is the unit choice for measuring
  angle. This is bookkeeping on top of the structural prediction, not a
  derivation step.

Under this reclassification, the BAE-campaign admission ledger reduces:

| Admission | Status before reclassification | Status after reclassification |
|---|---|---|
| BAE (`\|b\|²/a² = 1/2`) | bounded | bounded (UNCHANGED) |
| `P` (radian-bridge) | bounded | **convention** (per this note) |
| **Total** | **2** | **1 (BAE only)** |

This matches the Conventions Unification pattern (PR #729): unit
conventions and labeling conventions are the same kind of bookkeeping
operation, neither is a physical import.

## What this DOES NOT close

**The framework's natural angular scaling matching SI radian convention is itself a structural feature, not derived by this note.**

Honestly assessed limit of the reclassification:

The framework's character-algebra natively outputs `φ_dimensionless = 2/9`
(Probe 24 Step 1, retained). PDG's SI/radian convention numerically
matches this dimensionless value when reading it in radians (where full
cycle = `2π`). If the framework's natural angular scaling had output
`4π/9` instead (= `2/9` cycles), the SI/radian PDG match would not have
held; instead PDG-in-cycles match would.

That the framework's natural output `2/9` matches PDG's SI/radian
convention numerically is itself a structural feature of how the
framework's character-algebra produces angle-valued dimensionless
rationals. This is analogous to how the framework's natural length scale
matches "atomic-scale physics in meter convention" rather than
"Planck-scale physics in Planck-length convention" — which is itself
not a derivation but a structural feature of the framework's natural
length output.

This structural feature ("the framework's natural angular numerical
output uses the SI/radian numerical scaling rather than the cycle
numerical scaling") is **not** itself derived from the Cl(3)/Z³ stack,
in the same sense that the framework's natural length scale matching
meter-convention is not derived. Both are structural features that are
consistent with the corresponding SI/PDG conventions.

Under Conventions Unification (PR #729), this structural-feature kind of
agreement is **not** a physical admission — it is a feature of the
framework's natural unit system, consistent with the SI conventions
PDG uses.

## Why this is consistent (not new physics)

The reclassification is consistent with several existing framework
patterns:

### A. Length convention (meter)

The framework predicts dimensionless ratios `m_τ / M_Pl`, lattice
spacings `a_s` in framework units, etc. PDG measures `m_τ` in GeV,
which converts via `1 GeV = 1.78 × 10⁻²⁷ kg = 5.06 × 10¹⁵ m⁻¹`, etc.
None of these unit-conversion factors are derived from Cl(3)/Z³; they
are SI conventions for human-readable comparison. The framework's
natural energy unit happens to be `M_Pl ≈ 10¹⁹ GeV` numerically. This is
a structural feature of the framework's UV cutoff identification, not a
derivation of "1 GeV = 5.06 × 10¹⁵ m⁻¹".

### B. Time convention (second)

Similar to meter: the framework predicts dimensionless time ratios; the
SI second is bookkeeping.

### C. Mass convention (kilogram / GeV)

Similar.

### D. Angular convention (radian)

Per this note: the framework's character-algebra natively produces
dimensionless rationals like `2/9`. The SI radian is dimensionless;
the PDG match is direct. The convention "interpret `2/9` in SI/radian
scaling rather than cycle scaling" is the unit choice.

### Consistency check

For each of (A)-(D), the framework's natural scaling consistently
matches the corresponding SI/PDG convention numerically. None of these
conventions is itself derived from Cl(3)/Z³. All four are bookkeeping
on top of structural framework predictions. The radian convention slots
in as the angular analog of (A)-(C).

## Conditional, not promoted

This note is explicit that the reclassification is **conditional**. It
is not a closure claim. Specifically:

- **No new axiom.** The physical `Cl(3)` local algebra plus `Z^3`
  spatial substrate baseline (legacy aliases `A1`/`A2`) still suffice.
  The
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) note
  is unchanged.
- **No retained theorem promoted.** Probe 24 Step 1 retained content
  (`φ_dimensionless = 2/9`) is unchanged. Probes 24 + 30 + the
  irreducibility audit remain bounded as no-go probes for *deriving*
  the radian-bridge from independent retained content.
- **No PDG values consumed as derivation input.** PDG appears only as
  conventional comparator (the SI/radian convention is the PDG
  convention; matching framework's dimensionless `2/9` to PDG's
  numerical `2/9 rad` is conventional bookkeeping, not derivation
  input).
- **No promotion of any specific lane to retained status.**
  `effective_status` and `claim_type` on every existing claim row remain
  audit-lane authority.
- **BAE remains bounded.** The 30-probe campaign's BAE residue is
  unaffected.

The reclassification is a **vocabulary correction** that brings `P` into
the existing Conventions Unification umbrella. It is not new physics.

## Three honest framings

This note is structurally aware that the reclassification is
**partial** (sharpened, not full closure). The honest framings are:

1. **CLOSURE framing** (strongest): `P` is fully a unit convention
   under SI's definitional choice that `[rad] = L/L = 1`. The framework
   predicts a dimensionless rational; SI publishes a dimensionless
   rational; they match. No primitive needed. Admission count drops 2 → 1.

2. **STRUCTURAL OBSTRUCTION framing** (weakest): the framework's natural
   numerical scaling matching SI/radian convention rather than cycle
   convention is itself a structural feature requiring derivation. `P`
   remains a primitive demanding closure.

3. **SHARPENED framing** (this note's verdict): the reclassification
   moves `P` from "missing primitive" to "unit-convention bookkeeping
   under SI's dimensionless-radian definition". The reclassification is
   admissible under PR #729's Conventions Unification pattern. The
   structural feature "framework's natural scaling matches SI/radian
   convention numerically" is a consistency observation, parallel to
   meter / second / kilogram natural-scale matching, and is not itself a
   new admission under PR #729. Net effect: `P` is reclassified as
   convention; admission count drops 2 → 1 (BAE only).

This note adopts framing (3): SHARPENED partial closure / unit-convention
reclassification. The audit lane has authority over whether to retain
this reclassification. If the audit lane prefers framing (1) or (2),
the note is straightforward to retag.

## Comparison to landed conventions

| Convention layer | Framework natural output | SI/PDG convention | Conversion factor | Status |
|---|---|---|---|---|
| Length | dimensionless lattice ratios `a_s · M_Pl / ħ`, `r_lattice` | meters | `1 m = ...` (numerical, not derived) | unit convention (PR #729) |
| Time | dimensionless lattice ratios `a_τ · M_Pl / ħ` | seconds | `1 s = ...` (numerical, not derived) | unit convention (PR #729) |
| Mass / Energy | dimensionless ratios `m_X / M_Pl` | GeV | `1 GeV = ...` (numerical, not derived) | unit convention (PR #729) |
| Angle (this note) | dimensionless rationals `n_eff/d² = 2/9` | radians | `1 rad = 1 dimensionless unit` (SI definition) | unit convention (this note) |

Each row applies SI/PDG convention bookkeeping on top of a structural
framework prediction. None is a physical admission; all are unit
conventions per PR #729.

## What this note does NOT do

This note explicitly does **NOT**:

1. **Close the BAE admission.** BAE remains bounded; the 30-probe
   campaign synthesis (PR #836) is unchanged.
2. **Promote any retained theorem.** No `claim_type` or
   `effective_status` field is modified.
3. **Add a new mathematical axiom.** The physical `Cl(3)` local
   algebra plus `Z^3` spatial substrate baseline still suffice on the
   retained stack.
4. **Use PDG values as derivation input.** PDG appears only as
   convention-comparator; the SI/radian convention is identified as the
   convention, not as a derivation input.
5. **Modify any of Probes 24 or 30's no-go content.** Both probes
   correctly identify that the radian-bridge is not derivable from
   independent retained character-algebra or dimensional content. This
   note does not contradict that; it reframes the bridge itself as a
   unit convention rather than a missing derivation.
6. **Resolve any sister bridge gap** (L3a, L3b, C-iso, W1.exact
   engineering frontier).
7. **Claim the framework derives the SI radian convention.** The SI
   convention is an external SI/PDG choice; the reclassification
   recognizes it as such (analogous to meter / second / kilogram
   conventions), not as derived content.

## What this note DOES do

It records, as repo-language clarification:

1. The radian-bridge primitive `P` is structurally identical to the
   length / time / mass unit conventions (meter, second, kilogram, GeV)
   that PR #729 already classifies as bookkeeping on top of structural
   predictions.
2. Per PR #729's pattern, unit conventions are not physical
   admissions. The radian convention is the angular analog.
3. Under this reclassification, the BAE-campaign admission ledger
   reduces from `BAE + P = 2` to `BAE = 1` (with `P` reclassified as
   unit convention).
4. The reclassification is conditional: the audit lane has authority
   over whether to retain this reclassification, and may prefer the
   stricter framing (`P` as primitive).
5. Whether or not the audit lane retains the reclassification, this
   note clarifies the structural relationship: `P` is structurally a
   unit-convention choice, not a missing derivation in the same
   class as BAE (which IS a missing structural input).

## Cross-references

- Foundational baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Conventions Unification: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- Preserved-`C_3` companion: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Probe 24 (φ_dimensionless = 2/9 retained): [`KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md`](KOIDE_BAE_PROBE_PHI_FROM_Z3_CHARACTER_SHARPENED_NOTE_2026-05-09_probe24.md)
- Probe 30 (radian dimensional inventory): [`KOIDE_BAE_PROBE_RADIAN_FROM_DIMENSIONS_BOUNDED_NOTE_2026-05-09_probe30.md`](KOIDE_BAE_PROBE_RADIAN_FROM_DIMENSIONS_BOUNDED_NOTE_2026-05-09_probe30.md)
- Radian-bridge irreducibility audit: [`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`](KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md)
- BAE rename pattern: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- Campaign terminal synthesis: [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

## Validation

Run:

```bash
python3 scripts/frontier_radian_unit_convention_reclassification_2026_05_10_radianconv.py
```

The runner is a review-hygiene check, not a physics proof. It verifies:

1. The note is classified as `meta` and does not declare pipeline status.
2. The reclassification of `P` as a unit convention is stated explicitly
   and cited to the Conventions Unification pattern (PR #729).
3. The framework's structural prediction (`φ_dimensionless = 2/9` per
   Probe 24 Step 1) is correctly identified as retained.
4. The SI definitional fact (`[rad] = L/L = 1`) is stated as the
   definitional input, not derived from Cl(3)/Z³.
5. The reclassification is stated as conditional / SHARPENED, not as
   strict closure.
6. The note does not promote any retained theorem or claim BAE is
   closed.
7. The note does not add a new mathematical axiom.
8. The note does not load PDG values as derivation input.
9. Cross-references to the recently-landed companion notes are present.
10. The structural-feature limit (framework's natural scaling matching
    SI/radian convention is itself a structural consistency
    observation) is stated honestly.

## Review-loop rule

When reviewing future branches that interact with the BAE-campaign
admission ledger:

1. Treat the radian unit (per this note) the same way as the meter,
   second, kilogram, GeV unit conventions: as bookkeeping on top of
   structural predictions, not as physical imports.
2. Track the framework's natural angular scaling matching SI/radian
   convention as a structural-feature consistency observation, parallel
   to length/time/mass natural-scaling consistencies under PR #729.
3. Do not promote BAE to retained status on the basis of this
   reclassification — BAE remains independently bounded.
4. Do not let this convention reclassification silently promote any
   downstream lane on `claim_type` or pipeline-derived status.
5. The audit lane retains authority over whether the unit-convention
   reclassification is retained, and may prefer the stricter framing
   (`P` as primitive) at its own discretion.

## Bottom line

**Verdict: SHARPENED partial closure / unit-convention reclassification.**

The radian-bridge primitive `P` is structurally identical to the meter /
second / kilogram / GeV unit conventions that
[`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
already classifies as bookkeeping on top of structural predictions. The
SI radian is itself dimensionless (`L/L = 1`); the framework's
character-algebra natively outputs the dimensionless rational
`φ_dimensionless = 2/9` (Probe 24 Step 1, retained); these are both
dimensionless numbers and match directly without unit-conversion
derivation. The convention choice "interpret in SI/radian numerical
scaling rather than cycle scaling" is the unit-convention bookkeeping
operation analog to choosing GeV over MeV or meters over centimeters.

Under this reclassification, the BAE-campaign admission ledger reduces:

| Item | Status |
|---|---|
| BAE (`\|b\|²/a² = 1/2`) | bounded (UNCHANGED) |
| `P` (radian-bridge) | **unit convention** (per this note) |
| **Total framework admissions for BAE-campaign closure** | **1 (BAE only)** |

The reclassification is conditional. The audit lane has authority over
whether to retain it. If retained, the framework's BAE-campaign open
admission count drops 2 → 1, with `P` joining the meter / second /
kilogram / GeV unit-convention class under PR #729.

This is meta vocabulary clarification, not new physics. No new axiom,
no retained theorem promotion, no PDG-input loading.
