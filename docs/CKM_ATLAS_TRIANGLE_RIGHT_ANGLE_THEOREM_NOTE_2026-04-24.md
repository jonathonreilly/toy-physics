# CKM Atlas Triangle Right-Angle Identity

**Date:** 2026-04-24

**Status:** retained structural-identity subtheorem of the promoted CKM
atlas/axiom package.  This note packages the exact right-angle geometry of the
rescaled atlas/Wolfenstein triangle carried by
[`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md).

**Primary runner:** `scripts/frontier_ckm_atlas_triangle_right_angle.py`

---

## 1. Statement

On the promoted CKM atlas surface, the retained CP-plane coordinates are

```text
rho = 1/6,
eta = sqrt(5)/6,
rho^2 + eta^2 = 1/6.
```

In the rescaled atlas triangle with vertices

```text
(0, 0), (1, 0), (rho, eta),
```

the interior angles are

```text
gamma_0 = arctan(eta/rho)       = arctan(sqrt(5)),
beta_0  = arctan(eta/(1-rho))   = arctan(1/sqrt(5)),
alpha_0 = pi - beta_0 - gamma_0 = pi/2.
```

So the atlas triangle is exactly right-angled:

```text
alpha_0 = 90 degrees.                              (A1)
```

The rescaled triangle area is

```text
Area_0 = eta/2 = sqrt(5)/12.                       (A2)
```

This is a pure structural corollary of the existing `1 + 5` CKM projector
surface.  It introduces no new fitted CKM input.

## 2. Boundary

This theorem is deliberately named the **CKM atlas triangle** theorem, not an
unqualified exact physical barred-unitarity-triangle theorem.

The existing retained CKM notes name `rho = 1/6` and `eta = sqrt(5)/6` as the
canonical atlas/Wolfenstein coordinates.  The exact rephasing-invariant
barred unitarity-triangle apex,

```text
rho_bar + i eta_bar = -V_ud V_ub^* / (V_cd V_cb^*),
```

receives finite-`lambda` corrections when the parent atlas parameters are
inserted into the exact PDG-standard CKM matrix.  With the current canonical
atlas numbers the guardrail calculation gives approximately

```text
rho_bar ~= 0.16264,
eta_bar ~= 0.36304,
alpha_bar ~= 90.69 degrees,
beta_bar  ~= 23.44 degrees,
gamma_bar ~= 65.87 degrees.
```

Those corrected physical-angle values are close to the atlas triangle, but the
exact retained right angle is the rescaled atlas identity (A1).  The runner
checks both the exact right-angle identity and this finite-`lambda` distinction
so the result cannot be over-read as an exact barred-triangle theorem.

## 3. Derivation

From the retained coordinates,

```text
tan(gamma_0) = eta/rho
             = (sqrt(5)/6) / (1/6)
             = sqrt(5),
```

so

```text
gamma_0 = arctan(sqrt(5)).
```

Similarly,

```text
tan(beta_0) = eta/(1-rho)
            = (sqrt(5)/6) / (5/6)
            = 1/sqrt(5),
```

so

```text
beta_0 = arctan(1/sqrt(5)).
```

For `x > 0`,

```text
arctan(x) + arctan(1/x) = pi/2.
```

Applying this at `x = sqrt(5)` gives

```text
beta_0 + gamma_0 = pi/2,
alpha_0 = pi - beta_0 - gamma_0 = pi/2.
```

The same statement has a geometric form.  The retained point lies on the
Thales circle with diameter `[0, 1]`:

```text
eta^2 = 5/36 = (1/6)(5/6) = rho(1-rho).
```

Any point on this circle sees the diameter under a right angle, so the angle
at `(rho, eta)` is exactly `90 degrees`.

## 4. Area and Atlas-Jarlskog Consistency

The rescaled atlas triangle has base length `1` and height `eta`, hence

```text
Area_0 = eta/2 = sqrt(5)/12.
```

Combining this with the retained Wolfenstein identities

```text
lambda^2 = alpha_s(v)/2,
A^2      = 2/3,
```

gives the same atlas/Wolfenstein Jarlskog-area factorisation already retained
in the CP-phase note:

```text
J_0 = 2 A^2 lambda^6 Area_0
    = 2 (2/3) (alpha_s(v)/2)^3 (sqrt(5)/12)
    = alpha_s(v)^3 sqrt(5) / 72.
```

Here `J_0` denotes the rescaled atlas/Wolfenstein area factor. The parent CKM
atlas runner separately carries the finite-`lambda` exact standard-matrix `J`
readout, including the usual cosine factors. So the right-angle geometry is
not an extra CKM primitive; it is another exact view of the same retained CKM
atlas surface.

## 5. What This Claims

- The rescaled atlas/Wolfenstein triangle has exact angles
  `alpha_0 = 90 deg`, `beta_0 = arctan(1/sqrt(5))`, and
  `gamma_0 = arctan(sqrt(5))`.
- The retained `gamma_0` equals the retained CKM phase
  `delta_CKM = arctan(sqrt(5))` on the atlas surface.
- The retained point lies exactly on the Thales circle
  `eta^2 = rho(1-rho)`.
- The rescaled atlas-triangle area is exactly `sqrt(5)/12`.
- The area formula reproduces the atlas factor
  `J_0 = alpha_s(v)^3 sqrt(5)/72`.

## 6. What This Does Not Claim

- It does not newly derive `rho = 1/6` or `eta = sqrt(5)/6`; those come from
  the CKM CP-phase structural identity theorem.
- It does not claim the exact barred unitarity-triangle angle is exactly
  `90 deg`; finite-`lambda` corrections shift the exact standard-CKM
  barred-triangle angles.
- It does not replace the parent atlas' finite-`lambda` exact standard-matrix
  `J` readout; the area relation is the atlas/Wolfenstein `J_0` factor.
- It does not derive higher-order Wolfenstein corrections.
- It does not introduce BSM flavor, PMNS, or Majorana phases.
- It does not use current global-fit angle values as derivation inputs.

## 7. Reproduction

```bash
python3 scripts/frontier_ckm_atlas_triangle_right_angle.py
```

Expected:

```text
PASSED: 26/26
CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_RETAINED=TRUE
BARRED_UNITARITY_TRIANGLE_EXACT_RIGHT_ANGLE_PROMOTED=FALSE
```

## 8. Cross-References

- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
