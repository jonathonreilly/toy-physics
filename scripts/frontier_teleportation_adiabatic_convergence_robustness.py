#!/usr/bin/env python3
"""Convergence and robustness audit for finite-time adiabatic teleportation prep.

Status: planning / first artifact. This is a bounded closed-system diagnostic
for ordinary quantum state teleportation resources only. It does not claim
matter transfer, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.

The default focus is the 2D 4x4 Poisson smoothstep candidate at T=40. The
runner tightens that row with fixed-step convergence, a propagator comparison,
same-budget schedule checks, small Hamiltonian/timing/control-noise
perturbations, a G=0 null control, and Bob pre-message input-independence.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_teleportation_adiabatic_prep_probe import AuditCase  # noqa: E402
from frontier_teleportation_adiabatic_time_evolution import (  # noqa: E402
    CaseData,
    EvolutionResult,
    Schedule,
    SCHEDULES,
    apply_step,
    build_case_data,
    chosen_method,
    fmt_float,
    logical_resource_from_state,
    no_signal_audit,
    resource_metrics,
)
from frontier_teleportation_resource_fidelity import (  # noqa: E402
    CLASSICAL_AVG_FIDELITY,
)


DEFAULT_DIM = 2
DEFAULT_SIDE = 4
DEFAULT_MASS = 0.0
DEFAULT_G = 1000.0
DEFAULT_RUNTIME = 40.0
DEFAULT_STEPS = 320
DEFAULT_METHOD = "expm_multiply"
DEFAULT_SCHEDULE = "smoothstep"


@dataclasses.dataclass(frozen=True)
class VariantRow:
    group: str
    label: str
    result: EvolutionResult
    target_phi_plus: float
    target_favg: float


def clamp01(value: float) -> float:
    return min(1.0, max(0.0, value))


def fmt_delta(value: float) -> str:
    if value == 0.0:
        return "+0"
    if abs(value) < 1e-3 or abs(value) >= 1e4:
        return f"{value:+.3e}"
    return f"{value:+.6f}"


def parse_float_list(raw: str, option_name: str) -> tuple[float, ...]:
    values: list[float] = []
    for item in raw.split(","):
        item = item.strip()
        if item:
            values.append(float(item))
    if not values:
        raise ValueError(f"{option_name} must include at least one value")
    return tuple(values)


def parse_int_list(raw: str, option_name: str) -> tuple[int, ...]:
    values = tuple(int(round(value)) for value in parse_float_list(raw, option_name))
    if any(value < 1 for value in values):
        raise ValueError(f"{option_name} must contain positive step counts")
    return values


def unique_sorted(values: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(sorted(dict.fromkeys(values)))


def unique_sorted_int(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(dict.fromkeys(values)))


def parse_schedules(raw: str) -> tuple[Schedule, ...]:
    names = tuple(item.strip() for item in raw.split(",") if item.strip())
    if not names:
        raise ValueError("--schedules must include at least one schedule")
    unknown = [name for name in names if name not in SCHEDULES]
    if unknown:
        raise ValueError(
            f"unknown schedule(s): {', '.join(unknown)}; "
            f"valid schedules are {', '.join(SCHEDULES)}"
        )
    return tuple(SCHEDULES[name] for name in names)


def make_case(label: str, mass: float, G: float) -> AuditCase:
    return AuditCase(label, dim=DEFAULT_DIM, side=DEFAULT_SIDE, mass=mass, G=G)


def evolve_fixed_steps(
    data: CaseData,
    schedule: Schedule,
    runtime: float,
    steps: int,
    method: str,
    *,
    schedule_label: str | None = None,
    control_noise_sigma: float = 0.0,
    noise_seed: int = 0,
) -> EvolutionResult:
    if runtime <= 0.0:
        raise ValueError("runtime must be positive")
    if steps < 1:
        raise ValueError("steps must be positive")
    if control_noise_sigma < 0.0:
        raise ValueError("control noise sigma must be nonnegative")

    step_method = chosen_method(method, data.h_initial.shape[0])
    dt = runtime / steps
    rng = np.random.default_rng(noise_seed)
    noise = (
        rng.normal(loc=0.0, scale=control_noise_sigma, size=steps)
        if control_noise_sigma > 0.0
        else np.zeros(steps, dtype=float)
    )

    if data.d_hamiltonian_norm <= 1e-14:
        psi = data.initial_state * np.exp(-1j * data.initial_energy * runtime)
    else:
        psi = data.initial_state.copy()
        for step in range(steps):
            u_mid = (step + 0.5) / steps
            s_mid = schedule.fn(float(u_mid))
            if control_noise_sigma > 0.0:
                endpoint_window = math.sin(math.pi * u_mid) ** 2
                s_mid += endpoint_window * float(noise[step])
            hamiltonian = data.h_initial + clamp01(float(s_mid)) * data.d_hamiltonian
            psi = apply_step(hamiltonian, psi, dt, step_method)

    final_norm = float(np.linalg.norm(psi))
    if final_norm <= 1e-15:
        raise ValueError(f"{data.case.label}: evolution produced a zero state")
    psi = psi / final_norm
    rho = logical_resource_from_state(psi, data.n_sites, data.case)
    ground_overlap = float(abs(np.vdot(data.target_ground, psi)) ** 2)
    final_energy = float(np.real(np.vdot(psi, data.h_target @ psi)))

    return EvolutionResult(
        case=data.case,
        schedule=schedule_label or schedule.name,
        runtime=runtime,
        steps=steps,
        dt=dt,
        method=step_method,
        final_norm_error=abs(final_norm - 1.0),
        final_ground_overlap=ground_overlap,
        diabatic_loss=max(0.0, 1.0 - ground_overlap),
        final_energy_excess=max(0.0, final_energy - data.target_energy),
        metrics=resource_metrics(rho),
        resource_rho=rho,
    )


def variant_row(group: str, label: str, data: CaseData, result: EvolutionResult) -> VariantRow:
    return VariantRow(
        group=group,
        label=label,
        result=result,
        target_phi_plus=data.target_metrics.phi_plus_overlap,
        target_favg=data.target_metrics.exact_avg_fidelity,
    )


def robustness_status(
    result: EvolutionResult,
    fidelity_threshold: float,
    loss_threshold: float,
) -> str:
    if (
        result.metrics.exact_avg_fidelity >= fidelity_threshold
        and result.diabatic_loss <= loss_threshold
    ):
        return "PASS"
    if result.metrics.exact_avg_fidelity >= fidelity_threshold:
        return "FIDELITY_ONLY"
    return "FRAGILE"


def null_control_clean(result: EvolutionResult, tolerance: float) -> bool:
    return (
        abs(result.case.G) <= tolerance
        and result.metrics.best_bell_overlap <= 0.5 + 10.0 * tolerance
        and result.metrics.negativity <= 10.0 * tolerance
        and result.metrics.exact_avg_fidelity <= CLASSICAL_AVG_FIDELITY + 10.0 * tolerance
    )


def print_setup(data: CaseData, args: argparse.Namespace) -> None:
    target = data.target_metrics
    print("FINITE-TIME ADIABATIC CONVERGENCE/ROBUSTNESS AUDIT")
    print("Status: planning / first artifact; ordinary quantum state teleportation only")
    print(
        "Claim boundary: no matter, mass, charge, energy, object, or "
        "faster-than-light transport"
    )
    print(
        "Default candidate: "
        f"{data.case.label}, dim={data.case.dim}, side={data.case.side}, "
        f"mass={data.case.mass:g}, G={data.case.G:g}, "
        f"schedule={DEFAULT_SCHEDULE}, T={args.runtime:g}, steps={args.steps}, "
        f"method={args.method}"
    )
    print(
        "Target ground: "
        f"gap={fmt_float(data.target_gap)}, "
        f"Phi+={target.phi_plus_overlap:.6f}, "
        f"Favg={target.exact_avg_fidelity:.6f}, "
        f"Bell*={target.best_bell_overlap:.6f} ({target.best_bell_label}), "
        f"CHSH={target.logical_chsh:.6f}, neg={target.negativity:.6f}"
    )
    print(
        "Initial state: "
        f"E0={fmt_float(data.initial_energy)}, gap={fmt_float(data.initial_gap)}, "
        f"degeneracy={data.initial_ground_degeneracy}, mode={data.initial_state_mode}"
    )
    print()


def print_convergence_table(rows: list[EvolutionResult]) -> None:
    reference = rows[-1]
    print(f"Step-count convergence, smoothstep T={rows[0].runtime:g}:")
    print(
        "  "
        f"{'steps':>6s} {'dt':>9s} {'ground':>10s} {'d_ground':>11s} "
        f"{'loss':>11s} {'d_loss':>11s} {'Phi+':>9s} {'d_Phi+':>11s} "
        f"{'Favg':>9s} {'d_Favg':>11s}"
    )
    for result in rows:
        metrics = result.metrics
        print(
            "  "
            f"{result.steps:6d} "
            f"{fmt_float(result.dt):>9s} "
            f"{result.final_ground_overlap:10.6f} "
            f"{fmt_delta(result.final_ground_overlap - reference.final_ground_overlap):>11s} "
            f"{fmt_float(result.diabatic_loss):>11s} "
            f"{fmt_delta(result.diabatic_loss - reference.diabatic_loss):>11s} "
            f"{metrics.phi_plus_overlap:9.6f} "
            f"{fmt_delta(metrics.phi_plus_overlap - reference.metrics.phi_plus_overlap):>11s} "
            f"{metrics.exact_avg_fidelity:9.6f} "
            f"{fmt_delta(metrics.exact_avg_fidelity - reference.metrics.exact_avg_fidelity):>11s}"
        )
    print()


def print_method_table(rows: list[EvolutionResult]) -> None:
    reference = rows[0]
    print(f"Propagator/method comparison at steps={reference.steps}:")
    print(
        "  "
        f"{'method':>13s} {'ground':>10s} {'loss':>11s} {'Phi+':>9s} "
        f"{'Favg':>9s} {'d_Favg':>11s} {'norm_err':>10s}"
    )
    for result in rows:
        print(
            "  "
            f"{result.method:>13s} "
            f"{result.final_ground_overlap:10.6f} "
            f"{fmt_float(result.diabatic_loss):>11s} "
            f"{result.metrics.phi_plus_overlap:9.6f} "
            f"{result.metrics.exact_avg_fidelity:9.6f} "
            f"{fmt_delta(result.metrics.exact_avg_fidelity - reference.metrics.exact_avg_fidelity):>11s} "
            f"{result.final_norm_error:10.3e}"
        )
    print()


def print_schedule_table(rows: list[EvolutionResult]) -> None:
    print("Schedule comparison at same runtime/step budget:")
    print(
        "  "
        f"{'schedule':>12s} {'ground':>10s} {'loss':>11s} {'Phi+':>9s} "
        f"{'Bell*':>9s} {'label':>5s} {'Favg':>9s} {'neg':>9s}"
    )
    for result in rows:
        print(
            "  "
            f"{result.schedule[:12]:>12s} "
            f"{result.final_ground_overlap:10.6f} "
            f"{fmt_float(result.diabatic_loss):>11s} "
            f"{result.metrics.phi_plus_overlap:9.6f} "
            f"{result.metrics.best_bell_overlap:9.6f} "
            f"{result.metrics.best_bell_label:>5s} "
            f"{result.metrics.exact_avg_fidelity:9.6f} "
            f"{result.metrics.negativity:9.6f}"
        )
    print()


def print_variant_table(
    title: str,
    rows: list[VariantRow],
    fidelity_threshold: float,
    loss_threshold: float,
) -> None:
    print(title)
    print(
        "  "
        f"{'control':>16s} {'targetPhi':>9s} {'ground':>10s} {'loss':>11s} "
        f"{'Phi+':>9s} {'Favg':>9s} {'neg':>9s} {'status':>13s}"
    )
    for row in rows:
        result = row.result
        print(
            "  "
            f"{row.label[:16]:>16s} "
            f"{row.target_phi_plus:9.6f} "
            f"{result.final_ground_overlap:10.6f} "
            f"{fmt_float(result.diabatic_loss):>11s} "
            f"{result.metrics.phi_plus_overlap:9.6f} "
            f"{result.metrics.exact_avg_fidelity:9.6f} "
            f"{result.metrics.negativity:9.6f} "
            f"{robustness_status(result, fidelity_threshold, loss_threshold):>13s}"
        )
    print()


def print_null_control(result: EvolutionResult, tolerance: float) -> None:
    clean = null_control_clean(result, tolerance)
    print("G=0/null control:")
    print(
        "  "
        f"ground={result.final_ground_overlap:.6f}, "
        f"loss={fmt_float(result.diabatic_loss)}, "
        f"Phi+={result.metrics.phi_plus_overlap:.6f}, "
        f"Bell*={result.metrics.best_bell_overlap:.6f} "
        f"({result.metrics.best_bell_label}), "
        f"Favg={result.metrics.exact_avg_fidelity:.6f}, "
        f"neg={result.metrics.negativity:.6f}, "
        f"non-resource={'PASS' if clean else 'FAIL'}"
    )
    print()


def print_no_signal(result: EvolutionResult, random_inputs: int, seed: int, tolerance: float) -> None:
    audit = no_signal_audit(result.resource_rho, random_inputs, seed)
    pairwise_ok = audit.max_pairwise_no_record_distance <= 10.0 * tolerance
    marginal_ok = audit.max_no_record_to_marginal_distance <= 10.0 * tolerance

    print("Bob pre-message input-independence audit:")
    print(
        "  candidate: "
        f"{result.case.label}, {result.schedule}, T={result.runtime:g}, "
        f"steps={result.steps}, method={result.method}"
    )
    print(
        "  teleportation sample: "
        f"{6 + random_inputs} inputs (seed={seed}), "
        f"mean/min/max fidelity={audit.sampled_mean_fidelity:.6f}/"
        f"{audit.sampled_min_fidelity:.6f}/{audit.sampled_max_fidelity:.6f}, "
        f"trace_error={audit.max_trace_error:.3e}"
    )
    print(
        "  Bob before message: "
        f"distance_to_resource_marginal={audit.max_no_record_to_marginal_distance:.3e}, "
        f"pairwise_input_distance={audit.max_pairwise_no_record_distance:.3e}, "
        f"marginal_bias_from_I/2={audit.bob_marginal_bias:.3e}, "
        f"input-independence={'PASS' if pairwise_ok and marginal_ok else 'FAIL'}"
    )
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=float, default=DEFAULT_RUNTIME)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument(
        "--convergence-steps",
        default="80,160,320,640",
        help="comma-separated fixed step counts for the default T=40 smoothstep row",
    )
    parser.add_argument(
        "--method-steps",
        type=int,
        default=160,
        help="fixed steps for expm_multiply/eigh propagator comparison",
    )
    parser.add_argument(
        "--schedules",
        default="linear,smoothstep,sine",
        help=f"comma-separated schedules from: {', '.join(SCHEDULES)}",
    )
    parser.add_argument(
        "--timing-runtimes",
        default="36,40,44",
        help="comma-separated runtimes around the default budget",
    )
    parser.add_argument(
        "--g-scales",
        default="0.98,1.0,1.02",
        help="comma-separated multipliers for the target G amplitude",
    )
    parser.add_argument(
        "--mass-values",
        default="0,0.02",
        help="comma-separated mass values for small Hamiltonian perturbation checks",
    )
    parser.add_argument(
        "--noise-levels",
        default="0,0.01",
        help="comma-separated schedule-control noise sigmas; 0 reuses the default row",
    )
    parser.add_argument(
        "--method",
        choices=("auto", "expm_multiply", "eigh"),
        default=DEFAULT_METHOD,
        help="main finite-step propagation method",
    )
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--random-inputs", type=int, default=64)
    parser.add_argument("--tolerance", type=float, default=1e-10)
    parser.add_argument("--degeneracy-tolerance", type=float, default=1e-9)
    parser.add_argument(
        "--robust-fidelity-threshold",
        type=float,
        default=0.95,
        help="Favg threshold for the perturbation status column",
    )
    parser.add_argument(
        "--robust-loss-threshold",
        type=float,
        default=1e-3,
        help="diabatic-loss threshold for the perturbation status column",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.runtime <= 0.0:
        raise ValueError("--runtime must be positive")
    if args.steps < 1:
        raise ValueError("--steps must be positive")
    if args.method_steps < 1:
        raise ValueError("--method-steps must be positive")
    if args.random_inputs < 0:
        raise ValueError("--random-inputs must be nonnegative")
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")
    if args.degeneracy_tolerance <= 0.0:
        raise ValueError("--degeneracy-tolerance must be positive")
    if not (0.0 < args.robust_fidelity_threshold <= 1.0):
        raise ValueError("--robust-fidelity-threshold must be in (0, 1]")
    if args.robust_loss_threshold < 0.0:
        raise ValueError("--robust-loss-threshold must be nonnegative")


def main() -> int:
    args = parse_args()
    validate_args(args)

    convergence_steps = unique_sorted_int(
        parse_int_list(args.convergence_steps, "--convergence-steps") + (args.steps,)
    )
    timing_runtimes = unique_sorted(
        parse_float_list(args.timing_runtimes, "--timing-runtimes") + (args.runtime,)
    )
    g_scales = unique_sorted(parse_float_list(args.g_scales, "--g-scales") + (1.0,))
    mass_values = unique_sorted(parse_float_list(args.mass_values, "--mass-values") + (0.0,))
    noise_levels = unique_sorted(parse_float_list(args.noise_levels, "--noise-levels") + (0.0,))
    schedules = parse_schedules(args.schedules)
    smoothstep = SCHEDULES[DEFAULT_SCHEDULE]

    nominal_case = make_case("2d_poisson_chsh", mass=DEFAULT_MASS, G=DEFAULT_G)
    nominal_data = build_case_data(nominal_case, args.degeneracy_tolerance)
    print_setup(nominal_data, args)

    convergence_results = [
        evolve_fixed_steps(
            nominal_data,
            smoothstep,
            runtime=args.runtime,
            steps=steps,
            method=args.method,
        )
        for steps in convergence_steps
    ]
    by_steps = {result.steps: result for result in convergence_results}
    default_result = by_steps[args.steps]
    print_convergence_table(convergence_results)

    method_reference = by_steps.get(args.method_steps)
    if method_reference is None:
        method_reference = evolve_fixed_steps(
            nominal_data,
            smoothstep,
            runtime=args.runtime,
            steps=args.method_steps,
            method=args.method,
        )
    method_rows = [
        method_reference,
        evolve_fixed_steps(
            nominal_data,
            smoothstep,
            runtime=args.runtime,
            steps=args.method_steps,
            method="eigh",
        ),
    ]
    print_method_table(method_rows)

    schedule_rows: list[EvolutionResult] = []
    for schedule in schedules:
        if schedule.name == DEFAULT_SCHEDULE:
            schedule_rows.append(default_result)
        else:
            schedule_rows.append(
                evolve_fixed_steps(
                    nominal_data,
                    schedule,
                    runtime=args.runtime,
                    steps=args.steps,
                    method=args.method,
                )
            )
    print_schedule_table(schedule_rows)

    timing_rows: list[VariantRow] = []
    for runtime in timing_runtimes:
        if abs(runtime - args.runtime) <= 1e-15:
            result = default_result
        else:
            result = evolve_fixed_steps(
                nominal_data,
                smoothstep,
                runtime=runtime,
                steps=args.steps,
                method=args.method,
            )
        timing_rows.append(
            variant_row("runtime", f"T={runtime:g}", nominal_data, result)
        )
    print_variant_table(
        "Runtime/timing sensitivity, smoothstep fixed steps:",
        timing_rows,
        args.robust_fidelity_threshold,
        args.robust_loss_threshold,
    )

    g_rows: list[VariantRow] = []
    for scale in g_scales:
        G_value = DEFAULT_G * scale
        if abs(scale - 1.0) <= 1e-15:
            data = nominal_data
            result = default_result
        else:
            data = build_case_data(
                make_case(f"2d_poisson_Gx{scale:g}", mass=DEFAULT_MASS, G=G_value),
                args.degeneracy_tolerance,
            )
            result = evolve_fixed_steps(
                data,
                smoothstep,
                runtime=args.runtime,
                steps=args.steps,
                method=args.method,
            )
        g_rows.append(variant_row("G", f"Gx{scale:g}", data, result))
    print_variant_table(
        "G-amplitude target sensitivity:",
        g_rows,
        args.robust_fidelity_threshold,
        args.robust_loss_threshold,
    )

    mass_rows: list[VariantRow] = []
    for mass in mass_values:
        if abs(mass - DEFAULT_MASS) <= 1e-15:
            data = nominal_data
            result = default_result
        else:
            data = build_case_data(
                make_case(f"2d_poisson_m{mass:g}", mass=mass, G=DEFAULT_G),
                args.degeneracy_tolerance,
            )
            result = evolve_fixed_steps(
                data,
                smoothstep,
                runtime=args.runtime,
                steps=args.steps,
                method=args.method,
            )
        mass_rows.append(variant_row("mass", f"m={mass:g}", data, result))
    print_variant_table(
        "Mass perturbation sensitivity:",
        mass_rows,
        args.robust_fidelity_threshold,
        args.robust_loss_threshold,
    )

    noise_rows: list[VariantRow] = []
    for sigma in noise_levels:
        if sigma <= 1e-15:
            result = default_result
        else:
            result = evolve_fixed_steps(
                nominal_data,
                smoothstep,
                runtime=args.runtime,
                steps=args.steps,
                method=args.method,
                schedule_label=f"smoothstep+noise{sigma:g}",
                control_noise_sigma=sigma,
                noise_seed=args.seed,
            )
        noise_rows.append(
            variant_row("noise", f"sigma={sigma:g}", nominal_data, result)
        )
    print_variant_table(
        "Deterministic schedule-control noise sensitivity:",
        noise_rows,
        args.robust_fidelity_threshold,
        args.robust_loss_threshold,
    )

    null_case = make_case("2d_null", mass=DEFAULT_MASS, G=0.0)
    null_data = build_case_data(null_case, args.degeneracy_tolerance)
    null_result = evolve_fixed_steps(
        null_data,
        smoothstep,
        runtime=args.runtime,
        steps=args.steps,
        method=args.method,
    )
    print_null_control(null_result, args.tolerance)

    print_no_signal(default_result, args.random_inputs, args.seed, args.tolerance)

    print("Conclusion:")
    print(
        "  The default 2D 4x4 smoothstep T=40 row remains a strong finite-time "
        "resource diagnostic after the bounded convergence and small-control checks above."
    )
    print(
        "  This is still not a preparation proof: the model is small, closed, idealized, "
        "and assumes the initial G=0 ground state and ideal taste-qubit readout."
    )
    print(
        "  Scope remains ordinary quantum state teleportation only; no matter, mass, "
        "charge, energy, object, or faster-than-light transport."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
