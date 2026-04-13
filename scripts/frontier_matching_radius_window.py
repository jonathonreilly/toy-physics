#!/usr/bin/env python3
"""Bounded matching-radius window for strong-field coarse-graining.

Purpose:
  Using the coarse-grained exterior law from the exact lattice field, identify
  the smallest matching radius R_match where the radial harmonic exterior law
  becomes vacuum-close across multiple exact source families.

This does not prove the matching theorem. It isolates a concrete finite
matching window that the eventual theorem must explain.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name, ok, detail, status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


cg = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()


def matching_rows(phi_grid):
    rows = []
    for r_match in [3.0, 3.5, 4.0, 4.5, 5.0]:
        a, rel_rms, max_rel = cg.fit_radial_harmonic_projection(phi_grid, r_match)
        direct_res, coarse_res = cg.residual_at_radius(phi_grid, r_match, a)
        rows.append((r_match, rel_rms, max_rel, direct_res, coarse_res, direct_res / coarse_res))
    return rows


def first_window(rows, coarse_thresh: float, improve_thresh: float):
    for row in rows:
        r_match, rel_rms, max_rel, direct_res, coarse_res, improve = row
        if coarse_res < coarse_thresh and improve > improve_thresh:
            return row
    return None


def main() -> None:
    print("Strong-field matching-radius window")
    print("=" * 72)

    phi_oh = cg.same_source.build_best_phi_grid()
    rows_oh = matching_rows(phi_oh)
    phi_fr = cg.build_finite_rank_phi_grid()
    rows_fr = matching_rows(phi_fr)

    print("\nExact local O_h family:")
    for row in rows_oh:
        print(
            f"  R={row[0]:.1f}  shell_rms={row[1]:.3f}  shell_max_rel={row[2]:.3f}  "
            f"direct={row[3]:.3e}  coarse={row[4]:.3e}  improve={row[5]:.1f}x"
        )

    print("\nExact finite-rank family:")
    for row in rows_fr:
        print(
            f"  R={row[0]:.1f}  shell_rms={row[1]:.3f}  shell_max_rel={row[2]:.3f}  "
            f"direct={row[3]:.3e}  coarse={row[4]:.3e}  improve={row[5]:.1f}x"
        )

    w_oh = first_window(rows_oh, coarse_thresh=1e-5, improve_thresh=100.0)
    w_fr = first_window(rows_fr, coarse_thresh=2e-5, improve_thresh=100.0)

    record(
        "a finite matching window emerges for the exact local O_h source family",
        w_oh is not None,
        (
            f"first window at R_match={w_oh[0]:.1f} with coarse={w_oh[4]:.3e}, "
            f"improvement={w_oh[5]:.1f}x"
            if w_oh is not None
            else "no admissible window found"
        ),
    )
    record(
        "a finite matching window emerges for the broader exact finite-rank family",
        w_fr is not None,
        (
            f"first window at R_match={w_fr[0]:.1f} with coarse={w_fr[4]:.3e}, "
            f"improvement={w_fr[5]:.1f}x"
            if w_fr is not None
            else "no admissible window found"
        ),
    )
    record(
        "the matching window is shared within the same narrow radial band",
        w_oh is not None and w_fr is not None and abs(w_oh[0] - w_fr[0]) <= 0.5,
        (
            f"O_h window={w_oh[0]:.1f}, finite-rank window={w_fr[0]:.1f}"
            if w_oh is not None and w_fr is not None
            else "window comparison unavailable"
        ),
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
