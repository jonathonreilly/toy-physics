# Codex Review State

**Date:** 2026-04-14  
**Primary audited source:** `origin/codex/review-active`  
**Canonical claims ledger:** `origin/codex/publication-prep`

If any older note, packet, scorecard, or summary conflicts with this file, this
file wins.

## Authority stack

Use these as the real Codex authority documents:

1. [/private/tmp/physics-review-active/docs/CI3_Z3_PUBLICATION_STATE_2026-04-12.md](/private/tmp/physics-review-active/docs/CI3_Z3_PUBLICATION_STATE_2026-04-12.md)
2. [/private/tmp/physics-review-active/docs/FULL_CLAIM_LEDGER.md](/private/tmp/physics-review-active/docs/FULL_CLAIM_LEDGER.md)
3. [/private/tmp/physics-publication-prep/docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md](/private/tmp/physics-publication-prep/docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md)

## Core publication caveats

These stay explicit even if every remaining live gate closes:

- individual fermion masses are not fully first-principles derived
  - safe claim: retained matter structure, bounded hierarchy/flavor support,
    and selected quantitative windows
- the strong CP problem is not addressed
- `alpha_EM = 1/137` is not derived
- full nonlinear GR is not a current Claude review lane

## Framework-premise rule

Codex accepts the framework premise:

> We take `Cl(3)` on `Z^3` as the physical theory.

That premise can close artifact-vs-physical disputes. It does **not** replace
missing bridge derivations.

So:

- yes:
  - generation closure can lean on the framework premise
  - `S^3` can lean on accepted topology infrastructure plus the framework
    premise already built into the theory statement
- no:
  - DM, `y_t`, or CKM cannot be declared closed just by repeating that the
    graph is physical

## Remaining live publication gates

These are the only three remaining flagship live gates:

1. **DM relic mapping**
2. **Renormalized `y_t` matching**
3. **CKM / quantitative flavor closure**

## Deferred post-gate backlog

These are real framework limitations, but they are **not** current flagship
gate work. Claude should only touch them after the three live gates close, or
if Codex explicitly reprioritizes.

1. **Individual fermion masses**
   - current safe state:
     - hierarchy / structure support is real
     - top has a bounded quantitative lane
   - current limitation:
     - no first-principles derivation of the individual charged-lepton and
       light-/mid-quark masses

2. **`alpha_EM = 1/137`**
   - current safe state:
     - structural electroweak-angle work exists
   - current limitation:
     - absolute EM coupling not derived from the lattice framework itself

3. **Strong CP**
   - current safe state:
     - untouched
   - current limitation:
     - no explanation for `theta_QCD = 0`

4. **Full nonlinear GR**
   - current safe state:
     - deferred from Claude gate work
   - current limitation:
     - not a full Einstein-equation derivation in full generality

Paper rule:

- acknowledge these honestly in the paper caveats
- do not let them distract from closing DM, `y_t`, and CKM first

## Focus rule

Routine review should focus on:

1. DM relic mapping
2. renormalized `y_t`
3. CKM

Everything else is out of scope unless Codex explicitly asks for cleanup.

Ignore gravity unless Codex explicitly asks for gravity cleanup.

## Lane-by-lane review state

### 1. DM relic mapping

Current strongest useful work:

- `DM_CLEAN_DERIVATION_NOTE.md`
- `DM_RELIC_BRIDGE_NOTE.md`
- `ETA_FROM_FRAMEWORK_NOTE.md`
- `BARYOGENESIS_NOTE.md`
- `EWPT_STRENGTH_NOTE.md`
- `DM_STOSSZAHLANSATZ_THEOREM_NOTE.md`
- `DM_INVARIANT_BRIDGE_NOTE.md`
- `DM_K_INDEPENDENCE_NOTE.md`
- `DM_DIRECT_OBSERVABLE_NOTE.md`
- `DM_BOUNCE_WALL_NOTE.md`
- `DM_TRANSPORT_DERIVED_NOTE.md`
- `BBN_FROM_FRAMEWORK_NOTE.md`

Current blockers:

- the baryogenesis chain is now much narrower than before
  - `J_Z3`, `v(T_c)/T_c`, and `Gamma_sph/T^4` are already the strongest part
    of the chain
