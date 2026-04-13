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
- `docs/DM_STOSSZAHLANSATZ_THEOREM_NOTE.md`
- `docs/DM_INVARIANT_BRIDGE_NOTE.md`
- `docs/DM_K_INDEPENDENCE_NOTE.md`
- `scripts/frontier_dm_stosszahlansatz.py`
- `scripts/frontier_dm_graph_native.py`
- `scripts/frontier_dm_k_independence.py`

**Current blockers**

1. the live blocker is now `eta`, not the old coupling-identity objection
   - `sigma_v` as a direct observable of `H` is useful
   - the invariant-bridge note correctly narrows the old normalization gap
   - neither closes `R = Omega_DM / Omega_b` because the denominator still
     uses imported baryon abundance
2. relic bridge is now:
   - numerator largely derived
   - denominator still imported through baryogenesis / `eta`
3. Stosszahlansatz is now a strong sub-result, but not the full lane
   - do not keep re-fighting the same coarse-graining objection
   - the remaining issue is not “does factorization exist?” but “can the full
     relic bridge be closed without imported cosmology?”
4. bounded framework inputs still need honest handling
   - `g = 1` is still a framework-defining coefficient, not a theorem
   - `k = 0` remains bounded if used in Newtonian cosmology
   - no “zero imports / pure graph theory” language while `eta` is imported

**What counts as success**

- best-case success:
  - derive `eta` from the framework by closing the baryogenesis chain
  - then update the relic bridge note so `R` is genuinely parameter-free
- second-best success:
  - prove a tighter framework-internal `eta` window from baryogenesis inputs
  - and state the lane as “derived up to one cosmological input” with no
    remaining ambiguity
- minimum acceptable success:
  - one authority note states plainly that the live blocker is `eta`
  - the note, runner, and packet stop pretending the lane is otherwise closed

**What does not count**

- dissolving the old `g_bare` objection while leaving the relic bridge open
- calling cosmological cancellation exact without a real derivation check
- calling the whole lane “pure graph theory” while still using imported bridge
  structure

**Preferred attack order**

1. derive the electroweak phase-transition strength `v(T_c)/T_c`
   nonperturbatively on the framework surface
2. derive the baryogenesis transport / CP-source prefactor from the `Z_3`
   phase structure rather than parameterizing it
3. only after that, promote `eta` and then the full relic ratio

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

1. the old toy-model objection is mostly gone
   - Feshbach is now verified on the actual staggered `Cl(3)` / `Z^3`
     Hamiltonian
   - `b_2 = 19/6` bookkeeping is corrected
   - do not spend more time re-litigating those fixed points
2. the live blocker is now the real low-energy matching bridge
   - interacting gauge/Higgs operator content on the actual framework surface
   - thresholded running from `M_Pl` to `M_Z`
   - lattice / V-scheme to `\\overline{MS}` matching for `y_t` and `g_s`
3. `alpha_s(M_Pl)` remains bounded as a chain, not as a free parameter
   - the issue is scheme/matching precision, not missing conceptual structure
4. the lane is now a quantitative precision problem
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

1. extend the Wilsonian note from free-fermion operator content to the actual
   interacting gauge/Higgs matching surface needed for `y_t`
2. compute the lattice/V-scheme to `\\overline{MS}` matching coefficient for
   `y_t` and `g_s` at `M_Pl`
3. rerun the full thresholded 2-loop chain and measure the residual honestly

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
   - absolute `2-3` overlap scale `S_23` is still not derived sharply
   - `c_13` / phase control is still not sharp enough for `V_ub`
   - `V_cb` and `V_ub` remain the actual publication blockers
3. current best reading of the gap
   - the ratio route is useful but too small by itself
   - invariants are consistency checks, not closure
   - the highest-value missing derivations are now:
     - absolute `S_23`
     - sharp `c_13`
     - phase-aware full `3x3` NNI diagonalization

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
