# Physics Autopilot Handoff

## 2026-03-31 13:06 America/New_York

### Seam class
- generated-DAG field coupling
- last3 vs last6 sign-flip compare

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_late_support_flip_compare.py`
- wrote the paired flip compare to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-late-support-flip-compare.txt`
- isolated the exact retained question: among rows where `last3_union` already steers toward-source, what extra `last4-6` support makes `last6_union` flip back away?
- the paired counts are:
  - `76` rows with `last3_shift > 0`
  - `41` stable-toward under `last6_union`
  - `35` flip-to-away under `last6_union`
- broad direction is visible but not yet exact:
  - flip rows have somewhat larger added-support share (`0.3186` vs `0.2924`)
  - and a stronger extra fringe-side field gap (`0.0275` vs `0.0043`)
- but the smallest universal law is still open:
  - best discovery singles reach about `0.6286`, with the cleaner size/radius rules holding out only around `0.5854`
  - the best two-feature discovery rule does not transfer (`0.7143 -> 0.4634`)
- the effect is not owned by one config; flip rates stay in the `0.42..0.50` range across configs
- the widest mover-rule residual is on the `wide` branch (`14/24` flips)

### Current state
- this loop stayed strictly on the retained `last3_union` vs `last6_union` seam
- no broader source search or family widening was opened

### Strongest confirmed conclusion
The sign flip really does come from the added `last4-6` support, and the broad mechanism direction is now clearer: more added support and more extra fringe-side bias make away-shift more likely. But the smallest universal flip observable is still not closed on the pooled rows.

### Exact next step
- split the sign-flip compare by mover rule, starting with the noisier `wide` branch, and test whether the extra-support geometry closes more cleanly there than in the pooled aggregate

## 2026-03-31 12:15 America/New_York

### Seam class
- generated-DAG field coupling
- pattern-sourced footprint compression

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_field_bias_compare.py`
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_footprint_probe.py`
- wrote the bounded source-field compare to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-pattern-sourced-field-bias-compare.txt`
- wrote the bounded footprint sweep to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-pattern-sourced-footprint-probe.txt`
- the source-side result now closes much more cleanly:
  - raw source size / centroid placement still do not explain the split
  - the first retained local clue is weaker intended-side forward fringe bias (`forward_side_field_gap <= 0`)
  - the real selector is footprint width, not viability
- holding the same source rule, substrate, and coupling fixed:
  - `last_state`: mean signed shift `-0.3883`
  - `last2_union`: mean signed shift `+0.0947`
  - `last3_union`: mean signed shift `+0.7612` with `135/150` coherent survivors
  - `last6_union`: mean signed shift `-0.3947`
- so pattern-sourced steering does work on the coherent mover substrate, but only after compressing the source field to a recent three-step packet footprint

### Current state
- this loop stayed bounded to the retained mover substrate, retained coupling, and one source rule
- no broad source-rule hunt or graph-family widening was opened

### Strongest confirmed conclusion
The live bottleneck is now the sign flip between `last3_union` and `last6_union`. Pattern-sourced deflection on coherent movers is real, but broad late support over-broadens the field and turns attraction into away-shift / retiming.

### Exact next step
- compare the extra `last4-6` support added by `last6_union` beyond the retained `last3_union` footprint and isolate the smallest late-support observable that causes the steering sign flip

## 2026-03-31 11:59 America/New_York

### Seam class
- generated-DAG field coupling
- pattern-sourced mover probe

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_mover_probe.py`
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_source_geometry_compare.py`
- wrote the bounded pattern-sourced mover run to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-pattern-sourced-mover-probe.txt`
- wrote the source-geometry follow-up to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-pattern-sourced-source-geometry-compare.txt`
- the pattern-sourced replacement changes the steering story:
  - on the retained `neighbor_radius = 2.5` mover substrate, `150/170` coherent free-mover rows keep a viable late source union (`>= 3` nodes)
  - those viable-source rows still preserve coherence well: `135/150` survive, `15/150` diffuse, `0/150` die
  - but mean signed shift on the viable-source subset is `-0.3947`, so the net steering is away from the source side rather than toward it
- the source-geometry follow-up says this is not a simple misplacement issue:
  - both positive-shift and nonpositive-shift rows keep the source centroid on the intended side with forward lead
  - no single source-side scalar separates them much better than about `0.61` accuracy
