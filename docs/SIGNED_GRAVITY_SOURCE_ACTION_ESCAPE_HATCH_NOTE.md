# Signed Gravity Source-Action Escape Hatch Audit

**Date:** 2026-04-25
**Status:** source-action escape-hatch classification after
`SOURCE_PRIMITIVE_BLOCKED_LOCAL`

This note audits what would be required for a different source action to derive
a signed active gravitational source while keeping positive inertial mass.

The boundary language is unchanged. This is not a negative-mass, shielding,
propulsion, or reactionless-force claim. The only admissible target is a
bounded signed-response sector with:

- positive inertial mass
- a native or naturally hosted conserved `chi_g = +/-1`
- source/response locking
- two-body action-reaction closure
- no hidden source-unit normalization trick

The immediate input is
[`GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md`](GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md),
which lands:

```text
FINAL_TAG: SOURCE_PRIMITIVE_BLOCKED_LOCAL
```

The retained parity scalar coupling variationally exposes

```text
delta E / delta Phi(x) = response_sign * epsilon(x) |psi(x)|^2
```

not `chi_g |psi|^2`.

## Classification Target

The escape-hatch question is not "can a sign be inserted?" It is:

> Can a source action derive a conserved signed active source, coupled to the
> retained gravitational response, without making inertial mass negative or
> breaking conservation/action-reaction?

That separates four cases:

1. retained Poisson/Born source
2. parity scalar variational source
3. inserted signed charge
4. hypothetical new action

## Case 1: Retained Poisson/Born Source

The clean retained gravity derivation uses the weak-field source

```text
rho_B = |psi|^2
```

as the source of the Poisson equation:

```text
(-Delta_lat) phi = rho_B
```

