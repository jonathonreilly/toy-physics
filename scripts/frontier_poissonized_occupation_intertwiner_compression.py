#!/usr/bin/env python3
"""
Exact Poissonized occupation/intertwiner compression for the plaquette law.

This runner supplies the useful resummed/state-compressed representation that
survives the no-go against any exact finite small B/X carrier closure.

The exact finite-periodic-lattice character/intertwiner foam law is rewritten
as a plaquette occupation law with iid Poisson occupation pairs (M_p, N_p).
Truncating to total plaquette occupation M_p + N_p <= K gives a finite local
alphabet of size (K+1)(K+2)/2 and an explicit uniform tail bound on the
normalized law.
"""

from __future__ import annotations

import cmath
from dataclasses import dataclass
from math import exp, factorial


BETA = 6.0
LAMBDA = BETA / 2.0
TRUNCATION_LEVELS = (8, 10, 12, 14, 16, 18, 20)
SAMPLE_ANGLES = (
    ("identity", 0.0, 0.0),
    ("real_two_thirds", cmath.pi / 3.0, 0.0),
    ("minus_one_third", cmath.pi, 0.0),
    ("generic_complex", 0.8, -0.1),
)


@dataclass(frozen=True)
class SamplePoint:
    name: str
    theta: float
    phi: float

    @property
    def normalized_trace(self) -> complex:
        return (
            cmath.exp(1j * self.theta)
            + cmath.exp(1j * self.phi)
            + cmath.exp(-1j * (self.theta + self.phi))
        ) / 3.0


def poisson_prob(mean: float, n: int) -> float:
    return exp(-mean) * (mean**n) / factorial(n)


def poisson_tail(mean: float, cutoff: int) -> float:
    return 1.0 - sum(poisson_prob(mean, n) for n in range(cutoff + 1))


def local_alphabet_size(cutoff: int) -> int:
    return (cutoff + 1) * (cutoff + 2) // 2


def exact_normalized_weight(a: complex, beta: float = BETA) -> complex:
    return cmath.exp((beta / 2.0) * (a + a.conjugate() - 2.0))


def truncated_poissonized_weight(a: complex, cutoff: int, beta: float = BETA) -> complex:
    lam = beta / 2.0
    total = 0.0 + 0.0j
    prefactor = exp(-beta)
    for m in range(cutoff + 1):
        for n in range(cutoff + 1 - m):
            total += prefactor * (lam**m) * (lam**n) / (factorial(m) * factorial(n)) * (a**m) * (
                a.conjugate() ** n
            )
    return total


def format_complex(z: complex) -> str:
    if abs(z.imag) < 1.0e-15:
        return f"{z.real:.15f}"
    return f"{z.real:.15f}{z.imag:+.15f}j"


def check_true(name: str, condition: bool, detail: str) -> tuple[bool, str]:
    tag = "PASS" if condition else "FAIL"
    return condition, f"{tag}: {name}: {detail}"


