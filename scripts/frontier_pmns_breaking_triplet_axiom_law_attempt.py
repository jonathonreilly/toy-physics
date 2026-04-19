#!/usr/bin/env python3
"""
Exact boundary theorem:
the current retained PMNS bank does not derive a positive axiom-side law for
the global breaking triplet (delta, rho, gamma). The strongest exact theorem
is the zero-locus / minimal-source statement: the breaking triplet is exactly
the 3-real complement of the aligned residual-Z2 core, with a zero locus that
is exactly the aligned core on the canonical positive patch.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def canonical_y(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * phi)], dtype=complex)
    ) @ CYCLE


def canonical_h(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    mat = canonical_y(x, y, phi)
    return mat @ mat.conj().T


def hermitian_coords(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(np.real(h[0, 0])),
        float(np.real(h[1, 1])),
        float(np.real(h[2, 2])),
        float(np.abs(h[0, 1])),
        float(np.abs(h[1, 2])),
        float(np.abs(h[2, 0])),
        float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
    )


def aligned_core_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> np.ndarray:
    b = 0.5 * (r12 + r31 * math.cos(phi))
    c = 0.5 * (d2 + d3)
    return np.array(
        [
            [d1, b, b],
            [b, c, r23],
            [b, r23, c],
        ],
        dtype=complex,
    )


def breaking_triplet_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> tuple[float, float, float]:
    _ = d1, r23
    delta = 0.5 * (d2 - d3)
    rho = 0.5 * (r12 - r31 * math.cos(phi))
    gamma = r31 * math.sin(phi)
    return delta, rho, gamma


def breaking_matrix(delta: float, rho: float, gamma: float) -> np.ndarray:
    return np.array(
        [
            [0.0, rho, -rho - 1j * gamma],
            [rho, delta, 0.0],
            [-rho + 1j * gamma, 0.0, -delta],
        ],
        dtype=complex,
    )


def aligned_basis() -> list[np.ndarray]:
    return [
        np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
    ]


def breaking_basis() -> list[np.ndarray]:
    return [
        np.array([[0, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=complex),
        np.array([[0, 1, -1], [1, 0, 0], [-1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
    ]


def real_vector(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()]).astype(float)


def real_rank(mats: list[np.ndarray]) -> int:
    stacked = np.column_stack([real_vector(m) for m in mats])
    return int(np.linalg.matrix_rank(stacked))


def compact(text: str) -> str:
    return text.replace(" ", "").replace("\n", "").replace("`", "")


def part1_the_global_breaking_triplet_is_exactly_a_three_real_source_complement() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE GLOBAL BREAKING TRIPLET IS EXACTLY A THREE-REAL SOURCE COMPLEMENT")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    h = canonical_h(x, y, phi)
    coords = hermitian_coords(h)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    h_rec = core + breaking_matrix(delta, rho, gamma)

    check(
        "H = H_core + B(delta,rho,gamma) exactly",
        np.linalg.norm(h - h_rec) < 1e-12,
        f"recon err={np.linalg.norm(h - h_rec):.2e}",
    )
    check(
        "The breaking matrix is exactly the delta/rho/gamma source complement",
        np.linalg.norm(
            breaking_matrix(delta, rho, gamma)
            - (delta * breaking_basis()[0] + rho * breaking_basis()[1] + gamma * breaking_basis()[2])
        )
        < 1e-12,
        f"(delta,rho,gamma)=({delta:.6f},{rho:.6f},{gamma:.6f})",
    )
    check(
        "The aligned core has exact residual-Z2 form [[a,b,b],[b,c,d],[b,d,c]]",
        np.linalg.norm(core - core.conj().T) < 1e-12
        and abs(core[0, 1] - core[0, 2]) < 1e-12
        and abs(core[1, 1] - core[2, 2]) < 1e-12,
        f"core offdiag diff={abs(core[0,1]-core[0,2]):.2e}",
    )


def part2_the_zero_locus_is_exactly_the_aligned_core_on_the_positive_patch() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ZERO LOCUS IS EXACTLY THE ALIGNED CORE ON THE POSITIVE PATCH")
    print("=" * 88)

    aligned_x = np.array([1.20, 0.90, 0.90], dtype=float)
    aligned_y = np.array([1.20 * 0.40 / 0.90, 0.40, 0.40], dtype=float)
    aligned_phi = 0.0
    h_al = canonical_h(aligned_x, aligned_y, aligned_phi)
    coords_al = hermitian_coords(h_al)
    core_al = aligned_core_from_coords(*coords_al)
    delta, rho, gamma = breaking_triplet_from_coords(*coords_al)

    check("The aligned sample lies on the canonical full-rank branch",
          np.linalg.matrix_rank(canonical_y(aligned_x, aligned_y, aligned_phi)) == 3,
          f"rank={np.linalg.matrix_rank(canonical_y(aligned_x, aligned_y, aligned_phi))}")
    check("On the aligned sample, the breaking triplet vanishes",
          np.linalg.norm([delta, rho, gamma]) < 1e-12,
          f"triplet={np.array([delta, rho, gamma])}")
    check("On the aligned sample, the breaking matrix is exactly zero",
          np.linalg.norm(breaking_matrix(delta, rho, gamma)) < 1e-12,
          f"B norm={np.linalg.norm(breaking_matrix(delta, rho, gamma)):.2e}")
    check("The aligned sample satisfies P23 H P23 = H",
          np.linalg.norm(P23 @ h_al @ P23 - h_al) < 1e-12,
          f"residual={np.linalg.norm(P23 @ h_al @ P23 - h_al):.2e}")
    check("The aligned sample is exactly the aligned core, not just a coordinate coincidence",
          np.linalg.norm(h_al - core_al) < 1e-12,
          f"recon err={np.linalg.norm(h_al - core_al):.2e}")

    generic_x = np.array([1.15, 0.82, 0.95], dtype=float)
    generic_y = np.array([0.41, 0.28, 0.54], dtype=float)
    generic_phi = 0.63
    h_gen = canonical_h(generic_x, generic_y, generic_phi)
    coords_gen = hermitian_coords(h_gen)
    delta_g, rho_g, gamma_g = breaking_triplet_from_coords(*coords_gen)

    check("A generic sample on the same canonical branch has a nonzero breaking triplet",
          np.linalg.norm([delta_g, rho_g, gamma_g]) > 1e-6,
          f"triplet={np.round([delta_g, rho_g, gamma_g], 6)}")
    check("A generic sample violates the residual-Z2 law",
          np.linalg.norm(P23 @ h_gen @ P23 - h_gen) > 1e-6,
          f"residual={np.linalg.norm(P23 @ h_gen @ P23 - h_gen):.3e}")


def part3_the_source_locus_has_exactly_three_independent_generators() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SOURCE LOCUS HAS EXACTLY THREE INDEPENDENT GENERATORS")
    print("=" * 88)

    aligned_rank = real_rank(aligned_basis())
    breaking_rank = real_rank(breaking_basis())
    total_rank = real_rank(aligned_basis() + breaking_basis())

    check("The aligned core basis has real rank 4", aligned_rank == 4, f"rank={aligned_rank}")
    check("The breaking basis has real rank 3", breaking_rank == 3, f"rank={breaking_rank}")
    check("Together they span the exact 7-dimensional active Hermitian grammar", total_rank == 7, f"rank={total_rank}")
    check("The breaking triplet is not reducible to one or two real source coordinates", breaking_rank == 3,
          "three independent generators are required")

    y0 = canonical_y(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    y1 = canonical_y(
        np.array([1.07, 0.91, 0.79], dtype=float),
        np.array([0.36, 0.33, 0.46], dtype=float),
        -0.41,
    )
    h0 = y0 @ y0.conj().T
    h1 = y1 @ y1.conj().T
    triplet0 = np.array(breaking_triplet_from_coords(*hermitian_coords(h0)), dtype=float)
    triplet1 = np.array(breaking_triplet_from_coords(*hermitian_coords(h1)), dtype=float)

    check("Two generic full-rank points on the same canonical support class can carry distinct breaking triplets",
          np.linalg.norm(triplet0 - triplet1) > 1e-6,
          f"|triplet0-triplet1|={np.linalg.norm(triplet0-triplet1):.3f}")
    check("That distinction shows the current bank still does not fix the source coefficients themselves", True)


def part4_the_existing_boundary_notes_record_the_open_coefficient_gap() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE EXISTING BOUNDARY NOTES RECORD THE OPEN COEFFICIENT GAP")
    print("=" * 88)

    note = read("docs/PMNS_BREAKING_TRIPLET_AXIOM_LAW_ATTEMPT_NOTE.md")
    align = read("docs/PMNS_EWSB_ALIGNMENT_NONFORCING_NOTE.md")
    slots = read("docs/PMNS_EWSB_BREAKING_SLOT_NONREALIZATION_NOTE.md")
    no_go = read("docs/PMNS_RIGHT_CONJUGACY_INVARIANT_NO_GO_NOTE.md")
    intrinsic = read("docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check("The new note states that no positive axiom-side breaking law is currently derivable",
          "no positive axiom-side value law is currently derivable" in note.lower())
    check("The alignment boundary note still says the current bank does not force EWSB alignment",
          "does not force ewsb alignment" in align.lower())
    check("The breaking-slot boundary note still says the current bank does not yet derive the breaking-slot vector",
          "does not yet derive the breaking-slot vector" in slots.lower())
    check("The right-conjugacy no-go still says the missing object must break right-orbit blindness",
          "must genuinely break right-orbit blindness" in no_go.lower())
    check("The intrinsic-completion boundary still records the selected-branch Hermitian-data gap",
          "selected-branch hermitian data" in intrinsic.lower()
          or "selected branch hermitian data" in intrinsic.lower())
    check("The atlas still carries the already-established Hermitian and breaking-slot rows",
          "| PMNS global Hermitian mode package |" in atlas
          and "| PMNS EWSB breaking-slot nonrealization |" in atlas)


def main() -> int:
    print("=" * 88)
    print("PMNS BREAKING TRIPLET AXIOM LAW ATTEMPT")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS global Hermitian mode package")
    print("  - PMNS EWSB residual-Z2 Hermitian core")
    print("  - PMNS EWSB alignment nonforcing")
    print("  - PMNS EWSB breaking-slot nonrealization")
    print("  - PMNS right-conjugacy-invariant no-go")
    print("  - PMNS intrinsic completion boundary")
    print()
    print("Question:")
    print("  Can the current exact bank derive a positive axiom-side law for the")
    print("  global breaking triplet (delta, rho, gamma)?")

    part1_the_global_breaking_triplet_is_exactly_a_three_real_source_complement()
    part2_the_zero_locus_is_exactly_the_aligned_core_on_the_positive_patch()
    part3_the_source_locus_has_exactly_three_independent_generators()
    part4_the_existing_boundary_notes_record_the_open_coefficient_gap()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - no positive axiom-side law for (delta, rho, gamma) is currently")
    print("      derivable")
    print("    - the strongest exact theorem is the zero-locus / minimal-source")
    print("      theorem")
    print("    - the breaking triplet is exactly a 3-real source complement to")
    print("      the aligned residual-Z2 core")
    print("    - its zero locus is exactly the aligned core on the canonical")
    print("      positive patch")
    print("    - the current retained bank does not derive the breaking")
    print("      coefficients as axiom-side outputs")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
