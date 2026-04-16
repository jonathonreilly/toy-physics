#!/usr/bin/env python3
"""
Three-generation observable incompatibility theorem
==================================================

STATUS: exact conditional support theorem on the retained three-generation /
flavor surface

THEOREM (Conditional observable incompatibility):
  On the physical-lattice Cl(3) / Z^3 surface, the three hw=1 sectors are
  pairwise inequivalent physical sectors of the Hamiltonian observable
  algebra.

  Admissible observable-preserving quotients are linear surjections
  Q : H_hw=1 -> H_red for which the exact retained translation observables
  descend to the quotient, equivalently:

      Q T_mu = T'_mu Q   for mu in {x, y, z}

  for some quotient representation T'_mu on H_red.

  1. The exact lattice translations act on the hw=1 sector by three distinct
     joint characters:
         X1 : (-1, +1, +1)
         X2 : (+1, -1, +1)
         X3 : (+1, +1, -1)
     so the translation algebra separates the three sectors exactly.

  2. Any admissible quotient from 3 sectors to 2 sectors must have an
     invariant one-dimensional kernel. Because the only common translation
     eigenlines are the three sector lines themselves, every such quotient can
     only DELETE one whole sector; it cannot identify two sectors while
     preserving the observable algebra.

  3. Any two-generation flavor package has vanishing CP-odd Jarlskog
     invariant J = 0. If one imposes the retained CKM witness J > 0 from the
     promoted CKM package on the same retained surface, that witness is
     incompatible with every admissible 3 -> 2 quotient.

  Therefore, conditional on the retained CKM witness J > 0, no admissible
  translation-observable-preserving reduction to fewer than three sectors
  reproduces the current retained flavor package.

This theorem is narrower than the full rooting-undefined theorem on C^8:
it works directly on the retained hw=1 observable sector and uses the
promoted CKM package as a retained-surface witness rather than as an
independent derivation of the three-sector surface itself.

PStack experiment: frontier-three-generation-observable-theorem
Dependencies: numpy + canonical_plaquette_surface.py only.
"""

from __future__ import annotations

import math
import sys
from itertools import product

import numpy as np

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def build_translation_operators() -> dict[str, np.ndarray]:
    """Exact translation characters on the retained hw=1 basis {X1, X2, X3}."""
    return {
        "Tx": np.diag([-1.0, +1.0, +1.0]),
        "Ty": np.diag([+1.0, -1.0, +1.0]),
        "Tz": np.diag([+1.0, +1.0, -1.0]),
    }


def translation_commutant_basis(ops: dict[str, np.ndarray]) -> list[np.ndarray]:
    """Basis for the commutant of the exact retained translation algebra."""
    dim = 3
    constraints = []
    eye = np.eye(dim, dtype=complex)
    for op in ops.values():
        constraints.append(np.kron(op.T, eye) - np.kron(eye, op))
    mat = np.vstack(constraints)
    _, svals, vh = np.linalg.svd(mat, full_matrices=True)
    tol = 1e-10 * max(1.0, svals[0]) if len(svals) else 1e-10
    null_vecs = [vh[i] for i, sval in enumerate(svals) if sval < tol]
    for i in range(len(svals), vh.shape[0]):
        null_vecs.append(vh[i])
    return [vec.reshape(dim, dim) for vec in null_vecs]


def joint_projector(chars: tuple[int, int, int], ops: dict[str, np.ndarray]) -> np.ndarray:
    """Projector onto the simultaneous eigenspace with the given sign triple."""
    ident = np.eye(3, dtype=complex)
    proj = ident.copy()
    for sign, name in zip(chars, ("Tx", "Ty", "Tz")):
        proj = proj @ (ident + sign * ops[name]) / 2.0
    return proj


def line_is_invariant(v: np.ndarray, ops: dict[str, np.ndarray], tol: float = 1e-10) -> bool:
    """Whether span{v} is invariant under all operators in ops."""
    for op in ops.values():
        ov = op @ v
        coeff = np.vdot(v, ov) / np.vdot(v, v)
        if np.linalg.norm(ov - coeff * v) > tol:
            return False
    return True


