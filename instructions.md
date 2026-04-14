# Claude Execution Instructions

**Date:** 2026-04-14  
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

## Deferred backlog after the 3 live gates

Do **not** work these until DM, `y_t`, and CKM are actually closed or Codex
explicitly reprioritizes them.

These are honest framework limitations to acknowledge and, only later, attack:

1. **Individual fermion masses not fully predicted**
   - safe current claim:
     - hierarchy structure is derived
     - one heavy / two lighter family structure is in
     - top mass has a bounded quantitative route
   - not yet derived:
     - `m_e`, `m_mu`, `m_u`, `m_d`, `m_s`, `m_c`, `m_b` individually
   - if worked later:
     - treat this as a post-flagship flavor-completion program, not as a
       hidden promise in the current paper

2. **`alpha_EM = 1/137` not derived**
   - safe current claim:
     - `sin^2(theta_W) = 3/8` at unification is structural
     - low-energy value uses running / threshold structure
   - not yet derived:
     - the absolute electromagnetic coupling itself from the lattice
   - if worked later:
     - attack this as a genuine lattice normalization / coupling-selection
       problem, not as a minor afterthought

3. **Strong CP problem untouched**
   - safe current claim:
     - the framework currently has no explanation for `theta_QCD = 0`
   - if worked later:
     - this is a separate program, not a cleanup note

4. **Full nonlinear GR not derived**
   - safe current claim:
     - gravity is deferred from Claude gate work
   - not safe:
     - full nonlinear GR in full generality
   - if worked later:
     - attack this as a separate gravity-completion lane after the flagship
       three gates are done

## Non-negotiable paper caveats

These caveats must stay explicit in any honest flagship submission:

- individual fermion masses are **not** fully predicted from first principles
  - safe claim: retained matter structure and bounded hierarchy/flavor support
- the strong CP problem is **not** addressed
- `alpha_EM = 1/137` is **not** derived
- full nonlinear GR is **not** a current Claude lane

## Scope rule

Everything outside the three live gates is out of scope unless Codex
explicitly asks for wording/package alignment.

Ignore gravity unless Codex explicitly reprioritizes it.

## Exact work queue

### Target A: DM relic mapping

**Goal**

- close the relic bridge or leave one sharp bounded authority note

**Primary files**

- `docs/DM_CLEAN_DERIVATION_NOTE.md`
- `docs/DM_RELIC_BRIDGE_NOTE.md`
- `docs/ETA_FROM_FRAMEWORK_NOTE.md`
- `docs/BARYOGENESIS_NOTE.md`
- `docs/EWPT_STRENGTH_NOTE.md`
- `docs/DM_STOSSZAHLANSATZ_THEOREM_NOTE.md`
- `docs/DM_INVARIANT_BRIDGE_NOTE.md`
- `docs/DM_K_INDEPENDENCE_NOTE.md`
- `scripts/frontier_dm_stosszahlansatz.py`
- `scripts/frontier_dm_graph_native.py`
- `scripts/frontier_dm_k_independence.py`
- `scripts/frontier_eta_from_framework.py`
- `scripts/frontier_baryogenesis.py`
- `scripts/frontier_ewpt_gauge_closure.py`

**Current blockers**

1. do **not** redo the pieces that are already in
   - `sigma_v` as a direct observable of `H` is already the right surface
   - `J_Z3`, `v(T_c)/T_c`, and `Gamma_sph/T^4` are already derived on the
     current branch
   - the invariant-bridge note correctly narrows the old normalization gap
   - the BBN/nuclear-physics objection is no longer the productive fight:
     `eta -> Omega_b` is counting once `m_p`, `G`, and `H_0` are taken from
     accepted framework authority
2. if you touch the BBN note or runner, keep the standard honest boundary
   - do **not** hardcode measured `m_p`, `G`, or `H_0` and label them
     `[DERIVED]` without pointing to the actual framework authority
   - the safe claim is: no nuclear reaction rates are needed for
     `eta -> Omega_b`
3. `L_w*T` is no longer the main blocker
   - the bounce / profile route is already the strongest transport sub-result
   - do **not** spend more time there unless you find a concrete bug