- the BBN/nuclear-physics objection is largely gone in principle
  - `eta -> Omega_b` really is counting once `m_p`, `G`, and `H_0` are taken
    from accepted framework authority
  - if the BBN runner is used, it must stop hardcoding measured `m_p`, `G`,
    and `H_0` under `[DERIVED]` without pointing to that authority
- `L_w*T` is no longer the main blocker
  - the bounce/profile route is now the strongest transport sub-result
- the live blocker is now the remaining transport sector behind `eta`
  - the old `D_q*T` Coulomb-log / inserted-`C_0` objection is mostly retired
    by the new native lattice mode-sum route
  - but that new `D_q*T` value is still only a one-loop, static-screened
    lattice transport computation with real finite-`L` soft-mode bias, so it
    should be treated as strong native bounded support rather than the final
    transport theorem
  - the latest coupled-transport route is a bounded strengthening, not
    closure
    - it still imports `C_tr`
    - it still imports non-perturbative EWPT calibration entering `v(T_n)/T_n`
  - `v_w` is improved, but it is no longer the only honest blocker
- the new Boltzmann-theorem note is a strengthening, not closure authority
  - its script verifies the master-equation structure only on a small 1D toy
    interaction model
  - the thermodynamic-limit and expansion steps still lean on standard
    Riemann/Weyl/Newtonian-cosmology structure
  - it therefore does **not** retire the live `eta` / transport blocker
- the branch still contains an internal EWPT/baryogenesis regime mismatch
  - older notes still use a partial-washout regime near `v/T ~ 0.5`
  - newer native EWPT notes give a strong first-order surface with
    `v(T_c)/T_c > 1`
  - until one note states which of `v(T_c)/T_c`, `v(T_n)/T_n`, or wall-local
    `v/T` is the real baryogenesis input, the lane is not promotable
- relic-ratio / cosmological bridge is therefore still not closed
- the new taste-enhanced `eta` note is **not** closure authority
  - it multiplies the already-bounded `eta_coupled` result by a post-hoc `8/3`
    trace factor
  - that does not rebuild the transport equations with the explicit
    taste-enhanced source
  - it also leaves the imported `C_tr` calibration and imported
    non-perturbative `v(T_n)/T_n` calibration untouched
- `g = 1` and `k = 0` remain bounded framework inputs where used

Paper-safe read:

> Structural DM inputs are materially stronger. The BBN objection is mostly
> retired, `L_w*T` is substantially narrowed, and `D_q*T` now has a native
> one-loop lattice route. The full relic mapping still remains bounded because
> `eta` still depends on imported `C_tr`, imported non-perturbative
> `v(T_n)/T_n`, and transport closure that is not yet fully native at the
> paper bar.

Best attack:

1. first derive `T_n` from the existing bounce / effective-potential surface
   using `S_3(T_n)/T_n ~ 140`
2. derive the wall-local CP source directly on the physical taste space; do
   not use a post-hoc `8/3` multiplier as closure
3. derive the transport prefactor `C_tr` from the framework transport system
   instead of FHS calibration
4. rebuild `v_w` on the reconciled native EWPT + HTL + bounce surface, with
   no stale imported non-perturbative enhancement
5. solve the coupled transport fixed point instead of scanning `D_q*T`,
   `v_w`, and `L_w*T` independently
6. only if there is real leverage, upgrade `D_q*T` beyond the present one-loop
   / static-screened native surface
7. if 1-6 fail, freeze the lane honestly as “framework baryogenesis plus
   standard transport closure”
8. only then promote `eta` and the full relic ratio

### 2. Renormalized `y_t`

Current safe state:

- bare UV theorem closed
- `Cl(3)` preservation under RG exact
- the zero-import route is materially better than the older observed-seeded
  crossover route
  - Feshbach is verified on the actual `Cl(3)` / `Z^3` Hamiltonian
  - the one-loop bookkeeping bug (`b_2`) is corrected
  - the operator count `n_link(Pi) = 2` is now explicitly derived
