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
  - a full backward historical sweep also shows no failure:
    - `59` tested checkpoints below `1232`, with `lowest_exact_limit = 192`
    - the only duplicate hazard was `variant_limit = 192`, where the sweep skipped a malformed `2026-03-22` log and fell back to the valid `2026-03-21` log
    - together with the widened and nearby ladders, no first failure appears anywhere in the full available historical `192 -> 5504` slice
  - a generated-family eligibility profile plus repaired canonical transfer check shows the law fails immediately on nearby `taper-wrap` ensembles:
    - the first non-pocket generated cohort already appears at `base:taper-wrap:default`, with `2` geometry rows (`geometry-c`, `geometry-e`), both `pair-only-sensitive`
    - after fixing the transfer checker to treat undefined support-edge metrics as zero-valued rather than skipping the row, the canonical `default/broader/wider` ladder gives `rows_total = 6`, `misclassified_total = 6`, `first_failure_ensemble = default`
    - all six failures are the repeated `geometry-c/e` rows, predicted as `add1-sensitive` by the fallback branch because their support metrics collapse to zero (`closure_load = 0`, `mid_anchor_closure_peak = 0`)
  - a direct generated-vs-historical comparer shows those failures are not just weak versions of the historical branch but a genuine support-collapse edge:
    - across `default`, `broader`, and `wider`, all `6` failing rows are still just `geometry-c/e`, and every current support/order-parameter observable is exactly zero (`support_load = 0`, `closure_load = 0`, `edge_identity_event_count = 0`, `edge_identity_support_edge_density = 0`)
    - the historical frozen bucket contains no `pair-only-sensitive` or `add1-sensitive` row with zero support activity:
      - historical `pair-only`: `support_load 7 -> 14`, `closure_load 38 -> 54`, `edge_identity_event_count 65 -> 89`
      - historical `add1`: `support_load 7 -> 16`, `closure_load 34 -> 64`, `edge_identity_event_count 54 -> 95`
    - so the first generated-family transfer break is best read as a support-collapse domain edge rather than an in-family continuation of the historical `pair-only-sensitive` mechanism
  - a minimal explicit domain guard isolates that edge cleanly:
    - guarding rows with `support_load = 0`, `closure_load = 0`, and `edge_identity_event_count = 0` moves all `6` canonical generated failures (`geometry-c/e` across `default/broader/wider`) into an out-of-domain bucket
    - no historical frozen-bucket row is guarded, and the historical `32/32` exact-close remains unchanged under the guarded projection
  - but the guard does not stabilize nearby generated transfer beyond that first edge:
    - on `base:taper-wrap`, the first non-guarded generated failure appears at `ultra` and repeats at `mega` as `mode-mix-f` (`pair-only-sensitive` actual, `add1-sensitive` predicted)
    - on neighboring `base:skew-wrap`, non-guarded generated failures already appear at `default` (`local-morph-c`) and broaden at `broader+` (`mode-mix-d`)
    - so support-collapse is only the first nearby generated-family boundary, not the whole transfer failure story
  - a direct comparer against the historical frozen `pair-only-sensitive` rows shows those surviving generated failures are not just a single shifted load or density branch:
    - the `skew-wrap` failures are over-supported and high-closure but sparse on support-edge density (`support_load = 20`, `closure_load = 63 -> 70`, `edge_identity_support_edge_density = 0.103 -> 0.140`)
    - the surviving `taper-wrap:mode-mix-f` failures are the opposite extreme (`support_load = 0`, `closure_load = 5`, `edge_identity_event_count = 10`, `edge_identity_support_edge_density = 0.500`)
    - so no single load, closure, or density threshold exact-separates all surviving generated failures from the historical frozen `pair-only-sensitive` branch
    - but all `11` surviving generated failures do exact-close into one compact anchor-balance band: `anchor_closure_intensity_gap` always stays between `-2.000` and `2.333` (empirically `0 -> 2`)
    - every historical frozen `pair-only-sensitive` row lies outside that band (`-9.667 -> -4.000` or `2.667 -> 6.000`)
    - projecting that same band onto the queued contrast cohorts keeps it exact against `add1` but reveals one small frozen `add4` pocket:
      - every frozen historical `add1-sensitive` row also stays outside the band (`anchor_closure_intensity_gap = -12.000 -> -2.667`)
      - only `2/8` frozen `add4-sensitive` rows enter the band (`base:taper-wrap:local-morph-ዦ`, `base:taper-wrap:local-morph-ᓭ`)
      - those in-band `add4` rows are otherwise inside the generated target ranges but sit at `mid_anchor_closure_peak = 12`, above the generated-failure maximum `8`
      - adding one compact in-band ceiling restores exact separation across all frozen historical cohorts: `anchor_closure_intensity_gap >= -2.000 and anchor_closure_intensity_gap <= 2.333 and mid_anchor_closure_peak <= 10.000`
      - under that refined clause the generated failures stay `11/11`, while frozen historical `pair-only-sensitive`, `add1-sensitive`, and `add4-sensitive` rows fall to `0/9`, `0/15`, and `0/8`
      - on a four-row focused comparison against representative `base:skew-wrap:local-morph-c` and `base:skew-wrap:mode-mix-d`, one compact support-layout observable already exact-separates the skew-wrap generated failures from the in-band `add4` pocket: `anchor_deep_share_gap >= 0.250`
      - physically, those skew-wrap generated failures carry a right/deep bridge shoulder (`anchor_deep_share_gap = 0.500`, `high_bridge_right_count = 1`) that the in-band `add4` rows lack (`0`, `0`), so the generated rows spread closure away from the mid anchor (`mid_anchor_closure_peak = 8`) while the frozen `add4` pocket traps it at `12`
      - on the same representative row set plus one representative `base:taper-wrap:mode-mix-f`, one compact low-support observable exact-separates `mode-mix-f` from both the skew-wrap shoulder and the in-band `add4` knot: `closure_load <= 24.500`
      - physically, `mode-mix-f` stays inside the anchor band by collapsing to a zero-support, low-closure floor (`support_load = 0`, `closure_load = 5`, `edge_identity_event_count = 10`) rather than by carrying the skew-wrap right/deep shoulder, so the refined band now has two generated realizations on the current bounded basis: a right/deep bridge shoulder and a nearly empty low-support throat, both distinct from the frozen `add4` mid-anchor knot
      - the bounded immediate generated basin (`taper-wrap`, `skew-wrap`, `taper-hard`, `skew-hard` through `mega`) contains no guard-surviving correctly classified comparison rows at all; every non-collapse row there is itself another transfer failure
      - one sparse outer generated guardrail slice over `rect-wrap`/`rect-hard` at `ultra` and `mega` adds no new refined-band generated row:
        - the only non-collapse outer failures are `base:rect-wrap:local-morph-f` at `ultra` and `mega`
        - both still sit on the base anchor-gap band boundary (`anchor_closure_intensity_gap = -2.000`) but fail the refined ceiling with `mid_anchor_closure_peak = 12.000`
        - a focused outer-rect comparison against the current shoulder/throat/knot representatives exact-separates the outer pair with one load observable: `closure_load >= 75.000`
        - physically, the outer guardrail still does not create a third generated realization inside the refined band; instead it marks a heavier knot-side continuation beyond the ceiling, sharing the frozen `add4` pocket's `mid_anchor_closure_peak = 12.000` and `anchor_deep_share_gap = 0.000` while retaining `high_bridge_right_count = 1.000` and much larger load (`support_load = 26.000`, `closure_load = 80.000`)
        - widening that same sparse rect guardrail one ensemble step to `wider|ultra|mega` still produces no beyond-ceiling non-collapse row outside the same `rect-wrap:local-morph-f` pair, so the present high-load continuation remains rect-local on that immediate bounded sparse slice
      - the next tested non-rect late guardrails also stay empty:
        - on the slightly wider `large` family at `ultra|mega`, the non-rect late slice (`taper-hard-large`, `taper-wrap-large`, `skew-wrap-large`) yields `scanned_nonrect_combinations = 6` and `first_nonrect_row = none`
	        - one tier later, that wider late slice still stays empty all the way through the tested deeper ladder: on `large` at `giga`, `tera`, `peta`, and `exa`, the same non-rect late slice yields `scanned_nonrect_combinations = 3` at each tier and `first_nonrect_row = none` at all four
        - on the differently placed `mirror` family at `ultra|mega`, the non-rect late slice (`skew-hard-mirror`, `skew-wrap-mirror`) yields `scanned_nonrect_combinations = 4` and `first_nonrect_row = none`
        - the mirrored late slice stays empty all the way through the tested deeper ladder: on `mirror` at `giga|tera`, the same non-rect late slice yields `scanned_nonrect_combinations = 4` and `first_nonrect_row = none`, and at `peta|exa` it yields `scanned_nonrect_combinations = 2` at each tier with `first_nonrect_row = none`
	      - but the more distant base late slice now shows a broader persistent non-rect beyond-ceiling branch:
	        - on the broader `base` `peta|exa` non-rect sweep, `nonrect_beyond_ceiling_rows = 3` and `high_load_hits = 3/3`
	        - the observed late non-rect beyond-ceiling rows are:
	          - `base:peta:base:taper-hard:local-morph-f`
	          - `base:exa:base:taper-hard:local-morph-f`
	          - `base:exa:base:skew-wrap:local-morph-k`
	        - the taper-hard member repeats unchanged across `peta|exa`: `support_load = 22.000`, `closure_load = 76.000`, `mid_anchor_closure_peak = 12.000`, `anchor_closure_intensity_gap = 4.000`, `anchor_deep_share_gap = 0.667`, `high_bridge_right_count = 2.000`
	        - the new skew-wrap member at `exa` still keeps the same high-load continuation while rotating the anchor geometry: `support_load = 21.000`, `closure_load = 84.000`, `mid_anchor_closure_peak = 12.000`, `anchor_closure_intensity_gap = -2.000`, `anchor_deep_share_gap = -0.667`, `high_bridge_right_count = 0.000`
	        - a direct row-level compare against the current shoulder/throat/knot representatives exact-separates the whole observed late branch with one tighter load cut: `closure_load >= 73.000`
	        - inside the observed late branch, the three realized forms each exact-separate with one feature:
	          - outer-rect tail: `support_load >= 24.000`
	          - taper-hard branch: `anchor_closure_intensity_gap >= 3.000`
	          - skew-wrap branch: `anchor_deep_share_gap <= -0.334`
	        - so `closure_load >= 75.000` still survives on the whole observed late non-rect branch, but the sharper current read is that it is one shared late high-load continuation with three distinct support-layout realizations rather than one undifferentiated tail
	      - on the already finished non-base late guardrails, there is still no broader-family transfer evidence for that branch:
	        - across `large` through `exa` and `mirror` through `exa`, the finished first-hit probes cover `30` non-rect combinations total and every one of those guardrails still reports `first_nonrect_row = none`
	        - the benchmark inventory itself now closes that current non-base frontier: outside `base`, the only available packs are `large` and `mirror`, the current late frontier only runs through `exa`, and all `12` non-base pack/ensemble pairs on `ultra..exa` are already covered with zero hits
	        - a bounded helper-validation detour now hardens that wall rather than changing it:
	          - the shared generated-family helper seam was real: non-base `build_rows_with_trees(...)` calls were still routing `_evaluate_extended_ge6_dpadj_nodes(...)` through `pack_name="base"`
	          - after threading the true pack name through that helper, all nine finished non-base first-hit probes reran with the same scanned-combination counts and still `first_nonrect_row = none`
	          - the helper-fixed `large:exa` exhausted-slice compare, full exhausted-wall mid-anchor translation compare, and full packet-neighborhood compare also match their earlier outputs in substance, so the present empty non-base wall does not depend on the stale helper path
	        - a direct exhausted-slice compare now shows what that empty wall is hiding:
	          - the nearest `large:exa` miss, `large:taper-wrap-large:local-morph-g`, already clears the observed late branch load floors (`support_load = 26.000`, `closure_load = 87.000`) but stalls at `mid_anchor_closure_peak = 8.000`, exactly `4` below the late-branch value `12.000`
	          - the nearest `mirror:exa` miss, `mirror:skew-hard-mirror:local-morph-f`, also stalls at `mid_anchor_closure_peak = 8.000` while remaining below the late load floor (`support_load = 17.000`, `closure_load = 59.000`)
	          - comparing the five observed base late rows against those two nearest exhausted-wall misses exact-separates with one scalar clause: `mid_anchor_closure_peak >= 10.000`
	          - a tighter row-level compare against the closest `large:exa` miss shows that the miss is not short on absolute bridge-bridge closure scale:
	            - the late `rect-wrap` and `taper-hard` rows realize `mid_candidate_bridge_bridge_closed_pair_max = 12.000`
	            - the `large` miss also realizes a `12.000` bridge-bridge closed-pair maximum, but on the left anchor band instead: `left_candidate_bridge_bridge_closed_pair_max = 12.000`, `mid_candidate_bridge_bridge_closed_pair_max = 8.000`
	            - with the richer packet metric set, the focused structural separator is the attached-packet lift: `delta_mid_left_attached_max >= 0.000`, where `delta = mid - left`
	          - widening that packet compare to the full exhausted wall gives one cleaner structural separator still:
	            - every observed late row has `mid_candidate_attached_max = 8.000`
	            - both exhausted-wall misses stop at `mid_candidate_attached_max = 7.000`
	            - `mid_candidate_attached_max >= 7.500` exact-separates the whole observed late branch from the whole exhausted wall
	            - the corresponding mid-anchor bridge-bridge closed-pair maxima remain `12.000` on the late side and `8.000` on the exhausted-wall side
		          - the neutral-balance pair sharpens that wall further:
		            - the late `base:exa:base:skew-wrap:local-morph-k` row and the `mirror:exa` miss keep the same coarse layout: `high_bridge_left/mid/right = 2/1/0`, `left_candidate_count = 2`, `mid_candidate_count = 3`
		            - they also keep the same dense-count profile (`left_candidate_dense_count = 2`, `mid_candidate_dense_count = 2`) and the same mid closed-ratio ceiling (`mid_candidate_closed_ratio_max = 0.500`)
		            - so the `12.000 -> 8.000` drop is not another band-placement or density change; the late row upgrades the dominant left/mid packet from `7` attached bridges and `8` bridge-bridge closed pairs to `8` attached bridges and `12` bridge-bridge closed pairs
		          - a direct packet-neighborhood compare now localizes that lift:
		            - the dominant late mid packet is the same full eight-support octagon across all five observed late rows
		            - both exhausted-wall misses share the same seven-support depleted mid template
		            - every observed late row completes that exhausted template in the same way:
		              - add the inward left-flank support node at relative `(-1, 0)`
		              - restore the four incident bridge-bridge support closures
		            - a follow-on topology translation compresses that coordinate description into one local hinge law:
		              - the inserted support is a four-incident flank hinge
		              - it touches two same-column neighbors and two inward neighbors
		              - so the late branch repairs the exhausted wall by restoring one local vertical flank ladder plus two inward bridge-bridge closures into the packet interior
		            - the closest `large` miss still keeps the full octagon on the left anchor band, while the `mirror` miss also leaves its strongest left packet one support short
		            - so the whole current late-vs-exhausted transfer reduces locally to one node-and-four-edge mid-packet completion, not another layout change
	        - so outside the observed `base` `peta|exa` slice, the current late-branch law still has no non-base counterexample, but the sharper transfer read is now that the present non-base generator family ceilings at `mid_anchor_closure_peak = 8.000` because it never lifts `mid_candidate_attached_max` above `7.000`, and with that leaves the corresponding mid-anchor bridge-bridge closure maximum at `8.000` instead of `12.000`
	    - so the post-guard transfer break is now best read as a second nearby domain boundary: a moderate anchor-balance regime with one high-mid-anchor frozen `add4` pocket plus two generated realizations inside the refined band, a skew-wrap right/deep shoulder and a `mode-mix-f` low-support throat, while the sparse outer `rect-wrap` failures and the broader distant `base` late branch form a heavier beyond-ceiling continuation beyond that refined ceiling; the exhausted `large`/`mirror` wall now sharpens that farther continuation by showing that the nearest non-base misses can imitate or even exceed the late branch on gross load, but still fail to fill the same inward left-flank support node that turns the dominant mid packet from `7/8` into `8/12`

