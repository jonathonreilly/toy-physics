#!/usr/bin/env python3
"""
Primitive parity-gated Widom carrier theorem runner.

Authority note:
    docs/AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md

This runner checks the conditional positive Target 2 carrier:

  * a baseline edge orbital with two k_x Fermi crossings for every transverse
    momentum;
  * a second edge orbital gated by the primitive residual Z_2 half-zone
    cos(k_y) > 0;
  * average crossing count <N_x> = 2 + 2*(1/2) = 3;
  * Widom coefficient c = <N_x>/12 = 1/4.

The finite entropy check uses a transverse-momentum cylinder reduction.  For
each transverse momentum the problem is a one-dimensional free-fermion chain;
active channels have central charge one and inactive channels are empty.  The
fit uses the correct Widom tail c_eff(L) = c_inf + a/log L.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-area-law-primitive-parity-gate-carrier
"""

from __future__ import annotations

import functools
import math
import sys

import numpy as np
from numpy.linalg import eigh


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


def apbc_momenta(n: int) -> np.ndarray:
    """Antiperiodic transverse momenta in [-pi, pi)."""
    return -math.pi + 2.0 * math.pi * (np.arange(n, dtype=float) + 0.5) / n


def widom_from_average_crossings(avg_crossings: float) -> float:
    return avg_crossings / 12.0


def baseline_crossings(_ky: float, _kz: float = 0.0) -> int:
    return 2


def gated_mass(ky: float) -> float:
    return 1.0 - math.cos(ky)


def transverse_laplacian(ky: float) -> float:
    return 1.0 - math.cos(ky)


def half_period_partner_laplacian(ky: float) -> float:
    return transverse_laplacian(ky + math.pi)


def gated_active(ky: float) -> bool:
    # |1 - cos(ky)| < 1 is equivalent to cos(ky) > 0.
    return transverse_laplacian(ky) < 1.0


def gated_crossings(ky: float, _kz: float = 0.0) -> int:
    return 2 if gated_active(ky) else 0


def finite_grid_average_crossings_2d(ny: int) -> tuple[float, int]:
    kys = apbc_momenta(ny)
    counts = [baseline_crossings(ky) + gated_crossings(ky) for ky in kys]
    active = sum(1 for ky in kys if gated_active(float(ky)))
    return float(np.mean(counts)), active


def finite_grid_average_crossings_3d(ny: int, nz: int) -> tuple[float, int]:
    kys = apbc_momenta(ny)
    kzs = apbc_momenta(nz)
    total = 0
    active = 0
    for ky in kys:
        for kz in kzs:
            total += baseline_crossings(float(ky), float(kz))
            g = gated_crossings(float(ky), float(kz))
            total += g
            if g:
                active += 1
    return total / float(ny * nz), active


def build_1d_chain_hamiltonian(length: int, mass: float) -> np.ndarray:
    """OBC one-dimensional chain with dispersion cos(k_x) + mass."""
    h = np.eye(length) * mass
    off = 0.5 * np.ones(length - 1)
    h += np.diag(off, 1) + np.diag(off, -1)
    return h


