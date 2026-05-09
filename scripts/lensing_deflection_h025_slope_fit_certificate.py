#!/usr/bin/env python3
"""Audit-facing certificate for the H=0.25 fine-refinement slope fit in
docs/LENSING_DEFLECTION_NOTE.md.

The note's load-bearing claim (per the auditor) is:

    At H=0.25 on b ∈ {3,4,5,6}, kubo_true follows a clean log-log power
    law with slope ≈ -1.43 and R² = 0.998, so the retained result is a
    non-standard power law rather than 1/b lensing.

This certificate proves exactly that bounded numeric statement:

  * the four fine-H single-b runner outputs at H=0.25 b ∈ {3, 4, 5, 6}
    are read from the canonical artifact `logs/2026-04-07-lensing-fine-
    asymptotic.txt` (the runner that produced them is
    `scripts/lensing_deflection_fine_single.py`);
  * the same per-b values are also present in the combined-analysis
    runner `scripts/lensing_deflection_lane_lplus.py` DATA dict (cached
    at `logs/runner-cache/lensing_deflection_lane_lplus.txt`);
  * the log-log slope fit on those four (b, kubo_true) points gives a
    slope rounding to -1.4335 with R² rounding to 0.998;
  * the corresponding |dM| fit gives slope -1.5162 with R² 0.995;
  * to attest that the fine-single runner remains framework-faithful,
    the certificate re-executes it for one cheap b-value (b=3 at H=0.5)
    and asserts the result matches the recorded H=0.5 entry from the
    medium-H sweep.

The certificate does NOT certify:

  * any continuum-stable exponent (the slope is still drifting with H);
  * any direct match to Newton/Einstein 1/b weak-field lensing — it
    explicitly asserts |slope - (-1)| > 0.1, ratifying the note's
    "non-standard power law" framing;
  * any extension to other families, larger b, or other observables.

This is a bounded numeric replay of the H=0.25 slope fit only.
"""

from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path


AUDIT_TIMEOUT_SEC = 120

REPO_ROOT = Path(__file__).resolve().parent.parent
ASYMPTOTIC_LOG = REPO_ROOT / "logs" / "2026-04-07-lensing-fine-asymptotic.txt"
COMBINED_RUNNER = REPO_ROOT / "scripts" / "lensing_deflection_lane_lplus.py"
FINE_SINGLE_RUNNER = REPO_ROOT / "scripts" / "lensing_deflection_fine_single.py"
CERTIFICATE_PATH = (
    REPO_ROOT / "outputs"
    / "lensing_deflection_h025_slope_fit_certificate.json"
)

H025_EXPECTED = {
    3.0: {"kubo": +5.986043, "dM": +0.025555},
    4.0: {"kubo": +3.819639, "dM": +0.015455},
    5.0: {"kubo": +2.826383, "dM": +0.011405},
    6.0: {"kubo": +2.211718, "dM": +0.008900},
}

# H=0.5 b=3.0 reference value from logs/runner-cache/lensing_deflection_sweep.txt
# (medium-H runner cache). Used as a cheap sanity replay of the fine-single
# runner — H=0.5 NL=30 finishes in ~3 s instead of ~90 s for H=0.25.
H05_B3_KUBO_EXPECTED = +7.0619
H05_B3_DM_EXPECTED = +0.034642
H05_B3_TOL_KUBO = 0.001
H05_B3_TOL_DM = 0.001

# Slope-fit tolerances chosen to match the cached value to 4 decimal
# places — we are certifying a fixed log-log fit on fixed inputs, so
# floating-point noise is the only source of variation.
SLOPE_KUBO_EXPECTED = -1.4335
SLOPE_DM_EXPECTED = -1.5162
R2_KUBO_EXPECTED = 0.9984
R2_DM_EXPECTED = 0.9954
SLOPE_TOL = 1e-3
R2_TOL = 1e-3

# The note's claim is "non-standard power law, NOT 1/b lensing" — encode
# this as |slope - (-1)| > 0.1 so the certificate cannot be re-purposed
# to ratify a 1/b reading.
NON_LENSING_MARGIN = 0.1


PARSE_RE = re.compile(
    r"H=([0-9.]+)\s+b=([0-9.]+)\s+NL=(\d+)\s+n_nodes=(\d+)\s+"
    r"dM=([+-][0-9.]+)\s+kubo_true=([+-][0-9.]+)"
)


