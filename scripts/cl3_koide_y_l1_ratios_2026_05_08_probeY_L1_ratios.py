#!/usr/bin/env python3
"""Runner for the bounded Wilson-chain heavy-quark ratio comparator."""

from __future__ import annotations

from pathlib import Path
import math
import re
import sys
from dataclasses import dataclass


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT
    / "docs"
    / "KOIDE_Y_L1_RATIOS_WILSON_INTEGER_DIFF_NOTE_2026-05-08_probeY_L1_ratios.md"
)

ALPHA_LM = 0.090668
M_TAU = 1.77686
MASSES = {
    "t": 172.69,
    "b": 4.18,
    "c": 1.27,
}
GATE = 0.05

PASS = 0
FAIL = 0


@dataclass(frozen=True)
class Fit:
    exponent: float
    label: str
    rel_err: float


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


def delta_n(mass: float) -> float:
    return math.log(mass / M_TAU) / math.log(ALPHA_LM)


def mass_error(actual_mass: float, exponent: float) -> float:
    predicted_ratio = ALPHA_LM ** exponent
    actual_ratio = actual_mass / M_TAU
    return abs(predicted_ratio / actual_ratio - 1.0)


def best_integer(mass: float) -> Fit:
    d = delta_n(mass)
    n = round(d)
    return Fit(float(n), str(n), mass_error(mass, float(n)))


def best_rational(mass: float, max_den: int = 6) -> Fit:
    d = delta_n(mass)
    best: Fit | None = None
    for q in range(1, max_den + 1):
        lo = math.floor(d * q) - 2
        hi = math.ceil(d * q) + 2
        for p in range(lo, hi + 1):
            exponent = p / q
            err = mass_error(mass, exponent)
            fit = Fit(exponent, f"{p}/{q}", err)
            if best is None or fit.rel_err < best.rel_err:
                best = fit
    assert best is not None
    return best


def main() -> int:
    note = NOTE_PATH.read_text()
    note_flat = re.sub(r"\s+", " ", note)

    section("note boundary checks")
    required = [
        "Claim type:** bounded_theorem",
        "source-note proposal only",
        "observational comparators, not derivation inputs",
        "does not derive quark masses",
        "does not rule out other heavy-quark mechanisms",
        "does not depend on or land any sibling absolute-mass probe",
        "assert retained or audited status",
    ]
    for marker in required:
        check(f"note contains {marker[:54]!r}", marker in note_flat)

    section("integer and q<=6 rational fits")
    for name, mass in MASSES.items():
        d = delta_n(mass)
        int_fit = best_integer(mass)
        rat_fit = best_rational(mass, 6)
        check(f"{name}: Delta n finite", math.isfinite(d), detail=f"Delta n={d:.4f}")
        check(
            f"{name}: integer fit fails 5% gate",
            int_fit.rel_err > GATE,
            detail=f"best={int_fit.label}, err={100*int_fit.rel_err:.2f}%",
        )
        check(
            f"{name}: q<=6 rational fit fails 5% gate",
            rat_fit.rel_err > GATE,
            detail=f"best={rat_fit.label}, err={100*rat_fit.rel_err:.2f}%",
        )

    section("near-half-power observation is comparator-only")
    mb_mc_delta = math.log(MASSES["b"] / MASSES["c"]) / math.log(ALPHA_LM)
    mb_mc_err = abs((ALPHA_LM ** (-0.5)) / (MASSES["b"] / MASSES["c"]) - 1.0)
    check("m_b/m_c exponent is near -1/2", abs(mb_mc_delta + 0.5) < 0.02, detail=f"Delta={mb_mc_delta:.4f}")
    check("m_b/m_c half-power error is below 2%", mb_mc_err < 0.02, detail=f"err={100*mb_mc_err:.2f}%")
    check("note says this near relation is not derived", "not as a derived theorem" in note)

    section("runner import boundary")
    source = Path(__file__).read_text()
    modules = set()
    for match in re.finditer(r"^(?:from|import)\s+([\w.]+)", source, re.MULTILINE):
        modules.add(match.group(1).split(".")[0])
    allowed = {"__future__", "dataclasses", "math", "pathlib", "re", "sys"}
    check("imports limited to stdlib", modules <= allowed, detail=f"modules={sorted(modules)}")

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
