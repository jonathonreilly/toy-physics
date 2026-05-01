#!/usr/bin/env python3
"""
Direct Wilson-loop alpha_s gate for the Cl(3)/Z^3 Wilson gauge surface.

This runner is intentionally strict.  It does not derive alpha_s from
alpha_bare/u0, alpha_LM, or the plaquette.  A retained result must be supplied
as a Wilson-loop/static-potential measurement certificate produced by an
independent production run.

Default behavior fails if no production certificate is present.  That is the
correct audit outcome until the framework has measured the static potential
with enough statistics, volumes, and scale-setting information to support the
claimed alpha_s(M_Z) number.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = REPO_ROOT / "outputs" / "alpha_s_direct_wilson_loop_certificate_2026-04-30.json"

ALPHA_S_TARGET = 0.1181
PDG_ALPHA_S_MZ = 0.1180
PDG_SIGMA = 0.0009
CF_SU3 = 4.0 / 3.0

FORBIDDEN_AUTHORITY_KEYS = {
    "alpha_bare_over_u0_squared",
    "alpha_lm",
    "u0",
    "mean_link",
    "plaquette_authority",
    "alpha_s_v_definition",
}


class Gate:
    def __init__(self) -> None:
        self.pass_count = 0
        self.fail_count = 0

    def check(self, name: str, condition: bool, detail: str = "", kind: str = "RETAINED-GATE") -> bool:
        status = "PASS" if condition else "FAIL"
        if condition:
            self.pass_count += 1
        else:
            self.fail_count += 1
        suffix = f"  ({detail})" if detail else ""
        print(f"  [{status}] [{kind}] {name}{suffix}")
        return condition


def load_certificate(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("certificate root must be a JSON object")
    return data


def collect_forbidden_paths(obj: Any, prefix: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_l = str(key).lower()
            if key_l in FORBIDDEN_AUTHORITY_KEYS:
                hits.append(f"{prefix}.{key}")
            hits.extend(collect_forbidden_paths(value, f"{prefix}.{key}"))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            hits.extend(collect_forbidden_paths(value, f"{prefix}[{i}]"))
    return hits


def positive_finite(x: Any) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(float(x)) and float(x) > 0


def ensemble_volume(ensemble: dict[str, Any]) -> int | None:
    dims = ensemble.get("dims")
    if isinstance(dims, list) and dims and all(isinstance(v, int) and v > 0 for v in dims):
        vol = 1
        for v in dims:
            vol *= v
        return vol
    L = ensemble.get("L")
    ndim = ensemble.get("ndim", 4)
    if isinstance(L, int) and isinstance(ndim, int) and L > 0 and ndim > 0:
        return L**ndim
    return None


def validate_metadata(gate: Gate, data: dict[str, Any]) -> None:
    metadata = data.get("metadata", {})
    gate.check(
        "certificate declares Wilson-loop/static-potential authority",
        metadata.get("authority") == "wilson_loop_static_potential",
        f"authority={metadata.get('authority')!r}",
    )
    gate.check(
        "certificate declares g_bare = 1 Wilson gauge surface",
        abs(float(metadata.get("g_bare", float("nan"))) - 1.0) < 1e-12
        and metadata.get("action") in {"SU3_Wilson", "Cl3Z3_SU3_Wilson"},
        f"action={metadata.get('action')!r}, g_bare={metadata.get('g_bare')!r}",
    )
    gate.check(
        "certificate declares no alpha_LM/u0/plaquette-chain authority",
        metadata.get("uses_alpha_lm_chain") is False
        and metadata.get("uses_alpha_bare_over_u0_squared") is False
        and metadata.get("uses_plaquette_as_running_coupling_input") is False,
        "all three flags must be false",
    )

    forbidden = collect_forbidden_paths(data)
    gate.check(
        "certificate does not expose forbidden authority keys",
        not forbidden,
        ", ".join(forbidden[:5]) if forbidden else "no forbidden keys",
    )


def validate_ensembles(gate: Gate, data: dict[str, Any]) -> None:
    ensembles = data.get("ensembles")
    gate.check("certificate contains ensemble list", isinstance(ensembles, list) and len(ensembles) > 0)
    if not isinstance(ensembles, list):
        return

    volumes = []
    spacings = []
    loops_with_stats = 0
    plateau_ok = 0
    potential_points = 0
    alpha_points = 0
    r0_values = []
    scale_setting = data.get("scale_setting", {})
    global_r0 = None
    if isinstance(scale_setting, dict):
        candidate = scale_setting.get("global_r0_over_a")
        if positive_finite(candidate):
            global_r0 = float(candidate)

    for ensemble in ensembles:
        if not isinstance(ensemble, dict):
            continue
        vol = ensemble_volume(ensemble)
        if vol:
            volumes.append(vol)
        a_fm = ensemble.get("a_fm")
        if positive_finite(a_fm):
            spacings.append(round(float(a_fm), 6))

        wilson_loops = ensemble.get("wilson_loops", [])
        if isinstance(wilson_loops, list):
            for loop in wilson_loops:
                if not isinstance(loop, dict):
                    continue
                mean = loop.get("mean")
                stderr = loop.get("stderr")
                n_cfg = loop.get("n_cfg")
                rel_err = abs(float(stderr) / float(mean)) if positive_finite(mean) and positive_finite(stderr) else float("inf")
                if isinstance(n_cfg, int) and n_cfg >= 500 and rel_err <= 0.05:
                    loops_with_stats += 1

        potential = ensemble.get("static_potential", [])
        if isinstance(potential, list):
            potential_points += len([p for p in potential if isinstance(p, dict) and positive_finite(p.get("R_over_a"))])
            for p in potential:
                if not isinstance(p, dict):
                    continue
                if p.get("plateau_pass") is True and float(p.get("plateau_chi2_dof", 99.0)) <= 2.0:
                    plateau_ok += 1

        running = ensemble.get("running_coupling", [])
        if isinstance(running, list):
            for p in running:
                if isinstance(p, dict) and positive_finite(p.get("mu_GeV")) and positive_finite(p.get("alpha_qq")):
                    alpha_points += 1

        r0_over_a = ensemble.get("r0_over_a")
        if positive_finite(r0_over_a):
            r0_values.append(float(r0_over_a))

    gate.check(
        "Wilson configurations cover at least three lattice volumes",
        len(set(volumes)) >= 3,
        f"volumes={sorted(set(volumes))}",
    )
    gate.check(
        "scale-control certificate covers at least two lattice spacings",
        len(set(spacings)) >= 2,
        f"a_fm={sorted(set(spacings))}",
    )
    gate.check(
        "Wilson-loop expectation values converge with statistics",
        loops_with_stats >= 12,
        f"qualified loops={loops_with_stats}",
    )
    gate.check(
        "static-potential extraction passes plateau tests",
        plateau_ok >= 6 and potential_points >= plateau_ok,
        f"plateau_ok={plateau_ok}, potential_points={potential_points}",
    )
    gate.check(
        "running coupling extracted at multiple scales",
        alpha_points >= 4,
        f"alpha_qq points={alpha_points}",
    )
    gate.check(
        "Sommer scale fit is in the standard beta=6 range",
        (bool(r0_values) and all(5.0 <= x <= 5.8 for x in r0_values))
        or (
            global_r0 is not None
            and 5.0 <= global_r0 <= 5.8
            and isinstance(scale_setting, dict)
            and scale_setting.get("mode") == "fixed_g_bare_global_sommer_fit"
        ),
        f"r0/a={r0_values}, global_r0/a={global_r0}",
    )


def validate_result(gate: Gate, data: dict[str, Any]) -> None:
    result = data.get("result", {})
    if not isinstance(result, dict):
        gate.check("result block exists", False)
        return

    alpha = result.get("alpha_s_MZ")
    uncertainties = result.get("uncertainties", {})
    if isinstance(uncertainties, dict):
        total_unc = result.get("total_uncertainty")
        if total_unc is None:
            total_unc = math.sqrt(
                sum(float(v) ** 2 for v in uncertainties.values() if isinstance(v, (int, float)) and v >= 0)
            )
    else:
        total_unc = None

    gate.check(
        "alpha_s(M_Z) result is a positive finite number",
        positive_finite(alpha),
        f"alpha_s_MZ={alpha!r}",
    )
    if not positive_finite(alpha):
        return

    alpha_f = float(alpha)
    gate.check(
        "full uncertainty budget includes all required components",
        isinstance(uncertainties, dict)
        and {"statistical", "finite_volume", "finite_spacing", "scale_setting", "running_bridge"}
        <= set(uncertainties),
        f"components={sorted(uncertainties) if isinstance(uncertainties, dict) else 'missing'}",
    )
    gate.check(
        "total uncertainty is finite and nonzero",
        positive_finite(total_unc),
        f"total_uncertainty={total_unc}",
    )
    gate.check(
        "final alpha_s(M_Z) is within one PDG sigma",
        abs(alpha_f - PDG_ALPHA_S_MZ) <= PDG_SIGMA,
        f"alpha={alpha_f:.6f}, PDG={PDG_ALPHA_S_MZ:.6f}+/-{PDG_SIGMA:.6f}",
    )
    gate.check(
        "candidate agrees with target 0.1181 within stated uncertainty",
        positive_finite(total_unc) and abs(alpha_f - ALPHA_S_TARGET) <= max(float(total_unc), 1e-12),
        f"alpha={alpha_f:.6f}, target={ALPHA_S_TARGET:.6f}, sigma={total_unc}",
    )


def validate_cross_check(gate: Gate, data: dict[str, Any]) -> None:
    cross = data.get("consistency_cross_check", {})
    if not isinstance(cross, dict):
        gate.check("alpha_LM/u0 chain is recorded only as consistency cross-check", False, "missing cross-check block")
        return

    direct = data.get("result", {}).get("alpha_s_MZ")
    old = cross.get("alpha_s_MZ_existing_chain")
    authority = cross.get("used_as_authority")
    gate.check(
        "alpha_LM/u0 chain is not used as authority",
        authority is False,
        f"used_as_authority={authority!r}",
    )
    gate.check(
        "existing alpha_LM/u0 chain numerically cross-checks the direct result",
        positive_finite(direct) and positive_finite(old) and abs(float(direct) - float(old)) <= 0.001,
        f"direct={direct!r}, existing={old!r}",
        kind="CONSISTENCY-ONLY",
    )


def print_missing_certificate(path: Path) -> None:
    print("\nSTRICT GATE BLOCKED")
    print(f"  Missing production certificate: {path}")
    print("\nRequired certificate schema, in outline:")
    print("  metadata.authority = 'wilson_loop_static_potential'")
    print("  metadata.action in {'SU3_Wilson', 'Cl3Z3_SU3_Wilson'}")
    print("  metadata.g_bare = 1.0")
    print("  metadata.uses_alpha_lm_chain = false")
    print("  metadata.uses_alpha_bare_over_u0_squared = false")
    print("  metadata.uses_plaquette_as_running_coupling_input = false")
    print("  ensembles[] with dims/L, a_fm, r0_over_a, wilson_loops[], static_potential[], running_coupling[]")
    print("  result.alpha_s_MZ plus statistical/finite_volume/finite_spacing/scale_setting/running_bridge uncertainties")
    print("  consistency_cross_check.alpha_s_MZ_existing_chain, used_as_authority=false")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificate",
        type=Path,
        default=DEFAULT_CERTIFICATE,
        help="Path to a production Wilson-loop/static-potential JSON certificate.",
    )
    parser.add_argument(
        "--print-template",
        action="store_true",
        help="Print a minimal JSON template and exit successfully.",
    )
    parser.add_argument(
        "--scout",
        action="store_true",
        help="Run a tiny Monte Carlo smoke test. This is infrastructure-only and not theorem evidence.",
    )
    parser.add_argument("--scout-volumes", default="2,3", help="Comma-separated L values for --scout.")
    parser.add_argument("--scout-therm", type=int, default=2, help="Thermalization sweeps for --scout.")
    parser.add_argument("--scout-meas", type=int, default=2, help="Measurement sweeps for --scout.")
    parser.add_argument("--seed", type=int, default=20260430, help="Random seed for --scout.")
    return parser.parse_args()


def template() -> dict[str, Any]:
    return {
        "metadata": {
            "authority": "wilson_loop_static_potential",
            "action": "Cl3Z3_SU3_Wilson",
            "g_bare": 1.0,
            "uses_alpha_lm_chain": False,
            "uses_alpha_bare_over_u0_squared": False,
            "uses_plaquette_as_running_coupling_input": False,
            "scale_anchor": "Sommer r0 in physical units",
            "running_bridge": "standard QCD beta function to M_Z",
        },
        "ensembles": [],
        "result": {
            "alpha_s_MZ": None,
            "uncertainties": {
                "statistical": None,
                "finite_volume": None,
                "finite_spacing": None,
                "scale_setting": None,
                "running_bridge": None,
            },
            "total_uncertainty": None,
        },
        "consistency_cross_check": {
            "alpha_s_MZ_existing_chain": 0.1181,
            "used_as_authority": False,
        },
    }


def random_su3_near_identity(rng: np.random.Generator, epsilon: float = 0.20) -> np.ndarray:
    """Generate a small SU(3) proposal by QR-projecting a traceless kick."""
    h = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    h = (h + h.conj().T) / 2.0
    h -= np.trace(h) * np.eye(3) / 3.0
    x = np.eye(3, dtype=complex) + 1j * epsilon * h
    q, r = np.linalg.qr(x)
    d = np.diag(r)
    phase = d / np.abs(d)
    q = q @ np.diag(np.conj(phase))
    det = np.linalg.det(q)
    q *= np.exp(-1j * np.angle(det) / 3.0)
    return q


def cold_links(lattice_size: int, ndim: int) -> dict[tuple[int, ...], list[np.ndarray]]:
    links: dict[tuple[int, ...], list[np.ndarray]] = {}
    for coords in np.ndindex(*([lattice_size] * ndim)):
        links[coords] = [np.eye(3, dtype=complex) for _ in range(ndim)]
    return links


def shifted(x: list[int], mu: int, step: int, lattice_size: int) -> list[int]:
    y = list(x)
    y[mu] = (y[mu] + step) % lattice_size
    return y


def compute_staple(
    links: dict[tuple[int, ...], list[np.ndarray]],
    x: list[int],
    mu: int,
    lattice_size: int,
    ndim: int,
) -> np.ndarray:
    staple = np.zeros((3, 3), dtype=complex)
    xp = shifted(x, mu, +1, lattice_size)
    for nu in range(ndim):
        if nu == mu:
            continue
        xpn = shifted(x, nu, +1, lattice_size)
        xm = shifted(x, nu, -1, lattice_size)
        xpm = shifted(xp, nu, -1, lattice_size)
        staple += (
            links[tuple(xp)][nu]
            @ links[tuple(xpn)][mu].conj().T
            @ links[tuple(x)][nu].conj().T
        )
        staple += (
            links[tuple(xpm)][nu].conj().T
            @ links[tuple(xm)][mu].conj().T
            @ links[tuple(xm)][nu]
        )
    return staple


def metropolis_sweep(
    links: dict[tuple[int, ...], list[np.ndarray]],
    lattice_size: int,
    ndim: int,
    beta: float,
    rng: np.random.Generator,
) -> tuple[int, int]:
    accepted = 0
    total = 0
    for coords in np.ndindex(*([lattice_size] * ndim)):
        x = list(coords)
        for mu in range(ndim):
            old = links[coords][mu]
            staple = compute_staple(links, x, mu, lattice_size, ndim)
            proposal = random_su3_near_identity(rng) @ old
            d_s = -(beta / 3.0) * np.trace((proposal - old) @ staple).real
            total += 1
            if d_s < 0.0 or rng.random() < math.exp(-min(d_s, 700.0)):
                links[coords][mu] = proposal
                accepted += 1
    return accepted, total


def single_wilson_loop(
    links: dict[tuple[int, ...], list[np.ndarray]],
    start: tuple[int, ...],
    r: int,
    t: int,
    spatial_dir: int,
    time_dir: int,
    lattice_size: int,
) -> float:
    w = np.eye(3, dtype=complex)
    x = list(start)
    for _ in range(r):
        w = w @ links[tuple(x)][spatial_dir]
        x[spatial_dir] = (x[spatial_dir] + 1) % lattice_size
    for _ in range(t):
        w = w @ links[tuple(x)][time_dir]
        x[time_dir] = (x[time_dir] + 1) % lattice_size
    for _ in range(r):
        x[spatial_dir] = (x[spatial_dir] - 1) % lattice_size
        w = w @ links[tuple(x)][spatial_dir].conj().T
    for _ in range(t):
        x[time_dir] = (x[time_dir] - 1) % lattice_size
        w = w @ links[tuple(x)][time_dir].conj().T
    return float(np.trace(w).real / 3.0)


def measure_loop_average(
    links: dict[tuple[int, ...], list[np.ndarray]],
    lattice_size: int,
    ndim: int,
    r: int,
    t: int,
) -> float:
    time_dir = ndim - 1
    total = 0.0
    count = 0
    for coords in np.ndindex(*([lattice_size] * ndim)):
        for spatial_dir in range(ndim - 1):
            total += single_wilson_loop(links, coords, r, t, spatial_dir, time_dir, lattice_size)
            count += 1
    return total / count


def run_scout(args: argparse.Namespace) -> int:
    gate = Gate()
    rng = np.random.default_rng(args.seed)
    volumes = [int(v) for v in args.scout_volumes.split(",") if v.strip()]
    print("=" * 78)
    print("Direct Wilson-loop alpha_s infrastructure scout")
    print("=" * 78)
    print("SCOUT ONLY: this does not certify alpha_s(M_Z).")
    print(f"volumes={volumes}, therm={args.scout_therm}, meas={args.scout_meas}, ndim=4, beta=6")

    all_generated = True
    all_finite = True
    potential_points = 0

    for lattice_size in volumes:
        links = cold_links(lattice_size, 4)
        accepted = 0
        total = 0
        for _ in range(args.scout_therm):
            a, n = metropolis_sweep(links, lattice_size, 4, 6.0, rng)
            accepted += a
            total += n
        loops: dict[tuple[int, int], list[float]] = {(1, 1): [], (1, 2): [], (2, 1): []}
        for _ in range(args.scout_meas):
            a, n = metropolis_sweep(links, lattice_size, 4, 6.0, rng)
            accepted += a
            total += n
            for key in loops:
                loops[key].append(measure_loop_average(links, lattice_size, 4, key[0], key[1]))

        means = {key: float(np.mean(vals)) for key, vals in loops.items()}
        finite = all(math.isfinite(v) for v in means.values())
        all_finite = all_finite and finite
        all_generated = all_generated and total > 0
        acc_rate = accepted / total if total else 0.0
        v_eff = None
        if means[(1, 1)] > 0 and means[(1, 2)] > 0:
            v_eff = -math.log(means[(1, 2)] / means[(1, 1)])
            potential_points += 1
        print(
            f"  L={lattice_size}: acc={acc_rate:.3f}, "
            f"W11={means[(1, 1)]:.6f}, W12={means[(1, 2)]:.6f}, "
            f"W21={means[(2, 1)]:.6f}, Veff(R=1)={v_eff if v_eff is not None else 'n/a'}"
        )
        gate.check(
            f"L={lattice_size} configurations generated",
            total > 0 and 0.0 < acc_rate < 1.0,
            f"updates={total}, acceptance={acc_rate:.3f}",
            kind="SCOUT-ONLY",
        )
        gate.check(
            f"L={lattice_size} Wilson loops finite",
            finite,
            f"means={means}",
            kind="SCOUT-ONLY",
        )

    gate.check(
        "scout covers multiple volumes",
        len(set(volumes)) >= 2 and all_generated,
        f"volumes={volumes}",
        kind="SCOUT-ONLY",
    )
    gate.check(
        "scout produces at least one effective-potential point",
        all_finite and potential_points > 0,
        f"potential_points={potential_points}",
        kind="SCOUT-ONLY",
    )
    print(f"\nSCOUT SUMMARY: PASS={gate.pass_count}  FAIL={gate.fail_count}")
    return 0 if gate.fail_count == 0 else 1


def main() -> int:
    args = parse_args()
    if args.print_template:
        print(json.dumps(template(), indent=2, sort_keys=True))
        return 0
    if args.scout:
        return run_scout(args)

    gate = Gate()
    print("=" * 78)
    print("Direct Wilson-loop alpha_s(M_Z) strict audit gate")
    print("=" * 78)
    print(f"certificate: {args.certificate}")

    try:
        data = load_certificate(args.certificate)
    except FileNotFoundError:
        print_missing_certificate(args.certificate)
        gate.check("production Wilson-loop certificate is present", False, str(args.certificate))
        print(f"\nSUMMARY: PASS={gate.pass_count}  FAIL={gate.fail_count}")
        return 1
    except Exception as exc:
        gate.check("production Wilson-loop certificate can be parsed", False, repr(exc))
        print(f"\nSUMMARY: PASS={gate.pass_count}  FAIL={gate.fail_count}")
        return 1

    validate_metadata(gate, data)
    validate_ensembles(gate, data)
    validate_result(gate, data)
    validate_cross_check(gate, data)

    print(f"\nSUMMARY: PASS={gate.pass_count}  FAIL={gate.fail_count}")
    if gate.fail_count:
        return 1
    print("Strict gate passed: direct Wilson-loop alpha_s route is ready for audit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