The open problem in this basin is no longer whether the family structure exists, whether the frozen bucket exact-closes, why `mode-mix-f` sits inside the anchor band, whether the outer `rect-wrap:local-morph-f` pair is the same mechanism as the frozen `add4` pocket, or whether any non-rect late guardrail ever broadens that outer continuation. The zero-support collapse edge is already isolated, the later moderate anchor-balance band plus `mid_anchor_closure_peak <= 10.000` ceiling still reduces to a skew-wrap right/deep bridge shoulder, a `mode-mix-f` low-support throat, and a frozen `add4` mid-anchor knot, and the `rect-wrap/rect-hard` guardrail still resolves into a heavier beyond-ceiling continuation under `closure_load >= 75.000`; now the broader `base` `peta|exa` non-rect sweep also participates, and the direct compare shows that the current observed late branch exact-separates from the earlier shoulder/throat/knot representatives under `closure_load >= 73.000` while splitting internally into an outer-rect load tail, a positive-intensity taper-hard branch, and a negative-deep skew-wrap branch. The helper-validation detour closed the strongest integrity seam without moving the science: after fixing the stale non-base pack routing inside the shared generated-family helper, the finished `large`/`mirror` first-hit guardrails, exhausted-slice compare, full exhausted-wall translation compare, and packet-neighborhood compare all survive unchanged in substance. Finished non-base late guardrails therefore still contribute no candidate row at all, but the exhausted `large:exa` and `mirror:exa` wall now shows that the missing ingredient is not gross load alone: the nearest non-base misses stall at `mid_anchor_closure_peak = 8.000`, while every observed late-branch row sits at `12.000`, and `mid_anchor_closure_peak >= 10.000` already exact-separates the observed late branch from those nearest exhausted-wall misses. The tighter row-level translation is sharper still: the closest `large` miss already carries the same `12.000` bridge-bridge closure maximum as the late branch, but it is parked on the left anchor band instead of the mid anchor band, and the richer packet metric shows that this focused split is already captured by `delta_mid_left_attached_max >= 0.000`. Once the compare is widened to the whole exhausted wall, the stable structural separator gets cleaner rather than more complex: `mid_candidate_attached_max >= 7.500`, with every observed late row at `8.000` and both exhausted-wall misses at `7.000`. The packet-neighborhood compare now makes the local mechanism explicit across the whole observed late branch: both exhausted-wall mid packets share the same seven-support template, every observed late row completes it by adding the inward left-flank support node at relative `(-1, 0)` plus its four incident bridge-bridge support closures, and the new topology translation compresses that further into one four-incident flank hinge that reconnects the local vertical flank ladder to the packet interior. A bounded adjacent-row confirmation pass now settles the wording choice: on the discovery wall plus a named nearby generated holdout, `mid_anchor_closure_peak >= 10.000`, `mid_candidate_bridge_bridge_closed_pair_max >= 10.000`, `mid_candidate_attached_max >= 7.500`, and the four-incident flank hinge are all equivalent. They all still reject the exhausted wall, and they all already light up the held-out `outer-rect` pair at `ultra|mega`. So the packet-lift / hinge language is real, but it is the common coarse law of the broader beyond-ceiling continuation rather than a unique marker of the late non-rect branch by itself. One bounded within-family compare now closes the active subbranch separator on the present five-row basis: the held-out `outer-rect` pair and the later `taper-hard` / `skew-wrap` rows all keep the same `8/12` packet and four-incident flank hinge, so packet completion itself is no longer the splitter. Above that shared law, the branch coordinates exact-close with one feature each on the current basis: the `outer-rect` pair keeps one low right bridge and also exact-separates under `support_load >= 24.000`; the `taper-hard` pair exact-separates by two right bridges (`high_bridge_right_count >= 1.500`), with the weaker within-family shadow `anchor_closure_intensity_gap >= 1.000`; and the remaining `skew-wrap` row exact-separates by negative deep share (`anchor_deep_share_gap <= -0.334`, equivalently no right bridge). A paired wider-base guardrail now sharpens that read rather than reopening it: both `wider:base:skew-wrap:local-morph-c` and `wider:base:skew-wrap:mode-mix-d` fall back to the depleted `7/8` packet at `mid_anchor_closure_peak = 8.000`, `mid_candidate_attached_max = 7.000`, `mid_candidate_bridge_bridge_closed_pair_max = 8.000`, and no four-incident flank hinge. So neither nearest wider base shoulder adds a fourth shared-packet subbranch. A bounded log-backed closure then rewrites the taper-hard residual more physically on the seven-row control set made of those five shared-packet rows plus both wider shoulders: the shared packet gate still exact-isolates the family, but within it the taper-hard pair exact-separates not only by `anchor_closure_intensity_gap >= 1.000` but also by the cleaner `high_bridge_right_count >= 1.500`. The crucial difference is that the two-right-bridge clause already stays exact on both wider shoulders without needing the packet gate, while the positive-intensity clause still leaks there. So the present beyond-ceiling continuation is best read as one shared packet regime already split into `outer-rect`, `taper-hard`, and `skew-wrap` subbranches, with taper-hard specifically forming the two-right-bridge arm of that regime rather than merely a positive-intensity branch. A finished-log audit now closes the current already-computed outside-family boundary as well: across the exhausted-wall misses, low-support throats, nearby shoulders, and paired wider sentinels, no row hits any shared packet law and none reaches `high_bridge_right_count >= 1.500`, while the helper-fixed non-base first-hit guardrails still report `first_nonrect_row=none`. So the only logged two-right-bridge rows remain the known `base` `peta|exa` taper-hard pair inside the current five-row shared-packet family. A first fresh beyond-boundary base control now says the same packet depletion persists one step farther: `ultra:base:skew-wrap:local-morph-c` again misses all four shared packet laws, stalls at `mid_anchor_closure_peak = 8.000`, `mid_candidate_attached_max = 7.000`, `mid_candidate_bridge_bridge_closed_pair_max = 8.000`, and no four-incident flank hinge, and stays below the cleaner taper-hard clause with only one right bridge. So the current three-way shared-packet split still does not widen at the first checked `ultra` shoulder either.

