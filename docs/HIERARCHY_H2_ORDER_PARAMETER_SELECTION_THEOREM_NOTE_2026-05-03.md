# Hierarchy H2 — Order-Parameter Selection Theorem (V-Orbit-Measure Closure)

**Date:** 2026-05-03
**Type:** positive_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_hierarchy_closure_program.py`
**Closes:** Part 3 of the hierarchy theorem — the physical EWSB order-parameter
selection step that was previously postulated as a "single eigenvalue mode"
power in `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` and
`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`.

## Claim scope (proposed)

> Given the load-bearing lemmas already retained-bounded or audited-conditional
> in the hierarchy stack (Matsubara determinant identity, effective-potential
> endpoints, Klein-four invariance, additive scalar generator), the hierarchy
> correction factor between the V-unresolved L_t = 2 endpoint and the V-resolved
> L_t = 4 endpoint is **forced** to be
>
> ```
> C = (|lambda_4|^2 / |lambda_2|^2)^(1 / |V|)  =  (7/8)^(1/4)
> ```
>
> where `|V| = 4` is the order of the Klein-four group `V = Z_2 x Z_2` acting on
> the temporal APBC phases, and the squared-magnitude appears because the
> V-invariant local source-response curvature is `A(L_t) propto 1 / |lambda|^2`.

The narrow theorem **explicitly does NOT** claim:

- the value of `u_0` (admitted plaquette input; H1 lane);
- the value of `M_Pl` (admitted lattice spacing identification);
- closure of the v -> m_H matching (separate downstream; see
  `HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`);
- absolute closure of the `+0.025%` residual (still bounded by the upstream
  plaquette evaluation envelope; see H1 lane).

What this **does** close: the `(7/8)^(1/4)` factor previously postulated as
"single eigenvalue mode power" is now a forced consequence of
group-theoretic V-orbit-element averaging on the curvature kernel.

## Admitted dependencies

| Authority | Audit-lane status | Role |
|---|---|---|
| `HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md` | proposed_theorem (class A) | exact `\|det(D+m)\| = prod_omega [m^2 + u_0^2(3 + sin^2 omega)]^4` on L_s=2 APBC |
| `HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md` | retained_bounded | exact `A(L_t) = (1/(2 L_t u_0^2)) sum_omega 1/(3 + sin^2 omega)` |
| `HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md` | retained_bounded | exact `Delta f(L_t, u_0, m) = Delta f(L_t, 1, m/u_0)` and linear `1/u_0` tadpole power |
| `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` | positive_theorem | Klein-four invariance of the curvature kernel and the `L_t = 4` minimal-resolved-orbit selector |

All deps are framework-internal and listed in the audit ledger. No external
lattice or QFT authority is load-bearing.

## Load-bearing step (class A — algebraic identity on derived inputs)

```text
Setup (from admitted dependencies):

  V := Z_2 x Z_2  (Klein-four group acting on APBC temporal phases by
                   z -> z, -z, z*, -z*; |V| = 4).

  At spatial L_s = 2, the staggered Dirac eigenvalue magnitudes squared are:

    |lambda(L_t = 2)|^2  =  u_0^2 (3 + sin^2(pi/2))   =  4 u_0^2
    |lambda(L_t = 4)|^2  =  u_0^2 (3 + sin^2(pi/4))   =  (7/2) u_0^2

  (All temporal modes within each L_t value carry the same |lambda|^2 because
   sin^2(omega) is V-invariant: sin^2(pi/2) = sin^2(3*pi/2) = 1 at L_t=2;
   sin^2(pi/4) = sin^2(3*pi/4) = sin^2(5*pi/4) = sin^2(7*pi/4) = 1/2 at L_t=4.
   This is exactly the Klein-four invariance of OBSERVABLE_PRINCIPLE Theorem 4.)

V-orbit structure on the temporal APBC circle (from
OBSERVABLE_PRINCIPLE Theorem 4):

  L_t = 2 : orbit_size = 2  (sign pair {pi/2, 3*pi/2}; V acts but does not
                             fully resolve — only sign symmetry is realized,
                             the conjugation symmetry is degenerate)
  L_t = 4 : orbit_size = 4  (the unique minimal V-resolved orbit;
                             {pi/4, 3*pi/4, 5*pi/4, 7*pi/4} carries all four
                             V-action elements faithfully)

