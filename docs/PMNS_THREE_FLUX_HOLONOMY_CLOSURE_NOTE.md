# PMNS Three-Flux Holonomy Closure

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Script:** `scripts/frontier_pmns_three_flux_holonomy_closure.py`

## Question

Can a finite native family of twisted flux holonomies close the reduced
graph-first PMNS oriented-cycle family exactly?

## Answer

Yes.

On the reduced graph-first cycle family

`A_fwd(u,v,w) = u B1 + v B2 + w B3`

the one-angle flux holonomy is the exact linear functional

`h_phi(A_fwd) = 2 u cos(phi) + 2 v sin(phi) + w`.

Therefore a generic three-angle family `phi_1, phi_2, phi_3` gives the exact
linear system

`M(phis) [u,v,w]^T = h`

with rows `[2 cos(phi_i), 2 sin(phi_i), 1]`.

Whenever `det M(phis) != 0`, the reduced coordinates `(u,v,w)` are recovered
exactly.

## Exact content

For the explicit generic choice

- `phi_1 = 0`
- `phi_2 = pi/2`
- `phi_3 = pi/3`

the design matrix is

```text
[[2,   0,       1],
 [0,   2,       1],
 [1, sqrt(3),   1]]
```

and has nonzero determinant.

So:

1. the three-flux holonomy vector is the exact image of `(u,v,w)`
2. the reduced coordinates are reconstructed exactly by solving that system
3. distinct reduced-channel points are separated exactly by the three-flux
   holonomy data

## Consequence

This upgrades the twisted-flux route from a partial value law to a positive
closure route on the reduced PMNS cycle family.

It is now strengthened further by
`PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*),
which shows that the exact `C3` character triple already supplies a canonical
native three-mode holonomy family. So the result below can now be read in two
ways:

- as a generic three-flux closure theorem, and
- more strongly, as a native `C3`-character closure theorem on the retained
  graph-first cycle frame.

It does **not** by itself prove full sole-axiom neutrino closure from
`Cl(3)` on `Z^3` alone. What remains blocked after the stronger `C3`-character
upgrade is no longer the readout family itself, but the sole-axiom production
of **nontrivial values** on that native family.

## Verification

```bash
python3 scripts/frontier_pmns_three_flux_holonomy_closure.py
```

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_three_flux_holonomy_closure.py
```

Last run (2026-05-10): `PASS=11 FAIL=0` on the present worktree. The
runner exercises class A finite-dimensional algebra and class B
construction-on-data: the reduced graph-first cycle family
`A_fwd(u,v,w) = u B1 + v B2 + w B3`, the one-angle flux holonomy
linear functional `h_phi(A_fwd) = 2 u cos(phi) + 2 v sin(phi) + w`,
the `3 x 3` design matrix with rows `[2 cos(phi_i), 2 sin(phi_i), 1]`,
the determinant nonvanishing on the explicit choice
`phi_1 = 0, phi_2 = pi/2, phi_3 = pi/3`, and the closed-form
inversion recovering `(u,v,w)` from `(h_1, h_2, h_3)`.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing one-angle-holonomy-functional step relies
on, in response to prior 2026-05-10 audit feedback identifying a
`missing_dependency_edge` repair target for audit row
`pmns_three_flux_holonomy_closure_note`. It does not promote this
note or change the claim scope, which remains the conditional
bounded algebraic claim that three chosen flux-angle readouts invert
the reduced three-coordinate cycle family, assuming the one-angle
holonomy law on that family.

One-hop authority candidates cited:

- [`PMNS_TWISTED_FLUX_TRANSFER_HOLONOMY_BOUNDARY_NOTE.md`](PMNS_TWISTED_FLUX_TRANSFER_HOLONOMY_BOUNDARY_NOTE.md)
  — audit row:
  `pmns_twisted_flux_transfer_holonomy_boundary_note`. Sibling
  candidate authority establishing the one-angle twisted-flux transfer
  law `h_phi(A_fwd) = 2 u cos(phi) + 2 v sin(phi) + w` and the reduced
  cycle family `A_fwd(u,v,w) = u B1 + v B2 + w B3` whose definitions
  the present runner imports via `flux_holonomy_on_reduced_family` and
  `reduced_cycle_family` from
  `frontier_pmns_twisted_flux_transfer_holonomy_boundary`. This is
  listed as a candidate dependency for the one-angle holonomy law named
  in the prior feedback notes as the missing dependency edge.
