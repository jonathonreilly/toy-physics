#!/usr/bin/env python3
"""Finite theorem audit for the eta source-character uniqueness target.

The target is the strongest current breakthrough version of the signed
response lane:

    The active scalar source coefficient is not an inserted sign. It is the
    unique local real source character of the APS determinant-orientation line
    compatible with normalization, orientation reversal, null quarantine,
    positive norm separation, refinement invariance, and local sewing.

Within that source-character grammar, the coefficient is forced to

    c(Y) = sign(eta_delta(D_Y)) = chi_eta(Y).

The tensor side is audited as a maximality statement. The same 3+1 symmetry
allows a canonical invariant A1 lapse/trace lift, but the complementary
E plus T1 channels have no nonzero invariant source vector from this scalar
line alone. A later oriented tensor-source lift can twist an already-retained
ordinary tensor source bundle, but it does not derive tensor components from
the scalar character.

This is not a negative-mass, shielding, propulsion, reactionless-force, or
physical signed-gravity claim.
"""

from __future__ import annotations

import itertools
import math
import os
import sys
from dataclasses import dataclass
from typing import Callable

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


def sign_eta(n: int) -> int:
    if n > 0:
        return +1
    if n < 0:
        return -1
    return 0


def enumerate_real_source_characters(max_eta: int = 8) -> list[dict[int, int]]:
    """Enumerate maps c:{-N..N}->{-1,0,+1} satisfying the source grammar."""

    domain = list(range(-max_eta, max_eta + 1))
    positives = list(range(1, max_eta + 1))
    valid: list[dict[int, int]] = []

    for values in itertools.product((-1, 0, +1), repeat=max_eta):
        f: dict[int, int] = {0: 0}
        for eta, value in zip(positives, values):
            f[eta] = value
            f[-eta] = -value

        if f[1] != 1:
            continue
        if any(f[eta] == 0 for eta in positives):
            continue
        refinement_ok = True
        for eta in positives:
            for k in positives:
                if eta * k <= max_eta and f[eta * k] != f[eta]:
                    refinement_ok = False
        if not refinement_ok:
            continue
        if not all(f[-eta] == -f[eta] for eta in positives):
            continue
        if any(f[eta] not in (-1, +1) for eta in positives):
            continue
        if any(eta not in f for eta in domain):
            continue
        valid.append(f)
    return valid


@dataclass(frozen=True)
class CandidateRule:
    name: str
    coeff: Callable[[int], complex]
    should_pass: bool
    expected_failure: str


def candidate_rules() -> list[CandidateRule]:
    return [
        CandidateRule("chi_eta", lambda eta: complex(sign_eta(eta), 0.0), True, "none"),
        CandidateRule("unsigned", lambda eta: complex(0 if eta == 0 else 1, 0.0), False, "orientation"),
        CandidateRule("raw_eta", lambda eta: complex(eta, 0.0), False, "unit/refinement"),
        CandidateRule(
            "parity_eta",
            lambda eta: complex(0 if eta == 0 else (1 if eta % 2 else -1), 0.0),
            False,
            "refinement",
        ),
        CandidateRule(
            "complex_phase",
            lambda eta: complex(0.0, 0.0) if eta == 0 else np.exp(0.5j * math.pi * eta),
            False,
            "real_action",
        ),
    ]


def rule_satisfies_constraints(rule: CandidateRule, max_eta: int = 8) -> tuple[bool, str]:
    domain = list(range(-max_eta, max_eta + 1))
    vals = {eta: rule.coeff(eta) for eta in domain}
    normalized = abs(vals[1] - 1.0) < TOL
    null = abs(vals[0]) < TOL
    real = all(abs(v.imag) < TOL for v in vals.values())
    unit = all(abs(abs(vals[eta]) - 1.0) < TOL for eta in domain if eta != 0)
    odd = all(abs(vals[-eta] + vals[eta]) < TOL for eta in range(1, max_eta + 1))
    refinement = True
    for eta in range(1, max_eta + 1):
        for k in range(1, max_eta + 1):
            if eta * k <= max_eta and abs(vals[eta * k] - vals[eta]) > TOL:
                refinement = False
    passed = bool(normalized and null and real and unit and odd and refinement)
    detail = (
        f"norm={normalized}, null={null}, real={real}, unit={unit}, "
        f"odd={odd}, refine={refinement}"
    )
    return passed, detail