4. relic bridge is now:
   - numerator derived
   - baryogenesis chain structurally derived except for transport
   - the remaining live transport blockers are now:
     - imported `C_tr`
     - imported non-perturbative EWPT calibration entering `v(T_n)/T_n`
     - and therefore the still-unreconciled `eta` surface
5. Stosszahlansatz is now a strong sub-result, but not the full lane
   - do not keep re-fighting the same coarse-graining objection
   - the remaining issue is not “does factorization exist?” but “can the full
     relic bridge be closed without imported cosmology?”
6. the new Boltzmann-theorem path is useful, but not closure authority for DM
   - do **not** call the full relic mapping or `R = 5.48` a theorem from that
     note
   - the current script verifies the master-equation structure only on a small
     1D toy interaction model
   - the thermodynamic-limit and expansion pieces still lean on standard
     Riemann/Weyl/Newtonian-cosmology structure
   - treat it as a bounded Boltzmann-reduction strengthening, not as a
     replacement for the live `eta` / transport blocker
7. latest transport routes are stronger, but the lane is still not closed
   - `D_q*T`: the old Coulomb-log / inserted-`C_0` objection is mostly gone
     because the new native mode-sum script does compute the width directly on
     the lattice
   - but do **not** over-promote that to full transport closure yet
     - the computation is still a one-loop, static-screened transport solve
     - finite-`L` undersampling of soft modes is explicitly doing real work in
       the quoted value
     - so this is best treated as strong native bounded support unless you can
       remove the residual one-loop / static-screening dependence
   - `v_w` is improved, but it is not the only blocker anymore
     - the present route still leans on perturbative CW / bag-model driving
       pressure and earlier imported non-perturbative enhancements
   - so the transport sector is narrower, but not closed
8. the branch still contains an internal EWPT/baryogenesis regime mismatch
   - older notes still lean on a partial-washout window near `v/T ~ 0.5`
   - newer native EWPT work gives a strong first-order surface with
     `v(T_c)/T_c > 1`
   - do **not** promote DM until one authority note states clearly which of
     `v(T_c)/T_c`, `v(T_n)/T_n`, or wall-local `v/T` actually enters the
     baryogenesis source
9. bounded framework inputs still need honest handling
   - `g = 1` is still a framework-defining coefficient, not a theorem
   - `k = 0` remains bounded if used in Newtonian cosmology
   - no “zero imports / pure graph theory” language while transport formulas
     are still imported
10. the new taste-enhanced `eta` route is **not** closure authority
   - do **not** call DM closed by multiplying the already-bounded
     `eta_coupled` by `8/3`
   - the current note assumes the taste-trace enhancement propagates
     coherently through transport without re-solving the transport system
   - it leaves the imported `C_tr` calibration and imported
     non-perturbative `v(T_n)/T_n` calibration untouched
   - until the transport equations themselves are rebuilt with the explicit
     taste-enhanced source on the same native surface, this stays bounded

**What counts as success**

- best-case success:
  - derive `C_tr`, `v(T_n)/T_n`, `D_q*T`, and `v_w` from actual framework
    transport / EWPT dynamics
  - derive `eta` from the framework by closing the transport sector
  - then update the relic bridge note so `R` is genuinely parameter-free
- second-best success:
  - prove a tighter framework-internal `eta` window using the current
    transport ranges
  - and state the lane as “derived up to standard transport formulas” with no
    remaining ambiguity
- minimum acceptable success:
  - one authority note states plainly that the live blockers are imported
    `C_tr`, imported non-perturbative `v(T_n)/T_n`, and therefore `eta`
  - the note, runner, and packet stop pretending the lane is otherwise closed

**What does not count**

- dissolving the old `g_bare` objection while leaving the relic bridge open
- calling cosmological cancellation exact without a real derivation check
- calling the whole lane “pure graph theory” while still using imported bridge
  structure
- plugging framework couplings into AMY/Moore or Moore-Prokopec formulas and
  then calling the transport sector fully first-principles derived

**Preferred attack order**

1. first derive `T_n` from the existing effective potential + bounce machinery
   rather than scanning it
   - use the nucleation condition `S_3(T_n)/T_n ~ 140`
2. derive the wall-local CP source on the physical taste space directly
   - no post-hoc `8/3` multiplier on top of an already-bounded transport solve
