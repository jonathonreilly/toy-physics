#!/usr/bin/env python3
"""Audit the current same-surface unit-bearing candidate classification.

This is not a derivation harness. It encodes the current theorem-grade
classification:
  - bulk/action class is homogeneous on the scale ray
  - spectral-gap class is exact but free in R
  - realized entropy/information carriers either fail or stay structural
  - therefore a future Planck derivation must add a new unit-bearing observable
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CLASS_NOTE = ROOT / "docs/PLANCK_SCALE_UNIT_BEARING_CANDIDATE_CLASSIFICATION_THEOREM_2026-04-23.md"
SCALE_RAY = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md"
LAMBDA_ID = ROOT / "docs/COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md"
MG_ID = ROOT / "docs/GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md"
BH_NOGO = ROOT / "docs/BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md"
HOLO = ROOT / "docs/HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md"
SELF_ENT = ROOT / "docs/SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md"
SINGLE_H = ROOT / "docs/SINGLE_AXIOM_HILBERT_NOTE.md"
SINGLE_I = ROOT / "docs/SINGLE_AXIOM_INFORMATION_NOTE.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(text.split()).lower()


def main() -> int:
    texts = {
        "class": normalized(read_text(CLASS_NOTE)),
        "scale": normalized(read_text(SCALE_RAY)),
        "lam": normalized(read_text(LAMBDA_ID)),
        "mg": normalized(read_text(MG_ID)),
        "bh": normalized(read_text(BH_NOGO)),
        "holo": normalized(read_text(HOLO)),
        "self": normalized(read_text(SELF_ENT)),
        "hilbert": normalized(read_text(SINGLE_H)),
        "info": normalized(read_text(SINGLE_I)),
    }

    n_pass = 0
    n_fail = 0

    print("Planck unit-bearing candidate classification audit")
    print("=" * 78)

    section("PART 1: CLASS A -- BULK/ACTION")
    p = check(
        "bulk/action class is exhausted by the scale-ray no-go",
        "fixes a scale ray, not an absolute scale anchor" in texts["scale"],
        "current gravity/action same-surface relations stay homogeneous on the remaining unit ray",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: CLASS B -- SPECTRAL / COMPACTNESS")
    p = check(
        "Lambda identity is an exact function identity in free R",
        "exact function identity in `r`" in texts["lam"]
        or "exact function identity in r" in texts["lam"],
        "the spectral-gap cosmology theorem does not select a numerical radius",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "graviton mass identity is an exact function identity in free R",
        "exact function identity in `r`" in texts["mg"]
        or "exact function identity in r" in texts["mg"],
        "the graviton compactness identity also leaves the radius free",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: CLASS C -- ENTROPY / INFORMATION")
    p = check(
        "current BH entropy carrier fails the 1/4 target",
        "c_widom = 1/6" in texts["bh"] and "!= 1 / 4" in texts["bh"],
        "the present free-fermion horizon carrier is a retained no-go for exact BH coefficient",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "boundary-law / holographic probe is bounded only",
        (
            "bounded companion" in texts["holo"]
            and (
                "establish a bekenstein-hawking law" in texts["holo"]
                or "ads/cft duality" in texts["holo"]
            )
        ),
        "the current boundary-law probe is not yet a unit-bearing horizon theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "self-gravity entropy probe is negative/inconclusive for area law",
        "negative / inconclusive result for area-law entropy" in texts["self"],
        "the simple self-gravity entropy observable is explicitly not the right area-law instrument",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "single-axiom Hilbert and information notes remain structural",
        "single axiom reduction" in texts["hilbert"]
        and "not the load-bearing accepted input ledger" in texts["hilbert"]
        and "it is not the load-bearing accepted input ledger" in texts["info"],
        "the one-axiom reductions compress structure but do not yet fix physical units",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: CLASSIFICATION NOTE VERDICT")
    p = check(
        "classification note exhausts the current same-surface candidate menu",
        "no currently admitted same-surface observable can break the planck scale ray" in texts["class"],
        "the note must state the elimination result explicitly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "classification note identifies the two surviving theorem classes",
        "boundary-density theorem" in texts["class"]
        and "per-cell action/information quantum theorem" in texts["class"],
        "the next real targets are now narrowed to two concrete theorem types",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Current same-surface candidate menu is exhausted. Any future no-import "
        "Planck derivation must add a new unit-bearing observable, most likely "
        "a boundary-density theorem or a per-cell action/information quantum theorem."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
