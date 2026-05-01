#!/usr/bin/env python3
"""
DM neutrino singlet-doublet CP slot tool.

Question:
  After the exact Z_3-covariant circulant family is ruled out in the physical
  heavy-neutrino mass basis, what is the minimal exact Hermitian-kernel carrier
  that can still support the standard leptogenesis CP tensor on the current
  Majorana stack?

Answer:
  In the Z_3 basis, the minimal surviving carrier is a singlet-doublet slot
  family with one residual-Z_2-even amplitude u and one residual-Z_2-odd
  amplitude v:

      K_Z3 =
      [ sigma,            (u+v)e^{-i phi},   (u-v)e^{+i phi} ]
      [ (u+v)e^{+i phi},  tau+rho,           m               ]
      [ (u-v)e^{-i phi},  m^*,               tau-rho         ]

  The current right-handed Majorana matrix is diagonalized from the Z_3 basis
  by a real pi/4 rotation inside the doublet block. Under that rotation,

      (K_mass)_{01} = sqrt(2) (v cos phi - i u sin phi)
      (K_mass)_{02} = sqrt(2) (u cos phi - i v sin phi)

  so

      Im[(K_mass)_{01}^2] = Im[(K_mass)_{02}^2] = -2 u v sin(2 phi).

  The exact source phase phi = 2 pi / 3 therefore gives

      Im[(K_mass)_{0j}^2] = sqrt(3) u v.

  So the physical leptogenesis carrier is no longer a vague "non-circulant
  bridge." It is a Z_3-basis singlet-doublet slot family with one even carrier
  amplitude and one odd activator amplitude.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

PI = np.pi
OMEGA = np.exp(2j * PI / 3.0)

S = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)
S2 = S @ S
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def mass_basis_rotation() -> np.ndarray:
    s = 1.0 / math.sqrt(2.0)
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, s, s],
            [0.0, -s, s],
        ],
        dtype=float,
    )


def exact_circulant_kernel(d: float, r: float, chi: complex) -> np.ndarray:
    return d * np.eye(3, dtype=complex) + r * (chi * S + np.conj(chi) * S2)


def z3_basis_kernel(k: np.ndarray) -> np.ndarray:
    return UZ3.conj().T @ k @ UZ3


def singlet_doublet_kernel(
    sigma: float,
    tau: float,
    rho: float,
    m: complex,
    u: float,
    v: float,
    phi: float,
) -> np.ndarray:
    a = (u + v) * np.exp(-1j * phi)
    b = (u - v) * np.exp(+1j * phi)
    return np.array(
        [
            [sigma, a, b],
            [np.conj(a), tau + rho, m],
            [np.conj(b), np.conj(m), tau - rho],
        ],
        dtype=complex,
    )


def mass_basis_kernel_from_z3(k_z3: np.ndarray) -> np.ndarray:
    rot = mass_basis_rotation()
    return rot.T @ k_z3 @ rot


def expected_mass_entries(u: float, v: float, phi: float) -> tuple[complex, complex]:
    k01 = math.sqrt(2.0) * (v * math.cos(phi) - 1j * u * math.sin(phi))
    k02 = math.sqrt(2.0) * (u * math.cos(phi) - 1j * v * math.sin(phi))
    return k01, k02


def cp_invariant_from_slots(u: float, v: float, phi: float) -> float:
    return -2.0 * u * v * math.sin(2.0 * phi)


def part1_even_and_odd_slot_decomposition() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE SINGLET-DOUBLET CARRIER HAS ONE EVEN SLOT AND ONE ODD SLOT")
    print("=" * 88)

    u = 0.37
    v = 0.14
    a = u + v
    b = u - v

    u_swap = 0.5 * (b + a)
    v_swap = 0.5 * (b - a)

    check(
        "Under doublet-slot exchange, the even amplitude u is invariant",
        abs(u_swap - u) < 1e-12,
        f"u -> {u_swap:.6f}",
    )
    check(
        "Under doublet-slot exchange, the odd amplitude v flips sign",
        abs(v_swap + v) < 1e-12,
        f"v -> {v_swap:.6f}",
    )

    print()
    print("  So the carrier is naturally resolved into one residual-Z_2-even slot")
    print("  amplitude and one residual-Z_2-odd slot amplitude.")


def part2_mass_basis_entries_are_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE PHYSICAL MASS-BASIS ENTRIES DEPEND ONLY ON THE SLOT AMPLITUDES")
    print("=" * 88)

    sigma = 2.2
    tau = 1.3
    rho = 0.17
    m = 0.28 + 0.11j
    u = 0.41
    v = 0.19
    phi = 2.0 * PI / 3.0

    k_z3 = singlet_doublet_kernel(sigma, tau, rho, m, u, v, phi)
    k_mass = mass_basis_kernel_from_z3(k_z3)
    expected_01, expected_02 = expected_mass_entries(u, v, phi)

    check(
        "The real doublet rotation gives the exact singlet-doublet mass-basis entry K01",
        abs(k_mass[0, 1] - expected_01) < 1e-12,
        f"K01={k_mass[0,1]:.6f}, expected={expected_01:.6f}",
    )
    check(
        "The same rotation gives the exact singlet-doublet mass-basis entry K02",
        abs(k_mass[0, 2] - expected_02) < 1e-12,
        f"K02={k_mass[0,2]:.6f}, expected={expected_02:.6f}",
    )

    sigma2 = 5.1
    tau2 = 0.7
    rho2 = -0.08
    m2 = -0.05 + 0.29j
    k_z3_b = singlet_doublet_kernel(sigma2, tau2, rho2, m2, u, v, phi)
    k_mass_b = mass_basis_kernel_from_z3(k_z3_b)
    same = abs(k_mass_b[0, 1] - k_mass[0, 1]) < 1e-12 and abs(k_mass_b[0, 2] - k_mass[0, 2]) < 1e-12
    check(
        "Spectator diagonal and doublet-block data do not change the physical singlet-doublet entries",
        same,
        f"K01={k_mass_b[0,1]:.6f}, K02={k_mass_b[0,2]:.6f}",
    )

    print()
    print("  The physical leptogenesis carrier therefore sits entirely in the")
    print("  singlet-doublet slot amplitudes. The rest of the Hermitian kernel is")
    print("  spectator data for this tensor component.")


def part3_cp_tensor_formula() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE STANDARD CP TENSOR IS EXACTLY PROPORTIONAL TO u v sin(2 phi)")
    print("=" * 88)

    u = 0.41
    v = 0.19
    phi = 1.1
    k_z3 = singlet_doublet_kernel(2.2, 1.3, 0.17, 0.28 + 0.11j, u, v, phi)
    k_mass = mass_basis_kernel_from_z3(k_z3)

    imag_01 = float(np.imag(k_mass[0, 1] ** 2))
    imag_02 = float(np.imag(k_mass[0, 2] ** 2))
    expected = cp_invariant_from_slots(u, v, phi)

    check(
        "Im[(K_mass)_{01}^2] equals the exact slot formula",
        abs(imag_01 - expected) < 1e-12,
        f"direct={imag_01:.6f}, expected={expected:.6f}",
    )
    check(
        "Im[(K_mass)_{02}^2] equals the same exact slot formula",
        abs(imag_02 - expected) < 1e-12,
        f"direct={imag_02:.6f}, expected={expected:.6f}",
    )
    check(
        "If either slot amplitude vanishes, the physical CP tensor vanishes",
        abs(cp_invariant_from_slots(u, 0.0, phi)) < 1e-12
        and abs(cp_invariant_from_slots(0.0, v, phi)) < 1e-12,
        "both the even and odd slot amplitudes are required",
    )

    phi_src = 2.0 * PI / 3.0
    expected_src = cp_invariant_from_slots(u, v, phi_src)
    check(
        "At the exact Z_3 source phase phi = 2 pi / 3 the tensor becomes sqrt(3) u v",
        abs(expected_src - math.sqrt(3.0) * u * v) < 1e-12,
        f"direct={expected_src:.6f}, sqrt(3)uv={math.sqrt(3.0)*u*v:.6f}",
    )

    print()
    print("  So the physical tensor is not controlled by one odd coefficient alone.")
    print("  It is the product of an even carrier slot and an odd activator slot.")


def part4_beyond_the_exact_circulant_class() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THIS CARRIER IS GENUINELY BEYOND THE EXACT CIRCULANT NO-GO CLASS")
    print("=" * 88)

    ok = True
    details = []
    for label, chi in [("1", 1.0 + 0.0j), ("omega", OMEGA), ("omega^2", np.conj(OMEGA))]:
        k = exact_circulant_kernel(1.2, 0.35, chi)
        k_z3 = z3_basis_kernel(k)
        offdiag = max(abs(k_z3[0, 1]), abs(k_z3[0, 2]))
        ok &= offdiag < 1e-12
        details.append(f"{label}: max singlet-doublet slot = {offdiag:.2e}")

    check(
        "Every exact Z_3-covariant circulant kernel has zero singlet-doublet slots in the Z_3 basis",
        ok,
        "; ".join(details),
    )

    u = 0.41
    v = 0.19
    phi = 2.0 * PI / 3.0
    k_z3 = singlet_doublet_kernel(2.2, 1.3, 0.17, 0.28 + 0.11j, u, v, phi)
    nonzero = max(abs(k_z3[0, 1]), abs(k_z3[0, 2])) > 1e-6
    check(
        "The singlet-doublet carrier turns on precisely those previously-empty slots",
        nonzero,
        f"|K01|={abs(k_z3[0,1]):.6f}, |K02|={abs(k_z3[0,2]):.6f}",
    )

    print()
    print("  This is why the old circulant route is exhausted while the new slot")
    print("  family still survives the physical mass-basis test.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SINGLET-DOUBLET CP SLOT TOOL")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the exact Z_3-covariant circulant class dies in the physical")
    print("  mass basis, what exact Hermitian-kernel carrier is left for leptogenesis?")

    part1_even_and_odd_slot_decomposition()
    part2_mass_basis_entries_are_exact()
    part3_cp_tensor_formula()
    part4_beyond_the_exact_circulant_class()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - the minimal physical carrier is a Z_3-basis singlet-doublet slot family")
    print("    - it carries one residual-Z_2-even amplitude u and one residual-Z_2-odd amplitude v")
    print("    - after the real Majorana doublet rotation, the standard CP tensor is")
    print("      exactly Im[(K_mass)_{0j}^2] = -2 u v sin(2 phi)")
    print("    - at the exact source phase phi = 2 pi / 3 this becomes sqrt(3) u v")
    print("    - the exact circulant class has zero singlet-doublet slots, so this")
    print("      carrier is genuinely beyond the old no-go route")
    print()
    print("  The live DM denominator target is therefore no longer a vague")
    print('  "non-circulant bridge." It is a singlet-doublet slot bridge with')
    print("  one even carrier amplitude and one odd activator amplitude.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
