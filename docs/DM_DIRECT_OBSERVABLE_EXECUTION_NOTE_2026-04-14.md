# DM Direct-Observable Execution Note

**Date:** 2026-04-14
**Branch:** `codex/dm-main-derived`
**Purpose:** branch execution note for the DM lane after the `main`-branch
atlas audit

---

## Status

**EXECUTION AUTHORITY** -- use this note for branch work planning.

This note does **not** promote the DM lane to closed. `review.md` still wins
on overall lane status: DM relic mapping remains **BOUNDED / OPEN**.

What changes here is the **workstream choice**:

- the primary branch route is now the **direct-observable stack**
- the `eta` / EW baryogenesis / transport story is demoted to a **secondary
  cosmology companion path**, not the main closure driver

---

## Core Decision

The branch should treat the DM numerator as:

    H  ->  lattice T-matrix  ->  sigma_v  ->  relic numerator

not as:

    g_bare  ->  alpha_s  ->  imported sigma_v  ->  relic numerator

and not as:

    EWPT / transport  ->  eta  ->  Omega_b  ->  R

The current best branch assets for this route are:

- `docs/DM_DIRECT_OBSERVABLE_NOTE.md`
- `docs/DM_COULOMB_FROM_LATTICE_NOTE.md`
- `docs/DM_FINAL_GAPS_NOTE.md`
- `docs/G_BARE_RIGIDITY_THEOREM_NOTE.md`
- `docs/DM_DENOMINATOR_BLOCKER_NOTE_2026-04-14.md`
- `docs/DM_ETA_ROUTE_AUDIT_2026-04-14.md`
- `scripts/frontier_dm_sigma_v_lattice.py`
- `scripts/frontier_dm_coulomb_from_lattice.py`

The current relic paper note is a **downstream summary surface**, not the
driver of the branch.

---

## What Is Genuinely Different

This route is genuinely different from the old `eta` bottleneck because it
tries to close the **relic numerator itself** from the Hamiltonian.

That means:

1. `sigma_v` is treated as a direct observable of `H` through the lattice
   resolvent / T-matrix.
2. The Coulomb shape is treated as a lattice Green's-function observable,
   not as an imported one-gluon-exchange ansatz.
3. The remaining problems become:
   - honest handling of the framework-defining `g = 1` coefficient
   - exact status of the thermodynamic-limit / relic-normalization bridge
   - secondary `k = 0` / radiation-era wording around the freeze-out
     expansion surface

Those are still hard, but they are the **right hard problems**.

---

## Branch-Safe Claim Boundary

As of this note, the branch can safely say:

- `sigma_v` has a native **direct-observable** route through the lattice
  T-matrix and optical theorem
- the Coulomb potential shape has a native route through the lattice
  Green's function
- these strengthen the DM numerator substantially
- the overall lane remains bounded because the full relic bridge still needs
  a sharp normalization closure, and any full `R` statement still has to
  handle the framework-defining `g = 1` surface and the baryon denominator
  honestly

The branch should **not** currently say:

- `g_bare = 1` is derived
- all imports are gone
- the full DM lane is closed
- the `eta` route is no longer needed in principle for all cosmology claims

---

## Live Blockers After The Pivot

1. **Authority mismatch inside the DM note set.**
   `DM_DIRECT_OBSERVABLE_NOTE.md` and `DM_COULOMB_FROM_LATTICE_NOTE.md`
   are newer and stronger than the older provenance wording in
   `DM_RELIC_PAPER_NOTE.md`.

2. **`sigma_v` wording needs discipline.**
   The direct-observable route is the correct surface, but finite-lattice,
   Born-level, coefficient, and thermodynamic-limit caveats still matter.

3. **`g = 1` remains the sharpest bounded blocker unless the new rigidity
   theorem route lands.**
   The direct-observable route dissolves the old "is it the same coupling?"
   objection. The remaining issue is whether the branch accepts the stronger
   operator-algebra claim in `G_BARE_RIGIDITY_THEOREM_NOTE.md`: no free bare
   coupling remains once the concrete `su(3)` operator algebra and its trace
   normalization are fixed. The self-dual-point discussion remains support,
   not a theorem.

