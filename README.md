# Discrete Event-Network Toy Model

This repository is an attempt to build a toy physics model while stripping away as much human observational bias as possible from the starting assumptions.

The motivating question is:

> If we do **not** start by assuming smooth space, continuous time, point particles, or measurement as primitive, how much physics-like structure can still be recovered from a much smaller event-and-relation ontology?

## Why This Project Exists

Most physical theories are written in a language that is already heavily shaped by human perception:

- we naturally think in terms of objects moving in space
- we picture time as a universal flowing background
- we often treat geometry as given before anything happens inside it
- we describe measurement using concepts that already assume observers, apparatus, and stable classical records

This project started by trying to remove some of that built-in bias.

So instead of beginning with particles in a pre-existing spacetime, the toy begins with a much thinner picture:

- discrete events
- local influence links between events
- persistence
- compatibility
- durable records

From there, the question is whether anything recognizably physics-like can emerge:

- effective geometry
- causal order
- inertial continuation
- gravity-like path bending
- measurement-like suppression of alternatives

## Core Axioms

These are the conceptual axioms the toy is built around.

1. **Reality is an evolving network of events and influence relations.**  
   The primitive layer is not particles in a container. It is a changing relational graph of events and allowed local influences.

2. **Stable objects are persistent self-maintaining patterns in that network.**  
   What looks object-like at larger scales is modeled as a pattern that keeps reproducing its own local structure over time.

3. **Space is inferred, not assumed.**  
   Spatial structure is reconstructed from influence neighborhoods and signal-delay structure rather than taken as fundamental.

4. **Duration is local update count, not universal background time.**  
   Time is treated as something measured along histories and persistent patterns, not as a globally imposed external clock.

5. **The arrow of time is tied to durable record formation.**  
   Time-asymmetry is connected to the growth of persistent, non-erasable records rather than inserted as a separate metaphysical primitive.

6. **Free systems follow the locally simplest admissible continuation.**  
   In the absence of strong disturbances, the system prefers locally coherent continuations rather than arbitrary jumps.

7. **Inertia is undisturbed natural continuation.**  
   What looks like inertial motion is the toy version of persistence of local continuation when nothing distorts the surrounding continuation structure.

8. **Gravity is natural continuation in a distorted continuation structure.**  
   Gravity-like behavior is modeled not as a force added by hand, but as path selection through a locally altered delay/load landscape.

9. **Measurement is durable record formation that separates alternatives.**  
   Alternatives may coexist or combine when no durable record separates them; once a durable record forms, those alternatives are no longer treated the same way.

10. **Observed large-scale structure should be explained by persistent local mechanisms wherever possible.**  
    If a geometry-like or measurement-like effect appears, the preferred explanation is that it emerged from local network structure rather than being imposed from outside.

## What The Toy Actually Is

The implemented model uses:

- events as nodes
- directed local influence links
- delay-like and compatibility-like quantities on those links
- persistent patterns that act as local sources of structure
- admissible histories through the resulting network
- path-selection rules defined on the continuation landscape
- durable-record sectors in interference-style toy setups

In this formulation, geometry-like behavior is associated with the continuation structure induced by persistence and delay, rather than with a fixed background geometry.

## Analysis Program

The analysis layer measures:

- geometry and profile observables
- boundary roughness and cavity structure
- degree and neighborhood structure
- local bridge/support topology
- overlap, suppressor, and transfer behavior

These observables are used to compare mechanisms across benchmark scenarios, generated families, perturbation ensembles, and frozen-frontier subsets.

The current analysis path has been hardened against:

- benchmark/reporting mismatches
- stale helper logic
- duplicated selectors
- duplicated rule evaluators
- transfer scripts using slightly different input slices
- feature helpers that were silently double-counting

The current mechanism claims are based on that corrected analysis layer.

## Current Results

The model presently supports the following claims.

### 1. Effective delay structure

Persistent patterns can generate a local delay field in the toy. Histories evaluated against that field do not behave as if they were propagating on an undistorted fixed background.

### 2. Gravity-like continuation

Path selection through the derived delay field produces inward-bending, gravity-like continuation on the benchmark suite. This is a toy mechanism result, not a derivation of general relativity.

### 3. Record-based interference suppression

Alternatives can coexist when no durable record separates them, and durable-record sectors suppress that coexistence in the slit-style interference toy.

