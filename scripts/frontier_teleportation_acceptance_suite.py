#!/usr/bin/env python3
"""Consolidated acceptance runner for native taste-qubit teleportation.

Status: bounded planning artifact. This suite orchestrates existing
teleportation scripts and reports coarse PASS/FAIL/SKIP categories. A PASS here
means the bounded script completed and its own hard gates, when present, passed.
It does not promote any open preparation, readout, measurement-apparatus, or
finite-time dynamics limitation.

Claim boundary: ordinary quantum state teleportation only. No matter transfer,
mass transfer, charge transfer, energy transfer, object transport, or
faster-than-light signaling is claimed or tested.
"""

from __future__ import annotations

import argparse
import dataclasses
import enum
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"


class Status(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    TIMEOUT = "TIMEOUT"


@dataclasses.dataclass(frozen=True)
class Candidate:
    script: str
    args: tuple[str, ...] = ()
    note: str = ""


@dataclasses.dataclass(frozen=True)
class ProbeSpec:
    key: str
    title: str
    category: str
    required: bool
    candidates: tuple[Candidate, ...]
    timeout_seconds: float
    highlights: tuple[str, ...] = ()
    missing_is_skip: bool = False


@dataclasses.dataclass(frozen=True)
class Gate:
    name: str
    status: Status


@dataclasses.dataclass(frozen=True)
class ProbeResult:
    spec: ProbeSpec
    status: Status
    script: str | None
    command: tuple[str, ...]
    elapsed_seconds: float
    return_code: int | None
    gates: tuple[Gate, ...]
    metrics: tuple[str, ...]
    reason: str

    @property
    def blocking_failure(self) -> bool:
        return self.status in (Status.FAIL, Status.TIMEOUT)


GATE_RE = re.compile(r"^\s*(?P<name>.+?):\s+(?P<status>PASS|FAIL)\s*$")


def default_probes() -> tuple[ProbeSpec, ...]:
    """Curated bounded suite.

    Defaults intentionally keep trial counts small. The goal is repeated
    acceptance telemetry, not exhaustive parameter hardening.
    """

    return (
        ProbeSpec(
            key="core_protocol",
            title="Core protocol gates",
            category="required",
            required=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_protocol.py",
                    (
                        "--trials",
                        "16",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-12",
                    ),
                ),
            ),
            timeout_seconds=30.0,
            highlights=(
                "minimum corrected-state fidelity",
                "maximum infidelity",
                "max Bell probability error",
                "max pairwise pre-message",
                "post-delivery correction fidelity",
            ),
        ),
        ProbeSpec(
            key="poisson_end_to_end_selected",
            title="End-to-end Poisson positive/null cases",
            category="required",
            required=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_end_to_end_poisson.py",
                    (
                        "--trials",
                        "12",
                        "--seed",
                        "20260425",
                        "--case",
                        "1d_null",
                        "--case",
                        "1d_poisson_chsh",
                        "--fidelity-threshold",
                        "0.90",
                        "--tolerance",
                        "1e-10",
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "High-fidelity threshold",
                r"^\s*1d_null\b",
                r"^\s*1d_poisson_chsh\b",
                "at least one Poisson case passes",
                "null controls do not pass",
            ),
        ),
        ProbeSpec(
            key="causal_channel",
            title="Causal Bell-record channel",
            category="required",
            required=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_causal_channel.py",
                    ("--tolerance", "1e-12"),
                ),
            ),
            timeout_seconds=30.0,
            highlights=(
                "path latency ticks",
                "correct-record fidelity",
                "wrong-bit control fidelity",
                "max pairwise pre-delivery",
            ),
        ),
        ProbeSpec(
            key="measurement_record",
            title="Measurement-record checks",
            category="required",
            required=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_measurement_record.py",
                    (
                        "--trials",
                        "16",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-12",
                    ),
                ),
            ),
            timeout_seconds=30.0,
            highlights=(
                "max premeasurement isometry",
                "max Bell-record probability",
                "max Bob trace distance",
                "minimum post-delivery",
                "maximum post-delivery infidelity",
            ),
        ),
        ProbeSpec(
            key="resource_fidelity_summary",
            title="Resource-fidelity summary",
            category="required-summary",
            required=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_resource_fidelity.py",
                    (
                        "--trials",
                        "16",
                        "--seed",
                        "20260425",
                        "--random-resources",
                        "0",
                        "--tolerance",
                        "1e-10",
                    ),
                ),
            ),
            timeout_seconds=45.0,
            highlights=(
                r"^\s*ideal Phi\+ resource\b",
                "isotropic v=1/3 boundary",
                "isotropic v=0.30",
                "classical qubit average-fidelity benchmark",
                "max exact-vs-Bell-overlap formula error",
            ),
        ),
        ProbeSpec(
            key="noise_fault_summary",
            title="Noise/fault-control summary",
            category="required-summary",
            required=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_noise_fault_controls.py",
                    (
                        "--trials",
                        "16",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-10",
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                r"^\s*ideal reference\b",
                "resource boundary v=1/3",
                "combined moderate controls",
                "stress below deadline threshold",
                "max output trace error",
            ),
        ),
        ProbeSpec(
            key="encoding_portability_summary",
            title="Encoding portability summary",
            category="required-summary",
            required=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_encoding_portability.py",
                    (
                        "--dims",
                        "1,2",
                        "--sides",
                        "2,4",
                        "--trials",
                        "2",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-12",
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "encoding cases surveyed",
                "logical Pauli pass",
                "teleportation/no-signaling pass",
                "maximum infidelity",
                "max pairwise pre-message",
            ),
        ),
        ProbeSpec(
            key="logical_readout_summary",
            title="Logical readout/extraction summary",
            category="required-summary",
            required=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_logical_readout_audit.py",
                    (
                        "--random-inputs",
                        "8",
                        "--seed",
                        "20260425",
                        "--case",
                        "1d_poisson_chsh",
                        "--tolerance",
                        "1e-10",
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "trace extraction validity",
                "traced logical resource",
                "high-fidelity postselection mass",
                "Bob before classical message",
                "native taste-only readout/apparatus",
            ),
        ),
        ProbeSpec(
            key="adiabatic_prep_hook",
            title="Optional finite-time/adiabatic-prep hook",
            category="optional",
            required=False,
            candidates=(
                Candidate(
                    "frontier_teleportation_adiabatic_time_evolution.py",
                    (
                        "--case",
                        "1d_null",
                        "--case",
                        "1d_poisson_chsh",
                        "--runtimes",
                        "5,20",
                        "--schedules",
                        "smoothstep",
                        "--steps-per-unit",
                        "4",
                        "--min-steps",
                        "40",
                        "--random-inputs",
                        "8",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-10",
                    ),
                    note=(
                        "finite-time closed-system diagnostic; not a "
                        "preparation proof"
                    ),
                ),
                Candidate(
                    "frontier_teleportation_adiabatic_prep_probe.py",
                    (
                        "--grid-points",
                        "9",
                        "--case",
                        "1d_null",
                        "--case",
                        "1d_poisson_chsh",
                        "--resource-threshold",
                        "0.90",
                        "--min-gap-threshold",
                        "1e-3",
                        "--exact-adiabatic-threshold",
                        "1e3",
                        "--norm-bound-threshold",
                        "1e5",
                    ),
                    note=(
                        "gap/adiabatic diagnostic only; not a finite-time "
                        "preparation proof"
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "best standard teleportation fidelity",
                "finite-time sensitivity",
                "non-null finite-time rows",
                "verdict:",
                "null/control paths clean",
                "Poisson paths with high endpoint resource",
                "clean-path plausible diagnostics",
                "also below conservative norm-bound threshold",
                "preparation proof demonstrated",
            ),
        ),
        ProbeSpec(
            key="taste_readout_operator_hook",
            title="Optional taste-readout operator/prep hook",
            category="optional",
            required=False,
            candidates=(
                Candidate(
                    "frontier_teleportation_taste_readout_operator_model.py",
                    note="future exact readout-operator model hook",
                ),
                Candidate(
                    "frontier_teleportation_preparation_readout_probe.py",
                    (
                        "--trials",
                        "8",
                        "--seed",
                        "20260425",
                        "--case",
                        "1d_poisson_chsh",
                    ),
                    note="fallback prep/readout diagnostic; no apparatus proof",
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "Audit grid",
                "Bob pre-message separation check",
                "probes=",
                "Cells/spectators can be ignored only",
                "In dim > 1",
                "gap to next distinct",
                "deterministic traced logical resource",
                "aggregate high-fidelity branch mass",
                "preparation/readout protocol demonstrated",
                "Preparation/readout remains unproven",
            ),
        ),
        ProbeSpec(
            key="bell_measurement_circuit_hook",
            title="Optional Bell-measurement circuit hook",
            category="optional",
            required=False,
            candidates=(
                Candidate(
                    "frontier_teleportation_bell_measurement_circuit.py",
                    note="future Bell-measurement circuit hook",
                ),
            ),
            timeout_seconds=45.0,
            highlights=(
                "Acceptance gates",
                "Bell measurement",
                "circuit",
            ),
        ),
        ProbeSpec(
            key="cross_encoding_hook",
            title="Optional three-register cross-encoding hook",
            category="optional",
            required=False,
            candidates=(
                Candidate(
                    "frontier_teleportation_cross_encoding_maps.py",
                    (
                        "--dims",
                        "1,2",
                        "--sides",
                        "2",
                        "--trials",
                        "1",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-12",
                    ),
                    note="bounded cross-map sample",
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "cross-encoding maps surveyed",
                "explicit nonidentity site maps needed",
                "axis-adapted cross maps",
                "wrong conversion control fails",
                "Acceptance gates",
            ),
        ),
    )


def strict_lane_probes() -> tuple[ProbeSpec, ...]:
    """Heavier present-gated profile for the current teleportation lane.

    Required default probes stay blocking. Strict-lane additions are blocking
    when their candidate script exists, but absent candidates SKIP so the suite
    remains usable while parallel workers land future artifacts.
    """

    required_defaults = tuple(probe for probe in default_probes() if probe.required)
    strict_present_gated = (
        ProbeSpec(
            key="finite_time_2d_smoothstep",
            title="Strict finite-time 2D smoothstep result",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_adiabatic_time_evolution.py",
                    (
                        "--case",
                        "2d_null",
                        "--case",
                        "2d_poisson_chsh",
                        "--runtimes",
                        "1,2,5,10,20,40,80",
                        "--schedules",
                        "smoothstep",
                        "--steps-per-unit",
                        "8",
                        "--min-steps",
                        "160",
                        "--random-inputs",
                        "64",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-10",
                    ),
                    note=(
                        "strict-lane finite-time 2D smoothstep diagnostic; "
                        "not a preparation proof"
                    ),
                ),
            ),
            timeout_seconds=180.0,
            highlights=(
                "Numerics:",
                "Case: 2d_null",
                "Case: 2d_poisson_chsh",
                "best standard teleportation fidelity",
                "finite-time sensitivity",
                "null/control paths non-resource",
                "input-independence=",
                "verdict:",
            ),
        ),
        ProbeSpec(
            key="taste_readout_operator_model",
            title="Strict taste-readout operator model",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_taste_readout_operator_model.py",
                    (
                        "--dims",
                        "1",
                        "2",
                        "3",
                        "--sides",
                        "2",
                        "4",
                        "--random-inputs",
                        "16",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane taste-readout operator model; still not "
                        "hardware readout proof"
                    ),
                ),
            ),
            timeout_seconds=90.0,
            highlights=(
                "Audit grid",
                "Case: dim=3 side=4",
                "fixed pair-hop X versus",
                "Bob pre-message separation check",
                "Cells/spectators can be ignored only",
                "In dim > 1",
                "Claim boundary",
            ),
        ),
        ProbeSpec(
            key="bell_measurement_circuit",
            title="Strict Bell-measurement circuit",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_bell_measurement_circuit.py",
                    (
                        "--trials",
                        "64",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane ideal Bell-measurement circuit; apparatus "
                        "dynamics remain open"
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "Native logical taste surface",
                "Stabilizer Bell projectors",
                "Logical circuit decomposition",
                "Bell outcomes exercised",
                "minimum corrected fidelity",
                "maximum corrected infidelity",
                "max pairwise pre-message",
            ),
        ),
        ProbeSpec(
            key="three_register_cross_encoding",
            title="Strict three-register cross-encoding",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_three_register_cross_encoding.py",
                    (
                        "--dims",
                        "1,2,3",
                        "--sides",
                        "2,4",
                        "--trials",
                        "4",
                        "--max-triples-per-geometry",
                        "512",
                        "--seed",
                        "20260425",
                        "--tolerance",
                        "1e-12",
                    ),
                    note="strict-lane bounded three-register cross-encoding audit",
                ),
            ),
            timeout_seconds=180.0,
            highlights=(
                "Valid KS geometries surveyed",
                "triples surveyed",
                "axis_adapted_three_register_cross_encoding",
                "unexpected result count",
                "minimum corrected-state fidelity",
                "max pairwise pre-message",
                "axis-adapted three-register maps",
                "wrong B resource conversion control",
            ),
        ),
        ProbeSpec(
            key="native_record_apparatus",
            title="Strict native record apparatus/carrier",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_native_record_apparatus.py",
                    (
                        "--trials",
                        "64",
                        "--seed",
                        "20260426",
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane native record apparatus/carrier candidate; "
                        "still not a detector or field-equation derivation"
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "record code:",
                "generated Bell labels",
                "carrier payloads derived from apparatus",
                "carrier pulse worldlines local",
                "max pairwise pre-delivery",
                "minimum delivered-record corrected fidelity",
                "wrong-record mean fidelity control",
            ),
        ),
        ProbeSpec(
            key="record_field_closure",
            title="Strict record-field durability ledger probe",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_record_field_closure.py",
                    (
                        "--trials",
                        "64",
                        "--seed",
                        "20260426",
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane local record-field/durability/ledger "
                        "candidate; still not a retained detector derivation"
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "eikonal max residual",
                "field-derived routes local/monotone",
                "max pairwise pre-delivery",
                "minimum field-delivered corrected fidelity",
                "adversarial pointer code",
                "thermal pointer proxy",
                "conservation ledgers",
            ),
        ),
        ProbeSpec(
            key="apparatus_dynamics_closure",
            title="Strict apparatus dynamics closure candidate",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_apparatus_dynamics_closure.py",
                    (
                        "--trials",
                        "64",
                        "--seed",
                        "20260426",
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane coupled field/bath/apparatus dynamics "
                        "candidate; still not a microscopic detector proof"
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "retarded field front",
                "finite-strength transducer",
                "finite spin bath",
                "Bob before field record delivery",
                "minimum corrected fidelity after delivered record",
                "apparatus conservation",
            ),
        ),
        ProbeSpec(
            key="microscopic_closure",
            title="Strict microscopic transducer/thermo/ledger closure",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_microscopic_closure.py",
                    (
                        "--dim",
                        "3",
                        "--side",
                        "2",
                        "--logical-axis",
                        "2",
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane native stabilizer Hamiltonian, "
                        "thermodynamic bound, and native ledger theorem"
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "native retained-axis stabilizers",
                "Hamiltonian transducer algebra",
                "finite-time Hamiltonian write",
                "thermodynamic detector theorem",
                "native ledger theorem class",
            ),
        ),
        ProbeSpec(
            key="remaining_blocker_reduction",
            title="Strict remaining-blocker reduction",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_remaining_blocker_reduction.py",
                    (
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane conditional uniqueness, side-4 sparse "
                        "resource, readout/correction, support-front, and "
                        "detector-class theorem checks"
                    ),
                ),
            ),
            timeout_seconds=60.0,
            highlights=(
                "conditional transducer uniqueness",
                "causal support carrier",
                "G=5000",
                "retained-axis readout/correction apparatus",
                "independent-fragment detector theorem",
            ),
        ),
        ProbeSpec(
            key="hard_blocker_attack",
            title="Strict hard-blocker attack",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_hard_blocker_attack.py",
                    (
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane obstruction, side-6 scaling control, "
                        "pulse schedule, and material spin-bath detector checks"
                    ),
                ),
            ),
            timeout_seconds=90.0,
            highlights=(
                "sole-axiom apparatus obstruction",
                "amplitude-level field obstruction",
                "side=6, G=20000",
                "calibrated pulse schedule",
                "material spin-bath detector model",
            ),
        ),
        ProbeSpec(
            key="nature_grade_push",
            title="Strict nature-grade push",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_nature_grade_push.py",
                    (
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane added-principle selection, signed sparse "
                        "scaling, noisy pulse, and finite-temperature detector checks"
                    ),
                ),
            ),
            timeout_seconds=90.0,
            highlights=(
                "causal-positive minimal action transducer",
                "least-dwell amplitude law",
                "side=8, G=-1000",
                "noisy pulse decoder",
                "finite-temperature detector robustness",
            ),
        ),
        ProbeSpec(
            key="open_item_attack",
            title="Strict open-item attack",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_open_item_attack.py",
                    (
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane bridge-principle, side-10 signed scaling, "
                        "correlated pulse, and Ising-domain detector checks"
                    ),
                ),
            ),
            timeout_seconds=150.0,
            highlights=(
                "retained-action bridge",
                "no-dwell carrier bridge",
                "side=10, G=-1000",
                "finite-size preparation fit",
                "correlated pulse/noise decoder",
                "3D Ising-domain detector proxy",
            ),
        ),
        ProbeSpec(
            key="unconditional_closure_attack",
            title="Strict unconditional-closure attack",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_unconditional_closure_attack.py",
                    (
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane bare-axiom underdetermination, conditional "
                        "scaling theorem, pulse threshold, and detector continuum checks"
                    ),
                ),
            ),
            timeout_seconds=30.0,
            highlights=(
                "bare one-axiom underdetermination witness",
                "minimal variational completion",
                "conditional sparse-resource theorem schema",
                "pulse threshold theorem",
                "thermodynamic Ising detector theorem",
            ),
        ),
        ProbeSpec(
            key="retention_theorem_attack",
            title="Strict retention-theorem attack",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_retention_theorem_attack.py",
                    (
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane selector retention, side-12 signed scaling, "
                        "controller envelope, and material Ising-domain checks"
                    ),
                ),
            ),
            timeout_seconds=30.0,
            highlights=(
                "selector retention theorem",
                "side-12 scaling theorem pressure",
                "local controller envelope",
                "material Ising-domain envelope",
            ),
        ),
        ProbeSpec(
            key="remaining_open_item_attack",
            title="Strict remaining-open-item attack",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_remaining_open_item_attack.py",
                    (
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane selector minimality, side-12 induction target, "
                        "controller requirements, and material requirements"
                    ),
                ),
            ),
            timeout_seconds=30.0,
            highlights=(
                "selector completion minimality",
                "side-12 induction target",
                "side-14 direct solve status",
                "controller requirement envelope",
                "material requirement envelope",
            ),
        ),
        ProbeSpec(
            key="conclusion_boundary",
            title="Strict conclusion boundary",
            category="strict-lane",
            required=True,
            missing_is_skip=True,
            candidates=(
                Candidate(
                    "frontier_teleportation_conclusion_boundary.py",
                    (
                        "--tolerance",
                        "1e-12",
                    ),
                    note=(
                        "strict-lane terminal planning boundary with explicit "
                        "nature-grade hold"
                    ),
                ),
            ),
            timeout_seconds=30.0,
            highlights=(
                "selector conclusion",
                "scaling conclusion",
                "hardware conclusion",
                "lane conclusion",
                "planning closes while nature-grade closure remains HOLD",
            ),
        ),
    )
    return (*required_defaults, *strict_present_gated)


