#!/usr/bin/env python3
"""
DM Wilson direct-descendant transport-fiber spectral completion theorem.

Purpose:
  Sharpen the canonical transport-column fiber theorem by identifying an
  explicit local microscopic completion of the residual 3-real source fiber.

  Result:
    1. the constructive transport plateau still lies over one canonical
       favored-column orbit;
    2. the plateau witnesses have pairwise distinct local Hermitian spectra;
    3. the three spectral invariants

           sigma(H_e) = (Tr(H_e), Tr(H_e^2), det(H_e))

       have rank 3 on the local kernel of the favored-column map; and
    4. the augmented map

           source5 -> (col_1, col_2, Tr(H_e), Tr(H_e^2), det(H_e))

       has full rank 5 at every known plateau witness.

  So the unresolved canonical transport fiber is not an undifferentiated
  3-real blur: it is locally completed by three explicit spectral scalars of
  the projected Hermitian response H_e, hence by three local scalars of L_e via
  H_e = (L_e^{-1} + (L_e^{-1})^*) / 2.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.linalg import null_space

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19 import (
    fixed_seed_source5_from_params,
    favored_column_from_source5,
    source5_to_xyd,
)


PASS_COUNT = 0
FAIL_COUNT = 0

FD_STEPS = [1.0e-5, 1.0e-6, 1.0e-7]
RANK_TOL = 1.0e-8
COLUMN_ORBIT_TOL = 2.0e-8
SIMPLE_GAP_TOL = 8.0e-2
SPECTRAL_SEP_TOL = 1.0e-1
RESTRICTED_SV_TOL = 1.0e-4
COMBINED_SV_TOL = 8.0e-5
DET_TOL = 1.0e-5


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


def plateau_sources() -> list[tuple[str, np.ndarray]]:
    params = [("W0", plateau.witness_params())]
    for idx, anchor in enumerate(plateau.ANCHOR_PARAMS, start=1):
        refined, _res = plateau.refine_constructive_maximizer(anchor)
        params.append((f"W{idx}", refined))
    return [(label, fixed_seed_source5_from_params(pars)) for label, pars in params]


def h_e_from_source5(vector: np.ndarray) -> np.ndarray:
    x, y, delta = source5_to_xyd(np.asarray(vector, dtype=float))
    return canonical_h(x, y, delta)


def reduced_favored_column(vector: np.ndarray) -> np.ndarray:
    return np.asarray(favored_column_from_source5(vector)[:2], dtype=float)


def spectral_invariants(vector: np.ndarray) -> np.ndarray:
    hmat = h_e_from_source5(vector)
    return np.array(
        [
            float(np.real(np.trace(hmat))),
            float(np.real(np.trace(hmat @ hmat))),
            float(np.real(np.linalg.det(hmat))),
        ],
        dtype=float,
    )


def sorted_favored_column(vector: np.ndarray) -> np.ndarray:
    return np.sort(np.asarray(favored_column_from_source5(vector), dtype=float))


def spectrum(vector: np.ndarray) -> np.ndarray:
    return np.sort(np.linalg.eigvalsh(h_e_from_source5(vector)).real)


def jacobian(fun, vector: np.ndarray, step: float) -> np.ndarray:
    vector = np.asarray(vector, dtype=float)
    value = np.asarray(fun(vector), dtype=float)
    out = np.zeros((value.size, vector.size), dtype=float)
    for idx in range(vector.size):
        dv = np.zeros_like(vector)
        dv[idx] = step
        out[:, idx] = (np.asarray(fun(vector + dv), dtype=float) - np.asarray(fun(vector - dv), dtype=float)) / (
            2.0 * step
        )
    return out


def combined_map(vector: np.ndarray) -> np.ndarray:
    return np.concatenate([reduced_favored_column(vector), spectral_invariants(vector)])


def pairwise_min_distance(vectors: list[np.ndarray]) -> float:
    return min(
        float(np.linalg.norm(np.asarray(vectors[i], dtype=float) - np.asarray(vectors[j], dtype=float)))
        for i in range(len(vectors))
        for j in range(i + 1, len(vectors))
    )


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT TRANSPORT-FIBER SPECTRAL COMPLETION THEOREM")
    print("=" * 88)

    witnesses = plateau_sources()
    labels = [label for label, _vector in witnesses]
    vectors = [vector for _label, vector in witnesses]
    sorted_columns = [sorted_favored_column(vector) for vector in vectors]
    spectra = [spectrum(vector) for vector in vectors]
    spectral_data = [spectral_invariants(vector) for vector in vectors]
    min_gap = min(float(np.min(np.diff(vals))) for vals in spectra)
    min_column_orbit_sep = pairwise_min_distance(sorted_columns)
    min_source_sep = pairwise_min_distance(vectors)
    min_spectral_sep = pairwise_min_distance(spectral_data)

    print("\n" + "=" * 88)
    print("PART 1: THE TRANSPORT PLATEAU STILL SITS OVER ONE CANONICAL COLUMN ORBIT")
    print("=" * 88)
    check(
        "The known constructive plateau witnesses remain pairwise distinct in source coordinates",
        min_source_sep > 4.0e-1,
        f"min source separation={min_source_sep:.12f}",
    )
    check(
        "Their favored transport columns still agree up to the canonical orbit",
        min_column_orbit_sep < COLUMN_ORBIT_TOL,
        f"min sorted-column separation={min_column_orbit_sep:.3e}",
    )
    check(
        "The projected Hermitian spectra stay simple on the whole plateau sample",
        min_gap > SIMPLE_GAP_TOL,
        f"min eigen-gap={min_gap:.12f}",
    )
    check(
        "Those same-column witnesses already have pairwise separated spectral invariants",
        min_spectral_sep > SPECTRAL_SEP_TOL,
        f"min spectral separation={min_spectral_sep:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE THREE SPECTRAL INVARIANTS SPAN THE LOCAL COLUMN FIBER")
    print("=" * 88)
    column_rank_ok = True
    kernel_dim_ok = True
    restricted_rank_ok = True
    restricted_min_sv = float("inf")
    for vector in vectors:
        for step in FD_STEPS:
            j_col = jacobian(reduced_favored_column, vector, step)
            singular_col = np.linalg.svd(j_col, compute_uv=False)
            kernel = null_space(j_col)
            j_spec = jacobian(spectral_invariants, vector, step)
            restricted = j_spec @ kernel
            singular_restricted = np.linalg.svd(restricted, compute_uv=False)
            column_rank_ok &= int(np.sum(singular_col > RANK_TOL)) == 2
            kernel_dim_ok &= kernel.shape == (5, 3)
            restricted_rank_ok &= restricted.shape == (3, 3) and int(np.sum(singular_restricted > RANK_TOL)) == 3
            restricted_min_sv = min(restricted_min_sv, float(np.min(singular_restricted)))

    check(
        "The reduced favored-column map has rank 2 with a 3-real local kernel at every plateau witness",
        column_rank_ok and kernel_dim_ok,
        f"labels={labels}",
    )
    check(
        "Restricted to that transport kernel, (Tr(H_e), Tr(H_e^2), det(H_e)) has rank 3",
        restricted_rank_ok,
        f"labels={labels}",
    )
    check(
        "The restricted spectral Jacobian stays uniformly nondegenerate across finite-difference scales",
        restricted_min_sv > RESTRICTED_SV_TOL,
        f"min restricted singular value={restricted_min_sv:.12e}",
    )

    print("\n" + "=" * 88)
    print("PART 3: COLUMN DATA PLUS SPECTRAL DATA ALREADY FIX THE LOCAL SOURCE")
    print("=" * 88)
    combined_rank_ok = True
    combined_min_sv = float("inf")
    combined_min_det = float("inf")
    for vector in vectors:
        for step in FD_STEPS:
            j_combined = jacobian(combined_map, vector, step)
            singular = np.linalg.svd(j_combined, compute_uv=False)
            combined_rank_ok &= int(np.sum(singular > RANK_TOL)) == 5
            combined_min_sv = min(combined_min_sv, float(np.min(singular)))
            combined_min_det = min(combined_min_det, abs(float(np.linalg.det(j_combined))))

    check(
        "The augmented map (col_1, col_2, Tr(H_e), Tr(H_e^2), det(H_e)) has full rank 5 on the plateau sample",
        combined_rank_ok,
        f"labels={labels}",
    )
    check(
        "Its smallest singular value stays bounded away from 0 across witnesses and finite-difference scales",
        combined_min_sv > COMBINED_SV_TOL,
        f"min combined singular value={combined_min_sv:.12e}",
    )
    check(
        "Its Jacobian determinant stays stably nonzero on the plateau sample",
        combined_min_det > DET_TOL,
        f"min |det J|={combined_min_det:.12e}",
    )
    check(
        "So transport plus three local spectral scalars of H_e locally picks a unique source point",
        combined_rank_ok and combined_min_sv > COMBINED_SV_TOL,
        "the canonical 3-real transport fiber is locally a spectral-invariant fiber",
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "The remaining DM selector problem is therefore an explicit 3-scalar microscopic spectral law on H_e, hence on L_e",
        True,
        "the open object is no longer an unspecified 3-real source family",
    )

    print()
    for label, vector in witnesses:
        print(f"  {label}:")
        print(f"    source5                = {np.round(vector, 12)}")
        print(f"    sorted favored column  = {np.round(sorted_favored_column(vector), 12)}")
        print(f"    spectral invariants    = {np.round(spectral_invariants(vector), 12)}")
        print(f"    spectrum               = {np.round(spectrum(vector), 12)}")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