## Current Regime Architecture

The current low-overlap map is:

- Historical exact law: the branch-aware frozen `rc0|ml0|c2` law exact-closes the historical ladder from `192` through `5504`. This is the in-domain historical classifier.
- Support-collapse out-of-domain guard: the first nearby generated failures (`geometry-c/e`) are zero-support collapse rows, so they are best treated as a domain guard rather than as an extension of the historical `pair-only-sensitive` mechanism.
- Moderate anchor-balance basin: after that guard, the surviving nearby generated `pair-only-sensitive` failures sit in a refined anchor-balance regime with `mid_anchor_closure_peak <= 10.000`. That basin currently reduces to a right/deep skew-wrap shoulder, a low-support `mode-mix-f` throat, and the frozen mid-anchor `add4` knot.
- Beyond-ceiling continuation: above that ceiling, the stable coarse law is the shared `8/12` mid-packet lift. On the bounded confirmation set, `mid_anchor_closure_peak >= 10.000`, `mid_candidate_bridge_bridge_closed_pair_max >= 10.000`, `mid_candidate_attached_max >= 7.500`, and the four-incident flank hinge are all equivalent. This broader continuation already includes the held-out `outer-rect` pair at `ultra|mega` as well as the later `base` `peta|exa` non-rect rows, and on the current five-row basis it already splits cleanly into an `outer-rect` low-right-bridge tail, a `taper-hard` two-right-bridge branch, and a `skew-wrap` negative-deep no-right-bridge branch. The paired wider base sentinels `wider:base:skew-wrap:local-morph-c` and `wider:base:skew-wrap:mode-mix-d` both fall back to the depleted `7/8` packet with no flank hinge, so the current three-way split does not widen immediately into a fourth shared-packet subbranch. A follow-on log-backed closure sharpens the taper-hard wording: the positive-intensity clause still needs the shared packet gate to stay exact, but the more physical two-right-bridge clause `high_bridge_right_count >= 1.500` already stays exact even on those wider controls, so taper-hard is now best read as the two-right-bridge arm of the shared packet regime. A finished-log audit closes the current already-computed outside-family boundary too: the exhausted-wall misses, low-support throats, nearby shoulders, and paired wider sentinels all miss the shared packet laws and stay below two right bridges, while the helper-fixed non-base first-hit frontier remains empty. A first farther `ultra:base:skew-wrap:local-morph-c` guardrail still repeats that depleted `7/8` packet with no flank hinge and only one right bridge, so the no-fourth-branch read survives one checked step beyond the finished wider pair.
- Current domain boundaries: the non-base `large`/`mirror` wall still stays empty through `exa`, and the nearest misses stall at the depleted `7/8` mid packet with no flank hinge. So the current evidence supports a base-local beyond-ceiling continuation separated from a non-base exhausted wall.

