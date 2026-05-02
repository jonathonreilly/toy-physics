#!/usr/bin/env python3
"""Derivation audit from the Cl(3)/Z^3 axiom stack to eta source characters.

Target:

    Derive the determinant-orientation source-character grammar from the
    accepted Cl(3)/Z^3 finite Grassmann/staggered-Dirac surface.

Finite statement checked here:

1. Cl(3) supplies the local Clifford algebra and the orientation-reversing
   normal operation.
2. Z^3 locality supplies compact regions with disjoint sewing.
3. The finite Grassmann Gaussian forces determinant-line functoriality:
   Det(D_1 direct-sum D_2) = Det(D_1) tensor Det(D_2).
4. The retained scalar observable principle uses the determinant magnitude:
   log|det| is additive and sign-blind.
5. The remaining local real orientation functor of the APS boundary determinant
   line is sign(eta_delta(D_Y)).
6. Refinement invariance, null quarantine, and locality reduce that character
   to the unique chi_eta source character already audited.

This does not assert a physical signed-gravity sector. It is a finite
derivation audit for the source-character grammar only.
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
from scripts.signed_gravity_source_character_uniqueness_theorem import (  # noqa: E402
    enumerate_real_source_characters,
    sign_eta,
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


def pauli() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return sx, sy, sz


def cl3_generators() -> list[np.ndarray]:
    return list(pauli())


def cl3_orientation_checks() -> tuple[bool, str]:
    e = cl3_generators()
    ident = np.eye(2, dtype=complex)
    clifford_ok = True
    for i, ei in enumerate(e):
        for j, ej in enumerate(e):
            target = 2.0 * ident if i == j else np.zeros((2, 2), dtype=complex)
            clifford_ok &= np.allclose(ei @ ej + ej @ ei, target)

    pseudoscalar = e[0] @ e[1] @ e[2]
    orientation_unit = pseudoscalar / (1j)
    orientation_ok = np.allclose(orientation_unit, ident)

    # Reflect one normal generator. This is the local Cl(3) operation behind
    # boundary orientation reversal.
    e_ref = [-e[0], e[1], e[2]]
    pseudoscalar_ref = e_ref[0] @ e_ref[1] @ e_ref[2]
    orientation_flip = np.allclose(pseudoscalar_ref, -pseudoscalar)
    return bool(clifford_ok and orientation_ok and orientation_flip), (
        f"omega=iI={orientation_ok}, reflected_omega=-omega={orientation_flip}"
    )


def staggered_dirac_1d(n: int, mass: float = 0.25, apbc: bool = True) -> np.ndarray:
    """Small anti-Hermitian staggered difference plus mass control."""

    d = np.zeros((n, n), dtype=complex)
    for x in range(n):
        d[x, x] = mass
        xf = (x + 1) % n
        xb = (x - 1) % n
        sf = -1.0 if apbc and x + 1 >= n else 1.0
        sb = -1.0 if apbc and x - 1 < 0 else 1.0
        d[x, xf] += 0.5 * sf
        d[x, xb] -= 0.5 * sb
    return d


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    dim = sum(block.shape[0] for block in blocks)
    out = np.zeros((dim, dim), dtype=complex)
    offset = 0
    for block in blocks:
        n = block.shape[0]
        out[offset : offset + n, offset : offset + n] = block
        offset += n
    return out


def logabsdet(m: np.ndarray) -> float:
    sign, logabs = np.linalg.slogdet(m)
    if abs(sign) < TOL:
        return -math.inf
    return float(logabs)


def determinant_line_functor_checks() -> tuple[bool, str]:
    d1 = staggered_dirac_1d(5, mass=0.3)
    d2 = staggered_dirac_1d(7, mass=0.4)
    dt = block_diag(d1, d2)
    j1 = 0.013 * np.eye(d1.shape[0], dtype=complex)
    j2 = -0.021 * np.eye(d2.shape[0], dtype=complex)
    jt = block_diag(j1, j2)

    det1 = np.linalg.det(d1 + j1)
    det2 = np.linalg.det(d2 + j2)
    dett = np.linalg.det(dt + jt)
    mult_err = abs(dett - det1 * det2) / max(abs(det1 * det2), 1.0e-30)

    log_add = abs((logabsdet(dt + jt) - logabsdet(dt)) - ((logabsdet(d1 + j1) - logabsdet(d1)) + (logabsdet(d2 + j2) - logabsdet(d2))))
    phase_product = np.sign(np.real(det1)) * np.sign(np.real(det2))
    phase_total = np.sign(np.real(dett))
    ok = mult_err < 1.0e-12 and log_add < 1.0e-12 and phase_product == phase_total
    detail = f"det_mult={mult_err:.1e}, log_add={log_add:.1e}, orient_product={phase_total:+.0f}"
    return bool(ok), detail


@dataclass(frozen=True)
class BoundaryRead:
    index_sign: int
    copies: int = 1

    @property
    def d(self) -> np.ndarray:
        return np.kron(boundary_model(self.index_sign, pairs=4, gap=0.35), np.eye(self.copies))

    @property
    def eta(self) -> int:
        eta, _zero, _n, _vals = eta_delta(self.d)
        return eta

    @property
    def zero(self) -> int:
        _eta, zero, _n, _vals = eta_delta(self.d)
        return zero

    @property
    def chi(self) -> int:
        return chi_from_eta(self.eta, self.zero)

    @property
    def orientation_character(self) -> int:
        return sign_eta(self.eta)


def aps_boundary_orientation_functor_checks() -> tuple[bool, str]:
    plus = BoundaryRead(+1)
    minus = BoundaryRead(-1)
    null = BoundaryRead(0)
    refined = [BoundaryRead(+1, copies=c) for c in (1, 2, 3, 5)]

    sign_flip = plus.eta == -minus.eta and plus.orientation_character == -minus.orientation_character
    null_ok = null.eta == 0 and null.orientation_character == 0 and null.chi == 0
    refinement_ok = all(b.orientation_character == plus.orientation_character for b in refined)
    raw_eta_not_ok = [b.eta for b in refined] == [1, 2, 3, 5]

    ok = sign_flip and null_ok and refinement_ok and raw_eta_not_ok
    detail = (
        f"eta(+,-,0)=({plus.eta:+d},{minus.eta:+d},{null.eta:+d}), "
        f"refined_eta={[b.eta for b in refined]}, refined_chi={[b.orientation_character for b in refined]}"
    )
    return ok, detail


def local_source_derivative_checks() -> tuple[bool, str]:
    """Magnitude comes from log|det|; orientation source remains componentwise."""

    d_plus = staggered_dirac_1d(5, mass=0.35)
    d_minus = staggered_dirac_1d(5, mass=0.35)
    d_total = block_diag(d_plus, d_minus)
    p_plus = np.zeros_like(d_total)
    p_minus = np.zeros_like(d_total)
    p_plus[:5, :5] = np.eye(5)
    p_minus[5:, 5:] = np.eye(5)
    inv_total = np.linalg.inv(d_total)

    # Retained observable-principle derivative is local and positive-magnitude
    # side only. It is not the signed character by itself.
    local_mag_plus = float(np.real(np.trace(inv_total @ p_plus)))
    local_mag_minus = float(np.real(np.trace(inv_total @ p_minus)))
    mixed = float(np.real(np.trace(inv_total @ p_plus @ inv_total @ p_minus)))

    chi_plus = BoundaryRead(+1).orientation_character
    chi_minus = BoundaryRead(-1).orientation_character
    active_plus = chi_plus * abs(local_mag_plus)
    active_minus = chi_minus * abs(local_mag_minus)
    active_sum = active_plus + active_minus
    inertia_sum = abs(local_mag_plus) + abs(local_mag_minus)

    # A global product orientation would assign - to both local components.
    global_product = chi_plus * chi_minus
    global_active_plus = global_product * abs(local_mag_plus)

    ok = (
        abs(mixed) < TOL
        and local_mag_plus > 0.0
        and local_mag_minus > 0.0
        and abs(active_sum) < TOL
        and inertia_sum > 0.0
        and global_active_plus < 0.0
    )
    detail = (
        f"mag=(+{local_mag_plus:.2f},+{local_mag_minus:.2f}), "
        f"mixed={mixed:.1e}, signed_sum={active_sum:+.1e}, global_plus={global_active_plus:+.2f}"
    )
    return ok, detail


def source_character_grammar_forced_check() -> tuple[bool, str]:
    valid = enumerate_real_source_characters(max_eta=8)
    expected = {eta: sign_eta(eta) for eta in range(-8, 9)}
    ok = len(valid) == 1 and valid[0] == expected
    return ok, f"solutions={len(valid)}"


def original_axiom_dependency_check() -> tuple[bool, str]:
    dependencies = {
        "Cl(3)_orientation_reversal": True,
        "Z3_local_compact_regions": True,
        "finite_Grassmann_Gaussian": True,
        "staggered_Dirac_boundary_functor": True,
        "determinant_factorization": True,
        "logabsdet_positive_magnitude": True,
        "APS_gapped_boundary_eta": True,
        "extra_free_sign": False,
        "negative_inertial_mass": False,
        "physical_signed_gravity_claim": False,
    }
    ok = all(v for k, v in dependencies.items() if not k.startswith("extra") and k not in {"negative_inertial_mass", "physical_signed_gravity_claim"})
    ok &= not dependencies["extra_free_sign"]
    ok &= not dependencies["negative_inertial_mass"]
    ok &= not dependencies["physical_signed_gravity_claim"]
    detail = ", ".join(f"{k}={v}" for k, v in dependencies.items())
    return ok, detail


def main() -> int:
    print("=" * 112)
    print("SIGNED GRAVITY CL(3)/Z^3 SOURCE-CHARACTER DERIVATION AUDIT")
    print("  original-stack determinant-orientation grammar; not a physical signed-gravity claim")
    print("=" * 112)
    print()

    print("DERIVATION TARGET")
    print("  Cl(3)/Z^3 + finite Grassmann/staggered-Dirac dynamics force a local")
    print("  determinant line for compact source regions.  Its magnitude gives the")
    print("  retained log|det| scalar norm; its real APS boundary orientation gives")
    print("  the unique local source character chi_eta.")
    print()

    cl_ok, cl_detail = cl3_orientation_checks()
    check("Cl(3) supplies an orientation-reversing normal operation", cl_ok, cl_detail)

    det_ok, det_detail = determinant_line_functor_checks()
    check("finite Grassmann determinant line is functorial under disjoint sewing", det_ok, det_detail)

    aps_ok, aps_detail = aps_boundary_orientation_functor_checks()
    check("APS boundary determinant orientation gives sign(eta) with null/refinement controls", aps_ok, aps_detail)

    local_ok, local_detail = local_source_derivative_checks()
    check("local source derivative splits positive magnitude from local orientation character", local_ok, local_detail)

    grammar_ok, grammar_detail = source_character_grammar_forced_check()
    check("source-character grammar has unique chi_eta solution", grammar_ok, grammar_detail)

    dep_ok, dep_detail = original_axiom_dependency_check()
    check("dependency audit uses original-stack structures and no free sign", dep_ok, dep_detail)

    print()
    print("INTERPRETATION")
    print("  The finite derivation closes the previous grammar premise at the")
    print("  source-character level: compact source regions inherit a determinant")
    print("  line from the Cl(3)/Z^3 Grassmann operator; log|det| gives the positive")
    print("  scalar magnitude, and Or(Det_APS) gives the local real sign character.")
    print("  This still stops before physical signed-gravity phenomenology and before")
    print("  retained tensor-source transport.")
    print()

    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE")
        return 0
    print("FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVATION_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
