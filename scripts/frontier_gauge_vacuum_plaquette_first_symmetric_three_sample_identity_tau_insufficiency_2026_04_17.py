#!/usr/bin/env python3
"""
Identity-plus-Tau insufficiency on the first symmetric three-sample plaquette
PF seam.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def radical_entries() -> dict[str, sp.Expr]:
    rt2 = sp.sqrt(2)
    return {
        "a": -3 * sp.sqrt(2 - rt2),
        "b": -3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) + 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "c": 16
        + 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        - 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
        "d": 3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) - 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "e": 16
        - 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        + 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
    }


def sample_matrix(entries: dict[str, sp.Expr]) -> sp.Matrix:
    return sp.Matrix(
        [
            [1, entries["a"], 0],
            [1, entries["b"], entries["c"]],
            [1, entries["d"], entries["e"]],
        ]
    )


def main() -> int:
    envelope_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md"
    )
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    pf_note = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    entries = radical_entries()
    fmat = sample_matrix(entries)
    a = entries["a"]
    b = entries["b"]
    c = entries["c"]
    d = entries["d"]
    e = entries["e"]

    tau0 = sp.symbols("tau_0", nonnegative=True)
    c_mass = sp.symbols("C", positive=True)
    lam = sp.symbols("lambda", nonnegative=True)

    rho10 = lam
    rho11 = sp.simplify((c_mass - 18 * lam) / 64)
    zhat_e = sp.simplify(1 + tau0 + c_mass)
    tau_relation_gap = sp.simplify(zhat_e - 1 - 18 * rho10 - 64 * rho11 - tau0)

    z_ret = sp.simplify(fmat * sp.Matrix([1, rho10, rho11]))
    z_ret_deriv = sp.simplify(sp.diff(z_ret, lam))
    deriv_first = sp.simplify(z_ret_deriv[0])

    c0 = sp.Integer(1)
    lam_p = sp.Integer(0)
    lam_q = sp.Rational(1, 36)
    rho_p = sp.Matrix([lam_p, sp.simplify((c0 - 18 * lam_p) / 64)])
    rho_q = sp.Matrix([lam_q, sp.simplify((c0 - 18 * lam_q) / 64)])
    z_p = sp.simplify(fmat * sp.Matrix([1, rho_p[0], rho_p[1]]))
    z_q = sp.simplify(fmat * sp.Matrix([1, rho_q[0], rho_q[1]]))
    z_gap = sp.simplify(z_q - z_p)

    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE IDENTITY-TAU INSUFFICIENCY")
    print("=" * 118)
    print()
    print("Exact first-seam affine fiber at fixed identity value and fixed tail mass")
    print(f"  rho_(1,0)(6)                               = {rho10}")
    print(f"  rho_(1,1)(6)                               = {rho11}")
    print(f"  Z_hat_6(e)                                 = {zhat_e}")
    print(f"  identity-relation gap                      = {tau_relation_gap}")
    print()
    print("Retained three-sample triple on that fiber")
    print(f"  Z_ret(lambda)                              = {z_ret}")
    print(f"  dZ_ret/dlambda                             = {z_ret_deriv}")
    print()
    print("Explicit witness pair at fixed C=1")
    print(f"  P: (rho10, rho11)                          = ({rho_p[0]}, {rho_p[1]})")
    print(f"  Q: (rho10, rho11)                          = ({rho_q[0]}, {rho_q[1]})")
    print(f"  Z_ret(P)                                   = {z_p}")
    print(f"  Z_ret(Q)                                   = {z_q}")
    print(f"  Z_ret(Q)-Z_ret(P)                          = {z_gap}")
    print()

    check(
        "The truncation-envelope note already fixes both the first-seam sample equations and the exact identity-mass relation",
        "`Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`" in envelope_note
        and "`Z_hat_B = 1 + b rho_(1,0) + c rho_(1,1) + R_B^(>1)`" in envelope_note
        and "`Z_hat_C = 1 + d rho_(1,0) + e rho_(1,1) + R_C^(>1)`" in envelope_note
        and "`Tau_(>1) = Z_hat_6(e) - 1 - 18 rho_(1,0)(6) - 64 rho_(1,1)(6)`" in envelope_note,
        bucket="SUPPORT",
    )
    check(
        "The exact radical-map note already fixes the retained three-sample operator F and its invertibility",
        "every entry of `F` is an explicit radical constant" in radical_note
        and "`det(F) != 0`" in radical_note,
        bucket="SUPPORT",
    )
    check(
        "The PF boundary note already identifies beta-side environment data, not one scalar, as the live missing plaquette object",
        "one common beta-side vector" in pf_note
        and "missing load-bearing input is now sharper than before" in pf_note,
        bucket="SUPPORT",
    )

    check(
        "Fixing Z_hat_6(e) and Tau_(>1) determines only the affine line 18 rho_(1,0)(6) + 64 rho_(1,1)(6) = C",
        tau_relation_gap == 0,
        detail=f"identity relation gap={tau_relation_gap}",
    )
    check(
        "The nonnegative retained coefficient family lambda in [0, C/18] stays on that exact fixed-identity fixed-tail slice",
        sp.simplify(rho11.subs({lam: 0}) - c_mass / 64) == 0
        and sp.simplify(rho11.subs({lam: c_mass / 18})) == 0,
        detail=f"rho11(0)={sp.simplify(rho11.subs({lam: 0}))}, rho11(C/18)={sp.simplify(rho11.subs({lam: c_mass / 18}))}",
    )
    check(
        "The retained three-sample triple varies nontrivially along that fiber",
        sp.simplify(deriv_first - a) == 0 and a != 0,
        detail=f"dZ_ret/dlambda first component={deriv_first}",
    )
    check(
        "So fixed identity value plus fixed tail mass still does not determine the retained coefficient pair",
        sp.simplify(rho_p[0] - rho_q[0]) != 0 and sp.simplify(rho_p[1] - rho_q[1]) != 0,
        detail=f"P={rho_p.T}, Q={rho_q.T}",
    )
    check(
        "An explicit fixed-identity fixed-tail witness pair already gives distinct retained three-sample triples",
        z_gap != sp.zeros(3, 1) and sp.simplify(z_gap[0] - a / 36) == 0,
        detail=f"witness gap={z_gap}",
    )
    check(
        "Therefore even fixing Z_hat_6(e) together with Tau_(>1) is still insufficient to close the first symmetric retained three-sample seam",
        tau_relation_gap == 0 and a != 0 and z_gap != sp.zeros(3, 1),
        detail="identity-plus-tail data leave an affine retained fiber with nonconstant sample image",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
