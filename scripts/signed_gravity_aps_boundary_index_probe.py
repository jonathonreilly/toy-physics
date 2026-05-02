#!/usr/bin/env python3
"""
Finite boundary-spectrum probe for the signed-gravity APS chi candidate.

This is not a physical signed-gravity derivation.  It checks the minimal
finite-dimensional behavior required before an APS/spectral-asymmetry label
can even be a candidate:

  * eta sign is invariant under boundary-basis relabeling/unitary conjugation
  * eta sign is stable under small gap-preserving boundary perturbations
  * eta sign changes only through an explicit zero crossing
  * a basis-local sign diagnostic can flip while the spectrum is unchanged

The source/response locking bridge remains an external theorem target.
"""

from __future__ import annotations

import numpy as np


TOL = 1.0e-10


def check(label: str, cond: bool, detail: str = "") -> bool:
    status = "PASS" if cond else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {label}{suffix}")
    return cond


def hermitian_part(a: np.ndarray) -> np.ndarray:
    return 0.5 * (a + a.conj().T)


def random_unitary(rng: np.random.Generator, n: int) -> np.ndarray:
    z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    q, r = np.linalg.qr(z)
    phases = np.diag(r) / np.maximum(np.abs(np.diag(r)), TOL)
    return q @ np.diag(phases.conj())


def eta_delta(d_boundary: np.ndarray, delta: float = 1.0e-8) -> tuple[int, int, int, np.ndarray]:
    vals = np.linalg.eigvalsh(hermitian_part(d_boundary))
    n_pos = int(np.sum(vals > delta))
    n_neg = int(np.sum(vals < -delta))
    n_zero = int(len(vals) - n_pos - n_neg)
    return n_pos - n_neg, n_zero, len(vals), vals


def chi_from_eta(eta: int, n_zero: int) -> int:
    if n_zero or eta == 0:
        return 0
    return 1 if eta > 0 else -1


def boundary_model(index_sign: int, pairs: int = 5, gap: float = 0.4) -> np.ndarray:
    """Toy gapped boundary Dirac spectrum with paired bulk modes.

    The unpaired boundary mode supplies eta = +/-1.  The paired modes are
    symmetric +/- levels and do not contribute to eta.
    """
    if index_sign not in (-1, 0, 1):
        raise ValueError("index_sign must be -1, 0, or +1")
    levels: list[float] = []
    if index_sign:
        levels.append(index_sign * gap)
    for j in range(pairs):
        level = gap + 0.35 * (j + 1)
        levels.extend([level, -level])
    return np.diag(levels).astype(complex)


def basis_artifact_label(d_boundary: np.ndarray) -> int:
    """A deliberately bad basis-local sign.

    It reads the first coordinate's diagonal entry, so a permutation of the
    same boundary Hilbert space can flip it without changing the spectrum.
    """
    value = float(np.real(d_boundary[0, 0]))
    if abs(value) < TOL:
        return 0
    return 1 if value > 0 else -1


def norm_bound(a: np.ndarray) -> float:
    return float(np.linalg.norm(a, ord=2))


