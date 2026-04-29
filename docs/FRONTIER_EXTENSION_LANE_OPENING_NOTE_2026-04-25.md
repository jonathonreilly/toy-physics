# Frontier Extension Lane Opening Note

**Date:** 2026-04-25
**Status:** accepted lane-opening note; planning only, not a science claim
surface
**Scope:** open three bounded framework-extension lanes:
native teleportation, chronology protection, and signed gravitational response.

This note is intentionally not part of the manuscript claim surface. It records
the accepted decision to open three new bounded workstreams and defines the
entry conditions, first gates, and language constraints for each one.

No lane opened here is promoted by rhetoric. No theorem status, prediction
status, or package-level publication status changes on `main` as a consequence
of this note alone.

## Accepted Opening Decision

The three targets have different shapes and are not equal flagships.

| target | lane type | accepted label | first decision gate |
|---|---|---|---|
| teleportation | constructive protocol | native taste-qubit teleportation | exact protocol plus no-signaling audit |
| time travel | boundary theorem | chronology protection | no operational past-signaling theorem |
| antigravity | high-risk discovery | signed gravitational response sector | derived or admissible `chi_g` sector with action-reaction |

The accepted framing is:

- teleportation means quantum state teleportation, not matter teleportation or
  FTL transport
- chronology is a no-go / protection lane, not a time-machine lane
- signed gravity is a search for a physical signed-response sector, not
  negative mass, shielding, or propulsion

## Existing Framework Hooks

### Quantum-information hook

The framework already has a local Hilbert/tensor-product surface, exact
`I_3 = 0` on that surface, and retained Bell/CHSH support with explicit
Kogut-Susskind taste measurements.

Starting references:

- [SINGLE_AXIOM_HILBERT_NOTE.md](SINGLE_AXIOM_HILBERT_NOTE.md)
- [I3_ZERO_EXACT_THEOREM_NOTE.md](I3_ZERO_EXACT_THEOREM_NOTE.md)
- [BELL_INEQUALITY_DERIVED_NOTE.md](BELL_INEQUALITY_DERIVED_NOTE.md)
- [logs/retained/bell_chsh_2026-04-17.log](../logs/retained/bell_chsh_2026-04-17.log)

The gap is not whether the framework can host quantum mechanics. The gap is an
explicit native teleportation protocol with encoded taste qubits, Bell
measurement, classical record transport, and correction.

### Chronology hook

The time stack already favors one Hamiltonian clock, codimension-1 Cauchy data,
and one temporal dimension. Multi-time extensions require nonlocal support
constraints incompatible with arbitrary graph-local data, and CTCs sit outside
the retained well-posedness story.

Starting references:

- [ANOMALY_FORCES_TIME_THEOREM.md](ANOMALY_FORCES_TIME_THEOREM.md)
- [CPT_EXACT_NOTE.md](CPT_EXACT_NOTE.md)
- [LIGHT_CONE_FRAMING_NOTE.md](LIGHT_CONE_FRAMING_NOTE.md)
- [CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md](CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md)

The gap is a formal operational boundary: `U(-t)` and CPT/T symmetry are
equation-level reversibility, not controllable channels to an earlier durable
record.

### Signed-gravity hook

The gravity side already has attractive weak-field closure, sign-sensitive
response tests, and several repulsive or sign-flipped regimes. Most of those are
not antigravity: some are interference windows, absorptive complex-action
effects, near-field geometry, or EM-like signed-source companions.

Starting references:

- [GRAVITY_CLEAN_DERIVATION_NOTE.md](GRAVITY_CLEAN_DERIVATION_NOTE.md)
- [GRAVITY_SIGN_AUDIT_2026-04-10.md](GRAVITY_SIGN_AUDIT_2026-04-10.md)
- [LENSING_K_SWEEP_NOTE.md](LENSING_K_SWEEP_NOTE.md)
- [COMPLEX_ACTION_NOTE.md](COMPLEX_ACTION_NOTE.md)
- [ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md](ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md)
- [SIGN_PORTABILITY_INVARIANT_NOTE.md](SIGN_PORTABILITY_INVARIANT_NOTE.md)

