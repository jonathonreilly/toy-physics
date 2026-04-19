#!/usr/bin/env python3
"""
Bounded CP-area deformation scan around the current minimal Schur-NNI quark solve.

Goal:
  Start from the current minimal magnitude solve on the Schur-NNI surface,
  then test the smallest bounded CP-sector deformations that can lift the
  Jarlskog invariant to the atlas value while keeping CKM magnitudes near
  their atlas targets.

Families scanned here:
  1. independent up/down 1-3 phases only
  2. common c13 enhancement + independent phases
  3. split up/down c13 enhancements + independent phases
  4. split c13 enhancements + independent phases + mild 12/23 rescalings

The up-sector mass ratios are allowed to re-fit inside a local nuisance
window around the current minimal solution, but those re-fits are not counted
as deformation cost.  The deformation score counts only:
  - phase shifts away from delta_std
  - multiplicative c13 enhancement factors in each sector that actually moves
  - multiplicative 12/23 coefficient rescalings

Units of the deformation score:
  - 10 degrees of phase shift = 1 unit
  - 10 percent multiplicative change = 1 unit
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import differential_evolution, minimize

from frontier_quark_mass_ratio_full_solve import (
    C12_D,
    C12_U,
    C23_D,
    C23_U,
    DELTA_STD,
    J_ATLAS,
    MAG_TOLS,
    R_DB,
    R_SB,
    V_CB_ATLAS,
    V_UB_ATLAS,
    V_US_ATLAS,
    build_nni_complex,
    diag_hermitian,
    solve_magnitude_surface,
)


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


IDX_R_UC = 0
IDX_R_CT = 1
IDX_DELTA_U = 2
IDX_DELTA_D = 3
IDX_ETA_U = 4
IDX_ETA_D = 5
IDX_K12_U = 6
IDX_K23_U = 7
IDX_K12_D = 8
IDX_K23_D = 9

PARAM_NAMES = (
    "r_uc",
    "r_ct",
    "delta_u",
    "delta_d",
    "eta_u",
    "eta_d",
    "k12_u",
    "k23_u",
    "k12_d",
    "k23_d",
)

TARGET_MAGS = np.array([V_US_ATLAS, V_CB_ATLAS, V_UB_ATLAS], dtype=float)

PHASE_UNIT_DEG = 10.0
PHASE_UNIT_RAD = math.radians(PHASE_UNIT_DEG)
PHASE_WINDOW_DEG = 45.0
PHASE_WINDOW_RAD = math.radians(PHASE_WINDOW_DEG)
MULT_UNIT = math.log(1.10)

R_UC_WINDOW = (0.5, 2.0)
R_CT_WINDOW = (0.5, 2.0)
C13_WINDOW = (1.0, 8.0)
COEFF_WINDOW = (0.85, 1.15)

GLOBAL_MAXITER = 55
GLOBAL_POPSIZE = 16
LOCAL_RANDOM_SEEDS = 40
LOCAL_JITTER_SEEDS = 12
PENALTY_WEIGHT = 1.0e6


@dataclass(frozen=True)
class Family:
    name: str
    description: str
    active_indices: tuple[int, ...]
    score_indices: tuple[int, ...]
    common_c13: bool = False
    seed: int = 0


@dataclass(frozen=True)
class Candidate:
    family: Family
    vector: np.ndarray
    observables: np.ndarray
    deformation_score: float
    penalty: float
    mag_overflow: np.ndarray
    j_shortfall: float
    feasible: bool


FAMILIES = (
    Family(
        "phase_only",
        "independent up/down 1-3 phases",
        (IDX_R_UC, IDX_R_CT, IDX_DELTA_U, IDX_DELTA_D),
        (IDX_DELTA_U, IDX_DELTA_D),
        seed=11,
    ),
    Family(
        "common_c13",
        "common c13 enhancement + independent up/down 1-3 phases",
        (IDX_R_UC, IDX_R_CT, IDX_DELTA_U, IDX_DELTA_D, IDX_ETA_U),
        (IDX_DELTA_U, IDX_DELTA_D, IDX_ETA_U, IDX_ETA_D),
        common_c13=True,
        seed=17,
    ),
    Family(
        "split_c13",
        "separate up/down c13 enhancements + independent 1-3 phases",
        (IDX_R_UC, IDX_R_CT, IDX_DELTA_U, IDX_DELTA_D, IDX_ETA_U, IDX_ETA_D),
        (IDX_DELTA_U, IDX_DELTA_D, IDX_ETA_U, IDX_ETA_D),
        seed=23,
    ),
    Family(
        "split_c13_mild_1223",
        "split c13 enhancements + independent phases + mild 12/23 rescalings",
        (
            IDX_R_UC,
            IDX_R_CT,
            IDX_DELTA_U,
            IDX_DELTA_D,
            IDX_ETA_U,
            IDX_ETA_D,
            IDX_K12_U,
            IDX_K23_U,
            IDX_K12_D,
            IDX_K23_D,
        ),
        (
            IDX_DELTA_U,
            IDX_DELTA_D,
            IDX_ETA_U,
            IDX_ETA_D,
            IDX_K12_U,
            IDX_K23_U,
            IDX_K12_D,
            IDX_K23_D,
        ),
        seed=29,
    ),
)


def wrap_to_pi(angle: float) -> float:
    return ((angle + math.pi) % (2.0 * math.pi)) - math.pi


def phase_shift(angle: float) -> float:
    return wrap_to_pi(angle - DELTA_STD)


def base_vector() -> np.ndarray:
    base = solve_magnitude_surface()
    vector = np.array(
        [
            base.r_uc,
            base.r_ct,
            DELTA_STD,
            DELTA_STD,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ],
        dtype=float,
    )
    return vector


def bounds_for_index(index: int, anchor: np.ndarray) -> tuple[float, float]:
    if index == IDX_R_UC:
        return (R_UC_WINDOW[0] * anchor[IDX_R_UC], R_UC_WINDOW[1] * anchor[IDX_R_UC])
    if index == IDX_R_CT:
        return (R_CT_WINDOW[0] * anchor[IDX_R_CT], R_CT_WINDOW[1] * anchor[IDX_R_CT])
    if index in (IDX_DELTA_U, IDX_DELTA_D):
        return (DELTA_STD - PHASE_WINDOW_RAD, DELTA_STD + PHASE_WINDOW_RAD)
    if index in (IDX_ETA_U, IDX_ETA_D):
        return C13_WINDOW
    return COEFF_WINDOW


def family_bounds(family: Family, anchor: np.ndarray) -> list[tuple[float, float]]:
    return [bounds_for_index(index, anchor) for index in family.active_indices]


def expand_active_vector(active: np.ndarray, family: Family, anchor: np.ndarray) -> np.ndarray:
    full = anchor.copy()
    full[list(family.active_indices)] = active
    if family.common_c13:
        full[IDX_ETA_D] = full[IDX_ETA_U]
    return full


def compute_deformed_observables(vector: np.ndarray) -> np.ndarray:
    r_uc = float(vector[IDX_R_UC])
    r_ct = float(vector[IDX_R_CT])
    if r_uc <= 0.0 or r_ct <= 0.0 or r_uc * r_ct >= 1.0:
        return np.array([math.nan, math.nan, math.nan, math.nan], dtype=float)

    m_u = r_uc * r_ct
    m_c = r_ct
    m_t = 1.0

    m_d = R_DB
    m_s = R_SB
    m_b = 1.0

    c12_u = C12_U * float(vector[IDX_K12_U])
    c23_u = C23_U * float(vector[IDX_K23_U])
    c12_d = C12_D * float(vector[IDX_K12_D])
    c23_d = C23_D * float(vector[IDX_K23_D])

    c13_u = float(vector[IDX_ETA_U]) * c12_u * c23_u * math.sqrt(m_u / m_t)
    c13_d = float(vector[IDX_ETA_D]) * c12_d * c23_d * math.sqrt(m_d / m_b)

    m_u_matrix = build_nni_complex(
        m_u,
        m_c,
        m_t,
        c12_u,
        c23_u,
        c13_u,
        float(vector[IDX_DELTA_U]),
    )
    m_d_matrix = build_nni_complex(
        m_d,
        m_s,
        m_b,
        c12_d,
        c23_d,
        c13_d,
        float(vector[IDX_DELTA_D]),
    )

    _, u_u = diag_hermitian(m_u_matrix)
    _, u_d = diag_hermitian(m_d_matrix)
    v = u_u.conj().T @ u_d

    vus = abs(v[0, 1])
    vcb = abs(v[1, 2])
    vub = abs(v[0, 2])
    jarlskog = abs(np.imag(v[0, 1] * v[1, 2] * np.conj(v[0, 2]) * np.conj(v[1, 1])))
    return np.array([vus, vcb, vub, jarlskog], dtype=float)


def deformation_score(vector: np.ndarray, family: Family) -> float:
    terms: list[float] = []
    for index in family.score_indices:
        if index in (IDX_DELTA_U, IDX_DELTA_D):
            terms.append((phase_shift(float(vector[index])) / PHASE_UNIT_RAD) ** 2)
        else:
            terms.append((math.log(float(vector[index])) / MULT_UNIT) ** 2)
    return math.sqrt(sum(terms)) if terms else 0.0


def constraint_metrics(observables: np.ndarray) -> tuple[np.ndarray, float, float, bool]:
    mag_overflow = np.maximum(np.abs(observables[:3] - TARGET_MAGS) - MAG_TOLS, 0.0) / MAG_TOLS
    j_shortfall = max((J_ATLAS - observables[3]) / J_ATLAS, 0.0)
    penalty = float(np.sum(mag_overflow**2) + j_shortfall**2)
    feasible = bool(np.all(mag_overflow <= 0.0) and j_shortfall <= 0.0)
    return mag_overflow, j_shortfall, penalty, feasible


def evaluate_active_vector(active: np.ndarray, family: Family, anchor: np.ndarray) -> Candidate:
    full = expand_active_vector(active, family, anchor)
    observables = compute_deformed_observables(full)
    mag_overflow, j_shortfall, penalty, feasible = constraint_metrics(observables)
    return Candidate(
        family=family,
        vector=full,
        observables=observables,
        deformation_score=deformation_score(full, family),
        penalty=penalty,
        mag_overflow=mag_overflow,
        j_shortfall=j_shortfall,
        feasible=feasible,
    )


def family_objective(active: np.ndarray, family: Family, anchor: np.ndarray) -> float:
    candidate = evaluate_active_vector(active, family, anchor)
    return PENALTY_WEIGHT * candidate.penalty + candidate.deformation_score


def random_seed(bounds: list[tuple[float, float]], active_indices: tuple[int, ...], rng: np.random.Generator) -> np.ndarray:
    values: list[float] = []
    for index, (lo, hi) in zip(active_indices, bounds):
        if index in (IDX_DELTA_U, IDX_DELTA_D):
            values.append(float(rng.uniform(lo, hi)))
        else:
            values.append(float(math.exp(rng.uniform(math.log(lo), math.log(hi)))))
    return np.array(values, dtype=float)


def clipped_jitter(seed: np.ndarray, bounds: list[tuple[float, float]], active_indices: tuple[int, ...], rng: np.random.Generator) -> np.ndarray:
    jittered = seed.copy()
    for i, (index, (lo, hi)) in enumerate(zip(active_indices, bounds)):
        if index in (IDX_DELTA_U, IDX_DELTA_D):
            step = 0.10 * (hi - lo)
            jittered[i] = float(np.clip(jittered[i] + rng.normal(scale=step), lo, hi))
        else:
            log_lo = math.log(lo)
            log_hi = math.log(hi)
            log_value = math.log(jittered[i])
            step = 0.12 * (log_hi - log_lo)
            jittered[i] = float(math.exp(np.clip(log_value + rng.normal(scale=step), log_lo, log_hi)))
    return jittered


def better_candidate(left: Candidate | None, right: Candidate | None) -> Candidate | None:
    if left is None:
        return right
    if right is None:
        return left
    if left.feasible and right.feasible:
        return right if right.deformation_score < left.deformation_score else left
    if left.feasible != right.feasible:
        return right if right.feasible else left
    left_key = (left.penalty, left.deformation_score)
    right_key = (right.penalty, right.deformation_score)
    return right if right_key < left_key else left


def local_seed_bank(family: Family, anchor: np.ndarray, de_seed: np.ndarray) -> list[np.ndarray]:
    bounds = family_bounds(family, anchor)
    rng = np.random.default_rng(1000 + family.seed)
    seeds: list[np.ndarray] = [anchor[list(family.active_indices)].copy(), de_seed.copy()]

    for _ in range(LOCAL_JITTER_SEEDS):
        seeds.append(clipped_jitter(de_seed, bounds, family.active_indices, rng))
    for _ in range(LOCAL_RANDOM_SEEDS):
        seeds.append(random_seed(bounds, family.active_indices, rng))
    return seeds


def solve_family(family: Family, anchor: np.ndarray) -> Candidate:
    bounds = family_bounds(family, anchor)
    objective = lambda active: family_objective(active, family, anchor)

    global_result = differential_evolution(
        objective,
        bounds,
        seed=family.seed,
        maxiter=GLOBAL_MAXITER,
        popsize=GLOBAL_POPSIZE,
        polish=False,
        tol=1.0e-3,
        updating="deferred",
        workers=1,
    )

    best_feasible: Candidate | None = None
    best_any: Candidate | None = evaluate_active_vector(global_result.x, family, anchor)

    for seed in local_seed_bank(family, anchor, global_result.x):
        result = minimize(
            objective,
            seed,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 800},
        )
        candidate = evaluate_active_vector(result.x, family, anchor)
        best_any = better_candidate(best_any, candidate)
        if candidate.feasible:
            best_feasible = better_candidate(best_feasible, candidate)

    return best_feasible if best_feasible is not None else best_any


def format_delta(value: float) -> str:
    return f"{value:+.4e}"


def print_anchor(anchor: np.ndarray) -> None:
    observables = compute_deformed_observables(anchor)
    print("\n" + "=" * 72)
    print("PART 1: Local Minimal-Solve Anchor")
    print("=" * 72)

    print(f"\n  anchored m_u/m_c      = {anchor[IDX_R_UC]:.6e}")
    print(f"  anchored m_c/m_t      = {anchor[IDX_R_CT]:.6e}")
    print(f"  anchored |V_us|       = {observables[0]:.6f}")
    print(f"  anchored |V_cb|       = {observables[1]:.6f}")
    print(f"  anchored |V_ub|       = {observables[2]:.6f}")
    print(f"  anchored J            = {observables[3]:.6e}")
    print(f"  anchored J/J_atlas    = {observables[3] / J_ATLAS:.6f}")
    print()
    print("  Nuisance re-fit window (not counted as deformation):")
    print(f"    m_u/m_c in [{R_UC_WINDOW[0]:.2f}, {R_UC_WINDOW[1]:.2f}] x anchor")
    print(f"    m_c/m_t in [{R_CT_WINDOW[0]:.2f}, {R_CT_WINDOW[1]:.2f}] x anchor")
    print()
    print("  Deformation score units:")
    print(f"    {PHASE_UNIT_DEG:.0f} deg phase shift = 1 unit")
    print("    10% multiplicative change = 1 unit")
    print(f"    phase scan bounded to delta_std +/- {PHASE_WINDOW_DEG:.0f} deg")
    print()
    print("  CKM corridor (same as the current phase-relaxed scan):")
    print(f"    |V_us - target| <= {MAG_TOLS[0]:.4f}")
    print(f"    |V_cb - target| <= {MAG_TOLS[1]:.4f}")
    print(f"    |V_ub - target| <= {MAG_TOLS[2]:.4f}")


def print_family_table(results: list[Candidate]) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Family Scan")
    print("=" * 72)
    print()
    header = f"{'family':<22} {'status':<11} {'score':>8} {'J/J_atlas':>10} {'dV_us':>11} {'dV_cb':>11} {'dV_ub':>11}"
    print(header)
    print("-" * len(header))
    for candidate in results:
        dv = candidate.observables[:3] - TARGET_MAGS
        status = "feasible" if candidate.feasible else "nearby"
        print(
            f"{candidate.family.name:<22} "
            f"{status:<11} "
            f"{candidate.deformation_score:>8.3f} "
            f"{candidate.observables[3] / J_ATLAS:>10.6f} "
            f"{format_delta(float(dv[0])):>11} "
            f"{format_delta(float(dv[1])):>11} "
            f"{format_delta(float(dv[2])):>11}"
        )


def print_best_candidate(candidate: Candidate) -> None:
    vector = candidate.vector
    observables = candidate.observables
    dv = observables[:3] - TARGET_MAGS

    print("\n" + "=" * 72)
    print("PART 3: Best Candidate")
    print("=" * 72)

    print(f"\n  family                = {candidate.family.name}")
    print(f"  description           = {candidate.family.description}")
    print(f"  feasible              = {candidate.feasible}")
    print(f"  deformation score     = {candidate.deformation_score:.6f}")
    print(f"  m_u/m_c               = {vector[IDX_R_UC]:.6e}")
    print(f"  m_c/m_t               = {vector[IDX_R_CT]:.6e}")
    print(f"  delta_u               = {math.degrees(vector[IDX_DELTA_U]):.3f} deg")
    print(f"    shift from delta_std = {math.degrees(phase_shift(vector[IDX_DELTA_U])):+.3f} deg")
    print(f"  delta_d               = {math.degrees(vector[IDX_DELTA_D]):.3f} deg")
    print(f"    shift from delta_std = {math.degrees(phase_shift(vector[IDX_DELTA_D])):+.3f} deg")
    print(f"  eta_u                 = {vector[IDX_ETA_U]:.6f}")
    print(f"  eta_d                 = {vector[IDX_ETA_D]:.6f}")
    print(f"  k12_u                 = {vector[IDX_K12_U]:.6f}")
    print(f"  k23_u                 = {vector[IDX_K23_U]:.6f}")
    print(f"  k12_d                 = {vector[IDX_K12_D]:.6f}")
    print(f"  k23_d                 = {vector[IDX_K23_D]:.6f}")
    print()
    print(f"  |V_us|                = {observables[0]:.6f}  (d = {dv[0]:+.4e})")
    print(f"  |V_cb|                = {observables[1]:.6f}  (d = {dv[1]:+.4e})")
    print(f"  |V_ub|                = {observables[2]:.6f}  (d = {dv[2]:+.4e})")
    print(f"  J                     = {observables[3]:.6e}")
    print(f"  J / J_atlas           = {observables[3] / J_ATLAS:.6f}")


def select_best_result(results: list[Candidate]) -> Candidate:
    best: Candidate | None = None
    for candidate in results:
        best = better_candidate(best, candidate)
    assert best is not None
    return best


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Bounded Quark Jarlskog Closure Scan")
    print("=" * 72)

    anchor = base_vector()
    print_anchor(anchor)

    results = [solve_family(family, anchor) for family in FAMILIES]
    print_family_table(results)

    best = select_best_result(results)
    print_best_candidate(best)

    phase_only = next(candidate for candidate in results if candidate.family.name == "phase_only")
    split_c13 = next(candidate for candidate in results if candidate.family.name == "split_c13")

    print("\n" + "=" * 72)
    print("PART 4: Scan Checks")
    print("=" * 72)

    check(
        "The anchored minimal solve still sits well below the atlas J",
        compute_deformed_observables(anchor)[3] / J_ATLAS < 0.25,
        f"J_anchor/J_atlas = {compute_deformed_observables(anchor)[3] / J_ATLAS:.4f}",
    )
    check(
        "Phase-only local deformations do not close the atlas J",
        not phase_only.feasible and phase_only.observables[3] / J_ATLAS < 0.25,
        f"phase-only J/J_atlas = {phase_only.observables[3] / J_ATLAS:.4f}",
    )
    check(
        "At least one c13-enhanced family reaches the atlas J inside the corridor",
        any(candidate.feasible for candidate in results if "c13" in candidate.family.name),
        ", ".join(
            f"{candidate.family.name}:{'yes' if candidate.feasible else 'no'}"
            for candidate in results
            if "c13" in candidate.family.name
        ),
    )
    check(
        "The best candidate found uses split c13 deformations rather than phase-only motion",
        best.family.name in {"split_c13", "split_c13_mild_1223"},
        f"best family = {best.family.name}",
    )
    check(
        "The split-c13 family closes the atlas J in the bounded local window",
        split_c13.feasible,
        f"J/J_atlas = {split_c13.observables[3] / J_ATLAS:.6f}",
    )

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
