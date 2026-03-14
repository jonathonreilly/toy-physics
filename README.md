# Discrete Event-Network Toy Model

This workspace contains a small runnable prototype for a discrete event-network model.

`Octopus physics` is a lightweight project nickname; the claims in this README are about the event-network toy model itself.

## How To Read This README

- `Model Axioms`, `Primitives`, and `Toy Rules` describe the conceptual scaffold and the assumptions currently carried by the model.
- `What the current script implements` describes the mechanics that are actually present in the repository.
- `What the current script demonstrates` is narrower: it lists behaviors that the runnable toy model currently produces or pressure-tests.
- `What is still cheating` lists the assumptions that remain unresolved or only partially justified.

## Model Axioms

This toy model is built around a compact event-network ontology:

- Reality is an evolving network of events and influence relations.
- Stable objects are persistent self-maintaining patterns in that network.
- Space is inferred from influence neighborhoods and signal delays.
- Duration is local update count along a pattern's history.
- The arrow of time is the direction of increasing durable record formation.
- Free systems follow the locally simplest allowed continuation.
- Inertia is undisturbed natural continuation.
- Gravity is natural continuation in a distorted continuation structure.
- Measurement is the formation of durable records that separate previously combinable alternatives.
- Consciousness is part of the wider ontology as a high-order record-integrating self-model, but it is not simulated here.

## Primitives

The code models the following toy primitives:

- `Event e`: a local change.
- `Link e -> e'`: an allowed influence from one event to another.
- `delta(e,e')`: delay on that influence.
- `k(e,e')`: compatibility weight for that influence.
- `History h`: an ordered chain of linked events.
- `W(h)`: the total weight of a history.
- `R`: a durable record state.
- `S`: a stable self-maintaining pattern in the event network.
- `tau_S(h)`: the internal update count of pattern `S` along history `h`.

## Toy Rules

- Reality evolves by extending compatible histories.
- Free evolution follows the locally best-compatible histories.
- Geometry is inferred from the delay and coupling structure, not assumed first.
- Duration is local update count, not a universal background.
- Dense stable patterns modify local delays, compatibilities, and update rates.
- Alternatives without durable records can combine.
- Alternatives tagged by different durable records cannot combine.
- Conscious systems are part of the wider framework as record-integrating predictive processes, but this prototype only models durable records, not consciousness itself.

## Conceptual Motivation

These points explain how the current toy model is motivated. They are not all direct outputs of the script:

- The ontology starts from events, links, delays, and durable records rather than particles in a pre-given container.
- The local `retained update` term `sqrt(dt^2 - dx^2)` is motivated by the boost-like symmetry pressure test, while the `spent delay` action adds the extra accounting assumption that still has to be justified.
- Gravity-like behavior is motivated by treating persistent self-maintaining patterns as sources of local delay/load rather than by inserting a force law.
- Measurement is motivated as durable record formation, with interference lost when alternatives are separated into different record sectors.

Run it with:

```bash
python3 /Users/jonreilly/Projects/Physics/toy_event_physics.py
```

What the current script implements:

- Extracts a classical-looking limit from the same shared local rule by following stationary-action geodesics on the async graph.
- Derives the local delay field from an emergent persistent pattern whose late-time occupancy sources graph-load under neighbor averaging, with the initial disturbance and self-maintenance rule jointly selected by searching interior one-node seeds against a compact rule family.
- Infers causal order from positive local delays on a graph, then orients propagation by that inferred causal order instead of a global step counter.
- Runs a small robustness sweep across rectangular, tapered, and skewed graphs, with hard or wrapped vertical boundaries and compact or extended local rule families.
- Models `measurement` as durable record formation in a two-slit-style path network.
- Uses one shared local edge rule for the causal-shell graph, the asynchronous continuation model, and the slit graph.
- Makes the local rule explicit through a small set of postulates and a derived `LocalRule` object.
- Uses bounded-memory summary passes for the deterministic, pairwise cross-weight, high-end weight-ladder, tracked-palette random, limited-rediscovery random, and geometry-randomized perturbation ensembles so the selector-free perturbation diagnostics can run without materializing every case row at once.
- Pressure-tests two of the biggest cheats:
  - why `positive weights only` are too weak for interference
  - why the `square rule` is less arbitrary once reversible linear mixing is required
  - which local scalar remains stable under boost-like frame mixing

