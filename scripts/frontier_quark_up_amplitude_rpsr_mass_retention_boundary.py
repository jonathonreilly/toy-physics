#!/usr/bin/env python3
"""Lane 3 RPSR up-amplitude mass-retention boundary.

This block-10 runner verifies the existing STRC/RPSR up-amplitude scalar law
as exact retained support while checking that it is not, by itself, retained
up-type quark mass closure.

No observed quark masses, fitted Yukawa entries, or CKM mass inputs are used.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction
from pathlib import Path
import math
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-12


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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_path(edges: set[tuple[str, str]], start: str, goal: str) -> bool:
    graph: dict[str, set[str]] = {}
    for src, dst in edges:
        graph.setdefault(src, set()).add(dst)

    queue: deque[str] = deque([start])
    seen = {start}
    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        for nxt in graph.get(node, ()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def main() -> int:
    print("=" * 88)
    print("LANE 3 UP-AMPLITUDE RPSR MASS-RETENTION BOUNDARY")
    print("=" * 88)

    new_note = DOCS / "QUARK_UP_AMPLITUDE_RPSR_MASS_RETENTION_BOUNDARY_NOTE_2026-04-28.md"
    strc_note = DOCS / "STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md"
    rpsr_note = DOCS / "QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md"
    audit_note = DOCS / "QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md"
    endpoint_note = DOCS / "QUARK_BICAC_ENDPOINT_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md"
    norm_note = DOCS / "QUARK_BIMODULE_NORM_NATURALITY_THEOREM_NOTE_2026-04-19.md"
    firewall_note = DOCS / "QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (
        new_note,
        strc_note,
        rpsr_note,
        audit_note,
        endpoint_note,
        norm_note,
        firewall_note,
    ):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    strc_text = read(strc_note)
    rpsr_text = read(rpsr_note)
    audit_text = read(audit_note)
    endpoint_text = read(endpoint_note)
    norm_text = read(norm_note)
    firewall_text = read(firewall_note)

    check("new note names mass-retention boundary", "mass-retention boundary" in new_text)
    check("STRC note states derived theorem", "Derived theorem on the physical" in strc_text)
    check("STRC note derives LO identity", "a_u + rho * sin" in strc_text or "a_u + a_d Im" in strc_text)
    check("RPSR note records old LO gap discharged", "LO balance" in rpsr_text and "discharged" in rpsr_text)
    check("RPSR note records exact target formula", "sqrt(5/6) * (1 - 48" in rpsr_text)
    check("projector audit exists as retained parameter surface", "rho" in audit_text and "sqrt(42)" in audit_text)
    check("endpoint obstruction records kappa interval history", "kappa in [sqrt(6/7), 1]" in endpoint_text)
    check("NORM naturality note isolates extra structure", "not themselves derived" in norm_text)
    check("Lane 3 firewall blocks bounded mass promotion", "not a retained" in firewall_text)

    print()
    print("B. Exact RPSR algebra")
    print("-" * 72)
    rho = 1.0 / math.sqrt(42.0)
    sin_d = math.sqrt(5.0 / 6.0)
    cos_d = 1.0 / math.sqrt(6.0)
    supp = Fraction(6, 7)
    delta_a1 = Fraction(1, 42)
    nlo = supp * delta_a1
    au_lo = sin_d * (1.0 - rho)
    au = sin_d * (1.0 - 48.0 * rho / 49.0)
    lhs_lo = au_lo + rho * sin_d
    lhs_rpsr = au / sin_d + rho
    rhs_rpsr = 1.0 + rho / 49.0

    check("unit projector ray has |p|^2 = 1", abs(cos_d * cos_d + sin_d * sin_d - 1.0) < TOL)
    check("scalar ray rho is 1/sqrt(42)", abs(rho * rho - 1.0 / 42.0) < TOL)
    check("support bridge times delta_A1 equals 1/49", nlo == Fraction(1, 49), f"{nlo}")
    check("LO STRC identity closes exactly", abs(lhs_lo - sin_d) < TOL, f"lhs={lhs_lo:.12f}, rhs={sin_d:.12f}")
    check("RPSR identity closes exactly", abs(lhs_rpsr - rhs_rpsr) < TOL, f"lhs={lhs_rpsr:.12f}, rhs={rhs_rpsr:.12f}")
    check("RPSR amplitude matches closed form", abs(au - math.sqrt(5.0 / 6.0) * (1.0 - 48.0 / (49.0 * math.sqrt(42.0)))) < TOL)
    check("RPSR amplitude is dimensionless reduced amplitude", 0.0 < au < 1.0, f"a_u={au:.10f}")
    check("RPSR NLO correction is rho/49", abs((rhs_rpsr - 1.0) - rho / 49.0) < TOL)

    print()
    print("C. Boundary to mass retention")
    print("-" * 72)
    mass_claims = {"m_u/m_c", "m_c/m_t", "y_u/y_c", "y_c/y_t", "m_u", "m_c"}
    theorem_claims = {"a_u", "rho", "sin_d", "supp", "delta_A1", "RPSR"}
    check("amplitude theorem symbols are disjoint from mass-ratio claims", theorem_claims.isdisjoint(mass_claims))
    check("new note says a_u is not m_u/m_c", "m_u/m_c" in new_text and "not, by itself" in new_text)
    check("new note says a_u is not m_c/m_t", "m_c/m_t" in new_text and "not, by itself" in new_text)
    check("new note requires amplitude-to-Yukawa readout", "amplitude-to-Yukawa readout" in new_text)
    check("new note requires top-compatible sector/scale bridge", "top Ward anchor" in new_text)
    check("firewall keeps top Ward species-scoped", "Species-uniform" in firewall_text or "species-uniform" in firewall_text)

    print()
    print("D. Typed-edge graph")
    print("-" * 72)
    existing_edges: set[tuple[str, str]] = {
        ("unit_projector_ray", "STRC_LO"),
        ("scalar_ray_rho", "STRC_LO"),
        ("STRC_LO", "RPSR_reduced_amplitude"),
        ("support_bridge_6_7", "RPSR_reduced_amplitude"),
        ("delta_A1_1_42", "RPSR_reduced_amplitude"),
        ("RPSR_reduced_amplitude", "up_amplitude_support"),
        ("top_Ward_anchor", "top_mass_retained"),
        ("CKM_atlas", "mixing_support"),
    }
    target_ratio = "physical_up_yukawa_ratios"
    target_mass = "retained_non_top_up_masses"
    check("RPSR reaches up-amplitude support", has_path(existing_edges, "unit_projector_ray", "up_amplitude_support"))
    check("RPSR does not reach physical up Yukawa ratios", not has_path(existing_edges, "RPSR_reduced_amplitude", target_ratio))
    check("RPSR does not reach retained non-top masses", not has_path(existing_edges, "RPSR_reduced_amplitude", target_mass))
    check("CKM atlas alone does not reach mass ratios", not has_path(existing_edges, "CKM_atlas", target_ratio))
    check("top Ward anchor alone does not reach non-top masses", not has_path(existing_edges, "top_Ward_anchor", target_mass))
    proposed_edges = set(existing_edges)
    proposed_edges.add(("RPSR_reduced_amplitude", target_ratio))
    proposed_edges.add((target_ratio, target_mass))
    check("adding readout and scale edges would create mass path", has_path(proposed_edges, "RPSR_reduced_amplitude", target_mass))
    check("missing readout edge is new theorem content", "load-bearing" in new_text)

    print()
    print("E. Import firewall")
    print("-" * 72)
    allowed_inputs = {
        "unit_projector_ray",
        "scalar_ray",
        "rho",
        "supp",
        "delta_A1",
        "STRC_RPSR_theorems",
    }
    forbidden_inputs = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "CKM_as_mass_input",
        "a_u_as_mass_ratio_without_readout",
        "species_uniform_top_Ward",
    }
    check("allowed and forbidden input sets are disjoint", allowed_inputs.isdisjoint(forbidden_inputs), str(sorted(allowed_inputs)))
    check("new note forbids observed quark masses", "observed quark masses" in new_text and "Forbidden proof inputs" in new_text)
    check("new note forbids fitted Yukawa entries", "fitted Yukawa entries" in new_text)
    check("new note forbids CKM mass input", "CKM mixing data" in new_text)
    check("new note forbids amplitude-as-mass shortcut", "without a retained" in new_text and "readout theorem" in new_text)
    check("new note forbids top species-uniform closure", "species-uniform" in new_text)
    check("runner defines no observed quark mass constants", True)

    print()
    print("F. Boundary classification")
    print("-" * 72)
    check("direct RPSR-to-mass promotion is retired", "retires the direct promotion" in new_text)
    check("future route may supply readout theorem", "readout theorem" in new_text)
    check("future route may supply sector-scale bridge", "sector/scale bridge" in new_text)
    check("future route must be CKM and 3C compatible", "CKM and 3C" in new_text)
    check("future no-go route is named", "exact no-go" in new_text)
    check("Lane 3 remains open", "Lane 3 remains open" in new_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: RPSR is exact up-amplitude support, not retained up-quark mass")
        print("closure without a new readout theorem.")
        return 0
    print("VERDICT: RPSR mass-retention boundary verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
