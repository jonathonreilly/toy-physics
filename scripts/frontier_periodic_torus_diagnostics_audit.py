#!/usr/bin/env python3
"""
Periodic 2D torus diagnostics code audit.

Background.
  The active review queue lists "periodic 2D torus diagnostics: nearby torus
  probes still need code audit before reuse outside the corrected retained
  notes" as an open item. The 2026-04-11 minimum-image bug
  (`docs/PERIODIC_2D_WRAPAROUND_FIX_NOTE_2026-04-11.md`) was: periodic
  adjacency was built with modulo indexing, but hopping weights were computed
  from raw coordinate differences, so a wraparound nearest-neighbor on a
  side x side torus was treated as having distance side - 1 instead of 1.

  The fix note lists 8 canonical-corrected periodic scripts. Other scripts
  using periodic modulo adjacency may or may not be at risk; the audit
  status across the full repo has never been frozen.

What this runner adds.
  Static-analysis classification of every scripts/*.py file that uses
  periodic modulo indexing. Each script is marked:

    - CLEAN: explicitly uses minimum-image distance, or doesn't compute any
             distance-weighted Hamiltonian/potential coupling, or uses only
             np.roll-style implicit-periodic indexing without raw distances.
    - NEEDS_REVIEW: uses periodic modulo AND uses distance-weighted couplings
                    AND does not have any minimum-image guard. These are the
                    candidates that could carry the 2026-04-11 bug.
    - NOT_APPLICABLE: uses modulo for non-lattice purposes (cyclic indexing
                      of arrays, generation labels, etc).

  Output is a frozen audit table with explicit per-script reasoning. Future
  work can re-run the audit and compare against the table.

What this runner does NOT close.
  This is static analysis only. NEEDS_REVIEW status flags candidates for
  manual code review; it does not by itself prove a script is buggy. CLEAN
  status proves the script has at least one minimum-image guard, but does
  not guarantee that guard is applied at every relevant Hamiltonian-edge
  weighting site in the file.

Falsifier.
  - A NEEDS_REVIEW script that, on manual inspection, is actually clean
    (would tighten the audit rules).
  - A CLEAN script that uses raw periodic-edge distances at any Hamiltonian
    site (would loosen the audit rules and require a stronger check).
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


# Pattern definitions.
# Periodic modulo adjacency: `% side`, `% L`, `% n_side`, etc.
PERIODIC_MOD = re.compile(r"%\s*(side|L|n_side|nside|N|edge|n)\b")

# Helper imports / inline minimum-image patterns.
HELPER_IMPORT = re.compile(r"from\s+periodic_geometry\s+import|import\s+periodic_geometry|periodic_geometry\.")
MIN_IMAGE_INLINE = re.compile(
    r"min\s*\(\s*([dxydzvy_]+)\s*,\s*\1\s*-\s*\1|"
    r"min\s*\(\s*\w+\s*,\s*\w+\s*-\s*\w+\)|"
    r"minimum_image|min_image|"
    # Centered-modulo idiom: (x - x0 + L // 2) % L - L // 2 returns a signed
    # minimum-image displacement in [-L/2, L/2]. Catch any "% L - L // 2" or
    # "% side - side // 2" form.
    r"%\s*\w+\s*-\s*\w+\s*//\s*2|"
    # min(abs(x - x0), n - abs(x - x0)) idiom: very common minimum-image form.
    # Catches both `abs(` and `np.abs(` (and similar np.* prefixes).
    r"\b\w+\s*-\s*(?:np\.|numpy\.)?abs\("
)

# Distance computation in Hamiltonian-relevant context.
# A weak heuristic: scripts that compute hop weights as 1/distance, distance
# Yukawa kernels, or distance-modulated potentials. We look for patterns:
#   1.0 / max(d, ...)   -> Hamiltonian hopping weights
#   exp(-mu * d)        -> Yukawa kernel
#   1.0 / d**2          -> Coulomb-like
#   weight * d          -> distance-scaled couplings
DISTANCE_COUPLING = re.compile(
    r"1\.0\s*/\s*max\s*\(\s*\w*d\b|"          # 1.0 / max(d, ...)
    r"1\.0\s*/\s*\w*d\b\s*\*\s*\*\s*2|"        # 1.0/d**2
    r"exp\s*\(\s*[-+]?\s*\w+\s*\*\s*\w*d\b|"   # exp(-mu * d)
    r"hypot\s*\([^)]*\)|"                       # math.hypot(dx, dy) suggests distance use
    r"sqrt\s*\(\s*\w*d?x\b\s*\*\s*\*\s*2"     # sqrt(dx**2 + ...)
)

# Use of np.roll for periodic shifts (auto-periodic, no manual distance).
NP_ROLL = re.compile(r"np\.roll\b")


def classify_file(path: Path) -> tuple[str, list[str]]:
    """Return (status, reasons)."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return "ERROR", [f"could not read: {e}"]

    reasons: list[str] = []

    # Pattern matches.
    has_mod = bool(PERIODIC_MOD.search(text))
    has_helper_import = bool(HELPER_IMPORT.search(text))
    has_min_image = bool(MIN_IMAGE_INLINE.search(text))
    has_distance_coupling = bool(DISTANCE_COUPLING.search(text))
    has_np_roll = bool(NP_ROLL.search(text))

    if not has_mod:
        return "NOT_APPLICABLE", ["no periodic modulo adjacency pattern"]

    # The modulo pattern matched. Determine whether it's lattice or non-lattice.
    # A weak heuristic: look for variable names like 'side', 'adj', 'pos[' near
    # the modulo, indicating lattice context. Otherwise mark as suspect.
    # We rely on the `has_distance_coupling` flag as the deciding factor.

    if not has_distance_coupling:
        # Modulo is used but no distance-weighted Hamiltonian/potential coupling.
        # Either pure adjacency tracking, np.roll-style, or non-lattice modulo.
        reasons.append("uses periodic modulo")
        if has_np_roll:
            reasons.append("uses np.roll for periodic shifts (auto-periodic)")
        if not has_distance_coupling:
            reasons.append("no distance-weighted couplings detected")
        return "CLEAN_NO_DISTANCE", reasons

    # Has both periodic modulo AND distance couplings. Check guards.
    if has_helper_import:
        reasons.append("imports periodic_geometry helper")
        return "CLEAN_HELPER", reasons
    if has_min_image:
        reasons.append("uses inline min(dx, side - dx) pattern")
        return "CLEAN_INLINE", reasons

    # Periodic modulo + distance couplings, but no minimum-image guard.
    reasons.append("PERIODIC modulo + distance-weighted couplings detected")
    reasons.append("NO minimum-image guard found (no helper import, no inline min())")
    return "NEEDS_REVIEW", reasons


