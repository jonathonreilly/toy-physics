# Physics Autopilot Handoff

## 2026-03-31 18:56 America/New_York

### Seam class
- decoherence scaling interpretation repair

### Science impact
- repaired the measurement/interpretation layer for the recent scaling claims:
  - purity is detector-conditioned purity, not full-state purity
  - size sweeps now compare fixed vs depth-scaled environment regions
  - cumulative env is now a genuine fixed-bin register test
  - evolving env is now labeled honestly as a discretized phase-bin test
- rerun result:
  - the wrong-way size trend survives
  - but it is now narrower than the earlier theorem-like wording
- retained numbers:
  - node-label detector-state purity rises `0.7060 -> 0.8858` with fixed env depth
  - and still rises `0.7060 -> 0.7944` when env depth scales with graph size
  - fixed-bin cumulative env stays near pure (`0.9896 .. 0.9827`)
  - discretized evolving env either stays pure or wrong-scales (`0.8067 -> 0.8509`)

### Strongest confirmed conclusion
The tested discrete environment architectures still fail to scale correctly on growing graphs, even after partially controlling for environment dilution. That keeps the non-unitary scaling law as the sharp frontier, but the repo should no longer describe this as a general proof that all finite-dimensional environments fail.

## 2026-03-31 17:39 America/New_York

### Seam class
- architecture reset
- adversarial critique / next-work plan

### Science impact
- no new measurement landed in this note; this is the current OPEX-facing reset after the harshest credible critique
- retained positive core:
  - corrected `1/L^p` propagator keeps the Born/interference package and fixes gravity sign
  - generated-DAG growth still creates the conditions for the retained unitary phenomena
  - two-register decoherence is now a real branch in the right post-barrier geometry, but it is tuned rather than generic
- retained critique:
  - several core ingredients are still selected rather than uniquely derived
  - the decoherence branch is geometry-sensitive and not structurally compressible by simple graph observables so far
  - no universal DAG force law or clean lensing law is retained
  - results that have not survived explicit code review or rerun should be treated as provisional by default
- current adversarial interest map:
  - toy-model mechanism interest: `10.0/10`
  - foundations / complex-systems / network-dynamics interest: `9.9/10`
  - broader theorist interest: `9.7/10`
  - bridge to known physics: `8.8/10`
  - publishable-as-foundational physics breakthrough: `8.2/10`
  - ready for top-tier mainstream physics claims: `4.6/10`

### Current state
- the project is no longer bottlenecked mainly by one more sweep
- the current bottleneck is architectural compression:
  - assumption ledger
  - claim ledger
  - explicit layer / coupling map
- the local manual workspace currently also has an uncommitted probe in:
  - `/Users/jonreilly/Projects/Physics/scripts/all_three_predictor.py`
  - this probe supports the stronger “phase-emergent, not simply structurally predictable” read and should not be confused with canonical `main` yet

### Strongest confirmed conclusion
The right current frame is not “finished theory.” It is: strong retained unitary core, real but tuned endogenous decoherence branch, and a sharper need to write down exactly what is assumed, what is retained, and what is still open.

### Exact next step
- while Claude continues the active science lane, keep OPEX in synthesis mode:
  - write the assumption ledger
  - write the claim ledger
  - freeze the architecture document
  - only reopen a compact predictor pass if it directly tests whether `ALL THREE` can be compressed by one mixed geometry-plus-phase feature
- after that, shift the default repo-facing work from mechanism hunting to thesis/paper packaging

## 2026-03-31 21:01 America/New_York

### Seam class
- generated-DAG field coupling
- live-window late-support geometry compare

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_live_source_window_geometry_compare.py`
- wrote:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-live-source-window-geometry-compare.txt`
- kept the source evolution fixed and widened only the live source window from `3` to `6` on the same paired tasks
- result:
  - `146` paired live-window rows
  - `last6` beats `last3` on `80/146`
  - mean shift moves from `-0.6000` to `+0.5040`
  - retained live `last6` subset is `52/146`
