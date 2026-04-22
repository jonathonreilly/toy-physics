#!/usr/bin/env python3
"""
O2.a — Re-derive the Casimir SUM via explicit gauge-by-gauge 1-loop enumeration.

The retained `C_τ = T(T+1) + Y² = 1` is computed in
`docs/KOIDE_EXPLICIT_CALCULATIONS_NOTE.md` Deliverable 2 by enumerating
the SU(2)_L × U(1)_Y gauge-boson contributions to the charged-lepton
self-energy:

    C_W± = T(T+1) − T_3²    (off-diagonal SU(2)_L on tau_L)
    C_W3 = T_3²             (diagonal SU(2)_L on tau_L)
    C_B  = |Y_L · Y_R| / 2  (hypercharge, GUT-normalised)

    C_tau = C_SU(2)_L + C_U(1)_Y  =  (C_W± + C_W3) + C_B
          = (T(T+1) - T_3^2) + T_3^2 + Y_L Y_R / 2
          = T(T+1) + Y_L Y_R / 2.

For the lepton chirality assignment Y_L = -1/2, Y_R = -1, this gives
T(T+1) + 1/4 = 1. So the "Y^2" combination in the C_tau = 1 statement
is operationally Y_L · Y_R / 2, not literally Y_L^2.

This sub-step rebuilds that calculation and surfaces the equivalence
to the SUM identity T(T+1) + Y^2 = 1 used in O1's two-line schema.
We then pin the algebraic identity Y_L · Y_R / 2 = Y_L^2 that holds
on the (Y_L, Y_R) = (-1/2, -1) lepton chirality assignment, which is
exactly the input that lets the SUM combination "look like" T(T+1) + Y^2.
"""

from __future__ import annotations

import sys
from fractions import Fraction


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("O2.a — gauge-by-gauge enumeration of the Casimir SUM")

    # Charged-lepton chirality assignment from the retained
    # CL3_SM_EMBEDDING_THEOREM (Peskin convention Q = T_3 + Y).
    T = Fraction(1, 2)
    T3 = Fraction(-1, 2)  # tau_L is the lower component
    Y_L = Fraction(-1, 2)
    Y_R = Fraction(-1)
    Q_L = T3 + Y_L
    Q_R = Fraction(0) + Y_R

    print(f"  tau_L: T={T}, T_3={T3}, Y_L={Y_L}, Q_L={Q_L}")
    print(f"  tau_R: T=0,  T_3=0,  Y_R={Y_R}, Q_R={Q_R}")

    record("A.1 Q_L = -1 (charged lepton)", Q_L == -1)
    record("A.2 Q_R = -1 (charged lepton)", Q_R == -1)

    # ---- B. Per-boson Casimir contributions on the tau self-energy ---------
    section("B. Per-boson Casimir contributions")
    C_Wpm = T * (T + 1) - T3 ** 2
    C_W3 = T3 ** 2
    C_B = abs(Y_L * Y_R) / 2
    print(f"  C_W±  = T(T+1) - T_3^2 = {C_Wpm}")
    print(f"  C_W3  = T_3^2          = {C_W3}")
    print(f"  C_B   = |Y_L Y_R| / 2  = {C_B}")

    record("B.1 C_W±  = 1/2", C_Wpm == Fraction(1, 2))
    record("B.2 C_W3  = 1/4", C_W3 == Fraction(1, 4))
    record("B.3 C_B   = 1/4", C_B == Fraction(1, 4))

    # ---- C. Sum gives C_tau = 1 -------------------------------------------
    section("C. C_tau = C_SU(2)_L + C_U(1)_Y = 1")
    C_SU2 = C_Wpm + C_W3
    C_U1Y = C_B
    C_tau = C_SU2 + C_U1Y
    record(
        "C.1 C_SU(2)_L = T(T+1) = 3/4",
        C_SU2 == T * (T + 1),
    )
    record(
        "C.2 C_tau = 1",
        C_tau == 1,
        f"C_tau = {C_SU2} + {C_U1Y} = {C_tau}",
    )

    # ---- D. EM convention cross-check: C_gamma = Q_tau^2 = 1 ---------------
    section("D. EM Q^2 cross-check (convention free)")
    C_gamma = Q_L ** 2
    record("D.1 C_gamma = Q_tau^2 = 1", C_gamma == 1)
    record("D.2 C_tau (mixed gauge) = C_gamma (EM)", C_tau == C_gamma)

    # ---- E. Algebraic identity Y_L Y_R / 2 = Y_L^2 on the lepton assignment
    section("E. Identity Y_L Y_R / 2 = Y_L^2  on (Y_L, Y_R) = (-1/2, -1)")
    lhs = Y_L * Y_R / 2
    rhs = Y_L ** 2
    record(
        "E.1 Y_L Y_R / 2 = Y_L^2",
        lhs == rhs,
        f"Y_L Y_R / 2 = (-1/2)(-1)/2 = 1/4 = (-1/2)^2 = Y_L^2",
    )
    record(
        "E.2 Therefore C_tau = T(T+1) + Y_L^2",
        C_tau == T * (T + 1) + Y_L ** 2,
    )

    # ---- F. The Higgs check: same SUM holds for the Higgs participants -----
    section("F. Higgs check: same SUM with Y_H = +1/2")
    Y_H = Fraction(1, 2)
    sum_H = T * (T + 1) + Y_H ** 2
    record(
        "F.1 T(T+1) + Y_H^2 = 1 for the Higgs (Y_H = +1/2)",
        sum_H == 1,
    )
    record(
        "F.2 Y_L^2 = Y_H^2 = 1/4  (same magnitude, opposite sign — SUM is sign-blind)",
        Y_L ** 2 == Y_H ** 2,
    )

    # ---- G. The SUM = 1 also holds for e_R (Q^2 = 1) — SUM is NOT unique
    section("G. SUM-only landscape: SUM = 1 is shared by L, H, AND e_R")
    cases = [
        ("Quark doublet Q",  Fraction(1, 2), Fraction(1, 6)),
        ("e_R",              Fraction(0),    Fraction(-1)),
        ("u_R",              Fraction(0),    Fraction(2, 3)),
        ("d_R",              Fraction(0),    Fraction(-1, 3)),
    ]
    sum_eq_1 = []
    for label, Tx, Yx in cases:
        s = Tx * (Tx + 1) + Yx ** 2
        if s == 1:
            sum_eq_1.append(label)
        print(f"  {label}: T(T+1) + Y^2 = {s}")
    record(
        "G.1 e_R also has SUM = 1 (because Q_eR = -1 and SUM = Q^2 there)",
        "e_R" in sum_eq_1,
    )
    record(
        "G.2 SUM = 1 NOT unique: shared by {L, H, e_R} — distinguishing lemma is the DIFFERENCE (O3)",
        sum_eq_1 == ["e_R"],
        "Only e_R among the non-doublets has SUM=1; quark doublet, u_R, d_R fail.",
    )

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    if n_pass == n_total:
        print("VERDICT: O2.a closed. The retained C_tau = 1 derivation is reproduced")
        print("from the W±, W3, B contributions; identity Y_L Y_R / 2 = Y_L^2 lets it")
        print("be written as T(T+1) + Y^2 = 1, the SUM half of the closure schema.")
        print("Next: O2.b — show that this SUM appears as a_0^2's proportionality.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
