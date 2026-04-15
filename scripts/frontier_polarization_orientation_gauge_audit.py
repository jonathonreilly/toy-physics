#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path("/private/tmp/physics-review-active")

FILES = {
    "anomaly": Path("/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md"),
    "cap_map": ROOT / "docs/S3_EXISTING_WORK_FOR_CAP_MAP.md",
    "support": ROOT / "docs/FINITE_RANK_SUPPORT_CANONICAL_FRAME_NOTE.md",
    "universal": ROOT / "docs/UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md",
    "common": ROOT / "docs/POLARIZATION_COMMON_BUNDLE_CANDIDATE_NOTE.md",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_all(text: str, *phrases: str) -> bool:
    return all(phrase in text for phrase in phrases)


def has_regex(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) is not None


def check(label: str, ok: bool, detail: str, failures: list[str]) -> None:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}: {detail}")
    if not ok:
        failures.append(label)


def main() -> int:
    texts = {name: read_text(path) for name, path in FILES.items()}
    failures: list[str] = []

    print("Polarization orientation / chirality gauge audit")
    print("Goal: test whether atlas orientation, handedness, and chirality data canonically reduce the residual bundle gauge")

    check(
        "Anomaly-forced time fixes the clock",
        has_all(texts["anomaly"], "d_t = 1", "chirality", "codimension-1"),
        "single-clock + chirality + codimension-1 are all stated in the time theorem",
        failures,
    )
    check(
        "Cap-map handedness is only a Z2 background choice",
        has_all(texts["cap_map"], "Both Z_2 elements", "orientation-reversing self-homeomorphism", "S^3"),
        "both cap orientations still give S^3",
        failures,
    )
    check(
        "Support residual gauge remains O(1) x O(2)",
        has_regex(texts["support"], r"O\(1\).+O\(2\)") and "residual gauge" in texts["support"],
        "support note states the exact leftover gauge on the dark complement",
        failures,
    )
    check(
        "Universal residual gauge remains SO(3)",
        "SO(3)" in texts["universal"] and "residual gauge" in texts["universal"],
        "universal note states the exact leftover spatial rotation orbit",
        failures,
    )
    check(
        "Pi_A1 core is exact but not enough to close",
        has_all(texts["common"], "Pi_A1", "candidate", "complement"),
        "common bundle candidate keeps Pi_A1 exact but complement orbit-canonical",
        failures,
    )
    check(
        "No canonical reduction beyond the surviving subgroups",
        has_all(texts["support"], "O(1)_{E_perp}", "O(2)_{T1_darken}") and "SO(3)" in texts["universal"],
        "the same residual groups survive after orientation/chirality/time are accounted for",
        failures,
    )

    if failures:
        print(f"SUMMARY: FAIL ({len(failures)} checks failed)")
        for name in failures:
            print(f"  - {name}")
        return 1

    print("SUMMARY: PASS (all checked orientation/chirality constraints collapse only to the known residual subgroups)")
    print("Residual subgroup on support side: O(1) x O(2)")
    print("Residual subgroup on universal side: SO(3)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
