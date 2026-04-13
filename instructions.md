# Claude Execution Instructions

**Date:** 2026-04-13  
**Branch:** `claude/youthful-neumann`

Read only these two files before working:

1. `instructions.md`
2. `review.md`

If any older note, packet, scorecard, or script conflicts with `review.md`,
`review.md` wins.

## Mission

Use Claude time only on the remaining live publication gates and on narrow
wording/package cleanup for already-retained lanes.

Codex handles:

- audit
- promotion
- paper authority
- publication package

## Where to land work

Land all real work here and push it:

- branch: `claude/youthful-neumann`
- remote: `origin/claude/youthful-neumann`

Do not leave real fixes only in local notes, packets, or scorecards.

## Current retained paper surface

These are already retained at the paper bar. Do not spend theorem time trying
to re-close them unless you are fixing stale wording.

- framework statement:
  - `Cl(3)` on `Z^3` is the physical theory
- weak-field gravity core:
  - Poisson / Newton chain
  - weak-field WEP
  - weak-field gravitational time dilation
- exact native `SU(2)`
- graph-first structural `SU(3)`
- anomaly-forced `3+1`
- retained `S^3` compactification / topology closure
- full-framework one-generation matter closure
- three-generation matter structure
- exact `I_3 = 0`
- exact CPT

## Remaining live publication gates

Only these three are still live flagship gates:

1. **DM relic mapping**
2. **Renormalized `y_t` matching**
3. **CKM / quantitative flavor closure**

## Non-negotiable paper caveats

These caveats must stay explicit in any honest flagship submission:

- individual fermion masses are **not** fully predicted from first principles
  - safe claim: retained matter structure and bounded hierarchy/flavor support
- the strong CP problem is **not** addressed
- `alpha_EM = 1/137` is **not** derived
- gravity is retained only on the weak-field surface
  - safe claim: Poisson / Newton core + weak-field WEP + weak-field time dilation
  - not safe: full nonlinear GR closure

## Important but not a flagship live gate

**Broad gravity beyond the retained weak-field core** is still bounded, but it
is no longer one of the three flagship live gates. Treat it as a companion
bundle:

- bounded:
  - conformal metric
  - geodesic equation
  - light bending
  - strong-field / frozen-star / echo package
- only work this lane if:
  - you are cleaning wording/package alignment, or
  - you have a genuinely new exact sub-theorem

## Framework-premise rule

Codex accepts the framework premise:

> We take `Cl(3)` on `Z^3` as the physical theory.

This can resolve artifact-vs-physical disputes. It is why generation closed.

It is **not** acceptable to reintroduce “the graph is physical” later as a
lane-specific rescue axiom to skip missing mathematics or physics.

## Exact work queue

### Target A: DM relic mapping

**Goal**

- close the relic bridge or leave one sharp bounded authority note

**Primary files**

- `docs/DM_CLEAN_DERIVATION_NOTE.md`
- `docs/DM_STOSSZAHLANSATZ_THEOREM_NOTE.md`
- `docs/DM_INVARIANT_BRIDGE_NOTE.md`
- `docs/DM_K_INDEPENDENCE_NOTE.md`
- `scripts/frontier_dm_stosszahlansatz.py`
- `scripts/frontier_dm_graph_native.py`
- `scripts/frontier_dm_k_independence.py`

**Current blockers**

1. direct observable route is not the same as relic closure
   - the new T-matrix / direct-observable notes correctly narrow the old
     “is `g_bare` the same coupling?” objection
   - if `sigma_v` is computed directly from `H`, that coupling-identity issue
     is mostly dissolved
   - that does **not** close the lane by itself because `R = Omega_DM/Omega_b`
     still needs the relic-ratio / cosmology bridge
2. relic-ratio / cosmology cancellation bridge
   - no hardcoded `True`
   - no “pure graph theory / zero imports” rhetoric unless the cancellation
     itself is actually derived and checked
3. Boltzmann / Stosszahlansatz coarse-graining
   - improved, but still not yet automatically a theorem-grade first-principles
     bridge
4. route discipline
   - if using a direct `H -> T -> sigma_v` route, keep the claim at the
     cross-section level unless the relic bridge is also discharged
   - if using a plaquette / coupling route, explain clearly why the
     Hamiltonian coefficient is part of the framework definition rather than a
     separately derived observable

**What counts as success**

- one authority note states exactly what is derived and what still uses
  coarse-graining
- the runner checks the bridge it claims to check
- no mismatch between note and runner

**What does not count**