def existing_candidate(spec: ProbeSpec) -> Candidate | None:
    for candidate in spec.candidates:
        if (SCRIPTS_DIR / candidate.script).is_file():
            return candidate
    return None


def parse_acceptance_gates(stdout: str) -> tuple[Gate, ...]:
    gates: list[Gate] = []
    in_gates = False
    for line in stdout.splitlines():
        if line.strip() == "Acceptance gates:":
            in_gates = True
            continue
        if not in_gates:
            continue
        if not line.strip():
            break
        match = GATE_RE.match(line)
        if match is None:
            continue
        gates.append(
            Gate(
                name=match.group("name").strip(),
                status=Status[match.group("status")],
            )
        )
    return tuple(gates)


def pattern_matches(line: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, line) for pattern in patterns)


def extract_metrics(stdout: str, patterns: Iterable[str], limit: int = 8) -> tuple[str, ...]:
    metrics: list[str] = []
    seen: set[str] = set()
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if not pattern_matches(stripped, patterns):
            continue
        if stripped in seen:
            continue
        seen.add(stripped)
        metrics.append(stripped)
        if len(metrics) >= limit:
            break
    return tuple(metrics)


def tail(text: str, max_lines: int = 8) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines[-max_lines:])


def run_probe(spec: ProbeSpec, python: str, timeout_override: float | None) -> ProbeResult:
    candidate = existing_candidate(spec)
    if candidate is None:
        missing = ", ".join(candidate.script for candidate in spec.candidates)
        status = Status.SKIP if (not spec.required or spec.missing_is_skip) else Status.FAIL
        reason = f"no candidate script present: {missing}"
        if spec.required and spec.missing_is_skip:
            reason = f"present-gated strict-lane candidate absent: {missing}"
        return ProbeResult(
            spec=spec,
            status=status,
            script=None,
            command=(),
            elapsed_seconds=0.0,
            return_code=None,
            gates=(),
            metrics=(),
            reason=reason,
        )

    script_path = SCRIPTS_DIR / candidate.script
    command = (python, str(script_path), *candidate.args)
    start = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout_override or spec.timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - start
        reason = f"timed out after {elapsed:.2f}s"
        if exc.stdout:
            reason += "\nstdout tail:\n" + tail(str(exc.stdout))
        if exc.stderr:
            reason += "\nstderr tail:\n" + tail(str(exc.stderr))
        return ProbeResult(
            spec=spec,
            status=Status.TIMEOUT,
            script=candidate.script,
            command=command,
            elapsed_seconds=elapsed,
            return_code=None,
            gates=(),
            metrics=(),
            reason=reason,
        )

    elapsed = time.monotonic() - start
    stdout = completed.stdout
    stderr = completed.stderr
    gates = parse_acceptance_gates(stdout)
    metrics = extract_metrics(stdout, spec.highlights)
    gate_failed = any(gate.status is Status.FAIL for gate in gates)

    if completed.returncode == 0 and not gate_failed:
        status = Status.PASS
        reason = candidate.note
    else:
        status = Status.FAIL
        reason_parts = [f"return code {completed.returncode}"]
        if gate_failed:
            failed_gates = ", ".join(gate.name for gate in gates if gate.status is Status.FAIL)
            reason_parts.append(f"failed gates: {failed_gates}")
        if stderr.strip():
            reason_parts.append("stderr tail:\n" + tail(stderr))
        elif stdout.strip():
            reason_parts.append("stdout tail:\n" + tail(stdout))
        reason = "\n".join(reason_parts)

    return ProbeResult(
        spec=spec,
        status=status,
        script=candidate.script,
        command=command,
        elapsed_seconds=elapsed,
        return_code=completed.returncode,
        gates=gates,
        metrics=metrics,
        reason=reason,
    )


