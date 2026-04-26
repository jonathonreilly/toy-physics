#!/usr/bin/env python3
"""Source-density audit for the signed gravitational response lane.

This P0 harness asks whether the retained parity-correct scalar coupling

    H_diag = (m + Phi) epsilon

naturally supplies a branch-fixed signed gravitational source.  It separates
four cases that must not be conflated:

  1. Born source:       rho = |psi|^2
  2. scalar bilinear:  rho_s = epsilon |psi|^2
  3. selector source:  rho_Q = <psi|Q_chi|psi>
  4. inserted control: rho_g = chi_g |psi|^2

The last case is a useful control, not a derivation of chi_g.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.frontier_signed_gravity_chi_selector_algebra import (  # noqa: E402
    EPSILON,
    I8,
    PAULIS,
    evaluate,
    kron,
)


EPS = 1e-12


@dataclass(frozen=True)
class SourceForm:
    name: str
    variational_from_scalar: bool
    signed: bool
    branch_fixed: bool
    conserved_on_retained_surface: bool
    positive_inertial_mass: bool
    native: bool

    @property
    def physical_candidate(self) -> bool:
        return (
            self.variational_from_scalar
            and self.signed
            and self.branch_fixed
            and self.conserved_on_retained_surface
            and self.positive_inertial_mass
            and self.native
        )


def passfail(condition: bool) -> str:
    return "PASS" if condition else "FAIL"


def parity(n: int) -> np.ndarray:
    return np.where(np.arange(n) % 2 == 0, 1.0, -1.0)


def normalize(psi: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(psi)
    if norm <= 0.0:
        raise ValueError("cannot normalize zero state")
    return psi / norm


def gaussian_packet(n: int, center: float, sigma: float, phase_k: float = 0.0) -> np.ndarray:
    xs = np.arange(n, dtype=float)
    envelope = np.exp(-0.5 * ((xs - center) / sigma) ** 2)
    phase = np.exp(1j * phase_k * xs)
    return normalize((envelope * phase).astype(np.complex128))


def hamiltonian_1d(phi: np.ndarray, mass: float = 0.3, response_sign: int = +1) -> np.ndarray:
    """Open 1D staggered Hamiltonian with parity scalar coupling."""

    n = len(phi)
    eps = parity(n)
    h = np.diag(((mass + response_sign * phi) * eps).astype(np.complex128))
    for x in range(n - 1):
        h[x, x + 1] = -0.5j
        h[x + 1, x] = +0.5j
    return h


def cn_evolve(hamiltonian: np.ndarray, psi: np.ndarray, steps: int = 64, dt: float = 0.075) -> np.ndarray:
    n = hamiltonian.shape[0]
    ident = np.eye(n, dtype=np.complex128)
    lhs = ident + 0.5j * dt * hamiltonian
    rhs = ident - 0.5j * dt * hamiltonian
    out = psi.astype(np.complex128, copy=True)
    for _ in range(steps):
        out = np.linalg.solve(lhs, rhs @ out)
    return out


def born_density(psi: np.ndarray) -> np.ndarray:
    return np.abs(psi) ** 2


def scalar_density(psi: np.ndarray) -> np.ndarray:
    return parity(len(psi)) * born_density(psi)


def scalar_charge(psi: np.ndarray) -> float:
    return float(np.sum(scalar_density(psi)).real)


def energy(psi: np.ndarray, phi: np.ndarray, response_sign: int = +1) -> float:
    h = hamiltonian_1d(phi, response_sign=response_sign)
    return float(np.vdot(psi, h @ psi).real)


def variational_derivative_residual(response_sign: int = +1) -> float:
    n = 48
    phi = np.linspace(-0.015, 0.02, n)
    psi = gaussian_packet(n, center=21.3, sigma=4.0, phase_k=0.19)
    analytic = response_sign * scalar_density(psi)
    numeric = np.zeros(n, dtype=float)
    step = 2e-6
    for idx in range(n):
        dphi = np.zeros(n, dtype=float)
        dphi[idx] = step
        ep = energy(psi, phi + dphi, response_sign=response_sign)
        em = energy(psi, phi - dphi, response_sign=response_sign)
        numeric[idx] = (ep - em) / (2.0 * step)
    return float(np.max(np.abs(numeric - analytic)))


def packet_source_rows() -> list[tuple[float, float, float, float, float]]:
    n = 96
    rows: list[tuple[float, float, float, float, float]] = []
    for sigma in (0.65, 1.25, 2.50, 5.00, 10.00):
        even = gaussian_packet(n, center=40.0, sigma=sigma)
        odd = gaussian_packet(n, center=41.0, sigma=sigma)
        phase = gaussian_packet(n, center=40.0, sigma=sigma, phase_k=0.73)
        rows.append(
            (
                sigma,
                float(np.sum(born_density(even))),
                scalar_charge(even),
                scalar_charge(odd),
                abs(scalar_charge(even) - scalar_charge(phase)),
            )
        )
    return rows


def scalar_charge_drift() -> tuple[float, float, float]:
    n = 96
    psi0 = gaussian_packet(n, center=40.0, sigma=1.25, phase_k=0.11)
    h0 = hamiltonian_1d(np.zeros(n))
    psi1 = cn_evolve(h0, psi0, steps=96, dt=0.075)
    norm_drift = abs(float(np.vdot(psi1, psi1).real) - 1.0)
    return scalar_charge(psi0), scalar_charge(psi1), norm_drift


def continuum_scalar_charge_rows() -> list[tuple[float, int, float, float]]:
    rows: list[tuple[float, int, float, float]] = []
    sigma_phys = 0.75
    for h in (1.0, 0.5, 0.25, 0.125):
        sigma_sites = sigma_phys / h
        n = int(max(96, math.ceil(16 * sigma_sites)))
        if n % 2 == 1:
            n += 1
        center = n / 2
        psi = gaussian_packet(n, center=center, sigma=sigma_sites)
        rows.append((h, n, float(np.sum(born_density(psi))), scalar_charge(psi)))
    return rows


def pauli_string(name: str) -> np.ndarray:
    return kron(*(PAULIS[label] for label in name))


def eigenspace(operator: np.ndarray, eigenvalue: int) -> np.ndarray:
    vals, vecs = np.linalg.eigh(operator)
    mask = vals * eigenvalue > 0.5
    return vecs[:, mask]


def restricted_epsilon_metrics(q: np.ndarray, branch: int) -> tuple[int, float, float, float]:
    basis = eigenspace(q, branch)
    restricted = basis.conj().T @ EPSILON @ basis
    vals = np.linalg.eigvalsh(restricted).real
    return len(vals), float(np.min(vals)), float(np.max(vals)), float(np.mean(vals))


def branch_source_rows() -> list[tuple[str, bool, bool, tuple[int, float, float, float], tuple[int, float, float, float]]]:
    names = ("IXY", "XYI", "XZY", "ZZZ")
    rows = []
    for name in names:
        q = pauli_string(name)
        row = evaluate(name, q)
        rows.append(
            (
                name,
                row.massive_conserved,
                row.scalar_pinned,
                restricted_epsilon_metrics(q, +1),
                restricted_epsilon_metrics(q, -1),
            )
        )
    return rows


def inserted_source_unit_control() -> tuple[float, float, float, float, float]:
    masses = np.array([0.5, 1.0, 2.0, 4.0, 8.0], dtype=float)
    q_plus = 4.0 * math.pi * masses
    q_minus = -4.0 * math.pi * masses
    slope_plus = float(np.polyfit(np.log(masses), np.log(np.abs(q_plus)), 1)[0])
    slope_minus = float(np.polyfit(np.log(masses), np.log(np.abs(q_minus)), 1)[0])
    neutral_q = float(4.0 * math.pi * (1.75 - 1.75))
    neutral_inertia = float(1.75 + 1.75)
    null_q = float(4.0 * math.pi * 0.0)
    return slope_plus, slope_minus, neutral_q, neutral_inertia, null_q


def source_form_table() -> list[SourceForm]:
    return [
        SourceForm(
            name="Born rho=|psi|^2",
            variational_from_scalar=False,
            signed=False,
            branch_fixed=False,
            conserved_on_retained_surface=True,
            positive_inertial_mass=True,
            native=True,
        ),
        SourceForm(
            name="scalar rho_s=epsilon|psi|^2",
            variational_from_scalar=True,
            signed=True,
            branch_fixed=False,
            conserved_on_retained_surface=False,
            positive_inertial_mass=True,
            native=True,
        ),
        SourceForm(
            name="neutral selector rho_Q=<Q>",
            variational_from_scalar=False,
            signed=True,
            branch_fixed=False,
            conserved_on_retained_surface=True,
            positive_inertial_mass=True,
            native=True,
        ),
        SourceForm(
            name="inserted rho_g=chi_g|psi|^2",
            variational_from_scalar=False,
            signed=True,
            branch_fixed=True,
            conserved_on_retained_surface=True,
            positive_inertial_mass=True,
            native=False,
        ),
    ]


def main() -> None:
    print("=" * 100)
    print("SIGNED GRAVITY SOURCE VARIATIONAL AUDIT")
    print("  P0 gate: source primitive, not a negative-mass or propulsion claim")
    print("=" * 100)
    print()

    print("VARIATIONAL SOURCE CHECK")
    res_plus = variational_derivative_residual(+1)
    res_minus = variational_derivative_residual(-1)
    print("  H_diag = (m + response_sign * Phi) epsilon")
    print(f"  max residual dE/dPhi - response_sign*epsilon*|psi|^2, response +: {res_plus:.3e}")
    print(f"  max residual dE/dPhi - response_sign*epsilon*|psi|^2, response -: {res_minus:.3e}")
    print("  read: the scalar coupling varies to the parity scalar density, not to chi_g|psi|^2")
    print()

    print("SPATIAL PARITY SCALAR SOURCE STABILITY")
    print(f"  {'sigma':>6s} {'Born':>9s} {'Q_scalar even':>15s} {'Q_scalar odd':>15s} {'phase delta':>12s}")
    print("  " + "-" * 66)
    for sigma, born, q_even, q_odd, phase_delta in packet_source_rows():
        print(f"  {sigma:6.2f} {born:9.6f} {q_even:+15.6e} {q_odd:+15.6e} {phase_delta:12.2e}")
    q0, q1, norm_drift = scalar_charge_drift()
    print()
    print(f"  free evolution scalar charge: {q0:+.6e} -> {q1:+.6e}")
    print(f"  free evolution norm drift: {norm_drift:.3e}")
    print("  read: epsilon|psi|^2 is signed, but a one-site translation flips it and kinetic hopping does not conserve it")
    print()

    print("CONTINUUM / REFINEMENT SANITY FOR PARITY SCALAR SOURCE")
    print(f"  {'h':>7s} {'N':>5s} {'Born':>9s} {'Q_scalar':>15s}")
    print("  " + "-" * 44)
    for h, n, born, q_scalar in continuum_scalar_charge_rows():
        print(f"  {h:7.3f} {n:5d} {born:9.6f} {q_scalar:+15.6e}")
    print("  read: the parity scalar monopole washes out under refinement for a smooth packet")
    print()

    print("LOCAL/TASTE BRANCH SOURCE CHECK")
    print(
        f"  {'Q':<5s} {'conserved':>10s} {'pins eps':>9s} "
        f"{'+ dim':>5s} {'+ eps min/max/mean':>25s} {'- dim':>5s} {'- eps min/max/mean':>25s}"
    )
    print("  " + "-" * 94)
    for name, conserved, pinned, plus, minus in branch_source_rows():
        pdim, pmin, pmax, pmean = plus
        mdim, mmin, mmax, mmean = minus
        print(
            f"  {name:<5s} {passfail(conserved):>10s} {passfail(pinned):>9s} "
            f"{pdim:5d} [{pmin:+.1f},{pmax:+.1f},{pmean:+.1f}]"
            f"{mdim:15d} [{mmin:+.1f},{mmax:+.1f},{mmean:+.1f}]"
        )
    print("  read: conserved neutral taste labels do not pin scalar source sign; epsilon pins sign but is not conserved")
    print()

    slope_plus, slope_minus, neutral_q, neutral_inertia, null_q = inserted_source_unit_control()
    print("INSERTED SIGNED SOURCE CONTROL")
    print(f"  q_bare = 4*pi*chi_g*M_phys gives |q|~M slope, chi=+1: {slope_plus:.6f}")
    print(f"  q_bare = 4*pi*chi_g*M_phys gives |q|~M slope, chi=-1: {slope_minus:.6f}")
    print(f"  null source gives null active source: q_bare={null_q:+.3e}")
    print(f"  same-point inserted +/- active source cancellation: q_bare={neutral_q:+.3e}")
    print(f"  same-point inserted +/- inertial mass sum: {neutral_inertia:.3f}")
    print("  read: source-unit normalization can carry a sign only after chi_g is supplied elsewhere")
    print()

    print("SOURCE FORM GATE TABLE")
    print(
        f"  {'form':<34s} {'var':>4s} {'sign':>5s} {'branch':>7s} "
        f"{'cons':>5s} {'m_i>0':>6s} {'native':>6s} {'candidate':>9s}"
    )
    print("  " + "-" * 92)
    forms = source_form_table()
    for form in forms:
        print(
            f"  {form.name:<34s} "
            f"{passfail(form.variational_from_scalar):>4s} "
            f"{passfail(form.signed):>5s} "
            f"{passfail(form.branch_fixed):>7s} "
            f"{passfail(form.conserved_on_retained_surface):>5s} "
            f"{passfail(form.positive_inertial_mass):>6s} "
            f"{passfail(form.native):>6s} "
            f"{passfail(form.physical_candidate):>9s}"
        )
    print()

    derivative_ok = res_plus < 1e-9 and res_minus < 1e-9
    born_positive = all(abs(row[1] - 1.0) < 1e-12 for row in packet_source_rows())
    scalar_translation_flip = packet_source_rows()[0][2] * packet_source_rows()[0][3] < 0.0
    scalar_not_conserved = abs(q1 - q0) > 1e-3
    neutral_labels_unpinned = all(
        plus[1] < -0.9 and plus[2] > 0.9 and minus[1] < -0.9 and minus[2] > 0.9
        for name, conserved, pinned, plus, minus in branch_source_rows()
        if name != "ZZZ"
    )
    no_native_candidate = not any(form.physical_candidate for form in forms)

    print("P0 SOURCE-PRIMITIVE VERDICT")
    print(f"  variational derivative identified: {passfail(derivative_ok)}")
    print(f"  positive Born/inertial density retained: {passfail(born_positive)}")
    print(f"  parity scalar translation flip observed: {passfail(scalar_translation_flip)}")
    print(f"  parity scalar nonconservation observed: {passfail(scalar_not_conserved)}")
    print(f"  conserved taste labels scalar-unpinned: {passfail(neutral_labels_unpinned)}")
    print(f"  native signed source candidate found: {passfail(not no_native_candidate)}")
    print()
    print("FINAL_TAG: SOURCE_PRIMITIVE_BLOCKED_LOCAL" if no_native_candidate else "FINAL_TAG: SOURCE_PRIMITIVE_CANDIDATE")


if __name__ == "__main__":
    main()
