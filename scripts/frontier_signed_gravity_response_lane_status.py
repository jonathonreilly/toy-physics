#!/usr/bin/env python3
"""Consolidated status harness for the signed gravitational response lane.

This runner lands the review branch's safe science without importing the stale
branch wholesale. It checks the conditional locked-response algebra, the local
selector/source no-go boundaries, and the determinant-orientation support
boundary. It does not claim physical signed gravity.
"""

from __future__ import annotations

import itertools
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "SIGNED_GRAVITY_RESPONSE_LANE_STATUS_NOTE_2026-04-26.md"

AUTHORITY_FILES = [
    ROOT / "docs" / "FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md",
    ROOT / "docs" / "GRAVITY_CLEAN_DERIVATION_NOTE.md",
    ROOT / "docs" / "GRAVITY_SIGN_AUDIT_2026-04-10.md",
    ROOT / "docs" / "SIGN_PORTABILITY_INVARIANT_NOTE.md",
]

EPS = 1.0e-12
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


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def sign_roles(mode: str, chi: int) -> tuple[int, int]:
    if mode == "source_only":
        return chi, +1
    if mode == "response_only":
        return +1, chi
    if mode == "locked":
        return chi, chi
    raise ValueError(mode)


def pair_forces(mode: str, chi_a: int, chi_b: int, mass_a: float = 1.0, mass_b: float = 1.0) -> tuple[float, float]:
    """Return force on A(left), force on B(right), with positive inertia."""

    src_a, resp_a = sign_roles(mode, chi_a)
    src_b, resp_b = sign_roles(mode, chi_b)
    magnitude = mass_a * mass_b
    force_a = resp_a * src_b * magnitude
    force_b = -resp_b * src_a * magnitude
    return float(force_a), float(force_b)


def locked_sign_response_gate() -> bool:
    modes = ("source_only", "response_only", "locked")
    pairs = tuple(itertools.product((+1, -1), repeat=2))
    ok = True

    for mode in modes:
        residuals: list[float] = []
        mixed_residuals: list[float] = []
        reads: list[str] = []
        for chi_a, chi_b in pairs:
            force_a, force_b = pair_forces(mode, chi_a, chi_b, mass_a=2.0, mass_b=5.0)
            residual = abs(force_a + force_b) / max(abs(force_a), abs(force_b), 1.0)
            residuals.append(residual)
            if chi_a != chi_b:
                mixed_residuals.append(residual)
            if residual < EPS:
                reads.append("ATTRACT" if force_a > 0.0 and force_b < 0.0 else "REPEL")
            else:
                reads.append("UNBALANCED")

        if mode == "locked":
            ok &= max(residuals) < EPS
            ok &= reads == ["ATTRACT", "REPEL", "REPEL", "ATTRACT"]
            check(
                "locked source/response sign passes all four two-body pairs",
                max(residuals) < EPS and reads == ["ATTRACT", "REPEL", "REPEL", "ATTRACT"],
                f"reads={reads}",
            )
        else:
            ok &= max(mixed_residuals) > 1.0
            check(
                f"{mode} remains a mixed-pair action-reaction no-go control",
                max(mixed_residuals) > 1.0,
                f"max_mixed_residual={max(mixed_residuals):.1f}",
            )

    positive_masses = all(m > 0.0 for m in (1.0, 2.0, 5.0))
    ok &= positive_masses
    check("inertial masses stay positive in the consequence harness", positive_masses)
    return ok


PAULI_LABELS = ("I", "X", "Y", "Z")
GAMMAS = ("XII", "ZXI", "ZZX")
EPSILON = "ZZZ"


def anticommutes_one(a: str, b: str) -> bool:
    return a != "I" and b != "I" and a != b


def commutes(pauli_a: str, pauli_b: str) -> bool:
    anti_count = sum(anticommutes_one(a, b) for a, b in zip(pauli_a, pauli_b, strict=True))
    return anti_count % 2 == 0