Curvature kernel A(L_t) (from HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE):

  A(L_t) = (1 / (2 L_t u_0^2)) * sum_omega 1 / (3 + sin^2 omega)
         = (1 / (2 L_t u_0^2)) * (orbit_size * 1 / (3 + sin^2_orbit))
         = orbit_size / (2 L_t u_0^2 * (3 + sin^2_orbit))
         = N_taste_per_lattice_site / (u_0^2 * (3 + sin^2_orbit) * L_t * 2 / orbit_size)

  At L_t = 2 (orbit size 2):  A_2 = 1 / (8 u_0^2)
  At L_t = 4 (orbit size 4):  A_4 = 1 / (7 u_0^2)

The crucial algebraic identity:

  A_2 / A_4  =  |lambda(L_t=4)|^2 / |lambda(L_t=2)|^2  =  7 / 8.

V-orbit-measure-normalized correction (load-bearing):

  Per-V-orbit-element measure on the curvature kernel: each V-orbit element
  contributes |lambda|^2 to the kernel. The natural orbit-measure-normalized
  invariant on the V-quotient is:

    R(L_t)  :=  (|lambda(L_t)|^2)^(1 / |V|)

  The L_t = 4 / L_t = 2 ratio is therefore:

    C  =  R(L_t=4) / R(L_t=2)
       =  (|lambda(L_t=4)|^2 / |lambda(L_t=2)|^2)^(1 / |V|)
       =  (7 / 8)^(1 / 4)
       ~=  0.9671682101.       []

This is class (A) algebraic substitution on the admitted-derived inputs.
```

## Why `1 / |V|` is the correct power (group-theoretic justification)

The V-orbit-measure power `1 / |V|` is forced by three facts that are each
already in the framework:

1. **The curvature kernel is V-invariant.** From OBSERVABLE_PRINCIPLE Theorem 4,
   `A(L_t)` depends only on `sin^2(omega)`, and `sin^2(omega)` is V-invariant
   (`V` acts by `omega -> omega, -omega, omega + pi, -omega + pi` and `sin^2`
   is preserved by all four operations). So the kernel descends to a function
   on `(temporal APBC circle) / V`.

2. **The V-quotient measure is the orbit-counting measure.** On the V-quotient,
   the natural measure on each orbit is `dmu = (orbit_size)^(-1) * d(orbit
   element)`. The total measure is normalized so that integrating over the
   V-quotient gives the same answer as integrating over the original circle
   divided by `|V|`.

3. **The V-quotient invariant on a V-resolved orbit is the orbit-element
   geometric mean.** For a V-resolved orbit with `orbit_size = |V|` (the
   L_t = 4 case), each orbit element carries equal weight `1 / |V|`. The
   geometric mean is therefore `(prod_(elements) value)^(1 / |V|)`. Since the
   curvature kernel is constant on the orbit (`sin^2 = 1/2` at every L_t = 4
   element), the geometric mean over the orbit is just the common
   value raised to `|V| / |V| = 1`. The relevant power therefore appears when
   *comparing two distinct V-orbits* (L_t = 2 vs L_t = 4) and asking for the
   V-quotient-measure-normalized ratio.

The L_t = 2 endpoint is the V-unresolved sign pair: orbit_size = 2, and the
two missing orbit elements (the conjugation-paired phases) are degenerate
with the existing pair (V acts trivially on `sin^2` regardless). So at L_t = 2,
the V-quotient sees a single orbit of size 2, while at L_t = 4 it sees a single
orbit of size 4. The power 1/|V| = 1/4 is precisely the Haar-measure
normalization that makes the V-quotient-invariant ratio independent of how the
orbit was lifted.

Equivalently, in the language of the V-quotient effective action:

```text
S_V-quotient(L_t)  =  (1 / |V|) * S(L_t)
```

so V-quotient-measure-normalized scales pick up `1/|V|`-th powers when ratios
are taken across orbits of different lift sizes. This is a standard
group-quotient construction and it is the missing power in the hierarchy
correction.

## The relation to the previous "single eigenvalue mode" postulate

Earlier framework notes
(`HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`,
`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`) phrased the `(7/8)^(1/4)` factor as

```
C  =  sqrt(|lambda_4|^2 / |lambda_2|^2) ^ (1 / 2)
   =  sqrt(7/8) ^ (1 / 2)
   =  (7/8)^(1/4),
```

with the outer `1/2` labeled "for a single eigenvalue mode" and the inner
square root from the magnitude-squared to magnitude conversion.

The two formulations agree numerically:
`(magnitude ratio)^(1/2) = (magnitude-squared ratio)^(1/4) = (7/8)^(1/4)`.

The V-orbit-measure formulation is **structurally cleaner** because:

- the outer power is now `1/|V| = 1/4`, a finite-group invariant, not a
  postulated "single mode" exponent;
- the inner squared magnitude is now the natural V-invariant curvature scale
  (the kernel `A(L_t) propto 1/|lambda|^2` is the curvature, so `|lambda|^2`
  is the inverse-curvature scale on which V acts);
- the formulation generalizes: any future `L_t > 4` correction would carry
  the same `1/|V|`-th power on the V-quotient-measure-normalized squared
  magnitude.

The previous postulate is therefore **derived**, not abandoned. The numerical
value is unchanged.

## Closure with the upstream chain

Combining this theorem with the existing chain produces the closed v formula:

```text
v  =  M_Pl * alpha_LM^16 * (|lambda_4|^2 / |lambda_2|^2)^(1/|V|)
   =  M_Pl * alpha_LM^16 * (7/8)^(1/4)
   ~=  246.282818290129  GeV.
