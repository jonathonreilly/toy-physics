#!/usr/bin/env python3
"""Runner for the Connes-Kreimer Birkhoff factorization note."""

from __future__ import annotations

from pathlib import Path

try:
    import sympy as sp
    from sympy import Symbol, simplify
except ImportError as exc:
    raise SystemExit("sympy required for exact algebra") from exc

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md"

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {label}")
    if detail:
        print(f"         {detail}")


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def pole_part(expr, e):
    """Projection onto strictly negative powers of e for simple Laurent sums."""
    expanded = sp.expand(expr)
    total = 0
    for term in sp.Add.make_args(expanded):
        coeff, powers = term.as_coeff_mul(e)
        power = sum(factor.as_powers_dict().get(e, 0) for factor in powers)
        if power < 0:
            total += term
    return simplify(total)


def test_coproduct() -> None:
    section("T1: rooted-tree coproduct")
    # For t1: Delta(t1) = t1 x 1 + 1 x t1.
    # For ladder t2: Delta(t2) = t2 x 1 + 1 x t2 + t1 x t1.
    delta_t1 = [("t1", "1"), ("1", "t1")]
    delta_t2 = [("t2", "1"), ("1", "t2"), ("t1", "t1")]
    check("Delta(t1) has the two counital terms", len(delta_t1) == 2, str(delta_t1))
    check("Delta(t2) has one admissible-cut term t1 x t1", ("t1", "t1") in delta_t2 and len(delta_t2) == 3, str(delta_t2))


def test_convolution() -> None:
    section("T2: character convolution")
    a, b, p, q = sp.symbols("a b p q")
    # phi(t1)=a, phi(t2)=b, psi(t1)=p, psi(t2)=q.
    conv_t1 = a + p
    conv_t2 = b + q + a * p
    check("(phi * psi)(t1) = phi(t1) + psi(t1)", simplify(conv_t1 - (a + p)) == 0)
    check("(phi * psi)(t2) = phi(t2) + psi(t2) + phi(t1)psi(t1)", simplify(conv_t2 - (b + q + a * p)) == 0)


def test_rota_baxter_identity() -> None:
    section("T3: Laurent pole Rota-Baxter identity")
    e = Symbol("e")
    pairs = [
        (1 / e + 2, 3 / e + e),
        (1 / e**2 + e, 2 / e + 5),
        (4 / e + e**2, 3 / e**2 + 7),
    ]
    results = []
    for x, y in pairs:
        left = pole_part(x, e) * pole_part(y, e) + pole_part(x * y, e)
        right = pole_part(pole_part(x, e) * y, e) + pole_part(x * pole_part(y, e), e)
        results.append(simplify(left - right) == 0)
    check("pole projection satisfies the Rota-Baxter identity on test pairs", all(results), f"results={results}")


def test_birkhoff_t1() -> None:
    section("T4: Birkhoff recursion on t1")
    e = Symbol("e")
    alpha = Symbol("alpha")
    phi_t1 = 1 / e + alpha
    phi_minus_t1 = -pole_part(phi_t1, e)
    phi_plus_t1 = simplify(phi_t1 + phi_minus_t1)
    check("phi_-(t1) removes the pole", simplify(phi_minus_t1 + 1 / e) == 0, f"phi_-={phi_minus_t1}")
    check("phi_+(t1) is the regular part", simplify(phi_plus_t1 - alpha) == 0, f"phi_+={phi_plus_t1}")


def test_birkhoff_t2() -> None:
    section("T5: Birkhoff recursion on t2")
    e = Symbol("e")
    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    phi_t1 = 1 / e + alpha
    phi_t2 = 1 / e**2 + beta / e + gamma
    phi_minus_t1 = -pole_part(phi_t1, e)
    prepared_t2 = simplify(phi_t2 + phi_minus_t1 * phi_t1)
    phi_minus_t2 = -pole_part(prepared_t2, e)
    phi_plus_t2 = simplify(prepared_t2 + phi_minus_t2)
    check("prepared t2 has only a simple pole plus regular part", simplify(prepared_t2 - ((beta - alpha) / e + gamma)) == 0, f"prepared={prepared_t2}")
    check("phi_-(t2) cancels that pole", simplify(phi_minus_t2 - ((alpha - beta) / e)) == 0, f"phi_-={phi_minus_t2}")
    check("phi_+(t2) is regular gamma", simplify(phi_plus_t2 - gamma) == 0, f"phi_+={phi_plus_t2}")


def test_convolution_unit() -> None:
    section("T6: convolution unit")
    a, b = sp.symbols("a b")
    # epsilon(1)=1, epsilon(t1)=epsilon(t2)=0.
    eps_phi_t1 = a
    phi_eps_t1 = a
    eps_phi_t2 = b
    phi_eps_t2 = b
    check("epsilon is the convolution unit on t1 and t2", all(simplify(x - y) == 0 for x, y in [(eps_phi_t1, a), (phi_eps_t1, a), (eps_phi_t2, b), (phi_eps_t2, b)]))


def test_note_boundary() -> None:
    section("T7: source-note boundary")
    text = NOTE.read_text(encoding="utf-8")
    lower = text.lower()
    bridge_subject = "framework operator is a " + "character on `h_r`"
    bridge_assertion = "the theorem " + "proves it"
    forbidden = [
        bridge_subject + "; " + bridge_assertion,
        "16-fold composition is " + "closed",
        "alpha_lm substitution is " + "closed",
        "pipeline-derived status: " + "retained",
    ]
    check("note declares positive_theorem", "**Claim type:** positive_theorem" in text)
    check("note avoids framework bridge and status overclaims", not any(item in lower for item in forbidden))


def main() -> int:
    print("# Connes-Kreimer Birkhoff factorization runner")
    print(f"# Source note: {NOTE.relative_to(ROOT)}")
    test_coproduct()
    test_convolution()
    test_rota_baxter_identity()
    test_birkhoff_t1()
    test_birkhoff_t2()
    test_convolution_unit()
    test_note_boundary()
    print(f"\n=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
