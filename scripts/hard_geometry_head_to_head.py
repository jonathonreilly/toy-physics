#!/usr/bin/env python3
"""Head-to-head summary for the retained hard-geometry lanes.

This is a review-safe comparison layer. It does not recompute the retained
artifact chain; it freezes the current ranking using the already-retained
joint-card / gravity-window / Born-calibration notes.
"""

from __future__ import annotations


LANES = [
    {
        "name": "Dense central-band + layer norm",
        "status": "retained",
        "joint": "Best retained same-graph joint row: N=80, npl=80, Born-clean, pur_min=0.500, gravity +2.799±1.612",
        "born": "Corrected Born stays at machine precision on the retained dense pocket",
        "why": "Best joint coexistence: strongest same-graph balance of Born, decoherence, and positive gravity",
    },
    {
        "name": "Generated asymmetry-persistence + layer norm",
        "status": "retained",
        "joint": "Best gravity-side retained row: N=100, thr=0.20, Born 2.31e-16, pur_cl 0.921±0.043, gravity +2.102±0.825",
        "born": "Corrected Born stays machine-clean on the dense probe",
        "why": "Best gravity side alone: stronger direct gravity pocket and cleaner mass-window fit, but less balanced jointly",
    },
    {
        "name": "Mirror chokepoint / Z2-protected transfer",
        "status": "provisional",
        "joint": "Artifact-backed at small N: Born-clean at N=15/25 with gravity +1.293 to +2.275 and pur_cl 0.577 to 0.733, but FAILS by N=40+",
        "born": "Corrected Born passes at machine precision in the tested chokepoint range",
        "why": "Highest-upside but provisional: the symmetry-protection idea is real and artifact-backed, but its scalability is not good enough to outrank the retained lanes",
    },
]


def main() -> None:
    print("HARD-GEOMETRY HEAD-TO-HEAD")
    print("=" * 88)
    for i, lane in enumerate(LANES, 1):
        print(f"{i}. {lane['name']} [{lane['status']}]")
        print(f"   {lane['why']}")
        print(f"   Born: {lane['born']}")
        print(f"   Retained row: {lane['joint']}")
        print()

    print("Ranking")
    print("1. Best joint coexistence: Dense central-band + layer norm")
    print("2. Best gravity side alone: Generated asymmetry-persistence + layer norm")
    print("3. Highest-upside but provisional: Mirror chokepoint / Z2-protected transfer")
    print()
    print("Review-safe bottom line:")
    print(
        "Hard geometry remains the shared enabler. Dense central-band is the strongest "
        "retained joint lane, generated asymmetry is the strongest retained gravity-side "
        "lane, and mirror chokepoint is now artifact-backed but still too small-N to "
        "outrank the retained lanes."
    )


if __name__ == "__main__":
    main()