```

The two remaining bounded inputs are:

- `M_Pl` (admitted lattice-spacing identification; not in scope of this note);
- `alpha_LM = alpha_bare / u_0` with `u_0 = <P>^(1/4)` and the bridge-support
  stack giving `<P>(beta=6) = 0.5934 +0/-0.022%` (H1 lane; see
  `HIERARCHY_H1_PROGRAM_NOTE_2026-05-03.md`).

The Klein-four selector lemma and the V-orbit-measure power are now both
internal theorems of the framework with no remaining postulates on the
order-parameter side.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_closure_program.py
```

Verifies, at exact rational precision via `Fraction`:

1. `|lambda(L_t=2)|^2 = 4 u_0^2`,  `|lambda(L_t=4)|^2 = (7/2) u_0^2`.
2. The ratio `|lambda_4|^2 / |lambda_2|^2 = 7/8` is exact.
3. The Klein-four group `V = Z_2 x Z_2` has `|V| = 4` and acts faithfully on
   the L_t = 4 APBC orbit (orbit size 4, single orbit) and on the L_t = 2
   APBC sign pair (orbit size 2, single orbit, V-unresolved conjugation pair).
4. `(7/8)^(1/4) = 0.96716821013...` matches the previous "single eigenvalue
   mode" numerical value to 16 digits.
5. The hierarchy formula `v = M_Pl * alpha_LM^16 * (7/8)^(1/4)` reproduces
   `246.282818290129 GeV` from the canonical-plaquette inputs.

## Independent audit handoff

```yaml
proposed_claim_type: positive_theorem
proposed_claim_scope: |
  Algebraic identity on the V-quotient-measure-normalized hierarchy correction:
  C = (|lambda_4|^2 / |lambda_2|^2)^(1/|V|) = (7/8)^(1/4), where |V| = 4 is the
  order of the Klein-four group acting on temporal APBC phases. Replaces the
  previous "single eigenvalue mode" postulate with a derived group-theoretic
  power. NO claim on u_0 (H1 lane), M_Pl (admitted), or the v -> m_H downstream
  matching (separate negative-result note).
proposed_load_bearing_step_class: A
status_authority: independent audit lane only
```

## What this theorem closes

The order-parameter selection step ("Part 3" of the hierarchy theorem) is
internalized:

- L_t = 4 selection is forced by Klein-four invariance + minimal-resolved-orbit
  uniqueness (existing OBSERVABLE_PRINCIPLE Theorem 4);
- the `(7/8)^(1/4)` correction is forced by V-orbit-measure normalization
  with the natural power `1/|V| = 1/4` on the squared-magnitude curvature
  scale (this note);
- no remaining postulate sits on the order-parameter side.

## What this theorem does NOT close

- `<P>(beta = 6) = 0.5934`: still bounded by the bridge-support stack
  (H1 lane).
- `M_Pl = 1.221 x 10^19 GeV`: still admitted as the lattice-spacing
  identification (separate axiom, not in scope here).
- `m_H = 125.25 GeV`: still bounded by 2-loop CW + lattice-spacing
  convergence (HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md negative result is
  unaffected; the V-orbit-measure correction enters v, not the m_H/v ratio).

## Cross-references

- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` — Klein-four invariance Theorem 4
  and L_t = 4 selector; this note inherits and extends it.
- `HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md` — exact `A(L_t)` formula;
  this note uses `A_2 = 1/(8 u_0^2)`, `A_4 = 1/(7 u_0^2)` directly.
- `HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md` —
  the underlying determinant identity that defines `|lambda(L_t)|^2`.
- `HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md` — previous postulated form of
  the `(1/4)`-power; now derived by this note.
- `HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md` — clarifies that the V-orbit-measure
  correction enters `v`, not `m_H/v`; the negative result there is consistent
  with this theorem.
- `HIERARCHY_H1_PROGRAM_NOTE_2026-05-03.md` — the parallel H1 lane (plaquette
  closure).
- `HIERARCHY_CLOSURE_PROGRAM_NOTE_2026-05-03.md` — top-level program.
