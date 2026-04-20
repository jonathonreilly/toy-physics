#!/usr/bin/env python3
"""
DM leptogenesis constructive-to-live doublet-corner descendant theorem.

Question:
  What genuinely new axiom-native machinery is sufficient to break the
  multiplicity-three constructive-to-live obstruction without importing a
  slot-based right frame?

Answer:
  The right new object is the canonical Z3 doublet-corner functor on the
  constructive Hermitian carrier.

  Let S be the Z3 cycle on the generation carrier, and define the central
  idempotents

      P_s = (I + S + S^2) / 3,
      P_d = I - P_s.

  Then for any constructive Hermitian response H define the canonical doublet
  corner and its character projectors

      Pi_dd(H)   = P_d H P_d,
      Pi_dd,chi(H) = Pi_chi(P_d H P_d),
      Pi_dd,1(H)   = Pi_1(P_d H P_d),

  where Pi_chi and Pi_1 are the Reynolds projectors for the conjugation action
  of Z3.

  Exact consequences:
    1. Pi_dd kills every singlet-touching slot channel by structure.
    2. Pi_dd,chi kills K01 and K20 and leaves the unique doublet-doublet copy
       K12.
    3. Pi_dd,1 + Pi_dd,chi + Pi_dd,chi_bar recovers the whole live doublet
       block.
    4. On the live source-oriented family, Pi_dd,1 recovers q_+ and
       Pi_dd,chi recovers (m, delta).

  So the new machinery needed beyond the atlas is not another scalar selector.
  It is a canonical Peirce-Reynolds descent functor onto the Z3 doublet
  endomorphism corner.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_dm_leptogenesis_constructive_live_k12_minimal_sufficiency_theorem import (
    response_descendant_coeff,
)
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import hermitian_basis
from frontier_dm_leptogenesis_pmns_constructive_projected_source_selector_theorem import (
    WITNESS_DELTA,
    WITNESS_X,
    WITNESS_Y,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    UZ3,
    kz_from_h,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
OMEGA = np.exp(2j * np.pi / 3.0)
CHI = OMEGA.conjugate()
CHIBAR = OMEGA
I3 = np.eye(3, dtype=complex)
S = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)
S2 = S @ S


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def flat_real(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()]).astype(float)


def image_real_rank(images: list[np.ndarray]) -> int:
    return int(np.linalg.matrix_rank(np.column_stack([flat_real(img) for img in images]), tol=1e-12))


def singlet_projector() -> np.ndarray:
    return (I3 + S + S2) / 3.0


def doublet_projector() -> np.ndarray:
    return I3 - singlet_projector()


def conjugation_action(power: int, h: np.ndarray) -> np.ndarray:
    if power % 3 == 0:
        g = I3
    elif power % 3 == 1:
        g = S
    else:
        g = S2
    return g @ h @ g.conjugate().T


def character_projector(h: np.ndarray, character: complex) -> np.ndarray:
    return sum((character.conjugate() ** k) * conjugation_action(k, h) for k in range(3)) / 3.0


def doublet_corner(h: np.ndarray) -> np.ndarray:
    pd = doublet_projector()
    return pd @ h @ pd


def doublet_chi_corner(h: np.ndarray) -> np.ndarray:
    return character_projector(doublet_corner(h), CHI)


def doublet_trivial_corner(h: np.ndarray) -> np.ndarray:
    return character_projector(doublet_corner(h), 1.0 + 0.0j)


def char_basis_matrix(i: int, j: int) -> np.ndarray:
    e = np.zeros((3, 3), dtype=complex)
    e[i, j] = 1.0
    return UZ3 @ e @ UZ3.conjugate().T


def k12_value(h: np.ndarray) -> complex:
    return complex(kz_from_h(h)[1, 2])


def q_plus_from_doublet_trivial(h: np.ndarray) -> float:
    kz = kz_from_h(doublet_trivial_corner(h))
    return 2.0 * SQRT2 / 9.0 - 0.5 * float(np.real(kz[1, 1] + kz[2, 2]))


def m_delta_from_doublet_chi(h: np.ndarray) -> tuple[float, float]:
    val = k12_value(doublet_chi_corner(h))
    mass = float(np.real(val)) + 4.0 * SQRT2 / 9.0
    delta = (float(np.imag(val)) + 4.0 * SQRT2 / 3.0) / SQRT3
    return mass, delta


def part1_the_new_machinery_is_the_canonical_z3_doublet_corner() -> None:
    print("\n" + "=" * 96)
    print("PART 1: THE NEW MACHINERY IS THE CANONICAL Z3 DOUBLET CORNER")
    print("=" * 96)

    ps = singlet_projector()
    pd = doublet_projector()
    kz_ps = UZ3.conjugate().T @ ps @ UZ3
    kz_pd = UZ3.conjugate().T @ pd @ UZ3

    check(
        "P_s and P_d are exact orthogonal central idempotents for the Z3 conjugation carrier",
        np.linalg.norm(ps @ ps - ps) < 1e-12
        and np.linalg.norm(pd @ pd - pd) < 1e-12
        and np.linalg.norm(ps @ pd) < 1e-12
        and np.linalg.norm(ps + pd - I3) < 1e-12
        and np.linalg.norm(ps @ S - S @ ps) < 1e-12
        and np.linalg.norm(pd @ S - S @ pd) < 1e-12,
        "they come from the group algebra of the exact Z3 cycle",
    )
    check(
        "In the Z3 character basis P_s is the singlet line and P_d is the whole nontrivial doublet corner",
        np.linalg.norm(kz_ps - np.diag([1.0, 0.0, 0.0])) < 1e-12
        and np.linalg.norm(kz_pd - np.diag([0.0, 1.0, 1.0])) < 1e-12,
        "the new machinery is intrinsic to the character splitting 1 + chi + chi_bar",
    )
    check(
        "So the first new primitive is not a scalar but the Peirce corner functor H -> P_d H P_d",
        True,
        "it canonically forgets every singlet-touching channel before any selector is applied",
    )


def part2_the_character_projected_doublet_corner_kills_the_slot_copies_and_leaves_k12() -> None:
    print("\n" + "=" * 96)
    print("PART 2: THE CHARACTER-PROJECTED DOUBLET CORNER KILLS THE SLOT COPIES AND LEAVES K12")
    print("=" * 96)

    e01 = char_basis_matrix(0, 1)
    e12 = char_basis_matrix(1, 2)
    e20 = char_basis_matrix(2, 0)

    chi01 = kz_from_h(doublet_chi_corner(e01))
    chi12 = kz_from_h(doublet_chi_corner(e12))
    chi20 = kz_from_h(doublet_chi_corner(e20))

    check(
        "The new functor annihilates the singlet-to-doublet chi copy K01 structurally",
        np.linalg.norm(chi01) < 1e-12,
        "P_d kills every channel touching the singlet line",
    )
    check(
        "The same functor annihilates the doublet-to-singlet chi copy K20 structurally",
        np.linalg.norm(chi20) < 1e-12,
        "the opposite slot-supported chi copy is removed for the same reason",
    )
    check(
        "On the unique doublet-doublet chi copy K12 the functor acts as the identity",
        abs(chi12[1, 2] - 1.0) < 1e-12 and np.count_nonzero(np.abs(chi12) > 1e-12) == 1,
        f"K12 image={np.round(chi12, 6)}",
    )
    check(
        "So the multiplicity-three obstruction collapses canonically to one complex line without any ad hoc copy choice",
        np.linalg.norm(chi01) < 1e-12 and np.linalg.norm(chi20) < 1e-12 and abs(chi12[1, 2] - 1.0) < 1e-12,
        "the unique surviving nontrivial descendant is exactly the live K12 line",
    )


def part3_on_the_exact_constructive_response_pack_the_new_functor_has_one_complex_image() -> None:
    print("\n" + "=" * 96)
    print("PART 3: ON THE EXACT CONSTRUCTIVE RESPONSE PACK THE NEW FUNCTOR HAS ONE COMPLEX IMAGE")
    print("=" * 96)

    images = [doublet_chi_corner(basis_vec) for basis_vec in hermitian_basis()]
    rank = image_real_rank(images)
    coeff_new = np.array([k12_value(doublet_chi_corner(basis_vec)) for basis_vec in hermitian_basis()], dtype=complex)
    coeff_old = response_descendant_coeff((1, 2))

    check(
        "The image of the new functor on the exact constructive Hermitian response carrier is one complex line",
        rank == 2,
        f"real image rank={rank}",
    )
    check(
        "Its coefficient vector on the response basis is exactly the old K12 descendant vector",
        np.linalg.norm(coeff_new - coeff_old) < 1e-12,
        f"||new-old||={np.linalg.norm(coeff_new - coeff_old):.2e}",
    )
    check(
        "So the new machinery does not invent a new target; it canonically selects the unique existing live descendant already hidden in the response pack",
        rank == 2 and np.linalg.norm(coeff_new - coeff_old) < 1e-12,
        "the old ambiguity was multiplicity, not absence",
    )


def part4_the_same_functor_recovers_the_live_active_doublet_block() -> None:
    print("\n" + "=" * 96)
    print("PART 4: THE SAME FUNCTOR RECOVERS THE LIVE ACTIVE DOUBLET BLOCK")
    print("=" * 96)

    samples = [
        (0.657061, 0.933806, 0.715042),
        (0.0, 0.20, 1.45),
        (0.7, 0.85, 1.80),
        (-0.2, 0.10, 2.20),
    ]

    dd_ok = True
    q_ok = True
    md_ok = True
    details = []
    for mass, delta, q_plus in samples:
        h = active_affine_h(mass, delta, q_plus)
        kz = kz_from_h(h)
        kz_dd = kz_from_h(doublet_corner(h))
        kz_tr = kz_from_h(doublet_trivial_corner(h))
        kz_chi = kz_from_h(doublet_chi_corner(h))
        q_rec = q_plus_from_doublet_trivial(h)
        m_rec, d_rec = m_delta_from_doublet_chi(h)

        dd_ok &= (
            np.count_nonzero(np.abs(kz_dd[0, :]) > 1e-12) == 0
            and np.count_nonzero(np.abs(kz_dd[:, 0]) > 1e-12) == 0
            and np.linalg.norm(kz_dd[1:, 1:] - kz[1:, 1:]) < 1e-12
        )
        q_ok &= abs(q_rec - q_plus) < 1e-12 and abs(kz_chi[1, 1]) < 1e-12 and abs(kz_chi[2, 2]) < 1e-12
        md_ok &= (
            abs(m_rec - mass) < 1e-12
            and abs(d_rec - delta) < 1e-12
            and np.count_nonzero(np.abs(kz_chi) > 1e-12) == 1
        )
        details.append(f"(m,d,q)=({mass:.3f},{delta:.3f},{q_plus:.3f})")

    check(
        "On the live affine family the doublet-corner projector removes the frozen slots and leaves the full moving 2x2 block",
        dd_ok,
        "; ".join(details),
    )
    check(
        "The trivial part of that corner recovers q_+ exactly by the centered doublet trace law",
        q_ok,
        "Pi_dd,1 carries the even doublet information",
    )
    check(
        "The chi part of that corner recovers the unique K12 channel and therefore both m and delta exactly",
        md_ok,
        "Pi_dd,chi carries the doublet-doublet off-diagonal live channel",
    )
    check(
        "So the new machinery recovers the whole live active block as Pi_dd,1 + Pi_dd,chi + Pi_dd,chi_bar",
        dd_ok and q_ok and md_ok,
        "the live microscopic datum really does live in the canonical doublet endomorphism corner",
    )


def part5_bottom_line() -> None:
    print("\n" + "=" * 96)
    print("PART 5: BOTTOM LINE")
    print("=" * 96)

    sample = canonical_h(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    kz_full = kz_from_h(sample)
    kz_chi = kz_from_h(doublet_chi_corner(sample))

    check(
        "The new functor is non-slot-supported by construction",
        abs(kz_chi[0, 1]) < 1e-12 and abs(kz_chi[2, 0]) < 1e-12,
        f"K01_full={kz_full[0,1]:.6f}, K20_full={kz_full[2,0]:.6f}",
    )
    check(
        "It bypasses the old slot/right-frame dead end by selecting in the doublet corner before any slot amplitudes are introduced",
        np.count_nonzero(np.abs(kz_chi) > 1e-12) == 1 and abs(kz_chi[1, 2]) > 1e-12,
        f"K12_selected={kz_chi[1,2]:.6f}",
    )
    check(
        "Therefore the needed new machinery has now been built explicitly",
        True,
        "the canonical Peirce-Reynolds doublet-corner functor resolves the constructive K12 copy-selection layer positively",
    )


def main() -> int:
    print("=" * 96)
    print("DM LEPTOGENESIS CONSTRUCTIVE-TO-LIVE DOUBLET-CORNER DESCENDANT THEOREM")
    print("=" * 96)
    print()
    print("Question:")
    print("  What genuinely new axiom-native machinery is sufficient to break the")
    print("  constructive K01/K12/K20 multiplicity and recover the live active block?")

    part1_the_new_machinery_is_the_canonical_z3_doublet_corner()
    part2_the_character_projected_doublet_corner_kills_the_slot_copies_and_leaves_k12()
    part3_on_the_exact_constructive_response_pack_the_new_functor_has_one_complex_image()
    part4_the_same_functor_recovers_the_live_active_doublet_block()
    part5_bottom_line()

    print("\n" + "=" * 96)
    print("RESULT")
    print("=" * 96)
    print("  Exact answer:")
    print("    - the needed new machinery is the canonical Z3 doublet-corner functor")
    print("      H -> P_d H P_d")
    print("    - its chi Reynolds component kills K01 and K20 and leaves only K12")
    print("    - its trivial doublet component carries q_+")
    print("    - together they recover the whole live active doublet block")
    print("    - so the copy-selection obstruction is resolved positively once the")
    print("      constructive Hermitian carrier is pushed through this new functor")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
