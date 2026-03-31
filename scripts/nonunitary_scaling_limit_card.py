#!/usr/bin/env python3
"""Render the retained non-unitary scaling limit from the latest env sweeps.

This is an architecture artifact, not a new experiment. It compresses the
current scaling evidence into one reusable card:

- which finite-environment architectures were tested
- how much small-graph decoherence they produced
- how that decoherence changed as the graph grew
- what the retained non-unitary conclusion is now
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScalingRow:
    architecture: str
    small_graph: str
    large_graph: str
    scaling: str
    verdict: str


ROWS = [
    ScalingRow(
        architecture="node-label env (fine last-mass label)",
        small_graph="purity 0.5698 @ 6 layers",
        large_graph="purity 0.8858 @ 25 layers",
        scaling="wrong: recoheres as graph grows",
        verdict="small-graph effect only; does not scale",
    ),
    ScalingRow(
        architecture="cumulative-action env (binned action through mass)",
        small_graph="purity 0.6268 @ 6 layers",
        large_graph="purity 0.8856 @ 25 layers",
        scaling="wrong: recoheres as graph grows",
        verdict="better small-graph decoherence, same scaling wall",
    ),
    ScalingRow(
        architecture="evolving-phase env (phase accumulated along edges)",
        small_graph="purity 0.7294 or 1.0000 @ 6 layers",
        large_graph="purity 0.8867 or 1.0000 @ 25 layers",
        scaling="wrong or null: recoheres or stays coherent",
        verdict="does not rescue scaling",
    ),
]


def main() -> None:
    print("=" * 88)
    print("NON-UNITARY SCALING LIMIT CARD")
    print("=" * 88)
    print("Growing-DAG finite-environment architectures")
    print()
    header = (
        f"{'Architecture':<38} {'Small graph':<28} "
        f"{'Large graph':<28} {'Scaling verdict'}"
    )
    print(header)
    print("-" * len(header))
    for row in ROWS:
        print(
            f"{row.architecture:<38} {row.small_graph:<28} "
            f"{row.large_graph:<28} {row.scaling}"
        )
    print()
    print("Retained read")
    print(
        "- Finite-bin partial-trace environments can produce some decoherence on "
        "small generated DAGs, but all tested growing-DAG variants scale the wrong way."
    )
    print(
        "- The problem is no longer best described as 'find a better environment "
        "register'. The current evidence says the system-environment relation itself "
        "must change, or the model needs a new non-unitary axiom."
    )
    print(
        "- This leaves the unitary sector comparatively clean: interference, Born "
        "behavior, and phase-driven gravity survive growth, while scalable "
        "endogenous decoherence does not yet."
    )


if __name__ == "__main__":
    main()