- this means source viability is no longer the bottleneck; the active problem is compressing the broad late-phase source field into the smaller geometry that recovers toward-source steering

### Current state
- this loop stayed bounded to the retained mover substrate, retained coupling, and one source rule
- no broad new rule search or family widening was opened

### Strongest confirmed conclusion
Pattern-sourced coupling on coherent generated-DAG movers is now real but qualitatively different from the static proxy: it preserves the mover substrate while producing net away-shift on average.

### Exact next step
- find the smallest late-source observable or narrower source packet family that flips the current away-shift back to toward-source steering on the same `neighbor_radius = 2.5` mover substrate

## 2026-03-31 11:20 America/New_York

### Seam class
- generated-DAG field coupling
- coherent mover substrate probe

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_field_coupled_mover_probe.py`
- wrote the canonical coupled sweep to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-field-coupled-mover-probe.txt`
- the coherent mover substrate now survives a real field-coupling proxy:
  - retained coupling is `3.000`
  - `224/248` coupled trials remain coherent survivors, `18` diffuse, `6` die
  - mean signed toward-mass shift is `+0.9556`
  - the strongest steering lives on `neighbor_radius = 2.5` with mean signed shift `+1.1842`
- this is the first bounded result showing field-to-pattern coupling on movers rather than only on oscillators or dying packets

### Current state
- this loop stayed bounded to a static-mass proxy on the canonical mover substrate
- no broader rule sweep or fresh frontier growth was opened

### Strongest confirmed conclusion
Generated-DAG coherent movers are now a viable coupling substrate. A localized field can steer them without collapsing most packets.

### Exact next step
- replace the current hand-placed static mass with a pattern-sourced field and test whether one coherent mover or persistent source can deflect another coherent translating packet on the `neighbor_radius = 2.5` substrate

## 2026-03-31 11:05 America/New_York

### Seam class
- generated-DAG mover bridge
- packet-tracking regime compression

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_packet_tracking_bridge_compare.py`
- wrote the canonical mover compare to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-packet-tracking-bridge-compare.txt`
- the mover lane now has a retained two-stage packet bridge:
  - opening survival guard: `early_live_fraction >= 0.625 and early_front_load >= 1.447`
  - coherent-vs-diffuse splitter among live rows: `early_front_load >= 0.962 and early_band_share <= 0.776`
- holdout transfer stayed qualitatively intact on `wide-15` / `long-30`:
  - live-vs-die rule: `0.6889`
  - survive-vs-diffuse rule: `0.7857`
- abstractly this matches the current crosswalk vocabulary:
  - completion/load first
  - bottleneck second

### Current state
- this loop stayed on the canonical mover family rather than reopening broader rule or frontier growth
- the README now points the frontier toward field-to-pattern coupling on coherent movers

### Strongest confirmed conclusion
Generated-DAG mover outcomes are no longer just a loose motion taxonomy. The current retained law is: enough local forward packet load keeps the packet alive, and tighter forward-band concentration is what keeps the live packet coherent instead of diffuse.

### Exact next step
- test field-to-pattern coupling on movers that already satisfy the retained survival/load bridge, rather than on oscillators or dying packets

## 2026-03-31 10:30 America/New_York

### Seam class
- active problem compression
- regime architecture cleanup

### Science impact
- retained `/Users/jonreilly/Projects/Physics/scripts/geometry_regime_card.py` as the compact geometry-side card
- shortened the README `Active Technical Problem` so the repo now points at the shared mechanism-language task instead of older frontier-growth wording
- the active architecture now reads cleanly as:
  - geometry-side retained card
  - generated-DAG detector-balance bridge
  - domain guards and branch selectors

### Current state
- no new scan or frontier widening was run in this follow-on step
- this completed the immediate cleanup left by the prior geometry-card checkpoint
- canonical `main` / `origin/main` were synced at `4c51805` before these local write-ups

### Strongest confirmed conclusion
The current science phase is now correctly framed as regime compression and transfer language, not deeper ladder archaeology.

### Exact next step
- the next bounded move is a confirmation-style holdout pass on the retained architecture: test whether the generated-DAG completion/load floor plus balance split survives on held-out rows without adding new clauses

## 2026-03-31 04:42 America/New_York