The gap is a physical sign selector. A response-only sign flip is a useful toy
control but is not a physical sector unless source sign and response sign are
locked strongly enough to pass two-body action-reaction.

## Lane A: Native Taste-Qubit Teleportation

### Goal

Show that ordinary quantum state teleportation can be implemented using native
`Cl(3)/Z^3` Hilbert, taste, and measurement structures.

### Opened minimal extension

1. Define one encoded logical taste qubit per participant from the
   Kogut-Susskind cell/taste factorization.
2. Build native gate and projector primitives from existing taste Pauli
   operators `X`, `Y`, and `Z`.
3. Implement Bell-pair preparation, Bell-basis measurement, and Bob-side Pauli
   correction.
4. Add a causal two-bit classical record channel.
5. Prove numerically and algebraically that Bob's pre-message reduced state is
   independent of the unknown input state.

### First acceptance gates

- random input states teleport with fidelity `1 - eps` at numerical precision
- all four Bell outcomes are exercised
- Bob's reduced density matrix before receiving the classical bits is input
  independent
- the protocol stays on the Hilbert/taste surface already used by the CHSH lane
- the note explicitly rejects matter teleportation, mass/charge transfer, and
  FTL language

### Initial artifact targets

- `scripts/frontier_teleportation_protocol.py`
- `scripts/frontier_teleportation_resource_from_poisson.py`
- `scripts/frontier_teleportation_causal_channel.py`
- `docs/TELEPORTATION_PROTOCOL_NOTE.md`
- `docs/TELEPORTATION_NO_SIGNALING_AUDIT.md`

### First retained-safe statement if the lane works

> The framework supports standard quantum state teleportation on an encoded
> taste-qubit register, with no operational signaling before the classical
> correction channel arrives.

### Risks

- The existing CHSH resource is entangled but may not be a high-fidelity Bell
  pair without additional preparation.
- Taste observables are defined on a larger cell/taste space, so the logical
  qubit encoding must be fixed carefully.
- Measurement as a durable record remains broader framework work; the first
  teleportation lane should use an explicit classical record model and not claim
  a final measurement derivation.

## Lane B: Chronology Protection

### Goal

Convert the existing single-clock and causal-order machinery into a formal
no-operational-time-travel boundary theorem.

### Opened theorem shape

Under the retained assumptions:

- one strongly continuous Hamiltonian clock `U(t) = exp(-itH)`
- arbitrary admissible local data on one codimension-1 slice
- causal graph / DAG or retarded support semantics
- no extra final-boundary or postselection constraint
- durable records treated as physical degrees of freedom

no operation at clock time `t_1` can alter admissible records or boundary data
at `t_0 < t_1`.

Any operational past-signaling construction must do at least one of:

- introduce a directed causal cycle
- abandon single-clock Cauchy well-posedness
- impose nonlocal fixed-point/final-boundary constraints
- use `U(-t)` while silently reversing the entire record/environment state

### First acceptance gates

- theorem note separates `U(-t)`, CPT/T, retrodiction, Loschmidt echo, and
  operational signaling
- cycle-insertion probe shows failure of partial order / retarded semantics
- record probe shows that inverse evolution changes an earlier record only when
  the record and environment are also reversed
- advanced-field probe is classified as future-boundary import, not a local
  past-directed signal

### Initial artifact targets

- `docs/CHRONOLOGY_PROTECTION_THEOREM_NOTE.md`
- `docs/U_MINUS_T_VS_PAST_SIGNALING_NOTE.md`
- `scripts/chronology_cycle_insertion_probe.py`
- `scripts/loschmidt_echo_record_probe.py`
- `scripts/advanced_vs_retarded_field_probe.py`

### First retained-safe statement if the lane works

> On the retained single-clock, local-data framework surface, the theory admits
> reversible reconstruction but no operational signaling to an earlier durable
> record.

### Risks

- Single-clock evolution is one of the hypotheses. A reviewer can always define
  a different constrained multi-time theory, but that would be outside this
  framework surface.