def build_selector_matrix(drop_index: int) -> np.ndarray:
    """2x3 selector deleting one of the three basis sectors."""
    rows = []
    for i in range(3):
        if i == drop_index:
            continue
        row = np.zeros(3, dtype=complex)
        row[i] = 1.0
        rows.append(row)
    return np.array(rows, dtype=complex)


def build_standard_ckm(s12: float, s23: float, s13: float, delta: float) -> np.ndarray:
    c12 = math.sqrt(1.0 - s12 * s12)
    c23 = math.sqrt(1.0 - s23 * s23)
    c13 = math.sqrt(1.0 - s13 * s13)
    phase = complex(math.cos(delta), math.sin(delta))
    return np.array(
        [
            [c12 * c13, s12 * c13, s13 / phase],
            [
                -s12 * c23 - c12 * s23 * s13 * phase,
                c12 * c23 - s12 * s23 * s13 * phase,
                s23 * c13,
            ],
            [
                s12 * s23 - c12 * c23 * s13 * phase,
                -c12 * s23 - s12 * c23 * s13 * phase,
                c23 * c13,
            ],
        ],
        dtype=complex,
    )


def jarlskog_3x3(v_ckm: np.ndarray) -> float:
    return abs(np.imag(v_ckm[0, 1] * v_ckm[1, 2] * np.conj(v_ckm[0, 2]) * np.conj(v_ckm[1, 1])))


def generic_u2(theta: float, alpha: float, beta: float, gamma: float) -> np.ndarray:
    """
    Generic U(2) matrix:
      U = e^{i alpha} [[e^{i beta} c, e^{i gamma} s],
                       [-e^{-i gamma} s, e^{-i beta} c]]
    """
    c = math.cos(theta)
    s = math.sin(theta)
    phase = complex(math.cos(alpha), math.sin(alpha))
    return phase * np.array(
        [
            [complex(math.cos(beta), math.sin(beta)) * c, complex(math.cos(gamma), math.sin(gamma)) * s],
            [-complex(math.cos(-gamma), math.sin(-gamma)) * s, complex(math.cos(-beta), math.sin(-beta)) * c],
        ],
        dtype=complex,
    )


def jarlskog_2x2(u: np.ndarray) -> float:
    return float(np.imag(u[0, 0] * u[1, 1] * np.conj(u[0, 1]) * np.conj(u[1, 0])))


def part1_translation_observable_algebra() -> dict[str, np.ndarray]:
    print("=" * 88)
    print("PART 1: EXACT TRANSLATION CHARACTERS ON THE hw=1 SECTORS")
    print("=" * 88)
    print()

    ops = build_translation_operators()
    sector_chars = {
        "X1": (-1, +1, +1),
        "X2": (+1, -1, +1),
        "X3": (+1, +1, -1),
    }

    print("  hw=1 basis:")
    for name, chars in sector_chars.items():
        print(f"    {name}: chi(Tx,Ty,Tz) = {chars}")
    print()

    check(
        "three hw=1 sectors carry pairwise distinct translation characters",
        len(set(sector_chars.values())) == 3,
    )

    comm_basis = translation_commutant_basis(ops)
    check(
        "translation commutant on H_hw=1 has dimension 3",
        len(comm_basis) == 3,
        f"dim = {len(comm_basis)}",
    )

    basis_projectors = {
        "X1": np.diag([1.0, 0.0, 0.0]),
        "X2": np.diag([0.0, 1.0, 0.0]),
        "X3": np.diag([0.0, 0.0, 1.0]),
    }
    span_mat = np.stack([m.reshape(-1) for m in comm_basis], axis=1)
    for name, proj_target in basis_projectors.items():
        coeffs, *_ = np.linalg.lstsq(span_mat, proj_target.reshape(-1), rcond=None)
        recon = sum(coeff * basis for coeff, basis in zip(coeffs, comm_basis))
        err = np.linalg.norm(recon - proj_target)
        check(
            f"sector projector {name} lies in the exact translation commutant",
            err < 1e-12,
            f"reconstruction error = {err:.2e}",
        )

    nonzero_char_triples = []
    for chars in product((-1, +1), repeat=3):
        proj = joint_projector(chars, ops)
        rank = int(np.linalg.matrix_rank(proj, tol=1e-10))
        if rank:
            nonzero_char_triples.append(chars)
        check(
            f"joint projector rank for character {chars}",
            rank in (0, 1),
            f"rank = {rank}",
        )

    expected = {sector_chars["X1"], sector_chars["X2"], sector_chars["X3"]}
    check(
        "only the three sector character triples have nonzero joint projector",
        set(nonzero_char_triples) == expected,
        f"nonzero = {sorted(nonzero_char_triples)}",
    )

    for name, chars in sector_chars.items():
        proj = joint_projector(chars, ops)
        err = np.linalg.norm(proj - basis_projectors[name])
        check(
            f"joint projector isolates sector {name}",
            err < 1e-12,
            f"||P-{name}|| = {err:.2e}",
        )

    projector_sum = sum(joint_projector(chars, ops) for chars in expected)
    check(
        "sector projectors resolve the hw=1 identity exactly",
        np.linalg.norm(projector_sum - np.eye(3)) < 1e-12,
        f"resolution error = {np.linalg.norm(projector_sum - np.eye(3)):.2e}",
    )

    print()
    print("  Consequence:")
    print("    the translation observable algebra already separates X1, X2, X3")
    print("    exactly on the retained hw=1 surface, and its commutant is")
    print("    exhausted by the three sector projectors.")
    print()

    return ops


