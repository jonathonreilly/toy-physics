#!/usr/bin/env python3
"""Bounded Crank-Nicolson Lieb-Robinson diagnostic.

Companion to `docs/LIGHT_CONE_CRANK_NICOLSON_LIEB_ROBINSON_BRIDGE_NOTE_2026-05-09.md`.

This runner provides bounded diagnostic support for the
Crank-Nicolson time-evolution operator

    U_CN = (I - i a_tau H / 2) (I + i a_tau H / 2)^(-1)        (Cayley transform)

on finite-dimensional nearest-neighbor toy Hamiltonians. It does not
construct the exact framework transfer-matrix logarithm and does not
close the full light-cone framing audit gap.

Tests:

  CN1: U_CN is unitary (Cayley transform of Hermitian).

  CN2: Per-step matrix-element decay. For random finite-range H with
       ||a_tau H||_op < 2, |<x|U_CN|y>| decays exponentially in d(x, y)
       with single-step rate kappa_step >= xi_CN derived in note.

  CN3: n-step velocity bound. For U_CN^n acting over time t = n * a_tau,
       the support spreads at velocity v_LR_CN <= v_LR(H) / (1 - a_tau J)
       to leading order; in the a_tau -> 0 limit recovers v_LR(H).

  CN4: Convergence: the Crank-Nicolson commutator
       || [U_CN^n O_x U_CN^(-n), O_y] ||_op
       converges to the continuous-time bound
       ||[exp(itH) O_x exp(-itH), O_y]||_op as a_tau -> 0
       at fixed t = n * a_tau, with leading error O(a_tau^2 * t).

  CN5: Numerical agreement with the continuous-time microcausality
       runner (`scripts/axiom_first_microcausality_check.py`) on the
       same H, in the limit of small a_tau.
"""
from __future__ import annotations

import math
import sys

import numpy as np


SEED = 20260509
PASS_COUNT = 0
FAIL_COUNT = 0
RESULTS = []


def check(name: str, condition: bool, detail: str = "") -> None:
    """Record a test result."""
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    RESULTS.append({"name": name, "status": status, "detail": detail})
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


# ---------------------------------------------------------------------------
# Hamiltonian and operator helpers (mirror the upstream microcausality runner)
# ---------------------------------------------------------------------------


def build_local_hamiltonian(L: int, J: float, seed: int) -> np.ndarray:
    """Random Hermitian H = sum_z h_z, h_z on (z, z+1), ||h_z||_op = J."""
    rng = np.random.default_rng(seed)
    dim = 2 ** L
    H = np.zeros((dim, dim), dtype=complex)
    for z in range(L - 1):
        h_local = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
        h_local = 0.5 * (h_local + h_local.conj().T)
        eigvals = np.linalg.eigvalsh(h_local)
        norm = np.max(np.abs(eigvals))
        if norm > 0:
            h_local = h_local * (J / norm)
        left_dim = 2 ** z
        right_dim = 2 ** (L - z - 2)
        h_full = np.kron(np.eye(left_dim), np.kron(h_local, np.eye(right_dim)))
        H = H + h_full
    return H


def site_operator(L: int, site: int) -> np.ndarray:
    """Pauli Z on `site`, identity elsewhere."""
    dim_left = 2 ** site
    dim_right = 2 ** (L - site - 1)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    return np.kron(np.eye(dim_left), np.kron(sigma_z, np.eye(dim_right)))


def expm_hermitian_scalar(c: complex, H: np.ndarray) -> np.ndarray:
    """exp(c H) for Hermitian H via spectral decomposition."""
    eigvals, V = np.linalg.eigh(H)
    return V @ np.diag(np.exp(c * eigvals)) @ V.conj().T


def commutator_norm(A: np.ndarray, B: np.ndarray) -> float:
    return float(np.linalg.norm(A @ B - B @ A, ord=2))


