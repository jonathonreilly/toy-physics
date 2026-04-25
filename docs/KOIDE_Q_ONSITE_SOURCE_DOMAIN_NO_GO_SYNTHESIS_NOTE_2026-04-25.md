# Koide Q Onsite Source-Domain No-Go Synthesis

**Date:** 2026-04-25
**Status:** conditional support / retained no-go synthesis; not retained
native Koide closure
**Primary runner:**
`scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py`

---

## 1. Purpose

The April 25 full Koide workstream contains one useful new `Q` result:
it separates two source domains that had been blurred in earlier notes.

```text
onsite local scalar source functions on the three-generation orbit
```

and

```text
central/projected C3-commutant source labels
```

are not the same source domain.

This matters because the first domain would erase the residual `Z` coordinate
and close the conditional `Q = 2/3` support chain, while the second domain
still admits non-Koide values.  The branch also contains stronger positive
closure labels, but those labels do not land here: the source-domain retention
law is still missing.

---

## 2. Exact onsite source-domain fact

Let `C` be the cyclic permutation on the physical three-generation orbit and
let an onsite scalar source be

```text
J_site = diag(a,b,c).
```

The C3-invariance condition is

```text
C J_site C^(-1) = J_site.
```

It forces

```text
a = b = c.
```

Therefore the C3-fixed onsite scalar source space is one-dimensional:

```text
J_site = s I.
```

If the retained physical charged-lepton undeformed scalar source domain were
exactly this onsite function algebra, the residual traceless source coordinate
would be removed:

```text
z = 0.
```

Combined with the already-landed background-zero / `Z`-erasure criterion, this
would give

```text
z = 0 <=> K_TL = 0 <=> Q = 2/3.
```

That is a genuine conditional positive result.

---

## 3. Exact commutant-source obstruction

The retained projected source grammar also contains the C3-commutant projectors

```text
P_plus = (I + C + C^2)/3,
P_perp = I - P_plus,
Z = P_plus - P_perp.
```

Equivalently,

```text
Z = -I/3 + (2/3) C + (2/3) C^2.
```

This `Z` is C3-invariant and satisfies

```text
Z^2 = I.
```

But it is not an onsite diagonal source function.  It has offsite entries in
the site basis.  The exact intersection is only the common scalar:

```text
onsite local functions  cap  End_C3(V) = span{I}.
```

So the source-domain choice is load-bearing.  Onsite source functions erase
`Z`; the retained central/projected commutant source grammar keeps it visible.

---

## 4. Counterdomain

On the normalized reduced two-channel carrier, write the source-relevant
coordinate as

```text
Y_Z(z) = diag(1+z, 1-z).
```

The Koide readout from the April 25 criterion note is

```text
Q(z) = 2 / (3(1+z)).
```

The zero-source point gives the Koide value:

```text
z = 0 -> Q = 2/3, K_TL = 0.
```

But the retained central/projected source grammar also admits, for example,

```text
z = -1/3 -> Q = 1, K_TL = 3/8.
```

This is the exact counterdomain.  It preserves C3 at the central/projected
source level while failing to close `Q = 2/3`.

---

## 5. What lands

This note lands the following science from the full Koide workstream:

1. strict onsite C3-invariant scalar source functions are only common scalars;
2. the projected `Z = P_plus - P_perp` source is C3-invariant but not onsite;
3. onsite source grammar would conditionally close `Q` through `z=0`;
4. the current retained commutant/projected grammar still admits nonclosing
   `zZ`;
5. the remaining `Q` primitive is now a source-domain theorem, not a new
   numerical Koide calculation.

---

## 6. What does not land

This note does not prove:

1. that the physical undeformed charged-lepton scalar source domain equals the
   onsite local function algebra;
2. that central/projected `Z` is a pure probe deformation rather than allowed
   undeformed source data;
3. that a parity, mixer, quotient, or potential law forces the odd source
   coefficient to vanish;
4. full retained `Q = 2/3` closure;
5. any retained closure of the Brannen phase `delta = 2/9`.

The branch's stronger positive full-closure labels, including the claimed full
dimensionless source-domain closure and the direct physical `Q` / `delta`
assignments, are not retained on `main`.

---

## 7. Residual theorem target

The next live theorem target is now:

```text
derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant
```

Equivalent formulations would also work:

```text
exclude_Z_as_undeformed_charged_lepton_source_data
derive_Z_as_probe_only_not_background
derive_a_plus_perp_mixer_or_parity_that_forces_z_zero
derive_physical_source_free_reduced_carrier_selection
```

Until one of these is retained, the `Q` lane remains open.

---

## 8. Closeout flags

```text
KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS=TRUE
STRICT_ONSITE_C3_SOURCE_DOMAIN_ERASES_Z=TRUE
CONDITIONAL_Q_CLOSES_IF_ONSITE_SOURCE_DOMAIN_RETAINED=TRUE
CURRENT_RETAINED_COMMUTANT_SOURCE_DOMAIN_ADMITS_Z=TRUE
Q_RETAINED_NATIVE_CLOSURE=FALSE
DELTA_RETAINED_NATIVE_CLOSURE=FALSE
FULL_DIMENSIONLESS_KOIDE_CLOSURE=FALSE
RESIDUAL_Q=derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant
```