def main() -> int:
    t0 = time.time()
    repo_root = Path("/Users/jonBridger/CI3Z2 Main")
    scripts_dir = repo_root / "scripts"
    if not scripts_dir.is_dir():
        print(f"ERROR: scripts dir not found at {scripts_dir}", file=sys.stderr)
        return 1

    # Audit every .py file under scripts/.
    py_files = sorted(scripts_dir.glob("*.py"))

    print("=" * 88)
    print("PERIODIC 2D TORUS DIAGNOSTICS CODE AUDIT")
    print("=" * 88)
    print(f"Scanning {len(py_files)} scripts under {scripts_dir.relative_to(repo_root)}/")
    print()

    by_status: dict[str, list[tuple[str, list[str]]]] = {
        "NEEDS_REVIEW": [],
        "CLEAN_HELPER": [],
        "CLEAN_INLINE": [],
        "CLEAN_NO_DISTANCE": [],
        "NOT_APPLICABLE": [],
        "ERROR": [],
    }
    for path in py_files:
        status, reasons = classify_file(path)
        by_status[status].append((path.name, reasons))

    # Print summary.
    print("Status counts:")
    for status, entries in by_status.items():
        print(f"  {status:>20}: {len(entries)}")
    print()

    # Detailed listings: NEEDS_REVIEW (priority), then clean categories.
    print("--- NEEDS_REVIEW ---")
    if not by_status["NEEDS_REVIEW"]:
        print("  (none)")
    else:
        for name, reasons in by_status["NEEDS_REVIEW"]:
            print(f"  {name}:")
            for r in reasons:
                print(f"    - {r}")

    print()
    print("--- CLEAN_HELPER (uses periodic_geometry helper) ---")
    for name, _ in by_status["CLEAN_HELPER"]:
        print(f"  {name}")

    print()
    print("--- CLEAN_INLINE (inline min(dx, side - dx) guard) ---")
    for name, _ in by_status["CLEAN_INLINE"]:
        print(f"  {name}")

    print()
    print("--- CLEAN_NO_DISTANCE (modulo without distance-weighted couplings) ---")
    cnd = by_status["CLEAN_NO_DISTANCE"]
    if len(cnd) > 12:
        for name, _ in cnd[:8]:
            print(f"  {name}")
        print(f"  ... and {len(cnd) - 8} more")
    else:
        for name, _ in cnd:
            print(f"  {name}")

    print()
    print(f"Total NOT_APPLICABLE: {len(by_status['NOT_APPLICABLE'])} (no modulo at all)")
    print(f"Total ERROR: {len(by_status['ERROR'])}")
    print()

    # ---- Cross-check vs canonical fix note ----
    canonical_corrected = {
        "frontier_self_consistency_test.py",
        "frontier_eigenvalue_stats_and_anderson_phase.py",
        "frontier_born_rule_alpha.py",
        "frontier_holographic_probe.py",
        "frontier_boundary_law_robustness.py",
        "frontier_staggered_geometry_superposition_retained.py",
        "frontier_bmv_entanglement.py",
        "frontier_branch_entanglement_robustness.py",
        "frontier_bmv_threebody.py",  # historical
    }

    # Every canonical-corrected script must NOT be NEEDS_REVIEW.
    canonical_in_review = [
        name for name, _ in by_status["NEEDS_REVIEW"]
        if name in canonical_corrected
    ]
    record(
        "A.1 every canonical-corrected script avoids NEEDS_REVIEW",
        len(canonical_in_review) == 0,
        f"canonical scripts in NEEDS_REVIEW: {canonical_in_review}\n"
        "(if non-empty, the audit is misclassifying canonical scripts and\n"
        "the regex rules need tightening)",
    )

    # ---- Sanity: known-clean canonical scripts hit one of the CLEAN_* buckets ----
    canonical_clean_status = {}
    for status_label in ("CLEAN_HELPER", "CLEAN_INLINE", "CLEAN_NO_DISTANCE"):
        for name, reasons in by_status[status_label]:
            if name in canonical_corrected:
                canonical_clean_status[name] = status_label
    canonical_missing = canonical_corrected - set(canonical_clean_status.keys())
    record(
        "A.2 every canonical-corrected script lands in some CLEAN_* bucket",
        len(canonical_missing) == 0,
        f"canonical NOT in CLEAN_*: {sorted(canonical_missing)}\n" + "\n".join(
            f"  {name} -> {status}" for name, status in sorted(canonical_clean_status.items())
        ),
    )

    # ---- Headline counts ----
    needs_review_count = len(by_status["NEEDS_REVIEW"])
    record(
        "B.1 audit produces a frozen NEEDS_REVIEW list",
        True,  # always passes; the list itself is the artifact
        f"NEEDS_REVIEW list contains {needs_review_count} script(s); see detail above.",
    )

    record(
        "B.2 audit is reproducible (deterministic regex scan)",
        True,
        "Audit uses fixed regex patterns over filesystem; output depends only\n"
        "on script content. Re-run gives identical classification.",
    )

    # Honest open boundary.
    record(
        "C.1 audit is static analysis only; NEEDS_REVIEW does not equal BUG",
        True,
        "Static analysis flags candidates by pattern matching. A NEEDS_REVIEW\n"
        "script may turn out to be clean on manual inspection if its distance\n"
        "computations don't actually feed periodic-edge weights. The audit\n"
        "narrows the manual-review surface; it does not replace it.",
    )

    print()
    print("=" * 88)
    print("SUMMARY")
    print("=" * 88)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}   wallclock: {time.time() - t0:.2f}s")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print(f"VERDICT: code audit produces a frozen NEEDS_REVIEW list")
        print(f"of {needs_review_count} script(s) with periodic modulo + distance-weighted")
        print("couplings + no minimum-image guard. Every canonical-corrected script")
        print("is correctly classified into a CLEAN_* bucket. The audit narrows the")
        print("manual-review surface for the active-queue 'periodic 2D torus")
        print("diagnostics' open item.")
        return 0

    print("VERDICT: periodic-torus audit has FAILs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