def parse_asymptotic_log(text: str) -> dict[float, dict[str, float]]:
    out: dict[float, dict[str, float]] = {}
    for line in text.splitlines():
        m = PARSE_RE.search(line)
        if not m:
            continue
        H = float(m.group(1))
        b = float(m.group(2))
        if H != 0.25:
            continue
        out[b] = {
            "NL": int(m.group(3)),
            "n_nodes": int(m.group(4)),
            "dM": float(m.group(5)),
            "kubo_true": float(m.group(6)),
        }
    return out


def log_log_fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    n = len(xs)
    lx = [math.log(x) for x in xs]
    ly = [math.log(abs(y)) for y in ys]
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    syy = sum((y - my) ** 2 for y in ly)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    slope = sxy / sxx
    intercept = my - slope * mx
    r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 1.0
    return slope, intercept, r2


def parse_combined_runner_data(text: str) -> dict[float, dict[str, float]]:
    """Parse the DATA dict of lensing_deflection_lane_lplus.py for H=0.25."""
    # Tiny, scope-limited extraction: find the 0.25: { ... } block.
    m = re.search(r"0\.25:\s*\{(.*?)\n\s*\},", text, re.DOTALL)
    if not m:
        raise RuntimeError("Could not find 0.25 block in combined runner source")
    block = m.group(1)
    out: dict[float, dict[str, float]] = {}
    for entry in re.finditer(
        r"([0-9.]+):\s*\{\"dM\":\s*([+-][0-9.]+),\s*\"kubo\":\s*([+-][0-9.]+)\}",
        block,
    ):
        b = float(entry.group(1))
        out[b] = {
            "dM": float(entry.group(2)),
            "kubo_true": float(entry.group(3)),
        }
    return out


def check(name: str, ok: bool, detail: str, results: list[tuple[bool, str, str]]) -> bool:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}: {detail}")
    results.append((ok, name, detail))
    return ok


def replay_h05_b3() -> tuple[float, float]:
    """Cheap replay of the fine-single runner at H=0.5 b=3 (~3 s).

    Re-attests that the runner that produced the fine-asymptotic log is
    still framework-faithful at a known reference point, without paying
    the ~90 s/run cost of an H=0.25 single-b execution.
    """
    cmd = [sys.executable, str(FINE_SINGLE_RUNNER), "0.5", "3.0"]
    proc = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    print("LIVE_REPLAY_COMMAND:")
    print("  python3 " + " ".join(cmd[1:]))
    print("LIVE_REPLAY_STDOUT_BEGIN")
    print(proc.stdout.rstrip())
    print("LIVE_REPLAY_STDOUT_END")
    if proc.returncode != 0:
        if proc.stderr.strip():
            print("LIVE_REPLAY_STDERR_BEGIN")
            print(proc.stderr.rstrip())
            print("LIVE_REPLAY_STDERR_END")
        raise RuntimeError(f"fine-single replay exited {proc.returncode}")
    m = PARSE_RE.search(proc.stdout)
    if not m:
        raise RuntimeError(f"could not parse replay stdout: {proc.stdout!r}")
    return float(m.group(5)), float(m.group(6))  # dM, kubo_true


