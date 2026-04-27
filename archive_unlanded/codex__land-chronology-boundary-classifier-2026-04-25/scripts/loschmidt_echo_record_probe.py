#!/usr/bin/env python3
"""Chronology lane probe: Loschmidt echo versus durable records.

This is a reversible bit-level toy model. A system bit writes a durable record
bit, and the record copies into an environment bit. Later inverse evolution can
remove the visible record only if the environment is reversed too.

The probe separates three claims:

1. a late operation does not alter the already-written earlier record;
2. retrodiction from a complete final state reconstructs the earlier state;
3. a Loschmidt echo erases records only when it reverses the whole closed
   record/environment/apparatus state.
"""

from __future__ import annotations

from dataclasses import dataclass


PASS = 0
FAIL = 0


@dataclass(frozen=True)
class State:
    system: int
    record: int
    environment: int
    apparatus: int


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


def flip_bit(state: State, bit: str) -> State:
    data = state.__dict__.copy()
    data[bit] ^= 1
    return State(**data)


def cnot(state: State, control: str, target: str) -> State:
    data = state.__dict__.copy()
    if data[control]:
        data[target] ^= 1
    return State(**data)


def write_record(state: State) -> State:
    return cnot(state, "system", "record")


def copy_record_to_environment(state: State) -> State:
    return cnot(state, "record", "environment")


def late_local_operation(state: State) -> State:
    state = flip_bit(state, "system")
    return flip_bit(state, "apparatus")


def forward_history() -> dict[str, State]:
    history: dict[str, State] = {}
    history["pre_record"] = State(system=1, record=0, environment=0, apparatus=0)
    history["t0_record_written"] = write_record(history["pre_record"])
    history["t0_environment_copy"] = copy_record_to_environment(history["t0_record_written"])
    history["t1_after_late_operation"] = late_local_operation(history["t0_environment_copy"])
    return history


def full_inverse_echo(final_state: State) -> State:
    state = late_local_operation(final_state)
    state = copy_record_to_environment(state)
    return write_record(state)


def partial_inverse_visible_record_only(final_state: State) -> State:
    state = late_local_operation(final_state)
    return write_record(state)


def partial_inverse_system_only(final_state: State) -> State:
    return late_local_operation(final_state)


def fmt(state: State) -> str:
    return (
        f"S={state.system}, R={state.record}, "
        f"E={state.environment}, A={state.apparatus}"
    )


def main() -> int:
    print("=" * 88)
    print("LOSCHMIDT ECHO RECORD PROBE")
    print("  Test: reversible reconstruction is not selective past-record editing.")
    print("=" * 88)
    print()

    history = forward_history()
    pre = history["pre_record"]
    written = history["t0_record_written"]
    copied = history["t0_environment_copy"]
    final = history["t1_after_late_operation"]

    print("Forward states:")
    for label, state in history.items():
        print(f"  {label:26s} {fmt(state)}")
    print()

    check(
        "record is written at t0",
        written.record == written.system == 1,
        fmt(written),
    )
    check(
        "durable environment copy exists before late operation",
        copied.record == 1 and copied.environment == 1,
        fmt(copied),
    )
    check(
        "late local operation leaves record/environment copies intact",
        final.record == copied.record and final.environment == copied.environment,
        fmt(final),
    )

    reconstructed_copied = late_local_operation(final)
    check(
        "retrodiction reconstructs the pre-operation copied state",
        reconstructed_copied == copied,
        fmt(reconstructed_copied),
    )

    sys_only = partial_inverse_system_only(final)
    visible_only = partial_inverse_visible_record_only(final)
    full_echo = full_inverse_echo(final)

    check(
        "system-only reversal does not erase durable records",
        sys_only.record == 1 and sys_only.environment == 1,
        fmt(sys_only),
    )
    check(
        "visible-record reversal leaves an environment witness",
        visible_only.record == 0 and visible_only.environment == 1,
        fmt(visible_only),
    )
    check(
        "full echo returns to pre-record state only by reversing environment too",
        full_echo == pre,
        fmt(full_echo),
    )
    check(
        "full echo is global reversal, not a late operation preserving the later lab",
        full_echo.environment == 0 and full_echo.apparatus == 0,
        "environment/apparatus memories are also undone",
    )

    print()
    print("SAFE READ")
    print("  - The inverse map reconstructs earlier closed states when all degrees are included.")
    print("  - Partial inverse evolution does not change the earlier durable record.")
    print(
        "  - Erasing the record requires erasing the environment/apparatus state too,"
        " so it is not an operational message to t0."
    )
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
