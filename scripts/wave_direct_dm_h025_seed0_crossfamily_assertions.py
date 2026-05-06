#!/usr/bin/env python3
"""Log-backed assertions for the seed-0 H=0.25 cross-family compression note.

This runner intentionally checks the frozen Fam1/Fam2 control logs rather than
rerunning the expensive fine-H control sweep.  It certifies only the bounded
two-row compression recorded in WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


AUDIT_TIMEOUT_SEC = 60
ROOT = Path(__file__).resolve().parents[1]


HEADER_RE = re.compile(
    r"family=(?P<family>Fam[0-9]+)\s+.*\bseed=(?P<seed>[0-9]+)\s+H=(?P<h>[0-9.]+)"
)
STRENGTH_RE = re.compile(r"^\[strength=(?P<strength>[0-9.]+)\]")
VALUE_RE = re.compile(r"^\s+(?P<key>dM\(early\)|dM\(late\)|delta_hist|R_hist|delta_hist/s)\s*=\s*(?P<value>[-+0-9.eE]+%?)")
NULL_RE = re.compile(r"null max \|delta_hist\| = (?P<value>[-+0-9.eE]+)")
SIGN_RE = re.compile(r"(?:sign pattern\(nonzero strengths\)|delta_hist sign pattern)\s*=\s*(?P<value>[+\- ]+)")
SPREAD_RE = re.compile(r"\|delta_hist/s\| spread\s*=\s*(?P<value>[-+0-9.]+)%")


@dataclass(frozen=True)
class FamilyExpectation:
    log_path: str
    selected_delta: float
    selected_r_percent: float
    selected_early: float
    selected_late: float
    null_max: float
    sign_pattern: str
    spread_percent: float
    delta_over_s: dict[float, float]


EXPECTED = {
    "Fam1": FamilyExpectation(
        log_path="logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt",
        selected_delta=-0.001256,
        selected_r_percent=-20.12,
        selected_early=0.004989,
        selected_late=0.006246,
        null_max=0.0,
        sign_pattern="- - -",
        spread_percent=7.77,
        delta_over_s={
            0.002: -0.305878,
            0.004: -0.314085,
            0.008: -0.330504,
        },
    ),
    "Fam2": FamilyExpectation(
        log_path="logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt",
        selected_delta=-0.001576,
        selected_r_percent=-22.61,
        selected_early=0.005393,
        selected_late=0.006969,
        null_max=0.0,
        sign_pattern="- - -",
        spread_percent=6.67,
        delta_over_s={
            0.002: -0.385126,
            0.004: -0.393942,
            0.008: -0.411609,
        },
    ),
}


def parse_value(text: str) -> float:
    return float(text.rstrip("%"))


def assert_close(label: str, actual: float, expected: float, tol: float) -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"{label}: expected {expected:+.9g}, got {actual:+.9g}")


def parse_log(family: str, expectation: FamilyExpectation) -> dict[str, object]:
    path = ROOT / expectation.log_path
    if not path.exists():
        raise AssertionError(f"{family}: missing source log {path}")

    rows: dict[float, dict[str, float]] = {}
    current_strength: float | None = None
    parsed: dict[str, object] = {"rows": rows}

    for line in path.read_text(encoding="utf-8").splitlines():
        if match := HEADER_RE.search(line):
            parsed["family"] = match.group("family")
            parsed["seed"] = int(match.group("seed"))
            parsed["h"] = float(match.group("h"))
            continue

        if match := STRENGTH_RE.match(line):
            current_strength = float(match.group("strength"))
            rows[current_strength] = {}
            continue

        if match := VALUE_RE.match(line):
            if current_strength is None:
                raise AssertionError(f"{family}: value before strength block: {line}")
            rows[current_strength][match.group("key")] = parse_value(match.group("value"))
            continue

        if match := NULL_RE.search(line):
            parsed["null_max"] = float(match.group("value"))
            continue

        if match := SIGN_RE.search(line):
            parsed["sign_pattern"] = " ".join(match.group("value").split())
            continue

        if match := SPREAD_RE.search(line):
            parsed["spread_percent"] = float(match.group("value"))
            continue

    required = {"family", "seed", "h", "null_max", "sign_pattern", "spread_percent"}
    missing = sorted(required.difference(parsed))
    if missing:
        raise AssertionError(f"{family}: missing parsed fields {missing} in {path}")

    return parsed


def check_family(family: str, expectation: FamilyExpectation) -> dict[str, object]:
    parsed = parse_log(family, expectation)
    rows = parsed["rows"]
    assert isinstance(rows, dict)

    if parsed["family"] != family:
        raise AssertionError(f"{family}: parsed family label {parsed['family']!r}")
    if parsed["seed"] != 0:
        raise AssertionError(f"{family}: expected seed 0, got {parsed['seed']}")
    assert_close(f"{family} H", float(parsed["h"]), 0.25, 0.0005)
    assert_close(f"{family} null max", float(parsed["null_max"]), expectation.null_max, 0.0)

    if parsed["sign_pattern"] != expectation.sign_pattern:
        raise AssertionError(f"{family}: expected sign pattern {expectation.sign_pattern!r}, got {parsed['sign_pattern']!r}")
    assert_close(f"{family} spread percent", float(parsed["spread_percent"]), expectation.spread_percent, 0.005)

    for strength, expected_delta_over_s in expectation.delta_over_s.items():
        if strength not in rows:
            raise AssertionError(f"{family}: missing strength {strength:.3f}")
        row = rows[strength]
        assert_close(f"{family} strength {strength:.3f} delta_hist/s", row["delta_hist/s"], expected_delta_over_s, 0.000001)
        if row["delta_hist"] >= 0:
            raise AssertionError(f"{family}: strength {strength:.3f} delta_hist should be negative")

    if 0.0 not in rows:
        raise AssertionError(f"{family}: missing null strength row")
    null_delta = rows[0.0]["delta_hist"]
    assert_close(f"{family} null delta_hist", null_delta, 0.0, 0.0)

    selected = rows[0.004]
    assert_close(f"{family} selected dM early", selected["dM(early)"], expectation.selected_early, 0.0000005)
    assert_close(f"{family} selected dM late", selected["dM(late)"], expectation.selected_late, 0.0000005)
    assert_close(f"{family} selected delta_hist", selected["delta_hist"], expectation.selected_delta, 0.0000005)
    assert_close(f"{family} selected R_hist percent", selected["R_hist"], expectation.selected_r_percent, 0.005)

    return parsed


def main() -> int:
    parsed = {family: check_family(family, expectation) for family, expectation in EXPECTED.items()}

    fam1_row = parsed["Fam1"]["rows"][0.004]  # type: ignore[index]
    fam2_row = parsed["Fam2"]["rows"][0.004]  # type: ignore[index]

    if not (fam1_row["delta_hist"] < 0 and fam2_row["delta_hist"] < 0):
        raise AssertionError("selected rows must share negative delta_hist sign")
    if abs(fam2_row["delta_hist"]) <= abs(fam1_row["delta_hist"]):
        raise AssertionError("selected ordering failed: Fam2 delta magnitude is not deeper than Fam1")
    if fam2_row["R_hist"] >= fam1_row["R_hist"]:
        raise AssertionError("selected ordering failed: Fam2 R_hist is not more negative than Fam1")

    fam1_late_gain = fam1_row["dM(late)"] - fam1_row["dM(early)"]
    fam2_late_gain = fam2_row["dM(late)"] - fam2_row["dM(early)"]
    assert_close("Fam1 selected late gain", fam1_late_gain, 0.001257, 0.000001)
    assert_close("Fam2 selected late gain", fam2_late_gain, 0.001576, 0.000001)

    print("WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_ASSERTIONS=TRUE")
    print("WAVE_DIRECT_DM_H025_SEED0_SHARED_SIGN=negative")
    print("WAVE_DIRECT_DM_H025_SEED0_COMMON_ORDERING=Fam2_deeper_than_Fam1_at_strength_0.004")
    print("WAVE_DIRECT_DM_H025_SEED0_WEAK_FIELD_CONTROL=TRUE")
    print("WAVE_DIRECT_DM_H025_SEED0_PORTABILITY_LAW=FALSE")
    print("WAVE_DIRECT_DM_H025_STABLE_AMPLITUDE_LAW=FALSE")
    print("RESIDUAL_SCOPE=fam3_and_family_wide_portability_not_claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
