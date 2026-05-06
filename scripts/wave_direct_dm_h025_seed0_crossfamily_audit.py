#!/usr/bin/env python3
"""Audit runner for the H=0.25 seed-0 direct-dM cross-family note.

The runner computes the two stated family/seed control ladders directly from
the matched-history harness.  It checks only the bounded claims made by the
note: exact nulls, common negative weak-field sign, within-family weak-field
control, and the Fam1/Fam2 ordering at the listed source strength.
"""

from __future__ import annotations

# Heavy compute runner.  The two-family H=0.25 ladder uses the same expensive
# wave/beam propagator as wave_direct_dm_h025_control_batch.py.
AUDIT_TIMEOUT_SEC = 1800

import gc
from statistics import mean

from wave_direct_dm_matched_history_probe import FAMILIES
from wave_retardation_continuum_limit import (
    IZ_END_PHYS,
    IZ_START_PHYS,
    K_PER_H,
    PW_PHYS,
    SRC_LAYER_FRAC,
    T_PHYS_LAYERS,
    cz,
    grow,
    prop_beam,
    solve_wave,
)


H_VALUE = 0.25
SEED = 0
STRENGTHS = (0.0, 0.002, 0.004, 0.008)
FAMILY_LABELS = ("Fam1", "Fam2")
MAX_SPREAD = 0.08
TARGET_STRENGTH = 0.004


def family_specs(label: str) -> tuple[str, float, float]:
    for family_label, drift, restore in FAMILIES:
        if family_label == label:
            return family_label, drift, restore
    raise SystemExit(f"unknown family label: {label}")


def shared_move_trace(iz_start: int, iz_end: int, move_steps: int) -> list[int]:
    if move_steps <= 1:
        return [iz_end]
    return [
        iz_start + int(round((iz_end - iz_start) * (u / (move_steps - 1))))
        for u in range(move_steps)
    ]


