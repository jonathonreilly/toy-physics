#!/usr/bin/env python3
"""Profile generated-family eligibility for non-pocket suppressor transfer rows."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from toy_event_physics import (  # noqa: E402
    _evaluate_extended_ge6_dpadj_nodes,
    _extended_ge6_dpadj_trees,
    canonical_generated_ensemble_specs,
    generated_ensemble_spec,
    pocket_wrap_suppressor_subtype_from_outcomes,
    procedural_geometry_variants,
    randomized_geometry_variants,
    scenario_by_name,
)


SUPPRESSOR_NODES = ((1, 0), (4, 0))
DEFAULT_SCENARIOS = ("taper-wrap", "skew-wrap")
STYLE_ORDER = ("geometry", "walk", "mode-mix", "local-morph")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack-name", default="base")
    parser.add_argument(
        "--scenarios",
        nargs="+",
        default=list(DEFAULT_SCENARIOS),
    )
    parser.add_argument(
        "--ensembles",
        nargs="+",
        default=[spec[0] for spec in canonical_generated_ensemble_specs()],
    )
    parser.add_argument(
        "--stop-on-first-nonempty",
        action="store_true",
        help="stop once a non-empty eligible non-pocket cohort is found",
    )
    return parser


def _evaluate_outcome(
    *,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    ge6_tree: object,
    dpadj_tree: object,
    pack_name: str,
    scenario_name: str,
) -> tuple[str, float, float, float]:
    (
        _actual_label,
        outcome,
        _ge6_prediction,
        _dpadj_prediction,
        _ge6_only_fraction,
        _ge7_core_fraction,
        deep_gap,
        pocket_gap,
        low_degree_gap,
        _boundary_gap,
        _crosses_midline,
        _center_variation,
        _span_range,
    ) = _evaluate_extended_ge6_dpadj_nodes(
        nodes=nodes,
        wrap_y=wrap_y,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
        pack_name=pack_name,
        scenario_name=scenario_name,
        retained_weight=1.0,
    )
    return outcome, deep_gap, pocket_gap, low_degree_gap


def _variant_entries(
    *,
    pack_name: str,
    scenario_name: str,
    ensemble_name: str,
) -> tuple[bool, list[tuple[str, set[tuple[int, int]], str]]]:
    _name, geometry_limit, procedural_limit, procedural_styles = generated_ensemble_spec(
        ensemble_name
    )
    base_nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    entries: list[tuple[str, set[tuple[int, int]], str]] = []
    for variant_name, perturbed_nodes, _node_delta in randomized_geometry_variants(
        pack_name,
        scenario_name,
        base_nodes,
        wrap_y,
        variant_limit=geometry_limit,
    ):
        entries.append(
            (f"{pack_name}:{scenario_name}:{variant_name}", set(perturbed_nodes), "geometry")
        )
    for style in tuple(dict.fromkeys(procedural_styles)):
        for variant_name, perturbed_nodes, _node_delta in procedural_geometry_variants(
            pack_name,
            scenario_name,
            base_nodes,
            wrap_y,
            variant_limit=procedural_limit,
            style=style,
        ):
            entries.append(
                (f"{pack_name}:{scenario_name}:{variant_name}", set(perturbed_nodes), style)
            )
    entries.sort(key=lambda item: (STYLE_ORDER.index(item[2]), item[0]))
    return wrap_y, entries


def _format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{key}:{counter[key]}" for key in sorted(counter))


def render_block(
    *,
    pack_name: str,
    scenario_name: str,
    ensemble_name: str,
    ge6_tree: object,
    dpadj_tree: object,
) -> tuple[str, int]:
    wrap_y, entries = _variant_entries(
        pack_name=pack_name,
        scenario_name=scenario_name,
        ensemble_name=ensemble_name,
    )
    style_counts: dict[str, Counter[str]] = defaultdict(Counter)
    first_examples: dict[str, list[str]] = defaultdict(list)
    eligible_total = 0
    for source_name, nodes, style in entries:
        style_counts[style]["variants"] += 1
        base_outcome, deep_gap, pocket_gap, low_degree_gap = _evaluate_outcome(
            nodes=nodes,
            wrap_y=wrap_y,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            pack_name=pack_name,
            scenario_name=f"{ensemble_name}:{source_name}:base",
        )
        if base_outcome != "dpadj-only":
            style_counts[style]["other_base_outcome"] += 1
            continue
        style_counts[style]["dpadj_only"] += 1

        pocket_signature = pocket_gap > 0.0 and deep_gap <= 0.0 and low_degree_gap <= 0.0
        if pocket_signature:
            style_counts[style]["pocket_signature"] += 1
            continue

        add1_nodes = set(nodes)
        add1_nodes.add(SUPPRESSOR_NODES[0])
        add4_nodes = set(nodes)
        add4_nodes.add(SUPPRESSOR_NODES[1])
        add1_outcome, _d1, _p1, _l1 = _evaluate_outcome(
            nodes=add1_nodes,
            wrap_y=wrap_y,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            pack_name=pack_name,
            scenario_name=f"{ensemble_name}:{source_name}:add-1-0",
        )
        add4_outcome, _d4, _p4, _l4 = _evaluate_outcome(
            nodes=add4_nodes,
            wrap_y=wrap_y,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            pack_name=pack_name,
            scenario_name=f"{ensemble_name}:{source_name}:add-4-0",
        )
        subtype = pocket_wrap_suppressor_subtype_from_outcomes(
            add_1_0_outcome=add1_outcome,
            add_4_0_outcome=add4_outcome,
        )
        style_counts[style]["eligible_nonpocket"] += 1
        style_counts[style][subtype] += 1
        eligible_total += 1
        if len(first_examples[style]) < 3:
            first_examples[style].append(source_name)

    lines = [
        f"scenario={scenario_name} ensemble={ensemble_name}",
        "-" * (19 + len(scenario_name) + len(ensemble_name)),
        f"eligible_nonpocket_total={eligible_total}",
    ]
    for style in STYLE_ORDER:
        counter = style_counts.get(style)
        if not counter:
            continue
        examples = first_examples.get(style, [])
        example_text = ", ".join(examples) if examples else "none"
        lines.append(
            "  "
            + f"{style}: variants={counter['variants']} "
            + f"dpadj_only={counter['dpadj_only']} "
            + f"pocket_signature={counter['pocket_signature']} "
            + f"eligible_nonpocket={counter['eligible_nonpocket']} "
            + f"other_base_outcome={counter['other_base_outcome']} "
            + f"subtypes={_format_counter(Counter({key: value for key, value in counter.items() if key.endswith('-sensitive')}))} "
            + f"examples={example_text}"
        )
    return "\n".join(lines), eligible_total


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(
        f"generated ensemble eligibility profile started {started}",
        flush=True,
    )
    total_start = time.time()
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees(retained_weight=1.0)

    scenarios = list(dict.fromkeys(args.scenarios))
    ensembles = list(dict.fromkeys(args.ensembles))
    first_nonempty: tuple[str, str] | None = None
    eligible_total = 0
    scanned_targets: list[tuple[str, str, int]] = []
    should_stop = False
    for scenario_name in scenarios:
        for ensemble_name in ensembles:
            block, block_eligible = render_block(
                pack_name=args.pack_name,
                scenario_name=scenario_name,
                ensemble_name=ensemble_name,
                ge6_tree=ge6_tree,
                dpadj_tree=dpadj_tree,
            )
            scanned_targets.append((scenario_name, ensemble_name, block_eligible))
            eligible_total += block_eligible
            print()
            print(block, flush=True)
            if first_nonempty is None and block_eligible > 0:
                first_nonempty = (scenario_name, ensemble_name)
                if args.stop_on_first_nonempty:
                    should_stop = True
                    break
        if should_stop:
            break

    print()
    print("Generated Ensemble Eligibility Profile")
    print("====================================")
    print(f"pack_name={args.pack_name}")
    print("scenarios=" + ",".join(scenarios))
    print("ensembles=" + ",".join(ensembles))
    print(f"eligible_nonpocket_total={eligible_total}")
    if first_nonempty is None:
        print("first_nonempty_target=none within tested targets")
    else:
        print(
            "first_nonempty_target="
            + f"{args.pack_name}:{first_nonempty[0]}:{first_nonempty[1]}"
        )
    print(
        "targets_scanned="
        + ",".join(
            f"{scenario}:{ensemble}:{eligible}"
            for scenario, ensemble, eligible in scanned_targets
        )
    )
    print()
    print(
        "generated ensemble eligibility profile completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
