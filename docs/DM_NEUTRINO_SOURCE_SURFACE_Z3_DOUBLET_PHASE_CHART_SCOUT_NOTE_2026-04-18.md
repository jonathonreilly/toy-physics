# DM Source-Surface Z_3-Doublet-Phase Chart-Change Scout Note

**Date:** 2026-04-18
**Status:** SCOUT -- chart-change stress test of the Case 3 microscopic
polynomial impossibility theorem. Verdict: **PARTIAL**.
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.
**Unit system:** natural dimensionless chart coordinates `(m, delta, q_+)`
on the retained `hw=1` affine chart `H = H_base + m T_m + delta T_delta
+ q_+ T_q`. All traces in matrix units of `Herm(3, C)`.

## Goal

Drop assumption A1.2 (that the affine chart `(m, delta, q_+)` is the
right parametrization) from the Case 3 impossibility theorem. Test
whether moving to a `Z_3`-irrep-natural complex coordinate on the
doublet reveals a delta-odd axiom-native polynomial invariant — which
would violate the theorem's delta-evenness claim.

Central sub-question: is `Im(z^3) = 3 q_+^2 delta - delta^3` with
`z = q_+ + i delta` an axiom-native Z_3-invariant scalar? If yes, HIT.

## Required reading (verified)

- [DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md](./KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md)

(The note `KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`
cited in the task prompt does not exist on the current atlas. The
analogous content on the Koide circulant side is carried by the two
`CIRCULANT_CHARACTER_*` notes and the `POSITIVE_PARENT_AXIS_OBSTRUCTION`
note. This scout still engages the chart-isomorphism question to those
notes.)

## Set-up

The retained `C_3[111]`-conjugation action on `Herm(3, C)` decomposes
the Hermitian tangent span as

- `T_q` = pure `Z_3`-singlet (circulant: `T_q = -I + C_3 + C_3^2`)
- `T_delta` = pure `Z_3`-doublet (one real-slice of the 2-D doublet)
- `T_m` = mixed (singlet + doublet, NOT circulant)

Let `T_{d,w}` and `T_{d,w-bar}` be the `omega`- and `omega-bar`-
eigenvectors of `C_3`-conjugation on `T_delta`:

```text
T_{d,w}    = (1/3) (T_delta + omega-bar C_3 T_delta C_3^{-1} + omega C_3^2 T_delta C_3^{-2})
T_{d,w-bar} = (1/3) (T_delta + omega C_3 T_delta C_3^{-1} + omega-bar C_3^2 T_delta C_3^{-2})
```

Both are complex, non-Hermitian, and satisfy `T_{d,w-bar} = T_{d,w}^\dagger`.

Define the complex doublet trace coordinate

```text
A(H) := Tr(H T_{d,w}).
```

Under `C_3`-conjugation of `H`: `A(C_3 H C_3^{-1}) = omega^{-1} A(H)`.
Hence `A^3` (and its complex conjugate) are `Z_3`-invariant.

## Direct computation on the chart

With `H = m T_m + delta T_delta + q T_q`:

```text
A(H) = Tr(H T_{d,w}) = 3 delta + i sqrt(3) m
```

(Numerically verified.) Therefore

```text
A(H)^3 + conj(A(H))^3 = 2 Re(A^3) = 54 delta^3 - 54 delta m^2 = 54 delta (delta^2 - m^2).
```

This is a **real, `Z_3`-invariant, delta-ODD** polynomial in `H`.

## Critical observations

### Observation 1. The prompt's `z = q_+ + i delta` is NOT `Z_3`-irrep-natural.

Under `C_3`-conjugation on `H`:

- `q_+` is a `Z_3`-SINGLET coordinate (fixed under `C_3`)
- `delta` is one REAL-SLICE of a 2-D `Z_3`-DOUBLET (rotates under `C_3`)