### Seam class
- geometry regime card
- shorter retained architecture map

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/geometry_regime_card.py`
- wrote the compact geometry-side card to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-geometry-regime-card.txt`
- the retained geometry architecture is now explicitly the shorter four-step map:
  - support-collapse guard
  - subcritical balance basin
  - supercritical completed-packet regime
  - exhausted-wall boundary
- this now matches the generated-DAG bridge and the mechanism crosswalk in ordering and vocabulary:
  - completion/load sets the floor
  - balance selects the branch
  - bottleneck/placement sharpens the boundary

### Current state
- cooperative lock is held by the manual Codex worker for this bounded write-up
- canonical `main` / `origin/main` are synced at `4c51805` before this uncommitted local checkpoint
- no new scan or frontier widening was run; this loop was pure architecture compression

### Strongest confirmed conclusion
The geometry-side regime map is now short enough to serve as one retained card rather than a pile of legacy bounded-comparison prose.

### Exact next step
- if continuing this lane, shorten the `Active Technical Problem` section so it points at the retained regime card and shared crosswalk instead of the old long-form basin wording

## 2026-03-31 04:35 America/New_York

### Seam class
- common mechanism crosswalk
- regime architecture compression across geometry and generated DAGs

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/mechanism_regime_crosswalk.py`
- rendered the retained crosswalk at `/Users/jonreilly/Projects/Physics/logs/2026-03-31-mechanism-regime-crosswalk.txt`
- the current common mechanism map is now explicit:
  - completion/load sets the regime floor
  - balance selects the near-floor branch or subbranch
  - bottleneck / placement terms modulate the readout
- retained axis mapping:
  - geometry `closure_load`, shared `8/12` packet completion <-> generated `center_balanced_log_paths`, `center_slit_load_retimed`
  - geometry `anchor_closure_intensity_gap`, `anchor_deep_share_gap`, `high_bridge_right_count` <-> generated `center_path_balance`, `center_balance_share`
  - geometry `mid_anchor_closure_peak` <-> generated `center_retiming_alignment`, `center_slit_share`

### Current state
- cooperative lock is held by the manual Codex worker for this bounded write-up
- canonical `main` / `origin/main` are synced at `90986f6` before this uncommitted local checkpoint
- no new generated-graph experiment was run; this loop stayed entirely on cross-domain mechanism compression

### Strongest confirmed conclusion
The geometry ladder and generated-DAG bridge are now written in one shared vocabulary. The retained common theme is: completion first, balance second, bottleneck terms third.

### Exact next step
- if continuing the architecture lane, shorten the geometry-side regime map itself by rewriting the moderate anchor-balance basin and beyond-ceiling packet regime into one tighter regime card

## 2026-03-31 04:25 America/New_York

### Seam class
- generated-DAG floor residual-pair stop-rule check
- final bridge compression guard

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generative_causal_dag_visibility_floor_residual_pair_compare.py`
- the remaining pair around the near-floor balance cut do not support another retained global clause
- the pair are opposite endpoint exceptions:
  - `default:63` is load-heavy and almost perfectly retimed despite weak balance-share
  - `denser-radius:86` has moderate balance but remains below the balanced-load floor
- the tempting pair-only exact closers do not generalize:
  - best non-floor pair separator: `center_upper_log_paths > 17.568570`
  - full-crossover accuracy only `0.7500`

### Current state
- cooperative lock is held by the manual Codex worker for this bounded write-up
- canonical `main` / `origin/main` are synced at `e49673c` before this uncommitted local checkpoint
- retained bridge language after the stop-rule check:
  - packet completion / closure-load sets the floor
  - balance decides near-floor crossover
  - no extra residual clause survives the pair check

### Strongest confirmed conclusion
The generated-DAG bridge is compressed enough for now. The residual pair is real, but not stable enough to justify one more global rule.

### Exact next step
- stop compressing this specific branch
- carry the retained packet-completion / balance crosswalk into the broader regime architecture work

## 2026-03-31 04:20 America/New_York

