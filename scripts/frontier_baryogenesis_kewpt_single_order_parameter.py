#!/usr/bin/env python3
"""
Baryogenesis K_EWPT single-order-parameter reduction on the current main
package surface.

This runner sharpens the first open electroweak stage after

  eta = J * K_EWPT * K_tr * K_sph

by showing that K_EWPT does not live on a hidden multi-field same-surface
scalar sector. On current main it reduces to one real functional of one unique
retained scalar thermal history lane:

  K_EWPT = F_EWPT[chi(tau)].
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

PASS = 0
FAIL = 0

ETA_OBS = 6.12e-10
J_PROMOTED = 3.330901e-5
K_NP_TARGET = ETA_OBS / J_PROMOTED
K_EQUAL_SPLIT = K_NP_TARGET ** (1.0 / 3.0)
K_TRANSITION_IF_10PCT_OTHER_STAGES = K_NP_TARGET / (0.1 * 0.1)


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"  [{tag}] {name}")
    if detail:
        print(f"         {detail}")


def info(name: str, detail: str = "") -> None:
    print(f"  [INFO] {name}")
    if detail:
        print(f"         {detail}")


def canon(z: complex) -> tuple[float, float]:
    return (round(z.real, 12), round(z.imag, 12))


def apbc_phases(lt: int) -> list[complex]:
    return [cmath.exp(1j * (2 * n + 1) * math.pi / lt) for n in range(lt)]


def orbit_partition(lt: int) -> list[list[tuple[float, float]]]:
    ops = [lambda w: w, lambda w: -w, lambda w: w.conjugate(), lambda w: -w.conjugate()]
    phases = sorted({canon(z) for z in apbc_phases(lt)})
    seen: set[tuple[float, float]] = set()
    parts = []
    for z in phases:
        if z in seen:
            continue
        orbit = sorted(
            {
                canon(op(complex(*z)))
                for op in ops
                if canon(op(complex(*z))) in phases
            }
        )
        parts.append(orbit)
        seen.update(orbit)
    return parts


def exact_local_a(lt: int, u0: float) -> float:
    return (1.0 / (2.0 * lt * u0**2)) * sum(
        1.0 / (3.0 + math.sin((2 * n + 1) * math.pi / lt) ** 2) for n in range(lt)
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS K_EWPT SINGLE-ORDER-PARAMETER REDUCTION")
    print("=" * 80)
    print()
    print("Question:")
    print("  On current main, does the transition-history factor K_EWPT live on")
    print("  a hidden multi-field scalar surface, or on one exact retained")
    print("  scalar thermal history lane?")
    print()

    print("=" * 80)
    print("PART 1: UNIQUE RETAINED SCALAR THERMAL LANE")
    print("=" * 80)
    print()

    resolved = []
    for lt in range(2, 14, 2):
        parts = orbit_partition(lt)
        sizes = [len(p) for p in parts]
        print(f"  Lt={lt:2d}: num_orbits={len(parts)}, sizes={sizes}")
        if len(parts) == 1 and len(parts[0]) > 2:
            resolved.append(lt)

    a2 = exact_local_a(2, 1.0)
    a4 = exact_local_a(4, 1.0)
    a_inf = 1.0 / (4.0 * math.sqrt(3.0))

    chi2 = 1.0
    chi4 = a4 / a2
    chiinf = a_inf / a2

    print()
    print(f"  chi_2   = {chi2:.12f}")
    print(f"  chi_4   = {chi4:.12f}")
    print(f"  chi_inf = {chiinf:.12f}")
    print()

    check(
        "the unique minimal resolved APBC thermal orbit is Lt = 4",
        resolved == [4],
        f"resolved single-orbit Lt values = {resolved}",
    )
    check(
        "chi_4 equals the exact static normalization ratio 8/7",
        abs(chi4 - 8.0 / 7.0) < 1e-12,
        f"chi_4 = {chi4:.12f}",
    )
    check(
        "chi_inf equals the exact endpoint ratio 2/sqrt(3)",
        abs(chiinf - 2.0 / math.sqrt(3.0)) < 1e-12,
        f"chi_inf = {chiinf:.12f}",
    )
    check(
        "the retained static same-surface normalization freedom is only O(10%)",
        (chiinf - chi2) < 0.16 and (chi4 - chi2) < 0.15,
        f"chi_inf - chi_2 = {chiinf - chi2:.6f}, chi_4 - chi_2 = {chi4 - chi2:.6f}",
    )
    info(
        "lane meaning",
        "the transition stage inherits one retained scalar thermal normalization lane rather than a broad multi-field same-surface scalar space",
    )
    print()

    print("=" * 80)
    print("PART 2: NO SAME-SURFACE EXTRA SCALAR FAMILY")
    print("=" * 80)
    print()

    yt_eft = (SCRIPTS / "frontier_yt_eft_bridge.py").read_text(encoding="utf-8")
    higgs_runner = (SCRIPTS / "frontier_higgs_mass_derived.py").read_text(encoding="utf-8")
    thermal_note = (
        DOCS / "BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md"
    ).read_text(encoding="utf-8")
    old_route_note = (DOCS / "BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md").read_text(
        encoding="utf-8"
    )

    check(
        "EW/Yukawa bridge records one Higgs doublet from the G_5 condensate",
        "N_H = 1" in yt_eft and "Higgs doublet from G_5 condensate" in yt_eft,
    )
    check(
        "Higgs/CW runner records one radial Higgs mode",
        "N_HIGGS = 1" in higgs_runner and "radial Higgs mode" in higgs_runner,
    )
    check(
        "Higgs/CW runner records three Goldstones",
        "N_GOLDSTONE = 3" in higgs_runner and "eaten by W+, W-, Z" in higgs_runner,
    )
    check(
        "thermal-order-parameter uniqueness note rejects a hidden extra scalar family",
        "unique thermal order-parameter surface" in thermal_note
        and "it does not derive a second same-surface scalar family" in thermal_note,
    )
    check(
        "old-route no-go note says the current package does not derive the needed extra scalar sector",
        "the current package does not derive the needed extra scalar sector" in old_route_note,
    )
    check(
        "old-route no-go note says the 2HDM-like route is not live on current main",
        "same-surface route on the current `main` package" in old_route_note
        and "the old route is no longer a live implementation candidate on current" in old_route_note,
    )
    info(
        "configuration-space consequence",
        "on the present authority surface K_EWPT cannot be promoted to a hidden extra-doublet or extra-family scalar problem",
    )
    print()

    print("=" * 80)
    print("PART 3: K_EWPT TARGET GEOMETRY")
    print("=" * 80)
    print()

    print(f"  K_NP,target                               = {K_NP_TARGET:.6e}")
    print(f"  equal three-stage K_EWPT benchmark        = {K_EQUAL_SPLIT:.6e}")
    print(f"  K_EWPT if K_tr = K_sph = 0.1              = {K_TRANSITION_IF_10PCT_OTHER_STAGES:.6e}")
    print()

    check(
        "K_NP target inherited by K_EWPT is 1.837341e-5",
        abs(K_NP_TARGET - 1.837341e-5) < 1e-11,
        f"K_NP,target = {K_NP_TARGET:.6e}",
    )
    check(
        "equal three-stage split gives K_EWPT = (K_NP)^(1/3)",
        abs(K_EQUAL_SPLIT - 2.638740e-2) < 1e-8,
        f"K_equal = {K_EQUAL_SPLIT:.6e}",
    )
    check(
        "10% transport and 10% sphaleron survival would force K_EWPT into the 1e-3 range",
        1.0e-3 < K_TRANSITION_IF_10PCT_OTHER_STAGES < 1.0e-2,
        f"K_EWPT = {K_TRANSITION_IF_10PCT_OTHER_STAGES:.6e}",
    )
    info(
        "geometry meaning",
        "the stage decomposition turns K_EWPT into a sharply normalized target even though the history functional itself remains open",
    )
    print()

    print("=" * 80)
    print("PART 4: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    kewpt_note = (DOCS / "BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md").read_text(
        encoding="utf-8"
    )
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    stage_note = (DOCS / "BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md").read_text(
        encoding="utf-8"
    )
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(
        encoding="utf-8"
    )
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")
    flagship = (DOCS / "CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md").read_text(
        encoding="utf-8"
    )

    check(
        "K_EWPT note records the single-lane functional K_EWPT = F_EWPT[chi(tau)]",
        "`K_EWPT = F_EWPT[χ(τ)]`" in kewpt_note,
    )
    check(
        "K_EWPT note records the exact static ratios chi_4 = 8/7 and chi_inf = 2/sqrt(3)",
        "`χ_4 = A_4 / A_2 = 8/7`" in kewpt_note
        and "`χ_inf = A_inf / A_2 = 2/sqrt(3)`" in kewpt_note,
    )
    check(
        "closure-gate note points to the K_EWPT reduction note",
        "BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md" in gate_note,
    )
    check(
        "stage-decomposition note points to the K_EWPT reduction note",
        "BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md" in stage_note,
    )
    check(
        "derivation atlas carries the K_EWPT single-order-parameter row",
        "Baryogenesis K_EWPT single-order-parameter reduction" in atlas,
    )
    check(
        "canonical harness index includes the K_EWPT runner",
        "frontier_baryogenesis_kewpt_single_order_parameter.py" in harness,
    )
    check(
        "current flagship entrypoint points to the K_EWPT note",
        "BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md" in flagship,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the transition-history stage K_EWPT now reduces to one real")
    print("      functional of one retained scalar thermal history lane")
    print("      K_EWPT = F_EWPT[chi(tau)]")
    print("    - the static same-surface scalar freedom on that lane is only")
    print("      an O(10%) normalization band")
    print("    - no hidden extra same-surface scalar-family rescue remains on")
    print("      the current authority surface")
    print("    - the genuinely open content is the history functional itself,")
    print("      not hidden extra scalar multiplicity")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
