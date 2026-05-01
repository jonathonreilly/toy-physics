#!/usr/bin/env python3
"""
Minimal Z3-covariant CP-supporting Dirac texture family for DM leptogenesis.

Question:
  Given the exact weak-axis 1+2 split on the neutrino triplet, what is the
  minimal Z3-covariant Dirac texture family that can possibly support a
  nonzero leptogenesis CP kernel?

Answer:
  The current exact 1+2 site-basis split diag(a,b,b) lifts through the
  canonical Z3 bridge to the even circulant slice

      Y_even = mu I + nu (S + S^2),

  with no Z3-odd component. Its Hermitian kernel stays in the same even slice,
  with real off-diagonal entries, so the standard CP tensor vanishes.

  The minimal Z3-covariant extension that can support a nonzero CP kernel is

      Y_CP = mu I + nu (S + S^2) + i eta (S - S^2),

  where S is the cyclic shift. This introduces the unique Z3-odd circulant
  generator. For generic eta != 0, the Hermitian kernel acquires complex
  off-diagonal entries and the standard CP tensor becomes nonzero.

Boundary:
  This does not derive eta from the axiom surface. It builds the exact minimal
  tool and identifies the remaining theorem target: derive the Z3-odd
  circulant generator (or an equivalent object) from the framework.
"""

from __future__ import annotations

import math
import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


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


def z3_bridge() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3.0)
    return (1.0 / np.sqrt(3.0)) * np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega * omega],
            [1.0, omega * omega, omega],
        ],
        dtype=complex,
    )


def shift_matrix() -> np.ndarray:
    return np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
        ],
        dtype=complex,
    )


def cp_tensor(h: np.ndarray) -> tuple[complex, complex]:
    return (np.imag(h[0, 1] ** 2), np.imag(h[0, 2] ** 2))


def even_slice_from_split(a: complex, b: complex, uz3: np.ndarray) -> np.ndarray:
    d = np.diag([a, b, b]).astype(complex)
    return uz3.conj().T @ d @ uz3


def minimal_cp_family(mu: float, nu: float, eta: float, s: np.ndarray) -> np.ndarray:
    i3 = np.eye(3, dtype=complex)
    return mu * i3 + nu * (s + s @ s) + 1j * eta * (s - s @ s)


def main() -> int:
    print("=" * 88)
    print("DM / FLAVOR: MINIMAL Z3 CIRCULANT CP TOOL")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md")
    print("  - docs/DM_NEUTRINO_CP_KERNEL_DEFORMATION_NECESSITY_NOTE_2026-04-15.md")
    print("  - docs/DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md")
    print()
    print("Question:")
    print("  What is the minimal exact Z3-covariant Dirac texture family that can")
    print("  evade the current CP-kernel no-go?")

    uz3 = z3_bridge()
    s = shift_matrix()
    s2 = s @ s
    i3 = np.eye(3, dtype=complex)

    a = 1.4 + 0.3j
    b = 0.8 - 0.2j
    y_even = even_slice_from_split(a, b, uz3)
    mu_even = (a + 2.0 * b) / 3.0
    nu_even = (a - b) / 3.0
    y_even_expected = mu_even * i3 + nu_even * (s + s2)
    h_even = y_even.conj().T @ y_even

    mu = 1.0
    nu = 0.25
    eta = 0.17
    y_cp = minimal_cp_family(mu, nu, eta, s)
    h_cp = y_cp.conj().T @ y_cp
    cp12, cp13 = cp_tensor(h_cp)

    y_cp_diag = uz3 @ y_cp @ uz3.conj().T
    expected_diag = np.diag([mu + 2.0 * nu, mu - nu + math.sqrt(3.0) * eta, mu - nu - math.sqrt(3.0) * eta])

    x0 = (mu + 2.0 * nu) ** 2
    xp = (mu - nu + math.sqrt(3.0) * eta) ** 2
    xm = (mu - nu - math.sqrt(3.0) * eta) ** 2
    h01_formula = (x0 + xp * np.exp(2j * np.pi / 3.0) + xm * np.exp(-2j * np.pi / 3.0)) / 3.0
    h01_closed = (2.0 * mu * nu + nu * nu - eta * eta) + 2j * eta * (mu - nu)

    print()
    print("Even 1+2 slice from the exact weak-axis split:")
    print(y_even)
    print()
    print("Minimal CP-supporting family sample:")
    print(y_cp)
    print()
    print("Hermitian kernel H_CP = Y_CP^dag Y_CP:")
    print(h_cp)

    check(
        "The exact 1+2 split lifts to the even circulant slice mu I + nu(S+S^2)",
        np.allclose(y_even, y_even_expected, atol=1e-12),
        f"mu={mu_even:.6f}, nu={nu_even:.6f}",
    )
    check(
        "The even circulant slice keeps the CP tensor zero",
        abs(np.imag(h_even[0, 1] ** 2)) < 1e-12 and abs(np.imag(h_even[0, 2] ** 2)) < 1e-12,
        f"H_even offdiag = {h_even[0,1]:.6f}",
    )
    check(
        "The minimal CP-supporting family is still exactly Z3-covariant",
        np.linalg.norm(y_cp @ s - s @ y_cp) < 1e-12,
        f"commutator norm = {np.linalg.norm(y_cp @ s - s @ y_cp):.2e}",
    )
    check(
        "The Z3 bridge diagonalizes the minimal family with split doublet eigenvalues",
        np.allclose(y_cp_diag, expected_diag, atol=1e-12),
        f"diag = {np.diag(y_cp_diag)}",
    )
    check(
        "The Z3-odd generator makes the Hermitian kernel genuinely complex off-diagonal",
        abs(np.imag(h_cp[0, 1])) > 1e-6 and abs(np.imag(h_cp[0, 2])) > 1e-6,
        f"H01 = {h_cp[0,1]:.6f}",
    )
    check(
        "The standard CP tensor is nonzero on the minimal CP-supporting family",
        abs(cp12) > 1e-6 and abs(cp13) > 1e-6,
        f"Im[(H01)^2]={cp12:.6e}, Im[(H02)^2]={cp13:.6e}",
    )
    check(
        "The off-diagonal kernel entry matches the exact closed form",
        abs(h_cp[0, 1] - h01_formula) < 1e-12 and abs(h_cp[0, 1] - h01_closed) < 1e-12,
        f"H01 = {h_cp[0,1]:.6f}",
    )

    print()
    print("Result:")
    print("  The current exact weak-axis geometry already identifies the even")
    print("  circulant slice singled out by the 1+2 split, but that slice stays")
    print("  CP-degenerate. The minimal exact Z3-covariant extension that can")
    print("  support a nonzero leptogenesis kernel is the unique odd circulant")
    print("  generator i(S-S^2).")
    print()
    print("  So the remaining theorem target is now sharper: derive the Z3-odd")
    print("  circulant generator, or an equivalent object, from the axiom surface.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