This is the source used in
[`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md) and in
the source-unit support theorem after the bare/physical normalization split.

Classification:

| gate | status |
|---|---|
| positive inertial mass | pass |
| source conservation | pass through norm conservation |
| branch-fixed signed active source | fail |
| source/response locking | not applicable |
| immediate escape hatch | no |

The Born source is the stable retained source. It cannot by itself generate a
negative active gravitational charge because it is nonnegative by construction.
Changing the sign of the potential or response in a later harness is then a
coupling/response convention or an inserted control, not a derived signed
source.

## Case 2: Parity Scalar Variational Source

The parity-correct scalar staggered coupling is:

```text
H_diag = (m + Phi) epsilon(x)
```

Its variational source is:

```text
rho_s = epsilon(x) |psi(x)|^2
```

This is genuinely signed. It is also the source one obtains from the retained
parity scalar action. That makes it the first plausible escape hatch.

It fails the physical signed-source gate for three independent reasons:

| gate | status | failure |
|---|---|---|
| signed | pass | `epsilon` has both signs |
| native variational source | pass | follows from the retained parity scalar coupling |
| positive inertial mass | pass for the norm | inertial norm is still `|psi|^2` |
| branch-fixed monopole | fail | one-site translation flips the sign |
| conserved source charge | fail | kinetic hopping changes scalar charge |
| refinement stability | fail | smooth-packet scalar charge washes out |

Therefore the parity scalar source is not a conserved gravitational branch
label. Treating it as `chi_g` would make the active gravitational monopole
basis- and packet-placement-dependent while the inertial norm stays unchanged.

This is the local source-action obstruction:

```text
rho_s = epsilon |psi|^2
```

is variational, but not branch-stable.

## Case 3: Inserted Signed Charge

The coherent consequence harness uses the algebraic form:

```text
rho_g = chi_g |psi|^2
q_bare = 4 pi chi_g M_phys
```

This is useful as a control because it cleanly separates:

- source-only signs
- response-only signs
- locked source/response signs

The locked table is the only one that gives same-sector attraction,
opposite-sector repulsion, positive inertial mass, and action-reaction for all
two-body pairs.

Classification:

| gate | status |
|---|---|
| positive inertial mass | pass by construction |
| signed active source | pass by insertion |
| action-reaction | pass only if source and response are locked |
| native derivation of `chi_g` | fail |
| source-action escape hatch | no, unless `chi_g` is derived elsewhere |

The Planck/source-unit normalization theorem can carry an already supplied sign:

```text
q_bare = 4 pi chi_g M_phys
```

but it does not derive that sign. It only converts a physical active monopole
to the bare Poisson source coefficient. Using this normalization as a source of
`chi_g` would be source-unit conflation.

## Case 4: Hypothetical New Source Action

A different source action is not ruled out by the local audit, but it must do
real work. To be an actual escape hatch it must supply a theorem, not a
phenomenological sign.

Minimum requirements:

| requirement | meaning |
|---|---|
| native source variable | the action must define an active source density before a sign is inserted by hand |
| conserved `Z2` branch | the sign must be stable under the retained kinetic and scalar-response evolution |
| positive energy/inertia | inertial mass and norm must remain positive in both branches |
| branch-fixed monopole | translating or changing a local basis cannot flip the total active charge |
| source/response locking | the same branch label must multiply active source and response |
| action-reaction closure | mixed-branch two-body forces must balance without negative inertial mass |
| Poisson compatibility | the long-range weak-field limit must reduce to the retained Laplacian Green kernel |
| source-unit discipline | `G_kernel`, `G_Newton,lat`, `q_bare`, and `M_phys` must remain separated |
| tensor/scalar discipline | scalar source changes must not be promoted to a full tensor gravity closure |
| bounded energy | opposite signs must not create an unbounded pair-production/runaway channel |

The hard part is the second and fourth rows. The previous selector scan found
conserved local taste labels, but they are scalar-source neutral. The label that
pins scalar sign, `epsilon`, is kinetic-broken. A new action must evade exactly
that obstruction.

## Failure Modes To Guard

### Basis Dependence

A candidate source that changes sign under a one-site translation, taste-basis
rotation, packet centering choice, or refinement convention is not an active
gravitational branch. It is a representation artifact unless a separate
superselection theorem fixes the basis and proves conservation.

The parity scalar source currently fails here.

### Kinetic Nonconservation

A branch label must commute with the retained free kinetic generator and remain
conserved under the massive scalar surface. A signed density that is produced
by a variational derivative but then oscillates or leaks under free evolution is
not a gravitational charge.

The local `epsilon` branch currently fails here.

### Tensor/Scalar Overreach

The scalar source problem must not be used to claim a full tensor gravity
completion. The scalar-trace/tensor notes leave a separate blocker: scalar
shell or Schur trace data do not determine the full `3+1` metric channels.

A new scalar source action could at most address the signed active monopole
problem. It would not close the full tensor action or full GR route without a
new tensor-valued localization/matching primitive.

### Source-Unit Conflation

The source-unit theorem separates:

```text
G_kernel = 1/(4 pi)
G_Newton,lat = 1
q_bare = 4 pi M_phys
```

With a supplied branch sign this becomes:

```text
q_bare = 4 pi chi_g M_phys
```

The sign is not produced by the unit conversion. Any argument that moves a sign
between `G`, `q_bare`, and `M_phys` without deriving a conserved `chi_g` is only
bookkeeping.

### Energy Runaway

Positive inertial masses with opposite active signs produce repulsive
interactions only if source and response are locked. Source-only or
response-only signs fail mixed-pair action-reaction. A new action must also
show that the energy functional is bounded or constrained enough to avoid
unlimited production of opposite active charges with positive inertial energy.

Passing a static force table is not enough. The action must identify the
conserved charge sector and the bounded Hamiltonian/constraint surface that
prevents runaway.

## Escape-Hatch Table

| route | active source | derived from retained action | signed | conserved branch | positive inertial mass | immediate status |
|---|---|---:|---:|---:|---:|---|
| retained Poisson/Born | `|psi|^2` | yes | no | yes | yes | not signed |
| parity scalar variational | `epsilon |psi|^2` | yes | yes | no | yes | blocked |
| inserted signed charge | `chi_g |psi|^2` | no | yes | conditional | yes | control only |
| hypothetical new action | TBD | TBD | required | required | required | open proof obligation |

## Boundary Verdict

No source-action escape hatch is immediately viable.

The retained Born source is stable but unsigned. The retained parity scalar
source is signed and variational, but not a conserved branch-fixed monopole.
The inserted signed charge gives a coherent consequence harness only after
`chi_g` is supplied externally. A hypothetical new action remains logically
open, but only if it derives a conserved branch-fixed active source, locks that
same branch to response, preserves positive inertial mass, respects the retained
Poisson/source-unit normalization, avoids scalar/tensor overreach, and supplies
an energy stability argument.

Until such an action is written and passes those gates, the signed-gravity lane
remains a consequence/control and no-go-boundary lane, not a physical signed
sector claim.
