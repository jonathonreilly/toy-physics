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
     - weak-field gravity is retained
     - weak-field WEP and time dilation are retained corollaries
     - 1PN-style extensions may be useful bounded companions
   - not safe:
     - full Einstein-equation closure
   - if worked later:
     - attack this as a separate gravity-completion lane after the flagship
       three gates are done

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
- `docs/YT_BOUNDARY_RESOLUTION_NOTE.md`
- `docs/YT_GAUGE_CROSSOVER_THEOREM.md`
- `docs/G_BARE_DERIVATION_NOTE.md`
- `docs/WILSONIAN_EFT_DERIVATION_NOTE.md`
- `docs/YT_MATCHING_COMPUTED_NOTE.md`
- `docs/YT_CL3_PRESERVATION_NOTE.md`
- `docs/RENORMALIZED_YT_THEOREM_NOTE.md`
- `scripts/frontier_alpha_s_determination.py`
- `scripts/frontier_yt_cl3_preservation.py`
- `scripts/frontier_yt_boundary_resolution.py`
- `scripts/frontier_yt_unified_boundary.py`
- `scripts/frontier_yt_gauge_crossover_theorem.py`
- `scripts/frontier_yt_matching_coefficient.py`
- `scripts/frontier_yt_matching_computed.py`
- `scripts/frontier_wilsonian_eft.py`
- `scripts/frontier_yt_full_closure.py`

**Current blockers**

1. the old toy-model objection is mostly gone
   - Feshbach is now verified on the actual staggered `Cl(3)` / `Z^3`
     Hamiltonian
   - `b_2 = 19/6` bookkeeping is corrected
   - the V-scheme to `\\overline{MS}` conversion itself is a real step forward
   - do not spend more time re-litigating those fixed points
2. the new gauge-crossover diagnosis is the right blocker
   - the old split-boundary objection is narrower now: the script really does
     derive one framework coupling that sets both `g_3(M_Pl)` and `y_t(M_Pl)`
   - but the framework `alpha_s(M_Pl)` is about `4.4x` the perturbative SM
     value obtained by running observed `alpha_s(M_Z)` upward
   - running the framework coupling downward with perturbative QCD hits
     breakdown near `10^15.8 GeV`
   - so the remaining blocker is now a concrete non-perturbative gauge
     crossover / step-scaling problem, not a vague UV-boundary mismatch
3. do **not** redo solved sub-steps
   - `Cl(3)` preservation under RG is already the right surface
   - Feshbach on the actual Hamiltonian is already verified
   - the 1-loop bookkeeping bug is fixed
   - the lattice matching coefficient itself is already narrowed to
     sub-percent scale
4. electroweak inputs are no longer the productive objection here
   - do **not** spend time arguing that the lane is open merely because the
     scripts use electroweak inputs such as `v`, `sin^2(theta_W)`, or
     low-energy electroweak boundary data
   - on the current Codex-side paper surface, those are fair game
   - the remaining blockers are instead the strong-coupling normalization and
     crossover map
5. `alpha_s` itself is still not a zero-import standalone closure
   - `g_bare = 1` is still only **BOUNDED**, not theorem-grade exact
   - the current `alpha_s` runner still uses imported plaquette-to-`V` and
     `V`-to-`\overline{MS}` matching coefficients
   - unless you actually internalize those coefficients on the same framework
     surface, do **not** call the absolute strong coupling “zero import”
6. the new scheme-independence theorem is a useful UV sub-result, not lane
   closure
   - it strengthens the claim that the UV ratio `y_t / g_3 = 1/sqrt(6)` is
     protected
   - it does **not** derive the framework-to-SM gauge crossover
   - do **not** cite the current script as an all-orders vertex-renormalization
     proof; it checks Ward / propagator identities, not full `Z_y / Z_g`
7. the live blocker is now one **self-consistent** framework-to-SM crossover
   - derive how the strong framework boundary hands off to the perturbative
     SM gauge trajectory
   - the preferred route is a one-shot non-perturbative finite matching
     theorem on the actual Hamiltonian, not a huge step-scaling march
   - lattice step-scaling is fallback if that cleaner route fails
8. thresholded running still matters, but the conceptual mismatch is now
   “framework strong boundary vs perturbative SM running”
   - the common boundary relation `y_t = g_3/sqrt(6)` is now enforced on the
     framework surface
   - what is still missing is the framework derivation of the gauge-side
     crossover to the perturbative trajectory used below `M_Pl`
9. the new “gauge crossover theorem” is still not closure authority
   - the current script still seeds the gauge trajectory from observed
     `alpha_s(M_Z)` when it builds `g_3(M_Pl)`
   - so the successful `m_t` number is still produced on an
     observed-seeded gauge path, not a fully framework-derived crossover map
   - its exactness claims around Feshbach-preserved gauge coupling and the
     projected Ward identity still outrun the current proof surface
10. the load-bearing external content is now very specific
   - if you can derive the plaquette-to-`V` and `V`-to-`\overline{MS}`
     coefficients on the framework surface, or replace them with a native
     background-field crossover theorem, the lane changes materially
   - if you cannot, keep the lane bounded and say so plainly

**What counts as success**

- best-case success:
  - derive one actual framework-native plaquette/lattice to
    `\\overline{MS}` crossover at `M_Pl` that sets both `g_3` and `y_t`
  - run the thresholded 2-loop chain with that common boundary and close the
    residual
- second-best success:
  - isolate the lane to the remaining explicit imported ingredients
    (for example bounded `g_bare = 1` and/or imported matching coefficients)
    and state that honestly
- minimum acceptable success:
  - keep the flagship note honest and bounded with the residual written as a
    self-consistent boundary problem rather than a vague “continuum bridge”

**What does not count**

- re-proving Feshbach on toy systems
- presenting corrected beta coefficients as if that alone closes the lane
- calling `alpha_s` or `y_t` “zero import” while the absolute boundary still
  comes through imported plaquette-to-`V` / `V`-to-`\overline{MS}` matching
- using observed `alpha_s(M_Z)` to build `g_3(M_Pl)` while calling the full
  high-scale boundary framework-derived
- using one high-scale coupling for `y_t` and a different one for `g_3`
- saying “the rest is just standard running” unless the actual common boundary
  is computed on the framework surface

**Preferred attack order**

1. do **not** re-prove Feshbach or the sub-percent matching coefficient
2. do **not** spend more time on the old “two unrelated UV couplings” story;
   that is no longer the real blocker
3. preferred route:
   - place the actual `Cl(3)` / `Z^3` Hamiltonian in a slowly varying SU(3)
     background field
   - do the same low/high-energy Schur-complement / Feshbach projection
     already verified on the real Hamiltonian
   - extract the induced low-energy gauge-kinetic coefficient
   - use that as the one-shot framework-to-SM crossover map
4. in parallel, if there is a clean route, derive or replace the imported
   plaquette-to-`V` and `V`-to-`\overline{MS}` coefficients on the same
   framework surface
5. keep `y_t / g_3 = 1/sqrt(6)` on that effective boundary, not on the raw
   plaquette coupling
6. only then run the full thresholded 2-loop chain from that common handoff
7. lattice step-scaling is fallback if 3-6 fail cleanly
8. if all of that fails, isolate exactly which low-energy gauge anchor or
   imported matching coefficient is
   still imported and keep the lane bounded

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
