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

## Scope rule

Everything outside the three live gates is out of scope unless Codex
explicitly asks for wording/package alignment.

If Codex explicitly asks for gravity companion cleanup, do **not** try to
promote broad gravity. The only acceptable work is to remove stale promotion
language. Exact blockers to gravity-companion promotion:

1. strong-field package
   - zero-echo amplitude is **not** theorem-grade while it still depends on
     the unresolved strong-field metric between `R_min` and `R_S`
   - “no singularity” must **not** be promoted beyond the current Hartree /
     collapse-floor support
2. broad eikonal package
   - geodesic equation remains conditional on the smooth-metric / continuum
     identification
   - conformal metric remains conditional on the same identification
   - factor-of-2 light bending remains conditional on conformal metric +
     null-ray identification
3. paper-safe gravity surface remains only:
   - Poisson / Newton weak-field core
   - weak-field WEP
   - weak-field time dilation

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
- do **not** assume the only remaining route is bigger lattice compute

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
3. current best reading of the gap
   - this is probably **not** “derive every overlap coefficient at `L >= 32` or fail”
   - the strongest exact formulas already put `V_cb` close to PDG if the
     residual `2-3` asymmetry is only modest
   - the high-value target is the **ratio / asymmetry** controlling `c_23^u/c_23^d`,
     not the absolute coefficients by brute force

**Preferred execution routes**

1. exact `V_cb` route from the full `2-3` NNI formula
   - stop leaning on the crude linear `m_s/m_b - m_c/m_t` estimate as the main
     quantitative route
   - work from the full `2x2` `2-3` block diagonalization with
     `c_23^u`, `c_23^d`, and `delta_23` explicit
   - prove that only a modest `O(10%)` asymmetry is needed to land near PDG

2. derive the **ratio** `c_23^u/c_23^d`, not the absolute coefficients
   - factor the coefficient into common lattice overlap times sector-dependent
     EW / radiative weighting
   - if the common overlap cancels, the remaining up/down asymmetry may be
     derivable without cluster-scale production
   - this is the best current non-cluster route

3. close `V_ub` analytically from NNI + `c_13` suppression
   - use the already-retained structural `c_13` suppression
   - test whether the framework implies up-sector dominance for the `1-3`
     rotation, giving `|V_ub| ~ sqrt(m_u/m_t)` or the equivalent exact NNI
     asymptotic

4. use CKM invariants rather than raw overlap amplitudes
   - if `V_us` is sharp and `V_ub` can be sharpened, use the derived phase scale
     and Jarlskog/invariant relations to solve for `V_cb`
   - do not import PDG angles for this route

5. cluster-compute fallback
   - only fall back to `L >= 32` / dynamical overlap production if the ratio /
     invariant routes fail cleanly

**Routes to stop overusing**

- do not keep presenting “needs more compute” as the only path without first
  exhausting the ratio / invariant routes
- do not chase Higgs `Z_3` universality as the main blocker
- do not spend time deriving all four absolute NNI coefficients if a sharp
  `c_23^u/c_23^d` or invariant route can close the lane sooner

**What counts as success**

- real quantitative closure with note/script/packet aligned
- or a clear proof that the remaining obstacle is specifically the unresolved
  `c_23^u/c_23^d` asymmetry / invariant input, not a vague “more compute”

**What does not count**

- route pruning alone
- bounded structural flavor patterns sold as a full CKM theorem
- saying the lane is “computational only” without also tightening the actual
  paper-safe bounded wording

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

- only report on:
  - DM relic mapping
  - renormalized `y_t`
  - CKM
- everything else is out of scope unless Codex explicitly asks for cleanup