def selected_probes(args: argparse.Namespace) -> tuple[ProbeSpec, ...]:
    probes = strict_lane_probes() if args.strict_lane else default_probes()
    if args.required_only:
        probes = tuple(probe for probe in probes if probe.required)
    if args.probe:
        requested = set(args.probe)
        known = {probe.key for probe in probes}
        unknown = sorted(requested - known)
        if unknown:
            raise ValueError(f"unknown probe key(s): {', '.join(unknown)}")
        probes = tuple(probe for probe in probes if probe.key in requested)
    return probes


def gate_summary(gates: tuple[Gate, ...]) -> str:
    if not gates:
        return "gates n/a"
    passed = sum(gate.status is Status.PASS for gate in gates)
    return f"gates {passed}/{len(gates)}"


def requirement_label(spec: ProbeSpec) -> str:
    if spec.required and spec.missing_is_skip:
        return "required-if-present"
    return "required" if spec.required else "optional"


def count_by_status(results: Iterable[ProbeResult]) -> Counter[str]:
    return Counter(result.status.value for result in results)


def print_result(result: ProbeResult, show_commands: bool, show_reason_on_pass: bool) -> None:
    required_label = requirement_label(result.spec)
    script = result.script or "none"
    print(
        f"{result.status.value:7s} {result.spec.key:34s} "
        f"[{required_label}] {result.elapsed_seconds:6.2f}s "
        f"{gate_summary(result.gates)} ({script})"
    )
    if show_commands and result.command:
        print("  command: " + " ".join(result.command))
    if result.metrics:
        for line in result.metrics:
            print(f"  metric: {line}")
    if result.reason and (result.status is not Status.PASS or show_reason_on_pass):
        for line in result.reason.splitlines():
            print(f"  note: {line}")


