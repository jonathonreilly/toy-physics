# Native Teleportation Axioms And Theory Note

**Date:** 2026-04-26
**Status:** planning / candidate theory artifact; not retained framework
promotion
**Companion runner:** `scripts/frontier_teleportation_axiom_closure_checks.py`

## Scope

This note proposes a first native axiom bundle for the taste-qubit
teleportation lane. These are not replacements for the framework's retained
`Cl(3)` on `Z^3` axiom surface. They are candidate lane-level closure
principles: if the teleportation lane is later promoted, these principles say
what must be derived, measured, or rejected.

The theory remains ordinary quantum state teleportation only. It does not
claim matter teleportation, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Native Teleportation Object

The primitive object is not just a state vector. A native teleportation event is
the tuple

```text
T = (Q_A, Q_R, Q_B, rho_RB, h, M_AR, c, gamma_c, C_B)
```

with:

- `Q_A, Q_R, Q_B`: retained logical taste-qubit factors embedded in the
  Kogut-Susskind cell/taste Hilbert space.
- `rho_RB`: the resource state on Alice's resource half and Bob's already
  present register.
- `h in Z2 x Z2`: the Bell-frame label of the resource.
- `M_AR`: Alice's Bell measurement on the input and resource-half factors.
- `c in Z2 x Z2`: the classical Bell record produced by `M_AR`.
- `gamma_c`: a 3D+1 causal worldline carrying `c` from Alice to Bob.
- `C_B`: Bob's retained-axis Pauli correction applied only after `gamma_c`
  reaches Bob.

The useful new object is therefore a framed, causally indexed channel:

```text
unknown state on Q_A
  + resource (rho_RB, h)
  + local Bell record c
  + causal record path gamma_c
  -> reconstructed state on Q_B
```

The record path and Bell frame are part of the data, not decorative
bookkeeping. Without them, the same resource can look like a failed fixed
`Phi+` protocol even when it is a high-fidelity framed resource.

## Boundary Principle

**B0. State-only reconstruction.** Teleportation is admissible only as
reconstruction of an unknown quantum state on Bob's already-present retained
taste-qubit factor. The local matter, mass, charge, energy, and object-support
ledgers are not transported by the protocol.

This is a guardrail, not a physics result. Any future script that reports a
teleportation success must keep this boundary explicit.

## Candidate Lane Axioms

### A1. Retained-Factor Observability

If the protocol traces over cells and spectator taste bits, then a deterministic
logical readout or correction operator must live in

```text
End(Q_r) tensor I_env.
```

Equivalently, a retained logical operation must commute with arbitrary
unobserved environment operations. A fixed-branch operator is allowed only if
the branch is measured, carried as a classical record, and used in a
branch-conditioned correction rule.

Consequence in 3D:

```text
xi_5 = Z_x Z_y Z_z = Z_r * product_{a != r} Z_a
```

is a signed fixed-branch logical `Z_r`, but it is not a traced retained-bit
`Z_r tensor I_env` operator. This turns the readout-convention audit from a
notation warning into a selection rule: raw `xi_5` is rejected for
deterministic traced 3D teleportation unless the spectator branch becomes an
explicit record.

### A2. Bell-Frame Connection

A Poisson-produced Bell resource may land in any of the four Bell sectors. The
sector is a discrete Pauli-frame connection, not automatically a failure and
not automatically invisible.

Use the convention

```text
Phi+ -> h = (0, 0)
Phi- -> h = (1, 0)
Psi+ -> h = (0, 1)
Psi- -> h = (1, 1)
```

where `h = (h_z, h_x)` labels the Bob-side local Pauli frame relative to
`Phi+`. Alice's Bell measurement produces `c = (z, x)`. Bob's correction must
use the composed frame

```text
c_total = c xor h
C_B(c, h) = Z^(z xor h_z) X^(x xor h_x)
```

up to the usual irrelevant Pauli phase convention.

The `3D side=2, G=1000` resource currently lands in the `Psi+` frame, so
`h=(0,1)`. A fixed `Phi+` protocol is expected to fail; a tracked `Psi+ ->
Phi+` frame is expected to pass. This is exactly what the 3D operator-consistent
end-to-end audit reports.

### A3. 3D+1 Causal Record Separability

The entangled quantum resource and the classical Bell record are separate
sectors. The resource can be nonlocal in the ordinary entanglement sense, but
Bob's correction channel is enabled only by a classical two-bit record carried
inside a 3D+1 future cone.

For a speed-one Manhattan record channel:

```text
t_delivery >= t_A + |dx| + |dy| + |dz|.
```

Before that event, Bob's accessible reduced state may contain resource bias,
but it must be independent of Alice's unknown input state. This axiom is the
lane-level no-signaling firewall: the correction is a causal feed-forward
operation, not a hidden superluminal control.

### A4. Native Resource Genesis

A resource is native only if it is supplied with a preparation certificate, not
just an offline diagonalized state. The certificate must include:

- the native Hamiltonian path or dissipative/cooling rule that prepares it;
- the Bell-frame endpoint `h`;
- a ground-tracking or stationarity diagnostic;
- a logical Bell-overlap or teleportation-fidelity diagnostic;
- robustness and scaling controls.

The current `3D side=2` smoothstep ramp is a preparation candidate, because it
starts from a unique, gapped, separable `G=0` state and reaches a high-fidelity
`Psi+` resource at finite time. It is not yet a resource-genesis proof because
it lacks scaling, apparatus, bath/leakage/noise, and physical control
derivations.

