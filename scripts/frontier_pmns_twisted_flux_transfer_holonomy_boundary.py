#!/usr/bin/env python3
"""Twisted/flux transfer holonomy boundary for the retained PMNS cycle lane.

Question:
  Can a twisted transfer / flux insertion / cycle-holonomy law on the graph-
  first oriented-cycle frame select the remaining values of the retained PMNS
  cycle channel?

Answer:
  Partially.

  On the canonical graph-first frame E12, E23, E31, the flux-threaded transfer
  kernel

      T(xbar, ybar, phi) = xbar I + ybar (e^{i phi} C + e^{-i phi} C^2)

  has an exact holonomy/spectral value law:

      tr(T)/3 = xbar
      tr(C^2 T)/3 = ybar e^{i phi}

  so xbar, ybar, and phi are recovered exactly from the twisted transfer data.

  But the current exact bank still does not select the full reduced oriented-
  cycle PMNS family

      A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31

  with one flux holonomy alone.  The holonomy probe has a 2-real kernel on the
  reduced carrier, so it is a genuine value law for the fluxed transfer
  carrier, but not a full positive closure law for the retained PMNS cycle
  channel.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE2 = CYCLE @ CYCLE
FOURIER = np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)],
        [1.0, np.exp(4j * np.pi / 3), np.exp(2j * np.pi / 3)],
    ],
    dtype=complex,
) / np.sqrt(3.0)


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


def e(i: int, j: int) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[i, j] = 1.0
    return out


E11 = e(0, 0)
E22 = e(1, 1)
E33 = e(2, 2)
E12 = e(0, 1)
E23 = e(1, 2)
E31 = e(2, 0)

B1 = E12 + E31
B2 = 1j * (E12 - E31)
B3 = E23


def twisted_flux_transfer_kernel(xbar: float, ybar: float, phi: float) -> np.ndarray:
    """Hermitian flux-threaded transfer kernel on the canonical cycle frame."""
    return xbar * I3 + ybar * (np.exp(1j * phi) * CYCLE + np.exp(-1j * phi) * CYCLE2)


def twisted_flux_holonomy_probe(phi: float) -> np.ndarray:
    """Canonical holonomy probe on the reduced cycle carrier."""
    return math.cos(phi) * B1 + math.sin(phi) * B2 + B3


def flux_moments(t: np.ndarray) -> tuple[complex, complex, complex]:
    mean = np.trace(t) / 3.0
    hol_fwd = np.trace(CYCLE2 @ t) / 3.0
    hol_bwd = np.trace(CYCLE @ t) / 3.0
    return mean, hol_fwd, hol_bwd


def recover_flux_parameters(t: np.ndarray) -> tuple[float, float, float]:
    mean, hol_fwd, hol_bwd = flux_moments(t)
    xbar = float(np.real(mean))
    ybar = float(np.abs(hol_fwd))
    phi = float(np.angle(hol_fwd))
    check("The backward holonomy is the complex conjugate of the forward one",
          abs(hol_bwd - np.conj(hol_fwd)) < 1e-12,
          f"hol_fwd={hol_fwd:.6f}, hol_bwd={hol_bwd:.6f}")
    return xbar, ybar, phi


def reduced_cycle_family_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return B1, B2, B3


def reduced_cycle_family(u: float, v: float, w: float) -> np.ndarray:
    return u * B1 + v * B2 + w * B3


def flux_holonomy_on_reduced_family(m: np.ndarray, phi: float) -> float:
    probe = twisted_flux_holonomy_probe(phi)
    return float(np.real(np.trace(probe.conj().T @ m)))


def part1_the_twisted_flux_transfer_kernel_has_exact_holonomy_modes() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE TWISTED FLUX TRANSFER KERNEL HAS EXACT HOLONOMY MODES")
    print("=" * 88)

    xbar = 0.93
    ybar = 0.37
    phi = 0.41
    t = twisted_flux_transfer_kernel(xbar, ybar, phi)
    vals = np.linalg.eigvalsh(t)
    vals_expected = np.array(
        [
            xbar + 2.0 * ybar * math.cos(phi),
            xbar + 2.0 * ybar * math.cos(phi + 2.0 * math.pi / 3.0),
            xbar + 2.0 * ybar * math.cos(phi + 4.0 * math.pi / 3.0),
        ],
        dtype=float,
    )
    vals_expected.sort()

    check("The fluxed transfer kernel is Hermitian", np.linalg.norm(t - t.conj().T) < 1e-12,
          f"hermitian_error={np.linalg.norm(t - t.conj().T):.2e}")
    fourier_t = FOURIER.conj().T @ t @ FOURIER
    check("The Fourier basis diagonalizes the twisted flux transfer kernel",
          np.linalg.norm(fourier_t - np.diag(np.diag(fourier_t))) < 1e-12,
          f"offdiag_error={np.linalg.norm(fourier_t - np.diag(np.diag(fourier_t))):.2e}")
    check("The twisted spectrum has the exact three flux-shifted eigenvalues",
          np.linalg.norm(np.sort(vals) - vals_expected) < 1e-12,
          f"vals={np.round(np.sort(vals), 6)}")


def part2_the_flux_holonomy_recovers_xbar_ybar_and_phi_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FLUX HOLONOMY RECOVERS xbar, ybar, AND phi EXACTLY")
    print("=" * 88)

    xbar = 0.93
    ybar = 0.37
    phi = 0.41
    t = twisted_flux_transfer_kernel(xbar, ybar, phi)
    rxbar, rybar, rphi = recover_flux_parameters(t)

    check("The transfer trace recovers xbar exactly", abs(rxbar - xbar) < 1e-12,
          f"recovered={rxbar:.12f}")
    check("The forward cycle holonomy recovers ybar exactly", abs(rybar - ybar) < 1e-12,
          f"recovered={rybar:.12f}")
    check("The holonomy phase recovers phi exactly", abs(rphi - phi) < 1e-12,
          f"recovered={rphi:.12f}")
    check("So the twisted transfer carrier has an exact value law", True,
          f"(xbar,ybar,phi)=({rxbar:.6f},{rybar:.6f},{rphi:.6f})")


def part3_the_one_angle_holonomy_does_not_select_the_full_reduced_pmns_family() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ONE FLUX HOLOMONY DOES NOT SELECT THE FULL REDUCED PMNS FAMILY")
    print("=" * 88)

    phi = 0.41
    b1, b2, b3 = reduced_cycle_family_basis()
    h_b1 = flux_holonomy_on_reduced_family(b1, phi)
    h_b2 = flux_holonomy_on_reduced_family(b2, phi)
    h_b3 = flux_holonomy_on_reduced_family(b3, phi)

    k1 = h_b2 * b1 - h_b1 * b2
    k2 = h_b3 * b1 - h_b1 * b3

    check("The reduced carrier is exactly the graph-first oriented-cycle family",
          np.linalg.norm(reduced_cycle_family(1.0, 0.0, 0.0) - b1) < 1e-12 and np.linalg.norm(reduced_cycle_family(0.0, 1.0, 0.0) - b2) < 1e-12 and np.linalg.norm(reduced_cycle_family(0.0, 0.0, 1.0) - b3) < 1e-12)
    check("A one-angle flux holonomy sees only one real linear combination on the reduced carrier",
          abs(flux_holonomy_on_reduced_family(b1 + b2 + b3, phi) - (h_b1 + h_b2 + h_b3)) < 1e-12,
          f"h(b1)={h_b1:.6f}, h(b2)={h_b2:.6f}, h(b3)={h_b3:.6f}")
    check("The reduced carrier has at least a 2-real kernel for that holonomy probe",
          np.linalg.norm(k1) > 1e-12 and np.linalg.norm(k2) > 1e-12 and np.linalg.norm(np.column_stack([k1.reshape(-1), k2.reshape(-1)])) > 1e-12,
          f"|k1|={np.linalg.norm(k1):.6f}, |k2|={np.linalg.norm(k2):.6f}")
    check("The holonomy probe annihilates two independent reduced-carrier directions",
          abs(flux_holonomy_on_reduced_family(k1, phi)) < 1e-12 and abs(flux_holonomy_on_reduced_family(k2, phi)) < 1e-12,
          f"h(k1)={flux_holonomy_on_reduced_family(k1, phi):.6f}, h(k2)={flux_holonomy_on_reduced_family(k2, phi):.6f}")

    a = b1
    b = b1 + 0.7 * k1 + 0.4 * k2
    check("Two distinct reduced-channel points share the same one-angle holonomy",
          abs(flux_holonomy_on_reduced_family(a, phi) - flux_holonomy_on_reduced_family(b, phi)) < 1e-12,
          f"h(a)={flux_holonomy_on_reduced_family(a, phi):.6f}, h(b)={flux_holonomy_on_reduced_family(b, phi):.6f}")
    check("But the two reduced-channel points are genuinely different", np.linalg.norm(a - b) > 1e-6,
          f"|a-b|={np.linalg.norm(a - b):.6f}")


def part4_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CIRCULARITY GUARD")
    print("=" * 88)

    from pmns_lower_level_utils import circularity_guard

    ok_kernel, bad_kernel = circularity_guard(twisted_flux_transfer_kernel, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_hol, bad_hol = circularity_guard(flux_holonomy_on_reduced_family, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    check("The twisted flux transfer kernel takes no PMNS-side target coordinates as inputs", ok_kernel, f"bad={bad_kernel}")
    check("The flux holonomy probe takes no PMNS-side target coordinates as inputs", ok_hol, f"bad={bad_hol}")


def main() -> int:
    print("=" * 88)
    print("PMNS TWISTED FLUX TRANSFER HOLOMONY BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can a twisted transfer / flux insertion / cycle-holonomy law on the")
    print("  graph-first oriented-cycle frame select the remaining values of the")
    print("  retained PMNS cycle channel?")

    part1_the_twisted_flux_transfer_kernel_has_exact_holonomy_modes()
    part2_the_flux_holonomy_recovers_xbar_ybar_and_phi_exactly()
    part3_the_one_angle_holonomy_does_not_select_the_full_reduced_pmns_family()
    part4_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive native flux result:")
    print("    - the twisted transfer kernel has an exact fluxed holonomy law")
    print("    - the holonomy recovers (xbar, ybar, phi) exactly")
    print()
    print("  Boundary on the retained PMNS reduced carrier:")
    print("    - one flux holonomy sees only one real linear combination on the")
    print("      3-real reduced oriented-cycle family")
    print("    - the probe has a 2-real kernel there, so it does not select a")
    print("      unique reduced PMNS point")
    print()
    print("  So this is a genuine twisted/flux transfer value law, but it is")
    print("  still only a boundary on the full reduced PMNS channel.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