Mixing a singlet with a doublet-real-slice into a single complex
`z = q_+ + i delta` is a **chart artifice**, not a `Z_3`-irrep decomposition.
Under the actual `C_3`-action, `(q_+, delta) -> (q_+, -delta/2 + sqrt(3)/2 delta_2)`
with `delta_2` a new direction OFF the chart. So `z` does NOT transform
as an `omega`-eigenvector under `C_3`, and `z^3` is NOT `Z_3`-invariant
in the axiom-level sense. The chamber-chart identity `Im(z^3) = 3 q_+^2
delta - delta^3` is therefore NOT a retained `Z_3`-invariant scalar.

### Observation 2. The correct doublet-phase cubic is `2 Re(A^3) = 54 delta(delta^2 - m^2)`.

This is what `Im(z^3)` "should have been" under the correct
`Z_3`-irrep-natural decomposition. It involves `(m, delta)` only, NOT
`q_+`. The reason is structural: `q_+` is a singlet and cannot enter
the phase of a doublet object. The natural complex doublet coordinate
is `A = 3 delta + i sqrt(3) m`, so the "DM arg(z)" is `arctan(sqrt(3)
m / 3 delta)` — a function of `(m, delta)` alone.

### Observation 3. `2 Re(A^3)` uses a NON-HERMITIAN inserted operator `T_{d,w}`.

The Case 3 impossibility theorem's Theorem 3 proof (delta-evenness of
`Tr(H^k)`, `det(H)`, heat-kernel traces, spectral gap, chiral Ward
saturation) restricts to polynomial functionals built from:

- traces `Tr(H^k)`,
- inserted `Z_3`-invariant Hermitian operators.

The combination `A^3 + conj(A)^3` is a real, `Z_3`-invariant polynomial
in the matrix entries of `H`, but it is built via `Tr(H T_{d,w})`
where `T_{d,w}` is NEITHER Hermitian NOR `Z_3`-invariant. Its
construction uses the **`Z_3`-character structure of the retained
operator algebra `M_3(C)`**: `T_{d,w}` is an `omega`-eigenvector of
`C_3`-conjugation, cubed into a singlet. This is legitimate structure
from the retained three-generation observable theorem (on
`H_hw=1` the retained algebra is all of `M_3(C)`), but it is BEYOND
the scope literally covered by the impossibility theorem's Theorem 3.

### Observation 4. Selector content.

Set `2 Re(A^3) = 0`. Solutions:

```text
delta = 0   OR   delta = +m   OR   delta = -m.
```

This is a **delta-odd axiom-native selector** on the chart, but it
fixes `delta` only modulo `m` (which is fixed by the Schur baseline
`D = m I_3`). It gives NO `q_+` constraint: it is independent of
`q_+`.

## Robustness checks (mandatory)

### (a) Lattice-is-physical check

`T_{d,w}` decomposes into Hermitian real/imaginary pieces:
`T_{d,w} = (T_delta + i T_{delta,perp}) / 2` (up to scale), with
`T_{delta,perp}` the orthogonal real Hermitian doublet direction. Both
`T_delta` and `T_{delta,perp}` are real symmetric matrices on the
`hw=1` basis `{X_1, X_2, X_3}`, which is itself a physical-lattice
triplet (per THREE_GENERATION_OBSERVABLE_THEOREM). So `T_{d,w}` IS a
physical lattice projection, not purely abstract group theory. Passes.

### (b) 3+1D check

In 3+1D the time direction supplies an independent real direction that
together with spatial `C_3[111]` generates a real 2-plane. The DM
doublet coordinate `A = 3 delta + i sqrt(3) m` has `m` playing the
role of a "time-like" singlet mixed with the doublet-real-slice
`delta`. The imaginary axis of `A` is carried by `T_m` (the `m`
direction), which has both singlet AND doublet content. So the complex
structure of `A` is consistent with the 3+1D-plus-spatial-`C_3`
picture. Passes, with the caveat that this is a retained-atlas
restatement, not a new derivation.

### (c) Koide `hw=1` convergence check

Koide one-scalar obstruction at cyclic commutant level: on circulants
`H_K = a I + b C + conj(b) C^2`, the character coordinate is
`z_K = sqrt(3) b`. The Koide equal-character-weight condition is
`a_0^2 = 2 |z_K|^2` (see KOIDE_CIRCULANT_CHARACTER_BRIDGE). `arg(b)`
is the Koide phase, and it is axiom-silent at local-polynomial level
on circulants.

