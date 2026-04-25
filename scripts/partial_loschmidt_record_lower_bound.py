#!/usr/bin/env python3
"""Chronology lane probe: partial Loschmidt record lower bound.

This is a pure-Python reversible bit-copy model for the record boundary.
A system bit writes a visible record bit, and that visible record fans out into
``k`` environment copies. A partial Loschmidt reversal can undo only the copy
carriers inside the reversed subsystem. Every durable copy left outside that
subsystem remains as a witness.

The probe formalizes the lower bound:

    remaining witness bits >= number of unreversed durable copy carriers.

In this exact copy model the inequality is saturated. The only zero-witness
case reverses every durable copy carrier; that case is classified as a global
closed-state reversal, not as operational past signaling.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


PASS = 0
FAIL = 0
RECORD = "record"


@dataclass(frozen=True)
class State:
    system: int
    record: int
    environment: tuple[int, ...]
    apparatus: int


@dataclass(frozen=True)
class ProbeResult:
    k: int
    reversed_copies: frozenset[str]
    state: State
    witnesses: tuple[str, ...]
    lower_bound: int
    classification: str


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


def copy_labels(k: int) -> tuple[str, ...]:
    return (RECORD,) + tuple(f"env_{index}" for index in range(k))


def powerset(labels: tuple[str, ...]) -> tuple[frozenset[str], ...]:
    subsets: list[frozenset[str]] = []
    for size in range(len(labels) + 1):
        for subset in combinations(labels, size):
            subsets.append(frozenset(subset))
    return tuple(subsets)


def cnot_system_to_record(state: State) -> State:
    if state.system == 0:
        return state
    return State(
        system=state.system,
        record=state.record ^ 1,
        environment=state.environment,
        apparatus=state.apparatus,
    )


def cnot_record_to_environment(state: State, index: int) -> State:
    if state.record == 0:
        return state
    environment = list(state.environment)
    environment[index] ^= 1
    return State(
        system=state.system,
        record=state.record,
        environment=tuple(environment),
        apparatus=state.apparatus,
    )


def late_apparatus_mark(state: State) -> State:
    return State(
        system=state.system,
        record=state.record,
        environment=state.environment,
        apparatus=state.apparatus ^ 1,
    )


def pre_record_state(k: int) -> State:
    return State(system=1, record=0, environment=(0,) * k, apparatus=0)


def forward_state(k: int) -> State:
    state = cnot_system_to_record(pre_record_state(k))
    for index in range(k):
        state = cnot_record_to_environment(state, index)
    return late_apparatus_mark(state)


def reverse_subset(final_state: State, reversed_copies: frozenset[str]) -> State:
    """Undo the late mark, then reverse selected copy gates.

    Environment-copy inverse gates are applied before the visible-record inverse
    gate because the record bit is their reversible copy control.
    """

    state = late_apparatus_mark(final_state)
    for index in range(len(state.environment)):
        if f"env_{index}" in reversed_copies:
            state = cnot_record_to_environment(state, index)
    if RECORD in reversed_copies:
        state = cnot_system_to_record(state)
    return state


def witness_labels(state: State) -> tuple[str, ...]:
    witnesses: list[str] = []
    if state.record:
        witnesses.append(RECORD)
    for index, value in enumerate(state.environment):
        if value:
            witnesses.append(f"env_{index}")
    return tuple(witnesses)


def classify(reversed_copies: frozenset[str], labels: tuple[str, ...]) -> str:
    if reversed_copies == frozenset(labels):
        return "global closed-state reversal; not operational past signaling"
    return "partial reversal; durable record boundary remains"


def run_case(k: int, reversed_copies: frozenset[str]) -> ProbeResult:
    labels = copy_labels(k)
    state = reverse_subset(forward_state(k), reversed_copies)
    witnesses = witness_labels(state)
    lower_bound = len(set(labels) - set(reversed_copies))
    return ProbeResult(
        k=k,
        reversed_copies=reversed_copies,
        state=state,
        witnesses=witnesses,
        lower_bound=lower_bound,
        classification=classify(reversed_copies, labels),
    )


def fmt_state(state: State) -> str:
    env = ",".join(str(bit) for bit in state.environment) or "-"
    return f"S={state.system}, R={state.record}, E=[{env}], A={state.apparatus}"


def fmt_subset(subset: frozenset[str]) -> str:
    if not subset:
        return "{}"
    return "{" + ", ".join(sorted(subset)) + "}"


def fmt_witnesses(witnesses: tuple[str, ...]) -> str:
    if not witnesses:
        return "{}"
    return "{" + ", ".join(witnesses) + "}"


def min_witnesses_by_reversed_count(k: int) -> dict[int, int]:
    mins: dict[int, int] = {}
    for subset in powerset(copy_labels(k)):
        result = run_case(k, subset)
        size = len(subset)
        mins[size] = min(mins.get(size, result.lower_bound), len(result.witnesses))
    return dict(sorted(mins.items()))


def exhaustive_results(max_k: int) -> tuple[ProbeResult, ...]:
    results: list[ProbeResult] = []
    for k in range(max_k + 1):
        for subset in powerset(copy_labels(k)):
            results.append(run_case(k, subset))
    return tuple(results)


def main() -> int:
    print("=" * 88)
    print("PARTIAL LOSCHMIDT RECORD LOWER BOUND")
    print("  Test: unreversed durable copies bound remaining record witnesses.")
    print("=" * 88)
    print()

    max_k = 6
    results = exhaustive_results(max_k)

    print("Forward copy sectors:")
    for k in range(max_k + 1):
        state = forward_state(k)
        expected = tuple(copy_labels(k))
        check(
            f"k={k}: forward state writes all durable copy carriers",
            witness_labels(state) == expected,
            fmt_state(state),
        )
    print()

    check(
        "all subsets saturate witness lower bound",
        all(len(result.witnesses) == result.lower_bound for result in results),
        f"cases={len(results)}",
    )
    check(
        "positive witness whenever any durable copy is outside reversal",
        all(
            len(result.witnesses) > 0
            for result in results
            if result.reversed_copies != frozenset(copy_labels(result.k))
        ),
        "partial reversals cannot erase all records",
    )
    check(
        "zero witness occurs only for full durable-copy reversal",
        all(
            (len(result.witnesses) == 0)
            == (result.reversed_copies == frozenset(copy_labels(result.k)))
            for result in results
        ),
        "full reversal is the only zero-witness case",
    )
    check(
        "environment outside reversed subsystem leaves a witness",
        all(
            len(result.witnesses) > 0
            for result in results
            if any(
                f"env_{index}" not in result.reversed_copies
                for index in range(result.k)
            )
        ),
        "at least one unreversed environment copy implies positive witness",
    )
    check(
        "full reversal returns each closed record sector to pre-record state",
        all(
            run_case(k, frozenset(copy_labels(k))).state == pre_record_state(k)
            for k in range(max_k + 1)
        ),
        "record/environment/apparatus memories are also undone",
    )
    print()

    print("Minimum witnesses by reversed-copy count:")
    for k in range(max_k + 1):
        mins = min_witnesses_by_reversed_count(k)
        total = k + 1
        expected = {count: total - count for count in range(total + 1)}
        check(
            f"k={k}: min witnesses equals unreversed copies",
            mins == expected,
            f"mins={mins}",
        )
    print()

    example_k = 4
    example_subsets = (
        frozenset(),
        frozenset({RECORD}),
        frozenset({"env_0", "env_2"}),
        frozenset({RECORD, "env_0", "env_1"}),
        frozenset(copy_labels(example_k)),
    )
    print(f"Boundary examples for k={example_k}:")
    print(f"  pre-record: {fmt_state(pre_record_state(example_k))}")
    print(f"  final:      {fmt_state(forward_state(example_k))}")
    for subset in example_subsets:
        result = run_case(example_k, subset)
        print(
            "  reverse="
            f"{fmt_subset(subset):34s} "
            f"witnesses={fmt_witnesses(result.witnesses):34s} "
            f"lower_bound={result.lower_bound} "
            f"classification={result.classification}"
        )
    print()

    print("SAFE READ")
    print("  - Partial reversal erases only the durable copies inside its subsystem.")
    print("  - Each unreversed environment copy remains a physical witness bit.")
    print(
        "  - The zero-witness case is full closed-state reversal, not an "
        "operational message to an earlier record."
    )
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
