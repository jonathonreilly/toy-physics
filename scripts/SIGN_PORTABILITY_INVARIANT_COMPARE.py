#!/usr/bin/env python3
"""Sign portability invariant: read registered family logs and assert thresholds.

Repair target (auditor, audit_status=audited_conditional, claim
sign_portability_invariant_note): replace the hard-coded comparison printer
with a runner that reads registered one-hop family outputs and asserts common
thresholds for zero-source cancellation, neutral cancellation, antisymmetry,
unit-slope tolerance, and basin/seed exclusions.

The runner intentionally stays inside the bounded conditional comparison
claim. It does not extend the claim surface; it only loads the per-row
outputs of the five retained sign-law family runners (plus the fifth-family
radial holdout), parses the rows, and asserts the four invariant gates that
the note proposes as the signed-control fixed point:

    G1. zero-source cancellation: every row has |zero| <= ZERO_TOL
    G2. neutral cancellation:     every row has |neutral| <= NEUTRAL_TOL
    G3. plus/minus antisymmetry:  every row has |plus + minus| <= ANTISYM_TOL
                                  relative to max(|plus|, |minus|)
    G4. unit-slope tolerance:     every PASSING row has |exp - 1| <= EXP_TOL

It also enumerates the basin/seed exclusions per family by listing the rows
that the family runners themselves rejected (the ``no`` rows in the source
logs). G1, G2, G3 are asserted on ALL rows in each log: the signed-control
fixed point requires that the exact controls hold even on the rows the
family runner rejected for sign orientation. G4 is asserted only on the
rows the family runner kept, since unit slope is reported only there.

Exit code 0 = OVERALL PASS, 1 = OVERALL FAIL.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
LOGS_DIR = PROJECT_DIR / "logs"
RUNNER_CACHE_DIR = LOGS_DIR / "runner-cache"

# Common thresholds for the four invariant gates.
ZERO_TOL = 1.0e-12      # zero-source baseline: exact zero
NEUTRAL_TOL = 1.0e-12   # neutral +1/-1 cancellation: exact zero
ANTISYM_TOL = 5.0e-3    # |plus+minus| / max(|plus|,|minus|) for plus/minus antisymmetry
EXP_TOL = 5.0e-3        # |exp - 1| for unit-slope weak-field response


@dataclass(frozen=True)
class ParsedRow:
    """A single per-row record from a family log."""

    family: str
    drift: float
    seed: int
    zero: float
    plus: float
    minus: float
    neutral: float
    double: float
    exp: float
    ok: bool


@dataclass
class FamilyResult:
    family: str
    log_path: Path
    rows: list[ParsedRow] = field(default_factory=list)
    excluded: list[ParsedRow] = field(default_factory=list)
    gate_results: dict[str, bool] = field(default_factory=dict)
    gate_details: dict[str, str] = field(default_factory=dict)


# Registered one-hop family logs. For each family, list candidate per-row
# sources in priority order: runner-cache outputs (preferred, since they
# carry the registered runner SHA + status) come first; the dated log
# files in logs/ are the fallback when the runner-cache is empty (e.g.
# for runners whose latest cached attempt timed out).
FAMILY_LOGS: list[tuple[str, list[Path]]] = [
    (
        "Grown transfer basin",
        [
            RUNNER_CACHE_DIR / "GROWN_TRANSFER_BASIN_SWEEP.txt",
            LOGS_DIR / "2026-04-06-nonlabel-grown-drift-basin-sweep.txt",
        ],
    ),
    (
        "Alternative connectivity family",
        [
            RUNNER_CACHE_DIR / "ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP.txt",
            LOGS_DIR / "2026-04-06-alt-connectivity-family-sign.txt",
        ],
    ),
    (
        "Second grown-family sign",
        [
            RUNNER_CACHE_DIR / "SECOND_GROWN_FAMILY_SIGN_SWEEP.txt",
            LOGS_DIR / "2026-04-06-second-grown-family-sign.txt",
        ],
    ),
    (
        "Third grown-family sign",
        [
            RUNNER_CACHE_DIR / "THIRD_GROWN_FAMILY_SIGN_SWEEP.txt",
            LOGS_DIR / "2026-04-06-third-grown-family-sign.txt",
        ],
    ),
    (
        "Fourth family quadrant",
        [
            RUNNER_CACHE_DIR / "FOURTH_FAMILY_QUADRANT_SWEEP.txt",
            LOGS_DIR / "2026-04-06-fourth-family-quadrant.txt",
        ],
    ),
]

HOLDOUT_LOGS: list[tuple[str, list[Path]]] = [
    (
        "Fifth family radial",
        [
            RUNNER_CACHE_DIR / "FIFTH_FAMILY_RADIAL_SWEEP.txt",
            LOGS_DIR / "2026-04-06-fifth-family-radial.txt",
        ],
    ),
]


# Regex helpers for the various log layouts.
# Number tokens accept either compact ("3.598e-05") or full-precision
# ("+3.598000e-05") scientific notation.
_NUM = r"[-+]?\d+\.\d+e[-+]?\d+"

# Style A: "drift seed | zero plus minus neutral double exp ok"
# (grown drift basin sweep)
_RE_DRIFT_SEED_PIPE = re.compile(
    rf"^\s*(?P<drift>[-+]?\d*\.\d+)\s+(?P<seed>\d+)\s*\|\s*"
    rf"(?P<zero>{_NUM})\s+(?P<plus>{_NUM})\s+(?P<minus>{_NUM})\s+"
    rf"(?P<neutral>{_NUM})\s+(?P<double>{_NUM})\s+"
    rf"(?P<exp>[-+]?\d+\.\d+)\s+(?P<ok>YES|no)\s*$",
    re.IGNORECASE,
)

# Style B: "drift seed zero plus minus neutral double exp ok" (no pipe)
_RE_DRIFT_SEED_PLAIN = re.compile(
    rf"^\s*(?P<drift>[-+]?\d*\.\d+)\s+(?P<seed>\d+)\s+"
    rf"(?P<zero>{_NUM})\s+(?P<plus>{_NUM})\s+(?P<minus>{_NUM})\s+"
    rf"(?P<neutral>{_NUM})\s+(?P<double>{_NUM})\s+"
    rf"(?P<exp>[-+]?\d+\.\d+)\s+(?P<ok>YES|no)\s*$",
    re.IGNORECASE,
)

# Style C: bullet form "- drift X.YY, seed N: zero ..., plus ..., minus ...,
# neutral ..., double ..., alpha A.AAAA" (fourth family quadrant dated log)
_RE_BULLET = re.compile(
    rf"^\s*-\s*drift\s+(?P<drift>[-+]?\d*\.\d+),\s*seed\s+(?P<seed>\d+):\s*"
    rf"zero\s+(?P<zero>{_NUM}),\s*plus\s+(?P<plus>{_NUM}),\s*"
    rf"minus\s+(?P<minus>{_NUM}),\s*neutral\s+(?P<neutral>{_NUM}),\s*"
    rf"double\s+(?P<double>{_NUM}),\s*"
    rf"alpha\s+(?P<exp>[-+]?\d+\.\d+)\s*$",
    re.IGNORECASE,
)

# Style D: "drift seed zero plus minus neutral double alpha" (no ok column,
# fourth family quadrant runner-cache form). The alpha column carries the
# weak-field exponent.
_RE_DRIFT_SEED_NOOK = re.compile(
    rf"^\s*(?P<drift>[-+]?\d*\.\d+)\s+(?P<seed>\d+)\s+"
    rf"(?P<zero>{_NUM})\s+(?P<plus>{_NUM})\s+(?P<minus>{_NUM})\s+"
    rf"(?P<neutral>{_NUM})\s+(?P<double>{_NUM})\s+"
    rf"(?P<exp>[-+]?\d+\.\d+)\s*$",
    re.IGNORECASE,
)


def _parse_row(family: str, line: str) -> ParsedRow | None:
    """Try the four known per-row layouts. Return None if no match."""
    m = _RE_DRIFT_SEED_PIPE.match(line) or _RE_DRIFT_SEED_PLAIN.match(line)
    if m is not None:
        return ParsedRow(
            family=family,
            drift=float(m.group("drift")),
            seed=int(m.group("seed")),
            zero=float(m.group("zero")),
            plus=float(m.group("plus")),
            minus=float(m.group("minus")),
            neutral=float(m.group("neutral")),
            double=float(m.group("double")),
            exp=float(m.group("exp")),
            ok=m.group("ok").upper() == "YES",
        )
    m = _RE_BULLET.match(line) or _RE_DRIFT_SEED_NOOK.match(line)
    if m is not None:
        # Fourth-family quadrant runner-cache and bullet form lack an
        # explicit ok flag. Apply the same sign-orientation acceptance
        # rule the family runner uses: a row counts as passing when the
        # canonical positive-source response (plus) is itself positive
        # AND minus is negative, so the antisymmetric pair carries the
        # expected sign. This reproduces the family runner's "passing
        # rows" count from the SAFE READ block of its log without
        # broadening the claim. Rows where the antisymmetric pair flips
        # sign are recorded as basin/seed exclusions.
        plus_v = float(m.group("plus"))
        minus_v = float(m.group("minus"))
        ok = plus_v > 0.0 and minus_v < 0.0
        return ParsedRow(
            family=family,
            drift=float(m.group("drift")),
            seed=int(m.group("seed")),
            zero=float(m.group("zero")),
            plus=plus_v,
            minus=minus_v,
            neutral=float(m.group("neutral")),
            double=float(m.group("double")),
            exp=float(m.group("exp")),
            ok=ok,
        )
    return None


def _read_family_log(family: str, candidates: list[Path]) -> tuple[list[ParsedRow], Path]:
    """Try each candidate path in priority order; return rows + the path used."""
    last_error: Exception | None = None
    for log_path in candidates:
        if not log_path.is_file():
            last_error = FileNotFoundError(f"missing: {log_path}")
            continue
        rows: list[ParsedRow] = []
        for raw in log_path.read_text().splitlines():
            parsed = _parse_row(family, raw)
            if parsed is not None:
                rows.append(parsed)
        if rows:
            return rows, log_path
        last_error = RuntimeError(
            f"no per-row records in {log_path}; format may have drifted "
            f"or the cached run produced no output (e.g. timeout)."
        )
    if last_error is None:
        last_error = FileNotFoundError(
            f"no candidate logs supplied for family {family!r}"
        )
    raise last_error


def _check_gates(family: str, rows: list[ParsedRow], log_path: Path) -> FamilyResult:
    result = FamilyResult(family=family, log_path=log_path, rows=rows)

    # G1: zero-source cancellation (all rows)
    bad_zero = [r for r in rows if abs(r.zero) > ZERO_TOL]
    result.gate_results["G1_zero_source_cancellation"] = not bad_zero
    result.gate_details["G1_zero_source_cancellation"] = (
        f"max|zero|={max((abs(r.zero) for r in rows), default=0.0):.3e} "
        f"<= {ZERO_TOL:.0e} ; offenders={len(bad_zero)}/{len(rows)}"
    )

    # G2: neutral cancellation (all rows)
    bad_neutral = [r for r in rows if abs(r.neutral) > NEUTRAL_TOL]
    result.gate_results["G2_neutral_cancellation"] = not bad_neutral
    result.gate_details["G2_neutral_cancellation"] = (
        f"max|neutral|={max((abs(r.neutral) for r in rows), default=0.0):.3e} "
        f"<= {NEUTRAL_TOL:.0e} ; offenders={len(bad_neutral)}/{len(rows)}"
    )

    # G3: plus/minus antisymmetry (all rows). Use a relative tolerance on
    # the antisymmetric residual: |plus+minus| / max(|plus|,|minus|).
    def _antisym_residual(r: ParsedRow) -> float:
        denom = max(abs(r.plus), abs(r.minus))
        if denom == 0.0:
            return abs(r.plus + r.minus)
        return abs(r.plus + r.minus) / denom

    residuals = [_antisym_residual(r) for r in rows]
    bad_anti = [r for r, res in zip(rows, residuals) if res > ANTISYM_TOL]
    result.gate_results["G3_plus_minus_antisymmetry"] = not bad_anti
    result.gate_details["G3_plus_minus_antisymmetry"] = (
        f"max|plus+minus|/max(|plus|,|minus|)={max(residuals, default=0.0):.3e} "
        f"<= {ANTISYM_TOL:.0e} ; offenders={len(bad_anti)}/{len(rows)}"
    )

    # G4: unit-slope tolerance on the rows the family runner itself
    # accepted (ok=YES). Rejected rows are the basin/seed exclusions.
    passing = [r for r in rows if r.ok]
    excluded = [r for r in rows if not r.ok]
    result.excluded = excluded
    if passing:
        exp_residuals = [abs(r.exp - 1.0) for r in passing]
        bad_exp = [r for r, res in zip(passing, exp_residuals) if res > EXP_TOL]
        result.gate_results["G4_unit_slope_tolerance"] = not bad_exp
        result.gate_details["G4_unit_slope_tolerance"] = (
            f"max|exp-1|={max(exp_residuals):.3e} <= {EXP_TOL:.0e} on "
            f"{len(passing)} passing rows ; offenders={len(bad_exp)}"
        )
    else:
        result.gate_results["G4_unit_slope_tolerance"] = False
        result.gate_details["G4_unit_slope_tolerance"] = (
            "no passing rows in family log; cannot evaluate unit-slope tolerance"
        )

    return result


def _print_family(result: FamilyResult) -> None:
    print(f"## family: {result.family}")
    print(f"   log: {result.log_path.name}")
    print(f"   rows parsed: {len(result.rows)} ; excluded by family: {len(result.excluded)}")
    for gate, ok in result.gate_results.items():
        flag = "PASS" if ok else "FAIL"
        print(f"   [{flag}] {gate}: {result.gate_details[gate]}")
    if result.excluded:
        excl_pairs = sorted({(r.drift, r.seed) for r in result.excluded})
        print(
            f"   basin/seed exclusions (drift, seed): "
            + ", ".join(f"({d:g},{s})" for d, s in excl_pairs)
        )
    print()


def main() -> int:
    print("# Sign Portability Invariant Comparison")
    print()
    print("Reading registered one-hop family outputs and asserting common")
    print("thresholds for the signed-control fixed point.")
    print()
    print(f"thresholds: ZERO_TOL={ZERO_TOL:.0e} NEUTRAL_TOL={NEUTRAL_TOL:.0e} "
          f"ANTISYM_TOL={ANTISYM_TOL:.0e} EXP_TOL={EXP_TOL:.0e}")
    print()

    all_results: list[FamilyResult] = []
    overall_pass = True

    print("## Core families")
    print()
    for family, candidates in FAMILY_LOGS:
        try:
            rows, log_path = _read_family_log(family, candidates)
        except (FileNotFoundError, RuntimeError) as exc:
            print(f"## family: {family}")
            print(f"   [FAIL] log_load: {exc}")
            print()
            overall_pass = False
            continue
        result = _check_gates(family, rows, log_path)
        all_results.append(result)
        if not all(result.gate_results.values()):
            overall_pass = False
        _print_family(result)

    print("## Holdout (out-of-band confirmation)")
    print()
    for family, candidates in HOLDOUT_LOGS:
        try:
            rows, log_path = _read_family_log(family, candidates)
        except (FileNotFoundError, RuntimeError) as exc:
            print(f"## family: {family}")
            print(f"   [FAIL] log_load: {exc}")
            print()
            overall_pass = False
            continue
        result = _check_gates(family, rows, log_path)
        all_results.append(result)
        if not all(result.gate_results.values()):
            overall_pass = False
        _print_family(result)

    print("## Summary")
    print()
    for result in all_results:
        gate_flags = "".join(
            "P" if ok else "F" for ok in result.gate_results.values()
        )
        print(f"  {result.family:<36} G1G2G3G4 = {gate_flags}")
    print()

    print(
        "Order parameter candidate (unchanged): the portable quantity is the "
        "signed-control fixed point — exact zero-source null, exact neutral "
        "cancellation, plus/minus antisymmetry, and weak-field response near "
        "unit slope. Basin width and seed selectivity remain family-dependent "
        "and are reported above as basin/seed exclusions."
    )
    print()

    if overall_pass:
        print("OVERALL: PASS")
        return 0
    print("OVERALL: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
