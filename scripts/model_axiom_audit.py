#!/usr/bin/env python3
"""Render the current axiom-level audit for the toy model.

This is an architecture artifact, not a new experiment sweep. It compresses the
current state of the project into four reusable views:

1. axiom status matrix
2. model layer / coupling map
3. retained core vs provisional branches
4. top frontier gaps

The goal is to make the theory bottlenecks explicit before more local scanning.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AxiomStatus:
    number: int
    short_name: str
    implemented: str
    tested: str
    derived: str
    still_assumed: str
    main_gap: str


@dataclass(frozen=True)
class Coupling:
    source: str
    target: str
    status: str
    note: str


AXIOMS = [
    AxiomStatus(
        1,
        "event-network ontology",
        "Y",
        "Y",
        "N",
        "Y",
        "graph growth still functions more as a chosen substrate than as a generator of most physics",
    ),
    AxiomStatus(
        2,
        "persistent self-maintaining patterns",
        "Y",
        "Y",
        "N",
        "Y",
        "the minimal rule-level principle for durable identity or movers is not yet forced",
    ),
    AxiomStatus(
        3,
        "space inferred, not assumed",
        "P",
        "P",
        "N",
        "Y",
        "generated DAGs help, but benchmark geometry and spatial embeddings still inject structure directly",
    ),
    AxiomStatus(
        4,
        "duration as local update count",
        "Y",
        "Y",
        "P",
        "P",
        "the proper-time-like scalar is retained, but its full dynamical role is still incomplete",
    ),
    AxiomStatus(
        5,
        "time arrow via durable records",
        "P",
        "P",
        "N",
        "Y",
        "true endogenous durable records are still missing; the current propagator cleanly preserves the unitary sector but has not yet produced a retained non-unitary mechanism",
    ),
    AxiomStatus(
        6,
        "free continuation prefers local coherence",
        "Y",
        "Y",
        "N",
        "Y",
        "the continuation/action chooser is selected because it works, not yet derived from deeper network rules",
    ),
    AxiomStatus(
        7,
        "inertia as undisturbed continuation",
        "P",
        "Y",
        "P",
        "P",
        "coherent movers exist, but mover dynamics and field response are not yet one clean shared law",
    ),
    AxiomStatus(
        8,
        "gravity as distorted continuation",
        "Y",
        "Y",
        "P",
        "P",
        "the corrected phase-driven rule is strong and the 2D momentum kick is cleaner, but transfer beyond the current 2D log-field setting is still provisional",
    ),
    AxiomStatus(
        9,
        "measurement as durable record formation",
        "P",
        "P",
        "N",
        "Y",
        "record separation is real in operators and topology changes, but durable record formation is not yet endogenous",
    ),
    AxiomStatus(
        10,
        "prefer local persistent explanations",
        "Y",
        "P",
        "N",
        "Y",
        "many mechanisms are local, but several closures are still selected rather than generated",
    ),
]


COUPLINGS = [
    Coupling(
        "graph-growth layer",
        "unitary/path-sum layer",
        "Y",
        "generated DAG interference and gravity survive graph growth and appear on random DAGs",
    ),
    Coupling(
        "graph-growth layer",
        "persistence layer",
        "P",
        "persistent movers live on generated DAGs, but graph evolution does not yet generate the mover physics by itself",
    ),
    Coupling(
        "persistence layer",
        "field / delay layer",
        "Y",
        "persistent or oscillating sources generate delay/field structure used by later probes",
    ),
    Coupling(
        "field / delay layer",
        "unitary/path-sum layer",
        "Y",
        "corrected 1/L^p gravity and steering act through phase / path weighting",
    ),
    Coupling(
        "unitary/path-sum layer",
        "interference observables",
        "Y",
        "Born-safe interference, Sorkin-zero behavior, and generated-DAG visibility all live here",
    ),
    Coupling(
        "record / topology layer",
        "unitary/path-sum layer",
        "Y",
        "topology-changing record operators retime or prune paths and reshape visibility",
    ),
    Coupling(
        "persistence layer",
        "record / topology layer",
        "P",
        "oscillatory, opaque, and node-environment probes exist, but durable endogenous records still do not retain as core",
    ),
    Coupling(
        "field / delay layer",
        "persistence layer",
        "P",
        "static and recent-footprint pattern-sourced fields can steer movers, but the feedback law is still branch-local and incomplete",
    ),
    Coupling(
        "record / topology layer",
        "time-arrow claim",
        "P",
        "the story is philosophically aligned, but the mechanism is not yet one strong endogenous closure",
    ),
]


RETAINED_CORE = [
    "Event-network ontology with local influence links as the primitive substrate.",
    "Local update count plus a retained proper-time-like scalar `sqrt(dt^2-dx^2)` in the kinematic sector.",
    "Linear reversible path-sum propagation with Born-safe interference, machine-precision Sorkin zero on the tested fixed-DAG family, and generated-DAG interference onset under growth.",
    "A comparatively clean unitary sector: Born-safe interference, corrected phase-driven gravity, pure-phase `k=0` limit, weak-coupling `k^2` response, and a near-constant 2D momentum kick from log-field plus path averaging all survive together.",
    "Shared mechanism language across geometry and generated DAGs: completion/load sets the floor, balance selects the branch, bottleneck or placement terms sharpen the readout.",
    "Coherent mover substrate on generated DAGs and viable pattern-sourced steering on the retained `neighbor_radius = 2.5`, `coupling = 3.0`, `last3_union` footprint.",
]


PROVISIONAL_BRANCHES = [
    "Detailed gravity transfer beyond the retained 2D picture, especially any 3D/continuum response law or scattering interpretation.",
    "Durable record formation as a fully endogenous mechanism rather than topology-changing or otherwise selected surrogate operators.",
    "A unified non-unitary law: the current search strongly constrains simple endogenous decoherence mechanisms, but does not yet produce a retained one.",
    "Full field-to-pattern coupling in one clean framework: mover steering is real, but the residual branch architecture is still not universal.",
    "Graph evolution as the source of more of the physics, rather than as a hand-designed substrate on which later layers are placed.",
    "Continuum interpretation: lensing, scattering, and any large-scale force analogue remain provisional or retracted.",
]


TOP_GAPS = [
    (
        "Gap 1",
        "Axioms 1 + 10",
        "Graph evolution should generate more of the physics.",
        "The ontology is event-network first, but too much of the later machinery still sits on chosen graph families, chosen embeddings, or chosen continuation closures.",
    ),
    (
        "Gap 2",
        "Axioms 5 + 9",
        "Durable record formation needs a true endogenous mechanism.",
        "Record effects exist, but the current propagator architecture now cleanly separates unitary from non-unitary behavior: tested endogenous node-label, topology, oscillatory, and opaque mechanisms constrain the space without yet yielding one strong local process that reliably turns coexistence into stable, history-carrying separation.",
    ),
    (
        "Gap 3",
        "Axioms 2 + 7 + 8",
        "Persistent movers need to feel the field in the same framework.",
        "Coherent movers, static steering, and pattern-sourced steering all exist, but the field-to-pattern feedback law is still partial and branch-local rather than one retained dynamics.",
    ),
]


def _render_matrix() -> None:
    print("=" * 100)
    print("AXIOM STATUS MATRIX")
    print("=" * 100)
    print("Legend: Y=yes, P=partial, N=no")
    print()
    header = (
        f"{'#':<2}  {'Axiom':<34} {'Impl':<4} {'Test':<4} "
        f"{'Der':<3} {'Assm':<4}  Main gap"
    )
    print(header)
    print("-" * len(header))
    for row in AXIOMS:
        print(
            f"{row.number:<2}  {row.short_name:<34} {row.implemented:<4} {row.tested:<4} "
            f"{row.derived:<3} {row.still_assumed:<4}  {row.main_gap}"
        )
    print()


def _render_couplings() -> None:
    print("=" * 100)
    print("LAYER / COUPLING MAP")
    print("=" * 100)
    print("Status: Y=retained, P=present but incomplete")
    print()
    for coupling in COUPLINGS:
        print(
            f"- {coupling.source} -> {coupling.target} [{coupling.status}]"
        )
        print(f"  {coupling.note}")
    print()
    print("Compressed architecture read:")
    print("  graph growth -> path structure exists")
    print("  persistence -> field -> path-sum exists")
    print("  path-sum -> interference exists")
    print("  record/topology -> path-sum exists")
    print("  field -> persistence is only partial")
    print("  persistence -> durable records is only partial")
    print()


def _render_core_vs_provisional() -> None:
    print("=" * 100)
    print("RETAINED CORE VS PROVISIONAL BRANCHES")
    print("=" * 100)
    print()
    print("Retained core")
    for item in RETAINED_CORE:
        print(f"- {item}")
    print()
    print("Provisional branches / selected closures")
    for item in PROVISIONAL_BRANCHES:
        print(f"- {item}")
    print()


def _render_gaps() -> None:
    print("=" * 100)
    print("TOP FRONTIER GAPS")
    print("=" * 100)
    print()
    for label, axiom_refs, title, body in TOP_GAPS:
        print(f"{label}: {title}")
        print(f"  Axiom pressure: {axiom_refs}")
        print(f"  Why it matters: {body}")
        print()


def _render_bottom_line() -> None:
    print("=" * 100)
    print("BOTTOM LINE")
    print("=" * 100)
    print(
        "The current bottleneck is architectural clarity more than another local "
        "phenomenon hunt. The retained core is already strong enough to say three "
        "things cleanly: the toy has a viable Born-safe path-sum sector, a retained "
        "phase-driven gravity sector, and a shared completion/balance mechanism "
        "language that bridges geometry and generated DAGs. The latest decoherence "
        "lane sharpens the same picture rather than broadening it: the unitary sector "
        "is comparatively well constrained, while the non-unitary sector still needs "
        "a new endogenous mechanism or a new axiom. The main frontier is therefore to "
        "make more of the architecture endogenous: graph growth should generate more "
        "of the physics, durable records should be real local products of the model, "
        "and movers should feel fields in the same framework that already gives them "
        "coherent persistence."
    )


def main() -> None:
    _render_matrix()
    _render_couplings()
    _render_core_vs_provisional()
    _render_gaps()
    _render_bottom_line()


if __name__ == "__main__":
    main()
