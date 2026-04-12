#!/usr/bin/env python3
"""Search the graph-first left-handed module for a natural chiral completion.

We take the current retained graph-first gauge surface at face value:

    V_L = (2,3)_{+1/3} ⊕ (2,1)_{-1}

This script asks a focused question:

    Can the missing right-handed singlets needed for anomaly-complete
    hypercharge arise *internally* from low tensor powers of V_L, or does the
    current surface force us to add a genuinely new completion sector?

The search is intentionally permissive:
- tensor products only
- no locality constraint
- no Fermi-statistics constraint

So if a target state is absent here, that is a strong obstruction.
If it is present here, that is only a candidate, not closure.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction


PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


def qstr(q: Fraction) -> str:
    if q.denominator == 1:
        return f"{q.numerator:+d}"
    return f"{q.numerator:+d}/{q.denominator}"


def su2_times_doublet(j2: int) -> Counter[int]:
    """Combine SU(2) spin j with a doublet (j=1/2), using 2j labels."""
    out: Counter[int] = Counter()
    if j2 == 0:
        out[1] += 1
        return out
    out[j2 - 1] += 1
    out[j2 + 1] += 1
    return out


def su3_times(rep: str, factor: str) -> Counter[str]:
    """Multiply an SU(3) irrep by either the singlet 1 or fundamental 3.

    We only need a small closed surface up to four factors of the fundamental.
    """
    if factor == "1":
        return Counter({rep: 1})

    table = {
        "1": Counter({"3": 1}),
        "3": Counter({"6": 1, "3bar": 1}),
        "3bar": Counter({"1": 1, "8": 1}),
        "6": Counter({"10": 1, "8": 1}),
        "8": Counter({"3": 1, "6bar": 1, "15": 1}),
        "10": Counter({"15": 1, "15p": 1}),
        "6bar": Counter({"3bar": 1, "15bar": 1}),
    }
    if rep not in table:
        raise KeyError(f"Missing SU(3) product rule for {rep} x 3")
    return table[rep]


# Current retained left-handed module
A = {"name": "Q_L-like", "j2": 1, "rep": "3", "Y": Fraction(1, 3)}
B = {"name": "L_L-like", "j2": 1, "rep": "1", "Y": Fraction(-1, 1)}
FACTORS = [A, B]


def build_tensor_powers(max_degree: int = 4) -> dict[int, Counter[tuple[int, str, Fraction]]]:
    states: dict[int, Counter[tuple[int, str, Fraction]]] = {0: Counter({(0, "1", Fraction(0, 1)): 1})}
    for n in range(1, max_degree + 1):
        current: Counter[tuple[int, str, Fraction]] = Counter()
        for (j2, rep, charge), mult in states[n - 1].items():
            for factor in FACTORS:
                for j2_new, m_su2 in su2_times_doublet(j2).items():
                    for rep_new, m_su3 in su3_times(rep, factor["rep"]).items():
                        key = (j2_new, rep_new, charge + factor["Y"])
                        current[key] += mult * m_su2 * m_su3
        states[n] = current
    return states


def singlet_sector(states_n: Counter[tuple[int, str, Fraction]]) -> Counter[tuple[str, Fraction]]:
    out: Counter[tuple[str, Fraction]] = Counter()
    for (j2, rep, charge), mult in states_n.items():
        if j2 == 0:
            out[(rep, charge)] += mult
    return out


def summarize_sector(sector: Counter[tuple[str, Fraction]]) -> list[str]:
    lines = []
    for (rep, charge), mult in sorted(sector.items(), key=lambda item: (float(item[0][1]), item[0][0])):
        lines.append(f"    ({rep})_{{{qstr(charge)}}}  multiplicity {mult}")
    return lines


def find_min_degree(states: dict[int, Counter[tuple[int, str, Fraction]]], target_j2: int, target_rep: str, target_q: Fraction, max_degree: int = 4) -> int | None:
    for n in range(1, max_degree + 1):
        if states[n][(target_j2, target_rep, target_q)] > 0:
            return n
    return None


def main() -> int:
    print("=" * 78)
    print("GRAPH-FIRST CHIRAL COMPLETION SEARCH")
    print("=" * 78)
    print("Retained input module: V_L = (2,3)_{+1/3} ⊕ (2,1)_{-1}")
    print("Question: can missing right-handed singlets arise internally from low")
    print("tensor powers of V_L, or is a genuinely new completion sector required?")

    states = build_tensor_powers(max_degree=4)

    print("\nWEAK-SINGLET CONTENT BY DEGREE")
    print("-" * 78)
    for n in range(1, 5):
        sector = singlet_sector(states[n])
        print(f"Degree n = {n}:")
        if sector:
            for line in summarize_sector(sector):
                print(line)
        else:
            print("    <none>")

    # Core obstruction: no one-particle weak singlets exist.
    check("No weak singlets on the one-particle 8-state surface", len(singlet_sector(states[1])) == 0)

    # Minimal target search on the right-handed (not charge-conjugated) convention.
    targets = [
        ("d_R-like weak singlet", "3", Fraction(-2, 3)),
        ("e_R-like weak singlet", "1", Fraction(-2, 1)),
        ("u_R-like weak singlet", "3", Fraction(4, 3)),
    ]

    print("\nMINIMAL DEGREE FOR RIGHT-HANDED-LIKE TARGETS")
    print("-" * 78)
    degrees: dict[str, int | None] = {}
    for name, rep, charge in targets:
        degree = find_min_degree(states, 0, rep, charge)
        degrees[name] = degree
        if degree is None:
            print(f"  {name}: absent up to degree 4")
        else:
            print(f"  {name}: first appears at degree {degree}")

    check("d_R-like state appears by degree 2", degrees["d_R-like weak singlet"] == 2)
    check("e_R-like state appears by degree 2", degrees["e_R-like weak singlet"] == 2)
    check("u_R-like state does not appear before degree 4", degrees["u_R-like weak singlet"] == 4)

    print("\nINTERPRETATION")
    print("-" * 78)
    print("  1. The current one-particle graph-first surface is left-handed only.")
    print("     There are no weak singlets at degree 1.")
    print("  2. A permissive composite search already finds d_R-like and e_R-like")
    print("     quantum numbers at degree 2.")
    print("  3. The u_R-like weak singlet is much harder: it does not appear until")
    print("     degree 4 in this permissive search.")
    print("  4. Because this search ignores locality and Fermi statistics, any")
    print("     positive result here is only a candidate. The absence results are")
    print("     the more important ones.")
    print("  5. Conclusion: anomaly-complete hypercharge does not arise naturally")
    print("     on the present 8-state one-particle surface. A clean chiral")
    print("     completion likely requires either:")
    print("       - a genuinely new completion sector, or")
    print("       - a higher/composite graph-canonical construction whose physical")
    print("         interpretation is still to be derived.")

    if FAIL:
        print(f"\nPASS={PASS} FAIL={FAIL}")
        return 1

    print(f"\nPASS={PASS} FAIL=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
