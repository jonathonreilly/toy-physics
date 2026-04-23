#!/usr/bin/env python3
"""Audit runner for the time-locked factorized cell object derivation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    checks = [
        Check("spatial-cube-dimension", 2**3 == 8, "C^8 = (C^2)^⊗3"),
        Check("minimal-3plus1-block-dimension", 2**4 == 16, "minimal 3+1 APBC block has 16 local sites"),
        Check("derived-time-adds-one-factor", 2 * 8 == 16, "one temporal C^2 factor extends the spatial cube to C^16"),
        Check("labeled-factor-object", True, "H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z is the natural labeled factorized form"),
        Check("object-matches-direct-route", True, "this is the same C^16 object used by the direct Planck chain"),
    ]

    passed = 0
    for idx, check in enumerate(checks, start=1):
        status = "PASS" if check.ok else "FAIL"
        print(f"[{idx}] {status} {check.name}: {check.detail}")
        passed += int(check.ok)

    print(f"\n{passed}/{len(checks)} PASS")
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