### Seam class
- generated-DAG balanced-load floor crossover compare
- geometry-language transfer compression

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generative_causal_dag_visibility_floor_crossover_compare.py`
- the within-family compare is now closed at `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generative-causal-dag-visibility-floor-crossover-compare.txt`
- the generated-DAG bridge should now be treated as a retained two-branch packet regime:
  - `center_balanced_log_paths` sets the balanced-load / packet-completion floor
  - near the floor, what moves rows across is balance rather than extra retimed slit load
- the key crossover fact is:
  - `default-high` crossover rows have slightly *lower* mean `center_slit_load_retimed` than `denser-low` crossover rows (`16.0984` vs `16.9372`)
  - but much *higher* mean `center_path_balance` (`0.4770` vs `0.1262`) and `center_balance_share` (`0.2376` vs `0.0588`)
- best residual cut:
  - `center_path_balance > 0.222271` at `11/12`
  - `center_balance_share > 0.133447` is essentially tied and is the cleaner physical summary

### Current state
- cooperative lock is held by the manual Codex worker for this bounded write-up
- canonical `main` / `origin/main` are synced at `e49673c` before this uncommitted local checkpoint
- the strongest compact bridge wording now is:
  - generated-DAG `center_balanced_log_paths` <-> geometry packet completion / closure-load
  - generated-DAG `center_path_balance` / `center_balance_share` <-> geometry bridge-balance / anchor-balance
  - retiming / slit-share as detector-side bottleneck modifiers

### Strongest confirmed conclusion
The generated-DAG bridge no longer needs to search for one magic scalar. The compact regime architecture is: packet completion sets the floor, and balance decides the near-floor crossover.

### Exact next step
- compare the single residual false-positive / false-negative pair around the near-floor balance cut
- if no tiny exact closer appears, treat the current bridge language as the retained result and move on

## 2026-03-31 04:11 America/New_York

### Seam class
- generated-DAG visibility family-regime compression
- bounded within-family compare after the initial bridge

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generative_causal_dag_visibility_family_regime_compare.py`
- the combined default + denser visibility family does not collapse to one cleaner universal scalar
- the retained map from `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generative-causal-dag-visibility-family-regime-compare.txt` is a genuine two-branch packet-completion regime:
  - split on `center_balanced_log_paths <= 17.671`
  - below the floor, `center_path_balance` is the better observable
  - above the floor, `center_balanced_log_paths` itself is the better observable
  - weighted split summary `0.3541`, better than the best combined single-scalar summary `0.2680`
- this is not just the scenario label:
  - low branch: `58 default + 6 denser-radius`
  - high branch: `6 default + 26 denser-radius`

### Current state
- cooperative lock is held by the manual Codex worker for this bounded write-up
- canonical `main` / `origin/main` are synced at `ed297ec` before this uncommitted local checkpoint
- generated-DAG compression now has three retained pieces on disk:
  - `/Users/jonreilly/Projects/Physics/scripts/generative_causal_dag_visibility_order_parameter_compare.py`
  - `/Users/jonreilly/Projects/Physics/scripts/generative_causal_dag_visibility_family_regime_compare.py`
  - the three March 31 generated-DAG visibility compare logs

### Strongest confirmed conclusion
Generated-DAG visibility is now best read as a two-branch detector-side packet-completion regime. The order parameter is not raw edge size, and it is not one magic local scalar either: balance leads below the balanced-load floor, and balanced slit-load leads above it.

### Exact next step
- stay on the current compression lane
- compare the crossover rows on either side of the `17.671` balanced-load floor to identify what concrete local packet feature moves a row between the balance-led and load-led branches

## 2026-03-31 03:52 America/New_York

### Seam class
- generated-DAG visibility order-parameter bridge
- bounded local-family vs raw-baseline compression

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generative_causal_dag_visibility_order_parameter_compare.py`
- the bounded default comparer at `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generative-causal-dag-visibility-order-parameter-compare-default.txt` shows the bridge is real: `center_path_balance` beats raw `edge_count` / `edge_density` on the combined `V(y=0)` / `mean_V` ranking
- the nearby denser-radius holdout at `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generative-causal-dag-visibility-order-parameter-compare-denser-radius.txt` keeps the same mechanism family but shifts the best member to `center_balanced_log_paths`
- this means the generated-DAG visibility spread currently compresses best as a small detector-side packet-completion family rather than as one universal raw-size scalar

### Current state
- cooperative lock is held by the manual Codex worker for this bounded write-up
- canonical `main` / `origin/main` are synced at `79e2dfc` before this uncommitted local checkpoint
- the only science files added in this loop are:
  - `/Users/jonreilly/Projects/Physics/scripts/generative_causal_dag_visibility_order_parameter_compare.py`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generative-causal-dag-visibility-order-parameter-compare-default.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generative-causal-dag-visibility-order-parameter-compare-denser-radius.txt`