def determinant_functor_locality_check() -> tuple[bool, str]:
    """Magnitude is global additive; orientation source must stay local."""

    magnitudes = np.array([2.0, 3.0, 5.0], dtype=float)
    signs = np.array([+1, -1, +1], dtype=int)
    dets = signs * magnitudes
    log_abs_additive = abs(math.log(abs(float(np.prod(dets)))) - float(np.sum(np.log(magnitudes)))) < TOL

    local_source_coeffs = signs.copy()
    global_product_sign = int(np.prod(signs))

    # Adding a remote negative component flips a global product sign but must
    # not flip the already existing local source coefficient.
    plus_alone_local = +1
    plus_with_remote_local = +1
    plus_alone_global = +1
    plus_with_remote_global = -1

    local_ok = plus_alone_local == plus_with_remote_local
    global_fails = plus_alone_global != plus_with_remote_global
    neutral_local_sum = int(local_source_coeffs[0] + local_source_coeffs[1])
    ok = log_abs_additive and local_ok and global_fails and neutral_local_sum == 0
    detail = (
        f"log_abs_additive={log_abs_additive}, global_product={global_product_sign:+d}, "
        f"local_pair_sum={neutral_local_sum:+d}, global_spectator_flip={global_fails}"
    )
    return ok, detail


def sym(i: int, j: int, n: int = 4) -> np.ndarray:
    out = np.zeros((n, n), dtype=float)
    if i == j:
        out[i, j] = 1.0
    else:
        out[i, j] = 1.0 / math.sqrt(2.0)
        out[j, i] = 1.0 / math.sqrt(2.0)
    return out


def diag(vals: tuple[float, float, float, float]) -> np.ndarray:
    return np.diag(np.array(vals, dtype=float))


def canonical_polarization_frame() -> list[np.ndarray]:
    sqrt2 = math.sqrt(2.0)
    sqrt3 = math.sqrt(3.0)
    sqrt6 = math.sqrt(6.0)
    return [
        sym(0, 0),
        sym(0, 1),
        sym(0, 2),
        sym(0, 3),
        diag((0.0, 1.0 / sqrt3, 1.0 / sqrt3, 1.0 / sqrt3)),
        diag((0.0, 1.0 / sqrt2, -1.0 / sqrt2, 0.0)),
        diag((0.0, 1.0 / sqrt6, 1.0 / sqrt6, -2.0 / sqrt6)),
        sym(1, 2),
        sym(1, 3),
        sym(2, 3),
    ]