## Active Technical Problem

The main active technical problem is projecting and translating the exact low-overlap law beyond the full available historical `192 -> 5504` frontier ladder.

The relevant questions are:

- whether the observed `base` late non-rect branch on `peta|exa` is already complete at the current three-row set or still missing more beyond-ceiling members on deeper base sweeps
- whether any wider/deeper base sentinel beyond the checked shoulders `wider:base:skew-wrap:local-morph-c`, `wider:base:skew-wrap:mode-mix-d`, and `ultra:base:skew-wrap:local-morph-c` ever rejoins the shared `8/12` packet regime, or whether the current three-way beyond-ceiling split is already the whole immediate shared-packet family
- whether any nearby non-base generated family can realize the same `8/12` packet lift / four-incident flank hinge and thereby break the current empty exhausted wall
- whether any genuinely new deeper base or nearby non-base control beyond the current finished-log boundary ever rejoins the shared packet regime with `high_bridge_right_count >= 1.500`, or whether taper-hard is already the whole current two-right-bridge arm
- how the exact branch-aware law should be physically interpreted at both the zero-support collapse boundary and the new anchor-balance basin split between right/deep bridge shoulder, low-support throat, frozen mid-anchor knot, and the heavier beyond-ceiling continuation
- whether the present shoulder/throat/knot translation can be expressed more cleanly in support-layout or topological language
- which parts of the present explanation are stable structure and which depend on the current observable basis

