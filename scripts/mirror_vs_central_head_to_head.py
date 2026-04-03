#!/usr/bin/env python3
"""Frozen head-to-head comparison: mirror chokepoint vs dense central-band.

This is a review-safe comparison layer. It does not recompute the retained
artifact chain; it freezes the current ranking using the already-retained
mirror and central-band notes.

Fairness note: the two lanes report different purity scalars (`pur_min` versus
`pur_cl`), so the comparison should be read lane-by-lane, using the full bundle
of Born, purity, gravity, and retained range rather than purity alone.
"""

from __future__ import annotations


LANES = [
    {
        "name": "Dense central-band + layer norm",
        "status": "retained",
        "joint": "Best retained high-N row: N=80, npl=80, Born-clean, pur_min=0.500, gravity +2.799±1.612",
        "purity": "pur_min",
        "born": "Corrected Born stays at machine precision on the retained dense pocket",
        "range": "retained through N=100 in a narrow density window, but thins by N=100",
        "why": "Best joint coexistence: stronger decoherence and wider retained range than mirror",
    },
    {
        "name": "Mirror chokepoint / Z2-protected transfer",
        "status": "retained bounded pocket",
        "joint": "Best retained mirror row: N=40, NPL_HALF=50, Born 1.01e-15, pur_cl=0.8764±0.03, gravity +4.6161±0.721",
        "purity": "pur_cl",
        "born": "Corrected Born stays at machine precision through N=60 on the strict pocket",
        "range": "retained through N=60, fails at N=80/100 on the strict pocket",
        "why": "Strongest small-N gravity and symmetry protection, but not the best joint lane overall",
    },
]


def main() -> None:
    print("MIRROR VS CENTRAL HEAD-TO-HEAD")
    print("=" * 92)
    for i, lane in enumerate(LANES, 1):
        print(f"{i}. {lane['name']} [{lane['status']}]")
        print(f"   Born: {lane['born']}")
        print(f"   Purity metric: {lane['purity']}")
        print(f"   Retained row: {lane['joint']}")
        print(f"   Range: {lane['range']}")
        print(f"   Why: {lane['why']}")
        print()

    print("Ranking")
    print("1. Best joint coexistence: Dense central-band + layer norm")
    print("2. Highest-upside but bounded challenger: Mirror chokepoint / Z2-protected transfer")
    print()
    print("Review-safe bottom line:")
    print(
        "Mirror is now a real retained bounded pocket with stronger small-N gravity, "
        "but the dense central-band lane still wins on joint coexistence and retained "
        "range. Mirror is the challenger, not the new best joint lane."
    )


if __name__ == "__main__":
    main()