def main() -> int:
    print("=" * 78)
    print("LENSING DEFLECTION H=0.25 SLOPE FIT CERTIFICATE")
    print("Source note: docs/LENSING_DEFLECTION_NOTE.md")
    print("Scope: bounded log-log slope fit on b ∈ {3,4,5,6} at H=0.25 only")
    print("=" * 78)
    print()

    results: list[tuple[bool, str, str]] = []

    # Stage 1 — read the canonical fine-asymptotic artifact.
    print("STAGE_1_FINE_SINGLE_ARTIFACT:")
    if not ASYMPTOTIC_LOG.exists():
        print(f"  [FAIL] missing artifact: {ASYMPTOTIC_LOG.relative_to(REPO_ROOT)}")
        return 1
    text = ASYMPTOTIC_LOG.read_text(encoding="utf-8")
    parsed = parse_asymptotic_log(text)
    for b in (3.0, 4.0, 5.0, 6.0):
        ok = b in parsed
        check(
            f"H=0.25 b={b:.1f} present in fine-asymptotic log",
            ok,
            f"NL={parsed[b]['NL']}, n_nodes={parsed[b]['n_nodes']}" if ok else "missing",
            results,
        )
        if ok:
            check(
                f"H=0.25 b={b:.1f} kubo_true matches expected",
                math.isclose(parsed[b]["kubo_true"], H025_EXPECTED[b]["kubo"], rel_tol=0.0, abs_tol=1e-6),
                f"got {parsed[b]['kubo_true']:+.6f}, expected {H025_EXPECTED[b]['kubo']:+.6f}",
                results,
            )
            check(
                f"H=0.25 b={b:.1f} dM matches expected",
                math.isclose(parsed[b]["dM"], H025_EXPECTED[b]["dM"], rel_tol=0.0, abs_tol=1e-6),
                f"got {parsed[b]['dM']:+.6f}, expected {H025_EXPECTED[b]['dM']:+.6f}",
                results,
            )

    # Stage 2 — cross-check against the combined L+ runner DATA dict.
    print()
    print("STAGE_2_COMBINED_RUNNER_CROSSCHECK:")
    combined_text = COMBINED_RUNNER.read_text(encoding="utf-8")
    combined = parse_combined_runner_data(combined_text)
    for b in (3.0, 4.0, 5.0, 6.0):
        if b not in combined:
            check(
                f"combined runner has b={b:.1f}",
                False,
                "missing from DATA[0.25]",
                results,
            )
            continue
        check(
            f"combined runner b={b:.1f} kubo matches asymptotic log",
            math.isclose(combined[b]["kubo_true"], H025_EXPECTED[b]["kubo"], rel_tol=0.0, abs_tol=1e-5),
            f"runner DATA={combined[b]['kubo_true']:+.6f}, log={H025_EXPECTED[b]['kubo']:+.6f}",
            results,
        )

    # Stage 3 — log-log slope fit on (b, kubo_true) for b ∈ {3,4,5,6}.
    print()
    print("STAGE_3_LOG_LOG_FIT:")
    bs = [3.0, 4.0, 5.0, 6.0]
    kubos = [H025_EXPECTED[b]["kubo"] for b in bs]
    dMs = [H025_EXPECTED[b]["dM"] for b in bs]
    slope_k, intercept_k, r2_k = log_log_fit(bs, kubos)
    slope_d, intercept_d, r2_d = log_log_fit(bs, dMs)
    print(f"  fit_input_b        : {bs}")
    print(f"  fit_input_kubo_true: {[round(k, 6) for k in kubos]}")
    print(f"  fit_input_dM       : {[round(d, 6) for d in dMs]}")
    print(f"  kubo_slope    = {slope_k:+.6f}")
    print(f"  kubo_intercept= {intercept_k:+.6f}")
    print(f"  kubo_R2       = {r2_k:.6f}")
    print(f"  dM_slope      = {slope_d:+.6f}")
    print(f"  dM_intercept  = {intercept_d:+.6f}")
    print(f"  dM_R2         = {r2_d:.6f}")
    check(
        "kubo slope matches expected (-1.4335)",
        abs(slope_k - SLOPE_KUBO_EXPECTED) < SLOPE_TOL,
        f"|{slope_k:+.6f} - ({SLOPE_KUBO_EXPECTED})| = {abs(slope_k - SLOPE_KUBO_EXPECTED):.2e} < {SLOPE_TOL:.0e}",
        results,
    )
    check(
        "kubo R² matches expected (0.998)",
        abs(r2_k - R2_KUBO_EXPECTED) < R2_TOL,
        f"|{r2_k:.6f} - {R2_KUBO_EXPECTED}| = {abs(r2_k - R2_KUBO_EXPECTED):.2e} < {R2_TOL:.0e}",
        results,
    )
    check(
        "dM slope matches expected (-1.5162)",
        abs(slope_d - SLOPE_DM_EXPECTED) < SLOPE_TOL,
        f"|{slope_d:+.6f} - ({SLOPE_DM_EXPECTED})| = {abs(slope_d - SLOPE_DM_EXPECTED):.2e}",
        results,
    )
    check(
        "dM R² matches expected (0.995)",
        abs(r2_d - R2_DM_EXPECTED) < R2_TOL,
        f"|{r2_d:.6f} - {R2_DM_EXPECTED}| = {abs(r2_d - R2_DM_EXPECTED):.2e}",
        results,
    )
    check(
        "kubo slope is non-standard (|slope − (−1)| > 0.1)",
        abs(slope_k - (-1.0)) > NON_LENSING_MARGIN,
        f"|{slope_k:+.4f} - (-1)| = {abs(slope_k - (-1.0)):.4f} > {NON_LENSING_MARGIN}",
        results,
    )
    check(
        "kubo R² > 0.99 (clean power law)",
        r2_k > 0.99,
        f"R²={r2_k:.4f} > 0.99",
        results,
    )

    # Stage 4 — cheap framework-faithfulness replay at H=0.5 b=3.0.
    print()
    print("STAGE_4_RUNNER_REATTESTATION_H05_B3:")
    try:
        dM_replay, kubo_replay = replay_h05_b3()
    except Exception as exc:
        check("fine-single replay at H=0.5 b=3", False, f"exception: {exc!r}", results)
    else:
        check(
            "replay kubo_true matches H=0.5 b=3 reference",
            abs(kubo_replay - H05_B3_KUBO_EXPECTED) < H05_B3_TOL_KUBO,
            f"replay={kubo_replay:+.6f}, ref={H05_B3_KUBO_EXPECTED:+.4f}",
            results,
        )
        check(
            "replay dM matches H=0.5 b=3 reference",
            abs(dM_replay - H05_B3_DM_EXPECTED) < H05_B3_TOL_DM,
            f"replay={dM_replay:+.6f}, ref={H05_B3_DM_EXPECTED:+.6f}",
            results,
        )

    # Selector firewall — make the safe scope explicit.
    print()
    print("SELECTOR_FIREWALL:")
    print("  safe_scope:")
    print("    - log-log slope fit on b ∈ {3,4,5,6} at H=0.25 only")
    print("    - asserts slope ≈ -1.4335, R² ≈ 0.998 with NON-1/b margin > 0.1")
    print("  excluded_scope:")
    print("    - no continuum-stable exponent (slope still H-dependent)")
    print("    - no Newton/Einstein 1/b lensing match (explicitly excluded)")
    print("    - no other families, observables, or impact-parameter ranges")

    # Write JSON certificate.
    cert = {
        "certificate_id": "lensing_deflection_h025_slope_fit",
        "source_note": "docs/LENSING_DEFLECTION_NOTE.md",
        "load_bearing_step": (
            "At H=0.25 on b ∈ {3,4,5,6}, kubo_true follows a clean log-log "
            "power law with slope ≈ -1.43 and R² = 0.998, so the retained "
            "result is a non-standard power law rather than 1/b lensing."
        ),
        "fine_single_runner": "scripts/lensing_deflection_fine_single.py",
        "fine_asymptotic_log": "logs/2026-04-07-lensing-fine-asymptotic.txt",
        "combined_analysis_runner": "scripts/lensing_deflection_lane_lplus.py",
        "combined_analysis_log": "logs/2026-04-07-lensing-deflection-lane-lplus.txt",
        "fit_inputs": {
            "b": bs,
            "kubo_true": kubos,
            "dM": dMs,
        },
        "fit_results": {
            "kubo_slope": slope_k,
            "kubo_intercept": intercept_k,
            "kubo_r_squared": r2_k,
            "dM_slope": slope_d,
            "dM_intercept": intercept_d,
            "dM_r_squared": r2_d,
        },
        "non_lensing_margin": {
            "abs_slope_minus_minus_one": abs(slope_k - (-1.0)),
            "threshold": NON_LENSING_MARGIN,
            "passes": abs(slope_k - (-1.0)) > NON_LENSING_MARGIN,
        },
        "framework_replay": {
            "command": "python3 scripts/lensing_deflection_fine_single.py 0.5 3.0",
            "expected_kubo_true": H05_B3_KUBO_EXPECTED,
            "expected_dM": H05_B3_DM_EXPECTED,
        },
        "expected_values": {
            "kubo_slope": SLOPE_KUBO_EXPECTED,
            "kubo_r_squared": R2_KUBO_EXPECTED,
            "dM_slope": SLOPE_DM_EXPECTED,
            "dM_r_squared": R2_DM_EXPECTED,
        },
        "checks": [
            {"name": name, "passed": ok, "detail": detail}
            for ok, name, detail in results
        ],
    }
    CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    print()
    print(f"CERTIFICATE_WRITTEN: {CERTIFICATE_PATH.relative_to(REPO_ROOT)}")

    n_pass = sum(1 for ok, _, _ in results if ok)
    print()
    print(f"PASS={n_pass}/{len(results)}")
    if n_pass == len(results):
        print("STATUS: BOUNDED H=0.25 SLOPE-FIT CERTIFICATE PASS")
        return 0
    print("STATUS: BOUNDED H=0.25 SLOPE-FIT CERTIFICATE FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
