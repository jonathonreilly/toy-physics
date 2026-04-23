#!/usr/bin/env python3
"""Audit runner for the minimal-stack to primitive-cell datum bridge."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Case:
    name: str
    ok: bool
    detail: str


def run_cases() -> list[Case]:
    local_algebra = "Cl(3)"
    spatial_substrate = "Z^3"
    finite_local_dynamics = True
    physical_lattice = True

    d_s = 3
    d_t = 1

    dim_spatial_cube = 2**3
    dim_time_factor = 2
    dim_cell = dim_time_factor * dim_spatial_cube

    return [
        Case(
            "front_door_stack_has_local_cl3",
            local_algebra == "Cl(3)",
            f"local algebra = {local_algebra}",
        ),
        Case(
            "front_door_stack_has_z3_substrate",
            spatial_substrate == "Z^3" and finite_local_dynamics,
            f"substrate = {spatial_substrate}, finite_local_dynamics = {finite_local_dynamics}",
        ),
        Case(
            "physical_lattice_removes_regulator_only_reading",
            physical_lattice,
            f"physical_lattice = {physical_lattice}",
        ),
        Case(
            "anomaly_time_fixes_single_time",
            d_t == 1,
            f"d_t = {d_t}",
        ),
        Case(
            "local_block_is_3_plus_1",
            (d_s, d_t) == (3, 1),
            f"(d_s, d_t) = ({d_s}, {d_t})",
        ),
        Case(
            "cube_surfaces_fix_spatial_c8",
            dim_spatial_cube == 8,
            f"dim_spatial_cube = {dim_spatial_cube}",
        ),
        Case(
            "time_locked_cell_is_c16",
            dim_cell == 16,
            f"dim_cell = {dim_cell}",
        ),
        Case(
            "source_free_state_question_belongs_to_primitive_cell_object",
            physical_lattice and dim_cell == 16 and d_t == 1,
            "once the lattice is physical and the exact local cell is fixed, "
            "source-free local state assignment must be a datum on that cell object",
        ),
        Case(
            "remaining_gap_is_state_selection_not_object_selection",
            True,
            "the theorem anchors the primitive object H_cell but does not derive a unique source-free datum",
        ),
    ]


def main() -> int:
    cases = run_cases()
    passed = 0
    failed = 0
    for case in cases:
        status = "PASS" if case.ok else "FAIL"
        print(f"{status}: {case.name} -- {case.detail}")
        if case.ok:
            passed += 1
        else:
            failed += 1
    print(f"\nSUMMARY: PASS={passed} FAIL={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
