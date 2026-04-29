# Chronology Protection Boundary Review Packet

**Date:** 2026-04-25
**Status:** review-hardening packet for the chronology-protection boundary lane
**Scope:** retained single-clock, local-data `Cl(3)/Z^3` chronology surface
**Companions:**
[CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md](CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md),
[U_MINUS_T_VS_PAST_SIGNALING_NOTE.md](U_MINUS_T_VS_PAST_SIGNALING_NOTE.md),
[CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md](CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md)

## Claim Boundary

The retained claim is narrow:

> On the retained single-clock, local-data framework surface, the theory admits
> reversible reconstruction but no operational signaling to an earlier durable
> record.

Do not inflate this into a universal no-time-travel theorem. The packet does
not disprove closed timelike curves, postselected quantum mechanics, absorber
theories, advanced-field formalisms, or multi-time systems. It classifies the
extra structure those theories import relative to the retained surface.

An operational past-signal claim must show a controllable choice at `t1`
changing which durable record physically existed at `t0 < t1`, while retaining
the same single-clock local Cauchy-data semantics. Retrodiction, conditioning,
symmetry-related solutions, full closed-state reversal, and global consistency
constraints do not by themselves meet that standard.

## Hostile Objections And Answers

| objection | strongest hostile version | bounded answer |
|---|---|---|
| `U(-t)` means time travel | If `U(-t) = U(t)^dagger` exists, then a later agent can just run the system backward and change the past. The theorem is playing word games by calling this reconstruction. | `U(-t)` is a global inverse map on a closed state. It reconstructs the earlier slice from the later slice as an equation. It is not a local operation at `t1` whose output is the already-realized slice at `t0`. If implemented physically as a Loschmidt echo, it must reverse the record, environment, apparatus, and agent memory included in the closed state. That is not a retained message to the past. |
| CPT/T allows backward causation | Time reversal and CPT symmetry already say the laws permit backwards propagation. Denying backward causation contradicts the symmetry. | A symmetry maps one solution to a symmetry-related solution. It does not give an agent inside one solution a same-history control knob that edits an earlier durable record. The chronology argument is not carried by CPT. The exact free-lattice CPT/T result is compatible with the boundary, but the load-bearing assumptions are one Hamiltonian clock, local Cauchy data, and retarded causal support. |
| Advanced fields are backward signals | Advanced Green functions make earlier fields depend on later sources. That is precisely a signal into the past. | In an advanced solve, later source data are supplied to the boundary-value problem for the earlier field. That is future-boundary import. The retained surface uses retarded support, where earlier fields do not depend on later source toggles. Absorber or time-symmetric formalisms may be studied, but unless they rederive the dependence as a retained local operation, they are outside this theorem's surface. |
| Postselection changes the past | Later selection changes earlier statistics, so it changes what happened. P-CTC and final-state projection models make the point explicit. | Ordinary postselection changes `P(past | later outcome)` and the accepted subensemble. It does not edit discarded runs or alter an already-realized durable record in one run. If postselection is promoted to deterministic dynamics, the accepted-state map imports a final boundary and usually becomes nonlinear or non-CPTP relative to the retained local surface. That is an outside theory surface, not a retained past signal. |
| CTCs can be paradox-free | Novikov-style consistency and Deutsch-style fixed points avoid paradoxes. Therefore paradox absence defeats the chronology argument. | Paradox-free CTCs can exist as mathematical constructions. The answer is not "CTCs are inconsistent." The answer is that loop consistency is a global fixed-point or admissibility constraint. Arbitrary local codimension-1 data are no longer freely evolved by one forward Hamiltonian clock. A unique fixed point removes free control; multiple fixed points need an extra selector; no fixed point rejects the attempted data. All are outside retained local Cauchy semantics. |
| Loschmidt echo erases records | A perfect echo can erase the record, so durable records do not protect chronology. | A perfect finite echo is allowed in principle. The boundary is what it reverses. Partial reversal leaves record or environment witnesses. Full zero-witness reversal includes the entire closed record sector: visible record, environment copies, apparatus marks, and memory of the echo intervention. That produces a later state equivalent to a pre-record configuration; it is not a selective edit of the earlier durable record while the later lab remains intact. |
| Multi-time theories exist | There are multi-time wave equations, ultrahyperbolic systems, extra-time models, and constrained support theories. A single-clock theorem cannot rule them out. | Correct. The theorem does not rule them out. It says they are not the retained single-clock codimension-1 local-data surface. Multi-time well-posedness normally requires nonlocal support constraints on admissible data. A generic local perturbation of one slice need not remain admissible. That is a different theory class, not a counterexample inside this lane. |
| Durable records are not yet fully derived | The proof assumes durable records, but the framework has not fully derived endogenous record formation. Then the chronology claim is incomplete. | This is a real limitation. The chronology lane now includes a finite redundant-carrier model showing what is sufficient once records form, but it still does not solve the measurement problem or derive macroscopic record formation. The present claim is conditional on formed physical records, not a complete derivation of why records form. |
| This only proves by assumption | The theorem assumes single clock, DAG/retarded support, no final boundary, no postselection, and durable records. Of course past signaling is absent if you assume away every mechanism that could provide it. | Yes, the result is conditional. That is the point. The lane is a boundary classifier, not an absolute metaphysical prohibition. Its value is to prevent hidden imports from being mistaken for consequences of the retained framework. A construction with late-to-early control must identify which assumption it drops and what replaces it. That is useful even when the outside theory is consistent. |

