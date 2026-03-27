# Discrete Event-Network Toy Model

This repository contains a runnable toy model built around one simple idea:

physics-like behavior might be recoverable from a discrete network of local events and influence links, without assuming smooth spacetime as the starting point.

`Octopus physics` is just a project nickname. The actual claims in this repository are about the toy model implemented here.

## README Map

This README is now story-first.

- `Short Version` is for a mixed audience.
- `Lay Version` explains the project without assuming much physics background.
- `Technical Version` explains what the code actually does and what the strongest current results are.
- `Current Limits` is the honest list of what is still unresolved.
- [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md) is the detailed chronological ledger.

## Short Version

The project starts from a few simple axioms:

- reality is represented as a network of discrete events and local influence links
- stable objects are persistent patterns in that network
- geometry is inferred from local delay/load structure rather than assumed first
- measurement-like behavior comes from durable record formation

From those ideas, the code builds a small toy world in which:

- a delay field can emerge from stable local patterns
- causal order can be inferred from that delay field
- path selection can produce gravity-like bending
- record formation can suppress interference
- different local geometry classes produce different mechanism families

The strongest current mechanism story is:

- `compact` behavior has a relatively clean threshold-core structure
- `extended` behavior is more permissive and has fallback structure
- late frontier growth is mostly adding more members of known families, not inventing new families
- the real unresolved work is now in the latent/topological structure of a small frozen hard core, not in pushing the frontier ladder forever

So the current project is best understood as:

- a well-audited, mechanism-rich toy model
- with real internal structure
- that is not yet a finished bridge to known physical laws

## Lay Version

### The basic idea

Instead of starting with particles moving around inside a pre-existing space, this toy starts with a network:

- nodes are events
- links are allowed local influences
- each link carries a delay and a compatibility-like weight

If that network develops stable repeating patterns, those patterns can act like the toy version of matter or structure. They change the local delay/load landscape, which in turn changes what routes or histories are easiest for the system to follow.

That is the core intuition behind the project:

- stable patterns distort continuation
- distorted continuation looks like effective geometry
- geometry-like effects can appear without being put in by hand first

### What the toy has actually shown

So far, the model has done a few nontrivial things:

- it can recover gravity-like path bending from a locally generated delay field
- it can produce measurement-like interference loss when alternatives are separated by durable records
- it shows a stable split between two mechanism families, called `compact` and `extended`

That compact/extended split matters because it means the toy is not just generating random behaviors. It has repeatable internal structure.

### What the long benchmark work taught us

For a long time, we kept widening generated families and rerunning mechanism checks. That was useful at first, because it showed the main mechanism map was not a shallow artifact.

But eventually the pattern changed:

- the number of example rows kept growing
- the number of mechanism families mostly stopped growing

That means the interesting scientific object is no longer the raw frontier size. It is the family structure underneath it.

In plainer terms:

- we are not mainly discovering new kinds of behavior now
- we are mostly finding more examples of the same kinds of behavior

That is why the project has shifted from “keep pushing the ladder” to “find the hidden structural rule.”

### Why the current frozen `5504` case matters

The repository now focuses a lot of mechanism archaeology on a frozen frontier snapshot at `variant_limit = 5504`.

That is not because `5504` is the biggest run ever. It is because it is the best microscope slide:

- late enough that the broad taxonomy is already mature
- small enough that the unresolved residual can be inspected directly
- hard enough to still be scientifically meaningful

Inside that frozen case, the hardest remaining low-overlap residual has been narrowed again and again:

- first to a low-overlap basin
- then to a center-spine residual
- then to a tiny `00` bucket
- and now to an exact-but-fragile closure family

That is a good sign. It means the unresolved part is becoming smaller and more concrete, not fuzzier.

## Technical Version

### Model Axioms

The toy is built around a compact event-network ontology:

- reality is an evolving network of events and influence relations
- stable objects are persistent self-maintaining patterns in that network
- space is inferred from neighborhoods and signal delays
- duration is local update count along a pattern history, not universal background time
- the arrow of time is tied to increasing durable record formation
- free evolution follows locally admissible/simple continuation
- measurement is modeled as durable record formation that separates alternatives