DM chart: `T_q = -I + C + C^2` IS circulant, but `T_delta, T_m` are
NOT circulants. The DM `A = 3 delta + i sqrt(3) m` is therefore
NOT the Koide `z_K`. They live in different slices:

- Koide `z_K`: complex doublet coordinate on the circulant subspace
  (dim 2 complex = 4 real, minus singlet `a`).
- DM `A`: complex doublet coordinate on the `(m, delta)` sub-chart of
  `Herm(3, C)`, where the imaginary axis picks up the doublet component
  of `T_m`.

They are NOT the same object in different coordinates. But they share
the **same structural phenomenon**: the `Z_3`-doublet phase is the
axiom-silent degree of freedom. Passes in the structural sense; does
NOT collapse the two problems to one.

## Exit classification

**PARTIAL.** The chart-change produces a genuine axiom-native
delta-odd Z_3-invariant polynomial

```text
S(H) := (Tr(H T_{d,w}))^3 + (Tr(H T_{d,w-bar}))^3 = 54 delta (delta^2 - m^2).
```

This VIOLATES the strict letter of the impossibility theorem's
delta-evenness if we admit non-Hermitian `Z_3`-doublet inserted
operators as "retained". But the named gap is sharp:

- `S(H)` is independent of `q_+` and so provides NO constraint on
  `q_+`. It pins `delta` only modulo `m` at the three values
  `{0, +m, -m}`.
- `S(H)` requires insertion of a non-Hermitian `T_{d,w}`; it is not
  literally of the form covered by the impossibility theorem's
  Theorem 3 (trace moments of Hermitian operators and their products).
- `S(H) = 0` selects `delta in {0, m, -m}`; active chamber
  `q_+ >= E_1 - delta` with `delta >= 0` retains the candidates
  `delta = 0` and `delta = m`, which still sweep a 1-dim ray in
  `q_+`.

Therefore the microscopic axiom IS richer than the Case 3 theorem
literally states: it DOES carry a delta-odd content via the
`Z_3`-character-cubed construction. But this content does NOT pin
`(delta_*, q_+^*)` — it only reduces `delta` to a finite set and
leaves `q_+` free.

**Named gap:** the residual `q_+` freedom is unchanged by the
doublet-phase-cubic construction. `q_+` is a singlet and cannot appear
in the `omega`-phase-cubed `Z_3`-character content.

## Candidate cubic selector

If `S(H) = 0` is the axiom-native selector equation on the
doublet-phase cubic, the DM active surface is reduced from the
2-real chamber `(delta, q_+)` with `delta >= 0, q_+ >= E_1 - delta`
to the union

```text
{delta = 0, q_+ free} ∪ {delta = m, q_+ free}
```

(the branch `delta = -m` is eliminated by the `Z_2` gauge `delta >= 0`
fixed by the carrier normal form).

This is genuinely progress: it halves (roughly) the residual
freedom. But it is not a PIN: `q_+` remains silent.

## Revised impossibility theorem status

The original Case 3 impossibility theorem's Theorems 3 and 4 should
be read as covering **trace moments and inserted Z_3-invariant
Hermitian operators** only. The present scout shows that extending the
operator class to non-Hermitian `omega`-eigenvectors of
`C_3`-conjugation (cubed into Z_3-invariants) DOES provide delta-odd
axiom-native content.

Proposed amendment to Theorem 3/4: "every retained `Z_3`-invariant
polynomial functional of `H` built from trace moments and
`Z_3`-invariant Hermitian operator insertions depends on `(delta,
q_+)` only through `(delta^2, q_+)`. Polynomial functionals built
from cubic combinations of `omega`-eigenvector trace insertions are
delta-odd but depend on `(m, delta)` only and do not involve `q_+`."

Therefore:

- The **`q_+`-silence** component of the impossibility theorem is
  NOT violated by the chart change; it stands.
