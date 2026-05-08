# Signed Gravitational Response Selector Boundary Note

**Date:** 2026-04-25
**Status:** first-pass discovery-lane boundary note; not a claim surface
**Lane:** signed gravitational response sector

This note records the first concrete pass on the signed gravitational response
lane opened in
[`FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md`](FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md).

The term "antigravity" remains shorthand only. This is not a negative-mass,
shielding, propulsion, or reactionless-force claim. The only admissible target
is a bounded signed-response sector with positive inertial mass, a native or
naturally hosted branch label `chi_g = +/-1`, source/response locking, and
two-body action-reaction closure.

## Starting References

- [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
- [`GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md)
- [`LENSING_K_SWEEP_NOTE.md`](LENSING_K_SWEEP_NOTE.md)
- [`COMPLEX_ACTION_NOTE.md`](COMPLEX_ACTION_NOTE.md)
- [`ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md`](ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md)
- [`SIGN_PORTABILITY_INVARIANT_NOTE.md`](SIGN_PORTABILITY_INVARIANT_NOTE.md)
- [`STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md`](STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md)
- [`STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md`](STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md)
- [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)

## Candidate Selector

The narrow candidate is:

> `chi_g` is a conserved `Z2` orientation of the staggered scalar-density /
> taste-parity mass branch: the sign of the scalar source bilinear relative to
> the parity-correct scalar response channel.

Why this is naturally hosted:

- The retained staggered scalar coupling is parity-correct:
  `H_diag = (m + Phi) epsilon(x)`, not an identity shift.
- The `Cl(3)` taste space already carries exact discrete parity/taste
  structure, including even-sector and `Z2` involution machinery.
- A signed scalar-density orientation is structurally closer to the existing
  electrostatic signed-source lane than to an inserted force sign.
- If such an orientation is superselected, the same branch label can multiply
  both the source term and the response term.

What is not derived:

- No theorem here proves that the gravitational source is the signed scalar
  bilinear rather than the positive Born density.
- No theorem here proves that `chi_g` is conserved in the full interacting
  theory.
- No sector-preparation mechanism is supplied.
- No claim is made that ordinary matter can switch branch or shield gravity.

So the status is **hosted candidate, not derived selector**.

## Minimal Sign Algebra

The harness tests three possibilities:

| mode | source sign | response sign | status |
|---|---:|---:|---|
| source-only | `chi` | `+1` | control |
| response-only | `+1` | `chi` | control |
| locked | `chi` | `chi` | candidate algebra |

For two bodies A and B with positive inertial masses, the pair interaction is
implemented as:

```text
U_A|B = - response_A * source_B * m_A m_B G(r)
```

The left-body force is proportional to `response_A * source_B`; the right-body
force is proportional to `- response_B * source_A`. Momentum balance therefore
requires:

```text
response_A * source_B = response_B * source_A
```

That equality is automatic for the locked case and fails for mixed-sign pairs
in the source-only and response-only controls.

## Four-Pair Table

`++` and `--` mean same-sector pairs. `+-` and `-+` mean opposite-sector pairs.

| mode | `++` | `+-` | `-+` | `--` |
|---|---|---|---|---|
| source-only | attract, balanced | unbalanced | unbalanced | repel, balanced |
| response-only | attract, balanced | unbalanced | unbalanced | repel, balanced |
| locked | attract, balanced | repel, balanced | repel, balanced | attract, balanced |

Only the locked table has the desired structure: same-sector attraction,
opposite-sector repulsion, and action-reaction for all four pairs.

## Scripts Added

- [`../scripts/gravity_signed_sector_harness.py`](../scripts/gravity_signed_sector_harness.py)
- [`../scripts/signed_gravity_two_body_action_reaction.py`](../scripts/signed_gravity_two_body_action_reaction.py)
- [`../scripts/staggered_antigravity_response_window.py`](../scripts/staggered_antigravity_response_window.py)
- [`../scripts/lensing_sign_phase_diagram.py`](../scripts/lensing_sign_phase_diagram.py)

## First Harness Results

Command:

```bash
python3 scripts/gravity_signed_sector_harness.py
```

Key output:

| gate | result |
|---|---:|
| locked two-body balance | max residual `0.000e+00` |
| source-only mixed-pair control | max residual `2.000e+00` |
| response-only mixed-pair control | max residual `2.000e+00` |
| positive inertial mass | pass, minimum tested `m = 1.000` |
| Born `|I3|/P` on fixed branch Hamiltonian | `9.001e-16` |
| Crank-Nicolson norm drift | `2.442e-15` |
| null-field branch delta | `0.000e+00` |
| same-sector `F~M` slope | `1.000000` |
| opposite-sector `F~M` slope | `1.000000` |
| inverse-square / screened / softened-kernel sign portability | pass |
| soft-lattice refinement to inverse-square force | monotone pass |

The continuum/refinement sanity check used softened lattice kernels at
`h = 1.0, 0.5, 0.25, 0.125`; the relative force errors against the
inverse-square reference were:

```text
1.462e-01, 4.027e-02, 1.033e-02, 2.599e-03
```

## Two-Body Control

Command:

```bash
python3 scripts/signed_gravity_two_body_action_reaction.py
```

Result:

- source-only and response-only controls fail mixed-pair momentum balance with
  residual `2.000e+00`
- locked signs pass every pair, mass ratio, and separation row with residual
  `0.000e+00`
- inertial masses are always positive; the sign is not a negative-mass sign

This is the main action-reaction gate.

## Staggered Response Window

Command:

```bash
python3 scripts/staggered_antigravity_response_window.py
```

The parity-correct staggered response hosts a clean branch-product window. At
strength `0.060`, the locked rows were:

| pair | displacement read |
|---|---:|
| `++` | `+2.9817e-02` toward |
| `+-` | `-2.9844e-02` away |
| `-+` | `-2.9844e-02` away |
| `--` | `+2.9817e-02` toward |

Norm drift stays at `~1e-15` and the zero-strength displacement is exactly zero
to printed precision.

Safe interpretation:

- the staggered parity scalar channel can host the branch-product response
  algebra
- this does not derive a conserved `chi_g`
- source-only and response-only response rows remain controls until the
  two-body action-reaction gate is included

## Lensing Phase Boundary

Command:

```bash
python3 scripts/lensing_sign_phase_diagram.py
```

The small lensing phase diagram deliberately separates `chi`-product sign from
wave-interference sign. On the tested light harness:

```text
chi_product=+1 TOWARD rows: 1/8
chi_product=-1 AWAY rows:   5/8
```

This agrees with the earlier lensing `k`-sweep boundary: lensing sign flips can
be wave-phase diagnostics. They are not a selector for `chi_g`, and they should
not be promoted as a physical signed-gravity sector.

## Acceptance Gate Status

| gate | first-pass status |
|---|---|
| candidate origin for `chi_g` | hosted candidate identified: scalar-density/taste-parity branch |
| free phenomenological sign avoided | partially: harness ties source and response signs to one branch label |
| four-pair table | pass |
| source-only / response-only controls | pass as no-go controls |
| two-body action-reaction | pass only for locked signs |
| positive inertial mass | pass |
| Born control | pass on fixed linear branch Hamiltonian |
| norm control | pass under Hermitian CN evolution |
| null-field control | pass |
| `F~M` control | pass |
| continuum/refinement sanity | pass at algebra/kernel level |
| family portability sanity | pass across inverse-square, screened, and softened kernels |
| native conservation theorem | local/taste-cell route now blocked by `NO_GO_STRICT_SELECTOR` |
| native signed source primitive | local parity/taste route now blocked by `SOURCE_PRIMITIVE_BLOCKED_LOCAL` |
| full physical sector claim | not made |

## P0 Follow-Up Status

Two follow-up P0 notes now narrow the lane:

- `SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md` (sibling artifact;
  cross-reference only — not a one-hop dep of this note)
  finds no local Pauli-string involution on the retained 8D taste cell that is
  both conserved on the massive parity-scalar surface and able to pin scalar
  source sign.
- `GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md` (sibling follow-up
  artifact; cross-reference only — that note cites `chi_selector` as its
  predecessor, not this note)
  finds that the retained scalar coupling varies to `epsilon|psi|^2`, which is
  signed but not branch-stable, not conserved by kinetic hopping, and not a
  smooth continuum monopole. The inserted `chi_g|psi|^2` source remains a
  control, not a derivation.

The remaining open space is therefore not ordinary family portability. It is a
broader nonlocal/boundary selector or a different source action with its own
conservation theorem.

## Boundary Verdict

The first pass supports the following limited statement:

> A signed gravitational response sector has a coherent minimal algebra if a
> single conserved `chi_g` label locks source and response signs. In that
> locked algebra, same-sector pairs attract, opposite-sector pairs repel,
> positive inertial mass is retained, and two-body action-reaction closes.

The first pass does not support the stronger statement:

> The framework has derived a physical antigravity sector.

The remaining blocker is the native selector/source theorem beyond the local
parity/taste-cell surface. If the sign cannot be derived or naturally
superselected, the lane remains a toy/control model, not a physics claim.
