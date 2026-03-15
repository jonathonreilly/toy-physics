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
- Reuses cached generated-geometry prediction contexts within a single run so repeated graph-side predictor diagnostics do not rebuild the same procedural, graph-local morph, and whole-shape frontier rows from scratch.
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
- A final benchmark then tests whether the current axis-aligned `survives/mixed` threshold is the right observable at all. It compares the current `box-min` rule with smooth combined observables (`harmonic`, `geometric`, `arithmetic`) on the core robustness sweep, the geometry-randomized ensemble, the procedural generator, and the contour miss.
- All four observables preserve the current strong cases: `12/12` core survives, `51/51` geometry-randomized survives, and `50/50` procedural survives. The difference is in what happens to the current threshold misses.
- `box-min` leaves the contour miss as `mixed` and promotes none of the procedural misses. `arithmetic` and `geometric` rescue the contour miss but also promote the geometry miss. `harmonic` is the most conservative smoother: it rescues the contour/procedural miss (`survives`, score `1.23`) but leaves the separate geometry miss as `mixed`.
- That makes `harmonic` the strongest tested candidate for a combined focusing observable so far. It smooths the threshold exactly where the model now looks overly sharp, without simply promoting every non-surviving case.
- A follow-up diagnostic then runs that `harmonic` observable through the existing selector/frontier machinery without changing the candidate pool. This pass is still diagnostic-only: it relabels the already-evaluated frontier candidates instead of changing the baseline selector or rerunning the search.
- On the current `156`-case frontier sweep, that harmonic relabeling changes the selected winner in `105/156` cases while keeping the harmonic-selected rule at `survives` in all `156/156` cases. The baseline-selected rule still survives under harmonic in `154/156` cases.
- Under harmonic, the selected rule lands on the `robustness` and `mixed` frontiers in `78/78` cases for both `compact` and `extended`, while the old baseline-selected motif remains on the harmonic `mixed` frontier in only `58/78` compact and `56/78` extended cases.
- That is a stronger threshold-cheat result than the original contour benchmark alone: the sharp `box-min` status rule is not just patching a local miss, it is materially steering the selector/frontier picture even when the underlying candidate set is held fixed.
- A second diagnostic then removes the bucketization step itself: it keeps the harmonic candidate relabeling, but replaces the discrete `survives/mixed/fragile` rank with the continuous harmonic score as the leading selector/frontier axis.
- Relative to the bucketed harmonic pass, that continuous-score rerank changes the selected winner in only `31/156` cases and keeps both the continuous winner and the old bucketed harmonic winner at `survives` in all `156/156` cases.
- But it almost eliminates frontier disagreement. Under continuous harmonic scoring, the selected rule sits on all four frontier views in `78/78` cases for both `compact` and `extended`, while the old bucketed harmonic winner remains on the continuous proper-time/geometry frontiers in only `72/78` and `74/78` compact cases, and `65/78` and `67/78` extended cases.
- That makes the bucketization cheat more precise: the discrete rank is carrying much of the current frontier disagreement, even though it changes the selected winner much less than the earlier `box-min -> harmonic` observable change.
- A third diagnostic then removes the hand-named frontier vocabulary itself. It derives a covariance-based axis set from the harmonic-continuous candidate pool using `center_gap`, `arrival_span`, `min_margin`, `geometric_focus_gap`, and the harmonic focus score, then builds selector-free frontiers on `pc1`, `pc12`, and `pc123`.
- The leading derived axis loads positively on `center_gap`, `arrival_span`, and focus score (`0.469`, `0.456`, `0.568`) and negatively on `min_margin` and `geometric_focus_gap` (`-0.381`, `-0.323`), so the covariance story is not just reproducing one of the earlier named views verbatim.
- Under that derived basis, the current selected rule stays on the full `pc123` frontier in `153/156` cases, but only on `pc1` in `122/156` and on `pc12` in `129/156`. So the same core motif family still survives the full derived frontier, but much of the apparent low-dimensional agreement disappears once the view vocabulary is learned from the candidate cloud instead of named by hand.
- The top derived-axis motif in both families is still `S[2,3]/B[3,4]`, appearing on the `pc123` frontier in `55/78` compact and `52/78` extended cases. That is the strongest current selector-invariant result without the original frontier labels.
- A fourth diagnostic then varies the metric basis itself instead of only the frontier vocabulary. It compares the full five-metric covariance basis against smaller alternatives such as `focus3 = {center_gap, arrival_span, focus_score}` and `action3 = {arrival_span, min_margin, focus_score}` on the same harmonic-continuous candidate pool.
- The result is stronger than a simple “smaller basis gets worse” story. `focus3`, `no_margin`, and `action3` all keep the selected rule on the full `pc123` frontier in `156/156` cases, while the weakest tested basis, `no_focus`, still keeps it in `144/156`.
- Even more interestingly, every tested basis still has nonempty `pc123` overlap with the full five-metric basis in all `156/156` cases. So the full derived frontier is not isolated to one exact metric bundle.
- But the detailed motif ranking is still basis-dependent. In `compact`, the top `pc123` motif stays `S[2,3]/B[3,4]` for `4/5` tested bases; in `extended`, the same motif is top for `3/5`. Bases like `no_focus` and `focus3` can flip the leading motif family even when the broad `pc123` overlap remains intact.
- That makes the current state more precise: the full derived frontier looks structurally real in the toy model, but the fine-grained ordering of motifs is still sensitive to which raw metrics we feed into the covariance analysis.
- A fifth diagnostic then bootstraps the basis choice itself instead of fixing a small palette by hand. It now combines `16` subset bases, `12` seeded linear-random projection bases, and `9` mild nonlinear bases (`37` total basis views) on the same harmonic-continuous candidate pool.
- The nonlinear family is itself broadened beyond a few fixed transforms: it now includes three full-transform views (`signed_sqrt`, `signed_log1p`, `softsign`) plus small random projections of each transformed metric space. That makes the basis generator meaningfully wider than the earlier subset-plus-linear ensemble.
- The full-basis reference still keeps the selected rule on `pc123` in `153/156` cases, and `35/37` sampled bases keep full case-by-case `pc123` overlap with that reference. The weakest current basis is the nonlinear random view `softsign:rand01`, which drops to `145/156` overlap and `71/156` selected-on-`pc123`. So the full derived frontier is still robust, but not perfectly invariant once the generator is broadened.
- The bootstrap stability map is more informative than the smaller basis ablation because it separates ubiquity from dominance. In this run, `S[2,3]/B[3,4]` is the most ensemble-stable `pc123` motif in both families:
  - `compact`: present in `37/37` bases, `2270` basis-case frontiers, `25` top-basis wins
  - `extended`: present in `37/37` bases, `2124` basis-case frontiers, `26` top-basis wins
