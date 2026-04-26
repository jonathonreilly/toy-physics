#!/usr/bin/env python3
"""Signed gravitational response sector first-pass harness.

This is a bounded discovery-lane tool. It does not assert that a physical
negative-gravity sector exists. It tests the minimal algebra required if a
native branch label chi_g = +/-1 is hosted by the Cl(3)/Z^3 staggered/taste
surface:

  source-only:          source sign = chi, response sign = +1
  response-only:        source sign = +1, response sign = chi
  source/response lock: source sign = chi, response sign = chi

Only the locked case is allowed to count as a candidate physical sector. The
other two are controls because they generically violate two-body momentum
balance for mixed signs.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np


MODES = ("source_only", "response_only", "locked")
PAIRS = ((+1, +1), (+1, -1), (-1, +1), (-1, -1))

CANDIDATE_ORIGIN = (
    "hosted candidate: a conserved Z2 orientation of the staggered scalar "
    "density / taste-parity mass branch, i.e. the sign of the scalar "
    "source bilinear relative to the parity-correct response channel"
)
CANDIDATE_STATUS = (
    "admissible-host check only; conservation and sector preparation are not "
    "derived in this pass"
)


@dataclass(frozen=True)
class PairResult:
    mode: str
    chi_a: int
    chi_b: int
    source_a: int
    response_a: int
    source_b: int
    response_b: int
    force_a: float
    force_b: float
    inertial_mass_a: float
    inertial_mass_b: float

    @property
    def coupling_a_from_b(self) -> int:
        return self.response_a * self.source_b

    @property
    def coupling_b_from_a(self) -> int:
        return self.response_b * self.source_a

    @property
    def balance_residual(self) -> float:
        scale = max(abs(self.force_a), abs(self.force_b), 1e-30)
        return abs(self.force_a + self.force_b) / scale

    @property
    def balanced(self) -> bool:
        return self.balance_residual < 1e-12

    @property
    def readout(self) -> str:
        if not self.balanced:
            return "UNBALANCED"
        return "ATTRACT" if self.coupling_a_from_b > 0 else "REPEL"


def sign_roles(mode: str, chi: int) -> tuple[int, int]:
    """Return (source_sign, response_sign) for one branch."""

    if chi not in (-1, +1):
        raise ValueError("chi must be +/-1")
    if mode == "source_only":
        return chi, +1
    if mode == "response_only":
        return +1, chi
    if mode == "locked":
        return chi, chi
    raise ValueError(f"unknown mode {mode!r}")


def kernel_force(distance: float, family: str = "inverse_square", h: float = 0.0, mu: float = 0.0) -> float:
    """Positive radial force magnitude for a unit source/test pair."""

    r = max(abs(distance), 1e-12)
    if family == "inverse_square":
        return 1.0 / (r * r)
    if family == "screened":
        return math.exp(-mu * r) * (1.0 / (r * r) + mu / r)
    if family == "soft_lattice":
        a2 = h * h
        return r / ((r * r + a2) ** 1.5)
    raise ValueError(f"unknown kernel family {family!r}")


def two_body_result(
    mode: str,
    chi_a: int,
    chi_b: int,
    inertial_mass_a: float = 1.0,
    inertial_mass_b: float = 1.0,
    z_a: float = -1.0,
    z_b: float = +1.0,
    family: str = "inverse_square",
    h: float = 0.0,
    mu: float = 0.0,
) -> PairResult:
    """Evaluate the signed two-body force on A(left) and B(right).

    Positive force on A points toward B. Negative force on B points toward A.
    With positive inertial masses, momentum balance requires F_A + F_B = 0.
    """

    if inertial_mass_a <= 0.0 or inertial_mass_b <= 0.0:
        raise ValueError("inertial masses must stay positive")
    if z_b <= z_a:
        raise ValueError("this harness assumes A is left of B")

    source_a, response_a = sign_roles(mode, chi_a)
    source_b, response_b = sign_roles(mode, chi_b)
    mag = inertial_mass_a * inertial_mass_b * kernel_force(z_b - z_a, family=family, h=h, mu=mu)

    # Interaction energy U_A|B = - response_A * source_B * m_A m_B G(r).
    # Therefore F_A = +(response_A * source_B) * |F| and
    # F_B = -(response_B * source_A) * |F|.
    force_a = response_a * source_b * mag
    force_b = -response_b * source_a * mag
    return PairResult(
        mode=mode,
        chi_a=chi_a,
        chi_b=chi_b,
        source_a=source_a,
        response_a=response_a,
        source_b=source_b,
        response_b=response_b,
        force_a=force_a,
        force_b=force_b,
        inertial_mass_a=inertial_mass_a,
        inertial_mass_b=inertial_mass_b,
    )


def four_pair_table(mode: str) -> list[PairResult]:
    return [two_body_result(mode, a, b) for a, b in PAIRS]


def _label_pair(a: int, b: int) -> str:
    return ("+" if a > 0 else "-") + ("+" if b > 0 else "-")


def _passfail(condition: bool) -> str:
    return "PASS" if condition else "FAIL"


def print_four_pair_tables() -> None:
    print("FOUR-PAIR SIGN TABLE")
    print("  A is left, B is right. F_A>0 and F_B<0 means attraction.")
    print()
    for mode in MODES:
        print(f"  mode={mode}")
        print(
            f"    {'pair':>4s}  {'src/resp A':>10s}  {'src/resp B':>10s}  "
            f"{'F_A':>9s}  {'F_B':>9s}  {'balance':>9s}  read"
        )
        for row in four_pair_table(mode):
            ar = f"{row.source_a:+d}/{row.response_a:+d}"
            br = f"{row.source_b:+d}/{row.response_b:+d}"
            print(
                f"    {_label_pair(row.chi_a, row.chi_b):>4s}  {ar:>10s}  {br:>10s}  "
                f"{row.force_a:+9.3e}  {row.force_b:+9.3e}  "
                f"{row.balance_residual:9.1e}  {row.readout}"
            )
        print()


def momentum_balance_scan() -> dict[str, float]:
    mass_cases = ((1.0, 1.0), (1.0, 3.0), (3.0, 1.0), (2.0, 5.0))
    out: dict[str, float] = {}
    for mode in MODES:
        residuals: list[float] = []
        for chi_a, chi_b in PAIRS:
            for ma, mb in mass_cases:
                row = two_body_result(mode, chi_a, chi_b, ma, mb)
                residuals.append(row.balance_residual)
        out[mode] = max(residuals)
    return out


def fm_scaling_slope(mode: str = "locked", chi_a: int = +1, chi_b: int = -1) -> float:
    source_masses = np.array([0.5, 1.0, 2.0, 4.0, 8.0], dtype=float)
    forces = np.array(
        [
            abs(two_body_result(mode, chi_a, chi_b, inertial_mass_a=1.25, inertial_mass_b=float(m)).force_a)
            for m in source_masses
        ],
        dtype=float,
    )
    slope, _ = np.polyfit(np.log(source_masses), np.log(forces), 1)
    return float(slope)


def _build_branch_hamiltonian(n: int, field: np.ndarray, response_sign: int, mass: float = 0.30) -> np.ndarray:
    hamiltonian = np.zeros((n, n), dtype=np.complex128)
    for x in range(n):
        parity = +1.0 if x % 2 == 0 else -1.0
        hamiltonian[x, x] = (mass + response_sign * field[x]) * parity
        if x + 1 < n:
            hamiltonian[x, x + 1] = -0.5j
            hamiltonian[x + 1, x] = +0.5j
    return hamiltonian


def _cn_evolve(hamiltonian: np.ndarray, psi: np.ndarray, steps: int = 32, dt: float = 0.08) -> np.ndarray:
    n = hamiltonian.shape[0]
    ident = np.eye(n, dtype=np.complex128)
    lhs = ident + 0.5j * dt * hamiltonian
    rhs = ident - 0.5j * dt * hamiltonian
    out = psi.astype(np.complex128, copy=True)
    for _ in range(steps):
        out = np.linalg.solve(lhs, rhs @ out)
    return out


def _slit_state(n: int, open_slits: tuple[int, ...]) -> np.ndarray:
    psi = np.zeros(n, dtype=np.complex128)
    for slit in open_slits:
        psi[slit] = 1.0 + 0j
    return psi


def _detector_probability(psi: np.ndarray) -> float:
    n = len(psi)
    detector = np.arange(3 * n // 5, n)
    return float(np.sum(np.abs(psi[detector]) ** 2))


def born_norm_control(mode: str = "locked", chi: int = +1) -> dict[str, float]:
    """Linear-Hamiltonian Born and norm controls for a fixed branch field."""

    n = 64
    xs = np.arange(n, dtype=float)
    source_site = 47.0
    raw_field = 0.035 / np.sqrt((xs - source_site) ** 2 + 1.0)
    source_sign, response_sign = sign_roles(mode, chi)
    field = source_sign * raw_field
    hamiltonian = _build_branch_hamiltonian(n, field, response_sign=response_sign)

    slits = (12, 16, 20)
    probs: dict[tuple[int, ...], float] = {}
    for size in (1, 2, 3):
        for subset in combinations(slits, size):
            evolved = _cn_evolve(hamiltonian, _slit_state(n, subset))
            probs[subset] = _detector_probability(evolved)

    a, b, c = slits
    p123 = probs[(a, b, c)]
    i3 = (
        p123
        - probs[(a, b)]
        - probs[(a, c)]
        - probs[(b, c)]
        + probs[(a,)]
        + probs[(b,)]
        + probs[(c,)]
    )
    i3_rel = abs(i3) / max(abs(p123), 1e-30)

    normalized = _slit_state(n, slits)
    normalized /= np.linalg.norm(normalized)
    evolved = _cn_evolve(hamiltonian, normalized)
    norm_drift = abs(float(np.vdot(evolved, evolved).real) - 1.0)

    zero_h_plus = _build_branch_hamiltonian(n, np.zeros(n), response_sign=+1)
    zero_h_minus = _build_branch_hamiltonian(n, np.zeros(n), response_sign=-1)
    zero_plus = _cn_evolve(zero_h_plus, normalized)
    zero_minus = _cn_evolve(zero_h_minus, normalized)
    null_branch_delta = abs(_detector_probability(zero_plus) - _detector_probability(zero_minus))

    return {
        "born_i3_rel": i3_rel,
        "norm_drift": norm_drift,
        "null_branch_delta": null_branch_delta,
    }


def continuum_family_sanity() -> dict[str, object]:
    family_specs = (
        ("inverse_square", {"family": "inverse_square"}),
        ("screened_mu_0p25", {"family": "screened", "mu": 0.25}),
        ("soft_lattice_h_0p50", {"family": "soft_lattice", "h": 0.50}),
        ("soft_lattice_h_0p25", {"family": "soft_lattice", "h": 0.25}),
        ("soft_lattice_h_0p125", {"family": "soft_lattice", "h": 0.125}),
    )
    family_rows = []
    for label, kwargs in family_specs:
        ok = True
        reads = []
        for chi_a, chi_b in PAIRS:
            row = two_body_result("locked", chi_a, chi_b, **kwargs)
            expected = "ATTRACT" if chi_a == chi_b else "REPEL"
            reads.append(row.readout)
            ok = ok and row.balanced and row.readout == expected
        family_rows.append((label, ok, reads))

    hs = np.array([1.0, 0.5, 0.25, 0.125], dtype=float)
    r = 3.0
    mags = np.array([kernel_force(r, family="soft_lattice", h=float(h)) for h in hs])
    target = kernel_force(r, family="inverse_square")
    rel_errors = np.abs(mags - target) / target

    return {
        "families": family_rows,
        "refinement_h": hs,
        "refinement_rel_errors": rel_errors,
        "refinement_monotone": bool(np.all(np.diff(rel_errors) < 0.0)),
    }


def main() -> None:
    print("=" * 92)
    print("SIGNED GRAVITATIONAL RESPONSE SECTOR HARNESS")
    print("  bounded first pass; not a negative-mass, shielding, or propulsion claim")
    print("=" * 92)
    print()
    print(f"candidate origin: {CANDIDATE_ORIGIN}")
    print(f"candidate status: {CANDIDATE_STATUS}")
    print()

    print_four_pair_tables()

    print("TWO-BODY MOMENTUM BALANCE CONTROL")
    balance = momentum_balance_scan()
    for mode in MODES:
        expectation = mode == "locked"
        passed = balance[mode] < 1e-12
        print(
            f"  {mode:<14s} max |F_A+F_B|/max|F| = {balance[mode]:.3e}  "
            f"{_passfail(passed == expectation)}"
        )
    print()

    inertial_masses = [1.0, 1.25, 2.0, 3.0, 5.0]
    positive_mass_ok = all(m > 0.0 for m in inertial_masses)
    fm_attr = fm_scaling_slope("locked", +1, +1)
    fm_rep = fm_scaling_slope("locked", +1, -1)
    controls = born_norm_control("locked", +1)
    print("BORN / NORM / NULL-FIELD / F~M CONTROLS")
    print(f"  positive inertial masses only: {_passfail(positive_mass_ok)}  min m={min(inertial_masses):.3f}")
    print(f"  Born |I3|/P on fixed branch Hamiltonian: {controls['born_i3_rel']:.3e}")
    print(f"  Crank-Nicolson norm drift: {controls['norm_drift']:.3e}")
    print(f"  null-field branch delta: {controls['null_branch_delta']:.3e}")
    print(f"  F~M slope, locked same-sector attraction: {fm_attr:.6f}")
    print(f"  F~M slope, locked opposite-sector repulsion: {fm_rep:.6f}")
    print()

    print("CONTINUUM / FAMILY-PORTABILITY SANITY")
    sanity = continuum_family_sanity()
    for label, ok, reads in sanity["families"]:
        print(f"  {label:<22s} {_passfail(ok)}  reads={','.join(reads)}")
    hs = sanity["refinement_h"]
    errs = sanity["refinement_rel_errors"]
    print("  soft-lattice force approaches inverse-square under refinement:")
    for h, err in zip(hs, errs):
        print(f"    h={h:.3f}: rel_error={err:.3e}")
    print(f"  refinement monotone: {_passfail(bool(sanity['refinement_monotone']))}")
    print()

    locked_expected = all(
        two_body_result("locked", a, b).readout == ("ATTRACT" if a == b else "REPEL")
        for a, b in PAIRS
    )
    all_gates = (
        locked_expected
        and balance["locked"] < 1e-12
        and positive_mass_ok
        and controls["born_i3_rel"] < 1e-10
        and controls["norm_drift"] < 1e-10
        and controls["null_branch_delta"] < 1e-12
        and abs(fm_attr - 1.0) < 1e-12
        and abs(fm_rep - 1.0) < 1e-12
        and all(ok for _, ok, _ in sanity["families"])
        and bool(sanity["refinement_monotone"])
    )
    print("FIRST-PASS VERDICT")
    print(f"  locked source/response sign algebra: {_passfail(locked_expected)}")
    print(f"  source-only and response-only are controls: PASS if mixed pairs fail balance")
    print(f"  candidate sector harness gates: {_passfail(all_gates)}")
    print("  status: consequence harness passed; native chi_g derivation remains open")


if __name__ == "__main__":
    main()