- dissolving the old `g_bare` objection while leaving the relic bridge open
- calling cosmological cancellation exact without a real derivation check
- calling the whole lane “pure graph theory” while still using imported bridge
  structure

### Target B: Renormalized `y_t`

**Goal**

- either close the residual bridge or keep one sharp bounded authority note

**Primary files**

- `docs/YT_FLAGSHIP_CLOSURE_NOTE.md`
- `docs/YT_CL3_PRESERVATION_NOTE.md`
- `docs/RENORMALIZED_YT_THEOREM_NOTE.md`
- `scripts/frontier_yt_cl3_preservation.py`
- `scripts/frontier_yt_matching_coefficient.py`
- `scripts/frontier_yt_full_closure.py`

**Current blockers**

1. the new Wilsonian-EFT close-claim is stronger than the actual evidence
   - Feshbach projection is an exact QM identity, but the current note/runner
     only verify it on toy Hamiltonians, not on the actual `Cl(3)` / `Z^3`
     Hamiltonian
2. EFT/operator-identification gap
   - symmetry preservation plus generic EFT logic does not by itself prove that
     the actual low-energy effective theory is the exact SM matching surface
3. coefficient/physics hygiene
   - the current Wilsonian runner uses incorrect one-loop SM beta-coefficient
     bookkeeping (for example `b_2 = 10/3` instead of the SM `19/6` with three
     generations and one Higgs doublet)
   - until that is fixed, the closure claim is not publication-safe
4. the practical bounded pieces remain:
   - low-energy continuum running
   - `alpha_s(M_Pl)` chain
   - lattice-to-continuum matching

**What counts as success**

- the Wilsonian route is rebuilt on the actual lattice Hamiltonian with correct
  EFT bookkeeping, or
- the lane is kept sharply bounded with the residuals stated plainly, or
- the flagship note is made cleanly bounded with no over-closure rhetoric

**What does not count**

- saying “Feshbach projection exists for any Hamiltonian” and treating that as
  proof of the actual SM low-energy bridge for this framework
- saying the remaining steps are “just mathematics” unless the note/script
  actually closes them at the paper bar

### Target C: CKM / flavor

**Goal**

- close a real quantitative route or stop at one sharp bounded authority note

**Primary files**

- `docs/CKM_*`
- `scripts/frontier_ckm_*`

**Current blockers**

1. Higgs `Z_3` universality is no longer the main conceptual blocker
   - the latest honest read is that the Higgs VEV is democratic, so the old
     universality obstruction should not be used as the primary stop sign
2. the real remaining blocker is quantitative closure
   - ab initio O(1) NNI / overlap coefficients are still not derived sharply
   - `V_cb` and `V_ub` remain off by factor-level errors
   - larger lattice compute or a real analytic overlap route is still needed

**What counts as success**

- real quantitative closure with note/script/packet aligned

**What does not count**

- route pruning alone
- bounded structural flavor patterns sold as a full CKM theorem
- saying the lane is “computational only” without also tightening the actual
  paper-safe bounded wording

### Target D: Broad gravity wording/package alignment only

**Goal**

- keep the retained gravity split honest and stable

**Primary files**

- `docs/GRAVITY_CLEAN_DERIVATION_NOTE.md`
- `docs/BROAD_GRAVITY_DERIVATION_NOTE.md`
- `docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`
- `scripts/frontier_broad_gravity.py`

**Current accepted split**

- retained:
  - weak-field Newton / Poisson
  - weak-field WEP
  - weak-field time dilation
- bounded:
  - conformal metric
  - geodesic equation
  - light bending
  - strong-field

**Required wording**

- `L^{-1} = G_0` is the framework’s closure condition for self-consistency
- it is not a theorem of pure algebra with zero remaining premise
- finite-lattice profile checks stay bounded even when they support a retained
  theorem path

## Status-alignment rule

For any lane you touch:

1. note
2. script
3. packet

must say the same thing.

If they disagree, the lane is not closed.

For `S^3`, the retained closure now lives in the theorem-note + accepted
topology-infrastructure chain. The computational runners are supporting
evidence, not the whole closure by themselves. Do not rely on runner headers
alone as the closure authority.

## Non-authority docs

Do not use these as closure authority if they outrun `review.md`:

- stale review packets
- scorecards
- pitch decks
- `*_FULL_CLOSURE_*` notes that overstate status

## Current execution summary

- `S^3` is closed
- the remaining flagship live gates are:
  - DM relic mapping
  - renormalized `y_t`
  - CKM
- broad gravity beyond the retained weak-field core is still bounded companion
  work, not a live flagship gate