def part2_no_collapse_quotients(ops: dict[str, np.ndarray]) -> None:
    print("=" * 88)
    print("PART 2: CLASSIFYING ADMISSIBLE TRANSLATION-OBSERVABLE 3->2 QUOTIENTS")
    print("=" * 88)
    print()

    e1 = np.array([1.0, 0.0, 0.0], dtype=complex)
    e2 = np.array([0.0, 1.0, 0.0], dtype=complex)
    e3 = np.array([0.0, 0.0, 1.0], dtype=complex)

    check("sector line X1 is translation-invariant", line_is_invariant(e1, ops))
    check("sector line X2 is translation-invariant", line_is_invariant(e2, ops))
    check("sector line X3 is translation-invariant", line_is_invariant(e3, ops))

    pair_differences = {
        "X1-X2": e1 - e2,
        "X1-X3": e1 - e3,
        "X2-X3": e2 - e3,
    }
    for name, vec in pair_differences.items():
        check(
            f"identification kernel {name} is not translation-invariant",
            not line_is_invariant(vec, ops),
        )

    for drop_index in range(3):
        selector = build_selector_matrix(drop_index)
        for op_name, op in ops.items():
            induced = selector @ op @ selector.conj().T
            err = np.linalg.norm(selector @ op - induced @ selector)
            check(
                f"delete-sector quotient {drop_index + 1} intertwines {op_name}",
                err < 1e-12,
                f"intertwiner error = {err:.2e}",
            )

    print()
    print("  Exact quotient theorem:")
    print("    admissible quotients are defined here by preservation of the")
    print("    exact retained translation observables, equivalently by")
    print("    translation intertwining Q T_mu = T'_mu Q on the hw=1 surface.")
    print("    every admissible 3->2 quotient has a one-dimensional")
    print("    invariant kernel; the exhaustive joint-character scan above shows")
    print("    the only invariant lines are X1, X2, X3 themselves.")
    print("    So a legal 3->2 quotient can only delete one whole sector.")
    print("    It cannot identify two sectors while preserving the observable")
    print("    algebra of lattice translations.")
    print()