### 4. Stable mechanism families

The broadest recurring split is:

- `compact`, with a cleaner threshold-core structure
- `extended`, with more permissive and fallback-heavy behavior

This split persists across reruns and generated families.

### 5. Family growth without comparable family proliferation

As generated families widened:

- membership kept growing
- the number of main mechanism families changed much more slowly

The resulting picture is a stable mechanism map with expanding support, rather than continual creation of new families at each deeper frontier.

### 6. Shared structure in the low-overlap basin

Fine-grained mechanism work is currently concentrated on a fixed frontier snapshot at `variant_limit = 5504`. On that controlled sample:

- the hardest low-overlap center-spine `00` core has an exact closure family with a broad rescue side and a tighter, more local baseline cut
- the low-overlap support-family map transfers across the three main low-overlap branches:
  - `add1-sensitive`
  - `add4-sensitive`
  - `pair-only-sensitive`
- the dominant shared bucket already shows interpretable subtype drift:
  - `add1`: left-dominant, higher-support branch
  - `add4`: mid-dominant, more internally closed branch
  - `pair-only`: lower-support, more open-support branch
- the outside-gate residual for `pair-only-sensitive` now exact-closes under a branch-aware second pass:
  - baseline low-closure pocket: `closure_load <= 46.500`
  - spillover carve-out: `mid_anchor_closure_peak <= 0 and high_bridge_right_count <= 0`
  - recovered right-low side branch: `high_bridge_right_low_count >= 1 and support_load <= 14.500 and mid_anchor_closure_peak <= 1`
  - combined outside-gate result: `26/26` for `pair-only-sensitive` (`6/0/0`)
- projected back onto the full frozen bucket, the combined law now exact-closes every `pair-only-sensitive` row with no leakage:
  - high-closure gated branch: `3/3`
  - outside-gate branch-aware branch: `6/6`
  - full-bucket `pair-only-sensitive` result: `9/9` with `0` false positives
- the remaining unmatched residue is now much narrower:
  - `20` rows total
  - exactly `15 add1-sensitive` plus `5 outside-gate add4-sensitive`
  - the cleanest zero-false-positive residual `add4` clause is `anchor_closure_intensity_gap >= -6.500 and mid_anchor_closure_peak >= 9.000`, which captures `3/5`
  - the stubborn high-mid four-row knot (`local-morph-а`, `local-morph-༸` vs `local-morph-छ`, `local-morph-గ`) exact-closes in a slightly richer transfer basis with `edge_identity_event_count <= 78.000` (`2/2` add4, `0` false positives inside that cluster)
  - one bounded two-clause follow-on keeps that knot exactness and improves full-residual `add4` precision without recall loss:
    - `edge_identity_event_count <= 78.000 and edge_identity_support_edge_density >= 0.166667` (exact threshold `1/6`, rounded as `0.167` in earlier logs)
    - full residual result: `5/5` add4 recovered, `8` add1 false positives (precision `0.385`, baseline seed precision `0.312`)
  - a direct branch combiner with the earlier zero-false-positive residual clause does not improve on that branch:
    - `anchor_closure_intensity_gap >= -6.500 and mid_anchor_closure_peak >= 9.000` is a strict subset of the density-qualified branch
    - the combined `A or B` law is identical to branch `A`
  - one bounded branch-A leakage carve closes most remaining leakage without recall loss:
    - `edge_identity_event_count <= 78.000 and edge_identity_support_edge_density >= 0.166667 and mid_anchor_closure_peak >= 1.000`
    - full residual result: `5/5` add4 recovered, `1` add1 false positive (precision `0.833`, recall `1.000`)
    - the remaining overlap is concentrated in `base:taper-wrap:local-morph-͋`
  - the final overlap exact-closes under one bounded exclusion inside that branch:
    - exclude `closure_load <= 50.500 and edge_identity_support_edge_density <= 0.182`
    - refined outside-gate `add4` result: `5/5` with `0` false positives
  - projected together with the earlier high-closure and `pair-only` branches, the full frozen `rc0|ml0|c2` bucket now exact-closes:
    - high-closure `add4`: `3`
    - outside-gate `add4`: `5`
    - `pair-only`: `9`
    - default `add1`: `15`
    - full-bucket result: `32/32`, `0` misclassifications, `0` ambiguity
  - the exact branch-aware law also transfers unchanged across the nearby frontier ladder we tested:
    - `variant_limit = 4112`: `25/25`, `0` misclassifications
    - `variant_limit = 4992`: `28/28`, `0` misclassifications
    - `variant_limit = 5504`: `32/32`, `0` misclassifications
    - no first failure appeared within the tested `4112 -> 5504` slice
  - a widened frontier sweep still shows no failure:
    - `variant_limit = 1232`: `10/10`, `0` misclassifications
    - `variant_limit = 1488`: `12/12`, `0` misclassifications
    - `variant_limit = 3344`: `20/20`, `0` misclassifications
    - together with the later limits, no first failure appears anywhere in the tested `1232 -> 5504` slice