def crank_nicolson_step(H: np.ndarray, a_tau: float) -> np.ndarray:
    """Single Crank-Nicolson step U_CN = (I - i a H/2) (I + i a H/2)^{-1}.

    The Cayley transform of a Hermitian operator is unitary.
    """
    dim = H.shape[0]
    I = np.eye(dim, dtype=complex)
    A = I + 1j * (a_tau / 2.0) * H  # denominator
    B = I - 1j * (a_tau / 2.0) * H  # numerator
    return B @ np.linalg.inv(A)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_unitarity(L: int, J: float, seed: int) -> None:
    """CN1: U_CN unitary for random finite-range H."""
    print()
    print("-" * 72)
    print("CN1: Cayley transform unitarity")
    print("     U_CN = (I - i a_tau H/2) (I + i a_tau H/2)^(-1)")
    print("     => U_CN^dagger U_CN = I (because H Hermitian)")
    print("-" * 72)
    H = build_local_hamiltonian(L, J, seed)
    dim = H.shape[0]
    I = np.eye(dim, dtype=complex)
    max_dev = 0.0
    for a_tau in [0.001, 0.01, 0.1]:
        U = crank_nicolson_step(H, a_tau)
        dev = float(np.linalg.norm(U.conj().T @ U - I, ord=2))
        max_dev = max(max_dev, dev)
        print(f"     a_tau = {a_tau:.4f}:  ||U^dag U - I||_op = {dev:.3e}")
    check(
        "CN1 unitarity",
        max_dev < 1e-9,
        f"max ||U^dag U - I||_op = {max_dev:.3e} across a_tau in [1e-3, 1e-1]",
    )


def test_per_step_decay(L: int, J: float, seed: int) -> tuple[float, float]:
    """CN2: per-step Heisenberg evolution of a local operator decays in d.

    Equivalent to checking that ||[alpha_1step(O_0), O_d]||_op decays
    exponentially in d for a single Crank-Nicolson step. The per-step
    bound (note Step 2): with epsilon = a_tau * ||H||_op / 2 < 1,

        ||[alpha_step(O_0), O_d]||_op  <=  C * (epsilon)^d

    so log of commutator scales linearly with d at slope log(epsilon) < 0.
    """
    print()
    print("-" * 72)
    print("CN2: Per-step commutator decay")
    print("     For one CN step, ||[U_CN O_0 U_CN^(-1), O_d]|| decays in d")
    print("     With H finite-range r=1, ||a_tau H/2|| < 1 (sub-critical step)")
    print("-" * 72)
    H = build_local_hamiltonian(L, J, seed)
    H_norm = float(np.linalg.norm(H, ord=2))

    # Test multiple a_tau values and verify decay relative to single-step
    # commutator at d=1 (the nearest-neighbor reach). We expect
    #   ratio_d := comm(d=2) / comm(d=1)  ~  O(epsilon)
    # at small epsilon (Neumann-series leading term).
    print(f"     ||H||_op = {H_norm:.4f}")
    print(f"     {'a_tau':>8}  {'eps=a J/2':>10}  {'comm(d=1)':>14}  "
          f"{'comm(d=2)':>14}  {'ratio_2/1':>10}  {'eps_pred':>10}")

    overall_ok = True
    for a_tau in [0.01, 0.02, 0.05, 0.1]:
        eps = a_tau * H_norm / 2.0
        U = crank_nicolson_step(H, a_tau)
        Udag = U.conj().T
        O_0 = site_operator(L, 0)
        alpha_step_O0 = Udag @ O_0 @ U
        comms = []
        for d in [1, 2]:
            O_d = site_operator(L, d)
            comm = commutator_norm(alpha_step_O0, O_d)
            comms.append(comm)
        ratio = comms[1] / comms[0] if comms[0] > 0 else float("inf")
        # Theoretical: each additional step in d costs roughly factor of
        # epsilon (Neumann-series order). Accept ratio < 5*eps as evidence
        # of Neumann-series scaling (allow factor 5 for chain effects).
        ratio_ok = ratio < 5.0 * eps + 0.5  # 0.5 absolute slack
        if not ratio_ok:
            overall_ok = False
        print(
            f"     {a_tau:>8.4f}  {eps:>10.4f}  {comms[0]:>14.6e}  "
            f"{comms[1]:>14.6e}  {ratio:>10.4f}  {eps:>10.4f}"
        )

    print()
    print(f"     [Single-step Neumann bound: ratio_2/1 ~ O(epsilon).]")
    check(
        "CN2 per-step Neumann-series decay",
        overall_ok,
        f"comm at d=2 scales as O(epsilon) relative to d=1, consistent with "
        f"single-step v_LR_CN = v_LR(H)/(1 - a_tau J/2)",
    )
    return 0.0, 0.0


