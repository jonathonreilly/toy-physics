# Gravity Signed Source-Density Boundary Note

**Date:** 2026-04-25
**Status:** first local source-primitive block for the signed gravitational
response lane
**Script:** [`../scripts/frontier_signed_gravity_source_variational_audit.py`](../scripts/frontier_signed_gravity_source_variational_audit.py)

This note records the P0 source-density audit after
[`SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md`](SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md).

The language boundary is unchanged. This is not a negative-mass, shielding,
propulsion, or reactionless-force claim. "Antigravity" remains shorthand only
for a bounded signed-response search. A physical signed sector still requires a
native or naturally hosted `chi_g = +/-1`, source/response locking, positive
inertial mass, and action-reaction closure.

## Question

The selector scan blocked the simplest local/taste-cell branch operator. The
next possible route was the source primitive:

> Does the retained parity-correct scalar coupling variationally source a
> positive Born density, a signed scalar bilinear, or a branch-fixed signed
> density?

The relevant retained inputs are:

- [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md):
  the Born / mass-density identification `rho = |psi|^2` (used as the
  unsigned baseline source candidate in this note's gate table). This
  replaces a prior citation of `GRAVITY_CLEAN_DERIVATION_NOTE.md` which
  itself consumes this same identification — the prior citation was a
  misattribution that created a length-2 citation cycle in the graph.
- [`GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md)
  and [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md):
  the retained scalar response channel is
  `H_diag = (m + Phi) epsilon(x)`.
- [`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md):
  source-unit normalization separates `G_kernel = 1/(4 pi)` from
  `G_Newton,lat = 1` and gives `q_bare = 4 pi M_phys`.

## Source Forms Audited

The harness keeps four source candidates separate:

```text
rho_B    = |psi|^2
rho_s    = epsilon |psi|^2
rho_Q    = <psi | Q_chi | psi>
rho_g    = chi_g |psi|^2
```

Only the last form has the algebraic shape needed for a locked signed source,
but it is not native unless `chi_g` has already been derived elsewhere.

## Result

Command:

```bash
python3 scripts/frontier_signed_gravity_source_variational_audit.py
```

Summary:

```text
max residual dE/dPhi - response_sign*epsilon*|psi|^2, response +: 1.084e-11
max residual dE/dPhi - response_sign*epsilon*|psi|^2, response -: 1.132e-11
free evolution scalar charge: +4.233389e-02 -> +5.457125e-02
free evolution norm drift: 2.354e-14
FINAL_TAG: SOURCE_PRIMITIVE_BLOCKED_LOCAL
```

The variational derivative of the parity scalar coupling is:

```text
delta E / delta Phi(x) = response_sign * epsilon(x) |psi(x)|^2
```

So the coupling varies to the parity scalar density, not to
`chi_g |psi|^2`.

## Why The Parity Scalar Source Fails As `chi_g`

The parity scalar density is genuinely signed, but it is not a branch-stable
gravitational monopole.

For normalized packets:

| sigma | Born charge | even-centered scalar charge | odd-centered scalar charge |
|---:|---:|---:|---:|
| `0.65` | `1.000000` | `+6.841826e-01` | `-6.841826e-01` |
| `1.25` | `1.000000` | `+4.233389e-02` | `-4.233389e-02` |
| `2.50` | `1.000000` | `+4.014794e-07` | `-4.014794e-07` |

A one-site translation flips the scalar charge while the positive inertial
norm is unchanged. Under free staggered evolution, the scalar charge also
changes while norm stays at numerical precision:

```text
Q_scalar: +4.233389e-02 -> +5.457125e-02
norm drift: 2.354e-14
```

This is not a conserved branch label.

The first continuum/refinement sanity check also rejects the parity scalar
monopole as a stable smooth-packet source:

| h | Born charge | scalar charge |
|---:|---:|---:|
| `1.000` | `1.000000` | `+4.953538e-01` |
| `0.500` | `1.000000` | `+7.762077e-03` |
| `0.250` | `1.000000` | `+4.537555e-10` |
| `0.125` | `1.000000` | `-4.163336e-17` |

The parity scalar charge washes out under refinement for a smooth packet.

## Taste-Cell Branch Check

The source audit reuses the selector scan's conserved neutral labels:

| `Q` | conserved on massive scalar surface | pins `epsilon` sign | `epsilon` spectrum in each branch |
|---|---|---|---|
| `IXY` | yes | no | `[-1,+1]`, mean `0` |
| `XYI` | yes | no | `[-1,+1]`, mean `0` |
| `XZY` | yes | no | `[-1,+1]`, mean `0` |
| `ZZZ = epsilon` | no | yes | `+` branch `+1`, `-` branch `-1` |

This reproduces the selector obstruction in source-density language:

- conserved neutral taste labels exist, but do not pin scalar source sign
- `epsilon` pins scalar sign, but is broken by kinetic hopping and is not a
  conserved branch

Therefore `rho_Q = <Q>` may be a conserved sign expectation for some neutral
labels, but it is not the source selected by the retained scalar coupling.

## Source-Unit Control

The source-unit theorem can carry a sign if a sign has already been supplied:

```text
q_bare = 4 pi chi_g M_phys
```

The control passes the expected bookkeeping gates:

```text
|q_bare| ~ M slope, chi=+1: 1.000000
|q_bare| ~ M slope, chi=-1: 1.000000
null source q_bare: +0.000e+00
same-point inserted +/- q_bare: +0.000e+00
same-point inserted +/- inertial mass sum: 3.500
```

But this is conditional bookkeeping. Source-unit normalization does not derive
`chi_g`; it only says how a derived active source charge would be represented
in the bare Poisson normalization.

## Gate Table

| source form | scalar-variational | signed | branch-fixed | conserved | positive inertial mass | native | candidate |
|---|---|---|---|---|---|---|---|
| `rho = |psi|^2` | no | no | no | yes | yes | yes | no |
| `rho_s = epsilon |psi|^2` | yes | yes | no | no | yes | yes | no |
| `rho_Q = <Q>` | no | yes | no | yes | yes | yes | no |
| `rho_g = chi_g |psi|^2` | no | yes | yes | yes | yes | no | no |

No audited local source form passes the physical signed-sector gate.

## Boundary Verdict

The local source-primitive route is blocked:

> The retained scalar coupling variationally exposes a signed parity scalar
> density, but that density is translation-sensitive, not conserved by
> retained kinetic hopping, and not stable under continuum/refinement. The
> conserved local taste labels are scalar-source neutral. The only form that
> gives the desired signed active source is `chi_g |psi|^2`, and that still
> requires an externally supplied `chi_g`.

This is a local/taste-cell and smooth-packet source-density block, not a global
mathematical impossibility theorem. It does not exclude:

- a nonlocal or boundary selector
- a constrained sector-preparation rule with its own conservation theorem
- a different source action that is not the retained parity scalar coupling
- an explicitly proposed global topological sign

Until one of those is supplied, the signed gravitational response lane remains
a consequence/control harness rather than a physical sector claim.

## Next Work

The next useful work should not be broad family portability. The current P0
state has two local negatives:

```text
NO_GO_STRICT_SELECTOR
SOURCE_PRIMITIVE_BLOCKED_LOCAL
```

The lane should now either:

1. propose a nonlocal or boundary-hosted `chi_g` with a concrete conservation
   theorem target, or
2. land the mechanism-separation and non-claim gates so lensing, complex-action,
   and inserted-charge controls cannot be mistaken for selector evidence.
