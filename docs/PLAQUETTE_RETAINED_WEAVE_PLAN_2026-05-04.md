# Plaquette Retained Weave Plan

**Date:** 2026-05-04
**Source PR:** [#528](https://github.com/jonathonreilly/cl3-lattice-framework/pull/528) — proposes retained promotion of ⟨P⟩(β=6)
**Companion weave PR:** TBD (#529 expected) — proposed downstream updates
**Status:** depends on PR #528 audit ratification

## Purpose

Once PR #528's proposed retained promotion of `⟨P⟩(β=6) = 0.5934` is
audit-ratified, multiple downstream docs need status language updates to
reflect the framework-native retained basis (instead of "imported MC",
"bounded scope", etc.).

This plan identifies the updates needed and provides the basis for the
companion weave PR.

## Scope of weave

### Numerical value: UNCHANGED

The plaquette numerical value `0.5934` is UNCHANGED — only the
status/scope language updates. Existing α_LM, u_0, α_s(v), α_s(M_Z)
values are all unchanged.

### Status language updates

| Old language | New language |
|---|---|
| "imported MC value" | "framework-native MC + L→∞ extrapolation" |
| "bounded by MC evaluation envelope" | "retained on numerical L→∞ extrapolation" |
| "same-surface evaluated value" | "framework-derived value" |
| "explicit caveat about imported scope" | (remove caveat after audit ratification) |
| "open analytic insertion" | "open analytic closure (SDP bootstrap path identified)" |

## Priority 1 docs (direct downstream of ⟨P⟩)

### 1. ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md

**Current**: "Using the retained plaquette value `<P> = 0.5934`"

**Proposed update**: explicit reference to PR #528's framework-native
verification:
- Add status amendment 2026-05-04 noting plaquette is now retained via
  framework-native L→∞ extrapolation (per PR #528)
- Update boundary discussion to remove any "MC import" caveat

**Affected lines:** ~68, ~88

### 2. ALPHA_S_DERIVED_NOTE.md

**Current**: status `bounded` due to plaquette open (per 2026-05-01 amendment)

**Proposed update**: status `proposed_retained` after PR #528 ratification
- Status amendment 2026-05-04 noting plaquette is now retained
- Numerical chain `<P> = 0.5934 → α_s(M_Z) = 0.1181` is now framework-native
- Still bounded on running bridge (separate scope; QCD_LOW_ENERGY_RUNNING_BRIDGE
  is standard SM infrastructure)

**Affected lines:** ~1-15 (status), ~88-99 (downstream chain)

### 3. GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md

**Current**: uses "same-surface evaluated value" language for 0.5934
**Current**: "best analytic candidate" 0.59353 with constant-lift

**Proposed update**:
- Add 2026-05-04 amendment: framework-native MC + L→∞ extrapolation
  matches 0.5934 within 0.2σ; the "best analytic candidate" 0.59353 from
  constant-lift was disproven by the slope theorem (which the framework
  itself derived); the constant-lift form is now retired as a candidate
- Status: bridge support remains valid for class-level pieces; ⟨P⟩
  numerical claim is now retained
- Note: V-invariance is correctly identified as class-level support
  primitive, not full ⟨P⟩ derivation (per [GAUGE_ISOTROPY_FROM_CL3_PSEUDOSCALAR_THEOREM_NOTE_2026-05-04.md](GAUGE_ISOTROPY_FROM_CL3_PSEUDOSCALAR_THEOREM_NOTE_2026-05-04.md))

**Affected lines:** ~240-270 (best analytic candidate), ~488-525 (live status)

### 4. COMPLETE_PREDICTION_CHAIN_2026_04_15.md

**Current**: "<P> = 0.5934 remains the one COMPUTED input. It is computed
from the axiom by lattice MC, not imported from experiment."

**Proposed update**:
- ⟨P⟩ is now framework-native MC + L→∞ extrapolation matching standard
  SU(3) Wilson MC L→∞ within 0.2σ
- Add reference to PR #528 + companion isotropy theorem
- Update overall chain status from "bounded" to "proposed retained" per audit

**Affected lines:** ~33-36, ~493-495

## Priority 2 docs (infrastructure)

### 5. QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md

**Current**: status `bounded` (uses standard SM 2-loop RGE)

**Proposed update**:
- Note that the input `α_s(v)` is now framework-native via plaquette
  retained promotion (PR #528)
- The bridge itself remains standard SM infrastructure (Machacek-Vaughn);
  this is documented as imported with explicit scope
- Status remains `bounded` on running bridge scope (not framework-native
  derivation), but boundary value α_s(v) is now retained

### 6. PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md

**Current**: references plaquette as bounded, with SDP bootstrap as
analytic-closure path

**Proposed update**:
- Note that SDP bootstrap proof-of-concept built (PR #528)
- Numerical retained achieved via L→∞ extrapolation
- Analytic SDP bootstrap remains open (target ~2-3% bound, ongoing work)

## Priority 3 docs (just comparators, no weave needed)

The following 50+ docs reference 0.5934 only as comparator and don't need
explicit weave updates (the value is unchanged):

- DM lane (DM_*, DM_LEPTON_*)
- Higgs lane (HIGGS_*)
- Hadron lane (HADRON_*)
- CKM lane (CKM_*)
- Cosmology (HUBBLE_*)
- Various atlas/audit notes

These can pick up the retained status implicitly via their dependency
chains once Priority 1-2 are updated.

## Audit dependency

The companion weave PR (#529) DEPENDS on PR #528 audit ratification:
- If audit ratifies PR #528 as proposed → weave PR can be merged
- If audit modifies PR #528's scope → weave PR adapts accordingly
- If audit rejects PR #528 → weave PR is closed

The weave PR should clearly state this dependency in its description.

## Recommended workflow

1. **PR #528 (this PR)**: source PR establishing proposed retained
   - Already contains all evidence + isotropy theorem + audit submission
2. **PR #529 (companion weave)**: proposed downstream updates
   - Branch off PR #528 head
   - Updates 6 priority docs with status amendments
   - Marked as "depends on #528 audit"
   - Auditor reviews both together
3. **Path 2 (parallel)**: SDP bootstrap development for analytic retained
   - Independent track for tightening to ~2-3% analytic bound
   - When complete, separate analytic-retained submission

This 3-track approach allows audit promotion (numerical) and analytic
development (Nobel-quality) to proceed independently.
