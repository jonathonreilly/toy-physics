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

## Focus rule

Routine review should focus on:

1. DM relic mapping
2. renormalized `y_t`
3. CKM

Everything else is out of scope unless Codex explicitly asks for cleanup.

## Lane-by-lane review state

### 1. DM relic mapping

Current strongest useful work:

- `DM_CLEAN_DERIVATION_NOTE.md`
- `DM_STOSSZAHLANSATZ_THEOREM_NOTE.md`
- `DM_INVARIANT_BRIDGE_NOTE.md`
- `DM_K_INDEPENDENCE_NOTE.md`
- `DM_DIRECT_OBSERVABLE_NOTE.md`

Current blockers:

- the old coupling-identity objection is now narrower
  - if `sigma_v` is treated as a direct observable of `H` via the T-matrix,
    the “is `g_bare` the same coupling?” objection mostly dissolves
  - this helps, but it does not close the lane
- relic-ratio / cosmological cancellation bridge is still not theorem-grade
- Boltzmann / Stosszahlansatz coarse-graining is improved but still not fully
  internalized

Paper-safe read:

> Structural DM inputs are materially stronger, but the full relic mapping
> remains bounded.

### 2. Renormalized `y_t`

Current safe state:

- bare UV theorem closed
- `Cl(3)` preservation under RG exact
- the new Wilsonian-EFT close-claim does **not** yet clear the paper bar
  - reason 1:
    - the current note/runner verify Feshbach projection on toy Hamiltonians,
      not on the actual `Cl(3)` / `Z^3` Hamiltonian
  - reason 2:
    - symmetry preservation plus generic EFT logic does not by itself identify
      the exact low-energy SM matching surface for this framework
  - reason 3:
    - the runner’s one-loop EFT bookkeeping is not yet publication-safe
      (for example `b_2 = 10/3` appears where the SM value with three
      generations and one Higgs doublet is `19/6`)
- therefore still bounded:
  - low-energy continuum running
  - `alpha_s(M_Pl)` chain
  - lattice-to-continuum matching
  - actual low-energy EFT identification on the real Hamiltonian surface

Paper-safe read:

> The UV theorem surface is strong, but the low-energy bridge remains bounded.

### 3. CKM / quantitative flavor closure

Current safe state:

- route pruning and bounded structural flavor notes are useful
- the old Higgs `Z_3` universality blocker is no longer the main issue
- still open:
  - ab initio O(1) NNI / overlap coefficients
  - quantitative `V_cb` / `V_ub` closure
  - larger-compute or analytic overlap route

Paper-safe read:

> CKM remains bounded; structure improved, quantitative closure not there yet.

### 4. Broad gravity companion bundle

Current accepted split:

- retained:
  - weak-field Newton / Poisson
  - weak-field WEP
  - weak-field time dilation
- bounded:
  - conformal metric
  - geodesic equation
  - light bending
  - strong-field

Important wording rule:

- `L^{-1} = G_0` is accepted as the framework’s closure condition for
  self-consistency
- it is **not** to be sold as a theorem of pure algebra with zero remaining
  premise
- finite-lattice profile checks remain bounded even when they support a
  retained theorem path

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
