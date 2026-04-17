#!/usr/bin/env python3
"""Frozen symmetry head-to-head: exact mirror chokepoint vs Z2 x Z2.

This script does not recompute the retained artifact chains. It freezes an
apples-to-apples comparison using the already-retained notes on main.

Shared metrics used for the ranking:
  - Born |I3|/P
  - detector-side d_TV
  - purity / decoherence
  - gravity centroid shift
  - retained range

Mirror-specific MI from the canonical chokepoint MI note is reported as a
supplement, but it is not directly compared to Z2 x Z2 because the latter
does not yet have a canonical MI artifact chain.
"""

from __future__ import annotations

MIRROR = {
    "name": "Exact mirror chokepoint",
    "rows": {
        80: {
            "dtv": 0.4291,
            "pur": 0.8182,
            "grav": 3.0551,
            "born": 2.43e-15,
            "k0": 0.0,
        },
        100: {
            "dtv": 0.2308,
            "pur": 0.9043,
            "grav": 1.3089,
            "born": 1.13e-15,
            "k0": 0.0,
        },
    },
    "range": "retained through N=100; N=120 loses gravity",
    "supplement": (
        "Mirror-specific MI is bounded and mid-N positive over the matched "
        "random baseline, but not a clean asymptotic law."
    ),
}

Z2Z2 = {
    "name": "Z2 x Z2",
    "rows": {
        80: {
            "dtv": 0.525,
            "pur": 0.785,
            "grav": 2.677,
            "born": 1.55e-15,
            "k0": 0.0,
        },
        100: {
            "dtv": 0.567,
            "pur": 0.742,
            "grav": 0.763,
            "born": 1.94e-15,
            "k0": 0.0,
        },
        120: {
            "dtv": 0.393,
            "pur": 0.764,
            "grav": 0.245,
            "born": 3.04e-15,
            "k0": 0.0,
        },
    },
    "range": "retained through N=120 on the dense extension; positive gravity but no clean gravity law",
}


def _fmt(x: float, digits: int = 4) -> str:
    return f"{x:.{digits}f}"


def main() -> None:
    print("SYMMETRY HEAD-TO-HEAD")
    print("=" * 96)
    print("Shared metrics on the retained lanes")
    print()
    print(
        f"{'N':>4s}  {'lane':>24s}  {'d_TV':>8s}  {'pur':>8s}  {'gravity':>10s}  "
        f"{'Born':>11s}  {'k=0':>8s}"
    )
    print("-" * 96)
    for n in (80, 100):
        m = MIRROR["rows"][n]
        z = Z2Z2["rows"][n]
        print(
            f"{n:4d}  {MIRROR['name'][:24]:>24s}  {_fmt(m['dtv']):>8s}  {_fmt(m['pur']):>8s}  "
            f"{m['grav']:+10.4f}  {m['born']:.2e}  {m['k0']:8.2e}"
        )
        print(
            f"{'':4s}  {Z2Z2['name'][:24]:>24s}  {_fmt(z['dtv']):>8s}  {_fmt(z['pur']):>8s}  "
            f"{z['grav']:+10.4f}  {z['born']:.2e}  {z['k0']:8.2e}"
        )
        print()

    print("Range")
    print(f"- {MIRROR['name']}: {MIRROR['range']}")
    print(f"- {Z2Z2['name']}: {Z2Z2['range']}")
    print()
    print("Supplement")
    print(f"- {MIRROR['name']} MI: {MIRROR['supplement']}")
    print()
    print("Read")
    print("- Exact mirror is the stronger gravity-weighted joint lane at the shared N=80/100 rows.")
    print("- Z2 x Z2 is the stronger decoherence-side lane and has the longer retained range.")
    print("- Both lanes remain Born-clean at machine precision on their retained harnesses.")


if __name__ == "__main__":
    main()
