# DM Split-2 Interval-Certified Dominance Closure Theorem

**Date:** 2026-04-21
**Status:** support - structural or confirmatory support note
**Primary runner:** `scripts/frontier_dm_split2_interval_certified_dominance_closure_2026_04_21.py`

## Claim

The residual split-2 carrier-side dominance/completeness blocker on the
dark-matter flagship lane is closed on the current package surface.

More precisely: after the prior carrier-side reduction localized all remaining split-2 pressure to the two explicit upper-face neighborhoods

- `CAP_BOX = {m in [-0.145,-0.14], delta in [1.1835,1.1935], slack in [0.0145,0.0245]}`
- `ENDPOINT_BOX = {m in [-0.145,-0.14], delta in [1.1839,1.1890], slack in [0,0.005]}`

this note certifies on each whole box that every spectral-row transport packet satisfies

```text
eta / eta_obs < 1.
```

So the residual split-2 carrier branch does not contain a transport-closing point.

## Prior reduction already on branch

Two earlier artifacts had already done the reduction work:

- `docs/DM_NEUTRINO_SOURCE_SURFACE_CARRIER_SIDE_CONCLUSION_NOTE_2026-04-18.md`
  compressed the surviving carrier-side pressure to the two explicit split-2
  upper-face neighborhoods `CAP_BOX` and `ENDPOINT_BOX`.
- `docs/DM_SPLIT2_DENSE_GRID_LIPSCHITZ_DOMINANCE_SUPPORT_NOTE_2026-04-21.md`
  showed on audited dense grids that both boxes stayed well below transport
  closure, but left open whether this was theorem-grade interval control or
  only sampled support.

This note closes that remaining proof gap.

## Exact affine setup

On the split-2 chart the active affine Hermitian family is linear in three
real parameters `(m, delta, slack)`. Writing `q_+ = q_floor(delta) + slack`,
the branch runner packages the exact affine generators as

```text
T_m      with ||T_m||_2     = 1,
T_delta  with ||T_delta||_2 = sqrt(3),
T_q      with ||T_q||_2     = 2.
```

So for every box in `(m, delta, slack)` space, Weyl gives an immediate
operator-norm perturbation radius

```text
r_box = h_m ||T_m||_2 + h_delta ||T_delta||_2 + h_slack ||T_q||_2
```

from the box center half-widths `(h_m, h_delta, h_slack)`.

For the two residual boxes this yields:

- `CAP_BOX`: center eigenvalues
  `(-1.588369475404, -0.326042391504, 1.771911866907)` and Weyl radius
  `0.021160254038`
- `ENDPOINT_BOX`: center eigenvalues
  `(-1.586428810925, -0.324516039457, 1.768444850383)` and Weyl radius
  `0.011916729559`

The resulting eigenvalue intervals stay pairwise disjoint on both boxes, so
the spectral projectors remain simple throughout each whole neighborhood.

## Exact projector-row intervals

For each eigenvalue `lambda_j` and each row `i`, the spectral weight is
computed exactly by the cofactor formula

```text
P_ij = det(H_(i) - lambda_j I_2) / prod_{k != j} (lambda_j - lambda_k).
```

Using interval arithmetic on the row cofactors and the Weyl-separated
eigenvalue intervals gives theorem-grade projector-entry intervals for every
row on both boxes. The strongest row is already the physical row-3 packet:

- on `CAP_BOX`, row 3 stays inside
  `[(0.6891, 0.8204), (0.1716, 0.2452), (0.0276, 0.0562)]`
- on `ENDPOINT_BOX`, row 3 tightens further to
  `[(0.7199, 0.7945), (0.1796, 0.2205), (0.0364, 0.0522)]`

All entry intervals remain inside `[0,1]`, and every row is controlled
simultaneously on each whole box.

## Transport upper bounds

The one-source flavored transport functional is already exact on the branch:

```text
F(P) = sum_alpha Psi(P_alpha).
```

The kernel `Psi(q)` is one-variable and has its small-leakage maximum at

```text
q_star = 0.035493877259706,
Psi(q_star) = 0.011015495595788.
```

Pushing the projector-entry intervals through this exact kernel yields
boxwise rigorous rowwise upper bounds:

- `CAP_BOX`: `eta / eta_obs <= (0.76920972, 0.88068906, 0.90419742)`
- `ENDPOINT_BOX`: `eta / eta_obs <= (0.75987683, 0.86362766, 0.89898279)`

So the theorem-grade margins to transport closure are:

- `CAP_BOX`: at least `0.095802577203`
- `ENDPOINT_BOX`: at least `0.101017210975`

Both residual boxes therefore stay strictly below `eta = 1` on their entire
domains.

## Theorem

**Theorem.** On the current split-2 residual carrier branch, the two explicit
upper-face neighborhoods `CAP_BOX` and `ENDPOINT_BOX` contain no
transport-closing point. Equivalently, interval-certified exact-carrier
dominance/completeness holds on the residual split-2 selector branch.

**Proof.** Weyl interval control gives disjoint eigenvalue boxes throughout
both neighborhoods; exact cofactor formulas then give rigorous projector-row
intervals; the exact one-variable transport kernel gives rowwise transport
upper bounds strictly below `eta = 1` on both whole boxes. Verified in
`scripts/frontier_dm_split2_interval_certified_dominance_closure_2026_04_21.py`
with `17 PASS, 0 FAIL`.

## Consequence for the DM flagship lane

The split-2 carrier-side dominance/completeness blocker is no longer open on
the current package surface.

At the point of this theorem alone, what remained open on the dark-matter
flagship lane was strictly selector-side on the current package surface:

- the finer right-sensitive microscopic selector law for the physical source
  branch / point

The stricter axiom-native A-BCC target remained a boundary/no-go statement,
but not a live package-surface blocker. The later same-day shifted same-law
packet theorem and ordered-chain current stack close the remaining
package-surface selector/current burden.

This theorem does not close the PMNS gate by itself. It removes the last
carrier-side completeness obstruction on the reviewed split-2 residual branch.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16](DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16](DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [dm_neutrino_source_surface_carrier_side_conclusion_note_2026-04-18](DM_NEUTRINO_SOURCE_SURFACE_CARRIER_SIDE_CONCLUSION_NOTE_2026-04-18.md)
