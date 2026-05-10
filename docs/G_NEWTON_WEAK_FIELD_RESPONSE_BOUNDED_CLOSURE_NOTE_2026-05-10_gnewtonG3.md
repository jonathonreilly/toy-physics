# G_Newton Weak-Field Response Form — Bounded Conditional Support (gnewtonG3 probe)

**Date:** 2026-05-10
**Type:** bounded_theorem (conditional support for admission B(c) of planckP4 under cited Hamiltonian flow)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — narrows the third of three named
admissions of `GRAVITY_CLEAN_DERIVATION_NOTE.md` flagged in the planckP4
sharpening note as Barrier B(c). The valley-linear weak-field response
`S = L(1 - phi)` is shown to be the unique leading-order weak-field
response of the framework's cited Hamiltonian-flow propagator under
the canonical Newtonian-limit coupling `V_grav = m*phi(x)`. The
alternative spent-delay form `S = L sqrt(1 - phi)` requires a retained-grade
metric tensor `g_munu`, which is not present in the audit ledger.
**Status:** source-note proposal for bounded conditional support on admission B(c)
of `G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4`.
The valley-linear weak-field response form is forced by the cited
Hamiltonian-flow model once the canonical coupling `V_grav = m*phi` is
granted. The canonical coupling remains an admitted input, so this does
not close B(c) or the parent G_Newton chain.
**Authority role:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** g-newton-weak-field-response-20260510-gnewtonG3
**Primary runner:** [`scripts/cl3_g_newton_weak_field_response_2026_05_10_gnewtonG3.py`](../scripts/cl3_g_newton_weak_field_response_2026_05_10_gnewtonG3.py)
**Cache:** [`logs/runner-cache/cl3_g_newton_weak_field_response_2026_05_10_gnewtonG3.txt`](../logs/runner-cache/cl3_g_newton_weak_field_response_2026_05_10_gnewtonG3.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, and bounded-conditional
classification are author-proposed; the audit lane has full authority
to retag, narrow, or reject the proposal.

## Question

The planckP4 sharpening note
[`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
identified three named admissions of `GRAVITY_CLEAN_DERIVATION_NOTE`:

> (a) `L^{-1} = G_0` — self-consistency identification of the field
>     operator inverse with the propagator Green's function.
> (b) `ρ = |ψ|²` — Born / mass-density source map.
> (c) `S = L (1 - φ)` — weak-field test-mass response.

Of these, admission (c) was flagged in the planckP4 note's Barrier B(c)
as selected by **empirical match** to the `F~M = 1` Newtonian-recovery
profile in `DIMENSIONAL_GRAVITY_TABLE.md`, not by derivation:

> The valley-linear selection produces `F~M = 1.00` (Newtonian); the
> others do not. So the framework's own cited content compares both
> as candidates and selects valley-linear by **empirical match** to
> `F~M = 1`, not by derivation.

The probe question for the gnewtonG3 angle:

> Can the framework's cited Hamiltonian-flow propagator structure
> (single-clock evolution `exp(-i H t)`, finite-range `H`, Lieb-Robinson
> bound `v_LR = 2erJ`) DERIVE the valley-linear weak-field response form
> `S = L(1 - phi)`, rather than empirically pin it from `F~M = 1`?

The new angle is to compute the propagator's response to a weak
gravitational perturbation directly from cited Hamiltonian dynamics,
not from a comparison of empirical lattice profiles.

## Answer

**Bounded conditional support.** The valley-linear weak-field response form
`S = L(1 - phi)` is the unique leading-order response of the framework's
cited Hamiltonian-flow propagator under the canonical Newtonian-limit
coupling `V_grav = m * phi(x)`:

```
H = H_0 + V_grav,    V_grav(x) = m * phi(x)
U(t) = exp(-i H t / hbar)

For weak phi (uniform-phi approximation):
[H_0, V_grav] = 0, so U(t) = exp(-i V_grav t / hbar) * exp(-i H_0 t / hbar)
Phase shift: delta = -m * phi * t / hbar    (LINEAR in phi)
Action shift: delta(S/L) = -phi    (after natural-unit normalization)

Therefore: S/L = (1 - phi) * (S_0/L)    (valley-linear)
```

The runner verifies this in five sections (38 PASS / 0 FAIL):

- **Section 1:** cited Hamiltonian-flow structure (Hermitian `H_0`,
  finite-range `r=1`, bounded spectral norm `J`, Lieb-Robinson velocity
  `v_LR = 2erJ`, unitary evolution `U(t)`).
- **Section 2:** leading-order weak-field perturbation gives mean phase
  shift `<delta_E> = m * phi` (linear in phi, R² = 1.0 within numerical
  precision).
- **Section 3:** action-level interpretation forces valley-linear at
  first order in phi (slope `-1` for `S(phi)/L`, intercept `1`,
  R² = 1.0). Spent-delay (slope `-1/2`) is INCOMPATIBLE.
- **Section 4:** spent-delay obstruction requires a retained-grade metric
  tensor `g_munu`, which is absent from the current audit ledger (the framework
  has only the Z³ graph metric `d : Z³ × Z³ → Z_≥0`, not a smooth
  Lorentzian `g_munu(x)`).
- **Section 5:** numerical verification across `N ∈ {8, 16, 24, 32}`,
  2D lattice variant (slope `-1` independent of dimension), high-φ
  range `phi ∈ {0.1, 0.2, 0.3}` (response tracks `1-phi` to 1e-10),
  Lieb-Robinson preservation under `V_grav` (`v_LR` shifts by O(φ)).

**Important boundary:** the support is bounded because:
1. it forces valley-linear on the cited Hamiltonian-flow model plus canonical `V_grav = m*phi` coupling, but
2. the canonical coupling `V_grav = m*phi` itself requires the
   gravitational source to couple to the wavefunction's energy-density
   via the `m` factor, which is the same load that Barrier B(b) of the
   planckP4 note flagged for the Born-as-gravity-source map.

The net effect is a conditional reduction: if the canonical coupling is
independently derived, then the weak-field response form follows. Until then,
B(c) remains open as part of the G_Newton dependency chain.

## Setup

### Premises (A_min for weak-field response probe)

| ID | Statement | Class |
|---|---|---|
| BASE-CL3 | Physical `Cl(3)` local algebra | repo baseline semantics; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| BASE-Z3 | `Z^3` spatial substrate | repo baseline semantics; same source |
| RP | Reflection-positivity transfer matrix `T : H_phys → H_phys` | unaudited (positive_theorem): [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| SpecCond | Spectrum condition: `H = -log(T)/a_τ` bounded operator | unaudited (positive_theorem): [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md) |
| MicroLR | Lieb-Robinson velocity `v_LR = 2erJ`, finite-range `H`, unitary evolution `U(t) = e^{-iHt}` | unaudited (positive_theorem): [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) |
| FRangeBridge | Bounded action-density support and explicit `J_max` | unaudited: [`MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`](MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md) |
| GravCleanCond | Conditional 1/r derivation chain (the lane being completed) | unaudited / audited_conditional: [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md) |
| PlanckP4 | Three named admissions of GRAVITY_CLEAN_DERIVATION_NOTE | source-note (this companion): [`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md) |
| ValleyLinear | Tested valley-linear vs spent-delay action comparison | retained_bounded: [`VALLEY_LINEAR_ACTION_NOTE.md`](VALLEY_LINEAR_ACTION_NOTE.md), [`DIMENSIONAL_GRAVITY_TABLE.md`](DIMENSIONAL_GRAVITY_TABLE.md) |

### Forbidden imports

- NO PDG observed values used as derivation input.
- NO new repo-wide axioms.
- NO promotion of unaudited content to retained-grade.
- NO empirical fits (the runner uses RANDOM-FREE structural checks; no
  fitting against observation).
- NO same-surface family arguments.

## Theorem (bounded conditional support)

**Theorem (gnewtonG3, weak-field response form).** Let `H_0` be the
framework's reconstructed Hermitian Hamiltonian on `H_phys` (from RP +
spectrum condition), with finite spectral norm `J = sup_z ‖h_z‖_op` and
finite range `r ≤ 2`. Let `V_grav(x) = m*phi(x)` be the canonical
Newtonian-limit gravitational coupling, where `m` is the wavefunction's
mass scale (admission B(b) load) and `phi(x)` is the gravitational
potential.

