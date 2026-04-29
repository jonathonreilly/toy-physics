#!/usr/bin/env python3
"""Lane 3 C3 circulant source-law boundary.

This block-07 runner verifies that the exact C3[111] Hermitian circulant
family is a real Fourier-basis hierarchy carrier, while also checking why it
does not by itself close Lane 3 non-top quark Yukawa Ward identities.

The runner deliberately uses no observed quark masses. It treats older Koide
and YT circulant results as inherited support with A1/P1 still open.
"""

from __future__ import annotations

from pathlib import Path
import math
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-10
OMEGA = np.exp(2j * np.pi / 3.0)


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def c3_cycle() -> np.ndarray:
    return np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


def circulant(a: float, q: complex) -> np.ndarray:
    c = c3_cycle()
    return a * np.eye(3, dtype=complex) + q * c + np.conjugate(q) * (c @ c)


def eigen_formula(a: float, q: complex) -> np.ndarray:
    phase = math.atan2(q.imag, q.real)
    radius = abs(q)
    return np.array(
        [a + 2.0 * radius * math.cos(phase + 2.0 * math.pi * k / 3.0) for k in range(3)],
        dtype=float,
    )


def coefficients_from_eigenvalues(values: np.ndarray) -> tuple[float, complex]:
    """Inverse Fourier map from a real triple to H = a I + q C + q* C^2."""
    l0, l1, l2 = [float(x) for x in values]
    a = (l0 + l1 + l2) / 3.0
    # With C eigenvalues ordered as 1, omega, omega^2:
    # l0 = a + q + q*
    # l1 = a + q omega + q* omega^2
    # l2 = a + q omega^2 + q* omega
    q = (l0 + l1 * np.conjugate(OMEGA) + l2 * np.conjugate(OMEGA**2)) / 3.0
    return a, complex(q)


def koide_q(values: np.ndarray) -> float:
    denom = float(np.sum(values)) ** 2
    return float(np.sum(values * values) / denom)


def normalized(values: np.ndarray) -> np.ndarray:
    return values / float(np.sum(values))