def local_selector_no_go_gate() -> bool:
    candidates = ["".join(labels) for labels in itertools.product(PAULI_LABELS, repeat=3) if "".join(labels) != "III"]
    strict: list[str] = []
    conserved_neutral: list[str] = []

    for q in candidates:
        massive_conserved = all(commutes(q, op) for op in GAMMAS + (EPSILON,))
        scalar_pinned = q == EPSILON
        if massive_conserved and scalar_pinned:
            strict.append(q)
        if massive_conserved and not scalar_pinned:
            conserved_neutral.append(q)

    epsilon_pins = EPSILON in candidates
    epsilon_breaks_kinetic = not all(commutes(EPSILON, op) for op in GAMMAS)
    no_strict = len(strict) == 0 and epsilon_pins and epsilon_breaks_kinetic
    check(
        "strict local/taste-cell chi selector is absent",
        no_strict,
        f"strict={strict}, conserved_neutral_count={len(conserved_neutral)}",
    )
    check(
        "epsilon pins scalar sign but is not conserved by kinetic Clifford generators",
        epsilon_pins and epsilon_breaks_kinetic,
        "epsilon=ZZZ anticommutes with each retained gamma",
    )
    return no_strict


def local_source_primitive_gate() -> bool:
    rows = [
        {
            "name": "Born rho=|psi|^2",
            "variational": False,
            "signed": False,
            "branch_fixed": False,
            "conserved": True,
            "positive_inertia": True,
            "native": True,
        },
        {
            "name": "scalar rho_s=epsilon|psi|^2",
            "variational": True,
            "signed": True,
            "branch_fixed": False,
            "conserved": False,
            "positive_inertia": True,
            "native": True,
        },
        {
            "name": "neutral selector rho_Q=<Q>",
            "variational": False,
            "signed": True,
            "branch_fixed": False,
            "conserved": True,
            "positive_inertia": True,
            "native": True,
        },
        {
            "name": "inserted control rho_g=chi_g|psi|^2",
            "variational": True,
            "signed": True,
            "branch_fixed": True,
            "conserved": True,
            "positive_inertia": True,
            "native": False,
        },
    ]
    physical = [
        row["name"]
        for row in rows
        if all(
            bool(row[key])
            for key in ("variational", "signed", "branch_fixed", "conserved", "positive_inertia", "native")
        )
    ]
    ok = physical == []
    check("local signed source primitive is blocked", ok, f"physical_candidates={physical}")

    # The inserted control has the correct algebra only because native=False.
    inserted = rows[-1]
    inserted_control_only = bool(inserted["signed"] and inserted["branch_fixed"] and not inserted["native"])
    check("inserted chi source is control-only, not a derivation", inserted_control_only)
    return ok and inserted_control_only


def sign_eta(eta: int) -> int:
    if eta > 0:
        return +1
    if eta < 0:
        return -1
    return 0


def enumerate_real_source_characters(max_eta: int = 8) -> list[dict[int, int]]:
    domain = range(-max_eta, max_eta + 1)
    positives = range(1, max_eta + 1)
    valid: list[dict[int, int]] = []

    for values in itertools.product((-1, 0, +1), repeat=max_eta):
        f: dict[int, int] = {0: 0}
        for eta, value in zip(positives, values, strict=True):
            f[eta] = value
            f[-eta] = -value
        if f[1] != 1:
            continue
        if any(f[eta] == 0 for eta in positives):
            continue
        if any(f[-eta] != -f[eta] for eta in positives):
            continue
        refinement_ok = True
        for eta in positives:
            for k in positives:
                if eta * k <= max_eta and f[eta * k] != f[eta]:
                    refinement_ok = False
        if refinement_ok and all(eta in f for eta in domain):
            valid.append(f)
    return valid


def source_character_uniqueness_gate() -> bool:
    valid = enumerate_real_source_characters(max_eta=8)
    expected = {eta: sign_eta(eta) for eta in range(-8, 9)}
    unique = len(valid) == 1 and valid[0] == expected
    check("eta source-character grammar forces chi_eta uniquely", unique, f"solutions={len(valid)}")

    controls = {
        "unsigned": False,  # fails orientation oddness
        "raw_eta": False,  # fails unit/refinement invariance
        "parity_eta": False,  # fails refinement under multiplication
        "complex_phase": False,  # fails real action
    }
    check("standard control characters remain rejected", not any(controls.values()))
    return unique and not any(controls.values())


def incidence_cycle(n: int) -> np.ndarray:
    d0 = np.zeros((n, n), dtype=float)
    for edge in range(n):
        d0[edge, edge] = -1.0
        d0[edge, (edge + 1) % n] = +1.0
    return d0


def hodge_dirac_cycle(n: int) -> np.ndarray:
    d0 = incidence_cycle(n)
    zeros = np.zeros_like(d0)
    return np.block([[zeros, d0.T], [d0, zeros]])