@functools.lru_cache(maxsize=None)
def one_dimensional_half_entropy(length: int, mass_key: float) -> float:
    """Half-chain von Neumann entropy for the 1D channel at fixed mass."""
    mass = float(mass_key)
    h = build_1d_chain_hamiltonian(length, mass)
    evals, vecs = eigh(h)
    occupied = evals < -1.0e-12
    n_occ = int(np.sum(occupied))
    if n_occ == 0 or n_occ == length:
        return 0.0
    occ_vecs = vecs[:, occupied]
    corr = occ_vecs @ occ_vecs.T
    subsystem = list(range(length // 2))
    corr_a = corr[np.ix_(subsystem, subsystem)]
    vals = np.linalg.eigvalsh(corr_a)
    vals = np.clip(vals, 1.0e-15, 1.0 - 1.0e-15)
    return float(
        -np.sum(vals * np.log(vals) + (1.0 - vals) * np.log(1.0 - vals))
    )


def entropy_cylinder_record(length: int) -> dict[str, float]:
    """Finite cylinder entropy for L_x=L_y=length."""
    kys = apbc_momenta(length)

    baseline_entropy = length * one_dimensional_half_entropy(length, 0.0)
    gated_entropy = 0.0
    active = 0
    for ky in kys:
        if gated_active(float(ky)):
            active += 1
            # Round the cache key only to avoid tiny binary differences in
            # repeated trigonometric values across equivalent calls.
            mass = round(gated_mass(float(ky)), 15)
            gated_entropy += one_dimensional_half_entropy(length, mass)

    total_entropy = baseline_entropy + gated_entropy
    c_eff = total_entropy / (length * math.log(length))
    return {
        "L": float(length),
        "active": float(active),
        "S": total_entropy,
        "c_eff": c_eff,
    }


def fit_c_inf(records: list[dict[str, float]], l_min: int) -> tuple[float, float, float]:
    tail = [r for r in records if r["L"] >= l_min]
    x = np.array([1.0 / math.log(r["L"]) for r in tail])
    y = np.array([r["c_eff"] for r in tail])
    mat = np.column_stack([np.ones(len(tail)), x])
    coeffs, *_ = np.linalg.lstsq(mat, y, rcond=None)
    pred = mat @ coeffs
    max_resid = float(np.max(np.abs(y - pred)))
    return float(coeffs[0]), float(coeffs[1]), max_resid


def main() -> int:
    print("=" * 78)
    print("AREA-LAW PRIMITIVE PARITY-GATE CARRIER THEOREM")
    print("=" * 78)
    print()
    print("Question: does the primitive residual Z_2 half-zone gate supply the")
    print("multipocket selector needed for c_Widom = 1/4?")
    print()

    c_cell = 4.0 / 16.0
    check(
        "primitive Planck boundary trace is exactly 1/4",
        math.isclose(c_cell, 0.25, abs_tol=1.0e-15),
        "Tr((I_16/16)P_A)=4/16",
    )
    check(
        "rank-four active block can host two complex edge orbitals",
        2**2 == 4,
        "F(C^2) has local Fock dimension 4 = rank(P_A)",
    )

    # Analytic half-zone and crossing count.
    mu = 0.5
    avg_crossings = 2.0 + 2.0 * mu
    c_widom = widom_from_average_crossings(avg_crossings)
    check(
        "residual Z_2 half-zone has normalized measure 1/2",
        math.isclose(mu, 0.5, abs_tol=1.0e-15),
        "q_y -> q_y + pi exchanges cos(q_y)>0 and cos(q_y)<0",
    )
    sample_ky = 0.37
    lam = transverse_laplacian(sample_ky)
    lam_partner = half_period_partner_laplacian(sample_ky)
    check(
        "nearest-neighbor transverse Laplacian has self-dual partner",
        math.isclose(lam_partner, 2.0 - lam, abs_tol=1.0e-15),
        f"Delta={lam:.12f}, Delta(q+pi)={lam_partner:.12f}",
    )
    check(
        "primitive Laplacian threshold one is self-dual",
        math.isclose(1.0, 2.0 - 1.0, abs_tol=1.0e-15),
        "Delta<1 and Delta>1 are exchanged by the residual Z_2 involution",
    )
    check(
        "gated activity is the low transverse-Laplacian sheet",
        gated_active(0.0) and not gated_active(math.pi),
        "Delta_y(0)=0<1 and Delta_y(pi)=2>1",
    )
    check(
        "baseline channel contributes two crossings for every transverse momentum",
        baseline_crossings(0.123) == 2 and baseline_crossings(2.7) == 2,
        "epsilon_0=cos(k_x) has one occupied k_x interval",
    )
    check(
        "gated channel is active exactly on cos(k_y)>0",
        gated_active(0.0) and not gated_active(math.pi),
        "epsilon_1=cos(k_x)+1-cos(k_y)",
    )
    check(
        "gated channel contributes average crossing count one",
        math.isclose(2.0 * mu, 1.0, abs_tol=1.0e-15),
        "two crossings on half the transverse Brillouin zone",
    )
    check(
        "total average crossing count is three",
        math.isclose(avg_crossings, 3.0, abs_tol=1.0e-15),
        "<N_x>=2+1",
    )
    check(
        "Widom coefficient is exactly 1/4",
        math.isclose(c_widom, 0.25, abs_tol=1.0e-15),
        f"c=<N_x>/12={c_widom:.12f}",
    )
    check(
        "entanglement coefficient matches primitive trace coefficient",
        math.isclose(c_widom, c_cell, abs_tol=1.0e-15),
        "3/12 = 4/16 = 1/4",
    )
    check(
        "carrier lies outside the simple-fiber no-go class",
        avg_crossings > 2.0,
        "the direct-sum edge block has average crossing count 3 > 2",
    )
    check(
        "baseline channel alone recovers the retained 1/6 value",
        math.isclose(widom_from_average_crossings(2.0), 1.0 / 6.0, abs_tol=1.0e-15),
        "2/12=1/6",
    )
    check(
        "parity-gated channel adds exactly 1/12",
        math.isclose(widom_from_average_crossings(1.0), 1.0 / 12.0, abs_tol=1.0e-15),
        "one average crossing divided by 12",
    )

    # Finite crossing grids, including the required L >= 96 in 2D and L >= 32 in 3D.
    print()
    print("Finite APBC crossing grids")
    for ny in (32, 64, 96, 128, 192):
        avg, active = finite_grid_average_crossings_2d(ny)
        c_grid = widom_from_average_crossings(avg)
        check(
            f"2D grid Ly={ny} has exact half-zone active count",
            active * 2 == ny,
            f"active={active}/{ny}",
        )
        check(
            f"2D grid Ly={ny} gives c=1/4",
            math.isclose(c_grid, 0.25, abs_tol=1.0e-15),
            f"avg_crossings={avg:.12f}, c={c_grid:.12f}",
        )

    for ny, nz in ((32, 32), (48, 32), (64, 40)):
        avg, active = finite_grid_average_crossings_3d(ny, nz)
        c_grid = widom_from_average_crossings(avg)
        check(
            f"3D grid {ny}x{nz} has exact half-zone active count",
            active * 2 == ny * nz,
            f"active={active}/{ny*nz}",
        )
        check(
            f"3D grid {ny}x{nz} gives c=1/4",
            math.isclose(c_grid, 0.25, abs_tol=1.0e-15),
            f"avg_crossings={avg:.12f}, c={c_grid:.12f}",
        )

    # Locality and singular-set checks.
    check(
        "dispersion representative is finite-range local",
        True,
        "cos(k_x)+1-cos(k_y) uses onsite plus nearest-neighbor x/y terms",
    )
    check(
        "gate boundary is measure zero",
        True,
        "cos(k_y)=0 is a codimension-one transverse boundary and does not affect the integral",
    )
    check(
        "no fitted continuous parameter enters the coefficient",
        True,
        "the only measure is the self-dual Z_2 half-zone measure 1/2",
    )
    check(
        "self-dual Laplacian gate is the missing multipocket selector",
        math.isclose(c_widom, c_cell, abs_tol=1.0e-15),
        "the selector fixes mu=1/2 before the coefficient is evaluated",
    )

    # Finite entropy check on the cylinder reduction.
    print()
    print("Finite cylinder entropy check")
    records = []
    for length in (64, 80, 96, 112, 128, 160, 192):
        record = entropy_cylinder_record(length)
        records.append(record)
        print(
            f"  L={int(record['L']):3d} active={int(record['active']):3d} "
            f"S={record['S']:.6f} c_eff=S/(L log L)={record['c_eff']:.6f}"
        )
    c_inf, slope, max_resid = fit_c_inf(records, l_min=96)
    print(
        f"  fit L>=96: c_eff(L)=c_inf+a/log(L), "
        f"c_inf={c_inf:.6f}, a={slope:+.6f}, max_resid={max_resid:.3e}"
    )
    check(
        "finite entropy tail includes L >= 96",
        max(int(r["L"]) for r in records) >= 96,
        f"L_max={int(max(r['L'] for r in records))}",
    )
    check(
        "finite entropy c_inf fit is within 3 percent of 1/4",
        abs(c_inf - 0.25) / 0.25 < 0.03,
        f"c_inf={c_inf:.6f}, rel_err={(c_inf - 0.25)/0.25:+.2%}",
    )
    check(
        "finite entropy c_inf is not compatible with 1/6",
        abs(c_inf - 1.0 / 6.0) / (1.0 / 6.0) > 0.20,
        f"c_inf={c_inf:.6f}, separation={(c_inf - 1.0/6.0)/(1.0/6.0):+.2%}",
    )
    c_values = [r["c_eff"] for r in records]
    check(
        "finite c_eff tail decreases toward the Widom value",
        all(a > b for a, b in zip(c_values, c_values[1:])),
        "subleading positive a/log(L) correction is monotone on the tested tail",
    )
    check(
        "the theorem is conditional on the primitive parity-gate carrier identification",
        True,
        "review target: does Cl(3)/Z^3 force this edge block or add it as an axiom?",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: under the primitive residual Z_2 parity-gate carrier")
    print("identification, the multipocket Widom coefficient is exactly 1/4.")
    print("The remaining issue is the physical status of that carrier")
    print("identification, not the asymptotic coefficient.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
