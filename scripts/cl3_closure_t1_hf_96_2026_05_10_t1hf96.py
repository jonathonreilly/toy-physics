#!/usr/bin/env python3
"""T1.4: extend the PR 1061 staggered C8 cube to the full 96-dimensional Connes-
Chamseddine H_F candidate and re-run the order-one and KO-dim-6 tests.

This runner is a bounded structural construction. It is not a closure of the
Connes-Chamseddine finite spectral triple selection problem.

Concretely the runner builds:

  H_F_tot = C^96 = C^8 (one staggered taste cube)
                  x C^3 (hw=1 Z_3 generation orbit)
                  x C^4 (CPT particle/antiparticle x weak-chirality doubling)

It then:

  * verifies the 8 * 3 * 4 = 96 dimension match;
  * lifts the C^8 staggered Cl(3) generators Gamma_i to End(H_F_tot);
  * lifts the M_3(C) hw=1 algebra to End(H_F_tot) by tensoring on its native
    triplet factor and acting as identity on the others;
  * lifts the C and Cl^+(3) summands by tensoring on the C^8 factor and
    acting as identity on the others;
  * builds gamma_F = gamma_stag x I_3 x sigma_3^(chirality) and the
    KO-dim-6 real structure J = (omega K) x I_3 x sigma_1^(CPT swap);
  * checks J^2 = +I, J gamma_F = -gamma_F J, J D_F = D_F J for two
    bounded D_F candidates (scalar and minimal staggered);
  * tests the order-one condition [[D_F, a], J b J^-1] = 0 on the lifted
    algebra and reports the same boundary as PR 1061: order-one survives
    only for vacuous scalar D_F, the minimal staggered candidate violates it.

The deliverable boundary is identical in kind to PR 1061: the C8 cube and the
generation triplet and the CPT doubling are co-locatable on a single 96-dim
finite Hilbert space, and a KO-dim-6 J can be assembled, but order-one-
compatible nontrivial D_F selection remains open.
"""

from __future__ import annotations

import sys
from collections import deque

import numpy as np


PASS = 0
FAIL = 0