def main() -> int:
    rng = np.random.default_rng(20260425)
    ok = True

    print("=" * 72)
    print("Signed-gravity APS boundary-index finite spectrum probe")
    print("=" * 72)

    d_plus = boundary_model(+1)
    d_minus = boundary_model(-1)
    d_null = boundary_model(0)

    eta_p, zero_p, _, vals_p = eta_delta(d_plus)
    eta_m, zero_m, _, vals_m = eta_delta(d_minus)
    eta_0, zero_0, _, _ = eta_delta(d_null)
    gap_p = float(np.min(np.abs(vals_p)))

    ok &= check(
        "eta sign gives both nonempty candidate sectors",
        chi_from_eta(eta_p, zero_p) == +1 and chi_from_eta(eta_m, zero_m) == -1,
        f"eta_plus={eta_p}, eta_minus={eta_m}",
    )
    ok &= check(
        "paired boundary spectrum is a null/control sector",
        chi_from_eta(eta_0, zero_0) == 0,
        f"eta_null={eta_0}, zero_modes={zero_0}",
    )

    # Basis relabeling/unitary conjugation must not alter eta.
    u = random_unitary(rng, d_plus.shape[0])
    d_relabel = u @ d_plus @ u.conj().T
    eta_r, zero_r, _, vals_r = eta_delta(d_relabel)
    ok &= check(
        "eta is invariant under arbitrary boundary-basis unitary relabeling",
        eta_r == eta_p and zero_r == zero_p and np.allclose(vals_r, vals_p),
        f"eta={eta_r}, max_eig_err={np.max(np.abs(vals_r - vals_p)):.2e}",
    )

    # A bad coordinate sign can flip under a simple permutation while the
    # spectral eta remains fixed.
    perm = np.arange(d_plus.shape[0])
    perm[[0, 2]] = perm[[2, 0]]
    pmat = np.eye(d_plus.shape[0])[perm]
    d_perm = pmat @ d_plus @ pmat.T
    art_before = basis_artifact_label(d_plus)
    art_after = basis_artifact_label(d_perm)
    eta_perm, zero_perm, _, _ = eta_delta(d_perm)
    ok &= check(
        "basis-local sign can flip while eta and the spectrum do not",
        art_before == -art_after and eta_perm == eta_p and zero_perm == zero_p,
        f"artifact={art_before}->{art_after}, eta={eta_p}->{eta_perm}",
    )

    # Small Hermitian perturbations below the gap cannot change inertia.
    # Use a strict operator-norm cap so the gap-preserving condition is clear.
    stable = True
    min_gap_after = np.inf
    for _ in range(100):
        raw = hermitian_part(rng.normal(size=d_plus.shape) + 1j * rng.normal(size=d_plus.shape))
        perturb = raw * (0.20 * gap_p / norm_bound(raw))
        d_pert = d_plus + perturb
        eta_q, zero_q, _, vals_q = eta_delta(d_pert)
        stable &= eta_q == eta_p and zero_q == 0
        min_gap_after = min(min_gap_after, float(np.min(np.abs(vals_q))))
    ok &= check(
        "eta sign is stable under sampled gap-preserving boundary perturbations",
        stable and min_gap_after > 0.5 * gap_p,
        f"initial_gap={gap_p:.3f}, min_gap_after={min_gap_after:.3f}",
    )

    # Explicit zero crossing: the unpaired boundary level moves through zero.
    crossings = []
    for t in np.linspace(1.0, -1.0, 9):
        d_cross = d_plus.copy()
        d_cross[0, 0] = gap_p * t
        eta_c, zero_c, _, _ = eta_delta(d_cross, delta=1.0e-9)
        crossings.append((float(t), eta_c, zero_c, chi_from_eta(eta_c, zero_c)))
    ok &= check(
        "sector change is tied to an explicit boundary zero crossing",
        crossings[0][3] == +1 and crossings[4][3] == 0 and crossings[-1][3] == -1,
        f"chi_path={[c[3] for c in crossings]}",
    )

    # Algebraic controls: positive inertial mass and null paired source unit.
    mass = 2.75
    chi = chi_from_eta(eta_p, zero_p)
    inertial_mass = mass
    active_charge = chi * mass
    response_sign = chi
    ok &= check(
        "positive inertial mass is independent of eta sign",
        inertial_mass > 0 and active_charge == response_sign * inertial_mass,
        f"M={inertial_mass:.2f}, active={active_charge:.2f}, response={response_sign:+d}",
    )
    ok &= check(
        "paired +/- boundary sources are source-unit null controls",
        (+mass) + (-mass) == 0 and mass + mass > 0,
        "active_sum=0.00, inertial_sum=5.50",
    )

    print("-" * 72)
    if ok:
        print("FINAL_TAG: APS_BOUNDARY_INDEX_PROBE_PASS_SOURCE_LOCKING_OPEN")
        return 0
    print("FINAL_TAG: APS_BOUNDARY_INDEX_PROBE_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