3. derive the transport prefactor `C_tr` from the framework transport system
   instead of FHS calibration
4. rebuild `v_w` on one reconciled native surface:
   - native Daisy EWPT
   - native / HTL `D_q*T`
   - native bounce wall profile
   - no stale imported non-perturbative enhancement
5. solve the **coupled** transport fixed point instead of treating
   `D_q*T`, `v_w`, and `L_w*T` as independent knobs
6. only if there is real mathematical leverage, upgrade `D_q*T` beyond the
   present one-loop / static-screened surface
7. if 1-6 fail, freeze the lane honestly as “framework baryogenesis plus
   standard transport closure”
8. only then update `eta` and the full relic ratio

### Target B: Renormalized `y_t`

**Goal**

- either close the residual bridge or keep one sharp bounded authority note

**Primary files**

- `docs/YT_FLAGSHIP_CLOSURE_NOTE.md`
- `docs/YT_ZERO_IMPORT_CLOSURE_NOTE.md`
- `docs/YT_BOUNDARY_RESOLUTION_NOTE.md`
- `docs/YT_GAUGE_CROSSOVER_THEOREM.md`
- `docs/YT_MATCHING_NATIVE_NOTE.md`
- `docs/YT_VERTEX_POWER_DERIVATION.md`
- `docs/G_BARE_DERIVATION_NOTE.md`
- `docs/WILSONIAN_EFT_DERIVATION_NOTE.md`
- `docs/YT_MATCHING_COMPUTED_NOTE.md`
- `docs/YT_CL3_PRESERVATION_NOTE.md`
- `docs/RENORMALIZED_YT_THEOREM_NOTE.md`
- `scripts/frontier_alpha_s_determination.py`
- `scripts/frontier_zero_import_chain.py`
- `scripts/frontier_native_matching.py`
- `scripts/frontier_vertex_power.py`
- `scripts/frontier_yt_cl3_preservation.py`
- `scripts/frontier_yt_boundary_resolution.py`
- `scripts/frontier_yt_unified_boundary.py`
- `scripts/frontier_yt_gauge_crossover_theorem.py`
- `scripts/frontier_yt_matching_coefficient.py`
- `scripts/frontier_yt_matching_computed.py`
- `scripts/frontier_wilsonian_eft.py`
- `scripts/frontier_yt_full_closure.py`

**Current blockers**

1. the old toy-model / split-boundary objection is no longer the main fight
   - Feshbach is now verified on the actual staggered `Cl(3)` / `Z^3`
     Hamiltonian
   - `b_2 = 19/6` bookkeeping is corrected
   - the new zero-import route is the right live surface
   - do **not** spend more time re-litigating the already-fixed toy issues
2. do **not** redo solved sub-steps
   - `Cl(3)` preservation under RG is already the right surface
   - Feshbach on the actual Hamiltonian is already verified
   - the 1-loop bookkeeping bug is fixed
   - the lattice matching coefficient itself is already narrowed to
     sub-percent scale
3. electroweak inputs are no longer the productive objection here
   - do **not** spend time arguing that the lane is open merely because the
     scripts use electroweak inputs such as `v`, `sin^2(theta_W)`, or
     low-energy electroweak boundary data
   - on the current Codex-side paper surface, those are fair game
   - the remaining blockers are now the plaquette / LM methodology surface
     and the quantitative residual in the zero-import chain
4. the latest zero-import route is stronger, but it is still not closure
   - the newest flagship note still labels the lane **BOUNDED**
   - its zero-import result is:
     - `alpha_s(M_Z) = 0.1182`
     - `m_t = 165.4 GeV`
     - about `-4.2%` on `m_t`
   - do **not** promote `y_t` closed from that note
   - do **not** let older “CLOSED” `y_t` notes outrank that newer bounded
     authority
     - `YT_FLAGSHIP_CLOSURE_NOTE.md` and `YT_BOUNDARY_RESOLUTION_NOTE.md`
       contain stronger closure language than the current honest state
     - until they are rewritten onto one consistent surface, treat
       `YT_ZERO_IMPORT_CLOSURE_NOTE.md` plus the reviewed scripts as the safer
       authority
