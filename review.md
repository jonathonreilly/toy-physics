# Review: monday-koide

Branch reviewed: `origin/monday-koide` at `302cd9e3`

Decision: not safe to land as a retained theorem.

V7.3 is materially better than the previous version: it demotes the unconditional `KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE` flag to a conditional closeout, admits that CD/CRIT are support/criterion notes on main, and embeds the downstream algebra instead of citing those notes as authority. The remaining blocker is narrower but still load-bearing: the branch still promotes the physical source-selection premise from "open" to "retained" by asserting that OP locality plus retained three-generation structure forces a C3-fixed onsite scalar source.

The runner passes (`TOTAL: PASS=56 FAIL=0`), but the pass set certifies downstream algebra after the disputed `J=sI` source choice is imposed. It does not verify that retained charged-lepton physics forces that source/readout choice.

## Blocking Findings

### [P0] Source-domain promotion still assumes the missing physical-selection theorem

File: `docs/KOIDE_Q_NATIVE_CLOSURE_VIA_OBSERVABLE_PRINCIPLE_LOCALITY_THEOREM_NOTE_2026-04-27.md`, lines 5-17

The note now scopes the final `Q = 2/3` closeout as conditional, but it still labels the underlying source-domain result as a retained promotion theorem. The retained authorities establish local scalar projectors and a three-generation matter structure; they do not by themselves prove that the physical charged-lepton scalar source/readout must be the strict onsite C3-fixed grammar rather than a broader projected source grammar. That missing source-selection theorem is the same residual the support/criterion notes left open, so the promotion remains too strong for main.

### [P0] C3-invariance of the physical undeformed source is asserted at the decisive step

File: `docs/KOIDE_Q_NATIVE_CLOSURE_VIA_OBSERVABLE_PRINCIPLE_LOCALITY_THEOREM_NOTE_2026-04-27.md`, lines 238-244

The derivation moves from OP-local onsite sources `diag(j_1,j_2,j_3)` to C3-invariant physical undeformed sources and then concludes `j_1=j_2=j_3`, hence `J=sI`. That invariance condition is not an algebraic consequence of locality; it is an additional physical-source selection rule. Without an independent retained theorem that the charged-lepton undeformed readout must preserve the generation-cycle symmetry in this way, the downstream `z=0` result remains conditional on the source choice.

### [P1] The runner proves the conditional algebra, not the physical source selection

File: `scripts/frontier_koide_q_native_closure_via_observable_principle_locality.py`, lines 317-367

The replay constructs the onsite diagonal source, imposes C3 invariance to get `J=sI`, projects that scalar into the two isotype channels, and obtains `z=0`. Those checks are clean, but they start exactly after the disputed physical premise has been inserted. The runner therefore certifies "if `J=sI`, then `z=0`, hence `Q=2/3`", not "retained charged-lepton physics forces `J=sI`".

## Merge-Hygiene Blocker

The branch is also stale relative to current `origin/main`. A direct merge of `origin/monday-koide` would delete the active open-science lane package and the recently landed EW lattice cos-squared complement theorem/runner/log:

```text
D docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md
D docs/lanes/open_science/README.md
D docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md
D docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md
D docs/lanes/open_science/03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md
D docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md
D docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md
D docs/lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md
D docs/EW_LATTICE_COS_SQ_THETA_W_COMPLEMENT_BRIDGE_THEOREM_NOTE_2026-04-26.md
D scripts/frontier_ew_lattice_cos_sq_theta_w_complement_bridge.py
D logs/retained/ew_lattice_cos_sq_theta_w_complement_bridge_2026-04-26.log
```

Any resubmission needs to be rebased or selectively ported onto current `origin/main`.

## What Is Landable

The branch has useful support material if reframed:

- A support note may state: OP-local onsite sources plus an added C3-fixed physical undeformed-source selection imply `J=sI`.
- The embedded algebra may then show: `J=sI` projects to equal `(P_+,P_perp)` channel sources, gives `z=0`, and yields `Q=2/3` on the CRIT carrier.
- The runner may remain as a conditional verifier with flags such as `KOIDE_Q_CONDITIONAL_ON_C3_FIXED_SOURCE=TRUE`.
- The note should not claim `CD_PHYSICAL_PREMISE_DERIVED_FROM_R1_PLUS_R2=TRUE` or `CRIT_PHYSICAL_PREMISE_DERIVED_FROM_R1_PLUS_R2=TRUE` as retained conclusions.

## Resubmission Target

To become theorem-grade, the next version needs an independent retained proof of the physical source-selection rule:

```text
retained charged-lepton physical readout
  => undeformed scalar source must be strict onsite and C3-fixed
  => J = sI
```

Until that theorem exists, V7.3 is best tracked in the charged-lepton mass/Koide open lane as conditional support evidence, not landed as retained native Koide closure.
