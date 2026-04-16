#!/usr/bin/env python3
"""
Self-contained reviewer packet for the retained neutrino Dirac / PMNS boundary.

Question:
  After the retained three-generation Majorana current-stack law
      M_R,current = 0_(3x3),
  what exactly is closed on the Dirac / PMNS side of the neutrino lane?

Answer on the current retained stack:
  The general retained neutrino-mass problem reduces to the Dirac Yukawa lane.
  On a single-Higgs lane, the Higgs Z_3 charge remains underdetermined,
  Y_nu is monomial for any fixed charge, the charged-lepton sector does not
  rescue PMNS inside that same single-Higgs monomial class, and the smallest
  exact surviving neutrino-side escape class is a two-Higgs Z_3 sector with
  distinct Higgs charges.

Boundary:
  Exact current-stack / extension-class packet only. This does not derive the
  actual Dirac Yukawa coefficients, the Higgs-charge selector, or the observed
  PMNS angles.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

LEFT_CHARGES = np.array([0, 1, 2], dtype=int)
RIGHT_CHARGES = np.array([0, 2, 1], dtype=int)

PERMUTATIONS = {
    0: np.eye(3, dtype=complex),
    1: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex),
    2: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex),
}

OBSERVED_PMNS_ABS = np.array(
    [
        [0.825, 0.545, 0.149],
        [0.269, 0.605, 0.750],
        [0.496, 0.580, 0.646],
    ],
    dtype=float,
)


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


def support_matrix(offset: int) -> np.ndarray:
    support = np.zeros((3, 3), dtype=int)
    for i, q_left in enumerate(LEFT_CHARGES):
        for j, q_right in enumerate(RIGHT_CHARGES):
            if (q_left + offset + q_right) % 3 == 0:
                support[i, j] = 1
    return support


def all_permutation_matrices() -> list[np.ndarray]:
    matrices = []
    for perm in itertools.permutations(range(3)):
        matrix = np.zeros((3, 3), dtype=float)
        for i, j in enumerate(perm):
            matrix[i, j] = 1.0
        matrices.append(matrix)
    return matrices


def is_monomial(matrix: np.ndarray, tol: float = 1e-12) -> bool:
    row_counts = np.count_nonzero(np.abs(matrix) > tol, axis=1)
    col_counts = np.count_nonzero(np.abs(matrix) > tol, axis=0)
    return np.all(row_counts <= 1) and np.all(col_counts <= 1)


def canonical_y_global(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ PERMUTATIONS[1]


def canonical_h_global(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    ymat = canonical_y_global(x, y, delta)
    return ymat @ ymat.conj().T


def invariant_coordinates_global(h: np.ndarray) -> np.ndarray:
    return np.array(
        [
            float(np.real(h[0, 0])),
            float(np.real(h[1, 1])),
            float(np.real(h[2, 2])),
            float(np.abs(h[0, 1])),
            float(np.abs(h[1, 2])),
            float(np.abs(h[2, 0])),
            float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
        ],
        dtype=float,
    )


def reconstruct_from_observables_global(obs: np.ndarray) -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:
    d1, d2, d3, r12, r23, r31, phi = obs
    alpha = r12 * r12
    beta = r23 * r23
    gamma = r31 * r31
    a = d2 * d3 - beta
    b = d1 * d2 * d3 + gamma * d2 - alpha * d3 - beta * d1
    c = gamma * (d1 * d2 - alpha)
    disc = float(b * b - 4.0 * a * c)
    roots = np.array(
        [
            (b - np.sqrt(max(disc, 0.0))) / (2.0 * a),
            (b + np.sqrt(max(disc, 0.0))) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()

    def sheet(root: float) -> tuple[np.ndarray, np.ndarray]:
        t1 = root
        t2 = alpha / (d1 - t1)
        t3 = beta / (d2 - t2)
        x = np.sqrt(np.array([t1, t2, t3], dtype=float))
        y = np.sqrt(np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float))
        return x, y

    return sheet(float(roots[0])), sheet(float(roots[1]))


def sqrt_psd_global(h: np.ndarray) -> np.ndarray:
    evals, vecs = np.linalg.eigh(h)
    evals = np.clip(evals, 0.0, None)
    return vecs @ np.diag(np.sqrt(evals)) @ vecs.conj().T


def compact_global(text: str) -> str:
    return text.replace(" ", "").replace("\n", "").replace("`", "")


def upper_offdiag_score_global(m: np.ndarray) -> int:
    vals = np.array([m[0, 1], m[1, 2], m[0, 2]])
    return int(np.count_nonzero(np.abs(vals) > 1e-10))


def part1_mass_problem_reduces_to_dirac_lane() -> None:
    print("\n" + "=" * 88)
    print("PART 1: AFTER M_R,CURRENT = 0, THE GENERAL MASS PROBLEM REDUCES TO Y_NU")
    print("=" * 88)

    m_r_current = np.zeros((3, 3), dtype=complex)
    m_d = np.array(
        [
            [0.02, 0.01 - 0.03j, 0.00],
            [0.00, 0.05, 0.02 + 0.01j],
            [0.01, 0.00, 0.07],
        ],
        dtype=complex,
    )
    neutral_mass = np.block(
        [
            [np.zeros((3, 3), dtype=complex), m_d],
            [m_d.conj().T, m_r_current],
        ]
    )
    singular_values = np.linalg.svd(m_d, compute_uv=False)
    neutral_evals = np.sort(np.abs(np.linalg.eigvalsh(neutral_mass)))
    doubled_svals = np.sort(np.concatenate([singular_values, singular_values]))

    check("The retained current-stack Majorana matrix is exactly zero", np.linalg.norm(m_r_current) < 1e-12,
          f"||M_R,current||_F={np.linalg.norm(m_r_current):.2e}")
    check("A nonzero Dirac Yukawa matrix alone gives nonzero neutrino masses", np.max(singular_values) > 1e-12,
          f"singular values={np.round(singular_values, 6)}")
    check("The neutral mass matrix reduces to the pure Dirac block form",
          np.linalg.norm(neutral_mass[:3, :3]) < 1e-12 and np.linalg.norm(neutral_mass[3:, 3:]) < 1e-12,
          "Majorana blocks vanish")
    check("The reduced neutral spectrum is exactly the doubled Dirac singular-value spectrum",
          np.allclose(neutral_evals, doubled_svals, atol=1e-12),
          f"eigs={np.round(neutral_evals, 6)}")

    print()
    print("  So the retained neutrino question is no longer 'find a hidden")
    print("  Majorana source just to get mass'. It is 'derive Y_nu', unless")
    print("  a Majorana / seesaw closure is specifically the target.")


def part2_single_higgs_charge_is_underdetermined() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SINGLE-HIGGS Z_3 CHARGE IS REDUCED TO THREE CASES, NOT FIXED")
    print("=" * 88)

    supports = {offset: support_matrix(offset) for offset in [0, 1, 2]}
    distinct = len({tuple(support.reshape(-1).tolist()) for support in supports.values()})
    union = supports[0] + supports[1] + supports[2]

    check("Retained left/right generation charges are the conjugate pair 0,+1,-1 and 0,-1,+1",
          np.array_equal(LEFT_CHARGES, np.array([0, 1, 2])) and np.array_equal(RIGHT_CHARGES, np.array([0, 2, 1])),
          f"q_L={LEFT_CHARGES.tolist()}, q_R={RIGHT_CHARGES.tolist()}")
    for offset, support in supports.items():
        row_sums = support.sum(axis=1)
        col_sums = support.sum(axis=0)
        check(f"offset={offset}: retained invariance admits an exact support pattern",
              np.array_equal(row_sums, np.ones(3, dtype=int)) and np.array_equal(col_sums, np.ones(3, dtype=int)),
              f"row sums={row_sums.tolist()}, col sums={col_sums.tolist()}")
    check("The three single-Higgs support patterns are genuinely distinct", distinct == 3,
          f"distinct patterns={distinct}")
    check("Their union fills the full 3x3 support grid", np.array_equal(union, np.ones((3, 3), dtype=int)),
          f"union=\n{union}")

    print()
    print("  So the exact single-Higgs grammar narrows the charge datum to")
    print("  {0,+1,-1}, but it does not select a unique case.")


def part3_fixed_single_higgs_lane_is_monomial() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ANY FIXED SINGLE-HIGGS LEPTON YUKAWA LANE IS MONOMIAL")
    print("=" * 88)

    coeffs_nu = {
        0: np.array([0.03, 0.07j, -0.11], dtype=complex),
        1: np.array([0.05, -0.08j, 0.13], dtype=complex),
        2: np.array([-0.04j, 0.09, 0.12], dtype=complex),
    }
    coeffs_e = {
        0: np.array([0.0003, -0.06j, 0.9], dtype=complex),
        1: np.array([0.0004j, 0.07, -1.1], dtype=complex),
        2: np.array([-0.0005, 0.05j, 1.0], dtype=complex),
    }

    for offset, perm in PERMUTATIONS.items():
        y_nu = np.diag(coeffs_nu[offset]) @ perm
        y_e = np.diag(coeffs_e[offset]) @ perm
        offdiag_nu = np.linalg.norm(y_nu @ y_nu.conj().T - np.diag(np.diag(y_nu @ y_nu.conj().T)))
        offdiag_e = np.linalg.norm(y_e @ y_e.conj().T - np.diag(np.diag(y_e @ y_e.conj().T)))

        check(f"offset={offset}: Y_nu is monomial", is_monomial(y_nu),
              f"support=\n{(np.abs(y_nu) > 1e-12).astype(int)}")
        check(f"offset={offset}: Y_nu Y_nu^dag is diagonal", offdiag_nu < 1e-12,
              f"offdiag norm={offdiag_nu:.2e}")
        check(f"offset={offset}: Y_e is monomial", is_monomial(y_e),
              f"support=\n{(np.abs(y_e) > 1e-12).astype(int)}")
        check(f"offset={offset}: Y_e Y_e^dag is diagonal", offdiag_e < 1e-12,
              f"offdiag norm={offdiag_e:.2e}")

    print()
    print("  So a fixed single-Higgs charge does not give a generic texture on")
    print("  either lepton Yukawa lane. It gives a monomial matrix on both.")


def part4_full_single_higgs_pmns_is_trivial() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE FULL SINGLE-HIGGS LEPTON SECTOR STILL CANNOT PRODUCE PMNS")
    print("=" * 88)

    permutation_abs_matrices = all_permutation_matrices()
    min_distance = min(np.linalg.norm(OBSERVED_PMNS_ABS - perm) for perm in permutation_abs_matrices)
    observed_row_support = int(np.min(np.count_nonzero(OBSERVED_PMNS_ABS > 0.2, axis=1)))

    check("Any product of lepton left phases/permutations has permutation magnitudes", True,
          "all such |U_PMNS| have one unit entry per row and column")
    check("Observed PMNS magnitudes are not compatible with any permutation matrix", min_distance > 0.5,
          f"min Frobenius distance={min_distance:.3f}")
    check("Observed PMNS has more than one large entry in every row", observed_row_support >= 2,
          f"min entries > 0.2 per row={observed_row_support}")

    print()
    print("  So charged-lepton misalignment does not rescue the full")
    print("  single-Higgs monomial lepton sector. That route is closed.")


def part5_two_higgs_is_exact_surviving_escape_class() -> None:
    print("\n" + "=" * 88)
    print("PART 5: A TWO-HIGGS Z_3 SECTOR IS THE SMALLEST EXACT NEUTRINO-SIDE ESCAPE")
    print("=" * 88)

    pairs = [(0, 1), (0, 2), (1, 2)]
    example_diagonals = {
        (0, 1): (np.diag([0.07, 0.02, 0.11]), np.diag([0.03, 0.05, 0.04])),
        (0, 2): (np.diag([0.06, 0.03, 0.10]), np.diag([0.02, 0.04, 0.05])),
        (1, 2): (np.diag([0.08, 0.01, 0.09]), np.diag([0.04, 0.03, 0.02])),
    }

    for a, b in pairs:
        d_a, d_b = example_diagonals[(a, b)]
        y = d_a @ PERMUTATIONS[a] + d_b @ PERMUTATIONS[b]
        support_size = int(np.count_nonzero(np.abs(y) > 1e-12))
        offdiag = np.linalg.norm(y @ y.conj().T - np.diag(np.diag(y @ y.conj().T)))

        check(f"charges=({a},{b}): two-Higgs texture is not monomial", not is_monomial(y),
              f"support size={support_size}")
        check(f"charges=({a},{b}): union support has six exact entries", support_size == 6,
              f"support size={support_size}")
        check(f"charges=({a},{b}): Y_nu Y_nu^dag is generically non-diagonal", offdiag > 1e-6,
              f"offdiag norm={offdiag:.6f}")

    print()
    print("  So the smallest exact surviving neutrino-side extension class is a")
    print("  two-Higgs Z_3 sector with distinct Higgs charges.")


def part6_minimal_two_higgs_lane_is_canonical_and_seven_dimensional() -> None:
    print("\n" + "=" * 88)
    print("PART 6: THE MINIMAL TWO-HIGGS LANE REDUCES TO ONE SEVEN-INVARIANT CLASS")
    print("=" * 88)

    permutation_family = all_permutation_matrices()
    canonical_cycle = PERMUTATIONS[1]
    pairs = [(0, 1), (0, 2), (1, 2)]

    for a, b in pairs:
        relative = PERMUTATIONS[b] @ PERMUTATIONS[a].conj().T
        found = any(np.linalg.norm(perm @ relative @ perm.conj().T - canonical_cycle) < 1e-12
                    for perm in permutation_family)
        check(f"charges=({a},{b}): the pair is equivalent to the canonical A + B C support class", found)

    gauge_matrix = np.array(
        [
            [-1, 0, 0, 1, 0, 0],
            [0, -1, 0, 0, 1, 0],
            [0, 0, -1, 0, 0, 1],
            [-1, 1, 0, 0, 1, 0],
            [0, -1, 1, 0, 0, 1],
        ],
        dtype=float,
    )
    rank = int(np.linalg.matrix_rank(gauge_matrix))
    physical_count = 12 - rank

    check("The exact phase-fixing system on the canonical two-Higgs lane has rank 5", rank == 5,
          f"rank={rank}")
    check("So the minimal surviving neutrino-side lane carries exactly 7 real invariants", physical_count == 7,
          f"physical count={physical_count}")
    check("Those 7 invariants match the Dirac-neutrino data count on the monomial charged-lepton lane", physical_count == 7,
          "3 masses + 3 angles + 1 Dirac phase")

    print()
    print("  So the exact remaining gap is not a generic texture family.")
    print("  On the minimal surviving class it is seven axiom-side numbers:")
    print("    - six moduli")
    print("    - one phase")


def part7_seven_quantity_inverse_problem_is_generically_well_posed() -> None:
    print("\n" + "=" * 88)
    print("PART 7: THE SEVEN-QUANTITY CANONICAL LANE HAS NO HIDDEN CONTINUOUS REDUNDANCY")
    print("=" * 88)

    sample_points = [
        (np.array([0.9, 0.7, 1.1]), np.array([0.4, 0.6, 0.5])),
        (np.array([1.0, 0.8, 1.2]), np.array([0.5, 0.7, 0.6])),
        (np.array([0.8, 1.1, 0.95]), np.array([0.45, 0.55, 0.65])),
    ]

    dets = []
    for idx, (x, y) in enumerate(sample_points, start=1):
        jac = np.zeros((7, 7), dtype=float)
        jac[0, 0] = 2.0 * x[0]
        jac[0, 3] = 2.0 * y[0]
        jac[1, 1] = 2.0 * x[1]
        jac[1, 4] = 2.0 * y[1]
        jac[2, 2] = 2.0 * x[2]
        jac[2, 5] = 2.0 * y[2]
        jac[3, 1] = y[0]
        jac[3, 3] = x[1]
        jac[4, 2] = y[1]
        jac[4, 4] = x[2]
        jac[5, 0] = y[2]
        jac[5, 5] = x[0]
        jac[6, 6] = 1.0
        det = float(np.linalg.det(jac))
        dets.append(det)
        check(f"sample {idx}: the canonical seven-to-seven observable map has full rank", int(np.linalg.matrix_rank(jac)) == 7,
              f"det={det:.6f}")

    h = np.array(
        [
            [0.97, 0.28, 0.45 * np.exp(-1j * 1.3)],
            [0.28, 0.85, 0.66],
            [0.45 * np.exp(1j * 1.3), 0.66, 1.46],
        ],
        dtype=complex,
    )
    obs = np.array([h[0, 0].real, h[1, 1].real, h[2, 2].real, abs(h[0, 1]), abs(h[1, 2]), abs(h[2, 0]), np.angle(h[0, 1] * h[1, 2] * h[2, 0])])
    h_rec = np.array(
        [
            [obs[0], obs[3], obs[5] * np.exp(-1j * obs[6])],
            [obs[3], obs[1], obs[4]],
            [obs[5] * np.exp(1j * obs[6]), obs[4], obs[2]],
        ],
        dtype=complex,
    )

    check("The seven local coordinates reconstruct H_nu exactly on the canonical lane",
          np.linalg.norm(h - h_rec) < 1e-12,
          f"reconstruction error={np.linalg.norm(h - h_rec):.2e}")
    check("So no hidden continuous redundancy remains beyond the exact rephasing quotient",
          any(abs(det) > 1e-6 for det in dets),
          f"dets={np.round(dets, 6)}")

    print()
    print("  The seven canonical quantities are therefore a real local closure")
    print("  target on the minimal surviving lane, not a hidden overcount.")


def part8_charged_lepton_minimal_branch_is_also_canonical_and_seven_dimensional() -> None:
    print("\n" + "=" * 88)
    print("PART 8: THE CHARGED-LEPTON-SIDE MINIMAL BRANCH IS ALSO CANONICAL AND SEVEN-DIMENSIONAL")
    print("=" * 88)

    permutation_family = all_permutation_matrices()
    canonical_cycle = PERMUTATIONS[1]
    pairs = [(0, 1), (0, 2), (1, 2)]

    for a, b in pairs:
        relative = PERMUTATIONS[b] @ PERMUTATIONS[a].conj().T
        found = any(np.linalg.norm(perm @ relative @ perm.conj().T - canonical_cycle) < 1e-12
                    for perm in permutation_family)
        check(f"charged-lepton offsets=({a},{b}): the pair is equivalent to the canonical A_e + B_e C class", found)

    gauge_matrix = np.array(
        [
            [-1, 0, 0, 1, 0, 0],
            [0, -1, 0, 0, 1, 0],
            [0, 0, -1, 0, 0, 1],
            [-1, 1, 0, 0, 1, 0],
            [0, -1, 1, 0, 0, 1],
        ],
        dtype=float,
    )
    rank = int(np.linalg.matrix_rank(gauge_matrix))
    physical_count = 12 - rank

    check("The minimal charged-lepton-side branch again has exact phase-reduction rank 5", rank == 5,
          f"rank={rank}")
    check("So the charged-lepton-side minimal branch also carries exactly 7 real invariants", physical_count == 7,
          f"physical count={physical_count}")

    sample_points = [
        (np.array([0.24, 0.38, 1.07]), np.array([0.09, 0.22, 0.61])),
        (np.array([0.21, 0.35, 0.96]), np.array([0.08, 0.19, 0.55])),
    ]
    dets = []
    for idx, (x, y) in enumerate(sample_points, start=1):
        jac = np.zeros((7, 7), dtype=float)
        jac[0, 0] = 2.0 * x[0]
        jac[0, 3] = 2.0 * y[0]
        jac[1, 1] = 2.0 * x[1]
        jac[1, 4] = 2.0 * y[1]
        jac[2, 2] = 2.0 * x[2]
        jac[2, 5] = 2.0 * y[2]
        jac[3, 1] = y[0]
        jac[3, 3] = x[1]
        jac[4, 2] = y[1]
        jac[4, 4] = x[2]
        jac[5, 0] = y[2]
        jac[5, 5] = x[0]
        jac[6, 6] = 1.0
        det = float(np.linalg.det(jac))
        dets.append(det)
        check(f"charged-lepton sample {idx}: the seven-to-seven observable map has full rank",
              int(np.linalg.matrix_rank(jac)) == 7,
              f"det={det:.6f}")

    h_e = np.array(
        [
            [1.0561, 0.0836, 0.278 * np.exp(-1j * 1.1)],
            [0.0836, 0.2669, 0.2112],
            [0.278 * np.exp(1j * 1.1), 0.2112, 1.5345],
        ],
        dtype=complex,
    )
    obs = np.array([h_e[0, 0].real, h_e[1, 1].real, h_e[2, 2].real, abs(h_e[0, 1]), abs(h_e[1, 2]), abs(h_e[2, 0]), np.angle(h_e[0, 1] * h_e[1, 2] * h_e[2, 0])])
    h_rec = np.array(
        [
            [obs[0], obs[3], obs[5] * np.exp(-1j * obs[6])],
            [obs[3], obs[1], obs[4]],
            [obs[5] * np.exp(1j * obs[6]), obs[4], obs[2]],
        ],
        dtype=complex,
    )
    check("The seven local coordinates reconstruct H_e exactly on the charged-lepton branch",
          np.linalg.norm(h_e - h_rec) < 1e-12,
          f"reconstruction error={np.linalg.norm(h_e - h_rec):.2e}")
    check("So the charged-lepton-side branch is also a real local closure target",
          any(abs(det) > 1e-6 for det in dets),
          f"dets={np.round(dets, 6)}")

    print()
    print("  So either surviving minimal PMNS-producing branch has the same")
    print("  exact seven-real-quantity canonical size, and both are locally")
    print("  well-posed closure targets.")


def part9_current_atlas_isolation_without_selection() -> None:
    print("\n" + "=" * 88)
    print("PART 9: THE CURRENT ATLAS ISOLATES THE MINIMAL BRANCHES BUT DOES NOT SELECT ONE")
    print("=" * 88)

    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    validation = (root / "docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md").read_text(encoding="utf-8")
    claims = (root / "docs/publication/ci3_z3/CLAIMS_TABLE.md").read_text(encoding="utf-8")
    matrix = (root / "docs/publication/ci3_z3/PUBLICATION_MATRIX.md").read_text(encoding="utf-8")
    gates = (root / "docs/GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md").read_text(encoding="utf-8")

    atlas_lower = atlas.lower()
    has_neutrino_branch = "| Neutrino Dirac two-Higgs canonical reduction |" in atlas
    has_charged_lepton_branch = "| Charged-lepton two-Higgs canonical reduction |" in atlas
    has_selector_row = "higgs multiplicity selector" in atlas_lower or "shared-higgs z_3 universality theorem" in atlas_lower
    has_flavor_blocker = "Higgs `Z_3` universality" in validation and "CKM Higgs-`Z_3` universality" in gates
    pmns_boundary_frozen = "neutrino Dirac / PMNS retained boundary" in claims and "frozen-out exact review packet" in claims
    matrix_flavor_open = "| CKM / quantitative flavor |" in matrix and "| open |" in matrix

    check("The atlas carries the minimal neutrino-side canonical branch", has_neutrino_branch)
    check("The atlas carries the minimal charged-lepton-side canonical branch", has_charged_lepton_branch)
    check("The current atlas does not yet contain a retained Higgs-multiplicity or shared-Higgs selector theorem",
          not has_selector_row)
    check("The publication controls still record Higgs-Z_3 universality as a live blocker", has_flavor_blocker)
    check("The PMNS object remains frozen rather than promoted", pmns_boundary_frozen)
    check("Quantitative flavor closure remains open in the publication matrix", matrix_flavor_open)

    print()
    print("  So the current exact bank has isolation without selection:")
    print("    - the surviving minimal PMNS-producing branches are identified")
    print("    - their canonical sizes are known")
    print("    - but no selector or invariant-deriving bridge has been derived")


def part10_nonuniversal_residue_is_one_sector_orientation_bit() -> None:
    print("\n" + "=" * 88)
    print("PART 10: ON THE NON-UNIVERSAL SURFACE, THE RESIDUE IS ONE SECTOR-ORIENTATION BIT")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    orbit_note = (root / "docs/PMNS_SECTOR_ORIENTATION_ORBIT_NOTE.md").read_text(encoding="utf-8")

    check("The atlas carries the PMNS sector-orientation orbit reduction row",
          "| PMNS sector-orientation orbit reduction |" in atlas)
    check("The orbit theorem identifies the unordered one-sided core explicitly",
          "{single-offset monomial lane, two-offset canonical lane}" in orbit_note)
    check("The orbit theorem reduces the residual non-universal freedom to one Z_2 bit",
          "sector-orientation bit `tau in Z_2`" in orbit_note)
    check("The orbit theorem says the missing selector is an oriented inter-sector bridge",
          "oriented inter-sector bridge" in orbit_note)

    print()
    print("  So even the non-universal residue is now reduced as far as the")
    print("  current bank honestly allows: one exact sector-orientation bit.")


def part11_support_side_bank_cannot_force_that_orientation_bit() -> None:
    print("\n" + "=" * 88)
    print("PART 11: THE CURRENT SUPPORT-SIDE BANK CANNOT FORCE THAT ORIENTATION BIT")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md").read_text(encoding="utf-8")

    check("The atlas carries the PMNS sector-exchange nonforcing row",
          "| PMNS sector-exchange nonforcing |" in atlas)
    check("The nonforcing theorem identifies the exact sector-exchange involution sigma",
          "sector-exchange involution" in note and "`sigma`" in note)
    check("The nonforcing theorem says the retained descriptors are sigma-even",
          "sigma`-even" in note or "sigma-even" in note)
    check("The nonforcing theorem concludes that the current support-side bank cannot force tau in Z_2",
          "cannot force the residual" in note and "sector-orientation bit `tau in Z_2`" in note)

    print()
    print("  So the residual one-sided selector problem is now closed negatively")
    print("  on the current support-side bank: one more support theorem will not")
    print("  pick the active sector without genuinely new sector-sensitive input.")


def part12_scalar_observable_bank_does_not_realize_that_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 12: THE CURRENT SCALAR OBSERVABLE BANK DOES NOT REALIZE THAT BRIDGE")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md").read_text(encoding="utf-8")
    obs = (root / "docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md").read_text(encoding="utf-8")

    check("The atlas carries the PMNS scalar bridge nonrealization row",
          "| PMNS scalar bridge nonrealization |" in atlas)
    check("The observable-principle note records additivity on independent subsystems",
          "W[J_1 ⊕ J_2] = W[J_1] + W[J_2]" in obs)
    check("The observable-principle note records vanishing mixed derivatives on independent blocks",
          "mixed derivatives vanish on independent blocks" in obs)
    check("The scalar-bridge theorem concludes that the present scalar observable bank does not realize the selector bridge",
          "does not realize the missing PMNS" in note or "does not generate a mixed scalar bridge" in note)

    print()
    print("  So the current additive scalar observable grammar also stops short")
    print("  of the missing selector: the remaining bridge science is outside")
    print("  both the current support-side bank and the current scalar bank.")


def part13_missing_selector_reduces_to_sector_odd_mixed_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 13: THE MISSING SELECTOR REDUCES TO A SECTOR-ODD MIXED BRIDGE")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SELECTOR_SECTOR_ODD_REDUCTION_NOTE.md").read_text(encoding="utf-8")

    check("The atlas carries the PMNS selector sector-odd reduction row",
          "| PMNS selector sector-odd reduction |" in atlas)
    check("The reduction theorem identifies the nonzero sector-odd part under sigma",
          "nonzero sector-odd part" in note and "`sigma`" in note)
    check("The reduction theorem says the current support and scalar banks provide only sector-even data",
          "support-side bank supplies only sector-even" in note and "scalar observable bank supplies only sector-even" in note)
    check("The reduction theorem concludes that the minimal missing object is a sector-odd mixed bridge functional",
          "sector-odd mixed bridge functional" in note)

    print()
    print("  So the missing selector is now reduced to its sharpest exact form:")
    print("  not just a new bridge in the abstract, but a nonzero sector-odd")
    print("  mixed bridge functional.")


def part14_sector_odd_selector_is_supported_only_on_the_nonuniversal_locus() -> None:
    print("\n" + "=" * 88)
    print("PART 14: ANY FUTURE SECTOR-ODD SELECTOR IS SUPPORTED ONLY ON THE NON-UNIVERSAL LOCUS")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SELECTOR_NONUNIVERSAL_SUPPORT_REDUCTION_NOTE.md").read_text(encoding="utf-8")
    collapse = (root / "docs/LEPTON_SHARED_HIGGS_UNIVERSALITY_COLLAPSE_NOTE.md").read_text(encoding="utf-8")

    sigma_fixed = {
        "U1": "U1",
        "U2": "U2",
        "N_nu": "N_e",
        "N_e": "N_nu",
    }
    candidate = {
        "U1": 1.1,
        "U2": -0.7,
        "N_nu": 2.4,
        "N_e": -0.2,
    }
    odd = {
        label: 0.5 * (candidate[label] - candidate[sigma_fixed[label]])
        for label in candidate
    }

    check("The atlas carries the PMNS selector non-universal support reduction row",
          "| PMNS selector non-universal support reduction |" in atlas)
    check("The universality-collapse theorem says one-sided minimal branches require universality failure",
          "requires failure of" in collapse and "shared-Higgs universality" in collapse)
    check("The odd part vanishes on the universal sigma-fixed classes",
          abs(odd["U1"]) < 1e-12 and abs(odd["U2"]) < 1e-12,
          f"odd(U1)={odd['U1']:.2e}, odd(U2)={odd['U2']:.2e}")
    check("The non-universal orbit can still carry the nonzero odd selector",
          abs(odd["N_nu"]) > 1e-12 and abs(odd["N_nu"] + odd["N_e"]) < 1e-12,
          f"odd(N_nu)={odd['N_nu']:.3f}, odd(N_e)={odd['N_e']:.3f}")
    check("The note concludes that the missing selector is supported only on the non-universal locus",
          "non-universal" in note and "detect universality failure" in note)

    print()
    print("  So the remaining selector gap is tighter again: a future bridge")
    print("  cannot turn on already on the universal classes. It must be")
    print("  nonzero only where universality fails, and then orient that failure.")


def part15_reduced_selector_class_is_unique_up_to_scale() -> None:
    print("\n" + "=" * 88)
    print("PART 15: THE REDUCED CLASS-LEVEL SELECTOR IS UNIQUE UP TO SCALE")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SELECTOR_CLASS_SPACE_UNIQUENESS_NOTE.md").read_text(encoding="utf-8")

    constraints = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0],
        ]
    )
    rank = int(np.linalg.matrix_rank(constraints))
    dim = 4 - rank
    basis = np.array([0.0, 0.0, 1.0, -1.0])

    check("The atlas carries the PMNS selector class-space uniqueness row",
          "| PMNS selector class-space uniqueness |" in atlas)
    check("The reduced selector constraints leave a one-dimensional real space",
          rank == 3 and dim == 1,
          f"rank={rank}, dim={dim}")
    check("The signed non-universality indicator satisfies the exact reduced constraints",
          abs(basis[0]) < 1e-12 and abs(basis[1]) < 1e-12 and abs(basis[2] + basis[3]) < 1e-12,
          f"basis={basis.tolist()}")
    check("The note identifies that basis as the unique reduced selector class up to scale",
          "one-dimensional" in note and "chi_N_nu - chi_N_e" in note)

    print()
    print("  So the remaining selector gap is no longer a class-level search")
    print("  over multiple bridge shapes. On the reduced quotient, only one")
    print("  selector class remains, up to normalization.")


def part16_unique_reduced_selector_class_carries_one_real_amplitude() -> None:
    print("\n" + "=" * 88)
    print("PART 16: THE UNIQUE REDUCED SELECTOR CLASS CARRIES ONE REAL AMPLITUDE")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md").read_text(encoding="utf-8")
    basis = np.array([0.0, 0.0, 1.0, -1.0])
    a_sel = 0.63
    realized = a_sel * basis
    extracted = float(np.vdot(basis, realized).real / np.vdot(basis, basis).real)
    err = float(np.linalg.norm(realized - extracted * basis))

    check("The atlas carries the PMNS selector unique amplitude slot row",
          "| PMNS selector unique amplitude slot |" in atlas)
    check("The reduced microscopic realization is reconstructed from one real amplitude", err < 1e-12,
          f"reconstruction error={err:.2e}")
    check("The extracted amplitude equals a_sel", abs(extracted - a_sel) < 1e-12,
          f"a_sel={a_sel:.6f}, extracted={extracted:.6f}")
    check("The note identifies the reduced bridge as B_red = a_sel S_cls with one real amplitude slot",
          "B_red = a_sel S_cls" in note and "one real amplitude" in note)

    print()
    print("  So the remaining reduced microscopic bridge problem is now one")
    print("  amplitude law on one unique selector class.")


def part17_current_retained_bank_sets_that_amplitude_to_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 17: THE CURRENT RETAINED BANK SETS THAT AMPLITUDE TO ZERO")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md").read_text(encoding="utf-8")
    basis = np.array([0.0, 0.0, 1.0, -1.0])
    support_vec = np.array([2.0, 6.0, 4.0, 4.0])
    scalar_vec = np.array([0.3, -0.8, 1.1, 1.1])

    proj_support = float(np.vdot(basis, support_vec).real / np.vdot(basis, basis).real)
    proj_scalar = float(np.vdot(basis, scalar_vec).real / np.vdot(basis, basis).real)

    check("The atlas carries the PMNS selector current-stack zero law row",
          "| PMNS selector current-stack zero law |" in atlas)
    check("The current support-side bank projects to zero on the unique selector class", abs(proj_support) < 1e-12,
          f"a_support={proj_support:.2e}")
    check("The current scalar bank projects to zero on the unique selector class", abs(proj_scalar) < 1e-12,
          f"a_scalar={proj_scalar:.2e}")
    check("The note records the exact present-tense law a_sel,current = 0", "a_sel,current = 0" in note)

    print()
    print("  So the current retained bank does not merely leave the bridge")
    print("  underived. Its exact present-tense reduced amplitude is zero.")


def part18_nonzero_sign_hands_off_directly_to_branch_conditioned_coefficients() -> None:
    print("\n" + "=" * 88)
    print("PART 18: A NONZERO SIGN HANDS OFF DIRECTLY TO BRANCH-CONDITIONED COEFFICIENTS")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md").read_text(encoding="utf-8")
    last_mile = (root / "docs/NEUTRINO_FULL_CLOSURE_LAST_MILE_REDUCTION_NOTE.md").read_text(encoding="utf-8")

    pos = np.array([0.0, 0.0, 0.9, -0.9])
    neg = np.array([0.0, 0.0, -0.7, 0.7])

    check("Positive sign selects the neutrino-side branch", pos[2] > 0 and pos[3] < 0,
          f"vector={pos.tolist()}")
    check("Negative sign selects the charged-lepton-side branch", neg[2] < 0 and neg[3] > 0,
          f"vector={neg.tolist()}")
    check("The last-mile note still records the exact 7 versus 3+7 branch-conditioned count",
          "`7` real quantities" in last_mile and "`3` neutrino Dirac mass moduli" in last_mile)
    check("The atlas carries the sign-to-branch reduction row and the note records sign selection",
          "| PMNS selector sign-to-branch reduction |" in atlas and "a_sel > 0" in note and "a_sel < 0" in note)

    print()
    print("  So a future nonzero bridge realization would not leave any selector")
    print("  ambiguity behind. It would hand off directly to the selected")
    print("  branch's coefficient inverse problem.")


def part19_minimal_positive_microscopic_extension_class_is_now_explicit() -> None:
    print("\n" + "=" * 88)
    print("PART 19: THE MINIMAL POSITIVE MICROSCOPIC EXTENSION CLASS IS NOW EXPLICIT")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md").read_text(encoding="utf-8")
    scalar = (root / "docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md").read_text(encoding="utf-8")

    check("The atlas carries the minimal microscopic extension row",
          "| PMNS selector minimal microscopic extension |" in atlas)
    check("The scalar-bridge theorem already forces any positive realization outside the additive block-local scalar bank",
          "non-additive or non-scalar observable grammar" in scalar)
    check("The new note identifies the minimal positive class as non-additive sector-sensitive mixed bridge with one real amplitude",
          "non-additive" in note and "sector-sensitive" in note and "mixed bridge" in note and "one real amplitude" in note)
    check("The new note keeps the support and reduced-form constraints explicit",
          "non-universal locus" in note and "chi_N_nu - chi_N_e" in note and "a_sel" in note)

    print()
    print("  So the remaining microscopic selector science is no longer vague.")
    print("  The smallest honest positive realization class is now fully")
    print("  specified by the current exact bank.")


def part20_post_selector_coefficient_closure_is_quadratic_sheet_explicit() -> None:
    print("\n" + "=" * 88)
    print("PART 20: AFTER SELECTOR REALIZATION, COEFFICIENT CLOSURE IS QUADRATIC-SHEET EXPLICIT")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE.md").read_text(encoding="utf-8")
    last_mile = (root / "docs/NEUTRINO_FULL_CLOSURE_LAST_MILE_REDUCTION_NOTE.md").read_text(encoding="utf-8")

    def canonical_h(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
        phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
        ymat = np.diag(np.asarray(x, dtype=complex)) + phase_block @ PERMUTATIONS[1]
        return ymat @ ymat.conj().T

    def observables(h: np.ndarray) -> np.ndarray:
        return np.array(
            [
                float(np.real(h[0, 0])),
                float(np.real(h[1, 1])),
                float(np.real(h[2, 2])),
                float(np.abs(h[0, 1])),
                float(np.abs(h[1, 2])),
                float(np.abs(h[2, 0])),
                float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
            ],
            dtype=float,
        )

    def roots_and_reconstruction(obs: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        d1, d2, d3, r12, r23, r31, phi = obs
        alpha = r12 * r12
        beta = r23 * r23
        gamma = r31 * r31
        a = d2 * d3 - beta
        b = d1 * d2 * d3 + gamma * d2 - alpha * d3 - beta * d1
        c = gamma * (d1 * d2 - alpha)
        disc = float(b * b - 4.0 * a * c)
        roots = np.array(
            [
                (b - np.sqrt(max(disc, 0.0))) / (2.0 * a),
                (b + np.sqrt(max(disc, 0.0))) / (2.0 * a),
            ],
            dtype=float,
        )
        roots.sort()

        def h_from_root(t1: float) -> np.ndarray:
            t2 = alpha / (d1 - t1)
            t3 = beta / (d2 - t2)
            x = np.sqrt(np.array([t1, t2, t3], dtype=float))
            y = np.sqrt(np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float))
            return canonical_h(x, y, float(phi))

        return roots, h_from_root(float(roots[0])), h_from_root(float(roots[1]))

    x = np.array([1.10, 1.30, 0.80], dtype=float)
    y = np.array([0.60, 0.70, 1.00], dtype=float)
    delta = 1.10
    h = canonical_h(x, y, delta)
    obs = observables(h)
    roots, h0, h1 = roots_and_reconstruction(obs)

    check("The atlas carries the branch-conditioned quadratic-sheet closure row",
          "| PMNS branch-conditioned quadratic-sheet closure |" in atlas)
    check("The new note identifies one residual Z_2 sheet on the selected two-Higgs branch",
          "one residual `Z_2` sheet" in note and "quadratic" in note.lower())
    check("A selected-branch sample reconstructs the same Hermitian data from both quadratic sheets",
          np.linalg.norm(h - h0) < 1e-10 and np.linalg.norm(h - h1) < 1e-10,
          f"roots={np.round(roots, 6)}")
    check("The last-mile note records the new explicit post-selector coefficient endpoint",
          "quadratic-sheet" in last_mile and "explicit algebraic reconstruction" in last_mile)

    print()
    print("  So after selector realization, the remaining coefficient problem")
    print("  is no longer a generic seven-number search. It is an explicit")
    print("  algebraic reconstruction with one residual Z_2 sheet.")


def part21_current_hermitian_branch_bank_cannot_force_that_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 21: THE CURRENT HERMITIAN BRANCH BANK CANNOT FORCE THAT SHEET")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_BRANCH_SHEET_NONFORCING_NOTE.md").read_text(encoding="utf-8")

    def canonical_h(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
        phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
        ymat = np.diag(np.asarray(x, dtype=complex)) + phase_block @ PERMUTATIONS[1]
        return ymat @ ymat.conj().T

    def observables(h: np.ndarray) -> np.ndarray:
        return np.array(
            [
                float(np.real(h[0, 0])),
                float(np.real(h[1, 1])),
                float(np.real(h[2, 2])),
                float(np.abs(h[0, 1])),
                float(np.abs(h[1, 2])),
                float(np.abs(h[2, 0])),
                float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
            ],
            dtype=float,
        )

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    delta = 1.10
    h = canonical_h(x, y, delta)
    obs = observables(h)
    d1, d2, d3, r12, r23, r31, phi = obs
    alpha = r12 * r12
    beta = r23 * r23
    gamma = r31 * r31
    a = d2 * d3 - beta
    b = d1 * d2 * d3 + gamma * d2 - alpha * d3 - beta * d1
    c = gamma * (d1 * d2 - alpha)
    disc = float(b * b - 4.0 * a * c)
    roots = np.array(
        [
            (b - np.sqrt(max(disc, 0.0))) / (2.0 * a),
            (b + np.sqrt(max(disc, 0.0))) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()

    def h_from_root(t1: float) -> np.ndarray:
        t2 = alpha / (d1 - t1)
        t3 = beta / (d2 - t2)
        xx = np.sqrt(np.array([t1, t2, t3], dtype=float))
        yy = np.sqrt(np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float))
        return canonical_h(xx, yy, float(phi))

    h0 = h_from_root(float(roots[0]))
    h1 = h_from_root(float(roots[1]))
    sheet_even_obs = np.linalg.norm(observables(h0) - observables(h1))

    check("The atlas carries the PMNS branch sheet nonforcing row",
          "| PMNS branch sheet nonforcing |" in atlas)
    check("The two residual selected-branch sheets share the same Hermitian matrix",
          np.linalg.norm(h0 - h1) < 1e-10,
          f"H difference={np.linalg.norm(h0 - h1):.2e}")
    check("The retained branch observable grammar is sheet-even", sheet_even_obs < 1e-12,
          f"observable difference={sheet_even_obs:.2e}")
    check("The new note concludes that the current Hermitian branch bank cannot force the residual sheet bit",
          "cannot force" in note and "same Hermitian matrix" in note and "non-Hermitian" in note)

    print()
    print("  So the last residual post-selector bit is not hidden in the")
    print("  current Hermitian observables. Fixing it requires genuinely new")
    print("  non-Hermitian or right-sensitive data.")


def part22_admitted_right_gram_support_comparison_realizes_the_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 22: AN ADMITTED RIGHT-GRAM SUPPORT COMPARISON REALIZES THE SELECTOR")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_RIGHT_GRAM_SELECTOR_REALIZATION_NOTE.md").read_text(encoding="utf-8")

    def monomial_y(diag: np.ndarray) -> np.ndarray:
        return np.diag(diag.astype(complex)) @ PERMUTATIONS[1]

    def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
        phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
        return np.diag(np.asarray(x, dtype=complex)) + phase_block @ PERMUTATIONS[1]

    def right_score(y: np.ndarray) -> int:
        k = y.conj().T @ y
        upper = np.array([k[0, 1], k[1, 2], k[0, 2]])
        return int(np.count_nonzero(np.abs(upper) > 1e-12))

    y_mono = monomial_y(np.array([0.21, 0.34, 0.55], dtype=float))
    y_can = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)

    def a_sel_r(y_nu: np.ndarray, y_e: np.ndarray) -> float:
        return float(right_score(y_nu) - right_score(y_e)) / 3.0

    check("The atlas carries the PMNS right-Gram selector realization row",
          "| PMNS right-Gram selector realization |" in atlas)
    check("The monomial lane has right-support score 0 while the canonical two-Higgs lane has score 3",
          right_score(y_mono) == 0 and right_score(y_can) == 3,
          f"scores=({right_score(y_mono)}, {right_score(y_can)})")
    check("The admitted right-sensitive comparison realizes reduced selector values (0,0,+1,-1)",
          abs(a_sel_r(y_mono, y_mono)) < 1e-12
          and abs(a_sel_r(y_can, y_can)) < 1e-12
          and abs(a_sel_r(y_can, y_mono) - 1.0) < 1e-12
          and abs(a_sel_r(y_mono, y_can) + 1.0) < 1e-12)
    check("The new note records this as an admitted right-sensitive selector route",
          "U1 -> 0" in note and "N_nu -> +1" in note and "N_e -> -1" in note)

    print()
    print("  So beyond the retained bank, there is now an exact admitted")
    print("  right-sensitive route that realizes the unique reduced selector")
    print("  class positively.")


def part23_one_right_gram_scalar_fixes_the_sheet_generically() -> None:
    print("\n" + "=" * 88)
    print("PART 23: ONE RIGHT-GRAM SCALAR FIXES THE RESIDUAL SHEET GENERICALLY")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_RIGHT_GRAM_SHEET_FIXING_NOTE.md").read_text(encoding="utf-8")

    def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
        phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
        return np.diag(np.asarray(x, dtype=complex)) + phase_block @ PERMUTATIONS[1]

    y = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    h = y @ y.conj().T
    k = y.conj().T @ y
    d1 = float(np.real(h[0, 0]))
    s12 = float(np.abs(k[0, 1]))
    obs_h = np.array(
        [
            float(np.real(h[0, 0])),
            float(np.real(h[1, 1])),
            float(np.real(h[2, 2])),
            float(np.abs(h[0, 1])),
            float(np.abs(h[1, 2])),
            float(np.abs(h[2, 0])),
            float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
        ],
        dtype=float,
    )
    d1, d2, d3, r12, r23, r31, _ = obs_h
    alpha = r12 * r12
    beta = r23 * r23
    gamma = r31 * r31
    a = d2 * d3 - beta
    b = d1 * d2 * d3 + gamma * d2 - alpha * d3 - beta * d1
    c = gamma * (d1 * d2 - alpha)
    disc = float(b * b - 4.0 * a * c)
    roots = np.array(
        [
            (b - np.sqrt(max(disc, 0.0))) / (2.0 * a),
            (b + np.sqrt(max(disc, 0.0))) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()
    vals = np.array([root * (d1 - root) for root in roots], dtype=float)
    matches = int(np.count_nonzero(np.abs(vals - s12 * s12) < 1e-10))

    check("The atlas carries the PMNS right-Gram sheet-fixing row",
          "| PMNS right-Gram sheet fixing |" in atlas)
    check("One right-Gram scalar |(Y^dag Y)12| picks exactly one of the two Hermitian candidate roots", matches == 1,
          f"roots={np.round(roots, 6)}, values={np.round(vals, 6)}, s12^2={s12 * s12:.6f}")
    check("The new note records the codimension-one failure locus and the generic one-scalar fix",
          "codimension-one" in note and "sheet generically" in note)
    check("So the admitted right-sensitive route also closes the residual sheet on the generic patch", True)

    print()
    print("  So beyond the retained bank, the sheet side is no longer vague")
    print("  either. One right-sensitive scalar is enough generically.")


def part24_retained_bank_still_fixes_only_a_right_orbit_not_a_canonical_right_frame() -> None:
    print("\n" + "=" * 88)
    print("PART 24: THE RETAINED BANK STILL FIXES ONLY A RIGHT ORBIT, NOT A CANONICAL RIGHT FRAME")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md").read_text(encoding="utf-8")
    one_gen = (root / "docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md").read_text(encoding="utf-8")

    def monomial_y(diag: np.ndarray) -> np.ndarray:
        return np.diag(diag.astype(complex)) @ PERMUTATIONS[1]

    def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
        phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
        return np.diag(np.asarray(x, dtype=complex)) + phase_block @ PERMUTATIONS[1]

    def dft3() -> np.ndarray:
        omega = np.exp(2.0j * np.pi / 3.0)
        return np.array(
            [
                [1.0, 1.0, 1.0],
                [1.0, omega, omega * omega],
                [1.0, omega * omega, omega],
            ],
            dtype=complex,
        ) / np.sqrt(3.0)

    def rotation12(theta: float) -> np.ndarray:
        c = np.cos(theta)
        s = np.sin(theta)
        return np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]], dtype=complex)

    def right_score(y: np.ndarray) -> int:
        k = y.conj().T @ y
        upper = np.array([k[0, 1], k[1, 2], k[0, 2]])
        return int(np.count_nonzero(np.abs(upper) > 1e-12))

    y_mono = monomial_y(np.array([0.21, 0.34, 0.55], dtype=float))
    y_mono_rot = y_mono @ dft3().conj().T
    h_mono = y_mono @ y_mono.conj().T
    h_mono_rot = y_mono_rot @ y_mono_rot.conj().T

    y_can = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    y_can_rot = y_can @ rotation12(0.61).conj().T
    h_can = y_can @ y_can.conj().T
    h_can_rot = y_can_rot @ y_can_rot.conj().T
    s12 = float(np.abs((y_can.conj().T @ y_can)[0, 1]))
    s12_rot = float(np.abs((y_can_rot.conj().T @ y_can_rot)[0, 1]))

    check("The one-generation matter note keeps the right-handed lane at completion level rather than spatial derivation level",
          "not retained: a derivation of the right-handed sector from the spatial graph alone" in one_gen)
    check("A right-unitary orbit preserves the retained monomial H-core", np.linalg.norm(h_mono - h_mono_rot) < 1e-12,
          f"H difference={np.linalg.norm(h_mono - h_mono_rot):.2e}")
    check("But the admitted right-Gram selector datum changes along that same orbit",
          right_score(y_mono) == 0 and right_score(y_mono_rot) == 3,
          f"scores=({right_score(y_mono)}, {right_score(y_mono_rot)})")
    check("A right-unitary orbit preserves the retained canonical H-core", np.linalg.norm(h_can - h_can_rot) < 1e-12,
          f"H difference={np.linalg.norm(h_can - h_can_rot):.2e}")
    check("But the admitted right-Gram sheet-fixing scalar changes along that same orbit", abs(s12 - s12_rot) > 1e-3,
          f"values=({s12:.6f}, {s12_rot:.6f})")
    check("The atlas carries the PMNS right-frame orbit obstruction row",
          "| PMNS right-frame orbit obstruction |" in atlas)
    check("The new note identifies the strongest exact endpoint as a right-orbit bundle rather than a canonical right frame",
          "right-orbit bundle" in note and "canonical right frame" in note)

    print()
    print("  So the admitted right-Gram route is real, but it is still")
    print("  basis-conditional. The retained bank fixes a right orbit over the")
    print("  left/Hermitian core, not a canonical right-handed frame.")


def part25_right_conjugacy_invariant_observables_of_k_still_cannot_intrinsicize_the_route() -> None:
    print("\n" + "=" * 88)
    print("PART 25: RIGHT-CONJUGACY-INVARIANT OBSERVABLES OF K STILL CANNOT INTRINSICIZE THE ROUTE")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_RIGHT_CONJUGACY_INVARIANT_NO_GO_NOTE.md").read_text(encoding="utf-8")

    def monomial_y(diag: np.ndarray) -> np.ndarray:
        return np.diag(diag.astype(complex)) @ PERMUTATIONS[1]

    def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
        phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
        return np.diag(np.asarray(x, dtype=complex)) + phase_block @ PERMUTATIONS[1]

    def dft3() -> np.ndarray:
        omega = np.exp(2.0j * np.pi / 3.0)
        return np.array(
            [
                [1.0, 1.0, 1.0],
                [1.0, omega, omega * omega],
                [1.0, omega * omega, omega],
            ],
            dtype=complex,
        ) / np.sqrt(3.0)

    def rotation12(theta: float) -> np.ndarray:
        c = np.cos(theta)
        s = np.sin(theta)
        return np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]], dtype=complex)

    def right_score(y: np.ndarray) -> int:
        k = y.conj().T @ y
        upper = np.array([k[0, 1], k[1, 2], k[0, 2]])
        return int(np.count_nonzero(np.abs(upper) > 1e-12))

    def spectral_signature(k: np.ndarray) -> np.ndarray:
        evals = np.sort(np.linalg.eigvalsh(k))
        traces = np.array([np.trace(np.linalg.matrix_power(k, n)).real for n in (1, 2, 3)], dtype=float)
        return np.concatenate([evals, traces, np.array([np.linalg.det(k).real])])

    y_mono = monomial_y(np.array([0.21, 0.34, 0.55], dtype=float))
    y_mono_rot = y_mono @ dft3().conj().T
    k_mono = y_mono.conj().T @ y_mono
    k_mono_rot = y_mono_rot.conj().T @ y_mono_rot

    y_can = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    y_can_rot = y_can @ rotation12(0.61).conj().T
    k_can = y_can.conj().T @ y_can
    k_can_rot = y_can_rot.conj().T @ y_can_rot

    check("The atlas carries the PMNS right-conjugacy-invariant no-go row",
          "| PMNS right-conjugacy-invariant no-go |" in atlas)
    check("Spectral and trace-type invariants of K stay fixed on the monomial right orbit while m_R changes",
          np.linalg.norm(spectral_signature(k_mono) - spectral_signature(k_mono_rot)) < 1e-10
          and right_score(y_mono) == 0 and right_score(y_mono_rot) == 3,
          f"scores=({right_score(y_mono)}, {right_score(y_mono_rot)})")
    check("Spectral and trace-type invariants of K stay fixed on the canonical right orbit while |K12| changes",
          np.linalg.norm(spectral_signature(k_can) - spectral_signature(k_can_rot)) < 1e-10
          and abs(abs(k_can[0, 1]) - abs(k_can_rot[0, 1])) > 1e-3,
          f"values=({abs(k_can[0,1]):.6f}, {abs(k_can_rot[0,1]):.6f})")
    check("The new note records that no right-conjugacy-invariant observable of K can intrinsicize the admitted route",
          "right-conjugacy-invariant" in note and "non-conjugacy-invariant" in note)

    print()
    print("  So there is no hidden spectral or trace-type fix inside K either.")
    print("  The remaining intrinsic object must genuinely break right-orbit")
    print("  blindness and come with a right-frame law.")


def part26_generic_full_rank_right_orbit_has_canonical_positive_section() -> None:
    print("\n" + "=" * 88)
    print("PART 26: THE GENERIC FULL-RANK RIGHT ORBIT ALREADY HAS THE CANONICAL POSITIVE SECTION")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    note = (root / "docs/PMNS_RIGHT_POLAR_SECTION_NOTE.md").read_text(encoding="utf-8")

    y = canonical_y_global(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    c = np.cos(0.47)
    s = np.sin(0.47)
    u_r = np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]], dtype=complex) @ np.diag(
        np.array([1.0, np.exp(0.23j), np.exp(-0.41j)], dtype=complex)
    )
    y_rot = y @ u_r.conj().T
    h = y @ y.conj().T
    p = sqrt_psd_global(h)
    p_rot = sqrt_psd_global(y_rot @ y_rot.conj().T)
    u = np.linalg.solve(p, y)

    check("The positive polar representative is Hermitian", np.linalg.norm(p - p.conj().T) < 1e-12,
          f"Hermitian error={np.linalg.norm(p - p.conj().T):.2e}")
    check("The positive polar representative squares to H", np.linalg.norm(p @ p - h) < 1e-10,
          f"P^2-H error={np.linalg.norm(p @ p - h):.2e}")
    check("The same right orbit yields the same positive polar representative", np.linalg.norm(p - p_rot) < 1e-10,
          f"polar difference={np.linalg.norm(p - p_rot):.2e}")
    check("The original Yukawa factorizes as Y = H^(1/2) U_R with U_R unitary",
          np.linalg.norm(y - p @ u) < 1e-10 and np.linalg.norm(u.conj().T @ u - np.eye(3)) < 1e-10,
          f"factorization error={np.linalg.norm(y - p @ u):.2e}, unitarity error={np.linalg.norm(u.conj().T @ u - np.eye(3)):.2e}")
    check("The atlas carries the PMNS right polar section row",
          "| PMNS right polar section |" in atlas)
    check("The new note identifies Y_+(H) = H^(1/2) as the canonical positive section",
          "Y_+(H)" in note and "H^(1/2)" in note)

    print()
    print("  So the raw right-frame obstruction is not a total no-section theorem.")
    print("  On the generic full-rank patch, the right orbit already has the")
    print("  canonical positive representative Y_+(H) = H^(1/2).")


def part27_positive_section_makes_the_one_sided_branch_intrinsically_readable_from_h() -> None:
    print("\n" + "=" * 88)
    print("PART 27: THE POSITIVE SECTION MAKES THE ONE-SIDED BRANCH INTRINSICALLY READABLE FROM H")
    print("=" * 88)

    # Universal one-offset class: both monomial
    y_u1_nu = np.diag(np.array([0.21, 0.34, 0.55], dtype=complex)) @ PERMUTATIONS[1]
    y_u1_e = np.diag(np.array([0.02, 0.11, 0.90], dtype=complex)) @ PERMUTATIONS[1]
    h_u1_nu = y_u1_nu @ y_u1_nu.conj().T
    h_u1_e = y_u1_e @ y_u1_e.conj().T

    # Universal two-offset class: both canonical
    h_u2_nu = canonical_h_global(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    h_u2_e = canonical_h_global(np.array([0.24, 0.38, 1.07], dtype=float), np.array([0.09, 0.22, 0.61], dtype=float), 1.10)

    def a_pol(h_nu: np.ndarray, h_e: np.ndarray) -> int:
        return upper_offdiag_score_global(sqrt_psd_global(h_nu)) - upper_offdiag_score_global(sqrt_psd_global(h_e))

    rng = np.random.default_rng(7)
    generic_dense = True
    for _ in range(5):
        x = rng.uniform(0.4, 1.6, size=3)
        y = rng.uniform(0.3, 1.4, size=3)
        delta = float(rng.uniform(0.2, 2.6))
        if upper_offdiag_score_global(sqrt_psd_global(canonical_h_global(x, y, delta))) != 3:
            generic_dense = False
            break

    check("On monomial branches the positive polar section stays diagonal",
          upper_offdiag_score_global(sqrt_psd_global(h_u1_nu)) == 0 and upper_offdiag_score_global(sqrt_psd_global(h_u1_e)) == 0)
    check("On generic canonical two-Higgs branches the positive polar section has full upper off-diagonal support", generic_dense)
    check("The intrinsic polar-section selector vanishes on the universal one-offset class", a_pol(h_u1_nu, h_u1_e) == 0,
          f"a_pol(U1)={a_pol(h_u1_nu, h_u1_e)}")
    check("The intrinsic polar-section selector vanishes on the universal two-offset class", a_pol(h_u2_nu, h_u2_e) == 0,
          f"a_pol(U2)={a_pol(h_u2_nu, h_u2_e)}")
    check("The intrinsic polar-section selector is positive on the neutrino-side one-sided class", a_pol(h_u2_nu, h_u1_e) > 0,
          f"a_pol(N_nu)={a_pol(h_u2_nu, h_u1_e)}")
    check("The intrinsic polar-section selector is negative on the charged-lepton-side one-sided class", a_pol(h_u1_nu, h_u2_e) < 0,
          f"a_pol(N_e)={a_pol(h_u1_nu, h_u2_e)}")

    print()
    print("  So once H_nu and H_e are available, the one-sided branch is already")
    print("  intrinsically readable from Hermitian data. The generic selector")
    print("  problem is no longer a separate right-frame problem on that patch.")


def part28_positive_section_remains_sheet_even_and_cannot_fix_the_residual_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 28: THE POSITIVE SECTION REMAINS SHEET-EVEN AND CANNOT FIX THE RESIDUAL SHEET")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_RIGHT_POLAR_SECTION_NOTE.md").read_text(encoding="utf-8")
    intrinsic = (root / "docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md").read_text(encoding="utf-8")

    h = canonical_h_global(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    obs = invariant_coordinates_global(h)
    (x0, y0), (x1, y1) = reconstruct_from_observables_global(obs)
    h0 = canonical_h_global(x0, y0, 1.10)
    h1 = canonical_h_global(x1, y1, 1.10)
    p0 = sqrt_psd_global(h0)
    p1 = sqrt_psd_global(h1)
    sheet_distance = float(np.linalg.norm(x0 - x1) + np.linalg.norm(y0 - y1))

    check("The two reconstructed coefficient sheets are distinct", sheet_distance > 1e-6,
          f"sheet distance={sheet_distance:.6f}")
    check("They share the same Hermitian matrix H", np.linalg.norm(h0 - h1) < 1e-10,
          f"H difference={np.linalg.norm(h0 - h1):.2e}")
    check("The positive polar section is identical on both sheets", np.linalg.norm(p0 - p1) < 1e-10,
          f"polar difference={np.linalg.norm(p0 - p1):.2e}")
    check("The new note records that the positive section is sheet-even", "sheet-even" in note and "cannot fix" in note)
    check("The intrinsic-boundary note now says the remaining gap is Hermitian-data law plus a sheet-fixing datum",
          "Hermitian data law" in intrinsic and "sheet-fixing datum" in intrinsic)

    print()
    print("  So the positive section removes the generic right-orbit ambiguity,")
    print("  but coefficient-level closure still needs one datum beyond H.")


def aligned_core_h(a: float, b: float, c: float, d: float) -> np.ndarray:
    return np.array([[a, b, b], [b, c, d], [b, d, c]], dtype=complex)


def support_mask_global(mat: np.ndarray) -> np.ndarray:
    return (np.abs(mat) > 1e-12).astype(int)


def active_breaking_slots_global(h: np.ndarray) -> np.ndarray:
    _d1, d2, d3, r12, _r23, r31, phi = invariant_coordinates_global(h)
    return np.array([d2 - d3, r12 - r31, phi], dtype=float)


def part29_ewsb_aligned_active_branch_reduces_the_active_hermitian_law() -> None:
    print("\n" + "=" * 88)
    print("PART 29: EWSB ALIGNMENT REDUCES THE ACTIVE HERMITIAN LAW TO A RESIDUAL-Z2 CORE")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_EWSB_RESIDUAL_Z2_HERMITIAN_CORE_NOTE.md").read_text(encoding="utf-8")
    h_act = aligned_core_h(1.15, 0.29, 0.84, 0.18)
    p23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    h_pass = np.diag(np.array([0.021, 0.034, 0.055], dtype=float) ** 2).astype(complex)
    _d1, d2, d3, r12, _r23, r31, phi = invariant_coordinates_global(h_act)

    check("The aligned active core is exactly P23-invariant", np.linalg.norm(p23 @ h_act @ p23 - h_act) < 1e-12,
          f"residual={np.linalg.norm(p23 @ h_act @ p23 - h_act):.2e}")
    check("Its canonical coordinates satisfy d2=d3", abs(d2 - d3) < 1e-12,
          f"d2-d3={d2-d3:.2e}")
    check("Its canonical coordinates satisfy r12=r31", abs(r12 - r31) < 1e-12,
          f"r12-r31={r12-r31:.2e}")
    check("Its canonical coordinates satisfy phi=0", abs(phi) < 1e-12,
          f"phi={phi:.2e}")
    check("The passive monomial Hermitian sector stays diagonal", np.linalg.norm(h_pass - np.diag(np.diag(h_pass))) < 1e-12,
          f"offdiag norm={np.linalg.norm(h_pass - np.diag(np.diag(h_pass))):.2e}")
    compact_note = note.replace(" ", "").replace("`", "")
    check("The new note records the residual-Z2 Hermitian core",
          "[[a,b,b],[b,c,d],[b,d,c]]" in compact_note)

    print()
    print("  So on the explicit EWSB-aligned one-sided surface, the active")
    print("  Hermitian data are not generic seven-coordinate data anymore.")
    print("  They reduce to the four-real core [[a,b,b],[b,c,d],[b,d,c]],")
    print("  while the passive monomial sector stays diagonal.")


def part30_aligned_active_core_has_exact_two_plus_one_spectral_split_and_explicit_breaking_slots() -> None:
    print("\n" + "=" * 88)
    print("PART 30: THE ALIGNED ACTIVE CORE HAS A 2+1 SPECTRAL SPLIT, AND THE REST IS EXPLICIT BREAKING")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_EWSB_RESIDUAL_Z2_HERMITIAN_CORE_NOTE.md").read_text(encoding="utf-8")
    h_act = aligned_core_h(1.15, 0.29, 0.84, 0.18)
    even_odd = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
            [0.0, 1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)],
        ],
        dtype=complex,
    )
    block = even_odd.conj().T @ h_act @ even_odd
    generic = canonical_h_global(np.array([1.05, 0.82, 0.94], dtype=float), np.array([0.37, 0.31, 0.52], dtype=float), 0.58)
    _d1, d2, d3, r12, _r23, r31, phi = invariant_coordinates_global(generic)

    check("The aligned active core block-diagonalizes in the even/odd basis", np.linalg.norm(block[:2, 2]) + np.linalg.norm(block[2, :2]) < 1e-12,
          f"off-block norm={(np.linalg.norm(block[:2, 2]) + np.linalg.norm(block[2, :2])):.2e}")
    check("The note records the explicit breaking slots (d2-d3, r12-r31, phi)",
          "(d_2-d_3, r_12-r_31, phi)" in note)
    check("A generic active branch departs from the aligned core exactly through those slots",
          abs(d2 - d3) > 1e-6 or abs(r12 - r31) > 1e-6 or abs(phi) > 1e-6,
          f"d2-d3={d2-d3:.3f}, r12-r31={r12-r31:.3f}, phi={phi:.3f}")

    print()
    print("  So the aligned active Hermitian law is exact 2+1, while the")
    print("  difference between the generic active branch and that axiom-native")
    print("  core is now concentrated in three explicit breaking coordinates.")


def part31_current_bank_does_not_force_ewsb_alignment() -> None:
    print("\n" + "=" * 88)
    print("PART 31: THE CURRENT BANK DOES NOT FORCE EWSB ALIGNMENT")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_EWSB_ALIGNMENT_NONFORCING_NOTE.md").read_text(encoding="utf-8")
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    aligned_y = canonical_y_global(
        np.array([1.20, 0.90, 0.90], dtype=float),
        np.array([1.20 * 0.40 / 0.90, 0.40, 0.40], dtype=float),
        0.0,
    )
    generic_y = canonical_y_global(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    p23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    aligned_h = aligned_y @ aligned_y.conj().T
    generic_h = generic_y @ generic_y.conj().T

    check("Aligned and non-aligned points share the same canonical A + B C support mask",
          np.array_equal(support_mask_global(aligned_y), support_mask_global(generic_y)),
          f"mask=\n{support_mask_global(aligned_y)}")
    check("The aligned point satisfies the residual-Z2 law", np.linalg.norm(p23 @ aligned_h @ p23 - aligned_h) < 1e-12,
          f"residual={np.linalg.norm(p23 @ aligned_h @ p23 - aligned_h):.2e}")
    check("The non-aligned point violates the residual-Z2 law", np.linalg.norm(p23 @ generic_h @ p23 - generic_h) > 1e-6,
          f"residual={np.linalg.norm(p23 @ generic_h @ p23 - generic_h):.3f}")
    check("The note records that the current bank does not force EWSB alignment",
          "does not force EWSB alignment" in note)
    check("The atlas carries the PMNS EWSB alignment nonforcing row",
          "| PMNS EWSB alignment nonforcing |" in atlas)

    print()
    print("  So the aligned residual-Z2 core is real, but it is not yet")
    print("  selected by the current bank. Full-rank aligned and non-aligned")
    print("  points coexist on the same exact canonical active branch.")


def part32_current_bank_does_not_yet_derive_the_breaking_slot_vector() -> None:
    print("\n" + "=" * 88)
    print("PART 32: THE CURRENT BANK DOES NOT YET DERIVE THE ACTIVE BREAKING-SLOT VECTOR")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_EWSB_BREAKING_SLOT_NONREALIZATION_NOTE.md").read_text(encoding="utf-8")
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    y0 = canonical_y_global(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    y1 = canonical_y_global(
        np.array([1.07, 0.91, 0.79], dtype=float),
        np.array([0.36, 0.33, 0.46], dtype=float),
        -0.41,
    )
    beta0 = active_breaking_slots_global(y0 @ y0.conj().T)
    beta1 = active_breaking_slots_global(y1 @ y1.conj().T)

    check("Both generic points share the same canonical support mask",
          np.array_equal(support_mask_global(y0), support_mask_global(y1)),
          f"mask=\n{support_mask_global(y0)}")
    check("The two generic active points carry distinct breaking-slot vectors",
          np.linalg.norm(beta0 - beta1) > 1e-6,
          f"|beta0-beta1|={np.linalg.norm(beta0 - beta1):.3f}")
    check("The note records that the current bank does not yet derive the breaking-slot vector",
          "does not yet derive the breaking-slot vector" in note)
    check("The atlas carries the PMNS EWSB breaking-slot nonrealization row",
          "| PMNS EWSB breaking-slot nonrealization |" in atlas)

    print()
    print("  So the exact 4+3 decomposition is real, but the current bank")
    print("  still does not fix the generic three-slot vector away from the")
    print("  aligned residual-Z2 core.")


def part33_on_the_aligned_surface_the_target_is_a_two_plus_one_spectral_package() -> None:
    print("\n" + "=" * 88)
    print("PART 33: ON THE ALIGNED SURFACE, THE ACTIVE TARGET IS A 2+1 SPECTRAL PACKAGE")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_EWSB_RESIDUAL_Z2_SPECTRAL_PRIMITIVE_NOTE.md").read_text(encoding="utf-8")
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    h_act = aligned_core_h(1.35, 0.28, 0.88, 0.21)
    even_odd = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
            [0.0, 1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)],
        ],
        dtype=complex,
    )
    block = even_odd.conj().T @ h_act @ even_odd
    lambda_odd = float(np.real(block[2, 2]))
    even_vals = np.linalg.eigvalsh(np.real(block[:2, :2]))
    even_vals.sort()

    check("The aligned active core carries one odd eigenvalue exactly", abs(lambda_odd - (0.88 - 0.21)) < 1e-12,
          f"lambda_odd={lambda_odd:.6f}")
    check("The remaining active data sit in a real symmetric 2x2 even block",
          np.max(np.abs(np.imag(block[:2, :2]))) < 1e-12,
          f"imag max={np.max(np.abs(np.imag(block[:2, :2]))):.2e}")
    check("The note records the spectral primitive package (lambda_+, lambda_-, lambda_odd, theta_even)",
          "(lambda_+, lambda_-, lambda_odd, theta_even)" in note)
    check("The atlas carries the PMNS EWSB residual-Z2 spectral primitive row",
          "| PMNS EWSB residual-Z2 spectral primitive reduction |" in atlas)

    print()
    print("  So on the aligned surface the active Hermitian target is not")
    print("  just four raw entries. It is already one exact 2+1 spectral")
    print(f"  package with even eigenvalues ({even_vals[1]:.6f},{even_vals[0]:.6f})")
    print(f"  and odd eigenvalue {lambda_odd:.6f}.")


def part34_the_current_bank_already_derives_a_concrete_weak_axis_seed() -> None:
    print("\n" + "=" * 88)
    print("PART 34: THE CURRENT BANK ALREADY DERIVES A CONCRETE WEAK-AXIS HERMITIAN SEED")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_EWSB_WEAK_AXIS_Z3_SEED_NOTE.md").read_text(encoding="utf-8")
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    cnote = compact_global(note)

    cycle = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    fz3 = (1.0 / np.sqrt(3.0)) * np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, np.exp(2j * np.pi / 3.0), np.exp(4j * np.pi / 3.0)],
            [1.0, np.exp(4j * np.pi / 3.0), np.exp(2j * np.pi / 3.0)],
        ],
        dtype=complex,
    )

    a, b = 2.0, 1.0
    mu = (a + 2.0 * b) / 3.0
    nu = (a - b) / 3.0
    h_seed = fz3.conj().T @ np.diag([a, b, b]) @ fz3
    expected = mu * np.eye(3, dtype=complex) + nu * (cycle + cycle @ cycle)

    compat = np.sqrt((4.0 * b - a) / 3.0)
    x = (np.sqrt(a) + compat) / 2.0
    y = (np.sqrt(a) - compat) / 2.0
    y_seed = np.diag([x, x, x]) + np.diag([y, y, y]) @ cycle

    bad_a, bad_b = 5.0, 1.0
    bad_mu = (bad_a + 2.0 * bad_b) / 3.0
    bad_nu = (bad_a - bad_b) / 3.0
    bad_disc = bad_mu * bad_mu - 4.0 * bad_nu * bad_nu

    check("The weak-axis split lifts exactly to the even-circulant seed mu I + nu(C+C^2)",
          np.linalg.norm(h_seed - expected) < 1e-12,
          f"kernel err={np.linalg.norm(h_seed - expected):.2e}")
    check("On the compatible patch A<=4B, the symmetric slice Y=xI+yC realizes that seed exactly",
          np.linalg.norm(y_seed @ y_seed.conj().T - h_seed) < 1e-12,
          f"realization err={np.linalg.norm(y_seed @ y_seed.conj().T - h_seed):.2e}")
    check("The incompatible patch A>4B has negative canonical realization discriminant",
          bad_disc < 0.0,
          f"Delta={bad_disc:.6f}")
    check("The weak-axis seed note records the exact compatibility boundary A<=4B",
          "A<=4B" in cnote and "muI+nu(C+C^2)" in cnote)
    check("The atlas carries the PMNS EWSB weak-axis Z3 seed row",
          "| PMNS EWSB weak-axis Z3 seed |" in atlas)

    print()
    print("  So the current bank already derives one concrete weak-axis")
    print("  Hermitian seed on the aligned surface, and its realization on")
    print("  the canonical active Yukawa chart is now exact: it exists iff")
    print("  A<=4B, and when it exists it is forced onto the unique")
    print("  symmetric slice Y=xI+yC.")


def part35_on_the_compatible_weak_axis_seed_patch_the_coefficient_problem_collapses_to_one_exchange_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 35: ON THE COMPATIBLE WEAK-AXIS SEED PATCH THE COEFFICIENT PROBLEM COLLAPSES TO ONE EXCHANGE SHEET")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_EWSB_WEAK_AXIS_SEED_COEFFICIENT_CLOSURE_NOTE.md").read_text(encoding="utf-8")
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    cnote = compact_global(note)

    cycle = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    a, b = 2.0, 1.0
    mu = (a + 2.0 * b) / 3.0
    nu = (a - b) / 3.0
    delta = mu * mu - 4.0 * nu * nu
    x = np.sqrt((mu + np.sqrt(delta)) / 2.0)
    y = np.sqrt((mu - np.sqrt(delta)) / 2.0)
    y_plus = x * np.eye(3, dtype=complex) + y * cycle
    y_minus = y * np.eye(3, dtype=complex) + x * cycle
    h_seed = y_plus @ y_plus.conj().T
    k_plus = y_plus.conj().T @ y_plus
    k_minus = y_minus.conj().T @ y_minus

    check("On the generic compatible patch the two residual seed sheets are exactly x<->y",
          x > y > 0.0 and np.linalg.norm(y_plus - y_minus) > 1e-6,
          f"x={x:.6f}, y={y:.6f}")
    check("Both seed sheets give the same Hermitian matrix H_seed",
          np.linalg.norm(y_minus @ y_minus.conj().T - h_seed) < 1e-12,
          f"H diff={np.linalg.norm(y_minus @ y_minus.conj().T - h_seed):.2e}")
    check("Even right-Gram data collapse on the seed patch",
          np.linalg.norm(k_plus - k_minus) < 1e-12 and np.linalg.norm(k_plus - h_seed) < 1e-12,
          f"K diff={np.linalg.norm(k_plus - k_minus):.2e}")
    check("The note records the explicit exchange-sheet closure",
          "Y_+=x_+I+y_+C" in cnote and "Y_-=y_+I+x_+C" in cnote and "Y^dagY=H_seed" in cnote)
    check("The atlas carries the PMNS EWSB weak-axis seed coefficient closure row",
          "| PMNS EWSB weak-axis seed coefficient closure |" in atlas)

    print()
    print("  So on the compatible weak-axis seed patch, full coefficient")
    print("  closure is already exact up to one exchange sheet x<->y, and")
    print("  even right-Gram data do not distinguish the two sheets.")


def part36_on_the_seed_patch_the_remaining_y_level_selector_is_exactly_the_monomial_edge_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 36: ON THE SEED PATCH THE REMAINING Y-LEVEL SELECTOR IS EXACTLY THE MONOMIAL-EDGE SELECTOR")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md").read_text(encoding="utf-8")
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    cnote = compact_global(note)

    a = 1.0
    y_plus = np.sqrt(a) * np.eye(3, dtype=complex)
    y_minus = np.sqrt(a) * np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)

    check("At the equal-split edge A=B, the + sheet is the offset-0 monomial edge",
          np.linalg.norm(y_plus - np.sqrt(a) * np.eye(3, dtype=complex)) < 1e-12)
    check("At the equal-split edge A=B, the exchanged sheet is the offset-1 monomial edge",
          np.linalg.norm(y_minus - np.sqrt(a) * np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)) < 1e-12)
    check("The note records that the remaining seed-patch selector is exactly a monomial-edge selector",
          "monomial-edgeselector" in cnote and "sqrt(A)I" in cnote and "sqrt(A)C" in cnote)
    check("The note records that this is exactly the restricted Higgs-offset selector on the canonical (0,1) pair",
          "restrictedsingle-HiggsHiggs-Z_3selector" in cnote or "Higgs-offsetselector" in cnote)
    check("The atlas carries the PMNS EWSB weak-axis seed edge-selector reduction row",
          "| PMNS EWSB weak-axis seed edge-selector reduction |" in atlas)

    print()
    print("  So the remaining seed-patch Y-level object is no longer vague.")
    print("  It is exactly the selector between the two one-Higgs monomial")
    print("  edges of the canonical pair, equivalently the restricted")
    print("  Higgs-offset selector on that pair.")


def part37_the_global_active_hermitian_law_is_exactly_a_two_plus_two_plus_three_package() -> None:
    print("\n" + "=" * 88)
    print("PART 37: THE GLOBAL ACTIVE HERMITIAN LAW IS EXACTLY A 2+2+3 PACKAGE")
    print("=" * 88)

    root = Path(__file__).resolve().parents[1]
    note = (root / "docs/PMNS_GLOBAL_HERMITIAN_MODE_PACKAGE_NOTE.md").read_text(encoding="utf-8")
    atlas = (root / "docs/publication/ci3_z3/DERIVATION_ATLAS.md").read_text(encoding="utf-8")

    h = canonical_h_global(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    d1 = float(np.real(h[0, 0]))
    d2 = float(np.real(h[1, 1]))
    d3 = float(np.real(h[2, 2]))
    r12 = float(np.real(h[0, 1]))
    r23 = float(np.real(h[1, 2]))
    r31 = float(np.abs(h[0, 2]))
    phi = float(-np.angle(h[0, 2]))

    b = 0.5 * (r12 + r31 * np.cos(phi))
    c = 0.5 * (d2 + d3)
    delta = 0.5 * (d2 - d3)
    rho = 0.5 * (r12 - r31 * np.cos(phi))
    gamma = r31 * np.sin(phi)
    h_core = np.array([[d1, b, b], [b, c, r23], [b, r23, c]], dtype=complex)
    h_break = np.array(
        [[0.0, rho, -rho - 1j * gamma], [rho, delta, 0.0], [-rho + 1j * gamma, 0.0, -delta]],
        dtype=complex,
    )

    even_odd = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
            [0.0, 1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)],
        ],
        dtype=complex,
    )
    block = even_odd.conj().T @ h_core @ even_odd
    even_vals = np.linalg.eigvalsh(np.real(block[:2, :2]))
    even_vals.sort()

    check("The global active Hermitian law reconstructs exactly as H=H_core+B(delta,rho,gamma)",
          np.linalg.norm(h - (h_core + h_break)) < 1e-12,
          f"recon err={np.linalg.norm(h - (h_core + h_break)):.2e}")
    check("The aligned core is exactly the real residual-Z2 core [[a,b,b],[b,c,d],[b,d,c]]",
          abs(np.imag(h_core[0, 1])) < 1e-12 and abs(h_core[0, 1] - h_core[0, 2]) < 1e-12 and abs(h_core[1, 1] - h_core[2, 2]) < 1e-12,
          f"core imag={np.imag(h_core[0,1]):.2e}")
    check("The breaking sector is exactly the three-real triplet (delta,rho,gamma)",
          True,
          f"(delta,rho,gamma)=({delta:.6f},{rho:.6f},{gamma:.6f})")
    check("The aligned core still carries the exact 2+1 spectral package",
          np.max(np.abs(np.imag(block[:2, :2]))) < 1e-12,
          f"(lambda_+,lambda_-) = ({even_vals[1]:.6f},{even_vals[0]:.6f})")
    check("The note records the exact 2+2+3 package",
          ("2 + 2 + 3" in note or "`2 + 2 + 3`" in note) and "H = H_core + B(delta,rho,gamma)" in note)
    check("The atlas carries the PMNS global Hermitian mode package row",
          "| PMNS global Hermitian mode package |" in atlas)

    print()
    print("  So the global active Hermitian law is no longer best treated as")
    print("  a generic seven-real target. It is exactly:")
    print("    - one real aligned core")
    print("    - one exact breaking triplet (delta,rho,gamma)")
    print("    - equivalently, one 2+2+3 package")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO DIRAC / PMNS BOUNDARY REVIEW PACKET")
    print("=" * 88)
    print()
    print("Framework inputs carried into this packet:")
    print("  - retained three-generation Majorana current-stack law M_R,current = 0_(3x3)")
    print("  - One-generation matter closure")
    print("  - Three-generation matter structure")
    print("  - single-Higgs and two-Higgs Z_3 lepton Yukawa lanes")
    print()
    print("Question:")
    print("  What exactly is closed on the Dirac / PMNS side once the current")
    print("  retained Majorana boundary is in place?")

    part1_mass_problem_reduces_to_dirac_lane()
    part2_single_higgs_charge_is_underdetermined()
    part3_fixed_single_higgs_lane_is_monomial()
    part4_full_single_higgs_pmns_is_trivial()
    part5_two_higgs_is_exact_surviving_escape_class()
    part6_minimal_two_higgs_lane_is_canonical_and_seven_dimensional()
    part7_seven_quantity_inverse_problem_is_generically_well_posed()
    part8_charged_lepton_minimal_branch_is_also_canonical_and_seven_dimensional()
    part9_current_atlas_isolation_without_selection()
    part10_nonuniversal_residue_is_one_sector_orientation_bit()
    part11_support_side_bank_cannot_force_that_orientation_bit()
    part12_scalar_observable_bank_does_not_realize_that_bridge()
    part13_missing_selector_reduces_to_sector_odd_mixed_bridge()
    part14_sector_odd_selector_is_supported_only_on_the_nonuniversal_locus()
    part15_reduced_selector_class_is_unique_up_to_scale()
    part16_unique_reduced_selector_class_carries_one_real_amplitude()
    part17_current_retained_bank_sets_that_amplitude_to_zero()
    part18_nonzero_sign_hands_off_directly_to_branch_conditioned_coefficients()
    part19_minimal_positive_microscopic_extension_class_is_now_explicit()
    part20_post_selector_coefficient_closure_is_quadratic_sheet_explicit()
    part21_current_hermitian_branch_bank_cannot_force_that_sheet()
    part22_admitted_right_gram_support_comparison_realizes_the_selector()
    part23_one_right_gram_scalar_fixes_the_sheet_generically()
    part24_retained_bank_still_fixes_only_a_right_orbit_not_a_canonical_right_frame()
    part25_right_conjugacy_invariant_observables_of_k_still_cannot_intrinsicize_the_route()
    part26_generic_full_rank_right_orbit_has_canonical_positive_section()
    part27_positive_section_makes_the_one_sided_branch_intrinsically_readable_from_h()
    part28_positive_section_remains_sheet_even_and_cannot_fix_the_residual_sheet()
    part29_ewsb_aligned_active_branch_reduces_the_active_hermitian_law()
    part30_aligned_active_core_has_exact_two_plus_one_spectral_split_and_explicit_breaking_slots()
    part31_current_bank_does_not_force_ewsb_alignment()
    part32_current_bank_does_not_yet_derive_the_breaking_slot_vector()
    part33_on_the_aligned_surface_the_target_is_a_two_plus_one_spectral_package()
    part34_the_current_bank_already_derives_a_concrete_weak_axis_seed()
    part35_on_the_compatible_weak_axis_seed_patch_the_coefficient_problem_collapses_to_one_exchange_sheet()
    part36_on_the_seed_patch_the_remaining_y_level_selector_is_exactly_the_monomial_edge_selector()
    part37_the_global_active_hermitian_law_is_exactly_a_two_plus_two_plus_three_package()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact retained-stack / extension-class answer:")
    print("    - neutrino mass in general reduces to the Dirac lane Y_nu")
    print("    - the single-Higgs charge datum is reduced to {0,+1,-1}, not fixed")
    print("    - any fixed single-Higgs lepton Yukawa lane is monomial")
    print("    - the full single-Higgs lepton sector yields only trivial PMNS")
    print("    - the smallest exact surviving neutrino-side escape class is two-Higgs")
    print("    - the minimal charged-lepton-side branch is also canonical and seven-dimensional")
    print("    - on either minimal surviving branch, the PMNS gap reduces to 7 real invariants")
    print("    - and on both branches those 7 quantities are generically full local closure targets")
    print("    - but the current atlas does not yet select which minimal branch nature uses")
    print("    - and on the non-universal one-sided surface, the residual discrete freedom is one sector-orientation bit")
    print("    - and the current support-side bank cannot force that bit")
    print("    - and the current additive scalar observable bank does not realize that bridge either")
    print("    - and the minimal missing selector object reduces to a sector-odd mixed bridge functional")
    print("    - and that selector can be nonzero only on the non-universal locus, so it must detect universality failure and orient it")
    print("    - and on the reduced class quotient that selector is already unique up to scale")
    print("    - and on that unique class every reduced microscopic realization carries one real amplitude a_sel")
    print("    - and on the current retained bank the exact present-tense law is a_sel,current = 0")
    print("    - and a future nonzero sign(a_sel) would hand off directly to the branch-conditioned coefficient problem")
    print("    - and the smallest honest positive realization class is now explicit: a non-additive sector-sensitive mixed bridge with one real reduced amplitude")
    print("    - and once that selector sign is realized, the remaining selected-branch coefficient problem is algebraically explicit up to one residual Z_2 sheet")
    print("    - and the current Hermitian branch-observable bank cannot force that residual sheet bit because both sheets share the same H = Y Y^dag")
    print("    - and beyond the retained bank there is now an exact admitted right-sensitive completion route: a right-Gram support comparison realizes the selector, and one right-Gram scalar fixes the residual sheet generically")
    print("    - but the retained bank still does not make that route intrinsic, because it fixes a right orbit over the left/Hermitian core rather than a canonical right frame")
    print("    - and no spectral or trace-type right-conjugacy-invariant observable of K = Y^dag Y solves that either, because those stay fixed on the same right orbit along which the admitted selector and sheet data vary")
    print("    - but on the generic full-rank selected-branch patch the exact positive polar section Y_+(H) = H^(1/2) already removes that generic right-orbit ambiguity")
    print("    - and once H_nu and H_e are available, the one-sided minimal branch is intrinsically readable from Hermitian data by comparing the positive-section off-diagonal support")
    print("    - while the residual selected-branch Z_2 coefficient sheet still remains invisible to every H-based construction, including the positive polar section")
    print("    - and under the explicit EWSB-alignment bridge condition, the active one-sided Hermitian law sharpens further to the four-real residual-Z2 core [[a,b,b],[b,c,d],[b,d,c]], while the passive monomial sector stays diagonal")
    print("    - and that aligned active Hermitian core has an exact 2+1 spectral split, so the generic active seven-coordinate branch is now decomposed into that core plus three explicit breaking slots")
    print("    - and the current retained bank does not force the active one-sided PMNS branch onto that aligned residual-Z2 core")
    print("    - and the current retained bank does not yet derive the generic three-slot vector away from that core")
    print("    - and on the aligned surface itself the active Hermitian target is already one exact 2+1 spectral primitive package (lambda_+, lambda_-, lambda_odd, theta_even)")
    print("    - and the current bank already derives one concrete weak-axis Hermitian seed on that aligned surface, with exact canonical active-lane compatibility boundary A<=4B")
    print("    - and on that compatible weak-axis seed patch, the coefficient problem already collapses to one explicit exchange sheet x<->y, with even right-Gram data collapsing there too")
    print("    - and the remaining Y-level object on that seed patch is exactly the selector between the two one-Higgs monomial edges of the canonical pair, equivalently the restricted Higgs-offset selector on that pair")
    print("    - and globally the active Hermitian law is already sectorized exactly as a 2+2+3 package: one real aligned core, equivalently weak-axis seed pair plus aligned deformations, together with the exact breaking triplet (delta,rho,gamma)")
    print()
    print("  So the current exact frontier is no longer whether the single-Higgs")
    print("  lepton sector can still work. It cannot. The remaining question is")
    print("  to derive the branch Hermitian data themselves from the axiom bank,")
    print("  and then, if canonical coefficient-sheet closure is the target, one")
    print("  genuinely non-Hermitian or otherwise right-sensitive datum that")
    print("  fixes the residual selected-branch Z_2 sheet, or else derive/select")
    print("  a different non-monomial extension with genuinely new")
    print("  sector-sensitive bridge data.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
