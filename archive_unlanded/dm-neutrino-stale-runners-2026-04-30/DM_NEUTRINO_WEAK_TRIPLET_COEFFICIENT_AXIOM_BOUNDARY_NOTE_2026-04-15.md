# DM Neutrino Weak-Triplet Coefficient Axiom Boundary

**Date:** 2026-04-15  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/dm-neutrino-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.
**Script:** `scripts/frontier_dm_neutrino_weak_triplet_coefficient_axiom_boundary.py`

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/dm-neutrino-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale runners on the DM-neutrino lane).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: the primary runner reads absolute paths under /Users/jonBridger/... and raises FileNotFoundError before the c_odd and even-leg coefficient checks complete. Why this blocks: the note claims exact single-axiom transfer-coefficient closure, but the shipped verifier is stale and cannot reproduce the load-bearing result in the current repository. Repair target: replace stale absolute-path reads with repository-local retained dependencies and rerun the coefficient-normalization checks end to end. Claim boundary until fixed: the note can be treated only as an unreproduced coefficient-closure proposal; no audited transfer-coefficient closure is available from the current runner.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Framework sentence

In this note, and in the DM denominator discussion that depends on it,

> “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.

Everything else is a derived atlas row, not a second axiom.

## Question

Does the current single-axiom `Cl(3)` on `Z^3` stack, together with the
current derived atlas rows, now derive the transfer coefficients in

- `gamma = c_odd a_sel`
- `[E1, E2]^T = M_even [tau_E, tau_T]^T`?

## Bottom line

Yes, canonically.

The transfer **class** is exact, and the transfer coefficients are now fixed
on the current single-axiom surface:

- `c_odd = +1` on the source-oriented branch convention
- `M_even = v_even [1,1]`
- `v_even = (sqrt(8/3), sqrt(8)/3)`

equivalently

- `gamma = a_sel`
- `E1 = sqrt(8/3) (tau_E + tau_T)`
- `E2 = (sqrt(8)/3) (tau_E + tau_T)`.

So the single-axiom transfer bundle is no longer blocked on coefficient
normalization.

## What changed for `c_odd`

The current stack already gives:

- one exact reduced selector amplitude slot `a_sel`
- one exact odd triplet target slot `gamma`

That by itself only closed the odd-sector **shape** of the map.

The new odd-normalization theorem adds the missing normalization law: on their
exact minimal blocks, the reduced selector generator `S_cls` and the triplet
odd generator `T_gamma` have the same exact bosonic source-response under the
unique additive CPT-even scalar generator. Therefore the canonical odd
normalization is `|c_odd| = 1`, and on the source-oriented branch convention
we record `c_odd = +1`.

## What closed the even leg

The exact source-side weak tensor carrier is

`K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]]`.

This carrier is exact and it still treats the two bright columns
symmetrically. The new weak even swap-reduction theorem sharpens that symmetry
into an exact reduction:

`M_even = [[v_1, v_1], [v_2, v_2]] = v_even [1,1]`

equivalently

`[E1, E2]^T = v_even (tau_E + tau_T)`.

So the current exact source side already kills the antisymmetric source mode
`tau_- = tau_E - tau_T`. The even leg is no longer a generic `2 x 2` matrix
problem.

The new even bosonic-normalization theorem then closes the last coefficient
step. The exact even channels

- `E1 = delta + rho`
- `E2 = A + b - c - d`

have canonical Frobenius-dual target generators that are isospectral to scaled
copies of the unique traceless row generator on the exact 2-row weak source
factor. Under the same unique additive CPT-even scalar generator used in the
odd theorem, this fixes

`v_even = (sqrt(8/3), sqrt(8)/3)`.

## What this closes

This now closes the strongest remaining overclaim about the transfer
**coefficients**.

The branch can no longer honestly say:

- “both `c_odd` and `M_even` are still open on the single-axiom stack”
- “the even target vector `v_even` is still open”

The sharper statement is:

- the current single-axiom `Cl(3)` on `Z^3` stack plus derived atlas rows fix
  the transfer **class**
- they fix the odd normalization `c_odd = +1`
- they fix the even coefficient vector
  `v_even = (sqrt(8/3), sqrt(8)/3)`
- so the transfer coefficients are now fully fixed

equivalently

- `gamma = a_sel`
- `E1 = sqrt(8/3) tau_+`
- `E2 = (sqrt(8)/3) tau_+`

with `tau_+ = tau_E + tau_T`.

## What remains open

What is still not derived on the current single-axiom surface is:

- the selector amplitude `a_sel`
- the symmetric weak source amplitude `tau_+`
- the fully rewritten leptogenesis benchmark expressed in that exact transfer
  law rather than the older reduced kernel

So the live gap is no longer transfer-coefficient normalization. It is the
source-amplitude law.

## Benchmark consequence

This is why the benchmark still stays

- `eta = 1.81e-10`
- `eta / eta_obs ~= 0.30`

The current pass closed the transfer coefficients, not the source amplitudes,
and the benchmark runner has not yet been rebuilt around the exact transfer
law.

## Command

```bash
python3 scripts/frontier_dm_neutrino_weak_triplet_coefficient_axiom_boundary.py
```
