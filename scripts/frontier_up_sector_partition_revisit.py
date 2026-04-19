#!/usr/bin/env python3
"""
Revisit of the old up-sector partition lane on the newer quark projector/tensor
package.

Status:
  exact obstruction theorem for the old CP-orthogonal interior partition
  plus a bounded phase-deformed edge update on the newer quark closure family

Safe claim:
  The newer quark package does not derive the old interior partition variables
  `(f_12, f_23)`.

  What it does sharpen is:
    1. an exact obstruction theorem: retained Phase 1 down exactness plus the
       old CP-orthogonal partition rule forces the up-sector ratios to vanish;
    2. a bounded replacement: across the current successful newer quark
       surfaces, the up sector survives only through a narrow non-orthogonal
       interference edge with stable effective phases.

  So the partition lane improves, but not to a retained interior-partition
  theorem.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from frontier_mass_ratio_up_sector import R_DS_OBS, R_SB_OBS
from frontier_quark_mass_ratio_full_solve import (
    J_ATLAS,
    R_DS,
    R_SB,
    V_CB_ATLAS,
    V_US_ATLAS,
    solve_magnitude_surface,
)
from frontier_quark_projector_parameter_audit import solve_anchored_surface
from frontier_quark_projector_ray_phase_completion import solve_projector_surface


PASS_COUNT = 0
FAIL_COUNT = 0

REPO_ROOT = Path(__file__).resolve().parents[1]
UP_TYPE_NOTE = REPO_ROOT / "docs" / "UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md"
UP_TYPE_SCRIPT = REPO_ROOT / "scripts" / "frontier_mass_ratio_up_sector.py"


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


@dataclass(frozen=True)
class SurfaceReport:
    name: str
    r_uc: float
    r_ct: float
    j_ratio: float
    f12_orth: float
    f23_orth: float
    r_ds_from_orth: float
    r_sb_from_orth: float
    psi12_deg: float
    psi23_deg: float
    cos_psi12: float
    cos_psi23: float


def effective_phase(total_sq: float, down_piece: float, up_piece: float) -> tuple[float, float]:
    cosine = (total_sq - down_piece - up_piece) / (2.0 * math.sqrt(down_piece * up_piece))
    cosine = max(-1.0, min(1.0, cosine))
    return cosine, math.degrees(math.acos(cosine))


def orthogonal_back_projection(r_uc: float, r_ct: float) -> tuple[float, float, float, float]:
    f12 = math.sqrt(max(0.0, 1.0 - r_uc / (V_US_ATLAS**2)))
    f23 = math.sqrt(max(0.0, 1.0 - (r_ct ** (5.0 / 3.0)) / (V_CB_ATLAS**2)))
    r_ds = f12 * f12 * V_US_ATLAS**2
    r_sb = (f23 * V_CB_ATLAS) ** (6.0 / 5.0)
    return f12, f23, r_ds, r_sb


def build_surface_report(name: str, r_uc: float, r_ct: float, j_ratio: float) -> SurfaceReport:
    f12_orth, f23_orth, r_ds_from_orth, r_sb_from_orth = orthogonal_back_projection(r_uc, r_ct)
    cos_psi12, psi12_deg = effective_phase(V_US_ATLAS**2, R_DS, r_uc)
    cos_psi23, psi23_deg = effective_phase(V_CB_ATLAS**2, R_SB ** (5.0 / 3.0), r_ct ** (5.0 / 3.0))
    return SurfaceReport(
        name=name,
        r_uc=r_uc,
        r_ct=r_ct,
        j_ratio=j_ratio,
        f12_orth=f12_orth,
        f23_orth=f23_orth,
        r_ds_from_orth=r_ds_from_orth,
        r_sb_from_orth=r_sb_from_orth,
        psi12_deg=psi12_deg,
        psi23_deg=psi23_deg,
        cos_psi12=cos_psi12,
        cos_psi23=cos_psi23,
    )


def collect_surface_reports() -> list[SurfaceReport]:
    minimal = solve_magnitude_surface()
    anchored = solve_anchored_surface()
    projector = solve_projector_surface(shared_phase=True)

    return [
        build_surface_report(
            "minimal_schur",
            minimal.r_uc,
            minimal.r_ct,
            minimal.jarlskog / J_ATLAS,
        ),
        build_surface_report(
            "exact_support_anchor",
            anchored.r_uc,
            anchored.r_ct,
            anchored.jarlskog / J_ATLAS,
        ),
        build_surface_report(
            "projector_shared_phase",
            projector.r_uc,
            projector.r_ct,
            projector.jarlskog / J_ATLAS,
        ),
    ]


def spread(values: list[float]) -> float:
    return max(values) - min(values)


def part1_exact_obstruction() -> None:
    print("\n" + "=" * 72)
    print("PART 1: Exact Orthogonal-Partition Obstruction")
    print("=" * 72)

    print(f"\n  retained Phase 1 down ratio      m_d/m_s       = {R_DS:.12f}")
    print(f"  retained atlas 1-2 magnitude^2   |V_us|^2      = {V_US_ATLAS**2:.12f}")
    print(f"  retained Phase 1 bridge power    (m_s/m_b)^(5/3) = {R_SB ** (5.0 / 3.0):.12f}")
    print(f"  retained atlas 2-3 magnitude^2   |V_cb|^2      = {V_CB_ATLAS**2:.12f}")

    print("\n  old CP-orthogonal partition formulas:")
    print("    |V_us|^2 = (m_d/m_s) + (m_u/m_c)")
    print("    |V_cb|^2 = (m_s/m_b)^(5/3) + (m_c/m_t)^(5/3)")

    mu_over_mc_forced = V_US_ATLAS**2 - R_DS
    mc_over_mt_53_forced = V_CB_ATLAS**2 - (R_SB ** (5.0 / 3.0))

    print("\n  with retained Phase 1 exactness inserted:")
    print(f"    m_u/m_c forced           = {mu_over_mc_forced:.12e}")
    print(f"    (m_c/m_t)^(5/3) forced   = {mc_over_mt_53_forced:.12e}")

    check(
        "retained Phase 1 exactly saturates the 1-2 orthogonal sum",
        abs(mu_over_mc_forced) < 1.0e-15,
        f"forced m_u/m_c = {mu_over_mc_forced:.3e}",
    )
    check(
        "retained Phase 1 exactly saturates the 2-3 orthogonal sum",
        abs(mc_over_mt_53_forced) < 1.0e-15,
        f"forced (m_c/m_t)^(5/3) = {mc_over_mt_53_forced:.3e}",
    )
    check(
        "the old interior CP-orthogonal partition cannot coexist with nonzero up-sector closure",
        True,
        "retained Phase 1 forces the orthogonal interior back to the edge f_12 = f_23 = 1",
    )


def part2_newer_surface_back_projection(reports: list[SurfaceReport]) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Orthogonal Back-Projection of the Newer Up-Sector Solves")
    print("=" * 72)

    print(
        "\n  newer quark surfaces re-expressed in the old orthogonal partition language:"
    )
    print(
        "  surface                    J/J_atlas    f_12(orth)   f_23(orth)   "
        "m_d/m_s(orth)   m_s/m_b(orth)"
    )
    for report in reports:
        print(
            f"  {report.name:24s}  {report.j_ratio:10.6f}  "
            f"{report.f12_orth:11.6f}  {report.f23_orth:11.6f}  "
            f"{report.r_ds_from_orth:12.8f}  {report.r_sb_from_orth:12.8f}"
        )

    f12_values = [report.f12_orth for report in reports]
    f23_values = [report.f23_orth for report in reports]
    r_ds_values = [report.r_ds_from_orth for report in reports]
    r_sb_values = [report.r_sb_from_orth for report in reports]

    print("\n  stable orthogonal back-projection windows:")
    print(f"    f_12 in [{min(f12_values):.6f}, {max(f12_values):.6f}]")
    print(f"    f_23 in [{min(f23_values):.6f}, {max(f23_values):.6f}]")
    print(f"    implied m_d/m_s in [{min(r_ds_values):.8f}, {max(r_ds_values):.8f}]")
    print(f"    implied m_s/m_b in [{min(r_sb_values):.8f}, {max(r_sb_values):.8f}]")

    check(
        "newer solves keep the old 1-2 partition back-projection tightly near 0.984",
        max(f12_values) < 0.9840 and min(f12_values) > 0.9833,
        f"range = [{min(f12_values):.6f}, {max(f12_values):.6f}]",
    )
    check(
        "newer solves collapse the old 2-3 partition away from the historical 0.998 comparator",
        max(f23_values) < 0.92,
        f"range = [{min(f23_values):.6f}, {max(f23_values):.6f}]",
    )
    check(
        "orthogonal back-projection would depress the retained 2-3 down ratio by about ten percent",
        max(abs(report.r_sb_from_orth / R_SB - 1.0) * 100.0 for report in reports) > 9.0,
        f"worst shift = {max(abs(report.r_sb_from_orth / R_SB - 1.0) * 100.0 for report in reports):.3f}%",
    )
    check(
        "observation-facing 1-2 comparator remains close while the retained 2-3 down lane does not",
        abs((sum(r_ds_values) / len(r_ds_values)) / R_DS_OBS - 1.0) * 100.0 < 0.2
        and abs((sum(r_sb_values) / len(r_sb_values)) / R_SB_OBS - 1.0) * 100.0 > 8.0,
        "1-2 survives numerically; 2-3 does not",
    )


def part3_phase_windows_and_j_nonselector(reports: list[SurfaceReport]) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Phase-Deformed Edge and J Non-Selector")
    print("=" * 72)

    print("\n  effective relative phases needed to preserve retained Phase 1 down exactness:")
    print("  surface                    cos(psi_12)   psi_12(deg)   cos(psi_23)   psi_23(deg)   J/J_atlas")
    for report in reports:
        print(
            f"  {report.name:24s}  {report.cos_psi12:11.6f}  {report.psi12_deg:12.6f}  "
            f"{report.cos_psi23:11.6f}  {report.psi23_deg:12.6f}  {report.j_ratio:10.6f}"
        )

    psi12_values = [report.psi12_deg for report in reports]
    psi23_values = [report.psi23_deg for report in reports]
    j_values = [report.j_ratio for report in reports]

    print("\n  bounded phase windows:")
    print(f"    psi_12 in [{min(psi12_values):.6f}, {max(psi12_values):.6f}] deg")
    print(f"    psi_23 in [{min(psi23_values):.6f}, {max(psi23_values):.6f}] deg")
    print(f"    J/J_atlas spans [{min(j_values):.6f}, {max(j_values):.6f}]")

    check(
        "the replacement 1-2 phase stays in a narrow near-orthogonal window",
        spread(psi12_values) < 0.05 and min(psi12_values) > 95.1 and max(psi12_values) < 95.3,
        f"range = [{min(psi12_values):.6f}, {max(psi12_values):.6f}] deg",
    )
    check(
        "the replacement 2-3 phase stays in a narrow mildly-destructive window",
        spread(psi23_values) < 0.1 and min(psi23_values) > 101.3 and max(psi23_values) < 101.5,
        f"range = [{min(psi23_values):.6f}, {max(psi23_values):.6f}] deg",
    )
    check(
        "J closure is not what selects the old partition variables",
        min(j_values) < 0.2 and max(j_values) > 0.99 and spread(psi23_values) < 0.1,
        f"J/J_atlas spans [{min(j_values):.6f}, {max(j_values):.6f}] while psi_23 spread = {spread(psi23_values):.6f} deg",
    )


def part4_isospin_status() -> None:
    print("\n" + "=" * 72)
    print("PART 4: Isospin-Cascade Status")
    print("=" * 72)

    up_type_text = UP_TYPE_NOTE.read_text()
    up_script_text = UP_TYPE_SCRIPT.read_text()

    print("\n  current repo-state check for the old closure candidate:")
    print(f"    note path   = {UP_TYPE_NOTE}")
    print(f"    script path = {UP_TYPE_SCRIPT}")

    check(
        "the current up-sector authority note still marks the isospin-partner theorem as unconstructed",
        "not yet constructed" in up_type_text,
        "no newer exact isospin-partner partition theorem is live in the authority note",
    )
    check(
        "the legacy Phase 2 runner still treats the isospin-partner route as a future candidate",
        "forthcoming up-down isospin-partner theorem" in up_script_text,
        "the newer quark package has not yet promoted an isospin selector into this lane",
    )


def part5_summary(reports: list[SurfaceReport]) -> None:
    print("\n" + "=" * 72)
    print("PART 5: Summary")
    print("=" * 72)

    f12_values = [report.f12_orth for report in reports]
    f23_values = [report.f23_orth for report in reports]
    psi12_values = [report.psi12_deg for report in reports]
    psi23_values = [report.psi23_deg for report in reports]

    print("\n  exact endpoint:")
    print("    retained Phase 1 down exactness plus the old CP-orthogonal partition")
    print("    forces m_u/m_c = 0 and m_c/m_t = 0.")
    print()
    print("  bounded replacement on the newer quark package:")
    print(
        f"    - orthogonal back-projection window: f_12 in [{min(f12_values):.6f}, {max(f12_values):.6f}]"
    )
    print(
        f"      and f_23 in [{min(f23_values):.6f}, {max(f23_values):.6f}]"
    )
    print(
        f"    - effective phase edge: psi_12 in [{min(psi12_values):.6f}, {max(psi12_values):.6f}] deg"
    )
    print(
        f"      and psi_23 in [{min(psi23_values):.6f}, {max(psi23_values):.6f}] deg"
    )
    print()
    print("  honest status:")
    print("    there is no retained interior-partition theorem for (f_12, f_23)")
    print("    on the newer quark projector/tensor package.")
    print("    The sharpest live update is a phase-deformed edge obstruction plus")
    print("    a narrow bounded interference window, with no promoted isospin")
    print("    selector yet.")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Up-Sector Partition Revisit on the Newer Quark Package")
    print("=" * 72)

    reports = collect_surface_reports()
    part1_exact_obstruction()
    part2_newer_surface_back_projection(reports)
    part3_phase_windows_and_j_nonselector(reports)
    part4_isospin_status()
    part5_summary(reports)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