def print_report(
    results: tuple[ProbeResult, ...],
    show_commands: bool,
    show_reason_on_pass: bool,
    strict_optional: bool,
    strict_lane: bool,
) -> None:
    required = tuple(result for result in results if result.spec.required)
    optional = tuple(result for result in results if not result.spec.required)
    elapsed = sum(result.elapsed_seconds for result in results)

    print("NATIVE TASTE-QUBIT TELEPORTATION ACCEPTANCE SUITE")
    print("Status: bounded planning artifact; ordinary quantum state teleportation only")
    print("Repository root: <repo-root>")
    if strict_lane:
        print(
            "Profile: strict-lane; default required probes plus present-gated "
            "current-lane diagnostics"
        )
    exit_policy = "Exit policy: required failures are blocking"
    if strict_optional:
        exit_policy += "; optional failures are blocking in strict mode"
    if strict_lane:
        exit_policy += "; absent strict-lane candidates SKIP"
    print(exit_policy)
    print()

    print("Required probes:")
    for result in required:
        print_result(result, show_commands, show_reason_on_pass)
    print()

    print("Optional hooks:")
    for result in optional:
        print_result(result, show_commands, show_reason_on_pass)
    print()

    required_counts = count_by_status(required)
    optional_counts = count_by_status(optional)
    print("Suite summary:")
    print(f"  required: {dict(sorted(required_counts.items()))}")
    print(f"  optional: {dict(sorted(optional_counts.items()))}")
    print(f"  total probe runtime: {elapsed:.2f}s")
    print()

    print("Limitations:")
    print("  PASS does not prove native preparation, taste-only readout hardware,")
    print("  durable measurement records, Bell-circuit synthesis, finite-time dynamics,")
    print("  or physical transport. Optional absent hooks report SKIP.")
    if strict_lane:
        print("  Strict-lane results remain bounded telemetry, not hardware proof.")
    print("  No matter, mass, charge, energy, object, or FTL transport is claimed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python interpreter for child scripts; defaults to this interpreter",
    )
    parser.add_argument(
        "--required-only",
        action="store_true",
        help="run only blocking required probes",
    )
    parser.add_argument(
        "--strict-optional",
        action="store_true",
        help="make optional hook failures affect the suite exit code",
    )
    parser.add_argument(
        "--strict-lane",
        action="store_true",
        help=(
            "run the strict-lane profile: default required probes plus "
            "present-gated finite-time 2D smoothstep, taste-readout operator, "
            "Bell-measurement circuit, three-register cross-encoding, and "
            "native record-apparatus / record-field / dynamics / microscopic "
            "closure / blocker-reduction / conclusion-boundary checks"
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="override every probe timeout in seconds",
    )
    parser.add_argument(
        "--probe",
        action="append",
        help="run only the named probe key; may be repeated",
    )
    parser.add_argument(
        "--show-commands",
        action="store_true",
        help="print the exact child command for each executed probe",
    )
    parser.add_argument(
        "--show-pass-notes",
        action="store_true",
        help="print notes for successful probes, including fallback-hook notes",
    )
    parser.add_argument(
        "--list-probes",
        action="store_true",
        help="list probe keys and exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    probes = selected_probes(args)

    if args.list_probes:
        for probe in probes:
            required = requirement_label(probe)
            candidates = ", ".join(candidate.script for candidate in probe.candidates)
            print(f"{probe.key:34s} {required:8s} {candidates}")
        return 0

    if args.timeout is not None and args.timeout <= 0:
        raise ValueError("--timeout must be positive when supplied")

    results = tuple(
        run_probe(probe, python=args.python, timeout_override=args.timeout)
        for probe in probes
    )
    print_report(
        results,
        show_commands=args.show_commands,
        show_reason_on_pass=args.show_pass_notes,
        strict_optional=args.strict_optional,
        strict_lane=args.strict_lane,
    )

    required_failed = any(
        result.spec.required and result.blocking_failure for result in results
    )
    optional_failed = any(
        (not result.spec.required) and result.blocking_failure for result in results
    )
    if required_failed or (args.strict_optional and optional_failed):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