def make_early_move(iz_start: int, iz_end: int, src_layer: int, nl: int):
    active = nl - src_layer
    move_steps = max(2, active // 2)
    trace = shared_move_trace(iz_start, iz_end, move_steps)

    def iz_of_t(t: int) -> int:
        if t < src_layer:
            return iz_start
        u = t - src_layer
        if u < move_steps:
            return trace[u]
        return iz_end

    return iz_of_t


def make_late_move(iz_start: int, iz_end: int, src_layer: int, nl: int):
    active = nl - src_layer
    move_steps = max(2, active // 2)
    wait_steps = active - move_steps
    trace = shared_move_trace(iz_start, iz_end, move_steps)

    def iz_of_t(t: int) -> int:
        if t < src_layer:
            return iz_start
        u = t - src_layer
        if u < wait_steps:
            return iz_start
        v = u - wait_steps
        if v < move_steps:
            return trace[v]
        return trace[-1]

    return iz_of_t


def measure_row(h_value: float, strength: float, family_label: str, drift: float, restore: float, seed: int) -> dict:
    """Compute one row from the live lattice configuration and wave histories."""
    nl = round(T_PHYS_LAYERS / h_value)
    pw = round(PW_PHYS / h_value) * h_value
    k_phase = K_PER_H / h_value
    src_layer = round(SRC_LAYER_FRAC * nl)
    if nl - src_layer < 4:
        raise SystemExit(f"insufficient active layers for H={h_value}")

    iz_start = round(IZ_START_PHYS / h_value)
    iz_end = round(IZ_END_PHYS / h_value)

    # Build the grown lattice configuration, free beam, two source histories,
    # and retarded-wave beam responses.  The printed row is not imported from
    # a frozen table or target-value dictionary.
    pos, adj, nmap = grow(seed, drift, restore, nl, pw, 3, h_value)
    free = prop_beam(pos, adj, nmap, None, k_phase, nl, pw, h_value)
    z_free = cz(free, pos, nl, pw, h_value)

    early = make_early_move(iz_start, iz_end, src_layer, nl)
    late = make_late_move(iz_start, iz_end, src_layer, nl)
    h_early = solve_wave(nl, pw, h_value, strength, early, src_layer)
    h_late = solve_wave(nl, pw, h_value, strength, late, src_layer)

    d_early = (
        cz(prop_beam(pos, adj, nmap, h_early, k_phase, nl, pw, h_value), pos, nl, pw, h_value)
        - z_free
    )
    d_late = (
        cz(prop_beam(pos, adj, nmap, h_late, k_phase, nl, pw, h_value), pos, nl, pw, h_value)
        - z_free
    )
    delta_hist = d_early - d_late
    r_hist = delta_hist / max(abs(d_early), abs(d_late), 1e-12)

    return {
        "H": h_value,
        "NL": nl,
        "PW": pw,
        "family": family_label,
        "drift": drift,
        "restore": restore,
        "seed": seed,
        "src_layer": src_layer,
        "iz_start_real": iz_start * h_value,
        "iz_end_real": iz_end * h_value,
        "strength": strength,
        "d_early": d_early,
        "d_late": d_late,
        "delta_hist": delta_hist,
        "r_hist": r_hist,
    }


def scaled_spread(rows: list[dict]) -> float:
    scaled = [r["delta_hist"] / r["strength"] for r in rows if r["strength"] > 0]
    return (max(abs(v) for v in scaled) - min(abs(v) for v in scaled)) / max(
        mean(abs(v) for v in scaled), 1e-12
    )


def sign_pattern(rows: list[dict]) -> str:
    out = []
    for r in rows:
        if r["strength"] <= 0:
            continue
        out.append("-" if r["delta_hist"] < 0 else "+" if r["delta_hist"] > 0 else "0")
    return " ".join(out)


def check(condition: bool, label: str, detail: str, counts: dict[str, int]) -> None:
    status = "PASS" if condition else "FAIL"
    counts[status] += 1
    print(f"{status}: {label}: {detail}")


def main() -> int:
    counts = {"PASS": 0, "FAIL": 0}
    by_family: dict[str, list[dict]] = {}

    print("=" * 108)
    print("WAVE DIRECT-DM H=0.25 SEED-0 CROSS-FAMILY AUDIT")
    print("=" * 108)
    print(f"families={','.join(FAMILY_LABELS)} seed={SEED} H={H_VALUE:.3f}")
    print(f"strengths={','.join(f'{s:.6f}' for s in STRENGTHS)}")
    print("Checks are bounded to the listed two families and do not assert a portability law.")
    print()

    for label in FAMILY_LABELS:
        family_label, drift, restore = family_specs(label)
        rows: list[dict] = []
        print(f"[family={family_label} drift={drift:.2f} restore={restore:.2f}]")
        for strength in STRENGTHS:
            r = measure_row(H_VALUE, strength, family_label, drift, restore, seed=SEED)
            rows.append(r)
            print(f"  [strength={strength:.6f}]")
            print(f"    NL={r['NL']}  PW={r['PW']:.3f}  src_layer={r['src_layer']}")
            print(f"    start_z_real={r['iz_start_real']:.3f}  end_z_real={r['iz_end_real']:.3f}")
            print(f"    dM(early)    = {r['d_early']:+.6f}")
            print(f"    dM(late)     = {r['d_late']:+.6f}")
            print(f"    delta_hist   = {r['delta_hist']:+.6f}")
            print(f"    R_hist       = {r['r_hist']:+.2%}")
            if strength <= 0:
                print("    null         = exact S=0 control")
            else:
                print(f"    delta_hist/s = {r['delta_hist'] / strength:+.6f}")
            gc.collect()
        by_family[family_label] = rows
        print()

    print("=" * 108)
    print("BOUNDED CHECKS")
    print("=" * 108)
    for family_label, rows in by_family.items():
        null_max = max(abs(r["delta_hist"]) for r in rows if r["strength"] == 0)
        spread = scaled_spread(rows)
        pattern = sign_pattern(rows)
        check(
            null_max <= 1e-12,
            f"{family_label} exact null",
            f"max |delta_hist| = {null_max:.3e}",
            counts,
        )
        check(
            pattern == "- - -",
            f"{family_label} weak-field sign",
            f"delta_hist sign pattern = {pattern}",
            counts,
        )
        check(
            spread <= MAX_SPREAD,
            f"{family_label} weak-field control",
            f"|delta_hist/s| spread = {spread:+.2%} <= {MAX_SPREAD:.2%}",
            counts,
        )

    fam1 = next(r for r in by_family["Fam1"] if r["strength"] == TARGET_STRENGTH)
    fam2 = next(r for r in by_family["Fam2"] if r["strength"] == TARGET_STRENGTH)
    check(
        abs(fam1["r_hist"]) < abs(fam2["r_hist"]),
        "S=0.004 R_hist ordering",
        f"|Fam1 R_hist|={abs(fam1['r_hist']):.2%} < |Fam2 R_hist|={abs(fam2['r_hist']):.2%}",
        counts,
    )
    check(
        abs(fam1["delta_hist"]) < abs(fam2["delta_hist"]),
        "S=0.004 delta_hist ordering",
        f"|Fam1 delta_hist|={abs(fam1['delta_hist']):.6f} < "
        f"|Fam2 delta_hist|={abs(fam2['delta_hist']):.6f}",
        counts,
    )
    check(
        abs(fam2["r_hist"]) - abs(fam1["r_hist"]) > 0.02,
        "no common amplitude collapse at S=0.004",
        f"|R_hist| gap = {abs(fam2['r_hist']) - abs(fam1['r_hist']):.2%}",
        counts,
    )

    print()
    print("=" * 108)
    print("SUMMARY")
    print("=" * 108)
    print(f"PASS={counts['PASS']} FAIL={counts['FAIL']}")
    print("Scoped conclusion: two-row seed-0 cross-family compression only.")
    print("Excluded: stable amplitude law, family-wide H=0.25 portability, Fam3 extrapolation.")
    return 0 if counts["FAIL"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
