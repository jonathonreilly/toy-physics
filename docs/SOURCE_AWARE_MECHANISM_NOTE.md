# Source-Aware Mechanism Note

**Date:** 2026-04-01  
**Scope:** review-safe mechanism note for why source-aware coupling is family-sensitive in 3D, and why broad shell support is not sufficient by itself.

## Short version

The current source-aware results are real, but they are narrow.

- The shell audit shows that phase contribution is spread across a broad set of shells on the retained 3D modular family, so the force law is not explained by a single thin shell band.
- The same audit also shows that broad shell support is present in both the Laplacian and source-resolved Green lanes, so shell support alone does not distinguish the better distance trend.
- The source-resolved Green lane improves the distance trend only weakly, while the source-projected lane is the only partial mover that clearly changes the exponent at all in the retained 3D family.
- Explicit non-overlapping source templates are sparse, and the clean-template pilots split by family: the retained 3D family can improve under source-projected coupling, but the denser control family and the 4D transfer pilot both flip back.
- The higher-dimensional follow-ups are also negative: the dense 5D source-projected pilot does not rescue the seam.
- A late detector-side purity ablation / rescue pair is negative for the simplest causal story: detector purity can be shifted modestly without collapsing or restoring the seam.

The review-safe conclusion is therefore:

- source-aware coupling is **family-sensitive in 3D**
- broad shell support is **not sufficient by itself**
- detector purity is **not sufficient by itself**
- the remaining seam is not another local shell or purity tweak, but an analytic explanation or a deeper architecture change

## What the diagnostics show

The mechanism picture comes from three script families:

- [scripts/path_shell_contribution_audit.py](/Users/jonreilly/Projects/Physics/scripts/path_shell_contribution_audit.py)
- [scripts/source_template_availability_scan.py](/Users/jonreilly/Projects/Physics/scripts/source_template_availability_scan.py)
- [scripts/source_template_clean_pilot.py](/Users/jonreilly/Projects/Physics/scripts/source_template_clean_pilot.py)
- [scripts/source_template_geometry_search.py](/Users/jonreilly/Projects/Physics/scripts/source_template_geometry_search.py)
- [scripts/fixed_template_source_green_pilot.py](/Users/jonreilly/Projects/Physics/scripts/fixed_template_source_green_pilot.py)
- [scripts/fixed_template_source_projected_pilot.py](/Users/jonreilly/Projects/Physics/scripts/fixed_template_source_projected_pilot.py)
- [scripts/four_d_source_projected_pilot.py](/Users/jonreilly/Projects/Physics/scripts/four_d_source_projected_pilot.py)
- [scripts/five_d_source_projected_pilot.py](/Users/jonreilly/Projects/Physics/scripts/five_d_source_projected_pilot.py)
- [scripts/detector_purity_ablation.py](/Users/jonreilly/Projects/Physics/scripts/detector_purity_ablation.py)
- [scripts/detector_purity_rescue.py](/Users/jonreilly/Projects/Physics/scripts/detector_purity_rescue.py)

### 1. Broad shell support is present, but it does not settle the mechanism

The shell audit on the retained 3D modular family shows that the Laplacian lane already has broad shell support and a strong distance trend, while the source-resolved Green lane also has broad shell support but only a much smaller distance exponent.

The important point is not the exact support number. It is that both lanes can have broad shell support, yet their distance trends differ.

That means shell support is a witness, not a complete explanation.

The retained-shell audit log also shows:

- Laplacian fit: `shift ~= 1.1477 * b^0.211`
- source-resolved Green fit: `shift ~= 0.3617 * b^0.026`

So the Green lane moves the distance trend, but it does so without needing the shell support picture to change in any obvious way.

### 2. Explicit source templates are sparse

The geometry-only scans show that fixed-count source templates are not broadly available under the default 3D construction:

- retained family: `clean template maps = 0`
- denser family: `clean template maps = 0`

Later template searches do find a tiny clean corner, but only at a very narrow layer/count combination.

That matters because it means the source-aware seam is not a broad template-availability effect. It depends on a narrow geometry corner.

### 3. The clean 3D pilots split by family

The explicit 3D clean-template pilot is the clearest family-sensitivity check.

In the retained family:

- Laplacian remains a stable baseline
- Green is weak and does not produce a broad fit
- projected coupling is the only lane that clearly moves the distance trend

In the denser family:

- the Green lane stays weak
- the projected lane no longer behaves like a stable rescue
- the improvement does not generalize into a broad family result

So the 3D source-aware seam is real, but it is family-sensitive rather than universal.

### 4. The 4D transfer is negative

The 4D source-projected pilot does not recover the 3D improvement.

On the retained 4D modular family:

- Laplacian keeps a small positive distance trend and a positive mass trend
- source-projected coupling flips the distance exponent positive and loses the mass trend

The 4D template-clean pilot reinforces that this is not a broad rescue lane.

That makes the source-aware seam look like a narrow 3D family effect, not a stable higher-dimensional mechanism.

### 5. The 5D transfer is also negative

The dense 5D source-projected pilot does not rescue the seam either.

In the tested dense 5D corner:

- the Laplacian lane keeps a near-flat `b` trend and a positive mass trend
- the source-projected lane flips to a worse positive `b` exponent or loses stable fits entirely

So the higher-dimensional extension does not broaden the source-aware effect.

### 6. Detector purity is not the main causal lever by itself

The detector-side purity experiments were a direct causality check, not just another correlation table.

On the retained 3D family:

- late mixing lowers detector purity from about `0.952` to about `0.894`
- but the projected `b` and `M` trends change only weakly

On the denser 3D family:

- late purification nudges detector purity only slightly
- and it does not restore a balanced source-aware rescue

So detector purity looks like a correlate of the good retained corner, but not the main causal knob by itself.

## What this does and does not claim

This note does **not** claim:

- a general theory of source-aware coupling
- a universal rescue of `1/b`
- a derivation of the shell/path mechanism from first principles
- a broad 4D or 5D transfer of the source-aware seam
- a detector-purity-only explanation of the source-aware seam

It does claim:

- broad shell support is present, but broad shell support alone is not enough
- source-aware coupling can move the distance trend only in a narrow 3D family-sensitive corner
- explicit source templates are too sparse to support a broad rescue claim
- 4D and 5D transfer are negative under the current clean controls
- detector purity is not the whole mechanism

## Review-safe summary

The current mechanism story is:

- the graph can support broad shell participation;
- the source-aware lane can still move the distance trend more than shell support alone;
- but the effect is family-sensitive, template-sparse, not robust under 4D/5D transfer, and not explained by detector purity alone.

So the correct next frontier is not another shell-local or purity-local tweak.
It is either:

- an analytic explanation of why the source-aware lane is family-sensitive, or
- a deeper architecture change that makes the source-aware effect robust.
