# Teleportation Acceptance Suite Note

Status: bounded planning artifact. This note documents
`scripts/frontier_teleportation_acceptance_suite.py`, a consolidated runner for
ordinary native taste-qubit quantum state teleportation checks.

## Scope

The suite runs existing teleportation artifacts as child processes and reports
coarse PASS/FAIL/SKIP categories. It is intentionally a harness, not a new
physics claim and not an implementation of preparation, apparatus dynamics, or
physical transport.

Claim boundary:

- Ordinary quantum state teleportation only.
- No matter, mass, charge, energy, or object transfer.
- No faster-than-light signaling.
- No proof of native preparation, durable records, Bell-circuit synthesis,
  taste-only readout hardware, or finite-time adiabatic dynamics.

## Default Required Probes

The default blocking probes are selected to be lightweight enough for repeated
use:

- `core_protocol`: native taste encoding, Bell projectors, ideal teleportation,
  Bob pre-message input-independence, and causal two-bit record gates.
- `poisson_end_to_end_selected`: selected `1d_null` and `1d_poisson_chsh`
  end-to-end Poisson cases, checking that the null does not pass and the
  positive case does pass high-fidelity gates.
- `causal_channel`: explicit directed Bell-record channel checks.
- `measurement_record`: ideal orthogonal Bell-measurement record model checks.
- `resource_fidelity_summary`: non-ideal two-qubit Bell-resource threshold and
  no-signaling summaries.
- `noise_fault_summary`: resource/noise/readout-control threshold summaries.
- `encoding_portability_summary`: bounded taste-encoding portability summary.
- `logical_readout_summary`: logical trace/readout audit summary, including the
  explicit limitation that native taste-only apparatus is not established.

## Optional Hooks

Optional hooks are non-blocking by default. If a hook candidate is absent, the
suite reports SKIP rather than FAIL. `--strict-optional` makes present optional
hook failures affect the exit code.

Current optional hook surfaces:

- `adiabatic_prep_hook`: prefers the finite-time adiabatic evolution diagnostic
  when present, otherwise falls back to the finite grid adiabatic/gap probe.
  Both are diagnostics only, not preparation proofs.
- `taste_readout_operator_hook`: prefers a future taste-readout operator model
  if present, otherwise falls back to the preparation/readout diagnostic when
  available.
- `bell_measurement_circuit_hook`: Bell-measurement circuit hook when present;
  otherwise SKIP.
- `cross_encoding_hook`: bounded three-register cross-encoding map sample when
  present.

## Strict-Lane Profile

`--strict-lane` switches from the default quick optional hooks to a heavier
current-lane profile. The default required probes remain blocking, and the
strict-lane additions are required if their candidate script exists in the
current worktree:

- `finite_time_2d_smoothstep`: full 2D null and 2D Poisson finite-time
  smoothstep evolution table with the current runtime grid.
- `taste_readout_operator_model`: taste-readout/operator factorization model
  over the current 1D/2D/3D bounded grid.
- `bell_measurement_circuit`: ideal logical/taste Bell-measurement circuit and
  correction audit.
- `three_register_cross_encoding`: bounded three-register A/R/B
  cross-encoding audit.
- `native_record_apparatus`: native record apparatus/carrier candidate for
  local record payloads and causal delivery telemetry.
- `record_field_closure`: local record-field durability and conservation-ledger
  probe.
- `apparatus_dynamics_closure`: coupled field/bath/apparatus dynamics
  candidate.
- `microscopic_closure`: native stabilizer Hamiltonian, thermodynamic bound,
  and native ledger probe.
- `remaining_blocker_reduction`: conditional reduction checks for the current
  selector, support-front, readout/correction, and detector-class blockers.
- `hard_blocker_attack`: obstruction and scaling-control checks for the
  remaining hard blocker packet.
- `nature_grade_push`: added-principle, signed-scaling, noisy-pulse, and
  finite-temperature detector stress packet.
- `open_item_attack`: bridge-principle, side-10 scaling, pulse/noise, and
  detector-proxy attack packet.
- `unconditional_closure_attack`: bare-axiom underdetermination, conditional
  scaling, pulse-threshold, and detector-continuum checks.
- `retention_theorem_attack`: selector-retention, side-12 scaling,
  controller-envelope, and material-domain checks.
- `remaining_open_item_attack`: selector minimality, side-12 induction,
  side-14 direct-solve status, and requirements-envelope checks.
- `conclusion_boundary`: terminal planning-boundary check that explicitly keeps
  nature-grade closure on hold.

These probes are "required-if-present": a present script must pass its own
return-code and gate checks, while an absent candidate reports SKIP so parallel
work on future artifacts does not make the suite brittle. This profile is still
bounded telemetry. It is not proof of preparation hardware, taste-only readout
hardware, durable measurement records, physical Bell-measurement apparatus, or
finite-time preparation in a real device.

The synchronized probe inventory is generated by:

```bash
python3 scripts/frontier_teleportation_acceptance_suite.py --strict-lane --list-probes
```

The current snapshot is cached at
[`outputs/frontier_teleportation_acceptance_suite_strict_list_probes_2026-05-06.txt`](../outputs/frontier_teleportation_acceptance_suite_strict_list_probes_2026-05-06.txt).

## Usage

Run the suite:

```bash
python3 scripts/frontier_teleportation_acceptance_suite.py
```

Run only blocking required probes:

```bash
python3 scripts/frontier_teleportation_acceptance_suite.py --required-only
```

List probe keys:

```bash
python3 scripts/frontier_teleportation_acceptance_suite.py --list-probes
```

Run the strict-lane profile:

```bash
python3 scripts/frontier_teleportation_acceptance_suite.py --strict-lane
```

List strict-lane probe keys:

```bash
python3 scripts/frontier_teleportation_acceptance_suite.py --strict-lane --list-probes
```

Compile check:

```bash
python3 -m py_compile scripts/frontier_teleportation_acceptance_suite.py
```

## Validation Snapshots

The current default probe inventory is cached at
[`outputs/frontier_teleportation_acceptance_suite_default_list_probes_2026-05-06.txt`](../outputs/frontier_teleportation_acceptance_suite_default_list_probes_2026-05-06.txt).

The current strict-lane probe inventory is cached at
[`outputs/frontier_teleportation_acceptance_suite_strict_list_probes_2026-05-06.txt`](../outputs/frontier_teleportation_acceptance_suite_strict_list_probes_2026-05-06.txt).

The current required-only run is cached at
[`outputs/frontier_teleportation_acceptance_suite_required_only_2026-05-06.txt`](../outputs/frontier_teleportation_acceptance_suite_required_only_2026-05-06.txt)
and reports `required: {'PASS': 8}`.

## Exit Policy

The suite exits nonzero when any required probe is missing, times out, returns a
nonzero child exit code, or reports an explicit failed acceptance gate.

Optional probes:

- absent candidate script: SKIP, non-blocking;
- present script success: PASS;
- present script failure: FAIL, non-blocking unless `--strict-optional` is set.

Strict-lane present-gated probes:

- absent candidate script: SKIP, non-blocking;
- present script success: PASS;
- present script failure or timeout: blocking FAIL/TIMEOUT.

## Reporting Limits

The runner extracts short numeric highlights and child acceptance gate counts.
It does not preserve full child stdout unless a child fails or times out. For
deep diagnosis, run the individual child artifact directly with its own CLI.

PASS means only that the bounded harness and the selected child gates passed.
It does not close the open preparation/readout/circuit/dynamics limitations
listed above.
