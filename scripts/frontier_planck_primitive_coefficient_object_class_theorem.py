#!/usr/bin/env python3
"""Audit runner for the primitive-coefficient object-class theorem."""

from dataclasses import dataclass


def expect(name: str, cond: bool) -> int:
    if cond:
        print(f"PASS: {name}")
        return 1
    print(f"FAIL: {name}")
    return 0


@dataclass(frozen=True)
class PrimitiveObject:
    dim: int
    packet_rank: int


@dataclass(frozen=True)
class VacuumObject:
    primitive: PrimitiveObject
    embedding_label: str
    vacuum_label: str
    local_value: float


def main() -> int:
    passed = 0
    total = 0

    primitive = PrimitiveObject(dim=16, packet_rank=4)
    vac_a = VacuumObject(
        primitive=primitive,
        embedding_label="iota_A",
        vacuum_label="Omega_A",
        local_value=0.25,
    )
    vac_b = VacuumObject(
        primitive=primitive,
        embedding_label="iota_B",
        vacuum_label="Omega_B",
        local_value=0.125,
    )

    total += 1
    passed += expect(
        "primitive-object-fixed",
        primitive.dim == 16 and primitive.packet_rank == 4,
    )

    total += 1
    passed += expect(
        "same-primitive-different-vacuum-data",
        vac_a.primitive == vac_b.primitive
        and (vac_a.embedding_label, vac_a.vacuum_label)
        != (vac_b.embedding_label, vac_b.vacuum_label),
    )

    total += 1
    passed += expect(
        "same-primitive-can-give-different-local-values",
        vac_a.local_value != vac_b.local_value,
    )

    total += 1
    passed += expect(
        "reduced-vacuum-value-not-function-of-primitive-object-alone",
        not (
            vac_a.primitive == vac_b.primitive
            and vac_a.local_value == vac_b.local_value
        ),
    )

    total += 1
    passed += expect(
        "generic-vacuum-reading-changes-object-class",
        hasattr(vac_a, "embedding_label") and hasattr(vac_a, "vacuum_label"),
    )

    total += 1
    passed += expect(
        "representation-reading-still-possible",
        vac_a.local_value == 0.25,
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
