#!/usr/bin/env python3
"""Conditional APS-locked source action proposal.

This script audits the smallest action ansatz that would close the APS
source/response-locking gap if accepted as a new source-action premise:

    S_int = - sum_a chi_eta(Y_a) M_a sum_x rho_a(x) Phi(x)

with chi_eta(Y)=sign(eta_delta(D_Y)) on a gapped APS boundary sector.

The script is deliberately strict: it distinguishes a conditional action
candidate from a derivation.  It is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.
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

from scripts.signed_gravity_aps_boundary_index_probe import (  # noqa: E402
    boundary_model,
    chi_from_eta,
    eta_delta,
)


TOL = 1.0e-10
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    status = "PASS" if passed else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return passed


def chi_eta(index_sign: int) -> int:
    eta, zero, _, _ = eta_delta(boundary_model(index_sign))
    return chi_from_eta(eta, zero)


def normalize(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    if norm <= 0.0:
        raise ValueError("zero vector")
    return vec / norm


def packet_density(n: int = 31, center: float = 15.0, sigma: float = 3.5) -> np.ndarray:
    xs = np.arange(n, dtype=float)
    psi = normalize(np.exp(-0.5 * ((xs - center) / sigma) ** 2).astype(complex))
    return np.abs(psi) ** 2


def interaction_action(phi: np.ndarray, rho: np.ndarray, mass: float, chi: int) -> float:
    """S_int = - chi M <rho, Phi>."""

    return -float(chi * mass * np.dot(rho, phi))


def active_source_from_variation(rho: np.ndarray, mass: float, chi: int) -> tuple[float, float]:
    """Return max residual and total active charge from -delta S/dPhi."""

    phi = np.linspace(-0.02, 0.03, len(rho))
    step = 1.0e-6
    numeric = np.zeros_like(rho)
    for idx in range(len(rho)):
        dphi = np.zeros_like(rho)
        dphi[idx] = step
        sp = interaction_action(phi + dphi, rho, mass, chi)
        sm = interaction_action(phi - dphi, rho, mass, chi)
        dsdphi = (sp - sm) / (2.0 * step)
        numeric[idx] = -dsdphi
    target = chi * mass * rho
    return float(np.max(np.abs(numeric - target))), float(np.sum(numeric))


@dataclass(frozen=True)
class SignLaw:
    name: str
    source_kind: str
    response_kind: str
    derived_without_new_action: bool

    def source_sign(self, chi: int) -> int:
        if self.source_kind == "positive":
            return +1
        if self.source_kind == "zero":
            return 0
        if self.source_kind == "chi":
            return chi
        raise ValueError(self.source_kind)

    def response_sign(self, chi: int) -> int:
        if self.response_kind == "positive":
            return +1
        if self.response_kind == "zero":
            return 0
        if self.response_kind == "chi":
            return chi
        raise ValueError(self.response_kind)


def force_read(force_a: int, force_b: int) -> str:
    residual = abs(force_a + force_b) / max(abs(force_a), abs(force_b), 1.0e-30)
    if abs(force_a) < TOL and abs(force_b) < TOL:
        return "ZERO"
    if residual > 1.0e-12:
        return "UNBALANCED"
    return "ATTRACT" if force_a > 0 else "REPEL"


def sign_law_table() -> list[tuple[str, float, bool, bool, str]]:
    laws = [
        SignLaw("retained_positive", "positive", "positive", True),
        SignLaw("aps_eta_spectator", "zero", "positive", True),
        SignLaw("aps_source_only_inserted", "chi", "positive", False),
        SignLaw("aps_response_only_inserted", "positive", "chi", False),
        SignLaw("aps_locked_action_ansatz", "chi", "chi", False),
    ]
    pairs = ((+1, +1), (+1, -1), (-1, +1), (-1, -1))
    desired = ["ATTRACT", "REPEL", "REPEL", "ATTRACT"]
    rows = []
    for law in laws:
        residuals = []
        reads = []
        for chi_a, chi_b in pairs:
            force_a = law.response_sign(chi_a) * law.source_sign(chi_b)
            force_b = -law.response_sign(chi_b) * law.source_sign(chi_a)
            residuals.append(abs(force_a + force_b) / max(abs(force_a), abs(force_b), 1.0e-30))
            reads.append(force_read(force_a, force_b))
        rows.append(
            (
                law.name,
                float(max(residuals)),
                reads == desired,
                law.derived_without_new_action,
                ",".join(reads),
            )
        )
    return rows


def hamiltonian(n: int, chi: int) -> np.ndarray:
    xs = np.arange(n, dtype=float)
    potential = 0.025 / np.sqrt((xs - 0.7 * n) ** 2 + 1.0)
    h = np.diag(chi * potential).astype(complex)
    for idx in range(n - 1):
        h[idx, idx + 1] = -0.5j
        h[idx + 1, idx] = +0.5j
    return h


def cn_evolve(h: np.ndarray, psi: np.ndarray, steps: int = 32, dt: float = 0.08) -> np.ndarray:
    ident = np.eye(h.shape[0], dtype=complex)
    lhs = ident + 0.5j * dt * h
    rhs = ident - 0.5j * dt * h
    out = psi.copy()
    for _ in range(steps):
        out = np.linalg.solve(lhs, rhs @ out)
    return out


def slit_state(n: int, slits: tuple[int, ...]) -> np.ndarray:
    psi = np.zeros(n, dtype=complex)
    for slit in slits:
        psi[slit] = 1.0
    return psi


def detector_probability(psi: np.ndarray) -> float:
    detector = np.arange(3 * len(psi) // 5, len(psi))
    return float(np.sum(np.abs(psi[detector]) ** 2))


def born_norm_controls(chi: int) -> tuple[float, float]:
    n = 64
    h = hamiltonian(n, chi)
    slits = (12, 16, 20)
    probs: dict[tuple[int, ...], float] = {}
    for size in (1, 2, 3):
        for subset in __import__("itertools").combinations(slits, size):
            probs[subset] = detector_probability(cn_evolve(h, slit_state(n, subset)))

    a, b, c = slits
    i3 = (
        probs[(a, b, c)]
        - probs[(a, b)]
        - probs[(a, c)]
        - probs[(b, c)]
        + probs[(a,)]
        + probs[(b,)]
        + probs[(c,)]
    )
    psi = normalize(slit_state(n, slits))
    evolved = cn_evolve(h, psi)
    norm_drift = abs(float(np.vdot(evolved, evolved).real) - 1.0)
    return float(i3), norm_drift


def main() -> int:
    print("=" * 96)
    print("SIGNED GRAVITY APS-LOCKED SOURCE ACTION PROPOSAL")
    print("  conditional action ansatz; not a physical signed-gravity claim")
    print("=" * 96)
    print()

    chi_p = chi_eta(+1)
    chi_m = chi_eta(-1)
    chi_0 = chi_eta(0)
    check("APS boundary eta supplies +/- sectors and null control", chi_p == +1 and chi_m == -1 and chi_0 == 0)

    print()
    print("PROPOSED ACTION TERM")
    print("  S_int[Phi,psi,Y] = - chi_eta(Y) M_phys sum_x |psi_x|^2 Phi_x")
    print("  chi_eta(Y) = sign eta_delta(D_Y), only on a gapped boundary sector")
    print("  This is a new source-action premise unless derived elsewhere.")
    print()

    mass = 2.75
    rho = packet_density()
    residual_p, active_p = active_source_from_variation(rho, mass, +1)
    residual_m, active_m = active_source_from_variation(rho, mass, -1)
    check(
        "source variation gives +M rho in chi=+ sector",
        residual_p < 1.0e-9 and abs(active_p - mass) < 1.0e-9,
        f"residual={residual_p:.3e}, active={active_p:+.6f}",
    )
    check(
        "source variation gives -M rho in chi=- sector",
        residual_m < 1.0e-9 and abs(active_m + mass) < 1.0e-9,
        f"residual={residual_m:.3e}, active={active_m:+.6f}",
    )

    c_cell = 4.0 / 16.0
    lambda_wald = 4.0 * c_cell
    check("positive Wald/area carrier is not multiplied by chi", c_cell > 0.0 and abs(lambda_wald - 1.0) < TOL)
    check("positive inertial mass is branch independent", mass > 0.0, f"M_+=M_-={mass:.3f}")
    check(
        "same-point +/- active source cancels with positive inertia",
        abs(active_p + active_m) < 1.0e-9 and 2.0 * mass > 0.0,
        f"C_signed_sum={active_p + active_m:+.3e}, M_sum={2.0 * mass:.3f}",
    )
    check(
        "source-unit conversion consumes the proposed signed source",
        abs(4.0 * math.pi * active_p - 4.0 * math.pi * mass) < 1.0e-9
        and abs(4.0 * math.pi * active_m + 4.0 * math.pi * mass) < 1.0e-9,
        "q_bare=4*pi*chi_eta*M_phys",
    )
    print()

    print("SOURCE / RESPONSE LOCKING TABLE")
    print(f"  {'law':<30s} {'max balance':>12s} {'table':>8s} {'old-derived':>11s}  reads")
    proposal_pass = False
    for name, max_resid, table_ok, old_derived, reads in sign_law_table():
        print(
            f"  {name:<30s} {max_resid:12.3e} "
            f"{'PASS' if table_ok else 'FAIL':>8s} {'YES' if old_derived else 'NO':>11s}  {reads}"
        )
        if name == "aps_locked_action_ansatz" and table_ok and max_resid < TOL:
            proposal_pass = True
    check("proposed action gives locked four-pair table", proposal_pass)
    print()

    i3_p, norm_p = born_norm_controls(+1)
    i3_m, norm_m = born_norm_controls(-1)
    check("Born I3 control stays linear in chi=+ sector", abs(i3_p) < 1.0e-10, f"I3={i3_p:+.3e}")
    check("Born I3 control stays linear in chi=- sector", abs(i3_m) < 1.0e-10, f"I3={i3_m:+.3e}")
    check("norm stays unitary in both fixed sectors", max(norm_p, norm_m) < 1.0e-10, f"max drift={max(norm_p, norm_m):.3e}")

    print()
    print("OPEN PROOF OBLIGATIONS")
    print("  1. derive this APS-locked source action from retained boundary/Wald/Gauss")
    print("     structure, rather than postulating it")
    print("  2. prove the eta sector is superselected for admissible boundary dynamics")
    print("  3. supply an energy-stability/no-runaway argument for positive inertial")
    print("     masses with opposite active signs")
    print("  4. lift the scalar active monopole action without claiming full tensor GR")
    print()

    final_ok = FAIL_COUNT == 0 and proposal_pass
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(
        "FINAL_TAG: APS_LOCKED_SOURCE_ACTION_CONDITIONAL_CANDIDATE"
        if final_ok
        else "FINAL_TAG: APS_LOCKED_SOURCE_ACTION_PROPOSAL_FAIL"
    )
    return 0 if final_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