### Core Primitives

The code works with toy versions of:

- events
- directed influence links
- local delay `delta(e, e')`
- local compatibility weight `k(e, e')`
- histories through the network
- durable records
- persistent patterns
- local update counts along a history

### What the Code Actually Implements

The runnable model currently does all of the following:

- infers a local delay field from stable persistent patterns on a graph
- infers causal order from positive local delays instead of imposing one global step order
- runs path selection on top of that inferred causal structure
- models durable-record sectors in a two-slit-style interference toy
- uses one shared local edge rule across the causal-shell graph, the asynchronous continuation model, and the slit graph
- runs corrected benchmark, overlap, and mechanism diagnostics through helper-backed scripts

The current practical entry points are:

```bash
python3 /Users/jonreilly/Projects/Physics/toy_event_physics.py
```

```bash
python3 /Users/jonreilly/Projects/Physics/scripts/base_confidence_check.py
```

For the deeper helper-backed verification pass:

```bash
python3 /Users/jonreilly/Projects/Physics/scripts/base_confidence_check.py --full
```

### What the Strongest Current Results Are

#### 1. Gravity-like continuation survives the benchmark cleanup

The model still supports a gravity-like story after the benchmark fixes:

- a local delay field can emerge from stable patterns
- path selection through that field can bend inward
- the high-retained-update / spent-delay end of the tested action family still performs best on the corrected benchmark

This is not yet a derivation of general relativity. It is a toy demonstration that geometry-like path bending can be recovered from local network structure plus a derived delay field.

#### 2. Measurement-like record sectors still matter

The model still supports the core record story:

- alternatives can combine when no durable record separates them
- durable record sectors suppress that combination

Again, this is a toy measurement story, not a full quantum formalism.

#### 3. The compact/extended mechanism split is real

The strongest stable mechanism picture is:

- `compact` has a cleaner threshold-core story
- `extended` is more permissive and uses fallback structure

The useful compressed version is:

- broad `6+` support is still the main compact support story
- the stricter `7+` route is the clean shared fast anchor
- `extended` can defect through fallback structure where `compact` stays more tightly thresholded

#### 4. Frontier growth is mostly support-filling now

The later non-pocket frontier work now looks like:

- stable taxonomy
- expanding membership
- flattening coarse-signature growth

The important conclusion from the compression passes is:

- the late ladder is mostly filling out already-seen basins
- it is no longer the main discovery engine

That is why the active science focus shifted toward:

- latent compression
- order parameters
- support topology
- candidate-lobe structure

and away from dense ladder chasing.

#### 5. The hardest frozen residual now has an exact closure with a broad rescue family

On the frozen `5504` low-overlap center-spine `00` core, the current add1-side closure is now compact and interpretable.

The baseline clause is:

- `delta_edge_identity_support_edge_density <= 0.018`

Exact rescue families then include clauses like:

- `delta_count_family_pocket <= -14.500`
- `delta_edge_identity_event_count <= -14.500`
- `pair_selected_event_present_count >= 6.000`
- `abs_delta_edge_identity_open_pair_count <= ...`
- exact binary event clauses of the form `ev_* >= 0.500`

This yields:

- exact add1 closure on the bucket target
- `42/0/0` for the add1 side
- `45/45` overall in that bucket

The important correction is that the rescue side is not actually “single-threshold fragile.”

- the old midpoint-count logic understated actual mask-stable interval width
- the strongest exact rescue we have now is:
  - `delta_count_family_pocket <= -14.500`
  - which exactly matches the width of the broader `delta_edge_identity_event_count <= -14.500` rescue
  - interval `[−18.000, −11.000)` with width `7.000`
- so the wide rescue is not just an abstract event-count delta; it is already mostly a pocket-family support-edge identity deficit
- one more bounded pocket-subfamily pass shows that this does **not** collapse all the way to one tiny micro-cause
  - best exact single micro-rescue is `delta_count_pocket_present0 <= -8.000`
  - interval `[−10.000, −6.000)` with width `4.000`
  - so the full width-`7.000` rescue still lives at the broader pocket-family level
