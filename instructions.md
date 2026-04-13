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
6. current transport routes are still bounded
   - `D_q*T`: present route plugs framework `alpha_s` into AMY/Moore kinetic
     theory and adopts literature collision-integral / NLO factors
   - `v_w`: present route plugs framework couplings into pressure/friction
     estimates and then adopts a literature-style `0.01-0.10` range
   - those are useful bounded transport closures, not yet native lattice
     derivations
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
- `docs/WILSONIAN_EFT_DERIVATION_NOTE.md`
- `docs/YT_MATCHING_COMPUTED_NOTE.md`
- `docs/YT_CL3_PRESERVATION_NOTE.md`
- `docs/RENORMALIZED_YT_THEOREM_NOTE.md`
- `scripts/frontier_yt_cl3_preservation.py`
- `scripts/frontier_yt_matching_coefficient.py`
- `scripts/frontier_yt_matching_computed.py`
- `scripts/frontier_wilsonian_eft.py`
- `scripts/frontier_yt_full_closure.py`

**Current blockers**

1. the old toy-model objection is mostly gone
   - Feshbach is now verified on the actual staggered `Cl(3)` / `Z^3`
     Hamiltonian
   - `b_2 = 19/6` bookkeeping is corrected
   - do not spend more time re-litigating those fixed points
2. do **not** redo solved sub-steps
   - `Cl(3)` preservation under RG is already the right surface
   - Feshbach on the actual Hamiltonian is already verified
   - the 1-loop bookkeeping bug is fixed
   - the lattice matching coefficient itself is already narrowed to
     sub-percent scale
3. the live blocker is now the real low-energy matching bridge
   - interacting gauge/Higgs operator content on the actual framework surface
   - thresholded running from `M_Pl` to `M_Z`
   - lattice / V-scheme to `\\overline{MS}` boundary conversion for `g_s`
     and `y_t`
4. `alpha_s(M_Pl)` remains bounded as a chain, not as a free parameter
   - the issue is scheme/matching precision, not missing conceptual structure
5. the lane is now a quantitative precision problem
   - if you can compute the matching cleanly, the lane likely closes
   - if not, keep it sharply bounded and stop calling it conceptually open

**What counts as success**

- best-case success:
  - compute the actual lattice-to-`\\overline{MS}` matching for the relevant
    Yukawa/gauge operators at `M_Pl`
  - run the thresholded 2-loop chain with that boundary and close the residual
- second-best success:
  - close the interacting operator-identification step cleanly and isolate the
    remaining uncertainty to one explicit matching coefficient
- minimum acceptable success:
  - keep the flagship note honest and bounded with the residual written as a
    precision/matching problem rather than a vague “continuum bridge”

**What does not count**

- re-proving Feshbach on toy systems
- presenting corrected beta coefficients as if that alone closes the lane
- saying “the rest is just standard running” unless the actual scheme matching
  is computed on the framework surface

**Preferred attack order**

1. do **not** re-prove Feshbach or the sub-percent matching coefficient
2. compute the actual boundary conversion from the framework lattice/V-scheme
   surface to `\\overline{MS}` at `M_Pl`
3. run the full thresholded 2-loop chain from that boundary
4. isolate any remaining discrepancy as a small boundary/scheme residual,
   not a vague continuum objection

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
2. do **not** redo the solved structural pieces
   - the exact `2x2` `2-3` block diagonalization is already done
   - the ratio route `c_23^u/c_23^d` is already done
   - the full `3x3` NNI `V_ub` route is already done as a bounded result
3. the real remaining blocker is quantitative closure
   - absolute `2-3` overlap scale `S_23` is still not derived sharply
   - `c_13` / phase control is still not sharp enough for `V_ub`
   - `V_cb` and `V_ub` remain the actual publication blockers
4. current best reading of the gap
   - the ratio route is useful but too small by itself
   - invariants are consistency checks, not closure
   - the highest-value missing derivations are now:
     - absolute `S_23`
     - sharp `c_13`
     - phase-aware full `3x3` NNI diagonalization

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

3. derive the **absolute** `S_23` overlap scale analytically
   - do not treat cluster compute as the first choice
   - use the continuum / Symanzik taste-splitting machinery if possible
   - this is now the highest-value unsolved piece for `V_cb`

4. close `V_ub` by deriving `c_13` and the relevant phase structure
   - the latest note shows `V_ub` is highly sensitive to residual `c_13`
   - deriving `c_13` from first principles is more valuable now than redoing
     crude mass-ratio estimates

5. use invariants only as a consistency layer
   - they do not independently close `V_cb`
   - use them after `S_23` / `c_13` are sharpened, not instead of that work

6. cluster-compute fallback
   - only fall back to `L >= 32` / dynamical overlap production if the ratio /
     analytic routes fail cleanly

**Routes to stop overusing**

- do not keep presenting “needs more compute” as the only path without first
  exhausting the analytic `S_23` / `c_13` routes
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
