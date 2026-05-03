# YT Schur K-Prime Row Absence Guard

```yaml
actual_current_surface_status: bounded-support / Schur K-prime row absence guard; finite source-only rows rejected
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_schur_kprime_row_absence_guard.py`  
**Certificate:** `outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json`

## Purpose

The Schur-complement support theorem gives a useful positive target: if a
future same-surface neutral scalar kernel supplies

```text
K(x) = [[A(x), B(x)^T],
        [B(x), C(x)]]
```

and the pole derivatives of `A`, `B`, and `C`, then the same-source
denominator derivative `D_eff'(pole)` is computable.

This note adds the matching claim firewall.  Current finite source-only
`C_ss(q)` rows, same-source FH slopes, and chunk metadata are not those Schur
kernel rows.  They must not be used as `A/B/C` evidence or as a hidden
`K'(pole)` closure.

## Counterfamily

The runner constructs two analytic same-source denominators with the same
finite source rows and the same pole location:

```text
D_1(x) = x - x_p
D_2(x) = D_1(x) + epsilon (x - x_p) prod_i (x - x_i)
```

At every finite measured shell `x_i`, `D_1(x_i) = D_2(x_i)`, so the source-only
rows `C_ss(x_i) = 1 / D(x_i)` match exactly.  Both denominators vanish at
`x_p`.  Their pole derivatives differ.  The second family is represented by a
nonzero Schur mixing row, so the same finite source-only evidence can coexist
with different Schur rows and different `D_eff'(pole)`.

This is not a no-go against the Schur route.  It is the precise input contract:
future production or theorem work must supply explicit same-surface `A/B/C`
kernel rows and pole derivatives.

## Harness Guard

The production harness now emits a default-off metadata block:

```text
metadata.schur_kprime_kernel_rows.implementation_status = absent_guarded
metadata.schur_kprime_kernel_rows.finite_source_only_c_ss_is_not_schur_rows = true
metadata.schur_kprime_kernel_rows.used_as_physical_yukawa_readout = false
```

That block is instrumentation only.  It is not evidence.

## Boundary

The runner passes:

```bash
python3 scripts/frontier_yt_schur_kprime_row_absence_guard.py
# SUMMARY: PASS=14 FAIL=0
```

No retained or `proposed_retained` y_t claim is authorized.  The next positive
routes remain explicit same-surface Schur `A/B/C` rows, certified
`O_H/C_sH/C_HH` pole rows, or same-source W/Z response rows with identity
certificates.

This block does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`.