- the rescued rows themselves are not heterogeneous exceptions:
  - both rescued rows share the same pocket-loss profile
  - `delta_count_pocket_total = -18`
  - `delta_count_pocket_present0 = -10`
  - `delta_count_pocket_present1 = -8`
  - `delta_count_pocket_role_pocket_only__pocket_only = -12`
- a bounded signed-basis scan now shows the wide family-law rescue is already expressible in a smaller visible pocket basis:
  - `delta_count_pocket_present0 + delta_count_pocket_present1 <= -14.500`
  - same rescued rows, same interval `[−18.000, −11.000)`, same width `7.000`
  - and an even wider exact matching composite exists:
    - `delta_count_pocket_present0 + delta_count_pocket_present1 + delta_count_pocket_role_pocket_only__pocket_only <= -26.000`
    - interval `[−30.000, −22.000)`, width `8.000`
- a canonical bounded weight scan then tightened the interpretation:
  - the two-term `present0 + present1` law is not unique
  - several exact family-mask matches already exist in the same visible pocket basis, including 1-term cuts:
    - `delta_count_pocket_present0 <= -8.000`
    - `delta_count_pocket_present1 <= -6.500`
- a margin-profile pass explains why:
  - the two rescued rows are isolated low-tail outliers across several pocket coordinates
  - next non-rescued rows are already at:
    - `present0 = -6`
    - `present1 = -5`
    - `pocket_only__pocket_only = -11`
    - `pocket_only__pocket_only__present0 = -6`
  - so many different visible-basis thresholds recover the same two-row rescue mask
- a bounded nearest-neighbor geometry-difference pass localizes the concrete edit bundle above those cutoffs:
  - the exact nearest non-rescued anchor is `base:taper-wrap:local-morph-௥` with `(-6, -5, -11)` on `(present0, present1, pocket_only__pocket_only)`
  - both rescued rows are missing the same own-side pocket-support family relative to that anchor:
    - `+6` `count_pocket_role_bridge__pocket_only`
    - `+1` `count_pocket_role_pocket_only__pocket_only`
    - joined split: `+4` `bridge__pocket_only__present0`, `+2` `bridge__pocket_only__present1`, `+1` `pocket_only__pocket_only__present1`
  - both rescued rows currently carry only `bridge__bridge` pocket-role activity, so the low-tail corner is a specific missing bridge-to-pocket / pocket-only support corridor, not a diffuse basis artifact
- a bounded corridor-clause scan over exactly those role/joined corridor coordinates confirms the same rescue mask is already reachable in compact corridor language:
  - exact two-term role clause:
    - `delta_count_pocket_role_bridge__pocket_only + delta_count_pocket_role_pocket_only__pocket_only <= -14.500`
    - same rescued rows and same interval `[−18.000, −11.000)` (width `7.000`) as the family-law reference
  - weighted corridor clauses can be even wider while still exact on this frozen core, e.g.:
    - `2*delta_count_pocket_role_bridge__pocket_only + delta_count_pocket_role_pocket_only__pocket_only <= -19.000`
    - interval `[−24.000, −14.000)` (width `10.000`)
  - this keeps the non-uniqueness result but sharpens the physical-language translation: the rescue side is expressible directly as a bridge-to-pocket plus pocket-only support deficit, not only as aggregate pocket totals
- a bounded canonical corridor-equivalence pass then settles the minimality question for this frozen core:
  - after scale/sign canonicalization, every bounded exact corridor clause found (`796/796`) reproduces the same family rescue mask
  - minimal exact family-mask closure is not the two-term role law; it is already non-unique at one term (`5` distinct one-feature cuts)
  - representative 1-term exact cuts include:
    - `delta_count_pocket_joined_bridge__pocket_only__present1 <= -2.500`
    - `delta_count_pocket_joined_pocket_only__pocket_only__present0 <= -6.500`
    - `delta_count_pocket_role_pocket_only__pocket_only <= -11.500`
  - so role-level corridor language remains useful as interpretation, but joined-level low-tail coordinates already carry sufficient exact rescue separation on this core
- a bounded robustness pass then separates “minimal exact” from “structurally roomy”:
  - the top 1-term corridor clauses are not brittle under row drops; they survive `45/45` single-row removals
  - the interpretable 2-term role clause also survives `45/45`
  - the real difference is threshold slack:
    - 1-term corridor widths stay around `1.000`
    - the 2-term role clause keeps width `7.000`
