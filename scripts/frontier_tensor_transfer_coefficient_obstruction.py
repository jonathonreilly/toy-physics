#!/usr/bin/env python3
"""Obstruction to deriving tau_tensor from current retained shell data alone.

This runner sharpens the current gravity frontier after the selector-transfer
law result.

Exact retained content already on the branch:
  1. The reduced shell law is identical on the audited restricted families:
     same radial shell kernel, same normalized anisotropic orbit mode, same
     shell-mean exterior response, same exact c_aniso.
  2. The active orbit direction on the projected tensor-correction quotient is
     also identical on those families.

Current tensor frontier:
  3. The selector-transfer coefficient tau_tensor = c_eta / c_aniso is only
     near-universal, not exact.

Conclusion:
  If two families share all currently retained reduced shell observables and
  the same active orbit direction, but have different tau_tensor, then no
  theorem that factors only through those retained shell data can determine
  tau_tensor exactly across the current class.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from io import StringIO

import numpy as np


ROOT = "/private/tmp/physics-review-active"

shell = SourceFileLoader(
    "one_parameter_shell",
    f"{ROOT}/scripts/frontier_one_parameter_reduced_shell_law.py",
).load_module()
fdtn = SourceFileLoader(
    "finite_rank_dtn",
    f"{ROOT}/scripts/frontier_finite_rank_dtn_correction_operator.py",
).load_module()
utk = SourceFileLoader(
    "tensor_universal_kernel",
    f"{ROOT}/scripts/frontier_tensor_universal_kernel.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    f"{ROOT}/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def max_profile_diff(a: list[tuple[float, float]], b: list[tuple[float, float]]) -> float:
    return max(abs(va - vb) for (_, va), (_, vb) in zip(a, b))


def max_mode_diff(
    a: dict[tuple[int, int, int], float], b: dict[tuple[int, int, int], float]
) -> float:
    keys = sorted(a)
    return max(abs(a[k] - b[k]) for k in keys)


def rel_scalar(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), 1e-16)


def normalized(v: np.ndarray) -> np.ndarray:
    return v / max(float(np.linalg.norm(v)), 1e-16)


def main() -> int:
    print("Tensor selector-transfer obstruction from retained shell data")
    print("=" * 78)

    phi_oh = same_source.build_best_phi_grid()
    phi_fr = coarse.build_finite_rank_phi_grid()

    red_oh = shell.reduced_data(phi_oh)
    red_fr = shell.reduced_data(phi_fr)

    with redirect_stdout(StringIO()):
        blk_oh = utk.family_block("exact local O_h", phi_oh)
        blk_fr = utk.family_block("finite-rank", phi_fr)

    c_aniso_oh = float(red_oh["anchor_per_Q"])
    c_aniso_fr = float(red_fr["anchor_per_Q"])
    c_eta_oh = float(blk_oh.eta_floor[1] / abs(blk_oh.scalar_action))
    c_eta_fr = float(blk_fr.eta_floor[1] / abs(blk_fr.scalar_action))
    tau_oh = c_eta_oh / c_aniso_oh
    tau_fr = c_eta_fr / c_aniso_fr

    rad_diff = max_profile_diff(red_oh["radial_profile"], red_fr["radial_profile"])
    orbit_diff = max_mode_diff(red_oh["norm_orbit"], red_fr["norm_orbit"])
    shell_diff = max_profile_diff(red_oh["mean_shell"], red_fr["mean_shell"])
    aniso_diff = max_profile_diff(red_oh["mean_aniso"], red_fr["mean_aniso"])
    c_aniso_diff = rel_scalar(c_aniso_oh, c_aniso_fr)

    act_oh = fdtn.family_active_vector(phi_oh)[:2]
    act_fr = fdtn.family_active_vector(phi_fr)[:2]
    active_dir_diff = float(np.max(np.abs(normalized(act_oh) - normalized(act_fr))))

    pair_operator = fdtn.build_active_operator()[np.array(fdtn.PAIR_ROWS), :]
    pair_rank = int(np.linalg.matrix_rank(pair_operator, tol=1e-12))

    tau_rel = rel_scalar(tau_oh, tau_fr)

    print("Shared retained reduced shell data:")
    print(f"  radial shell law difference = {rad_diff:.3e}")
    print(f"  orbit-mode difference       = {orbit_diff:.3e}")
    print(f"  shell-mean total difference = {shell_diff:.3e}")
    print(f"  shell-mean aniso difference = {aniso_diff:.3e}")
    print(f"  c_aniso relative difference = {c_aniso_diff:.3e}")

    print("\nShared active tensor-correction data:")
    print(f"  pair-quotient operator rank = {pair_rank}")
    print(f"  active-direction difference = {active_dir_diff:.3e}")

    print("\nSelector-transfer coefficients:")
    print(f"  tau_tensor(O_h)         = {tau_oh:.6e}")
    print(f"  tau_tensor(finite-rank) = {tau_fr:.6e}")
    print(f"  tau_tensor relative difference = {tau_rel:.6e}")

    record(
        "the exact local O_h and finite-rank families share the same retained reduced shell law",
        rad_diff < 1e-12
        and orbit_diff < 1e-12
        and shell_diff < 1e-12
        and aniso_diff < 1e-12
        and c_aniso_diff < 1e-12,
        (
            f"radial={rad_diff:.3e}, orbit={orbit_diff:.3e}, shell={shell_diff:.3e}, "
            f"aniso={aniso_diff:.3e}, c_aniso={c_aniso_diff:.3e}"
        ),
    )
    record(
        "the same two families share the same active orbit direction on the projected microscopic tensor-correction quotient",
        pair_rank == 2 and active_dir_diff < 1e-12,
        f"pair rank={pair_rank}, active-direction difference={active_dir_diff:.3e}",
    )
    record(
        "tau_tensor is still not exact across those families",
        tau_rel > 5e-2,
        f"tau relative difference={tau_rel:.6e}",
        status="BOUNDED",
    )
    record(
        "no theorem that factors only through the current retained reduced shell data and shared active orbit direction can determine tau_tensor exactly on the audited class",
        rad_diff < 1e-12
        and orbit_diff < 1e-12
        and shell_diff < 1e-12
        and aniso_diff < 1e-12
        and c_aniso_diff < 1e-12
        and active_dir_diff < 1e-12
        and tau_rel > 5e-2,
        (
            "identical retained shell inputs and identical active orbit direction still "
            f"leave tau mismatch={tau_rel:.6e}"
        ),
    )

    print("\nVerdict:")
    print(
        "The remaining gravity gap is not hidden in the current retained shell "
        "toolbox. Those shell observables, even augmented by the exact shared "
        "active orbit direction, are insufficient to force tau_tensor. The "
        "missing theorem must use additional microscopic source/lift data "
        "beyond the current reduced shell surface."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
        return 0
    print("Some checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