What the current script demonstrates:

- The same local rule can be used to extract stationary-action geodesics while still inferring causal order from local delays.
- With a proper-time-style action derived from the same delay field, those geodesics bend inward in a gravity-like way instead of merely routing around a slow region.
- The delay field itself now emerges from a local graph-relaxation rule: the code searches over interior one-node seeds and simple update rules, grows each candidate into an orbit, and lets the most localized stable non-boundary component source the decaying load profile.
- A local-delay graph can recover an inferred causal order without assigning all nodes the same global step number.
- The robustness sweep is now stronger than before: a minimal reduced compact family survives all six tested scenarios, and the extended family also survives all six.
- The compact-family repair is informative rather than ad hoc: the hard-topology winners under the full compact family are `skew-hard -> S[2,3]/B[3]` and `skew-wrap -> S[3,4]/B[1,3]`, which first repairs the compact family to `{3}, {1,3}, {2,3}, {3,4}`.
- Exhaustive minimization inside that repaired family shows one motif is still redundant, so the actual surviving compact subset is just `{1,3}, {2,3}, {3,4}`.
- One-by-one ablation of that three-option subset then shows all three remaining motifs are indispensable in the current sweep: removing `{1,3}` breaks `skew-wrap`, removing `{2,3}` breaks `taper-wrap`, and removing `{3,4}` causes the broadest collapse.
- A deeper mechanism ablation sharpens the story further: removing the delay field collapses the effect, and weakening field relaxation breaks the hardest wrapped skew case, so the field side looks genuinely load-bearing.
- The honest weak spot is now clearer too: replacing the proper-time-style action with plain coordinate delay weakens the sweep, but a bare link-length action still passes the current robustness metric, which means the action principle is not yet uniquely selected by the present tests.
- A final action-response discriminator closes most of that gap: once the benchmark also requires the distorted geodesic to move relative to the free geodesic, the spent-delay action with relaxed field propagation is the only named mechanism that both survives all six scenarios and keeps positive wrapped-case path response.
- A broader retained-weight family sweep then sharpens the remaining ambiguity: the low-weight half of the family fails the combined benchmark, while only the high-weight end survives, with the strongest wrapped-case response at the full spent-delay point `w = 1.0`.
- A cross-pack benchmark widens that test further across larger and mirrored scenario packs. It still favors the high-retained-update end, but it does not yet collapse the family all the way to a single exact coefficient.
- A final high-end proper-time consistency benchmark then zooms in on `w = 0.75..1.00` and checks every off-center boundary target across all packs. In the current grid, `w = 1.0` is the only retained weight that keeps the action gain larger than the extra coordinate delay everywhere, which is the first benchmark here to single out the exact spent-delay point within a tested family.
- The next decomposition makes that crossing more explicit: for a fixed distorted path, the consistency margin is linear in `w`, with a calculable critical weight `w* = 2 * delay_penalty / retained_total`.
- Under the current always-compare selector, the hardest case is now `mirror:rect-hard-large`, and the active winner stays `S[3,4]/B[1,3]` across the scanned `w = 0.75..1.00` range. So the present sign change is no longer a late branch switch; it is a single-branch crossing with the worst target moving as `w` changes.
- A rule-selection diagnostic shows why that branch is preferred: the fallback motif `S[2,3]/B[3,4]` keeps a slightly larger `center gap` at the low end, but the rescue motif `S[3,4]/B[1,3]` carries a much larger `arrival span`, so the current quality key `center gap + arrival span` already favors rescue from the start and favors it even more by `w = 1.0`.
- A frozen-branch comparison then removes another layer of heuristic freedom: the fallback branch becomes proper-time-consistent earlier, but the rescue branch keeps the stronger delay-distortion signature. Both branches still `survive`, so the selector is choosing between two viable motifs rather than between a working and failing one.
- The geometric diagnostic sharpens that point further: both frozen branches keep the same source row on the current hardest case, but they trade off final action contrast against boundary-delay distortion differently. So the selector is not reacting to a source jump; it is reacting to the current robustness quality.
- The focus-metric comparison makes the ambiguity explicit: on the current hardest case, pure geometric focus still favors the fallback branch throughout, a stiffness-style action-per-separation ratio favors the rescue branch throughout, and raw action-gap flips from fallback at low `w` to rescue at high `w`.
- A selector-policy ablation shows what survives when the old gate is removed. The current always-compare selector and the legacy gated selector differ in `20/78` compact benchmark pack-weight cases, concentrated in `base:taper-wrap`, `large:taper-wrap-large`, `large:skew-wrap-large`, and `mirror:rect-hard-large`; all of those changed cases still `survive`, so selector policy is steering branch choice more than pass/fail status.
- A new selector-free frontier layer now keeps nondominated motifs alive instead of collapsing immediately to one winner. It is diagnostic-only: the baseline selector still uses the current `always_compare` quality key, but the script now also reports `robustness`, `proper-time`, `geometry`, and `mixed` frontiers across both families and the benchmark packs.
- The cached frontier pass now runs end-to-end across all `156` family-pack-weight cases in the current benchmark grid. In the present run, the baseline-selected motif lies on the `robustness`, `proper-time`, `geometry`, and `mixed` frontiers in `52/156`, `22/156`, `35/156`, and `114/156` cases respectively, so no single frontier view reproduces the current selector.
- On the current hardest compact case, `mirror:rect-hard-large`, the selected rescue motif `S[3,4]/B[1,3]` sits on the `robustness` and `mixed` frontiers across the scanned retained-weight range, while the fallback motif `S[2,3]/B[3,4]` still remains nondominated on a non-identical view. That is the cleanest selector-free version of the current result: different metric views keep different motifs alive even when the baseline picks only one.
- The frontier reporting is now split three ways in the script: a case-level overview, a motif-frequency aggregate across both families, and a hard-case trace for the fallback/rescue motifs. In the current compact sweep, `S[2,3]/B[3,4]` appears on the `mixed` frontier in all `78` compact cases and on the `proper-time` frontier in `46`, while `S[3,4]/B[1,3]` is the current selected motif in `67/78` compact cases. That makes it possible to talk about selector-invariant motifs separately from selector-dependent winners.
- A first deterministic topology-perturbation ensemble now nudges each benchmark graph in two small ways at `w = 1.0` and tracks the unperturbed frontier palette through those perturbations. This is still diagnostic-only, but it is the first direct test of whether the current motif/frontier claims survive graph-level changes rather than only metric changes.
- Under that perturbation ensemble, the mixed-frontier story is much more stable than the selected-rule story. In the current run, `mixed`-frontier overlap survives in `26/26` perturbed cases for both `compact` and `extended`, while robustness overlap survives in `20/26` for both families. By contrast, the selected motif is retained in only `12/26` compact and `11/26` extended perturbed cases.
- The perturbation results are therefore interesting in a very specific way: some selector-free motif families look topology-robust, but the exact baseline winner is still quite topology-sensitive. That is a more honest and more useful result than simply reporting whether one selected motif keeps winning.
- A cross-weight perturbation comparison then asks whether that topology-robust story also survives a smaller retained-weight shift from `w = 1.0` down to `w = 0.95`. In the current run, the perturbed selected winner is actually stable across those two weights in `26/26` cases for both families, and `mixed`-frontier overlap also stays `26/26` for both families.
- The more fragile pieces are not the perturbed winner across the two high-end weights; they are the stronger overlap claims back to the unperturbed baseline. The base selected motif remains frontier-alive at both weights in `19/26` compact and `20/26` extended cases, while robustness overlap survives at both weights in `20/26` compact and `18/26` extended cases.
- So the current picture is sharper now: the selector-free mixed-frontier family looks robust to both topology nudges and a small retained-weight change, while the exact relationship back to the unperturbed baseline winner remains the part that breaks first.
- A high-end weight ladder now pushes that check one notch farther across `w = 0.90, 0.95, 1.00`. In the current run, the perturbed selected winner stays the same across the full ladder in `25/26` cases for both families, while `mixed`-frontier overlap survives in `26/26` cases for both families.
- The stronger selector-free overlaps are stricter on the full ladder: robustness overlap survives in `16/26` cases for both families, while proper-time and geometry overlap survive in `12/26` compact and `10/26` extended cases. So the mixed frontier still looks like the most stable selector-free object in the current model, but the tighter overlap notions remain much more local.
- A slightly wider seeded-random perturbation ensemble now pushes on the same question from the opposite direction: not hand-picked nudges, but three random removable/addable node choices drawn from each benchmark graph. In the current run, the same split still mostly survives that test.
- Under the widened random ensemble, `mixed`-frontier overlap survives in `38/39` compact and `39/39` extended cases, while robustness overlap survives in `30/39` for both families. By contrast, the exact unperturbed winner is retained in only `12/39` compact and `8/39` extended random perturbation cases.
- That is still the strongest selector-free result so far, but it is a little more honest than the earlier two-variant picture: once we stop insisting on one exact winning motif, the mixed-frontier family still looks substantially more stable than the exact winner under deterministic nudges, a small high-end weight shift, and a broader seeded-random graph ensemble, even though the wider random pass now exposes one compact-family mixed-frontier miss.
- A first limited-rediscovery random ensemble then removes one more cheat: instead of forcing perturbed graphs to stay inside the unperturbed frontier palette, it lets each random perturbation reintroduce a small number of locally rediscovered motifs. In the current `limit = 2` run, that repairs the last random `fragile` cases, but it does not strengthen the selector-free overlap story uniformly.
- Under limited rediscovery, all `39/39` random cases now `survive` in both families, and the mixed-frontier overlap remains `38/39` for `compact` and `39/39` for `extended`. But the stronger overlap claims get weaker: robustness overlap drops to `29/39` compact and `26/39` extended, and base selected-motif frontier survival drops to `32/39` compact and `29/39` extended.
- That tradeoff is useful rather than disappointing. It says some of the earlier random robustness was genuinely helped by palette inheritance, but the mixed frontier still remains the strongest selector-free object even after we relax that inheritance.
- A rediscovery-limit sweep over `0, 1, 2, 3` makes that tradeoff more precise. One extra rediscovered motif is already enough to repair the last random `fragile` cases in both families, and increasing the limit beyond `1` does not improve selected-rule retention, base selected-motif survival, or mixed-frontier overlap.
- In `compact`, the sweep goes `survives 38 -> 39`, `mixed 38 -> 38`, and `robustness 30 -> 29` from limit `0` to `3`. In `extended`, it goes `survives 38 -> 39`, `mixed 39 -> 39`, and `robustness 30 -> 26`. So the mixed frontier saturates early, while the stricter overlap notions erode as more local novelty is allowed back in.
- That is a strong cheat-removal clue: the mixed frontier looks like a more structural object than the exact inherited frontier identity, but the stronger overlap claims are still partly propped up by palette restriction.
- A geometry-randomized benchmark ensemble then pushes on the graph-family cheat more directly. Instead of only punching or shifting nodes inside the existing packs, it jitters the entire column profile of each graph into two deterministic whole-shape variants and then applies the minimal rediscovery limit `1`.
- Under that whole-shape geometry jitter, `compact` still `survives` in `25/26` cases and keeps `mixed`-frontier overlap in `25/26`, while `extended` still `survives` in `26/26` and keeps `mixed` overlap in `26/26`. By contrast, exact selected-winner retention drops to `9/26` in `compact` and `6/26` in `extended`, with robustness overlap at `17/26` and `16/26`.
- That is one of the strongest results in the repo now: even when we stop testing only local node edits and start deforming the whole benchmark shape, the mixed frontier still looks much more stable than the exact winner.
- A procedural graph-generator ensemble then goes one step farther: instead of deforming the original contour, it regenerates each graph from scratch inside the same bounding box using a seeded smooth column-profile rule, again with rediscovery limit `1`.
- Under that procedural generator, both families still `survive` in `25/26` cases and keep `mixed`-frontier overlap in `24/26` cases. Exact selected-winner retention drops to `7/26` in `compact` and `6/26` in `extended`, with robustness overlap at `18/26` and `17/26`.
- That is a harder and more honest result than the earlier pack-local tests: the mixed frontier is no longer merely surviving local edits to hand-authored shapes, but it is also not perfectly stable once the graph family is regenerated from a small independent generator.
- A focused diagnostic on the lone compact procedural `survive` miss narrows that failure further. The miss still keeps mixed-frontier overlap, and its `center_gap` is actually larger than its nearby surviving sibling. What collapses is `arrival_span`, from `1.773` in the surviving sibling to `0.335` in the miss.
- Geometrically, that miss is the one case with a cross-midline, high-variation centerline: `center_range 3.5` and `center_total_variation 8.0`, versus `2.0` and `4.0` in the surviving sibling. So the current evidence points to a specific sensitivity: some deformations preserve local focusing while flattening far-boundary delay distortion enough to miss the present `survives` threshold.
- A direct contour-sensitivity sweep then turns that clue into a mechanism test. Holding the span profile fixed and interpolating only the centerline deformation keeps mixed-frontier overlap intact across the whole sweep. The `survives -> mixed` transition happens only at the highest deformation point, where `arrival_span` falls below the current `0.5` cutoff (`0.680` at `alpha = 0.75` versus `0.335` at `alpha = 1.00`), while `center_gap` remains large (`0.849 -> 0.772`).
- That is the strongest current evidence for what the mixed frontier is sensitive to: not generic contour roughness, but specifically deformations that preserve local focusing while suppressing far-boundary delay spread.
- With that repair in place, `extended` still produces the larger average boundary-delay span, while the reduced `compact` family keeps a slightly larger average center gap.
- The earlier `skew-wrap` miss is now understood as a legacy reduced-family coverage bug, not as a deep compact-vs-extended ontology split.
- The failure-mode story is still useful history: before the repair, skewed cases mostly failed by producing empty or fragmented candidate patterns, not by hitting the boundary filter, which pointed more toward pattern formation than boundary selection.
- Cross-slit interference disappears when histories are separated by durable record sectors, without any appeal to consciousness, while single-slit diffraction remains inside each sector.
- A Hadamard-style reversible mixer preserves the 2-norm but not 1- or 4-norm totals, which is a useful reason the Born-style square survives the pressure test better than arbitrary power rules.
- Under boost-like frame mixing, `sqrt(dt^2 - dx^2)` is the only tested local scalar that remains invariant; the remaining action assumption is the choice to treat `dt - sqrt(dt^2 - dx^2)` as spent delay.