- the broad branch is real, but pooled closure is only moderate:
  - retained rows carry much more added field on the packet (`0.1006` vs `0.0249`)
  - best pooled rule: `extra_packet_side_gap <= -0.0080`
  - pooled accuracy: `0.7286` discovery / `0.6579` holdout
- the remaining split is mover-rule-local:
  - `self` carries most retained rows (`40/83`) but still has no strong local scalar (`0.6386`)
  - `wide` already tightens under `last6_corridor_share >= 0.7762` (`0.8113` local accuracy)

### Current state
- the broad live `last6` branch is now the retained source-side existence claim
- the residual question is inside mover-rule-local late-support geometry, not at the existence of live pattern-sourced steering itself

### Strongest confirmed conclusion
The field-to-pattern arrow is now stronger than a simple frozen-source surrogate claim. Broad live `last6` steering is real, and the main unresolved work is compressing its mover-rule-local residual, especially on `self`.

### Exact next step
- use `wide` as the clean control branch
- focus the next compression pass on the dominant `self` slice of the live `last6` branch

## 2026-03-31 18:08 America/New_York

### Seam class
- corrected-propagator decoherence
- measurement repair / rerun

### Science impact
- repaired four exposed issues in:
  - `/Users/jonreilly/Projects/Physics/scripts/two_register_decoherence.py`
  - `/Users/jonreilly/Projects/Physics/scripts/between_slit_decoherence.py`
  - `/Users/jonreilly/Projects/Physics/scripts/mass_scaling_momentum.py`
  - `/Users/jonreilly/Projects/Physics/scripts/constant_deflection_derivation.py`
- the main science change is on the endogenous node-env lane:
  - the earlier `D=0% at all connectivities` theorem-like read was an artifact of the shared env helper collapsing labels too aggressively plus a between-slit geometry that blocked the env-carrying mass nodes
  - after repair, the same family is weak but not zero:
    - downstream two-register: `G:3/12 I:12/12 D:4/12 ALL:1/12`
    - slit-adjacent mass: `G:8/12 I:12/12 D:1/12 ALL:1/12`
    - between-slit mass: `G:9/12 I:12/12 D:1/12 ALL:1/12`
    - connectivity trade-off: decoherence climbs to `50%` on the densest tested slice
- two supporting cleanups also matter:
  - generated-DAG `mass_scaling_momentum.py` now labels its DAG-side observable as detector-centroid shift, not `Δky`
  - `constant_deflection_derivation.py` now checks a real compact-source field profile and nonzero transverse gradient

### Current state
- the corrected unitary core remains intact
- the non-unitary side should now be read as:
  - weak, geometry-sensitive node-env decoherence exists
  - no retained strong endogenous all-three law yet

### Strongest confirmed conclusion
The node-environment architecture is not dead, but it is not the clean closure either. It survives only as a weak geometry-sensitive branch.

### Exact next step
- keep the unitary/non-unitary split
- remove the old universal-null theorem wording from any canonical summaries
- if the decoherence lane is reopened, treat node-env tagging as a weak surviving branch rather than as already exhausted

## 2026-03-31 16:56 America/New_York

### Seam class
- generated-DAG field coupling
- live-vs-frozen source compare

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_live_source_field_compare.py`
- wrote:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-live-source-field-compare-last3.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-live-source-field-compare-last6.txt`
- this is the first direct gap-3 compare between:
  - frozen recent source footprint
  - live sliding recent source footprint during the mover run
- current read:
  - on current code, frozen `last3` is no longer a positive retained steering branch (`mean_signed_shift = -0.0811`)
  - live `last3` weakens further (`mean_signed_shift = -0.5125`, paired mean delta `-0.4315`)
  - frozen `last6` is the current positive baseline (`mean_signed_shift = +0.4736`)
  - live `last6` survives in substance (`mean_signed_shift = +0.4420`, paired mean delta `-0.0317`)
- retained interpretation:
  - narrow recent-footprint steering still leans on the frozen-source surrogate
  - the broad current source branch already survives a stronger same-framework live-field version

