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
   - the remaining live transport blockers are `D_q*T` and `v_w`
5. Stosszahlansatz is now a strong sub-result, but not the full lane
   - do not keep re-fighting the same coarse-graining objection
   - the remaining issue is not “does factorization exist?” but “can the full
     relic bridge be closed without imported cosmology?”
6. latest transport routes are stronger, but still bounded at the paper bar
   - `D_q*T`: the Green-Kubo route is a real improvement, but the primary
     value still comes from the analytic continuum-limit Coulomb-log formula
     with an inserted constant `C_0 = 0.5`; the finite-lattice spectral route
     reuses the same analytic width rather than closing the transport
     coefficient natively from lattice data
   - `v_w`: the Boltzmann-closure route is also stronger, but it still leans
     on perturbative CW / bag-model driving pressure and the imported
     non-perturbative enhancement `R_NP = 1.5` from 2HDM lattice studies
   - so the transport sector is narrower, not closed
7. bounded framework inputs still need honest handling
   - `g = 1` is still a framework-defining coefficient, not a theorem
   - `k = 0` remains bounded if used in Newtonian cosmology
   - no “zero imports / pure graph theory” language while transport formulas
     are still imported

**What counts as success**

- best-case success:
  - derive `D_q*T` and `v_w` from actual framework transport dynamics
  - derive `eta` from the framework by closing the transport sector
  - then update the relic bridge note so `R` is genuinely parameter-free
- second-best success:
  - prove a tighter framework-internal `eta` window using the current
    transport ranges
  - and state the lane as “derived up to standard transport formulas” with no
    remaining ambiguity
- minimum acceptable success:
  - one authority note states plainly that the live blockers are `D_q*T`,
    `v_w`, and therefore `eta`
  - the note, runner, and packet stop pretending the lane is otherwise closed

**What does not count**

- dissolving the old `g_bare` objection while leaving the relic bridge open
- calling cosmological cancellation exact without a real derivation check
- calling the whole lane “pure graph theory” while still using imported bridge
  structure
- plugging framework couplings into AMY/Moore or Moore-Prokopec formulas and
  then calling the transport sector fully first-principles derived

**Preferred attack order**

1. do **not** spend more time on `v(T_c)/T_c`, BBN nuclear-physics rhetoric,
   or `L_w*T` unless you find a concrete mathematical bug
2. derive `D_q*T` from an actual framework Green-Kubo / correlator /
   transport computation if possible
3. derive `v_w` from actual wall-friction / Boltzmann closure on the same
   framework surface, not just literature scaling
4. if 2-3 fail, freeze the lane honestly as “framework baryogenesis plus
   standard transport closure”
5. only then update `eta` and the full relic ratio

### Target B: Renormalized `y_t`

**Goal**

- either close the residual bridge or keep one sharp bounded authority note

**Primary files**

- `docs/YT_FLAGSHIP_CLOSURE_NOTE.md`
- `docs/YT_BOUNDARY_RESOLUTION_NOTE.md`
- `docs/WILSONIAN_EFT_DERIVATION_NOTE.md`
- `docs/YT_MATCHING_COMPUTED_NOTE.md`
- `docs/YT_CL3_PRESERVATION_NOTE.md`
- `docs/RENORMALIZED_YT_THEOREM_NOTE.md`
- `scripts/frontier_yt_cl3_preservation.py`
- `scripts/frontier_yt_boundary_resolution.py`
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
2. the new boundary-resolution note is **still not** full closure
   - the old split-boundary objection is narrower now: the script does derive
     one framework coupling that sets both `g_3(M_Pl)` and `y_t(M_Pl)`
   - but the fully unified boundary is non-perturbative and hits a Landau pole
     under the SM RGE
   - the quoted successful `m_t` prediction still uses the framework Yukawa
     boundary together with the perturbative SM gauge trajectory generated from
     observed `alpha_s(M_Z)`
   - so the remaining blocker is no longer “two different couplings at the
     same boundary,” but a real strong-to-perturbative crossover / matching
     problem