5. the plaquette objection is no longer the main blocker
   - `frontier_zero_import_chain.py` now computes the plaquette on the same
     surface via multi-`L` SU(3) Monte Carlo and uses the largest-`L` value as
     the authoritative input
   - the infinite-volume `0.5934` number is now comparison-only, not a
     load-bearing input
   - do **not** spend time reopening the old “hardcoded benchmark” objection
     unless the chain regresses
6. deriving `n_link(Pi) = 2` is real progress, but it is not the full closure
   - `frontier_vertex_power.py` does derive that the vacuum-polarization
     operator has 2 link insertions
   - but it still assumes the Lepage-Mackenzie rule that an operator with
     `n_link` gauge links uses `alpha_bare / u_0^{n_link}`
   - until that map itself is derived framework-natively, do **not** say the
     last prescription-level import is gone
7. `frontier_native_matching.py` no longer carries the older contradiction
   - the latest remote head now agrees that the vertex `u_0^2` prescription is
     being claimed as derived
   - the remaining issue is narrower: whether that derivation really internalizes
     the LM operator-to-coupling map, not whether the branch contradicts itself
8. the older gauge-crossover theorem is still bounded support, not closure
   authority
   - its exactness language around Feshbach-preserved gauge coupling and the
     projected Ward identity still outruns the current proof surface
   - do **not** cite it as an all-orders continuum matching theorem
9. the live blocker is now one narrow methodology / observable bridge
   - derive the map from operator link counting to the physical effective
     coupling on the framework surface
   - then rerun the zero-import chain on that derived prescription
   - only after that should you worry about squeezing the remaining `4.2%`
     `m_t` residual with improved running or thresholds
10. keep the authority surface single and current
   - after any new result, update or retract the stale `y_t` closure notes in
     the same change
   - do **not** let older closure-language notes outrank the newest bounded
     or corrected authority surface

**What counts as success**

- best-case success:
  - derive the LM link-counting rule itself on the framework surface, not
    just the `n_link = 2` count
  - rerun the zero-import chain from that cleaned-up boundary and close the
    `m_t` residual
- second-best success:
  - isolate the lane to the one remaining honest methodology import
    (the LM map from link count to physical coupling)
  - and state that plainly in one authority note
- minimum acceptable success:
  - keep the flagship note honest and bounded
  - and with the remaining blocker written as the LM methodology bridge, not
    as the old broad crossover story

**What does not count**

- re-proving Feshbach on toy systems
- presenting corrected beta coefficients as if that alone closes the lane
- calling the lane closed while the script that supposedly closes the last
  import still assumes the LM operator-to-coupling rule it claims to retire
- using agreement with PDG as proof that the methodology itself is derived

**Preferred attack order**

1. do **not** re-prove Feshbach or the sub-percent matching coefficient
2. do **not** spend more time on the old observed-seeded crossover complaint;
   the newest zero-import route is the right surface now
3. do **not** spend more time reopening the old plaquette-benchmark objection
   - the latest zero-import chain now uses same-surface multi-`L` Monte Carlo
     for the authoritative plaquette
4. attack the real remaining theorem:
   - derive why an operator with `n_link` gauge links uses the physical
     coupling `alpha_bare / u_0^{n_link}` on the framework surface
   - do **not** just recount the links again
5. then tighten the authority surface:
   - rewrite or retract older closure-language notes so they do not outrank the
     newest bounded authority
6. only after 4-5 are clean, rerun the zero-import chain and see whether
   the remaining `m_t` residual persists
7. if the residual still sits at a few percent, then and only then attack
   2-loop Yukawa running / thresholds as the remaining quantitative issue
8. if 4-7 fail, isolate exactly the one remaining methodology import and keep
   the lane bounded

### Target C: CKM / flavor

**Goal**

- close a real quantitative route or stop at one sharp bounded authority note
- do **not** assume the only remaining route is bigger lattice compute

**Primary files**

- `docs/CKM_*`
- `docs/CKM_FULL_CLOSURE_NOTE.md`
- `scripts/frontier_ckm_*`
- `scripts/frontier_ckm_full_closure.py`

**Current blockers**

1. Higgs `Z_3` universality is no longer the main conceptual blocker
   - the latest honest read is that the Higgs VEV is democratic, so the old
     universality obstruction should not be used as the primary stop sign
