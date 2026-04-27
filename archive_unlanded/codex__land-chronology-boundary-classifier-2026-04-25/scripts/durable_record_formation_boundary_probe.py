#!/usr/bin/env python3
"""Chronology lane probe: finite durable-record formation boundary.

This is a sufficient record-carrier model, not a measurement derivation.  A
system bit writes a visible record and then fans out to k environment carriers.
Redundant carriers make the record robust to bounded damage, and any carrier
left unerased remains a witness.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


PASS = 0
FAIL = 0


@dataclass(frozen=True)
class RecordState:
    system: int
    record: int
    environment: tuple[int, ...]


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


def cnot_system_to_record(state: RecordState) -> RecordState:
    if state.system == 0:
        return state
    return RecordState(state.system, state.record ^ 1, state.environment)


def cnot_record_to_env(state: RecordState, index: int) -> RecordState:
    if state.record == 0:
        return state
    env = list(state.environment)
    env[index] ^= 1
    return RecordState(state.system, state.record, tuple(env))


def form_record(system_bit: int, k: int) -> RecordState:
    state = RecordState(system=system_bit, record=0, environment=(0,) * k)
    state = cnot_system_to_record(state)
    for index in range(k):
        state = cnot_record_to_env(state, index)
    return state


def later_system_flip(state: RecordState) -> RecordState:
    return RecordState(1 - state.system, state.record, state.environment)


def flip_env_subset(state: RecordState, subset: tuple[int, ...]) -> RecordState:
    env = list(state.environment)
    for index in subset:
        env[index] ^= 1
    return RecordState(state.system, state.record, tuple(env))


def erase_carriers(state: RecordState, erase_record: bool, env_subset: tuple[int, ...]) -> RecordState:
    env = list(state.environment)
    for index in env_subset:
        env[index] = 0
    return RecordState(
        state.system,
        0 if erase_record else state.record,
        tuple(env),
    )


def witness_count(state: RecordState) -> int:
    return int(state.record == 1) + sum(1 for bit in state.environment if bit == 1)


def majority_decode(environment: tuple[int, ...]) -> int:
    ones = sum(environment)
    zeros = len(environment) - ones
    if ones == zeros:
        raise ValueError("tie has no majority")
    return 1 if ones > zeros else 0


def all_subsets(k: int, size: int) -> list[tuple[int, ...]]:
    return [tuple(subset) for subset in combinations(range(k), size)]


def fmt_state(state: RecordState) -> str:
    env = ",".join(str(bit) for bit in state.environment) or "-"
    return f"S={state.system}, R={state.record}, E=[{env}]"


def main() -> int:
    print("=" * 88)
    print("DURABLE RECORD FORMATION BOUNDARY PROBE")
    print("  Test: redundant physical carriers make partial past-edit claims fail.")
    print("=" * 88)
    print()

    k = 5
    formed_zero = form_record(0, k)
    formed_one = form_record(1, k)
    after_late_flip = later_system_flip(formed_one)

    print("Record formation examples:")
    print(f"  S=0 -> {fmt_state(formed_zero)}")
    print(f"  S=1 -> {fmt_state(formed_one)}")
    print(f"  after later system flip -> {fmt_state(after_late_flip)}")
    print()

    check("zero system writes no positive carriers", witness_count(formed_zero) == 0)
    check(
        "one system writes visible record plus all environment carriers",
        formed_one.record == 1 and formed_one.environment == (1,) * k,
        fmt_state(formed_one),
    )
    check(
        "later system flip does not change record carriers",
        after_late_flip.record == formed_one.record
        and after_late_flip.environment == formed_one.environment,
        fmt_state(after_late_flip),
    )

    for flips in range(0, 3):
        decoded_ok = all(
            majority_decode(flip_env_subset(formed_one, subset).environment) == 1
            for subset in all_subsets(k, flips)
        )
        check(
            f"majority readout survives all {flips}-flip damage patterns",
            decoded_ok,
            f"patterns={len(all_subsets(k, flips))}",
        )

    three_flip_failures = [
        subset
        for subset in all_subsets(k, 3)
        if majority_decode(flip_env_subset(formed_one, subset).environment) == 0
    ]
    check(
        "durability threshold is explicit: some 3-flip patterns fail",
        len(three_flip_failures) > 0,
        f"failing patterns={len(three_flip_failures)}",
    )

    all_env = tuple(range(k))
    partial_erase = erase_carriers(formed_one, erase_record=True, env_subset=(0, 2))
    full_erase = erase_carriers(formed_one, erase_record=True, env_subset=all_env)

    check(
        "partial erasure leaves environment witnesses",
        witness_count(partial_erase) > 0,
        fmt_state(partial_erase),
    )
    check(
        "full carrier erasure is the only zero-witness erasure in this model",
        witness_count(full_erase) == 0,
        fmt_state(full_erase),
    )

    proper_subset_witnesses = []
    labels = ["record"] + [f"env_{index}" for index in range(k)]
    for mask in range(1 << len(labels)):
        erased_record = bool(mask & 1)
        erased_env = tuple(index for index in range(k) if mask & (1 << (index + 1)))
        erased = erase_carriers(formed_one, erased_record, erased_env)
        if mask != (1 << len(labels)) - 1:
            proper_subset_witnesses.append(witness_count(erased) > 0)
    check(
        "every proper carrier-erasure subset leaves a witness",
        all(proper_subset_witnesses),
        f"proper subsets={len(proper_subset_witnesses)}",
    )

    print()
    print("SAFE READ")
    print("  - This is a sufficient redundant-carrier model, not measurement closure.")
    print("  - Once carriers exist, later system operations do not erase them.")
    print("  - Zero witnesses require erasing all carriers, not sending a signal to t0.")
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