## Objection-Specific Red Lines

### `U(-t)` And Inverse Evolution

Accept:

- `U(-t)` exists for closed unitary evolution.
- A full state at `t1` determines the corresponding earlier closed state.
- A laboratory could approximate an echo on degrees it controls.

Reject:

- `U(-t)` as a late local operation on only the desired subsystem.
- Selective erasure of the earlier record while keeping all later witnesses.
- Treating mathematical reconstruction as a controllable same-history message.

Probe support:

- `scripts/loschmidt_echo_record_probe.py`
- `scripts/partial_loschmidt_record_lower_bound.py`
- `scripts/durable_record_formation_boundary_probe.py`

### CPT, T, And Backward Causation

Accept:

- T maps a solution to a time-reversed solution.
- CPT can be an exact structural symmetry on the stated free-lattice surface.
- Symmetry-related histories are legitimate equation-level objects.

Reject:

- "CPT permits time travel" as a chronology proof.
- "T symmetry gives an agent an operation that changes yesterday."
- Reliance on an unfinished interacting CPT extension for the chronology lane.

The chronology proof should stand even if the CPT discussion is removed. The
retained boundary comes from single-clock Cauchy data and retarded causal
support.

### Advanced And Symmetric Field Solves

Accept:

- Advanced Green-function calculations can make earlier field values depend on
  later source data.
- Time-symmetric or absorber formalisms may be coherent external frameworks.

Reject:

- Calling future-boundary data a retained local past-directed signal.
- Treating a half-advanced term as import-free merely because it is symmetric.

Probe support:

- `scripts/advanced_vs_retarded_field_probe.py`
- `scripts/future_boundary_import_index.py`

### Postselection And Final Boundaries

Accept:

- Postselection changes accepted-subensemble statistics.
- Final-state projection or P-CTC-style models can be defined as external
  models.
- Retrodictive probabilities can shift when conditioning on a later event.

Reject:

- "Discarded runs were changed."
- "Conditioning physically rewrote the individual past record."
- Hiding final-boundary/nonlinear dynamics inside the retained local channel.

Probe support:

- `scripts/postselection_ctc_nonlinearity_probe.py`
- `scripts/postselection_no_signaling_audit.py`

### CTC Fixed Points

Accept:

- Paradox-free CTC models can be mathematically formulated.
- Nonsingular loop equations may have unique fixed points.
- Singular loop equations may impose consistency constraints and leave selector
  freedom.

Reject:

- Treating fixed-point existence as retained arbitrary local Cauchy evolution.
- Treating a unique fixed point as a freely chosen late message.
- Treating multiple fixed points as predictive without an added selector.

Probe support:

- `scripts/chronology_cycle_insertion_probe.py`
- `scripts/causal_cycle_fixed_point_dimension_probe.py`
- `scripts/ctc_fixed_point_taxonomy_probe.py`

### Multi-Time Theories

Accept:

- Multi-time and ultrahyperbolic theories can be studied.
- They may have their own admissible support classes.

Reject:

- Claiming they preserve the retained one-clock, arbitrary local slice-data
  semantics without proof.
- Using a constrained multi-time theory as an internal counterexample to the
  retained single-clock theorem.

Probe support:

- `scripts/multi_time_support_constraint_probe.py`

### Durable Records

Accept:

- Endogenous durable-record formation is not fully derived in this lane.
- The measurement/record lane remains broader than this packet.

Reject:

- Omitting already-formed record/environment/apparatus degrees from the state.
- Reversing only the convenient subsystem and declaring the past record erased.

The honest statement is: once records are physical degrees of freedom, they
must be included in any reversal or channel analysis.

Probe support:

- `scripts/chronology_operator_algebra_no_past_signal_probe.py`
- `scripts/durable_record_formation_boundary_probe.py`

## What Would Actually Defeat The Retained Claim

A genuine counterexample inside the retained surface would need all of the
following:

1. one strongly continuous Hamiltonian clock `U(t) = exp(-itH)`;
2. freely specifiable admissible local data on one codimension-1 slice;
3. retarded or DAG-compatible support, with no hidden late-to-early edge;
4. no final boundary, postselection rule, or global fixed-point constraint;
5. durable record, apparatus, and environment carriers included in the state;
6. a controllable operation at `t1` that changes which durable record physically
   existed at `t0 < t1`.

Known apparent counterexamples fail by dropping at least one item. That does
not make them inconsistent. It classifies them as outside the retained surface.

Classifier support:

- `scripts/chronology_import_budget.py`

## Review Answers In One Line

| hostile claim | one-line answer |
|---|---|
| `U(-t)` is time travel. | It is full closed-state inverse reconstruction, not a local past-signal channel. |
| CPT/T gives backward causation. | It gives symmetry-related solutions, not same-history control over earlier records. |
| Advanced fields signal backward. | They import future boundary data; retained retarded support has no such channel. |
| Postselection changes the past. | It changes conditional ensembles or imports a final boundary, not discarded runs. |
| CTCs can be paradox-free. | Yes, by global consistency or fixed points, which are outside local Cauchy evolution. |
| Loschmidt echoes erase records. | Only full closed-state reversal erases all witnesses; partial reversal leaves records. |
| Multi-time theories exist. | Yes, as different constrained support surfaces, not retained one-clock data. |
| Durable records are underived. | Correct; this lane assumes formed physical records and does not close measurement. |
| This proves only by assumption. | Correct; it is a conditional boundary theorem and import classifier. |

## Safe Final Formulation

Use:

> The retained framework admits reversible reconstruction and external
> time-nonlocal theory surfaces, but it does not provide an operational channel
> by which a choice at `t1` changes an earlier durable record at `t0 < t1` on
> the retained single-clock local-data surface.

Avoid:

- "time travel is impossible"
- "CTCs are disproven"
- "postselection is invalid"
- "advanced fields are false"
- "CPT forbids backward causation"
- "durable records have now been fully derived"

## Review Commands

```bash
python3 -m py_compile \
  scripts/chronology_cycle_insertion_probe.py \
  scripts/loschmidt_echo_record_probe.py \
  scripts/advanced_vs_retarded_field_probe.py \
  scripts/causal_cycle_fixed_point_dimension_probe.py \
  scripts/postselection_ctc_nonlinearity_probe.py \
  scripts/postselection_no_signaling_audit.py \
  scripts/future_boundary_import_index.py \
  scripts/partial_loschmidt_record_lower_bound.py \
  scripts/chronology_import_budget.py \
  scripts/ctc_fixed_point_taxonomy_probe.py \
  scripts/multi_time_support_constraint_probe.py \
  scripts/chronology_operator_algebra_no_past_signal_probe.py \
  scripts/durable_record_formation_boundary_probe.py \
  scripts/chronology_protection_suite.py
python3 scripts/chronology_protection_suite.py
```