What is still cheating:

- The spatial graph geometry is still hand-authored.
- The gravity-like classical limit still assumes that histories extremize spent delay `dt - sqrt(dt^2 - ds^2)` rather than deriving that accounting rule from deeper dynamics.
- The delay field is now derived from an emergent persistent pattern, but the rule family and locality preferences used to choose among candidate patterns are still hand-chosen.
- The current robustness criterion is still hand-chosen too: `center gap`, `arrival span`, and selector policy materially affect which surviving branch wins on the hardest cases.
- The current perturbation ensemble is still a first pass: it uses only two deterministic graph nudges per scenario, tracks the unperturbed frontier palette instead of doing open-ended motif rediscovery on every perturbed graph, and only evaluates the strongest retained-weight point `w = 1.0`.
- The weight-robustness checks are still local: the current pairwise comparison uses only `w = 0.95` and `w = 1.0`, and the stronger ladder check only extends that to `w = 0.90, 0.95, 1.0`, so the model is still being tested in a narrow high-end band near the spent-delay point rather than across the whole retained-weight family.
- The random perturbation ensemble is also intentionally small and seeded: it currently samples only three random variants per scenario, and even the rediscovery-limit sweep only tests a small `0..3` band of extra locally rediscovered motifs, so it is still a first robustness probe rather than a large-scale random-graph study.
- The geometry-randomization layer is still narrow too: it only jitters contiguous column profiles with small deterministic shifts, so it is a first deformation test of the graph family rather than a broad random-geometry generator.
- The procedural graph generator is still very small and structured: it only produces smooth contiguous column profiles inside the existing bounding boxes, so it is a first independent-family probe rather than a general graph-generation study.
- The robustness sweep budget is also hand-chosen: smaller graphs, reduced rule families, and shorter persistence windows trade completeness for runtime.
- Complex amplitudes are still assumed rather than derived.
- Consciousness is still outside the simulation; only record formation is present.

So this prototype does not replace physics. It is a compact testbed for checking which parts of the ontology can already be realized with a simple discrete model, and which parts are still axioms wearing different clothes.