- electroweak inputs are no longer the productive objection on this lane
  - on the current Codex-side paper surface, using `v`, low-energy electroweak
    inputs, and the strengthened electroweak/hierarchy package is fair game
- therefore still bounded:
  - the current safest authority surface is:
    - `YT_ZERO_IMPORT_CLOSURE_NOTE.md`
    - `frontier_yt_2loop_chain.py`
    - `YT_VERTEX_POWER_DERIVATION.md`
    - `YT_GAUGE_CROSSOVER_THEOREM.md`
  - do **not** let older closure-language notes outrank that newer bounded
    authority
    - `YT_FLAGSHIP_CLOSURE_NOTE.md` and `YT_BOUNDARY_RESOLUTION_NOTE.md`
      currently overstate closure relative to the reviewed state
  - the newest flagship note still labels the lane `BOUNDED`
  - the zero-import chain gives:
    - `alpha_s(M_Z) = 0.1181`
    - `m_t = 169.4 GeV` (2-loop y_t RGE, via `frontier_yt_2loop_chain.py`)
    - about `-1.9%` on `m_t`
    - the earlier 1-loop result (`m_t = 165.4 GeV`, `-4.2%`) is superseded
  - the remaining blocker is no longer the old observed-seeded gauge path or
    the stale plaquette objection
  - the branch has materially narrowed the old LM objection
    - `frontier_vertex_power.py` derives `n_link(Pi) = 2`
    - the Coupling Map Theorem (YT_VERTEX_POWER_DERIVATION.md, Part 6) now
      claims to derive `alpha_bare / u_0^{n_link}` from the partition function
  - the older contradiction with `frontier_native_matching.py` is gone on the
    latest remote head
    - both main scripts now claim the vertex `u_0^2` prescription is derived
    - so the review question is no longer whether the branch contradicts itself
  - the old plaquette-benchmark objection is also largely gone
    - `frontier_zero_import_chain.py` now computes the plaquette on the same
      surface using multi-`L` SU(3) Monte Carlo and uses the largest-`L` value
      as authoritative
    - the `0.5934` benchmark is comparison-only, not the load-bearing input
  - the actual remaining gap is the boundary-consistency theorem
    - the current 2-loop zero-import run gives a strong bounded result
    - but it matches `y_t(M_Pl)` to the Ward BC while the same run gives
      `g_3(M_Pl) = 0.487`, not the framework value `1.067`
    - and the script itself says why: the current setup fixes `alpha_s(v)`,
      not one self-consistent `g_3(M_Pl)` trajectory
  - the older gauge-crossover theorem remains bounded support only
    - its exactness language still outruns the current proof surface

Paper-safe read:

> The UV theorem surface is strong, and the zero-import route with 2-loop y_t
> RGE gives m_t = 169.4 GeV (-1.9%). The old LM/plaquette objections are now
> materially narrower. The lane is still bounded because the current chain
> does not yet live on one self-consistent renormalized boundary surface:
> it enforces the Ward condition on `y_t(M_Pl)` while the same run gives
> a different `g_3(M_Pl)` than the framework value. The last theorem is to
> derive whether the physical crossover endpoint is at `v` or at `M_Pl`, and
> then run the entire gauge/Yukawa chain on that single surface.

Best attack:

1. do not re-prove Feshbach or the sub-percent matching coefficient
2. do not spend more time on the old observed-seeded crossover complaint; the
   newest zero-import route is the right surface now
3. do not reopen the old plaquette-benchmark objection unless the chain
   regresses; that is no longer the main blocker
4. derive the boundary-selection theorem:
   - either the physical crossover endpoint is `v`, in which case the lane
     should be rewritten as an electroweak-endpoint closure
   - or the endpoint is `M_Pl`, in which case `g_3(M_Pl)` and
     `y_t(M_Pl)=g_3(M_Pl)/sqrt(6)` must close on one single trajectory
5. then rewrite or retract the stale closure-language notes so they do not
   outrank the newest bounded authority
6. only after 4-5 are clean, rerun the zero-import chain
7. if a few-percent `m_t` residual remains after that, then treat improved
   Yukawa running / thresholds as the next quantitative sub-problem
8. if 4-7 fail, freeze the lane honestly as “zero-import up to the
   boundary/crossover theorem”

