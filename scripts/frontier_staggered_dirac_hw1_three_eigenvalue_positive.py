#!/usr/bin/env python3
"""Check the hw=1 circulant three-eigenvalue source note.

This runner verifies the load-bearing algebra used by
STAGGERED_DIRAC_HW1_THREE_EIGENVALUE_STRUCTURE_POSITIVE_THEOREM_NOTE_2026-05-10.
It does not audit or promote the cited BZ-corner carrier authorities.
"""

from pathlib import Path
import re
import sys

try:
    import sympy as sp
except ImportError:
    print("FAIL: sympy is required")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "STAGGERED_DIRAC_HW1_THREE_EIGENVALUE_STRUCTURE_POSITIVE_THEOREM_NOTE_2026-05-10.md"

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"PASS: {label}" + (f" ({detail})" if detail else ""))
    else:
        FAIL += 1
        print(f"FAIL: {label}" + (f" ({detail})" if detail else ""))


def main():
    a, x, y = sp.symbols("a x y", real=True)
    b = x + sp.I * y
    bbar = sp.conjugate(b)

    C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    I3 = sp.eye(3)
    C2 = C * C
    H = a * I3 + b * C + bbar * C2

    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2

    check("C^3 is identity", C**3 == I3)
    check("omega is a primitive cube root", sp.simplify(omega**3 - 1) == 0 and sp.simplify(1 + omega + omega**2) == 0)
    check("circulant H is Hermitian", sp.simplify(H - H.H) == sp.zeros(3))
    check("circulant H commutes with C", sp.simplify(H * C - C * H) == sp.zeros(3))

    h11, h22, h33 = sp.symbols("h11 h22 h33", real=True)
    h12r, h12i, h13r, h13i, h23r, h23i = sp.symbols(
        "h12r h12i h13r h13i h23r h23i", real=True
    )
    G = sp.Matrix(
        [
            [h11, h12r + sp.I * h12i, h13r + sp.I * h13i],
            [h12r - sp.I * h12i, h22, h23r + sp.I * h23i],
            [h13r - sp.I * h13i, h23r - sp.I * h23i, h33],
        ]
    )
    comm = sp.simplify(G * C - C * G)
    equations = [comm[i, j] for i in range(3) for j in range(3) if comm[i, j] != 0]
    solution = sp.solve(
        equations,
        [h11, h22, h33, h12r, h12i, h13r, h13i, h23r, h23i],
        dict=True,
    )
    check("Hermitian commutant has one three-real-parameter circulant family", len(solution) == 1)
    if solution:
        Gc = sp.simplify(G.subs(solution[0]))
        diag = [sp.simplify(Gc[i, i]) for i in range(3)]
        upper = [sp.simplify(Gc[0, 1]), sp.simplify(Gc[1, 2]), sp.simplify(Gc[2, 0])]
        lower = [sp.simplify(Gc[1, 0]), sp.simplify(Gc[2, 1]), sp.simplify(Gc[0, 2])]
        check("commutant diagonal entries are equal", diag[0] == diag[1] == diag[2], str(diag))
        check("commutant upper cyclic entries are equal", upper[0] == upper[1] == upper[2], str(upper))
        check("commutant lower cyclic entries are conjugate cyclic entries", lower[0] == lower[1] == lower[2], str(lower))

    for k in range(3):
        v = sp.Matrix([1, omega**k, omega ** (2 * k)])
        lam = a + b * omega**k + bbar * omega ** (-k)
        residual = sp.simplify(H * v - lam * v)
        check(f"Fourier vector v_{k} has expected eigenvalue", residual == sp.zeros(3, 1))

    lambdas_xy = [
        sp.simplify(a + 2 * x),
        sp.simplify(a - x - sp.sqrt(3) * y),
        sp.simplify(a - x + sp.sqrt(3) * y),
    ]
    computed = [sp.simplify(a + b * omega**k + bbar * omega ** (-k)) for k in range(3)]
    check("closed eigenvalue forms in x,y match Fourier formula", all(sp.simplify(u - v) == 0 for u, v in zip(computed, lambdas_xy)))
    check("sum of eigenvalues is 3a", sp.simplify(sum(computed) - 3 * a) == 0)

    generic = [sp.N(expr.subs({a: 0, x: 1, y: sp.Rational(1, 3)})) for expr in lambdas_xy]
    check("sample noncoincident spectrum has three distinct values", len({round(float(v), 12) for v in generic}) == 3, str(generic))
    coincident = [sp.N(expr.subs({a: 0, x: 1, y: 0})) for expr in lambdas_xy]
    check("sample coincidence boundary has repeated values", coincident[1] == coincident[2], str(coincident))

    text = NOTE.read_text()
    check("note exists", NOTE.exists())
    check("note declares positive_theorem claim type", "**Claim type:** positive_theorem" in text)
    check("note preserves independent audit authority", "**Status authority:** independent audit lane only" in text)
    check("note uses explicit physical Cl(3) language", "physical `Cl(3)` local algebra" in text)
    check("note uses explicit Z^3 substrate language", "`Z^3` spatial substrate" in text)
    compact_text = re.sub(r"\s+", " ", text)
    check("note rejects species derivation overclaim", "not a derivation of physical charged-lepton identity" in compact_text)
    check("note has no bare A1/A2/R1/R2 premise labels", not re.search(r"\\b(A1|A2|R1|R2)\\b", text))
    check("note has no cached-log authority", "runner-cache" not in text)
    check("note has no PDG charged-lepton mass numerals", all(s not in text for s in ("0.510998", "105.658", "1776.86")))

    print(f"PASS={PASS} FAIL={FAIL}")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