3. do **not** redo solved sub-steps
   - `Cl(3)` preservation under RG is already the right surface
   - Feshbach on the actual Hamiltonian is already verified
   - the 1-loop bookkeeping bug is fixed
   - the lattice matching coefficient itself is already narrowed to
     sub-percent scale
4. the live blocker is now one **self-consistent** framework-to-SM crossover
   - derive how the strong framework boundary hands off to the perturbative
     SM gauge trajectory
   - or isolate the low-energy gauge anchor explicitly and keep the lane
     bounded
5. thresholded running still matters, but the conceptual mismatch is now
   “framework strong boundary vs perturbative SM running”
   - the common boundary relation `y_t = g_3/sqrt(6)` is now enforced on the
     framework surface
   - what is still missing is the framework derivation of the gauge-side
     crossover to the perturbative trajectory used below `M_Pl`

**What counts as success**

- best-case success:
  - compute one actual lattice/V-scheme to `\\overline{MS}` boundary at `M_Pl`
    that sets both `g_3` and `y_t`
  - run the thresholded 2-loop chain with that common boundary and close the
    residual
- second-best success:
  - isolate the lane to one explicit imported low-energy anchor
    (for example `alpha_s(M_Z)`) and state that honestly
- minimum acceptable success:
  - keep the flagship note honest and bounded with the residual written as a
    self-consistent boundary problem rather than a vague “continuum bridge”

**What does not count**

- re-proving Feshbach on toy systems
- presenting corrected beta coefficients as if that alone closes the lane
- using observed `alpha_s(M_Z)` to build `g_3(M_Pl)` while calling the full
  high-scale boundary framework-derived
- using one high-scale coupling for `y_t` and a different one for `g_3`
- saying “the rest is just standard running” unless the actual common boundary
  is computed on the framework surface

**Preferred attack order**

1. do **not** re-prove Feshbach or the sub-percent matching coefficient
2. derive one common framework boundary for both `g_3` and `y_t` at `M_Pl`
3. only then run the full thresholded 2-loop chain from that boundary
4. if that fails, isolate exactly which low-energy anchor is still imported
5. keep the lane bounded unless the split-boundary problem is gone

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
3. the new full-closure script does **not** derive `V_cb`
   - it explicitly solves `c_23^d` by matching `V_cb` to PDG
   - do **not** cite that as a first-principles closure
4. the real remaining blocker is quantitative closure
   - absolute `c_23` / `S_23` normalization is improved but still bounded
     rather than theorem-grade
   - `c_13` suppression and phase control are still not jointly derived well
     enough for `V_ub` and `J`
   - the `J`-`V_ub` tension is reduced, not eliminated
5. current best reading of the gap
   - the new absolute-`S_23` route predicts `V_cb` within about `4.6%`
     without using PDG `V_cb`, which is real progress
   - but `K` still has `O(20%)` spread and a remaining EWSB sector correction,
     so the absolute normalization is not yet closed
   - the new `Z_3^3` phase work boosts `J` substantially, but the best current
     joint result still overshoots `V_ub` and undershoots `delta_CP`
   - invariants are still consistency checks, not closure

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

3. derive the **absolute** `S_23` / `c_23` normalization analytically
   - do not treat cluster compute as the first choice
   - use the continuum / Symanzik taste-splitting machinery and the new
     multi-`L` normalization evidence
   - the concrete remaining target is to remove the residual sector-dependent
     `K` / EWSB correction and reduce the current `~5%` `V_cb` gap

4. close `V_ub` by deriving `c_13` and the relevant up/down phase structure
   - the latest note shows the real issue is the `J`-`V_ub` tension
   - deriving `c_13` without fixing the phase structure is not enough
   - deriving a better phase embedding without fixing `c_13` is also not
     enough

5. use invariants only as a consistency layer
   - they do not independently close `V_cb`
   - use them after `S_23` / `c_13` / phase are sharpened, not instead of
     that work

6. cluster-compute fallback
   - only fall back to `L >= 32` / dynamical overlap production if the ratio /
     analytic routes fail cleanly

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