The open problem in this basin is no longer whether the family structure exists, whether the frozen bucket exact-closes, or whether the law survives on the nearby frontier ladder. It is how far that law transfers beyond the tested `1232 -> 5504` slice and how to express it in cleaner physical language.

## Active Technical Problem

The main active technical problem is widening and translating the exact low-overlap law beyond the tested `1232 -> 5504` frontier ladder.

The relevant questions are:

- whether the exact branch-aware law survives on wider fronts beyond the tested `1232 -> 5504` slice or on nearby generated-family ensembles
- whether that competition can be expressed more cleanly in support-layout or topological language
- which parts of the present explanation are stable structure and which depend on the current observable basis

## What Is Still Unresolved

The main unresolved points are:

- the spent-delay action family is favored in the benchmark, but not derived from deeper first principles
- low-overlap subtype competition is now much more compressed on the frozen `5504` bucket, but not yet a single minimal law that is proven stable on wider fronts
- the present mechanism language is more geometric and topological than it was earlier, but it is not yet a clean bridge to standard continuum physics
- the strongest fine-grained mechanism results are on a frozen frontier snapshot, not yet a general theorem over every wider generated family

## What Is Still Cheating

This is the explicit "do not flatter ourselves" block.

1. **The benchmark geometries are still partly hand-authored.**  
   The project now has procedural and randomized families, but the core benchmark worlds are still chosen by hand.

2. **The gravity-like classical limit is still assumed rather than derived.**  
   The spent-delay-style accounting rule is still selected because it works best in the current toy benchmark, not because it has been forced out of deeper dynamics.

3. **The delay field chooser is still hand-chosen.**  
   The delay field is derived from persistent patterns, but the rule family and locality preferences used to choose among candidate patterns are still designed rather than derived.

4. **Winner-level robustness still depends on hand-chosen criteria.**  
   Center gap, arrival span, selector policy, and the choice of combined status observable can still change which surviving branch wins on the same candidate pool.  
   Family-level structure is more stable than exact winner identity.

5. **The perturbation ensembles are still modest and structured.**  
   They are broader than they were early on, but they are still first-pass ensembles rather than exhaustive robustness studies.

6. **Weight robustness is still tested in a narrow high-end band.**  
   The current checks concentrate near the spent-delay end of the retained-weight family rather than exploring the whole space evenly.

7. **The random perturbation ensembles are still small and seeded.**  
   They are useful probes, but not yet large-scale random-graph studies.

8. **The geometry-randomization layer is still narrow.**  
   It currently jitters existing graph families rather than exploring a broad random geometry generator.

9. **The procedural graph generator is still small and structured.**  
   It is a useful independent-family probe, not a broad generator of arbitrary graph worlds.

10. **The sweep budgets are still hand-chosen runtime compromises.**  
    Smaller graphs, reduced rule families, and shorter persistence windows still trade completeness for tractability.

11. **Complex amplitudes are still assumed rather than derived.**  
    The toy has a measurement-like story, but not a derivation of the full complex-amplitude machinery.

12. **The strongest current hard-core mechanism results are still frozen-snapshot results.**  
    They may generalize, and some parts already transfer well, but the finest-grained structure is still being studied on a controlled frozen frontier.

13. **The project is still much stronger as toy mechanism science than as a bridge to known physics.**  
    The internal map is real enough to be interesting; the translation to standard physical law is still unfinished.

## Where The Detailed History Lives

This README is intentionally not the full research diary.

If you want the detailed chronology, active work queue, and worker handoff state, use:

- [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
- [physics_autopilot_handoff.md](/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md)
- [memory.md](/Users/jonreilly/.codex/automations/physics-autopilot/memory.md)
