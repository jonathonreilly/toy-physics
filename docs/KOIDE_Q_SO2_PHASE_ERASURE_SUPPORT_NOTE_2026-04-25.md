# Koide Q SO(2) Phase-Erasure Support Note

**Date:** 2026-04-25
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Status:** exact support theorem on the Brannen-parameterized `Q` route;
not retained native Koide closure
**Primary runner:**
`scripts/frontier_koide_q_so2_phase_erasure_support.py`

---

## 1. Purpose

The reviewed `koide-closure-targets-AB` branch contained one useful
object-level theorem and one overpromotion.  This note lands only the useful
part.

For the Brannen square-root mass carrier

```text
sqrt(m_k) = V0 * (1 + c cos(delta + 2 pi k / 3)),    k = 0,1,2,
```

the Koide ratio

```text
Q = (m_0 + m_1 + m_2) / (sqrt(m_0) + sqrt(m_1) + sqrt(m_2))^2
```

is exactly

```text
Q = (c^2 + 2) / 6.
```

Therefore `Q` is independent of both the overall scale `V0` and the Brannen
phase `delta`.  Equivalently, the `Q` observable erases the SO(2) doublet
angle on this carrier.

The note does **not** promote `Q=2/3` or `delta=2/9 rad` to retained closure.
It records the exact algebraic support theorem that narrows the remaining
open primitive.

---

## 2. Exact C3 trigonometry

Let

```text
theta_k = delta + 2 pi k / 3,    k = 0,1,2.
```

The two required `C3` identities are

```text
sum_k cos(theta_k) = 0,
sum_k cos(theta_k)^2 = 3/2.
```

They are the real and quadratic projections of the three cube roots of unity.
No mass input and no observed charged-lepton data enter.

---

## 3. Phase-erased `Q` formula

Set

```text
s_k = sqrt(m_k) = V0 * (1 + c cos(theta_k)).
```

Then

```text
sum_k s_k = 3 V0,
```

and

```text
sum_k m_k = sum_k s_k^2
          = V0^2 * sum_k (1 + 2c cos(theta_k) + c^2 cos(theta_k)^2)
          = V0^2 * (3 + (3/2)c^2)
          = (3 V0^2 / 2) * (2 + c^2).
```

So

```text
Q = [sum_k m_k] / [sum_k s_k]^2
  = [(3 V0^2 / 2)(2 + c^2)] / (9 V0^2)
  = (c^2 + 2) / 6.
```

Consequences:

```text
dQ/d(delta) = 0,
dQ/dV0 = 0,
Q(delta + phi) = Q(delta).
```

The Brannen phase is invisible to `Q`; it belongs to the separate selected-line
phase lane.

---

## 4. Conditional Koide point

The exact formula gives

```text
Q = 2/3  <=>  c^2 = 2.
```

Thus every proposed route that derives `c^2=2` on this Brannen carrier
immediately implies Koide `Q=2/3`.

The earlier AM-GM / reduced-carrier support stack can be read in this language
as the conditional equal-energy premise

```text
E_plus = E_perp,
3 a^2 = 6 |b|^2,
c^2 = (6 |b|^2) / (3 a^2) = 2.
```

That is a useful exact compatibility statement, but it is still conditional on
the physical theorem selecting that reduced carrier and source-free saddle.

---

## 5. What this note closes

This note closes the following support facts:

1. `Q` on the Brannen square-root carrier is exactly `(c^2+2)/6`.
2. `Q` is invariant under the carrier SO(2) phase rotation
   `delta -> delta + phi`.
3. `Q=2/3` is equivalent to `c^2=2` on that carrier.
4. The `delta` lane cannot be inferred from `Q`; `Q` erases `delta`.

---

## 6. What this note does not close

This note does **not** prove:

1. that the physical charged-lepton observable must use this Brannen carrier;
2. that retained charged-lepton physics selects `c^2=2`;
3. that the physical source-domain law is source-free on the reduced carrier;
4. that `delta_Brannen = 2/9 rad`;
5. the selected-line local boundary-source, based-endpoint, or Type-B
   rational-to-radian readout laws;
6. full retained dimensionless Koide closure.

So the retained status of charged-lepton Koide is unchanged: this is an exact
support theorem and a bridge-targeting tool.

---

## 7. Closeout flags

```text
KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT=TRUE
KOIDE_Q_INDEPENDENT_OF_BRANNEN_PHASE_AND_SCALE=TRUE
KOIDE_Q_CONDITIONAL_C2_EQ_2_IMPLIES_Q_2_OVER_3=TRUE
KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE
KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE
SOURCE_DOMAIN_RETENTION_PRIMITIVE_RESOLVED=FALSE
RESIDUAL_Q=derive_physical_source_free_reduced_carrier_selection_or_equivalent_c2_eq_2_law
RESIDUAL_DELTA=derive_selected_line_boundary_source_based_endpoint_and_Type_B_radian_readout
```


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