- and a visible-basis nearest-neighbor pass shows why the rescue side is still not the final discriminator:
  - there are baseline-covered add1 neighbors at basis distance `0.000` from the rescued rows
  - `local-morph-Ǎ` and `local-morph-఩` share the same visible pocket-basis coordinates as the rescued rows
  - but they differ by concrete node-layout edits and are already captured by the baseline density clause
  - so the remaining discriminating information is no longer on the rescue-side pocket basis itself; it now lives on the baseline-density / finer support-layout side
- other exact rescues also have real positive width:
  - `pair_selected_event_present_count >= 6.000` with width `2.000`
  - `abs_delta_edge_identity_open_pair_count <= 22.500` with width `1.000`
  - exact event predicates with interval `(0.000, 1.000]`

So the current read is:

- the mechanism closure is probably touching something real
- the rescue family is genuinely robust on the current frozen core
- the rescue family compresses to a pocket-family deficit law and now also to a small signed visible pocket basis
- the robust rescue still does not collapse to one tiny pocket subfamily
- and the exact rescue mask is not unique inside that visible pocket basis, because the rescued rows occupy an isolated low-tail corner whose concrete geometry is a missing bridge-to-pocket / pocket-only support corridor
- and this corridor now has an explicit compact role-level clause family that reproduces the exact rescue mask on the frozen core
- and canonical corridor equivalence confirms the closure is highly degenerate: one-feature joined/role corridor cuts already reproduce the exact family rescue mask
- but those minimal corridor clauses are only narrow exact cuts, while the 2-term role clause remains the wider and more interpretable representative
- and because baseline-covered add1 neighbors already sit at visible-basis distance `0.000`, the remaining unresolved structure now sits with the baseline-density / finer layout side rather than the rescue-side pocket coordinates alone
- a bounded baseline-side zero-distance pass now makes that local branch much more concrete:
  - on the rescued rows versus the two basis-distance-`0.000` baseline peers, the exact split is already a degenerate one-mask family on simple support counts
  - strongest exact local separator:
    - `edge_identity_closed_pair_count <= 62.000`
    - interval `[56.000, 68.000)` with width `12.000`
  - equivalent exact local cuts include:
    - `support_node_count <= 18.500`
    - `support_role_bridge_count <= 18.500`
    - `support_edge_count <= 31.500`
    - `support_edge_role_bridge__bridge_count <= 31.500`
  - so the local baseline branch is not “one special density trick”; it is a smaller all-bridge support graph with fewer closed pairs and fewer bridge-bridge edges
  - the same zero-distance pass also finds an exact local candidate-cell motif:
    - rescued rows lack `pocket/deep cell (1, -2)`
    - both basis-identical baseline peers carry that cell
  - but a broader baseline-covered add1 scan shows this is only a local branch marker:
    - `pocket/deep cell (1, -2)` appears in only `5/40` baseline-covered add1 rows
    - so the `(1, -2)` motif is not the whole baseline-side law
  - a bounded broader-family decomposition seeded by
    - `edge_identity_closed_pair_count`
    - `support_role_bridge_count`
    - motif presence for `(2, 1)`, `(4, 2)`, `(5, 0)`
    confirms that support totals plus this small motif set do **not** close the `(1, -2)` peer branch exactly (`5` peer rows vs `35` non-peers; best rules are partial, no exact separator)
  - a bounded topology-residual follow-up added support-layout signatures (bridge-degree bins plus support-edge span/orientation bins, including bridge-bridge-only variants) on the same `40` baseline-covered add1 rows
  - this richer layout basis still gives no exact `(1, -2)` peer-branch closure (best remains partial at `2/5` true positives with one false positive)
  - measured span/orientation coordinates are largely collapsed across this pool (`span>=4` and `skew` support-edge bins are all `0`), so these coarse topology bins do not provide the missing discriminator
  - so the broader baseline-covered add1 side now appears to require richer support-layout topology (or additional coordinates) beyond these coarse totals and sparse branch-cell motifs
  - a bounded candidate-anchored residual pass then closes the `(1, -2)` peer branch exactly on the same broader pool (`40` rows):
    - exact peer rule: `anchor_adj_bridge_count >= 3.500` (`5/5` TP, `0` FP)
    - equivalent complement: `anchor_adj_bridge_count <= 3.500` (`35/35` non-peer TP, `0` FP)
  - physical translation: the peer branch is exactly the subset where the `(1, -2)` anchor cell is coupled to a dense local bridge neighborhood (at least four adjacent bridge supports)
  - a bounded coordinate-agnostic local-neighborhood pass then shows this is **not** a generic “any dense local bridge cell” invariant:
    - `max_candidate_adj_bridge_count >= 6.500` hits all `40/40` baseline-covered add1 rows
    - so dense candidate-local bridge neighborhoods are ubiquitous across this pool, not specific to the peer branch
  - but one more bounded coarse-band translation does recover an exact non-anchor statement for the peer branch:
    - `high_bridge_left_low_count >= 0.500` (`5/5` TP, `0` FP)
    - complement: `high_bridge_left_low_count <= 0.500` (`35/35` non-peer TP, `0` FP)
  - so the broader baseline-covered add1 peer branch does compress beyond the fixed cell:
    - not “any dense local bridge candidate”
    - but “at least one dense high-bridge candidate in the left/lower band”
  - current best physical read:
    - broad baseline-covered add1 pool: dense local bridge neighborhoods are common
    - peer branch: the same local bridge density appears in a specific left/lower candidate band
  - a bounded non-peer-core decomposition now shows the remaining `35` baseline-covered add1 rows are not one amorphous residual:
    - two dominant non-peer families already occupy `20/35` rows
    - dominant buckets:
      - `rc0|ml0|c2` (`12` rows): no right-center high-bridge cell, no mid-low branch, exactly `2` high-bridge cells
      - `rc0|ml1|c3` (`8` rows): no right-center high-bridge cell, one mid-low branch, exactly `3` high-bridge cells
    - on that dominant `20`-row subset, the split is exact on `high_bridge_cell_count` alone:
      - `<= 2.500` isolates the compact `c2` family
      - `>= 2.500` isolates the `c3` / mid-low family
  - the remaining `15` rows then break into a small set of satellites rather than a diffuse cloud:
    - right-center low-support `c2` triplet:
      - exact via `edge_identity_closed_pair_count <= 61.000`
    - low-support `ml2p` `c3` pair:
      - exact via `high_bridge_low_count >= 1.500`
    - high-support `ml0` branch:
      - `c3` triplet and `c4p` pair
      - exact size split on the branch-local `5` rows via `high_bridge_cell_count <= 3.500` vs `>= 3.500`
    - high-support `ml1` `c4p` pair:
      - exact via `edge_identity_closed_pair_count >= 83.000 and high_bridge_mid_low_count >= 0.500`
  - so the broader baseline-covered add1 side now looks like:
    - solved peer branch: left/lower dense high-bridge band
    - two dominant non-peer families
    - a few small satellite branches
