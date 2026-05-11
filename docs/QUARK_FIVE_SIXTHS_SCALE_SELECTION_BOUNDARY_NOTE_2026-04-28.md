# Quark Five-Sixths Scale-Selection Boundary

**Date:** 2026-04-28
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** (1) staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`); (2) g_bare = 1 derivation target (canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md)).

**Status:** support / exact negative boundary / scale-selection theorem target for Lane
3 target 3A. This block-04 stretch attempt attacks the down-type `5/6`
bridge residual. It does not prove the non-perturbative exponentiation
mechanism, does not derive the threshold-local scale choice, and does not
claim retained `m_d`, `m_s`, or `m_b`.

**Primary runner:**
`scripts/frontier_quark_five_sixths_scale_selection_boundary.py`

## 1. Question

The bounded down-type route uses

```text
|V_cb| = (m_s/m_b)^(5/6),
5/6 = C_F - T_F = 4/3 - 1/2.
```

The current support packet shows a strong threshold-local match:

```text
m_s(2 GeV) / m_b(m_b)
```

is within about `0.2%` of the framework prediction. The same bridge is not
equally good on the common-scale comparison

```text
m_s(m_b) / m_b(m_b).
```

This note asks whether exact `C_F - T_F = 5/6` plus the CKM atlas value of
`|V_cb|` is enough to promote the down-type bridge, or whether a separate
scale-selection theorem is load-bearing.

## 2. Minimal Premise Set

Allowed premises:

1. exact `SU(3)` group theory:

   ```text
   C_F = 4/3, T_F = 1/2, C_F - T_F = 5/6;
   ```

2. retained CKM atlas leading value:

   ```text
   |V_cb| = alpha_s(v) / sqrt(6);
   ```

3. inherited comparator data from the existing bounded support note:

   ```text
   m_s(2 GeV), m_b(m_b), alpha_s(2 GeV), alpha_s(m_b);
   ```

4. standard one-loop quark-mass transport as inherited comparator context:

   ```text
   m_s(2 GeV) / m_s(m_b)
     = [alpha_s(2 GeV) / alpha_s(m_b)]^(12/25).
   ```

Forbidden proof inputs:

1. observed quark masses as derivation inputs;
2. fitted Yukawa entries;
3. using the better comparator surface as a theorem step;
4. treating `C_F - T_F = 5/6` as a non-perturbative scale theorem;
5. claiming retained down-type masses before the scale choice is derived.

## 3. Exact And Bounded Parts

The exact part remains narrow:

```text
C_F - T_F = 5/6,
|V_cb|_atlas = alpha_s(v) / sqrt(6).
```

If the bridge is granted, the predicted ratio is unique:

```text
R_pred = (m_s/m_b)_pred = |V_cb|^(6/5).
```

Using the repo's canonical same-surface value of `alpha_s(v)`, this gives

```text
R_pred = 0.0223897...
```

The threshold-local comparator is

```text
R_self = m_s(2 GeV) / m_b(m_b) = 0.0223445...
```

so `R_pred/R_self - 1 = +0.20%`.

That is real bounded support. It is not a scale theorem.

## 4. Scale-Selection Wall

One-loop transport relates the threshold-local and common-scale comparators:

```text
R_self = R_same * T,
T = [alpha_s(2 GeV) / alpha_s(m_b)]^(12/25).
```

With the values inherited from the existing support note,

```text
T = 1.147466...
R_same = 0.0194729...
```

The same predicted ratio then differs from the common-scale comparator by
about `+15%`.

Equivalently, the exponent inferred from a fixed CKM value depends on the
chosen mass-ratio surface:

```text
p_self = log(|V_cb|_atlas) / log(R_self) = 0.832890...
p_same = log(|V_cb|_atlas) / log(R_same) = 0.803802...
```

The threshold-local surface is close to `5/6 = 0.833333...`; the common-scale
surface is not. The difference is not numerical noise. It is the expected
effect of the nontrivial transport factor. For the same exponent to be exact
on both surfaces, one would need

```text
T^(5/6) = 1,
```

but the current inherited transport gives

```text
T^(5/6) = 1.121459...
```

So the `5/6` bridge has two separate load-bearing parts:

1. a non-perturbative exponentiation mechanism at the lattice/threshold
   surface;
2. a framework theorem selecting the threshold-local self-scale surface, or
   an RG-covariant transport theorem explaining why that is the correct
   observable for the bridge.

The exact Casimir identity supplies neither by itself.

## 5. Fan-Out Frames

The block-04 stretch attempt checked five frames:

1. **Casimir frame.** `C_F - T_F = 5/6` is exact, but a group rational is not
   an exponentiation mechanism.
2. **CKM-atlas frame.** `|V_cb| = alpha_s(v)/sqrt(6)` is retained, but the
   atlas gives a mixing amplitude, not a mass-ratio scale convention.
3. **Threshold-local frame.** The bridge is numerically sharp on
   `m_s(2 GeV)/m_b(m_b)`, so it remains valuable bounded support.
4. **Common-scale frame.** The same exponent on `m_s(m_b)/m_b(m_b)` fails by a
   material amount.
5. **RG-covariant frame.** A promotion route must derive the scale surface or
   supply a covariant transport theorem; choosing the better surface is an
   admitted comparator convention, not closure.

All frames agree that a retained 3A result cannot be obtained by citing
`C_F - T_F = 5/6` alone.

## 6. Theorem

**Theorem (five-sixths scale-selection boundary).** In the current Lane 3
down-type support stack, exact `SU(3)` group theory and the retained CKM atlas
value of `|V_cb|` determine the bounded prediction

```text
(m_s/m_b)_pred = |V_cb|^(6/5)
```

only after the `5/6` bridge and an observation surface are supplied. Because
the inherited one-loop transport factor between `m_s(2 GeV)/m_b(m_b)` and
`m_s(m_b)/m_b(m_b)` is nontrivial, the same fixed exponent cannot be an exact
scale-blind theorem on both surfaces. Therefore a retained 3A proof still
requires an independent scale-selection or RG-covariant transport theorem in
addition to the non-perturbative exponentiation mechanism.

## 7. What This Retires

This retires the overread:

```text
C_F - T_F = 5/6 and the threshold-local match is good,
therefore the 5/6 down-type bridge is retained.
```

The honest current status is narrower:

```text
exact Casimir rational + retained CKM value
+ threshold-local comparator convention
=> strong bounded support,
not retained down-type mass-ratio closure.
```

## 8. What Remains Open

Lane 3 target 3A remains open. A future retained route must supply at least
one of:

1. a non-perturbative theorem deriving the `5/6` exponentiation mechanism at
   the relevant lattice/threshold surface;
2. a scale-selection theorem deriving the threshold-local self-scale surface;
3. an RG-covariant bridge showing how the same framework law transports
   between scale surfaces without using observed quark masses as inputs.

Until then, down-type ratios remain bounded support and cannot retain
`m_d`, `m_s`, or `m_b`.

## 9. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_five_sixths_scale_selection_boundary.py
```

Expected result:

```text
TOTAL: PASS=34, FAIL=0
VERDICT: 5/6 remains bounded support until a scale-selection or
RG-covariant transport theorem is supplied.
```


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on **both** open gates:

1. **Staggered-Dirac realization derivation target** — canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`); in-flight supporting work: `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, `THREE_GENERATION_STRUCTURE_NOTE.md`, `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, `scripts/frontier_generation_rooting_undefined.py`, `GENERATION_AXIOM_BOUNDARY_NOTE.md`.
2. **`g_bare = 1` derivation target** — canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) (`claim_type: positive_theorem`, `audit_status: audited_conditional`); in-flight supporting work: `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`, `G_BARE_RIGIDITY_THEOREM_NOTE.md`, `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`, `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`, `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`, `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`, `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`.

The note produces (or directly supports) a quantitative gauge prediction (Wilson plaquette content, `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2`, `β = 6`, CKM/quark/hadron mass hierarchy, action-unit metrology, etc.) by fixing `g_bare = 1` without independently deriving it — therefore both gates must close for the lane to upgrade.

Therefore `claim_type: bounded_theorem` until both gates close. When both gates close, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
