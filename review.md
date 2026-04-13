# Codex Review State

**Date:** 2026-04-13  
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
- gravity is still a weak-field framework result, not full nonlinear GR

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
     - weak-field gravity retained
     - broad and strong-field gravity remain bounded companion work
   - current limitation:
     - not a full Einstein-equation derivation

Paper rule:

- acknowledge these honestly in the paper caveats
- do not let them distract from closing DM, `y_t`, and CKM first

## Focus rule

Routine review should focus on:

1. DM relic mapping
2. renormalized `y_t`
3. CKM

Everything else is out of scope unless Codex explicitly asks for cleanup.

If gravity companion docs are touched for cleanup, the promotion blockers are:

1. strong-field gravity
   - zero-echo amplitude is still conditional on the unresolved strong-field
     metric choice
   - “no singularity” is still bounded on the current Hartree / collapse-floor
     support
2. broad eikonal bundle
   - geodesic equation remains conditional on smooth-metric / continuum
     identification
   - conformal metric remains conditional on the same step
   - factor-of-2 light bending remains conditional on conformal metric +
     null-ray identification

So gravity-companion cleanup should only downgrade stale wording, not promote.

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
  - `v_w` is now the cleaner primary blocker
    - the present route still leans on perturbative CW / bag-model driving
      pressure and the imported `R_NP = 1.5` enhancement from 2HDM lattice
      studies
- relic-ratio / cosmological bridge is therefore still not closed
- `g = 1` and `k = 0` remain bounded framework inputs where used

Paper-safe read:

> Structural DM inputs are materially stronger. The BBN objection is mostly
> retired, `L_w*T` is substantially narrowed, and `D_q*T` now has a native
> one-loop lattice route. The full relic mapping still remains bounded because
> `eta` still depends on transport closure that is not yet fully native at the
> paper bar, especially `v_w`.

Best attack:

1. do not spend more time on BBN rhetoric or `L_w*T` unless a real bug appears
2. if `D_q*T` is touched again, the only high-value move is to upgrade it
   beyond the present one-loop / static-screened native lattice surface
3. derive `v_w` without imported `R_NP` / bag-model driving-pressure structure
4. if 2-3 fail, freeze the lane honestly as “framework baryogenesis plus
   standard transport closure”
5. only then promote `eta` and the full relic ratio

### 2. Renormalized `y_t`

Current safe state:

- bare UV theorem closed
- `Cl(3)` preservation under RG exact
- the Wilsonian / matching route is materially better than before
  - Feshbach is now verified on the actual `Cl(3)` / `Z^3` Hamiltonian
  - the one-loop bookkeeping bug (`b_2`) is corrected
  - the lattice matching coefficient is already computed at sub-percent scale
  - V-scheme to `\overline{MS}` conversion is a real narrowing of the old gap
- therefore still bounded:
  - the old split-boundary objection is no longer the best description
  - the new script really does derive one framework coupling and enforce
    `y_t = g_s / sqrt(6)` at the framework boundary
  - but the framework `alpha_s(M_Pl)` is about `4.4x` the perturbative SM
    value obtained by running observed `alpha_s(M_Z)` upward
  - perturbative running of the framework coupling breaks down near
    `10^15.8 GeV`
  - the quoted successful `m_t` prediction still uses the framework Yukawa
    boundary together with the perturbative SM gauge trajectory generated from
    observed `alpha_s(M_Z)`
  - so the remaining blocker is now a concrete non-perturbative gauge
    crossover / step-scaling problem, not the old “two unrelated UV
    couplings” problem
  - thresholded running down to `M_Z` still matters after that crossover

Paper-safe read:

> The UV theorem surface is strong, but the remaining issue is now a concrete
> framework-to-SM crossover problem: the common framework boundary is real,
> but the gauge-side handoff to the perturbative running used below `M_Pl` is
> not yet derived from the same framework surface.

Best attack:

1. do not re-prove Feshbach or the sub-percent matching coefficient
2. derive the framework-to-perturbative gauge crossover from the same boundary
   that fixes `y_t(M_Pl)`, with lattice step-scaling as the clearest current
   route
3. only then rerun the full thresholded 2-loop chain
4. if a low-energy gauge anchor is still needed, isolate it explicitly and
   keep the lane bounded

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
- invariants are useful, but do not independently solve the lane
- the highest-value unsolved targets are now:
  - absolute `S_23` / `c_23` with the residual sector correction removed
  - residual `c_13`
  - up/down phase embedding that resolves the remaining `J`-`V_ub` tension

Preferred routes:

1. use the exact `V_cb` formula already on branch as the baseline
2. use the ratio route only as an input reduction step, not as the closure
3. cheapest next route:
   - tighten `c_12/c_23` on multi-`L` data with enough configurations
   - use that to reduce the residual sector-correction ambiguity before
     reaching for large-`L` brute force
4. derive the absolute `S_23` / `c_23` normalization analytically from the
   continuum / Symanzik taste-splitting machinery and remove the residual
   sector-dependent correction
5. derive `c_13` and the up/down phase structure together
6. use invariant/Jarlskog relations built from derived quantities, not PDG
   angles, only as a consistency layer after `S_23` / `c_13` / phase sharpen

Only if those fail cleanly should the lane be treated as compute-limited.

Paper-safe read:

> CKM remains bounded; the absolute `S_23` route and the `Z_3^3` phase route
> are both materially better, but quantitative closure is still not there.

## Promotion rule

Only report work as promotable when the exact blocker for that lane is gone.

- DM: relic bridge itself must be closed, not just the old `g_bare` objection
- `y_t`: actual framework-to-perturbative gauge crossover must be derived, not
  just the common UV boundary on the strong side
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
