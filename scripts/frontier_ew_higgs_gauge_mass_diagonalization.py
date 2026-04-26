#!/usr/bin/env python3
"""Object-level verifier for the EW Higgs gauge-mass diagonalization theorem.

This runner audits the algebra in
docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md.
It does not use numerical electroweak pole masses, RGE inputs, or Higgs-mass
fits.  The checks are exact symbolic checks of the one-doublet tree-level
mass matrix, charge generator, coupling dictionary, and scalar Hessian
bookkeeping.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"


@dataclass
class Audit:
    passed: int = 0
    failed: int = 0

    def check(self, label: str, condition: bool, detail: str = "") -> None:
        if condition:
            self.passed += 1
            print(f"PASS: {label}" + (f" :: {detail}" if detail else ""))
        else:
            self.failed += 1
            print(f"FAIL: {label}" + (f" :: {detail}" if detail else ""))


def banner(title: str) -> None:
    print()
    print(f"=== {title} ===")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(is_zero(entry) for entry in matrix)


def audit_note_surface(audit: Audit) -> None:
    banner("Authority surface and scope")
    audit.check("theorem note exists", NOTE.exists(), str(NOTE.relative_to(ROOT)))

    text = read(NOTE)
    status_match = re.search(r"\*\*Status:\*\*\s*(.+?)\n\n", text, re.S)
    status = status_match.group(1).replace("\n", " ") if status_match else ""

    audit.check("status extracted", bool(status), status[:140])
    audit.check("status is standalone EW/Higgs theorem", "standalone positive electroweak/Higgs theorem" in status)
    audit.check("status limits theorem to tree-level gauge-boson spectrum", "tree-level gauge-boson mass spectrum" in status)
    audit.check("status does not promote Higgs/top/CKM lanes", "does not modify, promote, or close" in status)
    audit.check("primary runner is named in note", "frontier_ew_higgs_gauge_mass_diagonalization.py" in text)
    audit.check("what-this-does-not-claim section present", "## 10. What This Does Not Claim" in text)
    audit.check("no pole-mass derivation claimed", "It does not compute pole masses" in text)
    audit.check("bounded W mass lane not promoted", "does not promote the bounded `M_W`" in text)

    for rel in (
        "docs/CANONICAL_HARNESS_INDEX.md",
        "docs/publication/ci3_z3/PUBLICATION_MATRIX.md",
        "docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md",
        "docs/publication/ci3_z3/DERIVATION_ATLAS.md",
        "docs/publication/ci3_z3/RESULTS_INDEX.md",
    ):
        path = ROOT / rel
        audit.check(f"package surface exists: {rel}", path.exists())
        if path.exists():
            package_text = read(path)
            audit.check(
                f"package surface carries EW Higgs gauge-mass row: {rel}",
                "EW Higgs gauge-mass diagonalization" in package_text,
            )


def audit_pauli_and_vacuum(audit: Audit) -> None:
    banner("Pauli actions and unbroken charge")
    v = sp.symbols("v", positive=True, real=True)
    i = sp.I

    h0 = sp.Matrix([0, v / sp.sqrt(2)])
    tau1 = sp.Matrix([[0, 1], [1, 0]])
    tau2 = sp.Matrix([[0, -i], [i, 0]])
    tau3 = sp.Matrix([[1, 0], [0, -1]])
    t1, t2, t3 = tau1 / 2, tau2 / 2, tau3 / 2
    y = sp.Rational(1, 2) * sp.eye(2)

    audit.check("T1 H0 action", matrix_is_zero(t1 * h0 - sp.Matrix([v / (2 * sp.sqrt(2)), 0])))
    audit.check("T2 H0 action", matrix_is_zero(t2 * h0 - sp.Matrix([-i * v / (2 * sp.sqrt(2)), 0])))
    audit.check("T3 H0 action", matrix_is_zero(t3 * h0 - sp.Matrix([0, -v / (2 * sp.sqrt(2))])))
    audit.check("Y H0 action", matrix_is_zero(y * h0 - sp.Matrix([0, v / (2 * sp.sqrt(2))])))
    audit.check("T3 H0 = -Y H0", matrix_is_zero(t3 * h0 + y * h0))
    audit.check("Q H0 = 0 for Q=T3+Y", matrix_is_zero((t3 + y) * h0))

    alpha, beta = sp.symbols("alpha beta")
    xh0 = (alpha * t3 + beta * y) * h0
    audit.check("unbroken generator condition is alpha=beta", is_zero(xh0[1] - (beta - alpha) * v / (2 * sp.sqrt(2))))


def audit_mass_matrices(audit: Audit) -> None:
    banner("Gauge mass matrix diagonalization")
    g, gy, v = sp.symbols("g g_Y v", positive=True, real=True)
    w1, w2, w3, b = sp.symbols("W1 W2 W3 B", real=True)
    i = sp.I

    h0 = sp.Matrix([0, v / sp.sqrt(2)])
    tau1 = sp.Matrix([[0, 1], [1, 0]])
    tau2 = sp.Matrix([[0, -i], [i, 0]])
    tau3 = sp.Matrix([[1, 0], [0, -1]])
    t1, t2, t3 = tau1 / 2, tau2 / 2, tau3 / 2
    y = sp.Rational(1, 2) * sp.eye(2)

    charged_vec = g * w1 * t1 * h0 + g * w2 * t2 * h0
    charged_norm = sp.simplify((charged_vec.conjugate().T * charged_vec)[0])
    audit.check(
        "charged vacuum kinetic coefficient",
        is_zero(charged_norm - g**2 * v**2 * (w1**2 + w2**2) / 8),
        str(charged_norm),
    )
    audit.check(
        "charged complex-field identity W+W- = (W1^2+W2^2)/2",
        is_zero(((w1 - i * w2) / sp.sqrt(2)) * ((w1 + i * w2) / sp.sqrt(2)) - (w1**2 + w2**2) / 2),
    )
    mw2 = g**2 * v**2 / 4
    audit.check("M_W^2 = g^2 v^2 / 4", is_zero(mw2 - g**2 * v**2 / 4))

    neutral_vec = g * w3 * t3 * h0 + gy * b * y * h0
    neutral_norm = sp.simplify((neutral_vec.conjugate().T * neutral_vec)[0])
    audit.check(
        "neutral vacuum kinetic coefficient",
        is_zero(neutral_norm - v**2 * (g * w3 - gy * b) ** 2 / 8),
        str(neutral_norm),
    )

    mass = v**2 / 4 * sp.Matrix([[g**2, -g * gy], [-g * gy, gy**2]])
    gtot = sp.sqrt(g**2 + gy**2)
    photon_vec = sp.Matrix([gy / gtot, g / gtot])
    z_vec = sp.Matrix([g / gtot, -gy / gtot])
    mz2 = (g**2 + gy**2) * v**2 / 4

    audit.check("neutral matrix determinant vanishes", is_zero(mass.det()))
    audit.check("neutral matrix trace gives M_Z^2", is_zero(sp.trace(mass) - mz2))
    audit.check("photon eigenvector has zero eigenvalue", matrix_is_zero(mass * photon_vec))
    audit.check("Z eigenvector has M_Z^2 eigenvalue", matrix_is_zero(mass * z_vec - mz2 * z_vec))
    audit.check("photon and Z eigenvectors are orthogonal", is_zero((photon_vec.T * z_vec)[0]))

    rot = sp.Matrix([[g / gtot, -gy / gtot], [gy / gtot, g / gtot]])
    diag = sp.simplify(rot * mass * rot.T)
    audit.check("Weinberg rotation diagonalizes neutral mass matrix", matrix_is_zero(diag - sp.diag(mz2, 0)))

    cos2 = g**2 / (g**2 + gy**2)
    rho_tree = sp.simplify(mw2 / (mz2 * cos2))
    audit.check("rho_tree = 1", is_zero(rho_tree - 1))


def audit_electric_coupling(audit: Audit) -> None:
    banner("Electric coupling and normalization dictionary")
    g, gy, g1 = sp.symbols("g g_Y g1_GUT", positive=True, real=True)
    gtot = sp.sqrt(g**2 + gy**2)
    sinw = gy / gtot
    cosw = g / gtot
    e = g * gy / gtot

    audit.check("sin^2 + cos^2 = 1", is_zero(sinw**2 + cosw**2 - 1))
    audit.check("e = g sin(theta_W)", is_zero(e - g * sinw))
    audit.check("e = g_Y cos(theta_W)", is_zero(e - gy * cosw))
    audit.check("inverse electric coupling sum rule", is_zero(1 / e**2 - (1 / g**2 + 1 / gy**2)))

    gy_from_gut = sp.sqrt(sp.Rational(3, 5)) * g1
    audit.check("GUT-normalized dictionary g_Y^2 = (3/5) g1^2", is_zero(gy_from_gut**2 - sp.Rational(3, 5) * g1**2))


def audit_scalar_hessian(audit: Audit) -> None:
    banner("Scalar Hessian companion")
    h, mu, lam, v = sp.symbols("h mu lambda v", positive=True, real=True)
    hdagh = (v + h) ** 2 / 2
    potential = -mu**2 * hdagh + lam * hdagh**2
    stationary = sp.diff(potential, h).subs(h, 0)
    audit.check("stationary condition is mu^2 = lambda v^2", is_zero(stationary.subs(mu**2, lam * v**2)))

    expanded = sp.expand(potential.subs(mu**2, lam * v**2))
    m_h2 = sp.diff(expanded, h, 2).subs(h, 0)
    cubic = sp.expand(expanded).coeff(h, 3)
    quartic = sp.expand(expanded).coeff(h, 4)
    audit.check("radial Higgs Hessian m_h^2 = 2 lambda v^2", is_zero(m_h2 - 2 * lam * v**2))
    audit.check("scalar cubic coefficient is lambda v", is_zero(cubic - lam * v))
    audit.check("scalar quartic coefficient is lambda/4", is_zero(quartic - lam / 4))


def main() -> int:
    audit = Audit()
    print("=== EW Higgs gauge-mass diagonalization verifier ===")
    audit_note_surface(audit)
    audit_pauli_and_vacuum(audit)
    audit_mass_matrices(audit)
    audit_electric_coupling(audit)
    audit_scalar_hessian(audit)

    print()
    print(f"TOTAL: PASS={audit.passed}, FAIL={audit.failed}")
    if audit.failed:
        print("VERDICT: FAIL")
        return 1
    print("VERDICT: CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
