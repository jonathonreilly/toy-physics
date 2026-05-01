#!/usr/bin/env python3
"""Bridge CPT from the staggered hopping operator D to the physical H.

The older CPT runner proves the exact identities for the real anti-Hermitian
staggered hopping operator D.  The physical complex Hilbert-space Hamiltonian
used by the framework is H = i D.  Because CPT is antiunitary, the factor i
must be carried through explicitly.  A naive reuse of the D-level CP K action
flips H; the physical Hermitian lift composes the antiunitary time reversal
representative with one exact staggered spectral-flip unitary, so that the
Hermitian Hamiltonian is invariant and the CPT-odd SME sector vanishes.
"""

from __future__ import annotations

import numpy as np

TOL = 1.0e-12


def staggered_eta(mu: int, site: tuple[int, int, int]) -> int:
    return (-1) ** sum(site[nu] for nu in range(mu))


def build_D(L: int) -> np.ndarray:
    if L % 2:
        raise ValueError("even L required for bipartite periodic parity")
    n = L**3

    def idx(x: int, y: int, z: int) -> int:
        return ((x % L) * L + (y % L)) * L + (z % L)

    def site(i: int) -> tuple[int, int, int]:
        z = i % L
        y = (i // L) % L
        x = i // (L * L)
        return x, y, z

    D = np.zeros((n, n), dtype=complex)
    for i in range(n):
        x = site(i)
        for mu in range(3):
            eta = staggered_eta(mu, x)
            fwd = list(x)
            bwd = list(x)
            fwd[mu] = (fwd[mu] + 1) % L
            bwd[mu] = (bwd[mu] - 1) % L
            D[i, idx(*fwd)] += 0.5 * eta
            D[i, idx(*bwd)] -= 0.5 * eta
    return D


def build_C(L: int) -> np.ndarray:
    n = L**3

    def site(i: int) -> tuple[int, int, int]:
        z = i % L
        y = (i // L) % L
        x = i // (L * L)
        return x, y, z

    C = np.zeros((n, n), dtype=complex)
    for i in range(n):
        C[i, i] = (-1) ** sum(site(i))
    return C


def build_P(L: int) -> np.ndarray:
    n = L**3

    def idx(x: int, y: int, z: int) -> int:
        return ((x % L) * L + (y % L)) * L + (z % L)

    def site(i: int) -> tuple[int, int, int]:
        z = i % L
        y = (i // L) % L
        x = i // (L * L)
        return x, y, z

    P = np.zeros((n, n), dtype=complex)
    for i in range(n):
        x, y, z = site(i)
        P[i, idx(-x, -y, -z)] = 1.0
    return P


def antiunitary_conjugate(unitary_part: np.ndarray, op: np.ndarray) -> np.ndarray:
    """Apply U K op K U^{-1}; all U used here are involutory real unitaries."""
    return unitary_part @ np.conj(op) @ unitary_part.conj().T


def direction_D(L: int, mu: int) -> np.ndarray:
    n = L**3

    def idx(x: int, y: int, z: int) -> int:
        return ((x % L) * L + (y % L)) * L + (z % L)

    def site(i: int) -> tuple[int, int, int]:
        z = i % L
        y = (i // L) % L
        x = i // (L * L)
        return x, y, z

    D = np.zeros((n, n), dtype=complex)
    for i in range(n):
        x = site(i)
        eta = staggered_eta(mu, x)
        fwd = list(x)
        bwd = list(x)
        fwd[mu] = (fwd[mu] + 1) % L
        bwd[mu] = (bwd[mu] - 1) % L
        D[i, idx(*fwd)] += 0.5 * eta
        D[i, idx(*bwd)] -= 0.5 * eta
    return D


def fro(m: np.ndarray) -> float:
    return float(np.linalg.norm(m, ord="fro"))


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
    return ok


def main() -> int:
    print("=" * 78)
    print("PHYSICAL HERMITIAN HAMILTONIAN AND SME CPT BRIDGE")
    print("=" * 78)
    print()

    results: list[bool] = []
    for L in (4, 6):
        D = build_D(L)
        H = 1j * D
        C = build_C(L)
        P = build_P(L)
        CP = C @ P

        d_antiherm = fro(D.conj().T + D)
        h_herm = fro(H.conj().T - H)
        results.append(
            check(
                f"L={L} D -> H=iD Hermitization",
                d_antiherm < TOL and h_herm < TOL,
                f"||D^dag+D||={d_antiherm:.2e}; ||H^dag-H||={h_herm:.2e}",
            )
        )

        cdc = fro(C @ D @ C + D)
        pdp = fro(P @ D @ P + D)
        cpdcp = fro(CP @ D @ CP.conj().T - D)
        results.append(
            check(
                f"L={L} D-level staggered C/P/CPT identities",
                cdc < TOL and pdp < TOL and cpdcp < TOL,
                f"CDC=-D {cdc:.2e}; PDP=-D {pdp:.2e}; CPDCP=D {cpdcp:.2e}",
            )
        )

        naive = antiunitary_conjugate(CP, H)
        naive_flip = fro(naive + H)
        results.append(
            check(
                f"L={L} naive CP K flips H and exposes the old gap",
                naive_flip < TOL,
                f"||CP K(H) + H||={naive_flip:.2e}",
            )
        )

        # Physical Hermitian lift: choose the antiunitary time-reversal
        # representative T_H = C K.  Then CPT_H = C P T_H = P K on H.
        # Equivalently one could choose T_H = P K, giving CPT_H = C K.
        theta_h_unitary = P
        h_cpt = antiunitary_conjugate(theta_h_unitary, H)
        h_cpt_err = fro(h_cpt - H)
        results.append(
            check(
                f"L={L} physical Hermitian CPT lift preserves H",
                h_cpt_err < TOL,
                f"Theta_H=P K; ||Theta_H H Theta_H^-1-H||={h_cpt_err:.2e}",
            )
        )

        odd_full = 0.5 * (H - h_cpt)
        direction_errs = []
        trace_coeffs = []
        for mu in range(3):
            H_mu = 1j * direction_D(L, mu)
            H_mu_cpt = antiunitary_conjugate(theta_h_unitary, H_mu)
            odd_mu = 0.5 * (H_mu - H_mu_cpt)
            direction_errs.append(fro(odd_mu))
            trace_coeffs.append(abs(np.trace(odd_mu) / (L**3)))
        results.append(
            check(
                f"L={L} SME CPT-odd Hamiltonian sector vanishes",
                fro(odd_full) < TOL and max(direction_errs) < TOL and max(trace_coeffs) < TOL,
                (
                    f"||H_odd||={fro(odd_full):.2e}; "
                    f"max ||H_mu_odd||={max(direction_errs):.2e}; "
                    f"max |a_mu|={max(trace_coeffs):.2e}"
                ),
            )
        )

    print()
    passed = sum(results)
    failed = len(results) - passed
    print(f"Summary: PASS={passed}  FAIL={failed}")
    if failed:
        return 1
    print()
    print(
        "Verdict: PASS. The bridge explicitly carries the antiunitary i -> -i "
        "step in H=iD. The naive D-level CP K action flips H, while the "
        "physical Hermitian CPT representative induced by the staggered "
        "spectral-flip algebra preserves H and has zero CPT-odd SME sector."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