2. do **not** redo the solved structural pieces
   - the exact `2x2` `2-3` block diagonalization is already done
   - the ratio route `c_23^u/c_23^d` is already done
   - the full `3x3` NNI `V_ub` route is already done as a bounded result
3. the new Wolfenstein-cascade note is useful structurally, but it is **not**
   closure authority
   - lambda still uses an empirical `R_overlap = lambda_PDG / lambda_bare`
   - the absolute `c_23` scale still comes from `V_cb` matching
   - the phase sector still chooses `c_13 / c_23` by PDG-based optimization
4. the new full-closure script does **not** derive `V_cb`
   - it explicitly solves `c_23^d` by matching `V_cb` to PDG
   - do **not** cite that as a first-principles closure
5. the real remaining blocker is quantitative closure
   - absolute `c_23` / `S_23` normalization is improved but still bounded
     rather than theorem-grade
   - `c_13` suppression and phase control are still not jointly derived well
     enough for `V_ub` and `J`
   - the `J`-`V_ub` tension is reduced, not eliminated
6. current best reading of the gap
   - the new absolute-`S_23` route predicts `V_cb` within about `4.6%`
     without using PDG `V_cb`, which is real progress
   - but `K` still has `O(20%)` spread and a remaining EWSB sector correction,
     so the absolute normalization is not yet closed
   - the new `Z_3^3` phase work boosts `J` substantially, but the best current
     joint result still overshoots `V_ub` and undershoots `delta_CP`
   - invariants are still consistency checks, not closure
7. the new mass-basis NNI route is a bounded strengthening, not closure
   - it improves `|V_ub|` numerically by converting the Schur-complement
     result into the mass-eigenvalue NNI basis
   - but the current script still uses PDG quark masses directly and fitted
     geometric NNI coefficients from earlier bounded work
   - it does not derive the geometric coefficients or physical mass ratios on
     one common first-principles closure surface
   - and the phase sector is still open: `J`, `rho_bar`, and `eta_bar` remain
     far off

**Preferred execution routes**

1. exact `V_cb` route from the full `2-3` NNI formula
   - this step is already done; use it as the baseline and do not redo the
     old crude mass-ratio estimate work
   - the remaining task is not the formula, but the first-principles inputs
     to that formula

2. derive the **ratio** `c_23^u/c_23^d`, not the absolute coefficients
   - this step is also already done; use it and move on
   - do not spend more time re-deriving a 1-5% EW asymmetry unless you are
     materially changing the result

3. highest-value next route: derive the **absolute** `S_23` / `c_23`
   normalization analytically
   - do not treat cluster compute as the first choice
   - use the exact `V_cb` formula already on branch plus the sector-correction
     machinery
   - remove the residual sector-dependent `K` / EWSB correction without PDG
     back-calibration
4. derive `c_13` analytically from the full `3x3` NNI structure
   - Schur-complement / effective-mass-matrix route is preferred
   - do not treat PDG-anchored `V_ub` fits as closure authority
5. derive the mass-basis suppression from framework-derived mass ratios and
   framework-derived geometric coefficients, not PDG masses plus fitted
   coefficients
6. derive the surviving rephasing-invariant CKM phase from invariants built
   from the same EWSB-dressed mass matrices
   - do not use PDG-based `chi^2` optimization of `c_13 / c_23` as closure
7. multi-`L` ratio/normalization evidence is useful only as support for 3-6,
   not as a substitute for them
8. cluster-compute fallback
   - only fall back to targeted compute on one scalar quantity
     (`K_23` or physical `c_13`) if the analytic routes fail cleanly

**Routes to stop overusing**

- do not keep presenting “needs more compute” as the only path without first
  exhausting the analytic `S_23` / `c_13` / phase routes
- do not chase Higgs `Z_3` universality as the main blocker
- do not spend time deriving all four absolute NNI coefficients if `S_23`
  and `c_13` can close the lane sooner

**What counts as success**

- real quantitative closure with note/script/packet aligned
- or a clear proof that the remaining obstacle is specifically the unresolved
  absolute `S_23` / `c_13` / phase input, not a vague “more compute”

**What does not count**

- route pruning alone
- bounded structural flavor patterns sold as a full CKM theorem
- calibrating `c_23^d` from PDG `V_cb` and then calling `V_cb` derived
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
