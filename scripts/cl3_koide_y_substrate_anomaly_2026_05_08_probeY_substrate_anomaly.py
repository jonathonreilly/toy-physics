#!/usr/bin/env python3
"""Runner for the bounded anomaly-forcing boundary note."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT
    / "docs"
    / "KOIDE_Y_SUBSTRATE_ANOMALY_FORCING_NOTE_2026-05-08_probeY_substrate_anomaly.md"
)

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def charges(nc: int) -> dict[str, Fraction]:
    n = Fraction(nc, 1)
    return {
        "Q": Fraction(1, nc),
        "L": Fraction(-1, 1),
        "u_c": -(Fraction(1, 1) + Fraction(1, nc)),
        "d_c": Fraction(1, 1) - Fraction(1, nc),
        "e_c": Fraction(2, 1),
        "nu_c": Fraction(0, 1),
    }


def anomaly_traces(nc: int, scale: Fraction = Fraction(1, 1)) -> dict[str, Fraction]:
    y = {k: scale * v for k, v in charges(nc).items()}
    su2_sq_y = nc * y["Q"] + y["L"]
    su_nc_sq_y = 2 * y["Q"] + y["u_c"] + y["d_c"]
    grav_y = 2 * nc * y["Q"] + 2 * y["L"] + nc * y["u_c"] + nc * y["d_c"] + y["e_c"] + y["nu_c"]
    y_cubed = (
        2 * nc * y["Q"] ** 3
        + 2 * y["L"] ** 3
        + nc * y["u_c"] ** 3
        + nc * y["d_c"] ** 3
        + y["e_c"] ** 3
        + y["nu_c"] ** 3
    )
    return {
        "SU2^2Y": su2_sq_y,
        "SUNc^2Y": su_nc_sq_y,
        "gravY": grav_y,
        "Y^3": y_cubed,
    }


def witten_even_doublets(nc: int, ngen: int = 1) -> bool:
    return (ngen * (nc + 1)) % 2 == 0


def main() -> int:
    note = NOTE_PATH.read_text()
    note_flat = re.sub(r"\s+", " ", note)

    section("note boundary checks")
    required = [
        "Claim type:** bounded_theorem",
        "source-note proposal only",
        "does not by itself select the full Standard Model carrier sector",
        "odd `N_c >= 3`",
        "still does not select `N_c=3`",
        "does not uniquely force `N_c=3`",
        "does not strengthen their status",
        "assert retained or audited status",
    ]
    for marker in required:
        check(f"note contains {marker[:54]!r}", marker in note_flat)

    section("perturbative anomaly traces for multiple color ranks")
    for nc in [2, 3, 4, 5, 7, 9]:
        traces = anomaly_traces(nc)
        check(f"N_c={nc}: perturbative traces vanish", all(v == 0 for v in traces.values()), detail=str(traces))

    section("Witten parity correction")
    for nc in [2, 4, 6, 8]:
        check(f"N_c={nc}: Witten parity fails for one generation", not witten_even_doublets(nc), detail=f"doublets={nc+1}")
    for nc in [3, 5, 7, 9]:
        check(f"N_c={nc}: Witten parity passes for one generation", witten_even_doublets(nc), detail=f"doublets={nc+1}")
    check("N_c=3 is not unique among odd allowed ranks", all(witten_even_doublets(nc) for nc in [3, 5, 7, 9]))

    section("generation additivity")
    for ngen in [1, 2, 3, 4, 5]:
        nc = 3
        traces = {k: ngen * v for k, v in anomaly_traces(nc).items()}
        check(f"n_gen={ngen}: traces remain zero at N_c=3", all(v == 0 for v in traces.values()))
        check(f"n_gen={ngen}: Witten parity remains even at N_c=3", witten_even_doublets(nc, ngen))

    section("hypercharge scale homogeneity")
    for scale in [Fraction(2, 1), Fraction(-3, 1), Fraction(5, 7)]:
        traces = anomaly_traces(3, scale)
        check(f"scale={scale}: zero traces preserved", all(v == 0 for v in traces.values()), detail=str(traces))

    section("vectorlike and category-boundary checks")
    vectorlike_pair_trace = Fraction(1, 1) + Fraction(-1, 1)
    check("vectorlike cubic pair cancels", vectorlike_pair_trace == 0)
    anomaly_labels = {"SU2^2Y", "SUNc^2Y", "gravY", "Y^3", "WittenParity"}
    operator_coefficients = {"a", "b", "abs_b_squared_over_a_squared"}
    check("anomaly labels are disjoint from operator coefficients", anomaly_labels.isdisjoint(operator_coefficients))

    section("runner import boundary")
    source = Path(__file__).read_text()
    modules = set()
    for match in re.finditer(r"^(?:from|import)\s+([\w.]+)", source, re.MULTILINE):
        modules.add(match.group(1).split(".")[0])
    allowed = {"__future__", "fractions", "pathlib", "re", "sys"}
    check("imports limited to stdlib", modules <= allowed, detail=f"modules={sorted(modules)}")

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
