# Paper Outline Review

**Date:** 2026-04-12  
**Status:** review authority for the current Nature-letter outline  
**Primary target:** `docs/PAPER_OUTLINE_2026-04-12.md`  
**Supporting docs checked:** `docs/PAPER_STRATEGY_2026-04-12.md`, `docs/FLAGSHIP_PAPER_CONTRIBUTION_STATEMENT_NOTE.md`, `docs/CI3_Z3_PUBLICATION_RETAIN_AUDIT_2026-04-12.md`

---

## Bottom line

The current outline is still too broad for the audited repo state.

The structural gauge backbone is now materially stronger than before:

- exact native `Cl(3)` / `SU(2)`
- graph-first weak-axis selector
- graph-first structural `su(3)` closure
- bounded left-handed `+1/3` / `-1` abelian charge matching

But the outline still promotes several review-only or scenario-dependent lanes as
if they were already retained closure:

- anomaly-complete hypercharge
- Weinberg-angle threshold correction
- neutrino fit outputs
- `y_t` closure
- EWPT / baryogenesis headline numbers
- dark matter / `Omega_Lambda` / cosmology chain
- diamond-NV and echo prediction stack

If submitted in its current form, a strong referee will correctly classify the
paper as an overclaim stack.

---

## P1 outline blockers

### 1. Abstract overstates the retained state

The abstract currently claims:

- zero free parameters
- full Standard Model gauge group with correct hypercharge assignments
- three generations
- a long list of cosmological and flavor numbers as if they were retained

That is not consistent with the current audit.

**Required fix:**

- Rewrite the abstract around the structural core only.
- Keep the abelian factor bounded as hypercharge-like / left-handed matched.
- Move all fit- or scenario-dependent numbers out of the abstract unless their
  underlying lanes are independently upgraded first.

### 2. Gauge section overstates hypercharge and misstates the generation boundary

The gauge section is close on `SU(2)` and structural `SU(3)`, but it still goes
too far in two places:

- it treats the traceless abelian factor as fully identified hypercharge
- it does not state the generation result on the right surface

The current audit does not support hypercharge at full strength, and it
requires the generation claim to be presented as part of the framework rather
than as something separately re-proved by the EWSB cascade.

**Required fix:**

- State the graph-first result as:
  - structural `su(3) \oplus u(1)` closure
  - bounded left-handed charge matching
- Move anomaly-complete hypercharge to an explicit open theorem.
- Present generations as closed in the framework.
- Do not use the EWSB cascade or CKM lane as the closure mechanism.

### 3. The centrepiece prediction table is not manuscript-safe

The current Table 1 mixes retained closure with fits, imported inputs, and
scenario-dependent outputs.

In particular, the following are still review-only or bounded:

- dark matter ratio
- `Omega_Lambda`
- `sin^2(theta_W)` threshold correction
- neutrino angles / `delta_CP` / mass-squared ratio
- top mass from `y_t`

This is the single biggest manuscript-structure problem after the abstract.

**Required fix:**

- Split the table into:
  - retained structural / benchmark results
  - bounded phenomenology / consistency windows
- Or remove the review-only rows from the Nature-letter main text entirely.

### 4. The prediction section still includes unfinished or review-only lanes

The falsifiable-predictions section currently includes:

- diamond NV
- Born-gravity cross-constraint
- no-GW-echo claim
- strong frozen-star language

These are not yet frozen at the same evidentiary level as the structural gauge
and gravity backbone.

**Required fix:**

- Remove these from the main prediction table unless their pipelines are frozen.
- If kept anywhere, keep them in SI or an explicit exploratory section.

### 5. The outline is internally inconsistent on the `SU(3)` state

Section 4 presents the graph-first `SU(3)` closure as done, but the discussion
still says the integration of the selector and commutant steps is ongoing.

That inconsistency alone signals that the outline is lagging the current review
state.

**Required fix:**

- Update the discussion to reflect the graph-first structural closure.
- Keep only the remaining bounded points: detailed flavor closure and the
  phenomenology/topology bridges.

---

## What still needs done for the full paper

If the goal is the fully expansive paper, the remaining work is now sharply
defined.

### Work package A. Generation hierarchy / flavor cleanup

The exact orbit algebra is real, and the generation claim should now be treated
as part of the framework.

What is still missing is narrower:

1. a first-principles `1+1+1` hierarchy rather than a bounded model
2. a clean explanation of the two singlets
3. a sharper route from the generation closure to CKM / flavor quantities

### Work package B. Topology / compactification

Need:

1. close the `S^3` cap-map / compactification step strongly enough to move the
   topology lane from bounded to structural
2. remove the remaining gap between the local shell-growth result and the full
   global compactification theorem

### Work package C. Phenomenology triage

The full paper can only carry phenomenology that is either:

- genuinely derived from the retained structure, or
- explicitly labeled as bounded phenomenology / consistency

This means each of the following still needs its own upgrade or downgrade:

- Weinberg angle
- neutrino sector
- `y_t`
- EWPT / baryogenesis
- dark matter ratio
- `Omega_Lambda` / cosmology chain

### Work package D. Experimental / strong-field cleanup

These lanes should not sit in the main narrative until their methods freeze:

- diamond-NV / Born-gravity experimental section
- GW echo claims
- frozen-star strong-field story

---

## Recommended manuscript shape now

If the full paper is still the target, the correct structure is:

1. A main claim surface built around:
   - gravity
   - Born rule
   - dimension selection
   - exact native `SU(2)`
   - graph-first structural `SU(3)`
2. A clearly bounded gauge statement:
   - abelian factor currently hypercharge-like / left-handed matched
   - anomaly-complete completion is closed only at the full-framework,
     one-generation level
3. A framework statement made explicit once:
   - the lattice is physical, not a regulator
   - within that framework, the `1+1+3+3` orbit structure is physical
     generation structure
4. A second-layer phenomenology section that is explicitly labeled by status:
   - retained
   - bounded phenomenology
   - exploratory / future test

That preserves the expansive ambition without lying about the current closure
state.

---

## Non-negotiable edits before submission

- Rewrite the abstract.
- Rewrite the gauge section to stop treating hypercharge as fully closed and to
  state the generation result on the explicit framework surface.
- Split or demote Table 1.
- Remove unfinished prediction lanes from the main claim surface.
- Make the discussion consistent with the graph-first `SU(3)` closure.

Until those edits are made, the outline is not submission-safe.
