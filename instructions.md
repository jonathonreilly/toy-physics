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

1. `g_bare = 1`
   - the current argument fixes the coefficient of the nearest-neighbor
     Hamiltonian / hopping term
   - that may still be only a normalization or units choice
   - it is not yet shown to be invariantly the same physical coupling that
     later enters annihilation / relic calculations
2. relic-ratio / cosmology cancellation bridge
   - no hardcoded `True`
   - no “pure graph theory / zero imports” rhetoric unless the cancellation is
     actually derived and checked
3. Boltzmann / Stosszahlansatz coarse-graining
   - improved, but still not yet automatically a theorem-grade first-principles
     bridge

**What counts as success**

- one authority note states exactly what is derived and what still uses
  coarse-graining
- the runner checks the bridge it claims to check
- no mismatch between note and runner

**What does not count**

- saying the Hamiltonian can be written with coefficient `1` in lattice units
  and calling that “physical `g_bare = 1`”
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

- low-energy continuum running
- `alpha_s(M_Pl)` chain
- lattice-to-continuum matching

**What counts as success**

- those three residuals are actually discharged, or
- the flagship note is made cleanly bounded with no over-closure rhetoric

**What does not count**

- saying the remaining steps are “just mathematics” unless the note/script
  actually closes them at the paper bar

### Target C: CKM / flavor

**Goal**

- close a real quantitative route or stop at one sharp bounded authority note

**Primary files**

- `docs/CKM_*`
- `scripts/frontier_ckm_*`

**Current blockers**

- Higgs `Z_3` universality at flagship bar
- ab initio coefficient / hierarchy closure

**What counts as success**

- real quantitative closure with note/script/packet aligned

**What does not count**

- route pruning alone
- bounded structural flavor patterns sold as a full CKM theorem

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