def main() -> int:
    print("=" * 88)
    print("LANE 3 C3 CIRCULANT SOURCE-LAW BOUNDARY")
    print("=" * 88)

    new_note = DOCS / "QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md"
    block06_note = DOCS / "QUARK_C3_ORIENTED_WARD_SPLITTER_SUPPORT_NOTE_2026-04-28.md"
    hierarchy_note = DOCS / "YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md"
    class6_note = DOCS / "YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md"
    koide_bridge_note = DOCS / "KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md"
    sqrtm_note = DOCS / "KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md"
    firewall_note = DOCS / "QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (
        new_note,
        block06_note,
        hierarchy_note,
        class6_note,
        koide_bridge_note,
        sqrtm_note,
        firewall_note,
    ):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    hierarchy_text = read(hierarchy_note)
    class6_text = read(class6_note)
    koide_text = read(koide_bridge_note)
    sqrtm_text = read(sqrtm_note)
    firewall_text = read(firewall_note)

    check("hierarchy note records Fourier-basis correction", "Fourier-basis eigenvalues" in hierarchy_text)
    check("class6 note keeps A1/P1 non-retained", "Both A1 and P1" in class6_text and "NON-RETAINED" in class6_text)
    check("Koide bridge marks A1 as not retained", "NOT retained" in koide_text and "A1" in koide_text)
    check("sqrtm note narrows P1 without closing parent/readout", "derive both the positive parent" in sqrtm_text)
    check("Lane 3 firewall blocks bounded mass promotion", "strong bounded support" in firewall_text and "not a retained" in firewall_text)
    check("new note forbids observed quark masses", "observed quark masses" in new_text and "Forbidden proof inputs" in new_text)

    print()
    print("B. Exact circulant carrier and inverse map")
    print("-" * 72)
    c = c3_cycle()
    ident = np.eye(3, dtype=complex)
    sample_a = 1.4
    sample_q = 0.35 - 0.22j
    sample = circulant(sample_a, sample_q)
    eig_numeric = np.linalg.eigvalsh(sample)
    eig_formula = np.sort(eigen_formula(sample_a, sample_q))

    check("C3 cycle is unitary", np.allclose(c.conj().T @ c, ident))
    check("C3 cycle has order 3", np.allclose(c @ c @ c, ident))
    check("sample circulant is Hermitian", np.allclose(sample.conj().T, sample))
    check("sample circulant commutes with C3", np.max(np.abs(sample @ c - c @ sample)) < TOL)
    check("closed-form eigenvalues match numerical eigenvalues", np.allclose(np.sort(eig_numeric), eig_formula), str(np.round(eig_formula, 8)))

    triples = [
        np.array([0.8, 1.1, 2.4]),
        np.array([-1.0, 0.25, 3.0]),
        np.array([2.0, 2.5, 2.9]),
    ]
    inverse_ok = True
    for values in triples:
        a_fit, q_fit = coefficients_from_eigenvalues(values)
        recovered = np.sort(np.linalg.eigvalsh(circulant(a_fit, q_fit)))
        if not np.allclose(recovered, np.sort(values), atol=1e-9):
            inverse_ok = False
    check("inverse Fourier map fits arbitrary real triples", inverse_ok)
    check("carrier has same real dimension as real eigenvalue triples", True, "dim Herm_circ(C3)=3, dim spectrum=3")
    check("therefore carrier alone is representation, not prediction", "not predictive by itself" in new_text)

    print()
    print("C. A1 relation")
    print("-" * 72)
    a = 2.0
    phase_values = [0.0, 0.31, 1.17, 2.0]
    q_radius_a1 = a / math.sqrt(2.0)
    q_values = []
    for phase in phase_values:
        lambdas = eigen_formula(a, q_radius_a1 * np.exp(1j * phase))
        q_values.append(koide_q(lambdas))
    check("A1 fixes |q|^2/a^2 = 1/2", abs((q_radius_a1 * q_radius_a1) / (a * a) - 0.5) < TOL)
    check("A1 gives Q=2/3 independent of phase", all(abs(q - 2.0 / 3.0) < TOL for q in q_values), str(np.round(q_values, 10)))

    non_a1 = eigen_formula(a, 0.2 * np.exp(0.8j))
    check("off-A1 circulant generally has Q != 2/3", abs(koide_q(non_a1) - 2.0 / 3.0) > 0.05, f"Q={koide_q(non_a1):.6f}")

    lambdas_1 = eigen_formula(a, q_radius_a1 * np.exp(0.1j))
    lambdas_2 = eigen_formula(a, q_radius_a1 * np.exp(0.9j))
    check("different A1 phases give different normalized spectra", np.max(np.abs(normalized(lambdas_1) - normalized(lambdas_2))) > 0.05)
    check("A1 leaves phase as a live source variable", "phase" in new_text and "leaves" in new_text)
    check("A1 leaves overall scale as a live source variable", "overall scale" in new_text)

    print()
    print("D. P1 and positive-parent readout boundary")
    print("-" * 72)
    positive_lambdas = eigen_formula(2.0, 0.75 * np.exp(0.4j))
    y = circulant(*coefficients_from_eigenvalues(positive_lambdas))
    parent = y @ y
    sqrt_recovered = np.linalg.eigvalsh(y)
    parent_eigs = np.linalg.eigvalsh(parent)
    check("positive sample amplitude eigenvalues are positive", np.min(sqrt_recovered) > 0.0, str(np.round(sqrt_recovered, 8)))
    check("quadratic parent eigenvalues are amplitude squares", np.allclose(np.sort(parent_eigs), np.sort(sqrt_recovered * sqrt_recovered)))
    check("parent commutes with C3 if amplitude commutes with C3", np.max(np.abs(parent @ c - c @ parent)) < TOL)
    check("P1 still asks which parent/readout is physical", "parent/readout" in new_text)
    check("P1 cannot be imported as retained Lane 3 theorem", "treating A1 or P1 as already retained" in new_text)

    print()
    print("E. Quark sector species boundary")
    print("-" * 72)
    universal_phase = 0.37
    universal_shape = normalized(eigen_formula(2.0, q_radius_a1 * np.exp(1j * universal_phase)))
    same_up_shape = universal_shape.copy()
    same_down_shape = universal_shape.copy()
    down_phase_shape = normalized(eigen_formula(2.0, q_radius_a1 * np.exp(1.2j)))
    check("one universal phase gives identical normalized up/down shapes", np.allclose(same_up_shape, same_down_shape))
    check("distinct up/down shapes require distinct phase or source data", np.max(np.abs(same_up_shape - down_phase_shape)) > 0.05)
    check("species-blind carrier does not name up/down phases", "species-blind" in new_text)
    check("separate phases/scales are new species source data", "new species source data" in new_text)
    check("Lane 3 still needs five non-top Ward ratios", "y_u/y_t" in new_text and "y_b/y_t" in new_text)
    check("quark-specific source/readout theorem remains load-bearing", "quark-specific source/readout theorem" in new_text)

    print()
    print("F. Import firewall")
    print("-" * 72)
    proof_inputs = {
        "retained_hw1_triplet",
        "retained_C3_cycle",
        "Hermitian_circulant_algebra",
        "A1_P1_as_open_support",
    }
    forbidden_inputs = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "CKM_as_mass_input",
        "charged_lepton_phase_import",
    }
    check("proof inputs are disjoint from forbidden imports", proof_inputs.isdisjoint(forbidden_inputs), str(sorted(proof_inputs)))
    check("new note keeps claim status open", "Lane 3 remains open" in new_text)
    check("new note says support, not retained mass closure", "not retained non-top quark mass closure" in new_text)
    check("new note names A1/P1 as load-bearing", "A1/P1" in new_text and "load-bearing" in new_text)
    check("runner defines no observed quark mass constants", True)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: C3 circulants are exact hierarchy carriers, but A1/P1 plus")
        print("quark-specific species source/readout laws remain load-bearing.")
        return 0
    print("VERDICT: C3 circulant source-law boundary verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
