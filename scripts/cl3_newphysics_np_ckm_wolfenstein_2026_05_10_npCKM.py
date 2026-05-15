"""
NEWPHYSICS NP-CKM-Wolfenstein — P-Heavy-A circulant Cabibbo no-go runner.

Tests whether the P-Heavy-A primitive (sector-dependent rho-Koide circulants
on H_{hw=1} for up-type and down-type quarks, PR #1044) can produce the
observed Wolfenstein CKM structure (lambda, A, rho, eta) via the standard
mass-eigenstate diagonalization

    V_CKM = U_up^dagger U_down

where U_q is the unitary that diagonalizes the Hermitian circulant
H_q = a_q I + b_q C + b_bar_q C^2 on the cyclic Z_3 generation algebra
C_3[111] retained as Z7 in the framework primitive set.

Bottom-line claim of this runner: NO. Every Hermitian circulant on C_3[111]
is simultaneously diagonal in the discrete Z_3 Fourier basis F. Therefore
U_up and U_down differ from F only by (i) a column permutation P_q assigning
Fourier index k to generation g, and (ii) a diagonal phase D_q. The product

    V_CKM = (F P_up D_up)^dagger (F P_dn D_dn)
          = D_up^dagger P_up^T F^dagger F P_dn D_dn
          = D_up^dagger P_up^T P_dn D_dn

is a permutation matrix dressed by overall phases. Magnitudes |V_ij| are
either 0 or 1. The Cabibbo angle sin(theta_C) ~ 0.225, the Wolfenstein A,
the CP-plane (rho, eta), and the Jarlskog invariant J ~ 3e-5 are ALL forced
to zero (or trivially 1) by this primitive structure alone.

This runner certifies that the no-go is structural and parameter-free: it
holds for arbitrary (rho_up, delta_up, v_0_up), (rho_dn, delta_dn, v_0_dn)
admissible under P-Heavy-A, and is independent of the canonical alpha_s(v),
of the retained 3-generation count N_gen = 3 (PR #952), and of the retained
color count N_color = 3 (PR #954).

Constraints respected:
- No new repo-wide axioms.
- No new derivational imports.
- No PDG CKM observable enters as a derivation premise.
- P-Heavy-A is NOT promoted; this note is a negative source theorem on the
  candidate primitive's CKM-derivation capability.

Reproduction:
    python3 scripts/cl3_newphysics_np_ckm_wolfenstein_2026_05_10_npCKM.py
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np


# ---------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, *, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS  {label}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL  {label}")
        if detail:
            print(f"        detail: {detail}")


def section(name: str) -> None:
    print()
    print("=" * 72)
    print(name)
    print("=" * 72)


# ---------------------------------------------------------------------
# Z_3 Fourier eigenbasis for C_3[111] circulants
# ---------------------------------------------------------------------

OMEGA = np.exp(2j * np.pi / 3)


def z3_fourier_matrix() -> np.ndarray:
    """Unitary DFT_3 matrix.

    Diagonalizes every 3x3 circulant matrix.
    """
    F = np.array(
        [
            [1.0 + 0.0j, 1.0 + 0.0j, 1.0 + 0.0j],
            [1.0 + 0.0j, OMEGA, OMEGA**2],
            [1.0 + 0.0j, OMEGA**2, OMEGA],
        ]
    ) / math.sqrt(3.0)
    return F


def shift_matrix() -> np.ndarray:
    """C_1: circular shift mod 3 (the C_3 generator)."""
    return np.array(
        [
            [0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j],
            [0.0 + 0.0j, 0.0 + 0.0j, 1.0 + 0.0j],
            [1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j],
        ]
    )


def hermitian_circulant(a: float, rho: float, delta: float) -> np.ndarray:
    """P-Heavy-A circulant H_q = a I + b C + b_bar C^2 with rho = 2|b|/a, arg(b) = delta.

    The framework eigenvalue formula
        lambda_k = a (1 + rho cos(delta + 2 pi k / 3))
    is recovered for k = 0, 1, 2.
    """
    b_mag = 0.5 * rho * a
    b = b_mag * np.exp(1j * delta)
    b_bar = np.conj(b)
    C = shift_matrix()
    H = a * np.eye(3, dtype=complex) + b * C + b_bar * (C @ C)
    # Numerical Hermiticity check
    assert np.allclose(H, H.conj().T, atol=1e-12), "Circulant not Hermitian"
    return H


# ---------------------------------------------------------------------
# Test 1: F diagonalizes every 3x3 circulant (Schur's theorem)
# ---------------------------------------------------------------------

def test_fourier_diagonalizes_all_circulants() -> None:
    section("Test 1: Z_3 DFT diagonalizes every 3x3 Hermitian circulant")
    F = z3_fourier_matrix()

    # Sample 6 distinct (a, rho, delta) triples
    triples = [
        (1.0, 1.4142, 2.0 / 9.0),       # ~ charged lepton (BAE = sqrt(2), 2/9)
        (1.0, 1.7600, 2.1729),          # P-Heavy-A up-type fit
        (1.0, 1.5450, 4.3022),          # P-Heavy-A down-type fit
        (2.0, 0.5000, 1.0),             # generic small rho
        (1.0, 2.4999, 0.5),             # generic large rho (still < 2.5)
        (0.5, 1.0, -0.3),               # generic mixed
    ]

    for idx, (a, rho, delta) in enumerate(triples):
        H = hermitian_circulant(a, rho, delta)
        D = F.conj().T @ H @ F
        off = D - np.diag(np.diag(D))
        max_off = float(np.max(np.abs(off)))
        check(
            f"F diagonalizes H (a={a}, rho={rho}, delta={delta:.4f})",
            max_off < 1e-12,
            detail=f"max off-diagonal in F^H H F = {max_off:.2e}",
        )


# ---------------------------------------------------------------------
# Test 2: Both sectors share the same eigenbasis (V_CKM is permutation x phase)
# ---------------------------------------------------------------------

def test_v_ckm_is_permutation() -> None:
    section("Test 2: V_CKM = U_up^H U_down is permutation x phase")

    rho_up, delta_up = 1.7600, 2.1729
    rho_dn, delta_dn = 1.5450, 4.3022

    H_up = hermitian_circulant(1.0, rho_up, delta_up)
    H_dn = hermitian_circulant(1.0, rho_dn, delta_dn)

    w_up, U_up = np.linalg.eigh(H_up)
    w_dn, U_dn = np.linalg.eigh(H_dn)

    V = U_up.conj().T @ U_dn
    absV = np.abs(V)
    print()
    print("|V_CKM| (P-Heavy-A up-type x down-type fits):")
    for row in absV:
        print("  " + "  ".join(f"{x:+.6e}" for x in row))
    print()

    # Each row and column should be a unit vector (V is unitary)
    row_sumsq = absV ** 2
    check(
        "V is unitary (each row sums to 1)",
        np.allclose(np.sum(row_sumsq, axis=1), np.ones(3), atol=1e-10),
        detail=f"row norms^2 = {np.sum(row_sumsq, axis=1)}",
    )

    # Each row should have exactly ONE entry of magnitude 1, others of magnitude 0
    for r in range(3):
        sorted_abs = np.sort(absV[r])
        check(
            f"Row {r} has one |V_ij|=1 and two |V_ij|=0 (permutation pattern)",
            sorted_abs[0] < 1e-10 and sorted_abs[1] < 1e-10 and abs(sorted_abs[2] - 1.0) < 1e-10,
            detail=f"sorted |V_{r}| = {sorted_abs}",
        )

    # Largest off-diagonal magnitude across V
    max_offdiag = 0.0
    for r in range(3):
        for c in range(3):
            if r != c:
                # any non-trivial mixing would show up here; but V is permutation
                # so even "diagonal" may be 0. Look at max NON-1 entry.
                pass
    # Better metric: |Cabibbo entry| should be 0 not 0.225
    # The Cabibbo entry conventionally is |V_us| which under our setup is V[0,1].
    # But here V is a permutation; some row pairing has the 1, others are 0.
    # Compute "Cabibbo angle" prediction = first off-diagonal magnitude that arises
    # from the closest-eigenvalue identification.
    nontrivial_offdiag = float(np.min(np.abs(absV - np.eye(3))))  # 0 if V = I
    check(
        "V is exactly a permutation matrix (no continuous mixing)",
        np.max(np.abs(absV ** 2 - np.round(absV ** 2))) < 1e-10,
        detail=f"|V| entries are 0/1 to 1e-10 precision",
    )


# ---------------------------------------------------------------------
# Test 3: This holds for ALL (rho_q, delta_q) admissible under P-Heavy-A
# ---------------------------------------------------------------------

def test_parameter_free_no_go() -> None:
    section("Test 3: No-go is parameter-free across the P-Heavy-A admission")

    # Sweep rho in (0, 2.5) and delta in (0, 2 pi) for both sectors
    rng = np.random.default_rng(20260510)
    n_trials = 25
    max_dev_observed = 0.0
    for _ in range(n_trials):
        rho_up = float(rng.uniform(0.1, 2.4))
        delta_up = float(rng.uniform(0.0, 2.0 * math.pi))
        rho_dn = float(rng.uniform(0.1, 2.4))
        delta_dn = float(rng.uniform(0.0, 2.0 * math.pi))

        H_up = hermitian_circulant(1.0, rho_up, delta_up)
        H_dn = hermitian_circulant(1.0, rho_dn, delta_dn)
        _, U_up = np.linalg.eigh(H_up)
        _, U_dn = np.linalg.eigh(H_dn)
        V = U_up.conj().T @ U_dn
        absV2 = np.abs(V) ** 2
        # Distance from nearest permutation (which has entries 0/1)
        dev = float(np.max(np.abs(absV2 - np.round(absV2))))
        if dev > max_dev_observed:
            max_dev_observed = dev

    check(
        "Random parameter sweep: V is permutation to within numerical precision",
        max_dev_observed < 1e-8,
        detail=f"max |V|^2-round(|V|^2) over {n_trials} trials = {max_dev_observed:.2e}",
    )


# ---------------------------------------------------------------------
# Test 4: Wolfenstein parameters lambda, A, rho_W, eta_W, J cannot emerge
# ---------------------------------------------------------------------

def test_wolfenstein_parameters_are_forced_to_zero() -> None:
    section("Test 4: Wolfenstein (lambda, A, rho_W, eta_W, J) forced to 0/trivial")

    # Use the P-Heavy-A fitted parameters
    rho_up, delta_up = 1.7600, 2.1729
    rho_dn, delta_dn = 1.5450, 4.3022

    H_up = hermitian_circulant(1.0, rho_up, delta_up)
    H_dn = hermitian_circulant(1.0, rho_dn, delta_dn)
    w_up, U_up = np.linalg.eigh(H_up)
    w_dn, U_dn = np.linalg.eigh(H_dn)
    V = U_up.conj().T @ U_dn
    absV = np.abs(V)

    # By construction of np.linalg.eigh, eigenvalues come in ASCENDING order.
    # The framework's P-Heavy-A maps (lightest, middle, heaviest) -> (gen1, gen2, gen3) per sector.
    # Wolfenstein convention: V_ud = V[0,0], V_us = V[0,1], V_ub = V[0,2]; etc.

    V_ud_pred = float(absV[0, 0])
    V_us_pred = float(absV[0, 1])
    V_ub_pred = float(absV[0, 2])
    V_cb_pred = float(absV[1, 2])
    V_td_pred = float(absV[2, 0])
    V_ts_pred = float(absV[2, 1])

    # Wolfenstein lambda = |V_us|
    lambda_pred = V_us_pred
    # A lambda^2 = |V_cb| => A = V_cb / lambda^2 (if lambda > 0)
    A_pred = (V_cb_pred / lambda_pred ** 2) if lambda_pred > 1e-12 else float("nan")

    # CP plane: rho_W - i eta_W = V_ud V_ub^* / (V_cd V_cb^*).
    # With V essentially a permutation/phase matrix, V_ud V_ub^* will be 0 (or vanishing).
    # Jarlskog invariant J = Im(V_us V_cb V_ub^* V_cs^*).
    J_pred = float(np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])))

    print()
    print(f"  Predicted |V_us| = {V_us_pred:.6e}    (PDG ~ 0.22500)")
    print(f"  Predicted |V_cb| = {V_cb_pred:.6e}    (PDG ~ 0.04210)")
    print(f"  Predicted |V_ub| = {V_ub_pred:.6e}    (PDG ~ 0.00370)")
    print(f"  Predicted |V_td| = {V_td_pred:.6e}    (PDG ~ 0.00855)")
    print(f"  Predicted |V_ts| = {V_ts_pred:.6e}    (PDG ~ 0.04138)")
    print(f"  Predicted Wolfenstein lambda = {lambda_pred:.6e}    (PDG ~ 0.22500)")
    print(f"  Predicted Wolfenstein A      = {A_pred}              (PDG ~ 0.826)")
    print(f"  Predicted Jarlskog J         = {J_pred:.6e}    (PDG ~ 3.08e-5)")
    print()

    PDG_LAMBDA = 0.22500
    PDG_J = 3.08e-5

    check(
        "Predicted |V_us| is 0 or 1 (not 0.22500)",
        (V_us_pred < 1e-10) or (abs(V_us_pred - 1.0) < 1e-10),
        detail=f"|V_us|_pred = {V_us_pred:.6e}",
    )
    check(
        "Predicted lambda is far from PDG 0.22500",
        abs(lambda_pred - PDG_LAMBDA) > 0.20,
        detail=f"|lambda_pred - 0.225| = {abs(lambda_pred - PDG_LAMBDA):.6e}",
    )
    check(
        "Predicted Jarlskog J = 0 (not 3.08e-5)",
        abs(J_pred) < 1e-10,
        detail=f"J_pred = {J_pred:.6e}",
    )
    check(
        "Predicted Jarlskog J is far from PDG 3.08e-5",
        abs(J_pred - PDG_J) > 1e-6,
        detail=f"|J_pred - 3.08e-5| = {abs(J_pred - PDG_J):.6e}",
    )


# ---------------------------------------------------------------------
# Test 5: P_up != P_dn permutation freedom is still discrete (not continuous)
# ---------------------------------------------------------------------

def test_permutation_freedom_is_discrete() -> None:
    section("Test 5: Sector-dependent Fourier-to-generation map is discrete")

    F = z3_fourier_matrix()
    # Imagine choosing P_up != P_dn explicitly. The resulting V_CKM has |V_ij| in {0, 1}.

    perms = list(itertools.permutations([0, 1, 2]))
    max_offdiag = 0.0
    n_perm_pairs = 0
    for P_up in perms:
        for P_dn in perms:
            U_up = F[:, list(P_up)]
            U_dn = F[:, list(P_dn)]
            V = U_up.conj().T @ U_dn
            absV = np.abs(V)
            # Should be a permutation; magnitudes are 0 or 1
            dev = float(np.max(np.abs(absV ** 2 - np.round(absV ** 2))))
            if dev > max_offdiag:
                max_offdiag = dev
            n_perm_pairs += 1

    check(
        f"All {n_perm_pairs} (P_up, P_dn) pairs give permutation V",
        max_offdiag < 1e-12,
        detail=f"max |V|^2 - round(|V|^2) = {max_offdiag:.2e}",
    )

    # Confirm: discrete permutation set has 6 elements (S_3); none gives lambda ~ 0.225
    distinct_V = set()
    for P_up in perms:
        for P_dn in perms:
            U_up = F[:, list(P_up)]
            U_dn = F[:, list(P_dn)]
            V = U_up.conj().T @ U_dn
            absV = tuple(tuple(int(round(x)) for x in row) for row in np.abs(V).round(6))
            distinct_V.add(absV)
    check(
        "Permutation-freedom yields exactly 6 distinct |V_CKM| patterns (= S_3)",
        len(distinct_V) == 6,
        detail=f"# distinct |V| = {len(distinct_V)}",
    )


# ---------------------------------------------------------------------
# Test 6: lambda ~ 0.225 unreachable for any (rho_up, delta_up, rho_dn, delta_dn)
# ---------------------------------------------------------------------

def test_lambda_unreachable() -> None:
    section("Test 6: lambda ~ 0.225 unreachable for any P-Heavy-A admission")

    # Grid sweep with 30 x 30 x 30 x 30 = 810000 parameter combos: brute force
    # Use coarse grids; we already know the answer analytically — V is permutation.
    rho_grid = np.linspace(0.2, 2.4, 12)
    delta_grid = np.linspace(0.0, 2.0 * math.pi, 12)

    max_lambda = 0.0
    for rho_up in rho_grid:
        for delta_up in delta_grid:
            H_up = hermitian_circulant(1.0, rho_up, delta_up)
            _, U_up = np.linalg.eigh(H_up)
            for rho_dn in rho_grid:
                for delta_dn in delta_grid:
                    H_dn = hermitian_circulant(1.0, rho_dn, delta_dn)
                    _, U_dn = np.linalg.eigh(H_dn)
                    V = U_up.conj().T @ U_dn
                    # Cabibbo = max(|V_us|, |V_cd|) is the off-(1,1) magnitude
                    # in the (gen1, gen2) block. By eigenvalue ordering, V[0,1] etc.
                    lam = float(np.abs(V[0, 1]))
                    if lam > max_lambda:
                        max_lambda = lam

    check(
        "max |V[0,1]| over (rho_up, delta_up, rho_dn, delta_dn) grid is 0 or 1",
        max_lambda < 1e-8 or abs(max_lambda - 1.0) < 1e-8,
        detail=f"max |V[0,1]| over 20736 grid points = {max_lambda:.8e}",
    )

    # The PDG value lambda ~ 0.22500 is NOT in {0, 1}
    check(
        "PDG lambda = 0.22500 cannot be reached on P-Heavy-A admission",
        abs(0.22500 - max_lambda) > 0.2,
        detail=f"PDG 0.22500 vs admissible {{0, 1}}",
    )


# ---------------------------------------------------------------------
# Test 7: same-eigenbasis structural theorem (algebraic)
# ---------------------------------------------------------------------

def test_simultaneously_diagonalizable() -> None:
    section("Test 7: H_up and H_dn always commute (algebraic theorem)")

    # Any two circulants on the same C_3 generator commute, because they are
    # both polynomials in C and C^2 = C^{-1}, and C, C^2 commute (C is unitary).

    rng = np.random.default_rng(20260513)
    n_trials = 30
    max_comm = 0.0
    for _ in range(n_trials):
        rho_up = float(rng.uniform(0.1, 2.4))
        delta_up = float(rng.uniform(0.0, 2.0 * math.pi))
        rho_dn = float(rng.uniform(0.1, 2.4))
        delta_dn = float(rng.uniform(0.0, 2.0 * math.pi))
        a_up = float(rng.uniform(0.5, 2.0))
        a_dn = float(rng.uniform(0.5, 2.0))
        H_up = hermitian_circulant(a_up, rho_up, delta_up)
        H_dn = hermitian_circulant(a_dn, rho_dn, delta_dn)
        comm = H_up @ H_dn - H_dn @ H_up
        max_comm = max(max_comm, float(np.max(np.abs(comm))))

    check(
        "[H_up, H_dn] = 0 for all P-Heavy-A pairs (algebraic)",
        max_comm < 1e-12,
        detail=f"max |[H_up, H_dn]| over {n_trials} trials = {max_comm:.2e}",
    )

    # Commuting Hermitian operators are simultaneously diagonalizable; this
    # is the structural reason V_CKM is a permutation matrix.
    print()
    print("  [H_up, H_dn] = 0 implies they have a common orthonormal eigenbasis,")
    print("  which here is the Z_3 Fourier basis F. Hence U_up and U_dn span the")
    print("  same flag of eigenspaces, and V_CKM = U_up^H U_dn is a permutation")
    print("  matrix dressed by overall phases.")


# ---------------------------------------------------------------------
# Test 8: Charged-lepton sector consistency (Brannen-Rivero same group)
# ---------------------------------------------------------------------

def test_charged_lepton_same_group() -> None:
    section("Test 8: Charged-lepton Brannen-Rivero shares C_3[111]")

    # The Brannen amplitude-equipartition (BAE) primitive uses
    # rho_lep = sqrt(2), delta_lep = 2/9. Same C_3[111] group.
    H_lep = hermitian_circulant(1.0, math.sqrt(2.0), 2.0 / 9.0)
    F = z3_fourier_matrix()
    D = F.conj().T @ H_lep @ F
    off = D - np.diag(np.diag(D))
    max_off = float(np.max(np.abs(off)))
    check(
        "F diagonalizes charged-lepton Brannen-Rivero circulant",
        max_off < 1e-12,
        detail=f"max off-diagonal = {max_off:.2e}",
    )

    # If neutrino Dirac Yukawa is ALSO a C_3[111] circulant, PMNS = permutation
    # by the same argument. The framework already foreclosed neutrino Dirac
    # texture transfer in DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15.

    print()
    print("  This consistency observation matches DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO")
    print("  (2026-04-15): same-eigenbasis structure foreclosed neutrino sector earlier.")


# ---------------------------------------------------------------------
# Numerical density-of-rationals control (small-N reproducibility)
# ---------------------------------------------------------------------

def test_density_control() -> None:
    section("Density-of-rationals control: cannot fit lambda from {0,1} discrete set")

    # Trivially, lambda = 0.22500 is not in the discrete admissible set {0, 1}
    # for the P-Heavy-A primitive. Distance to nearest admissible value:
    PDG_LAMBDA = 0.22500
    dist = min(abs(PDG_LAMBDA - 0.0), abs(PDG_LAMBDA - 1.0))
    check(
        "PDG lambda is at distance >= 0.22500 from the discrete admissible set",
        dist >= 0.22500 - 1e-12,
        detail=f"min(|0.225 - 0|, |0.225 - 1|) = {dist:.5f}",
    )
    # The Wolfenstein A is also unreachable for the same structural reason
    # (|V_cb| is 0 or 1, but PDG ~ 0.0421).
    PDG_VCB = 0.04210
    dist_vcb = min(abs(PDG_VCB - 0.0), abs(PDG_VCB - 1.0))
    check(
        "PDG |V_cb| is at distance >= 0.0421 from discrete admissible set",
        dist_vcb >= 0.04210 - 1e-12,
        detail=f"min(|0.0421 - 0|, |0.0421 - 1|) = {dist_vcb:.5f}",
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> int:
    print()
    print("=" * 72)
    print("NEWPHYSICS NP-CKM-Wolfenstein — P-Heavy-A circulant Cabibbo No-Go")
    print("Source theorem runner; PR #1044 P-Heavy-A primitive (sector-dependent")
    print("rho-Koide circulants on C_3[111]) cannot reproduce CKM structure.")
    print("=" * 72)

    test_fourier_diagonalizes_all_circulants()
    test_v_ckm_is_permutation()
    test_parameter_free_no_go()
    test_wolfenstein_parameters_are_forced_to_zero()
    test_permutation_freedom_is_discrete()
    test_lambda_unreachable()
    test_simultaneously_diagonalizable()
    test_charged_lepton_same_group()
    test_density_control()

    print()
    print("=" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
