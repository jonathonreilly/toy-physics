# Signed Gravity APS / Wald / Gauss Bridge Audit Note

**Date:** 2026-04-25
**Status:** APS source-response bridge not derived on the current retained
surface
**Script:** [`../scripts/signed_gravity_aps_wald_gauss_bridge_audit.py`](../scripts/signed_gravity_aps_wald_gauss_bridge_audit.py)

This note pushes the only surviving nonlocal/boundary target from
[`SIGNED_GRAVITY_RESPONSE_BACKLOG_2026-04-25.md`](SIGNED_GRAVITY_RESPONSE_BACKLOG_2026-04-25.md):
the APS / spectral-asymmetry route.

The boundary language remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim. It is a
bridge audit: can the APS eta sign be tied to the active Gauss monopole and
the response sign without inserting `chi_g` by hand?

## Inputs

The prior APS probe established:

```text
FINAL_TAG: APS_BOUNDARY_INDEX_PROBE_PASS_SOURCE_LOCKING_OPEN
```

from
[`SIGNED_GRAVITY_APS_BOUNDARY_INDEX_CHI_PROBE_NOTE.md`](SIGNED_GRAVITY_APS_BOUNDARY_INDEX_CHI_PROBE_NOTE.md).
The eta sign is basis-invariant, gap-stable, and changes only when an explicit
boundary eigenvalue crosses zero.

The source-unit theorem establishes a positive source scale:

```text
c_cell = 1/4
lambda = 1
M_phys = C_abs
q_bare = 4 pi M_phys
G_Newton,lat = 1
```

from
[`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md).

The missing bridge was:

```text
C_signed = chi_eta C_abs
delta S_boundary / delta Phi = chi_eta M_phys |psi|^2
response coupling = chi_eta Phi
```

with the same `chi_eta = sign(eta(D_Y))` in all three places.

## Audit Result

Command:

```bash
python3 scripts/signed_gravity_aps_wald_gauss_bridge_audit.py
```

Summary:

```text
[PASS] APS eta supplies +/- boundary labels
[PASS] gap-preserving Phi deformation leaves eta source-neutral
       eta=1, zero=0, finite-diff d_eta/dPhi=0.000e+00
[PASS] eta sign changes only at zero crossing defect
       chi_path=[1, 1, 1, 1, 0, -1, -1, -1, -1]
[PASS] primitive area carrier fixes positive lambda
       lambda=1.000000
[PASS] retained source-unit gives positive exterior monopole
       C_abs=2.750000
[PASS] putting chi into Wald coefficient is rejected
       c_cell=+0.250, signed_minus=-0.250
FINAL_TAG: APS_WALD_GAUSS_BRIDGE_NOT_DERIVED
```

The important line is the variational one:

```text
d_eta / dPhi = 0
```

on the gapped boundary sector. A smooth gap-preserving boundary deformation
does not produce a signed local source density. A zero crossing changes the
eta sign, but that is a sector-changing boundary defect, not a weak-field
linear source law.

## Source-Action Table

The finite audit separates the possible source actions:

| law | `dS/dPhi` | status |
|---|---:|---|
| retained Wald/Gauss | `+M_phys` | positive unsigned source; eta independent |
| APS eta spectator | `0` | topological label only; no active source |
| inserted APS locked `chi=+1` | `+M_phys` | works only after adding `chi` to source action |
| inserted APS locked `chi=-1` | `-M_phys` | works only after adding `chi` to source action |

Therefore the APS eta sign does not variationally generate
`chi_eta M_phys |psi|^2` on the current retained surface.

## Wald / Gauss Constraint

The primitive boundary/Wald carrier fixes a positive area/source scale:

```text
c_cell = 1/4
lambda = 4 c_cell = 1
C_abs = M_phys
```

Putting the sign into the Wald coefficient would give:

```text
c_chi = chi / 4
```

so the `chi=-1` branch would have a negative area coefficient. That is
rejected. The sign, if it ever exists, must orient the active source/readout
while leaving the positive inertial mass and positive boundary carrier intact.
The current retained source-unit theorem does not do that; it maps an already
derived active charge into the bare Poisson source.

## Source / Response Locking Table

The bridge audit replayed the four-pair sign table for five laws:

| law | max balance residual | table | derived on current surface | read |
|---|---:|---|---|---|
| retained positive source | `0.000e+00` | fail | yes | all pairs attract |
| APS eta spectator | `0.000e+00` | fail | yes | zero active source |
| APS source-only inserted | `2.000e+00` | fail | no | mixed pairs unbalanced |
| APS response-only inserted | `2.000e+00` | fail | no | mixed pairs unbalanced |
| APS locked inserted | `0.000e+00` | pass | no | same-sector attract, opposite-sector repel |

This is the same core obstruction as the first signed-response harness:
source-only and response-only signs fail action-reaction, and the locked table
passes only when the sign has already been inserted into both source and
response.

## Controls

The audit keeps the basic controls clean:

```text
Born I3 = -4.441e-16
norm drift = 0.000e+00
inserted +/- null q_bare = +0.000e+00
inserted +/- inertial mass sum = 5.500
```

These controls show the bookkeeping is coherent. They do not promote the APS
sign into a physical active source.

## Boundary Verdict

The APS route is now narrowed:

> `sign(eta(D_Y))` remains a concrete, basis-invariant, gap-stable boundary
> label. But the current retained Wald/Gauss/source-unit stack fixes a
> positive unsigned active mass scale, and the eta sign is source-neutral under
> gap-preserving variations. The desired locked signed source appears only
> after adding `chi_eta` to the source action by hand.

Therefore the bridge is not derived:

```text
FINAL_TAG: APS_WALD_GAUSS_BRIDGE_NOT_DERIVED
```

This is not a global impossibility theorem. It leaves one precise proof
obligation:

```text
derive an APS/Wald/Gauss boundary action whose variation gives
delta S / delta Phi = chi_eta M_phys |psi|^2
while keeping c_cell > 0, M_inertial > 0, and response sign = chi_eta.
```

Until such an action is written, the APS route remains a boundary-label target
and inserted-control harness, not a physical signed gravitational sector.

## Conditional Action Proposal

That action has now been proposed explicitly in
[`SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md`](SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md)
with runner
[`../scripts/signed_gravity_aps_locked_source_action_proposal.py`](../scripts/signed_gravity_aps_locked_source_action_proposal.py).

The proposed term is:

```text
S_int = - chi_eta(Y) M_phys <|psi|^2, Phi>.
```

It returns:

```text
FINAL_TAG: APS_LOCKED_SOURCE_ACTION_CONDITIONAL_CANDIDATE
```

This is the cleanest target action for the APS route, but it is still a new
source-action premise until derived from retained APS/Wald/Gauss structure.
