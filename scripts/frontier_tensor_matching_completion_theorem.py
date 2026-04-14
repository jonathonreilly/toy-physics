#!/usr/bin/env python3
"""Minimal tensor matching/completion theorem on the current restricted class.

This runner does not try to re-close gravity from scratch. It takes the current
restricted scalar bridge package as given and asks a narrower question:

    what is the smallest additional tensor-valued boundary data needed to
    distinguish the tensor sectors that the scalar shell trace cannot see?

Exact content:
  1. The scalar Schur boundary action is unchanged across the scalar, vector,
     tensor, and mixed probes already on the branch.
  2. Therefore the missing completion data must live in channels beyond the
     current scalar shell trace.
  3. The vector and traceless-shear probes activate two independent Einstein
     channels, so at least two non-scalar boundary coordinates are required.

Bounded content:
  4. On the current restricted probe family, the mixed perturbation is locally
     additive in those two tensor channels.
  5. This identifies the smallest plausible tensor completion as a scalar
     Schur action augmented by one shift-like and one traceless-shear channel.

This is not a full GR closure theorem. It is the sharpest localization of the
remaining missing principle currently visible on the branch.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader


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


tcomp = SourceFileLoader(
    "tensor_completion",
    "/private/tmp/physics-review-active/scripts/frontier_tensorial_einstein_regge_completion.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()


@dataclass
class FamilySummary:
    label: str
    base_action: float
    vec_action: float
    ten_action: float
    mix_action: float
    vec_delta_ti: float
    vec_delta_tf: float
    ten_delta_ti: float
    ten_delta_tf: float
    mix_delta_ti: float
    mix_delta_tf: float
    additive_ti_err: float
    additive_tf_err: float


def family_summary(label: str, phi_grid) -> FamilySummary:
    base = tcomp.probe_family("base", phi_grid, eps_vec=0.0, eps_ten=0.0, omega=0.0)
    vec = tcomp.probe_family("vector", phi_grid, eps_vec=0.02, eps_ten=0.0, omega=1.0)
    ten = tcomp.probe_family("tensor", phi_grid, eps_vec=0.0, eps_ten=0.02, omega=1.0)
    mix = tcomp.probe_family("mixed", phi_grid, eps_vec=0.02, eps_ten=0.02, omega=1.0)

    vec_delta_ti = vec.e_ti - base.e_ti
    vec_delta_tf = vec.e_spatial_tf - base.e_spatial_tf
    ten_delta_ti = ten.e_ti - base.e_ti
    ten_delta_tf = ten.e_spatial_tf - base.e_spatial_tf
    mix_delta_ti = mix.e_ti - base.e_ti
    mix_delta_tf = mix.e_spatial_tf - base.e_spatial_tf

    additive_ti_err = abs(mix_delta_ti - (vec_delta_ti + ten_delta_ti))
    additive_tf_err = abs(mix_delta_tf - (vec_delta_tf + ten_delta_tf))

    return FamilySummary(
        label=label,
        base_action=base.scalar_action,
        vec_action=vec.scalar_action,
        ten_action=ten.scalar_action,
        mix_action=mix.scalar_action,
        vec_delta_ti=vec_delta_ti,
        vec_delta_tf=vec_delta_tf,
        ten_delta_ti=ten_delta_ti,
        ten_delta_tf=ten_delta_tf,
        mix_delta_ti=mix_delta_ti,
        mix_delta_tf=mix_delta_tf,
        additive_ti_err=additive_ti_err,
        additive_tf_err=additive_tf_err,
    )


def main() -> None:
    print("Minimal tensor matching/completion theorem")
    print("=" * 76)

    oh = family_summary("exact local O_h", same_source.build_best_phi_grid())
    fr = family_summary("finite-rank", coarse.build_finite_rank_phi_grid())

    print("Channel deltas relative to the scalar bridge:")
    for row in (oh, fr):
        print(
            f"  {row.label}: "
            f"vec=(dG_0i={row.vec_delta_ti:.3e}, dG_TF={row.vec_delta_tf:.3e}), "
            f"ten=(dG_0i={row.ten_delta_ti:.3e}, dG_TF={row.ten_delta_tf:.3e}), "
            f"mix=(dG_0i={row.mix_delta_ti:.3e}, dG_TF={row.mix_delta_tf:.3e})"
        )
        print(
            f"    additive errors: dG_0i={row.additive_ti_err:.3e}, "
            f"dG_TF={row.additive_tf_err:.3e}"
        )

    record(
        "the scalar Schur boundary action is unchanged across the scalar, vector, tensor, and mixed probes on the exact local O_h class",
        abs(oh.base_action - oh.vec_action) < 1e-14
        and abs(oh.base_action - oh.ten_action) < 1e-14
        and abs(oh.base_action - oh.mix_action) < 1e-14,
        (
            f"base={oh.base_action:.6e}, vec={oh.vec_action:.6e}, "
            f"ten={oh.ten_action:.6e}, mix={oh.mix_action:.6e}"
        ),
    )
    record(
        "the same scalar-action invariance persists on the finite-rank class",
        abs(fr.base_action - fr.vec_action) < 1e-14
        and abs(fr.base_action - fr.ten_action) < 1e-14
        and abs(fr.base_action - fr.mix_action) < 1e-14,
        (
            f"base={fr.base_action:.6e}, vec={fr.vec_action:.6e}, "
            f"ten={fr.ten_action:.6e}, mix={fr.mix_action:.6e}"
        ),
    )
    record(
        "one independent shift-like tensor coordinate is required beyond the scalar trace",
        oh.vec_delta_ti > 1e-5 and fr.vec_delta_ti > 1e-5,
        f"O_h dG_0i={oh.vec_delta_ti:.3e}, finite-rank dG_0i={fr.vec_delta_ti:.3e}",
    )
    record(
        "one independent traceless-shear coordinate is required beyond the scalar trace",
        oh.ten_delta_tf > 1e-4 and fr.ten_delta_tf > 1e-4,
        f"O_h dG_TF={oh.ten_delta_tf:.3e}, finite-rank dG_TF={fr.ten_delta_tf:.3e}",
    )
    record(
        "the mixed probe is locally additive in those two tensor coordinates on the exact local O_h class",
        oh.additive_ti_err < 5e-7 and oh.additive_tf_err < 5e-7,
        f"dG_0i err={oh.additive_ti_err:.3e}, dG_TF err={oh.additive_tf_err:.3e}",
        status="BOUNDED",
    )
    record(
        "the same two-channel local additivity persists on the finite-rank class",
        fr.additive_ti_err < 5e-7 and fr.additive_tf_err < 5e-7,
        f"dG_0i err={fr.additive_ti_err:.3e}, dG_TF err={fr.additive_tf_err:.3e}",
        status="BOUNDED",
    )
    record(
        "the smallest tensor completion compatible with the tested family is scalar Schur data plus one shift-like and one traceless-shear boundary coordinate",
        oh.vec_delta_ti > 1e-5
        and oh.ten_delta_tf > 1e-4
        and fr.vec_delta_ti > 1e-5
        and fr.ten_delta_tf > 1e-4
        and oh.additive_ti_err < 5e-7
        and oh.additive_tf_err < 5e-7
        and fr.additive_ti_err < 5e-7
        and fr.additive_tf_err < 5e-7,
        "tested family closes locally with two extra tensor channels; the missing theorem is the microscopic source-to-channel map and its tensor boundary kernel",
    )

    print("\nMinimal tensor boundary action template:")
    print("  I_tensor(f, a_vec, a_tf ; j, eta) = I_scalar(f ; j)")
    print("      + 1/2 [a_vec, a_tf] K_tensor [a_vec, a_tf]^T - eta^T [a_vec, a_tf]")
    print("  with K_tensor symmetric positive definite.")
    print("  The current branch does not yet derive K_tensor or eta from microscopic source data.")

    print("\n" + "=" * 76)
    print("SUMMARY")
    print("=" * 76)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