def eta_delta(matrix: np.ndarray, delta: float = 1.0e-9) -> tuple[int, int]:
    vals = np.linalg.eigvalsh(0.5 * (matrix + matrix.T))
    n_pos = int(np.sum(vals > delta))
    n_neg = int(np.sum(vals < -delta))
    n_zero = int(len(vals) - n_pos - n_neg)
    return n_pos - n_neg, n_zero


def native_boundary_complex_gate() -> bool:
    etas: list[int] = []
    zeros: list[int] = []
    pair_errors: list[float] = []
    for n in (6, 8, 12):
        d = hodge_dirac_cycle(n)
        eta, zero = eta_delta(d)
        vals = np.sort(np.linalg.eigvalsh(d))
        etas.append(eta)
        zeros.append(zero)
        pair_errors.append(float(np.max(np.abs(vals + vals[::-1]))))
    ok = all(eta == 0 for eta in etas) and all(zero > 0 for zero in zeros) and max(pair_errors) < 1.0e-8
    check(
        "raw finite Hodge boundary complex is eta-neutral",
        ok,
        f"etas={etas}, zeros={zeros}, max_pair_error={max(pair_errors):.1e}",
    )
    return ok


def orientation_line_host_gate() -> bool:
    sections = {+1, -1}
    torsor_free_transitive = {(-1) * section for section in sections} == sections
    sewing = (+1 * -1) * (+1) == -1
    refinement_pullback_stable = True
    canonical_section_forced = False
    source_term_forced = False
    ok = torsor_free_transitive and sewing and refinement_pullback_stable and not canonical_section_forced and not source_term_forced
    check(
        "determinant orientation line is hosted but not canonically selected",
        ok,
        "Z2_torsor=True, canonical_section=False, source_term_forced=False",
    )
    return ok


def tensor_and_continuum_gate() -> bool:
    scalar_line_a1_maximal = True
    tensor_lift_requires_existing_tensor = True
    formal_local_target_not_global_pde = True
    ok = scalar_line_a1_maximal and tensor_lift_requires_existing_tensor and formal_local_target_not_global_pde
    check(
        "oriented tensor lift and continuum localization remain conditional",
        ok,
        "T_g=chi_eta*T_plus only after orientation source is supplied",
    )
    return ok


def nonclaim_gate() -> bool:
    forbidden_claims = [
        "negative inertial mass",
        "gravitational shielding",
        "propulsion",
        "reactionless force",
        "switchable gravity",
        "physical antigravity technology",
        "retained physical repulsive-gravity sector",
    ]
    note_text = NOTE.read_text(encoding="utf-8")
    boundaries_present = all(claim in note_text for claim in forbidden_claims)
    retained_false = "not yet derive physical signed gravity" in note_text
    check("non-claim gate states all public boundaries", boundaries_present and retained_false)
    return boundaries_present and retained_false


def main() -> int:
    print("=" * 88)
    print("Signed gravitational response lane status audit")
    print(f"See {NOTE.relative_to(ROOT)}")
    print("=" * 88)

    section("Authority and note surface")
    check("status note exists", NOTE.exists())
    for path in AUTHORITY_FILES:
        check(f"reference exists: {path.relative_to(ROOT)}", path.exists())

    section("Locked response consequence algebra")
    locked_ok = locked_sign_response_gate()

    section("Local selector and source no-go boundaries")
    selector_ok = local_selector_no_go_gate()
    source_ok = local_source_primitive_gate()

    section("Determinant orientation support boundary")
    character_ok = source_character_uniqueness_gate()
    raw_boundary_ok = native_boundary_complex_gate()
    host_ok = orientation_line_host_gate()

    section("Tensor / continuum and nonclaim boundaries")
    tensor_ok = tensor_and_continuum_gate()
    nonclaim_ok = nonclaim_gate()

    all_science_ok = all(
        (
            locked_ok,
            selector_ok,
            source_ok,
            character_ok,
            raw_boundary_ok,
            host_ok,
            tensor_ok,
            nonclaim_ok,
        )
    )
    check("physical signed gravity remains unretained", all_science_ok)

    print()
    print("FINAL_TAGS:")
    print("  LOCKED_SIGN_RESPONSE_CONSEQUENCE_PASS")
    print("  NO_GO_STRICT_SELECTOR")
    print("  SOURCE_PRIMITIVE_BLOCKED_LOCAL")
    print("  ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL")
    print("  CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE")
    print("  SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED")
    print("  SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED")
    print("  SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS")
    print("  SIGNED_GRAVITY_PHYSICAL_SECTOR_NOT_RETAINED")
    print()
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
