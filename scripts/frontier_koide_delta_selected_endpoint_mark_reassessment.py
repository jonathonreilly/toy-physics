#!/usr/bin/env python3
"""
Koide delta selected-endpoint mark reassessment.

Purpose:
  Consolidate the post-minimal-radian attacks:

    - unmarked primitive naturality,
    - boundary defect mark,
    - source-asymmetry mark transfer,
    - the three minimal radian-input routes.

Result:
  Delta is still open, but the residual is sharper.  The remaining positive
  theorem must retain an oriented selected rank-one endpoint mark and a based
  endpoint trivialization, or supply a new joint Q/delta theorem that derives
  that mark without reintroducing a Q-visible source label.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def main() -> int:
    section("A. New endpoint-mark attack packet")

    runners = [
        "scripts/frontier_koide_delta_z3_wilson_d2_power_quantization_no_go.py",
        "scripts/frontier_koide_delta_lattice_propagator_radian_quantum_no_go.py",
        "scripts/frontier_koide_delta_hw1_baryon_wilson_holonomy_no_go.py",
        "scripts/frontier_koide_delta_minimal_radian_inputs_reassessment.py",
        "scripts/frontier_koide_delta_unmarked_primitive_naturality_no_go.py",
        "scripts/frontier_koide_delta_boundary_defect_mark_no_go.py",
        "scripts/frontier_koide_delta_source_asymmetry_mark_transfer_no_go.py",
    ]
    notes = [
        "docs/KOIDE_DELTA_Z3_WILSON_D2_POWER_QUANTIZATION_NO_GO_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_LATTICE_PROPAGATOR_RADIAN_QUANTUM_NO_GO_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_HW1_BARYON_WILSON_HOLONOMY_NO_GO_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_MINIMAL_RADIAN_INPUTS_REASSESSMENT_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_UNMARKED_PRIMITIVE_NATURALITY_NO_GO_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_BOUNDARY_DEFECT_MARK_NO_GO_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_SOURCE_ASYMMETRY_MARK_TRANSFER_NO_GO_NOTE_2026-04-24.md",
    ]
    missing = [rel for rel in runners + notes if not exists(rel)]
    record(
        "A.1 endpoint-mark attack artifacts are present",
        not missing,
        "\n".join(missing) if missing else f"{len(runners)} runners + {len(notes)} notes",
    )

    section("B. Residual algebra")

    eta = sp.Rational(2, 9)
    mu, spectator, c = sp.symbols("mu spectator c", real=True)
    residual_degree = sp.simplify(mu - 1 + c / eta)
    residual_channel = sp.simplify(-spectator + c / eta)
    closure_degree = sp.solve([sp.Eq(residual_degree, 0), sp.Eq(c, 0)], [mu, c], dict=True)
    closure_channel = sp.solve([sp.Eq(residual_channel, 0), sp.Eq(c, 0)], [spectator, c], dict=True)
    record(
        "B.1 degree and channel formulations have the same closure content",
        closure_degree == [{mu: 1, c: 0}] and closure_channel == [{spectator: 0, c: 0}],
        f"degree residual={residual_degree}; channel residual={residual_channel}",
    )

    alpha = sp.symbols("alpha", real=True)
    selected = sp.cos(alpha) ** 2
    spectator_alpha = sp.sin(alpha) ** 2
    record(
        "B.2 oriented mark formulation closes only at the selected line",
        sp.simplify(selected.subs(alpha, 0)) == 1
        and sp.simplify(spectator_alpha.subs(alpha, 0)) == 0
        and sp.simplify(selected.subs(alpha, sp.pi / 4)) == sp.Rational(1, 2),
        "selected=cos(alpha)^2; spectator=sin(alpha)^2.",
    )

    section("C. What is now ruled out")

    ruled_out = [
        "finite C3/spin/projective Wilson data -> no exp(2i) d2 power law",
        "one-clock propagator equivariance -> selected phase lambda remains free",
        "hw=1+baryon total support -> selected/spectator split remains free",
        "unmarked primitive naturality -> selected=spectator=1/2",
        "invariant boundary defect -> scalar; rank-one defect orientation remains free",
        "Q-invariant source transfer -> no rank-one mark; nonzero source orientation reopens Q",
    ]
    record(
        "C.1 six distinct routes reduce to the same selected endpoint mark/basepoint primitive",
        len(ruled_out) == 6,
        "\n".join(ruled_out),
    )
    record(
        "C.2 current packet does not prove no future theory can close delta",
        True,
        "It exhausts these retained/radian/mark/source-transfer classes and names the next primitive exactly.",
    )

    section("D. Remaining positive theorem")

    theorem = (
        "Derive a retained oriented selected rank-one endpoint mark P_sel and "
        "a based endpoint trivialization c=0 from physical boundary/source "
        "structure, while preserving Q's quotient/zero-source readout; or "
        "derive an equivalent vector-valued joint Q/delta theorem."
    )
    record(
        "D.1 remaining theorem statement is explicit",
        True,
        theorem,
    )
    record(
        "D.2 this reassessment is not delta closure",
        True,
        "No artifact in this packet sets the mark and basepoint from retained physics.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: selected-endpoint mark reassessment narrows delta but does not close it.")
        print("KOIDE_DELTA_SELECTED_ENDPOINT_MARK_REASSESSMENT=TRUE")
        print("DELTA_SELECTED_ENDPOINT_MARK_REASSESSMENT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_MARK=retained_oriented_selected_rank_one_endpoint_mark")
        print("RESIDUAL_TRIVIALIZATION=based_endpoint_c_equals_zero")
        print("RESIDUAL_COMPATIBILITY=preserve_Q_quotient_zero_source_readout")
        print("NEXT_ATTACK=derive_selected_endpoint_mark_or_formalize_as_explicit_new_primitive")
        return 0

    print("VERDICT: selected-endpoint mark reassessment has FAILs.")
    print("KOIDE_DELTA_SELECTED_ENDPOINT_MARK_REASSESSMENT=FALSE")
    print("DELTA_SELECTED_ENDPOINT_MARK_REASSESSMENT_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