- Some existing DAG Hamiltonian harnesses are symmetrized compatibility checks,
  not genuinely directed causal transport. Chronology probes should use
  explicitly directed/retarded semantics.
- Interacting CPT is still broader than the free-lattice CPT note, so chronology
  language should not lean on CPT as the main proof.

## Lane C: Signed Gravitational Response Sector

### Goal

Investigate whether the framework can admit a physical repulsive gravitational
sector without negative inertial mass, shielding, or reactionless propulsion.

This lane is opened as a high-risk discovery lane. The working name remains
"signed gravitational response sector," not "antigravity."

### Opened minimal extension

Introduce a conserved gravitational sign/branch label `chi_g = +/-1`, if and
only if it can be derived from, or naturally hosted by, retained `Cl(3)/Z^3`
structure.

The toy field law is:

```text
(-Delta + mu^2) Phi = sum_a chi_a m_a |psi_a|^2
H_a = H0 + response(chi_a Phi)
```

The physical constraint is that source sign and response sign must be locked.
Same-sector pairs then attract; opposite-sector pairs repel. Source-only or
response-only sign flips are controls, not physical sectors.

### First acceptance gates

- identify a candidate origin for `chi_g` rather than inserting it as a free
  phenomenological label
- four-pair table `++`, `+-`, `-+`, `--` gives the expected signs
- two-body action-reaction / momentum-balance control passes
- positive inertial mass is maintained
- Born, norm, null-field, and `F~M` controls remain clean
- continuum/refinement and family-portability checks do not collapse the sign
  sector into a parameter artifact

### Canonical artifact targets

- `docs/SIGNED_GRAVITY_RESPONSE_LANE_STATUS_NOTE_2026-04-26.md`
- `scripts/frontier_signed_gravity_response_lane_status.py`

Branch-level prototype harnesses for locked response, two-body balance,
lensing sign phases, staggered response windows, APS probes, determinant-line
probes, and no-go controls were reviewed. They were consolidated into the
canonical status note and harness rather than imported wholesale.

### First retained-safe statement if the lane works

> The framework admits a bounded signed-response search target. A physical
> antigravity-like sector requires a native `chi_g` selector, source/response
> locking, and two-body action-reaction closure.

### Risks

- The sign selector may not exist. If `chi_g` is only inserted, the lane remains
  a toy model.
- Positive density blocks source repulsion unless a signed source primitive is
  added.
- Existing repulsive rows are often interference-, absorption-, boundary-, or
  parameter-window effects.
- Response-only sign reversal risks one-way forces and should be treated as a
  no-go control unless it is tied to source sign.

### 2026-04-26 Status Update

The signed-response review landed as
[SIGNED_GRAVITY_RESPONSE_LANE_STATUS_NOTE_2026-04-26.md](SIGNED_GRAVITY_RESPONSE_LANE_STATUS_NOTE_2026-04-26.md).
The lane now has a compact status harness:

- locked source/response sign passes the two-body action-reaction consequence
  check;
- source-only and response-only signs remain no-go controls;
- the strict local/taste-cell `chi_g` selector and local signed source
  primitive are blocked;
- the determinant-orientation line is naturally hosted and gives a unique
  `chi_eta` source character inside its grammar, but no canonical physical
  source section or source action is derived.

This update does not promote a physical antigravity, negative-mass, shielding,
propulsion, reactionless-force, or switchable-gravity claim.

## Priority Order

If reviewer bandwidth is limited:

1. Run the teleportation protocol first. It is the fastest clean operational
   win and will sharpen the measurement/record interface.
2. Land the chronology boundary second. It protects the framework from sloppy
   implications of CPT, reversibility, and teleportation.
3. Run the signed-gravity harness third, but treat it as the highest-upside
   physics search.

## Non-Promotion Rule

No lane should be promoted by rhetoric. Promotion requires passing its first
acceptance gates and adding a corresponding theorem/protocol note. Until then,
the only accepted status is:

> lane opened for bounded work; planning only, not a claim surface