- the remaining tight part is therefore no longer “what are the baseline add1 families?”; it is whether this now-solved baseline family map transfers into the broader low-overlap basin
  - a bounded transfer pass on the frozen `5504` low-overlap rows now says “yes, mostly” at the family level:
    - all three low-overlap subtypes (`add1`, `add4`, `pair-only`) occupy the same two dominant support buckets:
      - `rc0|ml0|c2`
      - `rc0|ml1|c3`
    - they also all appear in the same left/lower `peer-band` (`high_bridge_left_low_count >= 0.500`)
    - shared primary-bucket occupancy is substantial, not anecdotal:
      - `rc0|ml0|c2`: `15` add1, `8` add4, `9` pair-only
      - `rc0|ml1|c3`: `12` add1, `9` add4, `7` pair-only
    - so the solved add1 map does transfer at the coarse support-family level; the low-overlap subtypes are not living in disjoint support-bucket worlds
  - what does **not** transfer is a tiny exact subtype rule inside those shared buckets:
    - `rc0|ml0|c2` remains mixed, with only partial subtype rules
    - `rc0|ml1|c3` remains mixed, with only partial subtype rules
    - a few subtype-exclusive satellites exist, but they are small and no longer look like the main scientific object
  - the current physical read is therefore:
    - the coarse support-family map is shared across low-overlap subtypes
    - subtype identity now lives in how those shared buckets are populated internally
    - the next missing signal is bucket-local support-layout / topology, not a brand-new global family axis
  - bucket-local profile summaries already show distinct internal loading patterns:
    - in `rc0|ml0|c2`, add4 is more mid-loaded, add1 is more left-loaded, and pair-only is the lower-support branch
    - in `rc0|ml1|c3`, add4 is the strongest mid-loaded subtype, add1 keeps the stronger left-loading, and pair-only is the higher-support / more right-loaded branch
  - one bounded bucket-local topology pass on the largest mixed shared bucket (`rc0|ml0|c2`) sharpens that read further:
    - add1 improves when support-edge density is low and left-loading is retained:
      - `edge_identity_support_edge_density <= 0.188 and high_bridge_left_count >= 0.500` (`12/15` TP, `2` FP)
    - pair-only improves when support is lower and the local edge-identity structure stays more open:
      - `edge_identity_open_pair_count <= 62.500 and support_role_bridge_count <= 14.500` (`6/9` TP, `2` FP)
    - add4 remains the hardest branch there, but the best partial rules are now clearly the more mid-loaded / more internally closed rows:
      - `edge_identity_closed_pair_count >= 57.500 and high_bridge_mid_count >= 0.500`
      - or equivalently high closed-pair ratio plus mid-loading
    - so even inside the biggest shared bucket, subtype drift is already physical:
      - add1: left-loaded, lower-density branch
      - add4: mid-loaded, more closed-support branch
      - pair-only: lower-support, more open-support branch