- [`PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md`](PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md)
  — audit row:
  `pmns_c3_character_holonomy_closure_note`. Sibling candidate
  authority strengthening the present three-angle closure to a native
  `C_3`-character closure on the retained graph-first cycle frame, as
  cross-referenced in the present note's "Consequence" section. The
  `C_3`-character readout supplies the canonical native three-mode
  holonomy family (phases `0, 2 pi / 3, 4 pi / 3`) that closes the
  reduced cycle values without admitting an external generic
  three-flux family. This is listed as a candidate dependency while
  independent audit decides whether it closes the edge.
- [`PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md`](PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md)
  — audit row:
  `pmns_oriented_cycle_channel_value_law_note`. Sibling source
  authority on the exact axiom-native oriented-cycle decomposition
  `A_fwd = c_1 E_12 + c_2 E_23 + c_3 E_31` with coefficient law
  `(c_1, c_2, c_3) = diag(A C^dagger)` on the `hw=1` triplet, supplying
  the cycle-frame substrate the present note's reduced family
  `(u, v, w)` lives in. This supplies cited one-hop support on the
  oriented-cycle channel value law while independent audit decides
  chain impact.
- [`PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md`](PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md)
  — audit row:
  `pmns_graph_first_cycle_frame_support_note`. Sibling
  source authority on the graph-first cycle frame carrying the reduced
  family `A_fwd(u,v,w)` substrate.

Open class D registration targets named by prior 2026-05-10 audit
feedback as `missing_dependency_edge`:

- A retained-grade source-note authority establishing
  `flux_holonomy_on_reduced_family(A_fwd(u,v,w), phi)
  = 2 u cos(phi) + 2 v sin(phi) + w` and the
  `reduced_cycle_family` definitions remains required to lift the
  bounded-grade three-flux closure to chain closure. The prior
  feedback notes state this explicitly:
  `missing_dependency_edge - add the source note proving
  flux_holonomy_on_reduced_family(A_fwd(u,v,w), phi) = 2u cos(phi)
  + 2v sin(phi) + w and the reduced_cycle_family definitions as a
  direct cited dependency, then audit that dependency first`.

## Honest auditor read

The independent 2026-05-10 audit on the previous note revision
recorded this row as conditional with load-bearing-step class B and
`chain_closes=False`, observing that the matrix-inversion step closes
algebraically once the one-angle holonomy law is granted, but that the
law is imported from an uncited runner module
(`frontier_pmns_twisted_flux_transfer_holonomy_boundary`) and no cited
authority is provided for the definitions of the reduced cycle family,
flux holonomy, or the claimed coefficient formula. The runner
`scripts/frontier_pmns_three_flux_holonomy_closure.py` is
registered with `runner_check_breakdown = {A: 8, B: 3, C: 0, D: 0,
total_pass: 11}` and verifies the conditional inversion (`PASS=11
FAIL=0` on 2026-05-10). The cite chain above wires the candidate
twisted-flux transfer holonomy boundary sibling, the candidate
`C_3`-character holonomy closure sibling, the oriented-cycle channel
value law source authority, and the cycle-frame support, and explicitly
registers the missing-dependency-edge target
named by the prior feedback notes. After this source edit, the
independent audit lane owns any current verdict and effective status;
this addendum does not request promotion.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority candidates the prior feedback requested, the runner
that exercises the conditional three-flux inversion, and the
missing-dependency-edge target named by the prior feedback notes. It
mirrors the live cite-chain
pattern used by the
`PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md` cluster
(commit `44da750e2`) and the
`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` cluster
(commit `8e84f0c23`). Vocabulary is repo-canonical only.