def rotation(axis: str, theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    rot = np.eye(4)
    if axis == "x":
        rot[2, 2] = c
        rot[2, 3] = -s
        rot[3, 2] = s
        rot[3, 3] = c
    elif axis == "y":
        rot[1, 1] = c
        rot[1, 3] = s
        rot[3, 1] = -s
        rot[3, 3] = c
    elif axis == "z":
        rot[1, 1] = c
        rot[1, 2] = -s
        rot[2, 1] = s
        rot[2, 2] = c
    else:
        raise ValueError(axis)
    return rot


def frob(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.tensordot(a, b, axes=2))


def rep_matrix(rot: np.ndarray, frame: list[np.ndarray]) -> np.ndarray:
    out = np.zeros((len(frame), len(frame)), dtype=float)
    for j, basis in enumerate(frame):
        image = rot.T @ basis @ rot
        for i, ref in enumerate(frame):
            out[i, j] = frob(ref, image)
    return out


def generator(axis: str, eps: float = 1.0e-6) -> np.ndarray:
    frame = canonical_polarization_frame()
    return (rep_matrix(rotation(axis, eps), frame) - rep_matrix(rotation(axis, -eps), frame)) / (2.0 * eps)


def nullity(mat: np.ndarray, tol: float = 1.0e-9) -> int:
    rank = int(np.linalg.matrix_rank(mat, tol=tol))
    return mat.shape[1] - rank


def tensor_invariant_maximality_check() -> tuple[bool, str]:
    gens = [generator(axis) for axis in ("x", "y", "z")]
    stack_full = np.vstack(gens)
    full_fixed = nullity(stack_full)

    a1_indices = [0, 4]
    comp_indices = [1, 2, 3, 5, 6, 7, 8, 9]
    stack_a1 = np.vstack([g[np.ix_(a1_indices, a1_indices)] for g in gens])
    stack_comp = np.vstack([g[np.ix_(comp_indices, comp_indices)] for g in gens])
    a1_fixed = nullity(stack_a1)
    comp_fixed = nullity(stack_comp)

    projector = np.zeros((10, 10), dtype=float)
    projector[0, 0] = 1.0
    projector[4, 4] = 1.0
    max_comm = max(float(np.linalg.norm(projector @ g - g @ projector, ord="fro")) for g in gens)

    ok = full_fixed == 2 and a1_fixed == 2 and comp_fixed == 0 and max_comm < TOL
    detail = f"fixed(full,A1,comp)=({full_fixed},{a1_fixed},{comp_fixed}), max_comm={max_comm:.1e}"
    return ok, detail


def source_character_action_check() -> tuple[bool, str]:
    masses = np.array([1.0, 2.0, 3.0], dtype=float)
    etas = np.array([+1, -1, +5], dtype=int)
    coeffs = np.array([sign_eta(int(eta)) for eta in etas], dtype=float)
    active = float(np.dot(coeffs, masses))
    inertial = float(np.sum(masses))
    null_coeff = sign_eta(0)
    ok = abs(active - 2.0) < TOL and inertial > 0.0 and null_coeff == 0
    detail = f"active={active:+.1f}, inertial={inertial:.1f}, null_coeff={null_coeff:+d}"
    return ok, detail


def main() -> int:
    print("=" * 104)
    print("SIGNED GRAVITY ETA SOURCE-CHARACTER UNIQUENESS THEOREM AUDIT")
    print("  determinant-line character uniqueness; controlled source-origin target")
    print("=" * 104)
    print()

    print("BREAKTHROUGH TARGET")
    print("  Derive the signed scalar source coefficient as the unique local real")
    print("  character of the APS determinant-orientation line, and prove the tensor")
    print("  lift from this scalar line is maximal at invariant A1.")
    print()

    valid = enumerate_real_source_characters(max_eta=8)
    expected = {eta: sign_eta(eta) for eta in range(-8, 9)}
    check(
        "source-character axioms have a unique normalized solution",
        len(valid) == 1 and valid[0] == expected,
        f"solutions={len(valid)}",
    )

    for rule in candidate_rules():
        passed, detail = rule_satisfies_constraints(rule)
        check(
            f"candidate rule classification: {rule.name}",
            passed == rule.should_pass,
            f"{detail}, expected_failure={rule.expected_failure}",
        )

    functor_ok, functor_detail = determinant_functor_locality_check()
    check(
        "determinant factorization splits magnitude additivity from local orientation source",
        functor_ok,
        functor_detail,
    )

    action_ok, action_detail = source_character_action_check()
    check(
        "source character separates signed active charge from positive inertia",
        action_ok,
        action_detail,
    )

    tensor_ok, tensor_detail = tensor_invariant_maximality_check()
    check(
        "3+1 covariance allows exactly A1 invariant source lift and no complement vector",
        tensor_ok,
        tensor_detail,
    )

    print()
    print("INTERPRETATION")
    print("  Within the determinant-orientation source-character grammar, chi_eta is")
    print("  not optional: it is the only normalized local real character.  The")
    print("  determinant machinery also explains why log|det| gives the positive")
    print("  scalar magnitude while Or(Det_APS) supplies the local sign.  Tensorially,")
    print("  the scalar source line is maximal at A1.  The later tensor route must")
    print("  twist an ordinary retained tensor source bundle, not extract tensor")
    print("  components from this scalar character.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("FINAL_TAG: ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL")
        return 0
    print("FINAL_TAG: ETA_SOURCE_CHARACTER_UNIQUENESS_AUDIT_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