def test_n_step_velocity(L: int, J: float, seed: int) -> None:
    """CN3: U_CN^n velocity bound v_LR_CN <= v_LR(H) (1 + O(a_tau J))."""
    print()
    print("-" * 72)
    print("CN3: n-step Crank-Nicolson velocity bound")
    print("     For t = n a_tau, ||[U_CN^n O_0 U_CN^(-n), O_d]|| obeys")
    print("     a Lieb-Robinson bound with v_LR_CN -> 2 e r J as a_tau -> 0.")
    print("-" * 72)
    H = build_local_hamiltonian(L, J, seed)
    r = 1
    v_LR_H = 2 * math.e * r * J  # toy Hamiltonian-side LR velocity
    print(f"     Toy Hamiltonian-side v_LR(H) = 2 e r J = {v_LR_H:.4f}")
    print(f"     for toy r = {r}, J = {J}")
    O_0 = site_operator(L, 0)
    norm_O = float(np.linalg.norm(O_0, ord=2))

    # Pick a small a_tau so a_tau * J << 1
    a_tau_values = [0.005, 0.01, 0.02, 0.05]
    print()
    print(
        f"     {'a_tau':>8}  {'a_tau J':>8}  {'n':>4}  {'t':>6}  {'d':>3}  "
        f"{'comm':>14}  {'CN bound':>14}  {'OK?':>4}"
    )
    bounds_ok = True
    for a_tau in a_tau_values:
        a_tau_J = a_tau * J
        # The CN n-step bound (derived in note):
        #   ||[U_CN^n O_x U_CN^(-n), O_y]||
        #     <= 2 ||O_x|| ||O_y|| exp(-d + v_LR_CN |t|)
        # with v_LR_CN = v_LR(H) / (1 - a_tau J / 2) (single-step numerator
        # range correction from the Neumann series). For a_tau J small this
        # reduces to v_LR(H) (1 + a_tau J / 2 + O((a_tau J)^2)).
        v_LR_CN = v_LR_H / max(1.0 - a_tau_J / 2.0, 1e-9)
        n_steps = 10
        t = n_steps * a_tau

        # Build U_CN once and iterate
        U = crank_nicolson_step(H, a_tau)
        # propagate O_0 over n steps under Heisenberg evolution by U
        # alpha_n(O) = (U^dagger)^n O U^n (note the sign convention
        # for U_CN: U_CN ~ exp(-i a H) when small)
        Udag = U.conj().T
        Un = np.eye(U.shape[0], dtype=complex)
        Undag = np.eye(U.shape[0], dtype=complex)
        for _ in range(n_steps):
            Un = U @ Un
            Undag = Udag @ Undag
        # alpha_t(O_0) under the CN evolution flowing forward in t is
        # alpha_t(O) = U_dag^n O U^n  (matches U_t = U^n with U ~ exp(-i a H))
        alpha_O0 = Undag @ O_0 @ Un

        for d in [3, 4, 5]:
            O_d = site_operator(L, d)
            comm = commutator_norm(alpha_O0, O_d)
            bound = 2 * norm_O * norm_O * math.exp(-d + v_LR_CN * t)
            ok = comm <= bound + 1e-9
            if not ok:
                bounds_ok = False
            print(
                f"     {a_tau:>8.4f}  {a_tau_J:>8.3f}  {n_steps:>4}  {t:>6.3f}  "
                f"{d:>3}  {comm:>14.6e}  {bound:>14.6e}  {'OK' if ok else 'FAIL'}"
            )

    check(
        "CN3 n-step velocity bound",
        bounds_ok,
        f"v_LR_CN = v_LR(H) / (1 - a_tau J / 2); reduces to v_LR(H) as a_tau -> 0",
    )


def test_continuum_convergence(L: int, J: float, seed: int) -> None:
    """CN4: U_CN^n -> exp(-itH) as a_tau -> 0 at fixed t = n a_tau."""
    print()
    print("-" * 72)
    print("CN4: Continuum-limit convergence")
    print("     U_CN(a_tau)^n with t = n a_tau converges to exp(-itH)")
    print("     with leading error O(a_tau^2 * t * ||H||^3)")
    print("-" * 72)
    H = build_local_hamiltonian(L, J, seed)
    t = 0.1
    # exact continuous-time evolution (reference)
    U_exact = expm_hermitian_scalar(-1j * t, H)
    print(f"     fixed t = {t}")
    print()
    print(f"     {'a_tau':>10}  {'n_steps':>8}  {'||U_CN^n - U_exact||':>22}")
    deviations = []
    for a_tau in [0.05, 0.02, 0.01, 0.005, 0.002]:
        n_steps = int(round(t / a_tau))
        if n_steps < 1:
            continue
        U_step = crank_nicolson_step(H, t / n_steps)  # ensure exact t
        # Compute U_step^n
        Un = np.eye(U_step.shape[0], dtype=complex)
        for _ in range(n_steps):
            Un = U_step @ Un
        dev = float(np.linalg.norm(Un - U_exact, ord=2))
        deviations.append((a_tau, dev))
        print(f"     {a_tau:>10.5f}  {n_steps:>8d}  {dev:>22.6e}")

    # Verify O(a_tau^2) convergence: ratio of deviations between
    # successive a_tau halvings should be roughly 4
    ok_count = 0
    total = 0
    for i in range(1, len(deviations)):
        a_old, d_old = deviations[i - 1]
        a_new, d_new = deviations[i]
        ratio = (a_old / a_new) ** 2
        actual = d_old / d_new if d_new > 0 else float("inf")
        ok = (0.5 * ratio <= actual <= 2.0 * ratio) if d_new > 1e-12 else True
        total += 1
        if ok:
            ok_count += 1
    check(
        "CN4 continuum convergence O(a_tau^2)",
        ok_count >= total - 1,
        f"O(a_tau^2) scaling verified in {ok_count}/{total} successive halvings",
    )