### Current state
- this stayed on one bounded field-to-pattern gap question only
- the unrelated local `README.md` edit remains intentionally untouched

### Strongest confirmed conclusion
The field-to-pattern arrow is partly real already. The current broad `last6` source branch survives live regeneration in substance, but the narrower `last3` branch does not.

### Exact next step
- compare live `last6` positive rows against live `last3` failures and isolate what the broad branch retains that the narrow branch loses:
  - extra forward corridor support
  - extra field landing on the packet
  - or a broader retiming envelope

## 2026-03-31 16:34 America/New_York

### Seam class
- architecture audit
- axiom status matrix

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/model_axiom_audit.py`
- wrote the canonical audit to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-model-axiom-audit.txt`
- the repo now has one explicit zoom-out artifact with:
  - axiom status matrix
  - layer / coupling map
  - retained core vs provisional branches
  - top frontier gaps
- the retained architecture read is:
  - core retained sectors: Born-safe path-sum, corrected phase-driven gravity, shared completion/balance mechanism language
  - main weak arrows: graph growth generating more of the physics, durable endogenous records, full field-to-pattern coupling
  - latest decoherence merges sharpen the same split: the unitary sector is comparatively retained, while the non-unitary sector still lacks a retained endogenous mechanism
  - latest momentum-space merge sharpens the retained gravity side too: the current 2D momentum kick is now better read as log-field plus path averaging than as an unresolved artifact

### Current state
- this pass intentionally did not reopen a broad experiment search
- the unrelated local `README.md` edit remains intentionally untouched

### Strongest confirmed conclusion
The project is currently bottlenecked more by architectural clarity than by one more local sweep. The right next month-scale frontier is now explicit at the axiom/layer level, and the newest decoherence results reinforce that by constraining the current non-unitary side rather than expanding it.

### Exact next step
- use the audit to choose the next deep lane deliberately:
  - graph-growth-first generation of later physics
  - endogenous durable record formation
  - stronger shared field-to-pattern dynamics on the coherent mover substrate

## 2026-03-31 16:16 America/New_York

### Seam class
- generated-DAG field coupling
- residual mechanism card

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_residual_mechanism_card.py`
- wrote the retained card to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-pattern-sourced-residual-mechanism-card.txt`
- the mover-lane residual map is now explicitly compressed:
  - base viable source-driven substrate: `neighbor_radius = 2.5`, coupling `3.0`, `last3_union`
  - over-broad failure trigger: `last6_union`
  - shared abstract family: forward-packet retiming
  - retained residual branches:
    - `wide`: low added field reaching the packet
    - `self:sparse-25`: collapse of forward corridor / forward-side support

### Current state
- this step was architecture-only and did not reopen any search
- the unrelated local `README.md` edit is still intentionally untouched

### Strongest confirmed conclusion
The mover-lane residual architecture is now small enough to retain honestly: one shared forward-retiming family, two residual mechanisms, no fake universal late-support scalar.

### Exact next step
- treat the residual card as the stop-rule map and only resume local threshold work when a new experiment directly targets one retained branch

## 2026-03-31 16:10 America/New_York

### Seam class
- generated-DAG field coupling
- residual branch crosswalk compare

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_residual_branch_crosswalk_compare.py`
- wrote the residual branch crosswalk to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-residual-branch-crosswalk-compare.txt`
- the current wide and self:sparse-25 residuals do not reduce to one retained universal rule:
  - wide-local rule `extra_field_mean_on_packet <= 0.0010` transfers at only `0.2500` on `self:sparse-25`
  - self:sparse-25 local rule `extra_support_corridor_share <= 0.0000` transfers at only `0.4583` on `wide`
- pooled forward-family rules exist but stay weaker than the branch-local stories:
  - best pooled single: `extra_forward_side_gap <= -0.0001`, pooled `0.6562`
  - best pooled deficit-only OR: `extra_support_forward_share <= 0.1429 or extra_forward_side_gap <= -0.0001`, pooled `0.6875`
  - branch accuracies for that retained pooled deficit family: `0.6250` on `wide`, `0.8750` on `self:sparse-25`
  - the best unconstrained pooled OR reaches `0.7500`, but only by mixing opposite directions in a way that is not physically clean enough to retain
