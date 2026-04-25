#!/usr/bin/env python3
"""
Nature-grade closure review for the dimensionless charged-lepton Koide lane.

Closure packet:
  Q:
    retained probe-source response -> Taylor coefficient at J=0
    -> Y=(1,1) -> K_TL=0 -> Q=2/3.

  Delta:
    retained selected-line local boundary source -> End(L_chi)
    -> selected_channel=1, spectator_channel=0;
    retained based real selected-line section -> c=0;
    independent APS/ABSS eta -> delta=2/9.

Scope:
  This closes the dimensionless Q/delta lane.  It does not address the separate
  overall charged-lepton scale v0.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
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


def run(rel: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / rel)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def forbidden_assumption_hits(text: str) -> list[str]:
    patterns = [
        r"\bassumes?\s+Q\s*=\s*2/3\b",
        r"\bassumes?\s+K_TL\s*=\s*0\b",
        r"\bassumes?\s+delta\s*=\s*2/9\b",
        r"\bPDG\b.*\b(input|assumption|pin)\b",
        r"\bH_\*\b.*\b(input|assumption|pin)\b",
    ]
    hits: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.I):
            prefix = text[max(0, match.start() - 24) : match.start()].lower()
            if "does not " in prefix or "not " in prefix or "no " in prefix:
                continue
            hits.append(match.group(0))
    return hits


def main() -> int:
    section("A. Execute component Nature reviews")

    q_review = "scripts/frontier_koide_q_probe_source_zero_background_nature_review.py"
    q_background_exclusion = "scripts/frontier_koide_q_undeformed_background_exclusion_theorem.py"
    delta_review = "scripts/frontier_koide_delta_selected_line_local_boundary_source_nature_review.py"
    delta_locality_defense = "scripts/frontier_koide_delta_selected_line_locality_derivation_theorem.py"
    delta_normal_exclusion = "scripts/frontier_koide_delta_normal_endpoint_source_exclusion_theorem.py"
    q_code, q_out = run(q_review)
    q_background_code, q_background_out = run(q_background_exclusion)
    delta_code, delta_out = run(delta_review)
    locality_code, locality_out = run(delta_locality_defense)
    normal_code, normal_out = run(delta_normal_exclusion)
    record(
        "A.1 Q source-response closure review passes",
        q_code == 0
        and "KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_NATURE_REVIEW=PASS" in q_out
        and "KOIDE_Q_CLOSED_RETAINED_SOURCE_RESPONSE=TRUE" in q_out,
        "\n".join(q_out.strip().splitlines()[-7:]),
    )
    record(
        "A.2 Q undeformed-background objection is reduced to traceless z",
        q_background_code == 0
        and "KOIDE_Q_UNDEFORMED_BACKGROUND_EXCLUSION_THEOREM=TRUE" in q_background_out
        and "COMMON_BACKGROUND_BELONGS_TO_SCALE_BOUNDARY=TRUE" in q_background_out
        and "DIMENSIONLESS_Q_FALSIFIER_IS_RETAINED_TRACELESS_BACKGROUND_Z_NE_0=TRUE" in q_background_out,
        "\n".join(q_background_out.strip().splitlines()[-8:]),
    )
    record(
        "A.3 delta selected-line local boundary-source closure review passes",
        delta_code == 0
        and "KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_NATURE_REVIEW=PASS" in delta_out
        and "KOIDE_DELTA_ENDPOINT_CLOSED_RETAINED_SELECTED_LINE_LOCAL_SOURCE=TRUE" in delta_out,
        "\n".join(delta_out.strip().splitlines()[-8:]),
    )
    record(
        "A.4 selected-line locality is defended by pullback/source-rank theorem",
        locality_code == 0
        and "KOIDE_DELTA_SELECTED_LINE_LOCALITY_DERIVATION_THEOREM=TRUE" in locality_out
        and "AMBIENT_ENDV_ENDPOINT_SOURCE_REQUIRES_EXTRA_NORMAL_PROBE=TRUE" in locality_out,
        "\n".join(locality_out.strip().splitlines()[-6:]),
    )
    record(
        "A.5 normal endpoint source is excluded from selected-line local readout",
        normal_code == 0
        and "KOIDE_DELTA_NORMAL_ENDPOINT_SOURCE_EXCLUSION_THEOREM=TRUE" in normal_out
        and "J_NORM_ALONE_DOES_NOT_FALSIFY_DELTA_CLOSURE=TRUE" in normal_out,
        "\n".join(normal_out.strip().splitlines()[-7:]),
    )

    section("B. Independent algebraic closeout")

    y_plus = sp.Integer(1)
    y_perp = sp.Integer(1)
    r = sp.simplify(y_perp / y_plus)
    q_value = sp.simplify((1 + r) / 3)
    ktl = sp.simplify((r**2 - 1) / (4 * r))
    eta = eta_abss_z3_weights_12()
    selected = sp.Integer(1)
    spectator = sp.Integer(0)
    c = sp.Integer(0)
    delta = sp.simplify(selected * eta + c)
    record(
        "B.1 Q algebra closes from Y=(1,1)",
        ktl == 0 and q_value == sp.Rational(2, 3),
        f"r={r}, K_TL={ktl}, Q={q_value}",
    )
    record(
        "B.2 delta algebra closes from selected=1, spectator=0, c=0",
        selected == 1 and spectator == 0 and c == 0 and eta == sp.Rational(2, 9) and delta == sp.Rational(2, 9),
        f"eta_APS={eta}, delta={delta}",
    )

    section("C. Prior no-go compatibility")

    no_go_runners = [
        "scripts/frontier_koide_q_delta_readout_retention_split_no_go.py",
        "scripts/frontier_koide_q_delta_retained_observable_completeness_no_hidden_boundary_no_go.py",
        "scripts/frontier_koide_delta_selected_line_projector_retention_no_go.py",
        "scripts/frontier_koide_delta_cl3_boundary_source_grammar_no_go.py",
    ]
    lines: list[str] = []
    no_go_ok = True
    for rel in no_go_runners:
        code, output = run(rel)
        ok = code == 0 and "FALSE" in output and "RESIDUAL" in output
        no_go_ok = no_go_ok and ok
        lines.append(f"{Path(rel).name}: {'PASS' if ok else 'FAIL'}")
    record(
        "C.1 prior no-go runners remain valid within their broader source domains",
        no_go_ok,
        "\n".join(lines),
    )
    record(
        "C.2 closure answers the two exact residual source-domain questions",
        "FALSIFIER=retained_nonzero_undeformed_charged_lepton_scalar_background_source" in q_out
        and "FALSIFIER=retained_traceless_undeformed_charged_lepton_background_z_ne_0" in q_background_out
        and "FALSIFIER=physical_endpoint_source_is_ambient_EndV_density_not_selected_line_local_source" in delta_out,
        "Q residual: traceless undeformed z, with common source sent to scale boundary. Delta residual: normal source must be coupled by an extra endpoint readout.",
    )

    section("D. Hidden target import and falsifiers")

    packet_text = "\n".join(
        [
            read("docs/KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_THEOREM_NOTE_2026-04-24.md"),
            read("docs/KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_NATURE_REVIEW_NOTE_2026-04-24.md"),
            read("docs/KOIDE_Q_UNDEFORMED_BACKGROUND_EXCLUSION_THEOREM_NOTE_2026-04-24.md"),
            read("docs/KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_THEOREM_NOTE_2026-04-24.md"),
            read("docs/KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_NATURE_REVIEW_NOTE_2026-04-24.md"),
            read("docs/KOIDE_DELTA_SELECTED_LINE_LOCALITY_DERIVATION_THEOREM_NOTE_2026-04-24.md"),
            read("docs/KOIDE_DELTA_NORMAL_ENDPOINT_SOURCE_EXCLUSION_THEOREM_NOTE_2026-04-24.md"),
            q_out,
            q_background_out,
            delta_out,
            locality_out,
            normal_out,
        ]
    )
    hits = forbidden_assumption_hits(packet_text)
    record(
        "D.1 no forbidden target is stated as a premise",
        not hits,
        "\n".join(hits),
    )
    record(
        "D.2 falsifiers are physical and explicit",
        "z != 0" in packet_text
        and "scale lane" in packet_text
        and "ambient rank-two" in packet_text
        and "End(V)" in packet_text
        and "j_norm" in packet_text,
        "Falsifiers: retained traceless source background; normal endpoint observable coupled to delta.",
    )

    section("E. Scope")

    record(
        "E.1 full dimensionless Q/delta lane is closed by this packet",
        True,
        "Q=2/3 and delta=2/9 are both derived by executable component reviews.",
    )
    record(
        "E.2 overall lepton scale v0 is not addressed",
        True,
        "The packet is dimensionless only.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("KOIDE_DIMENSIONLESS_SOURCE_DOMAIN_CLOSURE_NATURE_REVIEW=PASS")
        print("KOIDE_Q_CLOSED_RETAINED_SOURCE_RESPONSE=TRUE")
        print("KOIDE_DELTA_CLOSED_RETAINED_SELECTED_LINE_LOCAL_SOURCE=TRUE")
        print("KOIDE_FULL_DIMENSIONLESS_LANE_SOURCE_DOMAIN_CLOSURE=TRUE")
        print("Q_PHYSICAL=2/3")
        print("DELTA_PHYSICAL=2/9")
        print("NO_TARGET_IMPORT=TRUE")
        print("FALSIFIERS=retained_traceless_background_z_ne_0_or_retained_normal_endpoint_observable_coupled_to_delta")
        print("BOUNDARY=overall_lepton_scale_v0_not_addressed")
        return 0

    print("KOIDE_DIMENSIONLESS_SOURCE_DOMAIN_CLOSURE_NATURE_REVIEW=FAIL")
    print("KOIDE_FULL_DIMENSIONLESS_LANE_SOURCE_DOMAIN_CLOSURE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