### What the Current Mechanism Story Looks Like

At the highest level:

- `both-sensitive` is the compact loaded high-overlap family
- `add1`, `add4`, and `pair-only` share a lower-overlap boundary basin
- that lower-overlap basin also shares a coarse support-family map, not just a vague phenomenological label
- the visible boundary/profile variables are informative, but not sufficient to regenerate that low-overlap basin with a tiny exact rule family
- inside that low-overlap basin, the remaining unresolved structure now sits mostly inside shared primary support buckets, where the missing signal looks increasingly like bucket-local support-layout or candidate-topology interaction

That is the most honest current summary:

- stable taxonomy
- complicated boundary
- residual topological structure still unresolved

## Why the Ladder Is No Longer the Main Object

The ladder was useful because it established that the mechanism map was not a shallow artifact.

But later on, the pattern became:

- more rows
- roughly the same families
- weaker returns from each extra rung

So the current ladder is best treated as a guardrail, not the main science thread.

If future sparse sentinels show:

- a new subtype family
- exact-rule drift
- or a new unresolved collision

then the ladder matters again.

Otherwise, the main question is no longer “how many more rows are there?” It is:

- what hidden structural law separates the families we already know exist?

## What To Trust Right Now

The parts that are on relatively strong footing are:

- the corrected benchmark plumbing
- the compact/extended split as a real toy-model mechanism distinction
- the existence of a stable late taxonomy with growing membership
- the current `5504` frozen-core results as real mechanism archaeology, not just tool noise

The one-command practical confidence gate is:

```bash
python3 /Users/jonreilly/Projects/Physics/scripts/base_confidence_check.py
```

## Current Limits

These are the major unresolved or still-cheating parts of the project:

- the spent-delay action is benchmark-favored, but not yet uniquely derived from first principles
- there is no continuum limit or standard field-theory bridge yet
- there is no direct empirical prediction in ordinary physics language yet
- the low-overlap basin still does not collapse to a small robust visible law
- the exact closure on the frozen `5504` center-spine `00` core is only half-compressed: the rescue family is broad, but the baseline density cut is still locally tight

So this repository should currently be read as:

- a serious toy-mechanism program
- not yet a finished physical theory

## Where The Detailed History Lives

This README is intentionally no longer the line-by-line research diary.

For detailed chronology, worker state, and exact next steps, use:

- [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
- [physics_autopilot_handoff.md](/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md)
