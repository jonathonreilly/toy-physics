# Teleportation Resource From Poisson/CHSH: First Audit

Status: planning / first artifact. This note records a narrow audit of whether
the existing Poisson-driven CHSH lane already yields an encoded two-qubit Bell
resource for ordinary quantum state teleportation.

**Audit-conditional perimeter (2026-05-08):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
open_gate`. The audit chain-closure explanation is exact: "The runner
computes the reported reduced-resource diagnostics for the chosen
extraction, but the packet does not close the native preparation/
readout theorem selecting the last taste bit as a physical
deterministic teleportation resource. The note itself keeps that
bridge and broader mass/coupling/boundary hardening open." The
audit-stated repair target (`notes_for_re_audit_if_any`) is exact:
"missing_bridge_theorem: prove the native preparation/readout and
last-taste-bit logical-carrier selection, then rerun the small-
surface checks with the Poisson/CHSH machinery source included in
the restricted packet." This is a **planning / first-artifact**
note: the existing §"Limitation Status" already says the limitation
"has moved, but is not closed" and lists open hardening items
(beyond the two small default surfaces, mass/coupling/boundary
sensitivity, native preparation/readout story, separate
deterministic from postselection, restrict to quantum-state
teleportation only). The audit-conditional perimeter is therefore
exactly the absence of the native preparation/readout theorem
selecting the last taste bit as a physical deterministic carrier;
the runner certificate covers only the small-surface (`1D N=8`,
`2D 4x4`) bounded extraction. Nothing in this edit promotes audit
status; the note remains a first-artifact diagnostic. See "Citation
chain and audit-stated repair path (2026-05-10)" below.

It does not claim matter teleportation, charge transfer, mass transfer, or
faster-than-light transport. The only audited object is a quantum state
teleportation resource extracted from the two-species ground state used by
`scripts/frontier_bell_inequality.py`.

## Script

New runner:

```bash
python3 scripts/frontier_teleportation_resource_from_poisson.py
```

The runner imports the existing Poisson/CHSH machinery, builds the small
ground-state cases, and then extracts a candidate resource as follows:

1. Use the Kogut-Susskind cell/taste factorization already used in the CHSH
   lane.
2. Keep the last taste bit of each species as the logical qubit.
3. Trace over cells and spectator taste bits to get a deterministic two-qubit
   logical resource.
4. Separately scan fixed-environment postselected branches as diagnostics only.
5. Measure Bell overlap, two-qubit CHSH, purity, negativity, and standard
   teleportation fidelity for random input states.

The script also checks the Bell teleportation convention against an ideal
`Phi+` resource before running the Poisson cases.

## Default Run Results

Command:

```bash
python3 scripts/frontier_teleportation_resource_from_poisson.py
```

Protocol sanity:

- Ideal `Phi+` resource mean fidelity: `0.9999999999999996`
- Ideal `Phi+` resource minimum fidelity: `0.9999999999999991`
- Maximum output trace error: `5.551e-16`

| case | full CHSH | traced Bell overlap | traced CHSH | negativity | standard teleportation fidelity | deterministic high-fidelity resource |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `1d_null`, `G=0` | `2.000000` | `0.500000` (`Psi+`) | `2.000000` | `0.000000` | mean `0.669817`, min `0.500038`, max `0.987949` | no |
| `1d_poisson_chsh`, `G=1000` | `2.822668` | `0.997963` (`Phi+`) | `2.822668` | `0.497963` | mean `0.998621`, min `0.997964`, max `0.999470` | yes |
| `2d_poisson_chsh`, `G=1000` | `2.668376` | `0.970283` (`Phi+`) | `2.745662` | `0.470283` | mean `0.979360`, min `0.970287`, max `0.999810` | yes |

Postselected diagnostic branches:

| case | best branch Bell overlap | probability | branch CHSH | branch negativity |
| --- | ---: | ---: | ---: | ---: |
| `1d_null` | `0.500000` (`Psi+`) | `6.250000e-02` | `2.000000` | `0.000000` |
| `1d_poisson_chsh` | `0.998981` (`Phi+`) | `2.497454e-01` | `2.825546` | `0.498981` |
| `2d_poisson_chsh` | `0.999428` (`Psi+`) | `5.854540e-08` | `2.826809` | `0.499428` |

## Interpretation

The `G=0` null case does not produce an entangled Bell resource under this
extraction: the best Bell overlap is `0.500000` and negativity is zero.

The two audited Poisson/CHSH cases are positive on the deterministic traced
logical resource: both exceed the script's `0.90` Bell-overlap threshold and
both give high standard teleportation fidelity in the ideal Bell-measurement
protocol. This is stronger than merely observing a full-state CHSH violation.

The postselected branches are not promoted as resources here. They are useful
diagnostics, but a postselection scan is not a deterministic resource
preparation protocol.

## Limitation Status

The limitation has moved, but it is not closed.

Previous limitation: no Poisson-resource derivation artifact for teleportation.

Current status: small-surface positive first artifact. The existing Poisson/CHSH
ground-state machinery can yield a high-fidelity encoded two-qubit resource on
the audited `1D N=8` and `2D 4x4` cases after tracing to the last taste bit per
species.

Still open before promotion:

- Harden beyond the two small default surfaces.
- Check mass, coupling, dimension, boundary, and degeneracy sensitivity.
- Add a native preparation/readout story for the logical resource, not only an
  offline ground-state extraction.
- Separate deterministic traced extraction from diagnostic postselection.
- Keep the claim restricted to quantum state teleportation.

## Citation chain and audit-stated repair path (2026-05-10)

The audit verdict (2026-05-08, see top of note) flags that the
runner's reduced-resource diagnostics support the small-surface
positive observation, but the packet does not close the native
preparation/readout theorem selecting the last taste bit as a
deterministic teleportation resource. The cited authority chain on
this row currently stands as follows.

| Cited authority | Note / file | Effective status (2026-05-10) | Conditional on |
|---|---|---|---|
| Poisson/CHSH small-surface ground states | `scripts/frontier_bell_inequality.py` (imported by this runner) | source script in repo | restricted-packet inclusion of the Poisson/CHSH machinery source |
| This row's runner | `scripts/frontier_teleportation_resource_from_poisson.py` | runner produces the quoted certificate | bounded extraction on `1D N=8` and `2D 4x4` only |
| Adjacent retained Poisson resource sweep | [`TELEPORTATION_POISSON_RESOURCE_SWEEP_NOTE.md`](TELEPORTATION_POISSON_RESOURCE_SWEEP_NOTE.md) | `unaudited` (bounded_theorem) | adjacent diagnostic; not a substitute for the missing bridge theorem |
| Adjacent retained resource fidelity note | [`TELEPORTATION_RESOURCE_FIDELITY_NOTE.md`](TELEPORTATION_RESOURCE_FIDELITY_NOTE.md) | `audited_clean` (bounded_theorem) | bounded fidelity protocol; not a derivation of last-taste-bit selection |
| Adjacent retained measurement-record / apparatus-dynamics-closure | [`TELEPORTATION_MEASUREMENT_RECORD_NOTE.md`](TELEPORTATION_MEASUREMENT_RECORD_NOTE.md), [`TELEPORTATION_APPARATUS_DYNAMICS_CLOSURE_NOTE.md`](TELEPORTATION_APPARATUS_DYNAMICS_CLOSURE_NOTE.md) | `audited_clean` (bounded_theorem) | adjacent bounded results; do not select the last taste bit as native carrier |
| Live retained axiom-set anchor | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | `unaudited` / `meta` | the repository axiom from which native preparation/readout must derive |

The audit-stated repair path (verbatim from
`audit_ledger.json/notes_for_re_audit_if_any`) is to **prove the
native preparation/readout and last-taste-bit logical-carrier
selection**, then **rerun the small-surface checks with the
Poisson/CHSH machinery source included in the restricted packet**.
The first half is a missing bridge theorem from `A_min` /
retained Poisson-CHSH lane to a deterministic native carrier; the
second half is a packet-completeness step that pins the existing
runner to its full upstream chain. Until both land, this row
remains `audited_conditional` and the §"Limitation Status" gating
items above are unchanged. The acknowledged residual is exactly
the missing native preparation/readout theorem; the small-surface
positive numbers in the table are bounded diagnostics, not a
deterministic resource derivation.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not promote audit status
and does not modify any `docs/audit/data/*.json` file.