### 3. CKM / quantitative flavor closure

Current safe state:

- route pruning and bounded structural flavor notes are useful
- the old Higgs `Z_3` universality blocker is no longer the main issue
- the exact `2x2` `2-3` block route is already done
- the ratio route is already done
- the full `3x3` `V_ub` route is already done as a bounded result
- still open:
  - first-principles control of absolute `c_23` / `S_23`
  - first-principles control of `c_13`
  - phase structure strong enough to resolve the `J`-`V_ub` tension

Current best reading:

- this is still not obviously a pure cluster-compute wall
- the new absolute-`S_23` route is real progress
  - it predicts `V_cb ≈ 0.0403`, about `4.6%` low, without using PDG `V_cb`
  - so the lane is no longer blocked on a purely circular `V_cb` calibration
- but the lane is still not closed
  - `K` still has `O(20%)` spread and a residual EWSB sector correction
  - the lattice `c_13` story is still not sharp enough
  - the new `Z_3^3` phase work improves `J` substantially, but the best joint
    result still overshoots `V_ub` and undershoots `delta_CP`
  - the new mass-basis NNI route is a real bounded strengthening for `V_ub`,
    but it still uses PDG quark masses directly and fitted geometric NNI
    coefficients from earlier bounded work
  - it also leaves the phase sector open: `J`, `rho_bar`, and `eta_bar`
    remain far off
  - the new Wolfenstein-cascade note is useful structurally, but not closure
    authority
    - lambda still uses an empirical `R_overlap = lambda_PDG / lambda_bare`
    - the absolute `c_23` scale still comes from `V_cb` matching
    - the phase sector still optimizes `c_13 / c_23` against PDG observables
- invariants are useful, but do not independently solve the lane
- the highest-value unsolved targets are now:
  - absolute `S_23` / `c_23` with the residual sector correction removed
  - residual `c_13`
  - up/down phase embedding that resolves the remaining `J`-`V_ub` tension
  - and the mass-basis suppression itself must be put on a framework-derived
    surface rather than PDG masses plus fitted geometric coefficients

Preferred routes:

1. use the exact `V_cb` formula already on branch as the baseline
2. use the ratio route only as an input reduction step, not as the closure
3. highest-value next route:
   - derive the absolute `S_23` / `c_23` normalization analytically from the
     existing sector-correction machinery, with no PDG back-calibration
4. derive `c_13` analytically from the full `3x3` NNI structure
   - Schur-complement / effective-mass-matrix route is preferred
5. derive the mass-basis suppression from framework-derived mass ratios and
   framework-derived geometric coefficients, not PDG masses plus fitted
   coefficients
6. derive the surviving rephasing-invariant CKM phase from invariants built
   from the same EWSB-dressed mass matrices
7. use multi-`L` ratio/normalization evidence only as support for 3-6, not as
   a substitute for them
8. only if 3-7 fail cleanly should the lane be treated as compute-limited,
   and then only on one scalar quantity (`K_23` or physical `c_13`)

Paper-safe read:

> CKM remains bounded; the absolute `S_23` route and the `Z_3^3` phase route
> are both materially better, but quantitative closure is still not there.

## Promotion rule

Only report work as promotable when the exact blocker for that lane is gone.

- DM: relic bridge itself must be closed, not just the old `g_bare` objection
- `y_t`: actual framework-to-perturbative boundary selection must be derived,
  not mixed between `v` and `M_Pl`, and not while the viable path still lacks
  one single self-consistent gauge/Yukawa trajectory
- CKM: `V_cb` / `V_ub` must be quantitatively sharpened through absolute
  `S_23`, `c_13`, and phase control, not just structure or ratio routes

## Packet alignment rule

If you touch a lane, make sure all three agree:

1. note
2. script
3. packet

If they disagree, the lane is not closed.

## Non-authority docs

These are not science authority if they outrun this review state:

- stale review packets
- scorecards
- pitch decks
- older `*_FULL_CLOSURE_*` notes for DM, `y_t`, CKM, or gauge couplings

## Practical summary

- live gates:
  - DM relic mapping
  - renormalized `y_t`
  - CKM
