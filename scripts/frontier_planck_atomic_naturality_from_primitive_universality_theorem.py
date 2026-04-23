#!/usr/bin/env python3
"""Audit runner for atomic naturality from primitive universality."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_ATOMIC_NATURALITY_FROM_PRIMITIVE_UNIVERSALITY_THEOREM_2026-04-23.md"


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def hamming_weight(idx: int) -> int:
    return sum((idx >> bit) & 1 for bit in range(4))


def packet_atoms() -> set[int]:
    return {idx for idx in range(16) if hamming_weight(idx) == 1}


def transposition(i: int, j: int, dim: int = 16) -> tuple[int, ...]:
    perm = list(range(dim))
    perm[i], perm[j] = perm[j], perm[i]
    return tuple(perm)


def bit_swap(bit_a: int, bit_b: int) -> tuple[int, ...]:
    perm: list[int] = []
    for idx in range(16):
        bit_a_value = (idx >> bit_a) & 1
        bit_b_value = (idx >> bit_b) & 1
        out = idx
        if bit_a_value != bit_b_value:
            out ^= (1 << bit_a) | (1 << bit_b)
        perm.append(out)
    return tuple(perm)


def orbit_partition(generators: list[tuple[int, ...]], dim: int = 16) -> list[set[int]]:
    unseen = set(range(dim))
    orbits: list[set[int]] = []

    while unseen:
        start = min(unseen)
        orbit = {start}
        queue: deque[int] = deque([start])
        unseen.remove(start)

        while queue:
            current = queue.popleft()
            for generator in generators:
                nxt = generator[current]
                if nxt not in orbit:
                    orbit.add(nxt)
                    queue.append(nxt)
                    unseen.discard(nxt)

        orbits.append(orbit)

    return sorted(orbits, key=lambda orbit: (len(orbit), min(orbit)))


def orbit_sizes(orbits: list[set[int]]) -> list[int]:
    return sorted(len(orbit) for orbit in orbits)


def adjacent_transpositions(atoms: list[int]) -> list[tuple[int, ...]]:
    return [transposition(a, b) for a, b in zip(atoms, atoms[1:])]


def packet_stabilizer_generators() -> list[tuple[int, ...]]:
    packet = sorted(packet_atoms())
    complement = sorted(set(range(16)) - set(packet))
    return adjacent_transpositions(packet) + adjacent_transpositions(complement)


def hamming_stabilizer_generators() -> list[tuple[int, ...]]:
    generators: list[tuple[int, ...]] = []
    for weight in range(5):
        atoms = [idx for idx in range(16) if hamming_weight(idx) == weight]
        generators.extend(adjacent_transpositions(atoms))
    return generators


def residual_s3_generators() -> list[tuple[int, ...]]:
    # Bit 0 is held fixed as the temporal bit; bits 1, 2, 3 are spatial.
    return [bit_swap(1, 2), bit_swap(2, 3)]


def expect(name: str, cond: bool, detail: str = "") -> Check:
    status = "PASS" if cond else "FAIL"
    print(f"{status}: {name}: {detail}")
    return Check(name=name, passed=cond, detail=detail)


def main() -> int:
    note = NOTE.read_text()
    checks: list[Check] = []

    full_generators = adjacent_transpositions(list(range(16)))
    full_orbits = orbit_partition(full_generators)
    packet_orbits = orbit_partition(packet_stabilizer_generators())
    hamming_orbits = orbit_partition(hamming_stabilizer_generators())
    s3_orbits = orbit_partition(residual_s3_generators())

    checks.append(
        expect(
            "bare-frame-relabelings-are-transitive",
            len(full_orbits) == 1 and orbit_sizes(full_orbits) == [16],
            f"orbits={orbit_sizes(full_orbits)}",
        )
    )

    atom_weight = Fraction(1, 16)
    packet_value = len(packet_atoms()) * atom_weight
    checks.append(
        expect(
            "additivity-normalization-after-full-naturality-give-quarter",
            packet_value == Fraction(1, 4),
            f"rank={len(packet_atoms())}, atom={atom_weight}, packet={packet_value}",
        )
    )

    alpha = Fraction(1, 32)
    beta = Fraction(7, 96)
    packet_stabilizer_total = 4 * alpha + 12 * beta
    packet_stabilizer_value = 4 * alpha
    checks.append(
        expect(
            "packet-preserving-naturality-does-not-fix-quarter",
            orbit_sizes(packet_orbits) == [4, 12]
            and packet_stabilizer_total == 1
            and packet_stabilizer_value == Fraction(1, 8),
            (
                f"orbits={orbit_sizes(packet_orbits)}, "
                f"alpha={alpha}, beta={beta}, C(P_A)={packet_stabilizer_value}"
            ),
        )
    )

    checks.append(
        expect(
            "event-count-preserving-naturality-has-five-orbits",
            orbit_sizes(hamming_orbits) == [1, 1, 4, 4, 6],
            f"orbits={orbit_sizes(hamming_orbits)}",
        )
    )

    checks.append(
        expect(
            "retained-spatial-s3-naturality-has-eight-orbits",
            orbit_sizes(s3_orbits) == [1, 1, 1, 1, 3, 3, 3, 3],
            f"orbits={orbit_sizes(s3_orbits)}",
        )
    )

    required_phrases = [
        "Atomic naturality is a theorem if",
        "does **not** assume `rho = I_16/16`",
        "What is proved",
        "What remains a principle",
        "packet-preserving naturality alone does not prove quarter",
        "readout-enriched coefficient object",
        "PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md",
    ]
    checks.append(
        expect(
            "note-records-hostile-review-scope",
            all(phrase in note for phrase in required_phrases),
            "note distinguishes theorem, non-smuggling, countermodels, and remaining principle",
        )
    )

    passed = sum(check.passed for check in checks)
    failed = len(checks) - passed
    print(f"SUMMARY: PASS={passed} FAIL={failed}")
    if failed == 0:
        print("Atomic naturality theorem audit: VERIFIED WITH SCOPED COUNTERMODELS")
    else:
        print("Atomic naturality theorem audit: FAILED")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
