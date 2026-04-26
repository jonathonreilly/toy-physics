# Signed Gravity Boundary `Z2` Flux `chi_g` Probe Note

**Date:** 2026-04-25
**Status:** first concrete Candidate D pass; conserved-label positive,
source-locking negative
**Script:** [`../scripts/signed_gravity_boundary_z2_flux_probe.py`](../scripts/signed_gravity_boundary_z2_flux_probe.py)

This note tests the boundary `Z_2` holonomy / flux superselection route from
[`SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md`](SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md).
It uses the same claim boundary as the signed-gravity backlog notes. This is
not a negative-mass, shielding, propulsion, physical antigravity, or
reactionless-force claim.

The question is narrow:

> Can a boundary `Z_2` holonomy supply a native `chi_g = +/-1` that is more
> than an inserted signed charge?

## Candidate Definition

Use a finite cylinder graph with a closed boundary cycle `gamma_boundary` and
`Z_2` link variables

```text
U_e in {+1, -1}.
```

The candidate branch operator is the boundary Wilson loop

```text
Q_chi = product_{e in gamma_boundary} U_e.
```

It immediately has the desired algebraic shape:

```text
Q_chi = +/-1,
Q_chi^2 = 1,
P_+ != 0,
P_- != 0.
```

It is also gauge-relabel invariant under boundary vertex transformations
because each boundary vertex relabel flips two adjacent links in the closed
loop.

## Theorem Surface Required

The candidate is only conserved after specifying the retained local algebra.
The first probe separates three classes:

| move | status | reason |
|---|---|---|
| boundary gauge relabel | allowed | closed-loop product unchanged |
| local bulk plaquette away from the measured boundary | allowed | does not intersect the loop |
| boundary-touching plaquette flip | sector-changing defect | flips one loop edge in the probe |
| explicit boundary link flip | sector-changing defect | inserts/removes `Z_2` flux |
| topology-changing cut | outside candidate surface | no closed gauge-invariant loop remains |

So the clean conservation statement is conditional:

```text
[Q_chi, A_local] = 0
```

only for the holonomy-preserving local algebra. If boundary-touching plaquette
flips or boundary flux insertions are retained as ordinary dynamics, this
candidate is not superselected.

## Probe Output

Command:

```bash
python3 scripts/signed_gravity_boundary_z2_flux_probe.py
```

Summary:

```text
Q_chi sectors sampled: Q_plus=+1, Q_minus=-1
PASS: Z2 involution
PASS: nonempty sectors
PASS: boundary gauge relabel invariance
PASS: allowed local bulk move conservation
PASS: boundary-touching plaquette is sector-breaking
PASS: explicit boundary flux insertion is sector-breaking
PASS: topology-changing cut control fails candidate surface
PASS: positive inertial mass
PASS: inserted locked null monopole control
FAIL: native flux source locking
PASS: inserted source locking control
PASS: Born I3 control
PASS: unitary norm control
PASS: source-unit bookkeeping control
FINAL_TAG: BOUNDARY_CHI_SOURCE_NOT_LOCKED
```

## Source / Response Locking Audit

The holonomy passes the label part of the gate on the restricted surface, but
that is not enough. The source gate requires

```text
delta S / delta Phi(x) = M_phys psi^dagger(x) Q_chi psi(x),
```

which reduces in a pure sector to

```text
rho_active = chi_g M_phys |psi|^2.
```

The native boundary Wilson-loop variable tested here is a spectator with
respect to the scalar gravitational potential:

```text
delta S_native / delta Phi = 0
```

in the probe surface. It therefore does not derive

```text
Q_chi |psi|^2.
```

One can make the locked algebra pass by adding the source by hand:

```text
S_inserted contains chi_g M_phys Phi |psi|^2.
```

That inserted control has the expected consequences:

```text
C_active(+ sector) = +C_abs,
C_active(- sector) = -C_abs,
C_active(+ plus - equal norm) = 0,
M_inertial(+ plus - equal norm) > 0.
```

But this is exactly the inserted-charge case from
[`SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md`](SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md),
not a native derivation of the active source sign.

## Positive Mass, Null, Born, Norm, And Source-Unit Controls

The candidate is harmless on the retained controls when treated as a sector
label:

| gate | result | read |
|---|---|---|
| positive inertial mass | pass | `M_inertial = M_phys ||psi||^2 > 0` in both sectors |
| equal `+/-` active source | pass only for inserted locked source | active monopole cancels while inertial mass adds |
| Born control | pass | fixed Hermitian branch Hamiltonian leaves `I3 = 0` to roundoff |
| norm control | pass | sector phase evolution is unitary |
| source-unit bookkeeping | pass as control | `q_bare = 4 pi chi_g M_phys` consumes an already supplied sign |

The controls do not repair the source-locking failure. Source-unit
normalization remains bookkeeping after a sign has already been derived.

## Relation To The Local Blocks

This boundary flux candidate evades the strict local/taste-cell selector scan
in a limited sense: `Q_chi` is global and not one of the blocked local
Pauli-string involutions. It also avoids the kinetic nonconservation of the
local parity scalar because the label is topological on the restricted
holonomy-preserving algebra.

However, it does not evade the source-action obstruction. The retained
parity-correct scalar source still does not vary to `Q_chi |psi|^2`, and the
plain `Z_2` Wilson loop supplies no active Gauss monopole by itself.

## Gate Table

| gate | status |
|---|---|
| `Q_chi^2 = 1` | pass |
| both sectors nonempty | pass |
| gauge-relabel invariant | pass |
| conserved under allowed local moves | conditional pass |
| fails under sector-breaking moves | pass as control |
| fails under topology-changing cut | pass as control |
| native source/response locking | fail |
| inserted source/response locking | pass as control only |
| positive inertial mass | pass |
| null equal `+/-` monopole | pass only for inserted locked source |
| Born/norm controls | pass |
| source-unit discipline | pass as bookkeeping control |

## Verdict

The first boundary `Z_2` holonomy / flux pass gives:

```text
FINAL_TAG: BOUNDARY_CHI_SOURCE_NOT_LOCKED
```

The candidate is a real conditional superselection label if the retained
boundary algebra excludes boundary flux-changing defects. It is not yet more
than an inserted signed charge for signed gravity, because no native action or
Gauss-law identity makes the boundary holonomy multiply the active source and
the test response.

The next theorem target would have to add a non-ad-hoc identity of the form

```text
C_signed = Q_chi C_abs,
delta S_boundary / delta Phi = Q_chi M_phys |psi|^2,
response coupling = Q_chi Phi,
```

while retaining positive inertial mass and the holonomy-preserving
superselection surface. Without that bridge, the `Z_2` flux remains a
topological spectator or an inserted-charge bookkeeping label.