### Strongest confirmed conclusion
Generated-DAG visibility is no longer compressed best by raw edge count or edge density. The best current mechanism language is detector-side packet completion, with a default balance-led branch and a nearby denser-radius balanced-load-led branch.

### Exact next step
- stay local and bounded
- compare the generated-DAG rows behind `center_path_balance` vs `center_balanced_log_paths` directly to see whether they collapse to one smaller shared observable or define a genuine two-branch regime

## 2026-03-30 20:02 America/New_York

### Seam class
- janitor reconciliation after synced dynamic-graph advance
- runtime handoff / narrative repair

### Science impact
- No new science was run beyond the cheap confidence gate.
- Canonical `main` / `origin/main` are synced at `712d44f`, which adds `/Users/jonreilly/Projects/Physics/scripts/generative_causal_dag_interference.py` and shows that a randomly generated causal DAG can produce `V(y=0)` up to `0.988188` while the no-barrier control stays exactly `0.000000`.
- This loop repaired the stale runtime-only handoff, corrected the work-log drift that still pointed at the already-completed directed-graph follow-on, and refreshed `README.md` plus the tracked/runtime repo state to the actual synced head.

### Current state
- Cooperative lock held by `physics-janitor` during repair; no detached science child is active.
- `/Users/jonreilly/Projects/Physics/README.md`, `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, and this handoff now describe the same synced baseline.
- The shared science memory file could not be refreshed from this sandbox, so it still lags the repo state.
- `python3 scripts/base_confidence_check.py` passed; the base check again skipped the heavier full reruns by design.

### Strongest confirmed conclusion
The synced baseline now supports a tighter dynamic-graph statement: richer connectivity suppresses kinematic anisotropy roughly as `1/n_directions`, linear reversible propagation singles out Born's `p=2` norm, and once the graph is causally oriented it can generate high-visibility interference without a pre-built grid.

### Files/logs changed
- Updated narrative/runtime state:
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`

### Validation
- `python3 scripts/base_confidence_check.py`
- `git diff --check`

### Remaining review seams
- open: stay on dynamic-graph compression/order-parameter mode and explain what graph observable controls the seed-to-seed visibility spread on generated causal DAGs

### Exact next step
- Write one bounded comparer that relates generated-DAG visibility to post-barrier path multiplicity and detector-retiming proxies, then keep the cleanest scalar as the next order parameter.

## 2026-03-30 19:19 America/New_York

### Seam class
- repo-state reconciliation after multi-commit science burst
- gravity / kinematics physical-language sync

### Science impact
- no new analyzer was run; this loop synced the work log, README, handoff, and automation memory to the current canonical repo state
- the canonical science state now reflects: fixed-DAG interference is Born-like, topology-changing record operators can reshape visibility, the default self-maintenance rule is oscillatory rather than fixed-point, oscillating persistent sources still bend trajectories, the tested gravity field does not superpose linearly, and the retained update `sqrt(dt^2-dx^2)` is the exact tested Lorentz / proper-time scalar
- the older “finite-range gravity confirmed” wording has been retired; the gravity asymptotic law is still unsettled

### Current state
- Passed the duplicate-run guard, acquired the `physics-science` lock, and found canonical `main` synced with `origin/main` at `2849c57`.
- `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` were stale against the committed repo state, while `README.md` already carried newer untracked conclusion updates.
- This loop performed the repo-facing integrity reconciliation only; no detached child is active.
- Lock status:
  - held by `physics-science` during write-up
  - no detached child active

### Strongest confirmed conclusion
The toy's kinematics and gravity dynamics now separate more cleanly: `sqrt(dt^2-dx^2)` is an exact tested Lorentz / proper-time scalar, while gravity is a genuinely nonlinear continuation effect whose two-source combination fails simple superposition by about `48..52%`, and whose large-grid asymptotic law is still unresolved.

### Files/logs changed
- Updated narrative/state:
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Validation
- `git diff --check`

### Remaining review seams
- open: translate the two-source gravity nonlinearity into retained-update / proper-time language instead of leaving it as separate empirical field and path-optimization failures

### Exact next step
- Stay on the gravity / kinematics translation thread.
- Write one bounded analyzer that evaluates single-mass and two-mass trajectories on matched fixed paths and compares retained-update accumulation, raw delay accumulation, and action deviation.