- The **delta-evenness** component IS modified by the chart change:
  axiom-native delta-odd content exists but is `q_+`-blind.

## Explicit answer to the critical sub-question

**Is `Im(z^3) = 3 q_+^2 delta - delta^3` with `z = q_+ + i delta`
axiom-native, and if so what does it pin?**

NO, NOT in the form specified. The prompt's `z` mixes a `Z_3`-singlet
(`q_+`) with a `Z_3`-doublet-real-slice (`delta`) into a single
complex number, and this packaging is NOT a `Z_3`-irrep-natural
construction. Under `C_3`-conjugation, `z` does not simply rotate by
`omega`; the singlet and doublet parts transform differently. Hence
`z^3` is not retained-`Z_3`-invariant, and `Im(z^3)` is NOT an
axiom-native `Z_3`-invariant scalar.

**However,** there IS a closely related, correctly `Z_3`-irrep-natural
construction:

```text
A(H) := Tr(H T_{d,w}) = 3 delta + i sqrt(3) m,
S(H) := A^3 + conj(A)^3 = 54 delta (delta^2 - m^2).
```

`S(H)` IS a real, `Z_3`-invariant, delta-odd polynomial in `H`,
axiom-native at the `C_3`-character level. It pins `delta` (modulo the
Schur-fixed `m`) at `delta in {0, m}` on the positive-`delta` gauge.
**It does NOT involve `q_+`** and therefore does NOT pin `q_+`.

The axiom-native chart-change yields delta-selection but NOT
`q_+`-selection. The impossibility theorem's `q_+`-silence survives;
its delta-evenness claim does not (under the broader operator-class
admission).

## What this closes

- The "chart artifact" reading of delta-evenness is SHARPENED: the
  delta-even claim holds only for Hermitian-operator insertions;
  omega-eigenvector-cubed insertions DO yield delta-odd content.
- The prompt's specific `Im(z^3) = 3 q_+^2 delta - delta^3` is ruled
  out as axiom-native.
- The correct axiom-native delta-odd scalar is identified:
  `54 delta (delta^2 - m^2)`, independent of `q_+`.

## What this does not close

- `q_+`-selection remains axiom-silent at local-polynomial level.
- The integrated `(delta, q_+)` pin is still missing; the DM flagship
  selector gate is NOT closed by this chart change.
- Whether non-Hermitian omega-eigenvector operator insertions should
  be admitted as "retained axiom-native" remains a discipline question
  that must be resolved before promotion. The retained three-generation
  observable theorem establishes `M_3(C)` as the retained operator
  algebra on `H_hw=1`, which includes `T_{d,w}`, so the ingredient is
  retained; whether the `S(H)` scalar is RETAINED as an axiom-native
  observable requires a separate discipline call.

## Atlas position

- OBSTRUCTION scout, not flagship content.
- Candidate refinement of the Case 3 impossibility theorem's scope.
- Does NOT promote any retained candidate point
  (Schur-Q, det(H), Tr(H^2), F1, K_12) to theorem-grade.
- DOES NOT close the selector gate.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_z3_doublet_phase_chart_scout.py
```

## Paper-safe wording

> On the retained `hw=1` affine chart `(m, delta, q_+)`, the
> `C_3[111]`-conjugation doublet eigenvector `T_{d,w}` admits a
> complex trace-coordinate `A(H) = Tr(H T_{d,w}) = 3 delta + i sqrt(3)
> m`. The real Z_3-invariant combination `A^3 + conj(A)^3 = 54 delta
> (delta^2 - m^2)` is a delta-odd axiom-native polynomial functional
> in `H`, demonstrating that the delta-evenness claim of the Case 3
> impossibility theorem holds only for trace moments and
> Z_3-invariant Hermitian operator insertions, not for omega-eigenvector
> cubed insertions. The resulting selector pins `delta` modulo the
> Schur-fixed `m` at `{0, m}` but does NOT pin `q_+`. The DM flagship
> selector gate remains unclosed; the chart-change provides a PARTIAL
> delta-odd axiom-native content but no `q_+`-constraint.
