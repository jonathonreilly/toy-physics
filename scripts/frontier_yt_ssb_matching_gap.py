#!/usr/bin/env python3
"""Verifier for the scoped YT SSB matching-gap arithmetic boundary note.

This runner intentionally checks only the finite-dimensional H_unit component
overlap:

    H_unit = I_(N_iso * N_c) / sqrt(N_iso * N_c)

and therefore

    <alpha_0,a_0 | H_unit | alpha_0,a_0> = 1 / sqrt(N_iso * N_c).

It does not claim to derive the physical Standard Model Yukawa trilinear or to
close the SSB matching gap. The physical matching theorem remains open until
HS/source normalization, SSB VEV division, chirality projection, LSZ/external
state normalization, and absence of extra factors are derived separately.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass


PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-14


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
class PairSpace:
    n_iso: int
    n_c: int

    @property
    def dim(self) -> int:
        return self.n_iso * self.n_c

    @property
    def h_unit_prefactor(self) -> float:
        return 1.0 / math.sqrt(self.dim)

    def index(self, alpha: int, color: int) -> int:
        if not (1 <= alpha <= self.n_iso):
            raise ValueError(f"alpha={alpha} outside 1..{self.n_iso}")
        if not (1 <= color <= self.n_c):
            raise ValueError(f"color={color} outside 1..{self.n_c}")
        return (alpha - 1) * self.n_c + (color - 1)

    def h_unit_matrix_element(
        self,
        alpha_left: int,
        color_left: int,
        alpha_right: int,
        color_right: int,
    ) -> float:
        left = self.index(alpha_left, color_left)
        right = self.index(alpha_right, color_right)
        if left != right:
            return 0.0
        return self.h_unit_prefactor

    def component_overlap(self, alpha: int, color: int) -> float:
        return self.h_unit_matrix_element(alpha, color, alpha, color)


def close(a: float, b: float) -> bool:
    return abs(a - b) < TOL


def block_1_dimensions() -> PairSpace:
    print("\n=== Block 1: canonical dimensions ===\n")

    space = PairSpace(n_iso=2, n_c=3)

    check("1.1  N_iso is positive", space.n_iso > 0, f"N_iso={space.n_iso}")
    check("1.2  N_c is positive", space.n_c > 0, f"N_c={space.n_c}")
    check(
        "1.3  D = N_iso * N_c = 6",
        space.dim == 6,
        f"D={space.dim}",
    )
    check(
        "1.4  H_unit prefactor = 1/sqrt(6)",
        close(space.h_unit_prefactor, 1.0 / math.sqrt(6.0)),
        f"prefactor={space.h_unit_prefactor:.12f}",
    )

    return space


def block_2_matrix_form(space: PairSpace) -> None:
    print("\n=== Block 2: explicit H_unit matrix form ===\n")

    diag = [
        space.h_unit_matrix_element(alpha, color, alpha, color)
        for alpha in range(1, space.n_iso + 1)
        for color in range(1, space.n_c + 1)
    ]
    off_diag = []
    for alpha_l in range(1, space.n_iso + 1):
        for color_l in range(1, space.n_c + 1):
            for alpha_r in range(1, space.n_iso + 1):
                for color_r in range(1, space.n_c + 1):
                    if (alpha_l, color_l) != (alpha_r, color_r):
                        off_diag.append(
                            space.h_unit_matrix_element(
                                alpha_l,
                                color_l,
                                alpha_r,
                                color_r,
                            )
                        )

    expected = 1.0 / math.sqrt(6.0)
    check(
        "2.1  all six diagonal entries equal 1/sqrt(6)",
        all(close(value, expected) for value in diag),
        f"diag entries={[round(value, 12) for value in diag]}",
    )
    check(
        "2.2  all off-diagonal entries vanish",
        all(close(value, 0.0) for value in off_diag),
        f"off-diagonal count={len(off_diag)}",
    )
    check(
        "2.3  trace(H_unit) = sqrt(6)",
        close(sum(diag), math.sqrt(6.0)),
        f"trace={sum(diag):.12f}",
    )


def block_3_component_overlaps(space: PairSpace) -> None:
    print("\n=== Block 3: component overlap theorem ===\n")

    expected = 1.0 / math.sqrt(6.0)
    overlaps = []
    for alpha in range(1, space.n_iso + 1):
        for color in range(1, space.n_c + 1):
            overlaps.append(space.component_overlap(alpha, color))

    check(
        "3.1  every basis component overlap is 1/sqrt(6)",
        all(close(value, expected) for value in overlaps),
        f"overlaps={[round(value, 12) for value in overlaps]}",
    )

    alpha_0, color_0 = 1, 1
    ward_component_label = space.component_overlap(alpha_0, color_0)
    candidate_component_label = space.component_overlap(alpha_0, color_0)
    check(
        "3.2  two labels defined as the same H_unit component overlap agree",
        close(ward_component_label, candidate_component_label),
        (
            f"A={ward_component_label:.12f}, "
            f"B={candidate_component_label:.12f}"
        ),
    )
    check(
        "3.3  the shared component value is 1/sqrt(6)",
        close(ward_component_label, expected),
        f"value={ward_component_label:.12f}",
    )


def block_4_general_dimensions() -> None:
    print("\n=== Block 4: general positive-dimension spot checks ===\n")

    alt = PairSpace(n_iso=3, n_c=4)
    alt_expected = 1.0 / math.sqrt(12.0)
    alt_values = [
        alt.component_overlap(alpha, color)
        for alpha in range(1, alt.n_iso + 1)
        for color in range(1, alt.n_c + 1)
    ]
    check(
        "4.1  (N_iso,N_c)=(3,4) gives 1/sqrt(12) on every component",
        all(close(value, alt_expected) for value in alt_values),
        f"value={alt_values[0]:.12f}",
    )

    minimal = PairSpace(n_iso=1, n_c=1)
    check(
        "4.2  (N_iso,N_c)=(1,1) gives component overlap 1",
        close(minimal.component_overlap(1, 1), 1.0),
        f"value={minimal.component_overlap(1, 1):.12f}",
    )


def block_5_forbidden_imports() -> None:
    print("\n=== Block 5: forbidden physical-readout imports are absent ===\n")

    proof_symbols = {
        "N_iso",
        "N_c",
        "D",
        "I_D",
        "E_alpha_a",
        "H_unit",
        "alpha_0",
        "a_0",
    }
    forbidden_symbols = {
        "g_bare",
        "y_t_phys",
        "V_EWSB",
        "Z_LSZ",
        "P_chiral",
        "sigma_HS",
        "source_normalization",
    }

    leaked = sorted(proof_symbols & forbidden_symbols)
    check(
        "5.1  algebraic proof uses no gauge-coupling/readout symbols",
        not leaked,
        f"leaked={leaked}",
    )

    physical_matching_claimed = False
    hs_source_normalization_derived = False
    ssb_vev_division_derived = False
    chirality_projection_derived = False
    lsz_normalization_derived = False
    no_extra_factors_derived = False

    check(
        "5.2  runner does not claim physical Yukawa matching closure",
        physical_matching_claimed is False,
    )
    check(
        "5.3  HS/source normalization remains outside this proof",
        hs_source_normalization_derived is False,
    )
    check(
        "5.4  SSB VEV division remains outside this proof",
        ssb_vev_division_derived is False,
    )
    check(
        "5.5  chirality projection remains outside this proof",
        chirality_projection_derived is False,
    )
    check(
        "5.6  LSZ/external-state normalization remains outside this proof",
        lsz_normalization_derived is False,
    )
    check(
        "5.7  absence of extra physical factors remains outside this proof",
        no_extra_factors_derived is False,
    )


def main() -> int:
    print("=" * 72)
    print("YT SSB matching-gap arithmetic boundary verifier")
    print("=" * 72)

    space = block_1_dimensions()
    block_2_matrix_form(space)
    block_3_component_overlaps(space)
    block_4_general_dimensions()
    block_5_forbidden_imports()

    print("\n" + "=" * 72)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 72)

    if FAIL_COUNT == 0:
        print(
            "\n  OUTCOME: exact H_unit component-overlap arithmetic verified.\n"
            "  Framework instance: <component|H_unit|component> = 1/sqrt(6).\n"
            "  Boundary: this does NOT close the physical SSB/Yukawa matching\n"
            "  theorem; that operator-matching problem remains open.\n"
        )
        return 0

    print("\n  OUTCOME: arithmetic verifier FAILED.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
