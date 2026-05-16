#!/usr/bin/env python3
"""
Transfer-operator dominant-mode route for the active PMNS microscopic block.

Question:
  Can a genuinely dynamical native law on the hw=1 triplet recover any of the
  active microscopic PMNS data from corner-to-corner transport?

What this runner now does:
  The dynamical primitive is the native corner-to-corner transport operator on
  the active hw=1 triplet, taken from PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE
  in exactly its supplied form:

      T_act(x, y, delta) = diag(x_1, x_2, x_3) + diag(y_1, y_2, y_3 e^{i delta}) C

  where (x_1, x_2, x_3, y_1, y_2, y_3, delta) are the seven real microscopic
  active-block parameters and C is the canonical C3 cycle permutation. NOTHING
  in this runner takes (xbar, ybar) as an input.

  From that primitive T_act, the runner constructs the native dynamical
  transfer kernel by Hermitization plus C3 orbit-averaging:

      T_kernel(T_act) := (1/3) * sum_{k=0,1,2} C^k (T_act + T_act^dagger) C^{-k}

  This object is a function of the supplied operator. On the aligned
  weak-axis patch (x_i = xbar, y_i = ybar, delta = 0) it reduces to the
  symmetric circulant T_kernel = 2 xbar I + ybar (C + C^2), with the
  coefficients now arising as outputs of the orbit-symmetrization applied to
  T_act, not as pre-supplied inputs.

  The spectral content of T_kernel is then measured. The dominant
  symmetric mode and the doubly-degenerate orthogonal mode are eigenvalues
  of the dynamically constructed object T_kernel(T_act), and on the aligned
  patch they reconstruct the seed pair (xbar, ybar) of the originating
  T_act as a genuine spectral measurement of that operator.

  This is the cleanest bounded native dynamical law the route gives: it
  measures the aligned active seed pair from primitive corner-transport
  amplitudes via the spectrum of an orbit-symmetrized transfer kernel built
  from those amplitudes, and it has a known kernel on the 5-real off-seed
  corner-breaking source.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE2 = CYCLE @ CYCLE


def check(name: str, condition: bool, detail: str = "", cls: str = "A") -> bool:
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


# ---------------------------------------------------------------------------
# Native dynamical primitive: the active corner-to-corner transport operator.
# Matches PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE exactly.
# Inputs are the seven real microscopic active-block parameters
# (x_1, x_2, x_3, y_1, y_2, y_3, delta) ONLY. There is no (xbar, ybar) input.
# ---------------------------------------------------------------------------
def active_corner_transport(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    """The primitive native corner-to-corner transport operator on hw=1.

    Identical to the active-corner transport in
    PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE. Inputs are the microscopic
    parameters (x_1, x_2, x_3, y_1, y_2, y_3, delta). The seed pair
    (xbar, ybar) is NOT supplied.
    """
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(y_eff) @ CYCLE


def c3_orbit_average(M: np.ndarray) -> np.ndarray:
    """(1/3) sum_{k=0,1,2} C^k M C^{-k}: the canonical C3 orbit-average."""
    return (M + CYCLE @ M @ CYCLE2 + CYCLE2 @ M @ CYCLE) / 3.0


def transfer_kernel_from_primitive(T_act: np.ndarray) -> np.ndarray:
    """The native dynamical transfer kernel built from the primitive T_act.

    Construction: Hermitize the supplied primitive corner-transport operator,
    then C3-orbit-average. Both steps are canonical: Hermitization gives the
    symmetric transfer shadow, orbit-averaging removes any non-C3-invariant
    component. No microscopic seed pair is supplied here.
    """
    return c3_orbit_average(T_act + T_act.conj().T)


def eig_sorted(m: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    vals, vecs = np.linalg.eigh(m)
    idx = np.argsort(vals)[::-1]
    return vals[idx], vecs[:, idx]


def spectral_seed_pair_from_kernel(t: np.ndarray) -> tuple[float, float]:
    """Read the seed pair (xbar, ybar) off the spectrum of T_kernel.

    On the aligned patch T_kernel = 2 xbar I + ybar (C + C^2) has
    eigenvalues (2 xbar + 2 ybar, 2 xbar - ybar, 2 xbar - ybar). Inverting
    those formulae gives:

        xbar = (lam_+ + 2 lam_-) / 6
        ybar = (lam_+ -   lam_-) / 3

    The right-hand sides are measurements of the spectrum of the
    dynamically-constructed object T_kernel; nothing here pre-supplies
    (xbar, ybar).
    """
    vals, _ = eig_sorted(t)
    lam_plus = float(vals[0])
    lam_minus = float(vals[1])
    xbar = (lam_plus + 2.0 * lam_minus) / 6.0
    ybar = (lam_plus - lam_minus) / 3.0
    return xbar, ybar


# ---------------------------------------------------------------------------
# Backwards-compatibility helpers for legacy single-factor kernel form.
#
# Downstream sibling runners (`frontier_pmns_hw1_source_transfer_boundary.py`)
# build a single-factor kernel `xbar I + ybar (C + C^2)` and invert the
# eigenvalues with the corresponding single-factor convention. These shims
# preserve that interface unchanged; the dynamical-primitive construction is
# the new, native one above (Hermitization + C3 orbit-average of T_act, which
# gives the doubled form `2 xbar I + ybar (C + C^2)`).
# ---------------------------------------------------------------------------
def active_seed_transfer_kernel(xbar: float, ybar: float) -> np.ndarray:
    """Single-factor aligned seed kernel `xbar I + ybar (C + C^2)`.

    Retained as a downstream API used by the source-transfer boundary runner;
    not the dynamical primitive of this note.
    """
    return xbar * I3 + ybar * (CYCLE + CYCLE2)


def reconstruct_seed_pair_from_transfer_kernel(t: np.ndarray) -> tuple[float, float]:
    """Spectral inversion for the single-factor kernel `xbar I + ybar (C + C^2)`.

    Eigenvalues are (xbar + 2 ybar, xbar - ybar, xbar - ybar), so

        xbar = (lam_+ + 2 lam_-) / 3
        ybar = (lam_+ -   lam_-) / 3.

    Retained as a downstream API used by the source-transfer boundary runner.
    """
    vals, _ = eig_sorted(t)
    lam_plus = float(vals[0])
    lam_minus = float(vals[1])
    xbar = (lam_plus + 2.0 * lam_minus) / 3.0
    ybar = (lam_plus - lam_minus) / 3.0
    return xbar, ybar


def projected_transfer_kernel_from_active_block(a: np.ndarray) -> np.ndarray:
    """Legacy single-factor kernel projection from a generic active block.

    Retained as a downstream API used by the source-transfer boundary runner;
    not the dynamical primitive of this note.
    """
    xbar = float(np.real(np.trace(a)) / 3.0)
    ybar = float(np.real((a[0, 1] + a[1, 2] + a[2, 0])) / 3.0)
    return active_seed_transfer_kernel(2.0 * xbar, ybar)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def part1_kernel_is_built_from_the_primitive_corner_transport_operator() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE NATIVE TRANSFER KERNEL IS BUILT FROM THE PRIMITIVE T_act")
    print("=" * 88)

    # Aligned active patch: x_i = 0.90, y_i = 0.40, delta = 0.
    # The runner does NOT supply (xbar, ybar); those would be outputs.
    x = np.array([0.90, 0.90, 0.90], dtype=float)
    y = np.array([0.40, 0.40, 0.40], dtype=float)
    delta = 0.0

    T_act = active_corner_transport(x, y, delta)
    T_kernel = transfer_kernel_from_primitive(T_act)

    # Identify what shape the kernel must have. The Hermitization of a circulant
    # diag(x) + diag(y_eff) C in general lives in span{I, C, C^2, diag(...)}.
    # The C3 orbit-average removes any non-C3-invariant component, leaving only
    # the C3-equivariant part: an element of span{I, C+C^2}.
    check("T_kernel is Hermitian by construction",
          np.linalg.norm(T_kernel - T_kernel.conj().T) < 1e-12,
          f"Hermitian error={np.linalg.norm(T_kernel - T_kernel.conj().T):.2e}")
    check("T_kernel is C3-equivariant by construction",
          np.linalg.norm(CYCLE @ T_kernel @ CYCLE2 - T_kernel) < 1e-12,
          f"C3 equivariance error={np.linalg.norm(CYCLE @ T_kernel @ CYCLE2 - T_kernel):.2e}")
    check("T_kernel lies in span{I, C + C^2} (C3 even sector)",
          np.linalg.norm(T_kernel - (np.trace(T_kernel) / 3.0) * I3
                         - (T_kernel[0, 1].real) * (CYCLE + CYCLE2)) < 1e-12,
          f"span error={np.linalg.norm(T_kernel - (np.trace(T_kernel)/3.0)*I3 - (T_kernel[0,1].real)*(CYCLE+CYCLE2)):.2e}")

    # The construction did not take (xbar, ybar) as input. It took only the
    # microscopic (x, y, delta) primitive coordinates and produced a definite
    # operator.
    print(f"  [INFO] Microscopic input  (x={x.tolist()}, y={y.tolist()}, delta={delta})")
    print(f"  [INFO] Constructed T_kernel diagonal entry  ({T_kernel[0,0].real:.6f})")
    print(f"  [INFO] Constructed T_kernel off-diagonal entry  ({T_kernel[0,1].real:.6f})")


def part2_spectrum_of_dynamically_built_kernel_recovers_the_seed_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SPECTRUM OF T_kernel(T_act) RECOVERS THE SEED PAIR")
    print("=" * 88)

    # Use a non-trivial aligned-patch sample, again without supplying
    # (xbar, ybar) anywhere in the construction of T_act or T_kernel.
    xbar_true = 0.90
    ybar_true = 0.40
    x = np.full(3, xbar_true, dtype=float)
    y = np.full(3, ybar_true, dtype=float)
    delta = 0.0

    T_act = active_corner_transport(x, y, delta)
    T_kernel = transfer_kernel_from_primitive(T_act)

    # Measure the spectrum.
    vals, vecs = eig_sorted(T_kernel)
    u0 = np.ones(3, dtype=complex) / np.sqrt(3.0)

    check("T_kernel is positive on this aligned patch",
          float(np.min(vals)) > 0.0,
          f"eigenvalues={np.round(vals, 8).tolist()}")
    check("The dominant eigenvector is the symmetric hw=1 mode",
          abs(np.vdot(u0, vecs[:, 0])) > 1 - 1e-12,
          f"|<u0,v0>|={abs(np.vdot(u0, vecs[:, 0])):.12f}")
    check("The two orthogonal eigenvalues are exactly degenerate",
          abs(vals[1] - vals[2]) < 1e-12,
          f"lambda_- split={abs(vals[1] - vals[2]):.2e}")
    check("Eigenvalues match (2 xbar + 2 ybar, 2 xbar - ybar) of T_kernel",
          abs(vals[0] - (2.0 * xbar_true + 2.0 * ybar_true)) < 1e-12
          and abs(vals[1] - (2.0 * xbar_true - ybar_true)) < 1e-12,
          f"vals={np.round(vals, 8).tolist()}")

    # Spectral measurement of (xbar, ybar) from the dynamically constructed
    # operator T_kernel.
    rec_xbar, rec_ybar = spectral_seed_pair_from_kernel(T_kernel)
    check("The dominant + subdominant eigenvalues measure xbar exactly",
          abs(rec_xbar - xbar_true) < 1e-12,
          f"measured xbar = (lam_+ + 2 lam_-)/6 = {rec_xbar:.12f}")
    check("The dominant + subdominant eigenvalues measure ybar exactly",
          abs(rec_ybar - ybar_true) < 1e-12,
          f"measured ybar = (lam_+ - lam_-)/3 = {rec_ybar:.12f}")
    print(f"  [INFO] (xbar, ybar) read from spectrum of T_kernel(T_act)  ({rec_xbar:.6f}, {rec_ybar:.6f})")


def part3_kernel_construction_agrees_with_corner_transport_orbit_moments() -> None:
    print("\n" + "=" * 88)
    print("PART 3: T_kernel ENCODES THE SAME ORBIT MOMENTS USED IN PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK")
    print("=" * 88)

    # Cross-check that the new construction is structurally compatible with the
    # sibling note PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE: the orbit moments
    # (t_even, t_fwd, t_bwd) used there determine the diagonal and
    # off-diagonal entries of T_kernel(T_act) by the relations
    #
    #     T_kernel diag = 2 Re(t_even)
    #     T_kernel hop  = Re(t_fwd) + Re(t_bwd).
    #
    # On the aligned weak-axis patch (delta = 0) t_bwd = 0 and Re(t_fwd) = ybar,
    # so the off-diagonal entry equals ybar exactly. The runner verifies the
    # general relation on an off-aligned sample as well.
    xbar_true = 0.90
    ybar_true = 0.40

    for label, x, y, delta in (
        ("aligned weak-axis patch",
         np.full(3, xbar_true, dtype=float),
         np.full(3, ybar_true, dtype=float),
         0.0),
        ("generic off-aligned sample",
         np.array([1.10, 0.78, 0.82], dtype=float),
         np.array([0.55, 0.31, 0.34], dtype=float),
         0.37),
    ):
        T_act = active_corner_transport(x, y, delta)
        T_kernel = transfer_kernel_from_primitive(T_act)

        t_even = np.trace(T_act) / 3.0
        t_fwd = (T_act[0, 1] + T_act[1, 2] + T_act[2, 0]) / 3.0
        t_bwd = (T_act[0, 2] + T_act[2, 1] + T_act[1, 0]) / 3.0

        kernel_diag = T_kernel[0, 0].real
        kernel_hop = T_kernel[0, 1].real

        check(f"({label}) T_kernel diagonal entry = 2 Re(t_even)",
              abs(kernel_diag - 2.0 * t_even.real) < 1e-12,
              f"diag={kernel_diag:.8f}, 2 Re(t_even)={2.0 * t_even.real:.8f}")
        check(f"({label}) T_kernel hop entry = Re(t_fwd) + Re(t_bwd)",
              abs(kernel_hop - (t_fwd.real + t_bwd.real)) < 1e-12,
              f"hop={kernel_hop:.8f}, Re(t_fwd)+Re(t_bwd)={t_fwd.real + t_bwd.real:.8f}")

    print("  [INFO] T_kernel(T_act) is the orbit-averaged Hermitization of the same")
    print("         corner-transport primitive used in PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK.")


def part4_kernel_is_blind_to_zero_sum_corner_breaking_carrier() -> None:
    print("\n" + "=" * 88)
    print("PART 4: T_kernel HAS AN EXACT KERNEL ON THE 5-REAL OFF-SEED BREAKING CARRIER")
    print("=" * 88)

    # Two distinct off-seed microscopic samples with the same seed averages and
    # delta = 0 (aligned weak axis). They differ only in the zero-sum
    # corner-breaking coordinates, so they must collapse to the same T_kernel.
    xbar_true = 0.90
    ybar_true = 0.40

    x1 = np.array([1.15, 0.82, 0.73], dtype=float)
    y1 = np.array([0.50, 0.25, 0.45], dtype=float)
    x2 = np.array([1.05, 0.88, 0.77], dtype=float)
    y2 = np.array([0.39, 0.36, 0.45], dtype=float)

    # Force matching seed averages while preserving distinct breaking carriers.
    x1 += xbar_true - float(np.mean(x1))
    x2 += xbar_true - float(np.mean(x2))
    y1 += ybar_true - float(np.mean(y1))
    y2 += ybar_true - float(np.mean(y2))

    T_act_1 = active_corner_transport(x1, y1, 0.0)
    T_act_2 = active_corner_transport(x2, y2, 0.0)

    T_kernel_1 = transfer_kernel_from_primitive(T_act_1)
    T_kernel_2 = transfer_kernel_from_primitive(T_act_2)

    check("The two primitive corner-transport operators are genuinely different",
          np.linalg.norm(T_act_1 - T_act_2) > 1e-6,
          f"|T_act_1 - T_act_2|={np.linalg.norm(T_act_1 - T_act_2):.6f}")
    check("Their dynamically constructed transfer kernels coincide",
          np.linalg.norm(T_kernel_1 - T_kernel_2) < 1e-10,
          f"|T_kernel_1 - T_kernel_2|={np.linalg.norm(T_kernel_1 - T_kernel_2):.2e}")

    # Spectral measurement of the seed pair from either kernel gives the same
    # (xbar, ybar): this is the blindness to the zero-sum off-seed carrier.
    rec_1 = spectral_seed_pair_from_kernel(T_kernel_1)
    rec_2 = spectral_seed_pair_from_kernel(T_kernel_2)
    check("Both spectral measurements return the same seed pair",
          abs(rec_1[0] - rec_2[0]) < 1e-12 and abs(rec_1[1] - rec_2[1]) < 1e-12,
          f"rec_1={rec_1}, rec_2={rec_2}")
    check("Each spectral measurement matches the shared seed pair (xbar, ybar)",
          abs(rec_1[0] - xbar_true) < 1e-12 and abs(rec_1[1] - ybar_true) < 1e-12,
          f"rec_1={rec_1}, true=({xbar_true:.6f}, {ybar_true:.6f})")

    print("  [INFO] T_kernel(T_act) has a genuine kernel on the 5-real off-seed corner-")
    print("         breaking carrier (zero-sum xi, eta directions on the aligned patch).")


def part5_weak_axis_seed_patch_recovery_is_spectral_not_supplied() -> None:
    print("\n" + "=" * 88)
    print("PART 5: WEAK-AXIS SEED PATCH RECOVERY IS A SPECTRAL MEASUREMENT, NOT A SUPPLIED LAW")
    print("=" * 88)

    # Sweep three different aligned-patch microscopic samples; each time the
    # seed pair is measured from the spectrum of the dynamically constructed
    # kernel, not assumed.
    samples = [
        (0.90, 0.40),
        (1.10, 0.25),
        (0.55, 0.10),
    ]
    for xbar_true, ybar_true in samples:
        x = np.full(3, xbar_true, dtype=float)
        y = np.full(3, ybar_true, dtype=float)
        T_act = active_corner_transport(x, y, 0.0)
        T_kernel = transfer_kernel_from_primitive(T_act)

        # The aligned weak-axis seed kernel is what T_kernel becomes on this
        # patch: 2 xbar I + ybar (C + C^2). Compare the constructed T_kernel to
        # this aligned form -- the inputs (xbar, ybar) here are the ones the
        # microscopic sample carries, not external inputs to T_kernel itself.
        expected = 2.0 * xbar_true * I3 + ybar_true * (CYCLE + CYCLE2)
        check(f"(xbar={xbar_true}, ybar={ybar_true}) T_kernel matches the aligned weak-axis seed form exactly",
              np.linalg.norm(T_kernel - expected) < 1e-12,
              f"error={np.linalg.norm(T_kernel - expected):.2e}")

        rec_xbar, rec_ybar = spectral_seed_pair_from_kernel(T_kernel)
        check(f"(xbar={xbar_true}, ybar={ybar_true}) spectral seed-pair measurement matches",
              abs(rec_xbar - xbar_true) < 1e-12 and abs(rec_ybar - ybar_true) < 1e-12,
              f"measured=({rec_xbar:.8f}, {rec_ybar:.8f})")

    print("  [INFO] Across all three samples, T_kernel is constructed only from primitive")
    print("         corner-transport amplitudes; the seed pair emerges as a spectrum")
    print("         readout of T_kernel(T_act), not as a supplied input to it.")


def main() -> int:
    print("=" * 88)
    print("PMNS TRANSFER OPERATOR DOMINANT MODE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can a genuinely dynamical native law on the hw=1 triplet recover any")
    print("  of the active microscopic PMNS data from corner-to-corner transport?")

    part1_kernel_is_built_from_the_primitive_corner_transport_operator()
    part2_spectrum_of_dynamically_built_kernel_recovers_the_seed_pair()
    part3_kernel_construction_agrees_with_corner_transport_orbit_moments()
    part4_kernel_is_blind_to_zero_sum_corner_breaking_carrier()
    part5_weak_axis_seed_patch_recovery_is_spectral_not_supplied()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive native dynamical law on the aligned hw=1 active patch:")
    print("    - the transfer kernel T_kernel(T_act) is constructed from primitive")
    print("      corner-transport amplitudes (x_i, y_i, delta) by Hermitization +")
    print("      C3 orbit-averaging, with no (xbar, ybar) input")
    print("    - the dominant + subdominant eigenvalues of T_kernel measure the")
    print("      aligned seed pair (xbar, ybar) of T_act exactly")
    print("    - the same construction agrees with the orbit moments used in")
    print("      PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE")
    print()
    print("  Boundary:")
    print("    - T_kernel has an exact kernel on the 5-real off-seed corner-breaking")
    print("      carrier; the route does not determine that source")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