- retained read:
  - one shared abstract forward-packet-retiming family
  - two separate residual mechanisms inside it

### Current state
- this loop stayed strictly on the branch-crosswalk question
- the unrelated local `README.md` edit remains intentionally untouched

### Strongest confirmed conclusion
The mover-lane residual does not have one universal late-support law. The right architecture is:
- `wide`: low added field actually landing on the packet
- `self:sparse-25`: collapse of added forward corridor support / forward-side balance

### Exact next step
- write the compact residual-mechanism card for the mover lane so the repo retains the correct branch architecture before any more local threshold shaving

## 2026-03-31 15:40 America/New_York

### Seam class
- generated-DAG field coupling
- self sparse-25 config-local flip compare

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_config_local_flip_compare.py`
- wrote the sparse self slice to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-config-local-late-support-flip-compare-self-sparse-25.txt`
- the noisiest self config does tighten beyond the pooled self rule:
  - `8` retained rows total
  - `4` stay toward-source
  - `4` flip away under `last6_union`
- the pooled self separator only touches one row here:
  - `extra_packet_side_gap <= -0.0962` matches `1/8`
  - that one matched row flips, but it does not explain the whole slice
- the config-local slice is cleaner and more corridor-led:
  - stable rows keep far more added forward corridor support (`0.4527` vs `0.0439`)
  - flip rows carry stronger negative packet-side and fringe-side gaps
- the best config-local rules all tell the same story:
  - `extra_support_corridor_share <= 0.0000`
  - `extra_packet_side_gap <= 0.0000`
  - `extra_support_forward_share <= 0.1429`
  - each gives `0.8750` accuracy on the `8` rows

### Current state
- this loop stayed on the noisiest self residual slice only
- the unrelated local `README.md` edit remains intentionally untouched

### Strongest confirmed conclusion
The self residual compresses further on `sparse-25`: the sign flip there is best read as forward-corridor collapse, not just generic wrong-side packet bias.

### Exact next step
- compare the `wide` low-added-packet-field branch and the `self:sparse-25` corridor-collapse branch directly and test whether they are one smaller forward-packet-retiming language or two separate residual mechanisms

## 2026-03-31 15:14 America/New_York

### Seam class
- generated-DAG field coupling
- self-rule local sign-flip compare

### Science impact
- hardened `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_late_support_flip_compare.py` so sandboxed runs can fall back to serial execution instead of failing inside multiprocessing setup
- generalized `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_rule_local_flip_compare.py` so the interpretation text matches the selected target branch
- wrote the self-branch compare to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-rule-local-late-support-flip-compare-self.txt`
- the `self` branch does not reuse the `wide` late-support mechanism:
  - `39` retained rows total
  - `11` flip to away under `last6_union`
  - `28` stay toward-source
  - best retained self-local separator: `extra_packet_side_gap <= -0.0962` (`0.8235` discovery, `0.6818` holdout)
  - matched side: `2/3` flips with mean `last6_shift = -4.3651`
  - unmatched side: `9/36` flips with mean `last6_shift = +2.7135`
  - noisiest self config: `sparse-25` (`4/8` flips)
- physical read:
  - `wide`: extra support fails to land enough field on the packet
  - `self`: extra support lands too much field on the opposite packet side

### Current state
- no detached science child is running
- unrelated local `README.md` edits remain untouched

### Strongest confirmed conclusion
The late-support residual is mover-rule-local. `wide` and `self` need different physical language: `wide` is a low-added-packet-field branch, while `self` is a weaker wrong-side packet-field branch.

### Exact next step
- split the `self` branch by config, starting with `sparse-25`, and test whether negative packet-side gap closes more cleanly there than on the pooled self rows
- first concrete action: extend the rule-local compare with a config-local self summary and render the `sparse-25` self slice
