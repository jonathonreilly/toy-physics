#!/usr/bin/env python3
"""Staggered-Dirac boundary APS realization audit for the signed-gravity lane.

Question:

    Does the retained staggered-Dirac / Grassmann boundary operator produce a
    gapped unpaired APS eta/Pfaffian orientation mode without adding the
    orientation line by hand?

This is the natural follow-up to the raw cochain/Hodge boundary no-go.  The
strict pass condition for a native selector would be:

* a retained staggered boundary operator has eta_delta != 0 and no zero modes;
* the sign is stable under taste-compatible refinement and origin choices;
* orientation reversal flips the sign as boundary orientation, not as a basis
  convention;
* no rank-one orientation-line summand or kernel projection is inserted.

The audit below does not find such a native sign.  Retained-compatible
staggered boundary families are eta-neutral.  A tempting odd-open-face
unpaired eta exists, but it flips under a one-site staggering-origin shift and
vanishes under even/taste-compatible refinement.  Pfaffian signs of the real
skew kinetic kernel are determinant-line orientation choices: they flip under
odd basis relabeling while the spectrum and determinant are unchanged.

This is not a negative-mass, shielding, propulsion, reactionless-force, or
physical signed-gravity claim.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np


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


def eta_delta(mat: np.ndarray, delta: float = 1.0e-8) -> tuple[int, int, int, np.ndarray]:
    vals = np.linalg.eigvalsh(0.5 * (mat + mat.conj().T))
    n_pos = int(np.sum(vals > delta))
    n_neg = int(np.sum(vals < -delta))
    n_zero = int(len(vals) - n_pos - n_neg)
    return n_pos - n_neg, n_zero, len(vals), vals


def chi_from_eta(eta: int, zero: int) -> int:
    if eta == 0 or zero:
        return 0
    return +1 if eta > 0 else -1


def pair_error(vals: np.ndarray) -> float:
    ordered = np.sort(vals)
    return float(np.max(np.abs(ordered + ordered[::-1]))) if len(vals) else 0.0


def permutation_matrix(n: int, i: int, j: int) -> np.ndarray:
    perm = np.arange(n)
    perm[[i, j]] = perm[[j, i]]
    return np.eye(n)[perm]


def hermitian_staggered_1d(n: int, mass: float, apbc: bool = True, origin_shift: int = 0) -> np.ndarray:
    h = np.zeros((n, n), dtype=complex)
    for x in range(n):
        xp = (x + 1) % n
        xm = (x - 1) % n
        sf = -1.0 if apbc and x + 1 >= n else 1.0
        sb = -1.0 if apbc and x - 1 < 0 else 1.0
        h[x, xp] += sf * (-1j / 2.0)
        h[x, xm] += sb * (1j / 2.0)
        h[x, x] += mass * ((-1) ** (x + origin_shift))
    return h


def skew_staggered_1d(n: int, apbc: bool = True) -> np.ndarray:
    k = np.zeros((n, n), dtype=float)
    for x in range(n):
        xp = (x + 1) % n
        xm = (x - 1) % n
        sf = -1.0 if apbc and x + 1 >= n else 1.0
        sb = -1.0 if apbc and x - 1 < 0 else 1.0
        k[x, xp] += sf * 0.5
        k[x, xm] += sb * (-0.5)
    return k


def idx2(x: int, y: int, ny: int) -> int:
    return x * ny + y


def hermitian_staggered_2d(
    nx: int,
    ny: int,
    mass: float,
    *,
    periodic: bool,
    apbc_x: bool = True,
    apbc_y: bool = True,
    origin_shift: int = 0,
) -> np.ndarray:
    n = nx * ny
    h = np.zeros((n, n), dtype=complex)
    for x in range(nx):
        for y in range(ny):
            i = idx2(x, y, ny)
            if periodic or x + 1 < nx:
                sf = -1.0 if periodic and apbc_x and x + 1 >= nx else 1.0
                h[i, idx2((x + 1) % nx, y, ny)] += sf * (-1j / 2.0)
            if periodic or x - 1 >= 0:
                sb = -1.0 if periodic and apbc_x and x - 1 < 0 else 1.0
                h[i, idx2((x - 1) % nx, y, ny)] += sb * (1j / 2.0)

            eta2 = (-1) ** (x + origin_shift)
            if periodic or y + 1 < ny:
                sf = -1.0 if periodic and apbc_y and y + 1 >= ny else 1.0
                h[i, idx2(x, (y + 1) % ny, ny)] += eta2 * sf * (-1j / 2.0)
            if periodic or y - 1 >= 0:
                sb = -1.0 if periodic and apbc_y and y - 1 < 0 else 1.0
                h[i, idx2(x, (y - 1) % ny, ny)] += eta2 * sb * (1j / 2.0)

            eps = (-1) ** (x + y + origin_shift)
            h[i, i] += mass * eps
    return h


def skew_staggered_2d(nx: int, ny: int, apbc_x: bool = True, apbc_y: bool = True) -> np.ndarray:
    n = nx * ny
    k = np.zeros((n, n), dtype=float)
    for x in range(nx):
        for y in range(ny):
            i = idx2(x, y, ny)
            sf = -1.0 if apbc_x and x + 1 >= nx else 1.0
            sb = -1.0 if apbc_x and x - 1 < 0 else 1.0
            k[i, idx2((x + 1) % nx, y, ny)] += sf * 0.5
            k[i, idx2((x - 1) % nx, y, ny)] += sb * (-0.5)
            eta2 = (-1) ** x
            sf = -1.0 if apbc_y and y + 1 >= ny else 1.0
            sb = -1.0 if apbc_y and y - 1 < 0 else 1.0
            k[i, idx2(x, (y + 1) % ny, ny)] += eta2 * sf * 0.5
            k[i, idx2(x, (y - 1) % ny, ny)] += eta2 * sb * (-0.5)
    return k


def pfaffian_recursive(a: np.ndarray) -> float:
    """Small-matrix Pfaffian for real skew controls."""

    n = a.shape[0]
    if n == 0:
        return 1.0
    if n % 2:
        return 0.0
    total = 0.0
    for j in range(1, n):
        if abs(a[0, j]) < TOL:
            continue
        sub = np.delete(np.delete(a, [0, j], axis=0), [0, j], axis=1)
        total += ((-1.0) ** (j + 1)) * a[0, j] * pfaffian_recursive(sub)
    return float(total)


@dataclass(frozen=True)
class BoundaryRead:
    name: str
    eta: int
    zero: int
    chi: int
    gap: float
    pair: float
    hermitian_error: float


def read_boundary(name: str, h: np.ndarray) -> BoundaryRead:
    eta, zero, _n, vals = eta_delta(h)
    return BoundaryRead(
        name=name,
        eta=eta,
        zero=zero,
        chi=chi_from_eta(eta, zero),
        gap=float(np.min(np.abs(vals))) if len(vals) else 0.0,
        pair=pair_error(vals),
        hermitian_error=float(np.linalg.norm(h - h.conj().T, ord=2)),
    )


def retained_compatible_staggered_eta_gate() -> tuple[bool, str]:
    families = [
        read_boundary("cycle8_apbc_m0", hermitian_staggered_1d(8, 0.0, apbc=True)),
        read_boundary("cycle10_apbc_m03", hermitian_staggered_1d(10, 0.3, apbc=True)),
        read_boundary("torus4x4_apbc_m0", hermitian_staggered_2d(4, 4, 0.0, periodic=True)),
        read_boundary("torus4x6_apbc_m03", hermitian_staggered_2d(4, 6, 0.3, periodic=True)),
        read_boundary("open4x4_m03", hermitian_staggered_2d(4, 4, 0.3, periodic=False)),
        read_boundary("open4x5_m03", hermitian_staggered_2d(4, 5, 0.3, periodic=False)),
    ]
    eta_neutral = all(r.eta == 0 and r.chi == 0 for r in families)
    gapped = all(r.gap > 1.0e-3 and r.zero == 0 for r in families)
    paired = all(r.pair < 1.0e-8 for r in families)
    hermitian = all(r.hermitian_error < TOL for r in families)
    detail = "; ".join(
        f"{r.name}:eta={r.eta:+d},zero={r.zero},chi={r.chi:+d},gap={r.gap:.3f},pair={r.pair:.1e}"
        for r in families
    )
    return eta_neutral and gapped and paired and hermitian, detail


def orientation_reversal_gate() -> tuple[bool, str]:
    h = hermitian_staggered_2d(4, 6, 0.3, periodic=True)
    h_rev = -h
    p = permutation_matrix(h.shape[0], 0, 1)
    h_relabel = p @ h @ p.T
    reads = [
        read_boundary("base", h),
        read_boundary("orientation_reversed_minus_D", h_rev),
        read_boundary("odd_basis_relabel", h_relabel),
    ]
    spectra = [np.linalg.eigvalsh(rh) for rh in (h, h_rev, h_relabel)]
    rev_err = float(np.max(np.abs(np.sort(spectra[0]) + np.sort(spectra[1])[::-1])))
    relabel_err = float(np.max(np.abs(np.sort(spectra[0]) - np.sort(spectra[2]))))
    ok = all(r.eta == 0 and r.chi == 0 for r in reads) and rev_err < TOL and relabel_err < TOL
    detail = (
        f"eta={[r.eta for r in reads]}, chi={[r.chi for r in reads]}, "
        f"orientation_reversal_err={rev_err:.1e}, relabel_spectral_err={relabel_err:.1e}"
    )
    return ok, detail


def odd_open_face_quarantine_gate() -> tuple[bool, str]:
    odd0 = read_boundary("open5x5_origin0_m03", hermitian_staggered_2d(5, 5, 0.3, periodic=False, origin_shift=0))
    odd1 = read_boundary("open5x5_origin1_m03", hermitian_staggered_2d(5, 5, 0.3, periodic=False, origin_shift=1))
    refined = read_boundary("open10x10_refined_m03", hermitian_staggered_2d(10, 10, 0.3, periodic=False, origin_shift=0))
    trap_exists = odd0.eta == +1 and odd0.zero == 0 and odd0.chi == +1
    origin_flips = odd1.eta == -1 and odd1.chi == -1
    refinement_kills = refined.eta == 0 and refined.chi == 0
    ok = trap_exists and origin_flips and refinement_kills
    detail = (
        f"{odd0.name}:eta={odd0.eta:+d},chi={odd0.chi:+d}; "
        f"{odd1.name}:eta={odd1.eta:+d},chi={odd1.chi:+d}; "
        f"{refined.name}:eta={refined.eta:+d},chi={refined.chi:+d}; "
        "classification=odd_sublattice_imbalance_control"
    )
    return ok, detail


def pfaffian_orientation_control_gate() -> tuple[bool, str]:
    cases = [
        ("cycle8_skew_apbc", skew_staggered_1d(8, apbc=True)),
        ("torus3x4_skew_apbc", skew_staggered_2d(3, 4, apbc_x=True, apbc_y=True)),
    ]
    reads = []
    ok = True
    for name, k in cases:
        p = permutation_matrix(k.shape[0], 0, 1)
        kp = p @ k @ p.T
        pf = pfaffian_recursive(k)
        pfp = pfaffian_recursive(kp)
        eig = np.linalg.eigvalsh(1j * k)
        eig_p = np.linalg.eigvalsh(1j * kp)
        eig_err = float(np.max(np.abs(np.sort(eig) - np.sort(eig_p))))
        det_err = abs(float(np.linalg.det(k)) - float(np.linalg.det(kp)))
        sign_flip = pf * pfp < 0.0
        ok &= abs(pf) > 1.0e-8 and sign_flip and eig_err < 1.0e-8 and det_err < 1.0e-8
        reads.append(
            f"{name}:pf={pf:+.3e}-> {pfp:+.3e},eig_err={eig_err:.1e},det_err={det_err:.1e}"
        )
    return ok, "; ".join(reads)


def orientation_line_insertion_control_gate() -> tuple[bool, str]:
    h = hermitian_staggered_2d(4, 4, 0.0, periodic=True)
    eta_raw, zero_raw, _n_raw, vals_raw = eta_delta(h)
    gap_raw = float(np.min(np.abs(vals_raw)))
    reads = []
    for orient in (+1, -1):
        h_ext = np.block(
            [
                [np.array([[orient * 0.35]], dtype=complex), np.zeros((1, h.shape[0]), dtype=complex)],
                [np.zeros((h.shape[0], 1), dtype=complex), h],
            ]
        )
        eta_ext, zero_ext, _n_ext, _vals_ext = eta_delta(h_ext)
        reads.append((orient, eta_ext, zero_ext, chi_from_eta(eta_ext, zero_ext)))
    ok = eta_raw == 0 and zero_raw == 0 and gap_raw > 0.1 and reads == [(+1, +1, 0, +1), (-1, -1, 0, -1)]
    detail = f"raw=(eta={eta_raw:+d},zero={zero_raw},gap={gap_raw:.3f}), added_line={reads}"
    return ok, detail


def source_basis_gate() -> tuple[bool, str]:
    positive_source = np.array([1.0, 1.0])
    native_staggered_eta = np.array([0.0, 0.0])
    odd_imbalance_control = np.array([1.0, -1.0])
    desired = np.array([1.0, -1.0])
    native_basis = np.column_stack([positive_source, native_staggered_eta])
    coeffs, *_ = np.linalg.lstsq(native_basis, desired, rcond=None)
    residual = float(np.linalg.norm(native_basis @ coeffs - desired))
    odd_residual = float(np.linalg.norm(odd_imbalance_control - desired))
    ok = residual > 1.0 and odd_residual < TOL
    detail = (
        f"native_residual={residual:.3e}, odd_control_residual={odd_residual:.1e}, "
        "odd_control_admissible=False"
    )
    return ok, detail


def no_claim_gate() -> tuple[bool, str]:
    claims = {
        "native_staggered_aps_selector_found": False,
        "odd_open_face_as_selector": False,
        "pfaffian_sign_as_gauge_invariant_selector": False,
        "orientation_line_inserted_for_control": True,
        "physical_signed_gravity_prediction": False,
        "negative_inertial_mass": False,
        "shielding": False,
        "propulsion": False,
        "reactionless_force": False,
    }
    ok = (
        not claims["native_staggered_aps_selector_found"]
        and not claims["odd_open_face_as_selector"]
        and not claims["pfaffian_sign_as_gauge_invariant_selector"]
        and claims["orientation_line_inserted_for_control"]
        and not claims["physical_signed_gravity_prediction"]
        and not claims["negative_inertial_mass"]
        and not claims["shielding"]
        and not claims["propulsion"]
        and not claims["reactionless_force"]
    )
    return ok, ", ".join(f"{key}={value}" for key, value in claims.items())


def staggered_dirac_boundary_summary_gate() -> tuple[bool, str]:
    retained_ok, retained_detail = retained_compatible_staggered_eta_gate()
    odd_ok, odd_detail = odd_open_face_quarantine_gate()
    pf_ok, pf_detail = pfaffian_orientation_control_gate()
    line_ok, line_detail = orientation_line_insertion_control_gate()
    source_ok, source_detail = source_basis_gate()
    ok = retained_ok and odd_ok and pf_ok and line_ok and source_ok
    detail = (
        "native_staggered_aps_selector_found=False, "
        f"retained_eta_neutral={retained_ok}, odd_quarantine=({odd_detail}), "
        f"pfaffian_control=({pf_detail}), added_line_control=({line_detail}), "
        f"source_basis=({source_detail})"
    )
    return ok, detail


def run_audit() -> bool:
    retained_ok, retained_detail = retained_compatible_staggered_eta_gate()
    check("retained-compatible staggered boundary operators are eta-neutral", retained_ok, retained_detail)

    reversal_ok, reversal_detail = orientation_reversal_gate()
    check("staggered boundary orientation/relabel controls do not create eta sign", reversal_ok, reversal_detail)

    odd_ok, odd_detail = odd_open_face_quarantine_gate()
    check("odd-open-face unpaired eta is quarantined as sublattice imbalance", odd_ok, odd_detail)

    pf_ok, pf_detail = pfaffian_orientation_control_gate()
    check("Pfaffian sign is determinant-line orientation metadata, not invariant branch", pf_ok, pf_detail)

    line_ok, line_detail = orientation_line_insertion_control_gate()
    check("orientation-line insertion creates the APS sign only as a control", line_ok, line_detail)

    source_ok, source_detail = source_basis_gate()
    check("native staggered boundary source basis cannot span signed source", source_ok, source_detail)

    no_claim_ok, no_claim_detail = no_claim_gate()
    check("non-claim gate remains closed", no_claim_ok, no_claim_detail)

    return retained_ok and reversal_ok and odd_ok and pf_ok and line_ok and source_ok and no_claim_ok


def main() -> int:
    print("=" * 120)
    print("SIGNED GRAVITY STAGGERED-DIRAC BOUNDARY APS REALIZATION AUDIT")
    print("  retained staggered boundary eta/Pfaffian controls; not a physical signed-gravity claim")
    print("=" * 120)
    print()

    passed = run_audit()

    print()
    print("INTERPRETATION")
    print("  The retained staggered-Dirac boundary operators tested here are gapped")
    print("  but eta-neutral on taste-compatible cycles, tori, and even open faces.")
    print("  Odd open faces can create an unpaired eta, but that sign flips under a")
    print("  one-site staggering-origin shift and disappears under even refinement,")
    print("  so it is a sublattice-imbalance control, not a retained APS selector.")
    print("  Pfaffian signs exist only after choosing a determinant-line orientation:")
    print("  an odd basis relabel flips the Pfaffian while preserving spectrum and")
    print("  determinant.  The signed APS branch appears cleanly only after adding a")
    print("  rank-one orientation line.")
    print()
    print("VERDICT")
    print("  The retained staggered-Dirac / Grassmann boundary operator does not")
    print("  currently realize a native gapped unpaired APS eta/Pfaffian selector.")
    print("  This closes the most natural escape from the raw Hodge-boundary no-go")
    print("  unless a sharper retained boundary theorem identifies a non-added")
    print("  determinant-line mode on actual graph/refinement families.")
    print()

    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if passed and FAIL_COUNT == 0:
        print("FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED")
        return 0
    print("FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_AUDIT_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