### A5. Exhaustive Branch Accounting

No hidden conditioning is allowed. Every branch-sensitive datum must be in one
of three states:

```text
traced out and provably irrelevant;
recorded and causally delivered;
or rejected as an invalid deterministic protocol ingredient.
```

This applies to Bell outcomes, Bell-frame labels, spectator taste branches,
record drops/delays/flips, and preparation-path outcomes. The axiom is what
prevents fixed-spectator algebra from being silently promoted into a traced
operational readout.

## Derived Theory

### Theorem 1: Raw `xi_5` No-Go For Traced 3D Retained-Z

Assume A1 and a 3D retained axis `r`. Since

```text
xi_5 = Z_r S_env,  S_env = product_{a != r} Z_a,
```

and `S_env` is not proportional to `I_env`, `xi_5` is not in
`End(Q_r) tensor I_env`. Therefore raw `xi_5` cannot be used as deterministic
traced retained-bit `Z` in 3D. It can be used only after spectator-branch
measurement and branch-conditioned accounting.

This matches the 3D readout audit:

```text
retained-axis Z_r/X_r: PASS
raw xi_5 as traced Z: FAIL
raw xi_5 Bell projectors: FAIL
```

### Theorem 2: Bell-Frame Covariant Teleportation

Assume A2 and an ideal Bell-sector resource with frame `h`. Standard
teleportation with Alice outcome `c` reconstructs Bob's state after applying
the composed correction `c xor h`, up to Pauli phase convention. Thus the
protocol is covariant under the discrete `Z2 x Z2` Bell-frame group.

Practical consequence: a known `Psi+` resource is a valid framed resource; an
unknown or untracked `Psi+` resource is a fixed-`Phi+` protocol failure.

### Theorem 3: Pre-Delivery Input Independence

Assume A3 and that Bob has not received the record. Alice's local measurement,
averaged over the inaccessible Bell record, is a trace-preserving operation on
the Alice side. Therefore Bob's reduced state before record delivery is the
Bob marginal of the resource and is independent of the unknown input state.

For imperfect resources this marginal need not be exactly `I/2`; the required
condition is pairwise input independence. The 3D resource probe records exactly
this distinction: Bob's marginal has a resource bias, while pairwise
pre-message input distance remains at numerical zero.

### Theorem 4: Closure Is A Product, Not A Fidelity Number

High framed teleportation fidelity is necessary but not sufficient for native
closure. Nature-grade closure requires the product:

```text
retained-factor operator closure
AND Bell-frame calibration
AND native resource genesis
AND 3D+1 causal record delivery
AND exhaustive branch accounting
AND no-transfer boundary accounting
```

If any factor is missing, the lane remains a planning or conditional artifact
even when a small-surface fidelity number is excellent.

## Current Evidence Map

| axiom/theorem | current support | status |
| --- | --- | --- |
| B0 state-only boundary | protocol notes and causal notes reject matter, mass, charge, energy, object, and FTL language | supported guardrail |
| A1 retained-factor observability | 3D readout audit accepts `Z_r/X_r` and rejects raw `xi_5` traced readout | supported on audited finite surfaces |
| A2 Bell-frame connection | 3D resource lands in `Psi+`; fixed `Phi+` fails; tracked frame passes | supported on `3D side=2` |
| A3 3D+1 causal record separability | Manhattan speed-one channel delivers at tick 11 and blocks outside-cone use | supported as explicit channel |
| A4 native resource genesis | finite-time 3D ramp reaches high `Psi+` resource from a simple `G=0` state | candidate only |
| A5 exhaustive branch accounting | Bell outcome, frame, record faults, and raw-`xi_5` branch issues are explicit | partially supported |

## Nature-Grade Closure Blockers

The following blockers remain open and are not solved by this note:

- derive or physically model the durable Bell measurement and record creation;
- derive a 3D+1 record channel from retained field degrees instead of supplying
  it explicitly;
- prove scalable native resource generation beyond the dense `3D side=2`
  surface;
- supply apparatus-level retained-axis logical readout and correction;
- quantify robustness under physical noise, leakage, control errors, and
  finite resources;
- keep Bell-frame calibration operational when the frame is not known
  beforehand;
- establish conservation ledgers showing that no matter, charge, mass, energy,
  or object support is transported.

## Falsifiable Next Tests

The axiom bundle makes concrete near-term tests:

1. A spectator-branch-recorded raw-`xi_5` protocol should pass only when the
   branch record is causally delivered and used in correction.
2. Bell-frame scans should obey the `Z2 x Z2` correction law across all four
   resource frames.
3. A 3D+1 record-channel replacement should reproduce the same no-signaling
   result while deriving the record carrier from native dynamics.
4. Larger 3D resource probes should preserve a calibratable Bell frame and a
   useful gap/preparation path, or the resource-genesis axiom fails to scale.
5. Any attempted deterministic protocol using raw `xi_5` as traced 3D `Z`
   without spectator records should fail the retained-factor guard.

## Status

This theory pass narrows the lane by making the missing structure explicit. It
does not promote the teleportation lane beyond planning / candidate theory
artifact. The strongest current statement remains:

> Standard quantum state teleportation can be represented on native retained
> taste-qubit factors with explicit Bell-frame accounting and a causal 3D+1
> two-bit record channel, on the audited finite surfaces.