4. **The thermodynamic / radiation-era bridge is still real, but it is now
   secondary.**
   `DM_FINAL_GAPS_NOTE.md`, `DM_DIRECT_BOLTZMANN_NOTE.md`, and
   `DM_FRIEDMANN_FROM_NEWTON_NOTE.md` materially narrow that bridge. The
   remaining freeze-out-side issue is now better described as `k = 0` /
   normalization wording than as a broad missing numerator derivation.

5. **The `eta` path is still downstream if we want the full ratio or
   cosmology companions.**
   It is just no longer the branch's best first move.
   If the `g_bare` rigidity theorem lands, `eta` becomes the next honest
   full-closure blocker.

6. **If denominator work resumes, do not return to EWBG by default.**
   The current harsh route ranking is:
   - publication fallback: `R(eta)`
   - cleaner theorem-grade research path: leptogenesis via the taste staircase
   - not promotable at paper bar: the present EWBG / transport stack

---

## Preferred Attack Order

1. Normalize the numerator authority surface.
   Make the note/script/paper-summary stack agree on:
   - direct-observable `sigma_v`
   - lattice-native Coulomb potential
   - bounded `g = 1`
   - still-bounded overall lane

2. Treat `DM_RELIC_PAPER_NOTE.md` as a downstream summary and update it to
   reflect the newer numerator provenance.

3. Tighten the remaining direct-observable blockers:
   - `g = 1` / framework-normalization wording
   - integrate the rigidity-theorem route if it survives harsh review
   - thermodynamic-limit reduction
   - secondary `k = 0` / radiation-era expansion wording

4. Only after 1-3 are coherent should the branch spend another cycle on the
   denominator.
   When that happens:
   - freeze the paper-safe surface as `R(eta)` first
   - treat leptogenesis as the cleaner theorem program
   - only return to EWBG if a reconciled native EWPT result kills the
     detonation / regime-mismatch objection

5. If the direct-observable stack stalls, the next nontrivial alternative is
   **not** more transport tuning. It is to import the exact
   `log|det(D+J)|` observable-principle machinery from the retained hierarchy
   lane.
   Update after the denominator pass: this is now a real DM denominator
   normalization tool for the direct neutrino bridge. The local second-order
   cascade suppression law is now also closed by the Schur theorem; the
   remaining full-`eta` blocker is downstream on the Majorana / `Z_3`
   activation law.

---

## What Does Not Count

- dissolving the old `g_bare` objection while leaving the relic summary stale
- saying “zero imports” because the Coulomb note passes
- treating the self-dual-point observation as a derivation of `g = 1`
- returning immediately to `eta` transport without first exhausting the
  direct-observable stack

---

## Sharp Blocker After Audit

After the direct-observable pivot and the branch audit, the cleanest honest
blocker is:

> can the branch treat the unit coefficient in
> `H = sum eta_ij U_ij` as a physical framework constraint, or does the paper
> bar still require a theorem-grade selection principle beyond that premise?

If the answer is "the framework premise is admissible," then the next work is
mostly packaging and secondary `k = 0` / normalization cleanup.

If the answer is "no, derive `g = 1` beyond the framework premise," then the
branch does **not** currently have a closed route. The self-duality path is
negative, and the determinant / source-response machinery is not yet a DM
derivation.

---

## Immediate Branch Tasks

1. fix stale provenance in `DM_RELIC_PAPER_NOTE.md`
2. align `frontier_dm_sigma_v_lattice.py` with the honest branch-safe claim
3. repoint `instructions.md` Target A to this direct-observable execution note
4. only then decide whether the next implementation pass should target:
   - tighter thermodynamic / Friedmann wording
   - a merged numerator authority note
   - or the denominator route ranking in
     `DM_ETA_ROUTE_AUDIT_2026-04-14.md`
