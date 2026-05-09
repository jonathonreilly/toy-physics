#!/usr/bin/env python3
"""Mirror Chokepoint Note — registered certificate runner (2026-05-09 narrowing).

Mechanically verifies that the narrow retained table in
    docs/MIRROR_CHOKEPOINT_NOTE.md
matches the strict default runner-cache produced by
    scripts/mirror_chokepoint_joint.py
on its registered cache file
    logs/runner-cache/mirror_chokepoint_joint.txt

The retained scope is strictly the strict default card:
    NPL_HALF=25, connect_radius=4.0, layer2_prob=0.0, k=5.0, 16 seeds
at N=15 and N=25 (mirror p2=0 rows).

The runner exits 0 on PASS and nonzero on:
  - missing or unreadable strict joint cache
  - cache header drift (status != ok or exit_code != 0)
  - missing N=15 or N=25 mirror p2=0 row
  - any retained-row metric drift from the cache value
  - missing N=40/60/80/100 FAIL marker (these rows are claimed FAIL on this card)

This is intentionally a thin replay-of-cache assertion gate — it does not
re-run the strict joint runner. The strict joint runner has its own SHA-pinned
cache; this certificate verifies the note's table against that cache.

Out-of-scope rows (NPL_HALF=50 scaling, NPL_HALF=55 boundary scans,
layer2_prob=0.02 sparse rescue, and the dense NPL_HALF=60 boundary card) are
covered separately or not at all; they are NOT part of this note's retained
scope and are NOT asserted on here.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STRICT_CACHE = REPO_ROOT / "logs" / "runner-cache" / "mirror_chokepoint_joint.txt"

# Retained-row claims for the strict default card (mirror p2=0).
# Each entry must match the cache row exactly for PASS.
RETAINED_ROWS = {
    15: {
        "d_TV": 0.9716,
        "pur_cl_mean": 0.5769,
        "pur_cl_se": 0.02,
        "S_norm": 1.0006,
        "gravity_mean": 1.2927,
        "gravity_se": 0.691,
        "born_max": 1e-10,  # |I3|/P must be below 1e-10 (machine-precision Born)
        "k0_max_abs": 1e-12,
        "seeds_ok_min": 1,  # cache row shows 11/16; require any positive count
        "seeds_ok_expected": 11,
    },
    25: {
        "d_TV": 0.8014,
        "pur_cl_mean": 0.7329,
        "pur_cl_se": 0.05,
        "S_norm": 0.9986,
        "gravity_mean": 2.2748,
        "gravity_se": 0.525,
        "born_max": 1e-10,
        "k0_max_abs": 1e-12,
        "seeds_ok_min": 1,
        "seeds_ok_expected": 13,
    },
}

# Rows the note claims FAIL on this strict default card. Out of retained scope
# but recorded as part of the note's narrow read.
EXPECTED_FAIL_NS = (40, 60, 80, 100)

# Tolerance on numeric drift between note table and cache row.
NUM_TOL = 5e-4


def report(name: str, ok: bool, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    sep = " — " if detail else ""
    print(f"  [{status}] {name}{sep}{detail}")
    return ok


PLUSMINUS = "±"  # ±


_MIRROR_LINE_RE = re.compile(
    r"^\s*(\d+)\s+mirror p2=0"
    r"\s+(?P<d_tv>[\d.]+)"
    r"\s+(?P<pur_mean>[\d.]+)" + re.escape(PLUSMINUS) + r"(?P<pur_se>[\d.]+)"
    r"\s+(?P<s_norm>[\d.]+)"
    r"\s+(?P<grav_sign>[+\-])(?P<grav_mean>[\d.]+)" + re.escape(PLUSMINUS) + r"(?P<grav_se>[\d.]+)"
    r"\s+(?P<born>[\deE.+\-]+)"
    r"\s+(?P<k0_sign>[+\-])(?P<k0>[\deE.+\-]+)"
    r"\s+(?P<seeds_ok>\d+)\s+(?P<elapsed>\d+s)\s*$",
)

_MIRROR_FAIL_RE = re.compile(
    r"^\s*(\d+)\s+mirror p2=0\s+FAIL\s+\d+s\s*$",
)

_HEADER_RE = re.compile(
    r"NPL_HALF=(?P<npl_half>\d+).+?k=(?P<k>[\d.]+),\s*(?P<seeds>\d+)\s*seeds",
)


def parse_cache(text: str) -> dict:
    """Parse the strict joint cache into a structured dict."""
    out = {
        "header_ok": False,
        "exit_ok": False,
        "header_setup": None,
        "rows_pass": {},
        "rows_fail": set(),
    }
    if "exit_code: 0" in text and "status: ok" in text:
        out["exit_ok"] = True
    m = _HEADER_RE.search(text)
    if m:
        out["header_ok"] = True
        out["header_setup"] = {
            "npl_half": int(m.group("npl_half")),
            "k": float(m.group("k")),
            "seeds": int(m.group("seeds")),
        }
    for line in text.splitlines():
        mm = _MIRROR_LINE_RE.match(line)
        if mm:
            n = int(mm.group(1))
            grav_sign = +1 if mm.group("grav_sign") == "+" else -1
            k0_sign = +1 if mm.group("k0_sign") == "+" else -1
            out["rows_pass"][n] = {
                "d_TV": float(mm.group("d_tv")),
                "pur_cl_mean": float(mm.group("pur_mean")),
                "pur_cl_se": float(mm.group("pur_se")),
                "S_norm": float(mm.group("s_norm")),
                "gravity_mean": grav_sign * float(mm.group("grav_mean")),
                "gravity_se": float(mm.group("grav_se")),
                "born": float(mm.group("born")),
                "k0_signed": k0_sign * float(mm.group("k0")),
                "seeds_ok": int(mm.group("seeds_ok")),
            }
            continue
        ff = _MIRROR_FAIL_RE.match(line)
        if ff:
            out["rows_fail"].add(int(ff.group(1)))
    return out


def check_cache_present() -> tuple[bool, str | None]:
    if not STRICT_CACHE.exists():
        report("strict joint cache present", False,
               f"missing: {STRICT_CACHE.relative_to(REPO_ROOT)}")
        return False, None
    try:
        text = STRICT_CACHE.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        report("strict joint cache readable", False, f"{exc!r}")
        return False, None
    report("strict joint cache present and readable",
           True, str(STRICT_CACHE.relative_to(REPO_ROOT)))
    return True, text


def check_cache_header_clean(parsed: dict) -> bool:
    ok = parsed["exit_ok"]
    report("cache header status=ok exit_code=0", ok)
    return ok


def check_setup_matches(parsed: dict) -> bool:
    setup = parsed["header_setup"]
    if setup is None:
        return report("cache contains strict NPL_HALF=25 k=5.0 16-seed header",
                      False, "header line not parsed")
    ok = (setup["npl_half"] == 25 and abs(setup["k"] - 5.0) < 1e-9
          and setup["seeds"] == 16)
    return report(
        "cache contains strict NPL_HALF=25 k=5.0 16-seed header",
        ok,
        f"npl_half={setup['npl_half']}, k={setup['k']}, seeds={setup['seeds']}",
    )


def _close(a: float, b: float, tol: float = NUM_TOL) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol


def check_retained_row(n: int, claim: dict, cache_row: dict | None) -> bool:
    if cache_row is None:
        return report(f"N={n} mirror p2=0 row present in cache", False,
                      "row missing")
    checks = []
    checks.append(("d_TV", _close(cache_row["d_TV"], claim["d_TV"])))
    checks.append(("pur_cl_mean",
                   _close(cache_row["pur_cl_mean"], claim["pur_cl_mean"])))
    checks.append(("pur_cl_se",
                   _close(cache_row["pur_cl_se"], claim["pur_cl_se"])))
    checks.append(("S_norm", _close(cache_row["S_norm"], claim["S_norm"])))
    checks.append(("gravity_mean",
                   _close(cache_row["gravity_mean"], claim["gravity_mean"])))
    checks.append(("gravity_se",
                   _close(cache_row["gravity_se"], claim["gravity_se"])))
    checks.append(("born_below_1e-10",
                   cache_row["born"] < claim["born_max"]))
    checks.append(("k0_below_1e-12",
                   abs(cache_row["k0_signed"]) < claim["k0_max_abs"]))
    checks.append(("seeds_ok_expected",
                   cache_row["seeds_ok"] == claim["seeds_ok_expected"]))
    checks.append(("gravity_positive",
                   cache_row["gravity_mean"] > 0))
    all_ok = all(passed for _, passed in checks)
    detail_parts = [
        f"{name}={'ok' if passed else 'DRIFT'}" for name, passed in checks
    ]
    report(f"N={n} mirror p2=0 row matches retained-table claim",
           all_ok,
           "; ".join(detail_parts))
    return all_ok


def check_fail_rows_marked(parsed: dict) -> bool:
    missing = [n for n in EXPECTED_FAIL_NS if n not in parsed["rows_fail"]]
    ok = not missing
    return report(
        "cache marks N=40, 60, 80, 100 mirror p2=0 as FAIL on this card",
        ok,
        f"missing FAIL rows: {missing}" if missing else "all four present",
    )


def main() -> int:
    print("=" * 70)
    print("MIRROR CHOKEPOINT NOTE — RETAINED-ROW CERTIFICATE")
    print("Source note: docs/MIRROR_CHOKEPOINT_NOTE.md")
    print("Cache:       logs/runner-cache/mirror_chokepoint_joint.txt")
    print("Scope:       strict default card N=15 and N=25 (mirror p2=0)")
    print("=" * 70)
    print()

    ok_cache, text = check_cache_present()
    if not ok_cache or text is None:
        print()
        print("PASS=0/?  STATUS: CERTIFICATE FAIL (cache missing/unreadable)")
        return 1

    parsed = parse_cache(text)

    checks: list[bool] = []
    checks.append(check_cache_header_clean(parsed))
    checks.append(check_setup_matches(parsed))
    for n, claim in RETAINED_ROWS.items():
        checks.append(check_retained_row(n, claim, parsed["rows_pass"].get(n)))
    checks.append(check_fail_rows_marked(parsed))

    n_pass = sum(1 for c in checks if c)
    n_total = len(checks)
    print()
    print(f"PASS={n_pass}/{n_total}")
    if n_pass == n_total:
        print("STATUS: RETAINED-ROW CERTIFICATE PASS — note's narrow N=15/25 "
              "table matches strict joint runner-cache; out-of-scope rows are "
              "explicitly excluded.")
        return 0
    print("STATUS: RETAINED-ROW CERTIFICATE FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
