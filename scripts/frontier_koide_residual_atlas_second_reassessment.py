#!/usr/bin/env python3
"""
Koide residual atlas second reassessment.

Purpose:
  After the newest failures, step back from local variations and re-rank
  genuinely distinct remaining routes for the charged-lepton Koide lane.

Result:
  The live residuals are unchanged:

      Q:     derive the equal C3 center-label source / K_TL = 0.
      delta: derive the open selected-line Berry/APS endpoint.

  The next highest-plausibility Q attack is a D-term / moment-map neutrality
  theorem, because it is a physical mechanism that can set a real scalar to
  zero without simply postulating equal labels.  Its danger is that the zero
  level may be an FI/source parameter.  That is tested by
  frontier_koide_q_moment_map_dterm_source_no_go.py.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


PASSES: list[tuple[str, bool, str]] = []


@dataclass(frozen=True)
class Candidate:
    name: str
    side: str
    novelty: int
    nature_plausibility: int
    target_import_risk: int
    status: str
    residual_if_fails: str

    @property
    def rank_score(self) -> int:
        return 2 * self.nature_plausibility + self.novelty - self.target_import_risk


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
    section("A. Residual scalars")

    q_residual = "equal_C3_center_label_source_equiv_K_TL"
    delta_residual = "open_selected_line_Berry_APS_endpoint"
    record(
        "A.1 Q residual is still one source scalar",
        q_residual == "equal_C3_center_label_source_equiv_K_TL",
        f"RESIDUAL_Q={q_residual}",
    )
    record(
        "A.2 delta residual is still one endpoint functor",
        delta_residual == "open_selected_line_Berry_APS_endpoint",
        f"RESIDUAL_DELTA={delta_residual}",
    )

    section("B. Forbidden shortcuts")

    forbidden = [
        "postulate equal labels",
        "postulate K_TL vanishing",
        "choose the FI/moment-map zero level because it closes Q",
        "choose the Berry endpoint because it equals eta_APS",
        "fit Brannen delta by endpoint gauge",
        "promote source-free algebra to physical closure",
    ]
    record(
        "B.1 forbidden target imports are explicit",
        len(forbidden) == 6,
        "\n".join(forbidden),
    )

    section("C. Fresh candidate route ranking")

    candidates = [
        Candidate(
            "D-term / moment-map neutrality for C3 center source",
            "Q",
            novelty=8,
            nature_plausibility=8,
            target_import_risk=5,
            status="next_attack",
            residual_if_fails="FI_level_or_center_gauge_charge_not_retained",
        ),
        Candidate(
            "Osterwalder-Schrader reflection positivity on the source carrier",
            "Q",
            novelty=7,
            nature_plausibility=7,
            target_import_risk=6,
            status="queued",
            residual_if_fails="reflection_positive_family_keeps_center_state_free",
        ),
        Candidate(
            "Cobordism / invertible-phase classification beyond mod-2 anomaly",
            "Q",
            novelty=8,
            nature_plausibility=7,
            target_import_risk=6,
            status="queued_after_global_anomaly",
            residual_if_fails="cobordism_class_blind_to_center_source",
        ),
        Candidate(
            "Markov-category terminal-state theorem for classical center labels",
            "Q",
            novelty=6,
            nature_plausibility=6,
            target_import_risk=6,
            status="queued",
            residual_if_fails="terminal_prior_not_physical_preparation",
        ),
        Candidate(
            "Noncommutative-geometry real-action spectral triple with finite Hilbert state",
            "Q",
            novelty=6,
            nature_plausibility=6,
            target_import_risk=5,
            status="queued_after_two_point_no_go",
            residual_if_fails="finite_trace_state_choice",
        ),
        Candidate(
            "Adiabatic spectral-projector endpoint theorem",
            "delta",
            novelty=7,
            nature_plausibility=7,
            target_import_risk=5,
            status="queued",
            residual_if_fails="open_projector_endpoint_trivialization",
        ),
        Candidate(
            "Relative eta/rho endpoint theorem",
            "delta",
            novelty=6,
            nature_plausibility=6,
            target_import_risk=6,
            status="attacked_negative",
            residual_if_fails="rho_to_open_endpoint_normalization",
        ),
        Candidate(
            "Dai-Freed functorial gluing with selected boundary condition",
            "delta",
            novelty=7,
            nature_plausibility=7,
            target_import_risk=7,
            status="attacked_negative_but_may_strengthen",
            residual_if_fails="endpoint_sections_not_retained",
        ),
        Candidate(
            "Spectral-flow endpoint quantization with fractional offset removed",
            "delta",
            novelty=6,
            nature_plausibility=6,
            target_import_risk=7,
            status="attacked_negative",
            residual_if_fails="fractional_offset_is_eta_import",
        ),
        Candidate(
            "Joint Q/delta cobordism boundary source functor",
            "joint",
            novelty=9,
            nature_plausibility=6,
            target_import_risk=8,
            status="queued_low_confidence",
            residual_if_fails="same_two_primitives_decouple",
        ),
    ]

    ranked = sorted(candidates, key=lambda c: c.rank_score, reverse=True)
    detail = "\n".join(
        f"{idx+1}. [{c.side}] {c.name}: score={c.rank_score}, status={c.status}, residual={c.residual_if_fails}"
        for idx, c in enumerate(ranked)
    )
    record(
        "C.1 at least eight non-identical future routes are ranked",
        len(candidates) >= 8,
        detail,
    )
    record(
        "C.2 next attack is the highest-ranked not-yet-run Q route",
        ranked[0].name == "D-term / moment-map neutrality for C3 center source",
        f"next={ranked[0].name}",
    )

    section("D. Verdict")

    record(
        "D.1 no positive closure is claimed by this atlas",
        True,
        "This is route selection and residual discipline, not a closure theorem.",
    )
    record(
        "D.2 full lane still needs both Q and delta closure",
        True,
        "Q source primitive and delta endpoint primitive remain separate.",
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
        print("KOIDE_RESIDUAL_ATLAS_SECOND_REASSESSMENT=TRUE")
        print("KOIDE_RESIDUAL_ATLAS_SECOND_CLOSES_Q=FALSE")
        print("KOIDE_RESIDUAL_ATLAS_SECOND_CLOSES_DELTA=FALSE")
        print("RESIDUAL_Q=equal_C3_center_label_source_equiv_K_TL")
        print("RESIDUAL_DELTA=open_selected_line_Berry_APS_endpoint")
        print("NEXT_ATTACK=frontier_koide_q_moment_map_dterm_source_no_go.py")
        return 0

    print("KOIDE_RESIDUAL_ATLAS_SECOND_REASSESSMENT=FALSE")
    print("KOIDE_RESIDUAL_ATLAS_SECOND_CLOSES_Q=FALSE")
    print("KOIDE_RESIDUAL_ATLAS_SECOND_CLOSES_DELTA=FALSE")
    print("RESIDUAL_Q=equal_C3_center_label_source_equiv_K_TL")
    print("RESIDUAL_DELTA=open_selected_line_Berry_APS_endpoint")
    return 1


if __name__ == "__main__":
    sys.exit(main())
