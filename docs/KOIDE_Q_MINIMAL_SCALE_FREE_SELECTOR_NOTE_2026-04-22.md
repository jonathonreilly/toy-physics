# Koide Q Minimal Scale-Free Selector

**Date:** 2026-04-22
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Status:** exact support theorem on the admitted second-order `Q` carrier;
does not close native Koide `Q`
**Purpose:** tighten the `Q` route on the admitted second-order returned
carrier by showing that the selector variable is not an arbitrary quadratic
choice.

The key statement is:

> on the exact second-order returned mass carrier, there is no nontrivial
> scale-free `C_3`-covariant scalar at linear order, and at quadratic order
> there is exactly **one** nontrivial scale-free invariant ratio.

That ratio is equivalently:

- `E_perp / E_+`,
- `(r1^2 + r2^2) / (2 r0^2)` in the Fourier-coordinate normalization used
  below,
- `2 / kappa`,
- or `Q`.

So once the second-order carrier is admitted, the selector variable itself is
already unique up to reparametrization.

**Primary runner:** `scripts/frontier_koide_q_minimal_scale_free_selector.py`

---

## 1. Carrier

The returned charged-lepton mass object on `T_1` is the three-slot real vector

```text
x = (u, v, w),
```

or equivalently its cyclic Fourier image

```text
H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2.
```

The selector should be:

- `C_3`-covariant / invariant,
- local to the returned carrier,
- and scale-free.

---

## 2. Linear order

A real linear scalar on `x` has the form

```text
L(x) = a u + b v + c w.
```

Imposing invariance under the species 3-cycle forces

```text
a = b = c,
```

so the only invariant linear scalar is

```text
L(x) ∝ u + v + w = r0.
```

But `r0` is degree-1 and therefore not scale-free:

```text
r0(t x) = t r0(x).
```

So there is no nontrivial scale-free invariant at linear order.

---

## 3. Quadratic order

At quadratic order, the invariant scalar space is exactly two-dimensional:

```text
Q(x) = A r0^2 + C (r1^2 + r2^2).
```

Both basis elements are degree-2, so after quotienting by overall scale there
is exactly one nontrivial ratio:

```text
rho_Q = E_perp / E_+
      = (r1^2 + r2^2) / (2 r0^2)
      = 2 / kappa.
```

Here `kappa` is the existing circulant convention `a^2 / |b|^2`, under which
the doublet block carries the factor `2`.

Equivalently,

```text
Q = (1 + rho_Q) / 3.
```

The raw Fourier-coordinate ratio

```text
rho_F = (r1^2 + r2^2) / r0^2
```

therefore satisfies `rho_F = 2 rho_Q`. This note uses `rho_Q` for the
physical block-energy ratio that appears in the Koide scalar.

Therefore the minimal nontrivial scale-free invariant selector on the returned
carrier is unique up to reparametrization.

---

## 4. Consequence

This removes another apparent choice from the support `Q` route.

The remaining theory choices are now:

1. identify the physical selector carrier with the exact second-order returned
   mass operator,
2. identify the physical selector **value law** on the unique minimal scale-free
   invariant of that carrier.

The selector variable itself is no longer a separate ambiguity.

---

## 5. Bottom line

Once the second-order returned carrier is accepted, the unique minimal
scale-free `C_3`-invariant selector variable is already fixed:

```text
E_perp / E_+   <->   2/kappa   <->   Q.
```

So the only remaining substantive question is not "which invariant?" but
"what physical value law picks the relevant point on that one-variable family?"


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_dirac_realization_gate_note_2026-05-03](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