- With the broadened nonlinear ensemble, the same motif remains fully ubiquitous: in both families it appears in all `16/16` subset bases, all `12/12` linear-random bases, and all `9/9` nonlinear bases.
- But it is still not the only ubiquitous motif. In the current run, `17` motif-family pairs appear on `pc123` in every sampled basis, so the bootstrap result is not “one motif survives and everything else disappears.” The stronger claim is narrower: some motifs are basis-ubiquitous, and `S[2,3]/B[3,4]` currently dominates that ubiquitous set by aggregate coverage and top-basis wins.
- That is the strongest selector-invariant stability map in the repo so far. It no longer asks which motif wins under one chosen basis, or even one basis family, but which motifs keep reappearing on the full derived frontier across subset, linear-random, and nonlinear basis ensembles.
- A sixth diagnostic then stops fixing nonlinear transform intensity by hand too. It sweeps strengths `0.00, 0.25, 0.50, 0.75, 1.00` across the same three transform classes, again with both direct and projected variants, and asks when the transformed family first degrades beyond its own strength-zero baseline.
- On the current grid, none of the direct transformed bases break their identity-strength baselines at all. The first projected transform-induced break appears at strength `0.25` for both `signed_sqrt` and `softsign`, while `signed_log1p` does not break until `1.00`.
- The weakest transformed view is still `softsign:s1.00:rand01`, with `145/156` overlap and `71/156` selected-on-`pc123`. Even under that harsher sweep, the dominant motif `S[2,3]/B[3,4]` remains present in all `45/45` transform-family views in both `compact` and `extended`.
- That makes the nonlinear story more precise: the fragile part is not direct transformation by itself, but the combination of stronger nonlinear distortion with projection. The dominant motif survives that whole family anyway.
- A seventh diagnostic removes another remaining hand-choice inside that projection story. Instead of only keeping two seeded projected variants per mode/strength, it bootstraps `8` deterministic projections for every nonlinear mode/strength pair and asks which motifs still survive the broader projected family.
- This is a stronger test because it widens the projected subspace sampler without touching the underlying candidate pool. If the earlier nonlinear result had been mostly a tiny-palette artifact, it should break here first.
- In the current run, the dominant motif `S[2,3]/B[3,4]` remains the most projection-stable motif in both families across the full projected bootstrap, appearing in all `120/120` projected bases in both `compact` and `extended`.
- The twist is that the weakest projected cell is no longer a high-strength nonlinear corner. It already appears at `signed_log1p` strength `0.00`, which means projection choice itself is now the first real instability once that palette is broadened.
- That narrows the remaining cheat again: the model is no longer leaning on one specific two-projection palette, but the random projection generator itself is now visibly load-bearing.
- An eighth diagnostic tests that new weak spot directly by changing the projection generator, not the toy model. It compares the current raw random projections against row-normalized and orthonormalized variants on the same mode/strength grid.
- This is the right next step because the previous bootstrap showed that projection choice itself now breaks overlap earlier than transform intensity does. If normalization fixes most of that, then the main instability is in the projection generator rather than in the motif structure.
- In the current run, no projection generator cleanly wins on every metric. `row_norm` gives the best averages, `raw` keeps the best worst-case minima, and `orthonormal` improves top-basis dominance while actually worsening the weakest cells.
- That means the projection-induced weakness is not just a trivial scaling artifact. The generator matters, but changing it does not by itself remove the instability.
- A ninth diagnostic then pushes one layer deeper by changing the projection dimension itself. It compares orthonormal projected bases of dimensions `2, 3, 4, 5` on the same transformed metric family.
- That is a direct test of whether the remaining instability is mostly generator noise or metric-space compression. If the higher-dimensional projections restore overlap, then at least part of the weakness is coming from forcing the derived basis through too small a subspace.
- The current result is sharp. Dimension `2` is clearly the weakest (`107/156` minimum overlap, `33/156` minimum selected-on-`pc123`), dimension `3` is much healthier, and dimensions `4` and `5` nearly restore the full reference. Dimension `4` is the strongest by the current worst-case criterion, with `156/156` minimum overlap and `130/156` minimum selected-on-`pc123`.
- That makes the remaining projection story much clearer: a real part of the instability is compression-driven. Once the projected basis is allowed enough room, the same dominant motif `S[2,3]/B[3,4]` remains fully ubiquitous and the overlap almost completely recovers.
- A tenth diagnostic then reruns the selector-free stability map directly on that stronger `4D orthonormal` family instead of treating `3D` as the default projection bottleneck. This is the cleanest version of the question “what survives once the compression cheat is relaxed?”
- In the current run, all `60/60` bases in the `4D orthonormal` family keep nonempty `pc123` overlap with the full reference in all `156` cases. Selected-on-`pc123` is still not perfectly invariant, but it ranges much higher, from `130/156` to `156/156`.
- The dominant motif `S[2,3]/B[3,4]` remains the leading selector-free motif in both families across that whole `4D` ensemble, while `18` motif-family pairs are now fully ubiquitous across all `60` bases.
- That is a more meaningful selector-free result than the earlier `3D` story. Once the projection bottleneck is widened, the remaining disagreement looks more like motif ranking within a robust family than like wholesale loss of overlap.
- An eleventh diagnostic then switches from basis coverage to case-core intersection on that same `4D orthonormal` family. For each case, it intersects the `pc123` motifs across all `60` bases and asks which motifs are actually unavoidable rather than just frequently present.
- That is the stricter structural question. A motif can be ubiquitous across bases overall and still fail to be inevitable in any specific case; the case-core analysis separates those two ideas.
- In the current run, the case core is nonempty in `84/156` cases, and the currently selected rule lies inside that core in `81/156`. But exact basis-indifference is still absent: `0/156` cases have `core == union`, and the largest case core has size `4`.
- The strongest unavoidable motifs are now narrower than the broad basis-wide winners. In `compact`, `S[2,3]/B[3,4]` has `21` core hits out of `78` union hits. In `extended`, the strongest unavoidable motif is actually `S[3,4]/B[1,3]`, with `9` core hits out of `78` union hits.
- That is a useful sharpening. The selector-free family is robust, but truly unavoidable motifs are rarer than basis ubiquity alone suggests, and the `extended` case-core story is not identical to the family-wide coverage story.
- A twelfth diagnostic then turns those case-core counts into a mechanism map using the existing column-profile geometry metrics. It groups the `4D orthonormal` cases into `empty`, `single-selected`, `single-other`, `multi-selected`, and `multi-other` core regimes and compares their contour roughness and topology features.
- That is the right next question because the raw case-core counts alone do not say why some cases have an unavoidable motif and others do not. The mechanism map asks whether empty cores, single-motif cores, and multi-motif cores occupy distinct geometric regimes in the current graph family.
- In the current run, the split is surprisingly crisp. `72` cases have empty cores, and they are skew-heavy (`37/72`) with the same `37/72` midline-crossing count, plus higher average center-variation (`1.03`) and span-range (`1.47`) than the clean single-core regime.
- `74` cases land in the `single-selected` regime, and those are mostly rect+taper shapes (`52/74`) with lower average center-variation (`0.59`). The `multi-selected` regime is small (`7` cases) and mostly taper-shaped (`6/7`).
- That makes the current mechanism story much more concrete: empty cores are not random failures. They are concentrated in rougher, skewed, crossing profiles, while single-motif cores live in smoother rect/taper geometries.
- A thirteenth diagnostic then checks that mechanism continuously rather than only across named scenarios. It builds a small procedural family from the old contour-sensitivity path, holds the span profile fixed, and varies only the centerline roughness.
- That is the strongest follow-up to the mechanism map, because it asks whether the empty/single/multi core split really follows roughness as a continuous control parameter instead of just piggybacking on the benchmark scenario labels.
- The resulting response is not monotone in the interpolation parameter itself, because the realized roughness metrics dip in the middle and rise again. But it is strongly tied to the actual centerline roughness at fixed span profile.
- In `compact`, the low-roughness mid-sweep states (center-variation `2.0`) are the clean ones: all `6/6` weights land selected-in-core there, while the rougher states (center-variation `5.0`, `6.0`, and `8.0`) collapse back to all-empty cores.
- In `extended`, the same family shows a richer pattern: low roughness gives `6/6` multi-selected cores, mid-high roughness (`5.0`) collapses to `6/6` empty cores, and the roughest endpoint (`8.0`) partially re-enters the single-selected regime (`5/6`).
- That is a stronger mechanism result than the named-scenario map alone. The case-core split clearly tracks realized centerline roughness at fixed span profile, even though the response is family-dependent and can be re-entrant.
- A fourteenth diagnostic then removes the last big path-choice cheat in that roughness story. Instead of following one interpolation path, it probes a small basis of independent centerline modes at fixed span profile: `tilt`, `bowl`, `step`, and `zigzag`.
- That is the right next test because a single interpolation path can still hide a shape-specific artifact. The mode basis asks whether the roughness/core link survives across qualitatively different deformations or only along one chosen family.
- The result is more interesting than a simple “more roughness means more failure” rule. The broad roughness link survives, but the mode symmetry matters a lot.
- In `compact`, the smoother `tilt` mode stays mostly single-selected through amplitude `1.0` (`5/6` selected-in-core), and `step` even recovers to `6/6` selected-in-core at amplitude `1.5`. By contrast, `zigzag` is already fully destructive at amplitude `0.5`, with `6/6` empty cores.
- In `extended`, `bowl` at amplitude `1.5` gives `6/6` multi-selected cores, while `zigzag` collapses to `6/6` empty cores at amplitude `0.5` and then re-enters as `6/6` selected-in-core at amplitude `1.5`.
- So the roughness/core link is broader than one interpolation path, but it is not reducible to roughness magnitude alone. The symmetry class of the deformation is now clearly part of the mechanism.
- A fifteenth diagnostic then distills that mode result into a small invariant test. It groups the same fixed-span mode sweep by a simple shape signature: `smooth-monotone`, `step-like`, `curved`, `oscillatory`, plus whether the centerline crosses the midline.
- This is the direct answer to whether those invariants explain the behavior better than raw roughness alone. In the current run, they do.
- At the same roughness in `compact` (`center-variation = 2.0`), the outcomes split sharply by invariant class:
  - `curved/no-cross`: `1/6` selected-in-core
  - `smooth-monotone/cross`: `5/6`
  - `step-like/cross`: `3/6`
