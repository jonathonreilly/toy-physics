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
        "name": "Mirror chokepoint / Z2-protected transfer",
        "status": "retained",
        "joint": "Retained bounded pocket: Born-clean through N=60 on strict NPL_HALF=50; strongest row N=40, pur_cl 0.8764±0.03, gravity +4.6161±0.721",
        "born": "Corrected Born stays machine-clean on the retained chokepoint pocket",
        "why": "Strongest symmetry-protected challenger: stronger gravity than the dense central-band row, weaker decoherence and shorter range, but now artifact-backed through N=60",
    },
    {
        "name": "Generated asymmetry-persistence + layer norm",
        "status": "retained",
        "joint": "Best gravity-side retained row: N=100, thr=0.20, Born 2.31e-16, pur_cl 0.921±0.043, gravity +2.102±0.825",
        "born": "Corrected Born stays machine-clean on the dense probe",
        "why": "Best gravity side alone: stronger direct gravity pocket and cleaner mass-window fit, but less balanced jointly",
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
    print("2. Best symmetry-protected bounded challenger: Mirror chokepoint / Z2-protected transfer")
    print("3. Best gravity side alone: Generated asymmetry-persistence + layer norm")
    print()
    print("Review-safe bottom line:")
    print(
        "Hard geometry remains the shared enabler. Dense central-band is the strongest "
        "retained joint lane, mirror chokepoint is the strongest symmetry-protected "
        "bounded challenger through N=60, and generated asymmetry is the strongest "
        "retained gravity-side-alone lane."
    )


if __name__ == "__main__":
    main()
