# Cycle 03 — Route R1: ABJ-to-inconsistency derived for the framework

**Date:** 2026-05-02
**Route attempted:** R1 (anomaly → inconsistency on the framework's surface)
**Goal:** Replace the literature ABJ inconsistency claim with a
framework-internal proof using only retained-clean inputs.

## Context

The bounded theorem invokes Adler 1969 / Bell-Jackiw 1969 to claim:
"three nonzero anomaly coefficients ⇒ Ward identities break,
longitudinal gauge boson modes fail to decouple, theory is inconsistent."

This is currently a literature import.

## What we have available (retained-clean)

To close ABJ-to-inconsistency on the framework's actual current surface,
we may load only:

1. `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (positive)
2. `axiom_first_coleman_mermin_wagner_theorem_note_2026-04-29` (positive)
3. `cpt_exact_note` (positive)
4. `cl3_color_automorphism_theorem` (positive)
5. `physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30` (positive)

Plus retained_bounded primitives:
- `staggered_dag_note_2026-04-10`
- `staggered_fermion_card_2026-04-10`
- `native_gauge_closure_note`
- `graph_first_su3_integration_note`

## What we do NOT have available

- The axiom-first cluster's reflection positivity / spectrum condition /
  microcausality / KMS notes are all `unaudited`. They cannot be loaded
  as load-bearing inputs in a retained-positive proof.
- `physical_lattice_necessity_note` is `unaudited / no_go classification`
  (the framework's "graph and unitary are one irreducible physical object"
  upgrade). Not retained-clean.
- `axiom_first_lattice_noether_theorem_note_2026-04-29` is `unaudited`.
  No retained-clean Noether theorem on the surface.
- The upstream anomaly companion notes (Witten Z_2, SU(3)^3 cubic,
  hypercharge uniqueness) are all `audited_conditional` or `unaudited`.
- The Cl(3) is a *spatial* algebra in the framework, not a spacetime
  Clifford. There is no retained-clean lattice ABJ derivation in the repo.

## The honest gap

To say "the LH-content's nonzero anomaly traces force inconsistency
*on the framework's lattice surface*" requires something like:

(a) A lattice version of the Adler identity that says: in the
    framework's discretization, the divergence of the gauge current
    has a nonzero anomalous term proportional to the anomaly trace.
(b) A theorem that says: a nonzero gauge-current divergence is
    inconsistent with the framework's Hilbert/locality structure
    (e.g., breaks unitarity at the level of physical states).

The framework has neither (a) nor (b) on retained-clean primitives.

Step (a) would require a retained Wess-Zumino consistency or Fujikawa-
style measure-non-invariance derivation on Z^3 — none exist.

Step (b) would require a retained gauge invariance theorem that says
"physical states are gauge-invariant; nonzero current divergence
contradicts invariance." The retained `native_gauge_closure_note` is
bounded, not retained-positive, and does not contain such a step.

## What CAN be said honestly

What the framework *can* say with retained-clean inputs:

1. **The LH content's anomaly arithmetic is exactly as catalogued.**
   The numerical traces (-16/9 cubic, 1/3 mixed SU(3)^2 Y) are
   computed inside the framework on the retained left-handed content,
   and verified by an internal runner
   (`scripts/frontier_lh_anomaly_trace_catalog.py`, PASS=26 FAIL=0).
   But the *meaning* of "nonzero anomaly trace ⇒ theory is inconsistent"
   still imports the ABJ machinery.

2. **The framework wants a chiral gauge theory.** The accepted gauge
   sector is SU(2)_L × SU(3)_C × U(1)_Y with chiral matter. If anomalies
   were not cancelled, then either (i) the framework would have to be
   reinterpreted as a non-chiral / vector-like gauge theory, contradicting
   the retained chirality grading from Cycle 1; or (ii) the framework
   would have to be a non-gauge theory, contradicting the retained gauge
   closure.

3. **Anomaly cancellation is therefore *internally* mandatory** in the
   sense that any other choice contradicts retained framework structure.
   But the *proof* that anomalies are equivalent to gauge inconsistency
   (the ABJ → Ward identity → unitarity violation chain) remains an
   import.

## Possible derivation path (not closed in this cycle)

A future retained-positive derivation of admission #1 could go through:

(i) A retained reflection-positivity theorem on the lattice (currently
    `axiom_first_reflection_positivity_theorem_note_2026-04-29`,
    unaudited). Reflection positivity gives unitarity at the level of
    transfer matrix.

(ii) A retained Lieb-Robinson / microcausality theorem on the lattice
     (currently `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01`,
     unaudited).

(iii) A retained finite-volume Wess-Zumino consistency / Fujikawa-on-
      lattice derivation that ties the anomaly trace to the chiral measure
      Jacobian.

If those primitives were elevated to retained-clean, the ABJ-to-inconsistency
implication could be derived inside the framework. As of today (2026-05-02),
they are not.

## Outcome of Cycle 3 (Route R1)

**Not closed.** Admission #1 (ABJ inconsistency) **remains a literature
import** on the actual current retained-clean surface. The required
upstream primitives (reflection positivity, microcausality, Wess-Zumino
on the lattice) exist in the repo but are `unaudited`, not retained-clean.

**Status of admission #1:** still requires literature import. A path to
internal closure is sketched (cycle of upstream re-audits), but is not
in scope for one physics-loop cycle.

**Honest narrowing:** the residual literature import is now precisely
"ABJ axial anomaly ⇒ chiral gauge theory inconsistency in 3+1d" — i.e.,
the standard QFT result. This is much narrower than "any structural fact
about chirality / volume elements / Cauchy / unitarity"; the other 3
admissions can close on retained-clean inputs.

## Stretch attempt: alternate route via gauge invariance

Could we close R1 via a different argument — e.g., "the framework's
gauge sector is defined to be unitary, and a nonzero anomaly trace
contradicts unitarity by some lattice argument"?

The retained `native_gauge_closure_note` (bounded) gives the gauge
algebra emergence on the staggered surface but does *not* contain a
unitarity / Ward identity argument that would replace ABJ.

The retained `cpt_exact_note` gives CPT invariance but not gauge
invariance.

The retained `axiom_first_coleman_mermin_wagner_theorem_note_2026-04-29`
gives "no spontaneous breaking of continuous symmetries on Z^3 in d≤2"
which is not relevant to anomaly arithmetic.

None of these provide a retained-clean replacement for ABJ.

## Conclusion

**R1 remains an open literature import.** The bounded theorem must
keep "ABJ inconsistency for chiral gauge theories in 3+1d" as a
literature input until reflection positivity / microcausality / lattice
Wess-Zumino are themselves elevated to retained-clean.

The bounded scope is now sharply narrowed: only one literature
import remains (R1), and it is the standard QFT result that any
chiral gauge theory must satisfy anomaly cancellation.
