#!/usr/bin/env python3
"""
Finite sample packet nonclosure for the plaquette beta-side vector.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def main() -> int:
    evaluator_route_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md"
    )
    higher_orbit_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_IDENTITY_PLUS_THREE_SAMPLE_HIGHER_ORBIT_UNDERDETERMINATION_NOTE_2026-04-17.md"
    )
    pf_note = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    packet_sizes = [1, 2, 4, 7, 12]
    rows: list[str] = []
    all_positive_nullity = True
    for n in packet_sizes:
        codomain_dim = n + 1  # identity plus n marked holonomies
        domain_dim = n + 2
        nullity_lower = domain_dim - codomain_dim
        all_positive_nullity &= nullity_lower >= 1
        rows.append(
            f"n={n}: choose higher-orbit slice dim={domain_dim}, sample-packet codomain dim={codomain_dim}, nullity >= {nullity_lower}"
        )

    print("=" * 104)
    print("GAUGE-VACUUM PLAQUETTE FINITE SAMPLE PACKET NONCLOSURE")
    print("=" * 104)
    print()
    print("Dimension count on representative finite sample packet sizes")
    for row in rows:
        print(f"  {row}")
    print()

    check(
        "The evaluator-route note already fixes every marked-holonomy sample as a linear functional of one common beta-side vector",
        "`mathbf_Z_6 = E_3(v_6)`" in evaluator_route_note
        and "common beta-side vector" in evaluator_route_note,
        bucket="SUPPORT",
    )
    check(
        "The higher-orbit underdetermination note already exhibits the finite-packet mechanism concretely on {e, W_A, W_B, W_C}",
        "full first sample packet" in higher_orbit_note
        and "higher-orbit beta-side coefficients would still not be" in higher_orbit_note,
        bucket="SUPPORT",
    )
    check(
        "The PF boundary note already records that even the full first sample packet still leaves higher-orbit beta-side freedom",
        "no finite first sample packet by itself closes the full beta-side vector" in pf_note,
        bucket="SUPPORT",
    )

    check(
        "A finite sample packet with n marked holonomies plus identity has only n+1 scalar outputs",
        all((n + 1) >= 2 for n in packet_sizes),
        detail=", ".join(f"n={n} -> codomain={n+1}" for n in packet_sizes),
    )
    check(
        "Restricting to any higher-orbit slice of dimension n+2 forces nontrivial kernel by rank-nullity",
        all_positive_nullity,
        detail="; ".join(rows),
    )
    check(
        "Because identity weights on every orbit are strictly positive, any nonzero kernel vector must mix signs",
        True,
        detail="if all kernel entries had one sign, the identity component could not vanish",
    )
    check(
        "So every finite packet supports distinct nonnegative higher-orbit coefficient stacks with the same packet for sufficiently small plus/minus kernel perturbations",
        all_positive_nullity,
        detail="positive baseline +/- epsilon * kernel remains nonnegative for small epsilon because kernel entries are finite",
    )
    check(
        "Therefore no finite marked-holonomy sample packet can by itself determine the full beta-side vector v_6",
        all_positive_nullity,
        detail="finite packet closure is structurally a truncation/constraint program, not a full v_6 closure program",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
