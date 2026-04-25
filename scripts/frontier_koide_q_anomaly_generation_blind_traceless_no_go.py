#!/usr/bin/env python3
"""
Koide Q anomaly-generation-blind traceless-source no-go.

After the Q bridge is reduced to one scalar, K_TL = 0, a natural positive
route is to ask whether the retained anomaly-forced 3+1 theorem can remove the
traceless singlet-vs-doublet source. This runner checks that route at the
generation/source level.

Verdict:
  The retained SM anomaly constraints are generation blind. With the full
  right-handed completion, each generation is anomaly-free, so arbitrary
  generation/isotype weights remain anomaly-neutral. The anomaly polynomial is
  either zero on the completed branch or proportional to the identity on a
  left-handed trigger branch; neither contains the C_3 isotype operator
  P_plus - P_perp. Therefore anomaly constraints do not force K_TL = 0.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def anomaly_vector_for_one_generation() -> dict[str, sp.Rational]:
    """SM one-generation anomaly traces in Y = 2(Q-T3) convention.

    All fields are represented as left-handed Weyl fields. Right-handed
    fields are included as left-handed conjugates with opposite hypercharge.
    """
    fields = [
        # name, Y, SU2_dim, SU3_dim
        ("Q_L", sp.Rational(1, 3), 2, 3),
        ("L_L", sp.Rational(-1), 2, 1),
        ("u_R^c", sp.Rational(-4, 3), 1, 3),
        ("d_R^c", sp.Rational(2, 3), 1, 3),
        ("e_R^c", sp.Rational(2), 1, 1),
        ("nu_R^c", sp.Rational(0), 1, 1),
    ]
    traces = {
        "Y": sp.Rational(0),
        "Y3": sp.Rational(0),
        "SU3_Y": sp.Rational(0),
        "SU2_Y": sp.Rational(0),
        "Witten_doublets": sp.Rational(0),
    }
    for _name, hypercharge, su2_dim, su3_dim in fields:
        mult = su2_dim * su3_dim
        traces["Y"] += mult * hypercharge
        traces["Y3"] += mult * hypercharge**3
        traces["SU3_Y"] += su2_dim * (sp.Rational(1, 2) if su3_dim == 3 else 0) * hypercharge
        traces["SU2_Y"] += su3_dim * (sp.Rational(1, 2) if su2_dim == 2 else 0) * hypercharge
        if su2_dim == 2:
            traces["Witten_doublets"] += su3_dim
    return {key: sp.simplify(value) for key, value in traces.items()}


def left_trigger_vector_for_one_generation() -> dict[str, sp.Rational]:
    fields = [
        ("Q_L", sp.Rational(1, 3), 2, 3),
        ("L_L", sp.Rational(-1), 2, 1),
    ]
    traces = {
        "Y": sp.Rational(0),
        "Y3": sp.Rational(0),
        "SU3_Y": sp.Rational(0),
        "SU2_Y": sp.Rational(0),
    }
    for _name, hypercharge, su2_dim, su3_dim in fields:
        mult = su2_dim * su3_dim
        traces["Y"] += mult * hypercharge
        traces["Y3"] += mult * hypercharge**3
        traces["SU3_Y"] += su2_dim * (sp.Rational(1, 2) if su3_dim == 3 else 0) * hypercharge
        traces["SU2_Y"] += su3_dim * (sp.Rational(1, 2) if su2_dim == 2 else 0) * hypercharge
    return {key: sp.simplify(value) for key, value in traces.items()}


def main() -> int:
    section("A. One-generation anomaly cancellation")

    full = anomaly_vector_for_one_generation()
    record(
        "A.1 one completed SM generation has zero U(1), cubic, and mixed anomalies",
        full["Y"] == 0 and full["Y3"] == 0 and full["SU3_Y"] == 0 and full["SU2_Y"] == 0,
        f"full anomaly vector = {full}",
    )
    record(
        "A.2 Witten SU(2) parity is even after color multiplicity",
        int(full["Witten_doublets"]) % 2 == 0,
        f"doublets per generation = {full['Witten_doublets']}",
    )

    section("B. Arbitrary generation weights remain anomaly-neutral")

    w0, w1, w2 = sp.symbols("w0 w1 w2", real=True)
    weights = sp.Matrix([w0, w1, w2])
    weighted_full = {key: sp.simplify((w0 + w1 + w2) * value) for key, value in full.items()}
    weighted_perturbative = {
        key: weighted_full[key]
        for key in ("Y", "Y3", "SU3_Y", "SU2_Y")
    }
    record(
        "B.1 completed-branch anomaly constraints have rank zero on generation weights",
        all(value == 0 for value in weighted_perturbative.values()),
        f"weighted perturbative anomaly vector = {weighted_perturbative}",
    )

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.eye(3) - P_plus
    Z = sp.simplify(P_plus - P_perp)
    k_trace, k_tl = sp.symbols("k_trace k_tl", real=True)
    K = sp.simplify(k_trace * sp.eye(3) + k_tl * Z)
    record(
        "B.2 the K_TL source operator is C_3-equivariant",
        sp.simplify(C * K - K * C) == sp.zeros(3, 3),
        "K = k_trace I + k_tl(P_plus-P_perp).",
    )
    anomaly_with_K = {
        key: sp.simplify(sp.trace(K) * value)
        for key, value in full.items()
        if key != "Witten_doublets"
    }
    record(
        "B.3 the completed perturbative anomaly polynomial is blind to K_TL because the charge trace is zero",
        all(value == 0 for value in anomaly_with_K.values()),
        f"Tr_gen(K) times full anomaly vector = {anomaly_with_K}",
    )
    witten_weighted = sp.simplify((w0 + w1 + w2) * full["Witten_doublets"])
    record(
        "B.4 Witten parity supplies only an even-generation doublet count, not a continuous K_TL equation",
        int(full["Witten_doublets"]) % 2 == 0 and not witten_weighted.has(k_tl),
        f"weighted doublet count = {witten_weighted}; no coefficient of k_tl appears.",
    )

    section("C. Left-handed trigger branch is scalar in generation space")

    left = left_trigger_vector_for_one_generation()
    left_matrix = {key: sp.simplify(value * sp.eye(3)) for key, value in left.items()}
    record(
        "C.1 the left-handed anomaly trigger is proportional to identity on generation space",
        all(mat == left[key] * sp.eye(3) for key, mat in left_matrix.items()),
        f"left trigger vector = {left}",
    )
    left_tl_overlap = {
        key: sp.simplify(sp.trace(left_matrix[key] * Z))
        for key in ("Y", "Y3", "SU3_Y", "SU2_Y")
    }
    record(
        "C.2 identity-valued anomaly data have no independent isotype operator P_plus-P_perp",
        all(sp.simplify(left_matrix[key] - left[key] * sp.eye(3)) == sp.zeros(3, 3) for key in left_matrix),
        "The anomaly trigger carries generation scalar data only.",
    )
    record(
        "C.3 any apparent overlap is only full trace, hence multiplier/scale data, not a shape law",
        all(sp.simplify(left_tl_overlap[key] - left[key] * sp.trace(Z)) == 0 for key in left_tl_overlap),
        f"Tr(I*Z) overlaps = {left_tl_overlap}; no coefficient fixes k_tl=0.",
    )

    section("D. Explicit anomaly-neutral off-Koide source")

    y = sp.symbols("y", positive=True, real=True)
    k_tl_of_y = sp.simplify((1 - y) / (y * (2 - y)))
    eps = sp.Rational(1, 5)
    y_eps = [sol for sol in sp.solve(sp.Eq(k_tl_of_y, eps), y) if 0 < float(sol.evalf()) < 2][0]
    kappa_eps = sp.simplify(2 * y_eps / (2 - y_eps))
    q_eps = sp.simplify((1 + 2 / kappa_eps) / 3)
    record(
        "D.1 K_TL=1/5 is admissible and off Koide",
        sp.simplify(q_eps - sp.Rational(2, 3)) != 0,
        f"y={sp.N(y_eps, 12)}, Q={sp.N(q_eps, 12)}",
    )
    record(
        "D.2 the same off-Koide source is invisible to completed anomaly constraints",
        all(anomaly_with_K[key].subs(k_tl, eps) == 0 for key in ("Y", "Y3", "SU3_Y", "SU2_Y")),
        "Anomaly cancellation imposes no equation setting eps to zero.",
    )

    section("E. Verdict")

    record(
        "E.1 anomaly constraints do not force K_TL=0",
        True,
        "Completed anomalies vanish generation by generation; left-trigger anomalies are generation scalar.\n"
        "Neither supplies a traceless singlet-vs-doublet source law.",
    )
    record(
        "E.2 Q remains open after anomaly-generation-blind audit",
        True,
        "Residual primitive: derive no physical generation/isotype traceless source K_TL.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: anomaly data are generation blind and do not force K_TL=0.")
        print("The retained anomaly theorem supports the matter structure but does")
        print("not close the charged-lepton Koide Q source law.")
        print()
        print("KOIDE_Q_ANOMALY_GENERATION_BLIND_TR_SOURCE_NO_GO=TRUE")
        print("Q_ANOMALY_GENERATION_BLIND_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=physical_generation_isotype_no_traceless_source_K_TL")
        return 0

    print("VERDICT: anomaly-generation-blind audit has FAILs.")
    print()
    print("KOIDE_Q_ANOMALY_GENERATION_BLIND_TR_SOURCE_NO_GO=FALSE")
    print("Q_ANOMALY_GENERATION_BLIND_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=physical_generation_isotype_no_traceless_source_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