- At the same roughness in `extended` (`center-variation = 6.0`), the split is even sharper:
  - `curved/cross`: `6/6` selected-in-core
  - `oscillatory/no-cross`: `0/12`
- Across the current mode sweep there are `9` roughness groups where identical center-variation still splits into different case-core outcomes by invariant class.
- That is the strongest current mechanism statement in the repo: roughness magnitude matters, but monotone vs oscillatory and crossing vs non-crossing explain the case-core behavior better than roughness alone, without yet collapsing it to one single invariant rule.
- A sixteenth diagnostic then turns that into a predictive test rather than another descriptive split. It trains tiny decision trees on the raw sweep features and evaluates them with leave-one-mode-out generalization.
- That is the right next step because it asks whether the learned invariants actually predict the empty/single/multi regime on held-out modes better than roughness alone, instead of only sorting already-observed cases after the fact.
- In `compact`, roughness-only is still the best of the original named trees at `0.46` leave-one-mode-out accuracy, ahead of `mixed` at `0.44` and `invariant-only` at `0.43`.
- In `extended`, roughness-only and `mixed` tie at `0.59`, both ahead of `invariant-only` at `0.51`.
- So the present invariant bundle is explanatory but not yet the best predictive compression.
- A seventeenth diagnostic then removes the last hand-picked-feature cheat in that predictive test. Instead of privileging the current invariant bundle, it exhaustively searches all raw 1-, 2-, and 3-feature subsets from the same mode sweep.
- That search changes the story in a useful way. In `compact`, the best subset is `turning_points + crosses_midline` at `0.56`, which beats roughness-only. In `extended`, several simple summaries tie at `0.59`, including `center_range`, `center_variation`, and `max_step_fraction`.
- So roughness is not uniquely load-bearing in the predictive sweep. The cleaner current claim is that the original invariant bundle was incomplete: smaller raw subsets can beat or match roughness once the feature search is no longer hand-picked.
- An eighteenth diagnostic then asks whether those new best subsets are actually stable across held-out modes or only look good in the aggregate sweep.
- In `compact`, there is no repeat fold winner at all: each held-out mode picks a different 2-feature subset.
- In `extended`, the fold winners narrow to a 2-way split: `center_range` wins `2/4` held-out modes and `center_variation` wins the other `2/4`.
- So the predictive lift now looks real, but it still comes from a small family of simple geometry summaries rather than one locked minimal law.
- A nineteenth diagnostic then asks the harder transfer question: train those same geometry predictors on the full mode sweep, then test them unchanged on the roughness sweep and the independently generated procedural family at `w = 1.0`.
- That reverses part of the in-family story. In `compact`, roughness-only transfers best with mean accuracy `0.77`, including perfect accuracy on the roughness family itself, while the in-family winner `turning_points + crosses_midline` drops to `0.40`.
- In `extended`, roughness-only and `mixed` tie for best transfer at `0.56`, while the in-family best subset `center_range` falls to `0.50`.
- So the current out-of-family read is narrower and better: some of the extra in-family predictive lift was mode-family-specific, while roughness-like summaries are the most transfer-stable predictors found so far.
- A twentieth diagnostic then turns that into a selector-free predictor map. It scores every raw `1..3` feature subset by both mode-sweep CV and out-of-family transfer, then keeps only the nondominated subsets.
- In `compact`, the raw fronts contain `7` balanced and `5` transfer subsets, but those compress to `5` distinct predictor behaviors. Roughness-only sits on both fronts. The high-CV `turning_points + crosses_midline` rule stays on the balanced frontier, but not the transfer frontier.
- In `extended`, the raw fronts contain `11` balanced and `16` transfer subsets, but they compress to just `2` distinct behaviors. That means most of the raw frontier count was redundant supersets of the same roughness-style split.
- So the current best predictor-level claim is no longer “this one subset wins.” It is: roughness-like summaries are structurally stable across transfer, while some non-roughness summaries still survive on the balanced frontier because they trade stronger in-family fit for weaker transfer.
- A twenty-first diagnostic then removes another modeling choice: fixed tree depth. The same predictor Pareto map is recomputed at depths `1`, `2`, and `3` on the same mode/roughness/procedural datasets.
- Depth changes the balanced-frontier story a lot. In `compact`, the compressed frontier shifts from `2` behaviors at depth `1` to `5` at depth `2` to `6` at depth `3`. In `extended`, it shifts from `2` to `2` to `3`, with zero exact overlap between depths `1` or `3` and the depth-2 reference.
- But the transfer-stable core is much steadier: roughness-only stays on both fronts at all tested depths in both families, and it remains the top transfer subset throughout.
- So the current strongest predictor claim is now quite specific: the in-family balanced frontier is depth-sensitive, but the roughness-like transfer-stable part of the predictor story survives this capacity ablation.
- A twenty-second diagnostic then changes predictor family instead of tree depth. It keeps the structurally relevant feature subsets fixed and compares the current depth-2 trees to a tiny ordinal score model on the same raw features.
- In `compact`, roughness-only remains top-tier under both predictor classes: it reaches mean transfer `0.77` as both a tree and an ordinal score model. Non-roughness subsets move much more; for example, `center_range + turning_points` jumps from `0.56` as a tree to `0.74` as an ordinal score model, while still not displacing roughness-only.
- In `extended`, roughness-only also stays at the top transfer tier under both predictor classes, at `0.56` as a tree and `0.56` as an ordinal score model. Some non-roughness alternatives fall off harder under the ordinal score model than they did under trees.
- So the transfer-stable core now survives both a depth ablation and a predictor-family swap. What remains fragile is the richer in-family tradeoff structure, not the roughness-like transfer winner.
- A twenty-third diagnostic then loosens the ordinal model itself. It keeps the structural subset set fixed, but varies the ordinal internals across `minmax/equal`, `zscore/equal`, and `minmax/spread`.
- In `compact`, roughness-only is extremely stable under those internal changes: all three variants keep the same mean transfer `0.77`.
- In `extended`, roughness-only also stays stable at `0.56`, but it is no longer unique. A spread-weighted `center_variation + center_range` score rises to `0.62`, which beats the roughness-only ordinal score.
- So the current predictor claim needs one more refinement: the transfer-stable core is not just one roughness-only rule. It now looks like a small roughness-centered family, especially in `extended`, where a roughness-plus-range score can outperform the simpler roughness summary inside the ordinal family.
- A twenty-fourth diagnostic then pushes on the graph-side cheat again with a multi-style generated-geometry ensemble: three whole-shape jitter variants plus one variant from each of three procedural generator styles per scenario, including a new graph-local morph generator.
- In `compact`, that stronger graph-side test no longer prefers roughness-only by itself. The best model becomes an ordinal `center_variation + center_range` score at mean `0.59`, while the roughness-only tree reaches `0.58`.
- In `extended`, the multi-style generated ensemble shifts the lead again: `crosses_midline` ordinal scores tie at mean `0.68`, while the roughness-only tree lands at `0.62` and a `span_range` tree joins the top tier.
- So the current graph-side read is tougher and more specific than before: the generated ensemble still does not preserve one unique predictor, but the stable family is clearer. Roughness alone is no longer the right summary; the recurring winners live in a small centerline-shape family built from roughness, range, crossing, and span summaries once the generator class changes.
- A twenty-fifth diagnostic then widens the predictor vocabulary itself on that same multi-style generated ensemble. It keeps the graph-side benchmark fixed but adds two cheap node-set features, `boundary_fraction` and `pocket_fraction`, so the model can use local-shape signals rather than only interval-profile summaries.
- In `compact`, that wider feature vocabulary does not dislodge the old family at all. The best model is still an old-vocabulary summary, `center_range + turning_points + crosses_midline`, at mean `0.63`.
- In `extended`, the new local-shape feature `pocket_fraction` becomes genuinely top-tier: ordinal `pocket_fraction` models tie the best old-vocabulary crossing models at mean `0.68`.
- So the current predictor-side read is asymmetric. The older centerline-shape family still carries the `compact` story cleanly, but the `extended` side was indeed hiding some local-shape signal. The right claim is now: the stable family is mostly centerline-shape based, but local pocket structure can become equally competitive on the harder generated geometries.
- The same generated-feature diagnostic then widens that local-shape family again by adding `boundary_roughness` and `deep_pocket_fraction`.
- That stronger local-shape sweep does not overthrow the previous result. In `compact`, the winner is still the same old-vocabulary summary, `center_range + turning_points + crosses_midline`, at mean `0.63`.
- In `extended`, `pocket_fraction` remains the simplest top-tier local-shape feature: `pocket_fraction` ordinal models still tie the best old-vocabulary crossing models at mean `0.68`, while the newer local-shape signals appear only in combinations.
- So the local-shape story is now cleaner: the old vocabulary was missing real signal, but `pocket_fraction` still looks closer to the underlying mechanism than a generic bag of nearby local-shape proxies.
- A twenty-seventh diagnostic then derives a tiny local-shape basis automatically from occupied-node neighborhood degrees, instead of hand-picking pocket-like summaries in advance.
- That learned basis does not replace `pocket_fraction`. In `compact`, the best learned-basis coordinate is `degree_8_fraction`, but it reaches only mean `0.45` versus `0.58` for single-feature `pocket_fraction`. In `extended`, the best learned single basis feature is `degree_7_fraction` at mean `0.67`, still below `pocket_fraction` at `0.68`.
- So the strongest current claim is sharper again: `pocket_fraction` does not look like an arbitrary hand-crafted proxy for a simpler degree-based coordinate. It still appears to capture something more mechanism-relevant than the tiny automatically derived neighborhood basis.
- A twenty-eighth diagnostic then asks the sharper residual question on a stronger generated-geometry ensemble: as the learned neighborhood basis grows, does `pocket_fraction` still add anything once the automatic basis is allowed to catch up?
- That answer is now asymmetric. In `extended`, a learned degree basis reaches exact parity with `pocket_fraction` by basis size `5`: `degree_2_fraction` under an ordinal `zscore/equal` score hits the same `0.67 / 0.63` generated mean/worst accuracy, and adding `pocket_fraction` back gives no further gain.
- In `compact`, the learned basis trails `pocket_fraction` clearly through basis sizes `3..6`, then first reaches parity only at basis size `7` on `degree_2_fraction`, with basis size `8` also matching on `degree_1_fraction`. Before that threshold, the best combined `pocket + basis` rows help, but they still do not fully close the gap.
- So the local-shape claim is narrower and better now: `pocket_fraction` is not irreducibly special, but it is also not a trivial tiny-basis proxy. On the current stronger generated ensemble it behaves like a compressed summary that a very small learned neighborhood basis cannot match, especially in `compact`, even though a large enough learned degree basis eventually can.
- A twenty-ninth diagnostic then widens the automatic basis itself. Instead of only degree fractions, the learned basis can now also use richer local motifs such as pocket-adjacent wall counts, high-degree-neighbor fractions, and simple 2-hop neighborhood summaries, still without being handed `pocket_fraction` directly.
- That changes the compact-side story a lot. With the richer automatic basis, `compact` reaches exact parity with `pocket_fraction` already at basis size `3`: `motif_high_degree_neighbor_fraction` under an ordinal `zscore/equal` score matches the same `0.63 / 0.59` generated mean/worst accuracy, and the best combined `pocket + basis` row does not improve the mean score.
- `Extended` still reaches parity at basis size `5`, but the learned coordinate shifts too: `motif_high_degree_neighbor_fraction` now ties the `pocket` score at `0.67 / 0.63`, while `motif_deep_pocket_adjacent_fraction` is already essentially tied at smaller basis sizes.
- So the revised mechanism claim is sharper and more interesting: the old `compact` threshold of `7` was a degree-basis artifact, not a real need for a wide learned basis. Once the automatic basis can express richer local motifs, the `pocket` signal collapses quickly into a very small learned coordinate set.
- A thirtieth diagnostic then ablates those richer motif families directly.
- That ablation is quite sharp. Removing every richer motif restores the old degree-only story immediately: `compact` parity drops back to basis size `7`, while `extended` stays at `5`.
- But removing the motif families one at a time shows they are not equally important. Removing pocket-adjacency motifs does not hurt `compact` at all and actually brings `extended` parity forward to basis size `3`. Removing neighbor-moment or 2-hop motifs also leaves `compact` parity at `3`.
- The genuinely load-bearing family is local degree extremes. When `motif_low_degree_neighbor_fraction` and `motif_high_degree_neighbor_fraction` are removed together, `compact` parity retreats to basis size `5`, and `extended` loses clean parity entirely within the tested `3..8` range.
- So the mechanism story is tighter again: the fast rich-basis collapse is not primarily about pocket-adjacency. It is mostly carried by local degree-extremes information, with pocket-adjacent motifs acting more like alternative proxies than the main driver.
- A thirty-first diagnostic then splits that degree-extremes family apart.
- That split is even cleaner. Removing only `motif_low_degree_neighbor_fraction` barely changes anything: `compact` still reaches parity at basis size `3`, and `extended` actually improves to basis size `4`.
- Removing only `motif_high_degree_neighbor_fraction` is the real hit. `Compact` parity retreats to basis size `6`, and `extended` loses clean parity entirely in the tested range, closely matching the stronger failure pattern from removing both degree-extreme motifs together.
- So the current mechanism claim is now quite specific: the rich-basis collapse is carried mostly by `motif_high_degree_neighbor_fraction`, while `motif_low_degree_neighbor_fraction` behaves more like a weak helper or redundant proxy.
- A thirty-second diagnostic then decomposes that high-degree motif into simpler primitives: neighbor-share-above-threshold, mean high-degree-neighbor count, max neighbor degree, and the full three-feature bundle.
- None of those primitive replacements preserve the fast collapse. Replacing `motif_high_degree_neighbor_fraction` with any single primitive pushes `compact` parity back to basis size `7`, and `extended` still has no clean parity in the tested `3..8` range.
- The strongest failure is actually the full replacement bundle: even the three primitive coordinates together do not recover clean parity in either family, with `compact` stuck below parity at `-0.05/-0.03` pre-threshold and `extended` still just below the line.
- So the mechanism claim sharpens again: `motif_high_degree_neighbor_fraction` is not just a trivial alias for one simpler local statistic. In the current generated-geometry benchmark it behaves like a genuinely compositional local-motif coordinate.
- A thirty-third diagnostic then sweeps the high-degree threshold itself, replacing `motif_high_degree_neighbor_fraction` with thresholded variants `ge_5`, `ge_6`, `ge_7`, and `ge_8`.
- The sanity check passes: `ge_7` reproduces the original result exactly, with `compact` parity at size `3` and `extended` parity at size `5`.
- The real mechanism result is narrower than “exactly 7+” and sharper than “any hub exposure.” `ge_6` also reproduces the original parity thresholds in both families, while `ge_5` only recovers the fast `compact` collapse and `ge_8` fails badly, pushing `compact` back to size `7` and losing clean `extended` parity entirely.
- Even the full threshold bundle does not improve that story: it recovers `compact` at size `3` but only reaches `extended` parity at size `6`, worse than the single `ge_6` or `ge_7` coordinates.
- So the current best mechanism claim is: the load-bearing signal is a near-hub neighborhood effect centered around degree thresholds `6..7`, not a generic high-degree average and not a requirement for fully maximal `8`-degree neighbors.
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
- The current robustness criterion is still hand-chosen too: `center gap`, `arrival span`, selector policy, and now even the choice of combined status observable materially affect which surviving branch wins on the same fixed candidate pool.
- The current perturbation ensemble is still a first pass: it uses only two deterministic graph nudges per scenario, tracks the unperturbed frontier palette instead of doing open-ended motif rediscovery on every perturbed graph, and only evaluates the strongest retained-weight point `w = 1.0`.
- The weight-robustness checks are still local: the current pairwise comparison uses only `w = 0.95` and `w = 1.0`, and the stronger ladder check only extends that to `w = 0.90, 0.95, 1.0`, so the model is still being tested in a narrow high-end band near the spent-delay point rather than across the whole retained-weight family.
- The random perturbation ensemble is also intentionally small and seeded: it currently samples only three random variants per scenario, and even the rediscovery-limit sweep only tests a small `0..3` band of extra locally rediscovered motifs, so it is still a first robustness probe rather than a large-scale random-graph study.
- The geometry-randomization layer is still narrow too: it only jitters contiguous column profiles with small deterministic shifts, so it is a first deformation test of the graph family rather than a broad random-geometry generator.
- The procedural graph generator is still very small and structured: it only produces smooth contiguous column profiles inside the existing bounding boxes, so it is a first independent-family probe rather than a general graph-generation study.
- The robustness sweep budget is also hand-chosen: smaller graphs, reduced rule families, and shorter persistence windows trade completeness for runtime.
- Complex amplitudes are still assumed rather than derived.
- Consciousness is still outside the simulation; only record formation is present.

So this prototype does not replace physics. It is a compact testbed for checking which parts of the ontology can already be realized with a simple discrete model, and which parts are still axioms wearing different clothes.