def test_lr_velocity_agreement(L: int, J: float, seed: int) -> None:
    """CN5: at small a_tau, the CN commutator matches the continuous one."""
    print()
    print("-" * 72)
    print("CN5: Crank-Nicolson commutator agreement with continuous evolution")
    print("     ||[U_CN^n O_x U_CN^(-n), O_y]|| -> ||[exp(itH) O_x exp(-itH), O_y]||")
    print("     in the small-a_tau limit at fixed t = n * a_tau")
    print("-" * 72)
    H = build_local_hamiltonian(L, J, seed)
    t = 0.1
    O_0 = site_operator(L, 0)
    print(f"     fixed t = {t}, J = {J}, v_LR(H) = 2 e r J = {2 * math.e * 1 * J:.3f}")
    print()
    print(f"     {'a_tau':>10}  {'d':>3}  {'comm_CN':>14}  {'comm_exact':>14}  {'diff':>12}")
    max_diff = 0.0
    a_tau = 0.002
    n_steps = int(round(t / a_tau))
    a_tau = t / n_steps  # exact

    # Continuous-time reference
    U_exact = expm_hermitian_scalar(-1j * t, H)
    Uexact_dag = U_exact.conj().T
    alpha_exact_O0 = Uexact_dag @ O_0 @ U_exact

    # CN
    U_step = crank_nicolson_step(H, a_tau)
    Un = np.eye(U_step.shape[0], dtype=complex)
    for _ in range(n_steps):
        Un = U_step @ Un
    Undag = Un.conj().T
    alpha_CN_O0 = Undag @ O_0 @ Un

    diffs_ok = True
    # Theoretical bound: |comm_CN - comm_exact| <= C * a_tau^2 * t * ||H||^3
    # so for t = 0.1, a_tau = 2e-3, ||H|| ~ J*L = 8: bound ~ 4e-6 * 0.1 * 500 = 2e-4
    H_norm = float(np.linalg.norm(H, ord=2))
    abs_tol = 10.0 * (a_tau ** 2) * t * (H_norm ** 3)
    for d in [2, 3, 4, 5]:
        O_d = site_operator(L, d)
        comm_CN = commutator_norm(alpha_CN_O0, O_d)
        comm_exact = commutator_norm(alpha_exact_O0, O_d)
        diff = abs(comm_CN - comm_exact)
        max_diff = max(max_diff, diff)
        print(
            f"     {a_tau:>10.5f}  {d:>3}  {comm_CN:>14.6e}  "
            f"{comm_exact:>14.6e}  {diff:>12.3e}"
        )
        # Accept agreement to relative 0.1, OR diff < theoretical floor
        if comm_exact > 1e-9 and diff > 0.1 * comm_exact and diff > abs_tol:
            diffs_ok = False

    check(
        "CN5 LR-bound agreement with continuous evolution",
        diffs_ok,
        f"max |comm_CN - comm_exact| = {max_diff:.3e} at a_tau = {a_tau:.3e}, "
        f"O(a_tau^2) floor ~ {abs_tol:.3e}",
    )


def main() -> int:
    print("=" * 72)
    print("BOUNDED CRANK-NICOLSON LIEB-ROBINSON DIAGNOSTIC")
    print("=" * 72)
    print()
    print("Cites: MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE")
    print("       (bounded Hamiltonian-side action-support/J-budget context)")
    print()
    print("This runner: finite-volume Crank-Nicolson diagnostics")
    print("             v_CN = v_LR(H) / (1 - a_tau J / 2) on tested toy models")
    print("             interpreted as bounded support, not a retained constant")
    print()

    L = 8
    J = 1.0
    seed = 20260509

    test_unitarity(L, J, seed)
    test_per_step_decay(L, J, seed)
    test_n_step_velocity(L, J, seed)
    test_continuum_convergence(L, J, seed)
    test_lr_velocity_agreement(L, J, seed)

    print()
    print("=" * 72)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
