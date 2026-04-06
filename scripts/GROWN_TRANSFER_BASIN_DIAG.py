#!/usr/bin/env python3
"""One-row diagnostic for the retained grown-row basin.

This is a follow-up to the narrow basin sweep and is intentionally tiny.
It checks a single nearby grown row that was missing from the first compact
read, so we can tell whether the retained grown-row positives are a small
basin or just a one-point ridge.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.GROWN_TRANSFER_BASIN_SWEEP import _score_row


DRIFT = 0.20
RESTORE = 0.60


def main() -> None:
    row = _score_row(DRIFT, RESTORE)
    print("=" * 86)
    print("GROWN TRANSFER BASIN DIAG")
    print(f"  drift={DRIFT:.2f}, restore={RESTORE:.2f}")
    print("=" * 86)
    print(
        f"zero={row.signed_zero:+.3e} neutral={row.signed_neutral:+.3e} "
        f"plus={row.signed_single:+.3e} exp={row.signed_exponent:.3f}"
    )
    print(
        f"gamma0={row.action_gamma0:+.3e} F0={row.action_fm0:.3f} "
        f"F05={row.action_fm05:.3f} toward={row.action_toward}"
    )
    signed_ok = (
        abs(row.signed_zero) < 1e-12
        and abs(row.signed_neutral) < 1e-12
        and row.signed_single != 0.0
        and abs(row.signed_exponent - 1.0) < 0.05
    )
    complex_ok = (
        row.action_toward[0] > 0
        and row.action_toward[1] == 0
        and row.action_fm0 > 0.99
        and row.action_fm05 > 0.99
    )
    print()
    print("SAFE READ")
    print(f"  signed-source ok: {signed_ok}")
    print(f"  complex-action ok: {complex_ok}")
    if signed_ok and complex_ok:
        print("  this nearby row stays inside the retained grown-row basin")
    else:
        print("  this nearby row falls outside the retained grown-row basin")


if __name__ == "__main__":
    main()