## What Is Still Unresolved

The main unresolved points are:

- the spent-delay action family is favored in the benchmark, but not derived from deeper first principles
- low-overlap subtype competition is now much more compressed on the frozen `5504` bucket and exact across the available historical frontier ladder; the first nearby generated edge (`geometry-c/e`) isolates cleanly under a support-collapse guard, and the surviving non-guarded generated pair-only failures (`mode-mix-f`, `local-morph-c`, `mode-mix-d`) now exact-separate from frozen historical `pair-only-sensitive`, `add1-sensitive`, and `add4-sensitive` rows once the moderate anchor-balance band is tightened with `mid_anchor_closure_peak <= 10.000`. Above that ceiling, the current coarse continuation is now cleaner: the held-out `outer-rect` pair at `ultra|mega` shares the same `8/12` mid-packet lift and four-incident flank hinge as the five observed late rows, so the packet-completion law should now be read as the common beyond-ceiling mechanism rather than as a late-only signature. The bounded within-family compare closes the immediate separator on the present basis: the shared packet family already splits into an `outer-rect` low-right-bridge tail, a `taper-hard` two-right-bridge branch, and a `skew-wrap` negative-deep no-right-bridge branch. A paired wider-base guardrail now says the immediate answer is still no fourth shared-packet branch: both `wider:base:skew-wrap:local-morph-c` and `wider:base:skew-wrap:mode-mix-d` drop back to `mid_anchor_closure_peak = 8.000`, `mid_candidate_attached_max = 7.000`, and no flank hinge. A follow-on log-backed closure then sharpens the taper-hard branch itself: the positive-intensity clause still leaks on both wider shoulders unless the shared packet gate is written explicitly, but the cleaner physical clause `high_bridge_right_count >= 1.500` already stays exact across the whole seven-row control set. So the present beyond-ceiling split is now best read as one shared packet regime whose taper-hard arm is specifically the two-right-bridge branch. A finished-log audit then closes the current already-computed outside-family boundary: the exhausted-wall misses, low-support throats, nearby shoulders, and paired wider sentinels all miss the shared packet laws and stay below two right bridges, while the helper-fixed non-base first-hit frontier remains empty. A first fresh beyond-boundary guardrail now says the depletion persists one step farther too: `ultra:base:skew-wrap:local-morph-c` again misses every shared packet law, stays at one right bridge, and still leaks only the weaker intensity clause. What remains unresolved is no longer the finished exhausted-wall or nearby-generated tables themselves, but whether the companion `ultra` shoulder or still deeper base / nearby non-base controls beyond the current boundary ever realize the same packet completion.
- the present mechanism language is more geometric and topological than it was earlier, but it is not yet a clean bridge to standard continuum physics
- the strongest fine-grained mechanism results are exact on the available historical frontier ladder, but not yet a general theorem over nearby generated families because nearby generated transfer still shows in-domain failures after the empirical support-collapse guard is applied

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
