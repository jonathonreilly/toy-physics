# Koide BAE Probe 20 — V(m) Cubic-Extrema Extension to hw=1

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Status:** source-note proposal — Probe 20 of the Koide BAE-condition
(Brannen Amplitude Equipartition, formerly "A1-condition")
closure campaign. This probe asks whether the retained `Z^3` scalar
potential `V(m)` on the local Clifford trace, extended via spectral
functional calculus to the 3-dimensional `hw=1` `C_3`-orbit subspace,
yields extrema that satisfy the BAE condition `|b|^2 / a^2 = 1/2`.
**Authority role:** source-note proposal; effective status set only
by the independent audit lane.
**Loop:** koide-bae-probe20-vm-cubic-extrema-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_vm_cubic_extrema_2026_05_09_probe20.py`](../scripts/cl3_koide_bae_probe_vm_cubic_extrema_2026_05_09_probe20.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_vm_cubic_extrema_2026_05_09_probe20.txt`](../logs/runner-cache/cl3_koide_bae_probe_vm_cubic_extrema_2026_05_09_probe20.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner.

## Naming convention

In this note:
- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"BAE"** = Brannen Amplitude Equipartition condition `|b|^2 / a^2 = 1/2`
  for the `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. Historically labeled "A1-condition" prior to the
  2026-05-09 rename (PR #790).

## Constraint (per user 2026-05-09 directives)

**No new axioms. No external imports. No PDG observed values consumed.**
This probe operates strictly within the retained framework using only:

- `MINIMAL_AXIOMS_2026-05-03.md` (A1 = `Cl(3)`, A2 = `Z^3`).
- `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`
  in-scope content: the Clifford-trace algebra `Tr(T_m^2) = 3`,
  `Tr(T_m^3) = 1`, fixing `g_2 = 3/2` and `g_3 = 1/6`. The broader
  "mass tower" claim is OUT OF SCOPE in the retained note (depends on
  hidden upstream inputs `K_frozen`, `c_1`, `c_2`, `H_*` witness rates).
- `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`: retained
  `Q = 2/3` ⇔ `a_0^2 = 2|z|^2` algebraic equivalence on `hw=1`.

## Hypothesis tested

The retained `V(m)` on the local Clifford trace has the closed form

```text
V(m) = V_0 + L · m + (3/2) · m^2 + (1/6) · m^3,                    (1)
```

with `L = c_1 + c_2 / 2` and `c_2 = 35/12` exact, `c_1 ≈ -0.2526`
(numerical), so `L ≈ 1.2057`.

The single real coordinate `m = Tr(K_sel)` lies in the local
Clifford-trace direction. The natural `C_3`-equivariant promotion of
`(m → H)` to `hw=1` is the Hermitian circulant
`H = aI + bC + b̄C²` parameterized by `(a, |b|, arg b)` (3 real DOF).

**Hypothesis:** if `V(m)` extends to `hw=1` via spectral functional
calculus as `V_total(H) := Tr V(H) = Σ_k V(λ_k)`, where
`λ_k = a + 2|b| cos(arg(b) + 2 π k / 3)` are the eigenvalues, then the
extrema of `V_total` over `(a, |b|, arg b)` should land on the BAE
condition `|b|^2 / a^2 = 1/2`.

**This probe falsifies that hypothesis** within the cited source-stack content.

## Closed-form `V_total` on `hw=1`

Using `Tr(C^n) = 3` if `n ≡ 0 (mod 3)`, else `0`:

```text
Tr(H)   = 3 a,                                                     (2)
Tr(H^2) = 3 a^2 + 6 |b|^2,                                         (3)
Tr(H^3) = 3 a^3 + 18 a |b|^2 + 6 |b|^3 cos(3 arg b).               (4)
```

Hence the canonical extension

```text
V_total(a, r, φ) = 3 V_0 + 3 L a + (9/2) a^2 + 9 r^2
                 + (1/2) a^3 + 3 a r^2 + r^3 cos(3 φ)               (5)
```

where `r = |b|`, `φ = arg b`. **Equation (5) is symbolically verified
by the runner against the spectral sum `Σ_k V(λ_k)`.**

Consistency check (Section 3 of runner): at `r = 0`,
`V_total(a, 0, φ) = 3 V(a)`, recovering the 1D potential per axis `a`
(consistent with the retained `m_V ≈ -0.433` 1D minimum at retained `L`).

## Extremum equations on `hw=1`

```text
∂V_total / ∂φ = -3 r^3 sin(3 φ) = 0  ⟹  sin(3 φ) = 0,             (6)
∂V_total / ∂a = 3 L + 9 a + (3/2) a^2 + 3 r^2 = 0,                  (7)
∂V_total / ∂r = 18 r + 6 a r + 3 ε r^2 = 0,                         (8)
                where ε = cos(3 φ) ∈ {+1, -1}.
```

The angular condition (6) admits two solution branches: `ε = +1`
(C_3 directions `φ ∈ {0, 2π/3, 4π/3}`) or `ε = -1` (shifted directions
`φ ∈ {π/3, π, 5π/3}`).

The non-trivial radial branch (`r ≠ 0`) of (8) gives

```text
r = -ε (6 + 2 a),                                                   (9)
```

(with `ε^2 = 1`). Substituting (9) into (7) and clearing
the common factor `2/3`:

```text
9 a^2 + 54 a + 72 + 2 L = 0     [V_total non-trivial extremum]     (10)
```

## BAE condition in (a, r) coordinates

The BAE condition `r^2 / a^2 = 1/2`, combined with the non-trivial-
branch substitution (9):

```text
r^2 = (6 + 2 a)^2 = 4 (3 + a)^2,
4 (3 + a)^2 = a^2 / 2  ⟹  8 (3 + a)^2 = a^2,
8 a^2 + 48 a + 72 = a^2,
```

```text
7 a^2 + 48 a + 72 = 0     [BAE on non-trivial branch]              (11)
```

Roots: `a = (-24 ± 6√2) / 7`, numerically `a ∈ {-2.214, -4.643}`.

## The compatibility obstruction

Equations (10) and (11) are linearly independent quadratics in `a`.
A V_total non-trivial extremum coincides with a BAE point iff some `a`
satisfies both (10) and (11) simultaneously. Eliminating `a^2` between
(10) and (11) (multiply (11) by 9/7 and subtract from (10)):

```text
(54 - 48 · 9/7) a + (72 - 72 · 9/7 + 2 L) = 0
(378/7 - 432/7) a + (504/7 - 648/7 + 2 L) = 0
(-54/7) a + (-144/7 + 2 L) = 0,
```

```text
a = (7 L - 72) / 27     [forced "shared root" if it exists]        (12)
```

Substituting (12) back into (11) and solving for `L`:

```text
L ∈ {1.7368..., -7.6143...}     [V_total/BAE compatibility]         (13)
```

These are the **only two** values of `L` at which a V_total extremum
coincides with a BAE point.

The retained `L = c_1 + c_2 / 2 ≈ 1.2057` is **NOT** in the
compatibility set (13). The discrepancy is `|1.2057 - 1.7368| ≈ 0.531`
in `L` units — far outside any reasonable rounding tolerance.

**Conclusion:** the V_total extension's non-trivial extrema do not
satisfy BAE for the retained `L`.

## Numerical verification

For retained `L ≈ 1.2057`, the V_total non-trivial extrema are
(Section 8 of runner):

```text
a_1 ≈ -2.144,  r_1 ≈ 1.711,  r_1^2 / a_1^2 ≈ 0.637,
a_2 ≈ -3.856,  r_2 ≈ 1.711,  r_2^2 / a_2^2 ≈ 0.197.
```

Neither equals `0.500` (BAE). Section 9 of the runner confirms this
by an independent gradient descent.

## Per-eigenvalue extremization route (alternative interpretation)

A second natural interpretation: require each eigenvalue `λ_k` to
satisfy `V'(λ_k) = 0`. The roots of `V'(λ) = L + 3λ + (1/2)λ^2 = 0`
are `λ = -3 ± √(9 - 2 L)`. At `L = 0` (Clifford-only contribution):
`λ ∈ {0, -6}`.

The four `C_3`-orbit triples `(λ_0, λ_1, λ_2)` with each `λ_k ∈ {0, -6}`
realize the following `(a, r^2/a^2)`:

| Triple | `a` | `r^2/a^2` |
|---|---|---|
| `(0, 0, 0)` | 0 | undefined |
| `(0, 0, -6)` | -2 | 1.000 |
| `(0, -6, -6)` | -4 | 0.250 |
| `(-6, -6, -6)` | -6 | 0.000 |

**No triple realizes `r^2/a^2 = 1/2`.** The per-eigenvalue
extremization route is also incompatible with BAE.

## What this rules out

Within cited source-stack content (no axioms, no imports, no PDG values):

1. **`V_total = Σ V(λ_k)` extension** does not close BAE for retained `L`.
2. **Per-eigenvalue extremization** (`V'(λ_k) = 0` for all `k`) does
   not realize a BAE-compliant `C_3`-orbit triple.
3. **Any tuned `L`** that achieves V_total/BAE compatibility shifts the
   closure target from "BAE" to "deriving the compatible `L` from
   cited source-stack content." Since `L = c_1 + c_2/2` is itself derived from
   `K_frozen` upstream inputs that are out-of-scope per the retained
   note, this is not an in-scope path.

The obstruction is **structural** in the sense that it does not depend
on the numerical value of `c_1` (only on the algebraic shape of the
extremum equations). Even with tuned `L`, the V_total quadratic (10)
and the BAE quadratic (11) are linearly independent and share roots
only at isolated `L` values.

## What this does NOT rule out

- It does NOT rule out other extensions of `V(m)` to `hw=1`. Functional
  calculus gives `V_total = Σ V(λ_k)` (additive on the spectrum); other
  natural choices (e.g., `V_op = (3/2) H^2 + (1/6) H^3` interpreted as
  an operator without trace) would have different extremization
  behavior — but those are different functionals, not an extension of
  the retained `V(m)`.
- It does NOT close BAE positively. BAE remains an open derivation
  target across this 18-probe campaign. Probes 12 (Plancherel/
  Peter-Weyl), 13 (real structure), 14 (retained-U(1) hunt), 16
  (Q-readout functional pivot), 17 (sharpened obstruction), 18 (F1/F2/F3
  canonical-functional choice) each tested distinct routes; all are
  bounded.
- It does NOT contradict the retained `V(m)` 1D content. The retained
  `g_2 = 3/2`, `g_3 = 1/6` Clifford-trace identities are confirmed
  exactly by the runner. The `V_total` extension reduces to `3 V(a)` at
  `r = 0`, fully consistent.

## Sharpened residue

After Probes 12, 13, 14, 16, 17, 18, **20**, the BAE residue is
characterized as: a structure that pins `|b|^2 / a^2 = 1/2` on the
`hw=1` `C_3`-orbit Hermitian circulant. Probe 20 adds the negative
result: this structure is NOT supplied by spectral-functional extension
of the retained `V(m)`.

The residue therefore is NOT a consequence of:
- (Probe 12) Plancherel/Peter-Weyl conditional expectation on `A^{C_3}`;
- (Probe 13) any retained real-structure quotient of `M_3(ℂ)`;
- (Probe 14) any of nine inventoried retained continuous `U(1)` symmetries;
- (Probe 16) `U(1)_b`-invariance of the Brannen `Q`-readout functional;
- (Probe 18) any of three canonical log-isotype functionals `F_1`, `F_2`, `F_3`;
- (Probe 20) spectral-functional extension of `V(m)` to `hw=1`.

## Cross-references

- **Foundational notes:**
  `MINIMAL_AXIOMS_2026-05-03.md`,
  [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)
  (in-scope `V(m)` content; out-of-scope mass-tower claim).
- **Algebraic backbone:**
  [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
  (`Q = 2/3 ⇔ a_0^2 = 2|z|^2` exact equivalence on `hw=1`).
- **Cone narrow theorems:**
  [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md),
  [`KOIDE_CONE_COMPLETING_ROOT_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_COMPLETING_ROOT_NARROW_THEOREM_NOTE_2026-05-02.md).
- **Campaign synthesis:**
  [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md).
- **Immediate predecessors:**
  [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md),
  [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md),
  [`KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md).
- **Retained C_3 origin:**
  [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md).

## Forbidden-imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No new axioms introduced.
- No external imports.
- The retained note's out-of-scope "mass tower" claim is NOT consumed —
  only the in-scope Clifford-trace `g_2`, `g_3` content.

## Validation

```bash
python3 scripts/cl3_koide_bae_probe_vm_cubic_extrema_2026_05_09_probe20.py
```

The runner verifies:

1. Symbolic identities for `Tr(H)`, `Tr(H^2)`, `Tr(H^3)` on the
   `(a, r, φ)` coordinate system.
2. `V_total = Σ V(λ_k)` matches the closed form (5) symbolically.
3. The `r = 0` reduction recovers the 1D `V(m)` and the retained
   `m_V ≈ -0.433` extremum at retained `L`.
4. The angular extremum forces `sin(3 φ) = 0`.
5. The non-trivial branch reduces to the quadratic-in-`a`
   `9 a^2 + 54 a + 72 + 2 L = 0` (10).
6. The BAE condition reduces to `7 a^2 + 48 a + 72 = 0` (11).
7. Compatibility analysis confirms `L = c_1 + c_2 / 2 ≈ 1.2057` is NOT
   in the compatibility set.
8. Numerical extremum at retained `L` gives `r^2 / a^2 ∈ {0.637, 0.197}`,
   neither equal to `0.5`.
9. Per-eigenvalue extremization at `L = 0` realizes `r^2/a^2 ∈
   {0, 0.25, 1.0}`, none equal to `0.5`.

**Runner result: 27/0 PASS.**

## Review-loop rule

When reviewing future branches that propose to close BAE via the
retained `V(m)`:

1. The retained `V(m)` is a **single-coordinate** potential on the
   local Clifford trace `m = Tr(K_sel)`. Promoting it to `hw=1` requires
   a choice of extension; the canonical one (additive spectral
   functional calculus `V_total = Σ V(λ_k)`) does not close BAE
   for retained `L`.
2. Any alternative extension (e.g., operator-valued `V(H)` without
   trace, ad-hoc weighting) is itself a new admission, not a
   derivation from cited source-stack content.
3. The retained `c_1` value `(c_1 + c_2/2 = L ≈ 1.2057)` inherits
   the upstream `K_frozen` input, which is OUT OF SCOPE per the
   retained note. Tuning `L` to match the V_total/BAE compatibility
   set `{1.737, -7.614}` is therefore a separate derivation target,
   not a BAE closure.

## Honest assessment

The hypothesis tested (V(m) extension to hw=1 closes BAE) is FALSIFIED.
The structural reason is a clean linear-independence statement of two
quadratics in `a`. This is a sharpened bounded obstruction in the BAE
campaign and rules out the "V(m) extension to hw=1" route as a closure
mechanism within cited source-stack content.

The probe DOES NOT close BAE positively. The campaign retains BAE as
an open derivation target after Probe 20.
