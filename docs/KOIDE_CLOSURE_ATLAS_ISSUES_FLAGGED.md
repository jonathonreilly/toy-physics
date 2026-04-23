# Atlas Issues Flagged During Koide Support Review

**Date:** 2026-04-21
**Context:** issues found while reviewing retained atlas items cited by the
April 22 Koide support batch.

Flagging for reviewer attention; several are genuine caveats that matter for
how strongly the Koide lane can be stated on the package surface.

---

## Issue 1: `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` — mismatch between circulant Hermitian eigenvalues and Brannen/Rivero `√m` form

**Claim in retained note:**
> "every Hermitian operator commuting with the C_3[111] action is
> circulant, and its eigenvalue triple has exactly the Brannen/Rivero
> cosine form... If one further assumes the matrix-space equipartition
> condition A1 and the phenomenological identification P1, then Koide
> Q = 2/3 follows algebraically."

**Issue:**

- Brannen/Rivero form on √m_k:   `√m_k = v_0 (1 + √2 cos(δ + 2πk/3))`
- Circulant Hermitian eigenvalues: `λ_k = a + 2|b| cos(arg(b) + 2πk/3)`
  (shifted cosine)

These are NOT the same form. If we identify `λ_k = m_k` (operator
eigenvalues are masses), then `m_k = a + 2|b|·cos(...)`, which is
NOT `v_0²(1 + √2 cos)²`. The operator eigenvalue form gives a shifted
cosine in `m`, not in `√m`.

The `A1 + P1` conditions in the retained note are precisely the missing
bridge: **A1** (equipartition `2|b|/a = √2`) plus **P1** (phenomenological
identification `√m_k = λ_k^{1/2}` — i.e. amplitudes `√m_k` are square
roots of operator eigenvalues) are needed to recover the Brannen form.

Without A1 + P1, Q = 2/3 does NOT follow from circulant Hermitian
structure alone.

**Separately:** Q = 2/3 IS an algebraic identity of the Brannen/Rivero
parametrization `√m_k = v_0(1 + √2 cos(...))` with NO A1 + P1 needed
(uses only Σ cos = 0 and Σ cos² = 3/2). So the retained claim
"Q = 2/3 follows algebraically given A1 + P1" is correct, but the
retained statement needs to clarify that it is specifically the bridge
between circulant eigenvalues and Brannen √m-form that requires A1 + P1,
NOT the Brannen → Q = 2/3 step itself.

**Flag:** the retained note should clarify which algebraic identity is
A1 + P1 dependent and which is automatic.

---

## Issue 2: `KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md` — "coordinate-closed" claim uses observational H_* witness

**Claim in retained note:**
> "The line parameter `m` is fixed by the first continuous hit of the
> route-invariant reachable-slot ratio `r = w/v` of the earlier `H_*`
> one-clock witness... So the current positive candidate route is now
> coordinate-closed. There are no free internal parameters left on this
> lane."

**Issue:**

The `H_*` witness is derived from the PMNS observational chamber pin
(retained `G1 observational chamber pin (PMNS-pinned)` at
`(m, δ, q_+) = (0.657, 0.934, 0.715)` in
`scripts/frontier_higgs_dressed_propagator_v1.py`). This is an
**observational** input (PDG-matched PMNS angles), NOT a framework-
axiom-derived quantity.

So the "coordinate-closed" claim in the retained note is technically
correct in the sense that no *additional* free parameters remain beyond
retained inputs, but the `H_*` witness itself is observational.

**Flag:** the retained note should mark the `H_*` witness as an
observational pin, so the "coordinate-closed" status is understood as
"closed modulo the observational H_* pin." The current phrasing reads
as full framework closure, which is stronger than what is actually
established.

This matters for the Koide lane because the selected-line physical
`m_*` is retained via `H_*` matching, making `m_*` observational on the
current canonical surface. The April 22 support batch adds a useful
numerical consistency check:
`frontier_koide_as_pin_replaces_h_star_witness.py` shows that solving
the candidate AS phase condition on the retained selected line lands on
the same `m_*` to <0.003% deviation. That is important support, but it
does **not** by itself discharge the physical Brannen-phase bridge.

---

## Issue 3: `v_0` formula in KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE uses (7/8) potentially twice