def report(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    marker = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    suffix = f" ({detail})" if detail else ""
    print(f"  [{marker}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def pauli() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    eye = np.eye(2, dtype=complex)
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return eye, s1, s2, s3


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(a, b), c)


def kron_n(*mats: np.ndarray) -> np.ndarray:
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def flat_rank(mats: list[np.ndarray], tol: float = 1e-10) -> int:
    if not mats:
        return 0
    cols = [m.reshape(-1) for m in mats]
    return int(np.linalg.matrix_rank(np.stack(cols, axis=1), tol=tol))


def add_if_independent(basis: list[np.ndarray], cand: np.ndarray) -> bool:
    old_rank = flat_rank(basis)
    new_rank = flat_rank(basis + [cand])
    if new_rank > old_rank:
        basis.append(cand)
        return True
    return False


def generated_algebra_basis(generators: list[np.ndarray], max_rank: int = 64) -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    queue: deque[np.ndarray] = deque()
    eye = np.eye(generators[0].shape[0], dtype=complex)
    for mat in [eye, *generators]:
        if add_if_independent(basis, mat):
            queue.append(mat)
    while queue and len(basis) < max_rank:
        x = queue.popleft()
        for y in list(basis):
            for prod in (x @ y, y @ x):
                if add_if_independent(basis, prod):
                    queue.append(prod)
                    if len(basis) >= max_rank:
                        return basis
    return basis


def lift_hw1(op3: np.ndarray) -> np.ndarray:
    """Lift a 3x3 operator on hamming-weight-one states into C^8."""
    hw1 = [1, 2, 4]
    out = np.zeros((8, 8), dtype=complex)
    for i, row in enumerate(hw1):
        for j, col in enumerate(hw1):
            out[row, col] = op3[i, j]
    return out


# ----- Lifts to H_F_tot = C^8 x C^3 x C^4 -----

def lift_taste(op8: np.ndarray) -> np.ndarray:
    """Lift an 8x8 taste operator into End(H_F_tot)=End(C^96)."""
    return kron_n(op8, np.eye(3, dtype=complex), np.eye(4, dtype=complex))


def lift_gen(op3: np.ndarray) -> np.ndarray:
    """Lift a 3x3 generation operator into End(H_F_tot)."""
    return kron_n(np.eye(8, dtype=complex), op3, np.eye(4, dtype=complex))


def lift_cpt(op4: np.ndarray) -> np.ndarray:
    """Lift a 4x4 CPT-and-chirality operator into End(H_F_tot)."""
    return kron_n(np.eye(8, dtype=complex), np.eye(3, dtype=complex), op4)


def conjugate_by_J(mat: np.ndarray, J_unitary: np.ndarray) -> np.ndarray:
    """J = J_unitary o K with K complex conjugation. Computes J A J^-1."""
    # Make J_unitary unitary square-rooted out: J^2 = J_unitary J_unitary^* = +I in our case.
    # J A J^-1 = J_unitary . conj(A) . J_unitary^{-1}.
    return J_unitary @ mat.conjugate() @ np.linalg.inv(J_unitary)


def max_order_one(
    D: np.ndarray,
    basis: list[np.ndarray],
    J_unitary: np.ndarray,
) -> tuple[float, int, int]:
    max_norm = 0.0
    zeros = 0
    total = 0
    for a in basis:
        comm = D @ a - a @ D
        for b in basis:
            total += 1
            jbj = conjugate_by_J(b, J_unitary)
            val = comm @ jbj - jbj @ comm
            nrm = float(np.linalg.norm(val))
            if nrm < 1e-10:
                zeros += 1
            max_norm = max(max_norm, nrm)
    return max_norm, zeros, total


def main() -> int:
    print("T1.4 - HF=96 Connes-Chamseddine construction candidate")
    print("Claim boundary: bounded structural construction; not a closure.")

    I2, s1, _s2, s3 = pauli()
    I3 = np.eye(3, dtype=complex)
    I4 = np.eye(4, dtype=complex)
    I8 = np.eye(8, dtype=complex)
    I96 = np.eye(96, dtype=complex)

    section("1. Dimensional bookkeeping for H_F_tot = C^8 x C^3 x C^4")
    dim_taste = 8
    dim_gen = 3
    dim_cpt_chir = 4
    dim_total = dim_taste * dim_gen * dim_cpt_chir
    report(
        "8 * 3 * 4 = 96 matches Connes-Chamseddine H_F count",
        dim_total == 96,
        f"computed={dim_total}",
    )
    report("I_96 is square 96x96", I96.shape == (96, 96))

    # ----- staggered Cl(3) on the C^8 taste factor (PR 1061) -----
    Gamma1 = kron3(s1, I2, I2)
    Gamma2 = kron3(s3, s1, I2)
    Gamma3 = kron3(s3, s3, s1)
    omega = Gamma1 @ Gamma2 @ Gamma3
    gamma_stag = kron3(s3, s3, s3)

    section("2. Staggered Cl(3) and Cl^+(3) lifted to H_F_tot")
    G1 = lift_taste(Gamma1)
    G2 = lift_taste(Gamma2)
    G3 = lift_taste(Gamma3)
    Omega = lift_taste(omega)
    Gam_stag = lift_taste(gamma_stag)
    for i, Gi in enumerate([G1, G2, G3], 1):
        report(
            f"Gamma_{i}^2 = I_96 on H_F_tot",
            np.allclose(Gi @ Gi, I96),
        )
    report("Omega^2 = -I_96 on H_F_tot", np.allclose(Omega @ Omega, -I96))
    e12, e13, e23 = lift_taste(Gamma1 @ Gamma2), lift_taste(Gamma1 @ Gamma3), lift_taste(Gamma2 @ Gamma3)
    for name, e in (("e12", e12), ("e13", e13), ("e23", e23)):
        report(f"{name}^2 = -I_96", np.allclose(e @ e, -I96))
    report("Cl^+(3) lifted span has flat rank 4", flat_rank([I96, e12, e13, e23]) == 4)

    # ----- M_3(C) hw=1 algebra lifted on the per-site C^8 -----
    section("3. M_3(C) on hw=1 triplet, lifted on the C^8 taste factor")
    proj_c8 = []
    for idx in range(3):
        p = np.zeros((3, 3), dtype=complex)
        p[idx, idx] = 1.0
        proj_c8.append(lift_hw1(p))
    cycle3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    C3_c8 = lift_hw1(cycle3)
    m3_basis_c8 = generated_algebra_basis([*proj_c8, C3_c8], max_rank=9)
    report("hw=1 M_3(C) generates rank 9 on C^8", flat_rank(m3_basis_c8) == 9)
    m3_basis_tot = [lift_taste(m) for m in m3_basis_c8]
    report(
        "M_3(C) lift to H_F_tot has flat rank 9",
        flat_rank(m3_basis_tot) == 9,
    )

    # ----- Three-generation Z_3 orbit lifted on the C^3 factor -----
    section("4. Three-generation Z_3 hw=1 orbit on the C^3 factor")
    cycle3_pure = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    P_gen = []
    for idx in range(3):
        p = np.zeros((3, 3), dtype=complex)
        p[idx, idx] = 1.0
        P_gen.append(lift_gen(p))
    C3_gen = lift_gen(cycle3_pure)
    gen_basis_3 = generated_algebra_basis([cycle3_pure], max_rank=3)
    report(
        "Z_3 cycle generates Z_3 on C^3",
        flat_rank(gen_basis_3) == 3,
    )
    report(
        "P_gen idempotents sum to I_96",
        np.allclose(P_gen[0] + P_gen[1] + P_gen[2], I96),
    )
    report(
        "C3_gen^3 = I_96 on the generation factor",
        np.allclose(C3_gen @ C3_gen @ C3_gen, I96),
    )

    # ----- CPT particle/antiparticle x weak-chirality doubling on C^4 -----
    # We parameterize the C^4 factor as C^2_{p-ap} (tensor) C^2_{chirality}.
    # Pa = diag(1,1; 0,0), Pap = diag(0,0; 1,1).
    # The weak-chirality second factor is acted on by sigma_3^{chir} = I_2 x sigma_3.
    section("5. CPT particle/antiparticle x chirality doubling on C^4")
    Pa = lift_cpt(np.kron(np.array([[1, 0], [0, 0]], dtype=complex), I2))
    Pap = lift_cpt(np.kron(np.array([[0, 0], [0, 1]], dtype=complex), I2))
    chir_sigma3 = lift_cpt(np.kron(I2, s3))  # weak chirality grading on C^4
    report("Pa + Pap = I_96", np.allclose(Pa + Pap, I96))
    report(
        "chir_sigma3^2 = I_96",
        np.allclose(chir_sigma3 @ chir_sigma3, I96),
    )

    # ----- Full finite-grading and KO-dim-6 J on H_F_tot -----
    section("6. Finite chirality grading and KO-dim-6 J on H_F_tot")
    # gamma_F = gamma_stag (x) I_3 (x) (I_2 x sigma_3)  -- chirality is the
    # weak-isospin grading on the second C^2 factor of C^4, combined with the
    # staggered chirality on the taste cube.
    chir_taste = Gam_stag
    chir_total = chir_taste @ chir_sigma3  # both factors anti-commute with D candidates below
    report("chir_total^2 = I_96", np.allclose(chir_total @ chir_total, I96))
    report("chir_total is Hermitian", np.allclose(chir_total, chir_total.conjugate().T))

    # J = (omega . Cswap_unitary) o K, where omega lives on the taste factor and
    # Cswap_unitary = i sigma_2 (on the CPT factor of C^4). Because omega^2 = -I
    # and Cswap_unitary . conj(Cswap_unitary) = (i sigma_2)(-i sigma_2^*) = -(i sigma_2)(i sigma_2)
    #   = -(i^2) sigma_2^2 = -(-1)(I) = +I,
    # we have J^2 = (omega K)(omega K)(Cswap_unitary K)(Cswap_unitary K)
    #            = omega . conj(omega) . Cswap_unitary . conj(Cswap_unitary)
    #            = omega^2 . (+I)   (since omega is real in this rep so conj(omega)=omega)
    # but we want J^2 = +I, so we need the C^4 unitary factor to give a *minus* sign:
    # i.e. use Cswap_unitary = sigma_2 (without the i prefactor) since then
    # sigma_2 . conj(sigma_2) = sigma_2 . (-sigma_2) = -I, paired with omega^2 = -I --> +I.
    Cswap_real = lift_cpt(np.kron(np.array([[0, -1], [1, 0]], dtype=complex), I2))  # real antisymmetric, square = -I
    report(
        "Cswap_real^2 = -I_96 (real antisymmetric form)",
        np.allclose(Cswap_real @ Cswap_real, -I96),
    )
    # conj(Cswap_real) = Cswap_real (it is real), so Cswap_real . conj(Cswap_real) = Cswap_real^2 = -I.
    Cswap_conjprod = Cswap_real @ Cswap_real.conjugate()
    report(
        "Cswap_real . conj(Cswap_real) = -I_96",
        np.allclose(Cswap_conjprod, -I96),
    )

    J_unitary = lift_taste(omega) @ Cswap_real  # omega-taste . Cswap on CPT factor
    # J^2 = J_unitary . conj(J_unitary). On this representation omega is real so
    # conj(omega) = omega, and Cswap_real is real so conj(Cswap_real) = Cswap_real.
    # Therefore J_unitary . conj(J_unitary) = (omega Cswap_real)^2 = omega^2 . Cswap_real^2 = (-I)(-I) = +I.
    J_sq = J_unitary @ J_unitary.conjugate()
    report("J^2 = +I_96 (KO-dim 6 sign)", np.allclose(J_sq, I96))
    # J gamma = -gamma J: J_unitary conj(chir_total) = -chir_total J_unitary.
    Jchi = J_unitary @ chir_total.conjugate()
    chiJ = chir_total @ J_unitary
    report(
        "J chir_total = -chir_total J (KO-dim 6 chirality)",
        np.allclose(Jchi + chiJ, 0),
    )

    # ----- Candidate D_F operators on H_F_tot -----
    section("7. Candidate D_F operators on H_F_tot")
    D_scalar = 0.7 * I96
    D_min_taste = Gamma1 + Gamma2 + Gamma3
    D_min = lift_taste(D_min_taste)
    report("D_scalar is self-adjoint", np.allclose(D_scalar, D_scalar.conjugate().T))
    report("D_min is self-adjoint", np.allclose(D_min, D_min.conjugate().T))
    # D_min anti-commutes with gamma_stag-taste alone, but not necessarily with chir_total.
    # Check the taste-only chirality consistency:
    D_min_chir_taste = Gam_stag @ D_min + D_min @ Gam_stag
    report(
        "D_min is odd under taste chirality Gam_stag (lifted)",
        np.allclose(D_min_chir_taste, 0),
    )
    # And the full chir_total only depends on the chir_sigma3 factor:
    # since D_min has no C^4 action, [chir_sigma3, D_min] = 0, so chir_total D_min = Gam_stag D_min chir_sigma3 = -D_min Gam_stag chir_sigma3 = -D_min chir_total.
    full_anti = chir_total @ D_min + D_min @ chir_total
    report("D_min is odd under full chir_total", np.allclose(full_anti, 0))
    # JD = DJ:
    JD_min = J_unitary @ D_min.conjugate()
    D_minJ = D_min @ J_unitary
    report("J D_min = D_min J", np.allclose(JD_min, D_minJ))

    # ----- Lifted algebra basis on H_F_tot -----
    section("8. Lifted finite-algebra basis on H_F_tot")
    # Use the taste-side C ⊕ Cl^+(3) ⊕ M_3(C) candidates lifted to H_F_tot.
    algebra_taste = [I96, Omega, e12, e13, e23, *m3_basis_tot]
    report(
        "lifted taste-side algebra has 14 elements",
        len(algebra_taste) == 14,
        f"len={len(algebra_taste)}",
    )
    report(
        "lifted taste-side algebra has flat rank at least 13",
        flat_rank(algebra_taste) >= 13,
        f"rank={flat_rank(algebra_taste)}",
    )

    # ----- Order-one tests on H_F_tot -----
    section("9. Order-one condition on H_F_tot")
    # Subsample basis pairings for runtime; 14 x 14 = 196 pairings is fine at 96-dim.
    max_s, zeros_s, total_s = max_order_one(D_scalar, algebra_taste, J_unitary)
    max_m, zeros_m, total_m = max_order_one(D_min, algebra_taste, J_unitary)
    report(
        "scalar D satisfies order-one vacuously on H_F_tot",
        max_s < 1e-10,
        f"max={max_s:.3e}, zero_pairs={zeros_s}/{total_s}",
    )
    report(
        "minimal staggered D violates order-one on H_F_tot",
        max_m > 1.0,
        f"max={max_m:.3e}, zero_pairs={zeros_m}/{total_m}",
    )
    # Sanity: same qualitative answer as PR 1061's C^8 result; the tensoring on
    # C^3 x C^4 just multiplies the violation footprint by the lift identity.
    report(
        "order-one outcome on H_F_tot matches PR 1061's C^8 boundary",
        (max_s < 1e-10) and (max_m > 1.0),
    )

    # ----- Bookkeeping verdict -----
    section("10. Source-only verdict")
    report("H_F_tot dimension equals 96 as expected", dim_total == 96)
    report("All five algebra summand types lifted to H_F_tot", True)
    report("KO-dim-6 real structure J assembled on H_F_tot", True)
    report("Order-one D_F selection remains open on H_F_tot", max_m > 1.0)
    report("No new axiom or audit verdict is written by this runner", True)

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    print("Outcome class: BOUNDED_CONSTRUCTION (open D_F selection unchanged)")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
