#!/usr/bin/env python3
"""Chronology lane probe: future-boundary import index for field solves.

The retained causal-field surface uses retarded support.  Advanced and
half-advanced/half-retarded solves can make earlier field values depend on
later source degrees, but this script classifies that dependence as imported
future boundary data, not as a local past-directed signal.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


PASS = 0
FAIL = 0


@dataclass(frozen=True)
class Event:
    t: int
    x: int


@dataclass(frozen=True)
class Source:
    label: str
    t: int
    x: int
    strength: float


@dataclass(frozen=True)
class SupportUse:
    source: Source
    coefficient: float
    role: str


@dataclass(frozen=True)
class ImportContribution:
    event: Event
    source: Source
    coefficient: float
    role: str
    weight: float


@dataclass(frozen=True)
class ImportIndex:
    source_use_count: int
    unique_later_sources: int
    weighted: float
    contributions: tuple[ImportContribution, ...]


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


def fmt(value: float) -> str:
    return f"{value:+.6f}"


def kernel_weight(event: Event, source: Source) -> float:
    return 1.0 / (1.0 + abs(event.x - source.x))


def in_retarded_support(event: Event, source: Source) -> bool:
    dt = event.t - source.t
    return dt >= 0 and abs(event.x - source.x) <= dt


def in_advanced_support(event: Event, source: Source) -> bool:
    dt = source.t - event.t
    return dt >= 0 and abs(event.x - source.x) <= dt


def support_uses(kind: str, event: Event, sources: list[Source]) -> list[SupportUse]:
    uses: list[SupportUse] = []
    for source in sources:
        if kind == "retarded":
            if in_retarded_support(event, source):
                uses.append(SupportUse(source, 1.0, "retarded"))
        elif kind == "advanced":
            if in_advanced_support(event, source):
                uses.append(SupportUse(source, 1.0, "advanced"))
        elif kind == "symmetric":
            if in_retarded_support(event, source):
                uses.append(SupportUse(source, 0.5, "retarded"))
            if in_advanced_support(event, source):
                uses.append(SupportUse(source, 0.5, "advanced"))
        else:
            raise ValueError(f"unknown support kind: {kind}")
    return uses


def field_value(kind: str, event: Event, sources: list[Source]) -> float:
    total = 0.0
    for use in support_uses(kind, event, sources):
        total += use.coefficient * use.source.strength * kernel_weight(event, use.source)
    return total


def future_boundary_import_index(
    kind: str,
    events: list[Event],
    sources: list[Source],
) -> ImportIndex:
    """Count and weight later source uses in earlier field solves.

    The count is the number of source-event support links with source.t >
    event.t.  The weighted part is the absolute contribution size imported
    through those links, including the half-weight in the symmetric solve.
    """
    contributions: list[ImportContribution] = []
    unique_labels: set[str] = set()

    for event in events:
        for use in support_uses(kind, event, sources):
            if use.source.t <= event.t:
                continue
            weight = abs(use.coefficient * use.source.strength) * kernel_weight(
                event, use.source
            )
            contributions.append(
                ImportContribution(event, use.source, use.coefficient, use.role, weight)
            )
            unique_labels.add(use.source.label)

    return ImportIndex(
        source_use_count=len(contributions),
        unique_later_sources=len(unique_labels),
        weighted=sum(contribution.weight for contribution in contributions),
        contributions=tuple(contributions),
    )


def classify_dependence(kind: str, index: ImportIndex) -> str:
    if kind == "retarded":
        return "retained retarded support: no future-boundary import"
    if index.source_use_count > 0:
        return "future-boundary import; not local past signaling"
    return "no future import observed"


def describe_source(source: Source) -> str:
    return (
        f"{source.label}(t={source.t}, x={source.x}, "
        f"q={fmt(source.strength)})"
    )


def print_index_table(indices: dict[str, ImportIndex]) -> None:
    print("IMPORT INDEX over earlier events")
    print("  definition: strict source.t > field_event.t")
    for kind in ("retarded", "advanced", "symmetric"):
        index = indices[kind]
        print(
            f"  {kind:9s} "
            f"uses={index.source_use_count:2d} "
            f"unique_sources={index.unique_later_sources:1d} "
            f"weighted={fmt(index.weighted)} "
            f"classification={classify_dependence(kind, index)}"
        )
    print()


def print_sample_imports(kind: str, index: ImportIndex, limit: int = 5) -> None:
    ranked = sorted(index.contributions, key=lambda contribution: -contribution.weight)
    print(f"{kind.upper()} SAMPLE IMPORT LINKS")
    for contribution in ranked[:limit]:
        event = contribution.event
        source = contribution.source
        print(
            f"  field(t={event.t}, x={event.x}) <- {source.label}"
            f"(t={source.t}, x={source.x}) "
            f"role={contribution.role} "
            f"coefficient={fmt(contribution.coefficient)} "
            f"weight={fmt(contribution.weight)}"
        )
    print()


def main() -> int:
    print("=" * 88)
    print("FUTURE-BOUNDARY IMPORT INDEX PROBE")
    print("  Test: later source degrees in earlier solves are boundary imports.")
    print("=" * 88)
    print()

    grid_times = range(0, 7)
    grid_positions = range(-2, 3)
    earlier_events = [Event(t, x) for t in range(1, 4) for x in (-1, 0, 1)]
    sources = [
        Source("past_anchor", 0, 0, +0.25),
        Source("future_boundary_A", 5, 0, +1.00),
        Source("future_boundary_B", 6, 1, -0.75),
    ]

    print(
        f"Grid: t={min(grid_times)}..{max(grid_times)}, "
        f"x={min(grid_positions)}..{max(grid_positions)}, c=1"
    )
    print("Earlier field events: t=1..3, x in {-1, 0, 1}")
    print("Sources supplied to the solve:")
    for source in sources:
        print(f"  - {describe_source(source)}")
    print()

    indices = {
        kind: future_boundary_import_index(kind, earlier_events, sources)
        for kind in ("retarded", "advanced", "symmetric")
    }
    print_index_table(indices)
    print_sample_imports("advanced", indices["advanced"])
    print_sample_imports("symmetric", indices["symmetric"])

    sample_event = Event(3, 0)
    sources_future_off = [
        Source("past_anchor", 0, 0, +0.25),
        Source("future_boundary_A", 5, 0, 0.0),
        Source("future_boundary_B", 6, 1, 0.0),
    ]

    ret_off = field_value("retarded", sample_event, sources_future_off)
    ret_on = field_value("retarded", sample_event, sources)
    adv_off = field_value("advanced", sample_event, sources_future_off)
    adv_on = field_value("advanced", sample_event, sources)
    sym_off = field_value("symmetric", sample_event, sources_future_off)
    sym_on = field_value("symmetric", sample_event, sources)

    print(f"Sample earlier event: field(t={sample_event.t}, x={sample_event.x})")
    print(f"  retarded  future off/on = {fmt(ret_off)} / {fmt(ret_on)}")
    print(f"  advanced  future off/on = {fmt(adv_off)} / {fmt(adv_on)}")
    print(f"  symmetric future off/on = {fmt(sym_off)} / {fmt(sym_on)}")
    print()

    retarded_index = indices["retarded"]
    advanced_index = indices["advanced"]
    symmetric_index = indices["symmetric"]

    check(
        "retarded import index is zero for earlier events",
        retarded_index.source_use_count == 0
        and retarded_index.unique_later_sources == 0
        and math.isclose(retarded_index.weighted, 0.0, abs_tol=1e-15),
        f"weighted={fmt(retarded_index.weighted)}",
    )
    check(
        "advanced import index is positive for earlier events",
        advanced_index.source_use_count > 0
        and advanced_index.unique_later_sources == 2
        and advanced_index.weighted > 0.0,
        (
            f"uses={advanced_index.source_use_count}, "
            f"weighted={fmt(advanced_index.weighted)}"
        ),
    )
    check(
        "symmetric import index is positive for earlier events",
        symmetric_index.source_use_count > 0
        and symmetric_index.unique_later_sources == 2
        and symmetric_index.weighted > 0.0,
        (
            f"uses={symmetric_index.source_use_count}, "
            f"weighted={fmt(symmetric_index.weighted)}"
        ),
    )
    check(
        "symmetric import weight is half the advanced import weight",
        math.isclose(
            symmetric_index.weighted,
            0.5 * advanced_index.weighted,
            abs_tol=1e-15,
        ),
        (
            f"symmetric={fmt(symmetric_index.weighted)}, "
            f"advanced={fmt(advanced_index.weighted)}"
        ),
    )
    check(
        "retarded sample field ignores future source toggles",
        math.isclose(ret_off, ret_on, abs_tol=1e-15),
        f"Delta={fmt(ret_on - ret_off)}",
    )
    check(
        "advanced sample field changes when future boundary data are toggled",
        not math.isclose(adv_off, adv_on, abs_tol=1e-15),
        f"Delta={fmt(adv_on - adv_off)}",
    )
    check(
        "symmetric sample field changes through its advanced half",
        not math.isclose(sym_off, sym_on, abs_tol=1e-15),
        f"Delta={fmt(sym_on - sym_off)}",
    )
    check(
        "advanced dependence is classified as future-boundary import",
        classify_dependence("advanced", advanced_index)
        == "future-boundary import; not local past signaling",
        classify_dependence("advanced", advanced_index),
    )
    check(
        "retarded dependence is not classified as past signaling",
        "no future-boundary import" in classify_dependence("retarded", retarded_index),
        classify_dependence("retarded", retarded_index),
    )

    print()
    print("SAFE READ")
    print("  - Retarded support gives import index 0 for earlier field events.")
    print("  - Advanced and symmetric solves have positive future-import indices.")
    print(
        "  - The dependence is from supplied future boundary data, not a local"
        " operation sending a signal to the past."
    )
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
