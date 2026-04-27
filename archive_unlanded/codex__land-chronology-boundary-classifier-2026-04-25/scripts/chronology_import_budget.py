#!/usr/bin/env python3
"""Chronology import budget classifier.

This is a small counted/weighted registry for the chronology import classifier.
It does not prove an absolute impossibility theorem.  It only checks that named
constructions are classified by the imported structure they require outside
the retained single-clock, retarded/local-data surface.
"""

from __future__ import annotations

from dataclasses import dataclass


PASS = 0
FAIL = 0


@dataclass(frozen=True)
class ImportType:
    key: str
    label: str
    weight: int
    definition: str


@dataclass(frozen=True)
class Construction:
    key: str
    label: str
    imports: tuple[str, ...]
    classification: str
    operational_past_signal: bool


IMPORT_TYPES: dict[str, ImportType] = {
    "causal_cycle_fixed_point": ImportType(
        key="causal_cycle_fixed_point",
        label="causal cycle / fixed point",
        weight=2,
        definition=(
            "late-to-early edge or simultaneous fixed-point equation replacing "
            "retained DAG evaluation"
        ),
    ),
    "ctc_consistency": ImportType(
        key="ctc_consistency",
        label="CTC consistency",
        weight=3,
        definition="loop-wide admissibility condition for closed timelike histories",
    ),
    "postselection_final_boundary": ImportType(
        key="postselection_final_boundary",
        label="postselection / final-boundary",
        weight=3,
        definition="later accepted branch or final state used as an admissibility filter",
    ),
    "advanced_future_boundary_support": ImportType(
        key="advanced_future_boundary_support",
        label="advanced future-boundary support",
        weight=2,
        definition="future source degrees supplied to an earlier field solve",
    ),
    "multi_time_nonlocal_support_constraint": ImportType(
        key="multi_time_nonlocal_support_constraint",
        label="multi-time nonlocal support constraint",
        weight=3,
        definition="nonlocal support restriction replacing arbitrary local slice data",
    ),
    "full_closed_state_record_reversal": ImportType(
        key="full_closed_state_record_reversal",
        label="full closed-state record reversal",
        weight=2,
        definition=(
            "inverse evolution of the full closed state, including records, "
            "apparatus, environment, and memories"
        ),
    ),
}


CONSTRUCTIONS: dict[str, Construction] = {
    "retained_retarded_evolution": Construction(
        key="retained_retarded_evolution",
        label="retained retarded evolution",
        imports=(),
        classification="retained zero-budget retarded surface",
        operational_past_signal=False,
    ),
    "advanced_field": Construction(
        key="advanced_field",
        label="advanced field",
        imports=("advanced_future_boundary_support",),
        classification="future-boundary import; not operational past signaling",
        operational_past_signal=False,
    ),
    "postselection": Construction(
        key="postselection",
        label="postselection",
        imports=("postselection_final_boundary",),
        classification="conditional/final-boundary import; not same-run past editing",
        operational_past_signal=False,
    ),
    "ctc_fixed_point": Construction(
        key="ctc_fixed_point",
        label="CTC / fixed-point construction",
        imports=("causal_cycle_fixed_point", "ctc_consistency"),
        classification="global fixed-point and loop-consistency import",
        operational_past_signal=False,
    ),
    "multi_time_support": Construction(
        key="multi_time_support",
        label="multi-time support construction",
        imports=("multi_time_nonlocal_support_constraint",),
        classification="constrained nonlocal support surface outside retained semantics",
        operational_past_signal=False,
    ),
    "full_loschmidt_reversal": Construction(
        key="full_loschmidt_reversal",
        label="full Loschmidt reversal",
        imports=("full_closed_state_record_reversal",),
        classification="reconstruction/global un-writing; not operational past signaling",
        operational_past_signal=False,
    ),
}


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")


def counted_budget(construction: Construction) -> int:
    return len(construction.imports)


def weighted_budget(construction: Construction) -> int:
    return sum(IMPORT_TYPES[key].weight for key in construction.imports)