**Claim in retained note:**
> "v_0 ≈ √[v_EW × α_LM² × (7/8)] / (1 + √2 cos(2/9)) = 17.696 √MeV
>  vs 17.716 √MeV (0.11% off)
> ...
> The hierarchy theorem retains `v = M_Pl × (7/8)^(1/4) × α_LM^{16}`,
> but that does not by itself supply an independent lepton-sector
> first-power (7/8) factor, and reusing (7/8) in that way would risk
> double-counting."

**Issue:**

The retained note explicitly flags the `(7/8)` potential double-counting
but still writes the candidate formula with the doubled `(7/8)` factor.
The resulting `v_0` prediction is 0.11% off from the observed value.

**Alternative (found in this closure work):**

Using `y_τ^fw = α_LM/(4π)` instead, the `v_0` prediction is:
```
v_0 = √m_τ / (1 + √2 cos(2/9))     where m_τ = v_EW · α_LM/(4π)
```
This matches observed `v_0 = 17.71556 √MeV` at 0.002% (50× tighter
than the (7/8)-reused formula) and uses only retained atlas primitives
with no `(7/8)` double-counting concern.

**Flag:** the retained `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE` can
be strengthened by replacing the candidate `v_0 = √[v_EW · α_LM² · (7/8)]`
formula with `v_0 = √[v_EW · α_LM · (4π)^{-1}]`, which is 50× tighter
and avoids the `(7/8)` reuse concern.

---

## Issue 4: `scripts/frontier_higgs_dressed_propagator_v1.py` — `M_STAR`, `DELTA_STAR`, `Q_PLUS_STAR` are observational but not labeled as such

**Claim:**
The retained `H_STAR_3` operator is defined at
`(m, δ, q_+) = (0.657, 0.934, 0.715)` (the "G1 observational chamber
pin"), with the comment:
```
# G1 observational chamber pin (PMNS-pinned)
```

**Issue:**

The comment correctly notes this is "PMNS-pinned" (i.e. observational),
but downstream retained derivations built on `H_STAR_3` may implicitly
carry this observational input forward without explicit labeling.

**Flag:** retained notes citing `H_STAR_3` should explicitly mark the
`(m, δ, q_+)_*` values as observational pins from PMNS, so the
downstream derivations' observational dependency is transparent.

---

## Issue 5: Consolidation suggestion — addressed by this package

Several retained notes treat `α_LM/(4π)` as a 1-loop lattice PT factor
(e.g. `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`).
The April 22 support batch extends that to the charged-lepton sector via
the gauge-by-gauge Casimir enumeration in
`frontier_charged_lepton_yukawa_diagrammatic_enumeration.py` together with
the retained-matching cross-check in
`frontier_charged_lepton_yukawa_bz_quadrature_explicit.py`, supporting:

> "Charged-lepton Yukawa lattice-PT theorem: at 1-loop lattice
> perturbation theory on the retained `Cl(3)/Z³` Wilson-plaquette +
> 1-link staggered-Dirac canonical surface, the tau Yukawa coupling
> in framework convention equals `y_τ^fw = α_LM/(4π)` with Casimir
> coefficient `C_τ = 1` from the charged-lepton (colorless) group
> structure."

This materially strengthens support for the tau mass / `v_0` lane, but
it does **not** by itself close that scale bridge at theorem grade.

---

## Summary for reviewer

These flags are still scientifically important on the canonical review
surface. In particular:

- Issue 1 is part of the still-open A1/source-law bridge;
- Issues 2 and 4 matter for the still-open selected-line/Brannen
  physical bridge;
- Issue 3 matters for the still-bounded charged-lepton scale lane.

But fixing these issues in the retained notes would:
- Tighten the retained `KOIDE_CIRCULANT_CHARACTER_DERIVATION` note's
  A1+P1 role clarity (Issue 1)
- Mark the `H_*` witness observational dependency (Issues 2, 4)
- Upgrade the retained `v_0` formula to the 50× tighter
  `α_LM/(4π)` form (Issue 3)
- Strengthen the charged-lepton radiative/Yukawa support lane via
  explicit gauge-by-gauge enumeration and BZ cross-checks (Issue 5)