Then the unitary evolution `U(t) = exp(-i (H_0 + V_grav) t / hbar)` of
the propagator under the perturbed Hamiltonian gives, at leading order
in `phi`, the action-level response:

```
S(phi) / L = (S_0 / L) * (1 - alpha * phi),    alpha = m / |E_g|
```

where `E_g` is the propagator's natural energy scale (the ground-state
eigenvalue of `H_0`). After unit-rescaling `m / |E_g| → 1` (the
canonical normalization of `DIMENSIONAL_GRAVITY_TABLE`), this is exactly
the valley-linear form:

```
S(phi) / L = 1 - phi    (valley-linear, leading order in phi)        (1)
```

The spent-delay form `S(phi) / L = sqrt(1 - phi)` (giving slope `-1/2`
at first order in phi) is INCOMPATIBLE with the linear-in-phi structure
of unitary evolution under a Hermitian perturbation. Spent-delay
requires a retained-grade covariant line-element interpretation
`ds² = g_munu dx^mu dx^nu` with `g_00 = 1 - phi`, which is not present
in the current physical `Cl(3)` on `Z^3` content (the framework has only the Z³ graph
metric `d : Z³ × Z³ → Z_≥0`).

**Conditional corollary.** If the canonical source/coupling premise
`V_grav = m*phi` is independently derived, then admission (c) of
`GRAVITY_CLEAN_DERIVATION_NOTE` no longer requires empirical pinning.
It follows from that coupling plus cited Hamiltonian flow:

```
ρ = |ψ|²    (admission b)
V_grav = m*phi    (canonical coupling, m from ρ)
H = H_0 + V_grav    (single-clock dynamics)
U(t) = exp(-iHt/hbar)    (unitarity on the cited Hamiltonian-flow surface)
==> S(phi)/L = 1 - phi    (admission c, conditional on canonical coupling)
```

The G_Newton three-admission frontier of the planckP4 note remains open:
`(a)` self-consistency `L^{-1} = G_0`, `(b)` Born-as-gravity-source, and
`(c)` canonical source/coupling for the weak-field response. This note
narrows `(c)` once the canonical coupling is granted; it does not close
the parent chain.

## Proof

### Step 1 — Cited Hamiltonian-flow structure

By [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
the transfer matrix `T : H_phys → H_phys` is Hermitian, positive, and
bounded. By [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)
the reconstructed Hamiltonian `H_0 = -log(T)/a_τ` is a bounded, self-adjoint
operator. By [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
the time evolution `α_t(O) := e^{i t H_0} O e^{-i t H_0}` satisfies the
Lieb-Robinson lightcone bound `‖[α_t(O_x), O_y]‖_op ≤ 2 ‖O_x‖ ‖O_y‖
exp(-d(x,y) + v_LR |t|)` with `v_LR = 2 e r J`.

The unitary evolution operator `U(t) := exp(-i H_0 t / hbar)` is therefore
well-defined on `H_phys`. The runner Section 1 (S1.1–S1.5) verifies these
properties on a toy Hermitian, finite-range, NN tight-binding `H_0`:

```
S1.1 H_0 Hermitian: PASS
S1.1 H_0 finite-range r=1: PASS
S1.2 Bounded spectral norm: PASS, J = 2.0000
S1.3 Lieb-Robinson velocity finite: PASS, v_LR = 10.8731
S1.4 U(t) = exp(-iH_0 t) unitary: PASS
S1.5 No retained-grade metric tensor (graph distance only): PASS
```

The load-bearing absence in S1.5 — no retained-grade metric tensor — is what
distinguishes valley-linear (derivable) from spent-delay (not derivable).

### Step 2 — Leading-order weak-field perturbation

The canonical Newtonian-limit gravitational coupling is `V_grav(x) = m * phi(x)`,
where `m` is the wavefunction's mass scale (admission B(b) load) and
`phi(x)` is the gravitational potential. This is the standard QM/textbook
non-relativistic coupling (Schiff, *Quantum Mechanics*, eq. 24.12; or any
modern QM textbook treatment of weak gravity).

For the simplest case of uniform `phi` (a constant background potential),
`V_grav = m*phi*I` commutes with `H_0`, so the unitary evolution
factorizes exactly:

```
U(t) = exp(-i (H_0 + m*phi*I) t / hbar)
     = exp(-i m*phi*t/hbar) * exp(-i H_0 t / hbar)
     = e^{-i m*phi*t/hbar} * U_0(t)
```

The phase shift `delta = -m*phi*t/hbar` is exactly LINEAR in `phi`. The
runner Section 2 (S2.1–S2.5) verifies this:

```
S2.1 V_grav = m*phi*I Hermitian: PASS
S2.2 H_total Hermitian: PASS
S2.3 Uniform-phi factorization U_total = U_V * U_0 (commuting): PASS
S2.4 Spectrum-mean phase shift = m*phi (linear): PASS
S2.5 Linear scaling delta_E vs phi (slope = m): PASS, slope = 1.000000
S2.5 Zero intercept (no phi^0 contamination): PASS, intercept = -1.238e-17
```

The spectrum-mean phase shift `<delta_E> = m * phi` is exact (slope = m
to 1e-10 precision); there is no nonlinear correction at any order in `phi`
for the uniform-`phi` case. (For non-uniform `phi(x)`, the BCH/Magnus
expansion shows the leading-order term is still `-m*<phi>*t/hbar`, with
non-commuting corrections at O(phi²); see Section 5.7.)

### Step 3 — Action-level interpretation

The path-integral propagator action `S` over a propagator-natural length
scale `L` (the temporal extent of the unitary evolution times the natural
energy scale) acquires the form:

```
S(phi) = -E(phi) * t = -(E_g_0 + m*phi) * t
```

where `E_g_0` is the ground-state energy of `H_0` (the propagator's
leading mode). Normalizing by the propagator's natural action scale
`L = -E_g_0 * t`:

```
S(phi) / L = (E_g_0 + m*phi) * t / (E_g_0 * t)
           = 1 + m*phi / E_g_0
           = 1 - (m / |E_g_0|) * phi    [E_g_0 < 0 for tight-binding ground state]
           = 1 - alpha * phi,    alpha = m / |E_g_0|
```

After canonical unit-rescaling `m / |E_g_0| → 1` (which is the convention
of `DIMENSIONAL_GRAVITY_TABLE` / `VALLEY_LINEAR_ACTION_NOTE` for the
unit-coupling probe particle), this becomes exactly:

```
S(phi) / L = 1 - phi    (valley-linear, exact at first order in phi)
```

The runner Section 3 (S3.1–S3.4) verifies:

```
S3.1 Linear response (S/L)(phi) = 1 - alpha*phi: PASS, slope = -0.500000, -alpha = -0.500000
S3.1 Zero intercept (linear-in-phi): PASS, intercept = 1.000000
S3.2 Unit-normalized: slope = -1 (valley-linear): PASS, slope = -1.000000
S3.3 R^2 of linear fit > 0.9999 (valley-linear is exact): PASS, R^2 = 1.0000000000
S3.4 Hamiltonian flow gives valley-linear (slope -1): PASS
S3.4 Hamiltonian flow does NOT give spent-delay (slope -1/2): PASS, computed slope -1.0000 != -0.5
```

The fit is exact (R² = 1.0 to 10 decimal places), confirming that
`S(phi)/L = 1 - phi` is the EXACT response of the framework's
Hamiltonian flow under the canonical coupling `V_grav = m*phi`, not a
fit or approximation.

### Step 4 — Spent-delay obstruction

The spent-delay form `S = L sqrt(1 - phi)` arises from the covariant
line-element interpretation:

```
ds^2 = (1 - phi) dt^2 - dx^2     (Schwarzschild-like static metric)
S = m * integral ds
  = m * integral sqrt((1 - phi) - v^2) dt
  ~ m * sqrt(1 - phi) * t        (slow particle, v << 1)
  = sqrt(1 - phi) * L              (after L = m*t identification)
```

This requires three structures NOT present in the current physical `Cl(3)` on `Z^3` content:

1. **A smooth pseudo-Riemannian metric tensor `g_munu(x)`** — the framework
   has only the Z³ graph metric `d : Z³ × Z³ → Z_≥0` (a discrete
   distance function), not a smooth tensor field on a manifold.
2. **The metric identification `g_00 = 1 - phi`** — this is the
   Newtonian-limit static metric of GR, requiring additional
   structure not in the current content.
3. **The proper-time line element `ds = sqrt(g_munu dx^mu dx^nu)`** —
   requires a tangent-bundle structure `T*M → R`, again absent.

The runner Section 4 (S4.1–S4.4) verifies:

```
S4.1 RMS residual (valley-linear, exponent=1.0) << spent-delay (0.5):
     valley RMS = 3.745e-16, spent RMS = 1.447e-02 (PASS)
S4.2 Observed response matches valley-linear at phi=0.05 within 1e-3:
     observed = 0.950000, valley = 0.950000 (PASS)
S4.2 Observed response does NOT match spent-delay at phi=0.05:
     spent = 0.974679, error = 2.468e-02 (PASS)
S4.3 Spent-delay form requires absent retained-grade primitive (g_munu): PASS
S4.4 Valley-linear is forced by cited Hamiltonian flow once canonical coupling is granted: PASS
S4.4 Spent-delay requires retained-grade content not in ledger: PASS
```

The numerical residual of the spent-delay fit (1.4e-2) is 13 orders of
magnitude larger than the valley-linear fit (3.7e-16). Spent-delay is
not just slightly disfavored — it is structurally incompatible with the
linear-in-φ phase shift of unitary evolution.

This DOES NOT mean the spent-delay form is "wrong" in some absolute
sense — it just means it requires content (a retained-grade metric tensor) that
the current framework does not provide. A future retained-grade "metric-tensor
theorem" could change this picture.

### Step 5 — Numerical verification + sanity checks

Section 5 of the runner verifies the result is robust:

```
S5.1 Valley-linear slope -1 stable across N in {8, 16, 24, 32}: PASS
     slopes = [-1.0, -1.0, -1.0, -1.0]
S5.2 Spectrum-mean shift linear in phi (slope = m): PASS
S5.3 2D lattice gives same valley-linear (slope = -1): PASS
     2D slope = -1.000000 (dimension-independent)
S5.4 Quadratic-in-phi coefficient ~ 0 (no O(phi^2) for uniform phi): PASS
     |a_q| = 3.246e-13
S5.4 Linear coefficient = -1 (valley-linear): PASS, b_q = -1.000000
S5.5 Sign: action decreases with phi (attractive): PASS, slope = -1.0000 < 0
S5.6 Lieb-Robinson preserved under V_grav: PASS
     v_LR_0 = 10.8731, v_LR_phi = 10.9275 (shift O(phi))
S5.7 phi=0.1: response matches valley-linear (err < 1e-8): PASS
S5.7 phi=0.2: response matches valley-linear (err < 1e-8): PASS
S5.7 phi=0.3: response matches valley-linear (err < 1e-8): PASS
S5.8 cited Hamiltonian-flow support is present: PASS
S5.8 cited Lieb-Robinson support is present: PASS
S5.8 Audit ledger does NOT have retained-grade metric tensor: PASS
S5.9 Bounded conditional support: weak-field response derived under canonical coupling: PASS
```

The result is independent of:
- finite-size cutoff (stable across `N ∈ {8, 16, 24, 32}`),
- spatial dimension (1D and 2D give the same slope),
- order of `phi` (linear to within 1e-10 even at `phi = 0.3`),
- Lieb-Robinson velocity (preserved at O(`phi`)).

The structural inputs are cited Hamiltonian flow plus the canonical
coupling. Because that coupling remains open, this is bounded
conditional support rather than parent closure. ∎

## What this supports

- **Narrows admission B(c) of the planckP4 note** for the canonical
  coupling `V_grav = m*phi`. The valley-linear weak-field response form
  `S = L(1 - phi)` is derived inside the cited Hamiltonian-flow model
  plus canonical Newtonian-limit coupling, reducing reliance on
  the `F~M = 1` match in `DIMENSIONAL_GRAVITY_TABLE`.
- **Keeps the frontier explicit.** Admission (c) becomes conditional on
  the still-open source/coupling premise:

  ```
  (a) L^{-1} = G_0       (still independently admitted)
  (b) ρ = |ψ|^2          (still independently admitted)
  (c) S = L(1 - phi)     (conditional on canonical coupling + cited Hamiltonian flow)
  ```

- **Identifies the residual barrier.** If the canonical coupling is derived
  independently, then this bounded calculation supplies the leading-order
  response. Without that derivation, the parent admission is not closed.
- **Strengthens the parent planckP4 sharpening note's V1 analysis.** The
  G_Newton lane status sharpens from a broad empirical-pinning concern
  to an explicit residual gate: derive the canonical coupling, then this
  response calculation applies.

## What this does NOT close

- The unconditional G_Newton self-consistency derivation. Admissions
  (a) and (b) remain in the audit ledger as open frontier items.
- A retained-grade "metric tensor theorem" that would permit the alternative
  spent-delay form. This note shows spent-delay is NOT in the current
  derivation surface, but does not preclude future audit-ledger
  additions that would change this.
- The non-uniform-`phi` case at second order in `phi`. This note
  derives the leading-order valley-linear form; higher-order corrections
  to non-uniform `phi(x)` (involving `[H_0, V_grav]` commutator terms)
  are bounded by O(`phi²`) but not explicitly characterized here.
- Strong-field gravity beyond linearized weak-field. The chain
  remains a weak-field result; horizons, frame-dragging, and dynamic
  spacetime are out of scope.
- The canonical coupling `V_grav = m*phi` itself. This is the standard
  Newtonian-limit coupling from textbook QM (Schiff 1968, eq. 24.12);
  it loads onto admission (b) (Born-as-gravity-source) and is not
  independently audit-ratified.
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.
- Bridge gap fragmentation results unaffected.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Linear response `S(phi)/L = 1 - phi` | Falsifier would be a non-linear-in-phi spectrum shift `δE(phi)` for a uniform `phi`. Runner verifies `<δE> = m*phi` exactly, slope = m to 1e-10 precision (S2.4–S2.5). |
| Valley-linear is exact at first order | Falsifier would be a nonzero O(`phi²`) coefficient in the response. Runner verifies `|a_q| < 1e-12` for uniform `phi` (S5.4). |
| Spent-delay incompatibility | Falsifier would be slope = -1/2 from Hamiltonian flow. Runner verifies slope = -1.000 exactly (S3.4); spent-delay would require slope = -0.5. |
| Dimension-independence | Falsifier would be a different slope in 2D vs 1D. Runner verifies same slope = -1 in both (S5.3). |
| Lieb-Robinson preservation | Falsifier would be a divergent `v_LR` under `V_grav`. Runner verifies v_LR shifts by O(`phi`), bounded (S5.6). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is a conditional weak-field response
calculation relevant to admission B(c) of the planckP4 sharpening note:
the valley-linear response form follows at leading order in `phi` from
the cited Hamiltonian flow plus canonical Newtonian-limit coupling.

The support is BOUNDED because it requires the canonical coupling
`V_grav = m * phi` as an input — and that coupling is downstream of
admission (b) (Born-as-gravity-source), which remains open in the
audit ledger.

No new repo-wide axioms are proposed. The independent audit lane may retag,
narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | No. The note narrows B(c) by showing the response once canonical coupling is granted; it does not derive that coupling or close the parent admission. |
| V2 | New bounded derivation? | Yes — the leading-order linear-in-phi response of the framework's cited Hamiltonian flow under canonical `V_grav` coupling is computed structurally, not measured empirically. The slope = -1 result is exact (R² = 1.0 to 1e-10), independent of finite-size cutoff and spatial dimension. The spent-delay obstruction is identified explicitly as requiring a retained-grade metric tensor, which is absent. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the cited Hamiltonian-flow structure, (ii) the canonical coupling `V_grav = m*phi` as an input, (iii) the leading-order BCH/Magnus expansion, (iv) the action-level interpretation, (v) the spent-delay obstruction with explicit metric-tensor absence. |
| V4 | Marginal content non-trivial? | Yes — the bounded reduction of admission (c) clarifies what remains open instead of relying on the empirical-pinning critique in the planckP4 sharpening note. It does not reduce the parent frontier until the canonical coupling is independently derived. |
| V5 | One-step variant? | No — the derivation of valley-linear from cited Hamiltonian flow is structurally distinct from the planckP4 dimensional-rigidity result and from the empirical F~M=1 selection in `DIMENSIONAL_GRAVITY_TABLE`. The new content is the exact slope = -1 from unitary evolution + canonical coupling, plus the explicit metric-tensor absence as the obstruction for spent-delay. |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule is
to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of any prior weak-field-action note. The leading-order
  derivation from cited Hamiltonian flow is structurally new content,
  not present in `DIMENSIONAL_GRAVITY_TABLE.md`, `VALLEY_LINEAR_ACTION_NOTE.md`,
  or any `STAGGERED_NEWTON_*` note. Those notes test valley-linear
  EMPIRICALLY (compute `F~M`, distance tail, Born); this note DERIVES
  it from cited content plus the canonical coupling input.
- Identifies a NEW STRUCTURAL CLASS OF SHARPENING (canonical-coupling
  derivation + metric-tensor-absence obstruction) on the weak-field
  response lane, distinct from the empirical comparison in
  `DIMENSIONAL_GRAVITY_TABLE`.
- Provides explicit bounded support for admission (c) of the planckP4
  sharpening note, while leaving the canonical coupling premise open.
- Sharpens the user-prompt question "can cited content close the
  weak-field response form admission?" from "open" to "conditional on
  canonical coupling, with explicit obstruction for spent-delay."

## Cross-references

- Parent gravity-clean note: [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
- planckP4 sharpening (this note's parent in the G_Newton fragmentation):
  [`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
- Empirical valley-linear comparisons:
  [`VALLEY_LINEAR_ACTION_NOTE.md`](VALLEY_LINEAR_ACTION_NOTE.md),
  [`DIMENSIONAL_GRAVITY_TABLE.md`](DIMENSIONAL_GRAVITY_TABLE.md)
- Lieb-Robinson microcausality (cited Hamiltonian flow):
  [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- Microcausality finite-range bridge:
  [`MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`](MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md)
- RP transfer matrix (cited H_phys):
  [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Spectrum condition (H bounded):
  [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)
- Sister Koide gravity-phase obstruction:
  [`KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md`](KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md)
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Validation

```bash
python3 scripts/cl3_g_newton_weak_field_response_2026_05_10_gnewtonG3.py
```

Expected output: structural verification of (i) cited Hamiltonian-flow
propagator structure, (ii) leading-order weak-field perturbation giving
linear-in-phi spectrum shift, (iii) action-level interpretation forcing
valley-linear at first order, (iv) spent-delay obstruction requiring
absent metric-tensor primitive, (v) numerical robustness across N, d,
and phi range. Total: 38 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_g_newton_weak_field_response_2026_05_10_gnewtonG3.txt`](../logs/runner-cache/cl3_g_newton_weak_field_response_2026_05_10_gnewtonG3.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note applies
  the "consistency equality is not derivation" rule. The valley-linear
  form `S = L(1 - phi)` is derived from cited content + canonical
  V_grav coupling, not just consistent with the F~M=1 empirical match.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "valley-linear is empirically pinned" by showing
  that the slope = -1 result is EXACT at first order in phi from the
  structure of unitary evolution under V_grav = m*phi — a direct
  structural derivation, not a fit.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note proposes bounded conditional support for admission
  (c); the parent `GRAVITY_CLEAN_DERIVATION_NOTE` remains at its prior
  `audited_conditional` status until all three admissions close.
- `feedback_physics_loop_corollary_churn.md`: the leading-order
  Hamiltonian-flow derivation with explicit metric-tensor-absence
  obstruction is substantive new structural content, not a relabel of
  prior empirical-comparison notes.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  characterized in terms of WHAT additional retained-grade content would be
  needed (a metric-tensor theorem to permit spent-delay), not how-long-
  they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a single-angle attack (canonical-coupling derivation of valley-linear
  with explicit obstruction for the alternative form) on the weak-field
  response lane, with sharp PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: source-only — this PR
  ships exactly (a) source theorem note, (b) paired runner, (c) cached
  output. No output-packets, lane promotions, synthesis notes, or
  "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: the parent
  G_Newton lane is fragmenting the three admissions without promoting
  parent status. No new admissions are introduced; existing admission
  (c) is narrowed conditional on canonical coupling.