def imports_label(construction: Construction) -> str:
    if not construction.imports:
        return "none"
    return ", ".join(IMPORT_TYPES[key].label for key in construction.imports)


def print_import_registry() -> None:
    print("IMPORT TYPES")
    for import_type in IMPORT_TYPES.values():
        print(
            f"  - {import_type.key:38s} "
            f"weight={import_type.weight} "
            f"label={import_type.label}"
        )
    print()


def print_budget_table() -> None:
    print("CONSTRUCTION BUDGETS")
    print(
        "  "
        f"{'construction':34s} "
        f"{'count':>5s} "
        f"{'weight':>6s} "
        "classification"
    )
    for construction in CONSTRUCTIONS.values():
        print(
            "  "
            f"{construction.label:34s} "
            f"{counted_budget(construction):5d} "
            f"{weighted_budget(construction):6d} "
            f"{construction.classification}"
        )
        print(f"    imports: {imports_label(construction)}")
    print()


def budget_detail(key: str) -> str:
    construction = CONSTRUCTIONS[key]
    return (
        f"count={counted_budget(construction)}, "
        f"weighted={weighted_budget(construction)}, "
        f"classification={construction.classification}"
    )


def all_import_references_are_defined() -> bool:
    return all(
        import_key in IMPORT_TYPES
        for construction in CONSTRUCTIONS.values()
        for import_key in construction.imports
    )


def main() -> int:
    print("=" * 88)
    print("CHRONOLOGY IMPORT BUDGET")
    print("  Test: apparent late-to-early mechanisms are classified by imports.")
    print("=" * 88)
    print()

    print_import_registry()
    print_budget_table()

    retained = CONSTRUCTIONS["retained_retarded_evolution"]
    advanced = CONSTRUCTIONS["advanced_field"]
    postselection = CONSTRUCTIONS["postselection"]
    ctc = CONSTRUCTIONS["ctc_fixed_point"]
    loschmidt = CONSTRUCTIONS["full_loschmidt_reversal"]

    check(
        "all construction import references are defined",
        all_import_references_are_defined(),
    )
    check(
        "retained retarded evolution budget = 0",
        counted_budget(retained) == 0 and weighted_budget(retained) == 0,
        budget_detail(retained.key),
    )
    check(
        "advanced field budget > 0",
        counted_budget(advanced) > 0 and weighted_budget(advanced) > 0,
        budget_detail(advanced.key),
    )
    check(
        "postselection budget > 0",
        counted_budget(postselection) > 0 and weighted_budget(postselection) > 0,
        budget_detail(postselection.key),
    )
    check(
        "CTC/fixed-point budget > 0",
        counted_budget(ctc) > 0 and weighted_budget(ctc) > 0,
        budget_detail(ctc.key),
    )
    check(
        "multi-time support constraint budget > 0",
        counted_budget(CONSTRUCTIONS["multi_time_support"]) > 0
        and weighted_budget(CONSTRUCTIONS["multi_time_support"]) > 0,
        budget_detail("multi_time_support"),
    )
    check(
        "full Loschmidt reversal budget > 0",
        counted_budget(loschmidt) > 0 and weighted_budget(loschmidt) > 0,
        budget_detail(loschmidt.key),
    )
    check(
        "full Loschmidt reversal is reconstruction, not past signaling",
        "reconstruction" in loschmidt.classification
        and not loschmidt.operational_past_signal,
        (
            f"classification={loschmidt.classification}, "
            f"operational_past_signal={loschmidt.operational_past_signal}"
        ),
    )
    check(
        "positive budget is not promoted to an impossibility proof",
        all(not construction.operational_past_signal for construction in CONSTRUCTIONS.values()),
        "classifier boundary only",
    )

    print()
    print("SAFE READ")
    print("  - Count 0 is retained retarded evolution.")
    print("  - Positive count/weight marks imported structure outside that surface.")
    print(
        "  - The budget is a classifier, not a proof against every imported "
        "theory."
    )
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