def part3_ckm_witness() -> None:
    print("=" * 88)
    print("PART 3: CONDITIONAL CKM / JARLSKOG WITNESS -- TWO SECTORS ARE NOT ENOUGH")
    print("=" * 88)
    print()

    alpha_s_v = CANONICAL_ALPHA_S_V
    lam = math.sqrt(alpha_s_v / 2.0)
    A = math.sqrt(2.0 / 3.0)
    radial = 1.0 / math.sqrt(6.0)
    delta = math.atan(math.sqrt(5.0))

    s12 = lam
    s23 = A * lam**2
    s13 = A * lam**3 * radial

    v_ckm = build_standard_ckm(s12, s23, s13, delta)
    unitarity_err = np.linalg.norm(v_ckm @ v_ckm.conj().T - np.eye(3))
    j3 = jarlskog_3x3(v_ckm)

    print(f"  canonical alpha_s(v) = {alpha_s_v:.12f}")
    print(f"  |V_us| = {s12:.6f}")
    print(f"  |V_cb| = {s23:.6f}")
    print(f"  |V_ub| = {s13:.6f}")
    print(f"  delta  = {math.degrees(delta):.6f} deg")
    print(f"  J      = {j3:.6e}")
    print()

    check("promoted CKM matrix is unitary", unitarity_err < 1e-12, f"||VV^dag-I|| = {unitarity_err:.2e}")
    check("promoted CKM package has nonzero Jarlskog invariant", j3 > 1e-6, f"J = {j3:.6e}")

    thetas = np.linspace(0.13, 1.17, 5)
    phase_grid = np.linspace(0.19, 1.73, 5)
    max_j2 = 0.0
    max_formula_err = 0.0
    checked = 0
    for theta in thetas:
        c = math.cos(float(theta))
        s = math.sin(float(theta))
        expected = -(c * s) ** 2
        for alpha in phase_grid:
            for beta in phase_grid:
                for gamma in phase_grid:
                    u2 = generic_u2(float(theta), float(alpha), float(beta), float(gamma))
                    q2 = u2[0, 0] * u2[1, 1] * np.conj(u2[0, 1]) * np.conj(u2[1, 0])
                    j2 = jarlskog_2x2(u2)
                    max_j2 = max(max_j2, abs(j2))
                    max_formula_err = max(max_formula_err, abs(q2 - expected))
                    checked += 1

    check(
        "generic U(2) flavor package has J_2 = 0 on a dense parameter grid",
        max_j2 < 1e-12,
        f"{checked} samples, max |J_2| = {max_j2:.2e}",
    )
    check(
        "U(2) plaquette product equals -cos^2(theta) sin^2(theta) exactly",
        max_formula_err < 1e-12,
        f"{checked} samples, max formula error = {max_formula_err:.2e}",
    )

    print()
    print("  Consequence:")
    print("    an admissible 3->2 quotient can only delete one full sector,")
    print("    leaving a two-generation flavor package; every such package has J = 0.")
    print("    So if the retained CKM witness J > 0 is imposed on the same surface,")
    print("    no admissible reduction to fewer than three sectors can reproduce")
    print("    the retained observable flavor structure.")
    print()


def main() -> int:
    print("=" * 88)
    print("THREE-GENERATION OBSERVABLE INCOMPATIBILITY THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Are the three retained hw=1 sectors merely label copies, or are they")
    print("  physically distinct sectors whose exact translation-observable class")
    print("  cannot be reduced below three sectors without losing the retained")
    print("  flavor witness?")
    print()

    ops = part1_translation_observable_algebra()
    part2_no_collapse_quotients(ops)
    part3_ckm_witness()

    print("=" * 88)
    print("SYNTHESIS")
    print("=" * 88)
    print()
    print("  THEOREM.")
    print("    1. The exact translation algebra on the retained hw=1 sector has")
    print("       three distinct joint characters and exact rank-1 sector projectors.")
    print("    2. Therefore any admissible quotient to two sectors can only")
    print("       delete one whole sector; it cannot identify sectors.")
    print("    3. Any two-generation flavor package has J = 0. If the retained")
    print("       CKM witness J > 0 is imposed, it is incompatible with such")
    print("       a quotient.")
    print("    4. Hence, conditional on the retained CKM witness, no admissible")
    print("       translation-observable-preserving reduction to fewer than")
    print("       three sectors reproduces the observable flavor package.")
    print()
    print("  Relation to the existing rooting theorem:")
    print("    - frontier_generation_rooting_undefined.py blocks Cl(3)-preserving")
    print("      taste removal on the full C^8 surface.")
    print("    - this runner blocks admissible observable-sector reduction")
    print("      directly on the retained hw=1 physical sector.")
    print()
    print(f"  TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
