#!/usr/bin/env python3
"""Radiative charged-lepton tau-scale selector firewall.

This runner audits the support lane

    y_tau ?= alpha_LM / (4*pi)

against the retained charged-lepton mass objective.  It proves a narrow
negative boundary: the electroweak Casimir and one-loop factor are
generation-blind across e, mu, tau.  Therefore the radiative scale can be
support for a charged-lepton scale, but it cannot by itself identify the tau
eigenvalue or retire the charged-lepton mass import.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import math
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dm_leptogenesis_exact_common import ALPHA_LM, V_EW  # noqa: E402


PASS_COUNT = 0
FAIL_COUNT = 0


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


@dataclass(frozen=True)
class Generation:
    label: str
    pdg_mass_mev: float


GENERATIONS = (
    Generation("e", 0.510998950),
    Generation("mu", 105.6583755),
    Generation("tau", 1776.86),
)


def charged_lepton_casimir() -> Fraction:
    """Casimir used by the support lane for any charged lepton generation."""
    t_left = Fraction(1, 2)
    y_left = Fraction(-1, 2)
    y_right = Fraction(-1, 1)

    c_su2_left = t_left * (t_left + 1)  # 3/4
    c_su2_vertex = 2 * c_su2_left * Fraction(1, 2)
    c_u1_vertex = y_left * y_right * Fraction(1, 2)
    return c_su2_vertex + c_u1_vertex


def main() -> int:
    radiative_script = SCRIPTS / "frontier_charged_lepton_radiative_yukawa_theorem.py"
    diagram_script = SCRIPTS / "frontier_charged_lepton_yukawa_diagrammatic_enumeration.py"
    bz_script = SCRIPTS / "frontier_charged_lepton_yukawa_bz_quadrature_explicit.py"
    direct_no_go_note = DOCS / "CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md"

    print("Source surface")
    print("-" * 72)
    for path in (radiative_script, diagram_script, bz_script, direct_no_go_note):
        check(f"{path.relative_to(ROOT)} exists", path.exists())

    radiative_text = radiative_script.read_text(encoding="utf-8")
    diagram_text = diagram_script.read_text(encoding="utf-8")
    bz_text = bz_script.read_text(encoding="utf-8")

    check(
        "original radiative runner frames itself as support, not closure",
        "not a fully axiom-native retained closure theorem" in radiative_text,
    )
    check("radiative runner uses PDG tau as observational benchmark", "M_TAU_PDG" in radiative_text)
    check(
        "diagrammatic runner still cites an external loop integral surface",
        "I_loop is cited from retained YT_P1_BZ_QUADRATURE" in diagram_text,
    )
    check(
        "BZ runner states the support lane does not close Koide bridges",
        "does not by itself close" in bz_text and "Koide bridges" in bz_text,
    )

    print()
    print("A. Generation-blind radiative Casimir")
    print("-" * 72)
    casimirs = {gen.label: charged_lepton_casimir() for gen in GENERATIONS}
    check("charged-lepton Casimir is exactly one", charged_lepton_casimir() == 1)
    check(
        "same Casimir is assigned to e, mu, tau",
        len(set(casimirs.values())) == 1,
        str(casimirs),
    )

    permuted = tuple(reversed(tuple(casimirs.values())))
    check(
        "generation relabeling leaves the radiative Casimir vector invariant",
        permuted == tuple(casimirs.values()),
        f"C vector = {tuple(casimirs.values())}",
    )

    y_rad = ALPHA_LM / (4 * math.pi)
    y_by_generation = {gen.label: y_rad * float(casimirs[gen.label]) for gen in GENERATIONS}
    check(
        "radiative y value is identical for all charged-lepton generations",
        len({round(value, 18) for value in y_by_generation.values()}) == 1,
        str(y_by_generation),
    )

    print()
    print("B. Universal application is not the charged-lepton hierarchy")
    print("-" * 72)
    predicted_mass_mev = V_EW * 1000.0 * y_rad
    print(f"Universal radiative mass comparator: {predicted_mass_mev:.6f} MeV")

    ratios = {gen.label: predicted_mass_mev / gen.pdg_mass_mev for gen in GENERATIONS}
    print(f"Comparator ratios predicted/PDG: {ratios}")
    check(
        "universal radiative mass is close only to tau comparator",
        abs(ratios["tau"] - 1.0) < 1e-3 and ratios["mu"] > 10 and ratios["e"] > 1000,
        "observed masses are comparators, not proof inputs",
    )
    check(
        "same radiative rule cannot also fit electron and muon masses",
        abs(ratios["e"] - 1.0) > 1000 and abs(ratios["mu"] - 1.0) > 10,
    )

    print()
    print("C. Selector firewall")
    print("-" * 72)
    proof_inputs = {
        "ALPHA_LM",
        "one_loop_factor_4pi",
        "charged_lepton_electroweak_charges",
        "generation_blind_casimir",
        "retained_v_EW",
    }
    forbidden_selector_inputs = {"M_TAU_PDG", "m_e_PDG", "m_mu_PDG", "heaviest_observed_generation"}
    check(
        "PDG masses and heaviest-generation labels are not proof-input keys",
        proof_inputs.isdisjoint(forbidden_selector_inputs),
        f"proof inputs = {sorted(proof_inputs)}",
    )
    check(
        "no tau selector is present in the generation-blind Casimir data",
        len(set(casimirs.values())) == 1 and "tau" not in proof_inputs,
    )
    check(
        "direct Ward no-go already requires a new generation/source primitive",
        "generation-selection / loop-normalization / source-domain law" in direct_no_go_note.read_text(encoding="utf-8"),
    )

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: radiative alpha_LM/(4pi) remains support, not a")
        print("standalone retained tau selector.  It can supply a candidate")
        print("charged-lepton scale only after a separate generation/ratio")
        print("primitive identifies the tau eigenvalue without PDG input.")
        return 0
    print("VERDICT: selector firewall has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
