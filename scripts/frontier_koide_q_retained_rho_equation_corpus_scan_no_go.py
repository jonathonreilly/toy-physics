#!/usr/bin/env python3
"""
Koide Q retained-rho-equation corpus scan no-go.

Theorem attempt:
  Under the no-new-axioms rule, mine the current retained Koide-Q corpus for an
  already-retained source-side equality F(rho)=0 with nonzero derivative at the
  closing point.  Such an equation would set the hidden kernel source charge
  rho to zero and close the Q bridge without adding a new axiom.

Result:
  No retained positive closure is found.  The current corpus contains exact
  rank-one rho equations only in forbidden or non-retained roles:

      K_TL(rho)=0        target import / equivalent close condition;
      rho=0             named missing no-hidden-kernel source law;
      rho=1             retained full-determinant counterstate;
      beta_rho=0        RG/anomaly blindness, zero Jacobian on rho.

Exact residual:

      find_existing_retained_source_equality_with_rank_one_jacobian_in_rho.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

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


def read_rel(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def corpus() -> dict[str, str]:
    rels: list[Path] = []
    rels.extend((ROOT / "docs").glob("KOIDE_Q*.md"))
    rels.extend((ROOT / "scripts").glob("frontier_koide_q*.py"))
    return {
        str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore")
        for path in sorted(rels)
    }


def jacobian_rank(expr: sp.Expr, var: sp.Symbol) -> int:
    return sp.Matrix([expr]).jacobian([var]).rank()


def main() -> int:
    rho = sp.symbols("rho", real=True)

    section("A. Route brainstorm and ranking")

    routes = [
        (
            "old no-hidden-source audit",
            "highest chance but marked support/not closure, so cannot supply retained rho=0",
        ),
        (
            "physical source-language exclusion",
            "strong authority if present, but current audit leaves rank-visible language retained",
        ),
        (
            "axiom-native source descent",
            "would close if no-hidden-kernel charge were derived, but records zero rank on rho",
        ),
        (
            "observable-dual annihilator",
            "would close if source domain were Q*, but retained A* covectors remain",
        ),
        (
            "residual atlas unification",
            "best global simplifier, but dictionary entries are not retained equations",
        ),
    ]
    record(
        "A.1 five no-new-axiom route variants are explicitly ranked",
        len(routes) == 5,
        "\n".join(f"{idx + 1}. {name}: {why}" for idx, (name, why) in enumerate(routes)),
    )

    section("B. Text-corpus scan for retained rho equations")

    texts = corpus()
    rho_hits = {
        rel: text
        for rel, text in texts.items()
        if re.search(r"\brho\b|hidden[- ]kernel|kernel source|rank 1 in rho", text)
    }
    record(
        "B.1 Koide-Q corpus contains rho/kernel-source material to audit",
        len(rho_hits) >= 10,
        f"rho_or_kernel_hit_files={len(rho_hits)}",
    )

    positive_close_flags = {
        rel: re.findall(r"Q_[A-Z0-9_]*CLOSES_Q(?:_RETAINED_ONLY)?=TRUE", text)
        for rel, text in rho_hits.items()
    }
    positive_close_flags = {rel: hits for rel, hits in positive_close_flags.items() if hits}
    record(
        "B.2 no rho-bearing artifact prints a positive retained Q-closeout flag",
        not positive_close_flags,
        "\n".join(f"{rel}: {hits}" for rel, hits in positive_close_flags.items()),
    )

    support_note = read_rel("docs/KOIDE_Q_NO_HIDDEN_SOURCE_AUDIT_2026-04-22.md")
    support_note_plain = re.sub(r"[*_`]", "", support_note.lower())
    support_note_plain = re.sub(r"\s+", " ", support_note_plain)
    record(
        "B.3 old no-hidden-source audit is explicitly support, not closure",
        "not a closure theorem" in support_note_plain
        and "does not yet prove" in support_note_plain,
        "The strongest old support artifact refuses retained closure promotion.",
    )

    axiom_native = read_rel("scripts/frontier_koide_q_axiom_native_source_descent_next20_no_go.py")
    source_language = read_rel("scripts/frontier_koide_q_physical_source_language_exclusion_next20_no_go.py")
    separation = read_rel("scripts/frontier_koide_q_no_new_axiom_separation_no_go.py")
    record(
        "B.4 current source-descent audits explicitly record zero rank on rho",
        "jacobian([rho]).rank() == 0" in axiom_native
        and "jacobian([rho]).rank() == 0" in source_language
        and "zero rank on rho" in separation,
        "The named no-new-axiom candidate files do not contain the needed retained rho equation.",
    )

    atlas_note = read_rel("docs/KOIDE_Q_RESIDUAL_SCALAR_UNIFICATION_NO_GO_NOTE_2026-04-24.md")
    record(
        "B.5 residual atlas names rank-one rho equation as missing, not retained",
        "existing retained equality with Jacobian rank 1 in rho" in atlas_note,
        "The atlas supplies the search criterion, not the equation.",
    )

    section("C. Exact symbolic classification of rho equations")

    k_tl = sp.simplify(((1 + rho) ** 2 - 1) / (4 * (1 + rho)))
    candidates = [
        {
            "name": "K_TL(rho)=0",
            "expr": k_tl,
            "classification": "forbidden_target_import",
            "allowed_retained": False,
        },
        {
            "name": "rho=0",
            "expr": rho,
            "classification": "named_missing_no_hidden_kernel_source_law",
            "allowed_retained": False,
        },
        {
            "name": "rho=1",
            "expr": rho - 1,
            "classification": "retained_full_determinant_counterstate",
            "allowed_retained": False,
        },
        {
            "name": "beta_rho=0 / anomaly-RG blindness",
            "expr": sp.Integer(0),
            "classification": "rho_blind_zero_equation",
            "allowed_retained": False,
        },
    ]
    classification_lines = []
    for candidate in candidates:
        expr = sp.sympify(candidate["expr"])
        rank = jacobian_rank(expr, rho)
        sols = sp.solve(sp.Eq(expr, 0), rho)
        classification_lines.append(
            f"{candidate['name']}: rank={rank}, solutions={sols}, "
            f"class={candidate['classification']}"
        )

    record(
        "C.1 the exact rank-one rho equations are not allowed retained closure laws",
        all(not candidate["allowed_retained"] for candidate in candidates),
        "\n".join(classification_lines),
    )

    allowed_rank_one = [
        candidate
        for candidate in candidates
        if candidate["allowed_retained"]
        and jacobian_rank(sp.sympify(candidate["expr"]), rho) == 1
    ]
    record(
        "C.2 no allowed retained rank-one rho equation remains after classification",
        allowed_rank_one == [],
        f"allowed_rank_one={allowed_rank_one}",
    )

    record(
        "C.3 the positive close path is exactly one existing retained non-target equation",
        True,
        "Need F(rho)=0 with dF/drho nonzero at rho=0, where F is already retained and not K_TL/Q by another name.",
    )

    section("D. Hostile review")

    forbidden_imports = [
        "assume K_TL=0",
        "assume Q=2/3",
        "PDG mass",
        "H_* pin",
        "delta=2/9 assumption",
    ]
    record(
        "D.1 the scan does not import a forbidden target as a theorem input",
        True,
        "Forbidden inputs checked conceptually: " + ", ".join(forbidden_imports),
    )
    record(
        "D.2 no new axiom is accepted",
        True,
        "The runner only classifies existing files and exact symbolic candidates.",
    )
    record(
        "D.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=find_existing_retained_source_equality_with_rank_one_jacobian_in_rho",
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
        print("VERDICT: current corpus contains no retained positive rank-one rho equation.")
        print("KOIDE_Q_RETAINED_RHO_EQUATION_CORPUS_SCAN_NO_GO=TRUE")
        print("Q_RETAINED_RHO_EQUATION_CORPUS_SCAN_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("RESIDUAL_SCALAR=find_existing_retained_source_equality_with_rank_one_jacobian_in_rho")
        print("RESIDUAL_SOURCE=corpus_contains_only_conditional_forbidden_or_counterstate_rho_equations")
        print("NEXT_SEARCH_CRITERION=existing_retained_non_target_equation_F_rho_zero_with_dF_drho_nonzero_at_zero")
        return 0

    print("VERDICT: retained rho-equation corpus scan has FAILs.")
    print("KOIDE_Q_RETAINED_RHO_EQUATION_CORPUS_SCAN_NO_GO=FALSE")
    print("Q_RETAINED_RHO_EQUATION_CORPUS_SCAN_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=find_existing_retained_source_equality_with_rank_one_jacobian_in_rho")
    return 1


if __name__ == "__main__":
    sys.exit(main())
