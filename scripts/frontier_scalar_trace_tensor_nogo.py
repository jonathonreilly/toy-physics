#!/usr/bin/env python3
"""No-go theorem for scalar-trace-only tensor completion on the current gravity branch.

This runner sharpens the remaining gravity gap beyond the restricted
strong-field package already closed on the branch.

Exact logic:
  1. The current microscopic boundary functional depends only on the scalar
     shell trace / Schur-complement data.
  2. The tensorial completion probes on the branch keep that scalar boundary
     data fixed by construction.
  3. Therefore any purported completion principle that factors only through
     the scalar shell data must assign the same output to all such probes.

Bounded witness:
  4. Explicit vector-shift and traceless-shear perturbations with the same
     scalar boundary data produce different Einstein-tensor channels.
  5. Hence no scalar-trace-only completion principle can determine the full
     `3+1` metric on the current branch. A genuinely tensor-valued matching law
     is required for full nonlinear GR.
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


def main() -> None:
    print("Scalar-trace-only tensor completion no-go")
    print("=" * 72)

    phi_oh = same_source.build_best_phi_grid()
    phi_fr = coarse.build_finite_rank_phi_grid()

    base_oh = tcomp.probe_family("scalar bridge", phi_oh, eps_vec=0.0, eps_ten=0.0, omega=0.0)
    vec_oh = tcomp.probe_family("vector shift", phi_oh, eps_vec=0.02, eps_ten=0.0, omega=1.0)
    ten_oh = tcomp.probe_family("tensor shear", phi_oh, eps_vec=0.0, eps_ten=0.02, omega=1.0)
    mix_oh = tcomp.probe_family("mixed", phi_oh, eps_vec=0.02, eps_ten=0.02, omega=1.0)

    base_fr = tcomp.probe_family("finite-rank scalar bridge", phi_fr, eps_vec=0.0, eps_ten=0.0, omega=0.0)
    vec_fr = tcomp.probe_family("finite-rank vector shift", phi_fr, eps_vec=0.02, eps_ten=0.0, omega=1.0)
    ten_fr = tcomp.probe_family("finite-rank tensor shear", phi_fr, eps_vec=0.0, eps_ten=0.02, omega=1.0)
    mix_fr = tcomp.probe_family("finite-rank mixed", phi_fr, eps_vec=0.02, eps_ten=0.02, omega=1.0)

    def same_scalar_data(a, b) -> bool:
        return abs(a.scalar_action - b.scalar_action) < 1e-14

    print("O_h scalar-action invariance:")
    print(
        f"  scalar={base_oh.scalar_action:.6e}, vector={vec_oh.scalar_action:.6e}, "
        f"tensor={ten_oh.scalar_action:.6e}, mixed={mix_oh.scalar_action:.6e}"
    )
    print("Finite-rank scalar-action invariance:")
    print(
        f"  scalar={base_fr.scalar_action:.6e}, vector={vec_fr.scalar_action:.6e}, "
        f"tensor={ten_fr.scalar_action:.6e}, mixed={mix_fr.scalar_action:.6e}"
    )
    print("Tensorial residual channels:")
    print(
        f"  O_h vector |G_0i|={vec_oh.e_ti:.3e}, tensor |G_ij^TF|={ten_oh.e_spatial_tf:.3e}, "
        f"mixed (|G_0i|,|G_ij^TF|)=({mix_oh.e_ti:.3e},{mix_oh.e_spatial_tf:.3e})"
    )
    print(
        f"  finite-rank vector |G_0i|={vec_fr.e_ti:.3e}, tensor |G_ij^TF|={ten_fr.e_spatial_tf:.3e}, "
        f"mixed (|G_0i|,|G_ij^TF|)=({mix_fr.e_ti:.3e},{mix_fr.e_spatial_tf:.3e})"
    )

    record(
        "the current microscopic scalar boundary functional is invariant across vector/tensor perturbations with the same scalar shell data on the exact O_h class",
        same_scalar_data(base_oh, vec_oh) and same_scalar_data(base_oh, ten_oh) and same_scalar_data(base_oh, mix_oh),
        (
            f"scalar={base_oh.scalar_action:.6e}, vector={vec_oh.scalar_action:.6e}, "
            f"tensor={ten_oh.scalar_action:.6e}, mixed={mix_oh.scalar_action:.6e}"
        ),
    )
    record(
        "the same scalar-data invariance persists on the finite-rank class",
        same_scalar_data(base_fr, vec_fr) and same_scalar_data(base_fr, ten_fr) and same_scalar_data(base_fr, mix_fr),
        (
            f"scalar={base_fr.scalar_action:.6e}, vector={vec_fr.scalar_action:.6e}, "
            f"tensor={ten_fr.scalar_action:.6e}, mixed={mix_fr.scalar_action:.6e}"
        ),
    )
    record(
        "vector perturbations with unchanged scalar boundary data activate independent G_0i residuals",
        vec_oh.e_ti > 1e-5 and vec_fr.e_ti > 1e-5,
        f"O_h={vec_oh.e_ti:.3e}, finite-rank={vec_fr.e_ti:.3e}",
        status="BOUNDED",
    )
    record(
        "traceless shear perturbations with unchanged scalar boundary data activate independent traceless spatial residuals",
        ten_oh.e_spatial_tf > 1e-4 and ten_fr.e_spatial_tf > 1e-3,
        f"O_h={ten_oh.e_spatial_tf:.3e}, finite-rank={ten_fr.e_spatial_tf:.3e}",
        status="BOUNDED",
    )
    record(
        "mixed vector+tensor perturbations simultaneously activate both tensor channels while leaving scalar boundary data unchanged",
        mix_oh.e_ti > 1e-5 and mix_oh.e_spatial_tf > 1e-4 and mix_fr.e_ti > 1e-6 and mix_fr.e_spatial_tf > 1e-3,
        (
            f"O_h=(|G_0i| {mix_oh.e_ti:.3e}, |G_ij^TF| {mix_oh.e_spatial_tf:.3e}), "
            f"finite-rank=(|G_0i| {mix_fr.e_ti:.3e}, |G_ij^TF| {mix_fr.e_spatial_tf:.3e})"
        ),
        status="BOUNDED",
    )
    record(
        "no completion principle that factors only through the current scalar shell trace / Schur data can determine the full `3+1` metric on this branch",
        same_scalar_data(base_oh, vec_oh)
        and same_scalar_data(base_oh, ten_oh)
        and same_scalar_data(base_fr, vec_fr)
        and same_scalar_data(base_fr, ten_fr)
        and vec_oh.e_ti > 1e-5
        and ten_oh.e_spatial_tf > 1e-4
        and vec_fr.e_ti > 1e-5
        and ten_fr.e_spatial_tf > 1e-3,
        "same scalar data, different tensorial Einstein channels -> genuinely tensor-valued matching law required",
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