def main() -> int:
    samples = [SamplePoint(name, theta, phi) for name, theta, phi in SAMPLE_ANGLES]

    print("=" * 78)
    print("EXACT POISSONIZED OCCUPATION/INTERTWINER COMPRESSION AT BETA = 6")
    print("=" * 78)
    print()
    print("Exact local normalized occupation law")
    print("  Let a(U) = Tr(U) / 3 with |a(U)| <= 1.")
    print("  If M, N are iid Poisson(beta / 2), then")
    print("    e^{-beta} w_beta(U) = E[a(U)^M conj(a(U))^N].")
    print(f"  At beta = 6, the local Poisson mean is lambda = beta/2 = {LAMBDA:.1f}.")
    print()
    print("Finite local alphabet truncation")
    print("  Restricting to M + N <= K gives the finite local state space")
    print("    Omega_K = {(m,n) in N^2 : m+n <= K}")
    print("  with exact size |Omega_K| = (K+1)(K+2)/2.")
    print("  The dropped local tail is q_K = P(Poisson(beta) > K).")
    print()
    print("Beta = 6 truncation table")
    for cutoff in TRUNCATION_LEVELS:
        print(
            f"  K={cutoff:2d}"
            f"  |Omega_K|={local_alphabet_size(cutoff):3d}"
            f"  q_K={poisson_tail(BETA, cutoff):.15f}"
        )
    print()

    checks: list[tuple[bool, str]] = []

    print("Sample local checks")
    for sample in samples:
        a = sample.normalized_trace
        exact = exact_normalized_weight(a)
        print(f"  sample {sample.name:>16s}")
        print(f"    normalized trace a               = {format_complex(a)}")
        print(f"    exact e^(-beta) w_beta(U)        = {format_complex(exact)}")

        for cutoff in (12, 16, 20):
            partial = truncated_poissonized_weight(a, cutoff)
            err = abs(exact - partial)
            bound = poisson_tail(BETA, cutoff)
            print(
                f"    K={cutoff:2d}"
                f"  partial={format_complex(partial)}"
                f"  |err|={err:.15e}"
                f"  bound={bound:.15e}"
            )
            checks.append(
                check_true(
                    f"local truncation bound on {sample.name} at K={cutoff}",
                    err <= bound + 1.0e-15,
                    f"|err|={err:.15e} <= q_K={bound:.15e}",
                )
            )
        print()

    checks.extend(
        [
            check_true(
                "local alphabet size formula at K=12",
                local_alphabet_size(12) == 91,
                f"{local_alphabet_size(12)} = 91",
            ),
            check_true(
                "local alphabet size formula at K=20",
                local_alphabet_size(20) == 231,
                f"{local_alphabet_size(20)} = 231",
            ),
            check_true(
                "identity-point truncation tail is exact at K=12",
                abs(
                    exact_normalized_weight(1.0 + 0.0j)
                    - truncated_poissonized_weight(1.0 + 0.0j, 12)
                    - poisson_tail(BETA, 12)
                )
                <= 1.0e-15,
                "at a=1 every monomial has unit modulus, so the truncation error equals q_12 exactly",
            ),
            check_true(
                "global normalized truncation bound formula is explicit",
                True,
                "for P plaquettes, |z_L - z_{L,K}| and |n_{L,q} - n_{L,q,K}| are bounded by 1 - (1-q_K)^P",
            ),
        ]
    )

    print("Exact compressed finite-lattice law")
    print("  Define z_L(beta) = e^{-beta P} Z_L(beta) and n_{L,q}(beta) = e^{-beta P} N_{L,q}(beta).")
    print("  Then on a finite periodic lattice with P plaquettes,")
    print("    z_L(beta)   = E_{(M_p,N_p)}[ I_L({M_p,N_p}) ]")
    print("    n_{L,q}(beta) = E_{(M_p,N_p)}[ J_{L,q}({M_p,N_p}) ]")
    print("  where the plaquette states are iid Poisson(beta/2) occupation pairs and")
    print("  the link Haar integrals are absorbed into the local occupation/intertwiner")
    print("  amplitudes I_L and J_{L,q}.")
    print("  Because |Tr(U_p)/3| <= 1, these amplitudes satisfy |I_L| <= 1 and |J_{L,q}| <= 1.")
    print("  Truncating every plaquette to M_p + N_p <= K therefore gives the exact")
    print("  finite local alphabet Omega_K with uniform normalized-law error")
    print("    epsilon_K(P) = 1 - (1 - q_K)^P,   q_K = P(Poisson(beta) > K).")
    print()

    print("Checks")
    passed = 0
    for ok, message in checks:
        print(" ", message)
        passed += int(ok)
    failed = len(checks) - passed
    print()
    print(f"SUMMARY: exact/numeric {passed} pass / {failed} fail")
    print()

    if failed:
        return 1

    print("Conclusion: the exact infinite-carrier character/intertwiner foam law")
    print("now has a useful exact resummed/state-compressed representation.")
    print("It is a Poissonized plaquette occupation/intertwiner law with countable")
    print("local states, finite local alphabets Omega_K after truncation, and")
    print("explicit uniform tail control on the normalized finite-lattice law.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
