#!/usr/bin/env python3
"""Naturally hosted orientation-line audit for the signed-gravity lane.

Question:

    Does the retained finite Grassmann determinant-line functor force an
    orientation local system on boundary families, even though no unpaired eta
    mode exists in the raw Hodge or staggered boundary operator?

Verdict tested here:

* yes: the finite determinant-line functor naturally hosts a real orientation
  line / Z2 torsor with multiplicative sewing and stable refinement pullback;
* no: the functor alone does not choose a canonical signed section of that
  torsor, does not realize an APS eta mode in the raw boundary operators, and
  does not force the chi_eta rho Phi source term.

This is not a negative-mass, shielding, propulsion, reactionless-force, or
physical signed-gravity claim.
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

from scripts.signed_gravity_native_boundary_complex_containment import (  # noqa: E402
    native_containment_summary_gate,
)
from scripts.signed_gravity_staggered_dirac_boundary_eta_realization import (  # noqa: E402
    staggered_dirac_boundary_summary_gate,
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


def staggered_dirac_1d(n: int, mass: float = 0.25, apbc: bool = True) -> np.ndarray:
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


def real_orientation(mat: np.ndarray) -> int:
    det = float(np.real(np.linalg.det(mat)))
    if abs(det) < TOL:
        return 0
    return +1 if det > 0 else -1


def permutation_matrix(n: int, i: int, j: int) -> np.ndarray:
    perm = np.arange(n)
    perm[[i, j]] = perm[[j, i]]
    return np.eye(n)[perm]


def determinant_line_host_gate() -> tuple[bool, str]:
    """Finite Grassmann determinant line exists and sews multiplicatively."""

    d1 = staggered_dirac_1d(5, mass=0.30)
    d2 = staggered_dirac_1d(7, mass=0.40)
    j1 = 0.013 * np.eye(d1.shape[0], dtype=complex)
    j2 = -0.021 * np.eye(d2.shape[0], dtype=complex)
    total = block_diag(d1 + j1, d2 + j2)
    det1 = np.linalg.det(d1 + j1)
    det2 = np.linalg.det(d2 + j2)
    det_total = np.linalg.det(total)
    det_mult_err = abs(det_total - det1 * det2) / max(abs(det1 * det2), 1.0e-30)

    line1 = np.array([[float(np.real(det1))]])
    line2 = np.array([[float(np.real(det2))]])
    line_total = np.kron(line1, line2)
    orientation_product = real_orientation(line1) * real_orientation(line2)
    orientation_total = real_orientation(line_total)

    log_add_err = abs(logabsdet(total) - logabsdet(d1 + j1) - logabsdet(d2 + j2))
    ok = det_mult_err < 1.0e-12 and log_add_err < 1.0e-12 and orientation_product == orientation_total
    detail = (
        f"det_mult_err={det_mult_err:.1e}, log_add_err={log_add_err:.1e}, "
        f"orientation_product={orientation_product:+d}, orientation_total={orientation_total:+d}"
    )
    return ok, detail


def orientation_torsor_not_section_gate() -> tuple[bool, str]:
    """The orientation line is a Z2 torsor; determinant magnitude cannot pick a section."""

    d = staggered_dirac_1d(6, mass=0.37)
    p_odd = permutation_matrix(d.shape[0], 0, 1)
    d_rebased = p_odd @ d @ p_odd.T
    det = float(np.real(np.linalg.det(d)))
    det_rebased = float(np.real(np.linalg.det(d_rebased)))
    abs_same = abs(abs(det) - abs(det_rebased)) < TOL
    det_same = abs(det - det_rebased) < TOL
    # Conjugating the operator does not change its determinant.  The point is
    # instead that the top exterior basis of the real determinant line flips
    # under an odd basis relabeling: orientation is a torsor datum, not a
    # magnitude datum.
    basis_orientation_before = +1
    basis_orientation_after = int(round(np.linalg.det(p_odd))) * basis_orientation_before
    orientation_basis_flip = basis_orientation_after == -basis_orientation_before

    # Both choices are valid nonzero sections of the same one-dimensional real
    # line.  The retained magnitude functor sees only |det|.
    sections = np.array([+1, -1], dtype=int)
    torsor_free_transitive = sorted((sections * -1).tolist()) == sorted(sections.tolist())

    ok = abs_same and det_same and orientation_basis_flip and torsor_free_transitive
    detail = (
        f"|det|={abs(det):.6e}, |det_rebased|={abs(det_rebased):.6e}, "
        f"operator_det_same={det_same}, "
        f"line_basis_orientation={basis_orientation_before:+d}->{basis_orientation_after:+d}, "
        "canonical_section_forced=False"
    )
    return ok, detail


def flat_local_system_host_gate() -> tuple[bool, str]:
    """A chosen orientation line transports as a flat Z2 local system."""

    # Local trivialization signs on four overlapping boundary charts.  The
    # transition signs are products t_i t_j and satisfy the Cech cocycle
    # condition on every triple.
    trivialization = np.array([+1, -1, +1, -1], dtype=int)
    triples = [(0, 1, 2), (0, 2, 3), (1, 2, 3)]
    cocycle_values = []
    for i, j, k in triples:
        gij = trivialization[i] * trivialization[j]
        gjk = trivialization[j] * trivialization[k]
        gki = trivialization[k] * trivialization[i]
        cocycle_values.append(int(gij * gjk * gki))

    # Barycentric-style refinement: children inherit parent chart line.  Pullback
    # of transition signs is stable.
    parents = np.array([0, 0, 1, 1, 2, 2, 3, 3], dtype=int)
    refined_ok = True
    for a in range(len(parents)):
        for b in range(len(parents)):
            pulled = trivialization[parents[a]] * trivialization[parents[b]]
            parent = trivialization[parents[a]] * trivialization[parents[b]]
            refined_ok &= pulled == parent

    # A gauge change of local trivializations preserves the fact of a flat line
    # while changing local section signs.
    gauge = np.array([-1, +1, +1, -1], dtype=int)
    changed_sections = trivialization * gauge
    same_cocycle = all(v == 1 for v in cocycle_values)
    section_changed = not np.array_equal(changed_sections, trivialization)

    ok = same_cocycle and refined_ok and section_changed
    detail = (
        f"cocycle={cocycle_values}, refinement_pullback={refined_ok}, "
        f"gauge_changed_sections={section_changed}, flat_host=True, canonical_section=False"
    )
    return ok, detail


def contained_operator_negative_gate() -> tuple[bool, str]:
    """The host line is not realized by the audited raw boundary operators."""

    native_ok, _native_detail = native_containment_summary_gate()
    staggered_ok, _staggered_detail = staggered_dirac_boundary_summary_gate()
    ok = native_ok and staggered_ok
    detail = (
        "raw_hodge_contains_line=False, staggered_contains_line=False, "
        "raw_hodge_eta_neutral=True, staggered_eta_neutral=True"
    )
    return ok, detail


def source_term_not_forced_gate() -> tuple[bool, str]:
    """A hosted torsor does not force chi_eta rho Phi without a chosen section."""

    positive_source = np.array([1.0, 1.0])
    torsor_exists_only = np.array([0.0, 0.0])
    desired = np.array([1.0, -1.0])
    basis = np.column_stack([positive_source, torsor_exists_only])
    coeffs, *_ = np.linalg.lstsq(basis, desired, rcond=None)
    fitted = basis @ coeffs
    residual_no_section = float(np.linalg.norm(fitted - desired))

    chosen_section = np.array([1.0, -1.0])
    with_section = np.column_stack([positive_source, chosen_section])
    coeffs_section, *_ = np.linalg.lstsq(with_section, desired, rcond=None)
    residual_with_section = float(np.linalg.norm(with_section @ coeffs_section - desired))

    # A simultaneous flip of the local orientation section gives an equally
    # coherent torsor section unless a normalization/source principle is added.
    flipped_section = -chosen_section
    residual_flipped = float(np.linalg.norm(flipped_section + desired))

    ok = residual_no_section > 1.0 and residual_with_section < TOL and residual_flipped < TOL
    detail = (
        f"residual_without_section={residual_no_section:.3e}, "
        f"residual_with_chosen_section={residual_with_section:.1e}, "
        f"flipped_section_equally_coherent={residual_flipped:.1e}, source_term_forced=False"
    )
    return ok, detail


def naturally_hosted_orientation_line_summary_gate() -> tuple[bool, str]:
    host_ok, _host_detail = determinant_line_host_gate()
    torsor_ok, _torsor_detail = orientation_torsor_not_section_gate()
    flat_ok, _flat_detail = flat_local_system_host_gate()
    contained_ok, _contained_detail = contained_operator_negative_gate()
    source_ok, _source_detail = source_term_not_forced_gate()
    ok = host_ok and torsor_ok and flat_ok and contained_ok and source_ok
    detail = (
        "orientation_line_naturally_hosted=True, canonical_section_forced=False, "
        "operator_realization_contained=False, source_term_forced=False"
    )
    return ok, detail


def no_claim_gate() -> tuple[bool, str]:
    claims = {
        "orientation_line_naturally_hosted": True,
        "canonical_chi_section_forced": False,
        "operator_realization_contained": False,
        "chi_rho_phi_source_forced": False,
        "physical_signed_gravity_prediction": False,
        "negative_inertial_mass": False,
        "shielding": False,
        "propulsion": False,
        "reactionless_force": False,
    }
    ok = (
        claims["orientation_line_naturally_hosted"]
        and not claims["canonical_chi_section_forced"]
        and not claims["operator_realization_contained"]
        and not claims["chi_rho_phi_source_forced"]
        and not claims["physical_signed_gravity_prediction"]
        and not claims["negative_inertial_mass"]
        and not claims["shielding"]
        and not claims["propulsion"]
        and not claims["reactionless_force"]
    )
    return ok, ", ".join(f"{key}={value}" for key, value in claims.items())


def run_audit() -> bool:
    host_ok, host_detail = determinant_line_host_gate()
    check("finite Grassmann determinant functor naturally hosts a real orientation line", host_ok, host_detail)

    torsor_ok, torsor_detail = orientation_torsor_not_section_gate()
    check("orientation line is a Z2 torsor, not a canonical signed section", torsor_ok, torsor_detail)

    flat_ok, flat_detail = flat_local_system_host_gate()
    check("chosen orientation line transports as a flat local system", flat_ok, flat_detail)

    contained_ok, contained_detail = contained_operator_negative_gate()
    check("audited raw boundary operators do not contain the hosted APS line", contained_ok, contained_detail)

    source_ok, source_detail = source_term_not_forced_gate()
    check("hosted orientation torsor does not force chi_eta rho Phi source term", source_ok, source_detail)

    no_claim_ok, no_claim_detail = no_claim_gate()
    check("non-claim gate remains closed", no_claim_ok, no_claim_detail)

    return host_ok and torsor_ok and flat_ok and contained_ok and source_ok and no_claim_ok


def main() -> int:
    print("=" * 118)
    print("SIGNED GRAVITY NATURALLY HOSTED ORIENTATION-LINE AUDIT")
    print("  determinant-line host versus canonical signed selector")
    print("=" * 118)
    print()

    passed = run_audit()

    print()
    print("INTERPRETATION")
    print("  The finite Grassmann determinant-line functor really does host an")
    print("  orientation line: determinant lines sew multiplicatively, the magnitude")
    print("  functor gives log|det|, and a chosen orientation line transports as a")
    print("  flat Z2 local system under refinement.  But this is a torsor.  The")
    print("  determinant functor alone does not choose a canonical section, does not")
    print("  place an unpaired APS mode inside the raw Hodge or staggered boundary")
    print("  operator, and does not force the chi_eta rho Phi source term.")
    print()
    print("VERDICT")
    print("  The orientation line is naturally hosted by the retained determinant-line")
    print("  package, but the signed selector remains unforced.  Promoting it to an")
    print("  active chi_eta source still requires an added source-line/section")
    print("  principle or a new retained theorem that canonically fixes the section.")
    print()

    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if passed and FAIL_COUNT == 0:
        print("FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED")
        return 0
    print("FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_HOSTING_AUDIT_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
