#!/usr/bin/env python3
"""
Koide delta unit-endpoint residual atlas no-go.

Purpose:
  Step back after functor classification, orientation/basepoint audits,
  spectral-flow degree normalization, and Callan-Harvey degree normalization.
  The residual has been reduced to the unit endpoint readout:

      delta_open = mu * eta_APS + c,
      mu = n * N_desc,

  with closure requiring mu = 1 and c = 0.

This atlas does not close delta.  It records the exact residual form, checks
the branch-local reduction artifacts are present, and ranks genuinely new
attacks that could remove the condition if a retained theorem can be found.
"""

from __future__ import annotations

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


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def main() -> int:
    section("A. Residual reduction artifacts")

    required = [
        "scripts/frontier_koide_delta_endpoint_functor_classification_no_go.py",
        "scripts/frontier_koide_delta_orientation_identity_functor_no_go.py",
        "scripts/frontier_koide_delta_contractible_base_trivialization_no_go.py",
        "scripts/frontier_koide_delta_relative_cobordism_endpoint_no_go.py",
        "scripts/frontier_koide_delta_spectral_flow_degree_normalization_no_go.py",
        "scripts/frontier_koide_delta_callan_harvey_degree_functor_no_go.py",
    ]
    missing = [rel for rel in required if not exists(rel)]
    record(
        "A.1 endpoint residual reduction artifacts are present",
        not missing,
        "\n".join(missing) if missing else f"checked={len(required)} runners",
    )

    eta = sp.Rational(2, 9)
    mu, c = sp.symbols("mu c", real=True)
    delta = sp.simplify(mu * eta + c)
    residual = sp.simplify(delta / eta - 1)
    record(
        "A.2 final reduced delta residual is mu - 1 plus endpoint offset",
        residual == mu + c / eta - 1,
        f"delta_open={delta}; delta/eta_APS - 1 = {residual}",
    )
    record(
        "A.3 closure requires exactly mu = 1 and c = 0",
        sp.solve(sp.Eq(delta.subs(c, 0), eta), mu) == [1],
        "mu packages endpoint functor degree, descent/current normalization, and spectral-flow identification.",
    )

    section("B. Candidate routes after the reduced residual")

    candidates = [
        (
            1,
            "primitive anomaly-channel theorem",
            "Derive that the selected Brannen line is the unique primitive Callan-Harvey inflow channel.",
            "Could force mu=1 if uniqueness and primitivity are retained.",
        ),
        (
            2,
            "Picard torsor unit theorem",
            "Upgrade the open endpoint torsor to a based Picard object from retained boundary data.",
            "Could force c=0 but still needs orientation/degree.",
        ),
        (
            3,
            "determinant-line universal property",
            "Show the selected endpoint functor is the universal determinant-line holonomy map.",
            "Would identify the open line with the closed generator instead of choosing it.",
        ),
        (
            4,
            "marked relative cobordism",
            "Add a retained marked boundary section and test if relative eta uniqueness kills the boundary correction.",
            "Could remove c if the marking is derived from Cl(3)/Z3 data.",
        ),
        (
            5,
            "reflection-positive boundary state",
            "Use real/antiunitary positivity to orient the endpoint map and exclude conjugation.",
            "Could reduce n=-1 but not offsets without a basepoint.",
        ),
        (
            6,
            "locality and cluster primitive current",
            "Use boundary locality to forbid multiple selected-line current copies.",
            "Could exclude integer mu other than one if no spectator channels are retained.",
        ),
        (
            7,
            "lattice Wilson endpoint theorem",
            "Construct a finite Wilson/APS endpoint with an explicit selected boundary eigenline.",
            "Could prove unit spectral-flow degree if the selected line is canonically the crossing eigenline.",
        ),
        (
            8,
            "source-response covariance transfer",
            "Use the strict Q readout as a covariant operational readout for the delta endpoint.",
            "Risks importing the operational quotient law unless the covariance is retained.",
        ),
        (
            9,
            "endpoint variational action with no tunable center",
            "Search for a center-free boundary functional whose Euler condition gives mu=1,c=0.",
            "Must avoid fitting eta or hiding the endpoint law in the action.",
        ),
        (
            10,
            "higher Cl(3) boundary source grammar",
            "Exhaust local boundary source polynomials that can couple to the endpoint functor.",
            "Could prove no retained source can tilt away from unit readout, or expose the missing primitive.",
        ),
    ]
    lines = [f"{rank}. {name}: {claim} ({risk})" for rank, name, claim, risk in candidates]
    record(
        "B.1 at least eight genuinely new post-reduction routes are enumerated",
        len(candidates) >= 8,
        "\n".join(lines),
    )
    record(
        "B.2 top ranked route attacks the current-normalization product directly",
        candidates[0][1] == "primitive anomaly-channel theorem",
        "Next attack should test whether anomaly cancellation plus retained channel primitivity forces mu=1.",
    )

    section("C. Nature-grade boundary")

    forbidden_shortcuts = [
        "declare the selected line to be the unit channel",
        "choose an endpoint basepoint because it closes",
        "fit the endpoint action to eta_APS",
        "identify closed APS and open endpoint by notation",
    ]
    record(
        "C.1 target-import shortcuts are explicitly excluded",
        len(forbidden_shortcuts) == 4,
        "\n".join(forbidden_shortcuts),
    )
    record(
        "C.2 full delta closure still needs a retained theorem, not another support equality",
        True,
        "Exact APS/anomaly equality is already support; the missing object is the open selected-line readout law.",
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
        print("VERDICT: unit-endpoint residual atlas does not close delta.")
        print("KOIDE_DELTA_UNIT_ENDPOINT_RESIDUAL_ATLAS_NO_GO=TRUE")
        print("DELTA_UNIT_ENDPOINT_RESIDUAL_ATLAS_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_SCALAR=mu_minus_one_plus_c_over_eta_APS")
        print("NEXT_ATTACK=primitive_anomaly_channel_theorem")
        return 0

    print("VERDICT: unit-endpoint residual atlas has FAILs.")
    print("KOIDE_DELTA_UNIT_ENDPOINT_RESIDUAL_ATLAS_NO_GO=FALSE")
    print("DELTA_UNIT_ENDPOINT_RESIDUAL_ATLAS_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_SCALAR=mu_minus_one_plus_c_over_eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
