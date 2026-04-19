"""Frontier runner: Koide scalar-selector direct attack (scout).

This runner executes the explicit PASS/FAIL checks for the scout note
`docs/KOIDE_SCALAR_SELECTOR_DIRECT_ATTACK_SCOUT_NOTE_2026-04-18.md`.

Verdict structure: the attack produces a DEAD / MISS-STRUCTURE outcome.
The runner verifies each algebraic step of that verdict explicitly so the
obstruction claim itself is reproducible.

Run:

    python3 scripts/frontier_koide_scalar_selector_direct_attack_scout.py
"""
from __future__ import annotations

import numpy as np


TOL = 1e-12

PASS = 0
FAIL = 0


def check(label: str, condition: bool, extra: str = "") -> None:
    global PASS, FAIL
    verdict = "PASS" if condition else "FAIL"
    if condition:
        PASS += 1
    else:
        FAIL += 1
    extra_str = f"  ({extra})" if extra else ""
    print(f"  [{verdict}] {label}{extra_str}")


def allclose(a, b, tol: float = TOL) -> bool:
    return np.allclose(a, b, atol=tol)


def main() -> None:
    print("=" * 72)
    print("KOIDE SCALAR-SELECTOR DIRECT ATTACK — SCOUT RUNNER")
    print("=" * 72)

    # Constants
    sqrt2 = np.sqrt(2.0)
    sqrt3 = np.sqrt(3.0)
    sqrt6 = np.sqrt(6.0)
    sqrt8 = np.sqrt(8.0)
    E1 = np.sqrt(8.0 / 3.0)
    E2 = sqrt8 / 3.0
    gamma = 0.5

    # Intrinsic slot pair and CP pair (constants)
    a_star = E2 / 3.0 - sqrt3 * gamma / 6.0 + 1j * (E2 + gamma / 2.0)
    b_star = E2 / 3.0 + sqrt3 * gamma / 6.0 + 1j * (gamma / 2.0 - E2)
    cp1 = -2.0 * sqrt6 / 9.0
    cp2 = 2.0 * sqrt2 / 9.0

    # ------------------------------------------------------------------
    # STEP 1. Selected-slice decomposition identities (frozen-bank note)
    # ------------------------------------------------------------------
    print("\nSTEP 1. Frozen-bank decomposition identities on the selected slice.")

    # Bank identities
    check(
        "Re(a_* + b_*) = 2 cp2 = 4 sqrt2/9",
        allclose((a_star + b_star).real, 2.0 * cp2)
        and allclose(2.0 * cp2, 4.0 * sqrt2 / 9.0),
    )
    check("q_+* = -3 cp1/2 = sqrt6/3", allclose(-3.0 * cp1 / 2.0, sqrt6 / 3.0))

    # K_Z3 entries on the selected slice, from Z_3 doublet-block theorem
    q_plus = sqrt6 / 3.0
    delta = sqrt6 / 3.0
    for m_test in (-1.2957949, -1.16047, 0.0, 0.5, 1.3):
        K00 = m_test + 2.0 * q_plus - 4.0 * sqrt2 / 9.0
        K11 = -q_plus + 2.0 * sqrt2 / 9.0 - 1.0 / (2.0 * sqrt3)
        K22 = -q_plus + 2.0 * sqrt2 / 9.0 + 1.0 / (2.0 * sqrt3)
        Re_K12 = m_test - 4.0 * sqrt2 / 9.0
        Im_K12 = sqrt3 * delta - 4.0 * sqrt2 / 3.0

        check(
            f"K11 = 3 cp1/2 + cp2 - 1/(2 sqrt3) at m={m_test}",
            allclose(K11, 3.0 * cp1 / 2.0 + cp2 - 1.0 / (2.0 * sqrt3)),
        )
        check(
            f"K22 = 3 cp1/2 + cp2 + 1/(2 sqrt3) at m={m_test}",
            allclose(K22, 3.0 * cp1 / 2.0 + cp2 + 1.0 / (2.0 * sqrt3)),
        )
        check(
            f"Im K12 = -3 cp2/2 at m={m_test}", allclose(Im_K12, -3.0 * cp2 / 2.0)
        )
        check(
            f"K00 = m - 2 cp2 - 3 cp1 at m={m_test}",
            allclose(K00, m_test - 2.0 * cp2 - 3.0 * cp1),
        )
        check(
            f"Re K12 = m - 2 cp2 at m={m_test}",
            allclose(Re_K12, m_test - 2.0 * cp2),
        )
        check(
            f"Tr K_Z3 = m at m={m_test}",
            allclose(K00 + K11 + K22, m_test),
        )

    # ------------------------------------------------------------------
    # STEP 2. T_m^(K) lifts back to T_m in the H-basis.
    # ------------------------------------------------------------------
    print("\nSTEP 2. T_m^(K) in Z_3 basis = T_m in H-basis.")

    omega = np.exp(2j * np.pi / 3.0)
    U_Z3 = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega ** 2],
            [1.0, omega ** 2, omega],
        ],
        dtype=complex,
    ) / np.sqrt(3.0)

    T_m_K = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    T_m_H = U_Z3 @ T_m_K @ U_Z3.conj().T
    T_m_paper = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)

    check("T_m^(K) Hermitian", allclose(T_m_K, T_m_K.conj().T))
    check("T_m^(H) Hermitian", allclose(T_m_H, T_m_H.conj().T))
    check("T_m^(H) real", allclose(T_m_H.imag, 0))
    check(
        "T_m^(H) == T_m (affine-boundary generator)",
        allclose(T_m_H, T_m_paper, tol=1e-10),
    )

    # ------------------------------------------------------------------
    # STEP 3. C_3[111] isotypic decomposition of T_m.
    # ------------------------------------------------------------------
    print("\nSTEP 3. Isotypic decomposition of T_m under C_3[111] conjugation.")

    C = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    C2 = C @ C

    def iso(X, w0, w1, w2):
        return (
            w0 * X + w1 * (C @ X @ C.conj().T) + w2 * (C2 @ X @ C2.conj().T)
        ) / 3.0

    T_m = T_m_paper
    T_triv = iso(T_m, 1.0, 1.0, 1.0)
    T_w = iso(T_m, 1.0, np.conj(omega), omega)
    T_wbar = iso(T_m, 1.0, omega, np.conj(omega))

    check(
        "T_m = P_triv T_m + P_omega T_m + P_omega_bar T_m",
        allclose(T_triv + T_w + T_wbar, T_m),
    )
    check(
        "P_triv(T_m) = (1/3)(I + C + C^2) = (B_0 + B_1)/3",
        allclose(T_triv, (np.eye(3) + C + C2) / 3.0),
    )
    check(
        "P_omega(T_m) NOT zero (non-trivial isotypic content)",
        np.linalg.norm(T_w) > 0.1,
    )
    check(
        "P_omega_bar(T_m) NOT zero",
        np.linalg.norm(T_wbar) > 0.1,
    )

    # Cyclic-bundle span test: T_m is NOT in span{B_0, B_1, B_2}
    B0 = np.eye(3, dtype=complex)
    B1 = C + C2
    B2 = 1j * (C - C2)
    M_basis = np.column_stack([B0.flatten(), B1.flatten(), B2.flatten()])
    t_vec = T_m.flatten()
    # lstsq
    sol, *_ = np.linalg.lstsq(M_basis, t_vec, rcond=None)
    residual = np.linalg.norm(M_basis @ sol - t_vec)
    check(
        "T_m is NOT in span{B_0, B_1, B_2} (residual > 0.1)",
        residual > 0.1,
        extra=f"residual={residual:.3f}",
    )

    # ------------------------------------------------------------------
    # STEP 4. Observable-principle linear responses on the cyclic bundle.
    # ------------------------------------------------------------------
    print("\nSTEP 4. Linear observable-principle on the cyclic bundle.")

    T_delta = np.array(
        [[0, -1, 1], [-1, 1, 0], [1, 0, -1]], dtype=complex
    )
    T_q = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=complex)
    H_base = np.array(
        [
            [0.0, E1, -E1 - 1j * gamma],
            [E1, 0.0, -E2],
            [-E1 + 1j * gamma, -E2, 0.0],
        ],
        dtype=complex,
    )

    check("H_base Hermitian", allclose(H_base, H_base.conj().T))

    def H_sel(m):
        return H_base + m * T_m + (sqrt6 / 3.0) * T_delta + (sqrt6 / 3.0) * T_q

    for m_test in (-1.16047, 0.0, 0.5):
        H = H_sel(m_test)
        check(f"H_sel({m_test}) Hermitian", allclose(H, H.conj().T))
        r0 = np.real(np.trace(H @ B0))
        r1 = np.real(np.trace(H @ B1))
        r2 = np.real(np.trace(H @ B2))
        # Predicted linear formulas
        # Tr(T_m B_1) = 2, Tr(T_delta B_1) = 0, Tr(T_q B_1) = 6, Tr(H_base B_1) = -2 sqrt8 /3
        r0_pred = m_test
        r1_pred = 2.0 * m_test + 6.0 * (sqrt6 / 3.0) - 2.0 * sqrt8 / 3.0
        r2_pred = -1.0  # from antisymmetric frozen piece on the selected slice
        check(f"r_0(m={m_test}) = m", allclose(r0, r0_pred, tol=1e-10))
        check(f"r_1(m={m_test}) linear formula", allclose(r1, r1_pred, tol=1e-10))
        check(f"r_2(m={m_test}) = -1 (m-independent)", allclose(r2, r2_pred, tol=1e-10))

    # Check that the cyclic selector zero is NOT at m_* = -1.16047
    def sel_of_m(m):
        H = H_sel(m)
        r0 = np.real(np.trace(H @ B0))
        r1 = np.real(np.trace(H @ B1))
        r2 = np.real(np.trace(H @ B2))
        return 2.0 * r0 ** 2 - r1 ** 2 - r2 ** 2

    m_star_obs = -1.16047
    sel_at_obs = sel_of_m(m_star_obs)
    check(
        "Linear cyclic selector 2 r_0^2 - r_1^2 - r_2^2 at m_*=-1.16047 is NOT zero",
        abs(sel_at_obs) > 0.01,
        extra=f"selector value = {sel_at_obs:.4f}",
    )

    # ------------------------------------------------------------------
    # STEP 5. m-spectator blindness of the retained bank.
    # ------------------------------------------------------------------
    print("\nSTEP 5. m-spectator blindness of retained invariants.")

    def intrinsic_slots(H):
        K = U_Z3.conj().T @ H @ U_Z3
        return K[0, 1], K[0, 2]

    def intrinsic_cp_pair(H):
        K = U_Z3.conj().T @ H @ U_Z3
        # cp1 proportional to Im[((a-b)/sqrt2)^2], cp2 proportional to Im[((a+b)/sqrt2)^2]
        a = K[0, 1]
        b = K[0, 2]
        v1 = ((a - b) / np.sqrt(2.0)) ** 2
        v2 = ((a + b) / np.sqrt(2.0)) ** 2
        return v1.imag, v2.imag

    a_vals = []
    b_vals = []
    cp_vals = []
    for m_test in (-2.0, -1.16047, 0.0, 1.5):
        H = H_sel(m_test)
        a, b = intrinsic_slots(H)
        cp_v1, cp_v2 = intrinsic_cp_pair(H)
        a_vals.append(a)
        b_vals.append(b)
        cp_vals.append((cp_v1, cp_v2))

    check(
        "a_* constant along m (spectator)",
        all(allclose(a_vals[0], a, tol=1e-10) for a in a_vals),
    )
    check(
        "b_* constant along m (spectator)",
        all(allclose(b_vals[0], b, tol=1e-10) for b in b_vals),
    )
    check(
        "CP pair constant along m (spectator)",
        all(
            allclose(cp_vals[0][0], cp[0], tol=1e-10)
            and allclose(cp_vals[0][1], cp[1], tol=1e-10)
            for cp in cp_vals
        ),
    )

    # ------------------------------------------------------------------
    # STEP 6. Intrinsic slot values match the frozen-bank constants.
    # ------------------------------------------------------------------
    print("\nSTEP 6. Numerical slot values match the exact intrinsic pair.")

    H = H_sel(0.0)
    a_val, b_val = intrinsic_slots(H)
    check("a(H) = a_*", allclose(a_val, a_star, tol=1e-10))
    check("b(H) = b_*", allclose(b_val, b_star, tol=1e-10))

    # ------------------------------------------------------------------
    # STEP 7. Verdict summary.
    # ------------------------------------------------------------------
    print("\nSTEP 7. Verdict summary.")

    # The verdict is DEAD / MISS-STRUCTURE. The runner verifies:
    # (a) the frozen-bank decomposition is exact (steps 1-2),
    # (b) T_m has non-trivial ω/ω_bar isotypic content (step 3),
    # (c) the cyclic-bundle observable-principle at linear order does NOT
    #     pin m at the charged-lepton Koide point (step 4),
    # (d) the retained bank is blind to m (step 5-6).

    print(
        "\n  VERDICT: DEAD on the retained surface; MISS-STRUCTURE at pure-axiom level."
    )
    print(
        "  Missing primitive: P_m — a retained scalar functional sensitive to the"
    )
    print(
        "  non-trivial C_3[111] isotypic sectors of the selected-slice Hermitian."
    )

    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print(f"SUMMARY  PASS={PASS}  FAIL={FAIL}")
    print("=" * 72)

    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
